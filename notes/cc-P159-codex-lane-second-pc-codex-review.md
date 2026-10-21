# Codex review: P159

CC task P159: The Codex lane on the second PC (wife's gaming PC, nights or on request). Reviewed by Codex (`codex exec review`, read-only) after P159 DONE and before the Golem's commit, 2026-10-21 06:11.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The required desktop send button rejects lanes running on the second PC. External lane-package changes were outside this review's scope, and PowerShell execution verification was blocked by the environment's language-mode restriction.

- **medium** [P2] Route the desktop send action to remote Codex lanes (`scripts\Shard-Console.ps1:5910`)
  When the Codex lane is on the second PC, the new desktop button cannot reach this plan: `Get-GolemPickRows` marks another machine's Golem unusable, and `Get-GolemActionConfig` refuses it before calling `Get-AutopilotPlan`. Consequently, selecting Agapite or Verite and clicking ???Send to the second PC??? runs nothing???the exact configuration P159 requires. Add a remote dispatch path for this action rather than relying on the existing local-only picker flow; the new test bypasses that flow by calling `Get-GolemScopedConfig` directly.

(0.8 minutes, 221,603 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The only change in this repository is the new task note; the implementation outside this repository was not verified. The note documents two unmet owner-activity requirements while declaring the task DONE.

- **high** [P1] Do not equate idle CPU priority with stopping within two minutes (`notes\cc-P159-codex-lane-second-pc.md:209`)
  When she returns mid-run, requesting a cooperative stop and later lowering CPU priority does not guarantee the required stopping point within two minutes. The process can continue running tools, consuming memory and performing disk I/O indefinitely. The claim that this meets the deadline is therefore unsupported, especially since the notes say Codex itself was never exercised. Implement and verify bounded stopping, or report this requirement as unfinished rather than DONE.
- **medium** [P2] Publish partial work and release the claim on owner activity (`notes\cc-P159-codex-lane-second-pc.md:203`)
  The documented pause behavior explicitly omits the required partial push and claim release. If her PC stays busy or goes offline after pausing, the work remains only on that PC and the prompt remains unavailable elsewhere; the documented stale-claim policy also exempts paused claims. Preserve resumable session information if useful, but publish the partial branch and release ownership as requested, or obtain approval for this change before declaring P159 complete.

(0.6 minutes, 99,670 tokens)
