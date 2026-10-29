# cc-P688: the walk between places, and the bot's routes (SoS swap S15)

Iron Golem, 2026-10-29. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P688` (main at the P686 merge). Not committed, nothing deployed. **Stopped before the end** (last
section): one proof was cut off by the PC running out of memory, and the bot run is not green yet.

## In plain words

- **Every town on the new map can be walked to from its neighbours, except the islands.** I walked the whole map from
  every bank, public moongate and dock, the way the server moves a player. There are 8 groups. One group holds the
  mainland: Britain, Yew, Minoc, Vesper, Trinsic, Buccaneer's Den, Serpent's Hold, the author's new towns, and the Lost
  Lands through the stock dungeon teleporters. The other groups are Moonglow, Magincia and Nujel'm (the author joined
  them into one land), Jhelom, Skara Brae, New Haven, Valunstead, the Sea Market and Wind. Each of those is an island,
  or (Wind) reached by stock's magic teleporter. No gap needs clearing.
- **The overnight bot was standing on the old map.** Its private shard never loaded the new map files, so every night
  since the swap code merged it walked EA's old Britannia under the new code. It now builds and loads the same map the
  test shard reads. One check (T-039, "pointed at the board") also measured from the old New Haven; it now measures
  from the new board.
- **New characters on the bot's shard now wake on the tutorial isle**, because the isle is ready in its world. Three
  checks (T-039, P64-1, P64-2) expect them to start in New Haven, so they fail.
- **For you:** two choices on the Golem card. Shall I rerun the bot-point check the PC's low memory cut off? And should
  the bot's New Haven checks pick the New Haven start at character creation? Nothing to deploy.

## 1. The walk between places (the reachability table)

**How.** Two steps, both pinned's `Movement.cs` reduced to the map files (playbook section 6):
- `notes\cc-P688-tools\walkgrid.py`: the whole SoS map at once, one standing level a tile.
  - A step goes from a tile's GetStartZ top plus 2 to the next tile's low corner or itemTop (Movement.cs:265, :346,
    :437).
  - Going down has no limit, so many steps are one way. A player's diagonal needs both sides (:146-151).
  - Surfaces chain upward from the land within 16. Over water or rock they start from the lowest surface.
  - The shipped Trammel teleporters (`teleporters-sos.json`) are one-way joins.
  - 1,247 rounds of labelling; 2,634 one-way joins; 343 teleporter joins.
- `exact.py`: the same rules step by step, every level of a tile kept apart, the candidate closest in Z. One level a
  tile cannot follow a walker up one stack of floors and down another. So `verify.py` walks exactly from every place
  over 150 tiles around it, and back from any other group's ground it reaches. Groups joined both ways are merged.
  - **Papua's bank** (a z14 floor on z13 logs over the dirt) reaches Papua's docks out its door. The one-level
    survey cut it off the same way on stock Trammel.
  - **Fort Yondall**'s gate is two **static** metal doors (0x06C5, 0x06C7 at 3386-3387,382), which no one can open.
    But its gatehouse stairs climb to a z20 walkway and down outside, so the bank reaches the mainland and back.

**The table** (`out\table-groups.csv`; the places in `out\places.csv`; the exact walks in `out\exact.csv`):

| Group | Places (bank, moongate, dock) | Why apart |
|---|---|---|
| 1 | Britain (2 banks), Buccaneer's Den, Delucia, Minoc, Serpent's Hold, Trinsic (2), Vesper, Yew, Elmhaven, Hammerhill, Kameron Kove, Kettleburg, Papua, Fort Yondall; gates Britain, Yew, Minoc, Trinsic, Buccaneer's Den (Felucca); docks Buccaneer's Den, Papua, Skara Brae East, Trinsic East, Island I | the mainland; the Lost Lands join it through stock's dungeon teleporters, both ways |
| 2 | Magincia, Moonglow, Nujel'm banks; Moonglow, Magincia gates; their three docks | one land of the author's (stock: three islands) |
| 3 | Jhelom bank, gate, East Docks | island, as stock |
| 4 | New Haven bank, gate, Haven Docks | Haven Island, as stock |
| 5 | Skara Brae bank, gate, West Docks | island, as stock (its East Docks are on the mainland side) |
| 6 | Sea Market bank (4551,2323) | the floating market, by boat, as stock |
| 7 | Valunstead bank (482,430) | the author's island (60,230 tiles, 234-655 by 180-499): no dock, gate or teleporter |
| 8 | Wind bank | stock: entered by `wind.cfg`'s SkillTeleporter at 1361,883 (Magery 71.5), out by walking |

**What changed from stock.** Buccaneer's Den and Serpent's Hold can be walked to from the mainland: the exact walk
from each bank leaves its box (`out\verify.txt`). On Felucca that makes the pirate town a walk away, not a sail.
Moonglow, Magincia and Nujel'm are one land.

**Fixes for the owning prompts.** None blocks a walk.
- *S11 (P684, docks), or Chase:* Valunstead has a bank, people (P682) and a town region, but no way in except a boat
  or a spell. The author's go-menu gives it no dock. A dock point or a moongate is a choice for later, not a gap.
- *S13 (P686, Felucca):* say whether Buccaneer's Den being on the mainland matters to Felucca's design.
- *S10 or S5 (Fort Yondall's owner):* the fort's static doors could become real doors (a `trammel.mapops` removal and a
  decoration door). It is walkable today by the stairs, so this is looks, not access.

## 2. The bot's points

`notes\cc-P688-tools\bot_points.py` reads every fixed point from the bot's own files:
- `checks_p224_guilds.py`: the two guildmasters and the hunting yard;
- `checks_p224_vbuild.py`: the square and the work box;
- `checks_p224_mule.py` and `checks_p224_thieves.py`: Despise, Shame, the Burrows and the four champion altars
  (P685 kept all four);
- `checks_p224_rootdeep.py`: the Vault's points;
- T-039's board.

It also reads P732's isle route (`notes\cc-P732-tools\isle.py`, main's New Haven) and HavenSpots. It checks each point
is standable on SoS with the shipped `trammel.mapops` applied, that the points one check walks between share a walk
area, and that T-039 measures from `HavenSpots.QuestBoard`.

**Found and fixed (code copy):**
- `tools\playtest-bot\uobot\checks.py` T-039: it measured the new character's distance from stock New Haven's board
  (3502,2573). It now measures from 3633,2585 (HavenSpots.QuestBoard, P678).
- **The scratch shard read EA's Trammel.** Its Configuration copy lists `sl-map-overlay` first, but
  `docker-compose.bot.yml` never mounted it, so the server fell through to the client data's old Trammel. That held
  for every nightly since P675 merged, so the 10-29 01:30 run was the swap code on the stock land.
  - `docker-compose.bot.yml` now mounts `${CLIENT_DATA_OVERLAY}` read-only.
  - Before the shard starts, `Run-OvernightPlaytests.ps1` builds it into `BotRoot\sl-map-overlay`: the SoS base files
    plus the code under test's `trammel.mapops`, as `Start-TestShard.ps1` does.
  - It refuses to run when the build fails or the overlay is not first in `dataDirectories`.

**The P289 tutorial route** (`notes\cc-P289-tools\playthrough.py`) walks the old New Haven core. The core moved to the
isle (P662-P664). Its successor is the isle route, whose newest main copy (P732) already uses SoS New Haven and ran
0 failed on main (P732 notes). So nothing there needed moving.

## 3. The bot run on a private world

The runner itself reads the real repo's test world and Configuration, another desk. So
`notes\cc-P688-tools\bot-run.ps1` does what the fixed runner does, from this desk:
- copies the nightly's own world and Configuration (`D:\UO\bot-shard`, read only) to `D:\UO\golems\Iron\p688-work\bot`;
- writes Iron's TestAccountWipe request (a new slbot-admin password, only in `p688-work\bot\secrets.json`);
- builds the SoS overlay and runs `sl-modernuo:cc-P688` as `sl-p688-bot` on 127.0.0.1:2595 only;
- runs `uobot.run` (all checks, 1 run, no soak) and `uobot.report`.

`botrun.py` points uobot at the tool-trials client data for Cliloc. The `test-shard` lock was held from 12:08 to
12:55; the container is removed.

**Result, 12:09-12:54: 45 pass, 14 fail, 2 could not run** (`p688-work\bot\run\report.md`). Last night: 43 pass,
12 fail, 2 flaky, 4 could not run. **Not green.** Against last night:
- **Now pass:** P70-2, P70-3, P70-5, P70-10 (the mule modules), P171-1, P119-1.
- **Still fail, as every night before the swap:** P62-7, P141-2, P141-3, P142-3, P142-5, P175-2, P175-3, P70-11.
  P100-6 cannot run on a scratch shard. P142-1 now reaches Despise and fails a steal roll instead of the move.
- **New fails:**
  - **T-039, P64-1, P64-2:** the new character starts at 6638,3993, the isle's beach. `TutorialStart` sends creation's
    city 0 (the isle) there whenever `TutorialWorld.IsleReady()`. The bot always asks for city 0. Last night's
    test-world copy had no ready isle, so characters started in New Haven. The world copy the bot gets this time had
    one. On swap day the world is fresh and seeded, so these three will fail every night until the bot asks for the
    New Haven city (index 1, "The Bountiful Harvest Inn") where a check means New Haven. That changes what those checks
    test (a skipped tutorial, not a trainee), so it is Chase's call. Asked.
  - **P121-2, P129-1, P140-1:** creature fights (the poison wording within 45 s, a GargishOutcast and a BurrowScamp not
    killed). They were PASS or FLAKY last night; with one run each they read as flaky, not as the map.

## Tests

| Fact | Red | Green |
|---|---|---|
| docs `tools/tests/test_sos_walk.py` 1: the step rule on made-up grids | `red-test-rules.txt` (P678's stand-to-stand rule fails the land hill); `red-test-rules-diagonal.txt` (one-side diagonal) | `green-test-rules.txt` |
| 2: every bot point on the patched land | **not run**: the red run was stopped by the harness for low memory (below) | not run |
| 3: the table | `red-test-table.txt` (a table with Fort Yondall alone) | `green-test-table.txt` |
| 4: the exact walk at Papua's door and Fort Yondall's stairs; the static gate blocks | `red-test-exact.txt` (step measured from the walker's z) | 1 of 1 |
| code `tools/playtest-bot/tests/test_overnight.py` MapOverlay, 2 facts | `red-test-overnight-overlay.txt` | `green-test-overnight.txt`: 29 of 30; the other, the installer's dry run, fails because "SL overnight play tests" is registered on this PC (schtasks finds it), not this change |

- The bot's own `test_bot.py`: 12 of 12 pass.
- **Gated build** (`sl-modernuo:cc-P688`, 12:00, `docker-build` lock): 2,799 tests, 2,793 passed, 6 skipped, 0
  failed (`gated-build.log`). This prompt changes no server code.

## Where it stopped, and how to finish

1. **The bot-point proof.** At about 12:45 Claude Code stopped `bot_points.py`'s red run (and two wait loops) because
   Windows was out of memory. Windows had 0.5 to 4.6 GB free all day; its kernel pools held about 32 GB. The note
   said not to restart it unasked. To finish:
   - red: `set P688_UOBOT=<the pre-fix uobot copy>` (the session scratchpad's `pristine-uobot`, or `git show HEAD:` of
     `checks.py` into a folder). Then run `python -P notes\cc-P688-tools\bot_points.py
     D:\UO\golems\Iron\ShatteredLegacy D:\UO\golems\Iron\p688-work\patched > notes\cc-P688-tools\red-bot-points.txt`.
     T-039 must be BAD.
   - green: the same without `P688_UOBOT`, into `green-bot-points.txt`, exit 0. The first run builds the patched
     grid (about 15 min, about 2 GB) and caches it in `%TEMP%`.
2. **The isle start** (Chase's answer). If yes: `uobot/run.py` `fresh()` (or the three checks) asks for city 1. Then
   rerun `bot-run.ps1 -Only T-039,P64-1,P64-2` under the `test-shard` lock.

## Chase's decisions applied

- **A fresh test world on swap day:** no migration was planned here. The isle-start finding above comes from it: a
  fresh world has the isle ready.

## Files

- Code copy:
  - `tools/playtest-bot/uobot/checks.py` (T-039);
  - `tools/playtest-bot/docker-compose.bot.yml` and `Run-OvernightPlaytests.ps1` (the map overlay);
  - `tools/playtest-bot/tests/test_overnight.py` (MapOverlay).
- Docs copy:
  - `tools/tests/test_sos_walk.py` (new);
  - `notes\cc-P688-tools\`: `walkgrid.py`, `exact.py`, `verify.py`, `bot_points.py`, `bot-run.ps1`, `botrun.py`,
    `gated-build.ps1`, `mutants\`, `out\` (places, groups, the table, exact walks), and the red and green outputs.
- Outside the repos: `D:\UO\golems\Iron\p688-work\` (the SoS base and patched copies, the private bot world, its
  secrets and report) and `%TEMP%\p688-walkgrid*.npz` (the grid caches) can be deleted once this is finished.

P688 STOPPED: asked Chase (Iron-P688-20261029-125544-04f6)
