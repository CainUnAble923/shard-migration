# cc-P182: Web console phase 2: the Golem's buttons, the identity gap closed

2026-10-19. Opus. Prompt: `D:\UO\cc-prompts\cc-P182-cont-web-console-phase2.md` (handed by the Golem). Builds on P155
(`notes\cc-P155-web-console-phase1-status.md`). Not committed: the Golem commits after DONE. Both repos were clean at
the start apart from the overnight bot's transcript.

## Headlines

- **The Golem page has its buttons:** Wake, Turn on, Poke, Rest, Wrap up after this task (or Cancel wrap up), Find a
  stopping point (or Cancel stopping point), Long run, End long run, Night shift on or off, Run next (pick a queued
  prompt), Clear Run next, Retry stopped prompt (only while one is STOPPED), and Away mode on/off, greyed: away mode is
  P149's and is not built yet (Deviation 3).
- **Each runs the Shard Console's own code.** A button is one entry in `web-console\golem-actions.json`, which names
  the console action it is. The server starts `scripts\Invoke-WebConsoleAction.ps1`. That script dot-sources the
  console, reads the facts with `Get-ActionFacts` and builds the plan with `Get-ActionPlan` (through `Get-WebActionPlan`,
  which only maps the page's inputs to the console's boxes). It then runs the plan with `Test-PlanSafety` and
  `Invoke-Plan`. A Golem script that the console runs "in a window of its own" runs in that process instead, so its
  output streams back. Nothing re-implements a Golem action.
- **The typed word is checked three times:** by the page (Run stays dark until it matches), by `server.py`, and by the
  console's plan in the runner. Case does not matter, because phones capitalize. The console's own phrase still goes on
  to `Invoke-Plan`. Run next takes the prompt number, Retry takes the stopped prompt's number, and the rest take the
  console's phrase (`wake the golem`, `find a stopping point`, ...) or a short word (`poke`, `rest`, `cancel`).
- **One at a time.** A second press while one runs is refused (409) with what is running and since when. Output is
  polled once a second. The result line is the console's own (`golem.resume: done.`, its refusal, or `FAILED at step n`).
- **The action log:** `D:\UO\web-console\actions.log`, one JSON line per press (time, who, button, console action, the
  checked inputs, the result line, the exit code). It never holds a header, the typed word, the proof or a token. The
  presses show on the Timeline (kind `web`) and under Logs ("The web console's action log").
- **P155's identity gap is closed.** A new container, `uoconsole-proof` (`web-console\tailscale\proof_proxy.py`, standard
  library, image `python:3.12.7-alpine3.20`), sits inside the uoconsole node's own network namespace between Tailscale
  Serve and the console. It adds `X-UOConsole-Proof`: a secret in `D:\UO\web-console\proof.key` that only it and the
  console hold. The tailnet listener refuses every request without it, then checks Serve's login as before (only
  Chase's, from `settings.json` or this PC's own login, never hard coded). A container on the game PC that reaches
  `127.0.0.1:8096` directly can forge the login, but not the proof.
- **This PC's own page (`127.0.0.1:8095`) stays read only.** It shows the buttons greyed with the uoconsole address,
  because any container can reach that port too (Deviation 4).
- **Mobile first:** two big buttons a row (64 px tall), a bottom sheet for the inputs and the word (under the thumb,
  autocapitalize off, Run and Cancel 56 px), and the output under the controls. A phone test at a true 390 px drives it
  end to end.
- **The art:** P152's art had landed in 19 of the 20 slots (all but the spinner). The page now uses every slot: the
  Golem figure by its state, the tile icons, both runes, the header band, the stone and page textures, the crystals on
  tiles and lights, and the spinner while a button runs. A strip in `art.json` animates there too. **15 new button
  slots** (`btn-*.png`) are in the spec, and their request, `web-console-golem-buttons`, is filed through P152's helper.
  P152 had already run, so it was filed rather than added to P152's list.
- **The Shard Console has the three new actions too:** Poke the Golem, Run next (the picked queue row) and Retry stopped
  prompt, in a row of their own on the Golem tab. The Golem has three new small scripts and two new events.
- **The installer fix (step 4):** docker's progress shows as plain text and success is the exit code only
  (`Invoke-Docker`). The installer now also stops a running web console first, so an update takes effect.
- **No task-list tool** in this session (as in P154 and P155): progress went to the chat only.

