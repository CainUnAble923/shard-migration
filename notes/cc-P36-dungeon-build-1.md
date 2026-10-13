# cc-P36: New Haven dungeon, build 1 (F1, the move to 7.0.117.0, the dungeon region, four resources)

Prompt: `D:\UO\cc-prompts\cc-P36-dungeon-build-1.md` (with its "Revisions 2026-10-06"). Builder in `D:\ShatteredLegacy`.
Engine: `d4531cd94b739613155225c234900de9f47d2c88` (`docker/uo/Dockerfile:3` and `D:\UO\ModernUO-pinned`, both checked).
Image: `sl-modernuo:cc-p36` (`latest` not moved). Nothing committed; nothing run against live.

How it started: Chase said "continue your queue" with the autopilot idle after P34's refused commit. I handed P36 over
by hand the way `cc-autopilot.ps1` does (moved the prompt from `queue\` to `cc-prompts\`, set `state.json` current P36,
one line in `autopilot.log`).

## Headlines

- **F1 was real.** A GM miner with stone mining on, rolling under 0.1, throws `IndexOutOfRangeException` in
  `Mining.GetResourceType` on every one of the eight post-Valorite ores (watched red: the stack ends in
  `Mining.GetResourceType`). Fixed as stock does it: each ore now has its own granite as `Types[1]`, and Masonry takes
  the granites at their metal's tier. Dawnstone has ore and granite from the start.
- **7.0.117.0 is on the test shard, not live.** The copy's hashes match EA's install file for file (35 map, statics,
  tiledata and multi files), and the diffs re-ran to P24's exact numbers (statics 338 / 1,149, land 2,300 / 3,285).
  The test shard logs `Automatically detected client version 7.0.117.0`, `Restricting client version to 7.0.117.0 or
  newer. Action to be taken: Kick`, and no TileMatrix or MultiData lines. The package's floor is 7.0.117.0, its gates
  pass, and it is **not published**.
- **The Burrows exist as a region**: Trammel 5136-5247 x 1128-1263, a `DungeonRegion` with no magical entry (five
  refusals, each with Chase's line) and at most 3 hostile creatures on one Young player.
- **Four starter resources**: Dawnstone (metal 18), Burrowhide (leather 105), Rootwood (wood 316), Gloomsilk (cosmetic
  cloth). All 45 / 5 / 85 and craft gate 45; bonuses half of Dull Copper and Spined; region-only harvest; out of every
  BOD, commission, work order and random pick (asserted against the tables).
- **F3 is done**: the wood range now runs to Rootwood, so the eight extended woods are wood at last (hue and name).
  **F4 is fixed**: the Hunter's Satchel no longer turns an unknown hide into plain leather.
- **Tests: 1,044 of 1,044 pass** in the final build; 19 new facts in 3 files, every one watched red (two red runs,
  below). Three existing facts changed their expected values because of what this task added; each is listed.
- **One thing I got wrong mid-task, fixed:** my red-run restore missed `ClusterFSmithCommissions.cs` (it was not in
  the green snapshot because I had not changed it on green), so the second red run had a leftover mutation. Caught by
  the commission fact going red when it should not have; restored from git and the tree re-checked file by file.

## Citations that moved since `7c9215d97` (re-verified at `d4531cd9`)

| Brief or P24 said | Now |
|---|---|
| `SpellHelper.cs:673-680` (CheckTravel asks both regions) | `:637-645`; the `message ??=` line is `:641` |
| `PlayerMobile.cs:4398-4403` (Young death teleport to Entrance) | `:4079-4081` |
| `Ore.cs:176-187` (smelt difficulty) | `:168-179` |
| `CraftItem.cs:80-83` (leather/hide pairs) | `:77-80` |
| `docker-compose.test.yml:41` (client data mount) | `:46` before my edit |
| `Setup.ps1:30` / `:56` | `:30` / `:56` before my edit; `:31` / `:57` after (one comment line added) |
| Unchanged | `Mining.cs:284-288` (`patches/Mining.cs`, identical to pinned but line 8), `HarvestSystem.cs:140, 147, 332-352`, `Region.cs:802`, `BaseRegion.cs:76-81`, `ClientVerification.cs:34, 120`, `NoTravelSpellsAllowedRegion.cs:23-27`, `DungeonRegion.cs` (33 lines) |

---

## Part A: F1, the latent crash in extended-ore mining

**Fact first, red.** `tests/Engines/Harvest/ExtendedOreStoneMiningVerification.cs` A1 drives the stone branch with a
constant RNG (roll 0.0 < 0.1) for a 100-Mining player with `StoneMining` and `ToggleMiningStone`, through the real
`Mining.GetResourceType`. Red run (ores back to one type): `System.IndexOutOfRangeException ... at
Server.Engines.Harvest.Mining.GetResourceType(...)`. That is the crash inside the harvest timer, reproduced.

**Fix, argued.** Two options were on the table:
- *Guard the lookup in our code.* `GetResourceType` lives in `patches/Mining.cs`, a full-file replacement whose only
  change from pinned is `partial` on line 8. A guard there grows a replacement (the thing cc-P38 moved away from for
  `CraftItem`), and the stone miner would silently get ore instead of stone.
- *Give each ore a granite.* That is what stock does for every colored ore (pinned `Mining.cs:115-187`: ore, granite,
  elemental), costs 8 lines a class, and needs no patch. **Chosen.**

So `ClusterFExtendedOres.cs` gains `PlatinumGranite` .. `CelestialGranite` (`BaseGranite`, hue and name from the
resource), each ore's `HarvestResource` takes `(ore, granite)` (`ClusterFMiningExtension.Ore`), each metal's
`CraftResourceInfo` lists its granite (so `GetFromType` knows it, as stock's metals list theirs), and
`ClusterFMiningExtension.ExtendMasonrySubResources` registers the nine new granites in Masonry at their metal's tier
(Platinum 112.5 .. Celestial 200, Dawnstone 45), appended after Valorite Granite. Stock puts each colored granite at its
ore's requirement (pinned `DefMasonry.cs:139-147`), so this follows it. **Deviation to register**: Masonry materials
that OSI does not have (they follow from the extended ores, which are already deviations).

**Not done:** the Compact Ore Satchel accepts only plain `Granite` (not stock's colored granites either), so I left the
new granites out of it too.

**Facts (green):** A1 each ore and Dawnstone yield their own granite on the stone branch (resource and hue checked);
A2 off the branch, and without stone mining, it is ore; A3 each granite maps to its metal and is a Masonry material at
the tier, in order after Valorite Granite. Red for A3: the Masonry registration disabled
(`ArgumentOutOfRangeException` reading the list past its end).

## Part B: Q-063, the server moves to 7.0.117.0 (test shard only)

1. **Copy.** `robocopy D:\UO\UltimaOnlineVanilla D:\ShatteredLegacy\client-data\classic-client-7.0.117.0 /E`: 517
   files, 2.555 GB, 23 folders, 0 failed. `client.exe` FileVersion `7, 0, 117, 0`. SHA-256 of all 35 `map*`,
   `statics*`, `staidx*`, `tiledata.mul`, `multi.*`, `MultiCollection.uop`, `Multimap.rle` match the source, 0
   mismatches. (`client-data\` is gitignored in the shard repo, AGENTS rule 6.)
2. **Diffs.** P24's `diff_statics.py` and `diff_land.py`, copied to `notes\cc-P36-tools\` with `NEW` pointed at the copy:
   statics changed blocks Felucca **338**, Trammel **1,149**, 0 on the other four; land Felucca **2,300**, Trammel
   **3,285**, 0 elsewhere. Exactly P24's numbers, so EA has not patched in between. Outputs `changed_*.json` beside
   them (the two `.npy` arrays, 5.3 MB together, deleted: regenerable).
   Then P24's `scan_coords.py` and `placements.py` against today's tree and today's lists: **3,167 literal coordinate
   candidates in 173 files, 0 in a changed block** on either facet (P24 had 2,855 pairs; the tree has grown since).
3. **Compose.** `docker/uo/docker-compose.test.yml:46` now mounts `${CLIENT_DATA_PATH_TEST:-${CLIENT_DATA_PATH}}`
   (unset, it falls back to live's folder, as before). `.env.example` documents `CLIENT_DATA_PATH_TEST`. **I did not
   edit `docker\uo\.env`**: it holds `CF_API_TOKEN`. To recreate the test container I passed the variable on the
   command line (`CLIENT_DATA_PATH_TEST=... docker compose -f docker/uo/docker-compose.test.yml up -d`). **Chase's one
   line**, in `D:\ShatteredLegacy\docker\uo\.env`:
   `CLIENT_DATA_PATH_TEST=D:/ShatteredLegacy/client-data/classic-client-7.0.117.0`
   Until it is there, a plain `Start-TestShard.ps1` puts the test shard back on the 114 folder.
4. **Config.** `server\uo\modernuo\Configuration-test\modernuo.json` (bind-mounted, not in git): added
   `"clientVerification.minRequired": "7.0.117.0"` after `kickDelay`. JSON re-parsed; a backup of the old file is in my
   scratchpad. Pinned reads it with `GetSetting` and never writes it back (`ClientVerification.cs:34`); staff are exempt
   (`:120`).
5. **Package.** `player-package\payload\app\Setup.ps1:31` `$minVersion = [version]'7.0.117.0'`, comment `:26-30`
   rewritten (114.x installs as well as 7.0.24.0; "ship this floor before the server enforces it"). `:57`'s message
   still reads right: "client is version 7.0.114.40, the server needs 7.0.117.0 or newer".
   - **P44's probe 6 could not be rerun as P44 ran it**: `D:\UO\cc-p44-work` (the fake patcher and its harness) is gone.
     What I ran instead, with HEAD's `Setup.ps1` (old) and mine (new), `-ProbeFolder` on folders holding the seven
     required file names and a **real** `client.exe`:

     | Folder | Old Setup | New Setup |
     |---|---|---|
     | 114.40 `client.exe` (from `client-data\classic-client`), no `UO.exe` | exit 0, accepted | exit 1: "Found Ultima Online, but it cannot be used: ... client is version 7.0.114.40, the server needs 7.0.117.0 or newer." then the install-by-hand help |
     | 117.0 `client.exe` (from the copy) | exit 0 | exit 0 |
     | 114.40 plus a `UO.exe` (a text file, standing in for EA's launcher) | not run | goes into P44's wait path ("EA's launcher is downloading ..."), tries to start `UO.exe`, which fails as a non-exe; then P44's "did not start" help, exit 1 |

     So the floor routes a 114 install into the wait-for-EA path, which P44 proved with its fake. One wording note for
     Chase: the wait path says "EA's launcher is downloading Ultima Online (about 1.8 GB)", which is P44's first-install
     estimate; a 114-to-117 patch is far smaller. Left as is (a message change, not this task's).
   - **Gates:** a scratch build (`ShatteredLegacy-2026.10.12.1902.zip`, 77 MB, 740 files, into my scratchpad, not
     `dist\`) passed gates 1-6; `-CheckZip` passed gates 4, 6 and 5; `-GateSelfTest` stopped at gate 1 as designed. In the
     zip `app/Setup.ps1` has 0 non-ASCII bytes and the 117 floor. `tests\Build-UoOverrides.Tests.ps1` 11/11,
     `Cliloc-Overrides.Tests.ps1` 10/10, `Launch-Settings.Tests.ps1` 20/20. Line endings unchanged (LF, as
     `.gitattributes` sets for this file).
6. **Test shard on the copy** (image `sl-modernuo:latest`, no rebuild): container recreated at 19:03:45; the mount reads
   `D:/ShatteredLegacy/client-data/classic-client-7.0.117.0 -> /var/lib/uo/client-data/classic-client`. Log
   (`notes\cc-P36-tools\test-shard-117-start.log`, colors stripped; **local only**: `*.log` is ignored, and the file names
   the protected staff accounts and the LAN address, which stay out of a public repo): `Automatically detected client version
   7.0.117.0`, `Restricting client version to 7.0.117.0 or newer. Action to be taken: Kick`, `Loading maps done`, no
   TileMatrix "not found", no MultiData lines. One WRN (`Command stats already registered`), which live's own log has
   too.
7. **Seeder dry run: not run, and why.** A world command needs a staff session in the client: the server console takes
   only save, shutdown and restart (pinned `Console/ConsoleCommands.cs`). In its place, the coordinate re-scan in step 2
   (0 of 3,167 in changed blocks) is the same check P24 1b.1 made. The in-game dry run is in Chase's checklist.
8. For Chase: T-050 to T-052 and the live order are below.

## Part C: the dungeon region

`server/customizations/Regions/OldHavenBurrowsRegion.cs` (new, 174 lines).

- **Shape:** `DungeonRegion`, Trammel, `Rectangle3D((5136,1128,MinZ), (5248,1264,MaxZ))`, so x 5136-5247 and y
  1128-1263 inclusive (`Rectangle3D.Contains` is end-exclusive). Re-checked: none of pinned `regions.json`'s 145
  Trammel regions overlaps it. `Entrance` 3619,2620,0, provisional (the map batch confirms it is walkable and its z).
  `GoLocation` the middle, also for the map batch.
- **Registered** in `Initialize`, after `RegionJsonSerializer.LoadRegions` and `World.Load` (`Main.cs:671-675`), every
  start; it saves nothing. **Priority 50** (`DefaultPriority`): Despise needs 51 to beat an overlapping static region of
  equal priority because pinned makes every region Dynamic and a tie falls to list order
  (`DespiseRevamped/Region.cs:44-55`). Nothing overlaps here, so no tie; the file says to raise it if one ever does.
- **Names for players** (proposals; the code says "the Burrows beneath Old Haven"): **"the Burrows"** (short, matches
  Burrowhide and the Burrow Mother) or **"the Rootdeep Warren"** (says what the place is made of).
- **Young limit:** `AllowHarmful(from, target)` refuses when the target is a Young `PlayerMobile`, `from` is a hostile
  creature (a `BaseCreature`, alive, not tamed, not a player's summon), `from` is not already attacking, and
  `MaxHostilesOnYoung` (3) already are. "Attacking" = an unexpired entry in the player's `Aggressors`
  (`AggressorInfo.Expired`, 2 minutes after the last harmful act) **whose creature still has the player as its
  `Combatant`**: the combatant test drops a creature that hit once and wandered off, which expiry alone would count for
  two minutes. The check runs in the *attacker's* region (`Mobile.CanBeHarmful`, `Mobile.cs:8367`), so it applies to
  creatures inside the Burrows. Creature AI acquires targets through `CanBeHarmful`, so a fourth one does not even pick
  the player, and the `Combatant` setter refuses it too (asserted).
- **Travel:** `CheckTravel` decides by where the travel ends (`newLocation`), because `SpellHelper.CheckTravel` asks the
  destination's region and the caster's region with the same type and location. Players: refused `RecallTo` (spell,
  scrolls, runebooks, Sacred Journey, which uses the same type) and `GateTo` ending inside; `TeleportTo` ending inside
  when the caster is outside (Teleport and Ninjitsu's Shadow Jump; teleporting *within* the Burrows is allowed);
  `Mark` and `GateFrom` inside. Allowed: `RecallFrom`, `TeleportFrom`, and anything ending outside. Staff exempt, as
  `NoTravelSpellsAllowedRegion.cs:26`. Messages are Chase's drafts as written (none too long to compile; T-055 checks
  them in the client).
- **Known edge, not handled:** the region is told `newLocation` but not its map. When it is asked as the *caster's*
  region about travel to another facet at the same coordinates (Felucca 5136-5247 x 1128-1263, the same void strip),
  it would treat that as "inside". Nobody can stand there, so I left it and wrote it in the code.

**Facts** (`tests/Regions/OldHavenBurrowsRegionVerification.cs`, 6): C1 the rectangle exactly (four corners in, one
past each edge out, Felucca not), entrance, no housing, re-`Initialize` adds nothing, not a saved type; C2 each of six
refusals with its exact message through `SpellHelper.CheckTravel` (recall in, gate in, teleport in from 6 tiles
outside, mark, gate cast inside, recall to a rune inside from inside); C3 seven allowed cases; C4 a GM is exempt from
all four refusals tried; C5 three Mongbats attacking a Young player inside: the fourth `CanBeHarmful` false and cannot
take the player as `Combatant`, one of the three still can; a non-Young player with three on them is not limited; a
tamed creature neither counts nor is limited; and outside the region the answer is exactly pinned's handler.

**Red runs:** run 1 (`build3-red.log`) with the region never registered: C1 red ("not the exact type"). Because an
unregistered region also fails C2 and C5 for the wrong reason, **run 2** (`build4-red2.log`) registered it and only
disabled the rule: C2 red at "recall in" (allowed, no message), C5 red at the fourth creature (`CanBeHarmful` true).
Ran green after.

A setup mistake of mine, for the record: the first green attempt built "attacking" by adding `AggressorInfo` by hand
and then re-pointed the same three creatures at the veteran, which moved them off the Young player. The fact now uses
pinned's own path (`Combatant = target`, which runs `DoHarmful`) and gives the veteran its own creatures.

## Part D: the four resources

### What changed, file by file (shard repo)

| File | Change |
|---|---|
| `customizations/ResourceInfo.cs` | `Dawnstone` (18) after Celestial, `BurrowhideLeather` (105) after Barbed, `Rootwood` (316) after Starwood; their `CraftAttributeInfo`; info entries at index 17, 4 (both leather arrays) and 15; the granite type on the eight post-Valorite entries; **ranges** metal `<= Dawnstone`, leather `<= BurrowhideLeather`, **wood `<= Rootwood` (F3, was `<= Frostwood`)** |
| `customizations/ClusterFStarterResources.cs` (new) | `DawnstoneOre/Ingot/Granite`, `BurrowhideHides` (scissors to leather, as `BarbedHides`) and `BurrowhideLeather`, `RootwoodLog` (cuts to boards at 45, as `OakLog` at 65) and `RootwoodBoard`, `GloomsilkCloth : Cloth` (fixed hue, own name) |
| `customizations/Engines/Harvest/BurrowsRegionHarvest.cs` (new) | `MutateResource` overrides in our `partial Mining` and `partial Lumberjacking`: in the Burrows, a vein of the region's own (ChanceToFallback 0.5, fallback iron or plain log) rolled by pinned's `MutateResource`; outside, `base` with the bank's vein |
| `customizations/Engines/Craft/BurrowhideTailoringRegistration.cs` (new) | Tailoring `AddSubRes(BurrowhideLeather, "Burrowhide", 45, 1044462, 1049311)` at ServerStarted |
| `customizations/ClusterFMiningExtension.cs` | Blacksmithy and Tinkering Dawnstone at 45 (appended; Tinkering on its own guard); granites as `Types[1]`; Masonry granites |
| `customizations/ClusterFLumberjackingExtension.cs` | Carpentry (board) and Fletching (log) Rootwood at 45, appended; `RootwoodLog` in the logbook's non-gated discovery keys |
| `customizations/ClusterFMetalTiers.cs` | `Dawnstone = 45`, `RequiredSkill(Dawnstone) = 45`, new `IsPostValorite`; `GainCeiling` 0 (stated in its doc) |
| `customizations/ClusterFWoodTiers.cs` | `Rootwood = 45`, `RequiredSkill(Rootwood) = 45`; `GainCeiling` 0, so it is **out of the P67 gain chain** |
| `customizations/CompactOreSatchel.cs` | accepts `DawnstoneOre`, `DawnstoneIngot` |
| `customizations/CompactOreSatchelRoutingHook.cs` | Dawnstone logged in the Prospector's Logbook; **excluded from the Ore Bingo count** (`BingoCount`); no "unlock work orders" line for it |
| `customizations/ProspectorsLogbookGump.cs`, `SurveyArchivistGump.cs` | Dawnstone shown first; Archivist pays it (25, 1, 250), half of Dull Copper (without a row an unknown key pays Dull Copper's rate) |
| `customizations/ClusterFCompactAdminTools.cs` | `[CompactSeedDiscoveries` seeds Dawnstone too |
| `customizations/SeasonedLumberSatchel.cs` | Rootwood log to board |
| `customizations/ForestersLogbookGump.cs` | Rootwood listed with the known timbers (not gated, no reward) |
| `customizations/HuntersSatchel.cs` | **F4**: Burrowhide to Burrowhide leather; plain `Hides` to `Leather` named explicitly; an unknown hide returns null and is stored as hides |
| `customizations/SmithGuildSalvageBag.cs` | Dawnstone resmelts at 45 (the default was "0, no check"), pays Iron's 1 seal |
| `customizations/Services/PointsSystems/CleanUpBritanniaData.cs` | gear in Dawnstone, Burrowhide or Rootwood pays 0 (below) |
| `customizations/TestCenter/TestCenterKitEntries.cs` | the seven new stackables in the Test Kit |
| `patches/CraftItem-shard-hooks.patch` | two lines in its existing first hunk: `[RootwoodLog, RootwoodBoard]` and `[BurrowhideLeather, BurrowhideHides]`; every later hunk's new-file start moved by 3. Dry-run with `patch -p1 --fuzz=0` against pinned's `CraftItem.cs` before the build; applied clean in all five builds |

### Why the one patch edit

Pinned's equivalence table (`CraftItem.m_TypesTable`, `CraftItem.cs:64-90`) is `private static readonly`, built once;
the extended woods' eight pairs already live in this patch's first hunk for that reason
(`ClusterFLumberjackingExtension.cs` says so at its ServerStarted handler). Alternatives: reflection into an initonly
field (does not work on .NET 10, as that note records); leaving the pairs out (Fletching in Rootwood would refuse boards
and Tailoring in Burrowhide would refuse hides, unlike every stock tier). So: an existing patch, an existing hunk, two
lines. **No new patch file.**

### The audit the revisions asked for (every switch and range on `CraftResource` / `BulkMaterialType`)

A read-only sweep of `server\customizations\` and `server\patches\` (64 files read in detail; 124 more under `Items\`
and `Mobiles\` are `DefaultResource` assignments only). **No unbounded `> Valorite` or `>= Platinum` comparison on
`CraftResource` exists**; every range has an upper bound, so none captures Dawnstone. The only unbounded test is
`ClusterFSmithBODSystem.IsPostValorite(BulkMaterialType) => (int)mat >= 12` (`:418`), safe because `BulkMaterialType`
gains nothing.

| Place | Dawnstone / Burrowhide / Rootwood | Why |
|---|---|---|
| Mining tier gate (`ClusterFMiningExtension` veins) | **out**; harvested only in the region | region-only harvest |
| Smelt tier (`Ore-smelt-at-forge.patch`, `_ when RequiredSkill > 99`) | Dawnstone falls to pinned's default **50** | 45 is not > 99, so the post-Valorite branch never takes it. At Mining 45 the smelt chance is (45-25)/50 = 40%; stock's pattern (difficulty = harvest requirement) would give 45 and 50%. **Left at 50 to avoid a patch edit; reachable at 45, as the brief asks.** Register as part of the starter numbers |
| Gain ceilings (`CeilingFor`, `GainCeiling`) | **0** for both: they teach as stock metals and OSI woods do | asserted (D3) |
| "Orders that still teach" (`ClusterFSmithTeaching`) | out | reads `BulkMaterialType` only |
| Seal and deed values, deed metal names (`ShardClilocs.PostValoriteMaterial`, `SmithGuildBook.BodMatName`) | out | `BulkMaterialType` only |
| Salvage bag | **joins**: resmelt 45, seal 1 | its default was "no check" |
| Satchel tiers (`TierMetal`) | unaffected | |
| Hammer familiarity (`HammerMetal.All`, 17 rows) | **out**: `InferResource` gives -1, no familiarity | adding a row would change the gump and `HammerFamiliarityPaceVerification` |
| Clean Up Britannia | **out**: 0 for gear (and their materials are not turn-ins) | the default 0.1 let free dungeon ore out-earn its materials: `CleanUpBritanniaPointsVerification`'s invariant went red in build 1 on 354 piece-material pairs (290 Dawnstone, 64 Rootwood; counted from the EXCESS lines in `build1.log`). That was the red for this line |
| Discovery logs | **join** (Prospector's, Forester's) | out of Ore Bingo and of rare-wood reports |
| BODs, commissions, work orders, random picks | **out** | asserted against the tables (D8) |
| League ladder (`ClusterFLeagueRanks`) | already excluded "Dawnstone" by name, written ahead of this task | once `GetType` says Metal, its exclusion keeps the ladder at 17 (`LeagueLadderVerification` passes) |
| CompactAdminTools `[CompactOreInfo`, StaffHub resource loops | out (bounded Platinum..Celestial, Ironwood..Starwood) | |

**Two things that look like leaks and are stock behavior, left alone:**
- An **iron** (material None) smith BOD accepts an item in any metal: pinned `SmallBOD.EndCombine` rejects only when
  the deed names a colored material. A Dull Copper piece fills an iron order today; a Dawnstone one will too. Burrowhide
  likewise fills a plain-leather tailor order.
- Work orders ask for `typeof(Board)`, `typeof(Cloth)` and count subclasses, so a Rootwood board or Gloomsilk cloth
  counts as a board or cloth, as Oak boards already do. `BurrowhideLeather` is a `BaseLeather`, not a `Leather`, so it
  does **not** count for a Leather order (as Spined does not).

### Numbers (all deviations)

| Resource | Harvest | Craft gate | Bonuses | Hue now (first candidate) |
|---|---|---|---|---|
| Dawnstone | Mining 45 / 5 / 85, Burrows only | Blacksmithy, Tinkering 45; Masonry (granite) 45 | armour phys 3, durability 25, lower req 10; weapon durability 50, lower req 25; no runic numbers | 0x0A5B |
| Burrowhide | carved later (`OnCarve`, not a `HideType`) | Tailoring 45 | phys 2, luck 20 | 0x071D |
| Rootwood | Lumberjacking 45 / 5 / 85, Burrows only; logs cut to boards at 45 | Carpentry, Fletching 45 | none (cosmetic, item 12) | 0x0745 |
| Gloomsilk | spider drop later | any cloth recipe, not selectable | none (cosmetic, item 8) | 0x02C9 |

**No bolt for Gloomsilk:** `BoltOfCloth.Scissor` is not virtual and always makes plain `Cloth`, so a Gloomsilk bolt
would cut into ordinary cloth unless it re-implemented `IScissorable`. Not worth it for a drop that is cloth already.

### F3: the extended woods, before and after

- **Before** (wood range ending at Frostwood): `CraftResources.GetType(Ironwood .. Starwood)` is `None`, so
  `GetInfo` is null. Seen in red run 1: the wood fact died with a `NullReferenceException` reading `GetInfo(Ironwood)`.
  So `GetHue` is 0 (logs and boards undyed: `Log`'s constructor sets `Hue = GetHue(resource)`) and `GetName` is "" (no
  name line).
- **After:** each is `Wood`, its log and board carry its table hue (Ironwood 0x0966, Ghostwood 0x047E, Emberbark 0x0058,
  Frostbark 0x076E, Shadowbark 0x0544, Runewood 0x0060, Voidwood 0x022E, Starwood 0x04EC) and its name. Asserted (D2).
- **Collisions already in the table, not mine:** Ironwood 0x0966 is Shadow Iron's hue; Obsidian 0x0455 is Black
  Scales'; Barbed (AOS) 0x0851 is Green Scales'. Before F3 nobody could see Ironwood's. Worth a look in T-053.
- **The client check (T-053) is still Chase's**, per decisions item 7. I widened the range first because the brief
  orders it and the server side is proven; rolling back is the one line in `ResourceInfo.cs`.

### Hue candidates (T-054)

Chosen by `notes\cc-P36-tools\hue_pick.py`: nearest hues in the 117 `hues.mul` to a target colour by mid-ramp RGB,
skipping the 45 resource hues in `ResourceInfo.cs` and the two either side of each (the used list is printed by the
script).

| Resource (target) | Candidates |
|---|---|
| Dawnstone (pale rose-gold) | **0x0A5B** rgb(189,156,131), 0x0AA0 (189,180,164), 0x0A5C (189,180,131) |
| Burrowhide (earthy grey-brown) | **0x071D** "Neutrals #20" (123,98,74), 0x097D "Metals #28", 0x02E8 |
| Rootwood (dark red-brown) | **0x0745** "Neutrals #60" (115,65,41), 0x0471, 0x05F6 "Oranges #25" |
| Gloomsilk (dusky violet-grey) | **0x02C9** (90,65,106), 0x06E3 "GargoyleSkinHue #09", 0x04E2 "Pinks #49" |

### Facts (`tests/Items/StarterResourcesVerification.cs`, 10)

D1 appended values, all 43 old values by name and number, each new one's type, index, info, name and hue, and
`GetFromType` for all seven new item types; D2 F3 (above), plus every metal, leather and scale keeps its type and the
values just past each range stay `None`; D3 `IsPostValorite` false for Dawnstone (true for Platinum and Celestial),
`RequiredSkill` 45 for both, every ceiling 0; D4 two facts, a 45 miner in the Burrows gets Dawnstone on a roll that
does not fall back and iron at 44.9 on every roll, outside the bank's own vein (Valorite) is unchanged, and the same
for Rootwood against Oak; D5 all 16 new item types round-trip (amounts 7 to 29, hue and resource kept); D6
`ConsumeRes` succeeds at 45 and fails at 44.9 with the sub-resource's own message in Blacksmithy (Dagger), Tinkering
(Scissors), Tailoring (LeatherCap), Carpentry (Stool), Fletching (Bow) and Masonry (StoneChair), and each new
material is last in its list; D7 the bonuses on a real piece (PlateChest, Longsword, LeatherChest) against iron and
plain leather, and Dawnstone is at most half of Dull Copper with no runic numbers; D8 `BulkMaterialType` has no new
name and `SmallBOD.GetMaterial` maps all three to None; the commission picker run at every tenth from 0 to 200 at
rolls 0, 0.69 and 0.99, and with bypass, never returns Dawnstone; no requirement of any of the registered work orders
is a new type; the only random picks in pinned (`ColoredAnvil.cs:15`, `GlovesOfMining.cs:111`) draw Dull Copper ..
Valorite; D9 F4.

**Red run 1** (`build3-red.log`, 16 mutations, 16 facts red, 1,028 passed): D1 "Expected Metal, Actual None"
(ranges back); D2 the `NullReferenceException` above; D3 45 missing; D4 both: Dawnstone/Rootwood never given (overrides
off); D5 hue 0 on the round-tripped items (ranges back: **D5 has no red of its own**; a round-trip fact cannot be
broken without breaking the source generator, so its red is the range mutation's); D6 Burrowhide not in Tailoring
(`Assert.NotNull` on the sub-resource); D7 Dawnstone phys 0; D8 Dawnstone injected as the under-65 commission metal
("Found: Dawnstone"); D9 the satchel's Burrowhide line removed (null instead of leather); CUB invariant red on Dawnstone
gear. Restored from a hashed snapshot, all 32 files identical, plus `ClusterFSmithCommissions.cs` from git (the miss
in Headlines). Green after: final build 1,044 / 1,044.

### Existing facts whose expectations I changed (each because of what this task adds)

- `tests/Misc/TestCenterVerification.cs` `EveryShatteredLegacyKitEntryMakesAStackOfItsAmount`: 32 entries to **39**
  (the seven new stackables).
- `tests/Engines/Craft/CraftCategoryPagingVerification.cs` `EverySystemsMaterialAndScaleNamesAreTitleCaseStrings`:
  "ours are still last" now checks Celestial and Starwood second to last, Dawnstone and Rootwood last.
- `CleanUpBritanniaPointsVerification` was **not** changed: the code was (the 0 rate), and the fact passes unchanged.

### ASCII

Every file I touched is ASCII now. Eight of them already held non-ASCII (box-drawing rules and em dashes, 7,359 bytes,
almost all in comments): converted to `-`, `->`, `<->`, `~`, `*`. **Six of the changed strings are ones players see**:
two Lumberjacking discovery messages ("... properly process it - you don't ...", "unusual timber - Ironwood"), three
Prospector's Logbook labels, and its "gp -> Bank" total; five more are console warnings. No fact asserts any of them.

## Patch notes

`CHANGELOG.md`: new section **2026.10.12.5** (2026.10.12.4 is committed and pushed), `VERSION` bumped. Added: the
Burrows on the test shard, no magical entry, the Young limit, the four materials. Changed: the 117 floor in Play
Shattered Legacy, the extended woods' look. Fixed: GM stone mining on post-Valorite veins, the Hunter's Satchel. No
Staff lines. The wiki page is not published.

## Not verified

- Anything in a client: T-050 to T-056.
- The seeder dry run in game (Part B.7); the offline coordinate re-scan stands in for it.
- P44's probe 6 with its fake patcher (the harness is gone); see the table in Part B.5.
- Harvesting in the Burrows in a client: the area is void land with no mineable or choppable tiles until the map
  batch. The rule is proven only by facts.
- Whether `GoLocation` (5191,1195) and the entrance's z are right: both are the map batch's.
- The cc-p36 image has not run as a shard; the test shard runs `latest` on the 117 data.

## Proposed register rows

**bug-list**
- **F1** (ours, fixed in cc-P36): post-Valorite ores had one harvest type, so pinned's stone-mining roll
  (`Mining.GetResourceType`, `Types[1]`) threw `IndexOutOfRangeException` in the harvest timer for a GM miner with stone
  mining on, 10% of digs on those veins. Proved by `ExtendedOreStoneMiningVerification` A1 red. Fixed by a granite per
  ore, as stock.
- **F3** (ours, fixed in cc-P36, client look still T-053): `CraftResources.GetType`'s wood range stopped at Frostwood,
  so Ironwood .. Starwood had no info, no hue and no name. Proved by `StarterResourcesVerification` D2 red.
- **F4** (ours, fixed in cc-P36): `HuntersSatchel.ConvertHidesToLeather` turned any unknown hide into plain Leather,
  losing its resource. Proved by D9 red.

**deviations (`docs/fidelity-principle.md`)**
- The Burrows: at most **3** hostile creatures attack one Young player at once (`OldHavenBurrowsRegion.MaxHostilesOnYoung`;
  stock dungeons have no limit). Reverses by setting it out of the region's `AllowHarmful`.
- The Burrows: **no magical entry**; recall, gate and teleport in, mark and gate out refused for players, each with its
  own message (the five lines in `OldHavenBurrowsRegion.cs`); recall out allowed. Stock Trammel dungeons allow all.
- **Starter resources**: Dawnstone, Burrowhide, Rootwood, Gloomsilk; harvest 45 / 5 / 85, craft 45, bonuses half of
  Dull Copper / Spined, Dawnstone smelts at 50 (pinned's default for an unlisted ore, 40% at Mining 45).
- **Region-only harvest**: Dawnstone and Rootwood come only from the Burrows (`BurrowsRegionHarvest.cs`); OSI has no
  region-bound ore or wood.
- **Masonry granites for the post-Valorite metals and Dawnstone**, at the metal's tier.
- **Client floor 7.0.117.0** (`Setup.ps1` and, at the live step, `clientVerification.minRequired`).

## For Chase

**Deploy and commit, in this order:**

1. Commit with `Commit-ShardWork.ps1` (the autopilot does it on P36 DONE).
2. Add to `D:\ShatteredLegacy\docker\uo\.env`: `CLIENT_DATA_PATH_TEST=D:/ShatteredLegacy/client-data/classic-client-7.0.117.0`.
   Without it the next `Start-TestShard.ps1` goes back to the 114 data.
3. To try Parts A, C and D in game, put the test shard on `sl-modernuo:cc-p36` your usual way. Part B's checks need only
   the 117 data, which the test shard already runs.
4. Live, at a restart you already plan, in this order: build and publish the package (it carries the 117 floor); then
   point live's `CLIENT_DATA_PATH` at the 117 folder, add `"clientVerification.minRequired": "7.0.117.0"` to
   `server\uo\modernuo\Configuration\modernuo.json`, restart, and look for the same three log lines
   (`Automatically detected client version 7.0.117.0`, `Restricting ... 7.0.117.0 or newer`, no TileMatrix or
   MultiData errors).
5. To undo the live step: `CLIENT_DATA_PATH` back to `classic-client`, remove the `minRequired` line, restart. No save
   migration either way. (A package with the 117 floor stays out there; players already on 117 are unaffected.)

**In-game checks (in the client):**

- Archers' Guild wing, test shard, a player account: walk x 760-790, y 2128-2160 on Felucca and Trammel; floors walkable, walls solid (T-050).
- 117 client on test, a player account: log in and stay a minute; no kick at 20 seconds (T-051).
- Package on a 114 install: Play says the client is 7.0.114.x and the server needs 7.0.117.0, and waits for EA's update (T-052).
- Seeder dry run, test shard as GM: `[ClusterFSeedNewHaven dryrun`; reports nothing to move.
- Extended woods: `[add IronwoodLog` and `[add IronwoodBoard` (and the other seven) on live, then on test on cc-p36; before undyed and unnamed, after colored and named (T-053).
- Hues: `[add DawnstoneIngot`, `BurrowhideLeather`, `RootwoodBoard`, `GloomsilkCloth`, try the candidates with `[props`; name one per resource (T-054).
- Travel messages: a rune marked inside by a GM, recalled and gated to by a player; a player inside casting Mark, Gate and Recall out; each says Chase's line, recall out works (T-055).
- Young warning: a Young player moved inside the Burrows gets the dungeon warning gump (T-056).

**Decisions for Chase:**

1. The player-facing name: "the Burrows" or "the Rootdeep Warren" (or keep the working name).
2. Hues, by T-054.
3. Dawnstone smelts at 50 (40% at Mining 45, no patch). Say if you want stock's pattern (45, 50% at 45), which is one
   line in `Ore-smelt-at-forge.patch`.
4. The wait-for-EA message says "about 1.8 GB" also when a 114 install only needs the 117 patch. Reword later if it
   matters.

P36 DONE
