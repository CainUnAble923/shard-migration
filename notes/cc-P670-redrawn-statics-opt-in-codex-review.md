# Codex review: P670

CC task P670: Zigholtul's redrawn statics as an opt-in look in our client. Reviewed by Codex (`codex exec review`, read-only) after P670 DONE and before the Golem's commit, 2026-10-26 18:19.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The change substantially fulfills the requested vendoring, opt-in setting, packaging, credits, and evidence requirements, and its six package facts pass. However, live switching leaves stale pixel-picking masks, so interaction no longer matches the displayed art.

- **medium** [P2] Invalidate the pixel-picking mask when switching art (`client\patches\0008-redrawn-world-art.patch:160`)
  When a player toggles the setting after an affected graphic has been displayed, `Art.Invalidate` clears only its sprite. Reloading calls `PixelPicker.Set`, but that method returns immediately for an already-cached ID, retaining the previous image's dimensions and mask. The newly drawn trees and furniture consequently have incorrect click/target regions, and switching off can leave stock art using the redrawn mask. Invalidate or replace the corresponding picker entry along with the sprite; the current lookup-only tests do not exercise this live-switch path.

(1.3 minutes, 607,710 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.78). No actionable defects found in this repository's new notes, audit scripts, fit data, and screenshots. The client implementation, vendored PNGs, package gates, and CHANGELOG changes are in the separate code repository, so their correctness could not be verified from this diff.

No findings.

(0.8 minutes, 292,477 tokens)
