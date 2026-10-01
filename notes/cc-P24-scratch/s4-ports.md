# P24 S4: MiniChampionSystem, Underworld PuzzleRoom, Tomb of Kings chambers

Read-only research, 2026-10-01. Nothing outside `notes/cc-P24-scratch/` was changed.
Paths: `SV` = `D:\UO\ServUO-pub57\Scripts`, `PIN` = `D:\UO\ModernUO-pinned\Projects\UOContent`
(commit 7c9215d97), `OURS` = `D:\ShatteredLegacy\server\customizations`.
Type presence was checked against an index of every `class|enum|interface|struct` name declared
in pinned (7,120 names) and OURS (1,298 names), then each hit or miss was confirmed by opening the file.

## 0. Already ported? (searched by name and by behaviour)

- OURS: no MiniChamp, PuzzleBox, MagicKey, MazePuzzleItem, Mastermind, ChamberLever, ChamberSpawner,
  BaseDecayingItem, CircuitTrap (grep of all .cs in OURS returned none of them).
- Pinned: none of the three systems (grep for MiniChamp|PuzzleRoom|Mastermind|MazePuzzleItem|
  ChamberLever|ChamberSpawner returns only the two ToK *region* classes, see section 3).
- `notes/index-blindspots.md:354` already records `ChamberLever.Levers` vs `LeverPuzzleController`
  as a name-index false match. They are unrelated.

## 1. MiniChampionSystem

### Files (wc -l)

| File | Lines |
|---|---|
| `SV/Services/MiniChampionSystem/MiniChampionSpawn.cs` (controller `MiniChamp`, `SliceTimer`, `[GenMiniChamp]`) | 476 |
| `SV/Services/MiniChampionSystem/MiniChampSpawnInfo.cs` (per-type wave state) | 140 |
| `SV/Services/MiniChampionSystem/MiniChampType.cs` (enum, `MiniChampTypeInfo`, `MiniChampLevelInfo`, `MiniChampInfo` table) | 399 |
| **Total** | **1,015** |

No file outside the folder references `MiniChamp` (grep of SV, zero hits outside the folder).

### Dependencies and pinned equivalents

Grep of the three files for `Core.|Xml|Points|Region|Quest|Siege` returns nothing: **no XmlSpawner, no
PointsSystem, no expansion check, no Region type, no quest hook.** What it does use:

| ServUO use | Where | Pinned / OURS equivalent |
|---|---|---|
| `Map.GetSpawnPosition(Point3D,int)` (ServUO **core**, `D:\UO\ServUO-pub57\Server\Map.cs:1159-1175`) | SpawnInfo.cs:51,70 | Not in pinned. Pinned has `Map.CanSpawnMobile(Point2D,int)` (`Projects/Server/Maps/Map.cs:1102`); `ChampionSpawn.GetSpawnLocation` (`PIN/Engines/CannedEvil/ChampionSpawn.cs:799-823`) is the same idea. ServUO body is 17 lines; inline as a private helper (ServUO logic, not copied pinned logic) |
| `BaseRenowned` (essence always drops) | SpawnInfo.cs:83 | OURS `Mobiles/Normal/BaseRenowned.cs:22` |
| `ScriptCompiler.FindTypeByFullName` | SpawnInfo.cs:137 | `AssemblyHandler.FindTypeByFullName` (`Projects/Server/AssemblyHandler.cs:186`), or just `IGenericWriter.Write(Type)` (`Projects/Server/Serialization/IGenericWriter.cs:40`) / `ReadType` (`BufferReader.cs:139`) |
| `ReadStrongMobileList` | Spawn.cs:441, SpawnInfo.cs:138 | `ReadEntityList<T>` (`Projects/Server/Serialization/SerializationExtensions.cs:93`) |
| `PropertiesGump` | Spawn.cs:376 | `PIN/Gumps/Props/PropsGump.cs:25` |
| `ColUtility.Free`, `IPooledEnumerable` | SpawnInfo.cs:57, Spawn.cs:338 | drop (plain list; pinned range enumerables need no Free) |
| 80 distinct `typeof(...)` in the table (walked: `MiniChampType.cs`) | | 33 in pinned, 39 in OURS, 8 in neither (see below) |

