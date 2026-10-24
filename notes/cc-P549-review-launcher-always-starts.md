# P549: review of the launcher always starting the game

Reviewed 2026-10-24 against code HEAD `82ba93f`. P411's code commit `bd6118b` is an ancestor of local `main`, merged by `0de0d9e`. The reviewed launcher files match `main`. P543 restored the P411 notes and review without changing code.

Read both repositories' AGENTS.md, the direction and task documents, the P411 implementation notes and Codex review, and both P543 notes. Reviewed the launcher, updater, override builder, map applier, settings, shortcuts, README, and related tests under `player-package/`.

The findings below are additional to the P411 review. Its synchronous freshness-check hang, missing active-step trace records, swap-backup recovery, and second timeout during updater handoff are not repeated here. All findings concern our launcher code.

## Findings

### 1. bug: a freshness check can delete the last-good override list

`player-package/payload/app/Build-UoOverrides.ps1:880`, `:904`, `:914`, `:923`.

A part that throws during `-CheckOnly` is omitted without being marked stale. If nothing else is stale, execution reaches the normal list-writing path, which deletes the existing list when no parts remain or replaces it with a reduced list, then reports `Fresh=True`. `Overrides-Launch.ps1:118` accepts that result and skips rebuilding, so a temporary file lock can remove working art from this launch.

Evidence: built a valid synthetic art set, opened its `stamp.txt` with exclusive sharing, and called the unchanged builder with `-CheckOnly`. The list existed before the call; afterward it was deleted, `Fresh=True`, and `List` was empty.

Suggested fix: return from every check-only path before any write or deletion, and represent a failed check separately from a successful freshness result while preserving the previous list. Add a regression that locks a stamp and checks the list's hash and existence afterward.

### 2. risk: two Play calls can start builders in the same staging directory

`player-package/payload/app/Overrides-Launch.ps1:113`, `:126`, `:136`, `:137`.

There is no lock around discovering a builder, clearing staging, starting the child, and publishing its PID. A second Play call between child startup and PID publication sees no builder, deletes the first child's staging directory, and starts another writer there; only the last PID written is tracked. A ready marker can then belong to one writer while another is still modifying the same set, undermining the complete-set guarantee.

Evidence: a scratch wrapper around `Start-Process` scheduled a second unchanged `Invoke-UoOverrides` call in exactly that publication gap. It produced two live builder children and one PID entry. This confirms the race window; an actual half-built set being consumed by TazUO was not reproduced.

Suggested fix: use an install-specific interprocess lock around staging ownership, PID publication, and promotion, with each builder owning a separate staging generation. Add a concurrent-launch regression that checks there is only one owner and no promotion while a writer remains active.

### 3. bug: swap retries run outside the configured time limit

`player-package/payload/app/Overrides-Launch.ps1:69`, `:110`, `:123`, `:165`.

The initial promotion runs before the stopwatch starts, and promotion after a successful build runs after the timed wait. Each rename retries for 4.5 seconds, with more retries possible for promotion and rollback, so an art preparation call can exceed its configured limit while showing no rebuild progress bar during those retries. This is a separate path from the earlier review's blocking freshness check.

Evidence: prepared a ready staged set and made only its promotion rename throw, simulating a held directory. `Invoke-UoOverrides -LimitSeconds 1` returned after 4.82 seconds even though the current set was fresh and no rebuild was needed.

Suggested fix: share one deadline across promotion, preparation, and rollback attempts, preserving the current set when the remaining budget is exhausted. Test a ready staged set with a locked promotion destination and a short limit.

### 4. risk: map parsing and animation hashing have no progress step

`player-package/payload/app/Apply-MapOps.ps1:130`, `:162`, `:174`; `player-package/payload/app/Build-UoOverrides.ps1:425`, `:434`.

The map patch is read, parsed, and hashed before `map.copy` starts; animation files are hashed before `equip` starts. If those operations are slow in the rebuild child, the parent keeps redrawing the previous step, such as `art.stamp`, instead of naming the work that is taking time, and their time is missing from the individual step timings. Adding a trace line to the existing `Start-Step` calls alone would not cover these operations.

Evidence: an instrumented call with a synthetic map patch reached base-map validation after parsing without calling `Start-Step` once. The animation hash ordering was verified in source; slow hashing and a slow real map parse were not reproduced.

Suggested fix: start named progress and timing steps before reading and hashing these inputs, with counts for the map parser. Extend progress coverage beyond the existing forced `art.targets` delay.

### 5. risk: the timeout tests do not start Play or a game stub

`player-package/tests/Launch-Overrides.Tests.ps1:70`, `:117`, `:142`, `:230`; `player-package/tests/Launch-Settings.Tests.ps1:430`.

The facts named as starting the game after a timeout call only `Invoke-UoOverrides` and inspect its return value. The updater fact explicitly disables Play with `SL_UPDATE_NO_PLAY`, while the launch-settings sandboxes omit `Overrides-Launch.ps1`, so those end-to-end launches take Play's exception fallback instead of exercising preparation. Passing these suites does not prove that a timed-out builder lets the real Play flow reach TazUO with the previous list.

Suggested fix: add a loopback-only Play sandbox with the real override helper, a forced slow builder, and a game stub that records its startup time and override argument. Cover both an existing good set and a first install, including the updater-to-Play handoff.

## Checks and limits

- Ran `player-package/tests/Launch-Overrides.Tests.ps1` with Windows PowerShell `5.1.26100.9711`: all eight facts passed. The scratch probes above used that same PowerShell version and synthetic files, without modifying repository code or adding tests.
- No additional indefinite Play hang was confirmed beyond the previously reviewed freshness-check path. Swap retries above are a confirmed additional delay outside the limit.
- Found no remaining launcher route to the retired live shard: `Launch-Settings.ps1:38` and `:39` select port 2594 for LAN and public targets, settings force the target port and set `ignore_relay_ip=True`, and the reviewed shortcuts all call Play. This is source verification, not a live connection check.
- Did not run the launch-settings, art, or cliloc end-to-end suites because their Play sandboxes connect to the shard and can run script-update requests. Did not connect to Haven, launch a real game, deploy, build a package, or change code. The work PC's actual hang and published package remain unverified.
- Ran `tools/progress.py --dry-run` with the two work-copy paths: exit 0. Despite its documented dry-run behavior, it rewrote `tools/progress.json`; restored that file byte for byte from HEAD after confirming the work copy was clean before the run. No generated-file change remains.
- Execution policy rejected cleanup of the temporary probe folder, giving only "blocked by policy" as its reason. Small synthetic fixtures and probe scripts remain at `C:\Users\ckfle\AppData\Local\Temp\P549-review-c6279019`; both race-probe children were waited for before the probe exited.

P549 DONE
