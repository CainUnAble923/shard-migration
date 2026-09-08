# S10 — The carrier family

**Status: done.** Completed 2026-09-08. Answers the build half of Q-037 and settles the gargish
base-class question it asked for. Raises Q-038 and Q-039.

Five carriers, five tests, **zero patches, zero migrations**. That last line is the claim the
approval rests on and section 3 is where a future bump confirms it.

---

## 1. Verdict

| Question | Answer |
|---|---|
| Built | `BaseSetWeapon`, `BaseSetJewel`, `BaseSetClothing`, `BaseSetQuiver`, `BaseSetShield`, all in `Items/Artifacts/Equipment/Armor/Sets/` beside `BaseSetArmor`. **1,426 lines** against the ~1,000 estimate; section 7 says where the extra 40% went. |
| Gated | `docker/uo/build.sh` green, **42 tests** (27 before, 15 new: three per carrier). Each carrier's gate was **watched fail**, section 5. |
| Patches | **Zero.** `server/patches/` is 15 files before and after. `apply-patches.sh` is untouched. |
| Migrations | **Zero.** `server/migrations/` is 9 files before and after. No upstream serialization version moves. Every new field is at our own version 0 on our own class. |
| Gargish bases | **Yes, re-parented onto `BaseSetArmor`**, all four, in this commit, before any instance exists in a save. Section 4 has the serialization consequence. |
| `NegativeAttributes` | Pinned ModernUO has **no such type** (`grep -rl NegativeAttributes Projects` is empty), so the carriers naturally provide nothing for it, and nothing was added. The 8 files that need it are still blocked on that, not on a carrier. |
| Deviations | Three, section 6. The one that matters: `SetSelfRepair` is **inert** on weapon, clothing and shield, because giving it effect is a patch. Q-038. |

**The shape was decided before S10 started, and it held.** `SetHelper.GetSetProperties` already
branched on `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseQuiver` and `BaseJewel`
(`SetItem.cs:62-78`), `AosAttributes.GetValue` already keyed on `ISetItem.LastEquipped`
(`AOS-set-attribute-aggregation.patch:10`), and `PlayerMobile.GetItemResistance` already keyed on
`ISetItem.SetEquipped`. Not one of the three changed. Each carrier is `BaseSetArmor` transcribed
against its own ModernUO base, with the parts ServUO does not have on that base left out.

---

## 2. What was built

### Additive — `server/customizations/Items/Artifacts/Equipment/Armor/Sets/`, 5 files, 1,426 lines

