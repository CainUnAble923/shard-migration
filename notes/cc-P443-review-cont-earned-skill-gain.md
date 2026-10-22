# P443: review of earned skill gain (P191)

Reviewed 2026-10-22. Notes only. No code or tests changed.

Read both work copies' AGENTS.md, the direction decision and task list, and `notes/cc-P191-cont-earned-skill-gain.md` before reviewing the implementation. No separate P191 Codex review was found under `notes/`; also checked the P202/P204 integration notes and the later P189 apprentice implementation so its documented deviations are not presented as new findings.

## Findings

1. **risk | `server/customizations/ClusterFSkillGain.cs:387`**: With anti-macro disabled, a player can repeatedly taste the same ordinary food in a safe location all the way to their skill cap, and the Hiding row at `:333` similarly permits stationary training in a safe public spot outside a friend's house; neither path requires a harder target, consumed resources, or danger above 100. Add a targeted repetition limit or a harder training requirement for these extended rows, with repeated-food and stationary-hiding regression cases, while preserving their ordinary success results.

2. **risk | `server/customizations/Regions/ApprenticeTraining.cs:234`**: If `clusterf.skillCaps.totalCap` is configured below the sum of individual caps, the source permits an apprentice bonus to overshoot it because `:228` checks only whether the total is already full and `:234` clamps only to the individual cap: with no down-locked skills, a total of 699.8, a 700 cap, and an ordinary 0.1 gain multiplied by four, the total becomes 700.2. Limit the extra amount to the remaining total-cap room after any lowering and add that boundary case under the recommended two attempts; this is a source-traced risk, not a reproduced runtime defect, and the default sum-of-individual-caps setting does not expose it.

3. **risk | `server/tests/Skills/SkillGainRateVerification.cs:178`**: The Tactics model rolls every three seconds independently of weapon hits, but pinned `Items/Weapons/BaseWeapon.cs:888`, `:1763`, `:2590`, and `:2524` put its ordinary roll on the hit path, so the notes' 0.83 hours to 100 assumes 1,200 successful hits per hour while the neighboring Swordsmanship model assumes 1,200 swings with about half hitting against equal skill. Drive both skills from the same swing stream or explicitly label these as different combat scenarios, then regenerate the Tactics hours for the described three-second weapon; at a fixed 50 percent hit rate and three seconds per swing, that quoted time doubles.

4. **nit | `notes/cc-P191-cont-earned-skill-gain.md:12`**: The headline says Imbuing reaches its 140 ceiling in 3.5 hours, but its table's 3.51 hours is time to 120, and `server/tests/Skills/SkillGainRateVerification.cs:234` has no 140 milestone. Correct the headline and add a 140 milestone before publishing a measured time to that ceiling.

5. **nit | `notes/cc-P191-cont-earned-skill-gain.md:215`**: A fivefold chance factor does not make training five times faster once the roll saturates: pinned `Skills/SkillCheck.cs:145` compares against a random value below one, so P191's roughly 0.36 to 0.49 per-attempt gain chances near skill 100 become guaranteed gains, roughly 2 to 3 times the original rate rather than five. Describe the crystal as a chance multiplier subject to saturation, and measure actual time savings with the crystal instead of inferring them from R3's single held roll.

6. **risk | `server/tests/Skills/SkillGainRateVerification.cs:281`**: R1 supplies both configuration keys before calling `Configure`, and R3/R4 install their own rate constants through `Hook`, so reverting the production defaults to three attempts and fivefold amount would leave P191's tests passing. Add a case with both keys absent that checks the production defaults are two and one and observes the resulting gain, restoring the previous configuration afterward.

7. **risk | `server/tests/Skills/SkillGainRateVerification.cs:437`**: S1 only asserts that each modeled skill reaches 50, so a broken Blacksmithy or Mining climb above 50, or an incorrect Magery or Imbuing ceiling, can still produce a passing rate report; R2 exercises only Swordsmanship under the separate twofold-amount setting. Assert every reachable milestone for each model and explicitly check that ceiling-limited models stop gaining at their stated ceilings under the recommended rate.

## Checks with no new finding

- The production defaults are two attempts and a onefold amount at `server/customizations/ClusterFSkillGain.cs:39-40`. P191 already records that existing stored settings remain unchanged until edited, so that is not a new defect here.
- No individual-cap or skill-lock bypass was found in the reviewed paths. Ordinary and repeated gains reach pinned `Skills/SkillCheck.cs:248-280`, which requires an up lock and clamps to the skill's cap; the apprentice addition also clamps to that cap. Existing coverage includes `SkillGainPastStockCeilingVerification.G1/G5` and `SkillBonusAboveCapVerification.SkillGainAtTheCapStillDoesNotRaiseBase`.
- No new Young eligibility or apprentice stacking defect was found. Young status alone grants no gain multiplier; `ApprenticeTraining.Training` checks the matching quest and threshold, `InRegion` checks its area, and `OnGain` skips its bonus while pinned acceleration is active. `OldHavenNewPlayerSafeVerification.A4` already checks Young alone, a non-Young quest holder, the wrong skill, the 50-point boundary, and acceleration stacking.
- P189's notes already correct P191's claim that ServUO's apprentice region only supplies a buff, and explicitly document retaining pinned's timed acceleration outside the region. Those are not new findings in this review.

## Evidence and verification limits

The review read P191's changed `ClusterFSkillGain.cs`, `Engines/ML Quests/Items/NewHavenQuestBoard.cs`, `SkillGainRateVerification.cs`, and changelog entry. Supporting checks covered the gain-row and cap tests named above, `SkillGainRowKeysVerification.cs`, `OldHavenNewPlayerSafeVerification.cs`, the craft gain window and related tests, `ClusterFSkillCaps.cs`, `ClusterFYoungPlayer.cs`, `Regions/ApprenticeTraining.cs`, the Test Crystal scalar and SkillCheck patch, and the current Imbuing check.

Pinned source was verified at `d4531cd94b739613155225c234900de9f47d2c88`. Pinned paths above are relative to `D:/UO/ModernUO-pinned/Projects/UOContent/`; the skill setter was also checked at `Projects/Server/Skills.cs:174-193`, where it updates the total without enforcing a total cap. Food repetition was traced through pinned `Skills/TasteID.cs:21-51`, which leaves the food unchanged; Hiding was traced through `Skills/Hiding.cs:31-73`. Both reach the extended rows and the same gain pipeline, whose anti-macro default is disabled at `Skills/AntiMacroSystem.cs:96`; its bypass is at `:190-194`.

The safe training paths are inherited behavior that P191's rate reduction leaves available, not exploits introduced by its two default changes. Actual shard anti-macro settings, active rate settings, target availability, in-client timing, and the conditional total-cap example remain unverified. No test, build, game client, container, or live service was run or contacted, as this task requests a notes-only review with no lane tests. No tests were added, so no red/green claim is made.

Ran `tools/progress.py --dry-run` with both path overrides set to these work copies; it exited zero. Restored its `tools/progress.json` side effect byte for byte, leaving the review note as the only intended change.

P443 DONE
