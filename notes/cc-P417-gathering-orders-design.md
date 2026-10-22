# P417: rolled gathering orders for the Compact, Union and Outriders

2026-10-22. **Design proposal for Chase's review; no implementation authorized by this note.**
Work-copy evidence: ShatteredLegacy `da1a0cb`, shard-migration `241feef`; pinned ModernUO
`d4531cd94b739613155225c234900de9f47d2c88`. Paths beginning `C/` below mean
`ShatteredLegacy/server/customizations/`; `P/` means the pinned tree's `Projects/UOContent/`.
All numbers headed proposed are tuning suggestions, not running-server settings.

Recommend personal, nontransferable **harvest quotas**: accept, gather the named material, then
claim standing, guild currency and a small gold payment. Keep what you gather. One amount per
material, with variety coming from materials and places, rather than small/large quantities.
Refined deliveries remain an optional, limited supply service; ordinary gathering progression
never requires surrendering repair ingots. Add material sets after the single-material loop works.

## 0. What was checked, and what differs from the brief

Read both work-copy AGENTS files, `docs/README.md`, `docs/direction-decision.md`, `docs/tasks.md`,
the gathering wiki draft, P123 and P150 notes, F-12/F-20/F-38/F-40/F-43/F-47/F-48 in the feature
queue, and `notes/f12-levels-loops-caps.md`. Read P416's actual queued prompt at
`D:/UO/cc-prompts/queue/cc-P416-stone-mining-gate.md`; no P416 implementation note exists in this
work copy. It is a dependency, not a completed change.

| Verified source | Finding and design consequence |
|---|---|
| `C/ClusterFWorkOrderSystem.cs:147`, `:213`, `:247`, `:342`, `:376` | Current eligibility reads standing and effective skill; ordinary requirements count and consume items. Three active contracts per guild, one active instance of a definition. No issuance timer. New orders need an instance-based quota mode, not just changed text. |
| `C/GuildContractLedgerGump.cs:503` onward | Turn-in checks inventory, consumes, pays standing/currency and puts gold in the backpack, then moves the entry to history. The new claim must also serve the League Register's shared path and must not consume quota goods. |
| `C/ClusterFAccountData.cs:129` onward; `C/OreDiscoveryEntry.cs:108`; `C/WoodDiscoveryEntry.cs:91` | Guild progress is per character; discoveries and their aggregate harvest totals are per account. Subtracting an account total at claim would let a sibling character do the work. |
| `C/CompactOreSatchelRoutingHook.cs:69`, `:198`, `:230` | Mining logs colored ore **before** discovery substitution and tool/imbuing yield bonuses. Iron is excluded; granite is not in the ore tally. Add quota tallies at this harvest seam, including iron and granite. Do not pretend today's book already counts them. |
| `C/ClusterFLumberjackingExtension.cs:61`, `:122` | Timber totals also precede substitution/imbuing, and include regular logs. Boards are not counted. Use this harvest stream, with actor attribution, rather than inventory arrival. |
| `C/SurveyArchivistGump.cs:33`, `:228` onward; `C/ForestersLogbookGump.cs:73`, `:332` | Mining reports pay once **per new vein location**, not once per metal. Wood reports pay once per extended timber type. The brief's one-time-report shorthand must not hide miners' continuing exploration income. |
| `C/OutridersCrook.cs:180` onward; `C/ClusterFHuntersSatchelHooks.cs:40` onward | Existing animal progress means animals delivered and deleted. Satchel routing can intercept purchased or moved supplies and chooses a nearby player; it cannot prove who harvested them. Neither is a valid quota tally. Add actor-attributed field and first-tame tallies. |
| `C/ClusterFGuildSystem.cs:619-664`; `C/ClusterFGuildPromotion.cs:56-112` | These guilds have seven standing rungs, but the shared recipe/League rank index maps both 40,000 and 80,000 to index 4. Use the actual standing rung for order bands. Foresters' effective promotion still needs their craft skill; do not grant recipe rank early. |
| `C/Services/BulkOrders/BulkOrderSystem.cs:57-145`; P123 note | Craft BODs already have a six-hour issuance cadence, up to three available offers, skill/material rolls, sets and rewards. Reuse the pattern and tested clock/table seams. Leave the eight craft BODs, deed book, bribes and point banking alone. |
| `C/Requisitions/RequisitionSystem.cs`; `RequisitionTable.cs`; P150 note | Magic-item requisitions are personal, three requests per guild/day, with League rank caps, Renown and Leads. Gathering orders belong beside them, not inside that refresh or payout system. |
| `C/Tutorial/ClusterFLoops.cs:31-39`; `C/ClusterFSkillCaps.cs:13`; `C/LootBoxes/ClusterFLootBoxes.cs:54-73` | The loop ladder helper exists, but actual F-12 level/skill resets remain a stub. Current skill-cap default is 200. Loot-box LevelOf is a skill-total placeholder, not a real level. Do not use it as an order gate. |

P416 specifically makes one iron quota of 100, with today's Raw Ore Sample pay (75 standing,
4 Vouchers, 60 gold), turns the other iron-ore request into another metal's quota, gates stone
on `StoneMining`, sells the stock learning book and supplies restoration voucher shortfalls
for gold. P417 should extend that work, not create a second iron quota or undo its compatibility
rules. The proposed new rolled iron pay below is an explicit rebalance from 75 to 200; already
issued P416 entries retain their promised payout. Confirm P416's selected second metal before
implementing the catalog and map it to that metal's single standard amount.

No live shard, Haven, saves or deployment inspected. No code, services or `docs/` changed.
Harvest times, gold economy, material-site accessibility and anti-bot effectiveness are
**unverified in play**. This is custom guild content, not an OSI gathering-BOD port; any approved
behavior changes need the overseer's fidelity-register review before implementation ships.

## 1. The orders

### Acceptance, cadence and progress (proposed)

1. Each **account and guild** accrues one issue credit per six real hours, capped at three.
   Start a previously unissued guild with three; persist the clock. Credits are separate for
   `mining`, `foresters` and `rangers`, and shared among characters on the account. No online-time
   requirement. This borrows the OSI cadence while deliberately limiting sibling-alt issuance.
2. Drawing an offer spends one credit, creates a stable order ID and binds its character owner,
   material, amount, gates and reward table version. Opening or closing a window cannot redraw.
   Preview has Accept/Decline; decline spends that offer. Acceptance alone starts the tally.
   No paid bribes, reroll button or credit refund for abandonment.
3. Preserve **three held entries per guild per character**, counting offered, active and ready
   entries together with any legacy contracts and later weekly sets. Never draw when full.
   There is also a three-entry account-wide cap for *new rolled* entries in each guild, so
   splitting between siblings cannot stockpile more. Legacy entries do not get deleted to meet it.
