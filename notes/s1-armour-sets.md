# S1 — Armour set-bonus subsystem

**Status: the feasibility spike PASSED, and the content on top of it is done.**
Completed 2026-09-07. Reverses the CC3 decline of the eight Aloron armour pieces.

The whole task — spike, subsystem, 16 content files, four verification runs — took **30 minutes**.
That number is real but it is not a template; see *What it actually cost* at the bottom for why.

---

## 1. The spike, and its verdict

The brief said to stop if any of three things were true. None of them is.

| Stop condition | Verdict | Evidence |
|---|---|---|
| Needs more than targeted patches | **No.** Three patches, 44 added lines total, none rewriting upstream logic. | `server/patches/*set*.patch` |
| Plumbing touches so much of a base class that the next pinned-commit bump is unreconcilable | **No.** Zero fields added to any upstream class; zero upstream serialization versions bumped. | §3 |
| Property/attribute model differs enough that faithful behaviour is unreachable | **No.** `AosAttributes`, `AosSkillBonuses`, `StatMod`, `ResistanceType` and every cliloc the system uses exist in ModernUO under the same names. | §5 |

**The 187:1 unblock ratio in `docs/subsystem-policy.md` was measured against the right thing.**
It also understated the cost by one file and overstated it in a different way: `SetItem.cs` alone is
inert, but the plumbing it needed turned out to be three hooks, not a fork.

### The one decision that made it cheap

ServUO puts set state directly on `BaseArmor`, `BaseWeapon`, `BaseJewel`, `BaseClothing` and
`BaseQuiver`. Doing that here would mean **bumping `BaseArmor`'s `[SerializationGenerator(9)]` to 10
and writing a migration for a file ModernUO maintains** — the single most expensive thing this repo
could do to itself, and precisely the "unreconcilable on bump" failure the brief warned about.

Instead the state lives on **`BaseSetArmor : BaseArmor, ISetItem`**, an additive abstract class of
ours at its own serialization version 0. Ported set content derives from it; stock ModernUO armour is
untouched.

This is not an approximation. In ServUO every armour piece carries the set fields and pieces with
`SetID == SetItem.None` are inert — so the only behavioural difference is that a *stock ModernUO*
armour item can never become a set item. **No stock ModernUO armour is a set item**, so nothing is
lost. Verified: `StockArmourIsUnaffected` in the harness (§4).

---

## 2. What was built

### Additive (`server/customizations/`) — 19 files, 1,451 lines

| File | Lines | What |
|---|---|---|
| `Items/Artifacts/Equipment/Armor/Sets/SetItem.cs` | 457 | Port of ServUO `Items/Artifacts/Equipment/Armor/Sets/SetItem.cs` (387). The `SetItem` enum, `ISetItem`, `SetHelper`. |
| `Items/Artifacts/Equipment/Armor/Sets/BaseSetArmor.cs` | 365 | The plumbing ServUO puts inside `BaseArmor`: fields, serialization, `OnAdded`/`OnRemoved`/`OnDragLift`, `GetProperties`, `GetSetProperties`, `SetResistBonus`. |
| `Mobiles/PlayerMobileSetResistances.cs` | 21 | Additive `partial class PlayerMobile` overriding the resistance hook. **No patch needed — `PlayerMobile` is already `partial` and is not source-generated.** |
| `Items/Armor/TigerPelt*.cs` (8) | 296 | The TigerPelt armour the Aloron pieces derive from. |
| `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/Alorons*.cs` (8) | 312 | The eight Aloron pieces. |

### Patched upstream — 3 files, 44 added lines, 6 changed lines

Registered in `docker/uo/apply-patches.sh` after `SmallSmithBOD-PostValorite.patch`.
**This is the list §3 is about. It is the whole of it.**

---

## 3. Maintenance cost — what a pinned-commit bump has to reconcile

**This is the first thing we have built that ModernUO will not maintain for us.** Nobody else tracks
this. Read it before bumping `MODERNUO_COMMIT` in `docker/uo/Dockerfile`.

