# cc-P713: the Siege of Sosaria map stays out of releases until the swap goes live

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P713`. Not committed; nothing published or deployed.

## In plain words

- **The next player package ships the same land as today's.** The Siege of Sosaria map that P674 added is now behind
  one switch, and the switch is off. The download stays about 146 MB, not 181 MB. Players get the stock Trammel and
  Felucca with our own changes on top, now including the Wakening Isle, the same way as the 2026.10.26.1648 package.
- **The switch is one word in one file:** `player-package\vendor\sos-trammel-map\switch.txt` says `off`. The swap's
  go-live release changes it to `on`. Any other word, or a missing file, stops the package build.
- **The safety checks follow the switch.** With it off, a package that holds the SoS map files, or a README that
  credits the map, is refused. With it on, a package missing them is refused, as before.
- Nothing for you to do. The tutorial isle release can be built as usual.

## What changed

| Part | Where (code copy) | What it does |
|---|---|---|
| The switch | `player-package/vendor/sos-trammel-map/switch.txt` (new) | One word, `off`. `#` lines are comments. |
| Reading it | `Build-PlayerPackage.ps1`: `Get-SosMapSwitch`, param `-SosMap on\|off` | The build reads the file, and the switch must be exactly `on` or `off` (case matters). `-SosMap` overrides it for one run: the tests use it, and so does `-CheckZip` on a package built the other way. A release build leaves it out. The build prints `land: ...` with the setting and where it came from. |
| Staging | same, the land section | **On:** unchanged from P674 (the files\ gate, `app\map\` staged, gate 3). **Off:** `files\` is not read at all, so a desk without the 141 MB of map files can build. `Remove-SosMapReadme` drops the README's 5-line `app\map\` entry from the staged copy, and stops the build if it cannot find exactly one entry. `payload\README.txt` keeps the entry for the on state. |
| Gate 4 | same, `Test-PackageZip` | **On:** P674's checks (exactly the three ship rows, byte for byte), plus the README must credit the map. **Off:** any `app/map/` file is refused ("shipped, but the Siege of Sosaria map is switched off"), and it also gets no EA-file-type exemption. A README crediting the map is refused. |
| Docs | the build script's header; `vendor/sos-trammel-map/SOURCE.txt` | How to turn it on for the swap: change `switch.txt` to `on`, run `Add-SosMap.ps1` if `files\` is empty, and build. Not before the server runs the same land. |
| CHANGELOG | `2026.10.27.4`, Staff | One ops line. |

The launcher needed no change. `Build-UoOverrides.ps1` already falls back to the player's own files when there is no
`app\map\base-map1legacymul.uop` (P674). A new fact now holds it to that.

## Proof

**Facts** (`player-package/tests/Map-Overrides.Tests.ps1`, 16 of 16 green). The new P713 facts lift the build
script's functions out by name (the script builds when run, so it cannot be dot-sourced) and run gate 4 the way the
build runs it:

| Fact | Red against HEAD (`notes\cc-P713-tools\red-new-facts-on-head.txt`) |
|---|---|
| `P713_TheSwitchIsOffUntilTheSwapGoesLive` | no `Get-SosMapSwitch` |
| `P713_ASwitchThatIsNotOneWordOffOrOnStopsTheBuild` (`On`, `yes`, two lines, comments only, missing file) | same |
| `P713_SwitchedOffTheReadmeLosesOnlyItsAppMapEntry` | no `Remove-SosMapReadme` |
| `P713_WithNoAppMapTheLauncherPatchesThePlayersOwnStockFilesAsBefore` (3 lines and the player's tile; with a base, 6) | **passes at HEAD**: it guards P674's fallback, which was already right |
| `P713_Gate4SwitchedOffRefusesAnyAppMapFileAndTheCredit` | no `-SosMap` parameter. HEAD's gate 4 also demands the three map files from a zip with none (`red-head-clean-zip.txt`) |
| `P713_Gate4SwitchedOnWantsTheThreeFilesAndTheCredit` | no `-SosMap` parameter |

**The other package test files** (`package-tests-summary.txt`): Build-UoOverrides 26/26, Cliloc 10/10,
Launch-Overrides 19/19, Launch-Settings 27/27, Legion-Scripts 24/24, Music 9/9, Paperdoll-Bodies 9/9, Redrawn-Art
6/6, Ui-Skins 4/4. I did not run Package-Client.Tests.ps1: P670 and P674 recorded it red on this desk (its child
builds look for EA client data that this desk does not have).

**Real packages** (`package` lock, taken and released twice; built with `-TazUO D:\UO\golems\Iron\tazuo-p670\client
-UoData D:\UO\tool-trials\client-data-copy`, as P674 did):

- **Switch off (the repo's setting):** `ShatteredLegacy-2026.10.27.1704.zip`, 146 MB, 741 files, every gate passed.
  It was built while `vendor\sos-trammel-map\files\` was empty on this desk, so the off build does not need those
  files.
- **Switch on (`-SosMap on`):** `ShatteredLegacy-2026.10.27.1709.zip`, 181 MB, every gate passed. I first ran
  `Add-SosMap.ps1` to rebuild `files\` (checked against the manifest).
- **Gate 4 both ways on real zips** (`checkzip-both.txt`): P674's SoS zip (1515) passes with `on` and is refused with
  the repo's `off` (3 map files, the README credit, 3 EA file types). The off zip (1704) passes with `off` and is
  refused with `on`.
- **Against the published 2026.10.26.1648 package** (downloaded from get.shatteredlegacyuo.com; SHA-256 matches its
  version.json, `27b2bdc4...`; `compare-1648.txt`). Neither package has an `app/map/` file or any `.mul`/`.uop`/`.idx`.
  `app/trammel.mapops` keeps every one of 1648's 13,189 lines but its header. Its header changed from `F 1 214` to `F 1 879`, the
  count of blocks the patch touches. The 41,753 new lines (39,440 land, 1,647 statics, 665 block fingerprints) all
  fall inside x 6592-6865, y 3904-4049: the Wakening Isle (P662, the only change to that file since 1648).
  The README differs from 1648 only by P670's redrawn-art entry and P674's "No EA game file" wording, not by any map
  line. `Apply-MapOps.ps1` and `Build-UoOverrides.ps1` differ by P674's base support. With no `app\map\`, that code
  does nothing. The map stamp's new format (`uo-map 2`) makes each player's map copies rebuild once (P674 said so).
  I did not time that rebuild on stock land.

Both zips sit in `player-package\dist\` (git-ignored), unpublished.

## Notes for the swap

- When the switch flips to `on`, `trammel.mapops` must already be re-based onto the SoS land (S2). P674 measured
  today's patch on SoS land: 4 blocks drifted and 3 removals miss. The switch does not check that. S2 owns it.
- A player who never had an on package needs nothing when it turns on. The stamp names the base, so the first start
  after the update rebuilds onto the SoS land (P674's stamp fact).

## Commit preflight

- Code copy: `CHANGELOG.md`, `player-package/Build-PlayerPackage.ps1`, `player-package/tests/Map-Overrides.Tests.ps1`,
  `player-package/vendor/sos-trammel-map/SOURCE.txt`, new `player-package/vendor/sos-trammel-map/switch.txt`. All
  ASCII. `files\` and `dist\` are git-ignored (checked with `git check-ignore`).
- Docs copy: this file and `notes\cc-P713-tools\` (61 KB: the edit scripts, the build and CheckZip scripts, the
  comparison script, and the red, green and build logs; the build logs are UTF-16).
- I edited the code copy through scripts. The Read tool is denied there in unattended runs.
- Locks: `package`, taken and released twice. No Docker build, no test shard, no Haven. Nothing committed.

P713 DONE
