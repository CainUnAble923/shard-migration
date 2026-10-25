# P579: Requisitions Appraiser numbers for P452

2026-10-24. Research and recommendations only. No code changed.

## Recommendation

Keep the configured Appraiser formula for genuine magic, but calculate its property count and intensity after excluding ordinary exceptional crafting bonuses. A quality-only exceptional weapon should receive no Appraiser offer. Keep ordinary crafted magic eligible, including the intended blessed spellbooks. Use the same price for an Appraiser sale and a requisition turn-in.

This is a proposed rule for P452, not an implemented fix or a new OSI price claim. The Appraiser is our custom system. Its premiums are substantially higher than stock vendor payments for AOS magic.

## Scope and evidence

Read both work copies' AGENTS.md, the direction decision and task list, P150's implementation notes, P422's review and its Codex review, and the relevant source below. The code work copy's HEAD and local main both resolve to `bca69995142fa5f24305880a602e6888274364f2`. There is no diff from main in `server/customizations/Requisitions/` or `server/tests/Misc/RequisitionsVerification.cs`.

`D:/UO/cc-prompts/queue/cc-P452-fix-requisitions-fix-up-appraiser-magic-test.md` exists but is zero bytes, both on disk and in that repo's HEAD. There are no P452 acceptance criteria to read. This report uses the two Appraiser/book bugs in `notes/cc-P422-review-requisitions-and-leads.md` as its working scope. P422's refresh-hour and configuration-null findings are outside this numbers check.

Paths below use these roots:

| Prefix | Root |
|---|---|
| C | Code work copy, `server/customizations/` |
| P | Code work copy, `server/patches/` |
| T | Code work copy, `server/tests/Misc/` |
| M | `D:/UO/ModernUO-pinned/Projects/UOContent/`, verified at `d4531cd94b739613155225c234900de9f47d2c88` |
| S | `D:/UO/ServUO-pub57/Scripts/`, verified at `d76bf4443cf76d081ddaf8f57c87ff33749256af` |

## What vendors actually pay

In both `M/Mobiles/Vendors/GenericSell.cs:12-58` and `S/VendorInfo/GenericSell.cs:74-88`, the normal weapon payment is:

```text
max(1, truncate(base sell-table price * quality multiplier)
       + 100 * DurabilityLevel + 100 * DamageLevel)
quality multiplier: low 0.60, regular 1.00, exceptional 1.25
```

These are payments to the player, using `InternalSellInfo`. `InternalBuyInfo` is the vendor's stock offered to the player. `GetBuyPriceFor` computes a resale price at 1.90 times the sell payment; it is not another player payment. AccuracyLevel, AOS Damage Increase, Hit Chance Increase, slayers, and the other AOS properties do not add a premium in either GenericSell weapon branch. Do not confuse legacy DamageLevel with `Attributes.WeaponDamage`.

ServUO has an additional branch at `S/VendorInfo/GenericSell.cs:45-55`: when a vendor is supplied, vendor economy is enabled, and a matching buy entry has EconomyItem set, payment is 75% of that entry's current price, truncated and floored at 1. That branch returns before quality and legacy bonuses. `S/Mobiles/NPCs/BaseVendor.cs:33` enables the economy for AOS outside Siege. The table below specifies the ordinary GenericSell weapon branch, not every possible live economy quote.

| Item state | Dagger payment | Longsword payment |
|---|---:|---:|
| Regular, no legacy bonuses | 10 | 27 |
| Low, no legacy bonuses | 6 | 16 |
| Exceptional, no legacy bonuses | 12 | 33 |
| Regular, HCI 15 and AOS DI 50 | 10 | 27 |
| Exceptional, HCI 15 and AOS DI 50 | 12 | 33 |
| Regular, DamageLevel numeric value 1, DurabilityLevel 0 | 110 | 127 |
| Exceptional, both legacy levels numeric value 1 | 212 | 233 |

The weapon bases agree in both trees: `M/Mobiles/Vendors/SBInfo/SBBlacksmith.cs:173,218` and `SBWeaponSmith.cs:118,163`; `S/VendorInfo/SBBlacksmith.cs:193,238` and `SBWeaponSmith.cs:136,181`. Low and exceptional rounding truncates before legacy additions.

