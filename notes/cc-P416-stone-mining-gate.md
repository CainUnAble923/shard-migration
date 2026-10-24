# cc-P416: stone mining is learned before stone work; ore contracts become mining quotas; gold for missing vouchers

## In plain words

- **Stone Contracts are hidden until a miner learns stone mining.** In the Compact's Work Orders ledger (and the
  Dispatch Ledger), a miner who has not read Mining For Quality Stone sees no Stone Contracts. Instead, a gold line at
  the bottom says where to get the book. Garrett's dashboard has a new **Learn Stone Mining** button that sells the
  Compact's copy for 50 Mining Vouchers from Journeyman rank. Reading it still needs 100 Mining, and the button goes
  away once the miner has learned stone mining.
- **The two raw-ore contracts are now "mine this much" quotas.** They are **Mine Iron Ore** (100 iron ore, the old
  Raw Ore Sample's pay) and **Mine Dull Copper Ore** (50 dull copper ore, Journeyman, 65 Mining; it replaces the
  150-iron Ore Refinement Run). Only ore mined after accepting counts, the ledger shows the count, and nothing is taken
  at turn-in.
- **A miner short of vouchers can still restore their Jacob's Pickaxe.** The Restoration page offers to cover just the
  missing vouchers at 100 gold each. It shows the voucher price and the gold price before the miner confirms.
- **For you:** try it on the test shard. A Compact member without stone mining should see no Stone Contracts and the
  gold hint. Read the book (or set `StoneMining` true) and they appear. Take Mine Iron Ore and mine 100 iron. Restore a
  pickaxe with too few vouchers. The voucher rate (100 gold), the book's price (50V) and its rank (5,000 standing) are
  server settings, if you want them different.

## What changed (ShatteredLegacy, branch `golem/Iron/P416`)

| File | Change |
|---|---|
| `server/customizations/ClusterFWorkOrderSystem.cs` | `WorkOrderDef.NeedsStoneMining` (:138) and the gate in `IsEligible` (:191); `IneligibleReason` returns the hint. `WorkOrderMiningRequirement` (:76). `QuotaMet` (:281), `UsesLegacyTurnIn` (:295), `ConsumeRequirements(pm, entry)` (:316). Version 3 of `WorkOrderEntry` adds `MinedProgress` (:362) and `FromBeforeQuotas` (:368); write at :415. `OnOreMined` (:582), `StoneMiningHint` / `StoneMiningHintFor` (:610, :615). The two quota definitions (:648, :759). New `WorkOrderType.MiningQuota`, label "Mining Quota". |
| `server/customizations/GuildContractLedgerGump.cs` | The hint in the Available tab's footer (:141). No locked card for a Stone Contract either (`IsDiscoveryPending`, :240). Quota progress line (:306). Old-contract note (:338). Quota prompts for accepting, the Active tab and turn-in (:359, :536, :580). Turn-in passes the entry to `ConsumeRequirements`. |
| `server/customizations/CompactOreSatchelRoutingHook.cs` | `Mining.Give` calls `OnOreMined` (:150) after the yield bonuses and before the satchel routing, at the same hand-over where the Logbook keeps its tally. |
| `server/customizations/MinersCompactLiaisonGump.cs` | Settings `GoldPerMissingVoucher`, `StoneBookStanding`, `StoneBookVouchers` (:108-118). Dashboard button (:335). `DrawStoneMiningBook` (:688), `TryBuyStoneMiningBook` (:727). The Restoration page's "Short N vouchers?" action. `DrawRestoreWithGold` (:775), `GetRestoreCostCoveringVouchers` (:819). Buttons 41, 65, 81-85 and 94; `HandleRestoration(..., coverMissingVouchers)` (:1030). |
| `server/tests/Services/StoneMiningGateVerification.cs` (new) | Six facts (below). |
| `CHANGELOG.md`, `VERSION` | 2026.10.24.7. |

