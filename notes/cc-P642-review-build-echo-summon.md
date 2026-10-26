# P642: review of P630, the friendly Echo summon

Reviewed 2026-10-26. Notes only. No code, tests, configuration, accounts, or world state changed.

## Scope and evidence

Reviewed P630 commit `57d64db198a27633bf45d5c97cba6a8176959a37` against code work-copy HEAD `a3f017e`. The Echo sources, its new tests, and `ClusterFAccountData.cs` have no changes between that commit and this HEAD. Migration work-copy HEAD at review start was `0bc9e0033a8f7a773a7e2478cbb1cb4932e053dd`.

Read both work-copy AGENTS.md files, the direction and task guidance, `notes/cc-P630-build-echo-summon.md`, `notes/cc-P630-build-echo-summon-codex-review.md`, and the matching design, `notes/cc-P567-design-summons-league-reward.md`. Chase's original choice is recorded in `D:/UO/overseer/decisions-2026-10-22.md:15-16`. His acceptance of P567's defaults is recorded in `D:/UO/overseer/decisions-2026-10-23.md` under the 20:15 entry for 10-25 and repeated in the completed P630 prompt. The accepted defaults are Mythril, a reusable Tome, one weak Stygian Dragon Echo, 20 seconds, two slots, and a 30-minute account cooldown.

P630 is packet 1 only. The Tome, Registrar entry, and player pages belong to packet 2. Their absence is not a finding. The default switch, rank key, duration, slot cost, cooldown, and fixed creature profile match the accepted defaults in source.

Implementation and test files inspected, including P630's serializer changes and test adjustments:

- `server/customizations/LeagueEchoes/LeagueEchoSettings.cs`
- `server/customizations/LeagueEchoes/LeagueEchoPolicy.cs`
- `server/customizations/LeagueEchoes/LeagueEchoSystem.cs`
- `server/customizations/Mobiles/LeagueEchoes/LeagueDragonEcho.cs`
- `server/customizations/ClusterFAccountData.cs`
- `server/tests/Misc/LeagueEchoesVerification.cs`
- `server/tests/Mobiles/LeagueDragonEchoVerification.cs`
- `server/tests/Misc/AccountDataSerializerVerification.cs`
- `server/tests/Misc/LeagueShopVerification.cs`
- `server/tests/Misc/RequisitionsVerification.cs`
- `server/tests/Mobiles/Mule/MuleVerification.cs`

Also traced the relevant reward handlers in `ClusterFNotedBySystem.cs`, `ClusterFAchievements.cs`, `LootBoxes/ClusterFLootBoxes.cs`, `LevelGear/ClusterFLevelGear.cs`, `Mobiles/Evo/EvoPet.cs`, `Requisitions/RequisitionLeads.cs`, `ClusterFRareSelfRepair.cs`, and `Imbuing/ClusterFImbueEffects.cs`. Shard paths below are relative to the code work copy. Engine paths are relative to `D:/UO/ModernUO-pinned/Projects`; its HEAD is the required `d4531cd94b739613155225c234900de9f47d2c88`, and its working tree was clean.

This is a source review. The behavior below is traced through the actual implementations, but was not reproduced in a running test or client during P642. No Docker gate or shard was started. P630's reported green build is not an independently verified result of this review.

## New findings

### R1. Medium (P2): a lethally damaged Echo can award pet-loss achievements

**Location:** `server/customizations/Mobiles/LeagueEchoes/LeagueDragonEcho.cs:108`, with the unguarded consumer at `server/customizations/ClusterFNotedBySystem.cs:660`. The test gap is at `server/tests/Mobiles/LeagueDragonEchoVerification.cs:119`.

**What happens:** If a monster kills the Echo while its owner is at full health, the owner gets a `PetDiedAtFullHp` event. That event advances a saved achievement counter and can grant Acceptable Losses or Meat Shield Procurement. This violates the design's requirement that destroying the Echo grant no achievement, AP, Renown, or loot-box reward (`cc-P567-design-summons-league-reward.md:149-151`). It does not require a player to bypass Trammel's harmful-action rules: a wild enemy can deal the lethal damage.

The source path is:

1. Engine `Server/Mobiles/Mobile.cs:6016-6024` sets `Hits = 0` before calling `Kill()` for damage exceeding the remaining hits.
2. The Echo's `OnBeforeDeath` calls `Dissolve`, which calls `Delete` at `LeagueDragonEcho.cs:127`. Skipping normal death correctly avoids `CreatureDeathEvent`, but not deletion subscribers.
3. Engine `UOContent/Mobiles/BaseCreature.cs:3674` raises `CreatureDeletedEvent` before clearing the controller at line 3688. The Echo still has zero hits, its controller, `Summoned`, and `NoKillAwards`.
4. `ClusterFNotedBySystem.cs:584-587` sends any deleted creature with zero hits to `OnCreatureDied`. Lines 660-662 notify the living, full-health owner of a controlled creature's death. The controlled/summoned exclusion at line 664 comes after that notification, and this path never checks `NoKillAwards`.
5. `ClusterFNotedBySystem.cs:461-464` saves the counter and grants reached tiers. Acceptable Losses grants 5 AP for the first event at lines 173-176. Meat Shield Procurement grants 15 AP and 1 Renown at ten events at lines 180-186. `ClusterFAchievements.cs:1354-1367` applies those awards and invokes the achievement loot-box path for an online recipient. These achievements are once per account, not unlimited AP per death.