The good news first: `apply-patches.sh` is a hard gate since F2, so **every one of these fails the
build loudly rather than drifting silently.** There is no copied-upstream-logic anywhere in S1 — no
override reimplements a ModernUO method body — so there is no category of silent drift to watch for.

### Patch 1 — `Mobile-set-item-resistance-hook.patch`

- **File:** `Projects/Server/Mobiles/Mobile.cs` — **core server project, not UOContent.** The only
  patch this repo has outside `Projects/UOContent`.
- **Change:** adds `public virtual int GetItemResistance(Item item, ResistanceType type)` (14 lines)
  and rewrites the five `Resistances[n] += item.XResistance;` lines inside `ComputeResistances()` to
  route through it.
- **Assumes about upstream:** that `ComputeResistances()` still sums equipped-item resistances with
  those five statements verbatim, in that order, inside that loop.
- **A bump breaks it if:** ModernUO restructures `ComputeResistances`, renames it, moves resistance
  aggregation elsewhere, or changes `Resistances` from an `int[]`.
- **If it fails:** re-derive the hook at wherever the loop now lives. The patch adds behaviour to no
  one — with no `ISetItem` equipped, `GetItemResistance` returns exactly what the removed lines did.
- **Why it exists:** `ISetItem` is declared in `UOContent`, which `Server` cannot reference.
  ServUO applies set resistances in `PlayerMobile.ComputeResistances`; ModernUO's lives on `Mobile`
  in the core project, so the decision is delegated up to `PlayerMobile` through a virtual.

### Patch 2 — `AOS-set-attribute-aggregation.patch`

- **File:** `Projects/UOContent/Misc/AOS.cs`, in `AosAttributes.GetValue(Mobile, AosAttribute)`.
- **Change:** 13 added lines, no lines changed. An `if (obj is ISetItem { LastEquipped: true })`
  block immediately after `var obj = items[i];`.
- **Assumes about upstream:** that `AosAttributes.GetValue` still iterates `m.Items` with
  `var obj = items[i];` as the first statement of the loop body.
- **Deliberately placed at the TOP of the loop, not the bottom.** `AOS-pet-mimic-attribute-aggregation.patch`
  already appends to the *end* of the same `if/else if` chain (~70 lines below). Putting this one at
  the bottom too would have made the two patches share a hunk and given us an ordering dependency.
  They are now independent, and `patch` resolves both by context. **Do not move this block down.**
- **A bump breaks it if:** ModernUO rewrites the aggregation loop (e.g. to a LINQ or switch form).
- **Faithfulness note:** ServUO puts its equivalent block at the *bottom* of the same loop. The
  contributions are summed, so position is behaviourally irrelevant.

### Patch 3 — `BaseArmor-set-self-repair.patch`

- **File:** `Projects/UOContent/Items/Armor/BaseArmor.cs`.
- **Change:** adds `public virtual int EffectiveSelfRepair => ArmorAttributes.SelfRepair;` (3 lines)
  and points the one call site in `OnHit` at it instead of `ArmorAttributes.SelfRepair`.
- **Assumes about upstream:** that `BaseArmor.OnHit` still reads self-repair through the literal
  expression `Core.AOS && ArmorAttributes.SelfRepair > Utility.Random(10)`.
- **A bump breaks it if:** ModernUO changes its self-repair formula. It very well might — see the
  deviation in §5, ModernUO's and ServUO's self-repair mechanics already differ.
- **If it fails:** re-point the hook at the new call site, or drop the patch and accept the
  `SetSelfRepair` deviation instead. `BaseSetArmor.EffectiveSelfRepair` is the only override.

### What a bump does NOT have to reconcile

- No upstream serialization version is bumped, so **no upstream migration JSON is ours to maintain.**
- No upstream class gains a field.
- `PlayerMobileSetResistances.cs` is an additive `partial` and needs no patch — but it will fail to
  compile (loudly) if ModernUO ever gives `PlayerMobile` its own `GetItemResistance` or makes
  `PlayerMobile` source-generated in a way that conflicts. That is a compile error, not silent drift.

