# P24 s3b: Burrowhide (leather), Rootwood (wood), Gloomsilk (cloth), starter numbers

Read-only research. Nothing outside this scratch folder was changed. Engine = `D:\UO\ModernUO-pinned`
at `7c9215d97` (confirmed with `git log -1`). Abbreviations used below:

- `PIN/` = `D:\UO\ModernUO-pinned\Projects\UOContent\`
- `CUST/` = `D:\ShatteredLegacy\server\customizations\`
- `PAT/` = `D:\ShatteredLegacy\server\patches\`
- `AP` = `D:\ShatteredLegacy\docker\uo\apply-patches.sh`

**Build fact that matters for everything below:** `CUST/ResourceInfo.cs` is a full-file replacement of
`PIN/Misc/ResourceInfo.cs` (AP:251), as is `CUST/CraftItem.cs` for `PIN/Engines/Craft/Core/CraftItem.cs`
(AP:238-239). Top-level customizations are copied into `Misc/` additively (AP:193-201). So the
`CraftResource` enum, attribute tables and `GetType` ranges that actually compile are the CUST copy.

---

## 0. Findings outside the brief (read these first)

1. **Brief correction: there are eight extended woods, not six.** `CUST/ResourceInfo.cs:49-57` appends
   Ironwood, Ghostwood, **Emberbark, Frostbark**, Shadowbark, Runewood, Voidwood, Starwood (308-315).
2. **Apparent live bug: the extended woods are not classed as wood.** `CUST/ResourceInfo.cs:1095` still
   reads `>= CraftResource.RegularWood and <= CraftResource.Frostwood => CraftResourceType.Wood`
   (the metal range was widened to Celestial at :1092, the wood range was not). So for 308-315,
   `GetType` returns `None`, `GetInfo` returns null (:1062-1078), and therefore `GetHue` = 0 and
   `GetName` = "" (:1143-1168). `Log`/`Board` take their hue from `GetHue` (`PIN/Items/Skill Items/Lumberjack/Log.cs:26`)
   and fall back to `GetName` for their name line (Log.cs:58-72). Expected effect: extended logs and
   boards are unhued and carry no resource name. **Unverified in client**; no shard test covers it
   (grep of `server/tests` for GetHue/Ironwood finds only discovery-serializer tests). Any new wood
   must widen this range anyway, and widening it changes how the eight existing woods look. That is a
   decision, not a side effect.
3. **HuntersSatchel silently downgrades unknown hides.** `CUST/HuntersSatchel.cs:64-70`: any
   `BaseHides` not Spined/Horned/Barbed converts to plain `Leather`. A Burrowhide hide routed into the
   satchel would become regular leather unless a case is added.
4. **Pinned clothing has no resource-attribute path at all.** `PIN/Items/Clothing/BaseClothing.cs`
   has no `ArmorLuck`/`ArmorPhysicalResist` reads (grep: zero hits); `OnCraft` only sets `Resource`
   when `DefaultResource != None` (:199-204), which only shoes do (`PIN/Items/Clothing/Shoes.cs:48,72,160,174,226`).
   Cloth bonuses therefore need new code, not just data (section 3).

---

## 1. Burrowhide (leather)

### 1.1 How pinned does leather tiers

| Piece | Where | Notes |
|---|---|---|
| Enum values | `PIN/Misc/ResourceInfo.cs:19-22` (CUST :29-32) | RegularLeather=101, Spined 102, Horned 103, Barbed 104 |
| Type range | `PIN/Misc/ResourceInfo.cs:782` (CUST :1093) | `RegularLeather..BarbedLeather => Leather` |
| Attribute info | `PIN/Misc/ResourceInfo.cs:234-248` Spined; Horned/Barbed follow (CUST :387-438) | see section 4 |
| Info arrays (two) | `m_LeatherInfo` PIN :564, `m_AOSLeatherInfo` PIN :604 (CUST :799-877) | indexed by `resource - start` (CUST :1116-1126); AOS hues 0x8AC/0x845/0x851 |
| Hide items | `PIN/Items/Resources/Tailor/Hides.cs:6` `BaseHides`; 4 subclasses :91,119,147,175 | each `IScissorable`, scissors -> matching leather (e.g. :140 `ScissorHelper(from, new SpinedLeather(), 1)`) |
| Leather items | `PIN/Items/Resources/Tailor/Leathers.cs:6` `BaseLeather`; 4 subclasses :91,101,111,121 | |
| Names | Hides.cs:40-42, Leathers.cs:40-42 | cliloc arithmetic over `Spined..Barbed` only |
| Save format | Hides.cs:52 `_resource = (CraftResource)reader.ReadInt()` | enum stored as int: values must never move |
| HideType enum | `PIN/Mobiles/BaseCreature.cs:113-119` | Regular, Spined, Horned, Barbed |
| Creature props | BaseCreature.cs:1087-1088 `virtual int Hides`, `virtual HideType HideType` | |
| Carving | BaseCreature.cs:1649 `public virtual void OnCarve(...)`; skinning-knife leather switch :1727-1733; hide drop chain :1753-1768 | Felucca x2 (:1675-1679), ML human +10% (:1670-1673) |
| Tailoring sub-res | `PIN/Engines/Craft/DefTailoring.cs:658` `SetSubRes(typeof(Leather))`; :662-665 AddSubRes 0/65/80/99 | Tailoring uses **SubRes** for leather; **SubRes2 is unused** in DefTailoring (grep: no SetSubRes2) |
| Log/board-style equivalence | `PIN/Engines/Craft/Core/CraftItem.cs:72` (CUST :80-83) | `{SpinedLeather, SpinedHides}` pairs let hides count as leather |
| Armor | `PIN/Items/Armor/BaseArmor.cs:337-339` pre-AOS AR +10/13/16; :1233-1235 name cliloc; :1291 luck from AttributeInfo | |
| Clothing / weapon names | `PIN/Items/Clothing/BaseClothing.cs:684-686`, `PIN/Items/Weapons/BaseWeapon.cs:2866` | name prefix clilocs |
| Salvage | `PIN/Items/Containers/SalvageBag.cs:237` | type list |
| Test center | `PIN/Special Systems/Engines/TestCenter.cs:287,331` | |

**Creatures per hide type (counted, `override HideType => HideType.X`):**

Pinned, 33 creature files (+ BaseCreature itself):
- Spined 19: DireWolf, HellCat, PredatorHellCat, GiantToad, Ridgeback, SavageRidgeback, Alligator,
  GiantSerpent, IceSerpent, LavaLizard, LavaSerpent, Imp, RatmanMage, Ratman, RatmanArcher, Twaulo,
  Pixie, Centaur, Lizardman.
- Horned 5: Kirin, Unicorn, SeaSerpent, Drake, Wyvern.
- Barbed 9: Nightmare, GreaterDragon, AncientWyrm, Dragon, SerpentineDragon, ShadowWyrm, SkeletalDragon,
  WhiteWyrm, BakeKitsune.
- Explicit Regular 1: Meraktus.
- Files overriding `Hides =>` (any type): 82 (count only, list not reproduced).

Customizations, 23 creature files:
- Spined 14: PixieRenowned, RakktaviRenowned, TikitaviRenowned, VitaviRenowned, ClanChitterAssistant,
  ClanChitterTinkerer, ClanRibbonCourtier, ClanRibbonSupplicant, ClanScratchHenchrat,
  ClanScratchScrounger, Dimetrosaur, Kepetch, RuddyBoura, StoneSlith.
- Horned 7: WyvernRenowned, Allosaurus, HighPlainsBoura, KepetchAmbusher, LowlandBoura, Raptor, ToxicSlith.
- Barbed 2: StygianDragon, SkeletalDragonRenowned.

**Every file that names a tiered leather (consumers).**
Pinned `SpinedLeather|SpinedHides` (12 files): SmallBOD.cs, CraftItem.cs, DefTailoring.cs, BaseArmor.cs,
BaseClothing.cs, SalvageBag.cs, Hides.cs, Leathers.cs, BaseWeapon.cs, ResourceInfo.cs, BaseCreature.cs,
TestCenter.cs. Pinned `BulkMaterialType.Spined|Horned|Barbed` (11 files, all in `Engines/Bulk Orders/`):
BOBGump, LargeBOD, LargeBODAcceptGump, LargeBODGump, LargeTailorBOD, Rewards, SmallBOD,
SmallBODAcceptGump, SmallBODGump, SmallSmithBOD, SmallTailorBOD. Customizations + patches (6 non-creature
files): ClusterFWorkOrderSystem.cs (14 lines, e.g. :1450,:1517,:1608), CraftItem.cs :80-83,
HuntersSatchel.cs :66-68, ResourceInfo.cs, SmithGuildSalvageBag.cs :280-281, PAT/BulkMaterialType.cs :17-19.

**Tailor BODs.** `PAT/BulkMaterialType.cs:6-29` (replaces pinned) keeps Spined/Horned/Barbed at 9-11 and
appends ores at 12-19. All BOD code tests leather with `>= Spined && <= Barbed` ranges (e.g.
`PIN/Engines/Bulk Orders/SmallBOD.cs:144`, `LargeBOD.cs:126`, gumps' cliloc `1049348 + offset`) and the
material chance tables (`SmallTailorBOD.cs:14-16`, `LargeTailorBOD.cs:11-13`) and reward tables
(`Rewards.cs:749-788`). A Burrowhide BOD material would be value 20, outside every range.

### 1.2 What a fourth (starter) leather needs

| # | Change | File | Pinned patch? |
|---|---|---|---|
| 1 | Enum `BurrowhideLeather` **appended after BarbedLeather (=105)**, not inserted before Spined: values are saved as ints (Hides.cs:52; armor/clothing `Resource`), inserting would shift Spined/Horned/Barbed in every save. Leather block 101-199 has room. | CUST/ResourceInfo.cs:29-32 | no (CUST file) |
| 2 | Widen leather range to `<= BurrowhideLeather` | CUST/ResourceInfo.cs:1093 | no |
| 3 | `CraftAttributeInfo Burrowhide` + entry at index 4 in **both** leather arrays (name string, cliloc 0, hue) | CUST/ResourceInfo.cs ~:387, :799-877 | no |
| 4 | `BurrowhideHides : BaseHides, IScissorable` and `BurrowhideLeather : BaseLeather`, each with own `LabelNumber`/name (cliloc ranges stop at Barbed) | new CUST file | no |
| 5 | Equivalence pair `{BurrowhideLeather, BurrowhideHides}` | CUST/CraftItem.cs:80-83 | no (CUST file) |
| 6 | Tailoring sub-res: `DefTailoring.CraftSystem.AddSubRes(typeof(BurrowhideLeather), "Burrowhide", req, ...)` at ServerStarted, as the lumber extension does (CUST/ClusterFLumberjackingExtension.cs:263-282) | new or existing CUST file | no |
| 7 | Carving: **avoid** extending `HideType` (enum lives in pinned BaseCreature.cs:113 and the drop chain :1727-1768 would need a patch). Instead dungeon creatures set `Hides => 0` and override the virtual `OnCarve` (:1649) to add BurrowhideHides/Leather, or share a small base class. Must re-implement the Summoned/IsBonded/Animated guard (:1657-1658), Felucca x2 and skinning-knife branch if wanted. | new CUST mobiles | no |
| 8 | HuntersSatchel case `BurrowhideHides h => new BurrowhideLeather(h.Amount)` | CUST/HuntersSatchel.cs:64-70 | no |
| 9 | SmithGuildSalvageBag type list (optional) | CUST/SmithGuildSalvageBag.cs:280 | no |
| 10 | BODs: **recommend none.** Adding means BulkMaterialType 20 plus range edits in 11 pinned BOD files. | - | yes (11) |
| 11 | Armor name prefix / pre-AOS AR: switch returns 0 for unknown (BaseArmor.cs:1233-1245, :337-341). Acceptable; extended ores already live with it. | - | no |
| 12 | Work orders (optional) | CUST/ClusterFWorkOrderSystem.cs | no |

**Size: small-medium.** About 6-8 CUST files touched/added, roughly 150-250 lines, **zero pinned
patches** if BODs are skipped and carving goes through `OnCarve` overrides. Biggest risk: forgetting a
range (item 2) or the satchel (item 8); both fail silently.

---

## 2. Rootwood (wood)

### 2.1 How pinned does wood tiers

| Piece | Where |
|---|---|
| Enum | `PIN/Misc/ResourceInfo.cs:31-37` RegularWood 301 .. Frostwood 307 |
| Attribute info | PIN :323-333: **all six wood CraftAttributeInfo objects are empty** |
| Real wood bonuses | Only bows, ML only: `PIN/Items/Weapons/Ranged/BaseRanged.cs:230-234` calls private `ApplyWoodBonuses` (:239-281), a hard switch: Oak Luck+40 DamageInc+5; Ash SSI+10 LowerStatReq+20; Yew HCI+5 DI+10; Bloodwood RegenHits+2 HLL+16; Heartwood random (:283+); Frostwood 60/40 phys/cold DI+12. Unknown woods get nothing. |
| Info array | `m_WoodInfo` PIN :644-711, Oak hue 0x7DA cliloc 1072533 (:656-662) |
| Logs/boards | `PIN/Items/Skill Items/Lumberjack/Log.cs:142` OakLog etc; `PIN/Items/Skill Items/Carpenter Items/Board.cs:119` OakBoard; Board label range Oak..Yew only (Board.cs:46-48) |
| Harvest | `PIN/Engines/Harvest/Lumberjacking.cs:71-77` resources (req/min/max), :82-88 veins (Oak 300 of 1000 weight), tree tiles only (`StaticTiles = m_TreeTiles`, :51) |
| Carpentry sub-res | `PIN/Engines/Craft/DefCarpentry.cs:597` SetSubRes(Log); :601-607 Oak 65, Ash 80, Yew 95, Heart/Blood/Frost 100 |
| Bowcraft sub-res | `PIN/Engines/Craft/DefBowFletching.cs:262-270` same numbers |
| Tinkering | No wood sub-res: DefTinkering sub-res is ingots only (`PIN/Engines/Craft/DefTinkering.cs:570-582`) |

### 2.2 How our extended woods were added (counted)

Grep for the eight names across CUST + PAT: **16 files**. Real integration points are 11; 5 are false
positives (CharacterCreation.cs:98,109 "Ironwood Inn"; IronwoodCompositeBow.cs and Medusa.cs:100,116,
an artifact bow; ClusterFAccountData.cs:58 and WoodDiscoveryEntry.cs:82 comments).

| File | Hits | Role |
|---|---|---|
| CUST/ResourceInfo.cs | 57 | enum :49-57, empty attribute objects :488-496, m_WoodInfo entries :945-1018 (cliloc 0, string name) |
| CUST/ClusterFExtendedLumber.cs | 41 | 8 `*Log : Log` (axe to board at 100 skill) + 8 `*Board : Board`, all `SerializationGenerator(0,false)` |
| CUST/ClusterFLumberjackingExtension.cs | 47 | gate dictionary :33-43; vanilla discovery keys :48-57; `Give` override with discovery gate :59-102; grove logging :117-160; veins appended on WorldLoad :200-256 (req 100, weights 8..1); Carpentry AddSubRes on boards :274-281; Fletching AddSubRes on logs :293-309 |
| CUST/CraftItem.cs | 8 | log/board equivalence :72-79 (comment at extension :188-191 says m_TypesTable cannot be patched by reflection) |
| CUST/SeasonedLumberSatchel.cs | 8 | log->board map :56-63 |
| CUST/ForestersLumberSatchel.cs | 3 | comments only; accepts by `typeof(Log)`/`typeof(Board)` subclass (:34-40), so new woods are automatic |
| CUST/ForestersLogbookGump.cs | 21 | name lists :41-49, colours :60-67, thresholds :73-80 |
| CUST/ForestersGuildmasterGump.cs | 1 | name list :266 |
| CUST/ForestersLogbook.cs | 1 | comment :13 |
| CUST/ClusterFWorkOrderSystem.cs | 35 | wood work orders, e.g. :2246-2256, :2358-2389, `requiredWoodDiscovery` |
| CUST/TestCenter/TestCenterKitEntries.cs | 16 | kit registration :39-55 |

`AP:359-364` seds pinned `Lumberjacking` into `partial` so the CUST partial can override `Give`.

### 2.3 Grove tracking (P13)

`notes/cc-P13-grove-tracking.md` sections 1-2. Wood discovery is **keyed by string**
(`TryLogWoodDiscovery`, CUST/ClusterFLumberjackingExtension.cs:117-160): the item type is looked up in
the gated or vanilla dictionary (:33-57); groves record facet, region label and point and merge within
15 tiles on the same facet and region (:139-146). A new wood needs **one dictionary line**; no
serializer change (WoodDiscoveryEntry v1 is type-agnostic). A dungeon root logs its region by name
(the dungeon's named region), which P13 section 4 already treats as a non-teleportable grove.
Decision needed: gated (report to Foresters first) or vanilla (auto-Reported). A starter wood
probably belongs in the vanilla list.

### 2.4 What Rootwood needs

| # | Change | File | Pinned patch? |
|---|---|---|---|
| 1 | Enum `Rootwood` **appended after Starwood (=316)**; never between Frostwood and Ironwood | CUST/ResourceInfo.cs:57 | no |
| 2 | Widen wood range to `<= Rootwood` (fixes finding 0.2 too: decide) | CUST/ResourceInfo.cs:1095 | no |
| 3 | CraftAttributeInfo + m_WoodInfo entry at index 15 (string name, hue) | CUST/ResourceInfo.cs | no |
| 4 | `RootwoodLog : Log` (axe skill e.g. 0 or 40) + `RootwoodBoard : Board` | CUST/ClusterFExtendedLumber.cs | no |
| 5 | Equivalence pair | CUST/CraftItem.cs:79 | no |
| 6 | Carpentry + Fletching AddSubRes (2 lines) | CUST/ClusterFLumberjackingExtension.cs:274-309 | no |
| 7 | Discovery dictionary line | same file :33-57 | no |
| 8 | Satchel map line | CUST/SeasonedLumberSatchel.cs:56-63 | no |
| 9 | Logbook/guildmaster gump lists (if gated or shown) | CUST/ForestersLogbookGump.cs:41-80, ForestersGuildmasterGump.cs:266 | no |
| 10 | **Dungeon-only harvest.** The extended woods use the world-wide vein table (:202-256); Rootwood must not. Pinned `GetHarvestDetails` accepts an immovable `Static` item as a target (`PIN/Engines/Harvest/Core/HarvestSystem.cs:488-494`) but then validates its ItemID against tree tiles (:93, Lumberjacking.cs:51). Options: (a) "giant root" Static items using a tree ItemID, plus a `MutateVein` override in the CUST Lumberjacking partial (pinned Lumberjacking does not override it; base hook at HarvestSystem.cs:130,274) that forces the Rootwood vein when the target is a root or the region is the dungeon; (b) a self-contained root item with its own double-click/axe handling. (a) reuses skill gain and banks. | CUST Lumberjacking partial + new item | no |
| 11 | Bow bonus (optional): BaseRanged's switch is private and closed (:239-281). A bonus needs a patch to BaseRanged or a hook after `OnCraft`. Without it Rootwood is cosmetic for bows, like the eight extended woods. | PIN BaseRanged.cs | yes, if wanted |
| 12 | Test-center kit, work orders (optional) | CUST | no |

**Size: medium-small.** 7-9 CUST files, roughly 150-250 lines; the harvest gating (item 10) is most of
the new logic. Zero pinned patches unless bows should get a Rootwood bonus (1 patch). Board label
(Board.cs:46-48) and commodity DescriptionNumber (Log.cs:52-54, `1075062 + offset`) will be wrong or
off-range for 316, as they already are for 308-315 (unverified which cliloc 1075077 resolves to).

---

## 3. Gloomsilk (cloth)

### 3.1 What pinned has

- **No cloth CraftResource or CraftResourceType.** `CraftResourceType` is None/Metal/Leather/Scales/Wood
  (`PIN/Misc/ResourceInfo.cs:40-47`); no cloth block in the enum (:6-38).
- Cloth items carry **no resource field**: `Cloth` (`PIN/Items/Resources/Tailor/Cloth.cs:8`, ctor :11-15,
  hue only via Dye :21-31, scissors to Bandage :33-43), `UncutCloth` (UncutCloth.cs:8, scissors to
  Bandage :33-40), `BoltOfCloth` (BoltOfCloth.cs:8, scissors to 50 Cloth :41). All are
  `SerializationGenerator(0, false)` and not sealed.
- "Silk" in pinned (3 files): `SpidersSilk` reagent (`PIN/Items/Resources/Reagents/SpidersSilk.cs:6`),
  `DreadSpiderSilk` quest item (`PIN/Engines/ML Quests/Items/DreadSpiderSilk.cs:6`), and `Silk`, a
  paragon GiantBlackWidow mob (`PIN/Mobiles/Monsters/ML/Twisted Weald/Silk.cs:7`). None is a cloth.
- Tailoring consumes cloth as plain `typeof(Cloth)`: 58 occurrences in DefTailoring.cs, 49 of them
  as the primary resource of an `AddCraft` line (counted with grep). Other `typeof(Cloth|UncutCloth|BoltOfCloth)`
  users: DefCarpentry.cs 29, SBWeaver.cs 10, SBTailor.cs 4, CraftItem.cs 2, DefBlacksmithy.cs 1,
  SalvageBag.cs 1. CUST TailoringCraftRegistrations.cs adds 2 more.
- **Hue retention:** `DefTailoring.RetainsColorFrom` (DefTailoring.cs:50-62) checks exact
  `typeof(Cloth)`/`typeof(UncutCloth)`; the general fallback `CraftItem.RetainsColorFrom`
  (`PIN/Engines/Craft/Core/CraftItem.cs:357-379`) accepts **subclasses** of `Cloth` for BaseClothing
  products (`m_ColoredResourceTable` :88-94, IsSubclassOf :375). The hue comes from the consumed item
  (`OnResourceConsumed` :778-789). Consumption matches subclasses too: `Container` uses
  `type.IsInstanceOfType(item)` (`Projects/Server/Items/Container.cs:825,863,891`), the same reason
  extended logs were counted as `Log` (CUST/ClusterFLumberjackingExtension.cs:288-291).
- **Sub-resource slots:** Tailoring uses SubRes for leather (DefTailoring.cs:658-665). **SubRes2 is free**
  in tailoring; it exists per craft system (`PIN/Engines/Craft/Core/CraftSystem.cs:29,49,314-330`), is
  chosen per recipe by `UseSubRes2` (CraftItem.cs:162, :601), and Blacksmithy uses it for dragon scales
  (`PIN/Engines/Craft/DefBlacksmithy.cs:685-692`, 6 SetUseSubRes2/SetSubRes2 lines in that file).
- **No resource bonuses on clothing** (finding 0.4).

### 3.2 Two ways to build it

**A. Cosmetic cloth subclass (small, near change).** `GloomsilkCloth : Cloth` (and optionally
`GloomsilkBolt : BoltOfCloth` that scissors to GloomsilkCloth) with a fixed hue, Dye refused. It is
consumed by every cloth recipe unchanged and its hue carries to clothing through the subclass path above.
No enum, no sub-res, no pinned patch. **Size: 1 new CUST file, about 60-100 lines.** Limitation: no
stat bonus, and the player cannot pick it in the gump; the craft takes whichever cloth stacks it finds
(hue grouping: CraftItem.cs:791).

**B. Real tier (subsystem).** Needs: a `Cloth` block in `CraftResource` (e.g. 401+) and a new
`CraftResourceType.Cloth` with `GetType`/`GetStart`/`GetInfo` arms and an info array (CUST ResourceInfo);
a `Resource` field on Cloth/UncutCloth/BoltOfCloth (pinned files, serialized version bump, 3 patches) or
parallel subclasses; DefTailoring `SetSubRes2(typeof(Cloth))` + `AddSubRes2` + `SetUseSubRes2` on each
of the 49 cloth recipes (registration loop in CUST is possible: `CraftSystem.SetUseSubRes2(int,bool)`
:263); a BaseClothing patch so `OnCraft` records the cloth resource and applies attributes (there is
no path today); name prefix handling (BaseClothing.cs:674-694). **Size: subsystem, roughly 400-700
lines, 3-5 pinned patches.** Not recommended for a starter tier.

### 3.3 Getting it from cave spiders

- **Loot:** spiders already `PackItem(new SpidersSilk(n))` in their constructor
  (`PIN/Mobiles/Monsters/Arachnid/Melee/GiantSpider.cs:43`, FrostSpider.cs:46, GiantBlackWidow.cs:42,
  `Magic/DreadSpider.cs:44`). A new `CaveSpider` (CUST mobile) can `PackItem(new GloomsilkCloth(n))`
  or add it in `GenerateLoot`. Simplest, no carving needed.
- **Carve:** the Wool/Feathers analog is `virtual int Wool`/`Feathers` (BaseCreature.cs:1081-1082)
  which hard-code `TaintedWool`/`Feather` in `OnCarve` (:1690-1700). No generic hook exists; override
  the virtual `OnCarve` (:1649) and `corpse.AddCarvedItem(new GloomsilkCloth(n), from)`, the same call
  the base uses (:1693). Same guard caveats as 1.2 item 7.

---

## 4. Starter numbers: existing lowest tiers, then a first proposal

### 4.1 Existing (pinned; CUST copy identical for these rows)

| Tier | Harvest req / min / max | Craft sub-res req | CraftAttributeInfo (AOS) | Other |
|---|---|---|---|---|
| Dull Copper | Mining 65 / 25 / 105 (`PIN/Engines/Harvest/Mining.cs:116-123`, PAT/Mining.cs same lines); vein 112 of 1000 (:193, Iron 496 at :192) | Blacksmithy 65 (`DefBlacksmithy.cs:676`), Tinkering 65 (`DefTinkering.cs:575`) | ArmorPhysicalResist 6, ArmorDurability 50, ArmorLowerRequirements 20, WeaponDurability 100, WeaponLowerRequirements 50, Runic 1-2 attrs, ML intensity 40-100 (`ResourceInfo.cs:61-78`) | hue 0x973 (:431); pre-AOS AR +2 (`BaseArmor.cs:329`) |
| Spined | from creatures, no skill (Hides on 19 pinned + 14 CUST creatures) | Tailoring 65 (`DefTailoring.cs:663`) | ArmorPhysicalResist 5, ArmorLuck 40, Runic 1-3 attrs, ML intensity 40-100 (`ResourceInfo.cs:234-248`) | AOS hue 0x8AC (m_AOSLeatherInfo :604-622); pre-AOS AR +10 (`BaseArmor.cs:337`) |
| Oak | Lumberjacking 65 / 25 / 105 (`Lumberjacking.cs:72`); vein 300 of 1000 (:83) | Carpentry 65 (`DefCarpentry.cs:602`), Bowcraft 65 (`DefBowFletching.cs:265`) | **empty** (`ResourceInfo.cs:323`) | bows only, ML: Luck +40, DamageInc +5 (`BaseRanged.cs:245-249`); hue 0x7DA (:656) |
| Cloth | n/a | none (no tiers) | none; clothing reads no resource attributes | hue = dyed hue of consumed cloth |

Pattern in both harvest tables: min = req - 40, max = req + 40.

### 4.2 Proposal (first cut, for discussion)

"Low skill" = harvestable and craftable well before the 65 of the current lowest tier. "Modest" =
about half of that tier's bonus, no runic tools.

| Resource | Harvest req / min / max | Craft req | Bonus proposal | Needs code beyond data? |
|---|---|---|---|---|
| Dawnstone (ore) | Mining 45 / 5 / 85 | Blacksmithy/Tinkering 45 | ArmorPhysicalResist 3, ArmorDurability 25, ArmorLowerRequirements 10, WeaponDurability 50, WeaponLowerRequirements 25, Runic 0 | no (CraftAttributeInfo is read by armor/weapons) |
| Burrowhide (leather) | none (carve); dungeon creatures only | Tailoring 45 | ArmorPhysicalResist 2, ArmorLuck 20, Runic 0 | no |
| Rootwood (wood) | Lumberjacking 45 / 5 / 85 | Carpentry/Bowcraft 45 | bows: Luck +20, DamageInc +2 (half of Oak) | **yes**: BaseRanged patch (2.4 item 11), else cosmetic |
| Gloomsilk (cloth) | none (spider loot) | n/a under option A | hue only | bonus needs option B |

Notes on the proposal:
- 45 sits above Spined/Oak/Dull Copper's min (25) so a 45-skill player still fails sometimes; with
  min 5 a novice can occasionally succeed. Mirror the -40/+40 shape so skill-gain behaves like other tiers.
- Craft req 45 is below the existing 65 gate, so the starter tier is reachable before Spined/Oak/Dull
  Copper. If the starter tier should not undercut those, use 65 (same as lowest tier) instead.
- Placement: the enum must append (Dawnstone after Celestial, Burrowhide 105, Rootwood 316), so
  "starter" is a numbers choice, not an enum position. Code that compares tiers by enum order (e.g.
  BOD `>=`/`<=` ranges, `GetRandomResource(start,end)` at CUST ResourceInfo.cs:1154-1157) would treat these
  as top-of-range. None of the four should enter BOD tables.
- Fidelity: these are custom resources; every number here is a documented deviation for
  `docs/fidelity-principle.md` if adopted.

---

## 5. Unverified

- Client appearance of extended woods (finding 0.2): reasoned from code, not seen.
- Which cliloc `1075062 + 15` (Log.cs:52-54) resolves to for a Rootwood commodity deed.
- That `OnCarve` overrides get the skinning-knife (AOS) path right; I read the base only.
- Whether a Static with a tree ItemID placed inside a dungeon is chopped cleanly (CheckRange/banks);
  `CheckHarvest` overrides in pinned Lumberjacking (:125-156) were not read line by line.
- The Dawnstone numbers depend on the metal agent's design; only the Dull Copper reference row is mine.
- Counts of creature files use the one-line `HideType => HideType.X` form; I also grepped every
  `HideType.Spined|Horned|Barbed` use and found no other form outside BaseCreature.cs, so counts stand.
