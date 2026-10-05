# cc-P61: batch 7 (post-Valorite gain ceiling, earned achievement progress, post-Valorite deed metal names, P57 patch notes)

Builder task, 2026-10-05. Brief: `D:\UO\cc-prompts\cc-P61-batch-7.md`. Engine authority: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today); every pinned file:line below is against it.
`C\` = `D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`, `T\` = `server\tests`, `PKG\` = `player-package`,
`PIN\` = `D:\UO\ModernUO-pinned\Projects\UOContent`. Scratch: `D:\UO\cc-p61-work\` (`make-red.py` the red trees, `build1.log`,
`red1.log`, `red2.log`, `red2b.log`, `build-final.log`, `detail.log` the facts' printed numbers, `pkg\` the test package,
`pkg-red\` and `pkg-red.log` the package red run, `ea-lines.ps1` EA's material lines).

Shard HEAD `28916a3` (P60 committed). Uncommitted when I started: only `design\kitsune-ears-tail\` (the art chat's work in
progress; Chase said to ignore it, and I did not read or touch it; it kept changing while I worked). **No clash** with
another builder. Nothing committed, nothing deployed, no shard restarted, `sl-modernuo:latest` not moved
(`d5519301f920`, cc-p57's image, before and after), nothing published, the wiki page not published.

## Headlines

1. **All four parts done.** Final `docker\uo\build.sh -t sl-modernuo:cc-p61`: **47/47 patches** (46 plus
   `BOD-gumps-post-valorite-material.patch`), **869/869 shard facts** (837 + 32 new cases), image `sl-modernuo:cc-p61` = `9349dc9c9826`. Package: a
   fresh build in `D:\UO\cc-p61-work\pkg\` passed gates 1 to 6 (the cliloc gate now checks both ways), `-CheckZip` passed gates
   4, 5, 6; package tests 8 + 10 + 20 green.
2. **Red then green.** Server red1 (all three parts' behavior back to HEAD's): **12 failed** / 857. red2 (Part A's ceiling table
   off, hook and teaching kept): **11 failed** / 858 (first run); and again 11 / 858 with the revised A5b (red2b). Package: the new cliloc facts against HEAD's package
   scripts and files: **3 of 3 new failed** (7 old passed).
3. **Part A: the metal raises only the gain ceiling, through one hunk in our existing `CraftItem-shard-hooks.patch`.** The gain
   roll is pinned's own `Mobile.CheckSkill`; only its window moves, and only from the item's own maximum up. Success chance,
   failure, material loss and exceptional chance read the item's own range and are unchanged (fact A4 compares against
   pinned's formula). The chain from 140 to 200 has no gap (table below).
4. **A design consequence to know (decision 2):** a smith at 150 is offered Platinum, Toxic, Blaze or Frost by the small-order
   metal roll (Platinum half the time), but only **Frost** still teaches at 150 (Platinum stops at 125, Toxic at 137.5, Blaze
   at 150). So about 2% of a 150 smith's Society small orders teach in their metal; the rest are the fallback, as before. Crafting
   itself is not affected: the smith picks the metal at the forge.
5. **Part B:** one condition. 23 counted achievements over 11 trigger kinds checked earned and not earned.
6. **Part C:** eight clilocs 1900003-1900010, one line per pinned method in a new 4-file patch (4 methods: both deed gumps,
   which both tooltips call, and both accept gumps). Rollout: **package first, then server**, as P57.

## What changed (all uncommitted)

Shard (`D:\ShatteredLegacy`):
- `C\ClusterFMetalTiers.cs:51-82` (A): `GainCeiling(CraftResource)` and `GainCeiling(BulkMaterialType)`, from the tier constants.
- `C\ClusterFCraftGain.cs` (A, new): the window (`:35`), the craft's metal (`:46`), the hook (`:61`).
- `P\CraftItem-shard-hooks.patch` (A): one new hunk (`@@ -890,7 +910,8 @@`, `:59`), the gain call.
- `C\ClusterFSmithTeaching.cs` (A): `Teaches(m, type, gainCeiling)` (`:71`) reads the same window; `PickItems` and `PickSets`
  take the ceiling (`:118`, `:151`).
- `P\SmallSmithBOD-teaching-orders.patch` (A): the small order's pick passes the deed's metal.
- `C\ClusterFSmithCommissions.cs` (A): `TeachingKey` and `TeachingSet` take the commission's metal (`:197`, `:365`, `:511`, `:558`).
- `C\ClusterFAchievements.cs:2046-2053` (B).
- `C\ShardClilocs.cs:31-75` (C): eight constants and `PostValoriteMaterial`.
- `P\BOD-gumps-post-valorite-material.patch` (C, new) and its argued comment, `docker\uo\apply-patches.sh:378-387`; the Part A
  hunk is named in the CraftItem comment, `:255-258`.
- Facts new: `T\Engines\Craft\PostValoriteGainCeilingVerification.cs` (A), `T\Misc\AchievementProgressLineVerification.cs` (B),
  `T\Misc\PostValoriteDeedMaterialLineVerification.cs` (C). Updated: `T\Misc\SmithOrdersTeachVerification.cs` facts 1, 3, 4
  read "teaches" in the order's own metal.
- Package: `PKG\vendor\shattered-legacy-cliloc\entries.json` and `registry.csv` (8 entries), `PKG\Build-PlayerPackage.ps1:96-127`
  (the gate both ways), `PKG\tests\Cliloc-Overrides.Tests.ps1` (one new fact, one new bad-file case, the server/package fact
  covers all 11 constants).
- `CHANGELOG.md` (D and the patch notes), `VERSION` 2026.10.05 to 2026.10.05.2.
- No save shape changed; no migration JSON.

This repo: this note only.

## Part A: D83, post-Valorite metals raise the Blacksmithy gain ceiling

**Where pinned rolls the gain.** `CraftItem.CheckSkills` (`PIN\Engines\Craft\Core\CraftItem.cs:845-857`) calls
`GetSuccessChance(..., gainSkills: true)` (`:860`), which for each craft skill calls `from.CheckSkill(skill, minSkill,
maxSkill)` with the item's own range (`:891-894`). `SkillCheck.CheckLocation` (`PIN\Skills\SkillCheck.cs:56-75`) gains nothing
below min, nothing at or above max, and between them rolls `CheckSkill` with `chance = (value - min) / (max - min)`; the gain
chance is `gc = ((totalCap - total) / totalCap + (cap - base) / cap) / 2 + (1 - chance) * 0.5 (on a passed check)`, halved
(`:108-158`); the gain is `Gain` (`:236-281`), which obeys the lock, the skill cap and the total cap. The metal never enters the
roll: it gates use only (`CraftItem.cs:630`, `Skills[MainSkill].Base < RequiredSkill`). The success chance is computed after the
gain loop from the item's own range (`:902-904`).

**Data checked.** All 139 Blacksmithy items are 50 points wide (min + 50 = max); the highest maximum is 140 (the kabutos).

**Change (the least).** One line in the gain loop: `from.CheckSkill(skill, min, max)` becomes
`ClusterFCraftGain.CheckSkill(from, this, craftSystem, typeRes, craftSkill)`, which calls the same `from.CheckSkill` with:
- the item's own (min, max) when the craft is not Blacksmithy, the skill is not the main skill, the item is made of scales
  (`UseSubRes2`), the metal has no ceiling (iron, Dull Copper..Valorite), or the smith is below the item's max: **stock**;
- otherwise (min, max) = (ceiling - 50, ceiling), the item's own width slid up so its top is the metal's ceiling.

The metal is the craft's `typeRes`, or the craft's default when the player never picked one (`HammerMetal.CraftedResource`, the
same rule as Metal Familiarity, cc-P46 G).

**Patch versus hook, argued.** A hook alone cannot do it: the skill-check handlers (`Mobile.SkillCheckLocationHandler`,
already wrapped by `ClusterFSkillGain`) receive only (mobile, skill, min, max), not the craft or its metal; reading the
player's last-picked resource from `CraftContext` instead would be wrong for Craft X runs and the default resource. So the call
site needs one line, and it goes into our existing `CraftItem-shard-hooks.patch` (already a patch of this exact file and
method, `--fuzz=0`), not a new patch. Everything else is customization code.

**The gain band, argued.** Three choices for the window between the item's max and the ceiling:
1. **Slide the item's window up (chosen):** (ceiling - width, ceiling). The roll at distance d below the ceiling is exactly stock's
   roll for that item at distance d below its own max: chance = 1 - d / 50. A smith works a metal only from its requirement,
   12.5 below the ceiling (Celestial: 0), so in the band d is 0 to 12.5 and chance 0.75 to 1. Example: at 150 in Frost, chance
   0.75, the same roll stock gives a 112.5 smith on a plate tunic (75-125). It ends at the ceiling exactly as stock ends at a max.
2. "As if the item's max were the ceiling": (item min, ceiling). The chance then depends on the item's minimum: at 150 in Frost a
   plate tunic rolls (75, 162.5) chance 0.857 and a dagger near 1.0, so cheap items would teach markedly slower than plate for
   no reason a player could see, and the window jumps from width 50 to 87.5+.
3. A flat chance: not stock's shape at all.

What stock does at the same distance below a max (option 1's claim), from the formula: the item-dependent part of `gc` is
`(1 - chance) * 0.5` on a passed check (probability `chance`), so the expected bonus is `chance * (1 - chance) / 2`: 0 at the
ceiling, 0.094 at 12.5 below (chance 0.75), the same at the same distance below any item's max. The rest of `gc` (room under the
cap and the total) is pinned's and unchanged. With every width 50, every item teaches the same in the band, so the cheapest
item in a metal is as good a trainer as plate (decision 3).

**The chain (fact A1 prints it):**

| Metal | Needs (Base) | Teaches to (ceiling) | Next metal needs |
|---|---|---|---|
| Iron .. Valorite | 0 .. 99 | the item's own max (top: 140, the kabutos) | Platinum 112.5 |
| Platinum | 112.5 | 125 | 125 |
| Toxic | 125 | 137.5 | 137.5 |
| Blaze | 137.5 | 150 | 150 |
| Frost | 150 | 162.5 | 162.5 |
| Obsidian | 162.5 | 175 | 175 |
| Mythril | 175 | 187.5 | 187.5 |
| Adamantium | 187.5 | 200 | 200 |
| Celestial | 200 | 200 | (the cap, 200) |

No gap: stock items teach to 140, past where Platinum opens (112.5); every ceiling is the next metal's requirement, so the next
metal opens exactly where the last stops; at 140 Blaze (137.5) teaches to 150; Adamantium reaches the cap. Celestial teaches
nothing (it needs 200, the cap). Note: gains stop when **Value** reaches the ceiling (pinned's rule reads Value), while the
metal gate reads **Base**, so a held Hammer of Hephaestus or other Blacksmithy bonus stops the gain that many points early.
That is stock's behavior for any item.

**Teaching agrees (target 4).** `ClusterFSmithTeaching.Teaches(m, type, gainCeiling)` computes the same window with the same
function, so it cannot disagree. Where the metal is known before the pick it is passed: small Society orders (the post-Valorite
roll comes before the item pick, our `SmallSmithBOD-PostValorite.patch` then `SmallSmithBOD-teaching-orders.patch`), small and
large commissions (`mat` is chosen first). A large order's set is chosen before its metal (stock's order of rolls in
`LargeSmithBOD.CreateRandomFor`, our full replacement), so that pick still reads the item's own range; changing that would
reorder stock's rolls, and I did not. A large post-Valorite deed still teaches when made, whatever its set.

**Facts** (`T\Engines\Craft\PostValoriteGainCeilingVerification.cs`, numbers from `detail.log`):
- A1: the table above (ceilings = next requirement, Celestial = the 200 cap; stock metals none; stock top 140).
- A2 (10 cases): the window the craft hands `CheckSkill`, read off the handler. **150 Frost plate: (112.5, 162.5), can gain.
  162.5 Frost plate: (112.5, 162.5), no gain. Valorite plate at 140: (75, 125), no gain.** 140 Blaze: (100, 150) gains;
  187.5 Adamantium (150, 200) gains; 200 Celestial none; below the max (115 Platinum plate, 60 iron broadsword) the item's own.
- A3: a real gain through pinned's SkillCheck (RNG held at 0): 150 Frost 150 -> 150.1; 140 Blaze 140 -> 140.1; 162.5 Frost and
  140 Valorite unchanged.
- A4 (10 cases): `GetSuccessChance` equals pinned's formula on the item's own range, with and without the gain roll (e.g. 150
  Frost plate 1.5000, 140 Valorite plate 1.3000, 115 Platinum plate 0.8000; above 1 is pinned's own, it is a certain success).
  Exceptional chance follows from it unchanged.
- A5: 38,318 (skill 100..200, 17 metals, every Blacksmithy bulk order item) cases: `Teaches` == "the craft's window can gain";
  7,846 of them teach past the item's own max. 150 Frost teaches, 162.5 Frost not, 140 Valorite not.
- A5b: at 150 a Society small order in Frost teaches; in Frost the pick offers every armor piece the smith can make, with no metal
  only the fallback PlateChest (deterministic, on `PickItems`); a 400-order sample is printed (4 of 400 in Frost on one run, 2 on another). Green: in Frost 24 of 24 armor entries; red2b: 1 of 24.
- `SmithOrdersTeachVerification` facts 1, 3, 4 now read "teaches" in the order's metal; at 120 and 130 commissions are post-Valorite
  (Platinum/Toxic), so they now offer the whole makeable list (e.g. 130: PlateDo, kabuto, dragon chest, spears, swords...).

Register line (next free **D-122**; D-121 is P57's, proposed and not yet in `docs\fidelity-principle.md`, which ends at D-120):
- **D-122 Ours (cc-P61 A, Chase 2026-10-05).** Crafting a Blacksmithy item in a post-Valorite metal can raise Blacksmithy past
  the item's own maximum, up to the next metal's requirement (Platinum 125 .. Adamantium and Celestial 200), with stock's roll
  for the same distance below a maximum; success, failure, material loss and exceptional chance are unchanged. OSI: the item's
  range only. | Blacksmithy 140-200 by crafting | `visible`
- Amend the cc-P42 G "orders that still teach" entry: "in the order's metal" (small orders and commissions).

## Part B: D84, earned achievements still showed progress

**Cause.** `RowLines` (`C\ClusterFAchievements.cs`) added "Progress: n/m" for any achievement with a counter, earned or not, and
counters keep counting after the goal ("Oh Look, It's Dead": goal 1, kills 9). Only one place draws progress; the Unlocked popup
has none.

**Change** (`:2046-2053`): `!earned &&` on the progress line; the earned-only gray color went with it. The Earned line stays.

**Facts** (`T\Misc\AchievementProgressLineVerification.cs`): B1 every counted achievement (23, 11 trigger kinds: Kills,
OldHavenMageKills, UndeadKills, RatmanKills, OrcKills, OldHavenKills, ColoredOreMined, OreTypesDiscovered, IngotsSmelted,
NewHavenQuests, Logins) earned with its counter at nine times its goal: the row in the real gump (every tab, every page) has its
Earned line and no "Progress:" (printed: "Oh Look, It's Dead [5 AP / 5 R] | ... | (Earned: slew your first creature)"). B2 the
same not earned, counter at a third: the 15 visible ones show "Progress: n/goal" (the hidden ones are not listed until earned).

## Part C: D85, post-Valorite deeds name their metal

**EA's line** (`D:\UO\UltimaOnlineVanilla\Cliloc.enu`, read by `ea-lines.ps1`): 1045149 "All items must be made with valorite
ingots." (1045142-1045148 the same for dull copper .. verite, lower case). Ours, D-114's Title Case:

| Number | Text |
|---|---|
| 1900003 | All items must be made with Platinum ingots. |
| 1900004 | All items must be made with Toxic ingots. |
| 1900005 | All items must be made with Blaze ingots. |
| 1900006 | All items must be made with Frost ingots. |
| 1900007 | All items must be made with Obsidian ingots. |
| 1900008 | All items must be made with Mythril ingots. |
| 1900009 | All items must be made with Adamantium ingots. |
| 1900010 | All items must be made with Celestial ingots. |

None of these is used in EA's file (0 entries in 1900000-1999999, counted today).

**Patch versus hook, argued.** The line comes from four `public static int GetMaterialNumberFor` (`PIN\Engines\Bulk Orders\
SmallBODGump.cs:85-98`, `LargeBODGump.cs:106-119`, `SmallBODAcceptGump.cs:99-112`, `LargeBODAcceptGump.cs:112-125`); the tooltips
call the deed gumps' (`SmallBOD.cs:64`, `LargeBOD.cs:55`). Static methods on pinned classes, called by pinned code: no override or
hook reaches them, and replacing the gumps would hide upstream drift. So a patch, the smallest: in each, the fall-through
`return 0;` becomes `return ShardClilocs.PostValoriteMaterial(material);`, which is ours for the eight metals and 0 for
everything else (pinned's value). One file, four hunks of one line, applied after `BOD-combine-contained.patch` (which edits the
two deed gumps above it) and generated against that state. I included the accept gumps (not named in the brief): they had the
same blank line when a post-Valorite deed is offered.

**Package side.** `entries.json` and `registry.csv` carry the eight; `Build-UoOverrides.ps1` adds them to the player's copy
unchanged (it reads entries generically): against EA's real file the copy has 124,011 entries (124,000 + 11). **The gate,
extended:** `Test-ClilocEntries` now also fails when a number registry.csv lists is missing from the file, so a number the server
sends cannot ship without its text (before, only the other direction was checked). It runs on the vendored file before staging
and on the zip's `app/cliloc-entries.json` (gate 4).

**Facts.** Server (`T\Misc\PostValoriteDeedMaterialLineVerification.cs`): C1 for each metal, a small and a large deed: the deed
gump and the accept gump on the wire carry the number, and the tooltip lists it (8 x 6, all true); C2 every other material keeps
pinned's number (1045142..1045149, 1049348..1049350, None 0; a Valorite tooltip still 1045149); C3 the eight follow 1900002 in
order, in the block. Package (`Cliloc-Overrides.Tests.ps1`, now 10): new fact "ThePostValoriteDeedLinesAreEAsValoriteLineWithTheMetalNamed"
(each text = EA's 1045149 with the metal named, read from EA's file); the gate fact has a new case (Celestial left out: "lacks
1900010"); the server/package fact covers all 11 constants.

**Rollout:** package first, then server (same reason as P57: a client without our entries shows an empty line; here a deed's
material line is blank, not a menu row, so the cost of the wrong order is smaller, but still the line is missing).

## Part D: P57's patch notes and two stale lines

In `CHANGELOG.md`, 2026.10.05 (the newest section when the brief was written; P57 is in the test shard's image under that
version, `latest` = `cc-p57`):
- Added: our own menu words (Breed, Smelt Ore, Metal Familiarity; take the launcher's update); the Society guildmaster's
  small/large choice.
- Changed: Seal catalog prices x3; post-Valorite deeds bank more Seals; the achievements window layout.
- Fixed: achievement rows no longer run into each other; the Stealing pile fix.
- The two stale lines: "Mining them still needs 100" is now "smelts and mines at the same steps ... Below a metal's step, its
  vein gives iron."; the menu labels line now says "Smelt Ore" and "Breed"; the Added line about the hammer now says "Metal
  Familiarity" (it said "Knowledge").
- Post-Valorite ore needing its tier is in the fixed smelt line (one line, not two).

## Patch notes (this task)

2026.10.05 is committed (`2663209`, `28916a3`), so this task starts **2026.10.05.2** and `VERSION` is bumped. Changed: the gain
ceiling line; "Orders that still teach me" counts the order's metal. Fixed: earned achievements show no progress line;
post-Valorite deeds name their ingots (take the launcher's update). Note: players who saw 2026.10.05's bulletin will not see the
P57 lines added to it (the bulletin shows once per version); they are on the wiki page when it is next published.

## Facts, red then green

| Fact | Red | Green |
|---|---|---|
| A1 the ceilings and chain | red2 | green |
| A2 windows with a ceiling (6 of 10) | red1, red2 | green |
| A2 below the item's max (4 of 10) | **never red by design**: stock windows | green |
| A3 gains (2 of 4) | red1, red2 | green |
| A3 no gain (2 of 4) | **never red by design** | green |
| A4 success chance (10) | **never red by design**: the guard that success is pinned's | green |
| A5 agreement | red1 (hook off, teaching on: they disagree); red2 (150 Frost) | green |
| A5b the 150 small orders | red2 (first and revised versions) | green |
| `SmithOrdersTeachVerification` | **never red**: its teaching checks now take the metal on both sides | green |
| B1 earned, no progress | red1 | green |
| B2 not earned, progress | **never red by design** | green |
| C1, C3 | red1 | green |
| C2 | **never red by design**: pinned's materials | green |
| Package: 3 new or changed facts | 3/3 red against HEAD's package | 10/10 |

red1: 869 tests, **12 failed** (A2 x6, A3 x2, A5, B1, C1, C3), 857 passed. red2: 869 tests, **11 failed** (A1, A2 x6, A3 x2, A5,
A5b), 858 passed. red2b (the same tree, A5b revised to its deterministic form): **11 failed**, the same eleven.

## Builds

| Build | Command | Result |
|---|---|---|
| 1 | `build.sh -t sl-modernuo:cc-p61 --tests-only` | **47/47 patches; 869/869** (two earlier tries stopped: a hunk count I miscounted in the small teaching patch, and two analyzer errors in my new test, both fixed) |
| red1 | `red1\docker\uo\build.sh -t sl-modernuo:cc-p61-red1 --tests-only` | 47/47; 869, 12 failed |
| red2 | `red2\docker\uo\build.sh -t sl-modernuo:cc-p61-red2 --tests-only` | 47/47; 869, 11 failed |
| red2b | red2 again with the revised A5b | 47/47; 869, 11 failed |
| detail | `dotnet test` in `sl-uo-builder:cc-p61`, the four classes, verbosity detailed | all passed; numbers in `detail.log` |
| final | `build.sh -t sl-modernuo:cc-p61` | **47/47; 869/869, image `9349dc9c9826`**; `latest` still `d5519301f920` |
| package | `Build-PlayerPackage.ps1 -Out D:\UO\cc-p61-work\pkg` | gates 1-6 green; `ShatteredLegacy-2026.10.05.1041.zip`, 76 MB, 740 files |
| package | `-CheckZip` on it | gates 4, 5, 6 passed; its `app/cliloc-entries.json` holds the 11 entries |
| package tests | `Build-UoOverrides` 8/8, `Cliloc-Overrides` 10/10, `Launch-Settings` 20/20 | green (`scripts\tests\Shard-Console` not run: nothing it covers changed) |

The package zip is a test build (it records uncommitted player-package changes); build again after the commit.

## Deviations and decisions for Chase

Register: **D-122** (Part A, text above); amend cc-P42 G's "orders that still teach" (in the order's metal); Parts B, C, D: none
(C's numbers go under the client-policy cliloc block with P57's).

Decisions:
1. **Gain band shape:** I chose stock's roll at the same distance below a max (window slid up). Say if you want the band
   faster or slower; the place is `ClusterFCraftGain.Window`.
2. **Post-Valorite small orders rarely teach a high smith** (headline 4): the metal roll gives Platinum 50%, Toxic 25%, Blaze
   12.5%, Frost 6.25% ..., capped by what the smith can work, so at 150 only ~2% of orders are in a metal that still teaches
   (Frost). Option: when "Orders that still teach me" is on, roll the post-Valorite metal among those whose ceiling is above the
   smith (Frost at 150-162.4, Obsidian at 162.5-174.9, ...). Not built.
3. **Every item teaches alike in the band:** a dagger in Frost trains a 150 smith as well as a plate tunic, for 3 ingots instead
   of 25. That is what "the metal raises the ceiling" means with every item 50 wide. If you want plate to matter, the band could
   use option 2 (item min to ceiling), which favors hard items. Not built.
4. **Large Society orders** still pick their set before the metal (stock's roll order); the deed teaches in its metal once made.
   Reordering is possible in our full `LargeSmithBOD.cs` if you want the pick to see the metal.
5. **Accept gumps** got the line too (not in the brief; same bug).
6. **The P57 lines** went into 2026.10.05 as the brief says; players already past that bulletin will not see them in game.

## For Chase

Package first (Part C), then the server. Windows PowerShell unless noted.

1. Commit both repos (`design\kitsune-ears-tail\` is the art chat's, not mine).
2. Build the package from the commit: `D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1 -Notes "Post-Valorite smith deeds name their ingots"`
   (gates 1-6 must pass), then `D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1 -CheckZip <the new zip>`.
3. Publish it as usual (`D:\UO\haven-migration\Publish-PlayerPackage.ps1`, per `docker\downloads\README.md`), run `Play TEST Shard.bat`
   and accept the update.
4. Deploy the server to the test shard: `docker tag sl-modernuo:cc-p61 sl-modernuo:latest`, then
   `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down`, then `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`.

In game on the test shard:

5. **Gain ceiling (A):** `[SetSkill Blacksmith 150`, Frost ingots and a hammer: craft plate tunics (or daggers); Blacksmithy rises
   now and then. `[SetSkill Blacksmith 162.5`: no more gains in Frost; switch to Obsidian and it gains again. With Valorite at 140:
   no gains. The success rate looks the same as before.
6. **Teaching orders (A):** at 150 with "Orders that still teach me" on, ask for small orders until one is Frost: its item can be any
   armor piece, not only a plate tunic.
7. **Achievements (B):** `[achievements`, Combat: "Oh Look, It's Dead" shows its Earned line and no "Progress: 9/1"; an achievement
   not yet earned still shows its progress.
8. **Deed lines (C):** `[add SmallSmithBOD` (or ask the guildmaster) until a Platinum..Celestial deed; open it: "All items must be
   made with Frost ingots." (or its metal); hover it: the same line in the tooltip. A large one the same. Then start
   `app\tazuo\TazUO.exe` directly (no launcher): the line is blank there (what an un-updated player sees).
9. `[version` shows 2026.10.05.2 and the bulletin shows its four lines.
10. Promote to `docs\`: D83, D84, D85 closed in `bug-list.md`; D-122 and the cc-P42 G amendment in `fidelity-principle.md`; numbers
    1900003-1900010 in the client policy's cliloc block.

P61 DONE
