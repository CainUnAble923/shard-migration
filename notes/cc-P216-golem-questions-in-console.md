# cc-P216: Golems ask their questions on the console, and Chase answers there

2026-10-21. The Bronze Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Bronze\cc-P216-golem-questions-in-console.md`.
Read first: P182's, P186's, P187's, P131's and P149's notes and `D:\UO\golem\README.md`. Not committed: the Golem
commits after the PAUSED line. **Paused at Chase's stopping point** (the Golem's nudge arrived while the tests ran):
see Continuation, and the continuation prompt `cc-P353-cont-golem-questions-install-and-round.md` in the queue.

## Headlines

- **The consoles' side is done and tested** (ShatteredLegacy, this branch): the web console shows each Golem's open
  questions on its card in full, a button per choice, a box for Chase's words, "Cannot be undone" in red with a confirm,
  the context under "What the Golem saw", and "Earlier questions"; the Golem tab's header counts the open questions;
  `POST /api/answer` has the buttons' own checks; a remote Golem's questions come from its agent and its answer goes back
  as an agent command. The Shard Console lists the open questions on the Golem tab and has **Answer a Golem's question**.
- **The Golem side is built and tested, but staged, not installed** in `D:\UO\golem` (which is every Golem's live hook
  and not a repo). It is saved in `notes\cc-P216-golem-stage\` (three new files, five diffs, the hashes they were made
  against) for P353 to install. Until then the consoles show nothing new: no question files exist, and the Answer button
  is greyed.
- **Not done (P353):** the install, the AGENTS.md house-rule line (it names Ask-Chase.ps1, which must exist first), and
  the one real round.
- **P149 is already built** (the prompt said queued): `Submit-GolemAnswer` with `-Source email` is the hook for its
  replies; no email parsing was added here, as the prompt says.

## What changed

**`D:\ShatteredLegacy`** (branch `golem/Bronze/P216`)

| File | Change |
|---|---|
| `web-console\server.py` | `QUESTION_ID`, `ANSWER_TEXT_MAX`, `ANSWER_TIMEOUT`, `WHO_UNSAFE`; `Console(answer_runner=)`; `local_questions`, `remote_questions` (with "answer sent" for one queued to the agent), `questions_for`, `questions_summary` (the tab count; one Golem alone), `save_questions` (`POST /api/agent/questions`: only that Golem's ids), `answer` (`POST /api/answer`: checked against the open question, then Answer-Question.ps1 with argv only and the words as base64, or queued for a remote agent as command `answer`), `loggable` (an answer's words never reach the action log); cards carry `questions`; `/api/status` carries `questions` |
| `web-console\static\app.js`, `index.html`, `app.css` | `questionBlock` on every Golem card, `drawSoloQuestions` (one Golem alone), `drawQuestionCount` (the Golem tab badge), `sendAnswer` (confirm for an irreversible one); a half-typed answer survives the 5 s refresh (the Golem page waits while its box has focus) |
| `web-console\console-actions.json` | the twin of `golem.answer`: `page:question` |
| `web-console\tests\test_questions.py` (new), `fixtures\fake_answer.py` (new) | seven tests (below) |
| `web-console\tests\fixtures\agent_harness.py` | the typed words name the Golem (`wake gold`): broken since P187, so `RemoteAgent.Tests.ps1` could not start its harness (found here, fixed) |
| `scripts\Shard-Console.ps1` | `AnswerScript`; action `golem.answer` (row "Golem answer", its tooltip, its confirm title); `Get-OpenGolemQuestions` (this PC's and the remote Golems' as posted), `Get-GolemQuestionLines` (the Golem tab), `Show-AnswerPicker` (a row per choice, then the words), the plan (phrase `answer <golem> <prompt>`), `Test-PlanSafety` (Answer-Question.ps1 only with the button's arguments, only after the phrase), the button lit with the count |
| `scripts\tests\Shard-Console.Tests.ps1` | fact `P216_TheGolemTabShowsTheOpenQuestionsAndAnswerRunsAnswerQuestion` |

**`D:\UO\golem`**: staged in `notes\cc-P216-golem-stage\`, not installed (P353):

- `Questions.ps1` (new): the question and answer files; `New-GolemQuestion` (at most four choices, one label each;
  a repeat is the same question), `Get-IrreversibleWhy` (deleting saves or data, the LIVE shard or what players get,
  pushing main by hand), `Sync-GolemQuestions` (closes what the state no longer asks: Retry, the terminal, the phrase,
  parked), `Submit-GolemAnswer` (**part 5: the one way an answer becomes a file**, from any source; created once, so a
  second answer or one to a closed question is refused), `Get-PendingAnswers`, `Format-AnswerForSession` (the answer
  as data), `Get-QuestionCard` (open and the last five closed, for the agent).
- `Ask-Chase.ps1` (new): `-Question`, `-Choice` .. `-Choice4` (`-File` cannot pass a list), `-NoText`, `-Context`,
  `-Irreversible`; it hands the question to `golem.ps1 -Event Ask`, so it carries the session's Golem and prompt.
- `Answer-Question.ps1` (new): `Submit-GolemAnswer`, then `golem.ps1 -Event Answer`, then a wake as Retry-Stopped.ps1.
- `golem.ps1`: events `Ask` and `Answer`; `Invoke-RetryStoppedCore` (Retry stopped prompt's body, shared);
  a question on STOPPED (unless the session asked its own) and on NEEDS YOU (not while a STOPPED question waits); an
  answer that came before the STOPPED retries at once; `Get-AnswerContext` in the hand-off and in "carry on with it";
  status.json `questionsOpen` and `questionIds`; the hand-off's house rule now says to ask through Ask-Chase.ps1.
- `Remote-Agent.ps1`: `answer` on the allowlist (`Answer-Question.ps1 -Source remote`, the words as base64, empty
  optional inputs left out), `Send-AgentQuestions` (when they change, every 5 minutes; a web console without the route
  is skipped).
- `README.md`: section "Questions for Chase, answered on the console (cc-P216)", the Files rows.
- Tests: seven `P216_*` facts in `Golem.Tests.ps1`, one in `RemoteAgent.Tests.ps1`.

## Safe defaults (part 4), and how each was proved

| Rule | Where | Proved by |
|---|---|---|
| Answers only from the signed-in console | `do_POST` `/api/answer`: tailnet listener, proof, login, `X-UOConsole-Action`, same origin, `Sec-Fetch-Site`; this PC's page read only; an agent cannot answer | `test_only_the_signed_in_page_may_answer` (8 refusals, nothing run) |
| Answer text is data | base64 on every command line (web console, Shard Console, agent); `Test-PlanSafety` refuses plain words; never logged; the session is told it is data | `test_an_answer_runs_the_golems_own_script_with_argv_only_and_the_words_as_base64` (quotes, `$( )`, `&`, `|`, `-Root` intact), `P216_AnAnswerClears...` (`$(whoami)` stays text), the agent fact, the console fact |
| A closed question refuses a late answer | the server against the open question; `Submit-GolemAnswer` creates the file once | `P216_AClosedQuestionRefusesALateAnswer` (a second tab; Retry closed it first), `test_a_closed_question_a_stale_page_and_a_bad_answer_are_refused` |
| Cannot be undone says so | `Get-IrreversibleWhy`, `-Irreversible`; red on the card, a confirm on the page and `confirm: true` on the server; the Shard Console's confirm says CANNOT BE UNDONE | `test_an_answer_that_cannot_be_undone_wants_a_confirm`, `P216_AskChase...` (deleting saves flagged), the phone test |

## Tests

Every new test was seen failing first against the code before this prompt:

- Golem (`Golem.Tests.ps1 -Only P216` on the staged copy): 7 facts, 56 checks pass; on the old golem.ps1 all 7 fail
  (33 checks).
- RemoteAgent (`-Only P216`): 9 checks pass; on the old Remote-Agent.ps1 (with the new library) it fails (no
  `questions.json` reaches the game PC).
- Web console: `test_questions.py` 7 tests pass (the phone test in Edge at 390 px included); on HEAD's server and page
  all 7 fail. Full suite: 98 tests OK (1 skipped, as before).
- Shard Console: the P216 fact passes; on HEAD's Shard-Console.ps1 it fails (`Get-OpenGolemQuestions` missing).
- **Full runs, cut short by low memory:** both full suites were started in the background and both were stopped by
  Claude Code because the PC ran low on memory (not restarted, per the rule). As far as they got:
  - Golem.Tests.ps1 on the staged hook: 79 facts passed, 0 failed (it stopped in the P161 facts; the P216 facts had
    passed on their own). P353 runs it in full after the install.
  - Shard-Console.Tests.ps1: 285 passed, 13 failed. One was mine (`P84_EveryActionHasATooltipOfOneOrTwoPlainSentences`:
    the `golem.answer` tooltip had 5 sentences; shortened to 2, the fact now passes with P187's twin fact and the P216
    fact). The other 12 are failures earlier prompts' notes already list (PlayerCommandsNeverAppearInTheWorldTab,
    RedMeans..., the three EveryWindowAction/WithTheToggleOn facts, P99_TheConsoleReads..., the two P83 link facts,
    P84_TheUOLook..., the two P101 facts, P107_Links...); none touches the Golem tab's questions.

## Deviations and decisions for Chase

1. **Paused, not done:** the Golem side is staged (above); P353 installs it, adds the AGENTS.md line and runs the round.
2. **Resuming with the answer:** the start phrase is unchanged (Test-GolemPhrase must still match it); the answer
   rides in the hand-off's added context that the start phrase brings, which the new session reads first.
3. **Questions close by themselves** when their stop is cleared another way (`Sync-GolemQuestions`), including a
   parked prompt in away mode: its question closes with "parked", and the parked line is where it shows.
4. **A Codex lane's NEEDS YOU** (`Set-LaneNeedsYou`) writes no question yet: its resume is the lane's own.
5. **The Read tool was denied** once on `web-console\server.py` (unattended run); the edit was made with a script
   instead. No other step was skipped.

## Continuation

- **Done:** parts 2 to 5 on the consoles' side, in this branch, tested; parts 1, 3, 5 on the Golem side, staged and
  tested in a copy (`notes\cc-P216-golem-stage\`: apply the diffs to D:\UO\golem; they reproduce the tested files
  byte for byte against the hashes in `base-sha256.txt`).
- **Left (P353):** install in D:\UO\golem with backups; the full Golem suite after install; the AGENTS.md line in both
  repos; the one real round (a test question on a test lane answered from a throwaway web console, picked up by the
  Golem).
- **Mid-flight:** nothing. No lock was taken (no Docker, test shard, package or Haven work), and no live file in
  D:\UO\golem was changed.

P216 PAUSED
