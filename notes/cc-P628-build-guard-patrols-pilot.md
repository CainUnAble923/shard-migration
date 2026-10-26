# P628: guards that patrol and see, stage 1 (inventory and the witness contract, Cove pilot)

Written 2026-10-25 by the Iron Golem (Claude Code). Builds stage 1 of [cc-P608-guards-patrol-design.md](cc-P608-guards-patrol-design.md), Chase's option C (10-25 evening: physical patrols and line of sight in one test town first; New Haven qualified separately later; Persuasion never erases a crime). The design's nine-prompt sequence starts with: "1. Inventory town jurisdictions, call sites, legacy guard spawners, law dependencies, and source hooks. Build the incident/witness contract and failing-first sight/report tests." This is that prompt. I made it observable on the test shard in the pilot town, and it changes no guard behavior. The other eight prompts are drafted at the end of this note.

## In plain words

- Nothing changes for players: guards still answer exactly as they do today.
- On the test shard, staff can switch on a "witness" recorder for one pilot town, Cove on Trammel (`[GuardWitness on`). From then on, each crime there is noted with who could actually have seen it: in range, in line of sight past walls, and not hidden. Each "guards!" call is noted with which guards were close enough to hear it. `[GuardWitness log` shows the list.
- This is the groundwork the walking, seeing guards (the next stages) will act on: they will respond only to what a guard saw or a witness reported, never to a crime nobody saw.
- For Chase: nothing to decide or deploy. To see it, on the test shard in Cove: `[GuardWitness on`, commit a crime with a second character watching (and one behind a wall), call "guards", then `[GuardWitness log`.

## Part 1a: the inventory

All from source, not from a live world; paths as in the design (`U/` pinned UOContent, `S/` pinned Server, `C/` our customizations).

### Town jurisdictions (pinned `Distribution/Data/regions.json`)

| Facet | TownRegion | Plain GuardedRegion |
|---|---|---|
| Trammel | 49 | 2 (Moongates, New Haven Moongate) |
| Felucca | 49 | 2 |
| Ilshenar | 11 | 0 |
| Malas | 4 | 0 |
| Tokuno | 2 | 1 |
| TerMur | 1 | 1 |

Trammel's named towns include The Heartwood, Cove, Britain, Jhelom, Minoc, New Haven (and its separate moongate region), Haven, Trinsic, Vesper, Yew, Wind, Serpent's Hold, Skara Brae, Nujel'm, Moonglow, The Scholar's Inn, Magincia, Buccaneer's Den, Delucia and Papua. Several farm and field entries are TownRegions too ("A Wheatfield in Britain 1" and so on), and many entries have no name. A manifest has to choose its regions deliberately; it cannot simply take "every TownRegion". Counts are of top-level entries in that file. I did not check whether the shard's own region data overrides any of them (`C/Regions/` holds the Apprentice training and Old Haven regions, not town overrides). That is unverified.

### The pilot town

**Cove, Trammel**: two areas, (2200,1110)-(2250,1160) and (2200,1160)-(2286,1246), Z 0-128, priority 50. It is the design's example of a small settlement (2 post guards, 2 patrol guards). It is away from New Haven and Old Haven, which the design keeps for its own later qualification. The manifest is `ClusterFGuardWitness.Jurisdictions`: id `cove-trammel`, Trammel, region name "Cove". It has no Felucca twin, because separate facets never share guards.

### Every stock path that brings guards today

| Path | Source | What it does | Witness contract |
|---|---|---|---|
| Speech keyword *guards* | `U/Regions/GuardedRegion.cs` OnSpeech | `CallGuards` at the speaker's spot, no hearing check | observed (report) |
| Criminal aggression | GuardedRegion OnAggressed, reached from `S/Mobiles/Mobile.cs` AggressiveAction (`:3930`) | makes the aggressor a candidate | observed (incident) |
| Criminal action | GuardedRegion OnCriminalAction, from `Mobile.CriminalAction` (Criminal is set first) | candidate | observed (incident) |
| Helping a criminal | GuardedRegion OnGotBeneficialAction | candidate | observed (incident) |
| A red entering town | GuardedRegion OnEnter (when `AllowReds` is false; default `Core.AOS`) | permanent candidate | not a crime event; stage 3 |
| The fake call | GuardedRegion CheckGuardCandidate | the nearest town human within 8 tiles shouts and spawns a guard, with no sight check | replaced in stage 3 |
| CallGuards | GuardedRegion | every candidate within 14 tiles, no witness, hidden or line-of-sight check; dictionary members even outside the region | replaced in stage 3 |
| Human NPC and a murderer | `U/Mobiles/BaseCreature.cs:3097-3118` | a town human calls on an approaching murderer, distance only | replaced in stage 3 |
| Guard creation and movement | `U/Mobiles/Guards/BaseGuard.cs` Spawn, MakeGuard, TeleportTo; WarriorGuard and ArcherGuard attack and death reinforcements | idle reuse within 15, else construct at the target; instant kill (`guards.instantKill`, default true); teleports for distance or lost sight | the stage 2 guard replaces this in pilot towns |

