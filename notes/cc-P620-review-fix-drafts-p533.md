# P620: review of the P610 fixes from P533

Reviewed October 25, 2026. Notes only. Four medium-severity findings remain in the reviewed fixes. One was reproduced through a throwaway loopback service; the other three are source-confirmed, with C# runtime behavior unverified in this lane.

## Findings

### 1. Medium (P2): submitting an answer from an old page can answer a different question

**Location:** `docker/test-queue/server.py:535-540`, with the requests at `docker/test-queue/html/index.html:469-475` and `tools/decisions.py:481-499` in the notes repo. Scope: U8.

The new join preserves answers that were already saved when questions move, but the answer and Ask me later requests still carry only the positional ID. The server resolves that ID against the current questions before passing the resulting question to `_record`. Its question-text guard therefore compares the current question with the current record, rather than with the question the user saw.

Reproduced against the actual queue server on `127.0.0.1`, using scratch notes and an empty overlay:

1. Load a page where P901-D1 asks "Use oak for the door?" and P901-D2 asks "Add a lamp?".
2. Swap the two questions in the scratch notes without refreshing that page.
3. Submit the old door card's normal request: `{"id":"P901-D1","text":"oak, please"}`.
4. The server returns HTTP 200 and saves `oak, please` under `**Add a lamp?** Say which.`. The door question remains unanswered.

This is a separate operation from the stale take/undo problem already reported in P610's attached review. It can create a wrongly attributed answer before any take occurs. The same positional lookup serves Ask me later.

**Fix:** carry the displayed question identity on answer and later requests, validate it before mutating the answer store, and reject a changed question while preserving the browser draft. Use the stable answer identity and revision when editing an existing answer. Add endpoint regressions for an old page after insertion, reordering, and rewording, including an unchanged question that should still accept its answer. The current Identity tests rebuild the decision before answering, so they do not exercise this request path.

### 2. Medium (P2): disabling companions before a restart skips the new recovery

**Location:** `server/customizations/Companions/CompanionParty.cs:168-170` and `:183-185`. Scope: U1.

Save while an owner and companion are in the world, then start with `clusterf.companions.enabled` false. The newly added `ReconcileAfterLoad` returns without putting the companion away. Removing that return alone would still fail, because it delegates to `OnOwnerLogout`, whose enable guard at lines 114-118 also returns. `OnOwnerLogin` only recovers companions whose `AwayWithOwner` is already true, so the disabled restart leaves this companion at its old location instead of bringing it to the owner.

For a ghost companion, this also leaves `IsStabled` false. Pinned `Projects/UOContent/Mobiles/BaseCreature.cs:5987-6001` handles abandoned ghosts before the living-pet loyalty branch, so the new `KeepsLoyalty` patch does not protect it from removal after `BondingAbandonDelay` while its owner stays offline.

This combines the two transitions that P610 tests separately: an already-away companion logging in while disabled, and an in-world companion recovered at an enabled restart. The new restart guard leaves their combination broken. No ghost deletion was executed here.

**Fix:** run recovery of existing owned companions independently of the enable setting, including the actual internalization helper it calls. Retain the released, deleted, and roomed exclusions. Extend `server/tests/Mobiles/Companions/CompanionLifecycleVerification.cs:217` with enabled-save/disabled-start cases for both a living companion and a ghost, then verify repeated reconciliation, abandonment sweeps, and login recovery.

### 3. Medium (P2): a restart inherited from an old save is lost on the next save

**Location:** `server/customizations/Services/MiniChampionSystem/MiniChampionSpawn.cs:467-470`, with `MiniChampRestarts.cs:35-58` in the same directory. Scope: A1.

When the new restart store is absent, `ResumeAfterLoad` preserves the old behavior by scheduling a restart timer. It never records that pending restart in `MiniChampRestarts`. If the server saves and restarts again before that timer fires, the new save now contains the restart store but no entry for this controller. On the second load, `Loaded` is true and `PendingAt(this)` is null, so no timer is restored. The controller remains inactive indefinitely instead of completing the restart already scheduled by the first load.

The existing `ASaveFromBeforeTheRestartStoreKeepsServUOsRestart` fact only waits for that first timer. It does not save during the compatibility interval. This is a new failure introduced by the store's compatibility branch, distinct from the earlier disabled-controller finding.

