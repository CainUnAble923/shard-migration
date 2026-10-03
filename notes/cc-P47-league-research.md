# cc-P47: League build-out research (notes only)

Written 2026-10-03 by Claude (Code tab) from `D:\UO\cc-prompts\cc-P47-league-research.md`. Notes only: nothing built,
nothing in `D:\ShatteredLegacy` edited, no deploy, no commit.

**Engine:** `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88` (checked with `rev-parse HEAD`
today). All pinned citations are against that commit. "C\" = `D:\ShatteredLegacy\server\customizations\`,
"P\" = `D:\UO\ModernUO-pinned\Projects\`.

**How this was read:** five read-only research passes (League and ladder; contract code; guilds and currencies; mule
and followers; trial maps), then I re-checked the claims that carry a decision myself: pinned HEAD, `MapLoader.cs`
(no validation), `TileMatrix.cs:71-93` (file sharing), work-order definition count (115, `grep -c`), Artificer order
count (41), `MaxActiveOrdersPerGuild` is per guild (`ClusterFWorkOrderSystem.cs:377`), `PackMule` `ControlSlots = 2`
(`PackMule.cs:88`) against the exchange text "1 control slot" (`CrossGuildExchangeGump.cs:97`), `BaseVendor`
`RootParent != seller` (`BaseVendor.cs:435, :464`), `TeleportPets` 3-tile range (`BaseCreature.cs:4098`), how
`Lumberjacking` is made partial (`docker\uo\apply-patches.sh:430-435`, a sed), `CraftItem.AddSkill`
(`CraftItem.cs:293`). Other file:line citations below come from those passes and were not each re-opened by me.

**Docs moved while this ran.** `docs\feature-queue.md` F-12 gained "Ladder and reserve, decided 2026-10-03": max level
50, 100 at loop 1, then +5 per loop to 200 at **loop 21**; the separate 20 post-cap loops are **dropped**. The F-33
slot target now reads "by loop 11 (max level 150) with Trailwise Tack III, and by loop 21 without it". The brief's
"loop 10 / loop 20" wording is the old one. Everything below uses the new ladder.

## Summary

| # | Question | Answer in one line | Biggest risk |
|---|---|---|---|
| 1 | The League today | Membership, three statuses (one of them computed), Renown that is earned in one place and **never spent**, a Registrar gump. Of the three 10-01 signposts, only the office sign is built, and it is only placed by a seeder whose world-load setting defaults to off. | League data is **per account**, guild data is **per character**. The ladder has to pick one. |
| 2 | 17-rank ladder | 17 metals counted, Iron to Celestial, in `ResourceInfo.cs:6-27`. Generate the ranks by walking `CraftResource` metals. Store the rank **per character**. | **P36 appends Dawnstone after Celestial.** A naive generator gives 18 ranks with Dawnstone at the top. Needs an exclusion rule. |
| 3 | One contract framework | Base it on `ClusterFWorkOrderSystem` + `GuildResources` (115 defs, item requirements, gates, three reward channels). Add a world-persisted instance, progress types, expiry, escrow and a board. Not ML quests. | Kill credit with party share needs a small pinned patch. Hunts and culls wait on F-14 anyway. |
| 4 | Multi-guild favor | 17 guilds, one key each for standing and currency, per character. **Nothing banks for non-members today.** The exchange charges four currencies with hand-written checks. Generalise `GuildResources.TryPay` into a list of costs. | Several existing sites already pay non-members directly. Leave them, or route them through banking? |
| 5 | Multi-rep upgrades and mule | The rule is a small data record. The mule has no tiers, modules or traits and costs **2** slots, not 1. 5 of 7 sized effects need no patch; dismount resistance needs one; vendor sell needs a patch or our own sell flow. | Rank-gating player crafting has no hook in pinned craft. **Fix:** a guild-sold schematic consumed as a craft resource. |
| 6 | Follower slots | A ridden mount **still counts** against followers. A curve meets both targets exactly if `FollowersMax(loop 11) = 15 + E` and `FollowersMax(loop 21) = 16 + E` (E = evo mount cost). | Companion slot costs are written against the old 6-loop ladder, and E is unknown. Legacy-point pet slots can break "not before loop 21". |
| 7 | Citizen Commissions | Escrow numbers in a world ledger, items in an internal container. Strict state machine, a claims ledger instead of ever dropping a payout, posting fee as a sink, 7-day expiry. Steel and Silver mapped to milestone ranks. | **Renown becomes tradable between accounts**, and with it League rank. Close it by ranking on Renown earned from play only. |
| 8 | Trial maps | Holds. Register maps from a customization `Configure()` (no JSON or pinned edit). Tile data is shared by `fileIndex`. Cost is under 1 MB and 3 file handles per map (estimate). | Instance maps inherit **none** of the `Map.Trammel`-keyed rules: recall, gate and mark are open, and the stuck menu escapes. A custom region must restate everything. |

## Clashes and corrections found

1. **P36 vs the ladder (real clash).** `cc-P36-dungeon-build-1.md` Part D item 2 appends `Dawnstone` after Celestial and
   widens the metal range at `ResourceInfo.cs:1092`. The decided ladder rule is "generated from the metal list so a new
   metal adds a rank". Taken literally, Dawnstone (a 45-skill starter ore) becomes rank 18, above Celestial.
   - P36 already keeps the four new resources out of "BOD tables, commissions, work orders and random resource picks".
     Its consumer walk should add **the League ladder** to that list.
   - Proposed rule for Chase: the ladder is the metals that are **not region-only**. Concretely, an explicit
     `LadderExcluded` set (Dawnstone) beside the generator, or a flag on the resource info.
2. **P46 edits `ClusterFSmithCommissions.cs`** (Part D: commissions pay x3 Seals and x2 standing). The contract
   framework should not absorb Smith commissions until P46 has committed. Batch 2 below leaves them alone.
3. **P34 decorates the Registrar's office.** It reads `ClusterFRegistrarOfficeSeeder.cs`, and the office sign lives
   there (`:43-46, :164-173`). Batch 1 touches that seeder only if the sign needs fixing. If both run, run them one after
   the other.
4. **P45** will propose "5 League class trainers" and a party table (its prompt, line 110). Those are League-office NPCs
   and follower slots. Batch 1's office work and question 6's curve should be checked against P45's notes once they
   exist. `notes\cc-P45*` does not exist yet.
5. **"No fresh world" vs "a wipe is coming".** `AGENTS.md` ("There is no migration ... no fresh world") and
   `docs\direction-decision.md:38` say one thing. `feature-queue.md:234, :2153, :2247-2248` and this brief say a 100
   percent wipe is coming. Not mine to settle. For this work it hardly matters, because every new League field is
   additive (see 2.3).
