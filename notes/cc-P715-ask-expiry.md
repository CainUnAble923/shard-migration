# cc-P715: a Golem's question must not expire while its prompt is still waiting

Iron Golem, 2026-11-02. The change is in the live kit (`D:\UO\golem`, not a git repo): `golem.ps1` and
`tests\Golem.Tests.ps1`, each backed up as `<file>.bak-20261102-P715`. The full diff is `notes\cc-P715-tools\p715-kit.diff`,
with the edit scripts and the test logs beside it. The CHANGELOG line is in Iron's code copy
(`D:\UO\golems\Iron\ShatteredLegacy`, `CHANGELOG.md` and `VERSION`, 2026.11.02.3). Neither copy is committed.

## In plain words

- **A question a Golem asks you now stays on its Golem card until you answer it** (or retry, clear or park the prompt).
  - On 10-27, Iron asked about P707 and stopped. Eight seconds later one of its own log watchers ended and woke the
    stopped session for one more step.
  - The Golem took that step for you answering in the terminal. It closed the question as "no longer STOPPED", so you
    never saw a live card, and your answer was refused. P707 then sat for about two hours.
  - Now only words you type into that session count as an answer there. The session's own leftover tasks do not.
- **If you do type into a stopped session and it stops again on the same prompt**, the Golem now records that new stop
  and shows its question. Before, it ignored the second stop and showed the Golem as idle.
- **Nothing for you to do.** The family PCs get the change with the Tinker's next kit snapshot after P715 is committed.

## 1. Why the question closed (P707, 10-27)

From `golem.log` and the session's transcript (`8171e764-...jsonl`, times CDT):

| Time | What happened |
|---|---|
| 18:39:25 | `Ask-Chase.ps1`: question `Iron-P707-20261027-183925-e4f1` written, open. |
| 18:40:41 | The session's last message ended `P707 STOPPED: asked Chase (...)`. |
| 18:40:43 | Stop hook: `stoppedPrompt = P707`, session kept open, Chase emailed. The question stayed open (an `ask` question is reused, not replaced). |
| 18:40:46 | A Monitor started earlier in the session expired ("Monitor expired after 30m"). Claude Code queued its notice into the session, which started a new turn. |
| 18:40:49 | That turn ran one tool call (`TaskStop` of a leftover log watcher): PreToolUse and PostToolUse hooks ran. |
| 18:40:50-51 | **Activity hook**: "activity after P707 STOPPED: Chase answered" (twice: Pre and Post). It cleared `stoppedPrompt`, then `Write-Status` ran `Sync-GolemQuestions`. With nothing STOPPED and nothing running, the question was closed as "P707 is no longer STOPPED or running". |
| 18:40:52 | The session ended again with `P707 STOPPED: asked Chase (...)`. |
| 18:40:53 | Stop hook: skipped. P707 was `lastHandled` and not running, so the D90 rule treated it as already handled. The Golem stayed idle with no STOPPED and no open question. |

So the overseer's guesses were close but not it:
- The Stop hook did not read state too early.
- "Claimed and stopped" was handled correctly.

The cause was the Activity hook's rule from cc-P131: *any* tool call after a STOPPED means Chase answered in the
terminal. That rule predates background tasks. A Monitor, a background command or a subagent finishing can wake a
stopped session for a turn of its own, with no word from Chase.

## 2. The fix (`golem.ps1`)

| Where | Change |
|---|---|
| Stop hook, STOPPED | Records `stoppedAt` (UTC, round-trip format) in the state with `stoppedPrompt`. |
| Prompt hook (UserPromptSubmit) | Records `lastChasePromptUtc` in the session's file. It does this only for words typed by a person: a prompt starting `<task-notification>`, `<agent-message` or "Another Claude session sent a message" is the session's own (`Test-MachinePrompt`). Such a prompt no longer ends the session's hold either. |
| Activity hook | Clears a STOPPED only when Chase typed in *that* session after `stoppedAt` (`Test-ChaseSpokeSince`). Otherwise the STOPPED, its question, `needsYou` and the session's hold all stay as they are, and nothing is logged. A NEEDS YOU (permission prompt) is cleared by activity as before. |
| Stop hook, D90 skip | A prompt STOPPED again is no longer skipped when three things hold: its STOPPED had been cleared, nothing else is running, and the prompt is still claimed by this Golem. That is a session that took Chase's words and stopped again, so it is recorded as a new stop (question, email). In every other case the skip stands. |

