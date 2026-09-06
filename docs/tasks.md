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

## S1. Armour set-bonus subsystem — START HERE

**Reverses a decline. See `docs/subsystem-policy.md` for why the old rule was wrong.**

ServUO's armour set-bonus system is **one file, `Items/Artifacts/Equipment/Armor/Sets/SetItem.cs`,
387 lines**, and **187 ServUO files reference `SetItem`, `SetAttributes` or
`AbsorptionAttributes`**. Pinned ModernUO has none of it. That is an unblock ratio of roughly
187 to 1, the best in the backlog, and CC3 declined the eight Aloron pieces against it.

This is not a content port. It is a subsystem build, and the interesting question is not the
387 lines, it is the plumbing into `BaseArmor`, `BaseWeapon`, `BaseJewel` and `BaseClothing`.
Patching upstream base classes is what `server/patches/` is for, so the layering pattern should
hold, but **prove that before writing the whole thing.**

**Do the feasibility spike first, and stop if it fails.** Port `SetItem.cs`, wire the minimum
plumbing into one base class, and get one set item showing a set bonus. If that needs more than
targeted patches, if it means forking a base class beyond what a patch can express, stop and
write up what it would actually take. A negative answer delivered early is a good result.

**Then the eight Aloron pieces**, which are the proof the subsystem works on real content, plus
the TigerPelt set if it is cheap.

**Done when:** a clean Docker build with all patches applying, the server starting, the world
saving and reloading, and at least one set item verified to carry its set attributes. Record
what the next pinned-commit bump would have to reconcile, because that is this task's ongoing
cost and nobody else will track it.

## S2. Fountain of Fortune cluster

Also reverses a decline. `Items/Addons/FountainOfFortune.cs` (318 lines) plus a handful of leaf
items, roughly 900 lines total. The original decline assumed `EnchantedEssence` and
`RelicFragment` pull in Imbuing; they do not, both are leaf items in `SAQuestItems.cs` and
Imbuing only consumes them. Restores `LuckyCoin`'s `OnDoubleClick` and removes the Q-010
deviation. Small; do it after S1.

## S3. Cost every remaining decline

Produce the costed menu `docs/subsystem-policy.md` calls for: unblock ratio for Pet Training
(and for `SpecialAbility.cs` alone), the Mondain's Legacy quest framework, Myrmidex Invasion,
Shadowguard, Skill Masteries, Vice vs Virtue, City Loyalty, Exploring the Deep, Vendor
Searching and Instanced Peerless. Measurement only, no porting. The output is a table Chase
picks from.

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
About 360 candidate files. **The "0% dependency" figure was wrong** and P2 measured it properly
across all 462 files in ServUO `Mobiles/Normal`:

**Re-counted 2026-09-06 after CC3, by method rather than by cohort.** The earlier
"132 files touch Pet Training" was true and was being read as a decline rate. It is not one.

- **`SetWeaponAbility` is NOT blocked.** ModernUO has `BaseCreature.GetWeaponAbility()` at
  `BaseCreature.cs:1312` with `WeaponAbilityChance` at `:439`, 49 stock creatures override it,
  and every ability name matches. A `SetWeaponAbility` call ports to a `GetWeaponAbility`
  override. This is a transformation, not a decision.
- **57 files call `SetWeaponAbility`. 39 of those call nothing else blocked**, so 39 files move
  out of the "needs a decision" pile and into the portable one.
- **103 (22%) are genuinely blocked**: `SetSpecialAbility` (67), `SetAreaEffect` (19),
  `SetMagicalAbility` (18), `PetTrainingHelper` (15). None of those three has any definition in
  pinned ModernUO. These lose a real ability and each is its own call.
- **89 (19%) reference at least one type ModernUO does not have.** Port the dependency to the
  leaf like `LuckyCoin`, decline it like `FountainOfFortune`, or drop the creature. **This
  figure is CC2's and has never been independently re-counted.**

The groups overlap. CC3's sample is the useful calibration: 6 of 7 creatures were in the
"touches Pet Training" cohort and 6 of 7 ported anyway, so the real decline rate there was
about 14%, not 100%.

**Losing an ability is not automatically a decline.** `Saurosaurus` lost two of three abilities
and was still ported, following the `LuckyCoin` precedent: correct stats, loot and taming beat
no creature at all. Decline when the creature is meaningless without what it loses; log the
deviation either way.

**Draw batches only from the clean 275.** A batch of 20 sized against the one-hour estimate
will blow up if one Pet Training creature lands in it, and the fix is selection, not effort.
Filter first, then batch, and say which filter you used.

The Pet Training group gets scoped separately when someone chooses to take it on. It is
plausibly the single largest missing-subsystem decision left in the creature backlog.

**Budget:** roughly an hour per 20 clean creatures, so about 14 hours for the clean set,
across as many sessions. Build cycles are not the dominant cost; batch the builds anyway,
it saves about ten minutes in sixty.

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
