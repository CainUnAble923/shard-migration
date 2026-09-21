# CC6 batch 6 — the name-mapping row: what the 41 orphans actually are, and one alias spike

**This task ported nothing.** It sorted `tools/spawn-orphans.txt`'s 41 names into rows derived from the source trees
rather than from the earlier notes, ran every name in the "no ServUO source" row through a five-step lookup with the
evidence written beside each, built one `[TypeAlias]` spike on one name and proved it in the test gate, and stopped.
The orphan count moved from 41 to 40, and that 40 is the spike's number: delete one file and it is 41 again
(§3). Whether the route is rolled out is **Q-055**, Chase's decision, with both sides in §4.

Two things this note corrects in the earlier batches, both counted rather than described:

- **Batch 5 §9's example list for the 17-name row was wrong on three names**, though its 17/30 figure was right.
  `treasurelevel1h`, `Barreraak` and `Xenrr` are all ServUO types (`Items/Containers/TreasureChestMod.cs:63`,
  `Mobiles/NPCs/Barreraak.cs`, `Mobiles/NPCs/Xenrr.cs`). Batch 3 §9 had `TreasureLevel1H` in the "other" row and was
  right. Batch 1 §10's list of the row was 18 names, not 17 ("the five Underworld NPC names" are four).
- **The row's premise — "names that should already resolve to types pinned ships" — is mostly false.** Of its 17
  names, **2 map to a pinned type** (9 of 30 entries), **13 are ServUO types under other names** (17 entries; the seven
  Clan rats are ServUO's `ClanCA`…`ClanSSW`, the four Underworld NPCs are `Dugan`, `Tobin`, `Neville`, `Navrey`), and
  **2 exist nowhere** (4 entries). The cheap row is smaller than hoped, and the port rows are larger (§9).

And one thing it found where nobody was looking: **seven of the quest row's names are pinned's own ML-quest NPCs
under shorter spellings** (`abbein` → `ElderAbbein`, all in `Engines/ML Quests/Definitions/Heartwood.cs`), which
moves 7 names and 14 entries from the quest row to the name-mapping row (§2c).

## 1. The rows, derived from the files

**Method.** For each of the 41 names in `tools/spawn-orphans.txt` (regenerated, 41 as of 2026-09-21 before the spike),
one case-insensitive grep for a class/struct/enum declaration under `D:\UO\ServUO-pub57\Scripts`:

    grep -rilE "\b(class|struct|enum)\s+<name>\b" --include=*.cs Scripts

24 names hit exactly one ServUO file each; 17 hit nothing. The 24 are placed by the directory of the hit, which is
batch 1 §1's row key. Entry counts are the orphan file's.

| row | names | entries | members (entries) | source of the row key |
|---|---|---|---|---|
| **no ServUO declaration under the spawn name** | **17** | **30** | `eliteninjawarrior` (7), `magedragonsflamemage` (4), `bodysculptor` (2), `DryadA` (2), `escortablewanderinghealer` (2), `genericguard` (2), `ClanChitterAssistant`, `ClanChitterTinkerer`, `ClanRibbonCourtier`, `ClanRibbonSupplicant`, `ClanScratchHenchrat`, `ClanScratchSavageWolf`, `ClanScratchScrounger` (1 each), `ElderDugan`, `FiddlingTobin`, `NavreyNightEyes`, `NevilleBrightwhistle` (1 each) | grep hit nothing |
| `Mobiles/NPCs` + `Quests/` | 15 | 23 | `abbein`, `alethanian`, `aneen`, `athialon`, `jothan`, `mallew`, `taellia`, `vicaie` (2 each, `Mobiles/NPCs/<Name>.cs`); `Barreraak`, `Garamon`, `Gretchen`, `Jaacar`, `QuartermasterFlint`, `Xenrr` (1 each, `Mobiles/NPCs`); `Vernix` (1, `Quests/Vernix.cs`) | the hit's directory |
| other | 4 | 9 | `treasurelevel1h` (4, `Items/Containers/TreasureChestMod.cs`), `dockmaster` (2), `boatpainter` (2) (`Services/Expansions/High Seas/Mobiles/Vendors/`), `sphynx` (1, `Services/Malas/Sphynx/Sphynx.cs`) | the hit's directory |
| `Mobiles/Bosses` + `Niporailem` | 4 | 4 | `Medusa`, `SlasherOfVeils`, `StygianDragon` (`Mobiles/Bosses/`), `Niporailem` (`Mobiles/Normal/`) | the hit's directory |
| `IronBeetle` | 1 | 1 | `Mobiles/Normal/IronBeetle.cs` | the hit's directory |

17 + 15 + 4 + 4 + 1 = 41; 30 + 23 + 9 + 4 + 1 = 67. **So the 17/30 figure stands, batch 3's "other" row was right, and
batch 5's prose list was wrong on three names.** The rows above are the *source* rows. §9 re-cuts them by what
would actually close each name, which is the table later tasks should size from.

**Where the misnamed data comes from, so the row has a cause and not just a count.** `git log` on
`D:\UO\ModernUO-pinned` shows the whole `Distribution/Data/Spawns` tree in five commits; every one of these names
entered in `0d1fffd9f` (2021-09-03, "replaces with neruns distro"), whose message says it converts Premium Spawner
XML from Nerun's Distro into ModernUO's JSON. ServUO ships spawn XML of the same lineage (`D:\UO\ServUO-pub57\
Spawns\*.xml`, Premium Spawner format), and at the same coordinates it names the *ServUO* types. That second copy is
what makes most of the mappings below evidence rather than guesses: two exports of the same rooms, one naming the
type each tree has. What I could not verify: Nerun's own scripts. No Nerun's Distro exists on this machine, and none
of the six sibling trees under `D:\UO` (`UOAlive`, `Excelsior`, `ImmortalRealms`, `ServUO-ShatteredLegacy`,
`ModernUO-reference`, `ModernUO-work`) declares any of the 17 names, so whether Nerun shipped a custom
`GenericGuard` or `BodySculptor` is unknown here.

## 2. The 17, through the five steps

**The steps, in order, each name stopping at the first that answers it:**

1. **Exact match** — a declaration of the name in pinned `Projects/{Server,UOContent}` or `server/customizations`.
   By construction of the orphan list, none. (`tools/spawn_orphans.py` is that grep.)
2. **`[TypeAlias]` match** — every `TypeAlias("...")` string in the same three trees, last dotted segment, case-folded,
   the way `TypeCache` registers them (`AssemblyHandler.cs:251-263`). Counted: **129 alias names in pinned
   `UOContent`, 0 in pinned `Server`, 21 in ours. None of the 150 is any of the 41.** `tools/spawn_orphans.py` now
   registers aliases too (§7), and reported the same 41 rows before the spike, which is the same fact by a second
   route.
3. **Word-boundary variant** in pinned, corroborated by ServUO's spawn XML at the same place or by the type's own
   `Name`. A variant with no corroboration goes to step 5, not here.
4. **A ServUO source under a different name** — a port, for a later batch.
5. **Nothing anywhere.**

| name | entries | step | maps to | evidence |
|---|---|---|---|---|
| `eliteninjawarrior` | 7 | **3** | pinned `EliteNinja` (`Mobiles/Monsters/SE/EliteNinja.cs`) | ServUO `Spawns/malas.xml` names `EliteNinja`/`eliteninja` at the same Citadel spawners: `TheCitadel#12` (82,1875), `TheCitadel#11` (81,1892), `TheCitadel#5` (181,1883) are the exact coordinates of three of pinned's seven, with the same sibling sets (`serpentsfangassassin`, `tigersclawthief`, `dragonsflamemage`: batch 2's ports); `Citadel#7` (131,1860: 7 each of five names) is pinned's [139,1868] (7 each of the same five). Pinned's data never names `eliteninja` in the Citadel (10 entries elsewhere), so under stock ModernUO the Citadel has no elite ninjas at all. **The spike, §3** |
| `DryadA` / `Dryada` | 2 | **3** | pinned `MLDryad` (`Mobiles/Monsters/ML/Humanoid/Magic/MLDryad.cs`, body 266) | ServUO `Spawns/twistedweald.xml` names only `MLDryad`/`mldryad` in the Weald ((2185,1177) ×3, `dryad2` (2203,1161)) against pinned's [2171,1181] ×8 and [2207,1180] ×12; the pinned spawners' siblings are `CuSidhe`, `Changeling`, `Satyr`, `DireWolf`. Pinned's data never names `mldryad` anywhere, so its Twisted Weald has no dryads. Pinned's other `Dryad` (`Engines/Quests/Uzeraan Turmoil/Mobiles/Dryad.cs`) is the Haven quester "Anwin Brenna", a `BaseQuester`, and is **not** it. The two spellings are one name to `FindTypeByName` |
| `magedragonsflamemage` | 4 | **4** | ServUO `Mobiles/Normal/DragonsFlameGrandMage.cs` (62 lines, `: DragonsFlameMage`, "Black Order Grand Mage", fame 25000) | same XML: `DragonFlame 1` (135,1941), `Citadel#1` (178,1913), `Citadel#9` (132,1966), `Citadel#7` (131,1860) name `DragonsFlameGrandMage` with the counts (1/2/2/7) pinned gives `magedragonsflamemage` at [134,1947], [185,1920], [140,1974], [139,1868]. Batch 2 §9's guess, now with evidence. Its parent is **our** `DragonsFlameMage` (batch 2), so it is one leaf file |
| `ClanChitterAssistant` | 1 | **4** | ServUO `Mobiles/Normal/ClanCA.cs` | `Name = "Clan Chitter Assistant"`, `[CorpseName("a clan chitter assistant corpse")]` |
| `ClanChitterTinkerer` | 1 | **4** | `ClanCT.cs` | `Name = "Clan Scratch Tinkerer"`, corpse "a clan scratch tinkerer corpse" — **ServUO's own file disagrees with its class name (C-T) and with the spawn name**; a fidelity note for whoever ports it, not decided here |
| `ClanRibbonCourtier` | 1 | **4** | `ClanRC.cs` | `Name = "Clan Ribbon Courtier"` |
| `ClanRibbonSupplicant` | 1 | **4** | `ClanRS.cs` | `Name = "Clan Ribbon Supplicant"` |
| `ClanScratchHenchrat` | 1 | **4** | `ClanSH.cs` | `Name = "Clan Scratch Henchrat"` |
| `ClanScratchSavageWolf` | 1 | **4** | `ClanSSW.cs` | `Name = "Clan Scratch Savage Wolf"` |
| `ClanScratchScrounger` | 1 | **4** | `ClanSS.cs` | `Name = "Clan Scratch Scrounger"`. The seven together: 641 lines, `BaseCreature` direct, `AI_Melee`/`AI_Archer`, the only `new X(` are `Bow` and `Arrow` (3 files). Stock `ClanRibbonPlagueRat` is the eighth of the family and pinned has it |
| `ElderDugan` | 1 | **4** | ServUO `Mobiles/NPCs/Dugan.cs` (81 lines, `: MondainQuester`, `base("Elder Dugan", "the Prospector")`) + `Quests/EscortToDugan.cs` (58) | the `Name` string. **Quest row**: S5's engine mapping |
| `FiddlingTobin` | 1 | **4** | `Mobiles/NPCs/Tobin.cs` (120 lines: `Tobin : MondainQuester`, `base("Fiddling Tobin", "the Tinkerer")`, plus `DoneInTheNameOfTinkeringQuest`) | the `Name` string. **Quest row** |
| `NevilleBrightwhistle` | 1 | **4** | `Mobiles/NPCs/Neville.cs` (151 lines, `: BaseEscort`, `Name = "Neville Brightwhistle"`) | the `Name` string. Pinned has `BaseEscort` (`Engines/ML Quests/Definitions/BaseEscort.cs`); the ServUO one is the MondainQuester-era escort, so **quest row** |
| `NavreyNightEyes` | 1 | **4** | `Mobiles/Bosses/Navery/Navrey.cs` (185 lines, `Name = "Navrey Night-Eyes"`) + `EyeOfNavrey.cs` (41) + `Services/Underworld/Navrey's Lair/NavreysController.cs` (291) + `NavreysPillar.cs` (134) = 651 | the `Name` string. A boss with a lair mechanic: **the bosses row**, alongside Q-052's three |
| `escortablewanderinghealer` | 2 | **4** | ServUO `Quests/Escortables.cs:1255` `EscortableHealer : TownEscortable` (file 1,435 lines) | ServUO `Spawns/felucca.xml` names `escortablehealer` at the **identical** spawner (`Vendors#50`, 1333,1808). Pinned has `BaseEscortable` and `WanderingHealer` but no `TownEscortable` and no escortable healer, so this is a port of a piece of ServUO's escort family, not a variant of a pinned type. **Quest/escort row** |
| `genericguard` | 2 | **5** | — | no declaration or alias in pinned, ours, ServUO, or the six sibling trees. ServUO `Spawns/underworld.xml` has no guard entry at all; its nearest spawner to pinned's [1127,1202]/[1130,1202] is `Garamon` (1128,1165). Pinned has `WarriorGuard` and `ArcherGuard`, and no evidence says which, if either, Nerun meant. A spawn-data finding for Chase |
| `bodysculptor` | 2 | **5** | — | nothing in any tree. Pinned's `Sculptor` (`Mobiles/Townfolk/Sculptor.cs`, "the sculptor", random name, sells nothing) and ServUO's `Mobiles/NPCs/Sculptor.cs` are a different NPC by name and by what they do; with no corroboration the word-boundary hit stays a hit. The spawner sits in the Sea Market cluster ([4547,2321], among `dockmaster`, `boatpainter`, `treasurelevel1h`, `Fisherman`, `Shipwright`…), and ServUO's own XML has **no** Sea Market vendor spawners, so there is no second export to check against. A spawn-data finding for Chase |

