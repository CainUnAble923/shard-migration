# cc-P63: Player package and test deploy buttons in the Shard Console

2026-10-05. Builder in `D:\ShatteredLegacy`, scripts only, no Docker build. Brief:
`D:\UO\cc-prompts\cc-P63-console-package-and-deploy.md`. Pattern followed: cc-P60 (the Commit tab).

## Headlines

- **A Player package tab** with **Build package** (`package.build`) and **Publish package**
  (`package.publish`), and **Test shard > Deploy built image...** (`test.deploy`). All three are Mutates,
  RunIn window, refused with no `-Mode` (D37), printed under `-Mode DryRun`, and run the existing scripts
  as they are: `player-package\Build-PlayerPackage.ps1`, `D:\UO\haven-migration\Publish-PlayerPackage.ps1`,
  `docker tag` plus `docker\uo\Start-TestShard.ps1 -Down` / `-SkipBuild`.
- **Build package** needs a notes line (passed as `-Notes`, crossing the child command line as base64 and
  reaching the script by name in-process, so quotes, `$` and `;` arrive unchanged), runs the build, then
  `-CheckZip` on the one zip that build wrote, and shows the zip, version, notes and gate lines. It is
  **refused while the shard repo has any uncommitted file**, every file named (first 10, then "and N more").
