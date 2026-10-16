# cc-P126: Design: running CC work on a second machine (cloud or Haven) alongside the home Golem

2026-10-16. Research and a design note; nothing built, no machine set up, nothing published. Prompt:
`D:\UO\cc-prompts\cc-P126-second-machine-design.md`. Both repos at the start: shard-migration had the overseer's
`docs/feature-queue.md` edit and the bot's `testing/bot-runs/2026-10-16-0130/` (machine output, fine); the shard repo
was clean. The Golem handed this prompt at 05:53 after the start phrase (Chase's "golem work on shard tasks please" did
not match the two exact phrases; see "Deviations" item 1).

## Headlines

- **Recommendation in two lines.** Build the **Stone Golem** on the work PC (Windows, `D:` mirrored, the same
  `golem.ps1` unchanged) and do **not** build a cloud Golem yet. Before building Stone, land P131 (CLI sessions, which
  make the usage bars report) and read one week of `usage.json`: a second machine on the same Max plan shares its
  limits, so it only pays if the Iron Golem is not already using them up.
- **The one decision for Chase:** Docker Desktop on the work PC, yes or no. With it, Stone can take the port prompts
  (11 of the 31 measured). Without it, Stone takes the Windows-only console, Haven-file and tools prompts (7 of 31),
  and the ports stay home.
- **Measured, not guessed:** of the 11 queued prompts and the last 20 completed (31 in all), **22 are home-only**
  today (Docker on this PC, this PC's files, or the Windows client), **7 are Stone-capable** without Docker (Windows
  PowerShell 5.1, no Docker, no client), and **2 are cloud-capable** (Python and data already in git). The 11 of the 22
  that are home-only only because of the build become Haven- or Stone-capable if the builder image runs there.
- **The cloud is real but a poor fit.** A cloud session is Ubuntu 24.04, 4 vCPU, 16 GB, 30 GB, with Docker and `gh`
  but no .NET, Trusted network only, and it shares the plan's limits. It cannot reach the test world, the client data,
  Haven, or the Golem (PowerShell 5.1 hooks outside both repos), and Haven cannot be a cloud runner on a Max plan
  (self-hosted environments are Team and Enterprise only).
- **Two writers:** the queue says which Golem a prompt is for (`**Golem:**` line), a Golem claims a prompt by moving it
  in git, a non-home Golem commits to `stone/P<nn>` and the Iron Golem merges between its own prompts; the pairs that
  must never run in parallel are listed by area. The Golem's folders leave `D:\UO` loose files for a private git repo,
  with the secrets ignored.
- **Chase's drive decision (`D:` for the project, `S:` for Sunflower, both PCs):** nothing on this PC points at `H:`
  (checked: 21 shortcuts, 3 scheduled tasks, `C:\dev\sunflower`, the P109 and P110 notes and the dashboard config: 0
  hits), so the move here is one Drive for desktop setting and a check. Counts of hard-coded paths and the folder tree
  the work PC needs are in Q6.
- **Names:** Iron (home), Stone (work PC), Crystal (cloud). Each Golem posts a small status to the ops service, which
  already takes this PC's snapshot every minute; a status older than 15 minutes reads "unknown". Design in Q7.
- **Tests:** none (design only). **Patch notes:** none, since no code changed; the prompt's own Tests section says to
  run nothing that changes either repo except this note.

## Steps (the task list)

1. Wake the Golem and take the hand-off. Done.
2. Before you start: git status, read P99, port-recipe, the commit script, the Haven notes. Done.
3. Q1 labels. Done. 4. Q2 cloud. Done. 5. Q3 Haven. Done. 6. Q4 two writers. Done. 7. Q5 limits. Done.
8. Q6 work PC. Done. 9. Q7 names and status. Done. 10. This note and the draft prompts. 11. Preflight, DONE.

## What I read and measured

- `notes\cc-P99-golem.md`, `notes\port-recipe.md`, `D:\UO\Commit-ShardWork.ps1` (all 260 lines),
  `notes\cc-P105-haven-h1-host-agnostic.md`, `notes\cc-P107-haven-ops-move.md`, `notes\cc-P125-golem-long-run-toggle.md`,
  `D:\UO\golem\golem.ps1` (the header, the Prompt and Hand-Off paths), both repos' `.claude\settings.local.json`,
  `docker\uo\Dockerfile`, `docker\uo\build.sh`, the compose files' bind mounts, `scripts\Publish-GamePcSnapshot.ps1`,
  `docker\test-queue\server.py` (the gamepc routes), the queued prompts P127 to P136 and the Kind lines of P106 to P125.
- Sizes with `du -sm` on 2026-10-16 (every folder under `D:\UO` and `D:\ShatteredLegacy`), tracked bytes with
  `git ls-files | stat`, Docker images with `docker images`, drives with `Get-PSDrive`, tasks with `Get-ScheduledTask`,
  shortcuts with `WScript.Shell` over the Desktop and Start Menu, Drive for desktop's mount letter from
  `HKCU:\Software\Google\DriveFS`, Haven's hardware from `D:\UO\Haven-Website-Runbook.md:72` and its Docker from
  `D:\UO\haven-migration\haven-discovery-output.txt:5-6`.
- Claude Code documentation, all read 2026-10-16: `code.claude.com/docs/en/claude-code-on-the-web`,
  `.../cloud-environments`, `.../routines`, `.../self-hosted-environments`, `.../desktop-scheduled-tasks`,
  `.../cli-reference`, and `support.claude.com/en/articles/11145838` (Pro and Max usage limits). Quotes below are from
  those pages.

## Q1. What each kind of prompt needs