### Legacy guard spawners

Pinned's spawn data (`Distribution/Data/Spawns/`) has no WarriorGuard or ArcherGuard entry (searched by type name). Stock guards come only from the call paths above. In our customizations, `BaseGuard` appears only in `ClusterFJokeAchievements.cs` (the hidden guard-death achievement). `ClusterFNotedBySystem.cs` checks guarded regions, not guards. Hand-placed guards or staff spawners in the live world were not inspected (unverified): stage 4's seeder must inventory them before any town changes mode, as the design says.

### Law dependencies the stages must keep

Notoriety and Trammel's harmful rules (`U/Misc/Notoriety.cs`); `Mobile.CriminalAction` and the criminal timer; aggressor records (`AggressorInfo`, murder reporting); Stealing's own caught and criminal rules (`U/Skills/Stealing.cs`); Hiding's combat restriction and Detect Hidden; Young protection (`C/ClusterFYoungPlayer.cs` and its patches); town spell and vendor rules (GuardedRegion); murder bounties (`murderSystem.bountiesEnabled`, live setting unverified); the hidden achievements that read guard kills and guarded regions.

## Part 1b: the witness contract (ShatteredLegacy, branch golem/Iron/P628)

| File | Change |
|---|---|
| `server/customizations/ClusterFGuardWitness.cs` (new) | Incidents, witnesses, sight, reports and hearing, the pilot manifest, `[GuardWitness`. |
| `server/patches/GuardedRegion-witness-observe.patch` (new) | Four one-line calls in pinned `Regions/GuardedRegion.cs`, one per stock crime or call path above, each before the stock response, which runs unchanged. |
| `docker/uo/apply-patches.sh` | Registers it, with the alternatives argued. EventSink has an aggression event but none for a criminal action or region speech, and replacing GuardedRegion wholesale would hide upstream drift. |
| `server/tests/Regions/GuardWitnessVerification.cs` (new) | 4 facts, below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.25.14, one Staff line (players see nothing). |

The contract, as built from the design's "Seeing a crime and hearing a call":

