# cc-P814 placed pieces

Only what this fix-up moved. Everything else stands as in `notes\cc-P806-review\placed.md`, which this replaces for these two signs.

## Release branch (stock New Haven)

- 0xA854 signpost, 3471,2588,10, faces south, "Housing lesson, stop 1: a small house", north of the street on forest floor, no statics on the tile, road directly south, none north within 3, none beside (moved from 3469,2589, where it stood through the stock bench 0x0B2C)
- Housing stop 1 (no item), 3470,2590,10, on the dirt street, 2 tiles from its sign (moved from 3468,2591)

The old sign's blemish is gone: bank dirt at 3469,2586 was 3 tiles north of 3469,2589. The new tile's nearest bank dirt, at 3470,2585, is 3 tiles north and 1 west, so it is outside the column the rule reads. The stables sign keeps its one blemish, recorded in `notes\cc-P806-review\placed.md`.

## Main (SoS land)

- 0xA854 signpost, 3609,2614,0, faces south, "The stables: the sick-bay stall is inside, on the left", the porch strip just north of the door path, no statics on the tile (moved from 3608,2614, under the barn's eave, a hay roof piece 0x26EC at Z 29)

## On a seeded world

`SeedHaven` takes a named sign away from any spot but its own and places it at the new one. Fact: `AStop1SignLeftAtItsOldSpotIsTakenAwayOnASeededWorld`.
