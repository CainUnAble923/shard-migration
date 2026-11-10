# cc-P858: real-light lamps and the Festival Peddler's wagon

## In plain words

- **Eleven lamps that light up:** a dragon lantern, bird, koi and dragon egg lamps, a stained glass lamp, tall antique
  and modern floor lamps, an ornate table lamp, an ancient dragon brazier, a gold tray of candles and a jack-o-lantern
  with eleven carvings. Double-click one to light it or put it out; the house decorator turns it (the jack-o-lantern
  changes carving) and it stays lit. Ten are in the **Achievement store** (75 AP each, from 200 AP total); the
  jack-o-lantern is in the **Festival Peddler's Halloween stock** (20 tokens).
- **A fortune teller's wagon stands beside the Festival Peddler's stall in New Haven** whenever a festival is on (it goes
  up and comes down with the stall, from December 1 for winter). It sits on the edge of the paved square just east of
  the stall, and players can **climb its new steps onto the porch and walk inside** (the original could not be entered).
- **Credits** on every piece: Drafted and Milva for the lamps, Olorin for the wagon.
- **For you:** (1) the testers' (release) New Haven is a different map: the stall there stands at the same spot, which
  on that map is the old ruined Haven, so the release needs its own stall and wagon spot before this goes there (see
  "Both New Havens"); (2) prices are placeholders in `reward-stores.json`.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy on `golem/Iron/P858`. Main only.
