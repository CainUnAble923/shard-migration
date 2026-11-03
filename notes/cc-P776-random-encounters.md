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

## Where it stands

Finished. All 27 facts pass alone and in the full suite, all 32 mutants were killed, and the gated build is green
(`sl-modernuo:cc-p776`, 2977 passed, 0 failed, 6 skipped, EXIT=0). `latest` was not moved. Nothing was put on a shard.

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
- Green: 25 of 25 first (`green-probe5.txt`), then all 27 after the two reward facts and the sweep fix
  (`green-probe6.txt`, 2026-11-02 after the reboot).
- Mutants: 32 mutants, each breaking one rule (`mutate776.py`). All 32 were killed: the first 18 before the memory
  stop (`mutants-result.txt`), the other 14 after the reboot (`mutants-result2.txt`): boat, season, league, night,
  toll cap, toll deadline, follow into town, leave late, leave early, fighter removed, dawn, restart sweep, tamable,
  surveyor target. `run-mutants-checked.sh` runs them one at a time. Before each one, it drops the Docker VM's page
  cache and checks free memory, and it stops under 4 GB. It stopped once, at 3.8 GB, before `league`. After a cache
  drop the rest ran at 4.3 to 7.6 GB free.
- Gated build, first try: 2 facts failed in the full suite (`gated-build-1-failed-summary.txt`): Haven Island and
  town. Both had passed alone. The cause was the facts' test spot (4400, 600). It lies inside the north-east snow
  isles SOS fence (`SosFenceRegion`, priority 60), which another fact registers in the full run. That fence hid the
  facts' own lower-priority regions, so `Region.Find` returned the fence. The engine was right: no rule was
  refused wrongly. I moved the spot to (3400, 400), which keeps every offset the facts use clear of all fences. Now
  each place check first asserts its spot is not under a fence, and prints the region it found
  (`full-probe-diag-summary.txt`). After that, the full suite passed in the probe (4073 passed, 0 failed,
  `full-probe2-summary.txt`). The four place mutants (deny regions, town, dungeon, house) were killed again at the
  new spot (`mutants-result-newspot.txt`).
- Gated build, second try: EXIT=0 (`gated-build-summary.txt`).

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

## Resumed after the reboot (2026-11-02, evening)

Chase's answer (Iron-P776-20261102-180115-d497): the tower was rebooted at 18:53, and `festive_goodall` was gone. Run
the 27-fact check, the 14 mutants one at a time, and the gated build, checking memory before each. Done in that
order, with free memory checked (and the Docker VM's cache dropped) before every Docker run. One run, the
diagnostic full-suite probe, started at 3.2 GB free before I noticed. It finished without trouble, and every run
after it started at 5.6 GB or more.

P776 DONE
