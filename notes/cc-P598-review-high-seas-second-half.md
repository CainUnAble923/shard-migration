# P598: review of High Seas fishing, second half

Reviewed 2026-10-25. Notes only. No code changed.

The merged implementation still needs fixes. The hook duplication and crate-carving findings from the earlier reviews remain present. Bait has the same stale-cursor problem, and ordinary players cannot earn the new hooks, Oracle, or Charybdis bait through the current order system.

## Scope and evidence

Read both work copies' AGENTS.md, direction-decision.md and tasks.md, then:

- `notes/cc-P269-high-seas-fishing-second-half.md`
- `notes/cc-P269-high-seas-fishing-second-half-codex-review.md`
- `notes/cc-P587-cont-fixup-high-seas-fishing-second-half.md`
- `notes/cc-P587-cont-fixup-high-seas-fishing-second-half-codex-review.md`
- The original P269 prompt at `D:/UO/cc-prompts/completed/cc-P269-high-seas-fishing-second-half.md`.

Code reviewed at `8b0ccb8`, including P269's `19fd417`, its imported fix-up `30b225c`, and merge `db4c85b`. A direct diff between P269 and the fix-up is empty for the High Seas customization directory, its verification fixture, its three patches, and the FishingPole migration. The fix-up retained P269's behavior. Its patch-list conflict resolution keeps both the Hammer patches and the fishing patches, which target different upstream files. No additional conflict-resolution defect found.

All code paths below are relative to the code work copy. In the findings, `HS/` means `server/customizations/Services/Expansions/High Seas/`. Upstream citations are relative to `D:/UO/ModernUO-pinned/Projects/`, verified at clean commit `d4531cd94b739613155225c234900de9f47d2c88`. ServUO citations are relative to `D:/UO/ServUO-pub57/Scripts/`.

## Findings

### 1. High / P1: a pending hook cursor can copy a consumed hook

**Location:** `HS/Items/Fish/Hooks.cs:89`, especially lines 102-120.

**What happens:** Player A opens a hook's target cursor, then hands the hook to player B. B attaches it to a pole, deleting the hook. A finishes the original cursor on another pole. The callback checks the targeted pole, but never checks whether its stored `_hook` was deleted or still belongs to A. The deleted object's type, uses, and hue are copied to A's pole. Swapping these hooks back off the poles produces extra hook items as well as extra charges.

Pinned `Server/Targeting/Target.cs:121` checks the item being targeted. It does not validate the source hook stored in the cursor. This is the same issue reported by both earlier code reviews, still unfixed. ServUO's hook callback also lacks the guard; this is an inherited duplication bug with a broken result.

**Fix:** Before returning an old hook or changing a pole, require the source hook to exist, remain in the acting player's backpack, and have positive uses. Spend that validated source once. Add a regression covering a cursor completed after another player consumes the hook.

### 2. High / P1: bait cursors can duplicate charges after the cup is consumed

**Location:** `HS/Items/Fish/Bait.cs:177`, with the captured amount at lines 168-174 and charge changes at lines 202, 222, and 234.

**What happens:** A opens a bait target for a selected amount, then transfers the cup to B. B uses or combines the bait. A can still finish the old cursor on A's own pole, trap, or matching bait cup. `_amount` is added even if the source cup was deleted or no longer contains that amount, then subtracted from the stale source object. Bait can therefore be spent twice. The amount prompt also lacks source validation when it becomes a target.

`TryBeginTarget` clamps the amount only before the cursor is issued. Neither the prompt response nor `InternalTarget.OnTarget` checks current ownership, deletion, or available charges. The generic target checks do not protect this stored source object. ServUO has the same omission; copying it imports another duplication bug.

**Fix:** Revalidate the cup after the prompt and again when the target resolves. Require backpack ownership, a live source, and a positive amount no greater than its current charges before changing either destination or source. Cover the transfer-and-consume sequence for both equipment and cup-to-cup transfers.

### 3. High / P1: a completed order can pay after its fish have been carved

**Location:** `HS/Quests/ProfessionFishQuest/ShippingCrate.cs:289`; related `HS/Items/Fish/Fish.cs:29` and `HS/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs:173`.

**What happens:** Put the requested fish in the crate, then carve them with a blade. `BaseHighseasFish.Carve` calls `ScissorHelper` without consulting the crate. The fish become steaks while `_orderHave` still marks the order complete. Delivery pays the reward and reputation before `DeleteQuestItems` calls `ConsumeTotal`, whose failure is ignored. The remaining steaks are moved to the hold, so the player keeps the carved goods and receives payment for fish no longer present.

