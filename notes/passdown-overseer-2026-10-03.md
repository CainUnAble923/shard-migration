# Overseer pass-down, 2026-10-03 (11:35)

Supersedes `passdown-overseer-2026-10-02.md` for queue state and numbers (its "Lessons" still hold; read them).
The "how this chat works" section of `passdown-overseer-2026-10-01.md` still holds.

## Role, in one paragraph

Track the CC prompt queue (one builder at a time in `D:\ShatteredLegacy`; notes-only prompts run alongside), read CC
results from `D:\UO\shard-migration\notes\` when Chase says a prompt is done, write or number prompts in
`D:\UO\cc-prompts\`, record Chase's decisions in notes, keep `docs\bug-list.md` and `docs\fidelity-principle.md`
current, give Chase short in-game checklists. Never commit (Chase runs `D:\UO\Commit-ShardWork.ps1`). Git only with
`--no-optional-locks`. ASCII only, no em dashes, American spelling. Verify in code before asserting; cite file:line.
Engine authority: `D:\UO\ModernUO-pinned` at upstream `d4531cd94`. **Ignore anything "live" until the fresh-world
wipe (Chase 2026-10-03); only the TEST shard is in use.** Other chats (features, companions, dungeon) write prompts
too: they often leave them unnumbered (`cc-P-*.md`); number them, rename, fill the number into the file's title,
notes path and build tag, and move the draft to `cc-prompts\_renders\`.

## Numbers (re-derive before trusting)

- Bugs: **next free D61** (D59 HoH +5 from pack, D60 familiarity panel reach, 13:49). D50-D58 logged 2026-10-02/03; D51-D54 fixed in P42 and passed in game; D55-D58 fixed in
  P46 (in-game check pending).
- Deviations: **next free D-113** (D-107 to D-112 from P42). P46 adds text to update (D-109 teaching toggle, Seal
  numbers, Self Repair floor): read P46's notes and register.
- Features: **features chat owns `docs\feature-queue.md`**; next free there was F-33 (check the file).
- Prompts: **next free P51.** Re-check `cc-prompts\` and `completed\` right before saving.

## State of the shards

- TEST: new engine `d4531cd94` since the P43 cutover (2026-10-02 18:18). Running image `a4525e03b317` (P42).
  P46's image `sl-modernuo:cc-p46` (`8d7505c739f6`) is built and committed (`1f2b899`) but **not yet on the test
  shard**: deploy with `docker tag sl-modernuo:cc-p46 sl-modernuo:latest` then
  `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild` (stop first with `-Down`; call by full path).
- Stops now wait 60 s (D50, P43). The console "Rebuild" can still hit D56-type flakes; P46 fixed the known one.

## Queue (2026-10-03 11:35)

| Prompt | Kind | State |
|---|---|---|
| P44 one-step install (wait for EA patch) | builder, player package | **done 13:12**, uncommitted; notes read; prompt moved to `completed\` |
| P45 companion probes | builder (worktree) | after P44 |
| P48 League batch 1 (ladder, signposts) | builder | after P46 (done); account data bumps from whatever version P46 left |
| P50 chest mimic monster | Part A notes; Part B builder | Part B after P44 (player package). Art placed 2026-10-03 at `D:\UO\third-party\animated-mimic\` with `SOURCE.txt` |
| P35 clean-machine test | builder | **next builder** (P44 says so: it is the real-EA proof). B4 step 2 now asks P44's open questions |
| P36 dungeon build 1 | builder | after P44; map edits are patches per the client policy. Step 5 updated for P44 (older client now waits) |
| P34 winter decor | builder | never beside P48 (both touch the registrar office seeder) |
| P47 League research | notes | done (`notes\cc-P47-league-research.md`) |
| P49 dungeon chests and mimic research | notes | may run any time |

## Owed to Chase

1. **P46 in-game checklist** (end of `notes\cc-P46-smith-orders-2.md`) once its image is on the test shard:
   Celestial deed refuses iron; teaching toggle (choice gump and guild book, relog keeps it); Self Repair floor;
   commission rewards x3; runic prices; Hephaestus familiarity on default iron; Wisp Orb pet fight (no master swing,
   no karma loss on death); hammer regen 10/5 min with a "next use" timer.
2. Register P46 deviations; mark D55-D58 passed after the checklist.
3. Old items still open: F-12 numbers (reserve cap, step size above 100, League metal ranks may now be settled by
   P47/P48), P33 test list, P23/P27 old client checks.

## Results files from today

`notes\p39-step7-checks-2026-10-03.md` (new-engine cutover checks), `notes\p42-checks-2026-10-03.md` (P42 checks),
`notes\bod-choice-decision-2026-10-03.md` (all Smith BOD decisions).

## Lessons added 2026-10-03

- Before telling Chase what a CC result needs, read the CC notes' "For Chase" and checklist sections; CC chips
  ("suggested task") can duplicate a queued prompt: tell Chase to close them.
- `Start-TestShard.ps1 -Down` leaves PowerShell in the repo root, so call the script by full path afterwards.
- A fact that passes in CC's build can fail in the console's rebuild (order-dependent statics): deploy CC's tested
  image with `docker tag` + `-SkipBuild` instead of rebuilding.

## Update 13:12 (P44 done)

- P44 notes: `notes\cc-P44-wait-for-ea-patch.md`. All probes green, 4 watched red first. Changed
  `Setup.ps1`, `README.txt`, `Build-PlayerPackage.ps1` (new gate 4 check). Nothing proven against EA's real
  patcher (UAC, UIPI close, window behavior): P35 is the proof. Do not publish until P35 passes.
- Overseer edits: P35 B4 step 2 asks UAC count, window close, installer auto-start, copy EA's log; "2.5 GB" fixed.
  P36 step 5 points at P44 probe 6. P44 prompt moved to `completed\`.
- Scratch `D:\UO\cc-p44-work\` (about 1.5 GB) safe to delete.

## Update 19:15 (P35 done, commit blocked)

- P35 finished (`notes\cc-P35-clean-machine-test.md`). Commit refused `player-package/vendor/vc-runtime/vcruntime140.dll`
  (`Commit-ShardWork.ps1` blocks `.dll`; both repos public). Overseer fix: `.gitignore` ignores
  `player-package/vendor/vc-runtime/*.dll` (kept on the build PC; SOURCE.txt tracked; build checks hash and signature),
  and `Commit-ShardWork.ps1` now uses `status --porcelain --untracked-files=all`, because it expanded new folders with
  Get-ChildItem and swept in ignored files. Backup: `D:\UO\Commit-ShardWork.ps1.bak-2026-10-03`.
- Lesson: a CC prompt that vendors a binary must say "gitignored, build-PC only" up front.
