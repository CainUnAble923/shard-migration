# cc-P179: the League design pass (book of books, consolidation, player upgrades)

Stone Golem, 2026-10-20. Research and design only. No code, no docs, no CHANGELOG (no code changed).

## Headlines

- The League is the **League of Extraordinary Citizens** (`ClusterFGuildSystem.cs:823`), run by **Elara Voss, the
  League Registrar** (`LeagueRegistrar.cs:41-42`). It has 17 metal ranks, Iron to Celestial. Rank is stored per
  character (`ClusterFAccountData.cs:664-724`, `CharacterLeagueData` v1). Its currency is **Renown**, a counter per
  account (`ClusterFAccountData.cs:37`). **Nothing spends Renown yet**: `SpendRenown` (`:642`) has no callers. Rank
  reads `LifetimeRenown`, so spending never lowers rank. That makes this pass the first Renown sink.
- Today players get these from the League: the Registrar gump, the Requisitions board, the Compact's Mule errand (needs
  Dull Copper) and a bigger bank (1,000 items +100 per milestone, `ClusterFBankLimit.cs:26-47`). The
  `LeagueMemberPass` item exists, but nothing hands it out.
- **The League book** (proposed name "Citizen's Register"):
  - Guild books are **bound in**. The guild book is deleted and its guild key is recorded.
  - A bound guild can be **taken back out** free, which issues a fresh guild book.
  - The Register is issued at **Dull Copper**. How many guilds it holds grows with each milestone.
  - It shows each guild's P178 action list exactly as the guild book would.
  - The League adds its own cross-guild actions by League rank.
  - **Recommended:** fold F-34's bank-access "Citizen's Requisition Ledger" into it as a page, so the League has one
    book, not two.
- **Consolidation:** eleven candidates are in section 2. Recommended first:
  1. the Guild Ledger page (every currency and standing in one place; read-only; free);
  2. the Field Satchel of the League (one satchel replacing ore, lumber, hunter's and essence);
  3. the Combined Logbook.
- **Upgrades:** today's limits, from pinned:
  - backpack items: 125 (`Server/Items/Container.cs:177`);
  - backpack weight: 550 for a player on ML (`UOContent/Items/Containers/Container.cs:252-262`). The shard already
    replaces 550 with `Mobile.MaxWeight`, with no ceiling (`ClusterFBackpack.cs:33-43`), so carry weight is not
    scarce here.
  - **Recommendation:** sell **backpack item count**, not weight. Use four steps: 125, 150, 175, 200, 250. Gate them
    on milestones and price them in Renown. Weight belongs to Strength and to F-12's Legacy tree, the bank to F-19,
    pack-animal capacity to the mule (F-33), and stat and skill caps are never sold (F-13 guardrail).
- **Deviation:** `D:\UO\ModernUO-pinned` does not exist on this machine. I fetched the pinned commit itself,
  `d4531cd94b739613155225c234900de9f47d2c88` (from `docker\uo\Dockerfile:3`), as a read-only shallow copy into my
  session scratchpad, outside both repos. Every "pinned" citation below is a path in that commit.

## For Chase: decisions (no build until you answer)

Each line gives the overseer-style recommendation first.

1. **League book: bind or store?** Recommend **bind**. The guild book is deleted and its guild key is recorded; you
   can take it back out free. The alternative is to store the actual book item inside the Register.
2. **League book gate:** Recommend that the Register is issued free by the Registrar at **Dull Copper**. Capacity:
   - Dull Copper: 2 guilds;
   - Bronze: 4;
   - Verite: 6;
   - Blaze: 9;
   - Mythril: 12;
   - Celestial: all 18.
3. **Fold F-34's bank-access ledger into the Register** as its "Bank" page. Recommend yes. F-34's per-guild
   upgrades and range tiers stay exactly as designed.
4. **League-only remote actions by League rank.** Recommend:
   - Dull Copper: read-only status of every bound guild;
   - Bronze: open contracts for any bound guild;
   - Verite: turn in several guilds' orders at once (candidate C4);
   - Blaze: remote repair for every bound guild in one pass;
   - Mythril and up: reserved.
5. **Consolidation items first.** Recommend in this order:
   - C1, the Guild Ledger page: free, part of the Register;
   - C2, the League Field Satchel: Bronze, 5,000 Renown plus 50 gold-equivalent per tier merged (see the table);
   - C3, the Combined Logbook: Dull Copper, 500 Renown.
   Later: C4, C5 and C6.
6. **Backpack upgrade.** Recommend four steps, item count only, priced in spendable Renown:
   - 150 at Bronze, 2,000 Renown;
   - 175 at Verite, 6,000;
   - 200 at Blaze, 15,000;
   - 250 at Mythril, 30,000.
   Weight is not sold.
7. **Bank:** Recommend no purchase. F-19 already ties bank size to League milestones. P75's "League Warehouse" is
   dropped, or held until the bank hits its client ceiling in play.
8. **Currency:** Recommend that **Renown** pays for League items and upgrades, with gold as a small second cost.
   Guild currencies pay only for guild-specific parts, such as merging a guild's satchel into C2.
9. **Leaving.** No player can leave a guild or the League today; only staff `[ResetGuild` and the dev reset remove
   membership (`ClusterFGuildSystem.cs:1261-1320`, `ClusterFDevTools.cs:188-216`). Recommend that the Register
   follow membership live:
   - a guild you are no longer in shows greyed out and drops out at the next open;
   - its slot is freed;
   - nothing is refunded.

## 1. The League book ("Citizen's Register")

### What it is

The Register is one blessed book per character, bound to its owner, with small book art: the same art P178 picks for
guild books. It is issued by the Registrar and re-issued like P178's guild books: the old copy is deleted and stops
working, as the Custodian trash bag works.

It holds a list of guild keys, not items. Each bound guild gets a page that renders that guild's P178 remote action
list (action, rank needed, cost) from the same data P178 builds. The Register therefore never has its own copy of a
guild's actions. When P178 adds a tier, the Register shows it with no change.

### Bind (consume) or store?

**Recommend bind.**
- P178 already makes guild books cheap to re-issue, with the old one deleted. A stored item adds nothing a guild key
  does not already hold.
- A stored book is an item inside an item. It counts toward the backpack's 125 (nested items count,
  `Server/Items/Container.cs:245-246`), and the Register would need container rules, `CheckHold` and serialization of
  its children.
