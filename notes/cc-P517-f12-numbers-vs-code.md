# P517: F-12 numbers versus current code

Checked October 24, 2026. Notes only. No code or configuration changed.

**F-12 is not built as a player progression system.** The cap ladder helper matches
P282, and tutorial graduation now records loop 1. Player XP, the actual level reset,
per-loop player skill caps, scroll/reset transactions, reserve, and Keeper/Breaker
memory are still missing. A matching constant in a helper does not enforce a cap.

The largest differences are the flat player skill cap of 200 at every loop, the empty
reset hook, stock power scroll behavior, and the remaining effective-stat clamp of
500. P282 also carries historical descriptions that later work has overtaken.

**Sources and scope.** `S/` means the code work copy,
`D:\UO\golems\Valorite-tower\ShatteredLegacy`, at
`6f540be`. `M/` means the migration work copy,
`D:\UO\golems\Valorite-tower\shard-migration`, at
`668b31b751198e926e2507cff679c70cac87f00b` before these notes.
`U/` means read-only `D:\UO\ModernUO-pinned`, verified at
`d4531cd94b739613155225c234900de9f47d2c88`, matching
`S/docker/uo/Dockerfile:3`. Code values below are source defaults and behavior, not
claims about deployed configuration or a running character.

Read both `M/notes/cc-P282-*.md` files, the complete F-12 queue entry, and the revised
design that entry names. `M/docs/feature-queue.md:928` explicitly gives
`M/notes/f12-levels-loops-caps.md` precedence. P282's report points there for its
numbers. Its approved baseline also preserves the October 5 XP decisions. P282's
current-level gates and rewards are proposals, not approved implementation claims.

In the tables, `revised design:N` means
`M/notes/f12-levels-loops-caps.md:N`, `queue:N` means
`M/docs/feature-queue.md:N`, and `October 5 decisions:N` means
`M/notes/f12-decisions-2026-10-05.md:N`.

**Levels, loops, scrolls, and training caps**

