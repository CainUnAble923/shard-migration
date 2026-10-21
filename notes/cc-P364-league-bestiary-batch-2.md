# cc-P364: League hunt bestiary, batch 2 (fourteen renamed creatures on package bodies 2072-2085)

## In plain words

- Fourteen new monsters are in the game, each with a name of ours, stats on the shard's level scale, loot and a
  monster part: hedge snatchers, their mounted outrider, hornback raiders and ditch crawlers in the hills and gullies
  around New Haven (levels about 12 to 34); mire croakers in the swamps; brine lurkers in Covetous, moonmaws and
  thornwisps in the Yew woods, pale drifters in Deceit, slaghearts in Fire, glasswardens in Ice and tunnelmaws in
  Shame (levels about 40 to 60); and two mini-bosses for a group, the Siegebreaker in Covetous and the Hollow Oak in a
  Yew clearing (levels 78 and 84).
- The first time you kill one, the System adds it to your bestiary with a snarky line and a plain one, and every one
  of them sits in a League hunt table or culling table that F-24's job board will read when it is built (there was no
  such table before this prompt; this is the first).
- Their art ships in the player package: 14 more creature bodies (about 20 MB of animation source, every file under
  5 MB) on the route cc-P139 built, nothing of EA's touched, and a new package check proves no stock body is
  overwritten.
- For you: build and publish the player package (Player package > Build, then Publish) and rebuild the test shard
  from this commit; then `[ClusterFSeedBestiary dryrun` and `[ClusterFSeedBestiary` on the test shard to place the 25
  spawners, and look at a few of them in a client (the bodies draw, walk, attack, die; the parts drop). The numbers
  are first proposals, listed below, for you to tune.

Builder: Claude (Fable), the Bronze Golem, 2026-10-21. A fresh session on `golem/Bronze/P364` (ShatteredLegacy at
`7b11ab4`, shard-migration at `8afc52c`), both clean. Pinned is `D:\UO\ModernUO-pinned` (`d4531cd94`). Image
`sl-modernuo:cc-P364`; `latest` untouched. Nothing has run against any world.

## Status: finished on 2026-10-21

## Headlines

- **Fourteen creatures, fourteen bodies (2072-2085, anim7 slots 22-31 and 203-206), five authors credited**: Kalamarr,
  EmuResource, Vertigo and uodev (uo-pixel.de), Vert-I-Go (Humanoids) and Thagoras (Plant Pack). Every .vd is in the
  package byte for byte, `check-vd` said "free and matching" for every body against the 7.0.117.0 client, both
  registry gates read 0 problems over 623 rows, and the encoder's `--check` decoded every block back identical.
- **The League hunt and culling tables did not exist**: F-24 (hunts, culls, dives) is in the feature queue, unbuilt;
  `RequisitionSystem.HuntFamily` is its only seam. So Part 2's "add each to the tables" became **the first such
  tables**: `ClusterFLeagueBestiary.Entries` (type, in-game name, use, home, part, level band, the two lines),
  with `HuntTargets` (targets and mini-bosses) and `CullingPacks` as the two views F-24 will read. Nothing else reads
  them yet; the facts do.
- **Bestiary lines show once, on the first kill**: the creature's death event (`CreatureEvents.CreatureDeathEvent`,
  the hook achievements use) records the type in the account's `EncounteredCreatures`, the set `ClusterFAccountData`
  already kept for hunting work orders and nothing was writing, and sends the killer the System's line in its own hue
  and the plain line in parentheses. Only this table's creatures are recorded.
- **Homes are spawn data**: 25 spawner rows (`ClusterFLeagueBestiary.Spawners`) placed by `[ClusterFSeedBestiary`
  (dry run, re-run skips what stands, nothing moved or deleted), on Haven Island tiles checked walkable on the
  7.0.117.0 map, two swamp tiles, and stock spawner tiles from pinned's own `shared/trammel/*.json` for the dungeons.
- **A new package fact: no stock body is overwritten.** `player-package\tests\fixtures\stock-bodies-7.0.117.0.txt`
  lists every body the stock client names or draws (1,327 numbers from `validate-art.py bodies --all`); the fact
  refuses any registered body or `bodyAnims` body on that list, any body inside pinned's `bodyTable.cfg` range (1973
  and below) or past the server's table (0x1000), a body registered twice, two bodies on one anim7 slot, and a body
  row without its `bodyAnims` entry. 21 of 21 package facts pass.
