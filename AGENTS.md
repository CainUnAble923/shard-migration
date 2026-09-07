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
   **Count the artifact, never a description of it.** **Seven for seven**: every count in this
   project stated without counting has been wrong, including two that were the basis of a
   decision and one inside a document whose own subject was miscounting. A keyword hit is a
   candidate, not a result. **Publish the file list beside the count.** When a source states a
   count and a list that disagree, neither is the answer: go count the thing. Never adjust the
   work to match a number in a document, including one in your own brief. Assume any figure in
   a brief, including one I wrote, is unverified until you have counted it yourself, and say so
   when it turns out wrong.
4. **Upstream conversation is a hypothesis, never evidence.** Chase is in the ModernUO Discord
   from 2026-09-07. What upstream says there is genuinely useful for *intent* - whether a gap is
   deliberate or just not built yet, what a pinned-commit bump will bring, whether a patch of
   ours conflicts with work in flight. It is **not** a source for what the code does. Nothing
   enters `docs/` or a decision on the strength of a chat message; verify it in
   `D:\UO\ModernUO-pinned` and cite the file and line. Never write "upstream says" as a
   justification, and never treat a Discord claim as outranking the source tree.
5. **Source evidence beats a stated rule.** If a rule here rests on a premise your evidence
   disproves, the rule is void, not merely in tension. Say so and open a question. This has
   already happened twice and both times the evidence was right.
6. **Never commit** `Saves/`, `Accounts/`, `client-data/`, `backups/`, `server/uo/`, or logs.
7. **Incremental and stoppable is the point.** Every ported piece should leave the shard
   working. Nothing in this project should ever require a migration event, a fresh world, or
   a compensation pass. If a piece of content cannot be added without one, decline it.

## `docker/uo/build.sh` is the build command

Since S4, `D:\ShatteredLegacy\docker\uo\build.sh` is how this shard is built: builder stage,
then the shard's own tests, then the image, each gating the next. **`docker build` and
`docker compose build` are internal steps of it, not things to run directly.** Running them
directly produces an image with no test gate and no warning.

The reason it cannot all live inside `docker build`: every ModernUO test fixture calls
`NetState.Configure()`, which needs io_uring, which Docker Desktop's default seccomp profile
blocks. `docker build` has no `--security-opt`, and the BuildKit entitlement alternative would
stop `docker compose build` working. Evidence in `notes/s4-test-route.md`.

## Chase's shell is Windows PowerShell 5.1

`&&` is not a statement separator there. Any command you hand him chains with `;` or goes on
separate lines. `cd D:\X && git push` fails; `cd D:\X; git push` works.

## The shard runs Endless Journey

`Configuration/expansion.json` sets expansion **Id 11, "Endless Journey"**, with `SA`, `HS`,
`TOL` and `EJ` all true, alongside T2A, UOR, LBR, AOS, SE and ML.

**This decides what content is in scope**, and it has already been needed twice without being
written down anywhere. Ter Mur, High Seas, Time of Legends and Eodon are all content this shard
is entitled to, so "does this belong here" is usually answerable from that file rather than from
judgment.

Configured is not the same as present: a facet being enabled does not prove its map files are
loaded and reachable. Check before placing anything on one.

## Repo layout facts

```
D:\ShatteredLegacy               the shard. Infrastructure-as-code, NOT a ModernUO fork.
  server/customizations/         canonical custom scripts. 191 .cs, 42,617 lines. EDIT TARGET.
                                 (2026-09-06 snapshot; grows with every port. tools/progress.py
                                 recomputes it - that output is the live number.)
  server/patches/                overrides against stock ModernUO. 13 .patch + 5 replacements.
  server/migrations/             serialization migration JSONs.
  server/uo/modernuo/            build tree. NOT an edit target, NOT committed. See below.
  docker/                        compose stack; builds ModernUO from pinned commit 7c9215d97.

D:\UO\ServUO-pub57               ServUO, pristine. NOW A READ-ONLY CONTENT SOURCE.
D:\UO\shard-migration            this repo.
```

