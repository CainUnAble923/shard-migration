# Haven and the game PC: the runbook

Written by cc-P133 (2026-10-17) for Chase, so any service can be moved, rebuilt or restored by someone reading only this
file and the inventory. **The inventory is `D:\ShatteredLegacy\docker\haven\services.json`**: one entry per service, with its
host, container, image, ports, compose file, data, env variable names, secrets (where they live, never their values),
health URL, what it needs and what needs it, backup paths and owner. Haven's dashboard is generated from it
(`docker\haven\Build-HavenDashboard.ps1`), so the dashboard and the inventory cannot disagree. This runbook is the prose;
where the two differ, `services.json` is right and this file is out of date.

**Rule (both repos' `AGENTS.md`):** any prompt that adds, moves or removes a service on Haven or the game PC updates
`services.json` and this runbook in the same prompt, and adds a line to "Changed on" at the bottom.

Facts marked *unverified* come from Chase's notes and have not been seen yet; the first **Mega dashboard: deploy** prints
them (Discover) and keeps the output in `D:\UO\haven-ops\discovery-latest.txt`.

## The machines

| Machine | LAN | Tailnet | What it is |
|---|---|---|---|
| **Haven** | `192.168.1.61` | `haven.tail81098d.ts.net` (`100.98.32.16`) | Ubuntu home server, Docker 29.5.2. The public website and wiki behind NPM, the vault, the ops pages, the dashboard, Sunflower's print queue and Spoolman. `ssh chase@192.168.1.61` |
| **Game PC** (chases-tower) | `192.168.1.58` | `chases-tower.tail81098d.ts.net` (`100.78.49.68`) | Windows 11, Docker Desktop. The test shard and what reads its saves, the Golem, the Shard Console. Sleeps sometimes |
| **Hostinger** | outside | none | Sunflower's live WordPress store and its lead-time page |

Tailnet: `tail81098d.ts.net`. **Tailscale is the only way in from outside the house** (Chase's decision, 2026-10-15).
The router forwards 80 and 443 (NPM: the public website, wiki, downloads, vault) and 2593 (the retired live shard) and
nothing else.

```
                 internet
                    |
          router (forwards 80, 443 to Haven)         tailnet tail81098d.ts.net (phones, laptops, the game PC)
                    |                                          |
   +----------------+-----------------+         Tailscale Serve on Haven: :80 dashboard, :8093 ops page,
   |   Haven 192.168.1.61             |         :8787 print queue (each -> 127.0.0.1 on Haven)
   |                                  |                        |
   |  NPM sl-proxy :80 :443 ---> sl-website, sl-wiki, sl-downloads, sl-vaultwarden, kevins-parts-wp   (PUBLIC)
   |                                  |
   |  sl-homepage :3000 (LAN + loopback) <--- Tailscale :80
   |  sl-play-tests :8093 page, :8094 token listener <--- Tailscale :8093
   |  sunflower-print-queue :8787 <--- Tailscale :8787 ----- pushes over SSH ---> Hostinger
   |  spoolman :7912 (all interfaces)   monitoring-prometheus :9090, monitoring-grafana :3001 (tailnet IP only)
   |  npm-admin-tailnet (tailnet :81 -> NPM admin)   portainer :9443 (LAN + loopback) <--- Tailscale :9000
   +----------------------------------+
                    ^  snapshot every minute (POST :8094, bearer token)
                    |
   +----------------+-----------------+
   |  Game PC 192.168.1.58            |
   |  sl-modernuo-test :2594   sl-uo-status :8092   sl-shard-probe   sl-ddns   sl-portainer :9000/:9443
   |  sl-dashboard :3000 (old, stopped)   sl-play-tests (stopped since the cutover)   print queue (tower copy: retired 10-18)
   +----------------------------------+
```

**What a tile shows** (cc-P163): a dot or a State line for everything running. A *planned*, *retired* or *built, not
installed yet* service gets **no tile** (it stays in `services.json`, here, and in Discover's "in the inventory, not on
Haven"); set its `state` to `running` when it is, and the next build gives it its tile. An *on-demand* service (the
Sunflower dev store, stopped by design) says **"Stopped, started by hand"** with no monitor instead of a red dot.

**Up or down on every tile** (Chase's decision 2): Haven's containers through the dashboard's read-only Docker proxy;
web services by their health URL (`siteMonitor`); the game PC's services from the snapshot it pushes to Haven every
minute (`up.<key>` in `GET :8094/api/gamepc`), which says "Game PC offline since ..." for all of them when it sleeps.

## Deploy buttons

All on the Shard Console's **Websites** tab, after the phrase `deploy to haven`. Each runs one script in a window, starts
with a read-only Discover of Haven, prints its plan, and changes nothing until its word is typed. `-DryRun` stops after the
plan. Launchers are one line each in `D:\UO\haven-migration`; transcripts land in
`D:\ShatteredLegacy\scripts\shard-console-output\deploys\`.

| Button | Script | Word | What it changes |
|---|---|---|---|
| Mega dashboard: deploy | `docker\dashboard\haven\Deploy-MegaDashboard.ps1 -Mode Deploy` | `deploy` | Builds the config from `services.json`; backs up `~/sl-home` to `~/sl-home/backup-<time>`; copies compose and config; adds missing names to `~/sl-home/dashboard.env` (empty, never a value); stops the old Homepage on Haven; starts `sl-homepage` and its proxy on `192.168.1.61:3000` and `127.0.0.1:3000`; points Tailscale Serve (:80, :8093, :8787) at the loopback ports that answer; stops the game PC's `sl-dashboard`. Keeps the discovery in `D:\UO\haven-ops\discovery-latest.txt` |
| Mega dashboard: roll back | same, `-Mode Rollback` | `roll back` | Stops `sl-home`; turns off Serve's :80; starts the old Homepages on Haven and the game PC |
| Ops pages: deploy | `docker\ops\Deploy-HavenOps.ps1 -Mode Deploy` | `deploy` | `~/sl-ops`: git-pull, the deploy key, the token; after the cutover also recreates the page (a new `server.py`, and since P133 the loopback port :8093 for Tailscale) |
| Ops pages: cut over / roll back | same, `-Mode Cutover` / `Rollback` | `cut over` / `roll back` | Moves the play-test pages between the game PC and Haven (done 2026-10-16) |
| Print queue: deploy | `C:\dev\sunflower\print-queue\haven\Deploy-PrintQueue.ps1 -Mode Deploy` | `deploy` | Builds the queue on Haven, makes its own key; **proves the key from Haven before the move** (refuses, tower untouched, if Hostinger does not take it); stops the tower copy; moves the data (SHA-256 checked); starts Haven's; makes and checks the first push |
| Print queue: roll back | same, `-Mode Rollback` | `roll back` | Data back to the tower, Haven's stopped and set aside, the tower copy started |
| Portainer (Haven): deploy (cc-P163) | `docker\portainer-haven\Deploy-PortainerHaven.ps1 -Mode Deploy` | `deploy` | Refuses if a `portainer` container exists that is not its own (project `sl-portainer`) or 9443 is taken. Backs up the volume `portainer_data` first when it exists (Portainer stopped, tarred to `~/sl-portainer/backup-<time>.tgz`); copies the compose to `~/sl-portainer`; starts `portainer/portainer-ce:2.45.2` on `192.168.1.61:9443` and `127.0.0.1:9443` (HTTPS), `127.0.0.1:9000` (HTTP, for Serve); Serve :9000; the first time, prints the first-login link, the **5-minute** limit and the setup token |
| Portainer (Haven): roll back (cc-P163) | same, `-Mode Rollback` | `roll back` | Stops Portainer (the volume and backups kept); Serve :9000 off |
| Deploy to Haven (website, wiki macros) | `Deploy-Website.ps1`, `Publish-WikiMacros.ps1` | phrase | Content only; never NPM |
| Player package tab: Publish to dev (cc-P144) | `scripts\legion\Publish-LegionScripts.ps1 -Mode Dev` | phrase `publish scripts to dev`, then `yes` | `~/sl-scripts-dev/html` (the dev channel): backs up the set to `~/backups/legion-scripts/dev/<version>/`, swaps the scripts in, downloads each back, `scripts.json` last; rolls back on a mismatch. Refused unless the scripts repo is committed and level with GitHub |
| Player package tab: Promote to official (cc-P144) | same, `-Mode Promote` | phrase `promote scripts to official`, then `yes` | `<sl-downloads html>/scripts/` (the official channel), from the dev folder on Haven, with the same steps; backups in `~/backups/legion-scripts/<version>/`; tags `official-<version>` in the scripts repo |
| (once, by hand) dev channel setup (cc-P144) | same, `-Mode SetupDev` | `yes` | Makes `~/sl-scripts-dev`, copies the compose file, `docker compose -p sl-scripts-dev up -d` |

The console's **Open NPM** opens the SSH tunnel to NPM's admin page (`ssh -N -L 8081:localhost:81 chase@192.168.1.61`,
then `http://localhost:8081/`). On the tailnet it is also `http://haven.tail81098d.ts.net:81/` (the `npm-admin-tailnet`
forwarder, found by Discover on 2026-10-18).

**Discover's port check** (cc-P163): the Mega dashboard deploy's plan prints `PORTS OR IMAGES DIFFER` for any running
container whose published addresses (IPv4; the `[::]` twins left out) or image are not what its entry says, and the
mounts of any entry whose volumes still say "from Discover". Copy those into `services.json` and here.

## Tokens and keys

Where each is made and where it lives. **No value is ever in git, a log, a deploy transcript or this file.**

| Name | Lives in | Made where |
|---|---|---|
| `HOMEPAGE_VAR_OPS_TOKEN` | Haven `~/sl-home/dashboard.env` (chmod 600) | Copied on Haven from `~/sl-ops/ops.env` (`PLAYTESTS_TOKEN`) by the dashboard deploy; never leaves Haven |
| `HOMEPAGE_VAR_GRAFANA_TOKEN` | same file, pasted by Chase | Grafana > Administration > Users and access > **Service accounts** > Add service account, name `homepage`, role **Viewer** > Add service account token (no expiry, or a year) > copy it once |
| `HOMEPAGE_VAR_PORTAINER_KEY` | same file, pasted by Chase | Portainer on Haven > your user (top right) > **My account** > **Access tokens** > Add access token, name `homepage` > copy it once |
| `HOMEPAGE_VAR_PORTAINER_ENV` | same file (not a secret) | Portainer > **Environments** > click Haven's: the number in the address bar after `/endpoints/` (often `1`, sometimes `2` or `3`) |
| Portainer admin login | the vault | Portainer's first-time setup page, **within 5 minutes** of its first start, with the setup token Portainer (Haven): deploy prints (single use; dead once the admin exists) |
| `PLAYTESTS_TOKEN` | Haven `~/sl-ops/ops.env` and the game PC's `D:\UO\haven-ops\token.txt` | Ops pages: deploy (asked once, or made) |
| `keys/shard-migration` | Haven `~/sl-ops/keys` | Ops pages: deploy; public half is a read-only deploy key on GitHub |
| `keys/sunflower-live` | Haven `~/sunflower-print-queue/keys` | Print queue: deploy; public half goes in Hostinger hPanel > Advanced > SSH Access > SSH keys |
| `CF_API_TOKEN`, `CF_ZONE_ID` | game PC `D:\ShatteredLegacy\docker\uo\.env` (git-ignored) | Cloudflare > My Profile > API Tokens (DNS edit on the zone) |
| NPM admin login, everything else | the vault | |

**Pasting a token** (from the game PC, PowerShell): `ssh -t chase@192.168.1.61 "nano ~/sl-home/dashboard.env"`, put the
value after the `=` on its line, save, then `ssh chase@192.168.1.61 "cd ~/sl-home && docker compose -p sl-home up -d
--force-recreate homepage"` (or click Mega dashboard: deploy again, which keeps every value). Why Grafana is a
`customapi` tile and not Homepage's `grafana` widget: that widget reads `/api/admin/stats`, which needs Grafana's server
admin, and a Viewer service account cannot have it. The Viewer token reads `/api/search` (the dashboard count).

## Never move or expose

- **Spoolman's database** (its data volume). Never delete, prune or recreate it; back it up before any change to Spoolman.
- **Vaultwarden** and its data folder. A link tile only, never a widget, never a credential anywhere.
- **The public website, wiki, downloads and vault routing** in NPM (`sl-proxy`, ports 80 and 443). Nothing on the intranet
  is ever added to NPM, Cloudflare, or Tailscale Funnel.
- **Nothing intranet binds `0.0.0.0`.** The dashboard, the ops pages and the print queue publish on `192.168.1.61` and
  `127.0.0.1` only; the tailnet reaches them through Tailscale Serve. (Older stacks that do bind all interfaces, and are
  not forwarded by the router: Spoolman (seen on `0.0.0.0:7912` by Discover, 2026-10-18), the old Homepage, the game PC's
  `sl-uo-status`, `sl-portainer` and the test shard. Do not add router forwards for any of them. Grafana and Prometheus
  publish on Haven's tailnet address only, and Haven's Portainer on its LAN address and loopback.)
- **`docker volume prune`** on Haven: never. Several services keep their data in named volumes.

## Moving any service (the general steps)

1. **Read its entry in `services.json`**: ports, volumes, env names, secrets, `dependsOn` and `neededBy`.
2. **Back up first**: everything in its `backup` list, as a tar on the source host (`tar czf ~/backups/<key>-<date>.tgz ...`);
   for a database, a dump too.
3. **Stop it on the source** (`docker compose -p <project> stop`), so nothing writes while it moves.
4. **Copy** its compose folder and data to the target (`scp -r`, or `docker run --rm -v <vol>:/v alpine tar` for a named
   volume), and its env file (chmod 600).
5. **Start it on the target**, bound to that host's LAN address and loopback, never `0.0.0.0`.
6. **Point everything at the new place**:
   - **DNS** (Cloudflare) only if it is public; its record follows the house's public address, not a host (`sl-ddns`).
   - **NPM**: only for the public sites, the proxy host's forward host and port.
   - **Tailscale Serve**: on the new host, `tailscale serve --bg --http=<port> http://127.0.0.1:<port>`; on the old one
     `tailscale serve --http=<port> off`. (`tailscaleServe` in `services.json`.)
   - **The dashboard**: change the entry's `host`, ports, `href` and health URLs in `services.json`, run
     `docker\haven\Build-HavenDashboard.ps1`, commit, click Mega dashboard: deploy.
   - Anything in its `neededBy` list that names its address (for example the snapshot's URL in `scripts\haven-ops.json`).
7. **Check its health URL**, then remove it from the source (keep the backup).
8. **Write it down**: `services.json`, this file, and a "Changed on" line.

**What breaks while it moves:** whatever is in its `neededBy` list, until step 6. The dashboard tile reads Down or
"Not found" until the deploy.

## The services

Each heading names its `services.json` key. Restart is always `docker restart <container>` on its host unless it says
otherwise; logs `docker logs --tail 200 <container>`.

### Sunflower print queue `print-queue`

The opener orders page and the public lead-time page's pusher. **On Haven since 2026-10-18 08:56** (Print queue: deploy:
key proved from Haven, 7 files moved and checked, first push OK). Built on Haven from `C:\dev\sunflower\print-queue`
(Dockerfile, python:3-alpine); files in `/home/chase/sunflower-print-queue/{stack,data,logs,keys}`;
`http://192.168.1.61:8787/` and `http://haven.tail81098d.ts.net:8787/` (Serve :8787). Pushes to Hostinger over SSH
with **its own key** (made on Haven), 60 seconds after the last edit (a debounced timer, not a loop). **Data:** `data/`
(customer orders: back it up). **Restore:** stop it, put `queue.json` back in `data/`, start it. **Move:** the general
steps; the key moves with `keys/` (or make a new one and add it in Hostinger), and the new host's Serve needs :8787.
**Breaks while moving:** nobody can mark orders; the lead-time page keeps its last copy.

### Sunflower print queue (the tower copy) `print-queue-tower`

**Retired 2026-10-18** (state `retired`, no tile since cc-P163). It was `py queue_server.py` in
`C:\dev\sunflower\print-queue` on the game PC, `127.0.0.1:8787`, pushing with Chase's own key. The move found it not
running and renamed its data `data.moved-20261018` (kept, not served); the desktop shortcut now opens Haven's page.
**Print queue: roll back** would start it again (and the entry's state and tile would come back with it).

### Sunflower Custom Gifts store `sunflower-store`

WordPress on Hostinger, `https://sunflowercustomgiftshop.com`. Not ours to move; Hostinger's backups in hPanel. The
print queue pushes its lead-time snippet there.

### Sunflower dev store `sunflower-devstack`

`C:\dev\sunflower\sunflower-devstack` on the game PC, `:8080` while it runs (by hand). Stopped is its usual state, so its
tile says "Stopped, started by hand" and has no monitor (cc-P163).

### Spoolman `spoolman`

Filament inventory: `http://haven.tail81098d.ts.net:7912/`, REST at `/api/v1/`, health `/api/v1/health`, no login.
`SPOOLMAN_METRICS_ENABLED=TRUE` gives `/metrics` for Prometheus. Discover 2026-10-18: container `spoolman`, image
`ghcr.io/donkie/spoolman:latest`, compose folder `/opt/spoolman`, published on `0.0.0.0:7912` (all interfaces: its own
compose, not ours). *Still unverified:* the data volume; the next Discover prints its mounts. **Never touch its data volume.** **Back up:**
`docker run --rm -v <its volume>:/v -v ~/backups:/b alpine tar czf /b/spoolman-$(date +%F).tgz -C /v .` (Spoolman can
also export from its own UI). **Restore:** stop it, untar into the volume, start it. **Move:** the general steps; the
volume tar is the whole state; Prometheus's scrape target follows it.

### Prometheus `monitoring-prometheus`

Running on Haven, installed by hand (not by a console deploy). Discover 2026-10-18: container `monitoring-prometheus`,
`prom/prometheus:v3.14.0`, compose folder `/opt/monitoring`, published on **Haven's tailnet address only**
(`100.98.32.16:9090`), so `http://haven.tail81098d.ts.net:9090/` works and the LAN address does not. Chase's notes: config
`/opt/monitoring/prometheus.yml`, scrapes Spoolman's `/metrics` every 5 minutes, 5-year retention. The dashboard watches
`http://100.98.32.16:9090/-/healthy`. *From Discover (next deploy):* its data volume. **Back up** the config and the data.
(Was the planned entry `prometheus` until cc-P163.)

### Grafana `monitoring-grafana`

Running on Haven, installed by hand. Discover 2026-10-18: container `monitoring-grafana`, `grafana/grafana:13.1.8`, compose
folder `/opt/monitoring`, **tailnet address only** (`100.98.32.16:3001`, container port 3000):
`http://haven.tail81098d.ts.net:3001/`. The dashboard watches `http://100.98.32.16:3001/api/health`; its tile needs
`HOMEPAGE_VAR_GRAFANA_TOKEN` (Tokens and keys). *From Discover (next deploy):* its data volume. **Back up**
`/var/lib/grafana` (its volume or folder). (Was the planned entry `grafana` until cc-P163.)

### Game PC `gamepc-host`

The machine itself. Its tile reads `GET http://192.168.1.61:8094/api/gamepc` with the ops token: Up, or Offline with
"offline since" (3 minutes after the last snapshot), and the Golem's running prompt. The snapshot is the scheduled task
**SL game PC snapshot** (`scripts\Publish-GamePcSnapshot.ps1`, every minute while Chase is logged on;
`scripts\Install-GamePcSnapshotTask.ps1` installs it). Since P133 it also reports every game PC service the dashboard shows
(the `snapshot` keys in `services.json`), and since cc-P164 the test shard's deploy record (`testShard`: commit, version,
when), so Haven's play-test page can say "needs: rebuild test shard" and its bug reports carry the version.

### Status feed `uo-status`

`sl-uo-status`, nginx on the game PC, `:8092`: `shards.json`, `migration.json`, `downloads.json`, read by the website
and the dashboard. `D:\ShatteredLegacy\docker\uo-status\docker-compose.yml`. **Moving it** to Haven would need the shard's
status folder there too: it serves files the shard writes on the game PC.

### Shard probe `shard-probe`

`sl-shard-probe` on the game PC: checks the test shard's port and writes `shards.json`. Same compose as the feed.

### Test shard `test-shard`

`sl-modernuo-test` on the game PC, `:2594` (LAN; the router does not forward it). Built by `docker\uo\build.sh`, started by
`Start-TestShard.ps1` or the Shard Console (restart policy `no`). Saves in `server\lib\uo\modernuo-test`. Never moved
by a dashboard prompt; see `D:\ShatteredLegacy\docker\uo\README.md`.

### DDNS updater `ddns`

`sl-ddns` on the game PC: keeps `shatteredlegacyuo.com` at the house's public address (Cloudflare). Secrets in
`docker\uo\.env` (git-ignored). Since cc-P668 its **only** address source is the gate (`ddns-gate`, below): it publishes
Haven's address, never the game PC's, so Chase's VPN no longer matters (on 2026-10-26 it published the VPN's exit and the
site went dark). `docker\uo\Test-DdnsSafe.ps1` says whether the container is that one (UNSAFE otherwise; `-Fix` stops it
and sets restart=no); `Start-TestShard.ps1` and the console's "Restart sl-ddns" run it first. **Recreate** (after any
change to its compose): `docker compose -p uo -f docker\uo\docker-compose.yml up -d` in `D:\ShatteredLegacy`, then
`Test-DdnsSafe.ps1`. **Moving it** to Haven: never copy `docker\uo\.env` off the game PC; Haven gets its own Cloudflare
token (Chase makes it), then start it there, stop it here; only one may run.

