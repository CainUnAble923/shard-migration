# P388: player guide to levels, loops, scrolls, and the New Haven start

2026-10-21. Draft wiki page only. Work copies are the ShatteredLegacy and shard-migration repositories under `D:/UO/golems/Valorite-tower/`.

## Result

Created `notes/wiki-drafts/levels-loops-and-scrolls.md`, following the League and Society of Smiths page models. The draft distinguishes the built graduation loop from the planned F-12 level, XP, cap, skill-retention, and scroll system. It includes every ladder state, reset/retention guidance, Young rules, Sources, and Contradictions.

No code, tests, configuration, saves, services, or migration `docs/` files changed. No Haven connection, deployment, server operation, image build, commit, merge, push, or branch switch. No art was needed. No agents were delegated.

## Reading and scope

Read both work-copy AGENTS.md files first, the direction decision, governing-doc index, and task-list agreements. Used canonical `server/customizations/`, `server/patches/`, and `server/tests/`. Did not read `server/uo/`. Read-only pinned ModernUO reports commit `d4531cd94b739613155225c234900de9f47d2c88`.

Read the guide models, then the relevant feature-queue entries, especially F-5, F-9, F-12, and F-35. Followed their references into `notes/f12-levels-loops-caps.md` and `notes/f12-decisions-2026-10-05.md`. Read the corresponding topic sections in these task notes:

- `cc-P18-reset-stone-young-craftx.md`: Young implementation and the separate testing reset tool.
- `cc-P20-skill-scaling-research.md`: early level research, power-scroll implementation and conflicts; its historical high-skill and exploit details were not copied to the page.
- `cc-P23-live-defect-sweep.md`: D43 stock-scroll refusal, overwritten caps, and removal of the Smith scroll catalog.
- `cc-P25-stats-above-125-research.md`: historical stat/reset interactions, rather than a current promise of stat ceilings.
- `cc-P53-two-hundred-cap.md`: the built flat 200 skill policy.
- `cc-P54-f12-xp-and-gain-paths.md`: XP sources, echo, reserve, and numerical research. Used the later October 5 decision record to distinguish approvals from recommendations.
- `cc-P65-evo-pets-framework.md`: persistent pet stage and the missing owner-loop integration.
- `cc-P79-loot-boxes-fanfare.md`: existing rewards and the earlier loop placeholder.
- `cc-P80-new-player-tutorial.md`: tutorial framework, core/wings, recruiter, rewards, vision, and the P371 corrections.
- `cc-P103-tazuo-client-command.md`: tutorial client-window additions; no client command syntax is needed in this page.
- `cc-P172-pet-gain-speed.md`: owner-loop source still a placeholder; no promise of new pet progression from graduation.
- `cc-P189-cont-old-haven-new-player-safe.md`: Old Haven is not uniformly harmless; no blanket safety claim.
- `cc-P192-cont-fountain-of-youth.md`: checked the Young-clock change and its explicit wiki secrecy rule. No location, method, secret achievement, or link to that staff-only note appears on the draft page.
- `cc-P239-creature-levels-appraisal.md`: provisional strength estimate, separate from F-12 XP levels.
- `cc-P276-tutorial-farm-build.md`: implemented pet lesson, remaining placement/client work, and graduation-pet exception.
- `cc-P282-f12-numbers-and-level-gates.md` and its Codex review: corrected ladder, five-level reserve, approved baseline versus proposed transaction/valuation, and unverified pacing.
- `cc-P283-skill-gain-paths-research.md` opening/current-path findings: a 200 cap does not prove every training path exists.
- `cc-P371-graduation-is-the-first-loop.md` and its Codex review: real first loop, travel restriction, Young retention, skip default, missing F-12 work, and review limitations.
- `cc-P378-playtest-plans-10-21.md` scope/coverage: pending plans are not evidence of completed playtests. Also checked the P381 work-note format.

The large research notes were read for their relevant progression, scroll, tutorial, or Young sections, not presented as a new audit of every historical skill table. The page does not copy their historical coverage counts, model pacing, proposed level rewards, or undecided scroll prices.

## Current source evidence

Paths in this table are relative to ShatteredLegacy unless explicitly prefixed `pinned/`. File and line evidence stays here, not on the player page.

