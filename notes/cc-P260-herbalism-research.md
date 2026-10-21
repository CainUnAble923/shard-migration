# cc-P260: Herbalism and reagent growing, research

2026-10-20. Brief: `D:\UO\cc-prompts\claimed\Bronze\cc-P260-herbalism-research.md`. Design: `D:\UO\cc-prompts\design\
f-herbalism-reagents.md`, copied into `docs\feature-queue.md` as **F-51** (`:3450-3555`; next free is now F-52). That
entry is the one docs edit. No code, deploy or restart. Paths: "PIN" = `D:\UO\ModernUO-pinned\Projects\UOContent`, "SRV" =
`D:\UO\ModernUO-pinned\Projects\Server`, "C\" = `ShatteredLegacy\server\customizations\`, "P\" = `ShatteredLegacy\server\
patches\`, "T\" = `ShatteredLegacy\server\tests\`, "V\" = `D:\UO\ServUO-pub57\Scripts\`, "TAZ" = `D:\UO\tazuo-sl-build\
src\src` (the shard's TazUO source worktree; `D:\UO\TazUO` is a binary install). Every line was read today from the Bronze
work copies on `golem/Bronze/P260`; "unverified" marks what was not. Three subagents surveyed the plant engine, the skill
path and the house code; their citations were spot-checked before use.

## Headlines

