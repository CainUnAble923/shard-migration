# P518: skill gain paths research against the code

Reviewed October 24, 2026. Research only. No code, configuration, saves, or services changed.

P283's remaining path backlog still stands against this checkout. P191 changes how often eligible uses gain and how much they gain. P202 and P204 integrate that work; they do not add training content. They do not close P283's missing paths. The current source still supports P283's distinction between 23 served skills and 16 open skills in its historical set of 39, plus three bard follow-ups outside that set. Focus needs an additional worn-bonus qualification, described below.

This is a comparison of paths, not another P443 review. P443's findings are not repeated. A source-supported path means the gain call can continue toward Base 200 under its stated conditions. It does not establish live availability, a training time, or a path for every possible equipment choice.

## Sources and method

Read both work-copy AGENTS.md files, direction-decision, tasks, P283 and its review, P191, P202, P204, and P443 and its review. Checked the canonical customizations, registered patches, relevant existing tests, and pinned ModernUO implementations. Did not read the stale server/uo build tree.

Source snapshot:

- Code work copy: `6f540be8b84f63f76b8852fe638039b363b66a6b`.
- Notes work copy: `668b31b751198e926e2507cff679c70cac87f00b`.
- Read-only ModernUO: `d4531cd94b739613155225c234900de9f47d2c88`.

Paths below use `C/` for `ShatteredLegacy/server/customizations/`, `P/` for `server/patches/`, `T/` for `server/tests/`, and `U/` for `D:/UO/ModernUO-pinned/Projects/UOContent/`. References are current source lines; patch references name the hunk's target when appropriate. The research input is [P283](cc-P283-skill-gain-paths-research.md); the rate work is [P191](cc-P191-cont-earned-skill-gain.md), [P202](cc-P202-cont-fixup-cont-earned-skill-gain.md), and [P204](cc-P204-cont-fixup-cont-fixup-cont-earned-skill-gain.md).

The common boundary explains the result. `U/Skills/SkillCheck.cs:56-74` returns before rolling when Value is below the minimum or at/above the maximum. Direct checks also return at chance >= 1 (`:90-106`). `C/ClusterFSkillGain.cs:241-247,257-268` retains those boundaries for additional attempts. Its defaults remain two attempts and onefold amount (`:39-40,89-97`). More attempts cannot reopen an exhausted window.

For listed uses, hook G supplies a separate gain roll after the ordinary result. It remains a specific switch, not an extension of every skill (`C/ClusterFSkillGain.cs:320-440,447-474`). Cap-following maximums account for positive worn bonuses (`:210-217`), and hook G adds Value minus Base to its own maximum (`:464`). Ordinary gains still pass through pinned Gain and its skill lock and individual cap checks (`U/Skills/SkillCheck.cs:248-280`). These are separate responsibilities from the rate defaults.

## Combat and support

| Skills | P283 research says | Current code does | Gap |
|---|---|---|---|
| Bushido | Momentum Strike already supplies a path; other Bushido casts need not all become cap trainers. | The exact 70..120 location check matches hook G (`C/ClusterFSkillGain.cs:400-401`; caller `U/Spells/Bushido/MomentumStrike.cs:67`). | No new path needed. Retain the qualifying combat use. |
| Arms Lore | Train on harder material gear, including exceptional crafts, rather than all items equally. | Inspect uses gear difficulty +/-50; difficulty includes material, exceptional quality, and magic. Exceptional crafting has a separate callback (`C/ClusterFSkillGain.cs:406-415,507-526`; `C/ClusterFArmsLore.cs:159-207`). An exceptional Runewood item has difficulty 195 and upper edge 245. | No new gain path needed. Gear supply and access still need player verification. |
| Healing | Qualified bandaging already reaches the cap. | Hook G matches the primary 0..120 bandage check (`C/ClusterFSkillGain.cs:350-352`; `U/Items/Skill Items/Misc/Bandage.cs:444-445`). | None for the path. Preserve the treatment eligibility and existing delays. |
| Swordsmanship, Macing, Fencing, Archery, Throwing, Wrestling; Tactics, Anatomy; Parrying | P283's complement already has combat paths. | Weapon skills use direct hit checks; Tactics and Anatomy have cap-based checks; Parrying has direct checks (`U/Items/Weapons/BaseWeapon.cs:1340,1528,1569,2524-2527`). | No new content path identified. Weapon skill training still needs an opponent that keeps the direct check below certainty. This is not a timing measurement. |

