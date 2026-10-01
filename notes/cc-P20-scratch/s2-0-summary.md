## 2. Every skill past 120

### 2.0 Summary, one row per skill (58 rows, counted)

"Breaks from" is the lowest of 120 / 300 / 500 / 1000 at which the per-skill tables (2.1 to 2.5)
show a breaking use; "-" means the skill only scales or clamps up to 1000. "Gain ceiling" is the value
above which no use can raise the skill (section 3). Classification is the sub-reports'; I compiled
this table from their tables and BREAKS lists. Where a sub-report's table did not write the word
"breaks" but its BREAKS list names the use, I followed the list (Tracking, Animal Lore, Alchemy,
Tinkering, Lumberjacking, Mining).

| # | Skill | Breaks from | What breaks (worst) | Gain ceiling | Recommendation |
|---|---|---|---|---|---|
| 1 | Swords | 1000 | creatures stop hitting (defender hit chance, 5.9% at 1000) | ~220 | soft-cap hit-chance input past 120 |
| 2 | Macing | 1000 | same | ~220 | same |
| 3 | Fencing | 1000 | same | ~220 | same |
| 4 | Archery | 1000 | same | ~220 | same |
| 5 | Throwing | 1000 | same; not counted in the special-move mana discount | ~220 | same |
| 6 | Wrestling | 1000 | same | ~220 | same |
| 7 | Tactics | 500 | damage bonus outside DI caps (x5.9 total at 300, x8.2 at 500) | none (follows cap) | soft-cap past 120 |
| 8 | Anatomy | 500 | same, plus bandage term | none (follows cap) | soft-cap damage term |
| 9 | Parry | 300 | 187% block with Bushido 300 (live); 100% with shield at 380 | 380 | hard-cap block chance, soft-cap Parry |
| 10 | Bushido | 300 | Feint 100%+ from 237 (live); Confidence and HE heals quadratic; permanent Evasion at 400 | 120 | new effects past 120, cap Feint/heals |
| 11 | Focus | 1000 | regen outside the 18/24 caps | 200 | soft-cap |
| 12 | Arms Lore | 500 | uncapped exceptional armor resist bonus | 100 | cap the armor bonus |
| 13 | Magery | 500 | Earthquake 67 tiles, Greater Heal 400, fields 5 min | 120 | soft-cap radius, duration, heals |
| 14 | Evaluating Intelligence | 1000 | spell damage x9.3 from EI alone (x19.7 with Inscription); curse 96% | follows cap | soft-cap damage term, cap curse ~25% |
| 15 | Resisting Spells | 300 | always resists an equal-skill 300 caster; immune at 1000 | 130 | replace resist curve with one under 100% |
| 16 | Meditation | 1000 | 8.7 mana/s, casting no longer mana-limited | follows cap (active) / 200 | soft-cap |
| 17 | Inscription | 500 | spell damage integer bug; Reflect/Protection maluses become bonuses | 150 | fix bug, clamp maluses at 0, soft-cap |
| 18 | Necromancy | - | clamps at 120 | 120 | new effects past 120 |
| 19 | Spirit Speak | 500 | Strangle quadratic, Revenant immune, heals 250 | follows cap | soft-cap as a power stat |
| 20 | Chivalry | - | clamps 120-230 | 115 | new effects past 120 |
| 21 | Spellweaving | 1000 | Attune Weapon 315 absorb | 117.5 | soft-cap |
| 22 | Mysticism | 500 | Nether Cyclone 152% drain, heals 250-500 | 120.5 | same soft-cap as EI |
| 23 | Imbuing | 1000 | only through Mysticism damage | 140 | soft-cap the Mysticism read |
| 24 | Ninjitsu | 300 | Feint from 237; Surprise Attack divide by zero; form regen past cap | 137.5 | clamp malus and Feint |
| 25 | Hiding | 120 | hide while being hit from 118 | 100 | clamp combat range at 8 |
| 26 | Stealth | 1000 | 200 steps (mild) | 60 / 142 | soft-cap steps |
| 27 | Detect Hidden | 300 | 30-100 tile scans; guards cannot reveal Hiding 121+ | 100 | cap radius; scale guard DH |
| 28 | Snooping | - | clamps | 100 | let it scale |
| 29 | Stealing | 300 | never caught from 150; 4,500 gold a try at 300 | 127.5 | cap caught chance and weight |
| 30 | Lockpicking | - | clamps at 140 | 140 | let it scale; new locks |
| 31 | Remove Trap | - | scales (counter to tinker traps) | TrapPower+30 | let it scale |
| 32 | Poisoning | 120 | Infectious Strike level-up certain, and a pinned list-index bug | 100 | fix the pinned bug (ours to patch or report) |
| 33 | Healing | 300 | 138 HP per bandage at 300, 0.7 s delays; negative self delay above Dex 220 | 120 | soft-cap heal, floor delays |
| 34 | Veterinary | 500 | 225 HP/s on pets at 1000 | 120 | same curve as Healing |
| 35 | Begging | - | no effect past 100 | 100 | let it scale |
| 36 | Forensic Evaluation | - | no effect past 100 | 100 | let it scale |
| 37 | Animal Taming | - | clamps (control 99%) | 157 | let it clamp |
| 38 | Animal Lore | 300 | stable slots 68 at 300; pet heals 101-174 per 2 s | 120 | cap slots, soft-cap heal term |
| 39 | Herding | - | clamps | 146.1 | let it clamp |
| 40 | Musicianship | 300 | uncapped difficulty reduction: root cause of certain bard success | 120 | soft-cap the reduction |
| 41 | Peacemaking | 300 | certain success; area range 28 tiles at 300 | 120 area | cap success and range |
| 42 | Provocation | 300 | certain success; Fire Horn 216-400 at 300 | 180-200 | cap success; clamp Fire Horn inputs |
| 43 | Discordance | 300 | -100 effect at 300: zero resists, divide by zero in swing speed | 175-195 | hard-cap effect at 28 (OSI at 120) |
| 44 | Tracking | 300 | 310 tile search at 300; feeds Surprise Attack malus | 100 | soft-cap range |
| 45 | Item Identification | - | no effect past 100 | 100 | F-14 repurposes it (Appraisal) |
| 46 | Taste Identification | - | no effect past 100 | 100 | let it clamp |
| 47 | Camping | - | no effect past 100 | 100 | let it clamp |
| 48 | Cartography | - | cosmetic map bounds only | 130 | clamp map distance |
| 49 | Alchemy | 300 | Greater Conflagration 76-83/s at 300; gem bypasses cap | 150 | soft-cap potion enhancement |
| 50 | Blacksmithy | 300 | our code: no gain source 295-300, Celestial unreachable, large BOD lock-out | ~295 | fix our BOD windows first |
| 51 | Bowcraft/Fletching | - | clamps | 130 | content past 130 or let clamp |
| 52 | Carpentry | - | clamps | 140.3 | same |
| 53 | Cooking | - | clamps | 130 | same |
| 54 | Tailoring | - | clamps | 144 | same |
| 55 | Tinkering | 120 | trap damage Tinkering/10 uncapped: 300-900 at 300 | 130 | cap trap level at 10 |
| 56 | Mining | 300 | our code: salvage ingot dupe above ~143 | 155 ore / 400 sand | restore the cap in SmithGuildSalvageBag |
| 57 | Lumberjacking | 300 | axe +70% damage outside the DI cap at 300 | 148 | soft-cap at the GM value |
| 58 | Fishing | 1000 | rares on 65% of casts, serpents on 47% | 100 | cap rare chances |

Counts from the table: breaks from 120: 3 (Hiding, Poisoning, Tinkering); from 300: 17; from 500: 8;
from 1000: 13; never: 17. Total 58.

Common shape of the fix: almost every break is one of three things.
- **A chance that passes 100 percent** (block, resist, bard success, never caught, hide in combat).
  Hard-cap the final chance at an OSI-like ceiling.
- **A magnitude linear or quadratic in skill** (damage, heals, regen, range, radius, duration). Feed it
  an effective skill that follows a soft curve past 120.
- **A subtraction that crosses zero** (Hiding range, Discordance and Surprise Attack in the swing and hit
  formulas, Reflect/Protection maluses). Clamp at the OSI value; these are the ones that can throw.

The detailed per-skill tables follow, one file per group, as written by the sub-agents.
