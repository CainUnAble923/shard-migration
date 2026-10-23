# P492: review of the Tinker watchdog

Reviewed 2026-10-23. Notes only. No implementation changes, deployments, remote PC connections, or messages sent.

Read both work copies' AGENTS.md, the direction decision and task list, P222's implementation notes, P244's merge notes, and P410's implementation notes and Codex review. No separate P244 review was found beside its notes. The findings below do not repeat P244's portrait and console-test issues or P410's failed play-test mail classification issue.

Repo versions: ShatteredLegacy `7c085f7`; shard-migration `f9f6d68`. The watchdog implementation lives outside these repos in `D:\UO\golem`; citations below refer to those installed files as read today, including later changes such as P410.

## Findings

1. **bug**: `D:\UO\golem\Kit.ps1:142` and `D:\UO\golem\Install-Kit.ps1:15`: The installer does not make copy and rename errors terminating, so an ordinary PowerShell file error can bypass rollback and report a successful install with only some files replaced; an in-memory probe with failing `Move-Item` calls returned `Ok=true` and two files installed. Use terminating errors throughout backup, staging, replacement, and rollback, and test an actual file-operation failure through the installer entry point, since the current test uses an explicit throw and sets the error preference to Stop.

2. **bug**: `D:\UO\golem\TinkerLib.ps1:249`: The WIP fix ignores failed `git add` and `git commit` commands and always returns `ok=true`, after which the round clears the flag and wakes the Golem even though the blocking work remains uncommitted. Check each exit code and confirm both copies are clean before continuing, with a regression test for a failed commit; the generated script returned success in a probe where both Git operations returned exit 128.

3. **bug**: `D:\UO\golem\TinkerLib.ps1:577` and `:606`: The daily fix check excludes unknown stalls, so a reasoning session can select the same allowed fix again after its counter reaches two, up to the separate reasoning-session limit. Enforce the fix budget before every automatic or reasoned action and test repeated unknown stalls across permitted session times; an in-memory round probe applied three fixes with the configured limit of two and raised no question.

4. **bug**: `D:\UO\golem\TinkerLib.ps1:221`: A remote Golem's lock warning is cleared by checking the game PC's `locks` folder, although the remote hook uses its own root's locks, so an absent local lock is treated as proof that the remote lock is free. Include the target PC's lock in its collected facts and require that evidence before clearing the warning, with a test where the remote lock is held and the game PC's lock is absent.

5. **bug**: `D:\UO\golem\TinkerLib.ps1:369` and `:373`: A failing watch is treated as repaired by `kit-resync`, but local PCs immediately return success and remote PCs with matching hashes also return success without restarting or checking the watch; the Force parameter does not change either result. Verify recovery through a new heartbeat and provide a targeted watch restart when appropriate, with tests for a dead local watch and a dead remote watch whose files already match.

6. **bug**: `web-console/static/app.js:284` and `D:\UO\golem\TinkerLib.ps1:427`: The question email tells Chase to answer yes or no on the Tinker's card, but that card only displays the question text and offers Run now, Pause, and Resume, while the question is never registered with the existing answer system. Register these questions through `Questions.ps1`, connect the choices to the proposed action, and test that an answer applies that action once.

7. **bug**: `D:\UO\golem\Remote-Agent.ps1:244` and `D:\UO\golem\TinkerLib.ps1:373`: Both kit delivery paths return early when file hashes match, even if the refreshed manifest contains a setting key missing on the receiving PC, so a settings-only kit update never reaches the installer's settings merge. Include missing settings in the decision to install and test a manifest that adds a key without changing any file, while preserving existing per-PC values.

8. **risk**: `D:\UO\golem\TinkerLib.ps1:603`: The script applies any allowed fix without checking confidence, despite the rulebook requiring a question below 0.6; the round probe accepted confidence 0.1. Validate the answer's shape, arguments, and numeric confidence before applying it, and cover low, missing, and invalid confidence in the reasoning-session tests.

9. **risk**: `D:\UO\golem\TinkerLib.ps1:427`, `D:\UO\golem\TinkerMail.ps1:80`, and `:82`: Question causes, event bodies, and log lines reach email without credential redaction, and an intercepted question email retained both a synthetic private Windows path containing a space and a synthetic token. Redact credentials at the common sender and minimize unnecessary private paths, with fixtures covering question text, model answers, and logs; no actual secret disclosure was verified.

## Evidence and limits

Read the relevant implementation and test sections in these files:

- `D:\UO\golem\TinkerLib.ps1`, `Tinker.ps1`, `Tinker-Hidden.vbs`, `Kit.ps1`, `Install-Kit.ps1`, and `tinker-rulebook.md`.
- `D:\UO\golem\Golems.ps1`, `golem.ps1`, `Remote-Agent.ps1`, `Retry-Stopped.ps1`, `Wake-Golem.ps1`, and `TinkerMail.ps1`.
- `D:\UO\golem\tests\Tinker.Tests.ps1`, the P222 facts in `tests\Golem.Tests.ps1`, and `tests\RemoteAgent.Tests.ps1`.
- `scripts/Shard-Console.ps1`, its P222 fact in `scripts/tests/Shard-Console.Tests.ps1`, `web-console/server.py`, `web-console/static/app.js`, `web-console/console-actions.json`, `web-console/golem-actions.json`, and `web-console/tests/test_remote_golems.py`.

Ran the existing `D:\UO\golem\tests\Tinker.Tests.ps1 -Only P222` under Windows PowerShell 5.1: **133 checks passed, 0 failed**. The suite uses fake kits, scratch repositories, intercepted PC execution and mail, and a fake reasoning CLI. No new tests were added.

Additional Windows PowerShell 5.1 probes ran the existing functions with in-memory substitutes for file operations, Git, mail, reasoning, and other external effects. They demonstrated findings 1, 2, 3, 5, 8, and 9 without changing the installed kit or running a real fix. The remote-lock finding is supported by the source and a pure classification call, not by inspection of another PC's locks. Findings 6 and 7 are source findings, not completed UI or remote-install trials.

The targeted Python web kit-route test could not reach an assertion: Windows denied creation of its `data` subdirectory under both the default temp location and an ignored workspace scratch location. Its runtime result is unverified. The broader console and Golem suites were inspected for relevant coverage but not rerun. No live watchdog round, scheduled task, SMTP delivery, SSH operation, or Claude session was run.

Automatic approval review rejected an earlier combined probe command that would create scratch Git repositories and remove its scratch folders, stating only "blocked by policy." I used in-memory substitutes instead.

Automatic approval review also rejected cleanup of the Python test's ignored scratch folder, with the same reason. `downloads/p492-review-temp` remains in the code work copy; `git check-ignore` confirmed it is ignored, and it is not a deliverable. No tracked code file changed.

Installed source SHA-256 values, for identifying the reviewed revision:

| File under `D:\UO\golem` | SHA-256 |
|---|---|
| `TinkerLib.ps1` | `34F1D8A928EDE62CF8EA24E6BE55E81A0D087A4C5A6538E09C838AA4EB05B8B7` |
| `TinkerMail.ps1` | `0211675A539254C47A1BCC6CEB957C5C0A26AB25C3D2FD506239249A9F14D192` |
| `Kit.ps1` | `F20E7B6A2A0BEAD8C3EBCEB73B769F019DFD7BABC8A191A808C512D0C23B5638` |
| `tests\Tinker.Tests.ps1` | `CD72AFB7A70C78C85AF282A8E43DF70402631104A9439E83C2CF920E144062F7` |

P492 DONE
