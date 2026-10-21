# Codex review: P371

CC task P371: graduating from the New Haven island tutorial is the first real loop, and opens the is. Reviewed by Codex (`codex exec review`, read-only) after P371 DONE and before the Golem's commit, 2026-10-21 16:07.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The graduation, loop counter and cap hook largely implement the requested behavior. However, transport refusals can strand pets off-island, and disabling the tutorial leaves new players without an escape path. The official build was not run during this review.

- **medium** [P2] Provide an escape path when the tutorial is disabled (`server\customizations\Tutorial\TutorialIslandGate.cs:27`)
  With the existing `tutorial.enabled=false` setting and the new island gate left at its default, new players become trapped permanently without staff intervention. `OnLogin` does not enter them into the tutorial, leaving their record `NotStarted`; the recruiter offers neither graduation nor skipping in that state, while this predicate still blocks every exit. Coordinate these settings or provide a player-accessible waiver so disabling the tutorial does not strand new characters.
- **medium** [P2] Refuse transport before moving the player's pets (`server\patches\PlayerMobile-tutorial-island-gate.patch:16`)
  When a loop-0 player uses an off-island moongate, teleporter or stuck-help transport with following pets, the pets leave while the player remains behind. Pinned `Moongate.UseGate`, `Teleporter.DoTeleport` and `StuckMenu.TeleportTimer` call `BaseCreature.TeleportPets` before `MoveToWorld`, so this guard runs too late. Add destination preflight to those routes before their pet transport, and test refusal with a following pet.

(4.7 minutes, 651,894 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). No actionable defects found in this repository???s changes. The P80 corrections and P371 notes reflect the requested decision, with governing-doc updates queued for promotion. Server code, tests, CHANGELOG and VERSION are outside this diff, so their correctness and completion could not be verified.

No findings.

(0.5 minutes, 92,641 tokens)
