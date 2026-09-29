# Q-064: the seven recipe-gated garments, and where the gate actually is

2026-09-28, CC task P3. Read-only investigation. No build, no code, nothing in `D:\ShatteredLegacy` written.
Sources: `D:\UO\ServUO-pub57` (ServUO), `D:\UO\ModernUO-pinned` at `7c9215d97` (pinned),
`D:\ShatteredLegacy\server\customizations` (ours), all read by hand. The committed `tools/content_index.py`
(`git show HEAD:`) was run into the scratchpad, never against P2's working copy.

## 0. The answer in four lines

1. **The satchel check was checking the wrong gate.** In ServUO the tailor's craftsman satchel does **not** drop recipes
   560 to 566. Its list is hard-coded to `501-505, 550-552` (`Services/MondainsLegacyQuests/BaseReward.cs:151-154`).
2. **The real source is an Eodon kill drop**: `TimeOfLegends.CheckRecipeDrop`, about 35 lines, which drops one of 20
   recipe scrolls (560-566 plus the Tiger Pelt 570-577 and Dragon Turtle Hide 580-584 armour) from any creature that dies
   inside Eodon. Pinned has none of it. Ours has none of it.
3. **Pinned does have the craftsman satchel path, under other names**, and it is live by default. That matters in the
   opposite direction to the one Q-064 expected: pinned's satchel draws from **every** `AddRecipe`-registered tailor
   recipe, so registering the seven with `AddRecipe` would put them in quest satchels, which ServUO never does.
   Pinned already has the right call for this, `AddQuestRecipe`, which registers without entering the satchel pool.
4. **All seven land in one bucket: port with its gate.** The gate is bounded (seven trivial items, seven recipe lines,
   one ~40-line death hook in customizations) and is not a subsystem. It is not "port now" because without the Eodon hook
   the recipes are exactly the present-but-unreachable content Q-064's answer ruled out.

## 1. The seven items

All seven are trivial: a label, a graphic, a two-constructor shape, version 0, no custom logic. `ChefsToque` alone
carries resist and hit-point overrides. All four parents exist in pinned (`Items/Clothing/OuterLegs.cs`, `OuterTorso.cs`,
`Shoes.cs`, `Hats.cs`). Material for all seven is plain `Cloth`.

| Type | ServUO file:line | Parent | Graphic | Label | Recipe | Skill min-max | Cloth |
|---|---|---|---|---|---|---|---|
| `JesterShoes` | `Items/Equipment/Clothing/Shoes.cs:619` | `BaseShoes` | `0x7819` | 1109617 | 560 | 20.0-35.0 | 6 |
| `ChefsToque` | `Items/Equipment/Clothing/Hats.cs:2582` | `BaseHat` | `0x781A` | 1109618 | 561 | 6.2-21.2 | 11 |
| `GuildedKilt` | `Items/Equipment/Clothing/OuterLegs.cs:347` | `BaseOuterLegs` | `0x781B` | 1109619 | 562 | 82.8-97.8 | 8 |
| `CheckeredKilt` | `OuterLegs.cs:381` | `BaseOuterLegs` | `0x781C` | 1109620 | 563 | 41.4-56.4 | 8 |
| `FancyKilt` | `OuterLegs.cs:415` | `BaseOuterLegs` | `0x781D` | 1109621 | 564 | 20.7-25.7 | 8 |
| `FloweredDress` | `Items/Equipment/Clothing/OuterTorso.cs:1655` | `BaseOuterTorso` | `0x781E` | 1109622 | 565 | 75.0-90.0 | 18 |
| `EveningGown` | `OuterTorso.cs:1689` | `BaseOuterTorso` | `0x7821` | 1109625 | 566 | 75.0-90.0 | 18 |

Recipe lines: `Services/Craft/DefTailoring.cs:254-255` (toque), `:376-389` (kilts, dress, gown), `:550-551` (shoes), all
inside `if (Core.TOL)`, which is true here (expansion 11). Enum: `DefTailoring.cs:19-25`. Skill is Tailoring, tool is
any sewing kit, nothing else.

**Present in our tree under any name? No, for all seven.** Checked four ways:

- `class <Name>` in pinned and ours: none.
- `[TypeAlias]` naming any of the seven, in either tree: none. ServUO declares no alias on any of them either.
- Same graphic by hand, `0x7819`, `0x781A` to `0x781E`, `0x7821`: no hit in pinned or ours.
- Same label by hand, the seven clilocs above: no hit in pinned or ours.