**Fix:** record the deadline whenever the compatibility branch creates a pending timer, using the same persisted scheduling path as a normal completion. Test an old save with no store, allow the first load callback to schedule its restart, save before the deadline, reload with the new store, and verify one restart at the original deadline. Also test canceling that inherited restart before the second save.

### 4. Medium (P2): newly accepted set jewelry loses its set bonus in an extra slot

**Location:** `server/customizations/Accessories/ClusterFAccessories.cs:123-124` and `:355-358`. Scope: W3.

The expanded `KindOf` now accepts `BaseSetJewel` pieces in extra slots, but the set implementation still counts only direct `Mobile.Items`. For example, wear an ordinary bracelet on the paperdoll, Etoile Bleue on the ring layer, and Novo Bleue in the unlocked extra bracelet slot. Both Luck-set pieces are active jewelry, but `SetHelper.FullSetEquipped` counts only Etoile Bleue and returns false. The set's extra Luck, regeneration, and casting bonuses never activate.

Calling `item.OnAdded(m)` during accessory refresh does not solve this: `BaseSetJewel.OnAdded` calls that same direct-item counter. `SetHelper.AddSetBonus` and `RemoveSetBonus` also walk direct items, and `server/patches/AOS-set-attribute-aggregation.patch:8-16` reads the last piece's set attributes only in the direct-item loop. All these paths need a consistent definition of worn set pieces.

Supporting source: `server/customizations/Items/Artifacts/Equipment/Armor/Sets/BaseSetJewel.cs:154-167`; `SetItem.cs:232-248`, `:283-318`, and `:327-342` in that directory; `Luck/EtoileBleue.cs:22-28` and `Luck/NovoBleue.cs:22-28`. The new test at `server/tests/Misc/AccessoryIntegrationVerification.cs:213` checks classification, intrinsic absorption storage, and ordinary Luck, without completing a set in an extra slot.

**Fix:** include active extra-slot pieces consistently in set membership, bonus application/removal, and effective attribute aggregation, exactly once. Test Etoile Bleue plus Novo Bleue with one piece in an extra slot, both equip orders, moving the piece between paperdoll and container, and locking/removing the extra slot. Assert effective wearer bonuses and their removal. This finding concerns set activation; it does not repeat the absorption-reader defect already in P610's attached review.

## Scope and earlier findings

Read both work copies' AGENTS.md, the direction decision, task list, both `notes/cc-P610-*.md` files, P533's report and attached review, and the relevant P486, P487, and P491 source reviews. Reviewed code commit `f62d0b82ac61163efc090cc0488fe39e6c86b0e5` and notes/tooling commit `530562f`, including their changed tests, patches, migrations, callers, and consumers.

Current code HEAD is `57924e6`; notes HEAD before this report is `d0f45cc`. Citations use the work copies at those heads. Later changes to shared tutorial files were checked so P610's fixes were not reviewed against an older copy. Pinned ModernUO was clean at `d4531cd94b739613155225c234900de9f47d2c88`. ServUO and pinned source were read only. `server/uo/` was not used.

The attached P610 review already reports missing real-overlay Rootdeep coverage, loss of edits typed during a pending save, missing extra-slot absorption aggregation, and stale take/undo identity. Those are not additional findings here. P610's own follow-ups, including the Void Pool top-20 problem, were not repeated. The deferred recovery formula and tutorial exit gate were not treated as completed fixes or new defects.

## Validation and limits