**Why the current test misses it:** `LethalDamageDissolvesItWithNoCorpse` sets `LastKiller` and calls `echo.Kill()` while the Echo still has full hits. Engine `Mobile.cs:4737` calls `OnBeforeDeath` before the normal `Hits = 0` at line 4762, so this test's deletion does not enter the zero-hit subscriber branch. It also checks the other account's generic `kills` counter, not the owner's pet-loss counter or rewards. P630 already acknowledges missing per-consumer coverage; this finding identifies a concrete failing path within that gap.

**Fix:** Exclude `LeagueDragonEcho` from the pet-loss notification before it can increment a counter, or introduce a shared no-reward check that includes the Echo and preserves ordinary pet-loss achievements. Keep its summon and no-awards flags intact. Add a regression with a full-health online owner and actual lethal `Damage` from a wild creature. Compare the owner's pet-loss counter, earned keys, AP, Renown, and achievement loot-box ledger before and after; also retain an ordinary-pet positive control. Observe the regression fail against P630 before fixing it.

### R2. Medium (P2): disconnect does not end an Echo during the logout delay

**Location:** `server/customizations/LeagueEchoes/LeagueEchoSystem.cs:65` and `:267`; call eligibility also omits online state at `:108`. The test gap is at `server/tests/Misc/LeagueEchoesVerification.cs:350`.

**What happens:** A player can disconnect in the wilderness and leave the Echo alive and able to continue its existing fight for the rest of its lifetime. The service subscribes to `EventSink.Logout`, but does not subscribe to `Disconnected`, and `WhyEnd` does not check `owner.NetState`. A disconnected character can remain alive on the same map, within the leash, with the same rank. Repeated watchdog passes then keep the Echo rather than dissolving it. The design's question 6 explicitly calls for dissolution on disconnect, and its call transaction requires a living online caller (`cc-P567-design-summons-league-reward.md:143`).

Engine `Server/Mobiles/Mobile.cs:1307-1313` raises `Disconnected` when the network state is cleared, then schedules logout after `GetLogoutDelay()`. `Logout` raises `EventSink.Logout` and internalizes the character only at lines 9056-9065. Engine `Server/Regions/Region.cs:200` defaults ordinary logout to five minutes, longer than the Echo's whole life. Young players, staff, bedroll logout, and TestCenter can have zero delay, so testing only those cases can hide this defect. `UOContent/Mobiles/PlayerMobile.cs:4011-4018` shows those player exceptions.

**Why the current test misses it:** `EveryEndingDissolvesItGivesTheSlotsBackAndKeepsTheCooldown` invokes `EventSink.InvokeLogout(pm)` directly. It does not close a connection, raise `Disconnected`, or exercise the delayed logout interval. Its `NewCharacter` helper at lines 52-63 creates characters without a NetState, and the call tests accept those offline characters, so they also fail to enforce the online-call requirement.

**Fix:** Subscribe the same idempotent owner cleanup to `EventSink.Disconnected`, keep logout cleanup as a fallback, and reject offline owners in `Check` and the watchdog. Give successful-call fixtures a connected test NetState. Add a regression using a non-young Player with a logout delay longer than 20 seconds: call, disconnect, verify immediate deletion and exact follower restoration, then advance the clock and verify the later logout does not subtract slots twice or change the cooldown. Also verify an offline call refuses without creating a creature or deadline. Observe these regressions fail before the fix.

This is separate from the earlier review's harmful-action timing finding. That finding concerns actions between watchdog passes. Here the disconnect is never recognized by any watchdog pass while the owner remains in the world.

## Earlier review and remaining acceptance

The earlier P630 Codex review was read before forming these findings. Its findings remain there and are not reissued here. R1 and R2 add different event paths and regression requirements.

No additional save-format defect was identified in the inspected v23 account and v3 character changes. The appended fields, old-version defaults, and future-version refusals match the design in source. That does not establish full world reload behavior. `ASavedEchoDeletesItselfAfterLoad` manually serializes and deserializes a creature, then checks deletion and the registry; it does not assert follower reconciliation after an actual world load. P630 already assigns that check to packet 3, so this remains an explicit release gate rather than a new duplicate finding.

P630 also explicitly carries bad-setting logging, per-consumer reward assertions, house/duel checks, bard combat, normal victim attribution, appearance, and measured solo/party balance into later packets. This review does not claim those checks passed. The feature should remain disabled through those acceptance steps and the fixes above. No new activation or operator decision was made.

## Review verification

- Read current canonical customizations and pinned engine source; did not read `server/uo/`.
- Confirmed the reviewed Echo files and account schema have not changed since P630.
- No new tests were written or executed for this notes-only task. Suggested regressions above still need red and green runs in the fixing task.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies; exit 0. The known reporter behavior still rewrites `tools/progress.json` despite `--dry-run`; restored that file to its exact starting bytes. No progress totals are claimed here.
- No Haven contact, deployment, account action, commit, merge, push, or branch switch.
- Final checks: Windows PowerShell 5.1 confirmed; whitespace checks passed; the note has no em dashes and is below 5 MB. The code work copy is clean, and the only migration work-copy change is this note. The stop-request file was absent at the final checkpoint.

P642 DONE
