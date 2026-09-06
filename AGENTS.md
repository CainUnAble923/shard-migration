# Working agreements for agents on this repo

Applies to any agent working here (Codex, Claude, or otherwise). Humans should read it too.

## What this project is

**Shattered Legacy stays on ModernUO.** ServUO is a **content source** we port from, one
system at a time, for as long as the shard is being worked on.

Scope is all the newer content, worked as an ongoing backlog with no completion date. That is
the point, not a compromise: ModernUO stays modern (.NET 10, source-generated serialization,
fast saves, real tests), every port leaves a working shard, and stopping anywhere is safe.

The direction moved several times on 2026-09-06 while scope was pinned down. It is settled.
Read `docs/direction-decision.md`, which records the full history, before proposing a change.

**There is no migration.** No cutover, no fresh world, no account export, no password window.
Our existing custom scripts are never rewritten.

`D:\UO\ServUO-pub57` is a **read-only content source**. Never edit it, never build in it,
never migrate to it.

Work is organised in `docs/workstreams.md`. Foundation blocks everything; the rest run
indefinitely and in parallel.

## Fidelity principle

**Port content unchanged.** The shard runs standard content so players can use existing wikis
(UOGuide, Stratics) instead of needing a custom one. Every deviation from OSI behaviour is a
documentation debt only we can pay. Keep ServUO's default values unless there is a recorded
reason. Prefer turning a system off over running it differently. Record any deliberate
deviation in `docs/fidelity-principle.md`. Full reasoning there.

## Ground rules

1. **Decisions live in `docs/`.** If you make or change one, write it there in the same change.
2. **Verify against the source trees, not documentation.** Neither ModernUO nor ServUO
   documents its content coverage accurately. Every content claim in `docs/` came from
   reading and counting files. Hold new claims to the same bar.
3. **State what you could not verify.** An explicit "unverified" beats a confident guess.
4. **Source evidence beats a stated rule.** If a rule here rests on a premise your evidence
   disproves, the rule is void, not merely in tension. Say so and open a question. This has
   already happened twice and both times the evidence was right.
5. **Never commit** `Saves/`, `Accounts/`, `client-data/`, `backups/`, `server/uo/`, or logs.
6. **Incremental and stoppable is the point.** Every ported piece should leave the shard
   working. Nothing in this project should ever require a migration event, a fresh world, or
   a compensation pass. If a piece of content cannot be added without one, decline it.

## Repo layout facts

```
D:\ShatteredLegacy               the shard. Infrastructure-as-code, NOT a ModernUO fork.
  server/customizations/         canonical custom scripts. 115 .cs, 38,986 lines. EDIT TARGET.
                                 (2026-09-06 snapshot; grows with every port. tools/progress.py
                                 recomputes it - that output is the live number.)
  server/patches/                overrides against stock ModernUO. 9 .patch + 5 replacements.
  server/migrations/             serialization migration JSONs.
  server/uo/modernuo/            build tree. NOT an edit target, NOT committed. See below.
  docker/                        compose stack; builds ModernUO from pinned commit 7c9215d97.

D:\UO\ServUO-pub57               ServUO, pristine. NOW A READ-ONLY CONTENT SOURCE.
D:\UO\shard-migration            this repo.
```

**`server/uo/` is a build tree** holding a full ModernUO checkout with our customizations
copied into `Projects/UOContent/Misc/`. Every custom file exists twice on disk. It is
**readable as a recovery source** but never an edit target, never committed, never a build
input. `server/customizations` is canonical.

**`D:\UO\ServUO-pub57` is now a content source, not a target.** Read it to find the content
we want. Copy what we need into `server/customizations`, rewritten for ModernUO. Never edit
it, never build in it, never migrate to it.

## Known defects in the current setup

These are real problems with the shard as it runs today, independent of any porting work.

1. **`server/customizations` does not compile on its own.** A clean build from pinned
   ModernUO plus only the canonical inputs fails. Missing: `CraftContext` members
   `RepeatCount`/`RepeatItem`/`RepeatTypeRes`; eight extended wood enum members in
   `ResourceInfo.cs`; `OutridersGuildmaster`. Recover each from `server/uo/` and write it
   into `server/customizations`. **This is the highest-priority work item.**
2. **`apply-patches.sh` is not a verification gate.** It converts patch failures to warnings
   and exits 0. Seven patches currently fail against the pinned source while the script still
   reports success. A runner that cannot fail is not a runner. Fix it, then determine which of
   the seven are genuinely needed.
3. **Stale divergent migration JSONs.** `server/customizations/migrations/` holds PetMimic
   v0-v2 that differ from the canonical set in `server/migrations/` (v0-v8). Currently inert
   because `apply-patches.sh` uses `-maxdepth 1`, but it is save-corruption material if the
   copy strategy ever changes. Delete it.

## Five files are upstream replacements, not additions

`CharacterCreation`, `CraftItem`, `HammerOfHephaestus`, `Meditation`, `RegenRates` share a
basename with pinned ModernUO sources and replace them. This is why `apply-patches.sh`
excludes them by name. Any change to how customizations reach the build tree must preserve
that routing. The other 106 are additive.

## Porting ServUO content: the rules

- **Pick by what the shard needs**, not by completeness. This is not a migration; there is no
  finish line to reach.
- **Leaf content first.** Items, decorations, food, fishing, crafting resources. Few
  dependencies, drops straight in.
- **Decline anything resting on a missing subsystem.** ModernUO ships zero files for Skill
  Masteries, Shadowguard, Myrmidex Invasion, Vendor Searching, Instanced Peerless. Content
  needing those is a subsystem build, not a port. Say so and stop.
- **Check for name collisions against ModernUO before porting.** ServUO has 5,902 script type
  names and ModernUO has its own; a collision is a duplicate-type build failure.
- **Convert, do not translate blindly.** ServUO's hand-written `Serialize`/`Deserialize` with
  a version int becomes ModernUO's `[SerializationGenerator]` partial class with
  `[SerializableField]` members. ServUO's `[Constructable]` is ModernUO's `[Constructible]`.
  `Serial` is signed in ServUO and `uint` in ModernUO.
- **Each port lands in `server/customizations` and must build** before the next one starts.

## Asking questions

Do not block on Chase to relay a question. Use `notes/codex-questions.md`. Read its
**Standing answers** first. If the question is non-blocking, pick the most reasonable option,
record the assumption, and keep working. If it genuinely blocks, mark it `[OPEN-BLOCKING]`,
stop that thread, and pick up something else. Claude answers in the same file.

`notes/` is Codex's to write freely. `docs/` is Claude's: put findings in `notes/` and they
get promoted after review.

## Keeping progress current

`tools/progress.py` counts real state from the working trees.

```
python tools/progress.py             # print, rewrite README block, write progress.json
python tools/progress.py --dry-run   # print only
```

Run it at the end of every work session and include the result in that commit.

`tools/expansion_coverage.py` gives the same picture by **expansion** rather than by
directory: how much of each era's content exists, how much ModernUO already ships, and how
much we have added. Run it after any batch of ports.

    python tools/expansion_coverage.py

Its coverage figures are filename-stem matches, a proxy for presence and not for behaviour,
and unclassified files fall into the Pre-AoS bucket. Directional, not precise. Do not quote
them as completion percentages.
**Its buckets still describe the old migrate-to-ServUO plan and need rewriting for the new
direction.** Do not trust the numbers until that is done.
