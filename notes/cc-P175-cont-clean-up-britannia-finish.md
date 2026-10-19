# cc-P175: finish Clean Up Britannia (magic properties, monster corpses, the missing rewards)

2026-10-18. Opus. Prompt: `D:\UO\cc-prompts\cc-P175-cont-clean-up-britannia-finish.md`. Not committed (the Golem commits
after DONE). Both repos were clean at the start. Read first, as asked: P33's notes in full and P127's item 8 (map points
moved to the new map column with the level scale; nothing here touches maps).

## Headlines

- **Part A, magic properties add value.** A loot item now pays its material value plus its property weight / 30,
  ServUO's rule (ServUO `CleanUpBritanniaData.cs:811-816`; P33's notes cited it as :800-805).
  - The weight comes from **our imbue catalogue**, through one new function both systems use
    (`ImbueCatalogue.GetTotalWeight`): the properties the Imbuing Table sees.
  - Each property counts 100 at its Full value; our rows carry no per-property weight, while ServUO's run 100 to 150.
  - A plain longsword trashes for 1 point. With Hit Lightning 50 and Swing Speed 30 it pays 6: weight 150, + 5.
- **The anti-farm rule (P33's): crafted gear pays its materials only.** Measured, ServUO's rule breaks it three ways:
  - a dull copper runic hammer's craft adds up to **6 points for a 5-point use**;
  - exceptional crafted armor gets 15+ resist points from the craft (pinned `BaseArmor.cs:557-575`);
  - some crafted items are born with properties (RuneCarvingKnife, PhantomStaff).

  P33's own anti-farm fact went red on all of these. So properties count **only on items no player made**
  (`Item.PlayerConstructed`, which pinned's craft sets on every crafted item, `CraftItem.cs:1455` and `:1749`, and
  saves). Loot, and loot a player imbued, pay their properties.
- **Imbuing does not beat its cost.** Measured over 211 property and value pairs, every catalogue row at Full and at its
  top value: no imbued property adds more points than its imbuing gold would pay trashed (gold is 0.01 a coin).
  The closest is Night Sight, +3 points for 8 points of gold.
- **Part B, corpses pay by the creature:** the base is the creature's **Fame x 0.001**, plus every item inside, as before.
  - Examples: an orc 1.5, a lich 8, a dragon 15, an ancient wyrm 22.5, the champion Meraktus 70.
  - Base 0 for: a summoned creature, a pet (tamed, bonded, ever tamed), a creature with no Fame, and a kill the
    Custodian (or their party) did not earn by pinned's looting rights.
  - It counts toward the lifetime rank like any other points.
- **Part C: the store holds 122 of OSI's 134** (49 before; **73 ported**, in the prompt's order):
  - 36 single-file items;
  - all 24 pigments;
  - the six 300,000 charms;
  - the chaos and 8 virtue tiles, the fire pit, the horse barding, the dragon head and the beehive.

  **12 are still out**, each with what it needs (below).
- **Part D was already fixed.** cc-P36 widened the wood range in `CraftResources.GetType` to `<= Rootwood`
  (`ResourceInfo.cs:1174`). A fact per extended wood now pins it; they go red when the range is put back to Frostwood.
- **Part E:** the Sanitation Warden's text said "Corpses earn what is inside". It now says magic properties and the
  kill count. Nothing else on the Custodian or Clean Up gumps was stale; the token wording was already gone (P33).
- **Final build:** `Built sl-modernuo:cc-P175 with patches applied and 1541 shard test(s) passing` (1541 passed,
  4 skipped).

## What changed

`D:\ShatteredLegacy` (uncommitted):

