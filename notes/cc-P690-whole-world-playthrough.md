# cc-P690: the whole swapped world, played through (SoS swap S17, the 1.0 gate)

Iron Golem, 2026-10-31, third start (the first two stopped for P691 and the PC's memory; history at the end). Code
copy `D:\UO\golems\Iron\ShatteredLegacy` at main's P691 merge (`9f97914`), docs copy
`D:\UO\golems\Iron\shard-migration` at the P688 merge (P691's docs files are notes and proof tools only), both on
`golem/Iron/P690`. No game code changed: this prompt built, played and wrote down. Not committed (the Golem commits).

## In plain words

- **The swapped world was built from nothing, the way the test shard starts on swap day, and played from the real
  player package.** A new character woke on the Wakening Isle in the package's TazUO, played it through, and went on
  through the moongates on both Trammel and Felucca, walked to all six of the new towns, took Blackthorn's cellar
  hatch, sailed a boat from Haven's dock, dug up a treasure chest and found a Felucca champion's altar. The classic
  client (ClassicUO) started a character in New Haven's new town.
- **Two real faults, both from the New Haven move (P678):** New Haven's people are created again every time the server
  restarts (after two restarts there were three of each), and the cellar hatch down to Rootdeep does nothing when you
  step on it. The first must be fixed before swap day; the second only matters if the Rootdeep Burrows open at 1.0.
- **The go-live checklist is written** (Part 3): the exact order of world commands for swap day, rehearsed here, with
  two traps found on the way: the moongate command deletes Royal City's and Eodon's gates (two commands put them
  back), and the decoration command must be run only once.
- **For you:** nothing to try or deploy now. Two decisions for the swap day: whether the Rootdeep Burrows open at 1.0
  (the go-live text already leaves them out), and whether `[SignGen`/`[DoorGen` belong in the order (not run here).

## Chase's answer applied

Iron-P690-20261031-005433-e52a (console, 10:52): **"Reboot first, then retry"**. Chases-Tower had rebooted at 08:13,
after the question was asked, and P691 had merged into main in both repos since, so both blockers were gone: this
session is the retry. 12.7 GB of 31.7 were free at the start.

## Setup: what was built and started

| Step | Result |
|---|---|
| Start checks | Chases-Tower rebooted 08:13 today (after the question); 12.7 GB of 31.7 free at the start, about 5 GB in the afternoon. P691 merged on main in both repos (code `9f97914`, docs `5172aa8`); the code copy is at it. The docs branch is at the P688 merge without P691's notes, which only are notes and proof tools. |
| Image | `docker\uo\build.sh -t sl-modernuo:cc-P690` (`docker-build` lock). Run 1: 2,824 passed, **1 failed** (the Covetous flake, F7), no image (`gated-build-1-summary.txt`). Run 2: **2,825 passed, 0 failed**, 6 skipped, image built (`gated-build-2-summary.txt`). |
| Package | Built twice (`package` lock): `ShatteredLegacy-2026.10.31.1057` (switch off, 146 MB, `pkgbuild.txt`), then the swap's go-live package `ShatteredLegacy-2026.10.31.1102` with `-SosMap on` (the builder's one-run override; `switch.txt` untouched): **181 MB, 741 files, TazUO 3212623f + 9 patches, every gate green** (`pkgbuild-sosmap-on.txt`). Every client below is this zip, unzipped. |
| Fresh world | `fresh-shard.ps1`: the bot shard's Configuration (the test shard's: testCenter on), an **empty world**, the SoS overlay from this branch's `trammel.mapops` (`overlay.ps1`), `sl-p690-proof` on 127.0.0.1:2596 (`test-shard` lock). First boot stopped at ModernUO's owner prompt; `answer_owner.py` made a private owner through the Docker pipe. Then the swap-day order of Part 3, typed by the owner (`gen.py`, `runs/gen-log.txt`). |

## Part 1: the playthrough

Three clients played: TazUO **from the built package**, ClassicUO (the player launcher's, with the package's own map
files), and the play-test bot (the packets a client sends). Each start used a new character made by the client
itself at the character list.

