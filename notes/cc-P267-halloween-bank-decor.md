# cc-P267: Halloween decorations at the shard's main banks, on a date switch

Builder: the Gold Golem (Claude, Fable), 2026-10-20 to 2026-10-21, on the Gold PC (STEPHS-DESKTOP), branch
`golem/Gold/P267` in both repos. Pinned is `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`;
every pinned citation below is at that commit. Image `sl-modernuo:cc-P267`. Nothing has run against any world but the
throwaway test shard on this PC.

## 1. Ready for Chase: the checklist

The decor is **stock art only** (see section 2 for why), so **no player package is needed for it to show**. The
server deploy alone puts it up on October 24.

1. **Deploy the server** from main once this branch is merged: the usual live restart on the `cc-P267` build (or the
   next good image). On the first start the shard writes three settings into live's `modernuo.json`:
   `clusterf.seasonal.halloween.start` = `10-24`, `clusterf.seasonal.halloween.end` = `11-02`,
   `clusterf.seasonal.halloween.automatic` = `True`. Nothing is placed until the shard's local date (America/Chicago)
   reaches the start.
2. **Confirm the switch date.** `[ClusterFHalloweenDecor status` says the local date, the window and what is up. To
   move the dates, edit the two settings (`MM-DD`) and restart; a value that is not `MM-DD` falls back to the default
   and says so on the console.
3. **To see it before the 24th**, on the test shard first: `[ClusterFHalloweenDecor preview` (lists, changes nothing),
   `[ClusterFHalloweenDecor place` (puts it up now; it says it is outside the dates), `[ClusterFHalloweenDecor clear`
   (takes down exactly what it placed). A bank key or facet name limits each: `place luna`, `clear Felucca`. On the
   live shard a `place` before the 24th stays up until `clear` or until the season ends after November 2.
4. **Walk a few banks in the client and say what to move** (section 6 lists what I could not check without a client).
   The previews are `notes\art\halloween-banks\<bank>.jpg`; the row table with a reason per piece is
   `notes\cc-P267-tools\validate.out.txt`. Moving a piece is a change to `placement.json` (or a rule in `gen.py`),
   `validate.py`, `gen_layout.py`, rebuild.
5. **Player package: not needed for this.** Build and publish it only if you also want the community Halloween art
   (section 2: it is not on this PC); that is a follow-up prompt on the game PC.
6. **After November 2** nothing to do: the hourly check takes it down by itself, by serial, and the save remembers
   what was placed across restarts.

## 2. What is in, what is not, and why

**In:**
- **21 bank sets, 316 pieces**, as data (`ClusterFHalloweenDecorLayout.cs`, generated): the ten banks the prompt
  named (New Haven, Britain west, Moonglow, Trinsic, Vesper, Minoc, Yew, Skara Brae, Jhelom on Trammel; Luna on
  Malas), plus Umbra (Malas), Zento (Tokuno), the Royal City (Ter Mur), and the Felucca twins of the eight Britannia
  towns (same buildings on map0, every tile re-checked there). Section 3 has the table and the banks left out.
- **The switch**, built once to be shared (`ClusterFSeasonalSwitch.cs`): `clusterf.seasonal.<name>.start` / `.end`
  (`MM-DD`, inclusive, may wrap the year), `.automatic`, an hourly check that acts only when the season changes, the
  state and the **serials it placed** saved with the world. P266's winter decor is meant to use the same class with
  `name = winter`; P34's `ClusterFWinterDecor` keeps its own older copy until P266 moves it (not touched here).
- **Staff commands** `[ClusterFHalloweenDecor status | preview | place | clear [bank|facet] [dryrun]` (Administrator,
  `[ShardCommand]` WorldSetup / Skips / TestFirst), and the same verbs on the server console as `halloween ...`
  (the test shard runs with a tty; used for the client-free proof in section 5).
- Tests (section 4), previews (section 3), a CHANGELOG line, `docker\uo\COMMANDS.md` row, `VERSION` 2026.10.20.17.

