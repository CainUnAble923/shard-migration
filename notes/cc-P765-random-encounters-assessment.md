# cc-P765: Random Encounters, assessed for Shattered Legacy

Iron Golem, 2026-11-01. Assessment only, no code. Read from `D:\UO\third-party\code\random-encounters` (reference only:
nothing there was built or run). Docs copy `D:\UO\golems\Iron\shard-migration` on `golem/Iron/P765`, not committed.

## In plain words

- **What it is.** An old (2005-2006) RunUO script, lightly updated for ServUO in 2023. Every few minutes it picks
  players who are out travelling and drops a small group of creatures (or items) near them, chosen from a big XML file
  by facet, region and time of day.
- **What I found.** The idea fits the shard well: road ambushes between towns, League work in the field, festival
  events. The code does not:
  - it needs a spawner add-on that ModernUO doesn't have;
  - two bugs would leave its creatures in the world for good;
  - its cleanup deletes loot already in players' backpacks;
  - its 2,944 sample encounters mostly copy the stock world's spawns.
- **Recommendation: idea only.** If you want encounters, a new prompt can build a small encounter system of our own,
  about one Golem task, with three starter encounters (sketched below). Copying this code over would cost more and need
  more fixes.
- **For you:** decide whether you want that follow-up task. Nothing else to do.

## 1. What it does

**Origin.** "Random Encounter Engine V 2.0RC1" by Joe Kraska ("Courageous"), RunUO, 2005-2006. BRAX4578 put an update for
ServUO 57.1 on servuo.dev in January 2023, and says he takes no credit. 11 .cs files (4,262 lines), the bundled "Searches
System" (9 .cs, 3,567 lines, plus two Python generators), 4 XmlSpawner2 files switched off (`ArteGordon\*.cs.OFF`), and a
560 KB sample `RandomEncounters - Copy.xml`.

**How encounters are defined** (`RandomEncounters.xml`, read from `./Data/RandomEncounters.xml`):
- The root, `<RandomEncounters>`, has these attributes:
  - `picker` (`sqrt` or `all`), `language`, `skiphidden`;
  - `delay` (seconds after start);
  - `interval`: one value, or up to three as `dungeon:wilderness:guarded`; house and jail are "not implemented";
  - `cleanup` (seconds before spawns are swept), `cleanupGrace` (sweeps skipped while a player is near), `debug`.
- `<Facet name>` holds `<Region type="Dungeon|Wilderness|Guarded" name="<region name>|default">`.
- `<Encounter>` has these attributes:
  - `p`: probability; the engine draws once and takes the lowest probability at or above the draw; `p="-1"` is
    "inclusive" and always runs;
  - `distance` (`7` or `3:7`);
  - `landType` (`Water`, `OnRoad`, `OffRoad`, `AnyLand`), from the land tile under the player and a hard-coded road-tile
    table;
  - `time` (`Day`, `Night`, `Twilight`, `AnyTime`, from `Clock.GetTime`);
  - `level` (`1` or `0.4:Fighter`), compared with a level computed from the player's stats and weighted class skills
    (`Helpers.CalculateLevelForMobile`);
  - `scaleUp` adds up to two extra copies of each mobile for stronger players.
- Inside an encounter, `<Mobile pick="A,B" n="1:3" p=".25" effect="Smoke" effectHue>` and `<Item ...>` nest:
  - an item can sit in an item or on a mobile;
  - child mobiles spawn near their parent;
  - `<Prop name value>` sets a property on what was made.
- Types are looked up by class name (`SpawnerType.GetType`, `Activator.CreateInstance`). Gold cannot be spawned.

**Timers and picking** (`Timers.cs`, `EncounterEngine.cs:540-760`):
- **One timer per region category.** Dungeon, Wilderness and Guarded each have their own. The category comes from the
  region's class (`Helpers.RegionCategory`: `GuardedRegion`, `HouseRegion`, `DungeonRegion`, `Jail`, `GreenAcres`,
  otherwise Wilderness).
