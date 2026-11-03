# cc-P782: grave digging

## In plain words

- **Players can dig graves for reagents.** Tinkers now sell a gravedigger's spade for 40 gold. A player double-clicks it
  and targets a grave in a cemetery (Britain, Vesper, Cove, Moonglow, Jhelom, Yew, the Chapel of Saint Lucia and about
  fifteen more graveyards on our map). Graves outside cemeteries are refused.
- **What a dig finds rises with Forensic Evaluation:** bones for anyone; from 50 also fertile dirt; from 75 the
  necromancer's reagents (grave dust, nox crystal, bat wing, daemon blood, pig iron). About 1 dig in 25 (from 50 skill)
  also turns up a bonus: a rib cage or bone pile, a gravestone for a house, from 75 a low treasure map, from 90 a
  wooden coffin. No magic gear, nothing blessed.
- **Each grave is its own little store**, shared by everyone: 6 to 12 digs, then it rests 30 to 60 minutes. There is no
  karma or criminal penalty for digging.
- **For you:** every number, including which places count as cemeteries, is in `Configuration/grave-digging.json`, made
  on first start. Nothing else to deploy or decide.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P782`), image
`sl-modernuo:cc-p782`. Built as our own code. The idea is from **Grave Digging by Massapequa** (servuo.dev,
`D:\UO\third-party\code\grave-digging`, assessed in cc-P778). Nothing was copied, built or run from it. Massapequa is
credited in the CHANGELOG line and here, and the `CODE-INTAKE.md` row now reads "assess (P778), built (P782)".

## What was built

| Piece | File |
|---|---|
| The harvest: cemetery gate, nodes, finds by tier, the bonus roll, messages, `[GraveDiggingStaff` | `server/customizations/GraveDigging/GraveDigging.cs` |
| The gravedigger's spade (a stock `BaseHarvestTool`) | same file |
| The file and its validation (`grave-digging.json`) | `server/customizations/GraveDigging/GraveDiggingTable.cs` |
| `LootBoxRoller.MakeRow`: one loot table row made outside a box, for the bonus roll | `server/customizations/LootBoxes/LootBoxRoller.cs` (15 lines) |
| Tinkers stock the spade, beside the shovel | `server/patches/SBTinker-gravediggers-spade.patch` (new), `docker/uo/apply-patches.sh` |
| Seven facts | `server/tests/Misc/GraveDiggingVerification.cs` |
| CHANGELOG `2026.11.03.3`, `VERSION` | repo root |

No stock file is replaced: the source replaced pinned's `HarvestTarget.cs` to catch grave tiles inside Mining. Here the
spade is its own tool on its own harvest system, so `HarvestTarget` calls our `StartHarvesting` unchanged.

### How it works, and the decisions behind it

- **Graves:** the source's grave tiles, `0xED3`, `0xEDF`, `0xEE0-0xEE2`, `0xEE8` (the mounds; headstones are not dug).
  On the shard's Trammel map there are 692 of them (counted from the swapped map's statics).
- **"Cemetery regions only":** a grave counts if it is in a region whose name holds "Graveyard" or "Cemetery", or in
  one of the file's cemetery areas.
  - Our region files name only two cemeteries on Trammel: Britain Graveyard (10 graves inside) and Vesper Graveyard
    (48). Most graves lie elsewhere.
  - So the default areas are every cluster of 8 or more graves on the map: graves within 8 tiles of each other, the box
    padded by 3. That makes 24 areas holding 594 of the 627 graves in Britannia, each named after the nearest place in
    `Locations/trammel.json`.
  - They include Jhelom, Cove, Moonglow, Yew and Vesper cemeteries, the Chapel of Saint Lucia, the Dhampire ruins, and
    a large graveyard of six clusters around 2572-2633, 3094-3164 that has no named place nearby.
  - The areas are only checked by the dig. They are **not registered as regions**, so no town's guards, housing or
    music change.
  - Felucca uses the same map file (P675), so each area names both facets.
- **"A node per grave, not per player":** pinned's `HarvestBank` with a 1 x 1 bank, so each grave tile is its own node,
  shared by every digger. The source made a node at the player's feet when none was near, so stepping aside gave endless
  digs. Defaults: 6 to 12 digs, then 30 to 60 minutes to refill.
- **Tiers** (the source's): under Forensics 50, bones (1 to 3); from 50, bones (2 to 4) or fertile dirt (1 to 2); from
  75, bones, fertile dirt, grave dust, nox crystal, bat wing, daemon blood or pig iron, by weight.
- **The Forensics check:** from −25 to 100, so 20% at 0, 60% at 50 and certain at 100. Anyone can dig with a spade;
  Forensics makes it pay. Forensics gains by use, as with any harvest.
- **"A small bonus roll through our loot tables":**
  - Rate: 4% of successful digs, from Forensics 50.
  - The entries are written in the loot boxes' own row format (`PoolEntry`), checked by the loot boxes' own
    `CheckEntry` and made by their own factory (`LootBoxRoller.MakeRow`, a 15-line public door onto the private `Make`).
  - An entry's `minGrade` is the digger's Forensics grade: 1 from 0, 2 from 50, 3 from 75, 4 from 90.
  - Defaults:
    - a rib cage and a bone pile (pinned's, both cut into bones with scissors: the source's "human bones");
    - a gravestone `0x1165` and a weathered headstone `0xED7` as house decor (`@Decor`), from 50;
    - a treasure map from 75 (`@TreasureMap` level 1; the shard's revamp makes that a Stash, its lowest);
    - pinned's wooden coffin deed from 90.
- **"Grave decor deeds":** only the coffin is a deed. A gravestone is a single tile, so it comes as a decor item to lock
  down (the loot boxes' `LootDecor`), not as a deed. Our own gravestone deed would have been a new addon type for no
  gain.
- **Who sells the spade:** the prompt names no seller. Tinkers sell shovels, so they sell the spade beside them, through
  a one-line patch to pinned's `SBTinker.cs` (made with `diff -u` and checked with `patch --fuzz=0`, as the animal
  trainer's elixir was). Price 40 gold, 50 uses.
- **No penalty:** no karma, criminal flag or guards (the prompt: not for now).

## Rules check

| Rule | How it holds |
|---|---|
| No skill or stat points, power scrolls, bless deeds, property artifacts | Finds are stock resources and reagents. The bonus list may name only plain item types and four specials (`@TreasureMap`, `@Decor`, `@Reagents`, `@Seed`): a file naming gear (weapons, armour, jewels, clothing, talismans), a power scroll, a bless deed or any other special (`@MagicGear`, `@SlayerWeapon`, `@RunicTool` and the rest) is refused whole. Anything blessed is given unblessed (pinned's coffin deed is made blessed). Fact 6. |
| Rewards usable now and mostly helpful | Reagents and fertile dirt for necromancy, gardening and herbalism; bones for tailoring; a treasure map to dig up; house decor. |
| All numbers in a config file | `Configuration/grave-digging.json`: tiles, keywords, areas, node, range, tiers, the bonus (chance, minSkill, entries, grade thresholds), the spade. `[GraveDiggingStaff reload`. |
| Appears on an existing world by itself, idempotent | The file is written on first start. Tinkers' stock is code, so every tinker sells the spade on the next start. Nothing is placed in the world. |
| D40 serialization | One new saved type, `GravediggersSpade`, `[SerializationGenerator(0)]` on pinned's `BaseHarvestTool` fields. Nodes (`HarvestBank`) are not saved, as pinned's are not. No migration file is needed. |

## Tests

`GraveDiggingVerification`, seven facts (names in the file header): the file; the region gate; node depletion; the
tiers; the bonus odds; the rules; the tinkers' spade. They run the real harvest flow (`GetDefinition`, `CheckHarvest`,
`CheckRange`, `CheckResources`, `FinishHarvesting`) on a `GraveSpot`. The region gate is tested both ways: a default area
on Trammel and Felucca, and a registered region named "p782 Test Graveyard".

**Seen failing first** (probe: builder image `sl-uo-builder:cc-p780`, this branch's base, with the change mounted;
`cc-P782-tools/probe.sh`):

- Against the code before the change, the test file does not compile: `GravediggersSpade`, `GraveSpot`,
  `GraveDiggingTable` and `Server.Engines.GraveDigging` are unknown (`red-probe.txt`).
- First green run, 5 of 7 (`green-probe1.txt`):
  - fact 6 expected a level 1 map, but the shard's treasure revamp turns classic level 1 into a Stash (level 0). The
    fact now asserts the Stash;
  - fact 7 fails in every probe, because probes do not apply patches. That is its red; it passes in the gated build.
- Second run: 6 of 7, fact 7 as above (`green-probe2.txt`).
- A mutant with one break per fact (`red-mutants.txt`): **all 7 failed**, each on its own break. The breaks:
  1. the bonus allowed-list and gear check skipped;
  2. every place counted as a cemetery;
  3. nodes 8 x 8 instead of one per grave;
  4. the lowest tier always;
  5. the bonus minSkill ignored;
  6. blessed items given as made;
  7. no patch.

**Gated build** (`cc-P782-tools/gated-build.ps1`, the `docker-build` lock taken and released): **EXIT=0**, 3,000 tests:
2,994 passed, 6 skipped, 0 failed; all 187 patches applied, the new `SBTinker-gravediggers-spade.patch` among them; the
seven `GraveDiggingVerification` facts among the passes, fact 7 (the tinkers' spade) included now that the patch is in.
Image `sl-modernuo:cc-p782` (`latest` not touched). Summary in `cc-P782-tools/green-gated-build.txt` (the raw log is
git-ignored). Free memory was 5.4 GB and 8.8 GB before the probe and the build.

## Deviations and notes for Chase

- The cemetery areas come from the map's grave clusters, not from regions: only Britain and Vesper have graveyard
  regions in our files. Graves in clusters of fewer than 8, and Felucca-only graveyards, are not covered unless their
  region's name says so. Add a box to `areas` to open one; `[GraveDiggingStaff here` tells staff whether a spot counts.
- Gravestones come as lockdown decor, not deeds; the coffin is a deed.
- No in-game proof run on the private shard: not in "Done means", and the facts run the stock harvest flow.
- The tinkers' spade price is read when a tinker's shop is built, so a reload changes it at the next restart.
- Version `2026.11.03.3`: main has `2026.11.03` (P780), and P781's branch has `2026.11.03.2`.

## Files

- ShatteredLegacy:
  - new: `server/customizations/GraveDigging/` (2 files), `server/patches/SBTinker-gravediggers-spade.patch`,
    `server/tests/Misc/GraveDiggingVerification.cs`;
  - changed: `server/customizations/LootBoxes/LootBoxRoller.cs`, `docker/uo/apply-patches.sh`, `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P782-tools/` (probe and gate scripts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the grave-digging row's status (CRLF kept; backup in the session scratchpad).

P782 DONE
