# S8 — Finish the test route

**Status: done.** Committed 2026-09-07. Answers Q-026 and Q-029, and corrects Q-026's stated
cause, which was wrong.

Two defects in the S4 route, both found by other tasks, both now fixed in the route rather than
in every consumer. S5's and S6's workarounds are deleted, not relocated, and `apply-patches.sh`
fails the build for either of them coming back.

The gated build is green through `docker/uo/build.sh`: 15 patches, 6 test files, **27 tests**,
`sl-modernuo:s8` built, exit 0. Five negative proofs were run first; all five are in section 5.

---

## 1. How to write a creature test

Nothing. That is the fix.

```csharp
namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class MyCreatureVerification
{
    [Fact]
    public void ItConstructs()
    {
        var wolf = new GreyWolf();          // stock ModernUO
        var saur = new Saurosaurus();       // ported, from server/customizations
        ...
    }
}
```

The full route is still `notes/s4-test-route.md` section 1: a `.cs` file anywhere under
`D:\ShatteredLegacy\server\tests\`, `namespace ShatteredLegacy.Tests;`, the collection attribute,
then `docker/uo/build.sh`. S8 adds nothing a test author has to remember and removes eight lines
they used to have to copy.

`server/tests/Route/CreatureConstructionVerification.cs` is the worked example. It constructs a
stock creature and two ported ones with no scaffolding, and it asserts the **real** speed table is
loaded rather than a stand-in: a `Rat` comes out Slow (0.3/0.6) and an `AirElemental` Fast
(0.2/0.4), which is what separates the fix from the workaround it replaces.

## 2. Why this is a patch to an upstream test file

The brief said to argue this in `notes/` if the honest answer turned out to be a patch to an
upstream test-project file, the way S1 argued its core patch. It did. The argument was settled
from the probe in section 4 before the patch was written; it is written down here after, and the
ordering is stated rather than implied.

**What the defect actually is.** `Projects/UOContent.Tests/Fixtures/UOContentFixture.cs` calls a
hand-picked list of `Configure()` methods — `SkillsInfo`, `TestMapDefinitions`, `World`,
`RaceDefinitions`, `DecayScheduler`. The real server does not hand-pick: `Main.cs:441` runs
`AssemblyHandler.Invoke("Configure")`, which calls **every** public static `Configure` in every
loaded assembly, `NPCSpeeds.Configure` among them. `NPCSpeeds` is simply missing from the
fixture's list, so `_speedsByLevel` stays empty and every public `BaseCreature` constructor throws
`KeyNotFoundException` at `NPCSpeeds.GetSpeeds`.

**The patch is one call**, `server/patches/UOContentFixture-npc-speeds.patch`:

```csharp
        // Load Skills
        SkillsInfo.Configure();

+       Server.Mobiles.NPCSpeeds.Configure();
+
        // Configure networking (initializes RingSocketManager for tests)
```

Fully qualified rather than adding a `using`, to keep the hunk to one place.

**The alternatives, and why each loses.**

| Option | Why not |
|---|---|
| Keep S5's per-fixture workaround, moved into a shared helper | Still scaffolding every consumer must remember, and it registers **one** speed row. Every creature would come out Medium. CC6 is 137 creatures. |
| A `[ModuleInitializer]` in our own test file | Runs before `Core.ApplicationAssembly` is set. Touching `Core.BaseDirectory` there caches `""` permanently and breaks the whole assembly. |
| Our own copy of `NPCSpeeds.Configure`'s body | This is the thing `docs/subsystem-policy.md` forbids by name: sixty lines of upstream logic in our tree drifts silently on a bump, where a patch that no longer applies stops the build and names itself. **A failing patch beats copied upstream logic.** |
| Our own collection fixture alongside `UOContentFixture` | Impossible, not merely unwise. `UOContentFixture.Dispose` increments a **static** counter and throws `new Exception("NO!")` on the second disposal, so exactly one instance can exist per process. A second collection would construct a second one and blow up. Every shard test must stay in `"Sequential UOContent Tests"`. |

**Against the three questions in `docs/subsystem-policy.md`:**

1. **No `UOContent` hook exists** — the fixture is the only place that decides what a test host
   configures, and it is not extensible.
2. **It lives in the layering pattern** as one `.patch`, no forking.
3. **On a pinned-commit bump**, if upstream edits that region the patch stops applying and the
   build fails by name. If it applies but upstream changes what `Configure` does, every creature
   test fails loudly in the constructor. Both failure modes are loud. There is no silent one.

**And it is the safest patch in the tree**: it is the only one that touches a **test** project,
so it cannot change the shipped server. That is not an assertion — it is measured in section 6.

**Worth offering upstream.** It is a two-line fix to a fixture, it restores parity with what the
real server does, and upstream's own test at
`UOContent.Tests/Tests/Engines/Pathing/BitmapAStarAlgorithmTests.cs:356` carries a comment working
around the exact gap. Section E of `docs/gap-register.md` is where offers live; this belongs beside
the `SetPassword` report.

## 3. How to advance time

**Use `ShardTestClock`. Do not turn the timer wheel yourself — the build now refuses it.**

```csharp
ShardTestClock.Arm();                              // BEFORE scheduling anything