- **Who counts.** On each tick, candidates are online players at AccessLevel Player, alive, and, by default, not hidden.
  The "Young" check is commented out.
- **The sqrt picker is broken.** It computes `Math.Sqrt` of an empty list and then moves every candidate across
  (`EncounterEngine.cs:584-594`), so "sqrt" behaves as "all".
- **Lookup.** The region is looked up as `map:category:regionName:landType:time`, falling back to `default` and then
  `AnyTime` / `AnyLand`.
- **Logging.** It writes to the console on every check, debug or not (`Console.WriteLine` at `:642-728`).
- **The file is reread on change.** A reinitialize timer watches the XML's write time, so changes need no restart.

**Spawn finding** (`SpawnFinder.cs` with the Searches System):
- It searches a spiral, octant or line out from the player for a tile at the wanted distance with the same region class
  as the player, not in a house, and land or water as asked (`CanFit`, `CanSpawnMobile`).
- `SpiralSearch.cs` alone is a 2,536-line generated table.
- Spawns can show a smoke, fire, vortex, swirl, glow or explosion effect.

**Serialization and cleanup.**
- Every spawned thing gets an XmlSpawner2 attachment, `XmlDateCount`, the only `Serialize` override.
- `DeleteTimer` walks `XmlAttach.AllAttachments` every `cleanup` seconds and deletes what is older.
- Two defects:
  - **Creatures are never cleaned up.** `if ( !(c.Controlled = true ) )` (`Timers.cs:244`) is an assignment: it marks
    every encounter creature as controlled and never deletes one. Left alone, ownerless "controlled" monsters pile up
    for good.
  - **Items are deleted wherever they are.** That includes loot already in a player's backpack or bank (`Timers.cs:221-229`).
- `Import.cs` turns Nerun's / premium spawner files into encounter XML. That is where the sample's 2,944 encounters come
  from (215 at level 0, 709 at 0.4, 157 regions across Felucca, Trammel, Ilshenar, Malas and Tokuno). Only one encounter
  uses `landType`, and one uses `time`.

**Core edits needed:** none in the engine. It is all scripts, but it needs XmlSpawner2 (`XmlAttach`, `XmlDate`), which
ServUO ships and ModernUO does not. The region class `GreenAcres` is ServUO's.

## 2. Fit

**Where encounters would add to our game:**
- **Travel between towns** on the SoS land: roads and wilderness, Trammel and Felucca. Today, travel between towns is
  quiet unless you walk into a spawner. A road encounter makes the trip itself a small event.
- **League work in the field.** Combat contracts T1 and up, and the "shallow / standard / veteran dives" in
  f12-levels-loops-caps.md ("What current level unlocks"). An encounter can be the contract's target appearing, rather than
  a fixed spawn players camp.
- **Seasonal events.** The festival windows (`ClusterFSeasonalSwitch`) and Festival Tokens (P760). A festival-only
  encounter table switched by the season is a cheap way to make the world feel the festival outside New Haven's stall.
- **The reset loop.** Encounters should key on **current level** (F-12): the level that resets to 1 each loop, which
  `ClusterFCreatureLevels.ProvisionalPlayerLevel` stands in for until F-12 is built. A looped player at current level 10
  meets level-10 trouble again, and an echo loop stays quick. They should be tuned by the con bands, never above yellow
  (level gap +2) for the player's current level.

