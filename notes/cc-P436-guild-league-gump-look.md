# cc-P436: a new look for the guild and League gumps from art we already have

Step 1 (10-24) drew three looks and stopped for Chase. He picked **B, Stone and bronze** (10-25 20:09). Step 2
(10-25, below the step 1 sections) builds it.

## In plain words

- **The guild and League menus now have your pick, the stone and bronze frame:** a dark basalt frame with a braided
  bronze edge. That covers every guildmaster's pages and dashboard, the contract ledgers, the guild directory and
  starter path, the League board, the Register and the League's confirm and title menus: 34 menus, all switched in
  one place. Buttons and text stay as they are; the thin dividing lines become bronze.
- **Only players on our client (the Shattered Legacy package) see it.** Anyone on another client gets today's
  look, unchanged. The League shop is left alone: it is a scroll of its own.
- **For you:** the new frame reaches players in two parts, and both must go out together. The server image is
  `sl-modernuo:cc-P436`. The package must be published **with or before** the server deploy, because the frame's
  pictures travel in the package (players' launchers update it at their next start). If the server goes out first,
  turn the look off until the package is out with the setting `clusterf.guildStyle.enabled` = `False`. Nobody has seen
  it in the game client yet; a quick look at one guildmaster menu after the next package goes out is worth doing.

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

## Step 1 ended waiting for Chase

Asked through `Ask-Chase.ps1` (question Iron-P436-20261024-090945-cbe4): which look (A, B, C, or none, keep stock).
Step 1 stopped there on 10-24. Chase answered on 10-25 at 20:09: **B, Stone and bronze**.

---

# Step 2: look B built (2026-10-25)

Branches: ShatteredLegacy `golem/Iron/P436` (level with main at `57924e6` when I started), shard-migration
`golem/Iron/P436`, which carries step 1's WIP commit `b2bff82` (it sits on an older main; it only adds these notes and
tools).

## 4. The art: gumps 23200-23208

- **IDs.** `notes\cc-P436-tools\free_ids.py` uses `find-free-art.py`'s gump rules on `D:\UO\UltimaOnlineVanilla`. The
  first free runs of 9 started at 22470, 23083, 23200 and 40337. I took **23200-23208** (0x5AA0-0x5AA8), a round
  block away from the end of the last used block (22469). The next art prompt is most likely to start right after
  the last used ID, so this keeps clear of it. No branch in the repository registers any of them.
- **Pieces.** `make_pieces.py` writes the nine PNGs with the exact cut the step 1 preview used (`previews.basalt_frame()`).
  They are in AddBackground's order: top-left, top, top-right, left, centre, right, bottom-left, bottom, bottom-right.
  - Sizes: corners 12x12, top and bottom 96x12, sides 12x96, centre 190x44.
  - All are RGBA and fully opaque. TazUO's `ExternalImageLoader` keeps PNG alpha and keys out no colour, so nothing
    in them goes transparent.
  - `make_pieces.py --check` compares the shipped files with a fresh cut: 9 of 9 match.
- **Registry and credits.** `register_pieces.py` added 9 `kind=gump` rows to `registry.csv`, naming the source BMP
  and the cut, with Erachiro's terms quoted. It also added a section to `vendor\shattered-legacy-art\SOURCE.txt`:
  "Credit Erachiro", ship only inside the package, do not repost.
  - `find-free-art.py --check-registry` (with `--data D:\UO\UltimaOnlineVanilla`): "0 of 781 registered IDs are no
    longer free".
- **The rules.** The bronze braid is the top 5 rows of the top edge (measured: rows 0-4 bronze, 5-11 basalt). A rule
  drawn at 1 or 2 pixels shows the outer rows of the braid. The step 1 preview squeezed the braid to 3 pixels, so the
  real rules are a little thinner than the preview showed.

## 5. The server: one style for 34 gumps

