# cc-P77: Order of the Alembic (guild 18)

Run 2026-10-12 by Claude Code (autopilot hand-off after P76). Builder. Feature queue: F-43 and the F-9 table note.
The brief's `docs\` targets live in this file, since agents never edit `docs\`.

Sources:
- Pinned engine `D:\UO\ModernUO-pinned` at **`d4531cd94b739613155225c234900de9f47d2c88`**.
- Code repo `D:\ShatteredLegacy`, built as `sl-modernuo:cc-p77`. Not deployed, not committed, `latest` not moved.
- Tools: `notes\cc-P77-tools\`, copied from cc-P15's map tools. The PNG previews there are git-ignored
  (`.gitignore:25`, checked with `git check-ignore`).

## What was built

| Part | Change | Where |
|---|---|---|
| A | New guild: key `alembic`, display name "Order of the Alembic" | `ClusterFGuildSystem.cs`, `EnsureRegistered` |
| A | Apprentice task: Alchemy 50.0, or 10 Empty Bottles as tribute (same pattern as the other craft guilds); pays 25 standing and 10 scrip | same |
| A | Six-rank ladder, index 0 to 5, on the generic steps (0, 1,000, 5,000, 15,000, 50,000, 100,000 standing), with its own name table. **Placeholders:** the generic names until you pick (B below) | `ClusterFAlembicGuild.RankNames`; `GetRankName` gets an `alembic` case |
| A | Its own currency, stored per guild key like every guild's (`CharacterGuildData.GuildCurrency`), named **"Alembic Drams"** (placeholder) | `ClusterFAlembicGuild.CurrencyName`; added to `MuleUpgrades.CurrencyNames`, the shard's one name table |
| A | Joining is free, no skill or gold (the shared `Join`, F-9) | unchanged code path |
| A | Skills: Healers' Covenant now Healing, Anatomy; the Order Alchemy, Taste ID | `GuildSkillTable` |
| B | Guildmaster `AlembicGuildmaster` ("Distiller Orla Vance, of the Order of the Alembic"), a `StarterGuildmasterBase` like the Dojo's and the Keepers' | `ClusterFAlembicGuild.cs` |
| B | Post: the **Little Shop of Alchemy**, New Haven, Trammel **3463,2565,35**, Seeded | `GuildLocations.All` |
| B | Starter kit: Alchemy's creation items (4 empty bottles, a mortar and pestle, a robe). Taste ID has no creation items (`CharacterCreation.cs:959-966`; no `TasteID` case). The Healers' kit lost the bottles and mortar | follows from `GuildSkillTable` (F-9 rule: creation items per skill) |
| B | Guild Directory and League Guild Referrals: both draw `GuildProgressGump.Guilds()`, which is every registered guild, so the Order has a row with no further change (18 rows, 3 pages of 8) | `ClusterFGuildSystem.cs:808-822`; `LeagueRegistrarGump.cs:17` |
| D | Hall props: one addon, `AlembicHallAddon`, 11 stock-art components along the north wall | `ClusterFAlembicGuild.Hall` |
| D | Seeder `[ClusterFSeedAlembicHall [dryrun]` (Administrator, WorldSetup, re-run skips, test shard first). World load seeds only if `clusterf.alembicHall.seedOnWorldLoad` is true (default false) | `ClusterFAlembicGuild.cs` |
| - | Patch notes 2026.10.12.10 and `VERSION` | `CHANGELOG.md`, `VERSION` |

Not changed: the Healers' Covenant itself (name, pitch, its Healing 50 Apprentice task, its two New Haven starter
items). None of the 26 New Haven starter quests is an Alchemy or Taste ID quest, so `GuildStarterItems` did not change.

## Part B: the hall

**Building.** Pinned's post-UOML Trammel vendors spawn the Alchemist at **3461,2566,37**, with a Herbalist at
3461,2566,36 (`Distribution/Data/Spawns/post-uoml/trammel/Vendors.json`).
- Only a HairStylist survived pinned's importer on that tile (cc-P17 section 1.2 item 3); cc-P32's re-import restores
  the other two.
- Our `ClusterFNewHavenSeeder.cs:35` names the shop "Little Shop of Alchemy", and seeds Sadrah the courier at
  3462,2567,35.
- Read from the client map with the cc-P15 renderer, the shop is one room:
  - walls x3456 to 3465 and y2562 to 2571, slate floor at z35;
  - a door at 3465,2567 (east, onto the boardwalk) and one at 3457,2567 (west, steps down at 3456,2567);
  - display cases along the west wall and one in the middle (x3461, y2567 to 2569);
  - two bookcases at 3460-3461,2563.
- It is a separate building from the Healer's Hall to its north (x3460 to 3467, y2554 to 2561).

**The post, 3463,2565,35:**
- **Dry land and walkable.** Checked with the cc-P15 port of pinned `Map.CanFit` (height 16, client map, statics,
  pinned decoration), with the hall props added as decoration (`notes\cc-P77-tools\walk.py`):

  ```
  GM tile fits at z35: (True, 'ok')
  doors in fit set: [(3465, 2567), (3457, 2567)]
  all 8 neighbors: reachable (a walk from both doors at z35)
  2564 ...ooooooo...
  2565 ...oooooGo...
  2566 ..oooooooo...
  2567 ..oooo.oooo..      (x 3455 .. 3467; o reachable, G the guildmaster, . blocked)
  ```

- **Clear of the other NPCs:** not on Sadrah's tile or the Alchemist spawn tile.
- **Faces south**, toward the room and the east door.

**How it gets onto an existing world** (a world-state step, your call; test shard first):
1. `[ClusterFSeedGuildHalls dryrun`: it should list `alembic (AlembicGuildmaster) at Little Shop of Alchemy: would
   place at (3463, 2565, 35)`. The other Seeded guildmasters already there count as present.
2. `[ClusterFSeedGuildHalls`: places the missing ones only. It never duplicates (a guildmaster of the type within 15
   tiles counts as present).
3. `[ClusterFSeedAlembicHall dryrun`, then `[ClusterFSeedAlembicHall`: the 11 props, once. It moves and deletes nothing.

A fresh world gets both from the same two commands, or from the two `seedOnWorldLoad` settings if you set them.

## Part C: existing members and data

- **Healers' members with Alchemy or Taste ID skill: nothing is lost.**
  - Skill values are the character's, not the guild's.
  - Healers' standing, scrip, rank and Apprentice status stay with the Healers: they are stored by guild key, and
    no key changed.
  - Everyone starts in the Order at rank 0 (Initiate), not a member until they join. Joining is free.
- **Small duplicate:** a character who took the Healers' kit before this change already has Alchemy's bottles,
  mortar and robe. Joining the Order hands them over again, once. On a fresh world this does not arise. Not
  worth code; noted.
- **Alchemy BODs (F-20): no issuer data exists to move.**
  - The only BOD code is the smith's (`ClusterFSmithBODSystem.cs` and the files beside it).
  - Searching `server\customizations` finds no Alchemy BOD, no `AlchemyBOD` type, and no Arcane Society BOD issuer.
  - F-20's table already names the Order as the Alchemy BOD home (feature-queue.md:1724). When the Alchemy BOD port
    is built, it issues from `alembic`.
- **League promotion counts the Order like any guild.** `ClusterFLeagueRanks.CountGuildsAtOrAbove` loops over the
  character's joined guilds and asks `GuildRankIndex` for each (`ClusterFLeagueRanks.cs:320-338`). A test shows the
  Order counting at Apprentice and at Master.
  - The League ladder validator reads `AllGuilds.Count` (`ClusterFLeagueRanks.cs:570`), so a rank asking for "N
    guilds" can now ask up to 18.

## Part D: hall decor and art plan

### Stock decor in this pass (`ClusterFAlembicGuild.Hall`)

| Item | Art | Tile, z |
|---|---|---|
| alchemist table (ML, south-facing; pinned `AlchemistTableSouthAddon`) | 0x2DD4 | 3458,2563,35 |
| alchemist table | 0x2DD4 | 3459,2563,35 |
| mortar and pestle | 0x0E9B | 3458,2563,40 (on the table) |
| flask | 0x182A | 3458,2563,40 |
| scales | 0x1852 | 3459,2563,40 |
| wooden shelf (pinned `EmptyBookcase` art), beside the shop's two bookcases | 0x0A9D | 3462,2563,35 |
| dried herbs | 0x0C41 | 3462,2563,47 (on the shelf) |
| cauldron | 0x0975 | 3463,2563,35 |
| alchemist table | 0x2DD4 | 3464,2563,35 |
| heating stand, lit (pinned `HeatingStand.LitItemID`) | 0x184A | 3464,2563,40 |
| full vials (pinned `FullVialsWRack`) | 0x185D | 3464,2563,40 |

**Why the north wall.** A first layout put a work table against the south wall and a desk against the east wall.
Rendered, both were hidden behind those walls: the south and east walls draw in front in the client's view. Every
prop now stands along the north wall, which the render shows clearly. The rest of the room stays as it was:
- the shop's display cases and bookcases;
- the aisles between the cases;
- both doors;
- the eight tiles around the guildmaster.

Not used: the SA wall shelves (0x4C38 to 0x4C3B) and the alchemy machine (0x9D83 and up). Their art may not be in
every client's files, so they are left out until checked against our client.

### Art plan for a later art registration prompt (nothing registered or shipped here)

Nothing ships until:
- it is in `player-package\vendor\shattered-legacy-art\registry.csv`, with a slot from `scripts\find-free-art.py`;
- its SOURCE.txt terms are met.

DRC1K art: no modification without his OK. In-game hues are fine.

**On disk now (`D:\UO\third-party\`):**

| Piece | Folder, files | Use in the hall | Adds or replaces | Terms (SOURCE.txt) |
|---|---|---|---|---|
| Animated blue stone pillar lamp (7 frames) | `drc1k-uoassets\Blue_Stone_Assets\PillarLamp\pillar_lamp1.bmp` to `pillar_lamp7.bmp` (preview: `Animated Blue Stone Pillar Lamp.gif`) | a light by each door, or one in the room's open corner. It needs a light source on the item (an addon component cannot carry a light, so a small item class) | adds | DRC1K: non-commercial, ship only inside the client package, no modifications, attribution on our site |
| Blue stone arches | `drc1k-uoassets\Blue_Stone_Assets\arch_north.bmp`, `arch_west.bmp` (and `bow1`/`bow2`/`bow3` `_north`/`_west`) | over the inner doorways, if the hall is ever rebuilt as a stone hall; the wooden shop has no frame for them now | adds, later | DRC1K, as above |
| Barrels | `drc1k-uoassets\Barrels_By_DRC1K_UOASSETS\1.bmp` to `17.bmp` (the plain ones), `34_1.bmp`, `34_2.bmp`, `35_1.bmp` (stacks); previews `Barrel Overview 1.jpg`, `Barrel Overview 2.jpg`. Not the `_ruined` ones (19 to 33) | reagent casks outside the east door on the boardwalk (3466 to 3469, y2564 to 2571, z36), or a cask in the room's south corner (there they hide behind the wall; outside reads better) | adds | DRC1K, as above |
| Sewer pipes | `drc1k-uoassets\Sewer_Assets\pipe*.bmp`, `pipe_up_curve*.bmp`, `pupe_*.bmp` | still pipework for the "glassblowing" corner, with the bubble vat below | adds | DRC1K, as above |
| Oil lantern | `oil-lantern\lantern 1.bmp` to `lantern 3.bmp`, `lantern 4.png` | a hanging lantern over the work tables | adds | Ems; **no license file**: check the page's terms before shipping |
| Paintings | `paintings-odin\Paintings\*.bmp` (10 public-domain Pre-Raphaelite works; "The Garden of the Hesperides" or "Morgan le Fay" suit an alchemist) | one on the north wall above the shelf | adds | Odin; **no license stated**: ask or credit |

**Queued, not on disk yet** (`D:\UO\third-party\download-queue.md` rows 6 to 10, all still "todo" on 2026-10-12):

| Row | Piece | Planned folder | Use | Adds or replaces |
|---|---|---|---|---|
| 6 | Partialhue flasks (.1995) | `partialhue-flasks` | **replaces** the stock flask and full vials on the tables. Partial hue lets the liquid take a potion color while the glass stays clear | replaces |
| 7 | Hueable Anim Bubble Vat (.2145) | `bubble-vat` | the hall's centerpiece: **replaces** the stock cauldron at 3463,2563 (or stands in the SE open floor if it is larger than one tile) | replaces |
| 8 | Mad Scientist Items (.1797) | `mad-scientist` | lab dressing on the tables: retorts and coils beside the heating stand | adds |
| 9 | Rooster's Creature Tanks (.1999) | `creature-tanks` | specimen tanks, a pair by the west door, if tank footprints leave the door clear | adds |
| 10 | Base Item Variants (.1766) | `base-item-variants` | reagent and potion variants for the shelf and cases | adds |

Each needs its terms read when it lands. Footprints must be checked with `walk.py` before placing, so the doors and
the guildmaster's ring stay open.

## Rank name proposals (for Chase; placeholders in data until you pick)

The ladder's steps are the generic ones (index 0 to 5). Pick a set, mix them, or write your own.
`ClusterFAlembicGuild.RankNames` is the one place to change them.

| Index | Standing | A: the still | B: the work (alchemy's stages) | C: the order |
|---|---|---|---|---|
| 0 | 0 | Bottle-washer | Calcinator | Postulant |
| 1 | 1,000 | Stillhand | Distiller | Acolyte of the Alembic |
| 2 | 5,000 | Distiller | Sublimator | Brother or Sister of the Still |
| 3 | 15,000 | Alchemist | Philosopher | Keeper of the Retort |
| 4 | 50,000 | Master Alchemist | Adept of the Great Work | Elder of the Order |
| 5 | 100,000 | Alembic Sage | Magus of the Philosopher's Stone | Grand Alembic |

My pick: **A**. It reads as a trade, like the Smiths' and Foresters' ladders, and the top rank names the guild.
Note: C's rank 2 needs one word for every player; "Fellow of the Still" works for either.

## Tests (red then green)

New: `server\tests\Misc\AlembicGuildVerification.cs`, six facts:
1. Joining the Order hands over Alchemy's kit (4 bottles, mortar, robe; three items). On the same character, the
   Healers' kit then has bandages and scissors, and no bottle or mortar.
2. Alchemy and Taste ID are the Order's and nobody else's; the Healers keep Healing and Anatomy. The Apprentice task
   is Alchemy, or bottles.
3. The Order's ranks read through `GuildRankIndex`:
   - each step is index 0 to 5, one below each step is the index below, and the names are `RankNames`;
   - the Apprentice task lifts the index to 1;
   - League promotion counts the Order at Apprentice and at Master.
4. The guildmaster's post is the measured walkable tile:
   - no prop on or beside it, and clear of Sadrah and the Alchemist spawn;
   - the hall seeder's dry run would place it there;
   - the NPC is invulnerable and keyed to the Order.
5. The hall props are one addon whose components land on their design tiles, all along the north wall.
6. The Order has a Directory row (so a Referrals row), and its currency name.

Changed:
- `GuildStarterPathVerification`:
  - fact 1's Healers kit no longer has the mortar or bottles;
  - fact 5 counts 18 guilds; "every skill has exactly one guild" is unchanged and still passes.
- `GuildDirectoryRowsVerification`: fact 2 is now "18 guilds are 18 rows" (renamed).

The test host has no map files (D27), so "spawns on a walkable tile" is the offline CanFit measurement, pinned by
fact 4. NewHavenSeederFloorVerification does the same.

### Runs

| Run | Command | Result |
|---|---|---|
| Green, first | `bash docker/uo/build.sh -t sl-modernuo:cc-p77 --tests-only` | **1090 passed**, 0 failed; all six Alembic facts pass |
| Red | the same, after breaking each fact (below) | **8 failed** of 1090, 1082 passed |
| Restore | backups copied back; `cmp` byte-identical for all three files | diff back to the green state (7 files, +49 -15, plus the two new files) |
| Green, full | `bash docker/uo/build.sh -t sl-modernuo:cc-p77` (builder, tests, runtime image) | **1090 passed**; "Built sl-modernuo:cc-p77 with patches applied and 1090 shard test(s) passing." `sl-modernuo:latest` unchanged (8863156884f8, 2 days old) |

What the red run broke, and what failed:

| Break | Failed, with message |
|---|---|
| Alchemy and Taste ID back with the Healers, the Order's skills empty | `JoiningTheOrderHandsOverTheAlchemyKitAndTheHealersNoLonger` (Contains: filter not matched); `AlchemyAndTasteIdAreTheOrdersAndTheHealersKeepHealingAndAnatomy` (collections differ); `GuildStarterPathVerification.AFreshCharacter...` (the Healers' kit had the mortar again: values differ) |
| Rank names ignore the index (always the first) | `TheOrdersRanksReadThroughGuildRankIndex` (strings differ); `GuildRankIndexVerification.EachLaddersThresholdsAreWhereItsRankNameChanges` ("alembic: the name does not change at 1000") |
| The post moved onto Sadrah's tile, 3462,2567 | `TheGuildmastersPostIsTheMeasuredWalkableTile...` (values differ) |
| The cauldron moved beside the guildmaster, off the north wall (3463,2566) | `TheHallPropsAreOneAddonAtTheirDesignTiles` ("1 out of 11 items did not pass") |
| The currency name removed | `TheOrderHasADirectoryRowAndANamedCurrency` (strings differ) |

## Decisions for Chase

1. **Rank names:** pick set A, B, C or your own (table above). Placeholders until then.
2. **Currency name:** "Alembic Drams" is a placeholder. Others: "Still Marks", "Vial Tokens".
3. **Guildmaster name and look:** "Distiller Orla Vance", in a pink-hued robe and half apron. Rename freely.
4. **Apprentice task:** Alchemy 50, or 10 Empty Bottles. Same shape as the other craft guilds; change if you want
   Taste ID in it.
5. **World step:** when to run `[ClusterFSeedGuildHalls` and `[ClusterFSeedAlembicHall` on the test world, then live.
   Or set the two `seedOnWorldLoad` settings for the fresh world.
6. **A mule module for the Order?** P70 built 17 modules, one per guild then. The Order has none, and the 2026.10.12.9
   patch note says "seventeen of them, one from each guild", which is now one guild short. Options:
   - a module for the Order (a tonic drip, or a reagent rack that weighs less);
   - or leave it, and reword "one from each guild" in a later note.
7. **Glassblowing:** it "follows Alchemy". Here that means it is a stock book unlock inside the Alchemy menu; nothing
   in this prompt gates or teaches it. F-43's recipe gating (P78) decides whether the Order sells the Glassblowing
   book.
8. **Art plan:** which of the Part D pieces to register first. Recommended: the pillar lamp (on disk), then the
   bubble vat and the partialhue flasks when they download.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, run 2026-10-12 before DONE:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **Code, 9 files:** CHANGELOG.md, VERSION, ClusterFGuildStarterPath.cs, ClusterFGuildSystem.cs, MuleUpgrades.cs,
  GuildDirectoryRowsVerification.cs, GuildStarterPathVerification.cs, and the new ClusterFAlembicGuild.cs and
  AlembicGuildVerification.cs.
- **Docs, 12 files:** this note, and `notes/cc-P77-tools/` (README.txt and the scripts; the PNG previews are
  git-ignored).
- No file is near 5 MB; nothing BLOCKED.

P77 DONE
