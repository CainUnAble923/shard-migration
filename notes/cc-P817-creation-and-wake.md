# cc-P817: creation and the isle start: humans only, no trade choice, Tutorial Island only, a brighter wake, the pet at the end

## In plain words

- **Character creation is simpler.** The race row shows Human only (Elf and Gargoyle are gone), the profession list no
  longer has the Blacksmith (the "trade" start that gave Blacksmithy, Tailoring, Tinkering and Mining at 30), and the
  start map shows Tutorial Island alone. New Haven is still reached through the isle's moongate. An old or
  third-party client asking for any of these is refused or corrected by the server.
- **Waking on the beach is bright.** The washed-ashore moment had a gray dusk that lasted until you took a step (up to a
  minute). It is now a light morning shade, with a one-second dawn when you get up; the isle is daylight at any hour.
- **Your pet waits at the end of the isle.** The farm (Wren, the pests, the dog or cat) is now the last lesson before
  the moongate. Pip's bandaging lesson stays where it was, after chat. The farm is at the west end, so the last lesson
  means walking back from the standing stones to the farm, then out to the dock (my proposal for that is below).
- **Merrin the banker faces his counter and talks.** On the bank lesson he greets you as you come in and says what to
  do ("say 'bank'", then "drag the blue practice token in"). The bank got a tidy-up: the lesson sign moved off the road
  in front of the door to the grass by the corner, the practice bank box and the strongbox moved from the middle of the
  floor to the back wall with the vault chests, and a crowding potted plant went.
- **For you:** (1) the overseer applies `notes\cc-P817-tools\p817-release-isle-20261028.diff` and builds the next
  isle package from it: the race row and profession list need that package (new client patch 0012), the rest is the
  server. (2) Say if you want the farm moved east near the dock (section 5); I did not move buildings. (3) The brass
  fountain on its own pad in front of the bank is kept; say if you want it gone or moved (section 7).