1. **The raised garden beds are already ported.** cc-P128 brought ServUO's beds in (`C\Services\Plants\Raised Garden
   Beds\`, three patches, seven facts). Pinned has none. The bed is the home for the speed multiplier and the grace
   window, but a bed mound today has **no upkeep at all** (no water, no pests), so "grace on beds" means putting a slow
   upkeep back, not switching one off. Section 2.
2. **Plants do not tick on timers.** Growth runs when the world saves (every 5 minutes by default) and at login, over
   every plant whose 23-hour `NextGrowth` has passed. A per-plant speed is one virtual (`GrowthDelay`) in a patch the
   shard already maintains. Neglect today: a seedling dies in 2-3 unattended days, a grown plant in 3-4 (arithmetic in
   section 1), which is the design's base grace of 2 days already. Section 1.
3. **Two engine rules fight the design and need a decision.** Type crossing is the integer average of enum indices, so
   reagent types appended after the 43 stock ones would cross into bonsai and peculiar plants; and `PlantHue` is a flag
   enum the shard's dye and basket tables already key on, so "hue as strain tier" should be a separate `StrainTier` field.
   Both are cheap if decided now. Section 1, For Chase 1-2.
4. **Adding the skill is small on the server and awkward on the client.** Server: `Herbalism = 58` in the enum and a
   59th row in `Distribution\Data\skills.json` (the table is data, not code); our caps and totals follow
   `SkillInfo.Table.Length`; old saves load with the skill at 0. Client: names come only from `skills.mul`/`Skills.idx`,
   the player package may ship no mul (gate 4), so the entry is written into the player's own files by the existing
   override builder, and players with a saved skill-group XML will not see it until a small client patch adds unplaced
   skills to a group. Section 3 lists every file.
5. **Wild reagents already spawn.** Pinned ships 60 reagent spawners per facet (all eight magery reagents, 160 each,
   home range 200, respawn 11-23 minutes) and the shard imports that set. Foraging either replaces these or competes
   with free pickups. For Chase 7. Necro reagents are vendor-infinite (999 stock). Section 4.
6. **Yard tool and familiar are greenfield.** No yard system exists on this PC (third-party, ServUO or ours), pinned
   has no region around a house (only a placement-time 5-tile check), and no house-bound creature with a task AI. The
   hooks exist: `IsCoOwner`, the footprint bounds, the region lifecycle the Fountain's sanctum uses, `ForcedAI` on
   `BaseCreature`, and two `BaseHouse` points (collapse, transfer). Sections 7-8.
7. **Plan: seven phases**, skill plus reagent plants first (the only certain package push), beds, patches and ledger,
   kit, yard and plots, familiar, depth. The phase 1 draft prompt is at the end.

## 1. Plant engine (PIN `Engines\Plants`, 4,620 lines with the misc items)

**Files.** `PlantSystem.cs` (719: growth, health, maladies, seeds), `PlantItem.cs` (712: the bowl item, stages,
properties), `PlantType.cs` (483: the 43 types and their art), `PlantHue.cs` (167: hues and crossing), `Seed.cs` (221),
`PlantBowl.cs` (197), `PlantResources.cs` (49), `ReproductionGump.cs` (289), `PollinateTarget.cs` (90),
`MainPlantGump.cs` (468), `EmptyTheBowlGump.cs`, `SetToDecorativeGump.cs`, `MiscItems\` (Fertile Dirt, Green Thorns,
Orange Petals, Red Leaves). A `PlantItem` is an `Item, ISecurable` (`PlantItem.cs:34`) whose `PlantSystem` holds the
state (`:46-51`, saved only while the plant is growable).

**Growth ticks: no timers at all.** `CheckDelay = 23 h` (`PlantSystem.cs:30`) only stamps `NextGrowth` (`:60`, `:339`,
`:498`). Growth is driven by sweeps: `Configure` hooks `WorldLoad` and, unless auto-restart is on, `WorldSave`
(`:419-427`); each calls `GrowAll` (`:457-471`), which walks the static `PlantItem.Plants` list (`PlantItem.cs:36`) and
runs `DoGrowthCheck` on every growable plant not carried by a mobile whose `NextGrowth` has passed (`:466`). Login runs
the check on plants in the pack and bank (`:429-455`). So the cadence is the autosave interval, 5 minutes by default
(`World Saves\AutoSave.cs:38`); auto-restart defaults off (`Misc\AutoRestart.cs:56`; nothing in customizations sets it,
the shard's `modernuo.json` value unverified). If auto-restart were ever turned on, plants would stop growing between
restarts, which argues for a dedicated minute timer in the build (For Chase 12).

**One check (`DoGrowthCheck`, `:483-526`), in order:** stamp `NextGrowth = now + CheckDelay` (`:498`, before anything,
so a failed check still costs a day); refuse an invalid location (`:500-504`; valid = locked down with no parent, or in
the owner's pack or bank, `PlantItem.cs:168-184`); an empty bowl only dries (`:506-514`); beneficial effects (potions
cancel maladies; with none left and water at 2, hits +2 or +7 per heal potion, `:528-587`); malady damage: each of
infestation, fungus, poison, disease does level x 3-6, and water off 2 does |water-2| x 3-6 (`:589-622`); at 0 hits the
plant dies (`:127-134`: stage 7+ becomes dead twigs, earlier stages an empty bowl, `PlantItem.cs:520-531`); then `Grow`
(`:627-670`): below Healthy no stage; fertile dirt gives 10 percent double growth to stage 5; stage 9 yields one seed
per check if pollinated and one resource if the table has one (8 seeds and 8 resources per plant, `:63-64`, `:649-659`)
and self-pollinates if not (`:664-669`); finally new maladies roll (`:672-717`: infestation 30 percent base less potions,
+10 per water step off 2, +10 flowery, +10 bright; fungus 15 percent) and water decays 90 percent of the time (`:699-702`).
`MaxHits = 10 + stage x 2` (`:138`); health buckets Dying / Wilted / Healthy / Vibrant at 33 / 66 / 100 percent
(`:140-147`).

**A per-plant speed multiplier fits in one place.** Replace `CheckDelay` at `:498` and `:339` with a `PlantItem` virtual
(`GrowthDelay`, default `CheckDelay`), overridden by the bed mound as `CheckDelay / speed`. The shard already carries a
patch adding exactly this kind of virtual (`P\PlantItem-raised-garden-hooks.patch:9-14`), so it is two hunks. The 5-minute
sweep resolves a 4x bed (5.75 h) fine. Advancing several stages per check is worse: it would skip the per-stage malady
and pollination cycle. `CheckDelay` is used nowhere else: no gump text or message reads it (the gump paints only the
indicator, `MainPlantGump.cs:254-293`). Precedent for a custom cadence: `PottedCoffeePlant` keeps its own 23 h timer
(`C\Services\Plants\PottedCoffeePlant.cs:45, :110-116`).

**Neglect today (the arithmetic).** Planted at water 2 with nothing done: check 1 does no damage (water still 2),
check 2 does 3-6 (water 1), every check after 6-12 (water 0; dry dirt also drops infestation to 10 percent and fungus
to 0, `:674`, `:692`). Cumulative expected damage after checks 1-5: 0 / 4.5 / 13.5 / 22.5 / 31.5 (worst 0 / 6 / 18 / 30 /
42). Against `MaxHits` 12-14 for a seed or sprout, 16-22 for stages 3-6, 24-28 for stages 7-9: a seedling dies on the
third or fourth check, a mature plant on the fifth or sixth. **A seedling survives about 2-3 unattended days and a
grown plant about 3-4** (checks are 23 h apart, the first 23 h after planting). Growth stalls sooner: check 2 leaves
8-11 of 14 hits and growth needs 66 percent (`:629-632`), so about half of neglected seedlings miss day 2's stage. The
shard's own test reproduces the dry-bowl case (`T\Services\Plants\RaisedGardenVerification.cs:238-250`). The design's
"base grace 2 days" is roughly OSI's own number; the work is in extending it, not inventing it.

**Resources are finite.** A stock plant gives at most 8 resources and 8 seeds in its life, one per day at stage 9
(`:63-64`, `:649-659`). The design's starter farm ("50 to 100 regs a day" from a bowl or two and one bed) needs a
reagent lane that yields more per day and keeps yielding, which is a rule of its own, not a table row (For Chase 3).

**Types and how they cross.** 43 `PlantType` values (`PlantType.cs:5-47`), categories Default, five bonsai grades,
Peculiar, Fragrant (`:50-60`). Rows 0-16 (Campion to Tribarrel Cactus) are crossable and reproduce; bonsai 17-24 and
peculiar 25-41 neither; Cocoa Tree reproduces but does not cross (`:66-190`). `Cross(first, second)` (`:384-400`): any
non-crossable parent gives Campion Flowers; adjacent enum indices coin-flip; otherwise **the integer average of the
indices**. The "type ladder" is enum order, which is the design's "crosses average along it", but it also means a
reagent type appended at index 43 crossed with a Default type lands on a bonsai or peculiar index unless the reagent
lane gets its own crossing rule (a category check in `Cross`, or a separate `HerbType` ladder). For Chase 1.

**Hues and how they cross.** `PlantHue` is a flag enum (`PlantHue.cs:7-38`): Plain, Red, Blue, Yellow each
`| Crossable | Reproduces`; secondaries are ORs of primaries; Bright adds `0x8000000`; Black, White, Pink, Magenta, Aqua,
Fire Red carry neither flag (no pollen, no seeds). Client hues per value `:47-65`. `PlantHueInfo.Cross` (`:113-157`):
1 percent Black or White; Plain wins; same base gives its bright; two primaries give their mix; two secondaries give the
shared primary. Bright hues add 10 percent infestation. The design's "hue becomes strain tier along the metal hue
ladder" is a new axis: reusing `PlantHue` bits for tiers collides with these rules and with the pigment and basket tables
the shard already keys on `PlantHue` (`C\PlantPigmentHue.cs:80-92`, `P\CraftItem-plant-hue-tables.patch:9-22`).
**Recommendation: keep `PlantHue` for colour and add a `StrainTier` field on the mound and the seed**, shown as the
metal hue on the mound's art. For Chase 2.

**Seeds and resources.** Pollination (`PollinateTarget.cs:16-75`): both plants crossable, source at stage 7+ and at least
Healthy; seed type and hue from the two `Cross` functions, self-pollination keeps its own. Seeds come out of the
reproduction gump as `new Seed(type, hue, showType)` (`ReproductionGump.cs:268`), resources from
`PlantResourceInfo.CreateResource` (`:237`). The resource table is four rows (`PlantResources.cs:10-18`: Red Leaves,
Orange Petals, Green Thorns, Cocoa Pulp, each from named types in a bright hue). Fertile Dirt is not a resource; it is a
bowl flag giving the double-growth roll (`PlantSystem.cs:35-39`, `:633`). A reagent table is more rows of the same
shape (type gives `Garlic` etc.; reagent piles are `0xF84` Garlic, `0xF85` Ginseng, `0xF86` Mandrake, `0xF88`
Nightshade, `0xF7B` Blood Moss, `Items\Resources\Reagents\*.cs:9`).

**Art.** Stages 0-3 show a bowl of dirt, 4-6 a green bowl, 7+ the type's `ItemID` in the hue, dead twigs `0x1B9D`
(`PlantItem.cs:239-264`); the gump draws sprouts from `0xC62` (`MainPlantGump.cs:103-161`). A new type needs no client
change when the art exists: pinned already names the Pagan reagent decor (`Items\Special\Rares\PaganReagents\*.cs:9`:
garlic `0x18E1-0x18E4`, ginseng `0x18E9-0x18EC`, nightshade `0x18E5-0x18E7`); the tiledata read through vseUOAware
against the UOAlive client copy also has mandrake `0x18DD-0x18E0` and high-art `0xA8E5` garlic, `0xA8D2` ginseng,
`0xA8E9` mandrake, `0xA8F9` nightshade (presence in the shard's own client unverified). **Blood Moss has no plant art**
(only the pile `0xF7B`); it would reuse a fern or moss tile or take intake art. Plant names come from the art's tiledata
name unless clilocs are given (`PlantType.cs:235`); our own clilocs ship through the cc-P57 override path (section 3).

**What the shard already touches.** Nothing changes `PlantSystem` scheduling, `PlantType`, `PlantHue` or
`PlantResources`. Touchpoints: the raised beds (section 2), `PottedCoffeePlant`, basket weaving's `Clippers`
(`C\Services\BasketWeaving\Clippers.cs:133-153`), `PlantClippings`, `PlantPigment`, `NaturalDye`, and the plant-hue
colour tables patch (cc-P128).

## 2. Raised garden beds: already ported

Pinned has none (no `RaisedGarden`, `GardenBed`, `GardenShed` or art `19234` anywhere under `Projects`), and pinned's
`PlantItem` lacks the virtuals ServUO's bed subclass overrides. **cc-P128 ported ServUO's beds to this shard**
(`notes\cc-P128-port-consumables-crafting-gaps.md:74-75`, `:277`):

| Ours | Lines | What |
|---|---|---|
| `C\Services\Plants\Raised Garden Beds\RaisedGarden.cs` | 243 | `RaisedGardenAddon` (South, East, Large, Small; art 19234-19242, `:28-63`), `GardenAddonComponent` with a saved plant link (`:189-223`), chop refused while planted (`:68-93`), `RaisedGardenDeed` with direction gump (`:96-186`) |
| `C\Services\Plants\Raised Garden Beds\RaisedGardenPlantItem.cs` | 137 | the mound: `RequiresUpkeep = false`, own art and messages, immovable at plot Z+5 (`:22-27`), `ValidGrowthLocation` (`:76`), `IsUsableBy` = house owner or co-owner (`:132-136`), `ForceGrow` (`:84-96`) |
| `C\Services\Plants\FertileDirtGump.cs` | 78 | plant into a plot with or without fertile dirt |
| `P\PlantItem-raised-garden-hooks.patch` | 112 | adds six virtuals (`RequiresUpkeep`, `BowlOfDirtID`, `GreenBowlID`, three clilocs, `:9-14`), makes `ValidGrowthLocation` and `IsUsableBy` virtual (`:24`, `:48`), gates water and potions on `RequiresUpkeep` (`:63-108`) |
| `P\PlantSystem-raised-garden-upkeep.patch` | 53 | mounds: dirt always soft, no water or malady damage, no new maladies (`:12-49`), as ServUO (`V\Services\Plants\PlantSystem.cs:335, :523, :597`) |
| `P\Seed-raised-garden-plot.patch` | 39 | seed target accepts a plot (`:15-36`) |
| `T\Services\Plants\RaisedGardenVerification.cs` | 7 facts | `:131-336` |

ServUO's originals are 270 + 219 lines; the port is 662 lines across files and patches, done. Players have no source
for the deed yet: it is staff `[add` only (cc-P128 `:277`; no vendor, recipe or reward references `RaisedGardenDeed`
outside its own folder). **Consequences for Herbalism:** (a) the bed is the natural home for the speed multiplier and
the extended grace; (b) a mound today has **no upkeep at all**, so grace windows on beds mean re-introducing upkeep on
mounds at a slower decay rather than ServUO's all-or-nothing switch (For Chase 4); (c) one gap to carry: pinned's
`EmptyTheBowlGump` always hands back a `PlantBowl` (`EmptyTheBowlGump.cs:95`) where ServUO skips it for mounds
(`V\...\EmptyTheBowlGump.cs:76-82`), and the main gump's empty-bowl icon is not swapped (`V\...\MainPlantGump.cs:71-78`);
whether a test covers it is unverified. ServUO's Garden Shed (`V\Items\Addons\GardenShed.cs`, a 340-line storage addon)
is unrelated to growing and not ported.

## 3. Adding the Herbalism skill

**Server.** `SkillName` is `SRV\Skills.cs:17-76`, Alchemy 0 to Throwing 57 (58 values). `SkillInfo.Table` is **data,
not a literal**: `public static SkillInfo[] Table { get; set; } = Array.Empty<SkillInfo>()` (`Skills.cs:451`), filled by
`SkillsInfo.Configure` from `Distribution\Data\skills.json` (PIN `Skills\SkillsInfo.cs:135`); the file holds 58 rows
(counted), each with SkillID, Name, Title, stat scales and gains, GainFactor, ProfessionSkillName, primary and secondary
stat. Adding one at the end: `Herbalism = 58` in the enum (`:76`), an accessor in the `Throwing` pattern (`:767`), and a
59th JSON row. The docker build copies pinned's `Distribution\Data` as is (`docker\uo\Dockerfile:97`) and applies patches
from the repo root (`apply-patches.sh:14-16`), so a patch against `Distribution\Data\skills.json` carries it (no patch
touches a non-Projects path today; the first). No count constant: `Skills` sizes itself from `SkillInfo.Table.Length`
(`:465-467`, `:498-500`) and the indexer creates missing entries lazily (`:552-561`).

**Fixed 58s and switches in pinned.** `FeatureFlagManager._skillBlocks = new SkillBlockEntry[58]` (PIN `Engines\
FeatureFlags\FeatureFlagManager.cs:20`), bounds-guarded (`:484-485`, `:498`), so index 58 cannot be flag-blocked
rather than crashing (patch to `Table.Length`). `SkillsInfo.RandomSkill` caps at 58 for SA (`SkillsInfo.cs:13`), so
Herbalism is never rolled by random-skill items unless changed. `AosSkillBonuses.GetLabel` falls through to
`1042347 + (int)skill` (`Misc\AOS.cs:1312, :1323, :1339-1340`), an unrelated cliloc for 58: an item with "Herbalism +5"
mislabels until a case points at a shard cliloc. `Titles.GetTableType` defaults harmlessly (`Misc\Titles.cs:428-431`).
Character creation's whitelist and `AddSkillItems` just exclude it (`Engines\Character Creation\CharacterCreation.cs:20,
:446, :945`). `Commands\Skills.cs` parses by name and loops by length (`:25, :60, :83`), so `[SetSkill Herbalism` works.
`SkillCheck` has no per-skill switch (`Skills\SkillCheck.cs:126-133, :248-261`). Table walks that pick it up on their
own: `AOS.DisableStatInfluences` (`AOS.cs:17`), `ProfessionInfo` (`:37`), `SpecialScroll.GetSkillName` (`:39`),
`Teleporter` (`:389`), `DuelContext` (`:386`).

**Saves.** Skills serialize per mobile as version, cap, count, then one record per skill (`Skills.cs:816-838`,
`:345-380`); reading allocates `new Skill[info.Length]`, reads the saved count and fills `i < info.Length`
(`:498-518`). An old save with 58 entries loads into a 59-slot array; slot 58 is null until touched, then Base 0, Cap
100.0, lock Up (`:561`). **Existing saves load, Herbalism starts at 0.** The per-player total cap is saved (`:822`).

**Our overlays.** `ClusterFSkillCaps`: individual cap 200 (`C\ClusterFSkillCaps.cs:11`), `TotalSkillCap =
SkillInfo.Table.Length x 200` unless `clusterf.skillCaps.totalCap` is set (`:127-128`, `:30`; the stored value
unverified), re-applied at world load and login over `skills.Length` (`:32, :38, :167`), so a 59-row table gives
59 x 200 and lifts the new skill's cap to 200 by itself. `ClusterFSkillGain` wraps the four pinned handlers
(`:101-112`); `TryRow` switches on 16 named skills (`:318-403`), default = the stock window with the shard's
multipliers, so Herbalism gains at the base rate with no edit. Loop memory has no code (section 10). Enumerations
that include it silently: `ClusterFAchievements.CountSkillsAt` (`:1168-1174`), `ClusterFCompactAdminTools` (`:309-312`),
`ClusterFDevTools` (`:115`), `ClusterFLootBoxes.LevelOf` (`:58-66`, level = total / 10, so Herbalism raises box level),
`SmithSealScrollCensus` (`:85-89`), `Regions\ApprenticeTraining` (`:216`), `PackMule` (`:452-477`),
`TestCenter\TestCenterSkillGain` (`:60-70`), `TestCenterKit` (`:153`), `Mobiles\Bosses\Medusa` (`:674`),
`CleanUpBritanniaRewards` (`:274`, alacrity scrolls could roll Herbalism), `ClusterFStaffHub` (`:393-394`),
`ArtificersImbueGump` (`:196`). **Need a row by hand:** `ClusterFGuildStarterPath` guild table (`:46-64`), because
`EverySkillIsInExactlyOneGuild` enumerates every `SkillName` (`T\Misc\GuildStarterPathVerification.cs:418-432`) and fails
on a homeless skill; `CharacterCreation._allowedStartingSkills` (`:20-72`) and `AddSkillItems` (`:957`) if it may be a
starting skill; `ClusterFRecipeGate.BySkill` (`:389-400`) and `LootBoxRoller.BestCraft` (`:210-214`) only if Herbalism
is treated as a craft; `T\Engines\Craft\RecipeGatingVerification.cs:311` enumerates every skill (its assertion
unverified). Tests pinning 58: `T\Engines\Craft\CraftCeilingsVerification.cs:111` (`58 * 2000`, becomes `Table.Length`);
`TestCenterVerification.cs:139` asserts at least 58 (fine); `TwoHundredCapVerification.cs:120` uses `Table.Length` (fine).

**Client (TazUO at `client\TAZUO_COMMIT` 3212623f).** Skill names come **only** from the mul: `SkillsLoader.Load`
opens `skills.mul` and `Skills.idx` (TAZ `ClassicUO.Assets\SkillsLoader.cs:31-37`), walks every idx slot, skips empty
ones and numbers the survivors sequentially (`:41-54`), so Herbalism must sit in idx slot 58 with no gap. The EA
vanilla files (`D:\UO\UltimaOnlineVanilla`) hold 256 slots, 58 used, `skills.mul` 704 bytes (counted). No hard-coded
count: `PlayerMobile.Skills = new Skill[FileManager.Skills.SkillsCount]` (`ClassicUO.Client\Game\GameObjects\
PlayerMobile.cs:24`). An unknown index is dropped silently by the 0x3A handler (`Network\PacketHandlers\UpdateSkills.cs:
94`): no crash, the skill just never shows. TazUO reads a 0x3A sub-type 0xFE that carries names (`:23-45`) but pinned
never sends it (only 0x02 and 0xDF: `SRV\Network\Packets\OutgoingPlayerPackets.cs:119-146, :154-176`), and it would not
resize the player array anyway. **Groups:** `skillgrp.mul` is read only when the profile has no `skillsgroups.xml`
(`SkillsGroupManager.cs:204-215, :294, :488-545`); after that the saved XML rules (`:236-259`), and both skill gumps list
only grouped skills (`StandardSkillsGump.cs:308-316`, `SkillGumpAdvanced.cs:374-381`). So an existing player will not see
Herbalism until it is added to a group: a small client patch (unplaced skills go to Miscellaneous on load) or an XML
touch in `Play.ps1`. The server has no `skills.mul` dependence (grep of SRV and PIN: none).

**Shipping.** The player package forbids any mul, idx, uop or def in the zip (gate 4, `player-package\Build-PlayerPackage.
ps1:44-47`). Client data is patched **on the player's PC** from their own files by `payload\app\Build-UoOverrides.ps1`
(tiledata and animdata `:14-24`, `Cliloc.enu` `:26-35`, anim and bodyconv `:38-56`) into `app\uo-overrides\` with a
`files-override.txt` that `Play.ps1` passes as `-uofilesoverride` (`:9-10`, `Play.ps1:333`). cc-P57 Part D's clilocs
went that way (`Build-Cliloc` `:561-592`; `vendor\shattered-legacy-cliloc\entries.json`, `registry.csv` block 1,900,000+,
mirrored in `C\ShardClilocs.cs:21-31`; `notes\cc-P57-batch-6.md:153-192`). Override keys are lowercased in the loader
(`UOFileManager.GetUOFilePath`), so `skills.mul=` and `skills.idx=` lines are honoured. The TazUO build is
`client\Build-Client.ps1` (worktree at the pin plus `client\patches\0001-0003`, published to `D:\UO\tazuo-sl-build\client`,
`:1-20`); the package takes it by default (`Build-PlayerPackage.ps1:7-13`); no CI, Chase's machine. There is no skills
mul patcher yet; `Build-UoOverrides.ps1`'s binary writers (`Write-TileRecord :142`, `Write-AnimRecord :159`,
`Build-Cliloc :561`) are the model for a `Build-Skills` part.

**Files that change to add Herbalism**

| File | Change |
|---|---|
| new `P\Skills-herbalism.patch` on `SRV\Skills.cs` | `Herbalism = 58` (`:76`), `Skills.Herbalism` accessor (`:767` pattern) |
| new patch on `Distribution\Data\skills.json` | 59th row: SkillID 58, Name, Title, stat gains, GainFactor, ProfessionSkillName |
| PIN `Skills\SkillsInfo.cs:13` (optional) | RandomSkill bound 58 to 59 if random-skill items may roll it |
| PIN `Misc\AOS.cs:1312-1340` | a Herbalism case to a shard cliloc; rows in `entries.json`, `registry.csv`, `C\ShardClilocs.cs` |
| PIN `Engines\FeatureFlags\FeatureFlagManager.cs:20` | `new SkillBlockEntry[SkillInfo.Table.Length]` |
| `C\ClusterFGuildStarterPath.cs:46-64` | Herbalism under the Alembic (the test enforces one guild per skill) |
| `C\CharacterCreation.cs:20-72, :957` | only if it may be a starting skill |
| `C\Engines\Craft\ClusterFRecipeGate.cs:389`, `C\LootBoxes\LootBoxRoller.cs:210` | only if it counts as a craft |
| `T\Engines\Craft\CraftCeilingsVerification.cs:111` | `58 * 2000` to `Table.Length * 2000` |
| `T\` new facts | the table has 59 rows and row 58 is Herbalism; an old-format save loads it at 0; the total cap is 11,800 |
| `player-package\payload\app\Build-UoOverrides.ps1` | `Build-Skills`: copy the player's `skills.mul`/`Skills.idx`, write slot 58 and the name record, emit the two override lines (and a stamp); optionally `skillgrp.mul` |
| `player-package\Build-PlayerPackage.ps1:198-233`, `tests\` | a skills gate beside the cliloc gate; `Skills-Overrides.Tests.ps1` like the cliloc one |
| `client\patches\0004-*.patch` | `SkillsGroupManager.Load` puts any skill below `SkillsCount` missing from every group into Miscellaneous (`:204-259`) |
| `docs\feature-queue.md` F-51 | done in this prompt |
| no change | `ClusterFSkillCaps`, `ClusterFSkillGain`, every `Skills.Length` loop above, `Commands\Skills.cs`, pinned packets |

## 4. Reagents today

**Definitions.** Every reagent is a `BaseReagent : Item, ICommodity` (PIN `Items\Resources\Reagents\BaseReagent.cs:6`);
the folder holds the eight magery reagents, the five necromancy ones (Bat Wing, Daemon Blood, Grave Dust, Nox Crystal,
Pig Iron), Daemon Bone, Dragon's Blood and Dead Wood, plus the three bags. The spell system names them through
`Spells\Reagent.cs` (`m_Types` at `:8`, one static property per reagent from `:31`), so a grown reagent is the same item
type and needs no spell change. Mysticism spells name Dragon's Blood, Daemon Bone, Bone and Fertile Dirt
(`Spells\Mysticism\BombardSpell.cs:15`, `SpellPlagueSpell.cs:17`).

**Vendors (pinned, so ours).** Mage: the eight magery reagents at 3-5 gold, 20 in stock (`Mobiles\Vendors\SBInfo\
SBMage.cs:40-47`), and after ML the five necro reagents at 3-6 gold with **999 in stock** (`:51-55`); the variety dealer
also sells Bat Wing and Grave Dust at 999 (`SBVarietyDealer.cs:66-67`). Herbalist: Ginseng, Garlic, Mandrake,
Nightshade, Blood Moss (`SBHerbalist.cs:16-20`; the Herbalist NPC is `Mobiles\Vendors\NPC\Herbalist.cs:7`). Alchemist,
Glassblower, Healer, Holy Mage, Provisioner carry subsets. No vendor sells the mysticism reagents or Fertile Dirt (no
`typeof(DragonsBlood)`, `DaemonBone`, `FertileDirt` under `SBInfo`). Stock restocks hourly and a sold-out line doubles its
cap up to 999 (`GenericBuy.cs:105-109`, `BaseVendor.cs:130`).

**Wild spawn exists already.** Pinned ships `Distribution\Data\Spawns\shared\trammel\Reagents.json` and
`shared\felucca\Reagents.json`: **60 spawners per facet**, each with all eight magery reagents as entries, max count 160
each, home range 200, respawn 11 to 23 minutes (counted from the files; the first Trammel spawner is at 4282, 3700, and
they spread from x 342 to 6042). The shard imports `shared\**` and `post-uoml\**` (`C\ClusterFStockSpawnData.cs:11-16`;
`docker\uo\apply-patches.sh:440`; cc-P32 notes), so ground reagents already spawn on this shard. The spawner places items
like creatures (PIN `Engines\Spawners\BaseSpawner.cs:991`, `:1134-1140`). This is OSI's wild-reagent drop, not a pickable
plant; it is what a Herbalism forage would replace or gate (For Chase 7).

**Creature sources.** `BaseCreature.PackReg` (`Mobiles\BaseCreature.cs:5684`) and `PackNecroReg` (`:5661-5680`); 31
creature files call `PackReg`, 13 call `PackNecroReg`. Spider's Silk: six arachnids pack it directly (`GiantSpider.cs:43`,
`PackItem(new SpidersSilk(5))`; also Dread Spider, Frost Spider, Giant Black Widow, Terathan Drone and Matriarch).
Dragon's Blood and Daemon Bone come from `BaseCreature` helpers and the Dark Guardian (`Special\DarkGuardian.cs`).

**Hooks for the design's non-plant sources.**
- *Black Pearl from fishing:* pinned `Engines\Harvest\Fishing.cs` has the ML bonus table (`:113-118`, White Pearl at
  0.6 percent from 80 skill), `MutateType` (`:162`), `Construct` (`:213`) and `Give` (`:324`); our cc-P193 patch already
  overrides `GetResourceType` (`P\Fishing-high-seas-fish.patch:23-30`) and tags rare fish in `Give` (`:38-45`). A
  shoreline Black Pearl is one more `BonusHarvestResource` row or a branch in that `GetResourceType`.
- *Sulfurous Ash from volcanic mining:* our `Mining.Give` override (`C\CompactOreSatchelRoutingHook.cs:68`) sees every
  ore; a region or land-tile check there (lava, the Fire dungeon) adds ash beside the ore. The ML gem table
  (`Mining.cs:208-217`) is global, not by region, so the hook is the place.
- *Spider's Silk from webs and creatures:* already drops; a web static that gives silk is a new item.
- *Necro reagents:* vendor-infinite today, so a Herbalism source competes with a 3-gold vendor. The design's graveyard
  digging has no engine support: pinned's shovel is a mining tool only (`Items\Skill Items\Harvest Tools\Shovel.cs:7`,
  `BaseHarvestTool`), and digging exists only in treasure maps (our replacement copy `P\TreasureMap.cs`). A dig target
  on gravestone statics is new code (For Chase 8).
- *Imbuing gathering properties:* `ClusterFImbueEffects.OnGathered` (`C\Imbuing\ClusterFImbueEffects.cs:254`) is called
  by the gathering hooks with a `kind` string; Bountiful adds to the stack and Prospector rolls a rare find from a per-kind
  list (`:242-252`, kinds "mining" and "lumber"). A "herb" kind is one list in `ImbuingTable` and one call from the forage.

## 5. Wild patches and the ledger

**Placing respawning patches.** Three mechanisms exist:
1. **Spawners from a data file** (recommended): pinned's spawner spawns items (`BaseSpawner.cs:991`, `:1134`), the shard
   already ships and imports JSON spawn sets (`ClusterFStockSpawnData.cs:11-16`; the Despise exclusion shows a shard rule
   on import, `ClusterFDespiseStockSpawns.cs:19-24`). A `shard\herbs\*.json` set with a pickable `HerbPatch` item per
   biome gives placement, counts and respawn timers for free, and `[GenerateSpawners` places it. The 60 existing reagent
   spawner points per facet are a ready biome map, and the test world boots from the same import.
2. **Seeded coordinates**, as veins and groves (`ClusterFMiningExtension.cs:150`, `ClusterFLumberjackingExtension.cs:274`):
   deterministic and permanent, but it rides on a harvest definition, which herbs do not have.
3. **Seeder commands** like the New Haven and Rootdeep seeders (`C\ClusterFNewHavenServicesSeeder.cs`,
   `C\ClusterFRootdeepSeeder.cs`) for hand-placed sites such as the Alembic town farm.
The patch itself is a new `HerbPatch : Item` with a respawn timer, picked by double-click with a Herbalism check. Pinned
has no pickable-plant item class: the cotton and flax OSI picks are map statics, and `Items\Resources\Tailor\Cotton.cs:7`
is the picked resource, not the plant.

**Logging finds like the grove ledger.** The wood ledger is `ClusterFAccountData.WoodDiscoveries`
(`C\ClusterFAccountData.cs:73`), one `WoodDiscoveryEntry` per wood with `State` (Discovered, Reported) and a list of
`WoodLocationRecord` (facet, region, point, date, amount; `C\WoodDiscoveryEntry.cs:18-26`). The chop hook records a
grove on first find and merges chops within 15 tiles on the same facet and region (`C\ClusterFLumberjackingExtension.cs:
146-156`, `WoodDiscoveryEntry.cs:120, :133`). Reporting is a logbook button (`C\ForestersLogbookGump.cs:18-23, :475`)
that pays and marks Reported. Ore does the same with a per-vein Reported flag (`C\OreDiscoveryEntry.cs:17-35, :58`) and
the Survey Archivist (`C\SurveyArchivist.cs:51`, `:274-290`). An `HerbDiscoveries` dictionary of the same shape is one
field and one version bump of `ClusterFAccountData` (now `CurrentVersion = 20`, `:485`), plus an Alembic logbook on the
Forester's Logbook pattern (`C\ForestersLogbook.cs`). The achievement side already notifies on discovery counts
(`C\ClusterFAchievements.cs:1447`).

## 6. Proximity bonuses and upkeep

**Finding items near a bed.** `Map.GetItemsInRange(Point3D, range)` (`SRV\Maps\Map.ItemEnumerator.cs:46-62`; by
distance, `Map.ItemByDistanceEnumerator.cs:25-34`) walks the 8 x 8 sectors around a point, cheap for a radius of 2-4.
Inside a house the house's own lists are cheaper still: `BaseHouse.LockDowns`, `Secures` and `Addons` (section 7). The
growth check runs once a plant day, so a scan per bed per check costs nothing.

**Material tier and exceptional on crafted items.** Pinned has no single quality interface: `WeaponQuality`
(`Items\Weapons\WeaponEnums.cs:3`), `ArmorQuality`, `ClothingQuality`, `ToolQuality` (`Items\Skill Items\Tools\BaseTool.
cs:9`), `BookQuality`; resource is `CraftResource` on weapons, armor and clothing, and `BaseLight` (lanterns, lamps)
carries neither. Every crafted item gets `ICraftable.OnCraft(quality, makersMark, from, craftSystem, typeRes, tool,
craftItem, resHue)` (`Engines\Craft\Core\CraftItem.cs:21-26`), so **new kit items** (grow lamp, trough, trellis, pane)
implement `ICraftable`, keep `Quality` and the `CraftResource` from `typeRes`, and read their tier from
`ClusterFMetalTiers` / `ClusterFWoodTiers` as the rest of the shard does. F-29's rule (exceptional x1.5 on material
bonuses) applies by design.

**Durability and repair.** `IDurability` is `HitPoints` / `MaxHitPoints` (`Items\Misc\IDurability.cs:3-11`, an
*internal* interface). Repair (`Engines\Craft\Core\Repair.cs`) rolls `CheckSkill(skill, difficulty - 25, difficulty + 25)`
(`:47-75`) and then handles **only** `BaseWeapon` (`:236`), `BaseArmor` (`:310`) and `BaseClothing` (`:380`), with a
"TODO: Make an IRepairable" at `:163`. Kit items therefore need their own repair branch (a patch to `Repair.cs` keyed on
the making skill's craft system) or to be `BaseClothing`-shaped. Slow wear is a per-check `HitPoints` decrement in the
bed's growth check; "the skill that made it repairs it" falls out of Repair's craft-system dispatch once the branch exists.

## 7. Yard tool

**No yard system exists on this PC.** `D:\UO\third-party` has none (`CODE-INTAKE.md` lists no yard or garden code; the
only Xanthos file is a pet leash, `code\uo-wildlands-scripts\...\CUSTOM ITEMS\PetLeash.cs:3-5`), ServUO pub57 has only
the placement rule, and `D:\UO\ServUO-ShatteredLegacy` is empty (one empty `Server` folder). The community RunUO yard
systems the design mentions are not on this machine and the brief forbids fetching them, so the yard tool is greenfield.
The intake README already earmarks art: ph-flowers "Garden beds" (`third-party\README.md:62`), hanging-baskets "Yard tool
decor" (`:63`), garden-statues "Yard decor, gnome stand-in" (`:68`), azaleas (`:69`), fireflies (`:70`), pointy-red-hat
"Garden gnome familiar" (`:71`).

**What pinned gives a yard to hang on** (PIN `Multis\Houses\BaseHouse.cs`, 4,401 lines; `HousePlacement.cs`, 439;
`Regions\HouseRegion.cs`, 420):
- *Who:* `IsOwner` (`:3559-3561`), `IsCoOwner` (`:3563-3565`: owner, the co-owner list, or pre-AOS same account),
  `IsFriend` (`:3612`), `IsBanned` (`:3614`), `HasAccess` (`:3641`). The design's "owner and co-owners place" is
  `IsCoOwner`; the bed mound already uses it (`C\...\RaisedGardenPlantItem.cs:132-136`).
- *Where the house is:* `IsInside(Point3D, height)` (`:1513-1560`) is the footprint from `Components` (`SRV\Items\
  BaseMulti.cs:88`, `HouseFoundation.cs:117-126`); `FindHouseAt(Point3D, Map, height)` (`:1434-1449`) asks every multi in
  the sector. `HouseRegion` is the footprint only (`HouseRegion.cs:18, :46-61`), priority 12. **There is no region
  around a house.** The only "around" logic is at placement: `HousePlacement.YardSize = 5` (`:26`) and `CheckYard`
  (`:373-437`, called at `:271`) refuse another house within 1 tile or in the 5-tile front and back strips; nothing is
  persisted.
- *Counts:* `MaxLockDowns` (`:437`), `MaxSecures` (`:403`), `LockDownCount` (`:450-481`: lockdowns plus 125 per secure),
  `GetLockdowns` (`:3324-3347`); the lists `Addons` (`:512`), `LockDowns` (`:514`), `Secures` (`:516`), `Doors`, vendors.
  Addons register themselves on placement (`Items\Addons\BaseAddonDeed.cs:113`).
- *Collapse:* `Decay_Sandbox` (`:657-671`) kills vendors and deletes; `OnAfterDelete` (`:3371-3520`) unregisters the
  region (`:3380-3384`), releases lockdowns (`:3399-3414`) and secures (`:3434-3453`), **drops each addon's deed to the
  world and deletes the addon** (`:3455-3506`), deletes vendor inventories, kills vendors (`:3518`).
- *Transfer:* `TransferItem.OnSecureTrade` (`:3808-3845`) sets the owner and clears bans, friends and co-owners; the
  `Owner` setter (`:342-376`) resets nothing, so a yard or familiar hook belongs at `:3808-3845`, not the setter.

**Shape that falls out.** A yard is a second region per house: `IsInYard(Point3D)` beside `IsInside` from the footprint
bounds (the `GetItems` idiom, `:1254-1256`) plus a radius by house size; a `YardRegion` created where `UpdateRegion` makes
the `HouseRegion` (`:1645-1657`) and dropped where `OnAfterDelete` drops it (`:3380-3384`); yard items kept per house
serial in a `GenericPersistence` store (as `ImbueCustomStore` keeps item properties, `C\Imbuing\ClusterFImbueEffects.cs:
36-62`), so no `BaseHouse` save field is needed, and a two-hunk `BaseHouse` patch (collapse, transfer) releases or deeds
them and re-points the owner. `BaseHouse` is `abstract partial` (`:21`) and no shard patch touches it today, so the
build should expect the first. Placement refuses tiles inside another house or yard (`FindHouseAt` plus the yard test),
roads (land tile ids) and public plots (their region). Runtime regions are not saved: they are re-registered by their
owner after load, as the Fountain's sanctum region does (`C\FountainOfYouth\FountainSanctumRegion.cs:26-44`, re-created
in `FountainOfYouth.cs:129-137, :183-188`, removed in `OnDelete` `:175-180`). Region API: `SRV\Regions\Region.cs`
constructors `:130-178`, `Register` `:329-380`, `Unregister` `:382-417`, `Find(Point3D, Map)` `:291-312`; `regions.json`
is the only persisted source (`RegionJsonSerializer.cs:96-104`). Lockdown budget: yard items either count against
`MaxLockDowns` or carry a yard count of their own (For Chase 10).

## 8. Garden familiar

**Models in pinned.**
- `PlayerVendor` (PIN `Mobiles\Vendors\PlayerVendor.cs`, 1,319 lines) is a `Mobile`, not a creature (`:26`): no AI, no
  follower slot, `CantWalk` (`:87`), `House` saved with `OnHouseChanged` keeping `house.PlayerVendors` in sync
  (`:108-115`), a pay timer rebuilt after deserialization (`:197-203`), orphan recovery (`:212-238`: no house found,
  dismiss), `CanBeDamaged() => false` (`:1019`), `IsOwner` through the house (`:281-293`). Killed by the house on
  collapse (`BaseHouse.KillVendors` `:640-655`).
- `PlayerBarkeeper` (`Barkeeper\PlayerBarkeeper.cs`, 527) is a `BaseVendor`, so a `BaseCreature` with `AI_Vendor` and
  `FightMode.None` (`BaseVendor.cs:29, :65`); `DisallowAllMoves` and `NoHouseRestrictions` (`:163-164`); owner only.
- The shard's own house-bound mobile: the pet parrot (`C\Items\Addons\PetParrot.cs:82-84, :116-118`, `FindHouseAt` plus
  `IsCoOwner`).
- No house sitter, garden shed pet or ML house pet exists in pinned; no "task over beds" AI exists anywhere.

**What a familiar needs from `BaseCreature`** (PIN `Mobiles\BaseCreature.cs`, 6,061 lines):
- *No follower slot:* an uncontrolled creature costs nothing (`ControlMaster` is null unless controlled, `:1184-1186`;
  `AddFollowers` `:2639-2644`). So the familiar is **not** `Controlled`; it is bound by a saved house serial instead.
- *Despawn trap:* after load, any creature with `LastOwner != null && !_controlled && !IsStabled` gets a 3-day delete
  timer (`:2503-2508`). The familiar keeps `LastOwner` null or overrides this.
- *AI that survives restart:* `[AfterDeserialization]` calls `ChangeAIType` (`:2470-2519`, `:2512`), and `ChangeAIType`
  honours `ForcedAI` first (`:2589-2595`), so a `GardenAI : BaseAI` plugs in without touching the `AIType` enum
  (`AI\BaseAI\AIType.cs:18-30`). Its `DoActionWander` replaces `BaseAI.DoActionWander` (`BaseAI.cs:409-437`): pick the
  next job from the house's beds and bins, path to it, act, sleep.
- *Staying in the house and yard:* `Home` / `RangeHome` wander is a circle (`WalkRandomLogic.cs:98-126`); the region
  mechanism is `Mobile.WalkRegion` checked by `Region.OnMoveInto` (`SRV\Regions\Region.cs:748-749`), but the wander code
  clears it each step (`WalkRandomLogic.cs:77-81`). A `GardenAI` that only paths to targets inside `IsInside || IsInYard`
  needs neither. `HouseRegion.OnMoveInto` refuses uncontrolled creatures entering private AOS houses unless
  `NoHouseRestrictions` (`HouseRegion.cs:146, :155-158`), so the familiar sets it, as the barkeeper does.
- *Tasks:* the mound exposes `Pour` and `ApplyPotion` (gated on `RequiresUpkeep`, `P\PlantItem-raised-garden-hooks.
  patch:63-108`), the reproduction gump's harvest (`ReproductionGump.cs:237, :268`) and `Seed` planting
  (`P\Seed-raised-garden-plot.patch:15-36`); the familiar calls the same methods with itself as `from`, so every rule
  the player meets, it meets.
- *Transfer and collapse:* hook `TransferItem.OnSecureTrade` (`BaseHouse.cs:3808-3845`) to re-point the familiar's
  owner, and `OnAfterDelete` / `KillVendors` (`:3518`, `:640-655`) to turn it into a deed in the moving crate rather
  than delete it (For Chase 9).

**Bins.** A supply bin and a harvest bin are secure containers (`ISecurable`, as `PlantItem` is) the familiar finds
through the house's `Secures` list; the status gump lives on the supply bin as the design says. Tier, tasks and lines are
the familiar's own serialized fields; the lines table can follow `fanfare-lines.json` (`C\LootBoxes\ClusterFLootBoxes.cs:
287`) as a JSON file Chase can edit without a build.

## 9. Public plots and guild currency

**Rent ledgers today: none.** No weekly timer or rent exists in customizations (`FromDays(7` only a mule cooldown and
the chicken lizard egg; `Weekly` no code hits; `Rent` one achievement string). The timed-rent code on the box is pinned's:
`PlayerVendor.PayTimer` charging `ChargePerRealWorldDay` (`PlayerVendor.cs:98-100, :117-151, :170, :202`, `:1036-1045`),
restart-safe because `NextPayTime` is saved; and `RentedVendor` (`Mobiles\Vendors\RentedVendor.cs`, 358 lines:
`RentalExpireTime`, renewals by landlord and renter, `:56-60`, `:113-116`, rent to the moving crate `:158-162`; whether
it restarts its expiry timer after load is unverified). A plot ledger is simpler: one `GenericPersistence` store of
plots (id, rectangle, map, tenant account, paid-until, warned), an hourly world timer that charges a week of Drams on
the due date, warns a day before expiry (logbook line and a login message), and on expiry clears the plot (For Chase 11).

**Guild currency.** Per character: `CharacterGuildData.GuildCurrency` (`C\ClusterFAccountData.cs:753`), `GetCurrency`,
`SpendCurrency`, `AddCurrency` (`:926-935`). Priced purchases go through `GuildResources.TryPay(pm, guild, scripKey,
scrip, scripName, gold, materials)` (`C\GuildResources.cs:294-350`), all or nothing, scrip taken last, with `CanPay`
(`:351`). The Alembic's key is `"alembic"`, its currency placeholder "Alembic Drams" (`C\ClusterFAlembicGuild.cs:36, :41`),
six ranks on the generic ladder 0 / 1,000 / 5,000 / 15,000 / 50,000 / 100,000 (`RankNames` `:46-55`,
`ClusterFGuildSystem.GenericThresholds` `:618`). Weekly rent in Drams is `SpendCurrency` from the ledger timer; plot
count by rank reads `ClusterFGuildSystem.GuildRankIndex`.

**Region for a plot.** A `BaseRegion` rectangle re-registered at load from the store (the sanctum pattern in section 7;
static examples `C\Regions\RootdeepVault.cs:37-60`), with the plot mound's `IsUsableBy` checking the tenant instead of
`IsCoOwner`. The Alembic hall is the Little Shop of Alchemy in New Haven (`ClusterFAlembicGuild.cs:15`; seeded at
`ClusterFGuildStarterPath.cs:233`), the natural site for the town farm.

## 10. Hooks

- **Recipe gating:** `ClusterFRecipeGate` (`C\Engines\Craft\ClusterFRecipeGate.cs`) gates craft items by band and key
  per craft system (`Classify` `:126`, `IsKnown` `:246`); the owning guild per skill is `BySkill` (`:389-400`) and a
  Herbalism row would point at `alembic`. Craft guild rank needs the guild's craft skill per rank, 0/30/50/70/90/100
  (`C\ClusterFGuildPromotion.cs:3-5`, `ClusterFRecipeTable.cs:75`), updated from the craft menu (`ClusterFRecipeGate.cs:
  297`). The Alembic's skills are Alchemy and Taste ID (`ClusterFGuildStarterPath.cs:50`); adding Herbalism makes it a
  two-skill craft guild, which the promotion rule does not have today (For Chase 6). Strains and seed types "by Alembic
  rank" read `GuildRankIndex` directly; they are not craft items, so the recipe gate itself is not involved unless
  processing herbs into bundles is a craft menu entry.
- **BODs and commissions:** the 2016 bulk-order core and six crafts are built (cc-P122, cc-P123; `C\Services\BulkOrders\
  BulkOrderSystem.cs` header; the Alembic guildmaster gives Alchemy BODs, `CraftBulkEntries.cs:38`; `BODType` is widened
  by `P\BODType-all-crafts.patch:8-16`). A harvest order is a new `BODType` and deed, or, closer to the design, a rolled
  contract on the League engine, which is League batch 2 and **not built** (feature-queue `:102`; cc-P235 section 8).
  Renown is paid through `ClusterFAccountData.GrantRenown(amount, RenownSource)` (cc-P48).
- **Imbuing gathering:** `ClusterFImbueEffects.OnGathered` and `ProspectorFind` (`:242-262`), a `kind` string per gather;
  the property lists live in `ImbuingTable` (JSON), so "herb" is data plus one call.
- **Achievements:** `Reg(key, title, desc, cat, ap, renown, trigger, ...)` (`C\ClusterFAchievements.cs:1112`), 80
  registrations; triggers `T.Skill(SkillName, level)` (`:92`) and counted kinds (`:89`). "Green Thumb" is one `Reg` on a
  new counted `TriggerKind` fired from the harvest; no plant achievement exists today.
- **Loot box Scholar slot:** `C\LootBoxes\LootBoxRoller.cs:274-277`: the Scholar theme adds `Reagents(tier)` (`:344`) and
  a scroll; a seed roll by tier goes beside them, capped below the top strain tiers; `BoxTheme` is `ClusterFLootTable.cs:18`.
- **Loop memory:** designed (`notes\f12-levels-loops-caps.md:46-60`: faster gain below a skill's previous peak,
  compounding per loop, capped) but **not built**: `ClusterFSkillGain.cs` does rate and worn bonuses only (its header),
  nothing in customizations stores a skill peak, and the only "loop" code is the tutorial demo (`C\Tutorial\
  ClusterFLoops.cs`). Herbalism gets it when F-12 does; nothing to do now.
- **Alembic ranks:** `ClusterFAlembicGuild.GetRankName` (`:56`), six generic ranks (section 9).

## Phased build plan

Sizes are in cc-P prompt units: S = one sitting, M = a day with tests, L = two or three days or a split prompt.
"Package" marks a phase that needs a player package push.

| Phase | Prompt | Size | Needs | Package | What it delivers |
|---|---|---|---|---|---|
| 1 | Skill plus reagent plants | L | nothing | **yes** | `SkillName.Herbalism` (58), the `skills.json` row, the client entry through `Build-UoOverrides` and client patch 0004, the Alembic two-skill rank rule, five reagent `PlantType` rows with their own crossing lane, a reagent `PlantResources` lane with the perennial yield rule, `StrainTier` on mound and seed, Herbalism gain on plant, pollinate and harvest, the Scholar seed slot, "Green Thumb" |
| 2 | Beds as the farm | M | 1 | no | `GrowthDelay` virtual and the bed multiplier (Herbalism share, cap 2x), bed upkeep re-introduced at the slower rate with the grace window (base 2 days + Herbalism), Fertile Dirt on beds, a player source for the bed deed, the Empty-the-bowl gap, a dedicated minute timer for growth |
| 3 | Wild patches, ledger, other sources | M | 1 | no | `HerbPatch` item, a `shard\herbs` spawn set by biome (and the fate of the 60 reagent spawners), forage with Herbalism, `HerbDiscoveries` in account data (v21) with the Alembic logbook and Report, the Imbuing "herb" kind, Black Pearl on the shoreline roll, Sulfurous Ash in the volcanic mining hook |
| 4 | Garden kit and upkeep | L | 2 | no | the four categories as `ICraftable` items with Quality and `CraftResource`, the proximity scan in the bed's check, structure wear and a Repair branch, consumables and the supply bin, cap 4x |
| 5 | Yard tool and public plots | L | 2 | no | `IsInYard`, the `YardRegion` lifecycle, the yard item store, the tool's placement gump, counts by house size, the two `BaseHouse` hunks; the plot store and region, weekly Drams rent, warnings, expiry, plot count by rank, the town farm seeder |
| 6 | Garden familiar | L | 4, 5 | maybe | `GardenAI` on `ForcedAI`, the house binding, tiers and tasks, bins, the Alembic quest end with the sprout or gnome choice, transfer and collapse; a package push only if the gnome or sprout uses intake art |
| 7 | Breeding depth and side uses | M | 1, 3 | no | necro and mysticism herbs at 100-150, exotic herbs at 150+, mutation up a tier by Herbalism, Cooking and Healing side uses, harvest orders once the League engine exists |

**What blocks what.** 1 blocks everything (every gain roll and gate names the skill). 2 and 3 are independent after 1
and can run beside each other. 4 and 5 need 2 (the kit and the yard are about beds); 5's plot half also needs 2's bed
source. 6 needs 4's bins and 5's yard (it must know where it may walk). 7 is the long tail and needs League batch 2 for
the harvest orders only. **Only phase 1 needs a package push for certain** (the client skill entry); phase 6 might, for
art. Everything else is server-only and ships with a normal build. Phase 1 could be split 1a (skill and package, M) and
1b (plants, M) if the package push is wanted early so it can carry other pending client changes.

**Order recommended:** 1, then 2 and 3 together, then 4, 5, 6, 7.

## For Chase (decisions the code forces)

1. **Crossing lane.** Reagent types must not average into the stock enum (`PlantTypeInfo.Cross` averages indices).
   Proposal: reagent and stock plants do not cross at all (pollen refused across lanes), and reagent crosses average
   along the reagent ladder only. Yes?
2. **Strain tier as its own field**, not `PlantHue` (the shard's dye and basket tables key on `PlantHue`, and the
   mutation hues carry no pollen). The mound shows the metal hue from the tier; the plant keeps a colour of its own.
   Yes?
3. **Perennial yield.** OSI plants give 8 resources in a lifetime, one a day. For the design's 50-100 reagents a day
   from a starter farm, reagent plants need a yield rule of their own: proposal, a mature reagent plant gives N
   reagents per harvest (N by type, tier and Herbalism), every day, and never runs out while tended; bowls keep OSI's
   finite rule for stock plants. Confirm the shape; numbers are placeholders.
4. **Beds get a slow upkeep back.** Today's mounds never need water and never get pests. For grace windows on beds,
   proposal: mounds need water every grace period (2 days base, up to 7 at 200 Herbalism) and take maladies at a third
   of bowl rates; or keep beds carefree and put grace only on bowls. Which?
5. **Client entry route.** The skill name is written into each player's own `skills.mul`/`Skills.idx` by the override
   builder (the package may ship no mul), plus client patch 0004 so players with a saved skill-group file see it. Also
   decide whether Herbalism can be a starting skill at character creation.
6. **Alembic rank with two skills.** Craft guild rank requires the guild's skill per rank; the Alembic now has Alchemy
   and would gain Herbalism. Proposal: the higher of the two counts. Yes?
7. **The 60 OSI reagent spawners per facet.** Keep them (free pickups beside foraging), remove them (foraging is the
   wild source), or turn their points into herb patches? Recommendation: turn them into patches.
8. **Graveyard digging** has no engine support (the shovel is a mining tool); it is new code. Build it in phase 3, or
   leave necro reagents to vendors and League hunts (vendors hold 999)?
9. **Familiar on house collapse:** becomes a deed in the moving crate (recommended) or dies with the house?
10. **Yard budget:** yard items count against the house's lockdowns, or a separate count by house size?
11. **Expired plot:** crops die to twigs and items go to the tenant's bank or moving crate; or everything is deleted
    after the warning? Recommendation: the former.
12. **Growth cadence.** Plants grow on the autosave sweep today; proposal: a dedicated one-minute timer for the plant
    list so growth never depends on saves or auto-restart. Yes?
13. **Blood Moss art:** no plant art exists; reuse a fern tile, or take intake art (ph-flowers and friends) and accept a
    package push in phase 1 for it?
14. **Bed deed source:** Carpentry recipe (Foresters' recipe gate) or the Alembic shop for Drams?

## Draft build prompt, phase 1 (for the overseer to number once Chase answers)

```
# CC task P???: Herbalism phase 1: the skill and reagent plants (F-51)

**Model:** Fable

**Touches:** server (a Skills.cs patch and a Distribution\Data\skills.json patch; C\Engines\Plants\ additions for the
reagent lane; C\ClusterFGuildStarterPath.cs, C\ClusterFGuildPromotion.cs, C\LootBoxes\LootBoxRoller.cs,
C\ClusterFAchievements.cs; AOS.cs label case; tests), client (client\patches\0004 skill groups), player package
(payload\app\Build-UoOverrides.ps1 Build-Skills part, gate and tests). Needs a player package push.

**Summary:** Add the Herbalism skill end to end and the first reagent plants (Garlic, Ginseng, Mandrake, Nightshade,
Blood Moss) on the OSI plant engine, per notes\cc-P260-herbalism-research.md sections 1 and 3 and Chase's answers to
its For Chase list (1-3, 5, 6, 13).

Read first: notes\cc-P260-herbalism-research.md (sections 1, 3, 10 and the For Chase answers); docs\feature-queue.md
F-51; notes\cc-P128-port-consumables-crafting-gaps.md (the beds); notes\cc-P57-batch-6.md Part D (client overrides);
PIN Engines\Plants\PlantType.cs, PlantResources.cs, PlantSystem.cs; SRV\Skills.cs; TAZ ClassicUO.Assets\SkillsLoader.cs
and Game\Managers\SkillsGroupManager.cs.

**Ours.**

## Do

1. **The skill on the server:** `Herbalism = 58` and its accessor (a patch on SRV\Skills.cs); the 59th skills.json row
   (a patch on Distribution\Data\skills.json; Title "Herbalist", Int primary, Dex secondary, GainFactor as Alchemy's);
   FeatureFlagManager sized by Table.Length; the AOS label case to a shard cliloc; Herbalism under the Alembic in
   ClusterFGuildStarterPath; the two-skill promotion rule per Chase; CraftCeilingsVerification's 58 to Table.Length.
   Facts: table has 59 rows and row 58 is Herbalism; an old-format skills record loads with Herbalism at 0 and cap
   200 after ClusterFSkillCaps; total cap 11,800; `[SetSkill Herbalism 100` works.
2. **The skill on the client:** `Build-Skills` in Build-UoOverrides.ps1 writes the player's skills.mul/Skills.idx copy
   with slot 58 "Herbalism" and emits the override lines; a Pester test like Cliloc-Overrides.Tests.ps1; the package
   gate; client patch 0004 so a saved skillsgroups.xml gains the skill under Miscellaneous. Rebuild the client and the
   package through the normal scripts (take the package lock).
3. **Reagent plant types:** five PlantType rows in a reagent lane (own enum range or category), art per section 1
   (Blood Moss per Chase's answer 13), names through shard clilocs, crossing per answer 1 (a fact that a reagent x
   stock cross is refused and a reagent x reagent cross stays in the lane).
4. **Strain tier:** `StrainTier` on the mound/bowl and on Seed (serialized, versioned), 0 to Celestial on the metal
   ladder; the plant's displayed hue from the tier; seeds inherit the higher parent's tier; same-tier crosses mutate up
   a tier with a chance from Herbalism (placeholder 5 percent at 50, 25 percent at 200); a fact per rule.
5. **Yield:** the reagent PlantResources lane per answer 3: a mature reagent plant yields N per harvest, every day,
   N from type, tier and Herbalism (placeholder 4 at tier 0 and 0 skill, 12 at Celestial and 200); harvest from the
   reproduction gump as today; a fact per step of the curve.
6. **Gains:** a Herbalism CheckSkill on plant (0-50 window), pollinate (type tier window) and harvest (tier window),
   through pinned's handlers so ClusterFSkillGain's rates apply; a fact that each path can gain and that bowls alone
   cannot pass 50 (the design's first tier).
7. **Hooks:** Scholar box seed slot (a reagent seed of tier at most box tier - 2); "Green Thumb" achievement on the
   first reagent harvest; the Herbalist vendor sells reagent seeds of tier 0.
8. **Wiki:** one page, Herbalism: the five plants, how tiers and crossing work, where seeds come from, no numbers the
   curve can change.

## Done means

- Tests red then green through docker\uo\build.sh with the image tag the Golem hand-off gives; the package and client
  build green with their own tests; a client-test queue of 6-8 rows (the skill shows in both skill gumps for a new and
  an existing profile, a plant grows and yields, a cross stays in the lane, a tier mutation).
- Notes: headlines, what changed (file:line), the facts, the red run, the package and client steps.
- Patch notes: one ### Added line (players: Herbalism, grow your own reagents) and one ### Staff line (the override and
  the data patch) per the CHANGELOG comment; bump VERSION.
- Commit preflight: Commit-ShardWork.ps1 -DryRun result table in the notes.
- Finishing: do not commit; last line of the notes P??? DONE; end the final chat message with P??? DONE.
```

## Commit preflight

Run 2026-10-20 from the Bronze desk with `Commit-ShardWork.ps1 -DryRun`. The script reads the three main checkouts
(code, docs, scripts), not this Golem's worktrees, so "code clean" is the main checkout; this branch's two changed
files (`docseature-queue.md`, this note) are committed by the Golem after P260 DONE. The two docs files it lists are
the play-test importer's output, committed with each prompt.

| Repo | Result |
|---|---|
| code | clean |
| docs | dry run (2 pending: `testing/SUMMARY.md`, `testing/play-tests.json`) |
| scripts | clean |

Prompts with a finished note: none for P260 (it lists cc-P180, cc-P181 and cc-P185 as not ending in DONE or STOPPED,
which is not this task).

P260 DONE
