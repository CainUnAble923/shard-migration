# cc-P215: every Golem gets its own Admin and Player account for play trials

Builder: Claude (Opus), the Bronze Golem, on the game PC (CHASES-TOWER), 2026-10-21. Both work copies were clean on
`golem/Bronze/P215`. Pinned is `D:\UO\ModernUO-pinned` (`d4531cd94`).

## Status: finished on 2026-10-21, with two proofs waiting for the merge

Built, tested, and proven on a scratch test shard of this prompt's own. **Two of the "Proven" items cannot be shown
until this branch is merged and running on the real shards:**
- Gold's and Copper's accounts logging in on **their own** test shards. Those shards run main's code, which has no
  seeder yet.
- The two-account check on **the real Test Shard**. It is down today, and putting an unmerged image on it is not a
  Golem's call.

The exact commands for both are under For Chase. Both checks ran on the scratch shard, from this PC, with the real
accounts and passwords, and passed (section 4).

## Headlines

- **18 accounts, two for each of the 9 Golems that claim prompts:** `<golem>-admin` (Administrator) and
  `<golem>-player` (Player), for Iron, Bronze, Gold, Agapite, Verite, Copper, Silver, Stone and Crystal.
  - Shadow Iron and the Tinker are script Golems: they claim no prompts and get no accounts.
  - Each account has a starter character named after its Golem: `Copper` and `Copper the Tester`.
  - Each character is logged out at its own tile in **Green Acres** (Trammel): x 5440 plus 2 per Golem, y 1150 for
    admins, 1152 for players. That is open grass, out of the way of Chase's play-tests. Every tile was checked against
    the map files: no static, flat at z 0, no spawner.
- **Passwords: random, made on the game PC, never in git.**
  - Each is 24 letters and digits from the system CSPRNG.
  - They are kept in `D:\UO\golem\test-accounts-<golem>.key`, DPAPI-protected, readable only by that Windows account
    and SYSTEM.
  - The game PC holds every Golem's file, so Chase can read any password. Gold's, Copper's and Silver's PCs (and the
    switched-off Agapite and Verite, which share Gold's PC) were each sent only their own file.
  - Helper: `Get-GolemTestAccount.ps1 -Golem <name> -Role admin|player`. It defaults to GOLEM_NAME.
- **Shards get hashes only.** `golem-accounts.json` holds PBKDF2 hashes in pinned's format, the same one the Shard
  Console's account wipe writes. It travels in the kit to every PC.
  - `Start-TestShard.ps1` copies it into the test world folder on every start, `-Fresh` included.
  - The shard seeds the accounts at world load, before the owner prompt. **A fresh, empty world booted straight to
    listening, with the 18 accounts and characters made.**
  - On a running test world, `[SeedGolemAccounts` (or with `dryrun`) makes whatever is missing.
  - It runs on test shards only, behind the account wipe's own guard. It never wipes, and touches no other account.
- **Each Golem uses its own accounts.**
  - `tools\playtest-bot\golemcheck.py` logs in as the running Golem.
  - `uobot.run` with GOLEM_NAME set seeds the Golem's accounts after its wipe and runs its checks as that Golem.
  - The bot has a new test-shard target rule: 2594 and 2595-2599 on any host. **2593 is refused from any host, and
    through any relay.**
- **Testing together:**
  - The shared shard is the game PC's real Test Shard, reached as `chases-tower:2594` or by the LAN address it
    advertises. Gold's, Copper's and Silver's PCs reach the tower both ways.
  - A new lock, `shared-test-shard`, keeps two multi-Golem tests from overlapping.
  - The how-to is in `D:\UO\golem\README.md`.
  - **The two-account check passed:** Bronze's and Gold's players saw each other and both got the trade window.
- **The readiness check** (and so `Join-Golem.ps1`, which ends with it) gains a `test accounts` row. Both of the
  Golem's accounts log in headless on the PC's own test shard, then log out.
- **The web console** shows each card's two account names. On the game PC, Chase gets **copy admin password** and
  **copy player password** buttons; the password never appears on the page.

## 1. What was read, and what it decided

- **The guard.** P73's `TestAccountWipe.Refusal` (`server\customizations\Misc\TestAccountWipe.cs:80-101`) is public
  and pure. It requires `SL_SHARD_ROLE=test`, the `allowAccountWipe` setting True, and no 2593 listener. The seed
  calls it as is: "the same guard as P73".
- **The hash.** The seed installs a hash the way the wipe's admin does it, with `Account.ApplyPasswordWrite` (pinned
  `UOContent/Accounting/Account.cs:411`).
  - The first login rehashes the password to Argon2. So the seed decides "already right" by an account tag holding
    the manifest's hash (`GolemSeedTag`), not by the stored hash. That way a re-seed after logins changes nothing,
    which was proven on the live scratch world.
