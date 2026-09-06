# Working agreements for agents on this repo

Applies to any agent working here (Codex, Claude, or otherwise). Humans should read it too.

## What this project is

**Migrating Shattered Legacy from ModernUO to ServUO pub57**, so the shard carries the full
post-ML content catalogue.

The direction reversed twice on 2026-09-06 as the scope was pinned down. It is settled now:
the scope is **all** newer content, not a subset, and at that scope porting into ModernUO
means rebuilding ServUO inside it. Read `docs/direction-decision.md`, which records the whole
history honestly, before proposing another change.

**ServUO's content is not work.** It ships in the box. Every workstream is about our side of
the line. See `docs/workstreams.md`.

**TIME-BOXED, do this first:** switch ModernUO's `accountSecurity.encryptionAlgorithm` to
`SHA2` while the old shard still takes logins, or every player needs a password reset at
cutover. Detail in `docs/migration-plan.md` Phase 0.

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
  server/customizations/         canonical custom scripts. 111 .cs, 37,748 lines. EDIT TARGET.
  server/patches/                overrides against stock ModernUO. 11 .patch + 6 replacements.
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
**Its buckets still describe the old migrate-to-ServUO plan and need rewriting for the new
direction.** Do not trust the numbers until that is done.
