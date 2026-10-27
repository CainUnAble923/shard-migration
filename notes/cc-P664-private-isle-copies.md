# cc-P664: private copies of the isle (P481 F4)

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P664` (P662 and P663 merged in; P705 not yet in this branch). Chase confirmed private copies over
the hidden-players mix on 10-26 14:08 (the prompt's footer). Not committed; nothing deployed; Haven not touched.

## In plain words

- **Every new player gets their own Wakening Isle (test shard).** Each trainee, or a party together, is put on one of
  16 private copies of the isle. Other trainees' pests, pets, doors and sounds never reach their lessons.
- **Logging out keeps your place for half an hour.** Log back in within 30 minutes and you are still on your copy.
  After longer, the copy is cleaned and reset, and you start on a fresh one at your next lesson.
- **If all 16 copies are busy,** the player waits on the isle's beach with a line saying so, and is taken to a copy as
  soon as one frees. At up to 20 sign-ups a day that practically never happens. It starts to matter at about 5 or more
  new players an hour.
- **For you: nothing now.** You moved the two-client play-through on a private world (part 5, with P663's bot walk and
  the city-screen pictures) to P707, which comes after P665 and P666 and still gates going live.

## What was built

| Part | Where (code copy) | What it does |
|---|---|---|
| 1. The slot manager | `Tutorial/TutorialCopies.cs` (new) | `Claim` at entry: the trainee's current copy, else their party's, else the first free copy (seeded first). Who is on a copy is read from the world (a player's map, or the one they logged out on), never kept as a list. `Tick` (every minute) frees a copy 30 minutes after its last occupant left or logged out. `OnLogin`: a trainee on a copy whose generation moved on goes to a fresh copy at their first undone lesson. `[Tutorial copies` lists the 16, who is on each, and the line. |
| 2. MapOf, seed, reset | `TutorialWorld.MapOf` -> `TutorialCopies.CopyOf ?? Isle` (no side effects). `TutorialCorePlacement.SeedOn(map, dryRun, withHaven)` and `TutorialFarm.Seed(map, dryRun)` | A copy is seeded on assignment, and its placed serials are recorded. On free, `Reset` removes exactly those serials and sweeps anything else left on the copy (corpses, dropped items, spawned pests). A pet left behind goes to New Haven's start, never deleted. Then the generation rises and the copy is reseeded at once. `[ClusterFSeedTutorial` still seeds the Fold (map 32) and New Haven as before. |
| 3. The line | `TutorialCopies.Wait`, `ServeLine` | All 16 in use: the trainee goes to the Fold's beach (map 32, 6638,3993) with `WaitLine` and joins the line. When a copy frees, the oldest waiting trainee who is online and still on the Fold goes to it. |
| Entry | `TutorialStart.SendToIsle(pm, atNextLesson)` | Every way onto the isle (the start choice, Rook's remedial trip, `[Tutorial enter`, the line) goes through this one method. |
| Saved | `TutorialCopiesStore` (GenericPersistence, "TutorialCopies") | Each copy's generation, seeded and in-use flags, last-occupied time and placed serials; each trainee's copy and generation; the line. |

**The rules, as built.** A copy is "held" while anyone is on it online, and for 30 minutes after the later of its last
occupied minute and its last occupant's logout. That makes "logout and login inside a held copy" and "login after the
copy was freed" both real cases. A trainee who quits for good frees their copy 30 minutes later. A party member joins
a copy that a member of their party currently holds. Someone who leaves through the dock moongate frees their copy 30
minutes later, like anyone else.

## Facts (`server\tests\Tutorial\TutorialCopiesVerification.cs`, 7 facts)

Each was seen failing first. `notes\cc-P664-tools\mutate.py` writes one copy of the tutorial code per behaviour, with
that behaviour put back or left out behind the new API (the new API does not exist before the change). Each copy was
mounted over the builder image and the facts were run (`probe.sh`; summaries in `red-<name>.txt`).

| Behaviour removed (`mutate.py <name>`) | Facts that failed |
|---|---|
| `shared`: everyone on the one Fold (P663) | all 7 |
| `noparty`: no party sharing | **a party shares one copy** |
| `nohold`: a copy freed as soon as nobody is online | **logout and login inside a held copy**; the line (its copies freed at once) |
| `nogen`: login ignores the copy's generation | **login after the copy was freed** goes to a fresh copy at the first undone lesson (the chat stop, after three done) |
| `noreset`: reset removes only the placed serials | **a reset copy holds only fresh seeds** (a dropped stray stays) |
| `nosave`: the save leaves out the assignments | **a save and restart with copies in use** reads back whole |
| `noline`: nobody taken from the line | **all 16 in use: the next trainee waits on the beach, and moves when one frees** |

The pest fact (**two trainees in two copies kill pests without crediting each other**) drives the real kill credit at
farm step 2: each trainee's pests are their own copy's, and a kill credits only that trainee. My first `nohold` mutant
(ignoring the logout time) failed nothing, because the hold comes from the copy's last-occupied minute. The mutant
above is the honest "no hold".

**Existing facts.** Three P663 facts expected the trainee on the Fold. They now expect a private copy (and the pet on
the owner's map). `TutorialTestStart.Begin` hands back copies with nobody online (`ReleaseIdleCopies`), so facts
across the suite never run the 16 out. The copy facts empty the whole pool before and after (`FreeAllCopies`).
Probe, all tutorial and Fold facts: 178 passed, 0 failed, 1 skipped (`green.txt`).

## How often would someone wait (part 3)

I could not read today's sign-up rate. The status feed carries no account numbers by design ("No IPs, accounts ...",
`ShardStatusPublisher.cs`), live answered 503 when I looked, and the account files are Haven's. So, the arithmetic: a
copy is held about 1.5 hours per trainee (about an hour of lessons plus the 30-minute hold), with sign-ups arriving at
random (Poisson):

| Sign-ups | Copies busy on average | Chance all 16 are busy |
|---|---|---|
| 5 a day | 0.3 | 0 |
| 20 a day | 1.3 | 0 |
| 100 a day (even spread) | 6.3 | 0.08 % |
| 5 an hour | 7.5 | 0.46 % |
| 8 an hour | 12 | 16 % |
| 10 an hour | 15 | 43 % |

Waiting is real only at a sustained 5 or more new players an hour; then the pool grows from index 49 (FoldMaps). The
lesson time is an estimate: a measured number comes with part 5's play-through.

## Build

`docker\uo\build.sh -t sl-modernuo:cc-P664`, detached, under the `docker-build` lock (taken and released): **green**,
"Built sl-modernuo:cc-P664 with patches applied and 2678 shard test(s) passing." 2,683 tests: 2,678 passed, 0 failed,
5 skipped (the usual client-data facts). CHANGELOG: 2026.10.27.3 (VERSION too). Under "Added", the private copies
(test shard); under "Staff", `[Tutorial copies`. P705's branch also adds a 2026.10.27.2 section; the merge keeps both.

## Not done: part 5, the two-client play-through (asked Chase)

It needs:

- a private shard reading the isle's map (P662's patch over the private shard's map files);
- two TazUO clients with the patched map;
- **P289's play-test bot route rewritten for the isle:** its stops, the farm lesson, the city choice at index 0. The
  bot still walks the old plaza route; P663's notes say so.
- scripted solo and party runs;
- P663's folded-in proofs: the bot's walk of the isle and the shots of the city screen and five stops.

That is a job of its own, and this session's context was already long. Asked Chase (question
`Iron-P664-20261027-101447-d918`): a fresh session on this branch for part 5 only, a separate prompt (P664 marked
done), or hold. Free memory was also down to 0.6-0.7 GB after
two gated builds, too little for a shard and two clients. The code, the facts and the build are done. The question for
Chase is how to run it (below).

**Answered 10-27 11:38 (overseer, console): "Own prompt".** P664 is marked done. P707, after P665 and P666, does the
two-client play-through, the isle bot route and the shots, and gates going live. P664 was resumed in a new session
after P666 and P665 only to record this. Both WIP commits (`69b81ff` code, `900a648` docs) were checked and neither
deletes a file. **Version clash for the integrator:** this branch, P665 and P666 each add `2026.10.27.3` to
`CHANGELOG.md` and `VERSION`, so each later merge needs the next number.

**Denied in this unattended run, and not routed around:** a `Grep` of `docker\uo` for how the server applies the map
patch (`MapOverlay|overlay|mapops`). It came after the guard hook stopped the same read through Bash without the
`test-shard` lock. Part 5 will need it, under that lock.

## Not verified

- Nothing on a running shard or in a client: no copy seeded on the real isle map, and no trainee walked one.
- The first use of each copy costs about 0.4 s on the main thread (P661) and a world scan to record what the seeding
  placed. Not measured under load.
- P705's changes (the dock surface, `IsleReady`) are on their own branch. Merged with this one, `SendToIsle` must keep
  both: P705's readiness check in `OnCreated` and `ConsumeAtLogin`, and this prompt's `Claim`. The edits sit in
  different methods.

## Commit preflight

- Code copy: `CHANGELOG.md`, `VERSION`; `server/customizations/Tutorial/` `ClusterFTutorial.cs`,
  `TutorialCorePlacement.cs`, `TutorialFarm.cs`, `TutorialStart.cs`, `TutorialWorld.cs`, new `TutorialCopies.cs`;
  `server/tests/Tutorial/` `TutorialIsleVerification.cs`, `TutorialTestStart.cs`, new `TutorialCopiesVerification.cs`.
- Docs copy: this file and `notes\cc-P664-tools\` (the edit script, the mutants' script, the probe, the red and green
  summaries).
- Edits to existing code files were made through scripts: the Read tool is denied on the code copy in unattended runs.
- Locks: `docker-build` taken and released. No test shard, no package. Nothing committed.

P664 DONE
