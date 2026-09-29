# cc-P6: the shard publishes who is online (ShardStatusPublisher)

2026-09-29. Brief: `D:\UO\cc-prompts\cc-P6-status-publisher.md`. Spec: `D:\ShatteredLegacy\docker\uo-status\README.md`.
Not built into an image, not deployed. Nothing was restarted, recreated or `docker compose`d. P1 had finished (its note is
dated 2026-09-28) before this started.

**READ FIRST: HEAD of `D:\ShatteredLegacy` holds the RED STUB, not the publisher.** I made no commit. But while the red run
was building, `af1d4a6 Shard work, 2026-09-29 13:45` (author Chase, an autocommit) picked up all three of my files as they
were at that moment:

- `server/customizations/ShardStatusPublisher.cs` **as the stub**. `git show HEAD:server/customizations/ShardStatusPublisher.cs`
  has four `// P6 RED` bodies. It compiles and fails the four new tests, so **a `build.sh` of HEAD stops at the test gate.**
- the test file and the compose mount, both final. They are identical to the working tree.

The working tree now holds the real file, `cmp`-identical to the one that went green. So `git diff` in `D:\ShatteredLegacy`
currently shows exactly the stub-to-real change in that one file. It needs to be committed before anything is built from
HEAD. Checklist step 0 below.

## What changed

| File | Change |
|---|---|
| `server/customizations/ShardStatusPublisher.cs` | New. Top-level, so `apply-patches.sh` copies it into `Projects/UOContent/Misc/` (`apply-patches.sh:192-201`). No pinned type or stem called `ShardStatus*` exists, so no collision. |
| `server/tests/Misc/ShardStatusPublisherVerification.cs` | New. Four facts, `namespace ShatteredLegacy.Tests`, `[Collection("Sequential UOContent Tests")]`. |
| `docker/uo/docker-compose.yml` | One bind mount on `modernuo`, plus a one-line comment above it: `${SERVER_PATH}/lib/uo/modernuo/status:/var/lib/uo/modernuo/status`. |

**`docker-compose.yml` already had an uncommitted change that is not mine**: `RESOLVER_ADDRESS: "1.1.1.1:53"` on `ddns-updater`
(bug D23). I left it alone. `git diff docker/uo/docker-compose.yml` shows both, so commit them knowingly.

The container runs as root (the `Dockerfile` has no `USER`), so the publisher can write to the mount. It also creates the
folder if it is missing.

## Pinned citations (7c9215d97, all paths under `D:\UO\ModernUO-pinned\Projects\`)

**1. Connected clients and each one's mobile.**
- `Server/Network/NetState/NetState.cs:46` `private static readonly HashSet<NetState> _instances`, exposed at `:47` as
  `public static IReadOnlySet<NetState> Instances`. Added at `:115` on connect, removed at `:1068` in `Dispose`.
- `NetState.cs:201` `public Mobile Mobile { get; set; }`.
- Stock code iterates it the same way from timers on the main thread: `UOContent/Misc/FoodDecay.cs:24`,
  `UOContent/Gumps/WhoGump.cs:51`.

**2. In the world versus login or character select.**
- `NetState.Mobile` is assigned in exactly two places in pinned, both once a character has been chosen:
  `UOContent/Network/Packets/IncomingAccountPackets.cs:174` (character created) and `:261` (`PlayCharacter`), each followed
  by `m.NetState = state` (`:175`, `:262`). Grep: `\.Mobile = ` over `Server` and `UOContent`, non-test, finds only these two
  on a NetState. So at account login and character select `ns.Mobile` is null, which is how the publisher tells them apart.
- `Server/Mobiles/Mobile.cs:1244-1249` `NetState` getter returns the connection only while it is connected. Setting it
  moves a character parked on `Map.Internal` back to its `LogoutMap` (`Mobile.cs:1299-1302`). `Mobile.Map` is at `:2475`.