| File | Change |
|---|---|
| `server/customizations/ArtificersImbueGump.cs` | `ImbueCatalogue.GetTotalWeight(item, skipDamageIncrease)` :776-798 (summary cites ServUO `Imbuing.cs:1330-1452`, `:1986-2016`): the sum of `IntensityPercent` over the item's active rows |
| `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs` | Header :13-16. `GetPointsForEquipment` adds `weight / 30` :293-299 (ServUO :811-816, integer division as ServUO's int weight). `PropertyWeight` :307-317: Damage Increase left out on weapons (ServUO's id 12; pinned has no `DImodded`), and 0 for `PlayerConstructed` |
| `server/customizations/Services/CleanUpBritannia/ClusterFCorpseValue.cs` (new) | Part B: on pinned's `CreatureDeathEvent` (`BaseCreature.cs:3669`), the base (Fame x 0.001, `Pays`) and who earned it (`GetLootingRights`, `BaseCreature.cs:3344`), held beside the corpse in a `ConditionalWeakTable` (not saved); `BaseFor(corpse, custodian)` with the party rule |
| `server/customizations/ClusterFCustodianSystem.cs` | Header :20-22; `CorpseBasePoints` (0.10) removed; `ComputePoints(item, by)` :155 and `ComputeCorpsePoints(corpse, by)` :163 take the Custodian; `[cleanup` :314 and `[cleanupall` :384 pass the player |
| `server/customizations/SanitationWardenGump.cs` | :130 the corpse and magic-property line |
| `server/customizations/Services/CleanUpBritannia/CleanUpRewardItems.cs` (new, 565 lines) | 36 rewards: 5 robes, lily pads 2, mushrooms 4, yucca, bamboo, nest, 2 tapestries, table lamp, 2 chests of drawers, presentation stone, Sherry, Nocturne earrings, 5 boots, 3 slayer instruments, 6 charms |
| `server/customizations/Services/CleanUpBritannia/CleanUpPigments.cs` (new, 407 lines) | `CompassionPigment`, its 28 kinds and their hue and cliloc table, and the 24 store pigments, generated from ServUO's two files |
| `server/customizations/Services/CleanUpBritannia/CleanUpRewardAddons.cs` (new, 545 lines) | Chaos tile, 8 virtue tiles (shared base), fire pit, horse barding, dragon head, beehive |
| `server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs` | Header counts. 73 `// MISSING` lines are now store rows, each marked `(cc-P175)` with its ServUO line |
| `server/tests/Services/CleanUpPropertyWeightVerification.cs` (new) | Part A and D facts |
| `server/tests/Services/ClusterFCorpseValueVerification.cs` (new) | Part B facts |
| `server/tests/Services/CleanUpBritanniaStoreVerification.cs` | Counts 49 -> 122 and the 11 tiers; the new fact 6 (all 73 ported, bought, round-tripped) |
| `server/tests/Services/CleanUpBritanniaPointsVerification.cs` | The measurement host marks its pieces `PlayerConstructed` as real crafting does (:518); a stale comment about the wood range (:536) |
| `server/tests/Services/CustodianLayerVerification.cs` | P33 fact 5: a corpse with no death on record pays its contents only |
| `server/tests/Services/Plants/RaisedGardenVerification.cs` | An unrelated flaky fact fixed so the gate can pass (Deviation 6) |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.18.16`: Added, Changed, Staff. VERSION 2026.10.18.15 -> .16 (.15 was committed with P174) |

`D:\UO\shard-migration`: this note; `testing\playtest-steps.json` (P175-1 to 3); `testing\bot-triage.md` (`### P175`);
`README.md`, `dashboard.html`, `tools\progress.json` from `tools\progress.py`.

No saved type changed version.
- The new items are new types, each at version 0, each round-tripped by fact 6.
- The corpse record is not saved, by design: a corpse lasts minutes.
- `PlayerConstructed` is pinned's existing saved flag.

## P33's citations at today's pin (d4531cd9; P33 cited 7c9215d97)

- **Moved:**
  - `BaseCreature.CreatureDeathEvent`, P33's :3216, is now raised at :3540 (a bonded pet's death) and :3669 (every
    other death).
  - The house trash barrel, P33's `BaseHouse.cs:2043`, is now :2077.
  - Ours: `ResourceInfo.cs:1095` is now :1174, and fixed.
- **Unmoved:** `ScrollofAlacrity.cs:10`, `FurnitureContainer.cs:142` (Drawer), `ChampionTitleSystem.cs`.
- **A ServUO citation in P33 was off:** the imbuing-weight call is ServUO `CleanUpBritanniaData.cs:811-816`, not
  :800-805.

## Part A in numbers

**Magic vs plain** (iron; fact 1):
- longsword, plain 1, magic 6;
- plate chest (Luck 100, Str 8, Mage Armor), plain 2, magic 12.

**Runic crafting, the most 2,000 rolls of pinned's `BaseRunicTool.ApplyAttributesTo` add** (fact 3):

