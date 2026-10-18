# cc-P146: The play-test page asks Chase's decisions as real questions he can answer, plus Where filters

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P146-playtest-decisions-inbox.md`. The play-test service and page, the
importer's data, the Haven mirror. Not committed (the Golem commits after DONE). Both repos were clean at the start.
**CC never connected to Haven**: everything was proven on a local scratch copy of the service, as P107 did.

## Headlines

- **Every decision is now its own card on the play-test page.** Decisions are read from each notes file's
  "Deviations and decisions for Chase", "Decisions for Chase" or "Open questions" section. Each card has:
  - the question, in one or two plain sentences;
  - the options as buttons, with built and recommended marked;
  - **Keep what's built**, when something is built;
  - what is **live today** and what CC **recommends**;
  - a free-text box with **Save answer**, and **Ask me later**;
  - a link to the notes section on GitHub (under "More from the notes").
  - Ids keep the prompt and number: `P77-D3`.
- **Counted on 2026-10-18, after the mirror refresh:**
  - **703 decision items from 86 sources:** 84 notes files from P59 on whose sections the parser read, plus P82
    (prose, split by hand) and T-008. 27 of the 703 were split by hand.
  - **124 are asked (open):** You decide 124, and Questions 124.
  - 40 are answered elsewhere, each with its source, and 4 are moot, each with its reason.
  - The other 535 are "noted": older deviations that were never put to Chase as questions. They stay out of the
    default view (see Deviation 1).
- **Answers are saved with who and when** in the new `testing/decisions.json`. The page's identity is the
  Cloudflare Access email when Access is on; without it, "by" is empty, the same as results, ideas and bugs today.
  - An answer shows on its card and can be changed (the history is kept) until the overseer marks it **taken
    into P<nn>**.
  - After that the card shows "Taken into P150", the answer is locked, and the card leaves the default view.
- **Answers reach the repo on the next commit.** `decisions.json` is in the export bundle (`tools/opsdata.py`), so
  `opsmirror.py` brings it from Haven into `testing/` with the other marks.
  - The store carries each question's text, so the file reads on its own.
  - `python tools/decisions.py answers` prints the new answers for the overseer, and so does the page's **Copy new
    answers** button.
- **On the page:**
  - the header has an **"N new answers"** count;
  - a new **Answered, not yet taken** filter;
  - the overseer's **Taken into P...** button (and **Not taken** to undo it).
- **The 17 open "You decide" items are replaced by their real decisions.** These include the 10 "checklist not
  parsed, read the notes" placeholders, P72-0 to P93-0.
  - Each now shows only under All, with a "now asked as N questions" chip.
  - Each is out of the open count and the Who counts.
  - **The brief's "19" is not what I counted.** The triage has 20 DECISION rows: 2 are already passed (P89-0,
    P110-2), and 1 has no item on the page (P140-8). That leaves 17 open, and all 17 are replaced.
  - Answered elsewhere:
    - P59 (8 of 8), from `notes/f35-evo-pets-handoff-2026-10-05.md` and F-35 in `docs/feature-queue.md`;
    - P80 (8 of 8) and P89 (10 of 11), from `notes/decisions-2026-10-14.md`;
    - 7 of P93's 8 open questions, from the same file.
  - Moot:
    - **P89-D10**: the intranet is Tailscale only (cc-P133);
    - **P106-D10**: live's D94 question, since live is retired (cc-P108);
    - **P110-D5 and P110-D6**: Tailscale only.
- **From now on it is automatic.** The page reads every DONE notes file each time it loads, cached by file time.
  - A new prompt's decisions section becomes open questions with nobody editing anything. Only the prompts listed
    in the overlay's `notAsked` are "noted".
  - The P115 "every item has a Who" check now counts decisions, and also checks that every open item has exactly one
    Where.
- **Where chips** (Chase, 09:13), on a second row under the filter buttons: **Anywhere**, **Questions**, **Outside the
  game**, **In game: Admin**, **In game: Player**.
  - Under Player there are sub-chips: **Human**, **Gargoyle**, **Elf**, **Any character**.
  - Bot and CC items have Where Bot and CC, covered by the existing Bot and CC buttons.
  - The chips combine with Mine and the other buttons, and each chip shows how many it would show with the current
    button pressed.
  - **Today, Open:** Questions 124, Outside the game 69, In game: Admin 30, In game: Player 42 (Human 8, Gargoyle 1,
    Elf 8, Any character 27), Bot 95, CC 80.
  - **Mine:** 265, the same 124 / 69 / 30 / 42.
  - Every open item has exactly one Where (the check is in the suite).
- **Tests:**
  - 21 new facts in `tools/tests/test_decisions.py`, plus 1 new real-files fact in `test_play_who.py`.
  - With the P146 code removed: 20 of 21 failed, plus the real-files fact. The one that passed is "the page stays
    ASCII", which the old page already was.
  - Four targeted break-and-restore proofs, each caught by the fact it was aimed at, and each file was byte-identical
    afterwards.
  - Final: **shard-migration tools 151 of 151**, importer Pester **20 of 20**. The bot suite is **40 of 41**: the one
    failure is the known environmental one (the nightly task is installed), as recorded in P112 and P115.
- **Proven in a real browser** (headless Chrome through Selenium), on the new `server.py` with a scratch copy of today's
  notes, docs and testing:
  - 440 cards;
  - Mine 265; Mine + In game: Player 42 (only You and Bot-then-you badges); + Elf 8 (P138-4, P138-6, P81-0, P62-2 to
    P62-6);
  - answering P77-D1 by button and P77-D2 by text gave "2 new answers" and both in Answered, not yet taken;
  - `decisions.json` written with the time;
  - no horizontal scroll at the narrowest width headless Chrome allows (500 px);
  - the only console line is the old favicon 404.
- **Nothing was deployed.** On Haven the page picks this up by itself (cc-P137): the `server.py` change makes the
  service exit cleanly and the container restarts on the new file within about 2 minutes of Haven's pull. Nothing
  for Chase to restart.

## Why read time plus an overlay (not a fragile parser, not importer-written items)

- **Like P115's Who and steps.** The decisions are merged when `/api/items` is read (`tools/decisions.py`). Only the
  answers are stored. So:
  - no importer change can wipe them;
  - a notes edit shows at once;
  - Haven reads the notes and the overlay from its git-pull clone, with no new data file to seed.
- **The parser handles lists and the overlay handles everything else.** All 84 sections the parser found are
  numbered or bulleted lists, and it reads:
  - top-level entries, with continuation lines;
  - nested bullets, which are options when the entry asks to pick;
  - "Recommended: ...", placeholders and "defaults taken" (which mean built);
  - numbering that carries on into a second section.
  - **Prose, split by hand into `testing/decisions-overlay.json`:**
    - **P82**: section 6 "Hooks, TODOs and mismatches" holds its "For Chase" and "A decision for Chase" lines, as 5
      items, P82-D1 to D5;
    - **P93**: the real questions are in `notes/servuo-code-port-assessment.md`, "Open questions for Chase", as
      P93-D8 to D15;
    - **T-008**: Q-064 in `notes/codex-questions.md`, as T-008-D1;
    - **P106-D9** (delete `question-proof`) and **P106-D10** (live's D94 question), from its For Chase;
    - **P104-D5**, **P108-D8**, **P110-D7** and **P126-D7**, single questions from For Chase or a play-test item;
    - **P137-D8**, **P140-D9**, **P141-D8**, **P142-D11 to D13** and **P155-D9**, entries that held two questions,
      split in two.
  - The page marks each of these "split by hand".
- **The overlay's wording is hand-written for every asked prompt.** Each asked decision has a plain question,
  options, built and recommended, and a default. The work was:
  - four reading subagents, one per prompt group, on one written brief;
  - each read the notes and the later answer files;
  - I merged and validated their output: every parsed id covered, every overlay id built, every answer and moot
    with its source or reason. I then read a sample against the notes.
- **The answers store** follows `feature-ideas.json`'s rules: a fixed key order, ASCII, a temp file and rename, and
  its own lock (`playtests.Lock`).

## What changed, with file:line

**shard-migration**

| File:line | Change |
|---|---|
| `tools/decisions.py` (new, 494 lines) | `SECTION` :45, the section headings; `parse_notes` :73 and `split_entries` :102, one item per numbered entry (bullets when there are no numbers), numbering carried across sections; `shape` :144, the question (two sentences after a bold label), detail, options (nested bullets under a "pick/options/either" entry), built, recommended, default, GitHub anchor; `read_all_notes` :173 (DONE notes from P56 on, cached by time and size); `load_overlay` :212 (the notes clone first); `build` :225, merges the parse, the overlay and the answers into states (`STATES` :37); `replaced_items` :287; `annotate` :300 (`doc["decisions"]`, `replacedBy`, the Who counts, `summary.replaced`, `doc["answers"]`); the store `load`/`save`/`update` :354-382; `answer` :397, `later` :416, `mark_taken` :425 (needs `P<nn>`; `undo`); `copy_text` :456; a CLI `list` / `answers` :475 |
| `tools/playwhere.py` (new, 143 lines) | `classify` :37: a hand-set `place` first, then Who (You decide gives questions, Bot gives bot, CC gives cc), then the steps' Where line (`ADMIN` :26, `PLAYER` :27, else outside); `chars_of` :33; `annotate` :60 (`it["where"]`, `doc["where"]` counts and `missing`); `counts` :83; `primary` :102 and `shown_items` :132, the page's button rule, so the counts can be tested in Python |
| `testing/decisions-overlay.json` (new, 92 KB) | `notAsked` (51 older prompts), `replaces` (18 play-test items), `decisions` (wording, options, defaults, elsewhere, moot, noted, and the 27 hand splits) |
| `testing/bot-triage.md` | P139-0 (DEPLOY) in its table; new P160, P161 and P162 tables (CC 8, EYES 2, DEPLOY 1): the 11 items that had no Who and kept the suite red at the start |
| `testing/playtest-steps.json` | steps for those 11; `place`/`chars` by hand on P62-6 and P138-6 (Elf tests whose Where line also names Eve); P65-0, P81-0 and P113-0 now say to answer on the page |
| `tools/opsdata.py:34` | `testing/decisions.json` is in the export bundle (and so in the mirror) |
| `tools/tests/test_decisions.py` (new) | 21 facts, below |
| `tools/tests/test_play_who.py:298` | the real-files fact: every open item and decision has one Who and one Where, each counted once |

**Shard repo (`D:\ShatteredLegacy`)**

| File:line | Change |
|---|---|
| `docker/test-queue/server.py:19-26` | docstring: the routes |
| `docker/test-queue/server.py:118-119`, `:122` | `import decisions, playwhere`; both in `MODULES`, so a tools change reloads them (cc-P137) |
| `docker/test-queue/server.py:178` | `current_decisions()`: notes from the root, overlay from the notes clone then DATA, answers from DATA |
| `docker/test-queue/server.py:330-340` | `/api/items`: `decisions.annotate`, then `playwhere.annotate`; each failure becomes a flag, never a 500 |
| `docker/test-queue/server.py:370-380` | `/api/summary` `answers_new`; `GET /api/decisions/copy` |
| `docker/test-queue/server.py:498-514` | `POST /api/decisions/answer`, `/later`, `/taken` (an unknown id is a 404, a bad answer a 400) |
| `docker/test-queue/html/index.html:103-121` | CSS: decision cards, options, answers, the Where chips |
| `docker/test-queue/html/index.html:141`, `:145-146` | the **Answered, not yet taken** button; the Where chip row |
| `docker/test-queue/html/index.html:221-264` | `where`/`chr` (remembered per browser); `shown` = `shownPrimary` (the buttons, for items and decisions; replaced items only under All) and `whereMatch` |
| `docker/test-queue/html/index.html:287-299` | the open count leaves out replaced items; **N new answers**; `renderWhere()` |
| `docker/test-queue/html/index.html:311`, `:322-420` | Copy new answers in the Answered view; `allItems`, the chips and their counts, `decisionCard`, `decisionClick` |
| `docker/test-queue/html/index.html:671` | the new-answers count opens its filter |
| `docker/test-queue/README.md` | `decisions.json` under "Where the data is"; the four routes; `answers_new` |
| `CHANGELOG.md`, `VERSION` | 2026.10.18.6, one `### Staff` line (2026.10.18.5 was committed with P145) |

