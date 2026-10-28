# Codex review: P717

CC task P717: the first character on an account must take Tutorial Island; New Haven opens after. Reviewed by Codex (`codex exec review`, read-only) after P717 DONE and before the Golem's commit, 2026-10-28 08:14.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The unlock and per-account labels are implemented, but locked accounts can still start additional characters in New Haven before completion and after an account reset. The reported green gates do not cover these destination-level failures; runtime tests were not independently rerun.

- **high** [P1] Enforce the locked destination for additional characters (`server\customizations\Tutorial\TutorialStart.cs:143`)
  If the first character is still in the tutorial, creating a second character bypasses the account gate: converting its choice to `Choice.Isle` still reaches `Outcome.Elsewhere`, and `ConsumeAtLogin` sends it to New Haven. No character has graduated or skipped. This also violates the explicit requirement that a forced New Haven selection while locked land on the isle. Enforce the locked destination across the active-record cases and test creation of a second character before completion.
- **medium** [P2] Make account resets restore day-one start behavior (`server\customizations\ClusterFDevTools.cs:208`)
  After graduation or skip, resetting account flags removes the unlock but leaves the finished tutorial record intact. The next character therefore sees New Haven labeled locked yet still starts there through `Decide`'s `Outcome.Finished` branch, regardless of which entry is selected. The requested account resets cannot actually test day one again without an additional staff command. Reset the relevant tutorial eligibility state too, and extend the reset test to create and log in a new character instead of checking only the flag and city labels.

(1.1 minutes, 253,126 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The notes and supporting artifacts document substantial implementation and testing, but also explicitly retain two behaviors that miss the requested start restriction and reset workflow. The reported green tests do not establish those required outcomes.

- **medium** [P2] Enforce the lock while another character is in the tutorial (`notes\cc-P717-isle-first.md:49`)
  A player can create one character, leave it in the core, and create a second character that immediately starts in New Haven without anyone graduating or skipping. Converting the locked Haven selection to an isle selection does not enforce the restriction because `Decide` then returns `Elsewhere`, and `ConsumeAtLogin` sends that character home. The prompt explicitly requires a forced New Haven selection while locked to land on the isle; retaining this eligibility row leaves a straightforward bypass. Handle this account state explicitly and add a placement test for it.
- **medium** [P2] Make account resets restore the actual day-one start (`notes\cc-P717-isle-first.md:14`)
  After an account graduates or skips, either account-reset command clears the unlock flag but leaves the finished tutorial record. `TutorialStart.Decide` therefore still sends the next character to New Haven despite displaying it as locked. This misses the requested ability to test day one again using those resets; requiring an additional staff `[Tutorial reset` is not equivalent. Reset the relevant tutorial eligibility state too, and test character placement after the reset rather than only the flag and city names.

(0.8 minutes, 170,645 tokens)
