# cc-P785: chocolatiering recipes in Cooking

## In plain words

- **New in Cooking, under Chocolatiering:**
  - sweet cocoa butter (sugar and cocoa butter, at an oven);
  - from it, the dark, milk and white chocolate nutcrackers, which existed but could not be made until now;
  - chocolate figures of an orc, beetle, bunny, solen or unicorn, made from a bar of chocolate, a mold and a foil
    sheet.
- **Provisioners in every town now sell** the five molds, sacks of sugar, vanilla and foil sheets. Provisioners
  already standing in the world stock them after the next restart; nobody has to place anything.
- **Cocoa butter, cocoa liquor and the three chocolate bars were already in Cooking** (stock ModernUO). Nothing gives
  skill, stats, scrolls or gear.
- **For you:** nothing to do. Prices and recipes are in `Configuration/chocolatiering.json`; a change there takes
  effect at the next restart.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P785`), image
`sl-modernuo:cc-p785` (`latest` not touched). Built as our own code from P778's sketch. The figures and molds are an
idea from **Carlos_ar's "Chocolatiering Adventure"** (`D:\UO\third-party\code\chocolatiering`, reference only, never
built or run). Carlos_ar is credited in the CHANGELOG line and here. Nothing was copied, and the Candy Shack, the
Oompa-Loompas and the tarot cards are not ported, as P778 recommended.

## What was already there (counted, not assumed)

The brief asks for "cocoa butter and liquor from cocoa pulp, the three chocolates, sweet cocoa butter". Reading the
trees showed that most of this already existed:

- **Pinned's `DefCooking.cs` already makes 5 of these**, all `if (Core.ML)`:
  - cocoa butter and cocoa liquor from cocoa pulp, in Ingredients, at an oven (lines 100-112);
  - dark, milk and white chocolate, in Chocolatiering (group 1080001, lines 379-435).
  - Pinned also has the item types (`Items/Food/Chocolatiering.cs`): `CocoaPulp`, `CocoaButter`, `CocoaLiquor`,
    `SackOfSugar`, `Vanilla` and the three chocolates.
  - I did not add these five again. Fact 3 makes each of them, so they are covered by the tests the brief asks for.
- **Sweet cocoa butter is in ServUO, contrary to our header.** Our `CookingCraftRegistrations.cs` header and
  `Nutcrackers.cs` said it was "in neither tree". It is in ServUO pub57: `Items/Consumables/Chocolatiering.cs:164`, and
  the recipe is `Services/Craft/DefCooking.cs:419-422`. Both comments now say so.
- **Cocoa pulp** comes from the cocoa tree plant (pinned `PlantResources.cs:18`). Pinned paragons also drop cocoa
  butter, cocoa liquor, sugar and vanilla at a small chance (`BaseCreature.cs:3255`).
- **No vendor sold sugar, vanilla or foil**, in either tree. ServUO's foil comes from macaws, which we do not have. So
  the provisioner now sells all three; without them the chocolates could not be made.

## What was built

- **New items** (`server/customizations/Chocolatiering/`). Each is `[SerializationGenerator(0, false)]` (D40):
  - `SweetCocoaButter` (0x103D, label 1156401). It is ServUO's item without its quality field, which nothing reads.
  - `ChocolateFigure`: one class with two saved fields, its shape and its chocolate, instead of the package's five
    near-identical classes. It eats like the nutcracker (pinned's `CandyCane`) and is named, for example, "a dark
    chocolate orc".
  - `ChocolateMold`: an abstract base and five stackable molds (orc, beetle, bunny, solen, unicorn), art 0x2DB3,
    hue 1161, as in the package.
  - `SBChocolatier` (`Server.Mobiles`): the provisioner's new stock, read from the table.
- **The recipes** (`ChocolatieringRecipes.Register`) are added at ServerStarted, the `CookingCraftRegistrations` shape,
  into pinned's own Chocolatiering group. Registering is idempotent, and every recipe is ML.
  - **Sweet cocoa butter**: a sack of sugar and cocoa butter, Cooking 15-100, at an oven. This is ServUO's recipe.
  - **Chocolate nutcrackers** (dark 15-100, milk 32.5-107.5, white 52.5-127.5): sweet cocoa butter, a foil sheet and
    cocoa liquor. ServUO's lines 447-463 name `SweetCocoaButter` twice; the second time it sits under the foil sheet's
    label (1124032). Our `GoldFoil` header calls the foil the nutcracker's wrapper, so foil is what was meant, and our
    recipe uses it.
  - **Chocolate figures** are our own recipe: a bar of dark, milk or white chocolate, the shape's mold and a foil
    sheet, at that chocolate's skill range. That makes 15 entries, each shown in its own art and hue.
    - The package used sweet cocoa butter, liquor, a mold and foil for every figure, with only a data flag telling the
      chocolates apart. Ours makes the three chocolate bars matter.
    - A mold is used up by one figure. Pinned's craft engine consumes every resource and has no "required tool" hook,
      so a mold costs only 25 gold.
- **Our nutcracker recipes are now turned on.** Pinned's craft engine has no `CraftItem.Data`, so the nutcracker's kind
  (and a figure's shape and chocolate) is looked up from the craft entry when the item is made
  (`ChocolatieringRecipes.RecipeOf`, called from `ICraftable.OnCraft`). The nutcracker still comes wrapped and takes
  its hue when unwrapped.
  - **No pinned recipe scrolls.** ServUO gates the nutcrackers behind recipe ids 600-602, and nothing on our shard
    hands those scrolls out. Instead, our recipe gating (F-43) puts each entry in the Cooking recipe book for its
    minimum skill's band, like every other dish.
  - Fact 4 checks that each nutcracker is free or in a book band, never behind a scroll. The whole suite's
    `RecipeGatingVerification`, including `BandCountsPerCraftSkill`, still passes with the 19 new entries.
- **No separate bowl.** Everything is Cooking with a pinned cooking tool; the package's chocolatiering bowl is not
  needed.
- **Figures only where our client has the art.** All the art is there (`cc-P785-tools/art-check.txt`, from
  `artcheck.py`, which reads `artLegacyMUL.uop` and `tiledata.mul` in `D:\UO\tool-trials\client-data-copy`):
  - the figures: orc 0x20E0, beetle 0x260F, bunny 0x99A4 ("Easter Bunny EAST"), solen 0x2602, unicorn 0x25CE;
  - the mold 0x2DB3, the nutcrackers 0x9C10-0x9C12, the foil 0x9C48 and the sweet cocoa butter 0x103D;
  - two controls also matched: 0x9DE7 `lamp_blood`, as P783 found, and the gold coin.
  So all five figures are in.
- **Molds and supplies from a provisioner.** `Provisioner-chocolatiering.patch` is one line in
  `Provisioner.InitSBInfo` that adds `SBChocolatier`. It was made with `diff -u` against pinned, checked with
  `patch --fuzz=0` in the builder image, and is listed in `apply-patches.sh`.
  - Pinned runs `LoadSBInfo` on every world load (`BaseVendor.AfterDeserialization`) and on a map change, so
    provisioners already standing in an existing world stock the new rows by themselves, once.
  - The rows and default prices are 25 gold a mold, 6 a sack of sugar, 8 a vanilla and 5 a foil sheet.

## The table and the rules

`Configuration/chocolatiering.json` is written with the defaults on first start. It holds `enabled`, the 19 recipe
rows (each with its key, item, chocolate, figure, min and max skill, oven, and resources with amounts) and the 8
provisioner rows (type, price and stock).

- The recipes are added once, at start, so a changed file takes effect at the next restart.
- A bad file is refused whole and the built-in table is used; every error is printed.
- `[Chocolatiering status` (GameMaster, with `[ShardCommand]`) says what is in force and checks the file on disk.

**Rules check:**
- A recipe can make only `SweetCocoaButter`, `ChocolateNutcracker` or `ChocolateFigure`.
- A resource or a provisioner row cannot be any of these: a deed, a `SpecialScroll` (power, stat cap, alacrity or
  transcendence, so no skill or stat points), a weapon, armour, jewellery, clothing or a talisman (no item
  properties).
- The defaults are food, kitchen goods and molds. The chocolates and figures are candies a player can eat or keep
  now.

## Tests

`server/tests/Misc/ChocolatieringVerification.cs`, five facts:

1. **The table:** the defaults validate, with 19 recipes and 8 provisioner rows, and round-trip as JSON. Each of these
   is refused whole: a recipe making a power scroll, a deed among the resources, a longsword or a stat cap scroll
   among the provisioner rows, and an unknown setting.
2. **Every recipe is in Cooking's Chocolatiering group** with the table's skills, resources and oven flag. Registering
   again adds nothing, and pinned's five are present.
3. **Each recipe makes its item and uses up its resources:** pinned's five and our fourteen others, each figure in its
   shape, chocolate, art and hue. The cook stands beside a stone oven, because pinned checks the oven when the
   resources are used.
4. **The nutcrackers are unlocked:** dark, milk and white each make a wrapped nutcracker of that kind from sweet cocoa
   butter, foil and liquor, with no pinned recipe, each free or in a recipe book band.
5. **The provisioner sells the eight rows** at the table's prices, once each, also after its lists are rebuilt (a map
   change, the same `LoadSBInfo` as a world load).

**Seen failing first** (probe `cc-P785-tools/probe.sh`: builder image `sl-uo-builder:cc-p783`, this branch's base, with
the change mounted; `Provisioner.patched.cs` is pinned's file with the patch applied):

- Against the code before the change, the test file does not compile: `SweetCocoaButter`, `ChocolateFigure`,
  `ChocolatieringTable`, `ChocolatieringRecipes`, `ChocoResource` and `ChocoVendorRow` are unknown (`red-probe.txt`).
- First green run (`green-probe1.txt`): 4 of 5. Fact 3 found pinned's cocoa butter made nothing, because pinned checks
  for an oven when it uses the resources and my test kitchen had none. I put a stone oven beside the cook, and then got
  5 of 5 (`green-probe2.txt`).
- One mutant per fact (`red-mutants.txt`). Each fact failed on its own break:
  1. the refused-kinds check switched off: fact 1 fails;
  2. sweet cocoa butter not added to Cooking: facts 2 and 3 fail;
  3. a figure ignoring its entry (every figure a milk bunny): fact 3 fails;
  4. the nutcracker ignoring its entry (every nutcracker dark): fact 4 fails;
  5. pinned's `Provisioner.cs` without the patch: fact 5 fails.
- The patch was checked on its own with `PATCHCHECK=1 bash probe.sh x`: it is not yet applied in the image, and it
  applies with `--fuzz=0`.

**Gated build** (`cc-P785-tools/gated-build.ps1` runs `docker/uo/build.sh -t sl-modernuo:cc-p785`, under the
`docker-build` lock, which I took and released):
- **EXIT=0**: 3,018 tests, 3,012 passed, 6 skipped, 0 failed.
- All 188 patches applied, including `Provisioner-chocolatiering.patch`.
- The five facts pass, and so do `RecipeGatingVerification` and `CleanUpBritanniaPointsVerification`, both of which
  walk every Cooking entry.
- Summary in `cc-P785-tools/green-gated-build.txt`. The raw log is git-ignored (`*.log`).
- Free memory was 4.9 GB before the probes, and 11.3 GB after dropping the Docker VM's page cache before the gate.

## Deviations and notes for Chase

- **No in-game proof run** on the private shard: it is not in "Done means", and the facts run pinned's real craft flow
  (`CraftItem.CompleteCraft`).
- **The figures and molds are our own recipe and items, not OSI's.** The fidelity principle prefers stock content. The
  prompt asked for figures, so they are recorded here as shard additions; set `enabled` false, or remove the figure
  rows, to have only OSI's nutcrackers.
- **The nutcrackers need no recipe scroll** (OSI and ServUO use recipes 600-602). They follow our book bands instead,
  because nothing here hands out those scrolls.
- **Not done: the BOD rows.** ServUO's Cooking BODs list sweet cocoa butter (small deeds and the 200-point reward row),
  and our `CraftBulkEntries.cs` and `CraftRewardCalculators.cs` drop it as "not on the shard". It is on the shard now,
  so those rows could come back. I left them alone because it changes the BOD tables, which is outside this prompt; it
  would be a small follow-up.
- **The cliloc tool could not read this client's `Cliloc.enu`** (every lookup "not found", even pinned's 1079997). Item
  and recipe names use the clilocs pinned and ServUO already use (1079994-1080003, 1080009, 1156390-1156392,
  1156401), and plain words for the foil sheet, the molds and the figures.
- **Version `2026.11.03.6`.** Main is at `.5`, and P784's branch, not yet merged, is also `.5`. The integrator may need
  to renumber one of them.

## Files

- ShatteredLegacy:
  - new: `server/customizations/Chocolatiering/` (`ChocolatieringItems.cs`, `ChocolatieringRecipes.cs`,
    `ChocolatieringTable.cs`, `SBChocolatier.cs`);
  - changed: `server/customizations/Items/Consumables/Nutcrackers.cs` (`OnCraft` reads the kind; header);
  - changed: `server/customizations/Engines/Craft/CookingCraftRegistrations.cs` (header only);
  - new: `server/patches/Provisioner-chocolatiering.patch`;
  - changed: `docker/uo/apply-patches.sh` (one `apply_patch` line);
  - new: `server/tests/Misc/ChocolatieringVerification.cs`;
  - `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P785-tools/` (the art check, the probe and gate scripts, the patched
  `Provisioner.cs` the probe mounts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the chocolatiering row's call and status now read "built (P785)". A backup of the
  file from before the edit is in this session's scratchpad.

P785 DONE
