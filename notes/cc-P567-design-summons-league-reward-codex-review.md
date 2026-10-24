# Codex review: P567

CC task P567: design: summons as a high League rank reward. Reviewed by Codex (`codex exec review`, read-only) after P567 DONE and before the Golem's commit, 2026-10-24 17:07.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The note substantially fulfills the requested design scope, but its no-reward implementation contract overlooks an existing deletion-event achievement path. That concrete integration gap should be resolved before treating the design as build-ready.

- **medium** [P2] Include the pet-death achievement exclusion in the design (`notes\cc-P567-design-summons-league-reward.md:149`)
  When lethal damage deletes an Echo while its owner is at full health, the proposed flags do not prevent rewards: `ClusterFNotedBySystem.OnCreatureDeleted` calls `OnCreatureDied` for zero-hit creatures, which notifies `PetDiedAtFullHp` before checking `Summoned`, without checking `NoKillAwards`. This can award Acceptable Losses and Meat Shield Procurement, including AP, Renown, and an item. Add an explicit exclusion and its edit point to the implementation plan, rather than claiming the existing summon/no-awards flags suffice.

(0.8 minutes, 336,842 tokens)