4. At acceptance capture the character's material tally baseline and its consumed-work watermark.
   Only that character's later successful harvests qualify. One unit may fill one requirement
   of one guild order, selected by oldest acceptance, with excess going to the next active order.
   Overlapping baselines alone are insufficient; the allocator/watermark prevents duplicate use.
   No backfill from harvest before acceptance, while an offer was waiting, or after a slot was
   already fulfilled. No cross-credit between P416 iron, rolled iron and a set's iron component.
5. Show `Mine 100 Iron Ore after accepting: 34/100. Keep your ore; nothing is taken.` Likewise
   `Chop 60 Oak Logs` or `Tame 3 wild Horses`. The tables' ingot/board columns identify the
   refined commodity the guild supports; **quotas count ore/log harvest, not ingots/boards**.
   Smelting/cutting is optional and neither increases nor consumes quota progress.
6. On reaching quota, mark Ready and notify the owner. A **Claim** button in the existing ledger,
   Dispatch Ledger, logbooks and League Register pays once, remotely like current work orders.
   No NPC trip or inventory check. Ready entries occupy a slot until claimed. Normal orders have
   no expiry or failure penalty. Only the optional later Rush variant has a deadline.
7. Availability reads membership, the actual guild rung, **base** harvest skill and discoveries.
   Effective skill from a crook or equipment does not unlock offers. Recheck on acceptance.
   If skill falls later, hold progress and let the player resume; no new eligible offers are
   manufactured by repeatedly equipping tools. Rewards never scale up when claiming at a new rank.

**Roll rule:** choose the highest eligible catalog band with probability 70%; with 30%, choose
uniformly among the lower eligible bands; within a band, choose uniformly among its eligible
materials. With one band, choose it 100%. An active material may repeat: another iron order is
the same 100, never 150 or 250. The allocator makes this safe. Missing discoveries reduce the
pool, never produce impossible orders. Do not upgrade a reward because few materials are known.

Iron and regular wood are the baseline exceptions to discovery gating. All other metals/woods,
including Dawnstone and Rootwood, must have an account discovery record; for extended resources,
require `Reported` and the character's own base skill. Require reported stock metal records too,
matching today's metal-contract behavior. Stock woods auto-report on discovery. Granite also
requires a first personally mined sample of that granite material and `pm.StoneMining`.
Known sites remain visible as travel hints; no contract promises a high-tier resource at an
unverified or currently unreachable location.

### Rank unlocks

Rung is the seven-step standing ladder, **not** the shared six-step `GuildRankIndex`. For tracked
Foresters, apply effective promotion as well: rung 4/5 both require recipe grade 4; rung 6 needs
grade 5. The guild task can open Apprentice/Scout/Sawyer early today; the proposal does not award
1,000 standing for doing it. Tables and timing below use the actual standing thresholds.

| Standing/rung | Compact | Foresters | Outriders | New catalog access; earlier materials stay available |
|---:|---|---|---|---|
| 0 / 0 | Initiate | Woodcutter | Wanderer | Baseline ore/wood, ordinary field goods, beginner first tames |
| 1,000 / 1 | Apprentice | Sawyer | Scout | Starter dungeon materials, Dull Copper/Oak, wool/feathers, Black Bear |
| 5,000 / 2 | Journeyman | Forester | Outrider | Shadow Iron/Copper, Ash/Yew, Spined hides, Grizzly; weekly material sets later |
| 15,000 / 3 | Surveyor | Arborist | Trailblazer | Bronze/Gold/Agapite, Heartwood/Bloodwood, Horned/Barbed hides, Dire Wolf; stone if learned |
| 40,000 / 4 | Master Delver | Grove Warden | Beastmaster | Verite/Valorite, Frostwood, Nightmare/White Wyrm |
| 80,000 / 5 | Deepwarden | Master of the Wood | Warden of the Wild | All extended bands 5/6, subject to their separate base-skill/discovery gates; Greater Dragon |
| 150,000 / 6 | Legendary Prospector | Legendary Forester | Legendary Outrider | Same standard amounts and payouts; prestige shop, recipe-eligible sets; no endless numerical rank inflation |

### Compact catalog: material amount and qualification

Each row is a single repeatable quota. Amount is ore units (`item.Amount` at the base harvest
tally), not smelting output or stack weight. No alternate sizes for a metal.

| Refined commodity | Mine after accepting | Base Mining floor | Min rung | Reward band |
|---|---:|---:|---:|---:|
| Iron ingots | 100 Iron Ore | 0 | 0 | 0 |
| Dawnstone ingots | 60 Dawnstone Ore | 45 | 1 | 1 |
| Dull Copper ingots | 60 Dull Copper Ore | 65 | 1 | 1 |
| Shadow Iron ingots | 40 Shadow Iron Ore | 70 | 2 | 2 |
| Copper ingots | 40 Copper Ore | 75 | 2 | 2 |
| Bronze ingots | 24 Bronze Ore | 80 | 3 | 3 |
| Gold ingots | 24 Gold Ore | 85 | 3 | 3 |
| Agapite ingots | 24 Agapite Ore | 90 | 3 | 3 |
| Verite ingots | 16 Verite Ore | 95 | 4 | 4 |
| Valorite ingots | 16 Valorite Ore | 99 | 4 | 4 |
| Platinum ingots | 12 Platinum Ore | 112.5 | 5 | 5 |
| Toxic ingots | 12 Toxic Ore | 125 | 5 | 5 |
| Blaze ingots | 10 Blaze Ore | 137.5 | 5 | 5 |
| Frost ingots | 10 Frost Ore | 150 | 5 | 5 |
| Obsidian ingots | 8 Obsidian Ore | 162.5 | 5 | 6 |
| Mythril ingots | 8 Mythril Ore | 175 | 5 | 6 |
| Adamantium ingots | 6 Adamantium Ore | 187.5 | 5 | 6 |
| Celestial ingots | 6 Celestial Ore | 200 | 5 | 6 |

Skill evidence: `C/ClusterFMetalTiers.cs:21-66`, `C/ClusterFMiningExtension.cs:87-105`;
these are the actual mining floors, not today's lower contract skill gates.

