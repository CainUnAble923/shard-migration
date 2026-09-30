# D33 made exact: the reachability audit

2026-09-29, CC. **A measurement. Nothing ported, fixed, deleted, built or committed.** No .NET, no `build.sh`, no
container. `D:\ShatteredLegacy` was read only through `git archive` of HEAD (`8a52998`, 757 `.cs` under
`server/customizations`) into the scratchpad; the live working tree was not opened. CC9 close's uncommitted files were
measured separately, from the copies my CC9 session kept in its own scratchpad (8 of its 11 files, section 1.3).
`docs/` not touched. Changed: `tools/content_index.py` (new `reach` mode), `tools/test_content_index.py` (9 facts).

---

## 0. The number you asked for

**How many of the 219 sit behind the single largest gate: 45 (21%).** That gate is Clean Up Britannia's reward table.
It is not most of them.

**But the roadmap still changes, because the shape is better than "twenty gates".** The count is bigger than 219 and
the cheap end is very cheap:

- **340 ported item and creature files are in no player's reach at HEAD**, not 219 (section 1).
- *(2026-09-30: the 117 and 167 below are predictions that have since been built against. Delivered: **65** and
  **69 + 35 still predicted**. Section 3 has the corrected curve and why; D39.)*
- **Five one-file gates reach 117 of them**: three craft registrations in the `KingsCollectionCarpentryRecipes`
  shape (blacksmithy, tailoring, tinkering) and entries in two tables pinned already ships (treasure chests,
  stealable artifacts). The first ten gates, about 14 units of work, reach **167** (section 3).
- **Clean Up Britannia is the largest single gate (47 files) and ranks tenth by files per unit of work**, because it is
  a subsystem. It is worth building eventually. It is not the next thing.
- **80 files sit behind no gate worth naming**: 32 staff costumes, 14 files of two promotional sets whose bag and
  ticket nothing hands out, 28 items ServUO also ships with no source, and 6 that hang on one unported thing each.

And one correction to my own CC9 note, which I have to lead with because the brief rests on it: **Clean Up Britannia
gates none of CC9's 24 remaining `upstream` files.** I read ServUO's turn-in table as a reward table (section 7).

---

## 1. The exact count

### 1.1 Against the 219

Same scope as the rough pass: files under a subdirectory of `server/customizations` (ported content, AGENTS.md) that
declare at least one concrete item or mobile, without the 32 staff costumes the rough pass also set aside.

| | Files |
|---|---|
| Ported content files, costumes excluded | **570** |
| ... with no content type a player can obtain | **340** (60% of 570) |
| ... partly reachable | 1 (`Shame Revamped/Mobiles/Creatures.cs`: `BurningMage` and `LesserWindElemental` are in no spawn row) |
| **The 219 inside the 340** | **219 of 219** |
| **False orphans in the 219 the instrument now resolves** | **0** |
| **Real orphans the rough pass missed** | **121** |

Type level: **487 of 891** content types (concrete item or mobile) are unreachable by a player; 1 more only by a staff
command (`DevTestingCrystal`). Whole tree including our own top-level customs: 380 of 656 content files.

**Every error in the rough pass went the same way.** Word matching can only over-count reach, and it did: a name in a
comment, a base-class clause or an `is` check counted as a path. The 121 it missed, by why it saw them as named:

| Why the rough pass counted it named | Files | Example |
|---|---|---|
| named only as a base class | 38 | `TigerPeltBustier`, named by `AloronsBustier : TigerPeltBustier` |
| named only by a list that reads types | 36 | 34 imbuing reagents in `GemologistsSatchel.IngredTypes`, its accept list |
| comments, patch context lines, or a same-named nested type | 16 | `BestialArms` (a `.patch` context line), the Darden's set |
| constructed only by code that is itself unreachable | 16 | `InitiationArms` by `InitiationSuitBag`, which nothing makes; `GemologistsSatchel` by the fountain's reward code |
| named only in pinned code left commented out | 9 | `GreymistChest`, the five Grizzle pieces (section 3, gate 9) |
| named only by a data file that places nothing | 5 | the Eodon dinosaurs, named by `bodyTable.cfg` |
| **Total** | **121** | |

One of the 121 is a tree difference, not a miss: `VillainousEpiphany.cs` is unreachable at HEAD and reachable on the
live tree, through CC9 close's `Niporailem`. The full list of 340, with the 121 marked, is Appendix A.

### 1.2 The 29% was wrong in kind, and it was mine

§7 of `cc9-close.md` and D33 both say 219 is 29% of the ported tree. 29% is 219 over **768, every `.cs` file** in
customizations: gumps, timers, ClusterF systems and all. The numerator was a filtered set and the denominator was not.
The comparable figure is **340 of 570, 60%**. Stated both ways with denominators: **340 of 570 ported content files**,
**487 of 891 content types**.

### 1.3 HEAD versus the live tree

The live tree is HEAD plus CC9 close's 11 uncommitted files. Measured on HEAD plus the 8 of them I still hold:
`VillainousEpiphany.cs` moves to reached (its 12 types through `Niporailem`, placed by `TerMur.json:1264`), and every
new file of that batch is reachable: `Niporailem`, `NiporailemsTreasure`, `VirtuousEpiphany` (12), `OrcMask` (by
tailoring), `Cowbell` (by carpentry). So the live figure is **339 of 576**. Not measured: `Cello`, `Trumpet` and
`WallMountedBell`, whose copies I did not keep. By construction they are reached the way `Cowbell` is.

---

## 2. The instrument

`python tools/content_index.py reach [--ours PATH] [--sources] [--twins] [--json OUT]`, about 8 s. Per type and per
file: reached or not, the reference that reaches it, and for the unreached every reference that names it, with kind,
naming type, file and line. `--sources` adds the ServUO side (section 3) and `--twins` the sweep (section 4).
`CONTENT_INDEX_OURS` points the default at an export, which is how this ran without opening the live tree.

**The rule.** A name is not a reach. Only these put a type in the world, and only from code that runs:

| Kind | What it is |
|---|---|
| `new` | `new X(` |
| `typeof` | `typeof(X)`, with the call or list it sits in (`AddCraft`, `GenericBuyInfo`, `UniqueSAList` ...) |
| `string` | `"X"` in our code (spawn tables such as `ShameSpawns`, seeders) |
| `spawn` | an entry in `Distribution/Data/Spawns/**.json`, case-insensitive, aliases included (Q-048's `tanglingroots`) |
| `data` | a type in `Decoration/`, `MLQuests.cfg` or `Professions/` |

**Roots**, the code that runs by definition: pinned code (for names pinned does not declare itself), our patches (added
lines only), those data files, and any type of ours with a static `Configure` or `Initialize` (invoked by name,
`Server/Main.cs:441,448`). Our partials and replacements of pinned types are roots too.

**Five rules turned out to be necessary.** Each one changed a number, has a fact, and was watched failing (section 9):

1. **Reads are not reaches.** `typeof` inside `GetAmount`, `ConsumeTotal`, `Find`, `if (... == typeof(X))`, an accept
   list, ServUO's imbuing and slayer tables, or `Entries[typeof(X)] = points` (Clean Up's and Queen's Loyalty's
   **turn-in** tables) reads a type. The list is `READER_SITES`: 17 names, 16 of them read at a use in this task;
   `FindItemByType` is on it by its name alone.
2. **Static access runs code but creates nothing.** `DespiseSpawns.Definitions` makes the table's strings live.
   `FountainOfFortune.UnderProtection` does not make a fountain.
3. **An item or mobile acts only once something creates it.** The fountain is live, but nothing creates one (S2 D-3:
   only `[add` places it), so the `new GemologistsSatchel()` in its reward code never runs.
4. **A base class is reached through its children, unless it is an item in its own right.** `ShameGuardian` exists as
   its three guardians. `AloronsBustier` existing does not put a `TigerPeltBustier`, which has its own
   `[Constructible]`, in anyone's hands.
5. **Staff hand-outs are not player reach.** Six hooks register only GameMaster-or-higher commands that hand things
   out (`STAFF_ROOTS`). World generators such as `[SetupDespise` are not among them: they place content where players
   walk.

**The brief's four blind spots, and what happened to each:**

