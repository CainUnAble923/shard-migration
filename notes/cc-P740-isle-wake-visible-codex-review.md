# Codex review: P740

CC task P740: isle wake easier to see, bandages for the healing lesson, Echo off the isle. Reviewed by Codex (`codex exec review`, read-only) after P740 DONE and before the Golem's commit, 2026-10-31 00:51.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The change substantially implements the requested wake and healing improvements, with documented client proof and release compatibility. However, sustained movement can defeat the slow get-up, and the table's anti-hoarding limit does not survive restarts. Tests were not independently rerun during this read-only review.

- **medium** [P2] Persist the table's bandage allowance (`server\customizations\Tutorial\TutorialFarm.cs:408`)
  The anti-hoarding allowance disappears on every server restart because `_tableTaken` exists only in memory. A character can leave the healing lesson unfinished, bank or transfer each issued stack, exhaust the allowance, and receive another allowance after each restart. These are ordinary transferable `Bandage` items, so checking only the backpack does not prevent stockpiling. Persist the table issuance count with tutorial progress, as the existing Wren supply does with `BandagesIssued`, so the requested per-player limit survives restarts.
- **medium** [P2] Preserve the get-up animation across repeated movement input (`server\customizations\Tutorial\TutorialWake.cs:263`)
  If the player holds a movement key or keeps right-clicking to walk, subsequent movement attempts interrupt the get-up, but this early return prevents another resend. TazUO's `Mobile.EnqueueStep` resets the animation when starting movement, and the ClassicUO rejection behavior described in the proof notes also applies to subsequent refused moves. The single 100 ms resend therefore only protects an isolated first input: normal sustained movement can leave the character standing immediately while the server waits out the rise timer. Handle continued input without cancelling the visible get-up, and verify that interaction in both clients.

(1.5 minutes, 639,940 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.85). No actionable defects found in the documentation and proof tools in this repository. The recorded build and play-through results support the notes; server implementation changes are outside this diff and were not reviewed.

No findings.

(0.9 minutes, 596,390 tokens)