- Reproduced finding 1 through the actual queue server with the existing `tools/tests/test_decisions.py` Service fixture, temporary notes/data, an empty overlay, and a loopback-only listener. The process was terminated afterward. No live service or real decision record was touched.
- Ran the existing Identity, Revisions, and Page classes in `tools/tests/test_decisions.py`: all 12 tests passed. Their initial runs hit Windows access-denied errors creating child folders under Python's private temporary directories. The successful run used a process-local replacement for `tempfile.mkdtemp` that creates ordinary-permission directories in the ignored `downloads/P620` scratch area. Test code and application code were unchanged.
- Ran `notes/cc-P480-tools/test_graduation_rewards.py`: all four tests passed. These are stand-in-client tests, not an in-game graduation.
- Docker access was denied at `npipe:////./pipe/dockerDesktopLinuxEngine`. No builder inspection, C# test run, image build, or cold world restart could be performed. Findings 2-4 are source-confirmed; their proposed runtime regressions remain unverified. P610's reported 2,451-test gated build was not independently reproduced.
- Ran the progress reporter with both work-copy paths and `--dry-run`. A process-local `Path.write_text` guard suppressed its unconditional `tools/progress.json` write; that file stayed byte-identical. No generated status artifact changed.
- No code or tests were added or edited. No Haven connection, deployment, account operation, docs/ edit, commit, merge, push, or branch switch occurred. No new test gate or red-to-green fix is claimed by this review.

## Reviewed P610 file inventory

The code commit changes 48 files, counted with `git show --format= --name-only f62d0b8`. Its exact file list is:

```text
CHANGELOG.md
VERSION
docker/test-queue/README.md
docker/test-queue/html/index.html
docker/test-queue/server.py
docker/uo/apply-patches.sh
server/customizations/Accessories/AccessoriesGump.cs
server/customizations/Accessories/ClusterFAccessories.cs
server/customizations/ArtificersImbueGump.cs
server/customizations/ClusterFLeagueRanks.cs
server/customizations/ClusterFRootdeepSeeder.cs
server/customizations/Companions/BaseCompanion.cs
server/customizations/Companions/CompanionParty.cs
server/customizations/Imbuing/ClusterFImbueEffects.cs
server/customizations/LevelGear/ClusterFLevelGear.cs
server/customizations/OutridersGuildmasterGump.cs
server/customizations/Services/MiniChampionSystem/MiniChampRestarts.cs
server/customizations/Services/MiniChampionSystem/MiniChampionSpawn.cs
server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs
server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/Items/CauldronOfTransmutation.cs
server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/VoidPoolController.cs
server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/VoidPoolStats.cs
server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusChest.cs
server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Loot/ExodusHealingBonus.cs
server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Region.cs
server/customizations/Services/Revamped Dungeons/TheExodusEncounter/VerLorRegController.cs
server/customizations/Services/Underworld/ExperimentalRoom/ExperimentalGem.cs
server/customizations/Services/Underworld/PuzzleRoom/MagicKey.cs
server/customizations/Tutorial/TutorialLoans.cs
server/customizations/Tutorial/TutorialPetCare.cs
server/customizations/Tutorial/TutorialTradeTrials.cs
server/customizations/Tutorial/TutorialWingTrials.cs
server/migrations/Server.Engines.Exodus.VerLorRegController.v0.json
server/migrations/Server.Items.CauldronOfTransmutation.v0.json
server/patches/Bandage-asclepius-bonus.patch
server/patches/BaseCreature-companion-loyalty.patch
server/patches/PuzzleChest-repeat-wrong-guess.patch
server/tests/Misc/AccessoryIntegrationVerification.cs
server/tests/Misc/UnravelApprovalVerification.cs
server/tests/Mobiles/Companions/CompanionLifecycleVerification.cs
server/tests/Regions/RootdeepMapSafetyVerification.cs
server/tests/Services/CleanUpBritanniaPointsVerification.cs
server/tests/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs
server/tests/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs
server/tests/Services/UnderworldStateVerification.cs
server/tests/Tutorial/TutorialFirstPlayVerification.cs
server/tests/Tutorial/TutorialLoanLifecycleVerification.cs
server/tests/Tutorial/TutorialServicesVerification.cs
```

The companion notes commit changes these eight files:

```text
notes/cc-P480-tools/playthrough.py
notes/cc-P480-tools/test_graduation_rewards.py
notes/cc-P610-fix-drafts-from-p533-codex-review.md
notes/cc-P610-fix-drafts-from-p533.md
tools/decisions.py
tools/playwhere.py
tools/tests/test_decisions.py
tools/tests/test_play_who.py
```

Final checks passed: both inventories match their commits exactly, the report is ASCII with no em dashes or trailing whitespace and is below 5 MB, the code work copy is clean, and this report is the only notes-repo change. Stop requests were checked between steps and before completion.

P620 DONE
