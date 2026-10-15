# Overnight play tests, 2026-10-15-0130

**18 pass, 2 fail, 0 flaky** (20 checks, each run 3 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: commit 68631cb (-Commit, a worktree in D:\UO\bot-shard\src)
- World: a copy of the test world's automatic backup 2026-10-15-06-30-01, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P64-1 | FAIL | 0/3 | no bulletin gump on the account's first login (5 gumps: [['— ACHIEVEMENT UNLOCKED —', 'Still BreathingThe bar was on the floor. You cleared it. (Earned: logged in for the first time)'], ['— ACHIEVEMENT UNLOCKED —', "You've Read the IntroductionA promising start. The bar is currently underground. ... | [1](transcripts/P64-1-run1.txt) [2](transcripts/P64-1-run2.txt) [3](transcripts/P64-1-run3.txt) |  |
| P64-2 | FAIL | 0/3 | no bulletin, so no All patch notes to press (observed during the matching P64-1 run) | [1](transcripts/P64-2-run1.txt) [2](transcripts/P64-2-run2.txt) [3](transcripts/P64-2-run3.txt) |  |
| P64-3 | PASS | 3/3 | first heading 'Shattered Legacy 2026.10.14.19'; (you are here) on page 1: True | [1](transcripts/P64-3-run1.txt) [2](transcripts/P64-3-run2.txt) [3](transcripts/P64-3-run3.txt) | P64-3: the entry shows gold |
| P64-4 | PASS | 3/3 | last page ['Page 31 of 31']; last version 2026.10.01; after Previous ['Page 30 of 31'] | [1](transcripts/P64-4-run1.txt) [2](transcripts/P64-4-run2.txt) [3](transcripts/P64-4-run3.txt) |  |
| P58-0 | PASS | 3/3 | versions 10.02-10.05 shown: ['2026.10.05.3', '2026.10.05.2', '2026.10.05', '2026.10.04', '2026.10.03', '2026.10.02']; missing none; Staff list visible to a player: False | [1](transcripts/P58-0-run1.txt) [2](transcripts/P58-0-run2.txt) [3](transcripts/P58-0-run3.txt) | P58-0: the patch-note wording reads right |
| P61-5 | PASS | 3/3 | 2026.10.05.2 present: True, 4 player lines (CHANGELOG at the code under test: 4) | [1](transcripts/P61-5-run1.txt) [2](transcripts/P61-5-run2.txt) [3](transcripts/P61-5-run3.txt) |  |
| P64-5 | PASS | 3/3 | matching line: 'thril to 187.5, Adamantium and Celestial to 200. The chance to make the item is unchanged.' | [1](transcripts/P64-5-run1.txt) [2](transcripts/P64-5-run2.txt) [3](transcripts/P64-5-run3.txt) | P64-5: it wraps onto four rows |
| P71-7 | PASS | 3/3 | 2026.10.10 present: True, 5 player lines (CHANGELOG at the code under test: 5) | [1](transcripts/P71-7-run1.txt) [2](transcripts/P71-7-run2.txt) [3](transcripts/P71-7-run3.txt) |  |
| P64-6 | PASS | 3/3 | admin sees 'Staff (players do not see this list)': True; player sees it: False | [1](transcripts/P64-6-run1.txt) [2](transcripts/P64-6-run2.txt) [3](transcripts/P64-6-run3.txt) | P64-6: the staff list shows lavender |
| P66-7 | PASS | 3/3 | reply: 'ClusterF skill gain: rate enabled, 3 chance attempt(s), 5x gain amount; past stock ceilings on.' | [1](transcripts/P66-7-run1.txt) [2](transcripts/P66-7-run2.txt) [3](transcripts/P66-7-run3.txt) |  |
| P62-1 | PASS | 3/3 | worn: True (layer 18); messages [] | [1](transcripts/P62-1-run1.txt) [2](transcripts/P62-1-run2.txt) [3](transcripts/P62-1-run3.txt) |  |
| P62-7 | PASS | 3/3 | refusal True; worn False; back in pack True; messages ['Only females can wear this.', 'Welcome to Shattered Legacy BOT.'] | [1](transcripts/P62-7-run1.txt) [2](transcripts/P62-7-run2.txt) [3](transcripts/P62-7-run3.txt) |  |
| T-039 | PASS | 3/3 | gargoyle female at (3503, 2574, 14): message None; welcome gump says 'The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.'; the board is 1 tiles away | [1](transcripts/T-039-run1.txt) [2](transcripts/T-039-run2.txt) [3](transcripts/T-039-run3.txt) | T-039: a new player can find the board by eye |
| CREATE | PASS | 3/3 | gargoyle male: body 666 (want 666), status name 'Bot Gargoyle M A' (asked for 'Bot Gargoyle M A'), at (3503, 2574, 14) | [1](transcripts/CREATE-run1.txt) [2](transcripts/CREATE-run2.txt) [3](transcripts/CREATE-run3.txt) |  |
| T-047 | PASS | 3/3 | countdown 'You will enjoy the benefits and relatively safe status of a young player for another 13 days and 23 hours of play time. Say "I want to grow up!" to give it up sooner.' (days and hours: True); confirm gump: ['', "Renouncing 'Young Player' Status"] | [1](transcripts/T-047-run1.txt) [2](transcripts/T-047-run2.txt) [3](transcripts/T-047-run3.txt) |  |
| D41 | PASS | 3/3 | 18 rows, header says 18 guilds, 18 way buttons; duplicates none; Artificers' Order 1 time(s) | [1](transcripts/D41-run1.txt) [2](transcripts/D41-run2.txt) [3](transcripts/D41-run3.txt) |  |
| P56-6 | PASS | 3/3 | at 98.9: refused True ['You have no idea how to smelt this strange ore!'], ore left 10; at 99.0 over 6 tries: refused 0, smelted 3, burned 3 | [1](transcripts/P56-6-run1.txt) [2](transcripts/P56-6-run2.txt) [3](transcripts/P56-6-run3.txt) |  |
| P56-4 | PASS | 3/3 | at 112.4: refused True ['Double Click On Me For Help!'], ore left 10; at 112.5 over 8 tries: refused 0, smelted 3, burned 5 | [1](transcripts/P56-4-run1.txt) [2](transcripts/P56-4-run2.txt) [3](transcripts/P56-4-run3.txt) |  |
| P61-3 | PASS | 3/3 | rat killed by the player: True; row 'Oh Look, It\'s Dead [5 AP / 5 R]"You are, by definition, a killer now. Congratulations."(Earned: slew your first creature)'; other rows with progress: 2 | [1](transcripts/P61-3-run1.txt) [2](transcripts/P61-3-run2.txt) [3](transcripts/P61-3-run3.txt) |  |
| T-046 | PASS | 3/3 | same gump type True; same text True (29 lines); same buttons True [0, 1, 2, 10] | [1](transcripts/T-046-run1.txt) [2](transcripts/T-046-run2.txt) [3](transcripts/T-046-run3.txt) | T-046: each scope (this character / all / account) clearing what it says, joined guilds included, is not pressed by the bot; it would wipe its own characters |

## Fail, Flaky and could-not-run, every run

- **P64-1 FAIL** (Fresh account login: bulletin with the current version, All patch notes, no wiki button)
  - run 1 FAIL: no bulletin gump on the account's first login (5 gumps: [['— ACHIEVEMENT UNLOCKED —', 'Still BreathingThe bar was on the floor. You cleared it. (Earned: logged in for the first time)'], ['— ACHIEVEMENT UNLOCKED —', "You've Read the IntroductionA promising start. The bar is currently underground. (Earned: reached 50 in a skill)"], ['— ACHIEVEMENT UNLOCKED —', 'Legal Jurisdiction AcquiredThe one where monsters are less likely to specifically seek you out. (Earned: set foot in Trammel)'], ['— ACHIEVEMENT UNLOCKED —', 'Double-Digit Thousands Is a PersonalityThe wealth is real. For now. (Earned: held 10,000 gold in your bank)'], ['Welcome to New Haven', 'Every skill has a guild in New Haven. Joining one is free, and it hands you the tools of its trade and the starter items the trainers give.The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.The League of Extraordinary Citizens ties every guild together. Find its Registrar in New Haven.']]) ([transcript](transcripts/P64-1-run1.txt))
  - run 2 FAIL: no bulletin gump on the account's first login (5 gumps: [['— ACHIEVEMENT UNLOCKED —', 'Still BreathingThe bar was on the floor. You cleared it. (Earned: logged in for the first time)'], ['— ACHIEVEMENT UNLOCKED —', "You've Read the IntroductionA promising start. The bar is currently underground. (Earned: reached 50 in a skill)"], ['— ACHIEVEMENT UNLOCKED —', 'Legal Jurisdiction AcquiredThe one where monsters are less likely to specifically seek you out. (Earned: set foot in Trammel)'], ['— ACHIEVEMENT UNLOCKED —', 'Double-Digit Thousands Is a PersonalityThe wealth is real. For now. (Earned: held 10,000 gold in your bank)'], ['Welcome to New Haven', 'Every skill has a guild in New Haven. Joining one is free, and it hands you the tools of its trade and the starter items the trainers give.The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.The League of Extraordinary Citizens ties every guild together. Find its Registrar in New Haven.']]) ([transcript](transcripts/P64-1-run2.txt))
  - run 3 FAIL: no bulletin gump on the account's first login (5 gumps: [['— ACHIEVEMENT UNLOCKED —', 'Still BreathingThe bar was on the floor. You cleared it. (Earned: logged in for the first time)'], ['— ACHIEVEMENT UNLOCKED —', "You've Read the IntroductionA promising start. The bar is currently underground. (Earned: reached 50 in a skill)"], ['— ACHIEVEMENT UNLOCKED —', 'Legal Jurisdiction AcquiredThe one where monsters are less likely to specifically seek you out. (Earned: set foot in Trammel)'], ['— ACHIEVEMENT UNLOCKED —', 'Double-Digit Thousands Is a PersonalityThe wealth is real. For now. (Earned: held 10,000 gold in your bank)'], ['Welcome to New Haven', 'Every skill has a guild in New Haven. Joining one is free, and it hands you the tools of its trade and the starter items the trainers give.The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.The League of Extraordinary Citizens ties every guild together. Find its Registrar in New Haven.']]) ([transcript](transcripts/P64-1-run3.txt))
- **P64-2 FAIL** (All patch notes opens the history; a relog shows no bulletin)
  - run 1 FAIL: no bulletin, so no All patch notes to press (observed during the matching P64-1 run) ([transcript](transcripts/P64-2-run1.txt))
  - run 2 FAIL: no bulletin, so no All patch notes to press (observed during the matching P64-1 run) ([transcript](transcripts/P64-2-run2.txt))
  - run 3 FAIL: no bulletin, so no All patch notes to press (observed during the matching P64-1 run) ([transcript](transcripts/P64-2-run3.txt))

## Soak

120 minutes; activity {"walker_steps": 22698, "miner_digs": 3507, "miner_smelts": 0, "fighter_kills": 1671, "fighter_swings": 1677}.
Memory 484.1 MB at the start, 590.7 MB at the end, 590.7 MB at most.
Loud log lines (Exception, Error, crash, save failures): 0.

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-15T01:03:09.9003719Z sha256:918d37609f17fc0a63bfc3be68b5be668729ce1b09675dfb18c31b3cfbf5401b"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-15T01:03:09.9003719Z sha256:918d37609f17fc0a63bfc3be68b5be668729ce1b09675dfb18c31b3cfbf5401b"}`