**Granite:** optional separate material family from rung 3, never part of the ordinary ore roll.
A player can opt into stone work only after learning stone mining; the same issuance credit
funds it. Plain Granite: **6**, floor Mining 100, reward band 3. Each discovered stock colored
granite: **4**, floor `max(100, metal floor)`, band 4. Each extended granite: **2**, floor that
metal's Mining requirement, band 5 for Platinum through Frost and 6 for Obsidian through
Celestial. Dawnstone granite: **4**, floor 100, band 3. All keep the ore table's minimum rung
or rung 3, whichever is higher. Each granite material has exactly one amount; different
colored stones are different materials. Plain Granite is not a substitute for colored stone.
P416's stock book still requires 100 base Mining to learn (`P/Items/Skill Items/Specialized/StoneMiningBook.cs:25`).
Extend the satchel's colored-granite filter only in an explicit follow-up; quota completion
does not depend on carrying granite or on that bag repair.

### Foresters catalog

Amounts count freshly chopped logs; each named board commodity is supported without taking
boards from the forester. Extended harvest floors are **all 100 in today's code**. The higher
figures below are proposed order-access floors, following the already shared wood crafting
ladder, to keep Starwood jobs out of a first-loop pool. They do not silently change harvesting.
If the separate wood-harvesting redesign lands first, take its approved floors instead.

| Board commodity | Chop after accepting | Base Lumberjacking needed for order | Min rung | Reward band |
|---|---:|---:|---:|---:|
| Regular boards | 100 regular logs | 0 | 0 | 0 |
| Rootwood boards | 60 Rootwood logs | 45 | 1 | 1 |
| Oak boards | 60 Oak logs | 65 | 1 | 1 |
| Ash boards | 40 Ash logs | 80 | 2 | 2 |
| Yew boards | 40 Yew logs | 95 | 2 | 2 |
| Heartwood boards | 24 Heartwood logs | 100 | 3 | 3 |
| Bloodwood boards | 24 Bloodwood logs | 100 | 3 | 3 |
| Frostwood boards | 16 Frostwood logs | 100 | 4 | 4 |
| Ironwood boards | 12 Ironwood logs | 100 | 5 | 5 |
| Ghostwood boards | 12 Ghostwood logs | 115 | 5 | 5 |
| Emberbark boards | 10 Emberbark logs | 130 | 5 | 5 |
| Frostbark boards | 10 Frostbark logs | 140 | 5 | 5 |
| Shadowbark boards | 8 Shadowbark logs | 155 | 5 | 6 |
| Runewood boards | 8 Runewood logs | 170 | 5 | 6 |
| Voidwood boards | 6 Voidwood logs | 185 | 5 | 6 |
| Starwood boards | 6 Starwood logs | 200 | 5 | 6 |

The order floors must live in a shared catalog, with their deliberate distinction from today's
harvest floors visible in help. `C/ClusterFWoodTiers.cs:18-25` supplies the extended ladder.

**Sizing rationale:** 100 baseline units is a short normal gathering trip; 60/40/24/16 narrows
the colored-material request as rare banks and fallback yields matter more. Permanent known
veins/groves make 12/10/8/6 an outing rather than a new discovery requirement every time.
These are initial quantities, not measured time equivalences. Validate cold travel and known-site
trips separately. Aim for 10-25 active minutes for common work and 20-45 for rare work, including
travel. If a material misses badly, tune its **one amount**, never introduce a larger variant.

**Repair budget:** an iron quota consumes **zero ingots**, even if the player owns none at claim.
Current T1 restoration consumes 25 Iron Ingots, 1 Voucher and 100 gold
(`C/MinersCompactLiaisonGump.cs:43-45`). A band-0 quota's 10 Vouchers covers ten such voucher
charges, although its 75 gold covers only part of one restoration; harvesting still supplies
the ingots and other play supplies gold. No claim that 100 ore units always smelt to a fixed
number of ingots: pile graphics and smelting failure matter. The P416 gold fallback is a
separate safety valve, not a replacement for keeping repair materials.

### Outriders catalog: field collection and first wild tames

Use two selectable work tracks, sharing the same account/guild issue credits and held cap.
The player chooses **Fieldwork** or **Taming** before drawing; the choice spends the credit
and cannot be switched after seeing the result. This prevents a hunter receiving an impossible
tame and a tamer needing to kill their target. Material/species variety replaces quantity tiers.

| Field goods to collect personally after acceptance | Standard units | Min rung | Base field skill floor | Band |
|---|---:|---:|---:|---:|
| Ordinary hides, before cutting to leather | 40 | 0 | 0 | 0 |
| Raw ribs | 20 | 0 | 0 | 0 |
| Raw bird | 20 | 0 | 0 | 0 |
| Feathers | 40 | 1 | 30 | 1 |
| Wool, from live wild sheep | 12 | 1 | 30 | 1 |
| Spined hides | 20 | 2 | 50 | 2 |
| Horned hides | 12 | 3 | 70 | 3 |
| Barbed hides | 8 | 3 | 90 | 3 |

Field skill is proposed as the better of base Archery, Swordsmanship, Macing, Fencing or
Wrestling for carcass jobs, and base Herding for live-sheep wool. Do not gate hunting hides
on Animal Taming, as some current supply contracts do. Require a recorded first personal
collection of each field material; ordinary hides/ribs/bird are baseline exceptions. Record
observations even without an order or satchel, and show them on an Outriders field-log page.
Do not infer a material discovery from `EncounteredCreatures` kills alone.

| Successful **first-ever wild tame**, species | Standard animals | Base Taming floor | Min rung | Band |
|---|---:|---:|---:|---:|
| Horse | 3 | 29.1 | 0 | 0 |
| Black Bear | 3 | 35.1 | 1 | 1 |
| Grizzly Bear | 2 | 59.1 | 2 | 2 |
| Dire Wolf | 2 | 83.1 | 3 | 3 |
| Nightmare | 1 | 95.1 | 4 | 4 |
| White Wyrm | 1 | 96.3 | 4 | 4 |
| Greater Dragon | 1 | 104.7 | 5 | 5 |

Floors verified from those exact pinned creature files under `P/Mobiles/Animals/` and
`P/Mobiles/Monsters/`; notably Horse is **29.1**, not today's work-order 29.0. The taming
track opens with Horse at 29.1; later species require an account field sighting/encounter
plus base skill. Species with race restrictions (for example Cu Sidhe) wait for a resolver
that proves that character can tame them. A failed or aborted tame adds nothing.

Hook the successful taming action, snapshotting `Owners.Count == 0` **before** owner mutation;
credit only once control actually passes to the tamer. `P/Skills/AnimalTaming.cs:396-446`
contains the skill roll, first-tame branch, owner update and control assignment. A purchased,
transferred, released/retamed, shrunk/restored, summoned or previously owned pet adds zero.
The animal stays with the player; the crook's delivery action is only for legacy deliveries.

