# cc-P769: the first outside playtester's UX notes (creation, isle tutorial, New Haven)

Iron Golem, 2026-11-01. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P769`. Nothing is committed (the Golem commits), deployed, packaged for release or published. The
shared Test Shard was not touched.

**Done in two sessions.** The first stopped for memory (free memory fell to 1.4 GB, under the prompt's 3 GB line) and
asked Chase (Iron-P769-20261101-191918-65dd). He answered "Resume now": "If it falls under 3 GB again, finish with
builds and tests only and skip the shots." The second session (this one) started at 5.6 GB free. It ran the last
mutants, landed the skirt-colour client patch, and ran both gated builds (green), the client build and the package
build. Free memory fell to 1.9 GB and then 0.8 GB at the ends of the two Docker builds, so **the TazUO shots were
skipped**, as Chase said.

## In plain words

- **The Wakening Isle's lessons are plainer.** Lying on the beach, the hint now says how to get up: "hold the right
  mouse button on the ground, or press an arrow key". The backpack lesson gives the steps in the order the game shows
  them: click yourself once, choose Open Paperdoll, double-click the backpack picture, then the blue bag. The League
  lesson says exactly what to do at Elara. Saying **lesson** (no bracket) now reopens the lesson window, and the hint
  explains that the bracket is part of `[lesson`.
- **New tips, and fixes the tester hit.**
  - Short tips appear under the lesson text: hovering shows an item's name, resizing the game view, reading old chat in
    the Journal, double-clicking doors and gates, and seeing inside buildings (circle of transparency).
  - The bank lesson's blue token now comes the first time: saying "bank" inside the isle's bank starts the lesson.
  - The starting-city boxes on the character screen no longer look ticked when they are not. That was art we ship.
  - On the character screen, Pants Color now shows on a woman's skirt (a fix in our TazUO build).
- **More achievements.** Each of the 11 isle lessons has its own achievement, with its box. The first quest finished
  after the tutorial earns "Gainfully Employed". "The Tutorial Has a Checkbox" now arrives when the first New Haven
  trainer quest is turned in, not at the next login.
- **New Haven.**
  - After every New Haven lesson you are told to go back to Rook, with an arrow to him.
  - The tinkering lesson names the Item Identification skill, and double-clicking the odd curio uses it.
  - The escorts that ask for "the local weapons trainer" (and eight others) can be finished again. Their destinations
    had vanished with the old New Haven map.
- **For you:**
  - Both builds are green: main and the isle release. The isle release's changes are in one file, ready for an isle-only
    release.
  - There are no TazUO pictures of the new lesson texts: memory fell under 3 GB again, so they were skipped as you said.
  - The tester's disconnect left no log: the test shard was replaced at 12:09 that day. The death lesson now logs each step.
  - Nothing else for you to do until the release; the next player package will carry the client fix.

## The 14 items

| # | Item | Verdict |
|---|---|---|
| 1 | How to get up | **Fixed.** `TutorialWake.MoveHintLine`: "To get up, take a step: hold the right mouse button on the ground, or press an arrow key." (TazUO's arrow keys move by default: `Profile.DisableArrowBtn` is false.) Said in the system line and over the head, as P740 made it. |
| 2 | Backpack lesson | **Fixed.** Numbered steps in the client's order. One click on yourself opens TazUO's small menu (`GameActions.OpenPopupMenu`, `HoldShiftForContext` false by default), and pinned's `PaperdollEntry` is its Open Paperdoll line. |
| 3 | More tips | **Tips added.** `TutorialCoreTrials.Tip`: one line under the hint in the lesson window (and after the hint line) for movement (game view and black space), backpack (hover), paperdoll (moving windows), chat (Journal), farm (doors and gates), League (roofs and transparency). The optional Client tips page has three more rows: Read chat again, See inside buildings, A bigger game view. |
| 4 | The lesson command | **Fixed.** Saying `lesson` alone (any case, a trailing . ! ?) reopens the window for a trainee. `ReopenLine` and the finished window say "type [lesson (with the bracket) or just lesson", and name Tamsin. |
| 5 | League lesson | **Fixed.** The hint, Elara's greeting and a line when her window opens say: double-click her (or click once and choose Talk); her window finishing the lesson; Join the League or the X. On the isle she no longer says New Haven's ambient lines ("register today") or its proximity welcome. |
| 6 | Bank tokens | **Fixed.** Cause: after the death lesson the arrow points at the bank lesson's signpost, right at the bank's door, so a trainee walks in and says "bank" with the lesson not started, so no token. Saying "bank" in the isle's bank now starts the bank lesson when it is next (the token goes in before the banker opens the box) and gives a lost token again. Tested with a fresh trainee. |
| 7 | Disconnect | **Not reproduced; logging added.** The tester's session ran on the Test Shard container that P762's deploy replaced at 12:09 CST on 11-01. Its log went with it: the new container's log shows PaigeTest1 only at the character list (12:10). No crash: nothing else from that container survives. Reading the code (the rat's death, the ghost move, Sera's offer and the Resurrect button) found nothing that would drop a client. The death lesson now logs each step and any disconnect during it (`[Tutorial] Death lesson: ...`). |
| 8 | Achievements | **Fixed.** 11 isle-lesson achievements (`tutorial.lesson.*`, 5 AP, no renown, League category) granted when a lesson is finished, and "Gainfully Employed" (`quest.first`) on the first quest's rewards claimed, through a new 3-line core patch (`MLQuestEntry-quest-milestones.patch`). The patch also counts New Haven trainer quests at once. Titles: Upright and Mobile, Bag Inside a Bag, Cloaked and Ready-ish, Said the Thing, Pest Control Contractor, Bandage Enthusiast, Died on Purpose, Fiscally Responsible, Read the Brochure, Saw Things, Left the Nest. No skill or stat rewards. |
| 9 | Roofs | **Tip added, not defaulted.** TazUO already lifts roofs once you stand under one (`GameSceneDrawingSorting`: `_noDrawRoofs` when the player is under a roof). The circle of transparency (Options, Video, Misc) is a global setting since TazUO's profile migration 7, not a profile key, so the launcher's new-profile defaults cannot turn it on. "Hide roof" would hide every roof outdoors too. |
| 10 | Creation | **Map boxes fixed** (our art: see below). **Pants colour: fixed** in client patch `client\patches\0010-skirt-color-preview.patch` (a TazUO bug: see "The skirt colour" below). **Descriptions:** client already shows them (hover a profession: `ProfessionInfoGump` shows prof.txt's DescId cliloc as a tooltip). **Rotating:** client limit (the creation screen draws a paperdoll with no direction control). |
| 11 | Warrior person | **Fixed** (found by a read-only search). Pinned spawns escortables in Haven town (TownsPeople.json) whose New Haven escorts end in the ML plaza's regions ("the New Haven Warrior" and eight more). P678 took those regions off the map, so "take me to the local weapons trainer" had nowhere to go. Each destination is now a region over the Haven building doing that job (the Proving Grounds for the warrior), as the shop's parent so lookups still find the shop's own name. Alchemist and Farm have no matching building in pinned's Haven and stay unmatched. The tutorial's own lessons and the guild directory name places or seeded NPCs that exist. |
| 12 | Next quest | **Fixed.** Every New Haven lesson's end says "Next: follow the arrow back to Rook on his bench by the Albatross tavern and double-click him..." with the arrow on Rook. |
| 13 | Tinkering | **Fixed.** The step names the Item Identification skill. Double-clicking the curio in your backpack uses that skill, and the Skills-window route is described too. |
| 14 | Hide freezes | **Nothing slow on our side.** Hiding is one skill roll and a visibility update. Our hooks on skill use (`TradeSkillUsed`, the skill-gain clamp) do constant work, and `Hiding-combat-range-osi.patch` changes one number. Most likely the tester's PC. |

**The map boxes (item 10).** The package ships Fiddle-Me-This's restyled gumps 1209 and 1210. Those are the starting-city
list's markers (`CreateCharSelectionCityGump`: 0x04B9 not chosen, 0x04BA chosen or hovered). Its 1209 is a filled red
box and its 1210 an empty one, so the art reads backwards. `Build-PlayerPackage.ps1` now leaves those two out
(`$FmtLeftOut`, count 170 to 168), so the stock gems draw. `retired-files.txt` deletes them from existing installs. The only
other users are TazUO's grid container's two corner buttons.

## Tests

New facts (11): `server/tests/Tutorial/PlaytesterNotesVerification.cs` (9), and one each in
`TutorialTradeTrialVerification` (curio and the pointer back to Rook) and `Regions/HavenTownVerification` (escorts).
Changed facts:
- `AchievementEarnedLineVerification`: 146 to 158 achievements.
- `TutorialIsleWalkFixes4Verification`: the wake hint contains "get up".
- `TutorialIsleWalkFixesVerification`: the backpack hint says "double-click yourself".
- `TutorialVerification`: 13 boxes at graduation, the graduation and loop boxes plus the 11 lesson achievements' boxes.
- `HavenTownVerification`: a shop may sit inside an escort destination.

**Gated build, main** (`sl-modernuo:cc-p769`, logs in `notes\cc-P769-tools\`, UTF-16):
- Run 1 failed to compile the new test file (two missing usings): `gated-build-run1-compile-error.log`.
- Run 2: 2,917 tests, 2,909 passed, 6 skipped, 2 failed. The 2 failures were older facts encoding the old behaviour
  (the backpack wording and the box count), updated as above.
- **Run 3, green:** `gated-build-run3.log`. 2,917 tests: 2,911 passed, 6 skipped, 0 failed. `EXIT=0`.

**Gated build, isle release** (`sl-modernuo:cc-p769-isle`, `gated-build-isle.log`), **green:** 2,801 tests: 2,796
passed, 5 skipped, 0 failed. `EXIT=0`.

**Client build** (`client-build.ps1`, `client-build.log`, private output `D:\UO\golems\Iron\p769-client`):
- All ten client patches applied, 0010 included.
- 1,326 client unit tests passed.
- Publish succeeded. `EXIT=0`.

**Package build** (`package-build.ps1`, `package-build.log`, private output `D:\UO\golems\Iron\p769-pkg`, no
publish): `ShatteredLegacy-2026.11.01.2130.zip`, 146 MB, 741 files, "TazUO 3212623f + 10 patches". Every gate passed and `EXIT=0`. The zip has no gump 1209 or 1210 (the city boxes).

**Seen failing first** (P762's method: no old-code build can compile the new facts, so each fix is undone in a mutant
and the facts run in the builder image; `mutate769.py`, `probe769.sh`, `run-mutants.sh`, `mutants.txt`, `mutant-logs\`).
Every mutant turns exactly its fact red, and the unmutated copy passes 11 of 11 (both sessions):

| Mutant | Undoes | Fails |
|---|---|---|
| wakehint | item 1 | P769_TheWakeHintSaysHowToGetUp |
| backpack | item 2's steps | P769_TheBackpackStepsAreInTheOrderTheClientShowsThem |
| notips | item 3 | P769_LessonsCarryClientTipsUnderTheHint |
| nolessonword | item 4 | P769_SayingLessonOpensTheLessonWindow |
| league | item 5's hint | P769_TheLeagueLessonSaysWhatToDoWithElara |
| nobank | item 6 | P769_SayingBankInTheBankStartsTheBankLessonWithItsToken |
| noach | item 8's lesson grant | P769_EachIsleLessonGrantsItsOwnAchievementOnce |
| noquest | item 8's first quest | P769_ClaimingAQuestGrantsTheFirstQuestAchievementAtOnce |
| noescort | item 11 | P769_TheNewHavenEscortsHaveSomewhereToArrive |
| nonext | item 12 | P769_TheCurioStartsItemIdentificationAndTheEndSendsYouBackToRook (the same fact checks both) |
| nocurio | item 13 | P769_TheCurioStartsItemIdentificationAndTheEndSendsYouBackToRook |

The skirt fix (0010) has no unit test: it is one layer constant on a client screen. The client's own 1,326 tests pass
with it, and there are no shots (memory).

## The skirt colour (item 10)

TazUO put a human woman's skirt (0x1531) on the Pants layer. Its colour picker (`ColorPicker_ColorSelected`) dyes the
Skirt layer for a woman, as it does for the elf's skirt. So Pants Color changed nothing on screen. The server already
dyed the real skirt with the chosen colour. `0010-skirt-color-preview.patch` puts the skirt on the Skirt layer: one line
in `CreateCharAppearanceGump.cs`, with a row in `client\README.md`.

The patch was made in a TazUO worktree, `D:\UO\golems\Iron\tazuo-p769\w`. Last session's amend of its comment was
denied, so this session corrected the comment's method name (`OnColorSelected` to `ColorPicker_ColorSelected`) in the
exported patch text. That change is to a comment line only, and `Build-Client.ps1`'s `git apply --check` accepted it.

## On the isle-only release

`notes\cc-P769-tools\p769-release-isle-20261028.diff`: 23 files, made against the release tip `d542243` in a scratch
worktree (`D:\UO\golems\Iron\p769-isle`, detached, staged), **built green as `sl-modernuo:cc-p769-isle`**.
- **Isle parts:** items 1 to 8, the city-box art and the skirt patch (10), the tips page, the quest patch, CHANGELOG
  and VERSION.
- **Main only, not in it:** `TutorialWingTrials.cs`, `TutorialTradeTrials.cs` and `Regions/HavenTownRegions.cs` (items
  11 to 13), and their tests (`TutorialTradeTrialVerification.cs`, `Regions/HavenTownVerification.cs`).
- **One conflict, resolved:** `apply-patches.sh`. The release lacks P714's school-gate lines; the new patch line is
  kept alone.
- The release CHANGELOG leaves out the two New Haven lines.
- For the Golem's commit: the isle and main-only parts can be split by those three files and the two tests. I cannot
  commit, so they are not separate commits yet.

## CHANGELOG and VERSION

`2026.11.01.5` (main's newest was `2026.11.01.4`):
- **Added:** "Tutorial tips and fixes from playtester notes", and the first-quest achievement.
- **Changed:** the isle lesson wording and the lesson word; Rook's pointer and the tinkering skill.
- **Fixed:** the bank token, the escorts, the city boxes, the skirt colour on the character screen.
- **Staff:** the death-lesson log.

## Deviations and decisions for Chase

- **Stopped once for memory**, then resumed on Chase's answer (see the top).
- **No TazUO shots.** Free memory fell under 3 GB again during the builds, and Chase said to skip the shots then. The rig
  is ready for a later run, with the test-shard lock: `run-tazuo.ps1 -Image sl-modernuo:cc-p769 -Character "Iron Paige"
  -Script Shots769.py -Out notes\cc-P769-shots`. The city-list screen still cannot be reached without moving the real
  mouse (P762's finding).
- **The package build needed `-UoData`.** Gate 4 reads the EA file names from `client-data\classic-client`, which a Golem
  code copy does not have. `package-build.ps1` passes the shared copy `D:\UO\tool-trials\client-data-copy`, as earlier
  tasks did. The package used the private client build, because the client gate checks every patch, 0010 included.
- **Escort destinations for the Alchemist and the Farm** have no matching building in pinned's Haven. Those two escorts
  still cannot finish. Turning the Haven escortables off (`ClusterFHavenTownSpawns`) is the other option.
- **Worktrees and private folders added**, all mine to remove after the merge:
  - `D:\UO\golems\Iron\p769-isle` (the release copy, detached);
  - `D:\UO\golems\Iron\tazuo-p769\w` (detached, of the shared TazUO clone `D:\UO\cc-p40-work\tazuo-3212623f`);
  - `D:\UO\golems\Iron\p769-client\src` (Build-Client's own worktree of that clone), and the build outputs
    `p769-client\client` and `p769-pkg`.

## Files

- **ShatteredLegacy:**
  - new: `server/customizations/ClusterFQuestMilestones.cs`, `Tutorial/TutorialLessonAchievements.cs`,
    `server/patches/MLQuestEntry-quest-milestones.patch`, `server/tests/Tutorial/PlaytesterNotesVerification.cs`,
    `client/patches/0010-skirt-color-preview.patch`;
  - changed: `ClusterFAchievements.cs`, `LeagueRegistrar.cs`, `Regions/HavenTownRegions.cs`, and in `Tutorial/`:
    `ClusterFTutorial.cs`, `TutorialClientTips.cs`, `TutorialCorePlacement.cs`, `TutorialCoreTrials.cs`,
    `TutorialGreeting.cs`, `TutorialTradeTrials.cs`, `TutorialWake.cs`, `TutorialWingTrials.cs`;
  - `docker/uo/apply-patches.sh`, `player-package/Build-PlayerPackage.ps1`, `payload/app/retired-files.txt`,
    `client/README.md`;
  - six test files; `CHANGELOG.md`, `VERSION`.
- **shard-migration:** this file and `notes\cc-P769-tools\`: the build scripts and logs, the client and package build
  scripts and logs, the mutant scripts and logs, the release diff, the TazUO rig and `Shots769.py`.

P769 DONE
