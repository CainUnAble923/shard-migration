# cc-P101: Shard Console Websites tab, an NPM button, and one-click Haven deploys

2026-10-14. Console code and tests in `D:\ShatteredLegacy\scripts`. Nothing was deployed to Haven by this task.

## Look at this first: the public website is unreachable by its name (found, not fixed)

While wiring the status lights, `https://shatteredlegacyuo.com/` gave no answer from this PC. What I measured:
- `nslookup shatteredlegacyuo.com 1.1.1.1` answers **`192.168.1.58`**, a private LAN address (the game PC), from
  public DNS. The game PC has nothing on 443, so the name leads nowhere: from outside the house it cannot route at
  all.
- Haven serves the site correctly: `curl --resolve shatteredlegacyuo.com:443:192.168.1.61` gives **200**, and
  `http://192.168.1.61/` with that Host header redirects to https as it should.
- `wiki.shatteredlegacyuo.com` and `vault.chasekfleming.com` answer 200; only the apex name is wrong.

**My hypothesis, not verified:** the apex record is the one `sl-ddns` publishes, and it published the LAN address
instead of the house's public one (the PUBLIC DNS tile's territory, bug-list D47). The tile now shows this honestly:
`WEBSITES: 6 OF 7 UP, down: Public website (no answer: ConnectFailure)`. I changed nothing in DNS, sl-ddns or
Cloudflare. **For Chase: check the apex A record in Cloudflare and `docker logs sl-ddns`.**

## Headlines

- **Websites tab.** One line per site from `scripts\websites.json`, each with a status light, and a site picker with
  buttons:
  - **Open**: the browser.
  - **Restart, Redeploy (the site's own start script), Logs (last 200)**: for the game-PC sites (Play tests, Shard
    status, Homepage). Each runs in a window of its own.
  - **Deploy to Haven**: for the website and the wiki macros, after the phrase `deploy to haven`.
  - **Open NPM**.
  - **Check now** re-checks at once.
- **WEBSITES tile** on the main view, the seventh: `6 OF 7 UP` with the down ones named, amber when any is down. It
  checks every 60 s in a runspace, so a dead site never holds the window.
- **The site list is config** (`scripts\websites.json`): name, URL, the URL the light checks, where, container,
  start script, deploy name, plus the deploy allowlist, Haven's SSH target and NPM's tunnel. When a site moves to
  Haven (P89 H3), only that file changes.
- **Open NPM**: NPM's admin page listens only on Haven's own `127.0.0.1:81` (`haven-proxy-fix.sh` step 2;
  `proxy-discovery.txt:278`). So the button opens Chase's SSH tunnel `ssh -N -L 8081:localhost:81
  chase@192.168.1.61` in a window, then `http://localhost:8081/`, the way the runbook says to reach it. No NPM API
  call, no stored login.
- **Haven deploys.** The allowlist is the two deploy scripts that already exist, `Deploy-Website.ps1` and
  `Publish-WikiMacros.ps1`, with a written slot for P89's `Deploy-HavenOps.ps1`. A click asks the phrase, then runs
  `scripts\Invoke-WebsiteDeploy.ps1 -Deploy <name>` in a window. The helper checks the allowlist again, runs only a
  `.ps1` in `D:\UO\haven-migration`, and keeps a transcript in `scripts\shard-console-output\deploys\` (git-ignored).
  The deploy scripts use scp and ssh, so they use Chase's own key. `-DryRun` prints the exact command and runs
  nothing.
- **Tests:** 12 new facts and 4 updated. Full console suite **264 of 264** (252 before, plus the 12). Every new
  fact was watched failing first.

## What changed, with file:line

| File | What |
|---|---|
| `scripts/websites.json` (new) | the 7 sites, 2 deploys, the deploy slot, Haven's SSH target, NPM's tunnel; with why each value is what it is |
| `scripts/Invoke-WebsiteDeploy.ps1` (new) | the deploy helper: allowlist check, folder check, `-DryRun`, transcript, exit 0/1/2 |
| `docker/dashboard/Start-Dashboard.ps1` (new) | Homepage's start script, the counterpart of `Start-TestQueue.ps1` (Homepage had none, and the console never runs compose itself) |
| `scripts/Shard-Console.ps1` | below |
| `scripts/tests/Shard-Console.Tests.ps1`, `scripts/tests/fixtures/websites-2026-10-14.json` (new) | the facts; the fixture is `websites.json` as written |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.8, one `### Staff` line |

