# Codex review: P738

CC task P738: fix-up for P734 (CC task P734: a building and decorating guide, and a render review be. Reviewed by Codex (`codex exec review`, read-only) after P738 DONE and before the Golem's commit, 2026-10-30 07:35.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The recovered P734 files retain two actionable ClearBuild defects. The P738 notes document Chase's build waiver; I did not rerun the build or verify the external Golem changes.

- **medium** [P2] Restrict clearing to the saved build's actual pieces (`server\customizations\Builds\PlaceBuild.cs:115`)
  If a build overlaps existing decoration, clearing it deletes every immovable item at its coordinates, including unrelated chests, spawners or decorations. This also removes pre-existing pieces that placement skipped rather than created. Track placement ownership or otherwise distinguish the build's pieces before deleting; the current test protects only movable gold and misses this destructive case.
- **medium** [P2] Include opened doors and gates when clearing builds (`server\customizations\Builds\PlaceBuild.cs:111`)
  When a door or gate is open, ModernUO moves it by its opening offset. Searching only the saved closed-position tile therefore leaves it behind when clearing these practice builds. Search nearby doors and compare their closed locations, and extend the removal test to cover an open door.

(0.9 minutes, 312,842 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The guide resolution preserves P734's content and main's additions, but the imported review artifacts still omit the walking proof they reference. Code-repository changes and external Golem behavior were outside this review.

- **medium** [P2] Preserve the walking proof in tracked review artifacts (`notes\cc-P734-practice\gallery.md:6`)
  The referenced walking traces exist locally but are excluded by `.gitignore:11` (`*.log`), and none are tracked. After integration, another Golem cannot inspect the bidirectional stair, bridge, pier and doorway evidence supporting the PASS verdicts. Export those traces into tracked Markdown evidence rather than force-adding runtime logs, respecting [AGENTS.md:80](../../AGENTS.md#L80).

(1.1 minutes, 383,297 tokens)
