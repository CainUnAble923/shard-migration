# cc-P197: the Underworld (Stygian Abyss) and the mini champions (paused)

Written 2026-10-21 by the Gold Golem (Claude Opus 5.5), on branch golem/Gold/P197 of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Gold\cc-P197-port-underworld-mini-champions.md`. **Paused at Chase's request** shortly after
starting; the rest is the continuation prompt `D:\UO\cc-prompts\queue\cc-P352-cont-underworld-mini-champions.md`.
Nothing was committed, nothing touched the live shard or the test shard, nothing was placed in any world. ASCII only.

## Headlines

1. **The port was already in the tree, untested.** The branch head is `fb2de4a` ("WIP: golem/Gold/P197 unfinished
   work, kept when golem/Gold/P198 was claimed"): an earlier P197 session ported all 28 ServUO files of the row
   (`Services/Underworld/`, `Services/MiniChampionSystem/`, 5,689 lines in 30 files) and left no notes and no tests.
2. **It did not compile; now it does, and the full suite is green.** Three fixes (section 1). `docker/uo/build.sh
   --tests-only` (tag `sl-modernuo:cc-P197`, builder `sl-uo-builder:cc-P197`): **1,865 tests, 1,861 passed, 4 skipped
   (pre-existing), 0 failed.** No new tests yet, so nothing in the port is proven beyond compiling.
3. **Port row: 3 of 27 before, 27 of 27 after by the stem proxy** (`tools/progress.py`; the port list 736 to 760 of
   983, 5 of 16 systems in). This counts files present, not files verified: treat the row as "in, unverified" until
   P352 finishes.
4. **Nothing reviewed, run or seen yet.** No client check, no race-gate check, no League hook, no Fountain of Fortune
   reconciliation, no test-shard boot. All of it is in the Continuation section and P352.

## 1. What changed (this session)

All in `D:\ShatteredLegacy\server\customizations\`:

| File | Change | Why |
|---|---|---|
| `Services/MiniChampionSystem/MiniChampionSpawn.cs:68` (and its 10 uses) | the saved list `_spawn` renamed `_spawnList` | the serialization generator emits a `ClearSpawn()` helper for a collection field `_spawn`, which clashed with ServUO's own `ClearSpawn()` (CS0111, the WIP's one compile error). The rename keeps ServUO's method name; the save shape (field 6, a list of `MiniChampSpawnInfo`) is unchanged, and no world has saved one |
| `Services/Underworld/ExperimentalRoom/Region.cs:40-64` | static `Register()` / `Unregister()` renamed `EnsureRegistered()` / `RemoveRegistration()` | they hid `Region.Register()` / `Unregister()`, so `Instance.Register()` inside them did not compile (CS0176) |
| `Services/Underworld/Maze of Death/Region.cs:198-227` | the same rename | the same error |

What the WIP holds (for the reviewer): `Services/Underworld/` (Generate.cs 360 lines; ExperimentalRoom 7 files;
Maze of Death 7; Navreys Lair 2; PuzzleRoom 8), `Services/MiniChampionSystem/` (3 files),
`Items/Internal/InvisibleTile.cs` (68), and `Mobiles/Bosses/Navery/NavreyNightEyes.cs`: an unsaved `Controller` link
to the lair and the `OnNavreyKilled` call ServUO makes (closes D-83; her save shape is unchanged).

## 2. Tests

None written this session. The suite is green as it stood (1,861 passed, 4 skipped, through `build.sh --tests-only`
under the docker-build lock); P352 owns the new facts, each to be seen failing first.

## Deviations and decisions for Chase

None new from this session (the three fixes change no behaviour). Decisions waiting for P352 to put to you, from
reading the WIP's headers: the Experimental Room region, which ServUO declares but never registers, is registered
here (`ExperimentalRoom/Region.cs` header); and `[GenMiniChamp` places all fourteen mini champions active, as ServUO's
does.

## For Chase

Nothing to see yet: the port is not verified. Do not run `[GenMiniChamp` or the Underworld generator on any shard
until P352 has reviewed them. Patch notes are left for P352 too: an Added line now would describe content nobody has
checked.

## Continuation

**Done:** the WIP compiles; the suite is green; the port row counted.

**Left** (the full list is the continuation prompt, P352, in the queue):
1. Review the ~5,700 WIP lines against ServUO file by file and fix what is wrong (Generate.cs and its re-run and dry
   run, the puzzle room, the Maze of Death, the Experimental Room, Navrey's lair, the mini champions and whether
   every creature type their tables name exists here).
2. Open to every race: remove any race or gargoyle-only gate, each a recorded deviation.
3. League culling hooks (F-24) for mini champion kills.
4. The Fountain of Fortune: ServUO's Underworld `Generate.cs` places one; our `ClusterFFountainOfFortuneSeeder`
   already does (Q-021). Only one may.
5. The client check against 7.0.117.0.
6. Tests (each seen failing first), the full suite green, a clean test-shard boot.
7. Notes, play tests, patch notes, commit preflight.

**Mid-flight:** nothing. The three fixes are complete and built; no lock is held; no container or world was touched.
Scratch (build logs) is in the session scratchpad, outside both repos.

**Numbering:** P352, not P287. P287 is the next number above queue, claimed and completed, but
`_superseded/fixup-loop-20261020/` already holds a cc-P287 and a cc-P349, so the next number free everywhere is 352.

## Repo size rule

No file added this session; nothing over 5 MB.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, first run, no BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

Code: the three fixed files. Docs: this file and the four files `tools/progress.py` rewrote when I counted the row
(`README.md`, `dashboard.html`, `tools/progress.json`, `tools/expansion-coverage.json`). The continuation prompt is in
`D:\UO\cc-prompts\queue\`, outside both repos. P180, P181 and P185 are listed as unfinished; they are other Golems'.

P197 PAUSED
