# cc-P43: 60 s stop timeout, then the test-shard cutover (P39 steps 5 and 6)

2026-10-02. Brief: `D:\UO\cc-prompts\cc-P43-stop-timeout-and-cutover.md`. TEST shard only. Live (`sl-modernuo`, image
`bc04a35bf344`, started 11:57:46 UTC) was not stopped, restarted, recreated or composed; `Up 11 hours` at start and
end. No commit, no build, nothing deleted. Git only with `--no-optional-locks`.

## Headlines

1. **Part A done.** `stop_grace_period: 60s` in both compose files, `Start-TestShard.ps1 -Down` uses `down -t 60`.
   `compose config` shows `stop_grace_period: 1m0s`; the recreated test container has `StopTimeout` **60**.
2. **Step 6 passes.** A plain `compose stop` (no `-t`) now lets D36 finish: `Writing world save snapshot done (1.76
   seconds)` and `[SaveOnShutdown] ...saved in 1943 ms` before `Shutting down`, **exit 0**, stop took 2.98 s, `Saves`
   whole (22 files, same set as the 17:07:32 save, no new `temp\` folder). D50 is fixed on the test container.
3. **NOT cut over. I stopped before step 8**, because step 4 un-purged the world. The purge's 30-minute spawner hold
   ran out at 17:37:21; the old engine ran 15 s (18:09:13 to 18:09:28) and the 27 spawners refilled at once. The
   18:09:30 save holds **7 instances of the collision types**: Slith 2, ToxicSlith 3, Spellbinder 1 (mobiles),
   ValkyriesGlaive 1 (item, `0x400C577C`). The 17:07:32 save held **0** (section 3). On the new engine each of these
   fails to load "3 bytes short" and raises `Delete the object and continue? (y/n/a)` (P30 section 2c), which blocks
   the boot. Step 9 expects no prompt. `latest` is still `0e65420330ca` (old engine); the world is still idx v3 and
   fully reversible.
4. **The clean world still exists twice**, hash-identical to the 17:07:32 save: `D:\UO\p39-rollback\modernuo-test-after-purge`
   and `modernuo-test\Backups\Automatic\2026-10-02-23-09-30` (the 18:09 save moved it there). Section 5 gives Chase
   two ways on.
5. **My miss, and the brief's:** neither of us saw that step 4 (boot the old engine to prove the stop) re-opens the
   window the hold existed to close (P37 section 3 says exactly this). I could have caught it before booting. Cost:
   one more step before the cutover, nothing lost.

## 0. Starting state (18:0x), all as the brief said

| Thing | State |
|---|---|
| `D:\ShatteredLegacy` | HEAD `52df305`, `status --short` empty |
| `sl-modernuo:latest` | `0e65420330ca` (= `cc-p37` = `pre-bump-purge-7c9215d97`) |
| `sl-modernuo:cc-p38` | `45b7523ae54b` |
| `sl-modernuo-test` | `Exited (137)`, image `0e65`, finished 22:08:01 UTC, `StopTimeout` 1 |
| `sl-modernuo` (live) | image `bc04a35bf344`, running since 11:57:46 UTC, `StopTimeout` 1 |
| Test `Saves` | 22 files, 17:07:31.626 to 17:07:32.177, `Mobiles.idx` `03 00 00 00` |
| Rollback copies | `modernuo-test-after-purge` 281 files 760,173,858 bytes; `modernuo-test-before-purge` 228 files 629,263,402 bytes (same as P39 section 8) |
| `temp\` | the two stale half-saves from P39 (`538C...`, `CE03...`) |

Hash list of the 17:07:32 `Saves` kept in my scratchpad for the step 6 comparison.

**Numbering:** no clash. `notes\` has P40 and P41 (research, not mine, untracked), no P42 or P43 note before this
one; `cc-P42-defect-batch-3.md` brief exists and waits for this.

## 1. Part A: the timeout

```diff
 docker-compose.yml, service modernuo:
     restart: unless-stopped
+    stop_grace_period: 60s   # D50: was 1 s, which SIGKILLed D36's shutdown save mid-write. Takes effect when live is next recreated (fresh-world wipe).

 docker-compose.test.yml, service modernuo-test:
     restart: "no"
+    stop_grace_period: 60s   # D50: was 1 s, which SIGKILLed D36's shutdown save mid-write
 and line 8, the usage comment:
-#   docker compose -f docker/uo/docker-compose.test.yml down     stop it
+#   docker compose -f docker/uo/docker-compose.test.yml down -t 60     stop it (60 s for the shutdown save, D50)

 Start-TestShard.ps1, -Down:
-    docker compose -f $compose down
+    # -t 60 as well as stop_grace_period in the compose file: D36's shutdown save needs seconds (D50).
+    docker compose -f $compose down -t 60
```

- `docker compose -f docker\uo\docker-compose.test.yml config` -> **`    stop_grace_period: 1m0s`**
- After the step 4 recreate: `docker inspect sl-modernuo-test --format "{{json .Config.StopTimeout}}"` -> **`60`**
- `COMMANDS.md`, `SERVER.md`: no docker stop/down command in either (grep for stop/down/restart/attach/kill;
  SERVER.md's `systemctl stop uo` lines describe the old systemd host). No change.
- **Not changed, outside the file list:** `docker/uo/test-shard.sh:14` (`--down`) runs a bare `$COMPOSE down`. With the
  compose key it now waits 60 s anyway, so it is safe; add `-t 60` there next time someone is in that file.
- All three files ASCII only (byte check: 0 bytes above 127).
- Live: file change only. The live container keeps `StopTimeout` 1 until it is recreated. **Until then, a live stop
  still kills D36's save after 1 s**: stop live with `docker stop -t 60 sl-modernuo` (never compose on that file, D29)
  or type `save` first.

## 2. Part B steps 4 to 6, as run

### Step 4: boot on the old engine (18:09:04 to 18:09:14)

`D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`, run bare. `Container sl-modernuo-test Recreate`, started
23:09:05 UTC on `0e65`. Log:

```
[SL] Commit: 7c9215d97  .NET: 10.0.203
[SaveOnShutdown] listening for SIGTERM: a stop saves the world first (D36)
[18:09:10 WRN] Command stats already registered to Stats_OnCommand.      (predates this task)
[18:09:13 INF] Loading world done (205689 items, 35114 mobiles) (2.58 seconds)
[18:09:13 INF] Listening: 127.0.0.1:2594
[18:09:13 INF] Listening: 172.27.0.2:2594
```

**P39's "35,181 - 107 = 35,074 mobiles expected" was wrong, and it said it was not re-read.** The post-purge save
holds 35,114 mobiles and 205,689 items, both counted from its `.idx` headers and agreeing with this boot. The 17:05:55
boot read the 17:05:00 autosave; the world moved by +40 mobiles and -607 items (net of the 107 + 1 purged) between 17:05:00 and 17:07:32.

### Step 5: `StopTimeout` -> `60`. Pass.

### Step 6: plain stop, no `-t` (18:09:28.481 to 18:09:31.460, 2.98 s)

```
docker compose -f D:\ShatteredLegacy\docker\uo\docker-compose.test.yml stop     -> exit 0
docker inspect: status=exited exit=0 oom=false finished=2026-10-02T23:09:30.682 UTC
```

Log with Docker timestamps (UTC):

```
23:09:26.473 Client: 172.27.0.1: Connected. [1 Online]       (the Docker gateway, i.e. a host-side probe; not a player)
23:09:27.971 Client: 172.27.0.1: Disconnected. [0 Online]
23:09:28.719 [SaveOnShutdown] Saving the world before shutdown...
23:09:28.753 Saving world
23:09:28.899 Saving world done (0.15 seconds)
23:09:28.899 Writing world save snapshot
23:09:30.373 Created backup at /var/lib/uo/modernuo/Backups/Automatic/2026-10-02-23-09-30
23:09:30.663 [SaveOnShutdown] ...saved in 1943 ms
23:09:30.663 Writing world save snapshot done (1.76 seconds)
23:09:30.663 Shutting down
```

SIGTERM to exit: about 1.96 s. Under the old 1 s it would have been killed again.

`Saves` after: **22 files, 18:09:29.468 to 18:09:30.063**, `Compare-Object` of file names against the 17:07:32 set: no
difference. `Mobiles.idx` `03 00 00 00`. `temp\` holds only P39's two old folders, nothing new. The new backup
`2026-10-02-23-09-30` has 22 files + `.backup-complete`, hash-identical to the 17:07:32 save.

### Step 7: the world is idx v3, new save time **18:09:30**. Rollback copies not retaken.

## 3. Why I stopped before step 8: the collision types are back

The `SerializedTypes.db` of the 18:09:30 save lists `Server.Mobiles.Slith`, `ToxicSlith`, `Spellbinder` and
`Server.Items.ValkyriesGlaive`; the 17:07:32 one did not. To count instances rather than names, I decoded the idx v3
files: header `int version, int count`, then 33-byte entries `byte, long typeHash, uint serial, long created, long
position, int length`, the hash looked up in `SerializedTypes.db` (`int 0, int count`, then `long hash` + 7-bit-length
name). **Every entry in both saves resolved to a name (0 unresolved)**, which is the check that the layout is right.

| Save | Mobiles | Items | Instances of the 11 |
|---|---|---|---|
| 17:07:32 (after purge; = after-purge copy; = backup `23-09-30`) | 35,114 | 205,689 | **0** |
| 18:09:30 (now in `Saves`) | 35,327 | 208,501 | **7**: Slith 2, ToxicSlith 3, Spellbinder 1, ValkyriesGlaive 1 (`0x400C577C`) |

+213 mobiles and +2,812 items in a 15-second run: the spawners were refilling. No Raptor or StoneSlith yet.

Cause: P37 section 3. Deleting a spawned creature restarts its spawner, so the purge holds the 27 spawners for 30 min
and expects the stop inside that window. The hold ended 17:37:21; step 4 booted the old engine at 18:09, with our
types still compiled in, and they spawned. Effect on the new engine: P30 section 2c, each instance reads 3 bytes short
and the load stops at a `Delete the object and continue? (y/n/a)` prompt, one for mobiles and one for items. Not
re-probed today; P30 run 2c is the evidence.

So step 8 would fail step 9 by construction. I did not tag, boot, or touch the world.

## 4. State at the end (18:1x)

- `sl-modernuo:latest` = `0e65420330ca`. `cc-p38` = `45b7523ae54b`, not tagged latest.
- `sl-modernuo-test`: `Exited (0)`, `StopTimeout` 60, image `0e65`.
- Test world: `Saves` = the 18:09:30 save, idx v3, **7 collision instances**. Loads on `0e65`, not cleanly on `cc-p38`.
- Clean copies of the 17:07:32 world: `D:\UO\p39-rollback\modernuo-test-after-purge` (whole folder) and
  `modernuo-test\Backups\Automatic\2026-10-02-23-09-30` (`Saves` only).
- `D:\ShatteredLegacy`: three files modified (section 6), nothing else.

## 5. To finish the cutover (Chase or a follow-up task): pick one

**Option A (recommended): put the clean 17:07:32 world back, then cut over with no old-engine boot in between.**
The stop proof is done, so nothing needs the old engine again. Loses only the 15 s of old-engine run.

```powershell
Rename-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test modernuo-test.p43-respawned-aside
Copy-Item D:\UO\p39-rollback\modernuo-test-after-purge D:\ShatteredLegacy\server\lib\uo\modernuo-test -Recurse
Select-String prebakeMaps D:\ShatteredLegacy\server\uo\modernuo\Configuration-test\modernuo.json
docker tag sl-modernuo:cc-p38 sl-modernuo:latest
cd D:\ShatteredLegacy\docker\uo; .\Start-TestShard.ps1 -SkipBuild
```

Expect: `Commit: d4531cd94b73...`, no prompt of any kind, **`Loading world done (205689 items, 35114 mobiles)`** (the
counts of the 17:07:32 save, counted in section 3), then `Listening`; 14 JSONs in `Configuration-test\FeatureFlags`.
The copy keeps the after-purge copy as the rollback (copy, not move). Set the aside folder aside; do not delete it.

**Option B: re-purge on the old engine, then cut over inside 30 minutes.** Boot on `0e65`, `purgecollisions dryrun`
(expect at least the 7, more the longer it runs), `purgecollisions`, `save`, `purgecollisions dryrun` -> "would delete
0", `compose stop` (60 s now), then the three cutover lines from option A, all inside the new 30-min hold. Console
via `D:\UO\p39-work\console_send.py` as in P39. More steps and a timed window; no advantage over A that I can see.

**Option C: cut over now and answer the prompts `y`.** P30's trial did this. It needs an interactive `docker attach`
and contradicts step 9's "no prompt". Not recommended.

After whichever: leave the shard running, record the boot time (from the first save, 5 min at most, the world is idx
v5 and cannot go back to `7c9215d97`), then Chase's client checks, P39 notes section 6 (step 7).

**Whatever is chosen: from now on the test shard's purged types are only safe on disk while the old engine is not
running.** Do not boot `0e65` on the cleaned world again except as option B.

## 6. Files changed, for Chase's commit (`D:\ShatteredLegacy`)

- `docker/uo/docker-compose.yml` (+1: `stop_grace_period: 60s` and its comment)
- `docker/uo/docker-compose.test.yml` (+1 key, line 8 usage comment)
- `docker/uo/Start-TestShard.ps1` (`-Down` -> `down -t 60`, one comment)

Suggested subject: "D50: 60 s stop grace period on both shard services; test shard verified, live on next recreate".
Verified: test container StopTimeout 60 and a plain stop completed the D36 save, exit 0. Not verified: live (file only).

And `D:\UO\shard-migration\notes\cc-P43-stop-timeout-and-cutover.md` (this file). `docs\` not touched; D50 in
`docs\bug-list.md` can be marked fixed for the test shard and pending recreate for live.

## 7. Scratch

- Hash list of the 17:07:32 `Saves`: scratchpad only, not kept in the repo.
- No new files under `D:\UO\p39-work` or `D:\UO\p39-rollback`.
