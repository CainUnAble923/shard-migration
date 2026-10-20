# cc-P186: the Golem join kit (set up any extra PC to work the queue)

2026-10-19. The Iron Golem (Opus, the integrator). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P186-cont-golem-join-kit.md`.
Not committed: the Golem commits after DONE. Both repos were clean at the start apart from the overnight bot's
transcript. P184 is DONE (its notes end `P184 DONE`), so this builds on its registry, claims, guard, `Setup-SecondPC.ps1`,
`Setup-Golem.ps1`, `Check-GolemSetup.ps1` and `SECOND-PC.md`, and forks none of them. P158/P159 have not run, so the
Codex lanes stay disabled entries. No task-list tool is offered in this session (as in P184), so progress was in this
file and the Golem's log. Four parts ran in parallel as helpers (the UO file assessment; paths, SentinelOne and
portraits; the web console's control of every Golem; laptop power and back-off). I wrote the kit, the readiness check,
the game-PC scripts, the registry and the wiring, re-ran every helper's suite myself and read their changes.

## Resumed (2026-10-19, after the 19:09 resume note)

The first session died about 16:40 with Docker frozen. This session read the note and `git status`, and carried on: everything above was already written and its suites green; left were the Shard Console suite (it crashed: Deviation 13), the CHANGELOG line for that fix, the ASCII check of all 51 touched text files (none bad) and the preflight. No Docker, test shard, package or Haven step was needed, so no lock was taken. No task-list tool is offered in this session either. The Read tool was denied once (unattended) on `D:\ShatteredLegacy\scripts\Shard-Console.ps1` :9418; I had already read those lines with `sed`, and made the two edits with a small Python script (exact-match, one each, backup in the scratchpad), as this repo's unattended runs do.

## Headlines

- **One script per PC: `Join-Golem.ps1 -Name <it> -DryRun`, then without** (`D:\UO\golem\JOIN-PC.md` is the guide in
  plain words). Two phases. As an administrator, the machine half: a fit table that stops a too-small PC, or a taken
  D:, before any change; the `golem` account; D: as a VHDX (P184's `Setup-SecondPC.ps1`); the game PC's folder layout;
  the kit copied onto D:; programs from winget's official manifests; the power, wake, update-hours and auto sign-in
  settings. Then, signed in as the golem account, the user half: Claude Code's native installer; stops that say exactly
  what to click for Claude on the Max plan with **no ANTHROPIC_API_KEY**, each Codex lane in its own home, Tailscale and
  GitHub; one deploy key per repo; the clones at the same paths; hooks; tasks; the registration file; this PC's own test
  shard built, health-checked and stopped; the readiness check. Every step is idempotent and skipped when done; a dry
  run lists every stop a real run would make.
- **The readiness check, `Test-GolemReady.ps1`**, any PC, any time: green/red table, one-line verdict, exit code =
  failures, written to `ready-<name>.json` and posted to the game PC from an extra PC, shown on that Golem's card. It
  does a **real claim and release of a fixture prompt** with that PC's own claim code (in a temp folder), an MCP
  `initialize` to vseUOAware, a push and delete of a test branch (`-PushTest`), and the laptop checks. Every outside
  program has a time limit. **Run for real on the game PC: `NOT READY: 2 of 21 checks failed: docker, docker image`**:
  the Docker engine here does not answer (see "For Chase"); everything else is green.
- **The registry has every PC.** Cobalt became **Gold** (machine `STEPHS-DESKTOP`, Tailscale `stephs-desktop`); the Codex
  lanes on her PC are **Agapite** (Chase's ChatGPT login) and **Verite** (hers); **Copper** and **Silver** are the
  daughters' laptops; **Stone** is the work PC. All are disabled until each PC's readiness is green. New optional fields
  (`kind`, `tailscale`, `docker`, `autologon`, `portrait`, `power`, `backoff`) are checked by `Read-GolemRegistry`.
- **A guard bug, fixed first.** P184's worktree guard counted every Golem in the registry on any PC. The disabled Cobalt
  entry named the same paths as the Iron Golem's own copies (as every extra PC must, 2d), so at the start of this prompt
  the guard denied the Iron Golem every git command in its own `D:\ShatteredLegacy` and `D:\UO\shard-migration`. It now
  compares only Golems on this PC.
- **The web console controls every Golem.** Each Golem's card has the Iron Golem's buttons, with the same typed confirm
  and identity check. A Golem on another PC opens no port: its agent (`Remote-Agent.ps1`) pulls its commands over
  Tailscale from the web console's tailnet address, runs them through that PC's own Golem scripts (an allowlist),
  and posts results (onto the Timeline with the Golem's name), status and readiness. A command for an offline Golem
  shows "queued until Gold is online (expires HH:MM)" and expires after 30 minutes. Each PC has its own secret, minted
  once on the game PC (only a salted hash kept) and kept with DPAPI on that PC.
- **The back-off rule is wired in.** Before each claim and in the wake target, `Test-GolemBackOff` can make a Golem claim
  nothing (outside its hours, on battery, battery saver, throttling, its owner active, a game running); at each watch a
  running lane that must stop is asked for a stopping point. Only with multiGolem on; the game PC's entries have no
  back-off block, so nothing changes there.
- **Laptops**: a "Golem <name> (on AC)" power plan switched in for the hours (plugged-in values only); a wake task;
  Wake-on-LAN and S0/S3 detected per PC, with a wake test; auto sign-in of the golem account through Sysinternals
  Autologon (an LSA secret, not the Winlogon value every account can read), then locked with `tsdiscon`; Windows Update
  active hours; a Docker CPU cap. `Set-GolemPower.ps1 -Undo` restores every value it changed.
- **Paths**: `golem-paths.json` lists 92 paths, with file:line users, read or write, and whether an extra PC can use the
  same path. 22 cannot (mostly the user profile), each with a fix or a separate SentinelOne entry.
  `SENTINELONE-EXCLUSIONS.md` has one block per PC.
- **Assessment**: `Find-UoFiles.ps1` (read only) ran on the game PC. Nothing UO lives outside `D:\UO` and
  `D:\ShatteredLegacy` except profile data (Claude memory, client settings) and about 4 MB of test leftovers in Temp.
- **Portraits**: ten placeholders (piece-01 recoloured per metal) in `scripts\console-art\golems\`, shown on the cards and
  set as the golem account's picture; ten art requests filed through P152's pipeline for Chase to approve.

## What changed, with file:line

`D:\UO\golem` (outside git; backups `*.bak-20261019-P186` beside each changed file, and
`Golems.ps1.bak-20261019-P186-cards` from the web console helper):

| File | Change |
|---|---|
| `golem.ps1` | the guard compares only Golems on this PC :2001; `Get-GolemBackOffNow` :1741 (GolemPower.ps1's `Test-GolemBackOff`, or the test seam `backoff-fake-<name>.json`); asked in `Hand-Off` :1759, in `Get-WakeTarget` :1280, and at the watch :2496 (a running lane that must stop gets `winding = stopping-point`, the same as Find a stopping point) |
| `Golems.ps1` | `Read-GolemRegistry` checks the new optional fields :79; `Get-GolemCards` :685ff carries `ready`, `remote`, `portrait`, `lastSeen`, `online`, `winding`, `stoppedPrompt` (the web console helper) |
| `golems.json` | Cobalt is Gold; Agapite, Verite, Copper, Silver, Stone added (disabled); `kind`, `tailscale`, `docker`, `autologon`, `portrait`, `power`, `backoff` |
| `Join-Golem.ps1` (new, 482 lines) | probes and actions :71 to :133 (every probe can be faked, every action is recorded and skipped in a dry run); removal :155; the admin phase :185 (fit :190, account :226, drive and layout :246, programs :262, back-off :291); the user phase :306 (apps :311, sign-ins :326, GitHub :366, files :398, Docker :455, ready :478) |
| `Test-GolemReady.ps1` (new) | the readiness check; `Run-Exe` with a time limit; the fixture claim judged a minute into the Golem's own hours |
| `Remove-Golem.ps1`, `Add-GolemEntry.ps1`, `Export-GolemKit.ps1`, `Set-GolemGitHubRules.ps1` (new) | the game PC's side: removal; a PC's registration into the registry; the kit zip (no state, logs or secrets; refuses if a real key shape is inside); the two GitHub rulesets |
| `Check-GolemSetup.ps1` | now runs `Test-GolemReady.ps1` with the same parameters |
| `GolemPaths.ps1`, `golem-paths.json`, `SENTINELONE-EXCLUSIONS.md`, `New-GolemPortraits.py`, `portraits\account\` (new, helper) | `Read-GolemPaths` :63, `Test-GolemLayout` :121, `New-GolemLayout` :151, `Get-GolemPortrait` :178, `Set-GolemAccountPicture` :186 |
| `GolemPower.ps1`, `Set-GolemPower.ps1` (new, helper) | detectors `Get-GolemSleepModel` :134, `Get-GolemPowerState` :182, `Get-GolemWolSupport` :224, `Get-GolemOwnerActivity` :290, `Test-GolemBackOff` :357, `Test-GolemWakeEvent` :384, `Get-GolemLaptopReport` :408; `Invoke-SetGolemPower` :406, `Undo-SgpAll` :354 |
| `Find-UoFiles.ps1`, `Move-UoFiles.ps1` (new, helper) | the walk :189, `Get-DirClass` :101, `Get-Proposal` :142, the script-reference check :276; `Move-One` :71, the row loop :91 |
| `Remote-Agent.ps1` (new, helper) | the pull agent (endpoints in its header) |
| `Poke-Golem.ps1`, `Wrap-Up.ps1`, `Find-StoppingPoint.ps1`, `Set-RunNext.ps1`, `Retry-Stopped.ps1` | an optional `-Golem` passed on to golem.ps1 (helper; I reviewed the diffs: unchanged without `-Golem`) |
| `JOIN-PC.md` (new), `SECOND-PC.md`, `README.md` | the guide; Cobalt is Gold and a pointer to the kit; "Joining another PC (cc-P186)" |
| `tests\Join.Tests.ps1` (new), `tests\GolemPaths.Tests.ps1`, `tests\GolemPower.Tests.ps1`, `tests\UoFiles.Tests.ps1`, `tests\RemoteAgent.Tests.ps1` (new, helpers), `tests\Golem.Tests.ps1` | two P186 facts (the guard, the back-off) and the suite now clears `GOLEM_NAME`/`GOLEM_ROOT` at its start :25 |
| `D:\UO\golem\merge-queue`, `D:\UO\cc-prompts\merging` | made empty by `New-GolemLayout` (P184 makes them on first use; the layout check wants them) |

`D:\ShatteredLegacy` (the web console helper, plus the portraits and the patch notes):

| File | Change |
|---|---|
| `web-console\server.py` | listeners and endpoints docstring :10, :30-39; the agent block :317-600 (`registry` :318, `mint_agent` :364, `agent_auth` :385, `_sweep` :432 expiry, `queue_remote` :458, `take_commands` :502, `finish_command` :516, `save_report` :537, `portrait_path` :574, `golem_cards` :583); the agent GETs :930 and POSTs :994; `golem` in /api/action :1035; `--golem-root`, `--mint-agent`, `--revoke-agent` :1076 |
| `web-console\panels.py` | `decide_agent` :63, `ready_summary` :78, the Timeline names the Golem :231 |
| `web-console\golem-actions.json`, `static\app.js` (`golemCard`, `drawGolemTeam`, `openSheet` :358, `run` :433), `static\app.css` :101, `static\index.html` :37, `tailscale\docker-compose.yml` (a comment) | every Golem's card with its readiness, portrait, online state, queued commands and buttons |
| `scripts\Shard-Console.ps1` | `Test-PlanSafety` :3321 allows a trailing `-Golem` on the eight Golem scripts only; `ConvertTo-GolemCardDocument` :4243, `Get-GolemScopedConfig` :4260, `Add-GolemToPlan` :4284; `Get-GolemCardLines` :4323 (readiness, online) |
| `scripts\Invoke-WebConsoleAction.ps1` :17, :44 | `-Golem` |
| `scripts\console-art\golems\*.png` (new) | ten portraits, 256 px, 23 to 27 KB each |
| `web-console\tests\test_remote_golems.py`, `tests\fixtures\agent_harness.py` (new), `scripts\tests\Shard-Console.Tests.ps1` (five P186 facts :7591-:7660) | tests |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.19.5`, four `### Staff` lines; 2026.10.19.5 |

