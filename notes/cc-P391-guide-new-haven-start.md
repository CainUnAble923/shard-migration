# P391: player guide to the New Haven start

October 22, 2026. Golem Codex lane, Valorite-tower work copies. Docs-only draft.

## Deliverables and boundaries

- Player page: [new-haven-start.md](wiki-drafts/new-haven-start.md).
- This evidence and verification note.

The page covers arrival, Rook, the nine core entries, optional wings, the farm and Vault lessons, skipping and remedial, starter pets, boxes, graduation as loop 1, Young retention, and leaving the island. Sources and Contradictions are its final sections. Planned trials are explicitly marked (planned).

Read both work-copy root AGENTS.md files first, plus the document-governance index, direction decision, task list, model League and Society pages, and the relevant feature queue sections. No code, patches, tests, deployment, running settings, accounts, or docs/ files were changed. No Haven connection, commit, merge, push, or branch switch. No delegation or network research was needed.

## Reading scope

Searched top-level notes/cc-P*.md for New Haven, Rook Hallowell, tutorial, core and wing trials, remedial, graduation, evo pets, and boxes. Read primary tutorial histories P80, P276, and P371 with its review, and the October 14 tutorial decisions directly. Related topic sections inspected: P14/P15 (arrival and board), P59/P65 (pet choices), P79 (boxes), P103 (client window buttons), P140/P141 (tutorial creatures and Vault), P188/P189 (way in and Old Haven safety), P192 (Young clock and explicit wiki exclusions), P201/P275 (net lesson), P146 (decision pointers), P217/P377 (older wiki descriptions), P364 (bestiary context), P378 (pending playtest plans), and P387/P388/P389 (related guide evidence and unresolved limitations). Large research, intake, and playtest notes were screened for topic passages, not treated as newly executed verification. Some broad combined output was truncated; claims below use focused reads of the relevant decisions and current source instead of unseen output.

P276's continuation P372 has no matching cc-P372 note in this work copy. P289's playable-core prompt is mentioned by P371, but the canonical station handlers here still contain only the vision and farm Animals handler. No pending prompt or playtest plan is counted as built behavior. The page does not disclose hidden achievement names, triggers, locations, or rewards and does not link to secret material.

Final source pass also screened all matching tutorial/remedial/graduation passages across the remaining cc-P notes, including incidental intake, status, service, and playtest references. P165's client handshake repair is relevant to P103's window buttons and is included in Sources; its own notes leave their in-client check unfinished. The two P391 draft files were already untracked at this session's initial status check. Reviewed their claims against current canonical source before retaining and completing them.

## Current implementation evidence

Paths below are relative to the ShatteredLegacy work copy unless prefixed M (shard-migration). File:line citations belong here, not on the player page.

