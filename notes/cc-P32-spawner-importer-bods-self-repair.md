# cc-P32: the spawner importer (PT-07), smith BOD paths (PT-11), rare Self Repair (F-27)

Written 2026-10-02 by Claude (Opus 5.5) from `D:\UO\cc-prompts\cc-P32-spawner-importer-bods-self-repair.md`.
Pinned 7c9215d97 is the authority for every pinned citation. Nothing was committed, deployed, restarted, or
run against any world. ASCII only.

**Numbering:** no clash. P30 (`notes\cc-P30-modernuo-upgrade-research.md`) and P31
(`notes\cc-P31-registrar-office-cleanup.md`) exist; `D:\ShatteredLegacy` was clean at `e092a3d` when this
started (P29 is `56cae9d`). No commit landed while I worked (checked again before the last build).

## Headlines

1. **PT-07, patched, keyed on the guid rather than z.** A z-only patch, as the brief and P17 proposed, would
   bring back **12** of the 338 lost spawners. **326 were stacked on the very same x,y,z**: pinned's data
   puts distinct spawners on one tile (four creature lists on one Lost Lands tile, a chest and a mage on one
   Fire tile). The import's own guid match already replaces the same spawner on a re-run, so the patch
   removes the delete by location and nothing else (`server/patches/ImportSpawners-guid-key.patch`).
2. **What a re-run adds to the test world** (`shared/**` then `post-uoml/**`, the sets the test world
   matches): **338** spawners. Trammel 136, Felucca 127, Tokuno 39, Ilshenar 23, Malas 13, Ter Mur 0. New
   Haven gets back all 8 from P17's table, the Healer among them. P17's Ilshenar 27 counted 4 spawners twice
   (they appear in both Ilshenar Outdoors files with the same guid).
3. **No duplicate Healer:** the New Haven services seeder now retires its own stand-in Healer spawner
   (3462,2559,35) once pinned's (found by its data guid) is back. Its dry run reports this.
4. **`uoml/**` must never be run on this shard.** `docker/uo/SERVER.md:355-357` lists it and live ran it.
   Pinned picks `post-uoml` *or* `uoml` by `Core.SA` (`Gumps/AdminGump.cs:3975`): they are alternatives.
   Stock, uoml's 23 same-tile spawners replaced post-uoml's. With the patch, running both stacks them.
   This is for Chase to know before any live re-run (not asked for here; nothing touches live).
5. **PT-11:** no deed can be paid twice and no deed can get stuck. **One limit was dodged:** a regular smith
   gives large deeds at 70.1 Blacksmithy with no rank, and the guildmaster paid them in Seals and standing
   below Journeyman. Fixed: the Journeyman gate now also applies at the guild turn-in (guildmaster and book).
   **Bigger, not fixed, for Chase:** guild deeds have no cooldown and regular smiths pay OSI's rewards for
   them, so the guild is a free reroll for OSI rewards (section B.4).
6. **F-27:** Self Repair is out of the random table (a two-line pinned patch); a new hook rolls it at 1 in
   500 on magic weapons and armor from high-end corpses. **Found and not changed:** the Artificer imbue
   gump sells Self Repair 5 to 7 on weapons and armor (`customizations/ArtificersImbueGump.cs:274-276`,
   `:304-306`), which is now the common way to get it. Chase's call.

Red and green, through `docker/uo/build.sh` only. **Red** (`--tests-only`, both new patches moved out of
`server/patches`, the Journeyman check forced open, the Self Repair roll made ten times too common, and the
high-end test widened to every creature): 421 tests, **10 failed, exactly the 10 new facts meant to fail**,
each on its own assertion with no exception. There are 11 new facts (5, 2, 4); the eleventh, Part B fact 1,
passed in both runs, as it should (it guards claims, it fixes nothing). **Green** (`-t sl-modernuo:cc-p32`, everything
restored): both patches applied, **421 of 421 passed**, image built. `sl-modernuo:latest` was not touched by these
runs (it and `sl-modernuo:cc-p30-trial` were built by other sessions during this task, 38 and 29 minutes before
mine; my red run used the shared `sl-uo-builder:latest` builder tag, as `build.sh` always does).