An important difference for books: ModernUO's ordinary Spellbook sell base is 9, while ServUO's is 25 (`M/Mobiles/Vendors/SBInfo/SBMage.cs:104`; `S/VendorInfo/SBMage.cs:116`). Both list the vendor's regular empty Spellbook stock at 18 (`:16` and `:34`, respectively). Neither GenericSell implementation adds a spellbook magic premium. Keep ModernUO as our baseline. Copying ServUO's 25 here would import a separate price discrepancy. A NecromancerSpellbook is offered at 115 in both mage buy lists, but neither mage sell list registers that exact type, so those lists establish no necromancer-book buyback price.

## Why exceptional weapons currently qualify

ServUO's AOS `OnCraft` adds 35 DI for exceptional quality, applies runic attributes when appropriate, then adds truncated Arms Lore / 20 outside Siege (`S/Items/Equipment/Weapons/BaseWeapon.cs:6346-6373`). At Arms Lore 0 and 100, an otherwise plain exceptional weapon has DI 35 and 40. Siege uses a divisor of 12.5 instead. ServUO's additive order is different from pinned ModernUO's.

Pinned ModernUO applies runic attributes first, then assigns exceptional DI 35 and adds Arms Lore / 20, capped at 50 (`M/Items/Weapons/BaseWeapon.cs:655-684`). Our `P/BaseWeapon-arms-lore.patch:3-17` changes the Arms Lore addition to `ClusterFArmsLore.ExceptionalDamageBonus`. That helper is `truncate(15 * clamp(ArmsLore, 0, 200) / 200)` (`C/ClusterFArmsLore.cs:35-53`). Our ordinary exceptional range is therefore 35 through 50, including DI 42 at Arms Lore 100. This applies to exceptional ranged weapons too, through BaseWeapon.

`C/ArtificersImbueGump.cs:211` gives DI a Full value of 50. Intensity is integer `value * 100 / Full` (`:134`). `C/Requisitions/RequisitionItems.cs:202-205,228-231` currently reads the full catalogue count and intensity without a crafting adjustment. Defaults in `C/Requisitions/RequisitionTable.cs:95-109` pay:

```text
price = clamp(base + 25 * property count + RoundToEven(0.5 * total intensity), 1, 500)
base: weapon 25, ranged 20, armor 40, shield 30, jewelry 13,
      spellbook 9, instrument 10, clothing 8, other 10
no properties: price 0 before applying the minimum of 1
```

The actual implementation uses the configured coefficients, `Math.Round(double)` and the configured cap (`C/Requisitions/RequisitionItems.cs:386-396`). The values above are built-in defaults, not verified live configuration.

| Our crafter's Arms Lore | Exceptional DI | Count | Intensity | Current dagger Appraiser quote | Stock dagger payment | Proposed Appraiser quote |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 35 | 1 | 70 | 85 | 12 | 0 |
| 100 | 42 | 1 | 84 | 92 | 12 | 0 |
| 200 | 50 | 1 | 100 | 100 | 12 | 0 |

A dagger requires three ingots (`M/Engines/Craft/DefBlacksmithy.cs:302`), and a blacksmith's base ingot stock price is 5 (`M/Mobiles/Vendors/SBInfo/SBBlacksmith.cs:16`). The base resource purchase is 15 gold. Current Appraiser payments exceed that by 70, 77 or 85 gold per successfully crafted exceptional dagger, before tools and failed crafts. The Appraiser has no purchase budget or daily sale limit in `C/Requisitions/Appraiser.cs:111-142`. A 500-gold per-item cap does not stop repeated low-cost sales.

## Proposed price rule in detail