### Bump checklist

1. `docker build` — a failed patch now fails the build (F2).
2. Re-run the verification harness in §4. All four tests must pass.
3. If patch 1 fails, check `ComputeResistances` first; it is the most structural of the three.

---

## 4. Verification — what was actually proven, and how

Everything below is headless. No client, not on Chase's machine, loopback-only containers, scratch
save directory under `%TEMP%\claude\s1run`. Nothing touched the live stack, `Saves/`, `Accounts/`,
or the uncommitted `docker-compose.yml` (Q-009).

### Build

Clean Docker build from pinned `7c9215d97`, **all 12 patches applied**, zero errors, and no warning
from any of our files (the build's one warning, NETSDK1194 about `--output` on a solution, is
pre-existing and upstream). Publish step 41 s, whole build 53 s. (CC3 recorded ~17 min; that was a cold layer
cache. With the ModernUO clone and .NET SDK layers warm, a build cycle here is under a minute —
worth knowing before anyone sizes a task around build cost again.)

### Runtime, real server

Two runs of `sl-modernuo:s1`, `--network=none`, scratch Saves/Backups/Archives, scratch
`Configuration` with `listeners: ["127.0.0.1:2593"]`:

- **Run 1** — server starts, listens, `save` → *"Writing world save snapshot done (0.32 seconds)"*,
  `shutdown` → exit 0.
- **Run 2** — same image, same Saves directory → *"Loading world done (622 items, 91 mobiles)"*,
  saves again, exits 0. **No exceptions in either run.**

### Set behaviour, xunit harness

The real server's console has only `save`, `shutdown` and `restart` — there is **no way to create an
item without a client**, so the live runs prove start/save/reload with the new assembly but cannot
prove set behaviour. That was done with a throwaway xunit file against ModernUO's own
`UOContentFixture`, which boots a full world headless.

The harness is **not committed** — it would land in `Projects/UOContent.Tests`, which
`apply-patches.sh` has no route for, and building one would be scope creep. It is kept at
`%TEMP%\claude\s1verify\ArmourSetBonusVerification.cs` and reproduced by:

```
docker build -f docker/uo/Dockerfile --target builder -t sl-uo-builder:s1 .
docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "<dir>:/verify:ro" -w /build/modernuo sl-uo-builder:s1 bash -c \
  "cp /verify/ArmourSetBonusVerification.cs Projects/UOContent.Tests/Tests/ && \
   dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release \
   --filter FullyQualifiedName~ArmourSetBonusVerification --logger 'console;verbosity=detailed'"
```

`--security-opt seccomp=unconfined` is required: `NetState.Configure()` needs `io_uring`, which
Docker Desktop's default seccomp profile blocks. `docker/uo/docker-compose.yml` already sets the same
option for the same reason, so this is not a new requirement.

**Four tests, all passing.** The measured output:

| Check | Result |
|---|---|
| One piece worn | `SetID=Aloron Pieces=4 IsSetItem=True SetEquipped=False`, resists 7/7/6/7/7 |
| Four pieces worn | `SetEquipped=True` on all four; `LastEquipped=True` on **exactly one** |
| Set attributes reach the mobile | `AosAttributes.GetValue` → `BonusMana=15`, `LowerManaCost=20` (patch 2) |
| Per-piece attributes still stack | `BonusDex=16` = 4 pieces × 4 |
| Set resistances reach the mobile | 60/60/60/60/60 = 4 × (base + set bonus) (patch 1) |
| Per-piece resist maths | `tunic.SetResistBonus(Physical)` = 7 + 8 = 15, `(Cold)` = 6 + 9 = 15 |
| Set self repair | `ArmorAttributes.SelfRepair=0`, `EffectiveSelfRepair=3` (patch 3) |
| Breaking the set | phys back to 21, `BonusMana=0`, `SetEquipped=False` on every piece |
| Serialization round trip | `SetEquipped`, `LastEquipped`, `SetHue=1234`, `SetSelfRepair=3`, `SetPhysicalBonus=8`, `SetColdBonus=9`, `SetAttributes.BonusMana=15`, `SetAttributes.LowerManaCost=20` all survive |
| Stock `LeatherChest` | not `ISetItem`, phys 2, `BonusMana=0` — unaffected |
| Bare `TigerPeltChest` | `SetID=None`, `IsSetItem=False`, phys 2 — inert, exactly as ServUO |

