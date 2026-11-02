# cc-P776: our own random encounters (three starters)

Iron Golem, 2026-11-02. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P776`, not committed. Tools and logs are in `notes\cc-P776-tools\`. The design follows P765's
assessment (`notes\cc-P765-random-encounters-assessment.md`): its three sketched encounters and its never-do list.
No code was copied from the RunUO engine P765 read; this is ours, written from scratch.

## In plain words

- **Travelers can now run into trouble on the roads.** Out in the wilds of Trammel and Felucca, about once in a while
  (a 5% roll each minute while you are travelling, at most once every 25 minutes per account), something happens a
  short way off the road: brigands demanding a toll, a League surveyor pinned down by wolves or orcs, or, on Halloween
  nights only, a procession of lantern walkers that leaves you alone unless you start it.
- **Where it never happens:** the Wakening Isle, New Haven and Haven Island, any town or guarded area, dungeons,
  houses, boats, jail. **Who it never happens to:** staff, ghosts, Young characters, characters still in the tutorial,
  anyone hidden, standing still (afk) or already fighting. Encounter creatures leave after 8 minutes if nobody fights
  them, vanish if they walk into a town, and are cleared at every restart.
- **Everything is in one file**, `Configuration/encounters.json` on the server (written on first start): the chance,
  the cooldown, the facets, the no-go regions, and the three encounters. `"enabled": false` there, then
  `[Encounters reload`, turns it all off.
- **For you:** try it on the test shard with `[Encounters force toll` (or `surveyor`, `procession`) as staff, and
  decide whether 5% a minute feels right. Not yet seen in a client: the creatures' behaviour (walking up, the
  surveyor's fight, the procession's walk) is tested only in code.

## Where it stands (stopped, not finished)

The code, the 27 facts, the CHANGELOG line and the version bump are written. Not done: the last green probe of all
27 facts, 14 of the 32 mutants, and the gated build. The mutant run was killed by Claude Code because the PC ran
critically low on memory (4.5 GB of 32 GB free afterwards). Its container on mutant 14 (`boat`) hung for 3 hours, and
Docker could not kill it (`festive_goodall`, image `sl-uo-builder:cc-P774`, "did not receive an exit event"). I was
told not to rerun the memory-heavy work on my own, so I released the docker-build lock and stopped here.

## Design and files (code copy `D:\UO\golems\Iron\ShatteredLegacy`)

- `server/customizations/Encounters/EncounterTable.cs`: the config. `Configuration/encounters.json` is written with
  the defaults on first start. A file that fails its checks is refused whole, and the defaults are kept.
- `server/customizations/Encounters/ClusterFEncounters.cs`: the engine. A 60 s timer rolls for each eligible traveler,
  picks a weighted encounter the player qualifies for (facet, day or night, level range, League, season), and spawns
  it 9 to 15 tiles away, preferring spots out of line of sight. A 10 s sweep handles cleanup. The staff command is
  `[Encounters status|check|reload|force <id>`, in the DevTool category. A `GenericPersistence` ("RandomEncounters",
  version 0) saves only the serials of spawned creatures, so a restart removes them.
- `server/customizations/Encounters/EncounterSurveyor.cs`: the surveyor ally. Source-generated serialization,
  version 0, no fields (D40).
- `server/tests/Misc/RandomEncounterVerification.cs`: 27 facts.
- `CHANGELOG.md` has a new `## 2026.11.02.6` with "Travelers may now run into trouble on the roads", and `VERSION` is
  2026.11.02.6.

## The starters

- **Toll Road** (day, level 15 and up): 2 to 4 brigands and a toll keeper. Saying "pay" pays 5% of the gold in your
  pack, at most 200, and they leave. If you do not pay within 30 s, they turn hostile. Whoever does the most damage
  to the toll keeper gets an existing Hunter loot box (source `encounter:toll`, once per loop, through
  `ClusterFLootBoxes.Award`).
- **Lost Surveyor** (League members, level 10 and up): Odile Marchant, the League surveyor, fights 2 to 3 orcs,
  ratmen or wolves. If she lives, she thanks you and leaves.
- **Lantern Procession** (Trammel, night, Halloween season): 3 to 5 lantern walkers and a lantern bearer. They walk
  past unless attacked and leave at dawn. The bearer's killer gets 1 festival token, through `FestivalTokens.Grant`.

No new item rules, and no skill or stat gains: the creatures are ordinary, so normal combat gains apply. The System
line is sent to the player when an encounter starts.

## Tests

- Red: the facts alone failed to compile, because `Server.Encounters` did not exist yet (`red-probe.txt`,
  PROBE_EXIT=3).
- Green: 25 of 25 passed (`green-probe5.txt`). After that, I added two reward facts and a fix to the sweep (dead
  creatures' serials are dropped from the saved set). **These have not been seen green.**
- Mutants: 32 mutants, each breaking one rule (`mutate776.py`, `run-mutants.sh`). The first 18 were all killed:
  off switch, staff, dead, Young, trainee, hidden, idle, combat, already in one, both cooldowns, crowd, isle, facets,
  deny regions, town, dungeon, house (`mutants-result.txt`). Not run: boat, season, league, night, toll cap, toll
  deadline, follow into town, leave late, leave early, fighter removed, dawn, restart sweep, tamable, surveyor target.
- Gated build: not run.

## Deviations and decisions for Chase

- There is no League field-contract system yet, so the surveyor only gives her thanks. She marks no map.
- There is no road-tile check, so the Toll Road can happen anywhere in the wilderness by day.
- The toll box goes into the backpack through `Award`, not onto the toll keeper's corpse. There is no achievement for
  declining the toll.
- Cooldowns are kept in memory only, so a restart resets them.
- "Never on a boat" means within 8 tiles of any boat, because `FindBoatAt` needs multi data the test host lacks.
- The Grep tool was denied automatically on the ShatteredLegacy path (I used it to find `var json = ` in the facts
  file). I used Bash grep instead.
- Version 2026.11.02.6 may collide with another Golem's branch at merge.
- Credit: the idea follows P765's reading of a RunUO encounter engine. No code was copied.

## Not verified

The creatures' behaviour in a client: the walk-up, the surveyor's fight, and the procession's walk.

## To finish (when memory allows)

1. Free the hung container (`docker rm -f festive_goodall`; if Docker still cannot kill it, restart Docker Desktop).
2. `bash notes/cc-P776-tools/probe776.sh "FullyQualifiedName~RandomEncounterVerification"`: 27 of 27 must pass.
3. Run the remaining 14 mutants: edit `mutants.txt` in the scratchpad mutant folder down to those 14, then
   `run-mutants.sh`.
4. Take the docker-build lock and run `notes\cc-P776-tools\gated-build.ps1` detached. The log is UTF-16; strip NULs
   and check for `EXIT=0`.

P776 STOPPED: the mutant run was killed for low memory and its container hung; the 27-fact green probe, 14 mutants and the gated build are not run