### DDNS gate `ddns-gate`

`sl-ddns-gate` on the game PC, in the same compose project (`uo`), no host port: answers sl-ddns at
`https://ddns-gate:8443/ip` (self-signed certificate in volume `ddns_tls`; sl-ddns trusts it through `SSL_CERT_FILE`).
It serves Haven's address from `sl-homeip` (LAN `192.168.1.61:8098`, then the tailnet), and refuses (403, no address in
the text, the record is left alone, `*** REFUSED ***` in its log) when Haven does not answer, Haven's URLs disagree, or
Haven reports a known VPN exit (`BLOCK`) or one it learned (the game PC's egress differing from Haven's for 15 minutes,
kept in volume `ddns_gate`). **Check the way to Haven:** `docker\uo\Test-DdnsSafe.ps1 -Reach` (with the VPN on and off).
**Logs:** `docker logs sl-ddns-gate`. Code: `docker\uo\ddns-gate`.

### Home IP `homeip`

`sl-homeip` on Haven: the house's public IPv4 as text, `http://192.168.1.61:8098/ip` and `127.0.0.1:8098` (Tailscale Serve
:8098; never public, never NPM). Every 3 minutes it asks two public lookups and keeps the answer only when they agree; `/ip`
answers 503 when there is no agreed answer younger than 15 minutes; `/status` is the detail. `~/sl-homeip`
(project `sl-homeip`). **Deploy / roll back:** `docker\homeip\Deploy-HavenHomeIp.ps1 -Mode Deploy|Rollback` (Discover first,
typed word). No data, nothing to back up. Stopped, sl-ddns gets no address and leaves the record alone.

