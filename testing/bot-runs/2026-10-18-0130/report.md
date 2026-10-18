# Overnight play tests, 2026-10-18-0130

**10 pass, 2 fail, 0 flaky, 12 could not run** (24 checks, each run 3 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: commit 73a0348 (-Commit, a worktree in D:\UO\bot-shard\src)
- World: a copy of the test world's automatic backup 2026-10-18-06-30-00, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P64-1 | PASS | 3/3 | title 'Shattered Legacy 2026.10.18'; All patch notes button yes; wiki text none | [1](transcripts/P64-1-run1.txt) [2](transcripts/P64-1-run2.txt) [3](transcripts/P64-1-run3.txt) |  |
| P64-2 | PASS | 3/3 | history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run) | [1](transcripts/P64-2-run1.txt) [2](transcripts/P64-2-run2.txt) [3](transcripts/P64-2-run3.txt) |  |
| P64-3 | PASS | 3/3 | first heading 'Shattered Legacy 2026.10.18'; (you are here) on page 1: True | [1](transcripts/P64-3-run1.txt) [2](transcripts/P64-3-run2.txt) [3](transcripts/P64-3-run3.txt) | P64-3: the entry shows gold |
| P64-4 | FAIL | 0/3 | last page ['Page 41 of 44']; last version 2026.10.02; after Previous ['Page 40 of 44'] | [1](transcripts/P64-4-run1.txt) [2](transcripts/P64-4-run2.txt) [3](transcripts/P64-4-run3.txt) |  |
| P58-0 | PASS | 3/3 | versions 10.02-10.05 shown: ['2026.10.05.3', '2026.10.05.2', '2026.10.05', '2026.10.04', '2026.10.03', '2026.10.02']; missing none; Staff list visible to a player: False | [1](transcripts/P58-0-run1.txt) [2](transcripts/P58-0-run2.txt) [3](transcripts/P58-0-run3.txt) | P58-0: the patch-note wording reads right |
| P61-5 | PASS | 3/3 | 2026.10.05.2 present: True, 4 player lines (CHANGELOG at the code under test: 4) | [1](transcripts/P61-5-run1.txt) [2](transcripts/P61-5-run2.txt) [3](transcripts/P61-5-run3.txt) |  |
| P64-5 | PASS | 3/3 | matching line: 'thril to 187.5, Adamantium and Celestial to 200. The chance to make the item is unchanged.' | [1](transcripts/P64-5-run1.txt) [2](transcripts/P64-5-run2.txt) [3](transcripts/P64-5-run3.txt) | P64-5: it wraps onto four rows |
| P71-7 | PASS | 3/3 | 2026.10.10 present: True, 5 player lines (CHANGELOG at the code under test: 5) | [1](transcripts/P71-7-run1.txt) [2](transcripts/P71-7-run2.txt) [3](transcripts/P71-7-run3.txt) |  |
| P64-6 | PASS | 3/3 | admin sees 'Staff (players do not see this list)': True; player sees it: False | [1](transcripts/P64-6-run1.txt) [2](transcripts/P64-6-run2.txt) [3](transcripts/P64-6-run3.txt) | P64-6: the staff list shows lavender |
| P66-7 | PASS | 3/3 | reply: 'ClusterF skill gain: rate enabled, 3 chance attempt(s), 5x gain amount; past stock ceilings on.' | [1](transcripts/P66-7-run1.txt) [2](transcripts/P66-7-run2.txt) [3](transcripts/P66-7-run3.txt) |  |
| P62-1 | PASS | 3/3 | worn: True (layer 18); messages [] | [1](transcripts/P62-1-run1.txt) [2](transcripts/P62-1-run2.txt) [3](transcripts/P62-1-run3.txt) |  |
| P62-7 | FAIL | 0/3 | refusal False; worn True; back in pack False; messages ['Welcome to Shattered Legacy BOT.'] | [1](transcripts/P62-7-run1.txt) [2](transcripts/P62-7-run2.txt) [3](transcripts/P62-7-run3.txt) |  |
| T-039 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/T-039-run1.txt) [2](transcripts/T-039-run2.txt) [3](transcripts/T-039-run3.txt) | T-039: a new player can find the board by eye |
| CREATE | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/CREATE-run1.txt) [2](transcripts/CREATE-run2.txt) [3](transcripts/CREATE-run3.txt) |  |
| T-047 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/T-047-run1.txt) [2](transcripts/T-047-run2.txt) [3](transcripts/T-047-run3.txt) |  |
| D41 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/D41-run1.txt) [2](transcripts/D41-run2.txt) [3](transcripts/D41-run3.txt) |  |
| P56-6 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P56-6-run1.txt) [2](transcripts/P56-6-run2.txt) [3](transcripts/P56-6-run3.txt) |  |
| P56-4 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P56-4-run1.txt) [2](transcripts/P56-4-run2.txt) [3](transcripts/P56-4-run3.txt) |  |
| P61-3 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P61-3-run1.txt) [2](transcripts/P61-3-run2.txt) [3](transcripts/P61-3-run3.txt) |  |
| P119-1 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P119-1-run1.txt) [2](transcripts/P119-1-run2.txt) [3](transcripts/P119-1-run3.txt) |  |
| P129-1 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P129-1-run1.txt) [2](transcripts/P129-1-run2.txt) [3](transcripts/P129-1-run3.txt) |  |
| P139-1 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P139-1-run1.txt) [2](transcripts/P139-1-run2.txt) [3](transcripts/P139-1-run3.txt) |  |
| P140-1 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/P140-1-run1.txt) [2](transcripts/P140-1-run2.txt) [3](transcripts/P140-1-run3.txt) |  |
| T-046 | ERROR | 0/3 | ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it | [1](transcripts/T-046-run1.txt) [2](transcripts/T-046-run2.txt) [3](transcripts/T-046-run3.txt) | T-046: each scope (this character / all / account) clearing what it says, joined guilds included, is not pressed by the bot; it would wipe its own characters |