DamageEaterContext.CheckDamage(m, 100, 0, 0, 100, 0, 0, 0);

ShardTestClock.AdvanceSeconds(4);                  // or Advance(TimeSpan)
```

`server/tests/Route/ShardTestClock.cs` is the whole thing: ~70 lines of helper and three tests
that prove it.

- **`Arm()`** pins `Core.Now` to a fixed epoch (the test host leaves it at `DateTime.MinValue`, so
  any `Core.Now - TimeSpan` throws) and re-seeds the wheel to agree with `Core.TickCount`. It
  **empties the wheel**, which is why it must come before anything the test wants to fire.
- **`Advance(by)`** moves `Core._tickCount` and `Core._now` forward together in 8 ms steps — the
  wheel's own tick rate — slicing at each step. A callback due at t+3 s therefore runs with
  `Core.Now` reading t+3 s.
- `Advance` throws if `Arm` was not called, rather than silently wiping what the test scheduled.

**Why any of this is necessary (Q-029).** `Timer.Slice` turns the wheel and nothing else. Read
`Projects/Server/Timer/Timer.TimerWheel.cs:54`: it takes an **absolute** tick count, loops `Turn()`
until it has caught up, and never assigns to `Core._now`. The server's main loop moves the clock
first and slices second (`Main.cs:469-474`). A test that slices alone runs every callback against a
frozen present.

Three separate traps live in that one call, and the route now closes all three:

1. **A frozen clock.** S6's first eater test drove `AOS.Damage` and then sliced four seconds, and
   reported `healed=40 expected=3`. `Mobile.Damage` starts `Mobile.HitsTimer`
   (`Projects/Server/Mobiles/Mobile.cs:8910`), which does `Hits++` and re-arms every turn, so four
   seconds of wheel regenerated the whole hit. The test was measuring regeneration.
2. **The argument is absolute, not a delta.** Slicing to 4000 twice does nothing the second time.
   Every consumer that reads it as "advance by 4 s" is wrong on the second call.
3. **Re-initialising the wheel empties it.** S6's `Timer.Init(0)` was doing real work by accident:
   setting `m.Hits` below `HitsMax` starts `HitsTimer` (`Mobile.cs:2029`), and the `Init` dropped
   it, which is the only reason that test's arithmetic was deterministic. `Arm()` now does the same
   thing **on purpose**, and says so where the test can read it.

`SliceAloneDoesNotAdvanceTheClock` in the same file pins upstream's behaviour deliberately: it
schedules a one-second timer, slices four seconds, and asserts the timer **ran** while `Core.Now`
**did not move** and the callback saw the old time. If a future bump ever makes slicing advance the
clock, that test is what notices, and this file should be revisited rather than trusted.

**The gate.** `apply-patches.sh` fails the build for any mirrored test file that calls
`Timer.Slice` or `Timer.Init`, or that calls `NPCSpeeds.RegisterSpeed` or `NPCSpeeds.Configure`.
`Route/ShardTestClock.cs` is the single exemption, because one of its tests has to call the wrong
thing to prove it is wrong. Line comments are stripped before matching, so a test file may name and
discuss either rule freely — this note's rules are discussable in the code that obeys them.

## 4. Q-026's stated cause was wrong, and it mattered

Q-026 said:

> `NPCSpeeds.Configure()` fills it from `Data/npc-speeds.json` and returns **silently** when the
> file is not under `Core.BaseDirectory`, which in the test host it is not.

**The file is there.** Measured inside the builder image on 2026-09-07, before anything was
written, by a throwaway probe test:

```
Core.BaseDirectory = '/build/modernuo/Projects/UOContent.Tests/bin/Release/net10.0'
Data dir exists = True
Data file count = 272
npc-speeds.json exists = True
BEFORE Configure: new GreyWolf() THREW KeyNotFoundException: The given key 'Medium' was not present
NPCSpeeds.Configure() returned. MinIdle=15 MaxIdle=25
AFTER  Configure: new GreyWolf() OK, active=0.25 passive=0.5
```

`UOContent.Tests.csproj` already carries a `CopyData` target that copies `Distribution/Data/**`
into `$(OutDir)/Data`, and `Core.ApplicationAssembly` is set to the test assembly by the fixture's
first line, so `Core.BaseDirectory` **is** that output directory. Nothing was missing. Nothing ever
called `Configure`.

**Why this is worth a section rather than a footnote.** The stated cause and the real cause point
at different fixes. "The data file is not where the loader looks" is a build-system change —
`$(SolutionDir)` resolution, a Dockerfile copy, an `apply-patches.sh` step, a patch to a `.csproj`.
The real cause is one missing call. Had the brief been believed, S8 would have spent its budget
changing how data reaches the test host and might well have made the tests pass for a new wrong
reason, which is exactly what the brief warned about.

Both S5 and I had reasoned about `Configure`'s early return from reading its body, and neither of
us checked whether the file it looks for was on disk. **The rule this earns is the existing one
aimed one level lower: a plausible mechanism read out of source is still a hypothesis until the
artifact is looked at.** `AGENTS.md` already says to count the artifact rather than a description
of it. This is the same rule applied to a cause rather than to a count, and it is the eleventh
figure or claim on this project to move under scrutiny.

## 5. What was proved red

Per `AGENTS.md`, "a gate nobody has watched fail is not a gate." Five proofs, each broken
deliberately, watched fail, then restored.

| # | What was broken | Where it failed | Result |
|---|---|---|---|
| **A** | `UOContentFixture-npc-speeds.patch` moved out of `server/patches/` and its `apply_patch` line commented out | `build.sh` step 2 | **8 failed, 19 passed.** All four `CreatureConstructionVerification` tests and all four `AthenaeumIsleQuestVerification` tests red with `KeyNotFoundException : The given key 'Medium' was not present in the dictionary`. `BUILD FAILED ... No image was built`, exit 1 |
| **B** | A test file calling `Timer.Slice(4000)` and `Timer.Init(0)` | `docker build` step 1, in `apply-patches.sh` | `FAILED: Route/DeliberatelyBrokenRouteRules.cs — drives the timer wheel directly. Use ShardTestClock.Arm() then ShardTestClock.Advance()`, exit 1 |
| **C** | The same file calling `NPCSpeeds.RegisterSpeed` — S5's exact workaround, put back | `docker build` step 1, same run as B | `FAILED: ... registers NPC speeds by hand. The route loads Data/npc-speeds.json for every test ...; delete the workaround`, exit 1. Both B and C reported in one run, and the run named both |
| **D** | The behaviour under test: `DelayHeal`'s `TimeSpan.FromSeconds(3)` changed to `FromMinutes(3)` in `server/customizations/Abilities/SAPropEffects.cs` | `build.sh` step 2 | **Exactly one test red** — `ACompletedAloronSetEatsColdDamage`, `Expected: 73 Actual: 65`. `BUILD FAILED`, exit 1 |
| **E** | The clock helper itself: `Core._now = Core._now.AddMilliseconds(step)` deleted from `Advance`, leaving it a bare wheel turn | `build.sh` step 2 | **2 failed, 25 passed.** `AdvanceMovesTheClockByExactlyWhatItWasAsked` — `Expected 2026-01-01T00:00:10Z, Actual 2026-01-01T00:00:00Z`; `AdvanceFiresATimerAtTheRightTime` — the callback fired **`-00:00:03`** off the mark, i.e. three seconds early into a frozen present. `BUILD FAILED`, exit 1 |

Every temporary change was reverted and the clean gated build then went green end to end.

**Proof E is the one that earns its place, and it says something proof D does not.** Under E, the
damage-eater test **still passed**: the heal fires on wheel turns regardless of the clock, so the
eater test alone cannot tell a correct clock from a frozen one. Only the clock's own tests can. If
S8 had shipped `ShardTestClock` without them, the helper could have regressed to exactly S6's
original bug and nothing in the build would have said so — which is the F2 defect wearing its third
set of clothes.

## 6. The shipped server is provably unchanged

Rather than a runtime smoke run, which would only show that a server starts, the S6 and S8 runtime
images were compared directly:

```
sl-modernuo:s6   Server.dll 10a91058…  ModernUO.dll fd294a0c…  UOContent.dll bcb02482…
sl-modernuo:s8   Server.dll 10a91058…  ModernUO.dll fd294a0c…  UOContent.dll bcb02482…
                 UOContent.Tests.dll   0686e7c6…  →  c470c86b…
```

Byte-identical across every assembly the shard actually runs. The **only** thing S8 changed in the
image is `UOContent.Tests.dll`, which is the assembly it set out to change. `SAPropEffects.cs` was
edited for proof D and restored bit-identically — git reports it unmodified, and this hash agrees.

That is a stronger statement than a smoke run and it took thirty seconds. Worth reusing whenever a
change claims to be test-only.

## 7. S5 and S6 moved onto the route

Both workarounds are **deleted**, not kept alongside. If they stayed they would be the examples the
next author copies, and the defect would survive the fix.

- **`AthenaeumIsleQuestVerification.cs`** — the eight-line `EnsureNpcSpeedsTable` and its call are
  gone, along with `using System.Collections.Generic;` which existed only for it. A comment in its
  place says what used to be there and where the job moved. Proof A is what confirms it is really
  relying on the route now: with the patch removed, four of S5's five tests go red.
- **`AbsorptionAttributesVerification.cs`** — `AdvanceTimers`/`Timer.Slice` replaced by
  `ShardTestClock.AdvanceSeconds`, and the bare `Timer.Init(0)` by `ShardTestClock.Arm()` in the
  same position, with a comment saying what the `Init` had been doing by accident (section 3, trap
  3). `ColdDamageThroughAosDamageReachesTheEater` keeps its split design: S8's clock fixes the
  frozen-`Core.Now` half of that problem, but **regeneration during the wait is real behaviour** and
  would still swamp an 8-point heal, so asserting on the context rather than on hit points is still
  right. The comment now says which half was fixed and which was not.

## 8. Verification

Headless throughout. No client, not on Chase's machine, `--network=none` on every container,
scratch working files under `%TEMP%\claude\s8`. Nothing touched the live stack, `Saves/`,
`Accounts/`, `docs/`, or the uncommitted `docker-compose.yml` (Q-009). No deploy, nothing started
or restarted. `D:\UO\ModernUO-pinned` and `D:\UO\ServUO-pub57` were read only.

- **Gated build, clean:** `docker/uo/build.sh -t sl-modernuo:s8` — 83 structured customizations, 6
  shard test files, **15 patches applied**, **27 tests passed**, `sl-modernuo:s8` built, exit 0.
  Wall clock 6 m 54 s from a warm cache.
- **Five negative proofs:** section 5.
- **Upstream tests are undisturbed.** The fixture patch changes what every `UOContent.Tests` test
  sees, so it was checked against a pristine container built from the same image:
  - 65 tests across `DetectHidden`, `Tracking`, `SectorSpawnCache`, `SpawnPositionState`,
    `SpiralScan`, `EventScheduler`, `MLQuestPacket`, `WeaponAbilityPacket` and `CorpsePacket`:
    **65 passed with the patch, 65 passed without it.**
  - The 11 `BitmapAStarAlgorithmTests` — the suite whose source comments on this very gap — fail
    **identically with and without** the patch, with `FileNotFoundException : Data: tiledata.mul was
    not found`. Pre-existing: the builder image carries no client data. Not ours and not S8's.
  - **The full `UOContent.Tests` project still cannot be used as a comparison**: it hangs. Killed at
    600 s, re-confirming S4 section 5. Which upstream test hangs was not chased; it is not our gate.
- **Probe method:** a long-lived container from `sl-uo-builder:latest` with files `docker cp`'d in,
  so each iteration cost seconds instead of a 266 s image build. Six full `build.sh` cycles were
  still needed for the proofs, because a gate has to be proved through the gate.

## 9. Findings for `docs/`

1. **`docs/gap-register.md` D1 and Q-026 both state the wrong cause.** The file is present in the
   test host; the fixture never calls `Configure`. Section 4. The recorded fix ("one line in
   `apply-patches.sh` copying `Distribution/Data`") would have been unnecessary work against a real
   defect that was somewhere else.
2. **`AGENTS.md`'s "count the artifact, never a description of it" wants a sibling clause for
   causes.** A mechanism deduced from reading source is a hypothesis until the artifact is
   inspected. Both of us reasoned correctly about `Configure`'s early return and neither looked in
   the output directory. Section 4.
3. **`notes/s4-test-route.md` section 1 should point at this note** for the two things the route now
   does centrally, and section 8's "nothing tests the content ports" list should gain
   `server/tests/Route/` as a third category: tests of the route itself.
4. **The `UOContentFixture` patch is an upstream-contribution candidate**, section 2, for section E
   of the register.
5. **`tools/progress.py` still does not count `server/tests`.** S4 left it alone at one file; there
   are now six files and 27 tests, and the test count is the closest thing this project has to a
   regression-coverage number. Raised as Q-033.
6. **The runtime image ships 16 test-infrastructure assemblies.** Pre-existing, not S8's, measured
   here because the image comparison in section 6 walked past it. Raised as Q-032.

## 10. What it cost

| Phase | Wall clock |
|---|---|
| Read `AGENTS.md`, `docs/subsystem-policy.md`, S4/S5/S6/S8 in `docs/tasks.md`, `notes/s4-test-route.md`, Q-026 and Q-029 | ~9 min |
| Read the implementations: `NPCSpeeds`, `UOContentFixture`, `UOContent.Tests.csproj`, `Core.BaseDirectory`, `Timer.TimerWheel`, `Core._now`/`_tickCount` and their `InternalsVisibleTo`, `Mobile.Hits` | ~11 min |
| **Probe the running test host — the step that disproved Q-026's cause** | **~7 min** |
| Write the patch, the two route files, the `apply-patches.sh` validator, and move S5's and S6's fixtures | ~18 min |
| Fast iteration in a live container (all 27 tests, then upstream comparison against a pristine one) | ~9 min |
| **Five negative proofs, four `build.sh` cycles** | **~22 min** |
| Clean gated build with the runtime image, image comparison | ~8 min |
| This note, questions, progress | ~14 min |
| **Total** | **~98 min** |

The probe is seven minutes that changed the design. Everything after it followed from "the table is
already on disk and nobody asks for it"; the fix the brief described would have been a Dockerfile
or `.csproj` change, and it would have been solving a problem that does not exist.

A warm gated build cycle is **6 m 54 s** end to end, or about **5 minutes** with `--tests-only`.
That is up from S4's 2 m 20 s: 27 tests instead of 4, and 83 structured customizations instead of
39. Budget five minutes per proof, not two.

## 11. What S8 leaves for later

- **Q-018 is still open** from S4: whether to require an entitled buildx builder so plain
  `docker build` gates too, at the cost of `docker compose build`. Unchanged by S8.
- **Three questions raised, none fixed here.** **Q-031** asks whether `docs/gap-register.md` D1
  wants its cause corrected; **Q-032** is the 16 test assemblies in the runtime image; **Q-033** is
  `progress.py` not counting `server/tests`. All three are non-blocking, and all three were raised
  rather than fixed inside an infrastructure task that had a scope.
- **There is still no route into `Projects/Server.Tests`.** Unchanged from S4. Nothing needs one.
  Note that our new patch touches `UOContent.Tests` and is therefore covered by the same route it
  enables — the creature tests are its regression test.
- **`ShardTestClock.WheelTickMilliseconds` duplicates upstream's private `_tickRate`.** If upstream
  changes 8 ms, `Advance` loses step accuracy but not correctness, and
  `AdvanceFiresATimerAtTheRightTime`'s 16 ms tolerance would notice a large change. Add it to the
  bump checklist rather than trying to read a private field.
- **CC6 can start.** Both blockers named in its dependency are gone: a creature constructs, and a
  timing-dependent test measures time.

## 12. Extended by CC6 batch 1 (2026-09-19): the skill-check handlers

Third gap in the fixture's hand-picked `Configure` list, found the same way as the speed table: a
creature test failed for a reason that was the host's, not the creature's. `Mobile.CheckSkill` is
`SkillCheckLocationHandler?.Invoke(...) == true`, the real server assigns the four handlers in
`SkillCheck.Initialize` through `AssemblyHandler.Invoke("Initialize")` (`Main.cs:448`), and the
fixture never does, so **every skill roll in the test host fails**: `Stealth.OnUse` reveals the
user, and anything that rolls a skill takes its failure branch silently. `TrapdoorSpider`'s stealth
walk found it (`notes/cc6-creatures-batch1.md` §6).

Fixed where S8 fixed the speed table: one call added to `UOContentFixture-npc-speeds.patch`,
`Server.Misc.SkillCheck.Initialize();`. Alternatives rejected for the reasons section 2 gives: a
per-test assignment of the handler is the workaround-per-consumer this route exists to remove, and
dropping the assertion would leave a ported behaviour unverified because the host could not roll a
skill. `SkillCheck.Configure` (the stat-gain settings) is **not** called; it reads
`ServerConfiguration`, which the fixture does not load, and the handlers do not need it to decide a
roll. Proved red first: builds B and C failed on the spider fact with the handler unset, build E
passed with it set and nothing else changed in that fact.
