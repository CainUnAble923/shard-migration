# Shard Migration: ModernUO to ServUO

Working repo for moving the shard off ModernUO onto ServUO `pub57`, so the shard can
carry post-ML content (High Seas, Time of Legends, Endless Journey).

This repo is the shared source of truth for everyone working on the migration,
human or agent. If a decision is not written down here, it is not decided.

## Why we are doing this

ModernUO declares expansions through `EJ` but never implemented the content.
Measured by file count in each tree:

| Content | ServUO pub57 | ModernUO main |
|---|---|---|
| High Seas | 134 | 0 |
| Time of Legends / Eodon / Myrmidex | 74 | 0 |
| Ter Mur / Stygian | 18 | 5 (spawn data only) |

Target scope is the **full post-ML world including naval combat and Eodon**, which is
precisely the content ModernUO lacks. See `docs/direction-decision.md` for why porting
the other way was costed and rejected.

## What we give up

ServUO targets `net48` and runs under Mono off Windows, versus ModernUO's .NET 10.
Serialization goes from source-generated back to hand-written. This is a deliberate
trade of engineering quality for content reach. Do not relitigate it in code review.

## Layout

```
docs/     decisions and plans. Read these first.
tools/    converters and migration scripts (spawners, accounts)
notes/    working notes, scratch findings, anything not yet a decision
```

## Start here

1. `docs/migration-plan.md` - the seven phases, in order
2. `docs/direction-decision.md` - why ServUO and not the reverse port
3. `docs/shard-inventory.md` - what we actually have to migrate, and the revised Phase 2 scope
4. `docs/client-analysis.md` - what UOAlive and Immortal Realms customized, and the
   custom-facet finding that changes our map plans

## Current status

- [x] Direction decided: migrate to ServUO
- [ ] **URGENT** Deploy/restart the ModernUO image so startup enforces SHA2 password hashing
      (enforcement is staged in the shard infrastructure repo; live state is unverified)
- [x] Custom surface counted: **~131 files / ~39,900 lines**, already isolated from
      upstream. No Core bucket. See `docs/shard-inventory.md`
- [x] Shard located: `shattered-legacy-infrastructure` (builds ModernUO from pinned commit)
- [x] Add `client-data/` and `server/uo/` to that repo's `.gitignore`
- [ ] Stand up stock ServUO pub57 reference shard
- [x] Create the independent `ServUO-work` scratch clone; keep the pub57 reference pristine
- [ ] Write spawner JSON to XmlSpawner XML converter
- [ ] Write accounts exporter (MUO binary to ServUO accounts.xml)

## Migration progress

<!-- PROGRESS:START -->
**Overall: 1%** (2/138 tracked items). Counted from the working trees, not hand-maintained.

```
Baseline recovery  ░░░░░░░░░░░░░░░░░░░░░░    0/3     0.0%   canonical tree compiles
Content ports      ░░░░░░░░░░░░░░░░░░░░░░    1/111   0.9%   106 additive + 5 replacements
Patch triage       ░░░░░░░░░░░░░░░░░░░░░░    0/17    0.0%   11 .patch + 6 replacements, 0 found obsolete
Phase gates        ███░░░░░░░░░░░░░░░░░░░    1/7    14.3%   of 7 phases complete
```

| Phase | Status |
|---|---|
| 0 Freeze and inventory | in progress |
| 1 Stock ServUO reference | done |
| 2 Rewrite custom scripts | in progress |
| 3 Move accounts and spawners | not started |
| 4 Spawns and maps | not started |
| 5 Runtime and hosting | not started |
| 6 Verify and cut over | not started |

**Blocking Phase 2:** canonical tree does not compile. Missing:
- CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes)
- ResourceInfo extended wood enum members (8)
- OutridersGuildmaster

<!-- PROGRESS:END -->