In `Shard-Console.ps1`:
- `-Site` parameter :126.
- Config: `WebsitesFile`, `Websites`, `WebsiteDeployScript` :334.
- Phrase `deploy to haven` :746.
- Six actions, group Websites :980.
- Plan dispatch :2085.
- Safety :2316. A window `docker restart` names only a game-PC site's container from the config, never a shard;
  `ssh` only as exactly the NPM tunnel; the deploy helper only as `-Deploy <allowlisted>`, with the phrase in the
  plan.
- CORE: `ConvertFrom-WebsiteConfig` :3587, `Get-WebsiteState` :3650, `Get-WebsitesGlance` :3671,
  `Format-WebsitesPanel` :3694, `Get-WebsitePlan` :3724.
- Tile fit for any number of tiles :5794, with the row cap raised from 130 to 150 px.
- `Update-NetworkTile` re-fits the tiles when the DNS tile's words change (it set them directly before).
- SHELL: `Get-WebsiteProbe` :6072, `Start-WebsiteProbe` :6107, `Update-WebsitesView` :6114,
  `Update-WebsitesTile` :6128, `New-WebsiteButton` :6157.
- The tile :6753, the tab :7204, `-Status` :7406. Header comment, tooltips, CLI help.

**Statuses:** one GET with redirects not followed, so a 301 counts as up. A 2xx or 3xx is up; anything else, or a
refused connection, is down; no answer within 4 s is NO ANS. The NPM row's light checks `http://192.168.1.61/` (NPM's
proxy port), because the admin page is only reachable while the tunnel is open; its row says so.

**Not in the allowlist, on purpose:** `Haven-Wiki-Update.ps1` updates the DokuWiki container, with the wiki down
about a minute, and `Haven-Website-Deploy.ps1` is the first-time setup. Neither is a routine deploy. Both are named in
the config's `_deploySlots`.

## No secrets: the proof

`grep -n -i -E 'password|passwd|token|secret|apikey|api_key|BEGIN .*PRIVATE KEY|ssh-rsa AAAA|ssh-ed25519 AAAA|sshpass'`
over `websites.json`, `Invoke-WebsiteDeploy.ps1`, `Start-Dashboard.ps1`, the fixture, and the added lines of the
console diff found 6 lines. Every one is prose saying nothing is stored:
- `websites.json:3` and its fixture copy: "No key, password or token ever goes in this file";
- `Invoke-WebsiteDeploy.ps1:12`: "Nothing here holds or asks for a key, password or token";
- the console's `web.npm` tooltip, the WEBSITES section comment, and the tab caption.

The fact `P101_NothingSecretIsInTheConfigOrTheNewScripts` checks the same patterns as JSON keys or key material.
It went red when I planted `"password": "planted-for-the-test"` in `websites.json`, and green again after the file
was restored (`cmp` identical).

## Tests (each seen failing first)

New, in `scripts\tests\Shard-Console.Tests.ps1`:

