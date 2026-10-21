# cc-P369: fix-up for P264 (companions B1): its branch did not merge into main

**Golem:** Bronze. **Date:** 2026-10-21. **Branch:** `golem/Bronze/P369` (ShatteredLegacy work copy). **Image:**
`sl-modernuo:cc-P369`.

## In plain words

- The companions groundwork from P264 can now be merged. Its build failed because of two old tests that fail at
  random, about 1 run in 20 or 60. Neither has anything to do with companions; P264 just happened to hit one.
- Both tests are fixed so they no longer fail at random. Before, a merge could fail for no real reason. Now 60
  isolated runs of each pass, and so do 5 full test runs.
- You won't notice anything in game; this only makes merges more reliable.
- Nothing for you to do.

## Headlines

- **The merge:** this branch is now `origin/main` (`a67da42`, which includes P366, P367 and P219) plus
  `origin/golem/Bronze/P264` (`aa6b750`). The only conflicts were `CHANGELOG.md` and `VERSION`.
- **The red test was a flake that was already on main.** The integrator's log (`golem-ShadowIron.log` 11:03:57)
  does not name the failing test. I rebuilt and reran the full suite many times and found two intermittent
  failures. Both are older tests that also fail without P264:
  1. `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant`
     (cc-P46, 2026-10-03), Sagittarri and ForestNymph cases.
  2. `CC6Batch1CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape` (cc-P130).
- **Both tests are fixed** (below). The image builds green: `Built sl-modernuo:cc-P369 with patches applied and
  2031 shard test(s) passing.`

## The conflicts

| File | Resolution |
|---|---|
| `CHANGELOG.md` | P264's single Staff line ("Companions, first part ...") moved under main's newest heading, **2026.10.21.16**, after P367's Music Room lines. Main's .15 and .16 sections are otherwise unchanged. |
| `VERSION` | The higher: 2026.10.21.16 (main), over P264's .15. |

I first merged onto `e7e5dbd`. `origin/main` then moved to `a67da42` (P367 and P219), so I aborted, fast-forwarded to
`a67da42` and merged P264 again. Main's two new commits touch no file under `server\` or `docker\`, so the server
tree I built and tested is the one on the branch.

## The two flaky tests

### 1. The wisp orb fight (`server\tests\Services\Revamped Dungeons\DespiseRevamped\WispOrbPossessionVerification.cs`)

- **The failure:** "the possessed creature never took the foe as its Combatant: the fight did not start"
  (line 301). Every safety check before it held.
- **How often:**
  - full suite: once in 3 runs on cc-P369 and once in 4 on cc-P366 (main without P264)
  - isolated, with a diagnostic copy of the test: 2 failures in 40 runs
- **Cause:** the diagnostic output showed both failures had the same shape. The foe (Naba, then Phantom) had
  wandered, then picked the **party member** (`foeCombatant` = the Friend at 5399,560) instead of the possessed
  creature. The orb's default aggression is Defensive, which guards the master only. So the creature correctly
  stayed out of it, and the "the fight happened" check went red.
- **This is not a game bug.** The test assumed the foe would always go for the creature.
- **Fix:** the theory starts with `f.Foe.Combatant = f.Pet;`, so the fight always starts on the creature, and a
  comment explains why. The safety checks (never harms its master or party, master never targets it, never
  joined) are unchanged.
- **After the fix:** 0 failures in 60 isolated runs of the class (6 cases each).

### 2. The Skree's control slots (`server\tests\Mobiles\Normal\CC6Batch1CreatureVerification.cs`)

- **The failure:** `Assert.Equal(3, skree.ControlSlots)`, expected 3, actual 2.
- **Cause:** randomness, not test order. The port of ServUO's `CalculateSlots`
  (`server\customizations\Services\Pet Training\BaseCreature.PetTraining.cs:192-212`) sets `SlotsLowered` when the
  creature's stats rolled low at construction. The slot setter then clamps to the definition's minimum less one,
  so a Skree is legitimately 2 slots sometimes, as in ServUO.
- **Fix:** the test expects `PetTrainingStore.Get(skree, false)?.SlotsLowered == true ? 2 : 3`.
- **Before the fix:** 1 failure in 60 isolated runs. **After:** 0 in 60.

**Full suite after both fixes:** the image build's run, then 5 more full runs on `sl-uo-builder:cc-P369`. Every
run passed, 3127 of 3222 with 95 skipped (the dotnet total, which includes the stock tests). No other failure
showed up in about 20 full runs this session.

## P264's own work

P264's code and tests are unchanged:

- `server\customizations\Companions\*`
- `ClusterFSkillCaps.cs` and `ClusterFSkillGain.cs`
- `CompanionBaseVerification` (6 facts)

The 6 facts pass in every full run above. Its notes, `notes\cc-P264-companions-b1-base-and-record.md`, still apply.

## Deviation

- The prompt said to check out `golem/Bronze/P264`. The hand-off said to stay on `golem/Bronze/P369` and not
  switch branches, so I merged `origin/golem/Bronze/P264` into P369 instead. That is the same content on the
  branch the Golem commits.

P369 DONE
