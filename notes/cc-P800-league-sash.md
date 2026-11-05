# cc-P800: the League sash upgrades over time

## In plain words

- **The League sash now grows with the character.** Elara gives each registered citizen one free, from a new League Sash row in her menu. It is blessed, bound to that character, and stays through every loop.
- **Six steps, Dull Copper to Celestial.** When a character reaches the rank, they pay Renown at Elara (50 up to 10,000, placeholders). Each step gives a new name and metal hue and adds 1% more Renown from achievements and League jobs while worn, up to +6%. Spending never lowers rank.
- **Old League sashes convert by themselves** when their owner next logs in. A second one stays as an "old League" keepsake. Loot boxes stop giving the sash once a character has one.
- **For you:** nothing is live yet. After the merge, release `notes\cc-P800-tools\p800-release-isle-20261028.diff` to the test shard (below). Two things to look at: Dull Copper and Bronze look alike on the sash, and I found a Butcher's Eye bug to fix separately.

## What was built

Chase chose **Earned at Elara** (`Iron-P800-20261105-132922-5351`), so this is option 1 of `notes\cc-P800-league-sash-plan.md`.

- **`server/customizations/LeagueShop/LeagueSash.cs` (new):** the `LeagueSash` item, the table and the system.
  - **The item** is a source-generated serialized type saving its owner and step (D40). It is blessed and bound to the character. Nobody else can lift it, including another character on the account; staff can.
  - **Trade and drop** are refused. Dye and scissors are refused too; the plan didn't list those, but a dye breaks the hue's meaning and scissors would destroy it.
  - **The character's step** and the unpaid fraction of a Renown are kept in the account's `FlagValues`, the same per-character keys loops use. There is no account schema change, and it works unchanged on both branches.
- **`Configuration/league-sash.json`:** every number: first hue, sound, effect, and each step's metal, fee and bonus. Written with defaults on first start, refused whole if bad, reloaded by `[LeagueSash reload`. `[LeagueSash` lists the steps; `[LeagueSash step <n>` sets your own sash without a fee.
- **Elara's menu:** a League Sash row and page, showing the sash, the next step, its rank and fee, and Upgrade only when both are met. The press checks everything again, so a stale page charges nobody.
- **The Renown bonus:** paid on achievements and League jobs (requisitions and, on main, hunts), only while the owner wears their own sash. Fractions carry over, so a +3% sash on a 10 Renown achievement pays a little over time rather than nothing.
- **Loot boxes:** the sash leaves both box pools once the character has one. A sash rolled into a box stays the old type until opened, so an unopened box gives the opener theirs, or a keepsake if they already have one.
- **Version:** main `2026.11.05.3`, release `2026.11.03.2`, with a CHANGELOG entry in each.

## Where the build differs from the plan

- **Conversion runs at world load and at login.** The plan said world load. On a real load the pass found the sash and left it, because the holder's `Account` read as empty, so nothing converted. The facts could not see this, as a test character always has an account. Login now does the work, and a character's sash converts the first time they log in after the update.
  - **Unverified:** why `Account` was empty. The pinned source sets it while accounts load, and I saw this on one new character only. So I don't know how many characters the load pass will reach; the login pass covers them either way.
- **"Converts when picked up" became "converts at the next login or load".** A bound sash can't normally rest in a house, since the drop is refused. If one is there, it converts once its owner holds it at a login or load.
- **Renown inside loot boxes earns no bonus.** The plan named achievements and League jobs, so box Renown is left out.
- **An offline character earns no bonus**, because the sash has to be worn by a character online.
- **A rank-hued old sash goes to League blue at step 0**, as the plan says. A character with a Bronze-hued sash loses that look until they pay for the steps.

## Tests

`server/tests/Misc/LeagueSashVerification.cs`, 21 test cases from 16 facts: each of the six steps, the first sash, short Renown, the last step, Elara's page and a stale page, unregistered, a lost sash, conversion in place, conversion at login, binding and blessing, a loop, the bonus, the carry, the file, boxes, a save round trip, and a real achievement.

- **Red:** these facts were written after the code, so I broke the code on purpose. All 22 breaks turned a fact red (`cc-P800-tools\mutants.txt`), and every fact went red at least once. After the login refactor, 5 more breaks, including 2 repeats of changed code, all turned red (`mutants2.txt`).
- **Green on main:** `sl-modernuo:cc-p800`, 3,144 tests passing, `EXIT=0`, 193 patches applied (`gated-build.log`).
- **Green on the isle:** `sl-modernuo:cc-p800-isle`, 2,887 tests passing, `EXIT=0`, 176 patches applied (`gated-build-isle.log`).
- **`latest` was not moved.** The shared Test Shard was not touched; every proof ran on the private shard on 2596.

**Two failed isle gates, neither from this work.** Each was one unrelated test, and each passed on the next run; I kept both logs in `cc-P800-tools`:

- `TheInfernusDropsFireFromCombatOnACooldownAndItBurnsWhoeverStandsInIt` ("no second drop after the cooldown"). This is a random drop test.
- `AKilledNonBondedPetPaysNoImbueKillEffect`. This is a real bug, below.

A third isle failure was mine: main's `OnlineCharacter` helper isn't on the release, so the diff adds it.

## Proof in the client

- **`notes\cc-P800-shots\final\`:** one TazUO run on the private shard. All 14 checks in `walk.log` pass. The character takes the first sash from Elara's menu, wears it, and buys step 1 on her page with real Renown. The other five steps were set with `[LeagueSash step`, because their fees need about 20,000 Renown; facts cover every paid step.
- **`notes\cc-P800-shots\sheet-worn-steps.jpg`:** the worn sash in the paperdoll at all seven looks. I looked at it, and at Elara's menu and page shots.
- **`notes\cc-P800-shots\convert\`:** a saved old sash through a real restart and a real login, on the final main image. `load-1.log` shows the pass leaving it and `Converted Iron Old's old sash at login`. `load-2.log` adds no line after a second restart and login, so the conversion was saved and nothing repeated.
- **`[League] league-sash.json was missing; wrote the built-in defaults`** is in the shard log, so first start writes the file.

**Limits of that proof:**

- The step shots were taken before the login pass was added. That change doesn't touch the sash's look or Elara's page, so I did not retake them.
- Elara was placed on a meadow with `[add` and held still, not at her New Haven post.
- The conversion proof ran on main only; on the isle it is covered by the facts, not a real load.
- Elara's window shows no background in these shots, on her old menu rows too. I didn't find out why; it may be this rig's client. Please check it in a normal client.
- The upgrade's effect and sound were not seen or heard.

## For Chase

1. **Release to the test shard after the merge.** Apply `notes\cc-P800-tools\p800-release-isle-20261028.diff` to `release/isle-20261028`, then build and move the shard. It applies cleanly to the release tip `e8d210c`, and the same code built green as `sl-modernuo:cc-p800-isle`. The sash and fact files are byte-for-byte main's. If P799 or P806 land on the release first, expect small conflicts in `CHANGELOG.md` and `VERSION`. The P799 files I listed don't overlap with this diff's code, but I only saw the start of that list, and I did not check P806's.
2. **Dull Copper and Bronze look almost the same** (hues 2419 and 2418), and Celestial is a dark blue not far from the first sash. These are the metals' own hues, and the steps take them from the ladder, so the file can't change a step's hue today. If you want them clearer, that's a small follow-up.
3. **The fees and bonuses are placeholders.** Edit `Configuration/league-sash.json` and run `[LeagueSash reload`. A bonus of 0 turns it off.

## Found while here (not fixed)

- **Butcher's Eye can throw an error when a creature dies.** `ClusterFImbueEffects.ButcherOn` makes its rare part with `Activator.CreateInstance(type)`, and `UndyingFlesh` has no parameterless constructor, so the rare roll throws `MissingMethodException`. It's on main and the release. It should be a small fix in its own task, and it also makes `AKilledNonBondedPetPaysNoImbueKillEffect` fail at random.
- **The Infernus fact fails now and then** for random reasons. I did not trace it.

## Deviations and decisions for Chase

- **One command was auto-denied, as an unattended run.** I tried to run `rm -rf cc-P800-shots/*` in `notes` to clear my first shot attempt, chained with the next shot run. I did not retry the delete. Those leftovers stay: a few files at the top of `notes\cc-P800-shots\` and the folder `steps\`, an earlier run with a robe over the sash. Only `final\`, `convert\` and the sheet are the proof. They can be deleted.
- **Worktree to remove after the merge:** `D:\UO\golems\Iron\p800-isle` (detached at `e8d210c`, staged): `git -C D:\UO\golems\Iron\ShatteredLegacy worktree remove --force D:\UO\golems\Iron\p800-isle`.
- **Memory:** one wait for a build was stopped for low memory. The detached build carried on and finished green, so nothing was restarted. Available memory was about 3.2 GB then, and 7.3 GB after dropping the Docker cache.

## Files

- **ShatteredLegacy:** new `LeagueShop/LeagueSash.cs` and `tests/Misc/LeagueSashVerification.cs`. Changed `ClusterFAchievements.cs`, `LeagueRegistrarGump.cs`, `LeagueShop/LeagueShop.cs`, `LootBoxes/LootBoxItems.cs`, `LootBoxes/LootBoxRoller.cs`, `Requisitions/LeagueHunts.cs`, `Requisitions/RequisitionSystem.cs`, `Tutorial/ClusterFLoops.cs`, `CHANGELOG.md`, `VERSION`.
- **shard-migration:** this file, the plan, `notes\cc-P800-tools\`, `notes\cc-P800-shots\`.

P800 DONE