- The publisher's test, per connection: `ns.Mobile` not null, not `Deleted` (`Mobile.cs:2418`), `m.NetState == ns`, and
  `Map` neither null nor `Map.Internal`. The `m.NetState == ns` clause handles `PlayCharacter` taking over a character
  already logged in (`IncomingAccountPackets.cs:253`, `m.NetState?.Disconnect(...)`): the old connection stays in
  `Instances` until its dispose runs, still pointing at the character, and would otherwise count it twice.
- A character starts counting between `PlayCharacter` and `DoLogin` (the `LoginTimer` at `:491-527` waits for the client
  version). That window is tens of milliseconds and the character has been chosen, so I count it.

**3. Access level and hidden.**
- `Server/Mobiles/Mobile.cs:1031` `public AccessLevel AccessLevel`.
- `Server/Mobiles/Mobile.cs:1228` `public bool Hidden`.
- Names come from `Mobile.Name` (`Mobile.cs:1426`, `m_NameMod ?? m_Name`), not `RawName` (`:1419`). A disguised character is
  published under the name other players see, so the site never reveals who is behind a disguise.

**4. Repeating timer on the main thread, and registration at startup.**
- `Server/Main.cs:436-452`, the startup order: `_now = DateTime.UtcNow` (`:436`), `_firstTick` (`:437`), `Timer.Init`,
  `AssemblyHandler.Invoke("Configure")` (`:441`), `World.Load`, `AssemblyHandler.Invoke("Initialize")` (`:448`),
  `NetState.Start`, `EventSink.InvokeServerStarted` (`:452`), `RunEventLoop`.
- `Server/AssemblyHandler.cs:132-149` `Invoke(method)` calls every `public static` method of that name in every loaded
  assembly. Stock precedent for starting a repeating timer in `Initialize`: `UOContent/Misc/FoodDecay.cs:12-15`.
- `Server/Timer/Timer.DelayCall.cs:63` `Timer.StartTimer(TimeSpan delay, TimeSpan interval, Action callback)`, count 0
  meaning forever (`:64`, `:71-75`).
- **`Server/Timer/Timer.TimerWheel.cs:152` calls `timer.OnTick()` with no try/catch**, and the wheel is sliced from the main
  loop. So an exception in the callback leaves the event loop. `Publish()` catches everything for that reason.

**5. Server start time and last save.**
- Start: `Server/Main.cs:111` `Core.Uptime => TickCount - _firstTick` (milliseconds), `:109` `Core.Now`. The publisher takes
  `startedAt = Core.Now - Core.Uptime` in `Configure`, which is the `DateTime.UtcNow` of `:436`.
- Save: `Server/World/WorldEvents.cs:24-26` `EventSink.WorldSave`, raised at `Server/World/World.cs:308` on the main thread
  inside the `try`, after `Persistence.SerializeAll()` succeeded. The publisher records `DateTime.UtcNow` there.
  - **What that time means**: the moment the world was captured, not the moment the files reached disk. The write happens
    after, on a thread-pool thread (`World.cs:316`, `WriteFiles`), and a failed write would not change `lastSaveAt`.
  - **`lastSaveAt` is `null` until the first save of each process**, up to five minutes with the default
    `autosave.saveDelay` (`UOContent/World Saves/AutoSave.cs:38`). The key is always present. The widget does not read
    this field today (`docker/website/html/index.html`), so null is harmless.
  - Rejected: `Directory.SetLastWriteTimeUtc(SavePath, Core.Now)` at `World.cs:359` would survive a restart, but it runs on
    the thread-pool thread and reading a directory mtime through Docker Desktop's bind mount is a guess I cannot test here.
    `EventSink.WorldSavePostSnapshot` (`World.cs:357`) fires on that thread too.

**Path override**: `Server/Configuration/ServerConfiguration.cs:46-47` `GetSetting(string key, string defaultValue)`
reads without writing (unlike `GetOrUpdateSetting`, `:95-104`, which writes the default back into `modernuo.json`). Key
`shardStatus.path`, default `/var/lib/uo/modernuo/status/status.json`. Unset on the live shard.

## Behaviour

- Timer from `Initialize`: first write on the first turn of the event loop (delay zero), then every 30 seconds,
  unconditionally.
