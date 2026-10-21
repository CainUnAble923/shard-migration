# cc-P177: one look for every guild menu (survey and mockups)

2026-10-21, Gold Golem. Branch `golem/Gold/P177` in both repos. Research, design and mockups: no menu is converted, no
guild behaviour changes, players see nothing new. Chase, 2026-10-18 20:30: "all guild menus need to be uniform in UI
and style, we may need to add some art? if possible to help differentiate while in menu".

**Open the index page:** `notes\art\guild-menus\index.html` (mockups, crests, survey table and 40 survey renders).

## Headlines

- **Survey: 40 guild menus, rendered.** Every guild menu a Journeyman member sees today, dumped from the server's own gump
  entries and drawn with EA's art (`notes\art\guild-menus\survey\`, table in the index page and below). They already
  share one frame (9270) and one rule (9304), but almost nothing else:
  - **sizes**: 26 different ones, from 560 x 144 (the recipe shop) and 360 x 260 to 760 x 540 and 380 x 662;
  - **30 of 40 are see-through** (an alpha region); 9 are solid (cc-P169's 2624 panel); the Clean Up store is built
    from scroll images;
  - **headings**: 25 of 40 use hue 1154, which TazUO draws **green** (cc-P169), so on most menus a title looks like a
    met requirement; 15 use only 1153 (white);
  - **buttons**: the same arrows mean different things (4005 and 4011 both "open"; 4014 back; 4017 and 4023 both close);
  - **requirements** in four styles: cc-P169's lines (only the Hammer and Jacob's upgrades), green / red labels, yellow
    `#FFD700` HTML, and plain gray text;
  - **headers**: a centred title, sometimes the NPC's name; rank and currency lines in a different place on every
    guild's menu; **no menu has any art that tells one guild from another.**
