# cc-P705: the Codex findings on P663 (dock surface, start fallbacks)

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P705` (P663 merged in; P662's map patch not in this branch). The review:
`notes\cc-P663-tutorial-moves-to-isle-codex-review.md`. Not committed; nothing deployed; Haven not touched.

## In plain words

- **No one can land in empty darkness any more (test shard).** If a server has the start choice but not yet the
  isle's map, picking "Tutorial Island" starts the new character in New Haven with a note saying so. Their account
  keeps its tutorial, so a character made once the isle opens can still take it.
- **Staff characters made with the default "Tutorial Island" start in New Haven**, not out at sea where the island's
  button is drawn on the city screen.
- **The dock's lesson marker and moongate stand on the dock**, not on the sea floor under it. On the isle's real map
  that would have made the tutorial's setup command refuse.
- Nothing for you to do. These ship with the tutorial.

## The three findings and the fourth fix

| Finding | Fix | Fact (`TutorialIsleVerification`) | Seen failing first |
|---|---|---|---|
| **P1, high:** the dock's stops resolve the land's Z under the planks | `TutorialWorld.Ground` stands on the highest walkable surface (Surface, not Impassable) whose top is above the land and within a person's height of it (16, pinned Movement), else the land's average Z. The rule is in `SurfaceZ`: planks 2 above the sea are stood on; a roof 20 above a floor is not | `TheGroundIsTheWalkableSurfaceNotTheLandUnderIt`: a plank over the sea gives -2; a floor under a slate roof gives 0; static water is no surface; bare land is the land | mutant `surface` (land Z only): this fact fails, 24 pass |
| **P2:** the tutorial-off New Haven entry uses literal coordinates | `CharacterCreation.TutorialOffCities()` builds it from `HavenSpots.Start` and `HavenSpots.Map`. `HavenSpots.Start` became a property, settable only as a test seam (the codebase's idiom, like `FitsOn`); S7 still changes its value in one place | `TheTutorialOffListReadsNewHavensStartFromHavenSpots`: moves the start, and the entry follows | mutant `havenoff` (the literal back): fails |
| **P2:** staff with the default isle pick get the display spot in the sea | `TutorialStart.OnCreated`: anyone not enrolled (staff, or the tutorial off) whose city is the isle entry gets New Haven's start. Staff are still never enrolled | `StaffWhoPickTheIsleStartInNewHavenNotInTheSea` | mutant `staff`: fails |
| **The missing isle** (the prompt's own) | `TutorialWorld.IsleReady` (a seam; default: the beach `CanFit`s a person). It is false while the site is void (no P662 patch). Creation then places an isle pick in New Haven. The first login gives the new outcome `IsleMissing`: New Haven, a system line saying the isle isn't open yet and the account's tutorial is unused, the choice consumed, nothing entered or skipped | `WithoutTheIslesLandTheIslePickStartsInNewHaven`; also, once the land is there, the account's next character goes to the isle as usual | mutant `missing` (no check): fails |

The mutants (`notes\cc-P705-tools\mutate.py`) each put one fix's old behaviour back behind the new API, because the new
API does not exist before the change, so the facts cannot compile there. They were mounted over the builder image
(`probe.sh`, P663's probe with the CharacterCreation copy selectable). Each failed exactly its own fact; the other 24
isle facts passed (`red-<name>.txt`). On the real code all 175 tutorial and Fold facts pass; 1 is skipped, the usual
client-data fact (`green.txt`).

**The seam in the existing facts.** The test host's world has no map data at the isle's site, so its `CanFit` cannot
stand for P662's land. The facts that go to the isle set `IsleReady` to true: `TutorialTestStart.Begin`, and the isle
facts' fixture, which also restores it. In round 1 I had a fact "on the host's map the isle is not ready". It failed
because the host has no map data at all (`CanFit` succeeds anywhere), so I dropped it. The real check belongs to
P664's play-through on a private world with P662's patch, and to a server before that patch.

**`SurfaceZ` takes each tile's flags and height** rather than an item id. The test host loads no tiledata, so an id
reads as "no surface" there; round 1 failed that way. `Ground` looks the flags and `CalcHeight` up in `TileData` itself.

**With P662's map:** P662 ends the dock on a stone landing (land at the deck's height) under the moongate and the
dock-end stop, so those two stand on land either way. This fix makes any plank-covered stop right too.

## Build

`docker\uo\build.sh -t sl-modernuo:cc-P705`, detached, under the `docker-build` lock (taken and released), WSL page
cache dropped first: **green**, "Built sl-modernuo:cc-P705 with patches applied and 2675 shard test(s) passing."
2,680 tests: 2,675 passed, 0 failed, 5 skipped. The four new facts pass in it. Free memory fell to 0.6 GB near the end:
the session's background waiter was stopped for low memory, but the build itself finished.

CHANGELOG: a new 2026.10.27.2 section (VERSION too). Under "Fixed", the missing-isle fallback (test shard). Under
"Staff", the staff start, the tutorial-off start and the dock spots.

## Not verified

- Nothing on a running shard or in a client. The missing-isle message and the dock surface were not seen in game.
- `IsleReady`'s real default (a `CanFit` at the beach) was not run against a real map: the host has none.

## Commit preflight

- Code copy: `CHANGELOG.md`, `VERSION`; `server/customizations/CharacterCreation.cs`, `Tutorial/HavenSpots.cs`,
  `Tutorial/TutorialStart.cs`, `Tutorial/TutorialWorld.cs`; `server/tests/Tutorial/TutorialIsleVerification.cs`
  (4 facts, the seam set and restored), `TutorialTestStart.cs` (the seam).
- Docs copy: this file and `notes\cc-P705-tools\` (the edit scripts, the mutants' script, the probe, the red and green
  summaries; 37 KB).
- Code edits were made through scripts: the Read tool is denied on the code copy in unattended runs.
- Both copies on `golem/Iron/P705`; nothing committed. No question asked of Chase.

P705 DONE
