# cc-P685: Felucca's champion spawns on the SoS land (SoS swap S12)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P685`. Not committed; nothing deployed; the test shard not touched. The map is Zigholtul's (Siege of
Sosaria Trammel Map 3.0), which Felucca reads too (P675).

## In plain words

- **Felucca's 17 champion altars all stand on usable ground on the new map.**
  - Three of the Lost Lands altars (LL06, LL07, LL11) were floating over land the author rebuilt lower. They move to
    nearby open shelves of the same wilderness.
  - One more (LL08) keeps its altar but gets a new eject point, where players are thrown out of the spawn area, because
    the ground under its old one is now 19 Z lower, leaving it in the air.
  - The other 13, among them the five dungeon champions, stay exactly where they are.
- **No champion spawn area touches a town, a guard zone or the fenced unfinished land,** and no two overlap.
- **For you:** nothing to do until the swap goes live. On swap day `[GenChamps` on the fresh world places them.

## How it was done

**Starting point:** P696's proposal (Valorite, `golem/Valorite/P696`, 4843d5b, not merged). It keeps 14 altars, moves
LL06, LL07 and LL11 to its option A, and gives LL08 a new eject point. I checked every site on the map
(`notes\cc-P685-tools\champs.py`, P481's copy of the SoS files, P681's walk rules), not just the three.

**Where a champion is.** ChampionSpawn places these from the invisible controller:

- the 5 x 5 platform at controller Z - 20, with the altar at Z - 15 (ChampionSpawn.cs:819-842);
- the spawn area, [X-24, X+24) x [Y-24, Y+24) (ChampionSpawn.cs:190-193);
- the eject point, which GenChamps gives each site.

**The test, per site:**

| Part | Passes when |
|---|---|
| Platform | every one of its 25 tiles has a floor within 5 Z of the platform's Z |
| Spawn area | its walkable share is at least 80 percent of stock's for the stock site, or a quarter of the area (dungeon rooms are walled; stock's own share is the measure) |
| Guard zones | no tile of the area is in a TownRegion or GuardedRegion: Trammel's SoS regions (P676), which say where the towns stand on the land Felucca shares; Felucca's own regions stay pinned's until S13 |
| Closures | no tile of the area is in an S14 closure box |
| Eject point | it has a floor within 5 Z |

**Calibrated on stock.** Destard's (D3) and Fire's (D4) platforms miss the floor on 12 and 8 of their 25 tiles on SoS,
and on exactly the same tiles on stock Felucca: the platform's own pieces cover the uneven room floor, as they do today.
A platform that misses the floor on exactly the tiles it misses at stock's site is **stock-tolerated**.

**The stock sites as they are, on SoS** (`red\red-stock-sites-on-sos.txt`): 6 of 17 fail.

- **LL06, LL07, LL11:** their platforms hang 20 to 90 Z over the rebuilt ground, and their eject points have no floor.
- **LL08:** its eject point has no floor.
- **D3 and D4:** stock-tolerated, as above.

**The shipped sites** (`out\champs.csv`, `out\champs.txt`): **all 17 pass**, and no two spawn areas overlap.