`CheckLift` does not intercept carving. Pinned `Server/Items/Item.cs:4371` consumes the fish directly and tries to place the steaks in its container. ServUO supplies the missing `ShippingCrate.CheckCarve` restriction and calls it from its fish's `Carve`. Both earlier code reviews reported this integration omission, which remains unfixed.

**Fix:** Restore the crate's carving restriction in the fish path. Independently verify and consume the actual required fish before changing reputation or issuing a reward. A shortage must leave the order unpaid. Cover carving followed by attempted delivery.

### 4. High / P1: classic-boat orders cannot award the new hooks or Oracle

**Location:** `HS/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs:116`; related `PlayerFishingEntry.cs:68` and `FishQuestHelper.cs:84`, `:121`, and `:215` in that same directory.

**What happens:** Every available boat receives exactly one order line, clamped to 5-20 fish. `GetPointsAwarded` awards at most three points per fish, so even the largest dungeon-fish order is worth only 60 points. Rewards use that order's points, not accumulated reputation. Tier 2 starts at 100. Consequently, all current orders pay tier 1, which contains no LavaHook, JunkProofHook, DredgingHook, or OracleOfTheSea. Repeating orders or raising reputation never changes this.

Charybdis bait is further restricted to tier 4. The explicitly copied ascending tier checks prevent tier 4 even if multi-line orders become available. `FishInfo` marks Charybdis as `cannotfishup`, and the reviewed reward and acquisition paths supply no alternative. Thus lava-pole fishing and the Oracle summoning chain remain staff-only. The P269 note's statement that orders pay tier 1 or 2 understates the actual restriction in this build.

**Fix:** Close or explicitly defer this acquisition dependency. Faithful multi-line galleon progression is needed to reach tier 2 under the original points rules. Charybdis bait additionally needs an approved resolution of the copied tier bug or another approved acquisition path. Do not silently replace order points with reputation or change OSI values. Add an acquisition test that starts with an available player boat and earns the required equipment; constructing it directly does not cover this gap.

### 5. Medium / P2: an unrelated boat can satisfy delivery of a remote crate

**Location:** `HS/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs:46` and `:87`; related completion at line 162.

**What happens:** Talk selects the player's nearest owned boat and computes one `inRange` flag. `HasFishQuest` uses that flag for every order without checking `order.Boat` or the crate's location. A player can fill a crate on boat A at the departure port, recall to the delivery port where boat B is parked, and collect payment while boat A and the cargo remain behind. `Complete` does not recheck the monger, boat, or crate location when the gump response arrives.

The corresponding ServUO helper has the same broad nearest-boat check. This is an inherited delivery-validation bug, not a fix-up merge regression.

**Fix:** Validate each order against its recorded boat and hold. Require that boat and the crate to be at the destination on the correct facet, and revalidate the player and destination when paying. Cover a completed crate left at departure while a second owned boat is at delivery.

### 6. Medium / P2: players have no usable way to resign an unfinished order

**Location:** `HS/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs:277`; related `ShippingCrate.cs:223`, `:229`, and `:304` in the same directory.

**What happens:** The standalone progress gump only has Close. The note says resigning means destroying the crate, but the crate has no destroy action. Its `DropToItem` refuses container drops, including into a trash barrel or the shard's trash bag, and its world-drop override refuses ground drops. Its SmallCrate parent supplies no chopping action. The normal ServUO quest-log resignation path was removed with that framework. A player who wants to abandon an order therefore cannot invoke the intended resignation behavior through this interface.

The current test calls `forfeit.Delete()` directly. That proves the server-side penalty, but not player access to cancellation. Pinned `UOContent/Multis/Boats/BaseBoat.cs:614` also refuses dry docking with anything in the hold, so leaving the unwanted crate there blocks normal docking.

**Fix:** Add an owner-validated Cancel Order action to the existing order UI or crate context menu. Recheck ownership on response, apply the resignation penalty once, and dispose of the crate through that action. Exercise the player action rather than direct deletion in its regression test.

### 7. Medium / P2: Corgul's Mysticism handbook was omitted on a false dependency claim

**Location:** `HS/Mobiles/Corgul/CorgulTheSoulbinder.cs:122`; the false premise is also at line 21 and in `HS/Items/Artifacts/CorgulsHandbookOnTheUndead.cs:5`.

**What happens:** Corgul's guaranteed unique reward is drawn from only the sash and undead handbook. The Mysticism handbook was excluded because the port searched for ServUO's `MysticBook` name. Pinned already supplies the equivalent `UOContent/Items/Skill Items/Magical/MysticSpellbook.cs:7`, including Mystic book type, offset 677, and 16 spells. Its Spellbook base provides the artifact attributes. The omission removes requested loot and increases the other unique artifacts' shares.