## The decision items, per source prompt

The asked, elsewhere and moot items. The 535 noted ones are listed by `python tools/decisions.py list`, which prints
every item with its state. "replaces" names the play-test items each prompt's decisions stand in for.

**P59** (8 asked):

- P59-D1 ELSEWHERE: Should recolored bodies (25, 27, 34, 37, 23, 98, 63, 64, 65 and 127) count as the same creature, so none of them is an evo pet stage? (answered elsewhere: notes/f35-evo-pets-handoff-2026-10-05.md, answer 1)
- P59-D2 ELSEWHERE: Should evo pet lines use third-party creature art, which means shipping custom client art (an animal slot or a UOP entry) to every player? (answered elsewhere: notes/f35-evo-pets-handoff-2026-10-05.md, answer 2; docs/feature-queue.md (F-35, "Build plan, decided (Chase, 2026-10-05 13:40)"))
- P59-D3 ELSEWHERE: How long should the fox evo line be, and which bodies make up its stages? (answered elsewhere: notes/f35-evo-pets-handoff-2026-10-05.md, answer 3; docs/feature-queue.md (F-35, "Build plan, decided (Chase, 2026-10-05 13:40)"))
- P59-D4 ELSEWHERE: Which five bodies should make up the dog evo line? (answered elsewhere: docs/feature-queue.md (F-35, "Stage picks, decided (Chase, 2026-10-05)"))
- P59-D5 ELSEWHERE: Which five bodies should make up the cat evo line? (answered elsewhere: docs/feature-queue.md (F-35, "Stage picks, decided (Chase, 2026-10-05)"))
- P59-D6 ELSEWHERE: Which five bodies should make up the bird evo line, and what if third-party art is declined? (answered elsewhere: docs/feature-queue.md (F-35, "Stage picks, decided (Chase, 2026-10-05)"))
- P59-D7 ELSEWHERE: Is it fine that the dog (217) and cat (201) starter stages are bodies players already see everywhere as town critters? (answered elsewhere: notes/f35-evo-pets-handoff-2026-10-05.md, answer 4)
- P59-D8 ELSEWHERE: Should every chosen unused body get a bodyTable.cfg entry (Animal) as part of the F-35 build, so pets cannot open doors and keep their... (answered elsewhere: notes/f35-evo-pets-handoff-2026-10-05.md, answer 5)