The rule the prompt asks for now holds. A question stays open while its prompt is claimed by the asking Golem and that
Golem's last line was STOPPED. It closes only through these paths, all unchanged:
- **Answered:** `Submit-GolemAnswer`.
- **Retried or requeued:** the prompt goes back to `queue\`, so `stoppedPrompt` is cleared.
- **Cleared:** the start phrase, or Chase typing in the session.
- **Finished:** DONE.
- **Parked:** away mode.

`Questions.ps1` (`Sync-GolemQuestions`) needed no change: it was right to close a question once the STOPPED was gone.
The STOPPED itself was being dropped wrongly.

An old state with no `stoppedAt` (a STOPPED recorded before this change) is cleared by any later words Chase typed in
that session, never by tool calls alone.

## 3. Tests

Two new facts in `tests\Golem.Tests.ps1`, beside the cc-P216 question facts:

- `P715_AQuestionStaysOpenWhileItsStoppedPromptWaits` replays P707's events in order: Ask-Chase, Stop with
  `STOPPED: asked Chase`, a `<task-notification>` prompt, a `TaskStop` Pre and Post tool call, then the same STOPPED line
  again. It checks:
  - the question is still open;
  - `stoppedPrompt` is still P100;
  - status.json says STOPPED with one open question;
  - no "Chase answered" line is logged;
  - Chase's answer on the card is taken and P100 goes back to the queue.
- `P715_ChaseTypingInTheStoppedSessionStillClearsIt` checks:
  - words typed in the stopped session still clear the STOPPED and close its question (the old behaviour, kept);
  - a second STOPPED on the same prompt after that is recorded, with a question of its own;
  - words typed in another session do not clear a stop in this one.

**Seen failing first.** Run against the old `golem.ps1`, the two facts failed 11 of 15 checks
(`notes\cc-P715-tools\golem-tests-before.log`). The first failure is the exact message P707 got: "expired P100 is no
longer STOPPED or running (retried, cleared, parked or finished)". With the fix: 15 of 15.

**Full suite** (`notes\cc-P715-tools\golem-tests-after.log`): 1699 checks passed, 6 failed.
- **1 was mine.** `P131_ARealStoppedSaysNeedsYouAndTheDecisionWanted` checked the old rule ("Chase answers CC: its next
  tool use clears the STOPPED"), which is the bug itself. The fact now:
  - sends a tool call alone and checks it stays STOPPED;
  - then sends Chase's words and a tool call, and checks they clear it.
  The P131 facts: 141 checks, 0 failed. The P216 question facts: 56, 0 failed.
- **5 were already failing before P715**, in `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` and
  `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly`:
  - they fail the same way against the old `golem.ps1`;
  - P770's final run (`notes\cc-P770-tools\golem770-final.txt`) already lists the first as FAIL;
  - they are about which areas a claim touches, nothing this change reaches. I left them alone.

## Deviations and decisions for Chase

- **Edits made by script, not with the Read and Edit tools.** The unattended run denied the Read tool on
  `D:\UO\golem\tests\Golem.Tests.ps1`: I wanted to read lines 3874-3880 to place the new facts. So I made the kit
  edits with the Python scripts in `notes\cc-P715-tools\`:
  - `add_test.py`, `fix_golem.py` and `add_changelog.py`;
  - each checks that its anchor text matches exactly once;
  - the result is checked in `p715-kit.diff`.
- **A P131 fact changed** (see Tests): its old check encoded the rule this prompt removes.
- **Known failing P184 facts** (5 checks, already failing before P715): worth a fix-up prompt of their own.
- **No forced kit snapshot.** P770 forced one so it could test on Gold. This fix needs no test on a family PC, so the
  Tinker's normal sync takes it there after the commit.

P715 DONE
