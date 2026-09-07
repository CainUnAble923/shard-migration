# Task list and working agreement

**The single task list.** Any agent working this project uses this file. `backlog.md` is
superseded and kept only for its history. Live status renders into `README.md` and
`dashboard.html` from `tools/progress-state.json`; edit status there, not here.

Task IDs here match the IDs in that status table.

**Read `AGENTS.md` first.** This file assumes it.

## Your role

You are the **implementer**. You can compile, which the Claude in chat cannot: its sandbox has
no working NuGet and too old a C# compiler. That single fact defines the split.

- **You**: write code, build it, fix what the compiler says, verify behaviour, commit.
- **Claude (chat)**: cross-codebase research, drafts, reviews your commits, keeps `docs/`
  current, answers your questions. Call it "the overseer" if you like; it reviews, it does not
  merge.
- **Chase**: decides scope, priorities and anything touching the live shard.

## Where you work

| Path | What |
|---|---|
| `D:\ShatteredLegacy` | the shard. `server/customizations` is the edit target. |
| `D:\UO\ServUO-work` | scratch clone of ServUO. Read and experiment freely. |
| `D:\UO\ServUO-pub57` | **pristine reference. Never edit, never build in.** |
| `D:\UO\shard-migration` | this repo. `notes/` is yours; `docs/` is the overseer's. |

## The loop

1. Take the top unfinished task below. One task at a time.
2. Build after every file. Do not batch twenty ports and then compile.
3. Commit per logical unit with a message saying what and why.
4. Write findings to `notes/`. If something contradicts a doc, say so in the commit message
   and open a question rather than editing `docs/` yourself.
5. Run `python tools\progress.py` at the end of a session and commit the result.
6. Push. The overseer reviews from the pushed commits.

**Questions:** `notes/codex-questions.md` is the shared queue for any agent. Read its
**Standing answers** first. Non-blocking, decide and record the assumption. Blocking, mark
`[OPEN-BLOCKING]`, stop that thread, take the next task.

## One task, one chat

**Start a fresh chat for each task.** Context only grows within a session, and a porting run
that reads dozens of ServUO files climbs fast. High context means slower replies and
eventually compaction, where earlier detail is lost. That is precisely when an agent forgets
a standing rule like "port unchanged" or "check the destination exists before copying".

Nothing is lost by restarting: `AGENTS.md` and this file are re-read at the start of every
session, and the work itself lives in git.

**Split the large tasks further.** These are too big for one session:

- **CC4 Revamped Dungeons** (255 files, 6 dungeons) - one chat per dungeon. Start with
  DespiseRevamped (4 files), then Shame (11), Wrong (26), Covetous (29), Exodus (38),
  Blackthorn (147). Blackthorn is volume rather than complexity: many small armour variants.
- **CC6 Creatures and NPCs** (~360 files) - one chat per batch of roughly 20.
- **CC5 High Seas cheap half** (~78 files) - two or three chats.

**Signs the current session has run too long**, regardless of the percentage shown: it
re-reads files it already read, repeats work, restates conclusions it reached earlier, or
stops applying a rule it followed at the start. Any of those means restart now.

### What a task has actually cost

Measured, not estimated. Two data points, and they deserve different amounts of trust.

| Task | Files | Context used | 5-hour window | Agent wall clock |
|---|---|---|---|---|
| S2 | 38 ported, 1 patch, 5 tests | not recorded | not recorded | not recorded |
| CC3 | 17 ported, 29 verified | 278k of 1M (28%) | ~1% | ~17 min build, ~9 min verify |
| P2 | 2 ported, 462 surveyed | 231.5k of 1M (23%) | ~9% | ~20 min |
| P1 | 1 ported | ~492k of 1M (49%), **unreliable** | ~5% | not recorded |

**CC3 is now the best number for a real content task**: 17 files ported and 29 candidates
verified for 278k, in a fresh chat. Note where the time went. Writing and building 17 files took
8:34; deciding *which* files to port took 8:48. Verification is half the cost of a content task
and no estimate that ignores it will hold.

**P2 is the trustworthy number for a single port.** One task, one fresh chat, measured at the end. Note that a
large share of it was the one-time survey of all 462 `Mobiles/Normal` files that produced the
60/40 split. A port that reads only the files it ports costs less.

**P1's figure is not clean.** That chat had also run F2 through F5, so 49% covers four
foundation tasks plus a port, not a port. Do not size anything against it.

