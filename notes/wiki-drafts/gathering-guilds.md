# Gathering guilds: Foresters, Miners, and Outriders

Draft checked against project notes, source code, and existing test cases on October 21, 2026. Features still to come are marked (planned). Availability and settings on the running shard have not been checked. Configurable numbers below are source defaults.

## Where to begin

Gathering supplies Britannia's workshops and gives you work outside town. These guilds provide tools, resource bags, and contracts.

Open the Guild Directory with `[guild`, choose a guild, and use **Show me the way**. At its guildmaster, join through the guild page. Joining is free and requires no skill or tribute. Open **Services** for the guild's own dashboard.

| Guild | New Haven chapter, Trammel | Currency |
|---|---|---|
| Foresters' Union | Cedric Rowanwood at Carpenters of New Haven | Timber Tokens |
| Miners' Compact | Garrett Ashveil, the Miners' Compact Liaison, at the south mountain mine camp | Mining Vouchers |
| Rangers' League, also called the Outriders | Mira Ashfen at the stables | Trail Marks |

You can join all three. Membership, standing, currency, and active contracts belong to your character. Ore and timber discovery records belong to your account. Losing a logbook does not erase its discoveries, and gathering records finds even without the book in your pack.

The separate **Apprentice task** pays 25 standing and 10 of that guild's currency once. It is available after joining.

| Guild | Complete the task with either option |
|---|---|
| Foresters | 50.0 base Lumberjacking, or 20 regular Boards. |
| Miners | 50.0 base Mining, or 20 Iron Ore. |
| Outriders | 30.0 base Archery, or 25 Arrows. |

Tribute comes from your backpack or bank and is consumed only if you use the item option. Skill bonuses do not meet these base-skill requirements.

## Standing and rank

Standing measures progress. Tokens, Vouchers, and Marks are balances you can spend without spending standing.

| Standing | Foresters | Miners | Outriders |
|---:|---|---|---|
| 0 | Woodcutter | Initiate | Wanderer |
| 1,000 | Sawyer | Apprentice | Scout |
| 5,000 | Forester | Journeyman | Outrider |
| 15,000 | Arborist | Surveyor | Trailblazer |
| 40,000 | Grove Warden | Master Delver | Beastmaster |
| 80,000 | Master of the Wood | Deepwarden | Warden of the Wild |
| 150,000 | Legendary Forester | Legendary Prospector | Legendary Outrider |

Completing the Apprentice task can open the second rank before its standing threshold. Foresters also need crafting skill for promotion: the better of base Carpentry or Bowcraft/Fletching must reach 30, 50, 70, 90, and 100 for the successive promotion grades. Grove Warden and Master of the Wood share the 90-skill grade. Earned promotions are retained if skill later falls.

The Foresters' top-rank guild trial is (planned), with its requirement waived by default until built. Some dashboards show standing alone and can disagree with the guild page's task or crafting requirements. See Contradictions.

## Foresters: trees and the Forester's Logbook

Joining supplies trade tools, a blessed **Forester's Logbook**, and a blessed **Foresters' Lumber Satchel**. Carry the satchel in your backpack to collect newly chopped logs automatically. It holds logs and boards and reduces their carried weight by **75 percent**. If it cannot take a harvest, the normal backpack or ground placement applies.

Use an axe or hatchet on a tree to gather logs. To make boards, double-click the axe and target a log stack in your backpack. Each log becomes one board of its wood type when you meet the cutting requirement. Regular wood is the starting material. Colored woods need these base Lumberjacking levels:

| Wood | Lumberjacking |
|---|---:|
| Oak | 65.0 |
| Ash | 80.0 |
| Yew | 95.0 |
| Heartwood, Bloodwood, Frostwood | 100.0 |

The extended woods below currently all require **100.0 base Lumberjacking to harvest**. Their crafting requirements are separate.

| Extended wood | Carpentry or Bowcraft/Fletching to work it |
|---|---:|
| Ironwood | 100.0 |
| Ghostwood | 115.0 |
| Emberbark | 130.0 |
| Frostbark | 140.0 |
| Shadowbark | 155.0 |
| Runewood | 170.0 |
| Voidwood | 185.0 |
| Starwood | 200.0 |

Rootwood is a separate starter wood from Rootdeep Burrows, harvested and worked at 45.0. It is outside the extended ladder.

Groves keep their wood after regrowth and server restarts. A rare grove can still yield ordinary logs. Your logbook records the area where you stood, so a grove entry points to a nearby find rather than promising that every tree there has that wood.

Double-click the logbook in your backpack to see recorded timber types, dates, totals, and grove locations. Colored stock woods and Rootwood need no report. Extended woods first appear as **Pending Report**.

