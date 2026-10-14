# cc-P106: the Shard Console shows when a shard is waiting for an answer, and lets Chase answer it

2026-10-14. Console code in `D:\ShatteredLegacy`. Prompt: `D:\UO\cc-prompts\cc-P106-shard-questions.md`. Not committed
(autopilot commits after DONE). Both repos were clean at the start, apart from the play-test importer's machine output.
**Live (`sl-modernuo`) was only ever read** (docker inspect and logs). It is still at D94's question, untouched, up
since 08:06. The test shard (`sl-modernuo-test`) was not touched either.

## Headlines

- **The console now sees D94.** Read from the real Docker just now (read only), the LIVE tile says:
  **`WAITING FOR AN ANSWER`** (amber): `Delete the object and continue? (y/n/a) Server.ClusterFAccountPersistence
  0x40128E03: ArgumentOutOfRangeException at System.DateTime.ThrowTicksOutOfRange(), since 08:06 (Shard question tab)`.
- **Why nobody saw it:** the prompt is `Console.Write` with no newline, and docker logs records a line only once it
  ends. So the question itself is never in `docker logs`. The reader recognises each question by what is printed
  before it, on a running container that has been silent for 20 s (`Get-ShardQuestion`).
- **Every console read pinned ModernUO makes at start, with what each answer does,** is in the table below. Six are
  recognised: bad object, bad file, missing type, the fatal "press return to exit", the owner-account prompt, and the
  restore-a-backup menu.
- **The health check never calls a waiting shard healthy.** `Get-HealthState` says `WAITING` whatever Docker's check
  says, and `Start-TestShard.ps1`'s wait stops with the question instead of timing out.
- **One email per question**, subject `[Shard] Live is waiting for an answer: <question>`. It goes through the
  **Golem's mail path** (its `email.json` and DPAPI `smtp-cred.xml`, read only, as `Send-BotReport.ps1` does), from the
  console's refresh and from `-Status`. Sent questions are remembered in `%LOCALAPPDATA%\ShardConsole\question-mail.json`.
  **No email has been sent yet:** live's D94 email goes out the first time the console (or `-Status`) runs against Docker.
