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
- **CC5 High Seas cheap half** (**77 candidates** (S9)) - two or three chats.

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

## S5. Translate one ML quest onto ModernUO's engine — DONE

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

## S8. Finish the test route — DONE

**Runs before CC6.** The S4 route has now needed extending on contact with a real case three
times, which is normal for infrastructure and is the argument for having built it before the
content. Two defects, both found by S5 and S6, both belonging in the route rather than in every
consumer.

**1. No `BaseCreature` can be constructed in a test** (Q-026). Every public constructor needs a
`Data/npc-speeds.json` table the test host does not load. S5 worked around it inside its own
fixture, which was right for S5 and is the wrong permanent answer: every creature test after it
would re-implement the same workaround, and a route that needs a workaround in every consumer is
not a route. **CC6 is 137 creatures away from needing this.**

**2. `Timer.Slice` advances the wheel, not the clock** (Q-029). A test that damages a mobile and
then slices is measuring `Mobile.HitsTimer`, not the thing it thinks it is measuring. That is a
test passing for the wrong reason, which is the most expensive kind, and it would be inherited
silently by every timing-dependent test written after it. The route needs one documented, correct
way to advance time.

**Prove both gates.** Per `AGENTS.md`: break it deliberately, watch the build go red, restore it,
watch it go green, and say so in the note. A gate nobody has watched fail is not a gate.

**Done when:** a test constructs a stock ModernUO creature and a ported one with no per-fixture
scaffolding; a timing-dependent test advances time correctly and demonstrably fails when the
behaviour under test is broken; S5's and S6's fixtures are moved onto the route's way of doing
both, so the workarounds do not survive as examples; and `notes/s8-test-route.md` documents how to
write a creature test and how to advance time.

## S9. Re-measure the remaining content backlog — DONE

**Measurement only. Do not port anything.** The last task of this shape, S3, shipped no code and
removed 223 files of backlog that did not exist. It was the highest-value hour this project has
spent.

**Every remaining content row is still an unfiltered ServUO file count.** Revamped Dungeons at
255, Artifacts and equipment at 466, Decoration/housing/crafting at 297, High Seas cheap half at
~78. The creatures row went **462 to 137** when the S3 filter was applied. These four are the
biggest items left on the plan and none has had that filter applied.

Apply the two-step S3/S6 method to each:

1. **Filter by what ModernUO already declares.** 3,134 of ServUO's 6,144 files are types ModernUO
   has; those are duplicate-type build failures, not candidates.
2. **Then resolve, because a reference count is an upper bound on work, not the work.** For what
   remains: how many are clean, how many are blocked and by what, and how many are blocked by
   something already built (armour sets, absorption, ML quests) and are therefore now free.

**Publish the file list beside every count.** Ten counts on this project have moved under
scrutiny; none of these four has been checked at all.

**Done when:** `notes/s9-backlog-remeasure.md` has a row per content task with filtered count,
resolved breakdown, blockers named, and a recommended order. Update `docs/tasks.md`'s figures via
`tools/progress-state.json` and run `python tools\progress.py`.

## S7. `Services/PointsSystems`

12 files, 2,857 lines, unblocks 55. A hard dependency of both Vice vs Virtue and City Loyalty, so
it gates two clusters currently sitting in the deferred list. Not scheduled; costed and available.

## CC9. Artifacts and equipment — START HERE

**Status table calls this `C6`.** Measured by S9 and it is the cheapest row on the whole backlog,
which is the reverse of how this plan used to be ordered.

**IN PROGRESS. 245 of 437 files ported across four batches; 448 customizations in the tree.**

Batches 1-4 done 2026-09-08. Batch 4 closed the two buckets S10 unblocked: the `GargishDagger`
re-parent (after measuring the no-instance condition against the live save's type table, three
backups and two archives), 40 of the 41 carrier-blocked files, and the set-armour bucket, which
was **85 files, not 79** — 79 set pieces plus 6 Phoenix suit files ServUO keeps under `Sets/`
without a `SetID`.

**Remaining: 120 plain, 29 in-row, 10 co-port, 44 upstream/carrier**, plus `Swiftflight`, which
Q-041 answers as a one-off `ISetItem` implementer rather than a sixth carrier.

**The client spot check is now the overdue item, not a batch.** `docs/client-check-backlog.md`
said "after CC9 lands, in one sitting". It covers **245 files** and nothing has been seen in a
client since June. Batch 5 does not depend on it, but every batch added to it is risk that only a
client can retire.

**Re-costed from a build rather than a count, by CC9 batch 1, and S9's figures were optimistic.**
S9 said 455 candidates with 320 dropping straight in, 88% needing nothing built. Reading the
files instead of counting them gives **437 real candidates, of which 272 need nothing built —
62%, not 88%.** The gap: **18 are already in ModernUO under other names** (gargish cloth, leather
and stone armour as `Gargish*Type1`/`Type2`, `SerpentstoneStaff`) and **must not be ported**;
**83 are set-armour re-parents** onto `BaseSetArmor`; and **41 are carrier-blocked** (Q-037).

Batch 2 then corrected batch 1's own bucket: carrier-blocked is **41, not 30**, because the
in-row bucket only ever checked the one member that put a file there.

**A green build hides this.** Batch 1 compiled 31 files clean on the first cycle while concealing
8 types that would not have compiled mechanically and 3 that should never be ported at all.
Compiling is necessary and is not sufficient.

Two findings that removed most of the apparent blocking, both verified:

- **`FlipableAttribute` is ModernUO's `FlippableAttribute`.** One extra letter, `Flip` body
  identical statement for statement. **86 files** of false blocking. With `ITool`, `IRepairable`,
  `IFlipable`, `ItemQuality` and four more, 169 file-references are a one-token transformation.
