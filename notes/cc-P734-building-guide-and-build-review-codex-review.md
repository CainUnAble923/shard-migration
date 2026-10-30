# Codex review: P734

CC task P734: a building and decorating guide, and a render review before build work merges. Reviewed by Codex (`codex exec review`, read-only) after P734 DONE and before the Golem's commit, 2026-10-29 20:47.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The reusable builds and placement tests are present, but ClearBuild can delete unrelated world items and leave opened doors behind. The Golem changes outside this repository were not verified in this review.

- **medium** [P2] Include open doors and gates when clearing a build (`server\customizations\Builds\PlaceBuild.cs:111`)
  If a practice building's door or farmhouse gate is open when ClearBuild runs, its location has shifted by the door's opening offset. Searching only the saved closed-position tile leaves it behind after the surrounding build is removed. Resolve doors by their closed location as well as their current location, and cover an open door in the removal test.
- **medium** [P2] Restrict clearing to items belonging to the saved build (`server\customizations\Builds\PlaceBuild.cs:115`)
  When a build overlaps existing decoration, this deletes every immovable item at each listed coordinate, regardless of its type or item ID. For example, clearing a floor tile also deletes an unrelated chest or spawner at the same position. Track placed items or match the expected pieces rather than treating a coordinate match as ownership; the current test only protects movable gold and misses this destructive case.

(1 minutes, 306,507 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The submitted artifacts omit the tracked walking proof and contain an incorrect stock-art placement instruction. The external Golem implementation and code-repository changes are outside this diff, so their correctness could not be verified here.

- **medium** [P2] Replace the stone-wall ID advertised as red fire (`notes\guides\building-and-decorating.md:939`)
  A builder following this mandatory stock-art lookup will place a stone wall rather than fire: reading `D:\UO\UltimaOnlineVanilla\tiledata.mul` identifies item `0x0026` as an eight-high `stone wall`. Correct the entry to a verified fire item ID; labeling this value ???verified (code)??? propagates incorrect placement instructions, contrary to the source-verification requirement in [AGENTS.md:58???60](../../AGENTS.md#L58-L60).
- **medium** [P2] Preserve the walking evidence in tracked review artifacts (`notes\cc-P734-practice\gallery.md:5`)
  The referenced walking evidence will disappear when this work merges: every file in `notes/cc-P734-review/walks/` ends in `.log`, and `git check-ignore -v` confirms that `.gitignore:11` excludes them. Consequently, another lane cannot verify the bidirectional stair, bridge and door walks from the committed artifacts. Export the relevant step traces into tracked Markdown evidence instead of force-adding runtime logs, respecting [AGENTS.md:80](../../AGENTS.md#L80).

(2.5 minutes, 1,044,734 tokens)
