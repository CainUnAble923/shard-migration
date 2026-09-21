# CC6 follow-up — the dragon breath restored (Q-054) and the Incubator taken (Q-053, P12)

Date: 2026-09-21. Agent: Claude Code (Fable 5.1), headless. Pinned ModernUO `7c9215d97`. ServUO pub57.
Files: `server/customizations/Mobiles/Normal/{Slith,ToxicSlith,FireDaemon,CrystalHydra}.cs` (edited),
`server/customizations/Mobiles/Abilities/Fire Breath/CrystalHydraBreath.cs` (new),
`server/customizations/Items/Functional/Incubator.cs` (new), `server/customizations/Items/Functional/ChickenLizardEgg.cs`
(one clause restored), `server/customizations/Engines/Craft/IncubatorCarpentryRecipe.cs` (new),
`server/patches/Beverage-chicken-lizard-egg-pour.patch` (new) + its line in `docker/uo/apply-patches.sh`,
`server/tests/Mobiles/Normal/CC6FollowupBreathIncubatorVerification.cs` (new, 7 facts), and two things this task did
not set out to touch and had to: `docker/uo/apply-patches.sh` (patch fuzz pinned to 0, §6) and
`server/tests/Mobiles/Normal/CC6Batch4CreatureVerification.cs` (one wrong statistical expectation, §5).

**Status: done, both parts.** 4 creature files edited, 4 files added, 1 patch, 1 egg clause restored, 7 new facts,
built through `build.sh` (**17 patches**, **97 tests green**, 90 before + 7), the four breathers constructed live and
declaring their abilities in a headless run, an egg driven through a secured incubator by a real world save, a real
reload and a real pitcher, save and reload identical, final image `sl-modernuo:cc6f1` (2acfcfc573d8) loading clean
with the probe removed. Nothing seen in a client. Two red proofs, one of which found the patch gate tolerating drifted
context and closed it (§6).

**Two things the brief had approximately right, both found by reading the source rather than the earlier notes:**
the crystal hydra does **not** take the default fire breath — it is the one type of the four with its own definition
in ServUO's table, and it is cold, four times as frequent, and five targets wide (§2); and the recipe needed **no
patch** — this repo already appends to `DefCarpentry.CraftSystem` after `DefCarpentry.Initialize()` from
`EventSink.ServerStarted`, so the incubator's entry rides the same route (§4). **The patch count goes 16 → 17, not
18.** And batch 4 §9's "the egg needs no change" was wrong by one clause (§3).

**The orphan count does not move: 41 before, 41 after.** This task ports no spawn-named creature. `ChickenLizard` (8
entries) was closed by batch 4; this makes the cluster reachable, not the name. `tools/spawn-orphans.txt` is untouched.

## 1. What the task is

Two fixes, one build, from `docs/patch-backlog.md` P12 and `notes/codex-questions.md` Q-053/Q-054 (commit `2939c63`):

- **A.** D-55 (`Slith`), D-56 (`ToxicSlith`), D-62 (`FireDaemon`) and D-68 (`CrystalHydra`) each recorded
  `SetSpecialAbility(SpecialAbility.DragonBreath)` as a Pet Training loss. Pinned ModernUO has the ability as
  `BaseCreature.GetMonsterAbilities()` (`:1131`) returning `MonsterAbilities.FireBreath` / `ColdBreath`
  (`Mobiles/Abilities/Fire Breath/`), CC4 Shame used it, and batch 5 declared it on `SkeletalDragonRenowned`. The four
  are on the shard fighting wrong. Restore the breath, one test fact each.
- **B.** The chicken lizard egg (batch 4) had no driver: nothing set `Incubating`, nothing called `CheckStatus()`, and
  no beverage reached its `Pour`. So no player could ever reach a `BattleChickenLizard`. Port ServUO's `Incubator`
  (158 lines), the `Beverage.Pour_OnTarget` egg branch, and the carpentry recipe.

## 2. Part A: which breath each creature gets, and what in ServUO decided it

ServUO's `DragonBreath` ability takes its numbers from a `DragonBreathDefinition` chosen **by creature type**:
`DragonBreathDefinition.GetDefinition(bc)` (`Services/Pet Training/SpecialAbility.cs:1065-1074`) returns the first
definition whose `Uses` array contains `bc.GetType()`, else `Definitions[0]`, the default. The table
(`Initialize()`, `:885-1063`) has nine definitions: the default, then Skeletal Dragon/Renowned (cold, 0x480),
Leviathan, Red Death, Frost Dragon/Cold Drake (cold, hue 1264), AntLion (poison), Rend, Crystal Sea Serpent, and
**Crystal Hydra**. Grepped for the four: `typeof(CrystalHydra)` is at `:1062` and the other three appear nowhere in
the file.