For field goods, count fresh yield in the actual carve/shear operation with its actor and
source creature. `P/Mobiles/BaseCreature.cs:2003` (`OnCarve`) and
`P/Mobiles/Animals/Misc/Sheep.cs:72` (`Carve`) are the source seams. Count carcass hides once,
never again when converted to leather; track `Carved`/sheep-regrowth state, not item moves.
Require wildlife and the actor's lawful harvest/loot rights; no farmed player pets, summons,
resurrected animals or someone else's nearby satchel. Automatic shearing uses the owning
player as actor and the same source validation. Natural sheep wool regrowth is legitimate
new work, subject to issuance limits, not a second credit for the same fleece.

### Light turn-ins and material sets

Retain a small **Supply counter**, separate from standing orders, only if Chase wants refined
goods removed from circulation. Rung 2+: once per account/guild/week, **10 ingots of an eligible
discovered metal** or **10 boards of an eligible discovered wood**. No raw ore/logs, no baseline
novice delivery. This intentionally accepts market stock, pays **gold only**, no standing,
guild currency, bonus roll or skill check; quote at or below the lowest NPC sell-to-player
price for that type. If the implementer cannot verify an arbitrage-free price, omit that row.
It is a supply trade, never a way to fill a harvest quota. Repair ingots can be kept by declining.

Crafted delivery work stays in the owning craft's existing OSI BODs and commissions. An
Outrider tack/provisions delivery, if later added, must have a maker/consumption requirement
and a separate economy review; do not add another craft-order system here.

**Later material sets:** keep Grand Tribute-style names, but request three **distinct** eligible
materials, each at its catalog amount. They are an extra weekly order, not a higher quantity
of one resource and not three old deeds consumed into a new deed. Randomly choose three eligible
bands if possible, then one material per band; if only two bands have materials, choose three
distinct materials from those bands. If fewer than three materials qualify, show a discovery
hint and issue nothing. All three must pass gates before the set is offered. A set uses one
held slot and the same exclusive harvest allocator; units already used for singles cannot
also fill it. Declining/abandoning consumes that week's opportunity.

Proposed weekly standing/currency/gold: rung 2 **500/25/250**, rung 3 **750/37/400**, rungs 4-6
**1,000/50/600**, paid for the whole set (not plus the single payouts). Its lower pay per unit
is deliberate: it uses **no six-hour issue credit** and is optional extra work. Once per
account/guild at Monday 05:00 UTC; a held set must be resolved before the next is issued, no
accumulating weekly credits. No repeatable single-material Grand Tribute or Valorite Cache.

## 2. Reward ladder and time to rank

### Guaranteed order payment (proposed)

Band belongs to the requested material/species, never the claimant's rank at collection.
Guild currency means Mining Vouchers, Timber Tokens or Trail Marks respectively. Deposit gold
in the bank; store a pending payment if delivery fails. No completion XP or Renown in phase 1.

| Material band | Standing | Guild currency | Gold | Examples |
|---:|---:|---:|---:|---|
| 0 | 200 | 10 | 75 | Iron, regular wood, Horse |
| 1 | 300 | 15 | 125 | Dull Copper, Oak, Black Bear |
| 2 | 450 | 22 | 175 | Copper, Yew, Spined hides |
| 3 | 700 | 35 | 250 | Agapite, Bloodwood, Barbed hides |
| 4 | 1,000 | 50 | 350 | Valorite, Frostwood, White Wyrm |
| 5 | 1,400 | 70 | 500 | Platinum-Frost, Ironwood-Frostbark, Greater Dragon |
| 6 | 1,800 | 90 | 650 | Obsidian-Celestial, Shadowbark-Starwood |

This replaces today's inversions rather than copying them: a repeated 20-Valorite turn-in
currently pays 6,000 standing and 10,000 gold (`ClusterFWorkOrderSystem.cs:655-666`). A quota
must not inherit that payout merely because its definition used to be called a cache.
Within bands pay is flat; increasing rarity across bands raises pay while reducing the one
quantity. Tune an outlying material's band/quantity after timing data, not the player's rank.

### BOD-style reward choices and bonus odds

Use existing guild currency for chosen upgrades; introduce no fourth standing/points currency.
One modest, exclusive bonus roll per single-material claim adds variety. Generate the outcome
at acceptance and persist it hidden; repeated claims cannot redraw it. No bonus is a box.

| Order band | No extra | +5 guild currency | Cosmetic | Rare find | Sum |
|---|---:|---:|---:|---:|---:|
| 0-1 | 80% | 15% | 5% | 0% | 100% |
| 2 | 78% | 15% | 5% | 2% | 100% |
| 3-4 | 75% | 15% | 5% | 5% | 100% |
| 5-6 | 70% | 15% | 5% | 10% | 100% |

Cosmetics: guild-hued stock-art apron, cloak or wall certificate, uniform among a guild's
approved three-item cosmetic list. Bind these cosmetics to the account, no skill/stat bonuses.
Duplicate cosmetic substitutes +5 currency, without a second roll. No custom art is required.
Rare-find outcome: Compact **1 Diamond**; Foresters **1 BarkFragment**; Outriders **1 DaemonBone**.
These real stock items are verified in `P/Items/Gems/Diamond.cs`,
`P/Items/Resources/MiscMLResources.cs:135`, and `P/Items/Resources/Reagents/DaemonBone.cs`.
They are useful finds, not a source of epic components; existing legacy gem orders must be
retired from new issuance before Diamond bonuses ship. Reward items never add harvest credit.

| Chosen reward/service | Qualification and proposed cost | Chance / status |
|---|---|---|
| Compact tool/satchel progression | Existing Jacob's Pickaxe upgrades/restoration and Compact bag ladder, current standing/skill/material/gold costs | 100% when qualified and paid; no free tier skip from RNG |
| Seasoned Lumber Satchel / Seasoned Hunter's Satchel | Rung 2, prior bag + 75 guild currency + 5,000 gold | 100%; proposed acquisition path for existing item tiers |
| Arborist Lumber Satchel / Warden's Field Satchel | Rung 4, prior bag + 250 currency + 20,000 gold | 100%; preserve contents and existing item stats |
| Journeyman's Crook / Warden's Crook | Rung 3 / 5, prior crook + 150 / 500 Marks + 10,000 / 50,000 gold | 100%; existing powers, no extra skill cap |
| Forester axe service | Rung 1, 10 Tokens for one replacement ordinary gathering axe | 100%; a concrete tool sink without inventing a new powered axe ladder |
| Guild cloak/certificate choice | Rung 2 / 6, 50 / 250 currency | 100%; same cosmetic pool, chosen version, no standing bonus |
| Band V recipe scroll, later weekly material sets only | Legendary effective promotion; valid owning-craft reward table and that craft's guild rank 5 | **2%** per completed eligible set; no recipe roll on singles |

