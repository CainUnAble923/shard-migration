# P538: art on disk that has no registry attribution yet

2026-10-24. Research only. The grouped catalog below lists unpacked art in the local library with no matching source attribution in the current shard registry. Proposed uses are suggestions, not new scope or a decision to import anything.

The most direct matches are `paperdoll-buttons` and `dark-scrolls-ui` for the guild and League menu work in P436; `quest-markers`, `training-dummy-pinata`, `npc-shop-signs`, and shoreline or garden ambience for the tutorial island in P481; `hippogriff`, `raven-lord-mount`, and `thagoras-moose` for reward mounts; and the remaining Hestia furniture, garden, and lighting packs for decor. See the partial-pack section before choosing from the large animation or icon collections.

## Sources and limits

- Read both work-copy AGENTS.md files, direction-decision.md, and tasks.md. No files under docs were edited.
- No notes copy of the library was found. Notes P177, P201, P265, P266, P364, and P365 reference it. The master is available here: `D:\UO\third-party\ART-LIBRARY.md`, updated 2026-10-23. Its sections 1 through 8 provide the organizing context. Its disk labels predate several imports.
- Compared `player-package/vendor/shattered-legacy-art/registry.csv`, its `SOURCE.txt`, and `skins.json` in the code work copy. Read the separate `player-package/vendor/paperdoll-sos/SOURCE.txt` so an import outside this registry is not mistaken for unused art.
- Each catalog row has an actual unpacked file witness under `D:\UO\third-party\<set>\`. The terms source for that row is `<set>\SOURCE.txt`. File witnesses prove presence, not animation completeness or placement in a world.
- Compared ServUO resource numbers in source citations. Pack-name and source-filename checks supplement the comparison for the shortlisted and partial packs. For the mount shortlist and named partial animation packs, also compared VD SHA-256 against registered source hashes. Numeric body IDs are not resource numbers. Registry attribution is the basis for the catalog; a different copy, renamed derivative, or asset inside another vendor could escape that comparison.
- A focused tracked-code search found no mentions of dark-scrolls-ui, Abraxus, paperdoll-buttons, quest-markers, seagulls, hippogriff, ravenmount, or thagoras-moose. This supports those candidates but does not establish runtime nonuse for every file in every catalog pack.
- No live world, package installation, screenshots, Haven service, or client was inspected. Nothing here proves that a registered item has been placed or published. Counts in the old library are deliberately not repeated. This is a set-level inventory, with a witness file rather than an unverified image total.
- Scope is unpacked art sets named in the library. Code-only resources, audio, queued downloads, external-only downloads, previews, archive-only content, and absent art are excluded. Expanded the library's moongate color and Hestia painting-family shorthand where those folders exist. This is not a full disk crawl of all downloads.

## License flags

`No license stated` means exactly that. A local intake convention to credit an author and ship only inside the player package or private repository is not a license grant. Read the row's SOURCE before import. `Credit` means that SOURCE records an attribution request or the intake attribution convention; it does not imply every author has the same legal terms.

`EA` means derived from EA art. Keep the existing package override or patch-record route, never raw EA files. `RIP` means another game's art, or a possible rip with unresolved origin. `IP` means a franchise look. The master library records Chase's 2026-10-13 RIP allowance and 2026-10-23 IP allowance with new in-game names and no brand or character names. Some older SOURCE files still contain the earlier ban or request for review; those old policy statements do not reverse the later calls. They also do not supply a missing license.

`REPL` means the download targets stock IDs. A future import needs new IDs or an optional skin and a fresh collision check. Author-supplied IDs are not reserved for us. Specific terms override the general intake convention. In particular, DRC1K prohibits modifications and commercial use including donations; the Kevsurcu Chinese boat says ServUO-exclusive, which does not establish permission for this ModernUO shard. Mad Scientist's remade machine has an unknown original author. These are qualifications on candidates, not instructions to import them.

## Guild and League menus, P436

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `abraxus-paperdoll` | Abraxus paperdoll, by Cerrera | No license stated; REPL; Credit: see SOURCE | Optional matching paperdoll skin; older client dimensions need fitting. | `Abraxus/abraxus looking at/Gump 2008 0x7D8 - Copy (2).bmp` |
| `abraxus-status` | Abraxus status, by Cerrera | No license stated; REPL; Credit: see SOURCE | Matching optional status panel; check current Endless Journey fields. | `Gump 10860 0x2A6D.bmp` |
| `ancient-hue-file` | A complete custom hues.mul, by Erachiro; a source for individual hues | No license stated; Credit: see SOURCE | Inspect single unused hues for guild accents; never replace the whole hue file. | `hues.mul` |
| `dark-scrolls-ui` | Dark scroll frames, buttons, and UI gumps, by CorvaeOboro | No license stated; REPL; Credit: see SOURCE | Candidate shared P436 frame and button style; retain readable text contrast. | `UI_DarkScrolls/UI_DarkScrolls/ui_scroll_arrow_down_0x826.bmp` |
| `paperdoll-buttons` | Quest and Guild paperdoll button states, by Castiel | No license stated; EA; Credit: see SOURCE | Quest and Guild entry buttons for P436; check the current client layout before using. | `Gump 22450.bmp` |
| `spell-icons` | Colorized Magery spell icons, by CorvaeOboro | CC0 author license; EA; Credit: see SOURCE | Optional spell-school accents in P436; these are EA-derived icons. | `UI_MagicSpells/ui_spell_1_Clumsy_0x8C0.bmp` |
| `status-bar-10860` | gump 10860 Status Bar Update for Endless Journey, by rahto | No license stated; EA; REPL; Credit: see SOURCE | Optional status skin with Endless Journey fields. | `Gump 10860 .bmp` |
| `uo-paperdoll-project` | Paperdoll and equipment art with GIMP sources, by Zigholtul | No license stated; Credit: see SOURCE | Paperdoll framing and equipment-slot art for an optional skin. | `UO Paperdoll Project (Classic UO) 1.0/PNGs/Equipment/Hair/Art/Anime Spike Gump (Art).png` |

## Tutorial island, P481, and town paths

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `african-trees` | African Tree Sprites 2.0, by Thagoras | Author permits use/editing; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Africa/Aloe a.bmp` |
| `azaleas` | Rooster's PH Azalea Bushes, by RedRooster (Steven Armstrong) | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Rooster's PH Bushes/flowerbush1.bmp` |
| `bamboo` | Bamboo 2.0, by Thagoras | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Bamboo Update/Bamboo  01.bmp` |
| `beach-trees` | beach trees, by ParanoiaPhD | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `beachtree3.bmp` |
| `butterflies` | Butterflies, by Vrark | No license stated; RIP or possible RIP; Credit: see SOURCE | P481 farm and garden ambience. | `Ambient creatures with scripts/Legend of Zhao Yun butterfly 1 50_.vd` |
| `ems-clutter` | Clutter, by Ems | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `half filled scroll.bmp` |
| `ems-picnic-pack` | Picnic pack, by Ems | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `chocolate cupcake.bmp` |
| `fireflies` | Fireflies, by Ems | No license stated; Credit: see SOURCE | P481 garden and path landmarks after dark. | `Item 0x357F.bmp` |
| `garden-statues` | Garden statues, by Ems | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `statue 2.1.bmp` |
| `hanging-baskets` | Rooster's Hanging Plant Basket's w/PH Plant's!, by RedRooster (Steven Armstrong) | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Rooster's Hanging  Flower Pots/HangerSouth 2.bmp` |
| `hestia-garden-items` | Garden Items, by Hestia | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Garden by Hestia/Anim christmas hedge/Hedge 1a.bmp` |
| `hestia-letters-numbers` | Letters and Numbers by Hestia, by Hestia | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Letters Numbers/Ground Tile E/Letter A.bmp` |
| `hestia-water-barrel` | Animated Water Barrel, by Hestia | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Water Barrels/Fallen Barrel 1a.bmp` |
| `kevsurcu-big-trees` | New 3 Big Trees by Kevsurcu, by Kevsurcu | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Tree/Tree 01/Tree 01_001.bmp` |
| `kevsurcu-raft` | Raft by Kevsurcu (2022-12-19), by Kevsurcu | No license stated; Credit: see SOURCE | P481 dock dressing; functional river travel would need a separate system. | `Rafts/1/01.BMP` |
| `laoth-wooden-crates` | Simple wooden crates, by Laoth | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `crate (1).bmp` |
| `mrriots-misc-items-2` | Potted and growing plants and Asian fans, by MrRiots | Author permits use/editing; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `FanArt-1.bmp` |
| `mrriots-spring-plants` | Flowers, plant boxes, seed bags, and pots, by MrRiots | Author permits use/editing; EA; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `1.bmp` |
| `mrriots-storage-crates` | [MrRiots] Storage Crates, by MrRiots | Author permits use/editing; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Crate1-1.bmp` |
| `npc-shop-signs` | NPC Shop Signs, by Castiel | Specific terms in SOURCE; REPL; Credit: see SOURCE | P481 farm, trainers, stables, and exits; use new IDs beside stock signs. | `Item 0x50C2.bmp` |
| `osi-plants` | OSI plant replacements, by Thagoras | No license stated; RIP or possible RIP; REPL; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Set 1/Bluebell a.bmp` |
| `ph-flowers` | Rooster's Partial Hue Flowers, by RedRooster (Steven Armstrong) | No license stated; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Rooster's PH Flower's/FlowerPH1.bmp` |
| `plants-set-2` | Trees and Plants - Set 2, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Set 2/Black Cherry/BlackCherry 01.bmp` |
| `pottery` | Unified Pottery Project 2.0, by otimpyre | No license stated; EA; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Unified Pottery Project/01.bmp` |
| `quest-markers` | Animated exclamation and question markers, by RedRooster | No license stated; Credit: see SOURCE | P481 lesson NPC markers: animated exclamation and question marks. | `Quest Marker/E1.bmp` |
| `seagulls` | Seagulls, by Vrark | No license stated; RIP or possible RIP; Credit: see SOURCE | P481 shoreline ambience; flying-only art, with separate sound provenance to check. | `Seagulls/IE seagull 2.vd` |
| `tall-trees` | Tall Trees & Stuff 1.3, by Zigholtul | No license stated; EA; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Tall Trees & Stuff (1.3)/50%/Item 3274 (Tree).bmp` |
| `training-dummy-pinata` | Scarecrow swing, hit, break, and candy-spill frames in both facings, by Archaaz | No license stated; EA; Credit: see SOURCE | P481 combat practice target; breaking pinata for a graduation event. | `Scarecrow/South Facing/1.bmp` |
| `transparent-water` | Transparent Water Tiles, by abu | No license stated; EA; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `Transwater/Tiles/1.bmp` |
| `verdant-autumn-trees` | Trees of Verdant and Autumn leaves, by CorvaeOboro | CC0 author license; EA; Credit: see SOURCE | P481 farm, garden, shoreline, or town wayfinding decor. | `ART_Tree/item_tree_base_0x0CC9.bmp` |

## Mounts, pets, and creature rewards

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `cerberus` | Three-headed hound animation, by Odin | No license stated; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `Cerberus.vd` |
| `hippogriff` | Hippogriff, by Dr Death | No license stated; Credit: see SOURCE | A new League or achievement reward mount. | `Hippogriff mount - L anim Slot.vd` |
| `kirin` | Replacement Kirin Animation, by Vert-I-Go | No license stated; REPL; Credit: see SOURCE | A separate new mount look instead of replacing the stock kirin. | `Kirin.vd` |
| `mastodon` | Mastodon, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | Large wilderness mount candidate; test rider alignment and scale. | `Mastodon.vd` |
| `new-lion` | New Lion, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `New Lion.vd` |
| `panther` | New Panther, by Vert-I-Go | No license stated; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `New Panther.vd` |
| `pointy-red-hat` | A pointed hat with item art and wearable animation, by Vrark | No license stated; Credit: see SOURCE | Garden-gnome familiar accessory or costume; a wearable hat, not a new creature body. | `Hat/Pointy red hat.bmp` |
| `raven-lord-mount` | Raven Lord Mount, by Anon the Felon | No license stated; Credit: see SOURCE | A rare bird mount reward. | `ravenmount.vd` |
| `red-whelp` | Fixed Red Whelp, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `Red Whelp.vd` |
| `sea-creatures` | Sharks, threshadon, and a seahorse mount animation, by Vert-I-Go | No license stated; Credit: see SOURCE | Seahorse mount candidate and coastal encounters; water travel is separate work. | `Great White.vd` |
| `thagoras-dragon-pack` | Dragon pack, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `Dragon Pack/Dragon 01.vd` |
| `thagoras-moose` | Moose Mobile, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | A woodland hunt target or reward mount; needs mobile and riding setup. | `Moose.vd` |
| `tiger` | Tiger, by Vert-I-Go | No license stated; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `anim4_0xF0.vd` |
| `wolf-replacement` | Wolf Replacement, by Vert-I-Go | No license stated; REPL; Credit: see SOURCE | An additional pet stage, tameable, or mount reward; verify animation actions first. | `Wolf replacement.vd` |

## Guild halls, homes, and League display rooms

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `hestia-paintings-7` | Painting statics, by Hestia | No license stated; Credit: see SOURCE | Guild gallery, League collection display, or house decor rewards. | `Paintings 7/pic dragon eye 2b.bmp` |
| `hestia-paintings-6` | Painting statics, by Hestia | No license stated; Credit: see SOURCE | Guild gallery, League collection display, or house decor rewards. | `Paintings 6/pic skeleton angel 1a.bmp` |
| `hestia-paintings-5` | Painting statics, by Hestia | No license stated; Credit: see SOURCE | Guild gallery, League collection display, or house decor rewards. | `Paintings 5/pic angel 1a.bmp` |
| `hestia-paintings-3` | Painting statics, by Hestia | No license stated; Credit: see SOURCE | Guild gallery, League collection display, or house decor rewards. | `Paintings Hestia 3/Painting Bird yellow 1a.bmp` |
| `bobble-heads` | Character bobble-head statics in TIFF format, by otimpyre | No license stated; Credit: see SOURCE | League trophy-room collectibles; TIFF originals need format conversion. | `[Custom Art] Bobble Heads/Item 0xBE02.tiff` |
| `archin-bust-statues` | Bust Statues, by Archin | No license stated; EA; Credit: see SOURCE | Guild founders and League milestone displays. | `Archin_Bust/Female_Bust/F_Bust1A.bmp` |
| `colossus` | Colossus, by Odin | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Colossus.png` |
| `dragon-mailbox` | Dragon mailbox, by Dameon | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `DragonMailbox_East_64x96.png` |
| `ems-gramophone` | Gramophone (2023-01-28), by Ems | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Item 0x2147.bmp` |
| `hestia-anim-4` | Animated bird paintings, spilled wine, wings, belts, and necklaces, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Anim Items and Other Items #4/Anim Bluebird Painting/Anim Bluebirds 1a.bmp` |
| `hestia-anim-hedge` | Anim Hedge and More, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `For Servuo to post/Anim Arch Hedge/Hedge Arch Anim 3a.bmp` |
| `hestia-anim-kitchen-5` | Animated book, coffee pot, toaster, and stained glass, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Anim Kitchen Items and other/Anim Book/Anim Book 1a.bmp` |
| `hestia-anim-lights` | Animations Lights, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Lights Anamiated from Rendered Spirits/Brazier 1/Lamp Column 1a.bmp` |
| `hestia-anim-wheels-mannequins` | Animated wheels, cogs, mannequins, and tiles, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Anim Wheels Manniquins Tiles and Other/Anim Cog/Cog 3a Anim.bmp` |
| `hestia-barrels-crates` | Barrels, Fallen Barrels, Crates, Baskets, by Hestia | No license stated; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Barrels New type/Barrel Apple.bmp` |
| `hestia-bars-tables-a-f` | Bars and Tables A-F, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Bar and Table A-F/A1 Bar E.bmp` |
| `hestia-bars-tables-g-l` | Bars and Tables G-L, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Bar and Table G-L/G1 Bar E.bmp` |
| `hestia-curtains-wallpapers` | Curtains and Wallpapers, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Curtain and Wallpaper/Curtain 6a.bmp` |
| `hestia-doors-walls-roofs` | Doors, Walls, Windows, Roof Corners, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Doors Walls Window Roof by Hestia/crystal roof corner 1a.bmp` |
| `hestia-fireplaces-2` | Anim Fireplace's 2, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Anim Fireplaces/Fireplace 10aa.bmp` |
| `hestia-furniture` | Counters, shelves, fridge, dressers, and animated casino machine, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Furniture by Hestia/Above Counter Shelf 1a.bmp` |
| `hestia-furniture-a-f` | Furniture A-F, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Furniture A-F/A Corner E.bmp` |
| `hestia-furniture-g-l` | Furniture G-L, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Furniture G-L/G Corner E.bmp` |
| `hestia-keys` | Partial-hue key types, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Keys/Key 1a.bmp` |
| `hestia-misc-1` | Animated mirror, shelves, trays, lights, and birdbaths, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Misc Items by Hestia/Anim Mirror/Animated Mirror 1a.bmp` |
| `hestia-misc-2` | Trophy shelf, microscope, granite furniture, shelves, and paintings, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Misc Items by Hestia 2/Atlas Statue.bmp` |
| `hestia-misc-3` | Closed vault doors and animated New Year ball, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Misc Items 3 by Hestia/Anim Christmas Fence Brown/Anim Brown Fence 2a.bmp` |
| `hestia-paintings-1` | Paintings by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Paintings Hestia/Painting Abstract Face 1a.bmp` |
| `hestia-paintings-2` | Paintings by Hestia #2, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Paintings by Hestia 2/Painting Bird Yellow 1a.bmp` |
| `hestia-paintings-4` | Paintings #4, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Hestia Paintings 4/blue dragon pic 1a.bmp` |
| `hestia-ramps` | Ramps, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Ramps/Ramp Dirt 1a.bmp` |
| `hestia-requested-1` | Chandeliers, animated chandelier, and tailor table, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Requested Items 1 by Hestia/Anim Chandalier 1a partial hue/anim chandalier 1a partial hue.bmp` |
| `hestia-statues-more` | Gargoyle and Pan statues and other statics, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Statues and More by Hestia/diamond cart 1a.bmp` |
| `hestia-tables-partial-hue` | Tables Partial Hue, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Tables Partial Hue/Table 1b.bmp` |
| `hestia-tan-shelves` | Tan shelfs, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Shelf Tan/Empty Fridge 1a.bmp` |
| `hestia-tiles` | Floor tiles and animated fireplace inserts, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Tiles by Hestia/Anim fireplace tile/Fireplace E 1a.bmp` |
| `hestia-walls-hedges` | Walls and Hedges, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `For Servuo to post/Barn Wall partial hue/Barn Door 1ca.bmp` |
| `hestia-walls-windows-fences` | Walls Windows and Fences, by Hestia | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Wall and Fence by Hestia/Anim Christmas lights 1/Anim Lights 1a.bmp` |
| `lb-throne-fixes` | LB Throne & Fancy Benches Item Art fixes. 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Item 0x1526 LB Throne Leftside Fixed.bmp` |
| `mad-scientist` | Mad Scientist Items, by Hestia | Specific terms in SOURCE; EA; Credit: see SOURCE; Unknown original machine author | Alembic or Artificer lab; skip the machine with an unknown original author. | `Mad Scientist/Anim Elec Ball Partial Hue/Electric Ball 1a.bmp` |
| `mrriots-art-package` | Mixed custom house and town statics, by MrRiots | Author permits use/editing; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `BMPs/AlchemyDrawer.bmp` |
| `mrriots-misc-3` | Alchemy box, resource sacks, beehive, and corrupted crystal, by MrRiots | Author permits use/editing; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `BMP/Alchemy Boxset/AndScroll2.bmp` |
| `mrriots-misc-items` | Jars, posters, backpacks, animated book, pipe, and candle jar, by MrRiots | Author permits use/editing; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Package/Package/Book-1.bmp` |
| `mrriots-new-uo-art` | [MrRiots] New UO Art, by MrRiots | Author permits use/editing; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `CleanRack1-1.bmp` |
| `plated-statues` | Modified Statues: Gold (or Bronze) and Copper Plating, by Archaaz | No license stated; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Statues/statue-1.bmp` |
| `pool-table-set` | Pool Table Set, by OUTLANDSOwyn | Author permits use/editing; Credit: see SOURCE | Guild tavern or League social room. | `Billiard_Blue.bmp` |
| `rooster-chess` | Rooster's PH Chess Pieces, by RedRooster | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Rooster's PH Chess Pieces/Bishop.bmp` |
| `rooster-glass-floor` | Rooster's Glass Floor Tile, by RedRooster | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Rooster's Glass Floor Tile/Glass Tile1.bmp` |
| `rooster-modular-windows` | Rooster's Modular Windows, by RedRooster | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `2.0/1.bmp` |
| `rooster-roman-scholar` | Roman scholar outfit gumps, by RedRooster | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `RomanScholarSet/Gold Leaf Headpiece Gump.bmp` |
| `simple-items` | Small house and town item statics, by Hello Frank | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `for servuo/16.bmp` |
| `uo-character-paintings` | Ultima Online Character Paintings, by Castiel | No license stated; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Anniversary1.bmp` |
| `walls-new-windows` | NEW Item ART - Walls with New Window Styles, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `NEW Window Item ART Images/Bamboo Hut Walls with Windows/01 Bamboo Hut E-W Wall - Window.bmp` |
| `wood-walls-round-windows` | NEW Wood Walls with Round Windows, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Dark Wood Braced E-W Round Window.bmp` |
| `ziggy-paintings-1` | Ziggys Custom Paintings Vol.1, by Zigholtul | No license stated; Credit: see SOURCE | Guild-room furnishing, player-house decor, or League display rewards. | `Ziggys Custom Paintings/Art Statics/UO Painting (Axehandle Hound) Art Static 1.bmp` |

