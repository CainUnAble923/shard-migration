# Codex review: P735

CC task P735: finish P688's two leftovers (bot-point proof run, New Haven start for three bot checks. Reviewed by Codex (`codex exec review`, read-only) after P735 DONE and before the Golem's commit, 2026-10-31 20:12.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.91). The changes implement the requested New Haven starts with tutorial-unlocked pool accounts. Recorded evidence confirms the bot-point proof, all three private-world checks, and build gates passed; I also reran the 8 new tests and 12 existing bot tests successfully. The changelog and required completion notes are present.

No findings.

(1 minutes, 363,087 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.91). The supplied evidence records a green point proof, three passing private-world checks, and passing gates. However, the proposed commit includes raw logs explicitly forbidden by repository instructions; the actual server-repository changes are outside this review's diff.

- **medium** [P2] Keep raw build and shard logs outside the commit (`notes\cc-P735-p688-leftovers.md:155`)
  The new files include `gated-build.log`, `gated-build-1.log`, and the runs' `shard.log` and `checks.log` files, which the Golem would commit with this directory. [AGENTS.md:80](../../AGENTS.md#L80) explicitly prohibits committing logs. Keep these raw artifacts outside the repository or in ignored scratch storage; the concise gate summaries and notes can retain the verification evidence.

(0.6 minutes, 246,699 tokens)
