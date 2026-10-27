# Codex review: P709

CC task P709: design: quest-gated Chivalry and Necromancy, and fewer skill choices at character crea. Reviewed by Codex (`codex exec review`, read-only) after P709 DONE and before the Golem's commit, 2026-10-27 14:27.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.93). The note substantially covers the requested design and clearly separates proposals from verified behavior. However, the mandatory tithing objective has a progression deadlock for characters who already have a full tithing balance.

- **medium** [P2] Provide a tithe-step fallback for characters at the points cap (`notes\cc-P709-gated-skills-and-start-choices.md:73`)
  A character who fills their tithing balance before this step cannot complete the initiation. Pinned `Gumps/TithingGump.cs` caps the balance at 100,000 and refuses further donations when full, while this design rejects existing balance as evidence and prohibits Chivalry casting before completion, preventing the player from spending those points. Define an alternative completion path for a capped balance, or another explicit way to perform the required donation without first unlocking Chivalry.

(1 minutes, 298,164 tokens)
