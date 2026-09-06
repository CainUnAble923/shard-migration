# Claude Code: task list and working agreement

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

**Foundation is now yours.** Codex completed F1 only (the three missing pieces are recovered
and tracked, and the tree reportedly compiles). F2 through F5 remain, despite a commit titled
"Normalize patch runner" that only changed three lines of the Dockerfile. Verify state before
trusting any status; `apply-patches.sh` still swallows failures.

## CC0. Finish Foundation (F2-F5)

Do these before any porting. Details in `backlog.md`.

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

## CC1. Validate the port recipe
`notes/port-recipe.md` was drafted from source study, not from a build. Prove or correct it.

- Port one simple ServUO creature from `Mobiles/Normal` with no dependencies into
  `server/customizations`. Build it. Spawn it.
- Confirm or correct every claim in the recipe, especially the two fidelity traps:
  `DefaultRangePerception` being 16 in ModernUO where ServUO passes 10, and the two speed
  constructor arguments being replaced by a derived `GetSpeeds()`.
- Answer the three open questions at the bottom of the recipe.

**Done when:** it builds, spawns, and `notes/port-recipe.md` is corrected from experience
rather than inference.

## CC2. Second port, timed
Do a second creature using only the recipe, changing nothing else.

**Done when:** it builds, the recipe is corrected wherever it was still wrong, and you have
recorded roughly how long it took. That number prices every task below it.

## CC3. Eodon creatures
52 files, 6,607 lines, zero coupling to any subsystem ModernUO lacks. Dinosaurs and tribal
mobs, the most visible part of the Valley. See `docs/eodon-separability.md`.

Work in batches of about five. Build each batch before starting the next.

**Done when:** all 52 build, and the count shows up in `python tools\expansion_coverage.py`
under Time of Legends.

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
