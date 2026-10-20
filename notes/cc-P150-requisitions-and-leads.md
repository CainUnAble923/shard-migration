# cc-P150: Requisitions board, the Appraiser, and Leads (F-47, F-48)

2026-10-19. Fable (the Bronze Golem, branch `golem/Bronze/P150` in `D:\UO\golems\Bronze\`). Prompt:
`D:\UO\cc-prompts\claimed\Bronze\cc-P150-requisitions-and-leads.md`. Not committed: the Golem commits after DONE. Both
work copies were clean at the start. "C\" is `server\customizations\`, "P\" is `D:\UO\ModernUO-pinned\Projects\`
(pinned `d4531cd94`).

No task-list tool exists in this session, so the prompt's steps were tracked here instead:

- [x] Read the spec (F-47, F-48, F-9, F-24, F-37, F-49) and the P47, P48, P127, P142, P145 notes
- [x] Found what exists ("What exists" below, file:line)
- [x] Section 1: the board (data, roll, refresh, turn-in, pay, gump, hall hook)
- [x] Section 2: the Appraiser (price formula, NPC, seeder, towns)
- [x] Section 3: Leads (roll, kill hook, 2x and pity, expiry, seams)
- [x] Section 4: loot rater tag (server side; the script change is noted for Chase)
- [x] Tests, red then green: run on the resume (2026-10-19 evening, Chase's resume note): every fact red first, two real
      defects found by the green run and fixed, final gate green, image `sl-modernuo:cc-P150` built (see "Tests")
- [x] Patch notes, VERSION (2026.10.19.6 on the resume: 2026.10.19.5 is cc-P191's)
- [x] Commit preflight dry run against the Bronze work copies (both "dry run", nothing BLOCKED)
- [x] Notes finished

## Headlines

- **Finished on the resume (overseer's note of 2026-10-19 19:08).** The 14:45 run wrote everything but never got a
  build (Docker froze). The files the overseer saved on `golem/Bronze/P150-wip` turned out to be the **red tree** (the
  break script had been applied when the branch was saved), which made the first build of the resume the red cycle: 11
  of the 12 facts failed, each by its break. Reversing the breaks and building the real tree found **one compile error
  in the test and two real defects** (a guild's board view opened on the first guild instead of its own, and the Lead's
  kill handler read the map of a creature pinned had already deleted, so a Lead never dropped into a corpse through the
  real death event). Both fixed; fact 7 got its own red (its saved break never reached it); the final gate is green:
  **1,557 shard tests, image `sl-modernuo:cc-P150`**. Detail under "Tests".
- **A requisitions board (F-47).** Each character holds **3 open requests per guild** for 17 guilds (the Custodians post
  none), rolled from a per-guild theme table (`Configuration\requisitions.json`, written with the defaults on first
  start) at the tier the character's **rank in that guild** allows, capped by the **League rank gate**. The set rolls
  over once a day at a fixed server time (**05:00 UTC**, in the table); an unfilled request is simply replaced: no Renown
  loss, no standing loss, no Infamy (which does not exist in code). Found or crafted both count: the turn-in reads the
  item's properties through the Artificers' catalogue, so the board and the Imbuing table agree on what a property is.
- **Pay** is the tier's Renown (`GrantRenown`, `RenownSource.LeagueJob`, so it counts toward League rank), the guild's
  standing, and **gold equal to the Appraiser's price**, one formula (`AppraiserPricing.Price`) shared by both. The item
  is consumed. An item turned in here cannot also go to Clean Up Britannia (it is gone), and the turn-in pays no Clean Up
  points: one exit per item.
- **Where:** a `RequisitionsBoard` item in the New Haven field office (League view, every guild, paged), a
  **Requisitions** button on every guild's hall page (`GuildTaskDetailGump`, that guild's view at its New Haven chapter),
  a **Requisitions board** entry on the League Registrar's menu, and the Appraiser's menu. A later real hall (F-49) calls
  `RequisitionsBoard.OpenFor(pm, guildKey)` or places a `RequisitionsBoard` with `GuildKey` set; nothing else is needed.
  Turning in needs a counter within reach: a board covering the guild within 3 tiles, the Registrar or an Appraiser
  within 4, or that guild's guildmaster within 8.
- **The Appraiser (F-47).** A League clerk NPC who buys any magic item (property count and intensity, near stock sell
  levels, capped at 500 gold); a plain item is refused ("a shopkeeper will buy it"). Double-click for Appraise, Sell,
  "Which requisition wants this?" and the board; drop an item on them for a quote with Sell and Keep. Placed by
  `ClusterFRequisitionSeeder` on every world load at **9 posts**: the field office and the banks of Britain, Trinsic,
  Minoc, Vesper, Moonglow, Skara Brae (Trammel), Luna (Malas) and the Royal City (Ter Mur). Coordinates below.
- **Leads (F-48).** A request may roll with a Lead (10% to 35% by League band): an area and a creature group, held
  **3 days**, personal. A qualifying kill there gets an **extra roll** at the fame band's chance (the "2x": the natural
  chance once more) and counts toward a **pity guarantee at the 40th kill**; the drop is a normal item that fills the
  request, into the corpse, no tag. A Lead that runs out just clears. A request carrying a live Lead **survives the daily
  refresh** until the Lead has lapsed (so a Lead always pays off). **Changed from the brief:** a qualifying kill is a
  non-pet creature of the Lead's group, in the area, with **Fame at or above a floor (1,000)**, not "whose loot table can
  roll that item type": pinned creatures do not keep their loot packs, and every AOS pack from Meager up rolls every kind
  (reasoned below). Seams: `RequisitionLeads.Sources` (an `IRequisitionLeadSource` list asked before the area table: for
  treasure maps, stolen family parts, exploration achievements) and `ClusterFRequisitions.HuntFamily` (an active League
  hunt names the slayer family a slayer row marked "any" asks for).
- **Loot rater (section 4).** The server side: `[requisitions` prints one `[Requisition]` line per open request (the
  `[artificerrank` shape), and `ClusterFRequisitions.FirstMatch(pm, item)` answers "would any open request take this".
  The script (`SL_Combat_Rater.py`, `D:\UO\sl-scripts`) is not on this desk and is not changed; the line format and the
  two-line change it needs are under "For Chase".
- **Deviation D-131** (text below): OSI has no requisition board, Appraiser or Leads.
- **Save format:** `ClusterFAccountData` **v20** adds `CharacterRequisitionData` per character serial (append-only; a v19
  save loads with no board, and each character rolls its first set when it next reads one).
- Tests: 12 facts in `server\tests\Misc\RequisitionsVerification.cs`, each red first against a deliberate break (the
  table under "Tests").

## What exists (read first, reused)

| What | Where | Used for |
|---|---|---|
| Guild defs, 18 guilds, `GuildTaskDetailGump` | `C\ClusterFGuildSystem.cs:26` (`GuildDef`), `:105-290` (the registrations), `:303` `GetDef`, `:306` `GetDefForGuildmaster`, `:628` `RankThresholds`, `:642-664` `GuildRankIndex` (0 Initiate to 5 top), `:1030` the hall page | the guild list the board rolls for; the tier is the rank index; the hall page's new button |
| Per-character guild data | `C\ClusterFAccountData.cs:697` `CharacterGuildData` (`AddReputation :882`, `JoinedGuilds :707`), `:136-153` the per-serial accessors, `:371-430` the versioned reader, `:451` `CurrentVersion` (19 before this task) | the standing paid; the storage pattern copied for v20 |
| Renown | `C\ClusterFAccountData.cs:588` `GrantRenown(amount, RenownSource)`, `:610` `RenownSource` (`LeagueJob` reserved for batch 2 by cc-P48) | the Renown pay |
| League rank | `C\ClusterFLeagueRanks.cs:194` `GetRank`, `:208` `SetRank`, `:436` `LeagueLadderTable` (the JSON-with-defaults pattern, `:446-465` the rows) | the gate; the table pattern |
| Registrar gump | `C\LeagueRegistrarGump.cs:106-132` the main menu (rows full since cc-P69), buttons 18-25 taken | the new entry on the League Rank row |
| Field office | `C\ClusterFRegistrarOfficeSeeder.cs:2` (walls x3453-3462, y2596-2603, floor z18), `C\ClusterFRegistrarOfficeLayout.cs:20-33` the props, `C\ClusterFNewHavenSeeder.cs:71` the Registrar at 3459,2601,18 | where the board and the first Appraiser stand |
| Seeders | `C\ClusterFInstitutionSeeder.cs` (runs every world load, duplicate-safe within 15 tiles) | the pattern for `ClusterFRequisitionSeeder` |
| Commissions (F-37) | `C\ClusterFSmithCommissions.cs:44` `IssuedAt` (written, never read: no expiry exists, cc-P47 3.1), `:721` `Complete` (Seals and standing, no Renown); **Infamy: no code anywhere** (`grep -rn Infamy` over `C\`: nothing) | F-37's penalty does not apply here and could not: nothing to call |
| Work orders | `C\ClusterFWorkOrderSystem.cs:260` `WorkOrderEntry`, `:336` the system | the inline-entry shape copied for `RequisitionEntry` |
| Clean Up Britannia turn-in | `C\Services\CleanUpBritannia\CleanUpTrash.cs:39` `AddCleanupItem`, `:111` `Award`; `C\Services\PointsSystems\CleanUpBritanniaData.cs:316` `PropertyWeight` reading `ImbueCatalogue.GetTotalWeight` | the "one exit per item" check; the same intensity reader |
| The Artificers' catalogue | `C\ArtificersImbueGump.cs:29` `ImbuePropertyDef` (`Get`, `Set`, `FullMax`, `IntensityPercent :134`), `:145` `ImbueCatalogue`, `:745` `ForItem`, `:755` `GetItemFlag` (weapon, armour, jewel, clothing; **no spellbook**), `:782` `GetTotalWeight`, `:799` `CountActiveProperties` | reading a request's property and an item's count and intensity; a spellbook is read through its own `AosAttributes` |
| Loot generator | `P\UOContent\Misc\LootPack.cs:179-258` the AOS magic lists (weapons, ranged, armour, shields, jewelry in every pack from Poor up), `:337-380` the AOS packs; `P\UOContent\Items\Skill Items\Tools\BaseRunicTool.cs:283, :613, :801, :930, :1084` `ApplyAttributesTo` (weapon, armour, hat, jewel, spellbook), `:574` `GetRandomSlayer`; `P\UOContent\Misc\Loot.cs:67-181` the type lists, `:393-496` the Random* makers | the Lead's drop; the "can roll that type" reasoning |
| Slayers | `P\UOContent\Items\Weapons\SlayerGroup.cs:20` humanoid super Repond, `:66` undead super Silver, `:434` `GetEntryByName`; `SlayerEntry.cs:105` `Slays(Mobile)`; `BaseWeapon.cs:24` `ISlayer` (weapons, spellbooks, instruments) | slayer requests and the family's super slayer; a Lead's group test |
| Stock sell prices | `P\UOContent\Mobiles\Vendors\GenericSell.cs:12-83` (quality, durability and damage level only; magic properties add nothing); SBInfo tables: Longsword 27, Bow 17, WarMace 15, GoldRing 13, Spellbook 9, Lute 10, LeatherChest 52, PlateChest 121, HeaterShield 115 | the Appraiser's base prices |
| Creature death seam | `P\UOContent\Mobiles\CreatureEvents.cs:8-9` `CreatureDeathEvent`, raised at `BaseCreature.cs:3669` after `base.OnDeath(c)` (the corpse exists); ours at `C\ClusterFAchievements.cs:1356` (`[OnEvent]`, `LastKiller`) | the Lead's kill hook |
| Regions | `P\Distribution\Data\regions.json` names (Despise, Covetous, Deceit, Shame, Wrong, Destard, Hythloth, Ice, Fire, Orc Cave, Orc Fortress, Terathan Keep, Britain Graveyard, Khaldun, Doom); ours `C\Regions\OldHavenBurrowsRegion.cs:35` "the Rootdeep Burrows" | the area table; `Region.IsPartOf(name)` |
| P145's rater | `C\Imbuing\ArtificerRankCommand.cs` (`[Artificer]` lines, 180-character chunks); `notes\cc-P145-combat-script.md:62` | the `[requisitions` command's shape |
| Hall locations | `C\ClusterFGuildStarterPath.cs:205-236` `GuildLocations.All` | the per-guild view is the hall page, so no new tiles were needed |

Also read: F-9's skills table (`C\ClusterFGuildStarterPath.cs:39-66`); `notes\cc-P48-league-batch-1.md` ("Left for batch
2": `LeagueJob` Renown, a Registrar row); `notes\cc-P127-port-treasure-maps-monster-stealing.md` and
`notes\cc-P142-monster-stealing-shard-rules.md` (family parts live in the creature's pack, `StealLootTables.cs`
`TryFamilyPart`): both are seams here, nothing built.

## What changed, with file:line

### D:\ShatteredLegacy

| File | What |
|---|---|
| `C\Requisitions\RequisitionData.cs` (new, 166 lines) | `RequisitionKind` (Property, Slayer, AnyMagic); `RequisitionEntry` (guild, kind, category, property, min intensity, min properties, slayer, tier, Renown, standing, rolled at; the Lead: area, group, expires, kills) with its own version and `Serialize`; `CharacterRequisitionData` (`RolledDay`, `Requests`, `Find`, `CountFor`) |
| `C\Requisitions\RequisitionTable.cs` (new, 545 lines) | the JSON table: `RefreshHourUtc`, `PerGuild`, `LeagueGate`, `Tiers`, `Themes`, `SlayerFamilies`, `Leads`, `Areas`, `Appraiser`; `BuildDefaults :215`, `TierFor`, `GateFor`, `ThemesFor`, `AreasFor`, `LeadChancePercent`, `ExtraRollPercent`; `Parse`/`Validate :419` (refused whole), `LoadOrWriteDefaults`, `Reload` |
| `C\Requisitions\RequisitionItems.cs` (new, 454 lines) | `RequisitionCategories` (16 kinds: any, weapon, sword, mace, fencing, axe, bow, armor, leatherArmor, metalArmor, shield, jewelry, spellbook, necrobook, hat, instrument; each a test and a maker); `RequisitionProperties` (`TryRead`, `IntensityOf`, `PropertyCount`, `TotalIntensity`, `HasSlayer` with the group's super, `SetAtLeast`); `RequisitionMatch.Check` (the reasons in the player's words); `AppraiserPricing` (`Price`, `Explain`); `RequisitionItemFactory.Create` (the Lead's drop) |
| `C\Requisitions\RequisitionSystem.cs` (new, 392 lines) | `ClusterFRequisitions`: `DayIndex`, `NextRefresh`, `DataOf`, `EnsureCurrent`, `Open`, `TierFor`, `Refresh` (keeps live-Lead requests, fills to 3 per guild), `Make`, `TurnIn` (consume, pay, take down), `GiveGold`, `FirstMatch`, `Describe`, `PayText`, `TierName`, `Lines`; the `HuntFamily` seam; `Chance` and `Clock` (swapped by the facts); `[requisitions` and `[RequisitionsStaff reload|reroll|show`; `Configure` at `CallPriority(110)` (after the catalogue's 100) |
| `C\Requisitions\RequisitionLeads.cs` (new, 277 lines) | `IRequisitionLeadSource` and `Sources`; `TryRoll`, `Attach`, `Sweep`; `Qualifies` (`:166-187`: at the death event the creature is already deleted, pinned `Mobile.cs:4899-4902` before `BaseCreature.cs:3669`, so the kill's map and place are the corpse's), `DropChancePercent`, `KillerOf` (a pet's master counts), `OnCreatureDeath` (`[OnEvent(CreatureDeathEvent)]`), `HandleKill` (count, roll, make, deliver to the corpse); the family nouns |
| `C\Requisitions\RequisitionsBoard.cs` (new, 339 lines) | `RequisitionsBoard` item (0x1E5E; `GuildKey` command property, empty = League view; `OpenFor`, `Guilds`, `CanTurnInHere`); `RequisitionsBoardGump` (one guild per page, 3 rows: tier, request, Turn in, pay, lead; Previous/Next guild on the League view; a guild's own view shows that guild whatever page it was opened on, `:168-175`); `RequisitionTurnInTarget` |
| `C\Requisitions\Appraiser.cs` (new, 451 lines) | `Appraiser` NPC (invulnerable, Talk, double-click, drag-drop quote; `Sell`); `AppraiserGump` (Appraise, Sell, Which requisition wants this, the board; the quote with Sell/Keep); `AppraiserTarget`; `ClusterFRequisitionSeeder` (`AppraiserPosts`, `OfficeBoard`, `Seed` on world load and `[ClusterFSeedRequisitions`, `Fit` by `Map.CanFit` with a 2-tile fallback) |
| `C\ClusterFAccountData.cs` | v20: `_requisitionData` and `GetOrCreateRequisitionData`/`GetRequisitionData`/`RequisitionDataCount`/`ClearRequisitionData` after the loot records (`:197-213`); the reader's v20 block after v19 (`:440-450`); `CurrentVersion = 20` (`:485`); the writer's tail (`:588-594`) |
| `C\ClusterFGuildSystem.cs` | `GuildTaskDetailGump.BtnRequisitions = 9` (`:1048`); the bottom-row **Requisitions** button when the guild has theme rows (`:1183-1189`); its case opens the guild's view (`:1243-1245`) |
| `C\LeagueRegistrarGump.cs` | `BtnRequisitions = 26` (`:40`); the **Requisitions board** entry on the League Rank row's right (`:135`); its case opens the League view (`:420-422`) |
| `C\ClusterFDevTools.cs` | the test wipe's guild option also clears the requisitions (`:155`) |
| `server\tests\Misc\RequisitionsVerification.cs` (new, 788 lines) | the 12 facts (`GoldIn` at `:149-158` sums the pooled `FindItemsByType` enumerator with a loop: LINQ on it does not compile) |
| `server\tests\Misc\AccountDataSerializerVerification.cs:590-592, :652-655, :694-696` | the three "written again it is the current version" facts read 20 (they read 19 since cc-P80) |
| `CHANGELOG.md`, `VERSION` | 2026.10.19.6: the board, the Appraiser, Leads, `[requisitions`; staff: the table, the commands, the seeder |

### D:\UO\shard-migration

This file.

## The rules, as built

### Storage: per character

Requests are **per character** (the prompt's "rolled per character (or account, match how guild standing is stored and
say which)"): guild standing is per character since cc-P18 (`CharacterGuildData`), the tier reads it, so the record is
keyed the same way: `ClusterFAccountData._requisitionData[serial]`, v20, append-only after v19's tutorial record. A
save from before v20 loads with no record; a character rolls its first set when it next reads a board.

### The roll and the refresh

- The **refresh day** is `DayIndex(now) = floor((now - 05:00 UTC offset - 2026-01-01) in days)`. The set is rolled
  lazily: whenever a board, a turn-in, `[requisitions` or the Appraiser's "who wants this" reads it and the day has
  turned. No timer. `[RequisitionsStaff reroll` forces one.
- At a refresh every open request **without a live Lead** is dropped and each guild with theme rows is filled back to
  **3** (`perGuild`). A request **with a live Lead is kept** (its slot is not refilled until it goes). A filled request's
  slot stays empty until the next refresh: "3 per guild" is also "3 fills per guild per day".
- **Tier** = min(the character's rank index in that guild (`GuildRankIndex`, 0 Initiate to 5 top; **0 outside the
  guild**), the League gate for the character's League rank). Unregistered: gate 0.
- A theme row names an item kind and either a property (kind **Property**: the tier's minimum intensity and minimum
  property count apply), a slayer family (kind **Slayer**: the family, or "any", which asks `HuntFamily` first and then
  draws from `slayerFamilies`), or neither (kind **AnyMagic**: "no questions asked", the tier's property count).
- Pay is the tier row's Renown and standing; gold is the Appraiser's price of the item at turn-in.

### Turn-in

`ClusterFRequisitions.TurnIn`: the request must still be open (a stale gump after a refresh is refused with "taken
down"); the item must be in the backpack, not blessed, of the kind, and meet the kind's test:
- Property: has the property, `IntensityOf >= MinIntensity` (percent of the catalogue row's Full value; a boolean row is
  100 when on), `PropertyCount >= MinProperties`.
- Slayer: `Slayer` or `Slayer2` is the family **or its group's super slayer** (Repond fills an orc request; Silver is
  itself the undead super).
- AnyMagic: `PropertyCount >= MinProperties`.
Then: `GrantRenown(Renown, LeagueJob)` (counts toward League rank), `AddReputation(guild, standing)` **whether or not
the character is in the guild** (nothing banks for non-members anywhere yet, cc-P47 4.2; see decision 3), gold into the
backpack in piles of at most 60,000 as pinned's shopkeepers pay, the item deleted, the request removed.

Property reading: a weapon, armour piece (shields included), jewel or clothing piece goes through the catalogue
(`ImbueCatalogue.ForItem`, `def.Get`); a **spellbook**, which the catalogue does not cover, is read through its
`AosAttributes` by name (21 rows mapped in `RequisitionProperties.AosByName`), its skill bonuses and slayers counted; an
instrument has only slayers. `PropertyCount` is the catalogue's `CountActiveProperties` for catalogue items.

### The Appraiser's price

    price = base(kind) + perProperty x count + perIntensityPoint x totalIntensity, capped at max; 0 when count is 0

Defaults: base weapon 25, ranged 20, armour 40, shield 30, jewelry 13, spellbook 9, instrument 10, clothing 8, other 10
(near the SBInfo sell prices listed above); perProperty **25**; perIntensityPoint **0.5** (intensity is the sum over
properties of value / Full x 100, the Clean Up weight); max **500**. Examples: a longsword with Hit Chance 15 (33% of 45)
pays 25 + 25 + 16 = **66**; one with five properties at their Full values 25 + 125 + 250 = **400**; a spellbook with
Lower Mana Cost 8 (20% of 40) 9 + 25 + 10 = **44**. A shopkeeper pays 27 for any longsword. The same formula is the
board's gold pay, so a requisition never loses to plain selling (F-47).

### Leads

- **Chance a new request carries a Lead**, by League band (the gate tier 0-5): 10, 15, 20, 25, 30, 35 percent.
- **Where:** a registered source's pick first (`RequisitionLeads.Sources`, none registered today), else a random area
  the League rank may go to (`areas[].minLeagueRank`) that lists the request's slayer family (a slayer request) or any
  area (other kinds; the group is one of the area's). Held **3 days** from the roll.
- **Qualifying kill** (`Qualifies`): a creature that is not controlled or summoned, with **Fame >= 1,000**
  (`qualifyingFameMin`), whose region `IsPartOf` one of the area's region names (so "Despise Passage" counts for
  Despise, and the facet is free unless the area names one), and whose type the group's slayer entry `Slays` (or group
  "any"). The killer is `LastKiller`, or a pet's master.
- **Chance on the k-th qualifying kill:** `extra + (100 - extra) x (k - 1) / (pityKills - 1)`, with `extra` the
  creature's fame band's percent (0-999: 2; 1,000-4,999: 5; 5,000-14,999: 10; 15,000+: 20) and `pityKills` **40**, so
  kill 1 is the extra roll alone and kill 40 is 100 percent. A drop resets the count; the Lead runs on to its expiry.
- **The drop** (`RequisitionItemFactory.Create`): a random item of the request's kind (pinned's `Loot` lists filtered by
  base class; the armour sub-kinds from small type lists), `BaseRunicTool.ApplyAttributesTo` with the request's property
  count and its minimum intensity as the floor, then the asked property raised to at least the floor (`SetAtLeast`, a
  random value from the floor to Full), or the slayer set, and plain fillers (Luck, stats) until the count is met. It
  goes into the corpse, or the backpack when there is none, with one line to the player. No tag.
- **Expiry** clears the Lead's four fields and nothing else; the request then rolls over at the next refresh.

**Why the fame floor instead of "whose loot can roll that item type":** pinned's creatures call `AddLoot(LootPack.X)`
in their constructors and the pack generates at once (`LootPack.Generate`, `LootPack.cs:120-150`); nothing on the live
creature says which pack it had. And every AOS pack from Poor up lists the same five kinds (weapon, ranged, armour,
shield, jewelry; `LootPack.cs:179-258`), only the chances differ (Poor 0.02%, Meager 1%, Average 5%, Rich 20%, Filthy
Rich 33%). So "can roll a sword" is true of nearly everything and the real question is "how likely", which is what the
fame band's `extra` encodes. Chase can move the floor and the bands in the table.

### The hall hook (F-49)

A real hall shows the guild's view with `RequisitionsBoard.OpenFor(pm, guildKey)` from any gump, or by placing
`[add RequisitionsBoard <guildKey>` (the League view with no key). Turn-ins there work once the hall has a board
covering the guild or its guildmaster within 8 tiles (`CanTurnInHere`).

## The data tables and every number picked (Chase tunes them in `Configuration\requisitions.json`)

**League gate** (the highest tier a League rank allows): rank 0 (unregistered) 0; Iron (1) 1; Bronze (5) 2; Verite (8)
3; Toxic (11) 4; Obsidian (14) 5. The bands follow the cc-P48 ladder's guild-rank bands.

**Tiers** (by the rank index in the guild, capped by the gate):

| Tier | Guild rank | Min intensity (% of Full) | Min properties | Renown | Standing |
|---|---|---|---|---|---|
| 0 | Initiate (or not a member) | 20 | 1 | 10 | 40 |
| 1 | Apprentice | 30 | 1 | 20 | 60 |
| 2 | Journeyman | 40 | 2 | 35 | 90 |
| 3 | Master | 55 | 2 | 55 | 130 |
| 4 | Grandmaster | 70 | 3 | 80 | 180 |
| 5 | top rank | 85 | 3 | 110 | 250 |

For scale: a Smith commission pays 80 to 1,440 standing a piece (cc-P46), Apprentice is 1,000 standing and Master
15,000; the League ladder's Bronze is 2,500 lifetime Renown and Celestial 110,000 (cc-P48). At most 3 fills per guild
per day.

**Themes** (76 rows; weight in brackets; a row with no property is "anything magic"):

| Guild | Rows |
|---|---|
| Warriors' Brotherhood | sword + Hit Chance Increase (3), mace + Hit Lightning (2), sword + Hit Lower Defense (2), mace + Hit Fireball (1), sword slayer any (2), mace slayer Repond (1), shield + Defense Chance Increase (1) |
| Arcane Society | spellbook + Lower Mana Cost (3), jewelry + Lower Mana Cost (2), jewelry + Faster Cast Recovery (2), spellbook + Spell Damage Increase (2), jewelry + Lower Reagent Cost (1), spellbook + Faster Casting (1) |
| Healers' Covenant | armor + Hit Points Regen (3), jewelry + Enhance Potions (2), armor + Poison Resist Bonus (1), jewelry + Bonus Intelligence (1) |
| Order of the Alembic | jewelry + Enhance Potions (3), armor + Poison Resist Bonus (2), jewelry + Bonus Intelligence (1), hat + Luck (1) |
| Rangers' League | bow + Hit Chance Increase (3), bow + Hit Lower Defense (2), bow slayer any (2), leather armor + Stamina Regen (1), bow + Velocity (1) |
| Miners' Compact | armor + Bonus Strength (3), armor + Lower Stat Req (Armor) (2), jewelry + Bonus Strength (2), weapon + Durability (Weapon) (1) |
| Society of Smiths | metal armor + Physical Resist Bonus (3), armor + Durability (Armor) (2), sword + Durability (Weapon) (1), shield + Defense Chance Increase (2) |
| Tinkers' Union | jewelry + Bonus Dexterity (3), jewelry + Luck (2), jewelry + Defense Chance Increase (2), jewelry + Night Sight (1) |
| Thieves' Den | any magic item, no questions asked (3), jewelry + Bonus Dexterity (2), fencing + Hit Lower Attack (2), leather armor + Night Sight (1) |
| Twin Paths Dojo | sword + Swing Speed Increase (3), fencing + Hit Stamina Leech (2), armor + Stamina Regen (1), sword + Hit Lightning (1) |
| Keepers of the Last Door | necromancer spellbook + Spell Damage Increase (3), jewelry + Spell Damage Increase (2), jewelry + Lower Mana Cost (1), weapon slayer Silver (2), weapon slayer Exorcism (1) |
| Foresters' Union | axe + Hit Chance Increase (3), axe + Damage Increase (2), bow + Damage Increase (1), armor + Lower Stat Req (Armor) (1) |
| Tailors' Circle | leather armor + Mana Regen (3), leather armor + Fire Resist Bonus (2), hat + Luck (2), leather armor + Lower Mana Cost (1) |
| Maritime Brotherhood | armor + Cold Resist Bonus (2), jewelry + Luck (2), fencing + Hit Lightning (2), armor + Energy Resist Bonus (1), weapon slayer Reptilian Death (1) |
| Merchants' Exchange | jewelry + Luck (3), any + Luck (2), armor + Hit Point Increase (1), jewelry + Lower Reagent Cost (1) |
| Bards' Consortium | instrument slayer any (4), jewelry + Bonus Intelligence (2), armor + Mana Regen (1), jewelry + Mana Increase (1) |
| Artificers' Order | any magic item, for unravelling (3), jewelry + Faster Casting (2), armor + Mage Armor (1), weapon + Spell Channeling (1) |
| The Custodians | none (F-47) |

Property names are the Artificers' catalogue's rows; a row the catalogue does not know is refused at load. The "any"
slayer families: Silver, Repond, Reptilian Death, Exorcism, Arachnid Doom, Elemental Ban, Fey, Dragon Slaying, Orc
Slaying, Troll Slaughter, Ogre Thrashing, Terathan, Ophidian.

**Leads:** days 3; pity kills 40; qualifying fame floor 1,000; Lead chance by band 10/15/20/25/30/35; extra roll by
fame 2/5/10/20 (at 0 / 1,000 / 5,000 / 15,000).

**Areas** (key: shown name; regions; groups; League rank to unlock): graveyard: the Britain Graveyard; Silver; 0.
rootdeep: the Rootdeep Burrows; any; 0. despise: Despise, Despise Passage; Repond, Reptilian Death, Ogre Thrashing; 0.
orccave: the Orc Cave; Orc Slaying, Repond; 0. covetous: Silver, Repond; 1. deceit: Silver; 1. shame: Elemental Ban,
Earth Shatter; 1. wrong: Repond, Orc Slaying; 1. orcfort: the Orc Fortress; Orc Slaying; 2. destard: Dragon Slaying,
Reptilian Death; 5. hythloth: Exorcism, Daemon Dismissal; 5. ice: Elemental Ban, Summer Wind; 5. fire: Exorcism, Flame
Dousing; 5. terathan: Terathan Keep; Terathan, Arachnid Doom; 5. khaldun: Silver; 8. doom: Exorcism, Silver; 11.
Region names are pinned's `regions.json` and ours; whether each is loaded on the live worlds is not checked here (a Lead
to an unloaded region never qualifies a kill, and the pity never moves: a thing to watch in play).

**Appraiser:** the bases, 25 per property, 0.5 per intensity point, cap 500 (above).

**Appraiser posts** (`ClusterFRequisitionSeeder.AppraiserPosts`; Trammel tiles probed standable with the cc-P15 CanFit
port, `notes\cc-P77-tools\probe.py`; the two others taken from the Banker spawners in pinned's `Spawns` data and left
to `Map.CanFit` at seed time, with a 2-tile fallback and a console line if nothing fits):

| Town | Where | Facet | x, y, z |
|---|---|---|---|
| New Haven | League field office, east wall | Trammel | 3461, 2599, 18 |
| Britain | outside the West Bank, south door | Trammel | 1426, 1694, 0 |
| Trinsic | by the bank | Trammel | 1900, 2685, 10 |
| Minoc | by the bank | Trammel | 2505, 554, 0 |
| Vesper | by the bank | Trammel | 2883, 686, 0 |
| Moonglow | by the bank | Trammel | 4473, 1158, 0 |
| Skara Brae | by the bank | Trammel | 586, 2148, 0 |
| Luna | by the bank | Malas | 992, 523, -50 (not probed) |
| Royal City | by the bank | Ter Mur | 838, 3439, -20 (not probed) |

The office's League board: 3459, 2596, 18 (the north wall, beside the flowerpot of `ClusterFRegistrarOfficeLayout`).

## Deviation (the register; the register ends at D-122 in `docs\fidelity-principle.md`, D-123 to D-130 are proposed in cc-P66, P67 and P71; next free D-131)

| D-131 | **Ours (cc-P150, F-47 and F-48, Chase 2026-10-16).** The League of Extraordinary Citizens runs a requisitions board: each guild posts three requests a day per character for a magic item (a kind with a property at a minimum intensity, a slayer family, or anything magic with enough properties), rolled from a per-guild theme table at the character's rank in that guild and capped by League rank; a turn-in consumes the item and pays Renown, that guild's standing and gold at the Appraiser's price; an unfilled request rolls over with no penalty. The Appraiser, a League NPC in the New Haven field office and eight bank towns, buys any magic item by property count and intensity near stock sell levels (floor 25-40 gold a kind, 25 a property, half a gold an intensity point, cap 500). Leads: a request may carry a three-day rumor naming an area and a creature group; a qualifying kill there (fame 1,000 and up, of the group, in the area) gets an extra roll at the fame band's chance and the item is certain by the 40th such kill. OSI: none of this exists; shopkeepers pay a magic item's plain price and no NPC wants loot | wiki: the board, the Appraiser's price, Leads | `visible` | `cc-P150` |

## Tests

`server\tests\Misc\RequisitionsVerification.cs`, 12 facts (the file's header lists them). Four `build.sh` cycles on the
resume, all through the gate (`docker/uo/build.sh -t sl-modernuo:cc-P150`, `--tests-only` for the first three), with
the docker-build lock held and released after; logs in the session scratchpad (`p150-green1.log`, `p150-green2.log`,
`p150-red7.log`, `p150-final.log`).

| Build | Tree | Result |
|---|---|---|
| 1 | the saved branch as restored | builder stage red: one compile error, `RequisitionsVerification.cs(149)` CS0411 (LINQ `Sum` over pinned's pooled `FindItemsByType` enumerator). Fixed with a loop, as `RecipeGatingVerification.cs:112` notes. The customizations compiled clean. |
| 2 (the red cycle) | the saved branch, which held the **red tree**: every break of `p150-red.py` except the kind-check one for facts 6 and 7 was in the files the overseer saved | 1,561 tests, **14 failed**: 11 of the 12 facts, each by its break (table below), and the three `AccountDataSerializerVerification` version facts (they asserted 19; the record is v20 now). Fact 7 passed: the kind-check break does not reach the slayer branch. |
| 3 (fact 7's red) | the real tree (breaks reversed by `p150-unred.py`), the version facts on 20, and one break for fact 7 alone: `Satisfies` in `RequisitionProperties` returned true for any slayer (the super-slayer rule gone) | **3 failed**: fact 7 ("Assert.False: a Silver sword taken for an orc request"), and two facts the saved breaks had hidden: fact 12 (the warriors' board view listed the Society of Smiths) and fact 9 (the 40th kill through the real death event put nothing in the corpse). Both real defects, fixed (next row). |
| 4 (final) | the real tree with the two fixes | **green: 1,561 tests, 1,557 passed, 4 skipped, 0 failed**; the runtime image `sl-modernuo:cc-P150` built (label sl.commit=453735e, dirty, as the branch is uncommitted). |

How each fact went red (build 2 unless said; the reason is the break's, read from the failure message):

| Fact | Break | Red seen as |
|---|---|---|
| 1 the table | `Validate` skipped the property check | "Assert.Null failure": the misspelt file was accepted and became the table |
| 2 the roll | `Refresh` filled to `perGuild - 1` | 34 requests, not 51 |
| 3 the tier | `TierFor` ignored the League gate | tier 2 where the gate says 0 |
| 4 the refresh | `Refresh` rolled on every read | the ids an hour later were all new |
| 5 the pay | double Renown, and a Renown loss on every refresh; the refresh-on-read break hit first | "That request has been taken down; the board has refreshed" |
| 6 refusals | the kind check gone; the refresh-on-read break hit first | the wrong-kind reason was the taken-down line, not "a sword" |
| 7 slayers | (build 3) `Satisfies` returned true for any slayer | a Silver sword was taken for an orc request |
| 8 the Appraiser | double gold per property | 91 gold, not 66 |
| 9 Leads | `DropChancePercent` never reached 100 | 5 percent at the 40th kill, not 100 |
| 10 quiet expiry | a Renown loss on every refresh; the perGuild - 1 break hit first | 34 requests, not 51 |
| 11 the save | the pity count written as 0 | the round trip read `LeadKills` 0 for 7 |
| 12 the board | any board covered any guild; the perGuild - 1 break hit first | 2 "Turn in" buttons, not 3 |

Facts 5, 6, 10 and 12 were red by an earlier break in the same tree rather than their own; each is still a fact seen
failing on its own assertion. The two defects build 3 found are the kind the saved breaks masked: fact 12's own break
(any board covers any guild) sat behind the gump defect, and fact 9's pity break stopped the fact before the death event.

The defects, for the record:

- **A guild's board view ignored its guild** (`RequisitionsBoardGump`): the page argument chose the guild, so the
  Society of Smiths (first in the registry) opened from every guildmaster's Requisitions button and from
  `OpenFor(pm, guildKey)` when the caller's page was 0. Now a guild key fixes the page to that guild
  (`RequisitionsBoard.cs:168-175`); the League view pages as before.
- **A Lead never dropped through the real death event** (`RequisitionLeads.Qualifies`): pinned's `Mobile.OnDeath`
  deletes a non-player mobile (`Mobile.cs:4899-4902`) before `BaseCreature.OnDeath` raises `CreatureDeathEvent`
  (`BaseCreature.cs:3669`), so the handler saw a deleted creature on the internal map and said "nowhere". The kill's map
  and place are now read from the corpse when the creature is gone (`RequisitionLeads.cs:166-187`); the corpse is set
  by pinned's corpse handler before `OnDeath` runs (`Corpse.cs:619`), and `LastKiller` is untouched by death
  (`Mobile.cs:6018` is its only writer). The 39 direct `HandleKill` calls of the fact had passed because the creature
  was alive; only the 40th went through the event.

## Deviations and decisions for Chase

1. **Per character.** Requests are per character because guild standing is per character (cc-P18); the tier reads it.
2. **A non-member sees and may fill a guild's requests at tier 0**, and the standing is paid into that guild's record
   at once, as the three member-tool sites and Imbuing do today (F-24's "banked until they join" has no code yet, cc-P47
   4.2). When banking is built, `TurnIn` is the one place to route it through. Say if non-members should instead see
   only the guilds they are in.
3. **A request with a live Lead survives the daily refresh** until the Lead lapses (up to 3 days), so "a Lead always
   pays off" holds against "requests refresh daily"; everything else rolls over. The slot is not refilled while it waits.
4. **Qualifying kill = the fame floor (1,000), the group and the area**, not "whose loot table can roll that item type"
   (reasoned above). The floor is in the table.
5. **The "2x" is one extra roll at the fame band's chance** (2/5/10/20 percent), which is the shape pinned's packs
   give a magic item of one kind; the holder's natural roll is untouched. The pity ramps linearly to 100 at kill 40.
6. **The refresh is 05:00 UTC** (`refreshHourUtc`), before the US morning; lazily applied, so no timer and no load-time
   sweep.
7. **Infamy does not exist** (F-37 says to build it later; nothing in `C\` carries the name, checked by a fact), so
   "no Infamy" is true by construction; when it exists, requisitions must stay out of it.
8. **Clean Up Britannia:** an item turned in here is consumed, so it cannot also be dropped in a Clean Up barrel, and the
   turn-in pays no Clean Up points: one exit per item, as proposed in F-47.
9. **The loot rater's "Requisition" tier is server-ready, not script-done.** `[requisitions` prints the lines; the
   script (`SL_Combat_Rater.py` in `D:\UO\sl-scripts`) is not on this desk (the Golem's work copies are the two repos),
   so it is not changed. The exact change is under "For Chase".
10. **Luna and Royal City tiles are not probed:** the CanFit port reads Trammel only and the vseUOAware inspector
    returned no statics for Malas (land only), so those two posts are the Banker spawner tiles, offset two tiles, and
    the seeder checks `CanFit` and tries the map's z and a 2-tile ring before giving up with a console line. Check both
    in a client (`[ClusterFSeedRequisitions` reports what it did).
11. **The office board sits on the wall tile** (3459, 2596, 18), the usual place for a bulletin board; if TazUO draws
    it badly there, move it to 3459, 2597 (the floor tile beside the flowerpot) with `[props`.
12. **VERSION** went to 2026.10.19.6 on the resume (2026.10.19.5 is cc-P191's section, finished earlier the same
    evening on this desk). The P150 branch is based before P191's commit, so the integrator's merge of `CHANGELOG.md`
    will see both sections added at the top; keep both, 2026.10.19.6 above 2026.10.19.5.
13. **The Read tool was denied** for `D:\ShatteredLegacy\docker\uo\build.sh` (an unattended run auto-denies) in the
    first run; the resume read it with `cat` under the docker-build lock, as the hook asks. The usage is
    `docker/uo/build.sh [-t IMAGE_TAG] [--tests-only]`.
14. **No task-list tool** exists in this session; the steps were ticked at the top of this file instead.
15. **The first run's red build was killed (low system memory) and not restarted; the resume ran the gate.** Four
    foreground cycles of about three minutes each; free memory was 1.7 GB at the start with Docker's WSL VM holding
    12 GB from the evening's earlier builds, and nothing was killed. The branch the overseer saved held the red tree,
    not the real one (the 14:45 note said the opposite); the resume's reverse script (`p150-unred.py`, the red script's
    pairs swapped) restored it, and `git diff` against the saved branch shows exactly the reversed breaks plus the
    three fixes above.
16. **Two defects shipped in the 14:45 code and were caught only by the gate** (the board view's guild, the Lead's
    death-event delivery). Both are the kind a probe finds and a read does not; noted here so the pattern is on record.

## For Chase

Test shard, after a restart with this build (the seeder places everything at world load; `[ClusterFSeedRequisitions`
re-runs it and reports):

1. **The board.** Walk into the field office (3459, 2601). A bulletin board hangs on the north wall; double-click it.
   The League view opens on the first guild you are in: three requests, each with a tier, the item asked for, the pay
   and a Lead line; Previous/Next guild pages through 17 guilds. `[requisitions` prints the same as `[Requisition]`
   lines.
2. **A guild's view.** Talk to any guildmaster in New Haven: the hall page has a **Requisitions** button at the bottom
   (not for the Sanitation Warden). The Registrar's menu has **Requisitions board** beside League Rank.
3. **A turn-in.** `[RequisitionsStaff show` lists your requests; make an item that fits one (for example `[add
   Longsword`, then `[props` it and set `Attributes.AttackChance 20`), stand at the board, press **Turn in**, target it:
   "Requisition filled ... Paid N Renown, N standing and N gold". The slot stays empty; `[RequisitionsStaff reroll`
   rolls a new set at once.
4. **Tiers.** `[props` yourself, set `LeagueRank` 8, join a guild and raise its standing (`[guildstanding` or the dev
   tools), `[RequisitionsStaff reroll`: that guild's requests read Journeyman or Master tier with higher pay.
5. **The Appraiser.** The clerk stands by the office's east wall and at the eight banks. Drop a magic item on them: a
   quote with the formula and **Sell for N gold** / Keep; a plain item: "no magic properties: a shopkeeper will buy it".
   Double-click for Appraise, Sell, "Which requisition wants this?" and the board.
6. **A Lead.** `[RequisitionsStaff show` until a line ends with an area (or set one by hand: `[props` cannot reach the
   record; reroll a few times, the chance is 10% a request at Iron). Go there (the Britain Graveyard for undead at rank
   0), kill the named creatures: each qualifying kill counts, and the item is in a corpse by the 40th at the latest, with
   "The rumor held: ...". A Lead line shows days left and kills so far.
7. **Quiet expiry.** Leave a set unfilled past 05:00 UTC: `[props` your account record is unchanged (Renown, standing);
   the board shows new requests.
8. **The table.** `Configuration\requisitions.json` after the first start; edit a number, `[RequisitionsStaff reload`;
   a typo in a property name is refused with the row named and the old table kept.
9. **The rater's "Requisition" tier** (the script change, two parts, in `D:\UO\sl-scripts\SL_Combat_Rater.py`): send
   `[requisitions` where `request_rank` sends `[artificerrank` and parse the journal lines
   `[Requisition] <guild>|<kind>|<category>|<property or slayer:<Name> or ->|<minIntensity>|<minProperties>|<tier>|<renown>|<standing>|<lead or ->`
   up to `[Requisition] end` (the header line starts `[Requisition] N open`); then in `tier_for`, before every other
   tier, return "Requisition" when the item's kind matches `category` (the kinds are the board's keys: any, weapon,
   sword, mace, fencing, axe, bow, armor, leatherArmor, metalArmor, shield, jewelry, spellbook, necrobook, hat,
   instrument) and the parsed property's intensity (value / the rater's max x 100) is at or above `minIntensity`, or the
   slayer name matches, or `kind` is AnyMagic and the property count is at or above `minProperties`. The server already
   answers the same question for one item: `ClusterFRequisitions.FirstMatch(pm, item)`; a `[requisitionmatch` command
   over a targeted item is a ten-line follow-up if the script would rather ask than parse.
10. Not verified in a client: the gump layouts (the board's rows, the Appraiser's quote), the board's art on the wall
    tile, the two unprobed posts. Add to the client-check list.

## Repo size rule

No new file is over 5 MB; the largest new file is the test (about 40 KB). Nothing large was written to either repo;
scratch (the pristine copies and the build logs) is in the session scratchpad outside both.

## Commit preflight

Run on the resume, 2026-10-19, against the Bronze work copies (`-CodeRepo D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo
D:\UO\golems\Bronze\shard-migration -NoRefresh`; the script's defaults are the main checkouts, where other Golems' work is
pending). Neither repo BLOCKED. No file over 5 MB in either repo (`find -size +5M`: none). The docker-build lock was taken
for the four cycles and released; no other lock was needed.

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  15 file(s) pending:
    CHANGELOG.md
    VERSION
    server/customizations/ClusterFAccountData.cs
    server/customizations/ClusterFDevTools.cs
    server/customizations/ClusterFGuildSystem.cs
    server/customizations/LeagueRegistrarGump.cs
    server/tests/Misc/AccountDataSerializerVerification.cs
    server/customizations/Requisitions/Appraiser.cs
    server/customizations/Requisitions/RequisitionData.cs
    server/customizations/Requisitions/RequisitionItems.cs
    server/customizations/Requisitions/RequisitionLeads.cs
    server/customizations/Requisitions/RequisitionSystem.cs
    server/customizations/Requisitions/RequisitionTable.cs
    server/customizations/Requisitions/RequisitionsBoard.cs
    server/tests/Misc/RequisitionsVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  1 file(s) pending:
    notes/cc-P150-requisitions-and-leads.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

P150 DONE
