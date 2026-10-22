# P402: Noted by the System code review

Reviewed 2026-10-22. Review notes only. No code changes.

## Summary

The review found correctness issues, maintenance risks, and missing tests for P263 and its P361 merge. I found no achievement ID collisions or path that grants the same achievement's AP and reward twice during ordinary event processing.

The findings below come from source inspection, not a running shard or a client reproduction. Suggested fixes are for a later implementation task.

## Scope and evidence

- Code work copy: `D:\UO\golems\Valorite-tower\ShatteredLegacy`, HEAD `1ecd9f3cc786db045d5619d89ee4e15f1f279784`.
- Notes work copy: `D:\UO\golems\Valorite-tower\shard-migration`, HEAD `c99448b8ca1bb385fbd03253e747248e83fb5711`.
- Pinned source: `D:\UO\ModernUO-pinned`, HEAD `d4531cd94b739613155225c234900de9f47d2c88`, with a clean working tree. Upstream citations below are relative to that directory; other code citations are relative to the code work copy.
- Read both work copies' `AGENTS.md`, `docs/direction-decision.md`, `docs/tasks.md`, and the P263 and P361 notes before reviewing. Also checked the original list at `D:\UO\cc-prompts\design\f-exploit-achievements-accessory-slots.md`; it explicitly allows AFK and unattended farming.
- Counted registration calls and resolved their string constants across these definition files: `server/customizations/ClusterFAchievements.cs`, `server/customizations/ClusterFJokeAchievements.cs`, `server/customizations/Accessories/AccessoryAchievements.cs`, and `server/customizations/ClusterFNotedBySystem.cs`. They contain 145 registrations with distinct keys, including P263's 45 and P262's five additional `noted.*` entries, for 50 entries with that prefix.
- Reviewed `ClusterFNotedBySystem.cs`, `LootBoxes/NotedJokeItems.cs`, `ClusterFStoreBought.cs`, the achievement grant and persistence code, loot box award and opening code, League title definitions and picker, smith commission generation and completion, commission gump actions, `LargeBODItemFill.cs`, `SmithGuildSalvageBag.cs`, and `Services/Pet Training/PetTrainingHooks.cs`, all under `server/customizations/`. Checked `SmithGuildBook.cs` for the large commission actions.
- Reviewed `server/patches/Mining.cs` and the eight patches listed by P263: `Recall-arrival-achievement.patch`, `Moongate-arrival-achievement.patch`, `Runebook-full-achievement.patch`, `PetOrders-release-achievement.patch`, `CraftItem-fail-streak-achievement.patch`, `Resmelt-recycle-achievement.patch`, `SalvageBag-recycle-achievement.patch`, and `SmallBOD-crafted-only.patch`. Checked their registration in `docker/uo/apply-patches.sh` and the existing animal taming hook.
- Reviewed all nine facts in `server/tests/Misc/NotedBySystemVerification.cs` and related assertions in `AchievementEarnedLineVerification.cs`, `AchievementProgressLineVerification.cs`, `AccessorySlotsVerification.cs`, `BODCombineContainedVerification.cs`, `PostValoriteBODMaterialVerification.cs`, and `LargeBODItemFillVerification.cs` under `server/tests/Misc/`, plus `server/tests/Services/BulkOrders/BulkOrderSystemVerification.cs` and `server/tests/Items/SalvageBagIngotReturnVerification.cs`. Searched the full `server/tests/` tree for the affected keys, hooks, and policy setting before recording missing coverage.

## Findings

1. **F01 | bug | `server/customizations/ClusterFNotedBySystem.cs:609`, `:621`.** The checks for Geography Major and Not My Problem use temporary damage entries as proof that damage never happened, but healing to full clears those entries and lookups also prune expired entries (`Projects/Server/Mobiles/Mobile.cs:2043`, `:5880`), so previously disqualifying damage can disappear before the kill. Track the disqualifying damage for the relevant encounter, with explicit cleanup, and add cases that heal to full or expire the damage entry before death.

2. **F02 | bug | `server/patches/Mining.cs:299`; `server/customizations/ClusterFNotedBySystem.cs:767`.** Rock Bottom and Still Nothing retain their streak when a player successfully mines another vein, because only a failed resource check updates the streak, so returning to the original empty tile can finish an interrupted run. Reset the streak on an intervening qualifying mining attempt at another tile or a successful resource check, and cover an empty-at-A, successful-at-B, empty-at-A sequence.

