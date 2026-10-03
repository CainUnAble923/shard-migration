# cc-P46: Smith orders 2

2026-10-03. Brief: `D:\UO\cc-prompts\cc-P46-smith-orders-2.md`. Engine upstream `d4531cd94`; every pinned citation is
`D:\UO\ModernUO-pinned` at that commit. Scratch: `D:\UO\cc-p46-work\`.

## Headlines

1. **All eight parts done; everything green.** Final build (build 4) through `docker\uo\build.sh -t
   sl-modernuo:cc-p46`: **41/41 patches** (39 + 2 new), **579/579 shard facts**, image `sl-modernuo:cc-p46` =
   **`8d7505c739f6`**. Upstream suites in that builder: **UOContent.Tests 1,096 passed, 91 skipped, 0 failed;
   Server.Tests 893 passed, 17 skipped, 0 failed** (the same as cc-P42). `sl-modernuo:latest` not moved
   (`a4525e03b317` before and after). Nothing deployed, no shard touched, nothing committed.
2. **Red proof:** one build of a copy of the final tree with every fix undone (`D:\UO\cc-p46-work\make-trees.py red`):
   **56 of 644 fail, every one a P46 fact**, covering A, B, C, D, E, G and H. Part F's red is order-dependent by nature
   and is proved with an order probe (below): red alone and when it runs before the craft facts, green after them;
   green all three ways in the final tree.
3. **Part F's cause is not what the brief said; corrected and fixed at the root.** Our own fixture patch
   (`UOContentFixture-npc-speeds.patch`) installs SkillCheck's handlers for every run but never configured
   `AntiMacroSystem`, which `SkillCheck.CheckLocation` reads. So any gain-range skill check in any fact threw unless a craft
   fact had run first, and this fact reached that line only when its random deed rolled a coloured ore (about 1 in 5).
   The fixture patch now configures AntiMacro too (one call, argued below), the shared helper the brief asked for
   exists (`ShardTestHost`), and the fact's deed is fixed to Dull Copper. Sweep: 17 fact classes each alone and all 145
   runs forward and reversed, green.
4. **Part H's cause found by a probe on the timer wheel, not guessed.** None of the brief's candidates. Our Despise AI
   is ServUO's line for line and writes `ControlOrder = OrderType.Attack`; ServUO's setter only clears the Combatant,
   pinned's issues the order, and `IssueAttack` sets `Combatant = ControlTarget`, which is still the **master** while
   following. That one harmful act made the master's Combatant the creature (pinned `Mobile.AggressiveAction`), so in
   war mode he swung at it. 64 of 64 probe cases showed it, all with the same stack. The karma loss is real too:
   pinned's `NoKillAwards` is not serialized; a reloaded creature the master had hit cost him 55 karma (and gave 5
   fame) when it died, in the red fact.
5. **Found by the way, fixed:** a test class whose static field read BOD data broke the whole collection (build 2:
   513 of 529 failed): xUnit calls `MemberData` methods while discovering, before the fixture has configured the server.
   My own fact; fixed (a property). Worth knowing for anyone writing a theory.
6. **Clash, not mine to resolve:** during this task another session committed `69830a7` (ShrunkPet, 2 files, 10:57) to
   `D:\ShatteredLegacy`, and there are uncommitted `docker\wiki\` changes that are not mine. No file overlaps with mine;
   its 5 facts pass in my build. The brief's "one builder at a time" was not held by that session.
7. **For Chase to weigh (not changed):** the runic ladder jumps x4.5 from Bronze (800) to Gold (3,600); large
   commissions pay far more standing than large deeds (a Valorite exceptional full plate commission 6,000 vs a large
   Valorite deed 620); at Master a Self Repair 1 imbue then disenchant still nets +2 shards for about 11,700 gold.

## Before I started

`D:\ShatteredLegacy` HEAD `d22a649`, `status --short` empty; `D:\UO\shard-migration` clean. P42 is committed (its files
are tracked). `notes\` has no P44 or P45 file, so this ran before them: no clash then. `sl-modernuo:latest` was
`a4525e03b317` (Chase retagged `cc-p42` as latest). Read: `cc-P42-defect-batch-3.md` (headline 5, Parts F, G1, G2, H),
`bod-choice-decision-2026-10-03.md`. HEAD at the end: `69830a7` (headline 6).

## Part A: argued before the patches were written

The material rule lives in pinned code on two of the three paths: small deed combine (`SmallBOD.EndCombine`,
`Engines/Bulk Orders/SmallBOD.cs:117-169`, with the map `SmallBOD.GetMaterial` at `:98-115`) and small into large
(`LargeBOD.EndCombine`, `LargeBOD.cs:94-152`). The third, item into large, is ours (`LargeBODItemFill.cs`). Options:

1. **Two small pinned patches (chosen).** `SmallBOD.cs`: the eight post-Valorite cases in `GetMaterial` and one
   `else if` for Platinum..Celestial beside pinned's DullCopper..Valorite branch, same message (1045168). `LargeBOD.cs`:
   the same `else if` beside its ore branch, same message (1045162). Our `LargeBODItemFill` gets the same branch. The
   rule then lives where pinned keeps it, and if upstream changes either method the patch stops the build at
   `--fuzz=0`.
2. Override `EndCombine` in `SmallSmithBOD` (through the existing `SmallSmithBOD-PostValorite.patch`) and in our
   `LargeSmithBOD.cs`, checking post-Valorite ore before calling base. Rejected: to keep pinned's message order (full,
   not in request, ore, exceptional) the overrides must copy pinned's checks, which then drift silently from pinned's.
   `docs/subsystem-policy.md`: a failing patch beats copied upstream logic.
3. Renumber `BulkMaterialType` so the post-Valorite ores fall inside pinned's DullCopper..Valorite range. Rejected:
   the values are serialized in every existing deed (`BaseBOD.cs:128`, `(BulkMaterialType)reader.ReadInt()`), and
   Spined..Barbed sit between.
4. Fix only our item fill. Rejected: leaves both pinned paths open.

Tailor deeds never carry a post-Valorite material, so the new branch is inert for them.

## Part F: argued before the fixture patch was changed

**The brief's premise, checked and corrected.** The brief (and my first reading) had the handler installed by whichever
fact ran first. It is installed for every run by our own fixture patch: `UOContentFixture-npc-speeds.patch` adds
`SkillCheck.Initialize()` to `TestServerInitializer` (in the build tree, `TestServerInitializer.cs:119-123`), with
`NameList`, `Corpse` and `BaseCreature` configuration, as "a Configure or Initialize the real server reaches ... and this
curated subset does not". It does not add `AntiMacroSystem.Configure()`, which `SkillCheck.CheckLocation` reads
(`SkillCheck.cs:72`). So in the test host every `Mobile.CheckSkill(skill, min, max)` whose value lies inside
`[min, max)` threw, unless `CraftXVerification` or `MakeXRepeatVerification` (`if (AntiMacroSystem.Settings == null)
AntiMacroSystem.Configure()`) had already run. The second condition was random: `ALargeDeedNeedsSeventyPointOneBlacksmithy`
turned in `new LargeSmithBOD()`, whose ore is rolled; an iron deed's range (0-55, `GetSkillRange`,
`ClusterFSmithBODSystem.cs:410`) is "no challenge" at 70.1 and never reaches line 72; a coloured one (about 1 in 5) does.
Hence build 6 green, Chase's rebuild red. (Found when the red image failed this fact alone, in both orders; proved by
reading the build tree's `TestServerInitializer.cs`.) The probe I ran first, "imbue class then SmithBODPaths" red and
reversed green, was that roll, not the order.

Options:
1. **Add `AntiMacroSystem.Configure()` to the fixture patch beside `SkillCheck.Initialize()` (chosen).** The defect is
   that patch configuring half of SkillCheck. It is the route's one place for "what the real server configures and the
   curated subset does not", it applies at `--fuzz=0`, it changes no shipped code (a test project), and it fixes every
   fact that reaches a gain-range skill check at once, present and future.
2. Only the per-fact helper the brief asked for (`ShardTestHost.EnsureSkillChecks`) in each fact that reaches
   `CheckSkill`. Kept as well, because the brief asks for it and it costs nothing, but alone it leaves the trap for the
   next fact that turns in a deed or crafts and forgets the call.
3. Configure AntiMacro from customizations at load. Rejected: changes the shipped server to suit the test host.

And the fact gets a fixed Dull Copper deed (40-72), so its skill check reaches line 72 every run and its red is not a
roll of the dice.

---

## Part A: post-Valorite deeds take only their own ore (D55)

**Where the ores are defined:** `CraftResource.Platinum..Celestial` in our `server\customizations\ResourceInfo.cs:20-27`
(a full replacement of pinned's, after Valorite); `BulkMaterialType.Platinum = 12 .. Celestial = 19` in
`server\patches\BulkMaterialType.cs:21-28`.

**Changed** (argued above, option 1):
- `server\patches\SmallBOD-post-valorite-material.patch` (new): `GetMaterial` maps the eight ores; `EndCombine` refuses
  another ore on a Platinum..Celestial deed with pinned's 1045168, beside pinned's own ore branch.
- `server\patches\LargeBOD-post-valorite-material.patch` (new): small into large, same `else if`, pinned's 1045162.
- `LargeBODItemFill.cs:70-77`: the item fill's ore check covers Platinum..Celestial (contained items go through it).
- `docker\uo\apply-patches.sh`: the two `apply_patch` lines with their comment.
- A fourth path exists and was already right: the Hammer of Hephaestus auto-fill compares post-Valorite ores by
  `CraftResource` (`HammerOfHephaestus.cs`, `MaterialMatches`). Mapping them in `GetMaterial` leaves it correct.

**Facts** (`server\tests\Misc\PostValoriteBODMaterialVerification.cs`, 48 = 16 ores x 3): for each ore DullCopper..
Celestial, (1) small deed by its own cursor: own ore fills (1045170), iron and the next ore down refused 1045168 and
kept; (2) small into large: own ore combines (1045165), iron and the next ore down refused 1045162; (3) item into large,
by cursor and by "combine with contained items": only the right ore fills. Red: the 24 post-Valorite cases fail ("a Iron
gorget filled a Obsidian large deed"); the 24 DullCopper..Valorite cases are green on both sides (pinned's rule
unchanged, as asked). Both new patches refuse a mutated context line at `--fuzz=0`.

Not changed, noted: the BOD book's material filter has no post-Valorite entries (pinned `BOBGump.cs:372-385`), so such
deeds show only under "all". Out of scope.

## Part B: "Orders that still teach me", per character (default on)

**Setting:** `CharacterGuildData.SmithTeachingOrders` (`ClusterFAccountData.cs`), the guild data keyed by character
serial that standing lives in. Version 0 -> **1**: the bool is written last; the reader accepts 0..1 (an unknown newer
version still fails loudly, D40) and a v0 record reads as on. `IsEmpty` counts it, so a character whose only guild data
is "off" is not dropped by the v15 migration's empty test.

**Off means** (`ClusterFSmithTeaching.cs`: `WantsTeaching` / `SetWantsTeaching`; the pickers take `teaching`):
- small: `SmallSmithBOD.CreateRandomFor(pm, teachingOnly: false)`, exactly stock's generator (which already keeps only
  items the smith can make);
- large: any of the 8 sets the smith can make every piece of; commissions: any item or set the smith can make, with the
  65/35 weapon/armor split kept. Stock's large roll checks nothing, so "can make" is my reading of the brief's "any item
  the smith can make", which is also what the gump line says. Say if large should be stock's blind roll instead.
- Every Society path reads it: guildmaster talk and context menu, the choice gump, the guild page, the guild book and
  commissions all go through `TryCreateSmallBOD`, `LargeSmithBOD.CreateRandomFor`, `TeachingKey`, `TeachingSet`.
  Regular smiths never read it.

**Where the player sees it:** a check box (client art 210/211) labelled "Orders that still teach me", with "Off: any
item you can make." under it, in `SmithBulkOrderChoiceGump` (50 px taller) and at the bottom of the guild book's order
page (`SmithGuildBook.cs`, button 8). Clicking flips it, says so, and redraws.

**Facts** (`SmithTeachingToggleVerification.cs`): (1) default on, for a new character and a hand-written v0 record;
(2) survives serialize and deserialize, off and on; (3) off through the choice gump's box, a GM's 60 small orders include
non-teaching items ("PlateArms x4, ShortSpear x4, ... Dagger x2"), large at 120 gives other sets ("Bardiche x11, Axe x10,
PlateArms x10, ..."), commissions too; on, all 60 teach ("PlateGloves x12, PlateArms x11, ..."); (4) the regular-smith
generator gives a 120 smith non-teaching items either way (196/200 on, 194/200 off); (5) both gumps show the one setting.
Red: 2, 3 and 5 fail; 1 and 4 are guards, green on both sides.

**Deviation D-109, new text:** "**Ours (cc-P42 G1, Chase 2026-10-03; toggle cc-P46 B).** The Society's bulk orders and
commissions ask only for items whose crafting can still raise the smith's Blacksmithy; past the top of every item they
ask for the hardest the smith can make. Players can turn it off per character (default on); off, they ask for any item
the smith can make. OSI picks any item the smith can make. Regular smiths unchanged"

## Part C: Self Repair imbue floor

`ArtificersImbueGump.cs`: `ImbuePropertyDef.PricedAboveAll`, set on both Self Repair entries. `ShardsFor` / `GoldFor` =
max(the old scaling, `ImbueCatalogue.MostShardsOfOthers(standing)` + 1 / `MostGoldOfOthers` + 1), the maximum computed
from the catalogue at the asking standing (every property without the flag, at its highest value for that standing).
Nothing hard-coded. Today the dearest other is **Lower Reagent Cost** in both shards and gold: 17 / 7,000 at Master,
20 / 8,000 at Arcane.

| Self Repair value | Master before (shards / gold) | Master after | Arcane before | Arcane after |
|---|---|---|---|---|
| 1 | 11 / 11,666 | **18** / 11,666 | 11 / 11,428 | **21** / 11,428 |
| 2 | 23 / 23,333 | 23 / 23,333 | 22 / 22,857 | 22 / 22,857 |
| 5 | 58 / 58,333 | 58 / 58,333 | 57 / 57,142 | 57 / 57,142 |
| 6 | 70 / 70,000 | 70 / 70,000 | 68 / 68,571 | 68 / 68,571 |
| 7 (Arcane only) | - | - | 80 / 80,000 | 80 / 80,000 |

Only value 1 moves; its gold was already above every other property's. (From the fact's own output.)

**Side effects** (all keyed to `ShardBase`, unchanged): extract 10 shards + the essence, full disenchant 20 shards per
property, essence crafting 80 shards + 20,000 gold; an imbue also gives `shards / 2` standing. Shards are the Artificers'
guild currency, earned only by imbue-side actions and work orders, never bought or sold for gold. Cycle "imbue Self
Repair 1, then disenchant": at Master -18 + 20 = **+2 shards** for 11,666 gold and the item (+9 standing); at Arcane
-21 + 20 = -1. Before the floor it was +9 at Master. Not a loop (gold and an item in, 2 shards out, and shards have no
gold outlet), and the floor narrows it; to close it, the floor could also be at least `ShardBase / 2 + 1` (21).

**Facts** (`ImbueSelfRepairGateVerification.cs` 4 and 5): at Master and Arcane every value 1..max costs more shards and
more gold than every other property's dearest value, and equals max(scaled, floor); the table's own buttons at the
lowest tier take the floored price. The 14,999 / 15,000 gate fact (1) and the 70 / 70,000 fact (2) unchanged and green.
Red: 4 (both ranks) and 5 fail ("Self Repair 1 at Master Artificer: 11 shards, Lower Reagent Cost 17").

## Part D: commissions x3 Seals, x2 standing

`ClusterFSmithCommissions.cs`: `ComputeBaseReward` is the old formula; `ComputeReward` (small) multiplies it by
`BlacksmithGuildmaster.SealMultiplier` (3) and `StandingMultiplier` (2), the bulk orders' own constants; a large
commission's totals are built from the base and multiplied after their floors (5 Seals, 50 standing). So every
commission pays exactly three times the Seals and twice the standing, and their order among themselves and against
bulk orders is unchanged. The representative-values comment carries computed numbers.

| Commission (`D:\UO\cc-p46-work\d_calc.py`) | Seals before | Seals after | Standing before | after |
|---|---|---|---|---|
| Small Iron regular | 1-2 | 3-6 | 40 | 80 |
| Small Iron exceptional | 2-3 | 6-9 | 80 | 160 |
| Small Dull Copper exceptional | 4 | 12 | 120 | 240 |
| Small Valorite regular | 11-13 | 33-39 | 250 | 500 |
| Small Valorite exceptional | 27-33 | 81-99 | 400 | 800 |
| Small Platinum exceptional | 40-50 | 120-150 | 440 | 880 |
| Small Celestial exceptional | 135-167 | 405-501 | 720 | 1,440 |
| Large Iron exceptional ringmail set (4) | 12-18 | 36-54 | 480 | 960 |
| Large Valorite exceptional full plate (5) | 202-247 | 606-741 | 3,000 | 6,000 |
| Large Celestial exceptional full plate (5) | 1,012-1,252 | 3,036-3,756 | 5,400 | 10,800 |
| Large Valorite exceptional dragon scale (x2.5) | 506-618 | 1,518-1,854 | 7,500 | 15,000 |

(The old comment's "~2, ~30, ~45, ~150" were close: computed 2-3, 27-33, 40-50, 135-167.) For Chase: large commission
standing was already about 10x a large deed's (3,000 vs 310 for Valorite); x2 keeps that ratio, 6,000 vs 620.

**Facts** (`SmithCommissionRewardsVerification.cs`): (1) five kinds x 40: Seals a multiple of 3 whose third is in the old
range, standing exactly 2x old (seen: Iron exc 6-9, Valorite exc 81-99, Platinum exc 123-150, Celestial exc 408-498);
(2) large at 30, 100, 130, 20 each: standing exactly 2x the old set formula, Seals a multiple of 3 ("samurai_plate
Valorite: 234 Seals, 3000 standing (was 78, 1500)"); (3) completing pays the entry's reward ("Exceptional Valorite Plate
Haidate: paid 87 Seals, 800 standing"). Red: 1 and 2 fail in every case; 3's multiple-of-3 check fails 2 times in 3 at
x1 (red in the final red build, green by chance in the first).

## Part E: runic hammer prices

`SmithSealCatalogGump.cs`: Gold 3,600, Agapite 5,400, Verite 9,000, Valorite 15,000; coming soon Platinum 22,500, Toxic
30,000, Blaze 39,000, Frost 51,000, Obsidian 66,000, Mythril 84,000, Adamantium 108,000, Celestial 150,000. Dull
Copper..Bronze (200, 350, 550, 800), tools and smithy hammers unchanged. `Rows(Cat)` (internal, read only) for the fact.

Orders needed per runic now (`e_calc.py`, best to worst case; Seals per order from cc-P42 G2's table and Part D's; with
Part A a post-Valorite deed now needs items of its own ore):

| Runic | Seals (was) | small Valorite exc BOD | large Valorite exc plate | large Celestial exc plate | small Valorite exc commission | large Valorite full plate commission | large Celestial full plate commission |
|---|---|---|---|---|---|---|---|
| Dull Copper | 200 | 3 | 1 | 1 | 3 | 1 | 1 |
| Shadow Iron | 350 | 4-5 | 1 | 1 | 4-5 | 1 | 1 |
| Copper | 550 | 6-7 | 1 | 1 | 6-7 | 1 | 1 |
| Bronze | 800 | 9-10 | 1 | 1 | 9-10 | 2 | 1 |
| Gold | 3,600 (1,200) | 37-45 | 3 | 1 | 37-45 | 5-6 | 1-2 |
| Agapite | 5,400 (1,800) | 55-67 | 4 | 1 | 55-67 | 8-9 | 2 |
| Verite | 9,000 (3,000) | 91-112 | 6-7 | 2 | 91-112 | 13-15 | 3 |
| Valorite | 15,000 (5,000) | 152-186 | 9-12 | 2-3 | 152-186 | 21-25 | 4-5 |
| Platinum | 22,500 (7,500) | 228-278 | 14-17 | 3-4 | 228-278 | 31-38 | 6-8 |
| Celestial | 150,000 (50,000) | 1,516-1,852 | 90-112 | 18-23 | 1,516-1,852 | 203-248 | 40-50 |

(Toxic..Adamantium are in `e_calc.py`'s output, all in order.) **The Bronze -> Gold step looks wrong:** x4.5 (800 ->
3,600) where every other adjacent step is x1.3 to x1.75; Bronze is about 10 small Valorite exceptional deeds, Gold
about 40. Not changed, as asked. Also: one large Celestial exceptional deed still buys any runic up to Agapite outright.

**Facts** (`SmithRunicPricesVerification.cs`): (1) the rows carry the new prices, the unchanged ones as they were, and
the ladder rises; (2) Gold..Valorite through the catalog's own buy button: price - 1 Seals buys nothing, the price buys
the hammer and leaves 0. Red: all 5 fail.

## Part F: order-dependent fact (D56)

Cause and the argument for the fixture-patch fix: "Part F: argued" above. **Changed:**
- `server\patches\UOContentFixture-npc-speeds.patch`: `Server.Misc.AntiMacroSystem.Configure();` after
  `SkillCheck.Initialize();`, with its comment line; hunk `+111,19` -> `+111,23`; applies at `--fuzz=0` to pinned's
  `TestServerInitializer.cs`. `apply-patches.sh`'s comment for it updated ("five shard calls").
- `server\tests\Route\ShardTestHost.cs` (new): `EnsureAccounts`, `EnsureSkillChecks`, `EnsureCraftSystems` (the last
  delegates to the existing `CleanUpCraftHost.EnsureCraftSystems`). Used by every P46 fact class and by
  `SmithBODPathsVerification`, `SmithOrdersTeachVerification`, `ImbueSelfRepairGateVerification`,
  `ImbueEssenceSourcesVerification`, `ImbueExtractDurabilityVerification` (the last two said in a comment that the host
  does not run `SkillCheck.Initialize`, false since S8; corrected).
- `SmithBODPathsVerification` fact 2: a fixed Dull Copper plate deed (40-72) instead of `new LargeSmithBOD()`.

**Proof** (scratch-only order probe `P46OrderProbe`: runs named classes' own facts by reflection, in a given order, in
one fresh process; xUnit 2.9.3 cannot order classes within one collection):

| Image | CraftX > SmithBODPaths | SmithBODPaths > CraftX (reversed) | SmithBODPaths alone |
|---|---|---|---|
| red (P42's fixture patch and fact setup) | 16 ran, 0 failed | **1 failed, NRE at SkillCheck.cs:72** | **1 failed, the same** |
| final | 16 ran, 0 failed | 16 ran, 0 failed | 2 ran, 0 failed |

That is Chase's failure on demand: in his log CraftX and MakeX ran after SmithBODPaths. **Sweep**, final image: 17
classes (the 10 new or changed in cc-P42, the 2 imbue facts that installed handlers, the 5 new here) **each alone: all
green**; all 17 together **forward 145/145, reversed 145/145**. `DefBlacksmithy.CraftSystem`: the P42 classes that need
it already build it (cc-P42 build 5); corpse handler, accounts' persistence and SkillCheck handlers come from the
fixture. Logs: `D:\UO\cc-p46-work\sweep-final\`.

**Also found, fixed in my own fact:** a static field reading BOD data, in a class with a `MemberData` theory, ran during
xUnit's discovery, before the fixture configured the server; the fixture's assembly load then failed and 513 of 529
facts failed (build 2). Now a property, with a comment saying why. Not fixed, noted: `ShameRevampedVerification`'s
`EnsureCorpses` comment says the fixture does not register the corpse handler; it has since S8. Harmless.

## Part G: Hammer of Hephaestus familiarity on default iron (D57)

**Cause, as the overseer read it, confirmed in a fact:** with the context's `LastResourceIndex` at -1, `CraftGump.cs:441-455`
passes `typeRes = null`, Craft X passes the same (`ClusterFCraftRun.cs:94-129`), the hook passed it on, and
`HammerMetal.InferResource(null)` is -1. Pinned itself reads a null type as the default: `BaseArmor.OnCraft`
(`BaseArmor.cs:545`, `typeRes ?? craftItem.Resources[0].ItemType`) and `CraftItem.ConsumeRes` (`:615-626`).

**Changed:** `HammerMetal.CraftedResource(typeRes, system, item)` (`HammerOfHephaestus.cs`) = `typeRes ?? (item.UseSubRes2
? CraftSubRes2 : CraftSubRes).ResType`; the hook's two `RecordFamiliarity` calls use it (`CraftItem-shard-hooks.patch`,
`+` lines only, counts unchanged, no hunk header moved). Both hammers, by hand and Craft X.

**Facts** (`server\tests\Engines\Craft\HammerFamiliarityVerification.cs`, a plate chest at an anvil and forge from a
fresh context): (1, 2) Hammer and Reinforced Hammer: one craft with no material picked -> Iron familiarity 1; (3) a Craft
X run of 3 -> 3; (4) picking Dull Copper counts Dull Copper, not Iron. Red: 1-3 fail (familiarity 0); 4 green both sides.

## Part H: the master attacked their possessed creature; karma on its death (D58)

**Found by a probe, before any fix** (scratch `D:\UO\cc-p46-work\probe\tree\server\tests\Probe\P46PossessedFightProbe.cs`):
8 good creatures x 2 foes x master karma 5,000 / 0 x war mode on / off, the AI on the timer wheel for 60 s, logging every
aggressive action touching the master with its stack. **64 of 64: the master's Combatant became the creature**, war
mode or not, before a blow landed, always by this stack: `DespiseMeleeAI.Obey` (`AI.cs:50`, `ControlOrder =
OrderType.Attack`) -> `BaseCreature.SetControlOrder` -> `BaseAI.IssueOrder` -> `IssueAttack` (`PetOrders.cs:201`,
`Combatant = ControlTarget`) -> the `Mobile.Combatant` setter -> `DoHarmful(master)` -> `master.AggressiveAction
(creature)` -> the master's Combatant set (`Mobile.cs:3877-3927`, when it has none). `ControlTarget` was the master
because Obey's follow branch sets it (`AI.cs:112`). **ServUO pub57 on the same path:** its `ControlOrder` setter calls
`OnCurrentOrderChanged`, which for Attack sets Warmode and clears the Combatant (`BaseAI.cs:1270-1277`), and nothing reads
`ControlTarget` there; so the port was right for ServUO and wrong under pinned. The brief's candidates (area attacks,
notoriety, the master's combatant following the pet's) were watched and never fired.

**Karma:** pinned's `NoKillAwards` is a plain property (`BaseCreature.cs:1315`), not in the generated save; confirmed by a
save and load in a fact (true before, false after). A creature loaded from a save pays kill awards (`BaseCreature.cs:
3546`) to anyone with looting rights, and a master who swung at it has them.

**Changed:**
- `AI.cs` (melee and mage, 8 sites): `ControlOrder = OrderType.Attack` -> `IssueOrder(OrderType.Attack, null, target)`
  with the creature's real target (its Combatant, the aggressor found near the anchor, or its focus): pinned's own API,
  which sets `ControlTarget` first. The header says why.
- `DespiseCreature.cs`: `CanBeHarmful` refuses the master and anyone in the master's party while possessed, so no
  attack, spell or area effect of its own can touch them and its Combatant cannot be set to them;
  `[AfterDeserialization]` re-asserts `NoKillAwards = true`.

**Facts** (`WispOrbPossessionVerification.cs` 3-6): (3) Silenii, Forest Nymph and Sagittarri, each vs Phantom and Naba, 30
s of AI with a party member beside the master: it engages the foe, never harms master or party, the master never targets
it, no aggressor entry joins them; (4) `CanBeHarmful` false for master and party, true for the foe, and setting its
Combatant to the master is refused; (5) after a save and load `NoKillAwards` is still true; (6) a reloaded creature the
master did most of the damage to, killed by a foe: the master's karma and fame unchanged. **Red:** all 9 fail: (3)
"Silenii -> master" harmful act, (5) false after load, (6) **karma 5,000 -> 4,945, fame 0 -> 5**. Not a deviation: it
restores ServUO's behaviour and the constructor's own intent.

---

## Gates

| Gate | Result |
|---|---|
| probe builds (scratch tree, `cc-p46-probe`) | Part H: 64/64 cases the master targets the creature; Part F order probe |
| build 1 (`cc-p46`) | 2 test compile errors (`using Server.Gumps`; CS0169 unused field) |
| build 2 | 513/529 failed: my static field ran before the fixture (Part F, "also found") |
| build 3 | 41/41 patches, 574/574, image `d60929a944e9` |
| red build 1 (`cc-p46-red`) | 55/639 fail; its Part F run exposed the real cause |
| **build 4, final** | **41/41, 579/579, image `8d7505c739f6`** (574 + 5 ShrunkPet facts from `69830a7`) |
| red build 2 | **56/644 fail**, all P46 facts; 39/39 patches (the 2 new ones removed) |
| green-probe build | 644/644 (579 + 64 probe cases + the order probe) |
| Part F order probe | red: reversed and alone fail with the NRE; final: green all ways |
| sweep, final image | 17 classes alone green; all 145 forward and reversed green |
| upstream UOContent.Tests / Server.Tests (`cc-p46` builder) | 1,096 passed, 91 skipped, 0 failed / 893, 17, 0 |
| new patches at `--fuzz=0` | 2 clean, each refuses a mutated context line; the fixture patch applies at `--fuzz=0` |
| ASCII | every added line and every new file ASCII only |

## What Chase stages and commits (`D:\ShatteredLegacy`)

Modified: `docker/uo/apply-patches.sh`; `server/customizations/` `ArtificersImbueGump.cs`, `ClusterFAccountData.cs`,
`ClusterFSmithBODSystem.cs`, `ClusterFSmithCommissions.cs`, `ClusterFSmithTeaching.cs`, `HammerOfHephaestus.cs`,
`LargeBODItemFill.cs`, `Mobiles/Normal/DespiseCreature.cs`, `Services/Revamped Dungeons/DespiseRevamped/AI.cs`,
`SmithBulkOrderChoiceGump.cs`, `SmithGuildBook.cs`, `SmithSealCatalogGump.cs`; `server/patches/`
`CraftItem-shard-hooks.patch`, `LargeSmithBOD.cs`, `UOContentFixture-npc-speeds.patch`; `server/tests/Misc/`
`ImbueEssenceSourcesVerification.cs`, `ImbueExtractDurabilityVerification.cs`, `ImbueSelfRepairGateVerification.cs`,
`SmithBODPathsVerification.cs`, `SmithOrdersTeachVerification.cs`; `server/tests/Services/Revamped Dungeons/
DespiseRevamped/WispOrbPossessionVerification.cs`.
New: `server/patches/SmallBOD-post-valorite-material.patch`, `LargeBOD-post-valorite-material.patch`;
`server/tests/Route/ShardTestHost.cs`; `server/tests/Engines/Craft/HammerFamiliarityVerification.cs`; `server/tests/Misc/`
`PostValoriteBODMaterialVerification.cs`, `SmithCommissionRewardsVerification.cs`, `SmithRunicPricesVerification.cs`,
`SmithTeachingToggleVerification.cs`.
**Not mine, do not stage with this:** `docker/wiki/content/pages/sidebar.txt`, `docker/wiki/content/pages/uo/start.txt`,
`docker/wiki/content/pages/uo/macros/`, `docker/wiki/macros/` (uncommitted, another session's).

`tools\progress.py` not run (it rewrites the README block, and this task commits nothing); run it with the commit.

## For the overseer (`docs\`, which I did not edit)

- D-109: new text in Part B. Smith Seals register entry: commissions x3 Seals / x2 standing too (cc-P46 D).
- Bug list: D55, D57, D58 fixed in cc-P46; D56 fixed with its cause corrected (the fixture patch configured SkillCheck
  without AntiMacro; test order and a random deed decided whether it bit). D58's karma half: `NoKillAwards` not saved.
- AGENTS layout counts: 41 `.patch` files (`tools/progress.py` recounts); the fixture patch adds five calls now.
- Worth a line in `test-host-truths`: a `MemberData` theory's class statics run at discovery, before the fixture.

## Checklist for Chase (test shard, after `sl-modernuo:cc-p46` is on it)

- [ ] **A Celestial (any post-Valorite) deed refuses iron**: Combine on a Celestial plate gorget deed, target an iron
      gorget: "The item is not made from the requested ore." A Celestial gorget fills it.
- [ ] **Teaching toggle**: a GM opens Bulk Orders (guild page): "Orders that still teach me" is checked. Uncheck it, ask
      for small orders: ringmail, weapons, helms appear (not only plate). Check it again: plate only.
- [ ] **Relog keeps the setting**: off, log out and in (and after a restart): still off.
- [ ] **The guild book shows the same setting**: the book's order page box matches the choice gump's; flip one, the
      other follows.
- [ ] **Self Repair 1 at Master** asks **18 shards** (a slayer is 15, Lower Reagent Cost 100 is 17) and 11,666 gold; 21
      shards at Arcane.
- [ ] **A commission pays about 3x**: a small Valorite exceptional commission promises 81-99 Seals and 800 standing (was
      27-33, 400) and pays what it promised.
- [ ] **Catalog**: Runic Hammers shows Gold 3,600, Agapite 5,400, Verite 9,000, Valorite 15,000; Post-Valorite 22,500 ..
      150,000; Dull Copper..Bronze still 200-800.
- [ ] **Hammer of Hephaestus**: after a fresh login, craft iron plate with the hammer without touching the material menu:
      the hammer's Metal Familiarity property goes up.
- [ ] **Possessed creature**: possess, lead it into a fight with opposing creatures, in war mode and out of it: you never
      swing at it, and a party member beside you is never hit by it.
- [ ] **Its death costs nothing**: after a restart (so it is a loaded creature), let it die to opposing creatures: your
      karma and fame do not change.
- [ ] Decide: the Bronze -> Gold runic jump (x4.5); large-commission standing (6,000 for Valorite full plate); Self
      Repair 1 disenchant +2 shards at Master; large orders "off" = can-make sets, or stock's blind roll.
- [ ] Scratch to delete when done: `D:\UO\cc-p46-work\` (trees, logs, probes); images `sl-uo-builder:cc-p46`,
      `sl-uo-builder:cc-p46-red`, `sl-uo-builder:cc-p46-probe` (about 5 GB each), and `sl-modernuo:cc-p46` once retagged
      or replaced. Docker reports 61 GB reclaimable in images overall; older `cc-p42*` and `cc-p38*` builders are among it.