| Claim | Evidence |
|---|---|
| Per-character loop count, no new level implementation | `server/customizations/Tutorial/ClusterFLoops.cs:23-31` reads a character-serial key; `:34` graduates to loop 1; `:36-42` documents and leaves the reset hook empty. `:47-61` rejects repeated/backward awards, calls the empty hook, stores the counter, and awards the loop. |
| Ladder formula | `server/customizations/Tutorial/ClusterFLoops.cs:31`: loop 0 -> 50, loop 1 -> 100, then `100 + 5 * (min(loop, 21) - 1)`. The page enumerates loop 0 through loop 21. The scroll-target rows are 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200. Those rows substantiate the 20 scroll steps; creation plus loops 1..21 account for all 22 cap states. |
| Vision changes no progression | `server/customizations/Tutorial/ClusterFLoops.cs:69-87` sends text, particles, sound, and completes the station. It never calls CompleteLoop or changes a skill/stat. Its universal skill-reset narration is not treated as the complete Keeper/Breaker specification. |
| Tutorial entry and later characters | `server/customizations/Tutorial/ClusterFTutorial.cs:64-96`: entry is per account; login grants a character its first loop if the account record is graduated, or skipped with the waiver enabled. There is no normal-graduation reward call in that login waiver. |
| Recruiter identity, location, and interaction | `server/customizations/Tutorial/TutorialRecruiter.cs:25-31` sets plaza spot, name Rook Hallowell, and title; `:50-67` opens the tutorial gump on double-click in range. Placement is a seeder, not proof of a placed NPC in a running world. |
| Core, optional wings, placeholders | `server/customizations/Tutorial/TutorialStations.cs:58-76` enumerates the core; `:176-180` registers the loop vision. `server/customizations/Tutorial/ClusterFTutorial.cs:122-138` runs a handler or explanation fallback; `:141-156` completes the core and announces optional wings. `server/customizations/Tutorial/TutorialFarm.cs:112` installs the farm's animals handler. No claim that all trials are playable. |
| Player-facing graduation and skip | `server/customizations/Tutorial/TutorialGumps.cs:44-67` shows the core/wing list and graduate button after CoreDone; `:82-100` routes the buttons; `:108-145` implements the two skip confirmations. `server/customizations/Tutorial/ClusterFTutorial.cs:216-240` checks only active tutorial/core completion before graduation, not a current level of 50. |
| Provisional skip default and remedial | `server/customizations/Tutorial/ClusterFTutorial.cs:36-45` defaults the waiver true; `:162-188` records skip and conditionally graduates; `:193-207` starts remedial; `:232-233` calls the idempotent loop award and normal graduation rewards. |
| Graduation box/pet | `server/customizations/Tutorial/ClusterFTutorial.cs:249-263`: Explorer tier 1 award, town-opening guidance, farm-pet flag suppression, starter-line validation. The page avoids promising a pet if follower capacity prevents the grant. |
| Island travel and dungeon | `server/customizations/Tutorial/TutorialIslandGate.cs:14-28` defaults the gate true, identifies Haven surface and Rootdeep annex, and checks loop 0. `:30-42` refuses off-island destinations while allowing island movement and lifecycle internalization. Spell/boat entry points follow at `:44-84`. The draft states the ordinary player rule without bypass instructions. |
| Skills currently default to 200 independently of loop | `server/customizations/ClusterFSkillCaps.cs:11`, `:27-30`, `:35-43`, `:150-151`, `:160-196`: configured flat cap, all-skill total policy, world-load/login application, no call to MaxLevelFor. The page describes every skill being trainable in principle, without asserting every 200 training path has shipped. |
| Current stock power scrolls | `pinned/Projects/UOContent/Items/Special/Special Scrolls/PowerScroll.cs:238-272`: CanUse refuses when the named skill cap is already >= the scroll value; Use sets that skill cap. `server/customizations/ClusterFSkillCaps.cs:187-196` explicitly overwrites skill caps on application. No custom PowerScroll replacement or scroll patch was found in the canonical layering inspected. Thus 105..120 scrolls cannot open F-12 loops under default 200 caps. |
| Different temporary player-strength estimates | `server/customizations/ClusterFCreatureLevels.cs:41-79` defines the source and best-base-combat-skill estimate, with a fixed-level setting alternative. `server/customizations/LootBoxes/ClusterFLootBoxes.cs:48-69` uses the real loop provider but total base skills / 10 for its level placeholder. Neither is player XP storage. |
| Young play-time limit and wording | `server/customizations/ClusterFYoungPlayer.cs:35-51` defines 336 hours and the account play-time clock. `:54-70` supplies the voluntary phrase and confirm window; `:109-111` builds the remaining-play-time login line. `server/patches/Account-young-duration.patch:9`, `:20`, `:31`, `:41` routes duration, countdown, and expiry to those helpers. |
| Skill gain does not remove Young; other endings remain | `server/patches/PlayerMobile-young-time-only.patch:8-13` removes the 450 skill-total condition. `server/customizations/ClusterFYoungPlayer.cs:5-15` explains retained murder and standard-renunciation rules; the current existing Young verification cases below exercise them. Loop recording has no RemoveYoungStatus call. |
| Young is not immunity in tutorial fights | `server/customizations/Tutorial/TutorialCreature.cs:31` overrides IgnoreYoungProtection true. No list of special hostile creatures, exploit routes, or hidden achievements is included in the page. |

