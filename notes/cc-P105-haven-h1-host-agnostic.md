# cc-P105: Haven H1: the play-test service made host-agnostic, still running on the game PC

2026-10-14. Builder of `sl-play-tests`. Prompt: `D:\UO\cc-prompts\cc-P105-haven-h1-host-agnostic.md`. Step H1 of cc-P89's
plan (`notes\cc-P89-haven-pages-plan.md`, Part C item 1), with Chase's 10-14 decisions. Nothing deployed to Haven,
nothing changed on the running game PC service. Not committed (autopilot commits after DONE). Both repos were clean at
the start.

## Headlines

- **With the defaults the game PC page behaves exactly as today.** Checked side by side: the previous `server.py` (git
  HEAD) and the new one ran on identical copies of the real notes, docs and testing data, and got the same requests.
  - **All 19 routes answered the same** status and content type.
  - **The same five files were written**: play-tests.json, SUMMARY.md, feature-ideas.json, bug-reports.json and a
    screenshot.
  - The only differences are additions: an empty `by` on each item, and empty `gamepc`, `repo` and `identity` blocks
    in `/api/items`. The page shows none of them while they are empty.
- **`PLAYTESTS_DATA`** separates `testing/` (play tests, SUMMARY.md, ideas, bug reports and their screenshots) from the
  notes root. Notes and docs are still read from the root. Default: the root, as before.
- **A second, token-guarded listener** (`PLAYTESTS_LAN_PORT`, off by default, never started without a token) serves
  `GET /api/export`, `POST /api/ingest/gamepc` and `GET /api/gamepc`.
  - The export is a bundle of every file under `testing/`, with each file's SHA-256 (`tools\opsdata.py`).
  - `write_bundle` puts a bundle back, refusing a bad hash or any name outside the list. H2's commit step will use it.
- **"Game PC offline since"** appears once the stored snapshot is over 3 minutes old, and **"repo as of"** comes from
  the pull container's stamp file, else git, else nothing. Both are in `/api/items` and the page's footer.
- **`nav.js` URL mode with `lanOnly`:** a row may carry a whole `url`, and `lanOnly: true` hides it off the home
  network. Dashboard is marked `lanOnly`. Today's rows are unchanged.
- **The optional Cloudflare Access check** (off unless `ACCESS_TEAM_DOMAIN` and `ACCESS_AUD` are both set) verifies the
  Access JWT itself: RS256 signature, audience, issuer, expiry and email. It uses the standard library only, so no new
  dependency (decision 1).
