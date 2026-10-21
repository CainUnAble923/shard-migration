# Codex review: P196

CC task P196: port Blackthorn Dungeon (revamped). Reviewed by Codex (`codex exec review`, read-only) after P196 DONE and before the Golem's commit, 2026-10-20 23:32.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The change substantially implements the planned sitting and documents the deferred invasion system, but introduces a damage-range deviation, a flaky build-gating test, and omits the required placement dry run. Build and runtime results were not independently rerun during this read-only review.

- **medium** [P2] Provide the requested dry run before world generation (`server\customizations\Services\Revamped Dungeons\BlackthornDungeon\Generate.cs:84`)
  The task explicitly requires a placement command with a dry run, but this command declares `NoDryRun = true` and immediately deletes previous placements before creating replacements. There is no preview branch, and the handoff only instructs Chase to run `[GenBlackthorn`. Add a non-mutating preview reporting the affected facets, placements and existing objects before the destructive replacement command is used.
- **medium** [P2] Make the kill-tally assertion independent of the random drop (`server\tests\Services\Revamped Dungeons\BlackthornDungeon\BlackthornDungeonVerification.cs:396`)
  This kill uses the production artifact roll, which has a nonzero chance of awarding an artifact and removing the player's tally. When that legitimate outcome occurs, `TryGetValue` fails and the full build gate goes red despite correct behavior. Control the random outcome for this assertion, or accept and verify both valid outcomes; the later forced-drop check can still cover the award path.
- **medium** [P2] Preserve the paladin specialties' original damage ranges (`server\customizations\Services\Revamped Dungeons\BlackthornDungeon\InvasionSpawner\Creatures.cs:129`)
  For Chivalry invaders, `IsFighter` includes the paladin specialty, but ServUO's damage branch tests only `AI_Melee`. Consequently, these invaders now deal 15-28 instead of 12-22 base damage; the same substitution in `InvaderCaptain` changes 20-28 to 22-30. Keep the healing/weapon-ability predicate separate from the damage predicate and test both ranges. This unintended balance change conflicts with the [fidelity agreement](AGENTS.md#L152-L154).

(2.9 minutes, 2,243,191 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The documentation provides a substantial handoff, but the play-test numbering misroutes checks and the reward test is underfunded. This verdict covers the docs-repository changes; the server implementation and reported build results were not independently verified.

- **medium** [P2] Supply enough artifacts for both reward purchases (`testing\playtest-steps.json:2850`)
  On a character with no existing Blackthorn points, twelve artifacts yield only twelve points, but this test requires purchases totaling 35 points. After buying the painting, the tunic purchase must fail even when the implementation is correct. Generate at least 35 artifacts or explicitly provision the required starting balance so the stated pass condition is achievable.
- **medium** [P2] Align the checklist numbering with the seven play-test entries (`notes\cc-P196-port-blackthorn-dungeon.md:399`)
  `playtests.parse_notes` extracts six items here, but the triage and steps define seven, inserting the gas-cloud test at P196-2. Consequently, P196-2 through P196-6 receive instructions and Who assignments for different tests, and P196-7 is never imported. For example, the invader test becomes EYES with shield-placement instructions, while the completed boot receives invader instructions. Split the gas-cloud check into its own numbered checklist item and renumber the remainder to match.

(0.7 minutes, 265,059 tokens)