**Out of the brief's scope, one file:** `docker/uo/apply-patches.sh` gains two `apply_patch` lines with comments.
The runner fails any patch in `server/patches` that it does not name (the first green attempt failed exactly
so: "present in /patches but never applied"), so the brief's "a pinned change goes in `server\patches\`" cannot
be done without it.

---

## Part A: PT-07, the spawner importer

### A.1 Facts, re-read

- **The command.** Pinned registers `ImportSpawners` (Developer) at
  `UOContent/Engines/Spawners/Commands/ImportSpawnersCommand.cs:23` with handler `GenerateSpawners_OnCommand`
  (`:29`). `[GenerateSpawners` is an alias of it, with `ImportSpawner` and `GenSpawners` (`[Aliases]`, `:27`;
  `CommandSystem.Register` registers each alias, `Server/Commands.cs` Register/DoRegister). The decisions note
  cites `UOContent/Commands/ImportSpawnersCommand.cs`; the file is under `Engines/Spawners/Commands/`.
- **The delete.** `ImportJsonSpawners` (`:193-274`): for each entry, every `BaseSpawner` from
  `map.GetItemsAt<BaseSpawner>(location)` whose type equals the entry's is deleted (`:228-242`).
  `GetItemsAt<T>(Point3D)` builds a `Point2D` from x,y (`Server/Maps/Map.ItemEnumerator.cs:31`): z is ignored.
  Deleting a spawner deletes what it spawned (`BaseSpawner.OnDelete`, `BaseSpawner.cs:1428-1434`, `RemoveSpawns`).
  The new spawner is then made, placed and filled (`:246-249`), and a world spawner with the **same guid** is
  deleted (`:251-254`, from `allSpawners`, built from every `ISpawner` in the world at `:60-67`).
- **The guid is stable.** The JSON constructor reads `guid` from the entry (`BaseSpawner.cs:299-302`); it is
  saved with the spawner (`[SerializableField(0)] _guid`, `:54-57`) and written back by `ToJson` (`:501`).
  All 5,536 entries in `shared/**` and `post-uoml/**` carry one (0 missing). Upstream's reorganisation of the
  data (`723e1a836`, 2025-12-30, which created `shared/`) kept every guid: the 5,604 distinct guids before it
  and after it are the same 5,604 (counted with `git grep` on both trees).
- **The losses, counted** (script over the data, simulating `:228-254` exactly, files in path order;
  `shared/**` then `post-uoml/**`; 100 files, 5,536 entries, 5,532 distinct guids):

  | map | entries | survive stock | lost stock | lost at a different z | lost on the same x,y,z |
  |---|---|---|---|---|---|
  | Trammel | 2,137 | 2,001 | 136 | 9 | 127 |
  | Felucca | 2,122 | 1,995 | 127 | 1 | 126 |
  | Tokuno | 456 | 417 | 39 | 0 | 39 |
  | Ilshenar | 447 | 420 | 27 (4 are one spawner listed twice) | 2 | 25 |
  | Malas | 214 | 201 | 13 | 0 | 13 |
  | Ter Mur | 160 | 160 | 0 | 0 | 0 |

  P17's counts (136, 127, 27, 13, 39, 0) are right as counts of x,y collisions. Of the same-tile ones, **324
  have different creature lists** from the spawner that replaced them and 6 are identical copies. Examples:
  Felucca 5643,1435,0 `EvilMage` and `TreasureChestLevel4`; Felucca 823,2264,0 `FarmableOnion` and
  `FarmableCabbage`; Lost Lands tiles with four different creature lists each (Lost Lands alone is 92 per
  facet).
