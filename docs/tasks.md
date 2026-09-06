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

## CC2. Second port, timed — START HERE
Do a second creature using only the recipe, changing nothing else.

**Done when:** it builds, the recipe is corrected wherever it was still wrong, and you have
recorded roughly how long it took. That number prices every task below it.

## CC3. Eodon core content
**About 22 files, ~4,000 lines.** Corrected down from an earlier inflated figure of 52; see
`docs/eodon-separability.md` for what went wrong and the exact file list.

- Six creatures: Allosaurus, Archaeosaurus, Dimetrosaur, Najasaurus, Saurosaurus,
  SilverbackGorilla, plus `Mobiles/Normal/Raptor.cs`
- Ten artifacts: the eight Aloron armour pieces, RaptorClaw, TOL decoration artifacts
- The quest line: `Quests/Eodon/Creatures.cs`, `Items.cs`, `TigerCubEnclosure.cs`
- `RaptorTeeth.cs`, `MoonstonePowerGenerator.cs`

**Verify the list yourself before starting.** Confirm each is absent from stock ModernUO
(`tools/modernuo-stems.txt`) and references no Myrmidex or Shadowguard. If a file turns out to
be a large shared system that merely mentions Eodon, skip it and say so.

Work in batches of about five, building each batch.

**Done when:** all build, and the count moves in `python tools\expansion_coverage.py` under
Time of Legends.

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
About 360 candidate files, 0% dependency. Pure additive volume. Batch it.

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
