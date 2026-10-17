# cc-P155: Web console, phase 1: status, read only, at uoconsole on the tailnet

2026-10-17. Opus. Phase 1 of 6 of `D:\UO\overseer\web-console-plan.md`, to Chase's decisions of 13:15: game PC, Python,
only Chase, `uoconsole` on the tailnet. The PowerShell console keeps working alongside it.

## Headlines

- **A read-only web console** at `D:\ShatteredLegacy\web-console\`: tiles and lights, the Golem (state, reason, ready
  countdown, the running prompt and the queue with each Summary, model and size, finished prompts with their headline,
  night shift, self-wake, usage bars), Today on one phone screen, Needs you, a timeline, a log viewer with search, and
  a links hub with up dots. Polls every 5 s; never blocks.
- **Python standard library only** (like the play-test server): nothing to install, starts with `pythonw` from a
  scheduled task at Chase's logon. **Listens on 127.0.0.1 only**, on two ports: `:8095` for this PC, `:8096` for the
  sidecar.
- **`https://uoconsole.tail81098d.ts.net/`** comes from a Tailscale container on the game PC's Docker (hostname
  `uoconsole`, Tailscale Serve, its certificate, **Funnel off, no published port**). **Only Chase:** on `:8096` a request
  is answered only when Serve's `Tailscale-User-Login` is an allowed login (default: this PC's own Tailscale login, read
  at run time, never written to git); local requests on `:8095` are allowed. Everyone else gets `not allowed`.
- **Not run for real yet:** there is no Tailscale auth key, so the sidecar has not started and the page has not loaded
  at `https://uoconsole...`. Everything up to the sidecar was proved on this PC (below).
- **One status source:** the Shard Console's own reads (`Get-ConsoleRefreshData`, cc-P154) now end in one status file,
  `scripts\shard-console-cache\console-status.json` (schema 1). Two writers, one logic: the console's refresh runspace
  after each refresh, and `scripts\Write-ConsoleStatus.ps1`, a collector loop the web console starts, which skips a
  turn while the console has written recently. The web console reads only that file; the Shard Console paints its tiles
  from it at its start.
- **Never a secret on a page:** every string the service sends passes a redactor (tokens, keys, passwords, bearer
  headers, private keys, `tskey-`, `ghp_`, `sk-` and more); logs are tail-only and redacted; the status file carries no
  secrets by design.
- Tests: 23 Python tests and 6 new console facts, every one seen failing (23 breaks, all restored by hash). The phone
  check runs at a true 390 px through DevTools device emulation, because headless Edge will not make a window narrower
  than about 500 px. A plain `--window-size=390` gave a 492 px viewport and would have proved nothing.
- **Two bugs found by my own checks:** the status file could not be written over once it existed (`[IO.File]::Replace`
  with `$null` gets `''` from PowerShell), and the first phone check was not at phone width. Both are fixed, and each now
  has a check that fails without the fix.
- **No task-list tool** in this session, as in P154: progress went to the chat only.

## The design, and why

**Where:** the game PC. The status is the game PC's Docker, files, Golem and repos (and phase 2 onward act on them).

**Python, standard library** (not FastAPI): `docker\test-queue\server.py` already serves the play-test pages this way,
the game PC has Python 3.11 and 3.12 and nothing to `pip install`, and phase 1 needs only GETs. FastAPI would buy request
validation and async that phase 1 does not use, at the price of a dependency to install and keep current on the game
PC. The question is open again for phase 2 (actions with streamed output); `http.server` can stream, so I expect not.

**A scheduled task at logon, not a Windows service:** the console reads Chase's files, Docker Desktop (in his session)
and his Tailscale login, like the Shard Console and the Golem; a service would run as another account. The cost is that
it is down while nobody is logged on to the game PC (so is the Golem).

**The name `uoconsole`:** a tailnet name is a machine name, so the console has its own node: `tailscale/tailscale:v1.88.3`
in userspace mode (no `NET_ADMIN`, no tun), Tailscale Serve proxying `https://uoconsole.tail81098d.ts.net/` to
`http://host.docker.internal:8096`. Proved on this PC before relying on it: a container reaches a service bound to
`127.0.0.1` on the game PC through `host.docker.internal` (Docker Desktop forwards it), so the service never needs a LAN
or `0.0.0.0` bind.

