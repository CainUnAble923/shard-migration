# cc-P184: multi-Golem (several Golems working the queue at once, like a dev team)

2026-10-19. Fable. Prompt: `D:\UO\cc-prompts\cc-P184-cont-multi-golem.md` (handed by the Golem at 11:29).
Not committed: the Golem commits after DONE. Both repos were clean at the start apart from the overnight bot's transcript.
No task-list tool exists in this session (TaskCreate and TodoWrite are not offered), so progress was in this file and the
Golem's log, not a task list.

## Headlines

- **It all ships behind `multiGolem: false`** in `D:\UO\golem\settings.json`. Off, the one Golem behaves exactly as
  today: the whole existing suite (480 checks) is green on the new hook, and one new fact pins the off switch
  (today's files, today's folders, `status.json` says `multiGolem false`).
- **A registry, `D:\UO\golem\golems.json`:** one entry per Golem (name, machine, engine `claude` or `codex`, lane
  `Opus`, `Fable` or `any`, the ChatGPT account for a Codex lane, the Touches areas it may take, its two work copies,
  enabled, integrator, hours). Shipped: the **Iron Golem** (the integrator, Opus lane, the real folders) and the
  **Bronze Golem** (Fable lane, worktrees under `D:\UO\golems\Bronze\`), both on this PC; a `Cobalt` Claude Golem for
  the wife's PC and a `Copper` Codex lane as disabled examples. `Read-GolemRegistry` validates every field and throws
  with every problem in one message; the hook then refuses the phrase with that message, emails once a day, and the
  consoles show it.
- **One work copy and branch per Golem.** The integrator stays in `D:\ShatteredLegacy` and `D:\UO\shard-migration` on
  main, so nothing Chase uses moves. Every other Golem gets git worktrees of both repos (`Setup-Golem.ps1 -Name
  Bronze`) and is put on `golem/<name>/P<nn>` from fresh main at each claim; a dirty copy refuses the claim and emails.
  The session learns who it is from `GOLEM_NAME` (and `GOLEM_ROOT`), set by the launcher; the hand-off tells it its
  real copies, its branch and the lock rule; a sync PreToolUse **worktree guard** denies writes to any other Golem's
  copy and shared equipment without its lock.
- **Claims are tokens plus renames.** `claimed\.tokens\<file>.token` is made with `CreateNew` (exactly one maker), then
  the prompt is renamed into `claimed\<name>\` with a claim record (Golem, session, time, branch, areas). This matters:
  **two concurrent `[IO.File]::Move` calls on one file both returned without an exception in 4 of 12 runs on this PC**
  (`race.ps1`), so a bare rename is not a safe claim here. Lanes, the `**Golem:**` line, the Golem's allowed areas,
  **Touches** overlap (guessed from the text when the line is missing, logged), the `golem`/`console` exclusivity and
  "never while another Golem is mid-commit" all decide what a Golem may take; what it skips is said in its log. A claim
  with no live session for `claimStaleMinutes` (90) goes back to the queue, logged and emailed.
- **Locks are a sign-up sheet** (`locks\<resource>.json`: owner, session, since, TTL, why): `test-shard`,
  `docker-build`, `package`, `haven`, `commit`. `Use-GolemLock.ps1 -Take test-shard -Minutes 60 -Wait` for sessions;
  the hook takes `commit` around every commit and merge and `docker-build` around a merge build; stale ones expire and
  the watch emails.
- **The integrator merges**, one ticket at a time, between its own prompts and at the watch: `git merge --no-ff
  --no-commit` in each repo, the build when `server\` or `docker\uo\` changed, `Commit-ShardWork.ps1 -Merge` with
  every check it has, a push, the prompt to `completed\`. A conflict, a red build or a refused commit undoes it all,
  keeps the branch, and writes `cc-P<next>-cont-fixup-<orig>.md` into the queue for the Golem that made the branch.
  PAUSED is merged like DONE; STOPPED is not. The console's **Merge branches now** runs a round by hand.
- **Seeing them:** the Golem tab and the web console show one card per Golem (name, lane, engine, machine, state, the
  prompt and branch, the locks it holds, where its usage figure comes from). Emails say `[Bronze Golem]`.
- **The rollout test** (two real Claude Code sessions, Iron on Opus and Bronze on Fable, on throwaway clones of both
  repos with a local bare origin, two docs-only fixture prompts) is written up below under "The two-Golem test on this
  PC", with the claims, the branch, the lock wait and the merge from the logs.
- **A mistake of mine reached GitHub.** The first run of that test used a hook whose `-Root` defaulted to
  `$PSScriptRoot`; with `[CmdletBinding()]` that is empty while parameter defaults are evaluated (checked), so the
  throwaway sessions' hooks ran with no root, fell into the single-Golem path, and the Iron session's DONE ran the real
  `Commit-ShardWork.ps1` on the real repos: commits `453735e` (code) and `6b13743` (docs), titled "CC task P901: team
  test A ...", pushed. They hold only this prompt's in-progress console and web console work plus machine output (the
  script's safety checks ran); nothing secret or unwanted left the machine, but the title is wrong. I did not rewrite
  public history (the repo rule). The root now resolves in the body, not the default; details under Deviations.
- **`multiGolem` is off at the end.** Turning it on is one line, under "For Chase".

## What changed, with file:line

`D:\UO\golem` (outside git; backups `golem.ps1.bak-20261019-P184`, `tests\Golem.Tests.ps1.bak-20261019-P184`,
`README.md.bak-20261019-P184`, `settings.json.bak-20261019-P184`, `Add-GolemHooks.ps1.bak-20261019-P184`;
`D:\UO\Commit-ShardWork.ps1.bak-20261019-P184`):

| File | Change |
|---|---|
| `Golems.ps1` (new, 700 lines, dot-sourced by golem.ps1) | the registry `Read-GolemRegistry` :50, `Resolve-GolemSelf` :89 (-Golem, GOLEM_NAME, cwd, else the integrator), `Get-GolemFileName` :105 (the integrator keeps today's names), `Test-GolemHours` :110; Touches `Get-PromptTouches` :122 (the line, else a guess from paths and keywords), `Test-AreasOverlap` :161 (`docs-only` never overlaps), `Test-ExclusiveArea` :167, `Test-LaneFits` :184; claims `Get-ClaimCandidate` :217, `Invoke-Claim` :246 (token, rename, record, git mode), `New-ClaimToken` :275, `Release-StaleClaims` :315; locks `Enter-GolemLock` :376 (CreateNew, stale expiry, renew), `Exit-GolemLock` :413, `Clear-StaleLocks` :421, `Get-HeldLocks` :434; worktrees `Initialize-GolemWorktree` :455, `Reset-GolemBranch` :467; the integrator `Write-MergeTicket` :484, `Sync-RemoteTickets` :502 (a pushed branch's `Golem-Ticket:` trailer), `Get-NextPromptNumber` :528, `New-FixupPrompt` :539, `Invoke-Integrate` :584; `Get-GolemCards` :684 |
| `golem.ps1` | the multi setup after the paths :206 (`Set-GolemPaths` :223: per-Golem files, the first-run migration of `state.json`, `progress.json`, `sessions.json` into the integrator's with backups); new events `Guard`, `Lock`, `Integrate` and params `-Golem`, `-BuildScript`, `-Resource`, `-Minutes`, `-Release`, `-Wait`, `-WaitMinutes`; `-Root` resolved in the body (see Deviations); `Get-SessionName` :755 ("Golem Bronze P902"), GOLEM_NAME and GOLEM_ROOT in `Start-CliSession` and the launcher .cmd; `Get-WakeTarget` :1266 honours the lane and the areas; `Write-Status` :1596 (`multiGolem`, `golemName`, `integrator`, `branch`, `golems` cards, `registryError`; `status.json` stays the integrator's view plus the cards); `Wait-GolemLock` :1625; `Invoke-IntegratorRound` :1636; `Hand-Off` :1731 (the candidate), :1880 (the claim, the branch, a refused claim given back); `Get-MultiHandOffText` :1944; `Get-GuardDecision` :1966; `Lock` :2383, `Integrate` :2402; the watch's shared pass and one pass per local Golem :2425; the guard :2558; the invalid registry refuses the phrase :2659 and the Stop :2844; the commit on a branch with the ticket, the integrator's round after its own DONE, the ticket and `merging\` for the others :2913 to :2990 |
| `golems.json` (new) | the registry: Iron, Bronze, and the disabled Cobalt and Copper examples |
| `settings.json` | `multiGolem` false, `claimStaleMinutes` 90, `lockTtlMinutes` 120, `queueMode` folder, `integrateOnWatch` true |
| `Setup-Golem.ps1` (new) | a Golem's worktrees (or clones on another PC), its hooks (the integrator's file copied, then `Add-GolemHooks.ps1` in process), `claimed\<name>` |
| `Use-GolemLock.ps1`, `Integrate.ps1` (new) | the sign-up sheet for sessions and scripts; the console's Merge branches now |
| `golem-guard.cmd` (new), `Add-GolemHooks.ps1` | the worktree guard: PreToolUse (Edit, Write, MultiEdit, NotebookEdit, Bash, PowerShell), sync, 30 ms unless `GOLEM_NAME` is set; added to both real repos' `.claude\settings.local.json` (backups in `cutover-backup\`) |
| `Start-Golem.ps1`, `Stop-Golem.ps1`, `Wake-Golem.ps1` | `-Golem <name>` |
| `Setup-SecondPC.ps1`, `Check-GolemSetup.ps1`, `SECOND-PC.md` (new) | section 9: the `D:` drive from a VHDX (diskpart, a startup task), the one-command check (drive, git, claude, sign-in, registry, copies, hooks, Docker, a test push), the guide |
| `README.md` | "Several Golems at once (cc-P184)" and the Files table |
| `tests\Golem.Tests.ps1` | fourteen `P184_*` facts :1723 to :2060, with a team world (temp repos, a bare origin, Bronze worktrees, a CLI stub that records GOLEM_NAME, a build stub) |
| `D:\UO\Commit-ShardWork.ps1` | `-CodeRepo`, `-DocsRepo`, `-Branch` (every repo on it, never main, `push -u`), `-Merge` (on main, completes the merge), `-NoRefresh` (forced for any copy but the real pair; the scripts repo only with the real pair), `-NoArchive`, `-Ticket` and `-TicketFile` (a `Golem-Ticket:` trailer through `git commit -F`); every check it had applies to all of them (:18, :61, :187, :237) |

`D:\ShatteredLegacy`:

| File | Change |
|---|---|
| `scripts\Shard-Console.ps1` | `ConvertFrom-AutopilotStatus` reads `MultiGolem`, `GolemName`, `Golems`, `RegistryError` :4234; `Get-GolemCardLines` :4241 (pure: one row per card, the registry error, nothing while off); the Golem tab's panel :5032; the status document's `golem.multiGolem` and `golem.golems` :9111; the button `golem.integrate` (config :246, the row :1230, the phrase `merge branches`, the subject :951, the plan :5312, the allowed and present lists) |
| `scripts\tests\Shard-Console.Tests.ps1` | three `P184_*` facts :7515 to :7570; `P182_TheGolemTabHasPokeRunNextAndRetry` updated on purpose (the queue row now has four buttons) |
| `scripts\Publish-GamePcSnapshot.ps1` | reads the integrator's `state-<name>.json` when `multiGolem` is on :55 |
| `web-console\panels.py` | `status_problems` checks `golem.golems` when present :292 |
| `web-console\static\app.js`, `index.html` | a Golems card (`golemCard`, `drawGolemTeam`), hidden while off :172 |
| `web-console\golem-actions.json` | the `integrate` button (word `merge branches`) |
| `web-console\tests\test_web_console.py` | `test_golem_cards_are_optional_and_checked` :171 |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.19.4`, four `### Staff` lines; 2026.10.19.4 |

No server code changed, so no build and no image.

### Hard-coded paths (section 2), and how a session in a worktree is kept safe

Named `D:\ShatteredLegacy` or `D:\UO\shard-migration` in the Golem's own files (P126 counted 374 files over the whole
tree; these are the ones that run): `golem.ps1` (`-PromptDir`, `-Repo`, `-CleanRepos` defaults, the cwd filter
`^d:[\\/](UO|ShatteredLegacy)` on Prompt, Activity and Stop), `Start-Golem.ps1` (the queue), `Add-GolemHooks.ps1` and
`Move-ToGolem.ps1` (the two hook files), `Commit-ShardWork.ps1` (the two repos, `opsmirror.py --root`, `progress.py`),
`Publish-GamePcSnapshot.ps1` (`state.json`), `unattended-permission.ps1` (the cwd filter), the Shard Console's config
(`D:\UO\golem`, the queue), and every prompt. What was done: the worktrees live under `D:\UO\golems\`, so every cwd
filter already accepts them; the registry carries each Golem's copies, and the hook uses them for `-Repo`,
`-CleanRepos`, the commit (`-CodeRepo`, `-DocsRepo`) and the hand-off text (which tells the session to read
`D:\ShatteredLegacy` as its own copy, never to touch the real folders or another Golem's, and never to commit or switch
branches); `Commit-ShardWork.ps1` runs the mirror, the dashboard and the scripts repo only for the real pair; the
guard denies Edit, Write and shell writes outside the Golem's own copies and shared equipment without its lock; and
the launcher sets `GOLEM_NAME` and `GOLEM_ROOT` for whatever else reads them. Prompts keep saying `D:\ShatteredLegacy`.

Docker tags: `build.sh -t sl-modernuo:cc-P<nn>` already builds `sl-uo-builder:cc-P<nn>`, so two Golems' builds never
overwrite each other's images; the one thing that does collide is the test shard container (`sl-modernuo-test`, one per
PC), which is why `test-shard` is a lock and a second PC runs its own.

## Tests

Each new fact was run against the pre-P184 hook (`golem.ps1.bak-20261019-P184`) first: **all 14 `P184_*` facts FAIL
there (18 checks passed, 62 failed)**, then pass on the new hook. The three console facts were run with the committed
`Shard-Console.ps1` swapped in (`git stash`): **3 facts, 0 passed, 3 failed**, then 4 of 4 on the new one (with the
updated P182 row fact). The web console's new test fails on the old `panels.py` by construction (no `golems` check).

| Fact | Red on the old code because |
|---|---|
| `P184_WithMultiGolemOffNothingChanges` | `status.json` had no `multiGolem` field (the rest of the proof is the old suite, 480 checks green on the new hook) |
| `P184_TheRegistryIsValidatedAndRefusesLoudly` | no registry, no refusal, no email |
| `P184_ARaceForOnePromptGivesItToExactlyOneGolem` (two hook processes at once, six runs green) | both handed the same prompt (and, with a bare rename, still did: see Deviations 2) |
| `P184_LanesAreHonored` | Iron (Opus) took the Fable prompt; no branch |
| `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` | the server prompt started beside Bronze's; no guess logged; client-package not refused |
| `P184_GolemAndConsoleAreExclusiveAndWaitForACommit` | the golem prompt started beside the console one and beside a held commit lock |
| `P184_AStaleClaimIsReleasedBackToTheQueue` | no claims, no release, no email |
| `P184_LocksAreASignUpSheetAndStaleOnesExpire` | no `-Event Lock`; nothing expired; no wait |
| `P184_TheWorktreeGuardDeniesOtherDesksAndUnlockedEquipment` | no `-Event Guard` |
| `P184_TheHandOffNamesTheWorkCopiesTheBranchAndTheLocksAndTheSessionCarriesGOLEM_NAME` | the hand-off named nothing; the CLI saw no GOLEM_NAME and the name "Golem P101" |
| `P184_TheIntegratorMergesTwoBranchesInOrderAndAConflictBecomesAFixUpPrompt` (the real `Commit-ShardWork.ps1` on temp repos: `-Branch` commits pushed to a bare origin, two `-Merge` commits on main, the build stub for the server change only, the conflict's fix-up prompt with its Model, Golem and branch, main untouched, no half merge) | no branch commit, no ticket, nothing merged, no fix-up |
| `P184_ARedBuildBecomesAFixUpAndTheIntegratorMergesAfterItsOwnDone` | no round after the integrator's DONE |
| `P184_TheFirstMultiRunMigratesTheStateWithABackupAndStatusCarriesACardPerGolem` | `state.json` not migrated; no cards; no per-Golem status files |
| `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly` (the library alone: the Touches rules, the lane rule; two clones of a bare prompts repo, the second claim's push rejected and undone) | the library did not exist |
| console `P184_TheStatusCarriesOneCardPerGolemAndTheTabListsThemWithTheirMachine` | no `Golems`, no card lines |
| console `P184_TheStatusDocumentCarriesTheGolemCardsForTheWebConsole` | no `golem.golems` |
| console `P184_MergeBranchesNowIsAGolemButtonWithItsOwnPhraseAndScript` | no `golem.integrate` |
| web `test_golem_cards_are_optional_and_checked` | a bad card was not named |

Full suites, on exactly the files that are live:

- **The Golem:** `tests\Golem.Tests.ps1` on the final hook: **587 checks, 0 failed** (480 old, 107 new; the suite was
  run three times today as the hook changed, 586, 586 and 587 green). `Codex.Tests.ps1` 39 passed.
  `Move-ToGolem.Tests.ps1` as before (it needs the scheduled task and reports its usual export error here).
- **Console facts** `SL_FACT_FILTER='^(P184_|P182_|P183_|P125_|P131_|P160_|P161_|P162_)'`: 33 facts, 31 passed, 2 failed
  in that run; both re-run alone pass (`P182_WindowStepsRunInThisProcessForTheWebConsole` is order-sensitive in a
  combined run, P182's notes say the same; the row fact needed the update above). The full console run is not repeated:
  it dies silently partway at HEAD too (P182's and P183's notes).
- **Web console:** `python -m unittest discover -s web-console/tests`: 42 tests OK.

### The two-Golem test on this PC (section 8.2)

Setup (`scaffold.ps1`, in the session scratchpad; the world under `D:\UO\golems-p184-test`, deleted afterwards):
bare clones of both real repos as `origin-code.git` and `origin-docs.git`; the integrator's copies cloned from them;
a copy of the Golem folder as the root (`multiGolem` true, `autoWake` false, `-NoMail` so every email is a log line,
`-Cli` naming the real `claude.exe`); the registry with Iron (Opus, the integrator) and Bronze (Fable, worktrees made by
`Setup-Golem.ps1`); hooks in every copy pointing at that root; `ENABLED` and `ENABLED-Bronze`; two fixture prompts,
`cc-P901-team-test-a.md` (**Model:** Opus, **Touches:** docs-only: a note, take the `test-shard` lock for 3 minutes,
hold it 90 s, release) and `cc-P902-team-test-b.md` (**Model:** Fable, docs-only: a note, take the same lock with
`-Wait`, release). Then `golem.ps1 -Event SelfWake -Manual -Golem Iron -Model Opus` and the same for Bronze on Fable:
two real Claude Code sessions, named "Golem Iron P901" and "Golem Bronze P902", opened as windows of their own
(`-Cli` disables the Windows Terminal tab path, as it does in the tests).

Three runs. Run 1 (13:04) is Deviations 1: no root, no claims, the stray commits. Run 2 (13:11): Bronze claimed P902
at once but the claim was given back (its worktree showed `.claude/settings.local.json` as untracked: Deviations 15),
and the Iron window died before its first hook. Run 3 (13:30), with the exclude, the tab launch and the refused-claim
text, is the one that counts. From the two logs (`golem.log` is the integrator's, `golem-Bronze.log` Bronze's; the
emails are `would email` lines because of `-NoMail`):

```
13:30:10 SelfWake  recorded session Golem Iron P901 for P901 (console): wt, process 56752
13:30:11 SelfWake  claim: P901 wants Opus, not this lane (Fable): skipped                    (Bronze)
13:30:12 SelfWake  recorded session Golem Bronze P902 for P902 (console): wt, process 64984
13:30:19 Prompt    claimed P901 (cc-P901-team-test-a.md) for Iron: areas docs-only, branch main
13:30:21 Prompt    claimed P902 (cc-P902-team-test-b.md) for Bronze: areas docs-only, branch golem/Bronze/P902
13:30:21 Prompt    work copy ...\golems\Bronze\ShatteredLegacy: on golem/Bronze/P902 from main
13:30:22 Prompt    work copy ...\golems\Bronze\shard-migration: on golem/Bronze/P902 from main
13:30:31 Stop      P901 STOPPED, no commit            (the Iron session: Read of the prompt file denied, Deviations 15)
13:30:57 Lock      lock test-shard taken by Bronze for 2 min
13:31:13 Lock      lock test-shard released by Bronze
13:31:22 Stop      P902 DONE, committing: CC task P902: team test B ...
13:31:24 Stop      P902 is on golem/Bronze/P902, pushed; a merge ticket waits for the integrator (Iron)
13:31:24 Stop      would email: [Bronze Golem] P902 done on golem/Bronze/P902, waiting for the Iron Golem to merge
13:31:24 Stop      hand-off: nothing in the queue is for Bronze right now (lane Fable; 1 queued)
13:31:23 RetryStopped  retry: P901 (cc-P901-team-test-a.md) back in the queue, picked to go next
13:31:25 SelfWake  self-wake for P901 (console) refused: a session for P901 was opened 75 s ago (one per prompt per 2 minutes)
13:31:55 Lock      lock test-shard taken by Bronze for 2 min        (by hand, to make the Iron session wait)
13:32:53 SelfWake  recorded session Golem Iron P901 for P901 (console): wt, process 75104
13:33:02 Prompt    claimed P901 (cc-P901-team-test-a.md) for Iron: areas docs-only, branch main
13:33:16 Lock      lock test-shard held by Bronze: Iron waits (up to 30 min)
13:33:30 Lock      lock test-shard released by Bronze
13:33:36 Lock      lock test-shard taken by Iron for 3 min
13:33:56 Stop      P901 DONE, committing: CC task P901: team test A ...
13:33:59 Stop      integrator: merging 1 ticket(s) after P901
13:33:59 Stop      integrator: golem/Bronze/P902 has no changes against main in ...\ShatteredLegacy
13:34:01 Stop      integrator: merged golem/Bronze/P902 (P902 from Bronze, DONE) into main: 0 code file(s), 1 docs file(s)
13:34:01 Stop      would email: [Iron Golem] merged P902 from Bronze
```

What that left behind, checked before the world was deleted: the throwaway docs repo's `main` reads
`63e6e85 Merge golem/Bronze/P902: ...` (a merge commit with `cce1819` from the branch and `4811ffd`, Iron's own P901
commit, as its parents), equal to `origin/main` (pushed to the local bare origin); `notes\cc-P901-team-test-a.md` and
`notes\cc-P902-team-test-b.md` both on main; both prompts in `completed\`; `merge-queue\` empty. The session names
were "Golem Iron P901" and "Golem Bronze P902" in Windows Terminal tabs, each launcher setting `GOLEM_NAME` and
`GOLEM_ROOT`. The `status.json` written by the last event lacked the cards (Deviations 16), found by this run and fixed.
Two real sessions, about four minutes of Opus and Fable use each.

## Deviations and decisions for Chase

1. **The stray commits on GitHub** (`453735e` code, `6b13743` docs, "CC task P901: team test A ..."). Cause: I had
   changed `golem.ps1`'s `-Root` default from `'D:\UO\golem'` to `$PSScriptRoot` so a copied folder (the test world)
   would drive itself; with `[CmdletBinding()]` that variable is empty while defaults are evaluated (a two-line script
   proves it: the default sees `[]`, the body sees the folder), so every hook of the first test run had no root: no
   settings, so `multiGolem` read false; no state, so every Stop was "idle" and handed the next fixture prompt into the
   prompts root; and the Iron session's "P901 DONE" ran the real `Commit-ShardWork.ps1` with no `-CodeRepo` (the real
   repos), which committed my in-progress P184 console and web console files plus the morning's machine output and
   pushed. The real Golem's own hooks ran the same way for about an hour (12:59 to 13:16) but did nothing: `ENABLED`
   could not be found, so they exited; `state.json` and the real queue are untouched (checked). Fixed: `-Root`
   defaults to `''` and the body sets it from `$MyInvocation.MyCommand.Path`; the same in `Use-GolemLock.ps1`,
   `Integrate.ps1` and `Setup-Golem.ps1`. I did not revert or rewrite: both repos are public and the rule is that a
   pushed commit is not taken back; the content is this prompt's own work and will be the same at the P184 commit.
   Your call whether a plain "P184 covers the P901 commit" note in this file is enough (my assumption) or you want a
   revert-and-recommit pair for a cleaner history.
2. **A bare rename is not a safe claim on this PC.** `race.ps1` (12 runs, two processes, one file): 4 times both
   `[IO.File]::Move` calls returned without an exception (the file ended up in one place). The claim is therefore a
   `CreateNew` token first (exactly one process can make it), then the rename, then a check that the file arrived. The
   prompt's "atomic rename, the loser gets a not-found" holds only most of the time here; the token makes it always.
3. **`docs-only` never overlaps.** Read literally, two docs-only prompts overlap each other; but every prompt writes
   its own notes file (P126 Q4), and the prompt's own rollout test calls two docs-only prompts "non-overlapping". So
   `docs-only` is a free area; every other area overlaps itself.
4. **The integrator works on main, not on a branch.** Its own prompts go straight to main as today (one writer of main),
   and it merges the others between its own prompts and at the watch, only with clean trees. Merge, not rebase: the
   branch stays exactly as it was tested, one merge commit is one revert point, and nothing pushed is rewritten.
5. **The merge's checks are the build, not "the prompt's tests".** A prompt's tests are not machine-readable;
   `docker\uo\build.sh` (which runs the server test gate) runs when `server\` or `docker\uo\` changed, and
   `Commit-ShardWork.ps1 -Merge` keeps every commit check. Console and tool test runs on a merge are a follow-up.
6. **Two Docker builds at once were not measured with two real builds** (a build takes long, and this prompt had no
   server change). Reasoned instead: `build.sh` tags the builder per image tag, so images do not collide; CPU and the
   one daemon are shared; the merge build takes the `docker-build` lock, and sessions are told to. Serial by default.
7. **The guard is installed in both real repos too** (`Add-GolemHooks.ps1`), not only in worktrees: it costs 30 ms per
   tool call in any session without `GOLEM_NAME` (yours, mine) and only runs PowerShell in sessions the Golem opens
   while `multiGolem` is on, so the integrator's own sessions also obey the lock rule.
8. **The watch runs once per local Golem** by re-invoking `golem.ps1 -Event Watch -Golem <name>`, after one shared pass
   (stale locks, stale claims, the integrator's merge round). The scheduled task is unchanged.
9. **Codex lanes are registered, not handed:** an entry with `engine: codex` validates and shows a card, but its
   hand-off logs that P158 and P159 own that path. Their budget and runner are untouched.
10. **A second PC's claims and tickets go through git**, not a share: `queueMode: git` makes every claim, completion
    and fix-up a commit and a push in the prompts folder (a rejected push is a lost race, tested with two clones of a
    bare repo), and a pushed branch's `Golem-Ticket:` trailer becomes a ticket at the integrator's next watch. The
    prompts repo itself is Chase's to create (SECOND-PC.md step 6); the game PC stays in `folder` mode until then.
11. **The second PC's `D:` is a VHDX through diskpart**, re-attached by a SYSTEM startup task, not a partition and not
    Hyper-V's `Mount-VHD` (absent on Home); `-DryRun` on this PC stops correctly because `D:` is taken. Back-off while
    she uses the PC is `hours` in the registry; P159's "active session or a game running" rule is P159's to add to the
    same entry. Docker's data folder move is a Docker Desktop setting, printed, not scripted.
12. **`Commit-ShardWork.ps1` gained parameters, no check was weakened:** a branch commit must be on that branch and
    never `main`; a merge commit must be on `main`; the mirror, dashboard and scripts repo run only for the real pair.
13. **The `P182_TheGolemTabHasPokeRunNextAndRetry` fact was updated** on purpose: the queue row has a fourth button.
14. **Line endings:** every file written here is ASCII; the Golem folder's new files are CRLF (`Add-GolemHooks.ps1`,
    `Start-Golem.ps1`, `Stop-Golem.ps1`, `Setup-SecondPC.ps1`, `SECOND-PC.md` and `README.md` are LF, as they were or
    as written); the console and web console files keep the LF they had.
15. **Found by the rollout runs, fixed, each with the reason:**
    - a fresh clone does not exclude `.claude\settings.local.json` (the real repos do in `.git\info\exclude`, which a
      worktree shares), so Bronze's first claim was refused as "dirty"; `Setup-Golem.ps1` now writes that exclude line
      into each copy's common git dir when it is missing (a second PC's clones need it too);
    - a refused claim left the session with the phrase and no instructions, and it improvised (it found the queue
      folder and did the prompt without a branch); the hook now tells the session plainly to stop, and a DONE from a
      Golem session that holds no branch is not committed (emailed instead);
    - the first-start copy from cc-autopilot looked for a fixed `state.json`, so a non-integrator's first wake copied
      the ancient one; it now looks at the Golem's own state file;
    - `-Cli` (tests) disabled the Windows Terminal tab path; now only a `.cmd` stub does, so a real `claude.exe` named
      with `-Cli` opens the tab with the launcher that sets `GOLEM_NAME` (the direct-window launch died at once for the
      Iron session in two runs; the same command by hand, with its output captured, ran and claimed, so it was the
      window, not the session);
    - the Iron (Opus) session STOPPED at once because the unattended-permission hook denied the Read of its prompt
      file (a known trait of unattended sessions here); the multi hand-off now says to read it with Bash cat when Read
      is denied, and the retry (`RetryStopped`, then a wake after the two-minute rule) carried on;
    - the ticketed commit's message file was written with .NET's BOM-emitting UTF8, and git kept the BOM in the subject
      (`cce1819` in the throwaway repo); it is written without a BOM now;
    - "queue empty after P<nn>, the Golem rests" is what a non-integrator logs when nothing in the queue is for its
      lane; the wording is the old one (the queue may hold the other lane's prompts); the card and the hand-off log
      line say the precise thing.
16. **The integrator's own `status.json` write dropped the cards** (run 3): its status is an ordered hashtable, and
    `Add-Member` on a hashtable hangs a property on the wrapper that `ConvertTo-Json` never sees, so only a
    non-integrator's write (which reads the integrator's file back as an object) carried `golems`. Fixed with the
    indexer for a dictionary; the cards fact now also asserts the integrator's own write (red by the live run, green
    after the fix).
17. **Small marks the test left on this PC, undone:** the Golem's Windows Terminal profile fragment was rewritten with
    the throwaway folder as its starting directory (the next real wake rewrites it; restored by hand now); the
    throwaway sessions were stopped and the folder deleted; the real queue, `state.json`, `status.json` and prompts
    root were checked unchanged. A first-start copy of `smtp-cred.xml` from cc-autopilot into the throwaway root went
    with the folder. The Iron session in run 3 said DONE twenty seconds after taking the test-shard lock (the prompt
    asked for 90), without releasing it; the lock would have expired by its TTL.
18. **The real Golem emailed "NEEDS YOU: P184 stopped mid-task" once** (13:33) while this session waited on the
    rollout's monitors between turns; the later turns were read as waiting. Nothing was needed.

## For Chase

- **Turn it on:** in `D:\UO\golem\settings.json` set `"multiGolem": true`, then once
  `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Setup-Golem.ps1 -Name Bronze` (the worktrees under
  `D:\UO\golems\Bronze\` and their hooks). The next hook event migrates `state.json` into `state-Iron.json` (backup
  beside it). Then `D:\UO\golem\Wake-Golem.ps1 -Golem Bronze -Model Fable` (or the console's Wake once it learns
  `-Golem`; today it wakes the integrator) opens the Bronze session; your own sessions in the real folders are the Iron
  Golem's. One line to turn it on: `"multiGolem": true`. One line to turn it off: `"multiGolem": false` (claimed
  prompts stay in `claimed\<name>\` until you move them back).
- **Add a Golem:** an entry in `golems.json` (copy Bronze's: a UO-themed name, this PC's name, the lane, the areas,
  the two copies under `D:\UO\golems\<name>\`), `Setup-Golem.ps1 -Name <name>`, done. A PC: `SECOND-PC.md`. A Codex
  login: an entry with `engine: codex` and `account` (handed once P158 and P159 land).
- **What the console shows:** on the Golem tab, under the usual lines, `golems    : N in the registry (multiGolem on);
  the integrator is Iron`, then one line per Golem: name, lane, engine, machine, state, the prompt and its branch, the
  locks it holds, where its usage figure comes from; a bad registry is one amber line. The web console's Golem page
  has a Golems card with the same. The GOLEM tile stays the integrator's.
- **Stop one Golem without the others:** `Stop-Golem.ps1 -Golem Bronze` (its `ENABLED-Bronze` goes; the Iron Golem goes
  on), or `"enabled": false` on its entry, or `hours`. `Golem, stop` in a Golem's own session rests that Golem.
- **Merge now:** the Golem tab's Merge branches now (type `merge branches`), or `Integrate.ps1`. A conflict becomes
  `cc-P<nn>-cont-fixup-<orig>.md` in the queue, first in order, for the Golem that made the branch.
- **The sign-up sheet by hand:** `Use-GolemLock.ps1 -List`, `-Take test-shard -Minutes 60`, `-Release test-shard`.
- **The wife's PC:** `D:\UO\golem\SECOND-PC.md`, in order; `Setup-SecondPC.ps1 -DryRun` first; `Check-GolemSetup.ps1
  -Name Cobalt -PushTest` at the end says PASS on every line when it is ready.
- **The stray P901 commits:** see Deviations 1; nothing to do unless you want them reverted.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (the code repo reads clean
because the stray P901 commit already took this prompt's console files; the docs repo holds this note and the bot's
transcript):

```
Repo    Result
----    ------
code    clean
docs    dry run
scripts clean
```

No file over 5 MB was added. Scratch (the patch scripts, the race probe, the rollout scaffold) is in the session
scratchpad; the throwaway world under `D:\UO\golems-p184-test` was deleted after the run. The Golem's files are outside
git.

P184 DONE
