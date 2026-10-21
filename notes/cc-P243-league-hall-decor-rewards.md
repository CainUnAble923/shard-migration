# cc-P243: Hall decor rewards in the League shop (trophies, statues, display cases)

2026-10-21, the Bronze Golem (Opus), branch golem/Bronze/P243 of both repos. Prompt: `cc-P243-league-hall-decor-rewards.md`.
Not committed (the Golem commits after DONE). Both repos were clean at the start. P229 is merged (its shop is on this
branch: `LeagueShop/LeagueShop.cs`, `LeagueShopGumps.cs`, the 2026.10.21.3 patch notes). Nothing was run against any
world, nothing was deployed, and the package was not built or published.

## Headlines

- **The League shop has a Hall page with 19 pieces of house decor, opened by AP and bought with Renown** through P229's
  own `LeagueShop.Purchase`. AP is checked, exactly the price is taken, and LifetimeRenown and League rank never move.
  - Rows are in AP-tier order, greyed until AP opens them, and every purchase goes through the confirm step.
  - Every price and AP gate is a setting (`clusterf.leagueHall.<piece>.ap`, `.renown`).
- **The pieces:**
  - RedRooster's display cases (4): glass, books, gems, dyeable books. The shelf and the insert dye apart, as he built
    them.
  - Hestia's statues (4): winged dragon, dark dragon, jeweled dragon, grinning gargoyle.
  - Hestia's wall trophies (4): minotaur, sabertooth, troglodyte, skull.
  - Archaaz's wall trophies (5) and mounted heads (2): titan, oni, ophidian matriarch, terathan matriarch,
    paroxysmus; titan and oni heads.
  - 38 art IDs, 15592-15629, both facings where the author drew them.
