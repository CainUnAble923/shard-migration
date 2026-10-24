# Codex review: P535

CC task P535: skills design against what is built. Reviewed by Codex (`codex exec review`, read-only) after P535 DONE and before the Golem's commit, 2026-10-24 06:17.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.88). The notes largely fulfill the requested comparison and preserve the docs-only scope. However, they omit a verified conflict between an explicit Lumberjacking design decision and the implemented axe-damage clamp.

- **medium** [P2] Include the axe-damage clamp in the design comparison (`notes\cc-P535-skills-design-vs-build.md:81`)
  The Lumberjacking comparison omits a concrete design/build difference: `notes/skills-design.md` explicitly approves leaving the axe bonus uncapped (+50 percent at 200), but `BaseWeapon-axe-bonus-osi.patch`, registered in `apply-patches.sh:576`, routes it through `ClusterFSkillClamps.AxeLumberjackingSkill`, limiting players to 100 skill and a 30 percent bonus. Add this discrepancy and its later P67 history, distinguishing the implemented bound from the original decision as the report does for potions and parrying. Otherwise, this approved combat reward disappears from the reconciliation.

(1.6 minutes, 474,066 tokens)
