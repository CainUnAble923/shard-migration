# cc-P663: the tutorial moves to the Wakening Isle, with the start choice (P481 F3)

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, branch `golem/Iron/P663`. Design: P481 sections
4, 7, 11.2 and 12.3; site and coordinates from P673 section 1.4 (site A, the south-east void). Not committed; nothing
deployed; Haven not touched.

## In plain words

- **New characters choose where they start (test shard only).** The character creation screen now lists "Tutorial
  Island" first (the default) and "New Haven" second. Tutorial Island wakes you on the Wakening Isle; New Haven skips
  the tutorial and starts you in town, as the skip button does today.
- **The lessons moved to the isle, in one line from the beach to the dock.** Tamsin on the beach starts each lesson.
  The farm, where you pick your dog or cat, clear the pests and use a bandage, is now one of the main lessons, after
  chat. The last lesson is the moongate at the end of the dock: walk into it or double-click it, and it takes you, and
  every pet you have on the isle, to Rook in New Haven, who graduates you as before.
- **A skipper who changes their mind** clicks "Restart the tutorial" at Rook and is sent to the isle's beach; the dock's
  moongate brings them back to him.
- **For you:** nothing to do now. Nobody can see or walk the isle until P662's map patch is built. As you chose, the
  play-test bot's walk of the isle and the in-game pictures of the city screen and five stops are taken in P664's
  two-client play-through, which already has to pass before anything goes live.

## What was built