| Tool | One use is worth | ServUO's rule would add | This build adds |
|---|---|---|---|
| Dull copper hammer | 5 | **6** | 0 |
| Shadow iron | 10 | 6 | 0 |
| Copper | 25 | 10 | 0 |
| Bronze | 100 | 10 | 0 |
| Gold | 250 | 13 | 0 |
| Agapite | 1,000 | 13 | 0 |
| Verite | 4,000 | 15 | 0 |
| Valorite | 8,000 | 16 | 0 |
| Spined sewing kit | 10 | 9 | 0 |
| Horned | 100 | 12 | 0 |
| Barbed | 400 | 15 | 0 |

**Trash vs unravel** for typical loot (fact 4). Unravelling pays Essence Shards and an essence, not points, so they are
two currencies (unravel results have no Clean Up value on OSI either):

| Loot item | weight | trash points | full disenchant (shards) | extract one (shards + essence) |
|---|---|---|---|---|
| Longsword, 35 SSI, 40 HLD | 138 | 5 | 7 | 2 + 1 |
| Plate chest, 10 phys, 8 str, 50 luck | 200 | 8 | 7 | 1 + 1 |
| Gold ring, 15 SDI, 10 DCI | 147 | 4 | 7 | 2 + 1 |
| Bow, 50 hit fireball, 15 HCI | 133 | 4 | 7 | 2 + 1 |

Neither beats the other by a mile: a typical piece is worth about 4 to 8 points in the barrel or about 7 shards at the
table. Which way a player goes depends on whether they want store rewards or imbuing.

## Part B: the sample table

Real kills in the test host (the Custodian's damage on record, then `Kill`). Contents are the loot that rolled in that run.

| Creature | Fame | Base | Contents (one run) | Corpse pays |
|---|---|---|---|---|
| Rabbit | 150 | 0.15 | 0 | 0.15 |
| Mongbat | 150 | 0.15 | 0.33 | 0.48 |
| Skeleton | 450 | 0.45 | 1.39 | 1.84 |
| BurrowScamp (Burrows tutorial) | 600 | 0.6 | 0.53 | 1.13 |
| Orc | 1,500 | 1.5 | 1.6 | 3.1 |
| TheBurrowMother (Burrows boss) | 3,000 | 3 | 1.79 | 4.79 |
| DreadSpider | 5,000 | 5 | 8.06 | 13.06 |
| Lich | 8,000 | 8 | 6.96 | 14.96 |
| OgreLord | 15,000 | 15 | 15.81 | 30.81 |
| Dragon | 15,000 | 15 | 31.33 | 46.33 |
| DreadWarhorse (ours) | 15,000 | 15 | 13.52 | 28.52 |
| AncientWyrm | 22,500 | 22.5 | 49.53 | 72.03 |
| Meraktus (a champion) | 70,000 | 70 | 212.48 | 282.48 |

What I chose, and why:
- **Fame is the scale:** it is the only per-creature difficulty number pinned has. The other, bard difficulty
  (`BaseInstrument.GetDifficultyFor`, :307), depends on the instrument. P20's notes have no other.
- **Earned means looting rights:** anyone may loot a creature's corpse (`Corpse.IsCriminalAction` is false for one), so
  the loot rule says nothing about who earned it. The rights list (`Corpse.cs:303-311`) does. A pet's damage counts for
  its master. A party member of a rights holder earns it too.
- **Pets: Owners, not Controlled.** A probe showed an unbonded pet's control is already released when the death event
  fires (controlled True before the kill, False at the event), so "ever tamed" (Owners, which `AnimalTaming.cs:440`
  fills) is what still says it was a pet.
- **Staff-spawned creatures pay like any other.** Pinned marks nothing a staff `[add` made, and your play test uses
  `[add`.

## Part C: the store

**122 of 134.**
- **Ported (73):** the 36 items, 24 pigments and 13 addons above.
- **Changes from ServUO,** each in the file headers:
  - `IsArtifact` dropped;
  - the instruments' random harp, lute or drums through pinned's constructor;
  - the tiles share a base;
  - DragonHead's "old" save-conversion classes not ported;
  - Beehive without ServUO's bees overlay (pinned has no `OnLockDownChange`).
- **Prices and sections:** exactly OSI's; fact 6 checks each against ServUO's line.

**Still out (12), with what each needs:**

| Reward (price) | Needs | Size | Stand-in we could sell instead |
|---|---|---|---|
| Mailbox (1,000) | nothing missing: a house mailbox (LockableContainer, house lookups) | 295 lines | none needed: portable, not reached this session |
| VollemHeldInCrystal (500,000) | the Vollem creature (ServUO `Mobiles/NPCs/Vollem.cs`); the crystal side is pinned's `BaseImprisonedMobile` | 137 + 73 lines | none needed: portable next |
| The fishing set, 8 pieces (50,000 each) | ServUO HS `Items/Sets/FishermansSet.cs`; our `SetItem.Fisherman` exists (`SetItem.cs:27`), `IFishingAttire` (the fishing bonus hook) does not | 525 lines plus the hook | the set without its fishing bonus, or wait for the hook |
| RefinementAmalgamator (10,000) | ServUO's Armor Refinement system (`Services/Armor Refinement/`, 3 files) | 1,086 lines | none of similar appeal; leave out |
| StewardDeed (10,000) | the Mannequin system (`Mobiles/NPCs/Mannequin/`, 4 files) | 1,086 lines, plus Steward's own 926 | leave out, or a stand-in decor deed at 10,000 |

## Tests (each new one seen failing first)

**New facts, 43 in all, across `CleanUpPropertyWeightVerification` (Part A, D), `ClusterFCorpseValueVerification`
(Part B) and the store test's fact 6 (Part C):**
1. A magic item pays its plain twin + weight / 30 (exact numbers). A crafted one (`PlayerConstructed`, exceptional
   bonuses, Luck) pays the plain chest's points; unmarked it would carry 175+ weight.
2. The imbue anti-farm measurement (211 row-values, every row at Full and top).
3. The runic measurement, 11 tools.
4. Trash vs unravel (printed).
5. The 8 extended woods resolve (type Wood, info, start).
6. The corpse sample table (13 creatures).
7. Summoned, tamed, bonded, fameless, unearned and unrecorded corpses pay no base; a party member earns it.
8. Corpse points raise the lifetime rank.
9. Every ported reward is in the store at OSI's price, is bought, and round-trips (reader stops where the writer did;
   art, hue and cliloc read back).