- **`IsArtifact` is worth zero.** It looked like a top-two blocker at 280 files here. Pinned
  ModernUO has no consumer of the name at all. Delete the line, log it once.

**`ReforgedSuffix`**: 138 hits, of which **136 are single cosmetic assignments and 2 are real
uses**. Delete the line for free, or build a ~100-line naming carrier plus four serialization
patches and four migrations, which frees 110, or **141 with the gargoyle wearables**. That
overlap is +24 over the sum of the two costed separately.

**Do this before the decoration row.** It delivers 9 of the 14 gargoyle files, which sequences the
two carrier classes correctly instead of building them twice.

**S9 compiled nothing.** Every "drops straight in" is a claim about names, not a build result.
Expect some of the 320 to fail and report how many.

**Batch it.** A changed-file build measured 86s and 95s in CC9, not the ~266s, so group files per build rather than rebuilding per
file. Report the real per-batch cost; the old estimates predate S4 and are optimistic by ~6x.

### CC9 batch 3 — the plain remainder, 49 named

Weapons (21), jewellery (11), armour and shields (17). Listed in `notes/cc9-artifacts.md` §11,
which says "~35 files" and "the 19 remaining" gargish weapons; **both are wrong and the list
itself is right** — ServUO has 20 `Gargish*` weapon files, three are already ported and
`GargishTalwar` is in ModernUO, leaving **16**. All 49 verified present in ServUO, absent from
`server/customizations`, and absent from `tools/modernuo-stems.txt`. Count the artifact, not the
sentence above it — the same error as Q-019.

**Eight of the 49 are not plain, and the difference is a save-format decision, not a style one.**
A base whose ServUO descendants use `AbsorptionAttributes`, `SetAttributes`, `SetSelfRepair`,
`SetID` or `ISetItem` must derive from the matching carrier **at port time**, because adding the
ancestor later is not expressible as a migration. Grepped ServUO for every one of the 48; these
eight have such a descendant:

| Port with parent | Types | Descendant that forces it |
|---|---|---|
| `BaseSetArmor` | `GargishPlateArms` | `VirtuososArmbands` (`SetID`, `Pieces`, `BardMasteryBonus`) |
| `BaseSetArmor` | `GargishPlateKilt` | `VoidInfusedKilt` (`AbsorptionAttributes.EaterDamage`) |
| `BaseSetArmor` | `DragonTurtleHideArms`, `Bustier`, `Chest`, `Helm`, `Legs` | Darden's set, all five |
| `BaseSetShield` | `GargishKiteShield` | `DragonHideShield` (`AbsorptionAttributes.EaterFire`) |

The other 41 stay on their stock ModernUO base. `SetID` defaults to `SetItem.None`, so a carrier
parent on a non-set base is inert — this is exactly what S10 did for the four gargish bases.

### CC9 batch 4 — the carrier-blocked 41, plus ONE re-parent

Unblocked by S10. Before the re-parent, **re-verify that no instance exists in any save**
(`docs/gap-register.md`, "The re-parenting window closes on the next deploy").

**The re-parent list is one type, not four.** Q-039 approved four on the general rule; Q-040
answered the general rule narrow and measured every ported type's ServUO descendants. Only
`GargishDagger` has one that needs a carrier (`StoneDragonsTooth`, `AbsorptionAttributes`), so it
moves from `BaseKnife` to `BaseSetWeapon`. `LargeStoneShield`, `GargishKatana` and
`GargishGnarledStaff` stay on their stock bases, and so do batch 3's 40.

Then the **79 set-armour re-parents**, mechanical once the stock parent's members are looked up.

## S10. The carrier family

**DONE 2026-09-08.** Five carriers, 1,426 lines against the ~1,000 below, **zero patches and zero
migrations** as predicted, 42 tests green, all five gates watched fail. The gargish question at
the end of this section was settled YES and applied in the same commit; Q-039 extends it to four
more types for batch 4. Two deviations recorded: `SetSelfRepair` is inert on weapon, clothing and
shield (Q-038, `docs/gap-register.md`), and the Bestial berserk line is omitted as on
`BaseSetArmor`. See `notes/s10-carriers.md`.

**Decided 2026-09-08 (Q-037). Ran before CC4.** Deferred by S1 and again by S6, both times
"until a batch needs them". Two rows need them now.

Build `BaseSetWeapon`, `BaseSetJewel`, `BaseSetClothing`, `BaseSetQuiver` and a shield carrier,
modelled on `BaseSetArmor` (394 lines including absorption). Roughly **250 lines each, ~1,000
total, zero patches, zero migrations**, plus one test per carrier.

**Frees:** 41 files in CC9, 110-141 in CC4, and 8 more carrying `NegativeAttributes`.

**Why it clears the bar Pet Training did not:** zero patches means a pinned-commit bump cannot
break it, and the timing objection that put Pet Training on WAIT does not apply. `SetHelper` and
the AOS aggregation patch already dispatch on all five bases (`SetItem.cs:62-78`). S1 built the
mechanism and wired one carrier to it; this finishes that.

**The alternative was rejected on fidelity, not cost.** Deleting the `ReforgedSuffix` line is free
and ships 136 items with wrong names. A player looking those up on UOGuide finds the wrong thing,
136 times, which is precisely what `docs/fidelity-principle.md` exists to prevent.

**Scope boundary:** carriers and their tests only. Do **not** port the blocked content here and do
**not** build `ReforgedSuffix` naming here. Those are CC9 batch 4 and CC4.

**Settle inside this task:** deriving the four ported gargish armour-class bases from
`BaseSetArmor` would free 9 of the 41 with no new carrier. It is a save-format decision, so make
it deliberately with the serialization consequence written down, and make it before those types
reach a live world.

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
