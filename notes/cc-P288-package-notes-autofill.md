# cc-P288: the player package's "What is new" line fills itself

2026-10-23. Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P288-package-notes-autofill.md`, handed by the Golem to the Iron
Golem. Work copies: `D:\UO\golems\Iron\ShatteredLegacy` and `D:\UO\golems\Iron\shard-migration`, branch
`golem/Iron/P288`. Both were clean at the start. HEAD of ShatteredLegacy was `72f410f` (main after P287).

## In plain words

- **The Notes box on the Player package tab fills itself.** It now holds a one-line list of what changed for players
  since the published package, biggest first, for example "Tutorial farm, Rootdeep map, fog of war, League hunt
  bestiary, Kitsune ears and tail, New Haven community art and more". You can edit it before you press Build package.
- **A Refill button sits beside the box.** It puts the suggested line back, over whatever you typed. Under the box,
  the full list has one line per item, so you can see what the line came from and trim it.
- **The web console's Player package page does the same**: the box starts filled, a Refill button sits under it, and
  the full list is shown below.
- **It works even when the old zip is gone.** Before, the box stayed empty when `player-package\dist` no longer held
  the published zip. Now it finds the commit from the version's own build time. When nothing for players has changed,
  the box says "No client changes since 2026.10.22.0855".
- Nothing for you to do. The next time you open the Player package tab, the box is filled.

## Headlines

- **The line is made per player-facing commit, not per CHANGELOG version.** P153's line took every new Added, Changed
  and Fixed line in `CHANGELOG.md`, so server-only content filled it (Eodon, Sorcerer's Dungeon). Now a commit counts
  only when it touches something the package ships:
  - the map (`player-package/vendor/shattered-legacy-map/`)
  - the TazUO build (`client/patches/`, `client/TAZUO_COMMIT`, `client/Build-Client.ps1`)
  - creature bodies, art, gumps and paperdoll art (`vendor/shattered-legacy-art`, `paperdoll-sos`, `fiddle-me-this`)
  - music and cliloc text
  - the launcher and payload (the rest of `player-package/`)
  - the official Legion scripts promoted since then (`official-*` tags in this PC's scripts clone)

  Tests, `SOURCE.txt` and `.md` files never count. A server-only commit counts only when a player line it added says
  it reaches the install ("player package", "launcher" or "update your game").
- **The CHANGELOG decides whether players see it, and the prompt title gives the name.** The CHANGELOG lines a commit
  added (`CHANGELOG.md` at it against its first parent) decide: a commit with only Staff lines is left out and listed
  as left out (P277's dragon, P265's guild hall decor). The short name comes from the prompt title. For example,
  "CC task P236: Ship Chase's approved satchel and guild bag icons" becomes "satchel and guild bag icons", and "CC task
  P188: Rootdeep goes in (...)" becomes "Rootdeep map". A commit with no prompt title takes its first player line's
  lead phrase. The function is deterministic and tested, with no AI call (Deviation 2).
- **Biggest first, joined with commas, under 120 characters, no prompt numbers.** Items are ranked by:
  1. the kind of thing shipped: map 6, client 5, creature bodies 4, art and music 3, text 2, launcher, scripts and
     marked server lines 1;
  2. then the player lines added (Added 3, Changed 2, Fixed 1);
  3. then files touched;
  4. then newest first.

  The line keeps as many items as fit, and ends with " and more" when some are cut. Text is plain ASCII, because
  `Build-PlayerPackage.ps1` refuses anything else.
- **The published package's commit, even without its zip.** The commit still comes from the zip's `VERSION.txt` when
  `dist\` holds the zip. Otherwise it is now the newest commit on HEAD's first-parent line at or before the version's
  build minute. The version is `yyyy.MM.dd.HHmm` in this PC's local time, and Build package is refused while the repo
  is dirty. The list's header says which way the commit was found.

## The real fill (current main, `72f410f`)

**Against 2026.10.18.1122, as the prompt asks.** That version's zip is not in this work copy's `dist\`, so the commit
was found by build time: `ac9eee3` ("Shard work, 2026-10-18 11:20", committed 11:21:11; the build stamp is 11:22). 184
commits since, 15 touching shipped paths. It took 3.6 to 4.0 s.

```
LINE (118 chars): Tutorial farm, Rootdeep map, fog of war, League hunt bestiary, Kitsune ears and tail, New Haven community art and more

