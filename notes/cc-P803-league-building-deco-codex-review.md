# Codex review: P803

CC task P803: New Haven League building: replace the bulletin board and a full decoration review. Reviewed by Codex (`codex exec review`, read-only) after P803 DONE and before the Golem's commit, 2026-11-07 22:08.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.85). No actionable defects found in the changed code or new tests. The supporting artifacts include before/after reviews, placement records, release diff, and successful gated-build logs. Message posting is explicitly inapplicable to the existing requisitions board; opening and reading it was verified instead. I did not rerun builds or client tests.

No findings.

(1.1 minutes, 477,235 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The change supplies the release diff, build evidence and before/after proof, but the release sign placement violates an explicit decoration requirement. The recorded gated builds passed; I did not rerun them.

- **medium** [P2] Move the release signpost north of the road (`notes\cc-P803-tools\edit_layouts.py:25`)
  The release signpost is placed at y2596, south of the road at y2592???2595 (also recorded in `placed.md`), so its south-facing board faces away from approaching road traffic. This contradicts the prompt's explicit north-side requirement and [the building guide](notes/guides/building-and-decorating.md#L329-L335), which specifically requires signs for buildings south of a road to stand across it. Move the sign north of the road and regenerate the layout, release diff and proof.

(0.9 minutes, 527,764 tokens)