| Guide claim | Source evidence |
|---|---|
| All new characters start in New Haven | `server/customizations/CharacterCreation.cs:129-135` restricts available starting cities to New Haven, 3503,2574,14 Trammel; `:268-269` moves the character to its start. The older city arrays alone are not the current choice list. |
| Rook and nearby interaction | `server/customizations/Tutorial/TutorialRecruiter.cs:25-31` sets the plaza location, Rook Hallowell, and League recruiter title; `:50-67` opens orientation on nearby double-click; `:74-82` points at a recruiter only if one is found. `:113-117` defaults placement on load off. No current-world presence is asserted. |
| Entry, saved account scope, active character | `server/customizations/Tutorial/ClusterFTutorial.cs:49-57`, `:64-96`: first entry is gated by account NotStarted, character serial is saved, and later login can grant a graduated account's later character its own first loop. No normal graduation rewards are called by that login waiver. The saved record is exercised by the existing entry test listed below. |
| Directory and older quests | `server/customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs:61-65` places the board beside arrival; `:102-111` describes double-click for the directory and training quests on its second tab. The page does not publish a separate training-quest count. |
| Nine core entries | `server/customizations/Tutorial/TutorialStations.cs:59-76`: movement, paperdoll, backpack, chat, death, banking, travel, league, loop. The complete key inventory is recorded below. |
| Preview versus hands-on lesson | `server/customizations/Tutorial/ClusterFTutorial.cs:122-138` runs a registered handler or opens a preview and marks completion. `TutorialStations.cs:176-180` registers the vision; `TutorialFarm.cs:104-113` registers Animals. Search across canonical customization C# found no other TutorialStations.Handlers registrations. `TutorialGumps.cs:189-197` says the trial is still being built and lists intended locations/tools. These lists alone do not prove lessons or supplies delivered. |
| Graduation requires core only | `server/customizations/Tutorial/ClusterFTutorial.cs:100-119`, `:142-156`, `:216-240` checks the nine core keys, announces optional wings, and permits graduation with no level-50 or Vault-clear predicate. `TutorialGumps.cs:44-67` displays the core/wing list and Graduate after core completion; `:82-100` routes the player actions. The UI currently lists wings even before core completion; the guide does not claim strict UI locking. |
| Supported client buttons | `server/customizations/Tutorial/TutorialGumps.cs:157-184`, `:203-225` offers World Map, Journal, and options only to a client that supports the command handshake. P103 supplies the client patch history; no installed-client verification was performed. |
| Farm location and lesson | `server/customizations/Tutorial/TutorialFarm.cs:53-70` defines dog/cat, west gate, 3 pests and 10 bandages as defaults; `:130-166` gives directions and Farmhand dialogue; `:171-188` gives a pet only on the correct step and records success; `:192-222` credits player or controlled-pet damage and completes Animals; `:225-255` supplies bandages and recognizes successful Healing or Veterinary, completing Bandages. `:469` names Wren Tallow. |
| Farm progress and availability | `server/customizations/Tutorial/TutorialFarm.cs:93-94` keeps the unfinished pest count in memory; completion keys are in the account record. `:293-307` refuses placement outside the test shard by default or with the old trees remaining. M `notes/cc-P276-tutorial-farm-build.md`, headlines and Continuation, explicitly leaves world placement and client work unfinished. The farm's unguarded location is recorded there and in F-35. |
| Tutorial fights can hurt Young trainees | `server/customizations/Tutorial/TutorialCreature.cs:31` opts tutorial creatures out of Young protection. No claim that Old Haven or the farm is uniformly safe is made. |
| Vault participation and one-way route | `server/customizations/Regions/RootdeepVault.cs:122-160` admits the active trainee and their pet and rejects cleared/nonparticipating players; `:171-201` credits damage on Overdraft death and opens the crawlway; `:205-233` carries a credited living player and pets into the Warren. `:238-248` turns out disallowed logins. Its credit key at `:94` is outside the core list. M P141 and P188 establish the built route and unfinished placement/client checks. |
| Net lesson | `server/customizations/Items/Traps/Deployable/TrapLesson.cs:69-96` defines the lesson, two practice nets, and trainee entry checks; `:106-118` records a Penny Rat or Hoarding Rat held by a trainee's net. The key is not a core station. M P275 records this built, with world hazard placement left for seeding. |
| Skip confirmations and remedial | `server/customizations/Tutorial/TutorialGumps.cs:108-145` implements both prompts. `ClusterFTutorial.cs:162-207` records skip, conditionally records the first loop, grants the public skip achievement, and clears station progress on remedial entry. `:36-45` defaults skip-as-graduation true and explicitly calls it provisional. Skip does not invoke normal GraduationRewards. |
| Public tutorial achievements | `server/customizations/ClusterFAchievements.cs:1162-1177` defines Didn't Read the Manual and Read the Manual Eventually without a hidden flag; the remedial entry requires the skip achievement. `Tutorial/ClusterFTutorial.cs:235-237` grants the latter at remedial graduation. Values are omitted from the page since they are unnecessary for the route. |
| Graduation rewards and pet exception | `server/customizations/Tutorial/ClusterFTutorial.cs:210`, `:232-233`, `:249-263`: loop award precedes normal rewards; Explorer tier 1 is the tutorial award; farm.pet suppresses the four-line pet choice. `TutorialGumps.cs:228-264` implements that choice and full-follower refusal. No promise that a closed graduation picker can be reopened at Rook is made. |
| Ordinary bonded pet and slot | `server/customizations/Mobiles/Evo/EvoPet.cs:23` derives from BaseCreature; `:78` sets 1 slot; `:470-493` assigns control, bond, follow, and hue choice. `:28` leaves OwnerLoopsSource at zero. This is not wired to the real first-loop counter. Role abilities, high-stage unlocks from graduation, or a squire are not advertised as available. |
| Loop record and missing resets | `server/customizations/Tutorial/ClusterFLoops.cs:23-34` reads a per-character loop and defines the 50/100 ladder hook; `:36-42` leaves level/skill resets empty; `:47-61` rejects repeat/backward loops, stores the count, and calls the loop reward. `:69-87` is text/effects plus station completion only. The vision's reset narration is not evidence of an implemented reset. |
| Separate first-loop box | `server/customizations/LootBoxes/ClusterFLootBoxes.cs:218-221` awards a Loop box; `Tutorial/ClusterFTutorial.cs:249-251` separately awards the Explorer box. `server/tests/Misc/TutorialVerification.cs:287-300` checks two boxes at normal first graduation. Additional achievement boxes are possible, so the page does not promise exactly two total carried boxes. |
| Opening a bound box | `server/customizations/LootBoxes/LootBoxItems.cs:172-211` requires the matching account, backpack, and guarded region with guards enabled or a house in which the character is a friend (including owner/co-owner). The page uses this broader current rule rather than repeating the tutorial line's own-house shorthand. |
| Island restriction | `server/customizations/Tutorial/TutorialIslandGate.cs:13-28` defaults enabled, includes the island surface and Rootdeep annex, and identifies loop 0; `:30-42` permits local movement and refuses exits; `:44-84` adds spell and boat checks. The page gives the ordinary rule without route bypasses, settings names, or staff exemptions. |
| Young retention and clock | `server/customizations/ClusterFYoungPlayer.cs:35-51` defines 336 hours of account play and the clock accessor. Its header at `:5-12` retains murder and voluntary renunciation; `server/patches/PlayerMobile-young-time-only.patch:8-13` removes skill-total expiry. `Tutorial/ClusterFLoops.cs:47-61` never removes Young. No secret reset route is documented. |