Until you report an extended timber type, its harvest becomes regular logs. Open **Discovery Report**, review the rewards, and submit. You can do this from the book or through Cedric's **Forest Discoveries** page. The report awards Foresters' standing and Timber Tokens and lets future harvests yield that timber. The reward is once per extended wood type across the account, not once per grove.

Rare woods give crafted bows, staves, clubs, and wooden shields their own material bonuses. Exceptional pieces receive extra bonuses. Rootwood has no such bonuses. Learning a recipe and meeting its crafting requirements remain separate from discovering its material.

Open **Timber Contracts** for gathering work. Foresters also offer **Bulk Order Info** for Carpentry and Fletching deeds to members with skill in the craft. If you qualify for both, the guildmaster asks which craft you want. These crafting deeds are separate from timber contracts.

Cedric can replace a missing logbook or starting lumber satchel for **5 Timber Tokens each**.

## Miners: ore and the Prospector's Logbook

Joining supplies mining tools, a blessed **Compact Ore Satchel**, a blessed **Prospector's Logbook**, and a blessed **Compact Dispatch Ledger**. Request your first **Jacob's Pickaxe** through **Starter items**. That first claim is free and shares its reward record with **The Delucian's Lost Mine** training quest.

The guild starter route deliberately leaves out the training quest's 15-minute skill-gain acceleration. Claiming the reward through either route uses the same first claim.

Use a pickaxe or shovel on a suitable mountain or cave tile. The stock colored-ore ladder is Dull Copper at 65.0 Mining, Shadow Iron at 70.0, Copper at 75.0, Bronze at 80.0, Gold at 85.0, Agapite at 90.0, Verite at 95.0, and Valorite at 99.0. Iron is the starting ore.

| Extended metal | Base Mining to harvest; Mining threshold to smelt |
|---|---:|
| Platinum | 112.5 |
| Toxic | 125.0 |
| Blaze | 137.5 |
| Frost | 150.0 |
| Obsidian | 162.5 |
| Mythril | 175.0 |
| Adamantium | 187.5 |
| Celestial | 200.0 |

Dawnstone is a separate Rootdeep Burrows starter metal with a 45.0 harvest requirement. It is outside the post-Valorite ladder. Smelting has a skill roll, so reaching a metal's threshold does not guarantee success.

Ore deposits keep their material after regrowth and restarts, though a dig can yield fallback Iron Ore. Colored ore and Dawnstone are recorded automatically. Iron is not recorded as a colored-ore discovery.

Double-click the logbook in your backpack to inspect ore types, recorded veins, locations, and mined totals. **Blocks mined** counts distinct ore blocks you have worked. This count is separate from the book's vein entries.

Open **Field Report** to submit unreported veins remotely, or visit **Velara Thorne, the Survey Archivist**, at the mine camp. Each newly recorded vein pays Compact standing, Mining Vouchers, and gold deposited in your bank.

Platinum through Celestial need their first report before you can keep harvesting that ore. Until then, the discovery is recorded but its ore becomes Iron Ore. Reporting also satisfies discovery requirements on the contracts that ask for that ore type. You must still meet their other requirements.

## The Miners' Compact Liaison

Garrett's member dashboard offers **Work Orders**, **Restoration (Jacob's Pickaxe)**, pickaxe upgrades, **Upgrade Ore Satchel**, **Replace Starting Kit**, **Climbing Boots**, and the **Civic Mule Exchange**.

Keep the ore satchel in your backpack for automatic ore collection. It accepts ore, ingots, and plain Granite. Higher tiers reduce more weight and gain bulk smelting.

| Satchel | Weight reduction | Standing needed to upgrade to it | Smelts ore |
|---|---:|---:|---|
| Compact Ore Satchel | 50 percent | Issued on joining | No |
| Reinforced Ore Satchel | 55 percent | 1,000 | Yes |
| Surveyor's Ore Satchel | 60 percent | 15,000 | Yes |
| Deepdelver's Ore Satchel | 65 percent | 40,000 | Yes |
| Master Expedition Satchel | 70 percent | 80,000 | Yes |

Each upgrade takes the previous satchel plus Vouchers, ingots, and gold. The menu shows the full price. Materials and gold can come from your backpack and bank. Contents transfer into the new bag. The Liaison can recover previously unlocked higher tiers.

From Reinforced onward, choose **Smelt Ore** from the satchel's context menu while within 2 tiles of a forge. Each pile uses the forge's usual Mining check, output ratio, and loss on failure. Ingots return to the satchel, with normal overflow handling. Upgrading keeps this ability.