1. Read a separate Appraiser property summary. Keep the Artificers' catalogue, item attributes and requisition matching values intact. An economy fix should not rewrite what an item does or change Imbuing's budget.
2. For an exceptional BaseWeapon, including ranged weapons, use `max(0, raw DI - 50)` as Appraiser DI. Count its DI row only if that adjusted value is positive, and calculate its intensity from the adjusted value using Full 50. For non-exceptional weapons, use the raw DI as today. All other qualifying magic properties keep their current catalogue values.
3. Count the adjusted rows and sum their integer intensities. If none remain, offer no sale and pay 0. Otherwise use the existing configured formula and cap, with no additional exceptional-quality multiplier and no legacy vendor-price additions. This is the custom magic floor; do not also add stock GenericSell payment.
4. Use that same summary for Price, Explain, quote text and the Sell button. Recheck eligibility and recompute at sale time. A protected item gets no actionable offer even if its raw properties would have monetary value.
5. Requisition gold continues to call the same Price function (`C/Requisitions/RequisitionSystem.cs:245-253`). Keep the existing raw property matching rules for found or crafted items. A quality-only item that fills an allowed request can still receive its Renown and standing, but its gold is 0. Changing which crafted items fill requests is a separate design change.

The fixed allowance of 50 is deliberately conservative. Subtracting only 35 leaves 7 or 15 ordinary crafting DI at Arms Lore 100 or 200, still creating a sale. Looking up the maker's current Arms Lore cannot recover skill at crafting time. Maker marks are optional and are not evidence that an item is ordinary or magical. Pinned has no DImodded flag, as already noted in `C/ArtificersImbueGump.cs:775-780`.

This rule can undervalue genuinely imbued DI on an exceptional weapon: raw DI 50 receives no DI premium; raw DI 70 receives a premium only for residual DI 20. It still buys an exceptional weapon with another genuine property. Normal-quality DI-only loot keeps its DI premium. This tradeoff avoids a new save field or guessed provenance. Record the policy with P452's implementation notes and have the overseer promote it to the existing custom-system fidelity entry. It is a recommendation, not proof that the remaining crafting economy is balanced.

### The same issue also exists for exceptional armor

This is an additional source-confirmed case of our Appraiser counting crafting bonuses, not a ServUO defect to port. Ordinary exceptional non-shield armor gets 15 distributed resist bonus points under SE, plus our capped Arms Lore addition of up to 10 (`M/Items/Armor/BaseArmor.cs:557-605,822`; `P/BaseArmor-arms-lore.patch:3-9`; `C/ClusterFArmsLore.cs:55-57`). These go directly into PhysicalBonus, FireBonus, ColdBonus, PoisonBonus and EnergyBonus. The catalogue prices those same fields (`C/ArtificersImbueGump.cs:382-400`).

For a complete ordinary-exceptional exclusion, recommend omitting those five resist-bonus rows from the Appraiser summary on exceptional non-shield armor. This is conservative too: real runic resist bonuses share the fields and would lose that premium, while other magic rows would still earn payment. Do not alter raw resistance values or board matching. Under ML, BaseShield skips those exceptional resist grants, so this exclusion should not discard genuine shield resists merely because the shield is exceptional.

If P452 is limited to the P422 dagger case, log this armor case explicitly as remaining work and avoid saying it closed every ordinary-crafting payout. A precise split between crafted and magical resist bonuses would need provenance that the reviewed fields do not supply.

## Blessed spellbooks

Both trees construct ordinary spellbooks as blessed (`M/Items/Skill Items/Magical/Spellbook.cs:116-125`; `S/Items/Equipment/Spellbooks/Spellbook.cs:117-126`). ModernUO's NecromancerSpellbook inherits that constructor (`M/Items/Skill Items/Magical/NecromancerSpellbook.cs:6-10`). Our two factory categories construct those ordinary types (`C/Requisitions/RequisitionItems.cs:74-75`). Both the Appraiser's Sell and RequisitionMatch currently reject all blessed items (`C/Requisitions/Appraiser.cs:125`; `C/Requisitions/RequisitionItems.cs:316`). Price itself does not apply that check, so a book can show a positive quote and still fail the sale.

Recommend a shared protection rule used by matching, quoting and selling. Exempt the exact ordinary types Spellbook and NecromancerSpellbook from the blanket LootType.Blessed refusal. Use exact types for this initial exception, so `item is Spellbook` does not silently admit every artifact or reward subclass. Additional schools and special books can be reviewed separately. Continue rejecting other blessed items. Keep explicit personal protection separate: a Nontransferable/QuestItem, an insured item or an item with BlessedFor set should not become eligible through the ordinary-book exception. These fields exist in `D:/UO/ModernUO-pinned/Projects/Server/Items/Item.cs:569,801-828`.

