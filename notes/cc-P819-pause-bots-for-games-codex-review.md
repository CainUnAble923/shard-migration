# Codex review: P819

CC task P819: pause bot play testing while Chase plays other games. Reviewed by Codex (`codex exec review`, read-only) after P819 DONE and before the Golem's commit, 2026-11-08 00:28.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The shared-check integration and console switch are present, but timeout handling can restart client activity while a game is running, and soak cancellation leaves pending client creation active. The night deadline also rolls forward incorrectly for later waits.

- **high** [P1] Skip the soak after a game wait reaches the night deadline (`tools\playtest-bot\uobot\run.py:397`)
  If a wait during the checks times out, `pause.over` becomes true and the remaining checks are skipped, but this loop still starts the soak: `hold()` calls `playing()`, which returns an empty string when `over` is true, so `hold()` returns true. Game detection then stays disabled throughout the soak. Consequently, the default overnight run reconnects clients and runs its soak while Chase is still playing, immediately after declaring the night skipped. Check `pause.over` here or make `hold()` return false after timeout.
- **medium** [P2] Cancel pending actor setup before entering the game wait (`tools\playtest-bot\uobot\soak.py:137`)
  If a game starts while a soak actor is waiting inside `ctx.fresh()` for a resting pool account, setting this deadline does not stop that actor. `fresh()` can wait 330 seconds, whereas cleanup only joins each thread for 30 seconds. The soak can therefore return and enter the game wait with actor threads still alive; those threads subsequently log in and perform setup while Chase plays, and their clients were absent from the earlier cleanup. Make account acquisition/setup cancellable and ensure all actor threads have stopped before beginning the wait.
- **medium** [P2] Preserve the original night's deadline across successive waits (`tools\playtest-bot\uobot\run.py:258`)
  If the overnight run reaches a later check or soak boundary after 06:30 and discovers a game, passing the unchanged `HH:mm` value starts a wait until the following morning: `Test-GameRunning.ps1` explicitly advances an already-passed time to tomorrow. This can leave the nightly task and scratch shard running through the day instead of skipping the remainder of that night. Resolve one absolute deadline for the run and refuse further waits once it has passed.

(1.3 minutes, 448,282 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The reviewed kit copies leave Golem client steps failing rather than automatically waiting and resuming, and repeated checks can extend an expired night window until tomorrow. Changes outside this repository were not reviewed comprehensively.

- **medium** [P2] Preserve the current night's deadline across repeated checks (`notes\cc-P819-tools\kit\Test-GameRunning.ps1:34`)
  If a mid-run game check invokes this script at or after 06:30, `-Until 06:30` becomes tomorrow's deadline. The overnight bot invokes the CLI again when a game starts between checks or during a soak, so a run crossing 06:30 can wait into the next day and then resume instead of skipping the remainder of that night. Pass an absolute deadline established at the start of the night, or otherwise distinguish a pre-midnight launch from an expired morning window.
- **medium** [P2] Wait and resume client-opening steps instead of refusing them (`notes\cc-P819-tools\kit\LegionTest.ps1:54`)
  When Chase is playing, this returns a failed guard rather than scheduling a wait and resuming the requested step. For example, `Test-LegionScript.ps1` immediately exits 2 when this guard fails; no wait-status file is created and nothing retries after the game closes. Printing instructions for an agent to run another command does not implement the automatic wait/resume required by task item 3. Wire the wait into the execution path, using a background continuation if necessary.

(0.8 minutes, 258,369 tokens)