## What changed

D:\ShatteredLegacy:

| File | Change |
|---|---|
| `web-console\golem-actions.json` (new) | The 17 buttons: key, label, console action, word (`#prompt`, `#stopped` or a fixed word), inputs, `when` (which half of a pair applies), `disabled` (away mode), help, art slot |
| `web-console\server.py` | `LOCAL_READ_ONLY` :49, `INPUT_RULES` :60 (what each input may be; argv only, never a shell); `Console` takes `runner` (default the runner script); `proof()` :126; `buttons()`, `check_request` :156 (the word and inputs), `start_action` :192 (one at a time), `_run_job` :211 (stream, redact, 600 s limit), `job_view` :240, `log_action` :249, `web_actions` :263; the timeline gets the presses; `art_frames` :435; `/api/status` adds `actions` (buttons, canAct, job) and `artFrames` :563; `GET /api/action` :566; `do_POST` :584 (tailnet only, the `X-UOConsole-Action` header, same origin, `Sec-Fetch-Site`, JSON, 4 KB) |
| `web-console\panels.py` | `PROOF_HEADER` :25; `decide(listener, headers, allowed, proof)` :30, which checks the proof first (`hmac.compare_digest`), then the login; `timeline(..., web_actions)` :192 |
| `web-console\tailscale\proof_proxy.py` (new) | The forwarder: `make_server` :28 (drops any proof the caller sent, sets its own, passes the rest and the answer); `bind_refusal` :75 (never 127.0.0.1, where tailscaled hands direct tailnet connections; never off the loopback); `main` :82 (refuses a proof under 32 characters) |
| `web-console\tailscale\serve.json` | Serve proxies to `http://127.0.0.2:8097` (the forwarder), Funnel still false |
| `web-console\tailscale\docker-compose.yml` | The `proof` service (`uoconsole-proof`, `network_mode: service:tailscale`, the key mounted read only, no ports) |
| `web-console\Install-WebConsole.ps1` | `Invoke-Docker` :36 (step 4); `Stop-WebConsoleServer` :51; makes `proof.key` once (32 random bytes as hex, never printed); `up -d --force-recreate` :121 (the node's state volume is kept); passes `UOCONSOLE_PROOF` |
| `web-console\static\app.js`, `index.html`, `app.css` | `artNode` :39 (an image, or a stepping strip, or null for the stand-in); `applies` :222; `drawControls` :238; `openSheet` :277; the job poll :378; the Controls card, the job card and the sheet; every art slot; the stand-ins (a drawn Golem, a CSS spinner, a letter in a ring) |
| `scripts\Invoke-WebConsoleAction.ps1` (new) | The runner (56 lines): button -> `Get-ActionFacts` -> `Get-WebActionPlan` -> `Format-Plan` -> `Invoke-Plan` with `$script:WindowStepsInline`; lines marked with their colour (`SHARD_CONSOLE_PANE`); exit 0 done, 1 failed, 2 refused, 3 cancelled; `-DryRun` |
| `scripts\Shard-Console.ps1` | Config `PokeScript`, `RunNextScript`, `RetryScript`, `RunNextFile` :242; `Get-AutopilotQueue -RunNext` :4103 (the pick first :4110); the view's `RunNext`; the facts read `RUN-NEXT` :6498; the status file's `golem.runNext` :9046; `Test-PlanSafety`: Set-RunNext only with `-Prompt P<nn>` or `-Cancel`, Retry-Stopped only with `-Prompt P<nn>` :3328; `Get-WebActionPlan` :5029; plans `golem.poke` :5265, `golem.runnext` :5271 (shows the new order before the confirm), `golem.retry` :5291; the actions :1223 and tooltips :1818; the Golem tab row :11235, Retry lit only while STOPPED :8931, Run next takes the picked row :10112; `Invoke-Plan`'s window step runs here when `$script:WindowStepsInline` :7171; `-Action list` says so |
| `scripts\tests\Shard-Console.Tests.ps1` | Six `P182_*` facts (:7380-:7480) |
| `web-console\tests\test_actions.py` (new), `tests\fixtures\fake_runner.py` (new), `tests\test_web_console.py` | 18 new tests; P155's identity tests now carry the proof (the gap they accepted is closed) |
| `docker\haven\services.json` | `uoconsole-proof` (34 services); `web-console`'s name, data and note; the dashboard regenerated (`-Check` clean, 37 tiles, no tile change) |
| `scripts\console-art\README.md` | The web console uses every slot, plus the 15 button slots |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.19.2`, five `### Staff` lines; 2026.10.19.2 (today's 2026.10.19 was already committed) |

D:\UO\shard-migration: this file; `notes\console-art-spec.md` (a section and table for the button slots, written so
P152's importer still reads exactly the 20 rows above it); `notes\haven-runbook.md` (the console's buttons and proof, the
`uoconsole-proof` section, a Changed-on line); `testing\playtest-steps.json` and `testing\bot-triage.md` (P182-1 to 6).

D:\UO\golem (outside git; backups `golem.ps1.bak-20261019-p182`, `README.md.bak-20261019-p182`,
`tests\Golem.Tests.ps1.bak-20261019-p182`):

| File | Change |
|---|---|
| `golem.ps1` | `-Prompt`; `$RunNextFile` (`RUN-NEXT`); `Sort-Queue` :321 puts the pick first (so every order agrees: the hand-off, the status queue, the pace rule's independent next); `Find-PromptFile` :333; the hand-off removes the pick once it hands it :1634; `-Event RunNext` :1859 (`-Prompt P<nn>` or `-Cancel`; only a file in `queue\`); `-Event RetryStopped` :1881 (moves the STOPPED prompt from `cc-prompts\` back to `queue\`, clears `stoppedPrompt`, steps `lastHandled` back so its DONE is committed, picks it to go next, releases the session kept open for the STOPPED) |
| `Poke-Golem.ps1` (new) | Runs `-Event Watch` now and prints the state |
| `Set-RunNext.ps1` (new) | `-Event RunNext` |
| `Retry-Stopped.ps1` (new) | `-Event RetryStopped`, then `-Event SelfWake -Manual` with no model (the next prompt's, now this one) |
| `README.md` | The two events, the three scripts, `RUN-NEXT` |
| `tests\Golem.Tests.ps1` | Four `P182_*` facts (:1409-:1451) |

The swap of the live `golem.ps1` was a copy to `golem.ps1.new` and a rename on the same volume, after the full Golem
suite passed on the new copy (446 checks, 0 failed), because the hooks of running sessions read it.

Outside both repos: `D:\UO\art\requests\web-console-golem-buttons.json` (status new). Nothing was installed or
restarted: the running web console, its task and the sidecar are as Chase left them at 06:49.

## Tests

Every new test was seen failing first. At its first run each was red, because the code did not exist yet. Then a
mutation pass broke each guarded behaviour, one at a time, and ran the test that should catch it. It expected red,
then restored the file and checked its hash (`scratchpad\mutate.py`). **25 breaks, 25 caught.** The first pass caught
23. The two that stayed green showed weak tests, and both tests were strengthened:

| Break | Caught by |
|---|---|
| the proof not compared; no proof configured lets in | `Proof.test_the_tailnet_needs_the_sidecars_proof`, `test_no_proof_configured_refuses_the_tailnet` |
| the local listener may act; no `X-UOConsole-Action`; any origin; a form post | `LiveActions.test_only_chase_through_the_sidecar_may_act`, `test_cross_site_requests_are_refused` |
| the word not checked (server); the word not checked (console) | `test_the_word_is_checked_on_the_server`; `P182_AWebButtonCallsTheConsolesOwnPlanAndChecksTheWordOnTheServer` |
| two at once | `test_one_action_at_a_time` |
| inputs not passed to the runner | `test_each_button_calls_the_consoles_runner_with_its_inputs` (the fake runner records every call) |
| any model accepted | `test_bad_inputs_are_refused` |
| request headers in the log; the presses not on the Timeline | `test_the_action_log_never_holds_a_header_or_token` |
| lines kept unredacted (first pass: green, because redaction on the way out hid it; the test now also checks the job as kept) | `test_output_streams_back_and_the_result_is_the_consoles_line` |
| the local page told it may act | `test_the_page_is_told_the_buttons_and_whether_it_may_act` |
| a forged proof passed on | `ProofForwarder.test_it_sets_the_proof_and_passes_the_request_and_the_answer` |
| the forwarder binds 127.0.0.1 (first pass: green, because the test's empty proof file exited first; the check is now `bind_refusal` and tested alone) | `test_it_refuses_to_start_on_the_loopback_netstack_forwards_to` |
| Run lit without the word; small buttons | `PhoneControls.test_wake_poke_and_read_the_result_one_handed` |
| Run next with any argument; the pick not first (console); a stale page wraps up twice | `P182_PokeRunNextAndRetryRunTheGolemsOwnScripts`, `P182_TheQueueShowsTheRunNextPickFirst`, `P182_AWebButton...` |
| the pick never cleared; `lastHandled` kept on retry; the pick not first (Golem) | `P182_RunNextPutsThePickedPromptFirstAndItsHandOffClearsIt`, `P182_RetryStoppedPutsTheStoppedPromptBackFirstAndClearsIt` |

Also new, red at first for the missing code: `P182_EveryWebButtonIsAConsoleActionAndItsWordIsTheConsolesPhrase` (each
button's word is the console's `Get-ConfirmPhrase`); `P182_WindowStepsRunInThisProcessForTheWebConsole`. Its first red
run took the old path and opened one PowerShell window, which I closed. `P182_TheGolemTabHasPokeRunNextAndRetry`.
`P182_RunNextRefusesAPromptThatIsNotQueuedAndCancelClearsThePick`, `P182_RetryStoppedRefusesWithNothingStoppedOrAnotherPrompt`.
`test_the_real_runner_is_the_consoles_script`, `test_the_sidecar_config_serves_through_the_forwarder_only`.

The forwarder in a real container: a throwaway `python:3.12.7-alpine3.20` with the real `proof_proxy.py` and a test
key, in front of an echo service on the game PC's loopback. A request with `X-UOConsole-Proof: forged` arrived with
the key, once, with the login and body intact. `127.0.0.1:8097` in the container was refused. Run twice, the second
time after the `bind_refusal` change.

Full suites:

- **Web console (Python):** `python -m unittest discover -s web-console/tests`: **41 tests, OK** (23 of P155's, 18
  new, including both phone tests in headless Edge at a true 390 px).
- **The Golem:** `D:\UO\golem\tests\Golem.Tests.ps1`: **446 checks, 0 failed** (on the new `golem.ps1` before the swap).
- **Console facts:** the full run printed results up to the P154 facts and then ended silently with no summary line.
  **The same happens at HEAD.** I ran HEAD's suite from a temporary worktree (removed after), and it also ended there
  with no summary. So the crash is not P182's. Its failures were the same as mine plus four more that came from the
  worktree's path. The facts after that point (P155, P152 and the six P182 facts) ran with `SL_FACT_FILTER`: **17 of
  17 passed**. Failing in the full run, and failing at HEAD too: `PlayerCommandsNeverAppearInTheWorldTab` (a new
  `artificerrank` command from another prompt), P83 x2, P101 x2 and P107 (Haven mode since the ops cutover, as in
  P133's, P154's and P155's notes). Every `P125_*` and `P131_*` Golem-tab fact passed.
- **shard-migration tools:** `python -m unittest discover -s tools/tests`: 165 tests, the same 2 failures as before
  (`test_play_who.RealFiles`, other prompts' items; none of P182's).
- `Build-HavenDashboard.ps1 -Check`: up to date. `docker compose config` on the new compose (with a dummy key): valid,
  no `ports:`.
- The runner's dry run against the real Golem (read only): `poke` printed the console's plan; `wrapup` with a wrong word
  was refused (exit 2); `runnext P150` showed the new order (P150, then P183, ...). About 1.5 s each.

## Deviations and decisions for Chase

1. **Poke had no definition anywhere** (not in the console, the Golem, the plan or next-batch). Poke is now "the Golem's
   10-minute watch, now" (`Poke-Golem.ps1`, `-Event Watch`). It makes the Golem look again at a stall, a rest whose
   time has come, a pending self-wake or a night shift that ended. It changes nothing the watch would not change by
   itself. If you meant something else (nudging a quiet session, say), say so.
2. **Run next does not rename or renumber** (P148, held, asked for renaming). The pick is one file, `RUN-NEXT`, that
   `Sort-Queue` reads, so every order agrees and the hand-off that takes it removes it. A hand-off at the same moment
   takes either the old first or the pick, never half a rename, and other prompts' "Depends on P<nn>" lines stay true.
   The pick goes ahead of continuations too. P148's "Run next" in the console is this one now.
3. **Away mode is shown greyed and refused** (409, "arrives with P149"). P149 (away mode and email controls) is still
   queued and nothing exists to switch. When P149 lands, its two entries in `golem-actions.json` get an `action`.
4. **This PC's own page (`127.0.0.1:8095`) cannot act.** Any container on this PC's Docker can reach that port too, and
   there is no proof there. On this PC use the Shard Console, or open `https://uoconsole.tail81098d.ts.net/` (this PC
   has Tailscale), where the buttons work.
5. **Not proved end to end through Tailscale.** The new sidecar was not started, because installing is your step. Proved
   on this PC: the forwarder in a real container of the pinned image (above); the console's refusals; the compose file.
   One claim rests on how tailscaled works in userspace mode: a tailnet peer that dials `uoconsole:8097` directly lands
   on 127.0.0.1 in the node's namespace, where nothing listens, never on 127.0.0.2. For belt and braces you could
   restrict `tag:uoconsole` to port 443 in the tailnet access controls (P182-6).
6. **"Wake" is the console's Wake the Golem (CC session)** (`golem.resume`, which opens a CC session on the picked
   model). It refuses while the Golem is off, so **Turn on** (`golem.on`, Start-Golem.ps1) is there too.
7. **The confirm word ignores case** on the web (the console's own check is exact), because a phone capitalizes the
   first letter. The console's own phrase is what goes on to `Invoke-Plan`.
8. **Two reads were auto-denied** in this unattended run: the Read tool on `web-console\tailscale\serve.json` and on
   `web-console\static\app.js`. I had both files' contents from an earlier `cat` and did not read them again. I wrote
   the new versions in the scratchpad and copied them into place, then checked them with the tests and the phone
   screenshot.
9. **No server code changed**, so there was no `docker\uo\build.sh` run and no `sl-modernuo:cc-P182` image.
10. **The button art was filed as a request, not added to P152's list**, because P152 had already run.
    `web-console-golem-buttons` is in the Art tab.

## For Chase

Phase 1 is installed (your 06:49 install: the task SL web console and `uoconsole-ts` are running), so phase 2 is the
same install line again. It makes `proof.key`, stops and restarts the web console, and recreates the sidecar (the node
and its new proof forwarder). The node keeps its state, so it stays the same uoconsole.

1. **Install phase 2** (PowerShell on the game PC):
   - Dry run: `D:\ShatteredLegacy\web-console\Install-WebConsole.ps1 -Tailscale -DryRun`
   - Then: `D:\ShatteredLegacy\web-console\Install-WebConsole.ps1 -Tailscale`
   - Pass: no red docker lines, "sidecar started", and `docker ps` shows `uoconsole-ts` and `uoconsole-proof`.
2. **From your phone** (Tailscale on), open `https://uoconsole.tail81098d.ts.net/#golem`:
   - Wake: pick the model, type `wake the golem`, Run.
   - Once a prompt runs: Find a stopping point, type `find a stopping point`, Run.
   - Then Cancel stopping point, type `cancel`, Run.
   - Open the Timeline: the three presses are there, with their result lines.
3. **Check the refusals** on the game PC:
   - `curl.exe -s -o NUL -w "%{http_code}" -H "Tailscale-User-Login: <your login>" http://127.0.0.1:8096/api/health`
     prints 403 (no proof).
   - `http://127.0.0.1:8095/#golem` shows the buttons greyed.
4. **Retry stopped prompt**, the next time a prompt says STOPPED: on the web console or the Shard Console's Golem tab.
   Read why it stopped first, then type its number.
5. **The button icons**: the Art tab, request `web-console-golem-buttons` (15 icons, 28 px). Until they land, each
   button shows a letter in a bronze ring.
6. **Optional:** restrict `tag:uoconsole` to port 443 in the tailnet access controls (Deviation 5).

To go back to phase 1's behaviour, check out the previous `web-console` and run the same install line. Uninstall is
unchanged: `Install-WebConsole.ps1 -Uninstall [-Purge]`.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

No file over 5 MB: every new file is under 30 KB, and the largest changed one is `scripts\Shard-Console.ps1` at
0.79 MB (its facts file 0.55 MB). The tests' `__pycache__` folders, including the new
`web-console\tailscale\__pycache__`, are ignored (`.gitignore:76:__pycache__/`, proved with `git check-ignore -v`).
Scratch (patch scripts, the mutation pass, screenshots, the forwarder check) is in the session scratchpad, outside both
repos.

P182 DONE
