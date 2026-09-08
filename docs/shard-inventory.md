# Shattered Legacy: what we actually have to migrate

> **COUNTS SUPERSEDED 2026-09-07.** This says 111 customizations with 106 additive. It is now
> **198 files, 15 patches and 5 full-file replacements**, and the live figures come from
> `python tools/progress.py`. The *method* here (per-file classification against pinned ModernUO)
> is still how a customization gets triaged; only the numbers are historical.

Measured 2026-09-06 from `D:\ShatteredLegacy`.
Repo: https://github.com/CainUnAble923/shattered-legacy-infrastructure

## The good news: customizations are already isolated

This is **not** a ModernUO fork with edits scattered through it. It is
infrastructure-as-code that builds ModernUO from a pinned upstream commit
(`7c9215d97`) in Docker, and layers our own code on top. That is close to the ideal
starting position for this migration.

```
ShatteredLegacy/
  server/customizations/   <- canonical custom scripts, copied into the build tree
  server/patches/          <- the real upstream overrides
  server/migrations/       <- data migrations
  server/uo/modernuo/      <- working build tree, UNTRACKED, do not treat as source
  docker/                  <- compose stack, Dockerfiles
  design/                  <- system design notes
  client-data/ downloads/ backups/   <- binary, not source
```

## Phase 2 scope, measured

| Bucket | Files | Lines of C# | Notes |
|---|---|---|---|
| `server/customizations` | 111 `.cs` (114 total) | 37,581 | 106 additive files + 5 upstream replacements |
| `server/patches` | 6 `.cs` + 11 `.patch` | 2,078 | actual upstream overrides |
| `server/tools` | 1 `.cs` | 222 | |
| **Total custom surface** | **~131** | **~39,900** | |

Whole repo is 245 tracked files and a 3.4 MB `.git`. Small and clean.

Custom systems are prefixed `ClusterF*` (from the previous `clusterf-infrastructure`
name) plus Artificer, Arborist and BOD/mining extensions.

## What this means for the migration

The Phase 2 estimate in `migration-plan.md` was written not knowing this. Revised:

- **Content bucket** is mostly self-contained, but not entirely additive. Five files in
  `server/customizations` have the same basename as pinned ModernUO source files and replace
  them: `CharacterCreation`, `CraftItem`, `HammerOfHephaestus`, `Meditation`, and `RegenRates`.
  The remaining 106 files are additive by basename. Each needs its persistence rewritten
  from ModernUO's `[SerializationGenerator]` codegen to ServUO's hand-written
  `Serialize`/`Deserialize`, plus the `Serial` signedness sweep. Mechanical and highly
  patterned. This is the bulk but it is the *easy* bulk.
- **Override bucket** is only **11 real patches** plus 6 full-file replacements
  (`BaseGuildmaster`, `BulkMaterialType`, `JacobsPickaxe`, `LargeSmithBOD`, `Mining`,
  `ResourceInfo`). Re-apply by hand against ServUO stock files. Small enough to enumerate.
- **No Core bucket.** Nothing under `Projects/Server` is modified. That was the bucket
  that could have blown up the schedule, and it is empty.

Several patches target systems ServUO also has (`CraftGump`, `CraftItem`, `SmithBOD`,
`BulkMaterialType`, `Mining`, `ResourceInfo`, `Healer`, `BaseWeapon`). Check whether ServUO
already exposes the behavior before re-applying, since some exist only to work around
things ModernUO removed.

## Baseline verification findings (2026-09-06)

Verified by building a clean Docker context from pinned ModernUO `7c9215d97` plus only the
canonical tracked inputs (never `server/uo/`):

- The previous Docker build sourced `server/uo/modernuo/Projects/UOContent/Misc`, not
  `server/customizations`, so a successful old image did not prove the canonical tree complete.
- Copying the canonical directory wholesale into `Misc` produces duplicate definitions for
  `CharacterCreation`, `CraftItem`, and `Meditation`; replacements must be routed to their
  stock source paths.
- After routing all five basename collisions, the canonical-only build still fails because
  `CraftContext` lacks the `RepeatCount`, `RepeatItem`, and `RepeatTypeRes` members used by
  `CraftCountGump` and the custom `CraftItem`; `ResourceInfo.cs` lacks the eight extended wood
  enum members used by the lumber system; and `OutridersGuildmaster` is referenced but absent.
- Seven tracked patch applications report failure against the pinned source. The patch runner
  currently converts these failures to warnings and exits successfully, so its final success
  message is not a valid verification gate.

The missing canonical inputs and failing patches are verified. Their intended implementations
cannot be verified without another authoritative source; the generated `server/uo/` tree is
explicitly excluded and was not consulted.

## Hazard: `client-data/` is not gitignored

`client-data/` is 2.6 GB and untracked but **not** listed in `.gitignore`. A stray
`git add -A` in that repo would try to commit it. Add it to `.gitignore`, along with
`server/uo/` for the same reason.

## Codex / agent scoping

Point agents at `server/customizations`, `server/patches`, `server/migrations`,
`server/tools` and `design/`.

**Exclude `server/uo/`.** It is a build tree containing a full ModernUO checkout with our
customizations already copied into `Projects/UOContent/Misc/`. Every custom file appears
twice on disk, and an agent that reads both will not know which copy is canonical.
`server/customizations/` is canonical.
