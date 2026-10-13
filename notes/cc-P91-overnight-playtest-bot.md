# cc-P91 (overnight): a play-test bot that makes its own account and character

Prompt: `D:\UO\cc-prompts\cc-P91-overnight-playtest-bot.md`. Builder. Code in `D:\ShatteredLegacy\tools\playtest-bot\`,
triage in `testing\bot-triage.md`, the run in `testing\bot-runs\2026-10-13-1428\`. Not committed (autopilot commits after
DONE). Both repos were clean at the start.

## Headlines

- **HEAD does not boot.** The first build from the working tree (1,133 tests green) crashed at start:
  - `ImbueCatalogue`'s static initializer, from P82's Imbuing rework (90294a1), reads `SkillInfo.Table` before pinned's `SkillsInfo.Configure` fills it.
  - **The next deploy of HEAD to the test shard will crash the same way.** Proposed bug row 1.
  - So the bot ran on **36c7ae9 (P81)**, built in a detached worktree. The working tree was not touched.
- **Triaged: 164 open items:** 76 BOT, 15 BOT-PARTIAL, 8 EYES, 55 DEPLOY, 10 DECISION (`testing\bot-triage.md`, one line each).
- **Bot-able: 91.** Checks built: **20**, that is 18 play-test ids plus character creation and the D41 Guild Directory regression.
- **Result, each run 3 times: 20 PASS, 0 FAIL, 0 FLAKY.** One check's pass condition held but its statistic was meaningless on one run (P56-4, ore ran out), and it is fixed. A deliberate break proved the harness reports FAIL.
- **Soak: 120 minutes**, walker, miner and fighter: no exception, no crash, flat save times, 0 loud log lines. Memory rose 488 to 595 MB, and whether that is a leak is unverified.
- **Rule 1 held in the overnight run:** live and test containers had the same state, start time and image before and after.
  - **My one lapse was earlier, in the bot's own unit tests:** one red run may have opened a connection to the live shard on 2593 and sent a bogus game login. It is unverifiable, because live's docker log is empty, and the test is now fixed so it cannot happen. Section "Rule 1, and one thing I got wrong".
- **Email:** "Overnight play tests: 20 pass, 0 fail, 0 flaky" was sent through the autopilot's own settings, read only.
- **Repeatable:** `Run-OvernightPlaytests.ps1 -Commit 36c7ae9` (drop `-Commit` once HEAD boots). No scheduled task was registered; the command for one is under For Chase.

## 0. Chase's decision, and the proposed rewording

`docs\client-test-queue.md` says "Chase runs every one of these. No agent does, and no agent may." Chase has now asked
for a bot to run the ones it can, on a scratch world only. The bot never writes a Pass or Fail anywhere: it produces
evidence, and Chase marks. I did not edit `docs\`. Proposed rewording, for the overseer to place:

> **Chase decides every one of these. No agent marks a result.** Since cc-P91 an overnight bot
> (`tools\playtest-bot`) runs the ones a headless client can settle, on a scratch copy of the test world only, and
> leaves evidence in `testing\bot-runs\`. Most still need a server built from current source, which is a deploy
> decision and his alone; and anything about how it looks is his to see.

## The scratch world and its accounts

- **Code under test: commit 36c7ae9 (cc-P81), not HEAD.**
  - The first build from the working tree (HEAD 1644864) built and passed its 1,133 tests, then **crashed at boot**:
    `TypeInitializationException: The type initializer for 'Server.ImbueCatalogue' threw`,
    `IndexOutOfRangeException at Server.ImbueCatalogue.SkillRowName`, from `ClusterFImbueKnowledge.Configure()`
    (excerpt below).
  - The cause, read in source: `ImbueCatalogue`'s static initializer calls `SkillRowName`, which reads
    `SkillInfo.Table` (`server\customizations\ArtificersImbueGump.cs:511`).
  - That table starts empty (`Projects/Server/Skills.cs:451`) and is filled by pinned's `SkillsInfo.Configure`
    (`Projects/UOContent/Skills/SkillsInfo.cs:133-135`). `ClusterFImbueKnowledge.Configure`
    (`server\customizations\Imbuing\ClusterFImbueKnowledge.cs:96-98`) runs before it.
  - It came in with commit 90294a1, the Imbuing rework (P82). Only that commit touched `server\` or `docker\uo\`
    since 36c7ae9 (`git log 90294a1^..HEAD -- server docker/uo`).
  - So the run script gained `-Commit`. It builds from a detached worktree in `D:\UO\bot-shard\src`; the working
    tree is never touched.
  - Proposed bug-list row below. **The next deploy of HEAD to the test shard will crash the same way.**
- **Image:** `sl-modernuo:bot`, built by `docker/uo/build.sh -t sl-modernuo:bot` through all three gates (1,133 shard
  tests).
- **World:** a copy of the test world's newest automatic backup, `2026-10-13-19-25-00`
  (`server\lib\uo\modernuo-test\Backups\Automatic\`). The live `Saves` folder is never copied, because the test shard
  saves every 5 minutes and could be mid-save. The copy is in `D:\UO\bot-shard\world`, outside both repos, and is
  left in place after the run.
- **Configuration:** a copy of `Configuration-test` in `D:\UO\bot-shard\Configuration`, with these changes:
  - `listeners` set to `0.0.0.0:2595`;
  - `serverListing.address` set to `127.0.0.1`, and `serverName` to `Shattered Legacy BOT`;
  - `clusterf.testShard.allowAccountWipe` True (it was absent from Configuration-test).
- **Kept as they are, and recorded:**
  - `testCenter.enable` True; `testCenter.skillGainMultiplier` 5.0;
  - `clusterf.skillGain.amountMultiplier` 5;
  - `accountHandler.enableAutoAccountCreation` True (checked); `assistants.enableNegotiation` False (so there is no
    assistant kick); email disabled; no Discord webhook.
- **Accounts:** TestAccountWipe (cc-P73) did the wipe, from a request file in the console's own format
  (`New-WipeRequestText`, `New-WipePasswordHash`, dot-sourced from `Shard-Console.ps1 -LoadOnly`). Its three locks,
  all on the scratch shard:
  - `SL_SHARD_ROLE=test` in the bot's compose file;
  - `allowAccountWipe` True in the bot's Configuration copy;
  - no 2593 listener.
  - Its log line: `[AccountWipe] DONE: request bot-2026-10-13-1428-7429591e: deleted 7 accounts, 9 characters, 3348 items, 0 houses, 0 pets, 0 boats, 0 vendors, 0 guilds; kept 0 houses with no owner; admin 'slbot-admin' made (Owner); world saved; request removed`
  - `slbot-admin` (Owner) is the only account left.
  - The players `slbot-player` and `slbot-player2` to `4` are created by their first logins.
  - The passwords are random, live only in `tools\playtest-bot\secrets.local.json` (git-ignored, proved with
    `git check-ignore`), and are never printed.
- **Characters** are made through the real 0xF8 packet:
  - human, elf and gargoyle, male and female, checked by the `CREATE` check;
  - 18 characters are made in a run (15 for checks and 3 for the soak), across three accounts of 7 slots.
  - **Names are letters only.** The prompt's "Bot Human F 1" style is refused by the shard's name check, and the
    character is created as "Generic Player" (seen in a trial; the CREATE check now asserts the name survives).

Excerpt of the HEAD boot crash (`docker logs sl-modernuo-bot`, 13:35:23, first run):

```
[13:35:23 INF] Automatically detected client version 7.0.114.40
Error:
System.Reflection.TargetInvocationException: Exception has been thrown by the target of an invocation.
 ---> System.TypeInitializationException: The type initializer for 'Server.ImbueCatalogue' threw an exception.
 ---> System.IndexOutOfRangeException: Index was outside the bounds of the array.
   at Server.ImbueCatalogue.SkillRowName(SkillName skill)
   at Server.ImbueCatalogue.AddSkill(SkillName skill, Int32 slot, ImbuableItem applies, String family, Func`2 allows)
   at Server.ImbueCatalogue..cctor()
   ...
   at Server.ClusterFImbueKnowledge.Configure()
This exception is fatal, press return to exit
```

## Rule 1, and one thing I got wrong

**The real shards were never started, stopped, built or written.** Every run records both containers' state, start
time and image before and after; this run's before and after are in the report. The bot's compose file, project,
container, image, port and folders are all its own, and `Assert-Rule1` reads the compose file and refuses anything
else.

**My mistake, during the bot's own unit tests (not the overnight run):**
- The first version of the relay-refusal test had its fake login server relay the client to **127.0.0.1:2593**, the
  live shard's real published port.
- To prove the test goes red, I disabled the target check on purpose and ran the tests once.
- In that one run, the client **may have opened a connection to the live shard and sent a game-login packet (0x91)
  with an auth id that does not exist.** Live would reject that ("Invalid auth id"); nothing could log in.
- In the same run, a second test's stand-in passed its call through to the real `socket.create_connection`. So it
  may also have opened a bare TCP connection to 2593 and 2594, sending no data.
- **Unverified whether any of it arrived:** `docker logs sl-modernuo` is empty for the last 24 hours, so it shows
  nothing either way. Live's start time and state were unchanged afterwards.
- **Fixed:**
  - the relay test now names a dead local port;
  - both tests replace `socket.create_connection` with a guard that refuses everything except the fake server;
  - the red run was repeated with the check disabled, and the only connection attempted was to the dead local port,
    which the guard refused.
- The comment in `tests\test_bot.py` says why.

## Triage

`testing\bot-triage.md`: all 164 open items (163 open, 1 blocked), one line each, in exactly one bucket.

| Bucket | Items |
|---|---|
| BOT | 76 |
| BOT-PARTIAL | 15 |
| EYES | 8 |
| DEPLOY | 55 |
| DECISION | 10 |

- **Method.** A first pass was made by an agent with the bucket rules and the bot's abilities written out. I read
  every BOT and BOT-PARTIAL line against the play tests, and checked the count by script: 164 rows, 164 unique ids,
  matching `play-tests.json`.
- **My changes:** P82-0 is marked "could not run: the code with P82 does not boot".
- **The prompt's guesses:**
  - BOT or BOT-PARTIAL: T-002, T-004 to T-007, T-010, T-024 to T-027, T-039, T-041, T-042, T-045 to T-048.
  - **T-051, T-055 and T-056 are not open** in `play-tests.json` (already settled), so they are not in the triage.
  - D41 got a regression check of its own.

## The bot

`D:\ShatteredLegacy\tools\playtest-bot\`. Python 3, standard library only. `README.md` there has the layout, the
login sequence and a citation table for every packet the bot sends or reads.

- **Login:** as a 7.0.117.0 client with no encryption: 0xEF seed, 0x80, 0xA8, 0xA0, the 0x8C relay (checked against
  127.0.0.1:2595), a raw 4-byte seed, 0x91, then the Huffman-compressed game connection.
- **Actions:** create characters (0xF8), play (0x5D), walk (0x02, tracking the move sequence), speak (0xAD), single and
  double click, war mode and attack, lift and drop, equip, answer targets (0x6C) and gumps (0xB1), and ask for status
  and skills (0x34).
- **What it reads:** gumps (0xDD; pinned never sends 0xB0), ASCII, Unicode and cliloc messages (0x1C, 0xAE, 0xC1,
  0xCC, with text from the client's own Cliloc.enu), status v6, skills, containers, world items, mobiles, properties
  (0xD6) and the character list.
- **Every layout is checked against pinned**, with file:line in the README. An agent collected the first table; I
  re-read the key ones in source, among them the 0xF8 offsets (`IncomingAccountPackets.cs:90-139`), the Huffman
  encoder and its per-packet terminal code (`NetworkCompression.cs:30-163`, `NetState.cs:658-660`) and GameLogin.
- **Two things only the running shard showed:**
  - 0xF4 is **ours**, the ClusterF exploration packet (`ClusterFExplorationManager.cs:121-134`), not pinned's;
  - `Cliloc.enu` is BWT-compressed. So `uobot\cliloc.py` ports pinned's `BwtDecompress.cs` and the reader in
    `Localization.cs:97-140`: 123,489 entries, cached in `D:\UO\bot-shard\cache`.
- **Framing is self-checking.** Each compressed chunk is exactly one packet, and every packet whose length disagrees
  with the table is logged as `FRAMING` and counted. This run: 0 framing mismatches and 0 parse errors across all 62 transcript files.
- **Safety** (`uobot\safety.py`): host `127.0.0.1` and port `2595` only, and the relay must say the same; anything else
  disconnects and aborts. `tests\test_bot.py` has 9 facts: 4 for the refusal, 2 for Huffman, 3 for packet layouts.
  - All green. With the check broken, all 4 refusal facts went red, and no real port was dialled (see Rule 1 above).
- **Checks:** `uobot\checks.py`, one function per play-test id, citing the code under test for every string it asserts.
  - Each check runs 3 times; transcripts go to `transcripts\<id>-run<n>.txt`.
  - 3/3 is PASS, 0/3 FAIL, anything else FLAKY, and ERROR when it could not be set up.
  - Fresh characters rotate over three accounts, each resting 5.5 minutes: a player character stays in the world for 5
    minutes after it leaves (`Region.cs:200`) and blocks its account until then.
- **World-changing order:** the checks only add items and characters (ore, a forge, a rat, the stone, the Kitsune
  item); none runs a seeder, `[GenerateSpawners` or a reset. So no check can spoil another, and the world copy is not
  restored between groups. The world is copied fresh for every run.

## Results

Run `testing\bot-runs\2026-10-13-1428\` (14:28 to 16:56), code 36c7ae9, `-Runs 3`, `-SoakMinutes 120`, email sent.
**20 checks: 20 PASS (3/3 each), 0 FAIL, 0 FLAKY, 0 could not run.** The report, `results.json`, `email.txt` and the 62 transcript files (60 check runs, the session and the soak; 4.1 MB) are in the run folder. The shard's own logs and the build log are git-ignored (`testing/bot-runs/*/*.log`).

All 20 passing is not proof that the checks can fail:
- Two of them did fail on the way, for real reasons in my own checks, before they were right. P61-3 first matched the wrong row and its player never attacked; P62-1 targeted from out of range.
- After the run, P62-7 was broken on purpose (it expected "Only males can wear this."). It reported **FAIL 0/2**, the summary said "1 pass, 1 fail", and the script exited 1. Then it was restored, `cmp`-identical (scratchpad run 2026-10-13-1657).

| Id | Kind | Result | Evidence (last of 3 runs) |
|---|---|---|---|
| P64-1 | BOT | PASS 3/3 | title 'Shattered Legacy 2026.10.13.4'; All patch notes button yes; wiki text none |
| P64-2 | BOT | PASS 3/3 | history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run) |
| P64-3 | BOT-PARTIAL | PASS 3/3 | first heading 'Shattered Legacy 2026.10.13.4'; (you are here) on page 1: True |
| P64-4 | BOT | PASS 3/3 | last page ['Page 25 of 25']; last version 2026.10.01; after Previous ['Page 24 of 25'] |
| P58-0 | BOT-PARTIAL | PASS 3/3 | versions 10.02-10.05 shown: ['2026.10.05.3', '2026.10.05.2', '2026.10.05', '2026.10.04', '2026.10.03', '2026.10.02']; missing none; Staff list visible to a player: False |
| P61-5 | BOT | PASS 3/3 | 2026.10.05.2 present: True, 4 player lines (CHANGELOG at the code under test: 4) |
| P64-5 | BOT-PARTIAL | PASS 3/3 | matching line: 'thril to 187.5, Adamantium and Celestial to 200. The chance to make the item is unchanged.' |
| P71-7 | BOT | PASS 3/3 | 2026.10.10 present: True, 5 player lines (CHANGELOG at the code under test: 5) |
| P64-6 | BOT-PARTIAL | PASS 3/3 | admin sees 'Staff (players do not see this list)': True; player sees it: False |
| P66-7 | BOT | PASS 3/3 | reply: 'ClusterF skill gain: rate enabled, 3 chance attempt(s), 5x gain amount; past stock ceilings on.' |
| P62-1 | BOT | PASS 3/3 | worn: True (layer 18); messages ["To see the commands to do this just say 'help'."] |
| P62-7 | BOT | PASS 3/3 | refusal True; worn False; back in pack True; messages ['Only females can wear this.', 'Welcome to Shattered Legacy BOT.'] |
| T-039 | BOT-PARTIAL | PASS 3/3 | gargoyle female at (3503, 2574, 14): message None; welcome gump says 'The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.'; the board is 1 tiles away |
| CREATE | HARNESS | PASS 3/3 | gargoyle male: body 666 (want 666), status name 'Bot Gargoyle M A' (asked for 'Bot Gargoyle M A'), at (3503, 2574, 14) |
| T-047 | BOT | PASS 3/3 | countdown 'You will enjoy the benefits and relatively safe status of a young player for another 13 days and 23 hours of play time. Say "I want to grow up!" to give it up sooner.' (days and hours: True); confirm gump: ['', "Reno... |
| D41 | BOT | PASS 3/3 | 18 rows, header says 18 guilds, 18 way buttons; duplicates none; Artificers' Order 1 time(s) |
| P56-6 | BOT | PASS 3/3 | at 98.9: refused True ['You have no idea how to smelt this strange ore!'], ore left 10; at 99.0 over 6 tries: refused 0, smelted 3, burned 3 |
| P56-4 | BOT | PASS 3/3 | at 112.4: refused True ['You have no idea how to smelt this strange ore!'], ore left 10; at 112.5 over 8 tries: refused 0, smelted 1, burned 1 |
| P61-3 | BOT | PASS 3/3 | rat killed by the player: True; row 'Oh Look, It\'s Dead [5 AP / 5 R]"You are, by definition, a killer now. Congratulations."(Earned: slew your first creature)'; other rows with progress: 2 |
| T-046 | BOT-PARTIAL | PASS 3/3 | same gump type True; same text True (29 lines); same buttons True [0, 1, 2, 10] |

**Read with care:**
- **P56-4's third run counted only 2 of 8 tries at 112.5.** The ore pile ran down to 1, and a pile needs 2 ("There is not enough metal-bearing ore in this pile", 501987). The pass condition, refused at 112.4 and smelting at 112.5, held all three times, but the "about half" ratio that run is meaningless.
  - Fixed after the run: the check tops the pile up below 2, and counts that message separately.
  - Verified on the follow-up run: 5 smelted and 3 burned, then 6 and 2, out of 8. That is about 70%, not about half, on 16 tries; the play test's "about half" is a feel, and Chase decides.
- **T-039 passed on the welcome gump's sentence**, "The Guild Board in the town square lists every guild...". The separate "Follow the arrow to the Guild Board" message (`ClusterFGuildStarterPath.cs:768-780`) did not arrive within 12 s on any run. It is sent from the welcome gump, which the bot does not press. New characters start one tile from the board, (3503, 2574) against (3502, 2573).
- **T-047** gives "13 days and 23 hours". The play test asks for days and hours against 336 hours: 13 days 23 hours is 335 hours, under the 336; why it is one hour short of a fresh account's 336 was not checked. The confirm gump arrived each time, and the bot closed it without renouncing.
- **P58-0, P64-3 and P64-5 to P64-6** read `[version` at 2026.10.13.4. Their expected counts were checked against the CHANGELOG at 36c7ae9: 2026.10.05.2 has 4 player lines and 2026.10.10 has 5, matching the play-test text.


## The soak

Three bot characters for **120 minutes**, all at once, while the harness sampled the container every minute:
- a human walker on a loop through New Haven's square;
- a gargoyle miner digging at Mining 100;
- an elf fighter at Swords, Tactics and Anatomy 100 with a broadsword, killing the mongbats the admin spawned beside it.

| Measure | Value |
|---|---|
| Activity | 22699 steps, 3514 digs, 1695 mongbats killed (1697 attacks) |
| Container | running at every one of 117 samples; never restarted |
| Memory | 488.4 MB at the start, 594.9 MB at the end (594.9 MB at most): about +0.9 MB a minute, steadily |
| World saves | 31 in the run, each 0.54 to 0.72 s, flat from first to last (`Writing world save snapshot done`) |
| Loud log lines | **0** (Exception, Error, crash, save failure; the whole `shard.log` also has 0 lines with "exception" or "error") |
| Bot problems | none (the threads reported no errors) |

**What it means, and what it does not:**
- No crash, no exception and no save trouble in two hours under constant fighting and walking.
- Memory rose 106 MB over the run without levelling off. The flat save times say the world was not piling up items (corpses decay).
- **Whether the memory rise is a leak or the .NET heap still growing toward its working size is unverified.** Two hours is too short to tell. A longer soak, or `[LoopStats` and GC counts, would settle it.
- **The miner never found ore:** it digs at its own feet in New Haven's square, so every dig was "you can't mine there" and nothing was smelted. **There was no Make X batch.** Both are weaker than the prompt asked; see Deviations.


## Proposed bug-list rows

1. **HEAD crashes at boot: `ImbueCatalogue`'s static initializer reads `SkillInfo.Table` before pinned fills it.**
   - **Kind:** ours to fix. Proved by the boot log above, and by the same scratch setup booting cleanly from 36c7ae9.
   - **Reverses when:** `ClusterFImbueKnowledge` builds its defaults after `SkillsInfo.Configure`. For example, move its
     work from `Configure` to `Initialize`, or make `ImbuingTable.Defaults` and `SkillRowName` lazy.
   - **Reaches:** every boot of every build from 90294a1 (P82) on, both shards.
   - The build gate did not catch it, because the tests never run the Configure order with the real data files; see
     the next row.
2. **No test boots the shard's Configure and Initialize order.** 1,133 green tests sat over a server that cannot start.
   - **Kind:** ours, a gap in the gate.
   - **Reverses when:** a build gate starts the built image against an empty world and waits for "Listening". The
     bot's `Run-OvernightPlaytests.ps1` does exactly this and caught it first.
3. **Not a bug, a note: a character name with a digit is refused, and the character is made as "Generic Player" with no message.** It is ModernUO's name check; a real client refuses such names before sending. Recorded so nobody reads the bot's "Generic Player" characters in an older trial as a fault.

## Deviations and decisions for Chase

1. **The rule in `client-test-queue.md`.** The proposed rewording is in section 0 above. The overseer places it; I did
   not edit `docs\`.
2. **The run tested 36c7ae9 (P81), not HEAD,** because HEAD does not boot (bug row 1). Items from P82 on wait for that
   fix. Once it lands, run without `-Commit`.
3. **Checks built: 18 play-test ids plus 2 of the bot's own, out of 91 BOT and BOT-PARTIAL items.** I stopped adding
   checks to leave the night for a clean three-times run and the two-hour soak, as the prompt asks. The other 73 have
   sketches at the end of `bot-triage.md`.
4. **The bot cannot speak in keywords,** so vendors, bankers and keyword NPCs ignore it (commands and plain speech
   work). That rules out T-041, T-042, P56-1 to P56-3 and P69-1 as written, until keyword speech is added: it needs
   the speech keyword table from the client data.
5. **The soak's miner digs at its own feet** (no ore there, so no smelting) and there is no Make X batch. A better soak
   would teleport the miner to a mine.
6. **Transcripts are committed:** about 4 MB a night across about 60 files, each well under 5 MB. If that growth
   matters, ignore `testing\bot-runs\*\transcripts\` and keep only report.md and results.json.
7. **The scratch shard's client data is 7.0.114.40** (it said "Automatically detected client version 7.0.114.40") while
   the bot announces 7.0.117.0, which Configuration-test's `minRequired` asks for. A real 7.0.117.0 client against
   these data files is what Chase plays, so that matches.

8. **A registered git worktree.** `-Commit` leaves `D:\UO\bot-shard\src` (36c7ae9, detached) registered in the shard
   repo (`git worktree list`). It holds no changes, and the next `-Commit` run replaces it. To remove it:
   `git -C D:\ShatteredLegacy worktree remove --force D:\UO\bot-shard\src`.
9. **Watching `run.log` while the bot runs.** Git Bash's `tail -f` holds it open so that the script cannot append. That
   is how this run's `run.log` lost its lines from 14:29 to the end, a mistake of mine while watching it. The
   script's console output, `report.md`, `world.json` and `shard-start.log` carry the same facts. Watch with
   PowerShell's `Get-Content -Wait`, which shares the file, or do not watch it.

## For Chase

**Running the bot again, on any night:**

```
powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\tools\playtest-bot\Run-OvernightPlaytests.ps1 -Commit 36c7ae9
```

Drop `-Commit 36c7ae9` once HEAD boots again. `-Only T-047,P64-1` runs just those, `-SkipSoak` skips the two hours,
and `-NoEmail` keeps it quiet.

**A scheduled task, if wanted** (not registered by this task):

```
schtasks /Create /TN "SL overnight play tests" /SC DAILY /ST 01:30 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\tools\playtest-bot\Run-OvernightPlaytests.ps1"
```

**Reading a run:**
- `testing\bot-runs\<stamp>\report.md`: the headline, one row per check with its evidence and transcript links, then
  every run of every Fail, Flaky and could-not-run.
- `results.json` is the same, as data.
- The emailed subject is "Overnight play tests: N pass, N fail, N flaky".

**Left for Chase (already on the play-test page; the bot settled the other half):**

- P64-3: the current version's entry shows gold (the bot saw "(you are here)" on page 1).
- P58-0: the patch-note wording reads right (the bot saw 2026.10.02 to 10.05 and no Staff list for a player).
- P64-5: the 2026.10.05.2 line wraps onto four rows (the bot saw the line's text and ending).
- P64-6: the staff list shows lavender (the bot saw it for staff and not for a player).
- T-039: a new player can find the board by eye (the bot saw the welcome sentence and the start one tile away).
- T-046: each scope clearing what it says, joined guilds included (the bot compared the two gumps only, and pressed nothing).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run after the notes were
written:

```
Repo Result
---- ------
code dry run
docs dry run
```

**Pending in the code repo:**
- `.gitignore`, `CHANGELOG.md`, `VERSION`;
- `tools/playtest-bot/`: README, the two scripts, the compose file, `uobot/*.py`, `tests/test_bot.py`.
- `secrets.local.json`, `cache/` and `__pycache__/` are ignored (`git check-ignore` proved each).

**Pending in the docs repo:**
- `.gitignore`, these notes, `testing/bot-triage.md`;
- the run folder: report, results, email, world and real-shard JSON, and 62 transcripts. Its `*.log` files are ignored.
- No file in the run folder contains either bot password (checked by script).

**Patch notes:** `CHANGELOG.md` 2026.10.13.12 `### Staff` line (2026.10.13.11 was committed with P90), and `VERSION`
2026.10.13.12. The wiki page was not published.

P91 DONE