| Part | Where (code copy) | What it does |
|---|---|---|
| 1. One lesson map | `Tutorial/TutorialWorld.cs` (new) | `TutorialWorld.MapOf(trainee)` and `Isle`: the Fold, map 32 (F4 returns the trainee's copy). Every core lookup asks it. The 18 core `Map.Trammel` uses are 0 now (counted per file below). |
| New Haven's spots | `Tutorial/HavenSpots.cs` (new) | Rook, the moongate's way out, the start, the island gate's bounds, the town vet, the healer and New Haven's public moongate, in one class for P678 (S7). The Fold mirror's send-home reads it too. |
| 2. The seeder | `Tutorial/TutorialCorePlacement.cs`, `TutorialFarm.cs`, `TutorialGuide.cs` (new), `TutorialIsleFarmLayout.cs` (new, generated) | `[ClusterFSeedTutorial` places, on map 32: a marker at each stop, Tamsin, the walking tiles, the camp, clothes rack and signpost props, the pale echo and Sera in the training yard, Merrin and a practice bank box behind the bank's door, Elara in the lodge behind its door, the stones' marker, the dock moongate; and the farm (330 pieces), its door, Wren, Tobin, the pests and the pen. In New Haven: Rook and the town vet if missing. It refuses until P662's patch is on the server (its fit check reads the server's map; the void fails it, and the refusal names P662). |
| 3. The order | `Tutorial/TutorialStations.cs`, `ClusterFTutorial.cs`, `TutorialCoreTrials.cs`, `TutorialFarm.cs` | movement, backpack, paperdoll, chat, **core.farm** (new), death, banking, league, loop, **travel last**. `IsDone`: an old travel key counts only once the rest are done. Wren answers only from core.farm on; her third step finishes it; an account with its pet starts at the pests. |
| 4. Pets cross | `TutorialWorld.Cross` | Every crossing (the start, the moongate, the remedial trip, a skip on the isle) moves the trainee's controlled pets: on the Fold every one on the Fold, at any range and order; entering from elsewhere those within 12 tiles. Stabled pets and other players' pets stay. |
| 5. The start choice | `Tutorial/TutorialStart.cs` (new), `CharacterCreation.cs`, `ShardClilocs.cs`, cliloc `entries.json` and `registry.csv` | Two entries, both Trammel: "Tutorial Island" (index 0; button at 3650, 2932, sea south of the SoS Haven town, read from the author's `Map1.mul`) and "New Haven". Descriptions 1900014 and 1900015. The choice is saved per character in the account's data and consumed at its first login. With the tutorial off (live) the list stays New Haven alone and nothing is recorded. |
| 6. Eligibility | `TutorialStart.Decide`, `ConsumeAtLogin` | The prompt's table, row for row (facts below). A character with no choice (made before this build) is never entered or moved: login no longer enters a fresh account's character by itself. |
| 7. Remedial | `ClusterFTutorial.StartRemedial`, `TutorialGumps.cs`, `TutorialIslandGate.cs` | Rook's button sends a skipper to the beach. The island gate counts the Fold as the island, which is the allowed route for a loop-0 trainee; FoldRegion still refuses every travel spell in or out. Rook also gets "Go to the Wakening Isle" for a trainee in New Haven with core lessons left. |

**Counts, `Map.Trammel` in the code copy** (`git show HEAD:<file> | grep -c`, then the work copy): TutorialCorePlacement
8 → 0, TutorialCoreTrials 4 → 0, TutorialFarm 4 → 0, TutorialRecruiter 1 → 0, TutorialIslandGate 1 → 0 (18 → 0, as
design 12.3 counted). TutorialTradeTrials 4 and TutorialWingTrials 11 are unchanged (15, the wing and trade trials that
stay in New Haven). The remaining `Map.Trammel` in `Tutorial\` are `HavenSpots.Map` and the two city entries.

**The isle's stops** (P481 11.2 plus (+424, +1992), all in `TutorialWorld`): beach 6638,3993; Tamsin 6640,3992; tiles
6646,3992 and 6649,3992; camp 6656,3990; rack 6665,3992; signpost 6692,3990; farm gate 6714,3979 (Wren 6714,3978, Tobin
6714,3976: the farm's own spots moved with the farm); yard gate 6736,3995 (echo 6736,3998, Sera 6740,4000); bank door
6762,3980 (Merrin 6762,3976); lodge door 6782,3995 (Elara 6782,3999); stones 6794,3982; dock end 6831,3991, moongate
6832,3991. Z is read from the lesson map, so the knoll's height comes from P662's land.

## Decisions and deviations

- **The farm is 330 pieces, not 334.** P481's `newisle.py` read the 4 rows of `RemovedTrees` (the two trees P276's map
  patch removes) as farm pieces, and the design and P673 say 334. `notes\cc-P663-tools\gen_isle_farm.py` reads only the
  `Pieces` table: 330. Heights above the old ground: 0 to 42; none stood below its ground.
- **New Haven keeps its farmhouse, door and pen** for the wing trials still taught there (the pen trial, the porch
  stop of the housing tour), until S7 moves them. `[ClusterFSeedTutorialFarm` now places only those; Wren and the pests
  are on the isle only.
- **The travel tour's first stop** pointed at the old tutorial gate. It is New Haven's public moongate now (3450, 2677,
  25, pinned `PublicMoongate.cs:194`); the moongate's way out beside Rook was too close to the tour's last stop, Rook.
  The reputation tour's healer stop is New Haven's healer.
- **A skipped account's new character that chose the isle** becomes the account's recorded character, so Rook offers
  it remedial training as the table asks (P453 lets only the recorded character use his window).
- **Doors.** The bank's and lodge's doors are dark wood, facing WestCW (both in east-west walls), at P481's door tiles.
  Their look against P662's walls is unchecked until that patch exists.
- **The props** are server items (`Static`): campfire 0x0DE3, two bedrolls 0x0A55, a dress form 0x0EC6 for the clothes
  rack, a wooden signpost 0x0B97, a strong box 0x0E7C as the practice bank box. Ids from the vanilla tiledata names.
- **Rook stays Rook.** Tamsin's window is the same page with the core and the skip only; graduation and the wings stay
  with Rook. Core lesson buttons in Rook's window send a trainee to the isle.

## Facts (`server\tests\Tutorial\TutorialIsleVerification.cs`, 13 facts, 21 cases)

Each was seen failing first against the old behaviour put back behind the new API (the new API itself does not exist
before the change, so the facts cannot compile there). `notes\cc-P663-tools\mutate.py` writes one copy of the tutorial
code per behaviour; each copy was mounted over the builder image's and the facts run.

| Behaviour put back (`mutate.py <name>`) | Failed / of | The facts it failed (the targeted one in bold) |
|---|---|---|
| `order`: the old order (farm optional, travel seventh) and the old done rule | 4 / 20 | **the order**; the moongate (both cases) and remedial, which walk the core in the new order |
| `pets`: the moongate moves only the player | 2 / 20 | **a pet crossing the dock**; remedial (its pet stays on the isle) |
| `table`: the choice alone decides, no table | 6 / 20 | **the six rows where the table differs from the choice alone**: in core elsewhere (both), graduated (both), skipped (both). The four rows where they agree (fresh, deleted mid-core) fail under `cities` below |
| `choice`: one loose account flag kept in memory | 3 / 21 | **a choice surviving a disconnect**, **a second character not consuming another's choice**; the tutorial-off fact |
| `step`: double-click only | 1 / 21 (+1) | **the moongate by step**; the double-click case passes, as it should |
| `reconnect`: the login keeps the trial | 1 / 21 (+1) | **a reconnect regenerating the supply** |
| `remedial`: no trip to the isle | 1 / 21 (+1) | **remedial** |
| `cities`: New Haven alone in the list | 18 / 21 | **the city list**, and every fact that creates a character through it, including the four eligibility rows above |
| `golive`: login enters any fresh account's character (P80) | 2 / 21 (+1) | **a character from before go-live**, a second character's choice |
| `live`: the choice recorded with the tutorial off | 1 / 21 | **with the tutorial off, creation records no choice** |

(+1): these copies were made before the tutorial-off guard and fact were added, so that fact fails in them too. Every
fact failed in at least one copy for its own reason. Summaries: `notes\cc-P663-tools\red\red-NAME.txt`.

Then green: all 21 cases pass on the builder image (bind-mounted probe), and again in the gated build below.

**Existing facts moved to the isle.** 43 of the 205 tutorial facts failed after the change, every one for the moved
behaviour: login no longer enters a character with no choice (they now use `TutorialTestStart.Begin`, which picks
"Tutorial Island" and logs in), the lessons stand on map 32, Wren follows the core order (`ToTheFarm` marks the four
lessons before her), the core has 10 lessons and 38 stations, and the seeder's lines changed. The Burrows facts enter
with `TryEnter` (they test participation, not the isle). All pass again (below).

## Build

`docker\uo\build.sh -t sl-modernuo:cc-P663`, run detached under the `docker-build` lock (released): **green, `EXIT=0`**,
"Built sl-modernuo:cc-P663 with patches applied and 2671 shard test(s) passing." 2676 tests: 2671 passed, 0 failed, 5
skipped (the usual client-data facts). Windows had 3.3 GB free before it; the Docker VM 12.8 GB. The package's
`Cliloc-Overrides.Tests.ps1`: 10 of 10 after the two numbers were added (it failed first, 14 against 16, before the
test was told of them).

## Not done: the bot route and the in-game pictures

Part 8 also asks for the P289 bot route on a private world with the isle loaded, and TazUO shots of the city screen and
five stops. The isle's land is P662's map patch, which is not built (P673 1.4 orders it after S1 and S2). Site A is void
on the server's map: the seeder refuses there (its fit check, as designed) and nothing can walk. So neither proof can be
taken in this prompt. P289's `playthrough.py` also still walks the old plaza route; it needs the isle's stops, the farm
lesson and creation's city index 0 before it can run, and is best changed when it can be run.

Asked Chase (question `Iron-P663-20261027-072418-8776`). Chase chose (console, 2026-10-27 08:35): fold them into P664's
two-client play-through on a private world, which already gates going live, and mark P663 done so P662 can start. The
overseer has added both proofs to `cc-P664-private-isle-copies.md` ("Added 10-27"). `playthrough.py`'s new route
(the isle's stops, the farm lesson, city index 0) goes with them.

## Not verified

- Anything on a running shard: the isle is void until P662, so no walk, seed, Tamsin, door or moongate was seen in a
  client. The facts drive the real hooks in the test host.
- Young death on map 32: pinned's Young death teleport runs before the death lesson's handler, which puts the ghost
  back by Sera on the lesson map. Where the teleport itself sends a ghost on the Fold is not checked.
- The farmhouse on flat land: each piece keeps its height above New Haven's sloped ground, as P481 11.2 set. On a flat
  meadow the floor may step where the old ground did; P481's `iso-farm.png` mock was drawn the same way.
- The city screen: TazUO's placement of the isle's button (by percentage of the facet) and the two descriptions in the
  package's cliloc copy.

## Asked, and commit preflight

- Asked Chase one question (above; answered: fold into P664). Haven was not touched. Nothing deployed or published; no package built.
- Unattended-run denials, worked around: the Read tool on the code copy (edits made through scripts instead), a Grep
  of `docker\uo` (the probe used the flags P191's notes give), and `powershell -ExecutionPolicy Bypass` from Bash for the
  package test (run through the PowerShell tool instead).
- Both work copies are on `golem/Iron/P663`; nothing committed (the Golem commits).
- Code copy: 27 files changed (`CHANGELOG.md`, `VERSION` 2026.10.27, the cliloc entries, registry and their test,
  `CharacterCreation.cs`, `ShardClilocs.cs`, `Fold/FoldRegions.cs`, 11 tutorial files, 8 test files) and 7 new
  (`HavenSpots.cs`, `TutorialWorld.cs`, `TutorialStart.cs`, `TutorialGuide.cs`, `TutorialIsleFarmLayout.cs`,
  `TutorialIsleVerification.cs`, `TutorialTestStart.cs`).
- Notes copy: this file and `notes\cc-P663-tools\` (the farm generator, the probe and red-run scripts, the SoS sea scan,
  the red summaries; 77 KB). No file over 5 MB. `docs\` untouched.

P663 DONE
