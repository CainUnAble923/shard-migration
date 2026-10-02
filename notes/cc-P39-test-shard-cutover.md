# cc-P39: ModernUO upgrade, part 3 of 3: test shard cutover

2026-10-02. Brief: `D:\UO\cc-prompts\cc-P39-test-shard-cutover.md`. Checklist: `notes\cc-P38-engine-upgrade.md`
section 11. TEST shard only. Live (`sl-modernuo`, image `uo-modernuo` `bc04a35bf344`, started 11:57:46 UTC) was not
stopped, restarted, recreated or tagged for; it was `Up` at the start and at the end. No commit, no build, nothing
deleted. Git used only with `--no-optional-locks`.

## Headlines

1. **NOT cut over. I stopped between step 4 and step 5, as the brief requires**, because step 4 did not behave as
   section 11 says. "SaveOnShutdown saves on stop" did not happen: `docker compose ... stop` SIGKILLed the shard
   about 1.6 s after SIGTERM (exit **137**), partway through the shutdown save ("Writing world save snapshot", no
   "done"). The cause is **`Config.StopTimeout = 1`** on the test container, **and on the live container too**
   (section 3). The new engine was **never booted**; the test world is still idx v3 and can still go back to `7c9215d97`.
2. **The purge itself is done and verified, and the world on disk is the right one.** Dry run 108 (107 mobiles +
   1 item, 27 spawners), "TOTAL: deleted 108, held 27 spawner(s) for 30 min", explicit `save` done 17:07:32, then
   "would delete 0". The killed shutdown save was never published, so `Saves` is the 17:07:32 post-purge save, idx
   **03**. Stopped at 17:08:00, 39 s after the purge (hold runs to 17:37:21).
3. **Both rollback copies exist and are hash-checked** (section 2): before-purge = the 17:00:01 save, after-purge =
   the 17:07:32 save.
4. **Image behind `sl-modernuo:latest` now: `0e65420330ca`** (= `cc-p37` = `pre-bump-purge-7c9215d97`, pinned
   engine with P33, P37 and the purge command). It was `246b0d5813e5` at the start. `cc-p38` (`45b7523ae54b`) is
   **not** tagged `latest`. The test container is stopped (`Exited (137)`).
5. **World counts** on the purge image at boot (17:05:55): **206,297 items, 35,181 mobiles**. After the purge:
   35,181 - 107 = 35,074 mobiles expected (not re-read: the shard was not booted again).
6. **What I need from Chase or the overseer:** decide the stop timeout (section 3), then resume at step 5 (section 5).
   Step 5's check is already known to pass (read-only, section 4).

## 1. Starting state (17:04)

| Thing | State |
|---|---|
| `sl-modernuo:latest` | `246b0d5813e5` (= `pre-bump-7c9215d97`) |
| `sl-modernuo-test` | image `246b0d5813e5`, started 20:03:14 UTC, Up |
| `sl-modernuo` (live) | image `bc04a35bf344` (`uo-modernuo`), started 11:57:46 UTC, Up |
| Test world | `D:\ShatteredLegacy\server\lib\uo\modernuo-test`, 629,263,402 bytes, 228 files, Mobiles.idx `03 00 00 00`, `SerializedTypes.db` present |
| `D:\UO\p39-rollback` | did not exist |
| `D:\ShatteredLegacy` HEAD | `52df305` (P38), working tree clean |
| D: free | 230.6 GB |

**Correction to my own assumption, and to anyone reading section 11:** the test shard autosaves **every 5
minutes** (17:00:00, 17:05:00, 17:07:30 manual, ...), not hourly. Each save moves the old `Saves` into
`Backups\Automatic\<utc time>` by rename. A copy that straddles :x0 or :x5 would be torn.

## 2. Steps, as run

### Step 1: rollback copy before the purge (17:04:55 to 17:04:56)

```
New-Item -ItemType Directory D:\UO\p39-rollback
Copy-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test D:\UO\p39-rollback\modernuo-test-before-purge -Recurse
```

