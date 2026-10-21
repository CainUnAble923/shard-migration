# cc-P222: the Tinker, a watchdog that unsticks the Golems and keeps every PC's kit in step

2026-10-20. The Iron Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P222-tinker-golem-watchdog.md` (with
its 17:33 addendum). Work copies `D:\UO\golems\Iron\ShatteredLegacy` and `...\shard-migration`, branch
`golem/Iron/P222`. Both were clean at the start. Read first: P184, P186, P187 and P208's notes, `Retry-Stopped.ps1`,
`Remote-Agent.ps1`, `ShadowIron.ps1`, and today's overseer entries. P216 (questions on the console) is not in main, so
the Tinker asks through NEEDS YOU on its card and email. This session had no task-list tool, so it reported its steps
with P153's `Set-Step.ps1`.

## Headlines

- **The Tinker runs.** It is a script Golem in `golems.json` (engine `script`, not the integrator, areas `[]`): it never
  claims a prompt. The scheduled task **Tinker** (registered, Ready) runs `D:\UO\golem\Tinker.ps1` every 10 minutes on
  the game PC. It has its own log (`golem-Tinker.log`), card (`status-Tinker.json`, shown on both consoles with Run now,
  Pause and Resume) and ledger (`tinker-ledger.json`).
- **One real round: Gold, Copper and Silver are in step with the game PC.** At 18:54 to 18:55 the round sent each PC
  only what differed (16, 16 and 17 files, as one zip over SSH). Each PC installed it all or nothing through the zip's
  own `Install-Kit.ps1`, and each Remote Agent restarted on the new script. Afterwards all three PCs' `golem.ps1` and
  `Golems.ps1` hashes match the tower's (`E9A65C38...`, `FF838C30...`), and `kit-state.json` says kit `4f81abf25f14`
  on each. The card shows it ("Copper in step; Silver in step; Gold in step; Stone NOT in step: its PC did not
  answer"). Stone (the work PC) did not answer over SSH; see Deviation 4.
- **The kit in step** (`Kit.ps1`, `Install-Kit.ps1`):
  - A manifest (`kit-manifest.json`: path, SHA-256, size, and the settings keys a kit may add) covers every
    `D:\UO\golem` script, guide, `golems.json`, `golem-paths.json`, the rulebook and `D:\UO\unattended-permission.ps1`.
    Per-PC files never travel.
  - The install checks every hash, parses every script, and validates the new registry with the new `Golems.ps1` in a
    child process before swapping anything. It backs up the old files, renames all the new ones in together, and rolls
    back if any rename fails.
  - `settings.json` only gains missing keys (the 15:58 `mergeGolem` case).
  - A snapshot is taken only while no claimed prompt holds the `golem` area. The 18:57 scheduled round said "not
    taken: Iron runs P222, which touches the golem area".
  - The Remote Agent also pulls the kit from the web console (`/api/agent/kit`), once the game PC runs this branch's
    `server.py`.
- **The known stalls, each fixed and counted:**
  - **own-wip:** the Golem's own uncommitted work on its own branch. It is kept as a WIP commit with no Golem-Ticket
    line, then the flag is cleared and the Golem woken.
  - **lost-handoff:** a DONE whose hand-off was lost, when the notes end `P<nn> DONE` on `golem/<G>/P<nn>`. The
    Golem's own hook commits it with its ticket.
  - **low-memory:** a build killed for low memory. The Tinker waits for more than 8 GB free and no Docker build, then
    retries, at most twice a day per prompt.
  - **watch-failing:** a Golem's watch silent for 20 minutes, or an error in its log. The Tinker resyncs the kit and
    reports.
  - **stale-needsyou:** a NEEDS YOU whose cause is gone (the copy is clean, the lock is free). The flag is cleared.
- **Everything else becomes one plain question**, after a short reasoning session when that is allowed. It runs
  `claude -p` read-only in a scratch folder, Fable (Opus for merge or registry problems), with a bundle and
  `tinker-rulebook.md`, and answers in a fixed JSON shape. Only a fix on the list is applied, by the script. Limits: 6 a
  day, none over 90% of the week, none for the same Golem and prompt within the hour.
  - **It worked on its first real round.** For Copper's P212 the session said the prompt needs files that live only
    on the game PC, so a retry on Copper would stop the same way; it asked rather than guess. For Silver's P169 it said
    the session looks frozen on a Read since 17:50, and that a second session could collide with it; it asked too.
    Both went to Chase as questions (emails below). No fix was applied.
- **The never list is code:** `Test-TinkerScriptSafe` refuses any script that pushes main, resets, cleans, stashes,
  deletes or force-pushes a branch, deletes a work copy, touches live or Haven, or runs a Claude session on a Golem's
  PC. A fix comes at most twice a day per Golem and prompt; the third time is a question, as a pattern.
- **Causes 2 and 3, fixed at the source with tests:**
  - A claim that finds its own earlier prompt's uncommitted work keeps it as a WIP commit on that branch and goes on.
  - A branch that already has work is never reset to main.
  - A DONE with a lost hand-off takes its branch back from the work copy.
  - The overseer's `Get-MultiHandOffText` fix for the extra PCs is kept and now has a fact.

## What changed

### `D:\UO\golem` (not a repo; backups `*.bak-20261020-P222` of Golems.ps1, golem.ps1, Remote-Agent.ps1, golems.json, README.md, JOIN-PC.md, tests\Golem.Tests.ps1)

| File | Change |
|---|---|
| `Kit.ps1` (new, 206 lines) | `Get-KitFiles` :35, `New-KitManifest` :55, `Compare-KitManifest` :68, `Test-KitRegistryInChild` :88, `Install-KitStaging` :101 (hashes, parse, registry, backup, all-or-nothing swap with rollback, settings keys added only, `kit-state.json`), `New-KitSnapshot` :171 (`kit\current`, three earlier kept), `New-KitStaging` :197 |
| `Install-Kit.ps1` (new) | the installer a PC runs from its staging folder; `-RestartAgent` ends and starts the agent task when `Remote-Agent.ps1` changed; one JSON line |
| `TinkerLib.ps1` (new, about 610 lines) | the never list `Test-TinkerScriptSafe` :53; `Invoke-TinkerOnPc` :76 (here, or SSH + scp as `golem@<tailscale>` with the `golem-remote` key, every script checked first); the facts script; `Get-TinkerFinding` :178 (pure); `Get-TinkerFixScript` :233 / `Invoke-TinkerFix` :309 (the listed fixes); `Sync-TinkerKit` :360; `Add-TinkerQuestion` :406; `Test-TinkerEscalationAllowed` :420 and `Invoke-TinkerEscalation` :460; `Add-TinkerCause` :490 (learning); `Invoke-TinkerRound` :514; `Write-TinkerStatus` :597 |
| `Tinker.ps1` (new), `Tinker-Hidden.vbs` (new) | a round; `-Pause`, `-Resume`, `-Register`, `-Unregister`, `-ForceSnapshot`; one round at a time (a mutex) |
| `tinker-rulebook.md` (new) | what the reasoning session reads: the JSON shape, the nine allowed fixes, the never list |
| `Golems.ps1` | `Reset-GolemBranch` :560 (keeps its own earlier branch's work as WIP and goes on) and :575 (a branch with work is checked out as it is, never reset); `Get-GolemCards` :1001 (the `tinker` block) |
| `golem.ps1` | `-Event Clear [-Reason]` :2729 (the Tinker clears a flag); `Get-LostHandOffBranch` :1576, used at a DONE with no branch :3654; the "holds no branch" log line no longer loses its end (`Log "..." + ...` passed only the first string) |
| `Remote-Agent.ps1` | `Sync-AgentKit` :173 and the loop :255: every `-KitMinutes` (10) it compares with the web console's kit, fetches what differs into `kit-staging\<id>\`, installs with `Install-Kit.ps1`, and restarts its own task for a new `Remote-Agent.ps1`; an older web console (404) is skipped |
| `golems.json` | the Tinker entry (engine script, display "the Tinker", areas []) and a line in `_comment` |
| `README.md` | new section "The Tinker" (who, the kit, the known stalls, questions and the reasoning session, never, learning, the source fixes, settings) |
| `JOIN-PC.md` | after the join the kit keeps itself in step; nothing needs copying by hand |
| `tests\Tinker.Tests.ps1` (new, 14 facts) and `tests\Golem.Tests.ps1` (3 P222 facts) | below |

### `D:\ShatteredLegacy` (this branch)

| File | Change |
|---|---|
| `web-console/server.py` | `GET /api/agent/kit` and `/api/agent/kit/file?path=` (an agent's secret needed; only a path the manifest lists, no folders or `..`): `kit_manifest` :764, `kit_file` :769, `KIT_PATH` :93 |
| `web-console/static/app.js` | `tinkerCard` (last round, fixes today, recent fixes, questions, waiting, the kit on each PC) with Run now and Pause or Resume; Shadow Iron's card logic no longer takes the Tinker for a merge Golem |
| `web-console/golem-actions.json`, `console-actions.json` | `tinker-run`, `tinker-pause`, `tinker-resume` (card `tinker`), twinned with the console |
| `web-console/tests/test_remote_golems.py` | the kit routes fact |
| `scripts/Shard-Console.ps1` | `TinkerScript` :250; actions `golem.tinkerrun`, `golem.tinkerpause`, `golem.tinkerresume` in the Golem merge row (:1259), phrases `run tinker` / `pause tinker` / `resume tinker`, plan :5717, safety :3385 (Tinker.ps1 alone, or with -Pause or -Resume), tooltips |
| `scripts/tests/Shard-Console.Tests.ps1` | `P222_TheTinkersButtonsRunTinkerPs1AfterTheirPhraseAndNothingElse` |
| `CHANGELOG.md`, `VERSION` | 2026.10.20.10, one `### Staff` line |