**What this is for:** a fresh chat starts near zero, so context is per-chat and a restart fully
resets it. The 5-hour and weekly limits are account-wide rolling windows and a new chat does
**not** reset those. At the observed rate a full task costs single-digit percent of a 5-hour
window, so context, not the plan limit, is the binding constraint on a long task.

**Stop well rather than badly.** On a task that batches, if context passes about 60% before the
work is done: finish the batch you are in, commit it, write what is done and what remains into
the task's `notes/` file, and stop. Say clearly that the task is partially complete and what the
next chat picks up. A clean handoff mid-task beats running out of room mid-batch.

## Hard boundaries

- **Never deploy to the live shard.** Building and testing locally is yours; `docker compose
  up`, restarts and image deploys are Chase's call.
- **Never touch** `Saves/`, `Accounts/`, `client-data/`, `backups/`, or commit `server/uo/`.
- **Never edit `docs/`.** Put it in `notes/` and it gets promoted after review.
- **Never change direction.** It moved three times in one day and is settled. New evidence
  goes in a question, not a rewrite.
- **Port unchanged.** See the fidelity principle in `AGENTS.md`. Deviating from OSI behaviour
  is a documentation debt only we can pay.

---

# Tasks

**Foundation is complete and CC1 is done, as of 2026-09-06.** Foundation is 7/7 and the port
recipe has been validated against a real build and a running client. `apply-patches.sh` no
longer swallows failures, and it mirrors subdirectories, so structured content is unblocked.

**Start at CC2.** Everything above it is kept for its history and its acceptance criteria, not
as work. Live status is in `tools/progress-state.json` and renders into `README.md` and
`dashboard.html`; the findings behind it are in `notes/`. Verify state for yourself before
trusting any status — that rule has already paid for itself three times on this project.

## CC0. Finish Foundation (F2-F5) — DONE

Completed 2026-09-06. Findings in `notes/f2-patch-runner.md`,
`notes/f3-patch-triage.md` and `notes/f4-f5-foundation-cleanup.md`. Kept for its acceptance
criteria and for what it turned up: eight broken patches rather than seven, six of which had
never been valid diffs, and none obsolete because ModernUO changed.

- **F2. Make `apply-patches.sh` fail on a failed patch.** It still converts failures to
  warnings and exits 0. Seven patches currently fail while the build reports success.
  *Done when:* a deliberately broken patch fails the build, and the real seven are listed
  with their errors in `notes/`.
- **F3. Triage those seven.** For each: still needed, or obsolete because ModernUO changed?
  Fix or remove with a one-line reason. Update `patches_triaged` and `patches_obsolete`.
- **F4. Delete `server/customizations/migrations/`.** Three PetMimic JSONs diverging from the
  canonical v0-v8 set in `server/migrations/`. Inert today, save-corruption material if the
  copy strategy changes.
- **F5. Make `RegenRates` routing explicit.** It works by accident: both it and ModernUO's
  land in `Misc/`, so ours overwrites. The other six replacements are explicitly routed.

Also verify F1 for yourself rather than trusting the flag: run a clean Docker build from
pinned ModernUO plus only tracked canonical inputs and confirm it succeeds.

**Done when:** all four are committed and `python tools\progress.py` shows Foundation 7/7.

## CC1. Validate the port recipe — DONE

Completed 2026-09-06. `PlagueRat` ported, built, spawned, saved and reloaded; three repaired
patches exercised at runtime. **Both drafted fidelity traps were wrong**, one exactly backwards.
The recipe is rewritten from what the build actually did. Full write-up in
`notes/cc1-p1-runtime-validation.md`; the speed decision it raised is answered as Q-008.

The original brief, kept because its acceptance criteria are the model for CC2 onward:

`notes/port-recipe.md` was drafted from source study, not from a build. Prove or correct it.

- Port one simple ServUO creature from `Mobiles/Normal` with no dependencies into
  `server/customizations`. Build it. Spawn it.
- Confirm or correct every claim in the recipe, especially the two fidelity traps:
  `DefaultRangePerception` being 16 in ModernUO where ServUO passes 10, and the two speed
  constructor arguments being replaced by a derived `GetSpeeds()`.
- Answer the three open questions at the bottom of the recipe.

**Done when:** it builds, spawns, and `notes/port-recipe.md` is corrected from experience
rather than inference.

## CC2. Second port, timed — DONE

