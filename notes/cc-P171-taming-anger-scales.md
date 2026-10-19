# cc-P171: Taming anger chance scales with skill (a 200 tamer should not anger a beast 95% of the time)

2026-10-18. Opus. Prompt: `D:\UO\cc-prompts\cc-P171-cont-taming-anger-scales.md`. Not committed (the Golem commits
after DONE). Both repos were clean at the start.

## Headlines

- **The cause:** pinned `AnimalTaming.cs:208` (d4531cd9) reads
  `else if (creature.CanAngerOnTame && Utility.RandomDouble() < 0.95)`. That is a flat 95% whatever the tamer's skill,
  so Chase's 30 angers in a row at 200 were the expected run.
- **The fix:** the chance is now `max(floor, base - perPoint x (Animal Taming - MinTameSkill))`, never above base.
  - Three server settings: `clusterf.taming.angerBase` 0.95, `clusterf.taming.angerPerPoint` 0.015,
    `clusterf.taming.angerFloor` 0.15.
  - Against the Dread Warhorse (108): 95% at 108, 77% at 120, 32% at 150, 17% at 160, 15% from 161.3 up.
  - Everything else in the anger branch is pinned's, untouched: the message, the sound, the pacify keep, Honor and
    Ethereal Voyage, the attack.
- **Which skill:** `Skills.AnimalTaming.Value`, so **worn bonuses count**. It is the value pinned's own checks read:
  the "no chance" gate (`:184`) and the taming roll's `CheckTargetSkill` (`:406`).
