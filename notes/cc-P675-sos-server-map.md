# cc-P675: the server reads the SoS map, Felucca on the same file, and the Fold's mirror moves (SoS swap S2)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P675` (main at the P681 merge, `cac97fc`). Not committed; nothing deployed or published; Haven
not touched. The "Held" line in the prompt (swap prompts wait for the isle release) is met: P678's notes record that
release shipping at 21:09 on the 27th (package 2026.10.27.2106).

## In plain words

- **The server now reads Zigholtul's Siege of Sosaria map for Trammel, and Felucca shows the same land.** On the test
  shard, when it is next started from this code, a character standing in Valunstead stands on his town, not in the
  sea, on Trammel, on Felucca and on the Fold.
- **Our own map changes now sit on his map.** The Rootdeep Burrows and the Wakening Isle carry over unchanged. The old
  hole into Rootdeep in Old Haven's bank is gone from the map patch, because that bank is his Second Bank of Haven now
  and S7's cellar hatch replaced it. The old tutorial farm's two removed trees are gone from the patch too: the farm
  lives on the isle now.
- **The Fold's "send them home" area moved** off the author's Passage of Lost Souls cave to the empty corner where the
  Wakening Isle sits, on Trammel and Felucca. A player wandering into his cave stays there; one who somehow reaches the
  isle's beach outside the tutorial is sent to New Haven.
- **Paused at your request, with everything built and green.** The one thing left is pictures of the new land in our
  client, queued as P716.
- **For you:** nothing to decide. Once this merges, the test shard should not be restarted from main until the swap's
  go-live day (S3 and S8 are still to come; the overseer holds that). See "For the overseer" below.

## What changed

| Part | Where (code copy unless docs) | What it does |
|---|---|---|
| 1. The overlay on SoS | `docker/uo/Build-MapOverlay.ps1` | The base is now the package's SoS files (`player-package/vendor/sos-trammel-map/files/`, `-Base`), each checked against `manifest.csv` (size and SHA-256) before use, through the applier's `-BaseDir` (P674). The overlay still holds `map1LegacyMUL.uop`, `statics1.mul`, `staidx1.mul`. `-Stock` keeps the old build on EA's files. It refuses a `map1.mul` in the client data or the overlay (below). |
| 1. The test shard | `docker/uo/Start-TestShard.ps1` | Builds the overlay when the SoS files are on the PC (was: when EA's client data was), warns and leaves the overlay alone without them. `-NoMapOverlay`'s help says Felucca then shows EA's Trammel too. |
| 2. Felucca | new `server/customizations/Maps/SosMaps.cs` | `Configure` at priority 3 (after `MapLoader.Configure` at 2, like `FoldMaps`) sets Felucca's file index to 1 and drops its TileMatrix if one was made. Index 0, client id 0, name, size, season 4 and `FeluccaRules` stay. It throws (the shard does not start) if pinned's `Map` loses the two private fields. |
| 3. The patch | `player-package/vendor/shattered-legacy-map/trammel.mapops`, its `SOURCE.txt` | Re-based onto SoS: 875 blocks (was 879). The Burrows' 210 and the isle's 665 blocks carry over line for line, and their fingerprints did not change (both sit on void that is byte-for-byte the same in stock and SoS). Dropped: the 2 way-in blocks (x 3608-3623, y 2616-2623: P413's ant hill and P188's three wall removals) and cc-P276's 4 farm tree removals (2 blocks). |
| 3. The pristine copy | docs `notes/cc-P675-tools/sos-base/ORIGINAL-SHA256.txt` | The three SoS files under the client's names, as `rebase.py` (and later map builds, e.g. P662's `--base`) check them. |
| 4. The Fold | `server/customizations/Fold/FoldRegions.cs`, `FoldCommands.cs`, `FoldMaps.cs` (a comment) | `FoldMirrorRegion.Area` is x 6160-7167, y 3744-4095; one instance on Trammel (`Instance`) and a twin on Felucca (`FeluccaInstance`); `SendHome` works on either. `[Fold goto`'s default is `TutorialWorld.Beach` (6638, 3993), which P663 had already marked as "[Fold goto's default after S2". |
| Facts | `server/tests/Misc/SosMapsVerification.cs` (new), `server/tests/Regions/FoldVerification.cs`, `server/tests/Misc/MapCheckRealDataVerification.cs`; docs `tools/tests/test_mapops.py` | Below. |

