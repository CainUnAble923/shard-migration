# cc-P42: defect batch 3

2026-10-03. Brief: `D:\UO\cc-prompts\cc-P42-defect-batch-3.md`. Engine upstream `d4531cd94`; every pinned citation is
`D:\UO\ModernUO-pinned` at that commit. Builds only through `docker\uo\build.sh -t sl-modernuo:cc-p42` (red tree:
`-t sl-modernuo:cc-p42-red`). `sl-modernuo:latest` not moved (`45b7523ae54b` before and after). Nothing deployed, no shard
touched, nothing placed in any world, nothing committed. Git only with `--no-optional-locks`. Scratch:
`D:\UO\cc-p42-work\` (logs, scripts, the red tree).

## Headlines

1. **All eleven parts done; everything green.** Final build: **39/39 patches** (36 + 3 new), **491/491 shard facts**
   (451 at cc-P38 + 40 new or changed), image `sl-modernuo:cc-p42` **`a4525e03b317`** (build 6, the final tree). Upstream suites: **Server.Tests 893 passed, 0 failed; UOContent.Tests
   1,096 passed, 0 failed** (cc-P38: 1,095 and 1 failed). Shard console suite **87/87** (84 + 3).
2. **Red proof:** one build of a copy of the tree with every fix undone (`D:\UO\cc-p42-work\red\make-red.py`):
   **31 of 491 facts fail**, spread across Parts A, B, D, F, G1, G2, H, I, J and K. Part C proved red inside the
   builder (our importer patch reversed: upstream's patched test fails). Part E proved red in PowerShell (old check put
   back: 2 facts fail). One Part F fact needed its own red run (below). The 3 new patches each refuse a mutated context
   line at `--fuzz=0`.
3. **Two scope notes.** `docker\uo\apply-patches.sh` is outside the brief's file list, but a new patch must be named
   there or the build fails ("present but never applied"); I added three `apply_patch` lines, each with its comment, and
   updated the fixture patch's comment that called itself "the ONLY patch ... that touches an upstream TEST project".
   No other file outside scope changed.
4. **Brief corrections (counted, not taken on trust):**
   - Part D: `0x0001` is not a serial. It is the **item id** `BaseAddon` uses (pinned `Items/Addons/BaseAddon.cs:27`,
     `base(1)`), printed by `0x{item.ItemID:X4}`. The line named the *old office addon the replace would delete*, which
     still exists during a dry run. Fixed on that basis.
   - Part H: pinned `SmallBOD.EndCombine` (`Engines/Bulk Orders/SmallBOD.cs:117-169`) checks **no** "crafted" or "not
     already part of a deed"; neither does ServUO pub57 (`Scripts/Services/BulkOrders/SmallBODs/SmallBOD.cs:310-381`).
     I mirrored pinned exactly; see Part H.
   - Part G2 line numbers: `ComputeGuildReward` was at `ClusterFSmithBODSystem.cs:324-352` and `SealDivisor` at `:280`
     (comment block `:259-278`), not `:326-350`, `:303`, `:282-301`. Same code.
   - The 43 Despise spawners, 2 listed stock spawners in the Old Haven box, 40 stock spawners in that box, 491 facts:
     counted (lists below).
5. **Found, not fixed (out of scope), chip raised:** post-Valorite Smith deeds (Platinum..Celestial) check **no
   material**. Pinned's material checks cover `DullCopper..Valorite` and `Spined..Barbed` only (`SmallBOD.cs:142-150`,
   `LargeBOD.cs:120-129`) and `SmallBOD.GetMaterial` (`SmallBOD.cs:98-115`) maps no post-Valorite resource, while our
   `BulkMaterialType` appends Platinum=12..Celestial=19 (`server\patches\BulkMaterialType.cs`). So an iron item fills a
   Celestial small deed, which then pays thousands of Seals. Part H's item fill mirrors the same checks and so shares
   the gap. A reward exploit; the chip "Fix post-Valorite BOD material check gap" has the details.
6. **Numbering:** no clash. `notes\` had no P42 file before this; P43 notes exist and P43 passed (P39 step 7 checks file).

## Before I started

`D:\ShatteredLegacy` HEAD `a7c5d3b`, `status --short` empty. No commit by Chase's script during the task (HEAD still
`a7c5d3b` at the end). Read: `p32-decisions-2026-10-02.md`, `p31-checks-2026-10-02.md`, `cc-P37-upgrade-prep.md` s7,
`cc-P38-engine-upgrade.md` s13, `artificer-materials-decision-2026-10-02.md`, `pt07-pt11-decisions-2026-10-02.md`.

---

## Part A: Self Repair through imbuing

**Facts.** The gump gates every property by its discovery threshold, which comes from its gold base
(`ArtificersImbueGump.cs` `ComputeThreshold`: under 500 -> 3, under 1,500 -> 5, under 3,000 -> 8, else 10), and maps
threshold to standing in `ArtificersGuildmasterGump.GetMinStanding` (`ArtificersGuildmasterGump.cs:270-276`: 10 ->
15,000, 8 -> 5,000, 5 -> 1,000). Self Repair was 5 shards / 2,000 gold, so threshold 8: **Artificer (5,000)**. Prices
scale with target value and rank: `ShardsFor`/`GoldFor` = base x (target / rank max) x (1 + (cap% - 100) / 100).

**Rank ladder** (`ArtificersGuildmasterGump.cs:252-259`): Apprentice 0, Journeyman 1,000, Artificer 5,000, **Master
Artificer 15,000**, Arcane Artisan 40,000. **Recommendation: Master Artificer.** The price already scales up at Arcane
(x2.0 vs x1.75), Master is where every other top-tier property (SSI, DI, HCI, DCI, LRC, slayers) unlocks, and Arcane
Artisan at 40,000 is the top of the ladder, which would make Self Repair close to unobtainable. If Chase wants Arcane
Artisan it is one constant (`ImbueCatalogue.SelfRepairMinStanding`, `ArtificersImbueGump.cs:126`).

**Change.** `ImbuePropertyDef` gains `MinStandingOverride` / `RequiredStanding` / `RequiredRankName`
(`ArtificersImbueGump.cs:47-59`); the three rank checks (view row, select stage, apply) use them. Self Repair weapon and
armor (`:298-301`, `:329-332`): **40 shards, 40,000 gold base, Master Artificer**, constants at `:124-126`.

**Proposed numbers, with the current most expensive properties** (computed by the gump's own formula;
`D:\UO\cc-p42-work\imbue_prices.py`; the 6 at Master is the fact's own reading):

| Property, value | Master (15,000) shards / gold | Arcane (40,000) shards / gold |
|---|---|---|
| **Self Repair, new**, 1 / 2 / 5 / 6 (Arcane: 7) | 11 / 11,666; 23 / 23,333; 58 / 58,333; **70 / 70,000** | 11 / 11,428; 22 / 22,857; 57 / 57,142; 68 / 68,571; **80 / 80,000** |
| Self Repair, old, top value | 8 / 3,500 | 10 / 4,000 |
| Lower Reagent Cost 100 | 17 / 7,000 | 20 / 8,000 |
| Swing Speed / Damage / Hit Chance / Defense Chance at max | 14 / 6,125 | 16 / 7,000 |
| Any slayer (flat) | 15 / 6,000 | 15 / 6,000 |

At its top value Self Repair costs about 4 to 5 times the shards and 10 times the gold of any other property. One
exception for Chase to weigh: Self Repair **1** (10% chance per tick) costs 11 shards, fewer than a slayer's 15 or LRC's
17, though its gold is still above every other property's. A floor price would close that; I did not add one unasked.
Side effects, all keyed to `ShardBase`: extracting Self Repair from an item yields 10 shards plus the essence (was 1),
fully disenchanting one yields 20 (was 2), and crafting an essence costs 80 shards and 20,000 gold. No loop: buying it
always costs more than the item gives back.

**Materials move.** OSI's imbuing does not offer Self Repair at all and **strips it** when an item is imbued (ServUO
pub57 `Scripts/Services/LootGeneration/Imbuing/Core/Imbuing.cs:512-528`, in `ImbueItem` at `:415`). So there is no OSI
price to map onto. The price is kept as one number of the imbuing resource (`ShardBase`) plus gold, the same shape as
every other property. At the materials move it maps cleanly: the property's `ShardBase` becomes a count of the top tier,
**Relic Fragments** (OSI gives those for the strongest intensities: `Imbuing.cs:770-795`). The gold and the rank gate
carry over unchanged.

**Facts** (`server\tests\Misc\ImbueSelfRepairGateVerification.cs`), all through the table's own buttons:
1. At 14,999 the row reads `[req: Master Artificer]`, and Apply (sent anyway, as a client could) refuses on weapon and
   armor: no property, no shards, no gold taken.
2. At 15,000, Self Repair 6 costs **70 shards and 70,000 gold** (was 8 / 3,500).
3. Every other property keeps its base price and threshold tier; Swing Speed 78 at Master still costs 14 / 6,125.

Red: all 3 fail with the old price and tier (fact 3 because Self Repair is then no longer the dearest).

**Deviation text (register):** "Imbuing offers Self Repair (weapons and armor, 5 to 7 by rank) at Master Artificer
(15,000 standing) and above, priced well above every other property (40 Essence Shards and 40,000 gold at the vanilla
maximum, scaling with value and rank). OSI's imbuing never adds Self Repair and removes it from any item it imbues.
Ours, with F-27 (Self Repair 1 in 500 from high-end loot only), is the deliberate, expensive way to get it."

## Part B: `[ClusterFOldHavenCleanup` and New Haven's spawners

**Facts.** The box is X 3520-3760, Y 2420-2760 (`ClusterFOldHavenCleanup.cs:112-114`). New Haven's west half ends at
X 3545 (`ClusterFNewHavenServicesSeeder.cs`, P21), but our own New Haven placements reach X 3559 (the Necromancers
Guild Hall NPCs at 3547-3555, `ClusterFNewHavenSeeder.cs:64-65`), and `ClusterFAreaScan.cs:25` defines New Haven to
X 3570. So no box edge separates the two towns, and I did not move it.

**Every stock Trammel spawner in the box, post-uoml/** and shared/** (counted from the files by the fact and by
`D:\UO\cc-p42-work\oldhaven_scan.py`): 40.** 27 in `post-uoml/trammel/Outdoors.json` (undead and spellbinders,
skeletons, zombies, sheep, 13 pumpkin patches, 4 mixed wildlife, 2 brigand camps, **a Healer at 3618,2614,0**), 10 in
`post-uoml/trammel/Vendors.json` (EvilWanderingHealer 3554,2457; Noble x2; **BlacksmithGuildmaster 3526,2536,20**;
AnimalTrainer; Fisherman; IronWorker and Miner on the guildmaster's tile at z 21 and 22; Dryad; BaseEscortable), 1 in
`shared/trammel/Reagents.json` (3538,2536), 2 in `shared/trammel/TownsPeople.json` (TownCrier 3652,2619; escort
3645,2661). The full list with entries is in `D:\UO\cc-p42-work\oldhaven_scan.txt` and in the fact's output.

**Of those, the ones a type on the cleanup's list spawns: exactly 2.** The New Haven Blacksmith Guildmaster
(Vendors.json, 3526,2536,20) and **the ruins' Healer** (Outdoors.json, 3618,2614,0). The second one is new: it sits 1
tile from the cleanup's own NPC target `("Healer", 3617, 2614)`, so a real run took the stock spawner **and** its Healer.
Our spawners in the box (`ClusterFOldHavenSeeder`: OldHavenMage, DrelgorTheImpaler) are on no list.

**Fix: stop matching by place, start matching by what upstream ships.** New `ClusterFStockSpawnData.cs` reads the
shipped spawn files (`Core.BaseDirectory/Data/Spawns`, post-uoml/** and shared/** only, never uoml/**). A world spawner
is stock when it has a stock guid (the importer keeps the data's guid: pinned `BaseSpawner.Dto.cs:25`) or, for one
placed before guids were kept, the same x,y,z and entry names. The cleanup now:
- leaves any stock spawner alone and says so (`[STOCK, KEPT] ...`) (`ClusterFOldHavenCleanup.cs:245-250`);
- leaves alone any NPC whose `Spawner` is a stock spawner (`:191`);
- refuses to run if it reads no stock data (it cannot tell the towns apart without it) (`:160-167`);
- returns its lines from `Run(bool dryRun)` (`:150`), so the dry run and the real run are the same code;
- deletes **after** each scan, not inside it. Before, `spawner.Delete()` and `m.Delete()` ran inside a `foreach` over
  `World.Items.Values` / `World.Mobiles.Values`, which removes from the collection being enumerated. Not in the brief;
  it is on every real run, so fixed while there.

**Facts** (`server\tests\Misc\OldHavenCleanupVerification.cs`):
1. 40 stock spawners in the box; the 2 above are the only ones with a listed type.
2. With both stock spawners, a same-tile copy of the guildmaster's with a new guid, and the stock Healer's NPC on its
   target tile, beside a stray guildmaster spawner (3596,2595), a stray Healer spawner (3640,2600) and a stray
   guildmaster NPC (3645,2615): the dry run deletes nothing and names exactly the strays. The real run keeps all stock
   and deletes all strays, and the dry run's counts and kept-lines equal the real run's (`Would delete 1 NPCs, 2
   spawners ... Stock spawners left alone: 3`).

Red: fact 2 fails with stock matching off. Still declared `Shard = Unverified` (red in the console) until Chase has
run it once; flipping it to `TestFirst` is his call.

## Part C: upstream's importer test

`server\patches\ImportCleanupTests-guid-key.patch`, one hunk group on
`Projects/UOContent.Tests/Tests/Engines/Spawners/Json/ImportCleanupTests.cs:138-196`. The test now also places a
spawner with the file's own guid on the tile, and asserts: the other-guid spawner is **kept** (`Assert.False
(existing.Deleted)`, still in the dictionary), the same-guid one is **deleted and replaced**. Argued as S8's fixture
patch was: it changes no shipped code, it turns the gate's "0 failed" back into a real check, and a later upstream change
to the importer stops the build here. The alternatives (record a known failure; drop PT-07) are cc-P38 s13.1's, and
Chase chose this one.

- Gate: **UOContent.Tests 1,096 passed, 91 skipped, 0 failed; Server.Tests 893 passed, 17 skipped, 0 failed**
  (`D:\UO\cc-p42-work\suite-*.log`). Skips are the tile-data tests, as in P30 and P38.
- Red: in the green builder, `ImportSpawners-despise-exclusion.patch` and `ImportSpawners-guid-key.patch` reversed with
  `patch -R --fuzz=0`: `Import_DuplicateLocation_ReplacesExistingSpawner` **fails** (`Assert.False() Failure`), the other
  3 tests in the class pass (`red-C.log`).

## Part D: the registrar dry run's phantom line

**Cause** (correcting the brief, Headline 4): `ClusterFMineCampSeeder.ForeignItemsOn` listed every non-component item on
a layout tile, and during `replace dryrun` the old office addons it is about to delete are still there. A `BaseAddon` is
an item with id 1, so it printed `<Addon> 0x0001`. The real run deletes them first, so it never printed the line.

**Change:** `ForeignItemsOn` takes the same `removing` list `SeedAddons` already had for this case and skips those
addons (`ClusterFMineCampSeeder.cs:191-198`). Nothing else in what it reports changes.

**Fact** (`RegistrarOfficeVerification.cs` fact 8, `ReplaceDryRunDoesNotReportTheAddonsItRemoves`): on a cc-P19
office, the dry run's "left alone" lines name none of the addons it would delete, and still name a real item placed on
a layout tile (`Item 0x0EED`). Red: fails with the old check.

## Part E: the console's status-writer check

`Shard-Console.ps1`: `ConvertFrom-ContainerInspect` now keeps each mount's `Source` beside `Destination` (`:206-211`).
New `ConvertTo-HostPath` (`:984`) normalises `D:/x`, `/run/desktop/mnt/host/d/x`, `/host_mnt/d/x` and `/mnt/d/x` to
`D:\x`. New `Test-StatusWriterMount` (`:995`) counts a writer when the destination is the target or an ancestor of it and
the source, followed down to the target, is `Publisher.Folder`. The writer loop uses it (`:1031`), and the "written by"
line now says what it checks. As proposed in cc-P37 s7.3.

**Facts** (`scripts\tests\Shard-Console.Tests.ps1`, Windows PowerShell 5.1, **87/87**):
- (changed) only the test shard mounting the status folder still warns;
- (new) live mounting the parent (`.../lib/uo/modernuo:/var/lib/uo/modernuo`, as cc-P37 set it), with the test shard
  mounting `modernuo-test` at the same destination: writer is LIVE only, green, no warning;
- (new) the test shard's own parent alone: "written by : none";
- (new) a WSL-form source (`/run/desktop/mnt/host/d/...`) maps to the same folder.

Red: with the old exact-destination check put back, the two LIVE facts fail (85/87).

**Must land before the live deploy at the wipe** (cc-P37 s6). It changes only the console.

## Part F: the Bulk Order button chooses small or large; large gated by skill only

**Facts before.** The guild page's Bulk Order button only said "Please speak with the Guildmaster directly." away from
the NPC (`SmithGuildmasterGump.cs:291-296` before), and from the NPC it rolled small or large at random. Large needed
Journeyman (5,000) and 70.1 to request (`ClusterFSmithBODSystem.cs:52`, `:97`, `:148`) and Journeyman to turn in
(`CanTurnInLarge`). The book's "Request Small" called the random roll too, so it could hand out a large deed, and both
book buttons dropped the deed straight in the pack with no accept gump.

**Change.**
- `MeetsLargeSkill` (`ClusterFSmithBODSystem.cs:56`): 70.1 Blacksmithy (`Base`, as before) or an active Dev Testing
  Crystal. It is the only large gate now: request (`TryCreateLargeBOD`), the NPC's roll (`TryCreateBOD`), and turn-in
  (`CanTurnInLarge`, `:483`; refusal text now `"Large orders need 70.1 Blacksmithy. Any blacksmith will take this
  one."`). `LargeOrderStanding` is gone. Caps (3 small, 1 large) and their messages are unchanged.
- `TryCreateSmallBOD` (`:117`): small only, never a large roll. `TryCreateBOD` uses it for its small branch.
- `OfferBOD(pm, large)` (`:180`): the one entry point for a chosen order. It needs no NPC and shows pinned's own
  `SmallBODAcceptGump`/`LargeBODAcceptGump`, as the NPC path does (pinned `BaseVendor.cs:1393-1397`). OK puts the deed
  in the pack; cancel deletes it.
- New `SmithBulkOrderChoiceGump.cs`: Small always; Large only at 70.1, otherwise a grey line "Large bulk order: needs
  70.1 Blacksmithy (yours is N)". A Large reply sent anyway is checked again.
- Guild page: Bulk Orders opens the choice, with or without the NPC (`SmithGuildmasterGump.cs:294`). **Resolves D51.**
- Guild book: **I kept its two buttons and made them the same choice** (one entry point, `OfferBOD`; `SmithGuildBook.cs
  :329-337`, `:629-639`). Small is always small; Large shows only at 70.1, else the same reason line. Both now go through
  the accept gump. Fewer clicks than sending a second gump from the book.
- **The NPC's talk and context-menu path keeps its stock random roll** (default kept: it is the stock way). It now uses
  the skill-only gate, so at 70.1 with no rank it can roll large.

**Facts** (`SmithBulkOrderChoiceVerification.cs`, plus the rewritten PT-11 fact in `SmithBODPathsVerification.cs`):
1. At 70.0 (and 50,000 standing) the choice has no Large button and says why; a Large reply sent anyway makes no deed
   and says the skill message.
2. At 70.1 with **0 standing**, Large opens the large accept gump with no NPC anywhere; OK puts the deed in the pack.
3. Caps: a second large and a fourth small are refused with their messages.
4. Small from the choice is always small: 40 requests at 120 skill, each cancelled at the accept gump.
5. Guild page opened with no guildmaster: Bulk Orders, Small, OK gives a small deed, and no "speak with" message.
6. (`SmithBODPathsVerification` fact 2, rewritten from Journeyman to skill) a complete large deed pays a 70.0 member
   nothing at the guildmaster or the book and stays in the pack; at 70.1 with 0 standing it pays (117 Seals in the run).

Red: facts 2, 3, 5 and 6 fail in the red build. Fact 4 stayed green there, because the reverted Journeyman gate also
blocked the large roll, so I proved it alone: in the red builder with only the small-roll revert, it fails
(`red-F4.log`). Fact 1 is green on both sides on purpose: the 70.1 floor existed before; it guards the new gump.

**Deviation text (register):** "The Society of Smiths' Bulk Order button (on the guild page, anywhere) and the Smithing
Guild Book let the player choose a small or a large order; a large one needs 70.1 Blacksmithy and no rank. OSI's smiths
choose small or large at random (talking to the Blacksmith Guildmaster still does). Regular smiths are unchanged."

## Part G: orders that still teach, and rewards

### G1. The engine's gain condition, cited

Crafting rolls `from.CheckSkill(craftSkill.SkillToMake, minSkill, maxSkill)` for each of the item's craft skills inside
`CraftItem.GetSuccessChance(gainSkills: true)` (pinned `Engines/Craft/Core/CraftItem.cs:874-894`). `SkillCheck.
CheckLocation` (`Skills/SkillCheck.cs:56-74`) returns false with no gain when `value < minSkill`, and true with no gain
when `value >= maxSkill`. Only in between does it call `CheckSkill`, which can gain (`:108-158`). **So an item teaches
while min <= Blacksmithy < max**, using the item's own `CraftSkill` range. Material and exceptional quality do not enter
that roll. The engine counts them only in whether the smith can make the item at all (every required skill, success
chance, and for exceptional `GetExceptionalChance > 0`). So that is where they count here: the stock "can make" test of
`SmallSmithBOD.CreateRandomFor` (`SmallSmithBOD.cs:139-157`) is kept, and the material rolls stay stock. Our
`CraftItem-shard-hooks.patch` does not touch the gain path (it adds a Dev Testing Crystal bypass, `:875-881`, which
returns before the gain roll).

**Rule** (`ClusterFSmithTeaching.cs`): of what the smith can make, the items that teach; if none teaches, the hardest
(highest max, the ones closest to their skill). Small orders: stock flips a coin between the armor list (with materials)
and the weapon list. When only one list has a teaching item that list is used; when neither has, the list holding the
hardest makeable item. Large orders: a set (of the 8) where every piece teaches; if none, the makeable sets with the most
teaching pieces, then the highest lowest maximum. Commissions: the same, with the pool's 65/35 weapon/armor split kept
among teaching items. Amounts, material and exceptional rolls are stock throughout.

**Scope decision: the Society's orders only.** Guildmaster, choice gump, book and commissions. Regular NPC smiths are
the OSI path (PT-11: they keep OSI's orders and rewards), and pinned's `Blacksmith.CreateBulkOrder` makes a regular large
deed with `new LargeSmithBOD()` and no mobile (`Mobiles/Vendors/NPC/Blacksmith.cs:98`), so it cannot be filtered without
another pinned patch. To extend the rule to them: one line in the new small patch, plus a `Blacksmith.cs` patch for large.
Say if wanted.

**Where the code is.**
- Small: `server\patches\SmallSmithBOD-teaching-orders.patch` (new) adds `CreateRandomFor(Mobile m, bool teachingOnly)`
  with two calls into `ClusterFSmithTeaching`. The one-argument form regular smiths call is unchanged. Alternative
  considered: a copy of the 60-line generator in customizations. Rejected: it would drift from pinned silently, while the
  patch stops the build if upstream changes the method. The guild path calls it with `true` (`ClusterFSmithBODSystem.cs`
  `TryCreateSmallBOD`).
- Large: `server\patches\LargeSmithBOD.cs` (already our full replacement). The stock constructor's two rolls are passed
  in, `SetTypes(int)` names the 8 sets (`:85`), and `CreateRandomFor` picks the set after the exceptional roll (`:116`).
  The parameterless constructor (regular smiths) is unchanged in effect.
- Commissions: `SmithCommissionPool.TeachingKey` and `SmithCommissionSetPool.TeachingSet` (`ClusterFSmithCommissions.cs
  :195`, `:353`), called from `Generate` and `GenerateLarge` (`:495`, `:542`).

**Facts** (`SmithOrdersTeachVerification.cs`; 60 draws per row; the tallies from the green run, `facts-detailed.log`):

| Skill | Small guild orders | Large guild orders | Commissions (small / large) |
|---|---|---|---|
| 30 | ringmail, shields, maces, daggers, swords (18 kinds, all teach) | (none below 70.1) | Longsword, WarMace, ringmail / ringmail_set x60 |
| 70 (large 70.1) | 26 kinds across both lists, all teach | axes, polearms, swords | 25+ kinds / heavy_archer, light_archer, female_plate |
| 100 | plate only: helm, gloves, legs, chest, arms, gorget | plate x60 | plate and dragon pieces / full_plate 49, samurai 7, dragon 4 |
| 120 | **PlateChest x60** (75-125, the last BOD item that teaches) | plate x60 (fallback: chest only teaches) | plate chest, dragon, samurai / dragon_scale x60 |
| 130 | **PlateChest x60** (fallback: nothing teaches; hardest) | plate x60 (fallback) | kabuto, PlateDo, DragonChest / samurai_plate x60 |

Each fact asserts every draw teaches, or that nothing on offer teaches and the draw is the fallback the rule names.
Fact 4: the one-argument generator (regular smiths) still gives a 120 smith items that teach nothing (**194 of 200**).

For Chase: past 125 no **BOD** item teaches (PlateChest is the top), so a 130+ smith gets PlateChest small deeds and
plate large deeds as fallback. Commissions reach further (Tokuno kabuto 90-140, PlateDo 87-137), so they keep teaching to
about 140. Above that nothing in Blacksmithy teaches at all, whatever the order.

Red (G1 rule off): small at 70, 100, 120, 130; large at all four; commissions at 70 and 100 fail. Small at 30 and
commissions at 30, 120, 130 stayed green: at 30 almost every stock pick teaches anyway, and `TeachingKey` filters before
the mutated fallback. Each kind of order (small, large, small and large commission) has red coverage.

**Deviation text (register):** "The Society of Smiths' bulk orders and commissions ask only for items whose crafting can
still raise the smith's Blacksmithy (the item's skill range contains the smith's skill); past the top of every item they
ask for the hardest the smith can make. OSI's orders pick any item the smith can make. Regular smiths are unchanged."

### G2. Rewards

`ClusterFSmithBODSystem.cs:291-314`: Seals are the old divisor-400 count (floor 1) **times 3** (`SealMultiplier`), and
standing the old table **times 2** (`StandingMultiplier`). Still no gold. The order of worth is unchanged (every value is
an exact multiple), so exceptional and large still pay more. I multiplied after the floor, so the cheapest orders get the
x3 too (iron regular 10 pays 3, not 1). Dividing the gold by 133 would have left them at the floor of 1, against "across
the board".

**Before and after**, computed from the formulas and pinned's gold table (`Engines/Bulk Orders/Rewards.cs` `m_GoldTable`
and `ComputeGold`'s `gold * 9 / 10` to `gold * 10 / 9`; `D:\UO\cc-p42-work\g2_calc.py`). Ranges come from the gold
randomisation; the "seen" column is from 40 deeds each in the fact:

| Order | Gold equivalent | Seals before | Seals after | Seen in the fact | Standing before / after |
|---|---|---|---|---|---|
| Iron small regular, 10 | 135-166 | 1 | **3** | 3 | 25 / **50** |
| Iron small exceptional, 20 | 450-555 | 1 | **3** | 3 | 60 / **120** |
| Dull Copper small exceptional, 20 | 720-888 | 2 | 6 | (not a fact) | 75 / 150 |
| Valorite small regular, 20 | 3,600-4,444 | 9-11 | 27-33 | (not a fact) | 120 / 240 |
| Valorite small exceptional, 20 | 10,800-13,333 | 27-33 | **81-99** | 81-99 | 180 / **360** |
| Platinum small exceptional, 20 | 16,200-19,999 | 40-50 | 120-150 | (not a fact) | 195 / 390 |
| Celestial small exceptional, 20 | 54,000-66,665 | 135-167 | 405-501 | (not a fact) | 300 / 600 |
| Large Valorite exceptional plate, 20 | 180,000-222,222 | 450-556 | **1,350-1,668** | 1,350-1,647 | 310 / **620** |
| Large Platinum exceptional plate, 20 | 270,000-333,333 | 675-833 | 2,025-2,499 | (not a fact) | 330 / 660 |
| Large Celestial exceptional plate, 20 | 900,000-1,111,110 | 2,250-2,778 | **6,750-8,334** | 6,756-8,316 | 470 / **940** |

(The old comment block's "~4" for Dull Copper exceptional and "~10" for Valorite regular were estimates; computed, they
were 2 and 9-11. The block now carries the computed values.) Fact 5 asserts, for the five the brief named, standing =
2x old exactly and Seals a multiple of 3 inside 3x the old range. Red: all five fail at x1.

**Seal catalog, checked, not changed** (`SmithSealCatalogGump.cs:60-102`). With x3 income:
- Early game is fine: a Sturdy Pickaxe (50) is 17 iron orders (was 50).
- **The top end gets cheap. Flag for Chase.** A Valorite Runic Hammer (5,000) is now 3 to 4 large Valorite exceptional
  plate deeds (was about 10), or about 55 small Valorite exceptional ones. **One** large Celestial exceptional deed
  (6,750+) buys a Valorite runic outright. The Gold to Verite runics (1,200-3,000) fall to one large deed each. The
  "coming soon" post-Valorite runics (7,500-50,000) are 1 to 7 large Celestial deeds.
- With the Part G1 rule, a GM's guild orders are now mostly exceptional plate, which is also the best-paying kind. So
  income for a top smith rises by more than 3x in practice.
- And the post-Valorite material gap (Headline 5) lets a Celestial deed be filled with iron today, so it should be
  closed before or with this reward change.

**Deviation text:** none new (the Seal economy is ours already). Update the register's Smith Seals entry to "x3 Seals,
x2 standing (cc-P42)".

## Part H: large Smith deeds fill by item

**Facts.** `server\patches\LargeSmithBOD.cs` is our full replacement of pinned's `LargeSmithBOD.cs`, and `EndCombine` is
virtual (pinned `LargeBOD.cs:94`). So the change needs **no pinned patch**: `LargeSmithBOD.EndCombine` passes small deeds
to `base` (pinned's combine, unchanged) and anything else to `LargeBODItemFill.Fill` (`LargeSmithBOD.cs:139-153`).

**`LargeBODItemFill.cs` (new):** the item must be in the backpack (`1045158`, as `BODTarget.cs:18-22`). Then the same
checks, in the same order and words, as pinned's small deed (`SmallBOD.cs:117-169`): the item's type or a subclass on
one of the deed's entries, and an armor, clothing or weapon (`1045169`); that entry not full (`1045166`); the ore
(`1045168`) or leather (`1049352`) when the deed names one; exceptional when asked (`1045167`). One item adds 1 to its
entry; `1045170` and the deed's gump, and the cursor again until complete. Turn-in unchanged (`Complete` = every entry
full).

**Not added, because stock has neither (Headline 4):** a "crafted" or maker check, and "not already part of a deed" (an
item that fills an entry is deleted, so it cannot fill twice). Adding a crafted check to large deeds alone would make
them stricter than small ones. If Chase wants "crafted only" for both, it is a small follow-up on both paths.

**Contained items** (`BODCombineContained.cs:65`): for a `LargeSmithBOD`, every item in the bag is offered, small deeds
and items alike. A mixed bag fills every entry it can and says how many went in. Tailor large deeds still take small
deeds only.

**Tailor later:** the same override would carry to tailor deeds with one change, but `LargeTailorBOD` is pinned's own
file, so it needs a pinned patch (or a replacement like ours for smiths). `LargeBODItemFill` already has pinned's leather
and clothing branches. The large gump's combine button text is still pinned's (1045155-style "combine with another
deed"); it now also takes items. Changing the text would touch `BOD-combine-contained.patch`'s file; not done.

**Facts** (`LargeBODItemFillVerification.cs`, an exceptional Dull Copper large plate deed of 10):
1. The deed's own Combine button and cursor on an exceptional Dull Copper gorget: the gorget is gone, its entry reads 1,
   `1045170`, no other entry moves.
2. Refused, item kept, never stock's `1045159`: iron `1045168`; not exceptional `1045167`; a longsword `1045169`; full
   entry `1045166`; an item in the bank: the cursor is refused by the targeting layer first (`500237`, "Target can not be
   seen."), and the deed's own check called directly says `1045158`.
3. A completed small deed still combines (`1045165`) and is consumed.
4. "Combine this deed with contained items" on a bag of 3 gorgets, 2 legs, an iron gorget, a longsword and a completed
   helm deed: gorgets 3, legs 2, helm 10, iron and longsword stay, "6 items were combined with the deed."

Red: facts 1, 2 and 4 fail with stock's EndCombine; 3 is green on both (it pins the small-deed path).

**Deviation text (register):** "A large Smith bulk order deed takes the crafted items directly, each filling its entry
as a small deed of that entry would (type, ore, exceptional), as well as completed small deeds. OSI fills large deeds
only by combining completed small deeds."

## Part I: Wisp Orb possession and combat (D52)

**Cause, found before fixing.** Our possess path is a line-for-line port of ServUO's (`WispOrb.cs` InternalTarget vs
pub57 `Scripts/Items/Quest/WispOrb.cs:350-380`). It relies on `SetControlMaster` to end the fight. ServUO's does:
`RemoveAggressed`/`RemoveAggressor` both ways and both combatants cleared (pub57 `Scripts/Mobiles/Normal/BaseCreature.cs
:6664-6673`). Pinned's does none of it (`Mobiles/BaseCreature.cs:3748-3795`). So the player kept the creature as
`Combatant` and swung at it (the server sends the combatant; in war mode the client attacks it). The creature's
defensive AI picks as aggressor anyone near its anchor whose `Combatant` is the creature (`DespiseRevamped/AI.cs:388-415`,
`m.Combatant == creature`), which is its own master. Not a client-side attack: no client packet is involved once the
server clears the combatant (pinned `Mobile.Combatant`'s setter sends the change).

**Fix:** `WispOrb.EndFight` (`WispOrb.cs:528-545`), ServUO's six lines, called right after `SetControlMaster` (`:588`).
Pinned's `SetControlMaster` is not patched: taming has the same gap but nobody tames mid-fight, and a pinned patch for
that is a separate decision.

**Fact** (`WispOrbPossessionVerification.cs` fact 1): a player and a Silenii harm each other and have each other as
Combatant, then the player possesses it through the orb's own double-click and target. Afterwards the player's combatant
is not the creature, the creature's is null, no aggressor or aggressed entry joins them either way, and the creature's
AI does not pick the player. Red: fails without `EndFight`. Not a deviation: it restores ServUO's behaviour.

## Part J: stock creature spawners in Trammel Despise (D53)

**Counted:** only `shared/trammel/Despise.json` places stock spawners in the Despise dungeon area on Trammel (all of
post-uoml/**, shared/** and uoml/** scanned): **43**, of which **30 creature-only, 11 treasure-chest-only, 2 mixed**
(Lizardman + TreasureChestLevel2 + TreasureChestLevel3, at 5503,529,60 and 5386,612,45). Felucca's file has its own 43
with different guids.

**Fresh world: an exclusion we own, through the importer.** `server\patches\ImportSpawners-despise-exclusion.patch`
(new, 9 lines, after the guid-key patch) asks `ClusterFDespiseStockSpawns.Admit` about each spawner the JSON import
builds. A spawner of the Trammel file loses its creature entries and keeps its chests; one with nothing left is not
placed. Everything else, on every map, passes untouched. Which spawners are stock is read from the shipped file itself
(`ClusterFStockSpawnData`), not a list in our code. Argued:
- Editing or shadowing upstream's JSON: every data bump would need a re-merge, and a silent upstream change to the file
  would bring the creatures back. Rejected.
- A runbook step "run the cleanup after spawn generation": correct only if someone remembers it on every path. Rejected
  as the primary guard (it exists anyway, for existing worlds).
- The import hook covers every path that reads the file: `[GenerateSpawners` of the file, of `shared/**`
  (`docker/uo/COMMANDS.md:155`, `SERVER.md:355`), and the admin gump's world build (pinned `Gumps/AdminGump.cs:4060-4061`).
  Note: the console's fresh-world sequence (`Shard-Console.ps1` `WorldSetupOrder`, 12 named files) does not include
  `shared/trammel/Despise.json` at all. The test world got the stock spawners from a broader import.

**Existing world:** `[ClusterFDespiseStockCleanup [dryrun]` (`ClusterFDespiseStockSpawns.cs`), Administrator,
`ShardCommand(WorldSetup, Rerun = DeletesAgain, Shard = TestFirst, DryRun = "dryrun")`. Any argument other than
`dryrun` prints usage and does nothing, so a typo cannot delete (the Old Haven cleanup's P21 defect). Trammel only. It
deletes the creature-only stock spawners with what they spawned, strips the creature entries from the mixed ones (the
chests stay, `RemoveEntry` deletes the stripped entries' spawns: pinned `BaseSpawner.Entries.cs:93-110`), and keeps the
chest-only ones. It matches stock spawners by guid or by x,y,z and names. It never touches the revamp's 47 (not in the
file) or Felucca.

**Facts** (`DespiseStockSpawnsVerification.cs`):
1. The file: 43 = 30 + 11 + 2; Felucca 43.
2. A real `[GenerateSpawners` of the Trammel file places **13** spawners, every entry a chest (the 2 mixed with their 2
   chests each); the Felucca file places all 43, 32 with creatures.
3. On a world with the 43 stock Trammel spawners, the revamp's 47 and Felucca's 43: the dry run changes nothing and
   lists 30 deletions and 2 strips. The real run says `deleted 30 creature spawners, stripped the creatures from 2 mixed
   ones, kept 11 chest spawners`, leaves 13 chest-only spawners, the 47 and Felucca's 43 untouched. A second dry run
   finds nothing (`kept 13`).

Red: facts 2 and 3 fail with the hook admitting everything and the cleanup only reporting.

**Deviation text (register):** "Trammel Despise runs the revamp only: the pre-revamp creature spawners (ettins,
lizardmen, elementals, trolls, ogres, cyclopes) are not placed; its treasure chests stay. Felucca Despise is classic."
(Whether OSI's Trammel Despise kept any pre-revamp creatures: unverified here.)

## Part K: logout in Despise destroyed the Wisp Orb (D54)

**Checked in ServUO first.** pub57's `DespiseController.OnEnterRegion` (`Scripts/Services/Revamped Dungeons/
DespiseRevamped/DespiseController.cs:597-609`) excludes nothing, and `Region.OnRegionChange` (`Server/Region.cs:1128-
1163`) fires `OnEnterRegion` for the move to the internal map too. So ServUO, as written, also dissolves the orb on
logout, and its own `OnLogin` (`:563-595`) then has no orb to bring back. Our port did the same through
`DespiseRegion.OnExit` -> `OnLeaveDespise`.

**Fix** (`DespiseController.cs:647-663`): `OnLeaveDespise` returns at once when the owner is on `Map.Internal` (or no
map), as at logout (pinned `Mobile.Logout`, `Projects/Server/Mobiles/Mobile.cs:9056-9066`). The owner comes back at
`LogoutLocation`, inside the dungeon, so no exit fires. Walking or recalling out still dissolves the orb. This makes
`OnLogin`'s "back to your stronghold with your creature" and `DespiseCreature.CanAutoStable => false` reachable.

**Fact** (`WispOrbPossessionVerification.cs` fact 2): possess in Despise Good; internalize as `Mobile.Logout` does and
turn the timer wheel (`ShardTestClock`): the orb lives, `orb.Pet`, `creature.Orb` and `ControlMaster` all still linked.
Log back in at the logout location and run `OnLogin`: still linked. Walk to 1500,1500: the orb is deleted and the
creature freed. Red: the orb is gone after the logout step.

**Deviation text (register):** "A Wisp Orb survives its owner logging out inside Despise (the possessed creature stays
linked and returns with them); leaving the dungeon by foot or magic still dissolves it. ServUO's code dissolves it on
logout too, contradicting its own login handler."

---

## Gates

| Gate | Result |
|---|---|
| `build.sh -t sl-modernuo:cc-p42`, build 1 | compile error (missing `using Server.Gumps`) |
| build 2 | 1 test compile error (`Concat` typing) |
| build 3 (tests only) | 490/491: the bank-item refusal (fixed, Part H) |
| red build `-t sl-modernuo:cc-p42-red` | **31 of 491 fail**, listed in `build-red.log` |
| build 4 (full) | 39/39 patches, **491/491**, image built |
| facts alone (`facts-detailed.log`, first try) | 15 failed: `DefBlacksmithy.CraftSystem` is null when no earlier test built it; both Smith fact classes now build it as `CraftXVerification` does |
| build 5 (full) | 39/39, **491/491**, image `c3dff254ad31`; the new facts alone **53/53** |
| build 6 (full) | after replacing the em dash in one Old Haven message string with a colon (text only): 39/39, **491/491**, image `a4525e03b317` |
| upstream Server.Tests (builder cc-p42) | **893 passed, 17 skipped, 0 failed** |
| upstream UOContent.Tests, shard filtered out | **1,096 passed, 91 skipped, 0 failed** |
| Part C red | upstream test fails with our importer patch reversed |
| Part F fact 4 red, alone | fails with only the small-roll revert (`red-F4.log`) |
| new patches at `--fuzz=0` | 3 clean, 3 refused when one context line is mutated |
| shard console (PowerShell 5.1) | **87/87**; old check put back: 85/87 |

Build 6 (the final tree): **39/39 patches, 491/491 shard facts**, image `sl-modernuo:cc-p42` = **`a4525e03b317`**.
`sl-modernuo:latest` still `45b7523ae54b`. Shard HEAD still `a7c5d3b`.

## What Chase stages and commits (`D:\ShatteredLegacy`)

Modified: `docker/uo/apply-patches.sh`, `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`,
`server/customizations/` `ArtificersImbueGump.cs`, `BODCombineContained.cs`, `ClusterFMineCampSeeder.cs`,
`ClusterFOldHavenCleanup.cs`, `ClusterFSmithBODSystem.cs`, `ClusterFSmithCommissions.cs`, `Items/Quest/WispOrb.cs`,
`Services/Revamped Dungeons/DespiseRevamped/DespiseController.cs`, `SmithGuildBook.cs`, `SmithGuildmasterGump.cs`;
`server/patches/LargeSmithBOD.cs`; `server/tests/Misc/RegistrarOfficeVerification.cs`, `SmithBODPathsVerification.cs`.
New: `server/customizations/` `ClusterFDespiseStockSpawns.cs`, `ClusterFSmithTeaching.cs`, `ClusterFStockSpawnData.cs`,
`LargeBODItemFill.cs`, `SmithBulkOrderChoiceGump.cs`; `server/patches/` `ImportCleanupTests-guid-key.patch`,
`ImportSpawners-despise-exclusion.patch`, `SmallSmithBOD-teaching-orders.patch`; `server/tests/Misc/`
`ImbueSelfRepairGateVerification.cs`, `LargeBODItemFillVerification.cs`, `OldHavenCleanupVerification.cs`,
`SmithBulkOrderChoiceVerification.cs`, `SmithOrdersTeachVerification.cs`; `server/tests/Services/Revamped Dungeons/
DespiseRevamped/` `DespiseStockSpawnsVerification.cs`, `WispOrbPossessionVerification.cs`.

`docker/uo/apply-patches.sh` is not on the commit script's protected list that I know of, but check it is staged.

## For the overseer (`docs\`, which I did not edit)

- Deviation register: Parts A, F, G1, H, J, K texts above; Smith Seals entry x3/x2 (G2).
- `docs\feature-queue.md` / bug list: D51, D52, D53, D54 fixed in cc-P42; the post-Valorite material gap is new.
- AGENTS layout counts: 39 `.patch` files now (`tools/progress.py` recounts); two patches now touch an upstream test
  project.

## Checklist for Chase (test shard, after `sl-modernuo:cc-p42` is on it)

- [ ] **Imbue Self Repair**: an Artificer at 14,999 sees `[req: Master Artificer]` and cannot apply; at 15,000 Self
      Repair 6 on a weapon asks 70 shards and 70,000 gold. Confirm 40 / 40,000 / Master (or say Arcane Artisan, or a
      floor price for value 1).
- [ ] **Old Haven cleanup**: `[ClusterFOldHavenCleanup dryrun`. Expect `[STOCK, KEPT]` for 3526,2536,20
      (BlacksmithGuildmaster) and 3618,2614,0 (Healer), and no `[DRY RUN]` line for them or for anything New Haven's
      spawn data placed. Run it for real only if the dry run's list is what you want gone.
- [ ] **Registrar**: `[ClusterFSeedRegistrarOffice replace dryrun` prints no "already on its tiles, left alone: ...
      0x0001" line.
- [ ] **Console**: status panel "written by" line; now it should say TEST or none as before. After live gets the parent
      mount at the wipe, it should say LIVE.
- [ ] **Bulk Order choice**: guild page (from the guild directory, no NPC near) and from the guildmaster, at 69 and 71
      Blacksmithy with little standing. At 69 Large is greyed with the reason; at 71 Large gives the accept gump and OK
      puts the deed in the pack. Same in the guild book.
- [ ] **Teaching orders**: a GM asks for small orders: plate only (helm, gloves, legs, chest, arms, gorget). At 120,
      plate chests only.
- [ ] **Turn-in numbers**: an iron exceptional small of 20 pays 3 Seals and 120 standing (was 1 and 60). A large
      Valorite exceptional plate pays about 1,350-1,670 Seals. Then weigh the Seal catalog note in G2.
- [ ] **Large deed by items**: double-click a large deed, Combine, target a matching crafted item: it fills its line.
      Then "Combine this deed with contained items" on a bag of mixed pieces.
- [ ] **Despise**: `[ClusterFDespiseStockCleanup dryrun` (expect 30 deletions, 2 strips, 11 kept; the numbers can be
      lower if the world lost some), then the real run, then walk Trammel Despise: no ettins, lizardmen or elementals;
      chests still spawn; the revamp still there; Felucca Despise still classic.
- [ ] **Wisp Orb**: fight a Despise creature, possess it: you stop attacking it and it follows. Log out in Despise, log
      back in: orb in pack, creature with you. Walk out: the orb vanishes.
- [ ] Decide: commissions' Seal rewards were not changed (G2 named only bulk orders); x3 there too?
- [ ] Decide: extend G1 (teaching orders) to regular NPC smiths? Default: no (OSI path).
- [ ] Start the chip "Fix post-Valorite BOD material check gap" before or with the reward change.
- [ ] Scratch to delete when done: `D:\UO\cc-p42-work\` (logs, red tree), `sl-uo-builder:cc-p42-red` and
      `sl-uo-builder:cc-p42` (about 5 GB each), and `sl-modernuo:cc-p42` once it is retagged or replaced.
