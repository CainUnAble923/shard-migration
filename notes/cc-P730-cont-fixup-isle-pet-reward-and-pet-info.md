# cc-P730: P726 (the isle pet as a reward, Pet Info) brought onto main

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P730`. Not committed, nothing deployed, Haven not touched.

## In plain words

- **P726's work is ready to merge again.** It covers Wren's pet as the farm's reward, the healing lesson with Pip on
  his bench, Pet Info, the cloak and pitchfork regeneration and the lessons in the quest log. It had clashed with
  P728's farm fixes, which reached main separately. Nothing in it changed: the clash was only P728's lines appearing
  twice.
- The shard's tests all pass with P726 and everything now on main together (2,758 tests).
- **For you: nothing to do.** One thing for the integrator: P729 (no TazUO page at start) also uses version
  2026.10.28.8, so whichever of P729 and this merges second needs its CHANGELOG section renumbered to 2026.10.28.9.

## What was done

`golem/Iron/P730` starts from main `806c4ba` (P728 and P679 merged). The prompt says to check out `golem/Iron/P726` and
merge main into it, but the hand-off forbids switching branches. So I brought P726 into this branch instead:
`git merge --squash golem/Iron/P726` in both work copies. The result is the same tree, staged for the Golem's commit,
with no merge left in progress.

- **Docs copy:** merged with no conflicts. These are P726's notes and tools: `notes\cc-P726-isle-pet-reward.md`,
  `notes\cc-P726-tools\`.
- **Code copy:** the same nine conflicts the integrator hit.

## The conflicts, and why each took P726's side

P726 was written on top of P728's commit `f4e684e`, cherry-picked into its tree uncommitted (its notes, "Before
anything: P728 is in this branch"). Main later merged that same commit. So both sides changed the same lines from the
merge base `3dd8559`: main with P728 alone, P726 with P728 plus its own work.

- **Checked:** for every conflicted file, main's copy is byte-identical to P728's commit (`git diff f4e684e main --`
  is empty for all nine). Main has nothing in them that P726 lacks.
- **So each file takes P726's version**, and both sides survive:

| File | Resolution |
|---|---|
| `CHANGELOG.md` | P726's: its 2026.10.28.8 section (3 Added, 2 Changed) above P728's 2026.10.28.7, which is identical to main's, as is everything below (checked by diff) |
| `VERSION` | 2026.10.28.8, the higher |
| `server/customizations/Tutorial/TutorialCoreTrials.cs`, `TutorialFarm.cs`, `TutorialRecruiter.cs` | P726's (P728 plus the pet-as-reward order, the healing lesson, Pip's bench, and P726's fix to P728's load seed) |
| `server/tests/Tutorial/TutorialFarmVerification.cs`, `TutorialIsleBandageWaitVerification.cs`, `TutorialIsleWalkFixes4Verification.cs` (added on both sides), `TutorialIsleWalkFixesVerification.cs` | P726's |

**The result, checked:** the staged tree differs from `golem/Iron/P726` only in what main gained since, P679's files:
- `docker/uo/Dockerfile`, `apply-patches.sh`;
- `Maps/SosTeleporters.cs`, `Tutorial/HavenSpots.cs` (a comment);
- `server/data/teleporters-sos.json`, `server/data/Locations/`;
- the three SoS patches and `server/tests/Maps/SosGatesVerification.cs`.

No conflict markers remain.

## Tests

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P730`, `docker-build` lock, released), **EXIT=0**:
- 2,758 tests: 2,752 passed, 6 skipped (the usual client-data facts), 0 failed (`cc-P730-tools\green-gated-build.txt`);
- that is P679's 2,753 and P726's 5 new facts (`TutorialIslePetRewardVerification`, all passed).

**P726's bot route on a private shard was not run again.** It passed (run 5, 0 failed checks) on P726's tree. This tree
differs from that one only in P679's files, which the isle does not read:
- moongate and teleporter data for Trammel and Felucca, and the staff go-menu;
- a comment in `HavenSpots.cs`.

Nothing needed fixing.

## Files

- Code copy: P726's change set (staged by the squash merge, conflicts resolved as above).
- Docs copy: P726's notes and tools (staged), this note, `notes\cc-P730-tools\` (the build script and its summary).

P730 DONE