### Ops pages `play-tests`

`sl-play-tests` on Haven since 2026-10-16: Play tests, Ideas, Bug reports, Shard status. `~/sl-ops/stack/docker-compose.yml`
(project `sl-ops`); page `192.168.1.61:8093` and `127.0.0.1:8093` (Tailscale Serve :8093), token listener
`192.168.1.61:8094`. **Data:** `~/sl-ops/data` is THE copy of play-test results, ideas and bug reports (the game PC mirrors
it into git at every commit). **Back up** `~/sl-ops/data` and `~/sl-ops/ops.env`. **Roll back** with Ops pages: roll back.
**Move:** the general steps; then `scripts\haven-ops.json` (its URLs) and the snapshot's target follow.

### Ops pages repo pull `ops-git-pull`

`sl-ops-git-pull` on Haven: clones of both repos, pulled every 2 minutes, so the page and `server.py` follow `main` once
Chase pushes. Needs the read-only deploy key (`~/sl-ops/keys`). Nothing to back up but the key.

### Public website `website`

`sl-website` (nginx) on Haven, public through NPM as `https://shatteredlegacyuo.com`. Deployed by the console's Deploy to
Haven (`Deploy-Website.ps1`). Content is in git. **Never change its NPM routing.**

### Wiki `wiki`

