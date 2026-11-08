# cc-P852: decoration addons from the 11-07 and 11-08 scout, assessed

## In plain words

- **65 decoration downloads were looked at:** holiday pieces, furniture, lamps, town dressing and whole buildings.
  Every one of them is built from art our game client already has, so none needs a client or player package update.
- **Worth taking, best first:** a carpet deed that lays a carpet of any size on a house floor; a batch of house
  furniture (stone fireplaces, the Hunt Master buffet and dining tables, harpsichords, small kitchens, couches); a
  winter set for New Haven's square (an animated Christmas train, a big snow globe, Santa and snowman benches); a
  fortune teller's wagon for the Festival Peddler; and real lamps that light up.
- **Not worth it:** the Deceit brazier (ModernUO already has it), the original player houses as addons (the client
  already has those designs), an "arena" that is only a wall ring, and three Milva lamps that the Drafted lamp set
  already covers. None of the 65 grants skill, stats, power scrolls or bless deeds.
- **For you:** pick which of the five "port first" items to queue. The winter set needs to be queued soon to be in
  New Haven by December 1.

Iron Golem, 2026-11-08. Assessment only: no code, nothing built, run or copied out of `D:\UO\third-party`. Docs copy
`D:\UO\golems\Iron\shard-migration` on `golem/Iron/P852`; code copy `D:\UO\golems\Iron\ShatteredLegacy` read only.
`docs\` not edited. Every folder's row is now in `D:\UO\third-party\CODE-INTAKE.md` (65 new rows, backup
`CODE-INTAKE.md.bak-20261108-p852`).

## How this was checked

- For each folder: `SOURCE.txt` (author, link, description, terms), each `.cs` header and the class list. Script:
  `notes/cc-P852-tools/survey.py` (output `survey.txt`, `survey.json`).
- **The art check.** The script pulls every art ID out of each addon (`AddComplexComponent`, `new AddonComponent`,
  `base(0x...)`, `ItemID =`) and looks each one up in the player package's client data
  (`D:\UO\tool-trials\client-data-copy`: `artidx.mul` for an image, `tiledata.mul` for its name).
  - **All 65 folders: every ID has an image in our client. 0 missing.**
  - The high IDs (0x4000 and up, the SA to Endless Journey art) were checked by name, so a custom-art slot would show
    up as a wrong name (the P779 ship-hull scare). Every name matches the piece: `Harpsichord SOUTH` for the pianos,
    `banquettable SOUTH` and `feasting_table_SOUTH` for the Hunt Master tables, `Beer_Table_East`,
    `wedding_arch_1_south`, `Orrery_1`, `town_xmas_tree`, `Christmas_Garland_So`, `Lamp Dragon SOUTH`. List:
    `notes/cc-P852-tools/high-art-names.txt`.
  - The only images in the folders are the authors' screenshots (`.jpg`, `.png`), not art.
  - Two odd picks to drop when rebuilding: the Large Christmas Tree uses a `Sigil PVP` piece and three statues
    (leprechaun, wizard, bear); the pond uses two world-tree mosaic tiles. They exist in the client; they just look
    out of place.
- **So every one is free to rebuild as our own data.** The `.cs` files are YAAAG addon-generator output (one
  `AddComplexComponent` line per piece, a deed, a Serialize pair). Nothing of the authors' code is worth keeping: the
  component lists (art, offset, hue, light, name) are what we need. Credit the author anyway (the scout's default
  terms).
- **Clashes checked** against pinned ModernUO (`D:\UO\ModernUO-pinned\Projects\UOContent`) and our
  `server/customizations`: only `DeceitBrazier` exists already (pinned `Items/Misc/DeceitBrazier.cs`). ModernUO's
  `SnowGlobe` items are small hand-held globes, a different thing from Milva's walk-round addon.
- **Rules check:** no folder grants skill or stat points, power scrolls, bless deeds or property artifacts. The
  hammock and water wheel deeds are themselves `Blessed` (a deed that stays in the pack on death), which is not a
  bless deed; rebuild them unblessed like our other decor deeds.

## The one piece of code that unlocks the batch

Our addons today are one C# class each (P724's `TutorialIsleAddons.cs`, P783's tables, `Items/Addons/`). 43 "port"
rows below at that rate is 43 classes. Instead:

- **A data addon:** one `ShardDecorAddon` and one deed that read their pieces from a data file in the shard's own
  decoration format (pinned's `[Decorate` text, the format of `server/data/Decoration/Builds` and P812's
  `[VBuild capture`). One file per addon, keyed by name; the deed names the file. Facings are separate files
  (`grey-fireplace-large-east`, `-south`).
- Then each "data" row is a file, made by a script from the download's component list, checked in the art index, and
  rendered with `isorender.py` for a look before it ships.
- Rough size: about 300 lines and facts for the addon, deed, file loader and a staff `[DecorAddon <name>` command,
  then one file per piece.

"Port cost" below: **data** = a data file once that addon exists; **small code** = a little behaviour on top (a
light, a facing choice on the deed); **medium code** = a gump and house checks to rebuild.

## Every folder

"Ser" counts hand-written Serialize overrides; for the data rows they disappear (the addon is ours). Terms: no
folder states a license. The scout's default applies to all: community work, credit the author, ship only inside the
player package or the private repo, do not repost. Extra credits are in the Terms column.

| Folder | Author | Group | What it is | Fit | Size; art | Port cost | Terms | Recommendation |
|---|---|---|---|---|---|---|---|---|
| `blue-couches` | Diesel | housing furniture | Couch in four facings: pillows and hued table pieces | Housing reward stores (Artisan decor, P783), League building lounge | 4 .cs, 504 lines, 8 Ser; stock: 7 art IDs, all in our client | data | none stated; credit Diesel | **port**: four tidy facings; one data row each |
| `grey-fireplaces` | Diesel | housing furniture | 10 grey stone fireplaces, 5 sizes, east and south | Housing; the League building hearth; New Haven inn in winter | 10 .cs, 1317 lines, 20 Ser; stock: 5 art IDs, all in our client | data | none stated; credit Diesel | **port**: five sizes fit small and large rooms; plain stone, so they sit in any house style |
| `diesel-lamps-pillars` | Diesel | housing furniture | 14 lamps built from tables, candles and hued beehive shades; 3 flame pillars | Housing lamps in 7 shade colours; pillars for the League building or a shrine | 17 .cs, 1739 lines, 34 Ser; stock: 7 art IDs, all in our client (up to 0x42CA) | data | none stated; credit Diesel | **port**: cheap; the shade hues should move to our hue list |
| `drafted-lamps-jackolanterns` | Drafted | housing furniture | 11 real light items (not addons): dragon, bird, koi, antique and modern tall lamps, ornate table lamps, a dragon brazier, a gold candle tray, a jack-o-lantern that flips through 11 styles | Housing lamps; the Festival Halloween stock (jack-o-lanterns) | 11 .cs, 813 lines, 11 Ser; stock: 52 art IDs, all in our client (up to 0x9952) | small code | none stated; credit Drafted | **port**: real lamps that light and flip; supersedes the three Milva lamp downloads, which use the same art |
| `milva-dragon-lantern` | Milva | housing furniture | Dragon lantern, lights when used (one item) | Housing | 1 .cs, 51 lines, 1 Ser; stock: 1 art IDs, all in our client (up to 0x4C40) | small code | none stated; credit Milva | **skip**: same art (0x4C40) and job as the Drafted dragon lantern; take that one |
| `milva-stained-glass-lamp` | Milva | housing furniture | Stained glass lamp, lights when used (one item) | Housing | 1 .cs, 49 lines, 1 Ser; stock: 1 art IDs, all in our client (up to 0x4C50) | small code | none stated; credit Milva | **skip**: folded into the Drafted lamp set (same SA lamp art range); add 0x4C50 there if Drafted lacks it |
| `milva-tall-lamps` | Milva | housing furniture | Two tall glass lamps, light when used | Housing | 2 .cs, 100 lines, 2 Ser; stock: 2 art IDs, all in our client (up to 0x4C56) | small code | none stated; credit Milva | **skip**: folded into the Drafted lamp set (antique and modern tall lamps); add 0x4C52/0x4C56 there if missing |
| `lagatha-beer-bar` | Lagatha | housing furniture | Beer bar (EA beer table art), north and west | New Haven inn and tavern; League lounge; housing | 2 .cs, 184 lines, 4 Ser; stock: 6 art IDs, all in our client (up to 0x9F5C) | data | none stated; credit Lagatha | **port**: tavern dressing with real EA art |
| `lagatha-desks-benches` | Lagatha | housing furniture | Tinker's bench and a writing desk (author calls it a computer desk) from EA tinker and repair tables and satchels | Housing; Artificers' Order workshop; League building office | 4 .cs, 368 lines, 8 Ser; stock: 9 art IDs, all in our client (up to 0xA27E) | data | none stated; credit Lagatha | **port**: rename the 'computer desk' to a writing desk |
| `lagatha-kitchens-bbq` | Lagatha | housing furniture | Two small kitchens (marble bar, sink, cooking machine) and two barbecues with steaks | Housing; New Haven inn kitchen; cooks | 4 .cs, 370 lines, 8 Ser; stock: 11 art IDs, all in our client (up to 0x9DA3) | data | none stated; credit Lagatha | **port**: small-room kitchens are what housing lacks |
| `lagatha-new-kitchen` | Lagatha | housing furniture | Kitchen with pie safes, spice rack and a stove, east and south | Housing; inn kitchen | 2 .cs, 240 lines, 4 Ser; stock: 19 art IDs, all in our client (up to 0xA2A9) | data | none stated; credit Lagatha | **port**: pairs with the small kitchens; the candied apples and Halloween spice pieces can be swapped out of season |
| `lagatha-pianos` | Lagatha | housing furniture | Two harpsichords (EA art) with benches | Housing; tavern; League lounge; bards | 2 .cs, 174 lines, 4 Ser; stock: 14 art IDs, all in our client (up to 0x63C9) | data | none stated; credit Lagatha | **port**: a showpiece for bards' houses |
| `lagatha-holiday-fireplace` | Lagatha | holiday kit | Holiday fireplace with stockings and garland (pre-SA art) | Winter: New Haven inn (P266 SeasonalDecor), Festival winter stock | 1 .cs, 127 lines, 2 Ser; stock: 26 art IDs, all in our client | data | none stated; credit Lagatha; originally by Gwenivere (Knights of the Round Table shard): credit both | **port**: a winter fireplace is missing from P266's set (Hestia's was held back on terms) |
| `lagatha-holiday-table` | Lagatha | holiday kit | Winter feast table, east-west | Winter: inn feast, Festival winter stock | 1 .cs, 163 lines, 2 Ser; stock: 26 art IDs, all in our client | data | none stated; credit Lagatha; originally by Gwenivere: credit both | **port**: low priority; take with the fireplace; P34's inn feast already covers the town |
| `lagatha-holiday-table-ns` | Lagatha | holiday kit | Winter feast table, north-south | as above | 1 .cs, 162 lines, 2 Ser; stock: 26 art IDs, all in our client | data | none stated; credit Lagatha; originally by Gwenivere: credit both | **port**: the other facing of the same table |
| `lagatha-campfire-witches` | Lagatha | holiday kit | Bonfire with witches flying round it | Halloween: New Haven square or a hilltop (SeasonalDecor) | 1 .cs, 119 lines, 2 Ser; stock: 5 art IDs, all in our client (up to 0xA2F7) | data | none stated; credit Lagatha | **port**: animated EA bonfire; a Halloween centrepiece for 2027 |
| `lagatha-dancing-fire` | Lagatha | holiday kit | Bonfire with skeletons dancing round it | Halloween: as above | 1 .cs, 118 lines, 2 Ser; stock: 5 art IDs, all in our client (up to 0xA2F7) | data | none stated; credit Lagatha | **port**: the other Halloween bonfire; pick one or both in 2027 |
| `manwitch-brass-orrery` | manwitch | housing furniture | Animated brass orrery (one EA art piece, 0xA17B) | Housing reward; League building study; Artificers' Order | 1 .cs, 96 lines, 2 Ser; stock: 1 art IDs, all in our client (up to 0xA17B) | data | none stated; credit manwitch | **port**: one tile, always animated; a plain decor item, no addon needed |
| `manwitch-buffet-table` | manwitch | housing furniture | Buffet table, OSI Hunt Master reward art, two facings | League hunt rewards (P780 daily hunts, reward store); housing | 2 .cs, 190 lines, 4 Ser; stock: 20 art IDs, all in our client (up to 0x9D52) | data | none stated; credit manwitch | **port**: it was an OSI hunting reward, so it fits the League hunt reward row |
| `manwitch-formal-dining` | manwitch | housing furniture | Formal dining table, OSI Hunt Master reward art, two facings | League hunt rewards; housing | 2 .cs, 191 lines, 4 Ser; stock: 24 art IDs, all in our client (up to 0x9D7E) | data | none stated; credit manwitch | **port**: pairs with the buffet table |
| `manwitch-hammock` | manwitch | housing furniture | Hammock with a direction choice on the deed (look only) | Housing; Wakening Isle beach; League field camp | 1 .cs, 118 lines, 2 Ser; stock: 11 art IDs, all in our client | small code | none stated; credit manwitch | **port**: small: the deed's facing choice is the only code |
| `manwitch-water-wheel` | manwitch | housing furniture | Animated water wheel (EA watermill art), deed with a direction choice | Housing by water; New Haven mill; the isle farm | 1 .cs, 148 lines, 2 Ser; stock: 8 art IDs, all in our client (up to 0xA0F8) | small code | none stated; credit manwitch | **port**: animated, real EA art; the facing choice is the only code |
| `medusa-fountains` | Celestial | town dressing | Two 4x4 Medusa fountains: bubbling and bloody | New Haven square; Halloween (the bloody one); housing | 2 .cs, 276 lines, 4 Ser; stock: 31 art IDs, all in our client (up to 0x40BC) | data | none stated; credit Celestial | **port**: the bloody one is a ready Halloween piece |
| `celestial-fairy-tree` | Celestial | town dressing | Fairy tree (stock tree, mushrooms, sparkles) | Wakening Isle grove; housing yard | 1 .cs, 140 lines, 2 Ser; stock: 32 art IDs, all in our client | data | none stated; credit Celestial | **idea only**: pretty but no named spot; keep for a grove brief |
| `celestial-holiday-dining` | Celestial | holiday kit | Gold holiday dining set for 12, east only | Winter housing reward | 1 .cs, 169 lines, 2 Ser; stock: 17 art IDs, all in our client | data | none stated; credit Celestial | **idea only**: three feast tables already on this list; one facing only |
| `celestial-christmas-train` | Celestial | holiday kit | Christmas train: animated engine wheels, smoke and lights (deco, cannot board) | Winter: New Haven square (SeasonalDecor, P266); Festival winter | 1 .cs, 350 lines, 2 Ser; stock: 46 art IDs, all in our client (up to 0xA000) | data | none stated; credit Celestial | **port**: a winter showpiece the town lacks; stock art, no package change |
| `candyapple-christmas-tree` | Candy Apple | holiday kit | Large Christmas tree with presents and odd extras (a PvP sigil, a leprechaun, a wizard statue) | Winter | 1 .cs, 153 lines, 2 Ser; stock: 46 art IDs, all in our client (up to 0xA608) | data | none stated; credit Candy Apple | **idea only**: New Haven already has its square and bank trees (P34, P266); the stray pieces would need picking out |
| `candyapple-xmas-deco` | Candy Apple | holiday kit | Six winter addons: boat tree, classic tree, deer tree, Santa bench, snowman bench, Christmas convo | Festival winter stock (housing); New Haven square benches | 7 .cs, 1089 lines, 14 Ser; stock: 115 art IDs, all in our client (up to 0xA4D0) | data | none stated; credit Candy Apple | **port**: the Santa and snowman benches are new to our winter set |
| `milva-bank-christmas-1` | Milva | holiday kit | Christmas dressing for the whole Britain bank roof | Britain only | 1 .cs, 382 lines, 2 Ser; stock: 68 art IDs, all in our client (up to 0xA000) | data | none stated; credit Milva | **idea only**: built for Britain bank's roof; our winter dressing is New Haven (P266) |
| `milva-bank-christmas-2` | Milva | holiday kit | Second Britain bank roof dressing with a small vendor building | Britain only | 1 .cs, 423 lines, 2 Ser; stock: 88 art IDs, all in our client (up to 0xA000) | data | none stated; credit Milva | **idea only**: as above |
| `milva-snowglobe` | Milva | holiday kit | Large walk-round snow globe with moving snow | Winter: New Haven square; Festival winter top reward | 1 .cs, 223 lines, 2 Ser; stock: 37 art IDs, all in our client (up to 0xA000) | data | none stated; credit Milva | **port**: big and animated; ModernUO's small snow globes are a different item |
| `xl-christmas-sleigh` | Milva | holiday kit | Extra large sleigh you can walk into and sit in | Winter: New Haven square by Father Christmas (P34) | 1 .cs, 219 lines, 2 Ser; stock: 31 art IDs, all in our client (up to 0xA000) | data | none stated; credit Milva | **port**: low priority: take the train first, the sleigh if the square has room |
| `winter-snow-trees` | Milva | holiday kit | Three snow trees (one decorated) | Winter roads (P266 SeasonalDecor) | 3 .cs, 355 lines, 6 Ser; stock: 10 art IDs, all in our client (up to 0x9DB8) | data | none stated; credit Milva | **port**: low priority; variety for P266's road trees |
| `halloween-deco-items` | Milva | holiday kit | Chopping block with a moving blade, gore rack, skull pit | Festival Halloween stock; the witch drops (P779) | 3 .cs, 354 lines, 6 Ser; stock: 64 art IDs, all in our client (up to 0x4695) | data | none stated; credit Milva | **port**: low priority; the witch already drops a gore rack and torture block (P779), so take the skull pit and blade |
| `olorin-halloween-bank-topper` | Olórin | holiday kit | Halloween roof topper for Britain bank: pumpkin patch and small tomb, two pieces | Halloween; the pumpkin patch could stand anywhere | 2 .cs, 410 lines, 4 Ser; stock: 50 art IDs, all in our client (up to 0xA5E5) | data | none stated; credit Olórin | **idea only**: sized for Britain bank; P267 already dresses our bank for Halloween |
| `spider-webs` | Milva | holiday kit | Large and medium spider webs as one-piece addons | Halloween; dungeons; League dives | 2 .cs, 186 lines, 4 Ser; stock: 9 art IDs, all in our client | data | none stated; credit Milva | **port**: saves staff hand-placing thin web pieces |
| `deceit-brazier` | ImaNewb | town dressing | Deceit brazier that spawns monsters when used | none | 1 .cs, 165 lines, 1 Ser; stock: 1 art IDs, all in our client | small code | none stated; credit ImaNewb | **skip**: pinned ModernUO already has DeceitBrazier (Items/Misc), with a wider monster list |
| `hopers2-world-tree` | hopers2 | housing furniture | World tree floor mosaic (EA art), large and small, two facings | Housing floor; League building hall floor | 4 .cs, 388 lines, 8 Ser; stock: 65 art IDs, all in our client (up to 0x9E7D) | data | none stated; credit hopers2 | **port**: low priority; real EA mosaic art |
| `olorin-autumn-trees` | Olórin | town dressing | 16 autumn trees with nests and hives (EA leaf art) | Autumn town dressing; the Wakening Isle; open world | 15 .cs, 1583 lines, 30 Ser; stock: 33 art IDs, all in our client (up to 0xA668) | data | none stated; credit Olórin | **port**: big variety for little cost; an autumn season dressing if Chase wants one |
| `olorin-boulders-cairns` | Olórin | town dressing | 6 boulders and 4 cairns | Wakening Isle; League field work; open world; housing yards | 10 .cs, 929 lines, 20 Ser; stock: 31 art IDs, all in our client | data | none stated; credit Olórin | **port**: plain stock rock, useful almost anywhere |
| `olorin-cloud-ship` | Olórin | structures | Sky ship with cargo hold and crew rooms (staff add a teleporter) | Events; a sky area we do not have | 1 .cs, 490 lines, 2 Ser; stock: 91 art IDs, all in our client (up to 0xA675) | data | none stated; credit Olórin | **idea only**: no sky area yet |
| `olorin-feasting-tables` | Olórin | town dressing | Three festival feasting tables | New Haven festival square; the inn | 3 .cs, 372 lines, 6 Ser; stock: 19 art IDs, all in our client | data | none stated; credit Olórin | **port**: low priority; overlaps the Hunt Master tables |
| `olorin-fortune-teller-wagon` | Olórin | town dressing | Fortune teller's wagon you can step into | The Festival Peddler's stall in New Haven; fairs | 1 .cs, 265 lines, 2 Ser; stock: 77 art IDs, all in our client (up to 0xA778) | data | none stated; credit Olórin | **port**: gives the Festival Peddler a home; z needs a nudge to walk in (author's note) |
| `olorin-gargish-light-posts` | Olórin | town dressing | Two gargish light towers | Town lighting; League building outside | 2 .cs, 237 lines, 4 Ser; stock: 10 art IDs, all in our client (up to 0x413F) | data | none stated; credit Olórin | **port**: low priority |
| `olorin-grandfather-clock` | Olórin | housing furniture | Two-storey grandfather clock, east and south, for a hidden door | Housing; a secret room | 2 .cs, 492 lines, 4 Ser; stock: 58 art IDs, all in our client (up to 0xA582) | data | none stated; credit Olórin | **idea only**: the trick needs a hidden door we would add ourselves; no named spot |
| `olorin-hunters-camp` | Olórin | town dressing | Archer and hunter camp | League field work; the isle's hunter; open world | 1 .cs, 241 lines, 2 Ser; stock: 82 art IDs, all in our client (up to 0xA2A9) | data | none stated; credit Olórin | **port**: a ready camp for League field NPCs |
| `olorin-hunters-wagon` | Olórin | town dressing | Hunter's cabin on wheels with a ladder | Open world; League field | 1 .cs, 233 lines, 2 Ser; stock: 50 art IDs, all in our client (up to 0xA55A) | data | none stated; credit Olórin | **port**: low priority; pairs with the camp |
| `olorin-inn-stable` | Olórin | town dressing | Small stable that leans on an inn | New Haven inn; League building stables | 1 .cs, 154 lines, 2 Ser; stock: 29 art IDs, all in our client (up to 0xA668) | data | none stated; credit Olórin | **port**: fits towns with no room for a full stable |
| `olorin-large-icebergs` | Olórin | town dressing | Five large icebergs and ice flows | Sea dressing near ice | 5 .cs, 1498 lines, 10 Ser; stock: 53 art IDs, all in our client (up to 0x45D0) | data | none stated; credit Olórin | **idea only**: no northern sea work queued |
| `olorin-large-marketplace` | Olórin | town dressing | Large decorated marketplace, one stall left empty | New Haven market; a festival market | 1 .cs, 1049 lines, 2 Ser; stock: 245 art IDs, all in our client (up to 0xAC79) | data | none stated; credit Olórin | **port**: 245 art pieces of ready dressing; needs a spot check on both New Havens (release and main differ) |
| `olorin-paddle-boat` | Olórin | town dressing | Animated paddle boat, north facing | Harbour or river dressing | 1 .cs, 410 lines, 2 Ser; stock: 36 art IDs, all in our client (up to 0xAA68) | data | none stated; credit Olórin; author: 'yours to use however you wish' | **idea only**: clear terms, but no harbour job queued |
| `olorin-pond-bridge` | Celestial | town dressing | Medium pond with a bridge, animated water and candle lily pads (by Celestial, not Olorin) | Housing yard; New Haven park; the isle | 1 .cs, 180 lines, 2 Ser; stock: 39 art IDs, all in our client (up to 0xA286) | data | none stated; credit Celestial | **port**: low priority; the folder name says Olorin but the author is Celestial |
| `olorin-rose-garden` | Olórin | town dressing | Raised rose garden bed | Housing yard; herbalism; New Haven gardens | 1 .cs, 196 lines, 2 Ser; stock: 41 art IDs, all in our client (up to 0xA4E4) | data | none stated; credit Olórin | **port**: low priority |
| `olorin-sarcophagus-set` | Olórin | holiday kit | 15 sarcophagi (open, closed, male, female) and a display rack | Dungeons; League dives; Halloween | 15 .cs, 1613 lines, 30 Ser; stock: 109 art IDs, all in our client (up to 0x48AD) | data | none stated; credit Olórin | **port**: dungeon and crypt dressing in one set |
| `olorin-scaffold-set` | Olórin | town dressing | Six scaffolds, three sizes, two facings | Building sites in towns; the League building's works | 6 .cs, 560 lines, 12 Ser; stock: 4 art IDs, all in our client | data | none stated; credit Olórin | **port**: low priority |
| `olorin-temple-of-the-dragon` | Olórin | structures | Huge golden dragon temple statue and structure | An event or League trial centrepiece | 1 .cs, 599 lines, 2 Ser; stock: 57 art IDs, all in our client (up to 0xA1FE) | data | none stated; credit Olórin | **idea only**: too big for any named spot |
| `smithy-townhouse` | Olórin | structures | Three-storey smithy townhouse (workshop, living, bedroom) as one addon | A server-placed town building | 1 .cs, 423 lines, 2 Ser; stock: 111 art IDs, all in our client (up to 0xA531) | data | none stated; credit Olórin | **idea only**: a building, not furniture; use as a reference for a New Haven or village smithy |
| `house-boat-addon` | Carl Hamilton | structures | House boat on water, two facings (staff placed) | Harbour dressing | 2 .cs, 390 lines, 4 Ser; stock: 52 art IDs, all in our client | data | none stated; credit Carl Hamilton | **idea only**: no harbour job queued |
| `prebuilt-houses-12-custom` | Carl Hamilton | structures | 12 custom houses as addons (staff placed, no house rules) | Town and village shells | 12 .cs, 2970 lines, 24 Ser; stock: 292 art IDs, all in our client | data | none stated; credit Carl Hamilton | **reference only**: not player houses; for shells our builds (P734 PlaceBuild) do better |
| `prebuilt-houses-custom-structures` | Carl Hamilton | structures | 6 custom houses and 4 structures: gallows, park, old dock ruins, blacksmith shop, guild house | Town dressing (gallows, park, dock ruins) | 10 .cs, 2087 lines, 20 Ser; stock: 318 art IDs, all in our client (up to 0x41E7) | data | none stated; credit Carl Hamilton | **idea only**: the gallows, park and dock ruins are handy dressing; take them when a town brief asks |
| `prebuilt-houses-original` | Carl Hamilton | structures | The 13 original and 7 Renaissance player houses as addons | none | 20 .cs, 5722 lines, 40 Ser; stock: 307 art IDs, all in our client | data | none stated; credit Carl Hamilton | **skip**: the client's multi data already holds these designs |
| `arena-addon` | ImaNewb | structures | Arena: stone wall ring and floor. The post promises a moongate and controller; the code has neither | none | 1 .cs, 185 lines, 2 Ser; stock: 4 art IDs, all in our client | data | none stated; credit ImaNewb | **skip**: only walls and floor; any arena we want we would build ourselves |
| `wedding-arches` | Milva | housing furniture | Two rose wedding arches and two with a ladder (EA art) | Housing reward; a New Haven chapel or garden | 4 .cs, 372 lines, 8 Ser; stock: 19 art IDs, all in our client (up to 0x9ECD) | data | none stated; credit Milva | **port**: real EA wedding art; a nice reward store row |
| `wedding-venue` | Kitten | structures | Wedding venue: arch, chairs, flower stands, candelabras | Staff weddings and events | 1 .cs, 314 lines, 2 Ser; stock: 13 art IDs, all in our client (up to 0xA000) | data | none stated; credit Kitten | **idea only**: a staff event set; place with the arches if a wedding is asked for |
| `variable-carpet` | Milva | housing furniture | Carpet deed: pick a style and hue, target two corners on your house floor, any size | Housing (all houses); the reward stores | 3 .cs, 661 lines, 4 Ser; stock: 9 art IDs, all in our client | medium code | none stated; credit Milva; Manu (1.0), Draco van Peeble (2.0), Milva: credit all three | **port**: the most useful housing piece here; gump and house checks to rebuild |

Totals: **port 43, idea only 15, reference only 1, skip 6.**

## Shortlist by use (top 15 named)

**Housing furniture** (Artisan decor and reward stores, P760 and P783; the League building)
1. `variable-carpet`: a carpet of any size and style on a house floor.
2. `grey-fireplaces`: 10 stone fireplaces, 5 sizes.
3. `manwitch-buffet-table` and `manwitch-formal-dining`: OSI's Hunt Master reward tables, a natural League hunt
   reward row.
4. `lagatha-pianos`: two harpsichords.
5. `lagatha-kitchens-bbq` and `lagatha-new-kitchen`: small kitchens and barbecues.
6. `drafted-lamps-jackolanterns`: 11 lamps that light and flip (and the jack-o-lantern for Halloween).
7. `manwitch-water-wheel`: an animated water wheel for houses by water and New Haven's mill.

**Holiday kit** (SeasonalDecor, P266 and P267; the Festival store)
8. `celestial-christmas-train`: animated train for New Haven's winter square.
9. `milva-snowglobe`: a big snow globe with moving snow.
10. `candyapple-xmas-deco`: Santa and snowman benches and three trees.
11. `lagatha-holiday-fireplace`: the winter fireplace P266 left out.
12. `spider-webs` with `olorin-sarcophagus-set`: Halloween and crypt dressing (Halloween 2027, League dives now).

**Town dressing** (New Haven, the Wakening Isle, League field work)
13. `olorin-fortune-teller-wagon`: a home for the Festival Peddler's stall.
14. `olorin-boulders-cairns`: rock for the isle, field camps and yards.
15. `olorin-hunters-camp`: a ready camp for League field NPCs.

**Structures:** none in the top 15. The buildings (smithy townhouse, prebuilt houses, dragon temple, cloud ship,
house boat) are idea or reference only until a town brief names a spot; our own builds (`[PlaceBuild`) do this job.

Runners-up worth a later batch: `olorin-large-marketplace` (a ready New Haven market, if a spot fits both New Havens),
`olorin-autumn-trees` (if Chase wants an autumn dressing), `medusa-fountains`, `olorin-inn-stable`,
`wedding-arches`, `lagatha-campfire-witches` and `lagatha-dancing-fire` (Halloween 2027).

## Port first (for the overseer to put to Chase)

1. **The data addon plus the housing furniture batch.** One `ShardDecorAddon` and deed reading our decoration
   format, then the fireplaces, Hunt Master tables, harpsichords, kitchens and couches as data files, sold in the
   reward stores (the Hunt Master tables in the League hunt row). *Why:* it turns every later "port" row here into a
   data file instead of a class, and housing has the least new decor.
2. **The variable carpet, rebuilt as ours.** Style and hue gump, two-corner target, house owner and fit checks,
   removal confirm; a size cap in settings. *Why:* the most useful single housing piece in the batch, and the only one
   that needs real code (the 3 .cs are an old RunUO gump to rewrite for ModernUO). Credit Manu, Draco van Peeble and
   Milva.
3. **A winter set for New Haven before December 1:** the Christmas train and the large snow globe on the square,
   the Santa and snowman benches, the holiday fireplace in the inn, added to P266's SeasonalDecor area lists (and
   the benches and fireplace as Festival winter stock). *Why:* winter starts on its own on 12-01 (P266); stock art
   means no player package build. Place everything twice: release and main New Haven differ (x 3400-3560 against
   3600-3760). Needs item 1 first, or four classes written by hand if item 1 cannot land in time.
4. **The fortune teller's wagon for the Festival Peddler.** *Why:* the stall is up in three seasons and stands in the
   open; the wagon gives it a look. Same two-New-Havens caveat; the author notes the z needs a nudge to walk in.
5. **The Drafted lamps as real lights.** 11 `BaseLight` items (lit and unlit art, flip), with the Milva dragon,
   stained-glass and tall lamps folded in. *Why:* lamps that work are a housing staple, and the jack-o-lantern gives
   the Halloween stall a 2027 row. Small code, 11 Ser to source-generate.

## Not done

- No in-game or rendered look at any piece: the check is by data (art index and tiledata names). Each port prompt
  should render its pieces with `isorender.py` before placing.
- No spot check in New Haven for the train, snow globe, wagon or market: that belongs in each port prompt.
- `D:\UO\third-party\README.md` and `ART-LIBRARY.md` were not changed (the prompt names only CODE-INTAKE.md).
- The project copy `claude/servuo-code-intake.md` was not edited: the scout re-syncs it from the master.

P852 DONE