Blessed status, exceptional BookQuality, a maker mark, and the number of spells stored are worth zero properties and zero intensity. An empty or full ordinary book with no attributes, skill bonuses or slayer gets no Appraiser offer. A book with real magic keeps the current reading in `C/Requisitions/RequisitionItems.cs:207-252`: attributes count, each positive skill slot counts, and each occupied slayer slot counts. Each slayer contributes 100 intensity; each positive skill bonus contributes truncated `bonus * 100 / 15`. A stored spell is content, not a magic attribute.

Do not exempt all crafted books from magic pricing. Ordinary inscription can roll real magic based on the crafter's Magery (`M/Items/Skill Items/Magical/Spellbook.cs:154-208`), and `P/Spellbook-improvement-talisman.patch` can add a property. Those rolled attributes are intended magic, unlike the automatic exceptional weapon DI. The current default ordinary Spellbook recipe uses ten blank scrolls (`M/Engines/Craft/DefInscription.cs:443-445`). Enabling sales of magical crafted books is not a general profitability guarantee.

## Concrete expected prices

Every row uses defaults, normal quality unless specified, no other properties, and a movable, owned, unprotected item. DI means Damage Increase; HCI means Hit Chance Increase. N and I are the proposed Appraiser count and total intensity. These are source-derived calculations, not runtime test results.

| Item | N | I | Proposed gold |
|---|---:|---:|---:|
| Plain dagger | 0 | 0 | 0 |
| Exceptional dagger, DI 35, 42 or 50 only | 0 | 0 | 0 |
| Normal dagger, DI 35 only | 1 | 70 | 85 |
| Normal weapon, HCI 15 only | 1 | 33 | 66 |
| Exceptional dagger, DI 50 and HCI 15 | 1 | 33 | 66 |
| Exceptional bow, DI 50 and HCI 15 | 1 | 33 | 61 |
| Exceptional weapon, DI 70 only | 1 | 40 | 70 |
| Normal weapon, one slayer only | 1 | 100 | 100 |
| Normal weapon, HCI 45, DCI 45, DI 50, SSI 60, Luck 100 | 5 | 500 | 400 |
| Same weapon but exceptional quality | 4 | 400 | 325 |
| First five-property normal weapon, Luck raised to 300 | 5 | 700 | 500, exactly at the cap |
| First five-property normal weapon, Luck raised to 400 | 5 | 800 | 500, capped from 550 |
| Either ordinary book, blessed but no magic, empty or full | 0 | 0 | 0 |
| Either ordinary book, blessed, LMC 8 | 1 | 20 | 44 |
| Either ordinary book, blessed, SDI 6 | 1 | 50 | 59 |
| Either ordinary book, blessed, one +5 skill slot | 1 | 33 | 50 |
| Either ordinary book, blessed, one slayer | 1 | 100 | 84 |
| Either ordinary book, blessed, LMC 8, +15 skill, one slayer | 3 | 220 | 194 |
| Exceptional non-shield armor, only crafting resist bonuses | 0 | 0 | 0 under the armor recommendation |

SDI uses this shard's catalogue Full 12, not an assumed external cap (`C/ArtificersImbueGump.cs:234`). LMC uses Full 40 (`:224`). HCI uses Full 45 (`:215`). Preserve round-to-even: intensity 33 contributes 16 gold from 16.5, giving the weapon price 66, not 67. Do not round each property's gold separately. Integer property intensities are summed first, then the single monetary rounding is applied.

## Proposed P452 regression cases

These are acceptance cases to implement later, not tests added or run by P579. Every new P452 test must be seen failing against the old behavior, then passing after the fix, using the project's existing test gate.