3. **F03 | bug | `server/customizations/ClusterFNotedBySystem.cs:785`, `:815`.** Ground checks use the departure tile because the movement event runs before `SetLocation` (`Projects/Server/Mobiles/Mobile.cs:4103`, `:4386`), and the classifier has no Z argument, so terrain or a fire field on another floor can count toward Hot Foot or Frostbitten without being the surface walked on. Count a completed move at its destination and classify the surface or field at the player's height, with regressions for entering and leaving the terrain and crossing a bridge or upper floor.

4. **F04 | bug | `server/customizations/ClusterFNotedBySystem.cs:626`.** A visible owner exactly 15 tiles from the pet does not qualify for Remote Work even though its stated boundary is 15 or more, because `InRange(..., 15)` includes 15 (`Projects/Server/Mobiles/Mobile.cs:3076`). Exclude only the range below 15 and test visible owners at 14, 15, and 16 tiles.

5. **F05 | bug | `server/customizations/ClusterFSmithCommissions.cs:675`.** Pre-Crafted fires from small commission completion at line 755, but `CompleteLarge` never calls the hook, so an otherwise qualifying large commission cannot earn it despite the definition saying simply "a commission." Call `CommissionCompleted` once when a large commission completes, using its existing `IssuedAt`, and cover both sides of the time boundary through final piece turn-in.

6. **F06 | risk | `server/customizations/ClusterFNotedBySystem.cs:861`.** Mule Train checks follower coordinates without checking the follower's map or dead-pet state, so an off-facet follower at matching coordinates or a dead bonded pack animal can contribute; `InRange(Point3D, ...)` checks X and Y only (`Projects/Server/Mobiles/Mobile.cs:3076`). Require a living, unstabled follower on the owner's map and test off-facet and dead followers as exclusions.

7. **F07 | risk | `server/customizations/ClusterFNotedBySystem.cs:738`, `:751`.** The recycle checks accept any fresh player-crafted item, including one handed over by another player, although the definitions describe the recycler's own work; the assumption that another player's item cannot reach the pack in time is explicitly acknowledged in P263's notes and is not enforced. Record the actual crafter independently of an optional maker's mark, or deliberately change the displayed contract, and test a fresh item passed between players.

8. **F08 | risk | `server/customizations/ClusterFNotedBySystem.cs:647`, `:666`, `:712`, `:760`, `:806`, `:883`.** The static tracking dictionaries retain strong references to players and creatures without lifecycle cleanup, and released pets that are never retamed remain in `_released` even after its time window passes or the pet is deleted. Expire release records and remove tracking state on entity deletion, using weak references or bounded storage where appropriate, then verify that repeated release-and-delete activity does not keep growing the tables.

9. **F09 | risk | `server/customizations/ClusterFNotedBySystem.cs:694`, `:473`.** Every newly filled runebook creates a permanent per-account counter even after Rune Archivist is earned, and refilling an already recorded book continues incrementing its marker, so routine book activity keeps adding saved state with no remaining achievement benefit. Stop recording books once the account reaches the highest tier and use a membership marker rather than an ever-increasing counter; all of these counters are serialized by `server/customizations/ClusterFAchievements.cs:1823`.

10. **F10 | risk | `server/customizations/ClusterFNotedBySystem.cs:815`, `:821`; `server/customizations/ClusterFAchievements.cs:1253`.** Every eligible movement event reads dynamic items, land, and static/multi tiles even for a player whose equipment cannot qualify, and each movement-triggered notification filters and sorts the full definition collection even after that account has earned the relevant tiers. Check equipment and remaining achievement eligibility before terrain work, cache definitions by trigger, and stop unnecessary grant checks at the final tier; actual server timing and allocation cost remain unmeasured.

11. **F11 | risk | `server/tests/Misc/NotedBySystemVerification.cs:323`, `:423`, `:768`.** The data checks cover registration but do not positively exercise Frostbitten, Mule Train, Pantsless Wonder's final threshold, or most follow-up tiers, so a missing or incorrect threshold can survive the nine family tests. Add one-short, threshold, and repeated-event cases for each live counted tier, plus focused positive and negative cases for snow and pack followers, checking AP and reward delivery as well as the earned key.