**"At least one set item verified to carry its set attributes" is met, and then some.**

---

## 5. Deviations — deliberate, for `docs/fidelity-principle.md`

Four. Chase to log. Each is *omission*, never approximation, per "prefer turning a system off over
running it differently".

### D-1. `AbsorptionAttributes.EaterCold = 2` is omitted from all eight Aloron pieces

ServUO's property is `SAAbsorptionAttributes` (`Scripts/Misc/AOS.cs:2753`), the Stygian Abyss damage-
eater system. ModernUO has **zero** of it. It is not a leaf dependency: its `GetValue` pulls in
`Enhancement`, `RunicReforging` and `SkillMasterySpell`, three further subsystems ModernUO also
lacks. That is a separate task with its own ratio, not something to smuggle into S1.

Effect lost: 2% cold damage eaten per piece. **Cost to close:** cost `SAAbsorptionAttributes` and its
damage-time hook as its own subsystem — a good candidate for S3's costed menu.

### D-2. Aloron's Dinosaur Slayer is omitted — *both the effect and the tooltip line*

ServUO's `SetHelper.GetSetSlayer` returns `SlayerName.Dinosaur` for a completed Aloron set and
`SlayerName.Myrmidex` for Darden. ModernUO's `SlayerName` enum has neither, and the method's only
consumers are three call sites in `BaseWeapon` combat code — weapon plumbing, outside an armour
spike. `GetSetSlayer` is therefore **not present** in our `SetItem.cs`.

**The `list.Add(1156345); // Dinosaur Slayer` line is dropped from the items too.** Keeping the
tooltip while the effect does nothing would advertise a bonus the player does not get, which is worse
than the item simply not having it.

**Cost to close:** append `Dinosaur` (and `Myrmidex`) to `SlayerName`, add `SlayerGroup` entries
listing the dinosaur types (we already ship Allosaurus, Raptor, Najasaurus, Dimetrosaur,
Archaeosaurus, Saurosaurus from CC3), restore `GetSetSlayer`, and patch `BaseWeapon.CheckSlayers` to
take the set slayer. Roughly a half-day, and it also unblocks the Darden set.

### D-3. `SetSelfRepair` follows ModernUO's self-repair mechanic, not ServUO's

Patch 3 makes `SetSelfRepair` *contribute* faithfully — the set's self repair is added to the
armour's own at the same point ServUO adds it. But the two emulators' self-repair formulas already
differ and this is not ours to reconcile:

- ServUO: `HitPoints += selfRepair` on a 60-second cooldown, chance 25% (80% if Antique).
- ModernUO: `SelfRepair > Utility.Random(10)` → `HitPoints += 2`, chance 25%.

This is a **pre-existing emulator difference**, not something S1 introduced. Recorded so nobody
later reads the Aloron self-repair as a porting error.

### D-4. Property-list ordering differs slightly

ServUO emits the set block inside `AddNameProperties`, between the gorgon-lens line and the damage-
type line. ModernUO splits `AddNameProperty` from `GetProperties`, so ours emits the header block
before `base.GetProperties(list)` and the "Only when full set is present" block after it. Same
cliloc numbers, same values, slightly different order within the tooltip. Cosmetic.

Also omitted from `SetHelper.GetSetProperties`: the `IFishingAttire` branch. ModernUO has no such
interface and it belongs to the Fisherman set, which we are not porting. It is unreachable for our
content.

---

## 6. Corrections to `notes/cc3-eodon.md`

CC3's decline evidence was right about the blocker and **wrong about the scope**, in our favour.

