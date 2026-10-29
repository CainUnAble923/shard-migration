# Codex review: P679

CC task P679: Moongates, teleporters and the staff go-menu (SoS swap S4). Reviewed by Codex (`codex exec review`, read-only) after P679 DONE and before the Golem's commit, 2026-10-28 20:09.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.86). The changes implement the requested gate placements, teleporter replacements and author-derived staff go-menu, with documented client and build evidence. No actionable regression was found. The teleporter land check passed independently; the full build and client checks were not rerun in this read-only review.

No findings.

(0.9 minutes, 391,085 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The work substantially implements the requested swap, but its teleporter placement and proof overlook reverse sources created by back-enabled entries. The teleporter fact passes despite retaining reverse teleporters that cannot activate on changed SoS terrain.

- **medium** [P2] Check reverse teleporter sources when back is enabled (`notes\cc-P679-tools\tele_fix.py:66`)
  For entries with `back: true`, `GenTeleporter.TeleportersCreator.CreateTeleporter` also creates a source at `dst`, but this condition checks firing only for `src`. Consequently, the generator and new map fact accept nonfunctional reverse teleporters. For example, the retained destinations at 2041,215,14 and 2042,215,14 on both facets occupy SoS-changed tiles whose lowest open floor is Z 15, so their reverse teleporters never fire. Treat `dst` as a source when `back` is enabled in both the placement decisions and verification.

(1.7 minutes, 709,403 tokens)