**Totals:** step 3 → 2 names / 9 entries; step 4 → 13 names / 17 entries; step 5 → 2 names / 4 entries. 17 / 30.

### 2b. One correction to bucket 4 that is really bucket 3, and one to the "other" row

`treasurelevel1h` (4 entries, the Sea Market at [4534,2349] and [4535,2349]) is ServUO's `TreasureLevel1h :
BaseTreasureChestMod` (`Items/Containers/TreasureChestMod.cs:63`). **Our port of that file** (`server/customizations/
Items/Containers/TreasureChestMod.cs:4`) says "ServUO's file also carries TreasureLevel1h and other variants that
nothing here references; not ported." The spawn data references it, four times. It is ~50 lines on a base we already
have, and the cheapest item on the whole list; it stays "other" here because this task ports nothing.

### 2c. The quest row's hidden name-mapping cluster: seven Heartwood elders

Running the same five steps over the other 24 names, because the greps were already written:

| spawn name | entries | pinned type | evidence |
|---|---|---|---|
| `abbein` | 2 | `ElderAbbein` (`Engines/ML Quests/Definitions/Heartwood.cs:3361`) | `DefaultName => "Elder Abbein"`; ServUO `Mobiles/NPCs/Abbein.cs`: `Name = "Elder Abbein"`, `base("the wise")` |
| `alethanian` | 2 | `ElderAlethanian` (`:3445`) | `"Elder Alethanian"` |
| `aneen` | 2 | `LorekeeperAneen` (`:3584`) | `"Lorekeeper Aneen"`; ServUO `Aneen.cs`: `Name = "Lorekeeper Aneen"` |
| `jothan` | 2 | `ElderJothan` (`:3417`) | `"Elder Jothan"` |
| `mallew` | 2 | `ElderMallew` (`:3321`) | `"Elder Mallew"` |
| `taellia` | 2 | `ElderTaellia` (`:3294`) | `"Elder Taellia"` |
| `vicaie` | 2 | `ElderVicaie` (`:3387`) | `"Elder Vicaie"` |
| `athialon` | 2 | **none** | ServUO `Athialon.cs` (`"Athialon"`, `"the expeditionist"`); pinned's Heartwood file has no Athialon. Stays a port, quest row |

All seven pinned types are `partial class … : BaseCreature` with `AIType.AI_Vendor`, i.e. the RunUO ML-quest NPCs,
and ServUO's are `BaseVendor`s with the same names and titles. Both spawn files place them at Heartwood ([7048,382]
six together, [7053,338] Aneen; ServUO's `trammel.xml` at (7046,390) and (7054,340)). **Pinned's data never names
`elder*` or `lorekeeper*` anywhere except `eldergazer` and `elderdugan`, and `MLQuest.Generate()` is a no-op that
places nothing** (`Engines/ML Quests/MLQuest.cs:103`), so under stock ModernUO the Heartwood quest givers exist in
the assembly and never appear in the world. Same shape as the Citadel, bigger consequence: these are quest givers.

**Not verified:** that pinned's `ElderAbbein` offers the same quests ServUO's `Abbein` does. Both are ML-quest
NPCs by the same name; the quest lists were not compared, and a rollout that aliases them should compare them first.

## 3. The spike: `[TypeAlias("Server.Mobiles.EliteNinjaWarrior")]` on stock `EliteNinja`

**What was built.** One additive file, `D:\ShatteredLegacy\server\customizations\Mobiles\Aliases\
EliteNinjaSpawnAlias.cs`, 20 lines of which four are code:

```csharp
namespace Server.Mobiles;