The recipe chance matches today's `RecipeGatingTable.LargeBodScrollChance = 0.02`
(`C/Engines/Craft/ClusterFRecipeTable.cs:87`), but is a separate gathering setting. On a weekly
set, roll either a recipe at 2% or +5 currency at 98%; a failed/unavailable recipe outcome also
pays +5 currency, never rerolls. No regular single-order cosmetic/rare roll on sets.
Use `ClusterFRecipeRewards` with a non-epic table and a BOD source classification, not a direct
learn call. Foresters use Carpentry/Fletching; Compact may use Blacksmithy only if the player
also meets the Society's rank gate; Outriders may use Cooking only if Maritime rank qualifies.
If no appropriate craft pool exists, disclose the currency substitute before accepting.
Band I-IV promotion books remain the owning guild's route. Bands VI+, wild-only and epic
recipes stay with their approved boxes/bosses/quests; no gathering path bypasses F-43.
Learned keys stay account-wide, scrolls retain existing tradeability and learning rules.

Upgrade costs are proposals except for the explicitly existing Compact services. The wiki
notes did not verify acquisition paths for higher wood/hunting bags and crooks; these must
be wired and tested, not advertised as already purchasable. Current Compact bag costs range
from 25 Vouchers + materials + 5,000 gold to 250 Vouchers + materials + 100,000 gold
(`MinersCompactLiaisonGump.cs:75-96`). Orders primarily solve standing/currency, not every
high-tier gold/material bill. At roughly 0.05 currency per standing, 150,000 standing brings
about 7,500 currency before spending; keeping gold/material gates prevents free maximum gear.

### Progression estimates: assumptions and reproducible calculation

These are **standing thresholds reached**, not promises of promotions before their skill/trial
requirements. They exclude the time to train, travel to unlock materials, acquire tools or
complete F-12 loops. Projections assume every permitted stock tier is discovered/reported and
the relevant base skill is reached when its rung opens; Foresters also meet promotion crafting
requirements. No extended resource, granite opt-in, rare drop, recipe or bought resource is
needed. For Outriders this is the Taming track through White Wyrm. Fieldwork-only stops at
band 3; its slower estimate is given below rather than hiding that difference.

**Schedules:** casual = five 45-60 minute gathering sessions/week, **two rolled completions
per session** (10/week); heavy = seven 2-3 hour sessions/week, **three completions per day**
(21/week). Neither assumes round-the-clock collection of all 28 weekly issue credits.
Initial cached credits and fractional weeks are smoothed; round upward to actual sessions.
No quitting/declining, no optional Supply counter income in the model. Whether those sessions
really finish the quantities is unverified until playtesting; a one-order casual session
roughly doubles the order portion of the time, not the reward per order.

With highest eligible bands 0,1,2,3,4,4 over the six standing intervals, the roll rule gives:

```
Q(0) = 200
Q(h) = 0.70 * reward(h) + 0.30 * mean(reward of eligible lower bands)
Q by interval = [200, 270, 390, 585, 823.75, 823.75]
standing gaps = [1000, 4000, 10000, 25000, 40000, 70000]
weeks per gap = gap / (ordersPerWeek * Q + fixedStandingPerWeek + reportsPerWeek)
```

For the requested **orders plus today's contracts** comparison, casual also does one existing
low-rank contract/session, heavy two/day. Keep its current actual payment in every interval:
Compact `mining.iron_ingots_s` = **100 standing** for 50 ingots; Foresters
`foresters.boards_s` = **75** for 50 boards; Outriders `rangers.tame_horse` = **200** for five
animals delivered. This is a comparison workload, **not** permission to keep those repeatables
forever. The existing contracts are uncapped, so there is no unique current fastest time;
a player with purchased stock could repeat much faster than these assumed workloads.

Mining report allowance after the first rung: casual two **new Dull Copper veins/week** at 50
standing each, heavy six/week = 300. No Iron discovery payout. Foresters' stock wood reports
pay no standing, and no Outrider discovery standing was verified: use zero. The first report
of each of the eight stock colored ores totals **1,050 standing**, but it is part of whatever
new-vein reports actually occur, not an extra recurring 1,050. All extended wood reports sum
**3,150 standing**, once per account across Ironwood, Ghostwood, Emberbark, Frostbark,
Shadowbark, Runewood, Voidwood and Starwood (250/300/300/350/400/450/500/600); exclude them from
this stock-only projection. Previously paid discoveries cannot be paid again for another alt.

**Cumulative weeks: new quotas plus current fixed payments and the reports above**

| Standing | Miners casual | Miners heavy | Foresters casual | Foresters heavy | Outriders casual | Outriders heavy |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 0.40 | 0.18 | 0.42 | 0.19 | 0.33 | 0.14 |
| 5,000 | 1.61 | 0.72 | 1.72 | 0.79 | 1.41 | 0.62 |
| 15,000 | 3.83 | 1.73 | 4.06 | 1.87 | 3.46 | 1.53 |
| 40,000 | 7.71 | 3.52 | 8.08 | 3.74 | 7.10 | 3.18 |
| 80,000 | 12.24 | 5.63 | 12.72 | 5.92 | 11.44 | 5.17 |
| 150,000 | 20.16 | 9.31 | 20.85 | 9.74 | 19.01 | 8.66 |

**Recommended folded system:** remove new issuance of the repeatable fixed orders. Keep the
same quota schedules/report allowances, plus a later named weekly set, completed every other
week casually or weekly heavily. Use its 500/750/1,000 standing after rungs 2/3/4 respectively.
Before sets ship, subtract that weekly contribution; do not budget an unbuilt reward as live.

| Standing | Miners casual | Miners heavy | Foresters casual | Foresters heavy | Outriders casual | Outriders heavy |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 0.50 | 0.24 | 0.50 | 0.24 | 0.50 | 0.24 |
| 5,000 | 1.93 | 0.91 | 1.98 | 0.94 | 1.98 | 0.94 |
| 15,000 | 4.28 | 2.02 | 4.39 | 2.09 | 4.39 | 2.09 |
| 40,000 | 8.23 | 3.90 | 8.41 | 4.01 | 8.41 | 4.01 |
| 80,000 | 12.76 | 6.05 | 12.99 | 6.20 | 12.99 | 6.20 |
| 150,000 | 20.68 | 9.81 | 21.00 | 10.02 | 21.00 | 10.02 |

