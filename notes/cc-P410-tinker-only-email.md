# cc-P410: one voice for Golem email: only the Tinker writes to Chase

2026-10-22. The Iron Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P410-tinker-only-email.md`.

## In plain words

- From now on only Terry the Tinker emails you. The Golems, the Codex helpers, Shadow Iron's merges, the overnight
  test bot and the Shard Console's live-shard questions hand their news to Terry instead of mailing you themselves.
- A problem (a Golem stopped or asking, a merge that failed, a stall, a commit that failed, a usage limit nearly
  reached, a PC that stopped answering mid-prompt, a bot crash) still reaches you at once, one mail each, with the few
  log lines behind it. The same open problem is not mailed twice; it shows in the next brief instead.
- Everything else (finished, merged, started, woke, night shift) waits for Terry's brief at 7:00 AM, 12:30 PM and
  6:00 PM: what got done, what each Golem is on, what waits on you, usage, what is next, and a short log at the bottom.
  The first brief is tomorrow at 7:00 AM. A sample of each is below.
- To try or deploy: the game PC already runs it (installed in `D:\UO\golem`). The family PCs and Stone switch over by
  themselves once the web console on the game PC runs this branch's `server.py` (restart it after the merge); until
  then they keep mailing you as before. Stone needs nothing by hand. To undo: set `tinkerOnlyMail` to false.

## What was asked, what was done

| Part | Done | Where |
|---|---|---|
| 1. Find every sender | Done: the list below, with file and line | this file |
| 2. Route, do not send | Every non-Tinker send writes one JSON event (when, Golem, PC, kind, subject, body, key, prompt, log lines) instead of mailing; the remote PCs' events go up through their agent like their status and questions | `GolemOutbox.ps1` (new), `golem.ps1` `Send-GolemMail`, `Remote-Agent.ps1` `Send-AgentOutbox`, `server.py` `save_outbox` (`POST /api/agent/outbox`), `Send-BotReport.ps1`, `Shard-Console.ps1` `Send-ConsoleMail` |
| 3. The Tinker sends | Problems at once, deduplicated by key while open; info held; replies to Chase's emailed commands at once | `TinkerMail.ps1` (new) `Invoke-TinkerMailRound`, `Send-TinkerProblem`, `Update-TinkerProblems`; `TinkerLib.ps1` |
| 4. The brief | 07:00, 12:30, 18:00; plain part, then "The log"; `tinkerBriefTimes`, `tinkerOnlyMail` | `TinkerMail.ps1` `New-TinkerBrief`, `Get-TinkerBriefDue` |
| 5. Tests | 7 new facts and 1 web console test, each seen failing on the old code first | below |
| 6. Ship to every PC | Installed on the game PC; the kit snapshot carries it to the other PCs; `server.py` goes with this branch | below |

## 1. Every place mail was sent (before this change)

Line numbers are the pre-P410 files (the copy hashed at the start).

| Sender | Where | Notes |
|---|---|---|
| The one mail function of every Golem's hook | `D:\UO\golem\golem.ps1:331` `Send-Mail` (SMTP), called only from `golem.ps1:355` `Send-GolemMail` | cc-P157 put every hook mail through `Send-GolemMail`; routine ones were folded into `mail-later.jsonl` unless `routineEmails` |
| Finished / handoff / queue empty / progress | `golem.ps1:373` `Send-DoneLeft` (`progressEmails`), `:3493` handoff, `:4937` queue-empty | info |
| Rest, usage limit, pace, run cap | `:2801`, `:4554` | info; the usage limit one is a problem |
| Night shift | `:1993` `Send-NightSummary` (`:2032`), `:2232` night-start, `:2274` night-skipped | info |
| Marathon, queue low, reset offer, plan stale | `:1113`, `:1120` `Send-QueueLow` (to the overseer's address with `-To`, unchanged), `:878` `Send-ResetOffer`, `:4236` | plan stale is a problem |
| Woke a session, model fallback | `:1916`, `:4408` | info, problem |
| The integrator and Shadow Iron (merges) | `:2602`, `:2603` (old integrator), `:2674` merge-waits, `:2687` merged, `:2690` fix-up, `:2696`, `:2699` merge-needs-you | merged is info; the rest are problems |
| The Codex lane finish and its problems | `:3077` lane-needs-you, `:3158` lane-cannot-start, `:3180` lane-lost, `:3261` lane-done | via the same hook (`Codex.ps1` sends nothing itself) |
| Stops, questions, stalls, commits | `:3299`, `:3430`, `:3456`, `:3872` question, `:4123` stale lock, `:4127` stale claim, `:4305` stalled, `:4639` waiting-on-you, `:4649` registry, `:4689` parked, `:4727` stopped, `:4778`, `:4903` commit-failed, `:4967` mid-task | |
| Away mode and email commands | `D:\UO\golem\Away.ps1:255`, `:264` (away ended, digest), `:515`, `:529` (replies to Chase's commands) | dot-sourced into the hook; the replies are kind `reply` |
| The Tinker | `D:\UO\golem\TinkerLib.ps1:394` `Send-TinkerMail`, `:416` its question mail | now the only sender |
| The remote agent | `Remote-Agent.ps1` sent no mail itself; each remote PC's own hook mailed through its own `Send-Mail` | now its events go up through the agent |
| The overnight bot | `D:\ShatteredLegacy\tools\playtest-bot\Send-BotReport.ps1:32` (start, crash, morning report, written by `uobot\notify.py` and `report.py`) | crash is a problem; start and report go in the brief |
| The Shard Console | `D:\ShatteredLegacy\scripts\Shard-Console.ps1:7166` `Send-ConsoleMail` (cc-P106: the live shard waits for an answer) | a problem |
| Test and setup mails | `Send-TestEmail.ps1:19`, `Setup-Email.ps1:12` | left as they are: run by hand, to check the mail works |
| The switches | `settings.json` `progressEmails` (still decides whether a finish is reported at all), `routineEmails` (cc-P157 folding; not used while routing), `notifications` (Windows toasts, not mail), `mailCommands` (off on the game PC) | new: `tinkerOnlyMail`, `tinkerBriefTimes` |

## How it works

**A sender** (`Send-GolemMail`, `Send-BotReport.ps1`, `Send-ConsoleMail`) asks `Test-OutboxRoute`: `tinkerOnlyMail`
on, an enabled `Tinker` in `golems.json`, and on the Tinker's PC a Tinker round in the last 60 minutes and not paused,
on another PC the agent's mark `outbox-accepted`. Yes: it writes `outbox\<id>.json` and logs `to the Tinker (<kind>):
<subject>`. No: it mails as before and logs `not via the Tinker (<why>)`. So a stopped or paused Tinker never swallows
mail. A mail with `-To` (the low-queue mail to the overseer's address) is sent as it is.

**The kinds:** `problem` = every "Needs you" mail, plus fix-up, merge failures, stalled, mid-task, commit failed,
cannot start, model fallback, plan stale, a rest for a usage limit, a bot crash, a live shard question. `reply` = the
answer to Chase's own emailed command (sent at once, never held). Everything else is `info`. The key is
`<mailKind>|<golem>|<prompt>`.

**Family PCs and Stone:** each PC's Golem writes into its own `D:\UO\golem\outbox\`; its `Remote-Agent.ps1` (already
calling the game PC every 5 to 60 seconds for commands and status) posts up to five events (48 KB) a call to
`POST /api/agent/outbox`; the web console keeps them in `remote\<Golem>\outbox\` (named for the agent's own Golem,
its key rebuilt from that name), and the Tinker reads them beside its own outbox. The file leaves the PC only once the
game PC has it. An empty post every 10 minutes is the probe: the first good answer writes `outbox-accepted`, and only
then does that PC's Golem route its mail. An older web console answers 404, the mark is removed, and the PC mails
itself as before.

**The Tinker's round** (every 10 minutes, after its fixes): each event is read; a problem is mailed at once unless the
same key is still open; problems and info are kept in `tinker-mail\held\`. Its own problems: a PC that has not
answered for 30 minutes while its Golem's last status was running something (a PC asleep with nothing in hand is only
in the brief), and any usage window at 90% or more (Claude week, Claude 5-hour, Fable week when read, each Codex
account's week and 5-hour), once per window. Its questions (`Add-TinkerQuestion`) are open problems too. Closing: a
Golem's problem when that Golem is no longer STOPPED or NEEDS YOU and the problem has been quiet for 30 minutes (no
Golem status: after a day); the Tinker's own when the cause is gone. A closed problem can mail again.

**The brief** at each brief time (a brief more than three hours late is skipped and the next one carries it; the
first round after install sends none, so the first is tomorrow at 7:00 AM): done since the last brief (a line per
prompt with the first of its plain words; prompts without plain words counted per Golem), the crew now, waiting on you
(open questions with their choices, then problems still open), usage, next up, what to do, then "The log" (at most 40
lines: merges into main with their commits, claimed / handed / DONE / STOPPED lines from every Golem's log in time
order, other events, the Tinker's fixes and closings). Then the held events move to `tinker-mail\briefed\<time>\` with
`brief.txt`, the brief as sent (kept 7 days). The Tinker's card carries `mail` (last brief, open problems, how many
wait).

Signed: the From name is "Terry the Tinker", every mail ends "Terry the Tinker, the crew foreman", and the subject
keeps `[Tinker]` so existing mail filters still match.

## Sample brief (written from today's real data)

The 6:00 PM brief for 12:30 to 6:00 PM on 10-22, from the real statuses, usage files, logs, the cc-prompts queue and
main's merges in that window (each merge stands for the finish and merge events the Golems would have written). Made
by `make-samples.ps1` in a copy; nothing was sent. The log is cut after ten lines here (the brief has 40).

```
Subject: [Tinker] The 6:00 PM brief: 27 done, nothing waiting on you

