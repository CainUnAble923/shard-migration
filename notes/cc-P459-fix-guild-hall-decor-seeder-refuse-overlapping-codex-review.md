# Codex review: P459

CC task P459: guild hall decor seeder: refuse overlapping or out-of-date placements; test the real d. Reviewed by Codex (`codex exec review`, read-only) after P459 DONE and before the Golem's commit, 2026-10-24 20:47.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The main requested protections and real-JSON test are implemented, but stale-template detection misses some edits and doorway preflight has correctness gaps. The hall placer also reports rejected decor as successfully placed. Build and test results were not independently rerun during this read-only review.

- **medium** [P2] Recognize open tower doors during placement preflight (`server\customizations\GuildHallDecor\GuildHallDecorSeeder.cs:239`)
  The newly introduced `GuildHallDecorDoor` does not derive from `BaseDoor`. While it is open, its nodraw item is also non-impassable, so neither this branch nor the subsequent item check recognizes its doorway. Another decor set can therefore be placed directly in the open tower entrance; the door subsequently closes over it because its closing check only considers mobiles. Treat tower doors as reserved doorways even while open.
- **medium** [P2] Exclude refused decor from the hall placer's success count (`server\customizations\ClusterFGuildHallPlacement.cs:242`)
  When the new preflight refuses a hall's decor, this branch prints the refusal but leaves the decor entry already added to `did`. The following hall summary and final count still report that decor as placed, despite nothing being created. Only add successful placements to `did`, and run the same preflight during dry runs so they do not promise placements the real run rejects.
- **medium** [P2] Restrict doorway conflicts to overlapping elevations (`server\customizations\GuildHallDecor\GuildHallDecorSeeder.cs:239`)
  When a door occupies the same X/Y on another storey, this branch rejects the placement regardless of Z. The swing check below likewise ignores elevation. Consequently otherwise valid upstairs or downstairs decor is refused even though it cannot obstruct the door. Apply vertical intersection checks to both door cases, as the static and impassable-item checks already do.
- **medium** [P2] Reject stale placements whose group was removed or renamed (`server\customizations\GuildHallDecor\GuildHallDecorSeeder.cs:111`)
  When a template edit removes or renames a group, this loop never examines the items carrying its old group key. Re-running the whole set therefore succeeds and leaves the obsolete group standing; a renamed group can also be placed alongside its old copy because same-anchor items are exempt from overlap checks. Compare existing group keys against the requested full template and require clearing obsolete groups.
- **medium** [P2] Include the placed item name in the template hash (`server\customizations\GuildHallDecor\GuildHallDecorSeeder.cs:74`)
  A name-only template edit leaves this hash unchanged, although the constructor copies `Row.Name` into the saved item. Re-running then skips the existing rows rather than requesting a clear, leaving outdated names indefinitely. Include `Name` in the hash so changes to every persisted row attribute trigger the stale-template protection.

(1.5 minutes, 412,526 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.8). No actionable defects found in this repository???s generator changes, rendering helper, notes, or rendered tower. The server implementation and reported build/test results are in the separate code repository and could not be verified from this diff.

No findings.

(0.4 minutes, 144,893 tokens)