### The reader's order (part 1's check)

The prompt expected UOP before MUL. Pinned reads it the other way: `TileMatrix` asks `Core.FindDataFile("map1.mul")`
first and only if no data folder has one asks for `map1LegacyMUL.uop` (`Projects/Server/TileMatrix/TileMatrix.cs:105-113`);
`FindDataFile` walks `dataDirectories` in order and takes the first folder holding the name (`Main.cs:346-372`). So:

- The overlay's `map1LegacyMUL.uop` beats the client's own (`classic-client-7.0.117.0`) because the overlay folder is
  first, which `Start-TestShard.ps1` already enforces (it refuses to start otherwise).
- A `map1.mul` in **any** data folder would beat both. Neither client folder on this PC has one
  (`D:\UO\UltimaOnlineVanilla`, `D:\UO\tool-trials\client-data-copy`: only `map*LegacyMUL.uop`). The overlay script
  now refuses if the client data or the overlay holds one.
- Pinned orders a UOP's chunks by the first 4 bytes of each chunk (`ConvertToMapEntries`, an unstable sort). P674's
  pack keeps the author's block headers, which are the block numbers (chunk headers 0, 4096, ... 454656, strictly
  rising), as EA's are, so the server reads his chunks in order.
- The server reads the UOP's entries by the hash of `build/map1legacymul/<n>.dat`, taken from the file's own name
  (`UOPFiles.GenerateHashes(stream.Name, ...)`), version 5: P674's pack writes those names and version 5.

## Facts, each seen failing first

**Map patch** (docs `tools/tests/test_mapops.py`, run with `SL_SHARD_REPO` set to the code copy): 10 of 10 green
(`green-test-mapops.txt`). Facts 4 to 6 are rewritten; the old 5 (rebuild P167's stock scratch build) and 6 (the ant
hill) described a patch that no longer exists. Red: the new facts against today's patch (`red-test-mapops-old-patch.txt`,
a copy of the code tree with HEAD's `trammel.mapops`): 4 fails on the ant hill's 0x310A at 3615,2616; 5 fails with 4
blocks drifted on SoS and the 3 wall removals missing; 6 fails on the way in's two blocks. Fact 7 (the isle) passes
either way.

| Fact | What it pins |
|---|---|
| 4 `the_shipped_patch_is_the_burrows_and_the_isle_only` | every line in the Burrows or the isle; no removals |
| 5 `the_shipped_patch_is_made_on_the_sos_map` | on the pristine SoS copy (at `ORIGINAL-SHA256.txt`): drifted 0, missing 0, and `diff(sos, applied)` is the shipped file line for line |
| 6 `the_way_in_from_old_haven_is_gone` | no line and no fingerprint in the way in's or the old farm's blocks; none of P413's burrow, P188's hole or P276's removals |

**The overlay** (`overlay-run.ps1`, `overlay_check.py`; `out-overlay-green.txt`, `out-overlay-red.txt`,
`out-overlay-check.txt`): the new script builds on SoS in 5 s, the stamp skips the second run, and it refuses a
`map1.mul` in the client data, a base file with one byte changed, and a missing base file. The overlay equals
`rebase.py`'s SoS + patch exactly (land byte for byte, 0 statics blocks differing). Red: HEAD's script on the same
call builds on EA's files (504,384 is sea 0x00A8 at -5; 128,618 statics blocks differ from SoS + patch).

**Server** (probe runs in the builder image `sl-uo-builder:cc-P681`, this branch's base, with this prompt's files
bind-mounted: `probe.sh`). Red used the image's own Fold code and a stub `SosMaps` with the same names and no behaviour
(`red-stub/`):

