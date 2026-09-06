# Shattered Legacy: ServUO content on ModernUO

Working repo for **staying on ModernUO** and pulling selected ServUO content into it,
piece by piece. Reversed from the original migrate-to-ServUO plan on 2026-09-06; see
`docs/direction-decision.md` for why.

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
**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece. There is no total to reach, so there is no single completion percentage here by design.

```
Setup health   #########.............  3/7   blocking defects resolved
```

| Setup defect | Resolved |
|---|---|
| CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes) recovered | yes |
| ResourceInfo extended wood enum members (8) recovered | yes |
| OutridersGuildmaster recovered | yes |
| server/customizations compiles standalone | **no** |
| apply-patches.sh fails on failed patch | **no** |
| stale server/customizations/migrations removed | **no** |
| RegenRates routing made explicit | **no** |

**Patches:** 17 total, **7 currently failing to apply**, 0 triaged, 0 found obsolete. `apply-patches.sh` still exits 0 on failure, so a green build proves nothing.

### Content moved over: 0 of 2,045 candidate files (0.0%)

```
Items/Artifacts                ..................    0/325     0.0%
Mobiles/NPCs                   ..................    0/222     0.0%
Services/Expansions            ..................    0/175     0.0%
Items/Addons                   ..................    0/169     0.0%
Services/Revamped Dungeons     ..................    0/150     0.0%
Items/Equipment                ..................    0/148     0.0%
Mobiles/Normal                 ..................    0/138     0.0%
Services/XmlSpawner            ..................    0/97      0.0%
Items/Decorative               ..................    0/88      0.0%
Quests                         ..................    0/84      0.0%
Items/Quest                    ..................    0/78      0.0%
Items/Resource                 ..................    0/61      0.0%
Items/Consumables              ..................    0/59      0.0%
Services/CleanUpBritannia      ..................    0/52      0.0%
Items/StoreBought              ..................    0/51      0.0%
Items/Functional               ..................    0/49      0.0%
Services/New Magincia          ..................    0/40      0.0%
Items/Containers               ..................    0/31      0.0%
Services/BulkOrders            ..................    0/28      0.0%
```

_Counted by matching ServUO file stems (excluding those stock ModernUO already has) against `server/customizations`. Auto-counted, never hand-edited._

**Ported systems logged: 0**

_None yet. Blocked until the setup defects above are resolved._

**Deliberately declined:**

- **Eodon / Time of Legends** — gated on Myrmidex Invasion (83% dep) and Shadowguard (71%), both subsystem builds. Deferred, not declined: measure how much of the Valley separates first.
- **Vice vs Virtue, City Loyalty, Skill Masteries, Exploring the Deep** — 29-100% dependent on subsystems ModernUO lacks entirely. Deferred to workstream 4.

Counted from the trees: 114 customization files, 16 patch files, stale migrations subfolder still present.
Shard status: running on ModernUO.
<!-- PROGRESS:END -->