In shard-migration, `notes/wiki-drafts/gathering-guilds.md` covers the gate, the Compact's copy, quotas and the gold
restore.

### Facts checked (prompt's "facts already found")

- Pinned `Items/Skill Items/Specialized/StoneMiningBook.cs`. It refuses below 100.0 base Mining (:26), sets
  `pm.StoneMining = true` (:36), then deletes itself (:39). Confirmed.
- Pinned `Mobiles/Vendors/SBInfo/SBStoneCrafter.cs:31` sells it for 10,625 gold, and :41 buys it back at 5,000.
  Confirmed.
- `RegisterMinersCompactStoneOrders` (`ClusterFWorkOrderSystem.cs`, now about :1100) has **10** Stone Contracts. I
  counted them; fact 1 asserts 10. None had a stone-mining gate before. Their Mining gates are 30 to 90, but stone
  mining itself needs 100.0 to learn. In practice the gate now asks for GM Mining; their own gates are left as they were.
- The work orders and the dashboard came in with the content migration (`9f5dc21`). Since then only shard-work commits
  and P414 have touched the file. The restoration prices are F-16's (comments at `MinersCompactLiaisonGump.cs:41-71`).

## Part 1: the gate

- `IsEligible` refuses a Stone Contract to a character without `StoneMining`. The ledger lists only eligible orders,
  plus discovery-pending locked cards, and `IsDiscoveryPending` now refuses them too. So an unlearned miner sees none,
  not even a locked card. Accept re-checks with the same lists, so a stale page cannot accept one.
- **The hint** is one line in the Available tab's footer, between Back and X, on every page of the list:
  "Stone Contracts open once you learn stone mining: read Mining For Quality Stone (needs 100 Mining). The Stone Crafter
  sells it, and so does the Compact from Journeyman rank." The rank name comes from the setting.
- **Where the list is shown.** The Liaison's Work Orders button and the Compact Dispatch Ledger
  (`CompactDispatchLedger.OnDoubleClick`) both open `GuildContractLedgerGump`, so one change covers both; fact 1
  opens the Dispatch Ledger. The Member Dashboard has no contract list of its own, so its hint is the new
  **Learn Stone Mining** button. Once learned, that button becomes the line "Stone mining: learned".
- **Held Stone Contracts stay finishable.** Turn-in (`GuildContractLedgerGump.TurnIn`) never checks eligibility, only
  the requirements, so a contract taken before the gate can still be turned in (fact 2).

## Part 2: the Compact sells the book

- **Rank: Journeyman** (5,000 standing), the default. Reading the book needs GM Mining anyway, so a rank gate only
  says the Compact keeps its copy for proven members. A higher rank would add nothing a 100-Mining miner lacks.
- **Price: 50 Mining Vouchers**, vouchers only. Settings: `clusterf.compact.stoneBookVouchers` and
  `clusterf.compact.stoneBookStanding`. The Compact's other voucher items:

| Item | Price | Rank |
|---|---|---|
| Kit item / satchel / boots replacement | 5V | member |
| Reinforced Ore Satchel (upgrade) | 25V + 5,000gp + ingots | Apprentice |
| T2 Jacob's Pickaxe upgrade | 50V + 25,000gp + ingots | |
| **Mining For Quality Stone (new)** | **50V** | **Journeyman** |
| Surveyor's Ore Satchel (upgrade) | 75V + 20,000gp + ingots | Surveyor |
| Surveyor's Climbing Boots | 75V + 20,000gp + ingots | Surveyor |
| T3 / T4 / T5 pickaxe upgrades | 200V / 350V / 500V + gold and ingots | |

  The book sits between the Apprentice and the Surveyor satchel upgrades, at roughly three Journeyman-tier contracts
  (14 to 18V each). The Stone Crafter's copy stays the gold route at 10,625. At the contracts' 47 gold per voucher, 50V
  is worth about 2,350 gold of contract pay, so the Compact's copy is the member's discount.