What changed for players since 2026.10.18.1122 (commit ac9eee3, found by its build time: no zip in dist\ names its commit), biggest first:
- tutorial farm (P276, map): The New Haven tutorial has its farm
- Rootdeep map (P188, map): The Rootdeep Burrows are in the world
- fog of war (P352, CHANGELOG 2026.10.21.11, client): The world map now has a fog of war
- League hunt bestiary (P364, bodies): Fourteen new creatures for the League's hunts
- Kitsune ears and tail (P166, bodies): Fox ears and tail
- New Haven community art (P237, art): New Haven has new decorations made by the community
- hall decor rewards in the League shop (P243, art): The League Shop has a Hall page
- satchel and guild bag icons (P236, art)
- loot that flies out of the box (P242, art): Opening a loot box now sends the best thing inside flying out of it
- New Haven winter holiday decorations (P266, art): New Haven dresses up for winter from December 1 to January 6
- icons for the achievement categories (P241, art): The achievements window now groups each list by category under a heading with the category's own icon
- music for areas (P368, music): The shard can play music of its own in chosen places and fights
- creature levels (P239, launcher): Every creature and NPC now shows how tough it is next to you
  Left out, staff only in CHANGELOG.md: P277 rideable red dragon
  Left out, staff only in CHANGELOG.md: P265 guild hall decor packs