**The array walk.** 80 types are named in `m_Table`. 33 are in pinned (e.g. `Meraktus`, `Minotaur*`,
`LavaSnake`, `Efreet`), 39 are already in OURS (all 13 Renowned bosses, the `Enslaved*` goblins, 12
of 13 `Essence*` types, `FireAnt`, `LavaElemental`, `PitFiend` ...). The 8 in neither:

- `ClanCA ClanCT ClanRC ClanRS ClanSH ClanSS ClanSSW`: **already ported under other names**, e.g.
  `OURS/Mobiles/Normal/ClanChitterAssistant.cs:1-3` ("ServUO: Mobiles/Normal/ClanCA.cs ... named by
  the spawn-data spelling ... not ServUO's ClanCA", Q-056). A one-token rename per table entry.
- `EssencePersistence` (`SV/Items/Resource/EssencePersistence.cs`, 62 lines, `Item, ICommodity`):
  genuinely missing, used once (`MiniChampType.cs:314`, Skeletal Dragon). Leaf item.

So the **stock table is fully satisfiable** for 1 leaf port + 7 renames. Note pinned already
places the Abyss mini-champ creatures as **flat** spawners (`D:\UO\ModernUO-pinned\Distribution\Data\Spawns\post-uoml\termur\Abyss.json:118-121`,
`RakktaviRenowned` with the clan rats), i.e. pinned has the creatures but not the staged wave logic.

### Does pinned already have a mini champ? (by behaviour)

- `ChampionSpawn` (`PIN/Engines/CannedEvil/ChampionSpawn.cs`, 1,519 lines) is staged waves ending in a
  champion, but always builds a `ChampionPlatform` and `ChampionAltar` (`:150-151`), does power scrolls
  (`:421`), and a new `ChampionSpawnType` needs an upstream patch: `ChampionTitleContext.cs:40-45` throws
  `NotImplementedException` for any type without a title mapping, and `ChampionSpawnInfo.cs:41` says so.
  Wrong tool for a small dungeon mini champ.
- `GauntletSpawner` (`PIN/Engines/Doom/GauntletSpawner.cs`, 429 lines): one creature type per room,
  count scaled by players (`:279-302`), random traps (`:228-276`), door lock, completes when all dead
  and hands off to `Sequence` (`:379-405`). A chain of rooms, not a multi-type wave ladder with a boss.
  Close in spirit (could fake levels as a sequence of spawners ending on one with `TypeName = BurrowMother`),
  but its spawn count is player-scaled, it spawns at its own location (`:356`), and it is tied to
  `GauntletRegion` (`:168-186`).
- Pinned `Spawner` / `BaseSpawner` (`PIN/Engines/Spawners/`) has no level progression.

Verdict: **no pinned equivalent; MiniChamp is a self-contained, small, near port.**

### Can it end in the Burrow Mother? Yes, with no engine change.

How a type is defined (`MiniChampType.cs`):
- `enum MiniChampType` (`:7-23`), 14 members.
- `MiniChampTypeInfo(int required, Type spawnType)` (`:25-35`); `MiniChampLevelInfo(params MiniChampTypeInfo[])`
  (`:37-45`); `MiniChampInfo(Type essenceType, params MiniChampLevelInfo[] levels)` (`:47-58`),
  `MaxLevel = Levels.Length` (`:52`).
- `m_Table` (`:72-388`) is **positional**: `GetInfo` indexes by `(int)type` and silently falls back to
  entry 0 when out of range (`:390-398`).
- The boss is just the **last level with one entry of count 1**: Meraktus is
  `new MiniChampLevelInfo(new MiniChampTypeInfo(1, typeof(Meraktus)))` (`:383-386`). Renowned types play
  the same role for the others (e.g. `:93-96`).

Defining `BurrowMother` needs: (1) a `BurrowMother : BaseCreature` (the spawner casts with
`as BaseCreature` and dereferences without a null check, `MiniChampSpawnInfo.cs:67,77`; nothing named
Burrow Mother exists in pinned, SV or OURS); (2) append one enum member; (3) append one `MiniChampInfo`
at the **same index** (append-only, because the type is saved as an int, `MiniChampionSpawn.cs:400`);
(4) an essence type or `null` (Meraktus passes `null`, `:366`; the `CreateInstance(null)` throw is
swallowed by the `try/catch` at `MiniChampSpawnInfo.cs:104-105`, so `null` works but by exception).
Better in our port: `EssenceType == null` short-circuit.

Behaviour to know before designing around it:
- Boss level `Required = 1` gives `MaxSpawned = 2*1-1 = 1` (`MiniChampSpawnInfo.cs:16`): exactly one
  Burrow Mother per cycle. Killing her completes the last level, `AdvanceLevel` finds no level, calls
  `Stop()` and schedules restart after `RestartDelay` (default 5 min, `MiniChampionSpawn.cs:128,308-313`).
  **There is no completion reward or event beyond the boss's own loot.** A hook (e.g. virtual
  `OnCompleted`) would be ours to add.