**What they must never do:**
- **Never on the Wakening Isle or in New Haven.**
  - Exclude the isle's map (`TutorialWorld.Isle` = `FoldMaps.Fold`) and every tutorial region.
  - Exclude Haven Island and its town regions (`Regions/HavenTownRegions.cs`), Old Haven's Burrows and the apprentice
    training regions.
  - Exclude any character that has not graduated loop 0 (the tutorial's trainee state), and Young characters.
  - The engine only knows "Guarded / Dungeon / Wilderness" by class, and our Haven and isle regions would read as
    Wilderness. An explicit deny list is required, not optional.
- **Never grief AFK or busy players.**
  - Only players who have travelled recently (a few dozen tiles in the last few minutes).
  - Not while gathering in place, at a forge, in a trade or bank window, mounted on a ship, in a house or a guarded town.
  - Not hidden, not dead.
  - One encounter per player per 20-30 minutes, with an account-wide cooldown so alternate characters cannot farm.
  - A cap per screen, so a group of ten does not get ten ambushes at once.
- **Never break our reward rules.**
  - Creatures carry their normal loot only.
  - Any box goes through `ClusterFLootBoxes.Award` with a source key (`encounter:<id>`), so it comes once per loop and
    shows the repeat line after.
  - No power scrolls (those are F-12's cap gates from champions, paragons and bosses), no stat or skill rewards, no
    Festival Tokens outside a festival, nothing that bypasses the AP / Renown budgets.
  - Encounter creatures are not tameable (no rare-pet farming by standing in the right spot).
  - Cleanup deletes only unowned creatures that are not fighting, never items in a player's container or on a corpse
    being looted.
- **Never fight the existing world.**
  - No spawns inside houses, on boats, in dungeons that have their own spawn design (The Setting, the New Haven dungeon's
    bands, champion spawns), or in jail.
  - Despawn quietly when no player is in range.

**Three sample encounters in our setting** (sketches, not final text; the System's lines are in its dry, PG voice):

1. **"Toll Road"** (travel). On a road tile between two towns, by day, current level 15 and up. Two to four brigands at
   the player's con band step out of the brush, and one demands a toll:
   - say "pay" to lose 5% of the gold you carry, up to 200, and walk on;
   - fight, and the leader's corpse holds the toll box and normal brigand loot.
   
   System: "An unlicensed toll booth has opened on this road. Your options are compliance or a sharply worded reply."
   Achievement on the first win: "Declined to Pay the Road Tax". One loot box, once per loop (source `encounter:toll`).
2. **"Lost Surveyor"** (League work). Wilderness, any time, for League members with an open field contract. A League
   surveyor (a friendly NPC) is pinned down by two or three creatures native to the area. Save her and she marks a cave
   or ruin on your map for the contract, and the contract's progress counts the kills.
   
   System: "A League surveyor has located a hostile ecosystem by standing in it." Reward: contract credit and her
   thanks. No box; the contract pays as contracts do.
3. **"The Lantern Procession"** (festival). Only while the Halloween switch is on, at night, off-road on Trammel. A slow
   column of lantern-headed walkers (a reskinned undead type) crosses near the player. It is harmless unless attacked;
   if attacked, the leader drops a Festival Token by P760's rule (whoever did the most damage).
   
   System: "A procession is passing through. Attendance is optional; interference is noted." Despawns at dawn.

## 3. Port cost

**Files and lines** (downloaded .cs, the zips left out):

| Part | Files, lines | ModernUO equivalent | Port or replace |
|---|---|---|---|
| Engine, picking, generation | `EncounterEngine.cs` 1,167, `Records.cs` 374, `Definitions.cs` 49 | Generic collections, `Timer.DelayCall`, `AssemblyHandler.FindTypeByName`, `Utility` | Rewrite small: about 300 lines |
| Config | XML + `XmlLinePreservingDoc.cs` 53; reread on change | The shard's pattern: a JSON file in `Configuration/` written with defaults on first start and a `[... reload` command (as `reward-stores.json`, P760), plus `clusterf.encounters.*` switches in `modernuo.json` | Replace |
| Regions, time, land | `Helpers.cs` 344 | `Region.IsPartOf<GuardedRegion/DungeonRegion/HouseRegion/JailRegion>`, `Clock.GetTime`, `TileFlag.Wet`; our deny list; `ClusterFCreatureLevels` for levels | Rewrite: about 100 lines |
| Spawn finding | `SpawnFinder.cs` 382 + Searches System 3,567 (spiral tables, octant, line, circle) | A random ring search with `Map.CanSpawnMobile`, a region check and a line-of-sight check, as pinned's spawners do: about 60 lines | Replace |
| Sorted lookup | `RedBlackTree.cs` 993 | `SortedList` / `SortedDictionary` | Delete |
| Creation tag and cleanup | `XmlDateCount.cs` 41, `Timers.cs` 357, needs XmlSpawner2 | A registry of what each encounter spawned (serials and time), a sweep timer and a startup sweep, or one source-generated field on a marker; no attachment system | Rewrite: about 120 lines |
| Staff commands | `Commands.cs` 80 (`[rand`) | `CommandSystem.Register`: `[Encounters status|reload|force <player> <id>` | Rewrite: about 60 lines |
| Spawner import | `Import.cs` 422 | Not wanted: our spawns are our own | Drop |

- **Rough effort.** One Golem prompt for the engine (about 650 lines of our own code), its JSON, the deny list, the
  cooldowns, the three sample encounters and facts (an encounter never fires on the isle, in Haven, for a trainee or an
  idle player; cleanup never touches a player's items; boxes go once per loop). Then content, a few encounters at a
  time, as later prompts.
- **A line-by-line port** would cost more:
  - XmlSpawner2 is a large dependency, and pinned has none, so its attachments must be replaced either way;
  - the two cleanup defects and the sqrt picker must be fixed either way;
  - ArrayList and Hashtable code needs reworking throughout;
  - the Searches System's generated tables would have to be kept or regenerated.
  
  Little of the original would survive.

**Risks:**
- **Griefing and fairness:** see the never-do list. These are the main design risk, more than the code.
- **Loot inflation:** a per-encounter source key through `ClusterFLootBoxes` caps boxes. Creature loot stays what the
  creature drops anywhere.
- **Server load:** a candidate scan every few minutes is cheap. The spawn search must stay bounded, with fixed tries and
  no tables.
- **Persistence:** spawns left at a restart must be swept on load. That was the original's attachment job, and it is
  where it went wrong.
- **Content debt:** the engine is the cheap part. Encounters that feel like ours need writing, tuning by con band and
  facts, as the sample's 2,944 imported entries show.

**License.**
- `COPYING.txt` (in the root and again in `Searches System\`) is the **GNU General Public License, version 2**.
- The headers say "This program is free software ... either version 2 of the License, or (at your option) any later
  version" (Searches System, 7 files), or "This file is restricted according to the GPL" (`Import.cs`, `Commands.cs`,
  `RedBlackTree.cs`).
- The ReadMe calls it "a limited use license ... contained in COPYING.TXT". One file credits Joannes Vermorel (2003),
  for the red-black tree.
- So it is GPL v2 or later, which can be combined with ModernUO's GPL v3.
- `SOURCE.txt` says "TERMS: none stated", which is wrong: the terms are the GPL.
- If any of it were ported:
  - keep the copyright lines, and keep the server's source available to anyone the server binaries go to;
  - running the server for players is not distribution under GPL v2/v3; ModernUO is under plain GPL v3, not AGPL;
  - credit Joe Kraska and BRAX4578.
- An "idea only" rewrite copies no code, so no GPL duty arises, but crediting the idea in the notes is good manners.

## 4. Recommendation

**Idea only.** Encounters fit travel, League field work and festivals. This code would not survive a ModernUO port:
XmlSpawner2 attachments, two cleanup defects (creatures kept for good, looted items deleted), a non-working picker,
generated search tables and imported stock-spawn data. If Chase wants the feature, a new prompt can build a small,
ours-from-scratch encounter system to the never-do list above, starting with the three samples.

## Other notes

- **`D:\UO\third-party\CODE-INTAKE.md`:** the master table had no row for `code/random-encounters`. Its last rows are
  from 10-22, and `code/pet-shrink` (P764) is missing too. I added a row with Overseer `assess (P765)` and the license
  fixed to "GPL v2 or later". The scout's project copy (`claude/servuo-code-intake.md`) re-syncs from the master.
- **Related prior art:** UOReSpawn's `AmbushNPC` (`notes/cc-P104-uorespawn-read.md`): a hidden trigger that springs a
  facet-themed gang. That is a placed ambush, not a travel encounter. The same deny list would apply if it were ever
  ported.
- **Nothing built, run or changed in the code copy.**

P765 DONE