Completed 2026-09-06. `GreaterPoisonElemental`, about 20 minutes end to end, headless. The
number and the phase split are in `notes/cc2-timed-port.md`. The brief is kept below because
its shape is the model for how a timed task gets scoped.

Do a second creature using only the recipe, changing nothing else. The deliverable is a
timing number, not the creature. Pick something representative of the ~360-file C4 batch:
a loot pack, and at least one thing PlagueRat did not exercise.

Use the recipe as written. If it is wrong, note it, work around it, keep the clock running,
and correct it after the timing is captured. A recipe fixed mid-run gives a number that no
longer describes what porting costs.

**Run this one headless. No client, and not on Chase's machine.** P1 needed ClassicUO because
it was verifying patch behaviour; a creature port does not. The compile is the real gate, and
body and hue values check against the ServUO source. Batches of 20 will never get a client
session each, so a timing number that includes one prices work nobody will do. Appearance and
AI behaviour get spot-checked later, five creatures at a time, not here.

**Done when:** it compiles in a clean Docker build, the server starts with the type registered,
the world saves and reloads clean, the recipe is corrected wherever it was still wrong, and
`notes/cc2-timed-port.md` has the phase breakdown, the total, and an estimate for a batch of 20
with the reasoning shown. Phases matter more than the total: build cycles are fixed cost and
the transformation is per-file, and that ratio is what prices every task below.

## CC3. Eodon core content — DONE

Completed 2026-09-06. **17 files ported, 12 declined**, not the "about 22" this file claimed.
That count was wrong for the third time. Evidence for every decision is in
`notes/cc3-eodon.md`; `docs/eodon-separability.md` now carries the correction.

Declined with evidence, all three genuinely blocked rather than skipped:

- **The eight Aloron armour pieces** rest on the armour set-bonus subsystem. `SetItem`,
  `SetAttributes` and `AbsorptionAttributes` are all absent from pinned ModernUO and `BaseArmor`
  has none of the plumbing. Plus the TigerPelt set, eight more unlisted files.
- **The Valley of One quest line** is 8 files and 3,870 lines, not 3 files, and rests on ServUO's
  Mondain's Legacy quest framework (6,269 lines) while ModernUO ships a different quest engine.
  A subsystem port, not a content port.
- **`MoonstonePowerGenerator.cs`** is Myrmidex Invasion content, in a directory named
  `Myrmidex Invasion`. It reached the list because "moonstone" matched.

Time of Legends coverage moved 53/157 to 59/157. Four build batches, zero failed builds.

**The lesson, now three for three:** every content count in this repo derived from keywords has
been wrong. Verify the list before porting it, publish the list beside the count, and expect the
decline set to be real work that was hiding inside an optimistic total.

## S1. Armour set-bonus subsystem — DONE

Completed 2026-09-07 in about 30 minutes. Spike passed all three stop conditions, so the content
followed in the same session. `SetItem.cs` plus **three targeted patches**, 44 added lines and 6
changed, none rewriting upstream logic and none bumping an upstream serialization version, so no
upstream migration is ours to maintain. Eight Aloron pieces and the TigerPelt armour ported.

**Read `notes/s1-armour-sets.md` section 3 before ever bumping `MODERNUO_COMMIT`.** It lists every
patched upstream file, what each patch assumes, and what breaks it. That is this task's ongoing
price and nothing else tracks it.

**The number that justified this task was wrong.** I claimed 187 files unblocked; the real figure
is **114**. See the correction in `docs/subsystem-policy.md`. The decision holds easily at 114.

~~One incidental finding worth carrying: a warm build cycle is 53 seconds.~~ **Superseded by S5,
2026-09-07.** Measured through `build.sh`: **20s with nothing changed, 266s with one changed
customization file.** The 53s and CC2's 0:44 both predate S4 and neither compiled nor ran the
tests. **Any batch estimate built on those is optimistic by about 6x.**

## S4. Test route for ported subsystems — DONE

Completed 2026-09-07. `server/tests/<path>` mirrors into `Projects/UOContent.Tests/Tests/<path>`,
and a failing test stops a build instead of living in `%TEMP%` with a paragraph asking someone to
re-run it. **Not a new mechanism**: F2's structured-customizations loop became `mirror_cs_tree()`
called twice, same destination-must-not-already-exist guard, everything F2 established unchanged.
No patch to an upstream project file was needed; `UOContent.Tests.csproj` has no
`<Compile Include>` items so the SDK's default glob picks the tests up.