## Station inventory counted from source

Counted the `new("...", TutorialWing...)` rows in `server/customizations/Tutorial/TutorialStations.cs`, not its header or P80's reported total. There are 9 core entries and 28 wing entries in this one file.

Core: core.movement, core.paperdoll, core.backpack, core.chat, core.death, core.banking, core.travel, core.league, core.loop.

Wings: combat.weapons, combat.healing; magic.magery, magic.necromancy, magic.chivalry, magic.bushido, magic.ninjitsu, magic.mysticism; gathering.mining, gathering.lumberjacking, gathering.fishing, gathering.camping; crafting.blacksmithy, crafting.tailoring, crafting.carpentry, crafting.tinkering, crafting.alchemy, crafting.fletching, crafting.cooking, crafting.inscription, crafting.cartography; animals.taming; bard.trial; thieving.trial; housing.basics; travel.wing; reputation.wing; shard.systems.

This is a row count, not 37 playable trials. Current registrations are core.loop in TutorialStations.cs and animals.taming in TutorialFarm.cs. Farm healing completes combat.healing through its separate skill hook. Vault and net credit keys are not extra required core rows.

## Decision evidence and contradictions

M `docs/feature-queue.md:2753-2804` describes F-35's vision-first story, guildmasters, and freely skipped steps; `:2889-2901` moves the pet before combat and decides a bonded evo dog/cat; `:3256-3276` records the required core, optional wings, melee plus ranged, and Inn-room plan. M `notes/decisions-2026-10-14.md`, Tutorial items 2-10, confirms Rook, Echo, Common Explorer box, client buttons, and the hybrid order. M `docs/feature-queue.md:1225-1238` gives the level ladder; M P371 supplies the later graduation/Young decision and provisional skip default.