- **Sight** (`Sees`): the observer is alive, has player access (staff sight is never a guard's), is on the same map, within 14 tiles, can `CanSee` the actor (a hidden actor is unseen), and has line of sight to the actor and to the action's place where that differs. Walls block it, through pinned's `Map.LineOfSight`. There is no facing cone.
- **An incident** is recorded synchronously in the crime's own callback, before anything can move, hide or delete the actor. It holds: id, kind (aggression, criminal action, criminal assist), town, place, time, culprit, victim, and each qualified witness. A witness is a guard, a townsperson (`BaseCreature.IsHumanInTown`, uncontrolled) or a player, each with the culprit's place as last seen. A hidden onlooker who saw it is a witness, as the design allows. The same culprit's crimes within one second in one town are one incident, because one attack raises both the aggression and the criminal callbacks. The incident is upgraded to an aggression with its victim. At most 64 per town are kept.
- **A report**: a living player's *guards* in a pilot town reports the most recent incident they themselves witnessed in the last 15 seconds. A caller who saw nothing raises an investigation at their spot, with no suspect. One caller is limited to one report every 2 seconds. It is heard by the guards within 15 tiles (spoken), 18 (yelled) or 1 (whispered) in the same town. Hearing needs no line of sight, and it passes on the incident and its last seen place, never a live position.
- **Observe only, off by default.** `[GuardWitness on|off|status|log` (Administrator, DevTool, test shard only). The switch is not saved; a restart turns it off. Off, or outside a pilot town, nothing is recorded. Players get no message from it: with stock guards still answering, a "No guard answers nearby" would be false. That line belongs to stage 3, when the pilot's guards answer only through this contract.

## Tests: red first, then green

How I ran them: builder image `sl-uo-builder:cc-P627` (a recent build; GuardedRegion is stock in it), with `ClusterFGuardWitness.cs`, the fact file and the patched `GuardedRegion.cs` bind-mounted, `dotnet test` filtered to `GuardWitnessVerification`. The facts use two test towns of their own on Trammel, registered as TownRegions, with the pilot manifest pointed at one of them. Walls are a real stone-wall row (`TestTileRows.StoneWall`, NoShoot) so pinned's line of sight blocks. Scripts, the stub, the mutants and logs are in the session scratchpad.

| Fact | What it pins |
|---|---|
| `SightNeedsRangeLineOfSightAndAVisibleActor` | Seen at 10 and at 14 tiles, not at 15. Not seen by a dead observer or by a GM. Not seen through a stone wall (and `InLOS` is false there). An actor in sight whose action's place is behind the wall does not count. A hidden actor is unseen at one tile. |
| `ACrimeIsRecordedAtTheEventWithExactlyItsWitnesses` | Through `Mobile.CriminalAction` in the pilot town: one incident with exactly the player 5 tiles off, a hidden onlooker, a provisioner (townsperson) and a guard. It excludes the player 16 tiles off and the one behind the wall, and has the right roles and place. Hiding and running afterwards change nothing recorded. The culprit's attack a moment later (through `Mobile.AggressiveAction`) is the same incident, now an aggression with its victim. A crime in an ordinary guarded town, or with the service off, records nothing. |
| `ACallReportsOnlyWhatTheCallerSawAndIsHeardInSpeechRange` | Through real speech (`DoSpeech` with the *guards* keyword):<br>- The witness reports their incident. It is heard by a guard 10 tiles off and by one 14 tiles off, out of the culprit's view, but not by one 17 off. The stock response still runs: an idle guard took the culprit as its focus.<br>- A second call within 2 seconds is ignored; a yell then reaches the 17-tile guard; a whisper reaches nobody.<br>- A caller behind the wall who did not see it raises an investigation with no suspect. After 15 seconds even the witness's call is an investigation. A dead caller reports nothing. |
| `AJurisdictionIsNamedRegionsOnOneFacet` | The shipped manifest is Cove on Trammel. A child region of Cove counts; Cove on Felucca and Britain do not. |

**Red on the old code:** a stub `ClusterFGuardWitness` with the same public names and no behavior, and pinned's GuardedRegion without the patch: 4 of 4 failed.

**Green:** 4 of 4.

**Mutations of the finished code**, each run alone:

| Mutant | Red facts |
|---|---|
| m0: the real service but pinned's GuardedRegion without the observe calls | the crime fact and the call fact (the real entry points are what reach it) |
| m1: no line-of-sight check | the sight, crime and call facts |
| m2: staff sight counts | the sight fact |
| m3: no 15-second report window | the call fact |
| m4: a yell carries only 15 | the call fact |
| m5: anyone nearby is a witness, seen or not | the crime and call facts |
| m6: only the exact region counts, not its children | the jurisdiction fact |

What the first runs found:
- My first crime fact expected a hidden player standing by to be no witness. That was my mistake, not the service's: the design lets a hidden onlooker witness and report what they saw. Only a hidden actor goes unseen. The fact now counts the onlooker.
- Pinned's `GetMobilesInRange` returns a ref struct, so the facts collect guards with a loop rather than LINQ.

**Gated build:** I took the `docker-build` lock and dropped the Docker VM's page cache first (7.4 GB available at launch). I ran `docker\uo\build.sh -t sl-modernuo:cc-P628` detached with its log on disk and released the lock afterwards.
- It finished with EXIT=0: "Built sl-modernuo:cc-P628 with patches applied and 2522 shard test(s) passing". Of 2,526 tests, 2,522 passed and 4 were skipped (the real-map-data facts); none failed.
- `GuardedRegion-witness-observe.patch` applied, all 4 witness facts passed in it, and every existing fact on guards, regions, achievements and Young protection passed alongside.
- The images are `sl-modernuo:cc-P628` = `5f44105920ad` and `sl-uo-builder:cc-P628` = `b28090b4d28d`. The log is `build-P628.log` in the session scratchpad.

## Deviations and decisions for Chase

- **Observe-only first stage.** The design's prompt 1 builds the contract and its tests; it does not change guards. To make it playable on the test shard without changing anyone's game, the stock crime and call paths in guarded regions call the service, which only records (pilot town, switched on). Stage 3 is where the pilot town's guards start answering only through it.
- **Pilot town: Cove, Trammel.** The design names Cove as a small-settlement candidate and asks for one test town before New Haven. If Chase prefers another, it is one line in the manifest.
- **Not done here (later stages, drafted below):** the physical guard, its movement and combat, dispatch, posts and routes, beginner safety, New Haven, the Persuasion checkpoint, budgets, and the other towns. Theft gets no special handling yet: a caught theft reaches the contract through Stealing's own `CriminalAction`, as the design asks (no new law).

## Unverified

- Line of sight across floors (a witness upstairs). The test host has no map or static data, so the facts block sight with an item wall. Floors and buildings in real Cove are a stage 4 route-survey check.
- The live world's guard population and any hand-placed guard spawners (stage 4's inventory).
- Performance: each crime in a pilot town does one range query of 14 tiles; each call one of at most 18. Measuring under load is stage 8.

