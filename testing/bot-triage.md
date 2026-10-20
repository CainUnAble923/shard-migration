# Open play tests: who tests each one (cc-P91, re-sorted cc-P115)

Every open or blocked item in `testing/play-tests.json`, in exactly one bucket (219 on 2026-10-15; cc-P137 sorted the 40 that had none on 2026-10-17, 268 in all).
**This file is the single source of each item's Who.** The play-test page reads it (through `tools/playwho.py`, merged
into `/api/items` when it is read; nothing is written back), and so does the overnight bot's plan
(`uobot/tonight.py`: BOT and BOT-PARTIAL are "bot-checkable"). The steps for each item are beside it in
`testing/playtest-steps.json`. The importer (`tools/playtests.py`) never writes either file. A new item that is not in
this file yet shows "Who: not sorted yet" on the page until it is added here.

The bot (`D:\ShatteredLegacy\tools\playtest-bot`) is a headless UO protocol client on a SCRATCH copy of the test world
(127.0.0.1:2595, client 7.0.117.0), with an admin and player accounts of its own. **It never marks a result**: a check
is evidence, and Chase marks on the play-test page.

| Bucket | Who on the page | Meaning |
|---|---|---|
| **BOT** | Bot | the pass condition is something the server sends (a message, a gump's text or buttons, an item in a pack, a skill value, a mobile at a place, a refusal, staying connected) |
| **BOT-PARTIAL** | Bot, then you | the bot can settle the mechanics, but part of the pass condition is how it looks; the reason says which half is Chase's |
| **EYES** | You | art, hues, rendering, paperdolls, animation, "reads right", "feels fast enough": in the game or on screen |
| **DEPLOY** | You | needs a deploy, the Shard Console, the player package, Windows Sandbox, a web page, a router/DNS step, or live (retired since 2026-10-14); the reason says which |
| **DECISION** | You decide | Chase picks something |
| **CC** | CC | Claude Code can settle it with no game client and no eyes: a file, a log, a test suite, a script's output, a page's HTML, a database row, git history. Not run by cc-P115; queued as CC verification prompts |

Where a check depends on a context-menu label, a tooltip line or a gump colour, the bot sees the server's cliloc number,
property text or layout code, not what the client draws, so those items are BOT-PARTIAL.

**Code under test:** HEAD. cc-P95 fixed the boot crash (D89); the 2026-10-15 01:30 run tested commit 68631cb. The old
note "items from P82 on cannot be checked" no longer applies.

## Counts

The page's header counts each Who live (`/api/items`, `who.counts`). This file no longer keeps a Counts table: every
result and every new prompt's items changed it, so it was always out of date (cc-P137). On 2026-10-17, after cc-P137
sorted the 40 items that had none: BOT 82, BOT-PARTIAL 23, EYES 24, DEPLOY 53, DECISION 14, CC 72; 268 in all.

## Where a new prompt's items are sorted (cc-P137)

**The prompt that writes the items sorts them**, before it writes DONE: one row per item under its own `### P<nn>`
group here (`| P<nn>-<k> | BUCKET | reason |`, BUCKET one of the six above, never anything else), and its steps in
`testing/playtest-steps.json`. The item numbers are the order of the list under the notes' **For Chase** heading, as
`tools/playtests.py` reads it: put a line containing "To try it" (or "in game", "checklist") right before that list,
because any other paragraph there makes the importer skip the whole list and leave one "checklist not parsed"
placeholder instead (P123 and P127 to P130 lost their items that way). Run
`python -m unittest tools/tests/test_play_who.py`: `RealFiles` fails while any open item has no Who, while any row
names a bucket the page does not know, or while any row's steps have the wrong shape. Anything that still slips
through shows on the status page's **Needs overseer review** box ("play-test items not sorted"), so the overseer sorts it.

## Checks built (cc-P91)

18 play-test ids, plus two of the bot's own:
- `CREATE`: character creation for every race and sex, through the real packet;
- `D41`: the Guild Directory regression.

Ids with a check: P56-4, P56-6, P58-0, P61-3, P61-5, P62-1, P62-7, P64-1, P64-2, P64-3, P64-4, P64-5, P64-6, P66-7, P71-7, T-039, T-046, T-047.
cc-P119 added one more: P119-1 (`p119_1` in `uobot/checks.py`).
The other BOT and BOT-PARTIAL items are the backlog for the next nights: the sketches at the end say how each could be
checked.

## Items by prompt group


### client-test-queue

| id | bucket | reason |
|---|---|---|
| T-001 | BOT-PARTIAL | Bot: the craft gump layout carries the MAKE X entry text/cliloc; Chase: the text actually draws in the client (the original bug was a drawing one) |
| T-002 | BOT | Quest gump, skill updates and the quest-complete message are all server-sent; the test shard's 5x multiplier makes it a smoke test only |
| T-003 | BOT | Craft gargish plate (Blacksmithy) and cloth (Tailoring) on a gargoyle, equip: item in pack then worn layer. Row is BLOCKED; the bot result says whether it still is |
| T-004 | BOT | Walk the four craft gumps, read each new entry's required skill from its detail page; assert not 0 and not 120 |
| T-005 | BOT | Scan every craft gump page for WoodPulp / WorkableGlass entries; assert none |
| T-006 | BOT | Admin runs [GenerateSpawners, [go to Ter Mur, Abyss, Underworld; count mobiles in range |
| T-007 | BOT | Run the two generators, visit both, count distinct mobile types seen against 41 and 37 |
| T-008 | DECISION | Pass condition is a choice: whether Q-064's forty Eodon lines get written; Chase looks at what is there |
| T-010 | BOT | Find the gargoyle alchemist, save, restart the scratch shard, re-read its name/title and [props type |
| T-011 | DEPLOY | Website panel (homepage) reads live's status.json and live is retired; the publisher half can be checked now on the test shard's status.json |
| T-012 | EYES | Paperdoll rendering of a petrified clone |
| T-013 | BOT-PARTIAL | Bot: the chest is locked and trapped (lock message, trap fires); Chase: it renders as a chest |
| T-023 | BOT | Thief steals LightInTheVoid; item lands in pack or the refusal text says why (weight over 10) |
| T-024 | BOT | [go Labyrinth, find a Miasma mobile near its spawner, kill it, corpse appears |
| T-025 | BOT | Same as T-024 for Lady Lissith in Twisted Weald |
| T-026 | BOT | [GenStealArties, wait 15 min, go TerMur 1134 1204 7, see HalfEatenSupperArtifact, steal succeeds |
| T-027 | BOT | [add TreasureMapChest 5 several times, list contents; count orc/tribal masks and read their properties |
| T-028 | DEPLOY | Shard Console stop/start and docker logs; live is retired, so run the same D36 check on the test shard (same image, Test shard tab) |
| T-031 | BOT | Measure skill gain per use with and without the multiplier; ClusterFSkillGain bonus gains still appear |
| T-032 | CC | Pass is one log line at startup; CC can start a throwaway shard with testCenter on and an internal 2593 listener and read its log |
| T-039 | BOT-PARTIAL | Bot: first-login welcome names the board and the board is in range of the start point; Chase: a new player can actually find it by eye |
| T-041 | BOT | Join a guild, list pack: the creation items for the guild skills are there; joining the Smiths keeps ingots |
| T-042 | BOT | Ask for the starter item twice: item once, quest marked done, second ask gives nothing |
| T-044 | BOT | Gargoyle Tailoring gump lists the 8 gargish cloth armor pieces and they craft; garments absent |
| T-045 | BOT | Second character on a joined account: guild gump says not a member; joining hands its own items |
| T-046 | BOT-PARTIAL | Bot: the stone and [ResetMyAccount open the same gump (passed); Chase: press each scope, which the bot will not (it would wipe its own characters) |
| T-047 | BOT | Young countdown text (days and hours vs 336 h); "I want to grow up!" brings the confirm gump |
| T-048 | BOT-PARTIAL | Bot: Liaison and Survey Archivist positions and the tent pieces' coordinates; Chase: the two tents look right and the NPCs stand at the openings |
| T-014 | DEPLOY | Website panel shows live's status.json; live is retired (cc-P108), so it waits for the new live |
| T-015 | DEPLOY | Website heartbeat reads live's status.json; live is retired, so it waits for the new live |

### P56

| id | bucket | reason |
|---|---|---|
| P56-1 | BOT | Member hands in a deed; system message "Society of Smiths: +n standing, +52 Smithing Seals banked." and the balance grows by that |
| P56-2 | BOT | Non-member hands a deed to a town Blacksmith; gold lands in the bank and the bank-points gump opens (cc-P122, OSI's 2016 rules; was gold and an item in pack) |
| P56-3 | BOT | Ask mode: the hand-in gump's Bank button text carries the new Seal figure |
| P56-4 | BOT | Smelt Platinum at 112.4: refusal message, ore stays; at 112.5 smelts about half the time |
| P56-5 | BOT | Satchel smelt at 112.4: "left unsmelted"; at 112.5 ingots appear in the satchel |
| P56-6 | BOT | Valorite refused at 98.9, smelts at 99; iron smelts at any skill |
| P56-7 | BOT-PARTIAL | Bot: the context-menu entries' cliloc ids and that each opens its gump; Chase: the labels show as words (custom clilocs) |

### P57

| id | bucket | reason |
|---|---|---|
| P57-1 | BOT | Seal catalog gump text: Sturdy Shovel 150, Mining Gloves +5 1,800, Salvage Bag 750, Valorite runic 45,000; deed still +52 |
| P57-2 | BOT | A Celestial exceptional 20 deed banks about 1,466 Seals (message) |
| P57-3 | BOT | Mine a Platinum vein at 112.4 (iron only) and 112.5 (Platinum about half); count ore types in pack |
| P57-4 | BOT-PARTIAL | Bot: Bulk Order Info opens the Small/Large gump with the Completed orders line and no deed; Chase: the gump is opaque and the line fits |
| P57-5 | BOT-PARTIAL | Bot: context menu cliloc ids for Breed, Smelt Ore, Metal Familiarity and the panel opens; Chase: the words draw in our client, and a client without overrides shows a blank row |
| P57-6 | EYES | No row overlaps, tabs on two rows, opaque, line breaks: layout |
| P57-7 | BOT | Steal from a 150-ingot pile at Stealing 150; amount moved to pack at most 100 |

### P58

| id | bucket | reason |
|---|---|---|
| P58-0 | BOT-PARTIAL | Bot: [version on a player has the 2026.10.02 to 10.05 sections and no Staff lines (passed); Chase: the patch-note wording reads right |

### P59

| id | bucket | reason |
|---|---|---|
| P59-0 | CC | Research notes whose 8 decisions Chase already answered on 2026-10-05 (f35 hand-off) and P65 built; CC confirms from files |

### P60

| id | bucket | reason |
|---|---|---|
| P60-1 | CC | The Commit tab's place is asserted by the console's form fact, and shard-console.log shows Chase has used commit.run from it 14 times since 2026-10-05 |
| P60-2 | CC | Five real Preview commit runs are logged (scripts\shard-console-output\*_commit.preview_repos.log) with the PREVIEW banner, WARNING lines and the -DryRun table; -NoExit is a fact |
| P60-3 | CC | The DRY RUN dialog title, BEFORE YOU TYPE preface and the doubled-quote -Message line are each held by console facts that run a real dry child |
| P60-4 | CC | The in-flight guard (notes not DONE, files changed in 5 min) refusing with names and no dialog is fully unit-tested on facts |
| P60-5 | CC | Already done for real: 14 commit.run logs in scripts\shard-console-output each end with the script's table, 'pushed' (or 'clean') for code and docs |
| P60-6 | CC | The SYSTEM refusal is a plan rule tested by P60_SystemRefusesCommitRunAndThePreviewSaysSo; a real SYSTEM shell would only re-test WindowsIdentity.IsSystem |

### P61

| id | bucket | reason |
|---|---|---|
| P61-1 | BOT | Skill gains per metal and craft success counts are server state the bot reads |
| P61-2 | BOT | Order deed item names at 150 with 'Orders that still teach me' on are gump/OPL text |
| P61-3 | BOT | Achievements gump text: Earned line, no 'Progress: 9/1', unearned rows keep progress |
| P61-4 | BOT-PARTIAL | Bot: deed gump and tooltip line 'All items must be made with Frost ingots.' (small and large); Chase: the blank line in a client started without the launcher |
| P61-5 | BOT | [version history holds 2026.10.05.2 with its four lines (current version is newer) |

### P62

| id | bucket | reason |
|---|---|---|
| P62-1 | BOT | Female equips KitsuneEarsTail: the item is on her worn layer |
| P62-2 | EYES | Paperdoll placement of the ears and tail is art |
| P62-3 | EYES | Walk animation sync is client rendering |
| P62-4 | EYES | Mirrored walk animation is client rendering |
| P62-5 | EYES | What shows in the other directions, standing and running is client rendering |
| P62-6 | EYES | Whether it reads as fox ears and a tail is a judgment by eye |
| P62-7 | BOT | Male equips it: 'Only females can wear this.' and the item stays in the pack |
| P62-8 | BOT | After a restart the female still has the item on its layer: server state |

### P63

| id | bucket | reason |
|---|---|---|
| P63-1 | CC | Blank notes refusal and the dirty-tree file list are console facts; the tab is in the form fact; Chase has used the tab (package.build 2026-10-06) |
| P63-2 | CC | Done for real: 20261006-063853_package.build_package.log shows the build, GATE 4, 6 and 5 on the new zip; the dry-run quote doubling is a fact |
| P63-3 | CC | Done for real: 2026-10-05 16:07:09 publish answered no ('Nothing done.', exit 3), 16:07:25 PUBLISHED; the no-version.json refusal and PUBLIC preface are facts |
| P63-4 | CC | Chase answered the 'Type yes' prompt in the real window three times (no, then yes twice), so it was visible; the logs record each answer's outcome |
| P63-5 | DEPLOY | Shard Console, Test shard tab, Deploy built image: never run for real (shard-console.log has no test.deploy); it retags latest and restarts the test shard |
| P63-6 | CC | Picking the image latest already is refuses before any phrase: asserted by a console fact |

### P64

| id | bucket | reason |
|---|---|---|
| P64-1 | BOT | Fresh account login: bulletin gump title, new lines, All patch notes button, no wiki button |
| P64-2 | BOT | Press All patch notes: history gump arrives; a relog shows no bulletin |
| P64-3 | BOT-PARTIAL | Bot: [version text and '(you are here)' on page 1; Chase: the current entry shows gold |
| P64-4 | BOT | Next to 'Page N of N', last page ends with 2026.10.01, Previous returns |
| P64-5 | BOT-PARTIAL | Bot: the 2026.10.05.2 line ends 'The chance to make the item is unchanged.'; Chase: it wraps onto four rows in the client |
| P64-6 | BOT-PARTIAL | Bot: 'Staff (players do not see this list)' present for admin, absent for player; Chase: shown lavender |

### P66

| id | bucket | reason |
|---|---|---|
| P66-1 | BOT | Hide 5 tiles from a fight: "You can't seem to hide right now."; at 9+ works; Hiding base passes 100 |
| P66-2 | BOT | Detect Hidden: no gain on an empty spot, reveals a hidden second character, "[trapped]" on a trapped chest, 15-tile hider not found |
| P66-3 | BOT | Repeated steals from a monster at 127.5 with +20: caught roughly 1 in 5 (count of caught messages) |
| P66-4 | BOT | Peacemaking success rate at Musicianship 200 vs 120 the same; Musicianship base rises past 120 |
| P66-5 | BOT-PARTIAL | Bot: share of incoming swings that cost HP at Parry 200 vs 120; Chase: the blocks as seen in a fight (a parry sends no server message) |
| P66-6 | BOT | Tactics base rises toward 200 with a +15 Tactics item worn |
| P66-7 | BOT | [ClusterFSkillGain output includes the rate and "past stock ceilings on" |

### P67

| id | bucket | reason |
|---|---|---|
| P67-1 | BOT | Carpentry gains in Frostbark, stops at 155, Shadowbark gains; at 99.9 Ironwood says "You cannot work this strange and unusual wood." |
| P67-2 | BOT | Fletching 150 with Frostbark logs: bows gain, kindling never |
| P67-3 | BOT | Tinkering gump material list Platinum..Celestial; scissors gain at 150, stop at 162.5 |
| P67-4 | BOT | Blacksmithy 180 plus a +10 item: base caps at 187.5 |
| P67-5 | BOT | Orders at 150 with the toggle on are all Frost post-Valorite; off: Platinum, Toxic, Blaze reappear |
| P67-6 | BOT | Explosion trap HP loss at Tinkering 200 vs 120; Remove Trap failure rate |
| P67-7 | BOT | Axe damage at Lumberjacking 148 vs 100 (target HP via [props), statistical |

### P68

| id | bucket | reason |
|---|---|---|
| P68-1 | DEPLOY | Shard Console, Commit tab: the live countdown and the Force box are a hand check (built and tested only with stubs) |
| P68-2 | DEPLOY | Shard Console, Player package tab: the Check selected button and its window are a hand check |

### P71

| id | bucket | reason |
|---|---|---|
| P71-1 | BOT | Twenty Nerve Strikes at Bushido 200 vs 120; count paralyze messages |
| P71-2 | BOT | Stable 23 pets at Taming/Lore/Vet 200, the 24th refused |
| P71-3 | BOT | Fire Horn damage at 200 vs 120 (target HP via [props), about +10% |
| P71-4 | BOT | Count steps until revealed at Stealth 200 (about 34) and 120 (about 24) |
| P71-5 | BOT | Bandage heal amounts at Healing/Anatomy 200 within 54 to 90 |
| P71-6 | BOT | Harness edits the scratch copy's stepsAt200 to 30 and restarts; steps become 30 (scratch config only) |
| P71-7 | BOT | [version history holds 2026.10.10 with five lines (current version is newer) |

### P72

| id | bucket | reason |
|---|---|---|
| P72-0 | DECISION | Leveling gear research (plan only): 10 decisions (port code or design, how an item becomes levelable, XP rules, resets, trade); nothing built to test |

### P73

| id | bucket | reason |
|---|---|---|
| P73-1 | DEPLOY | Shard Console run from Chase's own Windows login (the wipe is refused as SYSTEM); step 1 of the real test-account wipe |
| P73-2 | CC | Precondition only: the test shard must run an image with P73's wipe; its log proves it |
| P73-3 | DEPLOY | Shard Console, Test shard tab: Wipe test accounts (keep world). Wipes Ringo, Eve, Garg and Elf Female, so Chase picks the moment |
| P73-4 | DEPLOY | Shard Console wipe, first dialog: counts shown and the new admin name typed |
| P73-5 | DEPLOY | Shard Console wipe, second dialog: the confirmation phrase |
| P73-6 | DEPLOY | Shard Console wipe window: password, then stop, back up Saves, start, DONE line |
| P73-7 | DEPLOY | After the real wipe: log in with the four test shortcuts (admin password rehash, new characters) |

### P74

| id | bucket | reason |
|---|---|---|
| P74-1 | DEPLOY | Shard Console launch; cc-P99's Golem replaced cc-autopilot, so P74's tile and tab are now GOLEM / Golem but the check still applies |
| P74-2 | DEPLOY | Shard Console GOLEM tile and Golem tab (P74's AUTOPILOT, renamed by cc-P99); the Golem is active since 2026-10-14 |
| P74-3 | DEPLOY | Shard Console, Golem tab: Send test email (now the Golem's Send-TestEmail.ps1); Chase checks his inbox |

### P65

| id | bucket | reason |
|---|---|---|
| P65-0 | BOT-PARTIAL | Bot: [EvoPet give/xp/loops/bond/info walk (Echo lines, pick gump, body ids), reset stone, stable/claim, death/res, doors; Chase: the animation table, plus the 10 section-9 decisions |

### P69

| id | bucket | reason |
|---|---|---|
| P69-1 | BOT | Registrar errand: refused at Iron, 49 ore refused, 50 ore + 25 ingots accepted, bonded Compact mule (hue number), "You have your mule", "Replace my mule" |
| P69-2 | BOT-PARTIAL | Bot: upgrade to Bronzeback, name, hue number, hits, pack size, contents and bond kept; Chase: each tier's hue looks right on the body |
| P69-3 | BOT | Breed two mules, restart the scratch shard (or [props DeliverAt), foal deed arrives in bank |
| P69-4 | BOT | Foal deed tooltip lines: sex, tier 1, generation, family line, qualities, bloodline |
| P69-5 | BOT | Trade a foal deed between the bot's two characters; the receiver's mule is theirs with the foal's genes ([props) |
| P69-6 | BOT | Existing mules on the test shard world: Shadowhide, 1 slot, owner's follower count |

### P70

| id | bucket | reason |
|---|---|---|
| P70-1 | BOT | Tinkers' Union hall gump: buy Clockwork Load Harness I schematic with scrip and vouchers |
| P70-2 | BOT | Mule Modules craft group: crafts with materials, gump refuses without |
| P70-3 | BOT | Drop module on mule (tooltip lists it), Options > Remove returns it to pack as tier I |
| P70-4 | BOT | [add MuleModule TimberRack 3 on a tier 1 mule: refused, still in pack |
| P70-5 | BOT | Tier II craft consumes the tier I only on success |
| P70-6 | BOT | Trailwise Tack III: follower count drops by one, returns on removal |
| P70-7 | BOT | Trailwise II homing: after a gate the mule appears beside the bot within seconds; "all come" works |
| P70-8 | BOT | Soul Tether II: corpse empty, pack still on the ghost ([props), resurrect |
| P70-9 | BOT | Ore Hopper fitted: mule pack weight drops ([props or container weight) |
| P70-10 | BOT | Survey II: Options lists the map, quest arrow points at it; III: "Dig here" spawns chest and guardians |
| P70-11 | BOT | Trader's Ledger III: bank opens in town, refused in a dungeon, while criminal, after a fight |

### P75

| id | bucket | reason |
|---|---|---|
| P75-0 | DECISION | League rewards proposal after keeping TazUO's assistants: 7 open questions (Scavenger, Field Salvager, Corpse Claim, Courier, Ledger, prices); nothing built |

### P76

| id | bucket | reason |
|---|---|---|
| P76-0 | DECISION | Extra facets research: 8 decisions (map-file policy, first facet, names, packaging, timing); nothing built |

### P77

| id | bucket | reason |
|---|---|---|
| P77-0 | DECISION | Alembic guild built with placeholders: 8 decisions (rank names A/B/C, currency, guildmaster, world step, mule module); the hall itself can be bot-checked later |

### P78

| id | bucket | reason |
|---|---|---|
| P78-0 | DECISION | Recipe gating built with defaults taken: 12 decisions to confirm or change (promotion model, merge rule, prices, empty categories, fidelity entry) |

### P79

| id | bucket | reason |
|---|---|---|
| P79-0 | DECISION | Loot boxes and fanfare built: 9 decisions (per-account achievements, level stand-in, tier rules, leather tier 5, box strength, placeholders) |

### P80

| id | bucket | reason |
|---|---|---|
| P80-0 | CC | Tutorial decisions are answered and recorded; what is left is confirming the record, not a choice |

### P81

| id | bucket | reason |
|---|---|---|
| P81-0 | EYES | Siege of Sosaria paperdoll art, spell icons, custom art and the NSFW body switch: all art; the switch is now in TazUO's Options (cc-P111) |

### P82

| id | bucket | reason |
|---|---|---|
| P82-0 | BOT | Imbuing rework is server-side (menu rows, hint lines, book teaching, Overcharged near a soul forge, tooltip line); boot crash fixed by cc-P95 so it can run now. Rank-4 rung and mule socket cap are separate decisions |

### P83

| id | bucket | reason |
|---|---|---|
| P83-1 | CC | The play-test page answers on the game PC's LAN address; Chase uses it daily |
| P83-2 | CC | Open view order (newest prompt first) and card contents (what, Expect:, needs <version>) are in the API and the page's script |
| P83-3 | CC | Pass, Fail, Later and Reopen are API writes with tests (test_playtests_reopen.py); real results are in play-tests.json |
| P83-4 | CC | Failed view and Bug id are /api/bug writes; the tile's amber rule is console fact P83_AFailNotYetLoggedTurnsItAmber |
| P83-5 | CC | 'Add an item by hand' posts /api/manual; numbering M-001, M-002 is in tools\playtests.py add_manual |
| P83-6 | CC | The service imports every 60 s; P114's notes ended 'P114 DONE' and its 6 items landed with nobody running the importer |
| P83-7 | CC | Console PLAY TESTS tile count and its two links are console behaviour under Shard-Console.Tests.ps1 |

### P84

| id | bucket | reason |
|---|---|---|
| P84-1 | DEPLOY | Shard Console, status bar Look: box (UO or Plain); takes effect on the next open |
| P84-2 | DEPLOY | Shard Console, status bar tick 'actions in their own windows'; applies at once |
| P84-3 | DEPLOY | Shard Console output pane beside the output, with Copy, Clear, Stop and Hide/Show |
| P84-4 | DEPLOY | Shard Console gump art read from the client data and cached in scripts\shard-console-cache\ |
| P84-5 | DEPLOY | Shard Console tooltips on hover |

### P85

| id | bucket | reason |
|---|---|---|
| P85-1 | CC | Homepage has reloaded since P85; its 'Shard status' entry is visible in its services API |
| P85-2 | CC | judge.py list/confirm/gate/task/status and the 7-day amber review date are tools\ code with tests |

### P86

| id | bucket | reason |
|---|---|---|
| P86-0 | DEPLOY | Shard Console Disconnect VPN button with Proton VPN (PUBLIC DNS tile), sl-ddns restart offer; needs Chase's own VPN |

### P87

| id | bucket | reason |
|---|---|---|
| P87-2 | CC | Note to the overseer about cc-autopilot.ps1's commit quoting; the Golem's golem.ps1:611 turns double quotes into single before the -File call |
| P87-3 | CC | Claim that the two dirty testing\ files went into P87's commit |

### P88

| id | bucket | reason |
|---|---|---|
| P88-1 | CC | The one deploy step is done: /nav.js answers |
| P88-2 | CC | Homepage's custom.js (cc-P88 loader) is served on every request |
| P88-3 | EYES | The shared menu bar on three pages, on a phone, current page in gold: a look check |
| P88-4 | CC | Describes the state before the restart; the fallback text is in the page and the condition has passed |

### P89

| id | bucket | reason |
|---|---|---|
| P89-0 | DECISION | Haven pages plan: 10 of 11 decisions answered 10-14 (decisions-2026-10-14.md); #10, whether NPM routes dashboard.shatteredlegacyuo.com, is still Chase's own check |

### P90

| id | bucket | reason |
|---|---|---|
| P90-1 | CC | Idea from this and the Ideas tab post /api/ideas/add; tests in tools\tests\test_feature_ideas.py |
| P90-2 | CC | 'Similar:' matching and the feature-queue list with a filter are page script over /api/ideas features |
| P90-3 | EYES | Copy new ideas puts text on the clipboard of a plain-http page and marks ideas taken; the API side is tested, the copy-paste is Chase's |
| P90-4 | CC | Became F-NN and Declined (reason required, decision 10-14) are /api/ideas/status writes |

### P91

| id | bucket | reason |
|---|---|---|
| P91-0 | CC | The bot exists and runs nightly; its 'For Chase' is how to run and read it, the schtasks line (done by P102) and a docs rewording for the overseer |

### P92

| id | bucket | reason |
|---|---|---|
| P92-0 | DECISION | Page change is done (status page reads 'Port list: 1 of 16 systems in. 283 of 983 files'); one question left: is 283 of 983 the right count |

### P93

| id | bucket | reason |
|---|---|---|
| P93-0 | DECISION | Read-and-report assessment; its 'Open questions' need Chase's answers (8). Some are already moot: P98/P100 (drafts) and P104 (UORespawn read) ran |

### P94

| id | bucket | reason |
|---|---|---|
| P94-1 | CC | Autopilot bug D90 (a prompt handed twice never commits); fixed in P99 in the Golem and cc-autopilot, the Golem replaced autopilot, and P94 was committed (537f293) |
| P94-2 | CC | False 'stopped mid-task' emails (D91); fixed in P99 (Get-AgentsOut check plus a foreground-subagents hand-off line) |
| P94-3 | CC | Play-test files tripping the start check (D92); P99 added the 'machine output' hand-off sentence and Commit-ShardWork stages with git add -A |

### P95

| id | bucket | reason |
|---|---|---|
| P95-1 | CC | Note to the overseer: D89 is marked FIXED but still sits in section 1 of docs/bug-list.md (line 88) |
| P95-2 | CC | Claim about the bot: the nightly task passes no -Commit 36c7ae9; last night built HEAD 68631cb and it booted |
| P95-3 | CC | Claim about a file: testing/bot-runs/2026-10-14-0817/ was left as evidence to be committed |
| P95-4 | CC | Claim about which files P95 changed in D:\ShatteredLegacy |

### P96

| id | bucket | reason |
|---|---|---|
| P96-0 | DEPLOY | Shard Console, Fix test shard tab: try Diagnose on the healthy shard; Prune images (frees 7.2 GB or more) is Chase's call |

### P97

| id | bucket | reason |
|---|---|---|
| P97-0 | EYES | Deploy is done (page has the Bugs tab, /api/summary has bugs_new); left: Chase files a bug from the page, ideally from his phone with a screenshot |

### P99

| id | bucket | reason |
|---|---|---|
| P99-0 | CC | The Golem cutover ran (D:\UO\golem\ACTIVE exists) and it drives the queue; its 'For Chase' was the cutover steps |

### P100

| id | bucket | reason |
|---|---|---|
| P100-1 | BOT | Server sends the Visual Builder gump on `[VBuild` (staff); its title and buttons are gump text |
| P100-2 | BOT-PARTIAL | Bot: items placed, hue value, 21x21 refused, nudge moves 1 tile; Chase: the painted pieces and hue look right on screen |
| P100-3 | BOT | Server-side: Wipe box removes builder-placed items and leaves the town's own decoration (items in the box before and after) |
| P100-4 | BOT | Server-side: Undo restores what the wipe removed, step by step, until the area matches its start |
| P100-5 | BOT | Server-side, as Administrator: world mode lets a wipe take loose decoration, and undo puts it back |
| P100-6 | BOT | Server-side: the undo record survives a save and a restart |

### P101

| id | bucket | reason |
|---|---|---|
| P101-1 | DEPLOY | Router/NPM: whether https://shatteredlegacyuo.com/ answers from outside; P101's 'public DNS gives 192.168.1.58' was the router answering port 53 |
| P101-2 | DEPLOY | Shard Console, Websites tab: the buttons (Logs, Open NPM, Deploy to Haven) need Chase's console and SSH key |
| P101-3 | CC | Done by P107: scripts/websites.json has ops-pages, ops-cutover and ops-rollback deploys and _deploySlots says P107 filled the slot |

### P102

| id | bucket | reason |
|---|---|---|
| P102-1 | CC | Done: last night's 01:30 run stopped and removed the scratch shard (run.log 04:00 'Container sl-modernuo-bot Removed') |
| P102-2 | CC | Done: the play-test service was restarted; play-tests.json carries reopenedAt on every item |
| P102-3 | CC | Done: the nightly task is registered and ran |
| P102-4 | CC | Done: the 01:30 run found 18 items and emailed 'starting' first |

### P103

| id | bucket | reason |
|---|---|---|
| P103-1 | CC | Claim: the server half ships with the test-shard deploy; the test shard now runs 68631cb, which contains P103 (2d82e7b) |
| P103-2 | EYES | The buttons open client windows (World Map, Journal, Options): only a real client shows that, and stock TazUO must show none |

### P104

| id | bucket | reason |
|---|---|---|
| P104-1 | DECISION | Chase's call to delete a 436 KB scratch folder nothing refers to; nothing to test |
| P104-2 | CC | Note for whoever keeps the third-party records (overseer); SOURCE.txt still says '0 .cs' and 'TERMS: none stated' |

### P105

| id | bucket | reason |
|---|---|---|
| P105-1 | CC | Done: sl-play-tests was restarted since (after P102 and P112), so it runs H1's code and the page answers as before |
| P105-2 | CC | Information: H2 came next and P107 built it (046541a); the cutover itself is P107-0 |

### P106

| id | bucket | reason |
|---|---|---|
| P106-0 | DECISION | The live question it was built for is gone (live retired, sl-modernuo absent); left: 2 small choices from the notes |

### P107

| id | bucket | reason |
|---|---|---|
| P107-0 | DEPLOY | Haven ops cutover: Shard Console Websites tab (Ops pages: deploy, cut over), a GitHub deploy key and the snapshot task; not done (no haven-ops state.json) |

### P108

| id | bucket | reason |
|---|---|---|
| P108-1 | DECISION | Whether the player launcher (Play.ps1, Launch-Settings.ps1, Play-Lan.bat) points at the test shard 2594 or stays on 2593 until 1.0; it changes a published package |
| P108-2 | DEPLOY | Router step: the 2593 forward to this PC now leads nowhere; closing it is optional |
| P108-3 | CC | Done: Homepage serves the new services.yaml ('UO Test Shard' tile, no 'UO Server' or 'UO Who's Online') |
| P108-4 | CC | Claim: status containers recreated and the test shard back up on the same image |
| P108-5 | CC | Claim: the overseer's passdown note went in with P108 |

### P109

| id | bucket | reason |
|---|---|---|
| P109-1 | DEPLOY | Hostinger hPanel SSH key, after the print-queue deploy (Shard Console, Websites tab); not deployed yet (192.168.1.61:8787 does not answer) |
| P109-2 | DEPLOY | After the print-queue deploy: the LAN page opens from the desktop shortcut; no NPM host |
| P109-3 | CC | Information: the rollback exists (Websites tab, Print queue: roll back, word `roll back`) |

### P110

| id | bucket | reason |
|---|---|---|
| P110-1 | DEPLOY | Shard Console, Websites tab, Mega dashboard: deploy; best after P107 and P109 (neither done yet) |
| P110-2 | DECISION | A rule, nothing to test: never route Homepage through NPM or Cloudflare |
| P110-3 | CC | Information: the rollback exists (Websites tab, Mega dashboard: roll back, word `roll back`) |

### P111

| id | bucket | reason |
|---|---|---|
| P111-4 | EYES | Client-side only: the Options list and the paperdoll art when the add-on folder is missing |
| P111-5 | CC | Claim: nothing to deploy; the commit pushed the patch and launcher change |

### P112

| id | bucket | reason |
|---|---|---|
| P112-1 | CC | Done: the play-test page was restarted and serves the P112 robot code |
| P112-2 | EYES | How the robot icons and bot chip look on the cards; nobody has seen them on screen |

### P113

| id | bucket | reason |
|---|---|---|
| P113-0 | EYES | The console window's icon in the title bar and taskbar; one small choice (copy the icon under scripts\) is in the notes |

### P114

| id | bucket | reason |
|---|---|---|
| P114-1 | EYES | Which client starts and where it lands: window title and character in the world |
| P114-2 | EYES | Gumps and macros in place, the Options list, and a Legion script starting: all on screen |
| P114-3 | CC | Rollback instructions, nothing to test; the .bak shortcuts exist |
| P114-4 | CC | Rollback instructions, nothing to test; the installed launcher backups exist |
| P114-5 | CC | A recovery command for later; CC can confirm its paths and that repo and install match today |
| P114-6 | DEPLOY | Player package: before any publish, build a new package (Shard Console, Player package tab); the 10.13 zip in dist predates P114 |

### P119

Added by cc-P119 (2026-10-15), after the cc-P115 sort below was counted.

| id | bucket | reason |
|---|---|---|
| P119-1 | BOT | Each creature appears with its body, dies to the player and leaves a corpse: all server-sent. Built, `p119_1` |
| P119-2 | EYES | Whether each body draws whole and animates: art, on screen |
| P119-3 | EYES | Riding the two mounts: the mounted rider's look |
| P119-4 | BOT-PARTIAL | The hatchet's 50 damage is server-sent (and pinned by a shard test); the thrown-axe effect is Chase's |

### P121

Added by cc-P121 (2026-10-15).

| id | bucket | reason |
|---|---|---|
| P121-1 | EYES | Reading a creature's ability list in the [props gump: staff tooling, on screen |
| P121-2 | BOT-PARTIAL | A tamed spider's poison level and the poisoned message are server-sent; the green flash is Chase's eyes |
| P121-3 | CC | The test world loads and saves with the new save file: done by CC on a scratch copy (two boots) |

### P122

Added by cc-P122 (2026-10-15).

| id | bucket | reason |
|---|---|---|
| P122-1 | BOT-PARTIAL | Offers, the wait message, bank gold and the points gump are server-sent; reading the rewards list is Chase's |
| P122-2 | BOT-PARTIAL | Seals and the absence of the rewards gump are server-sent; the Society's own gumps are Chase's |
| P122-3 | BOT-PARTIAL | Offers and the guild master's refusal are server-sent; the deed gump's button is Chase's |
| P122-4 | BOT | The bribe price, the bank withdrawal and the improved deed are all server-sent |

### P123

Added by cc-P123 (2026-10-15).

| id | bucket | reason |
|---|---|---|
| P123-1 | BOT-PARTIAL | Each vendor's offer, bank gold and the points gump are server-sent; reading the rewards list is Chase's |
| P123-2 | BOT-PARTIAL | The combine messages and the points line are server-sent; the wood line on the deed is Chase's eyes |
| P123-3 | BOT-PARTIAL | Book entries and the filtered rows are server-sent; the filter page's eight-craft layout is Chase's eyes |
| P123-4 | BOT-PARTIAL | Context menus, offers and turn-ins are server-sent; the Foresters' craft question is a gump Chase reads |
| P123-5 | BOT-PARTIAL | The keg's uses, the dye's hue and uses and the talisman's charges are server-sent; the looks are Chase's |
| P123-6 | CC | The test world loads and saves with the new deeds: done by CC on a scratch copy |

### P127

Added by cc-P127 (2026-10-16).

| id | bucket | reason |
|---|---|---|
| P127-1 | BOT-PARTIAL | The map's name line, facet line and the decode messages are server-sent; that the map opens and draws is Chase's eyes |
| P127-2 | BOT-PARTIAL | The chest's item id and the four hued spawns are server-sent; the dig animation and the chest art are Chase's eyes |
| P127-3 | BOT-PARTIAL | The refusals, the disarm messages, the guardian and the chest's contents are server-sent; how the loot looks is Chase's |
| P127-4 | BOT-PARTIAL | The facet cliloc and the spawn types are server-sent; that the client shows the Malas map is Chase's eyes |
| P127-5 | BOT | The special-item message, the pack, the once-per-creature rule and the balm's refusal are all server-sent |
| P127-6 | BOT | Skill update packets |
| P127-7 | CC | The test world loads and saves with the old maps and chests carried over: done by CC on a scratch copy |

### P128

Added by cc-P128 (2026-10-16).

| id | bucket | reason |
|---|---|---|
| P128-1 | BOT-PARTIAL | The craft results, the grapes' cliloc and the stat packets are server-sent; that the foods look right is Chase's eyes |
| P128-2 | BOT-PARTIAL | The craft, the refusal cliloc and the resistance packets are server-sent; the buff icons are Chase's eyes |
| P128-3 | BOT-PARTIAL | The paralyze, the pack count and the speed-control packet are server-sent; the thrown effects are Chase's eyes |
| P128-4 | BOT | The stat packets, loyalty and cliloc 1113051 are all server-sent |
| P128-5 | BOT-PARTIAL | The book's clilocs, the reeds' hues and the craft gump's rows are server-sent; the basket's look is Chase's eyes |
| P128-6 | BOT | Pigment hues, the mix clilocs and the dyed shirt's hue are all server-sent |
| P128-7 | BOT-PARTIAL | The placement, the plant gump and the growth are server-sent; the bed's art is Chase's eyes |
| P128-8 | EYES | Eight small things to look at; the tincture gump is the one worth eyes |
| P128-9 | CC | The test world loads and saves on the new image: done by CC on a scratch copy |

### P129

Added by cc-P129 (2026-10-16).

| id | bucket | reason |
|---|---|---|
| P129-1 | BOT | Each creature appears with its body, dies to the player and leaves a corpse: all server-sent. Built, `p129_1` |
| P129-2 | EYES | Whether each new body draws whole and animates: art, on screen |
| P129-3 | EYES | A tamed drake's and lion's ability lists in [props, and the cold aura's message and particles: the list is staff tooling, the particles are art |
| P129-4 | EYES | Riding a wild tiger once CanRide is set, and the pelts on its carved corpse: the mounted look is art; the pelts are a shard test |
| P129-5 | BOT-PARTIAL | Lifting the gold foil spawns three to five macaws that attack (server-sent); the nest's art is Chase's eyes |
| P129-6 | EYES | Carving a pumpkin with the kit and lighting it: the carved face and the lit form are art |
| P129-7 | EYES | A parrot on a perch in a house, fed a wafer, chopped into its deed and placed again: the house check needs a real house, and the parrot's look is art |
| P129-8 | EYES | The four peerless bosses by eye, and their tricks (a pet eaten, satyrs, the ooze, the terror): bodies and effects are art |
| P129-9 | DEPLOY | Seeding Old Haven: the seeder's dry run and placement on the test shard, and Vorlak still spawning under his old spawner, are a staff command and a world decision |
| P129-10 | CC | The test world loads and saves on the new image, the perch patch included: done by CC on a scratch copy |

### P130

Added by cc-P130 (2026-10-16).

| id | bucket | reason |
|---|---|---|
| P130-1 | BOT-PARTIAL | The lore gump's training section and the second-lore refusal are server-sent (clilocs in the gump layout, a 0xC1); how it draws is Chase's eyes |
| P130-2 | BOT-PARTIAL | The battle-experience overheads and the tracker gump are server-sent; the bar's drawing is Chase's eyes |
| P130-3 | EYES | The training menu, the slider and the confirmation are a chain of gumps: art and layout on screen; the arithmetic is a shard test |
| P130-4 | EYES | The planning gump: layout on screen; the zeroing rule is a shard test |
| P130-5 | BOT | The trainer's greeting and his Quest Giver tooltip line are both server-sent |
| P130-6 | DEPLOY | Reading slot ranges on the live world (a new dragon, a nightmare, a dragon from before the build): staff props on a world decision |
| P130-7 | EYES | The gate's sparkle is art; the bar and the gump are a shard test |
| P130-8 | DEPLOY | A live retame with two taming skills: a world sequence with a second character |
| P130-9 | EYES | No training section on an evo pet's or a pack mule's lore gump: on screen; the exclusion is a shard test |
| P130-10 | CC | The test world loads and saves on the new image, the slot pass logged: done by CC on a scratch copy |

Count check (cc-P115): 219 ids listed, 219 unique, against 219 open or blocked items in `testing/play-tests.json`. The
P119 group above is outside that count.

## Not built yet: how each BOT item could be checked


Setup shorthand: "admin" = the admin character; "player" = a fresh player character; all on the scratch shard.
Assert exact strings where quoted; numbers are from the notes.

- **T-001** admin [add tinker tools/hammer, open each craft gump; assert a MAKE X entry/cliloc is in the layout text. Chase checks it draws.
- **T-002** player: take a New Haven training quest, use the skill; assert skill update packets raise the skill and the quest-complete message arrives. Run once with testCenter.skillGainMultiplier off if the harness can.
- **T-003** gargoyle player, [SetSkill Blacksmith/Tailoring 100, ingots/cloth; craft gargish plate and cloth; assert items in pack and equip succeeds (worn-item packet on the gargoyle).
- **T-004** admin [SetSkill all four to 120; open each gump, walk categories, read each new entry's detail page; assert required skill not 0 and not 120.
- **T-005** same walk as T-004; assert no entry text contains "WoodPulp" or "WorkableGlass".
- **T-006** admin [GenerateSpawners per the ten files; [go Ter Mur, Abyss, Underworld; assert mobile count near the bot > 0 in each.
- **T-007** admin [GenerateNewShame, [SetupDespise, tour both; assert distinct mobile types reach 41 and 37.
- **T-010** admin [go Royal City, find the gargoyle alchemist, [props type; [save, restart scratch, relog; assert the same type/title "alchemist".
- **T-013** admin [add the hybrid treasure chest; double-click: locked message; [set Locked false, open: trap fires (HP drop / message). Chase checks the graphic.
- **T-023** admin [go to a LightInTheVoid spawn; thief player at Stealing 120; steal; assert the item reaches the pack, or record the refusal text (weight).
- **T-024** admin [go Labyrinth (Malas); assert a mobile named Miasma near its spawner; [kill; assert a corpse.
- **T-025** admin [go Twisted Weald; assert Lady Lissith; [kill; assert a corpse.
- **T-026** admin [GenStealArties; wait 15 min; [go 1134 1204 7 TerMur; assert HalfEatenSupperArtifact item; thief steals it into pack.
- **T-027** admin [add TreasureMapChest 5 x5; open; list contents; assert about one orc or tribal mask per chest with properties ([props / OPL).
- **T-031** player: raise a skill from 0 with the multiplier on and off; assert gains per use differ by about the multiplier and ClusterFSkillGain bonus gains still occur.
- **T-039** new player: assert the first-login message names the board's place and the board item is in the visible item list from the start point. Chase checks findability.
- **T-041** player joins the Smiths with ingots in pack; assert creation tools for the guild skills arrive and the ingot count is unchanged.
- **T-042** player takes the starter item twice; assert one item, the quest marked done, the second ask gives nothing.
- **T-044** gargoyle player opens Tailoring; assert the 8 gargish cloth armor entries and that one crafts; robe/sash/half apron absent.
- **T-045** account with a joined character makes a second character; assert guild gump says not a member; join gives its own items.
- **T-046** stone and [ResetMyAccount; assert identical gump text/buttons; each scope clears joined guilds as stated.
- **T-047** Young player; assert countdown text like "13 days and 23 hours of play time"; say "I want to grow up!"; assert the confirm gump.
- **T-048** [go New Haven mine camp; assert Liaison and Survey Archivist positions and two tent pieces west of the existing one. Chase checks the look.
- **P56-1** member with known Seals; [add SmallSmithBOD until iron 10 regular, fill, hand in; assert "Society of Smiths: +n standing, +52 Smithing Seals banked." and balance +52.
- **P56-2** non-member hands the same deed to a town Blacksmith; assert gold in the bank and the 1157076 gump (cc-P122).
- **P56-3** set "Completed orders" to "Ask each time"; hand in; assert the Bank button's text shows the Seal figure.
- **P56-4** [SetSkill Mining 112.4, [add PlatinumOre 10, target a forge; assert "You have no idea how to smelt this strange ore!" and ore remains; at 112.5 assert ingots about half the time.
- **P56-5** [add ReinforcedOreSatchel with the ore; Smelt at 112.4: assert "left unsmelted"; at 112.5 assert ingots in the satchel.
- **P56-6** [add ValoriteOre 10 at 98.9: assert refusal; at 99 smelts; iron smelts at 0.
- **P56-7** [add TrashBag, PetMimic, PackMule (tame); request context menus; assert entries for "Clean Up Britannia", "Eat"/"Status", "Use" and that each opens its gump or "Target the ... pack mule". Chase checks the labels draw.
- **P57-1** open the Seal catalog; assert "150", "1,800", "750", "45,000" on the named rows; deed still +52.
- **P57-2** [SetSkill Blacksmith 200, Celestial exceptional 20 deed, bank; assert about 1,466 Seals.
- **P57-3** [go a Platinum vein; mine at 112.4 (iron only) and 112.5 (Platinum about half); count ore in pack.
- **P57-4** Bulk Order Info on the guildmaster; assert Small/Large gump and the "Completed orders" line. Chase: opaque, fits.
- **P57-5** context menus on mule, satchel, Hammer of Hephaestus; assert Breed, Smelt Ore, Metal Familiarity entries and the panel gump. Chase: client labels and the TazUO.exe blank row.
- **P57-7** thief [SetSkill Stealing 150, 150 iron ingots in a pack on the ground; steal; assert at most 100 moved.
- **P58-0** player [version, page through; assert 2026.10.02 to 2026.10.05 sections present, no Staff lines. Chase: wording.
- **P61-1** [SetSkill Blacksmith 150, Frost ingots; craft; assert occasional gains; at 162.5 none in Frost, gains in Obsidian; Valorite at 140 none.
- **P61-2** at 150 with "Orders that still teach me" on, ask until Frost deeds; assert item names vary beyond plate tunics.
- **P61-3** [achievements Combat; assert "Oh Look, It's Dead" Earned line and no "Progress: 9/1".
- **P61-4** [add SmallSmithBOD until Platinum..Celestial; assert gump and OPL text "All items must be made with Frost ingots." (or metal); large too. Chase: TazUO.exe blank check.
- **P61-5** [version history; assert 2026.10.05.2 with four lines.
- **P62-1** female player, [add KitsuneEarsTail, equip; assert it is worn.
- **P62-7** male player equips it; assert "Only females can wear this." and item stays in pack.
- **P62-8** restart scratch; assert the female still wears it.
- **P64-1** fresh account; assert bulletin gump title "Shattered Legacy <current version>", an "All patch notes" button and no wiki button.
- **P64-2** press All patch notes; assert history gump; relog; assert no bulletin gump.
- **P64-3** player [version; assert current version first with "(you are here)". Chase: gold.
- **P64-4** Next to the last page; assert "Page N of N" and 2026.10.01 last; Previous goes back.
- **P64-5** assert the 2026.10.05.2 line ends "The chance to make the item is unchanged." Chase: four-row wrap.
- **P64-6** admin [version: "Staff (players do not see this list)" present; player: absent. Chase: lavender.
- **P65-0** [EvoPet give dog, pick a hue, close and reopen via double-click, [EvoPet xp 500 / 2500 / 10000, [EvoPet loops 1, [EvoPet xp 40000, loops 5, bond on, [EvoPet info; assert body ids 217 > 739 > pick > 277 > 1410 and the Echo lines; reset stone keeps stage, hue, pick, bond; stable/claim; die/res; door stays shut. Chase: the animation table.
- **P66-1** [SetSkill Hiding 150; attack, step 5 tiles, hide: assert "You can't seem to hide right now."; at 9+ hides; Hiding base passes 100.
- **P66-2** Detect Hidden 150: empty spot no gain; player hides nearby, reveal; trapped chest: assert "[trapped]"; hider at 15 tiles not found.
- **P66-3** thief 127.5 with Shadow Dancer Leggings; steal from a monster x50; assert caught about 1 in 5.
- **P66-4** peacemaking success at Musicianship 200 vs 120 the same; playing raises Musicianship past 120.
- **P66-5** Parry 200, Bushido 120, Evasion, two-hander; take 100 swings; compare damaging hits vs Parry 120. Chase: blocks as seen.
- **P66-6** Tactics 185 + a +15 item; fight; assert base Tactics rises.
- **P66-7** [ClusterFSkillGain; assert output includes the rate and "past stock ceilings on".
- **P67-1** [SetSkill Carpentry 150, Frostbark boards, stools gain; at 155 none; Shadowbark gains; at 99.9 assert "You cannot work this strange and unusual wood.".
- **P67-2** Fletching 150 Frostbark logs: bows gain, kindling never.
- **P67-3** Tinkering gump materials include Platinum..Celestial; scissors gain at 150, stop at 162.5.
- **P67-4** Blacksmithy 180 + a +10 item, Mythril plate; assert base stops at 187.5.
- **P67-5** Blacksmithy 150, toggle on: orders post-Valorite all Frost; off: Platinum, Toxic, Blaze.
- **P67-6** explosion trap at Tinkering 200 vs 120; compare HP loss; Remove Trap failure rate.
- **P67-7** axe damage at Lumberjacking 148 vs 100 on a dummy ([props Hits before/after).
- **P69-1** fresh player registers; "The Compact's Mule" refused at Iron; set Dull Copper rank; 49 ore refused, 50 ore + 25 ingots accepted; assert a bonded Compact mule, 1 slot; "You have your mule"; release: "Replace my mule".
- **P69-2** grant currencies and 25,000 gold; Civic Mule Exchange; assert Bronzeback name, hue number, higher hits, bigger pack, contents/name/bond kept. Chase: hue on body.
- **P69-3** two mules of each sex, Breed; [save, restart scratch (or [props DeliverAt); assert foal deed in bank.
- **P69-4** read the foal deed's OPL; assert sex, tier 1, generation, family line, qualities, bloodline.
- **P69-5** trade the deed to the other character; use it; assert their mule with the foal's genes.
- **P69-6** [props on an existing mule; assert Shadowhide, 1 slot, owner's follower count.
- **P70-1** join Tinkers' Union, Apprentice, 20 scrip, 5 Mining Vouchers; buy Clockwork Load Harness I schematic.
- **P70-2** craft it from Mule Modules with 15 ingots, 2 gears, 10 bone; without them assert refusal.
- **P70-3** drop on mule; OPL lists it; Options > Remove; assert back in pack, tier I.
- **P70-4** [add MuleModule TimberRack 3 on a tier 1 mule; assert refusal, still in pack.
- **P70-5** craft tier II with a tier I in pack; assert tier I gone only on success.
- **P70-6** Trailwise Tack III on a tier 3 mule; assert followers -1, back on removal.
- **P70-7** Trailwise II; gate away; assert mule beside the bot within seconds; "all come" from afar.
- **P70-8** Soul Tether II; kill full mule; assert empty corpse, pack on ghost; resurrect.
- **P70-9** 100 iron ingots in mule pack; fit Ore Hopper; assert pack weight drops.
- **P70-10** decoded map in mule pack, Survey II: Options lists it and a quest arrow packet points at it; III at the spot: "Dig here", chest and guardians appear.
- **P70-11** Trader's Ledger III: "Open your bank box" works in town; refused in a dungeon, while criminal, after a fight.
- **P71-1** Bushido 200, Nerve Strike x20; about 1 non-paralyze; at 120 about 2.
- **P71-2** Taming/Lore/Vet 200; stable 23 pets; assert the 24th refused.
- **P71-3** four bard skills 200, Fire Horn on a dummy; damage about +10% over 120.
- **P71-4** Stealth 200 hidden; count steps until revealed (about 34); 120 about 24.
- **P71-5** Healing/Anatomy 200; bandage a hurt character; heals 54 to 90.
- **P71-6** harness sets scratch clusterf.skillScaling.stealth.stepsAt200 = 30, restarts; assert about 30 steps.
- **P71-7** [version history; assert 2026.10.10 with five lines.
- **P82-0** imbue a few rows at the table, read a formula book, place an ArtificersSoulForge and try Overcharged, read the custom property's OPL line.
- **D41 regression (extra)** player double-clicks the New Haven board: Guild Directory gump; assert each guild name appears once (Artificers' Order once), 18 rows across 3 pages of 8 now that the Alembic is registered (P23 said 17 before P77); League Registrar's Guild Referrals lists the same rows.

### Sorted by cc-P137 (2026-10-17)

Open items the page showed as "Not sorted yet", from P115 to P155; the four rows above that said CHASE now name a real bucket.

| id | bucket | reason |
|---|---|---|
| P115-1 | DEPLOY | Restarting the play-test page: the overseer restarted sl-play-tests on 10-16 05:56 and Haven serves it now |
| P115-2 | EYES | The Who badges' colours and outlines on the page |
| P115-3 | DEPLOY | The Mine filter on the web page |
| P116-0 | DEPLOY | The P116 checklist is one paragraph: reopen the Shard Console and check the tabs scroll |
| P117-0 | DEPLOY | The P117 checklist is one paragraph: rebuild the test shard, then a fresh login shows the bulletin |
| P123-0 | CC | Placeholder: the importer could not read this prompt's For Chase list (a paragraph before the list that is not a marker switches the parser off; cc-P137 notes). CC reads the notes; the prompt's own checks are the rows it wrote here |
| P124-0 | DEPLOY | The P124 checklist is one line: the player package now ships our TazUO build |
| P125-1 | DEPLOY | The Golem's long run is a Shard Console control |
| P125-2 | DEPLOY | Wrap up is a Shard Console control |
| P125-3 | DEPLOY | Find a stopping point is a Shard Console control |
| P125-4 | DEPLOY | The GOLEM tile at rest, and waking it with the phrase |
| P125-5 | DEPLOY | The rest emails arrive in Chase's inbox |
| P126-0 | DECISION | P126 is a design: its For Chase is one decision and a few facts about the work PC |
| P127-0 | CC | Placeholder: the importer could not read this prompt's For Chase list (a paragraph before the list that is not a marker switches the parser off; cc-P137 notes). CC reads the notes; the prompt's own checks are the rows it wrote here |
| P128-0 | CC | Placeholder: the importer could not read this prompt's For Chase list (a paragraph before the list that is not a marker switches the parser off; cc-P137 notes). CC reads the notes; the prompt's own checks are the rows it wrote here |
| P129-0 | CC | Placeholder: the importer could not read this prompt's For Chase list (a paragraph before the list that is not a marker switches the parser off; cc-P137 notes). CC reads the notes; the prompt's own checks are the rows it wrote here |
| P130-0 | CC | Placeholder: the importer could not read this prompt's For Chase list (a paragraph before the list that is not a marker switches the parser off; cc-P137 notes). CC reads the notes; the prompt's own checks are the rows it wrote here |
| P131-1 | DEPLOY | Signing the CLI in is Chase's own account, on the game PC |
| P131-2 | DEPLOY | Waking the Golem is a Shard Console control |
| P131-3 | DEPLOY | Self-wake is a Shard Console setting and an email |
| P131-4 | DEPLOY | The night shift is a Shard Console setting |
| P131-5 | DEPLOY | The GOLEM tile, the email subject and the Windows notification through a rest |
| P131-6 | CC | The new keys are a file CC can read |
| P132-0 | EYES | The P132 checklist is prose: the console's Enhanced look, its splitters and the art slots |
| P133-0 | DEPLOY | P133's For Chase is the Haven dashboard's deploy steps (Websites deploys, tokens, keys) |
| P154-1 | EYES | How fast the console feels is Chase's call |
| P154-2 | EYES | The two first-open waits are on screen |
| P154-3 | DEPLOY | Restart the console to get P154's code |
| P155-1 | DEPLOY | The auth key is made in Chase's Tailscale admin console |
| P155-2 | DEPLOY | Installing the web console on the game PC |
| P155-3 | DEPLOY | Opening the web console on the tailnet |
| P155-4 | DEPLOY | Reading the web console's views |
| P155-5 | DECISION | Phase 2 (Golem controls on the web console) is a later prompt for Chase to queue |
| P155-6 | DEPLOY | Uninstalling the web console, only if wanted |
| P134-1 | CC | Which files P134 added and changed is git history |
| P134-2 | CC | Where the vseUOAware copy lives and that third-party was untouched is on disk |
| P134-3 | CC | Asking the vseUOAware server from a CC session in shard-migration; cc-P137 did exactly that |
| P135-1 | CC | Which files P135 added is git history |
| P135-2 | CC | What P135 did not touch is on disk and in git |
| P135-3 | BOT-PARTIAL | The map check commands' replies are server messages; the red-rune overlay is Chase's eyes |
| P136-0 | DEPLOY | P136's For Chase is one line: the status page keeps itself current and opens with the Needs overseer review box (a web page) |

### P137

Added by cc-P137 (2026-10-17).

| id | bucket | reason |
|---|---|---|
| P137-1 | BOT | The resurrection gump is server-sent, and the bot can die (P119-1 run 2 on 10-16 did) and walk (the soak's walker). Check not written yet: an admin `[kill`s a fresh character, it walks to 3463,2600, and the bot waits for the ResurrectGump |
| P137-2 | BOT | The context menu's entries (clilocs 3006195, 3006198) and the tithing gump are server-sent |
| P137-3 | DEPLOY | The survey and the seeder are staff commands on the test shard after a deploy |
| P137-4 | BOT | The refusal message and the shard total are server-sent |
| P137-5 | BOT | Where an item lands (0x25 into the satchel or the pack) and the full message are server-sent |
| P137-6 | CC | The service state on /api/items says which tools code runs and since when |
| P137-7 | BOT | The overnight bot's own P119-1 result |

### P138

Added by cc-P138 (2026-10-17).

| id | bucket | reason |
|---|---|---|
| P138-1 | EYES | Where the ears and tail sit on the paperdoll is a drawing question; the before/after images are in the notes (section 2) |
| P138-2 | EYES | The hood case: the ears poke through the hood of a GM robe; a look, not a packet |
| P138-3 | BOT-PARTIAL | Bot: a man equips it (the worn-item packet, layer 0x12); Chase: the male paperdoll 54783 looks right |
| P138-4 | EYES | The elf bodies (14 and 15) take the same gumps; a look |
| P138-5 | BOT | The refusal is server-sent: a gargoyle gets "Only humans and elves can wear this." and the item stays in the pack |
| P138-6 | EYES | Standing, walking and running in the eight directions, with and without a robe: how the tail reads is a look |
| P138-7 | EYES | Chase's local Topless and Nude add-on only; never on the test shard's package |

### P139

Added by cc-P139 (2026-10-17).

| id | bucket | reason |
|---|---|---|
| P139-1 | BOT | The body-route creature spawns with body 2048 in the mobile packet, fights back with its bow, dies to the player and leaves a corpse (0x2006, amount 2048): all server-sent. Built, `p139_1`, run on this prompt's image (notes) |
| P139-2 | DEPLOY | The new package (anim7 with the body, the launcher's Bodyconv.def and mobtypes.txt copies) has to be built and published from the committed tree, and the test shard rebuilt, before anything draws |
| P139-3 | EYES | Whether body 2048 draws and animates in TazUO: walk, stand, the bow shot (action 4), get hit, death, the corpse, the fidgets: art on screen |
| P139-4 | EYES | The launcher's copies on Chase's PC (app\uo-overrides\Bodyconv.def and mobtypes.txt end with our lines): a file on his machine |
| P139-0 | DEPLOY | Placeholder for P139's For Chase list; Chase's part is the deploy (build and publish the package, rebuild the test shard, run the launcher) then the look, as rows P139-2 to P139-4 say; P139-1 is the bot's |

### P140

Added by cc-P140 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P140-1 | BOT | Six Burrows spawns appear with their bodies in the mobile packet, fight back, die and leave a corpse (0x2006, amount = body): server-sent. Built, `p140_1`, run on this prompt's image (notes) |
| P140-2 | DEPLOY | The package (anim7 with 24 bodies, about 25 MB more) must be built and published from the committed tree, and the test shard rebuilt, before any new body draws |
| P140-3 | EYES | Every new body draws whole and animates (walk, stand, attack, hit, death, corpse): art on screen, 23 bodies |
| P140-4 | EYES | The Slinger's rust red (hue 1258) against the sheet's frame recolour: a colour call |
| P140-5 | EYES | The Crop Crow: the 1.5x bird in black between the bird and the eagle: a look |
| P140-6 | EYES | The Overdraft's 1.5x scale next to a player, and its strongbox-brown hue 1740: a look |
| P140-7 | EYES | The decoy Safe Deposit Boxes spring and bite a tutorial participant (cc-P50's mimic frames): art, on screen; the engagement rule is a shard fact |
| P140-8 | DECISION | The Tree Fellows (Rootling): keep the hued stock bogling, or decide the 6 to 17 MB files' route (notes, Decisions) |

### P141

Added by cc-P141 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P141-1 | DECISION | Approve the Burrows layout and the look per zone on the mockup page, or say what to change: the map batch waits on it |
| P141-2 | BOT | After the map batch: the Vault doorway's refusal (the Echo's line for a non-trainee and a graduate) and a trainee and pet walking in are server-sent (system message, the mobile's position). Check not written yet: the floor is void land today |
| P141-3 | BOT-PARTIAL | After the map batch: the Overdraft's death, the crawlway's item id changing from rocks (0x1367) to a hole (0x1B71) and the move into the Warren are server-sent; whether the cave-in and the dust read right is Chase's. Check not written yet |
| P141-4 | EYES | After the map batch and the seeder: the landing ankh stands against the east wall facing the arrival and a ghost that walks to it is offered resurrection; how it sits on the new floor is a look |
| P141-5 | DECISION | A Young trainee who dies in the Vault wakes at New Haven's healer (pinned's Young rule), not the landing: keep it, or ask for a Vault rule (a pinned patch) |
| P141-6 | DECISION | The Warren fillers: Rotworm and Grubber kept as rare spawns, BloodWorm moved to the Gloom (too strong for tier 1), or dropped |
| P141-7 | DEPLOY | After the map batch: run the seeder on the test shard (dry run, then for real) and look at the 33 spawners, the ankh and the crawlway in place |

### P142

Added by cc-P142 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P142-1 | BOT | The refusal lines (system messages) and the special-item cliloc are server-sent; the standing is set with `[GuildStanding` |
| P142-2 | BOT | The special-item cliloc inside a champion spawn region is server-sent |
| P142-3 | BOT | The special-item cliloc inside the Burrows region at Initiate, and The Burrow Mother's refusal line, are server-sent; the region exists before the map batch |
| P142-4 | BOT | The minor haul (pack contents, the scrip line) and the skill update packets are server-sent |
| P142-5 | BOT | The caught, wary and already-stolen lines, the reveal and the creature attacking are all server-sent |
| P142-6 | BOT-PARTIAL | The scroll's learning, the craft menu row and the item properties are server-sent; the cloak and the ring on a paperdoll are Chase's eyes |
| P142-7 | DEPLOY | Needs a save and a restart of the test shard through the Shard Console |

### P144

Added by cc-P144 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P144-1 | DEPLOY | Check scripts is a Shard Console button that reaches Haven over SSH |
| P144-2 | DEPLOY | TazUO's script editor and the Shard Console's Commit tab on the tower |
| P144-3 | DEPLOY | Publish to dev is a Shard Console button that changes what Haven serves |
| P144-4 | DEPLOY | Promote to official changes what every install pulls, then a browser and GitHub |
| P144-5 | DEPLOY | Needs the work PC, the tower and GitHub |
| P144-6 | DEPLOY | Needs the new package's launcher on a PC flagged dev, Haven's dev channel and Tailscale switched off |
| P144-7 | DEPLOY | Needs a built and published player package on a player's PC or in Windows Sandbox |

### P145

Added by cc-P145 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P145-1 | EYES | TazUO's script list and the SL_Combat window on screen |
| P145-2 | EYES | A Legion script fighting in a real client: targeting, the highlight, the cooldown bar |
| P145-3 | EYES | Which mobiles the script attacks, watched in the client |
| P145-4 | EYES | Companion care in the client with a pet out |
| P145-5 | EYES | AFK seeking, looting and walking back, watched in the client |
| P145-6 | EYES | The panic hotkey mid-fight in the client |
| P145-7 | EYES | The rater's lines and the Results window |
| P145-8 | BOT-PARTIAL | The bot can check [artificerrank's lines (a server message); the window's rank label and the Unravel tier are Chase's |
| P145-9 | EYES | The profile editor and Suggest's notes in the client |
| P145-10 | EYES | Per-character settings across a relog |
| P145-11 | EYES | Auto-sort moving items into bags in the client |

### P160 (sorted by cc-P146)

| id | bucket | reason |
|---|---|---|
| P160-0 | CC | P160's For Chase only explains the pacing; nothing to do by hand. golem.log shows the Saturday rest, the Sunday 4:00 AM self-wake and hand-ons, and the one free-reset email |

### P161 (sorted by cc-P146)

| id | bucket | reason |
|---|---|---|
| P161-1 | CC | Which windows close and which are kept open is in golem.log and the session records after a night of hand-offs, against the Golem tests |
| P161-2 | CC | The four settings and their defaults are in D:\UO\golem\settings.json and the Golem README |
| P161-3 | EYES | Typing in a finished window on the desktop and watching it stay open is Chase's, on screen |
| P161-4 | EYES | Whether closed sessions' tabs vanish from the golem Windows Terminal window, and closing the dead P999 test tab, is on Chase's screen |
| P161-5 | CC | The duplicate-wake refusal is a Golem test fact and shows in golem.log as a refused second wake |
| P161-6 | DEPLOY | The new sessions line is on the Shard Console's Golem tab, after a console restart loads P161's code |

### P162 (sorted by cc-P146)

| id | bucket | reason |
|---|---|---|
| P162-1 | CC | After the Wed 10-21 4:00 PM reset, golem.log, the Golem's state and the sent mail show whether the window opened Tue 4:00 PM, handed on to 97%, ignored the warning and the night pace check, self-woke and mailed the summary |
| P162-2 | CC | The three settings and their defaults are in D:\UO\golem\settings.json, the README and the Golem tests |
| P162-3 | CC | That the Golem never spends the free reset or usage credits is read from golem.ps1 and golem.log |

### P147 (sorted by cc-P147)

| id | bucket | reason |
|---|---|---|
| P147-1 | EYES | The Achievements button in Help's slot on the classic paperdoll, and that it opens the page, are on screen |
| P147-2 | EYES | That another character's paperdoll has no Achievements button is on screen |
| P147-3 | EYES | The top bar's Achievements button and the page it opens are on screen |
| P147-4 | EYES | The modern paperdoll menu's Achievements line is on screen |
| P147-5 | EYES | That the stock TazUO shows Help and no Achievements is on screen |

### P146 (sorted by cc-P147)

| id | bucket | reason |
|---|---|---|
| P146-1 | DEPLOY | The decisions on the page and the Where chips (Mine + Questions, Mine + In game: Player + Elf) are on Chase's screen |
| P146-2 | DEPLOY | Answering a card (a choice, Keep what's built, the box, Ask me later) is done on the page |
| P146-3 | CC | After Chase answers, the next commit's testing/decisions.json holds the answer with who and when; checked in the repo |
| P146-4 | CC | The service's /api/items service.code changes after Haven's pull with no restart, and /api/items carries decisions; read from the page's API |

### P166

Added by cc-P166 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P166-1 | EYES | How the tail reads facing west and north (and that the other six directions did not change) is a look; the renders are in the notes |
| P166-2 | EYES | Whether the ears sit right on a bald head and still rise out of hair is a look, side by side |

### P170

Added by cc-P170 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P170-1 | BOT | Each offer is the accept gump the server sends, with the item and its metal in its text; the bot can ask the Society for orders at 144 with the setting on and off and read them |

### P171

Added by cc-P171 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P171-1 | BOT | The anger and start messages (502805, 1010597) are what the server sends; the bot can tame a Dread Warhorse at 200 and count them |

### P173

Added by cc-P173 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P173-1 | BOT | The disenchant list, the Extract row and the essence are gump text and an item the server sends; the bot can run the table's buttons on a Summer Wind War Axe |

### P175

Added by cc-P175 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P175-1 | BOT | The two Appraise for Cleanup messages are server text; the bot can add the swords, set the properties and appraise them |
| P175-2 | BOT | The "Corpse cleared ... +N Clean Up points" messages are server text; the bot can kill an Orc and a Dragon and clean up both |
| P175-3 | BOT-PARTIAL | Buying through the store gump and the item in the pack are the bot's; how the new rewards look and the pigment's hue are Chase's |

### P176

Added by cc-P176 (2026-10-18).

| id | bucket | reason |
|---|---|---|
| P176-1 | BOT | The confirmation page and the three summary lines are gump and server text, and the bag's contents are items; the bot can fill a bag, press Unravel Container and read them |

### P182

Added by cc-P182 (2026-10-19).

| id | bucket | reason |
|---|---|---|
| P182-1 | DEPLOY | Installing the web console and its sidecar on the game PC is a step on the PC, not in the game |
| P182-2 | EYES | Pressing the Golem buttons on a phone over the tailnet and judging one-handed use are Chase's |
| P182-3 | DEPLOY | The refusal checks run against the installed service on the game PC |
| P182-4 | EYES | Needs a real STOPPED prompt and the Shard Console on the game PC |
| P182-5 | DECISION | Generating and approving art is Chase's choice in the Art tab |
| P182-6 | DECISION | A tailnet access-control change is Chase's |

### P193

Added by cc-P193 (2026-10-20).

| id | bucket | reason |
|---|---|---|
| P193-1 | BOT-PARTIAL | The catch clilocs (1043297 with a fish label) and the carve are server-sent; that the fish look right is Chase's eyes |
| P193-2 | EYES | Deep water needs a boat and a dungeon needs a walk the bot does not make; the rare fish's tooltip is Chase's eyes |
| P193-3 | BOT | The buoy's item id, the bob overhead message, the skill packets and the trap's contents are all server-sent |
| P193-4 | BOT-PARTIAL | The deed, its clilocs and the addon's components are server-sent; the hung trophy's look is Chase's eyes |
| P193-5 | EYES | Staff-placed champions on a boat; the fight is Chase's eyes |
| P193-6 | BOT-PARTIAL | The set bonus packets are server-sent; the bait bonus has nothing to bite until baits land |
| P193-7 | CC | The test world loads and saves on the new image: done by CC on a scratch copy |