- **New Haven** (the test world's 52 spawners in the region, P17 1.1.3, match the simulated 52 for exactly
  `shared/**` + `post-uoml/**`; with `uoml/**` it would be 55): P17's table is confirmed, file and guid in
  `post-uoml/trammel/Vendors.json`:

  | x,y,z | lost | survivor today |
  |---|---|---|
  | 3463,2558,35 | Healer (count 2) | HealerGuildmaster (36) |
  | 3526,2536,20 / 21 | BlacksmithGuildmaster, IronWorker | Miner (22) |
  | 3470,2519,49 | HairStylist | Herbalist (48) |
  | 3461,2566,36 / 37 | Herbalist, Alchemist | HairStylist (35) |
  | 3446,2606,32 / 31 | LeatherWorker, Furtrader | Tanner (30) |

### A.2 The patch: why the guid, not z

`server/patches/ImportSpawners-guid-key.patch` (2 hunks, applies at `--fuzz=0`): deletes the
delete-by-location block (`:228-242`) and the now-unused queue (`:212`), with a comment. Nothing else.

Alternatives argued:
1. **Same x,y,z and type** (the brief's first option, P17's suggestion). One comparison. Recovers 12 of 338:
   the 326 same-tile losses stay lost, because pinned's data deliberately stacks different spawners on one
   tile. Rejected: it fixes the visible New Haven case and leaves 96% of the bug.
2. **z plus "only if the old spawner's guid is not in the file being imported"**. Recovers 299: it still
   loses Tokuno's 39, which are stacked across two files (the later file's import deletes the earlier
   file's spawner). Rejected: more code, still wrong.
