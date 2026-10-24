# P511: Review of the player package building from our TazUO build

Reviewed 2026-10-23. Notes only. Code reviewed at `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`, which is also local `main`; P124 commit `00153a5609b9ba119f43d181980ec85bf2fdce41` is its ancestor. Read both work copies' AGENTS.md, the direction decision and task list, and `notes/cc-P124-package-ships-our-tazuo.md`. No separate P124 review was found beside that note or in the notes referencing P124. The findings below are additional to its implementation report.

## Findings

1. **Bug, `player-package/Build-PlayerPackage.ps1:661`: Checking an existing package skips the client stamp gate.** `-CheckZip` reports success for a zip whose `app/tazuo/sl-build.txt` names an unrelated upstream commit and contains no patches, so checking a selected package does not establish that it contains the required client build. Validate the archived stamp against the current pin and patches, and add rejection tests for missing, stale, extra and reordered patch records in an existing zip.

2. **Risk, `player-package/PackageClient.ps1:82` and `player-package/Build-PlayerPackage.ps1:985`: The accepted stamp is not tied to the executable assemblies.** A current stamp passes the client gate with `TazUO.dll` missing or replaced, and gate 3 only compares staged files with that same input folder, so mixing an older assembly into the folder can ship a different client under the current version. Have the client builder record the required published files and their hashes, verify them before staging and in the archive, and add missing/replaced assembly rejection tests.

3. **Risk, `client/Build-Client.ps1:70` and `client/Build-Client.ps1:86`: Skipping client tests still produces a shippable build stamp.** `-SkipTests` bypasses `dotnet test` but writes the same stamp as a tested build, which `Test-PackageClient` accepts without evidence that tests ran. Record whether the required client tests passed, refuse skipped-test builds when packaging, and cover both outcomes with a regression test.

## Evidence and verification

- Read the P124-listed implementation and tests: `player-package/PackageClient.ps1`, `player-package/Build-PlayerPackage.ps1`, `player-package/tests/Package-Client.Tests.ps1`, the package configuration/facts/plans/display in `scripts/Shard-Console.ps1`, and the P124 cases in `scripts/tests/Shard-Console.Tests.ps1`. Also read `client/Build-Client.ps1`, `client/README.md`, `client/TAZUO_COMMIT`, and the archive checks' Legion scripts helper. P124's changelog and version changes were inspected through its commit.
- All four current patches applied sequentially with `git apply --check` followed by `git apply` to temporary copies of their target files read directly from pinned TazUO commit `3212623f63436be1c0f4e3b308b202b29597c026`. Files checked: `0001-enhanced-packet-client-command.patch`, `0002-paperdoll-bodies-option.patch`, `0003-shard-buttons-achievements.patch`, and `0004-world-map-fog-of-war.patch`. No patch application failure found. The source clone was read only.
- Existing PowerShell tests run under `powershell.exe`, Windows PowerShell `5.1.26100.9711`: `P124_TheDefaultClientIsOurBuildAndTheBuilderTakesItFromTheHelper`, `P124_TheGateReadsTodaysAndTheOlderSlBuildTxtShape`, and `P124_TheClientVersionComesFromSlBuildTxt`. All three passed, suite exit 0. The remaining package tests and console tests were read, not run.
- Finding 1: the current builder's `-CheckZip` passed gates 4, 6 and 5 on the local artifact `D:\ShatteredLegacy\player-package\dist\ShatteredLegacy-2026.10.23.1001.zip`, exit 0. Copied it outside both repos, replaced only the client stamp with upstream `1111111111111111111111111111111111111111`, date `2000-01-01 00:00`, and no patch lines, and updated the sidecar's hash and byte count; the same checks still passed, exit 0. Used `-UoData D:\ShatteredLegacy\client-data\classic-client` for local file-name checks, with no network calls.
- Finding 2: isolated client folders holding the real apphost and a current stamp returned zero `Test-PackageClient` problems with no `TazUO.dll`, and again with a substituted assembly. In the copied archive above, replaced `app/tazuo/TazUO.dll` with the valid, unrelated `ClassicUO.IO.dll` from the local build and updated the sidecar; gates 4, 6 and 5 still passed, exit 0. This exercises the finished-zip checks, not a player launch.
- Finding 3: executed the unchanged `client/Build-Client.ps1 -SkipTests` in an isolated PowerShell process with temporary output and local `git` and `dotnet` stand-ins. The stand-ins recorded zero test calls, the real script wrote its normal current stamp, and the client gate returned zero problems; no real client compilation or test pass is claimed by this probe.
- The existing helper and console fixtures deliberately accept placeholder executables with current stamps. No existing P124 test asserts binary identity, rejects a skipped-test stamp, or rejects a stale stamp inside an existing archive. The real-package test explicitly supplies `-TazUO`; the no-argument default is checked structurally and by the original P124 manual build report.

## Limits and scope

No new tests or code changes were made. No full TazUO rebuild, player launch, clean-PC installation or player login was performed. The probes establish the gates' behavior, not that a wrong client has actually been published. No Haven connection, deployment, account operation, commit, merge, push or branch switch occurred.

Ran the required progress reporter with both work-copy path overrides and `--dry-run`, exit 0. Despite that flag, it rewrote `tools/progress.json`; restored that incidental change byte for byte from HEAD so this task changes only this note.

Temporary probe artifacts remain outside both repositories in `%TEMP%\sl-p511-apply-review` and `%TEMP%\sl-p511-probe-review`, plus the initially created, inaccessible directory `%TEMP%\sl-p511-apply-d6ytrh2y`. Automatic approval review rejected their cleanup with "blocked by policy"; no further cleanup was attempted. No file over 5 MB was added to either repository.

P511 DONE