- **Writer identity, `by`,** on every result, manual item, idea and bug report: the Access email when on, empty
  otherwise. The identity comes from one function with room for a second source (H6's shard login).
- **Tests:** 13 new facts, 12 of them seen failing first. The tool suite is 67 of 67, the importer's Pester tests 20
  of 20.
- **Scratch Haven-mode run on this PC:** export, ingest, token refusals, "repo as of" from git, and "Game PC offline
  since" on the page in the browser. The real `testing\` folder was byte-identical before and after.

## What changed

### `D:\ShatteredLegacy\docker\test-queue\`

| File:line | Change |
|---|---|
| `server.py:1-55` | Docstring: the new settings and routes |
| `server.py:81-97` | `--data`/`PLAYTESTS_DATA`, `--lan-bind`, `--lan-port`, `--token-file`, `--access-team`, `--access-aud`, `--access-certs` (tests only), `--repo-stamp` |
| `server.py:103-112` | `DATA` (default the root), `TOKEN` (env, else the token file), `VERIFIER` (only when both Access settings are set) |
| `server.py:124` | the importer reads notes from the root and writes under `DATA` |
| `server.py:147-161` | `repo_as_of` (cached a minute) and `service_state`: `/api/items` `service` gains `gamepc`, `repo` and `identity` |
| `server.py:198-219` | `identity()` (Access today; H6 adds its source here) and `who()`: 403 for every route but `/nav.js` when Access is on and the token is not good |
| `server.py:248`, :322-376 | every data call uses `DATA`; `by` is passed to results, manual items, ideas (add, delete) and bugs (add, delete) |
| `server.py:393-434` | `LanHandler`: bearer token (constant-time compare) on every request; export, ingest (64 KB cap), the snapshot |
| `server.py:436-452` | `main`: the token listener only when a port and a token are both set; the log says which |
| `html/nav.js:8-13,23,51-63,77-80,96` | URL mode, `onLan`, `lanOnly` (Dashboard) |
| `html/index.html:237-240,246,367,510` | the footer's "Repo as of", "Game PC offline since" and "Signed in as"; "by" on result, idea and bug chips, each only when non-empty |
| `README.md` | "Running on Haven" section |

`docker-compose.yml` is unchanged: the defaults are the old behaviour.

### `D:\UO\shard-migration\tools\`

| File:line | Change |
|---|---|
| `opsdata.py` (new) | `export_bundle` :63, `write_bundle` :90 (an allow-list of names, hash checks before any write, temp file and rename, a removed screenshot removed from the mirror), `save_gamepc` :127, `gamepc_status` :140 (offline after 180 s), `repo_as_of` :156 |
| `accessjwt.py` (new) | `verify_rs256` :42 (RSASSA-PKCS1-v1_5, SHA-256), `AccessVerifier` :63 (keys from `https://<team>/cdn-cgi/access/certs`, cached an hour, re-fetched at most once a minute for an unknown kid; aud, iss, exp, nbf with 60 s leeway, email), `token_from` :143 (header, else cookie) |
| `playtests.py:224` | items gain `by` |
| `playtests.py:492-495` | `import_all(..., data=None)` |
| `playtests.py:537,555` | `set_result(..., by="")` |
| `playtests.py:572,581` | `add_manual(..., by="")` |
| `ideas.py:42,146,154` | ideas gain `by`; `add(..., by="")`. Bugs already had `by` (cc-P97) |
| `tests/test_haven_h1.py` (new) | 13 facts |

`D:\ShatteredLegacy\CHANGELOG.md`: new section **2026.10.14.11** (10-14.10 was committed), one `### Staff` line;
`VERSION` 2026.10.14.11. Wiki not published.

## Tests

`python -m unittest discover -s tools/tests -p "test_*.py"` in shard-migration.

The 13 new facts:

- **The export bundle:** round-trip of every file the service writes, screenshots included, byte for byte; a mirror
  drops a screenshot the source removed; a tampered file, five foreign names (`../evil.txt`, `notes/...`, a `.exe`,
  path climbs) and a wrong schema are all refused, with nothing written.
- **The snapshot:** never received, then fresh, then offline since its arrival time; a non-object refused.
- **Access:**
  - A good token passes, with `aud` as a list or a string.
  - A bad signature, edited claims, wrong audience, wrong issuer, expired, not yet valid, no email, `alg none`, unknown
    kid, garbage and empty are each refused. A throwaway 1024-bit RSA key is made in the test from the standard library.
  - The token is read from the header or the cookie.
- **`by`:** recorded on manual items, results, ideas and bugs; empty without an identity.
- **The service, run for real on free local ports:**
  - Defaults: 8 GET routes are 200; three writes land under the root; export and the snapshot are not on the page port;
    no second listener.
  - Haven mode: writes land in the data folder only; the stamp gives "repo as of"; four wrong or missing tokens get 401
    on export and ingest; the export over HTTP round-trips into a mirror; ingest and the snapshot work; 413 over 64 KB.
  - A port with no token: no listener.
  - Access on, against a local key server: `/nav.js` is open; five routes and a write without a token get 403; a bad
    signature gets 403 and writes nothing; the header and the cookie each work; `by` is the email, lower-cased, on a
    manual item, a result, an idea and a bug.
- **The menu:** URL mode and `lanOnly` are there, and today's three rows are unchanged.

Fail first:

- Setup: the tracked files back at git HEAD (`git stash`), and the two new modules replaced by permissive stubs. The
  stubs were an export that carries nothing and a verifier that accepts anything.
- Result: **13 run, 8 failed, 4 errors, 1 passed.** The pass is "a good token passes", which an accept-everything stub
  also passes.
- Then the real code was restored: `git diff` of both repos byte-identical to before the stash, and the stubs gone.
  **13 of 13 passed.**

Fixed along the way:

- The first red run hung. On Windows a refused localhost connection takes about 2 s, and `start()` retried 100 times
  after the old server had already exited. `start()` now stops as soon as the process has exited.
- The first green run had one failure in my own test: "a refused write writes nothing" compared against an empty
  folder, but the importer writes `play-tests.json` at start. The test now compares before and after.

Final:

- Tool suite **67 OK** (13 new; the ideas, bug-report and dashboard facts include service runs).
- `Import-PlayTests.Tests.ps1` **20 passed, 0 failed**.

### By hand

- **Defaults, old against new:** the scratch script `compare_defaults.py` (in my scratchpad, not in a repo):

  ```
  ALL ROUTES SAME: True | SAME FILES: True
  ITEM KEYS only new: ['by'] only old: []
  SERVICE KEYS only new: ['gamepc', 'identity', 'repo']
  ```

  The first try showed three page routes as 500 and 404 on the old side. That was my harness: I had copied the old
  `server.py` without its `html\` folder. With HEAD's `index.html` and `nav.js` beside it, everything matched.
- **Haven mode on this PC:**
  - Setup: notes root the real repo, data a scratch copy of `testing\`, ports 18093 and 18094 on 127.0.0.1, a random
    token in a scratch file.
  - The token listener: no token 401, a bad token 401, export on the page port 404.
  - Ingest stored the snapshot; a manual item went to the scratch data; the export carried the files.
  - `service` read `repo: fc85416bd1ef (git)`. After backdating the snapshot 10 minutes it read `offline: true`, and
    the page footer said "Repo as of 2026-10-14 13:01 (fc85416). Game PC offline since 2026-10-14 18:13 UTC."
  - The menu still showed all three links on a LAN address. `onLan` refused `ops.shatteredlegacyuo.com` and accepted
    a 100.x Tailscale address; URL mode returned the absolute URL. No console errors, so the new `nav.js` parses.
  - The real `testing\` was SHA-256-identical before and after, and the server was stopped.

## Deviations and decisions for Chase

1. **The Access check uses the standard library, not PyJWT.** P89 said the standard library cannot verify RS256. It
   can: verifying is one modular power and a padding compare (`verify_rs256`, RFC 8017). So `python:3-alpine` needs
   no pip step. H4 can still add `cloudflared`'s own check in front, as P89 preferred.
2. **When Access is on, it guards every route but `/nav.js`, reads included**, not only writes. With Access in front
   (H4), a request without its token did not come through Cloudflare. `/nav.js` holds no data and Homepage loads it
   (P89's bypass).
3. **`by` is the last writer** of a result (set on every result change, empty on a re-open with no identity), the adder
   of an idea, manual item or bug, and the deleter in a delete record. Status changes on ideas and bugs do not record
   a `by` yet. Say if you want that.
4. **Every item gains `"by": ""`** the next time the game PC service writes play-tests.json, once it is restarted with
   this code. That is machine output in `testing\`, committed as usual.
5. **Not in H1, left for their steps:**
   - the read-only page on the LAN port (H3);
   - the Origin check and per-identity rate limits (H4);
   - the snapshot publisher and the mirror refresh in `Commit-ShardWork.ps1` (H2, which will call `opsdata.write_bundle`);
   - the git-pull container that writes `REPO_STAMP` (H3).
6. **The game PC's running `sl-play-tests` still runs the old code** until it is restarted (For Chase). Nothing about
   it changes when it is, apart from item 4.

## For Chase

- Nothing to deploy for H1. Restart the game PC service when convenient so it runs this code:

  ```
  docker restart sl-play-tests
  ```

  The page should look exactly as it does now.
- H2 is next in cc-P89's order: the game PC's snapshot publisher and the mirror refresh before each commit.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

P105 DONE