- **Each piece comes as a deed that places it only in a house the buyer owns.** The deed follows pinned's patterns:
  - placement as `BaseAddonDeed`/`BaseAddon.CouldFit`, which needs `house.IsOwner`;
  - the facing choice as `MinotaurStatue`'s;
  - the wall rule as `TrophyDeed`'s;
  - chopping gives the deed back.
  - **The deeds are account-bound** (P79's AccountBinding), so nobody gets a piece their own AP has not opened (F-13).
- **EA-derived art** (Hestia's trophies, all of Archaaz's) ships the way earlier EA-derived art does: only as our own
  PNG override inside the player package, never as an EA file. Each registry row says so. This needs Chase's
  confirmation (Deviations 1).
- **Tests:**
  - Server: 5 new facts, each seen red first.
  - Package: 1 new fact, red on two mutations; the registry ledger was updated.
  - Full gate green twice: `sl-modernuo:cc-P243`, **2,025 tests, 2,021 passed, 4 skipped, 0 failed**.
  - P26's gates pass.
- **Not seen in a client.** Facings and the trophy walls need a look ("For Chase").

## 1. Pick

Read: the three `SOURCE.txt` files, `notes\cc-P229-league-reward-shop.md` (via its code), and P229's stock table
(`LeagueShop.cs:92-120`). Contact sheets of all three sets were made in the session scratchpad. They are not committed,
because two of the sets are EA-derived.

| Set | Folder | What it is | Taken | Left out |
|---|---|---|---|---|
| RedRooster, "Rooster's Display Cases" V.1.0 | `display-cases` | His own drawing, 44 x 107. Shelf1 and Shelf2 are the same case drawn for two facings. Each insert comes in two widths: odd numbers fit Shelf1, even fit Shelf2. No pixel of a shelf and its insert overlaps, so draw order does not matter (checked) | Shelf1/2; Book 1/2, Book 5/6 (partial hue), GEM1/2, GlassInsert1/2 | Shelf3/4, GlassInsert3/4, Book 3/4, GEM3/4 (kept small) |
| Hestia, "Trophys and Statues", statues | `hestia-trophies\Statues` | Rendered statues, not EA art | 1a/1b winged dragon, 2a/2b dark dragon, 5a jeweled dragon, 6a gargoyle | the gnomes, fairy, animals, children (garden pieces, not a trophy hall) |
| Hestia, trophies | `hestia-trophies` | Stock creatures' heads on plaques: **EA-derived** (her SOURCE.txt warns "likely") | Minotaur, Sabertooth, Troglodyte, Skull (1a/1b) | Lasher, Sphynx, Tri Wolf, Man and Woman (partial hue human heads) |
| Archaaz, "New Trophies and Heads" | `trophies-heads` | **EA-derived** ("using existing art", his words) | Trophies Titan, Oni, Ophidian Matriarch, Terathan Matriarch, Paroxysmus; heads Titan, Oni | fish, harpy, horses, llama, ophidian knight and mage, hellcat, terathan avenger, drone, warrior |

Nothing taken is marked RIP or IP. Hestia's statues look like rendered garden figures, with no game or brand look.

**Which file is which wall.** The packs do not say. I compared each trophy's silhouette with OSI's own trophy pair
(north 0x1E60, west 0x1E67, read from the client's art) and took the better match within each pair. The match was
clear for most pairs. It was close for the **skull, titan and troglodyte** (margins 0.01-0.03), so check those three in
the client (For Chase). The floor pieces' a/b (or 1/2) files are assigned south, then east, without a reference.

## 2. Ship the art

All files are written by `notes/cc-P243-tools/hall_art.py` (registry first, then PNGs, then records):

- **registry.csv:198-235:** 38 rows, kind art.
  - The source column names the pack and the file.
  - The license column carries each author's rule: "none stated; community work: credit <author> in the shard
    credits, ship only inside the player package or the private repo, do not repost".
  - RedRooster's rows add that he asks to be listed.
  - The EA-derived rows add "EA-derived ...: ships only as our PNG override, never as an EA file".
- **art/15592.png-15629.png** (236 KB): `scripts\anchor-art-frames.py --black-transparent --keep-geometry`. That is BMP
  to PNG and pure black made transparent; no other change, and the tool re-read each PNG against its BMP.
- **records.json:57-94:** 38 tiledata records, inserted as lines so the hand layout is kept. They follow OSI's records,
  read 2026-10-21:

  | Piece | Copies | Flags | Height |
  |---|---|---|---|
  | Shelves | bookcase 0xA97 (without Container: a case holds nothing) | Impassable, ArticleA | 12 |
  | Inserts | — | ArticleA (Book 5/6 also PartialHue, as their author made them) | 0 |
  | Statues | statue 0x1224, plus Impassable, as cc-P34's statue | Impassable, ArticleA | 20 |
  | Trophies | trophy 0x1E60 | ArticleA | 0 |
  | Mounted heads | — | ArticleA | 2 |

  Names are 19 ASCII characters at most.
- **The server's copy:** `LeagueHallArt.Records` (`LeagueHall.cs:139-190`), applied by `ShatteredLegacyArt.Apply`
  (`ShatteredRunestone.cs:64-65`). The server reads the unpatched EA tiledata, where these are empty slots.
- **SOURCE.txt:331-355:** the set's section: authors, links, credit rules, the EA-derived ruling, pixels and records.
- **IDs:**
  - `find-free-art.py --explain` showed 15590-15633 all free (EA placeholder slots).
  - 15536-15589 were skipped, because P242 (committed, not yet merged) uses them.
  - `--check-registry`: **0 of 228 registered IDs are no longer free.**
  - `validate-art.py check-registry`: **0 of 228 rows have problems.**

## 3. Items (`server/customizations/LeagueShop/LeagueHall.cs`, new, 490 lines)

| Line | What |
|---|---|
| `:65-136` | `LeagueHall`: the 19 `Pieces` (key, label, kind, default AP and Renown, facings: label, parts, the wall needed), `Stock()` (shop entries priced from the settings now, ordered by AP then Renown), `Find`, `FindEntry` |
| `:139-190` | `LeagueHallArt`: the server's tiledata copy |
| `:194-232` | `LeagueHallFacingGump`: the facing choice. Pinned's `RewardOptionGump` takes cliloc numbers only, so this is our own two-button version |
| `:239-274` | `LeagueHallComponent : AddonComponent, IDyable`. `NeedsWall`/`WallPosition` come from the facing: a north wall at (0,-1) and a west wall at (-1,0), as pinned `TrophyAddon.CouldFit`. `Dye` (`:257`) works only for a display case's parts, only for an owner or co-owner of the house it stands in, with any tub that takes dyeables (a plain dye tub). Pinned's furniture tub refuses dyeables and wants locked-down furniture, which addon parts never are |
| `:277-318` | `LeagueHallAddon : BaseAddon`. `ShareHue => false`, so each part keeps its own hue; its deed comes back bound to the same account |
| `:322-489` | `LeagueHallDeed : BaseAddonDeed`, bound to the buying account. Double-click checks the account and the pack, then asks for the facing (one-facing pieces skip that), then targets. `TryPlace` (`:398`) is pinned `BaseAddonDeed`'s target step for step, with its refusal lines. The account binding (`:466-489`) is `LootBox`'s, line for line |

## 4. The Hall page (`LeagueShop/LeagueShopGumps.cs`)

- **Shop window:** the shop gains a **Hall** button beside Titles (`:28`, `:68-69`, `:145-149`).
- **`LeagueHallGump` (`:248-`):** the shop's own frame and rows (`LeagueShopGump.Row`: price and AP in cc-P169's
  colours, art greyed until AP opens the row), five a page, a Shop button back. A row press sends the confirm step
  for the row, found again by key and priced from the settings now.
- **The confirm gump** (`:171-240`) takes `fromHall`, so Buy and Back return to the Hall page.
- **Kept out of the loot boxes:** the Hall rows are not in `LeagueShop.Stock`, so P229's loot boxes (whose pool is
  `Stock`) never hand out Hall decor. Fact 1 checks this.