The committed index agrees: `hidden` lists `GuildedKilt`, `CheckeredKilt`, `FancyKilt`, `FloweredDress`, `EveningGown` and
`JesterShoes` with no same-graphic twin. `ChefsToque` is not in `hidden` because `Hats.cs` is a candidate file, not a
discarded one, as `notes/index-blindspots.md` already says.

**Recipe number collisions:** none. No `AddRecipe`, `AddRareRecipe` or `AddQuestRecipe` with 560 to 566 anywhere in
pinned (pinned uses literals, so the grep is complete for it), no bare `56[0-6]` anywhere under `Engines/Craft`, and ours
registers no recipes at all.

## 2. How a player gets the recipes in ServUO

Two sources, and the satchel is not one of them.

**Primary: the Eodon kill drop.** `Services/Expansions/TimeOfLegends.cs:23` subscribes `CheckRecipeDrop` to
`EventSink.CreatureDeath`. At `:98-133`, for any `BaseCreature` whose corpse is inside Eodon:

- chance = `Fame / 1,000,000` + `min(luck, 1800) / 152,000` (`:106`, `:115`), luck from `RealLuck` for players;
- on a hit, one third drop a random Aloron or Darden armour piece (`:119`, table `:138`), two thirds drop a
  `RecipeScroll` drawn uniformly from 20 IDs (`:145-150`): **560-566, 570-577, 580-584**.

"Inside Eodon" is `SpellHelper.IsEodon` (`Spells/Base/SpellHelper.cs:1162-1168`): Ter Mur x 0-1087, y 1344-2495, or a
small Felucca box x 6975-7042, y 2048-2115. So a 1,500-fame creature with a 1,000-luck killer gives roughly
0.15% + 0.66% per kill, and a given garment recipe is 1 in 20 of two thirds of that.

**Secondary: treasure chests.** `TreasureMapChest.GetRandomRecipe` (`Services/TreasureMaps/TreasureMapChest.cs:523-528`)
picks uniformly from **every** registered recipe, as one of eight "special" rolls (`:487`) and as a fallback in
`TreasureMapInfo.cs:917`. Any registered recipe can come from a chest, these seven included.

**Not a source: the craftsman satchel.** `TailorsCraftsmanSatchel` (`Items/Containers/CraftsmanSatchel.cs:156-194`) calls
`Reward.TailorRecipe()`, which is `GetRecipe(new int[] { 501, 502, 503, 504, 505, 550, 551, 552 })`
(`BaseReward.cs:151-154`). The Q-064 answer and `notes/index-blindspots.md` Part A both assumed the satchel draws from the
registry. That is true of **pinned's** satchel and false of ServUO's.

## 3. The craftsman satchel, type by type

| ServUO | Pinned | Ours |
|---|---|---|
| `BaseCraftsmanSatchel` (`Items/Containers/CraftsmanSatchel.cs:6`) | **`BaseCraftmansSatchel`**, renamed and namespaced `Server.Engines.MLQuests.Items` (`Engines/ML Quests/Items/CraftmansSatchel.cs:10`) | none |
| `TailorsCraftsmanSatchel` | **`TailorSatchel`** (`:41`) | none |
| `SmithsCraftsmanSatchel` | **`BlacksmithSatchel`** (`:56`) | none |
| `TinkersCraftsmanSatchel` | **`TinkerSatchel`** (`:71`), recipes from inscription or alchemy only, the rest `// TODO` | none |
| `FletcherCraftsmanSatchel` | **`FletchingSatchel`** (`:101`), runic kit `// TODO` | none |
| `CarpentersCraftsmanSatchel` | **`CarpentrySatchel`** (`:117`), runic saw `// TODO` | none |
| `AlchemistCraftsmanSatchel` | **absent**; pinned's `TinkerSatchel` draws alchemy recipes instead | none |
| `BaseReward.TailorRecipe()` fixed list | **absent**; replaced by `CraftSystem.RandomRecipe()` over every `AddRecipe` (`Engines/Craft/Core/CraftSystem.cs:106-114`, `:273-277`) | none |

Who hands them out in pinned: `ItemReward.TailorSatchel` and siblings (`Engines/ML Quests/Rewards/ItemReward.cs:25-37`),
used by 41 quest definitions, 22 in `Definitions/Heartwood.cs` and 19 in `Definitions/Sanctuary.cs` (counted with
`grep -cE "ItemReward\.\w+Satchel"`; those are the only two files), 9 of them tailor satchels, for example "The King of Clothing", collect 10 kilts
(`Definitions/Heartwood.cs:1154-1156`). The ML quest system is on unless configured off:
`questSystem.enableMLQuests` defaults to `Core.ML` (`Engines/ML Quests/MLQuestSystem.cs:146`), and nothing in
`customizations/Configuration` sets it. **Whether the Heartwood and Sanctuary quest NPCs are actually spawned in our
world was not checked.**

