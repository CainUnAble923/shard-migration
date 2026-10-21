# cc-P199: port the Base items remainder (resources, equipment, containers, tools, functional)

Written 2026-10-20 by the Gold Golem (Opus), on branch golem/Gold/P199 of both repos. Prompt:
`cc-prompts/claimed/Gold/cc-P199-port-base-items-remainder.md`. Both repos were clean at the start. Not committed: the
Golem commits after P199 DONE.

## Headlines

1. **The row moved from 172 / 298 to 250 / 298 files** (`tools/progress.py`, the stem proxy). The brief's "106 of 220"
   is the 2026-10-13 list; counted today with the same method the row has 298 candidates, 172 done at the start (later
   prompts and the row's own growth). All Port systems: **556 / 983 (56.6%)** after. The 48 files left are all
   equivalents pinned already has under another name (29) or declined subsystems (19); the list is in section 5.
2. **Trap training kits, Remove Trap's gain path, are in and reachable.** The circuit, cylinder and slider kits
   (ServUO Items/Functional), the circuit gump (ServUO Gumps/Traps/CircuitTrap.cs), and the vendor who sells them, the
   Collector of Oddities (99,375 gold each), with a dry-run placement command at ServUO's spot (Moonglow, Trammel
   4305,1003). Remove Trap follows ServUO at Endless Journey: no 50 Lockpicking / 50 Detect Hidden prerequisite. The kits
   train Remove Trap only; nothing in ServUO's kits trains Lockpicking (the brief's "Lockpicking and Remove Trap gain
   paths" is the port list's wording; see section 4).
3. **What the other ports were waiting for is wired.** Eleven bulk order reward placeholders are real rewards now
   (automaton actuator, Blackrock moonstone, Blackrock automaton head, eight runic mallets and chisels); the mana phasing
   orb and fey wings pay Clean Up points; the orb and both skeleton keys are in the treasure map supply loot; the
   chicken coop is craftable beside the incubator; Forged Metal of Artifacts works (one Enhance patch line).
4. **78 ServUO files ported**, 82 new .cs files in `server/customizations` plus 3 new patches; 6 new test files, one fact
   added to an existing one and one count changed: **73 new facts, every one seen red** (75 breaks, 2 builds, files hashed and restored
   byte-identical both times). Shard tests **1,684 passed, 4 skipped, 0 failed** of 1,688 (P193 reported 1,554 passed;
   the rest are the branches merged since and these 73). The test world boots, saves and reloads clean on `sl-modernuo:cc-P199`.
5. **Client check: nothing blocked.** Every item, gump and art id the ports use is in the shard's 7.0.117 client
   (scripted check against `tiledata.mul`, `artLegacyMUL.uop` and `gumpartLegacyMUL.uop`, section 6).
6. **Five porting agents** did the bulk in parallel (resources and tools, containers, storage, functional, addons and
   Eodon), each from one brief (scratchpad `BRIEF.md`); I wrote the kits, the vendor, the patches and the wiring, built
   every cycle and fixed what the builds found. All of their reports are folded in below.

## 1. What changed, with file:line

### Trap training kits (mine)