6. **Stale facts in docs and code** (worth fixing when touched):
   - `feature-queue.md` F-33 says the mule is "sold by the Outriders". The Cross-Guild Exchange sells it, and it opens
     from 5 guildmaster gumps (Outriders, Artificers, Foresters, Miners, Smiths).
   - The mule costs **2** slots (`PackMule.cs:88`, `PackMuleDeed.cs:52`), not 1. The exchange text says "1 control slot"
     and "StrongBackpack" (`CrossGuildExchangeGump.cs:92-97`); both are wrong. `PackMuleDeed.cs:18` comment says 1.
   - F-33 cites "cc-P41 section 7.4". There is no 7.4 heading; `party.json` is in 7.3 (`:547-558`).
   - The companions doc's party table (`docs\companions\companions-squire-evo-research.md:140-191`) is written on the
     old six-loop ladder (loops 0-5).
   - `ClusterFWorkOrderSystem.cs:332` says the cap is "across all guilds combined"; the code caps per guild (`:377`).
   - The Artificer catalogue comment says 39 orders (`:106`); `All.Add(new` counts **41**.
   - `CompactDispatchLedger.cs:15-16` says backpack only; turn-ins use pack plus bank since F-11.
   - `GetRankName` has no `mining` case (`ClusterFGuildSystem.cs:576-585`), so the Directory shows the generic ladder
     for the Miners' Compact, whose real ladder is `MinersCompactLiaisonGump.GetRankName` (`:682-690`).
   - The Registrar's ambient speech starts only from `OnAfterSpawn` (`LeagueRegistrar.cs:108-112`). The seeder places it
     with `MoveToWorld` (`ClusterFNewHavenSeeder.cs:181-195`), so the greeting probably never fires. Unverified in game.
   - `LeagueMemberPass` is handed out by nothing (no reference outside its own file).
   - The worldbuilding doc gives the Registrar at 3459,2598; code says 3459,2601 (`ClusterFNewHavenSeeder.cs:71`).

---

## 1. What the League is today

### Files

| File | Lines | What it is |
|---|---|---|
| `ClusterFLeagueSystem.cs` | 157 | Static. Flag keys (`:29-47`), `enum CitizenStatus { Unregistered, RegisteredCitizen, RecognizedCitizen }` (`:51-56`), `GetStatus(data, guild)` (`:62-67`), `JoinLeague` (`:94-105`), `OnDispatchRead`, `OnGuildReferralSeen`, `OnGuildJoined` (`:111-156`). |
| `LeagueRegistrar.cs` | 170 | NPC "Elara Voss", invulnerable, opens the gump (`:71-104`), 6 ambient lines (`:25-33`). |
| `LeagueRegistrarGump.cs` | 259 | 5 views (`:24`), main menu buttons 10-17 (`:93-106`), dispatch switch `:198-258`. |
| `LeagueMemberPass.cs` | 49 | Blessed item that opens `GuildProgressGump`. Nothing hands it out. |
| `ClusterFAccountData.cs` | 777 | Storage (below). |
| `ClusterFAchievements.cs` | 1896 | `AchievementCategory.League = 8` (`:28`), 9 League achievements. |
| `ClusterFBankLimit.cs` | 81 | F-19's League-rank stub. |
| `ClusterFRegistrarOfficeSeeder.cs` | 211 | Office props and sign. |
| `ClusterFNewHavenSeeder.cs` | 328 | Places the Registrar (`:71`). |

Passing mentions only: `ClusterFBulletin.cs` (League Dispatch category, `:17, :387`), `ClusterFGuildSystem.cs:434`
(calls `OnGuildJoined`), dev and admin reset tools, and the referral calls in the Artificers, Foresters, Outriders and
Miners gumps.

### Storage and keys

- League state is account flags: `ClusterFAccountData.Flags` (`HashSet<string>`) and `FlagValues` (`:49-50`). It is
  saved by a hand-written `Serialize`, version 15 (`:348-369`).
- `Renown` and `AchievementPoints` are plain ints on the same class (`:33-34`, saved `:354-355`).
- The container is the `ClusterFAccountPersistence : Item` singleton, holding a dictionary keyed by **account username**
  (`:680-777`, `:685`).
- So **League registration, Renown and AP are per account**. Guild membership, standing and currency are **per
  character serial** (`CharacterGuildData`, `:121-131, :472-602`).

### Statuses

| Status | How |
|---|---|
| Unregistered | No `league.joined` flag. |
| Registered | `JoinLeague` sets the flag (`:100`). Only Registrar button 10 calls it (`LeagueRegistrarGump.cs:214-216`). |
| Recognized | Computed, not stored: the current character has at least one joined guild (`:65`). It can differ between characters on one account. |

`FlagIntroCompleted` (`:32`) is declared and never set.

### Renown and AP

- **Earned in one place:** `TryGrant` adds `def.AP` and `def.Renown` (`ClusterFAchievements.cs:837-838`).
- **Totals:** 74 `Reg(` definitions; Renown sums to **6,505** and AP to **2,505**. This matches F-13's figures.
- **League achievements (9):** registered_citizen 10/25, first_dispatch 5/10, first_referral 5/10, guildbound 15/50,
  ap_100 10/25, ap_500 25/75, renown_500 20/50, veteran 15/35, known 40/100 (AP/Renown). That is 145 AP and 380 Renown.
- **Spent:** `SpendRenown` (`ClusterFAccountData.cs:452-455`) has **0 callers**.
- There is no League tab in `[achievements` (`CategoryTabs`, `ClusterFAchievements.cs:1546-1556`).

### The design doc's MVP list (`league_of_extraordinary_citizens.md:91-98`)

| MVP item | State |
|---|---|
| League membership | Built |
| Initial metal citizen rank | **Not built** (`ClusterFBankLimit.cs:39-40`: "League ranks do not exist yet") |
| Renown placeholder | Built (shown at `LeagueRegistrarGump.cs:139`) |
| Introductory quest flow | **Not built** (`intro_completed` never set) |
| Guild directory | Built (`GuildProgressGump`) |
| New Haven representative | Built |
| League Dispatch integration | Built |
| Future-facing hooks | Partly (achievement category; no expedition hooks) |

### The 2026-10-01 signposts (`feature-queue.md:554-563`)

| Signpost | State |
|---|---|
| League row at the top of the Guild Directory | **Not built.** `GuildProgressGump.Guilds()` returns only `AllGuilds` (`ClusterFGuildSystem.cs:728-742`); rows at `:797-830`. |
| Welcome-page line | **Not built.** `GuildWelcomeGump` (`ClusterFGuildStarterPath.cs:777-806`) has only the Guild Board text. |
| Office sign | **Built in code**, item 0x0BCF at 3463,2597,13 (`ClusterFRegistrarOfficeLayout.cs:40`), named at `ClusterFRegistrarOfficeSeeder.cs:43-46`. It is placed only by `[ClusterFSeedRegistrarOffice`, or on world load when `clusterf.registrarOffice.seedOnWorldLoad` is true, which defaults to false (`:52, :60`). **Unverified on the live world.** |

---

## 2. The 17-rank ladder

### 2.1 The metal list, counted

`ResourceInfo.cs:6-27`, 17 entries: Iron, Dull Copper, Shadow Iron, Copper, Bronze, Gold, Agapite, Verite, Valorite,
Platinum, Toxic, Blaze, Frost, Obsidian, Mythril, Adamantium, Celestial (`Iron = 1` to `Celestial = 17`). This is the
same order as the design ladder (`league_of_extraordinary_citizens.md:58-74`). The six trial ranks (Dull Copper 2,
Bronze 5, Verite 8, Blaze 11, Mythril 14, Celestial 17) are where the storyline puts them.

- **Names and hues:** the private `m_MetalInfo` array (`:581-747`) holds them. The extended metals have localization
  number 0, so name only. There is no public enumerator.
- **The generator** is a walk over the enum:
  `for (r = CraftResource.Iron; CraftResources.GetType(r) == CraftResourceType.Metal; r++)`, using `GetName` and
  `GetHue` (`:1143, :1163`). The upper bound is the hard-coded range `>= Iron and <= Celestial` (`:1092`).
