# Codex review: P773

CC task P773: in-game play test tasks for the three testers ([tasks, [report, the Play Test Goblin). Reviewed by Codex (`codex exec review`, read-only) after P773 DONE and before the Golem's commit, 2026-11-02 05:44.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The implementation substantially covers the requested tester management, in-game reporting, Goblin assignment rules, and release artifacts. However, pending email notifications can be lost, and dry runs can send and delete real email.

- **medium** [P2] Stop dry runs before processing pending email (`scripts\Run-PlayTestGoblin.ps1:47`)
  When `goblin-mail.txt` remains from an earlier failed delivery, invoking this wrapper with `-DryRun` still sends that email and deletes it. The switch only reaches Python; the wrapper continues into its normal delivery path. This makes the documented preview command perform an external action and consume pending state. Exit before email handling when `$DryRun` is set.
- **medium** [P2] Preserve pending notifications when generating the next email (`scripts\playtest_goblin.py:272`)
  If SMTP fails or email is not configured, the wrapper deliberately leaves the email for retry. However, the next run with new reports or assignments overwrites that pending email here. Since `reportsSeen` already advanced, the previous reports will never appear in a subsequent email, so Chase misses their notification. Queue or merge unsent notifications rather than replacing them.

(2.7 minutes, 1,059,470 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.9). The release artifact contains a report-submission error path that resets the selected task and loses entered evidence. The notes and recorded gates otherwise cover the requested deliverables, although this repository does not contain the console and Goblin implementation changes themselves.

- **medium** [P2] Preserve the current task and text when submission fails (`notes\cc-P773-tools\p773-release-isle-20261028.diff:797`)
  When a tester presses a problem button without text on the second or third task, `Answer` returns false, but the unconditional `ShowTasks` rebuilds the window on the first task. The instruction to add words and press again can therefore lead to evidence being submitted against the wrong task. A report write failure also discards the entered text. Handle the return value and redisplay the same task with its text retained when submission fails.

(0.9 minutes, 208,916 tokens)
