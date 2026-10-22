# Artificers' Order

Draft checked against project notes and source code on October 21, 2026. The running shard and its settings have not been checked. Numbers below are built-in defaults. Features still to come are marked (planned).

## What the Order is

The Artificers' Order is Britannia's guild of enchanters and item-shapers. Its skill is Imbuing: adding magical properties to weapons, armor, shields, jewelry, and clothing. You can also recover magic from unwanted equipment and craft property essences for other enchanters.

Thornwick Vesper is the guildmaster. Open the Guild Directory with `[guild`, find the Artificers' Order, and choose **Show me the way**. In New Haven, the chapter is in the Magery School. There is also a post in Royal City, Ter Mur.

## Joining and your first task

Joining is free. Visit the guildmaster, open the guild hall page through **Talk**, and join. You can belong to other guilds too. This membership is separate from the older NPC guild system that charges gold to join.

Joining gives your character a blessed **Artificers' Essence Satchel** and **Artificers' Toolkit**. Keep the toolkit in your backpack and double-click it to open the Imbuing Table while traveling. The satchel opens a Mastery Dashboard when double-clicked.

On the guild hall page, choose **Guild services** to reach the Member Dashboard for formula books and enchanting work orders.

The separate **Apprentice task** asks for either:

| Option | Requirement |
|---|---|
| Demonstrate the skill | At least 20.0 base Imbuing |
| Offer tribute | 3 Diamonds, taken from your backpack or bank |

If you meet the skill requirement, the task does not take diamonds. Completing it pays **25 standing and 10 Essence Shards**. It also opens access to the Apprentice Formulary, even before you earn 1,000 standing. The guild's rank displays differ here; see Contradictions below.

Membership, standing, currency, and active work orders belong to each character. Learned formulae and property mastery are shared by the account. Learned formulae are intended to stay through loops.

## Ranks and what they open

Standing earned through successful imbuing and guild work orders raises your rank. The standing ladder is:

| Rank | Standing | Formula books available to buy |
|---|---|---|
| Apprentice | 0 | The free Basic properties are already known; no book purchase needed for them. |
| Journeyman | 1,000 | Apprentice Formulary |
| Artificer | 5,000 | Journeyman Formulary |
| Master Artificer | 15,000 | Artificer's Formulary |
| Arcane Artisan | 40,000 | Arcane Formulary, plus the Master Formulary when the trial requirement is met or waived |

The Order's top-rank trial is (planned). Its requirement is waived by default until trials are built. It is separate from the League's story trials.

Rank opens the books for sale. **Reading a book teaches your whole account.** Buy them from **Member Dashboard > Formula Books** at the guildmaster. Books cost Essence Shards only, with no gold charge. Reading consumes the book; unread books can be traded.

| Book | Essence Shards | What it teaches |
|---|---|---|
| Apprentice Formulary | 250 | Basic leeches, Hit Lower Attack and Defense, elemental damage conversion, Balanced, Velocity, Spell Channeling, Mage Armor, and skill bonuses; Refined versions of free properties. |
| Journeyman Formulary | 500 | Basic hit spells, Damage Increase, Mage Weapon, and Reflect Physical Damage; Refined versions of the Apprentice book's new properties; Full versions of free properties. |
| Artificer's Formulary | 1,000 | Basic area hits, single slayers, Hit Chance, Defense Chance, Spell Damage Increase, Lower Mana Cost, and the craft properties below; Refined versions of the preceding book's new properties and Full versions of the Apprentice book's. |
| Arcane Formulary | 2,000 | Basic Faster Casting, Faster Cast Recovery, Swing Speed Increase, and super slayers; Refined versions of the Artificer's book's new properties and Full versions of the Journeyman book's. |
| Master Formulary | 4,000 | Refined versions of the Arcane book's new properties, Full versions of the Artificer's book's, and a sixth property slot under the default rules. Requires the trial or its waiver. |

On/off properties, such as slayers and Night Sight, do not grow stronger through intensity tiers. Casting Focus appears in the design ladder but is not an available imbue property.

