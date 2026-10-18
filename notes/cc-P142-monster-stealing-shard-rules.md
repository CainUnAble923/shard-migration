# cc-P142: Monster stealing, our rules on top of P127's faithful port

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P142-monster-stealing-shard-rules.md` (Chase's answers of 2026-10-16 06:58
and 07:00, the overseer's 10-16 08:02 addition). P127 is DONE and committed (its notes end `P127 DONE`). Both repos
were clean at the start apart from the overnight bot's `testing/bot-runs/2026-10-18-0130/` and the importer's files
(machine output). Model: Fable. Not committed: the Golem commits after DONE. Scratch: the session scratchpad (the
build logs, the break script and its clean copies with hashes); nothing of it is in either repo.

**Second hand-off, 2026-10-18 (the overseer's 05:55 change):** the first session stopped one build short (low memory);
this one carries Chase's 05:51 decision, "stealing from monsters in Burrow warrens needs to be sooner in thieves guild.
it is the tutorial dungeon", through the code, the facts (red first), these notes and the patch notes, then the gate.
What moved is in the section "The second hand-off" below; the headlines and tables read as the rules now are.

## Headlines

1. **P127's port stays the base; every one of Chase's rules sits on top of it in three new files beside
   `StealingHandler.cs`**, and OSI's rule is kept next to ours wherever it changed (ServUO's chance table is still in the
   code as `GetServUOStealingChance`, for the register and a fact). The hook in pinned `Stealing.cs` is unchanged; no new
   patch.
2. **Where and who (decision 1):** monster stealing needs the Thieves' Den. The ladder uses the Den's own rank names
   (the generic ladder): an **Initiate** (any member) works OSI's places, Felucca's dungeons and champion spawns on any
   facet, **and the Rootdeep Burrows outside the Vault, the tutorial dungeon** (Chase, 10-18 05:51; it was Master in
   the first hand-off); a **Journeyman** (5,000 standing) every facet's dungeons; a **Master** (15,000) the shard's own
   later dungeons (`ShardDungeonRegionTypes`, empty today) and bosses anywhere, the Burrows' named bosses among them (The
   Burrow Mother, The Gloom Queen). Too low a rank in a covered place hears "The Den does not trust an Apprentice to
   work the dungeons beyond Felucca. Come back a Journeyman."; a non-member hears "Only a hand sworn to the Thieves'
   Den knows where a monster keeps its treasures."; outside every covered place nothing is said, as OSI says nothing.
   Never: a pet, a summon (OSI's), a tutorial creature, the pack mule, anything standing in the Vault, a creature
   already stolen from.
3. **The odds (decision 2) run to 200:** 5% at 100, 11 at 120, 23 at 160, 35 at 200 (0.30 a point), OSI's fame bonus
   (1 to 5) on top, so the most famous creature at 200 is 40%. **The lower tier (decision 3)** starts at 60: 2% at 60 to
   5% at 100 (0.075 a point), a minor table only (coin, Den scrip, lockpicks, small potions, bandages), never an OSI
   special. The curve is a fact at 60, 80, 100, 120, 160 and 200, weak and famous.
4. **One success per creature (decision 3a):** a miss leaves the creature open after a 5-second per-creature cooldown
   ("The creature is wary of your hands. Give it a moment." inside it), reveals the thief and makes the creature attack
   them ("The creature catches your hand in its hoard and turns on you!"). A success marks the creature and OSI's "nothing
   left to steal" line follows from then on.
5. **New loot (decision 4), on one draw from 100:** 1% a loop scroll fragment, 4% a recipe scroll (three in four from the
   Den's own table, the fourth from every craft's Band V pool), 15% one of **five stolen-only components** (shadowsilk
   thread, ember ash; whisperleaf from fame level 10; thief's wire from 20; a lucky fang from 30), 80% OSI's special item
   as before. A Burrows creature gives one more of its family part at 10% on top of either tier. **Three Den recipes are
   built** (the recipe-gating system they need is cc-P78's, already in): the Shadowsilk Cloak (Tailoring, Stealth +5 and
   Hiding +3), the Thief's Smoke Bomb (Alchemy, hides on Hiding 50 where the stock bomb wants Ninjitsu 50) and the
   Pickpocket's Charm (Tinkering, Stealing +5 and Snooping +5), each a pinned-style own recipe (ids 9400 to 9402) so it
   never enters a guild's Band V rotation and is learned only from a scroll, which the steal is the source of. Two more
   are proposals (below): the Gilded Lockpick and Shadow Cloak IV.
6. **Skill gain (decision 5):** P127's gain-only roll stays and its window widens with the floor: (60, 100 + 2.5 x the
   creature's fame level) after every legal attempt, success or miss, so a weak creature trains to 100 and a 30,000-fame
   one to 200; through `ClusterFSkillGain`'s wrapped handlers, so the shard's rate, worn-bonus and cap rules apply.
7. **Saved state (decision 6):** the stolen flag and the Gem of Salvation timer now live in `MonsterStealingStore`, a
   side table in its own save file (`Saves/MonsterStealing`, pinned's `GenericPersistence`, the shape P121 and P130
   chose), so both outlive a restart and BaseCreature's and PlayerMobile's save formats are untouched. The prompt's
   "serialize it, with a version bump" is met by the store's own version; the BaseCreature patch it could have been is
   argued below and listed for Chase.
8. **The balm and the lotion (decision 6):** P127's note said ServUO calls their hooks from `AOS.Damage`; it does not.
   ServUO has four call sites, none in `AOS.Damage` (counted: `HarrowerTentacles.cs:245`, `MonstrousInterredGrizzle.cs:305`,
   `Regions/DamagingRegion.cs:181`, `Services/Pet Training/SpecialAbility.cs:2585`). One of the four is ours already,
   the pet-training Life Drain ability (`SpecialAbility.cs`, ported by P121), so the **Life Shield Lotion is wired there
   now** (a fact: 30 drains under it do less than half of 30 bare). The other three are pinned's Harrower tentacles (a
   patch) and two files pinned does not have (the Grizzle, damaging regions), so the **Balm of Protection still reduces
   nothing**: not a damage-hook question but a port question, listed for Chase with the hunk.
9. Tests: 10 new facts in `MonsterStealingShardRulesVerification.cs` and 3 of P127's rewritten, **every one seen red**
   in one deliberate break run (13 breaks, 6 files, restored byte-identical by hash), then green in build 2; the two
   Burrows facts rewritten for the second hand-off were **seen red against the old rule** (a filtered run on the builder
   image: both failed, the Burrows answering Master and `ShardDungeon`), then the gate: **1,440 tests, 1,436 passed, 0 failed, 4 skipped in build 6**, the 20 Monster Stealing facts among the passes (counted in the log). `CHANGELOG.md`
   **2026.10.18.3**, `VERSION` bumped. Play-test items P142-1 to P142-7 sorted (five BOT, one BOT-PARTIAL, one DEPLOY).

## What changed, with file:line

`D:\ShatteredLegacy`:

| File | What |
|---|---|
| `server/customizations/Services/Monster Stealing/Core/StealingHandler.cs` (rewritten, 298 lines) | the flow: already stolen (1094948), the never list (502708), place and rank (`ThievesDenStealRules.CheckPlaceAndRank`, the line in red), the floor, the retry cooldown, the roll, the two tiers, the family part, `SetStolen` on success only, `Miss` (cooldown, reveal, `AggressiveAction` + `Combatant`), the gain roll; `GetStealingChance` (ours, :231-244), `FameBonus` (:246-255), `GetServUOStealingChance` (OSI's, kept, :257-280), `FameLevel` and `GainCeiling` unchanged from P127; `Outcome`/`LastOutcome` for the facts; `Floor` 60, `SpecialFrom` 100, the slopes, `RetryCooldown` 5 s, the three lines |
| `.../Core/ThievesDenStealRules.cs` (new, 223 lines) | `StealPlace` (with `TutorialDungeon`), `PlaceOf` (tutorial dungeon :110, shard dungeon, champion spawn, dungeon by facet), `IsTutorialDungeon` (`TutorialDungeonRegionTypes` :61, the Burrows) and `IsShardDungeon` (`ShardDungeonRegionTypes` :67, empty today; both a parent walk), `RequiredRank` (:151-161, the tutorial dungeon at Initiate), `IsBoss` (:166-167, `ClusterFLootBoxes.IsBoss` or `ShardBossTypes` :74, the Burrows' named bosses), `IsNeverStolen`, `DenRank` (membership and `GuildRankIndex`), `RankName`, the lines, `CheckPlaceAndRank` |
| `.../Core/StealLootTables.cs` (new, 267 lines) | the minor weights and `MinorPick`, the special thresholds and `SpecialPick`, `GoldFor`, `GiveMinor` (scrip into the Den purse through `CharacterGuildData.AddCurrency`), `ComponentsFor` by fame level, `RecipeScroll` (the "thieves" reward table, the built-in `DenRecipeKeys` when a config file lacks it, the Band V pool), `OsiSpecial` (ServUO's `Random(Length - 2)`), `MakeSpecial`, `FamilyPartOf` and `TryFamilyPart` |
| `.../Core/MonsterStealingStore.cs` (new, 176 lines) | `GenericPersistence("MonsterStealing", 10)`, version 0: the stolen set and the gem timers, written as mobile references; deleted or expired entries dropped on save and on load; the creature- and player-deleted events; `Configure` once; `ClearForTests` |
| `.../Items/StolenComponents.cs` (new) | `StolenComponent` (stackable, 0.1 stones, a property line) and the five: `ShadowsilkThread` 0x0FA0 hue 0x455, `EmberAsh` 0x0F8C 0x4E7, `Whisperleaf` 0x0F88 0x48F, `ThiefsWire` 0x1876 0x8A5, `LuckyFang` 0x10E8 0x8A5 (placeholder art and hues, as the Burrows parts) |
| `.../Items/ThievesDenRecipeItems.cs` (new) | `ShadowsilkCloak : BaseCloak`, `PickpocketsCharm : BaseRing`, `ThiefsSmokeBomb : SmokeBomb` (pinned's `OnDoubleClick` line for line with Hiding 50 in place of Ninjitsu 50, `SmokeBomb.cs:20-24` at d4531cd9) |
| `.../Items/GemOfSalvation.cs` | `NextUse`/`SetNextUse` read and write the store (:34-36); the in-memory table is gone |
| `server/customizations/Engines/Craft/ThievesDenCraftRegistrations.cs` (new) | the three entries at ServerStarted (idempotent; the host calls `Register`), ids 9400 to 9402, min 100, max 130 |
| `server/customizations/Engines/Craft/ClusterFRecipeTable.cs:95-98` | the default `"thieves"` reward table (the three Den keys and the Shadow Cloak schematics I to III) |
| `server/customizations/Engines/Craft/ClusterFRecipeRewards.cs:30-31` | `RecipeRewardSource.Steal` (pays no epic table, like a quest) |
| `server/customizations/Services/Pet Training/SpecialAbility.cs:1594-1599` | the Life Shield Lotion asked before a Life Drain on a player (ServUO `SpecialAbility.cs:2582-2585`) |
| `server/tests/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs` (new, 10 facts) | below; facts 1 and 2 rewritten in the second hand-off for the Burrows at Initiate (:183-203, :280-288) |
| `server/tests/Services/Monster Stealing/MonsterStealingVerification.cs` | the fixture joins the Den; facts 1 to 3 rewritten for the shard's rules (ServUO's table through `GetServUOStealingChance`; place instead of `CheckLocation`; a success marks, below 60 nothing) |
| `CHANGELOG.md`, `VERSION` | section **2026.10.18.3** (four Added, two Changed, one Fixed); 2026.10.18.3 |

`D:\UO\shard-migration`: this note; `testing/playtest-steps.json` P142-1 to P142-7; `testing/bot-triage.md` group P142;
the importer's and the bot's machine output.

Nothing in `server/patches/` changed and `apply-patches.sh` is untouched: P127's `Stealing-monster-stealing.patch` is
the only hook and it still calls `StealingHandler.HandleSteal`.

## The rules, as built

### The ladder (decision 1)

| Den rank (index) | Standing | Opens |
|---|---|---|
| not a member | | nothing; the non-member line in any covered place |
| Initiate (0), Apprentice (1) | 0, 1,000 | OSI's places: a dungeon on Felucca, a champion spawn region on any facet; and the tutorial dungeon, the Rootdeep Burrows outside the Vault (`TutorialDungeonRegionTypes`: `OldHavenBurrowsRegion`; Chase 10-18 05:51) |
| Journeyman (2) | 5,000 | plus a dungeon on any other facet (any `DungeonRegion`: Trammel, Ilshenar, Malas, Tokuno, Ter Mur, Eodon) |
| Master (3) | 15,000 | plus the shard's own later dungeons (`ShardDungeonRegionTypes`, empty today; a later dungeon is added there, not to the tutorial set) and bosses anywhere (`ClusterFLootBoxes.IsBoss`: champions, the Harrower, peerless, the Despise bosses, the Shame guardian, Navrey, any `IRareSelfRepairSource`; not paragons; plus `ShardBossTypes`, The Burrow Mother and The Gloom Queen, which the loot boxes do not count as bosses) |
| Grandmaster (4), Legendary (5) | 50,000, 100,000 | nothing more (proposal for Chase below) |

`PlaceOf` answers one place per spot: the tutorial dungeon first, then a shard dungeon (the Burrows is also a stock
`DungeonRegion` on Trammel, so without that order it would be a Journeyman's facet dungeon and an Initiate would be
refused there), then a champion spawn, then a dungeon by facet. The Vault is a child of the Burrows and is on the never
list by the creature's region, so a thief of any rank standing in the Burrows cannot reach into it. The two sets are
kept apart on purpose: `TutorialDungeonRegionTypes` is the Initiate's, `ShardDungeonRegionTypes` the Master's, so a
later dungeon added to the second does not loosen the first.

### The curve (decisions 2 and 3), in percent

| Stealing | weak creature (fame 1) | fame level 25 (+1) | level 30 (+2) | level 35 (+3) | the most famous (level 40, +5) |
|---|---|---|---|---|---|
| below 60 | 0 | 0 | 0 | 0 | 0 |
| 60 | 2 | 3 | 4 | 5 | 7 |
| 80 | 3.5 | 4.5 | 5.5 | 6.5 | 8.5 |
| 99.9 | 4.99 | | | | 9.99 |
| 100 | 5 | 6 | 7 | 8 | 10 |
| 120 | 11 | 12 | 13 | 14 | 16 |
| 160 | 23 | 24 | 25 | 26 | 28 |
| 200 | 35 | 36 | 37 | 38 | 40 |

Minor tier: 2 + 0.075 x (skill - 60). Special tier: 5 + 0.30 x (min(skill, 200) - 100). OSI's fame bonus unchanged:
1 / 2 / 3 / 5 at fame level 25 / 30 / 35 / 40 (ServUO's line, 0 at fame 1 to 40 at 30,000). The minor line meets the
special one at 100 with no step down. OSI for comparison: 2 at exactly 100, 5 from 100.1, 8 from 110.1, 10 at exactly
120 and 8 again above it (its quirk; a fact pins it), nothing past that but the fame bonus, nothing below 100.

### The miss (decision 3a)

A miss sets the creature's `NextRetry` to now + 5 seconds (one timer per creature, any thief), says the caught line,
calls `RevealingAction` on the thief (pinned's `OnTarget` already revealed them at the start of the steal; this is for
a thief who hid between), and `from.AggressiveAction(thief, false)` then `from.Combatant = thief`, so the creature's AI
takes the thief as its target. Inside the cooldown the attempt says the wary line and rolls nothing (no gain either).
The cooldown is in memory: a restart clears it, which only lets a thief retry sooner once.

### The loot (decisions 3 and 4)

Minor tier, Stealing 60 to 99.9 (one draw of 100):

| Weight | Prize |
|---|---|
| 35 | gold: 20 + fame / 40, give or take a quarter (fame 1: 15 to 25; 30,000: 577 to 962) |
| 25 | Thieves' Den scrip, 1 to 3, paid into the character's Den purse (`CharacterGuildData.GuildCurrency["thieves"]`), "You pocket N Thieves' Den scrip from the creature's hoard." (a thief with no account, never a player, gets gold instead) |
| 15 | lockpicks, 2 to 5 |
| 15 | a small potion: heal, lesser cure, refresh, agility, strength or night sight |
| 10 | bandages, 5 to 10 |

Special tier, Stealing 100 and up (one draw):

| Share | Prize |
|---|---|
| 1% | a loop scroll fragment (`LoopScrollFragment`, five make a loop scroll; a box's rare pool pays one in seven of a 2 to 25 percent slot and the Loop box one outright, so a steal is the rarer source: at 40% success that is one fragment in 250 tries at best) |
| 4% | a recipe scroll: 75% from the `"thieves"` reward table (the three Den recipes and the Shadow Cloak schematics I to III), else from `"bandV"` (every gated craft's Band V scrolls); an `AccountRecipeScroll`, learned account-wide |
| 15% | a stolen-only component the creature's fame level allows, uniformly: thread and ash from any creature, whisperleaf from level 10 (fame 7,500), thief's wire from 20 (15,000), a lucky fang from 30 (22,500) |
| 80% | OSI's special item, ServUO's draw from the first nine of `SpecialItemList` (never the lantern or the tool box), as P127 |

On top of either tier: a creature whose pack holds a Burrows family part (`BurrowsPartBase`, which every Burrows family
packs, P140) gives one more of that part at 10%. No other creature has a family part, so nothing else changes.

### The components and the recipes (decision 4)

| Component | From | Feeds |
|---|---|---|
| shadowsilk thread | any creature | Shadowsilk Cloak (10), Pickpocket's Charm (2) |
| ember ash | any creature | Thief's Smoke Bomb (3) |
| whisperleaf | fame level 10+ | Thief's Smoke Bomb (1); proposed Shadow Cloak IV (6) |
| thief's wire | fame level 20+ | proposed Gilded Lockpick (2) |
| lucky fang | fame level 30+ | Pickpocket's Charm (1) |

Built (each a craft entry with a pinned-style own recipe, learned from a scroll; `ThievesDenCraftRegistrations.cs`):

| Id | Recipe | Craft | Inputs | Result |
|---|---|---|---|---|
| 9400 | Shadowsilk Cloak | Tailoring 100 to 130, Misc | 14 cloth, 10 shadowsilk thread | a cloak (0x1515, hue 0x455): Stealth +5, Hiding +3 |
| 9401 | Thief's Smoke Bomb | Alchemy 100 to 130, the stock bomb's group | 1 eggs, 3 ember ash, 1 whisperleaf | a smoke bomb that hides on Hiding 50 (the stock one needs Ninjitsu 50), 10 mana, pinned's own use otherwise |
| 9402 | Pickpocket's Charm | Tinkering 100 to 130, Jewelry | 2 gold ingots, 1 lucky fang, 2 shadowsilk thread | a ring (0x108A, hue 0x8A5): Stealing +5, Snooping +5 |

Why own recipes and not Band V scrolls: the Den owns no craft skill (`RecipeOwners.BySkill`), so a Band V entry at
Tailoring 100 would enter the Tailors' Circle's rank-4-and-5 rotation and rank-5 starter set (`GuildRecipeShopGump.Rotation`
and `ClusterFGuildPromotion.Grant` draw `RecipeKind.Scroll` keys). `Classify` puts an item with `CraftItem.Recipe` in
`RecipeKind.OwnRecipe` (key `recipe:<id>`), which those draws skip, and the gate, the menu hint ("found only in the wild")
and `AccountRecipeScroll` already handle own recipes (the mule schematics are the precedent, ids 9000 to 9173; the Den's
block is 9400). Max skill 130: `CraftCeilingsVerification.K1` holds Tinkering's stock top at 130 (cc-P67's chain from
the stock top to 200 belongs to the materials); the first build had the charm at 150 and that fact went red, so all three
sit at 130.

Proposed, not built (each waits on something named):

| Recipe | Craft | Inputs | Result | Waits on |
|---|---|---|---|---|
| Gilded Lockpick | Tinkering 100 | 2 thief's wire, 1 gold ingot | a lockpick worth +10 Lockpicking on the roll and half as likely to break | a hunk in pinned `LockPick.cs` (the roll reads the skill value only); the mechanism is a patch, so it is Chase's call |
| Shadow Cloak IV | Tailoring, the mule module line | the tier III cloak, 6 whisperleaf, 4 ember ash | the mule hides at once when attacked (no 30-second cooldown) and stays hidden while mounted | `MuleModuleData` is a fixed three-tier table (`MaxTier`); a fourth tier is a mule-line change, not a recipe |

The F-9 Den starter items the prompt named as upgrade targets (the Bag of Smoke Bombs, the Twilight Jacket) do not exist
yet: `CharacterCreation.cs:641-645` packs five stock `SmokeBomb`s and there is no jacket type. The Thief's Smoke Bomb is
the smoke-bomb upgrade in the meantime; a jacket line can take the shadowsilk thread when F-9 builds it.

### Skill gain (decision 5)

After every legal attempt (the thief was allowed to roll: member, rank, place, skill at or above 60, not inside the
cooldown), success or miss: `thief.CheckTargetSkill(Stealing, from, 60, 100 + 2.5 x fame level)`, gain only (the
steal's outcome was decided before it). Through pinned's handlers as `ClusterFSkillGain` wraps them, so: the shard's
rate (`chanceAttempts` and `amountMultiplier`), the worn-bonus rule when the window's top is the cap, and pinned's
no-challenge rule (a thief whose Stealing value is at or above the window's top gains nothing). So the ceiling is the
creature's: fame 1 trains to 100, fame 7,500 (level 10) to 125, 15,000 (level 20) to 150, 22,500 (level 30) to 175,
30,000 (level 40) to 200, the player's cap in every case. P127's fact (a thief at 150 gains against a 30,000-fame
creature; nothing with `clusterf.stealing.monsterGain` off) still holds, with the fixture now a Den member.

### Saved state (decision 6)

`MonsterStealingStore` (`Saves/MonsterStealing`, version 0): the set of creatures stolen from (written as mobile
references; a deleted creature is dropped on save and skipped on load; `CreatureDeletedEvent` removes it live) and each
player's Gem of Salvation `NextUse` (dropped once past; `PlayerDeletedEvent` removes it). `StealingHandler.HasBeenStolen`
and `GemOfSalvation.NextUse` read it. A world saved before the file existed loads with it empty (pinned's
`GenericPersistence` returns when the file is absent), so nothing migrates.

**The alternative, argued (subsystem policy: a patch names what it rejected):** ServUO's own shape is a serialized
`HasBeenStolen` on `BaseCreature` (`BaseCreature.cs:326-332`) and `NextGemOfSalvationUse` on `PlayerMobile`. That is a
patch to each file's serialization with a version bump of pinned's own types; P121 and P130 rejected that shape for
pet-training state for the same reasons that apply here: a pinned bump of either file collides with our field, the
generator's migration file would have to be kept by hand (P127 found the build emits none), and the side table is
exactly as durable. Rejected here for the same reasons; the hunk is listed for Chase in case he prefers ServUO's shape.

## Deviations from OSI (the register)

Each is "ours", reverses by the line named, and keeps OSI's code beside it where that was possible:

1. **Monster stealing needs the Thieves' Den and its rank** (`ThievesDenStealRules.CheckPlaceAndRank`). OSI: anyone.
2. **The tutorial dungeon (the Burrows) from Initiate; every facet's dungeons from Journeyman; the shard's later
   dungeons and bosses from Master** (`PlaceOf`, `RequiredRank`, `IsBoss`). OSI: Felucca dungeons and champion spawns
   only (kept as the Initiate's places).
3. **The chance curve** (`GetStealingChance`): 5 to 35 percent from 100 to 200 by skill; OSI's steps (`GetServUOStealingChance`)
   are 2 / 5 / 8 / 10 and stop at 120. The fame bonus is OSI's.
4. **A lower tier from Stealing 60 with its own table** (`StealLootTables.GiveMinor`). OSI: nothing below 100.
5. **One success per creature, not one attempt; a miss has a 5-second cooldown and provokes the creature** (`HandleSteal`,
   `Miss`). OSI: any attempt marks the creature and costs nothing more.
6. **New loot on the special draw** (fragments, recipe scrolls, the five components, 20% of successes) and the Burrows
   family part. OSI: the nine special items only (kept as the other 80%).
7. **Every legal attempt rolls Stealing gain on (60, 100 + 2.5 x fame level)** (P127's rule, widened). OSI: no gain.
8. **The never list is longer:** tutorial creatures, the Vault, the pack mule (ours; OSI's pets and summons kept).
9. **The stolen flag and the gem timer live in a side save file**, not on the mobiles (P127's "in memory" deviation
   closes; this one replaces it).
10. **The Thief's Smoke Bomb** hides on Hiding where OSI's smoke bomb needs Ninjitsu: a new item, the stock one untouched.
11. **Three recipes, five components, one reward table** that OSI does not have (the F-43 register entry covers the
    gating itself).
12. **The Life Shield Lotion is live in one of ServUO's four sites** (the pet Life Drain); the other three are not here
    (below), so a player under it is still drained in full by the Harrower's tentacles.

## Decisions taken inside the task

- **"Bosses" means `ClusterFLootBoxes.IsBoss`** (`!IsParagon && IsHighEndSource`): the shard already has one answer to
  "is this a boss" for loot boxes and rare self-repair, and a paragon is a souped-up ordinary creature, not a boss. So a
  paragon in Felucca Despise is an Initiate's mark. The first draft of the boss fact used a paragon and went red on
  exactly this; it uses a champion (Barracoon) now. **Second hand-off:** with the Burrows open to an Initiate, "bosses
  anywhere stay Master" (Chase 05:51) met the fact that the Burrows' named bosses are plain `BaseCreature`s to that
  test (`TheBurrowMother`, `TheGloomQueen`; `IsHighEndSource` lists stock types and `IRareSelfRepairSource`, which they
  do not implement, P140). Rather than widen the loot-box list (which would hand them loot boxes and self-repair rolls,
  P140's call to make), the Den has its own small `ShardBossTypes` set beside the loot-box test. The Overdraft is not
  in it: it lives in the Vault, which is never.
- **The refusal line only in a covered place.** `HandleSteal` runs after every pack steal from any `BaseCreature`,
  townsfolk included; a line on every one would be noise and a tell. So: outside every covered place the handler is as
  silent as OSI's; inside one, the non-member and too-low lines.
- **A thief inside the cooldown rolls no gain**: the attempt was not a legal one. Everything else that reaches the roll
  gains, hit or miss (decision 5 says "every legal attempt").
- **The family part is found in the creature's pack**, not declared per class: every Burrows family packs its part at
  construction (P140), so the cheapest "roll its family part" is one more of what is already there. A creature with no
  part in its pack gets nothing extra, which is every non-Burrows creature.
- **The scrip goes into the purse, not the pack:** the shard's guild currency is a number on `CharacterGuildData`, not an
  item (F-7), so "Den scrip" as loot is `AddCurrency("thieves", n)` and a line.
- **Components are stackable placeholders on stock art with hues**, as the Burrows parts are, for Chase's eye.
- **P127's claim about the balm and lotion corrected:** ServUO calls `BalmOfProtection.HandleDamage` and
  `LifeShieldLotion.HandleLifeDrain` from four content sites, not from `AOS.Damage`. Counted with one grep over
  `D:\UO\ServUO-pub57\Scripts` excluding the Monster Stealing folder: `HarrowerTentacles.cs:245` (lotion),
  `MonstrousInterredGrizzle.cs:305` (balm), `Regions/DamagingRegion.cs:181` (balm), `Services/Pet Training/SpecialAbility.cs:2585`
  (lotion). The shard's `AOS-damage-eater-hook.patch` is a specific call, not a general damage hook, and ServUO's balm
  never went through `AOS.Damage` anyway, so a hunk there would be a deviation beyond OSI; the right wiring is at the
  four sites, one of which is ours.

## Tests

`server/tests/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs`, 10 facts, `[Collection("Sequential UOContent Tests")]`:

1. `ANonMemberAndATooLowRankAreRefusedWithTheLine`: a non-member in a Felucca dungeon is refused with the line; a member
   or not on open land hears nothing (`NotHere`); an Apprentice in a Trammel dungeon is refused with the line naming
   Apprentice and Journeyman and a Journeyman proceeds; an Initiate in the Burrows (`OldHavenBurrowsRegion.Initialize`,
   the thief at 5200,1200; `IsTutorialDungeon` and not `IsShardDungeon`, the place `TutorialDungeon` at rank Initiate)
   proceeds, and The Burrow Mother beside them is a boss to the Den, refuses the Initiate with a line naming Master and
   gives to a Master; an Initiate against a champion (Barracoon) in a Felucca dungeon is refused with a line naming
   Master, a paragon is no boss, a Master proceeds.
2. `EachRankOpensExactlyItsPlaces`: `RequiredRank` for the five places (the tutorial dungeon at Initiate) and the boss
   flag; the rank names; `PlaceOf` for a Felucca dungeon, the same dungeon on Trammel, open land, a champion spawn laid
   down on Trammel (a `ChampionSpawn` with `SetInitialSpawnArea` and `UpdateRegion`, an Initiate proceeds there, and the
   place is gone when the spawn is deleted), and the Burrows (`TutorialDungeon`, not `ShardDungeon`, rank Initiate;
   `ShardDungeonRegionTypes` empty).
3. `TheExcludedCreaturesRefuse`: a pet, a summon, a Gourdling (tutorial creature), a pack mule, a creature standing in the
   Vault (`RootdeepVaultRegion.Initialize`, the creature at 5150,1140) against a Master, each `Never` and unmarked; a
   creature already stolen from is `AlreadyStolen`.
4. `TheChanceCurveMatchesTheTable`: the table above at 59.9, 60, 80, 100, 120, 160, 200 and 250 for fame 1 and 30,000;
   no step down at 100; OSI's table beside it (15 at 120 and 13 at 130 against fame 30,000).
5. `TheMinorTableBelow100AndTheSpecialTableFrom100`: every `MinorPick` and `SpecialPick` boundary; `GoldFor`; each minor
   prize lands (gold, lockpicks, a potion, bandages in the pack, scrip in the purse); a member at 80 steals three minor
   hauls in 600 tries and never an OSI special; a Master at 200 steals five special prizes in 300 tries, each an OSI
   special, a component, a fragment or a recipe scroll, never a minor one.
6. `FragmentsRecipesAndTheNewComponentsCanDrop`: `MakeSpecial` gives a fragment, a Den recipe scroll (key in
   `DenRecipeKeys`), a wild scroll, the component ladder by fame level (2 / 3 / 4 / 5 types at 0 / 10 / 20 / 30), a weak
   creature only thread or ash, a famous one all five within 200 draws, an OSI special from the first nine; a Burrow Grub
   gives Burrower Claws at a 0.0 roll and nothing at 0.5, a skeleton never.
7. `TheDenRecipesAreOwnRecipesLearnedFromAScroll`: the three craft items exist with ids 9400 to 9402, classify as
   `OwnRecipe` with the Den keys, are absent from their skill's Band V keys, name the stolen components among their
   resources; a fresh account does not know the cloak, `Learn` of `recipe:9400` makes it known and not the bomb; the
   cloak's and the ring's skill bonuses; the stock smoke bomb refuses a thief with Hiding 100 and no Ninjitsu and the
   Thief's Smoke Bomb hides them for 10 mana.
8. `TheLifeShieldLotionHalvesALifeDrainOnAPlayer`: 30 Life Drains on a player land 300 to 1,200 hits; under the lotion
   30 more land less than half of that; `HandleLifeDrain` takes 50 to 99 percent off and nothing once the effect ends.
9. `AMissCanBeRetriedAfterTheCooldownAndProvokesTheCreature`: a hidden member at 60 misses, is unmarked and revealed,
   the creature's combatant is the thief, `NextRetry` is within 5 seconds; the at-once retry is `Wary`; with the
   cooldown moved past, a real roll again.
10. `AfterOneSuccessTheCreatureRefusesAndTheFlagSurvivesASave`: a Master at 200 succeeds against a 30,000-fame creature
    (a miss on the same creature retried), 21 more attempts are `AlreadyStolen` and give nothing; the store's round trip
    (`Serialize` to a buffer, `ClearForTests`, a marked creature deleted, `Deserialize`) brings the flag and a gem timer
    back and not the deleted creature.

P127's `MonsterStealingVerification.cs`: the fixture joins the Den (an Initiate); `TheChanceTableIsServUOsBesideOurs`
(ServUO's through `GetServUOStealingChance`, ours at 120), `AFeluccaDungeonIsOSIsPlaceAndTrammelsIsOurs` (places and
`CheckPlaceAndRank` in place of `CheckLocation`), `AThiefAt120StealsASpecialItemOncePerCreature` (a success marks and a
miss does not; below 60 `TooLittleSkill`); the other seven unchanged.

**Seen failing first.** One break set on the real tree (`breaks.py` in the scratchpad: 13 textual breaks across 6
files, each asserted to match once, the originals snapshotted with SHA-256 and restored from the snapshot, then
re-hashed: byte-identical), run through `build.sh --tests-only`:

| Run | Tree | Result |
|---|---|---|
| build 1 | the real tree, first cut | 1,439 tests, 1,430 passed, 5 failed: three of mine (the paragon as a boss, OSI's 130 quirk, the smoke bomb with no skill callback installed), `CraftCeilingsVerification.K1` (Tinkering, the charm at 150 raised the stock top: fixed to 130), and `WispOrbPossessionVerification` ForestNymph vs Phantom (pre-existing flaky, P135 saw it too, green in every other run here) |
| build 2 | the real tree, fixed | **1,439 tests, 1,435 passed, 0 failed, 4 skipped** |
| build 3 | the 13 breaks | 1,440 tests, 1,422 passed, 14 failed: exactly the 13 facts aimed at (the 10 new and P127's 3 rewritten), plus RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies (pre-existing flaky, P141 and P135 saw it, green in builds 1, 2 and 4) |
| build 4 | restored (hashes identical) | 1,440 tests, 1,435 passed, 1 failed: my own fact 5 counted five pack items after five special steals and two stackable prizes (seeds or components) had merged into one stack; the fact now sums amounts. Code untouched |
| build 5 | the same tree, that assertion fixed | stopped during the builder stage's image export by the Claude Code harness because the machine was critically low on memory (0.9 GB of 31.7 free when read afterwards; the test shard and six service containers were up). Not restarted in that session: the harness asks that it be started again only when asked |
| red run (second hand-off) | the old rule (the Burrows at Master), facts 1 and 2 rewritten for the Burrows at Initiate | the builder stage, then `dotnet test` on the builder image filtered to the two facts: **both failed** as aimed: fact 1 at the Burrows' required rank (expected 0, Initiate; actual 3, Master), fact 2 at `PlaceOf` (expected not `ShardDungeon`; actual `ShardDungeon`). Log in the scratchpad (`red-test.log`) |
| build 6 (the gate) | the tree to commit: the Burrows at Initiate, `ShardBossTypes`, the two facts tightened to name `TutorialDungeon` | **1,440 tests, 1,436 passed, 0 failed, 4 skipped**; the 20 Monster Stealing facts (10 here, 10 in P127's file) all passed, counted in the log; the raised-garden and wisp-orb facts passed this time. Exit 0, `--tests-only: stopping before the runtime image`. Log `build6.log` in the scratchpad |

The breaks, one per fact: the non-member treated as an Initiate (fact 1); every facet an Initiate's (2); the tutorial
creature off the never list (3); the special slope 0.25 (4); the fragment share 0.02 (5); whisperleaf from level 15 (6);
no recipe on the cloak (7); no cooldown on a miss (9); the flags not written on save (10); the lotion not asked (8);
Trammel's dungeon reported as Felucca's (P127 fact 2); 11 at 120 in OSI's table (P127 fact 1); the floor at 50 (P127
fact 3, and fact 4's 59.9).

The red run of the second hand-off was a filtered test on the builder image, not the whole gate, because only the two
facts had changed and the gate takes the machine's memory for a while; the green is the whole gate (build 6).

**Not done:** a client, and a boot of a saved world with the new store file (P127 proved that route for its types; the
store is a new file a missing copy of which loads empty, and its round trip is fact 10). P142-7 asks Chase for the
restart.

## Play-test items added

P142-1 to P142-7 (steps in `testing/playtest-steps.json`, Who in `testing/bot-triage.md` group P142): P142-1 BOT (a
Trammel dungeon at Initiate then Journeyman), P142-2 BOT (a champion spawn at Initiate), P142-3 BOT (the Burrows at
Initiate, then The Burrow Mother at Initiate and Master; `[go 5200 1200 0`, a spawned skeleton, the region exists
before the map batch; rewritten in the second hand-off, it said Journeyman then Master), P142-4 BOT (the
lower tier at 80), P142-5 BOT (a miss, the wary retry, the retry after six seconds), P142-6 BOT-PARTIAL (a stolen recipe
learned and crafted; the look is Chase's), P142-7 DEPLOY (the flag and the gem timer across a restart). The standing is
set with the test shard's `[GuildStanding thieves <amount>` (the staff command, test shard only); no bot check is written yet.
`python -m unittest tools/tests/test_play_who.py`: `RealFiles.test_every_open_item_has_a_who` fails on ids that are not
mine and were unsorted before this prompt (P160-0, P161-1 to P161-3 and the rest of its list, prompts that wrote no
triage rows); the P142 rows pass its shape checks. For the overseer.

## Deviations and decisions for Chase

1. **The ladder** (headline 2, the table above): Initiate OSI's places and the Burrows (your 05:51 call, built),
   Journeyman every facet's dungeons, Master the shard's later dungeons and bosses anywhere, the Burrows' two named
   bosses among them. Grandmaster and Legendary open nothing more; a proposal if you want them to mean
   something here: +1 percent on the roll per rank above Master (built in five lines in `GetStealingChance` if you say
   so). The rank names are the generic ladder's because the Den has no names of its own in `GetRankName`.
2. **The curve** (the table above): 5 / 11 / 23 / 35 at 100 / 120 / 160 / 200, fame +1 to +5 on top, the minor tier 2 to
   5 from 60 to 100. Numbers are constants at the top of `StealingHandler.cs`.
3. **The cooldown is 5 seconds per creature**, any thief (`RetryCooldown`); in memory.
4. **The loot tables** (above): the minor weights 35 / 25 / 15 / 15 / 10; the special draw 1 / 4 / 15 / 80; the family
   part at 10%; the Den share of recipe scrolls 75%; the component ladder at fame levels 10 / 20 / 30.
5. **The recipes:** three built (the cloak, the bomb, the charm, with their numbers) and two proposed (the Gilded
   Lockpick needs a `LockPick.cs` hunk; Shadow Cloak IV needs a fourth mule tier). Say which of the two to build, or
   neither; and whether the three built ones should be sold anywhere (today: stolen scrolls and, through
   `Recipe.Recipes`, the general box recipe pool) or stay stolen-only.
6. **Bosses are `ClusterFLootBoxes.IsBoss`,** paragons excluded, **plus the Den's own `ShardBossTypes`** (The Burrow
   Mother, The Gloom Queen), so an Initiate in the Burrows still needs a Master for its bosses. Say if a paragon should
   count, and whether the Burrows' bosses should instead join the loot-box boss list (that would give them loot boxes
   and rare self-repair rolls too, so it is P140's domain, not done here).
7. **The stolen flag and the gem timer are in a side save file**, not on the mobiles. ServUO's shape would be two
   serialization hunks with version bumps: `BaseCreature.cs` (a bool field, `HasBeenStolen`) and `PlayerMobile.cs` (a
   `DateTime`, `NextGemOfSalvationUse`), each with a hand-written migration file. Not built, for P121's and P130's
   reasons; say if you want ServUO's shape instead.
8. **The Balm of Protection still reduces nothing.** ServUO's three sites for it are the Grizzle (not ported), damaging
   regions (not in pinned) and nothing else; there is no OSI call in `AOS.Damage`. The one-hunk option the prompt
   named would be ours, not OSI's: in pinned `Misc/AOS.cs` at the damage-eater hook (after the reflect block),
   `if (m is PlayerMobile pm) totalDamage = (int)BalmOfProtection.HandleDamage(pm, totalDamage);`, which would make the
   balm cut every hit by 50 to 99 percent for 30 minutes, far stronger than OSI's. Recommendation: leave it inert until
   the Grizzle or damaging regions are ported, and register "applies, reduces nothing" as it stands. The **Life Shield
   Lotion** is live for the pet Life Drain; its other OSI site, the Harrower's tentacles, is a four-line hunk in pinned
   `HarrowerTentacles.cs:153` if you want it.
9. **The register entries this needs** (agents do not edit `docs/`): the twelve deviations above, and P127's entry 3
   (the in-memory flag and timer) closes.
10. **A correction to P127's note** for the record: its decision 4 said ServUO calls the balm and lotion hooks from
    `AOS.Damage`; it calls them from four content sites (counted above).

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) first; join the Den at its guildmaster (the Bountiful Harvest
Inn's back room) or through `[guild`, and set standing with `[GuildStanding thieves <amount>` (0 Initiate, 5000
Journeyman, 15000 Master).

To try it in game:

1. **A Trammel dungeon at member rank:** with Stealing 120 (`[SetSkill Stealing 120`) in Trammel Despise or Shame, steal
   from a monster's pack as an Initiate (standing 0), then as a Journeyman (5000). Pass: the Initiate is told the Den does
   not trust an Initiate to work the dungeons beyond Felucca and to come back a Journeyman, and never gets a special
   item; the Journeyman gets the special-item message now and then; a non-member in the same place is told only a hand
   sworn to the Den knows where a monster keeps its treasures.
2. **A champion spawn as a member:** at any facet's champion spawn, as an Initiate, steal from the spawn's monsters. Pass:
   the special-item message comes now and then, with no refusal.
3. **The Burrows:** `[go 5200 1200 0` on Trammel (the region exists before the map batch), `[add Skeleton` beside you,
   steal as an Initiate (standing 0). Pass: the Initiate steals as in Felucca's dungeons, no refusal. Then
   `[add TheBurrowMother` and steal from her: the Initiate is told the Den does not trust an Initiate to work a creature
   of that renown and to come back a Master; at standing 15000 the steal rolls.
4. **The lower tier:** with Stealing 80 in Felucca Shame as an Initiate, steal from thirty fresh monsters. Pass: now and
   then a little gold, lockpicks, a small potion, bandages or a scrip line (the Den purse in `[guild` rises); never a
   balm, lotion, seed, draught or gem; Stealing rises on the way.
5. **A miss and the retry:** with Stealing 60, hidden, steal from one monster and miss. Pass: you are revealed, the
   creature attacks you and the line says it caught your hand; stealing again at once says it is wary; after six seconds
   it rolls again; once a steal succeeds the creature says there is nothing left to steal.
6. **A stolen recipe and the craft:** steal until a recipe scroll comes, or `[add AccountRecipeScroll recipe:9400`;
   double-click it, open Tailoring's Misc page with Tailoring 100, `[add ShadowsilkThread 10`, craft the Shadowsilk Cloak.
   Pass: the row appears only after learning (never in a guild shop), the cloak gives Stealth +5 and Hiding +3; the
   Thief's Smoke Bomb (`recipe:9401`) hides a thief with Hiding 50 and no Ninjitsu; the Pickpocket's Charm (`recipe:9402`)
   gives Stealing +5 and Snooping +5.
7. **Across a restart:** after a successful steal, save and restart the test shard, steal from the same creature again.
   Pass: it still says there is nothing left to steal; a Gem of Salvation used before the restart still waits out its six
   hours.

## Repo size rule

No pending file in either repo is over 5 MB; the largest new one is this note. The build logs, the break script and its
snapshot folder stayed in the session scratchpad, outside both repos.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, rerun after the second hand-off's last edit (the same result as the first session's):

```
Repo Result
---- ------
code dry run
docs dry run
```

code, 15 files: `CHANGELOG.md`, `VERSION`, the three recipe-gating edits (`ClusterFRecipeRewards.cs`, `ClusterFRecipeTable.cs`,
`ThievesDenCraftRegistrations.cs`), the pet-training wiring (`SpecialAbility.cs`), the seven Monster Stealing files (four new,
the handler and the gem changed, the components and recipe items new), the two fact files. docs, 44 files: this note,
`testing/playtest-steps.json`, `testing/bot-triage.md`, `tools/progress.json` (the progress dry run writes it), the
importer's `testing/play-tests.json` and `testing/SUMMARY.md`, and the bot's run folder (`testing/bot-runs/2026-10-18-0130/`,
machine output). No pending file is near 5 MB (the only files over it in either tree are the paperdoll kit's
`.xcf` and `.mul` sources and the player-package zips, all older and none pending); both repos read `dry run`, nothing
BLOCKED; the script's archive step reports this note as finished (dry run, not moved).

## The second hand-off (2026-10-18, the overseer's 05:55 change)

The first session stopped with everything built and green in build 2 but the gate's final run (build 5) stopped by the
harness for low memory. Chase, 05:51: "stealing from monsters in Burrow warrens needs to be sooner in thieves guild. it
is the tutorial dungeon." What moved, with file:line:

| File | What |
|---|---|
| `ThievesDenStealRules.cs:44` | `StealPlace.TutorialDungeon`, a fifth place |
| `:52` | `RankForTutorialDungeon = RankInitiate` |
| `:61` | `TutorialDungeonRegionTypes { OldHavenBurrowsRegion }`: its own set, as the prompt allowed, so a later dungeon added to the Master set cannot loosen it |
| `:67` | `ShardDungeonRegionTypes` is now empty (Master; later dungeons go here) |
| `:74` | `ShardBossTypes { TheBurrowMother, TheGloomQueen }`: "bosses anywhere stay Master" inside a dungeon an Initiate may work; see the decision above |
| `:93` | the place name "the warrens" (only a boss line can carry it: the Initiate floor is the member floor, so no rank line is ever needed there) |
| `:110-113` | `PlaceOf` asks the tutorial set first |
| `:133-137` | `IsShardDungeon`, `IsTutorialDungeon`, one parent walk (`IsOfAny`) |
| `:156` | `RequiredRank`: the tutorial dungeon at Initiate; the boss raise unchanged |
| `:166-167` | `IsBoss`: the loot-box test or the Den's set (not a pet or summon) |
| `StealingHandler.cs:3-5` | the header comment |
| `MonsterStealingShardRulesVerification.cs:183-203` | fact 1's Burrows block: an Initiate proceeds; The Burrow Mother refuses the Initiate with the Master line and gives to a Master |
| `:280-288` | fact 2's Burrows block: `TutorialDungeon`, not `ShardDungeon`, rank Initiate, the Master set empty; `RequiredRank` for the fifth place and the boss raise over all five |
| `CHANGELOG.md` 2026.10.18.3 | the first Added line now says the Burrows is an Initiate's and its bosses a Master's (the section was uncommitted, so no new version) |
| `testing/playtest-steps.json` P142-3, `testing/bot-triage.md` P142-3 | the Burrows at Initiate, The Burrow Mother at Initiate then Master |
| this note | headline 2 and 9, the file table, the ladder table, register entry 2, the boss decision, tests 1 and 2, the build table, the play-test list, decisions 1 and 6 for Chase, in-game item 3 |

What did not change: the skill tiers (the 60 floor, the odds to 200), the never list (the Vault, the tutorial
creatures, pets, summons, the mule, a creature already stolen from), the loot, the gain rule, the store. Nothing of
Chase's was closed for memory: the build ran with the test shard and the six service containers up.

Nothing in the first hand-off's notes conflicted with the 05:51 decision beyond the Burrows' rank itself; "what you
changed back" is that one row of the ladder, and the P142-3 pass text, which had also wrongly said a paragon asks for a
Master (paragons are not bosses to the Den, the decision above).

The gate (build 6) is green on the exact tree to commit, the preflight above reads `dry run` for both repos, and nothing else is pending.

P142 DONE
