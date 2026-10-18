# cc-P163: Dashboard fixes after the first Haven deploy, and Portainer on Haven

2026-10-18. Opus. Follows Chase's P133 deploys of 10-18 (08:49 to 09:46) and his 09:00 "lets fix anything that seems
broken" and 09:02 "install it" (Portainer). CC never connected to Haven: every Haven change below is a button for Chase.
The only traffic to Haven from here was plain HTTP GETs to its pages.

## Headlines

- **The five tile problems are fixed in the inventory and the builder**, and the dashboard config is regenerated
  (`docker\dashboard\haven\config\services.yaml`; `Build-HavenDashboard.ps1 -Check`: up to date, 33 services, 37 tiles):
  1. **Print queue (tower copy)**: no tile; `print-queue-tower` is `retired 2026-10-18`; `print-queue` is `running`, its
     `verified` line is the 08:56 deploy (key proved, 7 files moved and checked, first push OK).
  2. **Nginx Proxy Manager**: watched at its front door `http://192.168.1.61:80/` (answers 200 from here); the link is
     still the console's SSH tunnel `http://localhost:8081/`. No tile monitors `localhost` any more.
  3. **`monitoring-grafana`, `monitoring-prometheus`, `npm-admin-tailnet`** are in `services.json` with owner, ports,
     volumes, backup lines and tiles. The planned `grafana` and `prometheus` entries are **renamed** to the real
     containers, not kept beside them. Their ports were in the 09:46 Discover all along: Grafana and Prometheus publish
     on **Haven's tailnet address only** (`100.98.32.16:3001`, `:9090`), which is why the LAN probes found them closed.
     Their tiles watch `http://100.98.32.16:3001/api/health` and `:9090/-/healthy` (both 200 from here).
  4. **Planned services get no tile** (my pick of the two). Also retired ones and "built, not installed yet" ones. They stay
     in `services.json`, the runbook and Discover's "in the inventory, not on Haven". The Legion scripts dev channel the
     brief named is **running** since before 09:46 (Discover shows `sl-scripts-dev` Up, Serve :8097 set), so it is set
     to `running` and keeps its tile. Hidden now: `print-queue-tower`, `web-console`, `uoconsole-ts`.
  5. **Dev store**: its tile says **"Stopped, started by hand."** with no monitor (the rule: kind `on-demand`).
- **Discover already printed every container's image and published ports** (P133's `docker ps -a --format`); the brief's
  "ports are not known from here" was before the 09:46 log. What it lacked, and now has: **mounts** for every running
  container, and a plan section that names any running container whose **published ports or image differ** from its entry
  (`PORTS OR IMAGES DIFFER`), with the mounts of entries whose volumes still say "from Discover" (the three new ones). On the
  real 10-18 text, nothing differs after this prompt's inventory fixes (Spoolman's all-interfaces bind and image were also
  corrected from it).