- A key list is one small set on `CharacterLeagueData`: a version bump from 1 to 2, a read branch for v1 that gives
  an empty set, and a round-trip test with a non-empty set.
- Binding is what gives the player the space back. That is the point of a book of books.

### Taking a guild back out

You can, free, and the guild book comes back as a fresh copy. There is no reason to trap a player, and a player at the
capacity limit needs a way to swap guilds.

### League rank gate

Chase's rule is "what you can do remotely should expand as players rank up". There are two axes, kept separate:
- **Guild rank** unlocks each guild's own actions (P178's per-rank list). The Register never lets you do more than
  your guild rank allows.
- **League rank** sets how many guilds the Register holds, and which **League actions** appear: the cross-guild ones
  no single guild book can do. Decision 4 has the proposed ladder.

### Leaving a guild or the League

- **Guild:** the page reads membership live through `IsJoined`, so a guild you have left shows greyed out with "You
  are no longer a member" and is dropped at the next open. Its slot is freed. No guild book is issued, since you are
  not a member.
- **League:** no exit exists today. If one is built, the Register stops working and every bound guild is re-issued as
  a guild book into the bank. Nothing is lost.
- **Staff resets** (`[ResetGuild`, the dev League reset) clear the key set with the rest. That is one line in each
  reset, and a test.

### Menu sketch on P177's template

P177 has not run yet, so this follows P177's brief: a header with crest and name, a rank line, a left menu, the
requirement colors from P169 and paging. P178 converts it once Chase approves P177.