- **Tests:** `LeagueBestiaryVerification`, five facts (constructs, typed body, spawns, dies to a corpse with the body;
  serializer round trip of creatures and parts; fights a player, drops its part, enters the bestiary once; in exactly
  one table with part, home, lines and a level inside its band; spawn data resolves and the seeder places every row
  once). Red then green in section 6.

## 1. What was read, and the picks

Read: `ART-LIBRARY.md` section 3 and the boss shortlist; the five packs' `SOURCE.txt`; the registry rules; P139's
checklist (section 3 there) and P140's body and creature tables; `ClusterFLeagueSystem.cs` (membership flags only),
`ClusterFCreatureLevels.cs` (the level is pinned's Bard difficulty uncapped, 1 to 200), P179 and P280's notes, F-24 in
`docs/feature-queue.md`; `RequisitionSystem.HuntFamily`. Every candidate .vd was rendered (`validate-art.py render
--vd`, the stand frame) to a contact sheet before naming.

**Skipped on purpose:** the boss shortlist's bodies (skeleton king, daemonmaster, fire and frost giants, Andariel, the
beholder and mind flayer) are left for the dungeon boss prompts; the ettin and minotaur have stock kin already; the
goatman archer needs cc-P139's animating-bow trick and waits; the Tree Fellows are over the 5 MB rule; the four
Diablo 2 golems of the elemental pack stay out unless Chase clears them. A full list of what remains in each pack is
in the package `SOURCE.txt` section.

| New name (in game) | Source folder and name | Author | Body | Slot | Layout, type | Level | Home | Hunt use |
|---|---|---|---|---|---|---|---|---|
| a hedge snatcher | `uo-pixel-monsters\kalamarr_goatmangoblin_truppe\L_01.vd` (goblin troop) | Kalamarr | 2072 | 203 | low, ANIMAL | 20 | Haven Island hills (south-west and north) | culling pack |
| a snatcher outrider | `uo-pixel-monsters\kalamarr_goblinreiter\L_goblineiter.vd` (goblin rider) | Kalamarr | 2073 | 204 | low, ANIMAL | 32 | Haven Island southern hills | hunt target |
| a hornback raider | `uo-pixel-monsters\dvir_kalamarr_goatman\H_goatmanmace.vd` (goatman, mace) | Kalamarr | 2074 | 22 | high, MONSTER | 27 | Haven Island north hills | hunt target |
| a ditch crawler | `uo-pixel-monsters\vertigo_crawler\H_crawler.vd` (crawler) | Vertigo | 2075 | 23 | high, MONSTER | 13 | Haven Island gullies | culling pack |
| a mire croaker | `humanoids\Humanoid\Bullywog Spear.vd` (bullywog) | Vert-I-Go | 2076 | 24 | high, MONSTER | 31 | the great swamp south of Britain; the marsh west of Cove | hunt target |
| a brine lurker | `humanoids\Humanoid\Kuo-Toa.vd` (kuo-toa) | Vert-I-Go | 2077 | 25 | high, MONSTER | 39 | Covetous, the lake halls | culling pack |
| a moonmaw | `uo-pixel-monsters\es_werwolf\L_werwolf.vd` (werewolf) | EmuResource | 2078 | 205 | low, ANIMAL | 44 | the Yew woods | culling pack |
| a thornwisp | `uo-pixel-monsters\es_waldgeist\H_waldgeist.vd` (forest spirit) | EmuResource | 2079 | 26 | high, MONSTER | 57 | the Yew woods | culling pack |
| a pale drifter | `uo-pixel-monsters\dvir_kalamarr_shadow\H_shadow.vd` (shadow) | Kalamarr | 2080 | 27 | high, MONSTER | 38 | Deceit | culling pack |
| a slagheart | `uo-pixel-monsters\dvir_kalamarr_lavagolem\L_lavagolem.vd` (lava golem) | Kalamarr | 2081 | 206 | low, ANIMAL | 46 | the Fire dungeon | culling pack |
| a glasswarden | `uo-pixel-monsters\es_crystal_golem\H_crystal_golem.vd` (crystal golem) | EmuResource | 2082 | 28 | high, MONSTER | 51 | the Ice dungeon | culling pack |
| a tunnelmaw | `uo-pixel-monsters\dvir_kalamarr_umber_hulk\H_umber_hulk.vd` (umber hulk) | Kalamarr | 2083 | 29 | high, MONSTER | 54 | Shame | hunt target |
| The Siegebreaker | `uo-pixel-monsters\uodev_kriegstroll\H_kriegstroll.vd` (war troll) | uodev | 2084 | 30 | high, MONSTER | 78 | Covetous, the lower hall | mini-boss |
| The Hollow Oak | `plant-pack\Plant Pack\Treant.vd` (treant) | Thagoras | 2085 | 31 | high, MONSTER | 74 | the Yew woods, a clearing | mini-boss |