Four negative proofs, each run and then removed: a failing assertion, a test that does not
compile, a test in the wrong namespace, and a test at an upstream path. All four fail the build.

**`docker/uo/build.sh` is now the build command for this repo.** See the entry in `AGENTS.md`.
A failing assertion fails `build.sh`, not `docker build`, because every ModernUO fixture calls
`NetState.Configure()`, which needs io_uring, which Docker Desktop's default seccomp blocks. The
BuildKit entitlement alternative would have stopped `docker compose build` working, so it was
rightly rejected. The gate also refuses to read "the filter matched no tests" as a pass.

**It landed four tests, not six.** My brief said six. The harness has four `[Fact]` methods and
always did. Q-019, and the fifth count this project has had to correct. The right thing was done:
the four landed unchanged rather than two being invented to match a number in a document.

## S2. Fountain of Fortune cluster — DONE

Completed 2026-09-07. **38 files, 2,292 ServUO lines, one patch, five new tests.** Closes Q-010:
`LuckyCoin.OnDoubleClick` is restored and pinned by a regression test, covering all twelve coin
droppers at once.

**My "roughly 900 lines" was wrong in both directions.** The core cluster is 465 lines across 4
files; the whole thing is 2,292 across 38, because `GemologistsSatchel` reads
`Imbuing.IngredTypes` and 35 of that table's 42 entries were missing from ModernUO. All 35 are
dependency-free leaf items, verified: a grep for `new X(` across all 31 `Items/Resource` files
returns nothing. So they were ported rather than worked around, and the ingredient table is
complete and verbatim.

**First content task to use S4's test route**, and the right call: the luck patch is exactly the
failure S4 exists to catch. A bump that stops routing loot through `Mobile.Luck` would leave the
patch applying and the build green while the reward silently stopped reaching the player.

Q-021 answered: nothing places a fountain yet. The OSI coordinates are Ter Mur
`(1121, 957, -42)`, from `Services/Underworld/Generate.cs:184`, and the shard runs Endless
Journey with `SA` true, so that is in scope. Small follow-on, not folded in here.

Q-022 answered and fixed in place: `build.sh` could not run its own test gate from Git Bash,
because MSYS rewrote `-w /build/modernuo` into a Windows path and the daemon error surfaced as
"tests did not pass".

## S3. Cost every remaining decline — DONE

Completed 2026-09-07, measurement only, nothing ported. `notes/s3-decline-costs.md` carries the
table, the file lists, the overlap analysis and the ranked recommendation.

**It found the error underneath every count this project has made.** 3,134 of ServUO's 6,144
script files have a primary type ModernUO already declares. See the new section at the top of
`AGENTS.md`. Every backlog figure quoted before today was roughly double what we would gain.

Ranked outcome:

- **Best ratio: `SAAbsorptionAttributes`.** One additive file against `BaseAttributes`, which
  ModernUO has, 57 files unblocked, closes S1's D-1 deviation, repeats S1's layering exactly.
  Now **S6**. Cost it at ~1,120 lines, not the ~350 headline: the smaller figure buys the
  property and tooltips, not the effect.
- **Best surprise: ModernUO already ships an ML quest engine.** 109 files, 240 quests, 205 of
  ServUO's 408 already present by name. The framework decline stands on two-engines-for-one-job,
  but the 203 missing quests are content work. Now **S5**, a spike. Q-023.
- **Strongest decline: Skill Masteries.** 35 upstream patch points for 14 files, against a
  `BaseCreature` upstream is actively refactoring. Fails questions 2 and 3 of
  `docs/subsystem-policy.md` at once.
- **`Services/PointsSystems`**: 12 files, 2,857 lines, unblocks 55, and a hard dependency of both
  Vice vs Virtue and City Loyalty. Better ratio than several things that were on the list and it
  was not on it. Now **S7**.
- **Pet Training buys fidelity, not throughput.** Of the 103, 37 are creatures we would gain and
  only **4** are genuinely hard-blocked, all four by a single override or guard. The rest degrade
  to deleting a one-line call, which is the `Saurosaurus` precedent and already settled.

## S5. Translate one ML quest onto ModernUO's engine — START HERE