```
+--------------------------------------------------------------+
| [League crest]  CITIZEN'S REGISTER         Bronze Citizen    |
|                 Renown 3,240   Guilds bound 3 / 4            |
+---------------+----------------------------------------------+
| > Overview    |  SOCIETY OF SMITHS        Journeyman         |
|   Smiths      |  ---------------------------------------     |
|   Miners      |  [o] Repair guild items      (Apprentice)    |
|   Foresters   |      Hammer of Hephaestus 140/150   [Repair] |
|   ---------   |  [x] Remote BOD turn-in      (Master)  grey  |
|   Ledger (C1) |                                              |
|   Bank (F-34) |  LEAGUE ACTIONS                              |
|   Bind book   |  [o] Open contracts, any bound guild (Bronze)|
|   Unbind      |  [x] Combined turn-in            (Verite) red|
+---------------+----------------------------------------------+
|  < Prev                                          Next >      |
+--------------------------------------------------------------+
```

- **Overview** lists every bound guild with rank, standing and currency on one line each. This is the C1 Ledger.
- **Bind book** asks for a target: the player targets a guild book in the backpack.
- **Unbind** lists the bound guilds and issues the chosen book back.

## 2. Consolidation items and processes

What a five-guild player (Mining, Smiths, Foresters, Rangers, Artificers) carries today:
- four satchels, all graphic 0xA272 with separate code: ore, lumber, hunter's, essence;
- two logbooks, both 0x1C11 and display-only: the Prospector's (`ProspectorsLogbook.cs:24`) and the Forester's
  (`ForestersLogbook.cs:24`);
- two order items: the Compact Dispatch Ledger (`CompactDispatchLedger.cs:29`) and the Smith Guild Book
  (`SmithGuildBook.cs:29`);
- three or four tools: the Hammer, Jacob's Pickaxe, the Artificers' Toolkit and the Outrider's Crook;
- the Smith Salvage Bag;
- duplicate stock skill kits, because duplicates are removed only within one guild's kit
  (`ClusterFGuildStarterPath.cs:290`);
- BOD deeds from up to 8 givers.

Guild currencies are counters, not items (`ClusterFAccountData.cs:753`), so they take no bag space.