- `BossSpawnPoint`, if set, is used for **every** creature at every level, not only the boss
  (`MiniChampSpawnInfo.cs:72-75`). For "boss appears in her lair" we must change this to apply only on
  the last level (a deliberate, logged deviation) or leave it unset.
- Previous-level creatures are not deleted on level-up; `ClearSpawn` moves them to `Despawns`
  (`MiniChampionSpawn.cs:274-285`), deleted only at `Stop()` (`:206-207, 221-229`).
- Leashing: anything beyond `SpawnRange + 10` is teleported back (`MiniChampSpawnInfo.cs:47-54`);
  default `SpawnRange = 30` (`MiniChampionSpawn.cs:129`). Size it to the cavern.
- Level shouts are hard-wired to Meraktus (`MiniChampionSpawn.cs:298-301, 316-347`); a Burrow Mother
  equivalent would be a per-info cliloc array, our addition.
- On load, an **inactive** controller schedules its own restart (`MiniChampionSpawn.cs:448-451`), so a
  GM `Active = false` does not survive a reboot. ServUO quirk; decide whether to keep it.

### Placement: hard-coded generator, replace it

`[GenMiniChamp]` (`MiniChampionSpawn.cs:13-104`) deletes all controllers in a static `Controllers` list
and recreates 14 at literal Ter Mur / Malas coordinates (`:29-101`). It is not wired into any other
SV command (grep). For New Haven we drop it and place one controller from our own dungeon generator,
registered in OURS `Misc/WeakEntityCollection.cs` (192 lines, already ported; used the same way by
`Services/Revamped Dungeons/DespiseRevamped/Setup.cs:44,73`).

### Serialization

ServUO v0, hand-written (`MiniChampionSpawn.cs:392-413`): `BossSpawnPoint, Active, (int)Type, Level,
SpawnRange, RestartDelay`, count + each `MiniChampSpawnInfo` (`Owner` item, `Killed, Spawned, Required`,
`MonsterType.FullName`, `Creatures`, `MiniChampSpawnInfo.cs:119-127`), then `Despawns`. On load it
restarts the 1 s `SliceTimer` (`:443-447`). ModernUO form: `[SerializationGenerator(0, false)]` on
`MiniChamp` with `[SerializableField]` for those six values plus `List<MiniChampSpawnInfo>` and
`List<Mobile>`; `MiniChampSpawnInfo` becomes a `[SerializationGenerator(0)] partial class` with
`Type`, three ints and `List<Mobile>` (pinned precedent: `PuzzleChestSolution`,
`PIN/Engines/Khaldun/PuzzleChest.cs:23-27`), `Owner` re-linked in `[AfterDeserialization]`.
No ServUO save will ever be imported (assumption, not verified), so no migration JSON is needed.