1. **Actual ordinary crafting.** Craft iron daggers through the real craft path using a normal tool at Arms Lore 0, 100 and 200. Assert the resulting exceptional DI values 35, 42 and 50 before checking pricing. Do not substitute staff-assigned attributes for this economy regression. Control randomness or use bounded attempts to get exceptional output. Cover marked and unmarked output. Each item must remain in the backpack, give no Appraiser Sell button, sell for no gold, and remain undeleted after refusal. Repeat attempts cannot pay anything. Add an exceptional ranged case through the same BaseWeapon path.
2. **Crafting plus real magic.** Add HCI 15 to each real exceptional dagger. All should quote and pay 66, with one priced row and intensity 33; the free DI must not increase the count or premium. Compare a normal weapon with HCI 15, and a normal DI-only weapon. Check the DI 70 residual case and the five-property/cap rows above. Pricing must not mutate DI, HCI, quality or catalogue values.
3. **Shared payment and raw matching.** Use separate equivalent copies for sale and turn-in, since each successful exit consumes its item. An appropriate request for the exceptional HCI item should pay the same 66 gold as a sale, plus its configured Renown and standing. A request that accepts raw exceptional crafting bonuses should still match; its quality-only item pays zero gold while keeping the configured non-gold rewards. Verify that a consumed item cannot pay again.
4. **Both ordinary books through real exits.** For exact Spellbook and NecromancerSpellbook, leave their constructor blessing in place. Check no-magic empty/full books and the magic price rows above. Sell a magical copy and turn in another to the relevant Arcane or Keepers request. Verify the exact gold, item consumption, request removal, Renown and standing. A numeric quote alone does not cover P422's bug.
5. **Both Lead categories.** For each default Arcane spellbook property and the Keepers necrobook property in `C/Requisitions/RequisitionTable.cs:257-262,305`, create a request and exercise the real qualifying-kill/Lead delivery path with a guaranteed roll. Verify the delivered constructor-blessed book meets the request and turns in successfully. Also sell a separate generated copy. Keep the original weapon Lead integration coverage. Directly calling the factory alone does not prove delivery and turn-in agree.
6. **Blessing boundaries and quote consistency.** Refuse an otherwise magical blessed sword, blessed jewelry and a blessed special Spellbook subclass. Check the exact ordinary books with QuestItem/Nontransferable, Insured or BlessedFor protection separately. Refusals must preserve items and pay nothing, and the quote must not offer a sale that Sell refuses for that protection. Keep map, distance and backpack checks. Change an item's property or protection after quoting, then confirm the server rechecks and pays only its current valid price.
7. **Armor counterpart.** If the armor recommendation is included, actually craft ordinary-tool exceptional non-shield armor at Arms Lore 0 and 200. Verify its free distributed resist totals, 15 and 25, and zero Appraiser payment. Give it another genuine property and verify only that row earns a premium. Check an exceptional shield's genuine resist row is retained under ML. Keep raw armor matching and combat values intact. This test distinguishes a general crafting-bonus fix from a dagger-only fix.

Existing `T/RequisitionsVerification.cs:479` sets magic properties directly, including an unblessed weapon sale. Its Luck 300 assertion reaches exactly 500 before clamping, so it does not prove the cap actually reduces an excessive quote. Use the Luck 400 case to exercise that branch. Its book assertion checks a numeric quote and later a distance refusal, not a nearby book sale. Its Lead test at `:539` covers an HCI sword only. Update those expectations where the proposed summary changes them and add the real craft/book integrations above.

## Verification and limits

Verified source paths and arithmetic offline. No runtime shard test, build, client session, live configuration inspection or live vendor quote was run. Actual crafting output under the assembled server, live price modifiers, tool consumption, success rates, economic throughput and the proposed protection paths remain unverified at runtime. The test cases above are future work for P452. No claim is made that excluding exceptional bonuses alone balances every material, craftable item or special item constructor.

Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing to these work copies; exit 0. The tool still writes `tools/progress.json` during dry-run. Its initially clean contents were restored byte for byte, leaving only the requested notes. No code, tests or files under docs were changed. No Haven connection, deployment, commit, merge, push or branch switch was made.

The wrapper requests this report's filename with `design-`; the embedded prompt requests the shorter `cc-P579-requisitions-appraiser-numbers.md`. That shorter filename is a pointer to this report so either task reference can find it.

P579 DONE