## Imbuing: knowledge, intensity, and materials

Every account starts with Basic knowledge of the five resist bonuses, stat bonuses, hit point, stamina and mana increases, their regeneration properties, Night Sight, Luck, Lower Requirements, Durability, Self Repair, Lower Reagent Cost, and Enhance Potions. Free knowledge does not mean a free imbue: materials, Shards, and gold still apply.

The rework gates what you can imbue by the **property you know and its learned intensity tier**. It allows work on already enchanted items. Increasing standing alone does not teach a property or raise its intensity.

| Tier | Strength |
|---|---|
| Basic | About one-third of the property's Full value, rounded |
| Refined | About two-thirds of Full, rounded |
| Full | The property's normal maximum in the shard's Imbuing Table |
| Overcharged | A higher maximum where the property supports it; its normal unlock sources are (planned) |

The menu shows properties your account knows and hints about further learning. Choose an item, property, and tier, then review the cost and success chance before confirming. A higher tier still requires enough Imbuing skill for a successful attempt.

An item normally has a limit of **5 properties counted by the table**. Reading the Master Formulary raises that to **6** under the default rules. Only one custom property can be placed on an item.

Ordinary properties require a matching **PropertyEssence** until you master that individual property. A successful imbue consumes one essence and advances its mastery count. The satchel's dashboard shows your progress. After mastery, you still pay Shards and gold, but no longer need that essence. You can also craft that property's essences to trade.

Knowing a formula and mastering an essence are separate. An essence does not teach a locked property or tier. Custom properties use their own ingredients instead of property essences.

Essences and custom ingredients can be drawn from your backpack or bank, including eligible containers. Backpack resources are used first. The confirmation page shows the required costs. A failed imbue consumes no resources, but can damage a weapon's or armor's current durability.

Self Repair is known at Basic without a rank requirement. It retains a price floor above other properties, so check its confirmation cost carefully.

### Skill bonuses and craft properties

Jewelry can receive the listed combat and other skill bonuses, with one skill per group. Crafting and gathering bonuses go on half aprons and full aprons under the default rules, with a crafting group and a gathering group. Their Basic, Refined, and Full bonuses are **+5, +10, and +15**. Worn bonuses do not count as trained base skill.

The Artificer's Formulary introduces these custom properties at Basic:

| Property | What it does |
|---|---|
| Bountiful | Adds yield to mining and lumber gathering. |
| Mastercraft | Improves the chance of exceptional crafting. |
| Prospector | Gives a chance at rare finds while mining or lumber gathering. |
| Butcher's Eye | Improves monster-part yields from kills and carving, with a chance at a rare part. |

Tool belts and broader guild gear for crafting skill bonuses are (planned).

### Where you can imbue

The toolkit and guildmaster's table allow known tiers up to **Full** away from a forge under the defaults. Overcharged work requires the learned tier and a real soul forge within **2 tiles**. A forge provides a success bonus; standing near one does not teach its properties.

An owner's nearby mule with an Imbued Barding Socket II supports up to Refined, while III supports up to Full with a forge bonus. Neither permits Overcharged. The default toolkit already reaches Full, so socket II does not increase that limit.

The advanced route through quests, commissions, loot boxes, and bosses for Overcharged tiers and rare formulae is (planned). The rank books do not teach Overcharged. Reinforce is also (planned); it has no available action in the current table.

## Unravel, extraction, and the satchel

Unravel and extraction are available without guild membership or learned formulae at the guildmaster's table. Members can use their toolkit for access while traveling.

| Action | Result |
|---|---|
| Full Disenchant | Permanently destroys the magic item. Pays Essence Shards and gives each active property a 25% chance to yield its PropertyEssence. |
| Extract a Property | Removes one property and gives its matching essence plus Shards. The item survives. Weapons and armor lose about 20% of maximum durability, rounded to whole points. |
| Unravel Container | After confirmation, fully disenchants eligible items directly inside a bag in your backpack. Nested bags and their contents stay untouched. |

