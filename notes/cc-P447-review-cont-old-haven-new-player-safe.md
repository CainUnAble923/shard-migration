# P447: Old Haven new player safety review (P189)

Reviewed 2026-10-22. Notes only. No code or tests changed.

Read both work copies' AGENTS.md, the direction decision, task list, and `notes/cc-P189-cont-old-haven-new-player-safe.md`. No separate P189 Codex review was found beside it; also read P425's entrance review and P443's skill-gain review, and do not repeat their findings or P189's documented deviations.

Code paths are relative to the ShatteredLegacy work copy. `Pinned/` means `D:/UO/ModernUO-pinned/`, verified at `d4531cd94b739613155225c234900de9f47d2c88`. Risks below describe source-traced scenarios, not reproduced player incidents.

## Findings

1. **risk | `Pinned/Projects/UOContent/Items/Containers/TrappableContainer.ExecuteTrap.cs:88`**: A non-Young mage can leave a Magic Trapped box for a Young player to open in Old Haven, where the trap calls `Damage` directly without checking Young or combat permission; `Spells/Second/MagicTrap.cs:38` sets its damage to 10-50, and P189's region adds no damage filter. Close the player-created container-trap path for protected Young players, preserving intended dungeon traps, and add a cast/drop/open regression case with an ordinary Young victim.

2. **risk | `Pinned/Projects/UOContent/Misc/Notoriety.cs:224`**: A non-Young guildmate, guild ally, or guild enemy can attack a Young player in Old Haven, including through a controlled pet, because the guild exception returns true before the player restriction and never checks Young. Document this inherited guild-combat exception or add a scoped Young protection rule for Old Haven, with guild and pet cases; joining is possible through a non-faction guild and the existing invitation explicitly warns that acceptance makes the player attackable, so this is a safety-policy risk rather than a new P189 regression.

3. **risk | `server/customizations/ClusterFOldHavenSeeder.cs:168`**: Retirement skips an unowned Vorlak at the Rootdeep entrance `(3619,2620)` or eastern training edge `(3690,2500)`, because `IsOldHavenArea` at `:351` stops at y 2600 and x 3680 while the training area extends through y 2650 and x 3703; a surviving Vorlak still ignores Young protection. Include the training area when identifying dangerous strays, retaining the existing exclusions for controlled creatures and creatures at unrelated homes, and add southern/eastern boundary cases to S2.

4. **risk | `server/customizations/Regions/ApprenticeTraining.cs:191`**: The gain that crosses 50 during pinned acceleration can receive both multipliers: pinned applies its x2-5 first, its synchronous skill-change notification completes the quest and clears `AcceleratedStart`, and P189 then sees an expired timer while subtracting that gain to recover the below-50 eligibility value. Capture whether acceleration applied before executing the underlying gain and pass that state to the apprentice hook, with a regression starting at 49.9 during acceleration; A4 tests acceleration and crossing 50 separately and misses their interaction.

5. **bug | `server/customizations/Regions/ApprenticeTraining.cs:168`**: Canceling a quest while its training buff is displayed leaves that untimed buff and `_buffed` membership behind until a region exit or a later positive skill gain, since cancellation has no refresh hook and zero-gain attempts return before refreshing. Refresh on quest removal and relevant skill changes, and cover canceling in place with skills locked; this is a stale training indicator, not continued Young protection or a continued gain bonus.

6. **nit | `server/customizations/Regions/ApprenticeTraining.cs:297`**: The west extension starts at x 3546, but pinned `Distribution/Data/regions.json:1523` ends New Haven at exclusive x 3545, leaving `(3545,2580,0)` outside both regions and delaying the advertised training transition by one tile. Start the extension at x 3545 and test x 3544/3545/3546 on the walk; Haven Island still covers the gap, so this is a training boundary defect rather than a hole in Young protection.

7. **risk | `server/tests/Regions/OldHavenNewPlayerSafeVerification.cs:179`**: A1 checks region names at Z 0 and A4 uses Young only to test gain eligibility, so P189's suite does not assert that stock undead cannot initiate attacks, an unrelated veteran and pet cannot attack, or backpack theft is rejected inside the new region. Add those checks through the real combat/theft entry points at the rectangle seam and entrance, plus a same-location Young-expiration transition; the existing global duration tests verify flags but would not catch a region-specific protection regression.

## Supporting traces and checks with no finding

- Direct backpack theft from a Young player is rejected at pinned `Projects/UOContent/Skills/Stealing.cs:119`, before item transfer. No bypass of that check was found in the reviewed P189 paths; property left on the ground is outside that ownership protection.
- Unrelated player attacks are rejected by pinned `Projects/UOContent/Misc/Notoriety.cs:236`. Controlled pets resolve their master at `:170`, then reach the same restrictions unless the guild exception applies; uncontrolled creatures reach `CheckYoungProtection` at `:218`.
- The two training rectangles meet at exclusive/inclusive y 2543 without a missing row. Both lie inside pinned Haven Island (`Distribution/Data/regions.json:1504`), and both `ApprenticeRegion` and its parent inherit `BaseRegion.YoungProtected == true` (`Projects/UOContent/Regions/BaseRegion.cs:43`). No additional surface protection gap was found at their seam or around the entrance.
- No new indefinite Young protection was found. `ClusterFYoungPlayer.Duration` is 336 hours of account play, the Account patch uses `YoungPlayed`, and `YoungPlayerVerification.At336HoursCheckYoungRemovesYoungFromEveryCharacter` covers its boundary; the region does not set or renew Young. The Fountain's clock reset is a separate P192 feature, not a P189 timer change.
- The stacking risk follows pinned `Skills/SkillCheck.cs:273`, `Projects/Server/Skills.cs:193`, `Mobiles/PlayerMobile.cs:3804`, `Engines/ML Quests/MLQuestSystem.cs:504`, `MLQuestEntry.cs:166`, and `Objectives/GainSkillObjective.cs:144`. New Haven quests have report-back messages, so completion does not immediately set `ClaimReward`; P189's `Training` can still return their area for this final gain.
- Cancellation follows pinned `Engines/ML Quests/MLQuestEntry.cs:449` and `Objectives/GainSkillObjective.cs:135`; neither clears the custom region buff. The rectangle converter preserves the supplied endpoints (`Projects/Server/Json/Converters/Rectangle3DConverter.cs:159`), and containment uses exclusive ends (`Geometry/Rectangle3D.cs:137`).

## Scope and verification limits

Read the P189 seeder, apprentice region, skill-gain hooks, Drelgor, retained mage and Vorlak classes, `OldHavenNewPlayerSafeVerification.cs`, the changed Drelgor/Vorlak test in `CCP129CreatureVerification.cs`, and the console's retirement-command classification fact in `scripts/tests/Shard-Console.Tests.ps1`. Supporting reads covered Young status and duration tests, its patches, the Burrows combat tests, pinned guild invitations, container-trap creation/opening/damage, combat permission, theft, region geometry, and quest completion/cancellation.

P189 already records that retirement requires a staff command on an existing world, mixed spawners are deliberately kept, training is quest-based rather than Young-based, and pinned's initial acceleration remains available outside the region. Those are not new findings here; P443's total-cap finding and P425's entrance/teleporter findings are also omitted.

No C# fixture, PowerShell test, build, game client, container, or live service was run or contacted. No tests were added, so no red/green claim is made; actual world spawners, guild membership, reachable map tiles, applied cleanup, and the runtime stacking scenario remain unverified. The progress reporter completed with work-copy path overrides and `--dry-run`, suppressing its `progress.json` write in memory to keep this task notes-only.

P447 DONE
