# Codex review: P770

CC task P770: Gold never claims its run-next (STEPHS-DESKTOP). Reviewed by Codex (`codex exec review`, read-only) after P770 DONE and before the Golem's commit, 2026-11-02 01:10.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The recorded changes substantially address Gold's run-next delivery and demonstrate the main STOPPED-question workflow. However, remote NEEDS YOU answers no longer resume their prompts, and remote forwarding loses existing wake-control and validation behavior.

- **medium** [P2] Reject overlong answers before queuing them remotely (`notes\cc-P770-tools\p770-kit.diff:189`)
  For a free-text answer longer than 2,000 characters, the new tower-side validation accepts it, queues the command, and exits successfully. However, `Submit-GolemAnswer` on the destination rejects answers exceeding `QTextMax` (2,000), so the question remains unanswered despite the successful tower invocation. Apply the same text-length validation before enqueueing, as the local answer path already does.
- **medium** [P2] Honor NoWake when forwarding remote answers (`notes\cc-P770-tools\p770-kit.diff:198`)
  When the tower calls `Answer-Question.ps1 -NoWake` for a remote question, this branch queues an ordinary answer command and exits before reaching the existing NoWake check. The agent receives no indication that waking was forbidden and immediately starts Golem Watch after answering, which can wake the stopped prompt. Preserve the caller's wake intent through forwarding and the new Watch scheduling so answering without resuming remains possible.
- **medium** [P2] Preserve resumption for remote NEEDS YOU answers (`notes\cc-P770-tools\p770-kit.diff:213`)
  For a remote `needsyou` question whose prompt is still current, the Answer event clears NEEDS YOU but leaves `current` populated and does not create RUN-NEXT. This new early exit suppresses the previous manual SelfWake, while the replacement Watch wake requires an idle Golem with RUN-NEXT. Consequently, these answers are saved but never launch the promised continuation. Defer an explicit wake request that also handles running prompts, rather than relying exclusively on the idle run-next path.

(2.4 minutes, 580,151 tokens)
