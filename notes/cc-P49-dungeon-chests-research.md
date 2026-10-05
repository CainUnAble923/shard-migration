# cc-P49: Dungeon treasure chests and the tameable mimic (F-32), research notes

Notes only. Nothing was built, deployed or committed, and nothing in `D:\ShatteredLegacy` was written.
Written 2026-10-04 by Claude against the prompt `D:\UO\cc-prompts\cc-P49-dungeon-chests-research.md`.

**Engine pin:** `D:\UO\ModernUO-pinned` HEAD is `d4531cd94b739613155225c234900de9f47d2c88`, checked with
`git rev-parse` on 2026-10-04.

**Citation prefixes:**
- "P\" = `D:\UO\ModernUO-pinned\Projects\`.
- "C\" = `D:\ShatteredLegacy\server\customizations\`.
- "S\" = `D:\UO\ServUO-pub57\Scripts\`.

**Scratch files:** `notes\cc-P49-scratch\`.
- `body729_a00.png` is a render of body 729.
- `chests.py`, `regs.py` and `uopanim.py` are the read-only parsers used for the counts and the render.

**Method:** five read-only research passes, one per question group. I then re-read the claims everything rests on
myself:
- the stock chest classes;
- the taming gates and the odds formula;
- the Unlock spell bypass;
- PetMimic's constructor;
- the body 729 render.

**Brief corrections:**
- The brief lists P44 and P35 as queued, and P48 as written. All three are in `cc-prompts\completed\`.
- P34, P36, P45, P50 and P51 are queued.

## Summary

| # | Question | Answer in one line | Biggest risk |
|---|---|---|---|
| 1 | Stock chests | `TreasureChestLevel1-4` are locked, trapped `LockableContainer`s that **decay 15-74 min after spawning, looted or not**; the spawner replaces them 5-10 min later on a random tile. 31 pinned spawn files name them; 26 are Trammel/Felucca. | The shard has a second, different chest family: the ServUO pack `TreasureLevel1-4` with MagicTrap, used by Shame Revamped (116 rows). "One system" has to decide whether it is folded in. |
| 2 | Depth | Regions have no floor concept. Use a shard config `Configuration/dungeon-tiers.json` keyed by map plus region name, with optional floor boxes, modeled on `league-ladder.json`. | Trammel Despise sits in the shard's own `DespiseRegion : BaseRegion` regions, so a lookup by `DungeonRegion` type finds nothing there. Look up by name through all covering regions. |
| 3 | Levels 5+ | Nothing clamps lock or trap checks at 100, so levels 5, 6 and 7 are meaningful (required Lockpicking 110 / 130 / 150). Reuse stock chest art with a hue per level. | **The Unlock spell opens any lock at Magery >= (RequiredSkill + 4) / 0.8, and Magic Untrap clears MagicTrap at any power.** Levels 5+ must block Unlock and never use MagicTrap. |
| 4 | Respawn | A persistent `DungeonChest` that refills itself. The refill is armed on first access, kept in a saved `DateTime`, and clears the contents first. The existing spawners stay as a fallback. | Spawner-driven refill cannot give a 30-60 minute timer per chest: the delay belongs to the whole spawner, and two Despise spawners are never full. |
| 5 | Mimic | No player can get a PetMimic today; F-32 is its only source. `new PetMimic()` is safe. Tame through a 10% subdue gate plus a 2-minute `Tamable` window, then swap creature for item on the next tick. | **The odds formula gives about 0.2% success at Taming 100 when `MinTameSkill = 100`.** The chance has to be set separately from the 100 gate. Pinned has no tame hook. |
| 6 | Icon | PetMimic is always hued 1154 and takes the ItemID of whatever it eats. Use the **partial** set with a tiledata PartialHue record (or the gray set without one). No paperdoll gump is needed. | The icon only shows while the mimic is dormant. No ID could be proposed: `find-free-art.py` and `registry.csv` were refused by the permission classifier in this session. |
| 7 | Clashes | No blocking clash. Need fixing: the P42 `IsChest` prefix test, P50's chest-state contract, P36's region name for the tier table, and P45 companions picking locks. | Renaming spawner entries without updating `ClusterFDespiseStockSpawns.IsChest` makes the import hook strip the renamed chests from Trammel Despise. |

**Feature-queue fact to correct (overseer):** F-32 says body 729 is "probably not chest-shaped" and that "a rock suits
OSI's Mimic body 729". The render shows a **pink king crab** (the genus Paralithodes, hence Paralithode). See
`cc-P49-scratch\body729_a00.png` and section 5.4. The rock icon is still fine for the item; it just does not match
OSI's body.

---

## 1. Stock chests on our engine

### 1.1 What they are

**Class hierarchy**
- `TreasureChestLevel1-4 : LockableContainer : TrappableContainer` (P\UOContent\Items\TreasureChests\TreasureChestLevel1.cs:7,
  same line in 2-4; P\...\Containers\LockableContainer.cs:9; TrappableContainer.cs:16).
- They are not `BaseTreasureChest`. That class is separate (P\...\Containers\BaseTreasureChest.cs:7). It holds the
  `TreasureLevel` enum Level1-6 (:9-17), has gold only, no trap, a lock up to 100, and resets itself on unlock (:46-64,
  :123-140). No spawn file uses it.
- No `DungeonTreasureChest` type exists in pinned, ServUO or C\.

**How `Utility.Random(a, n)` reads:** it returns a to a+n-1 (P\..\Server\Random\BuiltInRng.cs:34). The ranges below
use that rule. One research pass misread L4 gold as 200-400; I re-read the line and it is 200-599.

| | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| Item IDs | crates 0xE3C-0xE3F, 0x9A9, 0xE7E | crates, chests, keg 0xE7F, barrel 0xE77 | wooden 0xE42/3, metal 0x9AB/0xE7C, golden 0xE40/1 | as L3 plus keg |
| Lockpicking needed (`RequiredSkill`) | 57 | 72 | 84 | 92 |
| LockLevel (Req - 1..10) | 47-56 | 62-71 | 74-83 | 82-91 |
| MaxLockLevel (Req + 1..10) | 58-67 | 73-82 | 85-94 | 93-102 |
| Trap | Dart | Explosion | Poison (+Greater poison) | Explosion |
| TrapPower | 1-25 | 2-50 | 3-75 | 40-136 |
| Remove Trap: chance starts / certain | TP / TP+30 | same | same | 40-136 / 70-166 |
| Trap damage (TrapLevel 0, so TrapPower, 3-tile radius, resisted) | 1-25 physical | 2-50 fire | 3-75 poison | 40-136 fire |
| Gold | 30-129 | 70-169 | 180-419 | 200-599 |
| "OSI" gold in the code comments | 25-50 | 80-150 | 250-350 | 500-900 |

Sources:
- Lock and trap lines: `TreasureChestLevelN.cs:15-21`.
- Gold: L1 :33, L2 :32, L3 :37, L4 :38.
- Trap damage: P\UOContent\Items\Containers\TrappableContainer.ExecuteTrap.cs. Explosion :56-80, dart :103-116,
  poison :119-144.

**Lockpicking**
- Refused below RequiredSkill (P\UOContent\Items\Skill Items\Thief\LockPick.cs:121-126).
- Otherwise the roll is `CheckTargetSkill(LockLevel, MaxLockLevel)` (:128), linear between the two
  (P\UOContent\Skills\SkillCheck.cs:178-195).

**Remove Trap**
- Needs Lockpicking 50 and Detect Hidden 50 (P\UOContent\Skills\RemoveTrap.cs:17,21).
- The roll is `CheckTargetSkill(TrapPower, TrapPower + 30)` (:61). Success sets `TrapType = None` (:65).
- At stock L4, 36% of chests cannot be disarmed at Remove Trap 100.

**When the trap fires:** on the open after unlocking (`TrapOnOpen = !TrapOnLockpick`, LockableContainer.cs:13), or
through Telekinesis (TrappableContainer.cs:36-45). The trap is cleared once it fires (ExecuteTrap :49-51).

**Loot (summary; full detail in each file)**
- **L1:** gold, plus a 50% chance each of a 1-3 gem stack, a weapon, armor, clothing and jewelry.
- **L2:** adds reagents, scrolls of circles 1-5 and a potion.
- **L3 and L4:** adds wands, and weapons or armor with old-style magic levels (L3 up to level 2, L4 up to level 3).
  L4 gives stacks of 12 reagents, 16 scrolls and 12 gems.
- The pools come from P\UOContent\Misc\Loot.cs: 9 gems :142-147, 8 reagents :155-160, potions :168-172,
  wands :349-362.
- L4's crystal ball and L1's bolts are not implemented (comments in the files).

**Refill: none.**
- They override `Decays => true` (L1:71, L2:68, L3:113, L4:116) with `DecayTime` = `Utility.Random(15, 60)` minutes.
  That is 15-74, rolled once and not saved (L1:76; a pinned test pins it,
  `UOContent.Tests\Tests\Items\TreasureChests\TreasureChestDecayTests.cs`).
- The override beats the engine default, which would exempt non-movable or spawned items (P\Server\Items\Item.cs:336).
- `DecayScheduler` deletes the chest (P\Server\Items\DecayScheduler.cs:420-426). `Item.OnDelete` calls
  `Spawner.Remove` (Item.cs:3533-3539), which re-arms the spawner (P\UOContent\Engines\Spawners\BaseSpawner.cs:391-404).
- Every chest spawner in the data has minDelay 5:00 and maxDelay 10:00.
- **What a player sees today:** a chest exists for 15-74 minutes whether or not anyone touches it. A new one appears
  5-10 minutes later on a random tile in the spawner's home range. Emptying a chest does nothing.

### 1.2 Where they are placed (counted by parsing the JSON; `cc-P49-scratch\chests.py`)

"Cap" is the sum over spawners of min(count, the chest entries' maxCounts). All of these spawners are `Spawner`,
delay 5-10 min.

| File (`Distribution/Data/Spawns/`) | Spawners | Mixed with creatures | L1 | L2 | L3 | L4 | Cap |
|---|---|---|---|---|---|---|---|
| shared/felucca/Covetous.json | 11 | 4 | 2 | 7 | 8 | 4 | 31 |
| shared/felucca/Deceit.json | 5 | 3 | 0 | 4 | 5 | 1 | 15 |
| shared/felucca/Despise.json | 13 | 2 | 2 | 8 | 8 | 2 | 32 |
| shared/felucca/Destard.json | 8 | 0 | 0 | 3 | 8 | 5 | 23 |
| shared/felucca/Fire.json | 8 | 0 | 0 | 3 | 4 | 1 | 12 |
| shared/felucca/Hythloth.json | 48 | 3 | 14 | 12 | 14 | 9 | 53 |
| shared/felucca/Ice.json | 20 | 0 | 0 | 2 | 8 | 10 | 20 |
| shared/felucca/Outdoors.json | 5 | 0 | 0 | 3 | 5 | 2 | 18 |
| shared/felucca/PrismOfLight.json | 4 | 2 | 0 | 4 | 1 | 1 | 14 |
| shared/felucca/Shame.json | 67 | 0 | 15 | 28 | 19 | 5 | 67 |
| shared/felucca/TerathanKeep.json | 4 | 0 | 0 | 0 | 2 | 2 | 6 |
| shared/felucca/TownsPeople.json | 4 | 0 | 2 | 2 | 2 | 1 | 14 |
| shared/felucca/TrinsicPassage.json | 1 | 0 | 0 | 1 | 1 | 0 | 3 |
| **Felucca, 13 files** | **198** | 14 | 35 | 77 | 85 | 43 | 308 |
| shared/trammel/, the same 13 file names | 198 | 14 | 35 | 77 | 85 | 43 | 308 |
| shared/ilshenar/Ratmancave.json, Rock.json, Wisp.json | 3 | 0 | 1 | 1 | 2 | 3 | 17 |
| post-uoml/{felucca,trammel}/Vendors.json | 2+2 | 0 | `treasurelevel1h` (a C\ type), 4 in all | | | | 4 |

**Totals and gaps**
- 31 files.
- Malas, Tokuno and Ter Mur have no chest entries.
- Ten of the 13 Trammel/Felucca files are dungeons (Covetous, Deceit, Despise, Destard, Fire, Hythloth, Ice,
  PrismOfLight, Shame, TerathanKeep). In those ten: **171 spawners and a cap of 273 chests per facet**.
- Outdoors, TownsPeople and TrinsicPassage are not dungeons. Their chests should stay stock (section 4.5).
- **Dungeons with no chest spawns at all:** Wrong, Orc Cave, Khaldun, Sanctuary, Painted Caves, Blighted Grove,
  Paroxysmus, Misc Dungeons, and the New Haven dungeon (P36).

**Shard data**
- No JSON spawn files exist in D:\ShatteredLegacy outside `server\uo`. The image copies pinned's `Distribution/Data`
  unchanged (`docker\uo\Dockerfile:24-26,97`). The shard imports `post-uoml/**` and `shared/**`
  (C\ClusterFStockSpawnData.cs:17).
- **Shame Revamped** places its own chests from C#: `C\Services\Revamped Dungeons\Shame Revamped\ShameSpawns.cs`.
  - 116 `Shame_Chest` rows, 58 per facet: TreasureLevel1 x10, L2 x24, L3 x19, L4 x5.
  - All count 1, delay 1-2 minutes.
  - `[GenerateNewShame` stops and empties the other spawners in the Shame region (Generate.cs:196-228).
- **Unverified:**
  - whether the stock Shame.json chest spawners are dormant on our world;
  - which import (the console's 12-file fresh-world list at `scripts\Shard-Console.ps1:1314-1321`, or the broader
    `shared/**` import) the current test world used.
  - Counted from files, not from a world.

### 1.3 What P42 Part J (D53) left

The mechanism:
- `server\patches\ImportSpawners-despise-exclusion.patch` calls `ClusterFDespiseStockSpawns.Admit`
  (C\ClusterFDespiseStockSpawns.cs:44-53) for Trammel spawners whose GUIDs are in pinned's `shared/trammel/Despise.json`.
- It keeps entries whose name starts with `TreasureChestLevel` (`IsChest`, :37-38) and strips the rest.
- `[ClusterFDespiseStockCleanup [dryrun]` (:70-164) does the same on existing worlds. The P42 checks file records a
  dry run and a real run both passing (`notes\p42-checks-2026-10-03.md:14-15`).

What is left in **Trammel Despise**:
- 13 spawners, all chests, 20 entries (L1 x2, L2 x8, L3 x8, L4 x2), cap 32.
- The two formerly mixed spawners keep count 7 and 8 with only 2-3 chest slots between them. They are never full
  (this matters in section 4).
- Felucca Despise (43 spawners, 13 with chests) and the Despise revamp's own spawners are untouched.
- The shard reads pinned's own Despise.json. There is no copy or override.

### 1.4 ServUO pub57, and what OSI players expect

ServUO has **no** `TreasureChestLevel` types. Its spawn XML names `TreasureLevel1-4` from
`S\Items\Containers\TreasureChestMod.cs` (Nerun's pack). ModernUO's JSON looks like a renamed conversion of that XML:
the Felucca mention counts are 35/75/85/43 against pinned's 35/77/85/43. That is my inference, from text counts.

| | ServUO `TreasureLevelN` (also C\'s port, line for line) | Pinned `TreasureChestLevelN` |
|---|---|---|
| Lockpicking needed | 52 / 72 / 84 / 92 | 57 / 72 / 84 / 92 |
| MaxLockLevel | equal to Required, so a pick is certain once allowed | Required + 1..10 |
| Trap | MagicTrap at every level (1 tile, unresisted; **Magic Untrap removes it**) | Dart / Explosion / Poison / Explosion (3 tiles, resisted) |
| TrapPower | 1-25 / 2-50 / 3-75 / 4-100 | 1-25 / 2-50 / 3-75 / 40-136 |
| Gold | 30-100 / 70-100 / 180-240 / 200-400 | 30-129 / 70-169 / 180-419 / 200-599 |
| Life cycle | Deletes itself 2-6 min after first open; never decays unopened | Decays 15-74 min after spawn |

**OSI expectation.** This is general knowledge, not verified from source. Dungeon chests are thief content: locked
and trapped, graded by depth, and refilling on a timer. Pinned's own comments state OSI gold of
25-50 / 80-150 / 250-350 / 500-900. Against those, pinned pays more at L1-2 and less at L4. A player reading a wiki
will expect a chest to be lockable, trapped and graded. That matches the plan.

---

## 2. Depth

### 2.1 What the engine gives

- **No floors.** A region has Name, Map, Parent/Children, Area (rectangles), Priority, ChildLevel, GoLocation and
  Music (P\Server\Regions\Region.cs:202-226). `DungeonRegion` adds only `Entrance`
  (P\UOContent\Regions\DungeonRegion.cs:23). `ChildLevel` is hierarchy depth, not dungeon depth.
- **No z bounds on any Trammel/Felucca dungeon rectangle.** A rectangle without z spans -128..127
  (P\Server\Json\Converters\Rectangle3DConverter.cs, near :153-156).
- **Rectangle index is not a floor index.**
  - Only Ice, Orc Cave, Shame and Terathan Keep have rectangles that line up with floors.
  - Orc Cave's are out of order: rect 2 is level 1.
  - The other 13 Trammel dungeons use one rectangle for every floor.
- **No custom keys in regions.json.** Unknown keys are silently skipped (P\Server\Json\JsonConfig.cs:30-60; no
  `[JsonExtensionData]` on Region). The shipped file already carries dead lowercase `"rune"` keys
  (regions.json:3958, 4124). A `"Tier"` key would load and be thrown away. The shard also does not edit regions.json:
  it comes from the pinned clone.
- **Trammel Despise is a trap.** The shard registers four dynamic `DespiseRegion : BaseRegion` regions (Start, Good,
  Evil, Lower) at priority 51 with no parent (C\Services\Revamped Dungeons\DespiseRevamped\Region.cs:34,51-57;
  DespiseController.cs:178-181, boxes :691-695). Inside them, `Region.Find(p).GetRegion<DungeonRegion>()` returns null.
  The same four boxes are, usefully, a ready-made floor split.

### 2.2 Proposal: a tier table in shard config, with optional floor boxes

The file is `Configuration/dungeon-tiers.json`. It copies the `league-ladder.json` pattern in
`C\ClusterFLeagueRanks.cs`:
- the path (:429-437);
- `LoadOrWriteDefaults` (:702-756), called from `Configure()` (:168-177);
- `JsonDocument` with comments and trailing commas allowed (:549-552);
- a staff reload that refuses a bad file whole (:389-394).

```json
{ "map": "Trammel", "region": "Deceit", "tier": 2,
  "floors": [ { "name": "L3-4", "tier": 3, "x1": 0, "y1": 0, "x2": 0, "y2": 0 } ] }
```

**Lookup**
1. Walk every region covering the point, highest priority first (the sector's region list, P\Server\Maps\Map.cs:1874,
   plus `Region.Contains`, Region.cs:419).
2. Take the first region whose name is in the table.
3. Within it, the first floor box that contains the point wins. If none does, use the region's tier.
4. If no region matches, the chest stays stock and the server logs one warning per spawner.

Walking by name rather than by type makes the Trammel Despise `DespiseRegion` boxes work as floors with no special
case.

**When the tier is read:** at each refill, and it is stored on the chest. A config reload changes the next refill,
never a chest already filled.

**A new dungeon gets a tier with no code change:** add a row naming its region. The region itself must exist. P36
registers New Haven's in code, and P36 has to settle its final name first.

### 2.3 Tier table for review

Scale: 1 = starter, 4 = hardest stock, 5-6 = beyond stock.

**Counts:** 77 `DungeonRegion` entries in regions.json. Trammel 17, Felucca 18 (the Trammel 17 plus Khaldun),
Ilshenar 10, Malas 7, Ter Mur 25, Tokuno 0.

**About the floor splits:** they are judgement plus teleporter anchors from `teleporters.json`. They are not drawn
boxes. Every box needs drawing and an in-client check before it goes into the config.

| Region | Facet | Floors, and how they are known | Proposed tier per floor | Reason |
|---|---|---|---|---|
| Despise | Trammel (shard revamp) | 4 `DespiseRegion` boxes, exact | Start 1, Good 2, Evil 2, Lower 3 | Lower needs a Wisp Orb and holds the boss |
| Despise | Felucca | 3, by y band (about 516-640 / 640-770 / 770-1022) | 1 / 2 / 2 | Lizardmen, ogres, ettins |
| Wrong | T+F | 3, one rect | 1 / 2 / 2 | Low; level 3 slightly harder |
| Covetous | T+F | 3 plus lake, 2 rects that do not match floors | 1 / 2 / 2, lake 2 | Harpies and spiders, a few liches deep |
| Orc Cave | T+F | 3, one per rect (rect 2, 0, 1) | 1 / 1 / 2 | Orc captains and lords deepest |
| Shame | T+F | about 4; rect 1 is one deep section | 2 / 2 / 3, rect 1: 3 | Elementals from the start; revamp bosses |
| Deceit | T+F | 4, one rect | 2 / 2 / 3 / 3 | Undead; lich lords deeper |
| Hythloth | T+F | 4, one rect | 2 / 3 / 3 / 3 | Gargoyles, then daemons |
| Destard | T+F | 3, one rect | 3 / 3 / 3 | Dragons from the entrance |
| Ice | T+F | 3 rects = level 1 plus two lower areas | 2 / 3 / 3 | Frost trolls, then ice fiends and wyrms |
| Fire | T+F | 2, one rect | 3 / 3 | Fire elementals, hell hounds |
| Terathan Keep | T+F | 2 rects (cave, keep) | 3 / 4 | Matriarchs, ophidian knights |
| Khaldun | Felucca | 1 | 4 | Lich lords, puzzle chest |
| Misc Dungeons | T+F | several caves in one rect, not identified | 2 | Needs a box per cave later |
| The Painted Caves | T+F | 1 | 2 | Small ML cave |
| Sanctuary | T+F | 1 | 3 | ML mid |
| Blighted Grove | T+F | 1 | 3, peerless room 5 | Lady Melisande |
| Palace of Paroxysmus | T+F | 1 | 4, peerless room 5 | Chief Paroxysmus |
| Prism of Light | T+F | 1 | 4, peerless room 5 | Shimmering Effusion |
| New Haven dungeon (P36, planned) | Trammel | 1 box 5136-5247 x 1128-1263, map not built | 1 (boss areas 2) | Starter: 45-skill resources, Young limit |

For reference only:
- Malas Doom 5, Doom Gauntlet 5-6.
- Ilshenar, Ter Mur and Tokuno are not proposed. They have no chest spawns today (section 1.2), so tiering them waits
  until someone wants chests there.

### 2.4 From tier to chest level

The spawner's stock level stays the base. Depth adds to it:

| Tier | Level bonus | Stock L4 becomes |
|---|---|---|
| 1-2 | +0 | 4 |
| 3-4 | +1 | 5 |
| 5 | +2 | 6 |
| 6 | +3 | 7 (or 6 if 7 is not built) |

This keeps the stock 1-4 grading inside starter dungeons, so a tier 1 chest is exactly stock. Deeper floors can push
a chest past 4, as decided in F-32 answer 6. The bonus column is a Chase number (section 9).

---

## 3. Levels 5 and up

### 3.1 Skill ceilings, and why level 7 can mean something

**How high players can go**
- Live skill cap is 300 per skill (C\ClusterFSkillCaps.cs:10, re-applied at :106-124; live `modernuo.json:104-106`).
- F-12 plans a cap equal to max level, rising to 200 at loop 21 (`notes\f12-levels-loops-caps.md:3,29-40`). F-26
  uses the same 200.

**Nothing clamps at 100 in either check.** Lockpicking and Remove Trap both go through `CheckTarget`
(SkillCheck.cs:178-195) on the full `Value`.

**What play can reach today**
- Lockpicking gains stop at **140**: the hardest pinned lock is treasure map level 5+, with MaxLockLevel = Required +
  40 (P\UOContent\Items\Containers\TreasureMapChest.cs:198-207). P20 also gives this.
- Remove Trap gains go to TrapPower + 30.
- C\ replaces neither skill. `C\ClusterFSkillGain.cs:77-147` changes gain amounts, not the success roll.

**Level 7 makes sense under a 200 cap.**
- L6's MaxLockLevel 160 opens Lockpicking gain to 160.
- L7's 180 opens gain to 180.
- So the chain 5 -> 6 -> 7 is climbable.

**Recommendation:** build the levels as data rows. Ship 5 and 6, and add 7 when F-12 caps pass about 150.

### 3.2 Three bypasses to close first (all in pinned)

1. **The Unlock spell** opens any lock where `(int)(Magery * 0.8) - 4 >= RequiredSkill`. It sets `Locked = false`
   directly and lowers LockLevel (P\UOContent\Spells\Third\Unlock.cs:64-73). Only treasure map chests above level 2
   are exempt (:67).
   - At our 300 cap, Magery 143 / 168 / 193 opens L5 / L6 / L7.
   - **Fix without a pinned patch:** `DungeonChest` overrides the `Locked` setter (LockableContainer.cs:77) and
     refuses `false` unless it came through its own `LockPick` override (:94) or from staff. The spell then reports
     success while the chest stays locked. That is cosmetic, but it needs a message.
   - The alternative, a one-line patch to :67's exemption, touches an upstream file. Per AGENTS.md, an upstream patch
     needs its alternatives argued first, and the override needs no patch. So: the override.
   - **Should L1-4 also block Unlock?** Stock does not, and fidelity says keep stock, so no.
2. **Magic Untrap** removes a MagicTrap at any power and fizzles on everything else
   (P\UOContent\Spells\Second\RemoveTrap.cs:28-49). **Never use MagicTrap on 5+.** The C\ ServUO-pack chests use it at
   every level, which matters if Shame's chests are folded in (section 7).
3. **Telekinesis** fires the trap from range (TrappableContainer.cs:36-44; LockableContainer.cs:167-182). The blast
   reaches 1-3 tiles, so a caster further away is safe.
   - **Fix:** `TrapOnLockpick = true` (LockableContainer.cs:13,57,99) on levels 5+. The trap fires on the picker, who
     is adjacent.
   - Remove Trap still works while the chest is locked (RemoveTrap.cs has no lock check).

### 3.3 Proposed level table, 1-7

Levels 1-4 are stock lock, trap and loot. The extras in the last rows apply to every level, because F-32 answer 2
says "worth it" for all chests. Those extras are our deviation and go in `docs\fidelity-principle.md` when built.
Every number in levels 5-7 and in the extras is a proposal.

**Lock, trap and Remove Trap**

| | L1 | L2 | L3 | L4 | L5 | L6 | L7 |
|---|---|---|---|---|---|---|---|
| Lockpicking needed | 57 | 72 | 84 | 92 | 110 | 130 | 150 |
| LockLevel / MaxLockLevel | Req -1..10 / Req +1..10 | same | same | same | 100 / 140 | 120 / 160 | 140 / 180 |
| Pick chance at Req | ~50-95% | same | same | same | 25% | 25% | 25% |
| Trap | Dart | Explosion | Poison | Explosion | Explosion, TrapLevel 5 | Poison, TrapLevel 5 (Lethal) | Explosion, TrapLevel 7 |
| Trap damage | 1-25 phys | 2-50 fire | 3-75 poison | 40-136 fire | 50-150 fire | Lethal poison | 70-210 fire |
| TrapPower (disarm starts / certain) | 1-25 (+30) | 2-50 | 3-75 | 40-136 | 100-130 (130-160) | 120-150 (150-180) | 140-170 (170-200) |
| Trap fires on | open | open | open | open | **lockpick** | lockpick | lockpick |
| Unlock spell | works (stock) | works | works | works | **blocked** | blocked | blocked |

Notes on these rows:
- Trap damage with TrapLevel > 0 is (10..30) x TrapLevel for explosion (ExecuteTrap :59-72). Poison strength is
  TrapLevel - 1, capped at Lethal (:126-128). TrapPower then sets only disarm difficulty.
- Stock L4's TrapPower already tops out at 136, which is why L5 starts at 100 and not above it.

**Loot**

| | L1 | L2 | L3 | L4 | L5 | L6 | L7 |
|---|---|---|---|---|---|---|---|
| Gold | 30-129 | 70-169 | 180-419 | 200-599 | 1,000-2,000 | 2,500-5,000 | 5,000-9,000 |
| Standard gems | stock | stock | stock | stock | 3-5 stacks of 8-12 | 4-6 of 10-15 | 5-8 of 12-20 |
| Rare gems (`MiscMLResources.cs:183-295`) | - | - | - | - | 25% for 1 | 1, plus 25% for a 2nd | 1-3, WhitePearl and BrilliantAmber allowed |
| Magic items | stock (old magic levels) | stock | stock | stock | 3-4, props 2-4, intensity 20-70 | 4-6, props 3-5, 30-100 | 6-8, props 4-5, 50-100 |
| Currency (section 3.5) | 1-2 | 2-3 | 3-5 | 4-6 | 5-10 | 10-20 | 20-35 |
| Rare-table roll (section 3.6) | 0.5% | 1% | 2% | 3% | 5% | 10% | 20%, plus the artifact list |
| Mimic odds | 1 in 1000 | 1 in 600 | 1 in 400 | 1 in 250 | 1 in 200 | 1 in 150 | 1 in 100 (floor) |

**Gold anchors:**
- `BaseTreasureChest.cs:116-117`: its Level5 is 1,200-5,000 and Level6 is 5,000-9,000.
- `TreasureMapChest.cs:213`: level x 1,000.

I smoothed the step up from stock L4 (200-599): the L5 figure is an economy call for Chase.

**Mimic odds:** levels 1 and 4 and the floor are Chase's (F-32 answer 9). L2, L3 and L6 are interpolated by me.

### 3.4 Magic items within caps

- **Base item:** `Loot.RandomArmorOrShieldOrWeaponOrJewelry()` (Loot.cs:668).
- **Properties:** `BaseRunicTool.ApplyAttributesTo(item, false, luckChance, props, minInt, maxInt)`, the route
  treasure map chests already use (TreasureMapChest.cs:232-284).
  - Caps sit in each property's range in BaseRunicTool.cs. Examples: WeaponDamage 50 :398, SpellDamage 12 :1047,
    resists 15 :773.
  - `Scale` (:78-113) maps intensity onto those ranges, leaning low. **The minimum intensity is the lever.**
- **Do not** go through `LootPackEntry.Construct`. It reads `from.Region` and `from.Map` (LootPack.cs:647), and a
  chest filling itself has no mobile.
- **Luck:** generate on the successful `LockPick(from)` and pass `LootPack.GetLuckChance(from, null)` (:64-90).
- `RandomItemGenerator` and `RunicReforging` do not exist in pinned, and C\ dropped RunicReforging
  (C\Items\Containers\BaseTreasureChestMod.cs:9-12).
- **Correction to the brief:** "cc-P25 sweep D section F" is the PetMimic stat feed, not item caps. Item ceilings are
  the BaseRunicTool ranges above, and imbuing's 8, or 15 at top guild standing (C\ArtificersImbueGump.cs:182-195,
  1667-1674). P25's decisions removed stat ceilings and added no item caps.

### 3.5 Shard currencies

**There is no currency item.** Every guild currency is a per-character number,
`CharacterGuildData.GuildCurrency` (C\ClusterFAccountData.cs:623; `AddCurrency` :750). So a chest cannot drop
currency as loot. The two choices:
- **(a)** Credit the picker directly on a successful pick.
- **(b)** A new bearer item, for example a "Guild Writ", that credits whoever uses it.

**Recommendation: (b).** It can be traded and party-split, and it shows up in the chest like loot. It is one small
new item, and the build should check C\ for name collisions.

17 guilds are registered at C\ClusterFGuildSystem.cs:105-275.

| Guild | Currency | Earned today | Fits a dungeon chest |
|---|---|---|---|
| Thieves' Den | scrip | Apprentice task only (+10) | **Best fit** (Lockpicking, Remove Trap) |
| Warriors' Brotherhood | scrip | Apprentice task only | Yes |
| Rangers' League (Outriders) | Trail Marks | contracts | Yes |
| Arcane Society | scrip | Apprentice task only | Yes |
| Keepers of the Last Door | scrip | Apprentice task only | Yes |
| Twin Paths Dojo | scrip | Apprentice task only | Yes |
| League (per account) | Renown (`GrantRenown`, ClusterFAccountData.cs:516) | achievements | Yes, but needs a new `RenownSource` and a rank-counting decision |
| Artificers' Order | Essence Shards | imbuing, orders | Borderline. Imbuing ingredients fit chests better than its currency |
| Smiths, Miners, Foresters, Tailors, Tinkers, Healers, Bards, Maritime, Merchants | Seals, Vouchers, Timber Tokens, scrip | crafting and contracts | No (crafting or service guilds) |
| Custodians | none | | No |

**Proposal:** Thieves' Den scrip every time, plus one roll on {Warriors, Rangers, Arcane, Keepers, Dojo}.

**Caveat:** generic scrip is spent today only on starter item replacements, at 10 each
(C\ClusterFGuildStarterPath.cs:263,500). Chests would be the first real income for five guilds that have nothing yet
to spend it on.

### 3.6 Rare-drop table

Every class below was checked to exist.

1. `TreasureMap(level, map)` (P\UOContent\Items\Maps\TreasureMap.cs:63). Level 4-5 from L5 chests, 5-6 from L6-7.
2. `Lockpicks`, the decorative rare (P\...\Items\Special\Rares\Tinker\Lockpicks.cs:9). A Thieves trophy.
3. `DecoMagicalCrystal` (...\Rares\Magic\DecoMagicalCrystal.cs:9).
4. `DecoCrystalBall` (...\Rares\Magic\DecoCrystalBall.cs:9). Stock L4 lists "crystal ball (not implemented)".
5. `DecoWyrmsHeart` or `DecoDragonsBlood` (...\Rares\PaganReagents\).
6. `DecoGoldIngots` (...\Rares\Ingots\DecoGoldIngots.cs:9).
7. `MessageInABottle` or `SOS` (...\Skill Items\Fishing\Misc\).
8. `ScrollofAlacrity(Lockpicking or RemoveTrap)` (...\Special Scrolls\ScrollofAlacrity.cs:13).
9. `ScrollofTranscendence(skill, value)` (...\ScrollofTranscendence.cs:13). L6+ only.
10. L7 only: one roll on `TreasureMapChest.Artifacts` (TreasureMapChest.cs:87), or C\'s `KingsGildedStatue`
    (C\Items\Artifacts\Decorative\GildedStatue.cs:16).

**Avoid:**
- `PowerScroll`: F-12 reserves it for champions, paragons and bosses as the level-cap raiser.
- `StatCapScroll`: `ClusterFStatCaps` rewrites the cap at login, so the scroll would be lost.
- The veteran dye tubs: blessed veteran rewards.

**Also a loot hook:** F-12 lists treasure chests as a source of Awakening Scrolls (feature-queue near line 1134).
Add that when F-12 builds it.

### 3.7 Art for 5+: reuse stock chests with a hue

**Stock IDs and container gumps**
- Wooden 0xE42/0xE43 (gump 0x49).
- Metal 0x9AB/0xE7C (0x4A).
- Golden 0xE40/0xE41 (0x42).
- Keg 0xE7F (0x3E).
- Barrel 0xE77 (0x3E).
- Crates 0xE3C-0xE3F, 0x9A9, 0xE7E (0x44).

**Hue precedent:** pinned already hues stock chests. `ParagonChest` picks from 11 hues (ParagonChest.cs:16-17,28).

**Proposal**
- L5-7 use the metal and golden chests with one hue per level (for example L5 dark metal, L6 blood red, L7 an ore
  hue), plus a name such as "a deep-delve chest".
- **No new art, so no P26 cost.**
- New art would be item tiles through P26 (registry row, PNG, records; P26 shipped one item at 44 PNGs plus a
  launcher tiledata patch). It covers no container gump art.

**Unverified:**
- The open-container packet carries no hue (P\Server\Network\Packets\OutgoingContainerPackets.cs:108-123). Whether
  TazUO hues the opened gump from the item is unchecked.
- A level-7 chest that looks exactly like a level-5 one apart from hue is acceptable only if hues are distinct in
  play. That needs a client check.

---

## 4. Respawn on a looted timer

### 4.1 Why the spawner cannot do it

**How a spawned item leaves the spawner's list**
- Deleted (Item.cs:3533-3539).
- Lifted (P\Server\Mobiles\Mobile.cs:5110-5114). Chests are `Movable=false`, so only staff can lift one.
- Stacked by drag-drop (Item.cs:2516-2526).
- Lazily, in `OnDefragSpawn`, when the item is deleted, has no Spawner, has a Mobile root, is locked down, or is
  secure (BaseSpawner.cs:810-823).
- Moving an item with `[move` or onto `Map.Internal` does **not** unlink it.

**Why the spawner's timer does not fit**
- **The delay belongs to the spawner, not to a chest.** `Remove()` re-arms only if the spawner is running, not full,
  and its timer is not already running (:391-404). `OnTick` spawns one item and re-arms (:829-848).
- A spawner with count above 1 cannot give "30-60 minutes after *this* chest was emptied".
- The never-full Despise spawners (count 7 and 8, with 2-3 chest slots) tick for ever, so a removal never restarts
  their timer.
- Raising MinDelay and MaxDelay to 30-60 also slows creatures on mixed spawners. Felucca keeps mixed spawners in
  Covetous, Deceit, Despise, Hythloth and Prism.
- The respawn tile is random within the home range (:424-581). That breaks "the chest comes back where the mimic
  was" (P50).

**What it does well**
- A restart is safe: `_end` is saved, and `RebuildSpawned` re-arms with `_end - now` (BaseSpawner.cs:132-135;
  BaseSpawner.Entries.cs:155-171).
- Each respawn is a fresh object, so junk goes with it.

### 4.2 Recommended: a persistent `DungeonChest` that refills itself

**What the spawner does under this design**
- The spawner places the chest once, then stays full, because nothing unlinks an unmoved item that is not locked
  down.
- If the chest is ever deleted, the spawner replaces it, which gives a free safety net.
- `Decays => false` ends the stock 15-74 minute rotation.

**Precedents in pinned**
- `FillableContainer` (P\UOContent\Items\Containers\Fillable Containers\FillableContainer.cs): a saved timer
  (`[DeserializeTimer]`, :9-13), armed on `OnItemRemoved` and `LockPick` (:97-106), re-lock and re-trap in `Respawn`
  (:139-176).
  - **Do not copy its top-up:** it fills to a threshold and never clears (:178-190), so junk left inside reduces the
    refill.
- `BaseTreasureChest`: arms on unlock (:46-64) and does `ClearContents` then regenerate (:123-140).
  - **Do not copy its unsaved token:** it re-rolls the full delay on every restart (:70-77, :100-106).

**What "emptied" means: arm on first access after a refill.**
- First access is any of:
  - an `Open` or `OnTelekinesis` that gets past the lock;
  - the `Locked` setter going false (lockpick, staff, and the Unlock spell where it is allowed);
  - `OnItemRemoved` with `Items.Count == 0`.
- Arming is idempotent.

**Why not the alternatives**
- "Last item taken" is blocked by junk or by partial looting, and the chest goes stale for ever.
- "Trap disarmed" misses everyone who never disarms, and there is no virtual for it (RemoveTrap.cs:65).
- "Gold taken" is arbitrary.

**The edge cases**

| Case | Handling |
|---|---|
| Server restart mid-timer | Save `DateTime _nextRefill` (MinValue = not armed). In `[AfterDeserialization]`, re-arm with `max(0, _nextRefill - now)`, the spawner's own `_end` pattern. Downtime counts. (`[DeserializeTimer]`'s downtime handling is in the generator package and unverified.) |
| Junk left inside to block the refill | `Refill()` runs `ClearContents()` first, so junk cannot block it. |
| Players dropping items in | Override `TryDropItem` (LockableContainer.cs:107) and `OnDragDropInto` (:118) to refuse non-staff players, so the chest cannot be used as storage and nobody loses an item to the clear. |
| Staff moves the chest | `OnLocationChange` updates the saved home tile (Item.cs:4446; FillableContainer precedent :78-82). The initial home is captured in `OnAfterSpawn` (Item.cs:1613). |
| Staff lifts the chest | `Mobile.Lift` unlinks it from the spawner, which places a replacement. The lifted chest stops refilling (next row). |
| Locked down, secured, in a pack, or outside a tiered region | No refill. Guard: `IsLockedDown`, `IsSecure`, `RootParent != null`, or no tier found. The spawner already drops locked-down items (BaseSpawner.cs:816). Without the guard, a GM-given chest is an endless loot source. |
| Houses | Dungeon regions forbid housing (`DungeonRegion.cs:25`), so only staff could put one in a house, and the guard covers that. |

**Timer length:** a random 30-60 minutes per arm (overseer default). Chase number.

**Code shape (draft, for the builder)**
```
DungeonChest : LockableContainer      [SerializationGenerator(0)]
  saved: int _stockLevel; int _level; DateTime _nextRefill; Point3D _home; Map _homeMap;
         bool _isMimic; ChestMimic _mimic
  Decays => false; IsDecoContainer => false
  OnAfterSpawn / OnLocationChange -> _home
  Refill(): ClearContents; tier lookup -> _level; roll lock/trap/loot/mimic by _level; Locked = true;
            TrapOnLockpick = _level >= 5; MoveToWorld(_home) if internal; _nextRefill = MinValue
  LockPick(from) / Open / OnTelekinesis -> if _isMimic: Spring(from) else base + ArmRefill()
  Locked setter -> block Unlock-spell false at _level >= 5; false -> ArmRefill()
  OnItemRemoved -> Count == 0 -> ArmRefill()
  TryDropItem / OnDragDropInto -> staff only
  [AfterDeserialization] -> re-arm; self-heal if internal with no live mimic and nothing armed
```
The constructor does the first `Refill()`.

**Loot is generated at refill time.** The section 3.4 luck pass could move it to the first successful pick for levels
5+. I would keep refill-time generation for simplicity and drop luck. Decision in section 9.

### 4.3 Converting the stock spawners

The spawners name `TreasureChestLevelN`. Their entries become `DungeonChest` with a properties string such as
`StockLevel N`. Two places do the rewrite:
1. **At import:** extend the existing hook, `ImportSpawners-despise-exclusion.patch` ->
   `ClusterFDespiseStockSpawns.Admit`, generalized to a chest admit pass.
2. **In existing worlds:** a dry-run-first staff command, which deletes the old stock chests and respawns.

**Scope:** only spawners whose location resolves to a tier. That leaves Outdoors, TownsPeople, TrinsicPassage,
Ilshenar and Vendors stock (and that last one is `treasurelevel1h`).

**Unverified:** whether `SpawnerEntry` exposes a public way to change an entry's name in place. The members are
source-generated. If it does not, remove the entry and add a new one with the same counts.

---

## 5. The mimic

### 5.1 How a player gets a PetMimic today: they cannot

**What I searched:** every file outside `server\uo` that mentions `PetMimic`. There are 23:
- 8 in C\;
- 3 patches (`AOS-pet-mimic-attribute-aggregation`, `Bandage-pet-mimic-targeting`, `BaseWeapon-talisman-durability`);
- 9 migrations;
- 1 test;
- 2 in `docker\uo` (`apply-patches.sh:113`, a comment, and `SERVER.md`).

**Exactly one `new PetMimic(`**, in the test `server\tests\Items\StatBonusLeakVerification.cs:95`. There is no
vendor, loot, quest, craft, reward or spawn source. `SERVER.md:1154` documents only staff `[add PetMimic`.

**Other findings**
- D33's reachability audit covered customization subdirectories only (`notes\reachability-audit.md:38-52`).
  Top-level `PetMimic.cs` was never in scope, so D33 is silent on it.
- `notes\deploy-readiness.md:419` records 3 live instances in a save, presumably staff-made.
- **F-32 is the only source.** Nothing needs comparing.
- `PetMimicPurgePotion` is also staff-only (`SERVER.md:1155`). A player who tames a mimic cannot get a purge potion.
  That is a separate small gap (section 9).
- `SERVER.md:1141-1153,1293` are stale. They describe `customizations/migrations` v0-v2 and a base HP of 10. The
  folder is gone and the default is 100 (C\ClusterFPetMimicSettings.cs:32-33). This is for whoever next touches
  SERVER.md.

### 5.2 The constructor is safe

**Declaration**
- `PetMimic : Item, IAosItem, IWearableDurability`, `[SerializationGenerator(9, false)]` (C\PetMimic.cs:40-41).
- `MigrateFrom` V0-V3, V7 and V8 are in the file (:477-825).
- 9 migration JSONs, v0-v8.

**The constructor** (`[Constructible] public PetMimic()`, :455-473; the only public one)
- Sets weight, name, Blessed, `Layer.Talisman`, `Hue = 1154`, HP = MaxHP, a regen stamp, and empty lists.
- Starts no timer, registers nothing static, and needs no owner.
- `MaxHP` reads a `ServerConfiguration` key that `Configure` already touches.

**Equip effects** apply only in `OnAdded` when the parent is a Mobile (:1025-1036), so `tamer.AddToBackpack(new
PetMimic())` is inert until the player equips it.

**Schema:** nothing changes, because the tame calls the existing constructor.

**Unverified:** how the build emits the current-version (v9) schema file. There is no v9.json in `server\migrations`,
but this task adds no field either way.

### 5.3 Handoff: chest to creature and back

The body route is P50's. This section covers only the swap.

**Spring** (`Spring(from)`, called on the lockpick or open that would have looted)
1. Create the `ChestMimic` at the chest's level and facing.
2. `MoveToWorld` it to the chest's tile.
3. `Internalize()` the chest (Item.cs:2689) in the same call.

**Why internalize the chest**
- An item on `Map.Internal` is not defragged (BaseSpawner.cs:814-818). The chest keeps its spawner slot, so no second
  chest appears mid-fight.
- Internalizing beats hiding in place (`Visible = false`): area effects and targeting cannot reach it.

**Back to a chest**
- When the mimic dies, is tamed or is deleted by staff, its `OnAfterDelete` calls `chest.OnMimicGone()`.
- That clears the chest, sets `_isMimic = false` and arms the normal 30-60 minute refill.
- `Refill()` puts the chest back on `_home`.

**Restarts:** both objects hold saved references to each other. The chest's `[AfterDeserialization]` self-heals if
its mimic is gone.

**Spawn the creature only at spring time, never as a hidden proxy.** A pre-placed mobile would show its F-14 level
or con colour and give the chest away.

**For P50:** P50 asks F-32 to store the chest's type, level, location and facing. With this design, the internalized
chest *is* that record. `ChestMimic` needs only a saved `SourceChest` reference and the delete callback. P50's
"nothing left behind after death, delete or restart" check must allow for the internalized chest.

**Unverified:** whether a client sees a frame with both objects, or neither, during the same-tick swap. P50 Part A
measures this.

**Odds**
- **The roll happens at refill**, stored as `_isMimic`, with odds by `_level` from the table in section 3.3.
- Rolling at refill rather than at open has the same odds per cycle. It is testable, staff can see it with `[props`,
  and it cannot be re-rolled by repeatedly opening a chest.
- The odds table lives in config beside the level rows, so the curve is tuned without a build.

### 5.4 OSI's Mimic (background)

**ServUO `S\Mobiles\Normal\Mimic.cs` (97 lines)**
- Body 729, AI_Mage, FightMode.Closest.
- Str 281, Dex 140, Int 261, 543 hits, damage 13-20 split 20% across all five types.
- Resists 63/43/36/37/42.
- Magery 107.5, Resist 126.5.
- PackReg(20), FilthyRich x4 plus MedScrolls, 3% LuckyCoin.
- Not tameable.

**Paralithode** (`S\Services\ExploringTheDeep\Mobiles\Paralithode.cs`, 208 lines) shares body 729. It is tameable at
47.1 with 4 slots, and has an `OnAfterTame` override.

**Pinned has neither class.** `Distribution\Data\bodyTable.cfg:971` lists `729 Monster # Mimic`.

**Port size:** small, about 60 lines in ModernUO style. Every dependency resolves:
- `LootPack.FilthyRich` (P\UOContent\Misc\LootPack.cs:504);
- `LootPack.MedScrolls` (:44);
- `PackReg` (P\UOContent\Mobiles\BaseCreature.cs:5689);
- `LuckyCoin`, which is ours at C\Items\Quest\LuckyCoin.cs:7.

It would be a fidelity port, separate from the chest mimic, and nothing in F-32 needs it. It also gives P50 its level
4 reference stats.

**Body 729 in the client files**
- `mobtypes.txt:1025` (`729 MONSTER ... # Mimic`).
- `Bodyconv.def:469` maps it to the anim5 (Mondain) column.
- It is stored in `AnimationFrame3.uop`.
- Rendered read-only (`cc-P49-scratch\uopanim.py`, frames in `body729_a00.png`): **a pink king crab with long legs
  and claws.** It is not a chest and not a rock.
- **So OSI's body does not fit "the chest changes into the monster".** That confirms F-32's choice of Archaaz's chest
  art through P50.

### 5.5 The tame

**Gates in pinned `AnimalTaming.cs`, in order**

| Line | Gate |
|---|---|
| :129 | `Tamable` |
| :136 | `Controlled` |
| :143-162 | gender, and the CuSidhe race rule |
| :164 | follower slots |
| :170 | MaxOwners |
| :177 | `MustBeSubdued` |
| :184 | skill >= `MinTameSkill` (or mastery) |
| :203 | already being tamed |
| :208-235 | anger roll, only if `CanAngerOnTame` (default false, BaseCreature.cs:1061) |

**Which of these we can override**
- `Tamable` is a serialized property and **not virtual** (BaseCreature.cs:1286).
- `MinTameSkill` is a generated serialized field.
- `SubdueBeforeTame` is virtual (BaseCreature.cs:963). `MustBeSubdued` then requires hits below 10%
  (AnimalTaming.cs:43-44).

**Proposed window (no patch)**
1. `ChestMimic` sets `SubdueBeforeTame => true`. The stock 10% gate and the stock "beaten into subjugation" message
   (BaseCreature.cs:1882-1886) come with it.
2. `Tamable = false` at spawn. When hits first drop below 10% (an `OnDamage` override), set `Tamable = true` and start
   a 2-minute timer that sets it back to false.
3. The tame tick re-checks `Tamable`, so a window that lapses mid-attempt aborts (AnimalTaming.cs:307-314).
4. **Reset `Tamable = false` in `[AfterDeserialization]`.** It is saved, so a save during the window would otherwise
   bring the creature back tameable with no timer.

**The odds trap**
- Success is `CheckTargetSkill(AnimalTaming, minSkill - 25, minSkill + 25)`, with minSkill = MinTameSkill + 6 x owners
  + 24.9 (AnimalTaming.cs:396-406).
- With `MinTameSkill = 100`, the range is 99.9..149.9. **Success at 100 skill is about 0.2%, and 40% at 120.**
- So the "Animal Taming 100" requirement and the success chance must be set separately. Two ways:

| Option | How | Cost |
|---|---|---|
| **(a) Recommended** | `MinTameSkill = 100` keeps the hard gate at :184. The shard's existing `ClusterFSkillGain` wrapper of `SkillCheckTargetHandler` (C\ClusterFSkillGain.cs:35-46,77-87) substitutes a set chance when the target is a `ChestMimic`. | No patch; it reuses a seam we already own. |
| (b) | `MinTameSkill = 75` gives 50% at 100. The 100 gate then moves into an `OnDamage` or `Delta` check that refuses tamers below 100. | Clumsier; the refusal comes after the attempt starts. |

**Proposed chance:** 25% at 100, plus 1.5% per point above, capped at 75%. Chase number.

**Hand out the item, not a pet**
- A successful tame runs `Owners.Add`, `SetControlMaster(tamer)` (BaseCreature.cs:3748-3795), then sets `IsBonded`,
  `ControlTarget` and `ControlOrder` (AnimalTaming.cs:432-446).
- **There is no `OnAfterTame` or `OnTamed` hook in pinned**, and `SetControlMaster` and `OnControlledChange` are not
  virtual.
- **Without a patch:** override `Mobile.Delta(MobileDelta)` (virtual, P\Server\Mobiles\Mobile.cs:7838), which
  `SetControlMaster` calls at BaseCreature.cs:3790. When `Controlled && ControlMaster != null`, schedule
  `Timer.DelayCall(TimeSpan.Zero, ...)` to:
  1. `ControlMaster.AddToBackpack(new PetMimic())`, or bank it if the pack is full;
  2. send a message;
  3. delete the creature.
- **The delay matters:** :444-446 still write to the creature after `SetControlMaster`.
- On delete, `SetControlMaster(null)` and `Master = null` run (BaseCreature.cs:3672-3690). That releases the tamer's
  follower slots (`RemoveFollowers`, :2625), so the tame never leaves a pet.
- **With a patch:** a virtual `OnAfterTame(Mobile)` called after :446. The D-71 proposal already exists
  (`notes\cc6-creatures-batch4.md:167`, for ServUO creatures). If D-71 is scheduled first, use it, because it is
  cleaner than `Delta`. Otherwise `Delta` needs no patch. Per AGENTS.md, a patch argues its alternatives first; this
  paragraph is that argument for F-32's part.

**`ControlSlots`:** set it to 1. The tamer must have a free slot at target time (:164), even though the slot is
returned a tick later.

**Fail or lapse**
- **Failure:** message 502798 (:450-451). The creature is unchanged and can be retried while the window is open.
- **Any damage to the mimic after an attempt starts aborts it** (`LastDamage > m_StartTime`, :339). That includes the
  party's and pets' damage, so the party must stop hitting it.
- **Lapse:** `Tamable` returns to false and the fight continues to the death. The chest then comes back on the timer.
- The mimic does not flee or heal specially: P50 makes it rooted (`CantWalk`), and its regeneration is P50's stats
  call.
- **Proposal:** one window per mimic. It does not re-open if the mimic heals above 10% and drops again. That keeps
  "2 minutes" literal.

**Who may tame**
- Pinned has no loot-rights, party or damage checks. Anyone with the skill and a free slot may tame, one tamer at a
  time (`m_BeingTamed`).
- **Proposal:** limit the tame to the player who sprang the chest and their party.
  - Implement it in the `Delta` swap: a non-party tamer gets the creature released and deleted with no item, plus a
    message.
  - Better: refuse earlier by keeping `Tamable` true but rejecting non-party tamers in an `OnDamage` or
    target-time check.
  - **Unverified:** the shard may already have a target-time veto seam in `ClusterFRangersSystem`, but see the
    dead-code note below.
  - Chase decides between "party only" and "anyone".

**Dead code found:** C\ClusterFRangersSystem.cs:17-19,50-52 says an "AnimalTaming patch" consults
`HasPeacefulTaming`. No such patch exists in `server\patches` or `docker`, and pinned `AnimalTaming.cs` never
references it. This is a documentation or behaviour gap for whoever owns Rangers, outside F-32.

**Unverified:** the shard's live Animal Taming cap (the global 300 cap suggests nothing lower).

---

## 6. The mimic item icon

**How PetMimic looks today**
- Dormant `ItemID 0xE79`, a vanilla pouch (C\PetMimic.cs:34-36), **always hued 1154** (:37, :462).
- **It changes form:** `ConfirmEat` and `SwitchForm` copy the eaten item's ItemID (:1164-1166, :1197-1199) and re-hue
  it to 1154. Purge does the same (:1419-1420), and so does `PetMimicWeapon.cs:33,76`.
- The layer starts at Talisman, then follows the eaten form's tiledata layer for non-weapon forms (:953-980). Purge
  returns it to Talisman (:1423).
- The doc comment about an `itm_mimic_pouch.png` patcher (:27-31) is stale.

**Which art set: partial, with a PartialHue tiledata record.** UO hues and TazUO's PNG path both hue by indexing the
hue ramp from the texel's gray value (P26 section 1; TazUO `Art.cs:58-151`). Measured at 44 px:

| Set | Pixels | Result under hue 1154 |
|---|---|---|
| color | 992 opaque, 0 gray | repainted in hue 1154, amber lost. Fits only at Hue 0, which would mean changing PetMimic. |
| `mimic_gray_*` | 968 opaque, all exact gray | the whole rock takes 1154. Works with no records. |
| `mimic_partial_*` | 806 gray, 134 colored, 28 near-gray | with the tiledata PartialHue flag (0x40000) only the gray pixels hue, and the eyes and teeth stay amber. **Recommended.** |

**Clean-up for the partial set:** the 28 near-gray pixels will not hue, and could show as speckles. Snap them to exact
gray or to the amber before export. That is a Chase art task, under five minutes in any editor.

**The icon is only the dormant look.** Once the mimic eats anything it takes that item's art. Setting
`DormantItemID` changes new mimics only. Existing instances (3 in the save) keep their saved ItemID unless an
`[AfterDeserialization]` reset is added, as P26 did for the Reset Stone. That is optional.

**Paperdoll: not needed.**
- In TazUO, the paperdoll body draws a layer's gump as tiledata AnimID + 50000 (male) or + 60000 (female)
  (`D:\UO\cc-p40-work\tazuo-3212623f\src\ClassicUO.Client\Game\UI\Controls\PaperDollInteractable.cs:509-560`).
  The Talisman side slot draws the item's static art (`Gumps\PaperdollGump.cs:313,815-930`).
- Today's pouch has AnimID 0 and no gump, so the mimic shows only in the side slot.
- A new tile with AnimID 0 behaves the same way.
- For comparison, OSI talismans 0x2F58-0x2F5B have AnimID 1235-1238 with male gumps only.
- **Unverified in client:** a weapon-form mimic on the Talisman layer probably draws that weapon's gump on the body,
  in addition to the phantom weapon.

**Adding it through P26** (`notes\cc-P26-animated-runestone.md` sections 2, 4.3, 5.2, 13):
1. Pick an ID: `python scripts\find-free-art.py --placeholder --run 1`.
2. Add the row to `player-package\vendor\shattered-legacy-art\registry.csv` first.
3. Put `<decimal id>.png` into `vendor\shattered-legacy-art\art\`. It is an item icon, so use
   `anchor-art-frames.py --bottom-pad 0`.
4. Add a `records.json` tiledata record: name up to 19 characters, Wearable, Layer 9, **PartialHue**, AnimID 0.
5. Mirror any server-relevant flags in the server's in-memory table (`ShatteredLegacyArt`) plus the cross-check fact.
6. Set `PetMimicArt.DormantItemID`.

**No ID proposed.** The brief allows IDs only from `find-free-art.py` output. In this session the run was refused by
the permission classifier, and so was a read of `registry.csv`. The script itself only reads (I read it in full:
read-only opens, no writes). I did not work around the refusal.

**For Chase:** run it, and note that P50 draws from the same placeholder pool. P26's 2026-10-01 scan found
`0x3C01-0x3D11` free, with `0x3C10-0x3C3B` registered since; current state unverified.

```bash
python D:\ShatteredLegacy\scripts\find-free-art.py --placeholder --run 1
```

---

## 7. Clashes

| Against | Finding | Action |
|---|---|---|
| **P36** New Haven dungeon build 1 (queued) | Places **no chests or spawners**. Registers a `DungeonRegion` subclass in code on Trammel, 5136-5247 x 1128-1263, working name "the Burrows beneath Old Haven" (`cc-P36-dungeon-build-1.md:91-111`). Its Young limit (at most 3 attackers) will count a ChestMimic, which is fine. | The tier table needs P36's final region name: add the row when P36 lands. Chests there need new spawners, because no stock data covers it. That is a placement batch after P36's map exists. |
| **P42 Part J / D53** (completed) | `IsChest` keeps entries by the `TreasureChestLevel` prefix (C\ClusterFDespiseStockSpawns.cs:37-38). Renamed entries would be **stripped** by `Admit`. The cleanup command matches by GUID or position and names, so a later dry run could report differently. The count 7 and 8 spawners are never full. | Batch 1 must update `IsChest` (or run the rename after `Admit`) and re-run the P42 dry run as a gate. The never-full spawners stop mattering once chests refill themselves. |
| **Shame Revamped** (C\, live) | 116 rows of ServUO-pack `TreasureLevel1-4` (MagicTrap, delete 2-6 min after open, delay 1-2 min). Not covered by the brief. "One system for every dungeon" conflicts with leaving them. | **Chase decision (section 9):** fold Shame's chest rows into `DungeonChest`, or leave Shame Revamped as its own thing. Recommendation: fold in, because their MagicTrap is cleared by a circle-2 spell. |
| **F-3** Clean Up Britannia | Custodian cleanup takes ground items only (`Parent == null`), skips anything not `Movable`, and skips non-empty containers (C\ClusterFCustodianSystem.cs:116-150). It never touches chests or what is inside them. Monster corpses are eligible (:131), so a ChestMimic corpse is cleanable. | None. Junk handling lives in the chest (section 4.2). |
| **F-24** League dungeon dives | Objectives are gathering, kill limits and an investigation mini boss. No chest objective. | None now. A future "open N chests" objective wants the chest to raise an event on a successful pick: add a static event in batch 1 at no cost. |
| **F-14** creature levels | Levels come from `BaseInstrument.GetBaseDifficulty`, so ChestMimic gets one from its stats with no special case. | Spawn the creature only at spring time (section 5.3), so no level or con colour gives a chest away. |
| **P50** chest mimic monster (queued) | Builds `ChestMimic` (`CantWalk`) and a staff chest-to-mimic method. Asks F-32 for chest state. Draws art IDs from the same placeholder pool as section 6. | P50 stores only `SourceChest` plus the delete callback (section 5.3). Its "nothing left behind" check allows for the internalized chest. Coordinate registry rows. |
| **P45** companion probes (queued) | Probe A3 has a creature pick a lock and remove a trap on a test chest. | Chest hooks must accept a non-player `from`, so a companion can spring a mimic and arm a refill. The tame swap must use `ControlMaster`, not `from`. |
| **P51**, **P34** (queued) | No overlap. A new staff conversion command shows up in P51's hub through `[ShardCommand]`. | None. |
| **F-12** | Lists treasure chests as an Awakening Scroll source. | Loot hook later (section 3.6). |

**Running beside a builder:** these notes edit nothing, so no clash.

---

## 8. Build order

Each batch is small enough for one builder, and each leaves the shard working.

**Batch 1: `DungeonChest`, levels 1-4, self-refill, tiers.**
- `DungeonChest` with stock L1-4 numbers and loot (lifted from the stock files, not re-derived).
- Saved refill timer, clear-on-refill, drop refusal, lockdown guard, `OnAfterSpawn` home.
- `Configuration/dungeon-tiers.json` with lookup and reload. Rows ship for Despise (Trammel boxes, Felucca bands) and
  for every region tiered at region level only (no floor boxes yet).
- Spawner conversion: the import hook, `IsChest` updated, and an existing-world command with a dry run.
- Tests: a refill after the timer, a restart mid-timer, junk cleared, Unlock still works at L1-4 (stock), and a
  locked-down chest does not refill.
- Gate: P42's Despise dry run is unchanged apart from the renamed entries.

**Batch 2: levels 5-6 and "worth it".**
- Level rows in config.
- `TrapOnLockpick`, the Unlock block at 5+, no MagicTrap.
- `ApplyAttributesTo` magic items, gems and rare gems.
- The currency bearer item and its use.
- The rare table.
- The depth bonus.
- Fidelity entry for the L1-4 extras.
- Tests: Unlock refused at L5, the trap fires on the picker, and loot ranges by level (seeded).

**Batch 3: mimic handoff.** Needs P50 Part B's `ChestMimic`.
- The `_isMimic` roll at refill by level.
- `Spring`, internalize, `OnMimicGone`, refill back on the home tile.
- Restart self-heal.
- Tests: no second chest mid-fight, the chest comes back after death or delete, and a restart mid-fight.

**Batch 4: the tame.**
- `SubdueBeforeTame`, the 2-minute `Tamable` window and its reset on load.
- The chance substitution in `ClusterFSkillGain`.
- The `Delta` swap (or D-71's hook if it landed first) to `new PetMimic()`.
- Party-only check if Chase picks it.
- Tests: no pet remains, follower count restored, window lapse, and damage aborting a tame.

**Batch 5: icon and odds and ends.**
- After Chase runs `find-free-art.py` and fixes the 28 pixels: the registry row, the PNG, the PartialHue record, and
  `DormantItemID`.
- Optionally a player source for `PetMimicPurgePotion`.

**Later, separately:**
- Floor boxes for the single-rectangle dungeons (drawn, then checked in the client).
- New Haven's row after P36.
- New spawners for dungeons with none (Wrong, Orc Cave, Khaldun, the ML caves, New Haven).
- Level 7 when F-12 caps pass about 150.
- An OSI `Mimic` fidelity port if wanted.

---

## 9. Numbers and decisions that still need Chase

1. **Refill timer:** 30-60 minutes random per arm (overseer default), or another range.
2. **Depth bonus:** tier 1-2 +0, tier 3-4 +1, tier 5 +2, tier 6 +3 (section 2.4).
3. **The tier table** in section 2.3: every row, especially Destard 3 from the entrance, Khaldun 4, and the peerless
   rooms at 5.
4. **Levels:** ship 5 and 6 now and 7 later (recommended), or 5-7 now.
5. **Level 5-7 numbers:** required Lockpicking 110/130/150, TrapPower ranges, and trap levels (section 3.3).
6. **Gold for 5-7:** 1,000-2,000 / 2,500-5,000 / 5,000-9,000, or the steeper `BaseTreasureChest` anchors.
7. **Extras on L1-4:** currency 1-6 and a rare roll of 0.5-3%. Yes or no, given fidelity.
8. **Currency:** Thieves' scrip plus one combat-guild roll, through a bearer item. Is Renown in or out, and does it
   count toward League rank?
9. **The rare-drop table** (section 3.6) and its chance per level.
10. **Mimic odds at L2, L3 and L6:** 1 in 600 / 400 / 150 (interpolated). L1, L4 and the floor are already decided.
11. **Tame chance at Animal Taming 100:** 25%, plus 1.5% per point above, capped at 75%.
12. **Tame window:** opens at 10% hits (stock subdue). One window per mimic.
13. **Who may tame:** the springer's party only (recommended), or anyone.
14. **Shame Revamped's 116 ServUO-pack chest rows:** fold into `DungeonChest` (recommended), or leave them.
15. **Hue per level for L5-7.**
16. **Icon:** the partial set with a PartialHue record (recommended), or gray. Fix the 28 near-gray pixels. Run
    `find-free-art.py` (refused in this session).
17. **Purge potion:** give it a player source now or later.

## 10. Not verified

- **Live world state.** All counts come from files. I did not check which spawners exist on the test world, whether
  `[GenerateNewShame` has run, or how many characters have Lockpicking or Remove Trap above 110.
- **Floor boxes** for single-rectangle dungeons, the caves inside "Misc Dungeons", and every proposed tier.
- **Client behaviour:**
  - whether the opened container gump is hued;
  - the same-tick chest-to-mimic swap;
  - the paperdoll for a weapon-form mimic;
  - how hue 1154 looks on the partial icon in TazUO.
- **Source-generated members:** whether `SpawnerEntry` can be renamed in place, and how `[DeserializeTimer]` treats
  downtime.
- **Art pool:** that `0x3C01-0x3D11` still has free IDs, and the build's v9 schema output for PetMimic.
- **OSI's actual current chest rules** (general knowledge only).