So: **pinned has the satchel path, under a rename, and it is a small gate, not a missing subsystem.** It is just not the
gate these seven sit behind.

**The consequence for the port.** Pinned's `TailorSatchel` pool today is 501-505. `AddRecipe` for the seven would make it
501-505 plus 560-566: 7 of every 12 satchel recipes would become garments, the quiver recipes would drop at under half
their current rate, and a Heartwood kilt quest would start paying out kilt recipes, none of which ServUO does. Pinned
already has the right tool: **`AddQuestRecipe`** (`CraftSystem.cs:285-288`) registers the recipe on the craft item and in
`Recipe.Recipes` without adding it to the satchel pool. Pinned uses it once, `DefBlacksmithy.cs:525`. Use it for all
seven.

## 4. The gate, measured

| Piece | Pinned | Ours | Size |
|---|---|---|---|
| Seven item types | none | none | seven ~20-line files, one of them with resists |
| Seven recipe registrations | `AddQuestRecipe` exists; the lines do not | none | seven `AddCraft` + `AddQuestRecipe` pairs in `DefTailoring`, which is an upstream file, so a `--fuzz=0` patch and a line in the bump re-check list |
| Death event to hang the drop on | `BaseCreature.CreatureDeathEvent`, a generated event (`Mobiles/BaseCreature.cs:3216-3217`, raised at `:3281`, `:3411`) | already consumed with `[OnEvent(nameof(BaseCreature.CreatureDeathEvent))]` in `ClusterFAchievements.cs:1058` | no patch needed; a customizations file |
| `SpellHelper.IsEodon` | **absent** (no `IsEodon` anywhere in pinned) | absent | a 6-line bounds check, copy it into the new file |
| `RealLuck` | **absent** | absent | use `Mobile.Luck`; whether that differs from ServUO's `RealLuck` is **unverified** and would be a recorded deviation if it does |
| Aloron and Darden drop types (the other third of the roll) | absent | **present** (`Items/Artifacts/Equipment/Armor/Sets/Alorons Set/`, `Dardens Set/`) | none |
| Something killable in Eodon | Eodon moongate entry exists (`Items/Misc/PublicMoongate.cs:268-275`) | several Eodon creatures ported by CC3 (`notes/cc3-eodon.md`) | **unverified whether Eodon has live spawns on this shard.** If it has none, the hook is correct and fires never |
| Treasure-chest recipe roll (secondary) | pinned's chests create no `RecipeScroll` at all | none | separate, and it would affect every recipe; not part of this gate |

Total: one small patch and one new customizations file of about 40 lines plus seven item files. Bounded, near, no new
subsystem. The one unknown that could collapse it is Eodon's spawns, and that is a check, not work.

## 5. Recommendation, per garment

**All seven: port with its gate.** Not a manufactured spread: they share one recipe source, one drop table, one material
and one patch, so the bucket cannot differ between them.

| Garment | Bucket | Why |
|---|---|---|
| `JesterShoes` (560) | port with its gate | Reachable only through the Eodon death drop, which is a ~40-line customization plus one quest-recipe line, not a subsystem. |
| `ChefsToque` (561) | port with its gate | Same drop, same patch; it is a candidate-file co-port rather than a hidden type, which changes where the class goes, not the gate. |
| `GuildedKilt` (562) | port with its gate | Same drop; registering it with `AddRecipe` instead would leak it into pinned's quest satchels, so the gate is the drop, not the satchel. |
| `CheckeredKilt` (563) | port with its gate | As `GuildedKilt`. |
| `FancyKilt` (564) | port with its gate | As `GuildedKilt`; also worn by an NPC in ServUO's `APleaFromMinocQuest.cs:317`, which is not a reason to port early. |
| `FloweredDress` (565) | port with its gate | Same drop and patch; plain cloth, no other dependency. |
| `EveningGown` (566) | port with its gate | Same drop and patch; plain cloth, no other dependency. |

**Why not "port now":** "port now" would mean items plus recipe lines without the drop, which leaves inert recipes and
craftable-nowhere items, the exact outcome Q-064's answer rejects. **Why not "skip":** nothing here is a subsystem.

**The drop table is the one decision this raises (for Chase).** ServUO's table is 20 IDs. Three ways to port it:

