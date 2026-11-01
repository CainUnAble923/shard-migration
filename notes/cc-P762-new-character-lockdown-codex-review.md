# Codex review: P762

CC task P762: new-character lockdown: isle start, Human only, moongate skip. Reviewed by Codex (`codex exec review`, read-only) after P762 DONE and before the Golem's commit, 2026-11-01 10:01.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The main lockdown paths are implemented, but permanent gate-skipping can be bypassed and visitors are incompatible with the copy waiting queue. Build/test execution, screenshots, and release-branch applicability were not verified in this read-only review.

- **medium** [P2] Include visitors when serving the isle-copy waiting queue (`server\customizations\Tutorial\TutorialStart.cs:268`)
  When every copy is occupied, this new visitor path calls `TutorialCopies.Wait`, but `ServeLine` only accepts `ClusterFTutorial.IsParticipant(pm)`. Visitors are explicitly not participants, so they are removed from the queue without receiving a copy when capacity becomes available. They remain on the shared Fold despite being told they will automatically receive their own copy. Extend queue servicing to handle first-visit visitors as well as trainees.
- **medium** [P2] Apply the final-skip guard to orphan adoption and return trips (`server\customizations\Tutorial\ClusterFTutorial.cs:335`)
  If a second character visits the isle and gate-skips while the first character still owns an active tutorial, deleting the first character lets the skipper inherit that tutorial through `AdoptOrphanedRecord` on login or at Rook. Rook's `BtnToIsle` then sends the skipper back, and it can earn normal completion rewards. Guarding only `StartRemedial` does not enforce the required permanent skip; orphan adoption and active-tutorial return paths also need to respect `GateSkipped`.

(2.2 minutes, 821,381 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The included release patch leaves gate-skipping visitors restricted to Haven Island and permits them to return through orphaned-record adoption. The screenshot helper also defaults to the shared shard rather than the required private proof shard.

- **medium** [P2] Restrict the screenshot helper to private proof ports (`notes\cc-P762-tools\isle-shots762.ps1:27`)
  This new helper defaults to port 2594, which the proof-shard script identifies as the shared Test Shard, and its target guard permits that port. Running it without an explicit override logs into the shared shard and executes the supplied setup commands there, contrary to this task's private-proof-only requirement. Default to 2596 and explicitly reject the shared port.
- **medium** [P2] Prevent skipped visitors from adopting an orphaned tutorial (`notes\cc-P762-tools\p762-release-isle-20261028.diff:264`)
  The final-skip check only protects `StartRemedial`. If a visitor skips through the gate and the account's original tutorial character is subsequently deleted, `AdoptOrphanedRecord` still binds the active tutorial to that visitor at login or when speaking to Rook. Rook's existing lesson buttons then call `SendToIsle`, allowing the character back despite its permanent skip. Enforce the skipped-character restriction in adoption and return paths too.
- **medium** [P2] Give gate-skipping visitors their own graduation waiver (`notes\cc-P762-tools\p762-release-isle-20261028.diff:548`)
  When a second character visits while the account's first character is still taking lessons, this branch gives the reward but leaves the visitor at loop 0. `TutorialIslandGate.CanMove` consequently prevents that character from leaving Haven Island, and Rook cannot graduate it because the tutorial belongs to the first character. Grant the visitor its per-character skip waiver without changing the first character's tutorial record, and test onward travel.

(2.2 minutes, 943,327 tokens)