**`server/uo/` is a stale partial build tree, and it is NOT a copy of ModernUO.** Counted
2026-09-06: it holds only `Configuration/` and `Projects/UOContent/Misc/`, 161 `.cs` in total.
109 of those are ours, 52 are stock ModernUO `Misc/` files, and five of our current top-level
customizations are missing from it entirely, so it predates the F1 recovery. It is never an
edit target, never committed, never a build input. `server/customizations` is canonical.

It was useful once as a recovery source for our own files (Q-001). It is useless as a place
to read ModernUO: **it contains 161 files where ModernUO has 7,058 types.**

**`D:\UO\ModernUO-pinned` is pinned ModernUO source, read-only.** Created 2026-09-06 and
verified detached at `7c9215d97cb25c56b0b5cb35034944ccdaa0a485`, 3,991 `.cs` files. Grep it to
answer every dependency question in seconds, offline, with no build cycle and no Docker:

```
findstr /s /c:"class LuckyCoin" D:\UO\ModernUO-pinned\Projects\*.cs
```

Treat it exactly like `D:\UO\ServUO-pub57`: never edit, never build in it, never commit into
it. Bump it only when the pinned commit in `docker/uo/Dockerfile` changes, and change both in
the same commit or the two silently disagree.

**Check dependencies here BEFORE the first build.** P2 lost a whole build cycle to a missing
`LuckyCoin`. Every `new X(` in a ServUO file gets checked against this tree first.

If the clone is ever missing, the builder stage of the Docker image holds the same source at
`/build/modernuo`: `docker build --target builder -t sl-uo-builder D:\ShatteredLegacy\docker\uo`.

**`tools/modernuo-stems.txt` is not a substitute.** It is a filename-stem list. It is correct
for collision-checking a ported type's own name and wrong for everything else: it reports
`ICommodity`, `TextDefinition`, `Ribs`, `ThighBoots` and `IronOre` as missing when all five
exist. Use the builder image for dependency checks.

**`D:\UO\ServUO-pub57` is now a content source, not a target.** Read it to find the content
we want. Copy what we need into `server/customizations`, rewritten for ModernUO. Never edit
it, never build in it, never migrate to it.

## Setup defects: all seven closed 2026-09-06

Kept as history because each one taught a rule. Findings in `notes/f2-patch-runner.md`,
`notes/f3-patch-triage.md`, `notes/f4-f5-foundation-cleanup.md`.

1. **`server/customizations` did not compile on its own.** Three pieces were missing and were
   recovered from `server/uo/`. Verified by a clean Docker build during F3, which is only
   meaningful now that a patch failure can no longer pass silently.
2. **`apply-patches.sh` was not a verification gate.** It converted patch failures to warnings
   and exited 0. It now fails the build, and it mirrors customization subdirectories by path.
   **Eight** patches were broken, not seven; **six had never been valid diffs** at all, and
   **none** was obsolete because ModernUO changed. Real effects: MAKE X never worked, PetMimic
   attributes were never aggregated, talisman durability never applied.
3. **Stale divergent migration JSONs** in `server/customizations/migrations/` are deleted.

**The rule all three paid for: verify state, do not trust a status line.** A green build
proved nothing while the runner could not fail, and a commit titled "Normalize patch runner"
had changed three lines of a Dockerfile.

## Five files are upstream replacements, not additions

`CharacterCreation`, `CraftItem`, `HammerOfHephaestus`, `Meditation`, `RegenRates` share a
basename with pinned ModernUO sources and replace them. This is why `apply-patches.sh`
excludes them by name. Any change to how customizations reach the build tree must preserve
that routing. The rest are additive, and ported content goes in subdirectories that
`apply-patches.sh` mirrors by path.

## Filter by what ModernUO lacks before any count means anything

**3,134 of ServUO's 6,144 script files have a primary type ModernUO already declares.** They are
duplicate-type build failures, not porting candidates. Measured in S3 by indexing all 7,097 type
declarations across the 3,991 pinned files.

**So any count phrased as "ServUO files that reference X" is roughly double what we would gain**,
and this project quoted such figures as backlog size for weeks. Concretely: `Mobiles/Normal` is
462 files and **137** candidates; the "103 creatures blocked by Pet Training" is **37** we would
gain, of which **4** are genuinely hard-blocked.

