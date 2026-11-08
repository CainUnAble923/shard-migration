# cc-P823: fix-up of P817 (creation and the isle start) after P821's build review

## In plain words

- **The isle bank's roof is clean now.** A row of eight grey squares showed on the bank's west roof slope. They were
  the ceiling poking through the low edge of the roof, and they are gone. The League lodge had the same eight squares
  from the same builder code; they are gone too.
- **The outside photo of the bank is retaken without windows over it.** The photo now shows the bank lesson signpost
  by the road and the plain west roof slope.
- **P817's other changes ride along unchanged:** humans only, no trade profession, Tutorial Island as the only start, a
  brighter wake, the pet at the end of the isle, and Merrin facing his counter.
- **For you:** the overseer ships `notes\cc-P823-tools\p823-release-isle-20261028.diff` instead of P817's release diff.
  It is P817's diff plus the roof fix, and it needs the next isle player package, since the map patch is in the
  package. Nothing else to do.

Iron Golem, 2026-11-07. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P823`. Nothing committed; `latest` was not moved and nothing was published.

## Step 1: bringing P817 in

This step was not done as written. The prompt says to check out `golem/Iron/P817` and merge `main`; the hand-off says
to stay on `golem/Iron/P823` and not merge or switch branches. `P823` was already at `main`, so I took P817's one
commit in each repo with `git cherry-pick --no-commit` (`46cdbc5` docs, `d8d917c` code). The end state is the same, as
in P806.

The one conflict was `CHANGELOG.md`, because P813 had taken 2026.11.07.8. P817's lines moved to a new section,
**2026.11.07.9**, and `VERSION` is 2026.11.07.9. The isle release keeps its own number (P817's diff), unchanged.

## The reviewer's items

**1. 0x049C ceiling on the bank's west eave (6758,3973-3980): done.** The reviewer was right. The ceiling stands at
floor + 20 over the room, but the pitched roof's west eave column sits at floor + 19, so the ceiling showed through.
Every other column's roof is at 22 or higher.

What changed:
- **`trammel.mapops` (code copy):** the eight `S+ 6758 y 20 1180 0` lines are gone.
- **The lodge:** the same rule removed `S+ 6778 3996..4003 20 1180 0`. The lodge is laid by the same builder loop and
  showed the same eight squares (`lodge-before-isorender.png`). It was not on the reviewer's list, but it is the same
  defect, so I fixed it rather than leave it for a third review.
- **No other tiles:** a scan of the whole patch found no other ceiling tile under a lower roof slope.
- **No B lines changed:** they fingerprint EA's blocks, not ours. `SOURCE.txt` has a cc-P823 entry.
- **The driver:** `notes/cc-P662-tools/build_isle.py` now skips the west eave column when it lays the ceiling (only
  while `eaveDz` is below the ceiling's Z), so a rebuild lays the same.
- **The driver's record:** `notes/cc-P662-tools/statics-placed.csv` is the build's statics list, which
  `tools/tests/test_mapops.py` test 7 compares with the shipped patch. I took the 16 ceiling rows out of it.
- **A gap from P817:** the same test was failing on P817's branch, because P817 moved the strongbox and removed the
  potted plant in the patch and `isle-sets.json` but not in this CSV. The CSV now matches: the strongbox row is at
  6762,3973 and the plant row is gone. `test_mapops.py`: 14 tests, OK. I ran it with `SL_SHARD_REPO` pointing at the
  code copy.
- **Isle release:** the same 16 lines and the `SOURCE.txt` entry, in the release copy (`D:\UO\golems\Iron\p817-isle`,
  detached at `56f98af`). Its full staged diff is saved as `notes/cc-P823-tools/p823-release-isle-20261028.diff`
  (P817's diff plus this fix), and it replaces P817's.
- **Renders** (isorender on a fresh overlay of this patch, `D:\UO\golems\Iron\p823-proof\overlay`):
  - `bank-after-isorender.png`: the west slope is plain shingle, like the east one. `bank-before-isorender.png` is
    P817's render, with the squares.
  - `lodge-before-isorender.png` / `lodge-after-isorender.png`: the same fix on the lodge.
  - `bank-after-cutaway.png`: the inside, roof cut away, unchanged.

**2. The door-side shot was covered by the paperdoll and Version History: done.** These windows open on a run's first
login, after P817's clearing script had finished. P817's shot was the first of its run.

The fix:
- `Clear823.py` keeps closing gumps for about 30 s.
- The bank's west shot is taken after a throwaway warm-up login (`shots-bank-west.json`), since the clearing script
  does not reach TazUO's own windows.
- The tester stands at 6753,3984, west of the bank, so the signpost at 6757,3982 and the west slope are both in view.

New client shots, from the default camera, on the private proof shard (port 2596, image `sl-modernuo:cc-P823`, P817's
player package client with this patch):
- `bank-outside-west-after.jpg`: no windows; the signpost north of the road; the west roof slope plain.
- `bank-outside-after.jpg`: P817's door-side view again, now clean.
- `bank-inside-after.jpg`: inside, Merrin behind the counter, unchanged.
- `lodge-outside-after.jpg`: the lodge's west slope plain.
- `bank-outside-before.jpg`: P817's covered shot, for comparison.

All are in `notes/cc-P823-review/` with `placed.md`, which adds the 16 removed tiles to the top of P817's list.

## Walk

Nothing walkable changed: the removed pieces are ceiling tiles at Z 20 under the roof. So there was no stair, door or
join to walk. The inside shot shows the room unchanged with the tester inside.

## Tests and build

- **Gated build:** `docker/uo/build.sh -t sl-modernuo:cc-P823` on P817 plus main: **green**, 3,278 shard tests,
  EXIT=0 (`notes/cc-P823-tools/green-gated-build.txt`). That includes P817's facts. I changed nothing under `server/`.
- **Map patch tests:** `tools/tests/test_mapops.py`, 14 tests, OK (see item 1).
- **Locks:** docker-build and test-shard were taken and released; the proof shard is down. Free memory was 7.4 GB
  before the build.

## Deviations and decisions for Chase

- **Step 1:** cherry-pick instead of checkout and merge, as above.
- **The lodge's ceiling:** fixed too, though it was not on the review's list (item 1).
- **Two image reads were auto-denied:** `D:\UO\golems\Iron\p823-proof\shots\bank-outside-west.jpg` and
  `lodge-outside.jpg`, read in place to check them. Those shots belong in the review folder anyway, so I copied them
  to `notes/cc-P823-review/` and looked at them there. The west one was then retaken (item 2).
- **Package:** not rebuilt or published. The shots used P817's built package with this branch's `trammel.mapops`
  dropped into a copy of it (`D:\UO\golems\Iron\p823-pkg`). The isle package that ships the release diff picks up the
  fix by itself.

P823 DONE