1. **"They also inherit from the TigerPelt armour set … itself set-bonus content" — false.**
   Verified: `grep SetID Scripts/Items/Equipment/Armor/TigerPelt*.cs` returns **nothing**. All eight
   TigerPelt files are plain `BaseArmor` subclasses with no set data at all. They are ordinary leaf
   armour and would have ported on any day of CC3. `TigerPeltAloneIsNotASetItem` proves it at runtime.
   The "8 more unlisted files" were 8 free files, not 8 more blocked ones.

2. **"Carrying `SetItem.cs` (388 lines) across would not fix it — that file is the enum and the
   bonus tables, not the `BaseArmor` plumbing that reads them" — true, and the right instinct.**
   It was also the whole of the difficulty: the plumbing is 365 lines in one additive class plus
   44 patch lines. CC3 correctly identified the question and simply did not cost the answer.

3. **The file is 387 lines, not 388.** `docs/subsystem-policy.md` has it right.

---

## 7. What it actually cost

| Phase | Wall clock |
|---|---|
| Read `AGENTS.md`, `docs/tasks.md`, `docs/subsystem-policy.md`, CC3 decline evidence | ~4 min |
| Source study — ServUO `SetItem.cs` + `BaseArmor` set regions, then **checking every type and signature against `D:\UO\ModernUO-pinned` before writing a line** | ~10 min |
| Write the subsystem (3 files), generate the 3 patches, register them | ~5 min |
| Write 16 content files (scripted from a table — they are near-identical) | ~2 min |
| Docker build | 53 s |
| Write and run the verification harness, 3 iterations | ~7 min |
| Two live server runs (start / save / shutdown / reload) | ~7 min |
| **Total to a passing spike with all content ported** | **~30 min** |

**Do not size the next subsystem against this.** Three things made it cheap and none is guaranteed
to repeat:

- **The design decision in §1 removed the expensive half of the task before it was written.** Most of
  the 10-minute source-study phase was spent finding it. That is where subsystem work lives.
- **The 16 content files are eight near-identical pairs.** They were generated from a data table.
  `docs/tasks.md` already warns that CC3's 0:30/file came from homogeneous content; this is more so.
- **The build cache was warm.** 53 s versus CC3's ~17 min is the layer cache, not our code.

The genuinely transferable lesson: **check every type against `ModernUO-pinned` before writing a
line.** Twenty-four new files and three patches compiled on the first attempt, with no build-fix
cycle at all. `AGENTS.md` already says to do this; this is the first task where it paid in full.

---

## 8. What S1 leaves for later

Not blockers, not silently skipped — deliberately out of scope, with the shape of each recorded.

- **`BaseSetWeapon`, `BaseSetJewel`, `BaseSetClothing`, `BaseSetQuiver`.** `SetHelper` already
  handles all five item kinds (`GetSetProperties` branches on each, `SetCraftedWith` on weapons).
  Each is a copy of `BaseSetArmor` against its own base class, plus — for weapons — the
  `MixedSet` clilocs that are already wired. **`ISetItem` and patches 1 and 2 are kind-agnostic and
  need no further change.** Only patch 3 is armour-specific.
- **The other 20 sets in the `SetItem` enum.** Acolyte, Assassin, Darkwood, Grizzle, Hunter,
  Juggernaut, Mage, Marksman, Myrmidon, Necromancer, Paladin, Virtue, Luck, Knights, Scout,
  Sorcerer, Initiation, Fisherman, Luck2, Bestial, Virtuoso, Darden. `Scripts/Items/Artifacts/Equipment/Armor/Sets/`
  is where they live. Armour-only sets are pure content now. Sets with weapons or jewellery wait on
  the classes above. Bestial additionally needs `BestialSetHelper`; Fisherman needs `IFishingAttire`.
- **The `187` figure has not been re-counted.** It came from `docs/subsystem-policy.md` and is a
  grep across ServUO for `SetItem` / `SetAttributes` / `AbsorptionAttributes`. Some share of those
  187 are `AbsorptionAttributes`-only and are blocked by D-1, not by S1. Given this project's record
  on unverified counts — three for three wrong — **that split should be measured in S3 before anyone
  quotes 187 again.**