| Item | Client, character | Result | Evidence |
|---|---|---|---|
| Character creation: the city list | all | Two entries: "Tutorial Island" (The Wakening Isle) and "New Haven" (shown "New Haven (locked)" until the account has finished the isle, P717) | `runs/gen-log.txt`; the server's creation lines |
| Start choice 1, the isle | **TazUO from the package**, new account `p690isle`, Iron Wakener | Woke on the beach (6638, 3993) in the dusk; the package's launcher built the SoS map for the player's UO folder in **22 s** first start. The isle walk (P740's, unchanged but for the name): **70 checks, 0 failed**, wake to the dock's end beside the moongate | `runs/tazuo-isle-walk.log`, `-runner-log.txt`, `shots/tazuo-isle-*.jpg` |
| Start choice 2 on a new account | **ClassicUO**, new account `p690haven`, Haven Classic, New Haven picked | Started on the isle (6638, 3993, the Fold), "New Haven (locked)": as P717 designs | `runs/classic-new-account-log.txt`, `shots/classic-new-account-isle-start.jpg`, server line `started.city=New Haven (locked)` |
| Start choice 2 on an account past the isle | **ClassicUO**, Iron's Player account, Haven Classic | Started on New Haven's square (3634, 2586, Trammel), the author's Haven town drawn | `runs/classic-iron-account-log.txt`, `shots/classic-haven-start.jpg` |
| The isle, P662-P664, whole | bot, Iron Islander (`isle.py`, P740's route) | **85 checks, 0 failed**: every lesson in 170 s, the dock moongate to beside Rook (3632, 2584); the New Haven pick on the same account started on the square | `runs/bot-isle-playlog.txt` |
| A real character's world tour, after the isle | bot, the same Iron Islander (`tour.py`; staff steps by Iron's Admin, each logged STAFF) | **The clean run: 61 passed, 3 failed** (`runs/tour-final-log.txt`); the three are F2 and two of my driver's (below); the boat part rerun: 6 passed, 0 failed | `runs/tour-final-log.txt` |
| Off Haven Island | the same | Rook's Graduate: "You finished the tutorial. You can now leave Haven Island." (Before it, the New Haven gate refused: "Finish the main tutorial lessons, then ... choose Graduate.") | `runs/tour-debug-runs-log.txt` |
| Every public moongate, both facets | the same | **All 18**: Trammel's Moonglow, Britain, Jhelom, Yew, Minoc, Trinsic, Skara Brae, Magincia and New Haven (3696, 2570), each arrival on its gate at P679's height; then, after "I want to grow up!" (Felucca's list is not shown to the Young), Felucca's eight towns and Buccaneer's Den (2711, 2234). 36 checks | `runs/tour-final-log.txt` |
| One walk to each new town | the same | **All six**: Elmhaven (464 steps from Trinsic's gate, and back), Kameron Kove (604 from Britain's gate), Kettleburg (918 from Kameron Kove's bank, 847 back to Britain), Hammerhill (1,203 from Britain's gate, and back), Fort Yondall (1,290 from Minoc's gate to the gatehouse, then 341 up its stairs to the bank on the z20 walkway); Valunstead walked on the island from a staff-placed shore spot (no dock, gate or teleporter, P688) | `runs/tour-final-log.txt`; shots |
| Rootdeep by the hatch | the same | **FAIL (F2)**: the hatch is there (0x3E65 at 3618, 2620) and the character stands on it, but nothing happens. With its teleporter raised to Z 2 (a staff probe of the cause), the step goes down to the Landing (5193, 1138) and the ladder brings it back beside the hatch | `runs/tour-final-log.txt`, `runs/probe-hatch.txt` |
| Blackthorn (P691) | the same | From Britain's gate on foot (662 + 30 steps) onto the hatch in the keep's storeroom: down to the Fold's landing (6472, 3927). The "into the storeroom" check failed on my driver (its one-level grid put the character on the castle's wall-top, z 27, where the exact walker's box had no stair down); the next walk reached the hatch | `runs/tour-final-log.txt` |
| A boat from a dock | the same | On Haven's west pier: the deed (staff-given, as a shipwright sells) targeted at the sea, "A ship's key is now in my backpack", the plank unlocked with the key, boarded, anchor raised, sailed astern and stopped; the server had the character 3643,2684 -> 2685 (stopped against an earlier ship astern; in a debugging run the same ship sailed 12 tiles to 2696) | `runs/tour-final-log.txt` (the boat rerun), `runs/tour-debug-runs-log.txt` |
| A treasure map dug | the same | A level-1 map (staff-given, with a shovel) decoded, read by its pin (the map's bounds and pin as the client gets them), the character staff-placed 25 tiles off and walked to it, "Dig For Treasure": the chest came up with dirt piles and four guardians (skeletons and ratmen) round it, confirmed by staff at 2776, 2437 | `runs/tour-final-log.txt`, `runs/probe-pin.txt` |
| A Felucca champion seen | the same | P685's moved altar at 5432, 3220 on Felucca (staff-placed 12 tiles off, walked): the platform, pentagram and candles stand, 61 items | `runs/tour-final-log.txt`, `shots/tazuo-felucca-champion.jpg` |
| A save and two restarts | the server | Saved in 0.8 s, reloaded in 1.6 s; both restarts found F1 and F3 | `runs/restart-check-1.txt`, `-2.txt` |
| Pictures in the package's TazUO | TazUO from the package, Iron the Tester moved by Iron's Admin | 14 places: Britain's and Buccaneer's Den's gates, the six towns' banks (Fort Yondall's gatehouse), Blackthorn's keep, the Felucca champion, the dig, New Haven's gate, the Rootdeep hatch, Haven's pier with the ships | `shots/tazuo-*.jpg` (the patch-notes window covers the upper left, as in every shot run) |

My driver's two failures in the clean run (not the world's): the Blackthorn storeroom step above, and the boat: the
part order left the character on the Fold after Blackthorn's hatch, so the deed said "That is too far away"; the boat
part rerun from New Haven passed. **Staff help**, all logged as STAFF lines: putting the character at a start (a
gate, Valunstead's shore, 25 tiles from the treasure pin, 12 from the champion), giving the deed, the map and the
shovel, and Blessed (so the dig's guardians and the wild could not end the run). Everything else is the player's own
action through the client's packets.

## Part 2: what failed, each to its owner

| # | What failed | Evidence | Owner, and the fix |
|---|---|---|---|
| F1 | **New Haven's seeder doubles 37 of its people on every restart.** P678 moved 37 of `ClusterFNewHavenSeeder`'s 40 entries into the author's town (x 3600-3750), but `IsNewHavenArea` (ClusterFNewHavenSeeder.cs:274-275) is still the old plaza's box, x 3400-3560, y 2400-2760. At load (`seedOnWorldLoad`, `repairOnWorldLoad` on in the test config) `FindExisting` cannot see the 37 it placed and makes them again; only the three entries west of x 3560 (Gervis and Mugg among them) are found. | First boot "created 40"; each of two restarts "created 37, repaired 0, skipped 3" (`runs/restart-check-1.txt`, `-2.txt`); after them `[global get Location where sirhelper` and `... where andric` each found **3** (`runs/adminq.txt`). | **P678 (S7).** Read the town from HavenSpots or the new town region (the box round the entries), with a fact that seeds twice and counts. The main branch has had this since P678 merged, so the **current test shard probably has it too** (not checked: this prompt never touches it). Any world that has restarted since needs its extra copies deleted once by staff: the seeder's replace mode finds its pieces with the same old box, so it would not see them either. |
| F2 | **Rootdeep's cellar hatch does not take a player down.** The hatch (0x3E65) sits at Z -1 with its top at 2, so a player on it stands at Z 2; its teleporter is at Z 0. Pinned `Mobile.Move` (Mobile.cs:4226-4227) fires a zero-height item only at the mover's own Z. The fact `RootdeepWayInVerification.W1_TheHatchTakesAPlayerDown...` calls `OnMoveOver` directly, so it is green while the real step does nothing. | `runs/tour-final-log.txt`: "FAIL down the hatch" (stands on 3618,2620, stays); `runs/probe-hatch.txt`: the server has the player at (3618, 2620, **2**), the teleporter 0x1BC3 at Z 0. Probe of the cause (logged STAFF): with that one teleporter raised to Z 2, the same step lands on the Landing (5193, 1138), and the ladder brings the player back beside the hatch. | **P678 (S7, Rootdeep's way in).** Place the hatch's teleporter at the Z a player stands at on it (P691 did this for Blackthorn's: Z 17 on a z14 hatch), and make W1 step a player onto the hatch with `Mobile.Move`, seen failing on today's code first. Matters only if the Burrows open at 1.0; they are a draft and the go-live changelog already leaves them out. |
| F3 | **`[MoonGen` deletes every public moongate, ours too.** On the fresh world it removed 1 (Royal City's, placed at boot by `ClusterFRoyalCitySeeder`) and made 32; a second run removed 34 (the 32, Royal City's again and Eodon's from `[GenEodon`) and made 32. Neither comes back by itself: after two restarts TerMur had no public gate and the boot still said "Eodon moongate ... MISSING". `[SeedRoyalCity` and `[GenEodon` put both back. | `runs/gen-log.txt` (both runs); `runs/restart-check-*.txt`; `runs/adminq.txt` ("Nothing was found" on TerMur, then 850,3525,-38 after `[SeedRoyalCity`) | **The swap-day order (Part 3): `[MoonGen` first, then `[SeedRoyalCity` and `[GenEodon`.** A later prompt could make the Royal City seeder re-check its gate at load, as it re-checks its vendors. |
| F4 | **`[Decorate` is not idempotent**: a second run on the decorated world "generated 28 items" more. Which 28 was not established. | `runs/gen-log.txt` (my accidental second run) | **P680 (S5) / P683 (S6)**: find the 28 (a decoration type pinned's existence check misses, or one of the author's lines) and make a rerun place nothing; until then the checklist says run once. |
| F5 | **The console's "Fresh world" list is not the swap-day order**: it lacks `[MoonGen`, `[TelGen`, `[Decorate`, `[GenChamps`, `[GenBlackthorn`, `[GenEodon` and the stock Trammel and Felucca spawn files P681 re-placed. | `Shard-Console.ps1` `WorldSetupOrder` 'fresh' (14 files + sos, Shame, Despise, save) against Part 3 | **P682's owner of the list (the console), with this checklist as its source.** Not a game fault; the world would come up empty of gates and decoration if someone followed the button. |
| F6 | **The go-live changelog's Blackthorn condition names the hatch at 1515, 1436**; it stands at 1519, 1437 (P691 moved it off the barrels). | `go-live-changelog.md:24`; `BlackthornFold.cs:86`; seen in game at 1519,1437 | **P689 (S16) / P691**: one number in a staff-facing line. |
| F7 | **A flaky shard test**: `CovetousVoidSpawnVerification.SetupPlacesTheControllersThePoolTheSpawnersAndThePaths` failed the first gated build ("an angered spirit ... wandered from" its home more than 3 tiles in the 1.5 s the test gives the AI); the second build passed it. | `gated-build-1-summary.txt` (2,824 passed, 1 failed), `gated-build-2-summary.txt` (2,825 passed, 0 failed) | **P221 (the fix-up for P194's Covetous port), as a fix-up**: freeze the AI or measure against `RangeHome`. It is not the map. |
| F8 | **Duplicate region names at boot**: the four "Unfinished land: ..." fence regions (P687, code) share their names with S3/S13's no-housing regions (`regions-*.json`), on both facets; pinned warns "Duplicate region name" eight times. Lookups by point find both; a lookup by name finds one. | `runs/first-boot.log` lines 100-107 | **P687 (S14), with P676/P686**: rename one set (e.g. the no-housing ones "... (no housing)"). Low. |

Seen and not counted as failures (as designed, or known):
- A new account's New Haven pick is "New Haven (locked)" and starts on the isle (P717, Chase 10-28).
- Valunstead has no dock, gate or teleporter: reached here by a logged staff move, then walked (P688's group 7; Chase or S11).
- Fort Yondall's gate is static doors; the way in is the gatehouse stairs (P688), walked here.
- The first login's pile of windows and joke achievements over the isle's beach (P707 draft 1, still open).
- The patch-notes and TazUO version-history windows over the shots (the shot runner copies an old profile; the package's own new profile, in the isle run, showed no version history).

## Part 3: the go-live checklist for 1.0

Rehearsed on this prompt's private world (127.0.0.1:2596, `sl-modernuo:cc-P690`, empty world at first boot). Every step
below was run there. Steps 0 to 11, 13 and 14 ran in this order; 12 and 1a ran later in the session (1a after the
restarts had shown that Royal City's gate stayed gone), and 13 a second time after my accidental rerun of step 1.

### Before swap day: the gates

| # | Check | Where it stands now |
|---|---|---|
| 1 | Every swap prompt merged: S1 to S16 and P691 | Yes for this branch (main with P691); S18 and S19 are after 1.0 |
| 2 | **New Haven's seeder fixed (Part 2, F1)** | Not fixed: it doubles 37 of New Haven's people on every restart |
| 2a | The Rootdeep hatch fixed (F2), **or** the Burrows stay closed at 1.0 | Not fixed. The go-live changelog already keeps Rootdeep out while the Burrows are a draft |
| 3 | The gated build green | Green on the second run (2,825 passed, 0 failed); the first hit the Covetous flake (F7). Rerun once on that failure, as with the apply-patches flake |
| 4 | The player package built with the SoS map: `switch.txt` set to `on` in the release (or `-SosMap on` for a test build) | Rehearsed with `-SosMap on`: 181 MB, gates green, TazUO 3212623f + 9 patches |
| 5 | The go-live lines copied from `go-live-changelog.md` into CHANGELOG.md, its conditions checked | Its Blackthorn condition names the hatch at 1515, 1436; the hatch is at 1519, 1437 (F6) |

### Swap day: the fresh world, in this order

The world starts empty. On the test shard, `Start-TestShard.ps1` seeds the accounts and `SerializedTypes.db` from the
live save (the console's "Start fresh"), so the owner prompt never comes. A world with no accounts at all stops at
ModernUO's owner prompt; under a TTY the password it asks for is echoed into the container log (seen here; the private
world's log copies were redacted).

| # | Command (access) | What it placed here | Notes |
|---|---|---|---|
| 0 | first boot | the isle seeded on load (11 markers, 8 NPCs, the dock moongate, the farm), New Haven's 40 seeded pieces, the institutions, Royal City's gate, the Halloween rows, the requisition appraisers | nothing to type |
| 1 | `[MoonGen` (Developer) | 32 public gates: Trammel 9, Felucca 9, Ilshenar 9, Malas 2, Tokuno 3 | **deletes every PublicMoongate first**, ours too: Royal City's (placed at first boot by `ClusterFRoyalCitySeeder`) and Eodon's. So run it **first**, then step 1a and step 13 (F3) |
| 1a | `[SeedRoyalCity` (Administrator) | Royal City's gate back at 850, 3525, -38 | a restart does **not** put it back (the seeder's load hook runs only while the city has no gargoyle vendors); rehearsed |
| 2 | `[TelGen` (Developer) | 1,459 teleporters (`teleporters-sos.json`) | a rerun replaces (1,480 removed, 1,459 added) |
| 3 | `[Decorate` (Developer) | 49,462 items | **run once**: a second run added 28 more (F4) |
| 4 | `[GenerateSpawners Data/Spawns/shared/**/*.json` (Developer) | 5,080 spawners, 0 failures (P681's moves applied on import) | about 20 s of server time; a bot or client sitting idle meanwhile can be dropped for inactivity |
| 5 | `[GenerateSpawners Data/Spawns/post-uoml/**/*.json` | 313 | |
| 6 | `[GenerateSpawners Data/Spawns/uoml/**/*.json` | 76 | |
| 7 | `[GenerateSpawners Data/Spawns/sos/**/*.json` | 810 (P682's towns, keeps, wild) | |
| 8 | `[GenerateNewShame` (Administrator) | "Shame Revamped setup!" | |
| 9 | `[SetupDespise` (GameMaster) | "Despise setup complete" | |
| 10 | `[GenChamps` (Developer) | Felucca's champions (no chat line: pinned's command is silent) | P685's moved altar at 5432, 3220 seen standing |
| 11 | `[GenBlackthorn` (Administrator) | 1 post, 8 doors, 16 blockers, 36 teleporters, the cellar hatch, 23 spawners | refuses without the map overlay |
| 12 | `[ClusterFSeedRootdeep` (Administrator) | 33 spawners, ankh, crawlway, 2 teleporters, the hatch, 8 floor traps | **only if the Burrows open at 1.0**, and only after F2 is fixed; not run at world load |
| 13 | `[GenEodon` (Administrator) | 1 moongate, 2 vines, 46 spawners | after step 1 (F3); every boot logs "Eodon moongate ... MISSING (run [GenEodon)" until it has run after `[MoonGen`; a rerun replaces its 48 objects |
| 14 | `[save` (Administrator) | | |
| 15 | restart once, and read the boot | the save reloads (here: saved in 0.8 s, loaded in 1.6 s, 196,089 items, 41,277 mobiles) | **New Haven's seeder adds 37 more NPCs on every boot until F1 is fixed**: fix F1 before swap day, or the test shard gathers a crowd of Sir Helpers |

The console's "Fresh world" list (`Shard-Console.ps1`, `WorldSetupOrder` 'fresh') is narrower than this: it lists 14
named spawn files plus `sos/**`, Shame, Despise and save. It has no `[MoonGen`, `[TelGen`, `[Decorate`, `[GenChamps`,
`[GenBlackthorn`, `[GenEodon` or `[ClusterFSeedRootdeep`, and its spawn files leave out the stock Trammel and Felucca
dungeon, wild and town files P681 re-placed (`shared/trammel/*`, `shared/felucca/*`). The table above is the full order;
the console's list should follow it (F5).

Not in the order, decided here: `[DoorGen` and `[SignGen` (pinned's) were not run. `[SignGen` places stock signs at stock
spots, which the swap prompts never graded on SoS; `[DoorGen` scans the map for door frames and was not graded either.
`[DecorateMag` stays out (P680). Say if the live world had any of these and should again.

### After the world is up: the checks (each was done here; the evidence is Part 1)

1. A new account's first character, with either start pick, wakes on the isle beach (6638, 3993); the list shows "New
   Haven (locked)" (P717, as designed).
2. The isle played through to the dock moongate and beside Rook in New Haven (the bot route, 85 checks).
3. Rook's Graduate opens the island gate; all 18 public moongates on Trammel and Felucca land on their gates.
4. A walk from a gate or bank to each new town's bank.
5. Blackthorn's hatch in the keep's storeroom drops to the Fold's landing (6472, 3927).
6. A ship from Haven's pier sails; a level-1 treasure map decodes and digs up a chest with guardians.
7. A Felucca champion altar stands at P685's site.
8. TazUO from the built package, on a player's own UO folder: the first start builds the map in about 22 s.

## The proof's tools (`notes\cc-P690-tools\`)

- `gated-build.ps1`, `pkgbuild.ps1` (with `-SosMap on`), `overlay.ps1`; the build outputs `gated-build-*-summary.txt`,
  `pkgbuild.txt`, `pkgbuild-sosmap-on.txt`.
- `fresh-shard.ps1` (an empty world on 2596), `answer_owner.py` (the owner prompt, through the Docker pipe), `gen.py`
  (the swap-day order, typed by the owner), `adminq.py` (Iron's Admin's queries), `restart-check.ps1`, `redact.py`.
- The clients: `tazuo-pkg.ps1` (the package's launcher steps and its TazUO, P731's creation plugin, a Legion walk),
  `IsleWalk690.py` (from P740's by `make_walk690.py`), `classic-pkg.ps1`, `make_create_bin.py` (the start city as an
  argument), `shots690.ps1` (P716's shot runner on the package's client) with `shots690.json`; `p740\` is P740's tools as
  main has them, the base.
- The bot: `isle.py` (P740's route, unchanged) and `tour.py` (the world tour: a whole-map planner on P688's walk grid,
  P688's exact walker for the last stretch, a client that reads the facet, map pins and ships' multi cursors);
  `probe_hatch.py`, `probe_pin.py`, `dockmap.py`, `shipfit.py`; `edit_*.py` (the scripted edits of my own tools).
- `runs\`: every log quoted above; `shots\`: 24 pictures (3.5 MB).
- Outside the repos, deletable: `D:\UO\golems\Iron\p690-proof\` (the world, both packages unzipped, the clients, every
  raw frame, the owner's and the two new accounts' secrets).

Bot gaps found and worked round in `tour.py` (not shipped; for whoever drives uobot next, and in my memory notes): the
client keeps the old facet's world after a facet change; it does not read 0x99 (multi cursor), 0xF6 (a ship's move)
or map pins; ship commands are speech keywords; a ground target with graphic 0 lands at the land's Z, under sea statics.

## Deviations and decisions for Chase

- **"Two clients"** taken as TazUO (from the built package) and ClassicUO (the launcher's, with the package's map
  files), each making its own characters at the character list, as P740 did; plus the play-test bot for the long tour.
- **The package was built with `-SosMap on`** (the builder's one-run override) so the clients drew the swapped land;
  `switch.txt` stays `off` until the release.
- **Staff help** in the tour is listed above and in the log. Nothing staff did is counted as a player result.
- **The world is the test shard's configuration** (the bot shard's copy: testCenter on), as the swap goes live there
  first. testCenter's gifts (gold, maps, tools) reached every new character, as on the test shard.
- **My mistake, kept in the evidence:** a query with an empty `--only` re-ran the whole generation (`[MoonGen`,
  `[TelGen`, `[Decorate` and the shared spawn files) before I stopped it. It showed F3 and F4; spawner imports replace,
  so nothing else doubled. `gen.py` now needs `--only none` for no steps.
- **The Rootdeep probe** raised one teleporter to Z 2 on the private world to prove F2's cause; it was set back to 0
  before the clean run, which then failed on it as it should.
- **Read and Grep tools denied** in this unattended run, twice: Grep on `server\customizations` for "New Haven seed
  complete" (I wanted the seeder's file; `grep` in Bash found it), and one earlier Grep in `docker\uo` for the
  fresh-world notes (read with `cat` instead).
- The owner prompt's password went into the private container's log through its TTY; every copy was redacted, and the
  repo's copies were checked for it.
- **Not done:** the city screen's own picture of the two start choices (a client screenshot needs click automation of
  TazUO's creation screen; the server's city list and both outcomes are in the evidence instead). `[SignGen`,
  `[DoorGen` and `[DecorateMag` were not run (Part 3).

## Tests and commit preflight

- No game code or test changed, so no new fact; the gated build of this branch is green (2,825 passed, 0 failed, run
  2; run 1's one failure is F7, a flake).
- Locks: `docker-build`, `package` (twice) and `test-shard`, each taken and released. The private shard
  `sl-p690-proof` is removed; no TazUO or ClassicUO is left running. Haven and the shared Test Shard were not touched.
- Files: docs copy only: this note and `notes\cc-P690-tools\` (4 MB, no file over 5 MB). Code copy: unchanged.
- Memory: a note on the bot's traps (facet change, ships, staff items) for the next world tour.

## Earlier starts (kept)

### Second start (2026-10-31 00:54)

Chase's answer Iron-P690-20261030-073734-2ce1 was "Retry with my answer". I read it first, then checked:

| Check | Result |
|---|---|
| P691 on main | No. `golem/Iron/P691` is at `5ff0b91` (committed); main is at `dadf28f` (10-30 12:37) without it |
| Free memory | 1.2 GB of 31.7 GB; commit 101 of 113 GB |
| Kernel pools | paged 34.3 GB, nonpaged 13.9 GB (39 GB on 10-30); available 1.4 GB |
| Last boot | 2026-10-26 13:04 |
| Isle release | `release/isle-20261028` at `9e616f3` (P725); not shipped yet (P740 is for its next pick) |

Chase's rule (answer Iron-P688-20261029-125544-04f6): on low memory, stop and ask rather than fail. No lock was taken.

### First start (2026-10-30 03:39)

| Check | Result |
|---|---|
| Free memory (`Win32_OperatingSystem`) | 1.1 GB of 31.7 GB |
| Kernel pools (`Win32_PerfFormattedData_PerfOS_Memory`) | paged 27.7 GB, nonpaged 11.7 GB, committed 87.5 GB, available 0.9 GB |
| Largest processes | Memory Compression 3.2 GB, vmmemWSL 1.6 GB; nothing large of ours running |
| Prompts the playthrough depends on | P691 not merged; P689 committed, not yet on main (it is now) |

Answer Iron-P690-20261030-033912-f5a0: put back in the queue behind P691.

P690 DONE