Examples: casual Forester's last gap is `70000 / (10*823.75 + 0.5*1000) = 8.01 weeks`;
heavy Miner's last gap is `70000 / (21*823.75 + 1000 + 300) = 3.76 weeks`.
The different first-table top times for Outriders come from today's 200-standing deliveries,
not a larger proposed quota payout. Timing models intentionally ignore the one-time 25-standing
Apprentice task and its early rank bump; it can make the opening faster.

Sensitivity: with no new-vein reports, Miners match the folded Foresters column. If a character
knows only Iron/regular wood indefinitely, Q stays 200: standing from 150,000 worth of singles
takes **750 orders**, or 75 casual/35.71 heavy weeks before reports/sets. Thus discovery genuinely
matters. With bands 5 and 6 unlocked, Q becomes 1,139 and 1,462.5 respectively if all lower bands
are eligible; use those only after their real skills/loops, never as the default casual forecast.
Fieldwork-only Outriders use Q=585 from rung 3 onward, so their folded top takes about **25.7
casual / 12.3 heavy weeks** (same earlier Q and weekly set assumption). A one-completion-per-session
Forester takes about **39.9 weeks**, exposing the risk if the proposed quantities take too long.

## 3. Planned extras: include now, later or drop

| Extra | Verdict | Concrete boundary |
|---|---|---|
| Rolled ordinary harvest quotas | **Include now** | Main standing/currency path, with observed-material gates and one quantity per material. |
| Rush jobs | **Later** | Opt-in after showing destination/material and deadline; same standard amount, 45 minutes from acceptance, +25% standing/currency, same gold, one/account/guild/day. Timeout falls back to ordinary pay and never costs standing/Renown/Infamy. Shares issue credits and slots, no extra draws. Must price travel first. |
| Surveys | **Later** | A guaranteed known-to-the-server reachable harvest area plus standard material quota, once/account/guild/week. +10% standing, no extra gold. Can suggest an undiscovered grove/vein but cannot require unverified random terrain. Exploration reward is additive to a genuinely new discovery report only once, not an alias for repeat discovery pay. |
| Survey links to Leads | **Later** | Reuse P150's personal area-description/source-provider pattern and map display. Do not reuse its kill pity, magic-item generation, bonus drop chance or Renown payout. A survey is a destination hint for natural harvesting, never a guaranteed spawned rare vein. |
| Mule Hauls | **Later** | F-38 already requires the mule. Sealed guild-owned freight, mule required at pickup/checkpoints/delivery, once/account/guild/week, three distinct refined materials, fixed catalog quantities; no player repair stock consumed. Separate follow-up must settle loss/death/teleport/pack-transfer rules and rewards. No carry-heavy job for novices. |
| Rare-find collection orders | **Later** | Gems remain Compact work; timber ML extras stay Foresters work. Only freshly generated, actor-attributed rare finds, never backpack totals. Same timer/slots; choose after measuring real drop rates. The modest bonus items above may ship now, without a new rare-find quest. |
| Skill checks on completion | **Include now, bounded** | One ordinary skill-gain check after an authenticated quota claim; no skill awarded directly. Material floor-to-next-floor training window, using approved gathering tables, current skill cap and locks. Use the normal engine, one check per order, no extra check per unit/set component. No checks from market Supply-counter trades. |
| Small/large amounts of the same material | **Drop** | Contradicts Chase's 12:26 instruction. Later large jobs mean sets of distinct materials. |

Display any later percentage payout up front, rounded down to whole standing/currency units.

For a concrete first implementation of completion checks, stock mining windows end at the next
material's floor (Iron ends at 65; Valorite at 112.5); Dawnstone has its separate 45-65 window.
Stock wood ends at the next order-access floor (regular 65, Rootwood 45-65, Oak 80, Ash 95,
Yew 100). Do not invent a zero-width Heartwood/Bloodwood/Frostwood check: require the separately
approved wood training table, otherwise suppress their bonus check and explain it. Extended
metal/wood ceilings follow the approved shared next-material ceilings, last material capped
at 200. For taming, use the actual species `MinTameSkill +/-25` window; no guaranteed gain and
none on a repeat tame. Carcass/wool quotas have no extra combat/Herding check until an approved
activity-specific window exists. This is a bounded subset of F-20, with the remaining training
windows explicitly deferred; it does not claim to solve the known wood training ceiling.
Future optional refined **self-made** deliveries can get a craft check only when fresh-maker
evidence exists; inventory ownership alone earns no training. Keep this distinct from market trades.

## 4. Integration and compatibility

**Fixed contracts:** fold ordinary metal/wood/field-goods and tame deliveries into the quota
catalog. Keep names such as Grand Tribute as weekly sets later. Stop fresh issuance of existing
repeatable gathering definitions when each guild's quota replacement ships; do not alter Smiths,
Custodians or the eight craft BOD catalogs. Existing accepted orders finish under their original
consumption, delivery and payout terms; no surprise reward nerf, no compulsory reset. Legacy
standing/currency payments stay finite because old definitions cannot be reaccepted. P416's
already-held raw-ore contracts retain its promised either-old-turn-in-or-new-quota finish path,
with one completion flag across both. Existing held stone stays finishable as P416 requires;
new granite quotas obey the learned-stone gate everywhere, including remote/combined menus.

**Persistence:** additive versioned gathering-order/account schedule records plus per-character
harvest counters, allocation state, pending claim rewards and observed field materials. Keep
existing discovery records/locations untouched; their account identity and travel features survive.
Snapshot legacy terms when importing still-active definitions, with an explicit discriminator
for fixed delivery, P416 quota or rolled quota. Do not assign a numeric save version in this design:
inspect the current head after P416 before extending it. Old saves get empty quota counters,
not their lifetime harvest as fresh progress. An unknown version fails loudly. All state needed
to distinguish Offered/Active/Ready/Paid, issue credits and reward delivery is serialized.

**League:** show Gathering Orders as a separate section beside magic Requisitions. It pays guild
standing/currency/gold only; Requisitions keep magic-item turn-ins, their three/day refresh,
League gates, Renown and Leads. Gathered goods sold or crafted into a requisition are legitimate
later economic activity. A gathering claim never calls `GrantRenown(LeagueJob)` or pretends
to complete a League request. Standing can satisfy an existing League guild-rank requirement;
that remains its own promotion/trial check, not automatic League advancement.

**F-12 and loops:** preserve guild standing, currency, discovery history, recipes, issue clocks,
held order progress, consumed-work watermarks and one-time reward records through a loop.
Do not refill credits or regrant rank rewards on reset. Actual base skill must qualify again
for new high-material offers after a reset. A held order waits without expiry if skill resets.
With the approved max-level ladder, stock colored materials are practical from loop 1's cap
100; Mining 112.5 first fits loop 4's cap 115, and Celestial 200 requires loop 21. These are
**future capability limits**, not enforced current-level requirements in today's stub.
No additional current-level gate on a basic quota; a low-current-level veteran must be able
to gather and repair. Future F-12 must centrally supply a capability predicate when implemented;
do not gate using LootBoxes.LevelOf. Level restrictions on our powered reward tools continue
to apply on use; an order cannot bypass them. Stock tools keep OSI behavior.

