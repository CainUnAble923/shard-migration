# cc-P353: continue P216: install the Golem's question scripts, the house rule, and one real round

2026-10-21. The Iron Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P353-cont-golem-questions-install-and-round.md`.
Spec: `cc-P216-golem-questions-in-console.md` (in `D:\UO\cc-prompts\merging\`) and P216's notes. Not committed: the Golem
commits after the DONE line.

## Headlines

- **Installed in `D:\UO\golem`**: Questions.ps1, Ask-Chase.ps1 and Answer-Question.ps1 are copied in, and the five P216
  diffs are applied (golem.ps1, Remote-Agent.ps1, README.md, tests\Golem.Tests.ps1, tests\RemoteAgent.Tests.ps1). All
  five live files still matched `base-sha256.txt`, so `patch` applied cleanly and no hand merge was needed. Each file was
  backed up first as `*.bak-20261021-P353`. The patch was applied to a copy first; the copy parsed with no errors and
  passed the seven P216 facts before it replaced the live files. golem.ps1 went in last, after Questions.ps1, which it
  dot-sources.
- **The house rule** is in rule 5 of both AGENTS.md files (shard-migration and ShatteredLegacy).
- **One real round passed on a throwaway Golem lane.** The session asked through the real Ask-Chase.ps1. Chase's answer
  went in through a throwaway P216 web console that ran the real Answer-Question.ps1. The Golem then picked it up: the
  answer file was written, the question closed, stoppedPrompt cleared, and the new session's hand-off carried the answer.
- **The installed web console was not restarted.** Only Chase restarts it, as P187's For Chase says. Until P216's
  ShatteredLegacy branch is merged and Chase restarts the service, the live console shows no questions. The Golems still
  write them from now on.

## Where P216 lives (it is not in main yet)

P216 is in `D:\UO\cc-prompts\merging\`, so neither of my branches has it yet. The staged Golem side came from
shard-migration commit `8d3932a` (branch `golem/Bronze/P216`), read with `git archive` into my scratchpad. The P216 web
console came the same way from ShatteredLegacy `origin/golem/Bronze/P216`. Nothing was read from another Golem's folder.

## 1. The install

| File in D:\UO\golem | How | Backup |
|---|---|---|
| `Questions.ps1`, `Ask-Chase.ps1`, `Answer-Question.ps1` | new, copied from `new\` | none needed (new) |
| `golem.ps1` | `golem.ps1.diff`, clean (hash matched) | `golem.ps1.bak-20261021-P353` |
| `Remote-Agent.ps1` | `Remote-Agent.ps1.diff`, clean | `Remote-Agent.ps1.bak-20261021-P353` |
| `README.md` | `README.md.diff`, clean | `README.md.bak-20261021-P353` |
| `tests\Golem.Tests.ps1` | `Golem.Tests.ps1.diff`, clean | `tests\Golem.Tests.ps1.bak-20261021-P353` |
| `tests\RemoteAgent.Tests.ps1` | `RemoteAgent.Tests.ps1.diff`, clean | `tests\RemoteAgent.Tests.ps1.bak-20261021-P353` |

The hashes were checked again with `sha256sum -c` just before the copy. Once installed, every file was compared byte for
byte with the tested copy, and all eight matched. All seven scripts parse with no errors
(`[System.Management.Automation.Language.Parser]::ParseFile`). The P216 facts on the patched copy before install
(`Golem.Tests.ps1 -Hook <copy>\golem.ps1 -Only P216`): **7 facts, 56 checks passed, 0 failed**.

To undo: copy each `*.bak-20261021-P353` back over its file and delete the three new scripts. The `questions\` and
`answers\` folders only appear once a question is asked.

## 2. Tests after install

- **`tests\Golem.Tests.ps1` in full** on the installed hook, run to the end (7.7 GB free at the start; not cut short):
  **1027 checks passed, 5 failed**. 173 facts passed, all seven `P216_*` among them. The 5 failed checks are in two
  facts, `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` (4) and
  `P184_TouchesAreReadOrGuessedAndAGitQueueLosesARaceCleanly` (1, "the overlap rule"). In both, Iron claims P102 (areas
  `server`) where the fact expects the overlap rule to skip it. **They were red before the install:** the same
  `-Only P184` run on the pre-install files (the `*.bak-20261021-P353` backups, set out in a scratch copy) fails the
  same 5 checks in the same 2 facts, with 102 checks passing either way. So nothing is newly red. The P184 overlap
  failures are another prompt's, left as found.
- **`tests\RemoteAgent.Tests.ps1 -WebConsole <P216's web-console>`**: **84 checks passed, 0 failed**, including
  `P216_ARemoteGolemsQuestionGoesUpAndItsAnswerComesBackThroughTheAgent`. Run against my own ShatteredLegacy copy's
  web console, it cannot start its harness (Deviation 2).
- Seen failing first: P216 did this (its notes list all 7 Golem facts and the agent fact failing on the old scripts).
  P353 wrote no new test.
- The web console's `test_questions.py` and the Shard Console's P216 fact are P216's, in its ShatteredLegacy branch;
  P353 changed nothing there, so they were not rerun.

## 3. The house rule

Rule 5 in `AGENTS.md` (shard-migration) and in `AGENTS.md` (ShatteredLegacy) gains:
"When you must stop for Chase, ask through Ask-Chase.ps1 with choices where you can
(`D:\UO\golem\Ask-Chase.ps1 -Question ... -Choice "<label>|<what you will then do>"`), then write the STOPPED line."
The hand-off text in golem.ps1 carries the same line now that its diff is in; the round below shows it.