Levels are `ClusterFCreatureLevels.Level` on a fresh creature (random stats inside each range, so a point or two
either way), printed by fact 4 in the green cycle. SHA-256 and byte counts of every .vd: `registry.csv` and the
package `SOURCE.txt` (19,957,905 bytes in all; the largest, the forest spirit, 2.8 MB).

## 2. Part 1: the bodies (P139's route, once per file)

`propose` on the fourteen gave consecutive bodies from 2072 and the next free slot of each layout (22 up for the high
layout, 203 up for the low); `check-vd <body> --file 7 --slot S --type T --flags 0` said **free and matching** for all
fourteen against the 7.0.117.0 client (`D:\UO\UltimaOnlineVanilla`, the same version as the shard's client-data,
which this worktree does not carry). The Treant's note ("only actions 0-12: a monster, or an animal cut into a high
block") was read from the sprite: a tree that walks (0), stands (1), dies (2), strikes (4, 5) and is hit (10) is a
monster, so it stays MONSTER on a high slot. The crawler has no action 10 (get hit) and the goblins' low layout has
no fidgets: those moments show the stand frame, as P139 recorded for the kobold.

Registered: the .vd copies (`anim-src\bodies\2072.vd` to `2085.vd`), 14 `registry.csv` rows (623 rows now; both
`--check-registry`s read 0 problems), 14 `records.json` `bodyAnims` entries (38), a `SOURCE.txt` section with each
author, resource, terms and SHA-256, and 14 `ShardBodyTypes.Entries` (Animal for the four low-layout bodies, Monster
for the rest). `build-equip-anims.py` then `--check`: every block the .vd's bytes, every pixel identical; `sl-anim7.bin`
is 42,901,436 bytes in the git-ignored `build\` folder (P140's rule), rebuilt by the package build.

## 3. Part 1: the creatures, and Part 3: the lines

All in `server\customizations\Mobiles\Bestiary\`: `BestiaryParts.cs` (13 parts on `BestiaryPartBase`, stackable, a
stock graphic and hue each, named from the 7.0.117.0 tiledata: severed elf ears 0x312D, the dread horn's horn 0x315C
and 0x315D, a jaw bone 0x1B13, the slith tongue 0x5746, delicate scales 0x573A, hides 0x1078, a worldgem bit 0x1F13, a
bottle 0xF0E, a void core 0x5728, crystal shards 0x5738, a daemon claw 0x5721, a log 0x1BDD), `HavenHuntCreatures.cs`,
`CullingPackCreatures.cs`, `BestiaryMiniBosses.cs`. Every type is `[SerializationGenerator(0, false)]` with no saved
fields. Numbers are first proposals scaled from the nearest pinned creature, for Chase to tune:

| Creature | Base (pinned file) | AI, sound | Numbers | Special | Drops |
|---|---|---|---|---|---|
| Hedge Snatcher | our GreenGoblin cut to tier 1 | melee, 0x600 | Str 35-45 Dex 40-50 Int 15-25; hits 24-30; dmg 3-6; phys 10-15; skills 20-35; fame 400 | rummages corpses | 1 snatcher ears; Poor |
| Snatcher Outrider | Ratman up a step | melee, 0x600; ActiveSpeed 0.15 (mounted) | Str 60-75 Dex 70-85 Int 20-30; hits 50-65; dmg 5-9; phys 20-25; skills 30-60; fame 1200 | rummages | 2 snatcher ears; Meager |
| Hornback Raider | Orc (`Humanoid/Melee/Orc.cs`) | melee, 0x586 (satyr) | Str 70-85 Dex 50-65 Int 20-30; hits 40-52; dmg 4-8; phys 15-25; skills 25-50; fame 800 | rummages; meat 1 | 1 hornback horn; Meager |
| Ditch Crawler | GiantRat, Slime | melee, 0x388 (giant spider) | Str 25-35 Dex 25-35 Int 5-10; hits 16-22; dmg 2-5 (30% poison); poison 20-30; skills 10-25; fame 250 | lesser hit poison 20% | 1 crawler mandible; Poor |
| Mire Croaker | Lizardman cut down | melee, 0x266 (bullfrog) | Str 60-75 Dex 55-70 Int 20-30; hits 40-50; dmg 4-8; phys 15-20 poison 20-30; skills 25-55; fame 900 | swims; rummages; meat 1 | 1 croaker tongue; Meager |
| Brine Lurker | Lizardman up a step | melee, 417 (lizardman) | Str 85-100 Dex 70-85 Int 40-55; hits 55-70; dmg 6-10 (30% cold); phys 25-30 cold 30-40; skills 40-70; fame 1500 | swims; rummages | 1 lurker gills, 2 raw fish steaks; Meager |
| Moonmaw | DireWolf, Troll | melee, 0xE5 (dire wolf) | Str 100-120 Dex 90-110 Int 30-45; hits 70-85; dmg 8-13; phys 25-35; skills 45-80; fame 2500 | Bleed Attack; canine pack instinct; hides 10, meat 2 | 1 moonmaw pelt; Average |
| Thornwisp | Reaper cut down | mage, 466 (wisp) | Str 60-80 Dex 60-75 Int 80-100; hits 50-65; dmg 6-10 (50% poison); poison 50-60; Magery/EvalInt 45-60; fame 2500 | regular hit poison 40%; bleed immune | 1 thornwisp spark, 5 logs, 3 reagents; Meager + low scrolls |
| Pale Drifter | Shade as a melee creature | melee, 0x482 (shade) | Str 60-80 Dex 80-100 Int 40-60; hits 50-65; dmg 7-11 (60% cold); cold 50-60; skills 50-70; fame 3000 | lethal-poison immune; bleed immune | 1 drifter ectoplasm; Meager |
| Slagheart | Golem scaled down, our LavaElemental | melee, 268 (earth elemental) | Str 150-180 Dex 40-55 Int 30-45; hits 95-115; dmg 10-15 (60% fire); phys 40-50 fire 70-80 cold 0-5; skills 60-75; fame 4000 | lethal-poison and bleed immune | 1 slag core, 5 sulfurous ash; Average + gems |
| Glasswarden | CrystalElemental as a melee creature | melee, 278 (crystal elemental) | Str 140-170 Dex 50-65 Int 50-70; hits 95-115; dmg 10-15 (30% energy); phys 45-55 cold 60-70 poison 60-70; skills 65-85; fame 4500 | lethal-poison and bleed immune | 1 glasswarden shard; Average + gems |
| Tunnelmaw | Cyclops cut down | melee, 397 (scorpion) | Str 220-260 Dex 55-70 Int 25-40; hits 140-170; dmg 12-18; phys 45-55; skills 55-90; fame 5000 | Bleed Attack; meat 3 | 1 tunnelmaw claw; Average + gems |
| The Siegebreaker | Cyclops, Troll up a step | melee, 461 (troll) | Str 350-400 Dex 70-90 Int 40-60; hits 320-380; dmg 16-24; phys 50-60; skills 70-100; fame 9000 | Crushing Blow; cannot flee; meat 4 | 3 tusks, a gold jewel; Rich + Average + 2 gems |
| The Hollow Oak | Reaper grown into a boss | melee, 442 (reaper); ActiveSpeed 0.35 | Str 300-350 Dex 30-45 Int 60-80; hits 300-350; dmg 14-22 (20% poison); phys 50-60 **fire 5-15** poison 60-70; skills 70-90; fame 9000 | Paralyzing Blow; regular hit poison 30%; lethal-poison and bleed immune; cannot flee | 3 heartwood, a gold jewel, 20 logs; Rich + Average |

**The bestiary lines** (`ClusterFLeagueBestiary.Entries`; the System's line, then the plain line in parentheses as
achievements show theirs):

| Creature | The System says | (plain) |
|---|---|---|
| hedge snatcher | It steals from hedgerows and runs. The System respects the commitment. | A small goblin that raids the hills around New Haven in packs; drops snatcher ears. |
| snatcher outrider | A goblin that found a wolf willing to carry it. Nobody asked the wolf. | The hedge snatchers' mounted leader on Haven Island's southern hills; faster and tougher than its pack. |
| hornback raider | Half goat, half bandit, entirely convinced the hills are its. | A goat-headed raider of the hills north of New Haven; hits harder than it looks and drops a horn. |
| ditch crawler | A worm with ambitions and far too many legs. | A crawler of Haven Island's ditches and gullies; its bite is mildly venomous. |
| mire croaker | It croaks before it stabs. Consider that fair warning. | A frog-folk spear fisher of the swamps; it swims as well as it walks. |
| brine lurker | Something fishy with a spear. The System has heard all the jokes. | A fish-folk hunter of Covetous's flooded halls; its spear strikes cold and it swims. |
| moonmaw | Wolf by night, wolf by day, inconvenient at all hours. | A werewolf of the Yew woods that hunts in packs; its bite bleeds. |
| thornwisp | The forest's idea of a lantern. Do not follow it. | A forest spirit of the Yew woods; it casts, and its touch poisons. |
| pale drifter | A ghost that never learned to haunt properly, so it just drifts at you. | A pale shade of Deceit's halls; its touch is cold and no poison troubles it. |
| slagheart | A rock that is also a furnace. Neither was improved by the meeting. | A lava golem of the Fire dungeon; it burns to the touch and shrugs off poison and bleeding. |
| glasswarden | Beautiful, sharp and entirely humourless. | A crystal golem of the Ice dungeon; its shards strike with energy, and the cold does not slow it. |
| tunnelmaw | It chews through rock. Your armour is softer than rock. | A burrowing hulk of Shame's halls; its claws bleed and nothing out-digs it. |
| The Siegebreaker | A troll that took up siege work. The walls lost. | A war troll holding Covetous's lower hall; a mini-boss whose club crushes armour. Bring friends. |
| The Hollow Oak | An old tree with grievances. Many grievances. | An ancient treant of the Yew woods; a mini-boss, slow, grasping and poisonous, and it fears fire. |

The plain line names the source creature's kind in plain words ("a werewolf", "a lava golem", "a goblin") where the
word is generic English; the brand names (umber hulk, kuo-toa, bullywog, treant, waldgeist) appear nowhere in game,
and fact 4 refuses them in a creature's name.

How a player meets a line: `ClusterFLeagueBestiary.OnCreatureDeath` (`[OnEvent(CreatureDeathEvent)]`, as
`ClusterFAchievements.OnCreatureDeath`) takes `LastKiller` as a `PlayerMobile`, and `RecordKill` adds the type name to
the account's `EncounteredCreatures` (`ClusterFAccountData`, the set kept "on first kill" for hunting work orders
since the work-order system; nothing had written it, which `ClusterFDevTools` clearing it confirms) and sends the two
lines once. The hunting work orders that gate on `HasEncountered` are unchanged: they name stock types.

## 4. Part 2: the tables and the homes

**The tables.** `BestiaryEntry(Type, Name, Use, Home, Part, LevelFrom, LevelTo, Flavor, Plain)`; `BestiaryUse` is
HuntTarget, CullingPack or MiniBoss. `HuntTargets` = the targets and the mini-bosses (6: the outrider, the hornback
raider, the mire croaker, the tunnelmaw, the Siegebreaker, the Hollow Oak); `CullingPacks` = 8 (hedge snatchers, ditch
crawlers, brine lurkers, moonmaws, thornwisps, pale drifters, slaghearts, glasswardens). F-24's board reads these
(`Find(Type)`, `Find(BaseCreature)`); `RequisitionSystem.HuntFamily` is still the requisition seam and is untouched.

**The homes: 25 spawner rows, all Trammel**, placed by `[ClusterFSeedBestiary [dryrun]` (`CommandCategory.WorldSetup`,
`Rerun = Skips`, `Shard = TestFirst`; a row whose spawner stands within 3 tiles by its name `Bestiary: <label>` is
counted present). Stock `Spawner`, `HomeRange` set after the move so the bounds centre on the tile (P141's lesson).

| Home | Rows (tile, count, range, minutes) | How the tile was proven |
|---|---|---|
| Haven Island, south-west hills and woods | hedge snatchers 3430,2700 x3 r20 5-10; the outrider 3410,2745 x1 r15 10-15; ditch crawlers 3395,2690 x3 r12 4-8 and 3460,2725 x2 r12 4-8 | `check_walkability` on the 7.0.117.0 Trammel map: 7,011 of 7,200 tiles walkable in (3400,2680)-(3480,2770); the stock Outdoors spawner at 3450,2734 (r50) is the same hills. Clear of New Haven (3416-3545 x 2480-2648), Old Haven, the tutorial farm (3381-3399 x 2603-2619) and the Rootdeep hole (3619,2620) |
| Haven Island, north hills | hedge snatchers 3545,2395 x2 r15; hornback raiders 3570,2380 x2 r15 8-12 and 3640,2400 x2 r12 8-12 | the stock spawners at 3549,2409 (r40), 3483,2389 and 3690,2422 (r47) cover these hills; the coast north of them is water, which a spawner never picks |
| the great swamp south of Britain; the marsh west of Cove | mire croakers 1190,2885 x3 r15 8-12 and 2065,1000 x2 r12 8-12 | swamp land 0x3DC2-0x3DF0 at both tiles (`inspect_map_region`); stock swamp spawners at 1158,2872 (r130) and 2067,989 (r30) |
| Covetous, the lake | brine lurkers 5445,2030 x3 r12 5-10 and 5440,2023 x2 r10 5-10 | the stock WaterElemental spawner's tile (r15) and the spiders' (r15), `shared/trammel/Covetous.json` |
| Covetous, the lower hall | the Siegebreaker 5577,2006 x1 r8 30-45 | the stock HeadlessOne spawner's tile (r10) |
| the Yew woods | moonmaws 1059,1166 x3 r20 and 960,910 x2 r20 5-10; thornwisps 960,910 x2 r20 and 837,361 x2 r20 6-10; the Hollow Oak 1010,1250 x1 r10 30-45 | stock Outdoors spawners' tiles (Reaper, Corpser, Ettin mixes, r30); the clearing 980-1040 x 1220-1280 read 3,452 of 3,600 tiles walkable |
| Deceit | pale drifters 5170,678 x3 r10 and 5139,661 x2 r10 5-10 | the stock Shade/Wraith spawners' tiles (r10, r15) |
| the Fire dungeon | slaghearts 5699,1302 x2 r10 and 5859,1341 x2 r8 6-10 | the stock FireElemental spawners' tiles |
| the Ice dungeon | glasswardens 5731,176 x2 r12 and 5681,191 x2 r10 6-10 | the stock IceElemental spawners' tiles |
| Shame | tunnelmaws 5474,20 x1 r12 and 5649,101 x1 r10 10-15 | the stock EarthElemental spawners' tiles |

Nothing is placed by this prompt: the seeder runs on the test shard first (Chase, section 8), then live. Young players
are protected by pinned's own rule (an aggressive creature leaves a Young player alone until struck), so the island's
packs are safe to walk past and fair to fight.

## 5. For the overseer: deviations to register

- **D-P364-1 (ours, by design):** fourteen creatures that OSI never had, on third-party art renamed for the shard.
  Their stats are first proposals (section 3) scaled from the named pinned creatures, not OSI values: nothing to
  look up on a wiki, which `docs/fidelity-principle.md`'s "ours" column already covers for the Burrows bestiary.
- **F-24 note:** the hunt and culling tables are data only. F-24's build should read `ClusterFLeagueBestiary.Entries`
  (and could fold cc-P140's Burrows creatures in the same shape) rather than start a second list.
- **`EncounteredCreatures` has its first writer.** Hunting work orders gate on it (`HasEncountered(RequiredCreature)`,
  stock type names such as "Dragon"); this prompt writes only its own fourteen names there, so no order's gate moved.
  F-24 decides whether every first kill belongs in the set.

## 6. Facts, red then green

`server\tests\Mobiles\Bestiary\LeagueBestiaryVerification.cs`, five facts, run by the gated build (`docker\uo\build.sh`,
`-t sl-modernuo:cc-P364`, each cycle detached under the docker-build lock, taken 18:29 CDT; free memory 8.9 GB of 31.7
before cycle 1, 3.6 GB after cycle 2 with the WSL VM holding 13.8 GB of page cache, dropped to 4.9 GB with the
privileged-alpine `drop_caches` before cycle 3 (9.2 GB available then). Logs `build-P364-c1.log` to `-c3.log`,
`probe-P364-1.log` and `package-build-P364.log` in the session scratchpad.

| Cycle | Result |
|---|---|
| 1 (`--tests-only`) | compiled first time; **2,119 tests, 2,114 passed, 1 failed**: fact 2 made each part with `Activator.CreateInstance`, which the parts' optional-amount constructors defeat (the known host trap); `Loot.Construct` instead |
| probe (the five facts alone on `sl-uo-builder:cc-P364`, the fixed test bind-mounted, `--security-opt seccomp=unconfined`, 90 s) | 5 of 5 green; fact 4 printed the levels in the table of section 1 |
| **2, red** (`breaks.py apply`: eight breaks, `--tests-only`) | **2,119 tests, 2,110 passed, 5 failed: the five bestiary facts and nothing else.** Break by break below |
| **3, green** (`breaks.py restore`: byte copies, SHA-256 equal, no `P364-BREAK` left; the full build) | **2,119 tests, 2,115 passed, 4 skipped (the map-data facts, as always), 0 failed; image `sl-modernuo:cc-P364` = `0cdda879934f`** ("Built sl-modernuo:cc-P364 with patches applied and 2115 shard test(s) passing"); `latest` (`f53bfa00612d`) untouched |

The eight breaks and what each turned red (cycle 2's messages):

| Break (marker `P364-BREAK`) | Fact | Failure seen |
|---|---|---|
| body 2075 removed from `ShardBodyTypes.Entries` | 1 | `Assert.Equal() Failure: Values differ` (Empty, not Monster) |
| the Moonmaw's name made "a moonmaw!" | 1, 2 | `Strings differ` |
| the hedge snatcher's `PackItem(new SnatcherEars())` removed | 3 | `Assert.Single() Failure: The collection was empty` (no part on the corpse) |
| the Siegebreaker's tusks 3 to 1 | 3 | the amount (masked in the log by the earlier failure in the same fact) |
| the `[OnEvent]` hook removed | 3 | the first kill not recorded (same) |
| the glasswarden's band set to 5-30 | 4 | `Assert.InRange() Failure: Value not in range` (level 51) |
| the tunnelmaw named "an umber hulk" in the table | 4 | the brand-name check (same fact) |
| a spawner row's type changed to "Rat" | 5 | `Assert.NotNull() Failure: Value is null` (`Find` of a type outside the table) |

Facts 3 and 4 carry two or three breaks each; a fact stops at its first failing assertion, so one message per fact is
in the log and the later breaks in the same fact are proven only by the fact being red. The `[OnEvent]` break and the
tusk count are the two covered that way.

**Package tests** (`player-package\tests\Build-UoOverrides.Tests.ps1`, Windows PowerShell 5.1): **21 facts, 21 passed**
with the counts moved (623 registry rows, 38 body rows, 38 `bodyAnims`) and the new stock-body fact. The fact was
seen red twice while being written (a wrong CSV read gave "body rows: 0"; a stray carriage return gave "Illegal
characters in path"), then green; it is not a gate over the creatures, so no deliberate break was planted for it.
`scripts\tests\test_validate_art.py`: 23 tests, OK.

**Package build to scratch** (`Build-PlayerPackage.ps1 -Out <scratchpad>\pkg -UoData D:\UO\UltimaOnlineVanilla`, under
the package lock, with the shared `D:\UO\tazuo-sl-build\client`): it ran the paperdoll fit gate (2 gumps, 0 failures)
and the **animation encode gate ("anim7 matches")**, then the harness killed its shell for low system memory (the
13.8 GB page cache above), before staging and gates 1 to 6. **Not re-run**, as the harness and the standing rule say;
the command above is the one to run. The encode gate is the one the fourteen bodies touch, and the same encoder
`--check` passed by hand (section 2).

## 7. Decisions for Chase

- The numbers in section 3 (stats, loot, parts per kill) and the spawner counts and timers in section 4.
- The part graphics are stock placeholders with a hue each; swap any for art when you like (one line each in
  `BestiaryParts.cs`).
- The croakers' second home (the marsh west of Cove) and the Yew clearing are mine; move them if you have better spots.
- The Diablo 2 golems of the elemental pack (blood, dirt, fire, metal) are still out; say if the 2026-10-15 rip call
  covers them and a later batch can use them.

## 8. For Chase

1. Build and publish the player package from the console (Player package > Build, then Publish): the fourteen bodies
   ship in it; the launcher rebuilds `app\uo-overrides\` on the next start.
2. Rebuild the test shard from this commit (or deploy `sl-modernuo:cc-P364`), then as staff:
   `[ClusterFSeedBestiary dryrun` (says 25 would be placed), `[ClusterFSeedBestiary` (places them), and again (25
   present, 0 placed).
3. In a client, EYES: `[go 3430 2700` (hedge snatchers), `[go 3570 2380` (hornback raiders), `[go 5445 2030` on
   Trammel (brine lurkers), `[add TheSiegebreaker` somewhere safe: each body draws whole, walks, stands, attacks, is
   hit, dies and its corpse draws; the part is on the corpse; the first kill prints the two bestiary lines.
4. `[CreatureLevels` writes every creature's level to a file if you want the fourteen beside the stock ones.

## 9. Repo size rule

The fourteen .vd files are 19,957,905 bytes in all, the largest 2,792,832 (the forest spirit); none over 5 MB. The
encoded `build\sl-anim7.bin` (42.9 MB) is git-ignored (`.gitignore:100`, `git check-ignore -v` proves it) and rebuilt by
the package build's encode gate. No other file over 5 MB was added (`git status` in section 11).

## 10. Deviations in how the work was done

- **No League hunt or culling table existed** (F-24 unbuilt). The prompt's "add each to League hunt and culling
  tables" became "write the first ones" (`ClusterFLeagueBestiary`), as data F-24 reads, not a subsystem: no board, no
  job, no reward. Recorded as an assumption, not asked (the question answers itself from the code and the queue).
- **Bestiary lines have no display of their own**, so they show once on the first kill and live in the table; the
  prompt did not say where they appear. The write into `EncounteredCreatures` is the one side effect (section 5).
- **This worktree has no `client-data\`** (git-ignored, under `D:\ShatteredLegacy`, which is another desk). Every
  client-data check (`propose`, `check-vd`, both `--check-registry`s, `bodies --all` for the fixture, the package
  build's `-UoData`) ran against `D:\UO\UltimaOnlineVanilla`, a stock 7.0.117.0 install (`client.exe` file version
  7.0.117.0, the shard's version). The map and tiledata reads used the same folder through vseUOAware with explicit
  paths; the tool's saved folder points into `D:\ShatteredLegacy` and was not used.
- **The Read tool was denied on `docker\uo\build.sh`** (outside the primary working directory in an unattended run)
  and the Bash hook refuses any command naming it without the lock, so its options were taken from cc-P195 and
  cc-P266's notes (`-t <tag>`, `--tests-only`) rather than from the file. The build ran as those notes say.
- **Levels in the test host read without the poison-immunity bonus:** `BaseInstrument.IsPoisonImmune` is
  `bc.PoisonImmune != null`, and the host never runs `PoisonImpl.Configure`, so `Poison.Lethal` is null there and
  the four immune creatures (pale drifter, slagheart, glasswarden, the Hollow Oak) read 10 levels under their live
  value (fact 4's bands hold either way: 48, 56, 61 and 84 live). The table's levels are the host's; add 10 for those
  four on the shard.
- **The deliberate breaks ran as a full `--tests-only` cycle**, not a bind-mounted probe: the customizations' paths
  inside the builder image were not looked up, and a five-minute cycle costs less than a wrong mount.
- **Nothing ran against any world.** The spawners are placed by the staff command on the test shard first (section 8).
- Sounds are borrowed, as the prompt allows: goblins 0x600 (our GreenGoblin), satyr 0x586, giant spider 0x388,
  bullfrog 0x266, lizardman 417, dire wolf 0xE5, wisp 466, shade 0x482, earth elemental 268, crystal elemental 278,
  scorpion 397, troll 461, reaper 442.

## 11. Commit preflight

Not committed (the Golem commits after the DONE line). Both locks released (docker-build after cycle 3, package after
its build was killed). `git status` in `D:\UO\golems\Bronze\ShatteredLegacy` (`golem/Bronze/P364`):

```
 M CHANGELOG.md                                          2026.10.21.23: the fourteen creatures, the bestiary line, the staff command
 M VERSION
 M player-package/tests/Build-UoOverrides.Tests.ps1      counts 623 / 38 / 38; the stock-body fact
 M player-package/vendor/shattered-legacy-art/SOURCE.txt the batch-2 section (authors, terms, SHA-256)
 M player-package/vendor/shattered-legacy-art/records.json  14 bodyAnims
 M player-package/vendor/shattered-legacy-art/registry.csv  14 body rows
 M server/customizations/Mobiles/Evo/ShardBodyTypes.cs   14 entries
?? player-package/tests/fixtures/stock-bodies-7.0.117.0.txt   1,327 stock body numbers
?? player-package/vendor/shattered-legacy-art/anim-src/bodies/2072.vd .. 2085.vd   19,957,905 bytes, the largest 2,792,832
?? server/customizations/ClusterFLeagueBestiary.cs      the tables, the lines, the first-kill hook, the spawn data and seeder
?? server/customizations/Mobiles/Bestiary/              BestiaryParts.cs, HavenHuntCreatures.cs, CullingPackCreatures.cs, BestiaryMiniBosses.cs
?? server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs
```

`D:\UO\golems\Bronze\shard-migration`: this file only. No file over 5 MB in either tree; `docs\` untouched; nothing
under `build\` (git-ignored) is staged; no pinned patch. `D:\UO\third-party` was read, never built or run from; its
`SOURCE.txt` files are unchanged (no new clearing line was needed: the uo-pixel, humanoids and plant packs state no
terms and rips have been allowed since 2026-10-15).

Suggested commit subject: `CC task P364: League hunt bestiary, batch 2: fourteen renamed creatures on package bodies
2072-2085, the first League hunt and culling tables, bestiary lines on first kill, spawn data and seeder; stock-body
package check`.

P364 DONE
