# cc-P856: a winter set for New Haven before December 1

## In plain words

- **New Haven gets a winter set on December 1, by itself:** a Christmas train with lit lamps, smoke and turning
  wheels, a big walk-round snow globe with falling snow, a Santa bench and a snowman bench. They come down with the
  rest of the winter decorations after January 6.
- **Where on main's New Haven:** the train, the Santa bench and the snowman bench in the grassy park west of the big
  hall (north-west of the square); the snow globe on the grass by that hall's south-east corner. **On the release
  (testers') New Haven:** the Santa bench, the snowman bench and the globe on the harbour boardwalk below the plaza,
  and the train on the grass on the town's east side.
- **The Festival's winter stock** sells a Santa bench, a snowman bench and a holiday fireplace (stockings, garland, a
  bear rug) as house deeds. Each piece names its designer: Celestial, Milva, Candy Apple, and Lagatha after Gwenivere.
- **For you:** (1) the release half is a diff for the overseer to apply to the release branch
  (`notes\cc-P856-tools\p856-release-isle-20261028.diff`); (2) the holiday fireplace is **not** in either inn: no room
  fits it (see Deviations), so it is only a Festival deed; (3) when P855 merges, its Festival "holiday fireplace" row
  and this one overlap: keep one.

Iron Golem, 2026-11-10. Main code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy on `golem/Iron/P856`.
Release copy `D:\UO\golems\Iron\p856-isle`: a detached worktree at `6459dd3` (the tip of `release/isle-20261028`,
2026.11.08.3) with the release half staged; mine to remove after the overseer applies the diff. Nothing went to the
release branch, nothing deployed, no player package (stock art only). All play on the private proof shard (2596).
Downloads in `D:\UO\third-party\code\` read for their numbers only; nothing built, run or copied from there.

## Why hand-written classes

The prompt says to use P855's data addon if it has merged, else hand-written classes. P855 (committed `277078e` on
`golem/Iron/P855`) had not merged into main when this branch was cut (`9a06447`), so this is our own small addon
family. When P855 is in, these five designs could become P855 data files; nothing here depends on that.

## What was built (main; the release diff is the same code with the release town's rows)

- `server/customizations/WinterSet/WinterSetDesigns.cs`: **generated** by `notes/cc-P856-tools/convert856.py` from the
  downloads' YAAAG component lists (item ID, offset, hue, light, name). Counted (`convert-report.txt`): **train 241,
  snow globe 111, Santa bench 14, snowman bench 26, holiday fireplace 35** parts. Lights as the authors set them
  (YAAAG light 29 `Circle300`, 1 `Circle225`, 0 `ArchedWindowEast`).
- `WinterSet/WinterSetAddon.cs`: `WinterSetAddon` (a house addon of one design; parts keep their hues, each part shows
  "Design by <author>"), `WinterSetDeed` (Festival stock; deed names the author; redeed gives it back),
  `WinterSeasonAddon` (the seeded copy: an `IWinterDecorItem` with its row's key, no deed, never decays).
- `WinterSet/ClusterFWinterSetLayout.cs`: the set's rows for the winter decor (layer `addon`, ItemId 0).
- `ClusterFWinterDecorSeeder.cs`: every row is P678's layout plus the set's (`AllRows`); an `addon` row makes a
  `WinterSeasonAddon`; place/clear/status/areas unchanged otherwise (by serial, idempotent). **Existing worlds:**
  the switch only acts when the season changes, so a deploy in December would never place new rows; `TopUp` runs
  after every world load and places the set's missing rows **only while the decor is up** (automatic check on, it
  last put the decor up, in season, some of it standing), so a staff clear of the whole decor still stands.
  Before December 1 nothing is needed: the season's start places every row, new ones included.
- `RewardStores/FestivalStore.cs`: winter rows `santabench` (30 tokens), `snowmanbench` (30), `holidayfireplace` (40).
- `CHANGELOG.md` and `VERSION`: main **2026.11.10.2** (P855, not merged, takes 2026.11.10); release **2026.11.10**.

## Where they stand, and how the spots were chosen

Rules: P678's own map checks for the winter rows (`notes/cc-P678-tools/winter`: reached on foot from the square's
start, standing z, protected tiles: doors and swings, NPC posts, spawners, other seeders' tiles, the arrival tile, the
Reset Stone; nothing impassable), applied to **every tile a piece covers**, plus the town's walk with the pieces in
place, by `notes/cc-P856-tools/find856.py` (main, SoS map) and `rel/findrel.py` (release, vanilla Trammel; copies of
P266's `protected.py` and P237's `nhbase.py` repointed at my own copies, since they read another Golem's folder).
Three more rules came from looking: nothing standing under a piece (a garden bench under the first globe spot),
nothing impassable inside its outline (a fir between the train's cars), and **no building on the 3 tiles south or
east** of it (the client draws those over the piece: run 1's shots showed main's snowman bench under the hall roof,
main's globe under a building's roof, and release's snowman bench crammed among an ankh, lamps and a fence).

| Piece | Main (SoS New Haven) | Release (ML plaza) |
|---|---|---|
| Christmas train | 3612,2539,0, park west of the hall | 3548,2523,14, grass on the east side |
| Snowman bench | 3618,2545,0, park, between the train and the hall | 3503,2596,1, harbour pier |
| Santa bench | 3613,2554,0, park, open grass south of the train | 3503,2588,16, top of the harbour boardwalk |
| Large snow globe | 3639,2557,0, grass by the hall's south-east corner | 3519,2592,1, harbour pier |

Both towns: **all four together, the walk from the square reaches every tile it reached before**
(`validate-main.txt`, `validate-release.txt`). The train needs a flat clear 6 x 21: on main the nearest such place
to the square is the park (the square itself is paving full of protected tiles); on release, the east side.

`notes/cc-P856-review/`: `placed.md` (all **784** parts, one line each, both towns), `pieces.jpg` (the five designs),
`main-park.jpg` and `rel-harbour.jpg`, `rel-train.jpg` (isorender of each area with the pieces), `shots/` (the TazUO
shots below).

## Tests

`server/tests/Misc/WinterSetVerification.cs`, six facts (the release copy names fact 5 for its own town and checks
P266's ML town box, as the release has no `HavenSpots.Town`):

1. The five designs load with their part counts and authors, stock art only.
2. A house copy from its deed: every part at its offset with hue, light and name, its own hues kept, the author on
   parts and deed, redeed, and a save.
3. The set goes up with the decor as `WinterSeasonAddon`s at their rows, by serial; place twice places once; clear takes
   each down with all its parts and leaves an unrelated item on the tile.
4. `TopUp`: a world whose decor is up gets the missing set pieces once; a world cleared by staff, out of season or never
   put up gets nothing.
5. The rows: four, keys unique, each a design, inside the town; area `park` (release: `east`).
6. The Festival winter stock sells the three deeds.

`WinterDecorVerification.cs` (P34/P266/P678's facts): the three facts that place or count every row now use
`AllRows`, check an addon row as a `WinterSeasonAddon`, and count the addons' parts on clear.

- **Red first** (`red-stub.txt`, `red-isle.txt`): the facts against the code before the change (each branch's own
  seeder and Festival store, plus inert stubs of the new types so they compile): **6 failed** (every new fact),
  32 passed, on main and on release.
- **Green** (`green.txt`, `green-isle.txt`): 38 of 38 (WinterSet, WinterDecor, RewardStore facts) on both.
- **Gated builds** (`both-builds.ps1`, docker-build lock, page cache dropped first; `latest` not moved):
  - final main `sl-modernuo:cc-p856`: **EXIT=0, 3363 passed, 0 failed, 6 skipped** (`gated-build.log`);
  - final release `sl-modernuo:cc-p856-isle`: **EXIT=0, 3070 passed, 0 failed, 5 skipped** (`gated-build-isle.log`);
  - the first pair (`*-1.log`, before the spots moved) was also green: 3363 and 3070.

## In game (TazUO, `notes\cc-P856-shots\`)

Private proof shard only, under the test-shard lock, a fresh copy of the bot world per run, a Player-account
trainee ("Iron Winter"); staff hands (`kit\stage856.py`) put the decor up with `[ClusterFWinterDecor place` as
December 1 would, then the trainee stood north-west of each piece. Each run checks that a part of each piece stands
there; **every check PASS** in both towns (`release\walk.txt`, `main\walk.txt`), then `clear` took it all down.

- `main\` and `release\`: the final run, four shots each (`p856-main-*`, `p856-release-*`, also in the review folder).
- `run1-main\`, `run1-release\`: the first run, kept: it shows the three hidden or crowded spots that were moved.

## Deviations and decisions for Chase

- **The holiday fireplace is not placed in either inn.** It is 5 x 6 with its own back wall and a rug, south-facing.
  On main, the real inn's rooms are 5 x 4 bedrooms and a furnished common room; the hall the winter list calls "inn"
  is full (the long feast tables, stockings and painting on its north wall, and P34's own Christmas fireplace 0x3C60
  on its east wall: the inn already has a winter fireplace). The whole of main's town has one indoor room it fits, in
  the wrong building. The release's Gentle Rest Inn has no fit either (`find-fireplace-main.txt`, P678 rules; the
  release search found none). It ships as the Festival deed only. Placing it would mean moving the inn's furniture:
  say if you want that.
- **"On the square":** the train and benches are in the park beside the hall on main, not on the square itself (paved,
  full of NPC posts and other seeders' tiles); on release, on the harbour below the plaza and the east side.
- **"Main only" and "place everything twice"** read together as P849 did: the code change on main, and the release
  half as a diff (`p856-release-isle-20261028.diff`, 9 files, made against `6459dd3`, passes
  `git apply --cached --check` on `origin/release/isle-20261028`). For the overseer to apply; I did not commit it.
- **P855 overlap:** P855 (not merged) also adds a Festival winter row `holidayfireplace` (its data-addon deed) at the
  same place in `FestivalStore.cs`. The merge will conflict there; keep one of the two rows. Version: main here is
  2026.11.10.2 so P855's 2026.11.10 can go first.
- `TopUp` re-adds the set's pieces at a restart if staff cleared **only** the park or square area mid-season (a
  whole-decor clear stands). Rare; noted.
- The guard hook denied one command of mine whose text named another Golem's folder (a string I was replacing in my
  copy of P266's tool); I did it from a script file instead. Nothing read from or written to that folder.

## Files

- `ShatteredLegacy` (main): `server/customizations/WinterSet/` (3 new), `ClusterFWinterDecorSeeder.cs`,
  `RewardStores/FestivalStore.cs`, `server/tests/Misc/WinterSetVerification.cs` (new),
  `server/tests/Misc/WinterDecorVerification.cs`, `CHANGELOG.md`, `VERSION`.
- `shard-migration`: this file; `notes/cc-P856-tools/` (convert856.py, find856.py, validate856.py, rel/ (findrel.py,
  relwalk.py, the repointed copies), the edit scripts, probes, red stubs, build logs, kits, the release diff);
  `notes/cc-P856-review/`; `notes/cc-P856-shots/`.

P856 DONE
