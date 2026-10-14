# Overseer pass-down, 2026-10-13 (10:05)

Supersedes `passdown-overseer-2026-10-05.md` for queue state and numbers. That file's role paragraph, rules and
"how this chat works" still hold, with the changes below. Read this first, then the 10-05 file's "Role" and "Rules".

## What changed in how the work runs (2026-10-12/13)

- **Autopilot** (`D:\UO\cc-autopilot\`, Chase's). CC runs the queue by itself: it hands CC the lowest-numbered
  `cc-P<nn>-*.md` in `D:\UO\cc-prompts\queue\`, runs `Commit-ShardWork.ps1` (commit AND push, both repos public) after
  `Pnn DONE`, archives the prompt, hands the next. Emails Chase on STOPPED, a mid-task stop, or a git failure.
  - **Standing rule (Chase): when the overseer builds a queue, numbered prompts go straight into `queue\`.** Lowest
    number runs first, so number in the order you want them run, or hold later ones out of `queue\` until earlier
    ones are handed.
  - A handed prompt leaves `queue\` and sits in `cc-prompts\` until done (then `completed\`). Do not edit a handed one.
  - Overseer edits to `cc-autopilot.ps1` (backups `.bak-20261012-2035`): a refused commit (exit 2) is handed back to
    CC to fix and say DONE again, up to 2 tries, then email; prompt titles have `"` replaced by `'` (a quote broke
    P86's commit, 10-13).
  - Restart after a pause: Chase commits (Console Commit tab), then sends CC "go".
- **Every prompt carries**: Patch notes, a "Repo size rule" (no file over 5 MB), a "Commit preflight" (CC runs
  `Commit-ShardWork.ps1 -DryRun` until both repos are clean before DONE), and Finishing (`Pnn DONE`). Copy the block
  from any of P86-P90.
- **Overseer edits to `D:\UO\Commit-ShardWork.ps1`** (backup `.bak-20261012-1855`): runs `tools\progress.py` before
  every commit (never blocks), so the status dashboard refreshes each commit; `.env.example` no longer trips the `.env`
  check (real `.env` files still do).
- **Ignores**: `notes/cc-P*-tools/*.png` (shard-migration `.gitignore`); `design/paperdoll-sos/kit/` and
  `client-addons/` (ShatteredLegacy `.git\info\exclude`; P81 was told to add them to `.gitignore` too: verify).
- **CC permissions**: `C:\Users\ckfle\.claude\settings.json` allows web requests to 192.168.1.58, .61, localhost,
  127.0.0.1 (backup `.bak-20261013-0950`). SSH is not allowed blanket.
- **Scheduled task "Shard upstream watch"** (cloud, Mondays 7:54 CT, trig_01E1kp7BHv5w8NVfomuE3tAD): ModernUO and
  ServUO changes since the pin, patch dry-runs, writes project doc `claude/upstream-watch-YYYY-MM-DD.md`, and a CC prompt
  draft when action is due (the overseer numbers it). Separate from Chase's daily "ServUO scout and downloads".
- **New chat recommended (not started yet)**: a migration reassessment chat to rebuild the ServUO port target for the
  shard's current direction (the dashboard's "27% of 2045" is from the wholesale-port era). Starter text was given to
  Chase on 10-13.

## Done and pushed since 10-05 (read their notes when a question comes up)

P66-P68, P71, P72 (research), P67 (finished 10-12), P73 test account wipe + Console button, P74 Autopilot tab, P83
play-test page (port 8093) + dashboard metrics, P34 winter decor, P36 dungeon build 1 (moves TEST to client data
7.0.117.0), P50, P65, P69, P70, P75 (notes), P76 (notes), P77 Alembic guild, P78 recipe gating, P79 loot boxes and
fanfare, P80 tutorial framework, P81 paperdoll art, P82 Artificers Imbuing, P84 Console UO skin + tooltips + output
pane, P85 status dashboard judgment + `/status`, P86 Disconnect VPN button, P87 Console readability, P88 shared menu,
P89 Haven plan (notes).

## Queue (10:05)

| Prompt | State |
|---|---|
| P90 feature-ideas inbox on the play-test page | **running** (handed 09:54) |
| P91 overnight play-test bot (scratch shard on 127.0.0.1:2595, its own accounts) | queued; numbered 10:05 from an unnumbered draft |

Next free prompt: **P92**. Nothing else is drafted.

## Waiting on Chase