- `D:\UO\p39-rollback\modernuo-test-before-purge`: **629,263,402 bytes, 228 files**, idx `03 00 00 00`.
- Taken while the 246b shard was running, 4 min after the 17:00 save and before the 17:05:00 one. My first hash
  check ran into the 17:05 save's rename (files vanished mid-check). The copy itself is good: its 21 `Saves` files
  are dated 17:00:00 to 17:00:01, and all 21 are **hash-identical** to `Backups\Automatic\2026-10-02-22-05-02`,
  which is where the 17:05 save moved the 17:00 save. That backup has one more file, a 0-byte `.backup-complete`
  marker.
- Loads on `246b` (`pre-bump-7c9215d97`); it has no P33 data.

### Step 2: purge image (17:05:43)

```
docker tag sl-modernuo:pre-bump-purge-7c9215d97 sl-modernuo:latest     -> latest = 0e65420330ca
cd D:\ShatteredLegacy\docker\uo; .\Start-TestShard.ps1 -SkipBuild
```

- **My error, harmless:** I wrapped the script in `2>&1 | Out-String`. In PS 5.1 that turns compose's stderr line
  `Container sl-modernuo-test Recreate` into an error record, and the script's `$ErrorActionPreference='Stop'`
  threw on it. Compose had already been called and finished the recreate; only the script's own "wait for
  Listening" loop was skipped. I did that wait by hand from `docker logs`. Run the script bare, as Chase does.
- Container recreated on `0e65420330ca`, started 22:05:46 UTC.
- The old 246b container was killed the same way as in step 4: a half-written shutdown save is in
  `modernuo-test\temp\CE03E11A8FCA89FF` (17:05:45). So this boot loaded the 17:05:00 autosave. Nothing of value lost
  (no players were on).
- Boot log (output I rely on):
  ```
  [SL] Commit: 7c9215d97  .NET: 10.0.203
  ModernUO ... Version 0.15.6.52
  [SaveOnShutdown] listening for SIGTERM: a stop saves the world first (D36)
  [17:05:55 INF] Loading world done (206297 items, 35181 mobiles) (3.05 seconds)
  [17:05:55 INF] Listening: 127.0.0.1:2594
  [17:05:55 INF] Listening: 172.27.0.2:2594
  ```
  No prompt. One `WRN` that predates this task: `Command stats already registered to Stats_OnCommand`.

### Step 3: purge, from the server console (17:07:07 to 17:07:43)

`docker attach` needs a TTY on the calling side, which this session does not have, and the P37 route (pipe into a
fresh `docker run -i`) does not apply to a running container. So I wrote
**`D:\UO\p39-work\console_send.py`**: it opens the Docker Engine attach API on `\\.\pipe\dockerDesktopLinuxEngine`
with **stdin only**, writes one console line plus Enter, and closes. It is hard-wired to `sl-modernuo-test`,
refuses control characters (so it can never send Ctrl-C or a detach key), and reads nothing; the output was read
with `docker logs`. Each call answered `HTTP/1.1 101 UPGRADED`.

| Time | Sent | Output relied on |
|---|---|---|
| 17:07:07 | `purgecollisions dryrun` | `DRY RUN, nothing changed: 107 mobile(s), 1 item(s), 27 spawner(s) naming one of the 11.` Raptor 15, Slith 32, Spellbinder 20, StoneSlith 22, ToxicSlith 18, ValkyriesGlaive 1 (`0x40037E87 at (843, 665, 27) TerMur`). 27 spawner lines (25 TerMur, 2 Trammel `spellbinder`). `TOTAL (dry run): would delete 108 and hold 27 spawner(s) for 30 min.` |
| 17:07:21 | `purgecollisions` | `PURGE: 107 mobile(s), 1 item(s), 27 spawner(s) naming one of the 11.` same per-type counts. **`TOTAL: deleted 108, held 27 spawner(s) for 30 min.`** |
| 17:07:30 | `save` | `Saving world done (0.10 seconds)`, `Created backup at .../Backups/Automatic/2026-10-02-22-07-32`, `Writing world save snapshot done (1.68 seconds)` |
| 17:07:43 | `purgecollisions dryrun` | `DRY RUN, nothing changed: 0 mobile(s), 0 item(s), 27 spawner(s) naming one of the 11.` **`TOTAL (dry run): would delete 0 and hold 27 spawner(s) for 30 min.`** |

