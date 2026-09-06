# CC2 — second port, timed

Date: 2026-09-06. Agent: Claude Code, headless. Pinned ModernUO `7c9215d97`.
Creature: `GreaterPoisonElemental`, ServUO `Scripts/Mobiles/Normal` →
`server/customizations/Mobiles/Normal/GreaterPoisonElemental.cs`. 123 lines to 80.

**The deliverable is the timing, not the creature.** Recipe corrections are in
`notes/port-recipe.md`; this file is the clock, the method and the batch estimate.

Nothing was deployed. The live `sl-modernuo` container was never started and is still
`Exited (143) 2 months ago`, exactly as found. All testing ran in throwaway `--rm` containers
with **no published ports**, a scratch `Saves/` under the session temp directory, and a
scratch copy of `Configuration` edited to listen on `127.0.0.1:2593` only. No client.
`docker/uo/docker-compose.yml` was read and not touched (Q-009 is Chase's).

## What the number is

**Agent wall-clock, including model inference time.** It is not human effort and it is not CPU
time. It is the right unit for pricing this backlog because the work will be done by an agent,
but do not compare it to a human estimate.

Conditions that materially affect it, stated up front:

- **Warm Docker build cache.** The `git clone` of ModernUO and the .NET SDK install were already
  cached from CC1. A cold cache adds roughly 15–20 minutes, once, not per file.
- **No client session.** CC2's brief forbade one. P1 with a client took a multiple of this.
- **Excludes review** and excludes writing this file.

## The clock

All times UTC, 2026-09-06.

| # | Phase | From | To | Elapsed |
|---|---|---|---|---|
| 0 | Orientation — `AGENTS.md`, `docs/tasks.md`, `notes/port-recipe.md`, `notes/codex-questions.md`, `notes/cc1-p1-runtime-validation.md` | — | 20:01:18 | **≤1:00** (measured floor 0:21) |
| 1 | Creature selection + reading the ServUO source | 20:01:18 | 20:06:09 | **4:51** (2:00 lost to a shell stall → **2:51 net**) |
| 2 | Transformation, 123 lines → 80 | 20:06:09 | 20:06:49 | **0:40** |
| 3 | **Build cycle 1 — FAILED** (`LuckyCoin` not found) | 20:06:56 | 20:07:56 | **1:00** |
| 4 | Dependency resolution — decide and port `LuckyCoin` | 20:07:56 | 20:10:08 | **2:12** |
| 5 | **Build cycle 2 — CLEAN**, 9/9 patches, zero errors | 20:10:28 | 20:11:12 | **0:44** |
| 6 | Verification (breakdown below) | 20:11:12 | 20:20:33 | **9:21** |
| | **Total** | 20:00:57 | 20:20:33 | **19:36** |

Orientation began before the first clock mark, so the honest total is **about 20 minutes**.

### Phase 6 broken down

| Step | Elapsed | Note |
|---|---|---|
| Harness setup — scratch dirs, config copy, loopback rewrite | 3:11 | includes one failed attempt: a Git-Bash-style `/c/...` bind-mount path silently mounts empty under Docker Desktop, so the server fell through to its interactive data-path prompt |
| Run 1 — start / save / shutdown | 1:55 | **wasted.** The piped `save` was eaten by the owner-account prompt, which holds stdin before the console handler is live |
| Run 2 — `n` / `save` / `shutdown` | 1:37 | clean. `Saving world done (0.04 seconds)`, snapshot written |
| Assembly reflection check | 1:02 | proved the generator ran on both new types |
| Run 3 — reload the saved world | 1:12 | `Loading world done (621 items, 91 mobiles)`, no errors |

**Two of the six phases were substantially environment friction** — the 2:00 shell stall in
phase 1, and 3:11 + 1:55 in phase 6. All of it is session fixed cost, now written down, and
should not recur. See the batch estimate.

## Result

| Check | Result |
|---|---|
| Compiles in a clean Docker build | **Yes.** Zero errors, all 9 patches applied |
| Server starts | **Yes.** `Loading world done (617 items, 90 mobiles) (0.20 seconds)`, no errors |
| Type registered | **Yes**, by reflection over the shipped assembly — see below |
| World saves | **Yes.** `Saving world done (0.04 seconds)` + snapshot written |
| World reloads | **Yes.** `Loading world done (621 items, 91 mobiles) (0.27 seconds)`, no errors |
| Instance survives save/reload | **NOT VERIFIED — see below** |

Reflection over `/modernuo/UOContent.dll` in the built image, via a .NET 10 file-based app
(`dotnet run reflect.cs`) inside a throwaway container:

```
Server.Mobiles.GreaterPoisonElemental: base=BaseCreature
    generated=[Serialize(IGenericWriter) Deserialize(IGenericReader)]  ctors=[() (Serial)]
Server.Items.LuckyCoin:                base=Item
    generated=[Serialize(IGenericWriter) Deserialize(IGenericReader)]  ctors=[(Int32) (Serial)]
```

That is the source generator's output: the `(Serial)` deserialization constructor and both
serialization methods, none of which appears in our source. The assembly is the one the server
loads — proven independently by the ClusterF seeders, which live in the same assembly and ran at
world load. A type present in a loaded assembly is what `[add <type>` resolves against, so the
type is registered.

## What could not be verified headlessly

**One thing: an instance of the ported creature surviving a save and reload.**

The reason, not a hunch:

- The container console registers exactly three commands — `save`, `shutdown`, `restart`
  (`Projects/UOContent/Console/ConsoleCommands.cs`). There is no console spawn.
- `Saves/SerializedTypes.db` lists only types that have live instances. Stock `PlagueRat` and
  `GiantRat` are absent from it too, on a world that has neither. So an empty-world save cannot
  witness the registration of an uninstantiated type.
- `UOContent.Tests` ships no serialization round-trip harness — its tests are packet and utility
  tests — so the test project is not a way in either.

Placing an instance therefore needs a client, or a code scaffold that spawns one at world load.
Per the CC2 brief I did **not** work around it. **Left unverified, flagged for the batched
five-creature spot check.** The decision itself took under a minute; the search that produced the
three reasons above sits inside the 1:02 reflection step.

The residual risk is small and bounded: version 0, no `[SerializableField]`, no persisted state
beyond what `BaseCreature` already round-trips, and P1 proved that exact shape round-trips for
`PlagueRat`. Nothing this creature adds is what goes untested.

## Why this creature

Chosen against the shape of the ~360-file CC6 batch, not for convenience.

ServUO `Scripts/Mobiles/Normal` line-count distribution, n=462: min 32, p25 88, **median 105**,
p75 135, max 8033. Feature frequency: `AddLoot` 344/462, `PackItem` 195/462,
`Tamable = true` 122/462, `OnDeath` 78/462, `OnGaveMeleeAttack` 10/462.

`GreaterPoisonElemental` is 123 lines — between the median and p75 — and exercises, beyond what
`PlagueRat` did:

- **two `PackItem` calls**, one with a quantity constructor (`new Nightshade(4)`)
- **three `AddLoot` calls** rather than one, including `FilthyRich` and `MedScrolls`
- an **`OnDeath(Container c)` override** with a conditional `c.DropItem` — the shape 78 files use
- five property-body overrides returning `bool`, `Poison`, `double` and `int`, not just `int`
- `AIType.AI_Mage` rather than the `AI_Melee` default
- the two-argument `SetStr/SetDex/…/SetStam` overloads throughout

It calls neither `SetWeaponAbility` nor `SetSpecialAbility`, touches no Pet Training, Masteries,
VvV or City Loyalty, and its stem is absent from `tools/modernuo-stems.txt` — stock
`PoisonElemental` is present, so this is an addition, not a collision.

It was **not** a clean pick, and that turned out to be the most useful part of the run.

**Rejected, with reasons worth keeping:**

- `SabertoothedTiger` — the only strong tameable candidate near the median. Calls
  `SetMagicalAbility` and `PetTrainingHelper`, i.e. ServUO's Pet Training subsystem. Declined
  under the `AGENTS.md` missing-subsystem rule.
- `Ortanord` — has `OnDeath`, but the override body is `base.OnDeath(c);` and nothing else. It
  would have exercised the keyword and not the pattern.
- `EnslavedGoblin*` — a family of six at 120 lines, a genuinely representative *shape*, but no
  override at all.

**No tameable block was exercised.** Every tameable candidate between 85 and 140 lines that also
had a loot pack pulled in Pet Training. That is itself a finding for CC6: the tameable cohort is
not a straight port and needs its own decision before anyone batches it.

## The dependency gap — the finding that matters

Build cycle 1 failed on one line:

```
error CS0246: The type or namespace name 'LuckyCoin' could not be found
```

`LuckyCoin` is real ServUO content (`Scripts/Items/Quest/SAQuestItems.cs:443`) that ModernUO does
not ship. **The recipe has no step that would have caught this before a build cycle.** Its only
pre-build check is `tools/modernuo-stems.txt`, which is a list of *filename stems* and is correct
only for its stated purpose — collision-checking the ported type's own name. Used as a dependency
checker it reports `ICommodity`, `TextDefinition`, `Ribs`, `ThighBoots` and `IronOre` as missing
when all five exist; they are simply defined inside files named something else.

**There is a real dependency checker and nobody knew about it.** The Docker *builder* image holds
the full pinned ModernUO source at `/build/modernuo`:

```bash
docker run --rm --entrypoint sh sl-uo-buildertest:latest -c 'grep -rn "class FountainOfFortune" /build/modernuo/Projects'
```

That answered, in seconds each and with no build cycle: `ICommodity`'s member shape, every
`BaseCreature` virtual this creature overrides, the `LootPack` member names, and `BaseReagent`'s
constructor. It is now written into the recipe.

Related correction: **`AGENTS.md` is wrong that `server/uo/modernuo/` holds "a full ModernUO
checkout".** That tree contains only `Configuration/` and `Projects/UOContent/Misc/` — 161 `.cs`
files, all of them ours. There is no ModernUO source on disk outside the Docker images. Raised as
Q-011.

### How often will this fire? Measured, not guessed

Extracted all 7,058 type names from pinned ModernUO's `Projects/Server` and `Projects/UOContent`
and checked every `new X(` reference in all 462 ServUO `Mobiles/Normal` files against that set,
plus our 115 customizations:

| | files | share |
|---|---|---|
| Reference at least one type ModernUO lacks | 89 | **19%** |
| Call `SetWeaponAbility` / `SetSpecialAbility` / `SetMagicalAbility` / `PetTrainingHelper` | 132 | **29%** |
| **Clean on both checks** | **275** | **60%** |

Most common missing types: `Yeast` (8), `ConfirmMountStatuetteGump` (7), `Fur` (6),
`ParrotItem` (5), `AncientPotteryFragments` (5), `TatteredAncientScroll` (4), `BouraSkin` (3),
`SlithEye` (3). Caveat: a handful of the 89 are BCL rewrites (`Hashtable`, `ArrayList`,
`TimerStateCallback`) rather than missing content — still per-file work, but a different kind.

**So 40% of `Mobiles/Normal` needs a decision beyond the mechanical transformation.** That is the
single most important number for pricing CC6, and it was invisible before this run.

### The `LuckyCoin` decision

Ported `LuckyCoin` alongside the creature, to `server/customizations/Items/Quest/LuckyCoin.cs`,
**complete except for its `OnDoubleClick`**, which throws the coin into a `FountainOfFortune` — an
SA addon ModernUO does not have and whose own port would drag in `EnchantedEssence`,
`GemologistsSatchel`, `RelicFragment` and `SolesOfProvidence`. That is a subsystem, and
`AGENTS.md` says decline subsystems.

This keeps the deviation **in the item, not the creature**: `GreaterPoisonElemental`'s loot table
is faithful, which is what a player checks against UOGuide. Reversible in one file the day the
Fountain is ever built. `LuckyCoin` is dropped by 12 `Mobiles/Normal` creatures, so the decision
is reused rather than one-off. **Recorded as Q-010** — the deviation register lives in
`docs/fidelity-principle.md`, which is the overseer's file.

## Estimate for a batch of 20

### Splitting the measured run into fixed and per-file

| | measured | fixed or per-file |
|---|---|---|
| Orientation | ≤1:00 | **fixed per session** |
| Selection | 2:51 net | **mostly fixed** — one scan picks 20, and the scripts are now written |
| Reading the ServUO source | ~0:30 | **per file** — three files read inside phase 1 |
| Transformation | 0:40 | **per file** |
| Build cycle, warm | 0:44 | **per build**, not per file |
| Dependency resolution | 2:12 | **per affected file**; ~0:45 now the tooling is known, +0:40 to port a leaf item |
| Verification harness setup | 3:11 | **fixed** — now ~1:00, both failure modes are written down |
| Verification runs (3 + reflection) | 5:46 | **fixed per batch** — you verify the batch, not each file |

The ratio the brief asked for: **per-file work is 1:10 and a build cycle is 0:44.** Build cycles
are *not* the dominant cost at a warm cache, which is the opposite of what "build after every
file" assumes.

### Two scenarios

**A — build after every file, as `docs/tasks.md` mandates**

```
per file : read 0:30 + transform 0:40 + build 0:44                        = 1:54
         + dependency work on 19% of files
           0.19 x (check 0:45 + port a leaf 0:40 + one failed build 0:44)  = 0:24
                                                                   avg      2:18
x20                                                                        46:00
fixed    : selection 3:00 + harness 1:00 + verification 6:00
           + notes and commit 5:00                                         15:00
                                                                   TOTAL   61:00
```

**B — build in groups of five**

```
per file : read 0:30 + transform 0:40 + dependency 0:24   = 1:34   x20   = 31:20
builds   : 4 cycles x 0:44, plus ~2 extra cycles for failures            =  4:30
fixed    :                                                                 15:00
                                                                   TOTAL   50:50
```

### Call it one hour for a batch of 20 — and the reasoning behind that

- **Batching the builds saves about ten minutes out of sixty.** Real, but not the lever it looks
  like. At a warm cache a build cycle is 44 seconds; at a cold cache it would be the whole story,
  which is why the build cache must not be pruned between batches.
- **The real lever is pre-screening.** Running the type-gap check over the whole candidate list
  *before* starting — now a one-line `grep` against the builder image — moves every dependency
  discovery out of a failed build cycle and into selection, where it costs seconds. Both of this
  run's build cycles existed because that check did not exist. Doing it first would have made
  this a one-build port.
- **Select the batch out of the clean 60%.** The 29% that call `SetWeaponAbility` and friends are
  a design decision, not a port, and one of them landing mid-batch will cost far more than an
  hour. Filter them at selection and queue them separately.
- **The estimate assumes a 20-file batch is homogeneous.** It will not be. One creature with a
  real `[SerializableField]`, a `Serial` comparison, or a `TextDefinition` — none of which either
  port has exercised — could absorb the whole hour by itself. Those three are still the
  unverified corners of the recipe after two ports.

**Extrapolated:** 20 files/hour ⇒ the ~360-file CC6 batch is **roughly 18 hours of agent time**
across about 18 sessions, if the batches are drawn from the clean 60%. The other 40% is a
separate, larger and less predictable piece of work, and it should be scoped as one rather than
discovered file by file.

**Confidence:** the per-file transformation figure rests on n=1 and is the number I trust least.
The 19% / 29% / 60% split rests on all 462 files and is the number I trust most. If only one
figure survives this document, keep that one.

## Scratch environment, for repeatability

```bash
( sleep 12; echo n; sleep 35; echo save; sleep 30; echo shutdown; sleep 20 ) | docker run -i --rm --name sl-modernuo-cc2-run -v "$SCRATCH/run/Saves:/var/lib/uo/modernuo/Saves" -v "$SCRATCH/run/Backups:/var/lib/uo/modernuo/Backups" -v "$SCRATCH/run/Archives:/var/lib/uo/modernuo/Archives" -v "$SCRATCH/run/Configuration:/modernuo/Configuration" -v "D:/ShatteredLegacy/client-data/classic-client:/var/lib/uo/client-data/classic-client:ro" --security-opt seccomp=unconfined -e TZ=America/Chicago sl-modernuo-cc2
```

`$SCRATCH` must be a **Windows-style** path (`C:/Users/...`). A `/c/...` path mounts empty and the
failure is silent — the server just falls through to its interactive client-data prompt.

The scratch `Configuration/modernuo.json` was edited to `listeners: ["127.0.0.1:2593"]`,
`serverListing.address: "127.0.0.1"` and `autosave.enabled: "False"`.

The `echo n` answers the owner-account prompt, which holds stdin before the console handler
starts; without it the next piped command is swallowed. `shutdown` does **not** save — `save` must
be sent first.

The world is not empty even on a fresh `Saves/`: the ClusterF seeders build 617 items and
90 mobiles at world load, so there is real content to save and reload.
