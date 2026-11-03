# Codex review: P789

CC task P789: [tasks window readability, and no player-only tasks for staff accounts. Reviewed by Codex (`codex exec review`, read-only) after P789 DONE and before the Golem's commit, 2026-11-03 10:00.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The readability changes and release/build evidence substantially address the prompt, but legacy assignments lack the required staff warning and character-level staff can still receive player-only tasks. Actual cleanup of admin-chase's cards remains deferred to Chase, as acknowledged in the notes.

- **medium** [P2] Include character-level staff powers in the eligibility export (`server\customizations\PlayTest\PlayTestTasks.cs:704`)
  When a tester has a staff character on an account whose access level remains Player, this export reports `staff: false`, so the Goblin assigns player-only cards and the cleanup skips them. ModernUO permits character access levels independently of account access levels, and `ClusterFTutorial.TryEnter`, `TutorialStart`, and this patch's own `IsStaff` all recognize character-level staff powers. Include the account's characters when determining staff eligibility so assignment agrees with the actual tutorial restrictions.
- **medium** [P2] Show the staff warning on legacy player-only tasks (`server\customizations\PlayTest\PlayTestTasks.cs:932`)
  Existing P773 assignments, including admin-chase's cards, have no `needsPlayer` field, so they parse as null and this condition suppresses the required warning. The field is backfilled only by a normal Goblin run; neither releasing the shard nor running the cleanup backfills it. Consequently, the documented pre-cleanup check shows no warning on precisely the existing cards this requirement addresses. Treat missing eligibility conservatively, consistently with the Goblin, or migrate those tasks before displaying them.

(2.1 minutes, 691,206 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The screenshots and recorded builds support the readability changes, but the release diff misses the required warning for existing assignments without the new metadata. The real-account cleanup is explicitly deferred to Chase, and the web-console/Goblin implementation is outside this repository's diff.

- **medium** [P2] Show the staff warning on legacy player-only cards (`notes\cc-P789-tools\p789-release-isle-20261028.diff:403`)
  Existing P773 assignments, including admin-chase's G-0001, have no `needsPlayer` field, so the reader sets `NeedsPlayer` to null and this condition suppresses the required warning. After installing the release image but before running the cleanup/Goblin, staff therefore see those cards without the player-account instruction. Treat missing metadata conservatively as player-only, consistently with the documented bank policy, and cover a legacy assignment without the field in the test.

(1 minutes, 361,477 tokens)