## Magic schools and Imbuing

| Skills | P283 research says | Current code does | Gap |
|---|---|---|---|
| Magery | Needs Training Ward or repeatable lesson content after 120. | Highest book window remains 80..120 (`U/Spells/Base/MagerySpell.cs:15-17,30-42`). No Magery hook G row. | Open: eligible paid casting practice that supplies further gain without changing normal cast success. |
| Necromancy | Needs a school-specific adapter to the shared practice framework after 120. | Normal book checks use RequiredSkill..RequiredSkill+40, topping at 120; Vampiric Embrace requires 99 but overrides its window to 80..120 (`U/Spells/Necromancy/NecromancerSpell.cs:37-40`; `VampiricEmbrace.cs:24,32-42`). | Open: valid upper-school use, with costs and target checks, followed by a gain-only path. |
| Chivalry | Practice must start at its own ceiling, 115. | RequiredSkill..RequiredSkill+50 remains stock (`U/Spells/Chivalry/PaladinSpell.cs:126-130`); Noble Sacrifice requires 65. | Open: bridge 115 onward. Starting a lesson at 120 would leave an earning gap. |
| Spellweaving | Practice must bridge 117.5 onward. | RequiredSkill-12.5..RequiredSkill+37.5; Word of Death requires 80 (`U/Spells/Spellweaving/ArcanistSpell.cs:85-89`; `WordOfDeath.cs`). | Open: sanctioned, paid weaving use with further gain. |
| Mysticism | Practice must bridge 120.5 onward; do not solve Imbuing by silently changing the damage skill. | Highest requirement is 83, window -12.5/+37.5 (`U/Spells/Mysticism/MysticSpell.cs:9,46-54`). Reading Imbuing/Focus for power at `:42-44` does not make either the inherited DamageSkill gain check. | Open: a Mysticism lesson path. No Imbuing training path is supplied by that power calculation. |
| Resisting Spells | Eligible curse and necromantic effect checks already supply a path. | Hook G matches location 0..120 (`C/ClusterFSkillGain.cs:396-397`), including the calls named in its preceding comments. | No new path needed. Not every incoming spell reaches such a check. |
| Ninjitsu | Ninja weapons already train to 200 against a sufficiently skilled defender. Pure spell/form practice is optional. | Ninja weapons use an attack/defense direct chance (`U/Items/Skill Items/Ninjitsu/NinjaWeapons.cs:201-274`). With no hit/defense modifiers, effective Ninjitsu 200 against defense 120 gives 220/280, below certainty. | No required path gap. Ammunition and a challenging opponent remain necessary for this route; a form-only alternative would be new scope. |
| Evaluating Intelligence, Spirit Speak | Already served through damage-school gain calls. | `U/Spells/Base/Spell.cs:623-628` checks DamageSkill to its cap when it differs from CastSkill. | No new path identified. A support skill reaching 200 does not imply its casting school can do so. |
| Imbuing | P82 did not close the ceiling; recommends commissions involving real property improvements. | Property difficulty tops at 120, with applicable ease subtracted; the check is difficulty +/-20. Disenchant and essence crafting use 20..80 (`C/ArtificersImbueGump.cs:121-130,1248,1854,1997,2122`). No Imbuing hook G row. | Open: at best the present route ends at 140. Specify consumable improvement commissions or a separately scoped mastery action. Raising item power or budgets is not required to create a gain path. |

Casting-school exclusions are explicit in the code and in `T/Skills/SkillGainPastStockCeilingVerification.cs:452-473` (G7). P191 retains that design. Choosing and obtaining the ward or lesson, and defining a qualifying use for each school, remain builder inputs. This note makes no new design decision.

## Thief skills and bards