## Dungeon kits, biomes, and encounters

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `crystal-wall` | Crystal wall art, by WarWeeD | No license stated; Credit: see SOURCE | Artificer trial room or crystal cave; source files are JPEG, so inspect edges and transparency. | `Item 0x3A5C.jpg` |
| `aged-gatedoor` | Aged Gatedoor, by golfin | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `arch_left.bmp` |
| `altered-lands` | Altered Lands, by CorvaeOboro | CC0 author license; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `ENV/ENV_CaveDark/ART_M/env_0476_cave_A.bmp` |
| `arctic-pack` | Ice creatures, caribou, penguin, bear, and walrus animations, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `ArcticPack/H_Ice Dragon.vd` |
| `atlantis-tiles` | Atlantis Tiles, by Archaaz | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Atlantis/Blue Marble Walls/1.bmp` |
| `bariaur` | Bariaur, Bariaur 2 non casting, Bariaur 3, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Bariaur 2.vd` |
| `basilisk` | Basilisk, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Basilisk.vd` |
| `beholder` | Beholder & Beholder-Kin, by Vert-I-Go | No license stated; RIP or possible RIP; IP; rename; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Eye of the Deep.vd` |
| `bone-golem` | Bone Golem, by Thagoras | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `BoneGolem.vd` |
| `brontosaurus` | Brontosaurus, by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Brontosaurus.vd` |
| `caged` | Caged, by otimpyre | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `[Custom Art] Caged/A1.bmp` |
| `chains` | Chains of Torment, by otimpyre | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `[Custom Art] Chains of Torment/02.bmp` |
| `cobramen` | Cobramen, by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `anim4_0x64.vd` |
| `custom-caves` | Custom Caves, by otimpyre | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Custom Caves Entrances/1.bmp` |
| `djinni` | Djinni, by Thagoras | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Djinni.vd` |
| `drc1k-uoassets` | Dungeon walls, sewer pieces, rocks, graveyard props, pine, and animated effects, by DRC1K | Noncommercial only (including no donations); no modifications; client-package-only redistribution; attribution appreciated. Read SOURCE and per-pack terms. | Cave, sewer, graveyard, or pine scenery; preserve its noncommercial and no-modification terms. | `Animated Wheels by - DRC1K - UOASSETS/wheel1.bmp` |
| `dream-boat` | The Dream Boat 1.0, by otimpyre | No license stated; EA; Credit: see SOURCE | Decorative dock or ship variant; not a working ship by art alone. | `[Art] The Dream Boat/15935.bmp` |
| `dungeon-bookshelves` | Dungeon Bookshelves, by otimpyre | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Dungeon Bookshelves/1.bmp` |
| `ec-orcs` | EC Scaled down Orc, by Skandraven | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `OrcModdedEC.vd` |
| `formorian-giant` | Formorian Giant, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Formorian Giant.vd` |
| `frost-giant-conan` | Frost Giant (Conan Exiles Game), by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `New Frost Giant.vd` |
| `giant-blue-mushrooms` | Giant Blue Mushrooms, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `01.bmp` |
| `giants` | Giants, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Fire Giant Hammer.vd` |
| `gift-boxes` | Gift boxes - various sizes/shapes, by Laoth | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `gift (1).bmp` |
| `greater-feyr` | Greater Feyr, by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Greater Feyr.vd` |
| `hallow-trees` | Trees from the Hallow, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `HallowTree Sapling.bmp` |
| `holes` | Holes, by otimpyre | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Holes/[Custom Art] Hole Cave/1.bmp` |
| `hued-orestones` | Hued Orestones using Abu's Orestones, by Archaaz | No license stated; EA; Credit: see SOURCE | Miners Compact metal deposits; credit both Archaaz and Abu. | `Abu's Orestones with Hues/Copper 1.bmp` |
| `kevsurcu-3-chinese-boats` | 3 Chinese Boat, by Kevsurcu | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Chinese Boat 01/01.bmp` |
| `kevsurcu-chinese-boat` | Ancient Chinese Boat (All Directions and Suitable for Scripting), by Kevsurcu | No license stated; Credit: see SOURCE; ServUO-exclusive wording; ModernUO use unverified | Dock set or scripted ship candidate; ServUO-exclusive wording needs clarification for ModernUO. | `Ancient Chinese Boat/Ancient Chinese Boat (E)/220x145/01.bmp` |
| `kevsurcu-chinese-cargo-ship` | Ancient Chinese Cargo Ship, by Kevsurcu | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Ancient Chinese Cargo Ship/01.bmp` |
| `kevsurcu-royal-carriage` | Royal Carriage by Kevsurcu (2022-12-19), by Kevsurcu | No license stated; Credit: see SOURCE | Town travel stop decor; moving carriage behavior is separate work. | `Royal Carriage/01.bmp` |
| `kraken` | Kraken Replacement 1.1, by Thagoras | No license stated; REPL; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Kraken2.vd` |
| `lady-ghost` | Lady Ghost 1.0, by Thagoras | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `GhostLady.vd` |
| `lizardmen` | Lizardmen, by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Lizardman Cheiftan.vd` |
| `malboro` | Malboro 1.0, by Zigholtul | No license stated; IP; rename; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Malboro_H.vd` |
| `manticore` | Fixed Manticore Animation, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Manticore.vd` |
| `minecraft-uo` | Minecraft UO 1.0, by otimpyre | No license stated; IP; rename; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Minecraft UO/01 Stone.bmp` |
| `mini-mermaid-statues` | Mini Mermaid and Dolphin Statues, by Archaaz | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Mini Statues/Mini Dolphin Statue 1.bmp` |
| `moonkin` | Moonkin, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Moonkin.vd` |
| `naga` | Naga, by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Naga Female.vd` |
| `oga-iso-mushrooms` | Isometric mushroom sprite sheets, by Varkalandar | CC BY 4.0 option; credit Varkalandar. Alternative CC BY-SA 4.0 also offered. | Herbalism and cave scenery after slicing and fitting to UO scale. | `hjm-mushrooms_01.png` |
| `orc-lord` | Orc Lord, by Skandraven | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `OrcLord.vd` |
| `ore-stalagmites` | Ore-Specific Stalagmite Ore Deposits, by Archaaz | No license stated; EA; Credit: see SOURCE | Miners Compact survey sites or mine rewards. | `Stalagmite Ore Deposits/Copper 1.bmp` |
| `otyugh` | Otyugh, by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Otyugh.vd` |
| `partial-hue-chests` | Partial Hue Chests (version 2.0), by Archaaz | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Partial Hue Chests/Metal Chest 1.png` |
| `purple-grass-dirt` | Purple Grass - dirt, by WarWeeD | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `blackrock to pourplegrass-texture/Texture 556.bmp` |
| `purplegrass-to-dirt` | purplegrass (to dirt), by WarWeeD | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `1.bmp` |
| `red-giant-mushrooms` | Red Giant Mushrooms, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Image40.bmp` |
| `rooster-aztec-floor` | Rooster's Aztec Flooring, by RedRooster | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `aztec floor/aztecfloortile1.bmp` |
| `sahuagin` | Sahuagin (Resized), by Vert-I-Go | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Sahuagin Crossbow (2).vd` |
| `serpent-isle-tiles` | Ultima VII Art: Serpent Isle Tiles, by RedRooster | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Rooster's Serpent Isle Tiles/1.bmp` |
| `skeleton-keys` | New Skeleton Key Graphics, by Archaaz | No license stated; EA; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Skeleton Keys/Skeleton Key 1.bmp` |
| `succubus` | Succubus 2.1, by Thagoras | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `FeatheredSuccubus.vd` |
| `theart-crystal-set` | Crystal Set, by TheArt | No license stated; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Crystal Floors/Item 0xA5D0.bmp` |
| `token-keys` | Quest, Item, Token Keys, by Hestia | Specific terms in SOURCE; Credit: see SOURCE | Tutorial gates, League encounter keys, or quest tokens. | `Quest or Item Key and Tokens/Amber  Token.bmp` |
| `wow-troll` | WOW Troll Resized, by Vert-I-Go | No license stated; RIP or possible RIP; Credit: see SOURCE | A themed League hunt, dungeon, mine, or added-area encounter. | `Troll Resized.vd` |

