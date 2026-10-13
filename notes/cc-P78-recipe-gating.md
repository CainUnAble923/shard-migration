# cc-P78: Recipe-gated crafting (F-43)

Run 2026-10-12 to 2026-10-13 by Claude Code (autopilot hand-off after P77). Builder. The brief's `docs\` targets live in
this file; agents never edit `docs\`.

Sources:
- Pinned engine `D:\UO\ModernUO-pinned` at **`d4531cd94b739613155225c234900de9f47d2c88`**.
- Code repo `D:\ShatteredLegacy`, built as `sl-modernuo:cc-p78`. Not deployed, not committed, `latest` not moved
  (8863156884f8, unchanged).
- The Order of the Alembic (cc-P77) had already landed, so its key is live, not a placeholder.

**Provenance.** Two research subagents read pinned's craft and recipe code and our guild, BOD, commission, loop and
mule code. The pinned citations below are theirs. Line numbers are pinned's before our patches unless marked
"patched".

I read these myself:
- the patched `CraftGump.CreateItemList` and `OnResponse`, and the patched recipe checks in `CraftItem.Craft`. I
  rebuilt them by applying our six craft patches in order to a scratch copy;
- `ClusterFAccountData` / `CharacterGuildData` serialization;
- `MuleSchematics`;
- `ClusterFSmithBODPayout.Pay`;
- the League ladder JSON loader.

## Research findings

### The craft engine

**CraftItem** (`Projects/UOContent/Engines/Craft/Core/CraftItem.cs`)
- **Min skill:** each item holds `List<CraftSkill> Skills` (:142, :202), each with `SkillToMake`, `MinSkill` and
  `MaxSkill` (`Core/CraftSkill.cs:5-17`).
- **Main skill:** it is the entry whose `SkillToMake` is the system's `MainSkill` (:884-889), not necessarily
  `Skills[0]`. The gate looks it up the same way (`ClusterFRecipeGate.MinMainSkill`).
- **Recipe fields:** `Recipe` (:160) is set by `AddRecipe` (:204-218). `RequiredExpansion` (:158) is client-only.
- **The craft decision**, `Craft` (:914-1013; the hue variant is :1019):
  1. expansion;
  2. `GetSuccessChance` (skill below the minimum gives 1044153);
  3. **the recipe check at :961-973** (hue variant :1050): 1072847 "You must learn that recipe from a scroll.";
  4. `CanCraft`;
  5. `ConsumeRes`, `ConsumeAttributes`, `OnMade`, then the timer.
- **Our existing patch:** `CraftItem-shard-hooks.patch` wraps the recipe refusal in `ClusterFCraftRun.Refused`.

**CraftSystem** (`Core/CraftSystem.cs`)
- `CraftItems` and `CraftGroups` are plain lists (:43, :45).
- `CreateItem` (:99-117) has no visibility check.
- **Recipe registration:**
  - `AddRecipe` (:286) also feeds `RandomRecipe` (:119), so the Craftsman's Satchel hands it out
    (`CraftmansSatchel.cs:31-35`);
  - `AddRareRecipe` (:292);
  - `AddQuestRecipe` (:298) is in no pool.

**The 11 craft systems**

| System | Main skill | Notes |
|---|---|---|
| DefAlchemy | Alchemy | |
| DefBlacksmithy | Blacksmith | gump: Smelt, Repair, Mark, Enhance (:706-709) |
| DefBowFletching | Fletching | |
| DefCarpentry | Carpentry | |
| DefCartography | Cartography | 4 items: LocalMap 10, CityMap 25, SeaChart 35, WorldMap 39.5 (:89-95) |
| DefCooking | Cooking | |
| DefGlassblowing | **Alchemy** | DefGlassblowing.cs:18 |
| DefInscription | Inscribe | |
| DefMasonry | **Carpentry** | DefMasonry.cs:18 |
| DefTailoring | Tailoring | |
| DefTinkering | Tinkering | |

- There is no basket weaving and no "alter".
- **Imbuing is not a craft system.** Pinned has only `SkillName.Imbuing` and a TODO (`CraftItem.cs:1531`).

**The craft gump** (`Core/CraftGump.cs`)
- `CreateItemList` (:349-396) lists **every** item in the group. It filters nothing: no expansion, recipe or skill
  check.
- **Paging:** `i % 10` and `i / 10`.
- **Buttons:** make is `GetButtonID(1, i)` and details is `GetButtonID(2, i)`, where `GetButtonID = 1 + type + index*7`
  (:429).
- **Click mapping:** `OnResponse` (:460) decodes `index = id / 7` and makes `groups[LastGroupIndex].CraftItems[index]`
  (:506). So **the button id is the item's real index in its group**, and gaps are allowed.
- **Paths that skip the list entirely:**
  - Make Last (:628);
  - Last Ten (:293-347, :533-563);
  - `CraftGumpItem` (:306-342);
  - our Make X (`CraftCountGump.cs`, `ClusterFCraftRun.cs`);
  - the T2A menus;
  - `ClusterFSmithTeaching.cs:66`.
- **Misc buttons that never reach `CraftItem.Craft`:**
  - Smelt (:619, `Resmelt.Do`);
  - Repair (:680, `Repair.Do`);
  - Enhance (:719, `Enhance.BeginTarget`). Enhance uses `GetSuccessChance` only.

**ML recipes**
- `Recipe` (`Core/Recipes.cs`) registers in a static `Dictionary<int, Recipe> Recipes` (:26); a duplicate id throws
  (:18-21). There are no recipe enums: ids are literals.
- **Ids in use:**

  | Ids | System | Where |
  |---|---|---|
  | 0-41 | Blacksmithy | DefBlacksmithy.cs:355-651 |
  | 200-212 | Fletching | |
  | 300-321 | Carpentry | |
  | 400 | Inscription | commented out |
  | 501-508 | Tailoring | |
  | 600-602 | Tinkering | |
  | 9000+ | ours: mule schematics | `MuleModule.cs:233` |

- **Stored per character:** `PlayerMobile._acquiredRecipes` (:149), serialized (:3161-3173), with `HasRecipe`,
  `AcquireRecipe`, `RemoveRecipe` and `ResetRecipes` (:4178-4198).
- **Unknown recipes today are neither hidden nor greyed in the list.** Only `CraftGumpItem` greys MAKE NOW
  (:72-84, 1073620), and `Craft` refuses with 1072847.
- `RecipeScroll` (`Items/Skill Items/Misc/RecipeScroll.cs:52-86`) refuses a known recipe (1073427) and needs the item's
  minimum skill.

**Masonry and Glassblowing books**
- They set `PlayerMobile.Masonry` / `.Glassblowing` (MasonryBook.cs:34, GlassblowingBook.cs:34; player flags at
  PlayerMobile.cs:52-55).
- `DefMasonry.CanCraft` (:40) and `DefGlassblowing.CanCraft` (:38) refuse without the flag (and Carpentry or Alchemy
  100).
- `BaseTool.OnDoubleClick` (:155-161) checks `CanCraft` first, so without the book the menu never opens. **Both
  systems are already gated as a whole.**

**Inscription spell scrolls:** `DefInscription.CanCraft` (:47-74) refuses a scroll whose spell the crafter's book lacks
(1042404). The scrolls are registered by `AddSpell`, `AddNecroSpell` and `AddMysticismSpell` (:129-230).

### Ours

- **No hook into crafting** existed in customizations (no `CraftSystem` subclass, no `CraftSuccess` subscriber).
- **Craft patches before this one:**
  - `CraftItem-shard-hooks`;
  - `CraftItem-mule-module-tier`;
  - `CraftContext-shard-hooks`;
  - `CraftGump-MakeXClear`;
  - `CraftGumpItem-MakeX`;
  - `CraftGump-category-pages`. This one pages the category list and already uses the "keep the real index in the
    button id" technique.
- **Account record:** `ClusterFAccountData` is hand-serialized, at version 16 (`ClusterFAccountData.cs:396`).
  `CharacterGuildData` is version 2 (:628). An unknown version fails loudly (D40).
- **Guild rank was standing alone**, plus the Apprentice bump (`ClusterFGuildSystem.cs`, `GuildRankIndex`).
  `AddReputation` fires nothing, so there was no promotion step. Explicit promotion with trials existed only for the
  League (`ClusterFLeagueRanks.TryPromote`).
- **Loop reset: none exists** (F-12 is not built: "until loops exist", `ClusterFGuildStarterPath.cs:13-14`). The dev
  reset (`ClusterFDevTools.ExecuteReset`) never touched recipes.
- **BOD payout:** only the smith's, at `ClusterFSmithBODPayout.Pay`. **No BOD issuer exists for any other craft**,
  Alchemy included.
- **F-37 recurring clients:** no code exists. Only smith commissions do (`ClusterFSmithCommissions.cs`).
- **F-40 loot boxes, F-41 fanfare, F-42 epic crafting:** no code exists.
- **Mule schematics (cc-P70):**
  - already pinned quest recipes, learned once (`AcquireRecipe`), **never consumed per craft**;
  - bought through `MuleSchematics.Buy` (`MuleModuleGumps.cs:538`);
  - not world items, so there were no items to migrate. What crafting consumes is the previous-tier module
    (`CheckPreviousTier`).

## What was built

| Part | What | Where |
|---|---|---|
| A | Account store `LearnedRecipes` (account record **v17**); keys `recipe:<id>`, `book:<Skill>:<band>`, `item:<Skill>:<Type>`, `flag:Masonry`, `flag:Glassblowing`, `map:<region>` | `ClusterFAccountData.cs`; `Engines/Craft/ClusterFRecipeStore.cs` |
| A | Pinned ids reused: `recipe:<pinned id>`. **Sync** copies a character's pinned recipes and the two book flags onto the account, and the account's onto the character, at login, whenever the craft menu draws, and on every `Knows`. So OSI's RecipeScroll, satchels, loot and both books keep working and become account-wide | `ClusterFRecipeStore.Sync`, `Knows` |
| A | Staff commands: `[Recipes list / grant <key> / revoke <key> / learnall / forgetall` (targets a player, acts on the account; Grant, test shard only). `[RecipeGating [reload]` (Diagnostic: the table, on or off, counts per skill) | `ClusterFRecipeStore.cs` |
| A | `crafting.recipeGating.enabled` (default true) | `ClusterFRecipeGate.Configure` |
| B | The band table, merge threshold, prices, promotion skills, rotation sizes, chances and reward tables, all in **`Configuration/recipe-gating.json`** | `Engines/Craft/ClusterFRecipeTable.cs` |
| C | Menu filter, hint lines and help page | `server/patches/CraftGump-recipe-gating.patch`; `ClusterFRecipeGate.cs` (`ItemRows`, `AddHintRow`, `OnHintButton`, `RecipeHintGump`) |
| C | The same rule enforced in `CraftItem.Craft` (both overloads) | the same patch |
| D | `PatternBook` (skill, band) and `AccountRecipeScroll` (key); hued by band; tooltip and use rules | `Engines/Craft/RecipeItems.cs` |
| E | Promotion: skill cap, trial, grants (guild record **v3**: `RankCap`, `PromotedRank`, `TrialsPassed`) | `ClusterFGuildPromotion.cs`, `ClusterFGuildSystem.cs`, `ClusterFAccountData.cs` |
| E | Guild shop, opened by "Pattern books and recipe scrolls" on a craft guild's hall page | `Engines/Craft/GuildRecipeShopGump.cs`; `GuildTaskDetailGump.BtnRecipes = 8` |
| F | Hooks: large BOD scroll chance (smith payout); commission custom recipe (`CompleteLarge`, empty table); `CreateFromTable(table, source)` for boxes, bosses and quests; epic tables pay only Boss/LootBox; Cartography `LearnRegionMap` | `Engines/Craft/ClusterFRecipeRewards.cs`; one line each in `ClusterFSmithBODPayout.cs`, `ClusterFSmithCommissions.cs` |
| G | Mule schematics learned by the account; rank indexes 1, 2, 4 for tiers I, II, III | `MuleModuleGumps.cs` (`MuleSchematics`) |
| H | One owner per craft skill (`RecipeOwners.BySkill`) | `ClusterFRecipeGate.cs` |
| - | Patch notes 2026.10.13, `VERSION` | `CHANGELOG.md`, `VERSION` |

The patch had to be registered, so `docker/uo/apply-patches.sh` also changed (one entry, with its argument). That file
is outside the brief's listed paths; every earlier patch was registered the same way.

### Part A: how an item is checked (`ClusterFRecipeGate.Classify`, `IsKnown`)

| Kind | Which items | Known when |
|---|---|---|
| **Exempt** | Cartography (no bands), Masonry and Glassblowing (their pinned book gates the whole system; the book is now stored on the account), stock Inscription spell scrolls (gated by owning the spell) | always |
| **Free** | main-skill minimum 30.0 or less | always |
| **OwnRecipe** | the item has a pinned `Recipe` (OSI's ML recipes, our mule schematics). It stays a single scroll whatever its band | its `recipe:<id>` is on the character or the account. This holds even with gating off: it is pinned's own rule, made account-wide |
| **Book** | Band I to IV | its band book (after the merge rule), or its own `item:` key |
| **Scroll** | Band V and up | its `item:` key |

Staff (GameMaster and up) see and make everything.

### Part B: the bands, the file, and the counts

**The file.** `Configuration/recipe-gating.json` follows cc-P48's League ladder loader:
- at start, a missing file is written with the built-in defaults;
- `[RecipeGating reload` reads it again;
- **a bad file is refused whole** ("recipe-gating.json REFUSED (n errors); kept <source>:" and each error), and the
  table in force is kept;
- a field left out keeps its default.

What `Parse` checks:
- syntax;
- bands numbered 1, 2, 3 in order, each floor equal to the ceiling before it (the first is `freeUpTo`), ceilings
  rising, no book band after a scroll band;
- one book price per book band;
- no negative price, amount or count;
- six promotion skills, rising;
- two rotation sizes;
- chances 0 to 1;
- reward table names unique.

The test host runs no `Configure`, so it uses the defaults.

**Defaults (the brief's table):**
- free up to 30.0;
- books: I 30.1-50, II 50.1-70, III 70.1-90, IV 90.1-100;
- scrolls: V 100.1-120, VI to IX in steps of 20 to 200;
- merge below 5 items.

**Items per band, per gated skill**, counted by the build's test host with our registrations, post-Valorite metals and
mule modules in (`RecipeGatingVerification.BandCountsPerCraftSkill`, printed by the build):

| Skill (owner) | Items | Free | I | II | III | IV | V | Own recipe | Exempt | Books after the merge rule |
|---|---|---|---|---|---|---|---|---|---|---|
| Blacksmithy (smithing) | 187 | 30 | 48 | 29 | 27 | 0 | 2 | 51 | 0 | I, II, III |
| Tailoring (tailoring) | 147 | 34 | 16 | 30 | 31 | 16 | 0 | 20 | 0 | I, II, III, IV |
| Carpentry (foresters) | 163 | 12 | 8 | 29 | 75 | 14 | 0 | 25 | 0 | I, II, III, IV |
| Bowcraft/Fletching (foresters) | 22 | 5 | 1 | 2 | 3 | 0 | 0 | 11 | 0 | **IV** (I, II and III all fold into it) |
| Tinkering (tinkers) | 164 | 52 | 64 | 20 | 13 | 0 | 0 | 15 | 0 | I, II, III |
| Alchemy (alembic) | 28 | 12 | 3 | 8 | 2 | 0 | 0 | 3 | 0 | **II** (holds I), **IV** (holds III) |
| Inscription (arcane) | 112 | 0 | 5 | 1 | 0 | 0 | 0 | 9 | 97 (spell scrolls) | I, **IV** (holds II) |
| Cooking (maritime) | 46 | 34 | 1 | 7 | 4 | 0 | 0 | 0 | 0 | **II** (holds I), **IV** (holds III) |

- **Not banded:** Cartography (4 items), Masonry and Glassblowing (whole-system books).
- **Only Blacksmithy has Band V items today** (2). That is why the Band V shop fact runs under a test table whose Band V
  starts at 95.
- **The merge rule** folds a book band with fewer than 5 items into the next book band, repeatedly. The last book band
  (IV) never folds, since the next band is scrolls. Where a fold chain ends in an empty Band IV, the book is called
  "Band IV" while holding lower items (Fletching, Alchemy, Inscription, Cooking). It is sold at rank 3 and given at
  rank 4. Decision 3 below.

### Part C: the menu filter, and why a patch

**What it does.**
- `CreateItemList` asks `ClusterFRecipeGate.ItemRows` for the group's rows. Each known item keeps **its own index in
  the group** for its buttons, then come hint rows for the hidden ones.
- The loop pages by row instead of by item index. Everything else in the method is pinned's.
- `OnResponse` first offers the button to `OnHintButton`:
  - hint buttons are 1,000,000 + skill x 16 + band (band 0 is the wild line), far above pinned's ids;
  - a hint opens the help page and re-sends the craft menu;
  - any other button falls through to pinned unchanged.
- `CraftItem.Craft`'s two recipe checks become `if (!ClusterFRecipeGate.IsKnown(from, craftSystem, this))`, with the
  same refusal (1072847) through `ClusterFCraftRun.Refused`.

**Hint lines.**
- **Book line:** "N more patterns: <guild>, rank <the guild's own name for the rank that sells it>." N is the exact
  hidden count in that category. It shows once the crafter's skill (Value) reaches the lowest band floor among those
  items.
- **Wild line:** "Some designs are found only in the wild." One line for every scroll-only item (Band V and up, and
  pinned recipes), with no count.
- **The help page** (`RecipeHintGump`):
  - for a book: the guild, its hall (from `GuildLocations`), and the ranks that sell and give the book;
  - for the wild line: bosses, treasure, bulk orders and quests, and a pointer to the League field office;
  - a wiki-link placeholder line in both.

**Why a patch, argued.**
- Nothing in pinned or in our code can filter the list: `CreateItemList` loops every item (:356-395) and offers no
  hook.
- Pinned's per-character `HasRecipe` cannot carry account-wide band books.

The alternatives, rejected:

| Alternative | Why not |
|---|---|
| No patch | Impossible, for the reasons above |
| Hide in the gump only | Make Last, Last Ten, Make X, `CraftGumpItem`, forged button ids and the T2A menus would still craft. The gate has to sit in `Craft` |
| A CraftSystem subclass per craft | Replaces 11 pinned Def files |
| Renumbering the visible list | Breaks the button-to-item mapping that `OnResponse` relies on |
| Patching `PlayerMobile.HasRecipe` | Covers only items with a pinned `Recipe` |

**Shape of the patch.**
- One patch (`CraftGump-recipe-gating.patch`, 2 files, 3 hunks).
- It applies on top of `CraftItem-shard-hooks` and `CraftGump-category-pages`. I dry-ran it at `--fuzz=0` against a
  scratch copy with all six earlier craft patches applied, and the build applied it ("Applied:
  CraftGump-recipe-gating.patch").
- It is registered after `CraftGump-category-pages.patch` in `apply-patches.sh`, with its argument above it.
- Empty categories are still listed. Hiding them would mean editing `CraftGump-category-pages.patch`'s paging; not
  done, decision 9.

### Part D: items
- **`PatternBook` (craft skill, band)** and **`AccountRecipeScroll` (key)**. Both are serialization-generated v0.
- **Using one:** it must be in the pack. It teaches the account and is deleted. A known one is refused ("Your account
  already knows ... You keep this.") and kept. Unread ones are ordinary, tradeable items.
- **No skill is needed to read one.** Pinned's RecipeScroll needs the item's min skill (decision 5).
- **Hue by band along the ore/metal ladder** (`CraftResources.GetHue`): I Dull Copper, II Copper, III Gold, IV
  Verite, V Valorite, VI+ Celestial.
- **Tooltip:** craft skill, band, "Teaches your account".

### Part E: promotion, grants, shop

**How rank works now.** Rank is still `GuildRankIndex` 0 to 5 and the guilds keep their own rank names. For the
**craft guilds** (those that own a craft skill: smithing, tailoring, foresters, tinkers, alembic, arcane, maritime):
- the rank is the standing rank held under `RankCap`, never below `PromotedRank`;
- `RankCap` rises to the highest rank the guild's craft skill allows (`PromotionSkill` 0/30/50/70/90/100, the best Base
  of the guild's own craft skills). Rank 5 also needs the trial (`guilds.trialsWaivedUntilBuilt`, default true; or the
  guild in `TrialWaivedGuilds`; or `TrialsPassed`);
- the cap only rises, so **a loop that resets skills never lowers a rank**;
- rank 1 still needs standing 1,000 or the Apprentice task, as before, now plus skill 30.

**Who is tracked.**
- A craft guild is tracked from joining (`Join` calls `StartTracking`).
- **A guild record from before v3 is seeded at the rank its standing gave**, so nobody loses a rank.
- Non-craft guilds, and guild records built by hand, have no `RankCap` entry and rank by standing exactly as before.
  This kept every existing League, mule and BOD test unchanged.

**When it is checked** (`Update`):
- at login;
- at the guild hall page;
- opening `[guild`;
- finishing the Apprentice task;
- whenever the craft menu of a guild's skill draws.

**Grants on each rank reached.**
- **Rank 1 to 4:** that band's pattern book for each band-gated skill the guild owns (after the merge rule).
- **Rank 5:** a Band V starter set, `Rank5StarterScrolls` (2) unknown Band V scrolls per skill.
- **Delivery:** into the pack, else the bank, with a message saying where.
- **A book the account already knows:** none is given, and the player is told so.
- **Rank 0:** the starter kit is unchanged (F-9).

**The shop** (`GuildRecipeShop`, at the guildmaster, members only):

| Rank index | Listed |
|---|---|
| 0 to 3 | each band's book up to **one band ahead** of the rank that the account does not know yet. Further bands are not listed |
| 4 and 5 | also a daily Band V rotation of 3 or 5 scrolls (seeded by day and skill) |

- **Prices:** guild currency only.
  - Books: I 100, II 200, III 400, IV 800.
  - Band V scroll: 1,500 plus 10 of the skill's next-tier material (`BandVMaterial`): Platinum ingots for
    Blacksmithy and Tinkering, Ironwood boards for Carpentry and Fletching, Barbed leather for Tailoring, none for
    Alchemy, Inscription and Cooking (decision 6).
- **What is bought** is the unread item. A buy is re-checked against the rows at the click.

### Part F: other sources
- **F-20 BODs.**
  - `ClusterFSmithBODPayout.Pay` gives a turned-in **large** order (`LargeBOD`) `LargeBodScrollChance` (0.02) at a
    random Band V scroll for its craft. That is Blacksmithy, the only payout that exists. With 2 Band V smith items it
    can pay today.
  - Pinned's non-member turn-in at a regular smith (`BaseVendor.OnDragDrop`) has no hook and pays none.
- **F-37 commissions.** `SmithCommissionSystem.CompleteLarge` calls `TryCommissionScroll`:
  `CommissionScrollChance` (0.05) over `CommissionScrolls`, **empty**, so it pays nothing until custom recipes exist.
  No recurring-client code exists.
- **F-40 boxes, bosses and quests.** `ClusterFRecipeRewards.CreateFromTable(tableName, source)` returns a scroll from a
  `RewardTables` entry. An entry is a key, or a pool `bandV:any` / `bandV:<Skill>`. **No loot box code has landed**,
  so nothing calls it yet; the hook is there.
- **F-42 epic recipes.** A table marked `Epic` pays only to `Boss` and `LootBox` sources, never `Bod`, `Commission` or
  `Quest`. The default `epic` table is empty.
- **Cartography (F-6).** `LearnRegionMap(pm, region)` stores `map:<region>` on the account. Nothing calls it yet;
  region data waits for F-6.

### Part G: mule schematics
- **P70 had landed, and it already taught schematics once** (pinned quest recipes, `AcquireRecipe`). It never
  consumed them per craft: P70's actual build did not use the `AddRes` route the brief worried about. The only
  per-craft consumption is the previous-tier module, which is the design.
- **Converted:**
  - `MuleSchematics.RefuseBuy` asks the account store;
  - `Buy` teaches the account (`Learn`, which also writes it onto the character for pinned's check);
  - `RankFor` is now **1, 2, 4** for tiers I, II, III (4 and 5 for tiers IV and V, if module tiers ever grow);
  - payment unchanged (guild currency plus Mining Vouchers, Clean Up points for the Custodians).
- **Migration:** there are no schematic items in the world to migrate. Recipes a character already learned are copied
  onto its account by `Sync` at the next login or craft menu.

### Part H: owners and per-skill rules
- **One owner per craft skill** (`RecipeOwners.BySkill`): Blacksmith smithing; Tailoring tailoring; Carpentry and
  Fletching foresters; Tinkering tinkers; Alchemy alembic; Inscribe arcane; Cooking and Cartography maritime.
- **The two systems that follow another skill:** Masonry follows Carpentry and Glassblowing follows Alchemy, through
  their systems' main skills.
- **The test:** every one of the 11 craft systems maps to exactly one owner, and the owner's `GuildSkillTable` row
  teaches that skill.
- **Imbuing** is excluded (not a craft system; left to the Imbuing rework).
- **The Masonry and Glassblowing books** stay pinned's, stored on the account. They get no hint lines: without the
  book, the system's menu never opens (pinned `BaseTool.OnDoubleClick`).
- **Spell scrolls are exempt.** Custom spell scrolls, if added, would be Scroll or Book items like any other.
- **BOD issuers follow the owner, but nothing moved:** no Alchemy or Cooking BOD issuer data exists. When they are
  built they issue from `alembic` and `maritime`.

## Tests (red then green)

**New:** `server/tests/Engines/Craft/RecipeGatingVerification.cs`, 14 facts.
1. **Free and Band II.** A free item is visible and a Band II item hidden; the real craft menu packet (the patched
   `CreateItemList`, read off the wire) has the free item's make button and not the hidden one's. After the book, the
   button is there. A second character on the account sees it. With gating off, every item of the group is listed and
   no hints.
2. **Loop reset and books.** A known book is refused and kept; an unknown one is consumed and teaches. Rank Master
   reached with the skill survives every skill set to 0, and so do the recipes.
3. **Hint lines:** none at skill 0; at 200, the exact count and "Society of Smiths, rank <its name>"; one wild line
   with no digits; the help page names the hall.
4. **Promotion.**
   - With 200,000 standing and skill 40, the rank is 1 and the Band I book was granted.
   - With the waiver cleared, skill 100 holds at 4 until the trial is passed, then 5.
   - A second character on the account is promoted without a duplicate book ("already knows").
5. **Shop.**
   - At rank 0: one row, the Band I book.
   - Buying takes guild currency and no gold.
   - At rank 4, under a test table with Band V from 95: the Band V scroll needs Platinum ingots, is refused without
     them, and with them consumes them.
6. **Repair, Smelt and Enhance** each start their target with no recipes (the real `CraftGump.OnResponse` Misc buttons,
   anvil and forge placed).
7. **A mule schematic** learned once is known on three checks in a row and on a second character.
8. **One owner per craft skill**, which teaches it.
9. **The data file** round-trips; a file with a band floor out of step is refused whole and the defaults stay in force.
10. **Saves:** the account record v17 and guild record v3 round-trip.
11. **A pre-v3 guild record** is seeded at its standing rank (smithing tracked at Journeyman; the Warriors untracked,
    standing alone).
12. **Band counts** printed (the table above).

**Changed:**

| Test | Change | Why |
|---|---|---|
| `AccountDataSerializerVerification` | three asserts, version 16 to 17 | the account record bump |
| `RegularSmithBODVerification` | guild record version 2 to 3 | the guild record bump |
| `MakeXRepeatVerification`, `CraftXVerification`, `HammerFamiliarityVerification` | turn gating off in their constructors | their crafters make items above 30 skill they never learned (notice 1072847); these facts test the craft run, not recipes. `RecipeGatingVerification` turns gating on for its own |

**Runs:**

| Run | Result |
|---|---|
| First builds | two rounds of compile fixes (pinned's login event is `[OnEvent(nameof(PlayerMobile.PlayerLoginEvent))]`, not `EventSink.Login`; `System.Random` vs the `Server.Random` namespace; pooled `FindItemsByType` in tests) |
| Third | 19 failed. Older craft tests met the gate, a version assert, and Enhance needing a picked material; fixed as above |
| Green, tests only | **1102 passed**, 0 failed |
| Red, round 1 | 11 breaks at once (below): **12 failed**. Every new fact but the schematic one, plus `MuleModuleVerification` and two `CraftCategoryPagingVerification` facts the hint-button break also hit. The schematic break was absorbed: `Knows` itself writes an account recipe onto the character |
| Red, round 2 | the schematic consumed on use: **1 failed**, `AMuleSchematicLearnedOnceLetsTheModuleBeCraftedAgainAndAgain` |
| Restore | backups copied back and `cmp` byte-identical for all 8 files after each round |
| Green, full | **1102 passed**; "Built sl-modernuo:cc-p78 with patches applied and 1102 shard test(s) passing." |

Red round 1's breaks:
- book items always known;
- hints ignoring the floor;
- the hint hook swallowing every button;
- Cartography without an owner;
- a known book used up;
- the shop two bands ahead;
- account recipes not written to the character;
- a band floor check skipped;
- rank 5 ignoring the trial;
- a pre-v3 record not seeded.

**Not covered by a test:** the refusal inside `CraftItem.Craft` itself. Driving a real craft through the test host's
craft timer was not attempted. The rule it calls (`IsKnown`) is covered, and the patch hunk is three lines; this is
**unverified** in play.

## Decisions for Chase (defaults taken)

1. **Craft guild promotion model.** Rank = standing under a skill cap that only rises, never below the last promoted
   rank. Only the 7 craft guilds are tracked; the other guilds still rank by standing alone. Checked at login, the
   hall, `[guild`, the Apprentice task and the craft menu. Should non-craft guilds get skill gates too, and with which
   skill?
2. **The promotion skill** is the best Base of the guild's own craft skills: the Foresters take Carpentry or Fletching;
   the Arcane Society takes Inscription, not Magery; the Maritime Brotherhood takes Cooking or Cartography.
3. **Merge rule results:** Fletching has only a "Band IV" book holding Bands I to III; Alchemy, Inscription and Cooking
   each have a "Band IV" book holding Band II or III items. Keep the literal rule, or fold a leftover backward into
   the previous book?
4. **Hint rank:** the hint names the rank that *sells* the book (one band ahead: Band I at Initiate). The help page
   names both the selling and the granting rank.
5. **Reading a book or scroll needs no skill.** Pinned's RecipeScroll needs the item's min skill. Add a floor?
6. **Band V materials:** Alchemy, Inscription and Cooking have none (currency only). Leather has no tier past Barbed in
   our data. Names in the file.
7. **Prices and chances are placeholders:** books 100/200/400/800, Band V scroll 1,500 plus 10 material, large BOD
   2 percent, commission 5 percent (empty table), Rank 5 starter set 2 scrolls per skill, rotation 3 and 5.
8. **Staff see everything** (GameMaster and up bypass the gate).
9. **Empty categories** (every item hidden, no hint yet) are still listed in the category column, showing an empty
   item list. Hide them? That means editing `CraftGump-category-pages.patch`'s paging.
10. **Existing OSI recipe items are now hidden until learned** (before, they were listed and greyed in the detail
    page). They get the wild hint line.
11. **The fidelity register** needs its F-43 deviation entry (overseer): stock crafting gated, recipes per account.
12. **World step:** none needed. The JSON is written at first start. Existing characters keep their craft guild rank
    (seeded), and recipes they already learned move to their account at login.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, run 2026-10-13 before DONE:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **Code, 23 files:** the 14 changed and 9 new files listed above, including `docker/uo/apply-patches.sh` and
  `server/patches/CraftGump-recipe-gating.patch`.
- **Docs, 1 file:** this note.
- No file is near 5 MB; nothing BLOCKED.

P78 DONE