- Filtering constants at the top of the class: `HighestListedAccessLevel = AccessLevel.Player` and
  `ListHiddenCharacters = false`. Loosen either one to change who is listed.
- `names`: `SortedSet` with `StringComparer.OrdinalIgnoreCase`, so sorted case-insensitively and deduplicated
  ("Bram" and "bram" give one name, count 2), trimmed, empties dropped, first 50 kept. `count` is every listed character.
- Output is ASCII: `Utf8JsonWriter`'s default encoder escapes every non-ASCII character.
- Atomic write: write `status.json.tmp` beside the target, then `File.Move(tmp, path, overwrite: true)`, which is a rename.
  If anything fails before the rename, the temp file is deleted and the error rethrown to `Publish`.
- Failure: one `Warning` line naming the path, exception type and message, then silence for 10 minutes while every tick
  retries. On the first success after a failure, one `Information` line.
- Carries only the schema 1 fields. The shape test asserts the exact key set at every level, so a field added without the
  README changing first fails the build.

## Proof

Both runs were `docker/uo/build.sh -t <tag> --tests-only`: builder stage (patches plus compile), then the shard tests.
Neither built an image (`docker images sl-modernuo` has no `p6-*` tag), so `sl-modernuo:latest` is untouched and still
Chase's to build. No compiler warning mentions either new file in either log.

### Red: the tests against a stub

The real file was copied to this session's scratchpad and each of the four functions replaced with a stub that is wrong in
the way its test targets: `InWorld` takes every non-null `ns.Mobile`, `Players` returns every name unfiltered, unsorted and
uncapped, `Render` returns `{}`, and `WriteAtomically` is `File.WriteAllBytes` straight onto the target.

```
  Failed ...TheDocumentIsSchemaOneWithEveryFieldTypedAndNothingElse [2 ms]
   Assert.Equal() Failure: Collections differ
Expected: ["schema", "generatedAt", "shard", "players", "world"]
Actual:   []
     at ...ShardStatusPublisherVerification.cs:line 64

  Failed ...StaffHiddenAndCharacterlessConnectionsAreNeitherCountedNorNamed [4 ms]
   Assert.Equal() Failure: Values differ
Expected: 1
Actual:   3
     at ...ShardStatusPublisherVerification.cs:line 138

  Failed ...SixtyPlayersCountSixtyAndNameTheFirstFiftyCaseInsensitively [4 ms]
   Assert.Equal() Failure: Values differ
Expected: 50
Actual:   60
     at ...ShardStatusPublisherVerification.cs:line 168

  Failed ...TheFileIsReplacedWholeNeverRewrittenInPlaceAndLeavesNoTemp [62 ms]
   Assert.Equal() Failure: Collections differ
                          (pos 4096)
Expected: [..., 111, 111, 111, 111, 111, ...]
Actual:   [..., 111, 111, 110, 110, 110, ...]
     at ...ShardStatusPublisherVerification.cs:line 222

Total tests: 181
     Passed: 177
     Failed: 4
BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
```

Each one fails for its own reason:

- **Shape**: no keys at all.
- **Filtering**: 3 counted where 1 should be: staff and hidden were both let through. The connection at character select
  was still dropped, because even the stub skips a null `ns.Mobile`, so this red is about the access and hidden filter.
- **Cap**: `count` 60 passed (line 167), then 60 names where 50 should be (line 168).
- **Atomic write**: the red worth reading. A reader holding the file open across an in-place rewrite got the first
  4096 bytes of the old file (`o`, 111) and then the new one (`n`, 110). **That is exactly the half-and-half file nginx
  would serve**, measured rather than argued.

The real file was then restored from the scratchpad copy. `cmp` showed both files identical to the copies, and
`grep "P6 RED"` over `server/` was empty before the green run.

### Green

```
  Passed ...StaffHiddenAndCharacterlessConnectionsAreNeitherCountedNorNamed [3 ms]
  Passed ...TheFileIsReplacedWholeNeverRewrittenInPlaceAndLeavesNoTemp [29 ms]
  Passed ...TheDocumentIsSchemaOneWithEveryFieldTypedAndNothingElse [9 ms]
  Passed ...SixtyPlayersCountSixtyAndNameTheFirstFiftyCaseInsensitively [3 ms]
count=1 names=[Visible]
open reader saw 65556 bytes; old=65556 new=49172
Total tests: 181
     Passed: 181
exit=0
```