| Number or rule | Design value and source | Current code value and file:line | Result |
| --- | --- | --- | --- |
| First and final caps | 50 at creation, 100 at loop 1, +5 to 200 at loop 21; revised design:3-5,39-49 | `S/server/customizations/Tutorial/ClusterFLoops.cs:31` returns exactly those values and holds at 200 above loop 21 | Match in helper only. No production caller of `MaxLevelFor` was found in customizations or patches. |
| Ladder size | 22 cap states, 21 resets, 20 scroll-gated entries; revised design:225-227 | The helper represents loops 0..21, but `CompleteLoop` only requires a number greater than the recorded loop, `S/server/customizations/Tutorial/ClusterFLoops.cs:47-61` | Correct arithmetic; sequential, at-cap progression is not enforced. |
| First loop | P282 modeled a reset at cap 50, with no scroll, revised design:267-269 | `Graduate` requests loop 1, `S/server/customizations/Tutorial/ClusterFLoops.cs:33-34`; graduation checks tutorial participation and core completion, `S/server/customizations/Tutorial/ClusterFTutorial.cs:279-296` | First loop recording is built. A current-level-50 check and actual reset are not built. Graduation is the newer implemented entry rule. |
| Level after every reset | 1 for both Keeper and Breaker, revised design:38-44 | `ResetLevelAndSkillsForF12` has an empty body, `S/server/customizations/Tutorial/ClusterFLoops.cs:40-42` | Missing. Recording a loop changes no level, skill, stat, or XP. |
| Loop persistence | Per-character loop counter starting at 0 | Account flags keyed by character serial, absent value reads 0, `S/server/customizations/Tutorial/ClusterFLoops.cs:22-28`; write at :60 | Built. It is a loop record, not an XP/level record. |
| Individual skill cap | Each player's permanent maximum level, 50..200, revised design:34-40 | Global default 200, `S/server/customizations/ClusterFSkillCaps.cs:11,25-30`; every player's skills receive that flat cap at :176-196 | Mismatch below loop 21. The player's recorded loop is not read. |
| Total skill cap | 58 x permanent maximum level, revised design:35-36 | `SkillInfo.Table.Length * _individualSkillCap` when totalCap is 0, `S/server/customizations/ClusterFSkillCaps.cs:151-158`; default total 11,600 at all loops | Formula matches the all-skills intent, but its input is global 200 instead of the player's ladder cap. |
| Configured values above 200 | Design ladder ends at 200 | Only the former default of exactly 300 is rewritten once, `S/server/customizations/ClusterFSkillCaps.cs:92-111`; fixed-point cap is bounded by ushort, not 200, at :154-155 | 200 is a default, not an absolute configuration ceiling. Manual settings can remain higher. |
| Starting skill allocation | No selected starting skill above 50, revised design:29-30 | Values above 50 are rejected, `S/server/customizations/CharacterCreation.cs:409-419` | Match for creation allocation. It does not constrain subsequent training to 50. |
| Companion cap ladder | Same 50,100,+5,200 ladder | Defaults and helper match, `S/server/customizations/Companions/CompanionSettings.cs:74-78,99-111`; companion skill caps use its max level, `S/server/customizations/ClusterFSkillCaps.cs:132-148` | Built for companions. This overload does not apply per-loop caps to players. |
| Scroll targets | 105,110,...,200, one per reset for loops 2..21; first reset has none, revised design:47-49,267 | Stock `PowerScroll.CanUse` compares the named skill's cap; `Use` sets that skill's cap, `U/Projects/UOContent/Items/Special/Special Scrolls/PowerScroll.cs:238-272` | Missing level-scroll transaction. No customization/patch redirecting this stock behavior was found. Default cap 200 rejects ordinary 105..120 scrolls. |
| Scroll/reset consumption | One next-target scroll and one confirmed at-cap reset together; cancellation consumes nothing, revised design:267-276 | `CompleteLoop` calls the empty hook and records/rewards any higher loop, with no scroll, current-level, next-loop, or confirmation check, `S/server/customizations/Tutorial/ClusterFLoops.cs:47-61` | Missing. Current production callers only request graduation into loop 1; this is an integration gap, not a demonstrated player skip exploit. |
| Scroll fragments | Existing related hook says five fragments make one scroll | `CombineLoopScroll` only sends a message, `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:237-239` | No scroll is made or consumed. This is separate from the design's 20 target scrolls. |
| After loop 21 | Cap stays 200, no 205 scroll, cosmetics/board only; revised design:274 | Helper stays 200, but `CompleteLoop` can still record and call the ordinary loop-box reward for later loops, `S/server/customizations/Tutorial/ClusterFLoops.cs:31,47-61`; box award at `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:218-221` | Cap arithmetic matches. The reward path has no post-cap branch and still supplies a Loop box, including a fragment and cosmetic sash at `S/server/customizations/LootBoxes/LootBoxRoller.cs:283-285`. |
| Displayed player level | A real current level within the loop | Con color uses best Base combat skill, clamped 1..200, `S/server/customizations/ClusterFCreatureLevels.cs:59-76,86-98`; loot boxes use total Base skill / 10, clamped 1..200, `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:58-66` | Two different placeholders. Neither is F-12 progression or evidence that players have reached a level. |

The full ladder below was recalculated from the current helper at
`S/server/customizations/Tutorial/ClusterFLoops.cs:31` and compared with P282's table
in the revised design:312-335. The code-helper column is a returned value only.
Actual player training defaults remain 200 per skill and 11,600 total on every row.
Scroll targets below are design requirements; the code does not implement them.

| Loop | Design max level / skill cap | Code helper max | Design total skill cap | Design scroll to enter |
| ---: | ---: | ---: | ---: | --- |
| 0 | 50 | 50 | 2,900 | None, creation |
| 1 | 100 | 100 | 5,800 | None |
| 2 | 105 | 105 | 6,090 | 105 |
| 3 | 110 | 110 | 6,380 | 110 |
| 4 | 115 | 115 | 6,670 | 115 |
| 5 | 120 | 120 | 6,960 | 120 |
| 6 | 125 | 125 | 7,250 | 125 |
| 7 | 130 | 130 | 7,540 | 130 |
| 8 | 135 | 135 | 7,830 | 135 |
| 9 | 140 | 140 | 8,120 | 140 |
| 10 | 145 | 145 | 8,410 | 145 |
| 11 | 150 | 150 | 8,700 | 150 |
| 12 | 155 | 155 | 8,990 | 155 |
| 13 | 160 | 160 | 9,280 | 160 |
| 14 | 165 | 165 | 9,570 | 165 |
| 15 | 170 | 170 | 9,860 | 170 |
| 16 | 175 | 175 | 10,150 | 175 |
| 17 | 180 | 180 | 10,440 | 180 |
| 18 | 185 | 185 | 10,730 | 185 |
| 19 | 190 | 190 | 11,020 | 190 |
| 20 | 195 | 195 | 11,310 | 195 |
| 21 | 200 | 200 | 11,600 | 200 |