Full Disenchant refuses plain, blessed, newbied, equipped, quest, and faction reward items. Unravel Container also skips insured items. Its confirmation shows how many items will be destroyed and how many will stay. The chosen bag must be inside your backpack and unlocked.

Keep the purple Artificers' Essence Satchel in your backpack, even inside another bag. Extracted and disenchanted property essences go into it automatically. Looted or picked-up property essences, magical residue, enchanted essence, and relic fragments also route into it. A full satchel falls back to your backpack with a message; if the backpack cannot take a newly produced essence, check at your feet.

Bank moves, trades, and rearranging your backpack do not trigger this collection. Crafted essences arrive in the backpack. Double-click the satchel to check stored essence counts and mastery progress.

**Essence Shards are a currency balance, not items in the satchel.** Magical residue, enchanted essence, and relic fragments are separate physical materials. The Order's Unravel pays Shards and property essences; it does not use the standard residue-to-relic-fragment yield system.

## Work and rewards

Open **Member Dashboard > Guild Work Orders** for enchanting commissions. Orders become available when you have mastered every required property. Check that you also know the tiers needed to meet the requested values before accepting.

You can hold **one Artificer commission at a time**. Regular orders supply a specific blank item; enchant it and return that same item. Combined Smith and Artificer orders require Society of Smiths membership and ask you to craft a weapon in the specified metal, then enchant it.

Turning in a completed item consumes it and pays the displayed gold, Essence Shards, and Artificers' Standing. Combined orders also pay Smithing Seals and Smiths' standing. Eligible turn-in items can be found in the backpack or bank. Abandoning an order pays nothing and removes its supplied item if found.

| Reward or resource | How it fits |
|---|---|
| Essence Shards | Earned from disenchanting, extraction, work orders, and the Apprentice task. Spent on imbuing, essence crafting, formula books, and applicable mule upgrades. |
| Artificers' Standing | Earned from successful imbuing, work orders, the Apprentice task, and the Order's requisitions. Opens rank services. |
| Property essences | Extracted, sometimes recovered during full disenchanting, or crafted after mastery. Tradeable materials for imbuing. |
| Satchel and toolkit | Blessed tools issued on joining. |

The guild hall's **Requisitions** page provides another use for magic equipment. A matching turn-in consumes the item and pays Renown, Artificers' Standing, and gold. This is separate from the enchanting work orders and does not pay Essence Shards.

The Member Dashboard also opens the **Civic Mule Exchange** for upgrades to an existing mule. A first Compact Mule comes through the League Registrar's errand.

## Where its hall is

| Location | What is there |
|---|---|
| New Haven Magery School, Trammel, 3483, 2501 | The local chapter's guildmaster location. Use the Guild Directory's arrow to find the NPC. |
| Royal City, Ter Mur, 797, 3431 | The existing guildmaster post on the plaza west of the jeweler's shop. |
| Royal City headquarters (planned) | A full hall, top-rank trial, and travel-network stop. The New Haven chapter stays. The building choice remains open in the survey. |

## Sources

Project-note links are relative to this draft. Code paths below are in the Shattered Legacy repository; detailed file and line evidence is in [the P383 research notes](../cc-P383-guild-guide-artificers-order.md).

