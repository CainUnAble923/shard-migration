# cc-P145: TazUO Legion combat script, phase 1 (melee core and item rater)

2026-10-18. Fable. Prompt: `D:\UO\cc-prompts\cc-P145-combat-script.md`. Built, not committed; nothing deployed. The
scripts are in the Legion scripts repo (`D:\UO\sl-scripts`, P144), the one server change is in `D:\ShatteredLegacy`,
the design doc and this note in `shard-migration`.

## Headlines

- **The design doc is `notes/design-combat-script.md`** (for `docs\design\`): the files and why they are top-level
  modules, the two modes and four hotkeys, the state loop and tick priority, the targeting rules, survival, the melee
  module and the stance hook interface, the item rater (property table, scoring with headroom, compare mode, tiers,
  unravel against the account's known imbues, Suggest), and the later phases (archer, mage, tamer, Bushido, Chivalry,
  Necromancy stances, skill training, looter) as modules that plug into the same loop.
- **`SL_Combat.py` plus seven `SL_Combat_*.py` modules in `D:\UO\sl-scripts`** (2,287 lines of Python, counted with
  `wc -l`). Entry, settings (per character, JSON in a `Char` persistent var), core (Idle, Engage, Heal, Recover, Loot;
  stay alive, companions, fight, loot), targeting (reds, criminals and oranges always; grays only attacking you or a
  companion or on the hunt list; never blues, greens, invulnerables, own pets, companions, party; stick to the target
  unless attacked, then nearest or lowest HP), survival (bandage on threshold or poison with a cooldown bar sized from
  Dex, heal and cure and refresh potions, companion bandaging, "all guard me", panic: heal then recall, run or stand),
  melee (primary, secondary or alternating special by mana and cooldown; the stance hooks, empty), the rater, the gump
  (control window, Settings, Results, Profile editor with Suggest and Accept). Shared vars `SLC_*` every tick.
- **Every API call checked against the installed client's stub** (`ShatteredLegacy-2026.10.02.0840\app\tazuo\LegionScripts\API.py`,
  3,723 lines) by a script that lists each `API.x`, `API.Gumps.x` and `API.Player.x` the modules use and looks it up:
  none missing. The tazuo.org docs describe the newer build; the four things it adds (`CreateSlider`, `RequestHotkey`,
  `CreateEffect`, slider callbacks) are not used. `FindLayer` names and the Python search path (`LegionScripts` and the
  script's folder) were read in `D:\UO\tazuo-sl-build\src`.
- **Unravel on this shard is extraction into an Essence of a property**, not OSI's residue (`ArtificersImbueGump.cs:1267-1341`,
  `PropertyEssence.cs`), so the rater needs the account's *known imbue properties*, which the rank's formula books and
  the 140+ path decide. **New player command `[artificerrank`** (`server/customizations/Imbuing/ArtificerRankCommand.cs`,
  a `CommandCategory.Player` declaration, a row in `docker/uo/COMMANDS.md`) prints the rank, standing, count and the
  known properties by tier in `[Artificer]` lines of at most 180 characters, ending `[Artificer] end`; the script sends it
  on Refresh rank (and once at start when it has no cache), reads the journal, caches per character. Why not the
  `[guild` gump or a tooltip: design doc section 8.6.
- **Tests:** 4 server facts (`server/tests/Misc/ArtificerRankCommandVerification.cs`), 3 of them seen red against a stub
  `Lines` first; 33 CPython facts for the rater and targeting (`D:\UO\sl-scripts\tests\`, a fake `API`), 12 mutations
  run, 11 caught, one shown structurally uncatchable (table below). Full gate: see Tests.
- **Patch notes `2026.10.18.5`**, VERSION bumped: three player lines (Added), one Staff line.
- **Play-test items P145-1 to P145-11** (steps in `testing/playtest-steps.json`, Who in `testing/bot-triage.md`
  group P145): ten EYES, one BOT-PARTIAL (the command's lines).

## What changed

### D:\UO\sl-scripts (the scripts repo; uncommitted, see Deviations 1)

| File | Lines | What |
|---|---|---|
| `SL_Combat.py` (new) | 96 | Entry: header, `bind_hotkeys` :36 (unbinds old keys on a settings save), `on_stop` :63, the loop :82 (five errors in a row switch it off) |
| `SL_Combat_Settings.py` (new) | 208 | `SHARED` :16, `MELEE_STARTER` :30, `DEFAULTS` :48, `load` :109 (defaults merged under the saved JSON), `save` :132, profiles :149-167, the rank cache :192 |
| `SL_Combat_Core.py` (new) | 482 | `Core.tick` :209 (the priority), `_fight` :276 (leash, "cannot reach it" after 15 s without closing), `_recover` :306, `_loot` :327, `rate_item` :369 (slot from tiledata layer, the equipped piece via `FindLayer`), `rate_backpack` :423, `sort_item` :433, `refresh_rank` :458 |
| `SL_Combat_Targeting.py` (new) | 244 | `name_matches` :31, `companion_serials` :61 (Add companion list, friends, party) and `is_companion` :80 (`IsRenamable`), `note_damage` :115, `attacking_us` :141, `allowed` :162 (the rules), `choose` :216 |
| `SL_Combat_Survival.py` (new) | 234 | `bandage_seconds` :36, `tick_self` :133, `tick_companions` :151, `start_panic` :192, `tick_panic` :204 |
| `SL_Combat_Melee.py` (new) | 110 | `MeleeModule` :23, `specials` :63, the stance example :93 |
| `SL_Combat_Rater.py` (new) | 433 | `PROPERTIES` :30 (one line per property; the shard's custom ones :27), `parse_props` :118, `player_snapshot` :160, `score_props` :195, `reason_text` :227, `usable_essences` :240, `tier_for` :252, `rate` :266, `parse_rank_lines` :292, `request_rank` :325, `suggest` :351 |
| `SL_Combat_Gump.py` (new) | 480 | `open_main` :134, `refresh` :177, `open_settings` :213, `open_results` :321, `open_profile` :371, `_suggest` :451, `_accept_suggestion` :464 |
| `tests/fake_api.py`, `tests/test_rater.py`, `tests/test_targeting.py`, `tests/__init__.py` (new) | | 20 + 13 facts, CPython, one file per process |
| `README.md` | | The SL_Combat row, the tests paragraph, the module-cache note |

### D:\ShatteredLegacy

| File | What |
|---|---|
| `server/customizations/Imbuing/ArtificerRankCommand.cs` (new) | `[artificerrank`: `Lines` :60 (rank index and name from `ClusterFGuildSystem` with the character's guild data, standing, membership, `KnownTier` over `ImbueFamilies.AllKeys()`), `Chunk` :113 (180-character lines, the header repeated) |
| `server/tests/Misc/ArtificerRankCommandVerification.cs` (new) | 4 facts (below) |
| `docker/uo/COMMANDS.md` | The `[artificerrank` row under Player Commands |
| `CHANGELOG.md`, `VERSION` | `2026.10.18.5` |

### D:\UO\shard-migration

`notes/design-combat-script.md` (new), `testing/playtest-steps.json` (P145-1 to P145-11), `testing/bot-triage.md`
(`### P145`), this file.

## Tests

### Server: `docker/uo/build.sh --tests-only -t sl-modernuo:p145`

Two full runs, the builder rebuilt from the finished command each time (the builder stage is `sl-uo-builder:p145`;
`--tests-only` builds no shard image):

| Run | Total | Passed | Failed | Skipped | Result |
|---|---|---|---|---|---|
| 1 | 1,444 | 1,439 | 1 | 4 | `BUILD FAILED`: `LootBoxFanfareVerification.ContentsAreRolledAtEarnAndOpeningHandsOverExactlyThoseThenTheBoxIsGone`, not mine (below) |
| 2 | 1,444 | 1,440 | 0 | 4 | `Test Run Successful.`, exit 0 |

The four skipped are the suite's own standing skips (the same four in both runs). My four facts passed in both runs.
The one failure in run 1 is the known intermittent one (P100, P121 and P135 each saw it once): its output shows a
Mythril Box that rolled `60 x Bandage` twice, and `Assert.False(item.Deleted)` at line 212 fails because the second
stack merges into the first on hand-over and is deleted. Re-run three times by itself on the same builder: 3 of 3
green; then run 2 above, all green. Nothing in P145 touches loot boxes. Logged under bugs seen.

The four facts, red first: `ArtificerRankCommand.cs` was first written as a stub whose `Lines` returned only the end
line and whose `Chunk` returned nothing; the builder was built from that (`sl-uo-builder:p145`) and the filtered run
(`dotnet test ... --filter FullyQualifiedName~ArtificerRankCommandVerification`) gave **3 failed, 1 passed**:
`AFreshCharacterIsRankZeroNotAMemberAndKnowsTheFreePropertiesAtBasic`, `ChunkKeepsEveryLineUnderTheLimitAndEveryNameOnce`
and `AMemberAt5200WithHitChanceAtFullReadsRankTwoAndListsItOnTheFullLineOnly` red; `TheHandlerRunsForAPlayerWithoutThrowing`
green by construction (it guards the registration and the handler's cast, not the lines). Then the real `Lines` and
`Chunk`, and the gate above.

What they cover: a fresh character (no guild record) reads `rank 0 of 5`, `not a member`, every `free` ladder property
on a Basic line (Luck among them), no Refined or Full line, `end` last, no line over 180; a member at standing 5,200 with
Hit Chance Increase granted at Full reads `rank 2 of 5 (Artificer), standing 5,200`, the count one higher, Hit Chance
Increase on the Full line and on no other; sixty long names chunk into several lines all under 180 with the header
repeated and every name once in order, and no names give no lines; the handler runs for a player without throwing.

### Scripts: `python -B -m unittest tests/test_rater.py` (20 facts) and `tests/test_targeting.py` (13 facts), both OK

Each file installs a fake `API` (`tests/fake_api.py`: notoriety and persistent-var enums, a player with the attribute
totals, a world of mobiles, friends, party, journal, said messages) before importing the module, so they run in CPython
3.12 on this PC. The facts were written against the finished modules, so each was shown to catch a change by mutation
(`mutate_scripts.py` in the session scratchpad; one change at a time, restored after, `__pycache__` cleared between runs
because an equal-size mutation left a stale `.pyc` once):

| Mutation | Fact that went red |
|---|---|
| `MIN_HEADROOM` 0.15 to 0 | `test_a_property_at_cap_on_the_character_counts_for_fifteen_percent` |
| "undead" dropped from the super slayers | `test_a_sword_tooltip_parses_every_known_line_and_skips_the_rest`, `test_single_and_super_slayers_and_silver` |
| the Upgrade rule disabled | `test_upgrade_when_compare_is_on_and_it_beats_the_equipped_piece` |
| the rank answer accepted without its `end` line | `test_the_answer_is_parsed_once_the_end_line_arrives` |
| known-property lookup case-sensitive | `test_unravel_only_when_the_account_can_imbue_a_property_on_it`, `test_unravel_through_a_family_key` |
| compare mode not giving the equipped piece's total back | `test_compare_gives_the_equipped_pieces_contribution_back` |
| Suggest's HCI cap test off by one | `test_at_cap_drops_and_under_cap_raises_with_a_line_each` |
| `IsRenamable` no longer makes a companion | `test_companions_pets_friends_and_party_are_never_targets` (after the fact was strengthened: the pet in it is now a renamable *red*, since a renamable gray with nobody hurt was already refused by the gray rule) |
| hunt list matches whole names only | `test_whole_name_or_a_word_matches_case_insensitively`, `test_a_gray_on_the_hunt_list_is_a_target` |
| a gray out of war mode counts as attacking | `test_a_gray_in_war_mode_next_to_the_player_who_just_lost_hits_is_attacking` |
| the current target never kept | `test_sticks_to_the_current_target_while_nothing_attacks` |
| the "never" notoriety check removed | **not caught**: blues, greens and invulnerables then fall through the "always" and "gray" tests and are refused anyway. The check is a safety net on top of a whitelist, kept as written. |

Two facts failed on their first run against real mistakes of mine in the tests, not the code: the headroom fact used
HCI 40 of 45, where 5 of room against a 45 cap is under the 15 % floor (now 30 of 45, and a second assertion that 42
of 45 sits on the floor); and the `request_rank` fact filled the journal before the call, which `ClearJournal` then
emptied (the fake's `Msg` now answers like the server). Both were my expectations; the module was right.

What the script facts cover: a 17-line sword tooltip parsed to exactly its 13 known properties (slayer family, skill
bonus, elemental damage, a custom property, booleans, the mundane lines skipped); single, super and `silver` slayers;
every starter-profile name is a table name; a mundane item has none; the headroom rule at cap, under cap and on the
floor; compare mode's add-back; the three-part reason; zero and negative weights; each tier's rule, with compare on
and off and known lists with and without a family key; the rank parser (chunked lines, the `end` gate, a non-member)
and `request_rank` round trip; Suggest's cap, under-cap, caster and Necromancy decisions and its "nothing stood out"
line; hunt-list matching; each notoriety rule; the three ways a gray becomes a target; companions by list, friends,
party and renamable flag; dead and given-up mobiles; sticking to the target, re-picking by nearest or lowest HP when
attacked, replacing a dead target, the AFK origin range.

**Not tested here, by nature:** anything that needs the client (the gumps, hotkeys, pathfinding, bandaging, the real
tooltip text, `[artificerrank` through a real journal). That is the play-test list; the API names are checked, the
behaviour is not until Chase runs it.

## Play-test items added

P145-1 to P145-11 under **To try it** in For Chase (steps in `testing/playtest-steps.json`, Who in
`testing/bot-triage.md`). Who, Where, Do, Pass:

| Item | Who | Where | Do | Pass |
|---|---|---|---|---|
| P145-1 | Chase | TazUO, test shard | Play SL_Combat.py; CTRL+F9 twice | Eight files listed; the window opens; ON then off |
| P145-2 | Chase | A red or orange spawn, Assist | On; walk up; drop under 70% | Attacks and highlights it, toggles the special, bandages with a cooldown bar, war mode off when it dies |
| P145-3 | Chase | Animals and a gray | Stand by a horse; let a gray attack; hunt list "ettin" | Idle grays left alone; an attacking gray and a hunt-list gray fought; blues and greens never |
| P145-4 | Chase | With the evo pet or squire | Add companion; fight; let both drop | Never targeted; bandaged under 60%; "all guard me" under 50% |
| P145-5 | Chase | A spawn, AFK | Switch to AFK; watch; pull a target past 20 tiles | Seeks within 12, fights, loots, recovers, returns; the far target is given up |
| P145-6 | Chase | Mid-fight | Panic action recall and a rune; CTRL+F12 | Stops, drops war mode, heals, recalls; run and heal variants |
| P145-7 | Chase | A magic-loot kill, Loot helper on | Kill; open Results; Compare off, Rate backpack | One `[Rater]` line per item with tier, score, delta and reasons; Results lists them; no delta with Compare off |
| P145-8 | Bot, then Chase | Test shard | `[artificerrank`; Refresh rank | The `[Artificer]` lines (bot); the rank label and an un-imbuable item being Sell not Unravel (Chase) |
| P145-9 | Chase | The window | Profile: edit, Save as; Suggest; Accept | New profile selected; notes one line per decision; "Suggested <date>" saved |
| P145-10 | Chase | Two characters | Change, Save, relog; another character | Settings back for the first; defaults for the second |
| P145-11 | Chase | Three bags | Set bags; Auto-sort on; rate | Items queued to their tier's bag; "no Sell bag set" when unset |

## Not finished, and bugs seen

- **Not run in a client.** No TazUO session was available to this run; the scripts are checked by name against the
  installed API stub and by the CPython facts. The first real run will find what only the client shows (gump layout,
  tooltip wording, timing). Expect small fixes.
- **The scripts repo is not committed** (Deviations 1).
- **`[artificerrank` is on the test shard only once that image is deployed**; a client talking to a server without it
  gets no answer and the rater says so ("no answer to [artificerrank"); Unravel then never fires (the known list is
  empty), everything else works.
- **The task list:** the hand-off asked for one task per main step; this session had no task-list tool, so progress
  went to the chat updates instead.
- **Bug seen, not fixed, not mine: `LootBoxFanfareVerification.ContentsAreRolledAtEarnAndOpeningHandsOverExactlyThoseThenTheBoxIsGone`
  fails when the general pool rolls the same stackable twice** (run 1 above: `60 x Bandage, Studded Chest, 60 x Bandage`;
  the second stack merges into the first in the pack, `Deleted` is true, line 212). Ours to fix, in the test or the roller:
  either the fact should accept a merged stack (count the amount handed over, not the item objects), or
  `LootBoxRoller` should not roll one stackable twice for a box. P100, P121 and P135 saw the same flake once each; this
  is the first note that says why.

## Deviations and decisions for Chase

1. **The scripts repo needs your commit.** `Commit-ShardWork.ps1` takes `D:\UO\sl-scripts` as a third repo only on a
   PC with `%LOCALAPPDATA%\ShatteredLegacy\legion-scripts.json`, which Set up scripts repo writes (P144 For Chase step
   3, not yet run here, so `git status` in `D:\UO\sl-scripts` shows the nine new files and the README untracked). Run Set
   up scripts repo (or commit there by hand), then Publish to dev and Promote to official to reach players. Until then
   the dry run below shows no `scripts` row, as P144's did.
2. **Eight top-level files, not a folder.** P144's publisher ships top-level `*.py` only and its manifest check refuses
   paths, so the seven modules sit beside the entry script with the `SL_Combat_` prefix; TazUO lists them all, and each
   says "run SL_Combat.py instead" if played alone. One subfolder would be tidier; that is a P144 follow-up (teach
   `Get-LegionSourceFiles` and the manifest one level), not a P145 change. Say if you want it queued.
3. **Rank through a command, not the `[guild` gump.** The prompt offered tooltip, gump or command: nothing on the player
   carries the rank; the Guild Directory and the Artificers' Guildmaster gump show it but not the known properties, and
   the rater needs the properties (an essence is only useful for a property you can imbue). The command prints both.
   It is a plain Player command (`CommandCategory.Player`), declared like `[stats`; it changes nothing.
4. **A non-member still gets the free properties at Basic**, because `KnownTier` says a free property is Basic for every
   account, which is what the Artificers' table lets them imbue; the first line says "not a member" so the script and
   the player know.
5. **Companions are the union of** your Add companion list, TazUO's friends list, the party, and any mobile the client
   flags renamable (TazUO's own "own followers" test). The squire does not exist yet (`ClusterFTutorial.cs:12`), so it is
   covered by the renamable rule and the list, untested.
6. **"Attacking the player" is a client-side guess** (a gray in war mode within 2 tiles of whoever just lost hits, in
   the last 3 s, or a gray you attacked yourself). The API has no "who hit me". It errs on the side of not attacking.
7. **Enabled is remembered.** Running the script after a relog starts it in the state you left it (the settings are per
   character and "enabled" is one of them). Say if it should always start off.
8. **The installed client's API stub is the reference**, not tazuo.org, so the script runs on the package players have
   (`2026.10.02.0840`), and the newer build's additions are left alone.
9. **The starter profile's weights, the thresholds and the hotkeys are first guesses** (design doc section 12).
10. **Counts:** 2,287 script lines and 33 script facts counted with `wc -l` and unittest's own totals; the stub's 3,723
    lines with `wc -l`.

## For Chase

**Deploy:**

1. Deploy the image to the test shard (`sl-modernuo:p145` passed the gate; or build again from the commit) so
   `[artificerrank` answers.
2. Set up scripts repo on the tower (P144 For Chase step 3), then commit `D:\UO\sl-scripts` (Commit tab), Publish to
   dev, and when happy Promote to official.
3. Promote `notes/design-combat-script.md` to `docs/design/` and mark it in progress in `docs/feature-queue.md`.

To try it:

1. **Start it:** in TazUO on the test shard open the Legion scripts list and play SL_Combat.py; press CTRL+F9 twice:
   SL_Combat.py and seven SL_Combat_* modules are listed, the SL_Combat window opens with status, On, Assist, Pause,
   PANIC, the three checkboxes and the Profile dropdown, it says "[SL_Combat] ready", and CTRL+F9 says ON then off with
   the first button following.
2. **Assist mode on a red:** click On, walk up to a brigand or orc and let your hits fall under 70%: it enters war
   mode and attacks (red highlight, "Fighting ..." over your head), toggles the weapon special when mana allows, bandages
   you under 70% with a "Bandaging" cooldown bar, and drops war mode when it dies.
3. **No animal slaughter:** stand beside a horse or cow with it On, then let a gray attack you, then put "ettin" in the
   hunt list (Settings, Save) and stand near one: an idle gray is never attacked, an attacking gray is fought, a
   hunt-list gray is fought, blues and greens never.
4. **Companions:** Add companion and target your evo pet, then fight until it drops under 60% and you under 50%: the pet
   is never targeted, the script walks to it and bandages it with a cooldown bar, and you say "all guard me" once.
5. **AFK mode:** click Assist to switch to AFK (the anchor is set where you stand), step back and watch, then pull a
   target more than 20 tiles away: it seeks within 12 tiles of the anchor, pathfinds, fights, loots, recovers to 80%
   hits and 60% stamina, walks back; the far target is given up with "Too far from the anchor".
6. **Panic:** in Settings set panic action recall, target a Recall rune, Save, then press CTRL+F12 mid-fight: it stops
   attacking, drops war mode, says PANIC, bandages and drinks as needed, and recalls once you are over 70%; with "run" it
   walks to the anchor, with "heal" it stands and heals.
7. **The rater:** kill something that drops magic loot with Loot helper on, open Results, then toggle Compare off and
   click Rate backpack: each new magic item gets one "[Rater] name: tier score (+/-x vs slot). top three properties"
   line, Results lists them newest first with picture, tier colour and reason, and with Compare off there is no delta
   and Keep goes by score alone.
8. **The rank:** type `[artificerrank`, then click Refresh rank: the command prints "[Artificer] rank N of 5 (rank),
   standing X, Y properties known", Basic lines with Luck among them, Refined and Full lines where you know more, and
   "[Artificer] end"; the window's rank label shows the same rank and count, and an item whose only property you cannot
   imbue is Sell, not Unravel.
9. **Profiles and Suggest:** click Profile, set Hit Chance Increase to 20, Save as "Mine", then Suggest and Accept: the
   dropdown gains and selects "Mine"; Suggest fills the boxes and the notes with one plain line per decision ("Hit
   Chance is 25 of 45: ..."); Accept saves "Suggested <date>" and selects it.
10. **Per character:** change a threshold and the mode, Save, stop the script, relog and run it again, then run it on
    another character: the first gets its settings back, the second starts from the defaults.
11. **Auto-sort:** target a Keep, an Unravel and a Sell bag in Settings, tick Auto-sort, then Rate backpack: each rated
    item is queued into its tier's bag (Upgrade to Keep), Results shows "[to the Keep bag]", and with a bag unset the
    item stays with "no Sell bag set".

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after everything above:

```
Repo Result
---- ------
code dry run
docs dry run
```

Code: `CHANGELOG.md`, `VERSION`, `docker/uo/COMMANDS.md`, the command and its test. Docs: the two notes, the two play-test
files, and `testing/SUMMARY.md` and `testing/play-tests.json` (the play-test mirror's machine output, refreshed from
Haven by the script itself). No `scripts` row: this PC has no `legion-scripts.json` yet (Deviations 1), so the nine new
files and the README change in `D:\UO\sl-scripts` wait for Chase's commit there. No file over 5 MB anywhere (largest new
file: `SL_Combat_Core.py`, 17,289 bytes). Scratch (the builder logs, the mutation script, `__pycache__`) is in the session
scratchpad or removed; both repos' pending lists above are exactly the files in What changed.

P145 DONE