- **Proved through the real taming target**, by reflection on `AnimalTaming.InternalTarget.OnTarget`, so the patched
  line itself runs. A 200 tamer on a Dread Warhorse, 400 tries:
  - **before: angered 383** (pinned's 95%);
  - **after: angered 49** (12%; 15% expected).
- **27 creature types** on the shard can anger and are tamable (table below). They were counted by building every
  `BaseCreature` type in the test host, not by grep. The grep found 25 files; the two extra types inherit the flag:
  FrostDrake (from ColdDrake) and ParoxysmusSwampDragon.

## What changed

`D:\ShatteredLegacy` (uncommitted):

| File | Change |
|---|---|
| `server/customizations/ClusterFTamingAnger.cs` (new) | Defaults :21-23, the settings read in `Configure` :29-34 (`ServerConfiguration.GetOrUpdateSetting`, as `ClusterFHealerPolicy.cs:15-17`), `Chance(value, min)` :37-38 (`Math.Clamp(Math.Max(Floor, Base - PerPoint x (value - min)), 0, Base)`), `Chance(tamer, creature)` :41-42 (0 when `!CanAngerOnTame`), `Angers` :45-46 (pinned's test with that chance) |
| `server/patches/AnimalTaming-anger-scales.patch` (new) | One line: pinned `:208` becomes `else if (ClusterFTamingAnger.Angers(from, creature))`, with a two-line comment (`:208-210` in the built file) |
| `docker/uo/apply-patches.sh` | Applies it after `AnimalTaming-pet-training.patch` (its context), with the why, :678-683 |
| `server/tests/Skills/TamingAngerVerification.cs` (new) | The facts below |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.18.13`: one Changed line and one Staff line (the settings). VERSION 2026.10.18.12 → 2026.10.18.13 (.12 was committed with P170) |

`D:\UO\shard-migration`: this note; `testing\playtest-steps.json` (P171-1); `testing\bot-triage.md` (`### P171`);
`README.md`, `dashboard.html`, `tools\progress.json` from `tools\progress.py`.

**Why a patch and not a hook.** The test is an inline expression inside the private target class's `OnTarget`, and
no event or virtual reaches it.
- An override of `CanAngerOnTame` on each creature could only turn anger fully on or off, not scale it, and would
  cover only our 15 creature files, not pinned's 10.
- A replacement `InternalTarget` would copy about 200 lines of pinned taming and hide upstream drift. The project
  rejected that kind of change when it turned `CraftItem` into a patch (cc-P38).
- So it is one line, in the same file the pet-training patch already touches.

## The table (defaults)

Printed by `TheTableForEveryCreatureThatCanAnger` from the built image: every tamable type with `CanAngerOnTame`, its
live `MinTameSkill`, and the anger chance for a tamer at 108, 120, 150 and 200 Animal Taming.

| Creature | MinTameSkill | 108 | 120 | 150 | 200 |
|---|---|---|---|---|---|
| BloodFox | 72.0 | 41% | 23% | 15% | 15% |
| ColdDrake | 96.0 | 77% | 59% | 15% | 15% |
| CuSidhe | 101.1 | 85% | 67% | 22% | 15% |
| Dimetrosaur | 102.0 | 86% | 68% | 23% | 15% |
| Dragon | 93.9 | 74% | 56% | 15% | 15% |
| DragonWolf | 102.0 | 86% | 68% | 23% | 15% |
| DreadWarhorse | 108.0 | 95% | 77% | 32% | 15% |
| FrostDragon | 105.0 | 91% | 73% | 28% | 15% |
| FrostDrake | 96.0 | 77% | 59% | 15% | 15% |
| FrostMite | 102.0 | 86% | 68% | 23% | 15% |
| GreaterDragon | 104.7 | 90% | 72% | 27% | 15% |
| Hiryu | 98.7 | 81% | 63% | 18% | 15% |
| LesserHiryu | 98.7 | 81% | 63% | 18% | 15% |
| Lion | 96.0 | 77% | 59% | 15% | 15% |
| Najasaurus | 102.0 | 86% | 68% | 23% | 15% |
| Nightmare | 95.1 | 76% | 58% | 15% | 15% |
| OsseinRam | 72.0 | 41% | 23% | 15% | 15% |
| ParoxysmusSwampDragon | 93.9 | 74% | 56% | 15% | 15% |
| Reptalon | 101.1 | 85% | 67% | 22% | 15% |
| RuneBeetle | 93.9 | 74% | 56% | 15% | 15% |
| SabertoothedTiger | 102.0 | 86% | 68% | 23% | 15% |
| Saurosaurus | 102.0 | 86% | 68% | 23% | 15% |
| Skree | 95.1 | 76% | 58% | 15% | 15% |
| StygianDrake | 85.0 | 61% | 43% | 15% | 15% |
| SwampDragon | 93.9 | 74% | 56% | 15% | 15% |
| Triceratops | 102.0 | 86% | 68% | 23% | 15% |
| WhiteWyrm | 96.3 | 77% | 59% | 15% | 15% |

All 27 were 95% at every skill before.

## Tests

Shard tests through `docker/uo/build.sh -t sl-modernuo:cc-P171` only.

**`TamingAngerVerification`**, 11 cases:
1. `TheChanceFallsWithSkillToTheFloor` against a Dread Warhorse, defaults:
   - 108 (the minimum) 95%; 120 (+12) 77%; 148 (+40) 35%; 160 17%;
   - 162 and 200 the 15% floor;
   - 100 (below the minimum) still 95%.
2. `TheThreeSettingsAreRead`: `SetSetting` then `Configure`. 0.5 / 0.01 / 0.3 gives 0.4 at +10; a steeper slope hits the
   0.3 floor. The defaults are restored after.
3. `ACreatureThatCannotAngerNeverAngers`: a Horse at 200 with the settings at 100% anger. Chance 0, `Angers` false, and
   the real taming target starts the taming 200 of 200 times.
4. `ATwoHundredTamerAngersADreadWarhorseAboutFifteenPercent`: 400 tries through the real target; must be 30 to 95
   (15% is 60, 95% is 380).
5. `TheTableForEveryCreatureThatCanAnger`: the table above. It must contain the Dread Warhorse.

**Seen red first:**
- **Pinned's behavior** (`ClusterFTamingAnger` stubbed to a flat 0.95 with `Configure` reading nothing; the patch in
  place): **6 failed**. Fact 1 at 120, 148, 160 and 200; fact 2 (0.95 for 0.5); fact 4 (**angered 383 of 400**).
  1478 passed.
- **By mutation** (base hard-coded 0.9 with no cap, and the `CanAngerOnTame` test removed from `Chance` and `Angers`):
  the facts that match pinned on old code went red. Those are fact 1 at the minimum (108) and below it (100), and fact 3,
  the creature that cannot anger. With them, all of fact 1 and fact 2 failed: 7 TamingAnger failures.
- **Restored after each:** the source was copied back byte for byte, and `grep MUTATION` / `RED STUB` finds nothing.
- **First run with the fix:** 1 failure, my own expectation (Deviation 1); fixed.
- **Final:** `Built sl-modernuo:cc-P171 with patches applied and 1485 shard test(s) passing` (1485 passed, 0 failed,
  4 skipped).
- The table and the 49 of 400 come from a separate `dotnet test` of the class with detailed logging in the built
  builder image.

**Play-test tool tests:** `python -m unittest tools/tests/test_play_who.py`: 16 of 18. The 2 failures are earlier work:
M-001, P163-0, P164-0 and P165-1 to P165-6 have no Who or Where. P171-1 passes the shape test.

## Play-test items added

One, P171-1, under **For Chase** below. Sorted **BOT** in `testing\bot-triage.md` (`### P171`): the anger and start
messages, 502805 and 1010597, are what the server sends. It has steps and a check line in `testing\playtest-steps.json`.

## Deviations and decisions for Chase

1. **The brief's "160 and up 15%" is about 2 points early.** By its own formula, 160 against 108 is
   0.95 - 0.015 x 52 = **17%**, and the floor starts at 53.3 points above the minimum (161.3 for the warhorse). The
   brief's other two figures are exact: 120 gives 77%, 150 gives 32%. I kept the formula and its defaults, and the test
   says 17% at 160. Set `angerPerPoint` to 0.01539 if you want the floor exactly at 160 for the warhorse.
2. **Capped at base.** The brief's formula, below the minimum (only possible with a Dark Wolf familiar on a wolf,
   `CheckMastery`, `:184`), would go above 95%. I capped it at base, so it is never worse than pinned's.
