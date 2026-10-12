# cc-P73: wipe test accounts (shard-side wipe + a Console option)

Builder: Claude, in `D:\ShatteredLegacy`. Engine authority: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (checked with `git rev-parse HEAD`). Every engine file:line below is at that
commit, paths relative to `Projects\` (`S\` = Server, `U\` = UOContent). Customizations paths are
`D:\ShatteredLegacy\server\customizations\...`.

## Status: finished on 2026-10-12

Built, tested, and proven on a copy of the test world. **Not deployed:** the test shard still runs its old image, and
the real test world was not wiped. Chase runs that from the Console (For Chase, at the end).

## Headlines

- **Test shard > Wipe test accounts** is a new Console button. It refuses as SYSTEM, shows the test shard's own
  account, character and house counts, and asks for the new admin's name and the phrase `WIPE TEST ACCOUNTS`. Its
  window asks for the password, masked, twice. It then stops the test shard (shutdown save), backs up `Saves` to
  `Saves.aside-<time>`, places a request file, starts the shard, and shows the shard's DONE line and counts.
- **The wipe runs inside the shard**, with the engine's own deletes, never by editing save files:
  `server\customizations\Misc\TestAccountWipe.cs`. It runs last in `Initialize`, after world load and before the
  network starts, so `AccountPrompt` never sees an empty world and **no console prompt can hang the boot**.
- **Live can never honour it, in code: three locks.** The wipe needs `SL_SHARD_ROLE=test` (only
  `docker-compose.test.yml` sets it), `clusterf.testShard.allowAccountWipe: True` (only Configuration-test has it,
  written by `Start-TestShard.ps1`), and no listener on 2593. Otherwise it logs `REFUSED`, removes the request and
  changes nothing. The console has its own fourth lock: its safety check never writes a request outside the test world
  folder.
- **The password never reaches disk, a command line, git, notes or logs.** The console hashes it in the window that
  asked for it, in pinned's own PBKDF2 format. Only that hash goes in the request, and the request is removed once the
  wiped world is saved. The shard installs the hash as is, and the first login rehashes it to Argon2.
- **`aetherion`, `admin` and the protected list:** after a wipe, auto account creation would let anyone on the LAN
  create `aetherion` or `admin`, and `ServerAccess` can then make that account Owner. The wipe rewrites
  `server-access.json` to name only the new admin.
- **Correction to the brief:** the test `Saves` folder is **29 MB**, not about 2.5 GB. The world folder is 2.5 GB, but
  1.9 GB of that is `Archives` and 395 MB is `Backups` (`du -sh`, 2026-10-12). The backup copies `Saves`, and the
  free-space check is sized on `Saves`.

- **Proven on a copy of the test world.** The copy is the real test `Saves`, booted in its own container on port 2600.
  - **Boot:** 0 `Bad deserialize` lines and 0 prompts in five boots.
  - **Live refused:** the live-configured copy refused the request and wiped nothing.
  - **The wipe:** it deleted 7 accounts, 9 characters and 3,348 items, saved, and removed the request.
  - **Login:** the new admin logs in, and a wrong password is denied.
  - **Not twice:** a second boot wiped nothing, and the same request put back was refused as `ALREADY DONE`.
  - **Houses, vendors, pets, boats:** the test world has none, so they are proven by a shard test that builds them
    around a character and runs the real wipe. It was watched failing.

## Part A: what a wipe has to remove

`Account.Delete` (`U\Accounting\Account.cs:331-363`) deletes each character's houses (`BaseHouse.GetHouses(m)`, which
returns only houses whose `Owner == m`, `U\Multis\Houses\BaseHouse.cs:1342-1363`), then the character, then removes the
account (`Accounts.Remove`, `U\Accounting\Accounts.cs:41-45`). Everything else in this table is what that leaves, and
what `TestAccountWipe.Wipe` does about it (its step numbers are in brackets). The two research passes behind it were
spot-checked against source at every line cited in `TestAccountWipe.cs`. The rest are as they reported them.

| Thing | Engine on account delete | Wipe | How |
|---|---|---|---|
| Accounts (`Saves\Accounts`) | removed | **cleared** | `Account.Delete` on every account [6], then one new Owner [11] |
| Characters (`Saves\Mobiles`, PlayerMobile) | deleted | **cleared** | via `Account.Delete`; a character with no account is deleted after [6] |
| Equipped items, pack, bank box | deleted with the mobile (`S\Mobiles\Mobile.cs:2491-2497`, `S\Items\Item.cs:3542-3545`, contents `Item.cs:1543-1551`) | **cleared** | engine |
| Ridden mount | `MountItem.OnAfterDelete` deletes it (`U\Mobiles\Animals\Mounts\BaseMount.cs:332-338`) | **cleared** | engine |
| Pets, summons | summoned, bonded and dead pets deleted; **unbonded pets released into the wild with a 3-day timer** (`U\Mobiles\PlayerMobile.cs:3847-3862`, `U\Mobiles\AI\BaseAI\PetOrders.cs:476-530`) | **cleared** | every `BaseCreature` whose `ControlMaster` or `SummonMaster` is a character is deleted **before** the characters [1] |
| Hirelings, escorts | left with a dangling master (`BaseHire.cs:89-101`; `BaseEscortable.cs:539-570`) | **cleared** | same `ControlMaster` rule [1]; spawners make new ones |
| Stabled pets | deleted (`PlayerMobile.cs:3829-3837`) | **cleared** | engine |
| Shrunk pets (ours) | the figurine goes with the pack; the creature on `Map.Internal` keeps its master (`ShrunkPet.cs:56-66`) | **cleared** | `ControlMaster` rule [1] |
| Pack mules (ours, `PackMule.cs:33`) | as any pet | **cleared** | [1] |
| Houses of characters | deleted, **but** lockdowns, secure containers and rental contracts are unlocked and **left in the world** (`BaseHouse.cs:3400-3456`), addon deeds are dropped at the addon (`:3458-3504`), and vendors are `Destroy`ed, which drops their stock in a backpack on the ground or leaks it on `Map.Internal` (`:640-657`, `U\Mobiles\Vendors\PlayerVendor.cs:316-387`) | **cleared with contents** | lockdowns, secures, rental contracts, addons (a deleted addon gives no deed, `BaseHouse.cs:3467`), loose items inside (`GetItems`, `:1247`), vendor inventories and the moving crate are deleted first, the lists emptied, then the house [3] |
| Houses with no owner | not touched | **kept, counted** | server-placed buildings have no owner. The DONE line says how many were kept |
| Player vendors, barkeepers | `Destroy`ed with a house (above), else left | **cleared** | any whose `Owner` is a character, plus every vendor in a wiped house, plain `Delete` (stock goes with them) [2] |
| Boats | **not deleted**: no handler, decays in 9 days (`U\Multis\Boats\BaseBoat.cs:298`, `:57`) | **cleared** | `Owner` a character [4] |
| Player corpses | **left** (`U\Items\Misc\Corpses\Corpse.cs:135`), decay on their own | **cleared** | `Owner` a character [5] |
| Trash bags (ours) | **left** outside a pack (`TrashBag.cs:41-43`) | **cleared** | `Owner` a character [5] |
| Bulletin posts | **left** (`U\Items\Bulletin Boards\BulletinMessage.cs`, `Poster`) | **cleared** | `Poster` a character [5] |
| Items made during the delete | a Jacob's pickaxe makes its exhausted copy inside the pack being deleted (`JacobsReinforcedPickaxe.cs:164`) | **cleared** | items whose parent is deleted, and creatures whose master is deleted, swept until none (at most 5 passes) [7] |
| Guilds (`Saves\Guilds`) | the last member's delete disbands it (`U\Misc\Guild.cs:804-807`, `:1342-1380`) | **cleared** | engine; any left with no live leader `Disband()` [9]. Test world: `Guilds.bin` is 0 bytes |
| BOB entries (`Saves\BOBEntries`) | **left**: `BaseBOBEntry.Delete` (`U\Engines\Bulk Orders\Books\BaseBOBEntry.cs:37-41`) has no caller on book delete | **cleared** | the entries of every book that ends up deleted [8]. Test world: 0 bytes |
| Virtues, PlayerMurders, ChampionTitles, Disguises, ML quests | removed on `PlayerDeletedEvent` (`VirtueSystem.cs:78-79`, `PlayerMurderSystem.cs:58-65`, `ChampionTitleSystem.cs:28-35`, `DisguisePersistence.cs:73-80`, `MLQuestSystem.cs:623-633`) | **cleared** | engine. The wipe runs after every `Initialize`, so these handlers are subscribed |
| PointsSystem (ours, Clean Up Britannia) | removed on `PlayerDeletedEvent` (`Services\PointsSystems\PointsSystem.cs:198-208`) | **cleared** | engine, then `Clear()` on every system [10] |
| Jail | **no delete hook**; a deleted player is written as `Serial.MinusOne` and dropped at the next load (`U\Systems\JailSystem\JailSystem.cs:404-425`) | **cleared at the next load** | not touched (its tables are private). Test world: `Jail.bin` is 2 bytes, no records |
| Ethics | **no delete hook**; an entity keeps a null mobile (`U\Engines\Ethics\Core\Player.cs:133-146`) | **not handled** | `ethics.enable` is False and `Ethics.bin` is 0 bytes in the test world. See Deviations |
| Factions | `PlayerMobile.OnAfterDelete` removes the member (`Faction.cs:401-475`) | members cleared; **faction and town state kept** (world) | engine |
| StealableArtifacts, WeakEntityCollection | keyed by world items (`WeakEntityCollection.cs:38`) | **kept** | world content |
| StaffHubSpots (ours) | keyed by staff **username** (`StaffHub\ClusterFStaffHubSpots.cs:34`), no character reference | **kept** | Chase: staff travel spots stay. A new admin with an old staff name sees that name's spots again |
| ClusterFAccountPersistence (ours): League, renown, restorations, ore/wood/imbuing discoveries, creatures met, bulletin read position, per-character guild, League and exploration data | **left**, keyed by username; no remove or clear existed (`ClusterFAccountData.cs:853-880`) | **cleared** | new `ClusterFAccountPersistence.ClearAll()`, called after every delete, because deleting a Jacob's pickaxe writes the record back (`ClusterFRestorationRegistry.cs:150`) [10] |
| ClusterF achievements (ours) | **left**, keyed by username (`ClusterFAchievements.cs:268`, `:272`) | **cleared** | `LoadFromSave(empty, empty)` [10] |
| Recipes | on the PlayerMobile (no shard store found: searched AcquireRecipe, KnownRecipes, RecipeScroll) | **cleared** | with the character |
| ClusterF bulletins (ours) | global list, no player data (`ClusterFBulletin.cs:27-30`) | **kept** | world |
| ServerAccess protected list (`Configuration\server-access.json`) | **not touched** | **rewritten** to the new admin only | Part B.3 [11] |
| `AccountHandler.IPTable` | in memory, decremented (`Account.cs:355-358`) | engine | |

Searched for and not present: player-owned houses, camps or vendors defined in customizations; evo pets, companions,
familiars (only `PackMule` and `ShrunkPet`); galleons (no `BaseGalleon` in pinned).

## Part B: the shard-side wipe (`server\customizations\Misc\TestAccountWipe.cs`)

**Shape: a request file, read once at boot.** This is the brief's recommended shape, kept, and placed precisely:

- **Where:** `account-wipe-request.json` in the world folder, the parent of `World.SavePath`. In the test container that is
  `/var/lib/uo/modernuo`, which is `server\lib\uo\modernuo-test` on the host.
- **When:** in `Initialize`, at `[CallPriority(int.MaxValue)]`. Boot order is world load (`S\Main.cs:672`), then
  `AssemblyHandler.Invoke("Initialize")` (`:674`), then `NetState.Start()` (`:678`). `Invoke` sorts by `CallPriority`
  ascending (`S\AssemblyHandler.cs:143`, `S\Attributes.cs:59-70`), so the wipe runs **after every other `Initialize`**
  and before the network.
- **Why last, not first:** every system's `PlayerDeletedEvent` handler is subscribed by then. And `AccountPrompt`
  (`U\Misc\AccountPrompt.cs:10-17`, priority 0) has already run and seen the old accounts, so it never asks
  `create the owner account now? (y/n)`.
- **A world that already has no accounts** would prompt before the wipe gets to run. `TestAccountWipe.EarlyAdmin`
  (`int.MinValue`) makes the admin first in that one case, and the wipe keeps that account. This path is not proven: the
  copy had 7 accounts.
- **Deleting in `Initialize` is safe:** the world is `Running` from `World.cs:204` on, so deletes act at once (no
  deferred queue: `GenericEntityPersistence.cs:944-948`), and no delete path needs the loop or a NetState.

The order of the wipe (`Wipe`, steps 1 to 10, then 11 in `Initialize`):

1. Pets and summons first.
2. Vendors.
3. Houses with their contents.
4. Boats.
5. Corpses, trash bags and bulletin posts.
6. Accounts, then characters without one.
7. An orphan sweep.
8. BOB entries.
9. Guilds.
10. Shard records.
11. The new admin and the protected list.

Then it saves.

**Saving, then removing the request.** `World.Save()` only queues: the snapshot is posted to `Core.LoopContext`
(`S\World\World.cs:281`), a queue made at `S\Main.cs:545` that drains once the loop runs. So the wipe asks for the save
and polls once a second. A publish sets the `Saves` write time to `Core.Now` (`World.cs:466`). When that time is at or
after the wipe, the save is this one: the request is removed and the shard logs:

    [AccountWipe] DONE: request <id>: deleted N accounts, N characters, N items, N houses, N pets, N boats, N vendors, N guilds; kept N houses with no owner; admin '<name>' made (Owner); world saved; request removed

If no save publishes, it asks again once a minute, and after 10 minutes it logs `FAILED` and leaves the request. A crash
before the save leaves the save on disk untouched, so the next boot does the whole wipe again from scratch.

**Never twice.** The request's id goes into the `AccountWipe` persistence, registered only on the test shard, in the
same save as the wipe. A request that comes back is logged `ALREADY DONE`, removed, and nothing is wiped.

**A wipe that throws:** the shard logs `FAILED` and exits at once with `Environment.Exit(1)`, saving nothing. It does not
rethrow: an unhandled exception can stop at `This exception is fatal, press return to exit` (`S\Main.cs:430-434`), which
is the D40 hang in another form.

**The census and the audit.**

- **Census:** the shard logs `[AccountWipe] census: N accounts, N characters, N houses` at every start, and again after
  any save that changed it, on live too (counts only, no names). The console reads the newest one to show what a wipe
  would delete.
- **Audit:** on the test shard only, at start and after a wipe, it logs what a wipe must leave at none and what it must
  leave alone: houses with and without an owner, owned boats, tamed or summoned creatures, player vendors, player
  corpses, items inside a deleted container, loose items on `Map.Internal`, ClusterF account records, mobiles and items.

### B.1 Test only, enforced in code

`TestAccountWipe.Refusal` needs all three of these:

| Lock | Set by | Live has it? |
|---|---|---|
| `SL_SHARD_ROLE=test` in the environment | `docker\uo\docker-compose.test.yml` (new) | no: `docker-compose.yml` sets no such variable |
| `clusterf.testShard.allowAccountWipe` `True` in `modernuo.json` | `docker\uo\Start-TestShard.ps1`, on every run, like its listener fix (new) | no. The shard reads the key with `ServerConfiguration.GetSetting` (`S\Configuration\ServerConfiguration.cs:46`), which never writes, unlike `GetOrUpdateSetting`, so live's config never gains it |
| no listener on 2593 | Configuration-test listens on 2594 | live listens on 2593 |

If any lock is missing, the shard logs `[AccountWipe] REFUSED: <which lock>. Nothing was wiped; the request was removed.`
It removes the request because the file holds a password hash. The console adds a fourth lock: `Test-PlanSafety`
refuses a request path that is not `WipeRequestFile`, or that lies in the live world folder, and any wipe step without
the `WIPE TEST ACCOUNTS` phrase.

### B.2 No prompt, and the password

The owner prompt is the only boot prompt that an account wipe could cause. The wipe's order (B above) means it can never
appear. The other boot prompts (`ConfigurePrompts`, `AutoArchive`, the `y/n/a` load-error prompts at
`GenericEntityPersistence.cs:762` and `GenericPersistence.cs:127`) appear only for a missing setting or a broken save.
The wipe causes neither: it deletes through the engine, and it never edits a file. Proof: 0 prompts and 0
`Bad deserialize` lines in five boots (below).

**How the password requirement is met:**

- **Never on disk or a command line.** The console asks for the password in the action's own window: `Read-Host
  -AsSecureString`, typed twice. It is a `SecureString` until it is hashed in that process, and the plaintext string is
  dropped straight after.
- **Only a hash is written:** PBKDF2-HMAC-SHA256 in pinned's own format (`U\Accounting\Security\
  PBKDF2PasswordProtection.cs`): 2 bytes of iterations, an 8-byte salt and 32 bytes of hash, as upper-case hex.
  `HexStringConverter.GetBytes` reads only `A-F` (`S\Text\HexStringConverter.cs:113`). The hash travels in the request
  only, never on a command line.
- **Not in git, notes, logs or config.** The request is under `server\lib`, which is never committed (AGENTS rule 6).
  The console log and output files hold the admin name, never the password or the hash.
- **Removed after the boot that reads it.** The shard removes the request once the save publishes. The console removes
  it too, whenever its run ends (success, refusal, failure or no answer), so no hash stays on disk.
- **How the shard installs it:** `CreateAdmin` makes the account with a throwaway password, then
  `Account.ApplyPasswordWrite(hash, PBKDF2)` (`U\Accounting\Account.cs:411`). That member is `internal`, and reachable
  because customizations compile into UOContent. The first login verifies it with PBKDF2 and rehashes to the configured
  Argon2: `AccountHandler.cs:414` -> `PasswordWorker.cs:231`, or inline `Account.cs:441-444`.
- **Proof the formats agree:** the console's hash, a Python `hashlib` vector, and pinned's `ValidatePassword` agree on
  the same two strings, one of them non-ASCII (a console fact and a shard test). A real login with the proof password
  was accepted (below).

### B.3 `Protected accounts registered: aetherion` (and `admin`)

What `ServerAccess` does today (`U\Misc\ServerAccess.cs`):

- `Configure` reads `Configuration\server-access.json` and logs the line (`:49-63`).
- On every login, `EventSink_ResetProtectedAccount` (`:72-95`) finds an account with a protected name. If it is below
  Owner or banned **and the password given is its own**, the handler makes it Owner and unbans it.
- `Account.Delete` never touches the list.
- Configuration-test's list is `aetherion` and `admin`.

**When `aetherion` is gone:** auto account creation is on in Configuration-test
(`accountHandler.enableAutoAccountCreation True`; `AccountHandler.cs:297-299`). So whoever first logs in as `aetherion`
or `admin`, with any password, creates that account. If `AccountHandler`'s login handler runs before `ServerAccess`'s,
that new account then passes the password check and is made **Owner**. Both are subscribed in an `Initialize` with no
`CallPriority` (`AccountHandler.cs:72`, `ServerAccess.cs:68`), so their order is whatever `List.Sort` makes of equal
priorities. Not fixed, and not probed.

The Admin TazUO profile logs in as `admin`, so this is the ordinary case, not an exotic one.

**Handled:** the wipe sets the list to exactly the new admin (lower case) and saves it with
`ServerAccess.SaveConfiguration()`, which writes Configuration-test's file. A recreated `aetherion` or `admin` is then a
plain Player.

**Proof on the copy:**

- After the wipe the file reads `"protectedAccounts": ["p73admin"]`, and the next boot logs
  `Protected accounts registered: p73admin`.
- A login as `aetherion` with a made-up password was accepted and logged `Creating new account 'aetherion'`. No
  `Protected account ... has been reset` line followed.

### B.4 The four TazUO test launchers

The desktop shortcuts `SL TEST - Admin`, `- Human`, `- Gargoyle` and `- Elf` run
`ShatteredLegacy-2026.10.02.0840\app\Play-Test.bat -Account <profile>`. Each profile is
`app\tazuo\settings.test.<profile>.json`, with a saved username and password and auto-login on
(`Launch-Settings.ps1:28-31`). The saved usernames are `admin`, `human`, `Gargoyle` and `Elf`; I read the usernames
only, never the passwords.

After a wipe:

- **Human, Gargoyle, Elf:** they come back by themselves. Configuration-test has auto account creation on, so each
  profile's saved login recreates its account, as a Player, on its first login. Each account has no characters, so
  TazUO stops at the character list and you make new ones. `maxAccountsPerIP` is 5 there, and four profiles fit.
- **Admin:** it logs in as `admin`. Either:
  - **name the new admin `admin` and give it the password saved in that profile.** The profile then logs straight in as
    the Owner, or
  - name the admin something else. The profile then makes a Player account called `admin`, which is no longer
    protected (B.3).
- **Chase's daughter's account:** she logs in as before, and auto-creation makes her account again, with no characters.

## Part C: the Console option (`scripts\Shard-Console.ps1`)

**Test shard > Wipe test accounts (keep world)...** is key `test.wipe`, in the Test shard group, run in its own window.

**What the button does:**

1. **It refuses before any dialog** (`Get-WipeRefusals`), in these cases:
   - **The console runs as SYSTEM.** Same rule and wording as the Commit tab.
   - **The test shard is not running**, or its log since start has no census line. That means an image without P73.
   - **A request is already waiting.**
   - **The drive lacks room for the backup.** The check needs the save's size plus 10% plus 1 GB free.
2. **First dialog** (`Show-WipeAdminPicker`):
   - It shows what goes and what stays, using the test shard's own counts and the time it gave them.
   - It says plainly how this differs from Start fresh.
   - It asks for the new admin's name (one word: letters, digits, `.`, `_`, `-`).
3. **Second dialog:** the console's usual typed confirmation, with the full plan and a "BEFORE YOU TYPE" line. The
   phrase is `WIPE TEST ACCOUNTS`, matched exactly and case-sensitive.
4. **The window.** It is spawned with `-Mode Execute -Action test.wipe -ConfirmLive "WIPE TEST ACCOUNTS" -WipeAdmin
   "<name>"`, so it never receives a password. It re-reads the facts and runs the plan in this order:
   1. **Ask the password**, twice, not shown. Empty or mismatched cancels with **nothing changed** (exit 3).
   2. **Stop.** `Start-TestShard.ps1 -Down` stops the test shard (compose down, 60 s, which is the shutdown save, D50).
   3. **Check stopped.**
   4. **Back up.** Copy `modernuo-test\Saves` to `Saves.aside-<yyyyMMdd-HHmmss>` (`New-AsideName`), then verify the
      file count and bytes.
   5. **Place the request.** This is the first change to anything the shard reads.
   6. **Start.** `Start-TestShard.ps1 -SkipBuild` starts the shard and waits for the listener.
   7. **Wait** up to 300 s for the shard's DONE line, then show it with the audit and the new census. `REFUSED`,
      `FAILED` or silence is a failure, and a request left behind is removed.
   8. **Log** one line to `shard-console.log`.
5. **Cancel at any step before the request is placed leaves everything as it was.** Cancelling the name dialog, the
   phrase or the password stops before the shard is stopped. A failure after the stop leaves the save untouched and the
   backup beside it, and the window says so.

**Start fresh is unchanged** (`test.fresh`, `Shard-Console.ps1:1176-1183` in the brief, which has since moved down).
Its button now reads "Start fresh (new world, live accounts)". The Test shard tab's caption says, in capitals, how the
two differ:

- Start fresh makes a NEW WORLD with the LIVE accounts copied in.
- Wipe keeps the WORLD, copies nothing from live, and makes one admin.

**Facts** (`scripts\tests\Shard-Console.Tests.ps1`): 15 new, `P73_*`. 157 of 157 pass (142 before). They are the repo's
own `Fact` harness, not Pester (see Deviations). They cover:

- the SYSTEM refusal, with no dialog and no window;
- the other refusals: shard stopped, no census, request waiting, no room, free space unknown;
- the name rules;
- the exact phrase: four wrong phrases each run nothing and ask no password;
- cancel at the name, at the phrase and at the password: nothing run, no request, no backup;
- the plan's order, and that it names nothing live;
- the safety rules: request in the live folder, no phrase, another action's phrase, waiting on live;
- the child's command line, which carries the name and phrase but no password or hash;
- a full run on a world folder in TEMP: backup made, request holding only the hash, which re-derives from the password,
  DONE shown, no request left;
- refusal, failed start and silence, each ending in failure with the request removed and the backup kept;
- the hash against the Python vectors;
- the log parser;
- the caption.

The same harness makes every window action (now including `test.wipe`) honour `-Mode`, under D37's facts.

**Gates watched fail.** Each of these breaks turned exactly its own fact red (156 of 157), and each was restored
byte-identical:

- turning off the live-folder rule in `Test-PlanSafety`;
- ignoring a cancelled password;
- keeping the request after a failure.

## Proof on a copy (the real test world was never wiped)

**The copy.** `server\lib\uo\modernuo-test\Saves` (29 MB) was copied to my scratch folder, with a copy of
Configuration-test whose listener moved to 2600, so a client can never be relayed to the real test shard. Each boot was
a container of `sl-modernuo:cc-p73` with its own name and port, from the final image `179a9f942029`, with the same
mounts as `docker-compose.test.yml`. `sl-modernuo-test` kept running throughout (its StartedAt, 14:44:49Z, is unchanged)
and `sl-modernuo` was not touched.

**The password.** It was 24 random characters held in memory by the proof script and passed to the login probe in its
environment. It is in no file and no log; the script's own check found it absent from the request.

**The login probe** (`uo_login_probe.py`, scratch) sends a client's first two packets: the `0xEF` seed and the `0x80`
account login. It reports the server's `0xA8` server list (accepted) or `0x82` (denied, with its reason). That is the
shard's real login path, the password worker included.

Every boot below logged **0 `Bad deserialize` lines and 0 console prompts**.

| Boot | Setup | What the shard logged | Request file afterwards |
|---|---|---|---|
| A1 | **configured as live**: no `SL_SHARD_ROLE`, no allow key, listening on 2593 (host 2601), with a request | census `7 accounts, 9 characters, 0 houses`; `REFUSED: SL_SHARD_ROLE is '(unset)', not 'test' ... Nothing was wiped; the request was removed.` | gone |
| A2 | the test configuration, but no `SL_SHARD_ROLE` | same census; same `REFUSED` | gone |
| B | the test shard, with a request for admin `p73admin` | before: census `7 accounts, 9 characters, 0 houses`; audit `0 houses, 0 owned boats, 0 tamed or summoned creatures, 0 player vendors, 0 player corpses, 0 items in a deleted container, 1107 loose items on Map.Internal, 6 ClusterF account records, 35129 mobiles, 207797 items`. Then `DONE: ... deleted 7 accounts, 9 characters, 3348 items, 0 houses, 0 pets, 0 boats, 0 vendors, 0 guilds; kept 0 houses with no owner; admin 'p73admin' made (Owner); world saved; request removed`. After: census `1 account, 0 characters, 0 houses`; audit `... 0 items in a deleted container, 1107 loose items on Map.Internal, 0 ClusterF account records ...` | gone |
| C | logins on B | `p73admin` with its password: **ACCEPTED** (`Valid credentials`). Wrong password: **DENIED, reason 3 (bad password)**. `aetherion` with a made-up password: accepted as a new Player account (`Creating new account 'aetherion'`), with **no** `Protected account ... has been reset` line. `server-access.json` reads `["p73admin"]` | |
| D | second boot of the wiped copy, no request | `Protected accounts registered: p73admin`; census `2 accounts` (p73admin, and the aetherion C made), `0 characters, 0 houses`; same audit; **no wipe line** | none |
| E | the **same** request put back | `ALREADY DONE: request 20261012-142803-proof001 was carried out before. Nothing was wiped again; the request was removed.` Census unchanged | gone |

**What these runs show:**

- **Live is refused.** A1 is the live-configured copy. Both refusals name the first missing lock, `SL_SHARD_ROLE`.
- **Each lock on its own** (role, setting, port) is shown by the shard test
  `TheWipeIsAllowedOnlyWithAllThreeTestShardLocks`, which was watched failing.
- **Nothing is wiped twice.** D had no request; E's replayed request was refused.
- **Mobile and item totals differ between boots.** Spawners run between saves; the audit's own counts are what matter.

**Nothing ownerless remains, for what the world had.** The copy had **no houses, vendors, pets or boats before the
wipe** (the audit, B), so on real data that part is shown only for characters, accounts and their 3,348 items:

- 0 items in a deleted container.
- `Map.Internal` loose items unchanged at 1107, so nothing leaked there.
- ClusterF account records went from 6 to 0.

Houses (with a lockdown, a secure box with gold, a loose item and a vendor with stock), a pet in the world, a shrunk pet
on `Map.Internal`, a boat and a trash bag are proven by the shard test `AWipeLeavesNothingTheCharacterOwnedAndKeepsTheWorld`.
It builds each around a character and runs the real `Wipe`: all of them deleted, and a wild horse and an unowned item
kept. It was watched failing with the lockdown and secure deletes removed.

**Earlier run.** The same five boots ran first on image `4ae818364bee`, before `Wipe` took its targets as parameters,
with the same counts and results. The final image was proven again from a fresh copy.

## Build

```
& "C:\Program Files\Git\bin\bash.exe" docker/uo/build.sh -t sl-modernuo:cc-p73
Built sl-modernuo:cc-p73 with patches applied and 1011 shard test(s) passing.
```

- **Image:** `sha256:179a9f942029ccd60590315e7ed35b110ec212055579c64ec6f5c481d027ec82`, from the tree as committed. Build
  logs are in my scratch folder.
- **Shard tests:** 1011, which is 1006 before plus the 5 in `server\tests\Misc\TestAccountWipeVerification.cs`.
- **Noise:** the `Item.Amount <= 0` lines in the test log predate this task (P10, P17).
- **Watched fail** (shard). Two breaks went into one build, tagged `cc-p73-break`: the lockdown and secure deletes
  removed, and the role lock ignored. Exactly `AWipeLeavesNothingTheCharacterOwnedAndKeepsTheWorld` and
  `TheWipeIsAllowedOnlyWithAllThreeTestShardLocks` failed, and `BUILD FAILED ... No image was built`. The source was
  restored byte-identical (`cmp`).
- **Watched fail** (console). Three breaks, each turning its own fact red (Part C).
- **Console facts:** `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1` gives
  157 of 157.
- **A dry run against the real Docker**
  (`Shard-Console.ps1 -DryRun -StatusFromDocker -Action test.wipe -WipeAdmin newadmin`) refuses, correctly:
  `sl-modernuo-test` still runs the pre-P73 image, so it reports no census.

## Deviations and decisions for Chase

1. **The password is asked in the wipe's own window, not in the Console form.**
   - The form asks the name and the phrase. The window it opens asks the password, masked, twice, before it changes
     anything.
   - Asking in the form would have meant passing the password (or its hash) to the child window: on a command line,
     which other processes can read and which Windows can audit-log, or through an environment variable or a file.
   - This way it lives in one process only. Leaving it empty is a cancel with nothing changed.
2. **The request carries a PBKDF2 hash, not the password.** The brief allowed the password on disk until the boot that
   reads it; this never writes it at all. The cost:
   - The new admin's stored hash is PBKDF2 at 1024 to 1536 iterations until its first login, which rehashes it to
     Argon2.
   - Log in once soon after a wipe.
3. **Tests are the repo's `Fact` harness, not Pester.** The brief says Pester tests. `Shard-Console.Tests.ps1` is
   deliberately not Pester (its header: Windows ships Pester 3.4, confirmed here with `Get-Module -ListAvailable
   Pester`), so the 15 new facts follow it. The shard side has 5 xUnit tests in the build gate.
4. **The proof world has no houses, pets, vendors or boats.** The test world (and so the copy) had 0 of each, by the
   shard's own audit. Those paths are proven by the shard test `AWipeLeavesNothingTheCharacterOwnedAndKeepsTheWorld`,
   which builds them around a character and runs the real `Wipe`. They are not proven on real save data.
5. **Houses with no owner are kept and counted, never deleted.** A player house whose owner was already gone before the
   wipe (null after load) looks the same as a server-placed building, so the wipe keeps both and the DONE line says how
   many. The copy had 0.
6. **Not handled:**
   - **Ethics** entities, which keep a null mobile (no delete hook, `Player.cs:133-146`). Ethics is off and empty in the
     test world.
   - **Jail records**, private tables, which the engine drops at the next load (`JailSystem.cs:404-425`). Empty in the
     test world.
   - **Staff travel spots** stay, as decided. They are keyed by username, so a new admin given an old staff name sees
     that name's spots.
7. **The shard logs a census line on live too:** counts only, at start and after a save that changed them. The audit
   and the wipe run only where all three locks hold.
8. **Two new config locks:**
   - `SL_SHARD_ROLE: test` in `docker-compose.test.yml`, which recreates the test container at its next `up`.
   - `clusterf.testShard.allowAccountWipe: True`, which `Start-TestShard.ps1` adds to Configuration-test on every run.
     It refuses to start if it cannot.
9. **`Start fresh`'s button text changed** to "Start fresh (new world, live accounts)". Its plan is untouched.
10. **Brief figure corrected:** the test `Saves` is 29 MB. The world folder is 2.5 GB, nearly all of it `Archives` and
    `Backups`.

11. **`tools/progress.py` was not run for real** (its dry run works). At the end of this task, `tools/progress.json` and
    `docs/feature-queue.md` had uncommitted changes that are not mine, as did `docs/artificers-imbuing-design.md` and
    ShatteredLegacy's `design/paperdoll-sos/`. Running it would have folded someone else's work into my commit. My
    commits name my files only. Run it with the next commit.

No D-number or Q-number taken.

## For Chase

**Deploy (test shard only; nothing here touches live):**

1. My work is committed to `main` in both repos, not pushed. Push when you are ready. The image `sl-modernuo:cc-p73`
   was built from exactly the committed shard files.
2. Console > Test shard > **Deploy built image...**, pick `sl-modernuo:cc-p73`, and type `deploy to test`.
   - That points `sl-modernuo:latest` at it and restarts the test shard. The restart also applies the new
     `SL_SHARD_ROLE` variable and the new setting.
   - Or rebuild: Test shard > Rebuild through the gates and start.
3. When it is up, the log has an `[AccountWipe] census:` line and an `[AccountWipe] audit:` line. The wipe button needs
   the census line.

**To run the real wipe from the Console:**

1. Run the Console from your own Windows login, not as SYSTEM.
2. The test shard must be running on the P73 image (step 3 above). Nobody needs to be logged in: the stop disconnects
   them, and the shutdown save keeps their last minutes.
3. Test shard > **Wipe test accounts (keep world)...**
4. The first dialog shows how many accounts, characters and houses go, and what stays. Type the new admin's name.
   - **Use `admin` if you want the Admin TazUO profile to log straight in**, and use that profile's saved password in
     step 6.
   - Any other name works; the Admin profile then makes a plain Player called `admin`.
5. The second dialog: type `WIPE TEST ACCOUNTS` exactly.
6. A window opens. Type the new admin's password twice, then wait. Leaving it empty cancels with nothing changed. The
   window:
   1. stops the test shard;
   2. backs up `server\lib\uo\modernuo-test\Saves` to `Saves.aside-<time>` beside it;
   3. starts the shard;
   4. shows a green `[AccountWipe] DONE: ...` line, the audit, and "the test shard now has 1 account(s), 0 character(s)".
7. Log in as the new admin once, which rehashes its password to Argon2. Human, Gargoyle and Elf log in as before and
   make new characters.
8. **To undo:** Test shard > Stop. Then, in Explorer, rename `Saves` aside and rename the `Saves.aside-<time>` from step
   6 back to `Saves`. Then Test shard > Start.
   - Configuration-test's protected list will still name only the new admin. Re-add `aetherion` and `admin` to
     `server\uo\modernuo\Configuration-test\server-access.json` if you want them back.

**If it goes wrong:** the window says which step failed and keeps its output in `scripts\shard-console-output\`. The
request file never outlives the run. The shard refuses on live whatever happens to the request. If the shard says
`REFUSED`, the line names the missing lock.

**Promote to `docs\`:** the three-lock rule (the live shard must never honour a test-only action). It belongs beside
D22 and D29 in the deploy and test-shard documents.

P73 DONE
