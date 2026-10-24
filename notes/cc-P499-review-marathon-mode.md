# P499: review of marathon mode (P200)

Reviewed 2026-10-23. Notes only. No code, settings, or live Golem state changed.

P200 is in code main as commit `2a3c031`; the reviewed main and work-copy HEAD were `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`.
Read `notes/cc-P200-cont-marathon-mode.md`; no separate P200 review was present beside it.
The findings below exclude the issues already recorded there.

## Findings

1. **bug: `D:\UO\golem\golem.ps1:4270` and `:4292`.** When marathon tries to wake an idle Golem with no `restReason` and the five-hour window is full, it records `wakePending`, but subsequent watches require a rest reason to retry it and also exclude pending wakes from the marathon path, so it stays idle after the window resets. Retry transient pending wakes without requiring a preexisting rest reason, while keeping the normal wake checks, and add a regression starting from idle rather than an existing pace rest.

2. **bug: `D:\UO\golem\golem.ps1:1866` and `:4275`.** A pending marathon wake can open a CLI session outside the Golem's hours after marathon turns off: `Get-WakeTarget` rejects the target, but `Invoke-SelfWake` continues with the remembered prompt and model when that lookup returns nothing. Refuse automatic wakes when no eligible target remains, recheck hours and back-off before launching, and cover the transition from marathon on to off with a pending wake.

3. **bug: `D:\UO\golem\golem.ps1:926` and `:935`.** Each watch timestamps cached usage as a new observation without checking its report time, so an unchanged report can manufacture a slowdown and enable marathon despite the actual burn rate being unknown. Preserve the source observation time, exclude duplicate or stale reports from rate calculations, and test a reader outage with repeated watches.

4. **risk: `D:\UO\golem\golem.ps1:1099` and `:1103`.** An auto marathon state from the previous week survives a weekly reset when the new projection is unknown, retaining sprint pacing and widened hours; a probe one hour into the new week allowed 95% of the week while ordinary pacing would allow about 3.6%. Associate automatic state with its weekly reset and clear the old week's state before evaluating the new week, with a regression crossing the reset while auto is on.

## Evidence and missing coverage

These were temporary probes against unchanged source, using Windows PowerShell 5.1.
No new test files or fixes were added.

- Finding 1: an isolated enabled fixture with marathon on, no running prompt, and no rest reason saw 96% session usage at 13:00 with a 13:05 reset. Its watch saved a pending marathon wake; at 13:10, with fresh 0% session usage, the pending state remained unchanged and no CLI call occurred. Temporary fixture: `golem-test-a34cbb55` under the local temp folder. `D:\UO\golem\tests\Golem.Tests.ps1:2225` exercises resuming an existing pace rest, which misses this idle case.
- Finding 2: an isolated Bronze fixture had hours `22:00-06:30`, marathon off, and a due pending marathon wake at 13:10. The same watch logged `claim: outside Bronze's hours (22:00-06:30): nothing taken`, then launched `Golem Bronze P101` through the CLI stub. Temporary fixture: `golem-test-58f0a0be`. This proves the session opens; it does not prove the session later claims a prompt outside hours. The on/off cases at `D:\UO\golem\tests\Golem.Tests.ps1:2246` do not exercise a pending wake across a switch.
- Finding 3: extracted the real sampling and projection functions and supplied 24 hours of readings rising from 60.8% to 80%, with 20 hours until reset. The initial projection was 96%; after four hours of ten-minute watches reusing that identical report, the projection was 90.7%, below the 95% activation target, with no newer usage observation. Temporary data: `p499-projection-d05e701b`. `D:\UO\golem\tests\Golem.Tests.ps1:2159` supplies fresh reports for its watches and does not cover cached observations.
- Finding 4: extracted the real switch and pacing functions, supplied an on state from the old week and a new reset 167 hours away, with fresh weekly usage at 20%. The projection was unknown, auto stayed on, and `Get-PaceCheck` returned `Ok = true` with a 95% allowance. File and mail helpers were stubbed in memory; the switch and pacing calculations were unchanged. `D:\UO\golem\tests\Golem.Tests.ps1:2183` does not carry an active auto state through a weekly reset.

## Scope and checks

Read the P200 changes and relevant callers in:

- `D:\UO\golem\golem.ps1`
- `D:\UO\golem\Golems.ps1`
- `D:\UO\golem\GolemPower.ps1`
- `D:\UO\golem\Set-Marathon.ps1`
- `D:\UO\golem\tests\Golem.Tests.ps1`
- `scripts/Shard-Console.ps1`
- `scripts/tests/Shard-Console.Tests.ps1`
- `web-console/golem-actions.json`
- `web-console/console-actions.json`
- `web-console/static/app.js`
- The P200 changelog entry.

No additional finding in the reviewed console or web changes. No arithmetic bypass of
`usageLimitPct` was found when both usage windows are known and current; finding 3 concerns
the projection's input timestamps, and finding 4 concerns the pacing allowance.

Validation:

- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`, with `SL_FACT_FILTER=^P200_`: all three named facts passed (`P200_TheMarathonButtonSetsThePickedModeAfterItsPhrase`, `P200_TheGolemTabShowsTheProjectionMarathonAndWidenedHours`, `P200_TheMarathonPickIsOnTheGolemTabAndFollowsTheSetting`).
- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Golem.Tests.ps1 -Only P200`: seven named facts passed, with 47 checks passed and one fixture setup failure. The unverified fact was `P200_Marathon_WakesEveryAwakeGolemOnItsLaneAndOpensDaytimeHours`: its temporary local Git push failed because Git's `sh.exe` could not create a signal pipe (Win32 error 5), before the behavior assertions ran. The passing facts were `P200_Projection_MathOnRecordedSamples`, `P200_Projection_TheWatchRecordsSamplesAndStatusShowsIt`, `P200_Marathon_AutoTurnsOnBelowTargetWithHoursLeftAndOffAtTheTarget`, `P200_Marathon_TheFiveHourWindowStillPauses`, `P200_Marathon_TheLowQueueEmailFiresOnce`, `P200_Settings_DefaultAsStatedAndMarathonSetWritesOneKey`, and `P200_Marathon_LiftsTheRunCapAndTheLargeRestAndRunsTheNightShiftAtFull`.
- `python tools\progress.py --dry-run`, with paths set to these work copies: exit 0. Despite its flag, it rewrote `tools/progress.json`; restored that generated file to its clean starting contents so only this note is delivered.

The runtime files in `D:\UO\golem` are outside these repositories, so their exact correspondence
to merged P200 source is unverified; they include later changes. The reviewed `golem.ps1`
SHA-256 was `E8C2C1A44184B74171AA87E1EA1641E033731E41A6A209733B0F2D581C702FA8`.
Remote PC behavior and live account spending are unverified. No Haven connection, deployment,
live watch invocation, or work-copy commit, merge, push, or branch switch was performed.

P499 DONE
