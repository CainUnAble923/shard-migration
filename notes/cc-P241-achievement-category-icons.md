# cc-P241: Icons for the achievement categories (CC BY 3.0 game-icons set)

2026-10-21, the Bronze Golem (Opus), branch golem/Bronze/P241 of both repos. Prompt: `cc-P241-achievement-category-icons.md`.
Not committed (the Golem commits after DONE). Both repos were clean at the start. Nothing was run against any world,
nothing was deployed, and the package was not published.

## Headlines

- **Every achievement category now has an icon in the achievements window: ten icons, one per `AchievementCategory`,
  shipped as gumps 22459-22468.** The ten include Mischief, which is the hidden joke set. The prompt was written before
  P231 added Mischief, so its "plus one for hidden achievements" is Mischief's icon (see Deviations).
- **Where the icons show.**
  - Each list (Earned, Not Yet, Retired) is now grouped by category.
  - Each group starts with a heading row: the 44 x 44 icon, then the category's name in a label beside it.
  - On a category's own tab, the list opens on that category's heading.
  - On All, every category the player has rows in gets its heading.
  - The rows keep their own item art as before.
- **The window still reads without the icons.** The name is its own label and does not depend on the art.
  - A player without the package update sees an empty 44 px space beside each name. Our TazUO disposes a gump picture
    with no texture and draws the rest (`GumpPic.cs:31-35` in TazUO 3212623f), and the slots are empty in EA's gump art
    (`find-free-art.py --explain-gump`: FREE).
- **The joke set stays secret.** A Mischief heading appears only once the player has earned a joke achievement, because
  unearned hidden achievements are never listed.
- **The picks, all by Lorc on game-icons.net:**

  | Category | Gump | Icon |
  |---|---|---|
  | Combat | 22459 | crossed-swords |
  | Skills | 22460 | open-book |
  | Exploration | 22461 | compass |
  | Mining | 22462 | mining (a pick) |
  | Crafting | 22463 | anvil |
  | Legacy | 22464 | scroll-unfurled |
  | Discovery | 22465 | magnifying-glass |
  | Collection | 22466 | swap-bag (a sack) |
  | League | 22467 | laurel-crown |
  | Mischief | 22468 | imp-laugh |

  The contact sheet with two alternates each is `notes/art/achievement-category-icons/contact-sheet.png`.
- **Tests.**
  - Server: 3 new facts, each seen red first.
  - Package: 1 new fact, seen red on two mutations.
  - Full gate green: `sl-modernuo:cc-P241`, **1,996 tests, 1,992 passed, 4 skipped, 0 failed** (cycles 3 and 4).
  - P26's gates pass (below).
- **Two flaky gates hit along the way. Neither was caused by this work, and I did not change either** (Deviations):
  - the apply-patches accounting check, a SIGPIPE race;
  - two existing tests: P239's creature-level sampling and a Wisp Orb combat-start timing case.

## 1. Inventory (re-verified on the current tree)

