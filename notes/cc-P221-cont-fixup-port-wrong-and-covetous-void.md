# cc-P221: fix-up for cc-P194 (Wrong revamped and Covetous Void Spawn), whose branch did not merge into main

2026-10-20, the Bronze Golem (Fable), on branch `golem/Bronze/P221` of both repos. Prompt: `cc-prompts\claimed\Bronze\
cc-P221-cont-fixup-port-wrong-and-covetous-void.md`. Not committed: the Golem commits after DONE. P194's own notes are
`notes\cc-P194-port-wrong-and-covetous-void.md` (carried over unchanged by this merge).

## Headlines

1. **P194's work is on `golem/Bronze/P221` together with everything main gained since, in both repos, with every
   conflict resolved.** Main had moved 44 commits past P194's base in the docs repo (and the same prompts in the code
   repo); P194 is one commit per repo (`011f80c` code, `f986159` docs).
2. **How, and why not the prompt's literal steps.** The prompt says check out `golem/Bronze/P194` and merge main into
   it. The hand-off forbids switching branches or merging and says the Golem commits `golem/Bronze/P221`, which was
   cut from main (`77f59fb` code, `1c29697` docs; P194 was not an ancestor of either). So I did the equivalent on P221:
   `git cherry-pick --no-commit golem/Bronze/P194` in each repo, resolved the conflicts, then `git cherry-pick --quit`
   (the pattern P194's own second sitting used after its reset). The tree is main plus P194's content; the integrator
   merges P221 into main as a plain fast-forward merge. The P194 branch itself is untouched.
3. **Conflicts, five files, all resolved with both sides kept** (section 2): code `CHANGELOG.md` (P194's four Added
   lines and one Staff line moved under the newest heading, `2026.10.20.15`, beside P235's Staff line; P194's own
   `2026.10.20.4` heading dropped) and `VERSION` (the higher, `2026.10.20.15`); docs `testing\bot-triage.md` (P193's
   and P194's sections both kept, in that order), `testing\playtest-steps.json` (P193-1 to P193-7 and P194-1 to P194-7
   all kept under `items`; the file parses and has both sets) and `tools\expansion-coverage.json` (generated;
   regenerated). The three files the integrator named (`README.md`, `dashboard.html`, `tools\progress.json`) auto-merged
   here and were then regenerated anyway, since they are `progress.py` output.
4. **Build:** **green on the merged tree.** The full gate (`docker\uo\build.sh` with the P221 tag) ran all three steps: patches applied, **1,638 tests, 1,634 passed, 4 skipped (pinned's), 0 failed**, image `sl-modernuo:cc-P221` built; `EXIT=0`, 2026-10-21 01:23:57 to 01:26:08 UTC (2 minutes 11 seconds). Nothing was red, so nothing was fixed.
5. **Nothing else changed.** No code was edited beyond the conflict resolution; P194's 60 new files, its patch and its
   two test files came across as they were; main's `docker\uo\apply-patches.sh` and `PointsSystem.cs` auto-merged
   cleanly (P194's one `apply_patch` line and its `VoidPool` enum value, checked by eye).

## 1. What changed on `golem/Bronze/P221`

**Code (`ShatteredLegacy`), 63 paths staged:** P194's 60 new files under `server\customizations\Services\Revamped
Dungeons\{WrongDungeon, Covetous Void Spawn}`, `server\customizations\Services\PointsSystems\VoidPool.cs`, `Gumps\BaseRewardGump.cs`,
`Misc\WearableExtensions.cs`, `Services\CommunityCollections\CollectionItem.cs`, `server\patches\PlayerMobile-void-pool-context.patch`, the two test files
(`WrongRevampedVerification.cs`, `CovetousVoidSpawnVerification.cs`); modified: `docker\uo\apply-patches.sh` (one
`apply_patch` block, auto-merged), `server\customizations\Services\PointsSystems\PointsSystem.cs` (`VoidPool` enum
value, auto-merged), `CHANGELOG.md` and `VERSION` (resolved, section 2). `git diff --stat` of the P194 commit was
64 files, 10,145 insertions; all of it is here.

**Docs (`shard-migration`), 7 paths:** added `notes\cc-P194-port-wrong-and-covetous-void.md`; modified
`testing\bot-triage.md` and `testing\playtest-steps.json` (resolved, section 2); regenerated `README.md`,
`dashboard.html`, `tools\progress.json`, `tools\expansion-coverage.json` with
`SL_SHARD=D:/UO/golems/Bronze/ShatteredLegacy python tools/progress.py` against the merged code tree.

One thing seen and left: the README's "Shard status" sentence still says "main is 2026.10.20.4". That text is the
hand-written judgment in `tools\progress-state.json`, written by cc-P220 on main (`a0f5bc1`), not P194's or this
merge's; it is Crystal's to refresh.

## 2. The conflicts and how each was resolved

| Repo | File | Conflict | Resolution |
|---|---|---|---|
| code | `CHANGELOG.md` | P194 added a `## 2026.10.20.4` section (4 Added, 1 Staff); main's top is `## 2026.10.20.15` (P235's Staff line) over `.14` .. `.4` | both sets under the newer heading: `## 2026.10.20.15` now has `### Added` (P194's four lines) and `### Staff` (P235's line, then P194's line); the `.4` heading is gone; nothing below changed |
| code | `VERSION` | `2026.10.20.15` vs `2026.10.20.4` | the higher, `2026.10.20.15` |
| docs | `testing\bot-triage.md` | P193's section (main) and P194's section appended at the same place | both, P193 then P194 |
| docs | `testing\playtest-steps.json` | P193-1..7 (main) and P194-1..7 appended at the same place inside `items` | both, with the closing brace and comma between; parsed with `json.load`: 14 of the 14 keys present |
| docs | `tools\expansion-coverage.json` | two generated totals | took P194's side, then regenerated the file with `progress.py` |

Auto-merged by git and checked: `docker\uo\apply-patches.sh` (P194's `apply_patch "$PATCHES/PlayerMobile-void-pool-
context.patch"` block after `BaseWeapon-trained-weapon-ability.patch`), `PointsSystem.cs` (`CleanUpBritannia, VoidPool`),
docs `README.md`, `dashboard.html`, `tools\progress.json` (then regenerated).

## 3. Tests and build

P194 ran the full gate (`docker\uo\build.sh`), a red proof and two headless boots (its notes, section 3 and 7). This
fix-up changes no code, so the gate alone is the check: `docker\uo\build.sh -t sl-modernuo:cc-P221`, under the
docker-build lock, started detached (PowerShell `Start-Process` of `run-cycle-p221.sh` in the session scratchpad, log
on disk) so a harness reap could not take it. Memory before the build: Windows 9,044 MB free of 32,464; the Docker VM
7,367 MB free with 7,299 MB page cache (`free -m` in an alpine container), so no cache drop was needed.

**Result:** `START 2026-10-21T01:23:57Z` .. `END 2026-10-21T01:26:08Z`, `EXIT=0`. Log lines: `Total tests: 1638`,
`[tests] 1634 test(s) passed.`, `Built sl-modernuo:cc-P221 with patches applied and 1634 shard test(s) passing.`
Counted from the log: 1,634 `Passed`, 4 `Skipped`, 0 `Failed`. P194's second sitting saw 1,571 tests on the gate; main
has grown since, and every newer fact is green beside P194's ten. The log is `build-P221.log` in the session
scratchpad (`C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-golems-Bronze-shard-migration\
a6e83d9a-e72e-494b-9a90-9c51faf4b111\scratchpad\build-P221.log`).

**Noise, not failures:** the test log carries thirteen `[ERR] Item Server.Items.Corpse ... was changed to amount of 0,
but must be at least 1` lines with `System.Exception: Item.Amount <= 0 error` under them, logged by pinned's `Item`
while a test tears corpses down; no test around them failed and the gate counted them as nothing. Whether the same
lines appear in other prompts' logs was not checked.

**The harness and the build:** my wait loop (a background `until grep EXIT=` shell) was stopped by Claude Code for
low system memory while the session was idle (free memory had fallen from 9,044 MB to 2,265 MB; other Golems were
building). The build itself was a detached process and had already finished green; the log on disk was read after
the fact, as the memory note says to do. Nothing was restarted. The docker-build lock was released at once.

**P194's other checks** (the red proof of its ten facts and the two headless boots of its image on a scratch world)
were not repeated: no code changed in this fix-up, and the image here is the same tree plus main's later commits,
each of which the integrator built green before merging.

## 4. Commit preflight

Run 2026-10-20 (local) with `Commit-ShardWork.ps1 -DryRun`. The script reads the three main checkouts (code, docs,
scripts), not this Golem's worktrees, so "code clean" is the main checkout; this branch's staged changes (63 paths in
the code repo, 7 in the docs repo plus this note) are committed by the Golem after P221 DONE. The three docs files it
lists are the play-test importer's and the overnight bot's output, committed with each prompt.

| Repo | Result |
|---|---|
| code | clean |
| docs | dry run (3 pending: `testing/SUMMARY.md`, `testing/bot-runs/2026-10-19-0130/transcripts/P140-1-run1.txt`, `testing/play-tests.json`) |
| scripts | clean |

Prompts with a finished note: none for P221 (it lists cc-P180, cc-P181 and cc-P185 as not ending in DONE or STOPPED,
which is not this task).

**For the integrator:** merge `golem/Bronze/P221` into main in both repos; it already contains main as of `77f59fb`
(code) and `1c29697` (docs), so the merge is trivial unless main moved again. `golem/Bronze/P194` can then be retired;
nothing on it is missing here.

P221 DONE
