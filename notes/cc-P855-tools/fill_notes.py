"""cc-P855: fill the notes file's two placeholder sections (one-off)."""
p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P855-decor-addon-housing-furniture.md"
s = open(p, encoding="utf-8").read()

gated = """**Gated builds** (the docker\\uo build script through `gated-build.ps1`, image `sl-modernuo:cc-p855`, under the
docker-build lock, page cache dropped first; `latest` not moved):

- `gated-build-1.log`: EXIT=0, 3362 shard tests passing, 6 skipped (before fact 6 and `[DecorAddon place/clear`).
- `gated-build.log` (the final code): **EXIT=0, 3363 passing, 0 failed, 6 skipped** (the same 6 skips as main), all
  six ShardDecor facts and `TheStockIsF13sStarterTableAndHandsOverNoMagicItem` passing.

Free memory before the second build read 2.6 GB, 3.0 GB after dropping the Docker page cache; I wrote the walk and
these notes meanwhile and started the build when it read 10.1 GB."""

shots = """## In game (TazUO, `notes\\cc-P855-shots\\`)

Private proof shard only (127.0.0.1:2596, a fresh copy of the bot world, image `sl-modernuo:cc-p855`, main's SoS New
Haven), under the test-shard lock. A Player-account trainee, "Iron Decor", in TazUO; staff hands through
`kit\\stage855.py`. The shard's start log: `[DecorAddon] 30 designs in 14 deeds from
/modernuo/Data/ShatteredLegacy/Decoration/Addons`, no file refused.

- **Run 1, the pieces** (`p855-<design>.jpg`, 30 shots): staff stood each design on the grass east of the League hall
  (`[DecorAddon place <design> 3677 2570 0`, then `clear` before the next). Every piece draws where its file says:
  e.g. `p855-grey-fireplace-large-south.jpg` (lit fires), `p855-holiday-fireplace.jpg` (stockings, poinsettias, the
  bear rug), `p855-buffet-table-east-west.jpg`, `p855-harpsichord-south.jpg`, `p855-blue-couch-south.jpg` (the
  cushions' and table's own hues). Logs in `run1-logs\\`. Its player half stopped on a script bug of mine (TazUO
  title-cases property text, so my lowercase "buffet" match missed a deed that was there; the log shows the deed's
  text), so:
- **Run 2, the player** (`player\\`, `walk.txt`: every check PASS): with 1,000 AP and 2,000 Renown granted,
  `[leagueshop`, the hunt row's buffet table confirm (`p855-league-hunt-row-confirm.jpg`), Buy: one deed in the pack
  reading "A Deed For A Hunt Master's Buffet Table | Design By Manwitch | Facings: East-west, North-south | House
  Decor"; double-click: the facing window (`p855-facing-window.jpg`); east-west: the placement cursor; aimed at open
  ground: "You can only place this in a house that you own!" and the deed kept (`p855-refused-outside-house.jpg`).
  `p855-achievement-store.jpg` is the store's first page only; the furniture rows are on later pages and were not
  paged to in the shot (fact 5 covers them).
- Not shown in game: a player placing a deed inside their own house (no house was staged; P809's perch proof did the
  same). That path is pinned's `BaseAddonDeed` target, unchanged."""

s = s.replace("PLACEHOLDER-GATED", gated).replace("PLACEHOLDER-SHOTS", shots)
s = s.replace(
    "fails in any filtered run at `BasePigmentsOfTokuno.IsValidItem` (the Tokuno config only loads in the full suite: the\nsame probe failed the same way on the unchanged image) and passes in the gated build.",
    "fails in any filtered run at `BasePigmentsOfTokuno.IsValidItem` (a null `TreasuresOfTokuno.RewardEra`: the Tokuno\nconfig only loads in the full suite; my first probe, which ran the image's own unchanged tests after a compile error of\nmine, failed it the same way) and passes in the gated build.")
assert "PLACEHOLDER" not in s
s = s.rstrip() + "\n\nP855 DONE\n"
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
