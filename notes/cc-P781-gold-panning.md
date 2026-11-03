# cc-P781: gold panning

## In plain words

- **Miners can now pan for gold.** A new NPC, the Compact assayer, stands beside the Miners' Compact Liaison (the New
  Haven mine camp and the Minoc hall). He sells a prospector's pan for 300 gold. With Mining 60 or more, a player
  double-clicks the pan and targets river or lake water. The open sea doesn't work.
- **What a pan finds:** small gold nuggets, from Mining 75 medium ones, from 90 large ones, and now and then one of the
  eight Mondain's Legacy (ML) gems, such as a fire ruby or a white pearl. Each stretch of water gives 5 to 10 finds,
  then needs 10 to 20 minutes to settle.
- **What nuggets are worth:** the assayer buys them for 25, 100 or 350 gold. A Miners' Compact member can instead drop
  them on him for 2, 8 or 25 Compact standing each. Nothing it gives touches skills, stats, power scrolls, bless deeds
  or artifacts.
- **For you:** every number is in `Configuration/gold-panning.json`, made on first start. The one to look at is how
  sheltered the water must be: it allows rivers and lakes, but may also allow some sheltered sea inlets. Sample spots
  are below if you want to check a few in game. Nothing else to deploy or decide.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P781`), image
`sl-modernuo:cc-p781`. Built as our own code. The idea is from **Gold Panning by Hammerhand and Milva, shared by
manwitch** (servuo.dev, `D:\UO\third-party\code\gold-panning`, assessed in cc-P778). Nothing was copied, built or run
from it. They are credited in the CHANGELOG line and here, and the `CODE-INTAKE.md` row now reads
"assess (P778), built (P781)".

## What was built

| Piece | File (`server/customizations/GoldPanning/`) |
|---|---|
| The harvest: water and tile rule, gates, banks, size draw, gem bonus, messages | `GoldPanning.cs` |
| The file and its validation (`gold-panning.json`) | `GoldPanningTable.cs` |
| The prospector's pan (a stock `BaseHarvestTool`) and the three nuggets | `GoldPanningItems.cs` |
| The Compact assayer (a shopkeeper), his shop, the ledger, the world-load seeder, `[ClusterFSeedAssayers`, `[GoldPanningStaff` | `CompactAssayer.cs` |
| Seven facts | `server/tests/Misc/GoldPanningVerification.cs` |
| CHANGELOG `2026.11.03.2`, `VERSION` | repo root |

### Decisions the prompt left open

- **"Compact provisioners":** no such NPC exists in our code (`grep -i provisioner` finds only stock and gargoyle
  provisioners). The new **Compact assayer** is the Compact's provisioner for panning: he sells the pan and buys the
  nuggets. I did not add the pan to the Miners' Guild Store (P760). That would change `reward-stores.json`'s row list
  on worlds that already have the file.
- **Where the assayer stands:** beside each `MinersCompactLiaison` found in the world, two tiles east, or the nearest
  tile that fits. He has no coordinates of his own, because the liaison has two homes in our code: the New Haven mine
  camp (`GuildLocations`, 3498,2744) and the Minoc hall on the swapped map (`ClusterFGuildHallPlacementData`, 2431,532).
  He is placed on every world load (after the load, `Timer.DelayCall(Zero)`) only if none stands within
  `assayer.seedRange` (8) of that liaison, so loading twice places one.
- **Gold or standing:** buying for gold is the stock vendor sell window ("vendor sell"). Standing is given when a
  Compact member drops nuggets on him: the size's standing times the amount, and the nuggets are used up. Anyone else
  is told he only buys for coin, and keeps the nuggets.
- **"Shallow river and lake water only (no ocean)":** see the next section.
- **Art:** stock only. The pan is the pewter plate `0x9D7` in a dull iron hue. The nuggets are the ore piles `0x19B7`,
  `0x19BA` and `0x19B9` in the gold metal hue `0x8A5`. The source used fruit and an ingot pile. Not checked in the
  client by eye.

### The water rule, measured on our map

I read the shard's Trammel map (the swapped Siege of Sosaria files in `player-package/vendor/sos-trammel-map/files`,
the staidx and statics MULs and the map UOP) with a script in the session scratchpad:

- the open sea is **land water** (land tiles `0xA8-0xAB`, `0x136-0x137`): about 12 million tiles in Britannia;
- **862,266 water statics** (`0x1797-0x179C` and the animated runs) lie in Britannia, and 830,456 of the plain ones sit
  over a **sunken bed** (land `0x52-0x64` at z −15), mostly the coastal shallows.

So neither "statics only" (the source's idea) nor "what is under the static" tells a lake from the coast. The rule
used is **enclosure**. The target must be water (a land water tile or a water static), and from it dry land must lie
within `enclosureRange` (24) tiles in at least `enclosureDirections` (6) of the 8 compass directions:

- a lake reaches land all round;
- a river reaches land on both banks and the diagonals, with open water up and down stream;
- a coast reaches land only on its land side, with open sea beyond.

On the map, of water tiles with land beside them (a random sample):

| Reach | Directions needed | Counted as river or lake |
|---|---|---|
| 24 | 8 | 198 of 1,824 |
| **24** | **6 (default)** | **590 of 1,852** |
| 24 | 5 | 1,041 of 1,878 |

Eight shuts out rivers: a river longer than twice the reach finds land in only 6 directions (both banks and the four
diagonals), so the default is 6 (fact 2 checks a drawn river 3 wide and 200 long). **Unverified by eye:** some of the 590
may be sheltered sea inlets. Spots the default counts, to look at in game: 1374,2452; 2915,2789; 513,2416; 694,1696;
2203,503; 2544,696; 4172,3495; 1227,2927. Raising `enclosureDirections` to 7 or 8, or lowering `enclosureRange`,
narrows it.

### Numbers (all in `gold-panning.json`)

| What | Default | Why |
|---|---|---|
| Mining to pan | 60 | the prompt |
| The Mining check per pan | 40 to 110 | about 29% at 60, 86% at 100: a skill that pays off with training |
| Nugget sizes | small 60+ (weight 80), medium 75+ (17), large 90+ (3) | the source's 75/90/105, moved down to the prompt's 60 floor |
| Assayer pays | 25 / 100 / 350 gold | the source's trader came to about 33 gold a small nugget; a little under, since the water refills |
| Or Compact standing | 2 / 8 / 25 each | a requisition pays 40 to 250 standing (P150); a large nugget's worth is a tenth of a top one |
| ML gems | 2% a successful pan, shared by 8 gems (0.25% each), Mining 60 | "a low rate": the source had 2% each for nine (18%) |
| Water banks | 8 x 8 tiles, 5 to 10 finds, refill 10 to 20 minutes | the source's bank (stock Mining's ore banks hold 10 to 34) |
| Range, mounted | 2 tiles; not mounted | the source |
| The pan | 300 gold, 50 uses | a specialist's tool, dearer than a stock pickaxe; 50 uses like the stock harvest tools |

## Rules check

| Rule | How it holds |
|---|---|
| No skill or stat points, power scrolls, bless deeds, property artifacts | The pan finds nuggets (trade goods) and stock ML gems (crafting resources); the assayer pays gold or guild standing. Mining gains by use, as with any harvest; nothing is granted. |
| Rewards usable now and mostly helpful | Gold now; gems for jewelry and imbuing; standing toward Compact ranks. |
| All numbers in a config file | `Configuration/gold-panning.json`, refused whole if bad (unknown setting, a gem that is not an item, a size missing; fact 1). `[GoldPanningStaff reload`. |
| Appears on an existing world by itself, idempotent | The file is written on first start; the assayer seeds beside each liaison on every load, once (fact 7); the pan and nuggets need nothing placed. |
| D40 serialization | Five new saved types, all `[SerializationGenerator(0)]`: the pan (on pinned's `BaseHarvestTool` fields), the abstract `GoldNugget` and its three sizes, and the assayer (a `BaseVendor`). No older data to read, so no migration file (the repo keeps those only for changed schemas). |

## Tests

`GoldPanningVerification`, seven facts (names in the file header): the file; tile and water; skill gates; bank
depletion; price and standing; gems; the seeding. They run the real harvest flow (`GetDefinition`, `CheckHarvest`,
`CheckRange`, `CheckResources`, `FinishHarvesting`) on a `PanSpot`, with the water drawn by the fact through the
`GoldPanning.WaterAt` seam: the test host has no map files.

**Seen failing first** (probe: builder image `sl-uo-builder:cc-P776`, this branch's base, with the change mounted;
`cc-P781-tools/probe.sh`):

- Against the code before the change, the test file does not compile: `ProspectorsPan`, `PanSpot`, `GoldPanningTable`
  and `Server.Engines.GoldPanning` are unknown (`red-probe.txt`).
- First green runs:
  - Four xUnit analyzer errors (`Where` before `Assert.Single` or `Assert.Empty`), fixed (`green-probe1.txt`).
  - Two facts failed because my drawn lake was 30 tiles wide, wider than the 24-tile reach, so its edges read as open
    water. That is the rule working; the lake is now 24 (`green-probe2.txt`).
  - Then 7 of 7 (`green-probe3.txt`).
- A mutant with one break per fact: all **7 facts failed**, each on its own break (`red-mutants.txt`). The breaks:
  1. gem names not checked;
  2. every water tile counted as sheltered;
  3. no Mining gate, and every size open;
  4. nothing taken from the bank;
  5. standing paid for one nugget, not the stack;
  6. no gem roll;
  7. the seeder ignoring an assayer already there.

**Gated build** (`cc-P781-tools/gated-build.ps1`, the `docker-build` lock taken and released): **EXIT=0**, 2,990 tests:
2,984 passed, 6 skipped, 0 failed; all 186 patches applied; the seven `GoldPanningVerification` facts among the passes.
Image `sl-modernuo:cc-p781` (`latest` not touched). Summary in `cc-P781-tools/green-gated-build.txt` (the raw log is
git-ignored). Free memory was checked before each run (once 2.7 GB, back to 6.5 GB after dropping the Docker VM's page
cache). The harness stopped my background wait on the build for low memory partway through; the build itself, started
detached, ran on and finished green, read from its log on disk.

## Deviations and notes for Chase

- The enclosure rule is measured on the map but not checked by eye; sample spots above.
- No in-game proof run on the private shard: not in "Done means", and the facts run the stock harvest flow.
- The assayer's shop prices are read when he is made. After `[GoldPanningStaff reload`, a standing assayer keeps his
  old prices until the next restart (his shop is rebuilt then). The ledger's standing and the pan's finds follow the
  reload at once.
- Version `2026.11.03.2`: P780's branch, not yet merged, already uses `2026.11.03`.

## Files

- ShatteredLegacy: `server/customizations/GoldPanning/` (4 files, new), `server/tests/Misc/GoldPanningVerification.cs`
  (new), `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P781-tools/` (probe and gate scripts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the gold-panning row's status (CRLF kept; backup in the session scratchpad).

P781 DONE
