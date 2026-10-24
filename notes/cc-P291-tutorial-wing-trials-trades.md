# cc-P291: the tutorial's wing trials, part 2 (gathering, crafting, animals, bard, thieving and the tours)

## In plain words

- Every tutorial lesson now works; none says "coming soon". The 20 that were left open are in: mining, lumberjacking,
  fishing and camping; all nine crafts (smithing a dagger, sewing a skullcap, and so on, and the trainee keeps what they
  make); an animals lesson at the farm pen (herd, tame, study and bandage a goat); the bard's lesson; the thief's lesson
  with all ten thief skills on a practice chest and a tutorial-only mark; and four short walking tours (houses, travel,
  reputation, and the shard's own systems).
- Most of them happen in a new "trades yard", open ground just south-east of P290's training yard. The lesson lends
  its tools, materials and skill, puts its vein, tree, pond, anvil, chest or echoes beside the trainee, and takes all of
  it back when the lesson ends or the trainee walks away.
- Played on a private copy of the test world by the test bot with a new character: the core first, then all 20 new
  lessons and the walk-away rule. 190 checks passed; Alchemy's three failed on a bot mistake, and Alchemy then passed
  on its own rerun. The full build check passed: 2,243 tests, none failed.
- For you: a few small choices near the end (where the yard is, the farm's two ways to finish the animals lesson, and
  that kept products could be farmed a little by replaying).

2026-10-23, the Iron Golem (Opus 5.5), branch `golem/Iron/P291` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P291-tutorial-wing-trials-trades-and-more.md`. Not committed (the Golem commits).
Nothing deployed; nothing run against live or the shared test shard (2594).

This prompt ran twice. The first session (this morning) stopped with `P291 STOPPED: waiting on P289`, and its note was
kept on this branch as a WIP commit. Chase's answer (Iron-P291-20261023-083606-8740, the Overseer at 09:22): "P289 is in
main now (P475 merged 08:44). Go ahead with P291." Checked before starting: the code repo's branch sits on
`579ad58` (the P290 merge), which contains P289 (`368a445`), P475 (`0f1871f`) and P480; P276's farm is in too.

## What changed (server, `D:\UO\golems\Iron\ShatteredLegacy`)

- `server/customizations/Tutorial/TutorialTradeTrials.cs` (new): the second part of P290's `TutorialWingTrials`
  (now a `partial` class), so the new trials share P290's start, page, arrow, loans, Tick, Reset, Stop and returns.
  - `Trades`: one row per station (20): its place, its steps, its hint, an explained-skill line, the craft's product,
    or a tour's stops. Registered by key in `TutorialStations.Handlers` with P290's eight.
  - Three kinds of evidence, all the server's own:
    - **a skill step**: a successful roll of that skill (`SkillEvents.SkillUsed`) while the lesson is armed. A harvest
      rolls only when it yields (pinned `HarvestSystem.cs`: the resource is given after a successful `CheckSkill`);
      the camping roll lights the fire (`Kindling.cs:38`); taming, herding, lore, veterinary, the three bard skills and
      the ten thief skills each roll on the real use;
    - **made**: more of the craft's product in the backpack than when the lesson began (loaners not counted). It is
      checked every quarter second;
    - **a tour stop**: standing within 4 tiles of the next stop. Stops count in order only.
  - Props: a practice vein (cave floor 0x053B, in Mining's static tiles), a walnut tree (0x0CE0 and its leaves, in
    Lumberjacking's tree list), a 2 by 2 pond (water 0x1797, in Fishing's static water), an anvil and forge, a locked and
    lightly trapped practice chest with a purse inside, a mark (a human training echo with a backpack), two bard echoes,
    and a goat in the farm pen (`TutorialFarmGoat`, a stock goat, hued). Pinned's harvest accepts an unmovable `Static`
    item as its target (`HarvestSystem.GetHarvestDetails`, `Engines/Harvest/Core/HarvestSystem.cs:488-494`). The
    harvest bank under the prop is emptied from memory when a lesson arms, so the trainee never finds it dug out.
  - Covered skills: Blacksmithy also asks for Arms Lore on the dagger; Tinkering for Item Identification on an "odd
    curio" (`TutorialCurio`, unidentified until Item ID rolls on it: pinned only rolls Item ID on an `IIdentifiable`,
    `Skills/ItemIdentification.cs:44`); Alchemy for Taste Identification on an apple (pinned only rolls it on food,
    `Skills/TasteID.cs`). Explained, one line each when the lesson starts: Herbalism (camping), Imbuing (blacksmithy),
    Forensic Evaluation (thieving).
  - Stealth reads the Hiding **base** (`Skills/Stealth.cs:77`, 30 since ML), which a skill loan cannot lift. The thief's
    lesson raises the Hiding base to 30 for the lesson and puts the trainee's own base back at the end, keeping any gain
    made above 30.
  - Products kept (F-35: craft it, bank it): the ore, logs and fish, and the dagger, skullcap, barrel staves, scissors,
    refresh potion, kindling, dough, Magic Arrow scroll and local map. Tools, leftover materials, the curio, the apple,
    the lockpicks, the poison, the dagger lent to poison, the stolen purse and the recall rune all go back.
  - Props are named `tutorial prop: ...`; P290's `SweepLoaners` now deletes those too when the world loads.
- `TutorialWingTrials.cs` (P290's file): `partial`; the start, arm, leave, arrow and page use each trial's own place
  (P290's eight keep the training yard and their exact lines); the lesson page lists a trade trial's steps as "Done:" or
  "To do:" lines; after a lesson is done the hint is no longer said again (the first test-world run showed the old hint
  right after "done", which read like a new task).
- `TutorialFarm.cs`: no longer registers the `animals.taming` handler (Rook's button now starts the goat lesson). The
  Farmhand's pet-and-pests lesson still completes the station as before.
- `ClusterFTutorial.cs`, `TutorialCoreTrials.cs`, `TutorialGumps.cs`: the three "Coming soon" strings are gone (they
  could only show for a station without a lesson, and there is none now).
- `CHANGELOG.md` and `VERSION`: `2026.10.23.6` (main was at .5), one Added line.

No patch to pinned ModernUO.

## Where things are

| Place | Point | Used by |
|---|---|---|
| The trades yard | 3426,2626 (open, standable ground: `check_walkability` on the client map, 941 of 960 tiles walkable in 3400-3439 x 2618-2641; the nearest of the 19 blocked ones is 10 tiles from the yard) | gathering, the nine crafts, bard, thieving |
| Its work spot | yard + (2, 0) | the vein, tree, pond, first echo |
| Anvil, forge | yard + (2, -1), (2, +1) | blacksmithy |
| Mark, chest | yard + (1, 0), (-1, 0) | thieving |
| The farm field, the goat | 3390,2606, the goat at 3395,2606 inside the pen (P276's layout: pen x 3393-3398, y 2604-2608, its gap on the west) | animals |
| Tours | anywhere within 160 tiles of 3460,2590 | the four tours |

The tours' stops: houses (the farmhouse porch 3383,2612; the bank), travel (the tutorial moongate; Rook's plaza),
reputation (the training yard; Sera the healer; the plaza), shard systems (the League field office; the bank; Rook).

## Tests

`server/tests/Tutorial/TutorialTradeTrialVerification.cs` (new): 10 facts, 24 test cases with the Theory rows.

1. Every one of the 37 stations has a lesson and no page says "coming soon"; 20 trade trials (28 wing stations less
   P290's 8).
2. Gathering (4 rows): the tool lent and the props placed; a failed roll or another skill's roll does not count; the
   skill's roll finishes it; the tool, the loan and the props go back; what was gathered stays.
3. Crafting (9 rows): a loaner of the product's type does not count; a product does, and is kept; the covered skill is
   needed after it for Blacksmithy, Tinkering and Alchemy; the anvil and forge for Blacksmithy.
4. Products already in the backpack do not count (a new one merging into an old pile does).
5. Animals: herding, taming, lore and veterinary finish it; a tamed goat is wounded for the bandage, and again if it
   heals before one.
6. Bard: the three skills finish it.
7. Thieving: the chest is locked and trapped with an unblessed purse in it; the mark has a backpack and can be snooped;
   the ten finish it; the Hiding base goes to 30 and back, keeping the gain; the stolen purse goes back.
8. Tours (4 rows): the last stop first counts for nothing; each stop in order; the last finishes it.
9. Leaving: far from New Haven stops a tour; leaving the trades yard stops a lesson and takes everything back.
10. Props left by a restart are swept.

Two existing facts changed with the behaviour: P276's farm fact now registers the wing handlers before checking that
`animals.taming` has one, and P480's first-play fact expects the lesson page, not the coming-soon page, when staff run
Alchemy before the core.

| Run | When | Result |
|---|---|---|
| Red: the new facts with the trades unregistered and the prop sweep off (`--tests-only`) | 10-23 20:33 | 2,243 total, **25 failed** (exactly the 24 new cases and the changed farm fact), 2,214 passed, 4 skipped |
| Green, first try (`--tests-only`) | 10-23 20:35 | 4 failed: my count of trades (I wrote 21; there are 20), a 0.1 rounding in the Hiding check (skill bases are tenths), the goat's wound, and P480's fact |
| Green, full gate | 10-23 20:39 | 1 failed: the goat, healed back to full after a tick |
| The goat fact with a diagnostic message (`--tests-only`) | 10-23 20:43 | 1 failed: same trial, goat not deleted, steps Herding and Animal Taming, 12 of 12 hits. The test host refills a wounded creature at once (pinned `Mobile.DefaultHitsRate` is zero there; `RegenRates` never configures), so the fact now runs that tick at a creature's two seconds |
| Green, full gate | 10-23 20:46 | `Built sl-modernuo:cc-P291 with patches applied and 2239 shard test(s) passing.` |
| Green, final (after the test-world fixes below) | 10-23 21:14 | Same line: 2,243 total, 0 failed, 4 skipped; image `b476778dd087`. The run before it stopped in apply-patches on "BaseShield-arms-lore-wear.patch never applied", the known pipefail flake; the rerun applied it |

## The test-world run

A private scratch shard (`cc-P291-tools\scratch-shard.ps1`, P290's script renamed: image `sl-modernuo:cc-P291` on
127.0.0.1:2596, a copy of the bot shard's world and Configuration without the AccountWipe save, autosave off, P276's map
overlay; the test-shard lock held throughout, then released). `cc-P291-tools\tradetrials.py` drives the play-test bot's
client: the Iron test admin only seeds the tutorial (`[ClusterFSeedTutorial`), and a new character "Iron Trades" on the
Iron test player account does everything else as player actions: the nine core lessons first (P480's `play_core`), then
each new lesson from Rook's page.

Final run (`cc-P291-tools\playlog-final.txt`): **190 PASS, 3 FAIL**; the three were Alchemy's, a bot mistake (below),
and Alchemy passed on its own rerun (`playlog-alchemy-rerun.txt`). The server log had no exceptions.

| Lesson | What the bot did |
|---|---|
| Mining, Lumberjacking, Fishing | the loaned pickaxe, hatchet or pole on the practice vein, tree or pond until iron ore, logs or a fish came up |
| Camping | double-clicked the loaned kindling; the campfire lit |
| The nine crafts | opened the tool's craft menu, its group and its item (dagger, skullcap, barrel staves, scissors, refresh potion, kindling, dough, Magic Arrow scroll, local map); then Arms Lore on the dagger, Item Identification on the curio, Taste Identification on the apple |
| Animals | walked into the pen, herded the goat with the crook, tamed it, used Animal Lore, bandaged it; the goat went back |
| Bard | the lute picked at the first prompt; Peacemaking, Provocation (one echo on the other), Discordance |
| Thieving | Detecting Hidden and Remove Trap on the chest, a lockpick, opened it, stole the purse, snooped the mark's pack, begged, poisoned the dagger, Tracking, Hiding, then Stealth |
| The four tours | walked to each stop; each counted, the last finished it |
| Leaving | started Mining, walked 20 tiles away: the lesson stopped and the pickaxe went back |

What the first run (`playlog-run1.txt`, 31 failed) found, and the fixes:

- The bot could not find the craft menu's buttons (the bot's mule helper reads another layout); `tradetrials.py` now
  reads the menu's own rows. Bot only.
- The anvil and forge stood one tile east of the yard's centre and the walker stopped short of them, out of the
  anvil's two-tile reach. They now stand two tiles east, out of the way in from town. Server.
- The lockpick needs the trainee next to the chest; the bot stood two tiles away. The thief's page now says "Stand
  beside the chest to pick it and to steal", and the bot stands there. Server text and bot.
- Taming rolls Animal Lore as well (pinned `AnimalTaming`), so the Lore step can be done before the trainee ever uses
  Lore; the step and the hint now say so. Server text.
- Snooping and poisoning each cost a little karma (pinned); the thief's page says so now. Server text.
- After "done", the old hint was said again; no longer. Server.

The final run's Alchemy failure: the group is called "Refresh" and the item "refresh", and the bot pressed the group
again. It now looks for items in the item column only. Bot only.

## What is not covered

- In game the bot made one of each product; exceptional quality, failed attempts and running out of material were not
  played (a failed attempt simply leaves the trainee to try again with the leftover materials).
- Two trainees at once share the yard's work spot: each gets their own props and creatures on the same tiles. Not
  played with two characters.
- The lesson page's look in our TazUO was not checked (no screenshots taken); it uses P480's shared colors.
- A server restart in the middle of the thief's lesson would keep the lifted Hiding base of 30 on that character (it is
  a real skill value, saved with the character). Everything else a restart leaves behind is swept.

## For Chase

1. **The trades yard's place** (3426,2626) was chosen from the map files, as P290's training yard was. P80's station
   list names shops for these lessons ("Forge and Anvil", "A Stitch In Time", "the Bowyer" and others). Each lesson
   can move by changing its place in `Trades`; say where if you want them in the shops.
2. **Animals has two ways to finish.** Rook's button now runs the goat lesson at the pen (herd, tame, lore, bandage).
   Wren's pet-and-pests lesson at the farm gate still completes the same station, as P276 built it. If you want only
   one of them to count, say which.
3. **Kept products can be farmed a little.** A finished lesson can be replayed while the account is in the tutorial,
   and each replay keeps one product (an ore pile, a dagger, a skullcap, a scroll). All are starter items worth very
   little. If you would rather the replays give nothing, the products can be lent like the tools.

## Deviations and decisions for Chase

- The unattended Read tool was refused for
  `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial\TutorialWingTrials.cs` (wanted: to read P290's file
  before editing it, as P290's session also found). Read with `sed` in Bash instead; edits made with small Python
  replacement scripts in the scratchpad.
- This repo's branch was not moved: it carries the first session's WIP commit of this note (`3c97b87`), which main
  does not have, so it cannot fast-forward. P289's, P290's and P480's notes and tools were read from `origin/main` with
  `git show`. The tools here start from P290's (`playkit.py` unchanged; `scratch-shard.ps1` renamed to P291).
- The prompt asks for F-35 and the map playbook to be read first. F-35 (feature queue) and P80's station design were
  read; the playbook was not opened, since no map file changes here (props are server items).
- Nothing was written outside the two work copies and this session's scratchpad (builds, the scratch world, logs).

## Files

- Code (`D:\UO\golems\Iron\ShatteredLegacy`): two new files (`TutorialTradeTrials.cs`,
  `TutorialTradeTrialVerification.cs`); `TutorialWingTrials.cs`, `TutorialFarm.cs`, `ClusterFTutorial.cs`,
  `TutorialCoreTrials.cs`, `TutorialGumps.cs`; two existing facts (`TutorialFarmVerification.cs`,
  `TutorialFirstPlayVerification.cs`); `CHANGELOG.md` and `VERSION`.
- This repo: this note; `notes\cc-P291-tools\` with `tradetrials.py`, `playkit.py`, `scratch-shard.ps1` and the three
  play logs (about 330 KB in all).
- Nothing running: the scratch shard is down, and the docker-build and test-shard locks are released.

P291 DONE