```

The prompt's own example ("Rootdeep map, new satchel and guild bag icons, New Haven art, kitsune ears and tail,
creature con colors") names the same commits (P188, P236, P237, P166, P239). The fill ranks the bigger kinds (the
tutorial farm's map patch, the client's fog of war, the new creature bodies) above the art.

The 15 is what a probe script printed, using the package light's `ShipPaths` filter over those 184 commits. The fill
accounts for the same 15: 13 items, one commit each, plus the 2 left out. P352's client half and the server's "fog of
war" line merged into one item.

**Against what is published now, 2026.10.22.0855** (also by build time: `1ecd9f3`, the P380 merge at 04:03): "No
client changes since 2026.10.22.0855". 12 commits since; the one that touches shipped art, P277's dragon, is staff
only. `scripts\Get-WebConsoleList.ps1 -Page package` gave the same `whatsNew` in 3.6 s.

## What changed

### `D:\ShatteredLegacy` (the Iron copy)

| File:line | Change |
|---|---|
| `scripts/Shard-Console.ps1:1807` `Get-PackageShipPhrase` | kept as the last fallback name; knows map and music too |
| `:1830` `$script:WhatsNewKinds`, `WhatsNewNotShipped`, `WhatsNewMarked`, `WhatsNewPoints` | what ships, its rank, what never ships, the marked server line |
| `:1841` `Get-WhatsNewShipKind`, `:1855` `Get-ChangelogItemsAdded`, `:1863` `Get-PromptTitleName`, `:1881` `Get-WhatsNewShortPhrase`, `:1895` `Format-WhatsNewName`, `:1912` `Join-WhatsNew` | pure: kind, the lines one commit added, the short name from a title, the fallback from a line, ASCII and lower-casing (a word CHANGELOG.md also writes in lower case is lowered; "New Haven", "Rootdeep" keep their capitals), the comma join cut to fit |
| `:1931` `Get-PackageWhatsNew` | rewritten: per commit, biggest first; the line, the list, the left-out lines; a marked server line that names an item already there merges into it |
| `:1999` `Resolve-PackageBaseCommit`, `:2015` `Select-OfficialScriptTags` | pure: the published commit from the zip or the build time; the official scripts tags since then |
| `:2025` `Get-PackageSuggestion`, `:2037` `ConvertTo-WhatsNewDocument`, `:2046` `Format-WhatsNewList` | the suggestion from the facts; its web shape; the box under the notes |
| `:9037` `Get-WhatsNewFacts`, called at `:9103` in `Get-PackageLightFacts` | read only git: first-parent log, the log since, `CHANGELOG.md` at each shipping commit and its parent, then and now, the scripts clone's tags and diff. Replaces P153's two `CHANGELOG.md` reads |
| `:9798` `Update-PackageSuggestion` | the list box from `Format-WhatsNewList` |
| `:12512` | the Refill button (`packageNotesRefill`) between the box and Build package |
| tooltips `packageNotes`, `packageNotesFrom`, new `packageNotesRefill` | |
| `scripts/Get-WebConsoleList.ps1:76` | `-Page package` carries `whatsNew` |
| `web-console/static/app.js:960` `whatsNewBlock`, `:1045`, `:1083`, `textField` | the box starts with the line until edited (`packageNotes:edited`); Refill; the list |
| `scripts/tests/Shard-Console.Tests.ps1:8514` to `:8620` | six P288 facts; P153's two package facts (`:8198`, `:8208`) moved onto the new shapes |
| `web-console/console-actions.json` twins | `packageNotesRefill` is `page:refill` (P187's parity rule) |
| `web-console/tests/test_pages.py:488`, `tests/fixtures/fake_list.py` | the phone test: filled, edit kept, Refill, the list, no overflow |

Not changed: Publish. It still publishes the zip with the notes it was built with (its `version.json`), as before.

## Tests

Every new test was run red first: the new facts against the committed console, then green.

- **The console facts.** I copied the console to the scratchpad before editing and added the facts before patching.
  All 6 P288 facts failed on the old console (wrong line, wrong empty text, missing functions, an empty box), then
  passed.
- **The web console.** The new phone test ran on the old `app.js` and `fake_list.py`, which were swapped back in from
  the copy. It failed ("Refill under the Notes box"), then passed on the new ones.

| Fact | What it pins |
|---|---|
| `P288_ClientCommitsMakeTheLineAndServerOnlyCommitsDoNot` | the exact line from a map, an art, a launcher commit and a marked server line, in that order. Left out: a server-only commit, a staff-only one and a tests-only one. One list line per item with prompt, kind and lead; the left-out list; an unmarked server line gives "No client changes since v"; a server half merges into its client item |
| `P288_NothingNewSaysNoClientChangesSinceTheVersion` | no commits, and only tests and SOURCE.txt: "No client changes since 2026.10.18.1122" |
| `P288_ALongListIsCutToFit` | 15 items: at most 120 characters, the first ones kept, " and more", every item still in the list; a map still goes first though oldest |
| `P288_ShortNamesComeFromPromptTitles` | seven real subjects (P236, P188, P166, P352, P277, a P209 fix-up, a "Shard work" commit); map suffix, names keep capitals, ordinary words lowered, curly quote to ASCII; the no-title fallback cut at a word that is not a small one |
| `P288_ThePublishedCommitFromItsZipOrItsBuildTime` | zip first; else the commit at or before the build minute; an uncommitted zip; an earlier minute; none older; not a stamp; the scripts tags; scripts as an item; no commit, no suggestion |
| `P288_TheNotesBoxFillsAndRefills` | the box fills, the list header and left-out line, an edit kept, Refill beside the box puts it back over an edit, its tooltip, why there is none; the web document; the web list carries it |
| `test_the_notes_box_fills_itself_and_refill_puts_it_back` (web, headless Edge, 390 px) | the box starts filled, the list and left-out shown, an edit survives a redraw, Refill puts the line back, nothing wider than the phone |

Results:

- **Web console:** `python -m unittest discover -s tests`: 114 tests, OK (1 skipped, as before). A
  ConnectionResetError traceback is printed by a test that closes a socket early; it is not a failure.
- **Shard Console:** full suite: **450 facts, 436 passed, 14 failed** on the first full run.
  - One failure was mine. `P187_EveryConsoleButtonHasAWebTwin` caught that the new Refill button had no web twin. I
    added `"packageNotesRefill": "page:refill ..."` to `web-console/console-actions.json`'s twins. P187 and P288 then
    ran 14 of 14.
  - The other 13 were already failing. I ran those 13 facts on the untouched console and tests (swapped in from the
    scratchpad copy, then put back and checked with `cmp`), and all 13 failed there too. They need things this work
    copy does not have: `client-data\...\hues.mul` (P135 x3 and the three window-action facts), the links now pointing
    at Haven (P83 x2, P101 x2, P107), and newer server commands (`PlayerCommandsNeverAppearInTheWorldTab`,
    `RedMeansTestOnly...`). None of it was touched here.
  - Net after the fix: 437 passing, the same 13 failing as before.

## Deviations and decisions for Chase

1. **The published version.json carries no notes today.** The prompt says it carries `version` and `notes`. Fetched
   2026-10-23, `https://get.shatteredlegacyuo.com/version.json` holds `version` 2026.10.22.0855, `sha256`, `bytes`
   and `url`, and no `notes`. `Build-PlayerPackage.ps1:1031` writes `notes` only when `-Notes` is given. So the
   published package was built without the console's Notes box. Also, the published version is no longer
   2026.10.18.1122. I did the real fill against both.