- **The boot order.** AccountPrompt runs at priority 0 and asks for an owner when a world has no accounts, which hangs
  the boot (the D40 shape). The seed runs at `int.MinValue + 1`, after world load and just after P73's `EarlyAdmin`,
  so a fresh world has accounts before the prompt can look.
- **Where a logged-out character goes.** A character on the Internal map is moved to `LogoutMap`/`LogoutLocation`
  when its player connects (pinned `Server/Mobiles/Mobile.cs:1320-1324`). Seeded characters are built that way.
- **This PC is the game PC.** Its test shard (2594) is Chase's real Test Shard, and it was not running today. Docker
  had only the bot's scratch shard up, and another session's `uobot.run` was using it. So the proofs ran on a scratch
  shard of this prompt's own (section 4). Neither the real Test Shard nor the bot's shard was touched.
- **Reach.** Over SSH (the Tinker's key), Gold's, Copper's and Silver's PCs each connected to `chases-tower` and to
  192.168.1.58 (a port the tower publishes on all interfaces). So the LAN address the real Test Shard advertises
  works from them too. `golemcheck` returns to the host it dialled in any case.
- **What a remote PC can hold.** The kit export copied every file in `D:\UO\golem` that was not on its skip list, and
  `.key` files were not on it. So `agent-<golem>.key` would also have travelled in a new PC's kit zip. Every `.key`
  file is now skipped (`Export-GolemKit.ps1:21`).

## 2. What changed

`ShatteredLegacy` (the Bronze work copy):

| File | What |
|---|---|
| `server\customizations\Misc\GolemTestAccounts.cs` (new) | `ParseManifest` (`:85`): version 1; each name must be `<golem>-admin` or `-player` for its own Golem; character names letters and spaces; PBKDF2 hashes only; spots in Green Acres. `Seed` (`:200`): refuses on the guard, makes what is missing, corrects only the level or a new hash, touches no other account; counts made, changed, characters, already right, skipped. `MakeCharacter` (`:312`): human, backpack with 100 gold (something to trade), a robe, staff blessed, logged out at its spot. `Initialize` at `int.MinValue + 1` (`:68`); `[SeedGolemAccounts [dryrun]` (`:359`, Administrator, `[ShardCommand]` DevTool / Skips / TestOnly / dryrun) |
| `server\tests\Misc\GolemTestAccountsVerification.cs` (new) | 5 facts (section 3) |
| `docker\uo\Start-TestShard.ps1:122-130` | copies `D:\UO\golem\golem-accounts.json` (or `GOLEM_ACCOUNTS_MANIFEST`) into the test world folder on every start |
| `tools\playtest-bot\uobot\safety.py:15-56` | `check_test_target`, `check_test_relay`: test ports on any host, never 2593; the relay must name the dialled port |
| `tools\playtest-bot\uobot\client.py` | `test_target` (`:73`), so one client can dial a test shard; secure trade packets parsed (`:551`, pinned `OutgoingSecureTradePackets.cs:32-50`) |
| `tools\playtest-bot\uobot\golemcheck.py` (new), `tools\playtest-bot\golemcheck.py` (new runner) | `login` and `pair` (see each other, open a trade). The pair waits out the action delay after opening the pack before it lifts the coin |
| `tools\playtest-bot\uobot\run.py:176` | `use_golem_accounts`: with GOLEM_NAME, slbot-admin types `[SeedGolemAccounts` after the wipe and the checks log in as the Golem (`--no-golem` keeps the old accounts); the fresh pool keeps its own password |
| `tools\playtest-bot\Run-OvernightPlaytests.ps1:234` | copies the manifest into the bot's scratch world |
| `tools\playtest-bot\tests\test_golemcheck.py` (new), `tools\playtest-bot\README.md` | 9 facts; the README section |
| `web-console\server.py` | each card's `testAccounts` (`:696`); `POST /api/golem-password` (`:1490`): the tailnet listener, an allowed login, the page's header and origin, as `/api/action`; plain text with no-store, logged without the password; read through `Get-GolemTestAccount.ps1` as the service's own Windows account (`:1271`) |
| `web-console\static\app.js:332`, `:824` | the names on the card, and the two copy buttons |
| `web-console\tests\test_golem_accounts.py` (new) | 4 facts |
| `CHANGELOG.md` (2026.10.21.6, Staff), `VERSION` | |

`D:\UO\golem` (not a repo; backups `*.bak-20261021-P215` of each file changed):

| File | What |
|---|---|
| `GolemTestAccounts.ps1` (new) | the library and commands: `-Status`, `-New`, `-Rotate -Golem`, `-Write`, `-Deliver`; game PC only for the four that write. A re-`-Write` keeps every hash whose password still produces it, so the shards see no change |
| `Get-GolemTestAccount.ps1` (new) | one account's name and password for a script (`-Json` for Python); exit 3 when this PC has no file for that Golem |
| `test-accounts-<golem>.key` (9, new), `golem-accounts.json` (new) | made here with `-New` and `-Write`; the key files never leave the PC except by `-Deliver` |
| `Kit.ps1:21` | the kit carries `golem-accounts.json` (hashes only) |
| `Export-GolemKit.ps1:21` | every `.key` file is skipped |
| `Golems.ps1:37` | the `shared-test-shard` lock |
| `Test-GolemReady.ps1:180` | the `test accounts` row (only where Docker is on and the engine answers) |
| `README.md` | the section "Every Golem's own test accounts, and testing together (cc-P215)", the how-to, the lock |
| `tests\GolemTestAccounts.Tests.ps1` (new), `tests\Join.Tests.ps1` (one fact; the fake gains `testAccounts`) | |

Elsewhere: `D:\UO\golem\test-accounts-{gold,agapite,verite}.key` on STEPHS-DESKTOP, `-copper.key` on
AINSLEYS-LAPTOP and `-silver.key` on ELLIES-LAPTOP. Each is owned by that PC's golem account and SYSTEM only
(`icacls` read back). `D:\UO\p215-shard` is the scratch shard (1.8 MB, stopped).

## 3. Tests (each new one seen failing first)

**Server** (`GolemTestAccountsVerification`, 5 facts), through `docker\uo\build.sh -t sl-modernuo:cc-P215`:

| Run | Result |
|---|---|
| red, 5 breaks (one per fact), `--tests-only` | **5 failed**, 1908 passed; nothing else failed |
| green, full build | **1913 passed, 4 skipped**, image **`sl-modernuo:cc-P215` = `96f716f79ae6`**; `latest` (`8875829de577`) untouched |

| Break | Fact | Message |
|---|---|---|
| the guard ignored | `TheSeedRefusesWithoutTheTestShardFlag` | no "REFUSED" line |
| no `LogoutMap` | `EveryGolemInTheManifestGetsExactlyItsTwoAccounts` | expected Trammel, got null |
| every seed reinstalls every password | `AReseedChangesNothingAndOnlyADifferenceIsCorrected` | 6 changed, 0 already right |
| any username accepted | `TheManifestRefusesAnythingButAGolemsOwnTwoAccounts` | the bad manifest parsed |
| other '-admin' accounts raised | `AnotherAccountKeepsItsLevelAndCharacters` | expected GameMaster, got Administrator |

**Kit** (`tests\GolemTestAccounts.Tests.ps1`, 10 facts):
- Red against the kit as it was (the `.bak` copies, with empty stand-ins for the two new scripts): **8 of 10 failed**
  (11 checks). The two that passed there pass for any kit: no key file in git, and plain ASCII.
- The git fact went red on its own when a `test-accounts-planted.key` was put in the docs work copy ("none waiting to
  be added"), and green once it was removed.
- Green: **201 checks, 0 failed.** Among them:
  - every claiming Golem gets exactly its two accounts, with no script Golem among them;
  - passwords are random, DPAPI-protected, and in no manifest;
  - the hash is byte for byte the Shard Console's own `New-WipePasswordHash`;
  - a re-write keeps every hash, and a rotation changes exactly that Golem's two;
  - a `plain:` file becomes DPAPI on its first read;
  - GOLEM_NAME picks the Golem;
  - the kit carries the manifest and never a `.key` file;
  - the real passwords appear in no tracked or pending file of either repo (`git grep`);
  - the lock exists.

**Join kit** (`tests\Join.Tests.ps1`):
- `P215_TheReadinessCheckLogsInAsTheGolemsOwnTestAccounts` was red on the old `Test-GolemReady.ps1` (4 failed), green
  now.
- The suite: 98 passed, 4 failed. **The 4 failures are one P186 fact that fails the same way with the original files**
  (checked by swapping them back). Its faked "no Tailscale" falls back to a real tailnet probe on this PC, so
  `tailscale` reads Running. It is not caused by this work.

**Bot** (`tests\test_golemcheck.py`, 9 facts):
- Red on the old `safety.py`, `client.py` and `run.py`: 7 of 8 errored; the new run fact also errored. The one that
  passed checks that the overnight scratch rule is unchanged.
- Green: 9 of 9.
- The whole bot suite: 49 ran, 1 failed. That one is `test_overnight`'s installer dry-run fact, which finds the real
  scheduled task registered on this PC. It is environmental and not caused by this work.

**Web console** (`test_golem_accounts.py`, 4 facts):
- Red on the old `server.py`: 3 failed, 1 errored.
- Green: 4 of 4. The whole web-console suite: **81 ran, OK** (1 skipped).

**The other kit suites**, run after the kit changes:
- `tests\Tinker.Tests.ps1` (kit sync): **132 checks, 0 failed**.
- `tests\Golem.Tests.ps1`: 971 passed, 5 failed. The failures are in two P184 facts about overlapping areas (both
  claim P102 while a server prompt runs). `P184_OverlappingTouchesNeverRunTogetherAndGuessesAreLogged` fails the same
  way (1 passed, 4 failed) on a temp copy of the kit with the **original** `Golems.ps1`. So it comes from the live
  queue and claims on this PC, not from the lock name added here.

## 4. Proof on a scratch test shard (this PC)

`D:\UO\p215-shard`: its own container (`sl-modernuo-p215`), compose project, loopback port 2597 and image
`sl-modernuo:cc-P215`, `SL_SHARD_ROLE=test`. The Configuration is a copy of the bot's, with the listener 2597 and the
flag set as below. The world is **empty**: the `-Fresh` case, no accounts, plus the manifest. Under the `test-shard`
lock throughout.

1. **Boot, flag True:** 36 `[GolemAccounts] make ...` lines, then: `18 Golem accounts in the manifest: 18 made,
   0 changed, 18 character(s) made, 0 already right, 0 skipped. No other account is touched.` **No owner prompt.**
   Listening on 2597.
2. **Logins** (`golemcheck.py login --host 127.0.0.1 --port 2597`), each admin and player in and out, each standing on
   its own tile:

   | Golem | admin | player |
   |---|---|---|
   | Iron | ok, Iron at 5440,1150 | ok, Iron the Tester at 5440,1152 |
   | Bronze | ok, Bronze at 5442,1150 | ok, Bronze the Tester at 5442,1152 |
   | Gold | ok, Gold at 5444,1150 | ok, Gold the Tester at 5444,1152 |
   | Copper | ok, Copper at 5450,1150 | ok, Copper the Tester at 5450,1152 |

3. **Two accounts together** (`golemcheck.py pair --golem Bronze --with Gold`, two connections from one PC):
   - `see_each_other: true`, `gold_found: true`, `trade_window: {first: true, second: true}`, `ok: true`.
   - Bronze's client got `0x6F` display "with Gold the Tester"; Gold's got "with Bronze the Tester".
   - The first try had failed: it lifted the coin straight after opening the pack and got cliloc 500119, "You must
     wait to perform another action". `golemcheck` now waits 1.5 s first.
4. **The command, as bronze-admin:**
   - `[SeedGolemAccounts dryrun` replied `dry run: ... 0 to make, 0 to change, 0 character(s) to make, 18 already right`.
   - `[SeedGolemAccounts` replied `0 made, 0 changed, 0 character(s) made, 18 already right`.
   - This was after eight logins had rehashed eight passwords to Argon2: **a re-seed is idempotent.**
5. **Flag False** (restarted with `allowAccountWipe` False):
   - At boot: `[GolemAccounts] REFUSED: clusterf.testShard.allowAccountWipe is 'False' in modernuo.json, not True:
     only Configuration-test has it. ... nothing changed.`
   - `[SeedGolemAccounts` gave the same REFUSED line. The accounts already in the world still logged in.
6. **No password anywhere:** each of the 18 passwords was searched for in the 7 transcripts and the shard's whole log.
   0 hits.

Then the shard was stopped and the lock released.

## Deviations and decisions for Chase

1. **The two shared-shard proofs wait for the merge** (Status). Golems do not put an unmerged image on the real Test
   Shard. After the merge and your next test-shard start, they are the For Chase commands below.
2. **Crystal (cloud), Agapite and Verite (switched off) get accounts too.** "Every Golem in the registry that claims
   prompts" was read as engine claude or codex, enabled or not, so one switched back on has accounts waiting. Stone's
   PC refused the SCP copy ("Connection closed"); it runs no Docker, so it has no test shard. Its file is on the game
   PC.
3. **The hashes travel in the kit.** `golem-accounts.json` holds PBKDF2 hashes, not passwords, so every PC's fresh
   test world can seed every Golem. That is P73's own precedent: its request file carries a hash. If you would rather
   the hashes stayed on the game PC, the manifest could be served to agents by the web console instead.
4. **Remote passwords arrive in the clear and turn into DPAPI at the Golem's first read**, as the agent secrets do
   (`Remote-Agent.ps1`). They are golem and SYSTEM only from the moment they land. I did not read them over SSH: DPAPI
   under a key-based SSH logon might protect them with a key the golem's own session cannot use.
5. **Characters stand in Green Acres**, Trammel's staff area, away from every town and dungeon the play-tests use. A
   Golem player who logs out lingers
   5 minutes at its tile, as any player outside an inn does.
6. **The starter pack has 100 gold** (seeded characters only), so a trade check has something to offer.
7. **The bot's overnight run is unchanged without GOLEM_NAME.** The scheduled task does not set it. With it set, the
   bot logs in as the Golem's own accounts; that path is proven with stand-ins only, because the bot's scratch shard
   was busy with another run today.
8. **The web console's password endpoint is an exception to `redact_tree`:** it returns one password as text, by
   design. It answers only on the tailnet listener, to an allowed login, from the page itself, and its access-log line
   names who, which Golem and which role, never the value. The live console runs main's `server.py`, so the buttons
   appear after the merge and a console restart.
9. **The `test-shard` lock was taken three times only to read or edit `Start-TestShard.ps1`.** The guard hook matches
   that name in any command line, even a `grep`. Each time was a few minutes.
10. **Pre-existing failures, not caused by this work:**
    - the Join suite's P186 readiness fact (the tailnet fallback; above);
    - the bot's installer dry-run fact (the real task is registered here);
    - the 2026.10.21.6 CHANGELOG line was added after the green build, so image `96f716f79ae6` shows 2026.10.21.5 in
      `[version`.

## For Chase

1. **Commit and merge.** The Golem does this after DONE.
2. **Start the test shard** from main after the merge (Console > Test shard > Rebuild through the gates and start).
   - Its start copies `golem-accounts.json` in, and the log shows `[GolemAccounts] 18 Golem accounts ... 18 made`.
   - Nothing else on that world changes.
   - On a test world that is already running: `[SeedGolemAccounts dryrun`, then `[SeedGolemAccounts`.
3. **The shared-shard check:**
   - `powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take shared-test-shard -Minutes 20 -Wait`
   - `cd D:\ShatteredLegacy\tools\playtest-bot`
   - `python -P golemcheck.py pair --host chases-tower --port 2594 --golem Bronze --with Gold`
   - Expect `"ok": true`. Then `-Release shared-test-shard`.
4. **Gold's and Copper's own test shards** (after their PCs take the merged main and restart their test shards):
   - `ssh golem@stephs-desktop "python -P D:\ShatteredLegacy\tools\playtest-bot\golemcheck.py login --host 127.0.0.1 --port 2594 --golem Gold"`
   - The same on `ainsleys-laptop` with `--golem Copper`.
   - Or `Test-GolemReady.ps1 -Name Gold` on that PC: its `test accounts` row.
5. **The console:** after the merge, restart the web console. Each card shows its two account names, and on the game
   PC you get the copy buttons.
6. **New passwords for a Golem:** `GolemTestAccounts.ps1 -Rotate -Golem <name>`, then `-Write`, then `-Deliver`, then
   restart each test shard (or `[SeedGolemAccounts`).

**Promote to `docs\`:** the decisions above (accounts per Golem, the Green Acres meeting place, the
`shared-test-shard` lock and its rules on the real Test Shard).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -CodeRepo
D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration`

The script's defaults name the main copies, which hold none of this work. Code: 16 files pending; docs: 1 file.

```
Repo Result
---- ------
code dry run
docs dry run
```

Neither repo BLOCKED. No file is near 5 MB. No key file or manifest is in either repo (`git ls-files` and
`git status`, kit fact P215_PasswordFilesAndPasswordsAreNeverInGit).

P215 DONE