- **A new metal** is picked up automatically once that range is widened. That is exactly the P36 problem (clash 1),
  so the generator needs the exclusion set.
- **Inserting a metal mid-enum** would renumber saved values. Do not do it; P36 already appends.

### 2.2 Storage: per character (proposal)

Store the League rank **per character**, beside `CharacterGuildData` or as a new per-character League record in
`ClusterFAccountData`:

```
LeagueRank       int    0 = not registered, 1 = Iron ... 17 = Celestial (index into the generated table)
PromotionDone    set    rank indexes whose promotion job is complete
TrialsDone       set    chapter numbers complete
LifetimeRenown   int    see below (account level)
```

Why per character:
- Every rank-up input except Renown is per character: guild ranks, F-12 loops, and the Keeper or Breaker choice the
  trials make.
- Per-account rank would let one character's story chapters promote every alt.

Two consequences for Chase to confirm:
- **Registration stays per account; rank is per character.** Joining the League on one character makes every character
  Iron. That matches today's account flag.
- **Renown is per account**, so its threshold is shared by alts. Acceptable, since the other three checks are per
  character.

**Use lifetime Renown for the threshold, not the balance.** F-13's shop spends Renown. A threshold on the balance
would make buying from the shop cost rank progress. Add an account-level `LifetimeRenown` that only rises, fed from
`TryGrant` and League jobs. Commission Renown is excluded (7.5).

**Mapping the three statuses:**

| Today | On the ladder |
|---|---|
| Unregistered | rank 0 |
| Registered | rank 1, Iron. Granted by `JoinLeague`. |
| Recognized | Stays a computed display tag ("has a guild"). The Bronze guild requirement supersedes it as a gate. |

**Migration:** none owed under the wipe. If no wipe happens, it is still only additive. `ClusterFAccountData` goes from
v15 to v16, and on load every account with `league.joined` gets rank 1 on its characters. No existing data changes
meaning. A defaulting rule, not a migration event.

### 2.3 Rank-up rule: where each check plugs in

Decided rule: a Renown threshold, a promotion job at every rank, a story trial at the six milestone ranks, and a rank in
more guilds as ranks rise. One function, `LeagueRanks.CanPromote(pm, out reasons)`, called by the Registrar:

| Check | Source | Exists? |
|---|---|---|
| Renown threshold | `LifetimeRenown >= Threshold[next]` | New field. Numbers come with F-12. |
| Promotion job | `PromotionDone.Contains(next)`. Set by the contract framework when a job tagged `Promotion(next)` is turned in. | Needs batch 2. |
| Trial (2, 5, 8, 11, 14, 17) | `TrialsDone.Contains(chapter)`. Set by the chapter's end. | Needs the storyline, P36 (chapter 1) and the trial maps. |
| Guild ranks | Count of guilds where the character's rank index is at least X, at least N guilds. | **No numeric rank index exists**, only names (`GetRankName`, `ClusterFGuildSystem.cs:576-597`). |

The guild check needs a new helper: `GuildRankIndex(key, data)` returning 0 = Initiate to 5 = Legendary. It must
honour the custom ladders (Smithing, Outriders, Foresters, Custodians, Artificers, and Mining, which `GetRankName`
misses) and the Apprentice-task bump (`:595`).

**Decision needed:** with the trial required, nobody passes Dull Copper (rank 2) until chapter 1 exists, and chapter 1
needs the P36 dungeon. Options:
- (a) A config flag `league.trialsWaivedUntilBuilt`: a chapter that is not built does not block, and the flag is
  cleared chapter by chapter.
- (b) The ladder stops at Iron until chapter 1 ships.

Overseer or Chase to pick. (a) is my default.

**The Registrar gump.** The main menu is nearly full (H 420, 8 rows from y=106, `LeagueRegistrarGump.cs`). Add:
- a **Rank** view (new `View` value, `:24`): current rank in its metal hue, the four checks with ticks, a Promote button
  (free IDs 18 and up);
- the rank in the status line (`:87-88`, `DrawCitizenStatus :109-131`);
- a **Jobs** button that opens the board gump (batch 2).

**Stubs to wire when ranks exist:**
- `ClusterFBankLimit.LeagueRankBonus(Mobile) => 0` (`ClusterFBankLimit.cs:43`). It is the only stub in code, with
  `ItemsPerLeagueRank = 100` (`:28`, unused). Call `Apply` on promotion (`:13-14`).
- F-25's "+2 small and +1 large BOD per League rank" is in the queue only, not in code.

**Flag: per-rank bonuses were sized before the ladder had 17 ranks.** At Celestial (16 steps above Iron):
- The bank gets +1,600 items.
- F-25 gets +32 small and +16 large BODs.
- The F-24 active-job cap reaches 3 + 16 = 19 (or 20 if Iron counts as +1).

Suggest the bonuses step only at the six milestone ranks, or are re-sized. The job cap of 19 may be intended. Chase to
say.

---

## 3. One contract framework

### 3.1 What exists

| System | Lines | Model | Requirements | Expiry | Cap | Rewards | Base? |
|---|---|---|---|---|---|---|---|
| `ClusterFWorkOrderSystem.cs` + `GuildContractLedgerGump.cs` (560) + `GuildResources.cs` | 2,495 | Static `WorkOrderDef` by key (115 defs: Miners 25, Gem 4, Stone 10, Smiths 15, Rangers 33, Foresters 23, Custodians 5). Per-character `WorkOrderEntry` v1 (`:260-313`) in `CharacterGuildData.ActiveWorkOrders`. | Deliver item types from pack plus bank, all or nothing (`:226-251`). Tame-and-deliver (13 defs). "Craft" and "hunt" are really delivery. | None. `AcceptedAt` is display only; no abandon. | 3 **per guild** (`:342, :377`), history 20 | Standing, guild currency, gold created from nothing (`Ledger :531-535`) | **Yes** |
| `ArtificerWorkOrderSystem.cs` | 1,043 | Static defs (41), single active slot on `CharacterGuildData` | Item property values | None; abandon yes | 1 | Gold, Artificer and Smith scrip and standing | As a requirement type |
| `ClusterFSmithCommissions.cs` + gump (285) | 902 | Generated instances with inline data and a Guid (`:34-104`) | Craft one item of a type, material and quality; large = a piece set | None (`IssuedAt` never read); abandon yes | 3 small, 1 large | Seals and standing | Copy its **instance shape**. Do not touch until P46 lands. |
| `ClusterFSmithBODSystem.cs` | 529 | Pinned BOD deeds | Deed-based | None | 3 small and 1 large, counted from the backpack only | Seals, standing | No |
| Clean Up Britannia (5 files, 901) + `ClusterFCustodianSystem.cs` | | Points ledger on our `PointsSystem` (`GenericPersistence`) | n/a | n/a | n/a | Store | No. But see 3.4: `SyncStanding` overwrites Custodian standing. |
| Pinned ML quests (`P\UOContent\Engines\ML Quests`, ~3,651) | | One instance per **class** (`Dictionary<Type, MLQuest>`, `MLQuestSystem.cs:113`) | Collect (QuestItem only), Deliver, Kill (+area), Escort, GainSkill, timed variants | Per objective | 10 | **Items only** | **No**: no runtime parameters, no party support, no currency rewards |
| Pinned bounty (Player Murder System, ~1,135) | | `MurderContext` | n/a | Hides after 14 days, **never refunds** | n/a | Bank deposit | Escrow pattern only (`BountyReportMurdererGump.cs:61-64` withdraw, `BaseGuard.cs:150-175` deposit) |
| Pinned `BountyBoard` (90) | | `BaseBulletinBoard` subclass showing synthetic entries with fake serials (`:12-14, :37-73`) | | | | | Board pattern, if a bulletin-board UI is wanted |