- **Publish package** lists `dist\` newest first with version, notes (from `version.json`), size and built
  time. It is **blocked before the phrase** when the zip's `version.json` does not describe the zip
  (missing, unparsable, version, sha256 or bytes). Phrase: **`publish player package`**, with "This is
  PUBLIC" said first. The script then asks its own "Type yes" in the window, which stays open.
- **Deploy built image** offers `sl-modernuo:cc-p*` newest first, with id, created time and which one
  `latest` is now. Phrase: **`deploy to test`**. Then `docker tag`, `-Down`, `-SkipBuild`, stopping at the
  first failure; the old `latest` id and a "To roll back: deploy <tag>" line are said in the window.
- **Live is not affected by moving `sl-modernuo:latest`, checked rather than assumed:** the live container
  `sl-modernuo` was created from `uo-modernuo` (`docker inspect`: Config.Image `uo-modernuo`, running
  `bc04a35bf344`), because `docker/uo/docker-compose.yml` has `build:` and no `image:` (D29), and a restart
  keeps the image a container runs. The confirmation says so, computed from the live container each time.
- **Facts: 130, all green** (112 before plus 18 new). Five gates broken on purpose in one run went 7 facts
  red; the file was restored byte-identical (SHA-256 checked).
- **One real `package.build` through the console's code path passed** (gates 1 to 6, then 4, 6 and 5 again):
  `ShatteredLegacy-2026.10.05.1514.zip`, 76.4 MB. It was built from a **clean local clone of HEAD
  `9ab57e4`** in my scratchpad, not from `D:\ShatteredLegacy`, because the real tree held someone else's
  uncommitted work and the new guard refused it (section 5). Nothing was published, no tag moved, no shard
  restarted.
- **Not mine, seen while working:** `sl-modernuo:latest` moved from `9349dc9c9826` (cc-p61) to
  `b04ed61adb5a` (cc-p62) during this session; my docker calls were reads only (`images`, `inspect`). The
  working tree gained modified `design/kitsune-ears-tail/stage2-final/*.png` (3),
  `player-package/vendor/shattered-legacy-art/gumps/64783.png`, and 5 untracked kitsune reference files. I
  touched none of them. A commit right now would include them.

## 1. What changed

All in `D:\ShatteredLegacy`, uncommitted. `git diff --numstat`: `scripts/Shard-Console.ps1` +549 / -18,
`scripts/tests/Shard-Console.Tests.ps1` +435 / -5, `CHANGELOG.md` +3. New file
`scripts/tests/fixtures/docker-images-sl-modernuo-2026-10-05.txt` (72 lines, real `docker images` output).

`scripts/Shard-Console.ps1`:

- `:49-56` header: the three new things it calls.
- `:84-88` parameters `-PackageNotes`, `-PackageNotesB64` (what a click passes), `-PackageZip`, `-ImageTag`.
- `:113` `$script:PublishPublicWarning`.
- `:172-178` `Get-ConsoleConfig`: `BuildPackage`, `PackageDist`, `PublishScript`
  (`D:\UO\haven-migration\Publish-PlayerPackage.ps1`), `DeployTagPattern` (`^sl-modernuo:cc-p[A-Za-z0-9._-]*$`).
- `:276` `ConvertFrom-ImageTagListing`: `docker images` lines to Tag, Id, Created (UTC), newest first.
- `:553-570` `Get-ConfirmPhrase` (two phrases) and `Get-ConfirmSubject` (the dialog title per action).
- `Get-ConfirmPreface`: the commit warning now only for `Commit-ShardWork.ps1` (it fired for any real
  script step), and the public warning for `Publish-PlayerPackage.ps1`.
- `:618-623` `Get-ChildArgumentLine`: notes as base64; zip name and image tag quoted.
- `Get-ModeBanner`: `(player package)`, a BUILDING banner ("Nothing is published") and a publish banner.
- `:692`, and the end of `Get-ConsoleActions`: the three actions.
- `New-PlanStep`: a new step kind `checkzip`.
- `:861-960` the player package core: `Test-PackageNotes`, `Get-PackageZipProblems` (the guard),
  `Get-RolloutReminder`, `Get-PackagePlan`.
- `:962-1020` the deploy core: `Get-DeployCandidates`, `Get-DeployLiveLine`, `Get-DeployPlan`.
- `:1032-1034` `Get-ActionPlan` hands the three to those before touching any docker state it does not need.
- `:1219-1250` `Test-PlanSafety`: the only `docker tag` is `sl-modernuo:cc-p*` onto `sl-modernuo:latest`,
  typed, in a plan that names no live container; in-process scripts are the commit script, the build
  (only `-Notes` / `-CheckZip`, so never `-GateSelfTest`) and the publish script (typed, only `-Zip` on a
  zip under `dist\`); a `checkzip` step only runs the build script.
- `:1293` `Format-PlanStep` prints a `checkzip` step.
- `:1418` `New-ConsoleState`: `Images`. `:2387` `Get-DockerSections` reads `docker images sl-modernuo`.
- `:2238-2330` shell, read-only: `Get-PackageZips`, `Read-ZipPackageVersion`, `Get-PackageFacts` (git status
  and HEAD of the repo, `dist\`, the picked zip's SHA-256 and `app\package-version.txt`, `git show
  HEAD:CHANGELOG.md`, the newest `cc-P<nn>` note by number).
- `:2551`, `:2581` `Invoke-Plan` runs `checkzip`: exactly one zip in `dist\` written since the plan started,
  else it fails and says how many it found.
- `:2920-3000` `Show-ListPicker`, `Show-ImagePicker`, `Update-PackageList`.
- `:3040-3060` `Invoke-ConsoleButton`: package facts instead of docker for `package.*`; the image picker
  for `test.deploy`; `Get-ConfirmSubject`.
- `:3238-3243` Test shard tab caption and the button; `:3446` the Player package tab (notes box, Build
  package, zip list, Refresh list, Publish selected), between Commit and LIVE shard.
- `:3570`, `:3610` entry: `-Action list` lines; a headless `package.*` decodes the notes and reads package facts.

`scripts/tests/Shard-Console.Tests.ps1`: `New-PackageZipRow` / `New-PackageFacts` (`:112`), `New-DeployState`
(`:129`, the capture plus the real images listing), `Get-Plan` and `Invoke-ClickCapture` take the new
arguments and stub `Get-PackageFacts` and `Show-ImagePicker` (`:1026`), the window cases cover the three
(`:1048`), the form fact expects the tab and the button (`:974`), and 18 `P63_` facts (`:1666-2030`).

`CHANGELOG.md:41`: a `### Staff` list in `## 2026.10.05.2`: "Shard Console: a Player package tab builds the
player zip and publishes a chosen one, and the Test shard tab can put an image a prompt already built on the
test shard. Publishing and deploying each ask for a typed phrase first." **Same deviation as P60:** that
section is committed (`8a7e754`), so the header's rule would make a new `2026.10.05.3`, but `### Staff` is
not read by the server (`server/customizations/ShardVersion.cs:111-117` reads only Added, Changed, Fixed), so
that version would be empty and show no login bulletin. VERSION not bumped. Wiki not published.

`Publish-PlayerPackage.ps1`: not edited. Suggestions in section 7.

## 2. The confirmations, exactly as shown

Rendered from the code (`Get-ConfirmSubject`, `Get-ConfirmPreface`, the confirm step, `Format-Plan`, as
`Show-TypedConfirm` joins them) on real state: the publish on the zip built in section 5, the deploy on
`docker` as it was at 15:2x.

**Publish package**

```
window title: Publish player package: type to confirm
BEFORE YOU TYPE: This is PUBLIC: every player's launcher is offered this package at its next start.

This publishes ShatteredLegacy-2026.10.05.1514.zip (version 2026.10.05.1514) to get.shatteredlegacyuo.com and the website, and its version.json tells every installed launcher to offer it.

This will run:
  1. CONFIRM  typed: you must type exactly 'publish player package'. This publishes ShatteredLegacy-2026.10.05.1514.zip (version 2026.10.05.1514) to get.shatteredlegacyuo.com and the website, and its version.json tells every installed launcher to offer it.
  2. SAY      zip ShatteredLegacy-2026.10.05.1514.zip, version 2026.10.05.1514, 76.4 MB, built 2026-10-05 15:14:18. What is new: P63 console check build of 9ab57e4; not for release
  3. RUN      & 'D:\UO\haven-migration\Publish-PlayerPackage.ps1' -Zip '<scratchpad>\sl-head\player-package\dist\ShatteredLegacy-2026.10.05.1514.zip'
         # Publish-PlayerPackage.ps1: shows the zip, asks you to type yes HERE, then gates, copies to Haven, swaps in and checks both URLs, rolling back on a mismatch.
  4. SAY      Read the script's own last line above: PUBLISHED, NOT PUBLISHED, or Nothing done (it exits 0 when the answer is not yes).
  5. LOG      one timestamped line: package.publish ShatteredLegacy-2026.10.05.1514.zip
label: Type exactly:  publish player package
```

When the newest committed CHANGELOG section or the newest `cc-P<nn>` note gives the "package, then server"
rollout order, a step is added after step 2 (fact `P63_ThePublishRemindsThatTheServerFollowsWhenTheNotesSaySo`,
which holds the exact text): `SAY      Reminder: <file> says <that order>. The server deploy follows this
publish; it is not part of this button.` (Not quoted word for word here, or this note would trigger it.) A
warning only. It did not fire here: the newest
note is this one, and the newest committed section (2026.10.05.2) does not say it.

The window it opens says first:

```
==============================================================================
  RUNNING FOR REAL  package.publish (player package)
  This is PUBLIC: every player's launcher is offered this package at its next start. Publish-PlayerPackage.ps1 asks "Type yes" itself, below.
==============================================================================
```

**Deploy built image**

The picker first (`Get-DeployCandidates`, top five of 30):

```
sl-modernuo:cc-p62       b04ed61adb5a  2026-10-05 14:19:04  <- latest now
sl-modernuo:cc-p61       9349dc9c9826  2026-10-05 10:47:51
sl-modernuo:cc-p57       d5519301f920  2026-10-05 09:04:06
sl-modernuo:cc-p56       9d6829869880  2026-10-05 08:04:03
sl-modernuo:cc-p55       b574b7e9fb95  2026-10-05 07:27:46
```

Then, picking cc-p61:

```
window title: Deploy to test: type to confirm
This points sl-modernuo:latest at sl-modernuo:cc-p61 (9349dc9c9826, built 2026-10-05 10:47:51) and restarts the TEST shard on it. Live does not use this tag: sl-modernuo was created from 'uo-modernuo', and a restart keeps the image it runs, so moving sl-modernuo:latest changes nothing live. Only the live drift line compares against it.

This will run:
  1. CONFIRM  typed: you must type exactly 'deploy to test'. (the same text)
  2. SAY      sl-modernuo:latest before this deploy: b04ed61adb5a, built 2026-10-05 14:19:04.
  3. RUN      docker tag sl-modernuo:cc-p61 sl-modernuo:latest
         # Point sl-modernuo:latest at sl-modernuo:cc-p61. A tag only: no build, no gates (they ran when sl-modernuo:cc-p61 was built).
  4. SAY      To roll back: deploy sl-modernuo:cc-p62 (b04ed61adb5a).
  5. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down
         # docker/uo/Start-TestShard.ps1 -Down: compose down on the sl-uo-test project only (D22). The shard saves on stop (D36 fix, seen in its log since this start). If the stop times out, play since the last autosave is lost.
  6. RUN      powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild
         # docker/uo/Start-TestShard.ps1 -SkipBuild: sl-modernuo-test on the new sl-modernuo:latest, then waits for the listener.
  7. LOG      one timestamped line: test.deploy sl-modernuo:cc-p61 (9349dc9c9826), sl-modernuo:latest was b04ed61adb5a, built 2026-10-05 14:19:04
label: Type exactly:  deploy to test
```

If no `cc-p` tag names the old image, step 4 says `To roll back: docker tag <old id> sl-modernuo:latest, then
Test shard > Start (no cc-p tag names <old id>).` If live had been created from `sl-modernuo:latest`, the live
line would instead say: `LIVE was created from sl-modernuo:latest. A restart keeps the image it runs; the next
time live is recreated (a deploy) it would get this image.`

**Build package** has no phrase (it publishes nothing). Its window says
`BUILDING  package.build (player package)` / `Build-PlayerPackage.ps1 writes a zip into player-package\dist.
Nothing is published.`

## 3. Refusals and guards, wording

Each goes to the Output box as `<action>: <text>` and no window opens, no phrase is asked.

- Dirty tree: `D:\ShatteredLegacy has 13 uncommitted file(s), so the package would not be built from a commit:
  <first 10, comma-separated> and 3 more. Commit first (Commit tab), then build.` Every path git would commit
  counts, untracked included (`--untracked-files=all`, the list the commit script reads). A failed git status is
  a refusal too, never "clean" (D66).
- Notes: blank, `A package needs notes: the one line launchers show as "What is new". Type it in the Notes box.`;
  not printable ASCII on one line, `Notes must be one line of plain ASCII ...` (the build script's own rule,
  said before anything runs).
- Publish guard, each prefixed `Not publishing: `: no `version.json`, unparsable, `version.json says version X,
  the zip's app\package-version.txt says Y.`, `version.json says sha256 X, the zip is Y.`, `version.json says N
  bytes, the zip is M.` Also: nothing chosen, a name not in `dist\`, the script missing.
- Deploy: no image chosen; a tag that is not `sl-modernuo:cc-p*` (so never `latest`, `pre-bump-*` or
  `uo-modernuo`); a tag docker does not have; `sl-modernuo:latest already is <tag> (<id>). Nothing to deploy;
  Test shard > Start starts the test shard on it.`; cancelling the picker.

**Deviation: Deploy refuses a pick that `latest` already is.** The brief does not say; retagging to the same id
would only restart the test shard, which Test shard > Start already does without a phrase.

## 4. Tests

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`:
**130 facts, 130 passed, 0 failed** (112 before, all still green). The existing D37 facts now include the three
actions (every window action, dry, real and toggled, and a capture console that cannot run them). New:

| Fact | What it holds |
|---|---|
| P63_TheThreeActionsExistWithTheirGroupMutatesAndRunIn | Group, Mutates true, RunIn window, the phrases and dialog titles |
| P63_D37WithNoModeEachIsRefused | `Resolve-RunMode` refuses all three with no mode; any dry wins; banners |
| P63_TheRealChildGivenNoModeRefusesEachAndCallsNoDocker | a real `powershell.exe` on each click's line minus mode, phrase and notes: exit 2, REFUSED, no docker call, nothing past the banner |
| P63_TheDryRunPlansPrintTheCommandLinesWithNotesQuoted | the build line with `-Notes` (quotes, `$`, `;`, `&`, `%`, and `-GateSelfTest` as text) parses back to the notes; the CHECK, publish and deploy lines; tag, down, start order |
| P63_NotesCrossTheChildCommandLineUnchanged | the click's line run by a real dry child prints the exact `-Notes '...'`; no docker |
| P63_PackageBuildRefusesOnADirtyTreeAndNamesTheFiles | the wording, "and 3 more", no window, no override; git failure refuses; clean builds |
| P63_PackageBuildNeedsOneLineOfAsciiNotes | blank, spaces, two lines, a curly quote, an em dash |
| P63_TheZipPickerReadsVersionJson | a real temp `dist\` with three real zips: newest first, notes and sha256 read, missing and unparsable json, the stamp inside the zip, each guard case |
| P63_APublishWhoseVersionJsonDoesNotMatchIsBlockedBeforeThePhrase | sha mismatch, no json, nothing chosen, not in dist, no script: no phrase, no window |
| P63_PublishAsksThePhraseSaysPublicFirstAndOpensItsWindow | the phrase, `-NoExit`, the line, the preface; the commit keeps its own preface |
| P63_ThePublishRemindsThatTheServerFollowsWhenTheNotesSaySo | from the newest note, from the newest changelog section, never the header's example or an older section; a warning only |
| P63_ImageTagListingParsesRealDockerOutput | the real listing: ids, CDT to UTC, cc-p only, newest first, which is latest |
| P63_TestDeployShowsTheOldLatestAndHowToRollBack | step kinds, the old id, rollback by tag and by id, five refusals, the picker and its cancel |
| P63_TheLiveLineIsReadFromWhatLiveWasCreatedFrom | the line from the capture (`uo-modernuo`), and the other wording |
| P63_TestDeploysPlanNeverNamesTheLiveContainer | for every cc-p tag: no word equal to `sl-modernuo`, no live compose file or image, one docker command (the tag), safety passes; and the safety check refuses a deploy with a live restart or live check slipped in, a tag onto `uo-modernuo:latest`, from a non cc-p image, or with no phrase |
| P63_ADeployStopsAtTheFirstFailureAndSaysHowToRollBack | the real executor with the recording docker (exit 1): one docker call, FAILED at step 3, nothing after it, logged; a wrong phrase runs nothing |
| P63_ABuildRunsTheScriptWithTheNotesThenChecksTheZipItWrote | a stand-in build script gets every character of the notes; `-CheckZip` gets the new zip, not an older one; the zip, version and gate lines are shown; a build that wrote no zip fails at the check |
| P63_TheSafetyCheckGuardsTheNewScripts | `-GateSelfTest` refused, publish without phrase, outside `dist\` or without `-Zip` refused, another checker or script refused |

**Each gate watched failing.** One run with five breaks: `test.deploy` Mutates false, the dirty-tree refusal
skipped, the deploy names-live safety rule skipped, notes put raw on the child line, the publish guard skipped.
7 facts went red, each break caught by the facts meant for it. The file was restored and its SHA-256 compared
(OK). With Mutates false the real no-mode child ran `test.deploy` as "execute", read docker through the recorder
(exit 1, so no images) and refused at "no image tagged": it was also carrying no phrase, so it could not have run.
The older fact `AChildGivenNoModeRefusesEveryActionThatChangesSomething` stayed green under that break, because it
takes its expectation from `Mutates` itself; `P63_D37WithNoModeEachIsRefused` names the three outright.

**Read-Host in-process.** A stand-in publish script with Publish's `Read-Host` / "Nothing done" / exit shape, run
through `Invoke-ScriptStep` with `yes` and then `no` on stdin, took both branches and returned 0 both times; the
prompt itself never enters the output pipeline (it is not in the output file), as expected for the host prompt.

## 5. The real build

`D:\ShatteredLegacy` refused, as it should. The console line the Build button's window runs, on the real tree:

```
== PLAN: package.build (package) ==================================================
  1. REFUSE   D:\ShatteredLegacy has 13 uncommitted file(s), so the package would not be built from a commit: design/kitsune-ears-tail/stage2-final/paperdoll_260x237.png, design/kitsune-ears-tail/stage2-final/paperdoll_260x237_gray.png, design/kitsune-ears-tail/stage2-final/paperdoll_260x237_partialhue.png, player-package/vendor/shattered-legacy-art/gumps/64783.png, scripts/Shard-Console.ps1, scripts/tests/Shard-Console.Tests.ps1, design/kitsune-ears-tail/reference/ingame/ingame_walk_downleft_6x.png, design/kitsune-ears-tail/reference/ingame/ingame_walk_downright_6x.png, design/kitsune-ears-tail/reference/paperdoll_Gump_00013_EA_female_body.png, design/kitsune-ears-tail/reference/paperdoll_Gump_00013_female_body.png and 3 more. Commit first (Commit tab), then build.
exit=1
```

Note `player-package/vendor/shattered-legacy-art/gumps/64783.png` in that list: a build from this tree would
ship an uncommitted gump. That is the case the guard is for.

**Deviation: the real build ran on a clean local clone.** `git clone --local --no-hardlinks D:\ShatteredLegacy
<scratchpad>\sl-head` (HEAD `9ab57e4`, status empty), with `client-data` as a junction to the real one (gitignored;
gate 4 reads EA file names from it) and `vendor\vc-runtime\vcruntime140.dll` copied in (gitignored by
`.gitignore:69`; the build checks its SHA-256 and Microsoft signature, and the first run without it stopped at
that gate). Then the console from the working copy, against the clone:

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Shard-Console.ps1 -RepoRoot
<clone> -Mode Execute -Action package.build -PackageNotes 'P63 console check build of 9ab57e4; not for release'`
Exit 0. Output (`<clone>` = `C:\Users\ckfle\AppData\Local\Temp\claude\...\scratchpad\sl-head`):

```
==============================================================================
  BUILDING  package.build (player package)
  Build-PlayerPackage.ps1 writes a zip into player-package\dist. Nothing is published.
==============================================================================
== PLAN: package.build (package) ==================================================
  1. SAY      Building from <clone> at 9ab57e4, committed and clean. The zip goes to <clone>\player-package\dist; nothing is published.
  2. RUN      & '<clone>\player-package\Build-PlayerPackage.ps1' -Notes 'P63 console check build of 9ab57e4; not for release'
  3. CHECK    & '<clone>\player-package\Build-PlayerPackage.ps1' -CheckZip '<the one zip in <clone>\player-package\dist written since this plan started>'
  4. LOG      one timestamped line: package.build

[2/4] Build-PlayerPackage.ps1: stage, gates 1 to 3, zip, gates 4 to 6, version.json. A failing gate stops it and deletes the zip.
  gate 6: 123 native files checked, 172 skipped (IL-only .NET, non-Windows, excepted)
  built <clone>\player-package\dist\ShatteredLegacy-2026.10.05.1514.zip
        <clone>\player-package\dist\ShatteredLegacy-2026.10.05.1514.version.json
  76 MB, 740 files, TazUO 26.0909.63
  unsigned: SmartScreen will warn on first run; README.txt tells players what to do.
[3/4] Build-PlayerPackage.ps1 -CheckZip on the zip the step above wrote: gates 4, 6 and 5 again, on the file itself.
  GATE 4 passed: <clone>\player-package\dist\ShatteredLegacy-2026.10.05.1514.zip
  gate 6: 123 native files checked, 172 skipped (IL-only .NET, non-Windows, excepted)
  GATE 6 passed: <clone>\player-package\dist\ShatteredLegacy-2026.10.05.1514.zip
  GATE 5 passed: <clone>\player-package\dist\ShatteredLegacy-2026.10.05.1514.version.json
      zip     <clone>\player-package\dist\ShatteredLegacy-2026.10.05.1514.zip
      version 2026.10.05.1514, 76.4 MB. What is new: P63 console check build of 9ab57e4; not for release
      gates   1 to 6 passed in the build, and 4, 6 and 5 again on the zip just above. Nothing is published: Player package > Publish package does that.
[4/4] logged to <clone>\scripts\shard-console.log
package.build: done.
```

`version.json`: version `2026.10.05.1514`, sha256 `2736e9676ba1712a57b3c89e8004f8e8c6d7d6c5b65d81ad0c67fd6b3d1f9a07`,
80155162 bytes. **The zip stays in the scratchpad clone, not in `D:\ShatteredLegacy\player-package\dist\`**, so a
"not for release" zip never appears in the Publish list. Then `-Mode DryRun` of `package.publish` on that zip
(section 2) and of `test.deploy` against real docker: both printed and exited 0; `sl-modernuo:latest` was still
`b04ed61adb5a` afterwards.

## 6. Unverified

- The tab, picker and dialogs were built in a test and driven through `Invoke-ConsoleButton` with stubs, never
  clicked by hand.
- Publish's "Type yes" prompt inside a real console window: checked only with stdin redirected (the answer is
  read; the prompt is host output, not pipeline output). A by-eye look is item 5 in For Chase.
- `test.deploy` and `package.publish` were never run for real, by the brief. The deploy executor ran with a
  recording docker; the publish only as a dry plan and a stand-in.
- Moving `latest` and live: established from `docker inspect sl-modernuo` and the compose file today. If live is
  ever recreated from `sl-modernuo:latest`, the confirmation switches wording by itself (fact covers both).

## 7. What Publish-PlayerPackage.ps1 should change (described, not done)

1. **"Nothing done." exits 0**, the same as PUBLISHED. The console cannot tell a declined publish from a
   finished one, so it says "done" either way and asks Chase to read the last line. Suggest `exit 3` (or any
   non-zero distinct from 1) when the answer is not `yes`.
2. **With no `-Zip` it publishes the newest zip by write time.** The console always passes `-Zip`, and its safety
   check refuses a publish step without it, but a hand run straight after a test build (like section 5's, if it
   were in `dist\`) would offer that one. Suggest printing the version.json notes above the prompt in a colour,
   or requiring `-Zip`.
3. Its `-CheckZip` uses `D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1` (`$Pkg`, hard-coded), so a zip
   is gated by the working tree's build script, which may be uncommitted. Fine today; worth a line in its header.

## Known limits

- The rollout reminder reads the newest `cc-P<nn>` note by number, so between prompts it reads whichever task
  ran last, and it matches a sentence giving the order, not a heading. This note avoids that sentence on purpose.
- `checkzip` finds the build's zip by time; two builds at once would both fail at the check (it wants exactly one).

## For Chase

1. Commit the usual way. Look first at the kitsune files and `player-package/.../gumps/64783.png`: not from P63.
2. Open the console. **Player package** sits between Commit and LIVE shard. Click **Build package** with the notes
   box empty: the Output box says it needs notes. While anything is uncommitted it lists the files instead.
3. With a clean tree, type a notes line with a quote in it, tick **DRY RUN**, click **Build package**: a window
   says DRY RUN and prints `-Notes '...'` with the quote doubled. Untick and build for real: the window shows the
   build, then GATE 4, 6 and 5 on the new zip, then the zip, version and notes in green. **Refresh list** shows it
   at the top.
4. Select an old zip with no `version.json` (if any) and click **Publish selected**: refused, named. Select a good
   one: the dialog says PUBLIC first and wants `publish player package`. Type it, then in the window the script
   shows the zip and asks "Type yes"; answer `no` to back out (it says Nothing done).
5. While there, check the "Type yes" prompt is visible in that window (section 6).
6. **Test shard > Deploy built image...**: a list of `sl-modernuo:cc-p*`, newest first, with "<- latest now".
   Pick one, read the live line in the dialog, type `deploy to test`. The window says the old id and "To roll
   back: deploy <tag>", tags, stops and starts the test shard. Deploy the old tag the same way to roll back.
7. Pick the image latest already is: refused, nothing asked.

P63 DONE
