# cc-P88: One shared menu across Play tests, Shard status and the Homepage dashboard

Prompt: `D:\UO\cc-prompts\cc-P88-shared-menu.md`. Builder (web pages and Homepage config; no shard build). Not
committed (autopilot commits after DONE).

**Start state.** The code repo was clean. The docs repo had `testing\SUMMARY.md` and `testing\play-tests.json`
modified, and neither was mine. The whole diff was one `generatedAt`/`updatedAt` timestamp and one `sourceHash`,
rewritten by the play-test importer at 14:23Z, a minute after the P87 commit. That is machine output, not Chase's
work, so I carried on. Those two files go into the next commit.

## Headlines

- **One menu bar on all three pages: Play tests, Shard status, Dashboard.**
  - The labels and order are the same everywhere, the bar sits at the very top, and the current page is marked
    (gold, `aria-current="page"`).
  - Links are built from the host the browser used, never `localhost`.
  - Every link is 44 px tall. The bar wraps to a second line on a phone (checked at 375 px).
  - Contrast: links 14.05:1, hover 10.36:1, current page 7.15:1. The bar has its own dark colors, the same in light
    and dark mode.
- **One source:** `D:\ShatteredLegacy\docker\test-queue\html\nav.js` holds the page table, the CSS and the code.
  - A fourth page is one more row in `PAGES`.
  - Moving a page (to Haven, say) is that page's row: set `host`, and `port` and `path` if they change.
- **How each page gets it:**
  - **Play tests** loads `/nav.js`, which `sl-play-tests` now serves.
  - **Shard status** (`dashboard.html`) carries a copy that `render_dashboard.py` inlines from `nav.js` on every
    run, so it also works opened as `file:///`. There the links use **192.168.1.58**, `nav.js`'s `FALLBACK_HOST`.
  - **Homepage** loads `nav.js` from `:8093` through its supported `custom.js`.
- **`progress.py` keeps the menu.** I ran it repeatedly. The menu block was byte-identical between runs, and equal
  line for line to `nav.js`.
- **Nothing was restarted.** Both new pieces were tested on scratch containers on 18093 and 13000, against copies
  of the data, and the scratch containers were removed afterwards.
- **What the live pages show right now:**
  - **Shard status at `:8093/status`:** already has the menu, because the page is read from disk per request.
  - **Play-test page:** says "Menu not loaded: restart sl-play-tests", with a link to Shard status. It is read from
    disk too, but the running `server.py` predates `/nav.js`.
  - **Homepage:** unchanged, with no menu, until `sl-play-tests` is restarted. Then it gets the menu on the next
    reload.
  - All three are verified with headless Edge on the LAN address.

## The menu file, and how each page loads it

`nav.js` (plain script, no build step, ASCII). The `PAGES` table:

| key | label | host | port | path |
|---|---|---|---|---|
| playtests | Play tests | null | 8093 | `/` |
| status | Shard status | null | 8093 | `/status` |
| dashboard | Dashboard | null | 3000 | `/` |

- `host: null` means the host the browser used. With no host at all (`file:///`) it is `FALLBACK_HOST`,
  `192.168.1.58`.
- The current page comes from the script tag's `data-sl-page`, or else from matching the page's port and path.
- The script injects one `<style id="sl-menu-style">` and puts `<nav id="sl-menu">` first in `<body>`, edge to edge
  whatever margin the body has.
- It also exposes `window.SLMenu` (the pages, the URL builder and the current page) for later use.

| Page | How it loads the menu | File changed |
|---|---|---|
| Play tests (`:8093/`) | `<script src="/nav.js" data-sl-page="playtests">` first in `<body>`. Its old "Status" and "Dashboard" links and their script are gone. "Add an item" and the filters stay, because they are page-specific. If `/nav.js` fails to load, one line says to restart `sl-play-tests` and links Shard status. | `docker\test-queue\html\index.html` |
| (the service) | `GET /nav.js` serves `html/nav.js`, `text/javascript`, `no-store`, read fresh per request like the page. | `docker\test-queue\server.py`, `README.md` |
| Shard status (`:8093/status`, or the file) | A `<!-- DATA:NAV -->` block before `<div class="wrap">`. `render_dashboard.py` `nav_html()` reads `nav.js` (`SL_SHARD` root) and writes it inline as `<script data-sl-page="status">`. If `nav.js` cannot be read, or contains `</script`, the block is left as it was, never emptied. The header's old two-link nav and its `.links` CSS are removed. | `dashboard.html`, `tools\render_dashboard.py` |
| Dashboard (Homepage, `:3000/`) | `custom.js` adds `<script src="http://<host>:8093/nav.js" data-sl-page="dashboard" async>`. If it fails to load, Homepage shows as before. | `docker\dashboard\config\custom.js` |