## Existing verification cases inspected as source

No tests were added or modified, so no new red/green obligation arises. Lane tests: none, per prompt. These are source inspections, not tests executed by P388:

- `server/tests/Tutorial/GraduationLoopVerification.cs:71`: persistence, first-loop reward once, unchanged skill and Young, and later-character first loop. `:114`, `:157`, `:202`, `:215` cover ordinary movement/travel, internalization, and the dungeon. `:238` checks both skip settings and remedial idempotence. `:273` checks representative ladder states, including the terminal clamp.
- `server/tests/Misc/TutorialVerification.cs:111`, `:139`, `:171`, `:193`, `:225`, `:258`: saved entry, two confirmations, account scope, vision/Young, tutorial creature engagement, core/wings and graduation.
- `server/tests/Tutorial/TutorialFarmVerification.cs:205`, `:272`: pet/pest/healing lesson and no second graduation pet after the farm.
- `server/tests/Misc/YoungPlayerVerification.cs:100`, `:109`, `:146`, `:186`, `:238`, `:256`: 336-hour duration, skill total not ending Young, account-wide expiry, both voluntary phrases/confirmation, murder, and countdown formatting.
- `server/tests/Misc/TwoHundredCapVerification.cs:80`, `:135`: current cap default/migration and existing above-cap base skill preserved. The guide does not advise use of old over-cap characters.

## Decision evidence and contradictions

`notes/f12-levels-loops-caps.md:32-55` supplies current/max distinction, path-dependent skills, paired scroll/loop steps, reserve, and intended sources. `:76-94` retains stats. `:104-129` separates current-level gear gates, permanent capacity, collections, guilds, and recipes. `:258-295` identifies exact reserve valuation and transaction as proposals. None is represented as deployed behavior.

`docs/feature-queue.md:1225-1238` records the 21-loop ladder, Keeper/Breaker progression, and older 25-percent reserve. `:1240-1250` distinguishes skill echo from shared level echo; the later post-cap paragraphs remain alongside it. `notes/f12-decisions-2026-10-05.md`, Levels and XP, supplies approved XP sources, raw reserve credit, overflow loss, and terminal zero reserve. `notes/cc-P282-f12-numbers-and-level-gates.md` reaffirms the five-level reserve, correct ladder, and proposed exact transaction. No play-time estimate or unapproved level reward is advertised.

The page retains differences over ladder versions, flat versus designed skill caps, the vision's universal skill-reset narration versus Keeper/Breaker retention, graduation versus the modeled at-cap first reset, reserve size, post-cap loops, Young removal, tutorial format/completeness, temporary strength estimates, and scroll semantics. It makes no decision to settle them and changes no source document.

P371's Codex review also flags tutorial-disabled exit behavior and transport/pet ordering. These are reported review findings, not newly reproduced by P388. They are not turned into player instructions or bypasses. Live behavior, resolution of those findings, pet owner-loop integration, and transport edge cases remain unverified here. P371 explicitly leaves the full XP/skill reset integration unfinished; the draft does not mistake a method name or cap formula for that implementation.

## Validation and limits

The source snapshot establishes code and decisions, not deployed availability. No running-shard settings, world placements, client play-through, scroll acquisition rates, or XP pacing were checked. P276's world/client work remains recorded as unfinished in its note. No main-shard changes are implied by this guide.

Used Windows PowerShell 5.1.26100.9444 for shell work. `rg` is unavailable, so searches used Get-ChildItem and Select-String. No PowerShell 7 syntax or pwsh. No skills/plugins or network tools were needed.

Ran the required local progress reporter with SL_SHARD and SL_MIGRATE set to the two work copies and SL_SERVUO to the read-only reference: `python -B tools/progress.py --dry-run`, exit 0. As its source shows, dry-run still writes `tools/progress.json`. Its diff changed the generated time and removed active queue entries, unrelated to this guide. Following P381's docs-only handling, restored that one previously clean generated file to its exact HEAD bytes. It did not rewrite README, dashboard, or migration docs. The tool's broad content counts are not guide claims or independently recounted here.

Final editorial review: all relative Markdown links resolve; the ladder rows match the current source hook and enumerate all scroll targets; Sources and Contradictions are the last two sections. The page has no file:line citations, staff commands, exploit instructions, or hidden-achievement spoilers. Both new files are ASCII, have terminal newlines and no trailing whitespace, and are below 5 MB. These are editorial checks, not added test cases or a new repository gate.

Both repositories pass `git diff --check`. The code work copy is clean; migration status contains only the two requested new notes files. The generated progress JSON matches HEAD byte for byte. No tests were added, modified, or run. The stop-request file was absent at final review on October 21, 2026, at 22:10 CDT; it is checked again immediately before the completion marker.

P388 DONE
