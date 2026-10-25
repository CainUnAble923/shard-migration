# Hammer of Hephaestus

Player guide draft checked against source on October 25, 2026, including T3 from P168 and P372. The running shard and client have not been checked. Recovery rates below are the configured rates; known recovery issues still need follow-up.

## Get your first hammer

Join the **Society of Smiths** at **Forge and Anvil, New Haven, Trammel**. Joining is free and has no skill requirement. Open the Guild Directory with `[guild`, choose the Society, and use **Show me the way** to find its guildmaster.

On the guild's **Starter items** page, take the **Hammer of Hephaestus**. Your first copy is free, with no Apprentice task required.

You can also earn it from George Hephaestus's **It's Hammer Time!** training quest, which asks you to reach 50.0 Blacksmithy. Take that quest before reaching its skill threshold. The quest and guild share the same first claim, so completing one route does not give a second free hammer through the other.

## What each tier does

All available tiers are blessed, keep Metal Familiarity, and survive running out of uses. Equip the hammer to receive its Blacksmithy bonus. Keeping it in your backpack gives no held skill bonus.

| Tier | Name | Maximum uses | Recovery | Blacksmithy while held | Familiarity cap per metal | Familiarity benefit |
|---|---|---:|---|---|---:|---|
| T1 | Hammer of Hephaestus | 150 | 1 use per 30 minutes | +5 | 1,000 | Up to a 20% chance to refund a hammer use after a successful craft. |
| T2 | Reinforced Hammer of Hephaestus | 400 | 1 use per 15 minutes | +10, plus up to +2.5 from familiarity | 2,500 | Extra skill based on total familiarity across all supported metals. |
| T3 | Masterwork Hammer of Hephaestus | 800 | 1 use per 10 minutes | +15 | 5,000 | Refunds up to 25% of a successful craft's ingots and adds **Craft This Order**. |

Each tier has its own familiarity benefit. T2 replaces T1's use refund with extra skill. T3 replaces that extra familiarity skill with ingot savings. The benefits do not accumulate across tiers.

**T4 is not available.** The exceptional-quality benefit mentioned in the familiarity panel is future work.

## Build Metal Familiarity

Familiarity belongs to the hammer and is tracked separately for each supported metal, from Iron through Celestial. Successful smithing with that hammer rolls for a gain: +1 for a normal item or +3 for an exceptional item. Failed crafts add none.

The gain chance starts at 100% for an unfamiliar metal, falls as familiarity approaches the tier's cap, and never falls below 5% before the cap. Exceptional results increase the amount gained, not the chance of gaining.

Open the hammer's context menu and choose **Metal Familiarity** to see your progress. Double-clicking it away from a forge also opens that panel. Near a forge, double-clicking normally opens the smithing menu.

T1's use-refund chance reaches 20% at that metal's cap. T2's extra skill depends on familiarity across the whole metal list, so mastering one metal does not give the full +2.5.

T3's saving depends on familiarity with the metal being crafted. At 2,500 familiarity it averages 12.5%; at 5,000 it averages 25%. The hammer returns whole ingots and rolls for the fractional remainder. A successful 25-ingot craft at full familiarity returns 6 ingots, with a 25% chance of a seventh.

Bring the full recipe cost in your backpack: the saving is refunded after success. Failed crafts receive no refund. Other recipe materials are not refunded.

## Upgrade and recharge

Open **Hammer of Hephaestus Upgrades** at the Society guildmaster. Keep your hammer equipped or loose in the main backpack so the page can find it. It must not be exhausted when upgrading.

| Upgrade | Society standing threshold | Blacksmithy required | Smithing Seals | Gold | Iron Ingots | Valorite Ingots |
|---|---|---:|---:|---:|---:|---:|
| T1 to T2 | 5,000, Journeyman threshold | 80.0 | 25 | 10,000 | 500 | 100 |
| T2 to T3 | 15,000, Master threshold | 100.0 | 60 | 25,000 | 1,000 | 250 |

The hammer upgrade checks your current Blacksmithy, including equipped bonuses. Guild rank promotion has its own base-skill checks. Costs can come from your backpack and bank. Spending Seals does not spend standing.

Upgrading replaces the old hammer with a fully charged hammer of the next tier and carries over its familiarity values. Those values do not increase automatically to match the new cap.

For an immediate recharge at any available tier, use **Restore Hammer to Full Uses** on the same page. It costs **10 Smithing Seals and 200 Iron Ingots**, from your backpack and bank. Otherwise, let the hammer recover uses over time.

## Fill bulk orders with any tier

All available tiers can automatically file newly crafted matching gear into smith bulk order deeds, or BODs, for a Society member. Keep loose deeds or your **Smithing Guild Book** in the main backpack. Craft with the hammer as usual, choosing the item and metal yourself.

The hammer checks small deeds before large deeds and uses the first matching open request. It consumes the item into the deed and reports progress in your journal. Large smith deeds can accept individual crafted pieces directly, as well as completed small deeds.

Match the requested item, metal, and exceptional quality. A deed without a named metal can accept colored metal during ordinary auto-filing, so check your selected material. To keep a crafted item, put matching deeds and the book away from your backpack before crafting.

## T3: Craft This Order

1. Equip a usable **Masterwork Hammer of Hephaestus**.
2. Put an unfinished small or large **smith** deed in your backpack. Take it out of the book so you can target it directly.
3. Stand within 2 tiles of both an anvil and a forge. Put the required ingots and other recipe materials in your backpack and leave room for rejected items.
4. Open the hammer's context menu, choose **Craft This Order**, and target the deed.
5. Stay still and watch the progress window and journal. Use **Stop**, or close the progress window, to stop after the current attempt finishes.

The hammer selects the required item and metal, using Iron when the deed names no metal. It makes one normal crafting attempt at a time. Skill requirements, learned designs, skill rolls, possible skill gains, material costs, hammer uses, familiarity, and T3 savings still apply.

The selected deed gets first chance at each result. An exceptional-only deed rejects normal-quality items. Rejected items remain available in your backpack, although another matching deed can take them through ordinary auto-filing. Failed attempts still cost materials and uses, and the run continues while it can.

For a large order, the hammer first tries to combine completed small smith deeds lying loose in your main backpack. It then crafts the missing pieces, moving through unfinished lines automatically. **Put completed small deeds you want to keep in the bank before starting.** Combining consumes a whole small deed, even if a partially filled large-order line needs only a few more items.

The run ends when the deed is full, or stops when you move, take damage, die, remove the hammer, remove the deed, run out of materials or uses, fill your backpack, become overloaded, or start another craft. It also stops if you cannot make the required item, or after 500 attempts. Stops take effect around the current attempt, so stopping does not refund work already underway.

Progress already filed into the deed stays there. Fix the cause, then choose **Craft This Order** and target the unfinished deed again to continue.

Crafting the order does not turn it in. Open the deed to review its Society payout and your **Completed orders** setting, then submit it through the Society's normal turn-in route. Reopen the deed after a trade or guild change if its tooltip looks outdated. See the [Society of Smiths guide](society-of-smiths.md) for orders, standing, and Seals.

If the context-menu label is blank, check that your Shattered Legacy player package is current. The label needs the package's custom text entry; client rendering has not been verified for this draft.

## Source record

- [P600 source checks and limitations](../cc-P600-guide-hammer.md).
- [P168 implementation notes](../cc-P168-hammer-t3-craft-order.md) and [P372 integration notes](../cc-P372-cont-fixup-hammer-t3-craft-order.md).
- [P587 review](../cc-P587-review-hammer-t3.md), including unresolved recovery, exhaustion, large-deed combining, and tooltip issues.