- **What the page shows before buying:** what the book does, the rank line and the voucher line (each shown met or not
  met), and a note on the 100 Mining rule: "Reading it needs 100.0 Mining (you have 99.0): buy now, read it at 100."
  The skill is a note, not a block. The item is pinned's own `StoneMiningBook`, so the reading rule is pinned's.
- **Refusals:** a non-member; anyone who has already learned stone mining; below the rank, with the rank and standing
  named; and too few vouchers (`GuildResources.TryPay`'s message). The dashboard does not offer the book to a miner who
  has learned it.

## Part 3: anywhere else stone is offered

I searched every `.cs` under `server/customizations` for `Granite`, `granite`, `StoneMining`, "stone mining" and
"Stone Contract", plus the docker wiki text. No other path offers stone work to a miner:

- The mining guild's apprentice task is "Mining 50.0, or 20 Iron Ore" (`ClusterFGuildSystem.cs:186-193`). It has no
  stone.
- The League requisitions (`Requisitions/RequisitionTable.cs:280-283`) ask for armour, jewellery and weapon
  properties. They have no granite. The leads do not ask for granite either.
- The Liaison's "What We Mine" page lists ores only. The Survey Archivist and the Logbook are about ore veins.
- Granite appears only as a material or a filter: Masonry and Carpentry recipes (`ClusterFMiningExtension.cs:250-279`,
  `CarpentryCraftRegistrations.cs:62`, `ExodusCraftRegistrations.cs:73`), the satchels' and the mule's accepted items,
  the harvest tables, and `ResourceInfo.cs`. None of these offers or asks for stone, so none needs a gate.
- `IronBeetle.cs:314-333` already checks `pm.StoneMining` and 100 Mining before a beetle mines stone.
- The published wiki page `docker/wiki/content/pages/uo/guilds/miners_compact.txt:74` already says what this prompt
  builds ("**Stone Contracts** show only once you have learned stone mining, and the Compact sells its own copy of the
  stone mining book"). Before
  this prompt it was ahead of the code; now it matches.

## Part 6: ore contracts become mining quotas

- **How it counts.** A new requirement, `WorkOrderMiningRequirement`, is met by ore of exactly that type mined since
  the contract was taken. The count lives on the contract (`WorkOrderEntry.MinedProgress`, entry version 3) and is
  raised in `Mining.Give` (`CompactOreSatchelRoutingHook.cs:150`) as the harvest hands the ore over. That is the hook
  where the Prospector's Logbook keeps its tally.
- **Deviation:** the prompt says to count "from the same harvest tally the Prospector's Logbook keeps". That tally,
  `OreDiscoveryEntry.TotalMined`, leaves iron out on purpose (`CompactOreSatchelRoutingHook.cs` header and
  `_oreDiscoveryKeys`), so it cannot count an iron quota. Adding iron to it would make iron a "discovery" in the
  Logbook and in Ore Bingo. So the quota keeps its own count, at the same moment and from the same hand-over.
- **What counts and what does not.** The count includes the yield bonuses (Deepdelver's and Worldbreaker's +1, and
  Bountiful) and ore placed at the feet when the pack is full. An unreported extended ore that "crumbles" into iron
  counts as the iron the miner received. Ore mined before accepting never counts, because the contract did not exist
  yet. Ore bought, traded, picked up, or carried in the pack or bank never counts, because only `Mining.Give` adds to
  the count. Unverified: whether an Iron Beetle's mining goes through `Mining.Give`. I did not test it.
- **One amount per metal.** The iron quota keeps "Raw Ore Sample"'s key, its 100 ore and its pay (75 standing, 4V,
  60gp). Titled **Mine Iron Ore**, it has no gate.
- **The 150-ore contract is now Dull Copper.** "Ore Refinement Run" (key `mining.ore_refinement_s`, Journeyman, 150
  iron ore) becomes **Mine Dull Copper Ore**: 50 dull copper ore, with the same pay (350 standing, 16V, 400gp).
  - Why Dull Copper: it is the first colored ore and the next metal a Journeyman reaches. The Apprentice tier already
    asks for its ingots.
  - Its Mining gate goes from 50 to **65.0**, because Dull Copper cannot be mined below 65 (`patches/Mining.cs:116-123`,
    `HarvestResource` required skill 65.0).
  - It takes the DullCopper discovery gate like the other Dull Copper contracts.
  - Why 50: a Dull Copper vein yields its ore about half the time (fallback 0.5, `patches/Mining.cs:193`). So 50 Dull
    Copper ore is roughly the digging of the old 150 iron, plus finding the vein.
  - Shadow Iron (70) and Copper (75) would need higher gates than the Journeyman tier's 50 to 55.
- **Titles and descriptions say "mine",** and the ledger lists the line as "Mine 100 Iron Ore". The Active tab shows
  "Mine Iron Ore since taken: 60/100". The prompt underneath says "Mine the rest. Ore you carry or buy does not count."
  Accepting says "Ore you mine from now counts toward it; there is nothing to carry back."
- **Contracts already held finish either way.** An entry saved before this change (version 2 or older) is marked
  `FromBeforeQuotas`, and the mark survives later saves.
  - Such a contract is finished by mining the new quota, or by turning in what it asked for when it was taken
    (`WorkOrderDef.LegacyTurnIn`: 100 iron ore for Mine Iron Ore, 150 iron ore for Ore Refinement Run). The ore is
    taken only on that path.
  - The Active tab says "Taken before quotas: turning in 150 Iron Ore also finishes it."
  - A held Ore Refinement Run with no Dull Copper discovery can still be finished, because turn-in checks requirements,
    not eligibility.
- Not changed, as the prompt says: Foresters' contracts, ingot contracts and Stone Contracts stay turn-ins. P417
  designs the rest.

## Part 7: gold in place of missing vouchers

- **The rate:** `clusterf.compact.goldPerMissingVoucher`, **100 gold** per missing voucher. Here is the math.
  - Across the Compact's 39 contracts I counted from the definitions (comments stripped), the pay is 125,385 gold and
    2,656 vouchers. That is 47.2 gold beside each voucher; the median contract pays 33, with a range of 11.7 to 83.3.
  - The dashboard's own prices put gold beside vouchers at 100 (T1 restore) to 600 (T5 restore) per voucher: T2 250,
    T3 250, T4 429, satchels 200 to 400.
  - 100 is about twice what a contract pays beside a voucher, so working a contract always stays the better deal. It
    is still cheap enough to get out of the pickle: a T1 restore with no voucher costs 200 gold instead of 100; a T2
    restore with none costs 1,400 instead of 1,000; a T5 restore with none costs 70,000 instead of 60,000.
- **What it changes:** only the missing vouchers. The vouchers the member holds are used up to the price, the ingots
  are the same, and the base gold is the same. `GetRestoreCostCoveringVouchers(tier, held)` returns the price.
- **The flow:**
  1. The Restoration page shows the usual price list.
  2. When the member is short, it also shows "Short 3 vouchers? Pay 300 gold instead".
  3. That opens a page showing "With vouchers: 4V + 100 Iron + 15 DC + 1,000gp" and "With gold: 3 missing vouchers x
     100 = 300 gold more", then the gold price's lines, each met or not met, then "Restore with 1,300 gold".
- **Not enough gold** refuses and names the whole shortfall: "Restoring Jacob's Reinforced Pickaxe with gold for the
  missing vouchers costs 1,400 gold: the 1,000 base plus 4 missing vouchers x 100 = 400. You have 1,000 in your pack
  and bank: 400 short." Nothing is taken.
- A member with enough vouchers is never offered this. The page says to use the Restoration page, and the plain
  restore is unchanged.

## Tests (Parts 4 and 5)

`docker/uo/build.sh -t sl-modernuo:cc-P416`, under the `docker-build` lock (taken, then released). 13.6 GB was free
when I took the lock, and I dropped the VM's page cache before the green build.

New facts, `StoneMiningGateVerification`:

1. An unlearned Miner sees no Stone Contract in the Available tab at any scroll position, and no locked card. All 10
   are ineligible, each with the hint as its reason, while the other contracts are still listed. The hint names the
   book and Journeyman. The Dispatch Ledger opens the same list. After reading the pinned book (100.0 Mining), Granite
   Haul and Valorite Stone Tribute appear, a discovered-but-unreported vein's stone card appears locked, and the hint
   is gone.
2. A held Granite Haul turns in without stone mining: the granite is taken and the pay given.
3. The book page shows "Rank: Journeyman (need 1 more Standing)", "Mining Vouchers 60 / 50" and the 99.0 Mining note.
   Below the rank it is refused and nothing is taken. At the rank it is sold for 50V as the pinned book. At 99 Mining
   it cannot be read yet; at 100 it is learned. Then the dashboard shows "Stone mining: learned" instead of the button,
   and buying is refused.
4. The quotas are the two keys, one ore type each, titled "Mine ...", with the pay and gates above. Ore mined before
   accepting does not count. 400 iron ore in the pack and bank does not count, and shadow iron does not count toward
   iron. 60, then 40 iron mined through `Mining.Give` completes it. Turn-in takes no ore and pays 4V. The Dull Copper
   quota counts dull copper only.
5. A version 2 entry (`FromBeforeQuotas`) finishes by turning in 100 iron ore (taken). Another finishes by mining,
   with nothing taken. The flag and the count survive a version 3 save. A new contract is not from before quotas, so
   500 carried ore does not finish it.
6. Restoration with 6 vouchers works as today (4V and 1,000gp taken). With 1 voucher, the plain restore refuses; the
   gold page shows both prices; pressing it takes 1V + 1,300gp + the ingots and gives the pickaxe. With 0 vouchers and
   1,000 gold it refuses with the exact shortfall line above, and nothing is taken.

**Red first.** I ran a mutant with each new rule switched off:

- no stone gate, in eligibility or locked cards
- no hint
- the ore never counted
- no old turn-in
- the dashboard always offering the book
- no rank check on buying
- the gold-restore buttons unhandled

All six facts failed, and no other test did (6 failed, 2,279 passed). Each failed for its own reason:

| Fact | Mutant result |
|---|---|
| 1 | "Granite Haul" listed |
| 2 | Contract eligible without stone mining |
| 3 | Sold below the rank |
| 4 | Mined count 0 instead of 60 |
| 5 | Old turn-in not accepted |
| 6 | No pickaxe after the gold restore |

**Green.** The real code passed. The whole gate: **2,289 tests, 2,285 passed, 0 failed, 4 skipped**, and the image
`sl-modernuo:cc-P416` was built. `CHANGELOG.md` and `VERSION` were edited after the build. They are plain ASCII in
the existing format, and the patch-notes tests parse sample text, not the file.

Existing tests checked for the changes: the serializer tests compare work order entries field by field
(`AccountDataSerializerVerification.cs:424-437`), not as bytes, and the P414 version-1 entry test still reads.

## Deviations and decisions for Chase

- **The quota count is the contract's own, not the Logbook's per-ore tally**, because that tally excludes iron by
  design (Part 6).
- **The 150-ore contract became Dull Copper**: 50 ore, Mining gate raised to 65, DullCopper discovery gate, same pay.
- **Book:** Journeyman (the default), 50V. **Rate:** 100 gold per missing voucher. All three are server settings
  (`clusterf.compact.stoneBookStanding`, `stoneBookVouchers`, `goldPerMissingVoucher`).
- **Stone Contracts keep their own Mining gates of 30 to 90.** Since learning stone mining needs 100.0, those gates no
  longer matter once the stone gate is met. I did not change them.
- **Not tested:** whether an Iron Beetle's ore counts toward a quota.

P416 DONE
