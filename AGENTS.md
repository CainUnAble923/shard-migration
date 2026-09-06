# Working agreements for agents on this repo

Applies to any agent working here (Codex, Claude, or otherwise). Humans should read it too.

## What this project is

Migrating a live Ultima Online shard from **ModernUO** to **ServUO pub57** so it can carry
post-ML content: High Seas, Time of Legends, Endless Journey. Target scope explicitly
includes naval combat and Eodon.

Read `docs/direction-decision.md` before proposing we do it the other way. That was costed
and rejected with numbers, not vibes.

## Ground rules

1. **Decisions live in `docs/`.** If you make or change a decision, write it there in the
   same change. A decision that exists only in a chat log does not exist.
2. **Do not relitigate the direction.** Going to ServUO costs us .NET 10, source-generated
   serialization and fast saves. That trade was made deliberately for content reach. If you
   have new *evidence* that changes the math, open it as a note in `notes/` with the numbers.
3. **Never commit shard runtime data.** No `Saves/`, no `Accounts/`, no logs. See `.gitignore`.
4. **Never commit client data files.** `.mul`, `.uop` and `.idx` are huge and not ours.
5. **Verify against the source tree, not against documentation.** Neither ServUO nor ModernUO
   documents its content coverage accurately. Every content claim in `docs/` was produced by
   reading and counting files in the actual repos. Hold new claims to the same bar.
6. **State what you could not verify.** An explicit "unverified" is worth more than a
   confident guess. Several findings here carry that label on purpose.

## Two facts that are easy to get wrong

- **ServUO targets `net48`**, on every branch including `p58-wip`. The .NET 10 in its setup
  instructions is the build toolchain, not the target framework. Linux and macOS run Mono.
- **The six-facet client ceiling is an official-client limit only.** ClassicUO reads map
  indices well past 5. Verified in the wild: Immortal Realms ships `map0.mul` through
  `map21.mul`. ServUO's core allocates 256 map slots. Custom facets are a real option.

## Division of labor

Mechanical, high-volume, patterned work is a good fit for an agent: serialization rewrites,
API drift sweeps, the converters in `tools/`. Deep subsystem design is not. Specifically,
grafting the High Seas galleon and cannon subsystem onto a different boat model, or
implementing missing systems like Skill Masteries, needs human judgment and play-testing.
An agent will produce something that compiles and is subtly wrong.

## Conventions

- One commit per ported or rewritten system. A bad port should be one revert.
- Build after each script, not after each batch.
- When re-applying a ServUO override, re-apply it **by hand** against the current stock file.
  Never copy an old file over a new one. That is how a shard ends up running two copies of
  the same system.

## The layering pattern is not negotiable

The shard 's existing architecture is: **pristine upstream pinned to a commit**, plus
additive `.cs` in `server/customizations/`, plus targeted `.patch` files in
`server/patches/`, assembled at build time by `docker/uo/apply-patches.sh`.

**This pattern is the reason the migration is cheap.** It is why there is no Core bucket
and why the custom surface is a clean ~131 files instead of a diffuse fork. Preserve it
with ServUO as the new base.

- `D:\UO\ServUO-pub57` is the **pristine reference**. Never edit, never commit into it.
  It exists so "is this mine or is this stock?" stays a one-minute question.
- `D:\UO\ServUO-work` (if present) is a **scratch tree** for figuring out ports. Not the
  deliverable. Create it with `git clone ServUO-pub57 ServUO-work`, not `git worktree`,
  so the reference repo's `.git` is never written to.
- **Final output lands in `server/customizations` and `server/patches`** in the shard
  repo, with a ServUO-targeted `apply-patches.sh`.
- **Do not commit our code into a ServUO fork.** A year from now, pulling ServUO fixes
  must still be a pinned-commit bump, not a merge.

Note that `apply-patches.sh` uses `-maxdepth 1 -type f -name '*.cs'` and deliberately
excludes several files by name because they are handled as patches instead. Any change to
how customizations reach the build tree must preserve both behaviors.

## Asking questions

Do not block on Chase to relay a question. Use `notes/codex-questions.md`.

Read its **Standing answers** section first; most questions are already decided there.
If yours is not, append an entry using the template. If the question is non-blocking, pick
the most reasonable option, record the assumption, and keep working. If it genuinely
blocks, mark it `[OPEN-BLOCKING]`, stop that thread, and pick up something else.

Claude answers in the same file and promotes durable answers into this document.

`notes/` is yours to write freely. `docs/` is Claude's lane: put findings in `notes/` and
they will be promoted after review.

## CORRECTION: `server/customizations` is not complete

Earlier guidance in this file said to ignore `server/uo/` entirely and treat
`server/customizations` as canonical. **That was wrong and is now corrected.**

Codex verified by building a clean Docker context from pinned ModernUO `7c9215d97` plus
only the canonical tracked inputs. It does not compile. Missing from `server/customizations`:

- `CraftContext` members `RepeatCount`, `RepeatItem`, `RepeatTypeRes`, used by
  `CraftCountGump` and the custom `CraftItem`
- Eight extended wood enum members in `ResourceInfo.cs`, used by the lumber system
- `OutridersGuildmaster`, referenced but absent

The old Docker build sourced `server/uo/modernuo/Projects/UOContent/Misc`, so a green build
there never proved the canonical tree complete. It did not.

**Revised rule:**

- `server/customizations` is the **edit target**. New and changed code goes there.
- `server/uo/` is **not** an edit target and must never be committed, but it **is** the
  recovery source for customizations missing from the canonical tree. Read it to recover
  what is missing, then write the recovered code into `server/customizations`.
- Recovering the canonical tree to a compiling state is a **prerequisite** to Phase 2
  porting. Do not port further scripts against an incomplete baseline.

## `server/customizations` contains five upstream replacements

It is not purely additive. These five share a basename with pinned ModernUO sources and
replace them, and must be routed to their stock source paths rather than dropped in `Misc/`:

`CharacterCreation`, `CraftItem`, `HammerOfHephaestus`, `Meditation`, `RegenRates`

This is why `apply-patches.sh` excludes several files by name. The remaining 106 are
additive. Any change to how customizations reach the build tree must preserve this routing.

## `apply-patches.sh` is not a verification gate

It converts patch failures to warnings and exits 0. Seven tracked patches currently fail to
apply against the pinned source while the script still reports success. Until that is fixed,
a green build proves nothing about whether patches applied. Treat fixing this as a priority:
a runner that cannot fail is not a runner.

## Cleanup: stale divergent migration JSONs

`server/customizations/migrations/` holds `Server.Items.PetMimic.v0/v1/v2.json` that
**differ** from the canonical set in `server/migrations/` (which has v0 through v8).

Currently inert: `apply-patches.sh` uses `-maxdepth 1 -type f -name '*.cs'`, and the
Dockerfile now stages `server/customizations/` to `/customizations/` rather than copying it
into `Misc/`, so the subfolder is skipped. It was briefly live when the Dockerfile copied
the directory wholesale.

It is still a landmine: divergent duplicates of serialization migrations, which is
save-corruption material if any future change alters how customizations reach the build
tree. Delete `server/customizations/migrations/` and confirm `server/migrations/` is the
only source of migration JSONs.
