# cc-P109: Move the Sunflower opener print queue (wait queue) to Haven

2026-10-14. Prompt: `D:\UO\cc-prompts\cc-P109-haven-print-queue.md`. Built and proved on this PC. **Nothing was deployed
to Haven, nothing connected to Haven, and nothing was pushed to the Sunflower site.** The real queue and its data on
this PC were not touched. Customer data: this note gives counts and shapes only.

## Headlines

- **Version control:** the print queue is now its own git repo, `C:\dev\sunflower\print-queue` (new, no remote,
  **nothing committed**: see For Chase). Recommended over `sunflower-devstack` because that repo has no remote either,
  and it has someone's work in progress uncommitted (17 entries in `git status --short`, 12 of them staged, under
  `import\`, `plugin\` and others) that a commit there would sweep in. `data\`, `data.moved-*\`, `logs\`, `keys\`, `*.env`, key-like names and the old
  `index.backup-*.html` copies are ignored, proved with `git check-ignore -v` (below). `index.html` carries no sample
  orders or e-mail addresses (grepped).
- **Container:** `Dockerfile` (python:3-alpine, standard library, plus `openssh-client` and `tzdata`), `start.sh`,
  `docker-compose.yml`, `.dockerignore` (only the three files the image needs, so customer data never enters a build
  context). On Haven: `~/sunflower-print-queue/{stack,data,logs,keys}`, compose project `sunflower-pq`, container
  `sunflower-print-queue`, published on `192.168.1.61:8787` (LAN only), `restart: unless-stopped`, a health check.
  The 60 s auto-push and the daily backup are the server's own, unchanged.
- **Its own SSH key:** the deploy makes an ed25519 key **on Haven** the first time and prints only its **public** half,
  once. Chase's key is never named or copied. `ssh_config` (HostName, User and Port from this PC's `sunflower-live`
  alias, `StrictHostKeyChecking yes`) and `known_hosts` (the host keys **this PC already trusts** for that host, three
  of them today) are written to Haven's `keys\`: the host key is pinned, never accepted. With no trusted key here the
  deploy refuses.
- **Loud until Hostinger has the key:** a missing key fails at start (log line `PUSH NOT POSSIBLE ...`, page red at
  once), and any failed push puts a red line on the page: `Lead-time page not updated since <last good push>. Last push
  failed (<time>): <why>`. The last good push is kept in `data\push-state.json`, so it survives restarts and the move.
- **Data move, once, inside the deploy:** stop the game PC server, copy `data\*.json` to Haven, check each by SHA-256
  and the order count through the page's own `/api/state`, then rename this PC's `data` to `data.moved-YYYYMMDD`
  (kept). Any failure before the rename stops Haven's container, sets Haven's copy aside, and starts the game PC
  server again. Haven's data is never overwritten: a second deploy skips the move.
- **One click:** two new buttons on the Shard Console's Websites tab, **Print queue: deploy** and **Print queue: roll
  back**, through P101's helper and allowlist (`websites.json` deploys `print-queue`, `print-queue-rollback`, each a
  one-line launcher in `D:\UO\haven-migration`), after the phrase `deploy to haven`; then the window reads Haven,
  prints the plan and waits for the typed word (`deploy` or `roll back`). A **Print queue** site row was added too.
- **Rollback** takes Haven's data back (SHA-256 checked), stops and sets aside Haven's copy, starts the game PC server
  from `Start Print Queue.cmd`, and points the shortcut back. If Haven cannot be read it offers the newest
  `data.moved-*` after a typed `roll back anyway`.
- **Desktop shortcut:** the deploy repoints `Desktop\Sunflower Print Queue.lnk` at the Haven page; the rollback points
  it back at `Start Print Queue.cmd`, which is kept as the rollback path. Changed only when the real deploy runs.
- **Proof:** the whole Deploy and Rollback ran on this PC's Docker in a scratch folder against a **stub SSH server**
  (an alpine sshd whose `wp` only records what it is sent), with a scratch copy of the data. Every check passed;
  details below. Console facts: 302 before, **304 after** (2 new `P109_*`, 7 updated P101 facts).
- **Two bugs of mine caught by the proof** (below), both fixed before the final run.

## The print queue as found (re-checked)

`C:\dev\sunflower\print-queue`: `queue_server.py` (283 lines), `index.html`, `Start Print Queue.cmd`
(`py queue_server.py`), `data\` (`queue.json` and six daily `backup-YYYY-MM-DD.json`; 6 orders), `logs\push.log`, two
`index.backup-*.html`. **Not in any git repo** (`git rev-parse` failed). Not running at the start (nothing listening on
8787). `Desktop\Sunflower Print Queue.lnk` targets `Start Print Queue.cmd`. `~\.ssh\config` has `Host sunflower-live`
with HostName, User and Port 65002; `known_hosts` has its ed25519, ecdsa and rsa keys. As the prompt said.

## What changed

**Sunflower repo, `C:\dev\sunflower\print-queue` (uncommitted, see For Chase)**
- `queue_server.py`: environment variables move it into a container; **unset, it behaves as before** (`PQ_DATA`,
  `PQ_LOGS`, `PQ_BIND` default 127.0.0.1, `PQ_PORT` default 8787, `PQ_SSH_CONFIG` as `ssh -F`, `PQ_KEY`,
  `PQ_HOST_LABEL` default chases-tower). New: `lastOk` in the push state, saved to `push-state.json`; the missing-key
  check at start and in every push. The snippet's first line now says where it was pushed from (`... on haven.`); its
  marker, which the site's PHP checks, is unchanged.
- `index.html`: `showPush` only: the red "not updated since" line, and "Website last updated" after a restart.
- New: `Dockerfile`, `start.sh` (copies `/keys` into the user's own `~/.ssh` with 600, since ssh refuses keys others can
  read and a bind mount keeps the host's modes), `docker-compose.yml`, `.dockerignore`, `.gitignore`, `.gitattributes`
  (LF for the shell and Docker files), `haven/Deploy-PrintQueue.ps1` (343 lines: Discover, Deploy, Rollback; `-DryRun`;
  refuses SYSTEM; `-Local` for the proof only, which refuses any non-scratch root, PC folder or shortcut).

**`D:\UO\haven-migration` (not a repo):** `Deploy-PrintQueue.ps1` and `Deploy-PrintQueue-Rollback.ps1`, one-line
launchers like P107's.

**Shard repo `D:\ShatteredLegacy` (committed by the queue)**
- `scripts/websites.json:23` the Print queue site (on Haven, LAN URL, deploy `print-queue`); `:32-33` the two deploys.
- `scripts/Shard-Console.ps1`: the phrase `:838`, the dialog title `:855`, the two actions `:1093-1094`, their
  tooltips `:1313-1314`, the plan `:4067` (the same branch as P107's ops deploys) and its log line `:4072`.
- `scripts/tests/Shard-Console.Tests.ps1`: two new facts (`:5089`, `:5115`); seven P101 facts updated for the eighth
  site and two more deploys; `fixtures/websites-2026-10-14.json` re-copied from the real file (a fact checks they are
  equal).
- `CHANGELOG.md` 2026.10.14.15 `### Staff`, `VERSION` 2026.10.14.15.

