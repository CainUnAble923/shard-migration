# cc-P235: numbers pass for rolled Mining and Lumberjacking contracts (F-38)

2026-10-20. Brief: `D:\UO\cc-prompts\claimed\Bronze\cc-P235-work-order-numbers-pass.md`. Docs-only: nothing in `server\`,
`docker\` or the client changed; no tests. "C\" = `ShatteredLegacy\server\customizations\`, "PIN\" =
`D:\UO\ModernUO-pinned\Projects\UOContent\`. Every line number below was read today from the Bronze work copies
(`golem/Bronze/P235`). Where a number is an assumption and not a reading, it says so.

## Headlines

1. **The count is 39 Miners' and 23 Foresters' defs, not 41 and 23.** Parsed every `Register(new WorkOrderDef(` in
   `C\ClusterFWorkOrderSystem.cs` (115 in all: mining 39, rangers 33, foresters 23, smithing 15, custodians 5). Mining is
   25 ore and ingot (`:387-825`), 4 gem (`:841-917`), 10 stone (`:931-1102`), which is also cc-P47's count. F-38's 41 was
   not counted. The full list with gates and rewards is in section 1.
2. **The three inversions are real and bigger than F-38 says.** Every post-Valorite single-metal def pays less gold than
   Verite Haul's 2,500 (`:599-613`) except Celestial; Valorite Cache (`:654-668`) out-pays Celestial Tribute (`:811-825`)
   in standing and gold; Diamond Reserve (`:904-917`) pays 25,000, above every metal and stone def. Section 1.3.
3. **Today's worst farm is not an inversion, it is the jeweler.** All four gem contracts ask for stock gems that the
   jeweler sells (PIN `Mobiles\Vendors\SBInfo\SBJewel.cs:59-67`: Diamond 200 gold, Star Sapphire 125, Emerald 100 ...),
   20 at a time, restocked hourly and doubling to 999 when sold out (`GenericBuy.cs:105-109`, `BaseVendor.cs:130`).
   Diamond Reserve turns 600 gold of diamonds into 25,000 gold and 8,000 standing, repeatable at once (no cooldown,
   `:342`, `:376-377`). Stock gems are not mined on this shard (no mining hook references them; pinned mining's bonus
   gems are the six ML gems, PIN `Engines\Harvest\Mining.cs:208-217`). **Proposal: the stock gems leave the contracts;
   Rare finds ask for the six mined ML gems.** Decision 3.
4. **One formula, three payouts:** gold = amount x tier value x type multiplier; standing = the same number; guild tokens
   (Compact vouchers, Timber Tokens) = standing / 25 (today's own ratio, section 1.4). Tier values are in section 3; the
   check table in section 6 shows value per unit, gold per contract and gold per hour all rising strictly from Iron to
   Celestial and from plain logs to Starwood, and no type above 1.5x the plain contract per hour.
5. **The wood ladder has a hole the ore ladder does not.** Ore harvest was re-gated to the metal tiers by cc-P57 Part C
   (Platinum 112.5 .. Celestial 200, window +-40), so a miner climbs to 200 by mining. Extended wood harvest still needs a
   flat 100 Lumberjacking with windows that top out at 148 (`C\ClusterFLumberjackingExtension.cs:233-242`), so no
   lumberjack can pass 148, and a contract gated at Shadowbark 155 or above is unreachable. **The build needs the cc-P57
   pattern for wood** (harvest requirement = `ClusterFWoodTiers`, window +-40). Decision 4.
6. **Home: P48's contract engine, League batch 2, not today's static defs.** Rolled contracts need an instance with its
   own data (today's `WorkOrderEntry` stores only a def key, `:260-313`), Rush needs expiry (none today), Survey needs
   gather-after-accept progress, Haul needs a place and a mule check. cc-P47 3.2's `ContractInstance` has all four;
   adding them to `WorkOrderEntry` is the same work done twice. Section 8; fallback given.
7. **Named rotations:** keep the two Grand Tributes as weekly specials and the nine mixed-list commissions as a weekly
   rotation, all re-priced by the formula; retire the 47 single-material fixed defs (rolls replace them). Section 7.
8. **Decisions for Chase: 13**, one line each, in the section of that name. The draft build prompt follows them.

## 1. Today

### 1.1 The system

- `C\ClusterFWorkOrderSystem.cs` (2,495 lines). `WorkOrderDef` (`:63-128`) is static: key, guild, title, type (`:11-24`:
  11 kinds; Miners use ResourceContract, RefinementContract, GemContract, StoneContract; Foresters TimberContract),
  requirement lines (item type, amount), gates (standing, one skill, ore discovery Reported, wood discovery Reported),
  rewards (standing, vouchers, gold), repeatable. Every Miners' and Foresters' def is repeatable.
- `WorkOrderEntry` (`:260-313`) holds def key, guild, `AcceptedAt`, `CompletedAt`, taming progress. No expiry, no
  rolled data, no amount of its own.
- Limits: 3 active per guild (`MaxActiveOrdersPerGuild`, `:342`), one active copy per def (`CanAccept`, `:376-377`).
  No cooldown after a turn-in; the same def can be accepted again at once.
- Turn-in (`C\GuildContractLedgerGump.cs:537-541`): standing and currency added, gold created into the pack. Items are
  taken from pack and bank together, all or nothing (`ClusterFWorkOrderSystem.cs:226-251`, `GuildResources`). **No
  skill check anywhere on turn-in** (the only skill read is the gate, `GuildContractLedgerGump.cs:234`).

### 1.2 Every Miners' and Foresters' def

Columns: line range, key, title, requirement, gates (standing; Mining or Lumberjacking; discovery), rewards S standing /
V vouchers or tokens / G gold. All repeatable.

**Miners' Compact, ore and ingots (25)**

| Lines | Key | Title | Requires | Gate | S / V / G |
|---|---|---|---|---|---|
| 387-400 | mining.iron_ingots_s | Iron Shipment | 50 Iron Ingots | 0; none | 100 / 5 / 75 |
| 402-415 | mining.iron_ore_s | Raw Ore Sample | 100 Iron Ore | 0; none | 75 / 4 / 60 |
| 419-432 | mining.iron_ingots_m | Iron Bulk Order | 250 Iron Ingots | 0; Mining 30 | 600 / 30 / 350 |
| 437-451 | mining.dull_copper_ingots_s | Dull Copper Shipment | 30 Dull Copper Ingots | 1,000; Mining 40; DullCopper | 250 / 12 / 350 |
| 453-471 | mining.forge_resupply_m | Forge Resupply | 200 Iron + 50 Dull Copper Ingots | 1,000; Mining 45; DullCopper | 600 / 28 / 500 |
| 475-489 | mining.shadow_iron_s | Shadow Iron Shipment | 20 Shadow Iron Ingots | 5,000; Mining 50; ShadowIron | 300 / 14 / 500 |
| 491-505 | mining.copper_s | Copper Delivery | 20 Copper Ingots | 5,000; Mining 50; Copper | 300 / 14 / 500 |
| 507-521 | mining.ore_refinement_s | Ore Refinement Run | 150 Iron Ore | 5,000; Mining 50 | 350 / 16 / 400 |
| 523-541 | mining.deep_veins_m | Deep Veins Run | 40 Shadow Iron + 25 Copper Ingots | 5,000; Mining 55; ShadowIron | 900 / 40 / 750 |
| 545-559 | mining.bronze_s | Bronze Consignment | 15 Bronze Ingots | 15,000; Mining 60; Bronze | 500 / 22 / 1,000 |
| 561-575 | mining.agapite_s | Agapite Cache | 12 Agapite Ingots | 15,000; Mining 65; Agapite | 600 / 26 / 1,500 |
| 577-595 | mining.mid_tier_metals_m | Mixed Mid-Tier Metals | 50 Shadow Iron + 25 Bronze Ingots | 15,000; Mining 65; Bronze | 1,200 / 52 / 1,500 |
| 599-613 | mining.verite_s | Verite Haul | 8 Verite Ingots | 40,000; Mining 70; Verite | 1,000 / 44 / 2,500 |
| 615-629 | mining.valorite_s | Valorite Delivery | 6 Valorite Ingots | 40,000; Mining 80; Valorite | 1,500 / 60 / 4,000 |
| 631-650 | mining.high_metals_m | Rare Metals Commission | 20 Bronze + 10 Agapite + 8 Verite Ingots | 40,000; Mining 80; Verite | 2,800 / 112 / 3,000 |
| 654-668 | mining.valorite_cache | Valorite Cache | 20 Valorite Ingots | 80,000; Mining 90; Valorite | 6,000 / 240 / 10,000 |
| 670-692 | mining.grand_tribute | Grand Forge Tribute | 100 Iron, 50 Shadow Iron, 30 Bronze, 20 Agapite, 10 Verite, 5 Valorite Ingots | 80,000; Mining 95; Valorite | 5,000 / 200 / 5,000 |
| 699-713 | mining.platinum_s | Platinum Consignment | 10 Platinum Ingots | 15,000; Mining 65; Platinum | 800 / 32 / 500 |
| 715-729 | mining.toxic_s | Toxic Ore Delivery | 10 Toxic Ingots | 15,000; Mining 65; Toxic | 800 / 32 / 500 |
| 731-745 | mining.blaze_s | Blaze Metal Consignment | 10 Blaze Ingots | 15,000; Mining 65; Blaze | 1,000 / 40 / 750 |
| 747-761 | mining.frost_s | Frost Alloy Run | 10 Frost Ingots | 15,000; Mining 65; Frost | 1,000 / 40 / 750 |
| 763-777 | mining.obsidian_s | Obsidian Cache | 8 Obsidian Ingots | 40,000; Mining 75; Obsidian | 1,500 / 60 / 1,000 |
| 779-793 | mining.mythril_s | Mythril Reserve | 6 Mythril Ingots | 40,000; Mining 80; Mythril | 1,800 / 72 / 1,500 |
| 795-809 | mining.adamantium_s | Adamantium Delivery | 5 Adamantium Ingots | 80,000; Mining 90; Adamantium | 3,000 / 120 / 2,000 |
| 811-825 | mining.celestial_s | Celestial Tribute | 3 Celestial Ingots | 80,000; Mining 95; Celestial | 5,000 / 200 / 5,000 |

**Miners' Compact, gems (4)**

| Lines | Key | Title | Requires | Gate | S / V / G |
|---|---|---|---|---|---|
| 841-859 | mining.common_gems_s | Common Gem Cache | 5 Citrine, 5 Amber, 5 Tourmaline | 5,000; Mining 50 | 800 / 35 / 2,000 |
| 863-881 | mining.fine_gems_s | Fine Gem Consignment | 5 Amethyst, 5 Sapphire, 5 Ruby | 40,000; Mining 70 | 2,500 / 100 / 8,000 |
| 885-902 | mining.rare_gems_s | Rare Gem Tribute | 3 Star Sapphire, 3 Emerald | 80,000; Mining 80 | 5,000 / 200 / 15,000 |
| 904-917 | mining.diamond_cache | Diamond Reserve | 3 Diamond | 80,000; Mining 90 | 8,000 / 320 / 25,000 |

**Miners' Compact, stone (10)**

| Lines | Key | Title | Requires | Gate | S / V / G |
|---|---|---|---|---|---|
| 931-944 | mining.granite_haul_s | Granite Haul | 50 Granite | 0; Mining 30 | 250 / 12 / 400 |
| 946-959 | mining.granite_haul_m | Granite Bulk Order | 200 Granite | 0; Mining 40 | 1,200 / 52 / 1,500 |
| 963-977 | mining.dull_copper_granite_s | Dull Copper Stone Delivery | 30 Dull Copper Granite | 1,000; Mining 40; DullCopper | 300 / 14 / 600 |
| 981-995 | mining.shadow_stone_s | Shadow Stone Cache | 20 Shadow Iron Granite | 5,000; Mining 50; ShadowIron | 400 / 18 / 900 |
| 997-1016 | mining.mixed_stone_m | Mixed Stone Commission | 100 Granite, 30 Dull Copper, 20 Shadow Iron Granite | 5,000; Mining 55; ShadowIron | 1,200 / 52 / 2,000 |
| 1020-1034 | mining.bronze_stone_s | Bronze Granite Consignment | 15 Bronze Granite | 15,000; Mining 60; Bronze | 600 / 26 / 1,800 |
| 1036-1050 | mining.gold_granite_s | Gold Granite Cache | 12 Gold Granite | 15,000; Mining 62; Gold | 700 / 30 / 2,200 |
| 1054-1068 | mining.agapite_granite_s | Agapite Stone Delivery | 10 Agapite Granite | 40,000; Mining 70; Agapite | 1,200 / 50 / 4,000 |
| 1070-1084 | mining.verite_granite_s | Verite Stone Haul | 8 Verite Granite | 40,000; Mining 75; Verite | 1,800 / 72 / 6,000 |
| 1088-1102 | mining.valorite_granite_s | Valorite Stone Tribute | 5 Valorite Granite | 80,000; Mining 90; Valorite | 4,000 / 160 / 12,000 |

**Foresters' Union (23)**

| Lines | Key | Title | Requires | Gate | S / V / G |
|---|---|---|---|---|---|
| 1995-2008 | foresters.boards_s | Timber Delivery | 50 Boards | 0; none | 75 / 4 / 60 |
| 2010-2023 | foresters.boards_m | Timber Bulk Order | 250 Boards | 0; Lumberjacking 30 | 600 / 30 / 350 |
| 2027-2040 | foresters.oak_boards_s | Oak Timber Delivery | 30 Oak Boards | 1,000; Lumberjacking 40 | 250 / 12 / 350 |
| 2042-2055 | foresters.ash_boards_s | Ash Timber Delivery | 30 Ash Boards | 1,000; Lumberjacking 40 | 250 / 12 / 350 |
| 2057-2070 | foresters.camp_lumber_s | Field Camp Lumber | 100 Boards | 1,000; none | 300 / 14 / 300 |
| 2074-2087 | foresters.yew_boards_s | Yew Consignment | 20 Yew Boards | 5,000; Lumberjacking 50 | 400 / 18 / 700 |
| 2089-2107 | foresters.mixed_timber_m | Mixed Timber Commission | 100 Boards, 30 Oak, 20 Ash Boards | 5,000; Lumberjacking 50 | 900 / 40 / 800 |
| 2111-2124 | foresters.heartwood_s | Heartwood Delivery | 15 Heartwood Boards | 15,000; Lumberjacking 65 | 700 / 30 / 1,500 |
| 2126-2143 | foresters.quality_timber_m | Quality Timber Cache | 30 Yew + 15 Heartwood Boards | 15,000; Lumberjacking 60 | 1,200 / 52 / 2,000 |
| 2147-2160 | foresters.bloodwood_s | Bloodwood Haul | 10 Bloodwood Boards | 40,000; Lumberjacking 75 | 1,500 / 60 / 4,000 |
| 2162-2175 | foresters.frostwood_s | Frostwood Cache | 8 Frostwood Boards | 40,000; Lumberjacking 75 | 1,500 / 60 / 4,000 |
| 2177-2195 | foresters.rare_timber_m | Rare Timber Commission | 10 Bloodwood, 8 Frostwood, 10 Heartwood Boards | 40,000; Lumberjacking 75 | 2,800 / 112 / 6,000 |
| 2199-2219 | foresters.grand_tribute | Grand Forest Tribute | 100 Boards, 50 Yew, 20 Heartwood, 8 Bloodwood, 5 Frostwood Boards | 80,000; Lumberjacking 90 | 5,000 / 200 / 10,000 |
| 2223-2240 | foresters.rangers_supply_cross | Rangers' Field Lumber | 100 Boards + 30 Oak Boards | 1,000; none | 500 / 22 / 400 |
| 2244-2258 | foresters.ironwood_s | Ironwood Consignment | 8 Ironwood Boards | 40,000; Lumberjacking 100; Ironwood | 1,800 / 70 / 3,500 |
| 2260-2274 | foresters.ghostwood_s | Ghostwood Consignment | 6 Ghostwood Boards | 40,000; Lumberjacking 100; Ghostwood | 2,000 / 80 / 4,000 |
| 2276-2290 | foresters.emberbark_s | Emberbark Consignment | 6 Emberbark Boards | 40,000; Lumberjacking 100; Emberbark | 2,000 / 80 / 4,000 |
| 2292-2306 | foresters.frostbark_s | Frostbark Consignment | 5 Frostbark Boards | 40,000; Lumberjacking 100; Frostbark | 2,200 / 88 / 4,500 |
| 2308-2322 | foresters.shadowbark_s | Shadowbark Consignment | 5 Shadowbark Boards | 80,000; Lumberjacking 100; Shadowbark | 2,500 / 100 / 5,000 |
| 2324-2338 | foresters.runewood_s | Runewood Consignment | 4 Runewood Boards | 80,000; Lumberjacking 100; Runewood | 3,000 / 120 / 6,000 |
| 2340-2354 | foresters.voidwood_s | Voidwood Consignment | 3 Voidwood Boards | 80,000; Lumberjacking 100; Voidwood | 3,500 / 140 / 7,000 |
| 2356-2370 | foresters.starwood_s | Starwood Consignment | 2 Starwood Boards | 80,000; Lumberjacking 100; Starwood | 4,000 / 160 / 8,000 |
| 2372-2391 | foresters.exotic_timber_m | Exotic Timber Collection | 3 Ironwood, 2 Emberbark, 2 Runewood Boards | 80,000; Lumberjacking 100; Ironwood | 4,500 / 180 / 9,000 |

Confirms F-38's reading: one ore def (plus Ore Refinement Run, also iron ore), everything else ingots, granite or gems;
Foresters are boards only, no logs and none of the ML extras.

### 1.3 The inversions, with lines

1. **Post-Valorite pays less than Verite.** Verite Haul `:599-613`: 8 ingots, 2,500 gold (312 per ingot). Platinum
   Consignment `:699-713` and Toxic Ore Delivery `:715-729`: 10 ingots, 500 gold (50 per ingot). Blaze and Frost
   `:731-761` 750; Obsidian `:763-777` 1,000; Mythril `:779-793` 1,500; Adamantium `:795-809` 2,000: all under Verite.
   Only Celestial Tribute `:811-825` (5,000) beats Verite, and it is under Valorite Cache `:654-668` (10,000).
2. **Valorite Cache over Celestial.** Valorite Cache `:654-668`: 6,000 standing, 240 vouchers, 10,000 gold. Celestial
   Tribute `:811-825`: 5,000 / 200 / 5,000, for the metal that needs 200 Mining to dig.
3. **Diamonds over every metal.** Diamond Reserve `:904-917`: 25,000 gold and 8,000 standing for 3 diamonds. The best
   metal def is Valorite Cache's 10,000; the best stone def Valorite Stone Tribute `:1088-1102` 12,000; Rare Gem Tribute
   `:885-902` 15,000.

**Gates off the ladder (F-38's second finding, confirmed):** Platinum, Toxic, Blaze and Frost at Mining 65 (`:708, :724,
:740, :756`) against harvest and smelt tiers 112.5, 125, 137.5, 150 (`C\ClusterFMetalTiers.cs:20-23`). All eight woods at
a flat Lumberjacking 100 (`:2251, :2267, :2283, :2299, :2315, :2331, :2347, :2363`).

### 1.4 Today's reward shape, for reuse

Vouchers and Timber Tokens track standing: 100 to 5, 600 to 30 (one twentieth) at the bottom; 800 to 32, 1,500 to 60,
5,000 to 200, 6,000 to 240 (one twenty-fifth) everywhere above. Standing and gold have no fixed ratio: standing is
above gold on the iron defs (600 against 350) and below it on the top ones (6,000 against 10,000).

Ranks, for the standing gates (Compact `C\MinersCompactLiaisonGump.cs:682-690`, Foresters
`C\ForestersGuildmasterGump.cs:333-341`): 1,000 / 5,000 / 15,000 / 40,000 / 80,000 / 150,000. Compact purchases the
vouchers buy (`MinersCompactLiaisonGump.cs:74-97`): satchel T2 to T5 at 25 / 75 / 150 / 250 vouchers and 5,000 / 20,000 /
50,000 / 100,000 gold; the climbing boots (F-36) repeat the T3 to T5 pattern.

## 2. The ladders as they are now

**Ore (one table, `C\ClusterFMetalTiers.cs`).** `RequiredSkill` (`:43-63`): Iron 0, Dull Copper 65, Shadow Iron 70,
Copper 75, Bronze 80, Gold 85, Agapite 90, Verite 95, Valorite 99, Platinum 112.5, Toxic 125, Blaze 137.5, Frost 150,
Obsidian 162.5, Mythril 175, Adamantium 187.5, Celestial 200 (`:20-27`; cc-P53 Part B, Chase 2026-10-04). Dawnstone 45
(`:34`) is cc-P36's starter metal, never post-Valorite (`:40`).
- **Mining harvest sits on the same numbers.** Stock colored ore: required 65 .. 99, window required -40 to +40 (PIN
  `Engines\Harvest\Mining.cs:115-187`). Post-Valorite: required = the tier, window +-40 (`C\ClusterFMiningExtension.cs:
  101-110, :153-157`; cc-P57 Part C, Chase 2026-10-05). So Celestial is 160-240 and a miner climbs to the 200 cap by
  mining. Under the tier a vein gives iron.
- **Vein weights** (banks of 8 x 8 tiles, `Mining.cs:86-87`): Iron 496, Dull Copper 112, Shadow Iron 98, Copper 84,
  Bronze 70, Gold 56, Agapite 42, Verite 28, Valorite 14 (`Mining.cs:189-201`), Platinum 8 down to Celestial 1
  (`ClusterFMiningExtension.cs:131-141`), 1,036 in all. Veins are permanent (`:150`, seeded by coordinates).
- **Granite:** with the stone-mining book and the toggle, at Mining 100+, one dig in ten gives the vein's granite
  instead of its ore (`Mining.cs:284-287`). ML gems: six, 0.1 percent each per dig at 100+ (`Mining.cs:208-217`).
- **Loops (F-12):** the skill cap is 50, then 100, then +5 per loop to 200 at loop 21 (`notes\f12-levels-loops-caps.md:3`;
  F-36 states the Mining gates 120/150/180 as loops 5/11/17). A tier above 100 is therefore also a loop gate:
  loop = (tier - 100) / 5, rounded up (Platinum 112.5 is loop 3, Celestial loop 20). Contract gates inherit this
  without any work.

**Wood (`C\ClusterFWoodTiers.cs`, cc-P67 Part A).** `RequiredSkill` (`:36-48`): Ironwood 100, Ghostwood 115, Emberbark
130, Frostbark 140, Shadowbark 155, Runewood 170, Voidwood 185, Starwood 200 (`:19-26`; F-28 item 3, Chase
2026-10-02). Rootwood 45 is cc-P36's starter (`:33`). **These are Carpentry and Fletching numbers**; the file's own header
says so (`:9`, "Lumberjacking's harvest numbers are separate (the trees still need 100 Lumberjacking)").
- **Lumberjacking harvest today:** stock Oak 65, Ash 80, Yew 95, Heartwood, Bloodwood and Frostwood 100, windows
  required -40 to +40 (PIN `Engines\Harvest\Lumberjacking.cs:71-77`); the eight extended woods **all required 100** with
  windows 60-140 (Ironwood) to 68-148 (Voidwood, Starwood) (`C\ClusterFLumberjackingExtension.cs:233-242`). Nothing teaches
  Lumberjacking past 148 (cc-P54 `:485`; cc-P67 `:300-301`: P54 B.3's raise "not built").
- **Vein weights** (banks of 4 x 3, `Lumberjacking.cs:43-44`): Regular 490, Oak 300, Ash 100, Yew 50, Heartwood 30,
  Bloodwood 20, Frostwood 10 (`:82-88`), Ironwood 8 down to Starwood 1 (`ClusterFLumberjackingExtension.cs:254-263`),
  1,036 in all; groves permanent (`:274`, cc-P37). Rarity order matches the ore ladder position for position (F-28).
- **ML extras** per chop at 100+: bark fragment 10 percent, luminescent fungi 3, switch 2, parasitic plant 1, brilliant
  amber 0.1 (`Lumberjacking.cs:91-98`).

**Where the contract gates sit (proposal):** a contract for material M is offered when the player's harvest skill is at
or above M's requirement **on the harvest ladder** and M is Reported in the player's ledger (today's discovery gate,
`WorkOrderDef.RequiredDiscovery` / `RequiredWoodDiscovery`, kept). For ore that ladder is `ClusterFMetalTiers`. For wood it
must become `ClusterFWoodTiers` applied to Lumberjacking, which means re-gating the extended trees exactly as cc-P57 did
for ore: requirement = the wood's tier, window tier -40 to tier +40 (Ironwood 60-140 .. Starwood 160-240). That also
answers P54 B.3 (Lumberjacking's climb to 200) with the same shape the ore side already has. A GM lumberjack loses
Ghostwood to Starwood trees until they climb, as GM miners lost Toxic to Celestial on 2026-10-05. **Decision 4.** Until it
is built, wood contracts above Frostbark (140) can be offered but never trained for.

## 3. Tier values

One value per material, gold per unit; standing per unit is the same number; tokens one twenty-fifth. The curve is set
so that gold per hour rises gently with tier (about 1,000 at Iron to about 6,000 at Celestial) given the yield
assumptions in 3.3. Change the yields and the values move; the shape (strictly rising per unit, per contract and per
hour) is what the build should test, not the exact numbers.

### 3.1 Miners (ore, ingot, granite, gems)

| Material | Mining | Gold per ingot or ore | Granite (x2, see below) | Why this step |
|---|---|---|---|---|
| Iron | 0 | 2 | 4 | below the vendor's 4 (SBBlacksmith.cs:119) so buying iron to turn in never pays |
| Dull Copper | 65 | 5 | 10 | first colored step |
| Shadow Iron | 70 | 6 | 12 | |
| Copper | 75 | 8 | 16 | |
| Bronze | 80 | 10 | 20 | |
| Gold | 85 | 13 | 26 | |
| Agapite | 90 | 17 | 34 | |
| Verite | 95 | 24 | 48 | |
| Valorite | 99 | 36 | 72 | top of the stock ladder; 1.5x Verite |
| Platinum | 112.5 | 48 | 96 | post-Valorite starts above Valorite, closing inversion 1 |
| Toxic | 125 | 60 | 120 | |
| Blaze | 137.5 | 75 | 150 | |
| Frost | 150 | 100 | 200 | |
| Obsidian | 162.5 | 125 | 250 | |
| Mythril | 175 | 150 | 300 | |
| Adamantium | 187.5 | 190 | 380 | |
| Celestial | 200 | 240 | 480 | top; 120x iron per unit, about 6x iron per hour |

- **Ore and ingot share a value.** Large ore smelts one to one (PIN `Items\Resources\Blacksmithing\Ore.cs:213-230`); the
  Raw sample multiplier (section 4) carries the difference, not the value.
- **Granite is twice the ingot value and a quarter of the amount roll.** One granite costs ten digs' worth of attention
  while the other nine digs still give ore (`Mining.cs:284-287`), so it is a side contract, offered only to a player with
  the stone-mining book. Decision 13.
- **Gems (Rare finds):** the six ML mining gems (Blue Diamond, Dark Sapphire, Ecru Citrine, Fire Ruby, Perfect Emerald,
  Turquoise; `Mining.cs:208-217`), each 0.1 percent per dig at Mining 100+, not sold by any vendor: **600 gold each**, any
  kind, or **1,500** for a named kind. The nine stock gems leave the contracts (headline 3). Decision 3.

### 3.2 Foresters (logs, boards, ML extras)

| Material | Lumberjacking (proposed ladder) | Gold per board or log | Why this step |
|---|---|---|---|
| Regular | 0 | 1 | below the carpenter's 2 for boards (SBCarpenter.cs:71) and 1 for logs (:81) |
| Oak | 65 | 3 | |
| Ash | 80 | 7 | |
| Yew | 95 | 12 | |
| Heartwood | 100 | 18 | the three stock 100 woods are split by vein weight 30 / 20 / 10 |
| Bloodwood | 100 | 24 | |
| Frostwood | 100 | 32 | |
| Ironwood | 100 | 44 | first extended wood; above Frostwood, as F-28 scales the bonuses |
| Ghostwood | 115 | 56 | |
| Emberbark | 130 | 70 | |
| Frostbark | 140 | 85 | |
| Shadowbark | 155 | 105 | |
| Runewood | 170 | 130 | |
| Voidwood | 185 | 180 | |
| Starwood | 200 | 240 | the same top as Celestial |

- **ML extras (Rare finds):** bark fragment 100, luminescent fungi 300, switch 450, parasitic plant 900, brilliant amber
  8,000, from their drop rates (10 / 3 / 2 / 1 / 0.1 percent per chop, `Lumberjacking.cs:91-98`) at about 90 chops an
  hour (3.3). None is sold by a vendor (no `GenericBuyInfo` for them under PIN `Mobiles\Vendors\SBInfo`).
- **Dawnstone and Rootwood** (cc-P36 starters, dungeon-only) stay out of the rolls. Decision 9.

### 3.3 The yield assumptions behind the curve

These are **estimates, not readings**; they are the one input the build should replace with the overnight bot's
mining and logging logs once it has them. What is read: a dig or chop takes 1.6 s (`Mining.cs:102`, `Lumberjacking.cs:
58`, `HarvestTimer.cs:19, :27`), gives 1 ore (2 in Felucca) or 10 logs (20) (`Mining.cs:97-98`, `Lumberjacking.cs:53-54`),
from banks of 10-34 ore respawning in 10-20 minutes or 20-45 logs in 20-30 (`Mining.cs:88-91`, `Lumberjacking.cs:45-48`).
Ore and boards take tiledata's weight (`Server\Items\Item.cs:504`; the standard values are 12 and 1, and the tile lookup
tool failed today, so those two are unverified here), ingots 0.1 (`Ingots.cs:17`), granite 1 (`Granite.cs:16`), logs 2
(`Log.cs:29`). The mechanical ceiling is 2,250 digs an hour; walking, pack trips (33 ore per 400 stones) and smelting take
most of it.

| Material | Assumed units an hour, Trammel | Reasoning |
|---|---|---|
| Iron / regular logs | 600 ore / 900 logs | everywhere; the pack trip is the limit |
| Dull Copper .. Valorite | 300 down to 90 | bank-limited: a known bank gives about 22 ore per 15 minutes; a miner cycles several |
| Platinum .. Celestial | 80 down to 30 | one bank in 130 to one in 1,036; the logbook's travel makes 1-3 known banks the norm |
| Oak .. Frostwood | 500 down to 70 | 29 percent of banks down to 1 percent; 10 logs a chop |
| Ironwood .. Starwood | 60 down to 25 | as the rare ores |

Felucca doubles the per-dig amounts, so every rate below doubles there; the formula does not change, the contract is
simply done in half the time (the same is true of every BOD).

## 4. Types and multipliers

| Type | Multiplier | Amount | Form | Deadline or condition | Offered when |
|---|---|---|---|---|---|
| **Consignment** (the plain roll) | 1.0 | the tier's roll | ingots or boards | none | always |
| **Raw sample** | 0.9 | the tier's roll | ore or logs | none | always |
| **Rush** | 1.5 | the tier's roll | ingots or boards | **60 minutes of real time from accept** (the mid roll takes about 30 at the assumed yields). On expiry it **downgrades to a Consignment at 1.0**, it does not vanish, so the material is not wasted | 15 percent of offers |
| **Survey** | 1.25 | half the tier's roll | ore or logs | gathered **inside a named region** from a bank or grove **not yet in the player's ledger**; completing it writes the record (P13 grove record / `OreLocationRecord`), Reported, so the next tier's materials can be rolled | 10 percent |
| **Haul** | 1.3 | **twice** the tier's roll | ore or logs (the heavy form) | **requires a bonded Compact Mule** (F-38, Chase): the goods are taken from the mule's pack at a **depot in another town**; amount capped so it fits the mule's pack (tier 1 1,600 stones, cc-P69 table: 130 ore or 800 logs), so a bigger mule means a bigger haul; no deadline | 10 percent, only when the player owns a mule; otherwise a Consignment |
| **Rare finds** | 1.0 | small (below) | ML gems or ML extras | none | 5 percent, only at Mining or Lumberjacking 100+ (the extras need 100, `Mining.cs:208`, `Lumberjacking.cs:94`) |

Rare finds amounts: any mining gem 2-4; a named gem 1-2; bark fragment 6-12, fungi 2-4, switch 2-3, parasitic plant 1-2,
brilliant amber 1. At the assumed rates a bark contract is about an hour of logging as a byproduct and an amber
contract about ten; both pay like a contract of the player's tier.

Why these multipliers: Rush is the only type that pays more per hour than the plain roll (1.5x) and it is rationed by the
offer roll; Haul's 1.3x is eaten by the trip, so per hour it lands at 1.2x with a bigger single payout; Survey pays less
per hour than a Consignment (0.73x) because the record is the reward; Raw sample is 0.9x for skipping the forge and the
smelt loss. Section 6 has the numbers.

Depots do not exist yet: every guild institution stands in New Haven (`C\ClusterFInstitutionSeeder.cs:8-66`, all
Trammel 3510-3516, 2747-2748). Proposal: a Compact Depot Clerk in Minoc and Britain, a Foresters' Depot Clerk in Yew and
Skara Brae, each a vendor-less NPC with one gump button, Deliver. Decision 6.

## 5. Rolls

**Amount per tier (Consignment and Rush; Raw sample the same; Survey half; Haul double).** The roll is uniform between
one third and two thirds of the tier's assumed hourly yield, rounded to 5 (so 20 to 40 minutes of gathering):

| Metal | Roll | | Wood | Roll |
|---|---|---|---|---|
| Iron | 200-400 | | Regular | 300-600 |
| Dull Copper | 100-200 | | Oak | 165-335 |
| Shadow Iron | 95-185 | | Ash | 85-165 |
| Copper | 85-175 | | Yew | 50-100 |
| Bronze | 80-160 | | Heartwood | 35-75 |
| Gold | 65-135 | | Bloodwood | 30-60 |
| Agapite | 55-105 | | Frostwood | 25-45 |
| Verite | 40-80 | | Ironwood | 20-40 |
| Valorite | 30-60 | | Ghostwood | 18-35 |
| Platinum | 25-55 | | Emberbark | 17-35 |
| Toxic | 25-45 | | Frostbark | 15-30 |
| Blaze | 20-40 | | Shadowbark | 13-25 |
| Frost | 17-35 | | Runewood | 12-25 |
| Obsidian | 15-30 | | Voidwood | 10-20 |
| Mythril | 13-25 | | Starwood | 8-17 |
| Adamantium | 12-25 | | | |
| Celestial | 10-20 | | | |

Granite: a quarter of the metal's roll (Iron 50-100 .. Valorite 8-15; post-Valorite granite exists, `ClusterFMiningExtension.
cs:101-110`, so the table continues to Celestial 3-5).

**How the material is picked.** Eligible = every material whose harvest requirement is at or below the player's skill
(Base, as the harvest check uses, `HarvestSystem.cs:147`) **and** that is Reported in the player's ledger (iron and
regular logs always). Weights: the highest eligible tier 45, the next 25, the next 15, the rest share 15. A GM miner still
gets an iron roll now and then (the Compact still needs iron); it pays a fifth of their Celestial rate, which is a nudge
to leave it, not a farm. The discovery gate keeps the ledgers meaningful and makes Survey the way up. Decision 12.

**Offers, like BODs (F-20).** Each character holds **4 rolled offers per guild**, drawn when the ledger is opened and
each kept for **6 hours**; an accepted or expired offer is re-rolled, a declined one is not (no reroll fishing). The
active cap stays 3 per guild (`:342`). Type frequency per roll: Consignment 40, Raw sample 20, Rush 15, Survey 10, Haul
10, Rare finds 5 (Haul and Rare finds fall back to Consignment and Raw sample when their condition is not met). Decision
10.

**Turn-in skill check, per material (F-20: "like BODs").** The window is the material's harvest requirement **-20 to
+20**, iron and regular logs 0-55: the shape `ClusterFSmithBODSystem.GetSkillRange` uses for post-Valorite
(`C\ClusterFSmithBODSystem.cs:525-530`) and its None row (`:516`). As with BODs it is a gain check, not a pass check: the
turn-in always succeeds; the check is a chance to gain Mining or Lumberjacking. **Three checks per turn-in**, one per
third of the amount (a BOD of six items is one check; a 300-ingot contract deserves more). The windows: Dull Copper
45-85, Valorite 79-119, Platinum 92.5-132.5 .. Celestial 180-220 (clipped at the cap); Oak 45-85 .. Starwood 180-220.
Decision 11. Note the training value for wood above 148 depends on Decision 4: without the tree re-gate, the turn-in is
the only thing that trains Lumberjacking past 148, three rolls per contract.

## 6. Formula check

Formula: **gold = amount x tier value x type multiplier; standing = gold; tokens = round(standing / 25).** Mid roll,
assumed yields (3.3), plus 5 minutes of turn-in per contract (15 for Survey and Haul, which travel; 3 for Raw sample,
which skips the forge). Generated by `numbers.py` in the P235 scratchpad from the tables above; the monotonic check is
the script's own assert.

### 6.1 Pay rises with tier

| # | Material | Mining | Vein weight | Assumed ingots/h | Value | Roll | Mid | Gold, mid | Standing, mid | Tokens, mid | Minutes | Gold/h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Iron | 0 | 496 | 600 | 2 | 200-400 | 300 | 600 | 600 | 24 | 35 | 1,029 |
| 1 | Dull Copper | 65 | 112 | 300 | 5 | 100-200 | 150 | 750 | 750 | 30 | 35 | 1,286 |
| 2 | Shadow Iron | 70 | 98 | 280 | 6 | 95-185 | 140 | 840 | 840 | 34 | 35 | 1,440 |
| 3 | Copper | 75 | 84 | 260 | 8 | 85-175 | 130 | 1,040 | 1,040 | 42 | 35 | 1,783 |
| 4 | Bronze | 80 | 70 | 240 | 10 | 80-160 | 120 | 1,200 | 1,200 | 48 | 35 | 2,057 |
| 5 | Gold | 85 | 56 | 200 | 13 | 65-135 | 100 | 1,300 | 1,300 | 52 | 35 | 2,229 |
| 6 | Agapite | 90 | 42 | 160 | 17 | 55-105 | 80 | 1,360 | 1,360 | 54 | 35 | 2,331 |
| 7 | Verite | 95 | 28 | 120 | 24 | 40-80 | 60 | 1,440 | 1,440 | 58 | 35 | 2,469 |
| 8 | Valorite | 99 | 14 | 90 | 36 | 30-60 | 45 | 1,620 | 1,620 | 65 | 35 | 2,777 |
| 9 | Platinum | 112.5 | 8 | 80 | 48 | 25-55 | 40 | 1,920 | 1,920 | 77 | 35 | 3,291 |
| 10 | Toxic | 125 | 7 | 70 | 60 | 25-45 | 35 | 2,100 | 2,100 | 84 | 35 | 3,600 |
| 11 | Blaze | 137.5 | 6 | 60 | 75 | 20-40 | 30 | 2,250 | 2,250 | 90 | 35 | 3,857 |
| 12 | Frost | 150 | 5 | 50 | 100 | 17-35 | 26 | 2,600 | 2,600 | 104 | 36 | 4,309 |
| 13 | Obsidian | 162.5 | 4 | 45 | 125 | 15-30 | 22 | 2,750 | 2,750 | 110 | 34 | 4,806 |
| 14 | Mythril | 175 | 3 | 40 | 150 | 13-25 | 19 | 2,850 | 2,850 | 114 | 34 | 5,104 |
| 15 | Adamantium | 187.5 | 2 | 35 | 190 | 12-25 | 18 | 3,420 | 3,420 | 137 | 36 | 5,723 |
| 16 | Celestial | 200 | 1 | 30 | 240 | 10-20 | 15 | 3,600 | 3,600 | 144 | 35 | 6,171 |

Value per unit, gold per contract and gold per hour all rise strictly down the table: **PASS**.

| # | Material | Lumberjacking (proposed) | Vein weight | Assumed boards/h | Value | Roll | Mid | Gold, mid | Standing, mid | Tokens, mid | Minutes | Gold/h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Regular | 0 | 490 | 900 | 1 | 300-600 | 450 | 450 | 450 | 18 | 35 | 771 |
| 1 | Oak | 65 | 300 | 500 | 3 | 165-335 | 250 | 750 | 750 | 30 | 35 | 1,286 |
| 2 | Ash | 80 | 100 | 250 | 7 | 85-165 | 125 | 875 | 875 | 35 | 35 | 1,500 |
| 3 | Yew | 95 | 50 | 150 | 12 | 50-100 | 75 | 900 | 900 | 36 | 35 | 1,543 |
| 4 | Heartwood | 100 | 30 | 110 | 18 | 35-75 | 55 | 990 | 990 | 40 | 35 | 1,697 |
| 5 | Bloodwood | 100 | 20 | 90 | 24 | 30-60 | 45 | 1,080 | 1,080 | 43 | 35 | 1,851 |
| 6 | Frostwood | 100 | 10 | 70 | 32 | 25-45 | 35 | 1,120 | 1,120 | 45 | 35 | 1,920 |
| 7 | Ironwood | 100 | 8 | 60 | 44 | 20-40 | 30 | 1,320 | 1,320 | 53 | 35 | 2,263 |
| 8 | Ghostwood | 115 | 7 | 55 | 56 | 18-35 | 26 | 1,456 | 1,456 | 58 | 33 | 2,618 |
| 9 | Emberbark | 130 | 6 | 50 | 70 | 17-35 | 26 | 1,820 | 1,820 | 73 | 36 | 3,017 |
| 10 | Frostbark | 140 | 5 | 45 | 85 | 15-30 | 22 | 1,870 | 1,870 | 75 | 34 | 3,268 |
| 11 | Shadowbark | 155 | 4 | 40 | 105 | 13-25 | 19 | 1,995 | 1,995 | 80 | 34 | 3,573 |
| 12 | Runewood | 170 | 3 | 35 | 130 | 12-25 | 18 | 2,340 | 2,340 | 94 | 36 | 3,916 |
| 13 | Voidwood | 185 | 2 | 30 | 180 | 10-20 | 15 | 2,700 | 2,700 | 108 | 35 | 4,629 |
| 14 | Starwood | 200 | 1 | 25 | 240 | 8-17 | 12 | 2,880 | 2,880 | 115 | 34 | 5,112 |

**PASS** on the same three columns.

### 6.2 No type is a farm (gold an hour by type, same tier)

| Material | Consignment | Raw sample | Rush | Survey | Haul | | Per contract: Consignment | Raw | Rush | Survey | Haul |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Iron | 1,029 | 982 | 1,543 | 750 | 1,248 | | 600 | 540 | 900 | 375 | 1,560 |
| Dull Copper | 1,286 | 1,227 | 1,929 | 938 | 1,560 | | 750 | 675 | 1,125 | 469 | 1,950 |
| Bronze | 2,057 | 1,964 | 3,086 | 1,500 | 2,496 | | 1,200 | 1,080 | 1,800 | 750 | 3,120 |
| Valorite | 2,777 | 2,651 | 4,166 | 2,002 | 3,370 | | 1,620 | 1,458 | 2,430 | 990 | 4,212 |
| Platinum | 3,291 | 3,142 | 4,937 | 2,400 | 3,994 | | 1,920 | 1,728 | 2,880 | 1,200 | 4,992 |
| Frost | 4,309 | 4,105 | 6,464 | 3,186 | 5,240 | | 2,600 | 2,340 | 3,900 | 1,625 | 6,760 |
| Celestial | 6,171 | 5,891 | 9,257 | 4,645 | 7,488 | | 3,600 | 3,240 | 5,400 | 2,400 | 9,360 |
| Regular logs | 771 | 736 | 1,157 | 562 | 936 | | 450 | 405 | 675 | 281 | 1,170 |
| Yew | 1,543 | 1,473 | 2,314 | 1,132 | 1,872 | | 900 | 810 | 1,350 | 570 | 2,340 |
| Frostwood | 1,920 | 1,833 | 2,880 | 1,420 | 2,330 | | 1,120 | 1,008 | 1,680 | 720 | 2,912 |
| Ironwood | 2,263 | 2,160 | 3,394 | 1,650 | 2,746 | | 1,320 | 1,188 | 1,980 | 825 | 3,432 |
| Starwood | 5,112 | 4,891 | 7,669 | 3,673 | 6,188 | | 2,880 | 2,592 | 4,320 | 1,800 | 7,488 |

The largest per-hour ratio of any type over the Consignment of the same tier is **1.50x** (Rush), on both ladders, at
every tier (the full tables are in the scratchpad output; the rows above are a sample). Rush is 15 percent of offers,
about 2-3 a day per guild at 4 offers every 6 hours, so it cannot be chained. Standing an hour equals gold an hour
throughout, so the same bound holds for standing.

### 6.3 Against today's best def

The same yield assumptions applied to today's defs (no cooldown, re-accept at once):

| Def | Units | Gold | Standing | Minutes a fill | Fills/h | Gold/h | Standing/h |
|---|---|---|---|---|---|---|---|
| Iron Bulk Order (`:419`) | 250 Iron | 350 | 600 | 30 | 2.0 | 700 | 1,200 |
| Timber Bulk Order (`:2010`) | 250 Boards | 350 | 600 | 22 | 2.8 | 969 | 1,662 |
| Platinum Consignment (`:699`) | 10 Platinum | 500 | 800 | 12 | 4.8 | 2,400 | 3,840 |
| Verite Haul (`:599`) | 8 Verite | 2,500 | 1,000 | 9 | 6.7 | 16,667 | 6,667 |
| Valorite Delivery (`:615`) | 6 Valorite | 4,000 | 1,500 | 9 | 6.7 | 26,667 | 10,000 |
| Valorite Cache (`:654`) | 20 Valorite | 10,000 | 6,000 | 18 | 3.3 | 32,727 | 19,636 |
| Celestial Tribute (`:811`) | 3 Celestial | 5,000 | 5,000 | 11 | 5.5 | 27,273 | 27,273 |
| Starwood Consignment (`:2356`) | 2 Starwood | 8,000 | 4,000 | 10 | 6.1 | 48,980 | 24,490 |
| Diamond Reserve (`:904`), diamonds from the jeweler at 200 | 3 Diamond | 25,000 | 8,000 | a walk | 6 an hour (20 in stock, then doubling) | about 150,000 | about 48,000 |

So today a new member's honest best is about 700-1,000 gold and 1,200-1,700 standing an hour (the two bulk orders), and
the proposed Iron and regular-log Consignments land there (1,029 / 771 gold, the same in standing). Today's top defs pay
27,000 to 49,000 gold an hour when the player knows a bank, because the fixed amounts are tiny (2 to 8 units) and nothing
stops re-accepting; the proposal's top is 6,171 (Celestial) and 5,112 (Starwood), at 1.5x under a Rush. The Diamond
Reserve loop goes away with the stock gems. Nothing in the new table beats today's Platinum Consignment per hour by more
than 2.6x, and that def is the one F-38 called underpaid.

**Standing to rank, at the proposed rates:** Legendary (150,000) is about 45 hours of contract work spread over the ladder
(1,000 an hour at the bottom, 6,000 at the top), against about 6 hours of Celestial Tribute today.

## 7. Named rotations

Of the 62 defs, 47 ask for one material and 15 for a list (section 1.2). Proposal:

- **Keep as weekly specials, re-priced by the formula with a x2 Tribute multiplier, once per character per 7 days:**
  Grand Forge Tribute (`:670-692`) and Grand Forest Tribute (`:2199-2219`). Priced by the formula their lists come to
  100x2 + 50x6 + 30x10 + 20x17 + 10x24 + 5x36 = 1,560 gold, x2 = 3,120, and 100x1 + 50x12 + 20x18 + 8x24 + 5x32 = 1,412,
  x2 = 2,824 (standing the same). Their standing gate (80,000) and skill gate stay. Both lists stop at Valorite and
  Frostwood; the build should add a post-Valorite and an extended-wood line to each (say 2 Celestial, 2 Starwood) so the
  "full spectrum" the titles promise is true on this shard.
- **Keep as a weekly rotation ("this week's commission"), one Miners' and one Foresters' list active at a time, priced
  by the formula x1.1:** Forge Resupply (`:453`), Deep Veins Run (`:523`), Mixed Mid-Tier Metals (`:577`), Rare Metals
  Commission (`:631`), Mixed Stone Commission (`:997`); Mixed Timber Commission (`:2089`), Quality Timber Cache (`:2126`),
  Rare Timber Commission (`:2177`), Exotic Timber Collection (`:2372`). The rotation gives the ledger a handcrafted line
  without a list to farm.
- **Keep as is (cross-guild, Rangers' flavour):** Rangers' Field Lumber (`:2223-2240`).
- **Retire:** the 47 single-material defs, the three stock-gem defs and Diamond Reserve (rolls replace them all). Keys
  stay registered as hidden for one version so an active entry can still be turned in, then go.

## 8. Where it lives

**Recommendation: P48's contract engine (League batch 2), with the Miners' and Foresters' ledgers as its first guild
source.** Reasons:

1. **A rolled contract is an instance, and today's system has none.** `WorkOrderEntry` (`:260-313`) stores a def key;
   amount, material, type, deadline and place would all be new fields and a new version. cc-P47 3.2's `ContractInstance`
   (Guid, def or inline data, state, created, expires) and `ContractEntry` (progress per requirement, generalising
   `TamingProgress`) are exactly that shape, and Smith commissions already use the inline-data shape
   (`ClusterFSmithCommissions.cs:34-104`, P47 3.1).
2. **Rush needs expiry; nothing in the ledger expires** (`AcceptedAt` is display only, P47 3.1). Batch 2 lists expiry
   and abandon as engine features (`notes\cc-P47-league-research.md:737`).
3. **Survey needs gather-after-accept progress in a region**; batch 2 lists gather-after-accept through the `Give`
   overrides (`:736`), which is the hook `C\ClusterFLumberjackingExtension.cs:59` and `CompactOreSatchelRoutingHook.cs:67`
   already provide (cc-P54 `:116-117`).
4. **F-37 and F-20 already point the same way.** Commissions move onto the engine; the guild ledgers become "one more
   source on it" (P47 3.1). F-20's "work orders, no deeds" is about deeds, and holds either way: the Compact Liaison and
   Cedric keep issuing them.
5. **Doing it in the ledger first means doing it twice**: a v2 `WorkOrderEntry` with inline rolled data, expiry and
   progress is the engine's instance under another name, and the fold-in would then migrate it.

Cost: batch 2 is not built (feature-queue `:102` still lists it; cc-P48 delivered batch 1 only). F-38's build therefore
sits **after League batch 2a (engine and payout)** and can be its first non-League source, which also gives 2a a real
customer. **Fallback if Chase wants F-38 before the engine:** `WorkOrderEntry` v2 (rolled requirement list, type,
expiresAt, depot, progress) inside today's system, with the 4-offer roll stored on `CharacterGuildData`; Survey reduced to
"report a new vein or grove of X" (no region) so it needs no gather tracking; written so the fold-in is a data move.
Decision 8.

## Decisions for Chase

1. **The pay dial.** The curve tops out at about 6,000 gold and 6,000 standing an hour (Celestial, Starwood) and starts
   at about 1,000 (iron, regular logs). Keep, or scale every value by one factor (say x0.75 or x1.5)?
2. **One number, three payouts:** standing = gold, tokens = standing / 25. Yes, or keep standing above gold at the
   bottom of the ladder as today (a second curve)?
3. **Stock gems out.** The nine jeweler gems leave the contracts; Rare finds ask for the six mined ML gems. Yes?
4. **Wood harvest re-gate** to `ClusterFWoodTiers` with the cc-P57 shape (requirement = tier, window +-40), so
   Lumberjacking climbs to 200 and wood gates above 140 are reachable. A GM lumberjack loses Ghostwood to Starwood trees
   until they climb. Yes (recommended), no, or a softer ladder for the trees than for the crafts?
5. **Rush on expiry** downgrades to plain pay (recommended), or expires outright (frees the slot, material kept)?
6. **Haul depots:** a Depot Clerk in Minoc and Britain (Compact) and Yew and Skara Brae (Foresters), deliver-only. Those
   towns, others, or a single depot per guild for the first build?
7. **Survey's check:** region-tagged gather-after-accept (needs the engine), or the simpler "report a new vein or grove of
   X at the Archivist or Cedric" (works in either home)?
8. **Home:** after League batch 2a on the engine (recommended), or now as `WorkOrderEntry` v2 in the ledger?
9. **Dawnstone and Rootwood stay out of the rolls** (starter materials, dungeon-only). Yes?
10. **Offers:** 4 per guild per character, 6-hour life, decline does not reroll, active cap stays 3. Yes?
11. **Turn-in checks:** three gain checks per turn-in (one per third of the amount) in the material's -20/+20 window, or
    one as a BOD?
12. **Discovery gate stays:** a colored material rolls only once Reported in the player's ledger (today's rule). Yes?
13. **Granite:** value 2x the metal's ingot, a quarter of the roll, offered only with the stone-mining book. Yes, or
    granite out of the rolls (stone stays a named rotation)?

## Draft build prompt (for the overseer to number once Chase answers)

```
# CC task P???: Rolled Mining and Lumberjacking contracts (F-38, build 1)

**Model:** Fable

**Touches:** server (C\ClusterFWorkOrderSystem.cs or the League contract engine per Decision 8, C\GuildContractLedgerGump.cs,
C\ClusterFLumberjackingExtension.cs if Decision 4 is yes, new depot NPC and seeder entries if Decision 6 is yes,
C\ClusterFAccountData.cs or CharacterGuildData for the offers and instances, tests), docs-only elsewhere.

**Summary:** Replace the 47 single-material Miners' and Foresters' defs with contracts rolled from the player's tier,
five types, one reward formula, gates on the shared ladders and turn-in gain checks, per notes\cc-P235-work-order-numbers-pass.md
and Chase's answers to its 13 decisions.

Read first: notes\cc-P235-work-order-numbers-pass.md (all of it; the tables are the spec); docs\feature-queue.md F-38, F-20,
F-36, F-37; notes\cc-P47-league-research.md 3.1-3.2; notes\cc-P48-league-batch-1.md; notes\cc-P57-batch-6.md Part C;
notes\cc-P13-grove-tracking.md; C\ClusterFMetalTiers.cs; C\ClusterFWoodTiers.cs; C\PackMule.cs.

**Ours.**

## Do

1. **Tier values and rolls as data:** one table per ladder (P235 sections 3 and 5) in a static class beside
   ClusterFMetalTiers, read by everything below; a fact asserts value per unit, gold per mid contract and gold per hour
   rise strictly down each ladder (P235 6.1), and that no type exceeds 1.5x the Consignment per hour (6.2).
2. **Instances and offers:** 4 rolled offers per guild per character, 6-hour life, material picked by P235 section 5's
   weights from the player's eligible, Reported materials; type frequencies as 5; accepted offers become instances with
   amount, material, type, multiplier, expiry, depot.
3. **The five types:** Consignment, Raw sample, Rush (60-minute deadline, downgrade on expiry per Decision 5), Survey
   (per Decision 7), Haul (mule present, goods from the mule's pack, at a depot per Decision 6, amount capped to the pack),
   Rare finds (ML gems and ML extras only).
4. **Payout:** gold = amount x value x multiplier; standing the same; tokens / 25; through the ledger's existing
   AddReputation, AddCurrency and gold drop (GuildContractLedgerGump.cs:537-541), or the engine's GuildPayout.
5. **Turn-in gain checks:** per Decision 11, in the material's harvest requirement -20/+20 window; a fact shows a check
   runs on turn-in and none below or above the window.
6. **Wood harvest re-gate (Decision 4):** extended trees need their ClusterFWoodTiers value with a +-40 window, the
   cc-P57 Part C pattern; vein weights and permanence unchanged; a fact per wood.
7. **Named rotations (P235 section 7):** the two Grand Tributes as weekly specials at x2 with a post-Valorite and an
   extended-wood line added; the nine mixed lists as a weekly rotation at x1.1; Rangers' Field Lumber unchanged; the 47
   single-material defs, three stock-gem defs and Diamond Reserve retired (hidden one version, then removed).
8. **Ledger gump:** offers tab with type, material, amount, pay and (for Rush) time left; active tab shows progress for
   Survey and Haul.
9. **Wiki:** one page per guild describing the types, the ladder and the windows; no numbers the formula can change.

## Done means

- Tests red then green through docker\uo\build.sh with the image tag the Golem hand-off gives; every number in a fact
  comes from the data class, not a literal.
- Notes: headlines, what changed (file:line), the facts, the red run, a client-test queue of 6-8 rows (one per type,
  one for the depot, one for the re-gate).
- Patch notes: one ### Changed line (players: contracts are now rolled from your skill, five kinds, pay that rises with
  the material) and one ### Staff line (the retired defs and the data class) per the CHANGELOG comment; bump VERSION.
- Commit preflight: Commit-ShardWork.ps1 -DryRun result table in the notes.
- Finishing: do not commit; last line of the notes P??? DONE; end the final chat message with P??? DONE.
```

## Patch notes and preflight

- `CHANGELOG.md`: new section `2026.10.20.14` with one `### Staff` line (the top section `2026.10.20.13` was already
  committed by P233, so a new version was started); `VERSION` bumped to `2026.10.20.14`.
- `Commit-ShardWork.ps1 -DryRun` result table:

  Run 2026-10-20 from the Bronze desk. The script reads the three main checkouts (code, docs, scripts), not this
  Golem's worktrees, so "code clean" is the main checkout; this branch's three changed files (`CHANGELOG.md`, `VERSION`,
  this note) are committed by the Golem after P235 DONE. The three docs files it lists are the play-test importer's and
  the overnight bot's output, committed with each prompt.

  | Repo | Result |
  |---|---|
  | code | clean |
  | docs | dry run (3 pending: `testing/SUMMARY.md`, `testing/bot-runs/2026-10-19-0130/transcripts/P140-1-run1.txt`, `testing/play-tests.json`) |
  | scripts | clean |

  Prompts with a finished note: none for P235 (it lists cc-P180, cc-P181 and cc-P185 as not ending in DONE or STOPPED,
  which is not this task).

P235 DONE
