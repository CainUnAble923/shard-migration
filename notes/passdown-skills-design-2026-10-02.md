# Pass-down for the skills design chat (2026-10-02)

Written by the overseer for a new chat whose only job is **skills**: go through all 58 skills, one at a time, and map
out how each becomes relevant on this shard, how it synergizes with others, and how it can gain all the way to the
cap. Chase asked for this (2026-10-02, 11:19). It is design work in conversation with Chase, not building.

## What this chat produces

- **One design file:** `D:\UO\shard-migration\notes\skills-design.md`, one section per skill, filled in with Chase,
  one skill (or a small group) per sitting. Keep a status table at the top (not started / in discussion / decided).
- **Chase's decisions recorded as he makes them**, in that file, marked with the date.
- **Nothing built, nothing in `D:\ShatteredLegacy`.** When a group of skills is decided, tell Chase; the overseer
  turns decided groups into numbered cc-P prompts (check `D:\UO\cc-prompts\` and `completed\` for the next free
  number first; two chats collided on P29/P30 on 2026-10-02). Feature-sized ideas that are not skill design go to
  the features chat's `docs\feature-queue.md`, which that chat owns.

## Per-skill template

For each skill:
1. **Today:** what it does in pinned ModernUO (7c9215d97, `D:\UO\ModernUO-pinned`) and in ours
   (`D:\ShatteredLegacy\server\customizations`), with file:line. Read the code; do not trust notes or memory.
2. **Gain path:** every gain call and its `maxSkill` ceiling (cc-P20 already tabled these). Does it gain to the
   F-12 cap of 200 by play? If not, what use should train it past its ceiling (pattern: our `Meditation.cs:92`,
   a ceiling that follows the cap).
3. **What breaks or plateaus above 120** (cc-P20's per-skill breaks at 150/200/300).
4. **Relevance:** why a player would train it here. What it is for in our systems (guilds, the League, F-12 levels
   and loops, crafting, the New Haven dungeon).
5. **Synergies:** which other skills it pairs with, and what the pair unlocks.
6. **Proposal and open questions** for Chase. Ported behavior stays faithful unless Chase decides otherwise; every
   change is a deviation to register.

## Read first

- `notes\f12-levels-loops-caps.md` (also `claude/f12-levels-loops-caps.md` in the project): max level 200, skill cap =
  max level, total = 58 x max level, six loops, **loop memory** (faster gain up to a skill's previous peak, capped
  growth, live only), **no stat ceilings**, and "Still open" item 5 (this work).
- `notes\cc-P20-skill-scaling-research.md` (236 KB): all 58 skills past 120. **39 of 58 cannot gain past about 160 by
  use** (fixed `maxSkill`, `SkillCheck.cs:58-61`); 41 of 58 break by 1000; recommendation 3 at `:87`.
- `notes\cc-P25-stats-above-125-research.md` and `notes\p25-decisions-2026-10-02.md`: stats are uncapped (500 raw),
  which changes every stat-fed skill formula.
- **Worked example: F-26, Arms Lore** in `docs\feature-queue.md` (what it does today, why it cannot gain past 100,
  the proposed new jobs). Use it as the model for depth. F-27 (rare Self Repair) pairs with it.
- Memory: `areas/shattered-legacy.md` for Chase's vision (UO meets Dungeon Crawler Carl, cultivation, LitRPG, "Stubborn
  Skill Grinder with Time Loops"; one character that can do anything; base game first, races last).

## Rules that have bitten this project

- **Verify before asserting; cite file:line.** The repeated failure is asserting from a prompt or memory. The live
  stat cap was 500, not 125, in every note until cc-P25 read the config.
- Run git in Chase's repos only with `--no-optional-locks`.
- Chase prefers concise, actionable answers, American spelling, and no em dashes anywhere.
- When Chase brings a feature request, give feedback, suggestions and clarifying questions.

## Suggested order

Group by how much each group touches F-12 and the base game: crafting and gathering first (they already scale
through recipe and resource ceilings, so they are quick, and they feed guilds), then combat (weapon skills, Tactics,
Anatomy, Parry, Bushido), then magic schools, then utility and odd ones (Arms Lore is done as F-26; Begging, Spirit
Speak, Forensics, Camping, Remove Trap need the most invention).