- **`server\customizations\GuildStyle.cs` (new).** It holds `GuildStyle` and `GuildStyledGump`.
  - The gumps still build exactly as before, with stock art. `GuildStyledGump.SendTo` restyles a gump once, as it is
    sent, and only for a client that has our art.
  - **The frame:** 9270 becomes 23200.
  - **The inside:** an alpha region or cc-P169 panel (2624) that fills a frame, starting 0 to 12 pixels in from each
    edge, is removed. The frame's own basalt centre is the inside, and it is opaque.
  - **The rules:** 9304 becomes the top edge (23201) when drawn across, and the left edge (23203) when drawn down,
    at the rule's own size.
  - **Left alone:** buttons, labels, text, item art, other backgrounds, and an alpha region or panel in the middle
    of a gump.
- **Who counts as "has our art".** `GuildStyle.UsesOurArt(ns)` = `clusterf.guildStyle.enabled` (default True) and
  `TazUOClientCommand.CanRunCommands(ns)`.
  - Only our patched TazUO acknowledges the ClientCommand packet, and it ships in the same package as the PNGs.
  - Stock TazUO, ClassicUO and the EA client never acknowledge it, so they never receive an ID they cannot draw. They
    get today's gump, byte for byte.
- **The 34 classes** (`notes\cc-P436-tools\rebase_gumps.py`). One line each, `: Gump` became `: GuildStyledGump`, in
  28 files; every file already imported `Server.Gumps`. The classes:
  - GuildMenuGump, MinersCompactLiaisonGump, SmithGuildmasterGump, SmithSealsInfoGump.
  - ForestersGuildmasterGump, ForestersLogbookGump, OutridersGuildmasterGump, CrookActionsGump.
  - ArtificersGuildmasterGump, ArtificersImbueGump, ArtificersMasteryGump, ArtificerWorkOrderGump.
  - SanitationWardenGump, GuildContractLedgerGump, CrossGuildExchangeGump, SmithBulkOrderChoiceGump,
    SmithCommissionGump, SmithGuildBookGump, SmithSealCatalogGump.
  - SmithTurnInChoiceGump, RegularSmithBulkOrderGump.
  - GuildProgressGump, GuildTaskDetailGump, GuildWelcomeGump, GuildStarterItemsGump, GuildRecipeShopGump,
    GuildSchematicsGump.
  - LeagueRegistrarGump, LeagueRegisterGump, CombinedLogbookGump, LeagueHallFacingGump, LeagueShopConfirmGump,
    LeagueHallGump, LeagueTitleGump.
- **Left out on purpose.** That is step 1's table without:
  - LeagueShopGump: a scroll of its own, with no frame.
  - The two mule gumps beside GuildSchematicsGump, MuleOptionsGump and MuleSellGump: they are mule menus, not guild
    menus.
  - Step 1 said "36 gump classes" but its table lists the classes above plus those three, which is 37. I did not
    re-count step 1's sweep. The list here is the artifact: it is what `S1` pins by name.
- **The kill switch.** `clusterf.guildStyle.enabled` turns the look off for everyone. It is for a server deployed
  before the package carrying the art is published. A patched client on a package without the PNGs would draw blank
  frames, which is the gap step 1 noted. Launchers update the package at every start, so publishing the package
  with or before the server closes that gap. I did not add a package-version handshake; this setting covers it.

## 6. Tests

**Server:** `server\tests\Misc\GuildStyleVerification.cs`, 4 facts. I probed on `sl-uo-builder:cc-P624`, with the
new and changed files bind-mounted and `dotnet test` filtered.

| Fact | What it pins |
|---|---|
| S1 | Each of the 34 classes, found by name, is a GuildStyledGump |
| S2 | 27 real gumps, opened as `DumpsTodaysGuildMenus` opens them, are sent to two Journeymen: one on our client (the real ClientCommand acknowledgement, `OnEnhancedPacket(ns, 00 04)`) and one on a stock client. Ours: frame 23200 and no 9270, no alpha region or panel filling it, no 9304; buttons, labels, text and item art identical to the stock copy, in order. Stock: entries exactly as built, no ID of ours. Both compile and send. |
| S3 | `clusterf.guildStyle.enabled` off: our client gets stock |
| S4 | Restyle on a probe gump changes exactly the frame, two insides and two rules (5), across to 23201 and down to 23203; a mid-gump alpha region, a small panel, another background, a button and a label are untouched |

Results:
- **Red** (the helper present, the gumps still on `Gump`): S1 failed, listing all 34 classes; S2 failed for every
  gump ("our client got no stone and bronze frame", "still got frame 9270", and so on). S3 and S4 passed, as they
  should: they cover new behaviour.