| Skills | P283 research says | Current code does | Gap |
|---|---|---|---|
| Hiding, Snooping, Poisoning | Existing eligible uses already reach the cap. | Hook G matches outdoor/non-friend-house Hiding 0..100, target Snooping 0..100, and high poison windows ending at 100 with minimum 60 or 95 (`C/ClusterFSkillGain.cs:332-347`). | No additional path needed. Retain each row's restrictions. |
| Stealth | Use the armor ladder first, then the extended check after effective skill 142. | Matches location windows of width 80, maximum >=60, and Value >=142 (`C/ClusterFSkillGain.cs:337-338`). | No additional path needed. Unarmored use alone is not the whole climb. |
| Detect Hidden | Finding a real hider or trap supplies further gain. | The found-result callback rolls to Cap plus bonus after Value 100 (`C/ClusterFSkillGain.cs:482-499`; `P/DetectHidden-osi-radius-found-gain.patch`). | No additional path needed. Empty scans are not the upper-skill path. |
| Stealing | Full ten-stone theft and high-fame monster theft supply routes. | Hook G matches exactly 77.5..127.5 (`C/ClusterFSkillGain.cs:435-436`). Monster stealing separately checks 60..100+2.5*fameLevel (`C/Services/Monster Stealing/Core/StealingHandler.cs:297-304`). | No additional path needed. Do not restore the former unbounded stack-weight route. |
| Lockpicking | Needs obtainable higher-tier locks. | Ordinary picks read LockLevel..MaxLockLevel (`U/Items/Skill Items/Thief/LockPick.cs:121-128`). Treasure chests still cap RequiredSkill at 100 and set the maximum to RequiredSkill+40 (`P/TreasureMapChest.cs:345-355`). Skeleton keys read those same lock fields (`C/Items/Tools/SkeletonKey.cs:149-152`). | Open: repeatable high lock/chest tiers and their source. A better pick that bypasses the roll is not a gain path. |
| Musicianship | Normal instrument use already reaches the cap. | Its 0..120 location call matches hook G (`U/Items/Skill Items/Musical Instruments/BaseInstrument.cs:526-530`; `C/ClusterFSkillGain.cs:378-379`). | No additional path needed for Musicianship itself. |
| Peacemaking, Provocation, Discordance | Additional follow-ups outside the historical 39. Need suitable shard encounters or lessons. | Base creature difficulty is capped at 160 (`U/Items/Skill Items/Musical Instruments/BaseInstrument.cs:299-304`). Targeted peace/discord end at difficulty+15 minus music reduction; provoke at average difficulty+20 minus reduction (`U/Skills/Peacemaking.cs:163-171`, `Discordance.cs:154-168`, `Provocation.cs:131-154`). `P/Bard-musicianship-reduction-osi.patch` caps the music contribution; mule ease further lowers both check edges (`C/ClusterFSkillGain.cs:177-180`). | Still open as a dependable 200 ladder. With ordinary instruments and the full ten-point music reduction, tops are 165/170. Instrument quality/slayer modifiers can change those values, so these are not universal mathematical maximums. Define eligible nonimmune shard targets, including final-point headroom with music and mule ease. |
| Remove Trap | Already has a partner route from high Tinkering. | A 200 Tinker makes TrapPower 180; disarm checks power..power+30, hence 180..210 (`U/Engines/Craft/DefTinkering.cs:678-683`; `U/Skills/RemoveTrap.cs:61`). `P/Tinkering-trap-damage-osi.patch` caps damage level separately. | No new gain helper needed for an unbonused route. Verify lockable containers and trap supplies in a future player check. Low-level training kits are not the 200 path. |

## Animals