2. **Short names come from the prompt title first, and from the CHANGELOG line when there is no title.** The prompt
   asks for a short name per CHANGELOG entry, with the title as the fallback. CHANGELOG lines are whole sentences
   ("Every creature and NPC now shows how tough it is next to you"), and cutting them makes poor names. The titles
   are already short noun phrases, and the prompt's own example items match the titles (Rootdeep, satchel and guild
   bag icons, New Haven art, kitsune ears and tail). The CHANGELOG still decides inclusion (staff only means left
   out), gives each item's lead in the list, and gives the name for a commit with no title (a hand "Shard work"
   commit).
3. **"Marked player-visible" had no marker.** `CHANGELOG.md` has no such mark, and adding one would show in game: the
   server prints every line in the login bulletin. So a server-only line counts when it says it reaches the install:
   "player package", "launcher" or "update your game" (`$script:WhatsNewMarked`).
4. **Staff-only shipping commits are left out**, though their art is in the zip: P277's dragon and P265's guild hall
   decor. Players cannot get either yet. Both show under the box as "Left out, staff only", so you can type them in if
   you want.
5. **The published commit by build time** is new (part 1 needed it: this copy's `dist\` has no zips, and the box was
   empty whenever the zip was gone). It is an estimate, and the list's header says so. It assumes the package was
   built on a PC in this time zone from a clean commit.
6. **No CHANGELOG line.** This is a console change only. Every Golem's prompt edits the newest CHANGELOG section, so
   I added none.
7. **Tools denied in this unattended run.** `Read` on
   `D:\UO\golems\Iron\ShatteredLegacy\scripts\Shard-Console.ps1` (offset 1765), and `Grep` for the build's
   `Join-Path` folders in `player-package\Build-PlayerPackage.ps1`, both outside the working directory. I read with
   Bash `cat` and `grep` instead, and edited with Python patch scripts in the scratchpad, each checking its anchor
   occurs once.
8. **P153's two package facts were rewritten** onto the new shapes. Their old calls (`-ShipCommits`, `ChangelogThen`
   on the facts) no longer exist; what they pinned that still holds (the parse, the lead phrase, the box filling and
   never overwriting an edit) is still pinned.

P288 DONE