## Seasonal decor, prizes, and effects

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `moongate-white` | White spinning portal frames | No license stated; REPL; Credit: see SOURCE | Guild or League portal landmark, registered at new IDs rather than replacing stock gates. | `White Spinning Portal 1.bmp` |
| `moongate-black` | Black spinning portal frames | No license stated; REPL; Credit: see SOURCE | Guild or League portal landmark, registered at new IDs rather than replacing stock gates. | `Black Spinning Portal 1.bmp` |
| `moongate-red` | Red spinning portal frames | No license stated; REPL; Credit: see SOURCE | Guild or League portal landmark, registered at new IDs rather than replacing stock gates. | `Red Spinning Portal 1.bmp` |
| `moongate-blue` | Blue spinning portal frames | No license stated; REPL; Credit: see SOURCE | Guild or League portal landmark, registered at new IDs rather than replacing stock gates. | `Blue Spinning Portal 1.bmp` |
| `halloween-paperdoll` | Halloween Celebration: Free Halloween Paperdoll! (1.2), by yigitbaba | No license stated; EA; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Gump 50422.bmp` |
| `hestia-animal-dolls` | Animal Dolls, by Hestia | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Animal Bear Head 1a.bmp` |
| `hestia-christmas-fireplace` | Christmas Fireplace, by Hestia | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Anim Chirstmas Fireplace/Fireplace 13a.bmp` |
| `hestia-christmas-pole` | Animated holiday pole and exploding ball, by Hestia | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Anim Christmas Pole by Hestia/1 Christmas Pillar Animated/Pole 1a.bmp` |
| `hestia-dolls` | Dolls by Hestia, by Hestia | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Dolls by Hestia/Doll Body Apron partial hue.bmp` |
| `mrriots-halloween-2023` | Floating candles, bone furniture, Ouija board, and Halloween statics, by MrRiots | Author permits use/editing; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Item 0xB5E0.bmp` |
| `mrriots-halloween-2024` | [MrRiots] Halloween Art 2024 1, by MrRiots | Author permits use/editing; EA; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `HallUOWeen/Animated/1/1-1.bmp` |
| `mrriots-spring-easter` | [MrRiots] Spring/Easter inspired items 1, by MrRiots | Author permits use/editing; EA; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `EasterSpring/112.bmp` |
| `needoh-dumpling` | Fun animated Needoh and Dumpling set, by Mahgnitton | No license stated; IP; rename; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `needoh and dumpling/Dumpling Dyeable/Item 0x3BCD.bmp` |
| `portal-anim` | Portal, by eri | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `1.bmp` |
| `rainbow-sign` | Animated Rainbow Sign, by Archaaz | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Rainbow Sign/East/east rainbow 1.bmp` |
| `rooster-animated-rain` | Animated Rain, by RedRooster | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Rooster's RainAnim/rain 1.bmp` |
| `rooster-animated-snow` | Animated Snow, by RedRooster | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Rooster's Animated Snow/1.bmp` |
| `rooster-galaxy-floor` | Galaxy Flooring, by RedRooster | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `galaxyflooranim/1-1.bmp` |
| `star-tiles` | Animated Star Tiles!!, by RedRooster | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Animated Star Tiles/StarTile1.bmp` |
| `xmas-community-tree` | Xmas Holiday Event tree Decoration, by Erachiro | No license stated; Credit: see SOURCE | Seasonal town dressing, event prizes, or reward fanfare. | `Ultima Online Tree Art/Ornaments/Blue Ornaments/Blue Large Gold Trimmed Ornament.bmp` |

## Gear, costumes, and broader art sources

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `wonder-woman` | Shield, sword, and outfit gump images, by Dameon | No license stated; IP; rename; Credit: see SOURCE | Renamed costume rewards; JPEG source art needs inspection, and worn animations are unverified. | `Gump 50993.jpeg` |
| `almhara-dlc` | Weapons, armor, hair, jewelry, cloaks, and pet talisman art, by Zigholtul | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Age of Almhara DLC Pack (Ver. 1.4)/#01 Talismans/(Art Static) Bull Frog Pet.bmp` |
| `altered-weapons` | Altered Weapons, by CorvaeOboro | CC0 author license; EA; REPL; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `ART_Weapon/item_tool_CrookL_0x0E82.bmp` |
| `angel-wings-anim` | Angel Wings Animation, by Prapilk | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `AngelWings.vd` |
| `base-item-variants` | Potion, reagent, and other base-item variants, by CorvaeOboro | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `ART_BaseItemVariants/ART_Gems/item_gem_Amber_0xF25.bmp` |
| `carl-dupre-armor` | New Sir Dupre Armor GUMP and ART Item for Backpack 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Gump 50994 Sir Dupre Armor.bmp` |
| `carl-gm-robe` | New GM Robe GUMP and ART Item for Backpack 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Gump 50987 GM Robe Beltpouch.bmp` |
| `carl-lb-armor` | New LBritish Armor and LBlackthorn Robe Item ART images for Backpack 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Item 0x2042 LBritish Armor Backpack Item.bmp` |
| `carl-old-wizard` | New OLD Wizard GUMP and ART Item for Backpack 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `GUMP Old Wizard.bmp` |
| `carl-queen-dress` | New Queen Dress GUMP and ART Item for Backpack 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Gump 50990 Queen Dress to replace the LBritish Paperdoll Image - Copy.bmp` |
| `carl-wizards-robe` | New Wizards Robe GUMP and ART Item for Backpack 1.0, by Carl Hamilton | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Gump ART Wizards Robe.bmp` |
| `cyrddin-wings` | Wings, by Cyrddin | No license stated; Credit: see SOURCE; Uploader is not the author | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `wings/Gump 61176.bmp` |
| `dragon-shroud` | Hooded Dragon Shroud, by ParanoiaPhD | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Gump 60987dragon.bmp` |
| `garg-wings-admin-robes` | Enhanced Garg Wings and Admin Robes, by JBob | No license stated; EA; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `customized.bmp` |
| `hestia-wearables` | Wearable item and paperdoll art with animations, by Hestia | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Wearable Animation Doll Pipe Trim/ball cap 1a m art.bmp` |
| `mjollnir` | Mjollnir - Thor's Hammer 1, by RedRooster | No license stated; IP; rename; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Rooster's Mjollnir/Mjollnir-Gump.bmp` |
| `otimpyre-gm-robe` | GM Robe 2.0, by otimpyre | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Item 0x1F03new.bmp` |
| `paperdoll-templates` | Equipment-slot drawing templates in PSD, ORA, PDN, and TIFF, by Erachiro | No license stated; Credit: see SOURCE | Drawing templates for future equipment-slot art; an authoring aid, not ready-to-register UI. | `Gump Templates/Templates/Sketchbook Compatible_/Elven Female Paperdoll .tiff` |
| `piet-gumps-1` | Clothing and equipment paperdoll gumps, by Piet Zah | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Archer/Archer/Archer.bmp` |
| `piet-gumps-2` | More outfit gumps and tree statics, by Piet Zah | Specific terms in SOURCE; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Robe2/Robe2/Robe.bmp` |
| `rooster-roman-armor` | Rooster's Roman Armor Set, by RedRooster | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `RomanArmorSet/Roman Armor Gump.bmp` |
| `rooster-sword-gumps` | New Sword Gumps, by RedRooster | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Rooster's New Sword Gumps/Sword1.bmp` |
| `sailor-moon-items` | Sailor Moon Themed Items, by Elga de Uruk | No license stated; IP; rename; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Magical Girl Stuff/heart tiara bag item.bmp` |
| `tazuo-static-replacements` | Redrawn statics, AI-assisted art, and Enhanced Client pieces, by Zigholtul | No license stated; EA; REPL; Credit: see SOURCE | Optional client appearance pack; overlaps stock IDs and includes EA-derived redraws. | `UO Art Static Replacements for TazUO (2.0)/12252.png` |
| `theart-art-set` | Mixed static art, decor, and clothing gumps, by TheArt; sort before use | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `beartrap/tr1.bmp` |
| `uo-me-content` | Middle Earth themed statics and wearables in nested archives, by Erachiro | No license stated; IP; rename; Credit: see SOURCE | A renamed fantasy area or wearables; inspect nested archives individually. | `Grafiken/(ID0xB7)_Kampfsystem-Gump_Hintergrund.bmp` |
| `wings-odin` | Wings (gumps), by Odin | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `Harpy Wings.bmp` |
| `ziggy-dragon-armor` | (New) Dragon Armor, by Zigholtul | No license stated; Credit: see SOURCE | Guild or League cosmetic reward; check item, paperdoll, and worn-animation coverage. | `(New) Dragon Armor/Gumps/50679 Dragon Arms.bmp` |

## Whole maps for a separate area design

| Set | What it is | License flags | Feature it could serve | Unpacked file witness |
|---|---|---|---|---|
| `dungeon-map-4` | Dungeon Map For Map 4, by TheArt | No license stated; Credit: see SOURCE | A separate added area after map-slot and access design; never replace a live facet. | `map4.mul` |
| `paranoia-custom-map` | An actual 100% custom map (with a few buildings to start a city), by ParanoiaPhD | No license stated; Credit: see SOURCE | A separate added area after map-slot and access design; never replace a live facet. | `IceYouMusics Custom Map/Map0.mul` |
| `sos-trammel-map` | Siege of Sosaria Trammel Map 3.0, by Zigholtul | No license stated; Credit: see SOURCE | A separate added area after map-slot and access design; never replace a live facet. | `Siege of Sosaria Trammel Map (3.0)/Siege of Sosaria Trammel Map (UNFINISHED)/Map1.mul` |
| `termur-replacement` | Map Replacement for Ter Mur/Map 5, by TheArt | No license stated; Credit: see SOURCE | A separate added area after map-slot and access design; never replace a live facet. | `map5.mul` |

## Unused files inside packs that are already partly registered

These are not wholly unused sets. Paths below are relative to `D:\UO\third-party\`; each pack has its own SOURCE.txt. The named VD candidates were checked against registered source hashes and filenames. Gameplay support, rider alignment, action coverage, and duplicate art elsewhere in the library remain unverified.

| Set and exact candidate files | What it is | License flags | Feature it could serve |
|---|---|---|---|
| `theart-critters/OSI Classic Rips converted/H-boychild1.vd`, `H-boychild2.vd`, `H-girlchild1.vd`, `H-girlchild2.vd` | Child NPC bodies | No license stated; credit TheArt; EA | P481 child NPCs or later town stories. These are not juvenile animal stages. |
| `theart-critters/OSI Classic Rips converted/L-Flesh Renderer Mount.vd`; `OSI Remakes and Changes/Giant Wolf.vd`, `Unicorn Replacement.vd`; `Ridable Bird/Ridable Bird L Slot.vd`, `Ridable Bird Player Slot.vd` | Remaining mount and wolf looks | No license stated; credit TheArt; EA for Classic Rips and Remakes; bird provenance separate | League or achievement mount rewards. The red and colorable dragons are already registered as bodies 2086 and 2087. |
| `uo-pixel-animals/arx_goliathkaefer/arx_goliathkaefer.vd` | Goliath beetle | No license stated; credit Arx | Beetle pet or possible mount after action and rider checks. |
| `uo-pixel-animals/nexx666_radstar_leopard/H_leopard.vd` | Leopard | No license stated; credit Nexx666 and Radstar | Evo cat appearance or a woodland hunt. |
| `uo-pixel-animals/griffon_minitiere/H_frosch.vd`, `H_skorpion.vd`, `H_spinne.vd`, `L_echse.vd`, `L_kaefer.vd` | Small frog, scorpion, spider, lizard, and beetle animations | No license stated; credit Griffon; other-game origin unverified | Farm or cave ambience. Small animals do not establish a puppy, kitten, fox kit, or chick solution. |
| `plant-pack/Plant Pack/Ent02.vd`, `Ent03.vd`, `Trigit.vd` | Tree creatures | No license stated; credit Thagoras; source game not stated; rename | Herbalism guardians and woodland League hunts. The myconids, thorned hulk, and Treant already have bodies. |
| `plant-pack/Plant Pack/Tree Fellow 1.vd`, `Tree Fellow 2.vd`, `Tree Fellow 3.vd` | Oversized tree creatures | Same pack terms; each original exceeds 5 MB | Future woodland boss art only after a separate compliant derivative route. Never add these originals to either repo. |
| `elemental-pack/Elemental Pack/Golem Blood.vd`, `Golem Dirt.vd`, `Golem Fire.vd`, `Golem Metal.vd`, `Iron Golem.vd`, `JunkGolem.vd`, `Robot.vd` | Unregistered golem and machine looks | No license stated; credit Thagoras; RIP or unresolved source; rename | Artificer trials and construct hunts. CaveElemental and Stone Golem are already registered. |
| `underdark/Underdark/Beholder.vd`, `Carrion Crawler.vd`, `Drider Male.vd`, `Hive Mind.vd`, `Hook Horror.vd`, `Mind Flayer.vd`, `Remorhaz.vd`, `Umberhulk.vd` | Remaining underground creatures | No license stated; credit Vert-I-Go; RIP/IP; rename | New League encounters. The female drider and spider family are already registered. |
| `humanoids/Humanoid/Bugbear.vd`, `Deep Troll.vd`, `Ettin.vd`, `Frost Troll Mage.vd`, `Gnoll Captain.vd` | Remaining humanoid enemies | No license stated; credit Vert-I-Go; origin unresolved; rename franchise names | League hunt variants. Gnoll, Ratman Lord, Bullywog Spear, and Kuo-Toa already have registered bodies. |
| `spell-icons-1000/bmp/` excluding `crossed-swords.bmp`, `open-book.bmp`, `compass.bmp`, `mining.bmp`, `anvil.bmp`, `scroll-unfurled.bmp`, `magnifying-glass.bmp`, `swap-bag.bmp`, `laurel-crown.bmp`, `imp-laugh.bmp` | Remaining game-icons.net conversions | CC BY 3.0; attribute each used icon's author and Praxiiz | P436 section, rank, achievement, and currency icons. The excluded names are already gumps 22459-22468. Exact authorship must be resolved per new icon. |
| `erads-custom-content/` excluding imported bank-chest linings and crate skins | Remaining status, paperdoll, clothing, chess, and terrain art | Author permits use; credit Erachiro; IP for franchise looks; check individual files | P436 optional stone interface or League-room decor. P362 already imports the bank and crate skins. Remaining file selection is unverified. |
| `uo-art-mods/` excluding the imported Magic Scrolls subset | Item variants, environment art, and UI collections | CC0 1.0 author license; EA still applies; credit CorvaeOboro by convention | P436 frames or spell accents, crafting reward icons, or biome dressing. Subsets duplicate separate packs; do not count them twice. Remaining individual files are unverified. |
| `vrark-animations/` excluding the registered crate creature and Vanguard scamps | Large creature, miniature, trophy, and static-art collection | RIP/IP; rename; source-specific credits and terms | Added League hunt families, bosses, mounts, and trophy rooms. The library calls out newer horse, unicorn, beetle-rider, and mounted-knight art. No individual new Vrark file is cleared by this note. |
| `mobile-megapack/`, `uo-pixel-monsters/`, `gnolls/`, `orc-encampment/`, `display-cases/`, `hestia-trophies/`, `trophies-heads/`, `mrriots-christmas/`, `mrriots-winter/`, and `winter-holiday/` | Other partially imported creature, trophy, camp, and seasonal packs | Per-file SOURCE and existing registry terms; EA/RIP/CREDIT vary | More hunt, hall, and seasonal choices after a file-level comparison. These packs are not labeled wholly unused here. |

## Registered art that still lacks a feature assignment

P365 records the calves as waiting for a line. Registry bodies `2129`, `2130`, `2131`, and `2132` are the brown, spotted, red, and piebald calves from `uo-pixel-animals/prapilk_rindviehcher/L_01.vd` through `L_04.vd`. Their registry terms say no license stated, credit Prapilk, player package or private repo only, and no reposting. A farm pet line, tutorial farm youngster, or noncombat farm reward could use them.

Checked `server/customizations/Mobiles/Evo/ShardBodyTypes.cs` and `EvoPetData.cs`, plus tracked customization references to these decimal values. The body declarations exist, but no calf evo-line assignment was found. Other numeric hits are hues, coordinates, clilocs, or the unrelated hex item ID `0x2131`. This establishes a source-level gap only. Save contents and live placements are unverified.

The guild-hall packs from P265 are a different case. Bubble vat, creature tanks, flasks, crystal ball, blacksmith, firepit, floating crystals, arc orbs, marble railings, and the round towers already have registry rows and decor templates. They are not unused merely because the old library still says disk. The same applies to P365's Thagoras mounts, riding drake/bear/wolf/saddle, foals, and young lizards; P362's optional container/scroll skins; P243's trophy selections; and P81's separate SoS paperdoll vendor. No claim about whether those have been published or placed is made here.

## Evidence not promoted to an unused-art claim

The SoS paperdoll builder kit is already used by a separate vendor. Its unshipped source formats, animations, and body variants are not a new unused pack. `runebook-gump` is code rather than a ready art set. Audio and queued downloads are outside this report. The main catalog records only a file witness per set; duplicate copies inside broader collections remain possible.

## What remains unverified

No visual quality review, animation import test, free-ID allocation, licensing recheck with authors, or live usage audit was performed. A feature suggestion does not mean the corresponding ModernUO behavior exists. Maps, ships, wearable art, flying-only ambience, and mount animations each need implementation work beyond registering an image. Juvenile puppy, kitten, fox kit, and chick art remains an unresolved library gap. This task did not generate, move, copy, register, or add any art.

P538 DONE
