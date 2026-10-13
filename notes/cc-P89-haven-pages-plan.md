# cc-P89: Plan the move of Play tests, Shard status and Homepage to Haven (plan only)

Prompt: `D:\UO\cc-prompts\cc-P89-haven-pages-plan.md`. Notes only: nothing was moved, installed or changed on Haven or
on the game PC. Both repos were clean at the start. Not committed (autopilot commits after DONE).

## Headlines

- **Recommended shape: Haven serves the pages, the game PC keeps producing the data it alone can produce.**
  - `sl-play-tests` (Play tests, P90's Ideas, and `/status`) moves to Haven and reads a read-only clone of the docs
    repo that pulls from GitHub every 2 minutes.
  - **Shard status cannot be built on Haven.** `progress.py` needs the ServUO tree (`progress.py:18`), the shard tree
    and the autopilot's folder. So it stays a file built on the game PC at every commit (`Commit-ShardWork.ps1:97-105`),
    pushed, pulled, and served by Haven. Its freshness is unchanged: it is a per-commit page today too.
- **Play-test results and feature ideas: Haven becomes the only writer.**
  - The game PC fetches a copy (`GET /api/export`) just before each commit and writes it into `testing\` as a mirror.
  - With one writer and one read-only mirror, a merge conflict cannot happen. Haven never commits, so it holds no
    GitHub key.
- **Live game-PC facts reach Haven as a pushed snapshot.** A scheduled task on the game PC posts a small JSON every
  60 s: autopilot on/off and state, the queue, container states, and the shard probe.
  - When the game PC sleeps, the snapshot ages, and the pages say "game PC offline since <time>".
  - No Docker API is exposed over the LAN.
- **Outside access: Cloudflare Tunnel + Cloudflare Access** on one hostname (proposed `ops.shatteredlegacyuo.com`) for
  Play tests, Ideas and Shard status.
  - Login works in any browser: email, then a one-time code.
  - No router port is opened. NPM, the public website and Vaultwarden are not touched.
  - Homepage stays home-only. It can be reached away from home over **Tailscale**, which is **not installed on Haven
    today** (checked).
- **Shard-account login: recommended as a later, optional inner layer, never the only gate.**
  - Use a separate web password set in game (`[webpassword`), stored as an Argon2 hash in an account tag, not the game
    password.
  - Cloudflare Access stays the outer gate, so a restarting or wiped test shard never locks Chase out.
  - What it adds over Access alone: per-person roles from AccessLevel, and a path to a player account page later
    (sent to the features chat as a candidate F-item).
- **Haven inspected read-only over SSH (key, no password).** Two findings:
  - Haven **already runs a Homepage (`sl-dashboard`) on :3000**, from a June copy of the shard repo with local edits.
    The repo's `docker\dashboard\README.md` says Homepage runs on Haven, while its compose file and the P83/P85 entries
    point at the game PC's own `sl-dashboard`. **Two Homepages run today.**
  - `cloudflared` and Tailscale are not on Haven.
- **Build plan: 6 prompts** (H1 to H6 in Part C).
  - H1 and H2 are code on the game PC and run unchanged there, so they are safe to land first.
  - H3 is the cutover.
  - H4 is outside access.
  - H5 is Homepage.
  - H6 is the optional shard login.
  - Chase's own steps (Cloudflare dashboard, Tailscale login, a Windows firewall rule, the first deploy on Haven) are
    marked.

## What I could and could not inspect on Haven

**SSH:** `ssh haven` (`~/.ssh/config`: `192.168.1.61`, user `chase`, key `id_ed25519`) worked with `BatchMode=yes`,
with no password prompt. I ran only read-only commands: `hostname`, `uname -a`, `df -h`, `free -h`, `docker ps`,
`docker compose ls`, `docker network ls`, `ss -ltn`, `ls`, and `git log -1` and `git status --short` in
`~/shattered-legacy`. I read no file contents, no `.env` and no NPM data, and printed no git remote (a remote URL can
carry a token).

**Haven facts (2026-10-13):**

| Item | Value |
|---|---|
| Host | `haven`, Debian 13 (kernel 6.12.90+deb13.1), x86_64 |
| Disk | `/` 225 GB, 15 GB used, 199 GB free |
| Memory | 7.5 GiB, 5.7 GiB available; 7.7 GiB swap, unused |
| Listening | 22, 80, 443 (NPM), 3000 (Homepage), 127.0.0.1:81 (NPM admin) |
| Containers | `sl-proxy` (NPM), `sl-vaultwarden`, `sl-website`, `sl-wiki`, `sl-downloads`, `sl-dashboard` (Homepage, 0.0.0.0:3000), `kevins-parts-wp`, `kevins-parts-db` |
| Compose projects | dashboard, downloads, proxy, vaultwarden, website, wiki under `/home/chase/shattered-legacy/docker/`; kevins-parts under `/home/chase/clients/` |
| Networks | `proxy_default`, one `sl-*-net` per site, the kevins-parts nets |
| `~/shattered-legacy` | A git checkout at `44db37b` (2026-06-02), with 5 locally modified files (dashboard, proxy, website and wiki compose files, the website `index.html`, a wiki favicon). **Hand-maintained, not a pulled clone.** |
| Tools | git 2.47.3, python3 present; **`tailscale` not found; `cloudflared` not found** |

**Not inspected, by the task's rules:**
- NPM's proxy hosts, access lists and certificates;
- Haven Homepage's config;
- the Vaultwarden data;
- any `.env`;
- whether Haven's Homepage mounts its own Docker socket.

**Observations on the game PC:**
- Docker Desktop's unauthenticated API answers on **`localhost:2375`** but not on `192.168.1.58:2375`
  (`Test-NetConnection`: True and False). Homepage's `docker.yaml` (`host.docker.internal:2375`) depends on it. It must
  never be opened to the LAN.
- Public DNS over HTTPS (cloudflare-dns.com):
  - the apex and `www`, `get` and `dashboard.shatteredlegacyuo.com` resolve to **216.247.206.76** (this house; DNS
    only, not proxied);
  - `wiki` is Cloudflare-proxied (104.21.20.49, 172.67.191.91);
  - nameservers are Cloudflare (`zac`, `haley`).
  - `Resolve-DnsName -Server 1.1.1.1` on this PC returned **192.168.1.58** for the apex, so something on this network
    answers it locally. It is not the hosts file. Unverified what does (UniFi or a VPN resolver?). Worth knowing
    before adding LAN names.
- `dashboard.shatteredlegacyuo.com` is a **public** DNS name pointing at this house, and is in Homepage's
  `HOMEPAGE_ALLOWED_HOSTS` (`docker\dashboard\docker-compose.yml:14`). Whether NPM routes it anywhere was not checked.
  If it does, Homepage is public today. **Check this first** (Decision 10).

## Part A: what each page needs today

Collected by reading the files (an inventory agent, with the key lines re-read by me). `MIG` is
`D:\UO\shard-migration` and `SL` is `D:\ShatteredLegacy`.

### Play tests (`sl-play-tests`, port 8093)

| Kind | What | Where (file:line) | How often |
|---|---|---|---|
| Runs | `python:3-alpine`, `server.py` | `SL\docker\test-queue\docker-compose.yml:12-15` | always |
| Binds | `192.168.1.58:8093` and `127.0.0.1:8093` | compose:17-18 | |
| Reads | `MIG\notes\cc-P*.md` (P56+, only when the last line is `Pnn DONE`) | `MIG\tools\playtests.py:23,27,71-73,369-377,495-500` | import at start and every 60 s (`server.py:65-68,163-164`; compose `IMPORT_SECONDS`) |
| Reads | `MIG\docs\client-test-queue.md` (once, guarded) | `playtests.py:26,430-483` | once |
| Reads and writes | `MIG\testing\play-tests.json` (atomic tmp and rename, lock `play-tests.json.lock`, stale after 30 s) | `playtests.py:24,264-309,344-352,520-527` | on import change and on every POST |
| Writes | `MIG\testing\SUMMARY.md` | `playtests.py:25,353-356` | with every write |
| Reads | `MIG\tools\playtests.py` (mounted `/app/tools`) | compose:22 | at start |
| Serves | `/`, `/nav.js`, `/status` (`MIG\dashboard.html`, read per request), `/api/items`, `/api/summary` | `server.py:97-129` | per request |
| Accepts | **POST `/api/result`, `/api/bug`, `/api/manual`, `/api/import` with no auth**; 16 KB body cap only | `server.py:19-20,46,132-159` | per click |
| Page polls | `GET /api/items` | `html\index.html:167-170,206-208` | 30 s, skipped while typing |
| Second writer | `MIG\tools\Import-PlayTests.ps1` runs the same importer on the host, under the same lock | `Import-PlayTests.ps1:27` | by hand |
| P90 (queued) | `MIG\testing\feature-ideas.json`, same atomic write, ids `I-NNN` | P90 prompt, "Storage" | per click |

### Shard status (`MIG\dashboard.html`, served at `:8093/status`)

| Kind | What | Where | How often |
|---|---|---|---|
| Built by | `MIG\tools\progress.py`, then `expansion_coverage.py`, then `render_dashboard.py` | `progress.py:454-470` | before every non-dry commit (`D:\UO\Commit-ShardWork.ps1:97-105`, run by the autopilot after each DONE, `cc-autopilot.ps1:207`) |
| Reads | `SL\server\customizations\**\*.cs`, `SL\server\patches\*`, `SL\docker\uo\apply-patches.sh`, `SL\server\tests\**\*.cs`, `SL\VERSION` | `progress.py:33,79-80,96-117,210` | per run |
| Reads | **`D:\UO\ServUO-pub57\Scripts\**`** (game PC only, not in either repo) | `progress.py:18,35,83-85`; `expansion_coverage.py:21,79-80` | per run |
| Reads | `MIG\notes\cc-P*.md` (DONE/STOPPED), `MIG\tools\progress-state.json`, `MIG\tools\modernuo-stems.txt` | `progress.py:20,42-47,75,140-155` | per run |
| Reads | **`D:\UO\cc-autopilot\state.json`, `ENABLED`, `D:\UO\cc-prompts\queue\cc-P*.md`** (game PC only) | `progress.py:165-179` | per run |
| Reads | the `summary` of `MIG\testing\play-tests.json` | `progress.py:186-191` | per run |
| Reads | `SL\docker\test-queue\html\nav.js` (P88, inlined into `DATA:NAV`) | `render_dashboard.py:263-276` | per run |
| Writes | `MIG\tools\progress.json`, `MIG\tools\expansion-coverage.json`, the README blocks, `MIG\dashboard.html` | `progress.py:432,443-451`; `render_dashboard.py:335` | per run |
| Page polls | nothing (static; one script rewrites links and the stale badge) | `dashboard.html` script at the end | none |

### Homepage (`sl-dashboard` on the game PC, port 3000)

| Kind | What | Where | How often |
|---|---|---|---|
| Runs | `ghcr.io/gethomepage/homepage:latest` (1.13.1), `3000` on all interfaces | `SL\docker\dashboard\docker-compose.yml:3,7` | always |
| Mounts | `./config` read-write; **`/var/run/docker.sock:ro`**, apparently unused because `docker.yaml` uses TCP | compose:9-11; `config\docker.yaml:1-3` | |
| Polls | Docker API `host.docker.internal:2375` (`server: my-docker`) for `sl-modernuo` and `atm10` stats | `services.yaml:7-14,118-128` | Homepage default |
| Polls | `192.168.1.58:8092/status.json` (30 s), `migration.json` (300 s), `downloads.json` (300 s) | `services.yaml:16-74` | as listed |
| Polls | `192.168.1.58:8093/api/summary` | `services.yaml:79-96` | 60 s |
| Polls | ATM10 `192.168.1.58:8091/...` (5 widgets) | `services.yaml:130-203` | 15 to 60 s |
| Pings and site monitors | 192.168.1.58 and 192.168.1.61, `:80`, `:8092` | `services.yaml:14,37,109,115,125,148,208-230` | default |
| Browser loads | `http://<host>:8093/nav.js` (P88) | `config\custom.js:9-15` | per page load |

### Feeds the pages use (stay on the game PC)

| Feed | Served by | Written by | How often |
|---|---|---|---|
| `status.json` | `sl-uo-status` nginx :8092 (`uo-status\nginx.conf:15-20`) | `ShardStatusPublisher.cs` in the shard | 30 s |
| `shards.json` | the same (`:32-37`) | `sl-shard-probe` `probe.py` (`OUT=/status/shards.json`; probes :2593 and :2594) | 30 s |
| `migration.json` | the same (`:24-29`) | `SL\scripts\Build-MigrationStatus.ps1` | by hand; last 2026-09-29 |
| `downloads.json` | the same (`:41-46`) | `SL\scripts\Build-DownloadStatus.ps1` | nightly task (unverified) |

### The Shard Console (`SL\scripts\Shard-Console.ps1`)

| Tile or action | Reads | Where | How often |
|---|---|---|---|
| PLAY TESTS tile | `MIG\testing\play-tests.json` from disk | `Get-ConsoleConfig` `PlayTestsFile` :250; `Get-PlayTestGlanceNow` :3539-3546 | 30 s refresh |
| AUTOPILOT tile and tab | `D:\UO\cc-autopilot\ENABLED`, `state.json`, the log, `D:\UO\cc-prompts\queue\` | :247; `Get-AutopilotFacts` :3505-3537 | 30 s |
| `links.playtests`, `.status`, `.dashboard` | `http://localhost:8093/`, `/status`, `http://localhost:3000/` | :251-254; `Get-LinkPlan` :2856-2864 | per click |
| Status feed | `http://localhost:8092/status.json` | :214 | 30 s |

### P88's menu

- **`nav.js`:** the `PAGES` table (`:16-20`) has every `host: null` (the browser's host) and ports 8093/8093/3000.
  `FALLBACK_HOST = '192.168.1.58'` (`:22`).
- **`custom.js`:** `NAV_AT = { host: null, port: 8093 }` (`:9`).
- **`render_dashboard.py`:** `LAN_HOST` (`:179`) and `NAV_JS` (`:263`).

## Part B: the design

### 1. Repo data to Haven

**Recommend: a dedicated read-only clone of `shard-migration` on Haven, pulled every 2 minutes by a tiny container.**
- The container is `alpine/git` in a loop: `git fetch` then `git reset --hard origin/main`, over anonymous HTTPS,
  since both repos are public.
- Its path is `/srv/sl-ops/repo/shard-migration`, **not** `~/shattered-legacy`, which has local edits and is how
  Haven's stacks are deployed today.
- `sl-play-tests` mounts it read-only for `notes/`, `docs/`, `tools/` and `dashboard.html`.
- The shard repo is needed only for `nav.js` and the service code itself. Ship those inside the service's own deploy
  folder (as Haven's other stacks are deployed), not by pulling the shard repo.

| | |
|---|---|
| Cost | One container. Each fetch is a few KB when nothing changed; the docs repo is small. No credentials. |
| Lag | The autopilot pushes right after each DONE. A new prompt's play tests appear on Haven within about 2 minutes plus the 60 s import, against 60 s today. |
| GitHub down | The pull fails and the clone keeps its last state. The page shows "repo as of <last pulled commit time>" (a new field from `git log -1`). Results keep working, because results do not depend on the clone (item 3). |

**Alternatives:**
- **Push from the game PC** (rsync or scp after each commit): fewer moving parts on Haven, but it needs a write key
  from the game PC to Haven and couples every commit to Haven being up. Rejected.
- **A GitHub webhook to Haven:** instant, but it needs a public endpoint. Rejected.
- **A systemd timer on the host** instead of a container: fine too. The container keeps it inside compose like the
  rest of Haven. Chase's choice (Decision 4).

### 2. Game-PC-only data to Haven

| Item | Recommendation | Why |
|---|---|---|
| Autopilot on/off, `state.json` (running prompt, since), queue listing, latest DONE | **Pushed snapshot** | Files on `D:\`; nothing else can read them. |
| Container states (`sl-modernuo`, `sl-modernuo-test`, `sl-play-tests` while it still runs, `sl-uo-status`, `atm10`) | **Pushed snapshot** (`docker ps --format json`: name, state, started, image) | No Docker API leaves the PC. |
| Shard up/down (2593, 2594) | **Read `http://192.168.1.58:8092/shards.json` from Haven** | Already served on the LAN by `sl-uo-status`, every 30 s. |
| Player count and uptime | **Read `:8092/status.json`** | Same. |
| Play-test counts for the Console tile | The Console reads Haven's `/api/summary`, falling back to the mirror file | Item 7. |

**The snapshot:**
- `SL\scripts\Publish-GamePcSnapshot.ps1`, a Windows scheduled task every 60 s as Chase (not SYSTEM, so it can read
  `D:\UO`).
- It POSTs about 2 KB of JSON to `http://192.168.1.61:<ingest port>/api/ingest/gamepc` with a bearer token.
- The token is in `D:\UO\haven-ops-token.txt` on the PC and in an env file on Haven; neither is in git.
- **The ingest port is bound on Haven's LAN address only, never routed by the tunnel.** Haven stores the snapshot with
  its received-at time.

**When the game PC sleeps:**
- The snapshot stops. Any page section built from it shows **"Game PC offline since 14:32 (last snapshot)"** once the
  snapshot is older than 3 minutes.
- Feeds from `:8092` that do not answer show "game PC offline" the same way, never a stack trace or a blank widget.
- The play-test list itself still works: the notes come from the clone, the results live on Haven.

**Alternatives:**
- **A read-only Docker socket proxy** (`tecnativa/docker-socket-proxy` with `CONTAINERS=1`, everything else 0) on the
  game PC, published on the LAN. Real container stats for Homepage, but it adds a Docker API listener on the game
  PC's LAN address, and widgets error rather than say "offline". Kept as the option if Chase wants CPU and memory
  graphs (Decision 6).
- **Tailscale between the two machines:** not needed, since both are on the same LAN, and it is not installed on
  Haven.

### 3. Play-test results and ideas going back into git

**Recommend: Haven is the only writer; the repo copy is a mirror the game PC refreshes right before each commit.**
- On Haven, `play-tests.json`, `SUMMARY.md` and P90's `feature-ideas.json` live in a Haven data volume
  (`/srv/sl-ops/data/testing/`). The importer reads notes from the clone and writes there. Every Pass, Fail, Bug,
  manual item and idea writes there, under the existing lock.
- New endpoint **`GET /api/export`** (LAN ingest port, same token) returns the three files.
- **`Commit-ShardWork.ps1`**, before it runs `progress.py`, fetches the export and writes the three files into
  `MIG\testing\`. Then `progress.py` counts from current data and the commit carries the latest results.
  - If Haven does not answer, it keeps the previous mirror and prints "play-test mirror not refreshed (Haven
    unreachable)". The commit is never blocked.

**Why a conflict is impossible:**
- Exactly one process ever changes those files: the Haven service, under its lock.
- The game PC only ever replaces its copy wholesale with Haven's.
- The repo copy is never edited by hand. To enforce that, H2 makes `Commit-ShardWork.ps1` warn when `testing\` differs
  from the last export for any reason other than a fresh export.
- `Import-PlayTests.ps1` and the game PC's `sl-play-tests` are retired at cutover. Until then the game PC is the only
  writer, as today.
- Haven never commits, so there are never two committers on `main`.

**Seeding and cutover:**
- Stop the game PC service.
- Copy the three files from `MIG\testing\` to Haven once, then start Haven's.
- A mark made in the gap is impossible, because the old service is stopped first.

**Alternatives:**
- **Haven commits and pushes with a deploy key limited to the docs repo.** Results reach git within minutes even when
  the game PC sleeps. But it makes two committers on `main` (the autopilot pushes too), so every push from either
  side needs fetch, rebase and retry. A deploy key on an internet-reachable box also writes to a public repo.
  Rejected: more failure modes for a lag that does not matter (the overseer reads results at commit time anyway).
- **Keep writing on the game PC, Haven proxies to it:** the page dies whenever the game PC sleeps, which defeats the
  point of the move. Rejected.

### 4. Homepage on Haven

**Recommend: one Homepage, Haven's, rebuilt from the repo config; retire the game PC's `sl-dashboard` after it works.**
- **Game PC containers:** `customapi` widgets reading Haven's snapshot (`/api/gamepc` on the ingest port, LAN), with
  mappings for state and uptime. They read "offline since" when the PC sleeps.
  - The `server: my-docker` entries (`services.yaml:7-14,118-128`) go away. They would need the game PC's Docker API
    on the LAN.
  - The socket proxy (item 2) is the alternative if live CPU and memory matter.
- **Shard widgets:** keep polling `http://192.168.1.58:8092/status.json`, `shards.json` and so on over the LAN from
  Haven. `sl-uo-status` stays on the game PC.
- **Haven's own containers:** yes, show them (Vaultwarden, website, wiki, NPM up or down). Use a read-only socket
  proxy on Haven exposing container listing only, rather than mounting Haven's raw socket into Homepage.
  - Homepage is home and tailnet only, so up/down for Vaultwarden is fine to show.
  - No Vaultwarden widget with credentials.
- **Reach:**
  - At home: `http://192.168.1.61:3000`.
  - Away: over Tailscale, after Chase installs it on Haven.
  - Not through the Cloudflare tunnel: it lists every container and the home lab's layout.

### 5. Names and access

**At home:**
- Use the same `https://ops.shatteredlegacyuo.com` as away. The tunnel works from inside the house too, so there is
  one URL and one login everywhere.
- Homepage stays `http://192.168.1.61:3000`. No local DNS name is needed for that.
- If Chase wants LAN names later, UniFi's local DNS records (for example `dash.home.arpa`, the reserved home-network
  domain) beat per-device hosts entries. But see the apex observation above: something on this network already
  rewrites `shatteredlegacyuo.com` locally. Find it first.

**Away, compared:**

| | Tailscale | Cloudflare Tunnel + Access | NPM public host + basic auth |
|---|---|---|---|
| Login on a phone | Tailscale app signed in; then just the URL | Any browser: enter email, then the 6-digit code mailed to it; a session cookie for a set time (24 h proposed) | Basic-auth prompt every session |
| Borrowed or school PC | Usually impossible (needs an install) | Works | Works |
| Router | No ports | No ports (outbound tunnel only) | **Opens or reuses 443 to a staff page** |
| Exposure | None public | Only Cloudflare's login page is public; the origin is not reachable without passing Access | The origin is on the internet; basic auth over the same NPM that fronts Vaultwarden |
| Brute force | n/a | Email code to a fixed allow-list; Cloudflare rate-limits | Password guessing against NPM |
| Already in place | Not on Haven | Domain on Cloudflare; `cloudflared` used before (not on Haven now) | NPM on Haven |
| Weakest point | Device install | Email account security | Everything above; one NPM mistake exposes the page |

**Recommend:**
- Cloudflare Tunnel + Access for Play tests, Ideas and Shard status.
- Tailscale as the admin path (SSH and Homepage).
- NPM public only if both fail.

**The tunnel in detail:**
- A `cloudflared` container on Haven, in its own compose project, on a new network shared only with `sl-play-tests`.
  It routes `ops.shatteredlegacyuo.com` to `http://sl-play-tests:8000`.
- An Access application on that hostname, with policy "emails in {Chase's address}", plus his daughter's if wanted
  (Decision 2). Session duration 24 h.
- Nothing about NPM, the website, the wiki or Vaultwarden changes. They keep their own hostnames, certificates and
  ports. The tunnel never touches `proxy_default`.

**Hardening for write actions (Pass/Fail/Bug/manual/ideas):**
- **The service validates Cloudflare's `Cf-Access-Jwt-Assertion` header** on every request through the tunnel
  hostname: signature from the team's public certs, `aud` equal to the application's tag, not expired. A request that
  reaches the container any other way gets no writes.
  - Python's standard library cannot verify RS256, so H4 adds one small dependency (`PyJWT` with `cryptography`) or
    has `cloudflared` itself enforce it (its `access` setting on the ingress rule). **Prefer `cloudflared`'s own check
    plus the header check.**
- **Writes stay JSON POSTs** with `Content-Type: application/json`. A cross-site form cannot send that without a CORS
  preflight the server never grants, so add an `Origin` check equal to the ops hostname.
- **Rate limits:** the existing 16 KB body cap, plus 30 writes a minute per Access identity in the service. Cloudflare's
  free WAF rate-limit rule is a second layer if wanted.
- **The writer's identity:** record the Access email in each result (`by`), so Chase and his daughter are told apart.

**What changes because the pages stop being LAN-only:**
- **`nav.js` `PAGES`:** a page can now have a full `url` (`https://ops.shatteredlegacyuo.com/`, `.../status`, P90's
  `.../ideas`) instead of host and port.
  - Dashboard gets `lanOnly: true` and is shown only when the page was reached from a LAN or tailnet address.
  - `FALLBACK_HOST` becomes the ops URL.
- **`custom.js` `NAV_AT`:** points at `https://ops.shatteredlegacyuo.com/nav.js`.
  - Reached from Homepage at home, that script sits behind Access. Either serve `/nav.js` with an Access **bypass**
    policy (it holds no data), or have Homepage load it from Haven's LAN port. **Recommend the bypass on `/nav.js`
    only.**
- **`render_dashboard.py`:** `LAN_HOST` goes. The inlined menu needs no host once the URLs are absolute.
- **`index.html` and P90's page:** their API calls are already relative, so no change.
- **`server.py`:** gains the Access check, the export and ingest endpoints on a separate LAN-only port, and new data
  paths (`PLAYTESTS_DATA` separate from the clone root).
- **The docker-compose port bindings:** the service publishes nothing to the internet. One LAN port on Haven
  (`192.168.1.61:8094`, say) carries ingest and export with the token, and also serves the read-only page for LAN use
  without Access, writes refused. Plus the tunnel network.
- **The Console:** item 7.

### 5b. Logging in with the UO shard account

**How the shard checks a password (pinned ModernUO, read 2026-10-13):**
- Passwords are stored hashed: `Account._passwordAlgorithm` and `_password`
  (`Projects\UOContent\Accounting\Account.cs:29-33`).
- The default algorithm is **Argon2id**, t=1, m=16 MiB, p=1
  (`Accounting\Security\AccountSecurity.cs:40-46`; `Argon2PasswordProtection.cs:26-32`).
- `Account.CheckPassword` (`Account.cs:417-434`) verifies, then **rehashes and rewrites the account on success** when
  the algorithm or parameters changed. So it mutates game state and must run on the game loop.
- Account lookup is a plain `Dictionary` (`Accounts.cs:13,32`), also not thread-safe.
- ModernUO's own off-loop pattern is `PasswordWorker`: snapshot on the loop, verify on a worker, `Core.LoopContext.Post`
  back (`Security\PasswordWorker.cs:25,201,205-235`; `AccountHandler.cs:400-441`).
- **The UO client sends the password in plain text** inside packet 0x80 (`ReadLatin1Safe(30)`,
  `Network\Packets\IncomingAccountPackets.cs:560-561`). The client's own Twofish login crypto is obfuscation, not TLS,
  and is off for ClassicUO with encryption disabled.
- **No per-account lockout exists.** The only limiter, `IPRateLimiter` (`Server\Network\IPRateLimiter.cs`), counts
  connection attempts per IP and **exempts private-network addresses** (`:59-63`). So a check called from Haven
  (192.168.1.61) would get no protection from it.
- AccessLevel is `Player, Counselor, GameMaster, Seer, Administrator, Developer, Owner`
  (`Server\Mobiles\Mobile.cs:141-150`). There is no VIP level.
- Accounts carry tags: `Account.SetTag`/`GetTag` (`Account.cs:675-709`), saved with the account.
- No HTTP listener exists in ModernUO or our customizations. `ShardStatusPublisher.cs` only writes a file.

**Proposed endpoint (ours, `server\customizations\WebAuth\`, H6):**
- **Listener:** a `TcpListener` speaking one tiny JSON-lines protocol (one request line, one reply line). Only Haven's
  service ever calls it, so no HTTP stack is needed.
  - It binds to a port set in `Configuration` (`webAuth.bind`, default off).
  - Docker publishes it **only on `192.168.1.58`**, and a Windows firewall rule allows it only from `192.168.1.61`
    (Chase sets the rule).
  - Never routed by NPM or the tunnel; never called by a browser, only by Haven's service.
  - Haven authenticates to it with a second shared token.
- **Request:** `{name, password, clientIp}`.
- **Response:** `{ok: true|false, accessLevel: "GameMaster"}`, or `{ok:false, reason:"locked"}`. **Never a hash**, never
  whether the account exists (a wrong name and a wrong password look the same).
- **What it checks:** the account's **web password**, not the game password (see Risks):
  - on the loop (`LoopContext.Post`), look up the account and copy the `WebPasswordHash` tag and AccessLevel;
  - verify off-loop with the same Argon2 implementation;
  - nothing is written, so no rehash side effect, and `CheckPassword` is never called.
- **Limits:**
  - per account, 5 failures in 15 minutes locks that account's web login for 15 minutes;
  - per client IP (the forwarded `clientIp`, which Haven takes from Cloudflare's `Cf-Connecting-IP`), 20 failures an
    hour locks that IP for an hour;
  - a global cap of 10 requests a second.
  - All in memory, all reset by a restart. Acceptable, because Access is the outer gate.
- **Logging:** every attempt, as time, account name, client IP, result and reason, to its own log file and the
  console. Never the password.
- **Which shard:** the **test shard** (`sl-modernuo-test`, 2594), the only one in use until the fresh-world wipe. After
  the wipe, point it at live by config (`webAuth.enabled` in the live shard's settings, off in test). Both shards carry
  the code; config decides which answers.

**Who gets in where:**
- **Staff pages (play tests, ideas, shard status): `GameMaster` and up.** Counselor is a player-help role and should
  not mark build results. Chase's account is Owner or Administrator.
- **Chase's daughter:** ideas yes. Play tests: **ask** (Decision 2). Recommend yes if she play-tests, with her results
  marked "by" her.
- **Later, players:** the public website could use the same login for an account page (characters, achievements,
  donation status). That is a separate feature with its own threat model (public, many accounts). **Candidate F-item
  for the features chat:** "Player website login (account page) using the shard's web password", not planned here.

**Sessions:**
- Haven issues an HMAC-signed cookie: name, AccessLevel, expiry. Lifetime 8 hours; `Secure`, `HttpOnly`,
  `SameSite=Lax`.
- `/logout` clears it. The signing key lives in Haven's env file.
- HTTPS comes from the tunnel.

**Fallback when the shard is down (restart, crash, wipe):**
- **Recommend Cloudflare Access as the outer gate, always, and the shard login inside it as optional.**
- When the auth endpoint does not answer, Access-authenticated users on the allow-list get in with the role mapped from
  their Access email (Chase = Administrator). The page shows a banner: "shard login unavailable; signed in by
  Cloudflare".
- Chase can never be locked out by a restarting test shard.
- The alternative, a break-glass staff password stored on Haven, is one more secret to keep and gives nothing Access
  does not.

**Risks:**
- UO clients send passwords in plain text, and players reuse passwords. A website accepting the **game** password
  would turn any leak of the site (or of a sniffed game login) into both.
- **Recommend a separate web password, set in game with `[webpassword`** (typed twice). It follows ModernUO's own
  `[Password` command (`AccountHandler.cs:59-193`) and our `CommandSystem.Register` pattern
  (`ClusterFSelfResurrect.cs:12`). It is stored as an Argon2 hash in the `WebPasswordHash` account tag, the only thing
  the endpoint ever reads.
  - No web password set means no web login.
  - A world wipe drops it with the account, which is correct.

**Cloudflare Access alone, compared:**
- Access alone is enough for two people. It gives a strong login with no shard code.
- **The shard login adds:**
  1. Roles from AccessLevel instead of a hand-kept email list.
  2. Results attributed to an in-game identity.
  3. The groundwork for player-facing logins later.
- **It costs** a network listener inside the shard, a new command, and lockout code.
- **Recommendation: do H1 to H5 with Access alone; build H6 only when the player account page (the F-item) is
  wanted.** Until then it adds risk for little.

### 6. What stays on the game PC

- **Stays:**
  - the shard containers (`sl-modernuo`, `sl-modernuo-test`);
  - `sl-uo-status` (8092: it serves the public player status through Haven's NPM `/api/` route, per
    `SL\docker\uo-status\README.md:65`, unverified on Haven) and `sl-shard-probe`;
  - `sl-ddns`;
  - the autopilot (`D:\UO\cc-autopilot\`), both repos, `ServUO-pub57`, `ModernUO-pinned`;
  - `Commit-ShardWork.ps1`, `progress.py` and the dashboard build;
  - the Shard Console.
- **Nothing the shard needs moves.** The shard reads none of the three pages or their files. The only shard-side
  addition anywhere in this plan is H6's optional endpoint.
- **Leaves at cutover:** `sl-play-tests` (to Haven), and later `sl-dashboard` (Haven's replaces it).
  `Import-PlayTests.ps1` is retired.

### 7. Console and links

- **`Get-ConsoleConfig`:**
  - `PlayTestsUrl` becomes `https://ops.shatteredlegacyuo.com/` and `StatusUrl` becomes `.../status`;
  - `DashboardUrl` becomes `http://192.168.1.61:3000/`;
  - new `OpsApi` is `http://192.168.1.61:8094`.
- **The PLAY TESTS tile:** reads `OpsApi/api/summary` with the token. If Haven does not answer, it falls back to the
  mirror `testing\play-tests.json` and says "(from the last commit; Haven unreachable)".
- **The AUTOPILOT tile:** unchanged (local files).
- **New tile line or tooltip:** "Haven: snapshot received 12 s ago", so Chase can see the push working.
- **`nav.js`, `custom.js`, `render_dashboard.py`:** as in item 5.
- **Haven Homepage `services.yaml`:**
  - the Play tests and Shard status hrefs go to the ops URLs;
  - the summary widget reads `http://sl-play-tests:8000/api/summary`, or the LAN port;
  - game PC tiles move to the snapshot.

### 8. Rollback (minutes)

1. On Haven: `docker compose stop` for `sl-play-tests` (and `cloudflared`, if the page should vanish outside).
2. On the game PC: `Commit-ShardWork.ps1 -DryRun` refreshes the mirror from Haven's export (or run the export fetch by
   hand) so the latest results are in `testing\`, then `Start-TestQueue.ps1`. The old service runs again on
   `192.168.1.58:8093` with current data.
3. Point the links back: one commit reverting H3's config change (`nav.js` `PAGES`, `custom.js`, the Console URLs).
   H1 and H2 keep a `PLAYTESTS_MODE=local|haven` switch so the code itself needs no revert.
4. Homepage: the game PC's `sl-dashboard` is left stopped, not removed, until two weeks after cutover, so
   `docker start sl-dashboard` brings it back.

## Part C: the build plan

Each H-prompt is one autopilot run. **(C)** means Chase must act, at Haven's terminal or a web console. **(CC)** means a
prompt can do it. **(D)** means it needs a decision first.

1. **H1 (CC): make `sl-play-tests` host-agnostic, still running on the game PC.**
   - `PLAYTESTS_DATA` separate from the notes root.
   - `GET /api/export` and `POST /api/ingest/gamepc`, plus `/api/gamepc`, on a second, token-guarded listener.
   - "Game PC offline since" and "repo as of" fields.
   - `nav.js` URL mode with `lanOnly`.
   - An optional Cloudflare Access check (off unless configured).
   - Writer identity in each result.
   - Proves: unit tests for the export round-trip and the token refusal; a scratch run; the game PC page behaves
     exactly as today with the defaults.
   - P90's `feature-ideas.json` follows the same data path (P90 runs before H1, so H1 adapts it).
2. **H2 (CC, with one C step): the game PC side.**
   - `Publish-GamePcSnapshot.ps1` and its scheduled-task installer **(C: run the installer once)**.
   - `Commit-ShardWork.ps1` refreshes the mirror from `/api/export` before `progress.py`, never blocking.
   - Console URLs and the tile from config with fallback.
   - Proves: a dry run against a scratch Haven-mode service on the game PC; the commit preflight shows the mirror
     refresh; the tile falls back when the service is stopped.
3. **H3 (CC writes, C deploys): cutover on the LAN.**
   - `docker\ops\` compose for Haven: `sl-play-tests`, the git-pull container, the data volume, the LAN port
     `192.168.1.61:8094`.
   - A `Deploy-HavenOps.ps1` in the style of `D:\UO\haven-migration\`.
   - A cutover script that stops the game PC service, seeds Haven's data from `testing\` and starts Haven's.
   - **(C)** Run the deploy over SSH (or grant the prompt SSH write for this one run, Decision 8).
   - Proves: the page on `http://192.168.1.61:8094/` is read-only; a Pass marked on Haven appears in the next commit's
     `testing\play-tests.json`; the game PC sleeping shows "offline since"; rollback rehearsed once.
4. **H4 (C, then CC): outside access.**
   - **(C)** In Cloudflare Zero Trust: create the tunnel (copy its token into Haven's env file), add the public
     hostname `ops.shatteredlegacyuo.com` to `http://sl-play-tests:8000`, create the Access application and policy
     (emails), and add a bypass for `/nav.js` **(D: hostname, emails, session length)**.
   - **(CC)** The `cloudflared` compose service, enforcement of the Access JWT on writes, the Origin check, per-identity
     rate limits, and the switch of `nav.js` and the Console to the ops URLs.
   - Proves: from a phone on mobile data, the login page, then the code, then the list; a write without Access refused
     (curl to the LAN port); Vaultwarden, the website and the wiki unchanged (their URLs answer as before; NPM
     untouched).
5. **H5 (CC writes, C deploys): one Homepage on Haven.**
   - A `services.yaml` for Haven: snapshot widgets for the game PC, `:8092` widgets, Haven containers through a
     read-only socket proxy, the ops links, and `custom.js` from the ops `nav.js`.
   - The game PC's `sl-dashboard` stopped, not removed.
   - **(C)** Install Tailscale on Haven and log in, to use Homepage away **(D: whether at all)**.
   - Proves: every tile renders at `http://192.168.1.61:3000`; with the game PC asleep, its tiles read offline and
     nothing errors.
6. **H6 (optional, D): shard web login.**
   - `[webpassword`, the `WebAuth` endpoint (test shard), Haven's inner login with sessions, the Access fallback, and
     the AccessLevel gate.
   - Needs a shard build and tests (lockout, no hash in any response, no existence leak).
   - **(C)** The Windows firewall rule allowing only Haven to the auth port.
   - Proves: the facts and a client test, `[webpassword` then a web login. Restart the test shard mid-session and still
     get in through Access.

Order: H1 and H2 can land any time and change nothing visible. H3 is the move. H4 can follow the same day. H5 any time
after H3. H6 only on demand.

## Decisions for Chase

1. **Approve the shape** (Haven serves; the game PC builds Shard status and pushes a snapshot; Haven is the only writer
   of results, mirrored into git at commit). *Recommended: yes.*
2. **Who gets in:** Chase only, or Chase and his daughter? And should she see play tests as well as ideas?
   *Recommended: both, both pages, each result marked by who made it.*
3. **The outside hostname.** *Recommended: `ops.shatteredlegacyuo.com`, Access by email one-time code, 24 h sessions.*
4. **The repo pull on Haven:** a git-pull container, or a systemd timer? *Recommended: the container (it stays in
   compose); every 2 minutes.*
5. **Shard login (H6) now or later?** *Recommended: later, when the player account page is wanted. Access alone covers
   staff. If built, use a separate `[webpassword`, never the game password.*
6. **Game PC container stats on Homepage:** status from the snapshot (no new listener), or live CPU and memory through
   a read-only Docker socket proxy on the LAN? *Recommended: the snapshot.*
7. **Haven containers on Homepage** (Vaultwarden, website, wiki, NPM up or down): *Recommended: yes, through a
   read-only socket proxy; Homepage stays home and tailnet only.*
8. **Deploys on Haven:** keep them Chase-run (paste one command), or allow a CC prompt SSH write access for named
   deploy scripts only? *Recommended: Chase-run for H3 and H5; reconsider after.*
9. **Haven's stale Homepage and `~/shattered-legacy` checkout** (June, with local edits): replace that Homepage in H5,
   and leave the checkout alone (it is how the website, wiki and proxy are deployed)? *Recommended: yes; and record in
   `docker\dashboard\README.md` which Homepage is real until then.*
10. **`dashboard.shatteredlegacyuo.com`** resolves publicly to this house and is in Homepage's allowed hosts. Check
    whether NPM routes it. If it does, Homepage (container details) is public today. *Recommended: check NPM's proxy
    hosts now; if routed, remove the host or put it behind Access.*
11. **Homepage's "Migration status" entry** (from P88): rename to "Public progress page" when Haven's Homepage is
    built. *Recommended: yes.*

## For the features chat (candidate F-item, not planned here)

**Player website login:** players sign in to the public website with their shard account name and a web password set
in game (`[webpassword`), to see an account page: characters, achievements, donation status. It reuses H6's endpoint
if built, but is public and needs its own threat model (many accounts, password spraying, lockout abuse). Raised by
Chase on 2026-10-13 in cc-P89's prompt.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run after this notes
file was written:

```
=== code  (D:\ShatteredLegacy) ===
  nothing to commit
=== docs  (D:\UO\shard-migration) ===
  3 file(s) pending: testing/SUMMARY.md, testing/play-tests.json, notes/cc-P89-haven-pages-plan.md
  dry run: would add, commit and push

Repo Result
---- ------
code clean
docs dry run
```

**The two `testing\` files are not mine.** The live play-test importer rewrote them after the P88 commit, when P88's
notes said DONE. They are the only changes besides this notes file. No patch notes or VERSION change (notes only).
`progress.py` was not run by hand, because this task changes no counted file; `Commit-ShardWork.ps1` runs it before
the commit anyway.

P89 DONE