`sl-wiki` (DokuWiki) on Haven, public through NPM. Data in the Docker volume `sl-wiki-storage`. **Back up** that volume.
Wiki macros: `Publish-WikiMacros.ps1`.

### Downloads `downloads`

`sl-downloads` (nginx) on Haven, public through NPM as `https://get.shatteredlegacyuo.com`. Files in
`/home/chase/sharttered-legacy/downloads` (sic: the misspelt folder is the real one, seen 2026-09-28).
`Publish-PlayerPackage.ps1` rebuilds it. Its `scripts/` subfolder is the **official channel of the Legion scripts**
(cc-P144): `https://get.shatteredlegacyuo.com/scripts/scripts.json` and the `.py` files it lists, which every player package
install pulls on each start and every new package ships. Written only by the Shard Console's **Promote to official**
(`scripts\legion\Publish-LegionScripts.ps1 -Mode Promote`), which finds the folder with `docker inspect sl-downloads`,
writes it through a throwaway `nginx:alpine` container (the folder is root-owned), and backs up each set it replaces to
`~/backups/legion-scripts/<version>/`.

### Legion scripts dev channel `scripts-dev`

*cc-P144; running since 2026-10-18 (Discover 09:46; Serve :8097 set by that deploy).* `sl-scripts-dev` (nginx:alpine) on Haven, project `sl-scripts-dev` in
`~/sl-scripts-dev/stack` (source `D:\ShatteredLegacy\docker\scripts-dev`), serving `~/sl-scripts-dev/html` read only on
`192.168.1.61:8097` and `127.0.0.1:8097`, on the tailnet as `http://haven.tail81098d.ts.net:8097/` (Tailscale Serve :8097).
**Never public, never NPM.** It holds half-tested scripts for Chase's own PCs (the tower and the work PC, flagged dev in
their `%LOCALAPPDATA%\ShatteredLegacy\legion-scripts.json`); players never read it. Written by **Publish to dev**
(`Publish-LegionScripts.ps1 -Mode Dev`), from either PC, over the LAN or Tailscale, with that PC's own SSH key; each set it
replaces is backed up to `~/backups/legion-scripts/dev/<version>/`. **Start it (once):** `Publish-LegionScripts.ps1 -Mode
SetupDev`, then Mega dashboard: deploy for the Serve port. **Restart:** `cd ~/sl-scripts-dev/stack && docker compose -p
sl-scripts-dev restart`. **Data:** nothing to back up that git does not have (the scripts are in the private repo
`CainUnAble923/shattered-legacy-scripts`); the backups folder is history only. **Move it:** any host on the tailnet with
nginx; change `scripts-dev` here and in `services.json` and each dev PC's `devUrl`.

