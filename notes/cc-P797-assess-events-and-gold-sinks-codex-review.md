# Codex review: P797

CC task P797: assess events, minigames and gold sinks. Reviewed by Codex (`codex exec review`, read-only) after P797 DONE and before the Golem's commit, 2026-11-05 13:19.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The assessment substantially covers the requested items, rankings and recommendations, but its required terms assessment overlooks explicit author restrictions in both casino packs. No game code was changed.

- **medium** [P2] Record the casino author's explicit permission restrictions (`notes\cc-P797-assess-events-and-gold-sinks.md:27`)
  The blanket terms assessment misses restrictions embedded in both casino downloads: `CEOBlackJack.cs:2102-2106` prohibits copying, reproduction or distribution without express permission and requests contact plus $20 for shard use; `HiLoCards.cs:1225-1229` contains the equivalent $10 notice. Consequently, credit and private-repo distribution are not established permissions. Record these terms for both packs and distinguish an independent behavioral rebuild from reuse of their implementation. This also follows the source-over-documentation requirement in [AGENTS.md:58-60](../AGENTS.md#L58-L60).

(1.4 minutes, 370,758 tokens)