[TypeAlias("Server.Mobiles.EliteNinjaWarrior")]
public partial class EliteNinja
{
}
```

It is mirrored by `apply-patches.sh` to `Projects/UOContent/Mobiles/Aliases/EliteNinjaSpawnAlias.cs`; no patch, no
basename collision with stock `EliteNinja.cs`, no change to the type's members, constructors or serialization.

**Why it should work, checked before the build rather than assumed.** `TypeCache` (`AssemblyHandler.cs:251-263`)
iterates every type in the assembly and, for one carrying `TypeAliasAttribute` (read with `inherit: false`),
registers each alias under its full name and its last dotted segment in the same four maps a real type name goes in;
`FindTypeByName` (`:189-210`) reads those maps with `ignoreCase = true` by default, which is the call
`BaseSpawner.Spawn` makes (`BaseSpawner.cs:1126`). `TypeAliasAttribute` (`Attributes.cs:88-94`) is
`AttributeTargets.Class`, no `AllowMultiple`, so a second `[TypeAlias]` on any part of `EliteNinja` would be a
compile error, not a silent override; stock `EliteNinja.cs` carries only `[SerializationGenerator(0, false)]`. C#
merges attributes across the parts of a partial type. Saves write `Type.FullName`, which the alias does not touch.
Two things this project had not yet done in the tree, both proved by the green build: a second partial part on a
**stock, generator-serialized** type (batch 3 §9 proposed it for `IAcidCreature` and deferred it), and a
`[TypeAlias]` that is not a save-upgrade spelling (all 21 of ours are).

**The test**, `server/tests/Mobiles/Normal/CC6Batch6SpawnAliasVerification.cs`, three facts:

- `TheCitadelNameResolvesToTheStockEliteNinjaThroughTheAlias`: the attribute on `typeof(EliteNinja)` carries exactly
  that one alias; `FindTypeByName("eliteninjawarrior")`, `("EliteNinjaWarrior")` and `("Server.Mobiles.
  EliteNinjaWarrior", fullName: true)` all return `typeof(EliteNinja)`; `FindTypeByName("EliteNinja")` still does;
  `typeof(EliteNinja).FullName` is still `Server.Mobiles.EliteNinja`.
- `ASpawnerEntryCarryingTheCitadelNameFills`: a `Spawner` placed at [82,1875,0] on Malas (pinned's first Citadel
  spawner for the name) with the entry `eliteninjawarrior` ×4 — `Spawn(entry, out flags)` returns true, `flags` is
  `None`, and `Spawned` holds one `EliteNinja` on Malas at that location, registered against the entry. The host has
  no tile data, so `SpawnBounds` stays default and `GetSpawnPosition` returns the spawner's own location
  (`BaseSpawner.cs:571-577`) — the spawner path is exercised up to and including placement, but not the
  `CanSpawnMobile` walk over real tiles. That last step is a client check, Q-048's.
- `ANameWithNoAliasStillFlagsInvalidType`: the negative control. `magedragonsflamemage` (4 Citadel entries, a step-4
  port, not aliased) resolves to null and a spawner entry carrying it returns false with `EntryFlags.InvalidType`.
  So the file shows the mechanism discriminating, not merely passing.

**Proved in the gate, both directions** (§6): the test was built first **without** the alias file and the gate went
red on the two alias facts with the control green; then the alias file was added and the whole gate went green. The
orphan-count fact that **all five** CC6 batch tests pin moves 41 → 40 with it, and each says why. **To revert the
spike:** delete `EliteNinjaSpawnAlias.cs`, put those five asserts back to 41, regenerate `spawn-orphans.txt`. Nothing
else references it.

**Not rolled out.** The other eight names step 3 answered (`DryadA` → `MLDryad`, the seven Heartwood elders) are not
aliased. That is Q-055.

## 4. The alias route, argued both ways

The three ways to close a name that maps to an existing type, from the brief, with what this task found under each:

| route | what it is | verdict here |
|---|---|---|
| **`[TypeAlias]` on the stock type** | one additive partial-class file per name, as §3 | works; proved on one name; **Chase decides whether it is wanted** |
| **edit the spawn JSON** | rename the entries in `Distribution/Data/Spawns` | **forbidden** — pinned upstream data, we do not patch data |
| **leave it** | the spawners stay `InvalidType` and the rooms empty | the honest default, and what every other ModernUO shard running this data has |

**For the alias route.**

- It is cheap, additive and reversible: one file per name, no patch, no member, no save-chain change. Delete the file
  and the tree is as it was. 9 files would close 23 entries (§9).
- Nothing a player sees changes. The creature that spawns is stock `EliteNinja`: its name, corpse, loot, fame and
  UOGuide page are the stock ones. The alias is a string in a lookup table.
- The data is **pinned upstream's own**, naming pinned upstream's own types under the wrong spelling. This is not us
  inventing content; it is upstream's data disagreeing with upstream's assembly, which we cannot fix in the data
  because of the no-patch-data rule. The alias is the only place left where the two can be reconciled additively.
- Every mapping proposed has a second source: ServUO's Premium Spawner XML naming the ServUO type at the same rooms
  (§2), or the pinned type's own `Name` string equal to the spawn name (§2c).
- The alternative is not neutral. Under "leave it", the Citadel has no elite ninjas, the Twisted Weald has no dryads,
  and Heartwood has no quest givers, indefinitely, for content the shard is entitled to (Endless Journey).

**Against the alias route.**

- **The names are not OSI's.** `EliteNinjaWarrior`, `Dryada`, `MageDragonsFlameMage` are a spawn-file author's
  spellings (Nerun's, on the commit message; unverified beyond that). Carrying them means our tree wears names that
  never existed on OSI or in RunUO, which cuts against the fidelity principle's whole purpose: a player or a GM who
  types `[add EliteNinjaWarrior` gets a creature, and no wiki explains why.
- **It repurposes a save-compatibility device.** Every `[TypeAlias]` in ServUO, in pinned ModernUO, and in our tree
  (21 of them) records an *earlier spelling of the same type* so old saves load. Using it to absorb a data file's
  typos is a new meaning for the attribute, and the next reader will assume the old one.
- **The right fix is upstream.** Pinned's data misnaming pinned's types is a ModernUO bug: a pull request renaming
  the JSON entries (`eliteninjawarrior` → `EliteNinja`, `Dryada` → `MLDryad`, `abbein` → `ElderAbbein`, …) fixes it
  for every shard and reaches us on the next pinned bump with nothing in our tree. Aliases are a local workaround for
  a defect someone else owns. (They are also harmless once upstream fixes it: a dead alias resolves nothing.)
- **A pinned bump can break it loudly.** If upstream ever adds its own `[TypeAlias]` to `EliteNinja`, our second
  attribute is CS0579 and the build fails in the builder stage. That is the good kind of failure, but it is a
  maintenance surface where "leave it" has none.
- **Three of the mappings are corroborated only by name strings** (the Heartwood seven by `DefaultName`; `DryadA` by
  the Weald having one dryad type). Strong, but not the coordinate-and-count match the Citadel has, and §2c's quest
  lists were not compared.

**My recommendation, for what it is worth to the decision:** keep the spike, alias the nine (§9), and *also* report
the misnames upstream so the aliases have a retirement date. The fidelity principle is about what players experience,
and what they experience under "leave it" is empty rooms where the content they can read about should be. But that
is exactly the kind of call the brief says is Chase's, and the spike is one file to delete if the answer is no.

## 5. Deviations

None. Nothing was ported, and the alias changes no behaviour of `EliteNinja`.

## 6. What was proved

**6a. The gate was watched failing.** `docker/uo/build.sh --tests-only` with the new test in `server/tests/` and
**no** alias file, 2026-09-21. Builder stage green in 52 s (the test compiles against pinned's `Spawner` API). Test
gate: **Passed 98, Failed 2**, the build script printing `BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No
image was built.` and exiting 1. The two failures, verbatim:

- `TheCitadelNameResolvesToTheStockEliteNinjaThroughTheAlias` — `Assert.NotNull() Failure: Value is null` at line
  54, the `GetCustomAttribute<TypeAliasAttribute>` read: stock `EliteNinja` carries no alias.
- `ASpawnerEntryCarryingTheCitadelNameFills` — `Spawn returned false with flags InvalidType` at line 80: the
  spawner path rejects the name exactly as the live Citadel spawners do.
- `ANameWithNoAliasStillFlagsInvalidType` **passed**, as it must in both runs.

**6b. Then green, on the second try.** The alias file added, the batch-1 count fact moved 41 → 40 (with the reason
in its comment), `tools/spawn-orphans.txt` regenerated to 40, and `docker/uo/build.sh` run end to end. **First run:
red, Passed 96 / Failed 4**, no image. The three spike facts and batch 1's count passed; what failed was the same
count pinned again in **batches 2, 3, 4 and 5's** `EveryStockSpawnEntryNaming…Resolves` facts (`Expected: 41,
Actual: 40`), which I had not known were there — every CC6 batch pins the figure, not just the first, and the brief's
"the count may not move" was true of the number and not of the number of places it lives. All four moved to 40 with
the same two-line reason.

**6c. Green.** `docker/uo/build.sh`, 2026-09-21: builder stage green, test gate **Passed 100 / Failed 0**
(`[tests] 100 test(s) passed.`), runtime image `Built sl-modernuo:latest with patches applied and 100 shard test(s)
passing.` The three batch-6 facts among them:

    Passed ShatteredLegacy.Tests.CC6Batch6SpawnAliasVerification.TheCitadelNameResolvesToTheStockEliteNinjaThroughTheAlias
    Passed ShatteredLegacy.Tests.CC6Batch6SpawnAliasVerification.ASpawnerEntryCarryingTheCitadelNameFills
    Passed ShatteredLegacy.Tests.CC6Batch6SpawnAliasVerification.ANameWithNoAliasStillFlagsInvalidType

**Not proved, said plainly:** that a live Citadel spawner fills. The host has no map tiles, so the placement walk
(`CanSpawnMobile` over the real Citadel floor) did not run; and whether the live world's spawners were generated from
these files at all is still Q-048. Stand at [82,1875] on Malas after the next deploy and count; that is the client
check, and it is the same check every CC6 batch has owed.

## 7. What it cost

| what | time |
|---|---|
| orientation: both `AGENTS.md`, batches 1/2/3/5 §1/§9, the follow-up note, `spawn-orphans.txt`, `spawn_orphans.py` | ~20 min |
| the 41 through ServUO (declarations), pinned + ours (declarations, aliases, any-word), the six sibling trees | ~25 min |
| ServUO's Premium Spawner XML at the same coordinates (Citadel, Weald, Underworld, Heartwood, Britain, Sea Market) and pinned's spawn-data history | ~25 min |
| `AssemblyHandler`, `TypeAliasAttribute`, `BaseSpawner.Spawn`/`GetSpawnPosition`/`AddEntry`, the test host's map registration | ~15 min |
| the spike file, the test, `spawn_orphans.py` alias registration | ~20 min |
| two builds (red then green) | see §6 |
| this note, Q-055, progress | ~40 min |

**Tool change:** `tools/spawn_orphans.py` now registers `[TypeAlias]` strings the way `TypeCache` does. With no alias
covering an orphan it reproduced the committed 41 rows exactly (diffed); with the spike it reports 40.

## 8. Questions

- **Q-055** (non-blocking, Chase's): keep the spike and roll the alias route out to the nine mapped names, revert it,
  or keep it and report the misnames upstream. §4 has both sides; `notes/codex-questions.md` has the question.
- **No D-number.** Nothing here is a lost capability with a patch that reverses it. `genericguard` and
  `bodysculptor` are spawn-data findings (§2), not patch rows.
- **Q-052** (Chase's, open) now covers five bosses, not four: `NavreyNightEyes` is ServUO's `Navrey` with a 651-line
  lair (§2), and it sat in the "not in ServUO" row until this task.

## 9. What the rows now cost, re-cut by what closes each name

The source rows of §1 are the wrong shape for sizing, because "where ServUO keeps the file" and "what closes the
entry" disagree for 20 of the 41 names. By closure:

| what closes it | names | entries | members | cost, measured |
|---|---|---|---|---|
| **an alias on a pinned type** (Q-055) | **9** | **23** | `eliteninjawarrior` (7, done as the spike), `DryadA` (2), `abbein`, `alethanian`, `aneen`, `jothan`, `mallew`, `taellia`, `vicaie` (2 each) | 8 more files of the §3 shape, one test fact each; **zero if Q-055 says no** |
| **a leaf creature port, no subsystem** | 8 | 11 | `magedragonsflamemage` (4: `DragonsFlameGrandMage`, 62 lines on our `DragonsFlameMage`), the seven Clan rats (641 lines total, `Bow`/`Arrow` only) | one batch, eight files, the batch-2 recipe; the `ClanCT` naming disagreement to record |
| **a leaf item port** | 1 | 4 | `treasurelevel1h` (~50 lines into a file we already carry) | trivial; ride along with anything |
| **the quest/escort engine** (S5, Q-025) | 12 | 14 | `athialon`, `Barreraak`, `Garamon`, `Gretchen`, `Jaacar`, `QuartermasterFlint`, `Xenrr`, `Vernix`, `ElderDugan`, `FiddlingTobin`, `NevilleBrightwhistle`, `escortablewanderinghealer` | gated as before; **three names bigger** than batch 5 §9 said (the Underworld NPCs), **seven smaller** (the Heartwood elders moved up) |
| **bosses** (Q-052) | 5 | 5 | `Medusa`, `SlasherOfVeils`, `StygianDragon`, `Niporailem`, **`NavreyNightEyes`** | Q-052 plus Navrey's lair (651 lines) |
| **High Seas** | 2 | 4 | `dockmaster` (236 lines), `boatpainter` (42) | a subsystem question, unchanged |
| **`Sphynx`** | 1 | 1 | `Services/Malas/Sphynx/` (572 lines) | a leaf with its own service; unchanged |
| **P6** | 1 | 1 | `IronBeetle` | unchanged |
| **nothing to map: a spawn-data finding for Chase** | 2 | 4 | `genericguard` (2, Underworld entrance), `bodysculptor` (2, Sea Market) | nothing to build; a note to upstream if Chase wants one |

9 + 8 + 1 + 12 + 5 + 2 + 1 + 1 + 2 = 41; 23 + 11 + 4 + 14 + 5 + 4 + 1 + 1 + 4 = 67.

**Batch 7, by the same rule as before:** if Q-055 says yes, eight alias files close 16 entries in an afternoon with no
port; either way, the leaf-creature row (`DragonsFlameGrandMage` and the seven rats, 11 entries) is the next batch
with a ServUO source, and `TreasureLevel1h` rides along. The quest row is now 12 names and is still S5's. The
"cheapest block left" was never 30 entries; it is 23 if aliases are allowed and 15 by porting if they are not.