## Tests

**`D:\UO\golem\tests\Tinker.Tests.ps1`** (new): **132 checks, 0 failed**, run against the live kit. Each fact runs
in a temp folder with a fake game PC kit, a fake remote PC kit, fake work copies (git), and fakes for the PC runs, the
reasoning session (a `.cmd` printing a fixed answer) and the mail.

| Fact | What it pins |
|---|---|
| `P222_TheKitManifestHasTheScriptsTheRegistryAndTheHookButNoPerPcFile` | what the kit holds; 15 per-PC file kinds never in it; a bad path refused |
| `P222_AKitSwapIsAllOrNothingWithTheRegistryValidatedFirstAndPerPcFilesUntouched` | a bad registry refuses the whole install with nothing swapped; a wrong hash refuses; a swap failing part way is rolled back byte for byte; the good kit installs; per-PC files untouched; settings keep their values and gain only the missing key; backups |
| `P222_TheTinkerSendsAndInstallsTheKitOnARemotePcThroughItsOwnStagedInstaller` | one zip, the staged Install-Kit.ps1, in step; the next round sends nothing |
| `P222_NoSnapshotWhileAPromptHoldsTheGolemArea` | the hold, and `-ForceSnapshot` |
| `P222_EachKnownStallIsRecognized` | own-wip; another Golem's work (unknown, not guessed); stale-needsyou; lost-handoff and its "no DONE in the notes" case; low-memory; watch-failing (silent, or a recent error), an old error and an off Golem ignored; unknown; a running Golem |
| `P222_OwnWorkIsKeptAsWipTheFlagClearedAndTheGolemWokenAndTheThirdTimeIsAQuestion` | the WIP commit (no ticket line), Clear, Wake, the card's count; the third time a question, one email, NEEDS YOU on the card |
| `P222_ALowMemoryKillWaitsForMemoryAndNoBuildThenRetriesAtMostTwiceADay` | waits under 8 GB and during a build, then Retry; twice a day, then a question |
| `P222_ALostHandOffIsCommittedByTheGolemsOwnHook` | the Golem's hook told `P<nn> DONE` again |
| `P222_TheNeverListRefusesEveryForbiddenScript` | twelve forbidden scripts refused, four allowed; every fix script passes; refused before it runs; an unlisted fix has no script |
| `P222_AnUnknownStallGoesToAReasoningSessionAndOnlyAListedFixIsApplied` | a fake `claude -p` returning each answer shape: a listed fix is applied, an unlisted fix becomes a question, an ask becomes a question, an answer in no shape becomes the plain question; read-only, Fable, a scratch folder, the bundle and answer kept |
| `P222_TheReasoningSessionsLimitsHold` | 6 a day, the hour, 90% of the week, Opus for a merge or registry problem |
| `P222_TheSameCauseThreeTimesDraftsANewKnownRuleForTheOverseer` | three occurrences draft once; the same stall on later rounds does not count |
| `P222_TheTinkerHasACardWithItsRoundFixesQuestionsAndKit` | `Get-GolemCards`' `tinker` block; Pause: nothing runs, PAUSED on the card |