3. **The guid only (chosen).** The import already matches on guid (`:251-254`), so removing the location
   delete is enough. Simulated on the data: a fresh import keeps all 5,532; a re-run onto a stock-imported
   world adds exactly the 338 lost and removes nothing; a second re-run changes nothing.
   What it gives up: pinned's location delete also replaced a same-type spawner on the tile that the data
   does **not** name (pinned's own comment, `:228-229`, doubts it should exist outside migrations). Now such
   a spawner (staff-placed, or from an older import with other guids) is left alone. Our worlds were made
   from pinned's JSON, whose guids have not changed, so nothing on them is in that position. The one case
   that matters is `uoml/**` (headline 4), and the answer there is not to run it.
4. **Our own command instead of a patch.** A second importer would duplicate pinned's import and the stock
   `[GenerateSpawners` would stay broken in the console and the admin gump (`AdminGump.cs:2032`, `:2104`).
   Rejected.

"Re-running replaces, not duplicates" stays true, by guid (fact 2 below).

### A.3 Facts and runs

`server/tests/Misc/SpawnerImportVerification.cs`, 5 facts, all through the real command typed by a
Developer (`CommandSystem.Handle`, `[GenerateSpawners`):

1. Four spawners on one x,y (z, z+1, z+2, and a second at z+2) all survive one import.
2. Re-importing the same file: every spawner replaced by its guid (old objects deleted), the world's spawner
   count unchanged.
3. The same spawner on the same x,y,z is replaced; a staff spawner of the same type on that tile is kept.
4. Pinned's `post-uoml/trammel/Vendors.json` (95 spawners), imported for real from the test host's copy:
   all 95 present, each of the 8 New Haven vendors at its tile; a second import changes nothing.
5. The seeder: with its stand-in placed and then pinned's Healer imported, the dry run reports the retirement
   and deletes nothing; the real run deletes the stand-in and its Healers and places nothing; a third run
   does nothing.

Red (no patch): all 5 failed. (1) 1 of 4 survived, the last, `Cat` at z 2. (2) 2 of 3 on the first import.
(3) the stranger was deleted. (4) 87 of 95 after one import, and no Healer at 3463,2558,35. (5) "pinned's Healer
spawner is not in the world after importing Vendors.json". Green: all 5 pass.

### A.4 P17's Healer, and what an existing world needs

`ClusterFNewHavenServicesSeeder` (P17) already places nothing when any Healer or Healer spawner is in New
Haven (`HasHealer`), so on a fresh world, where spawners come first, it never places the stand-in. On a world
that has the stand-in, a re-run of Vendors.json would add pinned's Healer spawner beside it: four Healers.

Chosen: **the seeder retires its own stand-in once pinned's is back.** It finds pinned's by its data guid
(`f713041b-8980-4839-84cb-232cb39f710a`, `Vendors.json:146-161`) and the stand-in as the `Spawner` on
3462,2559,35 whose only entry is `Healer` and whose guid is not pinned's. That is the only thing the seeder
ever deletes; the header, `[Description]` and the console summary say so. It is not marked red in the
console (`Shard-Console.ps1` `Test-WorldCommandWarn` reds a summary starting "DELETES"); the overseer may want
it red. A cleanup command was the alternative; rejected because the seeder is already in the console's New
Haven sequence, right where it is needed, with a dry run.

An existing world needs: the re-run (A.5), then `[ClusterFSeedNewHavenServices dryrun` and
`[ClusterFSeedNewHavenServices`. A world where the seeder never ran needs only the re-run.

### A.5 Chase's run order, test world only

**Not live.** There is no dry run for `[GenerateSpawners`. Developer access. Needs an image with the patch
(`sl-modernuo:cc-p32`, or a later one once committed) on the test shard.

```
[save
[GenerateSpawners Data/Spawns/shared/**/*.json
[GenerateSpawners Data/Spawns/post-uoml/**/*.json
[ClusterFSeedNewHavenServices dryrun
[ClusterFSeedNewHavenServices
[save
```

- Do **not** run `Data/Spawns/uoml/**` (headline 4).
- Do **not** run plain `[ClusterFOldHavenCleanup` afterwards: its box starts at x 3520
  (`ClusterFOldHavenCleanup.cs:106`) and `BlacksmithGuildmaster` is on its list (`:93`), so it deletes the
  restored New Haven Blacksmith Guildmaster spawner at 3526,2536,20 (P21 section 7 defect 2, still open).
- Each `[GenerateSpawners` replaces and respawns every spawner in its files, so every stock-spawned NPC and
  creature is recreated, not only the 338. Vendors lose nothing (their stock is generated), but any creature
  a player was fighting is replaced.
- What to see: the import messages say `Generated 5,532`-ish in total across the two (the per-command totals
  count every spawner in the files, not only new ones). In New Haven: two Healers by 3463,2558, the
  HealerGuildmaster, a BlacksmithGuildmaster and IronWorker by 3526,2536 with the Miner, a HairStylist and an
  Alchemist and Herbalist by 3461,2566 and 3470,2519, a LeatherWorker and Furtrader by 3446,2606 with the
  Tanner. The seeder's dry run says `stand-in Healer spawner at (3462, 2559, 35) would be retired` if the
  stand-in is there, or `Healer spawner already there` with no retirement if it never was. After the real
  run: no spawner left on 3462,2559 (`[where` there, or `[props` the tile), and only two Healers.
- Counts to check: `[global count where Spawner` before and after should rise by about 338 (by exactly 338
  plus anything staff placed since, if the world was made by those two patterns).

### A.6 Re-run counts by file (what each pattern adds to a world made by the stock import)

`shared/**`: Felucca LostLands 92, Outdoors 27, Vendors 3, Fire 2, FelCropsLS 1, Hythloth 1, Reagents 1;
Trammel LostLands 92, Outdoors 26, Vendors 5, Fire 2, Hythloth 1, Reagents 1, TramCropsLS 1; Tokuno Outdoors
39; Malas Doom 12; Ilshenar Outdoors 11, Towns 7, Sorcerers 3, Blood 1, Vendors 1.
`post-uoml/**`: Trammel Vendors 8 (all New Haven), Malas South 1. Total 338.

### A.7 ModernUO upstream, draft issue for Chase to file

> **ImportSpawners (JSON) deletes stacked spawners from the shipped data**
>
> `ImportJsonSpawners` deletes every existing spawner of the same type at the entry's location before
> placing it (`Engines/Spawners/Commands/ImportSpawnersCommand.cs:228-242`). `Map.GetItemsAt<T>(Point3D)`
> matches on x,y only, and the shipped `Distribution/Data/Spawns` stacks spawners on one x,y, both at
> different z and at the same z with different entries. So each later spawner deletes the earlier one:
> importing `shared/**` and `post-uoml/**` keeps 5,194 of 5,532 spawners (Trammel loses 136, Felucca 127,
> Tokuno 39). Example: `post-uoml/trammel/Vendors.json` has a Healer at 3463,2558,35 and a HealerGuildmaster
> at 3463,2558,36, and New Haven ends up with no Healer. The guid match a few lines below (`:251-254`)
> already makes re-imports replace rather than duplicate, so dropping the location delete fixes it. We
> patched it that way on our shard. Also: `uoml` and `post-uoml` are alternatives (`AdminGump.cs:3975`), and
> without the location delete, importing both stacks their overlapping spawners (23 tiles).

---

## Part B: PT-11, smith BODs through both paths

### B.1 Facts, re-read

- **Regular smiths** (pinned, unpatched: no patch in `server/patches` touches `Blacksmith.cs`):
  issue on the context menu or 20% of purchases when `NextSmithBulkOrder` is zero, then set it to 1, 2 or 6
  hours by skill; a large deed at 70.1 by chance, `new LargeSmithBOD()`; a small by
  `SmallSmithBOD.CreateRandomFor` (`Mobiles/Vendors/NPC/Blacksmith.cs:76-105`). Accept `SmallSmithBOD` and
  `LargeSmithBOD` (`:107`). Turn-in pays OSI's reward item, gold and fame and deletes the deed
  (`BaseVendor.cs:1078-1150`, delete `:1148`); in SE+ it resets the issuing timer (`Blacksmith.cs:121-127`).
- **Guild path** (`customizations/ClusterFSmithBODSystem.cs`): members only; no cooldown; a cap of 3 small
  and 1 large **counted in the backpack** (`CountBODs`, `:437-454`); a large deed needs Journeyman (5,000
  standing) and 70.1 (`:93-105`, `:131-165`). Turn-in, at the guildmaster (`OnDragDrop`, `:176-245`) or
  from the Smithing Guild Book anywhere (`TurnInBOD`, `:402-431`; `SmithGuildBook.cs:572-581`), pays
  Seals, standing and 1 to 3 skill checks, and deletes the deed. Requesting from the book also works
  anywhere (`SmithGuildBook.cs:617-643`).
- **The header comment was wrong.** It said regular smiths no longer issue or accept BODs, by
  `patches/Blacksmith_DisableBODs.patch`. That patch is not in `server/patches`. Corrected in the file.

### B.2 The three questions, answered

1. **Can a deed pay twice?** No. Every path deletes the deed it pays for: vendor `BaseVendor.cs:1148`,
   guildmaster `ClusterFSmithBODSystem.cs:244`, book `:429`. A small combined into a large is deleted by the
   combine (`LargeBOD.cs:148`); our "combine contained" goes through the same `EndCombine`
   (`customizations/BODCombineContained.cs:82`). A book turn-in on a deed already paid elsewhere finds it
   deleted ("That order no longer exists", `SmithGuildBook.cs:575`).
2. **Can the guildmaster's limits be dodged through a vendor?**
   - The 3/1 cap: no, not through a vendor. Vendor deeds in the pack count toward it (`CountBODs` counts every
     `SmallSmithBOD`/`LargeSmithBOD`). It can be dodged without one (B.4).
   - The turn-in skill check: a vendor deed turned in at the guild gets it, a guild deed turned in at a
     vendor does not. Nothing is gained either way.
   - **The Journeyman gate: yes.** A regular smith gives a large deed at 70.1 with no rank, and the
     guildmaster paid it (a large Valorite exceptional is about 500 Seals and 310 standing, `:249-268`,
     `:328-338`). **Fixed** (B.3).
3. **Can a deed get stuck?** No. Both accept both (`Blacksmith.cs:107`, `ClusterFSmithBODSystem.cs:170`). A
   player who leaves the Society can still take a guild deed to any smith. A post-Valorite deed (only the guild
   issues large ones; both issue small ones, through the patched `SmallSmithBOD.CreateRandomFor`) is paid by a
   regular smith as an iron deed: pinned's reward tables stop at Valorite (`Engines/Bulk Orders/Rewards.cs:438-440`,
   `:486-487`). Underpaid, not stuck; the guild is the place for those.

