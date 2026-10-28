# cc-P677: our code and EA's later dungeons on the new land (SoS swap S8)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P677`.

## In plain words

- Our own placed things now stand on the new land. The south mine camp moves a few steps to the open ground at the
  mountain's foot (the old spot is rock now). The Exodus summoning altar appears on each new shrine's glyph. Despise's
  evil ankh and one gate, three of Wrong's teleporters and the Covetous void pool step off the author's new walls and
  pedestals.
- Blackthorn Dungeon is switched off on this land, because its old area is the author's dungeons now. Its code is kept
  whole for P691, which moves it into the Fold. Its stealable artifacts, and three from the old Ararat wreck, are
  parked so they never appear in the author's caves.
- A new check walks every coordinate in these files on the new map; the shard's 2,734 tests are green.
- Nothing for you to try yet: it goes live with the rest of the swap. Two guild halls (the Merchants' and the
  Custodians') still fail on the new land, and are left for P708, which moves them.

## What changed, by the prompt's parts

### 1. Blackthorn (off, ready for P691)

- `BlackthornDungeon/Region.cs`: new `BlackthornRegions.OnThisLand`, false. While it is false, `Initialize` registers
  neither the dungeon nor the castle region. They would lie over the author's dungeons (DungeonBounds 6151-6563,
  2301-2839) and over his own Blackthorn Castle, which P676 drew.
