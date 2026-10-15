# cc-P124: The player package builds from our TazUO build by default

2026-10-15. Prompt: `cc-prompts/cc-P124-package-ships-our-tazuo.md`. Both repos were clean at the start apart from the
play-test importer's machine output in `testing\`. Read first: `player-package.md`, cc-P63, cc-P68, cc-P103, cc-P111,
cc-P114.

## Headlines

- **Build package now ships our client.** `Build-PlayerPackage.ps1` with no `-TazUO` takes the folder from one place,
  the new `player-package\PackageClient.ps1` (`D:\UO\tazuo-sl-build\client`), which the console reads too. The console
  runs the script with `-Notes` only, as before, so Player package > Build package now ships TazUO `3212623f` with
  patches 0001 (P103) and 0002 (P111).
- **The client gate** refuses a folder with no `sl-build.txt` (the stock TazUO has none) and a stale build: a patch
  missing, an older patch (other SHA-256), an extra patch, another order, or another upstream commit than
  `client\TAZUO_COMMIT`. Each refusal names the problem and the rebuild command (`client\Build-Client.ps1`).
- **The add-on art gate:** nothing under `client-addons\` or `paperdoll-nsfw\` in the client folder is copied, at any
  depth, and gate 4 now holds every shipped body gump (`app\paperdoll-sfw\<id>.png`, and the six body IDs under
  `app\tazuo\ExternalImages\gumps\`) to the vendored SFW file byte for byte. The old gate caught only the kit's known
  hashes and names; a body art it had never seen passed (shown below).
- **"TazUO unknown" fixed:** the version is read from `sl-build.txt`, upstream short commit plus patch count: the real
  build says `83 MB, 741 files, TazUO 3212623f + 2 patches`, and `app\VERSION.txt` says the same.
- **The Player package tab** shows, above the zip list, the client folder Build will ship, its `sl-build.txt` as it is,
  its version, and "ready to build" or the gate's reason. A stale client is refused in the plan, before the script runs.
- Tests: 9 build-script facts (new `player-package\tests\Package-Client.Tests.ps1`) and 3 console facts, every one seen
  failing first. A real build from the default client into `player-package\dist\` (git-ignored) passed every gate.
  All suites green under Windows PowerShell 5.1.
- Nothing published; `D:\UO\haven-migration\Publish-PlayerPackage.ps1` untouched.

## What changed, file:line (ShatteredLegacy)

- `player-package\PackageClient.ps1` (new, 120 lines): the one default `:20` (`Get-PackageClientDefault` `:22`); the
  rebuild hint `:24`; `Read-ClientBuildInfo` `:30` (reads both `sl-build.txt` shapes: `built` on its own line, as
  `Build-Client.ps1` writes it, and on the upstream line, as the 2026-10-14 build has it); `Get-RepoClientPatches`
  `:62` (`client\TAZUO_COMMIT`, `client\patches\*.patch` with SHA-256); `Test-PackageClient` `:78` (the client gate);
  `Get-ClientBuildVersion` `:111`.
- `player-package\Build-PlayerPackage.ps1`: header `:8-14`; `-TazUO` with no literal default `:86`, dot-sources the
  helper and takes its default `:95-96`; the SFW body check's setup `:138-145` and its test in gate 4 `:254-258`; the
  client gate before staging `:547-549`; the add-on exclusion in the copy `:578-580`; the version from `sl-build.txt`
  `:683-686` (a stock client's `v.txt` still read as before).
- `scripts\Shard-Console.ps1`: dot-sources the helper `:155`; `PackageClient` in the config `:352-353`; the box's
  tooltip `:1353` (cc-P84's rule: every control has one); `Format-PackageClientText` `:1719`; the build plan names the
  client in its "Building from" line or refuses a stale one `:1757-1767`; `Get-PackageClientFacts` `:4755`, and `Client`
  in `Get-PackageFacts` `:4824`; the tab's read-only box (`packageClient`), filled on Refresh list `:7014-7016` and at
  start `:7919`.
- `scripts\tests\Shard-Console.Tests.ps1`: `New-PackageFacts -Client` (absent, the plans are as before), 3 facts `:5434-5475`.
- `player-package\tests\Package-Client.Tests.ps1` (new, 9 facts).
- `CHANGELOG.md` 2026.10.15.9 (`### Staff`), `VERSION` 2026.10.15.9.

## Tests

`Package-Client.Tests.ps1` runs the real builder in a child Windows PowerShell 5.1:

| Fact | What it pins |
|---|---|
| TheDefaultClientIsOurBuildAndTheBuilderTakesItFromTheHelper | the helper's default is our build; the builder has no literal default and dot-sources the helper |
| AClientWithNoSlBuildTxtIsRefusedWithHowToRebuild | a folder with a TazUO.exe and no sl-build.txt: no zip, names sl-build.txt and Build-Client.ps1 |
| ABuildMissingAPatchIsRefusedAsStale | sl-build.txt with only 0001: "STALE CLIENT BUILD", names 0002 |
| ABuildWithAnOlderPatchOrAnotherCommitIsRefusedAsStale | an older 0001 hash; another upstream commit (names TAZUO_COMMIT) |
| TheGateReadsTodaysAndTheOlderSlBuildTxtShape | both sl-build.txt shapes pass the gate |
| TheClientVersionComesFromSlBuildTxt | "<8-hex> + 2 patches"; none without sl-build.txt |
| ARealBuildFromAClientHoldingTheNsfwAddOnShipsNoneOfIt | a real build from a copy of our client with the local add-on planted inside it (and a Topless body over its ExternalImages 12.png) passes every gate and the zip holds no add-on file by name or SHA-256 |
| TheBuildReportsTheClientVersionFromSlBuildTxt | that build's summary and app\VERSION.txt say "TazUO 3212623f + 2 patches", never unknown; sl-build.txt ships beside TazUO.exe (the launcher reads it, P111) |
| AZipWhoseBodyArtIsNotTheSfwSetFailsTheCheck | the same zip with app/paperdoll-sfw/12.png replaced by unseen art fails -CheckZip with "NSFW GATE ... 12.png" |