## Proof (scratch, this PC, nothing to Haven or the site)

A scratch folder held a stand-in for Haven's root and a copy of the print-queue folder (code and data) standing in for
the game PC folder; a scratch copy of the desktop shortcut; the stub sshd `pq-proof-stub` with its host key pinned in
a scratch `known_hosts`. The game PC stand-in ran the new `queue_server.py` on port 18788 with an ssh config whose only
host is `127.0.0.1:9`, so it could not reach the site even by mistake. `Deploy-PrintQueue.ps1 -Local -Yes` with scratch
port 18787, project `pq-proof`, network `pq-proof-net`.

| Check | Result |
|---|---|
| Discover | read both sides; `game PC server: running`; `1 pinned host key(s)`; changed nothing |
| Deploy | dirs, stack, **key made** (public half printed once), `ssh_config` and `known_hosts` written, image built, game PC server stopped, **7 files copied and checked by SHA-256**, page up, **all 6 orders** served, PC `data` renamed `data.moved-20261014`, shortcut repointed. Exit 0 |
| Page loads | `GET /` 200, 47,789 bytes |
| Push before the key is authorized | fails loudly: `ssh: u@pq-proof-stub: Permission denied (publickey,...)`, in the API and `push.log`. It got past the host key check, so the pin works |
| Push after authorizing (as Chase will in Hostinger) | `OK updated`; `lastOk` set and saved to `push-state.json` |
| The right snippet | the stub's copy is **byte-identical** to `build_snippet(load())` run on the same data (9,661 chars), starts with the marker, says `on haven`, 6 public orders; `push.php` identical too |
| Edits save | `PUT /api/state` with one added field; `GET` returns it; order count unchanged |
| Backups roll | with today's backup removed, the edit wrote `backup-2026-10-14.json`, the same JSON as the pre-edit file |
| Auto-push | fired 60 s after the edit (log 16:26:30, then 16:28:03, `OK updated`) |
| Missing key | the image with an empty `keys`: start prints `WARNING: no SSH key at /home/pq/.ssh/sunflower-live ...`, `/api/push` is `ok: false` at once, a push logs `PUSH FAILED no SSH key ...` |
| The red line on the page | after a failed push, read in a browser (only the status line, not the page, which lists orders): `Lead-time page not updated since 10/14/2026, 4:28:03 PM. Last push failed (...)`, color `rgb(239,122,102)`, the page's `--danger` |
| Rollback | 8 files back from "Haven", checked by SHA-256, 6 orders, **the edit made on Haven is there**; container stopped; Haven's data set aside as `data.before-rollback-...`; game PC server answers again; shortcut back on the `.cmd`. Exit 0 |
| Dry run | `-Mode Deploy -DryRun` printed the plan and `DRY RUN: stopping here`; every file in both scratch trees hashed the same before and after |
| No pinned host key | refused: `this PC has no trusted host key for sunflower-live ...`, exit 1 |