- **Green:** 4 of 4. The six existing `GuildMenuTemplateVerification` facts were run alongside: 6 of 6.
- **Mutants** of GuildStyle.cs, each red:

| Mutant | What failed |
|---|---|
| ignores the switch | S3 ("Collections differ") |
| MaxInset 0 | S4 ("Expected: 5") and S2 ("GuildDirectory: an alpha region still fills our frame") |
| every rule across | S4 (position 4, the downward rule) |

**Package.** I held the package lock for this part.
- **`Build-UoOverrides.Tests.ps1`.** The pinned counts are now 781 rows and 54 gump rows (were 772 and 45). There is
  one new fact, `TheGuildFrameIsNineRegisteredCreditedPngsTheServerDraws`: each of 23200-23208 is registered once as
  a gump crediting Erachiro, its PNG is at the cut's size and RGBA, SOURCE.txt carries the section, and GuildStyle
  draws 23200.
- **Red** on a `git archive` copy of the pre-change tree with the new test file: 2 failed, "expected [781] but got
  [772]" and "gump 23200 registered once: expected [1] but got [0]". 23 passed. **Green:** 25 of 25.
- **The other package test files, green:** Cliloc-Overrides 10/10, Launch-Overrides 18/18, Launch-Settings 27/27,
  Legion-Scripts 24, Map-Overrides 7, Music-Overrides 9/9, Paperdoll-Bodies 9/9, Ui-Skins 4/4.
- **`Package-Client.Tests.ps1`: 3 of 9.** All six failures say "No EA client data in ...\client-data\classic-client".
  This work copy has no client data; P362 recorded the same six. On the pre-change copy it fails the same way (1 of
  9, since that copy also lacks the client folder). It is not caused by this change.
- **The real package build, in place of that test.** I ran `Build-PlayerPackage.ps1 -TazUO <client> -Out <scratchpad>
  -UoData D:\UO\UltimaOnlineVanilla`, never to dist and never published.
  - The default client build `D:\UO\tazuo-sl-build` is stale: it lacks patch 0005, and P362's build lacks 0006 and
    0007. So I built a current client with `client\Build-Client.ps1 -Out D:\UO\tazuo-sl-build-iron-p436`: patches
    0001-0007, 1,318 client tests passed.
  - With that client, every gate passed and it built `ShatteredLegacy-2026.10.25.2108.zip`. The zip carries
    `app/tazuo/ExternalImages/gumps/23200.png` to `23208.png`, 9 of 9.
  - The zip stays in the session scratchpad.

**Gated build.** I held the `docker-build` lock (9.4 GB free at launch) and released it afterwards.
- `docker\uo\build.sh -t sl-modernuo:cc-P436` finished with EXIT=0: "Built sl-modernuo:cc-P436 with patches applied
  and 2481 shard test(s) passing". Of 2,485 tests, 2,481 passed and 4 were skipped (the real-map-data facts); none
  failed.
- The images are `sl-modernuo:cc-P436` = `b441dcaaffaa` and `sl-uo-builder:cc-P436` = `aa7bc94f1407`.
- Memory ran low during the test gate, and Claude Code stopped my background wait loop. The build itself was
  launched detached, kept running and finished. The log is `build-P436.log` in the session scratchpad.
- CHANGELOG: 2026.10.25.9, one Changed line. P624's branch, not yet in main, takes .8.

## 7. Not done, and unverified

- **Not seen in a game client.** The tests prove what the server sends and the build proves what the package holds,
  but nobody has opened a guild menu on our client with this package. A quick look at a guildmaster menu after the
  next package goes out would confirm the frame draws as in the preview.
- **No package-version handshake** (the gap step 1 named). The kill switch and publishing the package first cover it
  instead.
- **Header icons** (spell-icons-1000) were not added, as step 1 suggested was optional.
- The client build `D:\UO\tazuo-sl-build-iron-p436` is outside every repo. The default client folder
  `D:\UO\tazuo-sl-build` is still stale, missing patches 0005-0007. The next real package build needs a current
  client, whoever builds it.

P436 DONE