**Seen red, by mutation of the production code** (each file restored from a byte copy afterwards; `grep "P175
MUTATION"` finds nothing):
- **Run 1, the old behavior:** no property weight, the flat 0.10 corpse base, the wood range back to Frostwood, and the
  73 store rows commented out. **35 failed:**
  - all 13 corpse samples, the zero-cases fact and the rank fact;
  - the magic-vs-plain and trash/unravel facts;
  - all 8 extended woods (and P36's own 3 wood facts);
  - the three store facts;
  - P33's corpse fact.
- **Run 2:** weight x10 with crafted gear counted, and the never-tamed check removed. **16 failed:**
  - the imbue measurement and all 11 runic facts;
  - P33's two anti-farm facts;
  - the magic-vs-plain fact;
  - the tamed-pet case.
- **The first green-path run also caught real things before the fix:** the dull copper runic (6 for 5), P33's two
  anti-farm facts (RuneCarvingKnife, PhantomStaff), and the tamed pet paying (control already released at the death
  event). Those led to the `PlayerConstructed` and Owners rules.
- **Run alone** (only these classes, in the built builder image), they failed 3 until they set up the craft tables and
  accounts themselves, as P33's facts do (`CleanUpCraftHost.EnsureCraftSystems`, `EnsureAccounts`). Now 43 of 43 pass
  alone.

**Final:** the full gate, 1541 passed, 0 failed, 4 skipped. The two runs before it failed only on known flakes
(Deviation 6), with no code change between.

**Play-test tool tests:** 16 of 18. The 2 failures are earlier work (M-001, P163-0, P164-0, P165-1 to 6 have no Who
or Where). P175's three items pass the shape test.

## Play-test items added

Three, under **For Chase** below, sorted in `testing\bot-triage.md` (`### P175`), with steps and check lines in
`testing\playtest-steps.json`:
- **P175-1 BOT:** trash a magic and a plain longsword.
- **P175-2 BOT:** `[cleanup` an orc and a dragon you killed.
- **P175-3 BOT-PARTIAL:** buy decor, a pigment and a charm. The bot can buy them; the look is yours.

## Deviations and decisions for Chase

1. **Crafted gear's properties pay nothing.** It is OSI's and ServUO's rule to count them. Counting them lets a crafted
   piece out-earn its inputs: a dull copper runic craft pays 6 for a 5-point use; an exceptional iron plate chest pays
   about double its 2.5 points of ingots. That breaks P33's anti-farm rule, so only loot (items not
   `PlayerConstructed`) pays for properties.
   - A deviation for the register (agents do not edit `docs/`).
   - The alternative is OSI's rule plus the measured excess, like P33's wood and cloth decision.