181 before this task was 177; P1 ended at 151, so 26 tests arrived between P1 and now, from other work.

## What the tests prove, and what they do not

- **Shape**: exact key sets at every level, types, `generatedAt`/`startedAt`/`lastSaveAt` parse as UTC in
  `yyyy-MM-ddTHH:mm:ssZ`, ASCII-only output with a non-ASCII name, and `lastSaveAt` present as `null` before a save.
- **Filtering** uses four real test NetStates (`PacketTestUtilities.CreateTestNetState`) and asserts they are members of
  `NetState.Instances`, so the test runs on the kind of object production enumerates. It covers staff, hidden, and a
  connection with no mobile.
- **Not tested**: the `m.NetState != ns` takeover clause and the `Map.Internal` clause of `InWorld`. Both come from reading
  source (section 2 above), not from a probe.
- **Not tested**: `Configure`, `Initialize` and `Publish`, meaning the timer, the catch-all and the rate-limited warning.
  The test fixture never calls `Configure`/`Initialize` (`UOContent.Tests/Fixtures/UOContentFixture.cs`), and the
  route forbids driving the wheel directly. They are small and were checked by reading. Chase's step 4 below is their first
  real run.
- **Atomic write is proven in the Linux builder container on its own filesystem.** It is **not** proven across Docker
  Desktop's bind mount onto NTFS and back out to `sl-uo-status`, which is where it actually matters. A rename there should
  still be one step, but that is unverified. Possible failure: if the rename is refused while nginx holds the file open,
  `Publish` logs one warning and retries on the next tick. A lasting failure shows up as a stale `generatedAt` and a
  `Shard status: could not write` line in `docker logs sl-modernuo`.

## Found in passing, not changed

- **The widget treats a timestamp from the future as offline.** `docker/website/html/index.html:326` shows "not answering"
  unless `age >= 0 && age < STALE_MS`. `generatedAt` has one-second precision and a viewer's clock can run behind the
  shard's, so a viewer whose clock is a second or more behind would see the shard as down. Suggested fix, not made because
  it is outside this brief: accept a small negative age, e.g. `age > -60000`. Unverified in a browser.

## Checklist for Chase

Every command below is for PowerShell 5.1 except `build.sh`, which runs from Git Bash as `AGENTS.md` says.

0. Commit the real publisher over the stub the 13:45 autocommit took (see the top of this note). First confirm the diff is
   only that file and that no stub is left:

   ```
   cd D:\ShatteredLegacy; git diff --stat; Select-String -Path server\customizations\ShardStatusPublisher.cs -Pattern "P6 RED"
   ```

   Expect one file changed and no `Select-String` output.

1. Build the image through the gate, from Git Bash:

   ```
   cd /d/ShatteredLegacy; docker/uo/build.sh
   ```

   Expect 181 of 181 and `Built sl-modernuo:latest`.

2. Pick up the new mount and image. **Only this service, never `down`** (the live shard and `sl-ddns` share the file):

   ```
   cd D:\ShatteredLegacy\docker\uo; docker compose up -d --no-deps modernuo
   ```

3. Delete the hand-made sample with fake names:

   ```
   Remove-Item D:\ShatteredLegacy\server\lib\uo\modernuo\status\status.sample.json
   ```

4. Log in with one character, wait a minute, then check that `https://shatteredlegacyuo.com/api/status.json` shows the
   name, and then the "Online now" widget on the site. While there: `generatedAt` should be at most 30 seconds old, and
   `docker logs sl-modernuo` should have no `Shard status:` line. A staff character will not appear; that is the filter
   working.
5. Stop the shard for 4 minutes (`docker stop sl-modernuo`, then `docker start sl-modernuo`) and confirm the widget says the
   shard is not answering. After the start it should recover within a few seconds, since the first write happens on the first
   turn of the event loop.