| File | What |
|---|---|
| `server/customizations/Items/Functional/CircuitTrapTrainingKit.cs:17` | ServUO's kit: Remove Trap opens the circuit; grid 9 below 80, 16 below 100, 25 from 100 (`:57-62`); finishing rolls Remove Trap 0-100 (`:88`). Saves grid size, path and progress (`:19-26`) |
| `server/customizations/Items/Functional/CylinderTrapTrainingKit.cs:15` | A `PuzzleChest`: Remove Trap sends the puzzle gump (`:38`), a right answer rolls Remove Trap 0-100 and sets a new solution (`:57-64`), a wrong one does nothing (`:44`), no treasure inside (`:28`) |
| `server/customizations/Items/Functional/SliderTrapTrainingKit.cs:25` | The sliding picture: eight styles, ServUO's solvable shuffle (`Reset`), the gump (`SliderTrapGump`), a solve rolls Remove Trap 0-100 and reshuffles |
| `server/customizations/Gumps/Traps/CircuitTrap.cs:14` | `ICircuitTrap`, `CircuitCount`, `CircuitTrapGump` (ServUO's BaseGump on pinned's `DynamicGump`; layout, paths and replies ServUO's) |
| `server/customizations/Quests/Eodon/MyrmidexThreat/Mobiles/CollectorOfOddities.cs:15` | The vendor and his shop (`:51-53`), ServUO Questers.cs:205-268 |
| `server/customizations/Quests/Eodon/MyrmidexThreat/ClusterFCollectorOfOdditiesPlacement.cs:18` | `[ClusterFPlaceCollectorOfOddities [dryrun]` at ServUO's Generate.cs:207-211 spot |
| `server/patches/RemoveTrap-trap-training-kits.patch` | `IRemoveTrapTrainingKit` (ServUO RemoveTrap.cs:15-18), its target branch (`:60-63`), the EJ rule (`:30-37`) |
| `server/patches/PuzzleChest-trap-training-kit.patch` | `OnWrongGuess` virtual (ServUO's `DoDamage` is virtual, Services/Khaldun/PuzzleChest.cs:372) and `SendPuzzleGump` (pinned's gump class is private) |
| `docker/uo/apply-patches.sh` (end of the patch list) | The three cc-P199 patches, after RemoveTrap-treasure-chest-disarm |

### The batches (agents)

Resources and tools (24 files): `Items/Resource/` AbyssalCloth, Blackrock, BloodOfTheDarkFather, EssencePersistence,
EtherealSand, FeyWings, IGem, LiveRock, OceanSapphire, PolishedMeteorite, PrimalLichDust, SmallFish, VoidEssence,
WoodPulp, WorkableGlass; `Items/Tools/` BegFishingPole, SkeletonKey (class `Skeletonkey`, ServUO's spelling),
MasterSkeletonKey, MetallicDyeTub, RunicMalletAndChisel, SteamPoweredBeverageMaker, PetBondingPotion;
`Items/Equipment/Talismans/` TalismanofGoblinSlaying, ManaPhasingOrb.

Containers (16 files, `Items/Containers/`): EssenceBox, GargoyleWoodenChest, JaacarBox, RewardBag (BaseRewardBag and the
reward helpers; its four bags are pinned's), Average/Meager/ValuableImbuingBag, Bulging/Dusty/MeagerMuseumBag,
RewardBackpack (three dusty backpacks), ScrollBox, ScrollBox2, ScrollBox3, ShipsStrongbox, UnknownSkeletons (three).

Storage (10 files): `Items/Tools/` ChestOfSending, GreaterBraceletOfBinding, ForgedMetalOfArtifacts, PenOfWisdom;
`Items/Functional/JewelryBox/` JewelryBox, JewelryBoxFilter, JewelryBoxGump; `Items/Functional/SeedBox/` SeedBox,
SeedBoxGump, SeedEntry (`Server.Engines.Plants.SeedEntry`; ours has an unrelated nested one in the New Haven seeder).

Functional (11 files): `Items/Functional/` Grinder, AcidVine, BaseDecayingItem, SlidingDoors, BaseArtifactLight,
BaseSwitch, Switches (UnderworldSwitchWE), GoblinFloorTrap (and its kit), ScaleCollar, CoralTheOwl;
`Items/Equipment/Instruments/SnakeCharmerFlute.cs` (the charm table and its walk through pinned's herding field).

Addons and Eodon (15 files plus one leaf): `Items/Functional/Automaton/` (nine: the actuator, moonstone, the three heads,
KotlAutomaton, BlackrockAutomaton, BrokenAutomatonHead, AutomatonStatue), ChickenCoop, HouseCraftables, StrangeContraption,
SerpentNest, SerpentsJawbone; the leaf `Services/InstancedPeerless/Medusa/RareSerpentEgg.cs` (a 12-hour `PeerlessKey`,
our DraconicOrb's shape).

Every file carries a header naming its ServUO source and each deliberate difference with ServUO's file:line.

### The wiring (mine)

| File | What |
|---|---|
| `server/customizations/Services/BulkOrders/BODRewardCollections.cs:186, :191, :194, :207-226, :314-316` | 11 placeholders become rewards: the three automaton parts (ServUO Rewards.cs:1064-1066) and eight mallets through ServUO's `RunicMalletAndChisel(type)` (`:1243-1249`); header :13-17 updated |
| `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs` | `ManaPhasingOrb 500` (ServUO :457), `FeyWings 75` (:736), were MISSING comments |
| `server/customizations/Services/TreasureMaps/TreasureMapInfo.cs:529-543` | ServUO's `_SpecialSupplyLoot` (:586-593) gains the orb in all five packages and both keys for the Assassin (ServUO's `typeof(SkeletonKey)` there names Enrico's collection mobile, a slip for the key) |
| `server/customizations/Engines/Craft/IncubatorCarpentryRecipe.cs` | the chicken coop, ServUO DefCarpentry.cs:231 (90-115, 150 boards, SA), registered with the incubator |
| `server/patches/Enhance-forged-metal-of-artifacts.patch` | ServUO Enhance.cs:253-258: the forged metal's aura forces one enhance to succeed |
| Blacksmithy/Tailoring/TinkeringCraftRegistrations.cs | three "in neither tree" comments now say the recipe gate is what keeps those entries out |
| `CHANGELOG.md` `## 2026.10.20.10`, `VERSION` | patch notes (Added, Changed, Staff) |

## 2. Tests (each new one seen failing first)

New fact files, all `[Collection("Sequential UOContent Tests")]`:

| File | Facts |
|---|---|
| `server/tests/Items/Functional/TrapTrainingKitVerification.cs` | 9: the kits as ServUO; Remove Trap at 0/0/0 opens the circuit; the grid by skill; walking the circuit and a wrong step; the slider one move from solved; the cylinder trains without hurting; a round trip of the three; the Collector's shop and placement (dry run, place, skip); the three patched files in the build tree |
| `server/tests/Items/P199ResourcesToolsVerification.cs` | 13 |
| `server/tests/Items/P199ContainersVerification.cs` | 10 |
| `server/tests/Items/P199StorageVerification.cs` | 9 |
| `server/tests/Items/P199FunctionalVerification.cs` | 17 |
| `server/tests/Items/P199AddonsEodonVerification.cs` | 14 |
| `server/tests/Mobiles/Normal/CC6FollowupBreathIncubatorVerification.cs` (one fact added) | the chicken coop's carpentry entry |
| `server/tests/Services/CleanUpBritanniaPointsVerification.cs` (count changed) | the table has two more rows |

Every ported type constructs with ServUO's values and round-trips with its saved fields set; each batch file lists its
facts at its top. Every fact cleans up what it made.

**Seen failing first.** Breaks in the ported code and the patches' `+` lines only, never the tests, applied by a script
that copies and hashes each file first (`breaks.py` in my scratchpad; break lists `breaks-*.json` there, one per batch,
written by an agent that read its batch's facts):
- Set 1, 75 breaks in 54 files, one build: **74 failed, 1,610 passed**. Of the 73 new facts, 72 red; plus the BOD reward
  list fact and the Clean Up count fact, both aimed at. Restored: 54 files, byte-identical.
- The one that stayed green, `ASkeletonKeyCannotPickAnUnpickableLock`, was masked by a second break in the same file
  (a master key that never opens anything cannot open an unpickable lock either). Set 2, that break alone: **1 failed,
  1,683 passed**, the fact red. Restored byte-identical.

**Builds.** `docker/uo/build.sh -t sl-modernuo:cc-P199`, docker-build lock taken before the first build and released after the image. Cycle 1 a
Docker metadata lock error (nothing built); cycles 2-5 compile fixes (generator backing-field clashes in ChestOfSending
and JewelryBoxFilter, a missing using, a name clash in my RemoveTrap patch, three test usings, two xUnit analyzer rules);
cycle 5 ran 1,687 tests with 7 red: five new facts, all real (below), and two older facts
(`CC6Batch2CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape`, `CC6Batch8Verification.MedusasGaze...`) that pass
alone and with each new class, and went green once the new failures were fixed: the failing facts left state behind.
Cycles 6-8 fixed the rest; the final full build passed 1,684 and built the image.

What the five red facts found, fixed in the code or the test:
- **The serialization generator never calls a `[SerializableProperty]` getter at save** (read in the generated source:
  it writes its own backing field). The greater bracelet's and the seed box's computed "saved" list properties were
  therefore never written: every friend slot and every seed slot was lost at a save. Both now keep a
  `[SerializableField]` list in step on every change (`SyncSaved`) and rebuild their slots in `[AfterDeserialization]`.
  Worth knowing for every future port: a computed `[SerializableProperty]` without `useField` does not save.
- The host never runs `BaseHouse.Configure`, so `Item.LockedDownFlag` is 0 and `IsLockedDown` cannot be set: the Coral
  and storage facts now set pinned's values (BaseHouse.cs:1304-1305) and put them back.
- The automaton is placed on the tinker's tile (ServUO KotlAutomatonHead.cs:58) and its AI steps before the fact read
  it; the fact allows two tiles.

## 3. Headless boot

`sl-modernuo:cc-P199` on a scratch copy of this desk's test world (`server/lib/uo/modernuo-test/Saves`, 134 KB: this
PC's test world is nearly empty, so the seeders build most of it at load), mounted as the compose file mounts it, the
shard's 7.0.117 client data read-only, loopback only, autosave off, no port published, under the test-shard lock. Three
boots: `Loading world done (660 items, 99 mobiles)`, then `(651 items, 99 mobiles)` twice; the third followed through
the stop: `Saving world done`, `Writing world save snapshot done`, `[SaveOnShutdown] ...saved in 670 ms`, `Shutting
down`. Zero exception lines in the three logs. The image was built before the changelog section was added, so it reports
`2026.10.20.9`; the next build carries `2026.10.20.10`. Nothing in that world is a type of this port; the three patches
add no saved field to any pinned type, so no migration JSON was needed.

Two comment-only edits after the final build (a section sign replaced by the word "section" in
`IncubatorCarpentryRecipe.cs` and `CC6FollowupBreathIncubatorVerification.cs`, for the ASCII rule); no code changed.

**Not done:** a client. Nothing here was seen in game.

## 4. Deviations and decisions for Chase

Where the port met the shard's own rules:
- **Remove Trap's prerequisite is gone**, as ServUO has it at Core.EJ (RemoveTrap.cs:30-37); the shard runs EJ. The
  shard's 200-cap and loop rules are untouched: the kits roll the ordinary `CheckTargetSkill`.
- **The trap kits train Remove Trap only.** The port list says "Lockpicking and Remove Trap gain paths"; ServUO's three
  kits roll Remove Trap and nothing else (ServUO CircuitTrapTrainingKit.cs:87, CylinderTrapTrainingKit.cs:61,
  SliderTrapTrainingKit.cs:146; ours :88, :61, :149), and the circuit's Lockpicking 100 "decipher" button is off for kits.
- **The Collector of Oddities is placed by a command, not a spawner.** ServUO uses an XmlSpawner; here he is placed once
  with a home range of 5, and the command re-places him if he is ever gone. His fourth item, the Stasis Chamber Power
  Core, is a Myrmidex Threat quest item and is left out.
- **The kits' ServUO quirks fixed:** the cylinder kit holds no treasure (ServUO's inherits a puzzle chest's 600-900 gold
  that nobody can reach); the circuit kit saves its grid size (ServUO's reloads at size 0 mid-circuit); the circuit
  gump's "show next" reads in range (ServUO `<=` reads one past the path).

From the batches (each in its file's header; the ones a player could notice):
- **ScaleCollar**: ServUO creates the 30 s release timer and never starts it, so a collared chicken stays frozen for
  good; here it is started.
- **GoblinFloorTrapKit**: ServUO re-checks skill, mount and guard zone and then places the trap anyway (`if`, not
  `else if`); here a failed check stops it.
- **CoralTheOwl**: ServUO's news timer is unbounded and leaks on a second "news"; here each telling is a counted timer
  in pinned TownCrier's shape.
- **ChestOfSending**: ServUO adds a charge at world save; pinned's generator has no save hook, so the chest catches up
  one charge per elapsed interval when used, and saves its next recharge time (ServUO does not, so every ServUO restart
  gives a charge).
- **GreaterBraceletOfBinding**: ServUO reads every slot back as a greater bracelet and silently drops friends wearing an
  ordinary one at each restart; here they are kept. `MaxRecharges` -1 ("no limit") is `int.MaxValue` (pinned's powder
  has no -1 case).
- **PenOfWisdom**: runebooks only (no runic atlas in either tree). Kept from ServUO and worth a decision: the pen is
  never deleted, works at 0 or negative uses, and says "crumbles to dust" every time.
- **UnknownMageSkeleton**: ServUO's scroll draw can run one past the table and throw; a null scroll is skipped.
- **The museum bags and dusty backpacks** drop ServUO's TerMurQuestRewardBook (in neither tree); ApplyMods takes
  ServUO's BaseRunicTool branch (no RunicReforging here); the backpacks' Stygian loot pool is built from pinned's tables
  without ServUO's SA tables.
- **KotlAutomaton**: `CanTransfer => false` has no pinned hook (an automaton could be transferred to another GM
  tinker); `CanFriend` is pinned's `AllowNewPetFriend`; IRepairableMobile dropped; creature rules as the port recipe
  (perception and speeds defaulted, SetWeaponAbility as GetWeaponAbility).
- **HouseCraftables**: pinned's CraftItem has no `Data` or create-item delegate, so a crafted piece takes its kind from
  the craft entry's name number; the two doors need a create hook (section 5).
- **SerpentsJawbone**: ServUO's RestrictRedsToFel is a config value (General.cfg:20, True); hard-coded true here.
- **SnakeCharmerFlute**: pinned's AI herds only in Wander (and Combat at AOS), so a fleeing snake does not walk; pinned
  clears the herding point on arrival where ServUO holds the snake there.
- **DragonBlood and MysticBook are pinned's DragonsBlood and MysticSpellbook** (same art and values); not ported again.
  The carving yield ServUO's creatures give (`DragonBlood => n`) still needs a BaseCreature carve hook (section 5).

## 5. Left for the next prompt

Not ported, with what each needs:

| Files | Why | What it would take |
|---|---|---|
| BedlamAltar, BlightedGroveAltar, CitadelAltar, ParoxysmusAltar, PrismOfLightAltar, TwistedWealdAltar (6) | the ML peerless altar system (`PeerlessAltar`) is in neither tree; ours has the bosses and keys, not the altars | a Peerless prompt: the altar base, its encounter and the key consumption |
| WallSafe | its whole purpose is ServUO's per-character secure gold balance on Account (`GetSecureAccountAmount` and kin, a saved field) | an Account change, or a decision to point it at bank gold |
| BookOfMasteries | Skill Masteries ("Later" on the port list) | the masteries system |
| PrimevalLichPuzzle | needs the Primeval Lich champion (`ChampionSpawnType.Infuse`), ScrollOfTranscendence and a ChampionSpawn patch | the champion |
| EtherealRetouchingTool | pinned's ethereals have no saved Transparent state | a pinned-base saved field |
| DragonTurtleEgg | DragonTurtleHatchling and DragonTurtleScute (ServUO TOL) | a 3-file port; our Pet Training and ChickenLizardEgg already have what it needs |
| FocusingGemOfVirtueBane | ExtendedWeaponAttributes.Focus and NegativeAttributes.Brittle, saved on BaseWeapon | the rage-focus and brittle system |
| BoxOfCrystalItems, BoxOfShadowItems | boxes of 18 addon deeds, none in either tree (reward-pool row) | the Crystal and Shadow furniture sets |
| CraftsmanSatchel, RewardBox | pinned has the equivalents (`CraftmansSatchel.cs`, RewardStrongbox) with different fills | a decision whether ServUO's fills replace pinned's |

Equivalents pinned or ours already has (the stem proxy keeps counting them): the 18 Gargish leather, stone and cloth
files (pinned's Type1/Type2 classes, each `[TypeAlias]`ed to the ServUO name), Gargoyle Accessories (pinned's tails),
DecorativeBox, FancyElvenArmoire, SimpleElvenArmoire, TrapableContainer (`TrappableContainer`), BaseTrash (ours,
CleanUpTrash), the two Mahjong packet files, DragonBlood, MysticBook, ElvenFletchings, LavaSerpenCrust, SeedRenewal,
HotGoo (`ExplosiveGoo`).

Hooks the batches found, not made here (each would make a ported item do more; none is needed for what is in):
- Detect Hidden revealing items (ServUO DetectHidden.cs:16-23, :106-131, :174-183): the goblin floor trap's reveal.
- Repair.cs (ServUO :233-238) for the broken automaton head, the Veterinarian (ServUO :47-61) and transfer (BaseAI :2122)
  for the automaton.
- The craft registrations ServUO has for these items: HouseCraftables (DefMasonry :228-325, DefCarpentry :244-249,
  DefTinkering :476-532, the doors need a create hook at pinned CraftItem.cs:1449/:1743), SnakeCharmerFlute (DefCarpentry
  :608-610), ScaleCollar (DefTinkering :455-456), AbyssalCloth (DefTailoring :214), WoodPulp (DefCooking :234),
  WorkableGlass and SoulstoneFragment (DefGlassblowing :137, :144), BlankScroll from WoodPulp (DefInscription :436),
  KotlBlackRod and DrSpectorsLenses (need the moonstone), WallSafe. KotlAutomatonHead (recipe 458) needs the Stasis
  Chamber Power Core.
- Sources: AntLion's unknown skeletons (ServUO AntLion.cs:78-86), the ship's strongbox from SOS chests (Fishing.cs:473),
  DemonKnight's Blood of the Dark Father (DemonKnight.cs:116-136), the dragon's-blood carve (BaseCreature :2322-2334,
  :3893), the goblin talisman's slayer (pinned TalismanSlayerName has no Goblin), the mana phasing orb's five readers
  (Spell, SpecialMove, WeaponAbility, CraftItem, AOS), veteran rewards (metallic dye tub, greater bracelet, seed box,
  Coral), the begging pole, the docks' small fish, the treasure chest imbuing ingredients (abyssal cloth, essence of
  persistence). ServUO's quests that hand out the reward containers (listed in each container's header) are ServUO's
  own quest system, not ported.
- World placement, for Chase if wanted (none placed by code): the Underworld switches (ServUO Underworld.cfg:98-104,
  :157-173), Citadel and Tokuno sliding doors (Citadel.cfg:136-165, Tokuno Misc.cfg:1-10), the strange contraption
  (5668,1925,0 Trammel and Felucca), the automaton statues (Spawns/TreasuresOfKotl.xml) and the serpent nests
  (Spawns/termur.xml, near 795,771).

Port list numbers for the overseer (agents do not edit `docs\`): Base items row **172 -> 250 of 298**; all Port systems
**556 / 983 (56.6%)**; the 2026-10-13 list's "106 / 220" for this row is stale (counted, not edited).

## 6. Client check

Scripted (`clientcheck.py` in my scratchpad: tiledata names, the art and gump UOP indexes by their hashed entry names),
against `D:\ShatteredLegacy\client-data\classic-client` (7.0.117). Present, every one: the kits' 41875 (0xA393) and
the slider gumps 0x9CED-0x9D35, the circuit gump's 0x28C8-0x28D4, 0x9A8, 0x868, 0x25F8, 0x13F9, 0x13FD, 0x13A8 and
buttons 10700-10731; the containers' 0x9AA, 0xE7D, 0x4025/6, 0xE80, 0x9A8, 0xECA-0xED2, 0xE75/6 and gumps 0x42, 0x9,
0x3C, 0x4B, 0x3D; the resources' and tools' 0x1767, 0x1765, 0x136C, 0x1EA7, 0x9D7F, 0x571C, 0xA3E8, 0x5726, 0xA3E9, 0xA414,
0xA1CE-0xA1D9, 0x2DB5, 0xDD6/7, 0x4007, 0x103D, 0x4B80, 0xDC0, 0x410A, 0xFAB, 0x12B3, 0x9A96, 0xF04, 0x2F58, 0x1096;
storage 0x4910/1, 0x1086, 0xFBF/0xFC0, 0x9F1C/D, 19288-19291, 0xDCF, 4023 and about forty gumps; functional 0x9A97/8,
0xCF1, 0x1091/2, 0x3660, 0x4004, 0x4140, 0x108B, 0x9A9B, 0x2805, 0x2A05-0x2A1C; addons 0x9CE9, 0x9CAA, 0x9DB1-4, 0x2233,
0x41BF, 0x9F74, 0x4513/4, 0x14F0, the house pieces 463-491, 1928-1948, 1305-1313, 2967-2978, 42171-42190. The automaton's
body 1406 is not covered by the tool (unverified). The Collector's tile, Trammel 4305,1003, is open grass at Z 0
(vseUOAware). **Blocked on client data: nothing.**

## 7. For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these. Then, as Administrator on the test shard,
run `[ClusterFPlaceCollectorOfOddities dryrun` and, if it says it would place him, `[ClusterFPlaceCollectorOfOddities`.

1. **Trap training kits:** a character with Remove Trap, Lockpicking and Detect Hidden all 0; `[add
   CircuitTrapTrainingKit`, `[add CylinderTrapTrainingKit`, `[add SliderTrapTrainingKit`. Use Remove Trap: it gives a
   target (no "You do not know enough about locks"). On the circuit, walk the lit path with the arrows to the last
   square ("You successfully disarm the trap!"); a wrong step says you fail and reset it. On the cylinder kit, a wrong
   guess shows the status gump and does not hurt; the right five disarm it. On the slider, put the picture together.
2. **The Collector of Oddities:** `[go 4305 1003 0` in Trammel (Moonglow): he stands there after the command above; say
   "vendor buy": the three kits at 99,375 gold each.
3. **Chicken coop:** Carpentry 100 and 150 boards: Carpentry menu, Other, chicken coop; lock it down in your house and
   stable a tamed chicken through its context menu, then claim it back.
4. **Kotl automaton:** Tinkering 100, `[add BlackrockAutomatonHead`, double-click it in the pack: three seconds later a
   bonded Blackrock automaton follows you; let it die: a broken automaton head is in your pack.
5. **House items:** in your house, `[add JewelryBox`, `[add SeedBox`, `[add CoralTheOwl`, `[add Grinder`, lock each down;
   the jewelry box takes only jewelry and filters by kind, the seed box keeps seeds in slots by kind and colour, Coral
   answers "news", the grinder turns coffee pods into grounds.
6. **Small items by eye:** `[add Skeletonkey`, `[add MasterSkeletonKey`, `[add MetallicDyeTub`, `[add PenOfWisdom`, `[add
   ChestOfSending`, `[add GreaterBraceletOfBinding`, `[add ForgedMetalOfArtifacts`, `[add SnakeCharmerFlute`, `[add
   ScaleCollar`, `[add ManaPhasingOrb`, `[add AbyssalCloth`, `[add Blackrock`, `[add PolishedMeteorite`: each with its own
   art, name and tooltip.
7. **Test world boot:** done by CC on a scratch copy (section 3).

Decisions worth your word (none blocks this prompt): the peerless altars as their own prompt; the wall safe (an
account gold balance, or bank gold); whether ServUO's craftsman satchel and reward box fills should replace pinned's;
the pen of wisdom's never-deleted quirk; and which of the craft registrations and loot hooks in section 5 to do next.

## Play-test items added

Through the For Chase list above; Who and steps in `testing/bot-triage.md` (P199 group) and
`testing/playtest-steps.json`: P199-1 BOT-PARTIAL (trap kits), P199-2 EYES (the Collector), P199-3 BOT-PARTIAL (chicken
coop), P199-4 BOT (automaton), P199-5 EYES (house items), P199-6 EYES (small items), P199-7 CC (test world boot).

## Repo size rule

No new file over 5 MB: the largest is `HouseCraftables.cs` at about 30 KB. Scratch (the type lists, the client
checker, the break lists and pristine copies, the build and boot logs, the boot world) is in the session scratchpad,
outside both repos. `tools/progress.py` was run (README block, dashboard, progress.json, expansion-coverage.json are its
output; README and dashboard carry the generator's own non-ASCII characters, as before this prompt).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-20, after the notes
were otherwise complete. Neither repo BLOCKED. Code: 103 files pending (CHANGELOG.md, VERSION, apply-patches.sh, the 7
changed customizations and 2 changed tests, the 82 new customizations files, 3 new patches and 6
new test files); docs: 7. No file over 5 MB in either repo; every touched hand-written file is ASCII. The docker-build
and test-shard locks were taken and released; no package or Haven lock was needed; nothing was placed in any world and
no live config changed.

```
=== code  (D:\ShatteredLegacy) ===
  103 file(s) pending:
    CHANGELOG.md
    VERSION
    docker/uo/apply-patches.sh
    ... (the files listed in section 1)
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  7 file(s) pending:
    README.md
    dashboard.html
    testing/bot-triage.md
    testing/playtest-steps.json
    tools/expansion-coverage.json
    tools/progress.json
    notes/cc-P199-port-base-items-remainder.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

P199 DONE