### Size

| Scope | Files | Lines (SV source) | Upstream patches |
|---|---|---|---|
| Engine only (controller minus `GenMiniChamp` body ~90, spawn info, table classes + our one entry) | 3 | ~400 of 476 + 140 + ~70 of 399 = **~610** | **0** |
| + full stock table (14 types) | +1 leaf (`EssencePersistence`, 62) | +~330 table lines, 7 renames | 0 |
| + `BurrowMother` creature | 1 new | ours to write | 0 |

**Small and near.** Gate is one 17-line helper; all 80 table types resolve. Ships with a test
(subsystem rule, `docs/subsystem-policy.md`): drive levels by deleting creatures, assert the boss
level spawns exactly one `BurrowMother` and the cycle stops.

## 2. Underworld PuzzleRoom (and Maze of Death puzzle)

### Files (wc -l), `SV/Services/Underworld/PuzzleRoom/`

| File | Lines | Role |
|---|---|---|
| `PuzzleBox.cs` | 112 | 3 boxes (`PuzzleType` West/East/North, `:7-12`) hand out a board if you hold the right key |
| `MagicKey.cs` | 151 | world key (never decays) gives a 30-min carried key via confirm gump (`:23-48, 93-132`) |
| `CopperPuzzleKey.cs` | 31 | `BaseDecayingItem`, 1800 s |
| `GoldPuzzleKey.cs` | 32 | `BaseDecayingItem`, 1800 s |
| `MazePuzzleItem.cs` | 215 | `BaseDecayingItem, ICircuitTrap`; circuit gump; shock damage; rewards copper then gold key (`:170-195`) |
| `MastermindPuzzleItem.cs` | 140 | `: PuzzleChest`; on solve gives `ExperimentalGem` (`:98-113`) |
| `PuzzleBook.cs` | 62 | `: BrownBook` with fixed text |
| `PuzzleRoomTeleporter.cs` | 45 | `: Teleporter`, requires `MagicKey` in pack (`:126-140`) |
| **Total** | **788** | |

**No Region.** "In the room" is a hard-coded `Rectangle2D(1089,1162,16,12)` on Ter Mur
(`MazePuzzleItem.cs:45-50`), also gating `MastermindPuzzleItem.OnDoubleClick` (`:40-44`).
`MagicKey.Decay` checks a different rectangle `(1234,1234,10,10)` (`MagicKey.cs:91`, used `:58`), which
does not match the room: looks like a ServUO placeholder bug (not verified in game).
Grep for `Core.|Xml|Points|Quest|Region` over the 8 files: none.

### Dependencies

