# cc-P674: the Siege of Sosaria map in the player package, for Trammel and Felucca (SoS swap S1)

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P674` (main at the P665 merge). Not committed; nothing deployed or published; Haven not touched.

## In plain words

- **The player package now carries Zigholtul's Siege of Sosaria map** as the land for Trammel and Felucca. The download
  grows by 37 MB (a 189 MB zip instead of 152 MB). Nothing changes for players until the swap goes live: the server
  side (S2 and the rest) is still to come, and nothing is published.
- **A player's first start after the update spends about 5 seconds building the map** (Trammel's copy with our own
  changes, and Felucca's copy of the same land), using about 220 MB more disk. Every later start skips it in under half
  a second.
- **The package's safety checks still hold.** The zip may hold exactly the author's three map files, byte for byte, and
  no other map file and nothing of EA's. A wrong, extra or missing map file stops the build.
- **For you: one decision.** Old packages must be kept off the swapped server, but today nothing tells the server
  which package a client runs, and staff use other clients too. Choose the rule on your Golem card
  (`Iron-P674-20261027-153414-0e8f`). The last part, pictures of the new land in our client, waits for the server
  prompt S2, which nobody has started.

## What was built

| Part | Where | What it does |
|---|---|---|
| 1. The asset | `player-package/vendor/sos-trammel-map/`: `SOURCE.txt`, `manifest.csv`, `Add-SosMap.ps1`; `files/` git-ignored (`.gitignore`) | The manifest holds the size and SHA-256 of the author's zip and his three files (kind `source`, read from `D:\UO\third-party\sos-trammel-map`), and of the three files that ship (kind `ship`). `Add-SosMap.ps1` checks his files and copies the statics and index. It packs `Map1.mul` with `mapops.py pack`, checks every result and deletes anything that does not match. A run took 2.3 s. `SOURCE.txt` carries the credit, the URL and his terms. |
| 2. Packing | docs `scripts/mapbuild/mapops.py`: `write_map_uop`, `pack`, `rename_uop`, CLI `pack` and `rename` | `synthetic_facet`'s writer, generalized: a map MUL becomes facet 1's UOP, `build/map1legacymul/<8 digits>.dat`, 4,096 blocks an entry, tables of 100 chained (EA uses 1,000 in one table; TazUO and pinned read any). The SoS pack is 112 entries, 89,919,252 bytes, and is deterministic. It reads back through `uofiles.MapFile` as all 458,752 of the author's blocks, unchanged, on facet 1 and, renamed, on facet 0. `synthetic_facet` still writes the same bytes as before (checked for 1, 2 and 3 chunks). |
| 3. Felucca on the player's PC | `payload/app/Apply-MapOps.ps1`: `-BaseDir`, `-AlsoAs`, `Copy-UopRenamed`, `Get-MapBaseName`; `Build-UoOverrides.ps1`: `-MapBase` (default `app\map`) | With `app\map\base-*` present, the patch goes on a copy of the shipped base instead of the player's own map. `map0LegacyMUL.uop` is then a copy of the patched map1 with each entry's name hash rewritten to map0's names: the client finds entries only by those hashes, so the bytes stay the same. The override list gains `map0legacymul.uop=`, `statics0.mul=` and `staidx0.mul=`, the last two naming Trammel's files. TazUO opens map files read-only and shared (`UOFile`: `FileShare.ReadWrite`), so one pair serves both maps. |
| 4. The stamp | `Apply-MapOps.ps1` `Get-MapStamp` (format `uo-map 2`) | It names each base file by full path, size and time, plus the extra facets. A new base or a switch from EA's map to the base rebuilds, and a missing Felucca copy is rebuilt. The old `uo-map 1` stamps all rebuild once. |
| 6. Gate 4 | the package build's `Test-PackageZip` and staging | Before staging, every ship row must be in `files\` at its size and SHA-256 ("SOS MAP GATE"), staged as `app\map\<file>`, and checked byte for byte in gate 3. In the zip, `app/map/` must hold exactly the three ship rows at their hashes. Only those three are exempt from "an EA data file type". The EA-name check is unchanged: the shipped names (`base-...`) are not EA's. The README gets a line under "What is in here" crediting the map. "No EA game file is included" still reads true: these are the author's files. |

**Measured first start** (`notes\cc-P674-tools\firststart.ps1`, on the real files: the SoS base, today's
`trammel.mapops`, Felucca included): **4.6 s** the first time, **0.40 s** the next (the stamp matches). The copies come
to 220.9 MB (map1 and map0 90 MB each, statics 46 MB, index 5.5 MB). That comes on top of the 141.7 MB shipped in
`app\map\`. The PowerShell output is byte for byte the Python `apply` and `rename` on the same base.
Today's patch on SoS land: 4 of its blocks have drifted and 3 of its removals miss. That is the "your files changed"
yellow line at the first start. S2 re-bases `trammel.mapops` onto SoS, which clears both.

**Shipping one pack against both** (the zip's deflate, measured on the real files): map 1 only, **36.8 MB** zipped;
both packs, **58.3 MB** (+21.5 MB). Building Felucca's on the PC costs a 90 MB copy and 112 hash rewrites, inside the
4.6 s. I kept the plan's choice: ship one, build the other.

**The package** (`package` lock, taken and released; built with `-TazUO D:\UO\golems\Iron\tazuo-p670\client` and
`-UoData D:\UO\tool-trials\client-data-copy`): `ShatteredLegacy-2026.10.27.1515.zip`, 181 MB as the build reports it
(189,420,719 bytes; yesterday's was 152,476,726), 741 files. Every gate passed: the paperdoll fit, the animation encode,
gates 3, 4 and 6. The map files compress to 21.5 + 14.5 + 0.8 MB in the zip. It sits in `player-package\dist\`
(git-ignored), unpublished.

## Facts, each seen failing first

| Fact | Where | Red, against | Green |
|---|---|---|---|
| Python 8: pack writes the whole map as the client reads it (3 chunks, last short, tables of 2 chained); rename gives facet 0 the same land, only the 24 hash bytes differ, and refuses a facet-0 file | `tools/tests/test_mapops.py` | HEAD's `mapops.py`: no `write_map_uop` (`red-py-head.txt`) | yes |
| Python 9: the PowerShell applier on a shipped base equals Python apply and rename, writes the 6 lines, Felucca reads Trammel's statics, the stamp skips and a new base rebuilds | same | the old applier: "A parameter cannot be found that matches parameter name 'BaseDir'" (`red-py-fact9-old-applier.txt`) | yes |
| Python 10: the manifest is the author's download, and packing his `Map1.mul` gives exactly the shipped UOP | same | HEAD's `mapops.py`: no `pack` (`red-py-head.txt`) | yes (112 entries, same SHA-256) |
| PS `P674_AShippedBaseIsPatchedInsteadOfThePlayersFilesAndFeluccaGetsTheSameLand` | `player-package/tests/Map-Overrides.Tests.ps1` | old applier: no `-BaseDir` (`red-ps-map.txt`) | 10 of 10 |
| PS `P674_TheStampNamesTheBaseSoANewBaseRebuildsAndAnUnchangedOneDoesNot` | same | same | |
| PS `P674_AFeluccaCopyRefusesAFileThatIsNotTrammelsMapAndAFacetOfAnotherSize` | same | old applier: no `Copy-UopRenamed` | |
| PS `P674_AShippedBaseMapReachesTheListForTrammelAndFeluccaAndTheNextStartOnlyChecks`: a real launch (`Invoke-UoOverrides`) | `player-package/tests/Launch-Overrides.Tests.ps1` | old scripts: the list names no map (`red-ps-launch.txt`) | 19 of 19 (`green-ps-launch.txt`) |
| Gate 4 on the built zip and four bad copies | `notes\cc-P674-tools\gate4_mutants.py`, `gate4_check.ps1` | a changed byte in `app/map/base-statics1.mul`, an extra `app/map/statics1.mul`, a stray `app/extra/statics9.mul`, and yesterday's zip with no map: each refused with its reason (`gate4-checkzip.txt`) | the built zip passes gates 4 and 6 |
| The staging gate | the build, with `files\base-staidx1.mul` moved aside | "SOS MAP GATE: files\base-staidx1.mul is missing. Run vendor\sos-trammel-map\Add-SosMap.ps1. Not building." (`sos-map-gate-missing-file.txt`) | restored, same SHA-256 |

One existing fact changed on purpose: Python fact 3 now expects the stamp's `uo-map 2`.

**The other package test files** (`package-tests-summary.txt`): all green except Package-Client.Tests.ps1, which passes
3 of 9. P670 recorded the same failures: its child builds look for EA client data where this desk has none. Not caused
here. Build-UoOverrides.Tests.ps1 failed one fact before I fixed it. **That was P665's miss, and it was my own task:**
P665 added the two vision-panel gumps (23209, 23210) to the art registry, and this fact's hard-coded counts (801 rows,
54 gumps) were not raised. Now 803 and 56, with a comment. 26 of 26.

**Python fact 5 fails, and it fails at HEAD too** (`test_5_the_shipped_patch_rebuilds_the_scratch_build_exactly`:
statics blocks 231751 and 332429 differ from P167's scratch build). Block 231751 is x 3616-3623, y 2616-2623 (the
Second Bank way-in); block 332429 is x 5192-5199, y 1128-1135 (the Burrows). It is not this task's; the overseer
should know the fact is red on main.

## Not done, and why

- **Part 5, the package version floor: asked Chase** (`Iron-P674-20261027-153414-0e8f`). Nothing tells the server
  which package a client runs today. The handshake our client answers (`TazUOClientCommand.cs`, enhanced packet 0xCE
  id 4) carries no version, and no client patch sends one. The fix needs a client patch (0009), a client rebuild and a
  server check. The rule for clients that send nothing matters: staff use ClassicUO and Razor (`D:\UO\CUO-Admin`,
  `RazorEnhanced-Admin`), and refusing them by default would lock staff out. The choices are on the card. My pick is
  to refuse a package older than the swap and let a client that sends nothing in, with a warning line.
- **Part 7, the proof on a private world with S2's server:** S2 is not written or claimed. TazUO draws land from its
  own files, so a client-only picture is possible now, but the prompt asks for it with S2's server. Doing it twice
  would cost a private shard and two clients. I will do it once S2 exists, or now if Chase or the overseer says so.
- **TazUO's map 0 and map 1 sharing one statics pair** is read from the source (`UOFile` opens read-only with
  `FileShare.ReadWrite`; each map gets its own reader). Not yet seen in a running client: part 7 shows it.
- **The `x` maps:** TazUO switches every facet to `map<N>x` files when the server sends `CLF_UNLOCK_FELUCCA_AREAS`
  (`MapLoader.LoadMap`). Pinned's Endless Journey row in `Distribution\Data\expansions.json` sends
  `NewFeluccaAreas: false`, and P188's map patch already shows in game the same way. Our live `expansion.json` is in
  the main copy, which I may not read. If it ever turns that flag on, the overrides would need the `x` names too.
- No CHANGELOG line: nothing reaches players until the swap goes live, and that day's line is S16's (P673 section 4).

## Deviations and decisions for Chase

- **Shipped names are not the client's.** The three files ship as `app\map\base-map1legacymul.uop`, `base-statics1.mul`
  and `base-staidx1.mul`, so gate 4 can keep refusing any file named like an EA file. The launcher copies them under the
  client's names into `app\uo-overrides\`, as it already did with the player's own files.
- **The package build does not run Python for the map.** It checks the files `Add-SosMap.ps1` made against the manifest
  and refuses on any mismatch. The prompt says the build "fetches or copies them"; here the copy is a separate step, as
  with the music tracks (`Add-Track.ps1`). It keeps the build from depending on the docs repo's path.
  `Add-SosMap.ps1 -MapOps` defaults to `D:\UO\shard-migration\scripts\mapbuild\mapops.py`; I ran it with my own copy.
- **The shared client at `D:\UO\tazuo-sl-build\client` is stale** (no patch 0008; P670 noted it), so I built with my own
  `tazuo-p670` build. Rebuild the shared client before the next real package (P670 said the same).
- **EA's map1 UOP holds one extra block** (458,753; the last entry is 196 bytes) and entries with 136-byte headers.
  The pack writes 458,752 blocks and no headers. TazUO adds the header length it reads, and nothing reads past the
  facet's last block.
- Python 3.12's `-I` vs `-P`: the scripts run with `-P`, as memory advises.

## Asked, and commit preflight

- Asked Chase: `Iron-P674-20261027-153414-0e8f` (part 5's rule).
- Code copy: new `player-package/vendor/sos-trammel-map/` (`SOURCE.txt`, `manifest.csv`, `Add-SosMap.ps1`; `files/`
  git-ignored, proven with `git check-ignore`); changed `.gitignore`, the package build script,
  `payload/README.txt`, `payload/app/Apply-MapOps.ps1`, `payload/app/Build-UoOverrides.ps1`,
  `tests/Map-Overrides.Tests.ps1`, `tests/Launch-Overrides.Tests.ps1`, `tests/Build-UoOverrides.Tests.ps1` (P665's
  counts).
- Docs copy: `scripts/mapbuild/mapops.py`, `tools/tests/test_mapops.py`, this file, `notes\cc-P674-tools\` (88 KB:
  the edit scripts, the first-start and build scripts, the gate 4 mutants, the question, red and green logs).
- Edits to existing code files went through scripts: the Read tool is denied on the code copy in unattended runs.
- No file over 5 MB is tracked: the map files are in the git-ignored `files\`, the zip in the git-ignored `dist\`.
  Locks: `package`, taken and released. No Docker build, no test shard. Nothing committed.

P674 STOPPED: asked Chase (Iron-P674-20261027-153414-0e8f) which version-floor rule part 5 should use; part 7 waits for S2's server; parts 1 to 4 and 6 are done and tested
