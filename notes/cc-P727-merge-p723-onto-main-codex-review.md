# Codex review: P727

CC task P727: land P721 (via its fix-up P723) on main. Reviewed by Codex (`codex exec review`, read-only) after P727 DONE and before the Golem's commit, 2026-10-28 15:54.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The vision conflict resolution preserves both edits, but the new mandatory pitchfork step can permanently block farm progression. Full shard tests and the isle bot route were not independently run during this read-only review.

- **medium** [P2] Retry issuing the pitchfork after the guard step is recorded (`server\customizations\Tutorial\TutorialFarm.cs:582`)
  If the trainee's backpack is full when they finish the Guard command, `GuardKey` is recorded even though `GivePitchfork` fails. Making room and double-clicking Wren, as the failure message instructs, cannot recover: `BeginCommands` only gives a pitchfork when no pet exists, and this branch never runs again once `GuardKey` is present. The trainee is stuck before the mandatory weapon step. Existing P718 trainees who already have `GuardKey` but no pitchfork encounter the same block. Retry issuance while the weapon step remains unfinished.

(0.9 minutes, 318,999 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.8). No actionable bugs found in the documentation and helper scripts in this repository. The recorded build and bot results support the notes, but the server changes and conflict resolution reside in the separate code repository and were not verified in this review.

No findings.

(0.5 minutes, 191,061 tokens)
