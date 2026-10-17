# cc-P133: Haven intranet dashboard, finished: Tailscale only, every service, live up/down

2026-10-17. Opus. Finishes P107 (ops pages), P109 (print queue) and P110 (mega dashboard) to Chase's decisions of
2026-10-15 12:03: **Tailscale only**, and **up or down on everything**. Built over two sessions: the first was closed
before it wrote these notes; the second (this one) found its work in both working trees, checked it, ran the proofs
again, fixed two test pins, and wrote this. Nothing here has reached Haven: CC never connects to it (P107's rule kept).

## Headlines

- **One inventory, `D:\ShatteredLegacy\docker\haven\services.json`: 29 services, 34 tiles** (counted from the file,
  2026-10-17), one entry per service on Haven and per shard service on the game PC, plus the Hostinger store. Every entry
  has host, container, image, ports, compose path, volumes, env **names**, secrets (where they live, never values),
  health URL, dependsOn and neededBy (kept as mirrors and checked both ways), backup paths, owner, and a `verified` line
  saying where each fact came from. Spoolman, Prometheus, Grafana and Haven's Portainer are marked *Chase's notes* or
  *planned*: their names, ports and volumes are unverified until the first Discover prints them.
- **The dashboard is generated from it** (`docker\haven\Build-HavenDashboard.ps1`), so the tiles and the inventory cannot
  drift: a console fact fails if `services.yaml` or `settings.yaml` differ from what the inventory makes. Five sections,
  in order: **Sunflower, Filament, Monitoring, Ultima Online / Shattered Legacy, Admin**. Homepage (P110's), not Homarr.
- **Up or down on every tile**: Haven's containers through the read-only Docker proxy; web services by `siteMonitor`;
  the game PC's services from the snapshot it already pushes every minute, now carrying a `services` list read from the
  inventory, and served by Haven's `/api/gamepc` as `up.<key>`: `Up`, `Down: <why>`, or **`Game PC offline since <time>`**
  for every one when the game PC sleeps (`tools/opsdata.py`). A running container the inventory does not list still gets
  a tile, in Admin, named "(not in the inventory)".
- **Tailscale only.** Every compose of ours publishes on Haven's LAN address and loopback, never `0.0.0.0`; **Tailscale
  Serve** (never Funnel) forwards the tailnet's :80 to the dashboard, :8093 to the ops page, :8787 to the print queue,
  each to a loopback port, set by the Mega dashboard deploy from `services.json`. The Cloudflare tunnel and Access plan
  (P89's H4) is gone from the ops pages' next steps. NPM, the public website and the wiki are untouched.
- **Discovery first.** The deploy's Discover now prints every container (`docker ps -a`: name, state, status, image,
  ports, compose folder), every listening port (`ss -tlnp`), and Tailscale (address, operator, Serve now), checks them
  against the inventory in the plan, and keeps the whole output in `D:\UO\haven-ops\discovery-latest.txt` (outside both
  repos). A console fact fails while a running container in any discovery on record has no inventory entry.
- **Print queue push** (item 5): P109 already did it the Sunflower chat's way: a **new** key made on Haven (Chase's key
  never copied), Linux paths and `python3` in the image, and a 60 s debounce `threading.Timer` after the last change
  (not a loop). P133 adds the order: **the key is proved from Haven (`ssh sunflower-live true`, inside the image) before
  the tower copy is stopped**; if Hostinger refuses it nothing moves and the tower keeps pushing. After the move the
  first push is made from Haven and checked, so the two never push at once.
- **Runbook** `notes\haven-runbook.md` (new, 328 lines): machines and a diagram, deploy buttons, tokens and keys (where
  each is made, never a value), what must never move or be exposed, the general move steps, a section per service
  (restart, data, backup and restore, how to move it), backup paths, and a "Changed on" log.
- **Rule for later prompts**: one section in both repos' `AGENTS.md`: any change to a Haven or game PC service updates
  `services.json` and the runbook (with a dated "Changed on" line) in the same prompt, and regenerates the dashboard.

## What changed

D:\ShatteredLegacy (uncommitted):

| File | Change |
|---|---|
| `docker/haven/services.json` (new) | The inventory: `schema`, `hosts` (Haven, game PC, Hostinger with LAN and tailnet names), `sections`, `tailscaleServe` (three loopback targets), 29 `services` |
| `docker/haven/HavenInventory.ps1` (new) | `Read-HavenInventory` (required fields, owners, hosts, sections, dependsOn/neededBy mirrored) :27; the YAML writer (every string double-quoted) :60; `ConvertTo-HomepageServices` :132 and `ConvertTo-HomepageSettings` :157; `ConvertFrom-HavenDiscovery` (three shapes: this deploy's, P110's, a plain `docker ps` table) :171; `Test-HavenInventoryCoverage` :222. Pure functions |
| `docker/haven/Build-HavenDashboard.ps1` (new) | Writes `services.yaml` and `settings.yaml` from the inventory; `-Check` exits 1 when they differ; `-Discovery` adds tiles for unlisted containers; exit 2 when the inventory is unsound |
| `docker/haven/discovery/haven-2026-09-28.txt`, `haven-2026-09-29.txt` (new) | The two real Haven discoveries on record (container tables only), so the coverage fact has real input |
| `docker/dashboard/haven/config/services.yaml`, `settings.yaml` | Now generated (header says so); five sections; P110's `HOMEPAGE_VAR_SPOOLMAN_URL` and `GRAPHS_URL` placeholders gone |
| `docker/dashboard/haven/config/custom.js` | +3 lines: the menu's tailnet link |
| `docker/dashboard/haven/docker-compose.yml` | Binds `${DASH_BIND:-192.168.1.61}` and `${DASH_LOOP_BIND:-127.0.0.1}:${DASH_LOOP_PORT:-3000}` (was `0.0.0.0`) :20-21; allowed hosts gain the tailnet name and address :32; env comment names the four `HOMEPAGE_VAR_*` |
| `docker/dashboard/haven/Deploy-MegaDashboard.ps1` | Reads and checks the inventory :73; `Get-ServePlan` (loopback targets only) :146; Discover prints containers, ports, Tailscale :159 and keeps the file :179; inventory check in the plan :186; config built from `services.json` :226; backup before replace :230; `dashboard.env` gets missing names empty, never a value :239; Serve from `tailscaleServe`, skipped where nothing answers :269; never `0.0.0.0`, never Funnel |
| `docker/ops/docker-compose.yml` | Loopback port for Serve `${LOOP_BIND:-127.0.0.1}:${LOOP_PAGE_PORT:-8093}:8000` :50; header: Tailscale only, H4 dropped |
| `docker/ops/Deploy-HavenOps.ps1` | `-LoopPort` (proof: PagePort + 1000) :47, passed as `LOOP_PAGE_PORT` :117-118 |
| `docker/ops/README.md` | Next steps: Tailscale Serve instead of Cloudflare Access |
| `docker/test-queue/html/nav.js` | `tailnetUrl` on the Dashboard row and `onTailnet()`: reached by a `.ts.net` name, the menu links the tailnet address :26-28, :73-79 |
| `scripts/Publish-GamePcSnapshot.ps1` | Reads the game PC keys from `services.json` and sends `services: {key: {up, detail}}` :71-86, :95-111, :118 |
| `scripts/tests/Shard-Console.Tests.ps1` | Ten `P133_*` facts (below); P110's pinned-groups fact updated to the five sections |
| `AGENTS.md` | The one-inventory rule :65-69 |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.17`, one `### Staff` line; VERSION 2026.10.16.6 -> 2026.10.17 |

D:\UO\shard-migration (uncommitted):

| File | Change |
|---|---|
| `notes/haven-runbook.md` (new) | The runbook |
| `notes/cc-P133-haven-intranet-dashboard.md` (new) | This file |
| `tools/opsdata.py` | `gamepc_status` returns `up` per service, "Game PC offline since ..." when stale :140-166 |
| `tools/tests/test_haven_h1.py` | `test_up_reads_each_service_and_says_offline_when_the_game_pc_sleeps` :214; the nav.js pin updated for `tailnetUrl` :473-476 |
| `AGENTS.md` | The same rule :391-395 |

C:\dev\sunflower\print-queue (not a git repo with commits; P109 left it uncommitted and this does too):
`haven/Deploy-PrintQueue.ps1`: step 5b in the plan; `Check the key from Haven` :266 before `Move the data` :275; the
first push from Haven after the move, checked :314.

Folders created: `D:\ShatteredLegacy\docker\haven\` and `docker\haven\discovery\`. Scratch: `D:\UO\scratch-p133\`
(proofs; deleted at the end, see below).

## Tests

**Console facts** (`scripts\tests\Shard-Console.Tests.ps1`). Before P133 (the first session's baseline, kept in its
scratch folder): **346 facts, 340 passed, 6 failed** (P83 x2, P101 x2, P107_LinksAndSites..., P110_TheHavenHomepage...).
After, the full suite run on 2026-10-17: **356 facts, 351 passed, 5 failed**. The ten new ones all pass, P110's is
fixed, and the five failures are the same pre-existing set. All five come from this PC being in Haven mode since the ops
cutover (`D:\UO\haven-ops\state.json` says `haven`), so the console's real config shows Haven's links where those facts
expect this PC's (`expected [http://localhost:8093/] but got [http://192.168.1.61:8093/]`, `expected [pc] but got [haven]`).
Not P133's; see Deviations.

The ten new facts, each **seen failing** by breaking one thing, running that fact alone (`SL_FACT_FILTER`), then
restoring the bytes and checking the SHA-256 (all ten restored identical):

| Fact | Broken by | Result |
|---|---|---|
| `P133_TheInventoryIsSoundAndHoldsNamesNeverSecretValues` | `"password": "hunter2"` added to `services.json` | FAIL, restored |
| `P133_TheDashboardIsGeneratedFromTheInventoryWithEverySectionAndTile` | a hand-added tile in `services.yaml` | FAIL (`expected [# GENERATED ...`), restored |
| `P133_EveryTileShowsUpOrDown` | every `siteMonitor` renamed | FAIL, restored. (First try renamed only one, on a tile that also has a container dot: it passed, correctly) |
| `P133_WidgetsThatNeedAKeyReadItFromTheEnvironmentNeverTheFile` | `{{HOMEPAGE_VAR_GRAFANA_TOKEN}}` replaced by a literal | FAIL, restored |
| `P133_NoComposeOfOursPublishesOnAPublicInterface` | the dashboard's bind default set to `0.0.0.0` | FAIL, restored |
| `P133_TheDiscoveryIsParsedIntoTilesAndEveryRunningContainerIsInTheInventory` | a discovery file with a running `stray-box` | FAIL (`expected [] but got [stray-box]`), file removed |
| `P133_TheDeployServesOnTheTailnetSavesItsDiscoveryAndBuildsFromTheInventory` | both `restart: unless-stopped` in the ops compose set to `"no"` | FAIL, restored. (Changing one of the two passed: the fact asks for at least one) |
| `P133_ThePrintQueueProvesItsKeyFromHavenBeforeTheTowerStops` | the key-check step renamed | FAIL, restored |
| `P133_TheSnapshotReportsEveryGamePcServiceTheDashboardShows` | `services` dropped from the snapshot | FAIL, restored. (First try mangled the path string, which still matched the fact's regex and passed: my mutation was weak, not the fact) |
| `P133_TheRunbookAndTheRuleKeepTheInventoryAndTheDocsInStep` | `## Changed on` renamed in the runbook | FAIL, restored |

Four facts parse the generated YAML with **Homepage's own js-yaml from the pinned image** (`docker run ...
homepage:v1.13.1 node`), so they need Docker running.

**Python** (`tools/tests`): `test_haven_h1` 14 tests OK. The new
`test_up_reads_each_service_and_says_offline_when_the_game_pc_sleeps` was seen failing (the offline line replaced by
`"Up"` in `opsdata.py`, restored by hash). The nav.js pin (`Menu.test_nav_js_...`) failed on P133's `tailnetUrl` before
I updated it; that pin is the one P110 missed and P112 fixed, and it was missed again here at first. Whole folder: **99 tests, 2
failures**, both `test_play_who.RealFiles` on the real play-test data in `testing\` (P115-P122 items with no Who, and
P122-2 with no check/do steps). Not P133's.

## Proofs (this PC, scratch, nothing reached Haven or Hostinger)

Scratch root `D:\UO\scratch-p133\` (outside both repos), stand-in containers for Haven's stale Homepage and this PC's
`sl-dashboard`, a stand-in `tailscale` on the PATH that only logs its calls, a stub sshd for Hostinger. Both deploy scripts
ran with `-Local`, which refuses any root not named scratch or proof and the real names.

**Mega dashboard** (`Deploy-MegaDashboard.ps1 -Local`, ports 18300 LAN stand-in and 18301 loopback):

| Check | Result |
|---|---|
| `-Mode Deploy -DryRun` | Discover printed containers, ports, Tailscale; inventory check named the unlisted ones (this PC's own containers, expected here) and the absent ones; nine-step plan; `DRY RUN: stopping here; nothing was changed.` |
| `-Mode Deploy -Yes` | backed up to `backup-20261017-134244`; config built from `services.json`; `dashboard.env`: the ops token copied from the scratch `ops.env` (`set`), Grafana and Portainer key `EMPTY`, no value printed; stale stand-in stopped; Homepage `Up (healthy)` on `127.0.0.1:18300` and `127.0.0.1:18301` only; `Homepage answers ... with the five sections`; Serve `--bg --http=80 http://127.0.0.1:18301` called, :8093 and :8787 **skipped because nothing answered**; the page over the "tailnet" port answered; PC stand-in stopped. Exit 0 |
| The page | `GET /` has Sunflower, Filament, Monitoring, Ultima Online / Shattered Legacy, Admin (all True) |
| `-Mode Rollback -Yes` | Homepage and proxy stopped; `serve --http=80 off`; both stand-ins started again. Exit 0 |
| Compose files | `docker compose config` on Haven's defaults: dashboard `192.168.1.61` + `127.0.0.1`; ops `192.168.1.61` x2 + `127.0.0.1`; print queue `192.168.1.61` + `127.0.0.1`. No `0.0.0.0`; `restart: unless-stopped` on every long-running service |

**Print queue** (`Deploy-PrintQueue.ps1 -Local`, port 18787, scratch game PC folder, stub sshd on `127.0.0.1:12222`
with its host key pinned):

| Check | Result |
|---|---|
| Deploy, key **not** added in "Hostinger" | key made, public half printed; host key check passed; `Permission denied (publickey...)`; **`REFUSED: Hostinger does not accept the container's key yet ... the tower copy keeps the queue and keeps pushing.`** Exit 1. The PC's `queue.json` hash unchanged, not renamed; Haven's `data` empty |
| Deploy, key added | `KEY-OK`, `Hostinger accepts the key from Haven`; then the move: 1 file copied and checked by SHA-256, `Haven's page serves all 3 orders`, PC data renamed `data.moved-20261017`; **`first push from Haven: OK updated (proof stub)`**, and the stub logged `wp eval-file .../push.php`. Exit 0 |
| Rollback | 2 files back, SHA-256 checked, 3 orders; container stopped; Haven's data set aside; the game PC stand-in answered again. Exit 0 |

One proof-harness bug of mine: the first "key added" run was still refused because PowerShell's pipe put a byte-order
mark in front of the key in the stub's `authorized_keys`. Rewritten from Git Bash, it passed. That was the harness, not
the deploy: on Haven the key is pasted into hPanel by hand.

Afterwards: all six proof containers, both networks, the images `sunflower-print-queue:local` and `pq-proof-stub-img`,
the game PC stand-in server (on the scratch port 18788, started by the proof rollback at 13:45:51), and the whole scratch
folder (with its copy of queue data) were removed.

## Deviations and decisions for Chase

1. **Two steps were denied automatically in the unattended run, and I did not retry them another way:**
   - **Reading `D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1` with the Read tool** so I could edit
     `New-P107Config` (around :4767). Why: since the cutover, `Get-ConsoleConfig` applies this PC's real mode (`haven`),
     so `New-P107Config ''` still has Haven's sites, and `P107_LinksAndSites...` fails with `expected [pc] but got
     [haven]`. The fix I wanted, test-only, right after the `if ($Mode) { ... }` line:
     `$c.Websites = ConvertFrom-WebsiteConfig ([IO.File]::ReadAllText($c.WebsitesFile)) $repo` (re-parse the sites before
     `Set-OpsSites` applies the mode it was given). It was failing before P133 too. P83 x2 and P101 x2 fail the same way
     (real Haven mode leaking into facts that expect this PC) and want the same kind of isolation.
   - **Reading `C:\dev\sunflower\print-queue\haven\Deploy-PrintQueue.ps1` around :320** to make the closing line
     "Until the key above is added in Hostinger, the page says in red ..." print only when the first push failed. It
     currently prints after a successful push too (seen in the proof). Cosmetic; the line above it says what really
     happened.
2. **Grafana's port is 3001 in the inventory, not 3000.** Chase's notes planned 3000, which is the dashboard's LAN port on
   Haven. Change `services.json` (entry `grafana`) if Grafana lands elsewhere.
3. **The dashboard on the tailnet is Tailscale Serve's :80, while NPM holds `0.0.0.0:80` on Haven.** Serve is expected to
   answer on the tailnet address first, because tailscaled handles Serve ports itself before traffic reaches the
   kernel. That is *unverified on Haven*: the proof's `tailscale` was a stand-in. The deploy checks
   `http://haven.tail81098d.ts.net/` for this dashboard's content (not just any 200), and says so in yellow if NPM's page
   answers instead. If that happens, set `tailscaleServe` port 80 to another port (8080, say) in `services.json`, run
   Build-HavenDashboard, and deploy again.
4. **Spoolman, Prometheus, Grafana and Haven's Portainer** are in the inventory from Chase's notes (names, ports, volumes
   unverified). If Discover finds them running under other names, the plan says so ("in the inventory, not on Haven"
   plus "RUNNING ON HAVEN, NOT IN THE INVENTORY"). Correct `services.json` and the runbook then. Spoolman probably
   listens on all interfaces today (Chase's note gives `:7912` on the tailnet name). It is not ours, so it is untouched
   and only recorded; if it should be tailnet-only, that is a change to its own compose.
5. **The print queue folder `C:\dev\sunflower\print-queue` has no commits** (P109 left it uncommitted and so does this).
   `Commit-ShardWork.ps1` does not cover it.
6. Item 5 (the WordPress push) needed no rework: P109 already makes a new key on Haven, uses Linux paths and `python3`,
   and pushes on a 60 s debounce timer, not a loop. P133 only added the key check before the move and the checked first
   push after it.
7. `docker\haven\discovery\` holds the two real Haven discoveries on record (container tables only, no secrets), so the
   coverage fact has real input in git. The newest live discovery stays out of git in
   `D:\UO\haven-ops\discovery-latest.txt`, and the same fact reads it once a deploy has written it.

## For Chase

All buttons are on the Shard Console's **Websites** tab, after the phrase `deploy to haven`. Each starts with a
read-only Discover of Haven, prints its plan, and changes nothing until you type its word.

1. **Ops pages: deploy** (word `deploy`). Since the cutover this recreates the page with the new compose, which adds
   the loopback port `127.0.0.1:8093` that Tailscale Serve forwards to. Asks nothing new.
2. **Mega dashboard: deploy** (word `deploy`). Read the plan first: it lists every container on Haven and any the
   inventory lacks. If it says Serve needs permission, run once
   `ssh -t chase@192.168.1.61 "sudo tailscale set --operator=chase"` and click again. It backs up `~/sl-home`, builds the
   tiles from `services.json`, starts Homepage on `192.168.1.61:3000` and loopback, sets Serve (:80 dashboard, :8093 ops
   page, :8787 once the print queue answers), and stops this PC's old `sl-dashboard`. Rollback: **Mega dashboard: roll
   back** (word `roll back`).
3. **Tokens** (never send them to anyone, never put them in git):
   - Grafana (once installed): Administration > Users and access > **Service accounts** > Add, name `homepage`, role
     **Viewer** > Add service account token > copy.
   - Portainer on Haven: your user (top right) > **My account** > **Access tokens** > Add, name `homepage` > copy. The
     **environment ID** is the number after `/endpoints/` when you click Haven's environment under Environments.
   - Paste them: `ssh -t chase@192.168.1.61 "nano ~/sl-home/dashboard.env"`, put each value after the `=` of
     `HOMEPAGE_VAR_GRAFANA_TOKEN`, `HOMEPAGE_VAR_PORTAINER_KEY`, `HOMEPAGE_VAR_PORTAINER_ENV`, save, then click Mega
     dashboard: deploy again (it keeps every value).
4. **Print queue: deploy** (word `deploy`). The first click makes the container's **own** key on Haven and prints its
   public half, then refuses to move anything because Hostinger does not know the key yet. The tower keeps pushing.
   Add that public half in **hPanel > Advanced > SSH Access > SSH keys > Add SSH key**, name it "print queue on Haven",
   then click **Print queue: deploy** again. This time it proves the key from Haven, stops the tower copy, moves the
   data (checked), and makes the first push from Haven.
5. **When to turn off the tower's print queue:** the deploy in step 4 does it, and only after Haven's key works. Nothing
   to do by hand. If the first push from Haven fails, the deploy says so in red; **Print queue: roll back** puts the
   tower copy back.
6. Click **Mega dashboard: deploy** once more after step 4, so Serve adds :8787.
7. **Final URLs** (tailnet only; at home the LAN ones work too):
   - Dashboard `http://haven.tail81098d.ts.net/` (LAN `http://192.168.1.61:3000/`)
   - Ops pages `http://haven.tail81098d.ts.net:8093/` and `/status` (LAN `http://192.168.1.61:8093/`)
   - Print queue `http://haven.tail81098d.ts.net:8787/` (LAN `http://192.168.1.61:8787/`)
   - Spoolman `http://haven.tail81098d.ts.net:7912/`; Vaultwarden as now
8. **Add to Haven's backups:** `/home/chase/sl-home/dashboard.env`; `/home/chase/sl-ops/data`, `/home/chase/sl-ops/ops.env`,
   `/home/chase/sl-ops/keys`; `/home/chase/sunflower-print-queue/data` and `/keys`; Spoolman's data volume (Discover
   prints its name); `/opt/monitoring` once Prometheus and Grafana exist; Docker volumes `proxy_npm_data`,
   `proxy_npm_letsencrypt`, `sl-wiki-storage` and Portainer's; Vaultwarden's data (as now); `/home/chase/clients/kevins-parts`
   and a dump of its database; `/var/lib/tailscale` (or just log in again after a rebuild). The runbook keeps this list.
9. Review the two auto-denied fixes in Deviations 1 (the P107 test isolation and the print queue's closing line). Each is
   one line.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

Neither repo BLOCKED. The docs repo's pending list also has `testing/SUMMARY.md`, `testing/play-tests.json` (the
mirror refresh) and `testing/bot-runs/2026-10-17-0130/` (the bot's output), which are machine output and not mine. No file
over 5 MB was added (`find -size +5M` on everything new: none). Scratch was outside both repos and is deleted.

P133 DONE