**Proposed prices** (defaults; each is a setting). P229's starter table runs 0-1,750 AP and 25-1,000 Renown; its
nearest pieces are the banner (250 AP, 150) and the trophy statuette (500 AP, 250):

| AP | Pieces | Renown |
|---|---|---|
| 250 | display cases: glass 150, books 200, gems 200, dyeable books 250; skull trophy 200 | 150-250 |
| 500 | oni head 250; minotaur, sabertooth, troglodyte trophies 300; gargoyle statue 350 | 250-350 |
| 1,000 | titan head 300; oni, ophidian, terathan trophies 450; paroxysmus trophy 500; winged and dark dragon statues 600 | 300-600 |
| 1,750 | titan trophy 600; jeweled dragon statue 1,000 | 600-1,000 |

All 19 pieces cost 7,700 Renown, which gives Renown its first large sink.

## 5. Guardrails (F-13)

- **Decor only.** No item properties, no skill or stat effects. A piece is an addon with art, a name and a hue.
- **Deeds are account-bound** (trade, drop, hand-over and lift by another account are all refused). Why:
  - The AP gate is per account.
  - A tradeable deed would let a 0-AP player buy a 1,750-AP statue from someone else.
- **Placed pieces are bound too.** A placed piece stays in its house. Chopping it gives back a deed bound to the
  original buyer, whoever owns the house then.
- **Contrast with P229:** its own rows (tabard, banner, statuette) stay tradeable as P229 built them. I did not change
  them; see Deviations 3.

## Tests

Server facts (`server/tests/Misc/LeagueHallVerification.cs`), each seen red first:

| Fact | Pins | Seen red |
|---|---|---|
| `AHallRowNeedsItsApAndTakesExactlyItsRenown` | 19 rows, unique, Decor, Hall art, AP-tier order, none in `LeagueShop.Stock`. One AP short and one Renown short: refused, nothing taken. Enough: exactly the price, one deed bound to the buyer. A changed setting is the new price (restored after) | red A (rows ordered by AP descending): "Collections differ" |
| `BuyingFromTheHallLeavesLifetimeRenownAndLeagueRankUnchanged` | Two Hall buys: Renown less exactly both prices; LifetimeRenown, rank and the rank check unchanged | red A (a buy that grants 1 Renown): "Expected 1800, Actual 1802" |
| `TheDeedPlacesOnlyInAHouseItsBuyerOwns` | Someone else's house and outside any house: `NotInHouse`, deed kept. Another account's character can neither use nor trade it. The buyer's house: `Valid`, both case parts on the spot, in `house.Addons`, the deed used up. A trophy in the open: `NoWall` for both facings, deed kept | red B (no account check, any house): "Expected NotInHouse, Actual Valid" |
| `ADisplayCasesShelfAndInsertDyeApart` | `ShareHue` false; dyeing the shelf leaves the insert, and dyeing the insert leaves the shelf; a stranger is refused; a statue takes no dye | red B (`ShareHue` true): "Assert.False() Failure" |
| `EveryPartHasItsTiledataAndAChoppedPieceGivesItsBoundDeedBack` | Every placed part has a record and every record is used; names, flags and the 19-character rule in the server's table; only trophies need a wall; chopping gives back a deed for the piece, bound to the buyer | red A (one record dropped): "Collections differ" |

**A test-host limit found on the way.** Under xUnit, `TileData.Load` never runs (`TileData.cs:292-297`), so
`TileData.MaxItemValue` stays 0. Every multi tile's ID is masked to 0, so `BaseAddon.IsWall` can never see a wall in a
test. My first version of fact 3 hung a trophy on a test wall and failed there in red A, which none of red A's breaks
explains. The probe on the builder image found the cause. So fact 3 checks the refusal (a trophy with no wall is
refused). Hanging one on a real wall is a play test.

Package fact (`Build-UoOverrides.Tests.ps1:480-532`):
- **What it checks:** the C# records equal records.json (IDs in order, names, flags by value, weight, height). Each ID
  is registered once as art with its PNG, and each license names its author's rule. Hestia's statues must not be
  marked EA-derived; her trophies and Archaaz's must be. The set has exactly 38 rows. The records fact's carve-out
  (`:253-254`) and the ledger (`:294-297`: 228 rows, 188 art) are updated.
