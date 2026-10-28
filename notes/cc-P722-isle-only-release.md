# cc-P722: an isle-only release branch (last night's build plus the isle fixes, no map swap)

Iron Golem, 2026-10-28.

## In plain words

- There is now a release branch with only your isle fixes on top of last night's release, and none of the Siege of
  Sosaria map swap: `release/isle-20261028`, commit `61ebab0` (pushed). The overseer releases from it.
- I played it on a private shard from that branch. A brand-new character went from the beach to Rook through all ten
  lessons with nothing failing. A real character in the game client walked the dock by the moongate **both ways**
  (onto the landing and back to the road, no step trouble), and in and out of the bank, the lodge and Wren's
  farmhouse through their doors. I looked at the bank, lodge, farm and dock shots: walls, roofs, doors, signs,
  tables and the counter all face the right way.
- One thing you will notice: the bank lesson's signpost stands two tiles straight in front of the bank's door, so
  walking straight at the door bumps into it and you step round it. It is P720's design and the same on main; say if
  you want it moved one tile aside.
- For you: nothing to try. When P723 (the bandage fix) merges into main, nothing changes here: the branch already has
  it.

## What to release

- **Branch:** `release/isle-20261028`, pushed to origin.
- **Commit:** `61ebab0ffd389d485d7f3b882d5f73572cf6f74a`.
- **Worktree:** `D:\UO\golems\Iron\release-isle-20261028` (a worktree of my code copy, outside both repos' desks).
- **Base:** `9ee74b6` (package 2026.10.27.2106). `VERSION` is `2026.10.28.5`.
- **SoS package switch:** `player-package\vendor\sos-trammel-map\switch.txt` says **off** on the branch (it was off at
  9ee74b6 already: P713 is in 9ee74b6's history, merged as 4decbd8). No pick touches it.
- Not built as a package, not published, not merged into main. The shared Test Shard was not touched.

## Isle fixes included (in merge order)

| Task | Picked | On the branch | Notes |
|---|---|---|---|
| P717 first character takes the isle | `0044237` | `9277a0d` | clean |
| P718 Chase's walk, round 1 | `08d9692` | `4f05664` | CHANGELOG/VERSION conflict only (both sections kept) |
| P720 Chase's walk, round 2 | `41fe8c1` | `3cd5e56` | map patch adapted (below); CHANGELOG; `SOURCE.txt` |
| P721 bandage wait, via P723 | `cb4dd56 -m 1` | `67cd6fd` | P723's own merge, taken against its first parent (P718) |
| P719 client defaults | `18d524e` | `61ebab0` | CHANGELOG as its own section `2026.10.28.5` |

**Merge order.** P717, P718 and P720 had merged into main in that order. P719 merged while I worked (`f6ee4fd`, the
same commit I picked). **P723 has not merged into main yet**; I took its branch tip `cb4dd56`, which is what it will
merge. If the integrator changes it before merging, the branch needs that change too.

**P721 through P723.** P721's own commit `7b0431a` was written before P718 and conflicted in six files. P723 is that
commit merged onto P718 with its conflicts resolved, so I picked P723's merge against its first parent: only P721's
changes, already fitted to P718. One conflict was left, with P720: the vision lesson's instruction line. P720 changed
"the bright blue rune stone" to "the lesson's signpost there"; P721 changed "under a minute" to "about a minute"
(it lengthened the scene). I kept both edits: "...double-click the lesson's signpost there. Watch the vision; it
lasts about a minute...".

**Left out:** every SoS swap commit (P674, P675, P678, P681, and the rest of P674 to P691), and everything else after
9ee74b6. Nothing from the isle work was left out.

## What I adapted for the stock land

**P720's map patch.** After P675, main's `trammel.mapops` is built on the SoS map, and P720 rebuilt the isle on that
copy. I checked the merge block by block (`notes\cc-P722-tools\mapops_compare.py`, `mapops_verify_merge.py`):
- P720 changed **44 blocks** (x 6624-6831, y 3952-4007), all on the isle.
- All 44 sit on void in both maps: their fingerprints (B lines) are **the same** at 9ee74b6 and in P720, and their
  lines at 9ee74b6 equal P720's parent's.
- So git's merge is exactly right: the branch's file is 9ee74b6's file with those 44 blocks' lines from P720,
  and every other block, every fingerprint (879) and the header are 9ee74b6's. The Old Haven way in, the Burrows'
  mouth and P276's farm removals stay, as on the stock land.
- `SOURCE.txt`: P675's re-base lines left out; P662's and P720's isle lines written for the stock land.

**CHANGELOG.** Main renumbered P718's section to `.3` when it merged; on the branch it is `.2`. Sections:
`2026.10.28` (P717), `.2` (P718, with P721's lines, where P723 put them), `.4` (P720), `.5` (P719).

**No code depended on swap code.** The picks share five files with the swap (`CharacterCreation.cs`,
`FoldRegions.cs`, `LeagueRegistrar.cs`, `TutorialStations.cs`, `TutorialTradeTrialVerification.cs`). Each pick's
change there stands alone. The isle coordinates are the isle's own, and P717's locked New Haven entry reuses the
branch's own New Haven (`HavenSpots`, stock: the moongate lands at 3501,2572).

## Tests on the branch

- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P722`, `docker-build` lock, released): **EXIT=0**,
  2,734 shard tests, 2,729 passed, 5 skipped, 0 failed (`cc-P722-tools\green-gated-build.txt`).
- **Map facts** (`tools\tests\test_mapops.py`): main's copy checks for the swap (the Old Haven way in gone), so I ran
  the version before P675 (`4afe091`) on the branch's patch: 9 of 10 pass (`green-test-mapops.txt`). The one
  failure, fact 5 (rebuilds P188's old scratch map), **fails the same way on 9ee74b6's own file**, on the same two
  blocks 231751 and 332429 (`base-9ee74b6-test-mapops.txt`). That failure was there before. Fact 7 (the isle is P720's
  build) fails on 9ee74b6 and passes on the branch.

## On the private shard (127.0.0.1:2596, `test-shard` lock, released; the shard is down)

The shard ran `sl-modernuo:cc-P722` on a copy of last night's bot world, with the branch's map patch on **stock**
client data (`cc-P722-tools\overlay.ps1`; 9ee74b6's `Build-MapOverlay.ps1` has no SoS base). The client was our
TazUO with patches 0001 to 0009 (P719's build), its map built from the branch's patch the way the package does.

**Bot route** (`cc-P722-tools\isle.py`, P721's route): **run 4, 0 failed checks** (`runs\run4\playlog.txt`). A fresh
character woke on cold sand on the beach, took all ten lessons, and the moongate put it beside Rook at
3501,2572 in 184 s. The New Haven pick started on the plaza at 3503,2574. What I changed in the bot:
- Rook and the New Haven start are back on stock New Haven. P718 had moved them for P678.
- P721's copy never ran on P720's isle (P721 was based before P720), so I taught it P720's layout: the vision's
  signpost replaces the rune; Wren is 4 tiles from the road behind the new fence; it walks into the bank round the
  lesson's signpost.
- Earlier runs: run 1 found those three. Run 2 was not fresh. Run 3 had all ten lessons pass but the bot's planner
  found no path into the bank. A real character walks it (below), so it is a bot limit, not the isle.

**Real character in TazUO** (Iron the Tester, the client's own steps, no teleport; `runs\walks\*.txt`):

| Walk | Result |
|---|---|
| **Dock by the moongate** | **East** from the road 6812,3991 onto the landing 6830,3991,-2; **west** back to 6812,3991,0. Both ways, no stuck step. |
| Bank | In through the south door (6762,3980) to the counter, and back out through the door. |
| Lodge | South through the north door (6782,3995) to Elara's desk (6782,3997), and back out to 6782,3991. |
| Farmhouse | North through the south door into the cottage (6691,3975,7), and back out to the road. |

**The signpost in front of the bank.** On the first bank walk, a straight walk north from the square stopped at
6762,3983. The bank lesson's signpost stands at 6762,3982 (`TutorialCorePlacement.SignPoint`, P720), two tiles in
front of the door and on its line. TazUO slid the character east along the wall instead of in. Round the post, the
door works both ways. It is a nuisance, not a block, and it is the same on main.

**Facing check** (my own look at the shots, `D:\UO\golems\Iron\p722-proof\shots\`, P720's spots):
- **Bank:** stone walls with whole corners and a pitched shingle roof. Windows. The door in the south wall, hung
  against the wall. The bank sign by the door. The counter runs along the room, with Merrin behind it. Chests and
  candelabras upright.
- **Lodge:** roof whole. League banners flat on the east wall. Bookcases backed against the walls, facing in.
  Elara's desk and the carpet square to the walls.
- **Farm:** one fence all round the field, with the pen closed inside it. The cottage's steps, door and chimney whole.
  The table, chairs and fireplace inside. The well upright. Signposts standing along the road.
- **Dock:** planks laid lengthwise, rope rails on both sides, posts at the corners. The moongate and its sign on the
  landing. The shore end meets the sand.

Nothing faced the wrong way. The stills: `bank`, `bank-in`, `lodge`, `lodge-north`, `lodge-in`, `farm`,
`farmhouse-in`, `dock`, `beach`, `camp-rack`, `chat-sign`, `yard`, `stones`, `bridge-walk` (with frames).

## Deviations and decisions

- **P723 was not merged** when I built the branch (the prompt asked to run after it merged). I took its pushed tip
  rather than stop; see Merge order.
- **Commits and a push.** The Golem's standing rule is no commits or pushes. This prompt asks for a pushed release
  branch, so I committed the picks on `release/isle-20261028` in its own worktree and pushed that branch only. My
  Golem branches (`golem/Iron/P722`) have no commits from me; the only new files are these notes.
- **Bot and walk tools** are in `notes\cc-P722-tools\` (2.4 MB): the resolve and check scripts, `isle.py` and its
  edit scripts, the walk maker and scripts, the proof-shard and shot runner copies, the runs.
- Outside the repos: `D:\UO\golems\Iron\release-isle-20261028\` (the worktree: keep it until the release is out),
  `D:\UO\golems\Iron\p722-proof\` (shard copy, overlay, shots) and `D:\UO\golems\Iron\p722-work\` (scratch); the last
  two can be deleted.

P722 DONE