### B.3 The fix

`ClusterFSmithBODSystem.cs`: `CanTurnInLarge(pm)` is the same gate as requesting (Journeyman standing, or an
active Dev Testing Crystal), checked in `OnDragDrop` after the completeness check and in `TurnInBOD`.
`SmithGuildBook.HandleTurnInBOD` says why instead of "not yet complete". The deed stays in the pack and the
refusal says any blacksmith will take it. No saved type changes. The two `5_000` literals became one constant.

Facts (`server/tests/Misc/SmithBODPathsVerification.cs`): (1) a guild deed at a regular smith and a vendor
deed at the guildmaster are each paid and deleted, and a small combined into a large is deleted;
(2) a complete vendor large deed pays a member at 1,000 standing nothing at the guildmaster or the book and
stays in the pack, and pays at 5,000. Red (check forced open): fact 2 failed, "below Journeyman (1000):
guildmaster True, book True; seals 0 -> 47"; fact 1 passed, as it should (it guards claims, it fixes nothing).
Green: both pass.

### B.4 Found, not fixed: the guild is a free reroll for OSI's rewards

Guild deeds have no cooldown, and the cap only counts the backpack. A member can request three, keep the good
ones, drop the rest in a trash barrel or the bank, and request again, as often as they like. Regular smiths
pay OSI's rewards for those deeds. So OSI's per-deed throttle (`Blacksmith.cs:78-95`, 1 to 6 hours, reset only
by a turn-in) no longer limits how fast a player can hunt the large-set deeds behind runic hammers and power
scrolls. Within the guild path the same reroll only speeds up Seals, which is Chase's design.