- **Red** on scratch copy a (an Archaaz row without its EA-derived mark): "15620: Archaaz's credit, EA-derived".
- **Red** on scratch copy b (a C# height changed): "expected [16] but got [20]. height of 15607".
- **Green:** **18 of 18** on the tree. `scripts\tests`: **55 of 55**.

**Build record** (`docker\uo\build.sh -t sl-modernuo:cc-P243`, runs detached, docker-build lock 10:13-10:26 CDT, page
cache dropped first). Logs are `build-P243-*.log` in the session scratchpad.

| Run | Result |
|---|---|
| red A, first | compile error: the serialization generator already makes `Dyeable` from `_dyeable` (my duplicate property removed) |
| red A | 2,025 tests, 4 failed: facts 1, 2 and 5 (own reasons), and fact 3 (the test-host wall limit above; the fact was then reworked) |
| red B | 2 failed: facts 3 and 4 (own reasons) |
| cycle 1 | **green: 2,025 tests, 2,021 passed, 4 skipped, 0 failed**; all 12 of P229's `LeagueShopVerification` facts pass |
| cycle 2 (after the patch notes) | **green, the same**; image 3a592668a9bc carries VERSION 2026.10.21.14 and the notes (read back from the container) |

The stubbed file was saved before the probes and restored after (byte-compared).

Repo size rule: the largest new file is the dragon statue PNG (well under 1 MB); nothing is over 5 MB.

## Website credits

For the shard credits list (each author's terms):

- **Display cases by RedRooster (Steven Armstrong)**, "Rooster's Display Cases",
  https://www.servuo.dev/archive/roosters-display-cases.1555/. He asks to be listed in shard credits.
- **Statues and trophies by Hestia**, "Trophys and Statues", https://www.servuo.dev/archive/trophys-and-statues.1804/.
- **Trophies and heads by Archaaz**, "New Trophies and Heads", https://www.servuo.dev/archive/new-trophies-and-heads.1428/.

None of the three states a license. As their `SOURCE.txt` files say, they are treated as community work: credit the
author, ship only inside the player package or the private repo, do not repost. Chase, 2026-10-21: use them and credit
their authors.

## Deviations and decisions for Chase

1. **EA-derived art ships as our PNG overrides.**
   - The prompt says such pieces "ship as our patch records only", but the package has no art-patch mechanism: maps
     have `Apply-MapOps.ps1`; art has nothing like it.
   - The art library's rule and P140's precedent (the crow, registry 2071: "ships only as our encoded blocks ...,
     never as an EA file", and SOURCE.txt: "as the EA-derived PNG art does") read as: EA-derived pixels may ship
     inside our own package files, never as an EA file. I followed that for Hestia's 4 trophies and Archaaz's 7
     pieces (22 IDs).
   - If you want them only as true patch records, they come out of registry.csv, records.json and `Pieces`, and the
     Hall keeps the 4 cases and 4 statues. Building an art-patch pipeline that rebuilds them from the player's own
     files would be its own prompt.
2. **Facings are judged, not stated.** The wall trophies were matched to OSI's north and west trophy. The skull, titan
   and troglodyte were close calls. The floor pieces were assigned south, then east.
3. **P229's own rows stay tradeable;** only the Hall's deeds are bound. If the same F-13 reasoning should apply to
   P229's banner and statuette, that is a small follow-up.
4. **Dyeing uses a plain dye tub**, not the furniture tub, which refuses dyeable items and wants locked-down
   furniture. Only the owner or a co-owner of the house can dye. Only the cases dye; statues and trophies do not.
5. **The trophy wall check is not covered by a server test** (the test host's tiledata limit, under Tests). The
   refusal is covered.
6. **Prices are proposals** (part 4), each a setting.
7. **Merge note for the integrator:**
   - This branch carries P241's ledger (190 -> 228 rows).
   - P242 (committed) moves the same lines from 180 to 234 rows. With all three merged: **282 rows, 15 gump rows, 242
     art rows**.
   - The records fact's carve-out line also gains a clause from both P242 and P243.

## For Chase

- **Setup:** rebuild the test shard from this branch (`sl-modernuo:cc-P243`), build the player package, and update a
  test client.
- **The Hall page:** give a test character AP and Renown (`[props` on the account data, or earn some), open the League
  Shop and press **Hall**.
  - Rows are in AP order, locked rows greyed with their AP, and each buy confirms.
  - Renown drops by exactly the price; League rank does not move.
- **Placing:** in a house that character owns, place a display case of each kind in both facings.
  - Do the shelf and insert line up?
  - Dye the shelf and then the insert with a dye tub: do they take different hues?
  - Book 5/6 (dyeable books) should tint only their partial-hue parts.
- **Wall trophies:** hang one of each against a north wall and a west wall.
  - Does each plaque sit flat on its wall?
  - Check the skull, titan and troglodyte especially.
  - In the middle of a room the deed should refuse ("This object needs to be mounted on something.").
- **Statues and heads:** place each statue and head; check the dragons' size against a room (they are 147 px wide)
  and that the statues block movement.
- **Re-deed and binding:** chop a placed piece; the deed comes back. Try to trade a deed to another account
  (refused), and use it in a house that character does not own (refused).
- **No update:** without the client update, the art shows EA's "UNUSED" placeholder.
- **Credits:** add the "Website credits" lines to the shard credits list.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration -Branch golem/Bronze/P243`. It points at
this Golem's work copies; the defaults are the main checkouts, which this desk may not touch. Code: 48 files pending
(8 changed, 38 PNGs, LeagueHall.cs, the new test). Docs: 2 (this note and the tools folder). Neither is BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P243 DONE