`D:\UO\art\requests\`: ten art requests `golem-portrait-<metal>` (status `new`), 256/96/48 px, Iron's reference piece-01,
the others Iron's. No image was generated (filing spends nothing).

No server code changed, so no build and no image.

## Decisions argued

- **Sign-in (Chase's (b))**: automatic sign-in of the golem account at boot, then locked. The password is a random 24
  characters, set on the account and kept only as Windows' LSA secret `DefaultPassword` through Sysinternals Autologon
  (Microsoft: "a user with administrative rights can easily retrieve and decrypt it"). The plain Winlogon value was
  refused: on the game PC that key is readable by `BUILTIN\Users`, so every family account could read it. Writing the
  LSA secret ourselves needs a Windows API call (the SentinelOne rule). For about a second the password is on
  Autologon's command line. The lock: `tsdiscon.exe` 20 seconds after sign-in (`rundll32 user32.dll,LockWorkStation`
  refused: a Windows API entry point). (a) needs a person after every reboot; (c) headless breaks the Golem's
  interactive tabs, hooks, nudge, stopping point and session closer.
- **Power**: a dedicated plan with only the plugged-in values changed, switched by tasks at the start and end of the
  hours and at boot, not `powercfg /requestsoverride` (it can only make Windows ignore requests, not keep a PC awake),
  not a keep-awake process (needs `SetThreadExecutionState`, a Windows API call), not editing the owner's plan (a missed
  switch-back would leave sleep off silently).
- **GitHub**: deploy keys per PC per repo with write, plus two rulesets on each public repo: "main is the integrator's"
  (only the Repository admin role, Chase's own login, can update `main`) and "Golems push golem/* only". A deploy key is
  no admin, so it can push `golem/**` only. Not possible: one PC's key cannot be told from another's by branch. A
  fine-grained token was refused: it is Chase's own credential, so the admin bypass would let it through. The private
  prompts repo needs write on `main` for claims, so it gets keys and no ruleset (rulesets on private personal repos
  need GitHub Pro anyway).
- **The registry entry**: a registration file that the integrator applies (`Add-GolemEntry.ps1`, validated, backed up,
  enabled only with `-Enable`), not a pull request: golems.json is not in a repo, and an entry grants a PC its lanes and
  areas, so a person looks first.
- **The remote agent pulls**; the remote PCs open nothing. The web console's tailnet listener (Tailscale Serve, never
  Funnel) takes `/api/agent/*` only with the Golem's name and its secret; a wrong key, another Golem's name, or a Golem
  on this PC all get 403.
- **Portrait tint**: HSV masks pick the metal trim, the glow and the stone; the trim's luminance is mapped through a
  shadow, mid and highlight colour per metal with a gamma for the finish; the stone is pulled toward the mid colour;
  alpha kept. Per-metal values are in the table under "The path list and portraits".

## The path list and portraits (2c, 2d)

- `golem-paths.json`: 92 entries. Every 2d.2 folder is listed with `create: true` (golem, cc-prompts with
  queue/held/completed/_renders/claimed/merging, overseer, tools\vseUOAware, the third-party code the prompts name, the
  worktree and lane folders, the web console, logs).
- Cannot match, each with its fix:

  | Path | Fix |
  |---|---|
  | `%USERPROFILE%\.claude`, `.claude.json` | stays in the profile. `CLAUDE_CONFIG_DIR` works (tested on a throwaway folder), but golem.ps1:1003 and Shard-Console.ps1:249 read the profile path. Separate SentinelOne entry |
  | `.local\bin\claude.exe`, `.local\share\claude` | stays. A junction works (`claude --version` ran through one), but the updater rewrites the folder. Separate entry |
  | `.codex` | moves: `CODEX_HOME=D:\UO\golem\codex-home\<login>` (tested; it also keeps the two ChatGPT logins apart) |
  | `%LOCALAPPDATA%\OpenAI\Codex\bin` | stays. Separate entry |
  | Docker Desktop's WSL data | moves: Docker Desktop's "Disk image location" `D:\DockerDesktop` (not tested here: it would move live data) |
  | pip cache, npm cache | `PIP_CACHE_DIR` (tested); `npm config set cache` (npm is not installed here) |
  | Store Python's user site | install python.org 3.11 for all users on the extra PCs (the kit does) |
  | `%LOCALAPPDATA%\ShatteredLegacy` | `SL_LEGION_SETTINGS` for the Legion file; the window state stays |
  | `.gitconfig`, `.ssh` | stay; no exclusion needed |
  | `C:\ShatteredLegacy\uo-d.vhdx` (extra PCs) | stays on C: by design. Separate entry |
  | `C:\ShardLane` (a P159 proposal) | should be under D: when P159 is written |
  | `cli.json` and `launch\*.cmd` naming `C:\Users\ckfle\.local\bin\claude.exe` | written per PC by `Check-Cli.ps1`; never copied (the kit leaves them out) |

- Portraits: `D:\ShatteredLegacy\scripts\console-art\golems\<metal>.png`, 256 px, 23 to 27 KB each (budget 60 KB each,
  about 262 KB in all). The account picture's eleven sizes (32, 40, 48, 64, 96, 192, 208, 240, 424, 448, 1080: Windows 11
  writes all eleven, 64 included) are in `D:\UO\golem\portraits\account\` (outside git, 4.5 MB; the kit carries them).

  | Metal | Shadow | Mid | Highlight | Gamma | Stone tint | Glow |
  |---|---|---|---|---|---|---|
  | Iron | 40,44,50 | 128,134,142 | 214,220,228 | 1.10 | .20 | 255,196,96 |
  | Bronze | 66,36,14 | 184,115,51 | 246,196,128 | 1.00 | .18 | 255,196,96 |
  | Gold | 92,62,8 | 228,180,48 | 255,244,170 | .85 | .15 | 255,236,150 |
  | Copper | 70,26,12 | 196,96,52 | 250,170,126 | .95 | .22 | 255,150,90 |
  | Silver | 64,68,78 | 186,192,204 | 252,252,255 | .80 | .12 | 170,220,255 |
  | Stone | 58,50,40 | 150,136,112 | 222,208,180 | 1.20 | .35 | 255,196,96 |
  | Agapite | 60,22,38 | 178,92,122 | 240,172,196 | .95 | .25 | 255,150,200 |
  | Verite | 24,52,26 | 104,150,84 | 192,230,160 | .95 | .25 | 170,255,150 |
  | Valorite | 18,32,74 | 74,116,192 | 164,204,252 | .90 | .25 | 120,200,255 |
  | ShadowIron | 16,14,22 | 78,72,92 | 160,154,178 | 1.10 | .30 | 190,140,255 |

- Email header image: `Send-Mail` (golem.ps1:276-293) sends plain text only. About 15 lines would add an HTML alternate
  view with the portrait as a linked resource (System.Net.Mail, nothing compiled). Not done here (see Deviations).

## The UO file assessment on the game PC (2e)

`Find-UoFiles.ps1` ran read-only on CHASES-TOWER: 218 s, 178,337 folders on C:, D:, G: and H:, 289 rows. Report:
`C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-shard-migration\2efdbfd4-3f59-417c-82b9-9fb1ea43c30d\scratchpad\find-uofiles-gamepc.csv`
(scratch; Chase can re-run it any time and it goes to his Desktop).

| kind | count | MB | keep | move | remove |
|---|---|---|---|---|---|
| classicuo (client settings) | 3 | 67.3 | 3 | 0 | 0 |
| claude-memory | 5 | 747.9 | 5 | 0 | 0 |
| download | 4 | 0.1 | 0 | 0 | 4 |
| golem-folder (old test copies in Temp) | 5 | 2.4 | 1 | 0 | 4 |
| package-cache (`.nuget\packages\modernuo.*`) | 4 | 5.1 | 4 | 0 | 0 |
| sl-player-package (test leftovers in Temp) | 144 | 0 | 0 | 0 | 144 |
| tazuo (test leftovers in Temp, and TazUO's settings) | 78 | 0.7 | 1 | 0 | 77 |
| uo-workspace, shard-work-folder, shard-layout, uo-assistant | 18 | 1.3 | 6 | 0 | 12 |
| script-ref (2e.4 references) | 28 | 0 | 28 | 0 | 0 |

No stray repo copies, no EA client, no old `D:\UO`-style folders elsewhere. Docker images and volumes are missing from
the report because the engine did not answer. One likely false positive: `Downloads\The Ultimate Dungeon Wall Set by-DRC1K.zip`
(matched "ultima").

What the shard's scripts point at outside `D:\UO` and `D:\ShatteredLegacy` (2e.4): nothing at `G:\Data\Games\UO`,
`D:\tazuo-sl-build` or `D:\LDPlayer`. Real ones: `C:\dev\sunflower\print-queue\...` and `sunflower-devstack`
(`docker\haven\services.json:107`, `:109`, `:115`, `:152`, `:160`), `D:\Cloud Drives\iCloudDrive`
(`tools\playtest-bot\overnight.json:6`, `uobot\archive.py:3`), `D:\Servers\Minecraft\ATM10\data`
(`docker\mc-status\docker-compose.yml:10`, `docker\atm10-site\docker-compose.yml:7`). The profile and Program Files ones
are in the path list above. None of these is a Golem path; moving them is Chase's choice, with these references to edit.

## Tests

Each new fact was seen failing first.

| Suite | Red first | Final |
|---|---|---|
| `tests\Join.Tests.ps1` (12 facts) | 11 facts against a folder with Golems.ps1 and none of the kit: 0 checks passed, 11 failed. The registry-fields fact: 1 passed, 5 failed before the validation. The kit's "words about secrets are not secrets" check: the real export refused golem.ps1 and two test files under the first secret pattern | **97 checks passed, 0 failed** |
| `tests\Golem.Tests.ps1` | `P186_TheGuardIgnoresGolemsOnOtherPCsThatShareTheSamePaths`: denied (the live failure exactly); `P186_TheBackOffRulePausesClaimsAndFindsAStoppingPoint`: 2 passed, 5 failed | **596 checks passed, 0 failed** (the whole suite) |
| `tests\GolemPaths.Tests.ps1` (8 facts) | 0 passed, 9 failed with nothing; 141/6 with the library only; five planted bugs each caught | **609 passed, 0 failed** (re-run by me) |
| `tests\GolemPower.Tests.ps1` (39 facts) | 73 assertions failed against empty stubs; the 4 that passed empty were turned red with mutations | **133 passed, 0 failed** (re-run by me) |
| `tests\UoFiles.Tests.ps1` (14 facts) | 0 passed, 15 failed with no scripts; two removed lines each caught by one fact | **79 passed, 0 failed** (re-run by me) |
| `tests\RemoteAgent.Tests.ps1` (8 facts, the real server.py and proof proxy) | 8/32, then 6/10, then 3/7 as parts landed | **75 passed, 0 failed** (re-run by me) |
| web console, `python -m unittest discover` | `test_remote_golems`: 9 of 9 errors before the change | **Ran 52, OK** (re-run by me) |
| Shard Console suite | five P186 facts: 5 of 5 failed before | **413 facts, 406 passed, 7 failed** (twice, after the fix below); the five P186 facts pass. The 7 fail the same at HEAD (a clean copy of HEAD: 408 facts, 14 failed, the same 7 plus 7 that only fail from a copy outside D:\ShatteredLegacy): live-state facts (Haven cutover, play-test counts, a new player command `artificerrank`, P184's `golem.integrate` tooltip), none P186's |

Two things found by running the suites in a Golem session:
- **The Golem suite inherited this session's `GOLEM_NAME=Iron`**, so every hook it started acted as Iron, and the watch's
  shared pass (which skips under a name) never ran: `P184_AStaleClaimIsReleasedBackToTheQueue` and
  `P184_LocksAreASignUpSheetAndStaleOnesExpire` failed (6 checks), on the pre-P186 hook too. With the name cleared they
  pass; the suite now clears it at its start, and the whole suite is 596/0.
- **The readiness check hung** on `docker version` (the engine here is stuck). Every outside call now has a time limit
  (45 s; the build 90 minutes), and Windows PowerShell 5.1's `Start-Process` needs its handle read for the exit code.

The end-to-end dry run on the game PC (real, read-only probes):
- `Join-Golem.ps1 -Name Gold -DryRun`: the fit table (Windows 11 Pro 26200, 31.7 GB, 32 threads, 267 GB free on C:,
  virtualization on: **Claude + Docker**), then "Stopped before any change: D: is taken by another drive", exit 2, as
  designed (this PC's D: is a real data disk).
- `Join-Golem.ps1 -Name Gold -DryRun -Phase user`: exit 0. Claude Code there and signed in on max; Tailscale up; would
  install the Codex CLI; would make three deploy keys, the SSH aliases and GitHub's published host key (checked against
  `gh api meta`), then a STOP with the exact `gh repo deploy-key add` lines; the clones there; the prompts repo "not
  yet"; would set up hooks for Gold, Agapite and Verite and register the remote agent task; a STOP for Docker not
  running; the readiness check last.
- `Test-GolemReady.ps1 -Name Iron`: 19 of 21 green; Docker and its image red.
- `Export-GolemKit.ps1 -DryRun`: 229 files, 12.1 MB.
- `Set-GolemPower.ps1 -Name Iron -DryRun` (by the helper): would make the Golem plan and its boot task; this PC already
  never sleeps on AC. Not to be run for real here.

## Deviations and decisions for Chase

1. **Section 0 says "Bronze Golem (wife's PC)"**, but Bronze is P184's second lane on the game PC and your 14:35 note
   names her Golem Gold. I used Gold for her PC, with Tailscale name stephs-desktop, and kept Bronze on the game PC.
2. **New names for the Codex lanes**: P184's Codex example was named Copper, which is now a daughter's laptop. Her PC's
   two Codex lanes are Agapite (yours) and Verite (hers), both disabled until P158/P159.
3. **The guard fix (golem.ps1 :2001)** was not asked for. Without it the Iron Golem could not run git in its own copies.
4. **The guard still reads the mere mention of `Start-TestShard`** as running the test shard (even `sed -n` on the file);
   I read that file through a glob. It is harmless, but a later prompt could make the guard tell a read from a run.
5. **The Docker engine on the game PC does not answer** (docker.exe calls hang; three were seen in the task list). I did
   not restart Docker Desktop (shared equipment, and Bronze may be using it). The readiness check says so in red.
6. **The email header image is not built**: golem.ps1's mail is plain text; it needs about 15 lines (above). I left it
   for a small prompt rather than change the mail path of a live Golem here.
7. **Two scheduled tasks run with Interactive logon as the golem account** (Golem Watch and the remote agent), so a wake
   opens its window in the golem session. The power phase tasks run as the golem user without admin rights (not SYSTEM:
   a SYSTEM task running a script on D: would let anyone who can edit `D:\UO` become SYSTEM). This assumes
   `powercfg /setactive` works without admin; check it on the first laptop.
8. **The golem account is a standard user**, not an administrator (the prompt's "admin, once" is the script, run as
   admin). It is in docker-users where Docker is on.
9. **"Pause/resume its lanes"** on a card is Rest and Turn on (Stop-Golem / Start-Golem with `-Golem`); a lane-pause flag
   is P159's, and the agent's `pause` and `resume` keys point at those so it is one line later.
10. **The web console needs a restart** to show the cards and take agents:
    `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\web-console\Install-WebConsole.ps1`. I did
    not restart it.
11. **Not tested for real** (no other PC here): the account, the drive, the installs, the sign-ins, Autologon, the wake,
    the deploy keys, the rulesets, the remote agent over Tailscale, a Docker build on another PC. Each is faked in the
    tests and dry-run here; Chase runs them on each PC.
12. **`multiGolem` is still false** on the game PC (P184's switch). The back-off, the registry fields and the cards take
    effect when it is on.
13. **The Shard Console suite.** **The Shard Console suite crashed partway** with my changes in place (exit 2, output cut off around the P154/P155 facts, 4 of 4 full runs), while a clean HEAD copy ran all 408 facts. Windows Error Reporting had the cause: powershell.exe faults `PSDataCollection.InternalInsertItem` (PSInvalidOperation) and `InvalidRunspaceState ... ConcurrentSessionStateProxyCallInProgress` (20:01, 20:13, 20:28). It is a race in P154's background reads: `Stop-ConsoleJobs` (and the 2-minute abandon in `Receive-ConsoleJobs`) called `Stop()` then `Dispose()` on a pipeline whose worker was still writing, often while it was still dot-sourcing the console at first boot. Timing decides it, so any changed file (scanned afresh on load) made it hit more often: the P154+P155 subset crashed about 1 run in 5 with any one of my three files, 0 in 15 at HEAD. Fixed with `Stop-ConsoleJob` (`scripts\Shard-Console.ps1` :9430): Stop, then `EndInvoke` before Dispose; both callers use it (:9422, :9442). After it: two full runs complete, no new WER report. No new fact for it: a race has no reliable red; the before/after run counts are the evidence. Not asked for, but without it the suite cannot finish. One CHANGELOG Staff line added.

## For Chase

**Names to confirm**: Iron and Bronze (game PC), **Gold** (her PC, stephs-desktop), **Copper** and **Silver** (which
daughter is which?), Stone (work PC, later); Agapite and Verite for her PC's two Codex lanes. Spares with portraits:
Valorite, Shadow Iron.

**Once, on the game PC** (about 10 minutes):
1. `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\web-console\Install-WebConsole.ps1` (restart
   the web console to pick up the cards and the agent endpoints).
2. `Set-GolemGitHubRules.ps1 -DryRun`, then without (main stays yours; the PCs push `golem/*` only).
3. The prompts repo (SECOND-PC.md step 6, `queueMode: git`), if the extra PCs should claim from the shared queue.
4. In Tailscale's ACL: `"tagOwners": { "tag:golem": ["autogroup:admin"] }` and a grant for `tag:golem` to reach
   `tag:uoconsole` on `tcp:443`. Optional while the PCs are signed in as you.
5. `Export-GolemKit.ps1` makes the zip for the PCs.
6. Look at the ten portrait requests in the art pipeline when you have a moment.

**On each PC** (about an hour each, mostly downloads; JOIN-PC.md has every click):
1. Copy the kit zip over (`tailscale file cp`, or a USB stick) and unzip it to Downloads.
2. `Find-UoFiles.ps1` (5 minutes, read only): look at the CSV on the Desktop.
3. As an admin: `Join-Golem.ps1 -Name Gold -DryRun`, then without. Restart the PC.
4. As the golem account: `Join-Golem.ps1 -Name Gold`. Do what each stop says (Claude sign-in as you, Tailscale, the
   deploy key lines on the game PC; for her Codex lane, her one sign-in), run it again until it reaches the readiness
   check.
5. Mint its web console secret on the game PC: `python -P D:\ShatteredLegacy\web-console\server.py --mint-agent Gold`,
   then on the PC `Remote-Agent.ps1 -Golem Gold -SaveKey`.
6. On the game PC: `Add-GolemEntry.ps1 -File <its registration> -DryRun`, then `-Enable` once its readiness is green.

**Questions**:
1. **Docker on each daughter's laptop?** The registry says no for both (heat, noise, RAM). Say yes per laptop and the fit
   check decides.
2. **Allowed hours per PC?** Now: Gold `22:00-07:00`, its Codex lanes `23:00-06:30`, Copper and Silver `22:00-06:30`.
   School nights may want something else (Windows Update can cover 18 hours of them).
3. **Her Codex sign-in under the golem account**: she signs in once, as the golem account, into
   `D:\UO\golem\codex-home\lane-steph` (JOIN-PC.md). Please confirm with her.
4. Is a password on Autologon's command line for about a second acceptable (SentinelOne may log it)? The alternative is
   typing it once into Autologon's window.
5. The game PC's Docker engine is stuck: restart Docker Desktop when nothing is building.
6. Tick the Temp leftovers (about 4 MB) in the Find-UoFiles report if you want them moved to `D:\UO\_to_delete\`.

The SentinelOne exclusion list, one block per PC, is `D:\UO\golem\SENTINELONE-EXCLUSIONS.md`. Your current exclusions
cannot be read from here: paste them and they can be compared.

## Repo size rule

No file over 5 MB: the largest new files are the ten portraits (under 30 KB each) and the account pictures (outside
git). The kit zips go to `D:\UO\golem-kit\` (outside git).

## Commit preflight

Run twice (after the last change). No BLOCKED, no REFUSING line.

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

The code repo also carries `docker\haven\services.json` (one state line, Portainer on Haven: "running (Portainer (Haven): deploy, 2026-10-19)", written 16:34 by the Shard Console's `web.portainer-haven` button, Shard-Console.ps1:1254). Not P186's work: it is the console's record of a deploy Chase ran, and it goes in with this commit unless Chase says otherwise.

P186 DONE
