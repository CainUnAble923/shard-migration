# P208: Shadow Iron, a merge-only Golem on the game PC (Iron becomes a normal Golem)

## Headlines

- **Shadow Iron merges now.** Cutover done at 15:39 on 10-20 (`settings.json` `"mergeGolem": "ShadowIron"`). The
  scheduled task **Shadow Iron** runs a merge round every 10 minutes as Chase, whether or not any Golem is awake.
- **The backlog is in main.** First round (15:40 to 15:45): **P203 merged** (P150's requisitions board, the Appraiser
  and Leads) and **P204 merged** (P191's skill-gain retune and the P202 fix-up). Both server builds were green and both
  repos were pushed (code `ceb4113`, docs `62683e6`). Second round (15:50): "nothing waiting". P151 and P201 were
  already in main. P150's, P191's and P202's leftovers moved from `merging\` to `completed\` (prompts repo `050eca0`).
- **Iron is an ordinary Golem** from its next prompt on. It works in `D:\UO\golems\Iron\ShatteredLegacy` and
  `...\shard-migration` on `golem/Iron/P<nn>`, and gets a merge ticket at DONE. Its lane stays Opus, its areas `*`.
  This prompt was handed on main, so its DONE is still committed on main in the real folders. The hook does that by
  design (see below).
- **Fixed on the way:** the integrator re-ticketed Gold's P151 and P201 at every round after they had merged, and
  each pass made an empty merge commit (twice on 10-20). A branch already in main is no longer ticketed.

## What changed

**`D:\UO\golem` (not a repo; backups `*.bak-20261020-P208`)**

- `Golems.ps1`
  - The registry rules:
    - New engine `script`. A script Golem never claims: `areas` must be `[]`, its lane is not read, and
      `Get-ClaimCandidate` and `Invoke-Claim` refuse it.
    - There is still exactly one integrator.
    - With `mergeGolem` set (read from the `settings.json` beside the registry), the integrator must be that script
      Golem, and a Golem that claims cannot be the integrator. With it off, the integrator must be a Golem that claims.
  - **Home Golem** (`Get-GolemHome`): the integrator, or with a script integrator the first claiming Golem on its PC
    (Iron). The home Golem keeps `golem.log`, `ENABLED` and the base of `status.json`, is the fallback for a hook with
    no name, and is the consoles' own Golem.
  - Merge round changes:
    - `Sync-RemoteTickets` skips a branch already in main.
    - `Invoke-Integrate` changes:
      - A busy lock ends the round, so the oldest ticket stays first.
      - A ticket another round already took is skipped.
      - A branch with nothing new is completed without a merge commit.
      - A fix-up's branch that fails again returns `needsyou` and gets no fix-up.
    - `New-FixupPrompt` names the fix-up after the original prompt and strips any `cont-fixup-` prefixes.
  - Cards carry `home`, `script`, `display` and a script Golem's `merge` block.
- `golem.ps1`
  - New events:
    - `-Event MergeRound`: does nothing unless `mergeGolem` names that Golem.
    - `-Event MergePause -On|-Off`.
  - `Invoke-MergeRound` steps:
    1. Checks for a pause.
    2. Takes the `merge-round` lock.
    3. Pulls the prompts repo.
    4. Runs `Sync-RemoteTickets`.
    5. Checks that both real folders are clean and on main. If not, it waits, shows the reason on its card and sends
       one email per dirty spell naming the files.
    6. Runs `Invoke-Integrate`.
    7. Sends emails (merged, fix-up, or NEEDS YOU with the output).
    8. Writes `status-ShadowIron.json` and refreshes the cards in `status.json`.
  - `-Event Integrate` (the old Merge branches now) runs one of Shadow Iron's rounds when the integrator is a script
    Golem. The watch and the after-DONE round leave merging to Shadow Iron.
  - Hooks from a session opened in the real folders without `GOLEM_NAME` resolve to Shadow Iron and do nothing, apart
    from the status line.
  - **A prompt handed on main finishes on main.** At DONE it is committed in the real folders as before, then the
    Golem goes back to its own work copies for the next claim. The worktree guard also lets it write there.
  - New setting key `mergeGolem`.
- New `ShadowIron.ps1`: one round, `-Pause`, `-Resume`, `-Register` and `-Unregister` (the task). New
  `ShadowIron-Hidden.vbs`: the windowless launcher.
- New `Set-MergeGolem.ps1 -On|-Off`, the switch.
  - It validates `golems.json` and `settings.json` together before writing either, and backs both up
    (`.bak-<stamp>-mergegolem`).
  - On: it runs `Setup-Golem.ps1 -Name Iron` and registers the task. It refuses while Iron runs a prompt unless
    `-Force` is given.
  - Off: Iron becomes the integrator in the real folders again, Shadow Iron is disabled, and the task is removed.
- `README.md`: new section "Shadow Iron merges (cc-P208)" (who merges, the loop, waits, fix-ups, the card, by hand,
  the switch, the registry rules) and the Files table. `JOIN-PC.md`: who merges and how to pause it.
- `tests\Golem.Tests.ps1`: five `P208_*` facts, 52 checks, all green:
  - the registry rules and the switch;
  - oldest first, one fix-up named after the original, a fix-up's second failure going to Chase, handled markers and
    no re-ticketing;
  - a busy lock, a dirty tree and a pause each wait without a fix-up;
  - Iron's hand-off makes a branch and a ticket, the cutover prompt finishes on main, and the guard;
  - `Set-MergeGolem.ps1` both ways.

**`D:\ShatteredLegacy`** (committed as "CC task P208 (part 1, before the cutover)", `7fec950`; the changelog and
VERSION 2026.10.20.4 come with this DONE)

- Web console:
  - **Shadow Iron's card**: the last round and its result, the tickets waiting, the last merge, the last failure, a
    dirty-tree warning and PAUSED, with the buttons **Merge now**, **Pause merging** and **Resume merging**. It shows
    no lane, usage or Wake.
  - Iron's card is an ordinary card. Iron is still the console's own Golem (the Controls).
  - Shadow Iron is not in the picker, and a Golem button aimed at it is refused.
  - `golem-actions.json`: the buttons have a `card: merge` field, and `merge-pause` / `merge-resume` use
    `when: mergePaused:on|off`.
  - Files: `server.py`, `static/app.js`, `console-actions.json`.
- Shard Console:
  - A Golem-tab line for Shadow Iron.
  - New actions `golem.mergepause` and `golem.mergeresume`, which run `ShadowIron.ps1 -Pause` or `-Resume` after
    their phrase. `Test-PlanSafety` allows exactly those two arguments.
  - The picker treats the home Golem as the console's own.
  - `Invoke-WebConsoleAction.ps1`: the same home rule.
- Tests:
  - Shard Console: new fact `P208_ShadowIronHasItsOwnCardLineAndButtonsAndIronStaysTheConsolesOwn`. Run: 419 of 425
    pass.
  - Web console: new test for the picker and the home Golem. All 68 tests pass.

## The cutover, as run

1. Built and tested everything with the switch off, then committed and pushed both repos (`7fec950` / `ce43ff8`). The
   prompt said to finish my own commit first, so I did this before the switch.
2. P203 still conflicted with main, only on CHANGELOG.md and VERSION (main had gained P187 and P200 since). As a
   fix-up it would have gone straight to NEEDS YOU, so I merged main into `golem/Bronze/P203` in a temporary
   worktree:
   - CHANGELOG.md keeps both sides; P150's section sits under a new heading 2026.10.20.3.
   - VERSION takes the higher number.
   - Committed `b2db9d5` with a `Golem-Ticket:` trailer and pushed.

   P204 merged cleanly. Its code is on the local branch `golem/Bronze/P204` (= P202's head). Removed the stale
   `handled-P204-*` markers (left by the busy-lock bug; kept in `D:\UO\golem\merge-queue-removed-P208\`).
3. `Set-MergeGolem.ps1 -On -Force` at 15:39: wrote both files and made Iron's worktrees and hooks. Registered the task.
4. The 15:40 round merged P203 then P204, built each and pushed. The 15:50 round found nothing waiting. The card in
   `status.json`: ShadowIron IDLE, "P203 merged, P204 merged", 0 waiting.

## Deviations and decisions for Chase

- **I committed before the cutover myself** (`Commit-ShardWork.ps1` under the commit lock). The hand-off said not to
  commit, but the prompt says "finish your own commit first", and the switch cannot be flipped with my work still
  uncommitted in the real folders. This DONE's commit (notes, changelog) is made by the hook on main.
- **I resolved P203's CHANGELOG/VERSION conflict on Bronze's branch** so the backlog could merge. P213 (queued) is
  meant to make the merger do this by itself.
- **Starting the task by hand (`Start-ScheduledTask`) was refused by the unattended-mode permission check.** I waited
  for its own 15:40 run instead.
- **The task runs "only when Chase is signed in"**, like the Golem Watch. Pushing main needs his GitHub login
  (credential manager). Running while signed out would need his password stored on the task.
- **The first round's log lines are missing.** My own `tail -F` on `golem-ShadowIron.log` blocked the hook's writes
  (they fail quietly). Git and the status file show what that round did; the 15:50 round logged normally.
- **To roll back:** `D:\UO\golem\Set-MergeGolem.ps1 -Off`. To pause merging: Pause merging on the card, or
  `ShadowIron.ps1 -Pause`.
- **Test failures that existed before this prompt** (they fail the same way on the pre-P208 copies):
  - Golem suite: `P184_OverlappingTouches...` and `P184_TouchesAreRead...`. The overseer made `server` a parallel
    area today and these facts still expect the old rule.
  - `P200_Marathon_Wakes...` failed once while three suites ran at the same time, then passed on its own.
  - Join suite: 4 facts (the join-kit patches of 10-20).
  - Shard Console: 6 facts tied to live data (Haven cutover links, the play-test count, the `artificerrank` command).
- I saw a `Crystal` entry in `golems.json` (disabled). It was not mine and I left it alone.

P208 DONE