- **A new Shard question tab, for both shards:** the question, what failed, the error and its first frames, and one
  button per allowed answer, each explained. Also Show the question and Stop the shard.
  - The typed phrase: `answer live` or `answer test` for n and Enter; **`delete on live` or `delete on test`** for y and
    a; `stop live` or `stop test` for Stop.
  - A delete answer first says what is lost (for D94: every account's ClusterF data), then **backs up the save** to
    `Snapshots\<shard>\<time>_pre-answer-<key>` and verifies it, and only then sends.
  - Every answer re-reads the question just before sending and refuses if it changed.
  - Every answer and Stop is logged with who, when, the question and the answer, and honours `-DryRun`.
- **How the answer reaches the process:** the Docker engine API on its named pipe (`\\.\pipe\docker_engine`): attach
  with stdin only, write the keys and Enter, close. Nothing stays attached. `docker attach` itself refuses scripted
  input on a tty.
- **No compose change was needed, on test or live:** both compose files already have `stdin_open: true` and `tty: true`
  (`docker-compose.yml:30-31`, `docker-compose.test.yml:56-57`, and `docker inspect` shows `OpenStdin=true Tty=true` on
  both). Live needs no recreate for this.
- **Proven on the real Docker** on a scratch shard: the test shard's image (`sl-modernuo:good-61db33c`), a copy of the
  test world with one object broken on purpose, its own compose project on loopback 2596. Three runs:
  - `n`: the server printed "Deserialization failed" and reached "press return to exit". Then Enter: it shut down.
  - `y`, on `ClusterFAccountPersistence` itself: the save was backed up (25 files, 29,609,081 bytes, verified), the
    object was deleted, and the shard loaded and listened.
  - Stop: `docker stop -t 60`, exit 0.
- **Facts: 281 of 281** (264 before plus 17 new, every new one seen failing first; three existing facts changed for the
  new tab, see Tests).

## What each console question is (pinned ModernUO, `D:\UO\ModernUO-pinned\Projects`)

| Kind | Where | What it prints first (visible in `docker logs`) | The question (not visible) | Answers |
|---|---|---|---|---|
| object | `Server/Serialization/GenericEntityPersistence.cs:756-771` | `***** Bad deserialize of <Type> (<serial>) *****`, then the exception or `Serialized object was N bytes, but M bytes deserialized` | `Delete the object and continue? (y/n/a)` | **y** deletes that object and loads on. **a** deletes it and every later bad object in that file without asking. **Anything else** throws "Deserialization failed.", and the load ends at the fatal line below |
| file | `GenericPersistence.cs:123-130`, `AdhocPersistence.cs:101-107` | `***** Bad deserialize of <file path> *****`, then the exception | `Skip this file and continue? (y/n)` | **y** skips the file (what it held is gone at the next save); anything else throws, as above |
| type | `GenericEntityPersistence.cs:399-415` | `failed` | `Error: Type '<name>' was not found (or marked abstract). Delete all of those types? (y/n)` | **y** drops every saved object of that type; anything else throws "Bad type" |
| fatal | `Server/Main.cs:433-434` | `This exception is fatal, press return to exit` (a full line, so visible) | (that line) | Any line ends the process (`DoKill`). Live (`restart: unless-stopped`) is started again by Docker; the test shard (`restart: "no"`) stays stopped |
| owner | `UOContent/Misc/AccountPrompt.cs:15-31` (only with no accounts) | `Do you want to create the owner account now? (y/n):` | (that line) | **y** asks a username and a password at the console (not sent from the panel); anything else goes on with no accounts |
| restore | `UOContent/World Saves/AutoArchive.cs:230-389, 454-510` (only with no valid save) | `Available backups and archives (...)` and the list | `... or Enter to start fresh:` / `[1]>` | A number restores that backup; Enter starts with no world. **Only Stop is offered**: choosing a backup is done at the console |

`UOContent/Engines/Pathing/PathCacheCommands.cs:73` also reads the console, but only after a staff command, never on
its own, so it is not watched. `ConsoleInputHandler.ReadLine` (`Server/Console/ConsoleInputHandler.cs:153-168`) is the
read for all but the restore menu. In headless mode it throws instead of waiting.

## What changed, with file:line

`D:\ShatteredLegacy`:

| File:line | What |
|---|---|
| `scripts/Shard-Health.ps1:100` | `Get-HealthState -Question`: `WAITING` for any question but a fatal (which stays `CRASHED`) |
| `scripts/Shard-Health.ps1:205-357` | The table above as comments; `$script:QuestionPrompts` :228; `Get-QuestionAnswers` :237 (the answer table, safe answer first, `Deletes` marked); `ConvertFrom-StampedLog` :267; `Get-ShardQuestion` :280 (the current run only, from the last `[SL] Starting`; quiet for `QuietSeconds`; kind, prompt, type, serial or file, exception, frames, since, signature, answers); `Get-QuestionLine` :335; `Test-QuestionStillAsked` :348; `Get-AnswerKeystrokes` :354 |
| `scripts/Shard-Console.ps1:162` | `$script:D94Loss`, what a delete answer to D94 loses |
| `scripts/Shard-Console.ps1:283-287` | Config: `QuestionQuietSeconds` 20, `QuestionTailLines` 80, `QuestionMailFile` |
| `scripts/Shard-Console.ps1:1899,1911` | `fix-test-shard.json`'s new `questionLosses` (default: D94's) |
| `scripts/Shard-Console.ps1:4906-4909` | A new section, `logtail <container>` (`docker logs -t --tail 80`); `-Capture` drops account lines from it as from `logs` |
| `scripts/Shard-Console.ps1:2634` | Each shard's `Question` in the state |
| `scripts/Shard-Console.ps1:2826-2840` | The tile: amber `WAITING FOR AN ANSWER` with the question in one line; a fatal stays red `CRASHED` and says it waits |
| `scripts/Shard-Console.ps1:2851, 2865, 2890, 2905` | `Get-QuestionLoss`, `Get-QuestionText` (panel, Show, email), `Get-QuestionMails` (one per new signature), `Get-QuestionPlan` (show, n, y, a, enter, stop) |
| `scripts/Shard-Console.ps1:952-957, 1170-1179` | The six actions (group `Shard question`) and their tooltips |
| `scripts/Shard-Console.ps1:2137` | Dispatch of `question.*` |
| `scripts/Shard-Console.ps1:1345, 2523` | The new plan step `answer` (with a `Signature`), and how a dry run prints it |
| `scripts/Shard-Console.ps1:2375-2397` | The safety check for `answer`: only to a shard's container, only n, y, a or Enter, only after its phrase. y and a only after `delete on <shard>` and a verified copy of that shard's save under `Snapshots\<shard>\` |
| `scripts/Shard-Console.ps1:5172-5185` | The runner's `answer`: reads the question again, refuses if changed, sends, prints what the shard said in the next 10 s |
| `scripts/Shard-Console.ps1:4610, 4619, 4650, 4669` | `Get-ShardQuestionNow`, `Send-ContainerInput` (the engine API pipe), `Send-ConsoleMail` (the Golem's mail path), `Invoke-QuestionMail` (docker-read states only, never a capture or `-DryRun`) |
| `scripts/Shard-Console.ps1:6163, 7758` | Mail from the refresh and from `-Status` |
| `scripts/Shard-Console.ps1:6464, 7172` | `Update-QuestionPanel` and the tab (LIVE or Test radio, the text, six buttons; only the question's answers enabled) |
| `docker/uo/Start-TestShard.ps1:206-210, 227-233` | The wait stops on a question, with the question and the tab named |
| `scripts/fix-test-shard.json` | `questionLosses` |
| `scripts/tests/Shard-Console.Tests.ps1` | 17 `P106_*` facts, the question states, the window cases, the tab list |
| `scripts/tests/fixtures/live-shard-question-d94-2026-10-14.txt` | Live's real `docker logs -t --tail 60`, two account lines dropped (`Remove-AccountLines`) |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.12, one `### Staff` line |