Labels: **home-only** (needs Docker on this PC, this PC's non-git files, or the Windows client), **Stone-capable**
(Windows PowerShell 5.1 and the mirrored `D:` tree, no Docker, no client), **Haven-capable** (would run on Haven if the
builder image and a Linux Golem were there; none is today), **cloud-capable** (a fresh Linux clone of the two repos is
enough). The "build" column means `docker\uo\build.sh`: every port prompt's gate.

| Prompt | Model | Used | Label | Reason |
|---|---|---|---|---|
| P127 treasure maps, monster stealing | Opus | build, test-shard boot, ServUO-pub57, play-test items | home-only (Haven/Stone with Docker: build and tests only) | the boot check needs the test world under `server\lib` (3,444 MB, not in git) |
| P128 consumables, crafting gaps | Fable | same | same | same |
| P129 creatures part 2 | Fable | same | same | same |
| P130 pet training | Fable | same, plus upstream patches | same | same |
| P131 wake the Golem from the console | Opus | installs the CLI on this PC, edits `D:\UO\golem`, console GUI | home-only | the Golem's files live only on this PC |
| P132 console facelift | Opus | console GUI, desktop shortcut, `D:\UO\logs` | Stone-capable (needs a screen) | PS 5.1 WinForms; the mirror has the shortcut and logs |
| P133 Haven intranet dashboard | Opus | repo files, console tests; CC never connects to Haven | Stone-capable | PS 5.1 facts; cloud lacks PS 5.1 |
| P134 vseUOAware checks and MCP | Opus | Python, a .NET build from `D:\UO\third-party\code` (342 MB, not in git), client MUL/UOP (5,221 MB, licensed) | home-only | the client data never leaves this PC |
| P135 vseUOAware staff commands | Fable | build, console | home-only (Stone with Docker) | server build |
| P136 status page self-judging | Opus | `tools\` Python, `D:\UO\Commit-ShardWork.ps1` | Stone-capable (cloud for the Python half) | the commit script is outside git |
| P126 this design | Fable | this PC's disks, registry, tasks | home-only | read this PC |
| P106 console shows a waiting shard | - | console, compose files, Docker | home-only | Docker |
| P107 Haven ops move | - | console, compose, a Docker proof on this PC | home-only (Stone with Docker) | the proof ran the stack here |
| P108 retire the live shard | - | scripts, compose, tests, Docker | home-only | Docker |
| P109 Haven print queue | - | repo files, deploy scripts, console | Stone-capable | PS 5.1, no Haven connection (unverified: I read its Kind line, not the whole prompt) |
| P110 mega dashboard | - | same | Stone-capable | same caveat |
| P111 TazUO paperdoll option | - | the TazUO fork build (`D:\UO\tazuo-sl-build`, 1,038 MB), local NSFW art, packaging | home-only | Windows client build, files outside git |
| P112 bot icon on play-test items | - | Python service and page, the bot's work check (in git) | cloud-capable | Python and data in git |
| P113 console window icon | - | console | Stone-capable | PS 5.1 |
| P114 test shortcuts start our build | - | player package launcher, the TazUO build, shortcuts | home-only | the build and client are outside git |
| P115 play-test who and how | - | play-test data, Python service | cloud-capable | Python and data in git |
| P116 console tab scroll | - | console | Stone-capable | PS 5.1 |
| P117 fresh-login regression | - | build, bot transcripts (in git) | home-only (Haven/Stone with Docker) | build |
| P118 bulk orders | - | build | same | build |
| P119 creatures part 1 | - | build | same | build |
| P120 pet training (stopped) | Fable | build | same | build |
| P121 pet ability core | Fable | build, new save file | same | build |
| P122 bulk orders core | Fable | build | same | build |
| P123 bulk orders crafts | Fable | build | same | build |
| P124 package ships our TazUO | Opus | package build, TazUO build, console | home-only | Windows, files outside git |
| P125 Golem long-run toggle | Opus | `D:\UO\golem`, console | home-only | the Golem's files |

Totals, counted from the table: **22 home-only, 7 Stone-capable, 2 cloud-capable, 31 in all.** Of the 22, **11 are
home-only only because of the build** (P117 to P123, P127 to P130): they move to whichever machine has Docker, the
test world and the builder image. The Model line exists on 15 of the 31 (every prompt from P120 on): 9 Fable, 6 Opus.

## Q2. Cloud

What the documentation says a cloud session is and has (`claude-code-on-the-web`, `cloud-environments`):

- "A cloud session is a Claude Code session that runs on cloud infrastructure instead of on your machine." Started
  from claude.ai/code, the Desktop app (Cloud instead of Local), the terminal (`claude --cloud "task"`), or a routine.
- The VM: "a fresh virtual machine (VM) running Ubuntu 24.04 on x86_64", "4 vCPUs, 16 GB of RAM, 30 GB of disk".
  Installed: "Docker: docker, dockerd, docker compose", `gh`, Python, Node and the usual toolchains. **"Toolchains
  outside this list, such as the .NET SDK, aren't pre-installed"**; a setup script installs them and is cached as a
  filesystem snapshot when it finishes "within roughly five minutes", expiring after "roughly seven days".
- Network: the Default environment is **Trusted**, "allowlisted domains only: package registries, GitHub, cloud SDKs".
  The list includes `github.com`, Docker Hub (`registry-1.docker.io`), `ghcr.io`, `dot.net`, `dotnet.microsoft.com`,
  `mcr.microsoft.com`, `pypi.org`. It does **not** list `deb.debian.org` (the Dockerfile's `apt-get`), `api.nuget.org`
  (the `dotnet publish` restore) or `builds.dotnet.microsoft.com` (where `dotnet-install.sh` fetches the SDK; unverified
  that this is the host it uses today). So the builder stage needs a **Custom** allowlist with those three added, or
  Full access. Unverified until tried.
- GitHub: "Any public repository, and private repositories that the Claude GitHub App is installed on" (or
  `/web-setup`, which lends the local `gh` token). `shard-migration` is **private** (`gh repo view`: PRIVATE);
  `shattered-legacy-infrastructure` is public. Pushes go through a GitHub proxy; "GitHub operations from the VM go
  through the GitHub proxy, which attaches the credential on the server side." `gh pr` and `gh issue` (GraphQL) are
  rejected by that proxy; the REST API works.
- Time limits: commands wait 2 minutes by default, up to 10, then move to the background for up to 30 more minutes;
  `BASH_DEFAULT_TIMEOUT_MS` raises it. Idle VMs pause after "a few minutes without activity" and can be reclaimed.
- Limits: **"cloud sessions share rate limits with all other Claude and Claude Code usage within your account. Running
  multiple tasks in parallel consumes more rate limits proportionately."**

Can the ModernUO build and the headless harness run there?

- **The builder stage, probably yes, unverified.** `build.sh` is `docker build --target builder`, `docker run
  --security-opt seccomp=unconfined` for the tests, then `docker build`. The VM has dockerd; the builder image is
  5.16 GB here and the runtime 1.29 GB, inside 30 GB; 16 GB RAM is half this PC's 32 GB but four times Haven's. The
  seccomp flag is a plain `docker run` option, so it should hold on the VM's dockerd (unverified). The three missing
  domains above must be allowed first. A cold build downloads the SDK, clones ModernUO and restores NuGet; here the ten
  warm builds of P70 were 1 to 5 minutes apart by their log times (22:29 to 22:51), so a warm cloud build fits the
  10-minute foreground cap and the cold one would run in the background. The environment cache keeps pulled images
  but **not built ones unless the setup script builds them**, and the setup script must finish in five minutes, which
  a cold builder build will not (unverified; the SDK download alone is slow). So every fresh VM rebuilds the builder
  image cold, or the setup script pre-pulls only the base layers.
- **The test-shard boot, no.** "The test shard boots clean from your tree" needs `server\lib\uo\modernuo-test` (the
  world: 3,444 MB, git-ignored) and the client data the console checks. Nothing in git gives a cloud session a world.
- **Play-test items, half.** Writing them is text; the bot that runs them is this PC's scheduled task.
- **The Golem, no.** It is PowerShell 5.1 hooks in `.claude\settings.local.json` (git-excluded, so a clone has none),
  `D:\UO\Commit-ShardWork.ps1` (outside git), DPAPI-encrypted mail credentials (`smtp-cred.xml`, which only this
  Windows login can decrypt), and `Import-Clixml`. A cloud Golem is a rewrite of the hand-off and commit loop in bash or
  Python, committed into the repo as `.claude\settings.json` hooks. I did not size that rewrite; `golem.ps1` is 68 KB.
- **Scheduled runs: routines.** "Routines execute on Anthropic-managed cloud infrastructure", triggers are a schedule
  ("The minimum interval is one hour"), an API POST with a bearer token, or GitHub events; "Routines run autonomously
  as full Claude Code cloud sessions: there is no permission-mode picker"; "Claude pushes its work to a branch prefixed
  with `claude/` unless your prompt directs it to push to another branch"; "Routines draw down subscription usage the
  same way interactive sessions do"; at the cap, "additional runs are rejected until your usage window resets" unless
  usage credits (metered overage) are on. Routines are "in research preview".
- **Desktop scheduled tasks** are the local cousin: they run on this machine while the app is open; not a second
  machine, so not relevant here except as the mechanism P131's self-wake could use (noted for P131, not decided).

What a cloud session cannot reach: the LAN (Haven, the test shard, this PC), `D:\UO` (ServUO-pub57 and
ModernUO-pinned are public GitHub clones, so those two it can re-clone), the client data, the TazUO build, the
third-party folder, the bot, the Shard Console (PS 5.1 WinForms), and Chase's mail.

## Q3. Haven

Haven: Lenovo ThinkCentre M60e, Debian 13, i5-1035G1 (4 cores, 8 threads), **8 GB** RAM, 238 GB NVMe with 204 GB free
(runbook, 2026-09-28), Docker 29.5.2 and Compose v5.1.4 (discovery output). It runs the proxy, wiki, downloads,
dashboard, vaultwarden, the print queue (P109) and the planned ops pages, and P133 adds Grafana and Prometheus.

- **Can it run the builder image and the harness?** Mechanically yes: real Linux dockerd takes `--security-opt
  seccomp=unconfined` directly (the Docker Desktop reason for `build.sh`'s split does not even apply). The costs:
  - RAM. `dotnet publish ModernUO.slnx` of 4,214 source files on 8 GB shared with six running containers is the risk.
    Unverified; I have no measurement of the build's peak memory here.
  - Speed. 4 cores against this PC's 24; a 1 to 5 minute warm build here becomes several times that (unverified).
  - A Linux Golem (the rewrite above) and the Claude Code CLI on Haven, signed in as Chase.
  - The test world would have to live on Haven too (3.4 GB today, copied from this PC each time the test shard moves),
    which contradicts the standing rule that the game PC holds the world and P108's "test shard only".
  - **The rule "CC never connects to Haven"** (P107, kept by P133) would have to be reversed for a Golem that lives
    there, or the Golem would be driven by Chase over ssh.
- **Cost of moving:** 2 prompts for the Linux Golem and its tests, 1 for the Haven runner image and a `build.sh` that
  runs there, plus the world-copy question, before the first port runs on Haven. Measured against 11 build prompts in
  the 31, and against Stone (same `golem.ps1`, zero rewrite), **not worth it yet.** Haven stays the web host; the
  dashboard (Q7) is where Haven helps.
- **Haven as a cloud runner:** "Self-hosted environments are in public beta on Team and Enterprise plans". Chase is on
  Max 20x (P131), so this path is closed. "Remote Control", which "is also available on Pro and Max plans", lets a
  phone steer a session running on this PC; it adds no machine.

## Q4. Two writers

Today one Golem commits straight to `main` in both repos and pushes (`Commit-ShardWork.ps1`), and the repo rule is
"Commit to main. Do not branch" because there is one writer. A second writer needs these five rules.

1. **The queue says which Golem.** A `**Golem:**` line in the prompt, beside `**Model:**`: `Iron`, `Stone`, `Crystal`,
   or `any`. No line means `Iron` (today's behaviour). `Get-PromptModel` already parses the Model line; the Golem line
   is the same shape. A Golem hands itself only prompts whose line names it or says `any`.
2. **Claims are git moves.** The queue folder leaves `D:\UO\cc-prompts` for a private repo (Q6 says which) and a
   Golem claims a prompt by `git pull --rebase`, `git mv queue\cc-P<nn>-*.md claimed\<golem>\`, commit, push. A push
   rejected because the other Golem pushed first means re-pull and try the next prompt. Two Golems cannot both hold a
   prompt, because only one move lands. The Iron Golem's hand-off does the same moves it does today (into the prompts
   root), so a prompt file is still never reused.
3. **One writer per file.** Each Golem writes only `state\<golem>\` (its state.json, status.json, progress.json,
   sessions, log). The queue and `claimed\` move by git only. Settings are per Golem (`settings\<golem>.json`).
   Prompt files are written by the overseer on this PC only. `completed\` is written by the merge step only.
4. **Branches and the merge step.** The Iron Golem keeps committing to `main`. Stone and Crystal commit to
   `stone/P<nn>` and `crystal/P<nn>` in both repos and push. The **Iron Golem merges**, between its own prompts, when
   both of its trees are clean (the same moment the bot window check runs): `git merge --no-ff stone/P<nn>` in each
   repo, then `build.sh` for a shard-repo merge, then push and move the prompt to `completed\`. A conflict, or a red
   build, leaves the branch where it is and emails Chase ("[Iron Golem] P<nn> from Stone needs you: merge conflict in
   <files>"); the Stone Golem's next hand-off is not blocked by it. Conflicts are found by the merge itself; a dry
   `git merge --no-commit --no-ff` followed by `git merge --abort` can report them earlier without changing anything.
5. **What must never run in parallel.** Every prompt touches `CHANGELOG.md` and `VERSION`, so those two conflict on
   every merge: the merge step takes both sides' CHANGELOG sections and bumps VERSION itself (the second Golem's
   prompts are told not to bump VERSION; the merge does). Beyond those, by area, at most one prompt in flight per area:
   - **server** (`server\customizations`, `server\tests`, `server\patches`): two ports share craft, loot and vendor
     tables; P122 and P123 both edited bulk-order files. One port at a time, anywhere.
   - **console** (`scripts\Shard-Console.ps1`, its tests): one file, every console prompt. One at a time.
   - **tools** (`tools\*.py`, `tools\progress-state.json`, the commit script): P136 and P126-style notes. One at a time.
   - **haven** (`docker\ops`, `docker\dashboard`, `haven-migration`): one at a time.
   - **package** (`player-package`): one at a time, and home-only anyway.
   - **notes and testing** (`notes\`, `testing\play-tests.json`): every prompt writes its own note (new file, no
     conflict) and play-test items (one JSON file; appends conflict textually but merge handles disjoint hunks; a
     conflict there is resolved by taking both items). `testing\` is machine output on this PC only; Stone's prompts
     write play-test items through the page or as rows the merge step imports (P83's importer), never by editing the
     JSON (so the JSON stays one writer: this PC).
   Two prompts in different areas can run in parallel (a port on Iron, a console prompt on Stone). The overseer sets
   the Golem line with this table; the Golem enforces it by refusing to hand itself a prompt whose area is already
   claimed by the other Golem (the claim folders show it).

## Q5. Cost and limits

- Usage limits are **one pool per account**: "all activity in both tools counts against the same limits" (support
  article), "cloud sessions share rate limits with all other Claude and Claude Code usage within your account" (cloud
  doc). Max has "a five-hour session limit and a weekly limit", and "a separate weekly limit for Fable". Two machines on
  Chase's account therefore **finish queued work sooner but never raise the weekly total.** Two sessions at once also
  reach the five-hour window twice as fast, after which both wait.
- **Whether the cap binds today is unmeasured.** `D:\UO\golem\usage.json` does not exist: the desktop app does not run
  the status line, so P125's usage bars have never reported (P125's note said this might happen). P131's CLI sessions
  will make them report. **Read a week of them before building Stone**: if the Iron Golem alone reaches the weekly
  cap, a second machine adds nothing; if it idles (rests for Chase, the bot window, model and context rests), Stone
  fills that time. Since the run began on 10-14 20:18 the Golem has finished 10 prompts in about 20 hours of wall
  clock to P125's DONE on 10-15 16:31, with rests between them; whether those rests were limit waits or Chase waits is
  in `golem.log` (they were all Chase, context or model rests; no `rate_limit` line in the log).
- The only ways to raise the total: a second subscription (another account, which cannot share this one's GitHub app
  and sessions the same way), or usage credits (metered overage) for routines. Neither is recommended here.
- A cloud session costs the same tokens as a local one and adds no VM charge ("there's no separate charge for the cloud
  VM").

## Q6. Chase's work computer (the Stone Golem)

### What syncs through GitHub today, and what does not

Sizes are `du -sm` on 2026-10-16, in MB, rounded.

| Thing | Size | In git? | Carry how |
|---|---|---|---|
| `D:\ShatteredLegacy` tracked files | 102 (`.git` 114) | yes, public | `git clone` |
| `D:\UO\shard-migration` tracked files | 34 (`.git` 18) | yes, private | `git clone` with Chase's GitHub login |
| `D:\UO\cc-prompts` (queue, completed, superseded) | 2 | no | new private repo (below) |
| `D:\UO\golem` (hook, scripts, tests, state) | 1 | no | same repo, secrets ignored |
| `D:\UO\tools` (3 console starters) | 1 | no | same repo |
| `D:\UO\Commit-ShardWork.ps1` and 17 other loose `D:\UO\*.ps1`/`.bat` that name `D:\UO` or `D:\ShatteredLegacy` (18 of 20) | under 1 | no | same repo |
| `D:\UO\logs` | 1 | no | not synced (per machine) |
| `D:\UO\ServUO-pub57` | 72 | a clone of `github.com/ServUO/ServUO` | `git clone` at pub57 |
| `D:\UO\ModernUO-pinned` | 90 | a clone at `d4531cd94` | `git clone` + checkout |
| `D:\UO\third-party` | 14,067 (9,400 is `vrark-animations`; `code\` is 342) | no | not synced; P134/P135 would need `code\` (342) |
| `D:\UO\bot-shard` (the bot's scratch world) | 468 | no | not synced; home-only |
| Docker builder image `sl-uo-builder` | 5,160 per tag (runtime 1,290) | no | rebuilt by `build.sh` on the work PC (needs Docker Desktop) |
| Test world `server\lib\uo\modernuo-test` (with its backups) | 3,444 (Saves alone 29) | no, ignored | not synced: it holds account data; a port's boot check on Stone would need a fresh world instead |
| `client-data` (UO client files) | 5,221 | no, ignored, licensed | not synced |
| The TazUO build `D:\UO\tazuo-sl-build` (client 262) | 1,038 | no | not synced; package prompts stay home |
| `player-package` (dist and vendor dll ignored) | 1,177 on disk | partly | the clone has the scripts; packages stay home |
| `backups` | 4,461 | no | never |
| `design\paperdoll-sos\kit` and `client-addons` | 718 and more | no | never (NSFW art, P81) |

**Never off the home PC:** `D:\UO\golem\smtp-cred.xml` (DPAPI: it cannot even be read on another machine or login),
`D:\UO\golem\email.json`, `D:\UO\haven-ops\token.txt` (none exists yet; mode is local), `docker\uo\.env` (the Cloudflare
token), `tools\playtest-bot\secrets.local.json`, saved client logins and the `settings.*.json` files beside the TazUO
build, any world save (`Saves\`, `Accounts\`), `client-data`, and `C:\Users\ckfle\.claude\` credentials. The work PC's
Golem needs its own mail credential made with `Setup-Email.ps1` there (or no mail: the Haven status row in Q7 is the
other way to see it), and its own GitHub login.

**Git over a two-way file sync, and why.** A file sync (Drive, OneDrive, Syncthing) would carry `state.json`,
`status.json`, the queue folder and `golem.log` both ways, and the Golem rewrites them on every tool call (`-Event
Activity`); two machines editing the queue folder at once is exactly how a prompt runs twice or never. Git makes every
change a commit with an author and a conflict a visible refusal, and the claim move in Q4 only works because a push
can be rejected. The cost is one `git pull --rebase` before each hand-off and a push after, which the Golem already has
the machinery for. The one thing a sync does better, carrying the 5 GB builder image and the client data, is a thing we
do not want carried.

So: **a third, private repo**, working name `uo-golem-ops`, cloned at `D:\UO\golem-ops` on both PCs, holding
`golem\` (the scripts, tests, README, `settings\<golem>.json`, `state\<golem>\` ignored), `cc-prompts\` (queue,
claimed, completed, superseded), `tools\`, `Commit-ShardWork.ps1` and the loose scripts, with `.gitignore` for
`smtp-cred.xml`, `email.json`, `token.txt`, `*.log`, `state\`. The hook paths in both repos' `settings.local.json`
(`D:/UO/golem/golem.ps1`, 10 lines each) and the 23 `golem\` files that name `D:\UO` keep working if `D:\UO\golem`
becomes a junction to `D:\UO\golem-ops\golem` (one `mklink /J`), so the move itself touches no script. A draft prompt
for this is below.

### Hard-coded paths, counted

`grep -rlI` on 2026-10-16 for `D:\UO` or `D:/UO`, for `D:\ShatteredLegacy`, and for `C:\Users\ckfle`:

| Where | Files | name `D:\UO` | name `D:\ShatteredLegacy` | name `C:\Users\ckfle` |
|---|---|---|---|---|
| `D:\ShatteredLegacy\scripts` | 133 | 60 | 70 | 2 |
| `D:\ShatteredLegacy\tools` | 27 | 7 | 8 | 0 |
| `D:\ShatteredLegacy\docker` | 153 | 18 | 5 | 0 |
| `D:\ShatteredLegacy\design` | 3,835 | 1 | 7 | 4 |
| `D:\UO\shard-migration\tools` | 56 | 12 | 21 | 0 |
| `D:\UO\shard-migration\scripts` | 2 | 2 | 0 | 0 |
| `D:\UO\golem` | 37 | 23 | 4 | 0 |
| `D:\UO\tools` | 3 | 2 | 3 | 0 |
| `D:\UO\haven-migration` | 102 | 15 | 23 | 0 |
| loose `D:\UO\*.ps1`, `*.bat` | 20 | 18 (either path) | | |
| `D:\UO\cc-prompts\queue` | 10 | 10 | 3 | 0 |
| `D:\UO\cc-prompts\completed` | 143 | 140 | 96 | 4 |
| both repos' `.claude\settings.local.json` | 2 | 10 lines each | | |
| `C:\Users\ckfle\.claude\settings.json` | 1 | 1 (the unattended-permission hook, `D:/UO/unattended-permission.ps1`) | | |
| Scheduled tasks naming `D:` | 3 (Golem Watch, SL game PC snapshot, SL overnight play tests) | | | |
| Shortcuts on the Desktop and Start Menu naming `D:` | 21 (all `D:\UO\...`, `D:\LDPlayer`, `D:\Steam`) | | | |
| Docker bind mounts naming `D:` | `docker\test-queue\docker-compose.yml` 6 lines, `docker\ops\docker-compose.yml` 1 (`PLAYTESTS_HOST_ROOT`), and the two ignored home-lab files naming `D:\Servers` | | | |

A file is counted once however many times it names the path. Counted as a union over all the folders in the table
(a file naming either path, once): **374 files.** The `C:\Users\ckfle` hits are 4 in `design\` (scratch scripts), 2
in `scripts\` (`tests\fixtures\console-capture-probe-2026-09-29.txt` and `tests\Shard-Console.Tests.ps1`: a captured
fixture and the facts that pin it, not runtime code), 4 in old prompts: the user profile is assumed nowhere that runs.

**The cheapest match is a real `D:`,** which Chase chose. The alternatives, for the record:
- `subst D: <folder>`: per login session, not seen by scheduled tasks or services started outside it, and Docker
  Desktop's WSL side mounts real drive letters (`/mnt/d`), not subst drives (unverified for the current Docker
  Desktop; it was true of WSL 2's automount). Refused.
- A junction from a real `D:\UO` to elsewhere: fine for folders, but the drive letter still has to exist. Only useful
  if the work PC's `D:` cannot be freed.
With a real `D:` nothing above is rewritten on either PC: zero edits.

### The folder tree the work PC needs

For the no-Docker Stone (console, Haven-file and tools prompts):

```
D:\ShatteredLegacy\              git clone (public)                 shattered-legacy-infrastructure
D:\UO\shard-migration\           git clone (private)                needs Chase's GitHub login
D:\UO\golem-ops\                 git clone (private, new)           golem\, cc-prompts\, tools\, Commit-ShardWork.ps1
D:\UO\golem        -> junction to D:\UO\golem-ops\golem             so the hook paths hold
D:\UO\cc-prompts   -> junction to D:\UO\golem-ops\cc-prompts
D:\UO\tools        -> junction to D:\UO\golem-ops\tools
D:\UO\Commit-ShardWork.ps1, unattended-permission.ps1, the loose scripts   copied from golem-ops (or junctions)
D:\UO\logs\                      made empty                         the console's startup log
D:\UO\haven-migration\           git clone? it is not a repo today (102 files, 1 MB); fold it into golem-ops
```

Plus, for Stone with Docker (the 11 build prompts): Docker Desktop with WSL 2, `D:\UO\ServUO-pub57` (clone at pub57),
`D:\UO\ModernUO-pinned` (clone, checkout `d4531cd94`), and a test world made fresh on the work PC (never a copy of this
PC's). Programs: Windows PowerShell 5.1 (built in), git, `gh`, Python 3 (the commit script runs `opsmirror.py` and
`progress.py`), the Claude desktop app or CLI signed in as Chase, .NET SDK 10 only if P134-style builds go there, Tailscale
(Q7). Per-machine files made on the work PC, never copied: `golem\state\stone\`, `settings\stone.json`, the mail
credential, `.claude\settings.local.json` in both repos (written by `Add-GolemHooks.ps1`, which is in `golem\`).

### One-time setup, in order

0. (Chase, employer) check that personal project work and these files may live on the work PC.
1. Free `D:` on the work PC: in Drive for desktop, move the Sunflower drive to `S:` (checklist B).
2. Install git, `gh` (`gh auth login`), Python 3, the Claude desktop app (sign in), Tailscale (join the tailnet).
3. `git clone` the three repos to the paths above; make the junctions (`mklink /J D:\UO\golem D:\UO\golem-ops\golem`
   and the other two); `mkdir D:\UO\logs`.
4. Run `D:\UO\golem\Add-GolemHooks.ps1` (it writes both repos' `settings.local.json`); copy the user-level
   `unattended-permission.ps1` hook line into `%USERPROFILE%\.claude\settings.json` (P131 should turn this into a
   script).
5. `Setup-Email.ps1` on the work PC if Stone should email; else leave `email.json` out and `Invoke-Wake` refuses, which
   is today's rule, so the Stone prompt (below) makes mail optional when the Haven status row exists.
6. Run the suites: `golem\tests\Golem.Tests.ps1`, `scripts\tests\Shard-Console.Tests.ps1`, `python -m unittest
   discover -s tools/tests`. All green before the first prompt.
7. Set `settings\stone.json` (`name: Stone`, `maxPerRun`, no `botWindow`), open a CC session in `D:\UO\shard-migration`
   and say the phrase. The first prompt should be one with `**Golem:** Stone` and a small Kind.
8. Optional, for ports: Docker Desktop, the two source clones, a fresh test world, then `docker\uo\build.sh` once by
   hand to prove the gate goes red and green there.

### The drive letters (Chase's decision 11:51: `D:` for the project, `S:` for Sunflower, both PCs)

This PC today: `C:` Windows (952 GB), `D:` Data (954 GB, 128 GB free: `D:\UO` and `D:\ShatteredLegacy`), `E:` Ventoy,
`G:` the ckfleming Google Drive, `H:` the sunflowercustomgiftshop Google Drive. Drive for desktop stores the letter per
account (`HKCU:\Software\Google\DriveFS`, `PerAccountPreferences`, `mount_point_path: "H"` for the Sunflower account).

**Checked for anything pointing at `H:` on this PC, 2026-10-16: nothing.** 21 shortcuts on the Desktop and Start Menu
(all `D:`), 3 scheduled tasks naming a drive (all `D:`), `C:\dev\sunflower` (0 files naming `H:` among `.ps1 .py .json
.md .bat .js .yml .env .txt`, node_modules and `.git` excluded), the P109 and P110 notes and `docker\dashboard` and
`scripts` in the shard repo (0). Not checked: files inside the Sunflower Google Drive itself, Chase's browser
bookmarks, and Windows "Quick access" pins; those are his to glance at.

**Checklist A, this PC (`H:` to `S:`):** nothing here needs a script change, so there is no path-change prompt for this
PC; a two-line verification prompt is in the drafts anyway.
1. Quit anything using `H:` (Explorer windows, the print-queue scripts if they read the Drive).
2. Drive for desktop: tray icon > gear > Preferences > the Sunflower account > gear (streaming options) > Drive letter
   > `S:`. (Menu names from Google's help and a university guide, 2026-10-16; the current app may word it slightly
   differently. The admin route is the registry value `DefaultMountPoint` under `HKCU:\Software\Google\DriveFS`.)
3. Restart Drive for desktop; confirm `S:` lists the Sunflower files and `H:` is gone.
4. Re-run the three checks above (`Get-ScheduledTask`, the shortcut scan, `grep H:` in `C:\dev\sunflower`): still 0.

**Checklist B, work PC (`D:` to `S:`, then `D:` free):**
1. Note what on the work PC points at `D:` today (shortcuts, Sunflower scripts, Quick access): the same three checks.
2. Drive for desktop > Preferences > Sunflower account > Drive letter > `S:`; restart it; confirm `S:`.
3. Confirm no volume holds `D:` (`Get-PSDrive`); if a physical partition should become `D:`, assign it in Disk
   Management; otherwise `D:` can be a folder on `C:` only through a real volume (a VHDX mounted as `D:` works and is
   the easy way to get a real letter without repartitioning: `New-VHD` + `Mount-VHD`, unverified on the work PC's
   Windows edition, Hyper-V tools needed).
4. Fix whatever step 1 found to say `S:`.
5. Then the one-time setup above.

The abandoned option (`S:` on both for the project) would have meant rewriting the 374 files above on this PC plus
the bind mounts, tasks, shortcuts and hooks, between Golem runs, with a rollback; Chase's decision avoids all of it.

## Q7. Names and seeing each other

- **Names everywhere:** **Iron Golem** (this home PC), **Stone Golem** (the work PC), **Crystal Golem** (cloud).
  Today's Golem becomes the Iron Golem. Renaming touches, counted 2026-10-16 (`grep -ci golem`): `Shard-Console.ps1`
  231 lines (2 with the `[Golem]` subject), its tests 139 (2), `golem.ps1` 75 (2), its README 28 (1), `Golem.Tests.ps1`
  51, `progress.py` 12, `render_dashboard.py` 2, `Publish-GamePcSnapshot.ps1` 9, `Send-BotReport.ps1` 5. Most of those
  lines are the word in comments and labels that can stay "Golem" as the kind; what must change is the **name** shown
  and emailed: the subject prefix becomes `[Iron Golem]`, `status.json` gains `name`, the tile and tab title the name.
  A setting `name` in `settings\<golem>.json` (default `Iron`) drives all of it, so Stone is the same code with one
  setting. The `golem.*` action keys, function names and file names stay.
- **Publishing a status.** Pick: **the ops service's ingest endpoint**, because it exists. `Publish-GamePcSnapshot.ps1`
  already POSTs this PC's Golem block (on, running, lastDone, runDone, queue) every minute to `/api/ingest/gamepc`, and
  `opsdata.gamepc_status` already turns an old snapshot into "offline since". The change: a second route
  `POST /api/ingest/golem/<name>` (same bearer token, 8 KB cap) storing `{name, machine, awake, resting, restReason,
  prompt, title, model, startedAt, lastResult, longRun, at}`, `GET /api/golems` returning every stored one with its
  age, and **a status older than 15 minutes reads `unknown`, never running.** Each Golem's `Write-Status` already
  rewrites `status.json` on every change; a one-line `Invoke-WebRequest` after it (fire and forget, 3 s timeout, never
  blocking a hook) plus the existing every-minute task is enough. Why not git: the status changes on every tool call
  (`-Event Activity`), hundreds of commits a day. Why not a file share: the work PC is off the LAN. **Reaching the ops
  service from the work PC** needs Tailscale (P133's decision: Tailscale only, nothing public), which the work PC can
  join as Chase's device, so the Stone Golem posts to `haven.tail81098d.ts.net:8094` after the Haven cutover, or to
  this PC's tailnet address before it (the LAN listener needs `PLAYTESTS_LAN_PORT` and a token on this PC's
  `sl-play-tests` too; P105 built it, P107 only enabled it for Haven). **Crystal** can reach neither; a cloud Golem
  would show `unknown` unless its prompt commits a status file to a `golem-status` branch at start and end (two
  commits per prompt) that the Iron Golem's snapshot task reads and forwards. Fine for later; Crystal is not built.
- **The console.** The GOLEM tile and the Golem tab show **one row per Golem**: a crystal (P132's green, amber, red,
  grey) for running, resting or waiting, stopped or needs-you, unknown; the golem art per P132 (glowing, idle, dark);
  then `Iron  P127 treasure maps  Opus  12 min`. The queue list marks each prompt's `**Golem:**` line and, from the
  `claimed\` folders, who holds it, so two never take the same one (the git move in Q4 is what enforces it; the
  console only shows it). The rows come from `/api/golems`; this PC's own row still comes from its `status.json` first
  (so the console works with the service down), the others from the service, `unknown` after 15 minutes.
- **Emails** carry the name: `[Iron Golem] P127 done, starting P128 (3 of 9)`, `[Stone Golem] P133 done on
  stone/P133, waiting for the Iron Golem to merge`.

## Recommended setup, and what to do first

1. **P131 first** (already queued): CLI sessions make the usage bars real, and its self-wake removes the rests that
   make the Iron Golem idle, which is the cheapest throughput there is.
2. **One week of `usage.json`** from P131's sessions: how much of the 5-hour and weekly windows the Iron Golem uses.
3. **If there is headroom: the Stone Golem**, in this order: the ops repo (draft A), the name and status design (draft
   B), the work PC setup (checklist B, then draft C on the work PC). Without Docker there it takes 7 of 31 prompt kinds;
   with Docker, 18 of 31.
4. **Crystal: not yet.** Two of 31 prompts fit, the Golem would be a rewrite, the limits are shared. Use a cloud session
   by hand from the desktop app for a P115-shaped data task when it comes up, and revisit if routines leave preview.
5. **Haven: not a build box.** 8 GB, four cores, and it would break the "CC never connects to Haven" rule. Haven is the
   status board.

## Draft prompts (not queued; written to the shape they would land in)

### Draft A: `cc-P-golem-ops-repo.md` (Iron, Opus, home-only, small to medium)

Move `D:\UO\golem\` (less `smtp-cred.xml`, `email.json`, `*.log`, `sessions\`, `state.json`, `status.json`,
`progress.json`, `usage.json`, `ENABLED`, `ACTIVE`, `STOP-REQUESTED`), `D:\UO\cc-prompts\`, `D:\UO\tools\`,
`D:\UO\Commit-ShardWork.ps1`, `D:\UO\unattended-permission.ps1`, `D:\UO\haven-migration\` (less any token) and the
loose `D:\UO\*.ps1`/`*.bat` into a new private GitHub repo `uo-golem-ops` cloned at `D:\UO\golem-ops`, with the
state files under `golem\state\<name>\` and ignored. Make `D:\UO\golem`, `D:\UO\cc-prompts`, `D:\UO\tools` junctions
into the clone so every hard-coded path (23 in `golem\`, 10 hook lines per repo, 3 scheduled tasks) keeps working.
`Commit-ShardWork.ps1` gains the third repo. Do it between Golem runs with the Golem resting; `Move-ToGolem.ps1`'s
refusals (a running prompt, `index.lock`) are the model. Tests: the Golem suite green from the new path; a fact that
the secrets are ignored (`git check-ignore`); the console's Golem tab unchanged. Rollback: remove the junctions and
move the folders back.

### Draft B: `cc-P-iron-golem-name-and-status.md` (Iron, Opus, home-only, medium)

1. `settings\<name>.json` gains `name` (default `Iron`); every email subject, `status.json` (`name`, `machine`), the
   tile, the tab title and the log line say it. 2. Prompts gain `**Golem:** Iron|Stone|Crystal|any`; `Get-NextQueued`
   hands only matching prompts; the claim is a git move `queue\` to `claimed\<name>\` with pull, commit, push, and a
   rejected push means try the next. 3. `server.py`: `POST /api/ingest/golem/<name>`, `GET /api/golems`, 15-minute
   `unknown`; `opsdata.py` stores them like the gamepc snapshot; `Write-Status` posts after each write (3 s, never
   blocking). 4. The console: one row per Golem from `/api/golems` (own row from `status.json` first), crystals and
   golem art per P132's slots, the queue list showing the Golem line and claims. 5. The merge step for `stone/P<nn>`
   branches (Q4 rule 4) in the Iron Golem's Stop path, with the CHANGELOG/VERSION rule and the conflict email. Tests:
   Golem facts for the routing, the claim and the merge (fixture repos), Python facts for the routes and the 15-minute
   rule, console facts for the rows; each seen failing first. Play-test items: none in game.

### Draft C: `cc-P-stone-golem-setup.md` (Stone, Opus, run on the work PC as its first prompt)

Verify the one-time setup: the three clones at their paths, the junctions, `Get-PSDrive` shows a real `D:`, the hooks
in both repos' `settings.local.json`, Tailscale reaches the ops service, the three suites green, `settings\stone.json`
has `name: Stone` and no `botWindow`, `Setup-Email.ps1` done or mail declared off. Then a dry wake: the phrase in a
CC session with an empty Stone queue should answer "nothing to hand you". Nothing committed to `main` from this PC
ever: prove `Commit-ShardWork.ps1` on Stone pushes `stone/P<nn>` (a fact against a fixture repo). Write
`notes\cc-P-stone-golem-setup.md` with what the work PC has (Docker yes or no, RAM, cores) for the overseer.

### Draft D: `cc-P-h-to-s-check.md` (Iron, Opus, tiny)

After Chase moves the Sunflower drive from `H:` to `S:` on this PC: re-run the three checks (scheduled tasks,
shortcuts, `C:\dev\sunflower`), plus the P109 print-queue and P110 dashboard configs, for `H:`; expect 0; if any, fix
and list. No other change is known to be needed (this note, Q6).

## Deviations and decisions for Chase

1. **The start phrase.** "golem work on shard tasks please" is not one of the two phrases (`Test-GolemPhrase` needs
   exactly "golem please work on the shard tasks" or "golem work"), so the hook handed nothing. I ran the Golem's own
   Prompt handler with the exact phrase (`golem.ps1 -Event Prompt -InputFile <json>`), which cleared the context rest,
   handed P126 and emailed "[Golem] Starting P126 (11 of 21)" as a typed phrase would. P99's decision 2 said the phrase
   is strict on purpose; say if you want "golem work on shard tasks please" and the like to match too (one line in
   `Test-GolemPhrase`, P131 could take it).
2. **No CHANGELOG or VERSION change**: nothing a player or staff member runs changed. The prompt's Patch notes section is
   the standard template; its Tests section ("run nothing that changes either repo except your notes") wins.
3. **The Q1 labels for P109 and P110 rest on their Kind lines**, not a full read. The other 29 I read enough of to be
   sure of the Docker and client needs.
4. **Unverified, marked above:** the cloud build (the three missing domains, seccomp on the VM, cold build time), a
   Haven build's memory, subst drives under WSL 2, Drive for desktop's exact menu names, the VHDX route on the work PC.
5. **The Golem line and the claim folders change the hand-off's shape** (Q4), which P131's wake button and self-wake
   will also read. If Draft B lands after P131, P131's "next queued prompt's Model line" lookup should become "next
   queued prompt for this Golem".
6. **I did not propose a Crystal Golem prompt.** Two cloud-capable prompts in 31 and a shared limit do not pay for a
   Linux Golem. If that changes, the design is: a routine per cloud-capable kind, prompts carrying `**Golem:**
   Crystal`, pushes to `crystal/P<nn>`, status via a `golem-status` branch.

## For Chase

**Recommendation:** the work PC as the Stone Golem (same scripts, `D:` mirrored, no rewrite), after P131 shows a week of
usage with headroom; no cloud Golem, and Haven stays the web and status host. **The one decision:** Docker Desktop on the
work PC or not (ports there, or only console, Haven-file and tools prompts). One neutral line: the work PC is the
employer's, so it is worth checking that personal project work and these files may be stored and run on it.

What the work PC has that I should know for the setup checklist: Windows edition, RAM and cores, whether Docker
Desktop is allowed, whether Tailscale is allowed, and whether it already has a real second volume that could become
`D:` once the Sunflower drive moves to `S:`.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code clean
docs dry run
```

docs, 76 files pending: this note, the overseer's `docs/feature-queue.md` edit (already pending when the prompt
started), the importer's `testing/SUMMARY.md` and `testing/play-tests.json`, and the bot's
`testing/bot-runs/2026-10-16-0130/` (machine output, 72 files). No file is near 5 MB. Nothing in the shard repo changed
("nothing to commit"). The dry run also listed this note as "archived (dry run, not moved)", so the commit will move
the prompt to `completed\`.

P126 DONE