**Recommendation:** a new League contract engine **beside** `ClusterFWorkOrderSystem`. It shares that system's
requirement records, `GuildResources` (pack plus bank `Has` and `TryConsume`, and the `Plan` / consume pattern at
`:204-248`) and gate shape (`IsEligible`, `:147-206`). It does not rewrite the 115 existing defs in the first build.

The guild ledgers keep working as they are. Once the engine is proven, the guild ledgers become one more "source" on
it, and Smith commissions and Artificer orders become requirement types or generators. That later fold-in is its own
batch, after P46.

### 3.2 Proposed shape

```
ContractDef      static, code-registered like WorkOrderDef: key, source (League | Guild | Citizen), guilds[] (1-3),
                 requirements[], rewards, minLeagueRank, tags (Promotion(n), Shareable), duration, gates
ContractInstance world-persisted (GenericPersistence, like PointsSystemPersistence, PointsSystem.cs:211-226):
                 Guid id, def or inline data (Citizen Commissions), poster, escrow, state, created, expires
ContractEntry    per character (CharacterGuildData list, versioned like WorkOrderEntry): instance or def id,
                 acceptedAt, expiresAt, progress (Dictionary<int,int> per requirement; generalises TamingProgress :271),
                 sharedFrom (party)
```

**Requirement types:**

| Type | Hook | Patch? |
|---|---|---|
| Deliver N of a type (filters: resource, exceptional) | Exists (`GuildResources`) | No |
| Craft after accept | Beside `ClusterFCraftRun.AfterAttempt(from, system, tool, item, exceptional)`. That is our existing hook in `server\patches\CraftItem-shard-hooks.patch` and it has the item. `NotifyCraftedItem` does not. | No new patch. One added call inside our own `ClusterFCraftRun`. |
| Gather after accept | Our `Give` overrides: `partial Mining` (`CompactOreSatchelRoutingHook.cs:67`, Mining is a full-file replacement in `patches`) and `partial Lumberjacking` (`ClusterFLumberjackingExtension.cs:59`, made partial by the sed at `apply-patches.sh:430-435`). | **Fishing has no override.** It needs the same sed treatment or a patch. |
| Kill N later (hunts, culls) | `CreatureDeathEvent` passes only the creature. Our achievements use `bc.LastKiller` only (`ClusterFAchievements.cs:1058-1063`). Fair party credit needs the looting-rights loop in `BaseCreature.OnDeath` (`:3550-3634`, beside `MLQuestSystem.HandleKill` at `:3634`). | **A small patch**, for F-14's batch, not the first build |
| Tame | Exists (Outriders crook) | No |

**Rules:**
- **Expiry:** `expiresAt` is checked lazily at gump open, turn-in and progress, plus a daily sweep timer. An expired
  entry is terminal and refunds once (7.3).
- **Abandon:** a button. Abandoning a promotion job only resets its progress.
- **Active cap:** 3 + (League rank - 1) across all League-board jobs. Today's per-guild 3 on guildmaster ledgers stays
  for those ledgers. **Chase to confirm** whether F-24's cap is meant to cover guild ledgers too. The code has always
  been per guild.
- **Rank locks:** `minLeagueRank` on the def. The board shows locked jobs greyed with "Requires Bronze", like F-13's
  shop.

**Party sharing (F-24 defaults):**
- The holder offers the job to party members in range. Each accepting member gets their own entry with `sharedFrom`.
- Kill and gather progress goes to every member who holds the shared entry, is on the same map and is within range
  (18 tiles, a default).
- Each member gets the full reward.
- **Deliver and craft requirements are not shareable:** each member turns in their own items. Otherwise one delivery
  pays N rewards.

**Payout** goes through one function, `ContractPayout.Pay(pm, rewards)`:
- Renown: account `Renown += n` and `LifetimeRenown += n`.
- XP: `LeagueXp.Grant(pm, n)`, a no-op stub until F-12.
- Gold: from nothing for system jobs; from escrow for commissions.
- Per guild in `guilds[]`: `GuildPayout.Pay(pm, key, standing, currency)` (4.3). **Full to each guild** (decided).
- **Never pay "custodians" standing:** `ClusterFCustodianSystem.SyncStanding` overwrites it from lifetime Clean Up
  points (`:189-204`). Pay Custodians in Clean Up points instead.

**Boards:**
- A `LeagueJobBoard : Item` that opens the job gump, which is also reachable from the Registrar. Tabs per F-24 answer 1:
  League, Multi-guild, and the player's own guilds.
- Offers are generated per player from the def pool, rotating daily, so "unlimited" jobs never contend over one
  listing. Citizen Commissions are the only shared listings.
- Placement by a seeder with a coordinate list (the `ClusterFNewHavenSeeder` `SeedEntry` pattern). Start with:
  - the League office;
  - the New Haven bank and tavern;
  - one board at the entrance of each dungeon the starter guilds point to;
  - the main-city banks later.

  Roughly 10 to 15 boards in the first pass. Coordinates are not chosen here; they need a map check.
- A `BaseBulletinBoard` subclass (the `BountyBoard` pattern) is possible, but the bulletin-board client UI is cramped
  for jobs. I recommend a gump.

---

## 4. Multi-guild favor

### 4.1 The 17 guilds

All are registered in `ClusterFGuildSystem.EnsureRegistered` (`:105-275`) as `GuildDef`. One key per guild serves as
both the standing key and the currency key.

| Key | Name | NPC (origin) | Currency | Earns today beyond the Apprentice task |
|---|---|---|---|---|
| smithing | Smiths' Fellowship | BlacksmithGuildmaster (stock) | Smithing Seals | BODs, commissions, salvage bag, artificer combos |
| arcane | Arcane Society | MageGuildmaster (stock) | scrip | none |
| tailoring | Tailors' Circle | TailorGuildmaster (stock) | scrip | none |
| tinkers | Tinkers' Union | TinkerGuildmaster (stock) | scrip | none |
| healers | Healers' Covenant | HealerGuildmaster (stock) | scrip | none |
| bards | Bards' Consortium | BardGuildmaster (stock) | scrip | none |
| thieves | Thieves' Den | ThiefGuildmaster (stock) + lookout | scrip | none |
| warriors | Warriors' Brotherhood | WarriorGuildmaster (stock) | scrip | none |
| mining | Miners' Compact | MinersCompactLiaison (custom) | Mining Vouchers | contracts, survey reports, discovery |
| rangers | Rangers' League | OutridersGuildmaster (custom) | Trail Marks | contracts |
| maritime | Maritime Brotherhood | FisherGuildmaster (stock) | scrip | none |
| merchants | Merchants' Exchange | MerchantGuildmaster (stock) | scrip | none |
| foresters | Foresters' Union | ForestersGuildmaster (custom) | Timber Tokens | logbook, contracts |
| artificers | Artificers' Order | ArtificersGuildmaster (custom) | Essence Shards | imbuing, orders |
| custodians | The Custodians | SanitationWarden (custom) | none | standing = lifetime Clean Up points |
| dojo | Twin Paths Dojo | TwinPathsDojoGuildmaster (custom) | scrip | none |
| keepers | Keepers of the Last Door | KeepersOfTheLastDoorGuildmaster (custom) | scrip | none |