This repeats the earlier P269 review finding. Proposed deviation D-177 does not justify a loss whose stated missing dependency actually exists.

**Fix:** Port `CorgulsHandbookOnMysticism` onto `MysticSpellbook` with ServUO's hue, label, and attributes, then restore it to `UniqueList`. Correct the missing-dependency note. Update the test that currently asserts a two-item unique list to cover the full list.

### 8. Medium / P2: fish-pie recipes still lack obtainable seasonings

**Location:** `server/customizations/Engines/Craft/CookingCraftRegistrations.cs:98`, `:111`, `:153`, and `:188`.

**What happens:** The recipes require MentoSeasoning, SamuelsSecretSauce, or DarkTruffle, and UnicornFishPie also requires FreshGinger. The item classes exist in `HS/Items/Resources/Cooking Ingrediants.cs`, but the current customization and patch references provide no vendor, loot, or crafting acquisition path for them. Pinned supplies no acquisition path under those types either. Ordinary players therefore cannot bake the new pies even after learning the Cooking book. Staff-created ingredients in the play test bypass the missing behavior.

ServUO stocks the first three in `Services/Expansions/High Seas/Mobiles/Vendors/SBInfos/SBSeaMarketTavernKeeper.cs:23` and ginger in `VendorInfo/SBBaker.cs:34` and `VendorInfo/SBFarmer.cs:34`. P269 explicitly records the gap as a pending decision, and its earlier docs review flags it. It remains unresolved after P587. The unavailable player summoning path in finding 4 also prevents relying on summoned Charybdis as a general pie source.

**Fix:** Port the original vendor acquisition paths and necessary placement, or obtain an explicit scope deferral before describing player pie crafting as finished. Verify buying the ingredients and crafting a pie through the normal recipe gate.

## Review coverage and limits

Reviewed the implementation files identified by P269, including:

- `HS/HighSeasFishing.cs`, `Generate.cs`, and `Persistence.cs`.
- `HS/Items/Fish/Bait.cs`, `Hooks.cs`, `FishInfo.cs`, and `FishPies.cs`.
- `HS/Items/OracleOfTheSea.cs`, `LavaFishItems.cs`, `LobsterTrap.cs`, and `LavaLobsterTrap.cs`.
- `HS/Spawners/CharybdisSpawner.cs`, `Mobiles/Charybdis.cs`, and `Mobiles/BaseSeaChampion.cs`.
- `HS/Mobiles/Corgul/CorgulTheSoulbinder.cs`, `BoundSoul.cs`, `SoulboundApprenticeMage.cs`, `SoulboundBattleMage.cs`, `SoulboundPirateCaptain.cs`, `SoulboundPirateRaider.cs`, `SoulboundSpellSlinger.cs`, and `SoulboundSwashbuckler.cs`.
- `HS/Items/Artifacts/CorgulsEnchantedSash.cs` and `CorgulsHandbookOnTheUndead.cs`.
- `HS/Quests/ProfessionFishQuest/FishMonger.cs`, `FishQuestHelper.cs`, `PlayerFishingEntry.cs`, `ProfessionalFisherQuest.cs`, and `ShippingCrate.cs`.
- `HS/Quests/ProfessionFishQuest/Books/RareBook1.cs`, `RareBook2.cs`, `RareBook3.cs`, `RareBook4.cs`, `RareBook5.cs`, and `RareBook6.cs`.
- `server/customizations/Engines/Craft/CookingCraftRegistrations.cs`.
- `server/patches/FishingPole-high-seas-bait-hooks.patch`, `Fishing-high-seas-bait-hooks-lava.patch`, and `AOS-fish-pies.patch`.
- `server/migrations/Server.Items.FishingPole.v1.json`, `docker/uo/apply-patches.sh`, and `server/tests/Services/HighSeasFishingSecondHalfVerification.cs`.

Compared the relevant ServUO implementations and pinned target, item, container, harvest, spellbook, champion, regeneration, and persistence code. The Corgul island/boat integration and the other explicitly recorded missing capabilities remain deferred work; this review does not claim they were completed.

These are source-review findings. No new tests were written, and no build, test suite, client session, timer-driven fight, save round trip, or world placement was run independently for P598. P269/P587's reported successful build and boot results remain attributed to their notes. Runtime reproduction and validation of future fixes are still required. No Haven connection, deployment, account change, commit, push, merge, or branch switch was made.

Session checks: `git diff --check` passed in both work copies. The notes contain no non-ASCII characters and are below the 5 MB limit. Ran `tools/progress.py --dry-run` against these work copies with `Path.write_text` suppressed, because its report builder otherwise writes `tools/progress.json` even in dry-run mode. No generated reports changed. Only this notes file is new; the code work copy remains clean.

P598 DONE