12. **F12 | risk | `server/tests/Misc/NotedBySystemVerification.cs:300`, `:354`, `:388`, `:431`, `:455`.** Retaming, recall counting, movement counts, crafting, and recycling are substantially tested through direct hook calls, which cannot detect a disconnected patch or the ground lookup error, and the pet-death case does not exercise a bonded pet. Add tests through the actual patched operations, including completed movement and bonded death/resurrection, and a save/load case that confirms noted counters and earned rewards remain account-wide and cannot be granted again.

13. **F13 | risk | `server/tests/Misc/NotedBySystemVerification.cs:674`; `server/customizations/ClusterFStoreBought.cs:21`.** The crafted-only tests reject a bought item for a small smith deed and a small commission, but do not assert that bought items are rejected by large direct fills, large commission pieces, or tailoring, and no test sets `CraftedOnly` to false. Cover each affected entry point and the disabled setting, restoring the setting afterward so a future refactor cannot silently bypass or permanently enforce the policy.

14. **F14 | risk | `server/customizations/SmithGuildBook.cs:684`; `server/customizations/ClusterFSmithCommissions.cs:570`.** The related reroll fix still permits unlimited large commission abandon/request cycles because the large abandon action never records a cooldown and `GenerateLarge` never checks one, a limitation already disclosed by P263. Apply a cooldown to both large actions if the fix is meant to cover all commissions, and add a regression through the book's large commission buttons.

## Checks with no additional finding

- **Duplicate awards:** nothing found in ordinary processing. `ClusterFAchievements.cs:1336` adds the earned key to an account-wide set before AP, Renown, title, or loot box work, and a repeated add returns before those effects; the title path also uses a set at `ClusterFNotedBySystem.cs:948`.
- **Death event overlap:** nothing found that calls the Noted death handler twice for a normal death. The deletion event covers ordinary creatures, while the death event branch requires a bonded controlled pet; pinned `BaseCreature.cs:3482` handles bonded death without the ordinary deletion path, and `:3674` raises the deletion event before clearing the master.
- **ID collisions:** nothing found among the registration sources listed above, including P231 and P262. The `noted.*` prefix is shared intentionally, not itself a collision, and P361 preserved the separate accessory trigger members before the new P263 members.
- **Titles and joke rewards:** nothing additional found in the P361 `HiddenUntilHeld` merge, reward key references, or the reviewed bound joke-item and Dented Box paths. The existing test verifies title visibility, reward references, and blessed/statless items, but this review did not prove their client appearance or every transfer route.
- **Farming:** repeated refusal clicks, repeated release/retame cycles, repeated terrain traversal, and preparing items before requesting a commission are easy to automate, but match the source design's express farming allowance. They do not bypass the account's once-only award guard, so ease of farming alone is not listed as a defect.
- **Known unreachable entries:** `noted.middle_management`, `noted.deja_vu`, `noted.procrastinator`, `noted.cold_feet`, and `noted.infamous` remain definitions without production notifications for their trigger kinds. This is the intentional data-only set disclosed by P263, not a newly discovered wiring regression; `NotedBySystemVerification.cs:761` checks their hidden metadata, not reachability.
- **Known coverage limits:** P263 already discloses the missing Sacred Journey and scissors hooks and the mining-only depleted-resource behavior. The source still has those limits; do not read its generic earned descriptions as proof that every travel, recycle, or harvest route is wired.
- **Tick hooks:** the reviewed Noted class installs a movement handler, not a periodic tick or think handler. F10 describes the movement cost; follower and house checks additionally run every tenth counted step at `ClusterFNotedBySystem.cs:839`.

## Validation and limits

This was a source review with no lane tests, as requested. No new tests were written, existing tests were not run, and no Docker build, deployment, account operation, or Haven connection was performed; historical P263/P361 green builds are not claimed as validation of these findings.

Ran `tools/progress.py --dry-run` with paths set to these work copies. That mode still writes `tools/progress.json`; restored that generated file to its original tracked contents so the deliverable stays notes-only.

Runtime reproductions, timing measurements, save/load behavior, and client rendering remain unverified. No files under `docs/` were edited, and no commits, merges, pushes, or branch switches were made.

Final checks: the code working tree is clean; the only notes-repo change is this report. The report is below 5 MB and contains no em dashes.

P402 DONE