The page leaves opening/order, incomplete lessons, weapon choice versus both combat styles, pet scope/terminology, old reward/Young wording, the provisional skip policy, unintegrated level/pet progression, dungeon Young death destination, and built-versus-placed status in its Contradictions list. It changes none of those decisions or source records.

P371's review flags a disabled-tutorial escape gap and transport/pet ordering. These are review findings, not reproduced by P391, and are not turned into player instructions. The unimplemented graduation picker reissue suggested by its error message is likewise not presented as a working recovery action. No code fix belongs to this draft task.

## Verification and limits

No tests added, changed, or run. Lane tests: none, per prompt. Existing tests were inspected as source, including their relevant assertions:

- `server/tests/Misc/TutorialVerification.cs:111`, `:139`, `:171`, `:193`, `:225`, `:258`: persistence, two confirmations/remedial, account scope, vision/Young, creature engagement, and core/graduation boxes.
- `server/tests/Tutorial/GraduationLoopVerification.cs:71`, `:114`, `:157`, `:165`, `:181`, `:215`, `:238`, `:273`: saved first loop, unchanged skills/Young, later-character waiver, movement/spells/boats, Rootdeep, both skip settings, and ladder examples.
- `server/tests/Tutorial/TutorialFarmVerification.cs:113`, `:205`, `:272`: placement guards, full farm lesson, and no second graduation pet after taking one at the farm.
- `server/tests/Regions/RootdeepVaultVerification.cs:161`, `:207`, `:280`: trainee/pet entry, credited crawlway, graduate refusal and login eviction.
- `server/tests/Items/Traps/DeployableTrapsVerification.cs:560`: nets on Stacks entry and a netted rat completing the lesson.

No running-world settings, NPC placement, map/client installation, client walk, or deployment was verified. No new claim of a full playable tutorial, XP levels, skill resets, Inn rooms, or working evo owner-loop integration is made. Numbers on the page come from enumerated core entries or explicit source defaults/decisions. No duration estimate is promised.

## Final editorial and repository checks

- Reviewed the completed page against the requested topic list and both model guides. The core and wing tables distinguish previews from working activities; the level ladder, Inn room, full trials, and squire remain explicitly (planned). The later-character login paragraph follows `ClusterFTutorial.cs:64-78`, independently of the normal graduation rewards.
- Read the player page for staff commands, exploits, and hidden-achievement spoilers. None are included. The tutorial achievements named on the page are public definitions at `ClusterFAchievements.cs:1162-1177`. Source paths have no line numbers on the player page; evidence citations stay in this note.
- Checked the page's relative Markdown links: all resolve. It has no em dashes or trailing whitespace. Sources and Contradictions are the final sections. Checked the numeric claims against the source defaults and the station-key inventory above; no timing estimate or unsettled housing amount is invented.
- Both repositories pass `git diff --check`. Also checked each untracked deliverable with `git diff --no-index --check -- NUL <file>` so the new files themselves received whitespace review. Both deliverables are below 5 MB.
- Ran the existing `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies. Its report completed and reported setup 7/7 with no stale migrations subfolder. Captured its `progress.json` write in memory because that script writes the snapshot even in dry-run mode. No README, generated report, dashboard, or other file was changed for this documentation task. The reporter's inventory is not a claim about playable content.
- Windows PowerShell version checked as 5.1. No PowerShell test scripts, new tests, lane tests, build, or client session were run. Existing test assertions were inspected, as recorded above.
- Final scope: only this note and `notes/wiki-drafts/new-haven-start.md` are pending in shard-migration; the code work copy is clean. No deployment or publication. Stop-request checks during the work were absent.

P391 DONE