| Skills | P283 research says | Current code does | Gap |
|---|---|---|---|
| Animal Taming | Needs a wild creature ladder, with a bridge around 125 and suggested high requirements 150.1/170.1. | `P/AnimalTaming-pet-training.patch` uses CurrentTameSkill in the ordinary timer window. For a fresh tame, the upper edge is requirement+49.9; owners add six each (`U/Skills/AnimalTaming.cs:396-406`). DreadWarhorse's literal 108 gives 157.9 fresh, 181.9 with four owners (`C/Mobiles/Normal/DreadWarhorse.cs:53`). Normal pet training clamps requirements at 108 (`C/Services/Pet Training/BaseCreature.PetTraining.cs:59`; `TrainingProfile.cs:171`). | Open for the demonstrated content. High player caps and stronger trained pets do not create the proposed wild ladder. Supply, spawn access, control, and retained pet strength still need specification. |
| Animal Lore | Already has a target-based hook, but lacks the corresponding high creature content. | Creature-target 0..120 calls get MinTameSkill-0.1..MinTameSkill+49.9 (`C/ClusterFSkillGain.cs:365-374`). This reads MinTameSkill, not the trained CurrentTameSkill. | Open: use the same higher wild variants. Merely keeping hook G enabled does not make a 108 target teach 200. |
| Herding | Share the high animal ladder; 150.1 alone is insufficient. | Uses MinTameSkill-30..MinTameSkill+30+Random(10) on herdable creatures (`U/Items/Weapons/Staves/ShepherdsCrook.cs:85-117,133-146`); no hook G row. | Open: a 170.1 target gives upper edges 200.1..209.1 before gear bonuses, while 150.1 tops at 189.1. The final route also needs worn-bonus handling or sufficient extra target headroom. |
| Veterinary | Ordinary eligible pet treatment already reaches the cap. | Shares Healing's primary 0..120 location hook (`C/ClusterFSkillGain.cs:350-352`; `U/Items/Skill Items/Misc/Bandage.cs:444-445`). | No new pet tier needed for Veterinary gain. Its location check does not trigger Animal Lore's creature-target row. |

The high-tame figures are checked examples, not an exhaustive runtime maximum. No constructor/profile enumeration was run. A later animal builder must establish the actual candidate list before treating the gap as a measured absence across every creature. Reward/evo art and stronger combat stats alone are not evidence of higher taming requirements.

## Crafts and gathering

| Skills | P283 research says | Current code does | Gap |
|---|---|---|---|
| Blacksmithy, Tinkering | Consuming advanced-metal crafts already supply paths. | `C/ClusterFCraftGain.cs:64-80,101-123` maps these crafts to metal ceilings. Adamantium is usable at 187.5 and teaches to 200 (`C/ClusterFMetalTiers.cs:26-27,70-80`). The gain window includes the worn bonus. | No new path needed. Keep the consumed-material and nonzero-recipe-window requirements. |
| Bowcraft/Fletching, Carpentry | Consuming shard-wood crafts already reach 200, even though harvesting does not. | The same helper maps these crafts to the wood ladder. Voidwood is usable at 185 and teaches to 200 (`C/ClusterFWoodTiers.cs:26-27,54-63`). | No new path needed. Starwood's use requirement of 200 is not circular because Voidwood supplies the final gains. Board cuts do not qualify. |
| Inscription | Needs ward commissions or other paid high-tier content after 150. | MysticSpellbook remains 50..150 (`U/Engines/Craft/DefInscription.cs:463`). ClusterFCraftGain has no Inscription mapping. | Open: obtainable consumable work bridging the existing ceiling to 200. |
| Alchemy | Registered top is 151, not the old 150; still needs commissions or recipes above that. | Eodon potion registrations are 51..151 under the TOL gate (`C/Engines/Craft/AlchemyCraftRegistrations.cs:62-95`). No Alchemy material mapping. | Open: a higher teaching ladder and repeatable ingredients/orders. Registry presence does not prove recipes and ingredients are obtainable. |
| Cooking | Needs provision orders or equivalent content after 130. | Green Tea is 80..130 (`U/Engines/Craft/DefCooking.cs:143-148`); current extra registrations top at 120 or below (`C/Engines/Craft/CookingCraftRegistrations.cs:52-85`). No Cooking material mapping. | Open: paid provision work with a sink and further gain. More food types alone do not change their skill windows. |
| Tailoring | Needs higher cloth/leather work or outfit commissions after 144, potentially 150 with module settings. | Gargish cloth chests register 94..144 (`C/Engines/Craft/TailoringCraftRegistrations.cs:90-99`); no Tailoring material mapping. | Open: orders or a resource/recipe ladder, including actual material sources. |
| Lumberjacking | First recommended batch: retier existing harvest resources and make further gain bonus-safe. | The eight extended resources still all require 100, with check maxima 140..148 (`C/ClusterFLumberjackingExtension.cs:232-241`). Harvest checks those resource fields after a Base gate (`U/Engines/Harvest/Core/HarvestSystem.cs:142-147`). Axe combat gain still uses 0..100 (`U/Items/Weapons/BaseWeapon.cs:2532,2605`). No Lumberjacking hook G row. | Open: harvest still ends at 148 without bonuses. Implement the existing approved tier ladder with resource teaching windows, not another craft change. Preserve discovery and grove behavior. |
| Mining | Already has advanced ores, not only the old sand route. | Ore difficulty is tier +/-40 (`C/ClusterFMiningExtension.cs:103-112,155-161`); Obsidian 162.5 has upper edge 202.5. Higher ore tiers and the sand resource in `P/Mining.cs` offer alternatives. | No new path identified. Resource eligibility and effective skill still matter; this is not a claim that every ore trains every equipment setup. |
| Fishing | Already reaches 200 through lobster/crab traps; a rod-only alternative is optional. | `C/Services/Expansions/High Seas/Items/LobsterTrap.cs:322-325` checks Fishing 0..Cap on its tick, with the deep-water Base gate. Rod resource checks remain 0..100 (`U/Engines/Harvest/Fishing.cs:100`). | No missing path if traps are accepted. Rare-fish selection does not itself extend rod gain. |

