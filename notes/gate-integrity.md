# Gate integrity: the fireball flake and gumps in the test host

2026-09-26. Two defects in `docker/uo/build.sh`'s gate, both found by the New Haven quest board task
(`notes/new-haven-quest-board.md` 6.1 and 6.2), filed as **D7** and **D8** in `docs/bug-list.md`. Both are fixed.
**No D-number**: nothing here changes what a player sees. The changes are one test fact, one new test fact and one
new Dockerfile layer, and the running server's assemblies are byte-identical (B.4).

---

## Part A: the fireball fact

### A.1 The cause, plainly

**The fact's last assertion was false in the test host, and chance decided whether a run exposed it.** It was not
timing, the clock, test order, the dragon's AI or any other test.

1. **The test host regenerates one hit point every 8 ms.** `UOContentFixture` never runs `RegenRates.Configure`, so
   `Mobile.DefaultHitsRate` stays `TimeSpan.Zero` and `HitsRegenRateHandler` stays null
   (`Mobile.cs:8018`, `GetHitsRegenRate`). `HitsTimer` (`Mobile.cs:8910-8925`) therefore runs with a zero interval,
   `AddTimer` puts a zero delay in the next slot (`Timer.TimerWheel.cs`, "Round up if we have a delay of 0"), and a
   damaged mobile gains a hit on every wheel tick: **125 hits a second**. CC6's breath-incubator fact had already
   noticed this (`CC6FollowupBreathIncubatorVerification.cs:149`), and S6 designed around it
   (`AbsorptionAttributesVerification.cs`, above `ColdDamageThroughAosDamageReachesTheEater`).
2. **The player has 125 hits, not the ~300 the fact's comment assumed.** `pm.RawStr = 500` carried the comment
   "enough hits to take the fireball's 120-150 and stay alive". But ML caps a player's `Str` at 150
   (`PlayerMobile.cs:588-599`), so `HitsMax` is 150 / 2 + 50 = **125**.
3. **The fireball always lands, at t = 2.4 s**, for 120-150 chaos damage.
   - A roll of **126-150 kills** the player: hits stay at 0, and the fact passed.
   - A roll of **120-125 leaves the player alive**. They regenerate to 125/125 by about t = 3.4 s, and the fact
     asserted `Hits < HitsMax` at t = 4 s, so it failed.

That is **6 rolls in 31, 19.4% per run**, independent of anything else in the run. The fact only ever passed when
the fireball killed the player.

### A.2 How it was proved

| Step | Result |
|---|---|
| Probe: the fact's steps up to the fireball, **60 times in one process**, fact run alone | **15 of 60 did no damage.** State at the `DoStygianFireball()` call was **identical in all 60**: player alive, hidden, full hits, 5.0 tiles, combatant set, dragon unmoved. So the cause is after the call |
| Same probe, hits traced every 100 ms through the 4 s | Every iteration: **one hit at t = 2400 ms**. When it killed: `125 -> 0`, stays 0. When it didn't: e.g. `125 -> 5`, then `5 -> 17 -> 30 -> ... -> 125` by 3400 ms, **one hit per 8 ms** |
| **Fail on demand**: the fireball's own call, `AOS.Damage(pm, dragon, roll, false, 0,0,0,0,0, 100, 0, false)`, then the 1.6 s left of the fact's window, then the old assertion | **roll 120: red** (5 at the hit, 125 after), **roll 124: red** (1, 125), roll 126: green (0, dead). Deterministic, every run |
| Before-rate, **50 runs** of build.sh's step 2 verbatim on a builder of HEAD's tree | **8 of 50 red (16%)**, every one this fact, every one `fireball: player 125/125`. No other fact failed in 50 runs |
| Watch the new assertion go red: fireball damage zeroed in `StygianDragon.cs:442` (reverted, tree clean) | **red**: `Assert.InRange() Failure`, `Actual: 0`, `Range: (120 - 125)` |
| After-rate, **50 runs** of step 2 verbatim on the fixed builder | **0 of 50 red**, 137 passed every run. At the before-rate, 50 greens by luck is about 0.84^50 ≈ 2 in 10,000 |
| The fixed fact alone, 30 runs, detailed output | **30 of 30 green.** **4 of 30 drew the rolls the old fact failed on** (120, 122, 124, and one 125 that left the player alive at 0), each read exactly: `120 taken at 2400 ms, lowest 5/125` |
| **10 full `build.sh -t sl-modernuo:gate` runs** on the final tree | **10 of 10 green**, 137 each (A.5) |