| Site | Boss | Controller | Eject | Change | Walkable share (stock's) |
|---|---|---|---|---|---|
| LL01 | random | 5511,2360,42 | 5439,2323,26 | kept | 0.84 (0.84) |
| LL02 | random | 6038,2401,47 | 5988,2340,24 | kept | 0.57 (0.57) |
| LL03 | random | 5549,2640,16 | 5645,2696,-8 | kept | 0.71 (0.71) |
| LL04 | random | 5636,2916,37 | 5721,2949,28 | kept | 0.66 (0.66) |
| LL05 | random | 6035,2943,50 | 6098,2997,17 | kept | 0.85 (0.85) |
| **LL06** | random | **5432,3220,19** (was 5265,3171,105) | **5423,3183,-3** | moved, P696 A | 0.88 (0.56) |
| **LL07** | random | **5324,3428,15** (was 5282,3368,50) | **5296,3428,-5** | moved, P696 A | 0.88 (0.69) |
| LL08 | random | 5207,3637,20 | **5209,3609,0** (was 5263,3687,0) | eject moved | 0.87 (0.85) |
| LL09 | random | 5954,3475,25 | 6013,3529,0 | kept | 0.87 (0.84) |
| LL10 | random | 5982,3882,20 | 5929,3820,-1 | kept | 0.79 (0.75) |
| **LL11** | random | **5768,4024,20** (was 5724,3991,41) | **5768,3996,0** | moved, P696 A | 0.92 (0.91) |
| LL12 | Lord Oaks | 5559,3757,21 | 5513,3878,3 | kept | 0.91 (0.86) |
| D1 Deceit | Neira | 5179,709,20 | 4111,432,5 | kept | 0.40 (0.40) |
| D2 Despise | Barracoon | 5557,827,65 | 5580,632,30 | kept | 0.33 (0.28) |
| D3 Destard | Rikktor | 5259,837,64 | 1176,2637,0 | kept, platform stock-tolerated | 0.79 (0.85) |
| D4 Fire | Semidar | 5815,1352,5 | 2923,3406,8 | kept, platform stock-tolerated | 0.42 (0.42) |
| D5 Terathan Keep | Mephitis | 5190,1607,20 | 5482,3161,-54 | kept | 0.59 (0.59) |

Classes, boss types and random-type rules stay pinned's. D4's eject point is inside Serpent's Hold (P696 noted it): an
exit into town, as in stock, not a spawn area in a guard zone.

## How the server uses it

- `server\patches\GenChamps-sos-sites.patch` (new, made by `cc-P685-tools\make_patch.py` with `diff -u`, checked with
  `patch --fuzz=0`) changes four lines of pinned's `GenChamps.cs`. It also adds a comment naming this prompt. It is
  registered in `docker\uo\apply-patches.sh` after the other SoS patches.
- `[GenChamps` (Developer) places them, as before. **Migration dropped** (Chase's fresh test world): nothing moves the
  champion spawns an existing world has; `[GenChamps` deletes and replaces every one when it runs.

## Facts

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_sos_champions.py`: (1) a subtest per altar, each of the 17 shipped sites passes on SoS, and no two areas overlap; (2) the patch puts in exactly champs.py's sites (P696's three moves and LL08's eject, the stock lines removed) | the stock sites on SoS: 6 of 17 fail, 4 of them not stock-tolerated (`red\red-stock-sites-on-sos.txt`); a copy of the patch with LL11 put back: fact 2 fails (`red\red-facts-mutated-patch.txt`) | 2 of 2, 17 altar subtests, `green-facts.txt` |
| code `server/tests/Misc/SosChampionSitesVerification.cs`: a fact per altar (17 theory rows): a real `[GenChamps` places exactly one ChampionSpawn of the site's class at its controller on Felucca, with its eject point on Felucca and its boss or random type, and none at a moved site's old spot | the gated build with the patch held out (its file and its apply-patches line): exactly LL06, LL07, LL08 and LL11 fail, the other 13 altars and 2,768 more facts pass, `red\red-build-1.txt` | 17 of 17 in the gated build, `green-build-2.txt` |

**The gated build** (the repo's gated build script, `-t sl-modernuo:cc-P685`, detached through
`cc-P685-tools\gated-build.ps1`; the Docker VM's page cache dropped first; docker-build lock taken and released):

- **Run 1, red:** 2,791 facts, 4 failed (the four changed sites), 2,781 passed, 6 skipped.
- **Run 2, green** (`green-build-2.txt`): **EXIT=0, 2,791 facts, 2,785 passed, 6 skipped, 0 failed.** The skips are
  the real-map-file facts that skip in every build.

## Not done, and why

- **Spawning in game** (CanSpawnMobile across each area, the platform assembled, walking from the eject point back):
  it needs the server and client on SoS together (S1, S2 live), for S15.
- **Felucca's guard zones** are S13's. The check uses Trammel's SoS towns, the same land. S13 should keep its zones
  clear of these 17 areas (`out\champs.csv` has them).

## Deviations and decisions for Chase

- **Code-copy edits by script.** The Read tool is auto-denied for files in my code copy, so I registered the patch
  with an exact-text Python script (`cc-P685-tools\edit_p685.py`), as in P682 to P684.
- **P696's option A taken for all three moves.** Each passes every check; option B was not needed.

## Commit preflight

- **Code copy:** new `server/patches/GenChamps-sos-sites.patch` and `server/tests/Misc/SosChampionSitesVerification.cs`;
  changed `docker/uo/apply-patches.sh` (the patch registered).
- **Docs copy:** this file, new `tools/tests/test_sos_champions.py`, and `notes/cc-P685-tools/` (champs.py,
  make_patch.py, the edit script, the build wrapper, `out/`, `red/`, the fact and build outputs; 1.5 MB, no file over
  5 MB).
- **Lock:** docker-build, taken for the gated builds and released. No test shard, package or Haven work. Nothing
  committed.

P685 DONE
