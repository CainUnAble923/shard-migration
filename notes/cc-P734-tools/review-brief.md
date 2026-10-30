# Build review brief for the P734 practice builds (the same steps the integrator's review prompt gives)

You are the build reviewer: a second Claude that did not make these builds. Look at them with fresh eyes. Read only;
do not edit any file except your own review file named below. Time limit: 45 minutes.

1. Read `D:\UO\golems\Iron\shard-migration\notes\guides\building-and-decorating.md` in full: the checklist (section 1),
   the wall, corner, roof, door and window rules (2), facing (3), heights and stairs (4), land (5), markers (6), proof
   (8), the human-builder rules and examples (9) and What to use where.
2. The work: six practice builds placed on a private test shard (The Fold). Five stand on Green Acres (x 5700-5779,
   y 1170-1224, flat grass Z 0): farmhouse 5700,1170; bank 5720,1170; lodge 5740,1170; market 5722,1195; twostory
   5742,1195. The dock stands on a real lake from round 2: origin 1550,612 (banks Z 1 west and east of the bridge rows,
   Z 6 south of the pier; the lake bed -15 under water statics at -5). Coordinates in the placed lists are relative
   to each origin. From round 2, also read the previous round's review file and say, item by item, whether each fix
   was made.
   - `notes\cc-P734-review\placed-<build>.md`: every piece (item ID, x,y,z relative, facing).
   - `notes\cc-P734-review\render-<build>.jpg` (isorender, client-correct) and the cut-aways
     `render-<build>-inside.jpg`, `render-twostory-ground-floor.jpg`, `render-twostory-upper-floor.jpg`.
   - `notes\cc-P734-review\shots\*.jpg`: TazUO from the default camera (outside, front, inside, the stair, both bridge
     ends, the pier). The paperdoll on the left of each shot is the client's; ignore it.
   - `notes\cc-P734-review\walks\walk-<build>.log`: a real character's steps through each door, gate, stair, bridge
     and dock and back (each line a step with x, y, z; "STUCK" means it could not go on).
   - The build files themselves: `D:\UO\golems\Iron\ShatteredLegacy\server\data\Decoration\Builds\practice-*.cfg`.
3. Check one by one, against the guide and the placed list, for each build: every wall and corner (post NW, L corner
   SE, the east/south rule, nothing missing or doubled), every door (in the wall line, opening onto its room, folding
   along the wall), every window (the right piece for its wall), every stair (climbs the right way, 5 per step, the top
   meets the floor, open above), every wall-mounted item (on its wall, facing the walk side), roofs (on the walls,
   nothing on top), signs (a sign naming it, not a marker), heights of the bridge and pier both ends (from the walk
   logs), furnishing that fits the place, and any piece where What to use where names a better one.
4. Write `notes\cc-P734-review\review-<round>.md` (round given below) with one section per build and, on a line of its
   own for each, exactly `BUILD REVIEW <build>: PASS` or `BUILD REVIEW <build>: FAIL`, and after a FAIL a numbered
   list (1. 2. 3.) of fixes, each naming the piece (item ID, relative x,y,z), what is wrong and what the guide wants.
   Say what you could not judge from the pictures. Reply with the six verdicts and the fix lists.