The Tinker facts are new files, so their first runs could only fail. Several did while I wrote them: the swap
fault-injection named an unchanged file, the remote install answer was hidden by CLIXML progress on stderr and by an
empty `-RestartAgent ''`, and a real Docker build on this PC decided the low-memory fact. Each was fixed in the code or
the fact.

**`tests\Golem.Tests.ps1`**, three new facts. Each failed on the untouched golem.ps1/Golems.ps1, except the hand-off
text fact, which pins the overseer's earlier fix and passes on both:
`P222_AClaimKeepsItsOwnEarlierBranchsWorkAsAWipCommitAndNeverResetsABranchWithWork`,
`P222_ADoneWithALostHandOffIsCommittedFromItsWorkCopysBranch`, `P222_AnExtraPcsHandOffNamesItsOwnClonesAsItsWorkCopies`.
Full suite on the staged kit (identical to the deployed one apart from TinkerLib): **836 checks passed, 5 failed**.
The 5 are the two P184 facts in Deviation 9.

**Web console** (`python -m unittest discover -s tests`): **69 tests OK** (1 skipped). The new
`test_the_kit_manifest_and_only_its_files_are_served_to_an_agent` failed on the old `server.py` and passes now.

**Shard Console** (Windows PowerShell 5.1): the new `P222_TheTinkersButtonsRunTinkerPs1AfterTheirPhraseAndNothingElse`
failed on the old console and passes. Full suite: **427 facts, 415 passed, 12 failed**. The 12 are the ones that fail
the same way on the old console in a work copy (P153's notes): `hues.mul`, the Haven cutover links, and two newer
server commands. `P187_EveryConsoleButtonHasAWebTwin` caught the missing web twins, which are now added.

## The real round, as it ran

From `D:\UO\golem\golem-Tinker.log` (the first round at 18:52 had an SSH quoting bug: every remote PC "did not
answer", because PowerShell 5.1 drops the inner quotes on the way to ssh.exe and the remote cmd.exe took a pipe as its
own. Fixed, then the round below):

```
18:54:52  kit on AINSLEYS-LAPTOP (Copper): installed kit 4f81abf25f14: 16 file(s); agent restarted
18:55:15  kit on ELLIES-LAPTOP (Silver): installed kit 4f81abf25f14: 17 file(s); agent restarted
18:55:22  kit on STEPHS-DESKTOP (Gold): installed kit 4f81abf25f14: 16 file(s); agent restarted
18:55:23  kit on TEK-DIRECTOR (Stone): its PC did not answer
18:56:06  round: kit 4f81abf25f14 (new kit 4f81abf25f14); Copper in step; Silver in step; Gold in step;
          Stone NOT in step: its PC did not answer; 0 fix(es), 1 question(s) (95 s)
18:58:42  round: kit 4f81abf25f14 (not taken: Iron runs P222, which touches the golem area); ... (the scheduled task)
```

Checked on each PC afterwards over SSH: `golem.ps1` `E9A65C38...` and `Golems.ps1` `FF838C30...` (the tower's), and
`kit-state.json` id `4f81abf25f14` from CHASES-TOWER. The agents' logs say "agent for the <name> Golem started" at
18:54 to 18:55, and each polled the web console by 18:56. In `status.json` the card reads `Tinker: NEEDS YOU` with
the kit block above.

Emails the Tinker sent to Chase (through the game PC's own mail, so an extra PC's NEEDS YOU is now heard):
`[Tinker] NEEDS YOU: Copper P212` (18:52) and `[Tinker] NEEDS YOU: Silver P169` (18:53). Silver's was sent again at
18:56, because the question's words changed. It was sent once more at 19:08, the first round after the key changed to
one email a day per Golem and prompt, since the old entry did not match the new key. From then on it is once a day.

## Deviations and decisions for Chase

1. **The kit travels over SSH today, and over the web console once it is updated.** The prompt has each Remote Agent
   fetch the kit from the console. That is built and tested (`/api/agent/kit`). But the running web console is
   `D:\ShatteredLegacy` on main, which gets these routes only when this branch is merged and the web console is
   restarted. The extra PCs' agents also predated this prompt. So the Tinker also sends the kit itself, over the SSH
   the overseer already uses (`golem@<tailscale>`, the tower's `golem-remote` key). That is the path that put Gold,
   Copper and Silver in step today. Both paths install with the same `Install-Kit.ps1`. Until the console restart,
   the agents' kit check gets a 404 and skips quietly.
2. **The real round ran with `-ForceSnapshot`.** P222 itself holds the `golem` area, so the normal rule takes no
   snapshot while it runs. My kit edits were finished, so I took the snapshot by hand for the real round. Since then,
   every scheduled round has said "not taken: Iron runs P222". After this DONE, the next round snapshots today's last
   two small TinkerLib fixes (made after the round: a per-occurrence count and one email per Golem and prompt a day)
   and sends them.
3. **Two learning and email fixes came from the real rounds.**
   - Silver's single ongoing stall was counted again on every round, and after three rounds the Tinker wrote a "new
     known rule" draft. A cause now counts once per Golem, prompt and cause. I removed that early draft and reset the
     ledger's counts.
   - Silver was also emailed twice. Now it is one email a day per Golem and prompt.
4. **Stone (TEK-DIRECTOR, the work PC) did not answer over SSH.** The registry has it enabled with no status file on
   the game PC. Its card says "NOT in step: its PC did not answer", and the Tinker tries again every round. Joining it
   is still the overseer's open item.
5. **Two questions are waiting for you on the Tinker's card:**
   - **Copper, P212:** it needs files that live only on the game PC. The reasoning session suggests running it on a
     game-PC Golem.
   - **Silver, P169:** its session looks frozen since 17:50. Close it or wake it; the session thought a second session
     could collide with the hung one.
6. **The hook fixes are in their own place.** "Hooks" in the kit means the hook scripts: `golem-guard.cmd`,
   `golem-nudge.cmd` and `D:\UO\unattended-permission.ps1`. Each repo's `.claude\settings.local.json`, which names
   them, is git-ignored and the same on every PC (`Add-GolemHooks.ps1`). It is not part of the kit, so it never
   overwrites a PC's own.
7. **`resolve-generated-conflict` refuses anything but generated files.** It takes main's side of the generated files
   and uses P213's `Resolve-NotesConflict` for CHANGELOG and VERSION. It works only on the Golem's own branch.
8. **The tests that create the kit's fakes never touch the real kit.** A fake that would open a session (Wake, Retry,
   the hook) is only recorded. A fact that reaches `D:\UO\golem\` throws. The remote root comes from the test's own
   settings, and no scheduled task is ended or started.
9. **Two Golem facts were already failing, before my changes:** `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged`
   and `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly` (P153's notes, Deviation 6). I did not change that code.

## For Chase

- **The Tinker's card** is on both consoles (the Golem tab's merge row has **Tinker: run now**, **Pause the Tinker**
  and **Resume the Tinker**; the web console's card has Run now and Pause or Resume). It shows the last round, the fixes
  today, the open questions, and which PCs' kits are in step.
- **Its questions** come by email too, once a day per Golem and prompt, each saying what the Tinker would do if you
  said yes.
- **New PCs need no kit copying:** the Tinker keeps their kit in step within 10 minutes.
- **To stop it:** `D:\UO\golem\Tinker.ps1 -Pause`, or Pause on its card.

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P222 -NoRefresh -NoArchive`.
Nothing blocked. Code: 9 files; docs: this note. No file over 5 MB.

```
Repo Result
---- ------
code dry run
docs dry run
```

P222 DONE
