# P547: review of trash bag corpse clearing (P415)

Reviewed October 24, 2026. Notes only. P415 commit
`c9c60712856479d222b2c235a52ae43a678f0bd6` is an ancestor of local main;
the code work copy and main both point to
`82ba93fdd3e047646cdf63cb4f468b9a30b90270`. No remote refresh was attempted.

Read both work-copy AGENTS.md files, the direction decision and task list,
`notes/cc-P415-trash-bag-corpse-claim.md`, the P432 review and its Codex review,
and the P530 comparison. No separate P415 review was found beside its note.
Previously reported bag-replacement loss, wall/floor access, protected corpse
contents, barrel bookkeeping, and crafted-item point farms are not repeated.

Paths below are relative to the ShatteredLegacy work copy unless stated
otherwise. Findings describe source behavior; client and runtime reproductions
remain unverified.

## Findings

1. **bug** | `server/customizations/ClusterFCustodianSystem.cs:136`, `:162`:
   The eligibility rule reused by both new menu actions accepts bonded pet
   corpses, so an empty one can be cleared immediately by an authorized looter,
   and after the loot timers expire anyone can delete one with its remaining
   contents; the zero pet base in `ClusterFCorpseValue.Pays` prevents a Fame
   award but does not prevent deletion.
   Exclude bonded pet corpses in the shared clearing predicate, preserving any
   pet identity needed after load, and add single-target and nearby regressions
   that assert the corpse and its contents survive, rather than only testing
   its zero base value.

2. **bug** | `server/customizations/ClusterFCustodianSystem.cs:436`, `:461`:
   The nearby warning saves no corpse list or location, so opening it at one
   hunt, moving or recalling to another hunt, and accepting deletes the newly
   scanned corpses and their loot without a warning for that selection; newly
   dead or newly eligible corpses can also enter the batch while the warning
   is open.
   Bind acceptance to the previewed corpse serials and map, revalidate their
   range and rights, and ask again if the destructive selection expands, with
   callback tests for movement, facet changes, and newly eligible corpses.

3. **risk** | `server/customizations/ClusterFCustodianSystem.cs:392`, `:461`;
   `server/customizations/TrashBag.cs:153`, `:206`:
   Bag ownership and backpack location are checked before opening the warning,
   but neither acceptance callback retains the bag, so banking, transferring,
   or deleting it while the warning is open still permits clearing and pays
   points without the required owned bag in the backpack.
   Pass a bag validator through both confirmation paths and refuse acceptance
   when it fails, with regression tests that move or delete the bag after the
   warning opens.

## Supporting evidence and coverage

- Pinned ModernUO was verified at
  `d4531cd94b739613155225c234900de9f47d2c88`, with a clean work tree.
  `D:/UO/ModernUO-pinned/Projects/Server/Mobiles/Mobile.cs:4847` creates the
  corpse before `OnDeath` at `:4873`.
  `Projects/UOContent/Items/Misc/Corpses/Corpse.cs:619` assigns it to the owner
  and `:631` moves the death contents into it. Bonded death then leaves a ghost
  pet at `Projects/UOContent/Mobiles/BaseCreature.cs:3482` and `:3495` rather
  than removing that corpse. Finding 1 concerns the corpse and its loot, not
  deletion of the ghost pet or loss of its resurrection ability.
- The pet's master enters the corpse aggressor list at pinned `Corpse.cs:297`;
  normal monster rights expire through `Projects/UOContent/Misc/Notoriety.cs:332`
  and item instancing expires at `Corpse.cs:321`. Our eligibility predicate
  checks neither `IsBonded` nor pet ownership. Our
  `server/customizations/Services/CleanUpBritannia/ClusterFCorpseValue.cs:75`
  excludes pets only from the base award. This is an inherited eligibility gap
  exposed by the new menu actions.
- Pinned `Projects/UOContent/Gumps/WarningGump.cs:87` invokes the stored
  callback on acceptance. The nearby callback calls the whole scan again with
  `confirmed: true`; the single callback keeps the corpse serial but neither
  callback keeps the bag. Source inspection establishes these paths; no live
  warning was answered during this review.
- `server/tests/Services/TrashBagCorpseClaimVerification.cs:193`, `:198`,
  `:326`, and `:330` test the unconfirmed helper and then call it directly with
  `confirmed: true`. They do not answer the actual warning, cancel it, or change
  the bag or selection before acceptance. The entry test at `:143` checks menu
  visibility, not entry clicks or the targeting callback. The regressions
  suggested above should exercise those real paths and be observed failing
  before fixes and passing afterward.
- `server/tests/Services/ClusterFCorpseValueVerification.cs:115` tests that
  summoned, tamed, and bonded creatures pay no base. It does not test whether
  their corpses can be cleared. The older
  `server/tests/Services/CustodianLayerVerification.cs` also checks corpse
  values and player eligibility, not bonded-pet clearing.

No additional loot-rights bypass was found in the ordinary fresh-kill and
shared instanced-loot paths: both menu actions use `CanClear`, and their
confirmation calls check it again. Player corpses with a retained
`PlayerMobile` owner are refused by the shared eligibility rule. Those source
checks and the existing player-corpse tests do not establish every saved-world
edge case.

No new point-farming route was found beyond issues already recorded in P432.
The new actions value the corpse with the acting character, delete it, and
award once; deleted corpses fail subsequent eligibility checks. The creature
base excludes summoned, tamed, bonded, animated, mastered, and previously tamed
creatures. Ordinary contents still pay their shared Clean Up values, as P415
explicitly intended. This is a source review, not an economy stress test.

## Files reviewed and validation

Read P415's listed implementation and test files:

- `server/customizations/TrashBag.cs`
- `server/customizations/ClusterFCustodianSystem.cs`
- `server/customizations/ShardClilocs.cs`
- `server/tests/Services/TrashBagCorpseClaimVerification.cs`
- `player-package/vendor/shattered-legacy-cliloc/entries.json`
- `player-package/vendor/shattered-legacy-cliloc/registry.csv`
- `player-package/tests/Cliloc-Overrides.Tests.ps1`
- The relevant P415 release entries in `CHANGELOG.md` and current `VERSION`.

Also read the corpse-value implementation and tests, the older Custodian
corpse test, and the pinned death, corpse, notoriety, and warning paths cited
above. The two new cliloc numbers agree across server, package, and registry.

No code or tests changed. No tests or build were run, as requested for this
notes-only review. Historical green results in P415's note are not a fresh
test result. No Haven connection, deployment, account operation, commit,
merge, push, or branch switch occurred. Commands ran in Windows PowerShell
5.1, and stop-request checks were made between steps.

Ran `tools/progress.py --dry-run` with both work-copy path overrides. Its
incidental progress.json write was suppressed in memory; the existing file
remained byte-identical. Global source counts are not used as review coverage.

Final checks: the code work copy is clean, and the migration work copy contains
only this new note. Whitespace checks passed in both repos. The note is ASCII,
contains no em dashes or trailing whitespace, and is below 5 MB. No stop request
was present at the final check. No P547 review work remains.

P547 DONE