The 58 multiplier was checked against the actual 58 entries in
`U/Distribution/Data/skills.json` (IDs 0..57, first at :3 and last at :915), loaded
into `SkillInfo.Table` by `U/Projects/UOContent/Skills/SkillsInfo.cs:135`.
The corresponding enum lists the entries at `U/Projects/Server/Skills.cs:19-76`.
These are the counted artifacts, not a count taken from the old research prose.

**XP, echo, reserve, and pacing**

For missing behavior, the code column points to the inspected integration boundary.
It does not invent a numeric setting of zero for an absent subsystem. The Python
research model is identified separately from production shard code.

| Number | Design value and source | Current code value and file:line | Result |
| --- | --- | --- | --- |
| Early XP | S2: 7.7598002866 x L^1.5 for transitions 1..99, normalized to a 3h opening, revised design:238-256 | Research only: `M/notes/cc-P282-scratch/approved_baseline.py:18-21` calls the S2 constructor in `M/notes/cc-P54-scratch/xp_ladder.py:52-72`; player reset integration remains empty at `S/server/customizations/Tutorial/ClusterFLoops.cs:40-42` | No player XP table or award path implements this curve. |
| Late XP | Monotone bridge at 100..104, about 102,272.54 XP per transition at 105..199; bridge about 7,644 for 99->100 versus 98,339 for 100->101, revised design:243-256 | Same research constructor, no player XP implementation | Unbuilt. The sharp bridge is part of the research result, not measured gameplay. |
| Solver target | 12.472264969h per late loop as an input derived from nominal 260h; actual empty-bank total 334.02h, revised design:238-241 | `M/notes/cc-P282-scratch/approved_baseline.py:20-21`; no server pacing target | 260h is not the resulting end-to-end time. Neither time is a server setting today. |
| Kill XP | 5 x creature level, modeling assumption, revised design:248 | No F-12 player award path. Existing gear XP uses Bard difficulty x its multiplier, `S/server/customizations/LevelGear/ClusterFLevelGear.cs:452-460`; evo-pet XP uses damage share x (20 + Fame/25) x its rate, `S/server/customizations/Mobiles/Evo/EvoPet.cs:212-221` | Unbuilt for players. Gear/pet XP must not be mistaken for this formula. |
| XP from skill gains | 2 x level XP per newly attained skill point, October 5 decisions:33; XP for acts, not currency/achievement turn-ins, :34 | Player gain wrapper applies rate bonuses, `S/server/customizations/ClusterFSkillGain.cs:272-300`; reset/peak integration is empty, `S/server/customizations/Tutorial/ClusterFLoops.cs:37-42` | No F-12 skill-peak XP accounting or level-XP award path was found. |
| Base echo | min(10,1 + 0.5 x loop): x1.5 at 1, x3 at 4, x6 at 10, x10 from 18, new ground x1; revised design:65-70 | Research function at `M/notes/cc-P54-scratch/xp_ladder.py:22`; no player loop/peak factor in gain amount application, `S/server/customizations/ClusterFSkillGain.cs:288-310` | Unbuilt. No extra global +20% loop bonus is implemented or required. |
| Keeper echo | Skills only: x1.5 at loop 1 to x50 at 21, never below base; exact linear step 48.5/20 = 2.425, loop 11 = 25.75; queue:1245-1249 | Research function at `M/notes/cc-P54-scratch/xp_ladder.py:23`; empty Keeper/Breaker reset hook at `S/server/customizations/Tutorial/ClusterFLoops.cs:37-42` | Unbuilt. x50 is not a player level-XP multiplier. |
| Echoed skill gain per use | Default maximum 2.0 skill points per use, October 5 decisions:38 | Current amount bonus repeats stock `SkillCheck.Gain`, `S/server/customizations/ClusterFSkillGain.cs:288-300`; no Keeper echo implementation | Unbuilt echo-specific cap. Global attempt/amount settings are different controls. |
| Breaker retention | +3 skills per loop past the first, all 58 by loop 21, floor eventually full peak; queue:1231-1233 | Empty reset/peak-memory hook, `S/server/customizations/Tutorial/ClusterFLoops.cs:37-42` | Unbuilt. Current skills staying unchanged on graduation is not the Breaker schedule. |
| Reserve size | Five outgoing-cap transitions C->C+5; zero at 200, revised design:260-263 | Research `bank(cap)` implements this sum at `M/notes/cc-P282-scratch/approved_baseline.py:24-25`; player reset hook has no bank handling, `S/server/customizations/Tutorial/ClusterFLoops.cs:40-42` | Unbuilt. Exact valuation remains a P282 proposal; five levels supersedes the queue's old 25% rule. |
| Reserve credit examples | At cap 50: 14,552.78 XP, arriving at level 29 plus partial XP. At 100: 501,528.78 XP, arriving at 101 plus 96,668.19 toward 102. Later full banks: 511,362.68 XP, arriving at 102, revised design:281-285,386-409 | Research credit loop at `M/notes/cc-P282-scratch/approved_baseline.py:28-33`; no server equivalent | Model values only. Five levels of cap-valued XP does not limit the credited jump to five levels. |
| Credit and overflow | Raw credit from level 1 once, no echo on credit; overflow lost; full reminder no more than every 30 minutes; no reserve after 200, revised design:269-274 | Empty reset integration, `S/server/customizations/Tutorial/ClusterFLoops.cs:37-42` | No reserve persistence, credit, overflow, or notification behavior is built. |
| Steady/cautious assumptions | 120 kills/h at own level versus 60/h at 75% of own level, minimum creature level 1; schedules 1/3/6 active h/day, revised design:300-305 | Research `rate_A` / `rate_B`, `M/notes/cc-P54-scratch/xp_ladder.py:39-40`; no F-12 player clock/rate | Modeling inputs, not configured throughput or daily XP multipliers. |
| Empty-bank pacing | To 50: 3h steady, 7.99h cautious. To 100: 10.55h / 28.13h. To 200: 334.02h / 890.67h, revised design:413-423,505-507 | Reproducible research estimates; no player progression implementation | Unbuilt and unverified in play. Steady days to 200 at 1/3/6h are 334.02 / 111.34 / 55.67. |
| Full-bank pacing, fill cost included | To 100: 10.13h / 26.99h; to 200: 406.44h / 1,083.83h steady/cautious, revised design:411-419 | Research estimates only | Unbuilt. Banking is not a free speed bonus; fill cost is already included. |
| Alternative curve | C=20/24/30/40, C=24 gives 32.64h to 100 and 239.65h to 200; escrow comparison 240.38h, revised design:425-444 | Comparison model only, `M/notes/cc-P282-scratch/xp_curve.py:10-39,96-127` | Not the approved S2 baseline and not shard code. The 160 content-ceiling scenario is also only a comparison. |