- [League guide](league.md): the draft's style model.
- [Feature queue](../../docs/feature-queue.md), F-9, F-33, F-37, F-43, F-47, F-49, and F-50: joining, guild skills, advanced progression, requisitions, halls, and satchel decisions.
- [Imbuing rework design](../../docs/artificers-imbuing-design.md) and [P82 implementation notes](../cc-P82-artificers-imbuing.md): property knowledge, formula books, intensity tiers, and outstanding features.
- [P15 starter path](../cc-P15-guild-starter-path.md), [P18 character guild data](../cc-P18-reset-stone-young-craftx.md), and [P27 essence access](../cc-P27-defect-batch-1.md): free joining, the separate Apprentice task, character membership, and bank materials.
- [P137 satchel collection](../cc-P137-usable-ankhs-and-playtest-fixes.md), [P173 slayers](../cc-P173-imbue-all-slayers.md), [P176 Unravel Container](../cc-P176-cont-artificers-unravel-container.md), and [P236 satchel icons](../cc-P236-satchel-icons-ship.md): later built behavior.
- [P150 requisitions](../cc-P150-requisitions-and-leads.md), [P151 hall survey](../cc-P151-guild-halls-survey.md), and [P265 hall decorations](../cc-P265-guild-hall-decor-packs.md): requests, existing posts, and unplaced hall plans.
- Code: `design/guilds/artificers_order.md`; `server/customizations/ClusterFGuildSystem.cs`, `ClusterFGuildStarterPath.cs`, `ClusterFGuildPromotion.cs`, `ArtificersGuildmasterGump.cs`, `ArtificersImbueGump.cs`, `ArtificerWorkOrderSystem.cs`, `ArtificersSatchel.cs`, `ArtificersToolkit.cs`, `PropertyEssence.cs`, and `Imbuing/`.
- Existing verification sources: `server/tests/Misc/ImbuingReworkVerification.cs`, `ImbueSelfRepairGateVerification.cs`, `ImbueEssenceSourcesVerification.cs`, `ImbueExtractDurabilityVerification.cs`, `ImbueAllSlayersVerification.cs`, `UnravelSatchelVerification.cs`, `UnravelContainerVerification.cs`, `GuildStarterPathVerification.cs`, and `GuildRankIndexVerification.cs`. These were read, not rerun for this draft.

## Contradictions

- **Joining and rewards:** the original guild design and parts of the guildmaster's text require Imbuing or diamonds to join and describe standing and Shards as joining rewards. F-9, P15, and current joining code make membership free and pay those rewards for the separate Apprentice task.
- **Apprentice and Journeyman:** the standing-only display calls the first rank Apprentice and requires 1,000 standing for Journeyman. The shared guild system treats completion of the Apprentice task as the second rank for the directory and formula shop, even with only the task's 25 standing. The guildmaster dashboard still uses standing alone.
- **Caps and Self Repair:** the original design and older P20, P42, and P58 notes describe standing-based intensity caps, increasing property slots, and a Master Artificer gate on Self Repair. P82 and current apply logic use learned tiers and the Master Formulary instead. Some guildmaster and welcome text still describes the former rules.
- **Book ladder:** the Imbuing design assigns separate rank indexes to the Arcane and Master books. The Order's standing ladder skips the index between Master Artificer and its top rank, so both books become available at Arcane Artisan, subject to the Master's trial check.
- **Trial:** the design and formula shop require a passed trial for the Master Formulary. The promotion system waives unbuilt trials by default. A completed Artificers' trial has not been established by these sources.
- **Reinforce and advanced formulae:** the rework design calls Reinforce free and names advanced unlock sources and Casting Focus. P82 reports Reinforce absent, and current code has no Reinforce action or Casting Focus imbue row. Advanced grant support exists, but normal reward sources for those unlocks remain unbuilt in the checked code.
- **Unravel materials:** F-50 groups Essence Shards with physical satchel contents and describes the standard Unravel ingredients. P137 and current code treat Shards as currency; this Unravel produces property essences and Shards, while the satchel also accepts separately acquired residue, enchanted essence, and relic fragments.
- **Work-order tiers and examples:** the original design assigns orders to standing tiers and gives armor and shield examples for combined work. Current availability checks mastery and Smith membership, and the combined-order definitions request weapons. Formula knowledge is not part of the order-availability check.
- **Mule forge:** F-33 assigns Unravel to socket II and Imbue to III. The later Imbuing design gives II Refined imbuing and III Full. Current defaults also permit Full through the toolkit away from a mule, which P82 records as an unresolved overlap.
- **Hall location:** the original design lists different Royal City and New Haven coordinates from the current guild location table. F-49 calls Royal City already posted; P151 describes an outdoor NPC post and a proposed hall. P265 builds decoration templates while explicitly placing no hall.