- `AchievementCategory` (`server/customizations/ClusterFAchievements.cs:184-196`; the prompt's `:152` has moved): Combat
  0, Skills 1, Exploration 2, Mining 3, Crafting 4, Legacy 5, Discovery 6, Collection 7, League 8, Mischief 9 (cc-P231,
  "no tab of its own, listed under All").
- Use per category (the `AchievementCategory.X` references): Skills 22, Combat 14, League 11, Mining 9, Exploration 8,
  Legacy 8, Crafting 6, Collection 4, Discovery 4, Mischief 1 (the joke set's own definitions are in
  ClusterFJokeAchievements.cs). Hidden achievements also exist outside Mischief (`hidden: true` at `:394`, `:415`,
  `:519`, `:565`, `:618`).
- **How the gump lays out a category before this change** (`AchievementsGump`, prompt's `:1804`, now `:1855`):
  - **Tabs.** A category is shown only as a tab: `CategoryTabs` holds All plus seven categories, then Quests, on two
    rows (`TabAt`). Collection, League and Mischief have no tab.
  - **The list** (`AddAchievementContent`): the definitions are filtered by the tab, ordered by category and then by
    title, and split into Earned, Not Yet (hidden ones left out) and Retired sections. Each section has a text
    divider.
  - **No category heading anywhere.** On All, the categories run together in each section.
  - **Rows** already carry their own item art (`ItemGumpId`, 88 uses, drawn with `AddItem` at x 14). So the category
    icons go on headings, not on rows.

## 2. Picks

Each icon is chosen for its meaning.
- **Skills:** the open book (learning), not Sbed's abstract rank emblem.
- **Legacy:** the scroll, a record of New Haven deeds.
- **Collection:** the sack, for the gold and the ore sets.
- **League:** the laurel crown (the League of Extraordinary Citizens).
- **Mischief:** the laughing imp.

Alternates (shown on the sheet):

| Category | Alternate 1 | Alternate 2 |
|---|---|---|
| Combat | sword-clash | broadsword |
| Skills | level-four-advanced (Sbed) | brain |
| Exploration | spyglass | boot-prints |
| Mining | mine-wagon (Delapouite) | mineral-heart |
| Crafting | hammer-nails | sewing-needle |
| Legacy | stone-tablet | tattered-banner |
| Discovery | treasure-map | third-eye |
| Collection | locked-chest | gems |
| League | wax-seal | medal |
| Mischief | drama-masks | domino-mask |

All alternates not marked otherwise are by Lorc.

- **Authors.** Praxiiz's zip has no per-author subfolders, despite the prompt and `license.txt`: 1,274 BMPs in one
  `bmp\` folder, and `_zips\Spell_Icons_1_1_0.zip` is the same. So each icon's author is the game-icons.net folder
  that serves it: `https://game-icons.net/1x1/<author>/<name>.html`, tried for all seven authors, 2026-10-21. Every
  candidate resolved to exactly one author. The script is `authors.sh` in the session scratchpad; it reads public pages
  only.
- **Swapping one** is a three-step change:
  - copy another BMP through `scripts\anchor-art-frames.py` to the same gump ID;
  - edit that registry row's source and license;
  - edit the comment in `CategoryIconGumpIds`.
- `notes/art/achievement-category-icons/make_sheet.py` redraws the sheet.

## 3. What shipped

| File:line (ShatteredLegacy) | Change |
|---|---|
| `player-package/vendor/shattered-legacy-art/registry.csv:188-197` | 10 rows, 22459-22468, kind gump, written first by `notes/art/achievement-category-icons/registry_rows.py`. License: `CC BY 3.0, Icons made by Lorc (game-icons.net); conversion by Praxiiz; credit both (...SOURCE.txt)` |
| `player-package/vendor/shattered-legacy-art/gumps/22459.png` to `22468.png` | 44 x 44 RGBA, 1.1 to 2.3 KB each, from `scripts\anchor-art-frames.py --black-transparent --keep-geometry --first-id 22459`. Pure black made transparent and the format converted; nothing else changed. The tool re-read every PNG against its source |
| `player-package/vendor/shattered-legacy-art/SOURCE.txt:313-330` | The set's section, with the credit rule copied from `spell-icons-1000\SOURCE.txt` |
| `server/customizations/ClusterFAchievements.cs:1851` | The gump's header comment: category headings |
| `:1890-1917` | `CategoryRowH` (50), the icon and label offsets, `CategoryIconGumpIds` (every category to its gump), `CategoryName` |
| `:2060-2078` (`PageRow` at `:2060`, `AddSection` at `:2064`) | `PageRow` gains `Category`; `AddSection` adds a heading before each run of one category within a section |
| `:2103-2108` | The three sections are built through `AddSection` |
| `:2134-2139` | The heading row: `AddImage` of the icon at x 16, and the name as a label at x 70, 14 px down (on the icon's middle), hue 1154 |
| `:2257-2258` | `RowHeight`: a heading is 50 tall |
| `server/tests/Misc/AchievementCategoryIconsVerification.cs` (new) | 3 facts, below |
| `player-package/tests/Build-UoOverrides.Tests.ps1:291-296` | The registry ledger: 190 rows, 15 gump rows (+10, cc-P241) |
| `:446-478` | New fact `EveryAchievementCategoryIconIsARegisteredGumpWithItsPngAndItsAuthorsCredit` |
| `CHANGELOG.md`, `VERSION` | 2026.10.21.12 (Added, and Staff) |

shard-migration: this note, plus `notes/art/achievement-category-icons/` (`contact-sheet.png` 680 x 1230, `make_sheet.py`,
`registry_rows.py`).

No records.json entry: gumps need none (`SOURCE.txt`: gumps\<id>.png go to `ExternalImages\gumps\`). The package
build ships one PNG per registered gump ID (`Build-PlayerPackage.ps1:111-121`), so nothing else changes there.

## 4. Free IDs and P26's gates

- `find-free-art.py --data D:\UO\tool-trials\client-data-copy --tazuo D:\UO\cc-p40-work\tazuo-3212623f --explain-gump
  22459 ... 22468`: all ten FREE (before registering).
  - This desk's worktree has no `client-data`, so I used P237's verified copy of the shard's client files (P237 notes
    A3).
  - They follow P147's 22456-22458.
  - Fiddle-Me-This ships 22450-22455, so these IDs are clear of it. No registry row on the newest main uses them.
- `find-free-art.py ... --check-registry`: **0 of 190 registered IDs are no longer free.**
- `validate-art.py --data D:\UO\tool-trials\client-data-copy check-registry`: **0 of 190 rows have problems**; all ten
  gumps ok.
- `player-package\tests\Build-UoOverrides.Tests.ps1`: **17 of 17**.
  - The first run was red on `TheServersCopyOfTheRecordsIsRecordsJsonAndEveryIdIsRegistered` (the ledger said 180
    rows). That was a real consequence of this work, so the ledger was updated (+10 gumps).
- `scripts\tests` (Python unittest): **55 of 55**. `scripts\tests\Art.Tests.ps1`: **12 of 12**.
- Repo size rule: the largest new file is the contact sheet (142 KB). Nothing is over 5 MB.

## Tests

Each new fact was seen failing first:

| Fact | What it pins | Seen red |
|---|---|---|
| `EveryCategoryHasItsOwnIconInTheRegisteredRange` | Every `AchievementCategory` maps to its own gump in 22459-22468, and there is one gump per category | red probe 1 (Combat dropped from the table): "Combat has no icon" |
| `APlayerWithAchievementsInEveryCategorySeesEveryHeadingWithItsIconAndName` | One achievement granted per category (the first without a prerequisite). On All, every category's heading appears with its name in a label beside the icon, and the icon ends inside its row and the list. Every category's tab opens on its own heading and shows no other | probe 1: KeyNotFound for Combat; probe 2 (heading drawn without its name label): "Assert.Single() ... did not contain any matching items" |
| `NoMischiefHeadingUntilAJokeIsEarned` | A fresh player sees no Mischief icon or label on any page of All | probe 2 (hidden locked achievements listed): "Filter matched in collection" (P231's `TheyAreHiddenUntilEarned` failed with it) |
| package: `EveryAchievementCategoryIconIsARegisteredGumpWithItsPngAndItsAuthorsCredit` | Parses the enum and `CategoryIconGumpIds` from the C#. Each ID is registered once as kind gump; its license is "CC BY 3.0, Icons made by <one of the seven authors> (game-icons.net)" and credits Praxiiz; its PNG is 44 x 44; the set's rows are exactly the table's IDs | scratch copy 1 (Mischief dropped from the table): "Mischief has an icon"; copy 2 (Crafting's license without its author): "Crafting's license names its author" |

The probes changed `ClusterFAchievements.cs` in place. The real file was saved first and restored after, and checked
by SHA-256 (0f7e73ca75a75731...) before the green build. The package probes ran on scratch copies.

**Build record** (`docker\uo\build.sh -t sl-modernuo:cc-P241`, each run detached, docker-build lock 09:07-09:20 and
09:25-09:26 CDT, with the Docker VM's page cache dropped before each run when free memory was low). Logs are
`build-P241-*.log` in the session scratchpad.

| Run | Result |
|---|---|
| red probe 1 | 1,996 tests, 13 failed: the 3 new facts and the gump facts that open the window (KeyNotFound), plus P239's flaky `BelowPinnedsCap...` (DeathAdder) |
| red probe 2 | 1,996 tests, 3 failed: 2 new facts (own reasons) and P231's `TheyAreHiddenUntilEarned` |
| cycle 1 | patches gate red: `Stealth-steps-scaled-200.patch - present in /patches but never applied or skipped by name`, although the same log says `Applied: Stealth-steps-scaled-200.patch` (Deviations) |
| cycle 2 | 1,996 tests, 1 failed: `WispOrbPossessionVerification...(Silenii, Phantom)`, "the fight did not start" (its other 6 cases passed); the 3 new facts passed |
| cycle 3 | **green: 1,996 tests, 1,992 passed, 4 skipped, 0 failed**, image built |
| cycle 4 (after the patch notes) | **green, the same figures**; image 36ab925873ac carries VERSION 2026.10.21.12 and the new notes (read back from the container) |

All five `AchievementsLayoutVerification` facts pass with the headings in the list: rows and headings never overlap,
everything sits between the tab rule and the pager, and every label ends inside the frame. All eleven
`JokeAchievementsVerification` facts pass too.

## 5. Website credits

For the shard's credits list (CC BY 3.0 requires it for every icon author used):

- **Icons made by Lorc** (http://lorcblog.blogspot.com), from **game-icons.net** (https://game-icons.net), licensed
  under Creative Commons Attribution 3.0 (CC BY 3.0).
- **Converted to UO spell-icon style by Praxiiz**: "1000+ Custom Spell Icons",
  https://www.servuo.dev/archive/1000-custom-spell-icons.258/.

Only Lorc's icons ship. If a swap brings in another author's icon, add "Icons made by <author>" for that author too:
Sbed for level-four-advanced, Delapouite for mine-wagon.

The rule as `D:\UO\third-party\spell-icons-1000\SOURCE.txt` states it (copied into the registry rows and
`SOURCE.txt`): "REQUIRED: include "Icons made by {author}" for each icon author used (Lorc, Delapouite, John Colburn,
Felbrigg, John Redman, Carl Olsen, Sbed; game-icons.net), plus credit Praxiiz for the conversion. Put this in the shard
credits list."

## Deviations and decisions for Chase

1. **"Plus one for hidden achievements" is the Mischief icon, so ten icons, not eleven.** P231 made the hidden joke set
   its own category after this prompt was written. Other categories also have a few hidden achievements; they keep
   their own category's heading and the row's existing "[Secret]" tag. A separate "secret" icon would need a place to
   show (for example beside "[Secret]"); say so if you want one.
2. **No per-author subfolders exist in the set.** Authors were taken from game-icons.net (part 2). All ten picks are
   Lorc's.
3. **Headings, not tabs.** The tab row is 22 px high and the icons are 44, and the prompt allows no change to the
   pixels beyond format and transparency, so the icons could not go in the tabs. They go on category headings in the
   list.
   - The cost is about 50 px per heading, so long lists run to more pages.
   - The tabs are unchanged, so Collection, League and Mischief still have no tab of their own; they show under All.
4. **The flaky patches gate (not fixed).** `docker/uo/apply-patches.sh:829-839` checks each patch file with
   `printf '%s' "$HANDLED_PATCHES" | grep -Fxq "$name"` under `set -euo pipefail` (`:9`).
   - When grep finds the name early and exits, printf can die of SIGPIPE, and the pipeline then counts as a miss. That
     is how cycle 1 failed on a patch its own log shows applied.
   - The fix keeps the check as strict: `grep -Fxq "$name" <<< "$HANDLED_PATCHES"`. It is outside this prompt's
     scope, so I did not make it. It can hit any Golem's build.
5. **Two flaky tests seen (not fixed).**
   - P239's `CreatureLevelsVerification.BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly` (DeathAdder this time;
     Scorpion in P271). Pinned's poison level is random per read, and the test reads 12 times.
   - `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant(Silenii, Phantom)`: "the
     fight did not start".
   - P271's note has a suggested fix for the first. Both deserve a small prompt.
6. **Not done:** a package build to scratch (the build is registry-driven and its count gate is what the package fact
   pins), and any look in a real client (For Chase).

## For Chase

- Rebuild the test shard from this branch (`sl-modernuo:cc-P241`), build the player package with the new gumps, and
  update a test client through the launcher.
- `[achievements` with a character that has some achievements:
  - On All, each section groups its rows under headings: the icon on the left, the category name beside it, in the window's
    header hue (1154).
  - Check the icons are crisp, their tan tiles sit well on the dark panel, and the names line up with the icons'
    middles.
  - Click each tab: the list opens on that category's heading.
- With a character that has earned a joke achievement (or one granted with `[ClusterFAchievement grant`, Administrator), the Mischief heading with
  the imp appears on All. Without one, there is no trace of it.
- With a client that has not updated: the headings show the names alone, with a blank space where the icon goes.
- To swap an icon, see part 2 and the contact sheet.
- Credits: add the "Website credits" lines above to the shard credits list (an agent may not edit `docs\`).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration -Branch golem/Bronze/P241`. It points at
this Golem's work copies; the default paths are the main checkouts, which this desk may not touch. Code: 17 files pending
(the 6 changed files, the 10 PNGs, the new test). Docs: 4 (this note and the three sheet files). Neither is BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P241 DONE
