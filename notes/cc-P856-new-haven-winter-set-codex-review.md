# Codex review: P856

CC task P856: port a winter set for New Haven before December 1. Reviewed by Codex (`codex exec review`, read-only) after P856 DONE and before the Golem's commit, 2026-11-10 09:14.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The port implements most requested content, but omits the seasonal inn fireplace and introduces restart behavior that reverses area-specific staff clears. Build and in-game results were documented in the companion notes; I did not independently rerun them.

- **medium** [P2] Preserve area-specific staff clears across restarts (`server\customizations\ClusterFWinterDecorSeeder.cs:271`)
  If staff run `winter clear park` or `winter clear square` during winter while other decorations remain, the next restart recreates the cleared addons. `LastAutomatic` remains true, and this loop treats deliberately cleared rows as missing upgrade content. This breaks the existing seasonal switch's promise that staff clears stand until the season changes. Persist whether these rows have already been introduced, or remember explicit clears, rather than replenishing every absent row on every load.
- **medium** [P2] Complete the requested seasonal inn fireplace placement (`server\customizations\WinterSet\ClusterFWinterSetLayout.cs:38`)
  The seasonal layout contains only four designs and never places the holiday fireplace. Consequently, neither December 1 placement nor the load-time top-up can deliver the requested fireplace in main's inn; selling its deed does not satisfy that requirement. The notes explain the space constraint, but this remains an unapproved omission from the task. Provide a workable inn layout or obtain approval for the reduced scope before marking it complete.

(1.5 minutes, 343,522 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The artifacts document successful builds and proof-shard screenshots, but an explicit deliverable???the holiday fireplace placed seasonally in both inns???is missing. Review of the main implementation is limited because its code changes are outside this repository.

- **medium** [P2] Complete the requested fireplace placement in both inns (`notes\cc-P856-new-haven-winter-set.md:116`)
  The task explicitly requires the holiday fireplace in the inn in both New Havens, but this delivery only adds its Festival deed; the release patch also omits its seasonal row. The space constraints explain the omission but do not constitute approval to drop that requirement. Resolve the furnishing conflict and verify both placements, or obtain an explicit scope reduction before marking P856 complete.

(2 minutes, 788,439 tokens)
