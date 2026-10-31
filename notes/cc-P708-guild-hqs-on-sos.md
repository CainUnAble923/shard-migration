# cc-P708: the guild and League headquarters move onto the Siege of Sosaria land (Chase's picks)

Iron Golem, 2026-10-31. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P708` (main at the P691 merge). Not committed by me; nothing deployed; the shared Test Shard and Haven
not touched. **Paused at Chase's request** at a clean point: the code builds green and every fact is green. What is left
is in the Continuation section and in `cc-P750-cont-guild-hqs-on-sos.md`. The places are Zigholtul's (Siege of Sosaria
Trammel Map 3.0); the guild rooms in them are ours.

## In plain words

- **Six headquarters now stand on the new land, where you picked.** The League's headquarters is in Valunstead's
  moated keep: the gatehouse rooms, with the great hall behind as its meeting room. The Merchants' counting house is a
  separate building by Valunstead's bank. The Healers are in Fort Whitestone's south wing, the Rangers in the court of
  Fort Viridian, and the Custodians and the Tinkers each have a stone house in Hammerhill. Each has its guildmaster, its
  sign and a travel stop at its door. Game shots: `notes\cc-P708-review\`.
- **Elara stays in New Haven.** The Valunstead headquarters has its own steward, Aldous Penhallow. He sends anyone who
  asks to join to Elara at the New Haven field office. No headquarters is needed to join a guild.
- **The Smiths stay at Serpent's Hold.** Fort Stormhammer's only public floor is a throne hall that holds the sealed
  Sentinels Military Base entrance, so a forge there would have to go upstairs in a bare room.
- **For you:** the halls are still test-shard only (`[ClusterFGuildHalls place` puts them up and takes away anything a
  hall left at its old place). Two things to decide: Valunstead is an island with no gate or dock yet (P688 found it),
  so its two headquarters are reached by boat or spell until something opens it, such as the author's moongate at
  655,397; and whether the Smiths should move upstairs at Stormhammer after all. A short follow-up (P750) finishes the
  Rangers' and two signs' checks in game.

## What changed

### 1. The six moves (`design/guild-halls/halls.json`, generated into `ClusterFGuildHallPlacementData.cs`)

Each site was checked on the SoS land by P281's own hall checks, through a P708 copy of them
(`notes\cc-P708-tools\p281sos`, made by `make_p281sos.py`). The copy differs from P677's in three ways:
- it reads **today's** SoS overlay (`make_sosclient.py`: the pristine SoS base plus today's `trammel.mapops`, so P687's
  boulders, P691 and P741 are in);
- it keeps clear of **our** decoration (`server/data/Decoration`, P680) and the **SoS spawners** (`server/data/Spawns/sos`,
  P682: the new towns' shops and garrisons), not only pinned's;
- its walk climbs **sloped land** as pinned `Movement.Check` does: onto a land tile whose lowest corner is within 2 of
  the start's top, the start's highest corner when it stands on land. P281's step of 3 between average heights cut Fort
  Whitestone's road, which drops 5 a tile down the hill.

| Hall | Was | Now (guildmaster; travel stop; sign) | The room |
|---|---|---|---|
| League | Castle British keep | Valunstead keep, 559,317,20 (new `LeagueSteward`); 564,322,17 on the moat bridge; brass sign 566,321 | the gatehouse's west room, behind the keep's south door; the east room for records; the great hall behind as the meeting room |
| Merchants | a new Guild House in Magincia (failed on SoS: the author's building stands on its plot) | Valunstead, 492,391,20; 499,388,15; sign 498,390 | the counting house in the walled yard north of the bank: crates, desks, bookcases and a display case, unused by P682 |
| Healers | Empath Abbey | Fort Whitestone, 902,1046,32; 890,1058,30 on the gate causeway; sign 893,1056 on the gate tower | the south wing east of the gate, three floors (32, 52, 72) |
| Rangers | Skara Brae (shared) | Fort Viridian, 1003,1004,0; 1015,1003,0 (the author's go point, on the road); sign 1014,1008 | the ruined fort's court, by the east entrance; open ground round it for animals |
| Tinkers | Vesper's Musician's Hall | Hammerhill, 1488,1023,10; 1495,1023,5; sign 1494,1026 | the stone workshop on the west lane, about 30 tiles from P682's tinker |
| Custodians | Britain's bank-side hall (failed on SoS) | Hammerhill, 1560,967,10; 1560,974,5; sign 1563,973 | the stone house north of the bank, its own entrance, about 30 tiles from the Tinkers |

- **Credit.** Each moved hall's building name says it is a place on Zigholtul's Siege of Sosaria map.
- **The League's steward** (`server/customizations/LeagueSteward.cs`): Aldous Penhallow, the League Steward,
  invulnerable. Double-click or "join", "league", "guild" near him: "To join the League or a guild, see Elara Voss at
  the League's field office in New Haven. Nothing here is needed for that." Elara (`LeagueRegistrar`) stays in New Haven.
- **The signs** hang by the building guide's rule (2.5): on the floor tile just outside the door's wall, two tiles along
  from the door, at the wall's base Z less 2; the even art on a south wall, the odd on an east wall (`edit_signs.py`).
  My first placement put each on the wall tile itself, where the wall drew over it: no sign showed in game.
- **Decor packs:** none of the six guilds has one (P265 made Alembic, Smiths and Artificers, and the shared towers,
  which P704 said not to use to make up for room), so none is placed.
- **The old sites** (`ClusterFGuildHallMoves.cs`, new, and `ClusterFGuildHallPlacement.OldSite`): `place` and `clear`
  first take away what a world still has of a moved hall at its old place: its sign (showing again a stock sign it
  hid), an old guild house and its doors, and a guildmaster of the old type within a tile of the old post. On the
  private shard the re-place took the six first-placement signs down and hung them outside (pass 3's log).
- **Every other hall stays** (16 of 18 already passed on SoS in P677; all 18 pass now).

### 2. Fort Stormhammer (the Smiths)

Walked on the SoS land and in game (`renders\stormhammer-*.jpg`, `cc-P708-review\tazuo-stormhammer-*.jpg`):
- **Rooms.** The keep (about 1477-1500, 1288-1312) has one ground-floor hall at Z 2: pillars, a throne dais with red
  curtains, stairs at the north and east corners. Above it, at Z 24, four bare rooms off a central stair; more floors
  at 46, 57 and 68, and corner towers. P682's garrison (four guards) stands at the gate and in the hall.
- **The dungeon entrance.** The author's Sentinels Military Base entrance (1482,1296,2) is **inside the hall**, at its
  north-west doorway. No teleporter runs there today, but it is the dungeon's way in. P704 asked that Stormhammer stay
  separate from it.
- **Forge space.** The ground floor is the only public floor, and it is the throne hall with the dungeon door. The
  forge group (7 by 5 tiles) would fit only in one of the bare Z 24 rooms, up a stair.
- **Travel.** The gate (1488,1320) is walkable from Britain (reached by the walk, the long way round), no gate or dock.
- **Recommendation: stay at Serpent's Hold**, whose hall passes every check on SoS. By the prompt that needs no question
  to Chase. If Chase wants Stormhammer anyway, the Z 24 room over the hall is the place, with the forge pack upstairs.

## Tests

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_guild_hqs_sos.py` (new): (1) the six halls in Chase's towns; (2) each guildmaster and travel stop standable at its Z and dry, the stop under open sky, the sign's tile dry with a wall to hang on; (3) each guildmaster reached on foot from its stop, and the stop joined on foot to the town's bank (Valunstead's island, Hammerhill) or to the Yew Forest Guardpost (the two forts) | main's design file: 3 of 3 fail (`red\red-test-guild-hqs-sos.txt`) | 3 of 3 (`green\test-guild-hqs-sos.txt`) |
| docs `tools/tests/test_s8_spots.py` fact 3: P281's hall checks on SoS now pass **every** hall (P677 allowed Merchants and Custodians to fail) | main's design file: fails with exactly `['custodians', 'merchants']` (`red\red-test-s8-fact3.txt`) | 4 of 4 (`green\test-s8-spots.txt`) |
| code `GuildHallSosMovesVerification` (new): (1) each moved hall in its picked town, League and Merchants in separate buildings, Custodians and Tinkers too, every other hall unmoved, the moves table names exactly the six; (2) the League's steward, not Elara, Elara in New Haven; (3) place takes a moved hall's old sign, old guild house, doors and old guildmaster away and places once, clear takes an old guildmaster too, a same-type guildmaster elsewhere stays; (4) each moved guild keeps a New Haven chapter and a new character joins it with no hall placed | mutants on the builder image (`probe-guild.sh`): main's table and placement code, facts 1-3 fail (`red\red-csharp-main-halls.txt`); main's placement code alone, fact 3 fails: the dry run counts the old sign as "already standing" (`red-csharp-old-placement.txt`); the Healers' chapter moved to Whitestone, fact 4 fails (`red-csharp-chapter-moved.txt`) | 19 of 19 guild hall facts (`green\probe-guildhall.txt`) |
| code `GuildHallPlacementVerification` fact 2: the League's hall is placed with `LeagueSteward` | | in the gated build |

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P708`, detached through `gated-build.ps1`, `docker-build` lock
  taken and released each time): **EXIT=0** twice. The second (`green\gated-build-2-summary.txt`; the full logs are git-ignored) has everything here: 2,835
  tests, 2,829 passed, 6 skipped, 0 failed.
- **A fact that passed by luck:** fact 4 first made its account without setting the password algorithm. It passed in
  the full build only because an earlier fact had set it, and failed alone. It now sets it as `AlembicGuildVerification`
  does.

## Live, on a private shard (127.0.0.1:2596, `test-shard` lock taken and released, container removed)

- **Setup.** `proof-shard.ps1` (P740's) on a copy of the bot world, the map overlay from this branch's patch
  (`overlay.ps1`, the test shard's own `Build-MapOverlay.ps1`), `sl-modernuo:cc-P708`. Shots with P690's runner
  (`shots708.ps1`) and P690's built package TazUO, windows off-screen.
- **Placing.** `[ClusterFGuildHalls place`: 44 things placed, all 18 halls; status shows each guildmaster in and sign up
  (`cc-P708-review\shots-pass1-log.txt`). After the rebuild with the signs rehung, `place` again: "took away the old
  GuildHallSign at (563, 320, 20)" and so on for the six, then the new signs (`shots-pass3-log.txt`).
- **What the shots show** (`cc-P708-review\tazuo-*.jpg`, the Tester's window; the patch-notes and paperdoll windows
  cover the top left, as in every proof run):
  - League: the steward in the gatehouse room; the keep's door and steps (the author's buildings are hued: pink stone,
    purple roofs).
  - Merchants: the guildmaster among the counting house's crates, display case and bookcase; the sign beside the steps.
  - Healers: the guildmaster in the south wing; the sign on the gate tower above the causeway.
  - Tinkers: the guildmaster on the workshop's red brick floor.
  - Custodians: the warden in his office; the sign beside the red door.
  - Rangers: the sign on the court wall by the east entrance, the Tester beside it and the author's cave mouth below.
  - Stormhammer: the gate, the throne hall with a garrison guard, the upper floor.
- **Not yet seen in a shot:** the Rangers' guildmaster and the Tester at Viridian (the court reads as green walls and
  yellow walkways and neither figure shows), and the League's and Tinkers' signs after rehanging. See Continuation.

## Mistakes, and what to trust

- **Signs on the wall tiles.** My first six signs sat on the wall tiles and the walls drew over them. Rehung by the
  guide's rule and rebuilt; four of six are confirmed in shots.
- **The walk's box.** My first reach fact used the points plus 12 tiles and said the keep and Whitestone were cut off.
  Valunstead's keep joins the lower town round the west of the island, and Whitestone's road needed the slope rule. The
  fact now walks a box the size of each place.
- **P677's `check.out.txt`** was rewritten by a red run of fact 3; restored from git.
- **The reply wording.** `place`'s line for a moved hall reads "placed took away the old GuildHallSign ...": the
  removal joins the placed list. Harmless, left for the continuation (listed there).

## Deviations and decisions for Chase

- **Valunstead's access.** Valunstead is the author's island with no dock, gate or teleporter (P688's group 7). Both
  Valunstead headquarters are reached by boat or spell until it is opened (the author's moongate at 655,397 is a
  landmark only today). Joining never needs them. Fallbacks if you prefer: Castle British (League), Magincia
  re-surveyed (Merchants).
- **Fort Viridian is a ruin.** No roofs; its courts and ramparts are the author's ruined fort. It fits a field post with
  open ground for animals, but there is no indoor room. Skara Brae is the fallback if that reads wrong.
- **Smiths:** stay at Serpent's Hold (above). Say if you want the Stormhammer upper floor instead.
- **A problem found, not fixed (not P708's):** the Smiths' forge decor at Serpent's Hold is refused once the guild house
  stands ("forge 0x0FB1 at 3032,3444,22: an impassable GuildHallBuilding at z 15"), yet `place` still reports it placed.
  Seen on both placements.
- **No `ask`:** nothing needed Chase mid-task.

## Continuation

Done: parts 1 (the six moves, the steward, the old-site clearing), 2 (the Stormhammer survey), the facts (seen failing,
green), the CHANGELOG line (`2026.10.31`, Staff) and VERSION, two green gated builds, the private-shard placement and
most shots. Nothing is mid-flight: the private shard is removed and both locks released.

Left (P750, `D:\UO\cc-prompts\queue\cc-P750-cont-guild-hqs-on-sos.md`):
1. Viridian in game: find why neither the Tester nor the Rangers' guildmaster shows at 1000-1003,1004-1006 (the map
   says open sky there), and move the post into a court that reads clearly if needed (the open court at about 991-1004,
   977-986 is one).
2. Confirm the League's (566,321) and Tinkers' (1494,1026) rehung signs in a shot; adjust if hidden.
3. `place`'s reply: a moved hall's removals on their own line ("took away from its old site ..."), keeping fact 3's
   "would take away" check.
4. Gated build, the final shots, notes.

## Files

- **Code copy:**
  - `design/guild-halls/halls.json`; `server/customizations/ClusterFGuildHallPlacementData.cs` and
    `server/tests/Misc/GuildHallPlacementDesignCopy.cs` (generated by `p281sos\gen.py`);
  - `server/customizations/ClusterFGuildHallMoves.cs` (new), `LeagueSteward.cs` (new), `ClusterFGuildHallPlacement.cs`
    (`OldSite`, place and clear);
  - `server/tests/Misc/GuildHallSosMovesVerification.cs` (new), `GuildHallPlacementVerification.cs` (fact 2);
  - `CHANGELOG.md` (2026.10.31, Staff), `VERSION`.
- **Docs copy:**
  - `tools/tests/test_guild_hqs_sos.py` (new), `tools/tests/test_s8_spots.py` (fact 3);
  - `notes/cc-P708-tools/`: `make_sosclient.py`, `make_p281sos.py` and the `p281sos` copy, `render_site.py`, `survey.py`,
    `probe_tiles.py`, `gap.py`, the `edit_*.py` scripts, `make_shots.py` and `shots708*.json`, `shots708.ps1`,
    `proof-shard.ps1`, `overlay.ps1`, `gated-build.ps1`, `probe-guild.sh`, `old-posts.json`, `renders/`, `out/`, `red/`,
    `green/`;
  - `notes/cc-P708-review/`: 16 TazUO shots and the three shot logs.
- **Outside the repos:** `D:\UO\golems\Iron\p708-work\` (the SoS client folder, hard links plus three rebuilt map files)
  and `D:\UO\golems\Iron\p708-proof\` (the private shard's copy, overlay and all shots). Both can be deleted.

P708 PAUSED
