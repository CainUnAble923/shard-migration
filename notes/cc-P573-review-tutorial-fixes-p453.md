# P573: review of the P453 tutorial fixes

Reviewed October 24, 2026. Code work copy HEAD is `1020e36`, the merge of P453 commit `4cb4265040bc6bbfbbdb3cf8a4be8348f321713b`. This is a source review. No code changed.

Read both work copies' AGENTS.md, the direction decision and task list, both `cc-P453-*.md` notes, P429's findings and tutorial fix-up draft, and both P502 review notes. The findings below concern failed delivery and recovery after deleting an active trainee. They do not repeat P429's unlimited-bandage or alternate-character findings, or P502's pending-companion ownership finding.

## Findings

### 1. Medium (P2): failed backpack delivery consumes the bandage allowance

**Location:** `server/customizations/Tutorial/TutorialFarm.cs:294`, through line 296.

**What happens:** A trainee at the patch-up step with no bandages and a full or overweight backpack asks the Farmhand for supplies. `GiveBandages` increments the saved `BandagesIssued` count before calling `AddToBackpack`, ignores its result, and returns `Given`. Pinned ModernUO's `Projects/Server/Mobiles/Mobile.cs:7584` uses `TryDropItem` for placement, and `:7594` through `:7606` drops the item into the world when placement fails. The stack can therefore be taken by someone else while the account permanently spends one of its three issues. Repeated conversations with the pack still full can exhaust all three without putting bandages in the trainee's pack.

**Suggested fix:** Use backpack delivery that does not drop the item on failure. Increment `BandagesIssued` only after successful placement; delete an undelivered stack, tell the player to make room, and leave the allowance available for a retry. Add a regression case with a full backpack, then free space and verify that a successful retry uses exactly one issue.

**Coverage:** `server/tests/Tutorial/TutorialFarmVerification.cs:445` tests repeated banking and the cap, but never fills the backpack. P453's notes say a full pack gets none; that scenario is not exercised by this test, and the production call drops the stack instead.

### 2. Medium (P2): deleting an active trainee does not let another character resume

**Location:** `server/customizations/Tutorial/ClusterFTutorial.cs:71`, through line 74; related checks at `:64`, `:112` and `:225`.

**What happens:** Delete the recorded character while its tutorial is `InCore`, `InWings` or `Remedial`, then visit Rook with another character on the account. The new `IsRecordedCharacter` fallback accepts a deleted or missing owner, so `TutorialGumps.cs:66` makes the page writable. However, it never assigns the new character's serial to the record. `IsParticipant` still requires an exact serial match, so lessons, completion, skip, graduation and the farm all refuse the replacement character. Login cannot recover it because `TryEnter` accepts only `NotStarted`; `StartRemedial` can transfer ownership only from `Skipped`. The active account record stays attached to the deleted character until a separate reset is used.

**Suggested fix:** At a defined entry point such as login or opening Rook's page, transfer an active record to the requesting character only after confirming the old character is missing, deleted or no longer on the account. Preserve progress, pet claims and the bandage count, then use that same ownership decision for the page and action checks. Add deletion/recovery cases for `InCore`, `InWings` and `Remedial`, and retain rejection when the original trainee still exists on the account.

**Coverage:** `server/tests/Misc/TutorialVerification.cs:598` deletes the trainee only after setting the record to `Skipped`. Its subsequent `StartRemedial` call takes the one path that updates `CharacterSerial`, so it does not cover an orphaned active record. This is a remaining recovery gap in the deleted-character exception, rather than the previously reported ability of a living alternate character to take rewards.

## Scope and checks

Reviewed the P453 diff and its changed files:

- `CHANGELOG.md` and `VERSION`.
- `docker/uo/apply-patches.sh`.
- `server/customizations/ClusterFAccountData.cs`.
- `server/customizations/Tutorial/ClusterFTutorial.cs`.
- `server/customizations/Tutorial/TutorialCreature.cs`.
- `server/customizations/Tutorial/TutorialFarm.cs`.
- `server/customizations/Tutorial/TutorialGumps.cs`.
- `server/patches/Bandage-tutorial-real-heal.patch`.
- `server/patches/Notoriety-tutorial-creature-outsiders.patch`.
- `server/tests/Misc/TutorialVerification.cs`.
- `server/tests/Tutorial/TutorialFarmVerification.cs`.

Also followed Rook's entry point, the Fountain of Youth reset, TestCenterLiveGuard, and the pinned ModernUO bandage, healing, harmful-action and backpack-delivery implementations under `D:/UO/ModernUO-pinned`. No additional actionable finding was established for the pet claim serialization, pending-companion claim checks, outsider harmful-action patch, or open-door matching.

No build, gameplay test, client session, world save/load or live-account inspection was run. The scenarios above follow the source paths and remain unverified in a running shard. P453's reported build results were not independently rerun. No tests were added or changed, and no connection to Haven was made.

Ran the required progress reporter with the work-copy path overrides and `--dry-run`; it exited successfully and recognized version `2026.10.24.11`. That mode still rewrote `tools/progress.json`, so its incidental output was restored byte for byte from HEAD. README and progress files are unchanged. Only this review note is delivered.

P573 DONE