## Checks before handing over

`git diff --check` is clean in ShatteredLegacy, and the new files (the customization, the patch, the facts, this note) are plain ASCII with no trailing whitespace (a patch's blank context line is a single space, as in every existing patch). Nothing was committed or deployed, Haven was not touched, no world or test shard was started, and the witness service is off in the build. The Read tool worked; no step was skipped.

## Remaining stages, as prompt drafts for the overseer to number

The design's sequence, 2 to 9, carried forward with what stage 1 now provides. `P<nn>` is for the overseer to fill in. The design reserves two more prompts for route or performance spillover.

---

### Draft: guard patrols stage 2: the physical guard

```
# CC task P<nn>: guard patrols stage 2: a physical guard that walks, sees, fights, searches and walks home

**Model:** Opus

**Touches:** server

**Summary:** Stage 2 of `notes\cc-P608-guards-patrol-design.md` (option C, Chase 10-25), after P628's witness contract (`notes\cc-P628-build-guard-patrols-pilot.md`). A new BaseCreature-based patrol guard with explicit states, no teleport, no instant kill, no reinforcements from nowhere.

## The work

1. Read the design's "Physical response, combat, and losing the trail" section, P628's notes and pinned `U/Mobiles/Guards/` (what not to inherit). Build `PatrolGuard : BaseCreature` with states Post/Patrol, Respond, Fight, Search, Return, Unavailable; its own controlled acquisition (no ordinary FightMode auto-targeting). Movement through the existing point/path primitives: about 0.4 s per tile on patrol, 0.2 s responding, no catch-up bursts.
2. Pursue a mobile only while `ClusterFGuardWitness.Sees` holds; on lost sight or Hidden, drop the live target and keep the last seen point with Z. Search up to 10 s there, at most two contested Detect Hidden attempts within 3 tiles, 5 s apart, each bounded by range and LOS. Attacks recheck visible target, legal harmful permission, range and LOS.
3. Ordinary combat at the design's starting strength (1,200-1,600 hits, 65-70% resists, 120 combat skills, 25-35 base damage). No instant kill, no avenge spawns, no loot, fame, karma or skill practice from killing one. Exclude it from taming, calming and luring. Give `ClusterFJokeAchievements`' guard-death credit and `IsGuard` an adapter so the new type counts where BaseGuard did.
4. Return to its post on foot; if blocked, retry within budget, then mark Unavailable. Never teleport or snap home.
5. Red-then-green tests: no relocation on any state change, lost LOS clears the target, hidden after a report means search not attack, blocked return goes Unavailable, death makes no reinforcement. Seen failing first.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. Nothing placed in any town yet. CHANGELOG Staff line.
7. Notes `notes\cc-P<nn>-guard-patrols-stage-2.md`. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 3: dispatch in the pilot town

```
# CC task P<nn>: guard patrols stage 3: local dispatch, relays and pursuit limits, and every guard path in the pilot town through one policy

**Model:** Opus

**Touches:** server

**Summary:** Stage 3 of `notes\cc-P608-guards-patrol-design.md`. In an enabled pilot jurisdiction, every crime and guard call goes through P628's witness contract to stage 2's guards; stock guards no longer appear there. Other towns stay stock.

## The work

1. Read the design's "Seeing a crime and hearing a call" and pursuit sections and the notes of P628 and stage 2. A per-town mode switch (saved), default off. In an enabled town, the GuardedRegion paths P628 observes (speech, aggression, criminal action and assist) plus OnEnter for reds, the fake call, CallGuards and BaseCreature's murderer call (`U/Mobiles/BaseCreature.cs:3097-3118`) route to the policy atomically, and BaseGuard.Spawn/MakeGuard never run there.
2. Dispatch: a guard who saw it responds at once; a heard report assigns an available guard with a plausible local route; dedupe by incident; never construct a guard as fallback. Relay to at most two guards within 18 tiles, two hops, 5 s lifetime. Reports expire after 15 s unassigned; an assignment lasts at most 60 s. "No guard answers nearby." when nobody heard.
3. Pursuit apron: an already visible pursuit may continue up to 20 tiles outside the jurisdiction for 10 s; never across maps, dungeons, private interiors or travel gates.
4. Red-then-green tests from the real entry points: no stock guard is created in an enabled town on any path; a heard report moves the right guard; duplicate speech dispatches once; the apron limit; a disabled town is exactly stock. Seen failing first.
5. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG Staff line (the pilot stays off on the live shard).
6. Notes `notes\cc-P<nn>-guard-patrols-stage-3.md`. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 4: posts, routes and the Cove itinerary

```
# CC task P<nn>: guard patrols stage 4: manifest reconciliation, post slots, waypoint authoring and the Cove itinerary

**Model:** Opus

**Touches:** server, map

**Summary:** Stage 4 of `notes\cc-P608-guards-patrol-design.md`: the seeder that places and owns guard slots, staff waypoint tools, route validation, and a complete reviewed itinerary for Cove (2 posts, 2 patrols).

## The work

1. Read the design's "Posts, staffing, and route authoring" section and the notes of P628 and stages 2 and 3. A versioned manifest per town/facet (stable ids, regions, posts, slots, routes, waypoints with Z, waits, apron). A seeder with status/dryrun, create-missing and repair modes, stable owned slots, reconciliation on rerun (never counting nearby mobiles), replacement at the post after 60 s (at most one per town per 10 s).
2. Inventory first: list every guard and guard spawner in and around Cove on the test shard world (under the test-shard lock) and report conflicts; never delete guards by rectangle.
3. Waypoint authoring for staff and export to the manifest; validation of map, Z, membership, reachable ground and every link both ways; reject houses, locked doors, dungeon entrances and gates.
4. Walk Cove (scratch shard, test-shard lock, never Haven): choose post tiles at the main entrance and the bank/square, one 45-90 s loop with two staggered patrols; record the itinerary and frames.
5. Red-then-green tests: rerun idempotence, a deleted waypoint, a reboot mid-pursuit returning home on foot, replacement limits.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG Staff line.
7. Notes `notes\cc-P<nn>-guard-patrols-stage-4.md` with the Cove itinerary. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 5: beginner safety (prerequisite for New Haven)

```
# CC task P<nn>: guard patrols stage 5: beginner safety that holds without guards, and P447's open risks

**Model:** Opus

**Touches:** server

**Summary:** Stage 5 of `notes\cc-P608-guards-patrol-design.md`: explicit prevention of player-origin harm to Young players in New Haven's protected service hubs, independent of any guard. A hard prerequisite for converting New Haven.

## The work

1. Read the design's "New Haven, Young players, and Old Haven" section, `notes\cc-P447-review-cont-old-haven-new-player-safe.md`, and P189's notes. Define the protected hubs (bank, healer, trainer hubs, town entrances, moongate).
2. Reject player-origin harm to a Young player in a hub at its source: direct attacks, pets, summons, guild exceptions, fields, traps, delayed damage and attacks crossing the boundary. Validate attribution on direct-damage paths rather than assuming CanBeHarmful covers them.
3. Resolve or record a decision for each P447 risk (the P189 retirement bounds, direct traps, guild exceptions). Keep Old Haven training and Rootdeep rules unchanged.
4. Red-then-green tests: a fresh Young player and one near expiry, guild, pet and summon attackers, traps and fields from outside a hub, all guards dead. Seen failing first.
5. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG player lines (this protects players on its own).
6. Notes `notes\cc-P<nn>-guard-patrols-stage-5.md`. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 6: qualify New Haven

```
# CC task P<nn>: guard patrols stage 6: New Haven posts, moongate, service routes and measured arrival times

**Model:** Opus

**Touches:** server, map

**Summary:** Stage 6 of `notes\cc-P608-guards-patrol-design.md`: New Haven's own manifest (8 post guards in pairs, 4 patrol guards on two service loops), its separate moongate region, public guidance, and measured arrival: 95th percentile within 3 s on hub tiles, 8 s on covered streets.

## The work

1. Read the design's New Haven sections and the notes of stages 4 and 5 (stage 5 must be done).
2. Survey doors and floors; post pairs at bank/square, healer/trainer hub, eastern exit and moongate; two short service loops; keep patrols out of Old Haven's grounds and Rootdeep; preserve trainer NPC floors and P189 quest targets.
3. Measure arrival times on a scratch shard (test-shard lock) and fix layout until the targets hold; leave New Haven in stock mode if a hub fails.
4. Public guidance: where posts are, "Guards respond to what they see and to nearby witnesses. The ruins are a training area outside town."
5. Tests for the manifest and guidance; the measurements in the notes. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG lines. Ask Chase (Ask-Chase.ps1) before switching New Haven's mode on anywhere but the test shard.
6. Notes `notes\cc-P<nn>-guard-patrols-stage-6.md`. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 7: the Persuasion checkpoint and Den hooks

```
# CC task P<nn>: guard patrols stage 7: the routine checkpoint challenge with Persuasion, and the Den's patrol jobs

**Model:** Opus

**Touches:** server

**Summary:** Stage 7 of `notes\cc-P608-guards-patrol-design.md`: the shared P606 routine-challenge adapter. Persuasion never erases a crime (Chase 10-25).

## The work

1. Read the design's "Persuasion, stealth, the Den, and bounties" section, `notes\cc-P606-begging-skill-design.md` (its guard contract) and P626's Persuasion notes (`ClusterFPersuasion.Practice`).
2. Authored routine checkpoints with stable ids: at 80 Base, an eligible innocent traveler may answer, visible within 3 tiles and LOS, two interruptible seconds; success acknowledges passage at that checkpoint for five minutes. One attempt per account/checkpoint/opportunity; one practice event at terminal resolution with a 30-minute checkpoint/account training limit.
3. Refusals: criminal or murderer, witnessed incident, pursuit, combat, recent theft, quest/faction gates. Recheck when speaking ends. No change to Criminal or murder counts, ever.
4. Den hooks: jobs about observing patrol timings or scouting an unwatched route, using the same witness rules; no exemption, no automatic suspicion.
5. Red-then-green tests including every refusal and no double practice after a guard is replaced or the server restarts.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG lines.
7. Notes `notes\cc-P<nn>-guard-patrols-stage-7.md`. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 8: budgets and stress

```
# CC task P<nn>: guard patrols stage 8: path and queue budgets, stress, and strength tuning

**Model:** Opus

**Touches:** server

**Summary:** Stage 8 of `notes\cc-P608-guards-patrol-design.md`: enforce the design's caps and measure the system under load.

## The work

1. Read the design's "Performance and failure limits" section. Caps: 3 guards per incident, 8 responding per town, 32 across towns, 64 queued incidents per town, 128 overall; one report per caller per 2 s; a reserved severe-harm queue. Path plans: 2 per town per second, 20 globally, 2 ms per dispatcher slice, including PathFollower's blocked-step repaths. Stop a blocked segment after 3 failures or 5 s.
2. Diagnostics: incident-to-assignment and arrival times, witness source, lost-trail reasons, queue drops, path plans and failures, unavailable slots; bounded, with player data redacted.
3. Stress on a scratch shard (test-shard lock): an idle town, a crowded bank, simultaneous crimes, call spam, hidden suspects behind walls, blocked routes, a group with high-end shard gear and pets. Tune strength and staffing from the measurements.
4. Tests for each cap and the blocked-segment stop. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG Staff line.
5. Notes `notes\cc-P<nn>-guard-patrols-stage-8.md` with the measurements. Last line `P<nn> DONE`.
```

---

### Draft: guard patrols stage 9: the remaining towns

```
# CC task P<nn>: guard patrols stage 9: the remaining guarded towns, conversion order and rollback

**Model:** Opus

**Touches:** server, map

**Summary:** Stage 9 of `notes\cc-P608-guards-patrol-design.md`: author and qualify the other guarded town/facet manifests in reviewed batches, and run integrated acceptance.

## The work

1. Read the design's staffing table and the notes of stages 4, 6 and 8. Choose a batch from P628's jurisdiction inventory (Trammel first; Felucca separately; field and unnamed TownRegions decided explicitly). Survey each town before classifying it.
2. Manifests, seeding and route validation per stage 4; arrival measurement per stage 6; conversion order and a rollback per town (its mode switch back to stock).
3. Integrated acceptance on a scratch shard. If the batch exceeds a safe size, stop and write the next batch as a new prompt rather than skipping a survey.
4. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. CHANGELOG player lines when towns are announced. Ask Chase before any town's mode goes on outside the test shard.
5. Notes `notes\cc-P<nn>-guard-patrols-stage-9.md`. Last line `P<nn> DONE`.
```

P628 DONE