**Current-level gates and proposed rewards**

These are P282 proposals. Their absence is unfinished feature work, not a numerical
regression introduced by P282. Searches for the specific title names, The Setting,
the proposed gate expression, and XP/peak integration were followed by reading the
player level and loop seams cited below.

| Number | P282 design value and source | Current code value and file:line | Result |
| --- | --- | --- | --- |
| Combat contracts/dives | Level 1 starter; T1 at 25, T2 at 50, T3 at 75, T4 at 100, T5/T6/T7 at 125/150/175; capstone at 200 plus loop 21 and epilogue, revised design:454-462 | No real player current-level field at the inspected level sources: `S/server/customizations/ClusterFCreatureLevels.cs:59-76` and `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:58-66` | F-12 gates are unbuilt. Existing skill/rank/content checks do not implement these level thresholds. |
| The Setting | 20 floors; floor N needs loop N+1 and proposed current level 95+5N: first floor loop 2/current 100, last loop 21/current 195, epilogue at 200, revised design:464-470 | No Setting floor/gate implementation found in customizations or patches; only the loop record/helper at `S/server/customizations/Tutorial/ClusterFLoops.cs:25-31` | Unbuilt. The old separate 20 post-cap loops are superseded. |
| Level titles | 25 First Light; 50 Wayfarer; 75 Delver; 100 Seasoned Delver; 125 Deepwalker; 150 Riftwalker; 175 Legacy Seeker; 200 + loop-21 epilogue the Unbroken, revised design:472-485 | `OnLevelUp` currently only plays fanfare, `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:213-215`; no matching F-12 title-grant implementation found | Unbuilt as level milestones. |
| Renown | +2 once per account for each new level 2..200; 98 by 50, 198 by 100, 298 by 150, 398 maximum; zero AP, revised design:487-498 | `GrantRenown` exists but has no level-claim mechanism, `S/server/customizations/ClusterFAccountData.cs:653-681`; `OnLevelUp` only plays fanfare at the line above | Unbuilt. The arithmetic is 199 eligible levels x 2 = 398. |
| Renown comparison | Bronze requires 2,500 in the source-default ladder, revised design:490 | `S/server/customizations/ClusterFLeagueRanks.cs:491` is 2,500 | Match as a default. Live League settings were not inspected. |
| Cosmetics | Persistent choices at 50/100/150/200, revised design:491 | Fanfare-only level hook, `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:213-215` | Proposed milestone border/badge awards are unbuilt. |
| Free stat/skill points | Zero from level-up or reset, revised design:254 | Loop recording only changes the flag and awards a loop box, `S/server/customizations/Tutorial/ClusterFLoops.cs:59-61`; no player level-up system | No direct point grant in this seam, consistent so far. Item-level points at `S/server/customizations/LevelGear/ClusterFLevelGear.cs:433-436` belong to gear, not player stats or skills. |