**11 guilds earn only through the Apprentice task** (25 standing, 10 scrip). The code says so:
"the generic guilds have no other scrip source yet" (`ClusterFGuildStarterPath.cs:260-262`). **The job board is the
first income those 11 guilds will have.** That is worth saying when the first job list is written: half the board
should serve them.

**Storage and API:**
- `CharacterGuildData` (`ClusterFAccountData.cs:472`): `GuildReputation` and `GuildCurrency`, both
  `Dictionary<string,int>`, case-insensitive (`:484-485`).
- `JoinedGuilds` (`:477`) and `ApprenticeGuilds` (`:481`) are sets.
- Methods: `GetReputation :590`, `AddReputation :591` (no clamp, no membership check), `GetCurrency :594`,
  `SpendCurrency :595-601`, `AddCurrency :602`. Several callers write the dictionaries directly.
- Membership is free and unlimited ("Each character can join multiple guilds", `ClusterFGuildSystem.cs:69`; `CanJoin`
  `:302-318`).

### 4.2 Banking for non-members: nothing exists

A grep for bank, banked, pending and escrow in guild code finds only ore and wood discovery "pending report" state and
pack-plus-bank item logic.

**Some sites pay non-members directly today:**
- Imbuing pays `artificers` standing with no membership check (`ArtificersImbueGump.cs:1470`).
- `ArtificerWorkOrderSystem.cs:1003-1004`, `CompactOreSatchelRoutingHook.cs:251` and `SurveyArchivistGump.cs:339` have
  no `IsJoined` check, though their tools are only handed out on joining.

**Membership is checked** at BOD turn-in (`ClusterFSmithBODSystem.cs:231, :451`), the salvage bag, contract accept
(`GuildContractLedgerGump.cs:445`) and custodians.

`[ResetGuild all` iterates only `JoinedGuilds` (`:1103-1105`), so standing held by a non-member survives it. Banked
values must be cleared too.

### 4.3 Proposal

Add to `CharacterGuildData` (its own version 0 becomes 1):

```
PendingReputation  Dictionary<string,int>
PendingCurrency    Dictionary<string,int>
```

