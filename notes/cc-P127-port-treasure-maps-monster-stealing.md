# cc-P127: Port list, Treasure maps revamp and Monster stealing

2026-10-16. Prompt: `cc-prompts/cc-P127-port-treasure-maps-monster-stealing.md`. Both repos were clean at the start (the
bot's `testing/bot-runs/2026-10-16-0130/` and the importer's two files are machine output). Not committed: the Golem
commits after DONE.

## Headlines

- **Both systems are in, whole, on the revamp's rules (Endless Journey is on, so ServUO's "new system" branches are the
  ones that run).** Treasure maps: five levels (Stash to Trove), five packages, seven facets, maps dropped by creatures on
  every facet for that facet, random valid chest spots, Cartography for decoding and the dig range, a rusty, standard
  or gold chest by Cartography, ServUO's loot (`TreasureMapInfo.Fill`), the trap that must be removed before the chest
  opens, ancient chest guardians on a failed Remove Trap, the grubber on a failed lockpick, the 30-day reset, and
  Unlock's new Magery rule. Monster stealing: a special item once per creature from Stealing 100 in a Felucca dungeon or
  a champion spawn, and all eleven thief items (balms, lotions, the seed, the draught, the gem, the lantern, the tool box).
- **Pinned's `TreasureMap` and `TreasureMapChest` are now routed replacements** (`server/patches/`): the diff against
  ServUO is the whole of each file, every pinned caller still compiles unchanged (the classic-level constructor,
  `LootChance`, the static classic `Fill` the camps and the SOS chest use, `Artifacts`), and saved maps and chests carry
  over through a version bump each (`TreasureMap` v0 to v1, `TreasureMapChest` v4 to v5): an old map's level is
  converted and it gets a package, as ServUO's own Deserialize does.
