# cc-P770: Gold never claims its run-next (STEPHS-DESKTOP), and remote questions

Iron Golem, 2026-11-01 to 11-02. The changes are in the live kit (`D:\UO\golem`, not a git repo). Each changed file is backed
up as `<file>.bak-20261101-P770`. The full diff is `notes\cc-P770-tools\p770-kit.diff`, with the test logs and edit
scripts beside it. Docs copy `D:\UO\golems\Iron\shard-migration` on `golem/Iron/P770`, not committed.
- ssh only with `~/.ssh/golem-remote`.
- No PC restarted (only the family PCs' "Golem Remote Agent" tasks restarted, by the kit resync).
- No GitHub sign-in; no `.env`.

## In plain words

- **A Run next set on the tower now reaches Gold, Copper and Silver, and they act on it at once.**
  - Before, the pick was written on the tower, where the family PCs never look. Gold sat idle with P766 and P768 picked
    for it.
  - Now it goes to that PC's agent. The Golem turns itself back on if it had rested with an empty queue, and wakes
    for it within a minute.
  - Tested twice on Gold with throwaway prompts (P9770, P9772): each was claimed about a minute after the tower set it.
- **Gold's queue was frozen since 14:39 yesterday.** An answer's retry moved a prompt in Gold's local prompts folder
  without saving that move, and every later update failed. It now saves that move, and a stuck folder resets itself.
  Copper's and Silver's were behind too, the same way.
- **You can answer the family PCs' questions from the tower**, and the Sweep lists them. `Answer-Question.ps1 -Id <id>
  -Choice <n>` sends the answer to that PC, which resumes the prompt. Tested with a real question Gold asked (P9772):
  answered from the tower, Gold resumed it and finished.
- **For you:**
  - The two test prompts left small notes files in shard-migration's main (`notes\cc-P9770-run-next-test.md`,
    `notes\cc-P9772-remote-answer-test.md`); delete them if you don't want them.
  - Stone's PC (TEK-DIRECTOR) did not answer, so it gets these changes when it is next on.

## 1. Why Gold did not log or act

Four faults, found on STEPHS-DESKTOP over ssh and in the tower's kit:

1. **A run-next set on the tower never reached Gold.**
   - `Set-RunNext.ps1 -Golem Gold` and `Assign-Prompt.ps1 -RunNext` run `golem.ps1 -Event RunNext` on the PC they run
     on. On the tower that wrote `D:\UO\golem\RUN-NEXT-Gold` (still there: P768, set 17:17) and `RUN-NEXT-Copper` (P766,
     12:07).
   - Gold's watch reads its own `RUN-NEXT-Gold` on STEPHS-DESKTOP, which still said P765 from the 14:39 answer.
   - The agent channel that reaches Gold (`remote\Gold\commands`, the web console's Run next) was never used by the
     scripts.
2. **An idle Golem never wakes for a pick.**
   - A CC Golem's watch only wakes it for the night shift, marathon, a retried wake or a repaired clone. Otherwise it
     writes `status-Gold.json` and exits, logging nothing.
   - That is why `golem-Gold.log` showed no Watch lines; the overseer's "no lines after 10-28" was the last Watch line.
     The log itself had lines up to 14:39 from other events.
   - Also, when the queue empties the Golem turns itself off (removes `ENABLED-Gold`), and an off Golem's watch exits
     before anything else.
3. **Gold's prompts clone was frozen.**
   - At 14:39 the answer's retry (`Invoke-RetryStoppedCore`) moved P765 from `claimed\Gold` back to `queue\` and never
     committed it. In git mode every other queue change is committed and pushed.
   - From then on `git pull --rebase` failed on the uncommitted change. `Repair-PromptsClone` only fixes a stuck rebase
     or a wrong branch, so the clone stayed as it was (25 commits behind tonight) with a stale queue.
   - Copper (31 behind) and Silver (34 behind) were clean but behind: an idle Golem never pulls.
4. **Wakes started by the agent failed.**
   - At 14:39 the agent ran the answer's wake from its own long-running process (started 10-28 05:17): "wt.exe did not
     start ... Access is denied". The window it opened instead (process 80772) never reported, so no session ran.
   - The scheduled wake task (`GolemWakeGold`) and the Watch task run fine: wt worked at 12:05.
   - `schtasks /query` still showed `GolemWakeGold`'s last run as 12:05, so the overseer's 17:20 `schtasks /run` did not
     run the task.

**The kit snapshot (the Tinker's sync)** works as designed:
- The Tinker takes no new kit snapshot while any claimed prompt touches the golem area. P767's changes, and then
  P770's, were held by that rule (from 22:18).
- The PCs were "in step" with the 06:17 snapshot. P767's kit therefore had not reached them; it did with P770's forced
  snapshot below.
- For this prompt I ran `Tinker.ps1 -ForceSnapshot -NoFix` (its documented hand override "when that prompt's kit edits
  are finished") after each install, so the test could use the new kit. That was at 00:12, 00:19, 00:37, 01:04.

## 2. The fixes (all three family PCs run them; the Tinker reported Copper, Silver and Gold in step, hashes checked over ssh)

| File | Change |
|---|---|
| `Set-RunNext.ps1` | A Golem on another PC with an agent this console knows (`Test-GolemViaAgent`: not this PC, and `remote\<name>\agent.json` exists) gets the pick as an agent command (`runnext` / `runnext-cancel`), as the web console's button does; it says where it went. |
| `Assign-Prompt.ps1` | `-RunNext` for such a Golem goes through `Set-RunNext.ps1`. |
| `golem.ps1` (watch) | An idle Golem with a Run next pick wakes for it at its watch, through `Invoke-SelfWake` (usage, pace and the `autoWakeMinMinutes` spacing still apply; a refused wake waits for its retry time). Not while rested by hand, STOPPED, winding down or resting on a wrap-up or stopping point. It logs the wake, or once why not. |
| `golem.ps1` (RunNext event) | It syncs the git queue first, so the pick is looked up in origin's queue. It clears a stale pick (`Clear-StaleRunNext`: one no longer queued gives way to the pick waiting behind it). A Golem that rested on an empty queue is turned on again for the pick; a Golem rested by hand stays off. |
| `golem.ps1` (retry) | In git mode the retry's move back to `queue\` is committed and pushed. |
| `Golems.ps1` | `Sync-PromptsGit`: a failed pull on a dirty clone is reset to origin/main (`Reset-DirtyPromptsClone`), cleaning `queue`, `claimed` and `merging` and logging what it dropped. `Test-GolemViaAgent`. |
| `Remote-Agent.ps1` | After a `runnext`, `answer` or `retry` that worked, it runs this PC's "Golem Watch" task, so the wake happens at once in the session that can open the terminal. It sets `GOLEM_AGENT=1` for what it runs. |

**Proven on Gold**, from `golem-Gold.log`:
- P9770, Gold idle with a stale P765 pick:
  - 00:14:25 Run next set on the tower; 00:14:32 Gold's clone reset, logging what it dropped.
  - My first version queued P9770 behind the stale P765. Fixed: the sync now comes first and `Clear-StaleRunNext`.
  - 00:24:43 Gold's own watch: "cc-P765 ... is no longer in the queue: cleared; P9770 ... goes next now".
  - 00:24:50 "P9770 is picked and the Golem is idle: waking for it"; 00:25:14 "claimed P9770".
  - P9770 DONE at 00:26.
- P9772, Gold OFF (rested on an empty queue):
  - 00:38:50 Run next set on the tower; 00:39:34 "the Golem rested with an empty queue; on again for P9772".
  - 00:39:45 the agent-run watch woke it; 00:40:09 "claimed P9772". Under a minute from the tower.
- **Copper and Silver:** the same faults (picks never reached, clones behind, idle never woken), the same kit, so the
  same fixes. Their stale local picks (P263, P289, long finished) are now cleared at their next pick. I did not queue
  test prompts for them.

## 3. Questions from family PCs

- **Where they are.** A family PC's questions live on that PC (`questions\`). Its agent sends a copy to the tower as
  `remote\<Golem>\questions.json` (the open ones in full, the last five closed).
- **`Answer-Question.ps1` on the tower.** When the id is not a tower question:
  - it finds it in those copies (`Find-RemoteQuestion`);
  - it checks the choice and text there with the same rules;
  - it queues an `answer` command for that PC's agent and says so. If that PC is off, the command keeps an hour, and it
    says how to answer on that PC.
  - A closed one is refused.
- **On the PC,** the agent runs `Answer-Question.ps1 -Source remote`. The answer is written and the prompt goes back
  first, then the watch, run by the agent at once, wakes the Golem; the agent's own process no longer wakes it.
- **`join\Sweep.ps1`** prints "Remote questions:" with each open one, its choices and the command to answer it
  (`Get-RemoteOpenQuestions`).

**Proven.** I tried a dummy question file first (P9771). Gold's hook expires a question whose prompt is neither
STOPPED nor running, so it closed at once (P715's subject); I removed it. So the test used a real one:
- P9772 asked `Gold-P9772-20261102-004034-5c7c` through Ask-Chase.ps1 on Gold and stopped.
- The Sweep listed it.
- `Answer-Question.ps1 -Id Gold-P9772-20261102-004034-5c7c -Choice 0 -Who "overseer (for Chase)"` on the tower (00:41:21)
  sent it.
- On Gold: 00:41:23 "answer ... from remote (overseer (for Chase)): Yes", the retry, and "the watch run now for it:
  Golem Watch started".
- The wake came at the 00:54 watch: my first version waited 10 minutes after the last wake; it now uses the 5-minute
  wake spacing.
- P9772 DONE at 00:55.

## Tests

New facts in `tests\Lane.Tests.ps1`. All 3 are red on the live kit before the change (`lane770-red.txt`) and green after
(`lane770-green.txt`: 86 checks, 0 failed):
- `P770_ADirtyPromptsCloneIsResetToOriginAndItsQueueIsFreshAgain`: a real bare origin and clone. An uncommitted move
  plus origin moving on: the sync gives origin's queue and claims, nothing uncommitted is left, and the drop is logged.
- `P770_RunNextForAGolemOnAnotherPcGoesToItsAgent`: a runnext command with its prompt, no `RUN-NEXT-Gold` on this PC,
  and its cancel. Without `agent.json` it stays local.
- `P770_AnswerQuestionAnswersAQuestionAskedOnAnotherPc`:
  - a wrong choice, text where it takes none, and a closed question are refused;
  - the answer command carries the agent's input shapes;
  - nothing is written as a local answer;
  - the Sweep's list shows it.

Other suites on the changed kit:
- `RemoteAgent.Tests.ps1`: 90 of 90 (run with `-WebConsole` on my code copy, never the main desk's).
- `Assign.Tests.ps1`: 3 of 3. My first version sent a fixture's made-up PC to an agent; the `agent.json` rule fixed that.
- `Golem.Tests.ps1`, full: 1,685 passed, 5 failed (`golem770-final.txt`). The 5 are P184's overlap checks, which fail
  the same way on the live kit (P767's notes).
  - An earlier full run also failed P370_3: an answer with `-Source remote` but not from the agent must still wake
    directly. Fixed with `GOLEM_AGENT`.
  - P125 and P131 failed earlier only near midnight; they also fail on live then.
- Rerun on the final `golem.ps1`: P182 18, P747 30, P370 49, P131_SelfWake 29, P200 58, P183 33 checks, all passed.

## Deviations and decisions for Chase

- **The test prompts were real prompts.** P9770 and P9772 were queued in `cc-prompts` (Golem line Gold), run by Gold,
  and merged by ShadowIron.
  - Their notes files are in shard-migration's main: `notes\cc-P9770-run-next-test.md`,
    `notes\cc-P9772-remote-answer-test.md`. My branch is older than them, so I could not delete them here.
  - I removed the prompt files from `cc-prompts\completed`.
  - P9772's real question also reached your Tinker briefs as "Gold has a question about P9772".
- **Forced kit snapshots.** `Tinker.ps1 -ForceSnapshot -NoFix`, 4 times (00:12, 00:19, 00:37, 01:04), so P770's finished kit reached the PCs
  while P770 itself held the golem area. P767's kit changes went out with them.
- **Not removed:** the tower's stranded `RUN-NEXT-Gold` (P768, now an Iron prompt) and `RUN-NEXT-Copper` (P766). They
  never act (those Golems read their own PCs' files); deleting them was refused in this unattended run. Remove them by
  hand if you like.
- **Stone (TEK-DIRECTOR)** did not answer any round tonight. It gets the kit when it is next on.
- **The P184 overlap failures** (5 checks, on the live kit too) are worth their own prompt: "Iron takes P104, not the
  server prompts" fails.

## Files

- **D:\UO\golem** (live kit, backups `.bak-20261101-P770`): `golem.ps1`, `Golems.ps1`, `Set-RunNext.ps1`,
  `Assign-Prompt.ps1`, `Answer-Question.ps1`, `Questions.ps1`, `Remote-Agent.ps1`, `join\Sweep.ps1`,
  `tests\Lane.Tests.ps1`.
- **shard-migration:** this file and `notes\cc-P770-tools\`:
  - the kit diff;
  - the test logs;
  - the edit scripts;
  - the two test prompts and the dummy question.

P770 DONE