| Fact | Red: stock data (`red-probe-stock.txt`) | Red: SoS overlay, stub (`red-probe-sos.txt`) | Green |
|---|---|---|---|
| `SosMapsVerification.FeluccaReadsTrammelsFileIndexAndKeepsItsOwnRules` | file index 0 | same | yes |
| `SosMapsVerification.APlayerOnTrammelFeluccaAndTheFoldAtValunsteadStandsOnSosTileAndZ` (real data) | sea 0x00A8 (168) | Trammel on SoS, **Felucca on sea 0x00A8 at -5** | yes, all three maps: grass 0x0003 Z 15, standing at 15; the hall's 0x04AB at 20 and 40, roof 0x0596 at 49 |
| `FoldVerification.APlayerFoundOnTrammelsMirrorIsSentToNewHaven` (corners on both maps; the beach on Trammel and Felucca sent home; PoLS level 2 on both left alone; staff left; recall in refused) | `Region` at 6160,3744, not the mirror | same | yes |
| `FoldVerification.FoldGotoIsForStaffOnTheTestShardOnly` | (6214, 2001) | same | yes |
| `FoldVerification.APlayerOn32And40StandsOnTrammelsTileAndZ` (real data; spots now Valunstead, the Haven start, the beach) | 0x00A8 at 504,384 | passes (Trammel and the Fold read the overlay) | yes |
| `MapCheckRealDataVerification.TheRealAdapterReadsTheSosMapAsTheIndependentUopReadDid` (real data; renamed) | 0x03E9 (EA's New Haven) | passes | yes |

Green with the SoS overlay (`green-probe-sos.txt`): **36 of 36**, the files above plus P681's
`SosSpawnPlacementsVerification` and the other real-data files (`ClimbingBootsVerification`, `ChestMimicVerification`,
`RootdeepWayInVerification`), all on SoS. Without client data (`green-probe-nodata.txt`, the gate's host): 30 passed,
6 skipped (the real-data ones). The tile values were read independently from the overlay's files by `spots.py`
(`out-spots.txt`).

**The gated build** (`docker\uo\build.sh -t sl-modernuo:cc-P675`, detached through `gated-build.ps1`, `docker-build`
lock taken and released; Windows 3.4 to 3.6 GB available, the Docker VM 13 GB free after dropping its page cache):

- **Run 1, red** (`red-build-1-summary.txt`): 2,704 facts, 2 failed, both P681's `SosSpawnPlacementsVerification` on
  Felucca (`NewHome` gave no value for any of the 61 Felucca moves). The first `SosMaps` **replaced** Felucca's `Map`
  object, and P681 keys its placement table by the `Map` object, built once. In the test host my facts swapped Felucca
  after that table was built. In production the swap runs before anything builds such a table, but a design that
  changes a map's identity under every holder is fragile, so I changed it.
- **The fix**: `SosMaps` now keeps Felucca's object and sets its private `m_FileIndex` to 1 (and drops a TileMatrix if
  one was already made). Nothing that holds `Map.Felucca` sees a different map. Probe re-run with P681's facts in the
  same host: 36 of 36 on SoS.
- **Run 2, green** (`green-build-2-summary.txt`): **EXIT=0, 2,704 facts, 2,698 passed, 6 skipped, 0 failed.** The 6
  skipped are the real-data facts, which skip in every build (the gate's host has no client files). `sl-uo-builder:cc-P675`
  and `sl-modernuo:cc-P675` are built.

**The package's map facts** (`player-package\tests\Map-Overrides.Tests.ps1`, which reads the shipped patch): 16 of 16
(`green-ps-map-overrides.txt`).

## Not done, and why

- **The TazUO shots with S1's client** (part 5's last item). Chase asked for a stopping point as the green build
  finished, and the overnight bot was still running on the scratch shard, whose world the private proof shard copies.
  Everything for them is ready (below) and queued as P716.
- No CHANGELOG line: nothing reaches players until the swap goes live (S16 writes that day's line, P673 section 4).

## For the overseer

- **Once this merges, main's test shard reads the SoS map on its next start** (`Start-TestShard.ps1` builds the
  overlay whenever `player-package\vendor\sos-trammel-map\files\` is filled, and Felucca reads Trammel's files in
  code). Players' packages still draw stock land (P713's switch is `off`). So the test shard should not be restarted
  from main until the swap's go-live (S1, S2, S3, S7, S8 all merged and the switch turned on), as section 2 of P673
  already says. `-NoMapOverlay` starts it on EA's Trammel, but Felucca then shows EA's Trammel, not EA's Felucca.
  The main desk needs `Add-SosMap.ps1` run once (it fills `files\`) before the go-live restart.
- **The switch-off package is unaffected.** The re-based patch's fingerprints for the Burrows and the isle are the same
  as before (those blocks are byte for byte the same in stock Trammel and SoS), so a player on stock land gets the
  same patch with no "your files changed" line. Only the way in and the old farm's trees are gone from it.
- **The Second Bank of Haven on stock land** (switch off): the ant hill is no longer drawn there. It only mattered for
  the old Rootdeep way in, which S7 (P678) already replaced with its hatch, on SoS.

## Deviations and decisions

- **Felucca by reflection, not by a new `Map`.** The prompt asked for "the way FoldMaps.cs registers maps". Registering
  a new map at index 0 was my first version; the gate showed why it is fragile (above). The field is private and
  readonly in pinned; `SosMaps` throws at start if pinned ever renames it, and `SosMapsVerification` fact 1 reads it in
  every build.
- **The farm's 4 removals were dropped too**, though the prompt names only the way in. They removed two of EA's trees
  inside the old tutorial farm's fence; on SoS that spot is the author's forest, the S- lines would only miss or take
  his tree, and the farm itself is on the isle now (P663).
- **The reader's order is MUL before UOP** (above), the reverse of the prompt's wording; the check guards a `map1.mul`.
- **`MapCheckRealDataVerification`'s adapter fact** now pins SoS values (renamed
  `TheRealAdapterReadsTheSosMapAsTheIndependentUopReadDid`): with the overlay mounted, EA's New Haven values no longer
  hold. Its other three facts report only, and passed on SoS.
- **No `-Stock` fact for the overlay script**: `-Stock` is the old code path unchanged.

## Continuation

- **Done:** parts 1 to 4, all facts red first and green, the gated build green, the package's map facts green.
- **Left:** the TazUO shots (part 5's last item), queued as `D:\UO\cc-prompts\queue\cc-P716-cont-sos-s2-tazuo-shots.md`.
  Ready for it in `notes\cc-P675-tools\`: `overlay-run.ps1` (builds the overlay), `proof-shard.ps1` (a private shard on
  2596 from `sl-modernuo:cc-P675` with the overlay first in `dataDirectories`), `shots.ps1` (P661's two-window shots,
  with the client's overrides built on the SoS base and today's patch, TazUO from `D:\UO\golems\Iron\tazuo-p670\client`)
  and `scenes.json` (Valunstead on Trammel, Felucca and the Fold; the beach on Trammel and Felucca; Passage of Lost
  Souls level 2). None of them has been run yet.
- **Mid-flight:** nothing. No container of mine is running; no lock is held; the scratch overlay is in this session's
  scratchpad and is rebuilt by `overlay-run.ps1` in about 5 s.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun` against both copies (`commit-preflight.txt`): exit 0.

- Code copy, 11 files: `docker/uo/Build-MapOverlay.ps1`, `docker/uo/Start-TestShard.ps1`,
  `player-package/vendor/shattered-legacy-map/SOURCE.txt` and `trammel.mapops`, `server/customizations/Fold/`
  (`FoldCommands.cs`, `FoldMaps.cs`, `FoldRegions.cs`), new `server/customizations/Maps/SosMaps.cs`,
  `server/tests/Misc/MapCheckRealDataVerification.cs`, new `server/tests/Misc/SosMapsVerification.cs`,
  `server/tests/Regions/FoldVerification.cs`.
- Docs copy: `tools/tests/test_mapops.py`, this file and `notes\cc-P675-tools\` (3 MB in all, the two build logs
  git-ignored as `*.log`; the edit scripts, the probe and proof scripts, the red stub, the hashes, the red and green
  logs). No file over 5 MB; everything ASCII. The SoS map files stay in the git-ignored `files\` and the scratchpad.
- Edits to existing code files went through scripts (`edit_*.py`). Locks: `docker-build`, taken and released twice.
  No test shard, no package build, no Haven. Nothing committed.
- The continuation prompt: `D:\UO\cc-prompts\queue\cc-P716-cont-sos-s2-tazuo-shots.md`.

P675 PAUSED