Not fixed because each fix changes the design Chase just confirmed: give the guild a cooldown; or mark guild
deeds and have regular smiths refuse them (a saved field on a pinned type, and lost through a bulk order book,
which rebuilds deeds); or count the bank and books toward the cap (still dodged by any other container).
**For Chase.**

### B.5 Deviation text for the register

> **Smith BODs: two paths (Ours).** OSI has one: any blacksmith gives and takes them. Here:
>
> | | Any blacksmith (OSI) | Blacksmith Guildmaster and Smithing Guild Book (Society of Smiths) |
> |---|---|---|
> | who | anyone with Blacksmithy | Society members |
> | gives | small deeds, large at 70.1, one per 1 to 6 hours or per turn-in | small and large, no cooldown, at most 3 small and 1 large in the backpack; large needs Journeyman (5,000 standing) and 70.1; deeds above Valorite at 105+ skill |
> | takes | any smith deed | any smith deed; a large one only from a Journeyman |
> | pays | OSI's reward item, gold, fame | Smithing Seals (about the deed's gold value / 400, more above Valorite), standing, 1 to 3 Blacksmithy skill checks |
> | where | every blacksmith | the guildmaster, or the book anywhere |
>
> Reason: the guildmaster is not everywhere smiths are (Chase, 2026-10-02). A deed above Valorite pays as iron
> at a regular smith.

### B.6 How F-25 meets this

