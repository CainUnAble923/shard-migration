# Achievements, Achievement Points, and loot boxes

Draft checked against project notes and source code on October 25, 2026. Availability and settings on the running shard have not been checked. Configurable numbers below are source defaults.

## Finding your achievements

Open **Achievement Records** with `[achievements`. The shard's custom TazUO client also has an **Achievements** button on your own paperdoll and top bar. Elara Voss, the League Registrar in New Haven, can open the records too.

Achievements belong to your account. Your characters share the earned list, Achievement Points, and Renown. Earning the same achievement on another character does not pay it again.

The window shows your AP and Renown at the top. Earned entries explain what you did and show their rewards. Unfinished entries show their requirements, including prerequisites and progress where a counter applies.

Use **All** to see every category available to you. Collection, League, and Mischief appear there without separate tabs. Categories have their own headings and icons.

| Category | What it covers |
|---|---|
| Combat | Creature kills and combat milestones. |
| Skills | Reaching skill milestones and developing several skills. |
| Exploration | Arriving in Britannia and visiting its facets. |
| Mining | Colored ore, ore discoveries, and mining work. |
| Crafting | Making items, exceptional work, and smelting. |
| Legacy | New Haven trainer quests and work in Old Haven. |
| Discovery | Survey reports and treasure map discoveries. |
| Collection | Collecting ore types and reaching bank-gold milestones. |
| League | Registration, League activities, and achievement milestones. |
| Mischief | Hidden achievements discovered through play. |

Hidden achievements stay out of the unfinished list until earned. Hidden entries also exist in other categories. Some hidden achievements now check their conditions more carefully. Their names and conditions are left for you to discover.

Older characters may have a **Retired** section. Those achievements are no longer awarded, but existing holders keep them and their rewards.

The **Quests** tab is a separate checklist for New Haven trainer quests. For League registration and guild work, see the [League guide](league.md).

## AP, Renown, and titles

**AP unlocks, Renown buys.** Each achievement lists its own AP and Renown reward. Some give no Renown.

| Account total | Purpose |
|---|---|
| Achievement Points, or AP | Your permanent achievement score. It opens shop tiers and free titles. Purchases do not spend it. |
| Renown | Your spendable League balance. Achievements, earned boxes, and requisition turn-ins can add to it. |
| Lifetime Renown | Qualifying Renown earned over time, used for League promotions. Spending in the shop leaves it unchanged. |

Open **Titles** from Achievement Records, the League shop, or the Registrar. Choose an unlocked title to show after your character's name, or choose **No League title** to clear it. Owned titles belong to the account; each character chooses what to display.

These titles unlock free when you reach the listed AP:

| AP | Title |
|---:|---|
| 100 | the Noted |
| 250 | the Accomplished |
| 500 | the Distinguished |
| 1,000 | the Renowned |
| 1,750 | the Illustrious |

An unlocked AP title stays owned. The shop also sells titles for Renown, with the AP requirements shown below.

## Earning loot boxes

A new achievement earned while you are online gives its box to an online character on your account. League promotions also award boxes to the promoted character. Repeating an already recorded source does not provide an endless supply of boxes.

Tutorial graduation gives an Explorer's box and records your first loop, which also awards a Loop box. The broader system of later loops, player levels, and skill resets is (planned).

Your character's first kill of each qualifying boss type awards a Boss box when you have looting rights or land the final blow. This reward now works during ordinary kills. Paragons do not qualify for boss boxes. Later kills of the same boss type on that character do not award another box. First-dungeon and floor-clear boxes are (planned).

Earned boxes have a **theme** and a **tier**. Their tooltip tells you the theme, tier, and what earned them. The ordinary achievement tier follows the AP paid by that achievement, rather than your account's total AP. Individual rewards can have exceptions.

| Tier | Achievement's AP reward | Non-resource box name and color | Base gold | Base Renown |
|---:|---:|---|---:|---:|
| 1 | Up to 10 | Common, gray | 250 | 0 |
| 2 | Above 10 through 25 | Uncommon, green | 750 | 25 |
| 3 | Above 25 through 50 | Rare, blue | 2,000 | 50 |
| 4 | Above 50 through 100 | Epic, purple | 5,000 | 100 |
| 5 | Above 100 through 250 | Legendary, orange | 12,000 | 200 |
| 6 | Above 250 | Celestial | 30,000 | 400 |

These currency amounts describe the ordinary earned-box roll. A League-themed earned box adds extra Renown. The shop's Bronze, Silver, and Gold boxes use their own rules below.

