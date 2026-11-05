# cc-P804: Herbalism, phase 1

## In plain words

- **Herbalism is in.** It's a new skill to 200 with the Order of the Alembic. Players pick wild herbs that grow back, keep a ledger with `[herbalism`, and take a bowl and seeds from a new herb table in the Order's hall.
- **Players can grow their own reagents.** Bowls grow at the usual pace, a raised bed is tended as one, and crossing same-strain plants can breed a better strain up the metal ladder. Herbs become bundles, and bundles open into reagents. A small farm makes about 70 reagents a day.
- **The Camping lesson now uses it:** the trainee picks wild garlic as well as lighting the fire.
- **For you:** nothing is live yet. Testers need the isle release **and a new player package**, or Herbalism won't show in their skills window (steps below). All numbers are placeholders in `Configuration/herbalism.json`, and I made some calls the research left open: please check the list under "Decisions I made".

## What was built

All seven parts are built on main and the release. The code is in `server/customizations/Herbalism/`, and the engine changes are four `.patch` files that apply with `--fuzz=0`.

1. **The skill.** `SkillName.Herbalism = 58` and a 59th `skills.json` row. Gains come from harvests, pollination, processing and picking, in a window that climbs with the herb's tier and the strain, up to 200. A mutation gives extra rolls. The Alembic owns the skill, and its Apprentice task now takes the higher of Alchemy and Herbalism.
   - Pinned's anti-macro defaults and feature flags both had 58 baked in. The anti-macro one would have crashed a fresh server at start, so both are patched.
   - **Loop memory:** the prompt says it applies, but no loop memory code exists yet (F-12), so there's nothing to hook.
2. **Foraging.** `HerbPatch` items, 27 spots in the file, placed by key on any world at load. Picked patches hide and regrow on a timer (60 minutes). Tiers: 0 garlic and ginseng; 50 mandrake, nightshade, blood moss; 100 grave moss, nox bloom, dragon's tongue. Exotics at 150 are a stub row with no patches. Finds go to a per-character ledger, and a pick can drop a seed.
3. **The reagent lane.** Five plant types appended after the stock 43. They cross only each other. Strain tier 0 to 16 runs Iron to Celestial and shows as the metal's hue. Bowls stay at OSI pace. Mature reagent plants yield every day without running out. All mounds of a bed share water, potions, tending and the harvest. Stock plants pass through every hook unchanged, and a fact holds that.
4. **Processing.** Double-click raw herbs: 5 become a bundle. A bundle opens into 10 reagents, up to 15 at 200. Two bowls and a six-plot bed at no skill make 36 herbs, so 7 bundles, 70 reagents a day (a fact holds it between 50 and 100).
5. **Neglect.** Grace is 2 days, plus up to 5 at 200. Past it, health falls but never to death. Each further grace length past that drops one strain tier. Tending resets it all.
6. **Alembic ties.** Types and strains need an Order rank to plant. The herb table gives a bowl and seeds once per character, and sells a raised bed deed for gold (5,000). "Green Thumb" is the first-harvest achievement.
7. **Lessons.** The Camping lesson adds a Herbalism step with a wild garlic prop and lent skill, on both branches. P802 is still in the queue, not merged, so this covers only the Camping point it lists.

**Saves (D40).** `ReagentSeed`, `RawHerb`, `ReagentBundle`, `HerbPatch` and `AlembicHerbTable` use the source generator. A plant's tier and neglect clock live in `HerbalStore`, a versioned `GenericPersistence` keyed by plant serial that fails loudly on an unknown version. So no engine type changes its save, and later phases add fields by version.

## Decisions I made

The P260 and P392 questions were never answered, so I took the research's recommended answer unless noted:

- Reagent and stock plants don't cross (U47).
- Strain tier is its own value, not `PlantHue` (U48).
- Reagent plants are perennial (U49).
- Reagent beds have slow upkeep at a third of the bowl's malady rate (U50).
- Blood moss uses the fern art (U59).
- The Alembic takes the higher of its two skills (U52).
- Stock reagent spawners stay (U53).
- **Not the research's answer:** the bed deed is sold at the herb table, not a Carpentry recipe (U60). The prompt asks for an Alembic starter, and it's one line to move.
- **Not asked:** Herbalism isn't a starting skill at character creation (U51).
- **My own design:** inside the lane, maladies cut the harvest instead of hurting the plant, so potions still pay and neglect is the only thing that costs health.
- **Left out of phase 1:** Scholar box seeds, the 2x bed speed, and the Cooking and Healing side uses. `HerbalLane.GrowthDelay` is the speed hook.

## Tests

`server/tests/Misc/HerbalismVerification.cs`: 52 test cases. They cover skill windows, respawn, bowl and bed growth and yield, crosses and mutation, processing amounts, neglect windows, gating, save and load of every new type, and the settings file.

- **Red:** the facts were written alongside the code, so I broke the code on purpose. 48 breaks (`mutants.txt`, `mutants2.txt`, `mutants3.txt`), and every fact went red at least once. One break first went unseen (too few herbs), so I tightened that fact and saw it red. One break failed to compile and was rewritten.
- **Green on main:** `sl-modernuo:cc-p804`, 3,175 tests passing, `EXIT=0`, 197 patches.
- **Green on the isle:** `sl-modernuo:cc-p804-isle`, 2,918 tests passing, `EXIT=0`, 180 patches.
- **Existing facts changed, by design:** Camping's props and steps, the total skill cap, the Alembic's skills, the achievement counts, and the fixed `58 * 2000` in the craft ceilings.
- **`latest` was not moved.** The shared Test Shard was not touched.
- **One isle gate failed** on `AKilledNonBondedPetPaysNoImbueKillEffect`, the random Butcher's Eye bug from P800 (log kept). It passed on the next run. It's still not fixed.
- **Package facts on main:** 27 of 28 pass, including 2 new ones. The failure is `TheCommunityArtRecords...` ("the layout has 36 rows"). This work doesn't touch that art, but I didn't run it on clean main, so I can't say it was already failing.

## Proof in the client

Private shard on 2596, private TazUO with patch 0011.