The craft helper is wired into the actual recipe gain call by `P/CraftItem-shard-hooks.patch`, GetSuccessChance hunk. Its map remains limited to the four material crafts above. Mule modules do not close the other gaps: main minima 50/70/90/100/110 get +40, secondary minima get +20 (`C/Mobiles/Mule/MuleModule.cs:169-170,269-274`). Default maxTier is three (`MuleModuleData.cs:55`), so the default main top is 130; configured tier five can reach 150. This can offer Cartography or Tailoring an alternate intermediate route, not 200.

## Other skills

| Skills | P283 research says | Current code does | Gap |
|---|---|---|---|
| Begging, Forensic Evaluation, Tracking, Taste Identification, Camping | Already have qualified extended uses. | Hook G covers eligible NPC begging, mobile/corpse forensics, the post-success Tracking check, food tasting, and kindling lighting (`C/ClusterFSkillGain.cs:355-360,382-391`). | No new path needed. Retain target/use restrictions and existing costs. |
| Item Identification / Appraisal | High creature levels already supply a path, conditional on access. | Creature appraisal checks 0..100 and is routed to level +/-25 by hook G (`C/ClusterFCreatureLevels.cs:369-376`; `C/ClusterFSkillGain.cs:420-429`). The source includes Harrower 200 and separate champion/peerless rules (`C/ClusterFCreatureLevels.cs:101-104,183-192`). | No missing helper. Accessible encounters of sufficient level remain unverified. Ordinary item identification is not this route. |
| Cartography | Needs repeatable high survey/map tiers, paired with locks. | Decode reads minimum-10..minimum+30; the current map table reaches minimum 100, including level seven (`P/TreasureMap.cs:1028-1042,1250-1259`). Tier-five mule modules can offer a separate craft top of 150. | Open: a higher map number alone does not close the gap. Supply actual higher difficulty, source, and repeatable decode/chest work. |
| Meditation | Active meditation already supplies a cap-following route. | After its eligibility/start checks it rolls 0..Cap (`C/Meditation.cs:107-116`), covered by EffectiveMax's worn-bonus adjustment. | No new path needed. Passive regeneration alone is not the required route. |
| Focus | P283 lists regeneration in its served complement. | Regeneration calls CheckBonusSkill for Focus (`C/RegenRates.cs:101,164`), which sets chance to r*(1-v)+v, where r is current/max resource and v=sqrt(Value*0.005) (`:28-41`). This is a direct check, with no EffectiveMax adjustment or Focus hook G row. | Conditional gap in the research's bonus-safe acceptance: below-full resources permit gains while Value <200, but positive bonuses can exhaust this route before Base 200. Details below. |

### Focus boundary that P283's complement needs to qualify

At Value 200, v is one and the direct chance is one regardless of the current resource fraction. Pinned's direct handler returns without a gain roll at that chance (`U/Skills/SkillCheck.cs:90-106`), as do extra attempts (`C/ClusterFSkillGain.cs:247,257-268`). With +15 Focus, this happens at Base 185. At Base 199.9 plus 15, Value is 214.9, v is greater than one, and for an ordinary resource fraction between zero and one the chance is at least one. No roll reaches Gain. The default above-cap bonus admission allows Value to exceed Cap (`C/ClusterFSkillBonusAboveCap.cs:20-36`).