| Fact | Covers |
|---|---|
| `P101_TheRealConfigReadsAsSevenSitesTwoDeploysAndTheNpmTunnel` | the real file, no problems; the fixture equals it |
| `P101_AConfigMissingAFieldLeavesThatSiteOutAndSaysWhy` | missing url, missing container, unknown deploy, a duplicate key: each left out and named; no file, not JSON, schema 2 give UNKNOWN; a privileged tunnel port and a bad ssh target are refused |
| `P101_EachResultReadsAsUpDownOrTimeout` | 200, 301 up; 404, 502, refused down; timeout NO ANS |
| `P101_TheTileCountsTheSitesUpAndTurnsAmberNamingTheDownOnes` | 7 OF 7 green; 6 OF 7 amber naming the site; three down in file order; CHECKING; the panel lines |
| `P101_DeployIsRefusedForAScriptNotInTheAllowlist` | the plan refuses a site with no deploy, a game-PC site, an unlisted deploy; safety refuses the helper with an unlisted name, without the phrase, or with extra arguments; the helper itself exits 2 |
| `P101_DeployDryRunPrintsTheExactCommandAndRunsNothing` | the plan's exact command; the helper's `-DryRun` against a stand-in script leaves no mark and no log folder; for real it runs and keeps one transcript; a script outside the allowed folder exits 2 |
| `P101_OpenNpmUsesTheConfigUrlAndTunnel` | a changed URL, port and target come through to the tunnel and the browser; any other ssh refused; no npm in the file is refused |
| `P101_RestartRedeployAndLogsAreForGamePcSitesAndNeverAShard` | the three commands; Haven sites refused; `docker restart` of sl-modernuo, sl-modernuo-test, sl-uo-status refused |
| `P101_TheProbeReadsUpDownAndNoAnswerFromRealSockets` | three TcpListeners on 127.0.0.1 answer 200, 503 and nothing |
| `P101_TheTileAndTheTabAreBuiltAndDrawn` | the form: tile, tab, six buttons, picker, a drawn result |
| `P101_NothingSecretIsInTheConfigOrTheNewScripts` | above |
| `P101_EveryWebsiteButtonRunHeadlessWithDryRunRunsNothing` | each of the six as `-DryRun -Action web.* -Site ...` |

Updated: the tab-order fact (Websites before LIVE shard), both P87 tile facts (seven tiles: seven across when wide,
four across in two rows at 1280 and below; Plain one row of seven), and the P84 tooltip fact covers the new actions
by itself.

**Seen failing first:**
- **Against the console before P101** (the file swapped back, then restored `cmp`-identical): 15 facts, 1 passed,
  14 failed. The one that passed is the secrets scan, which reads files, not the console.
- **The secrets scan, alone:** red with a planted password (above).
- **The three new safety rules, alone:** cut out on a copy, restored after. Red: Deploy (`not in the list`), Open
  NPM (`no other ssh`), Restart (`sl-modernuo`).

**Mistakes of mine, caught by the first runs:**
1. `Read-Fixture` parses capture files; the config fixture is now read as text.
2. PowerShell 5.1 has no `$PSScriptRoot` while it binds parameters, so the helper's default paths moved into its
   body.
3. The probe fact first expected a closed port to read down. Windows retries a refused connection for about 2 s, past
   the fact's 1 s timeout, so either reading is now accepted.
4. Seven tiles four across clipped PLAY TESTS' detail at 900 px. Three rows clipped PUBLIC DNS instead. The fix kept
   two rows and raised the row cap from 130 to 150 px. Since then the fact passes at all six sizes, three runs in a
   row. **What I did not establish:** the tile row reads 268 px at 900 px before and after, so I cannot say exactly
   why the cap fixed it, only that it did.

**The first full run: 264 facts, 262 passed, 2 failed**, both mine:
1. `P84_EveryControlInTheWindowHasATooltip`: the Check now button and the site picker had no tooltip. Both are now
   named (`web.check`, `web.pick`) with tooltips.
2. `P87_UOTilesNeverClipFromTheNarrowestWindowToAWideOne` at 900 px: `PUBLIC DNS: CHECKING needs 48 px, has 30`.
   `Update-NetworkTile` set the DNS tile's words directly, without re-fitting the tiles. Three across, those words
   always fit on one line, so it never showed; four across they wrap. It now goes through `Set-TileLook` (which
   re-fits) when its words change, and only re-colours when they do not. It passed when run alone because it depends
   on when the 1 s timer fires.