| Dependency | SV | Pinned / OURS |
|---|---|---|
| `BaseDecayingItem` | `SV/Items/Functional/BaseDecayingItem.cs`, 142 | **Missing in both.** Nearest pinned behaviour: `TransientItem` (`PIN/Spells/Spellweaving/Items/TransientItem.cs:7`, 94 lines; same 1072515/1072517 clilocs `:37,78`) but it is `Nontransferable` (`:24`) and starts its timer in the ctor (`:17-22`), while `MagicKey` needs a timer that starts only on the carried copy (`MagicKey.cs:41-48`). 42 ServUO classes derive from it (none in pinned or OURS), so it is itself a carrier worth porting once |
| `ICircuitTrap`, `CircuitCount`, `CircuitTrapGump` | `SV/Gumps/Traps/CircuitTrap.cs`, 292 | Missing. Built on ServUO's `BaseGump` (`SV/Gumps/BaseGump.cs`, 684), which **collides by name** with pinned's unrelated `Server.Gumps.BaseGump` (`PIN/Gumps/Base/BaseGump.cs:23`). Do not port `BaseGump`; rewrite the gump on `DynamicGump` |
| Circuit puzzle behaviour | | **Pinned has it**: `PowerGenerator` / `ControlPanel` (`PIN/Items/Misc/PowerGenerator.cs:10,41`), gump "Close the Grid Circuit" (`:280-322`), shock damage (`:194-232`). But `Solve` is non-virtual and drops arcane gems/diamond/ore (`:234-260`), gump class is private: reuse as-is, or copy its layout into our `CircuitTrapGump` |
| `PuzzleChest` (Mastermind) | | `PIN/Engines/Khaldun/PuzzleChest.cs:181` (`abstract`, ctor `(int itemID)` `:196`, `Solution` setter `:241`, `LockPick` overridable `:387`, `GenerateTreasure` `:431`). Its `PuzzleGump`/`StatusGump` are `private` (`:575, 786`) and `Singleton` (`:583, 791`), so ServUO's `CloseGump(typeof(PuzzleChest.PuzzleGump))` lines are dropped, not patched |
| `ExperimentalGem` (Mastermind reward) | `SV/.../ExperimentalRoom/ExperimentalGem.cs`, 720 | Missing; it is the Experimental Room subsystem. **Replace the reward** for our dungeon |
| `Teleporter.CanTeleport` | | virtual at `PIN/Items/Misc/Teleporter.cs:186` |
| `PuzzleRoomTeleporter` behaviour | | **Pinned has it**: `TicketTeleporter` (`PIN/Engines/ML Quests/Items/Teleporters.cs:91-141`), `TicketType` + `Message` as GM props (`:93-100`), denies without the item (`:116-136`), consumes only if `ITicket`. Set `TicketType = MagicKey`, `Message = 1113393`. **Zero-port** |
| `BrownBook(bool)` | | `PIN/Items/Books/BrownBook.cs:30` |
| `BaseCreature.TeleportPets` | | `PIN/Mobiles/BaseCreature.cs:3809` |
| World `MagicKey` dispenser placement | XmlSpawner data `D:\UO\ServUO-pub57\Spawns\underworld.xml:1935-1973` | no generator places it; we place it in our generator |
| Room placement | `SV/Services/Underworld/Generate.cs:105-133` (literal Ter Mur coords, via `[DecorateSA]`, `SV/Commands/DecorateSA.cs:39`) | replace with our generator; also replace the eject coords in `PuzzleBox.cs:45-52` and `MagicKey.cs:60-67` |

Behaviour note: `PuzzleBox.OnDoubleClick` teleports a keyless player out but does not `return`
(`PuzzleBox.cs:43-57`), so it then also prints "You do not have the required key". Harmless.

### Size and verdict

| Scope | Files | Lines |
|---|---|---|
| Room items (all 8) | 8 | 788 |
| + `BaseDecayingItem` (carrier) | 1 | 142 |
| + `CircuitTrapGump` rewritten on `DynamicGump` | 1 | ~250-290 (SV 292) |
| - `PuzzleRoomTeleporter` (use `TicketTeleporter`) | -1 | -45 |
| **Total** | **9** | **~1,150-1,180**, 0 upstream patches, reward replaced |

**Medium, near.** Two small gates (`BaseDecayingItem`, circuit gump). Not near if anyone tries to port
ServUO `BaseGump` (684 lines + name collision) or `ExperimentalGem` (Experimental Room subsystem);
both should be skipped. **Zero-port alternative** that covers most of the gameplay: place pinned
`PowerGenerator` (circuit), a `StrongBoxPuzzle` / `MetalGoldenPuzzleChest` (`PuzzleChest.cs:825,835`,
mastermind) and a `TicketTeleporter`. Lost: the key chain (magic key timer -> copper -> gold -> board)
and the decaying boards.

**Maze of Death** (same expansion, "puzzle pieces/box/region"): `SV/Services/Underworld/Maze of Death/`,
7 files, 1,717 lines; `UnderworldPuzzle.cs` 902 (`UnderworldPuzzleItem : BaseDecayingItem` `:8`, own
`UnderworldPuzzleGump : Gump` `:437`), `UnderworldPuzzleBox.cs` 68 (`: MetalChest`), `Region.cs` 372
(`MazeOfDeathRegion : Region` `:11` with a ~350-line literal Ter Mur path table from `:19`). Nothing in
pinned (grep `MazeOfDeath|Maze of Death|Underworld` in pinned .cs: only `LibraryBooks.cs`). The region's
path table is site-specific and would be rewritten for any new layout: **subsystem-sized, skip** unless
the maze is specifically wanted.