Iron Golem, 2026-11-07. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P817`. Isle release copy `D:\UO\golems\Iron\p817-isle`, a detached worktree at `56f98af` (the
`release/isle-20261028` tip), the change staged. Nothing committed, `latest` not moved, nothing published.

## 1. Humans only

- Client: new `client/patches/0012-humans-only.patch` (TazUO `CreateCharAppearanceGump.cs`): the Elf and Gargoyle radio
  buttons and labels are not added; Human was already the default, Male and Female stay. Applies with `--fuzz=0`; the
  private client build and the package build both applied it (`client-build.log`, `package-build.log`: "TazUO 3212623f
  + 12 patches"). Shot: `notes/cc-P817-shots/creation-1-races-before.jpg` and `creation-1-races-after.jpg` (one HUMAN
  button left).
- Server: main already turns an elf or gargoyle create packet from a player account into a Human, with a log line
  ("{Race} refused at creation ... made Human") and a message to the player (P762, `NewCharacterRules.RaceFor`, used
  in `CharacterCreation.cs`). The new fact `P817_AnElfOrGargoyleAskedForIsMadeHuman` (theory: elf, gargoyle) pins it.
  It was green before the change, as expected, so nothing in main changed for it.

## 2. The trade choice

- The "trade" start is the stock Blacksmith, profession 3, which this shard calls the Maker (Mining, Blacksmithy,
  Tinkering, Tailoring). No other creation screen had a trade-like choice, so this is the one removed.
- Server: `ClusterFStartChoices.RemovedProfessions` now holds the Maker; the create is refused with a log line naming
  it, like Necromancer, Paladin, Samurai and Ninja. The crafts stay pickable under Advanced (choose your own skills).
  Fact `P817_TheTradeProfessionIsRefused`.
- Client: the profession list comes from the player's own EA `Prof.txt`, which we never ship. The package's
  `Build-UoOverrides.ps1` now writes a copy of it without professions 3-7 into `app\uo-overrides\Prof.txt` (stamped,
  rebuilt only when the source changes) and lists it in the override map, as it does for cliloc and music. Facts:
  `player-package/tests/Prof-Overrides.Tests.ps1` (4 facts green, including "the screen leaves out exactly what the
  server refuses", read from the C# list). The TazUO shot's plugin log reads "professions the client lists: WARRIOR,
  MAGE, Advanced" (`creation-2-professions-after.jpg`, `creation-plugin-log.txt`). The isle release still offers
  Necromancer and the rest, so its copy leaves out only the Blacksmith (`notes/cc-P817-tools/isle_profession.py`).

## 3. Tutorial Island only

- `TutorialStart.Cities(account)` sends the isle alone while New Haven's start switch is off (players); staff and an
  open switch still get both. An old client that asks for a second entry is refused by pinned's create handler
  ("Invalid city selected"), and `Decide` turns any pick into the isle as before. New Haven is still reached through
  the isle's moongate and the moongate skip (P762, untouched). Fact
  `P817_TheStartMapIsTutorialIslandAloneAndStaffKeepBoth`; P762's facts updated to the one-entry list. Shot
  `creation-3-start-map-after.jpg` (only "Tutorial Island" on the map).

## 4. Too dark on startup

- Cause: not the shard clock or the package profile. The isle region is already always day
  (`FoldRegion.AlterLightLevel`, `LightCycle.DayLevel`). The dimness was the wake scene's own personal light: P740's
  `TutorialWake.DarkLight = 16`, held while the trainee lies on the sand, up to `SafetySeconds` if they do not know to
  take a step, then a two-step dawn.
- Fix: `DarkLight` 6, a `BrightestWake` cap of 8, one dawn step (3) after the get-up. Only the wake scene's personal
  light changed; no region or global light anywhere else. Fact `P817_TheWakeIsBrightAndTheIsleIsDayAtAnyHour`
  (the wake light at its darkest and the isle region's level at a night hour on the clock). P740's wake facts updated.
- Shots from the default camera, a fresh character each: `wake-before-1s.jpg` / `wake-before-20s.jpg` (gray dusk) and
  `wake-after-1s.jpg` / `wake-after-20s.jpg` (sand, palms and road in clear light).

## 5. The pet at the end of the isle

- `TutorialStations`: `core.farm` moved from after chat to after `core.loop` (the standing stones), last before
  `core.travel` (the moongate). Pip's healing lesson stays after chat at the farmhouse; Wren still hands bandages
  during it (`TutorialFarm`, new branch), since the healing hint points at her. Wren's done line now sends the trainee
  to the moongate; the farm's arrow line and quest-log hint say "back west along the road ... past the farmhouse".
- Records hold done keys, not positions: a character who already did the farm keeps it done and is not sent back, and
  `PetClaimed` still blocks a second pet. The moongate skip's pet scroll is unchanged. Facts
  `P817_TheFarmIsTheLastLessonBeforeTheMoongate`, `P817_AFarmDoneEarlierIsNotAskedAgainAndTheFarmComesAfterTheStones`,
  `P817_WrenHandsBandagesDuringTheHealingLessonBeforeTheFarm`; the pet reward and bandage-wait facts re-threaded.
- **The walk (proposal, nothing moved).** The isle is one road west to east: farm and farmhouse at the west end by the
  chat signpost, the stones on the knoll in the east, the dock and moongate east of that. With the farm last, a
  trainee walks from the stones back west along the whole road to Wren (the arrow leads), then east again to the dock.
  It reads, but it is a long double-back. Proposal: move Wren's gate, the cabbage rows and Tobin to the open ground
  just west of the dock road, so the stones, the farm and the moongate run in one line; the farmhouse with Pip stays.
  That is a building move, so it is for a later prompt if you want it.

## 6. The banker

- Merrin (`TutorialWorld.Banker`, 6762,3976) had no facing set, so he faced north at the vault chests. New
  `TutorialBankerVoice.cs`: he faces South, across the counter toward the carpet and the door (guide 3 and 11.2);
  `TutorialCorePlacement.SeedOn` turns an already seeded Merrin on every world load. Shot `bank-inside-after.jpg`.
- His voice: on the bank lesson, step 0 or 1, within 5 tiles, he says to that trainee alone "Welcome to the bank! Say
  'bank' and I will open your bank box." and, once the box is open, "Drag the blue practice token from your backpack
  into it.", then waits 25 s before saying it again. The full steps stay in the lesson window. Facts
  `P817_TheBankerFacesHisCounterAndSeedingTurnsAnOldOne`, `P817_MerrinSaysTheNextStepNearbyAndWaitsBeforeSayingItAgain`
  (also watched red alone, `red-merrin.log`).
- Every other isle NPC's facing is listed in `notes/cc-P817-review/placed.md`: none faces a wall, none changed. I meant
  to take a client shot of Sera in the yard too; Docker Desktop stopped before that shot ran, so Sera's verdict rests
  on the map (open yard, nothing north of her), not a shot.

## 7. The bank decoration pass

- Mockup `notes/cc-P817-review/bank-mockup.png`, before/after cutaways and isorenders in the same folder, client shots
  `bank-outside-before.jpg` / `bank-inside-before.jpg` and `bank-outside-after.jpg` / `bank-inside-after.jpg` in
  `notes/cc-P817-shots/`, every piece in `placed.md`.
- Changed: the lesson signpost from the road at the apron's east end to the grass at the bank's south-west corner, off
  the apron and the door's line (guide 6); the practice bank box from mid-floor to the back wall with the vault chests;
  the strongbox from the east wall to the back wall under the north torch; the inside potted plant in the south-east
  corner removed (it crowded the candelabra). Statics in `trammel.mapops` (one line moved, one gone) and the driver's
  `notes/cc-P662-tools/isle-sets.json`, so a rebuild lays the same; the server pieces move on load (`MoveOldProps`,
  `MoveToSign`). Facts `P817_ThePracticeBankBoxStandsOnTheBackWallAndAnOldOneIsTakenAway`,
  `P817_TheBankSignStandsOffTheRoadAndTheApron`.
- Kept and checked: the counter line with gold and scales on it, three vault chests, two candelabra, three wall
  torches, bench, carpet, the hanging bank sign two east of the door, the potted plant outside by the door; no stray or
  doubled pieces in walls or floor. The prompt's "brazier on its own paved pad" is a brass fountain (P720's addon); it is
  kept, a proposal for Chase.

## Tests, builds, package

- Red first: `notes/cc-P817-tools/red.log`: 12 new facts, 10 failed and 2 passed (the elf/gargoyle theory, already
  true on main, see 1). Green: `green.log` 12 of 12, `green-broad.log` the isle and creation suites.
- Gated build through `docker/uo/build.sh` as `sl-modernuo:cc-p817`: 3,280 tests, `EXIT=0`
  (`green-gated-build.txt`). `latest` not moved.
- Isle release: `notes/cc-P817-tools/p817-release-isle-20261028.diff`, applied in a detached worktree at `56f98af`
  (`release/isle-20261028`). Conflicts, resolved in the diff: the release has no P714 start rules
  (`ClusterFStartChoices`), so the Blacksmith refusal goes into `CharacterCreation.cs` and `NewCharacterRules.cs`
  there, and the release's `Prof.txt` copy leaves out profession 3 only. Built as
  `sl-modernuo:cc-p817-isle`: 2,988 tests, `EXIT=0` (`green-gated-build-isle.txt`).
- Player package: built through its own build, `ShatteredLegacy-2026.11.07.1511.zip` in `D:\UO\golems\Iron\p817-pkg`,
  gates 4, 5 and 6 passed (`checkzip.log`). Not published. The shots ran on that package's client against the private
  proof shard on port 2596.
- `CHANGELOG.md` 2026.11.07.8 with Chase's line, `VERSION` 2026.11.07.8.
- Docker Desktop was down when this session resumed (17:10); everything above had finished before that. No locks held.

## Files

Code copy: `client/patches/0012-humans-only.patch`; `player-package/payload/app/Build-UoOverrides.ps1`,
`player-package/tests/Prof-Overrides.Tests.ps1`; `player-package/vendor/shattered-legacy-map/trammel.mapops`,
`SOURCE.txt`; `server/customizations/ClusterFStartChoices.cs`; `server/customizations/Tutorial/` `TutorialBankerVoice.cs`
(new), `TutorialCorePlacement.cs`, `TutorialCoreTrials.cs`, `TutorialFarm.cs`, `TutorialStart.cs`,
`TutorialStations.cs`, `TutorialWake.cs`; tests under `server/tests/Tutorial/` and `server/tests/Misc/SchoolGateVerification.cs`;
`CHANGELOG.md`, `VERSION`. Docs copy: this file, `notes/cc-P817-review/`, `notes/cc-P817-shots/`, `notes/cc-P817-tools/`,
`notes/cc-P662-tools/isle-sets.json`.

P817 DONE