- **The template: `GuildMenuGump`**, `server\customizations\GuildMenuGump.cs` (new, 431 lines), proposed for cc-P178. One
  layout, 560 wide:
  - **header**: the guild's crest (60 x 60), its name in its accent colour, a subtitle (the NPC, or "Guild book"), the
    rank line ("Rank: Journeyman", "Standing 6,200 / 15,000 to Master") and the guild's currency at the right;
  - **left section list**: the open section in the accent colour, the rest arrow buttons;
  - **content**: headings, fields, action rows, item rows (art, name, note, price green or red, buy arrow live only
    when you can) and cc-P169's requirement lines with the action under them;
  - **footer**: Back, "Page 2 of 3" with arrows that gray out at the ends, Close;
  - **opaque** (cc-P169's panel), headings ice white (1153), so green and red only ever mean met and not met.
  - **Per guild only**: crest, accent hue and content (`GuildMenuThemes`, one line each).
- **Art: the client already has guild crests.** Gump art **5545 to 5592** is the classic gold guild-medallion set
  (60 x 60): anvil, pick, wizard's hat, scissors, gears, ankh, lute, hooded thief, crossed swords, bow, fish, coins,
  tree, shuriken and more. **Fourteen guilds get a fitting stock crest.**
  - **No crest**: the Custodians and the Keepers of the Last Door. They draw a placeholder, the 9270 frame at crest
    size with a broom or a skull in it.
  - **Stand-ins**: the Artificers (5585, a glowing blade), the Alembic (5583, a provisioner's table), the League (5545,
    Britannia's sigil).
  - `notes\art\guild-menus\art-requests.md` asks the art lane for those five, matching the stock set, on gump IDs
    22459 to 22463 (free here; recheck on the game PC).
  - `ART-LIBRARY.md` is not on this PC (see Deviations).
- **Mockups** (`notes\art\guild-menus\mockup-*.png`):
  - Society of Smiths: Overview (rank ladder and next rank) and the Seal Catalog;
  - Miners' Compact: Restoration (requirement lines);
  - Artificers' Order: Work Orders;
  - The Custodians: the Clean Up store on the template, with the placeholder crest;
  - the League: the Rank page (it fits the base);
  - the guild book tier-1 page for cc-P178: remote repair of the Hephaestus hammers, and what each later tier unlocks
    by rank.
- **Tests: 4 new facts, each seen red first.** Full gate `docker/uo/build.sh -t sl-modernuo:cc-P177`: **1,871 tests,
  1,867 passed, 4 skipped**, image built. A pre-existing test, `WispOrbPossessionVerification` (ForestNymph vs
  Phantom), failed 2 of 6 runs with unchanged code (see Deviations).

## The survey

Every row is one menu as a Journeyman member sees it (standing 6,200, 1,240 of each currency). Source paths are under
`server\customizations\`, at the constructor. "Inside": see-through (alpha region) or solid (2624). The renders are in
`notes\art\guild-menus\survey\today-<name>.png`.

| Menu | Source | Size | Inside | Buttons | Label hues | HTML colours | P169 lines |
|---|---|---|---|---|---|---|---|
| Guild Directory | `ClusterFGuildSystem.cs:879` | 760x540 | see-through | 4005, 4011, 4014 | 37, 53, 999, 1154 | AAAAAA | no |
| Hall page (every guild without its own menu: Tailors, Thieves, Alembic, Arcane, Tinkers, Healers, Bards, Warriors, Maritime, Merchants, Dojo, Keepers) | `ClusterFGuildSystem.cs:1052` | 520x400 | see-through | 4011, 4017 | 37, 68, 999, 1154 | AAAAAA, DDDDDD | no |
| New Haven welcome | `ClusterFGuildStarterPath.cs:795` | 420x260 | see-through | 4005, 4017 | 999, 1154 | DDDDDD | no |
| Starter items (any guild) | `ClusterFGuildStarterPath.cs:845` | 560x192 | see-through | 4014, 4017 | 999, 1154 | | no |
| Smiths guildmaster | `SmithGuildmasterGump.cs:53` | 380x662 | see-through | 4005 | 68, 990, 999, 1153, 1154 | AAAAAA | no |
| What are Smithing Seals? | `SmithGuildmasterGump.cs:371` | 360x260 | see-through | | 1153 | CCCCCC | no |
| Smith Seal catalog | `SmithSealCatalogGump.cs:138` | 500x440 | see-through | 4005, 4006, 4023 | 68, 990, 999, 1153 | | no |
| Smith commissions | `SmithCommissionGump.cs:40` | 420x240 | see-through | 4005 | 37, 999, 1153 | 666666 | no |
| Smith bulk order choice | `SmithBulkOrderChoiceGump.cs:41` | 400x290 | solid | 211, 4005, 4017 | 946, 999, 1153, 1154 | | no |
| Smithing Guild Book (remote book) | `SmithGuildBook.cs:162` | 500x620 | see-through | 211, 4005 | 37, 68, 946, 999, 1153, 1154 | 666666 | no |
| Hammer of Hephaestus restore / upgrade | `HammerOfHephaestus.cs:1118` | 460x616 | solid | 4014, 4023 | 34, 68, 946, 999, 1153 | | yes |
| Hammer familiarity | `HammerOfHephaestus.cs:965` | 480x584 | see-through | 4023 | 999, 1153, 1154, 1638 | 444444, C8A000 | no |
| Miners' Compact liaison (main, dashboard, restoration) | `MinersCompactLiaisonGump.cs:102` | 440x420 | solid | 4011, 4014, 4023 | 999, 1153 | 888888, AAAAAA, FFD700 | no (restoration: yes with a pickaxe registered) |
| Prospector's Logbook (ore log book) | `ProspectorsLogbookGump.cs:70` | 540x510 | see-through | 4023 | 34, 999, 1154 | | no |
| Survey Archivist | `SurveyArchivistGump.cs:66` | 440x420 | see-through | 4023 | 999, 1154 | 888888, AAAAAA | no |
| Jacob's Pickaxe T2 (T3 to T5 the same) | `JacobsReinforcedPickaxe.cs:223` | 440x370 | solid | 4014, 4023 | 34, 68, 946, 999, 1153 | | yes |
| Artificers guildmaster, dashboard | `ArtificersGuildmasterGump.cs:33` | 460x440 | see-through | 4011, 4014, 4023 | 999, 1153, 1154 | 888888, AAAAAA, CCCCCC, FFD700 | no |
| Imbuing table | `ArtificersImbueGump.cs:878` | 530x570 | see-through | 4011, 4023 | 33, 946, 999, 1153, 1154 | | no |
| Essence Satchel mastery | `ArtificersSatchel.cs:173` | 560x540 | see-through | 4005, 4023 | 68, 946, 999, 1153 | | no |
| Artificer work orders | `ArtificerWorkOrderSystem.cs:532` | 580x520 | see-through | 4023 | 946, 1153 | | no |
| Formula book shop | `Imbuing\ImbueFormulaBooks.cs:176` | 520x178 | see-through | 4005 | 999, 1154 | | no |
| Imbue knowledge | `Imbuing\ImbueFormulaBooks.cs:241` | 560x590 | see-through | 4005, 4017 | 946, 999, 1154 | | no |
| Foresters guildmaster, dashboard | `ForestersGuildmasterGump.cs:34` | 440x420 | see-through | 4011, 4014, 4023 | 68, 999, 1154 | 888888, AAAAAA, FFD700 | no |
| Forester's Logbook (log book) | `ForestersLogbookGump.cs:85` | 540x510 | see-through | 4023 | 946, 999, 1154 | | no |
| Outriders (Rangers' League) guildmaster, dashboard | `OutridersGuildmasterGump.cs:34` | 440x420 | see-through | 4011, 4014, 4023 | 999, 1154 | 888888, AAAAAA, FFD700 | no |
| Sanitation Warden (Custodians) | `SanitationWardenGump.cs:47` | 400x445 | see-through | 4005 | 68, 999, 1153, 1154 | 888888, AAAAAA | no |
| Clean Up Britannia store | `Services\CleanUpBritannia\CleanUpBritanniaRewards.cs:308` | images (scroll 0x1F40) | none | 5601, 5603 | 33, 53, 100, 1153 | | no |
| Guild Contract Ledger (any guild) | `GuildContractLedgerGump.cs:45` | 540x490 | see-through | 4011, 4014, 4023 | 999, 1154 | | no |
| Civic Mule Exchange | `CrossGuildExchangeGump.cs:31` | 460x460 | solid | 4023 | 999, 1153 | AAAAAA | yes with a mule |
| Guild recipe shop (any craft guild) | `Engines\Craft\GuildRecipeShopGump.cs:130` | 560x144 | see-through | | 37, 999, 1154 | | no |
| Mule module schematics (any guild) | `Mobiles\Mule\MuleModuleGumps.cs:575` | 480x300 | see-through | 4005 | 68, 946, 999, 1154 | | no |
| League Registrar (main, rank) | `LeagueRegistrarGump.cs:52` | 440x420 | solid | 4011, 4014, 4023 | 999, 1153 | 888888, AAAAAA | yes for a member |

Not dumped (they need a live situation): the Outriders' Crook actions (`OutridersCrook.cs:374`, private), the smith
bulk order turn-in choice (`ClusterFSmithBODPayout.cs:259`, needs a filled deed), and the Thieves' Den, which has no
menu of its own (its guildmaster opens the hall page). The Hephaestus and Jacob's upgrade menus are P169's and already
use its requirement lines.

The survey table and renders come from `GuildMenuTemplateVerification.DumpsTodaysGuildMenus`, rendered by
`notes\art\guild-menus\tools\render2.py` (cc-P169's `render.py` plus item art and a survey row per gump). Limits:
labels from clilocs are not drawn (the Clean Up store's item names), HTML is plain colour and word wrap, and the
backdrop stripes are made up so a see-through window shows.

## The template (part 2)

`GuildMenuGump` (`server\customizations\GuildMenuGump.cs:132`), abstract, in `Server.Gumps`. A menu sets `Subtitle`,
`Rank`, `Sections`, `Section`, `Page`, `PageCount` and `HasBack`, then calls `Build()` (`:188`) at the end of its
constructor. `Build` draws the frame, header, menu and footer, and calls the menu's `DrawContent(y)`.

- **Frame** `:193-195`: 9270 at 560 x 440 (taller on request), cc-P169's solid panel 2624 inside.
- **Header** `DrawHeader` `:207`: crest at 18,16 (or the placeholder); the name at 94,18 in the accent hue; the
  subtitle under it in gray (999); "Rank: X" in white (1153) and the standing toward the next rank in gray; the
  currency name and amount at the right; a 9304 rule at y 92.
- **Section list** `DrawMenu` `:242`: rows 26 apart at x 16. The open one is image 4006 with its name in the accent
  hue (no button). The others are 4005 buttons (10 + n) with gray names. A vertical 9304 rule at x 150.
- **Footer** `DrawFooter` `:263`: rule at H - 44; Back (4014, id 1) when the menu has one; "Page n of m" between the
  previous (4014, id 2) and next (4005, id 3) arrows, each gray art with no button at the ends; Close (4017, id 0).
- **Content helpers** (`:303-372`): `Heading` (white, rule under), `Text`, `Paragraph` (wrapping gray HTML for
  prose), `Field` (label and value), `ActionRow` (arrow, words, gray note), `ItemRow` (item art, name, note, price in
  met green or not met red, the arrow live only when you can take it), `Requirements` (cc-P169's `RequirementList`
  lines, summary and action).
- **One requirement rule**: P169's, unchanged. Met is green with a check (211). Not met is red with an X (5231), with
  how much more. Info is gray. The action is live only when every line is met. "Partly met" is not a third colour: a
  count line shows "10 / 25 (need 15 more)" in red until it is met. Prices on item rows use the same green and red.
- **Responses** `OnResponse` `:389`: 0 close, 1 back, 2 and 3 page (ignored past the ends), 10 + n section (opens its
  first page), 100 and up the menu's own (`OnContentButton`). The menu implements `Reopen(pm, section, page)`.
- **Per guild** `GuildMenuThemes` `:52`: key, name, accent hue, crest gump (0 for none) and the placeholder's item.
  The accents avoid the met, not met, info, heading and disabled hues, and are all different (T1). `Get` of an
  unknown key gives a plain theme (white, placeholder).
- **Rank line** `GuildMenuRank.For(key, data)` `:95`: the guild's own rank names (`ClusterFGuildSystem.GetRankName`),
  its ladder (`RankThresholds`) for the next rank, and its currency name (`MuleUpgrades.CurrencyName`). The
  Custodians (Clean Up points) and the League (Renown, metal ranks) pass their own values to the record.
- **The League (cc-P179)** has the theme `league` (5545, steel blue) and uses the same base: the mockup shows its Rank
  page. Its Register book would be a template menu whose sections are the bound guilds' action lists.
- **Guild books (cc-P178)** are template menus: sections are the book's tiers, each tier's actions gated by rank. The
  mockup shows tier 1 (repair) and the later tiers as requirement lines. Chase asked for the small book art for the
  books themselves (the item); the window is the template either way.

## Art (part 3)

- `D:\UO\ART-LIBRARY.md` is **not on this PC** (nor the art packs, per this PC's notes). I searched the client's own gump
  art instead: all 5,571 entries in `gumpartLegacyMUL.uop` (7.0.117.0), sized, and the 1,451 crest-sized ones (36 to
  120 px, near square) laid out in contact sheets. Families found:
  - **5545 to 5592**: gold guild medallions, 60 x 60, normal and pressed pairs. Chosen.
  - 1001 to 1038: gold-framed profession icons, 64 x 64 (anvil 1030, bow 1029, lute 1031, dagger hand 1038, axe on a log
    1036). They fit too, but are fewer and square.
  - 2730 to 2800: painted portraits (a miner 2757, a smith 2760, a tinker 2740). Too busy for a crest.
  - 7000 to 7064 and 20480 to 21642: spell and skill icons. Wrong style.
- Crest per guild, accent and placeholder: `crests.png`; the table is in `art-requests.md`.
- **Banners and borders**: none requested. The stock frame, panel and rules are what make the menus one set; the crest
  and the coloured name are the difference.
- **Requests**: five crests, in `notes\art\guild-menus\art-requests.md`: size, style, one line each, reference
  renders, IDs and the deliverable.

## Mockups (part 4)

`notes\art\guild-menus\`, drawn by `GuildMenuTemplateVerification.DumpsTheMockups` (the template's real entries) and
`tools\render2.py`:

| File | What it shows |
|---|---|
| `mockup-Smiths_Overview.png` | Society of Smiths, Overview: the rank ladder (reached ranks met, the rest gray), the next rank as requirement lines |
| `mockup-Smiths_SealCatalog.png` | Seal Catalog page 1 of 3: item rows, prices green / red, buy arrows gray when you cannot pay |
| `mockup-Miners_Restoration.png` | Miners' Compact Restoration: requirement lines, "1 requirement not met", Restore grayed |
| `mockup-Artificers_WorkOrders.png` | Artificers' Work Orders page 1 of 2: action rows with notes, fields |
| `mockup-Custodians_Rewards.png` | The Custodians' Clean Up store page 1 of 4, the placeholder crest |
| `mockup-League_Rank.png` | The League's Rank page on the same base |
| `mockup-SmithsBook_Repair.png` | Guild book tier 1 (cc-P178): remote repair of both Hephaestus hammers; tiers 2 and 3 locked by rank |

The numbers in the mockups are examples, not proposals. In particular, the repair prices ("40 gold, 1 Seal") are
cc-P178's to set.

## What changed, file:line

| File | Change |
|---|---|
| `server\customizations\GuildMenuGump.cs` (new, 431 lines, 17 KB) | `GuildMenuTheme` `:39`, `GuildMenuThemes` `:52` (19 themes), `GuildMenuRank` `:95`, `GuildMenuGump` `:132` (Build `:188`, header `:207`, menu `:242`, footer `:263`, helpers `:303-372`, OnResponse `:389`). Nothing uses it yet. |
| `server\tests\Misc\GuildMenuTemplateVerification.cs` (new, 538 lines, 27 KB) | T1 to T4 and the two dumps, below |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.21.2`, one `### Staff` line; VERSION `2026.10.21.2` |
| `shard-migration\notes\art\guild-menus\` (new) | `index.html`, `art-requests.md`, 7 mockups, `crests.png`, `stock-medallions.png`, `survey\` (40 renders), `tools\` (the render scripts) |

## Tests

`server\tests\Misc\GuildMenuTemplateVerification.cs`:

- **T1** `T1_EveryGuildAndTheLeagueHasATheme` (`:148`): every registered guild and the League has a theme with its
  own name; accents are not met, not met, info, heading or disabled, and all differ; each crest is in 5545 to 5592 or
  0 with a placeholder; exactly the Custodians and the Keepers have no crest.
- **T2** `T2_TheFrameHeaderAndContentArea` (`:186`), for the Smiths (crest) and the Custodians (placeholder): frame
  9270 at the menu's size, 2624 under the inside, no alpha region; the crest or the placeholder frame and item in the
  header; the name in the accent hue; a rank line; every label and button inside the frame; the six content labels
  above the footer's rule.
- **T3** `T3_SectionsAndPaging` (`:244`): the open section has no button, the selected art and an accent label;
  every other section is a button; "Page 1 of 3"; at page 1 previous is gray art with no button and pressing its id
  does nothing; next opens page 2; a section press opens its page 1; an id past the sections does nothing; at the
  last page next does nothing and previous works.
- **T4** `T4_RequirementsAreTheP169Lines` (`:290`): met and not met lines in their hues with the check or X beside
  them, the action button only when all are met, the summary's words.
- `DumpsTodaysGuildMenus` (`:347`) and `DumpsTheMockups` (`:413`) are not facts; they write GUMPJSON lines for the
  renders (run with `--logger 'console;verbosity=detailed'` on the builder image to see them).

Seen red first:

- **Red A** (four faults in `GuildMenuGump.cs` marked `RED-RUN MUTATION`: the Custodians' name misspelled, an alpha
  region for the panel, page arrows always live, the action always live): `Total tests: 1871, Passed: 1863,
  Failed: 4`, the four new facts. T1 `Expected: "The Custodians"`, T2 `Assert.Contains() Failure: Filter not matched`
  (no 2624), T3 `Assert.DoesNotContain() Failure ... Found: 2` (a previous button on page 1). T4 failed for the wrong
  reason: `Assert.Single() Failure: The collection contained 2 matching items` (the header's "Smithing Seals" label as
  well as the line's). I fixed the test to match the line only.
- **Red B** (the same faults, the fixed T4): `Failed: 4`, T4 now `Assert.Equal() Failure: Expected: False, Actual:
  True` (the Repair button live with a line not met).
- **Green** (faults removed; `grep -rn RED-RUN server/` finds nothing): `Total tests: 1871, Passed: 1867, Skipped: 4`,
  "Built sl-modernuo:cc-P177 with patches applied and 1867 shard test(s) passing."

## Deviations and decisions for Chase

- **A flaky test, not mine:** `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant
  (ForestNymph, Phantom)` failed in 2 of 6 gate runs ("the possessed creature never took the foe as its Combatant: the
  fight did not start", `WispOrbPossessionVerification.cs:301`) and passed in the other four with the same code. This
  task touches no AI or combat code. It is timing-dependent (30 seconds of 250 ms ticks for the fight to start). Worth a
  small task to make it deterministic.
- **The template class exists but nothing uses it.** The prompt asked to propose the class and where it lives. I wrote
  it so the mockups are the server's own output rather than hand drawings, and so cc-P178 starts from tested code. If
  you want a different look, cc-P178 changes this one file.
- **ART-LIBRARY.md and the art packs are not on this PC.** The crests are the client's own medallions. The scout's
  library may have better community art; a game-PC agent can check it against `art-requests.md`.
- **Free gump IDs 22459 to 22463** read free on this PC, but its check could not see the shipped vendor art or the TazUO
  source. Recheck on the game PC before registering.
- **"Partly met" is not a third colour.** The prompt asked for met / not met / partly met under one rule. cc-P169's rule
  has two states plus info. A count that is partly there reads red with "(need N more)". A third colour (say, yellow
  for 50 percent and up) would make yellow mean something, after cc-P169 removed yellow for exactly that reason. Say if
  you want it.
- **Accent hues** are my picks (`crests.png`). Some are close to each other: the Custodians' cyan and the Alembic's
  teal; the Smiths' orange and the Dojo's amber. Each is one number per guild in `GuildMenuThemes`.
- **The section list replaces the stacked buttons** that every guildmaster menu uses today (Bulk Orders, Contracts,
  Seal Catalog, ... in one column). The Smiths have 8 sections; the list holds 11 at the default height.
- **Width**: 560 is wider than most of today's menus (440). Item names longer than about 26 characters run into the
  price column; cc-P178 shortens or puts the detail on the note line.
- **The guild books** (cc-P178): the window is the template; the small book art you asked for is the item's.
- **Not changed:** every menu in the survey, all guild behaviour.

## For Chase

Look at `D:\UO\shard-migration\notes\art\guild-menus\index.html` (or the seven `mockup-*.png` and `crests.png` beside it).
Nothing changes in game: the test shard image `sl-modernuo:cc-P177` has the new class but no menu uses it, and
`[version` shows 2026.10.21.2.

**Approve this look, or say what to change.** cc-P178 waits in `held\` until you answer.

## Repo size rule

Largest new file: `notes\art\guild-menus\survey\today-Smith_Guildmaster.png` and its neighbours, about 60 to 130 KB each.
All of `notes\art\guild-menus\` is 3.3 MB, with no file over 1 MB. In the code repo, `GuildMenuGump.cs` is 17 KB and
the test is 27 KB. Scratch (build logs, gump size scan, contact sheets) is in the session scratchpad under
`%LOCALAPPDATA%\Temp\claude\`, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (commits nothing): code 4
files pending (`CHANGELOG.md`, `VERSION`, `GuildMenuGump.cs`, the test), docs 59 (this note, `index.html`,
`art-requests.md`, 7 mockups, `crests.png`, `stock-medallions.png`, 40 survey renders, 7 tool scripts). Neither repo
BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P177 DONE