## Fail, Flaky and could-not-run, every run

- **P64-4 FAIL** ([version pages: Next to Page N of N, last version 2026.10.01, Previous goes back)
  - run 1 FAIL: last page ['Page 41 of 44']; last version 2026.10.02; after Previous ['Page 40 of 44'] ([transcript](transcripts/P64-4-run1.txt))
  - run 2 FAIL: last page ['Page 41 of 44']; last version 2026.10.02; after Previous ['Page 40 of 44'] ([transcript](transcripts/P64-4-run2.txt))
  - run 3 FAIL: last page ['Page 41 of 44']; last version 2026.10.02; after Previous ['Page 40 of 44'] ([transcript](transcripts/P64-4-run3.txt))
- **P62-7 FAIL** (A male character cannot: 'Only females can wear this.', the item stays in the pack)
  - run 1 FAIL: refusal False; worn True; back in pack False; messages ['Welcome to Shattered Legacy BOT.'] ([transcript](transcripts/P62-7-run1.txt))
  - run 2 FAIL: refusal False; worn True; back in pack False; messages ['Welcome to Shattered Legacy BOT.'] ([transcript](transcripts/P62-7-run2.txt))
  - run 3 FAIL: refusal False; worn True; back in pack False; messages ['Welcome to Shattered Legacy BOT.'] ([transcript](transcripts/P62-7-run3.txt))
- **T-039 ERROR** (A new character is pointed at the board)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-039-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-039-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-039-run3.txt))
- **CREATE ERROR** (Character creation for every race and sex, through the real 0xF8 packet)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/CREATE-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/CREATE-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/CREATE-run3.txt))
- **T-047 ERROR** (Young by time played: the countdown, and 'I want to grow up!' brings the confirm gump)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-047-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-047-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-047-run3.txt))
- **D41 ERROR** (Regression: the Guild Directory lists each guild once)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/D41-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/D41-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/D41-run3.txt))
- **P56-6 ERROR** (Valorite refused at Mining 98.9, smelts at 99)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P56-6-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P56-6-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P56-6-run3.txt))
- **P56-4 ERROR** (Platinum refused at Mining 112.4; at 112.5 it smelts (about half the time))
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P56-4-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P56-4-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P56-4-run3.txt))
- **P61-3 ERROR** (Achievements: 'Oh Look, It's Dead' shows its Earned line and no 'Progress: 9/1'; unearned ones show progress)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P61-3-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P61-3-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P61-3-run3.txt))
- **P119-1 ERROR** (Five of cc-P119's ported creatures spawn, fight back and die to a player, leaving a corpse)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P119-1-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P119-1-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P119-1-run3.txt))
- **P129-1 ERROR** (Six of cc-P129's ported creatures spawn, fight back and die to a player, leaving a corpse)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P129-1-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P129-1-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P129-1-run3.txt))
- **P139-1 ERROR** (The body-route test creature spawns on body 2048, fights back with its bow and dies to a player, leaving a corpse)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P139-1-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P139-1-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P139-1-run3.txt))
- **P140-1 ERROR** (Six Rootdeep Burrows spawns appear on their bodies, fight back and die to a player, leaving a corpse)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P140-1-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P140-1-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/P140-1-run3.txt))
- **T-046 ERROR** (Reset stone and [ResetMyAccount open the same gump)
  - run 1 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-046-run1.txt))
  - run 2 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-046-run2.txt))
  - run 3 ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it ([transcript](transcripts/T-046-run3.txt))

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-17T16:53:00.312451183Z sha256:8e1a1916a7520a854b10e054d3fd8039b05b1a969bbef90a7ff35bdb977d669d"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-17T16:53:00.312451183Z sha256:8e1a1916a7520a854b10e054d3fd8039b05b1a969bbef90a7ff35bdb977d669d"}`