**Other cap numbers and stale descriptions**

| Number or older claim | Design/reference value | Current code value and file:line | Finding |
| --- | --- | --- | --- |
| Effective stats | Revised design:82-87 removes effective clamps; only engine bound 65,000 remains | Default individual 500 and total 1,500, `S/server/customizations/ClusterFStatCaps.cs:10-24,105-107`; `S/server/patches/PlayerMobile-individual-stat-cap.patch:8,17,26` still uses `Math.Min` with the individual cap for ordinary players under ML | Mismatch with the no-effective-clamp design. The patch is still applied at `S/docker/uo/apply-patches.sh:301`. Total 1,500 is still assigned, rather than removed. |
| Raw stat gain limit | Revised design:84-85 says both configs set stats.statMax=500 | Pinned code reads that key with default 125 under LBR, otherwise 100, `U/Projects/UOContent/Skills/SkillCheck.cs:23` | Configured 500 is unverified here. It is distinct from ClusterF's effective 500 clamp. No live configuration was inspected. Engine raw/effective Str bounds remain 65,000 at `U/Projects/Server/Mobiles/Mobile.cs:1854,1889`. |
| Skill cap 300 | Queue:1111-1114 and revised design:182 describe 300 as current | Default is now 200 and former default 300 is rescaled once, `S/server/customizations/ClusterFSkillCaps.cs:11,92-111` | Stale historical description. Overrides and previously earned Base values can remain higher; `Apply` writes caps, not Base. |
| Metal progression 100..300; all extended ore at 100 Mining | Revised design:187-188,197-201 | Platinum/Toxic/Blaze/Frost/Obsidian/Mythril/Adamantium/Celestial are 112.5/125/137.5/150/162.5/175/187.5/200 in `S/server/customizations/ClusterFMetalTiers.cs:20-27`; harvest uses all eight entries at `S/server/customizations/ClusterFMiningExtension.cs:103-112`; Blacksmithy registration at :188-195. Dawnstone is 45 at `S/server/customizations/ClusterFMetalTiers.cs:34` | Old 300-era description is stale. Post-Valorite mining does not all unlock at 100 today. The table and registration lines list the counted eight metals. |
| Achievements at skill 300 | Revised design:185-186 warns they become unreachable | `skills.grandmaster` and `skills.triple_grandmaster` retain the 300 triggers but are explicitly retired, `S/server/customizations/ClusterFAchievements.cs:533-538,769-774` | Warning has already been handled by retirement. These are the two definitions checked. |
| Smith scrolls 305..320; +25 future steps | Revised design:189-190 describes sales at 305..320 | Active catalog categories contain no scroll tab, `S/server/customizations/SmithSealCatalogGump.cs:37-52`; its comment at :40 still says future steps of 25 | Sales claim is stale; the remaining +25 comment contradicts the current +5 ladder. No code changed. |
| Stable slots at three skills of 200 | Revised design:136-141 says no hook today and 38 slots | Registered patch calls `ClusterFSkillClamps.StableSlots`, `S/server/patches/AnimalTrainer-stable-slots-scaled-200.patch:10`, applied at `S/docker/uo/apply-patches.sh:598`; default six slots per skill at 200, `S/server/customizations/ClusterFSkillClamps.cs:123,244-265` | Old 38 is stock arithmetic, not the default patched player result. New result is 5 + 3 x 6 = 23, skill-based, not a permanent-max-level stable entitlement. |
| Follower slots | Revised design:120-121 ties capacity to permanent maximum level; no complete F-12 numeric entitlement table there | Companion owner-loop curve starts at 5, ends at 19 at loop 21, `S/server/customizations/Companions/CompanionSettings.cs:87-95`; owner provider falls back to 0 at :120-123; `S/server/customizations/Companions/CompanionParty.cs:81-85` raises without lowering | Partial supporting code. No production provider assignment found; tutorial's real loop count is not wired into this seam. Exact F-12 player entitlement remains unbuilt. |
| Bank capacity | Revised design:122 gives base 1,000 and anticipates max-level access | Base 1,000 is built, `S/server/customizations/ClusterFBankLimit.cs:26`; bonus uses League milestones, not player level, at :32,40-47 | Base matches. This code supplies no F-12 maximum-level gate. |
| Test/live skill gain rates | Revised design:61-62 describes test x5 plus 3 attempts and x5 amount; October 5 decisions:39 proposed live stock x1 | Defaults are 2 attempts and x1 amount, `S/server/customizations/ClusterFSkillGain.cs:41-42,88-97`; old global Test Center multiplier only logs a retirement warning, `S/server/customizations/TestCenter/TestCenterSkillGain.cs:18-38` | Old rate description is stale; later P190/P191 code changed the baseline. These controls do not implement loop echo. |
| Old queue ladders/reserve | Queue contains max 1,000, 13 loops, five-reset/+25 examples, separate 20 post-cap loops, and 25% reserve, at :1138,1166-1184,1236,1252-1281 | Current helper is the 21-reset 200 ladder; revised P282 reserve is five levels | Documentation conflicts, not alternative live settings. Queue precedence at :928-930 and the later October 3 block at :1225-1249 prevent treating its older examples as current design. |