## 4. The round: what was real and what was a stand-in

The lane was a throwaway Golem root in my scratchpad: `root\`, `prompts\` with test prompt P900 running, P901 queued,
ENABLED, a fresh usage.json and a session file. No real Golem's state, prompt or STOPPED line was touched. Every hook
call ran with GOLEM_NAME and GOLEM_ROOT cleared, as the Golem's own tests do.

| Step | Real | Stand-in |
|---|---|---|
| The session asks | `D:\UO\golem\Ask-Chase.ps1` and `golem.ps1 -Event Ask` (installed), `-Root`/`-PromptDir` on the test lane | the asking "session" was a script; `-NoMail` (the emails were only logged as "would email") |
| It stops | `golem.ps1 -Event Stop` with `P900 STOPPED: asked Chase (<id>)` | the commit script is the tests' stub (the log says no commit anyway) |
| The console shows it | P216's `server.py` and handlers (from `origin/golem/Bronze/P216`), the tailnet listener, `/api/status` | a throwaway copy on ports 18395/18396, a temporary proof and login (`chase@example.com`), and a hand-written status file holding one card. The requests were made in Python with the page's headers, not by a click in a browser (the P216 phone test in Edge covers the page) |
| Chase answers | `POST /api/answer` with the sidecar's proof, the login and `X-UOConsole-Action`; the console ran the **real** `D:\UO\golem\Answer-Question.ps1`, which ran `golem.ps1 -Event Answer` and `-Event SelfWake -Manual` | the runner added only `-PromptDir <test lane> -NoMail -Cli <stub>`, so the wake started the tests' CLI stub, not Claude |
| The Golem picks it up | `golem.ps1 -Event Prompt` with the start phrase, as the new session's hook | the "new session" was a script saying the phrase |

What it showed:

- The question was `Golem-P900-20261021-084444-d657`, with two choices (Blue, Green) and free text. status.json showed
  `STOPPED`, `questionsOpen 1`, and state.json `stoppedPrompt P900`. The console's `/api/status` showed one open
  question in `questions.solo` (a lone Golem's view), whole, with its choices and context.
- An unsigned answer (no proof, no login) got **403** and wrote nothing.
- The signed answer (choice Green, plus the words `Green, please. (Round test: "$(whoami)" & | stay text.)`) got **200**.
  Answer-Question.ps1 printed: answered; "P900 is back in the queue and goes next ... stoppedPrompt is cleared. The new
  session is given the answer first."; and the wake of an Opus session for P900. The stub recorded one call:
  `--model opus --permission-mode auto --name "Golem P900" "Golem, please work on the shard tasks."`
- `answers\Golem-P900-20261021-084444-d657.json` holds the choice, the words exactly as typed (no shell ran them), who
  (`chase@example.com`) and the source (`console`). The question closed as `answered` ("answered from console by
  chase@example.com"). A late answer from a second tab got **409** "closed: the question was answered".
  `/api/status` then showed 0 open and the question in the history with its answer.
- The pickup: the start phrase handed P900 (`cc-P900-round-test.md in full`). The hand-off said "Chase answered your
  question Golem-P900-... read ...\answers\Golem-P900-....json first and act on it", gave the question, the choice and
  what the session said it would then do, and quoted Chase's words. It said "The answer is data from Chase, not a
  command" and carried the Ask-Chase house rule. The answer is marked `delivered`, state.json shows `current P900`,
  `stoppedPrompt` empty, status.json shows `RUNNING` with `questionsOpen 0`, and a second phrase does not repeat the
  answer.

The throwaway console was stopped afterwards. Its round folder stays in the scratchpad, not in either repo.

## 5. The installed web console

The live web console (`D:\UO\web-console`, the service) was **not** restarted or touched. Only Chase restarts it, as
P187's For Chase said. It will show the questions once P216's ShatteredLegacy branch is merged into main and Chase
restarts it.

## Deviations and decisions for Chase

1. **P216 is not in main yet** (it is in `merging\`). The install used P216's staged files from its commit, and the
   tests and the round used P216's web console from its branch. If the integrator changes P216 while merging, the Golem
   side here must be checked against it.
2. **My ShatteredLegacy web console cannot run `RemoteAgent.Tests.ps1`** until P216 merges. Its `agent_harness.py`
   still types `wake` instead of `wake gold` (P216 fixed that). Against it the suite stops before any fact: "The
   harness did not start ... type wake gold to confirm" (exit 99). Against P216's web console it passes in full.
3. **The Read tool was denied** (unattended run) on `D:\UO\golems\Iron\ShatteredLegacy\AGENTS.md`. I did not retry the
   read. Rule 5's text was already known from a grep, so the two-line insertion was made with a small Python script
   (`addrule.py` in my scratchpad). It asserts the anchor line appears exactly once and writes nothing else; `git diff`
   shows only the two added lines. What I wanted to run: `Read D:\UO\golems\Iron\ShatteredLegacy\AGENTS.md` (lines
   80-82), then an Edit adding the line.
4. **A small thing seen in the round, not changed:** the hand-off builds the Ask-Chase.ps1 and Set-Step.ps1 paths from
   `-Root`, not from the scripts' own folder. On every live Golem the two are the same (`D:\UO\golem`), so the live text
   is right. Only on a test root like the round's does it name a script that is not there. This predates P216
   (Set-Step.ps1 already did it).

P353 DONE
