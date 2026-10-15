# cc-P56: bank value for Society deeds, harder post-Valorite smelting, context-menu labels (D77, D78, D79)

Builder task, 2026-10-05. Brief: `D:\UO\cc-prompts\cc-P56-smith-economy-and-labels.md`. Engine authority:
`D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today); every pinned file:line
below is against it. `C\` = `D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`, `T\` = `server\tests`,
`PIN\` = `D:\UO\ModernUO-pinned\Projects`. Scratch: `D:\UO\cc-p56-work\` (`model.py` is the Part A model, `make-red.py`
the red tree). Shard HEAD `5f6a194`, tree clean when I started. No clash: nothing else wrote in `D:\ShatteredLegacy` while
I worked. Nothing committed, nothing deployed, no shard restarted, `sl-modernuo:latest` not moved.

## Headlines

1. **All three parts done. Final build `docker\uo\build.sh -t sl-modernuo:cc-p56`: 45/45 patches (the count is unchanged:
   Part B is a third hunk in P55's patch), 785/785 shard facts (749 plus 36 new), image `sl-modernuo:cc-p56` =
   `9d6829869880`.** `sl-modernuo:latest` is `b574b7e9fb95` (P55's image) before and after.
2. **Red then green.** One red tree (`make-red.py`, built `--tests-only` as `sl-modernuo:cc-p56-red`, log `red.log`):
   **29 failed, 756 passed**: 24 of the 36 new cases and the 5 updated ones; the other 12 new cases are guards that
   cannot go red against that tree. Details under "Facts, red then green".
3. **Part A: the bank now pays two parts**, the deed's gold value at the guild's rate times 1.25 (rounded up), plus the
   Seal catalog price of the best item OSI's reward ladder gives for that deed. Checked over **every smith deed shape,
   918**: the bank's lowest roll beats OSI's highest roll with OSI's best item on all of them; cash out is below OSI on all
   of them. Large Valorite exceptional plate: 1,500 Seals before, about 16,900 now (OSI about 16,500: 200,000 gold and a
   Valorite runic). **This is a big rise in Seal income** (small iron 10 regular: 3 to 52), because OSI hands a
   non-member an item on every deed and the old bank paid only the gold. No catalog price changed. Table in Part A.
4. **Found in Part A:** colored-metal **large weapon** deeds banked **3 Seals** before (any metal from Dull Copper to
   Celestial): pinned's gold table pays 0 gold for them (`PIN\UOContent\Engines\Bulk Orders\Rewards.cs:261-296`, the 2-, 5-
   and 6-part rows have only an iron column), and the bank was derived from that gold alone. OSI still gives such a deed
   an item (a large Valorite exceptional sword deed: a Verite runic, 9,000 Seals). Now they bank that item's price.
5. **Part B:** each post-Valorite ore smelts at its metal's tier (Platinum 112.5 .. Celestial 200), through one added
   hunk in `P\Ore-smelt-at-forge.patch`; the satchels inherit it with no copy. **A miner can now harvest an ore they cannot
   smelt:** harvesting any post-Valorite ore needs 100 Mining (`C\ClusterFMiningExtension.cs:98-105`, unchanged), so from
   100 to just under the tier they can mine it and the forge answers "You have no idea how to smelt this strange ore!"
   (501986). Table in Part B.
6. **Part C:** trash bag "Clean Up Britannia" (1151316), pet mimic "Status" (3000132), pack mule "Use" (3006132). **No stock
   cliloc says "Breed"** (nor "Smelt Ore"): the mule sits on "Use" until a cliloc of our own ships; the pipeline that would
   take is proposed in Part C (small: about 30 bytes of entries, one script step, two unknowns to settle in the client).
7. **Brief premises checked:** `SealDivisor` 400, `SealMultiplier` 3, the multipliers x1.5..x5 (`C\ClusterFSmithBODSystem.cs`)
   and the catalog lines (`C\SmithSealCatalogGump.cs:59-106`) are as stated; the pinned forge's default is 50 at
   `PIN\UOContent\Items\Resources\Blacksmithing\Ore.cs:178` (inside `:168-179`); `C\ClusterFMiningExtension.cs:98-105` is
   the 100-Mining harvest table; the three wrong labels are as P55 found them (3006131 "Close", 3006146 "Talk" twice,
   read again from EA's `Cliloc.enu`). The brief's "the large-deed factor" knob does not exist as a separate number: the
   large deed's worth comes from pinned's gold table (large rows) and its type points; nothing in the bank scales large
   deeds on its own.

## What changed (all uncommitted)

Shard (`D:\ShatteredLegacy`):
- `C\ClusterFSmithBODSystem.cs`: Part A (the reward section, `:284-458`).
- `P\Ore-smelt-at-forge.patch` (one hunk added, 3 hunks now) and its comment in `docker\uo\apply-patches.sh` (`:447-451`):
  Part B.
- `C\PackMule.cs`, `C\TrashBag.cs`, `C\PetMimic.cs`: Part C (the three entry classes went from private to internal so the
  facts can name them; nothing else changed in them).
- Facts, new: `T\Misc\SmithBankValueVerification.cs` (A, 17 cases), `T\Items\OreSmeltDifficultyVerification.cs` (B, 16),
  `T\Misc\ContextMenuLabelVerification.cs` (C, 3). Updated: `T\Misc\SmithOrdersTeachVerification.cs` fact 5 (it encoded
  cc-P42's "exactly three times the old Seals"; now the cc-P56 ranges, standing unchanged), and one comment in
  `T\Misc\RegularSmithBODVerification.cs` (H5 said an iron deed's Seals are "the floor of 1, times 3").
- No save shape changed (no migration JSON): Seal balances are stored as before and nothing rescales them (fact A5).

This repo: this note only. `docs\bug-list.md` and `notes\passdown-overseer-2026-10-03.md` were already modified when I
started; not mine, not touched. I did not run `tools\progress.py` (it rewrites `README.md` and `dashboard.html`; say if you
want it in the commit).

## Part A: banking a deed is worth at least what OSI pays a non-member (D77)

**Cause.** The bank paid `SealsForGold(gold)` only: the deed's OSI gold value / 400, rounded, floor 1, times 3 (cc-P42).
That is exactly OSI's gold at the guild's rate and nothing for the item OSI also hands over on every deed
(`PIN\UOContent\Engines\Bulk Orders\BaseBOD.cs:61-69`, `GetRewards`; the item from `Rewards.cs`'s ladder). The item is
most of OSI's value on most deeds (a small iron 10 regular: a 50-Seal shovel against 1.1 Seals of gold), so no single
multiplier could fix it: the item's share of OSI's value runs from a quarter (a large Valorite ring exceptional: 500 of 2,008, the lowest of all 918 shapes) to 100% (a
colored large weapon deed, no gold at all). The fix had to follow the item.

**Change** (`C\ClusterFSmithBODSystem.cs`):
- `SealsForGold` (`:322`): `max(1, ceil(gold x BankGoldShare x 3 / 400))`, `BankGoldShare = 1.25` (`:319`). **Why 1.25:**
  pinned's `ComputeGold` rolls between 9/10 and 10/9 of the table (`Rewards.cs:497-498`), and the bank rolls its own gold
  separately; 1.25 x 0.9 = 1.125 is above 1.111, so the bank's lowest roll beats OSI's highest. 1.2 fails 236 of the 918
  shapes in the model; 1.25 fails none. Rounding up (was to nearest, in steps of 3) removes the rounding loss that otherwise
  broke the floor by fractions of a Seal on 59 shapes. `SealMultiplier` (3) itself is unchanged, because
  `C\ClusterFSmithCommissions.cs:563, :790` multiply commission pay by it.
- `OsiRungSeals` (`:330-354`) and `OsiItemSeals` (`:361`): OSI's 23 ladder rungs (pinned `SmithRewardCalculator` Groups,
  `Rewards.cs:354-400`), each at the best catalog price of the items it can give; `LookupRewards`' rule (the highest rung
  reached). Unpriced items (P55's rule, extended): the midpoint of the best priced item on the nearest priced rung below and
  above. Fact A1 rebuilds the whole table from the live ladder and catalog, so a catalog change not carried here fails the
  build.
- `ItemSealsForDeed` (`:417`) and `ComputeGuildReward` (`:427`): bank = gold part + item part, small and large alike.
- **Post-Valorite** (`GoldEquivalentForSeals`, `:395`, `:405`; `ItemSealsForDeed`): pinned knows no post-Valorite
  material, so OSI pays a non-member **iron's** gold and an item with no material points for them (`Rewards.cs:438-441`,
  `:486-488`). Gold part: the larger of that and the Valorite-equivalent gold x multiplier (unchanged since cc-P42). Item
  part: the larger of the deed's own rung and the same deed's rung in Valorite. **The multipliers are kept, as numbers and as
  to what they multiply** (the gold part). The item part is not multiplied, argued: OSI's ladder ends at the Valorite
  runic, and multiplying the item by x5 would make one large Celestial exceptional deed worth about 84,000 Seals, five and a
  half Valorite runics, which is what cc-P46 Part E raised the runic prices to stop. With the item unmultiplied it banks
  about 24,400 (1.6 Valorite runics). The alternative's numbers are in "Decisions" if you want it.
- Standing and the skill checks: unchanged.
- Catalog prices: **unchanged.** None looked clearly out of line against OSI's ladder; every comparison reads them live.

**The table** (one deed of each row; "OSI" = what a non-member gets at a regular smith: gold at the middle of its roll at
the guild's rate, 3 Seals per 400 gold, plus the item at its catalog price; bank before = cc-P55's formula at the middle of
the roll; bank after = the build's own number at the middle, then its whole range; cash out after = cc-P55's half gold
plus 1 in 40 of the item, unchanged formula. Printed by fact A3 from the live code, `D:\UO\cc-p56-work\detail.log`):

| Deed | OSI pays | OSI in Seals | Bank before | Bank after (range) | Cash out after |
|---|---|---|---|---|---|
| Small iron 10 regular | 151 gold + Sturdy Shovel (50) | 51.1 | 3 | **52** (52 to 52) | 1.8 |
| Small iron 20 exceptional | 503 gold + gloves +3 (300) | 303.8 | 3 | **305** (305 to 306) | 9.4 |
| Small Gold 20 exceptional | 3,017 gold + Copper runic (550) | 572.6 | 24 | **579** (576 to 582) | 25.1 |
| Small Valorite 20 exceptional | 12,067 gold + 115 scroll (150) | 240.5 | 90 | **264** (252 to 275) | 49.0 |
| Large iron plate 20 exceptional | 20,111 gold + Copper runic (550) | 700.8 | 150 | **739** (719 to 759) | 89.2 |
| Large Valorite ring 20 exceptional | 201,111 gold + Ancient hammer +30 (500) | 2,008.3 | 1,500 | **2,386** (2,188 to 2,584) | 766.7 |
| Large Valorite plate 20 exceptional | 201,111 gold + Valorite runic (15,000) | 16,508.3 | 1,500 | **16,886** (16,688 to 17,084) | 1,129.2 |
| Large Valorite swords 20 exceptional | 0 gold + Verite runic (9,000) | 9,000.0 | 3 | **9,001** (9,001) | 225.0 |
| Small Platinum 20 exceptional | 503 gold + gloves +3 (300) | 303.8 | 135 | **470** (452 to 488) | 9.4 |
| Large Platinum plate 20 exceptional | 20,111 gold + Copper runic (550) | 700.8 | 2,250 | **17,829** (17,532 to 18,125) | 89.2 |
| Small Celestial 10 regular | 151 gold + Sturdy Shovel (50) | 51.1 | 45 | **407** (401 to 413) | 1.8 |
| Small Celestial 20 exceptional | 503 gold + gloves +3 (300) | 303.8 | 450 | **866** (807 to 925) | 9.4 |
| Large Celestial plate 20 exceptional | 20,111 gold + Copper runic (550) | 700.8 | 7,500 | **24,428** (23,438 to 25,417) | 89.2 |

"OSI pays ... item" is the best item of the deed's rung (a rung can roll a cheaper one: the 200 rung gives a Gargoyle's
Pickaxe, a Prospector's Tool or +3 gloves); the bank pays the best, so the floor holds for every roll of the item too.
Post-Valorite rows: OSI pays iron's rewards for them (no material points), so their bank was already above OSI before
except small Platinum exceptional (135 against 304); the change still raises them because the Valorite-equivalent item
part is added.

**The unpriced items and their values** (the ladder as fact A1 printed it): mining gloves +1 175 (between the pickaxe 50
and +3 gloves 300); colored anvil and 105 scroll 450 (Shadow Iron runic 350 and Copper runic 550); anvil and 110 scroll at
675 points 675 (550 and Bronze 800); 115 scroll 150 (Ancient hammers +10 100 and +15 200, P55's value kept); 120 scroll
1,900 (+15 hammer 200 and Gold runic 3,600). The 120 scroll's midpoint is wide; it only sets the 900 rung (some large
exceptional deeds in the middle metals), where the gold part is tens of thousands of gold.

**Every deed:** fact A2 builds all 918 shapes (small and the eight large sets, 10/15/20, regular/exceptional, 17
materials) and checks bank at the lowest roll >= OSI at the highest roll with its best item, and OSI > cash out. 918
checked, 0 failures; the tightest margin is 0.12 Seals (small iron 15 regular).

**Facts** (`T\Misc\SmithBankValueVerification.cs`): A1 the ladder equals the live ladder at live catalog prices; A2 all
918 shapes; A3 (13 rows) the table above at the middle roll; A4 every post-Valorite metal banks at least the metal below it
and Valorite, for every shape; A5 a saved balance of 1,234 Seals reads back as 1,234 and a turn-in adds exactly the deed's
Seals (1,234 + 264 = 1,498).

## Part B: post-Valorite ore is harder to smelt (D78)

**Cause.** Pinned's forge sets the smelt difficulty by a switch that lists Dull Copper (65) to Valorite (99) and gives
everything else 50 (`PIN\UOContent\Items\Resources\Blacksmithing\Ore.cs:168-179`); it refuses only when the difficulty is
above 50 and above the smelter's Mining (`:184-188`). So Platinum to Celestial smelted at any skill with the check 25 to 75.

**Change.** One hunk added to `P\Ore-smelt-at-forge.patch` (`--fuzz=0`, now three hunks; the brief's preferred seam, argued
in `apply-patches.sh:447-451`): before the switch's default,

    _ when ClusterFMetalTiers.RequiredSkill(m_Ore._resource) > 99.0 => ClusterFMetalTiers.RequiredSkill(m_Ore._resource),

`RequiredSkill` (`C\ClusterFMetalTiers.cs:30-49`) is above 99 only for the eight post-Valorite metals, so iron and the
stock colors fall through to the switch's own values exactly as before. The forge's usual window applies around the new
difficulty (`difficulty - 25` to `+ 25`, `Ore.cs:181-182`), so at the tier the chance is one half, as Valorite's is at 99.
The satchel calls this same step (P55's `SmeltAt`), so it inherits the change with no copy. Rejected: a second patch on the
same method (two seams for one switch); a check in the satchel only (the forge would still smelt Celestial at 50).

| Ore | Harvest (Mining, unchanged) | Smelt before | Smelt now | Check window now |
|---|---|---|---|---|
| Platinum | 100 | 50 (any skill) | 112.5 | 87.5 to 137.5 |
| Toxic | 100 | 50 | 125 | 100 to 150 |
| Blaze | 100 | 50 | 137.5 | 112.5 to 162.5 |
| Frost | 100 | 50 | 150 | 125 to 175 |
| Obsidian | 100 | 50 | 162.5 | 137.5 to 187.5 |
| Mythril | 100 | 50 | 175 | 150 to 200 |
| Adamantium | 100 | 50 | 187.5 | 162.5 to 212.5 |
| Celestial | 100 | 50 | 200 | 175 to 225 |
| Iron / Dull Copper .. Valorite | stock | 50 / 65 .. 99 | unchanged | unchanged |

**Harvest against smelt.** Every post-Valorite ore harvests at 100 Mining (`C\ClusterFMiningExtension.cs:98-105`, left as
the brief says). So yes: a miner between 100 and the tier can dig the ore and cannot smelt it. At the forge they get the
stock line 501986 "You have no idea how to smelt this strange ore!" and the pile is left whole (nothing lost); through a
satchel, the same line per pile and the pile counted "left unsmelted" in the satchel's summary. They can still sell or
store it, or smelt it later. If you want harvest and smelt to line up, the harvest table's `reqSkill` is the knob (not
touched here).

**Facts** (`T\Items\OreSmeltDifficultyVerification.cs`): B1 (8 ores) a tenth under the tier: refused, 10 ore left, no
ingots; at the tier a 0.49 roll smelts a large pile of 10 into 20 ingots and a 0.51 roll burns it to 5 (the 0.5 chance);
B2 the satchel at 112.4 leaves a Platinum pile whole, at 112.5 smelts it into the satchel; B3 (6) iron at 0 and 50 is
attempted (not refused), Dull Copper refused at 64.9 and smelted at 65, Valorite refused at 98.9 and smelted at 99.

## Part C: context-menu labels (D79)

Read from EA's `D:\UO\UltimaOnlineVanilla\Cliloc.enu` (124,000 entries) with `notes\cc-P29-tools\cliloc.py`, as P52 B and
P55 C did. Pinned sends any number above 0x7FFF as is and adds 3,000,000 to one at or below it
(`PIN\Server\ContextMenus\ContextMenuEntry.cs:39-48`).

| Entry | File:line | Was | Now | Client text now | Why this one |
|---|---|---|---|---|---|
| Pack mule breed (`PackMuleBreedEntry`) | `C\PackMule.cs:237` | 3006131 "Close" | **3006132** | "Use" | No entry reads "Breed", "Mate" or "Pair" (searched every entry with those words; the only hits are a quest title "They're Breeding Like Rabbits" and "(Breed: Cu Sidhe)"). "Use" is the nearest honest stock word; the target cursor then says what it is for. The old comment said 6131 was "Tame" (3006130 is). |
| Trash bag dump (`DumpEntry`) | `C\TrashBag.cs:121` | 3006146 "Talk" | **1151316** | "Clean Up Britannia" | The bag's gump dumps for Clean Up Britannia points; OSI's own name for the system. Considered: 1151298 "Appraise for Cleanup" (that is the appraise target, already used by `CleanUpTrash.cs:148`). No "Dump" or "Empty" entry. |
| Pet mimic status (`CheckStatusEntry`) | `C\PetMimic.cs:1610` | 3006146 "Talk" | **3000132** | "Status" | Exact. Also exists: 1072845 "Status". |
| Pet mimic feed (`FeedEntry`) | `C\PetMimic.cs:1591` | 3006135 "Eat" | unchanged | "Eat" | Near enough (P55). |
| Ore satchel (`SmeltOreEntry`) | `C\CompactOreSatchel.cs` | 3006143 "Smelt" | unchanged | "Smelt" | No "Smelt Ore" (P55). |

**Proposal for Chase: our own clilocs ("Breed", "Smelt Ore", later "Metal Familiarity"),** under
`notes\client-policy-2026-10-02.md` (we ship our patches, applied to EA's files on the player's machine, and our own TazUO
build):
- **What:** a step in the player package that reads the player's `Cliloc.enu`, adds our entries, and writes the result
  where the client reads it. Our reader exists (`cliloc.py`, a port of pinned's `Localization.cs:88-143` and
  `BwtDecompress.cs`); the writer is the same format without the compression (int 2, short 1, then per entry: int number,
  byte flag, ushort length, UTF-8 text).
- **Size:** the entries are tiny: "Breed" and "Smelt Ore" are 7 + 5 and 7 + 9 bytes, about 30 bytes with a third. The file
  written is the whole table: EA's is 5,078,062 bytes compressed and 5,061,666 uncompressed (measured: the BWT compression
  saves nothing on this file), so writing it uncompressed costs no space. The package itself would ship only our entries
  (a few hundred bytes of JSON or a .txt) and the script, not EA's file.
- **Numbers:** a block of our own that EA will not reach: EA's numbers stop at 1,166,081 below 3,000,000 and nothing is
  used from 1,200,000 to 2,999,999 or above 3,011,032 (counted). A block at 1,900,000 would do. Pinned already sends such
  numbers on the newer packet (`ContextMenu.cs:51-54`).
- **Unknowns to settle before building it** (both from P52 B, still open): whether TazUO's `-uofilesoverride` covers
  `Cliloc.enu`, and whether the client accepts an uncompressed file there. With our own TazUO build the second is ours to
  make true. Each EA client patch that changes `Cliloc.enu` means re-running the step (it patches the player's copy, so
  it picks up EA's changes for free).
- **Work estimate:** the script step and the writer are small (a day with testing on a clean machine); the client
  questions are the risk. Meanwhile the mule stays on "Use" and the satchel on "Smelt".

**Facts** (`T\Misc\ContextMenuLabelVerification.cs`; the number each entry sends, from the object's real menu): C1 an owned
pack mule's menu has the breed entry at 3006132 and no 3006131; C2 a trash bag in the pack has the dump entry at 1151316 and
no 3006146; C3 a pet mimic's status entry is 3000132, no 3006146, and "Eat" (3006135) is still there.

## Facts, red then green

36 new cases in three files; 5 old cases updated (`SmithOrdersTeachVerification` fact 5). Red tree
(`D:\UO\cc-p56-work\make-red.py`): A the bank's cc-P55 formula back (rounded, steps of 3, no item part, post-Valorite on the
multiplied Valorite gold alone) and one ladder rung stale (Valorite runic at 5,000); B the cc-P55 forge patch byte for
byte (every post-Valorite ore at 50); C the three numbers back to 6131, 6146, 6146.

Red result: 45/45 patches; 785 tests, **29 failed, 756 passed**. The 29 are 24 of the 36 new cases plus the 5 updated
ones; the 12 new cases that stay green there are guards over behaviour the red tree does not undo (listed).

| Fact | Red | Green |
|---|---|---|
| A1 ladder at catalog prices (red tree: one stale rung) | red | green |
| A2 all 918 shapes | red | green |
| A3 rows: small iron 10 reg, small iron 20 exc, small Gold, small Valorite, large iron plate, large Valorite ring, plate, swords, small Platinum, small Celestial 10 reg (10) | red | green |
| A3 rows: large Platinum plate, small Celestial 20 exc, large Celestial plate (3) | **never red**: the old post-Valorite bank was already above OSI's iron-level pay for these | green |
| A4 metals in order | **never red**: the old multipliers already ordered them; a guard on the new formula | green |
| A5 balances untouched | **never red by design**: nothing rescales a balance; a guard | green |
| B1 (8 ores) | red | green |
| B2 at 112.4 | red | green |
| B2 at 112.5 | **never red**: the old forge smelts Platinum at any skill | green |
| B3 stock ores (6) | **never red by design**: stock unchanged, a guard | green |
| C1, C2, C3 | red | green |
| Updated: `SmithOrdersTeachVerification` fact 5 (5) | red (old formula) | green |

## Builds

| Build | Command | Result |
|---|---|---|
| 1 | `build.sh -t sl-modernuo:cc-p56 --builder-tag sl-uo-builder:cc-p56 --tests-only` | 45/45 patches; **785/785** |
| detail | the same test command `build.sh` runs, in `sl-uo-builder:cc-p56`, filtered to the four classes, `verbosity=detailed` (no image made; only to read the facts' printed numbers) | 41/41; numbers in `detail.log` |
| red | red tree, `-t sl-modernuo:cc-p56-red --builder-tag sl-uo-builder:cc-p56-red --tests-only` | 45/45 patches; 785 tests, **29 failed**, 756 passed |
| final | `build.sh -t sl-modernuo:cc-p56` | **45/45 patches, 785/785, image `9d6829869880`**; `latest` still `b574b7e9fb95`. The builder stage was a BuildKit cache hit on build 1 (same inputs), so the "45 patches applied" line is build 1's; the tests ran again (785/785) |

Docker answered throughout. Builder tags made: `sl-uo-builder:cc-p56`, `sl-uo-builder:cc-p56-red`.

## Deviations and decisions for you

Register lines (next free D-119):
- **D-116 (amend), cc-P56 A:** banking now pays the deed's gold value x 1.25 at the guild's rate plus the Seal catalog
  price of the best item OSI's ladder gives for the deed, so banking is worth at least what OSI pays a non-member for every
  deed; cash out unchanged.
- **D-119 Ours (cc-P56 B, Chase 2026-10-05).** Post-Valorite ores smelt at their metal's tier (Platinum 112.5 .. Celestial
  200, `ClusterFMetalTiers`), with the forge's usual 25-point window; stock gives every ore it does not know 50. Harvest stays
  at 100, so a miner can dig an ore they cannot yet smelt. | harder top metals | `visible` | `cc-P56` B
- **D-120 Ours (cc-P56 C).** Context-menu labels on stock clilocs that are not the words we would choose: pack mule breed
  "Use", trash bag "Clean Up Britannia". Reverses when a client cliloc pipeline ships (Part C proposal).

Decisions:
1. **Seal income is much higher now** (headline 3). If it is too much, the honest knobs are the catalog prices (raise them
   all together, which keeps the bank/OSI relation, since the item part reads them) or `BankGoldShare` (not below 1.25,
   or the floor breaks on rolls).
2. **Post-Valorite item part unmultiplied** (Part A). The alternative (multiply the whole bank): large Platinum exceptional
   plate about 25,300, large Celestial about 84,400, small Celestial 10 regular about 1,810. Your call.
3. **Colored large weapon deeds** now bank their OSI item (headline 4). Post-Valorite large weapon deeds bank the same in
   every metal (the multipliers have no gold to multiply: pinned's table has none for them in Valorite). If those should
   climb with the metal too, they need a gold value of our own.
4. **The 120 power scroll's value** (1,900, a midpoint across a wide gap) is the softest number in the ladder. It only sets
   the 900 rung.
5. **Part C:** say whether to build the cliloc pipeline; "Use" is the mule's label until then.
6. **Harvest vs smelt** (Part B): left as briefed; one line in `ClusterFMiningExtension.cs` if you want them aligned.

## For Chase

Deploy to the test shard first:

1. `docker tag sl-modernuo:cc-p56 sl-modernuo:latest`
2. `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down`
3. `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`

In game on the test shard (a Society member smith; `[SetSkill Blacksmith 120`, `[SetSkill Mining 100` as needed):

4. **Bank value (D77):** note your Seals at the Society guildmaster. Fill and hand in a small iron deed (`[add SmallSmithBOD`
   until you get one, or the guild's own Small order): "Society of Smiths: +n standing, +52 Smithing Seals banked." (an
   iron 10 regular; about 178 for an iron 20 regular, about 305 for an iron 20 exceptional). Your old balance is still there
   plus that.
5. **Non-member comparison:** on a character not in the Society, hand the same kind of deed to a town Blacksmith: gold to
   your bank and the bulk-order rewards gump (OSI's 2016 rules, cc-P122; was "gold and an item, as before").
6. **Ask mode:** set "Completed orders" to "Ask each time" at the guildmaster; hand in a deed: the Bank button shows the new
   Seal figure.
7. **Smelting (D78):** `[SetSkill Mining 112.4`, `[add PlatinumOre 10`, stand by a forge, double-click the ore and target the
   forge: "You have no idea how to smelt this strange ore!" and the ore stays. `[SetSkill Mining 112.5` and try again: it
   smelts about half the time (a failure burns half the pile).
8. **Satchel:** `[add ReinforcedOreSatchel`, put the Platinum ore in it, at 112.4 choose Smelt by the forge: the pile is
   "left unsmelted"; at 112.5 it smelts into the satchel.
9. **Stock ores:** `[add ValoriteOre 10` at 98.9 Mining: refused; at 99: smelts. Iron smelts at any skill as before.
10. **Labels (D79):** `[add TrashBag` into your pack, single-click it: "Clean Up Britannia" (opens the dump gump). `[add
    PetMimic`, single-click: "Eat" and "Status" (Status opens the status gump). Tame a pack mule (or `[add PackMule` and tame it),
    single-click it: "Use" (starts breeding: "Target the ... pack mule").
11. Promote to `docs\`: close D77, D78, D79 in `bug-list.md` (D79 with the "Breed" label left on "Use" pending the cliloc
    decision); amend D-116 and add D-119, D-120 in `fidelity-principle.md`.

P56 DONE