Matches section 11 (expected about 107 + 1; P37 run B had the identical 108 and the identical per-type counts). The
27 spawners still *name* the types, as designed (P37 section 3): they are what refills Ter Mur from upstream.

### Step 4: stop and copy (17:08:00 to 17:09:16) -- RESULT DIFFERED

```
docker compose -f D:\ShatteredLegacy\docker\uo\docker-compose.test.yml stop
```

- Compose exit 0 at 17:08:02. Container `exited exit=137 finished=22:08:01.618 UTC`.
- Log of the stop, complete:
  ```
  [SaveOnShutdown] Saving the world before shutdown...
  [17:08:00 INF] Saving world
  [17:08:00 INF] Saving world done (0.21 seconds)
  [17:08:00 INF] Writing world save snapshot
  ```
  No `done`. The partial snapshot is in `modernuo-test\temp\538C119C4B3FBA7B` (Items.bin 2,900,837 bytes vs
  7,926,629 in the earlier temp, i.e. cut off). It was never moved into `Saves`.
- `Saves` is the step 3 `save`: **22 files, all 17:07:31.626 to 17:07:32.177**. That is after the purge, so the
  on-disk world is purged. Between 17:07:32 and the kill only time passed (the second dry run changes nothing and
  the spawners were held).
- Then the copy, which is part of step 4 and harmless, so I did it:
  ```
  Copy-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test D:\UO\p39-rollback\modernuo-test-after-purge -Recurse
  ```
  **760,173,858 bytes, 281 files** on both sides; all 22 `Saves` files hash-identical. It includes both stale
  `temp\` folders and the 17:07 backup.
- idx check. Section 11's `Format-Hex ... -Count 4` **does not run on PS 5.1** (`-Count` is PS 6+). Equivalent:
  ```
  [IO.File]::ReadAllBytes('D:\ShatteredLegacy\server\lib\uo\modernuo-test\Saves\Mobiles\Mobiles.idx')[0..3] | % { '{0:X2}' -f $_ }
  ```
  **`03 00 00 00`** on the world and on the after-purge copy. `SerializedTypes.db` present.
- After-purge `Saves` has one file the before-purge one does not: **`PointsSystem\PointsSystem.bin`** (P33). That is
  why this copy must go with `pre-bump-purge-7c9215d97` and the before-purge copy with `pre-bump-7c9215d97`
  (section 11.8 already says so; now shown on disk).

**Why I stopped here.** The brief: "If any step's result differs from what section 11 says to expect, stop, do not
continue to the next step." Step 4 expects a save on stop, and the shard was killed in the middle of it. The world
is fine this time only because step 3 had an explicit `save` 28 s earlier. Step 6 and everything after it put the
test shard on the new engine, where every later `stop` is killed the same way. P30 run 2b showed the new engine
publishes a save by renaming `Saves`. **What a SIGKILL during that publish leaves behind on the new engine is
unprobed.** That is a reason to fix the timeout before step 6, not after.

## 3. Finding: `StopTimeout = 1` on both UO containers (D36 is cut off after 1 s)

```
docker inspect sl-modernuo-test --format "StopSignal={{json .Config.StopSignal}} StopTimeout={{json .Config.StopTimeout}}"
  -> StopSignal="" StopTimeout=1
docker inspect sl-modernuo --format "{{json .Config.StopTimeout}}"
  -> 1
