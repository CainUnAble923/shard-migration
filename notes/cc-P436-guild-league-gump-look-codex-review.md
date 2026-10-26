# Codex review: P436

CC task P436: a new look for the guild and League gumps from art we already have (pick first, then b. Reviewed by Codex (`codex exec review`, read-only) after P436 DONE and before the Golem's commit, 2026-10-25 21:13.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The shared helper and registered art implement most of look B, but the fallback does not protect older patched clients, and two guild menus were missed. Build results were reported in the implementation notes; this review did not rerun them.

- **high** [P1] Verify frame availability before selecting custom art (`server\customizations\GuildStyle.cs:48`)
  Players using an older Shattered Legacy package also acknowledge ClientCommand, but lack gumps 23200???23208. This check therefore sends them invisible backgrounds and removes their stock panels instead of falling back. Publishing the package first does not update clients already running or players bypassing the launcher, and the global kill switch cannot distinguish them. Gate this on a frame-specific capability or package version, and test an older patched client explicitly.
- **medium** [P2] Include the remaining Miners' Compact gumps (`server\tests\Misc\GuildStyleVerification.cs:53`)
  The inventory omits `ProspectorsLogbookGump` and `SurveyArchivistGump`, which remain direct `Gump` subclasses drawing frame 9270, alpha interiors and rules 9304. These are Miners' Compact discovery/reporting menus; the newly styled `CombinedLogbookGump` directly opens the former. Consequently these guild pages retain stock styling even with the new package. Move both onto the shared helper and include them in the inventory and opening tests.

(1.5 minutes, 558,635 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). No actionable defects found in this repository???s changed notes and four new helper scripts. The notes document look B, implementation, verification, and limitations; server and package changes are outside this review???s diff, so their correctness and reported test results were not independently verified.

No findings.

(0.8 minutes, 151,397 tokens)