**Who gets in, and why two ports:** a request from the sidecar and a request from a browser on this PC both arrive from
`127.0.0.1`, so the address cannot tell them apart. The port does: `:8096` is only ever the sidecar's target and demands
the identity header; `:8095` is this PC. A tagged device or anything without a user login gets no header from Serve and
is refused. Serve drops any `Tailscale-User-*` header the caller sent.

**One status source:** the gathering stays where it is (`Get-ConsoleRefreshData` and the judging functions in
`Shard-Console.ps1`); `ConvertTo-ConsoleStatusDocument` turns one refresh into plain data and `Write-ConsoleStatusFile`
writes it atomically. The collector is the console's code dot-sourced, not a copy: `Write-ConsoleStatus.ps1` is 62 lines
that call those functions. It runs as one long loop (not a fresh process every 30 s) so its in-process caches survive:
the download site is checked at most every ten minutes, as in the console, and the prompt heads are read again only when
a file changes (cc-P154's caches). The lights' judgement moved into `Get-LightsFromFacts`, used by both the console's
lights and the file, so it exists once.

**What could not move cleanly, kept in one place anyway:** the new panels (Needs you, the timeline, the links' up dots,
the log viewer) are the web console's own and live in `web-console\panels.py`. The Shard Console does not show them yet,
so there is still only one copy. The DNS and websites tiles in the file come from the console's own probes when the
console writes it, and from the collector running the same `Get-NetworkProbe` and `Get-WebsiteProbe` when it does.

**What phase 1 shows:**

| Panel | From |
|---|---|
| Tiles (LIVE, TEST, STATUS PUBLISHER, PUBLIC DNS, GOLEM, PLAY TESTS, WEBSITES) and both lights | the status file: `Get-AtAGlance`, `Get-DnsGlance`, `Get-AutopilotGlance`, `Get-PlayTestGlance`, `Get-WebsitesGlance`, `Get-LightsFromFacts`, as the console judges them |
| The Golem | the status file: state, reason, ready time, winding, stopped prompt, the running prompt (Summary, model, size, steps, started, last activity), the queue in order (Summary or the first paragraph, model, size, "next"), ten finished prompts with their notes headline, night shift, self-wake, usage bars (`Get-UsageBars`) |
| Needs you | a STOPPED Golem or a stopped prompt, the Golem's needs-you, P146's `testing\decisions.json` when it exists (it does not yet; the page says so), play-test items whose Who is You, Bot then you or You decide (`tools\playwho.py`, the play-test page's own logic; the first ten, then a count: there were 85), a built service not deployed yet (P133's `services.json`), a package to publish (the package light says PUBLISH), and open lines of the overseer's chore list `notes\chores.md` (new, empty) |
| Timeline | both repos' last 25 commits, the console's action transcripts (`scripts\shard-console-output`: builds, deploys, publishes, commits, other actions), Haven deploy transcripts, the Golem's finished prompts, the overnight bot runs; newest first, 60 |
| Logs | fixed keys only, never a path: the Golem log, the console's action log, the test shard (`docker logs --tail 2000`), the newest action transcript, the newest Haven deploy, the newest bot run, the collector; tail, search, redacted |
| Links | the console's `websites.json` sites with the collector's checks, `web-console\links.json` (Haven dashboard on the tailnet, both Portainers, the download site; checked every 60 s, a redirect or 401 counts as up), both GitHub repos (from `git remote`) |
| The look | the Enhanced theme's colours (`Get-ConsoleTheme 'Enhanced'`), the console art from `scripts\console-art` by slot name when a slot has a file (crystal-<colour>, stone); drawn stand-ins otherwise. Today the folder has no art, so every slot uses its stand-in |

What P143 and P148 put here: P143's status reads (remote, over the tailnet, with an identity check) and P148's Today,
Needs you, the timeline, the log viewer and the links hub, all read only. Their actions, hide and archive, search,
launch buttons, quick actions and Run next belong to phases 2, 3 and 5.

## What changed

D:\ShatteredLegacy:

| File | Change |
|---|---|
| `web-console\server.py` (new, 426 lines) | The service: `Console` :49 (allowed logins :70, the status file :95, refresh request :105, the collector child :118, link checks :137, panels :160, log sources by key :217), handlers :306 (identity on every request, GET and HEAD only, security headers, redaction of everything sent), `main` :402 (any bind but loopback refused) |
| `web-console\panels.py` (new) | Pure functions: `decide` :26, `redact`/`redact_tree` :60, `parse_chores` :83, `needs_you` :95, the timeline :153-:180, `links` :208, `tail` :230, `status_problems` :242 (schema 1 as both consoles read it) |
| `web-console\static\index.html`, `app.js`, `app.css` (new) | The page: six sections, phone first, text set only with `textContent`, no inline script or style (the CSP forbids both) |
| `web-console\links.json` (new) | The extra links and their checks |
| `web-console\tailscale\docker-compose.yml`, `serve.json` (new) | The uoconsole node: pinned image, userspace, no ports, key from `D:\UO\web-console\tailscale.env`, Serve HTTPS 443 to `host.docker.internal:8096`, Funnel false |
| `web-console\Install-WebConsole.ps1` (new) | The task (`-DryRun`), the sidecar (`-Tailscale`, refuses without a key), `-Uninstall [-Purge]`; refuses SYSTEM; never prints the key |
| `web-console\tests\test_web_console.py`, `tests\cdp.py`, `tests\fixtures\console-status.json` (new) | 23 tests; a minimal DevTools client for the phone check |
| `scripts\Write-ConsoleStatus.ps1` (new) | The collector: one refresh, or `-Loop` with the request file and the skip when the console wrote recently |
| `scripts\Shard-Console.ps1` | `Get-LightsFromFacts` :1599 (and `Update-Lights` uses it); `Get-PromptInfo` :4015 reads `**Summary:**`; `StatusFile` in the config :407; the status file :8357-:8480 (`Get-StatusTileKey`, `Get-PromptSize`, `ConvertTo-ConsoleStatusDocument` :8370, `Write-ConsoleStatusFile` :8427, `Read-ConsoleStatusFile` :8445, `Show-StatusFileTiles` :8458); the refresh runspace writes the file after a refresh of the tiles (`Start-ConsoleRefresh` :8661, never from a capture); the window paints its tiles from the file at its start |
| `scripts\tests\Shard-Console.Tests.ps1` | Six `P155_*` facts (:6601-:6710) |
| `docker\haven\services.json`, `docker\dashboard\haven\config\services.yaml` | `web-console` and `uoconsole-ts` (31 services, 36 tiles), the dashboard regenerated (P133's rule) |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.17.3`, two `### Staff` lines; 2026.10.17.3 |

D:\UO\shard-migration: `notes\haven-runbook.md` (two service sections and a Changed-on line), `notes\chores.md` (new, the
overseer's chore list, empty), this file.

Outside both repos: `D:\UO\web-console\` (the installer makes it: settings, the key file, logs). Nothing was installed
here: no task registered, no sidecar started.

## Security checks, and how each was proved

| Rule | Proof |
|---|---|
| 127.0.0.1 only | `netstat` with the service on its real ports: `127.0.0.1:8095` and `127.0.0.1:8096` LISTENING, nothing else. `server.py --bind 0.0.0.0` refuses to start (fact `P155_TheWebConsoleListens...`) |
| Nothing from the LAN or the tailnet address | `curl` to `192.168.1.58:8095`, `:8096` and `100.78.49.68:8095`, `:8096`: connection refused (curl exit 7), all four |
| Nothing from the internet | the router forwards 80, 443 and 2593 to Haven only (runbook); the service is on loopback; the sidecar publishes no port (`docker compose config`: 0 `ports:`) and Funnel is false in `serve.json` |
| Only Chase on the tailnet | from a container on this PC (the sidecar's path, `host.docker.internal:8096`): no identity 403, `someone@example.com` 403; `access.log` recorded "no Tailscale identity" and "login not allowed" and not the caller's header. Tests: allowed login (any case) 200, other login 403, no identity 403, blank 403, no known login refuses all, local 200 |
| Accept no action | every method but GET and HEAD returns 405 (test); the only state a GET touches is the collector's request file (`?refresh=1`, at most every 10 s) |
| No secret on a page or in a log | redaction tests (seven kinds, bare and named); a token planted in the fixture never reaches the JSON or the rendered page; the access log writes listener, code, path and reason, never headers; logs are read by key, never by path (`?source=C:\Windows\win.ini` is 404); art by slot name only (`/art/../server.py`, `README.md`, `art.json` all 404) |
| Not framed, not sniffed | `Content-Security-Policy: default-src 'self'... frame-ancestors 'none'`, `X-Frame-Options: DENY`, `nosniff`, `no-store` (test) |

## Tests

Python, `python -m unittest discover -s web-console/tests` (from the shard repo): **23 tests, OK**.

| Test | Seen failing by |
|---|---|
| `Identity.test_no_identity_is_refused` | a missing identity let in |
| `Identity.test_the_allowed_login_on_the_tailnet_listener` | logins compared with case |
| `LiveServer.test_tailnet_listener_answers_only_the_allowed_login` | the tailnet listener treated as local |
| `LiveServer.test_read_only_every_other_method_is_refused` | the 405 handlers removed (501) |
| `LiveServer.test_no_secret_reaches_a_page` | no redaction on the way out |
| `LiveServer.test_the_status_is_the_file_both_consoles_read` | the status not read from the file |
| `LiveServer.test_art_is_served_by_slot_name_only` | any file in the art folder served |
| `StatusShape.test_problems_are_named` | the schema not checked |
| `Panels.test_needs_you_from_fixtures` | play tests not capped; an indented example read as a chore |
| `Panels.test_nothing_waits_on_a_quiet_day` | every planned service a deploy waiting (first try passed, because the test had no services: strengthened) |
| `Panels.test_timeline_newest_first_with_kinds` | oldest first |
| `Panels.test_links_with_their_dots` | a refused site shown as up |
| `Panels.test_log_tail_searches_and_redacts` | log lines not redacted |
| `Panels.test_redaction` | the `tskey-` pattern removed (first try passed through the `name=value` rule: a bare key case added) |
| `PhoneScreen.test_the_page_draws_and_nothing_is_wider_than_a_phone` | a tile's detail no longer wraps (the page grew to 685 px) |

The rest (local listener, the other identity cases, the fixture's own shape, the file on this PC) pass alongside those.

Console facts (`SL_FACT_FILTER='^P155_'`), each seen failing:

| Fact | Seen failing by |
|---|---|
| `P155_ARefreshBecomesTheStatusFileAndBothConsolesReadIt` (written, written over, schema 1, the TEST tile as `Get-AtAGlance` judges it, Python's `status_problems` accepts it, read back with its age, another schema refused) | a tile key changed; and the Replace with a plain `$null` again |
| `P155_TheConsolePaintsItsTilesFromTheStatusFileAtItsStart` | any age painted (a file eleven minutes old must be left alone) |
| `P155_TheConsolesOwnRefreshWritesTheStatusFile` (and nothing from a capture) | the refresh writes no file |
| `P155_ThePromptsSummaryAndSizeAreRead` | the Summary line not read |
| `P155_TheCollectorScriptWritesTheStatusFile` | the collector writes as the console |
| `P155_TheWebConsoleListensOnTheLoopbackOnlyAndPublishesNothing` | any bind accepted |

Full suites:

- **Console facts** (Windows PowerShell 5.1): the run on the near-final code, **368 facts, 363 passed, 5 failed**, the
  same five that failed before P154 and P155 (P83 x2, P101 x2, P107: this PC is in Haven mode since the ops cutover;
  P133's and P154's notes). The rerun on the final code: **368 facts, 362 passed, 6 failed**: those five, plus
  `P84_TheUOLookAddsUnderASecondToTheStart` ("UO adds 1038 ms", a timing limit of 1000), which ran while I was also
  running the Python suites and the commit dry run. Run alone right after, it **passed three times out of three**. Load,
  not a change: P155 does not touch the form's build. Every `P133_*`, `P154_*` and `P155_*` fact passed in both runs.
  Not green, for the same reason as P154 (Deviations there).
- **Web console:** 23 tests, OK.
- **shard-migration tools:** 99 tests, the same 2 failures as before (`test_play_who.RealFiles` on the play-test data in
  `testing\`); P155 reads that data but does not change it.

## Deviations and decisions for Chase

1. **The real page at `https://uoconsole...` was not loaded**: there is no auth key yet (For Chase, step 1). Everything
   up to the sidecar was proved on this PC; the sidecar's Serve config has not been run.
2. **Anything already running on the game PC is trusted as Chase**, as the PowerShell console is: a program on the PC
   can use `:8095`, and a container on the PC's Docker can reach `:8096` and send a forged `Tailscale-User-Login`. That
   is acceptable for a read-only phase 1. **Phase 2 (actions) must close it**, by having the console ask the sidecar's
   own Tailscale (`tailscale whois` on the peer, through its local API) rather than trust a header, or by a secret only
   the sidecar holds.
3. **The allowed login** defaults to whoever this PC's Tailscale is signed in as (read at run time, cached 5 minutes),
   because the login is an email address and both repos are public. To add someone (your daughter), put
   `{"allowedLogins": ["you@...", "her@..."]}` in `D:\UO\web-console\settings.json`.
4. **The status file's DNS and websites tiles** are only as fresh as their writer's probes (the console's, or the
   collector's every 30 s). The collector also emails a shard's new console question once, as the console's refresh
   does (cc-P106); the sent list is shared, so the two never both send one.
5. **The collector runs only while the web console runs** (it is the web console's child). With neither console open,
   the file goes stale and the page says how old it is.
6. **Play tests**: the game PC's `testing\play-tests.json` is the mirror of Haven's (refreshed at each commit since
   the cutover), so Needs you can be up to a commit behind the play-test page. 85 items are marked yours today; the
   inbox shows ten and a count.
7. `notes\chores.md` is new and empty: the overseer adds one `- [ ] ...` line per chore.
8. No art yet in `scripts\console-art`, so the page draws its stand-ins (crystals as coloured diamonds, a plain stone
   colour). Art dropped into the slots shows up without a change here.

## For Chase

1. **Make the auth key** (Tailscale admin console):
   - Access controls: add a tag owner, `"tagOwners": { "tag:uoconsole": ["autogroup:admin"] }`, and save.
   - Settings > Keys > **Generate auth key**: Reusable off, Ephemeral off, Tags on with **tag:uoconsole**, any
     expiry (it is only used for the first login). Copy it.
   - On the game PC, make `D:\UO\web-console\tailscale.env` holding one line, `TS_AUTHKEY=<the key>`. Notepad is fine.
     It stays outside git and is never printed.
2. **Install** (PowerShell, on the game PC): `D:\ShatteredLegacy\web-console\Install-WebConsole.ps1 -DryRun` to see the
   plan, then `D:\ShatteredLegacy\web-console\Install-WebConsole.ps1 -Tailscale`. It registers the task **SL web console**
   (starts at your logon), starts it, checks `http://127.0.0.1:8095/`, and starts the `uoconsole` container.
3. **The address:** `https://uoconsole.tail81098d.ts.net/` from your phone or the work PC (Tailscale on); on the game PC
   itself also `http://127.0.0.1:8095/`. Anyone else on the tailnet gets "not allowed".
4. **What phase 1 shows:** Today (every tile and light, the Golem, what needs you, the last few events), the Golem (state
   and reason, when it is ready, what is running, the queue with each Summary, model and size, recent finished prompts,
   night shift, self-wake, usage), Needs you, the Timeline, Logs (pick one, search, tail) and Links (with up dots).
   It changes nothing: no buttons yet.
5. **Phase 2 (Golem controls)** adds the Golem's buttons to the page: wake, poke, rest, wrap up, find a stopping point,
   long run, night shift, Run next and the away-mode switch, each with the typed confirm checked on the server, the action
   log, and the identity check hardened (Deviation 2).
6. To remove it: `Install-WebConsole.ps1 -Uninstall` (add `-Purge` to drop the node's state, then remove the machine in
   the Tailscale admin console).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

No file over 5 MB added (`find -size +5M` on everything new: none). The tests' `__pycache__` folders are git-ignored
(`.gitignore:76:__pycache__/`, proved with `git check-ignore -v`); the status file and its request file are in the
git-ignored `scripts\shard-console-cache\` (`.gitignore:90`). Scratch (probes, screenshots, break scripts) is in the
session scratchpad, outside both repos.

P155 DONE