The older 41-of-58 breakage and 39-of-58 gain-path counts near the start of the revised
design were not re-audited skill by skill. They are historical P20 coverage claims,
not newly verified P517 counts. Current `ClusterFSkillGain` already contains later
gain-path work, including the cap-based window at :320-338. This task does not infer
remaining missing skills from those old counts.

**Validation and limits**

- Read canonical customizations, relevant patches and their application entries,
  and the matching pinned upstream files. Did not read the generated `server/uo/`
  tree or connect to Haven.
- Searched tracked customizations and patches for ladder callers, loop consumers,
  power-scroll integration, XP/reserve/echo/peak handling, and proposed gates/titles.
  Confirmed the important findings by reading the implementations cited above.
  `rg` was unavailable; used `git grep` and PowerShell reads/searches.
- Recalculated all 22 helper rows and total-cap products from the inspected formula
  and the counted skills data. The rows and counted artifact paths are published above.
- Ran existing `python -B notes/cc-P282-scratch/verify_curve.py`: all 10 research
  checks passed. Added or changed no tests. These checks validate research arithmetic,
  not implementation of F-12 on the shard. Lane tests: none. No server build needed.
- Ran required `tools/progress.py --dry-run` successfully with SL_SHARD and SL_MIGRATE
  pointing to these work copies and SL_SERVUO to the read-only reference. Restored its
  incidental `tools/progress.json` write byte-for-byte so this remains notes-only.
- Windows PowerShell was 5.1.26100.9711. Runtime settings, deployed behavior, actual
  XP throughput, scroll acquisition times, and client behavior remain unverified.
- No commit, merge, push, branch switch, deployment, account operation, code edit,
  or migration `docs/` edit. The task's outer notes filename is a separate completion
  record linking this report, preserving both requested filenames.
- Final checks passed in both repositories. The code work copy is clean; only the
  two requested notes files are new in the migration work copy. Both are below 5 MB,
  contain no em dashes, and have no trailing whitespace.

P517 DONE