**XP:** normal harvesting/taming/skill-gain hooks remain the activity's XP source when F-12
exists. Phase 1 claims add no XP. Any later completion XP needs a separate budget to avoid
awarding the same work as harvest XP, skill-check XP and quota XP. Guild reputation is not XP.

**Loot boxes:** routine repeatable claims award none. Existing first-time achievement milestones
(including actual discovery achievements) may trigger their normal boxes; no manual second
box on an order completion or each gathering rank. Repeating on a later loop cannot regenerate
first-time boxes. Recipe/rare/cosmetic bonuses here are their own small item outcomes, never
epic components or loop-scroll fragments. Existing F-40 earn-time scaling and account binding
remain in their own subsystem.

## 5. Exploits and failure cases

| Attack/failure | Closure and remaining limit |
|---|---|
| Buy ore/ingots/boards, withdraw a bank stockpile, pick up or trade goods | Progress only comes from the authenticated server harvest action; no inventory/add-to-satchel event. Refining bought stock adds zero. Retired legacy orders are the finite compatibility exception; the optional gold-only Supply counter deliberately trades market stock. |
| Let an account's better miner complete a novice alt's job | Actor-attributed **per-character** material counters alongside the logbook harvest stream. Never subtract account discovery totals to calculate personal progress. Shared account/guild issuance and held caps prevent multiplying that account's draws. Standing/currency rewards go only to the bound character and cannot be transferred as points. |
| Create genuinely separate accounts | Account caps alone **cannot prove one human**, and no honest design closes this completely without an account policy. Nontransferable orders/progress, no signup/rejoin/reset refill, base-skill + discovery work and no tradeable powered jackpot remove the cheap multiplication path. Multiple independently trained accounts can still earn ordinary gold/items by doing real work; log issuance/claims for policy enforcement. Do not use IP caps that punish households. |
| Free rerolls, rank-up/relog/reset redraws, skill toggling | Spend credit on draw, persist offered parameters, no refund on decline/abandon, no rollover reroll. Rank/skill changes affect only a future credit's pool. Changing Fieldwork/Taming/stone preference applies before the next paid draw. Staff replacement preserves original table version/credit and is audited. |
| Prefarm lifetime totals, accept several orders then reuse one harvest | Baseline at acceptance plus exclusive unit allocator/consumed watermark. Future acceptance does not see old excess. The rule also covers sets and P416 quotas. Discovery reports may legitimately reward exploration separately; they do not duplicate quota units. |
| Smelt/cut/stack/split/drop/recollect loop | Only harvest counts. Ore-to-ingot, log-to-board, hides-to-leather and item-move callbacks never create quota units. One base unit cannot be counted as both raw and refined output. |
| Release/retame one horse, pass it between alts, buy a pet | Require first-ever wild tame, capture no previous owners before success, and credit exactly once after control assignment. Persisted creature owner history survives release/shrink. Exclude generated/summoned/test pets. No crook delivery credit on a new tame quota. |
| Farm owned sheep/pets or steal credit from the nearest carver | Wild-source/owner-history checks, legal actor attribution at carve/shear, one source yield event. Satchel proximity and loot pickup prove nothing. Reject previously tamed carcasses. Natural wild-sheep regrowth remains valid new fleece. |
| Pretend discovery-substituted ore was a kept rare material | Existing book may record the rare vein before swapping output. Quota effective material is **after** substitution, with the base amount: locked Platinum yielding Iron credits only an active Iron quota. Failed skill attempts give zero. Never alter existing discovery history to make these meanings identical. |
| Inflate yield through bonuses, duplicate callback, overflow delivery | Count the original base tally amount before Jacob/imbuing bonus additions, as today's book does. Attach harvest sequence/source IDs so retry/routing callbacks cannot credit twice. A completed extraction whose goods fall at the feet still counts: carrying is not required. No resource produced/consumed from the bank means no credit. |
| Replay stale Claim/Turn In requests, combined ledger bypass, reconnect after save | Resolve stable order ID + bound owner + state server-side, atomically mark paid and persist outcome/pending delivery with balance changes. Both ledgers call one service. A second response cannot pay, consume or roll again. Test a save with ready and pending-reward entries, and duplicate responses. |
| Harvest with staff/test crystal or restore older saves | Suppress issue/credit/rewards in dev-bypass mode and audit staff grants. Persist counters, allocations and clocks in the same world-save boundary. Full save rollback rolls back both work and rewards; do not store issue state in an independent sidecar clock that can drift. |

**Important semantic choice:** reuse the logbooks' **harvest tally stream**, not the raw account
totals as authorization. Add a long-lived per-character 64-bit quota tally with the actor and
effective material at those same seams; retain account discovery totals for display/history.
Iron/granite/field goods/first tames need new entries in that stream. This is necessary work,
not an assertion that today's logbook provides all requested quota data.

## 6. Build plan after Chase reviews

No prompt IDs reserved here; dispatcher can assign them. Sizes are estimates of substantive
implementation/review scope, not file counts measured from future code. Every server prompt
uses canonical customizations/targeted patches, argues any new upstream hook alternatives
before patching, and runs `docker/uo/build.sh` under the Golem docker-build lock in a throwaway,
loopback-only environment. Never deploy or connect to Haven. Every **new test must be observed
failing against the missing/broken behavior first**, then passing; retain red/green evidence.
PowerShell tests, if needed, run with `powershell.exe` 5.1.