Also changed:
- **`dashboard.html` got `<meta charset="utf-8">` and `<meta name="viewport" ...>`.** Without the viewport, a phone
  laid it out 980 px wide (`innerWidth` 981 under 375 px emulation), so the menu and the page were tiny.
- **`.gitignore`: `docker/dashboard/config/custom.js` is now tracked.** It had been ignored since 2026-09-22 as an
  empty home-lab default (commit 9a78266). It now carries the shard's menu, so it belongs in the repo.
  `custom.css` stays ignored (unused).
  - Proved: `git check-ignore -v docker/dashboard/config/custom.js` exits 1.

## Homepage: method and sources

- **Installed version: 1.13.1.** Read from `/app/package.json` in `sl-dashboard` (`ghcr.io/gethomepage/homepage:latest`).
- **Custom JS is supported in that version.** Read from its compiled route, `/app/.next/server/pages/api/config/[path].js`:
  - it accepts only `custom.css` and `custom.js`, and anything else gets "Unsupported file";
  - it reads the file from `/app/config` with `readFileSync` **on every request** and serves it as `text/javascript`;
  - the index page includes `<script src="/api/config/custom.js">`.
  - Homepage's docs describe the same feature: https://gethomepage.dev/configs/custom-css-js/ (not re-read online
    in this task; the installed code above is the evidence).
- **Rereads:** because the route reads the file per request, **a browser reload picks up a change to `custom.js`, with
  no restart**. `sl-dashboard` bind-mounts `D:\ShatteredLegacy\docker\dashboard\config` to `/app/config`, so the
  repo file is the live file.
- **No CSP:** Homepage sends no Content-Security-Policy header (checked with `curl -D -`), so a script from `:8093`
  is allowed.
- **The fallback group was not needed.** The existing "Play tests" and "Shard status" entries in `services.yaml` were
  not touched.

## The other "Migration status"

Homepage has two entries pointing at `https://shatteredlegacyuo.com/migration.html`: "Migration status" and "Art and
script downloads".
- **That page is the public website's progress page** (`docker\website\html\migration.html`, title "Shattered
  Legacy: progress").
  - It is served to the internet through the website and reads `/api/migration.json`, `/api/shards.json` and
    `/api/downloads.json` from `sl-uo-status` (port 8092).
  - `migration.json` comes from `scripts\Build-MigrationStatus.ps1`, built from the bug list: open and fixed
    defects, and ported files in reach.
- **Shard status is a different page.** It is the internal LAN-only dashboard (`dashboard.html`), rebuilt by
  `progress.py` on every commit: gates, tasks, queue, play tests, counts.
