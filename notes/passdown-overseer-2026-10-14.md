# Overseer pass-down, 2026-10-14 (15:45)

Supersedes `passdown-overseer-2026-10-13.md` (whose 10-14 updates are folded in here). The 10-05 file's "Role" and
"Rules" still hold. Read this whole file first, then `notes\decisions-2026-10-14.md`.

## How the work runs now

- **The queue.** Numbered prompts `cc-P<nn>-*.md` go straight into `D:\UO\cc-prompts\queue\` (Chase's standing rule);
  the runner hands the lowest number first, commits and pushes after `Pnn DONE`, archives to `completed\`. Max 6 per
  run, then it turns itself off; Chase starts the next run.
- **Two runners exist.** `D:\UO\cc-autopilot\` (old, **running now**: P108 handed 15:41) and `D:\UO\golem\` (P99, built,
  **not cut over yet**). Cutover is Chase's: Shard Console, Golem tab, **Move to the Golem** (dry run first; refuses
  while a prompt runs), then a new CC session in `D:\UO\shard-migration` and "Golem, please work on the shard tasks".
  Rollback: `D:\UO\golem\Move-ToGolem.ps1 -Rollback`. Golem fixes D90 (re-handed prompt never committed) and D91.
- **Unattended safety (overseer, 10-14):** `~\.claude\settings.json` now has `permissions.defaultMode: "auto"`,
  `skillOverrides: {"auto-mode-setup": "off"}`, `autoMode.environment` (repos, LAN, Haven, Docker), and a
  `PermissionRequest` hook `D:\UO\unattended-permission.ps1` that auto-denies any approval prompt while either runner's
  `ENABLED` exists (cwd under D:\UO or D:\ShatteredLegacy), logging to `D:\UO\unattended-denials.log`. Backup
  `settings.json.bak-20261014-unattended`. **Read that log after each overnight run.**
- **Both runners' hand-off text** treats `testing/play-tests.json`, `testing/SUMMARY.md` and `testing/bot-runs/` as
  machine output (backups `*.bak-20261014-botruns`).
- **Overnight bot:** scheduled task "SL overnight play tests", daily 01:30, args include **`-Commit HEAD`** (overseer
  added, so it never builds the Golem's half-done tree). Runs only when there is work; emails before and after.
- **Lessons:** commit overseer edits (`Commit-ShardWork.ps1 -Message ...`) before CC is handed a prompt, and never
  while CC is mid-prompt; keep each remote PowerShell call short (the bridge drops long ones); after a disconnect,
  check whether a write landed before redoing it.

## Done 10-14 (all pushed; read their notes when a question comes up)

P94 console run tile; P95 D89 boot fix; P96 Fix test shard tab (health check, good-* tags, rollback, prune);
P97 Bugs tab (+ reason required on ideas); P98 Building Duplicator (`[CaptureLayout`/`[StampLayout`); P99 Golem;
P100 Visual Builder (`[VBuild`); P101 Websites tab + NPM + one-click Haven deploys; P102 bot nightly + iCloud archive;
P103 TazUO fork + ClientCommand (tutorial buttons); P104 UORespawn read (idea only); P105 Haven H1; P106 Shard
question tab; P107 Haven ops move (H2+H3 scripts; Chase clicks the deploy).

Overseer did by hand 10-14: D93 workaround (`/p:NuGetAuditLevel=critical` in `docker/uo/Dockerfile`); Bugs tab
deployed; pruned 131 image tags (248 GB to 78 GB); **live deleted** (container, `uo-modernuo` images, world data;
kept `server\lib\uo\modernuo\status\`); desktop shortcuts "SL - TazUO TEST/LIVE" repointed to
`D:\UO\ShatteredLegacy\ShatteredLegacy-2026.10.02.0840` (backups `*.lnk.bak-20261014`).

## Queue (15:45)

| Prompt | State |
|---|---|
| P108 retire live: grey LIVE tile, `liveEnabled: false`, silent everywhere | **running** (old autopilot) |
| P109 Sunflower print queue to Haven | queued |
| P110 mega dashboard on Haven | queued |
| P111 in-game TazUO "Paperdoll bodies" option (SFW / Topless / Nude) | queued |
| P112 robot icon on play-test items the bot attempts tonight (all items still shown) | queued |

Next free prompt: **P113**. Next free bug: **D95** (re-derive). Next free feature: **F-45**.

## Standing decisions from Chase (10-14)

- **Faithful port first, customizations after**; finish what is started or requested. Port list in
  `notes\port-list-2026-10-13.md` (Pet Training: port fully, evo pets and companions on top).
- **Live does not exist** until a fresh 1.0 world. Test shard only. Never ask about live.
- Tutorial: hybrid trial order (option C); combat wing teaches melee and ranged; Rook is the recruiter; System voice is
  the Echo; TazUO patch yes; at the tutorial update **all accounts are wiped**.
- F-44 Inn room: one per character (character limit per account TBD), cannot grow, instanced via a gate in any Inn,
  weekly rent, items to bank with congratulations when a real house is placed.
- Haven pages: shape approved; Chase and his daughter get in; `ops.shatteredlegacyuo.com` behind Cloudflare Access;
  shard web login (H6) **sooner rather than later**; Haven deploys are one-click console functions Chase runs.
- Bot transcripts: 14 days in repo, then archive to iCloud (`D:\Cloud Drives\iCloudDrive`).
- Power Hour: rebuild natively later (Vita-Nex version breaks TazUO). Vault Pass and virtual storage: not now.
- Building Duplicator undo stays in memory (overseer suggestion, Chase asked; not formally confirmed).

## Waiting on Chase

1. **Golem cutover** at the next pause (after P108-P112 or a STOPPED).
2. **Router local DNS:** `shatteredlegacyuo.com` is mapped to 192.168.1.58 on the router (192.168.1.1), so the site
   looks down from inside the house only. Public DNS (216.247.206.76) and Haven are fine. Delete the entry or point it
   at 192.168.1.61. This also explains D47/D23 (sl-ddns "updating" every 5 min) and P101's finding.
3. **Haven deploys** from P107 (ops pages) and, later, P109 and P110: one click each on the Websites tab.
4. **Manual checks:** P98 capture/stamp, P100 `[VBuild`, P103 TazUO buttons (needs a test-shard build with them).
5. **The bug batches** (offered 10-14, no go yet): tooling (D91 remainder, D66, D37), Hammer of Hephaestus and smith
   deeds, smith menus, satchels, Despise, small gameplay, test harness. See the 10-14 overseer chat's grouping.
6. Optional cleanup: `D:\UO\question-proof\`, `D:\UO\third-party\code\uorespawn\_extracted-muo\`,
   `docker compose -p sl-uo-bot down -t 60`, Cloudflare `dashboard` record (Homepage is **not** public: verified).

## Record-keeping owed (overseer)

- Bug list: close **D94** (live gone) and D50's live half; D89 marked fixed (move to section 2); D93 worked around (still
  open for a pinned fix); correct D47/D23/P101 with the router finding; log **D95**: false NEEDS YOU emails still fire
  for background Bash commands (P99 only counts background agents).
- Fidelity register still ends at D-122 (see 10-13 file); promotions owed.
- Project doc `claude/passdown-overseer.md` mirrors this file.
