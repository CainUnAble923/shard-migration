# cc-P110: One mega dashboard on Haven (Shattered Legacy + Sunflower + home lab)

2026-10-14. Prompt: `D:\UO\cc-prompts\cc-P110-haven-mega-dashboard.md`. P89's H5, widened. Built and proved on this PC.
**Nothing was deployed to Haven and nothing connected to it.** The game PC's running `sl-dashboard` was never touched.

## Decisions for Chase (the question first)

1. **Where is "the Sunflower dashboard", the one with Spoolman and the graphing app? I could not find it.** Searched,
   all with nothing found:
   - this PC's Docker: every container, image and volume for `spool|grafana|influx|prometheus|homepage|dash|chart|graph`
     (only `sl-dashboard`, the shard's Homepage);
   - files to depth 4 under `C:\dev`, `D:\Websites`, `D:\Servers`, `D:\UO`, `D:\`, Documents, Desktop, Downloads,
     OneDrive, ProgramData and Program Files for `spoolman|grafana|influx|prometheus|homepage|services.yaml` (only
     unrelated hits: Orca-Flashforge's own `homepage` web folder, an old app's `HomePage.xaml`, the bot's checkout);
   - text in `C:\dev\sunflower`, shard-migration's notes and docs; running processes; listeners on Spoolman's and
     Grafana's usual ports (7912, 3001, 8086, 9090, 3030); the WSL distros (only `docker-desktop`);
   - Haven's old discovery output (`D:\UO\haven-migration\*.txt`): no Spoolman or graphing app.
   The one hint: **Orca-Flashforge is installed here**, so Spoolman (filament tracking) may run on another machine, a
   Pi, or the printer's own network. **The deploy's Discover prints Haven's running containers and ports and flags
   anything named like Spoolman or a graphing app** (`sunflower candidates:`), so the first click answers it for Haven.
   What is built: a marked Sunflower group with **Spoolman** and **Graphing app** tiles whose links come from
   `HOMEPAGE_VAR_SPOOLMAN_URL` and `HOMEPAGE_VAR_GRAPHS_URL` in Haven's `dashboard.env`. The deploy asks for both the
   first time (empty allowed); `-SetUrls` asks again. Homepage 1.13.1 ships a `spoolman` widget
   (`/app/src/widgets/spoolman` in the image; https://gethomepage.dev/widgets/services/spoolman/), left commented in
   `services.yaml` with how to turn it on. **Tell me the address and which graphing app, and the next prompt wires the
   widgets.** Nothing was installed.
2. **ATM10 shrank to one tile** (a link and a monitor on its status port) in Home lab. The old dashboard had six ATM10
   widgets reading the game PC; the server has been stopped for six weeks, and six error boxes would bury the rest.
   Say if you want them back.
3. **No "who's online" tile:** `status.json` was written only by the live shard, retired in P108.
4. **Kevin's Parts is not shown**, though the socket proxy could see it. It is a client's stack; say if you want its up
   or down there.
5. **Away from home:** Homepage allows only LAN names (`192.168.1.61:3000`, `haven:3000`). Tailscale is not on Haven
   yet (P89). When it is, add its name or IP to `DASH_ALLOWED_HOSTS` (the deploy's `-AllowedHosts`).
6. **`dashboard.shatteredlegacyuo.com` is not allowed** by the new Homepage (decision 10 is still open; it is public
   DNS). If NPM routes that name to a Homepage today, it stops working after the deploy, which is the safe side.

## Headlines

- **One Homepage on Haven, from `D:\ShatteredLegacy\docker\dashboard\haven\`**: compose project `sl-home`, container
  `sl-homepage` (`ghcr.io/gethomepage/homepage:v1.13.1`, pinned; the same image id as the `latest` the game PC runs),
  and `sl-homepage-dockerproxy` (`tecnativa/docker-socket-proxy:v0.4.1`, pinned): Haven's Docker read only, through
  the proxy (decision 7). Homepage itself never mounts the socket. Files in `~/sl-home` on Haven.
- **Three groups**:
  1. **Shattered Legacy:** Play tests, Ideas and Bug reports (counts from `/api/summary` on Haven's ops page), Shard
     status, Test shard (up or down from `shards.json` on 8092), **Game PC** and **Game PC containers** (from the
     snapshot, decision 6, through the ops token listener; the token comes from `dashboard.env`), Website, Wiki,
     **Public progress page** (renamed, decision 11), Art and script downloads.
  2. **Sunflower Custom Gifts:** Print queue (orders, printing, plates to print, lead-time page state; from a new
     counts-only `/api/summary` on the print queue), Spoolman, Graphing app (placeholders, decision 1), Live store,
     Dev store (LAN, the game PC's devstack on 8080: a red dot while it is not running, its usual state).
  3. **Home lab:** Haven's containers through the proxy (ops repo pull, downloads, this dashboard); Vaultwarden, NPM
     and the game PC's Portainer as links only; the status feed; ATM10.
- **P88's menu:** `custom.js` loads `nav.js` from the ops service on Haven (`192.168.1.61:8093`), the game PC's copy
  as fallback.
- **The deploy replaces Haven's stale Homepage** (stopped, not removed; `~/shattered-legacy` untouched) **and stops
  this PC's `sl-dashboard`** (not removed). Rollback starts both again. `docker\dashboard\README.md` now says which
  Homepage is real.
- **One click:** **Mega dashboard: deploy** and **Mega dashboard: roll back** on the Websites tab (P101's helper and
  allowlist; launchers in `D:\UO\haven-migration`), and a **Mega dashboard** site row. Discover first: Haven's running
  containers and listening ports, the stale Homepage, the env file, the ops token's presence, Sunflower candidates.
- **The menu's and the Console's Dashboard links now go to Haven** (`192.168.1.61:3000`). Haven's 3000 always has a
  Homepage: the stale one until the deploy, the real one after, the stale one after a rollback.
- **Proof:** deploy, page, widgets, token header, proxy limits, rollback and dry run, all on this PC with stand-ins
  (below). **Three bugs found by the proof**, fixed (below).
- Tests: 304 before (P109), **306 after**; two new P110 facts; five P101 facts and two link facts updated.

## What changed

**Shard repo `D:\ShatteredLegacy` (committed by the queue)**
- New `docker/dashboard/haven/`: `docker-compose.yml`; `Deploy-MegaDashboard.ps1` (216 lines: Discover, Deploy,
  Rollback, `-DryRun`, `-SetUrls`, refuses SYSTEM; `-Local` for the proof only, which refuses the name `sl-dashboard`
  for its stand-ins); `config/` (`settings.yaml`, `services.yaml` 299 lines, `docker.yaml`, `widgets.yaml`,
  `bookmarks.yaml`, `custom.js`, `custom.css`, `icons/shattered_legacy_logo.png` copied from `config/icons`).
- `docker/dashboard/README.md`: "Which Homepage is real" at the top; the old note kept below as history.
  `docker/dashboard/config` and its compose file are unchanged: they are the game PC's dashboard, live-mounted, and the
  rollback's config.
- `scripts/websites.json`: the Mega dashboard row and deploys `mega-dashboard`, `mega-dashboard-rollback`; the fixture
  re-copied.
- `scripts/Shard-Console.ps1`: `DashboardUrl` `:363` (Haven); the phrase `:840`; the dialog title `:858`; the two actions
  `:1099-1100`; tooltips `:1321-1322`; `links.dashboard`'s words `:3906`; the plan `:4075` and its log line `:4080`.
- `docker/test-queue/html/nav.js`: the menu's Dashboard entry is `192.168.1.61:3000` (P107 left it on the game PC
  "until H5"; this is H5). `dashboard.html` copies `nav.js` when `progress.py` runs at the commit.
- `scripts/tests/Shard-Console.Tests.ps1`: P110 facts `:5131`, `:5151`; updated below.
- `CHANGELOG.md` 2026.10.14.16 `### Staff`, `VERSION` 2026.10.14.16.

**`D:\UO\haven-migration` (not a repo):** `Deploy-MegaDashboard.ps1`, `Deploy-MegaDashboard-Rollback.ps1`.

**Sunflower repo `C:\dev\sunflower\print-queue` (uncommitted, like P109's work; still no commits there):**
`queue_server.py` gains `GET /api/summary`: active orders, openers left, plates to print (rounded up per order, as the
public page counts them; checked equal on the real data), counts by status, and the last push state. **Counts only, no
name, code or order detail.** On the real data: 6 orders, 28 plates, matching the lead-time snippet.

## Proof (this PC, scratch, nothing reaches Haven)

A scratch root stood in for `~/sl-home`; `dash-proof-stale` (an nginx holding the scratch port) stood in for Haven's
stale Homepage; `dash-proof-pc` for this PC's `sl-dashboard`; a scratch `ops.env` held a made-up token.
`Deploy-MegaDashboard.ps1 -Local -Yes`, port 18300, project `dash-proof`.

| Check | Result |
|---|---|
| Discover | printed the running containers and listening ports, `stale homepage: running`, `env file: no`, `ops token: yes`, `sunflower candidates: none`; changed nothing |
| Deploy | config copied; `dashboard.env` written (token copied server-side; the two URLs empty); stale stand-in stopped; Homepage and proxy up (healthy); page answers with the three groups; PC stand-in stopped. Exit 0 |
| YAML | all five files parsed by Homepage's own `js-yaml` inside the container (`services.yaml` 3 groups); Homepage's log shows no config error |
| Rendered groups (text dump below) | the three groups in order, every tile |
| Widgets from this PC | Test shard `Up`, probed seconds ago; Public progress page 21 open defects, 230 in reach; downloads 92/19/14/5 |
| Haven-only widgets (ops page on .61, the token listener, the print queue on .61) | Homepage's own collapsed "API Error Information" box; the page and every other tile unaffected |
| The token header | with the scratch copy pointed at a stub that answers only `Bearer <token>`: `Online`, last push, `P110` running, `2` queued, and the container list; the stub logged `auth ok` four times; a wrong token gets 401 |
| The print queue widget | pointed at a scratch print queue: `6` orders, `1` printing, `28` plates, `Not pushed yet` |
| The socket proxy from inside Homepage | `GET /containers/json` 200; `POST /containers/.../start` **403**; `GET /images/json` **403**; `GET /info` **403** |
| Rollback | the new pair stopped, the stale stand-in and the PC stand-in started again. Exit 0 |
| Dry run | `DRY RUN: stopping here; nothing was changed.`; the containers' states unchanged |
| A failed start (the first run, bug 1) | compose refused; the new one stopped, the stale stand-in **started again**, the PC stand-in untouched. Exit 1 |

Text dump of the rendered page (`get_page_text`, after the fix of bug 2; the API-error tiles are those that only work
on Haven):

```
Shattered Legacy: Play tests (container stats; API Error) | Ideas (API Error) | Bug reports (API Error) | Shard status |
  Test shard: Shard Test shard, State Up, Probed 5 seconds ago | Game PC (API Error) | Game PC containers (API Error) |
  Website (container stats) | Wiki (site monitor, container stats) | Public progress page: 21 open defects, 230 in reach |
  Art and script downloads: 92 art done, 19 to go, 14 scripts done, 5 nights left
Sunflower Custom Gifts: Print queue (container stats; API Error) | Spoolman | Graphing app | Live store (site monitor) |
  Dev store (site monitor)
Home lab: Ops pages repo pull | Downloads | This dashboard (container stats) | Password vault | Nginx Proxy Manager |
  Portainer (game PC) | Status feed (site monitor) | ATM10 Minecraft (site monitor)
Menu on top: Play tests, Shard status, Dashboard. Title: "Haven - Shattered Legacy, Sunflower and home lab".
```

Afterwards the proof containers, network, both stubs and the scratch folder (with its copy of the print queue data)
were removed. `sl-dashboard` on this PC: `running`, as before.

**Not proved here:** the run on Haven itself (ssh, `ss -ltn`, the real stale container, Haven's socket, the real ops
token and snapshot). That is your click.

## Bugs the proof found (all fixed before the final run)

1. **A byte-order mark in `dashboard.env`.** In this session's PowerShell, text piped into `bash` gained a UTF-8 BOM,
   which made the second line's name `\ufeffHOMEPAGE_VAR_SPOOLMAN_URL`; compose refused. A plain `powershell.exe` (how
   the Console runs deploys) pipes us-ascii with no mark (checked), so a real run would not have hit it, but the
   script now pins `$OutputEncoding` and strips a mark on the receiving side with `sed`. **The same piping pattern is in
   P107's `Deploy-HavenOps.ps1` (the token into `ops.env`)**; it is safe from the Console for the same reason, but
   worth the same `sed` when someone next touches it.
2. **Homepage 1.13.1 served its sample page** ("My First Group", stock bookmarks) though `/api/services` returned this
   config: the image ships a pre-built page and rebuilds it only when a browser sees the config hash change. The
   deploy now calls `/api/revalidate` and checks the page carries "Sunflower Custom Gifts" before calling it up.
3. **"Site updated: 57 years ago"** on the print queue tile: a null last push formatted as a date. The tile shows the
   push state instead (Updated, Push failing, Not pushed yet).

## Tests

`scripts\tests\Shard-Console.Tests.ps1`, full run: **306 facts, 304 passed, 2 failed.**
- `P107_TheSnapshotSendsNothingBeforeTheCutoverAndDryRunPrintsItsJson`: fails in every run here since the `SL game PC
  snapshot` task was installed (P108 notes).
- `P84_TheUOLookAddsUnderASecondToTheStart`: a timing fact (1,306 ms against a 1,000 ms limit in the full run). Run
  in its own group afterwards it **passed twice**; its own comment says a build swings by a second on a busy PC. Not
  caused by anything here as far as I can tell (two more buttons), but I did not prove that.
- **New:** `P110_TheMegaDashboardDeploysAreAllowlistedAndRunOnlyTheirLaunchers` (the row, both launchers run only their
  mode, both plans confirm/window/log with `deploy to haven` and pass the safety check, tooltips, the dialog title) and
  `P110_TheHavenHomepageIsPinnedLanOnlyAndReadsDockerOnlyThroughTheProxy` (both images pinned; Homepage never mounts
  the socket; the proxy containers-only, no POST, read-only; LAN names only in `HOMEPAGE_ALLOWED_HOSTS`; one Docker,
  Haven's; the three groups; decision 11; no `server: my-docker`; the token and URLs from `dashboard.env`; SYSTEM refused,
  dry run, Discover default; Discover prints containers and ports; the revalidate and its check; the proof never stops
  a real `sl-dashboard`).
- **Seen failing:** with the real launcher set to `-Mode Rollback` and the Docker socket added to Homepage's volumes,
  both failed (`runs only its mode`; `Homepage itself never mounts the Docker socket`); restored, `cmp` identical, both
  passed.
- **Updated:** five P101 facts (`TheRealConfigReads...`, `AConfigMissingAField...`, `TheTileCountsTheSites...`,
  `DeployIsRefused...`, `TheTileAndTheTabAreBuiltAndDrawn`: nine sites, nine deploys, `9 OF 9`, `8 OF 9`, the allowlist
  text, the buttons and labels) and the shared all-up results table, `P83_TheLinksOpenTheTwoPagesAndNothingElse` (`links.dashboard` is `192.168.1.61:3000`), `P107_TheMenuFollowsTheHost...` (the menu's
  Dashboard is Haven's). The P101 ones were red on the new config first.

## For Chase

1. **Deploy:** Shard Console > Websites > **Mega dashboard: deploy**, type `deploy to haven`, read what Discover prints
   (Haven's containers, ports, and any Spoolman or graphing app), then type `deploy`. It asks for the Spoolman and
   graphing app URLs; Enter leaves them empty.
2. Best after the ops cutover (P107) and the print queue deploy (P109): before them, those tiles show "API Error"
   (the ops page and print queue are not on Haven yet) and the Game PC tiles say so too.
3. **No NPM host to add.** Never route Homepage through NPM or Cloudflare.
4. Commit the Sunflower repo when you commit P109's work there (`/api/summary` is in the same uncommitted change).
5. Back: **Mega dashboard: roll back** (types `roll back`).

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: the files above (`CHANGELOG.md`, `VERSION`, `docker/dashboard/README.md`, `docker/test-queue/html/nav.js`, the
console, its tests and fixture, `websites.json`, and the ten new files under `docker/dashboard/haven/`). docs: this note
and the play-test importer's `testing/SUMMARY.md` and `testing/play-tests.json` (machine output). No file over 5 MB (the
largest new one is the logo PNG, copied from `docker/dashboard/config/icons`). No secret in git: the ops token and the
Sunflower URLs exist only in `dashboard.env` on Haven, which the deploy writes.

P110 DONE