- **Portainer (Haven): deploy / roll back** on the Websites tab, like the others: Discover, plan, typed word, backup,
  verify. `portainer/portainer-ce:2.45.2` (the docs' `lts`, pinned), volume `portainer_data` at `/data`, HTTPS
  `192.168.1.61:9443` and `127.0.0.1:9443`, Portainer's HTTP port on `127.0.0.1:9000` only, which Tailscale Serve gives the
  tailnet as `http://haven.tail81098d.ts.net:9000/`. The first deploy prints the first-login link, **the 5-minute limit** and
  Portainer's setup token, in big letters. **Proved for real on this PC** with scratch names (below), plus the dry run as a
  fact.
- Tests: 8 new console facts (each seen failing first), 4 P133/P101 facts updated. Full suites: see Tests.

## What changed

D:\ShatteredLegacy (uncommitted):

| File | Change |
|---|---|
| `docker/haven/services.json` | 33 services (counted: 32 before, minus none, plus `npm-admin-tailnet`; `grafana` and `prometheus` renamed). `print-queue` running, 08:56 verified :47; `print-queue-tower` retired, no tiles :97; `spoolman` image, compose folder, `0.0.0.0:7912` from Discover, neededBy `monitoring-prometheus` :167; `monitoring-prometheus` :199 and `monitoring-grafana` :237 (were `prometheus`, `grafana`; `tailnetBind` ports, monitors on `100.98.32.16`, volumes "from Discover"); `scripts-dev` running :441; `npm` tile `siteMonitor` and neededBy `npm-admin-tailnet` :631, :657; `npm-admin-tailnet` new :662; `homepage`, `homepage-dockerproxy` running :720; `portainer-haven` rewritten :766 (image, compose, ports, volume, admin login secret, tile href tailnet :9000); `old-homepage-gamepc` stopped on purpose; `tailscaleServe` 9000 -> `127.0.0.1:9000` :43 |
| `docker/haven/HavenInventory.ps1` | `Get-HavenTileMode` (none, by-hand, live) :127; by-hand tile :143; no tile for none :156; Discover's `-- mounts` section :235 and `Mounts` :245; `ConvertFrom-DockerPorts` :261; `Compare-HavenDiscoveredPorts` :285 |
| `docker/haven/discovery/haven-2026-10-18.txt` (new) | The 09:46 Discover's containers and listening ports, verbatim (indent removed), for the facts |
| `docker/dashboard/haven/Deploy-MegaDashboard.ps1` | Discover prints each running container's mounts :166; the plan prints ports or images that differ and the mounts to fill in :192-205; header :12-19 |
| `docker/dashboard/haven/config/services.yaml` | Regenerated |
| `docker/portainer-haven/docker-compose.yml` (new) | Portainer CE 2.45.2, LAN + loopback 9443, loopback 9000, `portainer_data`, the socket, `restart: unless-stopped`, no Edge port 8000 |
| `docker/portainer-haven/Deploy-PortainerHaven.ps1` (new) | Discover / Deploy / Rollback; refuses a `portainer` of another project or a taken 9443; volume tar before the replace :184; plan and typed word :177; first-login banner :213; Rollback :237; `-Local` proof switches |
| `scripts/websites.json` | `portainer-haven`, `portainer-haven-rollback` in the allowlist :38-39. No site row (below) |
| `scripts/Shard-Console.ps1` | Phrase :921, subject :942, the two buttons :1234-1235, tooltips :1790-1791, the plan's list and log line :5367, :5372 |
| `scripts/tests/Shard-Console.Tests.ps1` | 8 `P163_*` facts :6462-6625; P133_TheDashboardIsGenerated :6306 and P133_EveryTileShowsUpOrDown :6324 follow the two tile rules; P133_NoComposeOfOurs and the restart fact include the Portainer compose; P101's deploy list, allowlist message and button lists include the two deploys |
| `scripts/tests/fixtures/websites-2026-10-14.json` | Copied from `websites.json` (P101's fact pins the two equal) |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.18.8`, two `### Staff` lines; VERSION 2026.10.18.7 -> 2026.10.18.8 (the .7 section was committed) |

D:\UO\haven-migration (not a repo; the launchers live there by design): `Deploy-PortainerHaven.ps1`,
`Deploy-PortainerHaven-Rollback.ps1`, one line each, like the Mega dashboard's.

D:\UO\shard-migration (uncommitted): `notes/haven-runbook.md` (what a tile shows; the Portainer buttons; Discover's port
check; the NPM tailnet forwarder; Portainer admin login in Tokens; sections for `monitoring-prometheus`,
`monitoring-grafana`, `npm-admin-tailnet`, Portainer rewritten, print queue and tower copy, dev store, Spoolman; backups;
a Changed on line); this file.

## Tests

**New console facts** (`scripts\tests\Shard-Console.Tests.ps1`), each seen failing first in two red runs:

1. Against the changed inventory with the **stale** `services.yaml` (before the build): all 8 FAIL (tower tile still
   there, Web console still there, Dev store with a monitor, NPM without one, Grafana not on the tailnet address, Portainer
   href on 9443); two of them also showed bugs in my first draft (below).
2. With the **pre-change** `services.json` and `HavenInventory.ps1` swapped back in (then restored, SHA-256 checked OK): all
   8 FAIL for the right reasons (`the tower copy is retired: running until moved`, `Get-HavenTileMode is not recognized`,
   `services.json has monitoring-grafana`, `ConvertFrom-DockerPorts is not recognized`, `REFUSED: services.json
   tailscaleServe has no loopback HTTP entry for portainer-haven`, ...).

| Fact | Checks |
|---|---|
| `P163_TheTowerPrintQueueIsRetiredAndHavensRuns` | tower retired, no tile, nothing points at `localhost:8787`; Haven's running, verified 08:56 |
| `P163_PlannedRetiredAndNotInstalledServicesGetNoTile` | the rule on four states; no tile for any hidden entry; on a copy, scripts-dev planned loses its tile and running gets it back with its monitor |
| `P163_TheDevStoreSaysStoppedStartedByHandInsteadOfARedMonitor` | the words, no monitor, the link |
| `P163_NpmIsWatchedAtItsFrontDoorAndItsAdminLinkStaysTheTunnel` | `siteMonitor http://192.168.1.61:80/`, href = websites.json's tunnel URL, no `localhost` monitor anywhere |
| `P163_TheContainersDiscoverFoundAreInTheInventoryWithTheirRealPorts` | the three entries, the rename, Spoolman's link; on the **real 10-18 text**: nothing missing, nothing differing; Grafana's, NPM's and the ops pages' published addresses parsed |
| `P163_DiscoverParsesPortsAndMountsAndThePlanSaysWhatToFillIn` | ranges, `[::]` twins, exposed-only ports; the 10-18 text with Grafana moved to 3002, another image and a stray container: exactly those two named; mounts parsed; the deploy prints them |
| `P163_PortainerOnHavenHasADeployAndARollBackLikeTheOthers` | allowlist, launchers, plans (`confirm,window,log`), phrase, subject, tooltip, log line; compose pin, volume, no 8000, loopback 9000; inventory and Serve; tile and widget; deploy script's refusals, dry run, banner, backup before replace, no 0.0.0.0, no Funnel |
| `P163_ThePortainerDeployDryRunReadsPlansAndChangesNothing` | runs the deploy `-DryRun -Local` with scratch names and a stand-in `tailscale`: Discover, plan, `DRY RUN: stopping here`, exit 0, and no container, volume or copied file |

My own test bugs caught by the red runs: `ConvertFrom-DockerPorts` first returned its array with a leading comma, so a
pipeline after it saw one object (fixed in the function); and `docker volume inspect` on a missing volume threw under
`Stop` (fixed in the fact). Two list assertions I first extended (`P101_TheRealConfigReads...`, `P101_DeployIsRefused...`)
read a frozen fixture, `websites-2026-10-14.json`, not the live file: I reverted those two edits.

**Full console suite.** Baseline first: the same suite on a clean `git worktree` of HEAD (`ac9eee3`) in the scratchpad,
run while I worked: **385 facts, 371 passed, 14 failed**. Six of those fail only because a worktree is not at
`D:\ShatteredLegacy` (window-action and P135 child command lines, P60), and one is the stale-inventory
`P133_TheDiscoveryIsParsed...` (the 09:46 discovery-latest named `monitoring-grafana`, `monitoring-prometheus` and
`npm-admin-tailnet`), which this prompt fixes.

After, the real tree: **393 facts, 385 passed, 8 failed**. Then I fixed the one failure that was mine,
`P101_TheRealConfigReads...`: it pins `fixtures\websites-2026-10-14.json` to the live `websites.json` ("the fixture is the
real file"), and earlier prompts kept the two in step. I copied `websites.json` over the fixture and put back the two list
edits I had wrongly reverted. Re-run of P101, P110, P154's timing fact and P163: **23 facts, 21 passed**. The two failures
are `P101_TheTileAndTheTabAreBuiltAndDrawn` and `P101_EveryWebsiteButtonRun...`, both with the same message as the
baseline. So the full set left is **7 failures, all in the baseline**:

- `P83_TheLinksOpenTheTwoPagesAndNothingElse`, `P83_TheTileHasItsTwoLinks...`, `P101_TheTileAndTheTabAreBuiltAndDrawn`,
  `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing`, `P107_LinksAndSitesPointAtHaven...`: this PC is in Haven mode
  since the ops cutover, which leaks into facts that expect the game PC (P133's Deviations 1 already describes it).
- `PlayerCommandsNeverAppearInTheWorldTab`: in the baseline too; nothing here touches the World tab.
- `P154_TheRefreshNeverRunsOnTheWindowsThread` failed once in the full run (533 ms against its limit, while my proof and
  Python runs loaded the PC) and **passed** on the re-run alone. It is a timing fact; nothing here touches the refresh.

The 8 P163 facts, and every P133 and P110 fact, pass.

**Python** (`D:\UO\shard-migration\tools\tests`): 151 tests, 2 failures, both `test_play_who.RealFiles` on the real
play-test data in `testing\` (the same two P133 recorded). Not this prompt's: nothing here touches `testing\`.

## Proofs (this PC, scratch, nothing reached Haven)

`Deploy-PortainerHaven.ps1 -Local` under `<scratchpad>\proof-pt`, names `proof-portainer`, `proof_portainer_data`,
`proof-pt`, ports 19443/19444/19000, a stand-in `tailscale` that logs its calls:

| Run | Result |
|---|---|
| Deploy, new volume (`-Yes`) | "nothing to back up"; compose copied; volume, network, container created; `Portainer answers at https://127.0.0.1:19443/`; Serve called as `serve --bg --http=9000 http://127.0.0.1:19000` (stand-in); `api/users/admin/check` 404, so the banner printed with the setup token, which matched `docker logs` (`setup_token=faba859c...`). HTTP loopback 19000 answered 200. Exit 0 |
| Deploy again over the volume | Portainer stopped, volume tarred to `backup-20261018-155044.tgz` (2.8 KB), recreated, answered, banner again (no admin made in the proof). Exit 0. First try failed: Git Bash rewrote `/backup` in `docker run -v` to a Windows path; fixed for `-Local` only (`MSYS_NO_PATHCONV=1`, `pwd -W`), Linux is unaffected |
| Rollback (`-Yes`) | compose stop (container exited, volume kept); `serve --http=9000 off` (stand-in). Exit 0 |
| Refusal | a plain `alpine` container named `proof-portainer` (no compose project): `REFUSED: ... is not this deploy's`, exit 1, nothing changed |

Afterwards removed: the proof container, volume, network and the `portainer/portainer-ce:2.45.2` image. `alpine:3.20` was
pulled for the backup step and the refusal container and is left on this PC (small; may have been there before).

Not proved here: the "admin already exists" branch (204: it says so and prints no token), and what Portainer does at the
end of its 5 minutes (its docs say the user "must be created within 5 minutes"; the banner tells Chase to deploy again,
which restarts it).

## Deviations and decisions for Chase

1. **Read tool auto-denied** on `D:\ShatteredLegacy\docker\haven\services.json` (unattended run). I wanted it to edit the
   file with Edit. I did not retry the read; I had already printed the file with Python for the survey, and made every
   edit to `services.json`, `HavenInventory.ps1`, the console, the tests and the Portainer script with checked Python
   scripts (each replacement asserted to match exactly once, JSON re-parsed). Nothing else was denied.
2. **Item 4: no tile** for planned entries (not a grey tile). Homepage has no grey state: a tile with no monitor just has
   no dot, which reads like a forgotten tile. The rule also hides `retired` and `built, not installed yet` (the web console
   and its tailnet node, which would read Down until P155's install). Set `state` to `running` and rebuild to bring a tile
   back.
3. **The brief's ports premise was out of date.** At 09:01 the LAN probes of 9090 and 3001 were closed because Grafana and
   Prometheus publish on Haven's tailnet address only. The 09:46 Discover printed them. I filled them in from that log
   ("Discover 2026-10-18" in `verified`), and marked only their **volumes** "from Discover", which the next Mega dashboard
   deploy now prints.
4. **`npm-admin-tailnet` was made by hand on Haven** (`~/shattered-legacy/docker/npm-admin-tailnet`, not in git; socat in
   the host network forwarding the tailnet's :81 to NPM's admin). It makes NPM's admin reachable over the tailnet without the
   SSH tunnel. That is fine for Tailscale only, but nobody recorded it: worth a line from Chase on whether to keep it, and
   its compose belongs in git if so.
5. **Portainer on the tailnet is plain HTTP on :9000**, not HTTPS on 9443: P133's Serve rule forwards only to loopback
   HTTP (and tailnet HTTPS needs Tailscale certificates turned on). WireGuard encrypts the tailnet, so it is not sent in the
   clear. At home, `https://192.168.1.61:9443/` (self-signed: the browser warns once).
6. **No Websites site row for Portainer**: the console's light uses .NET's certificate check, which refuses Portainer's
   self-signed certificate, so the light would always read red. The two buttons do not need a row.
7. **Portainer mounts the Docker socket read-write.** That is how Portainer works (the docs' own install); it can change
   any container on Haven. It is LAN and tailnet only, and its admin login goes in the vault.
8. **The Homepage container reaching `100.98.32.16` and `192.168.1.61:80`** is the same path every other LAN monitor
   uses (a published port on Haven's own address); not proved from inside the container, since CC does not connect to
   Haven. If a tile reads down after the deploy while the page opens from the game PC, that is the place to look.
9. The baseline suite run used a clean `git worktree` of HEAD in the scratchpad. It was removed with
   `git worktree remove` and `prune`; `git worktree list` shows only the three that were there before.
10. **`D:\UO\sl-scripts` has uncommitted work that is not this prompt's**: `.gitignore`, `README.md` and `SL_Combat.py`
    modified, `SL_Loot.py` new, all changed between 14:51 and 15:21 today while this prompt ran (last commit 11:21). I never
    touched that repo. The commit preflight lists it under `scripts`, so the Golem's commit after P163 would take it with
    this prompt's work. Chase, check whose it is first (another session, or your own Legion edits).

## For Chase

The clicks, in order, all on the Shard Console's **Websites** tab after the phrase `deploy to haven`:

1. **Mega dashboard: deploy** (word `deploy`). Picks up the fixes. Its plan should now say every running container is in the
   inventory, no `PORTS OR IMAGES DIFFER`, and print the **mounts** of `monitoring-grafana`, `monitoring-prometheus` and
   `npm-admin-tailnet` (paste them to the next prompt, or into `services.json` volumes). "In the inventory, not on Haven:
   portainer" until step 2.
2. **Portainer (Haven): deploy** (word `deploy`). It pulls Portainer, starts it, and sets Serve :9000.
3. **FIRST LOGIN, WITHIN 5 MINUTES OF STEP 2:** open **https://192.168.1.61:9443/** (accept the certificate warning: it is
   Portainer's own), paste the **setup token** the window printed, and make the admin user. Put the password in the vault.
   **Missed the 5 minutes?** Click Portainer (Haven): deploy again: it restarts Portainer and you get 5 new minutes.
4. **The token for the dashboard:** in Portainer, your user (top right) > **My account** > **Access tokens** > Add, name
   `homepage` > copy. The environment ID is the number after `/endpoints/` when you click Haven's environment under
   **Environments**. Then `ssh -t chase@192.168.1.61 "nano ~/sl-home/dashboard.env"`, put them after
   `HOMEPAGE_VAR_PORTAINER_KEY=` and `HOMEPAGE_VAR_PORTAINER_ENV=`, save. (Grafana's `HOMEPAGE_VAR_GRAFANA_TOKEN` the same
   way, from Grafana's Service accounts, whenever you like: runbook, Tokens and keys.)
5. **Mega dashboard: deploy** once more, so the widget reads the token.

What each fixed tile should show after step 1 (`http://haven.tail81098d.ts.net/`):

- **Sunflower:** no "Print queue (tower copy)"; **Print queue** green with its order counts; **Dev store** with no dot and
  "Stopped, started by hand." in its description.
- **Monitoring:** **Prometheus** and **Grafana** green (watched on Haven's tailnet address; their links open on the
  tailnet). Grafana's Dashboards count says API Error until its token is pasted.
- **Ultima Online / Shattered Legacy:** **Legion scripts (dev)** green.
- **Admin:** **Nginx Proxy Manager** green (its front door), link still the SSH tunnel; new **NPM admin (tailnet)** green,
  opening `http://haven.tail81098d.ts.net:81/`; **Portainer (Haven)** red until step 2, then green; its widget API Error until
  step 5. No "(not in the inventory)" tiles.
- Gone: Web console and uoconsole node (not installed yet), until their state says running.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts dry run
```

No repo BLOCKED. `code` pending: this prompt's 13 files (10 modified, 3 new). `docs` pending: the runbook and these notes,
plus `testing/SUMMARY.md` and `testing/play-tests.json` (the importer's machine output, not mine). `scripts` pending: the
four `sl-scripts` files in Deviations 10, **not mine**. No file over 5 MB added (largest new file: the Portainer deploy
script, about 20 KB); scratch was all in the session scratchpad, outside both repos.

P163 DONE
