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
Setup health   ################......  5/7   blocking defects resolved
```

| Setup defect | Resolved |
|---|---|
| CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes) recovered | yes |
| ResourceInfo extended wood enum members (8) recovered | yes |
| OutridersGuildmaster recovered | yes |
| server/customizations compiles standalone | yes |
| apply-patches.sh fails on failed patch | yes |
| stale server/customizations/migrations removed | **no** |
| RegenRates routing made explicit | **no** |

**Patches:** 15 total, **0 currently failing to apply**, 8 triaged, 3 found obsolete. `apply-patches.sh` fails the build on a failed patch, so a green build means every patch applied.

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

### Task list (1 of 14 done)

| | Task | Status | Notes |
|---|---|---|---|
| `F1` | Recover the three missing pieces so customizations compiles standalone | done | CraftContext members, 8 ResourceInfo wood enums, OutridersGuildmaster. Build verification still outstanding. |
| `F2` | Make apply-patches.sh fail on a failed patch | **in progress** | Also: preserve subdirectories under customizations (see Q-002). 7 patches currently fail while the build reports success. |
| `F3` | Triage the seven failing patches | todo | Still needed, or obsolete because ModernUO changed? Fix or remove with a reason. |
| `F4` | Delete stale server/customizations/migrations/ | todo | 3 PetMimic JSONs diverging from the canonical v0-v8 set. |
| `F5` | Make RegenRates routing explicit | todo | Works by accident today: both land in Misc/ so ours overwrites. |
| `P1` | Validate the port recipe with one real port | todo | notes/port-recipe.md was drafted from source study, not a build. Confirm the two fidelity traps. |
| `P2` | Second port, timed, using only the recipe | todo | That number prices every content task below. |
| `C1` | Eodon core content | todo | ~22 files, ~4,000 lines. 6 dinosaurs, Raptor, 8 Aloron pieces, the quest line. Corrected down from 52. |
| `C2` | Revamped Dungeons | **blocked** | 255 files. BLOCKED on Q-002: 32 duplicate basenames across 137 files would overwrite when flattened. One chat per dungeon: Despise 4, Shame 11, Wrong 26, Covetous 29, Exodus 38, Blackthorn 147. |
| `C3` | High Seas, cheap half | todo | ~78 files. Fishing, rare fish, sea creatures, food. Skip anything touching BaseGalleon or cannons. |
| `C4` | Creatures and NPCs | todo | ~360 files, 0% dependency. Batches of ~20. |
| `C5` | Decoration, housing, crafting | todo | Addons, Decorative, New Magincia, Items/Resource, BulkOrders. 0% dependency. |
| `C6` | Artifacts and equipment | todo | ~473 files, 1-2%. Selectively: pieces anchoring a dungeon or quest. |
| `C7` | High Seas naval - written proposal only | todo | ~54 files. Means extending BaseBoat. Do not start; Chase decides from the proposal. |

_Detail and acceptance criteria in `docs/tasks.md`. Status lives in `tools/progress-state.json`._

**Deliberately declined:**

- **Eodon / Time of Legends** — gated on Myrmidex Invasion (83% dep) and Shadowguard (71%), both subsystem builds. Deferred, not declined: measure how much of the Valley separates first.
- **Vice vs Virtue, City Loyalty, Skill Masteries, Exploring the Deep** — 29-100% dependent on subsystems ModernUO lacks entirely. Deferred to workstream 4.

Counted from the trees: 114 customization files, 14 patch files, stale migrations subfolder still present.
Shard status: running on ModernUO.
<!-- PROGRESS:END -->

## Expansion coverage

<!-- EXPANSION:START -->
### Content by expansion

**3,039 of 6,144 ServUO files present** (49%), of which **0 ported by us**.

```
Pre-AoS (T2A/UOR/LBR)     ##########..........  2223/4294    52%
Age of Shadows            #############.......   201/309     65%
Samurai Empire            ###############.....    87/115     76%
Mondain's Legacy          ##########..........   241/471     51%
Stygian Abyss (Ter Mur)   ######..............   125/444     28%
High Seas                 ######..............    96/334     29%
Time of Legends (Eodon)   #######.............    53/157     34%
Endless Journey           #############.......    13/20      65%
TOTAL                     ##########..........  3039/6144    49%   +0
```

_Filename-stem matching: a proxy for presence, not behaviour. Unclassified files fall into Pre-AoS, inflating it. Directional, not a completion percentage._
<!-- EXPANSION:END -->