## 3. Tomb of Kings chambers

### Files (wc -l), `SV/Services/Tomb of Kings/Chambers/`

| File | Lines | Role |
|---|---|---|
| `Chamber.cs` | 125 | `ChamberInfo` (barrier loc, switch loc, switch id, `:7-22`) + static table of 12 (`:60-77`); `Chamber.Open` drops barrier for 10-15 min (`:106-118`) |
| `ChamberLever.cs` | 117 | 12 levers at literal coords (`:145-162`), randomly bound to chambers |
| `ChamberSpawner.cs` | 148 | corpse-looking item (`0x2006`, `:45-48`); 3-8 of **one** random type from `SilverSerpent, UndeadGuardian, PutridUndeadGuardian` (`:34-39, 79-101`); every 15 min, 50% chance, respawn only if all dead (`:56, 73-77`) |
| `ChamberBarrier.cs` | 102 | visible field + `Blocker` + `LOSBlocker` (`:157-200`) |
| `ChamberSwitch.cs` | 55 | inside switch, also opens the chamber (`:269-285`) |
| **Total** | **547** | |
| (`Generation.cs`, `[GenToK]`, calls `ChamberLever.Generate`, `Chamber.Generate`, `ChamberSpawner.Generate`, `:159-162`) | 168 | not needed |

Design: barriers and switches are **not persisted**; they `Delete()` themselves on load
(`ChamberBarrier.cs:248`, `ChamberSwitch.cs:303`) and `Chamber.Initialize` rebuilds them every boot
from the static table, **re-randomizing which lever opens which chamber** (`Chamber.cs:26-51`).
Everything is literal Ter Mur (`ChamberLever.cs:195`, `ChamberBarrier.cs:193`, `ChamberSwitch.cs:266`).
Grep for `Core.|Xml|Points|Quest|Region`: none.

### Dependencies

| Dependency | Pinned / OURS |
|---|---|
| `Blocker`, `LOSBlocker` | `PIN/Items/Misc/Blocker.cs:9`, `PIN/Items/Misc/LOSBlocker.cs:9` |
| `WeakEntityCollection` | OURS `Misc/WeakEntityCollection.cs` (192) |
| `SilverSerpent` | `PIN/Mobiles/Animals/Reptiles/SilverSerpent.cs:9` |
| `UndeadGuardian`, `PutridUndeadGuardian` | OURS `Mobiles/Normal/UndeadGuardian.cs` (54), `PutridUndeadGuardian.cs` (57) |
| `Map.GetSpawnPosition` | ServUO core; same 17-line helper as section 1 |
| ToK region | Pinned already has `TombOfKingsRegion` (`PIN/Regions/TombOfKingsRegion.cs:5`, light override `:20`) and `ToKBridgeRegion`, registered `PIN/Regions/RegionJsonRegistration.cs:57-58`. The chambers do not use either. No `regions.json` entry naming those types was found by grep (not verified further) |

### Pinned equivalents by behaviour

- **Lever opens a passage, auto-closes**: `RaiseSwitch` (`PIN/Engines/Khaldun/RaiseSwitch.cs:7-60`) +
  `RaisableItem` (`PIN/Engines/Khaldun/RaisableItem.cs:7`, raise `:75-83`, close delay ctor `:33-50`):
  GM-placeable, serialized, raises a blocking item by Z then lowers it after `CloseDelay`. Covers
  "lever opens chamber for N minutes" with **zero port**. Not covered: the energy-field look, the
  random lever-to-chamber mapping, the inside escape switch.
