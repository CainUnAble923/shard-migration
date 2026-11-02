# cc-P760 review: what is placed in the world

One thing is placed: the **Festival Peddler's stall** in New Haven (Trammel), up only while Halloween, winter or spring
is on (`FestivalMarket`, `server/customizations/RewardStores/FestivalStore.cs`). It is seeded on world load and on the
hourly check when a season starts, and taken away when it ends; every piece is tracked by serial in
`ClusterFSeasonalState` ("festival-peddler"), so take-down deletes exactly these six things. Nothing else in the prompt
places anything: the guild stores, the Achievement store and the League shop are windows on existing NPCs and buttons.

The peddler's tile is the setting `clusterf.festival.peddlerAt` (default `3636,2627,0`); every piece is placed relative
to it. All at Z 0 on flat grass (land 0x0003-0x0006, Z 0), checked tile by tile on the shard's own map (the isle
overlay's `map1LegacyMUL.uop` and statics, which carry New Haven as the shard draws it): no static on any of the six
tiles.

## The stall

| Item | Location | Facing / variant | What it is |
|---|---|---|---|
| FestivalPeddler (mobile) | 3636,2627,0 | faces south, CantWalk, RangeHome 0 | Tamsin Brightwick, the Festival Peddler; double-click (or say "festival", "buy", "token") opens the store |
| 0x0B7C table | 3636,2628,0 | the west half of a long east-west table | the stall's table, in front of her (south) |
| 0x0B7D table | 3637,2628,0 | the east half (0x0B7C + 0x0B7D join into one table; rendered both ways, `stall-isorender.png`) | the stall's table |
| 0x0E3D crate | 3635,2627,0 | | a crate of festival wares, behind her (west) |
| 0x0E77 barrel | 3637,2627,0 | | a barrel of festival wares, behind her (east) |
| 0xA854 signpost | 3634,2626,0 | reads from the south (the guide's north-of-the-path face) | "The Festival Peddler: festival wares for tokens" |

## Where and why

- **Off the bank square, on the walk side:** the stall stands in the grass yard south-east of New Haven's bank block,
  between the brown-roofed house to the west, the thatched shed to the north and the covered market roof to the east
  (`stall-isorender.png`). Customers come from the dirt yard to the north-west and walk up to the table from the south.
- **Clear of doors, signs and paths:** the house to the west opens on its west side; the shed and the market roof have
  no door on this yard. Nothing stands on the dirt path that runs east-west into the yard at y 2627 (x 3630 to 3634).
- **The sign north of its path:** the signpost is on the north edge of that path (the path's tiles at 3630-3634,2627
  are directly south of it), north-west of the stall, facing the path (building guide section 6).
- **No props on anything else, nothing stray:** the six tiles above are the whole stall.

## Proof

- `stall-isorender.png`: isorender of 3629-3643, 2620-2634 on the shard's map with the stall added
  (`notes/cc-P760-tools/render_stall.py`, `STALL_MAP` = the isle overlay folder).
- TazUO shots from the default camera on the private proof shard (127.0.0.1:2596, image `sl-modernuo:cc-P760`):
  `stall-outside.jpg` (the Tester three tiles north-west of the stall), `stall-south.jpg` (from the south, the
  customer's side), and the store windows (`festival-*.jpg`). Listed in `notes/cc-P760-reward-stores.md`.
- The stall went up by itself on the proof shard's first world load (today, November 1, is inside the Halloween window):
  `[FestivalMarket] The Festival Peddler's stall is up at (3636, 2627, 0) (6 pieces).`
- Not walked: the stall has no walkable join (no stair, bridge, dock or door), so section 4's walk logs do not apply.