- **Five small patches** reach the pinned files that have no hook: Stealing (ServUO's five-line call), LockPick,
  Unlock, RemoveTrap (the timed disarm) and BaseCreature (maps on every facet). Alternatives argued below.
- **Where the port met the shard's rules:** Stealing's gain. ServUO's handler rolls no skill check, so monster stealing
  gave no gain at all; the shard's rule (on by default, `clusterf.stealing.monsterGain`) rolls a gain-only Stealing check
  on (100, 100 + 2.5 x the creature's fame level) after each attempt, so a 30,000-fame creature trains to 200: the
  skills design's "Stealing trains against the target's level" with ServUO's own fame-to-level line standing in for F-14
  until creature levels exist. Cartography: the revamp's decode roll is (min - 10, min + 30) by level, so a Trove (min
  91) gains to 121; the shard's path past that is not this prompt's.
- **Left out, counted:** 23 loot-table types and 14 spawn-table creatures that neither pinned nor ours has (lists
  below), reforging and refinement (D-38's precedent), the Smuggler's Edge path, the Exodus zealot's ritual items.
- Tests: 20 new facts (8 treasure, 10 stealing, plus the Clean Up Britannia points fact rewritten), 19 of 20 seen red in two
  deliberate breaks and the one that stayed green then broken on its own; shard tests **1,320 of 1,320**, full upstream
  suites unfiltered **Server.Tests 893, UOContent.Tests 2,416, no failure**; the test world boots, saves and reboots on
  the image with its old maps carried over. Port list: Treasure maps **0 / 2 -> 2 / 2**, Monster stealing
  **0 / 14 -> 14 / 14**; all systems 340 / 983 -> **356 / 983** (progress.py).
- **P142 (queued since this prompt started) layers the shard's monster-stealing rules on this port.** Its decision 5 is
  the gain rule built here (`StealingHandler.RollShardGain`, setting `clusterf.stealing.monsterGain`); the rest of its
  decisions (every facet's dungeons by Den rank, the curve to 200, one success per creature, the lower tier, new loot)
  replace `HandleSteal`'s OSI rules from the outside and should start from `StealingHandler.cs`'s three public helpers.

## What was ported

### Treasure maps (ServUO `Scripts/Services/TreasureMaps/` -> ours)

| ServUO | Ours | What |
|---|---|---|
| `TreasureMapInfo.cs` (992) | `server/customizations/Services/TreasureMaps/TreasureMapInfo.cs` | the four enums, ConvertLevel, GetFacet and IsEodon (ServUO's `SpellHelper.IsEodon`, absent in pinned), every table and getter, `Fill`, and the lock-and-trap table pulled out as `GetLockAndTrap` so a fact can read it |
| `BagOfGems.cs` (32) | `.../TreasureMaps/BagOfGems.cs` | the gem bag |
| `TreasureMap.cs` (1,786) | `server/patches/TreasureMap.cs`, replacing `Projects/UOContent/Items/Maps/TreasureMap.cs` | the map: `[SerializationGenerator(1)]`, fields 0-5 pinned's, 6 Package, 7 NextReset, `MigrateFrom(V0Content)`; the constructors (below); the facet tables and rectangles; `GetRandomLocation`, `ValidateLocation`, `AdjustMap`; `AssignChestQuality`; decode, dig target and timer (Cartography range and casting allowed while digging in the revamp); `OnDug`, the completion the dig timer and the pack mule share; `ResetLocation` and the reset timer after a load; the revamp's name property and facet lines |
| `TreasureMapChest.cs` (1,014) | `server/patches/TreasureMapChest.cs`, replacing `Projects/UOContent/Items/Containers/TreasureMapChest.cs` | the chest: `[SerializationGenerator(5)]`, fields 0-5 pinned's, 6 FailedLockpick, 7 Quality, 8 DigTime, 9 AncientGuardians, 10 FirstOpenedByOwner, 11 TreasureMap, `MigrateFrom(V4Content)` (and pinned's V2, V3 and v0/v1 readers kept); `ChestQuality` with its art; `CanOpen` and `CheckLocked`; `SpawnAncientGuardian`; the grubber in `LockPick`; `ExecuteTrap`; `DisplayTo`'s first-open hook; `ImbuingIngreds`; `GetRandomRecipe`; pinned's classic `Fill`, `Artifacts`, lifted-item rules and remove gump unchanged |
| `TreasureMapProtection.cs` (75) | nothing | pinned already has it (`Misc/TreasureMapProtection.cs`, `TreasureRegion`) |

**The constructors, and why the classic level is the one pinned callers pass.** Pinned's `TreasureMap(int level, Map
map)` is called by `BaseCreature.OnBeforeDeath`, `ParagonChest`, `Fishing`, two quests, four camps' chests, `TestCenter`,
our `LootBoxRoller` and the mule, all with the classic 0-7 level. ServUO converts that level at the creature
(`TreasureMapInfo.ConvertLevel` in `BaseCreature.cs:5876`) and in `ParagonChest`, so its constructor takes a revamp
level. Ours converts inside the int constructor instead, so every one of those callers keeps ServUO's result without a
patch; the revamp-level constructor is `TreasureMap(TreasureLevel, Map, bool eodon)`, which `Fill` uses for the map a
chest sometimes holds. The one visible difference is staff: `[add TreasureMap 3 Trammel` is a Supply map here (classic
3) where ServUO would make a Hoard. Decision 1 below.

**The chest's two ways of being made.** Pinned's chest fills itself in the constructor; ServUO's is filled later, by the
dig, from the map. Ours: a chest made temporary (the dig, the mule) is empty until `TreasureMap.OnDug` assigns its
quality, fills it from the map and raises the spawns; any other chest (`[add TreasureMapChest 3`, the camps, pinned's
own lift tests) gets pinned's classic fill at once, as before. `MuleModules.Dig` now raises a temporary chest and calls
`OnDug`, so the mule's dig has the revamp's quality, loot and guardian rules (it used to copy the guardian loop).

### Monster stealing (ServUO `Scripts/Services/Monster Stealing/` -> `server/customizations/Services/Monster Stealing/`)

| ServUO | Ours | What |
|---|---|---|
| `Core/StealingHandler.cs` (255) | `Core/StealingHandler.cs` | `HandleSteal`, `CheckLocation`, `GetStealingChance` (ServUO's table), `FameLevel`; the has-been-stolen flag as a weak table; the shard's `RollShardGain` |
| `Core/BaseThieveConsumable.cs` (189) | `Core/BaseThieveConsumable.cs` | the effect enum, the per-player effect table, `ApplyEffect`/`RemoveEffect`, the saved effect type and duration |
| `Core/BaseBalmOrLotion.cs` (60) | `Core/BaseBalmOrLotion.cs` | the balm base, `ICommodity` in pinned's shape |
| `Items/*.cs` (11 files, 799) | `Items/*.cs`, the same eleven names | the four balms, two lotions, the seed, the draught, the gem (with its own resurrect gump), the lantern, the tool box |

The hook: `Stealing-monster-stealing.patch` adds ServUO's call (`Stealing.cs:419-423`) at the same place in pinned's
`StealingTarget.OnTarget`, after the pack-item roll.

### The five patches (`server/patches/`, all argued below)

| Patch | Pinned file | ServUO lines | What |
|---|---|---|---|
| `Stealing-monster-stealing.patch` | `Skills/Stealing.cs` | 419-423 | the call into `StealingHandler.HandleSteal` for a creature target |
| `LockPick-treasure-chest-failed-pick.patch` | `Items/Skill Items/Thief/LockPick.cs` | 158-180 | a failed pick marks a revamp chest (the grubber), or breaks one item in a classic one |
| `Unlock-treasure-chest-levels.patch` | `Spells/Third/Unlock.cs` | 78-96 | a revamp chest up to Cache takes full Magery against 50, 80, 100 |
| `RemoveTrap-treasure-chest-disarm.patch` | `Skills/RemoveTrap.cs` | 66-114, 235-251, 254-400 | the owner-only timed disarm with the ancient guardian, the out-of-range reset, `RemoveTrapTimer` |
| `BaseCreature-treasure-map-all-facets.patch` | `Mobiles/BaseCreature.cs` | 5902-5910 | maps drop on every facet, for the facet (pinned: Felucca and Trammel only) |

### Also changed

- `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs`: treasure maps pay ServUO's new-system column
  (Stash and Supply 50, Cache 250, Hoard 750, Trove 1000) now that the maps are the revamp's; the fact's expectations
  follow (`CleanUpBritanniaPointsVerification`).
- `server/customizations/Mobiles/Mule/MuleModules.cs` `Dig`: above.
- `docker/uo/apply-patches.sh`: the two `replace_file` lines and the five `apply_patch` lines, each with its reason.
- `CHANGELOG.md` new section **2026.10.16** (two Added lines); `VERSION` 2026.10.16. Wiki not published.
- `testing/playtest-steps.json` P127-1 to P127-7 and `testing/bot-triage.md` group P127.

## Dependency walk and what was left out

Every `typeof` and `new` in the 19 ServUO files (399 names) against pinned's 6,926 type names and our 1,738, scripted
(`mu-types.txt` from `D:\UO\ModernUO-pinned`, as the port recipe says). 66 were absent from both; a case-insensitive pass
found two renames (`ScrollOfTranscendence` and `ScrollOfAlacrity` are pinned's `ScrollofTranscendence` and
`ScrollofAlacrity`, used as such). The rest:

**Loot-table types left out (23), as P123 left its 13 rows:** `SledgeHammerWeapon`, `SmithyHammer` (pinned's
`SmithHammer` is a tool, not ServUO's weapon), `BladedWhip`, `BarbedWhip`, `SpikedWhip`, `ChefsToque`,
`SkullTiledFloorAddonDeed`, `AncientWeapon1`, `AncientWeapon2`, `AncientWeapon3`, `DecorativeHourglass`,
`AbyssalCloth`, `EssencePersistence`, `ManaPhasingOrb`, `RunedSashOfWarding`, `ShieldEngravingTool`, `ForgedPardon`,
`SkeletonKey`, `MasterSkeletonKey`, `SurgeShield`, `TastyTreat`, `OctopusNecklace`,
`AncientShipModelOfTheHMSCape`. So: the decorative table holds only the creeping vine (Ranger); the supply special
loot is the Legendary Mapmaker's Glasses (and, for an artisan, a recipe); the cache-and-up special loot is the two
skull weapons; the Ter Mur artisan's imbuing ingredients are 10 of 12; the decorative minor artifacts 4 of 5.
Pinned's gargish leather and stone armour comes as `Type1`/`Type2` pairs, so both stand in for each ServUO name (8 and 8
entries for ServUO's 4 and 4).

**Spawn-table creatures left out (14):** `ColdDrake`, `FrostDragon`, `FrostDrake` (Trammel/Felucca level 7 row),
`LeatherWolf`, `DragonWolf` (Ter Mur), `MyrmidexLarvae`, `WildTiger`, `Lion`, `SabertoothedTiger`, `Infernus`,
`KotlAutomaton`, `MyrmidexDrone`, `Triceratops`, `Anchisaur` (Eodon). Every row keeps at least one creature; they are
P129's (creatures part 2) to add back, and a one-line edit each here.

**Subsystems absent from pinned:** `RunicReforging.GenerateRandomItem` and `RefinementComponent.Roll`. D-38 (CC4) already
records chest loot unreforged and no refinement roll; the revamp's equipment gets pinned's `BaseRunicTool.ApplyAttributesTo`
with the chest's own AOS stat rolls (the same as pinned's classic chest), and `GetMinMaxBudget` (only reforging read it)
went with it. `Loot.MysticRegTypes`: absent, so a Ter Mur mage's stash gets the standard reagents.

**Not ported, by design:** `StealingHandler.HandleSmugglersEdgeSteal` and its `TryStealItem` (only the store-bought
Smuggler's Edge called them; the store is not ported); the `ExodusZealot` branches (the Exodus Encounter is a port-list
row of its own); `TreasureMapChest.Fill(from, cont, level, isSos)`, ServUO's old-system chest fill (pinned's classic
`Fill` is what the camps and the SOS chest run today, and the revamp fills through `TreasureMapInfo.Fill`); the balm of
protection's and life shield lotion's damage hooks (`HandleDamage`, `HandleLifeDrain` are here, but ServUO calls them
from its `AOS.Damage`, which pinned's does not: the two effects apply and expire, and reduce nothing yet. Decision 4).

## Alternatives for each patch, argued before patching

The subsystem policy: a failing patch beats copied upstream logic, and every patch names what it rejected.

1. **`TreasureMap` and `TreasureMapChest` as replacements, not patches.** A patch would be 1,500 added lines against a
   915-line file; a replacement shows as one file and the fact `TheFivePinnedFilesCarryTheirPatchedLines` plus the
   round-trip and dig facts stop the build if pinned's shape moves under it. Rejected: a subclass (`RevampTreasureMap`),
   because every pinned drop site constructs `TreasureMap` by name and the saved maps are `TreasureMap`s; and leaving
   pinned's map with a side table, because the level scale, the facets, the dig and the fill are all in the two files.
2. **Stealing.cs, five lines.** Rejected: re-registering the skill callback with our own target, which would copy the
   whole 300-line `StealingTarget` to add one call at its end.
3. **LockPick.cs and Unlock.cs, one hunk each.** Rejected: overriding `LockPick` on the chest to detect a failed pick
   (the failure never reaches the chest; only the item knows), and a `CanUnlock` virtual on `LockableContainer` (a
   larger patch to a more-used file).
4. **RemoveTrap.cs, three hunks.** Rejected: a replacement (the faction-trap half would be a copy hiding drift), and
   `IRemoveTrapTrainingKit`-style dispatch (pinned has no such interface; the chest is a `TrappableContainer` and the
   skill's target decides before the container sees anything). The locked check (501283) is applied to the revamp chest
   only, where ServUO applies it to every lockable container: pinned's RemoveTrap on a locked box is otherwise untouched.
5. **BaseCreature.cs, four lines.** Without it a map drops only on Felucca and Trammel (pinned's rule), and the Malas,
   Tokuno, Ter Mur and Eodon tables would be reached only through a chest's map or staff. BaseCreature already carries
   three of our patches; this hunk is ServUO's own lines. The `TreasureMapChance` virtual stays absent (D-42).

## Decisions taken inside the port (fidelity principle, D-4 rule)

Fixes to ServUO bugs that made something *broken* (fixed) or *missing* (copied), each marked in the file's header:

- **Fixed:** the balms, the seed and the draught never answered a double-click in ServUO (only Life Shield Lotion
  overrides `OnDoubleClick`; `OnUsed` was never called), so ten of eleven items were inert. They answer a double-click in
  the pack now.
- **Fixed:** `GetWidthAndHeight`'s missing `else` made every Trammel and Felucca map 300 wide (ServUO sets 600, then
  overwrites it); 600 here, as pinned and as the code reads.
- **Fixed:** `ResetLocation` computed a new spot and discarded it (a 30-day reset only un-decoded the map); it moves the
  chest now, as the code's name says.
- **Fixed:** `MutateType` turned a skull weapon gargish for every facet, leaving a human a weapon no human can hold; Ter
  Mur chests only.
- **Fixed:** the seed's and draught's `DoCleanup` cleared every cooldown on each world save (`< now + cooldown` is
  always true); expired entries drop as they are met.
- **Fixed:** the dig hued the spawn before its null check (a null spawn threw).
- **Fixed:** the grubber's item pick looped forever when every item was blessed; it gives up after ten draws.
- **Copied:** ServUO's `list.Concat(...)` results are discarded (two places), so its functional minor artifacts and the
  Malas coffin piece never drop from those paths; ours matches what ServUO runs, without the dead calls.
- **Copied:** `TreasureMapChest.Fill` for the SOS chest stays pinned's.

## Tests

Two new fact files, both `[Collection("Sequential UOContent Tests")]`:

- `server/tests/Services/TreasureMaps/TreasureMapRevampVerification.cs`, 8 facts (one a theory over the five levels):
  the revamp is on and classic levels convert; a map knows its facet and its spot is inside it; decoding by level; a
  dug chest is the revamp's and pays by level (lock, trap, quality, the gem bag's gold in the level's range, the gem
  count, the scroll count, the gear count, the map reference, four hued spawns with the guardians listed); the chest
  refuses to open while trapped or guarded (and the ancient guardian's name, hue, buffs); a failed pick brings a
  grubber that takes one item; a map and a chest survive a serialization round trip (package, reset, level; failed
  pick, gold art, dig time, map, ancient guardians); the five pinned files carry their patched lines in the build tree.
- `server/tests/Services/Monster Stealing/MonsterStealingVerification.cs`, 10 facts: ServUO's chance table and the
  fame line; only a Felucca dungeon counts (a `DungeonRegion` registered on each facet in turn); a thief at 120 steals a
  special item once per creature, a tame creature and a thief below 100 get nothing; a monster steal trains Stealing
  past 127.5 (and gains nothing with the shard rule off); one balm at a time, worn off; Stone Skin's resistances; the
  seed and the draught once in ten minutes; the tool box's lockpicks and daily top-up; the gem waits out six hours
  (and offers its gump when it can); a balm and the box survive a round trip.
- `CleanUpBritanniaPointsVerification.SpecialCasesPayServUOsValues`: the map points for classic levels 0-7 are now
  50, 50, 50, 50, 250, 250, 750, 1000.

**Seen failing first.** Two break sets on the real tree (`breaks.py` in my scratchpad, each reversal asserted, the
tree hashed before and after: byte-identical both times), each run through `build.sh --tests-only`:

- 19 breaks at once (no level conversion, no scroll drop, a Trove decodes at 50, spawns unhued, a trapped chest opens,
  no grubber, gold art wrong, the Stealing hook patch skipped, the chance table off by one, Trammel counts, a creature
  gives twice, no gain roll, a 0-strength balm, a 0-physical lotion, no seed cooldown, the box never decrements, the gem
  ignores its cooldown, a 31-minute balm, the old map points): **22 failed, 1,298 passed** of 1,320: every new fact but
  one went red (the theory in all five cases), and the points fact with them.
- The one that stayed green, `AMapKnowsItsFacetAndItsSpotIsInsideThatFacet`, had no break aimed at it; a second run
  with `GetFacet` answering Trammel for Malas: **1 failed, 1,319 passed**, that fact.

Greens: build 3 had my own test's arithmetic wrong (fame 18,750 is level 24.9995, truncated to 24; the fixture is 18,752
now). Build 4 and the final build after the restores: **1,320 of 1,320**. The full upstream suites, unfiltered, on the
final builder image: `Server.Tests.dll` 910 total, **893 passed, 0 failed**, 17 skipped; `UOContent.Tests.dll` 2,507
total, **2,416 passed, 0 failed**, 91 skipped.

**The test shard boots clean, and a world saved by the pinned map loads, saves and reloads.** `sl-modernuo:cc-p127`
on a copy of the test world's newest automatic backup (`2026-10-16-12-35-00`, saved by the running image), the parent
folder mounted as the compose file does:
- boot 1: `[ShardVersion] Shattered Legacy 2026.10.16 (63 version(s) in the changelog)`, `Loading world done (207044
  items, 35047 mobiles)`; stopped: `Saving world done`, `Writing world save snapshot done`;
- boot 2 on that save: `Loading world done (207658 items, 35102 mobiles)` (the seeders' additions), saved the same way,
  no error in either log beyond the standing Test Center port warning.
- The save's item index lists `Server.Items.TreasureMap`, so the version-0 maps the test world holds went through
  `MigrateFrom(V0Content)` (level converted, a package given) and were written back at version 1; it lists no
  `TreasureMapChest` (no dug chest was in the world), so the chest's v4-to-v5 path is proved by its round-trip fact only.
- Two things the port recipe's headless invocation no longer does, for the recipe: a piped `n`/`save`/`shutdown` is not
  read (the console commands never ran; `docker stop` saves on shutdown instead), and a world with no accounts now
  throws `HeadlessConsoleInputException` at the owner prompt rather than waiting on stdin. And mounting `Saves`,
  `Backups` and `Archives` separately makes the save's publish fail ("Cannot create Saves": the engine renames the
  folder), as `docker-compose.test.yml` already warns: mount the parent.

**Not done:** a client. Nothing here was seen in game.

**Migration JSONs:** the build emits none for a bumped version (P49 left that unverified; the builder image's
`Migrations/` holds only pinned's v0 and v2-v4 after a green build). `server/migrations/Server.Items.TreasureMap.v1.json`
and `Server.Items.TreasureMapChest.v5.json` are written by hand in the generator's shape (rule names copied from
pinned's own files), so the next bump of either type can migrate from this one; the build does not read them today.

## Play-test items added

Through the For Chase list below; Who and steps in `testing/bot-triage.md` (P127 group) and `testing/playtest-steps.json`:
P127-1 BOT-PARTIAL (decode), P127-2 BOT-PARTIAL (dig), P127-3 BOT-PARTIAL (lock, trap, open), P127-4 BOT-PARTIAL
(other facets), P127-5 BOT (monster stealing), P127-6 BOT (Stealing past 120), P127-7 CC (test world boot).

## Deviations and decisions for Chase

1. **Staff `[add TreasureMap <n>` takes the classic level** (converted), where ServUO takes a revamp level: `[add
   TreasureMap 7 Trammel` is a Trove here, `3` a Supply. Players never see it. Say if you want the enum instead.
2. **An ancient chest guardian drops its normal loot.** ServUO sets `NoLootOnDeath`, which pinned's BaseCreature lacks and
   this prompt did not patch for. For the register.
3. **The six-hour Gem of Salvation timer and the has-been-stolen flag live in memory**, not on the player or creature
   (ServUO serializes both on `PlayerMobile` and `BaseCreature`): a restart lets a gem be used again and a creature be
   stolen from once more. Creatures rarely outlive a restart; the gem's six hours can be shortened by one. For the
   register.
4. **Balm of Protection and Life Shield Lotion apply and expire but reduce nothing yet:** ServUO calls their hooks from
   its own `AOS.Damage` and `BaseCreature`'s life drain; pinned's have no such call, and a damage patch is its own
   decision (the AOS-damage-eater hook is the shape it would take). For the register, and a one-hunk follow-up if you
   want them live.
5. **The Smuggler's Lantern says Spell Channeling** and pinned never stops a cast for an equipped light anyway, so the
   line is true by accident. For the register as "ours".
6. **The shard's Stealing gain rule** (headline): on by default, `clusterf.stealing.monsterGain` false turns it off and
   leaves ServUO's no-gain handler.
7. **`TreasureMap.GetRandomLocation` gives up after 10,000 tries** and takes the last point unchecked: ServUO loops
   forever on a facet whose map files are missing. On the running shard with every facet's maps loaded it never fires;
   in the test host it always does. If a facet ever lacks its maps, a chest can land on water: a log line there would
   be the next step.
8. **Clean Up Britannia points for maps changed** with the level scale (above). A player's old map pays the new column.
9. **The deviation register entries this needs** (agents do not edit `docs/`): items 2, 3, 4, 5 above, and the 23 + 14
   left-out names as one entry each, "reverses when" being each type's own port.

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these.

1. **Get and decode a map:** as staff, `[add TreasureMap 5 Trammel` (a Cache map) and hand it to a player with Cartography 71; double-click it: it decodes and names itself a cache map of a theme for somewhere in Trammel (below 71 it is too difficult).
2. **Dig it:** with a shovel, walk to the pin and Dig; a rusty, standard or gold chest rises with four hued creatures around it, some titled (Guardian).
3. **Open it:** it refuses while locked or trapped; pick the lock (a failed pick marks it for a grubber), use Remove Trap (a 10-second tick; a failure fires the trap and wakes an Ancient Chest Guardian), then open it: a bag of gems with gold, skill scrolls, themed magic gear.
4. **Another facet:** `[add TreasureMap 3 Malas` and dig it on Malas: the map says Malas and the Malas creatures rise.
5. **Monster stealing:** with Stealing 120 and empty hands in Felucca Shame, steal from monsters' packs: now and then a balm, lotion, seed, draught or gem; the same creature never twice; a balm applies and a second is refused for 30 minutes.
6. **Stealing past 120:** set Stealing 130 and steal from twenty fresh monsters there: it rises.
7. **Test world boot:** done by CC on a scratch copy (below).

## Repo size rule

No pending file in either repo is over 5 MB; the largest new one is `server/patches/TreasureMap.cs`. Build logs and the
patch generator stayed in the session scratchpad.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

code, 33 files: `CHANGELOG.md`, `VERSION`, `docker/uo/apply-patches.sh`, the mule, the points data and its fact, the 14
monster-stealing files, the two treasure-map files, the two schema JSONs, the two replacements and five patches, the two
fact files. docs, 7 files: this note, `testing/bot-triage.md`, `testing/playtest-steps.json`, the overseer's pending
`docs/feature-queue.md`, and the machine output (`testing/SUMMARY.md`, `testing/play-tests.json`, `tools/progress.json`
from a `--dry-run` of progress.py, which writes it anyway; the bot's run folder). No file is near 5 MB.

P127 DONE