Jacob's Pickaxe progresses through Reinforced, Prospector, Deepdelver, and Worldbreaker versions. Upgrades require the earlier tool, standing, Mining, and payment. An exhausted pickaxe remains as a spent tool. The Liaison's Restoration page restores a tier already unlocked on your account; check its displayed requirements and cost.

The Liaison also sells blessed, account-bound climbing boots for reaching mountain deposits. Their successive requirements include Mining **120, 150, and 180**, **100, 300, and 600 distinct mined blocks**, and Surveyor, Master Delver, and Deepwarden standing. Wear the boots and double-click them to hop. Hops cost stamina. Pets stay below, and combat and taming are restricted while you are on a climbed tile.

## Outriders: animals, Herding, and the crook

The Outriders are the **Rangers' League** in the directory. Their skills include Archery, Tracking, Animal Taming, Animal Lore, Herding, Veterinary, and Camping.

Joining gives trade tools, a blessed **Outrider's Crook**, and a blessed **Hunter's Satchel**. Carry the satchel for leather, hides, bones, wool, feathers, and raw meat. It reduces content weight by **30 percent**, converts known hides to matching leather, and collects eligible carved resources nearby.

**Herding uses an ordinary Shepherd's Crook.** Double-click it, target a herdable wild animal, then choose where it should move. Success uses Herding against the creature's difficulty. Already controlled animals are refused. Herding moves an animal without making it your pet.

The **Outrider's Crook** opens a different menu. Double-click it in your backpack. The starting crook gives **+5 Animal Taming and +5 Peacemaking** while carried and offers these actions:

| Action | What happens |
|---|---|
| Deliver Pet for Contract | Target your own following pet within 2 tiles, matching an active taming contract. The guild takes the animal permanently and credits the contract. |
| Shrink Pet into Figurine | Store your own bonded, following pet in a figurine. Double-click the figurine in your backpack to return the pet when you have enough follower slots. |
| Instant Bond | Bond a tameable pet you control. The starting crook has a 48-hour cooldown. |

Accept the taming contract before delivering animals. Once all requested animals are delivered, open **Field Contracts** to collect payment. Delivery gives the animal to the guild; shrinking keeps it for you.

Outriders' rank also improves your controlled pet's chance to gain skills. Your Animal Taming and Animal Lore above 100 contribute too. Animal Lore's pet window shows **Learns** with the current multiplier. This increases the chance of a gain, not its size.

## Taking contracts

Foresters' **Timber Contracts**, the Compact's **Work Orders**, and Outriders' **Field Contracts** use the same ledger layout. The Dispatch Ledger opens Compact orders remotely from your backpack.

Read the requirements and rewards, accept an order, then use **Active** to turn it in. You can hold **3 active contracts per guild**, with one active copy of a particular contract. Material turn-ins take the whole required amount from your backpack and bank. Animal contracts use the crook's delivery progress.

Current contracts are fixed requests. Miners request ore, ingots, stone, or gems; Foresters request boards; Outriders offer animal deliveries and other field supplies. Completed orders pay the displayed standing, guild currency, and gold. Gathering and taming contract turn-ins currently give no skill checks.

Rolled gathering contracts, Rush jobs, Surveys, mule Hauls, Rare finds, and gathering-contract skill checks are (planned). A separate redesign of the wood harvesting ladder and its training range is (planned). The crafting table above does not describe that future harvesting ladder.

The League's **Requisitions** provide another use for matching magic items and pay standing, Renown, and gold. They are separate from these resource contracts. See the [League guide](league.md).

The League also offers a **Combined Logbook** for the ore and timber records and a **League Field Satchel** that holds guild satchels while preserving each one's filter and weight rules. Their purchases have separate League rank and payment requirements.

## Main halls (planned)

The decided headquarters towns are **Yew for the Foresters, Minoc for the Compact, and Skara Brae for the Rangers' League**. New Haven remains each guild's local chapter. The main halls and their full facilities are (planned); the cited hall survey placed nothing.

## Sources

Note links are relative to the shard-migration repository. Code paths name files in ShatteredLegacy. Detailed file and line evidence and verification limits are in the [P385 work notes](../cc-P385-guide-gathering-guilds.md).

