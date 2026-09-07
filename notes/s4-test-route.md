# S4 — Test route for ported subsystems

**Status: done.** Committed 2026-09-07. Answers Q-016.

`server/tests/<path>` is mirrored into `Projects/UOContent.Tests/Tests/<path>` by
`docker/uo/apply-patches.sh`, and `docker/uo/build.sh` runs those tests as a gate on the build.
S1's armour set-bonus tests are the first content in it.

---

## 1. How to add a test

1. Put a `.cs` file anywhere under `D:\ShatteredLegacy\server\tests\`. Subdirectories mirror by
   path; a top-level file lands directly in `Projects/UOContent.Tests/Tests/`.
2. Declare `namespace ShatteredLegacy.Tests;` (or a namespace beginning with it). **This is
   enforced** — `apply-patches.sh` fails the build for a test file that does not, because
   `build.sh` selects tests by that name and a test the filter never picks is a test that can be
   green while broken.
3. Use ModernUO's own fixture: `[Collection("Sequential UOContent Tests")]` on the class. It boots
   a headless world in about a second. Do not write a fixture of our own; see section 5.
4. Build with the gate:

```
docker/uo/build.sh
```

That is the whole route. There is no project file to edit: `UOContent.Tests.csproj` carries no
`<Compile Include>` items, so the SDK's default `**/*.cs` glob compiles anything under the project
directory at any depth, and `UOContent.Tests` is already in `ModernUO.slnx`. **Verified against
pinned `7c9215d97`.** Q-015's reasoning therefore never had to be applied — no patch to an upstream
project file was needed, so none was written.

Do not name a test file after an upstream one at the same relative path. `Gumps/TestLayoutGumps.cs`
would collide with ModernUO's own, and the mirror refuses to overwrite it (section 3, proof 4).

## 2. What a pinned-commit bump must run

Add this to the bump checklist in `notes/s1-armour-sets.md` section 3, which currently says
"re-run the verification harness in section 4". The harness is now committed, and the command is:

```
docker/uo/build.sh
```

It fails if any of our patches no longer applies (F2), if any test no longer compiles, or if any
test fails. Steps 1 and 2 alone, without building the runtime image:

```
docker/uo/build.sh --tests-only
```

PowerShell 5.1 has no shell for the script. The three commands it runs, from `D:\ShatteredLegacy`,
chained with `;`:

```
docker build --target builder -t sl-uo-builder:latest -f docker/uo/Dockerfile .
docker run --rm --network=none --security-opt seccomp=unconfined -w /build/modernuo sl-uo-builder:latest dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter FullyQualifiedName~ShatteredLegacy.Tests --logger "console;verbosity=normal"
docker build -t sl-modernuo:latest -f docker/uo/Dockerfile .
```

Running them by hand loses `build.sh`'s "a filter that matched nothing is a failure" check, so read
the test count.

## 3. What was built, and what each piece was proven to do

### `apply-patches.sh` — one mirror, two callers

The structured-customizations loop F2 wrote inline became `mirror_cs_tree()`, called twice:

```
mirror_cs_tree "structured customizations" "$CUSTOMIZATIONS" "Projects/UOContent"              2
mirror_cs_tree "shard tests"               "$TESTS"          "Projects/UOContent.Tests/Tests"  1  "ShatteredLegacy.Tests"
```

Same body, same destination-must-not-already-exist guard, same "NOTE: not installed (not a .cs
file)" report. Two arguments differ and both have a reason:

- **`mindepth`.** `server/customizations` uses 2 because its top-level `.cs` already means
  "additive into `Misc/`" and F2's `-maxdepth 1` copy owns those. `server/tests` uses 1 because a
  top-level test file has nothing else it could mean.
- **`require_ns`.** Tests only. See section 1, step 2.

Nothing else about F2 changed. Top-level customizations still go flat into `Misc/` with the same
seven name exclusions, subdirectories still mirror by path, every `.patch` file is still accounted
for by name, and a failed patch still fails the build. Verified by the same build that runs the
tests: 39 structured customizations installed, all 12 patches applied.

### `docker/uo/build.sh` — the build command for this repo

Three steps, each gating the next: builder stage (patches, then compilation), tests, runtime image.
It exits non-zero and builds no image if any step fails.

### Proofs run, all four

| Proof | Where it fails | Result |
|---|---|---|
| 1. A test asserting `1 == 2`, at the **top level** of `server/tests/` | `build.sh` step 2 | `Failed: 1, Passed: 4`, then `BUILD FAILED: ... No image was built`, exit 1. Also proved `mindepth 1`: `[patches] shard tests installed: 2 file(s).` |
| 2. A test that does not compile | `docker build` step 1 | `error CS0103` in `Projects/UOContent.Tests/Tests/DeliberatelyBrokenTest.cs`; publish exits 1 |
| 3. A test in the wrong namespace | `docker build` step 1 | `[patches] FAILED: DeliberatelyBrokenTest.cs — must declare 'namespace ShatteredLegacy.Tests'`, exit 1 |
| 4. A test at an upstream path (`Gumps/TestLayoutGumps.cs`) | `docker build` step 1 | `[patches] FAILED: ... would overwrite existing upstream file`, exit 1 |

All four temporary files were removed. The clean gated build then went green end to end: 12 patches
applied, 4 tests passed, `sl-modernuo:s4` built, exit 0.

**Proofs 2, 3 and 4 fail plain `docker build`.** Only proof 1 — a test that compiles and fails —
needs `build.sh`. That is the whole of the gap in section 5.

## 4. What landed: four tests, not six

`docs/tasks.md`, the S4 brief and Q-016's answer all say "S1's six tests". **There are four.**

`%TEMP%\claude\s1verify\ArmourSetBonusVerification.cs` is a single file with four `[Fact]` methods:
`AloronSetGrantsItsSetBonus`, `StockArmourIsUnaffected`, `TigerPeltAloneIsNotASetItem` and
`SetStateSurvivesASerializationRoundTrip`. There is no second harness file anywhere under `%TEMP%`.

The provenance is traceable. `notes/s1-armour-sets.md` section 4 says "**Four tests, all passing**"
and Q-016's *Context* says "Four tests". Q-016's *Answer* says "Land your six S1 tests", and
`docs/tasks.md` copied that. The six looks like a miscount of the eleven checks in the section 4
table, which is where the extra assertions actually live: `AloronSetGrantsItsSetBonus` alone covers
set completion, `LastEquipped` uniqueness, attribute aggregation, per-piece stacking, resistance
aggregation, self repair and set breaking. Nothing was lost. The count was wrong.

The four were committed **unchanged apart from the namespace and the header comment**. They were not
re-derived. Raised as Q-019.

**Five for five on counts stated without checking the list.** `docs/subsystem-policy.md` says to
publish the file list beside the count. This one was not even keyword-derived: it was a number
restated from a document that had the right number two paragraphs earlier.

## 5. The gate cannot live inside `docker build`, and why

**A failing test fails `build.sh`, not `docker build`.** That is a real gap against what S4 asked
for. It is environmental rather than a design preference, and here is the evidence.

Every ModernUO test fixture calls `Server.Network.NetState.Configure()` — `UOContentFixture.cs:30`,
`PathfindingTestFixture.cs`, and `TestServerInitializer.Initialize()`, which is what `ServerFixture`
uses. That reaches `IORingGroup.Create` and needs **io_uring**. Docker Desktop's default seccomp
profile blocks it:

```
System.InvalidOperationException : io_uring is not available (blocked by seccomp or kernel too old)
   at Server.Network.NetState.ConfigureNetwork() ... NetState.Network.cs:line 92
   at Server.Tests.UOContentFixture..ctor() ... UOContentFixture.cs:line 30
```

There is no fixture that avoids it, so "write the tests against a lighter fixture" is not an option,
and writing our own would mean copying upstream initialization logic into our tree — the thing
Q-015's answer forbids.

Measured, in this order:

1. `RUN dotnet test` in a plain `docker build` — the exception above. BuildKit's `RUN` runs under
   the daemon's seccomp profile, and `docker build` has no `--security-opt`.
2. `RUN --security=insecure` with `docker build --allow security.insecure` —
   `granting entitlement security.insecure is not allowed by build daemon configuration`. It needs a
   `docker buildx create --driver docker-container` builder carrying
   `--allow-insecure-entitlement security.insecure`. **`docker compose build` cannot pass an
   entitlement**, so taking that route would leave the compose deploy path unable to build the image
   at all. Rejected: breaking deploy to gain a gate is a bad trade.
3. `docker run --security-opt seccomp=unconfined` — works. Four tests in 1.0 s.

Option 3 is what `build.sh` does, and it is not a new requirement. `docker/uo/docker-compose.yml`
already sets `seccomp:unconfined` for the same reason, upstream ModernUO's own Linux CI runs its
containers with `--security-opt seccomp=unconfined`, and S1's harness needed it too.

**Is this the F2 defect wearing different clothes?** No, and the distinction is worth being exact
about. F2's runner *ran*, printed `FAILED`, and exited 0 — an active false green. Here, three of the
four failure modes fail `docker build` itself, and the fourth cannot report anything at all unless
`build.sh` runs it. The residual risk is "someone built the image without running the tests", which
is a *missing* signal rather than a lying one. It is still a real gap, so:

- `build.sh` is documented as **the** build command — in the script header, in `apply-patches.sh`,
  in the `Dockerfile`, and here.
- `build.sh` refuses to treat "the filter matched no tests", or a test count it cannot read, as a
  pass. A filter matching nothing exits 0 on some SDK versions; that is the one place this route
  could otherwise have gone green while broken, and it is closed.

Raised as **Q-018**, with the two options: leave it as it is, or require an entitled buildx builder
and accept that `docker compose build` stops working.

### Two other things measured while proving this

- **The full test suite is not usable as a gate here.** `dotnet test ModernUO.slnx` hangs
  indefinitely (killed at 10 minutes, container sitting at 0.3% CPU — blocked, not working), and so
  does `dotnet test` on the whole `UOContent.Tests` project. Filtered to our namespace it takes one
  second. Which upstream test hangs was not chased; it is not our gate.
- **Six upstream `UOContent.Tests` tests fail inside the builder image**, with
  `DllNotFoundException: Could not load libdeflate`. The builder stage installs no native libs; only
  the runtime stage does. Upstream CI installs `libdeflate-dev libzstd-dev libargon2-dev
  liburing-dev`, and adding them makes those six pass — verified. It was **not** done: our tests do
  not need them and it invalidates the whole layer cache. Worth knowing before anyone reads those
  six failures as ours.

## 6. Verification

Headless throughout. No client, not on Chase's machine, `--network=none` on every container, scratch
save directory under `%TEMP%\claude\s4run`. Nothing touched the live stack, `Saves/`, `Accounts/`, or
the uncommitted `docker-compose.yml` (Q-009). No deploy, and nothing was started or restarted.

- **Gated build, clean:** 12 patches applied, 39 structured customizations, 1 shard test file, 4
  tests passed, `sl-modernuo:s4` built, exit 0. Whole run 2 m 22 s from a warm cache.
- **Four negative proofs:** section 3.
- **Runtime smoke:** `sl-modernuo:s4` started against a scratch `Configuration`
  (`listeners: ["127.0.0.1:2593"]`), loaded the world, ran every ClusterF seeder, and reached
  `Listening: 127.0.0.1:2593` with **no exceptions**. `save` and `shutdown` were not re-driven:
  piped stdin is consumed by the owner-account prompt and the console reader wants a tty. S1 proved
  save and reload on this same content, and S4 changes no runtime behaviour, so this was not chased.

## 7. What it cost

| Phase | Wall clock |
|---|---|
| Read `AGENTS.md`, `docs/subsystem-policy.md`, S4 in `docs/tasks.md`, `notes/s1-armour-sets.md`, Q-015 and Q-016, `apply-patches.sh`, `Dockerfile` | ~8 min |
| Check how `UOContent.Tests` is actually structured and discovered in `ModernUO-pinned` — csproj globbing, `.slnx` membership, all three fixtures | ~4 min |
| **Establish whether the gate could live in `docker build` — three probes** | **~14 min** |
| Write `mirror_cs_tree`, the two call sites, the `Dockerfile` COPY, `build.sh` | ~7 min |
| Land S1's tests, first gated build | ~4 min |
| Four negative proofs, four build cycles | ~9 min |
| Runtime smoke run | ~6 min |
| **Total** | **~52 min** |

The seccomp investigation was a third of the task and none of it is visible in the diff. It is also
the only part that decided the design: every other choice followed from "the gate cannot be a `RUN`".

A warm gated build cycle is **2 m 20 s** — S1's 53 s plus the builder-stage image export and the
test run. Budget that, not 53 s, for anything that now has to pass the gate.

## 8. What S4 leaves for later

- **Q-018 is open**: whether to require an entitled buildx builder so that plain `docker build` gates
  too, at the cost of `docker compose build`.
- **Nothing tests the *content* ports**, and nothing should. This route is for subsystems, per
  `docs/subsystem-policy.md`: "Every subsystem built from here ships with a committed regression
  test." S2's Fountain of Fortune cluster is the next thing that should arrive with one.
- **`server/tests` mirrors `Projects/UOContent.Tests/Tests/`, not `server/customizations`.** S1's
  tests sit at `Items/Artifacts/Equipment/Armor/Sets/`, matching where the subsystem lives under
  customizations. That is a convention, not something the route enforces, and it is worth keeping.
- **`tools/progress.py` does not count `server/tests`.** It reports customization and patch
  counts from the trees; the test count is not in that line. One file today, so it was left alone
  rather than widened inside S4.
- **There is no route into `Projects/Server.Tests`.** Nothing we have needs one; a test aimed
  directly at a core patch would. `Mobile-set-item-resistance-hook.patch` is covered indirectly
  today, through `AloronSetGrantsItsSetBonus` reading `m.PhysicalResistance`.
