# cc-P223: the play-test bot gets checks for the first half of the "Not built yet" items, run tonight on this PC

Builder: the Gold Golem (Claude, Fable), 2026-10-20 night to 2026-10-21, on the Gold PC (STEPHS-DESKTOP), branch
`golem/Gold/P223` in both repos. Pinned `D:\UO\ModernUO-pinned` at `d4531cd94`. Main at the start was `83b1f97`
(the test shard and the bot's scratch shard were both built from the working tree at that commit; the bot's own
files are the only change on this branch, so the code under test is main's).

## Headlines

{{HEADLINES}}

## 1. The shard (part 1)

- `test-shard` and `docker-build` locks taken (`Use-GolemLock.ps1`), held through the night's runs, released at the end.
- `docker\uo\Start-TestShard.ps1 -Fresh`: the test save wiped, accounts seeded from this PC's `modernuo\Saves\Accounts`,
  current main built through the gates (1662 tests, 1658 passed, 4 skipped) as `sl-modernuo:latest`, the test shard
  up on 2594 and healthy, tagged `sl-modernuo:good-83b1f97`. It is **left running** for the night (part 5).
- **Where the bot ran.** The bot's rule 1 (`uobot/safety.py`, proven by `tests/test_bot.py`) refuses every host and
  port but `127.0.0.1:2595`: never the live shard (2593) and **never the real test shard (2594)**. The prompt's
  "the bot connects to this PC's own test shard only (127.0.0.1, the test port)" was read as that rule: the checks
  ran on the bot's own scratch shard, `sl-modernuo-bot` on 127.0.0.1:2595, a copy of the fresh test world's first
  automatic backup (`2026-10-21-03-05-00`) with the bot's accounts, built from the same working tree by
  `Run-OvernightPlaytests.ps1`. Nothing of the bot's ever touched 2594; the runner records both real shards'
  state before and after and says "rule 1 held".
- The fresh test world is empty of our seeded content until the seeders run: the checks that need it seed it on the
  scratch copy themselves (`[ClusterFSeedNewHaven missing`, `[ClusterFSeedMineCamp`, `[GenerateSpawners <file>`).

## 2. The checks (part 2)

{{CHECKS}}

## 3. The run (part 3)

{{RUN}}

## 4. Failures (part 4)

{{FAILURES}}

## 5. Chase's to play, by place

{{CHASE}}

## 6. Not built tonight, and why

{{NOTBUILT}}

## 7. Draft fix prompts

{{PROMPTS}}

## 8. Files changed

{{FILES}}

## 9. Commit preflight

{{PREFLIGHT}}