- [League guide](league.md) and [Society of Smiths guide](society-of-smiths.md): format and related player systems.
- [Feature queue](../../docs/feature-queue.md), F-9, F-11, F-16, F-20, F-28, F-36, F-38, F-43, F-47, and F-49: decisions and planned work.
- [P13](../cc-P13-grove-tracking.md), [P14](../cc-P14-newhaven-guild-mapping.md), [P15](../cc-P15-guild-starter-path.md), [P16](../cc-P16-mine-camp-tents.md), and [P18](../cc-P18-reset-stone-young-craftx.md): discoveries, starter items, locations, and character guild records.
- [P22](../cc-P22-small-features-1.md), [P36](../cc-P36-dungeon-build-1.md), [P37](../cc-P37-upgrade-prep.md), [P38](../cc-P38-engine-upgrade.md), [P55](../cc-P55-bug-batch-5.md), [P56](../cc-P56-smith-economy-and-labels.md), [P57](../cc-P57-batch-6.md), and [P67](../cc-P67-craft-ceilings.md): starter resources, permanent deposits, satchels, smelting, and material ladders.
- [P78](../cc-P78-recipe-gating.md), [P123](../cc-P123-port-bulk-orders-crafts.md), [P150](../cc-P150-requisitions-and-leads.md), [P151](../cc-P151-guild-halls-survey.md), and [P172](../cc-P172-pet-gain-speed.md): crafting promotion, deeds, requisitions, hall plans, and pet gains.
- [P227](../cc-P227-extended-wood-bonuses.md), [P235](../cc-P235-work-order-numbers-pass.md), [P238](../cc-P238-climbing-boots.md), [P280](../cc-P280-league-register-build.md), and [P283](../cc-P283-skill-gain-paths-research.md): wood bonuses, contract research, climbing, consolidation items, and training limits.
- Current guild code: `server/customizations/ClusterFGuildSystem.cs`, `ClusterFGuildStarterPath.cs`, `ClusterFGuildPromotion.cs`, the three guildmasters and their menus, `ClusterFWorkOrderSystem.cs`, and `GuildContractLedgerGump.cs`.
- Current gathering code: `ClusterFMiningExtension.cs`, `ClusterFLumberjackingExtension.cs`, `ClusterFMetalTiers.cs`, `ClusterFWoodTiers.cs`, `ClusterFWoodBonuses.cs`, `CompactOreSatchelRoutingHook.cs`, both logbooks and their menus, `SurveyArchivistGump.cs`, and the ore and lumber satchel classes under `server/customizations/`.
- Current animal and support code: `OutridersCrook.cs`, `ShrunkPet.cs`, `HuntersSatchel.cs`, `ClusterFHuntersSatchelHooks.cs`, `ClusterFPetGainSpeed.cs`, `ClimbingBoots.cs`, `ClusterFClimbing.cs`, `LeagueRegister/LeagueConsolidation.cs`, and pinned ModernUO's `Items/Weapons/Staves/ShepherdsCrook.cs`.
- Existing verification cases under `server/tests/Engines/Harvest/`, `Items/`, `Misc/`, `Services/BulkOrders/`, and `Skills/`, inspected as source for this draft.

## Contradictions

These differences remain on record without deciding between the sources.

- **Joining and rewards:** F-9's early description and P14 use account-wide guild membership. Current membership and balances are per character. Some guild help still presents the Apprentice task as a joining requirement and its payment as a joining reward; the guild page joins freely and pays the separate task.
- **Rank displays:** guild dashboards use standing alone. The guild page also recognizes the Apprentice task, and Foresters' promotion checks Carpentry or Fletching. The displayed ranks can differ.
- **Wood tiers:** F-28 and P67 describe the crafting ladder to 200. Current harvest code keeps all extended woods at 100 Lumberjacking, with training ranges ending by 148. P235 and P283 propose changes to harvesting, with different upper-window specifications.
- **Regular wood:** the gathering record tracks regular logs, but the Forester's Logbook's visible timber list omits them. Its empty-book help also differs from that tracking behavior.
- **Satchel descriptions and upgrades:** lumber-satchel comments describe smaller capacities and 50/55/60 percent reduction; the actual tier settings use 75/80/85 percent. Descriptions list higher lumber and hunting satchels and crooks, but no player acquisition route for those higher items was verified in the guild menus or other current sources.
- **Ore bag contents:** the ore satchel's help lists saltpeter, but its accepted materials omit saltpeter and colored granites. Its plain Granite support does not cover every granite type.
- **Contracts:** F-20 approves skill checks on gathering and taming turn-ins, and F-38 approves rolled gathering work. Current contracts remain fixed and have no turn-in skill checks. F-38's ore-contract gates differ from the harvesting and smelting ladder; P235 also records reward inversions. This guide does not treat the proposed contract numbers as current rewards.
- **Smelting menu text:** P55 calls the ore-bag action Smelt. P57 and the current client-label code call it Smelt Ore.
- **Wood bonuses:** F-28 assumes the Burrows work already added a bow-bonus hook. P36 and P227 record Rootwood as cosmetic, with the extended-wood bonuses added separately by P227.
- **Consolidation:** P179 describes the Combined Logbook and League Field Satchel as proposals. P280 and current code contain their purchase and use paths.