| creature | in a `Uses` list? | ServUO definition | pinned ModernUO equivalent | declared as |
|---|---|---|---|---|
| `Slith` | no | default (`:887-903`): scalar `Core.AOS ? 0.16 : 0.05`, 100% fire, 30-45 s, item 0x36D4, hue 0, sound 0x227, anger animation 12, stall 1.0 s, effect delay 1.3 s, damage delay 1.0 s | `FireBreath.cs`, every one of those values line for line | `MonsterAbilities.FireBreath` |
| `ToxicSlith` | no | default — **fire, not poison**: its poison is `Poisoning` 90-110 and 100% poison resistance, never the breath | same | `MonsterAbilities.FireBreath` |
| `FireDaemon` | no | default | same; beside its aura, which is `HasAura`, not a `MonsterAbility`, so the ability array is still one long | `MonsterAbilities.FireBreath` |
| `CrystalHydra` | **yes, `:1045-1063`** | scalar **0.13**, **100% cold**, **5.0-7.0 s**, item 0x36D4, hue **0x47E**, sound **0x56D**, animation 12, delays as default, **`attacksMultiples = true`** | `ColdBreath : FireBreath` (cold 100, fire 0, hue 0x480) is the mechanism; none of the five differences is a stock value | **`CrystalHydraBreath`** (ours), `: ColdBreath` |

**`CrystalHydraBreath`** (`Mobiles/Abilities/Fire Breath/CrystalHydraBreath.cs`, additive, the path pinned uses)
overrides the five values and adds the fan-out. `attacksMultiples` in ServUO's `DoBreath` (`:742-756`) means: gather
`SpellHelper.AcquireIndirectTargets(creature, target, map, 5)` — every damageable within **5 tiles of the target**,
alive, in the creature's LOS, `CanBeHarmful`, `ValidIndirectTarget` — filtered to `InRange(creature, MaxRange = 12)`,
then five draws, the first fixed on the target, each scheduling the same `BreathEffect_Callback` at the 1.3 s delay.
Here `Trigger` gathers the same list (pinned has no `AcquireIndirectTargets`; the filter is reproduced in
`AcquireSecondaryTargets` with `Map.GetMobilesInRange`, mobiles only), lets `FireBreath.Trigger` do the first breath
exactly as stock (stall, anger sound, animation, facing, the effect timer, the cooldown through `MonsterAbility.Trigger`),
and schedules up to four more `BreathEffect_Callback`s beside it. A hydra therefore breathes on a whole party every
5-7 s at 0.13 of its ~1475 hits, capped at 200, as cold: a very different creature from the one batch 4 shipped.

**The header of each of the four files now says which definition it got and why**, with the line range, and the
`D-nn` bullets that said "dropped" are gone. The test (§5) checks the numbers on the declared ability, not the type
name: `FireDamage`/`ColdDamage`/`BreathEffectHue`/`BreathEffectSound`/scalar/cooldowns/delays, and for the hydra also
that the stock `ColdBreath` it does **not** use is 0x480 and 30 s, and that one trigger hurts exactly the combatant plus
four of seven nearby players and not a player 15 tiles away.

**Said once, and only once, for all four (batch 5 §2 recorded it and CC4 accepted it):** what the mapping does not
reproduce. ServUO triggers a breath **on think**, 10% per think while off cooldown, and charges 30 mana
(`SpecialAbility.cs:172-176`, `CheckMana`, `TriggerChance` 0.1, `DragonBreath.TriggerOnThink`); pinned triggers on a
**combat action** (`BaseWeapon.cs:893`, `BaseRanged.cs:74`), 50% while off cooldown, no mana. Both then wait the
definition's interval. Range is `MaxRange` 12 there and `RangePerception` (16, the default) here, for the first breath
and for the hydra's fan-out filter alike. ServUO plays `AnimationType.Pillage` under SA; pinned plays legacy action 12
for every breath. None of these is a D-number.

**One ServUO quirk noticed in the ctor, recorded and not chased:** `DragonBreathDefinition`'s constructor
(`:1085-1122`) assigns `EffectSpeed = effectDuration` and never assigns `EffectDuration`, so every ServUO breath runs
with speed 5 and duration 0 — which is exactly pinned `FireBreath`'s `BreathEffectSpeed => 5`,
`BreathEffectDuration => 0`. Same effective values on both emulators, by accident on one of them.