| Blind spot | Result |
|---|---|
| **1. Base-type picks** | **None exist.** Neither pinned nor ServUO picks a random subclass by reflection. Every random pick I found goes through a `Type[]` list naming the concrete type (`Loot.Construct`, `Activator.CreateInstance(list[Random])`), and `typeof` walking covers those. Reflection sites read: pinned `Main.cs:548-647` (serialization check), `AddGump.cs` (the GM `[add` menu), `Factions/Core/Reflector.cs` (factions and towns), `MLQuestSystem.cs:55,91` (reads `MLQuests.cfg`, walked as data), ServUO `Mannequin.cs:167` (lists types). Our six dynamic `CreateInstance` calls are generic helpers and `typeof` lists the index already sees. **Count left open: 0** |
| **2. Reflection and `typeof` lists, own file included** | Handled at type level, so a list inside the file of the type that owns it counts, from the owning type. **73** reached types rest on a `typeof` at a site the reader could not name. I read 18 of the files involved (boss drop lists, harvest tables, a seeder): all genuine suppliers |
| **3. Craft tables** | Walked on all three sides. Our additive registrations are roots; pinned's `Def*` name only pinned types; ServUO's `Def*` are the craft gates in section 3. **Gap: recipes.** An `AddCraft` behind a recipe ID counts as reach, but whether the recipe can drop is an int the index cannot follow. 13 files are affected (the D32 garments, in the tailoring gate) |
| **4. Spawn data** | JSON parsed per entry, with line numbers, case-insensitive, aliases resolved. Other `Data/` files are split: those that place (`Spawns`, `Decoration`, `MLQuests.cfg`, `Professions`) and those that only name (`bodyTable.cfg` names the dinosaurs, `npc-speeds.json`, `regions.json`, the `[add` menu's `categorization.json`). ServUO's `Spawns/*.xml` and `RevampedSpawns/*.xml` are parsed per `<Objects2>` entry, for the gate side |

---

## 3. The gates, ranked

> **Corrected 2026-09-30 (cc-P12, D39).** Nine of these gates have now been built or attempted. The "Delivered"
> column records what each actually reached, with the note that established it; the cumulative curve below is
> restated with delivered and predicted figures kept apart; section 3.1 says why the prediction over-counts and which
> unbuilt gates to distrust. **The ranked numbers themselves are left as they were measured on 2026-09-29**, so the
> gap stays visible. Nothing was re-measured. Record of the change: `notes/cc-P12-audit-correction.md`.
> "Delivered" means established from source and the shard's tests, not seen in a client; P7's two carriers
> (Miasma, Lady Lissith) are unverified in the live save (`cc-P7` §4).

`--sources` finds, for each of the 487 unreachable types, every ServUO reference that would put it in the world:
construction, a list, a spawn row. Each carries where its owner stands for us: **pinned** (pinned has the type, so
the fix is a hook or a patch into it), **absent** (port it first), or **ours** (our copy dropped the line). Pinned code
left commented out is reported as well. I grouped those sources into gates by hand (`gatemap.py`, scratch), and the
tool's `what_if` computed what each gate reaches. `what_if` follows chains inside our tree: a bag that hands out a
set counts the whole set.

**The ranking is a greedy cover.** At each step it picks the gate with the most new files per unit of work, then
recomputes the rest, so overlapping gates are not counted twice. Gargish plate, for example, comes from blacksmithy,
alteration, the Ter Mur vendors and loot lists; it is counted once, under whichever gate comes first. Units, in this
project's terms: **1** = one additive hook file, one data table, or entries in one pinned list (a patch). **2** = a
small port (up to ~300 lines) plus a hook. **5** = an encounter (a boss, its placement, its loot), or S7 plus a small
system. **10** = a subsystem of about 1,000 lines. **20** = a subsystem of 3,000+ lines. Rough, and costed from line
counts and wiring, not from building anything.

| # | Gate | New files | Alone | Delivered | Of the 219 | Cost | What it is | Already half there |
|---|---|---|---|---|---|---|---|---|
| 1 | **Craft: blacksmithy** | **33** | 33 | **33** (craft-registrations §0) | 21 | 1 | ServUO `DefBlacksmithy`'s SA block, 36 types: **gargish plate (8 pieces), 16 gargish weapons and the Shortblade, six shields** (three gargish, three plate), `GargishAmulet`, two artifacts, two reagents | **Yes.** The pattern exists: `KingsCollectionCarpentryRecipes`, `OrcMaskTailoringRecipe`, `IncubatorCarpentryRecipe` |
| 2 | **Craft: tailoring** | **26** | 26 | **1** (craft-registrations §0) | 6 | 1 | masks, belts, cowls, collars, `LeatherTalons`; **13 of the 26 are D32's Tiger Pelt and Dragon Turtle pieces, which also need a recipe drop (gate 8) and a resource nobody has (Q-066)**. So 13 now, 13 later | Yes, same pattern; `OrcMaskTailoringRecipe` is the file |
| 3 | **Treasure chests: pinned lists** | **24** | 24 | **0, stopped** (cc-P8 §2.2) | 8 | 1 | entries in pinned `TreasureMapChest`/`TreasureMap` lists: imbuing essences, SOS decor, the dinosaurs as map guardians | Pinned has the chest. **It changes a stock loot distribution**, the `OrcMask`/`HatTypes` question: Chase decides |
| 4 | **Craft: tinkering** | **17** | 17 | **14** (craft-registrations §0) | 13 | 1 | gargish jewellery, SA gem jewellery | Yes, same pattern |
| 5 | **Stealable artifacts: pinned table** | **17** | 17 | **17** (cc-P8 §3) | 16 | 1 | **55 types**, decorative multi-type files, stolen from dungeon spawns | Pinned ships the spawner and its table (`Engines/Stealables/StealableArtifacts.cs`, 81 entries). A patch to it. Same policy question as gate 3 |
| 6 | Imbuing ingredient drops | 21 | 36 | not built | 0 | 2 | ServUO `ResourceDrops.cs`, 252 lines, on creature death | Pinned's `[OnEvent(nameof(BaseCreature.CreatureDeathEvent))]` is additive, **but passes only the creature**; ServUO's handler uses the corpse and the killer. The fit needs a probe. **Low value: pinned has no imbuing**, so the 34 reagents would drop and do nothing, bar `GemologistsSatchel` and a few tinkering and quest uses |
| 7 | Craft: carpentry | 8 | 8 | **2** (craft-registrations §0) | 8 | 1 | the six Darkwood pieces, `AudChar`, `GargishGnarledStaff` | Yes: `KingsCollectionCarpentryRecipes` is the file |
| 8 | Time of Legends drops + Eodon spawns | 14 | 19 | not built | 7 | 3 | `TimeOfLegends.CheckRecipeDrop` (about 50 lines: Aloron's and Darden's pieces, recipes 560-584 on Eodon kills), plus a spawn table for **the six Eodon creatures CC3 ported and nothing places** (`Eodon.xml`, 65 spawners) | The death event (as gate 6); the Shame pattern, `ShameSpawns` plus a generate command, for the spawns |
| 9 | **Pinned's own commented-out drops** | 7 | 11 | **2** (cc-P7 §0) | 0 | 2 | pinned wrote these and left them under `// TODO: uncomment once added`. `Ilhenir.cs:163-167` drops the five Grizzle pieces; `LadyLissith.cs:53` `GreymistChest`; `Miasma.cs:54` `MyrmidonGloves`; a champion list in `ChampionSpawnInfo.cs:126-128` (Gorilla, Allosaurus, Dimetrosaur); `DefInscription.cs:445` `ScrappersCompendium` | **Yes, entirely.** Pinned wrote the code and is waiting on the type, which we now have. Each is a patch that uncomments |
| 10 | **Clean Up Britannia** | **47** | 47 | not built | **45** | 20 | 47 of our types among the rewards (`CleanUpBritanniaRewards.cs`): the Knights (10), Scout (9), Sorcerer (8), Bestial (8) and Virtuoso (8) sets, and four jewels (`EtoileBleue`, `LuneRouge`, `NovoBleue`, `SoleilRouge`). ServUO's directory is 52 files and 5,161 lines, most of them reward items, plus `CleanUpBritanniaData.cs` (979, the turn-in values) and `PointsSystem.cs` (463, S7) | **The S7 seam only** (`Services/PointsSystems/ShameCrystals.cs`, a stub). S7 itself is not built; Shame's altars wait on it too |
| 11 | Craft: alchemy, masonry, bowcraft, inscription | 4 | 6 | not built | 1 | 2 | four registration files | Yes |
| 12 | Pinned champion lists and bosses | 2 | 6 | **0** (cc-P7 §0, §2.6) | 2 | 1 | entries in `ChampionSpawnType` and in Barracoon's and Neira's drops | Pinned has all three. A patch |
| 13 | Niporailem | 1 | 1 | **1** (§1.3) | 0 | done | CC9 close, built, uncommitted | Built |
| 14 | Underworld generator | 3 | 5 | not built | 0 | 2 | places `FountainOfFortune`, which unlocks its satchel and reagent chain | S2 ported the fountain; nothing places it (S2 D-3) |
| 15 | Virtue Artifacts system | 7 | 7 | not built | 6 | 5 | 122 lines on S7, **plus S7 (463)**. **Also the real gate for five of CC9's 24** (section 7) | The S7 seam |
| 16 | Quests: Zosilem and Thepem tiered | 7 | 7 | not built | 6 | 5 | two tiered quest chains | no |
| 17 | Boss: Primeval Lich | 6 | 6 | not built | 6 | 5 | champion boss | no |
| 18 | Quests: about ten single quests | 12 | 17 | not built | 9 | 10 | Tyball, Aliabeth, Barreraak, Farmer Nash, Naxatillor, Xenrr, Soulforge ... | no |
| 19 | Boss: Abyssal Infernal | 5 | 5 | not built | 5 | 5 | champion boss | no |
| 20 | Community Collections | 17 | 17 | not built | 17 | 20 | Zoo, Library, Museum: 56 types, 2,885 lines plus 12 NPC files | **no, and Q-064's rule declines it** |
| 21-27 | Dread Horn, Shimmering Effusion, Doom Gauntlet, Travesty, Paroxysmus, ServUO's treasure-map rewrite, gargoyle alteration | 14 | | not built | | 5-20 each | | |
| | **All gates together** | **292 of 372** | | **70 from the 9 built; see the curve** | | | | |

"New files" is the greedy column; "Alone" is what the gate reaches with nothing else built. Of the 219 is from the
"Alone" set. Both count ported content files, costumes excluded. Two gates reach nothing new once the cheap ones are
in, but they are **alternatives, not waste**: the Ter Mur vendor stock (28 files alone, cost 2, section 8) and pinned's
random loot lists (24 alone, cost 1). They sell or drop what blacksmithy makes.

**The cumulative curve, which is the planning number.** As predicted on 2026-09-29, then restated 2026-09-30:

| After | Cost as costed | **Predicted** (2026-09-29) | **Restated**: delivered + still predicted | of which **delivered** | of which **predicted** | Of 372 |
|---|---|---|---|---|---|---|
| gates 1-5 | 5 | 117 (31%) | **65** | 65 (gates 1-5 all attempted) | 0 | **17%** |
| gates 1-9 | 12 | 167 (45%) | **104** | 69 (gates 1-5, 7, 9) | 35 (gate 6: 21, gate 8: 14) | **28%** |
| + Clean Up Britannia | 32 | 214 (58%) | **151** | 69 | 82 (+ gate 10: 47) | **41%** |
| all 27 | about 190 | 292 (78%) | **227** | 70 (+ gates 12, 13) | 157 (the 18 unbuilt gates) | **61%** |

How each restated figure is built: take the predicted figure, remove the greedy predictions of the gates that have been
built (1, 2, 3, 4, 5, 7, 9, 12, 13: **135** predicted), add what they delivered (**70**: 33 + 1 + 0 + 14 + 17 + 2 + 2 +
0 + 1). 292 - 135 + 70 = 227. The delivered files are disjoint: each note measured its gate against its own Appendix A
group, and no file appears in two groups.

**Read the "predicted" part with three cautions.**

1. **It is the old greedy figure, not a new one.** The greedy cover assumed each earlier gate took its predicted files.
   The 65 files that built gates predicted and did not reach (tailoring 25, gate 3's 24, carpentry 6, gate 9's 5,
   tinkering 3, gate 12's 2) are back in the pool, so a later gate whose "Alone" exceeds its greedy figure may now
   reach more than its row says: gates 6 (21 greedy, 36 alone), 8 (14, 19), 11 (4, 6), 14 (3, 5) and 18 (12, 17).
   Which of the 65 they pick up is not known without re-running the cover. **Unverified**, and the only direction in
   which the restated curve may be low.
2. **Each unbuilt row still carries the over-count described in section 3.1**, which pushes the other way. Section
   3.1.3 rates each one.
3. **The 65 undelivered files are not gone, they are behind work nobody has costed**: a recipe source for 25 tailoring
   pieces (`craft-registrations` §2), ServUO's chest logic or its EJ rewrite for gate 3's 24 (`cc-P8` §2.4, a fidelity
   decision for Chase), peerless ingredient drops for six Darkwood pieces, a Corrupt champion placement for the five
   Grizzle pieces (`cc-P7` §2.3). None of that is in the "Cost" column.

**The denominator is the HEAD of 2026-09-29** (340 unreachable + 32 costumes = 372), kept for comparability. The live
tree has grown since (613 ported content files, `craft-registrations` §0), so these percentages describe the audit's
list, not today's tree.

### 3.1 Why the prediction over-counts, and which unbuilt gates to trust

#### 3.1.1 The record

| Gate | Predicted | Delivered | Where the difference went |
|---|---|---|---|
| 1 Blacksmithy | 33 | 33 | nowhere |
| 5 Stealables | 17 | 17 | nowhere (pinned's table is 80 entries, not the 81 above; no file affected) |
| 13 Niporailem | 1 | 1 | nowhere (measured, not predicted: it was built before the audit ran) |
| 4 Tinkering | 17 | 14 | an unobtainable resource (`CrystalShards`), a Doom recipe, and a tool fault that read a first resource as a product |
| 7 Carpentry | 8 | 2 | six Darkwood pieces need peerless ingredients nothing drops |
| 9 Pinned's commented drops | 7 | 2 | Ilhenir's carrier is never placed; the Valley entry needs six absent creatures and an enum ordinal pinned has already planned; Scrapper's rare recipe can never drop |
| 2 Tailoring | 26 | 1 | 25 entries are recipe-gated with no recipe source; several also need resources in neither tree |
| 12 Champion lists, bosses | 2 | 0 | both targets were twins of pinned artifacts players already get |
| 3 Treasure chests | 24 | 0 | pinned has none of the lists; every file needs new chest or map logic, some with absent types |

#### 3.1.2 The mechanism

The instrument answers one question well: **does some ServUO code site put type X in the world, and does the owner of
that site exist in pinned?** Its file lists have mostly held up: across nine built gates, one source turned out not to be a
source (`CrystalShards`, a resource in the `AddCraft` it was credited to, `craft-registrations` §4.1), and one reached
type is not (`Putrefaction`, through a method nothing calls, same section). What the gate figures then assumed, without the instrument ever testing it, is that **finding that site
is the same as delivering X**. That holds only when four further things are true, and every miss above is one of them
failing:

| | Condition | What the instrument did instead | Gates it broke |
|---|---|---|---|
| **A** | **The entry has no second condition.** Once the site runs, X is handed over: no recipe to learn, no resource to find, no points to earn, no objective to meet | counted the reference and stopped. `AddRes` is correctly a read, but whether the resource or recipe can itself be had is a second reachability question the tool never asks (`craft-registrations` §4.2) | 2, 4, 7, 9 (Scrapper) |
| **B** | **The carrier is live.** Whatever runs the site (a boss, a chest, a spawner) is itself placed in a world, not merely a type that exists | treated a pinned owner type as a live owner. Ilhenir exists and is never spawned; no treasure map points at Eodon | 9 (Ilhenir), 3 (guardians) |
| **C** | **Pinned's owner has the same mechanism.** A cost of "1: entries in a pinned list" needs the list | "owner: pinned" meant only that pinned declares the type; the hand grouping read it as "a patch into pinned's list" | 3 (all 24), 12 |
| **D** | **Nothing absent or duplicated rides along.** The same entry needs no type in neither tree, and X is not a twin of something pinned already reaches | resolved by name only, and did not look at the rest of the entry | 9 (Valley), 12 (twins), 3 (absent essences and specials) |

A and B are **one-hop blindness** in the instrument: it follows the edge into X and never the edges into the site's own
preconditions. C and D are **costing and grouping errors** made by hand on top of it (`gatemap.py`), and section 6
never listed them. Section 6's "Recipe IDs, 13 files" row was the only warning of A, and it undercounted by half in
tailoring alone.

**Why gates 1 and 5 hit exactly.** In both, the source is *terminal*: its only precondition is something already known
to be in play, and pinned has the identical slot.

- **Blacksmithy:** every entry takes iron ingots and nothing else, no recipe (A). The carrier is a player with a skill
  and a stock tool (B). Pinned's `CraftSystem` takes appended entries, and three hooks already did it (C). All 34 types
  are ours, none a twin (D).
- **Stealables:** each entry *is* its own carrier, a fixed spawn at a fixed point, and the spawner is enabled on the live
  world (B). Stealing it needs Stealing 100 and a weight under 10, both checked (A). Pinned ships the same table and
  P8 appended to it (C). ServUO's entries with absent types (11) were already outside the 17 files (D).

That is the test to apply to a prediction before it is briefed: **is the source terminal, and does pinned have the
slot?** A craft entry is terminal only if its resources are stock and it has no recipe. A drop is terminal only if the
creature is spawned. A reward table is terminal only if the currency can be earned.

#### 3.1.3 The unbuilt gates, rated

**Sound** means the source looks terminal on what is already written down; **suspect** means a condition above is
known or likely to fail; **count sound, cost wrong** means the files will come but the "Cost" column is not the work.
A rating from existing notes and the table's own text, not a re-measurement.

| Gate | Predicted | Rating | Why |
|---|---|---|---|
| 6 Imbuing drops | 21 | **suspect, and low value** | a direct drop on death (A holds), but each reagent drops only from particular creature types, and whether each is spawned is unchecked (B). Pinned's death event lacks the corpse and killer (C, already noted). Worthless in play without imbuing either way |
| 8 ToL drops + Eodon spawns | 14 | **mostly sound if both halves are built together** | ServUO drops the 12 set pieces directly by `Loot.Construct` (`TimeOfLegends.cs:98-133`, A holds), but only for kills inside Eodon (`SpellHelper.IsEodon`), at Fame/1,000,000 plus luck. The spawn half is pure placement, the stealables shape. Check pinned's death-event arguments and `IsEodon` first. May also pick up gate 3's four dinosaurs and banana (alone 19), unverified |
| 10 Clean Up Britannia | 47 | **count probably sound; cost is the risk** | a reward table is terminal once points can be earned, and turn-ins are mostly stock items. The unknown is the 20 units, which nothing here tests. Check the reward list for absent types (D) before briefing |
| 11 Other crafts | 4 | **suspect** | exactly tailoring's shape. Run `craft-registrations`' `parse_defs.py` over the four `Def*` files for recipes and resources before briefing |
| 14 Underworld generator | 3 | **suspect** | a chain: placement, then the fountain's reward code, then the satchel, then reagents. Each link is a second condition |
| 15 Virtue Artifacts | 7 | **count probably sound; cost depends on S7** | a system that hands out a list; points are earned by play. S7 is unbuilt and shared with Shame's altars |
| 16, 18 Quests | 7, 12 | **suspect until each chain is read** | a reward is terminal only if the giver is placed (B) and every objective is reachable (A). Neither has been checked for any of these quests |
| 17, 19 Primeval Lich, Abyssal Infernal | 6, 5 | **count sound, cost wrong** | both are champion bosses (ServUO `ChampionSpawnType.cs:147,154`): Ilhenir's failure (B) unless a champion spawn of their type is placed. `cc-P7` §2.4 shows those types collide with pinned's commented enum ordinals and must be built with Valley as one piece, not 5 units each |
| 20 Community Collections | 17 | declined (Q-064) | |
| 21-27 | 14 | **suspect** | peerless bosses need placement and keys (Lissith's silk is a peerless key in neither tree, `cc-P7` §2.2); the treasure-map rewrite is gate 3's fidelity fork |

**Before briefing any gate: apply A-D to each file's source in writing, and brief the number that survives.** That is a
reading task of an hour or so per gate, much cheaper than re-running the instrument, and it would have caught every miss
in 3.1.1. Extending the instrument to follow second hops (recipes, resources, carrier placement) would be a new
measurement; it is not needed to plan the next few gates.

### Not worth it, and saying so

- **Community Collections.** 17 files for a 20-unit subsystem, and Q-064 already said no collection system. Leave. It
  is also where 10 of the 16 twin-shaped questions live (section 4).
- **Peerless and champion bosses for one or two items each**: Dread Horn (2), Shimmering Effusion (2), Travesty (1),
  Chief Paroxysmus (1). Leave unless the boss is wanted for itself.
- **Gargoyle alteration.** 33 files alone, but 32 of them are reached more cheaply by gate 1. Its unique yield is
  one file, for about 10 units. Leave.
- **ServUO's treasure-map rewrite (`TreasureMapInfo`).** 24 files alone; after gate 3, three. Leave.
- **Mini champions, Huntmaster, Pet Training, VvV and Factions rewards, High Seas SOS artifacts.** Everything they
  would add is already reached by a cheaper gate. Build them for their own sake or not at all.
- **Imbuing ingredient drops (gate 6)** rank sixth on files and are nearly worthless in play until imbuing exists. I
  would move them down.
- **The 80 behind no gate.** 62 have no source in ServUO either: 32 staff costumes; the Initiation bag and Phoenix
  ticket (2), which also strands the 12 set pieces they hand out; and 28 items ServUO also ships unobtainable, such as
  `CloakOfDeath`, `AnniversaryRobe`, `ConjurersGrimoire` and `TheRedeemer`. **These are D32's case: in the type table
  and in no player's hands, by ServUO's own design.** The last 6 hang on one unported thing each (`TyballsShadow`,
  `OrcChopper`, `GargishWarrior`, `VendorSearch`, the `GMbody` command, and `RangersCloakOfAugmentation`, itself
  sourceless). Appendix A lists all 80.

---

## 4. The twin sweep

`--twins` runs three independent tests on our types against pinned's: **case** (same name in another case, since
`FindTypeByName` ignores case, `AssemblyHandler.cs:189`), **alias** (a pinned `[TypeAlias]` string naming ours), and
**art plus cliloc**, then **cliloc alone** (a named item's cliloc is close to unique). Result: **0 case, 2 alias,
0 art-plus-cliloc, 14 cliloc.** `MysticBook` and `JesterHatOfChuckles` are absent because CC9 declined to port them.

| Ours | Pinned | Test | My read |
|---|---|---|---|
| `GauntletsOfAnger` (`Items/Artifacts/Equipment/Armor/`) | **`GuantletsOfAnger`** (`Champion Artifacts/Shared/`), cliloc 1094902 | cliloc | **A twin.** Pinned misspells the class. ServUO has only ours. Pinned's is the reachable one, through champion spawns; ours is unreachable |
| `ShroudOfDeceit` (file `ShroudOfDeciet.cs`) | **`ShroudOfDeciet`** (file `ShroudOfDeceit.cs`), cliloc 1094914 | cliloc | **A twin.** The spellings are swapped between file and class in the two trees. Same shape as above |
| `GargoyleAlchemist` (`ClusterFGargoyleVendors.cs`) | `[TypeAlias("Server.Mobiles.GargoyleAlchemist")]` on `Glassblower` | alias | **Same full name, exactly.** See section 8.1 |
| `GargoyleStoneCrafter` (same file) | `[TypeAlias("Server.Mobiles.GargoyleStonecrafter")]` on `StoneCrafter` | alias | Same name in another case. `FindTypeByName` ignores case, so it collides; the full-name map does not |
| `HumanFeyLeggings` | `FeyLeggings`, cliloc 1075041 | cliloc | **Not a twin.** ServUO keeps both classes; ours is its Factions reward |
| the five Library glasses and their five gargish forms | `ArtsGlasses`, `MaceShieldGlasses`, `TradeGlasses`, `TreasureTrinketGlasses`, `WizardsGlasses` | cliloc | **Not twins.** ServUO keeps both: the Library ones are hued collection rewards (`Zorda.cs:109`) |
| `SmithGuildSalvageBag` | `SalvageBag`, cliloc 1079931 | cliloc | Ours, custom, different art. Not a twin |

The cliloc test covers **526 of 891** content types (the rest inherit their cliloc or set it another way), and art plus
cliloc covers 303. So "0 art-plus-cliloc hits" means none in 303, not none. Nothing was deleted.

---

## 5. Does Q-048 fall out of this? Half of it does.

**The half it answers: how ported content reaches the world.** Of the **296** reachable ported content types at HEAD,
every one comes through one of three channels, and there are no others:

| Channel | Types | Of which only this way | Runs by itself? |
|---|---|---|---|
| **Pinned spawn JSON**: `termur/Abyss.json` 140, `TerMur.json` 28, `Underworld.json` 22, `malas/Citadel.json` 7, `Labyrinth.json` 4, `Sanctuary.json` 3 per facet, `PrismOfLight.json` 2 per facet, `Vendors.json` and `trammel/Outdoors.json` 1 each | **204** | 198 | **No.** Only when `[GenerateSpawners` has been run for that file on that world |
| **Two GM commands**: `[GenerateNewShame` (41), `[SetupDespise` (37) | **78** | 78 | **No.** Administrator and GameMaster commands, run once per world |
| **Our startup hooks**: Athenaeum Isle quest registration (13), the New Haven board (1), the incubator recipe | **15** | 14 | Yes |

(6 types come by more than one channel.) Pinned code reaches **no** ported type, and neither do our patches.

**So on this shard, ported content reaches the world by world generation, not by code.** 282 of 296 exist only on a
world where someone ran the right commands. Abyss.json alone carries 140, which is the whole Stygian Abyss creature
port and its loot.

**The half it cannot answer: which of those commands have been run on the world a player is in.** That is a fact about
a save, and this task read none. Q-048's answer established the four termur/trammel files are in the live save. It did
not establish `[GenerateNewShame` or `[SetupDespise`.

**What that means for a fresh world, if that is where the live shard is going (section 7, item 3):** these 296 types
need, as runbook steps, `[GenerateSpawners` for `post-uoml/termur/{Abyss,TerMur,Underworld}.json`,
`shared/malas/{Citadel,Labyrinth}.json`, `shared/{trammel,felucca}/{Sanctuary,PrismOfLight}.json`,
`post-uoml/{trammel,felucca}/Vendors.json` and `post-uoml/trammel/Outdoors.json`, then `[GenerateNewShame` and
`[SetupDespise`. `docker/uo/SERVER.md:355-357`'s three patterns cover every spawn file. Nothing covers the two
commands. **Spawn data is not the only thing placing creatures at world generation.** Shame and Despise place 78 types
through their own generators, and on a fresh world those generators have to be run by hand.

**What would answer the rest:** a runbook for world creation that the deploy follows, or, for the live world, a count
of `Shame_Revamped` and `DespiseRevamped` spawners in the save.

---

## 6. What the instrument still cannot see

| Blind spot | Count | Which way it errs |
|---|---|---|
| **The save.** Anything a GM placed with `[add` (the fountain, S2 D-3) or that survives from before | unknown. 31 unreachable files are addons or decoratives, the likeliest candidates | calls them unreachable when a placed copy exists |
| **Which generation commands a world has had** (section 5) | 282 reachable types depend on it | calls them reachable when that world has not had them |
| **Recipe IDs.** A recipe-gated `AddCraft` counts as reach | 13 files (D32's garments in gate 2) | overstates gate 2 by 13. *(2026-09-30: by 25, and resources overstate too; section 3.1)* |
| **`typeof` at a site with no name** | 73 reached types; 18 files read, all genuine | could overstate reach |
| **The reader list is judgment**: 17 site names, each read | a ServUO reader missing from it overstates a gate; one wrongly on it understates one | both |
| **Resolution by name.** A ServUO source with our type's name but a different class | not measured; the 219 had none by hand | overstates gates |
| **A type named only as a generic argument** | 1 (`WardensCrook`, custom) | may understate reach |
| **Our `new` inside a `Deserialize` body counts as reach** | 2, both non-content | overstates |
| **Dynamic lookups by a computed name** | 6 in ours, all read and all resolved; 40 in pinned, not read | may understate |
| **Twin sweep** | cliloc read on 526 of 891 content types; art only as a literal first `base(...)` argument | misses twins |
| **Costs** | line counts and wiring, nothing built | rough, by construction |

---

## 7. What the brief restated wrongly, and what I stated wrongly first

1. **"29% of the ported tree."** A faithful quote of D33, which quoted me, and wrong in kind: 219 filtered files over
   768 unfiltered ones (section 1.2). **Exact: 340 of 570, 60%.**
2. **"Of CC9's 24 remaining upstream files ... a patch ... would put one of them in a player's hands"** is a faithful
   quote. **But the gating in that section of my note was wrong for 12 of the 24**, and so was §4's closing claim,
   "Clean Up Britannia ... is named as a source by 12 of these 28". Every Clean Up citation in `cc9-close.md` §1, §4
   and §6 (21 types, among them `ImprisonedDog`, `AnkhPendant`, the Corgul handbook and the five Virtue pieces) is
   `CleanUpBritanniaData.Entries`: **the points a player earns by turning an item in** (`CleanUpBritanniaData.cs:47-49`).
   None of them is in the reward table. Re-derived with the corrected instrument:

   | CC9 `upstream` files | What actually gates them |
   |---|---|
   | `LordBlackthornsExemplar`, `SentinelsGuard`, `DragonsEnd`, `JaanasStaff`, `KatrinasCrook` | **Virtue Artifacts system only** (gate 15: 122 lines plus S7) |
   | `StaffOfShatteredDreams`, `ConjurersTrinket` | **no source at all**, in ServUO either. My note had "Clean Up only" |
   | `SurgeShield`, `RunedSashOfWarding`, `ManaPhasingOrb` | treasure chests (gate 3, a pinned list) or ServUO's rewrite |
   | `AbyssalBlade`, `DeathsHead` | Abyssal Infernal only |
   | `CompassionArms` ... `SacrificeSollerets` (the five Virtue pieces already in our tree, §6) | the Virtue Artifacts system, not Clean Up |

   The §7 sample survives: the Knights, Scout, Sorcerer and Bestial pieces are genuine Clean Up **rewards**, and gate 10
   agrees. The "Luck" piece I cannot now identify from the note.
3. **"The live shard is being rebuilt on a fresh world."** That is outside what I can check, but it contradicts
   AGENTS.md ("no fresh world", rule 7) and `docs/direction-decision.md:38`. If it is right, both documents need the
   change recorded, and section 5's runbook list is the part of this audit that matters most. If it is wrong, section
   5 still stands for the test shard, which is rebuilt fresh routinely.
4. **"Spawn data is the only thing placing creatures at world generation."** Shame and Despise place 78 types,
   creatures among them, through their own commands (section 5).
5. **"Walking [craft tables] is probably the single highest-value part of this task."** Right. The craft gates are 1, 2,
   4 and 7 of the ranking, **90 files alone** for four hook files. *(2026-09-30: the table sums to 84, and 50 were
delivered; `craft-registrations` §0, §6.2.)*

---

## 8. Found in passing, written down and not acted on

1. **`GargoyleAlchemist` shares a full name with a pinned alias.** Ours is `Server.Mobiles.GargoyleAlchemist`
   (`ClusterFGargoyleVendors.cs:37`). Pinned's `Glassblower` carries `[TypeAlias("Server.Mobiles.GargoyleAlchemist")]`
   (`Mobiles/Vendors/NPC/Glassblower.cs:6`). `TypeCache` files an alias under its full name in the **same** maps as
   real types (`AssemblyHandler.cs:251-263`), and `FindTypeByName`/`FindTypeByHash` return the **first** type in the
   bucket (`:188-228`). Which one comes first is an ordering fact I cannot read from source. If saves resolve types
   through that map, a saved `GargoyleAlchemist` could come back as a `Glassblower`. **Unverified. The shape of a
   probe:** one test fact asserting `AssemblyHandler.FindTypeByFullName("Server.Mobiles.GargoyleAlchemist", false) ==
   typeof(GargoyleAlchemist)`, then the same for a save round trip. `GargoyleStoneCrafter` collides only
   case-insensitively. Neither name is in any spawn file.
2. **Gargoyle basics are unobtainable.** Gargish plate armour (8 pieces), 21 gargish weapons, three gargish shields
   and gargish jewellery are in our tree and in no player's reach, on a shard whose `expansion.json` has SA on and a
   gargoyle race. Pinned's blacksmithy, tinkering, Ter Mur vendors, random loot lists and character creation all lack
   them. This is gates 1 and 4, and it is probably the most visible gap in this whole audit to anyone playing a
   gargoyle.
3. **The Ter Mur vendor gate can avoid a patch.** ServUO adds `SBSAWeapons`/`SBSAArmor` to `Blacksmith` when on Ter Mur
   (`Mobiles/NPCs/Blacksmith.cs:67-69`), which would be a patch to pinned. Our `GargoyleArmorer` and
   `GargoyleWeaponsmith` (`ClusterFGargoyleVendors.cs`) are already seeded in the Royal City (`ClusterFRoyalCitySeeder`),
   so an `InitSBInfo` override on them is additive. That is a deviation in *which* vendor sells it, so it belongs in
   `docs/fidelity-principle.md` if chosen.
4. **Pinned has hooks written and waiting on our types** (gate 9). Five places under a `TODO: uncomment once added`,
   and `ChampionSpawnInfo`'s commented-out champion list. The cheapest kind of patch there is: pinned wrote the code.
5. **For D33 and D32 when promoted:** D33's "29%" and its "gated on Clean Up Britannia" both need correcting (section
   7). D32's thirteen belong under gate 2 (tailoring), gate 8 (recipe drops) and Q-066 (the resources), all three.
6. **Two ported artifacts duplicate pinned ones** (section 4): `GauntletsOfAnger` and `ShroudOfDeceit`. Unreachable,
   so no player holds a duplicate, but the type table claims content pinned already has, reachably.

---

## 9. Proof, reproduction, files

**`--legacy` did not move**, confirmed after every change and again at the end, against ShatteredLegacy `b21bcd9`
(198 `.cs`): **567 / 320 / 81 / 10 / 44, 1,022 of 1,022** in S9's bucket. The `Index`/`row` code paths were not edited.
The additions are the `reach` section, `blank`, `type_facts`, `twins`, `servuo_sources`, a `reach` CLI, and a
`CONTENT_INDEX_OURS` default.

**Tests: 25, all green** on the HEAD export (16 before, 9 new):
`CONTENT_INDEX_OURS=<export>/server/customizations python -m unittest tools/test_content_index.py`.

**Red, each fact watched failing.** A script (`red.py`, scratch) wrote nine copies of the tool, each with one rule
reverted, and ran the full suite against each:

```
case-insensitive spawn     -> FAILED (errors=1)             test_reach_spawn_entries_resolve_case_insensitively
static access              -> FAILED (failures=1, errors=1) test_reach_a_string_table_read_by_static_access_creates_its_entries,
                                                            test_reach_static_access_runs_no_instance_code
acting rule                -> FAILED (failures=1)           test_reach_static_access_runs_no_instance_code
reader: IngredTypes        -> FAILED (failures=1)           test_reach_a_list_that_reads_types_does_not_create_them
reader: Entries            -> FAILED (failures=1)           test_reach_servuo_turn_in_table_is_not_a_source
constructible base         -> FAILED (failures=1)           test_reach_a_base_is_reached_through_children_unless_it_is_an_item_itself
data whitelist             -> FAILED (failures=1)           test_reach_a_data_file_that_only_lists_names_places_nothing
pinned comments            -> FAILED (failures=1)           test_reach_pinned_code_left_commented_out_is_reported
twins cliloc               -> FAILED (failures=1)           test_twin_sweep_finds_a_pinned_type_under_a_misspelling
```

Every revert reddened its own fact and no other, apart from one expected pair: reverting static access also reddens
the fountain fact, because the fountain is then not live at all. My first red run also errored the S9 reproduction
in every copy, because the copies could not find `notes/`. That was a harness fault, fixed, and the second run is the
one above. The `Entries` fact was green under its own revert on the first run: `BestialArms` is not in the turn-in
table. It now also asserts `AntiqueWeddingDress`, which is.

**These facts are about the tree as it stands**, like the shard's spawn-orphan facts, and they are meant to move when
a gate is built. Change the expectation then, with a line saying which gate did it.

**Reproduce:**

```
git -C D:\ShatteredLegacy archive HEAD server | tar -x -C <dir>
python tools/content_index.py reach --ours <dir>/server/customizations --sources --twins
python tools/content_index.py row artifacts --legacy --ours <export of b21bcd9>/server/customizations
python tools/content_index.py compare-s9 artifacts --ours <export of b21bcd9>/server/customizations
```

The gate grouping, what-ifs and greedy ranking are scratch scripts over the tool (`gatemap.py`, `gates2.py`,
`gates3.py`, `greedy.py` in this session's scratchpad), because the grouping is judgment. The per-source what-if
ranking they start from is `reach --sources`.

**Files changed:** `tools/content_index.py`, `tools/test_content_index.py`, this note. **Not done:** no commit (brief);
`tools/progress.py` not run (it rewrites `README.md` and `tools/progress.json`, which other tasks have modified in this
working tree); `docs/` not touched. Numbering: no D-number or Q-number taken. Section 8.1 is Q-shaped and section 7
item 3 is Chase's.

---

## Appendix A. Every unreachable ported content file at HEAD, under the gate that reaches it first

*(2026-09-30: this is HEAD as measured on 2026-09-29. 70 of these files have since been delivered by built gates;
section 3's "Delivered" column says which groups and where each is recorded.)*

Greedy order, as in section 3. *(not in the 219: reason)* marks the 121 the rough pass counted as named.
340 files. The 32 costumes follow, outside the 340.

**Craft: blacksmithy registration** (33)

- `Items/Equipment/Armor/FemaleGargishPlateArms.cs`
- `Items/Equipment/Armor/FemaleGargishPlateChest.cs`
- `Items/Equipment/Armor/FemaleGargishPlateKilt.cs`
- `Items/Equipment/Armor/FemaleGargishPlateLegs.cs`
- `Items/Equipment/Armor/GargishChaosShield.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/GargishKiteShield.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/GargishOrderShield.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/GargishPlateArms.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/GargishPlateChest.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/GargishPlateKilt.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/GargishPlateLegs.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/LargePlateShield.cs`
- `Items/Equipment/Armor/MediumPlateShield.cs`
- `Items/Equipment/Armor/SmallPlateShield.cs`
- `Items/Equipment/Weapons/GargishAxe.cs`
- `Items/Equipment/Weapons/GargishBardiche.cs`
- `Items/Equipment/Weapons/GargishBattleAxe.cs`
- `Items/Equipment/Weapons/GargishBoneHarvester.cs`
- `Items/Equipment/Weapons/GargishDagger.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Weapons/GargishDaisho.cs`
- `Items/Equipment/Weapons/GargishKatana.cs`
- `Items/Equipment/Weapons/GargishKryss.cs`
- `Items/Equipment/Weapons/GargishLance.cs`
- `Items/Equipment/Weapons/GargishMaul.cs`
- `Items/Equipment/Weapons/GargishPike.cs`
- `Items/Equipment/Weapons/GargishScythe.cs`
- `Items/Equipment/Weapons/GargishTekagi.cs`
- `Items/Equipment/Weapons/GargishTessen.cs`
- `Items/Equipment/Weapons/GargishWarFork.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Weapons/GargishWarHammer.cs`
- `Items/Equipment/Weapons/Shortblade.cs` *(not in the 219: named only as a base class)*
- `Items/Resource/CrushedGlass.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/PowderedIron.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*

**Craft: tailoring registration** (26)

- `Items/Armor/TigerPeltBustier.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltChest.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltCollar.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltHelm.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltLegs.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltLongSkirt.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltShorts.cs` *(not in the 219: named only as a base class)*
- `Items/Armor/TigerPeltSkirt.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/AssassinsCowl.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/CowlOfTheMaceAndShield.cs`
- `Items/Equipment/Armor/CrimsonDaggerBelt.cs`
- `Items/Equipment/Armor/CrimsonMaceBelt.cs`
- `Items/Equipment/Armor/CrimsonSwordBelt.cs`
- `Items/Equipment/Armor/DragonTurtleHideArms.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/DragonTurtleHideBustier.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/DragonTurtleHideChest.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/DragonTurtleHideHelm.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/DragonTurtleHideLegs.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/ElegantCollar.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/ElegantCollarOfFortune.cs`
- `Items/Equipment/Armor/MagesHood.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/MagesHoodOfScholarlyInsight.cs`
- `Items/Equipment/Clothing/DaggerBelt.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Clothing/LeatherTalons.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Clothing/MaceBelt.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Clothing/SwordBelt.cs` *(not in the 219: named only as a base class)*

**Treasure chests: entries in pinned lists (patch)** (24)

- `Items/Artifacts/Consumables/GrapeBunch.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Decorative/CoffinPiece.cs`
- `Items/Artifacts/Decorative/CreepingVine.cs`
- `Items/Artifacts/Decorative/GrapeVine.cs`
- `Items/Artifacts/Decorative/LargeFishingNet.cs`
- `Items/Artifacts/Equipment/Armor/KelpWovenLeggings.cs`
- `Items/Artifacts/Equipment/Armor/ValkryieArmor.cs`
- `Items/Artifacts/Equipment/Clothing/AntiqueWeddingDress.cs`
- `Items/Artifacts/Equipment/Weapons/RunedDriftwoodBow.cs`
- `Items/Consumables/PerfectBanana.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Resource/EssenceAchievement.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceBalance.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceControl.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceDiligence.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceDirection.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceFeeling.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceOrder.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssencePassion.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssencePrecision.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/EssenceSingularity.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Mobiles/Normal/Allosaurus.cs` *(not in the 219: named only by a data file that places nothing)*
- `Mobiles/Normal/Dimetrosaur.cs` *(not in the 219: named only by a data file that places nothing)*
- `Mobiles/Normal/Saurosaurus.cs` *(not in the 219: named only by a data file that places nothing)*
- `Mobiles/Normal/SilverbackGorilla.cs` *(not in the 219: named only in pinned code left commented out)*

**Craft: tinkering registration** (17)

- `Items/Artifacts/Equipment/Jewelry/BraceletOfPrimalConsumption.cs`
- `Items/Equipment/Jewelry/BlueDiamondRing.cs`
- `Items/Equipment/Jewelry/BrilliantAmberBracelet.cs`
- `Items/Equipment/Jewelry/DarkSapphireBracelet.cs`
- `Items/Equipment/Jewelry/EcruCitrineRing.cs`
- `Items/Equipment/Jewelry/FireRubyBracelet.cs`
- `Items/Equipment/Jewelry/GargishBracelet.cs`
- `Items/Equipment/Jewelry/GargishEarrings.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Jewelry/GargishRing.cs`
- `Items/Equipment/Jewelry/PerfectEmeraldRing.cs`
- `Items/Equipment/Jewelry/TurqouiseRing.cs`
- `Items/Equipment/Jewelry/WhitePearlBracelet.cs`
- `Items/Equipment/Weapons/GargishButcherKnife.cs`
- `Items/Equipment/Weapons/GargishCleaver.cs`
- `Items/Resource/ArcanicRuneStone.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/CrystalShards.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/VoidOrb.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*

**Stealable artifacts: entries in pinned table (patch)** (17)

- `Items/Artifacts/Decorative/CarvedMyrmydexGlyph.cs`
- `Items/Artifacts/Decorative/DragonTurtleHatchlingNet.cs`
- `Items/Artifacts/Decorative/FigureheadOfBmvArarat.cs`
- `Items/Artifacts/Decorative/GildedStatue.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Decorative/KingsPainting.cs`
- `Items/Artifacts/Decorative/SADecorationArtifacts.cs`
- `Items/Artifacts/Decorative/SacredLavaRock.cs`
- `Items/Artifacts/Decorative/ShipsBellOfBmvArarat.cs`
- `Items/Artifacts/Decorative/SternAnchorOfBmvArarat.cs`
- `Items/Artifacts/Decorative/StretchedDinosaurHide.cs`
- `Items/Artifacts/Decorative/WakuOnASpit.cs`
- `Items/Artifacts/Decorative/WhiteTigerFigurine.cs`
- `Items/Artifacts/Equipment/Armor/CrownOfArcaneTemperament.cs`
- `Items/Artifacts/Equipment/Armor/MysticsGuard.cs`
- `Items/Artifacts/Equipment/Weapons/LightInTheVoid.cs`
- `Items/Artifacts/Equipment/Weapons/StaffOfResonance.cs`
- `Items/Artifacts/Equipment/Weapons/ValkyriesGlaive.cs`

**Imbuing ingredient drops (ResourceDrops, 252 lines, death hook)** (21)

- `Items/Quest/BouraPelt.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Quest/EnchantedEssence.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Quest/MagicalResidue.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Quest/RelicFragment.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/BottleIchor.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/ChagaMushroom.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/CrystallineBlackrock.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/DaemonClaw.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/DelicateScales.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/ElvenFletching.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/FaeryDust.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/GoblinBlood.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/LavaSerpentCrust.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/RaptorTeeth.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/ReflectiveWolfEye.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/SeedOfRenewal.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/SilverSnakeSkin.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/SlithTongue.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/SpiderCarapace.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/UndyingFlesh.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*
- `Items/Resource/VialOfVitriol.cs` *(not in the 219: named only by a list that reads types (is, GetAmount, accept-lists))*

**Craft: carpentry registration** (8)

- `Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodCrown.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodGauntlets.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodLeggings.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Darkwood/DarkwoodPauldrons.cs`
- `Items/Equipment/Instruments/AudChar.cs`
- `Items/Equipment/Weapons/GargishGnarledStaff.cs`

**Time of Legends drops (death hook) + Eodon spawn table** (14)

- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsBustier.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsHelm.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLegs.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsLongSkirt.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsSkirt.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsTunic.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensBustier.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensHelm.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensLegs.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensSleeves.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Dardens Set/DardensTunic.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Mobiles/Normal/Archaeosaurus.cs` *(not in the 219: named only by a data file that places nothing)*
- `Mobiles/Normal/Najasaurus.cs` *(not in the 219: named only by a data file that places nothing)*

**Pinned TODO drops, uncommented (Ilhenir, Lissith, Miasma; champion list; inscription)** (7)

- `Items/Artifacts/Equipment/Armor/Sets/Acolyte/GreymistChest.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleGauntlets.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleGreaves.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleHelm.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleTunic.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Artifacts/Equipment/Armor/Sets/Grizzle/GrizzleVambraces.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonGloves.cs` *(not in the 219: named only in pinned code left commented out)*

**Clean Up Britannia (rewards; 52 files, 5,161 lines + data)** (47)

- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialArms.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialEarrings.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialGloves.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialHelm.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialKilt.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialLegs.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialNecklace.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsBascinet.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsCloseHelm.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsFemalePlateChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsNorseHelm.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateArms.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateGloves.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateHelm.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Knights/KnightsPlateLegs.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Luck/EtoileBleue.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Luck/LuneRouge.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Luck/NovoBleue.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Luck/SoleilRouge.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutArms.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutBustier.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutCirclet.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutFemaleChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutGloves.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutLegs.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Scout/ScoutSmallPlateJingasa.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererArms.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererFemaleChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererGloves.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererHat.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererLegs.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Sorcerers/SorcererSkirt.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososArmbands.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososCap.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososCollar.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososEarpieces.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososKidGloves.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososKilt.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososNecklace.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososTunic.cs`

**Craft: alchemy, masonry, bowcraft, inscription registrations** (4)

- `Items/Artifacts/Equipment/Spellbooks/ScrappersCompendium.cs` *(not in the 219: named only in pinned code left commented out)*
- `Items/Equipment/Armor/LargeStoneShield.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Jewelry/GargishNecklace.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Weapons/StoneWarSword.cs`

**Pinned champion lists and bosses (patch)** (2)

- `Items/Artifacts/Equipment/Armor/GauntletsOfAnger.cs`
- `Items/Artifacts/Equipment/Armor/ShroudOfDeciet.cs`

**Niporailem (CC9 close; built, uncommitted)** (1)

- `Items/Artifacts/Equipment/Armor/Sets/Epiphany/VillainousEpiphany.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*

**Underworld generator (Fountain of Fortune placement)** (3)

- `Items/Addons/FountainOfFortune.cs` *(not in the 219: named only by static access or reads)*
- `Items/Artifacts/Equipment/Clothing/SolesOfProvidence.cs` *(not in the 219: named only by new)*
- `Items/Containers/GemologistsSatchel.cs` *(not in the 219: named only by new)*

**Virtue Artifacts points system (122 lines + S7 PointsSystem, 463)** (7)

- `Items/Artifacts/Decorative/MapOfTheKnownWorld.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Decorative/TenthAnniversarySculpture.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtue/CompassionArms.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtue/HonestyGorget.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtue/HonorLegs.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtue/JusticeBreastplate.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtue/SacrificeSollerets.cs`

**Quests: tiered (Zosilem, Thepem)** (7)

- `Items/Artifacts/Consumables/ElixirofAgapiteConversion.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Consumables/ElixirofGoldConversion.cs`
- `Items/Artifacts/Consumables/ElixirofMetalConversion.cs`
- `Items/Artifacts/Consumables/ElixirofValoriteConversion.cs`
- `Items/Artifacts/Consumables/ElixirofVeriteConversion.cs`
- `Items/Artifacts/Consumables/InfusedAlchemistsGem.cs`
- `Items/Artifacts/Equipment/Weapons/InfusedGlassStave.cs`

**Boss: Primeval Lich** (6)

- `Items/Artifacts/Decorative/MummifiedCorpse.cs`
- `Items/Artifacts/Equipment/Armor/CastOffZombieSkin.cs`
- `Items/Artifacts/Equipment/Armor/LightsRampart.cs`
- `Items/Artifacts/Equipment/Armor/ProtectoroftheBattleMage.cs`
- `Items/Artifacts/Equipment/Weapons/BansheesCall.cs`
- `Items/Artifacts/Equipment/Weapons/ChannelersDefender.cs`

**Quests: other (about ten single quests)** (12)

- `Items/Artifacts/Consumables/GobletOfCelebration.cs`
- `Items/Artifacts/Equipment/Armor/ResonantShieldOfVengeance.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Virtue/HumilityCloak.cs`
- `Items/Artifacts/Equipment/Clothing/SashOfMight.cs`
- `Items/Artifacts/Equipment/Jewelry/AmuletOfRighteousness.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Jewelry/BarreraakRing.cs`
- `Items/Artifacts/Equipment/Jewelry/NecklaceofDiligence.cs`
- `Items/Artifacts/Equipment/Weapons/FNPitchfork.cs`
- `Items/Artifacts/Equipment/Weapons/WindOfCorruption.cs`
- `Items/Artifacts/Tools/XenrrFishingPole.cs`
- `Items/Quest/ArielHavenWritofMembership.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Mobiles/Bosses/Navery/EyeOfNavrey.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*

**Boss: Abyssal Infernal** (5)

- `Items/Artifacts/Equipment/Armor/TongueoftheBeast.cs`
- `Items/Artifacts/Equipment/Armor/WallOfHungryMouths.cs`
- `Items/Artifacts/Equipment/Clothing/MagicalDoor.cs`
- `Items/Artifacts/Equipment/Clothing/RoyalGuardInvestigatorCloak.cs`
- `Items/Artifacts/Equipment/Jewelry/JadeArmband.cs`

**Community Collections (Zoo, Library, Museum; 2,885 lines + 12 NPCs)** (17)

- `Items/Artifacts/Decorative/BakeKitsuneStatue.cs`
- `Items/Artifacts/Decorative/ChangelingStatue.cs`
- `Items/Artifacts/Decorative/CollectionsBritLibraryMisc.cs`
- `Items/Artifacts/Decorative/LordBritishThroneAddon.cs`
- `Items/Artifacts/Decorative/PolarBearStatue.cs`
- `Items/Artifacts/Decorative/QuagmireStatue.cs`
- `Items/Artifacts/Decorative/ReptalonStatue.cs`
- `Items/Artifacts/Decorative/SnakeStatue.cs`
- `Items/Artifacts/Decorative/WolfStatue.cs`
- `Items/Artifacts/Equipment/Armor/MuseumArmor.cs`
- `Items/Artifacts/Equipment/Armor/RoyalZooLeatherArmor.cs`
- `Items/Artifacts/Equipment/Armor/RoyalZooPlateArmor.cs`
- `Items/Artifacts/Equipment/Armor/RoyalZooStuddedArmor.cs`
- `Items/Artifacts/Equipment/Glasses/CollectionsBritLibraryGlasses.cs`
- `Items/Artifacts/Equipment/Jewelry/MuseumJewlery.cs`
- `Items/Artifacts/Equipment/Spellbooks/ClaininsSpellbook.cs`
- `Items/Equipment/Talismans/CollectionsBritLibraryTalismans.cs`

**Boss: Dread Horn (peerless)** (2)

- `Items/Artifacts/Equipment/Instruments/DreadFlute.cs`
- `Items/Artifacts/Equipment/Weapons/DreadsRevenge.cs`

**Boss: Shimmering Effusion (peerless)** (2)

- `Items/Artifacts/Decorative/FerretImprisonedInCrystal.cs`
- `Items/Artifacts/Equipment/Jewelry/CrystallineRing.cs`

**Doom Gauntlet / Vrulkax points** (4)

- `Items/Artifacts/Equipment/Armor/BritchesOfWarding.cs`
- `Items/Artifacts/Equipment/Armor/CuffsOfTheArchmage.cs`
- `Items/Artifacts/Equipment/Armor/GlovesOfFeudalGrip.cs`
- `Items/Artifacts/Equipment/Clothing/TheScholarsHalo.cs`

**Boss: Travesty (peerless)** (1)

- `Items/Artifacts/Equipment/Clothing/MarkOfTravesty.cs`

**Boss: Chief Paroxysmus (peerless)** (1)

- `Items/Artifacts/Equipment/Weapons/ScepterOfTheChief.cs`

**ServUO treasure map rewrite (TreasureMapInfo, 3,899 lines)** (3)

- `Items/Artifacts/Equipment/Glasses/LegendaryMapmakersGlasses.cs`
- `Items/Equipment/Weapons/SkullGnarledStaff.cs`
- `Items/Equipment/Weapons/SkullLongsword.cs`

**Gargoyle alteration (AlterItem + [Alterable] on stock items)** (1)

- `Items/Artifacts/Equipment/Glasses/GargishGlasses.cs` *(not in the 219: named only as a base class)*

**Behind no ranked gate** (48)

- `Items/Artifacts/Decorative/SantaStatue.cs`
- `Items/Artifacts/Equipment/Armor/BronzedArmoroftheValkyrie.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Alorons Set/AloronsShorts.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationArms.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationBag.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationCap.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationChest.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationGloves.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationGorget.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationLegs.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Juggernaut/Evocaricus.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Items/Artifacts/Equipment/Armor/Sets/Mage/LeafweaveChest.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Myrmidon/MyrmidonBascinet.cs`
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixArms.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixChest.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixGloves.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixGorget.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixHelm.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixLegs.cs` *(not in the 219: created only by code that is itself unreached)*
- `Items/Artifacts/Equipment/Armor/Sets/Phoenix/PhoenixTicket.cs`
- `Items/Artifacts/Equipment/Armor/WardedDemonboneBracers.cs`
- `Items/Artifacts/Equipment/Clothing/AnniversaryRobe.cs`
- `Items/Artifacts/Equipment/Clothing/CloakOfDeath.cs`
- `Items/Artifacts/Equipment/Clothing/CloakOfLife.cs`
- `Items/Artifacts/Equipment/Clothing/CloakOfPower.cs`
- `Items/Artifacts/Equipment/Clothing/CloakOfSilence.cs`
- `Items/Artifacts/Equipment/Clothing/ConjurersGarb.cs`
- `Items/Artifacts/Equipment/Clothing/ConjurersGarbHarbringer.cs`
- `Items/Artifacts/Equipment/Clothing/ObiDiEnse.cs`
- `Items/Artifacts/Equipment/Clothing/RangersCloakOfAugmentation.cs`
- `Items/Artifacts/Equipment/Clothing/ShroudOfTheCondemned.cs`
- `Items/Artifacts/Equipment/Clothing/WardensArmorOfAugmentation.cs`
- `Items/Artifacts/Equipment/Glasses/Glasses.cs` *(not in the 219: named only as a base class)*
- `Items/Artifacts/Equipment/Jewelry/PetrifiedMatriarchsTongue.cs`
- `Items/Artifacts/Equipment/Spellbooks/ConjurersGrimoire.cs`
- `Items/Artifacts/Equipment/Weapons/EternalGuardianStaff.cs`
- `Items/Artifacts/Equipment/Weapons/TheRedeemer.cs`
- `Items/Artifacts/Talismans/FrostguardTalisman.cs`
- `Items/Artifacts/Talismans/JadeSnakeHead.cs`
- `Items/Books/Note.cs` *(not in the 219: named only as a base class)*
- `Items/Equipment/Armor/EvilOrcHelm.cs`
- `Items/Equipment/Clothing/FirstAidBelt.cs`
- `Items/Equipment/Clothing/GargoyleAccessories.cs`
- `Items/Equipment/Clothing/PlateTalons.cs`
- `Items/Equipment/Jewelry/StaffRing.cs`
- `Items/Equipment/Weapons/PaladinSword.cs` *(not in the 219: named only as a base class)*
- `Mobiles/Normal/PlagueRat.cs` *(not in the 219: named only in comments or tests, or by a same-named nested type)*
- `Services/Peerless/PeerlessKey.cs` *(not in the 219: named only as a base class)*

**Costumes (`Items/Equipment/Suits/`), no source in ServUO either** (32): BloodwormCostume, CentaurCostume, CyclopsCostume, DragonWolfCostume, DrakeCostume, DreamWraithCostume, EtherealWarriorCostume, ExodusMinionCostume, FireElementalCostume, GazerCostume, GiantPixieCostume, GiantToadCostume, GoreFiendCostume, LadyOfTheSnowCostume, MaddeningHorrorCostume, MinotaurCostume, MongbatCostume, OniCostume, OphidianMatriarchCostume, OphidianWarriorCostume, PixieCostume, SabertoothedTigerCostume, SatyrCostume, ShadowWyrmCostume, SkeletonCostume, SkitteringHopperCostume, SolenWarriorCostume, TitanCostume, VoidWandererCostume, WispCostume, WolfSpiderCostume, ZombieCostume
