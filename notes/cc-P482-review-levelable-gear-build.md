# P482: review of levelable crafted gear (P261 and P285)

Reviewed October 23, 2026. Notes only; no code changes.

Read P285's merge notes, P261's implementation notes, and P379's review of the same merge. P379 finding 1 already covers the pet-death XP exploit and its misleading live-pet test; that finding is excluded here. P261's explicitly deferred creature-level floor, per-minute limit, material budget, owner-level rules, and Echo decision are also excluded.

## Findings

1. **bug: Imbuing can exceed the shared property-slot limit.** `server/customizations/ArtificersImbueGump.cs:1799` counts only stored item properties, so buying five distinct properties on a plain crafted ring through `server/customizations/LevelGear/ClusterFLevelGear.cs:612` still leaves imbuing free to add a sixth distinct property, and both systems' bonuses remain effective. Use a shared count of stored and level-bought properties when imbuing, and add a regression that buys properties first, then attempts to imbue a different one past the limit.

2. **bug: Extra accessory slots lose level bonuses and earn no item XP.** `server/customizations/Accessories/ClusterFAccessories.cs:302` adds only a jewel's stored attributes, while `server/customizations/LevelGear/ClusterFLevelGear.cs:556` walks only direct mobile items, so moving a levelable bracelet into an unlocked extra slot removes its bought bonuses and stops its XP; a crafted toe ring can take a seal but cannot earn XP in its intended slot. Include active accessory jewels in both aggregation and XP awards, with tests for an extra bracelet, an active toe ring, and a toe ring smothered by shoes.

3. **risk: Material Luck is outside the advertised per-item ceiling.** `server/customizations/LevelGear/ClusterFLevelGear.cs:175` reads the catalogue's raw `Attributes.Luck`, so a normal gold item with no stored Luck can buy 100 and contribute 140, while an exceptional gold item can buy 150 and contribute 210 after the material multiplier (`server/customizations/ResourceInfo.cs:189`, `server/customizations/ClusterFExceptionalMaterial.cs:43`, pinned `Projects/UOContent/Misc/AOS.cs:644`). Include `GetLuckBonus()` in the existing-value calculation and test both qualities, or explicitly document that the ceiling applies only to enchanted Luck and allows material Luck on top.

4. **risk: Item XP reaches owners who have left the fight entirely.** `server/customizations/LevelGear/ClusterFLevelGear.cs:490` accepts any undeleted player in the damage attribution and `:533` awards their currently worn gear without checking map, range, or presence, so pet damage can keep leveling an owner's gear while the owner is safely elsewhere. Define the allowed presence rule, enforce it before awarding, and test a contributor who recalls away and a pet owner on another map; this is separate from the already documented lack of a creature-level floor or per-minute limit.

5. **risk: Repair, trade, and player-death preservation have no regression coverage.** `server/tests/Misc/LevelGearVerification.cs:372` tests only the store's direct buffer round trip, and none of its seven facts repairs an item, trades it, or carries it through a player's death and recovery, so a later lifecycle change can discard or misapply progression without failing these tests. Add those cases with assertions for serial, level, XP, points, bought bonuses, and the new wearer's effective values, plus a full world save/load case that checks bonuses after re-equipping.

6. **nit: Saving does not remove deleted-item rows from memory.** `server/customizations/LevelGear/ClusterFLevelGear.cs:251` filters deleted items into a temporary list for disk output but leaves `Rows` unchanged, so sealing and destroying items accumulates stale states and makes each subsequent save scan them until restart. Remove stale entries on the game thread, with a test that checks the in-memory registry after cleanup instead of only after deserialization.

## Evidence and limits

Reviewed code at ShatteredLegacy `d58c75e164cb580446a24338f2999e64b487d5c0`. Dependency reads used the read-only `D:\UO\ModernUO-pinned` checkout, verified at `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`; pinned paths above are relative to that checkout.

Read all four files in `server/customizations/LevelGear/`, `server/customizations/Mobiles/PlayerMobileSetResistances.cs`, `server/patches/AOS-level-gear-attribute-aggregation.patch`, its application in `docker/uo/apply-patches.sh`, and all seven facts in `server/tests/Misc/LevelGearVerification.cs`. Followed the relevant catalogue and imbuing checks, accessory aggregation and equip paths, companion resource maxima, material Luck readers, damage attribution, repair and death paths, and GenericPersistence serialization/load ordering.

The first finding follows from the two different property counters and the lack of a slot check in `EffectiveBonus`; the second follows from the direct-item loops and the accessory reader's raw attribute access. The material Luck totals are arithmetic from the checked getters and defaults, not a measured client result. All findings are source-review conclusions; their suggested runtime regressions have not been run.

No level reset was found in normal repair, trade, or player death: the registry follows the item serial, repair updates the existing item's durability, and death moves existing items between containers. No mismatched save-field order or serialization-version defect was found. These observations do not establish a full world restart or lifecycle test pass, and character deletion or destruction of the item itself is outside that preservation claim.

No additional wearer-total cap bypass was established. The material Luck concern is about an individual item's stated ceiling, not a global wearer Luck cap. P261 already records that individual attribute consumers and summon/provocation/spell attribution lack complete tests, so those existing gaps are not listed again.

No build, server test, client session, deployment, or Haven connection was performed. No tests were added. `tools/progress.py --dry-run` completed with exit 0 using the two work-copy paths; its live surface count was 1,610 customization files, 154 patch files, and 1,451 test markers in 229 files. Despite its help text, this command writes `tools/progress.json` from `build()` before checking the dry-run flag (`tools/progress.py:722`, `:737`); its generated change was restored to the initially clean baseline, leaving only this review note.

P482 DONE