**D-55, D-56, D-62 and D-68 are retired, not reversed.** They were never true; `docs/fidelity-principle.md` already
marks the four rows withdrawn pending this fix. **The fix has landed, so the rows can be struck in review.** No new
D-number is minted for these four, and no D-number is minted at all by this task (§8).

## 3. Part B: the Incubator, and the egg clause batch 4 §9 said it would not need

**`Incubator`** (`server/customizations/Items/Functional/Incubator.cs`, ServUO's path) is a house container:
`[Flippable(0x407C, 0x407D)]`, label 1112479, gump 1156, drop sound 66, `ISecurable` with `Level` defaulting to
`CoOwners`, `MaxEggs = 6`. Its `CheckHold` refuses everything unless `BaseHouse.CheckSecured(this)` (1113711, "must be
secured for the egg to grow, not locked down"), refuses anything that is not a `ChickenLizardEgg`, refuses a seventh
egg. Its two drop overrides call the base and then, for an egg, either burn it (past 120 h) or set `IncubationStart =
Core.Now; Incubating = true`. `CheckEggs_Callback` calls `CheckStatus()` on each egg, again only while secured. The
`[IncreaseStage]` Counselor command (+24 h then `CheckStatus`) is kept. All verbatim; the duplicated drop block is one
private method.

**Every member resolved in pinned before the first build:** `Container.OnDragDropInto(Mobile, Item, Point3D)`
(`Server/Items/Container.cs:282`), `Container.OnDragDrop(Mobile, Item)` (`:393`, → `TryDropItem`),
`CheckHold(Mobile, Item, bool, bool, int, int)` (`:212`), `DefaultGumpID`/`DefaultDropSound` virtuals (`:149`, `:152`),
`ISecurable` (`Gumps/Houses/SetSecureLevelGump.cs:8`, `SecureLevel Level { get; set; }` — the generator's property from
a `[SerializableField] SecureLevel _level` satisfies it, as stock `DyeTub` does), `SecureLevel` (`BaseHouse.cs:3910`,
namespace `Server.Multis`), `BaseHouse.CheckSecured(Item)` (`:1304`, `FindHouseAt(item)?.HasSecureItem(item)`),
`CommandSystem.Register(string, AccessLevel, CommandEventHandler)` (`Server/Commands.cs:221`),
`Mobile.BeginTarget(int, bool, TargetFlags, TargetCallback)` (`Mobile.cs:4031`), `Timer.DelayCall(TimeSpan, Action)`.
Stock `Corpse`, `TrashBarrel` and `BaseBoard : Container, ISecurable` are the generator shape for a `Container` subclass.

**The two ServUO drivers that lived inside hand-written serialization**, carried over as the hooks pinned has for the
same moments rather than dropped:

| ServUO | where | pinned | note |
|---|---|---|---|
| `Deserialize`: `if (Items.Count > 0) DelayCall(60 s, CheckEggs_Callback)` | per incubator, after load | `[AfterDeserialization]`, same body | the `PeerlessKey`/`BaseFish` shape |
| `Serialize`: `if (Items.Count > 0) DelayCall(10 s, CheckEggs_Callback)` | per incubator, **on every world save** | `EventSink.WorldSave += OnWorldSave` in `Initialize()`, walking `World.Items.Values.OfType<Incubator>()` for ones with items and scheduling the same 10 s call | `World.Save` invokes it on the game thread before the snapshot (`Server/World/World.cs:308`); the generator's `Serialize` is not a place to put a timer |

So the cadence is ServUO's, including its oddity: **an egg advances a stage within one save interval of crossing the
threshold** (`autosave.saveDelay` is 5 min on this shard) and 60 s after a restart, never in between. That is how OSI-
era shards ran it and what a wiki describes as "check back after a day"; not a deviation.

**The egg did need one change, and batch 4 §9 was wrong to say otherwise.** `Incubating`, `IncubationStart`,
`TotalIncubationTime` and `CheckStatus()` are public, as §9 said. But ServUO's `ChickenLizardEgg.DropToItem` is
`check && !(Parent is Incubator) && m_Incubating → Incubating = false`, and batch 4 dropped the middle clause "with the
type". Read against pinned `Item.DropToItem` (`Server/Items/Item.cs:3470`) → `OnDroppedInto` → `target.OnDragDropInto`
(or `OnDroppedOnto` → `target.OnDragDrop`): the incubator's override runs **inside** that call and sets `Incubating =
true`, control returns to the egg's override, and without the clause `check && _incubating` switches it straight back
off. The egg would have entered every incubator and never incubated. The clause is restored (`Parent is not
Incubator`), the header rewritten, and the first Part B fact asserts `Incubating` is true after a real `DropToItem`.
**Confirmed rather than assumed**, as the brief asked; the answer was "almost".

## 4. The two upstream hunks, argued before they were written — and why only one is a patch

### 4a. `Beverage.Pour_OnTarget` → a patch (`server/patches/Beverage-chicken-lizard-egg-pour.patch`)

ServUO `Beverage.cs:1489`: `else if (targ is ChickenLizardEgg) ((ChickenLizardEgg)targ).Pour(from, this);` between the
`PlantItem` and water-vat branches. Pinned `Beverage.cs:587-735` is the same chain — beverage, self,
`BaseWaterContainer`, `PlantItem` (`:684`), the Solen water vat — with no interface for the target and no virtual on
the target side. Alternatives considered:

1. **An additive interface (`IPourTarget`) on the egg.** Nothing in pinned consults one; the branch that would consult
   it is the patch. Rejected: it is the same hunk with an extra file.
2. **Override `Pour_OnTarget` in a pitcher subclass.** Players' pitchers are stock `Pitcher`s from stock vendors and
   loot; a subclass reaches none of them. Rejected.
3. **Make the egg accept the pitcher as a drop (`OnDragDrop`).** A different player action from the one OSI documents
   (target the egg with the pitcher), and the egg's `Pour` is written for the targeting flow. Rejected on fidelity.
4. **The partial-class trick** (batch 3): `BaseBeverage` is `partial` (generated), but C# cannot override or wrap a
   method from another part of the same class. Rejected: no seam.
5. **The patch.** Six lines (two of comment) inserted after a four-line branch whose text is unlikely to move
   (`item.Pour(from, this)` next to `PlantItem`); hunk `@@ -685,6 +685,12 @@`, `git apply --check` clean against
   pinned. **Chosen.** On a bump it either applies or fails the build in the patch gate; and the test pours through
   `Pour_OnTarget`, so a bump that leaves the patch applying while the branch stops reaching the egg goes red too.

### 4b. The carpentry recipe → **additive**, no patch (`Engines/Craft/IncubatorCarpentryRecipe.cs`)

ServUO `DefCarpentry.cs:229`: `AddCraft(typeof(Incubator), 1044294, 1112479, 90.0, 115.0, typeof(Board), 1044041, 100,
1044351)` inside `#region SA`. **The call is made deliberately: without it the incubator exists and no player can make
one, which is the "ported but unreachable" shape this task exists to fix. Reading pinned `DefCarpentry.cs` gave no
reason not to; it gave a reason not to patch it.**

`CraftSystem.AddCraft(...)` and `SetNeededExpansion(int, Expansion)` are public (`Engines/Craft/Core/CraftSystem.cs:
126-180`, `:248`); `DefCarpentry.CraftSystem` is a public static created by `DefCarpentry.Initialize()`; a `CraftItem`
appended later joins its group's list and is drawn by the gump on demand. **This repo already does exactly this:**
`ClusterFLumberjackingExtension.Configure()` subscribes `EventSink.ServerStarted` and appends sub-resources to
`DefCarpentry.CraftSystem` and `DefBowFletching.CraftSystem` "after `DefCarpentry.Initialize()`", which is the ordering
answer (`Initialize()` order across types is not guaranteed; `ServerStarted` is after all of them). Alternatives:

1. **A patch into `InitCraftList`** at the end of the "Other" group. Six lines, stable context. Rejected: it buys
   nothing over the additive call — a signature change on a bump breaks either one at compile time, and the patch adds
   a hunk to a 560-line data table upstream edits freely (every era block in it is a candidate for churn).
2. **The additive registration.** One 60-line file, one public API, the precedent above, idempotent, and the test host
   calls `Register()` directly because `ServerStarted` never fires there. **Chosen.** The entry lands at the end of
   the "Other" group, which is where ServUO's SA block sits relative to everything pinned has (pinned's group ends
   with the ML block; ServUO's SA block follows ML).

Two value decisions inside it, both toward the pinned table: the resource is `typeof(Log)` with name 1044041 ("Boards
or Logs"), as every wood entry in pinned `DefCarpentry.cs` is, because `CraftItem`'s type table
(`server/customizations/CraftItem.cs:64`) makes `Log` and `Board` interchangeable at consumption — 100 boards make one
exactly as ServUO's `typeof(Board)` does; and `SetNeededExpansion(index, Expansion.SA)` is added, the way pinned marks
every era-gated entry (`DefTailoring.cs:544`), so a non-SA shard would hide it. Skill 90.0-115.0, 100 of the resource,
no second resource, no recipe, not forced non-exceptional: verbatim.

**So the patch count is 17, not the brief's 18.** `apply-patches.sh` has 17 `apply_patch` lines and the build log
says `All 17 patches applied successfully.`

## 5. What was proved

| Gate | Result |
|---|---|
| `build.sh` FINAL (patches, tests, image) | green, `sl-modernuo:cc6f1` (2acfcfc573d8): `All 17 patches applied successfully` at `--fuzz=0`, `structured customizations installed: 604` (605 with the probe), `shard tests installed: 20`, **97 tests passed** (90 + 7) |
| **Part A, four facts, one per creature** (`TheSlithBreathesTheDefaultFire`, `TheToxicSlithBreathesTheDefaultFireNotPoison`, `TheFireDaemonBreathesTheDefaultFireBesideItsAura`, `TheCrystalHydraBreathesColdEveryFewSecondsAtUpToFiveTargets`) | each creature's `GetMonsterAbilities()` is exactly one ability; for the three it is `FireBreath` by exact type with the default definition's every number (fire 100, cold/phys/poison/energy/chaos 0, scalar 0.16, 30-45 s, item 0x36D4, hue 0, sound 0x227, animation 12, stall 1.0, delays 1.3/1.0); the fire daemon's aura is still `HasAura` beside it; the hydra's is `CrystalHydraBreath : ColdBreath` with cold 100, fire 0, scalar 0.13, **5-7 s**, hue **0x47E**, sound **0x56D**, and the stock `ColdBreath` it does not use pinned at 0x480 / 30 s; `BreathComputeDamage` at 300 hits is 39; `AcquireSecondaryTargets` returns the 7 players within 5 tiles of the combatant and not the combatant or the one 15 tiles off; **one `Trigger` and a 2.8 s advance hurt the combatant and exactly 4 of the 7 nearby, the far player untouched** |
| **Part B, three facts** (`TheIncubatorMustBeSecuredHoldsSixEggsAndNothingElse`, `AnEggInASecuredIncubatorWateredThroughAPitcherHatchesABattleChickenLizard`, `TheIncubatorIsCraftableUnderCarpentryOtherForAHundredBoards`) | label 1112479, item 0x407C, gump 1156, drop sound 66, `Level` CoOwners, `MaxEggs` 6; **unsecured: `OnDragDropInto` refuses and the egg stays in the pack, not incubating; after the house's own `AddSecure`: `HasSecureItem`/`CheckSecured` true, a real `Item.DropToItem` lands the egg in the incubator with `Incubating` true** (the restored clause); an apple is refused; five more eggs go in, a seventh is refused; a lifted egg stops and banks its 2 h; an egg past 120 h burns on the way in; a backdated egg does **not** advance through the save hook while the incubator is released, and does (New to Stage1) once re-secured. **The cycle:** six eggs at a time through `DropToItem`, backdate 25 h, `EventSink.InvokeWorldSave`, `Core.LoopContext` pumped, 11 s of wheel, Stage1 and Dry, `Pitcher.Pour_OnTarget` (the patch) leaves 4/5 with water 1, Moist, still incubating; 24 h, save, Stage2, pour; 24 h, save, Mature; repeated until one rolled a battle chicken: **48 eggs in the detailed run, 6 and 36 in two full-suite runs** (5% at Dry; 0 burnt); lifted with `OnItemLifted`, hatched **outside** the house with `TryHatchEgg`: exactly one new `BattleChickenLizard`, body 716, in the egg's hiryu hue, at the hatcher's feet; an immature egg crumbles. **The recipe:** `DefCarpentry.Initialize()` then `IncubatorCarpentryRecipe.Register()` twice gives exactly one `CraftItem` for `Incubator`: group 1044294, name 1112479, `RequiredExpansion` SA, Carpentry 90.0-115.0, one resource `Log` x 100 named 1044041 |
| Headless run 1b (probe image from build A8, fresh save; runs 1/2 were the same on the pre-fix hook, §6) | `Loading world done (618 items, 90 mobiles)`, listeners on 127.0.0.1; the probe constructs the four on Ter Mur: `Slith: 1 ability, FireBreath fire=100 cold=0 scalar=0.16 hue=0x0 sound=0x227 cooldown=30-45s range=16`, the same for `ToxicSlith` and `FireDaemon`, `CrystalHydra: 1 ability, CrystalHydraBreath fire=0 cold=100 scalar=0.13 hue=0x47E sound=0x56D cooldown=5-7s range=16`, 4 live; a `SmallOldHouse` placed on Felucca at 1400,1700 with **real multi data** (`components=8x8`, found by `FindHouseAt`); **unsecured drop refused; `AddSecure`; secured drop accepted, `parent=Incubator incubating=True`**; egg backdated 25 h; at t+90 s still New; **the harness `save` at t+165 s, no error line, and at t+185 s `stage=Stage1 ... total=25.0h itemid=0x41BE`**; then a real `Pitcher` through `Pour_OnTarget`: `pitcher 4/5, water=1 dryness=Moist`. Clean save, shutdown |
| Headless run 2b, reload run 1b's save | `Loading world done (636 items, 96 mobiles)`; **the incubator, its secure, its egg and the four breathers all back**: `secured=True items=1 egg ... stage=New incubating=True water=0 total=0.0h`, **identical to the state at the save** (the save at t+165 s preceded the check at t+175 s and the pour at t+185 s, and `shutdown` does not save, so New/0/0 is exactly what was written); the probe backdates 24 h; **the 60 s after-load check fires: t+90 s `stage=Stage1 total=24.0h`** (the probe's "expect Stage2" label assumed the save held Stage1; it held New, and New to Stage1 is the correct outcome); all four breathers describe themselves identically to run 1b; a second save, **no error line**; shutdown clean |
| Headless run 3, the final image, fresh save | `Loading world done (618 items, 90 mobiles)`, listeners on 127.0.0.1, `Saving world done`, `Shutting down`; **no `[cc6f1]` line**; only the usual three warnings (`stats` already registered, no accounts, no owner account) |
| Batches 1-5's orphan pins | **41, unchanged, all green** (`EveryStockSpawnEntry...` in each); the count did not move because nothing here is spawn-named |

**One earlier test corrected on the way.** Build A6 went red on batch 4's `TheEggIncubatesWatersMutatesAndHatches`:
`Assert.InRange(maturedDehydrated, 8, 55)`, actual 57 of 200. That fact says an unwatered egg survives 12.5% (0.5 x
0.25). Read against the egg: at the 48 h check an unwatered egg is stage 1 with water 0, `Dryness` 1 = **Dry**, below
`Parched`, so the 50% roll never fires; only the 72 h roll (Dehydrated, 75% burn) does, and survival is **25%**, mean
50 of 200. The range was wide enough to pass most runs (it passed five builds in this task before failing) and was
never right. Corrected to 28-72 (+-3.6 sigma at n=200) with the comment rewritten; a test bug of ours, the "read the
implementation before writing the assertion" shape.

**Not verified, per the standing rule, and batched for the client spot check:** the breath animation, the 0x47E
cold effect and the 0x56D sound on a crystal hydra; whether five players around one actually see five breaths; the
incubator's gump 1156 and its flip; the secure gump on it; an egg dropped by a client into an open incubator gump versus
onto its icon (both paths are covered by the test but only `DropToItem` with a gump point in the headless run); and
whether the "Other" group's last entry reads "an incubator" for 100 boards in a client's carpentry menu.

**Recorded and not chased, both host artefacts seen while getting the hydra fact green:** `Mobile.DefaultHitsRate` is
`TimeSpan.Zero` in the test host (nothing runs `RegenRates.Configure`), so a creature's `HitsTimer` adds a hit on
every 8 ms wheel tick and the hydra set to 300 hits breathed for 84 by the time the damage callback ran (650 hits x
0.13); the fact pins the computed damage before the trigger and the fan-out shape, not the landed number. And
`MonsterAbility.CanTrigger` read the hydra's breath as ready again immediately after a trigger in the isolated
`--filter` run on the same builder, while the same assertion held in every full-suite run; order-dependent, in stock
tick bookkeeping under the test clock, and removed from the fact rather than papered over.

## 6. Red proofs

Four gates were watched, and one of them did not fail when it should have.

| Gate | Broken how | Build | Result |
|---|---|---|---|
| the patch gate, `Beverage-chicken-lizard-egg-pour.patch` | one leading **context** line of the hunk changed (`item.Pour(from, this)` became `that`) | R1 | **GREEN. The build applied the patch and shipped.** `apply_patch` runs `patch -p1 --forward --ignore-whitespace --batch`, and GNU patch's default fuzz factor is 2: a hunk applies with up to two context lines at each edge not matching, and patch says so only on stdout ("succeeded at 685 with fuzz 2"), which the success branch discards with `>/dev/null`. The gate that F2/F3 exist for tolerates exactly the drift it is there to catch, and has since F2 for every patch in the tree |
| the same, with `--fuzz=0` added to both `patch` calls in `apply-patches.sh` | the same mangled context line | R1b | **red at stage 1**: `FAILED: Beverage-chicken-lizard-egg-pour.patch / Hunk #1 FAILED at 685 / 1 out of 1 hunk FAILED / ERROR: 1 item(s) did not apply. Failing the build.`, and **the other 16 applied at fuzz 0**, so no existing patch had been living on fuzz. Restored; FINAL green with all 17 at `--fuzz=0` |
| the test gate, Part A | `CrystalHydra.GetMonsterAbilities()` commented out | R2 | red: `TheCrystalHydraBreathesCold...`, `Assert.NotNull() Failure: Value is null` |
| the test gate, Part B, the egg clause | `Parent is not Incubator` removed from `ChickenLizardEgg.DropToItem` | R2 | red: `TheIncubatorMustBeSecured...`, `Assert.True(egg.Incubating)` false after a real drop, which is the defect batch 4 shipped |
| the test gate, Part B, the pour | the patch's added `egg.Pour(from, this)` commented out, so **the patch applies and does nothing** | R2 | red: `AnEggInASecuredIncubator...` (with the clause also gone this fact fails on `Incubating` first; the pour assertion is next in the same fact, and R1b proves the apply half) |
| the test gate, the recipe | 100 boards became 99 | R2 | red: `TheIncubatorIsCraftable...`, `Expected: 100 Actual: 99` |

R2: 4 failed, 93 passed, no image. All four files restored byte for byte (diffed against copies) before FINAL, which
went green.

**The `--fuzz=0` change is the one thing in this task outside its brief, and it is flagged here for review rather
than buried:** it is a change to the build gate, made because a red proof the brief asked for showed the gate green
over a mangled patch. It is two tokens in `docker/uo/apply-patches.sh` with the reason in a comment, it preserves the
runner's three jobs, and FINAL shows every patch in the tree applies exactly. If review would rather the runner stay
as it was, revert the two tokens and the R1 row above becomes the record that the gate is fuzzy.

**Also red before green, and why:** build A (two test compile errors, `Body` is a struct and `CraftRes` has `Name`
not `NameNumber`); A2 (a `PlayerMobile`'s `HitsMax` is 125 at most in the host, and the synthetic house floor
collapsed to 1x1 because `MultiComponentList`'s list constructor skips every 0-flag entry after the first); A3 (the
house at x 1300 on a Ter Mur that the host defines 1280 wide, so no sector held it; a fresh player has 50 hits);
A3-diag (`MultiSectorEnumerable` is not `IEnumerable`, and `HousePlacementEntry.Find` keys on the exact type, so the
test house had 0 lockdowns and `AddSecure` refused); A4 (`Item.IsSecure` is a flag bit `BaseHouse.Configure` assigns
and the host never runs it; `RemoveItem` is not a lift; the hydra killing 50-hit players); A5 (the hatched lizard
bounced to the house's ban location by `HouseRegion.OnLocationChanged`, real behaviour); A6 (batch 4's 12.5%, §5). A7
was the first green, and A8 after the save-hook fix below. **Seven `build.sh` runs and two builder-only diagnostics to a green with the probe, none of the reds
a product defect, seven of them the host's houses.** Headless run 1 on A7's image then logged
`[ERR] Attempted to start timer Server.Timer+DelayCallTimer while world is Saving` on the save hook, once per save:
`EventSink.WorldSave` fires inside `WorldState.Saving`, where `Timer.Start` logs a stack trace (`Timer.cs:85`).
The hook now gathers the incubators and starts the 10 s timers from the game loop's next iteration through
`Core.LoopContext.Post` (`Main.cs:480`); runs 1b/2b show two saves with no error line and the egg advancing.

## 7. What it cost

Wall clock, local time, one session, headless. Orientation began about 10:00 (+-5 min; the first file written is
timestamped 10:25:49).

| Phase | From | To | Elapsed |
|---|---|---|---|
| Orientation and pre-flight: both `AGENTS.md`, batch 4 §2/§9, batch 5 §2/§9, P12 and the P6 corrections, Q-053/Q-054; ServUO's `SpecialAbility.cs` table and `DragonBreath` body, `Incubator.cs`, the `Beverage.cs` branch, the `DefCarpentry.cs` entry; pinned `FireBreath`/`ColdBreath`/`MonsterAbility`/`BaseCreature` triggers, `Container`, `ISecurable`, `BaseHouse.AddSecure`/`CheckSecured`/`IsInside`, `Item.DropToItem`, `CraftSystem.AddCraft`, `DefCarpentry.Initialize`, the ClusterF precedent, `MultiData`, the test fixture, batch 4's egg fact | ~10:00 | 10:25 | ~25 min |
| Writing: the breath class, four creature edits, `Incubator`, the egg clause, the patch (generated from a pinned copy, `git apply --check` clean), the recipe, the runner line, the test, the probe, the harness, the note's §1-4 | 10:25 | 10:33 | ~8 min |
| Builds A to A8 and one diag builder, interleaved with two diagnostic filtered runs | 10:30 | 11:04 | ~34 min |
| Headless runs 1, 2 (A7 image, the ERR line found) and 1b, 2b (A8 image) | 10:57 | 11:11 | ~14 min, overlapping the builds |
| Red proofs R1 (green, the fuzz finding), R1b (red), R2 (red) | 10:57 | 11:07 | ~10 min, overlapping |
| FINAL build and run 3 | 11:07 | 11:13 | ~6 min |
| **To the final image and its clean run, end to end** | **~10:00** | **11:13** | **~73 min** |
| Note §5-8, `progress.py`, commits | 11:13 | | ~15 min |

Against the brief's "a small task, not a batch": about the same wall clock as batch 5's seventeen creatures, and
almost all of it in getting a *house* to exist in a test host that has no multi data, no placement table for a
subclass, no `BaseHouse.Configure`, no `RegenRates.Configure` and a 1280-wide Ter Mur. The product code compiled
first time and changed once after it (the save-hook timer). The test is 546 lines for a 205-line item; the house
stand-in is the reusable part of it for any later house-bound port.

Context: about 1.1M tokens of the 15M budget at this line.

## 8. D-numbers and questions

- **No new D-number.** Nothing in this task drops a ServUO behaviour. D-55, D-56, D-62 and D-68 are retired (§2);
  D-69 and D-70 are closed by Part B (P12's row). D-76 stays free.
- **No new question.** Two judgment calls are recorded here with their evidence for review to overturn rather than
  asked: additive registration instead of a `DefCarpentry.cs` patch (§4b, a one-file swap if review wants the patch),
  and `--fuzz=0` in the patch runner (§6, two tokens to revert). Q-055 stays free.
- **Two findings for `docs/bug-list.md`, both ours and both fixed here:** the patch gate applied a hunk with drifted
  context and said nothing (§6, the runner), and batch 4's egg fact asserted a 12.5% survival that the implementation
  makes 25% (§5, a test). And one for the standing entry on host gaps: `Timer.Start` inside `EventSink.WorldSave` logs
  an error per save; anything that wants "after the save" must post to `Core.LoopContext` (§6).
- For review: strike the four withdrawn rows in `docs/fidelity-principle.md`; mark P12 done and take the two hunks'
  count to "1 patch + 1 additive" in `docs/patch-backlog.md`; the "34 of P6's 88 want only this" line stands, with the
  rider that a creature in a `Uses` list (there are 11 types across the eight non-default definitions) needs its own
  `FireBreath` subclass, the `CrystalHydraBreath` shape, not `MonsterAbilities.FireBreath`.

## 9. Noticed in passing, not chased

- **Batch 6 (the name-mapping row):** nothing new. The alias hypothesis (batch 5 §9) was not touched; one adjacent
  fact worth having when it is: `[TypeAlias]` is `AllowMultiple = false` per batch 5, and stock `SmallOldHouse` is
  `partial` with the generator, so the partial-attribute trick would apply to multis exactly as to creatures.
- **Any later port with `SetSpecialAbility(DragonBreath)`** should read `SpecialAbility.cs:885-1063` first. Eight
  non-default definitions cover `SkeletalDragon`, `SkeletalDragonRenowned`, `Leviathan`, `RedDeath`, `FrostDragon`,
  `ColdDrake`, `AntLion`, `Rend`, `CrystalSeaSerpent`, `CrystalHydra`; `FrostDragon`/`ColdDrake` are cold at hue 1264,
  not `ColdBreath`'s 0x480, and `AntLion` is poison, which pinned has no breath for at all.