"Step 2 verbatim" is the same `docker run` build.sh makes, with the same flags, filter and logger, repeated on one
builder image. It is the test gate without steps 1 and 3, which do not touch the tests. The 10 full runs are
complete `build.sh` invocations.

Combined, the before-rate is **23 in 110 (21%)** (8/50 in the gate, 15/60 in process), against the predicted 19.4%.

### A.3 What the brief's pointers turned out to be

- **`ShardTestClock`**: not involved. The timers survive between `DoStygianFireball()` and the `Advance`, and the
  hit lands on schedule every time.
- **The dragon's AI during the 40 s**: not involved. The state at the call was identical in all 60 probe iterations.
- **A time captured before `Arm()`**: nothing in the damage path reads one.
- **Streaks**: chance. The 50 before-runs, in order, were
  `RGGGRGGGGGGGGGRGGGRRGGRGGGGGGGGGGGGGGGRGGRGGGGGGGG`: one adjacent pair in 50 at a 16% rate. That is ordinary.
- **Passed 6/6 alone**: about 0.81^6 ≈ 28% by chance. The probe then failed 15 of 60 iterations, run alone.
- **The brief's 7 in 20 (35%)** is higher than my 16-21% but within the noise of 20 runs. The quest board note's
  "suggests a wall-clock dependency" (6.2) is wrong. There is none in this path.

### A.4 The fix, and why it is not a loosening

`CC6Batch8Verification.cs:627-656`. The fact now advances the same 4 s in 8 ms steps and records the lowest hit
reading. One `Advance(8 ms)` is one wheel turn, and the `HitsTimer` that the damage starts is due on the turn after.
So the lowest reading is exactly `HitsMax - damage`, or 0 on a kill. It asserts
**`taken` in `[min(120, HitsMax), min(150, HitsMax)]`**: the fireball's own range, capped at the 125 the player can
lose.

The old fact accepted **any** damage of 1 or more, read 4 s late. The new one requires **the fireball's range**,
read on the tick it lands. It is stricter, not wider, and it was watched going red. Same `Advance` total, no retry,
no skip. The wrong `RawStr` comment is corrected at `:591`.