Resource themes use material names instead of rarity names. Miner's boxes follow a metal ladder, Woodsman's boxes a wood ladder, and Hunter's boxes a leather ladder. Artisan's boxes use the ladder for their craft. A material name on a box describes its tier; it does not promise that every item inside uses that material.

The theme supplies related rewards. For example, Miner's boxes give ore and gems, Explorer's boxes give maps, Scholar's boxes give reagents and a spell scroll, and Artisan's boxes give crafting supplies and a recipe or pattern book. Higher tiers also draw from pools of consumables, resources, magic gear, recipes, cosmetics, and rare rewards.

Contents are fixed when the box is awarded. Saving a box to open later will not improve its contents. Ordinary gear and supplies can be traded. Box cosmetic sashes and other items marked as account-bound stay with that account.

Some rewards still say **[Placeholder]**, including the League Shop Discount Token. Their promised functions are (planned); the placeholder is not a working discount or upgrade. Epic components exist, but their epic crafting recipes are (planned).

Loop scroll fragments also exist. Combining **5 fragments into a loop scroll** is (planned); the current action keeps the fragments and creates no scroll.

## Opening a box

Keep the box in your backpack and double-click it. You must be in either of these places:

| Place | Requirement |
|---|---|
| Guarded town area | You are inside the guarded region and its guards are enabled. |
| Player house | You are an owner, co-owner, or friend of that house. |

The box belongs to its earning or buying account. It cannot be traded, dropped on the ground, or stored in a house chest. Bags carried by your character are allowed.

Opening gives you the contents immediately and shows a reveal window. Items and gold go into your backpack, with your bank as the fallback when the pack cannot hold them. Renown goes into the account balance. The box then disappears.

With the matching player-package art, an eligible item can appear to fly out over your character as the box opens. An opening shows one such animation, chosen from the contents. Some item types have no flying animation.

## Fanfare and muting

Achievements and boxes come with the System's comments, UO sounds, and effects. Several celebrations close together merge into one show.

| Fanfare | Who sees it |
|---|---|
| Minor | You receive the effects, sound, and private overhead line. |
| Major | Nearby players see and hear the celebration. Ordinary box tiers 4 and higher use this level. |
| Capstone | A larger local celebration and a shard-wide announcement naming you. The graduation loop uses this level. |

Type `[FanfareMute` to toggle your own fanfare off or on. It applies to that character and suppresses the effects, overhead lines, and flying-loot animation. System chat messages still arrive, and shard-wide announcements still show.

A spoken announcer voice is (planned). The current System voice uses text with UO sounds.

## The League reward shop

Open **League Shop** from Achievement Records or from Elara Voss, the League Registrar in New Haven. League registration is not required to shop.

Locked rows show the AP you need. An available purchase opens a confirmation page. You need enough Renown and room in your backpack for the purchase. Buying leaves your AP, Lifetime Renown, and League rank unchanged.

| AP needed | Reward | Renown |
|---:|---|---:|
| 0 | Registered Adventurer title | 25 |
| 0 | League tabard | 50 |
| 0 | System's Bronze Loot Box | 40 |
| 100 | Hair restyling deed | 75 |
| 100 | Blessed rune marked to the New Haven Registrar | 60 |
| 250 | League banner | 150 |
| 250 | League cloak | 200 |
| 250 | System's Silver Loot Box | 150 |
| 500 | Trophy statuette showing your name and AP at purchase | 250 |
| 500 | League-hue pigment, one use | 300 |
| 500 | Veteran of the League title | 200 |
| 1,000 | System's Gold Loot Box | 400 |
| 1,750 | League regalia: robe, cloak, and sandals | 1,000 |
| 1,750 | The System's Favorite title | 500 |

The shop sells cosmetics, decor, titles, and conveniences. It does not sell combat properties, power scrolls, artifacts, or skill and stat increases. The tabard cannot be dyed.

### The shop's boxes

These boxes use the same opening locations and account binding as earned boxes. Their contents are drawn from eligible starter-shop cosmetics, decor, and conveniences, plus a bound League sash. They contain no gold, Renown, titles, or Hall decor. Duplicate draws are possible.

| Shop box | Draws | Eligible starter goods |
|---|---:|---|
| Bronze | 1 | Goods from rows requiring 0 AP. |
| Silver | 2 | Goods from rows requiring up to 250 AP. |
| Gold | 3 | Goods from rows requiring up to 1,000 AP. |

