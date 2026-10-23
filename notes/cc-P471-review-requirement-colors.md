# P471: Review of requirement colors (P169)

Reviewed October 23, 2026. Notes only. Code reviewed at
`0f1871f0af413c2cd0df2e65dd64d66dac7aeee7`; pinned ModernUO was verified at
`d4531cd94b739613155225c234900de9f47d2c88`.

Read `notes/cc-P169-requirement-colors.md` first. No separate P169 review was found
beside it. The standing-based rank rule, Apprentice task bump, and promotion cap
were already recorded there and are not new findings here.

## Findings

1. **bug**: `server/customizations/ClusterFRequirements.cs:235` and `:238`,
   called from `server/customizations/JacobsReinforcedPickaxe.cs:287`.
   With an active Testing Token and a missing or exhausted source pickaxe, the
   footer says the unmet requirements are waived and enables Upgrade, but
   `JacobsReinforcedPickaxe.cs:335` still rejects a missing usable source;
   the T3 through T5 menus have the same disagreement, and the Hammer upgrade
   also refuses an exhausted source (`HammerOfHephaestus.cs:1316`).
   Keep the source-item requirement mandatory when computing the footer's waiver
   and enabled state, and cover an active token with an unusable source in a test.

2. **risk**: `server/customizations/ClusterFRequirements.cs:149`.
   With overlapping material costs, such as two `GuildCost.Of<IronIngot>(10)`
   entries and only ten available ingots, `Price` marks both lines green and
   allows an "All requirements met" footer even though payment rejects the
   combined bill (`server/customizations/GuildResources.cs:319`); the reviewed
   P169 menus use distinct ingot types, so this is a helper contract risk rather
   than a demonstrated current menu failure.
   Derive the display's available quantities from the same reservation plan as
   payment, and test that `AllMet` agrees with `CanPay` for overlapping costs.

3. **risk**: `server/tests/Misc/RequirementColorsVerification.cs:93` and `:149`.
   The menu fixtures set Base and Cap and keep their source tools in the pack,
   so they do not protect the skill text and colors against a regression from
   effective `Value` to `Base` or `Cap`, including bonuses above the cap.
   Add a T2 case with Mining Base and Cap at 70 and the +5 Jacob's Pickaxe equipped,
   assert the displayed 75 and green skill line, then move it to the pack and
   assert 70, a red skill line, a disabled button, and refusal of the stale press
   while every other requirement remains met.

4. **risk**: `server/tests/Misc/RequirementColorsVerification.cs:337`.
   The forged-button checks make several requirements fail together, so an early
   rank or currency refusal can hide a missing later check, while the rich menu
   checks at `:326` never press the action.
   Add cases with exactly one unmet requirement and assert its text, hue, summary,
   disabled action, and refusal without spending anything, plus a fully met press
   for each menu; the existing payment and League tests do not establish this
   display-to-handler agreement for all of P169's menus.

## What checked out

No new rank-color defect was found beyond P169's recorded standing-versus-rank
decision. The Hammer and Jacob's upgrade skill lines and handlers consistently
read `Skills[...].Value`, so no ignored skill bonus or extra cap clamp was found
in those paths. `ClusterFSkillBonusAboveCap` and its PlayerMobile patch control
whether modifiers obey the cap before the menus read that value.

The met and unmet hue and art mappings agree with their requirement states.
The League rank page checks `report.Blocker` before drawing requirements, and
its ordinary count checks use the same amounts as promotion evaluation.

## Files reviewed

Code paths from the P169 note:

- `server/customizations/ClusterFRequirements.cs`
- `server/customizations/HammerOfHephaestus.cs`, the restoration and upgrade gump
- `server/customizations/JacobsReinforcedPickaxe.cs`
- `server/customizations/JacobsProspectorPickaxe.cs`
- `server/customizations/JacobsDeepdelverPickaxe.cs`
- `server/customizations/JacobsWorldbreakerPickaxe.cs`
- `server/customizations/MinersCompactLiaisonGump.cs`
- `server/customizations/CrossGuildExchangeGump.cs`
- `server/customizations/Mobiles/Mule/MuleUpgrades.cs`
- `server/customizations/ClusterFLeagueRanks.cs`, reports and promotion evaluation
- `server/customizations/LeagueRegistrarGump.cs`, the Rank page and response path

Tests and supporting sources:

- `server/tests/Misc/RequirementColorsVerification.cs`
- `server/tests/Misc/LeagueLadderVerification.cs`, promotion and Registrar cases
- `server/tests/Misc/GuildResourcesVerification.cs`, payment and restoration cases
- `server/tests/Mobiles/Mule/MuleVerification.cs`, the upgrade path
- `server/tests/Misc/SkillBonusAboveCapVerification.cs`
- `server/tests/Misc/GuildMenuTemplateVerification.cs`, requirement rendering cases
- `server/customizations/GuildResources.cs`
- `server/customizations/CompactGoldHelper.cs`
- `server/customizations/DevTestingCrystal.cs`, activation check
- `server/customizations/ClusterFSkillBonusAboveCap.cs`
- `server/patches/PlayerMobile-skill-bonus-above-cap.patch`
- `server/patches/JacobsPickaxe.cs`, the +5 Mining bonus
- `D:/UO/ModernUO-pinned/Projects/Server/Skills.cs`, effective skill calculation
- `D:/UO/ModernUO-pinned/Projects/UOContent/Skills/SkillsInfo.cs`, skill setup

## Verification limits

This was a source and test-coverage review. Findings were traced through the
display and handler implementations, but runtime reproductions and client colors
remain unverified in this run. No tests were added or run, and no build, client,
shard, or Haven connection was used.

The required progress command ran with `--dry-run` and the work-copy path
overrides and exited successfully. It still rewrote `tools/progress.json`;
that generated change was restored so this task leaves only this review note.

P471 DONE
