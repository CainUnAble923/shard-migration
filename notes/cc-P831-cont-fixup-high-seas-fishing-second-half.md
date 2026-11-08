# cc-P831: fix-up for P269 (High Seas fishing, the second half): its branch did not merge into main

## In plain words

- **Nothing changes in the game.** The High Seas fishing work from P269 (bait, magic hooks, the Oracle of the Sea, lava
  fishing, fish pies, Corgul) has been on main since 2026-10-25, when the earlier fix-up P587 merged it.
- **The integrator was retrying an old copy of P269's branch.** That copy was out of date, which is why it hit
  conflicts. This fix-up records that branch as merged, with main's version of every file kept, so the integrator
  stops retrying it.
- Nothing for you to do.

Iron Golem, 2026-11-08. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P831`.

## What I found

- `origin/golem/Iron/P269` (code `19fd417`, docs `49e4beb7`) branches from `608d0b4`, from before 2026-10-25. Main
  already has the same work: `30b225c` "CC task P587: fix-up for P269", merged as `db4c85b`. P587 brought P269's
  files onto main and resolved them against the main of that day (the same 30-odd files: `Bait.cs`, `Hooks.cs`,
  `FishPies.cs`, `OracleOfTheSea.cs`, the Corgul mobiles and so on). Main's CHANGELOG carries P269's player lines (the
  fish mongers, bait, hooks, the Oracle, under 2026.10.25).
- So the conflicts are not two pieces of work meeting. They are the old branch against main's newer copy of the same
  work plus everything merged since.

## What I did

Instead of checking out `golem/Iron/P269` as the prompt says, I merged it into this branch with `git merge --no-commit
--no-ff origin/golem/Iron/P269` in both copies. The hand-off says not to switch branches. The result is the same
merge, and the integrator merges `golem/Iron/P831`.

Conflicts and how I resolved them (main's side in every case):

| File | Conflict | Kept |
|---|---|---|
| `CHANGELOG.md` | P269's 2026.10.25 section against main's | Main's. It already has P269's lines (708-712, 1320), and P269's side added nothing main lacks. |
| `VERSION` | 2026.11.08 against 2026.10.25 | 2026.11.08, the higher. |
| `docker/uo/apply-patches.sh` | P269's side lacks every patch line merged since (P610, P721, P168, P728, P743, P714, P769, P763, P782, P785, P787, P793, P804, P809) | Main's. P269's three `apply_patch` lines (`FishingPole-high-seas-bait-hooks`, `Fishing-high-seas-bait-hooks-lava`, `AOS-fish-pies`) are already in it, in the same place. |
| `server/customizations/Engines/Craft/CookingCraftRegistrations.cs` | header comment: P269 says SweetCocoaButter is "in neither tree"; main says cc-P785 added it and the nutcrackers in `ChocolatieringRecipes.cs` | Main's (correct since P785). |
| docs `tools/expansion-coverage.json` | P269's older counts (883 / 4247 / 1208) against main's (884 / 4248 / 1209) | Main's, the later count. |

Every file git merged by itself already matched main. Check: in the code copy, `git write-tree` after the resolution
equals `origin/main^{tree}`, so the merge commit's tree is exactly main's. In the docs copy, `git diff --cached HEAD`
is empty. The docs main has since moved on only by the P826 review merge.

## Tests and build

- **No gated build.** The prompt asks for `docker\uo\build.sh -t sl-modernuo:cc-P831` when anything under `server\` or
  `docker\uo\` changed. Nothing did: the merged code tree is byte-identical to main's, so main's own gated build
  already covers it, including P269's facts as P587 left them. I took no lock and built no image.
- No other tests run, for the same reason.

## For the integrator

- The merge commit on `golem/Iron/P831` takes `golem/Iron/P269` in as a parent with main's tree. After it merges,
  P269's branch counts as merged and nothing on main changes.

P831 DONE