This is a source-traced conditional path limitation, not a reproduced runtime defect or a claim that Focus cannot reach 200. Removing the positive bonus leaves regeneration below certainty through Base 199.9 when resources are below full. Searched pinned source and canonical customizations/patches for Focus gain callers; the regeneration call sites are the relevant ongoing player route found. The pet Focus patch changes creature eligibility inside Gain, not this chance calculation. A future builder should probe the equipped case first and, if the bonus-safe requirement is retained, supply a narrow gain-only correction without changing regeneration strength. No code or tests are added here.

## Reconciled backlog and handoff

The historical 39 partition is unchanged. These are skill counts, not file counts; the named lists are the denominator:

- Served in source, 23: Bushido, Arms Lore, Healing, Resisting Spells, Ninjitsu, Hiding, Stealth, Detect Hidden, Snooping, Stealing, Poisoning, Musicianship, Veterinary, Bowcraft/Fletching, Carpentry, Tinkering, Fishing, Begging, Forensic Evaluation, Tracking, Appraisal, Taste Identification, Camping.
- Open, 16: Magery, Necromancy, Chivalry, Spellweaving, Mysticism, Imbuing, Lockpicking, Animal Taming, Animal Lore, Herding, Inscription, Alchemy, Cooking, Tailoring, Lumberjacking, Cartography.
- Outside that historical set, P283's additional bard follow-ups remain Peacemaking, Provocation, and Discordance. Focus adds the conditional equipment limitation above, not another skill wholly lacking a 200 route.

The other skills named in the group tables complete coverage of P283's complement: Blacksmithy, Mining, Remove Trap, Swordsmanship, Macing, Fencing, Archery, Throwing, Wrestling, Tactics, Anatomy, Parrying, Evaluating Intelligence, Spirit Speak, Focus, and Meditation, alongside those three bards. This crosswalk preserves P283's membership instead of presenting the old 39 as a fresh implementation count.

Carry forward P283's builder order: lumber harvesting; five school adapters on shared practice content; the animal ladder; Inscription/Alchemy/Cooking/Tailoring content; paired locks/maps and bard targets; then paid Imbuing mastery. The Focus equipment case is a separate narrow follow-up. The source comparison does not justify another global rate increase, blanket max-window change, or generic school hook G.

For each new route, require a continuous climb from the current ceiling, a real eligible repeatable use, and Base 199.9 to 200 with worn bonuses, plus no gain above the character's cap. Lower loop caps, resource costs, skill locks, normal success/effects, and one SkillUsed event per use must survive. P283's suggested content names are proposals, not existing code or fresh authority to implement them in this notes-only task.

## Verification and limits

Existing tests were read as evidence of intended coverage, not rerun. `T/Skills/SkillGainRateVerification.cs:166-230` models Swordsmanship, Tactics, Blacksmithy, Mining, Magery, and Imbuing; it is not a per-group content implementation. `SkillGainPastStockCeilingVerification.cs` and `SkillGainRowKeysVerification.cs` cover the existing hooks and their caller keys. They do not establish that the proposed wards, high animals, orders, maps, locks, or bard encounters exist. This is a coverage distinction, not a repetition of P443's test findings.

No new tests or gates were written; lane tests are none. No test, build, game client, container, live configuration, or Haven connection was used. Actual flags, recipe/ingredient/encounter access, deployment state, training times, exhaustive creature requirements, and runtime reproduction of the Focus boundary remain unverified. No decision documents were edited. The requested long-name run note links to this comparison so both filenames in the task are honored without duplicating the research.

Editorial checks counted 58 unique skill entries across the group tables and verified the named 23/16 partition, local Markdown links, cited source file existence, no em dashes, and no trailing whitespace. Ran `tools/progress.py --dry-run` with both work-copy path overrides; exit zero. Its known progress.json write was restored byte for byte, leaving only the requested notes. Both notes are below 5 MB. Stop requests were checked between steps.

P518 DONE
