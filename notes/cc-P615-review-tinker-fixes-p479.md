# P615: review of the P479 Tinker fixes and P597 follow-up

Reviewed 2026-10-25. Documentation only. No code changed.

## Result

Five findings: one high and four medium. The highest priority is the Docker lock identity: the prune can run under a builder's existing lock and then release that lock. The timeout wrapper also has an unbounded output wait. Mail suppression works with the current exact `briefs` setting, but some suppressed events are deleted, the brief loses Tinker question details, and surrounding spaces can bypass the mail switch.

P597's note records merge verification and tests, with no implementation changes. It does not repair these gaps. Findings 1 and 2 concern new P479 code. Findings 3 through 5 include behavior already present in the saved pre-P479 scripts; they are remaining gaps in the behavior P479 says it delivers, not regressions introduced by P597.

## Findings

### 1. High: the prune can borrow and release a builder's lock

Location: `D:\UO\golem\DockerPrune.ps1:79` and `:82`. Supporting code: `Use-GolemLock.ps1:25`, `Golems.ps1:152-164`, `Golems.ps1:854-859`, and `Golems.ps1:884-889`.

The prune takes and releases `docker-build` without identifying itself as the Tinker. The lock helper invokes `golem.ps1`, which resolves an omitted identity from `GOLEM_NAME` or the registry's home Golem. A scheduled Tinker without that environment resolves to the home Golem, currently Iron in the registry I read. A manual prune started from a builder's session can inherit that builder's identity instead.

`Enter-GolemLock` treats an existing lock with the same owner as a renewal, without comparing sessions. If Iron is building, the scheduled prune can therefore report success immediately, run alongside the build, and release Iron's lock in its `finally` block. Another builder can then acquire the supposedly free lock while the original build is still running. This defeats the serialization intended to keep cleanup away from builds and image handoffs.

Evidence: an isolated call to the actual lock functions, with file operations stubbed, started with an Iron lock belonging to session `builder`. Taking it as Iron/session `pruner` returned `Ok=true`, `Why=renewed`; the pruner's release deleted the simulated lock while the recorded session still said `builder`. No real lock or Docker operation was touched. This confirms the lock collision, not deletion of an image used by a real container.

Fix: give the prune an explicit identity distinct from builders on both take and release, and make lock acquisition/release distinguish independent sessions or lease tokens. Do not let a second process renew or release another process's build lease merely because the Golem name matches. Cover a builder-held lock using the real lock logic; the current P479 prune fact substitutes a Boolean lock hook and cannot expose this collision.

### 2. Medium: the hard timeout ends before output collection ends

Location: `D:\UO\golem\TinkerLib.ps1:89-91`.

`Invoke-TinkerLimited` limits the first `WaitForExit`, but then waits on `ReadToEndAsync().Result` without a deadline. A child process can inherit stdout or stderr and remain alive after its parent exits. In that case the first wait succeeds, the timeout branch never runs, and output collection blocks until the child closes the pipe. The local-script path uses this same helper. All direct Tinker SSH and SCP invocations I found enter the wrapper, but their complete wrapper call is not guaranteed to return within its limit.

Evidence: under Windows PowerShell 5.1, I called the actual helper with `TimeoutSec=1` and `cmd.exe /d /c "start /b ping.exe -n 7 127.0.0.1 & exit /b 0"`. The parent exited promptly, but the call took 6.21 seconds and returned `TimedOut=false`, `Code=0`. The child contacted loopback only and ended on its own. No SSH connection was made.

Fix: apply one wall-clock deadline to process exit and both output tasks. If output is still open at the deadline, return a timeout and dispose the streams. Use process containment that can clean up descendants even after the original parent exits. Add a case where the parent exits but a child keeps an output handle; the existing hung-parent case does not cover it.

### 3. Medium: suppressed outbox events are deleted rather than held

Location: `D:\UO\golem\TinkerMail.ps1:410-411`. Related P479 fallback: `golem.ps1:375-377`.

The immediate-send branch handles all `reply` events and every event when `tinkerOnlyMail=false`. It calls `Send-TinkerMail` and unconditionally removes the event. In `mailMode=briefs`, that sender returns without sending. An emailed-command reply is therefore lost even with the normal `tinkerOnlyMail=true`. With `tinkerOnlyMail=false`, the new Golem fallback writes a finish into the outbox, but the Tinker deletes it here and never generates a brief because brief generation also requires `tinkerOnlyMail`. P479's promise that this fallback news reaches the next brief is not fulfilled for that combination.

Evidence: isolated calls to the actual mail-round and sender functions, with settings and file operations stubbed, reproduced both cases: `Sent=0`, the event was deleted, `Held=0`, and no brief was generated. The immediate-send branch also exists in `TinkerMail.ps1.bak-20261025-P479:407`; P479 adds another path into it rather than introducing the branch itself.

Fix: decide whether an event is sent, held, or dropped before consuming it. In briefs mode, hold replies and fallback events for a brief, and allow scheduled briefs for that mode even if direct Golem routing is disabled. Have the sender report delivery status so a suppressed or failed send cannot be treated as delivery. Verify consumption through a full mail round, not just creation of the fallback event.