### Nginx Proxy Manager `npm`

`sl-proxy` on Haven: **the public entry**, 80 and 443 on all interfaces, admin on `127.0.0.1:81` (SSH tunnel). Volumes
`proxy_npm_data` and `proxy_npm_letsencrypt`. **Back up both volumes before any change.** Never add an intranet host to it.
Moving it means moving the router's 80/443 forward too: plan it as its own prompt. Its tile is watched at its front door,
`http://192.168.1.61:80/` (cc-P163; the admin port answers only on Haven's loopback, and `localhost` inside Homepage's
container is Homepage itself), and links the admin page through the console's SSH tunnel.

### NPM admin on the tailnet `npm-admin-tailnet`

Found by Discover on 2026-10-18, running 3 days: `npm-admin-tailnet`, `alpine/socat:1.8.1.1`, compose folder
`/home/chase/shattered-legacy/docker/npm-admin-tailnet` (**not in git**; made by hand on Haven, by whom and when not
recorded). No published ports, and Haven listens on `100.98.32.16:81`, so it runs in the host network and forwards the
tailnet's :81 to NPM's admin on `127.0.0.1:81` (inferred). `http://haven.tail81098d.ts.net:81/` answered from the game PC.
**Back up** its compose folder (it is not in git). Nothing else to keep.