1. **Deploy the play-test service** (it was never deployed; port 8093 still serves old nginx, so the page shows "not
   valid JSON"): `D:\ShatteredLegacy\docker\test-queue\Start-TestQueue.ps1`. P85's `/status`, P88's menu and P90 need it.
2. **P89's 11 decisions** (`notes\cc-P89-haven-pages-plan.md`, "Decisions for Chase"). **Decision 10 is a possible
   exposure:** `dashboard.shatteredlegacyuo.com` resolves to the house and is in Homepage's allowed hosts; if NPM routes
   it, Homepage (container details) is public now. Ask Chase to check NPM proxy hosts first. Then the Haven build
   prompts (H1...) from P89 Part C get numbered.
3. Outside access (Chase, 10-13): play tests, ideas and status must work away from home, behind a login; P89 recommends
   Cloudflare Access on `ops.shatteredlegacyuo.com`; shard-account login later with a separate `[webpassword`.
4. Play tests: 111 open, 1 failed (read `testing\play-tests.json` / `SUMMARY.md` and log the failure as a bug).
5. Open from P67/P71: P67's 4 caps at OSI tops (scale to 200?), Fletching stack recipes, Lumberjacking past 148,
   Lockpicking past 95/140, D88 (shard woods have no resource info, belongs with F-28); P71 Nerve Strike damage scaling.
   P72's 10 leveling-gear decisions go to the features chat.
6. Haven move order after decisions: P89 Part C.

## Record-keeping owed (overseer)

- Fidelity register still ends at **D-122** in `docs\fidelity-principle.md`. Promote: the D-122 amendment and D-123 to
  D-130 (P66, P67, P71), then everything later prompts proposed (grep notes for "Register line"). Re-derive next free.
- Bug list: next free **D89** (re-derive). Log the play-test failure and any bugs proposed in P74-P90 notes.
- `docs\client-test-queue.md`: P83 proposed freezing it with a pointer to the play-test page (decision 10 in P83).

## Lessons (10-12/13)

- The remote PowerShell from this chat drops on long calls: keep each call short (one `dir`, one file), and write
  files with a PowerShell here-string plus `[IO.File]::WriteAllText` (the FileSystem write tool timed out).
- Before blaming the queue, read `state.json` and the last lines of `autopilot.log`: three stalls on 10-12/13 were all
  commit refusals or a commit-message quoting bug, never CC.
- A prompt with a long title or quotes in its `#` line is fine now, but keep titles ASCII.
## Update 10:50

- Play-test service deployed by Chase (8093 now answers `sl-play-tests`; page and `/status` load). Waiting item 1 done.
- Chase agreed with `notes\port-list-2026-10-13.md`. Pet Training: **port fully**, evo pets and companions on top.
- **Direction (Chase): a faithful port comes first, our feature customizations after.** Finish work already started
  or requested. Weigh new feature prompts against this before drafting them.
- The port-list draft was numbered **P92** with those decisions written in and is in `queue\` behind P91.
  Next free prompt: **P93**.- (10:55) Customizations moved behind the port where not started: F-12 Levels and loops and F-37 Commissions now sit
  last in the work list with an "After the port" note; P83-DEPLOY marked done; `docs\feature-queue.md` has the order
  line at the top. Kept: TUTORIAL (P80 framework built), P90-P92 (port or tooling). The open P67/P71/P72 calls
  (caps past OSI, Fletching, Lumberjacking, Lockpicking, Nerve Strike, leveling gear) are after-the-port too.
  These edits are uncommitted in shard-migration; autopilot commits them with P90.
## Update 2026-10-14 05:50

- Overnight: P91 (play-test bot), P92 (port-list headline), P93 (servuo.dev code port assessment) all DONE and pushed.
  Queue went empty 17:29, autopilot off.
- P93 sent five false "NEEDS YOU: stopped mid-task" emails 17:16-17:23 before its real DONE (parallel subagents).
- P93 drafts P94-P98 live inside the assessment, not queued, waiting on Chase's go. They will be renumbered from P95
  because the autopilot progress-console draft was numbered **P94** (standard Before/Repo size/Preflight sections added,
  plus a report-only look at the false emails) and is in `queue\`. Next free number: **P95**.
## Update 2026-10-14 06:10

- Chase answered the open questions: all recorded in `notes\decisions-2026-10-14.md`.
- D89 (HEAD does not boot) logged in `docs\bug-list.md`; next free bug **D90**. Fix prompt **P95** queued behind P94.
- `docs\client-test-queue.md` rule reworded per P91 (bot gathers evidence, Chase marks).
- Still to draft (in order): Building Duplicator, Visual Builder (from P93's drafts), Shard Console website controls
  plus NPM tab plus Haven deploy buttons, bot nightly task (only when items, email before and after, transcript
  retention), ideas reason-required, TazUO tutorial patch, UORespawn closer read, Haven H1 (H6 login moved up).
  Next free prompt: **P96**.
- (06:15) **P96 bug-reports inbox** (plus reason required on ideas) queued. Next free prompt **P97**. Bot transcripts: 14 days, then archive to iCloud Drive (`D:\Cloud Drives\iCloudDrive`); goes in the bot prompt.

- (06:35) F-44 Inn room decisions added to `docs\feature-queue.md` (per character, cannot grow, instanced via a gate in
  any Inn, weekly rent, items to bank on placing a real house). Drafted and queued **P97-P103**: Building Duplicator,
  Visual Builder, console Websites tab (+NPM, Haven deploys), bot nightly + iCloud archive, TazUO ClientCommand
  patch, UORespawn read, Haven H1. Next free prompt **P104**. Autopilot sorts numerically, so P100+ is safe.

- (06:40) **Lesson:** P94 STOPPED at 06:01 because the overseer's own passdown append was uncommitted in shard-migration (every prompt's "Before you start" refuses non-CC changes). **Commit overseer edits with `Commit-ShardWork.ps1 -Message ...` before CC is handed a prompt.** Committed, P94 moved back to `queue\`.

- (07:20) Test shard down at 07:07 from D89 (HEAD deploy). Queue renumbered: new **P96 Fix test shard** (console panel, health check, good-build tags, rollback, prune); old P96-P103 are now P97-P104. Next free **P105**.

- (07:45) Chase renamed autopilot to **the Golem**; start phrase "Golem, please work on the shard tasks". **P105** builds D:\UO\golem beside cc-autopilot, renames every console button and string (Wake/Rest the Golem, GOLEM tile), fixes D90-D92 in both, and leaves a cutover script Chase runs. Next free **P106**. Bug batches still to draft on Chase's go.

## Update 2026-10-14 10:20

- P95 (D89 boot fix), P96 (Fix test shard tab, health check, good-* tags), P97 (Bugs tab) DONE and pushed. Test shard healthy on sl-modernuo:good-61db33c.
- P98 (Building Duplicator) work complete but STOPPED: every build fails on NuGet audit (logged **D93**). Overseer committed P98's files; prompt archived. Waiting on Chase's audit decision before the queue resumes at P99.
- Live container stuck at a delete prompt (logged **D94**); do not answer y. Next free bug **D95**.