### 4. Medium: the brief says a Tinker question exists but omits the question

Location: `D:\UO\golem\TinkerLib.ps1:485`. Rendering: `TinkerMail.ps1:249-258` and `:357-363`.

`Add-TinkerQuestion` keeps the cause, proposed action, and choices in `Round.questions`, but its problem record stores only a generic subject. `Get-TinkerOpenQuestions` reads question files and remote question summaries, not `Round.questions`. The brief's remaining problem line therefore says only that the Tinker has a question about a Golem. In briefs mode the detailed immediate email is suppressed, so the brief never tells Chase what decision is needed.

Evidence: I added a fabricated Copper question with cause `disk check is failing`, action `retry the disk check`, and choices `retry` and `wait`, then rendered a brief using the actual functions. The round contained the complete question. The brief contained none of the cause, action, or choices, only `the Tinker has a question about Copper`. The saved pre-P479 implementation has the same incomplete problem record at `TinkerLib.ps1.bak-20261025-P479:426`.

Fix: include the Tinker's current questions when building Waiting on you, or persist their complete content in a form the brief reads. Deduplicate that entry against its generic problem record. Require the brief fact at `tests\Tinker.Tests.ps1:696` to check the cause, action, and choices; it currently checks only `question about Copper`.

### 5. Medium: the console and senders interpret mailMode differently

Location: `D:\UO\golem\TinkerLib.ps1:456-457`. Other senders: `golem.ps1:336` and `:374-375`. Console: `ShatteredLegacy\scripts\Shard-Console.ps1:4979`.

The console trims and lowercases `mailMode`, but the senders compare the untrimmed string. With `"mailMode": " off "`, the console displays `off (no email at all)` while the sender treats it as neither off nor briefs and sends mail. The same mismatch lets `" briefs "` send immediate problems. Case alone is not the issue because PowerShell's equality comparison here ignores case.

Evidence: the actual `Send-TinkerMail` function, with only settings reads and the final mail transport stubbed, invoked the mail hook once for `" off "`. The current real setting is exact `briefs`, so this is a configuration-dependent defect, not evidence that today's setting leaks mail. The untrimmed gate already exists at `TinkerLib.ps1.bak-20261025-P479:399-400`.

Fix: normalize and validate the mode once in a shared settings helper used by the console and every sender. Cover surrounding whitespace, uppercase, missing, and unknown values with the same expected policy.

## Checks and limits

The image selector at `DockerPrune.ps1:44-57` protects image IDs used by containers, image names used by containers, `latest`, `good-*`, and an image carrying one of those kept tags. `Invoke-DockerPrune` reads running and stopped containers and inspects their actual image IDs before selection. I did not confirm a rule that selects an image already reported as in use. The lock failure above is a separate verified defect. Actual Docker removal behavior, concurrent builds, and remote process cleanup after an SSH disconnect remain unverified because I did not run Docker or connect to another PC.

The new question keys at `TinkerLib.ps1:479` and `:482` no longer depend on changing cause text. The day/Golem/prompt key plus the open-problem guard handles the reported repeated prompt-less question. I found no remaining changing-cause repeat in that path. This does not resolve the missing question details in finding 4.

Read the P479 note, both matching P597 notes including its earlier Codex review, and the relevant implementation and facts in:

- Shared kit: `DockerPrune.ps1`, `Prune-Docker.ps1`, `TinkerDocker.ps1`, `TinkerLib.ps1`, `TinkerMail.ps1`, `Tinker.ps1`, `golem.ps1`, `README.md`, and the named settings fields in `settings.json`.
- Shared-kit facts: `tests\Tinker.Tests.ps1` and `tests\Golem.Tests.ps1`, especially their P479 cases.
- Dependencies: `Golems.ps1`, `Use-GolemLock.ps1`, `Tinker-Hidden.vbs`, `Kit.ps1`, and `GolemOutbox.ps1`.
- This code checkout: `scripts\Shard-Console.ps1` and `scripts\tests\Shard-Console.Tests.ps1`, especially their P479 settings paths.
- Attribution: the saved P479 backups of `TinkerLib.ps1`, `TinkerMail.ps1`, and `golem.ps1`.

The shared kit is outside these task branches and is mutable. This review describes the files read on this date, not an independently reconstructed historical kit release. The earlier P597 repository-only review explicitly did not inspect those external scripts.

Validation used local PowerShell 5.1 probes of existing functions with fabricated inputs and stubbed side effects. No regression tests or code changes were added, so no new test gate needed a red/green cycle. I did not rerun the full suites, launch a real Tinker round, send mail, prune Docker, connect to Haven, or commit anything. Historical test totals in P479 and P597 were not independently reverified.

Ran `tools/progress.py --dry-run` with both checkout paths supplied; it exited 0. Despite its dry-run switch it rewrote `tools/progress.json`. That incidental output was restored byte for byte from the initially clean checkout so this task leaves only this review note.

The explicit lane instruction names this note `cc-P615-review-tinker-fixes-p479.md`; that destination takes precedence over the shorter name in the embedded work section.

P615 DONE
