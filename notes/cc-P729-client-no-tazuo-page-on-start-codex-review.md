# Codex review: P729

CC task P729: the player package must not open TazUO's own page at start. Reviewed by Codex (`codex exec review`, read-only) after P729 DONE and before the Golem's commit, 2026-10-28 20:25.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.91). The launcher seeds fresh profiles with the client's version, matching TazUO's condition for suppressing its Version History gump, while preserving existing character profiles and player-saved defaults. The change includes regression tests, a changelog entry, and the requested notes. Runtime login behavior was verified against source, not exercised in a real client.

No findings.

(0.8 minutes, 280,015 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.86). The documentation and recorded test outputs consistently describe the setting, fresh-profile behavior, preservation of player defaults, and red/green verification. No actionable defects were found in this repository's changes. The implementation and CHANGELOG are in the separate code repository; a real-client startup test remains explicitly unverified.

No findings.

(0.4 minutes, 89,792 tokens)