**Not in: the MrRiots Halloween art (prompt part 1), and this is the one part of the prompt I could not do here.**
- `D:\UO\third-party` on this PC holds only `code\` (empty). `ART-LIBRARY.md`, `mrriots-halloween-2023`,
  `mrriots-halloween-2024` and `training-dummy-pinata` are on the game PC only (memory note from P201: "ART-LIBRARY.md
  ... still absent on this PC"). The game PC answers ping but shares none of its folders (`\\chases-tower\D$` and
  friends: access denied / not found), and Tailscale's CLI is bound to another account here.
- servuo.dev lists "[MrRiots] Halloween Art 2024" (resource 2373, author `members/mrriots.9001`) and DRC1K's "Spooky
  Graveyard" (2517, out by the prompt), but the archive shows **"No permission to download"** without a member login,
  which I do not have, and nothing on it matches a 2023 Halloween set or a pinata. So I could neither read the
  library's tag legend nor get the pixels.
- **What I did instead:** the whole feature on stock art, which every client already has, so it needs no package and
  cannot slip past October 30 on a publish. The community pieces (floating candles, bone furniture, the Ouija board,
  the pinata) are an add-on: P34's pipeline (`notes\cc-P34-tools\convert_art.py`, `registry_rows.py`,
  `anchor-art-frames.py --keep-geometry --black-transparent`) registers them in an hour on the game PC, and this
  seeder takes new rows with new IDs without a code change (a row is key, bank, facet, x, y, z, item ID, name).
  **Decision for Chase:** queue that as a follow-up on a game-PC Golem (Iron or Bronze), or let this ship as is.
- Nothing from `drc1k-uoassets`, nothing from `code\great-pumpkin`, no boss, no currency, no mechanics.

## 3. The banks and the placement

### 3.1 How a template is made (`notes\cc-P267-tools\`, read-only map tools; `bankbase.py` is the loader)

The server's own client files (`client-data\classic-client-7.0.117.0`: land, statics, tiledata for all six facets
through `scripts\mapbuild\uofiles.py`) and pinned's data decide everything; nothing is placed by eye.

- **The building:** a flood from the banker's spawner tile (pinned `Data\Spawns\shared` and `post-uoml` Vendors.json)
  over floor tiles at the banker's z (pinned `GetTopSurfaceZ` within 2, nothing impassable, `CanFit`'s test), under a
  roof, stopping at doors. Zento's bank is an open stall on the market deck (no roof; the deck's edge and the stall
  pieces stand in for walls); Umbra's and Yew's floods are kept to a radius (7) because their arches and open courts
  join the neighbours' rooms.
- **Protected, never used:** the door tiles pinned `DoorGenerator` places (its frame lists and its two-apart /
  three-apart scan, with its `CanFit` refusal: without that a continuous wall of frame-listed pieces reads as a row of
  doors, which my first run did) and their swing tiles (`BaseDoor.GetOffset`), two tiles before and behind every
  doorway; door statics (Ter Mur, Tokuno) and their neighbours; every spawner in the box with its home range (capped
  at 2) and ring; every pinned Decoration cfg item in the box (the folders `Decorate.cs:37-42` loads per facet); every
  teleporter end (`Data\teleporters.json`: none fell in any bank's box) and its neighbours; **the shortest walk from
  every door to every banker over the floor, and its neighbours** (the "banker paths").
- **Modes and rules:**
  - `outside`: a ground tile touching the outer wall **south or east of it** (the faces the client draws; a piece
    north or west of a wall is drawn first and hidden behind it, P34's wall-art rule), surface within 2 of the floor,
    nothing in the way; a street tile only at the wall's foot, never free-standing; an impassable piece (carved
    pumpkin, cauldron, scarecrow, gravestone) only with three open orthogonal sides and never on a street tile.
    Pumpkins, gourds, hay, bones and skulls, 6 to 10 a bank with at least two tiles between pieces; two lanterns flank
    each door two tiles along the wall; one centrepiece at a convex corner on grass or dirt.
  - `corner`: an inner corner of the hall (walls on two sides): a cobweb, the variant for that corner (0x0EE3 NW,
    0x0EE4 NE, 0x0EE5 SE, 0x0EE6 SW; checked on a render of Britain's hall, `notes\art\halloween-banks` is after the
    fix). At most six a bank, three tiles apart.
  - `indoor`: a floor tile against an inner wall, out of the banker walk: bones, a skull, a small web, all passable.
  - `table`: a counter or table top (a Surface + Impassable static at the floor z, height 4 or more, under the roof):
    a skull with a candle, a candle, a small pumpkin, at the static's top z.
- `validate.py` re-checks every row from `placement.json` with the protected set rebuilt from the same sources and
  exits 1 on any failure; `gen_layout.py` refuses to write the C# while it fails. 316 rows, 0 failing.
- One `random.Random` per bank, seeded from its key (a Felucca twin seeds from the Trammel key, so the twins match
  where the buildings do); a rerun is the same table.

### 3.2 The banks

| key | bank | facet | floor z | bankers (pinned spawn) | rows | outside / corner / indoor / table |
|---|---|---|---|---|---|---|
| new-haven | New Haven | Trammel | 20 | 3484,2570, 3484,2576 | 17 | 6 / 6 / 5 / 0 |
| britain | Britain (west bank) | Trammel | 0 | 1425,1690 | 14 | 8 / 2 / 2 / 2 |
| moonglow | Moonglow | Trammel | 0 | 4471,1156 | 22 | 6 / 6 / 5 / 5 |
| trinsic | Trinsic | Trammel | 10 | 1897,2684 | 23 | 8 / 5 / 5 / 5 |
| vesper | Vesper | Trammel | 0 | 2881,684 | 13 | 9 / 0 / 2 / 2 |
| minoc | Minoc | Trammel | 0 | 2503,552 | 18 | 8 / 5 / 5 / 0 |
| yew | Yew | Trammel | 0 | 652,820 | 6 | 3 / 0 / 3 / 0 |
| skara-brae | Skara Brae | Trammel | 0 | 587,2146 | 14 | 8 / 3 / 2 / 1 |
| jhelom | Jhelom | Trammel | 0 | 1317,3773 | 15 | 8 / 3 / 2 / 2 |
| luna | Luna | Malas | -50 | 989,520 | 10 | 6 / 0 / 2 / 2 |
| umbra | Umbra | Malas | -85 | 2048,1343 | 10 | 6 / 1 / 2 / 1 |
| zento | Zento | Tokuno | 25 | 729,1249 | 10 | 10 / 0 / 0 / 0 |
| royal-city | Royal City | TerMur | -20 | 833,3439, 843,3439 | 19 | 6 / 6 / 5 / 2 |
| britain-fel | Britain (west bank) (Felucca) | Felucca | 0 | 1425,1690 | 14 | 8 / 2 / 2 / 2 |
| moonglow-fel | Moonglow (Felucca) | Felucca | 0 | 4471,1156 | 22 | 6 / 6 / 5 / 5 |
| trinsic-fel | Trinsic (Felucca) | Felucca | 10 | 1897,2684 | 23 | 8 / 5 / 5 / 5 |
| vesper-fel | Vesper (Felucca) | Felucca | 0 | 2881,684 | 13 | 9 / 0 / 2 / 2 |
| minoc-fel | Minoc (Felucca) | Felucca | 0 | 2503,552 | 18 | 8 / 5 / 5 / 0 |
| yew-fel | Yew (Felucca) | Felucca | 0 | 652,820 | 6 | 3 / 0 / 3 / 0 |
| skara-brae-fel | Skara Brae (Felucca) | Felucca | 0 | 587,2146 | 14 | 8 / 3 / 2 / 1 |
| jhelom-fel | Jhelom (Felucca) | Felucca | 0 | 1317,3773 | 15 | 8 / 3 / 2 / 2 |

Yew is thin (6) because its bank is a pair of small rooms off the big court; the court itself belongs to the inn and
the shops (the flood is kept to radius 7, else the inn's bedrooms got pumpkins). Vesper and Luna have no inner corner
that is not a door approach or a banker walk, so no cobwebs there.

**Banks with a pinned banker spawner that got nothing**, and why (every banker spawner in `shared` + `post-uoml`,
counted: 52 entries, 29 of them in the 21 sets above):
- Britain east (1650,1608 z20, both facets), Trinsic south (1813,2825, both): second banks of towns already done.
- Buccaneer's Den (2731,2192), Serpent's Hold (2880,3472), Nujel'm (3764,1317), Magincia (3734,2149, ruined since
  ML), Papua (5275,3977), Delucia (5669,3131), Wind (5347,76), Ocllo (3695,2511, Felucca), and 4551,2323 (both
  facets, post-uoml): not main banks of the shard's towns; the generator takes a new one as one line in `gen.py`
  (key, name, facet, z, bankers) if Chase wants any.
- Ilshenar: no town bank (Gargoyle City's two bankers at 854,680 and 855,603 z-40, Mistas 1610,556, two gypsy
  bankers, two banker camps). Left out as "no main bank"; same one-line addition if wanted.
- Felucca New Haven: pinned spawns no banker there.

### 3.3 The pieces (stock art, every ID checked for art and tiledata on 7.0.117)

| what | IDs | count | notes |
|---|---|---|---|
| pumpkins, gourd | 0x0C6A, 0x0C6B, 0x0C6C, 0x0C64 | 73 | passable |
| carved pumpkins (lit) | 0x4691, 0x4695 | 17 | pinned `HalloweenPumpkin.cs` uses these; Impassable, height 5, so only off the street with three open sides |
| lanterns | 0x0A22 | 39 | pinned `Lantern`'s lit art; two per door, four at Zento |
| hay | 0x0F34, 0x0F35 | 23 | |
| bones, skulls, piles | 0x0ECA, 0x0ECB, 0x0ECD, 0x0ECE, 0x0ED0, 0x1ADD, 0x1AE1, 0x1AE3 | 55 | passable variants only |
| cobwebs | 0x0EE3-0x0EE6 | 61 | one per inner corner, by corner |
| small webs | 0x10D2, 0x10D4 | 24 | indoor, against walls |
| skull with a candle, candle | 0x1854, 0x1858, 0x0A0F | 24 | counters (pinned `CandleSkull`'s lit IDs, `Candle`'s lit ID) |
| centrepieces | cauldron 0x0974, scarecrow 0x1E34/0x1E35, gravestone 0x0ED5/0x0EDB | in the counts above | one per bank at most, at a convex corner off the road |

Total 316. Nothing animates but the carved pumpkins (OSI's own frames). No hues.

### 3.4 Previews

`notes\art\halloween-banks\<key>.jpg`, one per bank set (21), drawn from the map files with the decor in: the
client's own view, roofs and upper walls left out so the inside shows, a red ring on an outside piece, a blue ring
on an inside one. The question for Chase on each: anything in the way, anything that looks wrong, anything to add.

## 4. Tests (`server\tests\Misc\HalloweenDecorVerification.cs`, 7 facts plus a 12-case theory)

1. `ThePlacementTableLoadsAndStaysOffBankersAndTeleporters`: 316 rows, 21 banks, unique keys, no item twice on a facet
   tile, every row's bank listed on the same facet, every facet a named map, every ID one of the stock pieces, no row
   on or beside a banker's tile, none on a teleporter tile in a bank box; the ten named banks are there with rows.
2. `TheSeasonWindowIsInclusiveAndMayWrapTheYear` (theory): 10-24 to 11-02 in and out at both ends; 12-01 to 01-06
   across the year end. `ABadDateSettingFallsBackToTheDefaultAndSaysSo`: a value that is not `MM-DD` (or `02-30`)
   keeps the default for that end and returns the console line naming the key.
3. `TheAutomaticCheckActsOnlyWhenTheSeasonChanges`: a world first seen on October 1 gets nothing; a staff place on
   the 10th stands; October 24 brings it up without doubling; a staff clear on the 28th stands; November 2 23:30 still
   up, November 3 00:30 down; a world first seen on October 30 is brought up; with the window set to 10-01 to 10-05
   the same October 30 is out of season and October 3 next year is in.
4. `PlaceTwicePlacesOnceAndClearRemovesExactlyTheDecorBySerial`: preview and clear dryrun change the item count by
   0; place twice gives 316 items, each at its row with its art, bank, not movable, no decay, its serial in the
   saved set; clear twice gives 0 and an empty set, and a gold pile and a same-art lookalike on the first row's tile
   stay; place after clear restores the same keys. `ABankOrFacetFilterPlacesAndClearsOnlyThatPart`: `luna`, then
   `Trammel`, then `clear Trammel` leaves Luna's; an unknown name is refused.
5. `TheDecorAndTheStateSurviveARestart`: the item round-trips key and bank; the season comes in, the state (last
   state and 316 serials) is written, wiped and read back, the placed items resolve from the reloaded serials; the
   in-season check and a second place add nothing; a deleted item's serial is dropped quietly; a stray HalloweenDecor
   the list does not know is swept by the season's end and reported; the end of the season after the "restart"
   removes everything by the reloaded serials; each last-state value round-trips.
6. `TheSettingKeysAreTheOnesThePromptNames`: `clusterf.seasonal.halloween.start`, `.end`, `.automatic`, defaults
   `10-24` and `11-02`, registered as `All["halloween"]`.

Runs through `docker\uo\build.sh`:

| Run | Result |
|---|---|
| tests-only, first | 2 xUnit analyzer errors in my test (xUnit2029, `Assert.Empty` on a filtered collection); fixed to a count |
| tests-only, second | **1662 tests, 1661 passed, 1 failed**: `LootBoxFanfareVerification.ContentsAreRolledAtEarn...`, the known flake (cc-P100, cc-P145, cc-P194: two identical stacks rolled and merged, "60 x Bandage, 60 x Bandage" in its output); all 19 Halloween results passed |
| full build, `docker/uo/build.sh -t sl-modernuo:cc-P267` | **1662 tests: 1658 passed, 4 skipped (pinned's own skips), 0 failed** (the flake did not recur); image `sl-modernuo:cc-P267` = `70e5c2cf4d46`; `latest` untouched |
| **red**, `notes\cc-P267-tools\breaks.py apply` (four breaks at once) | **1662 tests: 1651 passed, 7 failed**, break by break below. A first red run had a weaker clear break (the item untracked but left alive): the second clear's stray sweep removed it and fact 4 stayed green, which is the safety net working, not the gate; the break was made to keep the item tracked and the run repeated |
| green after `breaks.py restore` (byte copies, SHA-256 checked, no `P267-BREAK` left; the restored files are the ones the image was built from) | **1662 tests: 1658 passed, 4 skipped, 0 failed** (`--tests-only`, so no new image: `sl-modernuo:cc-P267` = `70e5c2cf4d46` stands) |

The red run, one break per fact:

| Break | Failed |
|---|---|
| 1. `clear` skips the first tracked item (left alive and tracked) | `PlaceTwicePlacesOnce...`: "Collection was not empty: [0x40025640 HalloweenDecor]"; `ABankOrFacetFilter...` (Luna's set not empty after `clear luna`) |
| 2. the window's end day left out (`k < b`) | `TheSeasonWindow...(11-02, in)` and `(01-06, in)`: expected True, got False; `TheAutomaticCheck...`: November 2 23:30 took it down ("the season is over", "removed 315") |
| 3. the saved serials not read back | `TheDecorAndTheStateSurviveARestart`: "Collections differ" at the reloaded serial set |
| 4. the row `britain/lantern-1` moved onto Britain's banker tile 1425,1690 | `ThePlacementTable...`: "britain/lantern-1 at 1425,1690 is on or beside the banker at 1425,1690" |

Facts 2b (`ABadDateSetting...`) and 6 (`TheSettingKeys...`) were not broken and stayed green, as expected.

## 5. Proof on this PC's test shard (client-free)

This PC has no game client, so the proof is the shard's own console: its start-up lines, and the same verbs the `[`
command runs, typed on the server console (`docker attach`, through `winpty` so Docker sees a terminal; the test
compose file gives the container a tty). Image `sl-modernuo:cc-P267` (`70e5c2cf4d46`), the test save as it was, the
test shard's `modernuo.json` pre-set to `start = 10-01` so October 20 is in season. Lines are the container log
(`docker logs sl-modernuo-test`), 2026-10-20 21:45 to 21:51 Chicago; nothing else was running against the save.

| Step | What was done | What the shard logged |
|---|---|---|
| 1 | first start on the image, window 10-01 to 11-02 | `the season has begun (10-01 to 11-02).` `placed 316 of 316 row(s); 0 already up.` then the start-up status: `up: 316 of 316 rows placed (by serial).` and the 21 bank counts |
| 2 | `docker restart -t 60` (the shutdown save, then a fresh load) | no placement line; the status: `up: 316 of 316 rows placed (by serial).` **The serials and the items survived the restart.** |
| 3 | `end` set to `10-19` in the test config, restart | `the season is over (10-01 to 10-19).` `removed 316 tracked item(s) by serial; nothing else is touched.` `up: 0 of 316 rows placed (by serial).` **The automatic take-down, by the saved serials, after a restart.** |
| 4 | console `halloween status` | `out of season (up October 1 to October 19)`, `up: 0 of 316` (the console route works) |
| 5 | `end` back to `11-02`, restart | `the season has begun (10-01 to 11-02).` `placed 316 of 316 row(s); 0 already up.` |
| 6 | console `halloween clear dryrun` | 316 `would remove` lines and `dry run: would remove 316 tracked item(s) by serial`; the status after it still 316 up |
| 7 | console `halloween clear` | `removed 316 tracked item(s) by serial; nothing else is touched.` then `up: 0 of 316 rows placed (by serial).` **`clear` removes all of it.** |
| 8 | `halloween place luna`, then `halloween place Malas` | `placed 10 of 10 row(s) for 'luna'`, then `placed 10 of 20 row(s) for 'Malas'; 10 already up.` (`umbra 10`); status `up: 20 of 316`, `luna 10/10, umbra 10/10` |
| 9 | `halloween clear Malas` | `removed 20 tracked item(s) by serial for 'Malas'; nothing else is touched.`; status `up: 0 of 316` |
| 10 | `halloween place` | `placed 316 of 316 row(s); 0 already up.`; status 316 of 316, every bank n/n |
| 11 | `halloween clear`, the config put back to the defaults (`10-24`, `11-02`), `Start-TestShard.ps1 -Down` | `removed 316 tracked item(s) by serial`, `up: 0 of 316`; the test shard stopped with its save; its world holds no HalloweenDecor |

Not proven here, for want of a client: the `[ClusterFHalloweenDecor` command typed in game (it calls the same `Run`
the console command calls, and the facts cover its verbs), what the pieces look like in game (the previews stand in),
and whether any piece is in a player's way (the tile rules stand in). Section 6 says what to walk.

## 6. Deviations, decisions and what I could not check

- **No screenshots.** This PC has no game client (no TazUO, no EA client; the memory note from P188 says the same),
  so the prompt's "screenshot each bank" is the previews in section 3.4 plus the test-shard log in section 5. **For
  Chase in the client:** walk New Haven, Britain and Luna with the decor up (`place` on the test shard) and look for a
  piece in a doorway or a walk, a lantern behind a wall, a cobweb on the wrong wall, a counter piece floating.
- **The community art is not in** (section 2). Not a judgment on the art: the files are not here.
- **Felucca twins** are a reading of "every facet the shard opens" (the prompt named the Trammel towns and Luna). If
  Felucca should stay bare, `clear Felucca` once, or drop the loop in `gen.py` and regenerate.
- **Doors:** the protected door tiles are pinned `DoorGenerator`'s scan over the box, with its `CanFit` refusal
  reduced to the files; a door Chase added by hand later is not in it (nor in P34's, which read New Haven's own
  seeder). The two-tiles-before-and-behind rule covers the approach either way.
- **Banker paths** are the shortest walk from each door to each banker over the floor; a banker with home range 0
  does not move, and every bank's bankers spawn at range 0 (the Vendors.json rows).
- **Art IDs above 0x3FFF** (the carved pumpkins 0x4691 and 0x4695) are stock art of the 7.0.117 client; my first
  validator refused them on a stale "< 0x4000" rule, corrected after the art check showed them present.
- Hue 0 everywhere; pinned's `TwilightLantern` hues 244 or 997 were not copied (the plain lantern reads as a lantern).
- `ClusterFWinterDecor` (P34) is left as it was. Two switches, one pattern, until P266 moves the winter one.
- `status.json` is unchanged (the publisher is public; the proof reads the container log instead).

## 7. Files changed

`D:\ShatteredLegacy`:
- `server\customizations\ClusterFSeasonalSwitch.cs` (new: `SeasonWindow`, `ClusterFSeasonalSwitch`, `ClusterFSeasonalState`)
- `server\customizations\ClusterFHalloweenDecorSeeder.cs` (new: `ClusterFHalloweenDecor`, `HalloweenDecor`)
- `server\customizations\ClusterFHalloweenDecorLayout.cs` (new, generated)
- `server\tests\Misc\HalloweenDecorVerification.cs` (new)
- `docker\uo\COMMANDS.md` (one row), `CHANGELOG.md` (2026.10.20.17), `VERSION`

`D:\UO\shard-migration`:
- `notes\cc-P267-halloween-bank-decor.md` (this)
- `notes\cc-P267-tools\` (`bankbase.py`, `gen.py`, `validate.py`, `gen_layout.py`, `render_previews.py`, `breaks.py`,
  `placement.json`, `validate.out.txt`, `gen.out.txt`)
- `notes\art\halloween-banks\*.jpg` (21 previews, 1.4 MB in all)

## 8. Website credits

None needed: every piece is Electronic Arts' own art as shipped in the client, placed by art ID. The credits section
for MrRiots' sets belongs to the follow-up that registers them.

## 9. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -Branch golem/Gold/P267 -NoRefresh -NoArchive`
(it commits nothing; both repos on `golem/Gold/P267`):

| Repo | Result |
|---|---|
| code | dry run |
| docs | dry run |

Neither repo BLOCKED. No file over 5 MB (the 21 previews are 1.4 MB in all; the largest 110 KB). Nothing is
committed: the Golem commits this branch after the DONE line and the merge Golem merges it into main.

P267 DONE
