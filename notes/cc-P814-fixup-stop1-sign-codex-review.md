# Codex review: P814

CC task P814: overseer fix-up for P806 (New Haven fixes, P799 chain): its build review said FAIL. Reviewed by Codex (`codex exec review`, read-only) after P814 DONE and before the Golem's commit, 2026-11-06 10:09.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.87). No actionable bugs found in the uncommitted changes. The release diff applies cleanly, and the accompanying records include the requested sign relocation, seeded-world cleanup tests, client evidence, and successful gated builds. Builds and client walks were not independently rerun.

No findings.

(0.9 minutes, 352,138 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The sign relocation, upgrade handling, and requested evidence appear complete, and the release diff applies cleanly to the current release tip. However, its new changelog entry is hidden from the runtime parser, leaving the required player-facing release note missing.

- **medium** [P2] Move the release changelog entry outside the HTML comment (`notes\cc-P814-tools\p814-release-isle-20261028.diff:9`)
  The release diff inserts the 2026.11.06.4 section inside CHANGELOG.md's opening HTML comment, beneath `Example:`. `PatchNotes.Parse` in `server/customizations/ShardVersion.cs` skips that comment entirely, so the release's new version has no parsed patch notes and players never see the housing-sign fix in the bulletin or patch history. Move the section below the closing `-->` and regenerate the release diff.

(1.3 minutes, 596,922 tokens)
