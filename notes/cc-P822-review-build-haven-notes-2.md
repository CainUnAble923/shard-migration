# cc-P822: build review of P802 (New Haven tutorial notes, batch 2)

## In plain words

- P802 passes the building review: it built nothing new in New Haven. It only places two teachers, moves lessons into
  buildings that already stand in town, and clears the old tutorial farm.
- Ilyra (Mysticism) stands behind the table in the Magery School facing the door. Morvain (Necromancy) stands on the
  skull-candle dais facing the room. Both look right in the shots. The old farm spot is empty.
- Three small gaps in P802's review files, none of them in the build (listed under Notes for the fix-up).
- Nothing for you to do. P802 can merge.

Reviewer: Iron Golem, fresh session, 2026-11-07. Read `notes/guides/building-and-decorating.md` in full, the P802
notes, `notes/cc-P802-review/placed.md`, both diffs (`git diff main...origin/golem/Iron/P802` in the code and docs
copies, and the release diff `notes/cc-P802-tools/p802-release-isle-20261028.diff`), and looked at every image in
`notes/cc-P802-review/`: the 16 main place renders, the 18 release place renders, and the 16 TazUO shots.

## What P802 places

Nothing on the map and no static decoration. In the world it places:

- **Two NPCs per build**, seeded at load (`TutorialWingTrials.SeedTeachers`) and put back on their tile and facing:
  - main: Ilyra Moonwhisper at 3652,2473,0 facing South, and Morvain Ashgrave at 3693,2475,2 facing West;
  - release: Ilyra at 3485,2491,52 facing South, and Morvain at 3556,2454,15 facing South.
- **Lesson props that exist only while a lesson runs**: training echoes, a wild-garlic patch, a thieving chest, and an
  anvil and forge only when the smithy's own are missing.
- **One removal**: P276's farm addon, its door, the pen spawner and its animals west of the ML plaza.

The lessons themselves move into buildings that already exist on the Siege map (smithy, library, pier, and so on).

## Checklist, item by item

| Check | Result |
|---|---|
| Walls and corners, doors, stairs, roofs | None built. The renders show only the map's own buildings with lesson markers. |
| Wall-mounted items | None placed. |
| Signs (a sign, not a rune marker) | No new signs and no rune markers. Lessons point with the quest arrow and the window, and most of the buildings already have a shop sign. |
| Shores, bridges, docks, heights | None built. Fishing uses the existing west pier, with the arm tile at -2 and real water at -5 beside it (shot `fishing-pier.jpg`). |
| Foliage | None placed. Lumberjacking uses the map's own oak or willow, and the two practice-tree statics were removed. |
| NPC facing (section 3) | Ilyra faces the school's door gap across her table, and Morvain faces the room over the candle line (`mysticism-ilyra2.jpg`, `necromancy-shrine-keeper.jpg`). Release facings are South, toward each hall, and are checked by facts. |
| Nothing stray / leftovers (2.6) | The old farm goes at every start, only P802's own pieces (`TutorialFarm.ClearHavenOnLoad`, on a `Timer.DelayCall(Zero)` from `Initialize`, after the load). `old-farm-spot.jpg` shows the spot empty. |
| Props on surfaces, clear of paths | The echo and prop tiles are inside rooms or yards, off doors (renders `places/*.jpg`, `places-release/*.jpg`). The camping garlic is on open grass beside the road, which is fine for a forageable herb. |
| Better piece in What to use where | Not applicable: nothing was dressed. |
| Proof left for the reviewer (section 8) | `placed.md` and renders for both builds, plus in-game shots on main. |

BUILD REVIEW P802: PASS

## Notes for the Iron Golem (not blocking, no fix-up needed for the merge)

1. `placed.md` lists only main's NPCs and lesson tiles. The release's two NPCs (Ilyra 3485,2491,52 South; Morvain
   3556,2454,15 South) and its lesson tiles appear only in the notes and in `lesson-places-release.json`. Add a release
   section next time.
2. `notes/cc-P802-tools/shard-after-seed-lines.txt` is empty (0 bytes), but the notes cite it as the evidence for "took
   away 7 thing(s)". The shot and the facts still cover the farm removal.
3. There are no in-game shots of the release build's places or NPCs; only renders. The notes say so.

P822 DONE
