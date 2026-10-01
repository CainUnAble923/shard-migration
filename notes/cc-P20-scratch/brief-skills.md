# Common brief for the per-skill audit (cc-P20)

Read-only research. Do NOT edit anything except your one output file. No builds, no commits.

Context: Ultima Online shard on ModernUO. Expansion config is Endless Journey: Core.AOS, SE, ML, SA, HS, TOL all true, so evaluate those branches (not pre-AOS ones). Players can raise each skill to 300.0 today (live), and the design will allow 1000.0 per skill. Skill.Value (UOContent/Server Skills.cs) includes item/skill-mod bonuses on top of Base.

Sources:
- D:\UO\ModernUO-pinned\Projects : pinned ModernUO, the ONLY authority for engine behavior. Cite file:line, paths relative to D:\UO\ModernUO-pinned\Projects. Do not reason from ServUO names.
- D:\ShatteredLegacy\server\customizations and D:\ShatteredLegacy\server\patches : the shard's overrides and additions. Where one of ours replaces pinned behavior, say so and cite both. Five files there REPLACE the pinned file of the same basename: CharacterCreation.cs, CraftItem.cs, HammerOfHephaestus.cs, Meditation.cs, RegenRates.cs (in customizations). patches\Mining.cs and other non-.patch files in patches replace pinned too; .patch files are diffs against pinned. Grep customizations for each of your skills (e.g. "SkillName.Hiding", "Skills.Hiding", "Skills[SkillName.Hiding]") because shard systems read skills too (e.g. our extended ore chain reads Mining 0-300).
- NEVER read D:\ShatteredLegacy\server\uo (stale generated tree).

Gain mechanics you need (UOContent/Skills/SkillCheck.cs): CheckSkill(skill, minSkill, maxSkill) returns false with no gain if value < min, and returns TRUE WITH NO GAIN ROLL if value >= maxSkill (SkillCheck.cs:53-61, :161-169). Direct-chance checks return true with no gain if chance >= 1.0 (:84-87, :190-193). So for each skill, report its GAIN CEILING: the highest maxSkill (or the skill value where the direct chance reaches 1.0) across its uses, i.e. the value above which that use can no longer raise the skill. This matters as much as the effect formulas.

For EACH skill in your list produce a table:
| Use (what reads the skill) | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
with each of 120/300/500/1000 classed as:
- scales: keeps growing sensibly
- clamps: stops having any effect past some value (say the value). Harmless but points past it are wasted
- breaks: chance over 100 percent that matters, immunity, negative values, divide by zero, runaway damage/healing, success that can no longer fail, anything a player could abuse. Say exactly what happens with numbers.
Then one line: recommendation: let it scale / soft-cap with diminishing returns (suggest the shape) / give it new effects past a point (suggest what).
Be concrete with numbers (compute the formula at 120, 300, 500, 1000). Note where a value is also capped by something else (e.g. AOS caps on damage increase at 100 or 300 percent, resist cap 70) that limits the harm.
Cover every place the skill is read that matters for gameplay; minor cosmetic reads can be listed in one line. If a skill reads only via a generic path, say so.

Write ASCII only: no em dashes, no smart quotes, no unicode arrows. Mark anything you could not verify as "unverified".
