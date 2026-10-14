# cc-P107: Haven H2 + H3: the ops pages (Play tests, Ideas, Bugs, Shard status) onto Haven, LAN cutover

2026-10-14. Builder, game PC and Haven files. Prompt: `D:\UO\cc-prompts\cc-P107-haven-ops-move.md`. P89 Part C items 2
and 3, after P105 (H1, DONE). Not committed (autopilot commits after DONE). Both repos were clean at the start.
**CC never connected to Haven**: no ssh, scp or docker context to 192.168.1.61, read or write. Everything for Haven is
files in the repo plus three named deploys Chase runs from the Shard Console's Websites tab.

## Headlines

- **Three buttons on the Websites tab** (after the phrase `deploy to haven`, through P101's helper and allowlist):
  **Ops pages: deploy**, **Ops pages: cut over**, **Ops pages: roll back**.
  - Each is `docker\ops\Deploy-HavenOps.ps1` behind a one-line launcher in `D:\UO\haven-migration` (the only folder the
    helper runs scripts from).
  - Each **starts with a read-only discovery of Haven**, prints its plan, and changes nothing until its word is typed
    in its window (`deploy`, `cut over`, `roll back`). So a click is a dry run until then; `-DryRun` stops after the plan.
  - All three refuse to run as SYSTEM.
- **The Haven stack, `docker\ops\docker-compose.yml`** (compose project `sl-ops`, under `~/sl-ops`, no sudo):
  - `sl-ops-git-pull` keeps read-only clones of both repos current every 2 minutes, with "repo as of" stamps;
  - `sl-play-tests` is the same `server.py` in Haven mode (P105), writing only `~/sl-ops/data`;
  - the page is on `192.168.1.61:8093` and the token listener (export, ingest, game PC snapshot) on `192.168.1.61:8094`,
    LAN only.
- **Found: `shard-migration` is private.** An anonymous `git ls-remote` is refused, while the infrastructure repo
  answers; P89 assumed both were public.
  - So the first Ops pages deploy makes a **read-only deploy key on Haven** and prints its public half for Chase to add
    on GitHub (once).
  - The infrastructure repo is cloned anonymously.
- **The token** for export and ingest is asked once (Enter makes a random one), written to Haven's `~/sl-ops/ops.env`
  (chmod 600) and `D:\UO\haven-ops\token.txt`. It is never printed, never on a command line, never in git.
- **Game PC side (H2):**
  - `scripts\Publish-GamePcSnapshot.ps1`, every minute once its task is installed. It sends the Golem, the queue and
    the containers, and nothing before the cutover.
  - `Commit-ShardWork.ps1` now takes Haven's export into `testing\` before `progress.py`, never blocking
    (`shard-migration\tools\opsmirror.py`).
  - The console's Play tests and Shard status links, the Websites lights and the PLAY TESTS tile follow
    `D:\UO\haven-ops\state.json` (Haven after the cutover, else this PC). The tile falls back to the mirror with
    "(Haven unreachable)".
  - The menu follows whichever host served it, and Homepage loads it from Haven first, then this PC.
- **Proof on this PC, without Haven:** the real compose file and the real `Deploy-HavenOps.ps1` in `-Local` mode
  (scratch folder, loopback ports, a stand-in for the game PC's page; the real `sl-play-tests` never stopped). **Two
  full cycles of deploy, cutover and rollback**, each verified:
  - export and ingest round-trip;
  - "game PC offline since";
  - a mark made on Haven coming back through the mirror refresh and the rollback;
  - Haven unreachable leaving the mirror as it was;
  - a second cutover refusing to overwrite Haven's data.
- **Tests:** 8 new console facts (8 of 8 red before) and 4 new Python facts (4 of 4 red against a stub). Final:
  **console 289 of 289, Python tools 71 of 71.**
- **Nothing was deployed and nothing moved:** this PC is still `mode: local` (there is no state file), and the game PC's
  page is serving as before.

## What changed

### `D:\ShatteredLegacy`

| File | What |
|---|---|
| `docker/ops/docker-compose.yml` (new) | The Haven stack. Everything is overridable by env (`OPS_ROOT`, `BIND`, the ports, project and names), so the same file runs the proof. `init: true` on the page so a stop is clean |
| `docker/ops/git-pull.sh` (new) | Clone once, then every `PULL_SECONDS` fetch `main`, reset hard, write `stamp-<repo>.txt` as `<commit> <commit time>`. A failed fetch keeps the clone |
| `docker/ops/Deploy-HavenOps.ps1` (new) | Discover :153, Deploy :172, Cutover :229, Rollback :285. Haven is reached by `Invoke-Haven`: one command over ssh as Chase, sent base64-encoded, because PowerShell 5.1 mangles quotes in native arguments; the token goes only on stdin |
| `docker/ops/README.md` (new) | The layout, the three buttons, the game PC side |
| `scripts/haven-ops.json` (new) | Haven's page, status, ops API, ssh and root; the game PC's fallback; the state and token file paths; the repo URLs. No secrets |
| `scripts/Publish-GamePcSnapshot.ps1` (new) | The snapshot, about 1 KB, `POST :8094/api/ingest/gamepc` with the bearer token. Sends nothing before the cutover unless `-Force`; `-DryRun` prints the JSON |
| `scripts/Install-GamePcSnapshotTask.ps1` (new), `scripts/Run-Hidden.vbs` (new) | The every-minute task "SL game PC snapshot" (as Chase, only while logged on, no window); `-DryRun`, `-Uninstall` |
| `scripts/Shard-Console.ps1:362-366, 370-416` | Config `Ops`; `ConvertFrom-OpsConfig`, `Get-OpsMode`, `Get-OpsLinks`, `Set-OpsSites` (in Haven mode a site with `havenUrl` is Haven's) |
| `scripts/Shard-Console.ps1:3829-3831` | Links: Haven after the cutover, this PC before; the text names the rollback |
| `scripts/Shard-Console.ps1:4872-4910` | PLAY TESTS: Haven's `/api/items`, `/api/ideas` and `/api/bugs`, plus the snapshot's age ("on Haven, game PC snapshot received 40 s ago"); else the mirror, "from the last commit (Haven unreachable)" |
| `scripts/Shard-Console.ps1:1065-1067, 1283-1285, 3998-4005` | The three Websites buttons, their tooltips, and their plan (phrase, the helper in a window, log), under the same safety rule as Deploy to Haven |
| `scripts/Shard-Console.ps1:3899` | Sites read an optional `havenUrl` |
| `scripts/websites.json` | The three deploys; `havenUrl` on Play tests and Shard status; the P89 slot now says it is filled (7 lines; the fixture is the same file) |
| `docker/test-queue/html/nav.js:24, 50-56, 66-71` | Dashboard pinned to the game PC until H5; host null means the host that served `nav.js`; the loopback name is no longer spelled out (the status page inlines this file and must not contain it) |
| `docker/dashboard/config/custom.js` | Loads the menu from Haven's :8093, else this PC's |
| `scripts/tests/Shard-Console.Tests.ps1` | 8 `P107_*` facts; the P101 facts' deploy list, buttons and fixture |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.13, one `### Staff` line |

### `D:\UO\shard-migration`

| File | What |
|---|---|
| `tools/opsmirror.py` (new) | `refresh`: mode local, skipped; mode haven, fetch `/api/export` and `opsdata.write_bundle` into `testing/`, naming what changed; unreachable, no token or a bad bundle each leave the mirror as it was. Always exit 0 |
| `tools/tests/test_opsmirror.py` (new) | 4 facts |
| `tools/tests/test_haven_h1.py`, `tools/tests/test_status_dashboard.py` | The Dashboard row's new host |
| `README.md`, `dashboard.html`, `tools/progress.json` | Regenerated by `progress.py` (the inlined menu); the commit does this anyway |

### Outside both repos (not versioned)

- `D:\UO\Commit-ShardWork.ps1:97-104`: the mirror refresh before `progress.py`, dry runs included. Backup:
  `Commit-ShardWork.ps1.bak-20261014-p107`.
- `D:\UO\haven-migration\Deploy-HavenOps-Pages.ps1`, `-Cutover.ps1`, `-Rollback.ps1`: the launchers, each one line.

## Tests

**Console** (`scripts\tests\Shard-Console.Tests.ps1`), the 8 `P107_*` facts:

- the real `haven-ops.json` (with no secret in it), and with no file, the game PC only;
- the mode is haven only when the state file says exactly `haven`;
- links and sites point at Haven after the cutover and at this PC before; Homepage does not move;
- the tile falls back to the mirror when Haven does not answer, and is as before with no cutover;
- the three deploys are in the allowlist, run only their launchers, and are each confirm, window, log under the safety
  check; the helper's `-DryRun` names the cutover launcher;
- the Haven scripts refuse SYSTEM, have `-DryRun`, take the token by `Read-Host -AsSecureString` and stdin only, and
  never print it; the compose file publishes on the LAN address only, mounts the clones read only, and holds no token;
- the snapshot sends nothing before the cutover; `-DryRun` prints JSON with the Golem and the containers; the
  installer's `-DryRun` registers nothing;
- the menu follows the host that served it, and Homepage tries Haven first.

Fail first: with every P107 change in the shard repo stashed (new files too) and the launchers moved away, **8 facts,
0 passed, 8 failed**. Restored, 5 passed and 3 failed, for my own mistakes:

- `Get-OpsMode` took a `[string]` parameter, which turns `$null` into `''`, so it never read the state file. It now
  asks whether the parameter was given.
- The facts' helper had to re-apply the site swap after writing its state file.
- A one-line `Where-Object` result indexed with `[0]` gave its first character.

Then 8 of 8. The full suite then needed the P101 facts to know the three new deploys and buttons (expected, since they
pin the file). **Final: 289 facts, 289 passed, 0 failed.**

**Python** (`python -m unittest discover -s tools/tests`): 4 new facts on the mirror (before the cutover nothing is
fetched; after it the export becomes the mirror and the changes are named; unreachable, no token, a tampered bundle
leave it untouched; exit 0 always). **Red against a stub: 4 of 4 failed. Green: 4 of 4.** The full run then failed 2
existing facts: the status page contained "localhost" (P105's `onLan` spelled it, and the page inlines `nav.js`) and the
pinned Dashboard row. Fixed in `nav.js` and the two tests. **Final: 71 of 71.**

### The proof (this PC, Haven mode, no Haven)

`D:\UO\ops-proof\`: the stack's folder (`haven\`), a copy of `testing\` as the mirror, a scratch state and token, an
override that clones the two repos from this PC instead of GitHub, and a stand-in container (`sl-ops-proof-gamepc`)
playing the game PC's page. Loopback ports 18093 and 18094. All through `Deploy-HavenOps.ps1 -Local` and the real
`docker\ops\docker-compose.yml`.

| Step | Seen |
|---|---|
| Deploy | Discovery (Docker 29.5.2, Compose 5.1.3, both ports free, nothing there yet), token written (not shown), git-pull up, both clones with stamps (`b8887652...` and `cacd8cf5...`). A second Deploy kept the token and changed nothing |
| Cutover | Stand-in stopped; 3 files seeded; page up; **"Haven's export matches all 3 seeded files"**; mode haven; the closing list of what to check |
| Pages | `/`, `/status`, `/nav.js`, `/api/ideas`, `/api/bugs` all 200; `/api/items` 216 items, `repo: b8887652d889 ... source stamp` |
| Snapshot | `Publish-GamePcSnapshot.ps1 -Force`: "sent 952 bytes"; `/api/gamepc` age 0, not offline, Golem on, 6 containers |
| Token | `/api/export` with no token: 401 |
| Offline | The stored snapshot set 10 minutes back: `offline: true, offlineSince: ...` in `/api/items` |
| Mirror | M-001 marked on the scratch Haven page, then `opsmirror.py`: **"refreshed from Haven: 3 files, 2 changed: testing/SUMMARY.md, testing/play-tests.json"**; the item is in the mirror |
| Unreachable | `opsmirror.py` against a closed port: "NOT refreshed (Haven unreachable ...); the previous mirror stays", exit 0 |
| Commit dry run | `Commit-ShardWork.ps1 -DryRun` (real, this PC is mode local): "play-test mirror: not cut over to Haven (mode local); the game PC's service writes testing/" |
| Rollback | Export taken (0 changed, the refresh already had it); page stopped; stand-in started; mode local |
| Second cutover | **REFUSED: Haven already has play-test data; a cutover never overwrites it.** That showed a gap: after a rollback a later cutover is legitimate. So the rollback now sets Haven's copy aside (`data/testing.before-rollback-<time>`, kept) |
| Second cycle | Deploy, Cutover ("matches all 3"), M-002 marked, Rollback: "3 files, 2 changed", "Haven data set aside", M-002 in the mirror. Page stop exit 143 (signal) after `init: true`, where the first was 137 (killed) |

Fixed during the proof, each a real bug the click would have hit on Haven:

- **Quotes:** `Invoke-Haven` passed the command as a native argument, and PowerShell 5.1 broke its double quotes (the
  discovery failed). Commands now travel base64-encoded.
- **Stderr:** Compose's progress on stderr ended the script under `$ErrorActionPreference = 'Stop'`. Inside
  `Invoke-Haven` it is now `Continue`, and the exit code decides.
- **The mode clash:** `$mode` (the state file) overwrote the `-Mode` parameter (variable names ignore case). It is now
  `$opsMode`.
- **The token file's CR:** the token now goes through `tr -d '\r'` on the way into `ops.env`.

The proof containers and network were removed afterwards (`docker compose -p sl-ops-proof down`, `docker rm -f
sl-ops-proof-gamepc`). The real `sl-play-tests` was up the whole time. **Not done:** anything on Haven.

## Deviations and decisions for Chase

1. **The stack lives in `/home/chase/sl-ops`**, not P89's `/srv/sl-ops`, so nothing needs sudo. It is separate from
   `~/shattered-legacy`.
2. **The page is on `192.168.1.61:8093`**, the same port it had on the game PC, writable on the LAN as it is today.
   P89's read-only LAN page comes with Cloudflare Access in H4.
3. **The service code comes from the git-pull clone** of the infrastructure repo, not from files the deploy copies. The
   page and menu update within 2 minutes of a push; a new `server.py` takes effect at the next Ops pages deploy (which
   recreates the page after the cutover).
4. **A deploy key for the private repo** (above). Alternatively, make `shard-migration` public, or use a fine-grained
   read-only token instead; the key is the narrowest.
5. **The rollback sets Haven's data aside rather than leaving it**, so a later cutover seeds fresh from `testing\` and
   still never overwrites.
6. **Homepage stays on the game PC** (H5): the menu's Dashboard link points at `192.168.1.58:3000` wherever the menu is
   shown, since Haven's own :3000 is the stale June Homepage.
7. **Bug reports made on Haven say version (unknown)** until the snapshot carries the test shard's `shard-commit.json`
   (an H5 follow-up).
8. **`Commit-ShardWork.ps1` is outside git** (`D:\UO`). The logic is in the versioned `opsmirror.py`; the script gained
   only the call, with a backup beside it.
9. **The Golem's own commits:** after the cutover every commit carries the mirror refresh. If Haven is down at commit
   time, the commit goes on with the previous mirror and says so.

## For Chase

**Nothing to add in NPM** for this step: the pages are LAN only. Outside access (`ops.shatteredlegacyuo.com`) is H4.

In order, when you want to move:

1. **Ops pages: deploy** (Websites tab, phrase `deploy to haven`, then type `deploy` in its window).
   - Read the discovery first: both ports must say free.
   - If Haven runs a firewall, allow 8093 and 8094 from your LAN.
   - Press Enter at the token prompt to make one.
   - It prints the deploy key's public half. On GitHub: `shard-migration` > Settings > Deploy keys > Add deploy key,
     title `sl-ops on Haven`, **Allow write access off**. Then click Ops pages: deploy again; it should end "Deploy done"
     with two clone lines.
2. **Install the snapshot task once:**

   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\Install-GamePcSnapshotTask.ps1
   ```

   It sends nothing until the cutover.
3. **Ops pages: cut over** (type `cut over`). What you should see after it:
   - `http://192.168.1.61:8093/` is Play tests with the same items, ideas and bug reports; `/status` is Shard status.
   - The window ends "Haven's export matches all N seeded files" and "mode is now haven".
   - `http://192.168.1.58:8093/` no longer answers (the game PC's page is stopped, not removed).
   - Reopen the Shard Console: the PLAY TESTS tile ends "on Haven, game PC snapshot received ... ago", Play tests and
     Shard status open Haven, and the Websites lights for both check Haven.
   - Homepage's menu still appears, now loaded from Haven.
   - The next commit prints "play-test mirror refreshed from Haven: ...".
   - Pull the game PC's network or let it sleep: within 3 minutes Haven's footer says "Game PC offline since ...".
4. **To undo: Ops pages: roll back** (type `roll back`). The game PC serves again with everything marked on Haven.

The scratch folder `D:\UO\ops-proof\` (233 MB, mostly the two clones) can be deleted.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

P107 DONE
