# Codex review: P663

CC task P663: The tutorial moves to the isle, with the start choice (P481 F3). Reviewed by Codex (`codex exec review`, read-only) after P663 DONE and before the Golem's commit, 2026-10-27 08:37.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). Most requested behavior is implemented, and the notes document approval to defer the client playthrough. However, dock surface placement blocks seeding against the planned map, staff can spawn at display-only sea coordinates, and starting-location centralization is incomplete. Runtime tests were not rerun during this review.

- **high** [P1] Resolve the dock's walking surface instead of its underlying land (`server\customizations\Tutorial\TutorialWorld.cs:73`)
  The planned dock has planks at Z 0 over water at Z -5 (`cc-P481-tools/newisle.py`), but `GetAverageZ` reads only land. Consequently, the dock marker and moongate are positioned underwater, and the seeder's `CanFit` preflight rejects these positions because they intersect the deck. Resolve the static walking surface for dock placements; otherwise the tutorial cannot be seeded even with the planned island patch loaded.
- **medium** [P2] Route the tutorial-disabled start through HavenSpots too (`server\customizations\CharacterCreation.cs:134`)
  The tutorial-enabled list uses HavenSpots, but the fallback immediately below still constructs New Haven with literal `(3503, 2574, 14)` coordinates. This misses the prompt's explicit single-source requirement: changing HavenSpots for S7 will relocate tutorial skips and gate exits while ordinary character creation with the tutorial disabled still starts at the old town. Construct the fallback entry from HavenSpots as well.
- **medium** [P2] Give staff a real start instead of the island's display coordinates (`server\customizations\Tutorial\TutorialStart.cs:122`)
  When a staff account creates a character with the default Tutorial Island selection, this branch returns the city's display-only sea coordinates `(3650, 2932, -5)` on Trammel. CharacterCreation then actually places the character there, and login deliberately does nothing for staff. Keep staff exempt from tutorial enrollment, but resolve this display entry to a real starting location.

(3.4 minutes, 1,542,909 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.78). No actionable bugs found in this repository's new notes, helper scripts, and failure summaries. The notes explicitly record the deferred play-through and screenshots. Server implementation and build claims cannot be independently verified from this docs-only diff.

No findings.

(0.7 minutes, 162,422 tokens)