- (a) **all 20, unchanged.** Faithful odds. But 570-584 are not registered, so 13 of every 20 scroll drops would be inert
  scrolls (`RecipeScroll.cs:64`, `r == null` returns), until the armour recipes land (section 6).
- (b) **only 560-566.** No inert scrolls, but each garment recipe drops about three times as often as on OSI. A recorded
  deviation in `docs/fidelity-principle.md`.
- (c) **all 20, and register 570-584 at the same time.** Faithful, but those recipes need `TigerPelt` and
  `DragonTurtleScute`, which neither tree has (section 6), so they would be learnable-but-uncraftable.

My lean is (a): unchanged odds, and an inert scroll is honest in a way a learnable-but-uncraftable recipe is not. Not
decided here.

## 6. What else the same gate covers (cheap to see, not hunted)

**The Eodon drop, not the satchel, is the finding worth more than the seven garments.** It is the only ServUO source of 20
recipes, and **13 of them are for items already in our tree**: `TigerPeltBustier`, `Chest`, `Collar`, `Helm`, `Legs`,
`LongSkirt`, `Shorts`, `Skirt` (`customizations/Items/Armor/`) and `DragonTurtleHideArms`, `Bustier`, `Chest`, `Helm`,
`Legs` (`customizations/Items/Equipment/Armor/`). In ServUO these are crafted by recipe (`DefTailoring.cs:664-702`,
`:781-793`); in ours nothing registers those recipes, so today they are exactly the present-but-unreachable content Q-064's
answer called misleading, except that ServUO also drops them from Eodon treasure chests (`TreasureMapInfo.cs:540`,
`:549`), which we do not have either. How they reach players on our shard now: nothing in customizations constructs them
(grep for `new TigerPelt*(` and `typeof(TigerPelt*)` outside their own files: none). **Not verified further.**

Their gate is larger than the garments': besides the drop and the recipe lines, each Tiger Pelt recipe needs `TigerPelt`
(4 per piece, from `WildTiger`, `Mobiles/Normal/WildTiger.cs:13`) and each Dragon Turtle recipe needs `DragonTurtleScute`.
Neither resource class exists in pinned or ours, and `WildTiger` is not in ours. That is a creature-plus-resource port per
set, still bounded, not a subsystem. It belongs in its own question.

**The satchel path itself gates little on this shard**, because pinned has it. What pinned's version lacks next to
ServUO's is small and already marked `// TODO` in the file: the alchemist satchel, the runic fletcher and carpenter tools,
and the non-artifact tinker draws.

## 7. Where the index misled, and where it did not

- **It did not mislead on the items.** Its `hidden` output matched every hand check: absent, no alias, no same-graphic twin.
- **It cannot see this question.** No row covers `Items/Containers` or `Services/Expansions`, so it never indexed
  `CraftsmanSatchel.cs` or `TimeOfLegends.cs`. And the satchel rename (`TailorsCraftsmanSatchel` to `TailorSatchel`)
  shares no name stem and no distinctive graphic (both are hued backpacks), so neither the name check nor the
  same-graphic check would pair them even if the file were in a row. "Absent" from the index for a renamed container type
  should be read as "not checked".
- **What actually misled was a note, not the tool.** `notes/index-blindspots.md` Part A, lines 15-17, reasons from
  pinned's satchel ("only registered recipes can drop") and the Q-064 answer inherited it as "registering may be the whole
  job". Both were right about pinned and silent about ServUO, where the satchel list is fixed and excludes 560-566.
  For P2: Part A is correct as a statement about this shard and wrong as a statement about where the recipes come from.
- **A small one for P2:** the committed docstring gives `hidden [--row artifacts]`, but the committed CLI takes the row as
  a positional argument and rejects `--row` (`error: unrecognized arguments: --row`). P2's uncommitted diff may already
  change this; not checked.

## 8. Not verified

- Whether Eodon has live spawns on this shard, which decides whether the drop fires at all.
- Whether Heartwood and Sanctuary quest NPCs are spawned (moot for these seven, relevant to every other satchel recipe).
- `RealLuck` against `Mobile.Luck`.
- Whether the seven could be registered from customizations at startup instead of by patch (`CraftSystem.AddCraft` and
  `AddQuestRecipe` are public; craft-group placement and init order not checked). Pinned's tailoring also groups
  differently from ServUO's: ServUO puts the kilts and dresses in group 1111747, which pinned does not use, so the port
  needs a group choice either way.
- Nothing was built or run in a client.