| File | Lines | ModernUO base | Fields | Set-specific shape, from the ServUO base it mirrors |
|---|---|---|---|---|
| `BaseSetWeapon.cs` | 245 | `BaseWeapon` (`[SerializationGenerator(10)]`) | 0-11 as `BaseSetArmor` | ServUO `BaseWeapon.cs:1214-1223, 1285-1288, 5524-5540, 6182-6186, 6640-6664`. No `MixedSet`, no `OnDragLift` (ServUO's weapon has neither; the other four bases have `OnDragLift`). `SetResistBonus` returns the weapon's own resistances. |
| `BaseSetJewel.cs` | 225 | `BaseJewel` (`[SerializationGenerator(4)]`) | 0-9, absorption at **10** | ServUO `BaseJewel.cs:708-720, 747-749, 834-850, 988-992, 1328-1337, 1520`. No `SetSelfRepair` in ServUO's jewel, so none here. Tooltip uses 1080240/1080241 (Jewelry Set). No `GetSetProperties` virtual; calls `SetHelper` directly, as ServUO does. |
| `BaseSetClothing.cs` | 367 | `BaseClothing` (`[SerializationGenerator(7)]`) | 0-11 as `BaseSetArmor` | ServUO `BaseClothing.cs:725-735, 754-757, 1082-1105, 1304-1309, 2014-2022, 2220-2300`. The full armour shape: per-piece and last-equipped resist arithmetic, `MixedSet`, `SetSelfRepair`. ServUO's clothing `GetSetProperties` puts the resist block first and `SetHelper` last, the reverse of its armour; reproduced as-is. |
| `BaseSetQuiver.cs` | 204 | `BaseQuiver : Container` (`[SerializationGenerator(1)]`) | 0-9, nothing after | ServUO `BaseQuiver.cs:435-444, 458-460, 466-475, 681-696, 711-715, 729-740`. No `SetSelfRepair` and **no absorption** in ServUO's quiver (`grep Absorption` on it is empty), so neither here. Not `IAbsorptionItem`. |
| `BaseSetShield.cs` | 385 | `BaseShield : BaseArmor` (`[SerializationGenerator(0)]`) | 0-11 as `BaseSetArmor` | `BaseSetArmor` transcribed. In ServUO a shield *is* a `BaseArmor` and inherits everything; here `BaseSetArmor` and `BaseShield` are siblings under `BaseArmor` and C# cannot be both, so the shield gets its own copy. Minus `EffectiveSelfRepair`, which `BaseShield.OnHit` never consults (section 6, D-1). |

**Field layout is the same on every carrier**, in this order: `SetAttributes` 0,
`SetSkillBonuses` 1, the five `Set*Bonus` 2-6, `SetHue` 7, `SetEquipped` 8, `LastEquipped` 9,
then `SetSelfRepair` 10 and `AbsorptionAttributes` 11 where the ServUO base has them. The jewel
has no 10, so its absorption is field 10. Every field has a save flag, so anything appended later
(`ReforgedSuffix` for CC4, say) needs no migration: an item saved before the field existed loads
with the default. `AbsorptionAttributesVerification.AbsorptionSurvivesASerializationRoundTrip`
proved that mechanism on `BaseSetArmor` in S6 and nothing about it is per-carrier.

### Changed — our own files, 4, +24/-4

`GargishEarrings`, `GargishNecklace` (with `GargishAmulet` and `GargishStoneAmulet` under it),
`GargishPlateChest`, `GargishPlateLegs`: `: BaseArmor` → `: BaseSetArmor`, plus a five-line
comment each pointing here. Section 4.

### Tests — 5 files, 967 lines, 15 facts

`server/tests/Items/Artifacts/Equipment/Armor/Sets/{Weapon,Jewel,Clothing,Quiver,Shield}SetCarrierVerification.cs`.
Each has the same three facts: a completed set reaches the mobile and breaks cleanly, a stock item
of that kind is unaffected, set state survives a serialization round trip.

The set pieces in the tests are **test-local subclasses**, because the real ones (Evocaricus, the
Luck rings, Cloak of Humility, Feathernock, Maleki's Honor) are CC9 batch 4's to port and the
brief drew that boundary hard. They carry the real pieces' values where those exist, plus a
test-only resist bonus or eater where the real piece has none, so that every path has something
to show. Two of them — the quiver's and the shield's partner piece — are on **`BaseSetArmor`**
rather than on another S10 carrier, so that each new carrier's gate depends only on itself and
on the S1 carrier that was already proven. It also means two of the five tests prove a set can
span two carriers, which every real mixed set (Juggernaut, Marksman, Virtue) relies on.

What each test drives, and through which hook:

| Test | Set attributes (AOS patch) | Resistances (Mobile hook) | Absorption | Hue swap | Stat mod |
|---|---|---|---|---|---|
| Weapon | `BonusStr`, `DefendChance` once; own `WeaponDamage` stacks x2 | own, unchanged | `EaterFire` 2x5 | yes | `SetStr` +10 |
| Jewel | `Luck` 2x150+100, `RegenHits`, `CastRecovery` | own (zero) | `EaterCold` 2x3 | yes | — |
| Clothing | `BonusMana` | **per-piece**: 2x(2+5) phys, 2x(3+5) cold | `EaterPoison` 2x4 | yes (Virtue's `SetHue = 0`) | — |
| Quiver | `AttackChance`; then re-ordered so the quiver is last-equipped and its own `WeaponDamage` 10+20 shows | own (zero) | n/a | yes | `SetDex` +8 |
| Shield | `DefendChance`; then re-ordered so the shield carries `WeaponSpeed` | **last-equipped**: 3x2+5 phys on one piece, 0 on the other; energy 3 → 0 → 6 | `EaterEnergy` | yes | `SetStr` +10 |

The quiver and shield tests re-order the pieces deliberately: with two carriers in one set, the
piece that completes the set is the one whose `SetAttributes` are aggregated, and the test proves
it both ways round.

---

## 3. Maintenance cost — what a pinned-commit bump has to reconcile

**Nothing new.** This is the section a future bump reads first, so it is short on purpose.

- **Patches added: 0.** `server/patches/` has the same 15 files. `apply-patches.sh` has the
  same `apply_patch` lines.
- **Upstream files changed: 0.** No replacement, no structural sed, no `.csproj` touch.
- **Upstream serialization versions bumped: 0.** `BaseWeapon` stays at 10, `BaseJewel` at 4,
  `BaseClothing` at 7, `BaseQuiver` at 1, `BaseShield` at 0.
- **Migrations added: 0.** `server/migrations/` has the same 9 files.
- **Upstream method bodies copied: 0.** No carrier override reimplements a ModernUO method; every
  override calls `base` and adds the set block around it.

What the carriers *do* depend on, all of it already on the S1 bump checklist
(`notes/s1-armour-sets.md` §3) and none of it new:

1. `Mobile-set-item-resistance-hook.patch` — the clothing and shield tests fail if it stops
   reaching `PlayerMobile.GetItemResistance`.
2. `AOS-set-attribute-aggregation.patch` — all five tests fail if `LastEquipped` stops being
   summed.
3. The five ModernUO base classes keeping the members each carrier overrides or reads:
   `OnAdded`/`OnRemoved`/`OnDragLift`/`GetProperties` (virtual on `Item`), the five
   `*Resistance` properties, and the `(int itemID)` / `(int itemID, Layer layer)` /
   `(int itemID, Layer layer, int hue)` / `(int itemID = 0x2FB7)` constructors. A change to any
   of those is a **compile error in our file**, which names itself. There is no silent case.

**Bump checklist for S10:** run `docker/uo/build.sh`. If a carrier fails to compile, the base
class signature moved; fix the carrier. If it compiles and its test fails, one of the two S1
patches is applying but no longer reaching the hook; that is S1's checklist, not this one.

---

## 4. The gargish base-class decision: yes, and applied

**Decided: the four ported gargish armour-class bases derive from `BaseSetArmor`.** Applied in
this commit to `GargishEarrings`, `GargishNecklace` (and through it `GargishAmulet` and
`GargishStoneAmulet`), `GargishPlateChest` and `GargishPlateLegs`.

**Why yes.** In ServUO every `BaseArmor` carries the set fields and the absorption fields; a piece
with `SetID == None` is inert. For a *ported* armour base, then, `BaseSetArmor` is the more
faithful parent, not the less: it is what the ServUO original actually has underneath it.
`TigerPeltAloneIsNotASetItem` (S1) is the proof that `None` is inert on our carrier. No test
constructs a gargish piece (CC9 shipped none, and S10 did not add one; see below), so the
evidence for the four is the S1 proof on the same base class plus a clean compile. It frees the 5 gargish-jewellery set pieces (`VirtuososEarpieces`, `VirtuososNecklace`,
`BestialArms/Earrings/Necklace`) and the 4 armour-class absorption users on these bases without a
sixth carrier, and it costs one token per file.

**The serialization consequence, written down.** A `[SerializationGenerator]` type serializes as
a chain: `Item`'s block, then each ancestor's block in order, then its own. Inserting
`BaseSetArmor` between `BaseArmor` and `GargishEarrings` inserts a block — version int plus a
save-flag mask, two bytes when every flag is clear — into the middle of every saved
`GargishEarrings`. That is **not expressible as a migration**: ModernUO's migration JSON describes
a type's own fields changing version, not a new ancestor appearing. An existing instance saved
under the old chain would misread from that point on. So the change is free exactly once, **before
any instance exists in a save**, and afterwards it costs a wipe of the type.

**That condition holds today, and this is the evidence.** The four types were ported in CC9 batch
1 (`d4ce1ce`, 2026-09-08). The live `sl-modernuo` container has been stopped since June
(`notes/cc9-artifacts.md` §10) and nothing has been deployed since; `sl-modernuo:latest` was
built 2026-09-07 02:49, before batch 1 existed. No live save can contain one. The scratch saves
from CC9's and S10's headless runs are throwaway and contain none either (the ClusterF seeders
build the world; none places a gargish piece). Doing this later, after a deploy, is the case Q-037
warned about, and it is why the change is in this commit rather than left for batch 4.

**What it changes at runtime for those four types: nothing observable.** `SetID` is `None`, so
`OnAdded`/`OnRemoved` fall through, `GetProperties` adds no line, `SetResistBonus` is never
consulted (the hook keys on `SetEquipped`), and `AosAttributes.GetValue` skips them (it keys on
`LastEquipped`). `AbsorptionAttributes` is empty and adds nothing. A stock-parity check for
`GargishEarrings` was not written because it would assert the same thing
`TigerPeltAloneIsNotASetItem` already asserts about the same base class.

**What this does not decide.** The same argument reaches `LargeStoneShield` (now that
`BaseSetShield` exists) and `GargishKatana`, `GargishDagger`, `GargishGnarledStaff` (now that
`BaseSetWeapon` exists). Q-037 scoped the decision to the four armour-class bases, so S10 stopped
there and raised the generalisation as **Q-039** with a recommendation to apply it as a rule
before `latest` is rebuilt. None of the five has a dependant that needs it today, so nothing is
blocked on the answer.

---

## 5. What was proved red

Per `AGENTS.md`: a gate nobody has watched fail is not a gate. **One run, all five carriers broken
at once, five failures, each attributed to its own carrier**; then restored and the gate run green.

**The break.** In each carrier's `OnAdded`, the single line `LastEquipped = true;` was deleted
(`%TEMP%\claude\s10\break.sh`, five `sed` deletions, one per file, each verified to remove exactly
one line). The set still completes and `AddSetBonus` still runs, so the carrier is *almost*
working; what breaks is that no piece marks itself as the attribute carrier, so the AOS patch sums
nothing and the stat mod is never added. It is the most plausible real regression: a bump that
reorders `OnAdded`, or a future edit that drops the line, leaves everything compiling and every
tooltip intact.

**The result: `Failed: 5`, `Passed: 37`, `BUILD FAILED: ShatteredLegacy.Tests tests did not
pass. No image was built.`, exit 1.** Wall clock 1 m 24 s. The five failures, each the
`Assert.True(<piece>.LastEquipped)` on the piece that completed the set, from the gate's own
output:

| Carrier | Failed test | Line | The piece |
|---|---|---|---|
| Weapon | `WeaponSetCarrierVerification.ACompletedWeaponSetReachesTheMobile` | `:88` | second sword |
| Jewel | `JewelSetCarrierVerification.ACompletedJewelSetReachesTheMobile` | `:101` | bracelet |
| Clothing | `ClothingSetCarrierVerification.ACompletedClothingSetReachesTheMobile` | `:112` | boots |
| Quiver | `QuiverSetCarrierVerification.ACompletedQuiverSetReachesTheMobile` | `:124` | **the re-worn quiver** |
| Shield | `ShieldSetCarrierVerification.ACompletedShieldSetReachesTheMobile` | `:144` | **the re-worn shield** |

The quiver and shield rows are the ones that show attribution. In those two tests the set is
first completed by the partner piece on **`BaseSetArmor`**, which was not broken, and that
assertion (`helm.LastEquipped` at `:98`, `chest.LastEquipped` at `:116`) **passed**; the test
then re-orders the pieces so the S10 carrier completes the set, and *that* assertion failed. The
break in each S10 carrier was caught by that carrier's own test at the first line that reads the
carrier's own state, with the S1 carrier still passing beside it in the same test. The other 37
tests, S1's, S2's, S5's, S6's and S8's among them, stayed green.

Every carrier was restored from the backup copies and the restored files are byte-identical to
the committed ones (`cmp` on all five). The clean gate then went green, section 8.

**Why one run rather than five.** Each test depends on its own carrier and, for the quiver and
shield, on `BaseSetArmor`, which was not broken. So one failure per carrier in one run is one
observation per gate, which is what the rule asks for; five separate runs would cost twenty
minutes to show the same five lines. S8 ran its proofs B and C the same way.

---

## 6. Deviations — deliberate, for `docs/fidelity-principle.md`

Three. D-1 is the only one a player could notice.

### D-1. `SetSelfRepair` is inert on `BaseSetWeapon`, `BaseSetClothing` and `BaseSetShield`

ServUO adds the set's self repair to the item's own at the durability roll: `BaseWeapon.cs:2320`,
`BaseClothing.cs:789`, and for shields through `BaseArmor`. S1 gave *armour* that through
`BaseArmor-set-self-repair.patch`, a three-line `EffectiveSelfRepair` hook. Pinned ModernUO has
no such hook on the other three: `Items/Weapons/BaseWeapon.cs:2088` and
`Items/Clothing/BaseClothing.cs:351` read `SelfRepair` directly inside `OnHit`, and
`Items/Shields/BaseShield.cs:35` is an `OnHit` override of its own that never consults
`BaseArmor.EffectiveSelfRepair`, so S1's hook does not reach a shield either.

Closing it is three patches in the S1 shape, one per base, and S10 was approved on zero. So:

- the field is **kept** — stored, serialized, settable — so Evocaricus (`3`), Cloak of Humility
  (`5`) and Maleki's Honor (`3`) compile in batch 4 and keep their value in the save;
- its effect is **absent**;
- its tooltip line (`1060450`, "self repair ~1_val~") is **not emitted**, per S1's D-2:
  advertising a bonus the player does not get is worse than omitting it.

Effect lost: a completed Juggernaut or Virtue set does not self-repair its weapon, cloak or
shield. Armour pieces of the same sets still do. Jewellery and quivers have no `SetSelfRepair` in
ServUO either. **Cost to close:** three patches of one to three lines each, listed with their
upstream line numbers in Q-038, plus restoring the three commented-out tooltip lines. Raised as
**Q-038** rather than done, because it changes the basis on which S10 was approved.

### D-2. The Bestial berserk line is not emitted

ServUO's set header on every base adds `1151541` ("Berserk ~1_VAL~") through
`BestialSetHelper.GetTotalBerserk`, a `Timer`-based helper S1 did not port and CC9 batch 2 lists
under the Bestial pieces as "needs reading". `BaseSetArmor` already omits the line for the same
reason; the five carriers follow it. Unreachable for any set on the shard until Bestial is ported,
at which point `BestialSetHelper` and the line come together.

### D-3. Property-list ordering, cosmetic

Same judgement as S1's D-4 and S6's absorption block: ServUO emits the set header inside each
base's `AddNameProperties`/`GetProperties` at a fixed spot; ModernUO's bases have no hook there,
so each carrier emits the header before `base.GetProperties` and the "Only when full set is
present" block and absorption block after it. Same clilocs, same values, a few lines lower.

**Reproduced, not deviated, and worth knowing:** ServUO's `BaseClothing.GetSetProperties` adds
`1151571` ("Mastery Bonus Cooldown: 15 min.") for a Virtuoso piece while the set is incomplete,
and `SetHelper.GetSetProperties` adds the same line again. A Virtuoso's Cap on ServUO shows it
twice; so does ours. The carrier carries a comment saying so.

---

## 7. Where the extra 40% went

Estimated ~250 lines per carrier, ~1,000 total. Actual 1,426. The estimate was measured against
`BaseSetArmor`'s 394 and assumed the other kinds were lighter, which is true of three of them:

| Carrier | Lines | Why |
|---|---|---|
| Quiver | 204 | fields 0-9 only, no self repair, no absorption, no resist arithmetic |
| Jewel | 225 | no self repair, no resist arithmetic |
| Weapon | 245 | no resist arithmetic, no `OnDragLift` |
| Clothing | 367 | **the full armour shape**: ServUO's clothing has the per-piece and last-equipped resist arithmetic, 130 lines of it |
| Shield | 385 | **a copy of `BaseSetArmor`**, because a ModernUO shield is a `BaseArmor` but not a `BaseSetArmor` |

The shield was the one nobody had costed: Q-037 said "a shield carrier" without a number, and the
honest number is `BaseSetArmor` again. The alternative was to factor the resist arithmetic into a
helper shared by armour, shield and clothing, saving ~250 lines across the three. Not done:
it would have changed `BaseSetArmor`, a proven S1 file, inside a task whose value is that it
patches nothing and disturbs nothing. If a fourth armour-shaped carrier ever appears, factor it
then.

---

## 8. Verification

Headless throughout. No client, not on Chase's machine, `--network=none` on every test container
and on the runtime run, scratch files under `%TEMP%\claude\s10`. Nothing touched the live stack,
`Saves/`, `Accounts/`, `docs/`, or the uncommitted `docker-compose.yml` (Q-009). Nothing deployed,
nothing started or restarted. `D:\UO\ModernUO-pinned` and `D:\UO\ServUO-pub57` were read only.

| Cycle | What | Result | Wall clock |
|---|---|---|---|
| 1 | `build.sh --tests-only`, first attempt | **Compile error in two tests**, not in any carrier: the two test-local `BaseSetArmor` stand-ins lacked `MaterialType`, which `BaseArmor` declares abstract. All five carriers and the four re-parented gargish bases compiled clean first time. | 30 s to the error |
| 2 | `build.sh --tests-only`, fixed | **42 passed**, 15 patches applied, 159 structured customizations, 11 test files | 1 m 24 s |
| 3 | `build.sh --tests-only`, all five carriers broken | **5 failed, 37 passed, `BUILD FAILED`, exit 1**; section 5 | 1 m 24 s |
| 4 | `build.sh -t sl-modernuo:s10`, restored | **42 passed**, `sl-modernuo:s10` built, exit 0 | 1 m 35 s |

**Runtime, real server, two runs of `sl-modernuo:s10`.** `--network=none`, loopback listeners
only (`127.0.0.1:2593`), scratch `Saves/Backups/Archives/Configuration` under
`%TEMP%\claude\s10\run` with `autosave.enabled` off, the CC2 recipe verbatim (`notes/cc2-timed-port.md`, "Scratch
environment"):

- **Run 1**, fresh world: *Loading world done (617 items, 90 mobiles)*, *Listening:
  127.0.0.1:2593*, `save` → *Writing world save snapshot done (0.24 seconds)*, `shutdown` → exit 0.
- **Run 2**, same `Saves/`: *Loading world done (621 items, 91 mobiles)*, listens, saves again
  (0.49 s), exit 0.
- **Zero** `exception`/`ERR`/`FATAL` lines in either log.

What this proves is what S1's runs proved: the assembly with five new `[SerializationGenerator]`
types and four re-parented ones starts, saves and reloads. It does not exercise a carrier
instance, because the console has no way to create an item without a client; the tests are where
the carriers are exercised. Neither run touched the live stack; the containers were `--rm` and are
gone.

**Read, not just compiled.** Each carrier was checked line by line against the ServUO base it
mirrors (line references in section 2) and against the ModernUO base it extends: constructor
signature, which hooks the base already overrides and whether it calls `base` (ModernUO's
`BaseWeapon.OnRemoved` returns early for a non-`Mobile` parent; `BaseJewel.OnAdded` and
`BaseQuiver.OnAdded` do not call `base`; each carrier calls `base` first regardless, which is
safe because `Item.OnAdded` is empty), and where `SelfRepair` is read. That last check is what
found D-1 on the shield: `BaseShield.OnHit` looked covered by S1's patch until it was opened.

---

## 9. What it cost

| Phase | Wall clock |
|---|---|
| Read `AGENTS.md`, `subsystem-policy.md`, `fidelity-principle.md`, S1/S6/S8 notes, Q-037, CC9 §4-5 | ~8 min |
| Source study: ServUO's set regions on four bases plus `BaseShield`; ModernUO's five bases, `Item` virtuals, test project shape, `NegativeAttributes` (absent), `SelfRepair` read sites | ~12 min |
| Write five carriers | ~10 min |
| Write five tests, re-parent four gargish bases | ~8 min |
| Build cycle 1 (compile error in tests), fix | ~3 min |
| Build cycle 2, green | ~2 min |
| Red proof: break, build cycle 3, restore, verify | ~4 min |
| Build cycle 4 (image), two runtime runs | ~6 min |
| Note, questions, progress | ~12 min |
| **Total** | **~65 min** |

Two things made it this cheap, and both are S1's: the interface-and-patch plumbing was already
kind-agnostic, and "check every type against `ModernUO-pinned` before writing a line" meant the
carriers compiled first time. The one build-fix cycle was in a test, and it was a base-class
abstract member the S1 test never had to think about because Aloron's pieces inherit it.

---

## 10. What S10 leaves for later

- **CC9 batch 4** can start: the 13 set pieces, the 9 non-armour absorption users and the 5
  gargish-jewellery set pieces from `notes/cc9-artifacts.md` §4 all have a parent now. Each is
  the Greymist re-parent shape: derive from the carrier, reproduce the stock parent's members.
  Bestial additionally needs `BestialSetHelper` (D-2); Fisherman needs `IFishingAttire`.
- **CC4** has its `ReforgedSuffix` route C: a `_reforgedSuffix` field appended to each of the six
  carriers, save-flagged, no migration, plus the ~60 lines of naming. Not built here, per the brief.
- **Q-038**: the three self-repair hooks. **Q-039**: the gargish rule generalised.
- **`SetHelper.GetSetSlayer`** is still absent (S1 D-2). With `BaseSetWeapon` in place the weapon
  half of restoring it is reachable; the `SlayerName` half is not. Unchanged by S10.