The downloads in `D:\UO\third-party\code\` (drafted-lamps-jackolanterns, milva-dragon-lantern, milva-stained-glass-lamp,
milva-tall-lamps, olorin-fortune-teller-wagon) were read for their numbers only; nothing built, run or copied from
there. Stock art only: no client or player package change. All play on the private proof shard (2596).

## In game (TazUO, `notes\cc-P858-shots\main\`)

Private proof shard (2596) only, under the test-shard lock, a fresh copy of the bot world on `sl-modernuo:cc-p858`. The
trainee "Iron Lamps" is on a Player account; staff hands (`kit\stage858.py`) only forced the winter festival
(`[FestivalMarket season winter`, which put up the stall and, by itself, the wagon: `[global get Location where
FortuneTellerWagon` = 3647,2632,0), moved the trainee, laid eleven lamps on the square (`[add`), set the night
(`[GlobalLight 26`) and turned one lamp (`[Flip`, the decorator's path). Everything else is the trainee's own client
(`kit\Walk858.py`). **Every check PASS** (`main\walk.txt`):

- `p858-stall-and-wagon.jpg`: the stall and the wagon together, from the grass between them.
- **The stair, walked for real both ways** (API.Walk, one tile a step, each step's z logged): up from the street
  3647,2643 z 0: 2642 z 0, 2641 z 2, 2640 z 7, 2639 z 12, 2638 z 17, the porch 2637 z 21, 2636 z 21, the doorway 2635
  z 19, inside 2634 and 2633 z 19; then back down the same tiles to 2643 z 0. No step rose more than one stair step.
  Shots: `p858-stair-foot.jpg`, `p858-porch.jpg` (on the porch), `p858-inside.jpg` (inside; TazUO lifts the roof),
  `p858-stair-going-down.jpg`, `p858-down-again.jpg`.
- **The lamps:** `p858-lamps-day.jpg` (eleven laid, unlit), `p858-lamps-night-unlit.jpg`, `p858-lamps-night-lit.jpg`
  (all eleven lit by double-click), `p858-lantern-turned.jpg` (the lit dragon lantern turned east, still lit); the
  jack-o-lantern went out on a second double-click.
- Copies of the shots and the walk log are in `notes\cc-P858-review\` for the build reviewer.

**What the runs caught.** `run1\` (kept): the trainee double-clicked the lamps 0.6 s apart and the server answered
"You must wait to perform another action" five times (6 of 11 lit); the script now waits 1.4 s. `run2\` (kept):
staff's `[Flip` did nothing to the lantern. **A real bug, not the script:** ModernUO's `[Flip` and the house's interior
decorator read `[Flippable]` from the item's own type, not inherited (`FlipCommandHandlers`, `InteriorDecorator.Turn`),
and it sat only on the shared base. Fact 3 had read it with inheritance and passed. Fixed: the fact now reads it as the
decorator does (seen failing on that code, `red-flippable.txt`: 3 facts red), `[Flippable]` is on each lamp with two
looks or more (`green-flippable.txt`), and the final run turned the lantern.

**Seen, not ours:** skeletons walk New Haven's square by the stall in every run (the pinned post-UOML spawners at
3635,2625 and 3651,2627, Spawner (113), load on main's SoS land too). Worth a look in a spawns prompt.


## The lamps (`server/customizations/Items/Lights/ShardLamps.cs`)

One base, `ShardLamp : BaseLight`, with a table of looks (unlit and lit art per facing or carving), and eleven lamps.
Stock `BaseLight` does the lighting (double-click within 2 tiles, the sounds); `Duration` is zero, so none burns out.
`[Flippable]` with a `Flip()` that steps to the next look and keeps the lamp lit or unlit, so the interior decorator's
Turn and `[Flip` both work. Each lamp's tooltip says how to light it and whom it is after.

**Every art ID was read from our client's tiledata and rendered** (`notes/cc-P858-tools/lampnames.txt`,
`cc-P858-review/lamp-art-1..3.jpg`), because the downloads' tables were wrong in places: Drafted's ornate table lamp and
dragon brazier both start on 0x04C1 (wooden logs), his dragon lantern's lit art is another lamp's animation frame
(0x4CDE), and Milva's dragon lantern and Drafted's disagree. What we use:

| Lamp | Looks (unlit/lit) | Light | After |
|---|---|---|---|
| Dragon lantern | S 0x4C40/0x4C41, E 0x4C42/0x4C43 | Circle300 | Drafted and Milva |
| Bird lamp | S 0x4C44/0x4C45, E 0x4C46/0x4C47 | Circle300 | Drafted |
| Koi lamp | S 0x4C48/0x4C49, E 0x4C4A/0x4C4B | Circle300 | Drafted |
| Dragon egg lamp | S 0x4C4C/0x4C4D, E 0x4C4E/0x4C4F | Circle300 | Drafted |
| Stained glass lamp | 0x4C50/0x4C51 | Circle225 | Drafted and Milva |
| Tall antique lamp | S 0x4C52/0x4C53, E 0x4C54/0x4C55 | Circle300 | Drafted and Milva |
| Tall modern lamp | S 0x4C56/0x4C57, E 0x4C58/0x4C59 | Circle300 | Drafted and Milva |
| Ornate table lamp | 0x49C2/0x49C1 | Circle150 | Drafted |
| Ancient dragon brazier | 0x194E/0x194D | Circle150 | Drafted |
| Gold tray of candles | S 0x983E/0x983F, E 0x983A/0x983B | Circle150 | Drafted |
| Jack-o-lantern | 11 carvings: 0x4694/0x4691, 0x4698/0x4695, 0x9934/0x9931 ... 0x9951/0x9952 | Circle150 | Drafted |

Milva's three lamps are the same art as Drafted's (P852's finding, confirmed by tiledata), so they are folded in as the
dragon lantern, the stained glass lamp and the two tall lamps, credited to both. Stock ModernUO has none of these types
(checked by class name in `D:\UO\ModernUO-pinned`); its `HalloweenPumpkin` lights only the two round pumpkins and only
rarely, so the 11-carving jack-o-lantern is new.

**Stores:** `AchievementStore.cs`, ten rows `ap.lamp.<kind>` (75 AP, opens at 200 AP total), after the paintings;
`FestivalStore.cs`, Halloween row `festival.halloween.jacklantern` (20 tokens). New rows take their defaults on a
server whose `reward-stores.json` predates them (`RewardStorePrices.PriceOf` falls back to the row's default). The
store guardrail (`EveryRowOfEveryStoreCanBeMadeAndNoneIsGearOrMagic`) passes: stock art, no properties.

## The wagon (`server/customizations/FestivalWagon/`)

- `FortuneTellerWagonDesign.cs`: **generated** by `notes/cc-P858-tools/convert858.py` from Olorin's YAAAG list (item,
  offset, hue, light, name; numbers only). Counted: **199 source parts**, our table **212**: the author's "ladder"
  0x3DB4 out, **14 stair parts** in.
- **The z nudge, done properly.** The author's note ("you will have to adjust the z a tad to get inside") is about the
  south porch: its deck (0x3EB0 at z 18, 3 high) tops out at 21, and the only way up was one 10-high block. We put a
  real stair there, the building guide's way (4.2): light wood north steps 0x0722 at z 0, 5, 10, 15 (top 20, one under
  the deck), blocks 0x0721 under the two upper steps, two tiles wide under the porch's two open deck tiles, hued as the
  wagon's wood (2418). From the porch the doorway (0x9B29, not impassable) leads onto the carpet at z 19.
- `FortuneTellerWagon.cs`: the addon (every part a `FortuneTellerWagonComponent` with its own hue, light and name, its
  tooltip naming Olorin; `ShareHue` off).
- `FestivalStore.cs` (`FestivalMarket`): the stall's `Up` places the wagon at `clusterf.festival.wagonAt` (x,y,z or
  `off`, default `3647,2632,0`) and tracks it by serial with the stall, so `Down` takes it away exactly; `TopUpWagon`
  (after every world load and hourly) puts it up once on a world whose stall is already up. **Existing worlds:** before
  December 1 nothing is needed (the winter season's start places the stall and the wagon); a world whose stall is up
  at deploy gets the wagon at the next load.

### Where, and why there

**Main's New Haven is on the Siege of Sosaria land**, not the vanilla map. The stall's own review (P760) checked the
vanilla files (`client-data-copy`), where 3636,2627 is a walled yard in the ruins of old Haven; on the SoS land the
server really runs, the stall stands on a strip of grass at the west edge of a large paved square
(`notes/cc-P858-tools/sosgrid.py`, `stallgrid.py`; P678's `view.py`). The wagon (6 by 16 with its stair) was placed by
P856's checker rewritten for it (`notes/cc-P858-tools/find858.py`, P678's rules: reached on foot from the square,
standing z within 2, no protected tile (doors, NPC posts, spawners, other seeders' rows), nothing blocking or standing
under it, nothing tall south or east of it for the camera, and the town's walk still reaching every tile it reached
before), with the stall's six tiles and a ring round them kept clear and the stair's foot required reachable.

- 186 origins fit near the stall; every one stands mostly on paving (the grass round the stall is too small: walls 8
  rows apart). The closest, **3647,2632**, is chosen: on the square's west edge, south of the open forge, 8 tiles east
  of the stall's barrel, its stair coming down onto the street (`cc-P858-review/main-stall-wagon-3647-2632.jpg`,
  `main-wagon-cutaway.jpg`).
- Nearer spots fail for named reasons (`find858.py` diagnostics): the forge's roof and display cases north, the
  Blacksmith's spawner at 3645,2617, a pinned spawner at 3651,2627.

Building guide (`notes/guides/building-and-decorating.md`): read first. Its "What to use where" market list has no
wagon or caravan piece, so the prompt's own pack is the fit. Checked against its list: the stair follows 4.1 and 4.2
(walked both ways for real, 5 a step, blocks under the upper steps, climbing toward the porch it serves); the wagon is
placed whole in its one variant, nothing turned (3); nothing new in the stall's walk or on a door line (5, 6); it
appears on an existing world by itself (7); renders, shots, walk log and `placed.md` are in `cc-P858-review/` (8).

### Both New Havens

"Main only" and "both New Havens" read together as P849 and P856 did, except that **the stall itself is the problem on
the release**: the release branch places it at the same 3636,2627, and the release's map is vanilla Trammel, where that
tile is the walled ruin yard of old Haven (a post-UOML skeleton spawner at 3635,2625 beside it), not the release's own
New Haven (the ML plaza, x 3400-3560). The wagon cannot stand there either (walls 8 rows apart). So the release half is
not a diff here: it needs a stall spot in its own New Haven first (a release prompt), and then
`clusterf.festival.wagonAt` set for that town (or `off`). Nothing was changed on the release branch.

## Tests

`server/tests/Items/LampsAndWagonVerification.cs`, eight facts:

1. Eleven lamps, each starting unlit on its first look, every look a distinct pair, credited.
2. Double-click within 2 tiles lights and again puts out each lamp; at 3 nothing; no burn-out timer.
3. Flipping by the decorator's path (`FlippableAttribute.Flip`): the lantern turns east and back, staying lit; the
   one-look lamp stays; the jack-o-lantern steps through all 11 carvings and back.
4. The stores: ten lamp rows in the Achievement store, each handing over its lamp; the jack-o-lantern in Halloween stock
   only.
5. A lit, turned lamp survives a save.
6. The wagon's design: 212 parts, no ladder, the two-wide stair 0, 5, 10, 15 under the porch deck at 18, blocks under
   the upper steps, nothing else on the stair's tiles; Olorin's names kept.
7. The wagon addon lays every part at its offset with its hue, light and name.
8. The wagon comes and goes with the stall; `TopUpWagon` puts it up once on a world whose stall is up, never when the
   stall is down or the setting is off.

`RewardStoreVerification.TheFestivalStallIsPlacedInSeasonAndRemovedWhenItEnds` now counts the wagon (pieces + 2).

Watched red, then green (`notes/cc-P858-tools/red-all.txt`, one container on `sl-uo-builder:bot`, `red-all.sh`):

- **The code before the change** (`red/stub/`: the stores as on main, the lamp and wagon names inert): **8 failed**
  (seven of the new facts and the stall fact), 14 passed. The eighth new fact (double-click) passes there vacuously (no
  lamps); it is red under `m-burnout`.
- **Twelve mutants** (`make_red.py`), each caught: a turned lamp forgets it was lit (fact 3), no flip (3, 5), the look
  always the first (3, 5), the lamp burns out (1, 2), no AP rows (4), no Halloween row (4), the wagon's hues lost (7),
  the stall up without the wagon (8, stall), the wagon untracked (8, stall), no top-up (8; `red-m-topup.txt`, its
  first version did not compile and was rerun), a top-up that doubles (8, stall), the ladder back and no stair (6).
- **Green:** 22 of 22 (the new facts and the 14 store facts).
- **After the TazUO run:** fact 3's helper corrected (see In game) and seen red on the code before the fix (3 red), then
  green (8 of 8).

- **Gated builds** (`gated-build.ps1`, docker-build lock, page cache dropped first; `latest` not moved): the final one,
  after the `[Flippable]` fix, `sl-modernuo:cc-p858` **EXIT=0, 3365 passed, 0 failed, 6 skipped** (`gated-build.log`,
  UTF-16), the eight lamp and wagon facts among them; the first (`gated-build-1.log`, before the fix) the same. Free
  memory was checked before each run; the second build started at 1.8 GB and the build's page-cache drop brought it to
  4 GB before the builder ran.

## Files

- `ShatteredLegacy`: `server/customizations/Items/Lights/ShardLamps.cs` (new), `server/customizations/FestivalWagon/`
  (2 new), `server/customizations/RewardStores/AchievementStore.cs`, `RewardStores/FestivalStore.cs`,
  `server/tests/Items/LampsAndWagonVerification.cs` (new), `server/tests/Misc/RewardStoreVerification.cs`,
  `CHANGELOG.md`, `VERSION` (**2026.11.10.4**: P855, P856 and P857, not merged here, take 2026.11.10 to .3).
- `shard-migration`: this file; `notes/cc-P858-tools/` (convert858.py, find858.py, render858.py, placed858.py,
  stallgrid.py, sosgrid.py, findwagon.py, findtogether.py, lampnames.py/.txt, the probe, red stub and mutants and
  results, the build wrapper and log, the TazUO kit); `notes/cc-P858-review/`; `notes/cc-P858-shots/`.

P858 DONE