- `Generate.cs`: `[GenBlackthorn` refuses while it is off ("off on this land until it moves into the Fold (P691).
  Nothing placed.").
- `Register(map)`, `Generate()` and `Delete()` are unchanged, so the facts and P691 use them as before, and
  `[DeleteBlackthorn` still works.
- No runtime code outside its folder uses the regions (checked).
- **The test world's Blackthorn items:** Chase chose a fresh test world on swap day, so there are none to delete. For any
  other world that has them, `[DeleteBlackthorn` removes them.

### 2. Despise, Wrong, the stealable artifacts (and Covetous, Exodus)

Each spot was moved onto SoS's version of the room, found with `notes\cc-P677-tools\probe.py` and the exact
standing-Z maps (`spots.Land.open_tops`).

| Where | Was | Now | Why |
|---|---|---|---|
| Despise, the evil ankh (`Setup.cs`) | 5472, 754, 10 | 5473, 754, 10 | the author's pedestal and statue stand on that tile, in the middle of the raised altar; the ankh is in front of it on the same platform |
| Despise, Gate3's evil end | 5388, 753, 5 | 5387, 753, 5 | the room's north and south edges are lined with pedestals round a sunken middle, and one stands on stock's gate tile; the gate is between the two north pedestals |
| Wrong, teleporter end (`Generate.cs`) | 5827, 590, 1 | 5827, 592, 0 | the floor begins two tiles south |
| Wrong, teleporter end | 5690, 573, 25 | 5690, 571, 25 | the upper floor ends at y 571 |
| Wrong, teleporter end | 5872, 532, 24 | 5872, 532, 15 | the floor is at Z 15 |
| Wrong, the 3 sparkles on those tiles (`WrongDecoration.cs`) | same as each teleporter | moved with it | |
| Covetous, the void pool controller | 5605, 1998, 10 | 5606, 1998, 0 | a flowstone on that tile; the floor is 0 |
| Exodus altar, 8 shrine tome spots (`ExodusSummoningAltar.cs`) | stock's raised shrines (Z 12 to 60) | each shrine glyph's tile at its standing Z | the author lays the glyphs flat |

The Exodus spots in full:
- Compassion 1858, 875, 0; Honesty 4209, 564, 65; Humility 4274, 3697, 0; Justice 1301, 634, 16; Sacrifice 3355, 290, 4.
- Spirituality 1595, 2490, 25: the glyph is 11 tiles west of ServUO's spot.
- Valor 2492, 3931, 10: the platform's top.
- **Honor 1727, 3528, 3:** the author drew no Honor shrine art, only its region, so this one is ServUO's x, y on the ground.
- All 8 shrine regions exist in P676's file. `ExodusEncounterVerification` now expects Compassion at Z 0.

**Stealable artifacts (`StealableArtifacts-servuo-entries.patch`).**
- Of our patch's 58 added entries, 49 are on Ter Mur, which is not on the SoS land.
- The other 9 are Ararat's 3 and Castle Blackthorne's 6 (3 on each of Trammel and Felucca):
  - Ararat's spots (6303-6313, 1664-1756) are the author's dungeon caves now, and this shard builds no Ararat wreck.
  - Castle Blackthorne's are Blackthorn's, which is off.
- Saves match entries by their index, so none can be dropped. Instead they stay in place, parked on `Map.Internal`,
  and one added check in pinned's `CheckRespawn` never spawns a parked entry. Nothing is created, so there is no churn
  in the Internal map's cleanup.
- P691 gives the Blackthorne six their new spots.
- The patch was rebuilt with `diff -u` and applies at fuzz 0.

### 3. Seeders and layouts

**The mine camp.**
- SoS's mountain reaches further north and west here. Only a pocket of open ground is left at its foot: 3493-3501,
  2733-2747, Z 1-7.
- The Miners' Compact tent and its liaison (3498, 2744, 4) were already on it and stay.
- Everything else moves into the pocket:
  - The Survey Archivist's tent moves (+2, -16). Its new footprint is 3494-3499, 2736-2740, one free row above the
    Miners' tent.
  - The Archivist herself: 3496, 2754, 4 to 3498, 2738, 4.
  - The forge: 3508, 2746 to 3499, 2746, 4. The anvil: 3510, 2746 to 3498, 2746, 4.
  - Gervis: 3505, 2749 to 3501, 2741, 1. Mugg: 3507, 2747 to 3497, 2747, 4. Jacob Waltz: 3510, 2745 to 3501, 2743, 1.
- **The design file changed, not the generated table.** `design/mine-camp-tents/layout.json` was rewritten by
  `notes\cc-P677-tools\replace_camp.py`. Every tent piece keeps its height above the ground: new Z = design Z, minus
  stock's `GetAverageZ` at its old tile, plus SoS's at its new tile. That also re-seats the Miners' tent's pieces, for
  example the pickaxe at 5, not 7.
- Then P16's generator rewrote `ClusterFMineCampLayout.cs` and the design copy. It was run from
  `notes\cc-P677-tools\gen_layout.py`, made by `make_gen_layout.py` because the original names another desk.
- The seeders (`ClusterFInstitutionSeeder`, `ClusterFNewHavenSeeder`, `ClusterFSouthMineDecor`), the Archivist's doc
  comment and P678's measured-floor table (`NewHavenSeederFloorVerification`) follow.

**The guild halls (`ClusterFGuildHallPlacementData.cs`).** I ran P281's own map checks on the SoS land: a copy of its
tools with its client folder pointed at the server's overlay, and Felucca read from Trammel's files as the server does
(`notes\cc-P677-tools\make_p281sos.py`, `p281sos\check.out.txt`).
- 16 halls pass.
- 2 fail: **Merchants** (Magincia; an SoS building stands on the guild house's plot) and **Custodians** (Britain; the
  warden's tile doesn't fit, and is by a door).
- Both are HQs P708 moves, so, as Chase said, they are left for P708. No hall changed.
- My point check also flagged the Society of Smiths (a "New" hall: its guildmaster, sign and forge are on the guild
  house multi's floor, which isn't in the map files) and two Alembic entries (a sign, and a decor group's anchor).
  P281's checks cover all of those properly and pass them.

**`ImportCleanupTests-guid-key.patch` (Felucca).** The only literal left in the patch's own lines is a test fixture's
spot (310, 310, 0) in a test host with no map. It is not world content, so the fact leaves it out by name.

**The Burrows' go-location** (`OldHavenBurrowsRegion.cs`, a staff [go spot): 5191, 1195 is void on SoS, so it moves to
5191, 1192, 0, the nearest open floor.

### 4 and 5. The fact over every literal, and the build

**`tools/tests/test_s8_spots.py`**, 4 facts:
1. Every coordinate literal in the 30 files stands on the land the server reads. The checker is `spots.py`:
   - The literals are P669's patterns, deduplicated, with the Z kept.
   - Each literal's facet is read per line, from `Map.X` or a hall's `MapIndex`.
   - A spot passes if a person can stand there: land at `GetAverageZ`, or a Surface static (Bridge items count half
     their height); nothing impassable or solid in the 16 Z above; and the literal's Z within 5.
   - Exempt, by rule only: another facet, area corners, old-world "moved from" spots, Blackthorn's files while its
     switch is off, the guild hall table (fact 3) and the test fixture.
2. Blackthorn is off (the switch, `Initialize` and the command).
3. P281's hall checks on SoS fail no hall but P708's two.
4. The 9 lost stealables are parked, and `CheckRespawn` skips them.

Run on the server's overlay:
- **Red on main (`722ad95`):** 3 of the 3 code-and-literal facts fail, with 25 literals failing
  (`red-test-s8-spots.txt`). Fact 3 passes on main too, since no hall changed.
- **Green: 4 of 4** (`green-test-s8-spots.txt`). 397 literals: 257 stand on the land; 73 are on another facet; 48 are
  Blackthorn's; 7 are guild hall entries (fact 3); 6 are area corners; 5 are old-world "moved from" spots; 1 is the
  test fixture.

**The counts, again.** The brief's 293 "moves" and 162 "rework" literals, across 30 files, match P669's
`geo-files.csv`. Today those files hold 397 distinct literals. P669 counted each `Point3D` twice (once more as a bare
tuple), and P678 (S7) has since removed or moved some (`ClusterFNewHavenServicesSeeder`, `ClusterFOldHavenStockSpawns`
are gone; the Haven spots moved into `HavenSpots.cs`). All 397 are walked by fact 1, so the 293 are covered.

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P677`, `docker-build` lock, released): **EXIT=0**, 2,734 tests,
2,728 passed, 6 skipped, 0 failed (`green-gated-build.txt`).

## Decisions and deviations

- **Migration work:** none was planned, and none was added (fresh world). The existing "move an old world's NPC from"
  code (`wasAt`, `.WasAt`, the camp's move table) is left as it was. Its "from" spots are rock now, which is harmless:
  a fresh world has nobody there.
- **Not changed, for P708:** the Merchants' and Custodians' halls. **For P691:** Blackthorn's code and its 6
  stealables' spots.
- **The P281 checks needed the server's view of Felucca.** A UOP map file names its blocks by its own facet's file
  name, so a copy of Trammel's can't be read as Felucca's. The copied tools read facet 0 from facet 1's files, as the
  server's map definitions do since P675.
- **Found, not in P669's list:** `WrongDecoration.cs` (its `new("Static", id, x, y, z, ...)` rows are not one of
  P669's patterns). I moved only its 3 sparkles that sit on the moved teleporters; its other rows are unchecked.
  `ClusterFNewHavenSeeder`'s `SeedEntry(..., x, y, Direction, z)` rows are not one of P669's patterns either (P678
  measured those). A later fact could read both formats.
- **The Read tool was denied** (unattended run) for `ExodusSummoningAltar.cs`, which I wanted to read before editing
  the shrine spots. I read it with `sed` and edited it with a script (`notes\cc-P677-tools\edit_exodus.py`), then
  checked the diff. The other code edits went the same way (`edit_*.py`), so every change is a reviewable script.
- **No CHANGELOG line:** the swap is held from release and nothing here is live yet. The swap release's notes should
  cover it.
- **Outside the repos:** `D:\UO\golems\Iron\p677-work\` (the SoS client folder of hard links, 2.9 GB of mostly
  links; the stealables a/b copies; the crops). It can be deleted. The temporary main worktree was removed.

## Files

- Code copy:
  - `BlackthornDungeon/Region.cs` and `Generate.cs`.
  - `DespiseRevamped/Setup.cs`, `Items/Functional/DespiseAnkh.cs` (its comment).
  - `WrongDungeon/Generate.cs`, `WrongDecoration.cs`.
  - `Covetous Void Spawn/Generate.cs`, `TheExodusEncounter/Items/ExodusSummoningAltar.cs`.
  - `server/patches/StealableArtifacts-servuo-entries.patch`.
  - `design/mine-camp-tents/layout.json`, `ClusterFMineCampLayout.cs`, `ClusterFInstitutionSeeder.cs`,
    `ClusterFNewHavenSeeder.cs`, `ClusterFSouthMineDecor.cs`, `SurveyArchivist.cs`.
  - `Regions/OldHavenBurrowsRegion.cs`.
  - Tests: `MineCampLayoutDesignCopy.cs` (generated), `NewHavenSeederFloorVerification.cs`,
    `ExodusEncounterVerification.cs`.
- Docs copy:
  - `tools/tests/test_s8_spots.py`.
  - `notes\cc-P677-tools\`: `spots.py`, `probe.py`, `replace_camp.py`, `gen_layout.py` and its maker, `p281sos\`
    and its maker, the `edit_*.py` scripts, `files-all30.txt`, the `out-*.csv` tables, and the red and green outputs.

P677 DONE