- **`notes\cc-P804-shots\skills\skills-window.jpg`:** Herbalism in the skills window under Miscellaneous, with the client's own group code placing it. The rig cut the list to that row in memory, because the window can't be scrolled here.
- **`notes\cc-P804-shots\final\`:** 5 checks pass in `walk.log`: the client knows the skill, a wild patch stands there, picking gives raw garlic, herbs process into a bundle, the table stands in the hall. Shots 1 to 10 run from the patch to the bed, and I looked at the patch, picked, bundle, starter and bed shots.
- **`final\restart.log`:** a real restart prints `0 placed, 23 already there`, so seeding is idempotent on a real load. `final\isle-start.log` shows the isle image seeding on first start.

**Limits of that proof:**

- **The bed shot is staff-placed in the open**, with the real classes. A house needs its own rig. Growth, yield and tending of a bed come from facts, not the client.
- **Not played in the client:** a full bowl from seed to harvest (nine real days; facts drive it), a cross, the Camping lesson, and the bed deed purchase. **The purchase has no fact either.**
- **The shots ran on the final main image.** The isle image ran only its first start, not the shots.
- **Package facts didn't run on the isle copy:** that worktree lacks the built `sl-anim7.bin`. The change is the same.
- **Client patch 0011 was built on main's patch set only.** It applies to the same pinned file on the release, but I didn't run a release client build.
- **`[self set Skills.Herbalism.Base 30` had no effect on the proof character:** it stayed at the proof shard's 100, so low-skill picking wasn't shown in the client. Facts cover it.
- **The camera is the rig's.** The art of a mandrake plant in a bed is small, and a strain's hue on a grown plant wasn't shot in the client; a fact holds it.

## For Chase

1. **Release to testers, after the merge.** Apply `notes\cc-P804-tools\p804-release-isle-20261028.diff` to `release/isle-20261028`, build, and move the shard. It applies cleanly to the release tip `e8d210c`, and the same tree built green as `sl-modernuo:cc-p804-isle`. P799 and P802 have not reached the release, so it isn't on top of them, and P800's isle diff isn't there either. Expect `CHANGELOG.md` and `VERSION` conflicts, and any release version bump to settle in order.
2. **The next player package needs:**
   - `client\patches\0011-unplaced-skills.patch`: a rebuilt client. A skill no saved group lists goes to Miscellaneous.
   - `player-package\payload\app\Build-UoOverrides.ps1`: writes `Herbalism` into slot 58 of the player's own `skills.mul` and `Skills.idx` copies. The stamp format changed, so everyone rebuilds that part once.
   - **Without the package:** nothing breaks. The client drops the unknown skill silently, and picking and growing still work, but the skill isn't in the window.
3. **Fix four spots.** They have no open ground within 8 tiles, so no patch appears: `Trammel:2100:1100`, `2150:1150`, `3550:2750`, `3990:2860`. The log names them, and the fix is an edit to the file's `Patches` list. All 27 were picked by hand without checking the map, so their biomes are approximate; New Haven's are near the yard. Please have someone look.
4. **Mainland patches sit on Trammel only.** Felucca has none.

## Phases 2 to 4, sketched

- **Phase 2, garden kit and upkeep.** The four categories as crafted items (Light, Water, Soil, Shelter), best per category, found by a proximity scan in `HerbalLane.GrowthDelay`. Herbalism alone up to 2x, the full kit 4x, bowls never. Structures wear slowly; consumables (a supply bin, a dose a week) give the top half of the bonus. Rain barrel and scarecrow extend `GraceDays`. New `HerbalRecord` fields go in by version.
- **Phase 3, garden familiar.** Needs the kit's bins and a seed vault. The sprout or gnome at the end of an Alembic quest line, bound to the house, with tasks by tier. While its bin is stocked it stamps `Tended`. It replants only the same strain from the vault, so breeding stays with the player.
- **Phase 4, yard tool and public plots.** `RaisedGardenPlantItem.IsUsableBy` and the seed target need a yard and plot rule, since both demand a house today. A yard region and budget by house size (U56), then town plots rented in Drams, with warnings and the U57 expiry rule.

## Found while here (not fixed)

- **Memory rule slip.** One shot run started at 2.4 GB available, under the prompt's 3 GB line: my check printed the number but didn't stop the run. It finished without trouble, and every later run checks and stops under 3 GB.
- **P800's tools folder isn't on this branch** because the branch predates that merge, so its rig came from P794's.

## Files

- **ShatteredLegacy:**
  - New: `server/customizations/Herbalism/` (3 files), `server/tests/Misc/HerbalismVerification.cs`, `server/patches/` (`Skills-herbalism`, `skills-json-herbalism`, `FeatureFlagManager-skill-count`, `Plants-herbalism-lane`), `client/patches/0011-unplaced-skills.patch`.
  - Changed: `docker/uo/apply-patches.sh`, `Build-UoOverrides.ps1` and its tests, `ClusterFAchievements.cs`, `ClusterFGuildStarterPath.cs`, `ClusterFGuildSystem.cs`, `RaisedGardenPlantItem.cs`, `TutorialStations.cs`, `TutorialTradeTrials.cs`, five existing test files, `CHANGELOG.md`, `VERSION` (main `2026.11.05.4`, release `2026.11.03.2`).
- **shard-migration:** this file, `notes\cc-P804-tools\`, `notes\cc-P804-shots\`.
- **To remove after the merge:** `git -C D:\UO\golems\Iron\ShatteredLegacy worktree remove --force D:\UO\golems\Iron\p804-isle`, and the private client at `D:\UO\golems\Iron\p804-client`. The folder `notes\cc-P804-shots\run1\` is an earlier run and can go.

P804 DONE
