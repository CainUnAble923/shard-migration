# P581: review of P455 death hooks

Reviewed 2026-10-24. Documentation only. No code changed.

P455 commit `2b08d9065947545cf05d4aebc7994e668594d6c5` is an ancestor of local
`main`, merged by `d83b902`. Reviewed code HEAD and local main are
`608d0b42485390f7963a713a28161d96e7618b63`; the P455 implementation and test
files have no differences from main. Pinned ModernUO is
`d4531cd94b739613155225c234900de9f47d2c88`, with a clean working tree.

Read `cc-P455-death-hooks.md` first. No separate P455 review was present beside
it. Also checked the P404/P429 findings that led to P455 and the later P476,
P528 and P533 references so the original failures are not reported again.

## Findings

No confirmed functional bug found in the P455 changes. I found no remaining
event-order failure preventing boss boxes or Self Repair, no duplicate award
path, and no double bestiary credit for pet, summon or provoked kills. The
following are test coverage risks, not observed gameplay failures.

1. **risk: boss test does not verify delivery or mixed player/pet credit.**
   `server/tests/Misc/DeathHooksVerification.cs:126`, especially `:137`.
   The real-kill test checks only the source record for one direct player
   kill. It would still pass if box delivery were removed after recording,
   and it never exercises an owner appearing through both direct damage and
   a pet's or summon's damage. Suggested fix: kill a boss through mixed
   damage by an owner, their pets or summons, and another eligible player;
   assert exactly one boss-source box reaches each eligible player's pack
   or bank, then kill another boss of the same type on the same loop and
   assert no additional boss-source boxes arrive. Filter by source because
   achievements can legitimately award their own boxes during the kill.

2. **risk: the Self Repair test cannot detect a second probability roll.**
   `server/tests/Misc/DeathHooksVerification.cs:170`, especially `:186`.
   `AlwaysZero` makes the first attempt succeed. A second traversal would
   then skip that plate because it already has Self Repair, so the test
   would pass even if unsuccessful items were receiving two chances per
   death. The statistical test at
   `server/tests/Items/RareSelfRepairVerification.cs:150` calls `TryRoll`
   directly and does not cover event multiplicity. Suggested fix: add a
   real-kill case with a counting random stub that misses the first
   `Next(500)` call and would hit a second, and assert exactly one such
   call per eligible item with no Self Repair added after the miss.

## Source checks and limits

Primary implementation files reviewed:

- `server/customizations/LootBoxes/ClusterFLootBoxes.cs`
- `server/customizations/ClusterFRareSelfRepair.cs`
- `server/customizations/Imbuing/ClusterFImbueEffects.cs`
- `server/customizations/ClusterFLeagueBestiary.cs`

Tests reviewed:

- `server/tests/Misc/DeathHooksVerification.cs`
- `server/tests/Items/RareSelfRepairVerification.cs`
- `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs`
- `server/tests/Misc/LootBoxFanfareVerification.cs`

Traced the pinned source rather than relying on the implementation note:
`Projects/Server/Mobiles/Mobile.cs:4762` sets hits to zero, `:4847` creates
the corpse, and `:4873` calls OnDeath. The corpse handler assigns
`owner.Corpse` before adding its initial contents at
`Projects/UOContent/Items/Misc/Corpses/Corpse.cs:619`. Normal death deletes
the creature at `Mobile.cs:4901`; deletion calls OnDelete at `:2489`
before setting Deleted at `:2503`.

`Projects/UOContent/Mobiles/BaseCreature.cs:3674` raises the deletion
event before clearing the control master at `:3688`. The death event is
raised later at `:3669`. This supports the moved handlers' reads of
Deleted, Controlled and the populated corpse. Each moved handler has only
the deletion-event subscription. The boss handler deduplicates players
with a HashSet at `ClusterFLootBoxes.cs:180`, and Award records the loop
before delivering at `:98`. Bestiary credit resolves one damage master at
`ClusterFLeagueBestiary.cs:183`, and its account set rejects repeat entries
at `:157`.

Also inspected the other death-event handlers listed in P455's audit,
the existing level-gear deletion hook, the box delivery helper, and the
peerless, SA, Navrey, Despise, Shame and champion death paths relevant to
the event timing. No additional P455 finding arose from those checks.

No build, gameplay probe or test suite was run for this docs-only review;
lane tests are none. P455's recorded red/green results were read, not
independently reproduced. The proposed additional tests were not written.
Ran `tools/progress.py --dry-run` with both work-copy path overrides;
it exited 0 but rewrote `tools/progress.json` despite the dry-run flag
(`tools/progress.py:722`, before the return at `:737`). Restored that
generated file to its original contents, leaving only this review note
changed. No Haven connection, deployment, commit, merge, push or branch
switch was performed.

P581 DONE