**P65** (10 asked):

- P65-D1: Are the evo pet XP thresholds (500 / 3,000 / 13,000 / 53,000 total) and the kill XP formula right, given they are server settings...
- P65-D2: Is the evo pet stat curve right, with stage 5 as strong as a Cu Sidhe on 1 control slot and the same curve for every line until roles...
- P65-D3: Keep the seven placeholder evo pet hues, knowing some may look odd on the already coloured UOP bodies, or pick a new list?
- P65-D4: Keep the placeholder Echo lines the evo pets use, or write new ones?
- P65-D5: The Bond Trial is only a staff flag until it is designed. How should a player pass it?
- P65-D6: A player's stage pick (for example the dog breed) is permanent and only staff can change it. Should players get one change of their own?
- P65-D7: A released evo pet cannot be re-tamed by anyone (Tamable is false). Should someone be able to tame it again?
- P65-D8: Keep the placeholder stage names (pup, young hound, hound, guardian hound, windrunner; kitten to manticore; kit to kitsune; chick to...
- P65-D9: The sabertooth costume body (1416) now swings with animal actions. Keep that, or exclude 1416 from the animation change?
- P65-D10: When F-12 lands, should EvoPet.OwnerLoopsSource be set to the real loop count and the real loop reset added to the evo pet test?

**P72** (10 asked) replaces P72-0:

- P72-D1: For leveling gear, should we port ServUO XmlLevelItems' code, or only its design, rewritten under our rules?
- P72-D2: How should a crafted item become levelable?
- P72-D3: Should leveling items earn XP from hits paid out when the creature dies, or on every hit?
- P72-D4: When several players damage a creature, should each contributor's items get full XP or a share split by damage?
- P72-D5: What happens to a leveled item when its owner's loop resets?
- P72-D6: Should companions' gear earn item XP and have its bonuses act now, given that how much a companion's weapon matters waits on P41's...
- P72-D7: Is this anti-farm list for item XP right: no XP from own or player-owned creatures, summons or NoKillAwards creatures, a creature-level...
- P72-D8: What may item level points buy?
- P72-D9: Is the item XP curve of 13 x n^1.4 (about 150 hours to level 200 for a steady player) the right starting point, with playtest setting...
- P72-D10: Should levelable items stay tradeable, or bind to a character on their first level?

**P75** (7 asked) replaces P75-0:

- P75-D1: Should the Clockwork Scavenger be dropped as the League auto-loot reward, since TazUO's Autoloot already does the job? If so, keep the...
- P75-D2: Should the Field Salvager only work at a forge, or allow salvaging anywhere at a lower yield?
- P75-D3: Are Corpse Claim's range and cooldown (12 tiles, 10 seconds) right, and should it work on party members' kills?
- P75-D4: Which commodities should Loot Courier tier II send to the bank, and when the bank is full should it stop or spill into the mule?
- P75-D5: Is the Expedition Ledger (offline progress) wanted at all, and if so only after F-24's jobs exist?
- P75-D6: Should League utility rewards cost more AP and Renown than cosmetics, or stay inside F-13's range (up to 1,750 AP and 1,000 Renown)?
- P75-D7: Should the server send TazUO's DisableFeatures for anything, given it can only disable tree stumps today?

**P76** (8 asked) replaces P76-0:

- P76-D1: May we ship whole community-made map files (with no EA bytes in them) as our own data in the player package?
- P76-D2: Which extra facet should be added first?
- P76-D3: Keep the placeholder facet names (The Proving Ward, The Hiltdeeps, Sosaria Before, The Unwritten Reach), or rename them?
- P76-D4: Should the big extra maps ship as a separate optional facet pack, or in the main player package?
- P76-D5: Is it fine to fetch UOFiddler and CentrED+ (and RadCopy for Siege of Sosaria) when facet wiring starts?
- P76-D6: What should the Siege of Sosaria map be for, given it is a second Trammel?
- P76-D7: Should extra facets be added before the world wipe, which is cheapest, or after the stock-map buildings that come first?
- P76-D8: CALYPSO is still to download (5 a day on servuo.dev). Revisit it as a facet candidate when it lands?

**P77** (8 asked) replaces P77-0:

- P77-D1: Which rank names should the Order of the Alembic use: set A (the still), B (the work), C (the order), or your own?
- P77-D2: Keep "Alembic Drams" as the Order's currency name, or use another such as "Still Marks" or "Vial Tokens"?
- P77-D3: Keep the guildmaster as "Distiller Orla Vance" in a pink-hued robe and half apron, or rename or restyle her?
- P77-D4: Is the Order's Apprentice task (Alchemy 50, or 10 Empty Bottles) right, or should Taste ID be part of it?
- P77-D5: When should the guild hall seed commands ([ClusterFSeedGuildHalls and [ClusterFSeedAlembicHall) run on the test world, or should the two...
- P77-D6: Should the Order get its own mule module like the other 17 guilds, or be left without one and the "one from each guild" patch note reworded?
- P77-D7: Glassblowing stays a stock book unlock inside the Alchemy menu, with nothing gating or teaching it. Should the Order sell the...
- P77-D8: Which of the Order's hall art pieces should be registered first?

**P78** (10 asked, 2 noted) replaces P78-0:

- P78-D1: Craft guild rank is standing under a skill cap that only rises, and only the 7 craft guilds are gated. Should the other guilds get skill...
- P78-D2: Is the promotion skill right as the best Base of the guild's own craft skills (Foresters: Carpentry or Fletching; Arcane Society:...
- P78-D3: The recipe band merge rule leaves Fletching with one Band IV book holding Bands I to III, and Alchemy, Inscription and Cooking each with...
- P78-D4: The recipe hint names the rank that sells the book (one band ahead), while the help page names both the selling and the granting rank....
- P78-D5: Reading a recipe book or scroll needs no skill, unlike stock RecipeScroll, which needs the item's minimum skill. Add a skill floor?
- P78-D6: Alchemy, Inscription and Cooking Band V recipes cost currency only (no material), and leather stops at Barbed. Keep that, or add Band V...
- P78-D7: Are the placeholder recipe prices and chances right (books 100/200/400/800, Band V scroll 1,500 plus 10 material, large BOD 2 percent,...
- P78-D8: Staff (GameMaster and up) bypass the recipe gate and see every craft item. Keep that?
- P78-D9: Craft categories whose items are all hidden still show in the category column with an empty list. Hide them (an edit to the craft gump...
- P78-D10: Existing OSI recipe items are now hidden until learned, with the wild hint line, instead of listed and greyed. Keep that?

**P79** (8 asked, 1 noted) replaces P79-0:

- P79-D1: Achievements are per account, so a second character on the account gets no loot box for achievements the account already holds. Keep...
- P79-D2: Until F-12 brings real levels, the loot-box level stand-in is total Base skill / 10. Keep that stand-in?
- P79-D3: Loot-box tiers: achievements by AP (10/25/50/100/250), bosses 4/5/6, League ranks in threes, clears 3, loops 6. Keep these tier rules?
- P79-D4: The leather ladder has no tier past Barbed, so a tier 5 box repeats Barbed and tier 6 uses Celestial in the metal hue. Should there be a...
- P79-D5: Box gear rolls 1 to 4 properties at up to 60 percent intensity, plain quality. Is that weak enough to sit below exceptional crafted...
- P79-D6: Seven loot-box rewards are placeholders: satchel upgrade, grove ledger page, companion items, boss trophy, League discount token, unique...
- P79-D7: Repeat counts on the achievement page show only for achievements earned on 2 or more loops, so the page looks the same until loops...
- P79-D8: Achievement fanfare is minor below tier 4 and major from tier 4; capstone fanfare is only for loops, reaching 200 and trial chapters....

**P80** (8 asked):

- P80-D1 ELSEWHERE: Every account starts the tutorial as NotStarted, so existing characters would be greeted at their next login. Turn `tutorial.enabled`... (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #1)
- P80-D2 ELSEWHERE: The tutorial recruiter is Rook Hallowell, the League recruiter, on the plaza at 3500,2572,14. Keep him, or have Elara Voss (the... (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #2)
- P80-D3 ELSEWHERE: The tutorial speaks as "System: ..."; F-35 called that voice the Echo. Are they the same voice? (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #3)
- P80-D4 ELSEWHERE: Tutorial achievements: "Didn't Read the Manual" 5 AP, "Read the Manual Eventually" 10 AP and 25 Renown, League category, not hidden.... (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #4)
- P80-D5 ELSEWHERE: The tutorial graduation box is an Explorer's tier 1 (Common). Keep it, or pick another theme or tier? (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #5)
- P80-D6 ELSEWHERE: Tutorial hints are server-driven only. Add the about-30-line TazUO client patch (a whitelisted 0xCE ClientCommand) so station buttons... (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #6)
- P80-D7 ELSEWHERE: The loop placeholders disagree: loot boxes start at loop 1, evo pets at loop 0. Which should F-12 use? (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #7)
- P80-D8 ELSEWHERE: Which trial order should the tutorial use: F-35's story order (gather, craft, tame, fight, heal, spell, dungeon, travel, echo) or this... (answered elsewhere: notes/decisions-2026-10-14.md, Tutorial (P80) #8)

**P81** (4 asked, 1 noted):

- P81-D1 ELSEWHERE: The local NSFW paperdoll switch lives in our launcher (`Play.ps1`, `Paperdoll-Bodies.ps1`), not in TazUO, because we ship TazUO's... (answered elsewhere: notes/cc-P111-tazuo-paperdoll-option.md, Headlines)
- P81-D2: Gump ids 62000-62026 stay Fiddle-Me-This's, so the kit's female versions of those 27 DLC wearables are not shipped (fine while no...
- P81-D4: The DLC templates shipped as the grayscale (hueable) set, not the pre-hued one. Keep the grayscale set?
- P81-D5: Do you want a later prompt for the kit's 18 animation VDs and its Equipconv.def changes?

**P82** (5 asked):

- P82-D1 [split]: The Artificers' ladder has five rungs (0, 1,000, 5,000, 15,000, 40,000) and no rank 4, so the rank 4 book (FC, FCR, SSI, super slayers,...
- P82-D2 [split]: Members with the Artificers' Toolkit can imbue anywhere up to Full, so mule socket II (Refined) adds nothing for them. Keep "anywhere"...
- P82-D3 [split]: ServUO gives an ordinary soul forge no bonus (only the Queen's 6 and the Royal City's 2). We use 2 percentage points as the standard...
- P82-D4 [split]: The design names crafter +skill as new without a rank, so it was put at rank 1 beside Jewelry +skill. Keep it at rank 1?
- P82-D5 [split]: The design gives no flavor text for the Creature of Habit achievement, so CC wrote one ("Twenty-five times. The System has stopped...

**P89** (11 asked):

- P89-D1 ELSEWHERE: Approve the Haven pages shape: Haven serves, the game PC builds Shard status and pushes a snapshot, and Haven is the only writer of... (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #1)
- P89-D2 ELSEWHERE: Who gets into the Haven pages: Chase only, or Chase and his daughter? And should she see play tests as well as ideas? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #2)
- P89-D3 ELSEWHERE: What outside hostname should the Haven pages use? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #3)
- P89-D4 ELSEWHERE: How should Haven pull the repo: a git-pull container or a systemd timer? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #4)
- P89-D5 ELSEWHERE: Build the shard login for the pages (H6) now or later? If built it uses a separate `[webpassword`, never the game password. (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #5)
- P89-D6 ELSEWHERE: Game PC container stats on Homepage: status from the snapshot, or live CPU and memory through a read-only Docker socket proxy on the LAN? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #6)
- P89-D7 ELSEWHERE: Show Haven's containers (Vaultwarden, website, wiki, NPM up or down) on Homepage through a read-only socket proxy? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #7)
- P89-D8 ELSEWHERE: Deploys on Haven: keep them Chase-run (paste one command), or give a CC prompt SSH write access for named deploy scripts only? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #8)
- P89-D9 ELSEWHERE: Haven's stale Homepage and its June `~/shattered-legacy` checkout: replace that Homepage in H5 and leave the checkout alone, noting... (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #9)
- P89-D10 MOOT: `dashboard.shatteredlegacyuo.com` resolves publicly to the house and is in Homepage's allowed hosts. Does NPM route it, and if so should... (moot: Since cc-P133 the Haven dashboard is Tailscale only: it binds Haven's LAN and loopback, never 0.0.0.0, and is served by Tailscale Serve; Chase was checking NPM himself (10-14))
- P89-D11 ELSEWHERE: Rename Homepage's "Migration status" entry (from P88) to "Public progress page" when Haven's Homepage is built? (answered elsewhere: notes/decisions-2026-10-14.md, Haven pages (P89) #11)

**P92** (1 asked, 5 noted) replaces P92-0:

- P92-D1: The status page counts the Port tier as 283 of 983 files, not the 222 of 905 in your port-list note; the gap is the Base items row...

**P93** (8 asked, 7 noted) replaces P93-0:

- P93-D8 [split] ELSEWHERE: Go on the servuo.dev draft prompts? Say which of draft P94 to P98 to save to the queue, and in what order. (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))
- P93-D9 [split] ELSEWHERE: Is the servuo.dev Vault Pass worth buying? Every Vault module needs Vita-Nex Core (months to port), and IPL is a launcher the shard does... (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))
- P93-D10 [split] ELSEWHERE: Are virtual storage chests wanted at all, given F-19's 1,000-item banks, the satchels and the mule? If yes it is a native rebuild. (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))
- P93-D11 [split] ELSEWHERE: Is Power Hour wanted? It would be a small native rebuild in `ClusterFSkillGain`; the Test Center already has a x5 gain factor. (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))
- P93-D12 [split] ELSEWHERE: The Animal Lore dashboard declares GPL-3.0: fine in the private repo, but it constrains any public release of the server code. OK to use? (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))
- P93-D13 [split]: Hunter's Bestiary gives +20% damage that stacks on slayers (about x2.4). When it joins F-24, keep it, shrink it, or cap it?
- P93-D14 [split] ELSEWHERE: UORespawn: keep it as an idea only, or unzip its ModernUO server scripts for a closer read? (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))
- P93-D15 [split] ELSEWHERE: Add the assessment copy (`notes\servuo-code-port-assessment.md`) to the Claude project as `claude/servuo-code-port-assessment.md`? (answered elsewhere: notes/decisions-2026-10-14.md, servuo.dev assessment (P93))

**P104** (2 asked, 3 noted) replaces P104-1:

- P104-D4: Should UORespawn stay an idea only, or do you want an M-sized wilderness filler of our own for custom areas? Nothing on the current plan...
- P104-D5 [split]: Delete `D:\UO\third-party\code\uorespawn\_extracted-muo\` (436 KB, still there)? Nothing refers to it.

**P106** (3 asked, 7 noted) replaces P106-0:

- P106-D6: Should `Shard-Console.ps1 -Status` run on a schedule every few minutes, so a shard question still emails you while the console is shut?
- P106-D9 [split]: Delete `D:\UO\question-proof\` (the scratch world, its broken copy and snapshot, about 138 MB, still there)? Nothing refers to it.
- P106-D10 [split] MOOT: Live is stopped at D94's load question (Delete the object and continue? y/n/a): answer y or a, n, or stop live? (moot: live is retired (cc-P108): live never exists until 1.0 and sl-modernuo is gone)

**P108** (2 asked, 6 noted) replaces P108-1:

- P108-D1: Start fresh is greyed because its new world took accounts from the live save, which is gone. Do you want a fresh test world again, and...
- P108-D8 [split]: The player launcher (`Play.ps1`, `Launch-Settings.ps1`, `Play-Lan.bat`, in the published player package) still points at 2593, where...

**P110** (6 asked, 1 noted) replaces P110-2:

- P110-D1 ELSEWHERE: Where is the Sunflower dashboard with Spoolman and the graphing app, so its tiles and widgets can be wired? (answered elsewhere: notes/cc-P133-haven-intranet-dashboard.md, Deviations item 4)
- P110-D2: The old dashboard had six ATM10 widgets reading the game PC; P110 cut them to one link tile (the server has been stopped for six weeks)....
- P110-D4 ELSEWHERE: Should Kevin's Parts (a client's stack) show its up or down on the Haven dashboard? (answered elsewhere: notes/cc-P133-haven-intranet-dashboard.md, docker/haven/services.json (kevins-parts-wp))
- P110-D5 MOOT: Homepage allows only LAN names; add Haven's Tailscale name to `DASH_ALLOWED_HOSTS` once Tailscale is on Haven? (moot: cc-P133 made the Haven intranet Tailscale only and rebuilt the dashboard for it)
- P110-D6 MOOT: Should `dashboard.shatteredlegacyuo.com` (public DNS) still reach a Homepage? (moot: the Haven intranet is Tailscale only (cc-P133); no public dashboard name)
- P110-D7 [split] ELSEWHERE: Confirm the rule: no NPM host for Homepage, and never route it through NPM or Cloudflare? (answered elsewhere: notes/cc-P133-haven-intranet-dashboard.md, Headlines)

**P113** (1 asked, 2 noted):

- P113-D2: The console window uses the website's `favicon.ico`, the same file the desktop shortcut uses. Keep sharing it, or copy it under...

**P126** (2 asked, 5 noted) replaces P126-0:

- P126-D1 ELSEWHERE: Should the Golem start phrase also match loose variants such as "golem work on shard tasks please"? (answered elsewhere: notes/cc-P131-wake-golem-from-console.md, Headlines (the two small fixes))
- P126-D7 [split]: Should the work PC (the Stone Golem) run Docker Desktop, so it can take port prompts, or stay on console, Haven-file and tools prompts...

**P137** (4 asked, 4 noted):

- P137-D1: The ankh menu offers Resurrect and Tithe Gold only, as pinned and OSI do after AOS (no Lock Karma). Keep that, or add Lock and Unlock...
- P137-D4 ELSEWHERE: P123 and P127 to P130 never reached the play-test page; run a small prompt to reconcile them (or make the importer treat a non-marker... (answered elsewhere: testing/playtest-steps.json, P123-1 to P130-10 (and P127-0))
- P137-D5: Eight working ankhs from ServUO's data (Felucca champion teleporters and Ter Mur's Stygian Abyss) are placed. Keep the Ter Mur ones, or...
- P137-D8 [split]: The other 85 ankh statics are art on OSI too and stay decoration. Do you want any of them working?

**P138** (2 asked, 7 noted):

- P138-D1: The kitsune ears and tail can now be worn by men (the rule is "not gargoyles", not "women only"). Keep it for both sexes, or make it...
- P138-D3: With a robe, the tail's root overlaps the robe's edge by up to 55 px in one walk frame. Leave it, or cut the tail at the robe too?

**P139** (2 asked, 9 noted):

- P139-D1 ELSEWHERE: Give the real Slinger the test creature's animating bow (or a shared `BodyActionBow`), or accept pinned's silent monster bow shot? (answered elsewhere: notes/cc-P140-rootdeep-burrows.md, the creature table (Burrow Scamp Slinger))
- P139-D6: TheArt's rideable red dragon `.vd` is 5.7 MB, over the 5 MB repo rule. Leave it out, or store it outside the repo (a git-ignored source...

**P140** (9 asked) replaces P140-8:

- P140-D1: The encoded creature animation files (sl-anim7.bin, 25 MB) are now git-ignored and built by the package build's encode gate. Keep that,...
- P140-D2: The Rootling: keep the hued stock bogling, or cut one Tree Fellow file down to a 1-tile size (about 0.5x, roughly 1.5 MB) and register it?
- P140-D3: The Burrow Scamp Slinger's colour: keep hue 1258 as shipped (the bow turns rust too), or the frame recolour that keeps the bow brown (a...
- P140-D4: The Overdraft's hue: keep 1740 brown, or 1901 iron?
- P140-D5: The Burrows creatures' parts per kill (1 normal / 2 elite / 3 boss) and the tutorial drops' gold (3 to 40) are first numbers. Keep them,...
- P140-D6: The mini champ engine: queue it as its own prompt (P24's port, about 610 lines plus a test), or leave the Burrow Mother carrying her own...
- P140-D7: The Ledger Bat is large (92 x 100 px at 1x) for a weak swarm creature. Keep it, give it a hue, or use a smaller body?
- P140-D8: The humanoids, vrark, plant, elemental and underdark packs' SOURCE.txt flag lines were left in their own wording. Should they read...
- P140-D9 [split]: Is the Overdraft's 1.5x walking crate boss-scale enough in the client, or should the AI art chat brief for a new boss body be written...

**P141** (8 asked) replaces P141-1, P141-5, P141-6:

- P141-D1: Approve the Rootdeep Burrows layout as drawn in notes/art/rootdeep-mockup/index.html (zones, rooms, the Vault's four rooms, the crawlway...
- P141-D2: A Young trainee who dies in the Vault: keep pinned's rule (the ghost wakes by New Haven's healer, about 57 tiles away, and walks back...
- P141-D3: The Warren fillers: keep Rotworm and Grubber as rare Warren spawns and BloodWorm (374-422 hits) as a rare Gloom spawn, move any of them,...
- P141-D4: Two trainees fighting the Overdraft together: the corpse follows pinned's looting rights, so the one who did less damage may not loot...
- P141-D5: Third-party tile kits: DRC1K's packs (X-2 to X-5) forbid modifications and reposting. Should any of them be used or asked about, or stay...
- P141-D6: The staff [go location (GoLocation): move it to the arrival at 5193,1138 with the map batch, or leave it?
- P141-D7: The 2026-10-18 01:30 nightly bot run was broken by P141's manual boot check. Re-run it now (Run-OvernightPlaytests.ps1 -Force), or let...
- P141-D8 [split]: The look per zone: which swatch set should each Burrows zone use (or a mix: say which floor, wall and door), from the mockup page's...

**P142** (11 asked, 2 noted):

- P142-D1: The Thieves' Den monster-stealing ladder (Initiate: OSI's places and the Burrows; Journeyman: every facet's dungeons; Master: later...
- P142-D2: The monster-stealing curve (5 / 11 / 23 / 35 percent at 100 / 120 / 160 / 200 skill, fame +1 to +5, the minor tier 2 to 5 percent from...
- P142-D3: The monster-stealing retry cooldown is 5 seconds per creature, for any thief, kept in memory. Keep it, or change it?
- P142-D4: The monster-stealing loot tables (minor weights 35/25/15/15/10, special draw 1/4/15/80, family part 10%, Den share of recipe scrolls...
- P142-D5: Two more Den recipes are proposed: the Gilded Lockpick (needs a LockPick.cs hunk) and Shadow Cloak IV (needs a fourth mule tier). Build...
- P142-D6: For monster stealing a boss is a loot-box boss or the Den's own list (The Burrow Mother, The Gloom Queen), and paragons do not count....
- P142-D7: The stolen flag and the Gem of Salvation timer are kept in a side save file, not on the mobiles. Keep that, or use ServUO's shape...
- P142-D8: The Balm of Protection applies but reduces nothing (its ServUO sites are not ported). Leave it inert, or add the one-hunk AOS.Damage...
- P142-D11 [split]: The three built Den recipes (the cloak, the bomb, the charm) come from stolen scrolls and the general box recipe pool. Keep that, make...
- P142-D12 [split]: Should the Burrows' two bosses join the loot-box boss list instead of the Den's own list (that also gives them loot boxes and rare...
- P142-D13 [split]: The Life Shield Lotion works for the pet Life Drain; should its other OSI site, the Harrower's tentacles (a four-line hunk in pinned's...

**P144** (3 asked, 9 noted):

- P144-D2: Your two PCs get Legion scripts from git, so the dev channel only serves a PC flagged dev with no repo. Keep the dev channel as the...
- P144-D5: When Set up scripts repo runs on the tower, the tazuo-sl-build client's older SL_Mining.py (152,611 bytes, 2026-10-05) lands in...
- P144-D8: Promote never removes an official Legion script: one deleted from the repo stays official until removed by hand on Haven. Keep that, or...

**P145** (3 asked, 7 noted):

- P145-D2: SL_Combat ships as eight top-level files (SL_Combat_*) because P144's publisher takes top-level *.py only. Keep that, or queue a P144...
- P145-D7: SL_Combat remembers whether it was enabled, so after a relog it starts in the state you left it. Keep that, or should it always start off?
- P145-D9: SL_Combat's starter profile weights, thresholds and hotkeys are first guesses (design doc section 12). Keep them, or change them?

**P155** (1 asked, 8 noted) replaces P155-5:

- P155-D9 [split]: Queue phase 2 of the web console (Golem controls: wake, poke, rest, wrap up, stopping point, long run, night shift, Run next, the...

**P160** (1 asked, 10 noted):

- P160-D2: Pace also gates the start phrase: ahead of pace the Golem rests, and pushing on means raising dayWeekAheadPct by hand. Want a one-off...

**P161** (1 asked, 9 noted):

- P161-D2: A queue-empty rest and a Golem stop also close the finished session after the delay. Keep that, or keep the last session open when the...

**T-008** (1 asked) replaces T-008:

- T-008-D1 [split]: Go to Eodon on the test shard (`[go 719 1863 40`, Ter Mur): is it reachable and does it have live spawns? If yes, write Q-064's...

## Tests

**`tools\tests\test_decisions.py`, 21 facts:**

- **Extraction:**
  1. A sample section gives one item per entry. It checks:
     - numbering carries into a second section;
     - the bold label is not one of the two sentences;
     - continuation lines;
     - nested bullets as options;
     - "Recommended:";
     - the anchor.
  2. **P77's notes give exactly P77-D1 to D8**, with D2's wording to the letter, D2 built (a placeholder), D6's two
     options, and D8's recommendation.
  3. **P78's notes give 12**, with D3's and D5's wording to the letter ("... Add a floor?"), every one built (defaults
     taken), and the anchor `decisions-for-chase-defaults-taken`.
  4. A new DONE prompt's decisions are open with nobody editing anything; a prompt that is not DONE gives none; each
     decision has a link, You decide and Where Questions.
- **Overlay:**
  5. notAsked gives noted; the overlay's wording wins; elsewhere carries the answer and source; moot carries the
     reason; a hand split gets its link and its "split" mark; an entry not in the overlay is asked.
  6. Replaced items get `replacedBy`. They leave the Who counts, and You decide counts the asking decisions; Mine and
     `summary.replaced` agree.
- **Answers:**
  7. Saved with who and when, shown on the card, changeable (the history is kept); the store holds the question.
  8. Refused: an unknown option, an empty answer, "built" where nothing is built, a moot one.
  9. **Taken:**
     - it needs `P<nn>`;
     - only answered ones are taken (Ask me later is not);
     - a taken answer is locked and leaves the default view (shown under All);
     - undo puts it back.
  10. **Exported:** `export_bundle` carries `testing/decisions.json`, a mirror written from it has the answer, and the
      copy text names it.
- **Where:**
  11. One Where per open item from its Who and steps, including Tailscale's "admin console" (outside, not Admin) and
      a hand-set place. A passed item gets none.
  12. **Each chip's counts** under Open: Questions 2, Outside 2, Admin 1, Player 4 (Human 1, Gargoyle 1, Elf 1, Any
      1), Bot 1, CC 1. The answered-elsewhere decision is not counted.
  13. **Combining with Mine:** Mine gives 9; Mine + Player 4; + Human 1; + Any 1; Mine + Questions 2. Bot + Player is
      empty, because Bot items have Where Bot.
- **Service** (the real `server.py` on a free port with a scratch root):
  14. `/api/items` carries the decisions, `replacedBy` and Where. Then:
      - answer: 200;
      - a bad choice: 400;
      - an unknown id: 404;
      - new answers 1, and `/api/summary` `answers_new` 1;
      - the copy text;
      - `decisions.json` written;
      - later;
      - taken into P150, after which a change is a 400.
- **Page (text):**
  15. The Where chip row, its eight labels, and the counts wired to the buttons.
  16. The card's buttons and routes.
  17. **Answered, not yet taken**, the new-answers count, the open count without replaced items, and Open is still the
      default.
  18. ASCII.
- **Real files:**
  19. Every overlay entry is an item; every asked, elsewhere and moot one has a question and a link, and every
      elsewhere and moot one has its source or reason.
  20. Every open You decide item is replaced by decisions that exist.
  21. P89-D10 and P106-D10 are moot; P59 and P80 are 8 of 8 elsewhere.

**`tools\tests\test_play_who.py`, 1 new real-files fact:** every open item and every active decision has a Who and
exactly one Where, and the Where counts add up to them (replaced items left out).

**Seen failing first:**
- **With the P146 code removed:** `decisions.py`, `playwhere.py` and the overlay moved away; `opsdata.py`,
  `server.py` and `index.html` at HEAD.
  - **20 of 21 failed.** The one that passed is "the source stays ASCII": the old page is ASCII too.
  - The new real-files fact in `test_play_who.py` also errored.
- **Restored:** all five files were `cmp`-identical to the kept copies.
- **Four targeted breaks** (`scratchpad\p146\breaks.py`), each in the code alone. After each one the file was
  restored and checked by SHA-1:

| Break | Caught by |
|---|---|
| numbering steps by 2 | the P77 fact, and 8 others |
| "Any character" matches every item | the two chip-count facts |
| taken also takes "later" | the taken fact |
| `decisions.json` left out of the export | the export fact |

**Whole suites:**
- **shard-migration `tools\tests`: 151 of 151.** It was 129 with 1 failure at the start: 11 unsorted items
  (P139-0, P160-0, P161-1 to 6, P162-1 to 3). I sorted those (above).
  - In one of four full runs, P105's `test_haven_mode_separates_the_data_and_guards_export_and_ingest_with_the_token`
    errored once. It passed on its own and in the next two full runs.
  - I did not keep the error text. That test starts its own service, so a port or timing race is the likely cause.
    **Unverified.**
- **Importer Pester (`Import-PlayTests.Tests.ps1`): 20 of 20.**
- **Bot suite (`D:\ShatteredLegacy\tools\playtest-bot\tests`): 40 of 41.** The failure is
  `test_installer_dry_run_prints_the_call_and_registers_nothing`, the known environmental one (the nightly task is
  installed; P112 and P115 recorded it).
- **Console Pester was not run.** Its facts do not read `server.py`, `index.html` or the tools this changes (grep);
  the CHANGELOG facts use fixtures.

**The real check in a browser** (`scratchpad\p146\browser_check.py`):
- **Setup:** headless Chrome 155 through Selenium, on the new `server.py` with a scratch copy of today's notes, docs
  and testing, port 18096.
- **The API:**
  - 703 decisions;
  - Who: You 114, Bot then you 27, You decide 124, Bot 95, CC 80, Not sorted 0;
  - Mine 265;
  - 17 replaced.
- **Open:**
  - 440 cards, 124 of them decisions;
  - chips: Anywhere 440, Questions 124, Outside the game 69, In game: Admin 30, In game: Player 42.
- **Mine:** 265 cards, and the same chip counts.
- **Mine + In game: Player:** 42 cards, only You and Bot-then-you badges. The sub-chips read Human 8, Gargoyle 1,
  Elf 8, Any character 27.
- **+ Elf:** 8 cards (P138-4, P138-6, P81-0, P62-2 to P62-6).
- **Mine + Questions:** 124.
- **Answering:**
  - P77-D1 by its first option and P77-D2 by text;
  - Mine + Questions went to 122;
  - the header read "You decide 122 | 2 new answers";
  - Answered, not yet taken showed both "Your answer: ..." lines;
  - `decisions.json` held both, with times.
- **Phone width:** 485 px of content in a 500 px window (headless Chrome's minimum), so no horizontal scroll.
  Screenshots are in the scratchpad.
- **The console:** only the old `/favicon.ico` 404.
- **Found and fixed there:** the header's "333 open" still counted the 17 replaced items. It now reads 316. A fact
  pins it.
- The scratch service was stopped. Its copy is in the scratchpad, outside both repos.

## Where, item by item

- **Derived** from Who and the steps' Where line for every open item.
- **Set by hand:** 2 items, plus the 11 newly sorted, which got their steps written for it.
  - **P62-6:** an Elf test whose line also names Eve, who stands by. It is Player, Elf.
  - **P138-6:** "the female character with the ears and tail". It is Player, Elf.
- **Rules that a test pins:**
  - "Tailscale admin console" (P155-1, P155-6) is outside, not Admin.
  - A Where line naming Admin or Eve and a player (T-011, P114-2, P119-4, P121-2) is Admin, because it needs the
    Admin account.
  - P114-1, all four shortcuts, is Admin.
- **Player items naming several accounts** (P81-0: Human, Elf and Gargoyle) appear under each sub-chip. The main Where
  is still one.

## Deviations and decisions for Chase

1. **535 older deviations are "noted", not asked.** Every notes file's section is read, as the brief asks: 703 items.
   But most entries in a "Deviations and decisions" section report what CC did, and asking all of them would bury
   the real questions.
   - **Asked:**
     - every prompt with an open You decide item;
     - the prompts the brief names (P65, P82);
     - those whose steps say to answer decisions (P81, P113);
     - every prompt from P136 on;
     - each read by hand, keeping only real choices open.
   - **The 51 older prompts** (P61 to P135, apart from those) are in the overlay's `notAsked`.
   - Their items are under **All** with "noted, not asked", and **can still be answered**.
   - **From P146 on, every new prompt's section is asked automatically.** That will include its pure reports: a
     prompt's notes can avoid that by putting reports under "Deviations" and questions under "Decisions for Chase".
     Or the overseer adds noted lines to the overlay.
2. **The count is 124 open, not "roughly 70".** The brief's 70 is the named prompts: P65 10, P72 10, P75 7, P76 8,
   P77 8, P78 10, P79 8, P82 5, P93 1 = 67. The rest is P81 3, P92 1, P104 to P126 (9), T-008 1, and **43 from the
   recent P137 to P161** (67 + 3 + 1 + 9 + 1 + 43 = 124).
3. **The brief's "19 You decide items" are 17 open** (counted above). P140-8 has a triage row but no item on the
   page: P140's notes list it, but the importer stopped at P140-7. Its question is P140-D2.
4. **Answered elsewhere is not counted as a new answer.** It shows as answered with its source, outside the default
   view (under All and Questions), since the overseer already has it.
5. **The overseer's "taken" is a button on the page** (Taken into P...; Not taken undoes it), like the ideas inbox's
   status writes. The overseer can also read `testing/decisions.json` in the repo, or run
   `python tools\decisions.py answers`.
6. **Where for CC items is "CC"**, beside Bot. The brief lists no chip for them; the existing CC button covers them,
   as the Bot button covers Bot.
7. **No task list for Chase.** The hand-off asked for one task per step. This session had no task-list tool
   (ToolSearch found none), so there was nothing to keep in progress.
8. **The Read tool was refused, unattended, on `D:\ShatteredLegacy\docker\test-queue\server.py`.** I wanted
   `Read D:\ShatteredLegacy\docker\test-queue\server.py` to read the service before patching it. As the standing
   memory note says, I read it with Bash `cat` instead, and patched both shard-repo files by script. Nothing was
   skipped.
9. **For the overseer, from the reading agents** (not changed here):
   - **P139's real items, P139-1 to 4, have triage rows and steps but never imported.** Its For Chase opens with a
     "Deploy first" paragraph the importer reads as a deploy marker. Only P139-0 came in; it is sorted DEPLOY.
   - **P141-D7** (re-run the broken nightly) is moot once a nightly has run.
   - **P78-D11** is an overseer task (the F-43 entry in `docs/fidelity-principle.md`), so it is noted, not asked.
   - **P110-D7** (never route Homepage through NPM or Cloudflare) is answered by cc-P133, Tailscale only. If you would
     rather confirm the rule yourself, the overlay line changes it to open.
10. **The bot's P64-1 and P64-2 will keep failing** while the newest CHANGELOG section is Staff-only. This one is too
    (P115's Deviation 5).

## For Chase

- **Where the decisions are:** the play-test page, `http://192.168.1.61:8093/`.
  - Press **Mine**, then the **Questions** chip: 124 questions, grouped by prompt.
  - Or leave Open on and pick a Where chip to do everything of one kind in one sitting. For example, Mine +
    **In game: Player** + **Elf** is 8 items.
  - The chips: Questions, Outside the game, In game: Admin, In game: Player (Human, Gargoyle, Elf, Any character).
- **How to answer** a card:
  - press one of its choices, or **Keep what's built**;
  - and/or write in the box and press **Save answer**;
  - or press **Ask me later**.
  - The card then says "Your answer: ..." with the date (and who, once Cloudflare Access is on).
  - Change it any time until the overseer takes it.
  - **More from the notes** opens the detail and a link to the exact notes section on GitHub.
- **The answers reach the overseer on the next commit.** The Golem's commit mirrors the page's data from Haven into
  `testing/decisions.json`. The header's **N new answers** and **Answered, not yet taken** show what is waiting.
  Once the overseer writes them into a prompt, they mark them "Taken into P<nn>" and those cards leave your view.
- **Nothing to deploy or restart.** Haven pulls this commit within 2 minutes, and the service restarts itself on the
  new `server.py` (cc-P137).

## Repo size

- No file over 5 MB is pending. The largest new one is `testing/decisions-overlay.json`, 92 KB.
- Scratch stayed in the session scratchpad, outside both repos:
  - the extract and overlay files;
  - the agents' generator scripts;
  - the browser copy and screenshots;
  - the break script.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run after these notes were
written (it also refreshed the mirror from Haven: `testing/SUMMARY.md` and `testing/play-tests.json`, which are machine
output):

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code:** `CHANGELOG.md`, `VERSION`, `docker/test-queue/README.md`, `docker/test-queue/html/index.html`,
  `docker/test-queue/server.py`.
- **docs:** this note, `testing/decisions-overlay.json`, `testing/bot-triage.md`, `testing/playtest-steps.json`,
  `tools/decisions.py`, `tools/playwhere.py`, `tools/opsdata.py`, `tools/tests/test_decisions.py`,
  `tools/tests/test_play_who.py`, and the mirror's `testing/SUMMARY.md` and `testing/play-tests.json`.

P146 DONE