**Other facts exposed to the same regen?** I grepped every hit assertion under `server/tests/`. This is the only one
that asserts on hits across an `Advance` after `Mobile.Damage` runs. The rest assert right after the damage call, or
never start the timer (S6's pair).

### A.5 Two `ShardTestClock` caveats found while reading, neither changed

Neither caused the flake. Both are true of the route today, and the header says to revisit it if its assumptions
break:

- **`Arm()` leaves dropped timers flagged `Running`.** `Timer.Init` swaps in fresh ring arrays but never clears
  `Running`, and `Start()` is a no-op while `Running` (`Timer.cs:108-111`). So an object created before an `Arm()`
  holds a timer that will never fire or restart. Harmless today, because every timed fact creates its objects after
  `Arm()`. A stale `Stop()` cannot corrupt the new wheel, because `InternalStop` checks identity (`Timer.cs:163`).
- **`Core.Now` is wall-clock after any fact that makes a test NetState.** `PacketTestUtilities.CreateTestNetState`
  sets `Core._now = DateTime.UtcNow` (`PacketTestUtilities.cs:62`). The quest board's facts and the new gump fact
  both call it. The clock still only moves forward, because real time is far past `Epoch`. But `Epoch` is not the
  process-wide base the header implies, and anything that reads the date or the time of day in a later fact sees the
  real one.

---

## Part B: the builder stage can now put a gump on a NetState

### B.1 The change

`docker/uo/Dockerfile:24-36`: **one new layer, right after the ModernUO clone**. It installs
`libdeflate-dev libzstd-dev libargon2-1`, with the same two `libargon2.so` symlinks and `ldconfig` as the runtime
stage. **Line 6 is untouched.** The runtime stage's `RUN` is untouched too, apart from a comment above it
(`:69`, keep the two in step). Comments are not part of a layer's cache key.

`ldconfig -p` in the new builder shows `libdeflate.so`, `libzstd.so` and `libargon2.so`.

### B.2 Which libraries, and why all three

**Exactly the runtime stage's list, less `ca-certificates` and `libicu-dev`, which line 6 already has.**

- **`libdeflate`** is the defect: `Deflate.Standard` is a `LibDeflateBinding` (`Server/Compression/Deflate.cs:26`),
  and `LibDeflate.Bindings` is referenced from `Server.csproj:39`.
- **`libzstd` and `libargon2`** are the same failure class, waiting for the first test that touches them. They back
  `ZstdNet` (`UOContent.csproj:50`: `ManagedArchive`, `AutoArchive`) and `Argon2.Bindings` (`:47`: account password
  hashing). Each is a native binding that throws on first use, and in a finalizer it would kill the host the same
  way. 2.1 MB for all three.
- **Not added:** `liburing-dev` and the `zstd` CLI. Upstream's prerequisite checker lists them for Debian
  (`BuildTool/Prerequisites/NativeLibraryChecker.cs:34`), but the runtime stage has neither. Adding them to the
  builder would give the tests something the server lacks (B.5). io_uring already works in the test host through
  `IORingGroup`. An observation only.

### B.3 Proof: one fact, watched red, then green, and kept

`server/tests/Route/GumpOnTheWireVerification.cs`, **kept**. It is the gate for this layer: if the builder ever
loses libdeflate again, the host dies here and build.sh goes red. It is about 125 lines and adds about 70 ms.

- It compiles a `DynamicGump` (background plus an html line), sends it with `pm.SendGump` to a player attached to
  `PacketTestUtilities.CreateTestNetState()`, and asserts `HasGump`.
- It then parses the 0xDD off `ns.SendBuffer`: length, serial, type id and x/y. It inflates the layout and the
  strings with the managed `ZLibStream`, **not** the native binding that packed them, so a pass means any zlib
  reader can decode the bytes. It asserts the layout elements, the string count, the text, and that the parsed
  lengths use exactly the packet.
- **Red first, on the unchanged Dockerfile**: `System.DllNotFoundException: Could not load libdeflate`,
  `Test host process crashed`, `Test Run Aborted`, **31 passed and then the host died**, exit 1. build.sh treats
  that as a failure.
- **Green after**: `0xDD, 183 bytes; layout 72 packed -> 74: { page 0 }{ resizepic 10 10 9260 265 140 }{ htmlgump
  30 30 150 75 0 0 0 }`, `strings: 1, 72 packed -> 94; first: Shattered Legacy gate: a gump reached the wire`.

### B.4 Build time and cache cost

- **Changing line 6, as the brief framed it, would have been the expensive route.** Every later layer rebuilds: the
  .NET SDK download and install, the ModernUO clone, and everything after. The runtime stage's
  `COPY --from=builder /usr/local/dotnet` layer would also get a new digest, so the SDK layer ships again.
- **As placed, the change costs one 5.6 s, 2.1 MB layer, once.** The build log shows the line-6 apt layer, the SDK
  install and the clone as `CACHED`. The first builder build took 2m41s, nearly all of it the `dotnet publish` that
  reruns on every change anyway. The ten full `build.sh` runs afterwards took 12-18 s each.
- **The running server is unchanged.** Against `sl-modernuo:qboard` (HEAD's FINAL), all **479 files under
  `/modernuo` hash identical except `UOContent.Tests.dll` and `.pdb`**. Those are the test assemblies the runtime
  ships anyway (D6), and they changed because Part A changed a test. `Server.dll`, `ModernUO.dll` and
  `UOContent.dll` are byte-identical. The runtime stage's apt layer has the same digest as in `qboard`.
  (My first hash pass used `xargs` without `-0` and silently skipped files with spaces in their names. The numbers
  here are from the redone pass.)

### B.5 Could this hide a real difference between the stages? Yes, in one direction

**The risk:** if someone later removes a library from the runtime list and not from the builder's, the tests pass
and the server crashes on first use. That is exactly the "green while broken" shape.

**What limits it:** the builder list is exactly the runtime list, not a superset. Both places carry a "keep the two
in step" comment. The builder's extra packages (`curl`, `git`, `gcc`, `patch`) are build tools, which shard code
never loads. So a native library the tests can reach is one the runtime also has, as long as the two lists are kept
together.

**What would remove it, and why it is not done here:** one source for the list, either a shared base stage or a
global `ARG` used by both stages. Either rewrites the runtime stage's `RUN`. That rebuilds its layer, may pull newer
Debian package versions into the running image, and is more than the line or two the brief allowed. Worth doing if
the list ever changes. Until then, the comments are the control.

The opposite direction was the old state. A library in the runtime and missing from the builder is loud (the host
crashes), not hidden. It made a whole class of fact impossible, but it never faked a pass.

---

## For `docs/bug-list.md`

- **D7: close.** Not flaky timing. The fact asserted a hit was still visible 4 s later in a host that regenerates
  125 hits a second, and it passed only when the fireball killed. 19.4% per run by construction. Measured 8/50 on
  HEAD, 0/50 after, plus 10/10 full `build.sh` runs. Fixed in the fact by reading the hit on the tick it lands and
  asserting the fireball's 120-150 range. This note, Part A. The "4 in 10" and "streaks" in the entry were noise.
- **D8: close.** The builder stage now installs the runtime stage's native libraries in its own layer. A kept fact
  sends a gump and reads it back, and was watched red on the old Dockerfile. This note, Part B.
- **New, route, ours to decide (Q-060):** the test host never runs `RegenRates.Configure`, so every damaged mobile
  in every fact regenerates one hit per 8 ms. Any fact that reads hit points across an `Advance` after damage
  measures regeneration. One fact was bitten (D7) and two already work around it.
- **New, low:** the two `ShardTestClock` caveats in A.5.
- **Stale:** the header of `NewHavenQuestBoardVerification.cs` still says no fact there can send a gump. Not
  touched here, because Q-058's picker task will rewrite that file and should drop the sentence then.

## Questions

**Q-060** (not blocking): should the route configure realistic regeneration? See `notes/codex-questions.md`.

## FINAL

`build.sh -t sl-modernuo:gate` on the final tree: **green on attempt 1**, and on each of 9 further attempts made as
the after-measurement. **10 of 10 green, 137 passed each, no fact failed on any attempt.** Image
**`sl-modernuo:gate` (`0a4a2f8c9373`)**. **Not tagged `latest`**: `sl-modernuo:latest` is still `07f8a69f4115`. As
it always does, build.sh retagged `sl-uo-builder:latest`.

Attempt 1 took 18 s because its builder layers were cache hits from a manual builder build of the identical tree
minutes earlier (`sl-uo-builder:gate`, the 2m41s build in B.4). So that build did the compiling, and attempt 1 ran
the same image through the tests.

`tools/progress.py` counts 138 tests against xUnit's 137, the same off-by-one as D11, unchanged.

Scratch images left from this task, safe to remove: `sl-uo-builder:probe`, `sl-uo-builder:gump-red`,
`sl-uo-builder:before`, `sl-uo-builder:gate`. The probe fact (`FireballFlakeProbe.cs`) was deleted and never
committed.