```

- So `docker stop` / `docker compose stop` / `down` / a recreate send SIGTERM, wait **1 s**, then SIGKILL. A world
  save here takes 1.7 to 2.6 s (17:00:01 1.62 s, 17:05:02 2.62 s, 17:07:32 1.68 s). **SaveOnShutdown (D36) can
  start but not finish.** It happened twice today: the step 2 recreate (temp `CE03...`) and the step 4 stop (temp
  `538C...`).
- **This applies to live too.** Every live stop or restart since that container was created has lost everything
  since the last autosave (at most 5 min), unless someone saved by hand first. Not probed on live; inferred from
  the same setting. I did not touch live.
- **Where the 1 comes from: unverified.** Not in either image (`.Config` has no `StopTimeout` in `cc-p38`,
  `pre-bump-purge-7c9215d97` or `pre-bump-7c9215d97`); no `stop_grace_period` in `docker-compose.yml` or
  `docker-compose.test.yml`, and `docker compose -f docker-compose.test.yml config` has no stop or grace key;
  `%USERPROFILE%\.docker\daemon.json` has none. Docker Compose is **v5.1.3**. A compose default is my best
  guess and is not checked.
- P38's load proofs did not see this because `loadproof.sh` uses plain `docker stop`, whose default is 10 s on a
  container created by `docker run`.
- **Two fixes, both outside my brief, so not done:**
  - per command: `docker compose -f ... stop -t 60` (and `down -t 60`). Works today, no file change.
  - durable: `stop_grace_period: 60s` on the service in **both** compose files. `docker-compose.yml` is the live
    file and is protected; it would need a recreate of live to take effect, which is Chase's call.
  - Not proven that `-t 60` lets the save finish (I did not want another stop/start cycle on a world the brief told
    me to stop on). First use: look for `Writing world save snapshot done` before the exit line.

## 4. Step 5, read-only (not acted on)

`Select-String prebakeMaps D:\ShatteredLegacy\server\uo\modernuo\Configuration-test\modernuo.json` ->
`"pathfinding.prebakeMaps": "False",`. So step 5 will pass as written.

## 5. To resume (Chase, or the next task): steps 5 and 6

The test world is ready for step 6 as it stands: purged, saved, idx 03, both copies taken. The 30-minute hold
(to 17:37:21) is saved in the world; on the new engine it will long have expired and the 27 spawners fill at once
(P37 section 3), which is what step 7's Ter Mur check wants. Nothing needs redoing.

```powershell
Select-String prebakeMaps D:\ShatteredLegacy\server\uo\modernuo\Configuration-test\modernuo.json
docker tag sl-modernuo:cc-p38 sl-modernuo:latest
cd D:\ShatteredLegacy\docker\uo; .\Start-TestShard.ps1 -SkipBuild
```

Expect the banner `Commit: d4531cd94b73...`, **no prompt**, "Loading world done" at about **206k items and 35.07k
mobiles** (P37/P38's 207,152 / 35,199 were a different moment of this world; today's pre-purge boot read 206,297 /
35,181), then "Listening". 14 feature-flag JSONs appear in `Configuration-test\FeatureFlags` (P30). **From the first
save on (5 minutes after boot at the latest), this world cannot go back to `7c9215d97`.**

**Whenever you stop the test shard from here on, use `-t 60`** until the timeout is fixed:
`docker compose -f D:\ShatteredLegacy\docker\uo\docker-compose.test.yml stop -t 60`, or type `save` on the console
first. `Start-TestShard.ps1 -Down` uses `down` with no `-t`, so it has the same 1-second kill.

**Never run `Start-TestShard.ps1` without `-SkipBuild`** while this is in flight: `latest` is not HEAD's build, and
building would overwrite it.

## 6. Step 7: Chase's client checks, in game (after step 6)

Log in with `D:\UO\Play-SL-Admin-TEST.bat` (test shard, port 2594). Record each result as a T-row in
`docs\client-test-queue.md`.

1. **Crafting.** Open any craft tool (e.g. a smith hammer near a forge and anvil). The normal craft gump must open,
   not a T2A-style menu. Then use **Craft X** twice: once in "keep going" mode and once in "stop on failure" mode.
   Use a low-skill character or a hard item so at least one attempt fails mid-run, and check that each mode does
   what it says.
2. **New Haven quest board.** Use the quest board in New Haven; it opens and lists quests.
3. **BOD combine.** With a small BOD and a large BOD, use "Combine this deed with contained items" on each, with the
   finished items in a container; both combine.
4. **Smith salvage bag (D42).** Put smithed metal items in a salvage bag and salvage; you get ingots back.
5. **Despise, Wisp Orb.** Possess a creature with a Wisp Orb in Despise, log out, log back in: the possessed pet must
   **not** have been auto-stabled.
6. **Individual stat cap.** Check a character's stat cap (status gump) is the shard's per-stat cap (boot log says
   500 per stat, 1500 total).
7. **Young status.** On a young character, the Young status and its countdown text show correctly.
8. **Stealable artifact slot.** Look at or steal a stealable artifact, in particular one from slot 80 or later in the
   list.
9. **Ter Mur refill and Spellbinder.** Go to one of the purged Ter Mur spawner spots, e.g. TerMur (668, 3831, -31),
   which named Raptor, or (1099, 3010, 50), which named only ToxicSlith. It should hold upstream's creatures again.
   In Trammel at (3650, 2509, 0) and (3598, 2450, 16), the two Old Haven spawners, Spellbinders should spawn.
10. **Starwood.** Make a GM lumberjack (e.g. `[SetSkill Lumberjacking 100` and target yourself; exact command form
    not checked in this task) and chop trees across many different banks (bank cells are 4x3 tiles). Starwood is
    about 1 bank in 1,036, so expect to search. When you get Starwood logs, check that the logging book records the
    find.

## 7. Step 8: rollback, if any client check fails (after step 6)

```powershell
cd D:\ShatteredLegacy\docker\uo; docker compose -f docker-compose.test.yml stop -t 60
Rename-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test modernuo-test.new-engine-aside
Copy-Item D:\UO\p39-rollback\modernuo-test-after-purge D:\ShatteredLegacy\server\lib\uo\modernuo-test -Recurse
docker tag sl-modernuo:pre-bump-purge-7c9215d97 sl-modernuo:latest
.\Start-TestShard.ps1 -SkipBuild
```

(Section 11's version, with `-t 60` added to the stop.) Set the new-engine world aside; do not delete it. Then
revert the P38 commits in both repos, and `git -C D:\UO\ModernUO-pinned checkout --detach 7c9215d97`. Use
`pre-bump-7c9215d97` (`246b`) only with `D:\UO\p39-rollback\modernuo-test-before-purge`: the after-purge save has
`PointsSystem\PointsSystem.bin`, which only an image with P33 reads.

**If you decide not to go ahead at all:** nothing to roll back. The test shard is stopped on `0e65` (pinned
engine, purged world). `.\Start-TestShard.ps1 -SkipBuild` brings it back up as it is.

## 8. Rollback copies

| Copy | Size | Save it holds | Pair with image |
|---|---|---|---|
| `D:\UO\p39-rollback\modernuo-test-before-purge` | 629,263,402 bytes, 228 files | 17:00:01 autosave on `246b`, idx 03 | `sl-modernuo:pre-bump-7c9215d97` (`246b0d5813e5`) |
| `D:\UO\p39-rollback\modernuo-test-after-purge` | 760,173,858 bytes, 281 files | 17:07:32 post-purge save on `0e65`, idx 03 | `sl-modernuo:pre-bump-purge-7c9215d97` (`0e65420330ca`) |

## 9. Clashes and scratch

- **Numbering:** no clash. At 17:10 `notes\` had no P40/P41/P42 file. Briefs `cc-P40-custom-client-research.md`
  and `cc-P41-companions-research.md` say nothing about Docker, `sl-modernuo` or stopping a shard (grep); P41
  mentions the test shard's skill gain only as a fact to read. `cc-P42-defect-batch-3.md` exists and waits for this.
  `D:\ShatteredLegacy` clean at `52df305`; `D:\UO\shard-migration` showed only the three files already modified at the start
  (`client-policy-2026-10-02.md`, `passdown-overseer-2026-10-02.md`, `skills-design.md`), not mine, plus this note.
- **Scratch from this task, kept:** `D:\UO\p39-work\console_send.py`. Two stale half-saves under
  `modernuo-test\temp\` (`CE03E11A8FCA89FF`, `538C119C4B3FBA7B`); ModernUO does not read `temp\`, and I left them
  (the brief: delete nothing).
- P38's scratch list (its section 13.4) is unchanged by this task; `cc-p37` / `pre-bump-purge-7c9215d97` and
  `pre-bump-7c9215d97` are still needed until P39 passes.