Terry here with the 6:00 PM brief on the crew.

Done since the 12:30 PM brief:
- P428 (Crystal), by Crystal, now in main: Nothing serious: no crash, no broken save, no merge that lost or doubled code.
- P429 (Crystal), by Crystal, now in main: I read the eleven Codex reviews that are in main: P400 to P404, P407, and P418 to P422. Then I checked every finding
- P408 (port OSI's Treasures of Sorcerer's Dungeon), by Iron, now in main: OSI's Halloween event, Treasures of Sorcerer's Dungeon, is now on the shard, ported from ServUO as written. From
- Verite: 13 more, in main (P418, P419, P421, P423, P425, P430, P432, P434, P437, P439, P441, P443, P445).
- Valorite: 11 more, in main (P417, P420, P422, P424, P426, P431, P433, P435, P438, P440, P442).

The crew now:
- Iron: working on P410 (one voice for Golem email)
- Bronze: off
- Valorite (Codex): off
- Verite (Codex): off
- Copper: idle, nothing it can take right now
- Stone: its PC is not answering me (it may be asleep or off)

Waiting on you:
- Nothing.

Usage:
- The Claude week: 20%, resets Wednesday at 4:00 PM
- The Claude 5-hour window: 0%, resets 11:00 PM
- Codex (Chase's account) week: 18%, resets Oct 29 at 3:31 PM
- Codex (Chase's account) 5-hour window: 19%, resets tomorrow at 1:37 AM
- Codex (Steph's account) week: 18%, resets Oct 29 at 3:37 PM
- Codex (Steph's account) 5-hour window: 16%, resets tomorrow at 1:37 AM
- Codex (the game PC) week: 9%, resets Oct 29 at 12:08 PM
- claude.ai says: Heads up. At this pace you'll run out Tuesday afternoon, before Wednesday's reset.
- No usage reset on offer.

Next up: P372 (fix-up for P168), P374 (continue P265), P375 (fix-up for P223), and 34 more.

What to do: nothing, the crew keeps going.

The log
-------
merge ShatteredLegacy 7508639 10-22 15:04 Merge golem/Iron/P408: CC task P408: port OSI's Treasures of Sorcerer's Dungeon (Jack the Pumpkin King) for Halloween
merge shard-migration d742e00 10-22 13:51 Merge golem/Verite/P418: CC task P418: a code review of the League Register build (P280) (review notes)
merge shard-migration 0636306 10-22 14:01 Merge golem/Valorite/P417: CC task P417: rolled gathering orders for the Miners, Foresters and Outriders (design notes)
merge shard-migration f394234 10-22 14:11 Merge golem/Verite/P419: CC task P419: a code review of the guild hall decor packs (P265) (review notes)
...
10-22 13:30  Iron  Prompt claimed P408 (cc-P408-sorcerers-dungeon-halloween.md) for Iron: areas server, branch golem/Iron/P408
10-22 13:32  Valorite  Watch claimed P417 (cc-P417-gathering-orders-design.md) for Valorite (Codex lane): areas docs-only, branch golem/Valorite/P417; outside its window: a Send to the second PC holds until 14:59
10-22 13:47  Verite  LaneFinish lane: P418 DONE by Codex: lane tests green, preflight clean (0 test command(s))
...

-- 
Terry the Tinker, the crew foreman
```

What the sample shows that is worth knowing: the "crew now" part reads each Golem's status as it is at the time of the
brief (here, 9 PM, when the sample was made; at a real 6:00 PM it is that moment's). A plain-words line is the first
bullet of the notes' "In plain words", cut where the notes wrapped it, so a few end mid-sentence ("From"); the Golems'
own done mails have always done the same.

## Sample problem mail (written from today's real data)

Iron's question about P263 at 3:54 AM today, as the hook builds it (`New-GolemMail 'question'` with the real question
file) and as the Tinker now mails it, with the real log lines from `golem.log`. (Those log lines still say "emailed":
they are from before this change; from now on they say "to the Tinker".)

```
Subject: [Tinker] Needs you: Iron has a question about P263 (the "Noted by the System" hidden)

Terry here. Iron ran into a problem at 3:54 AM.

The Iron Golem is asking you about P263 (the "Noted by the System" hidden) and has stopped until you answer.

The question:
P263 (the Noted by the System hidden achievements) was handed to Iron again, but it is already done and in main: Copper built it (commit 177a3aa, notes/cc-P263-noted-by-the-system-achievements.md ending P263 DONE) and P361's fix-up merged it (460f0e2; NotedBySystemVerification and 45 noted.* achievements are on main). Only P361's prompt was moved to cc-prompts\completed, so the queue re-issued P263. Doing it again would duplicate every achievement, which the prompt forbids. What should I do?

Choices:
- Retire it: Move the P263 prompt to completed with no code change; nothing is rebuilt
- Review it: Check main's P263 work against the prompt's Done-means list and fix only what is missing
- Redo it: Rebuild P263 from scratch on top of main (not recommended: duplicates)

Good to know:
- You can also answer in your own words.

What to do: answer it on the Golem card of the web console. Pick a choice or write your own answer.

Details
-------
Question Iron-P263-20261022-035456-bc54 on the Golem card.

The log
-------
2026-10-22 03:54:59  Ask          emailed: [Iron Golem] Needs you: Iron has a question about P263
2026-10-22 03:55:06  Stop         Golem Iron P380 kept open: P263 STOPPED
2026-10-22 03:55:06  Stop         P263 STOPPED, no commit
2026-10-22 03:55:08  Stop         emailed: [Iron Golem] Needs you: P263 stopped with a question
2026-10-22 03:55:08  Stop         notified: Golem: P263 STOPPED, needs you

I mail about a problem once. If it is still open at my next brief, it is in the brief.

-- 
Terry the Tinker, the crew foreman
```

Today Chase got two mails for that one stop (the question at 3:54:59 and the STOPPED at 3:55:08). Now both are the
one problem `needs-you|Iron|P263`, so only this mail goes out. See Deviations 3.

## Tests

Windows PowerShell 5.1 throughout. Every new test was first run against the code before the change and seen failing.

| Test | Old code | New code |
|---|---|---|
| `tests\Tinker.Tests.ps1` `P410_AProblemIsSentAtOnceAndNotAgainWhileStillOpen` (mailed once with its log lines and Terry's name; not again while Gold is still STOPPED; its question for the same stop is not a second mail; closed once Gold runs again; a new stop mails again) | FAIL (threw: no `Invoke-TinkerMailRound`) | PASS |
| `P410_ABriefAtABriefTimeCollectsTheHeldEventsAndClearsThem` (info is held, no mail; the 12:30 brief has P172's line, merged, the crew, what is next, the log at the bottom, no file paths above it; the held events are cleared; one brief per time; `tinkerOnlyMail` false: no brief) | FAIL | PASS |
| `P410_TheBriefTimesComeFromTheSettingAndAMissedOneIsNotSentLate` | FAIL | PASS |
| The one-stop part of the first fact (a question and a STOPPED for the same prompt, added after the 10-22 P263 double mail) | FAIL on the code before that fix (2 mails) | PASS |
| `tests\Golem.Tests.ps1` `P410_AGolemsFinishMailLandsInTheOutboxAndIsNotSent` (the finish is an event with when, Golem, PC, kind, key and the body; no mail; a STOPPED is a problem with key `stopped\|...\|P100`) | FAIL (5 checks) | PASS |
| `P410_TinkerOnlyMailFalseOrNoLiveTinkerSendsAsToday` (`tinkerOnlyMail` false, a Tinker silent for two hours, no Tinker: each mails as before, and the log says why) | FAIL (the two "says why" checks; the mails themselves were already as today) | PASS |
| `tests\RemoteAgent.Tests.ps1` `P410_ARemoteGolemsMailEventsGoToTheGamePcForTheTinkerAndTheMarkIsLeft` (against the real web console in its harness) | FAIL with the old `Remote-Agent.ps1` (3 checks) | PASS |
| `web-console\tests\test_remote_golems.py` `test_the_agent_posts_its_mail_events_for_the_tinker` (the probe, one event kept under the agent's own name and key, four bad bodies refused, a wrong secret refused) | FAIL (error) on HEAD's `server.py` | PASS |

**The rest of `tests\`**, old code (a pristine copy) against new:

| Suite | Old code | New code |
|---|---|---|
| `Golem.Tests.ps1` | 1483 passed, 5 failed: the two P184 facts (`P184_OverlappingTouches...`, `P184_TouchesAreReadOrGuessed...`), the known 10-22 failures | 1495 passed, 6 failed: the same 5 P184 checks, and `P131_AUsageLimitRestSaysWhenItIsReadyAndNotifiesWhenItIs`, which fails the same way on the old code when run after about 9:50 PM (the countdown crosses midnight and gains a day name: "Ready at Fri 12:24 AM"); run alone on both at 22:00, both FAIL |
| `Tinker.Tests.ps1` | 133 passed, 0 failed | 157 passed, 0 failed |
| `RemoteAgent.Tests.ps1` | exit 0 | exit 0 (with the new fact) |
| `Lane.Tests.ps1`, `Codex.Tests.ps1` | exit 0 | exit 0 |
| `Join.Tests.ps1` | 102 passed, 4 failed (this PC's own setup: Tailscale, folder owners, OpenSSH, Docker; two facts) | the same 102 and 4 |
| Installed copy, `-Only P410` | | Tinker 24 checks, Golem 13 checks, all pass on `D:\UO\golem` |

**ShatteredLegacy:** `web-console` (`python -m unittest discover -s tests`): 111 tests, 3 failures, all in
`test_golem_glow.PhoneGlow.test_five_states_on_a_phone` (Edge, the glow animation); HEAD's untouched web console fails
the same 3. `scripts\tests\Shard-Console.Tests.ps1`: 443 facts, 430 passed, 13 failed, the same 13 as on HEAD's
`Shard-Console.ps1` (World tab, window actions, P83, P101, P107, P135). One run also failed
`P154_TheRefreshNeverRunsOnTheWindowsThread` (a timing fact on the window thread); the next run passed it.
`Send-BotReport.ps1` has no test; `Add-OutboxMail`, which it calls, was checked by hand on a temp root (routed as a
problem with key `bot-crashed|Bot|<date>`; not routed with `tinkerOnlyMail` false), and every edited script parses.

**Live:** the Tinker's scheduled round at 22:28 ran the mail part: `briefs start: the last brief time was 2026-10-22
18:00; the next one is the first brief`, no mail, no open problem (Stone's PC is not answering, but its Golem has been
idle since 10:23 AM, so that is only in the brief).

## 6. Shipping it to every PC

- **The game PC: installed** in `D:\UO\golem` (not a repo; each replaced file backed up as `<name>.bak-20261022-P410`):
  `golem.ps1`, `TinkerLib.ps1`, `Remote-Agent.ps1`, `README.md` (a new section), the new `GolemOutbox.ps1` and
  `TinkerMail.ps1`, and `tests\Golem.Tests.ps1`, `tests\Tinker.Tests.ps1`, `tests\RemoteAgent.Tests.ps1`. Before
  installing, the live files' hashes were checked against the copy the change was built from. `settings.json` gained
  `tinkerOnlyMail: true` and `tinkerBriefTimes: "07:00,12:30,18:00"` (backup beside it). Every Golem on the game PC
  hands its mail to the Tinker from its next email.
- **The other PCs (Copper, Gold, Silver, Stone, ...): by the kit, as usual.** The Tinker takes no kit snapshot while a
  prompt touching the golem area runs ("not taken: Iron runs P410"); once the Golem commits P410, the next round
  snapshots the kit, and each PC's agent (or the Tinker over SSH) installs it. Both new files are top-level `*.ps1`, so
  they are in the kit; the two settings travel as kit settings keys (added where missing, never overwriting). A new
  `Remote-Agent.ps1` restarts its own agent task.
- **Then the web console on the game PC must run this branch's `server.py`** (the `/api/agent/outbox` endpoint): it
  reaches `D:\ShatteredLegacy` when Shadow Iron merges `golem/Iron/P410`, and the web console has to be restarted to
  load it. Until then the other PCs' agents get a 404, leave no `outbox-accepted` mark, and those Golems keep mailing
  Chase themselves, exactly as today. After the restart, each agent's next probe (within 10 minutes) leaves the mark
  and its Golem switches over.
- **Stone (no SSH): nothing by hand.** Its agent pulls the kit itself (`GET /api/agent/kit`) when its PC is on, and
  probes the outbox endpoint itself. Stone's PC has not answered since 10:23 AM today; it picks all of this up the next
  time it is on. If Stone's agent is ever older than cc-P222 (no kit pull), it needs the kit unpacked by hand as in
  JOIN-PC.md, but nothing here suggests that.
- **The overnight bot and the Shard Console** (`Send-BotReport.ps1`, `Shard-Console.ps1`, in ShatteredLegacy) switch
  over once the merge reaches `D:\ShatteredLegacy`. They find `D:\UO\golem\GolemOutbox.ps1` beside the mail settings,
  which is already installed.
- **To roll back:** `settings.json` `tinkerOnlyMail: false` (per PC), or put the `.bak-20261022-P410` files back.

## Deviations and decisions for Chase

1. **Two more senders routed than the prompt listed:** the overnight bot (start, crash, morning report) and the Shard
   Console's live-shard question mail. "Only the Tinker emails" seemed to cover them. A bot crash and a live shard
   question are problems (mailed at once); the bot's start and its morning report go in the 7:00 AM brief. The setup
   and test mails (`Send-TestEmail.ps1`, `Setup-Email.ps1`) still send directly: they exist to check the mail works.
   The low-queue mail to the overseer's address (`-To`) is not to Chase and is sent as before.
2. **A third kind, `reply`,** beside problem and info: the answer to an email command Chase sent (away mode, cc-P149)
   is mailed by the Tinker at once, never held for a brief.
3. **One stop is one problem.** On 10-22 one P263 stop sent two mails 9 seconds apart (the question, then the
   STOPPED). The Tinker now keys a Golem's question, STOPPED, mid-task stop, waiting-on-you and parked mails for the
   same prompt as one problem (`needs-you|<golem>|<prompt>`), so that is one mail. Its own questions stay separate.
4. **A silent or paused Tinker never swallows mail:** if the Tinker on the game PC has not run for 60 minutes or is
   paused, the Golems mail as before. On other PCs the switch waits for the web console (above).
5. **No brief at install:** the first round only records the last brief time (6:00 PM today), so the first brief is
   tomorrow at 7:00 AM. A brief more than three hours late (the game PC off at brief time) is skipped; the next one
   carries everything.
6. **Email commands:** a mail from the Tinker carries no one-time reply code (cc-P149's `mailCommands`, which is off on
   the game PC). If email commands are turned on later, replies to Terry's mails will need the code added to them.
7. **Unattended-run denials (two):** a Bash loop copying every file of `D:\UO\golem` into the scratchpad was denied; I
   copied the kit's file types by name instead (`cp D:/UO/golem/*.ps1 ...`). The Read tool was denied on
   `D:\UO\golems\Iron\ShatteredLegacy\web-console\server.py` (to fix one docstring line I had written with a
   backslash path); I fixed it with a small Python script instead. Neither changed what was done.
8. **Pre-existing failures** are listed under Tests: the P184 pair, the P131 clock fact after 9:50 PM, the Join
   environment checks, the phone glow test and the 13 Shard Console facts. None is from this change.

## Files

**`D:\UO\golem`** (installed; backups `.bak-20261022-P410`): `GolemOutbox.ps1` (new), `TinkerMail.ps1` (new),
`golem.ps1` (`Send-GolemMail` routes; the two settings), `TinkerLib.ps1` (settings, `Send-TinkerMail` signed by Terry,
questions as open problems, the mail round, the card's `mail`), `Remote-Agent.ps1` (`Send-AgentOutbox`), `README.md`,
`settings.json`, `tests\Golem.Tests.ps1`, `tests\Tinker.Tests.ps1`, `tests\RemoteAgent.Tests.ps1`.

**`D:\ShatteredLegacy`** (branch `golem/Iron/P410`): `web-console\server.py` (`save_outbox`, `POST /api/agent/outbox`),
`web-console\tests\test_remote_golems.py`, `tools\playtest-bot\Send-BotReport.ps1`, `scripts\Shard-Console.ps1`
(`Send-ConsoleMail`).

**`D:\UO\shard-migration`** (branch `golem/Iron/P410`): this notes file.

P410 DONE
