# cc-P716: TazUO pictures of the server on the SoS map (continues P675, SoS swap S2)

## In plain words

- No pictures yet. The overnight play-test bot was still running at 05:38 (it started at 01:33 and usually ends by
  03:30), and the proof shard needs the bot's world and the test-shard slot, so the pictures had to wait.
- The server's map overlay was rebuilt on the Siege of Sosaria map and checked again: it is still exactly SoS plus our
  patch, as it was in P675.
- The PC was short on memory too (about 4 GB free, and Claude Code stopped my background watcher for low memory).
  Two game windows and a shard need more than that.
- For you: nothing, unless the bot is stuck. If `uobot.run` (PID 18640) is still running well after its normal finish,
  look at it. Then put P716 back in the queue and a new session takes the pictures (about 15 minutes).

## What was done

1. `notes\cc-P675-tools\overlay-run.ps1 -Scratch <scratchpad>\p716` built the overlay on SoS
   (`map1LegacyMUL.uop` 89,919,252 bytes, `statics1.mul` 46,293,842, `staidx1.mul` 5,505,024). Its three refusals
   still refuse: a `map1.mul` in the client data, a base file with one byte changed, and a missing base file.
   `rebase.py <scratchpad>\p716\rebase` (no `--ship`) rebuilt the edited map. Today's shipped patch on SoS: drifted 0,
   missing 0. `overlay_check.py` (`cc-P716-tools\out-overlay-check.txt`): land identical to SoS + patch **True**,
   statics blocks differing **0**; 504,384 is `0003@15` and 6638,3993 is `0073@0`, the same as P675's green.
2. Not started. At 04:39, and again at 05:38, `uobot.run` (PID 18640, started 01:33:35,
   `--runs 3 --soak-minutes 120`) was alive and `sl-modernuo-bot` was up. The prompt says no proof shard while it runs,
   and `proof-shard.ps1` copies `D:\UO\bot-shard\world`, which the bot is using. I took no lock and started no
   container. The background wait for the bot was stopped by Claude Code for low memory (4.08 GB free at 05:38), and I
   did not start it again.
3. and 4. Not started.

## To finish (a new session)

The image `sl-modernuo:cc-P675` exists (P675 has merged into main as `ed57b58`). The scratch overlay lives in a
session scratchpad, so build it again first (about 5 s):

```
powershell -NoProfile -ExecutionPolicy Bypass -File notes\cc-P675-tools\overlay-run.ps1 -Scratch <scratch>
python -P -B notes\cc-P675-tools\rebase.py <scratch>\rebase
python -P -B notes\cc-P675-tools\overlay_check.py <scratch>\overlay <scratch>\rebase\edited
# check: no uobot.run process, no sl-modernuo-bot container, more than about 8 GB free
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take test-shard -Minutes 60 -Wait
powershell -NoProfile -ExecutionPolicy Bypass -File notes\cc-P675-tools\proof-shard.ps1 -Work <scratch>\shard -Overlay <scratch>\overlay
powershell -NoProfile -ExecutionPolicy Bypass -File notes\cc-P675-tools\shots.ps1 -Spec notes\cc-P675-tools\scenes.json -Out notes\art\sos-s2-shots
powershell -NoProfile -ExecutionPolicy Bypass -File notes\cc-P675-tools\proof-shard.ps1 -Work <scratch>\shard -Down
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release test-shard
```

Then look at all eight pictures: Valunstead on Trammel and Felucca; Valunstead on the Fold and the hall floor; the
beach on Trammel (the Player lands in New Haven) and Felucca (the Admin stays); Passage of Lost Souls 2 on both.

## State

- No lock held, no container of mine running, nothing committed. Files added: this note,
  `notes\cc-P716-tools\out-overlay-check.txt`, and a link line in P675's notes.

P716 STOPPED: the overnight bot was still running at 05:38 and memory was low; no shard started, nothing held
