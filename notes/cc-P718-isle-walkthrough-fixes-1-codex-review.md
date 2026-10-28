# Codex review: P718

CC task P718: fixes from Chase's walk of Tutorial Island (round 1). Reviewed by Codex (`codex exec review`, read-only) after P718 DONE and before the Golem's commit, 2026-10-28 09:39.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.95). Most requested mechanics are implemented, but existing seeded copies do not receive the new physical fixes, and required NPC greetings remain incomplete. Build and runtime gates were not independently executed during this read-only review.

- **medium** [P2] Add approach greetings for the remaining required NPC interactions (`server\customizations\Tutorial\TutorialGreeting.cs:97`)
  Item 1 also requests greetings for other isle NPCs that require double-clicking, but the integration covers only Tamsin, Wren and Elara. `TutorialDeathEcho` requires a double-click to start the death lesson and has no approach greeting; Sera likewise has no double-click instruction on approach for the resurrection interaction. The existing lesson hints do not supply the requested NPC overhead greetings. Extend the greeting predicates and hooks to these required interactions.
- **medium** [P2] Upgrade already-seeded copies with the new lesson props (`server\customizations\Tutorial\TutorialCopies.cs:128`)
  When loading an existing world, copies with `Seeded == true` and a nonempty `Placed` list never run the updated seeder. Consequently, returning trainees???and new trainees assigned a previously seeded free copy???still have no clothes table or field gate and retain the old signposts. `OnLogin` also preserves current copies without reseeding. Add an idempotent upgrade path for existing copies rather than relying on their eventual vacancy reset.

(3.4 minutes, 1,188,428 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.84). No actionable defects found in this repository???s notes and supporting scripts. The recorded tests and bot run support the reported work; the separate server implementation is outside this diff, so this verdict does not independently validate it.

No findings.

(1.2 minutes, 485,678 tokens)