| # | Candidate | Replaces | OSI or ours | Rank gate | Cost (proposal) |
|---|---|---|---|---|---|
| C1 | **Guild Ledger** (a Register page): every guild's rank, standing, currency and next promotion step on one page | opening each dashboard, `[GuildStanding` (staff only) | ours | Dull Copper (comes with the Register) | free |
| C2 | **League Field Satchel**: one satchel with one compartment per merged guild satchel. Each compartment keeps that satchel's own filter, reduction and stone cap. | the ore, lumber, hunter's and essence satchels | ours | Bronze | 5,000 Renown, plus a merge fee per satchel: 50 of that guild's currency |
| C3 | **Combined Logbook**: Prospector's and Forester's in one book, ready for the hide and cloth logs P178 lists | 2 logbooks, and every future one | ours (large BOD-book style, which Chase keeps for log books) | Dull Copper | 500 Renown |
| C4 | **Combined order turn-in**: one League action turns in every completed contract and work order in the pack, for every bound guild | walking to 5 liaisons, or opening 5 ledgers | ours | Verite | free (each guild pays as normal) |
| C5 | **League BOD book**: one book holding BODs of all 8 crafts, filtered by craft | pinned `BulkOrderBook` (`UOContent/Engines/Bulk Orders/Books/BulkOrderBook.cs:14`, 500 entries at `:138`, already extended to 8 crafts by `BulkOrderBooks.cs:18`) per craft, plus the Smith Guild Book | OSI book, our filter | Bronze | 2,500 Renown |
| C6 | **Guild Toolroll**: a blessed roll that holds one tool per guild (Hammer, Jacob's Pickaxe, Toolkit, Crook). Each tool still works from the roll. | 3-4 loose tools | ours (in the spirit of the OSI `KeyRing`, `UOContent/Items/Misc/KeyRing.cs:10`, 20 keys) | Verite | 7,500 Renown |
| C7 | **Retire the Dispatch Ledger**: the `[guild` Contracts button already does its job (`ClusterFGuildSystem.cs:1005-1018`) | Compact Dispatch Ledger | ours | n/a | n/a. A clean-up for P178, not a League item. |
| C8 | **Stock kit de-duplication**: when joining a guild, do not hand out a stock tool the character already has from another guild's kit | duplicate stock kits | ours | n/a | n/a. A starter-path fix. |
| C9 | **Salvage and trash in one**: the Smith Salvage Bag and the Custodian Trash Bag become two modes of one bag | 2 bags | ours | Bronze | 1,000 Renown |
| C10 | **League Repair**: one pass repairs every bound guild's special items, each at its guild's P178 price | one repair per book | ours | Blaze | free (normal repair prices) |
| C11 | **Commodity compression**: OSI commodity deeds (`UOContent/Items/Deeds/CommodityDeed.cs`) sold by the Registrar, to turn a stack into one deed for the bank | bank item count | OSI | Copper | gold, at vendor price |

Notes:
- **C2 risk:** every satchel overrides `UpdateTotal` and `CheckHold` its own way, and none shares a base class. Build
  C2 as a container of the existing satchel types, sealed inside, so each keeps its code. Do not rewrite four
  satchels. Merged satchels must count as one item toward the 125, or C2 does not save space. That needs a
  `TotalItems` override, with a test.
- **C6 has the same question.** A tool in the roll must still fire its own context menus. If that is hard, the roll
  can simply hand a tool to the pack on click.
- **The cheapest real win is C7 plus C8.** Both are guild fixes, not League items. They belong in P178's queue.

## 3. Player upgrades

### Today's values (pinned commit d4531cd, unless marked as shard)

| Limit | Value | Where |
|---|---|---|
| Container item count (any container, nested items included) | 125 | `Projects/Server/Items/Container.cs:177` (`GlobalMaxItems`), `:151`; enforced at `:244-254` |
| Saved per-container `MaxItems` (-1 means use the default) | per item | `Projects/Server/Items/Container.cs:87-102` |
| Default container weight | 400 | `Projects/Server/Items/Container.cs:179` |
| Player backpack weight (ML) | 550 | `Projects/UOContent/Items/Containers/Container.cs:252-262` |
| Shard: player backpack weight | `m.MaxWeight`, no ceiling | `ClusterFBackpack.cs:33-43`, swapped in on connect (`ClusterFWeightPatch.cs:19-51`) |
| Mobile carry weight | `(ML and Human ? 100 : 40) + 3.5 * Str` | `Projects/UOContent/Mobiles/PlayerMobile.cs:232` |
| Shard: Str cap | 500 per stat, 1,500 total (so a Human carries up to 1,850) | `ClusterFStatCaps.cs:10-11` |
| Bank weight | unlimited (0) | `Projects/Server/Items/Containers.cs:23` |
| Bank items | 125 in pinned; on the shard, 1,000 + 100 per League milestone, 1,600 at most | `ClusterFBankLimit.cs:26-47` |
| Pack horse / llama | `StrongBackpack`, 1,600 weight, 125 items | `Projects/UOContent/Items/Containers/Container.cs:227-234`; `PackLlama.cs:52`, `PackHorse.cs:52` |
| Shard: Pack Mule | 1,600-5,000 weight, 150-500 items by tier | `Mobiles/Mule/MuleData.cs:56-63` |
| House secures and lockdowns | from the placement entry, times 1.2 on ML | `Projects/UOContent/Multis/Houses/BaseHouse.cs:280`, `:677-698` |
| Shard: skill caps | 200 per skill, applied to everyone at login | `ClusterFSkillCaps.cs:120`, `:136-139` |

### Client and packet limits

- The container contents packet, 0x3C, writes its length and item count as ushorts
  (`Projects/Server/Network/Packets/OutgoingContainerPackets.cs:178-181`, `:211-213`). At 20 bytes per item that
  caps one container's direct children at about **3,270**. No backpack step proposed here comes near it.
- **The practical limit is the client gump.** F-19 asks for a TazUO test of a full bank above about 1,000 items.
  A 250-item backpack is well inside that, but should still get one render check.
- Nested items count toward the parent's 125 (`Container.cs:245-246`). A bigger backpack therefore also means more
  room inside satchels. That is intended.

### Proposed upgrades

| Upgrade | Steps | Cost (spendable Renown) | Gate | How to build |
|---|---|---|---|---|
| **Backpack items** (first) | 125 > 150 > 175 > 200 > 250 | 2,000 / 6,000 / 15,000 / 30,000 | Bronze / Verite / Blaze / Mythril | Store a `PackTier` on `CharacterLeagueData` (bump v1 to v2, read branch, round-trip test). Write the pack's saved `MaxItems`, the same way `ClusterFBankLimit` writes the bank (`ClusterFBankLimit.cs:119-153`), at login and on purchase. |
| Backpack weight | **not sold** | | | Weight is already Str-driven with no ceiling (`ClusterFBackpack.cs:33-43`), and F-12's Legacy tree already plans a carry-weight node (`feature-queue.md:1256`). Selling it would put it in two places. |
| Bank items | **not sold** | | | F-19 already grows the bank by League milestone. P75's League Warehouse would put it in two places. Hold it until play shows the bank is too small. |
| House storage | later | | | No player houses beyond F-44's inn room yet. Revisit with housing. |
| Pack animal capacity | **not the League's** | | | The mule's tiers and modules (Saddlebags, Load Harness) own it (F-33). |
| Stat or skill caps | **never** | | | The F-13 guardrail bans skill and stat items (`feature-queue.md:1357`). Caps are config values re-applied to everyone at login (`ClusterFStatCaps.cs:103-108`), so per-player caps would need a rewrite anyway. |

### Overlap check: everything that already raises a limit

| Limit | Raised by today | Designed to be raised by | Proposed owner |
|---|---|---|---|
| Backpack items (125) | nothing | nothing | **League** (this pass) |
| Carry weight | Str with no ceiling (`ClusterFBackpack.cs`); stat cap 500 | F-12 Legacy "carry weight" node | **Strength and F-12.** The League does not sell it. |
| Weight in the pack | guild satchels at 30-85% reduction (ore, lumber, hunter's) | P75 "Featherweight satchels" | **Guilds** (satchel tiers). Drop P75's Featherweight satchels. |
| Bank items | F-19 by League milestone | F-12 Legacy "bank slots"; P75 League Warehouse | **League milestones (F-19).** Drop the Legacy bank node and the Warehouse, or keep a single one. |
| Remote bank | nothing | F-34 ledger; F-33 Trader's Ledger III "portable bank" | **The Register's Bank page (F-34).** Keep the mule module as the anywhere tier, or drop one of them. |
| Second carry space | Pack Mule (F-33) | P75 "Overflow to mule" | **The mule** |
| Stat and skill caps | config, everyone | F-12 loops; F-13 veteran (superseded) | **F-12 loops.** Never sold. |
| Young, the reset stone, loot boxes, achievements | none of these raise storage (loot boxes only fall back to the bank, `LootBoxes\ClusterFLootTable.cs:134`) | none | n/a |
| Accessory slots | none exist in code or design | | n/a |

Two places in the existing design sell the same thing twice; Chase decides:
1. **Bank size:** F-19 by milestone, plus the F-12 Legacy bank node, plus P75's Warehouse.
2. **Remote bank:** F-34, plus the mule's Trader's Ledger III.

## What changed

Nothing in either repo except this notes file. No code, no tests, no CHANGELOG, no VERSION.

## Tests

None. This is a design-only task.

## Deviations and decisions for Chase

- **`D:\UO\ModernUO-pinned` is missing.** The engine was read from a read-only shallow fetch of the commit pinned in
  `docker\uo\Dockerfile:3`, kept in the session scratchpad, outside both repos. Someone should restore the pinned
  folder, or point the prompts at the new path.
- **P177 and P178 have not run.** P177 is in `queue`; P178 is in `held`. The menu sketch follows P177's brief, not an
  approved template. The Register reads P178's per-rank action list, so it is built after P178.
- **The shard citations** in sections 2 and 3 came from three read-only research passes over
  `server\customizations`. I re-checked `ClusterFBackpack.cs:33-43` and `ClusterFLeagueRanks.cs:446-465` myself.
- **Prices** are set against the default Renown ladder (`ClusterFLeagueRanks.cs:446-465`; achievements pay 6,505 in
  all). They are a starting point, one data value each.
- The decision list at the top is the "For Chase" list.

## For Chase

Answer decisions 1 to 9 at the top. Nothing is built until you do.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, 2026-10-20:

```
Repo Result
---- ------
code clean
docs dry run
```

P179 DONE