2. **Every property weighs 100 at Full.** Our catalogue has no per-property weight; ServUO's are 100 to 150 (slayers
   and some hit spells weigh more). A loot piece pays a little less than ServUO's rule would.
   - Adding a weight column to the catalogue is a small follow-up if you want OSI's exact numbers.
3. **The corpse curve, Fame x 0.001,** is a judgment, like P33's 0.10 it replaces.
   - A champion corpse pays 70 plus a lot of loot.
   - Halve or cap it if you think 15 a dragon is too much next to the 25 / 125 / 500 / 1,250 ranks.
4. **Staff-spawned creatures pay like any other** (nothing marks them). A corpse from before a restart pays only its
   contents (the record is not saved).
5. **The 12 rewards still out** (table above). Mailbox and Vollem are portable as they stand; the fishing set needs a
   decision about its fishing bonus; the amalgamator and the steward need whole systems. Pick stand-ins or a follow-up.
6. **Flaky tests, unrelated to this work,** each passed in other runs:
   - `CC6Batch1CreatureVerification` (Skree control slots 3 / 2) and `CC6Batch2CreatureVerification` (HighPlainsBoura
     2 / 1);
   - `CC6Batch8Verification.MedusasGaze...` (Medusa picks another mobile);
   - `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`. This one **I fixed**, because it failed in every
     run of this prompt and blocks the gate: a new bowl starts with 10 hits and dry dirt deals 6 to 12 (pinned
     `PlantSystem.cs:619`), so its seedling died about half the time while the fact said it lived. It now starts at
     full hits and asserts that the dry bowl did not grow and either lost hits or died, which is what the fact
     meant.
   - The control-slot pair (P170, P173, P175) is worth a prompt of its own.
7. **Also seen, not changed:** about 6 of the Clean Up table's MISSING rows may now resolve to types later prompts added
   (`TastyTreat`, `BalmOfSwiftness`, `FeyWings` among them). Not checked one by one; a small follow-up.
8. **No task-list tool exists in this session,** so per-step progress was not posted there; these sections follow the
   prompt's parts in order.
9. **Not deployed:** the test shard was not rebuilt or restarted. `sl-modernuo:cc-P175` (and `sl-uo-builder:cc-P175`)
   exist, and `latest` was not moved. The throwaway mutation and solo builder images were deleted.

## For Chase

Rebuild the test shard from HEAD after the commit (or start it on `sl-modernuo:cc-P175`). Then, to try it in game:

1. **Magic vs plain:** `[add Longsword` twice. On one, `[props`, then Weapon Attributes > Hit Lightning 50 and
   Attributes > Weapon Speed 30. Right-click a trash barrel (or your trash bag), Appraise for Cleanup, and target each.
   **Pass:** plain about 1 point, magic about 6.
2. **Orc vs dragon corpse:** as a Custodian, `[add Orc` and `[add Dragon`, kill each yourself, then `[cleanup` each
   corpse. **Pass:** the orc about 1.5 points plus what is inside, the dragon about 15 plus what is inside. Optional: a
   corpse someone else killed pays only what is inside.
3. **The new store sections:** `[add RunicHammer Valorite 40`, put it in your trash bag and Dump Now (320,000 points).
   - Open the Cleanup Officer's store and page through it: robes at 1,000 up to the charms at 300,000.
   - Buy the Bamboo, a pigment and the Lucky Charm.
   - Use the pigment on an artifact in your pack.
   - **Pass:** each lands in the pack with its art and hue; the pigment dyes the artifact and counts down from 5 uses.

Also answer Deviations 1 to 5 when convenient.

## Repo size rule

No file over 5 MB in either repo. The largest new file is `CleanUpRewardItems.cs` at about 18 KB. Build logs,
mutation copies and generator scripts stayed in the session scratchpad, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (after `tools/progress.py`):

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

Code: 17 files pending (the table under What changed). Docs: 9 (this note, the two `testing\` files I wrote, the
importer's `testing\SUMMARY.md` and `testing\play-tests.json` refreshed from Haven by the dry run, and `README.md`,
`dashboard.html`, `tools\progress.json`, `tools\expansion-coverage.json` from `tools\progress.py`). Nothing BLOCKED.

P175 DONE