| Prompt | Touches | Size and dependency | Required behavior tests |
|---|---|---|---|
| A. P416 reconciliation + harvest accounting | server; notes | Medium; first, after P416 lands. Actor/material catalog, iron/granite inclusion, character tallies and exclusive allocator; additive save versions | Harvest before/after accept; bought/picked-up/refined goods zero; sibling actor zero; substitution credits actual base material; bonuses not double-counted; overlapping quotas consume units once; save/load, old-save defaults and P416 either-way completion |
| B. Rolled Compact/Forester issuance and claims | server; notes; wiki draft | Medium; A. Stable offers, six-hour account schedule, three held, catalog/gates, shared claim path; retire fresh fixed issuance guild by guild | Six-hour boundaries, three-credit cap, first contact once, decline/abandon costs, restart/rejoin/loop no refill, all material gates/base skills, stone gate on every menu, reward snapshots, remote/register claim once, bag/inventory unchanged, legacy fixed finishability |
| C. Outriders quota sources and UI | server; notes; wiki draft | Medium/large; A/B. First-tame and lawful carve/shear hooks, field observations, separate tracks, field-log page | Actual successful tame event reaches progress; prior owners/transfer/shrink/failed tame zero; exact species/base skill; actual carve/shear actor vs nearby satchel; owned/summoned sources zero; hide-to-leather no second credit; sheep cooldown/restart; wildlife goods retained |
| D. Rewards and bounded skill checks | server; notes; wiki draft | Medium; B/C. Table-backed payouts, pending reward delivery, exclusive bonus odds, existing bag/crook upgrade acquisition | Payout thresholds/table odds with injected RNG boundary values; no bonus reroll on claim; unavailable/duplicate reward fallback; upgrade consumes prior item and transfers contents; gates retained; permitted check once through normal gain/cap/lock path; no check from bought stock; no XP/Renown/box on routine claim |
| E. Named weekly sets and recipe rewards | server; notes; wiki draft | Medium; B-D; optional second release | Three distinct eligible materials at exact standard quantities; exclusive allocation vs singles; weekly account limit and no banked week; no credit on old deed combination; whole-set payout; recipe 2% boundary, owning-guild/rank gate, unavailable pool fallback, epic/wild-only rejection |
| F. Playtest numbers and later variants | research/notes initially; separate server prompts only after review | Small numbers pass, then **separate medium prompts** for Survey, Rush, Rare finds and mule Haul | Record common/rare travel+harvest times, fallback yield and gold/tool costs; each later variant has source/expiry/teleport/loss/anti-replay tests appropriate to it; no giant all-extras implementation prompt |

A/B may ship for miners/foresters without waiting for C. Do not advertise Outrider quotas until
its sources are real. If D follows a later release, B uses guaranteed standing/currency/gold
only and hides unimplemented bonus/shop features. E is explicitly later; baseline singles
must support full standing progression without it. Supply-counter trading is optional and
can be omitted entirely; if requested, include a separately verified vendor-price test in D.
Future prose changes go to `notes/wiki-drafts/`, never agent edits to `docs/`.

For each implementation, include a scratch-save round trip with legacy, offered, partially
filled and ready entries, plus actual harvest/tame/claim integration tests. Pure formula tests
alone would miss the P150-style error where a hook exists but never reaches the player.

## 7. Open questions for Chase (non-blocking design choices)

These are review choices, not requests to build. No unattended execution waits for answers.

| Question | Options | Lean and consequence |
|---|---|---|
| Is the stock-only pace right? | About 21 casual / 10 heavy weeks as proposed; slower (one order/session gives roughly 40 casual weeks); faster by raising standing while leaving currency/gold separate | **Start with 21/10**, time real sessions before changing pay. Do not tune from level-200 rare-metal assumptions. |
| What happens to fixed orders? | Keep all repeatable alongside rolled; fold repeatables and retain named weekly sets; replace every fixed order including names | **Fold**. Unlimited purchased-stock turn-ins would defeat the quota identity and dominate the timer. Grandfather accepted work. |
| Should new iron quotas pay P416's 75 or proposed 200? | Preserve 75; rebalance all newly issued rolled work to this ladder | **200 for new rolls**, keep P416 already-issued promises. P416's second metal needs reconciliation before build. |
| Do ingot/board turn-ins still earn standing? | No refined turn-ins; optional gold-only Supply counter; a separate bounded paid progression delivery with fresh-origin proof | **Gold-only optional counter**, never force novice repair-stock consumption. Fresh-origin delivery needs its own design rather than inventory checks. |
| Issuance identity? | Per character like craft BODs; account/guild credits with character-owned work | **Account/guild credits**. It changes the OSI pattern intentionally and closes sibling-alt draws. Separate real accounts remain a policy issue, explicitly not solved by IP checks. |
| Must independent alt accounts share a human owner's cap? | Permit separate trained accounts to earn through real work; share caps across staff-confirmed linked accounts | **Support linked-account cap groups if Chase requires them**, using an established account policy. The server cannot infer a human identity from an IP or character name; no verified account-linking registry was found in the inspected gathering sources. Do not claim a hard human-level cap without it. |
| Extended wood order gates? | Current harvest floor 100 for every extended wood; proposed 100-200 order ladder; wait for the separate harvest redesign | **Proposed order ladder**, reconcile with an approved harvest redesign when it exists. Never present craft floors as current harvest behavior. |
| Outrider paths and pace? | Taming and Fieldwork with different top rewards; equalize by adding higher-risk field materials; keep tame deliveries | **First-tame and Fieldwork tracks now**, disclose field-only ~26/12-week estimate; add high-end field materials only from measured sources. No taking a player's new pet. |
| Skill training now? | No completion checks; bounded authenticated checks; guaranteed gains | **Bounded checks**, no guaranteed gain, with wood/field windows deferred explicitly. Honor F-20 without inventing a new skill-point currency. |
| How far should recipes and random rewards go? | Currency-only choices; proposed small bonus pool plus 2% non-epic set recipe; full BOD/loot-box reward lottery | **Small bonus + later 2% gated recipe**. Functional upgrades remain purchased, and epic/wild-only recipes remain in their existing sources. |
| Which extras first? | Rush; Surveys; mule Hauls; Rare-find quests | **Surveys after single quotas and sets**, using reachable-site evidence and personal Lead-style hints. Hauls require a separate mule/loss design. |

## 8. Verification for this design task

P417 has no lane tests and adds no executable code or test gates. Source inspection and
arithmetic checks are the validation for this note; implementation tests above are requirements
for future prompts, not claimed passing tests. Python recomputation checked both progression
tables, expected roll values, report sums and the fieldwork/one-order-session sensitivities.
Windows PowerShell reports version 5.1.26100.9444. The read-only progress command
`python tools/progress.py --dry-run` completed successfully with `SL_SHARD` and `SL_MIGRATE`
pointed at these work copies. It did write `tools/progress.json` despite `--dry-run`: ours to
fix in a separate tooling prompt, proven by the generated timestamp/diff and
`tools/progress.py:722` writing inside `build()` before `main()` checks `--dry-run` at line 737.
Restored only that generated file to its initially clean HEAD bytes; no tooling fix is included.
Final scope is this note alone; ShatteredLegacy is clean and no `docs/` file changed. The note
is under 5 MB and has no trailing whitespace. No commit, branch switch, build or deployment
was performed. No art request needed: proposed cosmetics use existing stock art and no new
asset has been requested or generated.

P417 DONE