**`-Status` and a dry run of each new button, by hand:**
- `-Status`: `WEBSITES : 6 OF 7 UP down: Public website (no answer: ConnectFailure)`.
- `web.open homepage`: OPEN `explorer.exe http://localhost:3000/`.
- `web.restart homepage`: WINDOW `docker restart sl-dashboard`.
- `web.redeploy playtests`: WINDOW the `Start-TestQueue.ps1` call.
- `web.logs homepage`: WINDOW `docker logs --tail 200 sl-dashboard`.
- `web.deploy website`: CONFIRM `deploy to haven`, then WINDOW `... Invoke-WebsiteDeploy.ps1 -Deploy website`.
- `web.npm`: WINDOW `ssh -N -L 8081:localhost:81 chase@192.168.1.61`, then OPEN `http://localhost:8081/`.
- `web.restart website` and `web.deploy vault`: REFUSE, with the reason.
- `Invoke-WebsiteDeploy.ps1 -Deploy website -DryRun`: prints `& 'D:\UO\haven-migration\Deploy-Website.ps1'` and
  `DRY RUN: nothing was run`.
- `-Deploy haven-ops` and `-Deploy ../evil`: REFUSED, exit 2.

**Not done by hand:** a real Deploy (that publishes, and it is Chase's click), a real Open NPM (it needs Chase's key
at a prompt), and a look at the tab at real size.

## Deviations and decisions for Chase

1. **NPM status is NPM's proxy port**, not its admin page (only reachable through the tunnel). Up means NPM is
   proxying; it does not prove the admin page loads.
2. **Open NPM opens a tunnel**, not just a link, because the admin page is LAN-closed on purpose. The prompt said "a
   link". Without the tunnel the link would not load. Close the tunnel window when done.
3. **Homepage got a start script** (`Start-Dashboard.ps1`). The console never runs `docker compose` itself (an
   existing safety rule), and Homepage had no script.
4. **Restart and Redeploy ask no phrase.** They touch only local web containers, never a shard, and safety enforces
   that. Deploy asks `deploy to haven`.
5. **Play tests and Shard status are one container** (`sl-play-tests`), so restarting either restarts both.
6. **The public website shows down** because of the DNS finding at the top, not because of the console.
7. **Seven tiles** wrap to four across in two rows below about 1,500 px (UO look); Plain keeps one row of seven.

## For Chase

- **The DNS finding at the top.** It is the one thing here that affects players.
- To try the tab: open the Shard Console, Websites tab.
  - Pick Homepage, then Logs: a window with its last 200 lines.
  - Open NPM: a tunnel window (your key's passphrase if it asks), then the NPM login page in your browser.
  - Deploy to Haven on the website: type `deploy to haven`, and its window runs `Deploy-Website.ps1`, with the log in
    `D:\ShatteredLegacy\scripts\shard-console-output\deploys\`.
- When P89's `Deploy-HavenOps.ps1` exists: add it to `deploys` in `scripts\websites.json`, as the `_deploySlots`
  entry says.

## Repo size and preflight

New files: 3 KB (config), 4 KB (helper), 1 KB (start script), 3 KB (fixture); none near 5 MB. Deploy logs are `*.log`, which
`.gitignore:31` ignores: `git check-ignore -v scripts/shard-console-output/deploys/x.log` gives `.gitignore:31:*.log`.

`Commit-ShardWork.ps1 -DryRun`: code has 8 files pending (`CHANGELOG.md`, `VERSION`, `scripts/Shard-Console.ps1`,
`scripts/tests/Shard-Console.Tests.ps1`, `docker/dashboard/Start-Dashboard.ps1`, `scripts/Invoke-WebsiteDeploy.ps1`,
`scripts/tests/fixtures/websites-2026-10-14.json`, `scripts/websites.json`); docs has 4 (`notes/shard-console.md`, this
note, and the play-test importer's `testing/SUMMARY.md` and `testing/play-tests.json`, which are expected machine
output).

```
Repo Result
---- ------
code dry run
docs dry run
```

## Final full run

`scripts\tests\Shard-Console.Tests.ps1` under Windows PowerShell 5.1, after the two fixes: **264 facts, 264 passed,
0 failed**, exit 0.

P101 DONE