- **Respawn the whole group only when all are dead**: pinned `Spawner` with `Group = true`
  (`PIN/Engines/Spawners/BaseSpawner.cs:85, 966-977`). Not covered: one random type per wave, random
  3-8 count, the 50% roll.
- `LeverPuzzleController` (`PIN/Engines/Doom/LeverPuzzle/LeverPuzzleController.cs`, 733) is a
  combination-lever puzzle **welded to Doom**: static Malas coords (`:61-70`), `[GenLeverPuzzle]`
  (`:195-230`), regions built on `Map.Malas` (`LeverPuzzleRegions.cs:12, 89`). Not reusable elsewhere
  without a rewrite; does not cover chamber gating.

### Size and verdict

Straight port: 5 files, 547 lines, 0 patches, all dependencies resolved. **Small and near**, but the
static-table, rebuild-on-boot design is wrong for a GM-built dungeon. Better: one `ChamberController`
item holding a serialized list of (lever, barrier, switch, spawner) references, built by our generator,
~300-350 lines total. Or use the zero-port `RaiseSwitch` + `RaisableItem` + `Spawner(Group)` set.

## 4. Traps and teleporters already in pinned

All `: BaseTrap` (`PIN/Items/Traps/BaseTrap.cs:7`, step-on and passive range triggers `:37-60`):
`FireColumnTrap` 80 (passive range 3, `:31-34`), `FlameSpurtTrap` 156, `GasTrap` 76 (poison, `:18-31`),
`GiantSpikeTrap` 34, `MushroomTrap` 56 (range 2), `SawTrap` 66, `SpikeTrap` 133 (reset 6 s, `:58`),
`StoneFaceTrap` 133, plus `BaseFactionTrap` (`PIN/Engines/Factions/Items/Traps/BaseFactionTrap.cs:16`).
`GauntletSpawner.SpawnTrap` already randomizes five of them into a rectangle (`GauntletSpawner.cs:228-276`).
None of the three ServUO systems uses a floor trap (the "trap" in `MazePuzzleItem` is the circuit gump),
so there is **no overlap and nothing to port** for traps.

Teleporters, all `: Teleporter` (`PIN/Items/Misc/Teleporter.cs:24`): `SkillTeleporter :310`,
`KeywordTeleporter :425`, `TimeoutTeleporter :642`, `ConditionTeleporter :742` (deny-only flags,
`:1013-1025`), `InteractionTeleporter :1029`, `MLQuestTeleporter` and `TicketTeleporter`
(`PIN/Engines/ML Quests/Items/Teleporters.cs:9, 91`). `TicketTeleporter` replaces
`PuzzleRoomTeleporter`. ToK's `ToKTeleporter.cs` (55) was not examined.

## 5. Summary table

| System | SV files / lines | Port for our dungeon | Patches | Class |
|---|---|---|---|---|
| MiniChampionSystem | 3 / 1,015 | 3 files, ~610 lines (engine + 1 entry); +62 + 7 renames for the stock table | 0 | small, near |
| PuzzleRoom | 8 / 788 | 9 files, ~1,150-1,180 (incl. `BaseDecayingItem`, rewritten circuit gump; teleporter dropped; reward replaced) | 0 | medium, near; zero-port alternative exists |
| Maze of Death | 7 / 1,717 | site-specific region path | 0 | subsystem, skip |
| ToK chambers | 5 / 547 | 5 files 547, or ~300-350 redesigned controller | 0 | small, near; zero-port alternative exists |

## Not verified

- No build was run (read-only task); every "resolves" above is by grep and reading, not compilation.
- `PropertiesGump` constructor signature vs ServUO's `(from, this)` call not checked.
- That the `MagicKey.cs:91` rectangle is a bug is inferred from it not matching `MazePuzzleItem.cs:45`.
- Whether any regions.json places `TombOfKingsRegion`; only a grep of Distribution was done.
- `ToKTeleporter.cs`, `SacredQuestBlocker.cs`, Serpent's Breath and Arisen files were not read.
- The ServUO `Spawns/underworld.xml` entry was read only at the two matching lines.