### House decor

The shop's **Hall** page sells display cases, dragon and gargoyle statues, wall trophies, and mounted heads. Each row has its own AP requirement and Renown price. These pieces are decorative, without skill or stat bonuses.

Hall pieces arrive as account-bound deeds. Place them in a house you own; wall trophies also need a wall. Chopping a placed piece returns its bound deed. Display-case shelves and inserts can be dyed separately with a plain dye tub. Hall deeds have stricter binding than the starter shop's ordinary tradeable decor.

## Sources

Note links are relative to the shard-migration repository. Detailed code file and line evidence is in the [P387 work notes](../cc-P387-guide-achievements-and-loot-boxes.md).

- [League guide](league.md) and [Society of Smiths guide](society-of-smiths.md): companion pages and draft format.
- [Feature queue](../../docs/feature-queue.md), F-13 and F-40 through F-42: shop decisions, earned boxes, fanfare, and planned epic crafting.
- [P55](../cc-P55-bug-batch-5.md), [P57](../cc-P57-batch-6.md), and [P61](../cc-P61-batch-7.md): earned descriptions, retired achievements, and progress presentation.
- [P79](../cc-P79-loot-boxes-fanfare.md) and [P82](../cc-P82-artificers-imbuing.md): earned boxes, themes, scaling, fanfare, and later reward changes.
- [P147](../cc-P147-achievements-button.md), [P165](../cc-P165-achievements-button-fix.md), and [P241](../cc-P241-achievement-category-icons.md): client access and category presentation.
- [P229](../cc-P229-league-reward-shop.md) and [P243](../cc-P243-league-hall-decor-rewards.md): shop goods, prices, titles, shop boxes, and Hall decor.
- [P231](../cc-P231-osi-joke-achievements.md), [P262](../cc-P262-accessory-slots.md), [P263](../cc-P263-noted-by-the-system-achievements.md), and [P361](../cc-P361-cont-fixup-noted-by-the-system-achievements.md): hidden-entry handling and the earlier boss-box defect. Their discovery details are omitted here.
- [P455](../cc-P455-death-hooks.md): first-boss boxes now award during ordinary kills.
- [P457](../cc-P457-noted-fixups-2.md): corrections to hidden achievement checks. Discovery details are omitted here.
- [P366](../cc-P366-cont-fixup-cont-loot-box-flying-loot.md) and [P371](../cc-P371-graduation-is-the-first-loop.md): flying loot and graduation rewards.
- [P376](../cc-P376-league-decisions.md) and Chase's October 23 answers in the [feature queue](../../docs/feature-queue.md), F-24: settled League decisions. Publish no AP ceiling or title count, list visible titles by name, and keep hidden titles secret.
- Current ShatteredLegacy source: `server/customizations/ClusterFAchievements.cs`, `ClusterFAccountData.cs`, `ClusterFLeagueRanks.cs`, `ClusterFGuildPromotion.cs`, `LeagueRegistrarGump.cs`, `LootBoxes/`, `LeagueShop/`, and `Tutorial/`, with their existing verification cases under `server/tests/`.

## Contradictions

Historical differences and unresolved limits remain on record below. P455 and Chase's October 23 decisions resolve the boss rewards, AP publication, and Renown spending items.

- **Boss rewards, resolved:** P263 reported that ordinary kills never awarded the first-boss boxes described by F-40 and P79. P455 corrected the award timing, so first-boss boxes now work.
- **Loops:** P79 records loop rewards as uncalled hooks and uses a fixed loop assumption. P371 records graduation as the first real loop and calls its reward. The wider later-loop system remains (planned).
- **AP totals and title counts, resolved:** Chase's October 23 rule supersedes the older catalog figures. This guide publishes no AP ceiling or title count and lists only visible titles by name. Hidden titles stay secret.
- **Renown spending, resolved:** Chase's October 23 decision confirms the delivered League shops. Older statements in F-13 and P75 that nothing spends Renown are history.
- **Box lifetime:** F-40 and P79 describe a box disappearing when emptied, with cleanup for leftovers. Current opening code hands over its contents, clears the list, and deletes the box in that opening action.
- **Gear strength:** F-40 promises box gear weaker than exceptional crafted gear of the same tier. P79 explicitly leaves that comparison unverified. This guide makes no strength guarantee.
- **Scroll fragments:** F-40 and the fragment tooltip say five make a loop scroll. P79 and the current combination action leave that function unbuilt.