- **The public page's data is stale.** `http://192.168.1.58:8092/migration.json` says `"generatedAt":
  "2026-09-29T18:16:30Z"`, two weeks old.
- **Unverified:** the public URL did not answer from this PC (curl: no connection, code 000). I could not see the
  live public page.

## Proof

- **The same bar on all three pages, current page marked, links from the LAN address.** Scratch copies on
  `192.168.1.58:18093` (play tests and `/status`) and `192.168.1.58:13000` (Homepage):
  - Play tests: links `http://192.168.1.58:8093/`, `http://192.168.1.58:8093/status`, `http://192.168.1.58:3000/`;
    "Play tests" current; the bar is the first child of `<body>`.
  - Shard status: the same three links; "Shard status" current; `min-height` 44 px.
  - Homepage, in headless Edge (`--dump-dom`): the same three links; "Dashboard" current.
  - `dashboard.html` as `file:///D:/UO/shard-migration/dashboard.html`: the same three links on 192.168.1.58;
    "Shard status" current.
  - Phone, 375 x 812 (the built-in browser's mobile emulation): the bar wraps to two lines and spans 0 to 375 px
    with no overflow. Each link is 44 px tall.
- **Screenshots** at 1280 px in `D:\ShatteredLegacy\scripts\shard-console-cache\screenshots\p88\`: `menu-playtests.png`,
  `menu-status.png` and `menu-dashboard.png`. That folder is git-ignored, because the Homepage shot shows home-lab
  services and the play-test page is internal (P83 keeps it LAN only), and both repos are public.
- **The live pages now, headless Edge on `192.168.1.58`:**
  - `:8093/status` has the menu;
  - `:8093/` shows "Menu not loaded: restart sl-play-tests with Start-TestQueue.ps1." with a Shard status link;
  - `:3000/` renders as before, with no `sl-menu`.
- **`progress.py` keeps the menu.** It reported `dashboard.html updated (REVIEWED, VERSION, NAV, ...)` on each run.
  The NAV block was `cmp`-identical between two runs, and the inline script `diff`-identical to `nav.js`.
- **Not testable in the built-in browser:** a page there could not fetch a second origin (even `fetch` with
  `no-cors` failed, and Homepage sends no CSP). So the Homepage check was done in headless Edge.

## Deviations and decisions for Chase

1. **Keep, rename or drop Homepage's "Migration status"?** It is the public website's progress page, not this
   menu's Shard status, and its data stopped updating on 2026-09-29.
   - I propose renaming it to **"Public progress page"**, so the two names do not collide.
   - Separately, decide whether `Build-MigrationStatus.ps1` should run again or the page should come down.
   - Not removed, as asked. "Art and script downloads" also links to that page; that looks like a copy-paste and
     may want its own link.
2. **Homepage still lists "Play tests" and "Shard status" as service tiles.** They carry the count widgets, so I left
   them. Drop the tiles now that the bar exists?
3. **The Shard Console's tile buttons say "Play tests", "Dashboard", "Status".** Rename "Status" to "Shard status"
   to match? Not changed here, because the console is not one of the three pages.
4. **Two places to edit when the play-test service moves.** `nav.js` holds every page's address, but Homepage's
   `custom.js` must know where `nav.js` itself lives (its `NAV_AT`, one line). There is no way around that short of
   inlining the file into Homepage's config.
5. **The bar uses its own colors** (dark slate with gold), not each page's palette, so it is identical everywhere
   and readable on both light and dark pages.
6. **I added a viewport meta to `dashboard.html`.** It was not asked for, but without it the menu was not tappable
   on a phone.

## For Chase

1. **Restart the play-test service** so it serves `/nav.js`. That is the one deploy step:

   ```
   cd D:\ShatteredLegacy\docker\test-queue; .\Start-TestQueue.ps1
   ```

   It recreates only `sl-play-tests`.
2. **Then reload Homepage** (`http://192.168.1.58:3000/`). `custom.js` is read on every request, so no Homepage
   restart is needed.
3. **Check:** the bar on all three pages, from your phone too, with the page you are on in gold.
4. Until step 1, the play-test page shows a one-line "Menu not loaded" notice with a link to Shard status, and
   Homepage has no bar.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run after this notes
file was written:

```
=== code  (D:\ShatteredLegacy) ===
  pending: .gitignore, CHANGELOG.md, VERSION, docker/test-queue/README.md, docker/test-queue/html/index.html,
  docker/test-queue/server.py, docker/dashboard/config/custom.js, docker/test-queue/html/nav.js
  dry run: would add, commit and push
=== docs  (D:\UO\shard-migration) ===
  7 file(s) pending: README.md, dashboard.html, testing/SUMMARY.md, testing/play-tests.json, tools/progress.json,
  tools/render_dashboard.py, notes/cc-P88-shared-menu.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

Patch notes: `CHANGELOG.md` 2026.10.13.10 `### Staff` line (2026.10.13.9 was already committed by P87), `VERSION`
2026.10.13.10. Wiki page not published.

P88 DONE