A spike, with permission to fail, run the way S1 was. S3 established that ModernUO's `Engines/ML
Quests` **exists** and is **the same OSI system**; it did not establish that it is behaviourally
complete. This settles that.

Translate **one** ServUO quest end to end onto ModernUO's engine. Pick one exercising an objective
type on both sides of the mapping (ServUO Slay/Obtain/Deliver/Escort/Apprentice against ModernUO
Kill/Collect/Deliver/Escort/GainSkill), not the easiest one. `QuestionAndAnswerObjective` has no
counterpart and its 2 files are a separate question later.

**Done when:** it builds through `build.sh`, the quest is offered and completable, and
`notes/s5-quest-spike.md` says whether the mapping holds. A well-evidenced no in an hour is a
good result.

**If it passes**, the Valley of One and Myrmidex Threat quest lines come back into scope as
content, and CC3's quest decline is fully reversed.

## S6. `SAAbsorptionAttributes`

Best measured ratio on the menu. One additive file against `BaseAttributes`. 57 files unblocked,
and it closes deviation D-1 from S1, where all eight Aloron pieces lost `EaterCold`.

Cost at **~1,120 lines**, not ~350. The ~350 buys the property and its tooltips; the effect needs
`SAPropEffects.cs` or a patch. S3's dependency check confirmed the scary-looking parts are small:
`GetValue`'s `RunicReforging` term is a 16-line type switch, and the `Enhancement` and
`SkillMasterySpell` terms both return 0 on a shard without those systems.

## S7. `Services/PointsSystems`

12 files, 2,857 lines, unblocks 55. A hard dependency of both Vice vs Virtue and City Loyalty, so
it gates two clusters currently sitting in the deferred list. Not scheduled; costed and available.

## CC4. Revamped Dungeons
150 candidate files. Despise, Shame, Wrong, Covetous Void Spawn, Blackthorn, Exodus. Best
value on the backlog: places to go and things to fight, 2% dependency.

Expect more coupling than creatures: regions, spawn definitions, quest hooks. Take one
dungeon at a time, complete, before starting the next.

**Done when:** each dungeon builds and its spawns generate.

## CC5. High Seas, cheap half
Fishing overhaul, rare fish, crabs and lobsters, fish pies, sea creatures. About 78 files,
0% dependency. **Skip anything referencing `BaseGalleon`, `ShipCannon` or `Cannon`** - that
is CC8 and a separate decision.

## CC6. Creatures and NPCs

**The backlog is 137 files, not ~360.** 325 of ServUO's 462 `Mobiles/Normal` files have a primary
type ModernUO already declares (S3, Q-024). Every earlier figure here was against the wrong
denominator. Verified independently: 462 stems against every `.cs` name in pinned ModernUO gives
325 present, 137 absent.

Of those 137:

- **65 are blocked by something other than Pet Training.** This replaces the old "89", which does
  not reproduce at any definition — four candidate definitions give 206, 135, 81 and 65. **65 is
  the planning number and its definition is: files ModernUO lacks, blocked by something that is
  not Pet Training.** Method and file list in `notes/s3-decline-costs.md` section 10.
- **37 touch Pet Training, and only 4 are genuinely hard-blocked**: `CrimsonDrake`, `IronBeetle`,
  `PlatinumDrake`, `SabertoothedTiger`. Two are entangled only by a `TrainingDefinition` override
  and two only by a `PetTrainingHelper.Enabled` guard on a tamed-pet branch. **Four is an upper
  bound on blocked, not a floor.**
- **`TribeType` blocks nothing.** ModernUO's `OppositionGroup` covers three of ServUO's four tribe
  pairs with the same semantics; only the goblin pair needs ~25 additive lines and no patch. This
  alone removed 52 files from the raw missing-type scan.

**Losing an ability is not a decline.** `Saurosaurus` lost two of three and shipped. A creature
whose only entanglement is a one-line `SetSpecialAbility` call gets that line deleted and the
deviation logged.

**Batch from the clean set, state the filter you used, and never recompute a percentage against
462.**

## CC7. Decoration, housing, crafting
Addons, Decorative, New Magincia, Items/Resource, BulkOrders. 0% dependency. Cheap and
visible; this is what players spend time on.

## CC8. High Seas naval - proposal first
Galleons and cannons, about 54 files. Not blocked by a missing subsystem, but it means
extending ModernUO's `BaseBoat`. **Do not start.** Write a proposal in `notes/` covering what
changes to `BaseBoat`, what breaks, and roughly how long. Chase decides.

---

## Deferred, do not start

Each needs a subsystem ModernUO has zero files for. These are builds, not ports: Myrmidex
Invasion, Shadowguard, Skill Masteries, Vice vs Virtue, City Loyalty, Exploring the Deep.
The Valley of Eodon works without Myrmidex.
