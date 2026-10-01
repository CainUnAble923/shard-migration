# P24 s3a - Harvest by region, mineable/choppable tiles, and what a new metal (Dawnstone) touches

Read-only research, 2026-10-01. Engine authority: `D:\UO\ModernUO-pinned` at 7c9215d97 (confirmed with
`git log -1`). Shard code: `D:\ShatteredLegacy\server\customizations` (below: `cust\`) and
`D:\ShatteredLegacy\server\patches` (below: `patches\`). `server\uo` not read. Pinned paths below are
relative to `ModernUO-pinned\Projects\`. Nothing outside `notes\cc-P24-scratch\` was changed. Scratch
scripts (tiledata parser) lived in the session scratchpad only.

---

## 1. Harvest by region

### 1.1 How the extended ores/woods hook in today

Both extensions are runtime mutations of the pinned singleton harvest definitions, not patches:

- `cust\ClusterFMiningExtension.cs:37-41` subscribes `EventSink.WorldLoad` (veins) and
  `EventSink.ServerStarted` (craft sub-resources).
- `ExtendMiningVeins` (`:66-134`) takes `Mining.System.OreAndStone` (pinned `UOContent\Engines\Harvest\Mining.cs:268-270`),
  appends 8 `HarvestResource`s (`:84-94`, all `reqSkill 100.0`, one type each) to `def.Resources` (`:97-101`),
  appends 8 `HarvestVein`s with weights 8..1 and Iron as fallback (`:108-124`), and sets
  `def.RandomizeVeins = false` (`:131`).
- Setting `Veins` recomputes `VeinWeights` (pinned `Engines\Harvest\Core\HarvestDefinition.cs:65-79`), so the
  pool becomes 1000 + 36 = 1036 (pinned vanilla weights 496..14 at `Mining.cs:190-201` sum to 1000).
- "Coordinate-seeded 8x8 banks" is pinned behaviour, not ours: `GetBank` divides by `BankWidth/BankHeight`
  (`HarvestDefinition.cs:104-127`; 8x8 set at `Mining.cs:86-87`) and `GetVeinAt` seeds
  `x*17 + y*11 + MapID*3` through `StableRandom.First(seed, VeinWeights)` when `RandomizeVeins` is false
  (`HarvestDefinition.cs:129-144`). Pinned itself sets `RandomizeVeins = Core.ML` (`Mining.cs:221`), true on
  this shard; our `:131` turns it off for Mining only.
- Lumber: `cust\ClusterFLumberjackingExtension.cs:173-177, 200-259` does the same to
  `Lumberjacking.System.Definitions[0]` (8 woods, weights 8..1, regular Log fallback). It does NOT set
  `RandomizeVeins`, so lumber keeps pinned `Core.ML` = true (`Lumberjacking.cs:118`).
- Both systems are made `partial` so we can override `Give`: Mining via the full-file replacement
  `patches\Mining.cs` (its only diff from pinned is line 8, `public partial class Mining`; checked with `diff`),
  routed by `docker\uo\apply-patches.sh:245`; Lumberjacking via a `sed` structural fix
  (`apply-patches.sh:359-365`). Our partials: `cust\CompactOreSatchelRoutingHook.cs:51-144` (Mining.Give:
  discovery gate, satchel routing, depletion broadcast) and `cust\ClusterFLumberjackingExtension.cs:30-101`
  (Lumberjacking.Give: wood gate, satchel routing).
- Other readers of `OreAndStone.Banks`: `cust\ClusterFExplorationSync.cs:275-277` (world-map depletion haze),
  `cust\CompactOreSatchelRoutingHook.cs:155-166`.

### 1.2 Pinned hooks available (what is virtual, what is already taken)

Flow: `HarvestTarget` -> `StartHarvesting` (`Core\HarvestSystem.cs:436-482`) picks the definition with
`GetDefinition(tileID, isLand)` (`:421-434`, first definition whose `Validate` passes), then the timer calls
`FinishHarvesting` (`:78-251`): `Validate` (`:93`), `CheckRange`, `CheckResources` (bank count, `:40-51`),
`GetBank` (`:119`), `MutateVein` (`:130`), `MutateResource(from, tool, def, map, loc, vein, primary, fallback)`
(`:140`, body `:332-352`), skill gate `skillBase >= resource.ReqSkill && CheckSkill(Min,Max)` (`:147`),
`GetResourceType` (`:149`), `MutateType` (`:153`, default `from.Region.GetResource(type)`, `:321-325`),
`Construct`, `bank.Consume`, `Give` (`:199`).

| Virtual | Pinned Mining overrides? | Pinned Lumberjacking overrides? | Ours overrides? |
|---|---|---|---|
| `MutateVein` | yes, Gargoyle pickaxe (`Mining.cs:356-372`) | no | no |
| `MutateResource` | no | no | no |
| `GetResourceType` | yes (`Mining.cs:274-291`) | no | no |
| `GetDefinition(int,bool)` | no | no | no |
| `CheckResources` | no | no | no |
| `OnHarvestStarted` | yes (`Mining.cs:451-459`) | yes (`Lumberjacking.cs:180-188`) | no |
| `BeginHarvesting` | yes (`Mining.cs:440-449`) | no | no |
| `Give` | no | no | yes, both (see 1.1) |

Not present in pinned: there is no `HarvestDefinition.RegionalVeins`, no per-region table, and no Region check
anywhere in `Engines\Harvest\Core\` except the `MutateType` default above. `Definitions` is
`{ get; init; }` (`HarvestSystem.cs:9`), so a third definition cannot be appended after construction.
`Region.GetResource(Type)` is a virtual hook on Server `Regions\Region.cs:764` that nothing in pinned
UOContent overrides (grep: only the definition and `Mining.cs:274`'s unrelated name).

### 1.3 Recommended design: override `MutateResource` in our partials, gated by a dungeon region

`MutateResource` is the right seam: it is virtual, overridden by neither pinned class nor by us, it receives the
**target** `map` and `loc` (from `GetHarvestDetails`, `HarvestSystem.cs:484-519`), and its return value is what
the skill gate at `:147` checks, so Dawnstone can carry its own low `ReqSkill/MinSkill/MaxSkill`.

Sketch (one new additive file, e.g. `cust\ClusterFDawnhollowHarvest.cs`):

```
public partial class Mining {            // namespace Server.Engines.Harvest
  static readonly HarvestResource Dawnstone = new(0.0 /*or 30*/, 0.0, 80.0, <msg>, typeof(DawnstoneOre), typeof(Granite));
  public override HarvestResource MutateResource(Mobile from, Item tool, HarvestDefinition def, Map map,
      Point3D loc, HarvestVein vein, HarvestResource primary, HarvestResource fallback)
  {
    if (def == OreAndStone && Region.Find(loc, map).IsPartOf<DawnhollowRegion>())
      return <roll: Dawnstone at X%, else Iron (def.Resources[0])>;
    return base.MutateResource(from, tool, def, map, loc, vein, primary, fallback);
  }
}
public partial class Lumberjacking { same, def == Definitions[0], Rootwood resource, regular Log fallback }
```

`Region.Find(Point3D, Map)` and `IsPartOf<T>()` exist at `Server\Regions\Region.cs:291, 539`.

Consequences, all confined to the region:
- Outside the region the base method runs unchanged, so the global pool, the 1036 weights, the seeded banks and
  the GM-only extended ores are untouched.
- Inside, the bank vein is ignored; bank depletion and respawn still use the global `OreAndStone` 8x8 banks
  (`HarvestSystem.cs:119, 197`), so the world-map haze (`ClusterFExplorationSync.cs:275`) keeps working.
  Lumber banks are 4x3 (`Lumberjacking.cs:43-44`).
- Prospector's tool and Gargoyle pickaxe act on the bank vein (`Items\Skill Items\Harvest Tools\ProspectorsTool.cs:70-100`,
  `Mining.cs:356-372`) and become no-ops in the region, because our override discards the vein. The Gargoyle
  elemental spawn needs `vein.PrimaryResource == resource` (`Mining.cs:384-386`), so it cannot fire on Dawnstone.
- **Give Dawnstone at least two types.** `Mining.GetResourceType` returns `resource.Types[1]` for a GM miner with
  StoneMining toggled on, 10% of the time (`Mining.cs:284-288`). See finding F1.
- Our `Mining.Give` (`CompactOreSatchelRoutingHook.cs:67-144`) only gates the 8 types in `_extendedOreGateKeys`
  (`:55-65`), so Dawnstone is delivered ungated unless added there (not wanted for a starter ore).
- Region: none exists for the dungeon. Precedent for a code-registered region is `DespiseRegion`
  (`cust\Services\Revamped Dungeons\DespiseRevamped\Region.cs:33-57`, priority `DefaultPriority + 1` with the
  reason recorded at `:44-50`, and `Register()` at `:56`). A `DungeonRegion` subclass
  (`UOContent\Regions\DungeonRegion.cs:5`) registered the same way avoids touching pinned `regions.json`.
  Whether the dungeon also needs a `regions.json` entry is for the map/region section, not verified here.

Alternatives considered and rejected:
- `Region.GetResource` override (type substitution after the skill check): fully additive, but the skill gate
  has already used Iron's 0-100 band, it would also rewrite colored ore and logs, and it fires on `from.Region`
  not the target tile.
- A separate `HarvestDefinition`: `Definitions` is init-only (`HarvestSystem.cs:9`), so it needs either an edit
  to the replacement `patches\Mining.cs` constructor (and a new patch for Lumberjacking), or a `GetDefinition`
  override. Only worth it if the dungeon must have its own bank sizes/respawn; see 2.4 for the one case where
  it is needed (walls not already in the tile lists).

**Patch or additive:** additive. One new file, no edit to any upstream file and no new `.patch`, because both
classes are already partial and neither overrides `MutateResource`. Size: about 80-120 lines (two overrides of
~15 lines, two `HarvestResource` defs, a region class of ~20-30 lines plus its registration). Add ~40 lines if
the 2.4 static-wall definition is wanted. Plus the Dawnstone item/resource work in section 3.

---

## 2. Mineable and choppable tiles in pinned

Validation is `HarvestDefinition.Validate` (`Core\HarvestDefinition.cs:188-213`): land targets check `LandTiles`,
static targets check `StaticTiles`; with `RangedTiles = true` the array is read as inclusive (lo, hi) pairs.
Static IDs are raw item IDs (`Server\Targeting\StaticTarget.cs:10` masks with `MaxItemValue`).

Tiledata source: `D:\UO\UltimaOnlineVanilla\tiledata.mul`, 3,188,736 bytes, parsed per pinned
`Server\TileData.cs:311-372` (64-bit flags branch since length >= 3188736, `:314-317`). The parse consumed
exactly 3,188,736 bytes, which is my check that the layout was read correctly. Names are as stored (20-char).

### 2.1 Mining land tiles (`_mountainCaveTiles`, `Mining.cs:24-50`, ranged, `RangedTiles = true` at `:95`)

22 pairs, 436 IDs actually matched (counted). Tiledata names per pair:

| Range (dec) | Hex | Count | Tiledata names |
|---|---|---|---|
| 220-231 | 0x00DC-0x00E7 | 12 | dirt 8, rock 4 |
| 236-247 | 0x00EC-0x00F7 | 12 | forest 7, rock 4, jungle 1 |
| 252, 236 | 0x00FC, 0x00EC | **0** | inverted pair, matches nothing (F2) |
| 268-279 | 0x010C-0x0117 | 12 | snow 8, rock 4 |
| 286-297 | 0x011E-0x0129 | 12 | sand 8, rock 4 |
| 321-324 | 0x0141-0x0144 | 4 | dirt 4 |
| 467-474 | 0x01D3-0x01DA | 8 | rock 8 |
| 476-487 | 0x01DC-0x01E7 | 12 | dirt 12 |
| 492-495 | 0x01EC-0x01EF | 4 | dirt 4 |
| 543-579 | 0x021F-0x0243 | 37 | rock 22, grass 15 |
| **581-621** | **0x0245-0x026D** | **41** | **cave 41** |
| 1741-1757 | 0x06CD-0x06DD | 17 | rock 9, grass 8 |
| 1771-1790 | 0x06EB-0x06FE | 20 | rock 12, dirt 8 |
| 1801-1824 | 0x0709-0x0720 | 24 | forest 12, rock 12 |
| 1831-1854 | 0x0727-0x073E | 24 | jungle 12, rock 12 |
| 1861-1884 | 0x0745-0x075C | 24 | snow 12, rock 12 |
| 1981-2004 | 0x07BD-0x07D4 | 24 | NoName 24 |
| 2028-2033 | 0x07EC-0x07F1 | 6 | cave exit 6 |
| 2100-2105 | 0x0834-0x0839 | 6 | cave exit 6 |
| 0x3F39-0x3F74 | | 60 | Obsidian 48, blank 12 |
| 0x3F82-0x3F8F | | 14 | Obsidian 14 |
| 0x3F91-0x3FCF | | 63 | Obsidian 62, blank 1 |

For a cave, the land "cave" set 0x0245-0x026D and the "rock" sets (0x01D3-0x01DA, rock members of
0x021F-0x0243 and of 0x06EB-0x075C) are the mineable terrain. A wall built as raised terrain from these IDs is
mineable natively.

### 2.2 Mining static tiles (`_mountainCaveStaticTiles`, `Mining.cs:52-55`)

One pair: 0x053B-0x054F, 21 IDs, **all named "cave floor"** (non-wall, passable, height 0). So pinned mines the
cave *floor* statics. 0x0550 is "stone roof"; 0x0551-0x0553 are also "cave floor" but outside the pair, so not
mineable. 0x0554-0x0560 are "stone roof".

### 2.3 Cave wall statics: NOT mineable in pinned

Every tiledata item named "cave wall" (counted by name, 35 IDs, all Wall+Impassable flags):
- 0x025C-0x0276 (27; heights 22 at 0x025C-0x026A, 18 at 0x026B-0x026F, 3 at 0x0270-0x0276)
- 0x027D-0x0280 (4; height 24)
- 0x2166-0x2169 (4; height 22)

(0x0277-0x027C between them are "ruined wall".) None is in `_mountainCaveStaticTiles`, so targeting a static
cave wall gives "You can't mine that" (`Mining.cs:461-470`). The brief's "0x053B-0x0553 region" is floor, not
wall. Also checked: no tiledata item named stalagmite, rock or boulder is in the list (stalagmites
0x08E0-0x08EA, rock 0x1363-0x136C etc. are not).

**Building walls that mine natively, options:**
1. Terrain walls from the land IDs in 2.1 (cave 0x0245-0x026D or rock). Works with zero code.
2. Static cave-wall art with mineable cave-floor statics (0x053B-0x054F) at the wall foot, which is how pinned
   expects cave mining to work. Works with zero code, but players mine the floor, not the wall.
3. Make static cave walls mineable in the dungeon only: needs code (2.4).

### 2.4 If static cave walls (or custom root art) must be harvestable

Appending IDs to `OreAndStone.StaticTiles` (the setter is public, `HarvestDefinition.cs:21`) would make every
cave wall on every facet mineable, which violates "nothing outside the region". The region-safe way, still
additive: in our `partial Mining`, keep a private `HarvestDefinition DawnWalls` (StaticTiles = the 35 cave-wall
IDs, its own banks), override `GetDefinition(int tileID, bool isLand)` to return
`base.GetDefinition(...) ?? (DawnWalls.Validate(...) ? DawnWalls : null)`, and override `CheckResources` to
refuse `DawnWalls` when `Region.Find(loc, map)` is not the dungeon. Caveats: `Mining` code that tests
`def == OreAndStone` (`Mining.cs:279, 361, 379`) and our depletion/haze readers (1.1) will not see that
definition; `ProspectorsTool` will route through it (`ProspectorsTool.cs:70`) and refuses when
`Veins.Length <= 1` (`:72`). About +40 lines. Same pattern for Lumberjacking if Rootwood needs non-tree art.

### 2.5 Choppable tiles (`m_TreeTiles`, `Lumberjacking.cs:11-34`)

Exact-match list (no `RangedTiles`), `LandTiles` empty (`:50-51`). 149 IDs, all unique (counted), sorted at
`Initialize` (`:190-193`). Tiledata names: tree 23, leaves 64, Yew tree 19, cypress leaves 8, fall leaves 6,
oak leaves 4, walnut leaves 4, cypress tree 4, and 2 each of cedar tree, cedar needles, oak tree, walnut tree,
willow leaves, apple tree, peach tree, pear tree, plus willow tree 1. Trunk IDs useful in a cave:
"tree" 0x0CCA-0x0CCD, 0x0CD0, 0x0CD3, 0x0D41-0x0D44, 0x0D57-0x0D5B, 0x0D6E-0x0D72, 0x0D84-0x0D86;
"Yew tree" 0x12B5-0x12C7.

**There is no root, trunk or petrified-wood static in the list, and none in tiledata at all:** name search found
"root" only on reagents (mandrake 0x0F86, 0x18DD-0x18DE, 0xA815, 0xAF20; ginseng 0x18EB-0x18EC), "trunk" only
on 0x9E38 plum_tree_trunk, "petrif" nothing, and stumps (0x0DAC-0x0DAD, 0x0E56-0x0E59, 0x324B-0x324D,
0xA71B-0xA71D) are not choppable. So "giant roots in cave walls" that chop natively must be built from listed
tree statics (dead-looking trunks are a design/art choice, unverified visually), or use custom/other art plus
the 2.4 override. Custom client art in this shard's `client-data` was not checked.

---

## 3. Dawnstone (metal): every file a new CraftResource metal touches

### 3.1 How the 8 extended ores were added

- Enum and tables: full-file replacement `cust\ResourceInfo.cs` -> pinned `UOContent\Misc\ResourceInfo.cs`
  (`apply-patches.sh:200, 251`; excluded from the additive copy at `:200`). Diff vs pinned (859 -> 1170 lines):
  enum `Platinum..Celestial` after `Valorite` (`ResourceInfo.cs:19-27`), lumber `Ironwood..Starwood` after
  `Frostwood` (`:49-57`), `CraftAttributeInfo` fields (`:77-81`) and init blocks (`:260-386`), metal
  `CraftResourceInfo` entries after Valorite ending at `:741-745`, wood entries ending at `:1014`, and the metal
  range in `GetType` widened to `<= CraftResource.Celestial` (`:1092`).
- Item classes: `cust\ClusterFExtendedOres.cs:23-151` (8 `BaseOre` + 8 `BaseIngot`, `[SerializationGenerator(0, false)]`).
- Harvest and Blacksmithy sub-res: `cust\ClusterFMiningExtension.cs` (1.1; `AddSubRes` at `:174-181`).
- BODs: `patches\BulkMaterialType.cs:20-28` (explicit 12..19), `patches\SmallSmithBOD-PostValorite.patch`,
  `patches\LargeSmithBOD.cs` (replacement, adds `m_PostValMaterialChances` and `CreateRandomFor`).

### 3.2 Enum placement and serialization

Metals are implicit 1..17 (`Iron = 1` at `ResourceInfo.cs:9`, then sequential); leather restarts at an explicit
101 (`:29`). **Put `Dawnstone` after `Celestial` = 18.** Anything inserted before Celestial would renumber
Platinum..Celestial (10..17), which are stored by numeric value: on ore/ingots via `[SerializableProperty(0)]`
`Resource` (pinned `Items\Resources\Blacksmithing\Ore.cs:8, 20-31`), on crafted gear, and as raw `int` keys in
`HammerOfHephaestus` familiarity dictionaries (`cust\HammerOfHephaestus.cs:117, 148-176, 483, 516-543`). Value 18
leaves a gap of 82 before 101, so no collision.

The mechanical rules that follow from `CraftResources` (`ResourceInfo.cs:1043-1131`):
- `GetType` metal range `:1092` must become `<= CraftResource.Dawnstone`, or Dawnstone resolves to
  `CraftResourceType.None` and `GetInfo`/`GetHue`/`GetName` return null/0/"".
- `GetIndex` is `resource - Iron` (`:1116-1126`), so the Dawnstone `CraftResourceInfo` must be the 18th entry of
  `m_MetalInfo`, i.e. appended directly after the Celestial entry (`:741-745`), not grouped with the low tiers.
- `GetFromType` needs no edit: the `CraftResourceInfo` constructor registers its types (`:548-562`).

Consequence of placement: Dawnstone sorts numerically above Celestial. Nothing in shard code compares
CraftResource ordinals except `:1092` (grep for `<`/`>`/`and` on `CraftResource.` found no other range test);
pinned code that tests `DullCopper..Valorite` (e.g. `Ore.cs:42-44` label, `Ore.cs:176-187` smelt difficulty)
treats Dawnstone like the extended ores: generic "iron ore" label and smelt difficulty 50 (which is a sensible
starter value).

### 3.3 Grep: where the 8 extended ore names appear in customizations

Pattern `\b(Platinum|Toxic|Blaze|Frost|Obsidian|Mythril|Adamantium|Celestial)(Ore|Ingot|Granite)?\b` over all
791 `.cs` files under `cust\`: **21 files, 403 matching lines.** "Frost" also matches non-ore text; each file
below was checked to contain real ore references except where noted.

| File | Lines | What it is | Dawnstone needs |
|---|---|---|---|
| ResourceInfo.cs | 66 | enum, attributes, metal table | **required** (3.2) |
| ClusterFSmithCommissions.cs | 43 | commission material by skill `:424-446`, multipliers `:712-719`, skill bands `:780-789`, tier `:814-822`, names `:836-844`, BOD map `:732` | optional; recommend exclude |
| ClusterFExtendedOres.cs | 41 | ore/ingot classes | **required** (+2 classes, ~15 lines, any file) |
| ClusterFMiningExtension.cs | 38 | veins + Blacksmithy sub-res | **required**: 1 `AddSubRes` line; no vein (harvest is 1.3) |
| HammerOfHephaestus.cs | 33 | `HammerMetal.All` + `InferResource` `:44-87`, BOD maps `:1514-1575` | optional; note `Count` feeds a cap `:639` |
| ClusterFWorkOrderSystem.cs | 33 | Compact work orders, one per extended ore `:701-823` (`requiredDiscovery`) | optional |
| ClusterFSmithBODSystem.cs | 29 | seal multipliers `:273-284`, skill bands `:373-382`, tiers `:465-474` (BulkMaterialType) | only if Dawnstone BODs |
| CompactOreSatchelRoutingHook.cs | 17 | gate keys `:55-65`, discovery keys `:190-208` | optional (+1 discovery key); do not gate |
| TestCenter\TestCenterKitEntries.cs | 16 | test-center kit `:20-29` | optional |
| SmithGuildSalvageBag.cs | 14 | salvage skill `:60-76`, seals `:85-93` | optional (defaults 0) |
| SurveyArchivistGump.cs | 12 | report rewards `:33-52`, order `:219-225` | optional, with discovery key |
| ProspectorsLogbookGump.cs | 10 | order `:36-42`, display/colour `:45-62` | optional, with discovery key |
| ReinforcedOreSatchel.cs | 9 | smelt difficulty `:54-73` (default 0.0) | optional |
| SmithSealCatalogGump.cs | 8 | runic hammer catalogue `:89` | no |
| SmithGuildBook.cs | 8 | BOD material names `:720-729` | only if BODs |
| MinersCompactLiaisonGump.cs | 7 | Adamantium ingot as upgrade cost only | no |
| CompactOreSatchel.cs | 6 | `_acceptedTypes` `:38-62`; also covers its 4 subclasses (Deepdelvers `:25`, Reinforced `:34`, MasterExpedition `:27`, Surveyors `:24`) | **recommended** (+2 types) |
| JacobsWorldbreakerPickaxe.cs | 5 | Adamantium ingot as upgrade cost only | no |
| ClusterFCompactAdminTools.cs | 5 | seed-discovery keys `:391-397`, `[CompactOreInfo` list `:437-442` | optional |
| OreDiscoveryEntry.cs | 2 | comments only | no |
| ClusterFAccountData.cs | 1 | comment `:53`; `OreDiscoveries` is string-keyed (`:55`, serialized as count+entries `:370-371`) | no schema change |

Named in the brief, **zero** ore-name hits, no change needed: `ArtificerWorkOrderSystem.cs` (uses vanilla
`CraftResource.Gold..Valorite` at `:479-503`), `ArtificersSatchel.cs`, `ClusterFHuntersSatchelHooks.cs`,
`DeepdelversSatchel.cs` (inherits the satchel list), `ClusterFDevTools.cs` (only clears `OreDiscoveries`, `:188`),
`ClusterFGuildSystem.cs` (Iron only, `:112, 192`).

### 3.4 Crafting

- Blacksmithy: pinned registers vanilla sub-res in `Engines\Craft\DefBlacksmithy.cs:671-683`; ours appends at
  ServerStarted (`ClusterFMiningExtension.cs:165-184`). Dawnstone = one more `AddSubRes` line. It will list
  after Celestial, because `AddSubRes` appends; ordering it next to Iron would mean editing pinned
  `DefBlacksmithy` (not checked further).
- Tinkering: pinned `Engines\Craft\DefTinkering.cs:570-582` has Iron..Valorite. **The 8 extended ores are not
  added to Tinkering anywhere** (grep for `DefTinkering` in `cust\`: 0 hits). Dawnstone in Tinkering would be the
  first; one `DefTinkering.CraftSystem.AddSubRes` line at ServerStarted.
- `cust\CraftItem.cs` (replacement) needs nothing: `BaseIngot`/`BaseOre` are already in its colored-resource
  table (`:97-103`); its explicit pair table only lists woods (`:71-72`).

### 3.5 BODs

Pinned maps CraftResource to BulkMaterialType only for DullCopper..Barbed (`Engines\Bulk Orders\SmallBOD.cs:102-112`)
and every material test, reward and label is a `DullCopper..Valorite` range (`SmallBOD.cs:140`, `LargeBOD.cs:121`,
`Rewards.cs:438-440, 486-487`, the four BOD gumps). Our extended BODs live beside that in five places
(`patches\BulkMaterialType.cs`, `SmallSmithBOD-PostValorite.patch`, `patches\LargeSmithBOD.cs`,
`ClusterFSmithBODSystem.cs`, `SmithGuildBook.cs`) plus `HammerOfHephaestus.cs:1505-1575`. **Recommendation: no
Dawnstone BOD tier.** If wanted later: `BulkMaterialType.Dawnstone = 20` (append; 12-19 are taken,
`BulkMaterialType.cs:21-28`), then each switch above.

### 3.6 Size

Minimum viable Dawnstone (mineable in-region, smeltable, craftable, satchel-routed):
- `cust\ResourceInfo.cs` (replacement): enum +1, attribute field +1, attribute block ~12, `m_MetalInfo` entry ~9,
  range edit 1. **~25 lines.**
- New or existing item file: DawnstoneOre + DawnstoneIngot. **~15 lines.**
- Blacksmithy (+Tinkering if wanted): **1-2 lines.**
- Harvest (section 1.3): **~80-120 lines**, one new file, shared with Rootwood.
- `CompactOreSatchel.cs`: **+2 lines.**
Total: 4-5 files, ~125-165 lines, no `.patch`, no new upstream replacement.

Optional integration (discovery logbook, archivist reward, admin seed, hammer, salvage, work order, test kit):
8 more files, ~2-6 lines each, ~30 lines. Commissions/BOD integration: 6+ more files including two
patch-route files; not recommended for a starter metal.

---

## Findings worth raising (beyond the question)

- **F1 (latent crash candidate).** All 8 extended-ore `HarvestResource`s have exactly one type
  (`ClusterFMiningExtension.cs:86-93`), but pinned `Mining.GetResourceType` returns `resource.Types[1]` for a
  GM miner with `StoneMining && ToggleMiningStone`, at 10% (`Mining.cs:284-288`). That is an
  `IndexOutOfRangeException` inside the harvest timer (`Core\HarvestTimer.cs:30-36`); `Server\Timer\` has no
  `catch` (grep). Read from source only, not reproduced. Dawnstone must not copy the one-type pattern.
- **F2.** `_mountainCaveTiles` pair `252, 236` (`Mining.cs:28`) is inverted and matches nothing; the intended range is unknown.
  Pinned bug; harmless here.
- **F3 (matters for Rootwood).** `CraftResources.GetType` wood range is still `RegularWood..Frostwood`
  (`ResourceInfo.cs:1095`), so the 8 extended woods (enum 308-315) classify as `None` and `GetInfo` returns null
  despite their `m_WoodInfo` entries (ending `:1014`). A Rootwood appended after Starwood inherits this. Read
  from source only; effect on in-game hue/name not run-verified.

## Could not verify

- Runtime behaviour of anything above (no build, no server run, per brief).
- Which tree statics look like roots; whether shard `client-data` adds custom art; whether the dungeon needs a
  `regions.json` entry in addition to a code region.
- The exact byte encoding the source generator uses for the `CraftResource` property (only that it is the
  numeric enum value that must not move).
