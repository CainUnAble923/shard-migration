# P734 practice builds: gallery

Six builds laid by `notes/guides/building-and-decorating.md`, placed with `[PlaceBuild practice-<name> x y z` on a
private test shard (The Fold), walked with a real character, shot in TazUO from the default camera and reviewed by a
second Claude until PASS. Pictures are in `notes/cc-P734-review/` (`render-*.jpg` isorender, `shots/*.jpg` TazUO);
the walk logs in `notes/cc-P734-review/walks/`; each build's every piece in `notes/cc-P734-review/placed-<name>.md`.

| Build | Shows | Guide rules it exercises | Pictures |
|---|---|---|---|
| **farmhouse** (The Fold 5700,1170) | A light wood cottage under thatch with a fenced cabbage garden: hearth on the north wall, bed, table and two chairs, a brass sign beside the door, one gate in the fence. | 2.1 whole build at one Z; 2.2 post NW, L corner SE, the east piece at the SW tile; 2.3 roof at wall Z + 20 one tile in, gable on the south row; 2.4 WestCCW door, one gate; 3 chairs facing the table, torch on a plain west wall; 5 one fence ring by the wall rule; 11.3 hearth under the ridge. | [render](../cc-P734-review/render-farmhouse.jpg), [cut-away](../cc-P734-review/render-farmhouse-inside.jpg), [front](../cc-P734-review/shots/farmhouse-front.jpg), [inside](../cc-P734-review/shots/farmhouse-inside.jpg) |
| **bank** (5720,1170) | OSI's stone shop walls and windows under shingles, a counter with a banker behind it, three vault chests, a framed red carpet for the queue, candelabras, a bank sign. | 2.2 the stone shop set; 2.5 sign two east of the door on the 0x0B98 hanger; 3 torches on plain north and west walls; 11.2 carpet edges by the art; 11.10 the banker from a spawner line. | [render](../cc-P734-review/render-bank.jpg), [cut-away](../cc-P734-review/render-bank-inside.jpg), [front](../cc-P734-review/shots/bank-front.jpg), [inside](../cc-P734-review/shots/bank-inside.jpg) |
| **lodge** (5740,1170) | A League lodge in grey brick: hearth on the north wall, bookcases backed on the north and west walls, a long table with chairs on both sides, banners on the east wall outside. | 2.2 grey brick set and its windows by wall; 3 bookcases 0x0A98 north / 0x0A99 west facing in, chairs by the art, banners flat on their wall; 11.4 no window behind furniture. | [render](../cc-P734-review/render-lodge.jpg), [cut-away](../cc-P734-review/render-lodge-inside.jpg), [front](../cc-P734-review/shots/lodge-front.jpg), [inside](../cc-P734-review/shots/lodge-inside.jpg) |
| **dock** (1550,612, a real lake) | A three-row plank bridge across the lake and a pier out from the south bank: rope rails on the outer rows, stacked posts at the ends and corners, barrel and crate on the bank. | 4.1 joins within one step (banks Z 1, a walker on the bridge at 2; bank Z 6, on the pier 6), walked both ways; 4.3 OSI's dock pieces; 11.6 a real shore; 11.7 the deck starts on flat bank; 11.8 rails on the outer rows. | [render](../cc-P734-review/render-dock.jpg), [west end](../cc-P734-review/shots/dock-west-end.jpg), [east end](../cc-P734-review/shots/dock-east-end.jpg), [pier](../cc-P734-review/shots/dock-pier.jpg) |
| **market** (5722,1195) | A paved square of mixed pavers, three stalls (fruit, fish, flour and ham) with crates and barrels behind, a stone fountain in the middle, lamp posts. | 9 floors mixed so they do not tile; What to use where (the stone fountain, stock goods); 5 paths and signs kept clear. | [render](../cc-P734-review/render-market.jpg), [square](../cc-P734-review/shots/market-square.jpg) |
| **twostory** (5742,1195) | A plaster house of two storeys: a straight dark wood stair climbing north from the ground floor to an open landing, a bedroom with the hearth upstairs. | 2.1 storeys at +20; 4.2 stairs 5 per step climbing toward their name, the top meeting the floor, the floor open above; 11.3 no hearth under a floor. | [render](../cc-P734-review/render-twostory.jpg), [ground floor](../cc-P734-review/render-twostory-ground-floor.jpg), [upper floor](../cc-P734-review/render-twostory-upper-floor.jpg), [stair foot](../cc-P734-review/shots/twostory-stair-foot.jpg), [upstairs](../cc-P734-review/shots/twostory-upper.jpg) |

## The reviews

Three rounds by a second Claude (a fresh subagent each round, none of which made the builds), each with
`notes/cc-P734-tools/review-brief.md` (the integrator's review steps) and every render, shot, placed list and walk:

| Round | farmhouse | bank | lodge | dock | market | twostory | File |
|---|---|---|---|---|---|---|---|
| 1 | FAIL (9) | FAIL (4) | FAIL (6) | FAIL (7) | FAIL (3) | FAIL (5) | `notes/cc-P734-review/review-round-1.md` |
| 2 | FAIL (1) | FAIL (1) | FAIL (2) | PASS | PASS | PASS | `notes/cc-P734-review/review-round-2.md` |
| 3 | PASS | PASS | PASS | PASS | PASS | PASS | `notes/cc-P734-review/review-round-3.md` |

Round 1 found the wrong piece at every south-west corner, chairs and carpet edges facing the wrong way, signs over
the door leaf, a chimney through the thatch, windows behind furniture, a pond of water statics a walker strolled
across and a rail across the pier's mouth. Round 2 found round 1's carpet-corner advice itself wrong (it drew both
ways), a south-facing bookcase on a west wall, a bed mid-room and a runner made of fringe. Each became a rule in the
guide's section 11.


Client-art ideas for later (not used here; they need a client-package prompt first, What to use where): `beach-trees`
and `bamboo` round the lake, `olorin-market-tents` (stock art, needs converting) as stall awnings, the brass fountains
for a town square.