### Password vault `vaultwarden`

`sl-vaultwarden` on Haven, public through NPM as `https://vault.chasekfleming.com`. Compose on Haven only
(`~/shattered-legacy/docker/vaultwarden`). Backups `~/backups/vault-data-*.tgz` (owner-only). **Move only with a fresh
backup and a tested restore**; never a widget.

### This dashboard `homepage`

`sl-homepage` (Homepage v1.13.1) on Haven, `~/sl-home` (project `sl-home`): `192.168.1.61:3000` and `127.0.0.1:3000`, on the
tailnet as `http://haven.tail81098d.ts.net/` (Tailscale Serve :80; Haven's own port 80 is NPM's). Config generated from
`services.json`; secrets in `~/sl-home/dashboard.env`. **Back up** `dashboard.env` (everything else is in git). Every
deploy backs up `~/sl-home` to `~/sl-home/backup-<time>` first.

### Dashboard Docker proxy `homepage-dockerproxy`

`sl-homepage-dockerproxy` (tecnativa/docker-socket-proxy v0.4.1): lets the dashboard read Haven's container states (GET
on containers only; every POST refused). Moves with the dashboard.

### Portainer (Haven) `portainer-haven`

Portainer CE on Haven, installed by **Portainer (Haven): deploy** (cc-P163; it was not on Haven before: Discover 2026-10-18).
Container `portainer`, `portainer/portainer-ce:2.45.2` (the `lts` tag of Portainer's docs, pinned), project `sl-portainer`
in `~/sl-portainer` (source `D:\ShatteredLegacy\docker\portainer-haven`). HTTPS with its own self-signed certificate on
`https://192.168.1.61:9443/` and `127.0.0.1:9443`; its plain HTTP port on `127.0.0.1:9000` only, which Tailscale Serve
gives the tailnet as `http://haven.tail81098d.ts.net:9000/`. **Data:** the Docker volume `portainer_data` (the admin user,
tokens, settings). **Back up:** every deploy tars it to `~/sl-portainer/backup-<time>.tgz` first; by hand,
`docker stop portainer; docker run --rm -v portainer_data:/data:ro -v ~/backups:/b alpine:3.20 tar czf /b/portainer-$(date +%F).tgz -C /data .; docker start portainer`.
**Restore:** stop it, untar into the volume, start it. **First start:** the admin user must be made within 5 minutes, with
the setup token from `docker logs portainer` (`setup_token=`; the deploy prints it); missed, deploy again. Its tile needs
`HOMEPAGE_VAR_PORTAINER_KEY` and `HOMEPAGE_VAR_PORTAINER_ENV`. It mounts the Docker socket read-write: it can change any
container on Haven. **Stacks and Portainer:** the stacks the console deploys
(`sl-home`, `sl-ops`, `sunflower-pq`) are made with `docker compose` from git, so Portainer lists them as *limited*
(created outside Portainer). Read them there; change them in git and redeploy, never in Portainer's editor, or the two
drift.

### Portainer (game PC) `portainer-gamepc`

`sl-portainer` on the game PC, `:9000` and `:9443`, volume `portainer_data`. `docker\portainer\docker-compose.yml`.

### Old Homepage on Haven `old-homepage-haven`

The June `sl-dashboard` in `~/shattered-legacy/docker/dashboard`, `0.0.0.0:3000`. **Stopped on purpose** by Mega dashboard:
deploy and kept for the rollback. Exited is right. Remove it (and this entry) once the new dashboard has run a few weeks.

### Old Homepage on the game PC `old-homepage-gamepc`

`sl-dashboard` on the game PC, stopped by the deploy (2026-10-18), started by the rollback. Same advice.

### Ops pages on the game PC `play-tests-gamepc`

`sl-play-tests` on the game PC, stopped since the cutover (2026-10-16); Ops pages: roll back starts it.

### Kevin's Parts site `kevins-parts-wp`

A client's WordPress, hosted on Haven under `/home/chase/clients/kevins-parts` (P89), public through NPM. Up or down only on
the dashboard. *Unverified:* image, volumes, NPM host. **Back up** its folder and volumes before touching Haven's Docker.

### Kevin's Parts database `kevins-parts-db`

Its database. **A dump before any move** (`docker exec kevins-parts-db mysqldump ...` with the stack's own credentials).

### Tailscale `tailscale`

`tailscaled` on Haven (and on the game PC, Chase's phone, the work PC). The only way in from outside the house. Haven's
**Serve** config (persisted in `/var/lib/tailscale`, survives a restart): tailnet :80 to `127.0.0.1:3000` (dashboard),
:8093 to `127.0.0.1:8093` (ops page), :8787 to `127.0.0.1:8787` (print queue), since cc-P144 :8097 to `127.0.0.1:8097`
(the Legion scripts' dev channel; all four seen in Discover, 2026-10-18 09:46), and since cc-P163 :9000 to
`127.0.0.1:9000` (Portainer, once its deploy runs). `tailscale serve status` shows it. **Never
`tailscale funnel`** (that would make it public). Changing Serve as `chase` needs a one-time `sudo tailscale set
--operator=chase` on Haven. Its tile reads the game PC's view of Haven's node (online or not).

### Web console `web-console`

*cc-P155, 2026-10-17.* The Shard Console's status, read only, for the phone and the work PC: tiles, lights, the Golem
and its queue, Needs you, the timeline, logs and links. A Python service on the **game PC** (`D:\ShatteredLegacy\web-console\server.py`,
standard library only), started at Chase's logon by the scheduled task **SL web console** (`web-console\Install-WebConsole.ps1`;
`-Uninstall` removes it). It listens on **127.0.0.1 only**: `:8095` for this PC's browser, `:8096` for the uoconsole sidecar,
where a request is answered only with the proof forwarder's `X-UOConsole-Proof` (cc-P182) and when Tailscale Serve's
`Tailscale-User-Login` is an allowed login (default: this PC's own
Tailscale login, Chase's; or `allowedLogins` in `D:\UO\web-console\settings.json`, kept out of git). It starts the status
collector (`scripts\Write-ConsoleStatus.ps1 -Loop`), which writes `scripts\shard-console-cache\console-status.json`; the Shard
Console writes the same file after its own refreshes. **Restart:** `Stop-ScheduledTask -TaskName 'SL web console'; Start-ScheduledTask -TaskName 'SL web console'`.
*cc-P182:* the Golem's buttons (`POST /api/action`, only on `:8096`), each run through `scripts\Invoke-WebConsoleAction.ps1`
(the Shard Console's own plans), one at a time, logged to `actions.log`. The installer stops a running copy first, so an
update is the install line again.
**Data:** `D:\UO\web-console` (settings, the key file, `proof.key`, `access.log`, `actions.log`, `collector.log`); back up
`settings.json` (`proof.key` is remade by the installer if lost; the sidecar is then recreated with it).
**Move it:** it reads the game PC's Docker, files, Golem and repos, so it moves only with them; on another PC, run the
installer there and point the sidecar at it. Up or down on Haven's dashboard from the game PC snapshot (the process).

### uoconsole (the web console's Tailscale node) `uoconsole-ts`

*cc-P155.* A Tailscale container on the game PC's Docker (`web-console\tailscale\docker-compose.yml`, project `uoconsole`,
image `tailscale/tailscale:v1.88.3`, userspace networking, **no port published**), hostname `uoconsole`: Tailscale Serve
gives `https://uoconsole.tail81098d.ts.net/` its certificate and proxies to `host.docker.internal:8096`. **Funnel off**
(`serve.json` AllowFunnel false). Its auth key (tagged `tag:uoconsole`) is `TS_AUTHKEY` in `D:\UO\web-console\tailscale.env`,
outside git; after the first login the node's state is in the volume `uoconsole_uoconsole-ts-state` and the key is not
needed again. **Start:** `web-console\Install-WebConsole.ps1 -Tailscale`. **Remove:** `-Uninstall` (`-Purge` also drops the
state; then remove the machine in the Tailscale admin console). **Never** `tailscale funnel`, never a published port.
*cc-P182:* Serve now proxies to `http://127.0.0.2:8097`, the proof forwarder below, not to `host.docker.internal:8096`.

### uoconsole proof forwarder `uoconsole-proof`

*cc-P182.* A `python:3.12.7-alpine3.20` container in the same compose project, `network_mode: service:tailscale` (the
node's own network namespace, **no port published**), running `web-console\tailscale\proof_proxy.py`: it listens on
`127.0.0.2:8097` (never 127.0.0.1, where tailscaled hands direct tailnet connections), sets `X-UOConsole-Proof` from
`D:\UO\web-console\proof.key` (mounted read only; any proof a caller sent is dropped) and passes each request on to
`host.docker.internal:8096`. So a container on the game PC that reaches `:8096` directly cannot act as Chase (P155's
Deviation 2). **Start/remove:** with the node (`Install-WebConsole.ps1 -Tailscale`, `-Uninstall`).

## Paths to add to Haven's backups

- `/home/chase/sl-home/dashboard.env`
- `/home/chase/sl-ops/data` and `/home/chase/sl-ops/ops.env` and `/home/chase/sl-ops/keys`
- `/home/chase/sunflower-print-queue/data` and `/home/chase/sunflower-print-queue/keys`
- Spoolman's data volume *(name unverified; the next Discover prints its mounts)*
- `/opt/monitoring` (Prometheus config and data, Grafana's data; installed, running since about 2026-10-15)
- Docker volumes `proxy_npm_data`, `proxy_npm_letsencrypt`, `sl-wiki-storage`, `portainer_data` (and `~/sl-portainer`,
  where the deploy leaves its backups)
- `/home/chase/shattered-legacy/docker/npm-admin-tailnet` (not in git)
- Vaultwarden's data folder (as now: `~/backups/vault-data-*.tgz`)
- `/home/chase/clients/kevins-parts` and its database dump
- `/var/lib/tailscale` (or just re-login after a rebuild)
- `~/backups/legion-scripts` is optional (history of replaced script sets; the scripts themselves are in GitHub)

## Changed on

- 2026-10-14 cc-P107: ops pages stack built (`sl-ops`); cut over to Haven 2026-10-16 by Chase.
- 2026-10-14 cc-P109: print queue container built (not deployed yet).
- 2026-10-14 cc-P110: the mega dashboard on Haven built (not deployed yet).
- 2026-10-17 cc-P133: this runbook and `services.json` (29 services); the dashboard generated from it; Tailscale only
  (Serve on :80, :8093, :8787; LAN and loopback binds, never `0.0.0.0`); the game PC snapshot reports every service; the
  print queue proves its key from Haven before the tower copy stops.
- 2026-10-17 cc-P155: the web console (`web-console`, game PC, 127.0.0.1:8095 and :8096) and its tailnet node
  (`uoconsole-ts`, planned until Chase makes the auth key); `services.json` 31 services.
- 2026-10-18 cc-P144: the Legion scripts' dev channel (`scripts-dev`, `sl-scripts-dev` on `192.168.1.61:8097` and
  `127.0.0.1:8097`, Tailscale Serve :8097; planned until Chase runs `-Mode SetupDev`) and the official channel in
  `downloads`' `scripts/` folder; `services.json` 32 services (counted from the file).
- 2026-10-18 cc-P163: after the first deploys (Chase, 08:49-09:46). The print queue runs on Haven (since 08:56) and the
  tower copy is retired (no tile); the dev channel, the dashboard and its proxy are running; `prometheus` and `grafana`
  renamed to the real `monitoring-prometheus` and `monitoring-grafana` (tailnet address only) and `npm-admin-tailnet` added,
  all from Discover; NPM watched at its front door; planned, retired and not-installed entries get no tile, the dev store
  says "Stopped, started by hand"; Discover prints mounts and flags ports or images that differ; Portainer on Haven
  (`portainer-haven`, `~/sl-portainer`, volume `portainer_data`, Serve :9000) gets its deploy and roll back buttons.
  `services.json` 33 services (counted from the file).
- 2026-10-19 cc-P182: the web console's Golem buttons; its tailnet listener demands the sidecar's proof; the proof
  forwarder `uoconsole-proof` (in `uoconsole-ts`'s namespace, 127.0.0.2:8097) between Serve and `:8096`.
  `services.json` 34 services.
- 2026-10-26 cc-P668: sl-ddns publishes Haven's address only. `ddns-gate` (`sl-ddns-gate`, game PC, project `uo`) and
  `homeip` (`sl-homeip`, Haven, `192.168.1.61:8098` and `127.0.0.1:8098`, Serve :8098) added, both built and not deployed;
  `ddns` now depends on the gate. `services.json` 36 services (counted from the file).
