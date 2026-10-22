# Codex review: P408

CC task P408: port OSI's Treasures of Sorcerer's Dungeon (Jack the Pumpkin King) for Halloween. Reviewed by Codex (`codex exec review`, read-only) after P408 DONE and before the Golem's commit, 2026-10-22 14:57.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The port substantially implements P408, but kill eligibility changes after deletion, shutdown misses creatures from completed rooms, and a new test can fail randomly. Build and runtime results were reviewed in the task notes, not independently rerun.

- **medium** [P2] Make the death-hook tally assertion independent of the drop roll (`server\tests\Services\Seasonal Events\TreasuresOfSorceresDungeon\SorcerersDungeonVerification.cs:679`)
  `KillBy` invokes the production artifact roll, which can legitimately succeed and remove the player's tally. These assertions then fail despite correct behavior, making the mandatory shard build gate intermittently red. Make this test deterministic through a controllable roll, or assert the valid tally-or-artifact outcomes while testing the no-drop tally separately.
- **medium** [P2] Retain rotated-out creatures for event shutdown cleanup (`server\customizations\Services\Seasonal Events\TreasuresOfSorceresDungeon\Spawner.cs:283`)
  When a room's boss dies while ordinary event creatures remain alive, `Reset()` clears their only tracking list without deleting them. Subsequent `off` or `remove` commands cannot remove those creatures, and saving also loses their association with the event. This contradicts P408's shutdown requirement and the documented cleanup behavior. Retain those creatures in a persisted cleanup collection, or remove them when advancing rooms; cover shutdown after at least one completed rotation.
- **medium** [P2] Preserve pre-deletion control state when checking kill eligibility (`server\customizations\Services\Seasonal Events\TreasuresOfSorceresDungeon\SorcerersDungeonData.cs:127`)
  When a non-bonded controlled pet dies in the dungeon, ModernUO's `BaseCreature.OnDelete` calls `SetControlMaster(null)`, clearing `Controlled` before `CreatureDeathEvent` reaches this check. The pet therefore contributes kill tallies and can award artifacts, whereas ServUO excludes controlled victims. Capture its eligibility alongside the map before deletion, and test an actual controlled-creature death. This also preserves the porting invariant in [AGENTS.md:171???173](AGENTS.md#L171-L173).

(2.3 minutes, 1,635,093 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.88). The only change in this repository is the new P408 notes file; there are no tracked staged or unstaged changes. The notes cover the requested facts, deviations, testing, staff checklist and credits. The server implementation and reported test results cannot be independently validated from this documentation-only diff.

No findings.

(0.4 minutes, 100,118 tokens)
