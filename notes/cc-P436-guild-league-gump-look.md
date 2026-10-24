# cc-P436: a new look for the guild and League gumps from art we already have (step 1: pick)

## In plain words

- **Three new looks are drawn for the guild and League menus, beside today's look.** Each preview shows the same three
  real menus: the Miners' Compact dashboard, the League board and the Foresters' page.
  - **A. Dark Celtic:** a dark frame with Celtic-knot corners and green arrow buttons.
  - **B. Stone and bronze:** a dark basalt frame with a braided bronze edge. It keeps today's buttons.
  - **C. Clean modern:** a flat dark frame with a thin bronze edge. Its art is already in the player package today.
- **The pictures are in** `D:\UO\shard-migration\notes\cc-P436-tools\previews\` (in this branch's copy):
  `overview.png` has all four one under another; `look-*.png` has each on its own.
- **Players will see nothing yet.** No menu has changed and nothing ships until you pick.
- **For you:** pick A, B, C or "none, keep stock" on the Golem card. After your pick, the menus change together, and
  anyone without our client keeps today's look.

## 1. The guild and League gumps today, and the stock art they use

I counted 36 gump classes in `server/customizations/`. A subagent swept the files, and I checked the totals against
the layouts I read myself: MinersCompactLiaisonGump, GuildContractLedgerGump, LeagueRegistrarGump and
ForestersGuildmasterGump.

Every gump below draws **frame 9270** (AddBackground) except LeagueShopGump.

| File:line | Class | Shows | Art besides frame 9270 | Inside |
|---|---|---|---|---|
| GuildMenuGump.cs:132 | GuildMenuGump (abstract) | guild menu template: crest, header, sections, rows (no guild uses it yet) | rule 9304; rows 4005/4007 (selected 4006); back 4014/4016; close 4017/4019; crest gumps 5545-5589 | solid panel |
| MinersCompactLiaisonGump.cs:28 | MinersCompactLiaisonGump | Miners' Compact pages and member dashboard | rule 9304; 4011/4012, 4014/4015, 4023/4025; requirement art | solid panel |
| SmithGuildmasterGump.cs:20, :365 | SmithGuildmasterGump, SmithSealsInfoGump | Society of Smiths pages, seals | rule 9304; 4005/4007, 4023/4025, 4014/4016 | alpha region (8) |
| ForestersGuildmasterGump.cs:20 | ForestersGuildmasterGump | Foresters' Union pages | rule 9304; 4011/4012, 4014/4015, 4023/4025 | alpha region (6) |
| ForestersLogbookGump.cs:26 | ForestersLogbookGump | Foresters' logbook | as above, plus 4014/4016 | alpha region (6) |
| OutridersGuildmasterGump.cs:20 | OutridersGuildmasterGump | Outriders pages | rule 9304; 4011/4012, 4014/4015, 4023/4025 | alpha region (6) |
| OutridersCrook.cs:367 | CrookActionsGump | crook actions | rule 9304; 4011/4012 | alpha region (6) |
| ArtificersGuildmasterGump.cs:19 | ArtificersGuildmasterGump | Artificers' Order pages | rule 9304; 4011/4012, 4014/4015, 4023/4025 | alpha region (6) |
| ArtificersImbueGump.cs:849 | ArtificersImbueGump | imbue, disenchant, unravel | as above, plus 4005/4006 | alpha region (6) |
| ArtificersSatchel.cs:170 | ArtificersMasteryGump | mastery tabs | rule 9304; tabs 4023/4025 or 4005/4006; 4014/4015 | alpha region (6) |
| ArtificerWorkOrderSystem.cs:518 | ArtificerWorkOrderGump | Artificer work orders | rule 9304; 4014/4015, 4023/4025, 4011/4012, 4005/4006 | alpha region (6) |
| SanitationWardenGump.cs:22 | SanitationWardenGump | Custodians' warden | rule 9304; 4005/4007, 4023/4025 | alpha region (8) |
| GuildContractLedgerGump.cs:27 | GuildContractLedgerGump | work order ledger (and the Dispatch Ledger) | rule 9304; 4014/4016, 4023/4025, 4011/4012; scroll 0x15E3/0x15E7, 0x15E5/0x15E9 | alpha region (6) |
| CrossGuildExchangeGump.cs:19 | CrossGuildExchangeGump | cross-guild exchange | rule 9304; 4014/4016, 4023/4025, 4005/4007 | solid panel |
| SmithBulkOrderChoiceGump.cs:18 | SmithBulkOrderChoiceGump | small or large BOD | its own 2624 tile; 9304; 4005/4007; check 210/211; 4014/4016, 4017/4019 | own panel |
| SmithCommissionGump.cs:20 | SmithCommissionGump | commissions | rule 9304; 4005/4007, 4023/4025, 4014/4016 | alpha region (8) |
| SmithGuildBook.cs:122 | SmithGuildBookGump | guild book | rule 9304; 4005/4007, 4023/4025, 210/211; item art | alpha region (8) |
| SmithSealCatalogGump.cs:19 | SmithSealCatalogGump | seal catalog | rule 9304; 4005/4006/4007, 4014/4016, 4023/4025 | alpha region (8) |
| ClusterFSmithBODPayout.cs:247, :516 | SmithTurnInChoiceGump, RegularSmithBulkOrderGump | bank or cash out; small or large | rule 9304; 4005/4007, 4017/4019 | alpha region (8) |
| ClusterFGuildSystem.cs:808, :1030 | GuildProgressGump, GuildTaskDetailGump | guild progress, task detail | rule 9304; 4005/4007, 4011/4012, 4014/4016, 4023/4025, 4017/4019 | alpha region (10) |
| ClusterFGuildStarterPath.cs:791, :839 | GuildWelcomeGump, GuildStarterItemsGump | starter path | rule 9304; 4005/4007, 4017/4019, 4014/4016 | alpha region (10) |
| Engines/Craft/GuildRecipeShopGump.cs:121 | GuildRecipeShopGump | recipe shop | 4005/4007 | alpha region (10) |
| Mobiles/Mule/MuleModuleGumps.cs:568 | GuildSchematicsGump (and the mule gumps there) | mule schematics, bins | rule 9304; 4017/4019, 4005/4007, 4018 | alpha region (6) |
| LeagueRegistrarGump.cs:24 | LeagueRegistrarGump | the League board (field office) | rule 9304; 4014/4015, 4023/4025, 4011/4012 | solid panel |
| LeagueRegister/LeagueRegisterGump.cs:74 | LeagueRegisterGump | the League Register | rule 9304; 4005/4007, 4017/4019, 4011/4012 | solid panel |
| LeagueRegister/LeagueConsolidation.cs:186 | CombinedLogbookGump | logbook picker | 4005/4007 | solid panel |
| LeagueShop/LeagueHall.cs:194 | LeagueHallFacingGump | hall facing picker | 4005/4007 | solid panel |
| LeagueShop/LeagueShopGumps.cs:23 | LeagueShopGump | the League shop | scroll art: 0x1F40, 0x1F42, 0x1F43, 0x39, 0x3A, 0x3B, 0x2635, 0x23C5; 0x837/0x838, scroll arrows, 4011/4012 | none (scroll) |
| LeagueShop/LeagueShopGumps.cs:161, :248, :357 | LeagueShopConfirmGump, LeagueHallGump, LeagueTitleGump | purchase confirm, hall items, titles | 4014/4015; item art; 9304 and 4011 (titles) | solid panel |

**Counts across the 36 classes** (classes sharing a file counted separately):

| Art | Gumps using it |
|---|---|
| Frame 9270 | 35 |
| Rule 9304 | about 28 |
| Solid panel 2624 (`RequirementStyle.AddSolidPanel`) | 10 |
| Alpha region (insets 6, 8 or 10) | about 24 |
| Buttons 4005/4007 | about 24 |
| Buttons 4023/4025 | about 20 |
| Buttons 4011/4012 | about 17 |
| Buttons 4014/4015 or 4014/4016 | about 21 |
| Buttons 4017/4019 | about 8 |
| Requirement art 211 / 5231 | every gump that draws a requirement list |

**What already centralises styling:**
- `RequirementStyle` (ClusterFRequirements.cs) holds the panel, check, cross and action art, and `AddSolidPanel`.
- `GuildMenuGump` and `GuildMenuThemes` are a full template, but nothing uses them.

**What does not:** about 24 gumps still hard-code `AddAlphaRegion`, 9304 and their button IDs, and `BgId = 9270` is
repeated in 11 files. Step 2's style helper replaces those calls, so every gump changes together.

## 2. How new gump art reaches the client

- **The path.** Our gumps ship as PNG files. TazUO loads them from `app\tazuo\ExternalImages\gumps\<id>.png` in
  place of the client's gumpart for that ID. It is the same path Fiddle-Me-This's restyled stock gumps take.
  - The package builder copies our files from `player-package\vendor\shattered-legacy-art\gumps\<id>.png`: exactly the
    registry's `kind=gump` rows, no more and no fewer (Build-PlayerPackage.ps1, the cc-P62 block).
  - Gump art needs no tiledata or animdata: there is no patch record and no `.mul` / `.uop` to build.
- **Already working this way:**
  - the achievement buttons and category icons, 22456-22468 (cc-P147, cc-P241)
  - the advent calendar, 22469 (cc-P266)
  - P362's container and scroll skins, 23052-23080
- **A new gump ID needs, end to end:**
  1. An ID that is free in the client's gumpart, in our registry, in Fiddle-Me-This and in the paperdoll art.
     `scripts\find-free-art.py`'s `gump_reasons` checks all of these; P362's `free_ids.py` wraps it for runs of N.
  2. The PNG in `vendor\shattered-legacy-art\gumps\`.
  3. A `registry.csv` row (`kind=gump`, source, licence, credit), plus a credits line in that folder's SOURCE.txt.
  4. A package build. Its gates count the PNGs against the registry and refuse a clash with Fiddle-Me-This or the
     paperdoll art.
  5. The server sending that ID.
- **A resizable frame takes nine consecutive IDs** (AddBackground draws `id` to `id+8`). A rule or panel is one ID
  drawn with AddImageTiled. A button takes two (normal and pressed).
- **Who sees it.** Only a client with our package has the PNGs. Stock clients draw nothing for an unknown ID, so the
  server has to choose.
  - `TazUOClientCommand.CanRunCommands(ns)` (TazUO/TazUOClientCommand.cs:191) is true only for our patched TazUO,
    which is the client that ships with the package. Step 2's helper uses our IDs for that client and stock IDs for
    everyone else.
  - **Gap:** a patched client running an older package (before the art) would draw blank frames. Step 2 should send
    the new IDs only to a package version that has them. The handshake does not carry the package version today, so
    that needs a small client-side addition.
- **No collision with P362.** P362 skins containers and scrolls client-side, chosen per player, at 23052-23080 and
  art 13049-13112. This look is chosen by the server for its own menus and takes its own free block. A and B change no
  stock ID and no P362 ID. C uses Fiddle-Me-This's own custom IDs, which nothing of ours uses yet.

## 3. The three looks

Pictures: `notes\cc-P436-tools\previews\`
- `overview.png`: all four stacked
- `look-0-stock.png` (today), `look-a-dark-celtic.png`, `look-b-stone-bronze.png`, `look-c-clean-modern.png`
- `pieces-*.png`: each look's own pieces, with their sizes

Each draws the Miners' Compact Member Dashboard, the League board and the Foresters' main page at their real
coordinates. The tools are `gumpkit.py` (a gumpart reader and a 9-slice drawer) and `previews.py`. The text is Tahoma
12 standing in for the UO font, so lines are close in length, not exact. The stock pieces are read from the client's
own `gumpartLegacyMUL.uop`: zlib, then EA's BWT pass, which `cc-P29-tools\cliloc.py` already ports.

| Look | Art (on disk) | Licence and credit | New gump IDs |
|---|---|---|---|
| **A. Dark Celtic** | CorvaeOboro's dark redraw of frame 2600 (`uo-art-mods\...\UI\GumpOverrides\0x0A28`-`0x0A30`: Celtic knots in the corners, dark field), his green arrow (4005/4007) as the row button, his purple X (4017/4019) as close. Back keeps stock. | CC0 1.0 (the repo's LICENSE). Attribution is not required, but we credit "CorvaeOboro, UO Art Mods". It redraws stock IDs, so it goes in as new IDs and never over 2600. | **13**: frame 9, row button 2, close button 2. The rule is the frame's top edge tiled 2 pixels high (AddImageTiled clips), so it needs no ID. |
| **B. Stone and bronze** | Erachiro's Basalt status gump (`erads-custom-content\...\Client\UO Gump Basalt Edition\Character Status Basalt .bmp`), cut into nine pieces: the braided bronze border (corner, edges mirrored) and plain basalt for the inside, measured to avoid its lettering and dividers. Buttons stay stock; their bronze suits it. | "Free to use", credit Erachiro; ship only inside the package. The pieces are cuts of his art, so the registry row should say "cut from". | **9** (the frame). The rule is the top edge tiled 3 pixels high (the braid). |
| **C. Clean modern** | Fiddle-Me-This's custom panel frame 62180-62188 (flat dark field, thin bronze edge). Buttons stay stock. | CC0 1.0 (NewYears1978, already credited in `vendor\fiddle-me-this\SOURCE.txt`). | **0**. The art is already in every package (`[Custom]\ExternalImages\gumps`). It would be the first server use of Fiddle-Me-This's custom IDs, so a later Fiddle-Me-This update must keep them (note it in its SOURCE). |

**Things common to all three:**
- **The inside.** Today a solid stone panel (2624) or an alpha region covers the frame's centre. Each look shows its
  own frame's field instead, so the helper draws no panel for our client.
- **Text is unchanged.** It keeps the gumps' own hues, and those already read on a dark field. A's green buttons are
  the loudest change.
- **The League shop is left alone.** It is already a scroll of its own. If wanted later, CorvaeOboro's dark redraw of
  the scroll background 9380 (CC0, in the same folder) would match A.
- Not tried: spell-icons-1000 icons in the headers. They are CC BY 3.0 with per-author credit, and each look stands
  without them. Step 2 could add rank or guild icons to any look.

**Step 2, in short (after the pick):**
1. Register the chosen pieces under a fresh run of free IDs, ship them, and credit them.
2. One `GuildStyle` helper replaces the frame, panel, rule and button calls in the 36 classes, with today's IDs
   whenever the client cannot show ours. The tests open every gump and check both IDs, ours and stock.
3. Then the docker build and the package gates.

## Stopped for Chase

Asked through `Ask-Chase.ps1` (question Iron-P436-20261024-090945-cbe4): which look (A, B, C, or none, keep stock).

P436 STOPPED: waiting for Chase's pick (asked Chase, Iron-P436-20261024-090945-cbe4)