F-25 makes turn-in "bank or cash out" with a standing toggle changed at the craft's guildmaster. With two
paths, "cash out" already exists: a regular smith pays OSI's rewards. Three things for whoever specifies F-25:
the toggle can only govern the guild path (regular smiths are pinned's, and would need a patch to read it);
large deeds "filled directly" (F-25 part 2) change `LargeBOD`, which regular smiths also pay for, so the
smaller bonus must hold at both or the vendor path becomes the better place to cash in a directly filled deed;
and B.4's reroll gets worth more as banking makes the top rewards reachable.

---

## Part C: F-27, Self Repair becomes extremely rare

### C.1 Facts, re-read

- Random table (`Items/Skill Items/Tools/BaseRunicTool.cs`): armor `baseCount = isShield ? 7 : 20` at `:635`,
  offset 0 or 4 at `:636`; case 5 is `SelfRepair 1-5` (`:703-707`, the call at `:705`), so a shield draws it
  from 7 slots and other armor from 20. Hats: `GetUniqueRandom(19)` (`:825`), case 12 is `SelfRepair 1-5`
  (`:894-898`, the call at `:896`). The weapon table has no Self Repair. Those are the only two random
  writers in pinned (every other `SelfRepair` hit is a fixed value, a reader, or `AOS.cs`).
- The same functions serve runic crafting (`m_IsRunicTool`, `:296`, `:626`, `:814`; the instance overloads
  `:268`, `:598`) and loot (`LootPack.cs:722-730` per the feature queue).
- Effect: N in 10 chance per wear to gain instead (`BaseArmor.cs:763`, `BaseWeapon.cs:2088`, `BaseShield.cs:35`,
  `BaseClothing.cs:351`).
- Artifacts set it as a fixed value in their constructors (Aegis: `Items/Shields/Artifacts/Aegis.cs:12`, rarity
  11 at `:19`).

### C.2 What changed

- **Pinned patch** `server/patches/BaseRunicTool-no-random-self-repair.patch` (2 hunks, `--fuzz=0`): marks the
  Self Repair slot as taken before the draw (`m_Props.Set(isShield ? 5 : 1, true)` for armor;
  `m_Props.Set(12, true)` for hats), the same way pinned already removes Mage Armor and leather's slots
  (`:638-647`). The item still gets its full number of properties, drawn from the rest. Alternatives: zeroing
  Self Repair after the roll in our own code would need a hook at every caller (loot, runic crafting, quest
  bags, chests) and would leave items one property short; a replacement file of `BaseRunicTool.cs` (1,200
  lines) for two lines is far worse to carry. Runic crafting goes through these functions, so it cannot
  produce Self Repair either.
- **Our hook** `server/customizations/ClusterFRareSelfRepair.cs` on pinned's `BaseCreature.CreatureDeathEvent`
  (raised at `BaseCreature.cs:3411` after the corpse holds the loot; also at `:3281` for a bonded pet, which
  the hook excludes as controlled). No patch.
  - **High-end, chosen:** `BaseChampion` (pinned's 10 champion bosses) and `Harrower`; any paragon
    (`IsParagon`); our `BasePeerless` and so `BaseSABoss` (Medusa, Slasher of Veils, Stygian Dragon,
    Niporailem); `DespiseBoss`, `ShameGuardian`, `NavreyNightEyes`; and any type implementing
    `IRareSelfRepairSource`, for the New Haven dungeon mini champ when it is built. Not champion spawn minions
    (thousands per spawn would make it common there). Not controlled or summoned creatures.
  - **Eligible items:** weapons and armor (shields included) in the corpse with at least one magic property
    (attributes, weapon or armor attributes, skill bonuses, or resist bonuses), `ArtifactRarity` 0 and no Self
    Repair already. So artifacts and set pieces keep their fixed values.
  - **Roll:** 1 in 500 per item; intensity 1 70%, 2 28%, 3 1.5%, 4 0.4%, 5 0.1%.

### C.3 Facts and runs

`server/tests/Items/RareSelfRepairVerification.cs`, 4 facts, seeded:
1. 20,000 five-property ordinary rolls each on plate, studded leather, a heater shield, a tricorne and a
   longsword: no Self Repair.
2. 20,000 Valorite runic hammer applications each on plate and a heater shield: none.
3. 500,000 high-end rolls on an eligible plate chest: within 15% of 1,000, 1 or 2 at least 95%, 3 to 5 seen
   and at most 5%.
4. With every roll forced to hit: an ordinary Ettin's corpse gets nothing; a paragon's magic plate gets
   intensity 1, its plain longsword nothing, and the Aegis keeps 5. Barracoon is high-end; a tamed paragon
   is not.

Red: all 4 failed. Without the patch, in 20,000 five-property rolls each: plate 5,022, studded 5,517, **shield
14,326** (72%: five draws from seven slots), hat 5,239, longsword 0; Valorite runic hammer: plate 4,888, shield
14,323. With the roll made ten times too common: 9,883 of 500,000 (range 850 to 1,150), intensity 1 to 5
6,928 / 2,763 / 148 / 40 / 4 (98.1% at 1 or 2, so the intensity curve was already right). With every creature
high-end: the ordinary Ettin was accepted. Green: all 4 pass.

### C.4 Deviation text for the register

> **Self Repair is extremely rare (Ours).** OSI rolls it on random magic armor, shields and hats (often on
> shields) and from runic crafting. Here it never comes from the ordinary loot table or from runic tools. It
> comes only from bosses, champions and paragons: each magic weapon or piece of armor they drop has a 1 in
> 500 chance of it, almost always at 1 or 2. Weapons can have it too, which OSI's random loot never gives.
> Named artifacts and sets keep their fixed values. Reason: field maintenance through Arms Lore (F-26) does
> its job (Chase, 2026-10-02, F-27).

The imbue gump line (headline 6) needs Chase's decision before this text is final.

---

## Checklist for Chase

**Part A (test world, after `sl-modernuo:cc-p32` or its commit is on the test shard):** the run order in A.5.
In New Haven you should see the Healer pair at 3463,2558, the Blacksmith Guildmaster and IronWorker at
3526,2536, the HairStylist, Herbalist and Alchemist, the LeatherWorker and Furtrader; one Healer spawner only
(none on 3462,2559 after the seeder). Do not run plain `[ClusterFOldHavenCleanup` afterwards. Do not run
`uoml/**`.

**Part B (client):**
1. A member below Journeyman with 70.1+ Blacksmithy: get a large deed from a regular smith (context menu,
   until one is large), fill it (or `[props` its entries full), drop it on the Blacksmith Guildmaster: refused
   with "Large orders are for Journeymen of the Society. Any blacksmith will take this one." and the deed
   stays. The book's turn-in button says the same.
2. Drop the same deed on the regular smith: OSI's reward, deed gone.
3. A Journeyman: same deed at the guildmaster pays Seals and standing.
4. A guild small deed at a regular smith: gold, deed gone. A regular smith's small deed at the guildmaster:
   Seals, deed gone.

**Part C:** no staff command shows the roll; only many kills of high-end creatures can (expect one item in
500 magic weapons and armor from them). On a test shard, `[props` a dropped magic item's Self Repair to check
it is 0 on ordinary loot; a staff-spawned paragon (`[add Ettin` then `[set IsParagon true`) killed many times
is the long way. The facts above are the evidence.

**Decisions for Chase:** the imbue gump's Self Repair (headline 6); the guild reroll (B.4); whether the
seeder's console line should show red (A.4); and fixing `[ClusterFOldHavenCleanup`'s box (P21 defect 2) before
anyone runs it on a world that has New Haven's Blacksmith Guildmaster back.

## Files changed (`D:\ShatteredLegacy`)

- `server/patches/ImportSpawners-guid-key.patch` (new, pinned)
- `server/patches/BaseRunicTool-no-random-self-repair.patch` (new, pinned)
- `server/customizations/ClusterFRareSelfRepair.cs` (new)
- `server/customizations/ClusterFNewHavenServicesSeeder.cs` (retires the stand-in; header, description, summary)
- `server/customizations/ClusterFSmithBODSystem.cs` (Journeyman gate at turn-in; header corrected)
- `server/customizations/SmithGuildBook.cs` (the book says why a large deed is refused)
- `server/tests/Misc/SpawnerImportVerification.cs`, `server/tests/Misc/SmithBODPathsVerification.cs`,
  `server/tests/Items/RareSelfRepairVerification.cs` (new)
- `docker/uo/apply-patches.sh` (two `apply_patch` lines; outside the brief's scope, see headlines)

No saved type changed (the seeder, hook and BOD changes add no serialized fields). No new command.
`scripts/Shard-Console.ps1` unchanged.
