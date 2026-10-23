# Codex review: P281

CC task P281: the guilds' real halls (F-49): place them on the test world from P151's survey and Cha. Reviewed by Codex (`codex exec review`, read-only) after P281 DONE and before the Golem's commit, 2026-10-23 00:36.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The implementation substantially covers the requested halls, travel notes, test-only guard, and screenshot evidence. However, ordinary door use and subsequent sign generation expose two repeat-placement defects. Build and client verification were not rerun during this read-only review.

- **medium** [P2] Reconcile stock signs when the guild sign already exists (`server\customizations\ClusterFGuildHallPlacement.cs:187`)
  If staff runs `[SignGen` after placing the halls, pinned `SignParser.Add_Static` deletes the hidden stock `Sign` and creates a visible replacement at the same location. The guild sign survives, but now overlaps the stock sign, and rerunning `place` skips this branch without hiding or remembering the replacement. Reconcile the stock sign even when the guild sign already stands, so the replacement-sign behavior remains correct after normal world setup commands.
- **medium** [P2] Identify existing doors by their closed position (`server\customizations\ClusterFGuildHallPlacement.cs:151`)
  If either new hall has an open door when `place` runs again, this lookup misses it: pinned `BaseDoor.OnOpenChanged` moves the door by its `Offset`. The seeder consequently creates another closed door in the same doorway and relinks the replacement front doors, leaving the originals behind. Compare against the door's closed position (accounting for `Open` and `Offset`) and cover rerunning placement with doors open.

(1.2 minutes, 717,569 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The notes and screenshots cover the requested halls and waiting Maritime placement, but the generator's repository override bypasses validation of its actual input. This review covers the docs-repository changes; the separate server implementation and reported build results were not independently verified.

- **medium** [P2] Validate the same repository that supplies the generated data (`notes\cc-P281-tools\gen.py:129`)
  When invoking the documented `gen.py <repo>` form with a repository other than Iron's work copy, `build()` reads that repository's design, but this subprocess still checks the hard-coded Iron design and decor templates in `check.py`. Consequently, valid Iron placements can authorize generating unchecked placements into the selected repository; if Iron's work copy is removed, generation fails altogether. Pass the selected design and repository paths through to the checker so the gate validates the data actually being generated.

(1.6 minutes, 657,287 tokens)