`GuildPayout.Pay(pm, key, standing, currency)`:
- **Pays** if `IsJoined(key)` and `IsApprentice(key)`.
- **Otherwise banks.** A joined member who has not done the Apprentice task also banks (F-24: "waits for the Apprentice
  task").

Flushing: `CompleteApprenticeTask` (`ClusterFGuildSystem.cs:370-408`) flushes pending into live after `:400-402`, then
the rank shows at once (Chase's veteran-mercenary picture). The guild page shows "Banked: N standing, M scrip, paid
when you finish the Apprentice task".

**Decision:** route the existing ungated sites (Imbuing and the others) through `GuildPayout`, or leave them? Leaving
them is the fidelity-safe default: they are not League work. Flag only.

### 4.4 Multi-currency cost path

`CrossGuildExchangeGump.HandlePurchase` (`:128-204`) reads four balances, checks five `if (x < cost) return` blocks,
then assigns all four dictionaries directly and calls `CompactGoldHelper.ConsumeGold`, **ignoring its return value**
(`:189-193`). It is safe on the single game thread, but it is not a reusable path.

The general path is `GuildResources.TryPay` (`:294-348`), which already does plan everything, then consume, but takes
**one** scrip key. Generalise it:

```
TryPay(pm, GuildCurrencyCost[] currencies, int gold, params GuildCost[] materials)
  check every currency (GetCurrency), materials (Plan), gold
  consume gold first (it is the one step that can fail), then materials, then currencies
```

Then move the exchange onto it. Upgrades (5.1) and League costs use the same call.

---

## 5. Multi-reputation upgrades and the mule

### 5.1 The rule, as data

```
UpgradeStep {
  Id                 "mule.tier3"
  From, To           item tier or type
  RankReqs[]         (guildKey, minRankIndex)        // 2+ guilds
  LeagueRankMin      optional
  Costs[]            (guildKey, amount)              // each guild's currency
  Gold, Materials[]  (Type, amount)
}
Check: every RankReq via GuildRankIndex (2.3); pay via the multi-currency TryPay (4.4).
```

Today each upgrade (Jacob's pickaxes `UpgradeStandingReq` 1,000 / 15,000 / 40,000 / 80,000; Hammer of Hephaestus
5,000) hard-codes one guild's standing and pays through single-scrip `TryPay`. They would move onto `UpgradeStep` when
the "mining, lumber and ranger items" follow the mule.

### 5.2 The mule today

- **Class:** `PackMule : BaseMount`, `[SerializationGenerator(0, false)]`. Body 0x123, ridable, Str 400-450, HP
  250-310, resists 20-65, skills 80-95 (`PackMule.cs:32-89`).
- **Slots:** `ControlSlots = 2`, `MinTameSkill 0`.
- **Pack:** `PackMuleBackpack` holds 4,000 stones and 400 items (`PackMuleBackpack.cs:26-27`).
- **Satchels:** dropping a Compact ore, Hunter's or Forester's satchel on it empties the satchel into the pack
  (`:139-183`).
- **Death:** the pack goes to the corpse (`:215`).
- **Saved:** only `_isMale` and `_nextBreedTime`. No tier, module or trait field. No `PackMule` schema in
  `server\migrations`. How the v0 schema is produced before the first version bump is unverified; PetMimic (v9) is the
  precedent.
- **Sold:** by the Cross-Guild Exchange for 25 each of Mining Vouchers, Smithing Seals, Trail Marks and Timber Tokens,
  plus 25,000 gold. No rank gate. The deed makes it pre-bonded and checks 2 free slots.
- **Breeding:** a pair, 7-day cooldown, a deed in the bank after 24 hours. The gestation timer is not saved, so a
  restart loses the foal. A bred mule is identical to a bought one.
- **Against `compact_mule.md` and F-33:** tiers, module slots, modules, traits, the Compact as seller, rank gates and
  the 1-slot cost are all missing.

### 5.3 Module system (proposal)

- **Mule tier:** a `[SerializableField] int _tier` (1-5). Module slots = tier.
- **Tier upgrades** are `UpgradeStep`s: Miners' Compact rank plus other guilds, Mining Vouchers plus their currencies,
  plus the design's rare materials.
- **Slot cost 2 to 1 (decided):**
  - Setting `ControlSlots` does not adjust the owner's `Followers`. A change must call
    `RemoveFollowers` -> set -> `AddFollowers` (`BaseCreature.cs:2625-2646`).
  - Existing mules need this on load, or the wipe makes it moot.
  - Trailwise Tack III sets it to 0 the same way.
- **Module item:** `MuleModule : Item` with `GuildKey`, `ModuleId`, `Tier`, and `MaxTier` from data (3 now, 5
  possible).
- **Attach:** drop it on the mule. `OnDragDrop` is already ours (`:139`). Check free slots, one module per guild, then
  move the item into an internal list.
- **Detach:** a context entry (`:191`) returns the item to the owner's pack.
- **Serialize:** `[SerializableField] List<Item> _modules` with the items internalized. That needs version 1 with
  `MigrateFrom` (PetMimic pattern).
- **Effects:** read from the list at the hook points below. The mule caches `HasModule(id, tier)`.

**Players craft the modules (decided), gated by guild rank and craft skill.** Pinned craft has no hook for a guild-rank
gate. Our `CraftItem` patch adds only `Refused` and `AfterAttempt`. Two routes:
- **Recommended:** the guild sells a **module schematic** (rank plus that guild's currency). The recipe consumes it as a
  craft resource (`AddRes`, `CraftItem.cs:287`). The rank and currency gate sits at the schematic purchase, so craft
  needs no patch.
- **Craft skill** is the recipe's primary skill. A guild's own skill can be a **secondary** requirement through
  `AddSkill` (`CraftItem.cs:293`).

**Guilds with no craft skill.** The pinned craft systems are Alchemy, Blacksmithy, Bow Fletching, Carpentry,
Cartography, Cooking, Glassblowing, Inscription, Masonry, Tailoring and Tinkering.

| Guild | Module | Craft by | Secondary skill (guild flavour) |
|---|---|---|---|
| Thieves' Den | Shadow Cloak | Tailoring | Hiding |
| Bards' Consortium | Minstrel's Bells | Tinkering (or Carpentry, which makes instruments) | Musicianship |
| Merchants' Exchange | Trader's Ledger | Inscription | none needed |
| Twin Paths Dojo | Steady Hoof Wraps | Tailoring | Bushido |
| Keepers of the Last Door | Soul Tether | Inscription (or Alchemy) | Spirit Speak |
| The Custodians | Salvage Bin | Tinkering (or Carpentry) | none. Custodians have no currency, so the schematic costs Clean Up points. |
| Warriors' Brotherhood | Expedition Barding | Blacksmithy | Tactics |

The alternative for any of these is "the guild crafts it for you": the schematic is the finished module, sold
directly. That breaks the "players craft" decision, so use it only if a recipe proves awkward.

### 5.4 Sizing the effects that touch pinned code

| Effect (module) | Pinned hook | From our side? | Size |
|---|---|---|---|
| Sell from the pack (Trader's Ledger) | `VendorSell` builds from `from.Backpack.FindItems()` (`BaseVendor.cs:1038-1068`). `OnSellItems` rejects `RootParent != seller` (`:435, :464`). | **No.** Either our own "sell cargo" flow (context entry, target vendor, `GetSellInfo` / `IsSellable` / `GetSellPriceFor`, re-implementing `OnSellItems :408-560` with `MaxSell 500`), or **a patch to `BaseVendor.cs`** (walk the mule's pack and relax the root check). | Own flow: about 150 lines and duplicated logic. Patch: small, but needs alternatives argued in notes first (AGENTS). Whether the client shows sell items from an unopened container is **unverified**. |
| Hide with the owner (Shadow Cloak I-III) | Hiding sets `Hidden`; no event (`Hiding.cs:87`). `OnHiddenChanged` and `RevealingAction` are PlayerMobile's. | Yes. Poll in `PackMule.OnThink` (`BaseCreature.cs:3871`), and override `Mobile.OnMove`'s reveal for II (`Mobile.cs:4117-4124`, protected virtual). | Small. **Caveat:** a mounted hidden player is revealed on the first step (`PlayerMobile.cs:3419-3440`), so II only applies while walking beside the mule. |
| Follow through gates and teleporters (Trailwise Tack) | Static `TeleportPets`: same map, 3 tiles, order Guard, Follow or Come (`BaseCreature.cs:4092-4122`), 20 call sites. The mule is pre-bonded, so recall already takes it. | Yes. A leash in `OnThink`: if on Follow and the owner changed map or is more than N tiles away, `MoveToWorld` to the owner. | Small. Honouring `Teleporter.DenyFollowers` (`:869`) from the leash is **unverified**. |
| Emergency recall to the stable (Arcane Ward III) | `AnimalTrainer.EndStable` steps (`:253-267`) are all public: `IsStabled`, `StabledBy`, `SetControlMaster`, `AddStabled`. | Yes | Small. Decide whether it respects `GetMaxStabled`. PackMule can already be stabled with a full pack (the refusal covers only llama, horse and beetle, `:237`). |
| Resist dismount (Steady Hoof Wraps) | `BaseMount.Rider` setter is not virtual and has no event. Paths: `Dismount.DoDismount` (`Dismount.cs:63`), `SetMountBlock` (`PlayerMobile.cs:1089-1096`), Bola (`Bola.cs:87`), InfusedThrow, RidingSwipe (`RidingSwipe.cs:38` calls `BaseMount.Dismount` directly). | **No. Needs a patch.** | Two choke points to cover all four: `Dismount.DoDismount` (ability and InfusedThrow) and `SetMountBlock` (Bola), plus RidingSwipe. One patch file, roughly 20 lines; argue the alternatives in notes first. |
| Lighter ore and ingots, logs and boards (Ore Hopper, Timber Rack) | `BaseQuiver` precedent: overrides `GetTotal(Weight)` (`BaseQuiver.cs:114-128`); `Container` totals are virtual. | Yes (`PackMuleBackpack` is ours) | Small. The rider never carries the pack's weight, so in practice this is more capacity. |
| Rise cheaply, pack kept (Soul Tether) | `GetInventoryMoveResultFor` returns `MoveToCorpse` (ours, `:215`); `ResurrectPet` is public virtual (`:4124`). | Yes | Small |

5 of the 7 need no patch. Dismount resistance needs one. Vendor sell needs a patch or our own flow.

---

## 6. Follower slots for a full party

**How pinned counts:**
- `FollowersMax` defaults to 5 (`Mobile.cs:7827`), saved per mobile, and nothing in pinned or the shard changes it for
  players.
- `Followers` moves only in `AddFollowers` and `RemoveFollowers` (`BaseCreature.cs:2625-2646`).
- **A ridden mount still counts:** the `Rider` setter internalizes the creature and never touches `Followers`
  (`BaseMount.cs:77-135`). Only ethereals move their slots onto the rider (`Ethereals.cs:88-102`).
- So the evolution mount costs its slots whether ridden or not.

**Inputs:**
- **Full party:** player plus 5 companions (companions doc, decided 12:34). Top-rank cost is 3 each, so 15 slots
  (`companions-squire-evo-research.md:148-155, :184-191`).
- **Mule:** 1 slot (decided), 0 with Trailwise Tack III.
- **Evo mount:** **E slots, unknown.**
- **Target** (F-33 as of today): the full set fits by **loop 11** with Tack III, and by **loop 21** without it.

**A curve that meets both targets exactly:** `FollowersMax(11) = 15 + E` and `FollowersMax(21) = 16 + E`, and under
`16 + E` from loop 11 to loop 20. With E = 3 as a placeholder:

| Loop | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12-20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Max level | 50 | 100 | 105 | 110 | 115 | 120 | 125 | 130 | 135 | 140 | 145 | 150 | 155-195 | 200 |
| `FollowersMax` | 5 | 6 | 7 | 9 | 10 | 11 | 12 | 14 | 15 | 16 | 17 | 18 | 18 | 19 |

- Loop 0 stays at stock 5. The companions doc's 2 squeezes a new player's horse; the doc raises that itself
  (`:192-195`).
- Loop 21's single extra slot is the "without Tack" target, and a small capstone reward.

**Still unknown:**
1. **The companion slot cost per rank on the new 22-step ladder.** The companions doc maps cost 1, 1, 2, 2, 3, 3 onto
   loops 0-5 of the old ladder. Until it is re-mapped, "top rank" may arrive at a loop other than 11, and the curve
   assumes it has arrived by then.
2. **E**, the evo mount's slot cost (companions and Evo design).
3. **Legacy points buy pet slots** (F-12, "each capped"). Those slots must sit **inside** this curve, or the loop-21
   target is met early by anyone who bought the node. Easiest: the curve is the cap, and Legacy slots are how part of
   it is earned. Or the node is cosmetic-size (+1) and the curve is lowered by 1.
4. **Tamers.** Tamed pets share the same slots, so a tamer trades party members for pets. That is intended by the
   companions doc.
5. **P45** (not run) may change any of the above; `party.json` does not exist yet anywhere under `D:\ShatteredLegacy`.

The setting is cheap: `FollowersMax` is a saved property, set wherever `ClusterFSkillCaps.Apply` runs (P41 7.3 already
places `party.json` there).

---

## 7. Citizen Commissions

Design (`league_of_extraordinary_citizens.md:211-290`):
- Player-posted requests: resources, crafted goods, consumables, trophies, supplies.
- Rewards: gold, Renown, guild currency; items later.
- Safeguards named but not sized: fee, expiry, rank requirement, escrow, per-account limit.
- One framework with the other two kinds.

### 7.1 Shape

A Citizen Commission is a `ContractInstance` with source `Citizen` and inline requirements (deliver only in the first
build). It is posted at any board or the Registrar.

**Escrow:**
- Held in the instance itself, in the world-level `GenericPersistence`.
- **Gold:** withdrawn from the poster's bank at posting (`Banker.Withdraw`, the bounty pattern).
- **Renown:** `SpendRenown` at posting (its first caller).
- **Guild currency:** `SpendCurrency` at posting.
- **Items** (later): moved into an internal container owned by the ledger. They are moved, never copied.
- The escrow is gone from the poster the moment the listing exists. Refunds return exactly what the instance holds.

### 7.2 Numbers (defaults to confirm)

| Setting | Default |
|---|---|
| Posting fee | 5 percent of the gold reward, minimum 100 gold. Never refunded (a sink, stops spam). |
| Expiry | 7 days, the poster may choose 1 to 14 |
| Per-account limit | Active postings: Bronze 2, Verite 4, Blaze 6, Mythril and above 8 |
| Reward cap per posting | By permission tier (below) |

**Steel and Silver**, which are not on the ladder, mapped onto milestone ranks so each permission arrives with a story
chapter:

| Design says | Ladder rank | Can |
|---|---|---|
| Iron | Iron (1) | Accept commissions |
| Bronze | Bronze (5) | Post small: one requirement line, rewards up to 5,000 gold / 50 Renown / 50 currency |
| "Steel" | **Verite (8)** | Post larger: up to 3 lines, 25,000 / 200 / 250 |
| "Silver+" | **Blaze (11)** | Post public / high-value: no line limit, 100,000 / 500 / 1,000, listed on every board |

### 7.3 State machine

`Open` then `Fulfilled` then `Closed`, or `Open` then `Cancelled` / `Expired` then `Closed`.
- Every transition checks the current state first. Each runs once, synchronously, on the game thread.
- No "claimed by" lock: any eligible citizen may deliver, and the first complete delivery wins. A lock would let one
  player sit on a listing.

### 7.4 Exploits and how each is closed

| Path | Closed by |
|---|---|
| Cancel after delivery | Delivery is one atomic turn-in: consume items, pay, mark `Fulfilled`. Cancel is legal only in `Open`. There is no partial-delivery state in the first build. |
| Delivery racing expiry | Turn-in checks `expiresAt` before consuming anything. `Expired` is terminal and refunds once, by its transition. Both run on the one game thread. |
| Deleted poster | `PlayerDeletedEvent` (already subscribed by `PointsSystem.cs:198`). Open listings become `Cancelled`. Renown refunds to the account, since it is per account. Gold and currency belonged to a deleted character, so they are destroyed and logged. Delivered but unclaimed items are deleted. |
| Deleted deliverer | The payout sits in the claims ledger (next row) for a character that no longer exists. Purge it on the same event. |
| Full backpack or full bank at payout | **Never drop to the ground and never fail the turn-in.** Gold goes to the bank as a balance, then anything that cannot be delivered (item limit F-19, weight) goes to a per-character **claims ledger**, collected at any board or the Registrar. The same ledger receives the poster's delivered goods. The poster never has items pushed into a full bank. |
| Self-dealing between alts | Posting and accepting on the same account is refused. Guild currency is per character, so without this rule commissions would move currency between alts. |
| **Renown becomes tradable between accounts** | Renown is otherwise untradable, and it gates League rank (2.3) and F-13's shop. Commission Renown goes into the spendable balance only, **never into `LifetimeRenown`**, so rank cannot be bought. Cap Renown per posting (7.2). |
| **Standing becomes buyable** | Commissions pay guild **currency**, never standing. Standing comes only from work done for the guild. |
| Delivering junk | Deliveries must be movable, not blessed, insured or newbied, not quest items, and not containers with contents. The `IsStandardLoot` / vendor-sell checks are the model. Material and quality filters work as in Smith commissions. |
| Fee farming | The fee is not refunded on cancel or expiry. |
| Crash between deduct and credit | Both happen in one tick, and a save is a snapshot between ticks. |
| Listing spam | The fee, the per-account limit, and the rank to post. |

---

## 8. Trial maps (instancing)

**The overseer's reading is right in substance and wrong in one detail.**
- `Distribution/Data/map-definitions.json` is loaded by `MapLoader.Configure` (`[CallPriority(2)]`,
  `P\Server\Maps\MapLoader.cs:47-58`).
- The "0-31, 127, 255 reserved" and "id and fileIndex 0-5" rules are **only a comment** (`:31-45`). `RegisterMap`
  assigns `Map.Maps[index]` and adds to `AllMaps` with **no range or duplicate check** (`:103-117`); I read it.
- How real each range is:
  - 127 is real: Internal, and special-cased in `Map.Parse` and `TileMatrix`.
  - 255 is real: the null-map byte in saves (`BufferWriter.cs:468`).
  - 0-31 is convention. Use indexes **32-126**; I propose 40-47.
- `Map.Maps` has 256 slots (`Map.cs:91`).

**Our server's data folder.** The image copies pinned's `Distribution/Data` unchanged (`docker\uo\Dockerfile:97`).
Nothing in customizations, patches or docker touches map definitions. Only `Configuration` is bind-mounted.

**Defining the pool** without editing JSON or pinned: a customization `public static void Configure()` (default
priority 50, so after `MapLoader` and before `World.Load`, `Main.cs:667-674`) creates
`new Map(id: 1, index: 40+i, fileIndex: 1, 7168, 4096, season, "Trial" + i, MapRules.TrammelRules)`, assigns
`Map.Maps[40+i]` and adds it to `AllMaps`. Use Malas (3/3) for Doom.

**It must run on every boot, with the same indexes.** Saves store the index byte and `ReadMap` returns
`Map.Maps[byte]`. A missed or renumbered registration loads everything on those maps with a null map.

**The client:** `SendMapChange` sends `MapID` (`OutgoingMapPackets.cs:55-62`), so the client sees Trammel or Malas.
Houses and multis are server items on map 1, so they are absent in the instance. Statics come from the shared files.

**Memory:** `TileMatrix` links matrices with the same `fileIndex` (`TileMatrix.cs:71-93`, read) and reuses their loaded
blocks, so **tile data is shared, not copied**. Per extra map:
- 3 file streams;
- outer block arrays (about 30 KB for Trammel size);
- a sector outer array (sectors themselves are lazy);
- a one-off hash of the map file at construction (5-10 ms per its comment).

**Estimate: under 1 MB and 3 file handles per map, about 8 MB and 24 handles for 8.** Not measured.

**Regions:**
- Regions are per map. A code-created region per trial map follows the shard's own `DespiseRegion` precedent
  (`C\Services\Revamped Dungeons\DespiseRevamped\Region.cs:56-61`): construct with the trial map, `Register()`, and
  raise the priority above 50.
- `DungeonRegion` gives no housing, dungeon light and no Young protection. It does **not** block travel.

**What happens inside one:**

| Event | Pinned behaviour on an unknown map index | What the trial region must do |
|---|---|---|
| Recall, gate, mark, Sacred Journey | **Allowed.** Every validator compares against named maps (`SpellHelper.cs:666-797`). | Override `CheckTravel` (the `NoTravelSpellsAllowedRegion` pattern). All four spells call the caster overload, which asks the region (`:634-643`). |
| Stuck menu | Allowed (`DungeonRegion.CanUseStuckMenu` excludes only Felucca), and it sends the player to Trammel or Felucca (`StuckMenu.cs:293-303`) | Override `CanUseStuckMenu` to false, or route to the trial's exit |
| Death | Corpse and ghost stay on the trial map | `OnDeath`: start a short timer, then move the ghost and corpse out (the `LeverPuzzleController.MoveMobileOut` pattern, `:422-435`). Or allow rez inside for party chapters. |
| Logout | `LogoutMap` is the trial map, and on login the player is restored into it (`Mobile.cs:1320-1323`), even after a reset | A `PlayerLoginEvent` handler (`PlayerMobile.cs:1234-1238`): if `pm.Map` is a trial map whose instance is not this player's live run, move them to the exit. |
| Server restart | Items and mobiles on the trial maps persist (same indexes). Instance run state must be saved too, or every run is treated as dead on boot and swept. | Save the run table, or sweep all trial maps on boot. **Sweeping is simpler.** |
| Pets | `TeleportPets` moves Guard, Follow and Come pets within 3 tiles. Stay, stabled and distant pets do not follow. | Move-in calls it per party member before `MoveToWorld`. Reset sweeps strays to the exit. |
| Party | `Party.Get(m).Members` (`Engines\Party\Party.cs:186`) | Move-in enumerates members in range of the entrance |

**Precedent:** pinned has **no** instancing. There is no `PeerlessAltar`, and the shard records that instanced
Peerless stayed WON'T (`C\Services\Peerless\BasePeerless.cs:5`). Same-map move-in and move-out precedents exist:
`LeverPuzzleController` (kick timers, `MoveMobileOut`) and the `GauntletSpawner` reset. ServUO's `PeerlessAltar.cs`
(`Enter :399-421`, `Exit :488-548`, deadline timers `:579-626`) is the content reference for the shape.

**The mechanism holds.** Risks:
1. Every `map == Map.Trammel` or `Map.Malas` rule is lost: travel, the Doom rules and 38 hard-coded `Map.Trammel`
   comparisons. The trial region must restate what matters.
2. Registration drift: indexes are save-critical and unguarded (`MapLoader.cs:116` overwrites silently). Put the
   indexes in one constant table, and add a test that asserts they are free and registered.
3. Stragglers: logged-out players, ghosts, corpses, pets and summons left on a reset map. Handle them with the login
   kick, a sweep at reset and a sweep at boot.

Also: `WorldLocation.Equals` compares `MapID` (`WorldLocation.cs:92-97`), so a trial location equals the same Trammel
location. Any of our code that compares locations should compare `Map` instead.

---

## Proposed build order

Each batch is one builder. Dependencies are marked.

**Batch 1: signposts and the ladder**
- Guild Directory League row, welcome-page line; confirm the office sign is in the live world (check
  `seedOnWorldLoad` or run the seeder). Fix the Registrar's ambient speech start.
- `LeagueRanks` generated from the metal enum, with `LadderExcluded` (Dawnstone, clash 1). Per-character League rank;
  account `LifetimeRenown`; `ClusterFAccountData` v16 defaulting (Registered -> Iron).
- `GuildRankIndex` helper, including the Mining ladder fix.
- Registrar Rank view and status line. `CanPromote` with Renown and guild-rank checks live; the promotion-job check
  and the trial check stubbed behind `league.trialsWaivedUntilBuilt` (decision 2.3).
- Wire `ClusterFBankLimit.LeagueRankBonus`, with the per-rank sizes Chase picks (2.3 flag).
- Depends on: nothing. Thresholds are placeholders until **F-12**.

**Batch 2: contract engine, job board and multi-guild jobs**
- `ContractDef`, `ContractInstance`, `ContractEntry`; deliver, craft-after-accept and gather-after-accept requirement
  types (craft via `ClusterFCraftRun`; gather via the `Give` overrides; Fishing needs the partial treatment).
- Expiry, abandon, active cap 3 + rank, rank locks, party sharing for gather progress.
- `GuildPayout` with banking for non-members and the flush in `CompleteApprenticeTask`.
- Multi-guild jobs paying full to each guild.
- `LeagueJobBoard` item, seeder, gump tabs. Promotion jobs for each rank, which turn on batch 1's promotion check.
- A first job list that serves the 11 guilds with no income.
- XP: stub until **F-12**. Hunts and culls (kill type and its patch) wait on **F-14**; dives on **P36**.
- Does not touch the guild ledgers or Smith commissions. Folding those in is a later batch, after **P46**.
- Might need splitting: 2a engine and payout, 2b boards and party.

**Batch 3: multi-rep upgrades and the mule**
- `UpgradeStep` data, the multi-currency `TryPay`; move the Cross-Guild Exchange onto it.
- Mule: slot cost 2 -> 1 with follower re-count; tiers 1-5 as `UpgradeStep`s; module slots = tier; `MuleModule` items,
  attach and detach, serialization v1.
- Module schematics sold by guilds (rank plus currency); recipes in the craft systems (5.3 table).
- First modules: the no-patch ones (Ore Hopper, Timber Rack, Shadow Cloak I-II, Trailwise Tack I-II leash, Soul
  Tether, Arcane Ward III recall, Field Medic Pack).
- Fix the exchange text and the F-33 "sold by the Outriders" line.
- **3b, later:** the two patch-needing effects (Steady Hoof Wraps; Trader's Ledger, own flow or a `BaseVendor` patch),
  each argued in notes first.
- Depends on: **the companions chat** (P41, P45) before mule tiers are built (F-33 asks for this), and the
  **FollowersMax curve** (question 6) for Trailwise Tack III's slot-0 step. That curve also needs **F-12**'s loop
  storage and the companions' re-mapped slot costs.

**Batch 4: Citizen Commissions**
- `ContractInstance` with source `Citizen`, deliver only. Escrow (bank gold, Renown, currency). Fee, expiry,
  per-account limit, rank permissions (7.2).
- State machine; claims ledger; `PlayerDeletedEvent` handling; same-account refusal; the `LifetimeRenown` exclusion.
- Exploit tests for each row in 7.4.
- Depends on: batches 1 and 2.

**After the first build:**
- Trial-map pool and trial region base, then chapters one at a time. Depends on: the storyline being edited, **P36**
  for chapter 1, and P36-style dungeon work for chapter 6.
- Hunts and culls with the kill-credit patch (**F-14**).
- Dives (**P36**).
- Folding guild ledgers, Smith commissions and Artificer orders into the engine (after **P46**).
- Commission item rewards.
- The `FollowersMax` curve (**F-12**, companions).