**Every count gets the filter applied and the denominator stated beside it.** A percentage
without its denominator written next to it is not a measurement.

## Equivalents hide under different names

Twice now a ModernUO feature has been recorded as missing because ServUO calls it something else,
and both times it cost real content:

- **`SetWeaponAbility`** → `BaseCreature.GetWeaponAbility()` (`BaseCreature.cs:1312`), overridden
  by 49 stock creatures. Made 57 files look blocked. **Transformation, not a decision.**
- **`TribeType`** → `OppositionGroup` (`UOContent/Mobiles/AI/OppositionGroup.cs:6`, used at
  `BaseCreature.cs:512` and `:1316`), same semantics for three of ServUO's four tribe pairs. Made
  53 files look blocked; only the goblin pair needs anything, ~25 additive lines and no patch.

**Before recording anything as missing, search pinned ModernUO for what it *does*, not what
ServUO *calls* it.** Zero occurrences of an identifier is evidence about a name, not about a
capability.

## Porting ServUO content: the rules

Read `docs/subsystem-policy.md` alongside these if anything you need is missing from ModernUO.
It carries the unblock-ratio test, when a patch into the ModernUO **core** project is allowed,
why a failing patch beats copied upstream logic, and why a ported subsystem ships with a test.

- **Pick by what the shard needs**, not by completeness. This is not a migration; there is no
  finish line to reach.
- **Leaf content first.** Items, decorations, food, fishing, crafting resources. Few
  dependencies, drops straight in.
- **A missing subsystem is not an automatic decline. Read `docs/subsystem-policy.md`.**
  This rule used to say "decline anything resting on a missing subsystem", which cost us
  content. It measured the wrong thing: "ModernUO ships zero files for X" says nothing about
  what X costs or what it frees. The armour set-bonus system turned out to be **one file, 387
  lines**, freeing **114**, and it had been declined on that rule.
  **Cost it by unblock ratio, and cost the smallest useful subset separately.** Then decline
  with the ratio recorded, or say it is worth building and stop for Chase to decide. Never
  build a subsystem inside a content task.
- **Losing a behaviour is not automatically a decline either.** `Saurosaurus` lost two of its
  three abilities and was still ported: correct stats, loot and taming beat no creature at all.
  Decline when the content is meaningless without what it loses. Log the deviation either way.
- **Check for name collisions against ModernUO before porting.** ServUO has 5,902 script type
  names and ModernUO has its own; a collision is a duplicate-type build failure. Use
  `tools/modernuo-stems.txt` for this and **only** this: it is a filename-stem list, correct for
  collision-checking a ported type's own name and wrong for anything else.
- **Resolve every dependency in `D:\UO\ModernUO-pinned` BEFORE the first build.** P2 lost a whole
  build cycle to a missing `LuckyCoin` because there was nowhere to look. There is now.
- **Walk the arrays, not just the file.** A dependency walk that stops at the file in front of you
  misses a `Type[]` one level down. S2 looked like ~900 lines and was 2,292, because
  `GemologistsSatchel` reads a 42-entry `Imbuing.IngredTypes` table and 35 entries were absent.
  Check every `new X(`, and then check the tables those types are registered in.
- **Convert, do not translate blindly.** ServUO's hand-written `Serialize`/`Deserialize` with
  a version int becomes ModernUO's `[SerializationGenerator]` partial class with
  `[SerializableField]` members. ServUO's `[Constructable]` is ModernUO's `[Constructible]`.
  `Serial` is signed in ServUO and `uint` in ModernUO.
- **Each port lands in `server/customizations` and must build** before the next one starts.

## Asking questions

Do not block on Chase to relay a question. Use `notes/codex-questions.md`. Read its
**Standing answers** first.

**Check whether the repo already answers it.** Q-021 asked whether an Underworld fixture belonged
on a shard without the Underworld; `Configuration/expansion.json` said the shard runs Endless
Journey with `SA` true, and ServUO's own generator carried the exact coordinates. Both were one
command away. A question that the source tree, the config, or `docs/` already answers costs a
round trip and reads as a judgment call when it is a lookup. Search first, ask second, and when
you do ask, say what you checked. If the question is non-blocking, pick the most reasonable option,
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