## Tests

Runner: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`.

**Red first:** the 17 new facts against the unchanged console: `17 facts, 0 passed, 17 failed`.

The facts by what the prompt asked:

| Asked | Fact |
|---|---|
| detection: the deserialize prompt (D94's real log) | `P106_TheD94LogIsADeserializeQuestionWithItsTypeSerialExceptionAndFrame` |
| detection: fatal "press return", and none (healthy start) | `P106_TheFatalPressReturnIsAQuestionAndAHealthyStartAsksNothing` |
| no false question: still printing, stopped, no log, already answered | `P106_AShardStillTalkingOrStoppedIsNotWaiting`, `P106_AnAnsweredQuestionIsNoLongerWaiting` |
| the other kinds (file, type, owner, restore) | `P106_EveryStartupQuestionIsKnownByWhatItPrints` |
| the answer table | `P106_TheAnswerTableSaysWhatEachKeyDoesAndWhichDelete` |
| the typed phrase for delete answers, and the backup before them | `P106_DeleteAnswersNeedTheTypedPhraseAndAVerifiedBackupFirst`, `P106_TheSafetyCheckRefusesADeleteAnswerWithoutItsBackupOrPhrase` |
| the other answers' and Stop's phrases; refused answers | `P106_OtherAnswersAndStopNeedTheirOwnPhrase`, `P106_AnAnswerTheQuestionDoesNotOfferIsRefused` |
| the tile text and colour | `P106_TheTileSaysWaitingForAnAnswerInAmberWithTheQuestion` |
| the health check | `P106_TheHealthCheckNeverCallsAWaitingShardHealthy` |
| one email per question | `P106_OneEmailPerQuestion` |
| the answer goes only to the same question | `P106_TheAnswerIsSentOnlyIfTheQuestionIsStillTheSame` |
| Show reads only | `P106_ShowPrintsTheQuestionItsContextAndEveryAnswerAndChangesNothing` |
| `-DryRun` for each button | `P106_EveryQuestionButtonRunHeadlessWithDryRunRunsNothing` (the real child process, five buttons, against a capture with D94 in it), plus the existing click facts, which now include all five window buttons on both shards |
| tab, phrase, tooltip | `P106_EveryQuestionButtonIsOnItsOwnTabWithAPhraseAndATooltip` |

**Getting to green.** The first runs failed for my own mistakes, each fixed:

- I read plain fixtures with `Read-Fixture`, which parses capture files. I now read them as text.
- Two PowerShell array traps in the answer table: a one-row table unrolled into its fields, and `,` binds tighter than
  `+`, so an explanation split in two. The rows now go in one at a time with `List.Add`.
- The headless fact's "no REFUSE" check was case-insensitive and matched the COPY line's "refuses if the target exists".
  It now looks for a REFUSE step.

Then the full suite: 5 existing facts failed on the new tab, all fixed:

- `TheFormBuildsFromACaptureWithoutBeingShown`: the tab list now includes Shard question.
- The three click facts: they run every window action. `question.*` now gets states where each shard is asking (D94;
  the fatal one for Enter).
- `P84_EveryControlInTheWindowHasATooltip`: the tab and its three controls now have tooltips.

**Final: `281 facts, 281 passed, 0 failed`**, run again after the last edit. `Start-TestShard.ps1` parses (0 errors).

### The real proof (Docker on this PC, a scratch shard)

- **The scratch shard** (`D:\UO\question-proof\`, outside both repos):
  - compose project `sl-uo-qproof`, container `sl-modernuo-qproof`, the test shard's image `sl-modernuo:good-61db33c`;
  - `127.0.0.1:2596` only, `restart: "no"`, `stdin_open` and `tty` as both real shards have;
  - a copy of the test world's newest automatic backup (2026-10-14 19:00) and of `Configuration-test`, set to 2596.
- **Breaking it:** a scratch script shortened one entity's recorded length in the copy's `Items.idx` by one byte (one byte
  changed, `cmp`). That makes ModernUO report "Serialized object was N bytes, but M bytes deserialized" and ask the
  y/n/a question.
  - The first try parsed the type index as 4 bytes; it is 2 (`DeserializeIndexesV4`, `ReadUShort`). So it changed a
    neighbouring record and broke a `Server.Items.Gold`. That is still a real bad deserialize, so it served for the
    `n` run.
  - The second try broke `Server.ClusterFAccountPersistence` itself, D94's type.
- **The console's own functions** (`D:\UO\question-proof\Proof.ps1`) ran with the test shard's container, save folder,
  snapshot root, log and mail file pointed at the scratch ones; live is only read.

| Run | What the console showed | Answer | What happened |
|---|---|---|---|
| A | tile `TEST : WAITING FOR AN ANSWER [amber] Delete the object and continue? (y/n/a) Server.Items.Gold 0x40019EA5: Serialized object was 31 bytes, but 8 bytes deserialized, since 14:02`; health `WAITING` (Docker had no health check on it); panel n/y/a; mails "Live ..." and "Test ..." (not sent) | `n` (`answer test`) | The shard echoed `...(y/n/a): n`, printed `System.Exception: Deserialization failed.` and `This exception is fatal, press return to exit` |
| A | tile `CRASHED AT START [red]`, panel: Enter only | Enter (`answer test`) | `Shutting down`, exit 139, stayed stopped |
| B | tile `WAITING FOR AN ANSWER ... Server.ClusterFAccountPersistence 0x40000270`; the panel said a delete loses every account's ClusterF data | `y` (`delete on test`) | Backed up to `Snapshots\test\20261014-190513_pre-answer-y`, **25 files, 29,609,081 bytes on both sides**, then sent. `Loading world done (206901 items ...)`, one item fewer; `Listening: 127.0.0.1:2596`. It also wrote `Saving world done` within a second of starting, so a delete is on disk at once |
| B | (running) | Stop (`stop test`) | `docker stop -t 60 sl-modernuo-qproof`, exit 0, checked not running |

The scratch log (`D:\UO\question-proof\shard-console.log`) has one START and one DONE line per action, with the user, the
question and the answer. The scratch container and its network were removed afterwards with
`docker compose -p sl-uo-qproof down -t 60`. Live and test were up the whole time (6 h and 5 h).

## Deviations and decisions for Chase

1. **The panel is its own tab, Shard question, for both shards** (a LIVE / Test choice on it), next to Fix test shard.
2. **The real proof ran on a scratch shard, not on the test container itself:** the same image, the same compose shape
   (stdin and tty), and a scratch copy of the test world. Running the real test container on a scratch save would mean
   recreating it with other mounts. The brief's point (never the real saves) holds either way.
3. **No compose change:** both files already open stdin and a tty, so there is nothing to apply to live.
4. **A fatal stays a red CRASHED tile** (P96's), with "waiting at press return to exit" added. Every other question is
   the amber `WAITING FOR AN ANSWER`.
5. **What the panel does not answer:**
   - the owner-account prompt's `y` (it needs a name and a password typed at the console);
   - the restore menu (choosing a backup).

   Both show the question and offer Stop.
6. **The email only goes when the console or `-Status` runs against Docker.** Nothing watches with the console shut. A
   scheduled `-Status` every few minutes would close that gap; say if you want it.
7. **Quiet time is 20 s.** A question is called only once the shard has been silent that long after the lead-in, so it
   is never called mid-print.
8. **Every non-delete answer also needs a phrase** (`answer live` or `answer test`). The safety check wants a phrase for
   anything that touches live.

## For Chase

**Live's D94 question, with the new panel.** Shard Console, Shard question tab, LIVE. It shows the question, the error
(`ReadDateTime` ticks out of range in `WoodDiscoveryEntry`), and the three answers. What each does there:

- **`y` or `a`: do not.** It deletes `ClusterFAccountPersistence` 0x40128E03, the one object that holds every account's
  ClusterF data (renown, achievement points, recipes, guild data, discoveries, the tutorial record, exploration). The
  proof shows the shard then loads and saves within a second, so the loss is written at once. The panel would back up
  the save first, but restoring it would only bring back the same question.
- **`n`:** deletes nothing. Loading fails, and live stops at "press return to exit". An Enter after that exits, and
  live's `restart: unless-stopped` starts it again into the same question. So `n` alone changes nothing useful.
- **Stop the shard (recommended):** type `stop live`. It runs `docker stop -t 60 sl-modernuo`. Nothing has loaded, so
  nothing is lost. It frees 2593, and live stays stopped, because unless-stopped does not restart a container that was
  stopped. This fits your 10-14 decision that live is treated as never existing until 1.0.

The overseer's pick and mine is **Stop**. The cause is D94's: live runs the September image against today's
`server/customizations`, which reads the account data differently. That is for the 1.0 fresh-world deploy, not an answer.

**Live compose change:** none. `docker-compose.yml:30-31` already has `stdin_open: true` and `tty: true`, and the
running container has both, so no recreate is needed.

**Other one-time things:**

- The first console start (or `-Status`) after this commit emails you live's question once:
  `[Shard] Live is waiting for an answer: Delete the object and continue? (y/n/a)`.
- `D:\UO\question-proof\` (the scratch world, its broken copy and its snapshot, about 138 MB) can be deleted. Nothing refers to it.
- The P102 leftover `sl-modernuo-bot` (loopback 2595) is still up; `docker compose -p sl-uo-bot down -t 60` removes it.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

P106 DONE