3. **MinTameSkill, as the brief says, not CurrentTameSkill.** Since cc-P130 the "no chance" gate reads
   `CurrentTameSkill`, which is higher for a trained pet that is tamed again. For every wild creature the two are equal.
   For a trained one the anger chance reads from the creature's base minimum, so it is a little lower than measuring
   from the trained one. Say if you want `CurrentTameSkill` instead; it is one word in `ClusterFTamingAnger.cs:42`.
4. **A fidelity note for `docs/` (agents do not edit it).** This is a deliberate deviation from OSI and ModernUO's flat
   95%. Per AGENTS.md it belongs in `docs/fidelity-principle.md`, which needs the overseer.
5. **Two unrelated flaky tests seen once:** `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies` (`:243`) in the
   mutation run, and in P170 `CC6Batch1CreatureVerification` (Skree control slots). Both passed in every other run.
   Neither was investigated here.
6. **No task-list tool exists in this session,** so per-step progress was not posted there; these sections follow the
   prompt's steps in order.
7. **Not deployed:** the test shard was not rebuilt or restarted by me. The image `sl-modernuo:cc-P171` (and
   `sl-uo-builder:cc-P171`) exists, and `latest` was not moved. The throwaway mutation builder image was deleted.

## For Chase

Rebuild the test shard from HEAD after the commit (or start it on `sl-modernuo:cc-P171`).

**The three settings** live in the test shard's bind-mounted
`D:\ShatteredLegacy\server\uo\modernuo\Configuration-test\modernuo.json` (`Configuration\modernuo.json` for the other
config). The server writes them there with the defaults on its first start with this build (`GetOrUpdateSetting`) and
reads them at start, so restart after changing one:

| Setting | Default | Turn it up to | Turn it down to |
|---|---|---|---|
| `clusterf.taming.angerBase` | 0.95 | anger more often at the minimum (1.0 = always) | anger less often at the minimum |
| `clusterf.taming.angerPerPoint` | 0.015 | skill counts faster: the floor comes sooner (0.0 = flat, pinned's behavior) | skill counts slower |
| `clusterf.taming.angerFloor` | 0.15 | even a master angers more often | a master almost never angers (0.0 = never) |

Pinned's behavior is `angerPerPoint` 0 with `angerBase` 0.95.

To try it in game:

1. **Tame a Dread Warhorse at 200:** a character at 200.0 Animal Taming with 3 follower slots free, at a wild Dread
   Warhorse. Use Animal Taming on it 20 times (step back after an anger). **Pass:** most tries start the taming; only
   about 1 in 7 (roughly 2 to 6 of 20) says "You seem to anger the beast!", where before it was nearly every try.

## Repo size rule

No file over 5 MB in either repo. The new files are source, the largest `TamingAngerVerification.cs` at about 9 KB.
Build logs and the patched scratch copies stayed in the session scratchpad, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (run after `tools/progress.py`):

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

Code: 6 files pending (the table under What changed). Docs: this note, the two `testing\` files I wrote, the
importer's `testing\SUMMARY.md` and `testing\play-tests.json` (machine output, refreshed from Haven by the dry run),
and `README.md`, `dashboard.html`, `tools\progress.json`. Nothing BLOCKED.

P171 DONE