Afterwards: the proof containers, network, both images and the whole scratch folder (with its copy of the data) were
removed. Nothing listens on 18787-18789. The real `data\` is as it was (same files, 07:07 times), the real shortcut
was never changed, and the real queue was never started.

**Not proved here:** the real Haven run (ssh, scp, `ss -ltn`, its uid, the bind on `192.168.1.61`), and a push to the
real site with the new key. The first is Chase's click; the second needs the key in Hostinger.

**Seen in the proof, worth knowing:** Windows wrote `queue.json` with CRLF line ends and the container reads and
writes LF, so the first backup on Haven differs from the moved file byte for byte but is the same JSON (checked).
`Exited (143)` on stop is python taking SIGTERM, as on any stop.

## Mistakes of mine the proof caught

1. **PowerShell variable names ignore case.** `$root` (the bash-style path) and the `-Root` parameter were one
   variable, so in `-Local` the Windows path was overwritten, and the copies and compose root would have pointed at a
   path Docker Desktop and `Copy-Item` cannot use. Found in the first Discover's output; the Windows path is now
   `$winRoot`. It only touched `-Local`; Haven's path is `$HavenRoot`.
2. Git Bash rewrote a container path (`/etc/ssh/...`) in a `docker exec` while setting up the stub; the proof uses
   `MSYS_NO_PATHCONV=1`. Proof harness only.

## Tests

`scripts\tests\Shard-Console.Tests.ps1`: before (P108's result) 302 facts, 301 passed; after **304 facts, 303 passed, 1 failed**.
The one failure in both is P107's scheduled-task fact, which fails because the `SL game PC snapshot` task is now
installed on this PC (P108 notes).

- **New:** `P109_ThePrintQueueDeploysAreAllowlistedAndRunOnlyTheirLaunchers` (the site row; both deploys point at
  `D:\UO\haven-migration\Deploy-PrintQueue*.ps1`; each launcher runs only its mode; both plans are confirm, window, log
  with `deploy to haven` and pass the safety check; tooltips; the helper's `-DryRun` runs nothing) and
  `P109_TheDeployScriptRefusesSystemPinsTheHostKeyAndNeverCopiesChasesKey` (SYSTEM refused, dry run, Discover default
  and typed words, `StrictHostKeyChecking yes` and `ssh-keygen -F`, no `accept-new` and no `id_*` key named, the key
  made on Haven, and the Sunflower repo ignoring `data/`, `data.moved-*/`, `logs/`, `keys/`).
- **Updated, each seen failing on the new config first** (5 red before the edit): `P101_TheRealConfigReads...` (eight
  sites, seven deploys), `P101_AConfigMissingAField...`, `P101_TheTileCountsTheSites...` (8 OF 8), 
  `P101_DeployIsRefused...` (the allowlist text), `P101_TheTileAndTheTabAreBuiltAndDrawn` (two more buttons, 7 OF 8).
- **New facts seen failing:** with the real launcher changed to `-Mode Rollback` and the deploy script's
  `StrictHostKeyChecking yes` changed to `accept-new`, both P109 facts failed (`runs only its mode`; `never accepted
  blindly`); restored, `cmp` identical, both passed.

## Deviations and decisions for Chase

1. **Own repo, not `sunflower-devstack`** (reasons above). If you would rather have it in devstack, move the folder
   in and commit there; nothing in it depends on where it lives except the launchers' path.
2. **The data move is part of the Deploy, not a separate button.** It happens once (Haven has no `queue.json`, this PC
   does) and is in the plan the window prints before the typed word. A second Deploy never moves or overwrites.
3. **Rollback takes Haven's data, not the moved copy.** The prompt said rollback "restarts it on the game PC from the
   moved data"; that would lose every edit made on Haven. It brings Haven's current data back and uses the moved copy
   only if Haven cannot be read, after asking.
4. **A "Print queue" row on the Websites tab** reads down (amber `7 OF 8 UP`) until the first deploy, because it checks
   the Haven URL. That is true, so it is left that way.
5. **Outside access (decide, not built):** default LAN only, as built. Putting it behind the same Cloudflare Access as
   the ops pages (when P89's H4 lands) would let you or Stephanie update the queue away from home; it holds customer
   names and order details, so it should never be reachable without Access. Your call.

## For Chase

1. **Commit the Sunflower repo** (the queue does not; it has no remote, so nothing leaves this PC):
   ```
   cd C:\dev\sunflower\print-queue; git add -A; git status; git commit -m "Print queue: container for Haven, own SSH key, deploy and rollback (cc-P109)"
   ```
   `git status` before the commit should list only the ten files above; `data\`, `logs\` and the old page copies stay
   out.
2. **Deploy:** Shard Console > Websites > **Print queue: deploy**, type `deploy to haven`, read the plan in the window,
   type `deploy`. Close the print queue window on this PC first if it is open (the deploy stops it anyway).
3. **Add the key in Hostinger:** the window prints one `ssh-ed25519 ...` line. hPanel > Advanced > SSH Access > SSH
   keys > Add SSH key, name it "print queue on Haven". Until then the page shows the red line and the lead-time page is
   not updated. Then press the page's push button once to see `Website updated`.
4. **No NPM host to add.** LAN only: `http://192.168.1.61:8787/`. The desktop shortcut opens it after the deploy.
5. Back to this PC at any time: **Print queue: roll back** (types `roll back`).

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: 6 files pending (`CHANGELOG.md`, `VERSION`, `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`,
`scripts/tests/fixtures/websites-2026-10-14.json`, `scripts/websites.json`). docs: this note. No file over 5 MB (the
largest pending is the console, about 500 KB). Customer data is in neither repo: the print queue's data never left
`C:\dev\sunflower\print-queue\data` except as a scratch copy for the proof, deleted afterwards.

P109 DONE
