# cc-P681: Stock spawners on the new land (SoS swap S9)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P681` (from main 9ee74b6). Not committed; nothing deployed; Haven not touched. The swap prompts' hold
ended when the isle release shipped (2026-10-27 21:09, P678's notes).

## In plain words

- **Every monster, animal, reagent and shopkeeper spawner in the old world data was checked against the new map.**
  That is 4,304 spawners across Trammel and Felucca. About 95 percent stay exactly where they are, because the new
  map still has walkable ground or a shop floor there.
- **About 60 per facet move a short way.** Most are in the wild, where a hill or forest became rock or sand, or the
  ground turned to sea. Some shopkeepers move where their building was rebuilt elsewhere. On Felucca, Haven's healer,
  smiths and provisioner go to the matching shops in the author's town.
- **About 22 per facet are left out:** deep-sea spawners whose sea is new land now, wild spawners with no walkable
  ground within 20 tiles, and wild spawners standing inside the author's new towns (S10 peoples those). Four vendors from
  the old New Haven's outlying halls move into the author's town beside their guilds.
- **No town loses a banker, healer, smith or provisioner it has today.** For you: a few towns never had one in the
  stock data (Cove's bank, Yew's and Wind's smiths, Nujel'm's healer and provisioner, Magincia's smith and
  provisioner). Say if S10 should add them. Nothing else to do until the swap goes live.

## How it was done

**Starting point:** P698's plan (Valorite, commit 34502e9 on `golem/Valorite/P698`, not yet merged). Its ledger of all
4,304 stock records (source, guid, home, ranges, entries, population kind, import status) is copied as
`cc-P681-tools\p698-spawner-plan.csv`. P698 checked no tile on the map. P681 checked every one, as P698 asked.

**The map:** `sosgrid.py` turns the SoS Trammel files into whole-map arrays with the playbook's walk rules
(cc-P188 / cc-P678 soswalk), vectorized:

- the standing Z, open water, covered tiles (inside a building) and the terrain class;
- the same arrays for stock Trammel and stock Felucca.

Felucca reads the SoS file on swap day (S2, P675), so both facets are graded on SoS. Against P678's tile-by-tile walk,
the grid agrees on 99.6 to 100 percent of tiles. The differences are where surfaces stack more than 16 apart.

**The test** (`regrade.py`, `Grader.passes`):

- A spawner that stands still (range 0 or 1) needs a floor of its tile within 5 Z. Every surface counts, not only the
  top one, so the upper floors of a building count.
- A ranged spawner needs walkable ground within 2 tiles of its home, and land over a quarter of its range. Dungeon
  rooms and ranges of 50 or more need a tenth. Reagent fields (range 100 to 200) need land somewhere in range.
- Sea life needs water at home and over a quarter of its range.

**Calibrated on stock.** I ran the same test over the stock maps (`regrade.py --baseline`, `out\baseline-stock.txt`).
The first version failed about 170 spawners per facet that work today: wild homes at Z 0 on hills, homes on a tree,
vendors over stacked floors. I relaxed it until about 30 per facet remain. Those are **stock-tolerated** (27 on Trammel,
29 on Felucca: Shame's and Ice's rooms, a few Magincia vendors) and are kept where they are. Only what the SoS land
breaks moves or goes.

**Purpose** (P698's rules), on top of the walk:

- A standing town NPC that was indoors on the stock map and is outdoors on SoS has lost its building.
- A wild spawner must stay out of the author's seven new towns. Those are S10's civic space: Valunstead, Hammerhill,
  Kameron Kove, Elmhaven, Kettleburg, Fort Yondall and Elandrim Nur Shaz, using his `Regions.xml` rectangles.
- A wild spawner whose ground changed habitat (green, sand, snow, swamp, rock or lava) has to find its old habitat.

**The search**, ring by ring out to 20 tiles (P673's rule), for the nearest tile that passes. A spawner whose only
fault is a changed habitat, with no match within 20, is kept: its home and range still pass the walk. The other search
rules:

- Town NPCs try indoors first. A town's banker, healer, smith or provisioner searches out to 40.
- In the author's Haven, a shopkeeper goes to the shop of its trade, where pinned's pre-UOML data (S7's source) has it.
- Wild spawners need the same habitat, outdoors, and not in a new town.
- Dungeon spawners stay on the same floor (within 10 Z). Sea life needs water.
- With nothing found, the spawner is dropped.

The 25 records with an explicit spawn rectangle are kept or dropped, never moved, because the rectangle would stay
behind. Moving is P673's 20 tiles at most, never chained.

**Left to others, and why:**

- **Never imported:** the 45 uoml/** records, the 30 Despise creature records and the old crier. Their existing
  hooks stay as they are.
- **S7 (P678):** 68 Trammel records that P678's `ClusterFHavenTownSpawns` refuses. These are the ML plaza's town
  spawners and Old Haven's ruin inside the author's town. P678 is not merged into this branch's base, so the rule is
  replicated in `regrade.py` to leave the same records alone.
- **ML New Haven's outlying vendors** (the Holy Mage, the evil wandering healer, the Actor and the mine camp's Miner)
  stood by halls that are forest or rock on SoS. They move into the author's town beside their halls' new homes in
  P678: the Haven Magery School, the Keepers' east house, the Bardic Guild, and the Mystic Mines of Haven for the Miner.
  Each is clear of P678's NPC tiles (`p678-homes.csv`, copied from `golem/Iron/P678`).
- **S14:** the north-east snow closure's two Outdoors records (P698's drops).

## Results

| | Trammel | Felucca |
|---|---|---|
| Stock records | 2,182 | 2,122 |
| Not this prompt's (never imported 76, S7 68) | 144 | 0 |
| Kept | 1,953 (27 stock-tolerated, 5 habitat-only) | 2,038 (29 stock-tolerated, 4 habitat-only) |
| Moved | 63 | 61 |
| Dropped | 22 | 23 |

- **Moves:**
  - Why they move: 36 to 37 per facet fail the walk outright; 13 to 14 changed habitat; 7 are standing NPCs whose
    floor's Z changed by 3 to 5; 2 lost their building; 1 was inside Fort Yondall; and on Trammel, ML New Haven's 4
    outlying vendors.
  - What moves: mostly wild encounters (21 to 22) and wildlife (13 to 14), then 9 sea spawners per facet, 6 dungeon
    rooms, 4 to 5 town services, crops, reagents and 2 ChaosGuards at Britain's castle.
  - On Felucca, Haven's healer, smiths and provisioner go to their shops.
- **Drops:**
  - 13 to 14 sea spawners per facet whose ocean is the author's new land (the new continent, coasts and islands);
  - 9 wild spawners per facet (6 wild encounter, 3 wildlife): 4 to 5 fail the walk with no ground within 20, 4 stand
    inside Kameron Kove, Elmhaven or Hammerhill (S10's), and 1 is in the north-east snow closure.
  - No post-uoml file loses a spawner, so the import facts that count them (and P678's Haven facts) stand.
- **The ledger**, with a reason for each of the 4,304 spawners: `cc-P681-tools\out\ledger.csv`. Totals by facet and
  kind: `out\summary.txt`.

**Core services** (`services.py`, `out\services.txt`): every stock Trammel and Felucca TownRegion the shard registers
keeps every banker, healer, smith and provisioner it has in stock. New Haven reads S7's pre-UOML Haven spawners. These
towns have none of a role in the stock data, inside their region rectangles:

| Town | Missing role |
|---|---|
| Cove | bank |
| Yew | smith |
| Wind | smith |
| Nujel'm | healer, provisioner |
| Magincia | smith, provisioner |

The fields and the Heartwood have no roles. S9 moves stock and does not invent people, so these are listed for Chase
and S10.

## How the server uses it

- `server\customizations\ClusterFSosSpawnPlacementsTable.cs` is generated by `regrade.py`. It holds 124 moves and 45
  drops, each by facet and data guid. Do not edit it by hand.
- `server\customizations\ClusterFSosSpawnPlacements.cs` does the lookup. `Place(guid, map, ref location)` returns
  false for a drop and sets the new home for a move.
- `server\patches\ImportSpawners-sos-placements.patch` is a new patch, applied after the Despise exclusion in
  `docker\uo\apply-patches.sh`. The importer asks `Place` before it builds each spawner, so a moved spawner is built at
  its new home as if the data said so.
  - It is a separate patch from P678's change to `ImportSpawners-despise-exclusion.patch`. Its hunk sits 12 lines above
    that one, and P678's edit keeps that patch's line count, so the two merge cleanly.
- Spawners are matched by guid, never by coordinates.
- **Migration dropped (Chase's fresh test world):** nothing moves spawners an existing world already has.

## Facts

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_sos_spawners.py` 1: every kept or moved home passes the walk on SoS, re-run from the map (stock-tolerated excepted, under 2 percent) | the stock homes left as they are on SoS: 111 spawners fail (`red\red-fact1-stock-homes-on-sos.txt`) | 3 of 3 |
| 2: every move within 20 tiles (40 for core services; Haven shops within the town), and the C# table equals the ledger | | |
| 3: no town loses a core service (`services.py`) | | |
| code `tests/Misc/SosSpawnPlacementsVerification.cs`: (1) every row is a stock spawner of its facet's shipped files, once, moved or dropped; (2) a real `[GenerateSpawners` of a stock file on Trammel and on Felucca builds moved spawners at their new home, no dropped one, the rest where the data says | main's builder image without the patch (`probe.sh`, `red\red-cs-probe.txt`): fact 2 fails on both facets, moved spawners built at their old homes | 3 of 3 in the gated build |

**The gated build** (`docker\uo\build.sh -t sl-modernuo:cc-P681`, detached through `gated-build.ps1`, docker-build
lock taken and released; about 2 GB available in Windows, 13 GB in the Docker VM):

- **Run 1, red** (`red\red-build-1-summary.txt`): 2,706 facts, 1 failed. `SpawnerImportVerification` fact 4 counts
  every spawner of post-uoml/trammel/Vendors.json, and the table then dropped ML New Haven's four outlying vendors. P678
  rewrites that fact too, so editing it would collide at merge. The vendors move into the author's town instead (the
  prompt's "a new spot in the town"), and the fact stands unchanged.
- **Run 2, green** on the table of that moment.
- **Run 3, green on the final table** (`green-build-3-summary.txt`): **EXIT=0, 2,706 facts, 2,701 passed, 5 skipped,
  0 failed.** The skips are the real-map-file facts that skip in every build. The final table keeps changed-habitat
  spawners rather than dropping them, so no post-uoml file loses a spawner. That keeps P678's Haven facts, which count
  them, true after both merge.

## Not done, and why

- **Walking each moved spawner in game, and pictures.** These need the server and the client on SoS (S1, S2).
- **New spawns for new land** (the author's islands, continent and towns). That is S10's job, from P698's 107
  requests.
- **The gaps in the stock data's own services.** Listed above, for Chase or S10.
- **Khaldun's 47 Felucca records.** P698 had no evidence for them. They were graded here on SoS like the rest: kept
  where they pass, moved or dropped where they don't (`ledger.csv`).

## Commit preflight

- **Code copy:**
  - new `ClusterFSosSpawnPlacements.cs`, `ClusterFSosSpawnPlacementsTable.cs`, `ImportSpawners-sos-placements.patch`
    and `tests/Misc/SosSpawnPlacementsVerification.cs`;
  - `docker/uo/apply-patches.sh` (the new patch registered).
- **Docs copy:** this file, `tools/tests/test_sos_spawners.py` and `notes\cc-P681-tools\`.
  - The tools, `out\` and `red\`, and the copy of P698's ledger.
  - About 3.5 MB in all, no file over 5 MB. The map grid caches live outside the repo, in `%TEMP%\p681-sosgrid*.npz`.
- **Lock:** docker-build, for the gated build, released after it. No package, no deploy, nothing committed.

P681 DONE