Console (`Shard-Console.Tests.ps1`): `P124_TheConsoleShipsOurClientBuildByDefault`,
`P124_ThePackageTabShowsTheClientFolderAndItsSlBuildTxt` (the box names the folder, shows every sl-build.txt line and
the version; after Refresh, a stale and a stock folder say so), `P124_ABuildPlanNamesTheClientAndRefusesAStaleOne` (the
same four steps, the "Building from" line naming the client; a stale client refused and no window opened).

**Each seen failing first:**
- Build-script facts, against HEAD's `Build-PlayerPackage.ps1` (swapped in for the run, then restored; hash checked):
  7 of 9 failed. The fake clients went past where the gate now stands and stopped only at gate 6; the planted add-on
  stopped the real build at gate 4, so its two dependent facts had no zip.
- The two helper-only facts, with `PackageClient.ps1` broken (the one-line shape not read, the version without its
  patch count): both failed.
- The body fact on its own: HEAD's `-CheckZip` on the swapped zip printed "GATE 4 passed"; the new one fails it with
  "NSFW GATE: app/paperdoll-sfw/12.png is not the SFW body".
- Console facts, before the console change: 3 of 3 failed.
- A test-harness slip found on the way and fixed: with `ErrorActionPreference Stop`, Windows PowerShell 5.1 turns a
  child's first stderr line into a terminating error, so the first harness read only that line. And in PowerShell the
  comma binds tighter than `+`, so `'TazUO upstream ' + $x, 'built ...'` made one line; both test files now
  parenthesise it, so the separate-line shape is really exercised.

**Suites, Windows PowerShell 5.1:** `Package-Client` 9/9, `Paperdoll-Bodies` 9/9, `Launch-Settings` 27/27,
`Build-UoOverrides` 12/12, `Cliloc-Overrides` 10/10, `Shard-Console` **317/317**. Three full console runs: the first
failed only `P84_EveryControlInTheWindowHasATooltip` (my new box had no tooltip; added); the second failed only
`P84_TheUOLookAddsUnderASecondToTheStart` ("UO adds 1836 ms", a timing fact whose window builds took 33-37 s on a busy
machine; my change adds the same to both looks, and the fact passed in the first and third runs); the third was all
green.

## The real build

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1 -Notes
"P124 real build: our TazUO client"` (no `-TazUO`): `player-package\dist\ShatteredLegacy-2026.10.15.1354.zip`, every gate
passed, `83 MB, 741 files, TazUO 3212623f + 2 patches`; `-CheckZip` on it: gates 4, 6 and 5 passed. `app\VERSION.txt`:
`TazUO 3212623f + 2 patches`, `built from ShatteredLegacy 3841faa + uncommitted player-package changes`. No entry names
the add-on. `dist\` is git-ignored (`git check-ignore -v`: `.gitignore:66:player-package/dist/`). Not published; the
console refuses Build on an uncommitted tree anyway, so Chase's own Build after the commit is the one to publish.

## Deviations and decisions for Chase

1. **The add-on in a client folder is left out, not refused.** Chase's own test client may hold
   `client-addons\paperdoll-nsfw\` (P111); refusing would block every build from such a folder. It is excluded by name at
   any depth, the client's own `ExternalImages\` is not copied at all (as before), and gate 4 checks names, the kit's
   hashes, every add-on file on this machine and now the six body gumps against the SFW set.
2. **version.json carries no client version,** so it is unchanged (the prompt: "if it carries one"). Launchers and
   Publish-PlayerPackage.ps1 read it; adding a field is not needed for the fix.
3. **"Stale" is strict:** any difference from `client\patches\` (name, hash, order, extra) or `client\TAZUO_COMMIT`.
   After any patch change, `client\Build-Client.ps1` must run before the next package.
4. **The console refuses a stale client in the plan**, before the script's own gate would, so no window opens for it.

## For Chase

From now on, Player package > Build package ships our client (TazUO 3212623f with our two patches); then Publish as usual.

## Repo size rule

No pending file is over 5 MB (the largest is `Shard-Console.ps1`, as before). The real build's 83 MB zip is in
`player-package\dist\`, git-ignored (proven above); test scratch went to `%TEMP%`.

## Not mine, pending in the docs repo

`notes/art/bestiary/stock-body-5.vd` (193,847 bytes) and `stock-body-6.vd` (79,964 bytes) appeared at 14:56, during
this task. Nothing in either repo's scripts or tests writes them (searched for the names); I did not create, open or
change them. They are not the importer's or the bot's output, so the Golem's commit would carry them in with P124:
Chase, say whether they should be committed.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: `player-package/PackageClient.ps1` (new), `player-package/Build-PlayerPackage.ps1`,
`player-package/tests/Package-Client.Tests.ps1` (new), `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`,
`CHANGELOG.md`, `VERSION`. docs: this note, the importer's `testing/SUMMARY.md` and `testing/play-tests.json`, and the two
`.vd` files above (not mine).

P124 DONE
