# cc-P54 group B: MAGIC skills, gain ceilings at the 200 cap

Scope: Magery, Evaluating Intelligence, Resisting Spells, Meditation, Inscription, Necromancy, Spirit Speak, Chivalry,
Spellweaving, Mysticism, Imbuing, Ninjitsu. Read-only research; nothing built or edited.

Paths: pinned = D:\UO\ModernUO-pinned\Projects at d4531cd94b739613155225c234900de9f47d2c88 (git rev-parse HEAD checked).
C\ = D:\ShatteredLegacy\server\customizations, P\ = D:\ShatteredLegacy\server\patches. Expansion EJ, so only AOS
branches are live; every "!Core.AOS" or "else" (pre-AOS) gain site is listed as dead.

## 0. Gain rules used (verified on d4531cd94)

- UOContent/Skills/SkillCheck.cs: CheckLocation reads skill.Value (:58); Value < min -> false, no roll (:62);
  Value >= max -> true, no roll, "No challenge" (:67); chance = (Value-min)/(max-min) (:70). CheckTarget same at
  :180/:184/:189/:192. Direct checks: chance >= 1.0 -> no roll (:100, :220). Gain needs Base < Cap (:248).
- C\ClusterFSkillGain.cs:63-111 wraps all four handlers; it re-runs the pinned handler with the SAME min/max/chance
  (3 attempts, 5x amount, :97-150), so no ceiling below is changed by it.
- "Ceiling" below is the highest skill VALUE at which a use still rolls (Value < max, or direct chance < 1).
  Caveat for every "Cap" use: Value includes item bonuses, so a player wearing +X stops rolling at Base = Cap - X until
  the items come off. This was already true before cc-P53 (ObeyCap clamped Value at Cap, Server/Skills.cs:317-327, so
  Value >= Cap then too). cc-P53's line "skill gain reads Base, never Value" is true for SkillCheck.cs:248 but not for the
  window test at :58-67, which reads Value.
- Non-use route, out of scope: Scrolls of Transcendence add Base directly up to Cap
  (Items/Special/Special Scrolls/ScrollofTranscendence.cs:81-92, :128). Whether they drop on the shard: unverified.

## (i) Table

| Skill | Gain calls (file:line, pinned/ours, min/max or chance) | Ceiling now | P20 ceiling (confirmed/corrected) | Reaches 200? |
|---|---|---|---|---|
| Magery | (1) Spell.cs:628 CheckSkill(CastSkill, min, max), pinned; window MagerySpell.cs:15-17, :41-42: book circle c min = ML table [-18,-4,10,24,38,52,66,80], max = min+40 (8th = 80-120); scroll uses index c (8th scroll 52-92). Recall.cs:106-119 sets 0/0 for runebook/Wraith (no roll). Wands skip (Spell.cs:616-619). (2) CraftItem.cs:893 (pinned, file patched by P\CraftItem-shard-hooks.patch; gain loop untouched) fed by DefCarpentry.cs:498 Pentagram 75-80 and :501 Abbatoir 50-55 (pinned) and C\Engines\Craft\TinkeringCraftRegistrations.cs:71 Void Orb 80-100 (ours). 3 sources, 4 windows. | 120 (8th circle from a book) | 120 confirmed; P20's "nothing else gains Magery" corrected (the 3 craft windows, all <= 100) | STALLED 120 |
| Evaluating Intelligence | (1) Spell.cs:625 CheckSkill(DamageSkill, 0, Cap) on every Magery and Mysticism cast (DamageSkill = EvalInt, Spell.cs:52; MysticSpell overrides only GetDamageSkill, MysticSpell.cs:42-44), pinned. (2) SpellHelper.cs:323 buff 0-120. (3) SpellHelper.cs:370 curse 0-120. (4) Skills/EvalInt.cs:75 0-120. All pinned. 4 sites. | Cap (200) via (1) | Cap confirmed | REACHES: any Magery or Mystic cast (not a wand) while Value < Cap |
| Resisting Spells | Live in AOS, 8 sites: (1) MagerySpell.cs:55 GetResistSkill, CheckSkill(0, Cap) only while Value < 1+10c+(1+c/6)*25 (:51-53); AOS callers Paralyze.cs:42 (5th, gate 66), ManaDrain.cs:41 (4th, 56), ManaVampire.cs:41 (7th, 111). (2) MagerySpell.cs:82 CheckResisted, CheckSkill(0, Cap) only while Value < (1+c)*10+(1+c/6)*25 (:78-80), and only if 0 < n < 1 (:65-73); AOS callers Third/Poison.cs:35 (3rd, 55) and BaseWeapon.cs:3461 HitDispel via DispelSpell (6th, 85). (3) MysticSpell.cs:121, same gate (:116-119); caller BombardSpell.cs:62 (6th, 85). (4) SpellHelper.cs:371 curse 0-120. (5)-(8) PainSpike.cs:59, MindRot.cs:58, CorpseSkin.cs:70, BloodOathSpell.cs:82, each 0-120. All pinned. Dead (pre-AOS only): FireHorn.cs:175, FireField.cs:144, :241, and every Magery CheckResisted in an else branch (MagicArrow:52, Harm:42, Fireball:43, Lightning:42, ManaDrain:61, Paralyze:62, MindBlast:96, EnergyBolt:44, Explosion:88, FlameStrike:42, ManaVampire:48, ChainLightning:78, MeteorSwarm:87). | 120 (curse and necro sites); the Magery/Mystic gates top out at 111 | 130 CORRECTED to 120: 130 is the 8th-circle CheckResisted gate, but no 7th/8th-circle spell calls CheckResisted in AOS (Flame Strike, Mana Vampire, Chain Lightning, Meteor all use it only pre-AOS) | STALLED 120 |
| Meditation | (1) C\Meditation.cs:115 CheckSkill(Meditation, 0, Cap) on a successful trance start (ours; replaces pinned Skills/Meditation.cs:80, 0-100). (2) C\RegenRates.cs:140 -> :28-42 passive direct chance n = cur/max*(1-v)+v, v = sqrt(0.005*Value) (ours, copy of pinned). 2 sites. | 200 (active: Cap; passive: v = 1 at Value 200) | Cap / 200 confirmed (both are now 200) | REACHES: active meditation while Value < Cap; passive regen while mana not full |
| Inscription | (1) Skills/Inscribe.cs:237 copy a book 0-50 (CheckTargetSkill), pinned. (2) CraftItem.cs:893 fed by DefInscription.cs (pinned): Magery scrolls by circle :133-180 (8th 75-125 at :179-180), necro scrolls min..min+1 (:214), mystic scrolls up to 75-125 (:608-609, :619-620), Enchanted Switch/Runed Prism/Runebook 45-95 (:409, :425, :434), BOD book 65-115 (:440), Spellbook 50-126 (:445), Mystic Spellbook 50-150 (:463). | 150 (Mystic Spellbook) | 150 confirmed | STALLED 150 |
| Necromancy | Spell.cs:628 with NecromancerSpell.cs:37-41: min = req, max = req+40, scroll max = min (no roll); top Exorcism.cs:67 and VengefulSpirit.cs:25 req 80 -> 120; VampiricEmbrace.cs:32-42 80-120. Pinned. 1 site. | 120 | 120 confirmed | STALLED 120 |
| Spirit Speak | (1) Spell.cs:625 CheckSkill(DamageSkill, 0, Cap) on every necro cast (DamageSkill = SpiritSpeak, NecromancerSpell.cs:15). (2) Skills/SpiritSpeak.cs:32 0-100. (3) SpiritSpeak.cs:159 0-120. Pinned. 3 sites. | Cap (200) via (1) | Cap confirmed | REACHES: any necro cast while Value < Cap (scrolls too: :625 runs before the cast check) |
| Chivalry | Spell.cs:628 via PaladinSpell.cs:51-80 (CheckFizzle -> base) and :126-130 (req..req+50); top NobleSacrifice.cs:28 req 65 -> 115. DamageSkill = CastSkill (:16-17), so no :625 roll. Pinned. 1 site. | 115 | 115 confirmed | STALLED 115 |
| Spellweaving | Spell.cs:628 via ArcanistSpell.cs:85-89 (req-12.5..req+37.5); top WordOfDeath.cs:16 req 80 -> 117.5. DamageSkill = CastSkill (:18-19). Pinned. 1 site. | 117.5 | 117.5 confirmed | STALLED 117.5 |
| Mysticism | Spell.cs:628 via MysticSpell.cs:46-54 (req-12.5..req+37.5, req table :9, top 83) -> 120.5. Pinned. 1 site. | 120.5 | 120.5 confirmed | STALLED 120.5 |
| Imbuing | C\ArtificersImbueGump.cs:1485 CheckSkill(diff-20, diff+20); diff = 40 + (maxDiff-40)*fraction, maxDiff = 100 + (pct-100)*0.2 (SkillDifficulty :120-127), pct <= 200 at standing >= 40000 (:1766-1773) -> diff <= 120. :1563 disenchant 20-80. :1625 essence craft 20-80. All ours (pinned has no Imbuing use; MysticSpell.cs:42-44 only reads it). 3 sites. | 140 | 140 confirmed | STALLED 140 |
| Ninjitsu | (1) Spells/Ninjitsu/AnimalForm.cs:212 CheckSkill(0, 37.5) on a successful morph (the :194 req..req+37.5 check is inside a /* */ comment, :193-199; AnimalForm.CheckFizzle => true, :112). (2) Spell.cs:628 via NinjaSpell.cs:62-90 (req-12.5..req+37.5): Mirror Image req 20 -> 57.5, Shadowjump req 50 (ShadowJump.cs:26) -> 87.5. (3) NinjaMove.cs:9 CheckGain(req-12.5, req+37.5) from Backstab.cs:59 (77.5), FocusAttack.cs:61 (67.5), SurpriseAttack.cs:66 (97.5), KiAttack.cs:81 (117.5), DeathStrike.cs:77 (122.5). (4) Items/Skill Items/Ninjitsu/NinjaWeapons.cs:274 direct chance (Fukiya / ninja belt shuriken, CombatCheck :202-275): chance = (N+20)(100+HCI) / (2(D+20)(100+DCI)), HCI and DCI each capped 45, floor 0.02; D = defender's weapon defend skill (BaseWeapon.cs:1205-1206). Pinned. 4 live sites. | 200 (Cap) via (4) whenever N < 2(D+20)(100+DCI)/(100+HCI) - 20; with HCI 0 and DCI 0, any defender with D > 90 | 137.5 CORRECTED to 200. P20's 137.5 came from the commented-out AnimalForm check (old :186, same comment on 7c9215d97); the live Animal Form roll is 0-37.5 and the best special move is Death Strike 122.5. P20 missed the ninja weapons. | REACHES: Fukiya or shuriken against a target with defend skill > 90 (e.g. Monsters/AOS/BoneDemon.cs:37 Wrestling 100, Animals/Mounts/Hiryu.cs:37 100.1-120), shooter carrying no HCI |

Counted: 4 reach 200 (Evaluating Intelligence, Meditation, Spirit Speak, Ninjitsu), 8 stalled (Magery 120, Resisting
Spells 120, Inscription 150, Necromancy 120, Chivalry 115, Spellweaving 117.5, Mysticism 120.5, Imbuing 140).

Side note from the table: the achievement "skills.magery_elite" (C\ClusterFAchievements.cs:683-688) needs Magery
Base >= 200 (:1068). Magery Base stops at 120 by play, so it is earnable today only by admin edit or Transcendence.

## (ii) Proposals for the stalled skills

### Shared: the five casting schools (Magery, Necromancy, Chivalry, Spellweaving, Mysticism)

All five stall for the same reason: the only gain is Spell.cs:628, whose window is fixed by the hardest spell of the
school, and every school's cast success is already 100 percent at its ceiling.

- (a) rejected. Raising the cast window's max to Cap changes cast SUCCESS (the same roll decides the fizzle,
  Spell.cs:628), so it would make OSI-range casting fail more; a separate gain-only roll on the cast (like the
  DamageSkill roll at :625) has no difficulty at all past 120: every 1st-circle cast would train a 199.9 mage. The rule
  allows (a) only when the difficulty still means something past 160; for casting it does not.
- (b) none available. No spell is harder than the top circle, scrolls are easier (MagerySpell.cs:41, NecromancerSpell.cs:40),
  and the only craft windows that train Magery stop at 100 (DefCarpentry.cs:498, :501; ours TinkeringCraftRegistrations.cs:71).
  Making the Void Orb window 160-200 would be a tinker recipe training Magery, not a casting use. No cast window takes a
  target or material input.
- (c) proposed: an Arcane Training Ward, ours. A stationary BaseCreature (new file, e.g. C\ArcaneTrainingWard.cs) in
  tiers T = 140 / 160 / 180 / 200 (window T-40..T, the pinned TrainingDummy idea, Items/Addons/TrainingDummies.cs:67,
  applied to spells). It overrides BaseCreature.OnHarmfulSpell(Mobile from) (pinned virtual, Mobiles/BaseCreature.cs:1995;
  called from Spell.cs:193-196 and SpellHelper.cs:931, :1010) and, when from is a player and from.Spell is a Spell of a
  casting school whose Value is at or above the gate, rolls from.CheckSkill(spell.CastSkill, T-40, T). The roll's result
  is ignored, so nothing about the spell changes. The ward ignores damage (AlterSpellDamageFrom to 0; AOS.Damage drops
  damage <= 0, Misc/AOS.cs:52 per P20, not re-read) and never dies. Placed by an existing seeder (C\ClusterFGuildHallSeeder.cs
  or the League hall).
  Gate: the school's current ceiling (Magery 120, Necromancy 120, Mysticism 120.5, Chivalry 115, Spellweaving 117.5).
  Which spells reach the hook (verified call sites): explicit Spell.HarmfulSpell in Clumsy, Feeblemind, Weaken, Curse,
  Mass Curse, Paralyze, Poison, Mana Drain, Mana Vampire (Magery) and Blood Oath, Corpse Skin, Evil Omen, Mind Rot,
  Pain Spike, Strangle (Necromancy); zero-delay SpellHelper.Damage(spell, ...) in Holy Light (Chivalry, HolyLight.cs:77),
  Word of Death, Thunderstorm, Essence of Wind (Spellweaving), Bombard, Eagle Strike, Hail Storm, Nether Cyclone,
  Spell Plague (Mysticism). Unverified: that from.Spell is still set when each of these reaches the hook (it is cleared
  at FinishSequence); delayed-damage spells reach SpellHelper.Damage from a timer and probably will not count. If that
  fails for a school, the fallback is to record the caster's last spell in a guild-hall Region.OnSpellCast override
  (pinned virtual, called at Spell.cs:965). A builder fact must establish this per school.
  Alternatives argued (AGENTS.md: argue before patching): gain-only roll in Spell.CheckFizzle (one pinned patch, S, but
  no difficulty, see (a)); League or guild contract turn-ins rolling checks like the smith BODs
  (C\ClusterFSmithBODSystem.cs:277-282), rejected for now because no mage contract system exists (the work orders in
  C\ClusterFWorkOrderSystem.cs are item deliveries with no gain roll).

Per school:

- Magery (120). (c) ward. Files: new C\ArcaneTrainingWard.cs (ours), one line in a seeder (ours). No pinned patch.
  Fidelity: nothing changes below 120 (gate 120; the ward is new content). Exploit check (six known): none worse. Magery
  feeds Reveal (Sixth/Reveal.cs:32, :62-85: radius 1 + Mag/20, chance 50*(Mag+DH)/(Hide+Stealth)), so 200 Magery
  reveals hiders better: it counters "guards cannot reveal hiders from 121", it does not worsen it. New in 160-200 (Value
  160-200 is already partly reachable with Magery items, e.g. C\Items\Artifacts\Equipment\Jewelry\CrystallineRing.cs:17
  +20, now above cap after cc-P53): Earthquake radius 11 -> 14 tiles (Eighth/Earthquake.cs:41), Greater Heal 81-90
  (Fourth/GreaterHeal.cs:51), Energy Field 59 s (Seventh/EnergyField.cs:45), Paralyze Field 69 s (Sixth/ParalyzeField.cs:48),
  Fire Field 104 s (Fourth/FireField.cs:51), summons 800 s. All scale; none crosses a P20 BREAK threshold (those are at
  500-1000).
- Necromancy (120). (c) ward. Same files. Fidelity: none below 120. Exploit check: none relevant. New in 160-200: none;
  Necromancy only gates spells and clamps (P20); spell power is Spirit Speak, which already reaches 200.
- Chivalry (115). (c) ward via Holy Light (the only damaging Chivalry spell). Same files. Fidelity FLAG: with the gate at
  115 the ward adds a gain source between 115 and 120, inside the OSI range where pinned has none (the HS Divine Fury
  tier at Chivalry 120, DivineFury.cs:46, is unreachable by casting today). Gating at 120 instead keeps OSI-range gain
  exactly as pinned but leaves Base 115-120 reachable only with item bonuses (Value). Chase decides. Exploit check: none.
  New in 160-200: none; Chivalry clamps at 120-230 (P20).
- Spellweaving (117.5). (c) ward via Word of Death / Thunderstorm / Essence of Wind. Same files. Fidelity FLAG: same as
  Chivalry for 117.5-120. Exploit check: none of the six. New in 160-200: Arcane Circle only joins weavers within 20 skill
  (ArcaneCircle.cs:117, :134), so a 200 weaver can no longer circle with 120 players; Attune Weapon absorb at 200 is
  75 + 6F (AttuneWeapon.cs:55), Word of Death 40-66 (WordOfDeath.cs:56-57). Scales, no break.
- Mysticism (120.5). (c) ward via the Mystic damage spells. Same files. Fidelity: none below 120 (gate 120.5).
  Exploit check: none. New in 160-200: Mysticism adds to Nether Cyclone drain (NetherCycloneSpell.cs:73), Cleansing Winds
  heal, Stone Form and Animated Weapon level ((M+I)/2) and lowers targets' resist chance (MysticSpell.cs:131-132).
  Spell damage reads max(Imbuing, Focus), not Mysticism. At 200/200 Nether Cyclone drains 0.333 - R/800 of stamina and
  mana; Animated Weapon level 200 (Wrestling and Resist 200). Scales; P20's breaks are at 500-1000.

### Resisting Spells (120)

- (a) proposed. The five live 0-120 sites (SpellHelper.cs:371 and the four necro sites) are gain-only rolls on a hostile
  spell that landed; their results are ignored. Past 160 the difficulty still means something: the curse is
  8 + (EI - R)/10 percent (SpellHelper.cs:384) and the necro effects are SS - R, and casters reach EI 200 and SS 200 by
  play (both rows above). Rule: max stays 120 while Value < 120, and becomes Cap once Value >= 120.
  Where: ours, one table entry in C\ClusterFSkillGain.cs (in ClusterFSkillCheckLocation, :63-68: for players, when
  skillName == MagicResist and maxSkill == 120.0 and Value >= 120, pass skill.Cap). Every MagicResist check with max 120
  that is live in AOS is one of those five; the only other one, FireHorn.cs:175, is pre-AOS. Because the five sites
  ignore the return value, changing the max cannot change any outcome. Alternative: five one-line pinned patches
  (SpellHelper.cs:371, PainSpike.cs:59, MindRot.cs:58, CorpseSkin.cs:70, BloodOathSpell.cs:82), or just SpellHelper.cs:371
  (curses are the common NPC mage cast). Rejected as the default because they are pinned patches and the wrapper reaches
  all five with no patch; the cost of the wrapper route is a magic-number match, which the builder's fact must pin down.
  A refinement, needing the SpellHelper patch: roll only when the curse was not fully resisted (curse > 0).
- (b) and (c) not needed.
- Fidelity: none below 120 (the window is exactly pinned's until Value 120).
- Exploit check: none of the six is fed by Resisting Spells. New in 160-200 (FLAG):
  - Nether Cyclone sign flip: the drain is (M+I)/1200 - R/800 (NetherCycloneSpell.cs:73, :81-84). Against a 120/120
    mystic it is 0 at R 160 and NEGATIVE above it, so the spell GIVES the victim stamina and mana (-5 percent of max at
    R 200). Against a 200/200 mystic the flip is at R 267. Fix belongs with this batch: clamp resistedReduction at 0
    (one pinned patch, or leave R lift off until it lands).
  - Resist floor (PlayerMobile.cs:1196-1214): 40 + (fixed-1000)/50, so 52 at 160 and 60 at 200 in all five resists with
    no gear; still under the 70 cap, and the curse/debuff override P20 flagged starts at 250.
  - Stat curses: 0 percent against casters with EI <= R - 80 (SpellHelper.cs:384); at R 200, immune to EI 120 curses.
    Magery/Mystic CheckResisted at R 200: about 82 percent vs a Magery 120 Poison, 75 percent vs a Mysticism 120
    Bombard (MagerySpell.cs:88-96, MysticSpell.cs:127-136), not "always" (that starts at R 235 vs a 120 caster).
  - Spell Plague: first-explosion chance 90 - 3*13 = 51 percent at R 200 (SpellPlagueSpell.cs:148-155); immunity is at 370.
  - Necro durations stay positive at R 200 vs SS 120 (Mind Rot 4 s, Corpse Skin 8 s, Pain Spike 10); they hit 0 when
    R - SS >= 100.

### Inscription (150)

- (a) rejected: the windows are craft recipes; raising Mystic Spellbook's max (DefInscription.cs:463) changes its
  success chance at every skill (CraftItem.cs:904), an OSI-range change, and a book is not harder past 150.
- (b) none: Inscription recipes take no material tiers.
- (c) proposed: new high-tier Inscription recipes, registered additively the way C\Engines\Craft\TinkeringCraftRegistrations.cs
  does (DefTinkering.CraftSystem appended at ServerStarted). New file C\Engines\Craft\InscriptionCraftRegistrations.cs
  (ours) with windows whose min is >= 120 and whose top max is 200 (e.g. 120-160, 140-180, 160-200, the smith BOD shape).
  The items themselves are a design decision for Chase (none chosen here); without a useful product this is a gold sink
  with a gain roll. If the recipes form a new group, Inscription goes from 11 to 12 categories, which is the paging that
  cc-P53 Part E added (P\CraftGump-category-pages.patch); test that the group shows on page 2.
- Fidelity: none below 120 if every new min is >= 120.
- Exploit check: none of the six. New in 160-200: the spell damage integer bug (Spell.cs:222-223,
  (fixed + 1000*(fixed/1000))/200) gives +20 percent at 200 instead of the intended 15; Reactive Armor +25 phys
  (ReactiveArmor.cs:194); Magic Reflect -15 (MagicReflect.cs:86) and Protection -5 phys / -25 Resist (Protection.cs:138-139)
  are still maluses (they invert at 300-500). Fix the integer bug in the same batch or accept +5 percent.

### Imbuing (140)

- (a) rejected: the imbue roll decides success (C\ArtificersImbueGump.cs:1485), so a Cap max would lower success at
  every skill.
- (b) proposed, ours: make the existing hardest targets harder. Add an item-load term to SkillDifficulty (:120-127):
  +20 difficulty per property already on the item beyond 4, so the 8th slot (8 slots at standing >= 15000, :1775-1781)
  on a 200 percent imbue gives diff 120 + 60 = 180, window 160-200. Callers that compute diff (:954, :982, :1425) must
  pass the item, and the gump's displayed chance (:1760-1764) must use the same diff.
- Fidelity FLAG: pinned has no Imbuing, so no OSI-range pinned behavior changes, but this is our system and it lowers
  success for 6th-8th slot imbues at every skill level (a 120 imbuer filling slot 8 at 200 percent drops from 100 to
  about 0 percent at diff 180). Alternative that changes nothing below 140: apply the load term only when the item is
  already at the player's intensity cap... rejected as harder to explain. Chase decides.
- Exploit check: none of the six. New in 160-200: none. Imbuing past 140 only feeds Mysticism damage through
  max(Imbuing, Focus) (MysticSpell.cs:42-44), and Focus already reaches 200 by passive regen (C\RegenRates.cs:28-42,
  :95, :152), so Mystic damage at 200 is reachable today.

## (iii) Line moves vs P20 (P20 audited 7c9215d97; re-verified on d4531cd94)

Unchanged (confirmed): Spell.cs:614-629 and :623-626 (CheckFizzle); MagerySpell.cs:15-17, :41-42, :51-56, :77-83,
:88-97; SpellHelper.cs:323, :370, :371; EvalInt.cs:75; PainSpike.cs:59; MindRot.cs:58; CorpseSkin.cs:70;
NecromancerSpell.cs:37-41; VampiricEmbrace.cs:32-42; SpiritSpeak.cs:32, :159; PaladinSpell.cs:126-130; DivineFury.cs:46;
ArcanistSpell.cs:85-89; MysticSpell.cs:9, :42-44, :46-54, :116-122; NinjaMove.cs:9; AnimalForm.cs:49-50;
C\RegenRates.cs:35-41 (passive check) and :82 (animal form regen, P20 :80-85); C\ClusterFSkillGain.cs:97-150.

Moved:
- BloodOathSpell.cs:85 -> :82.
- C\Meditation.cs:92 (active gain) -> :115; :83 (start chance) -> :106; :46-59 (armored block) -> :69-82; :85-87 -> :108-110.
- C\RegenRates.cs:156-165 (armored medPoints) -> :155-164.
- DefInscription.cs:457 (Mystic Spellbook) -> :463; :439 (Spellbook) -> :445; :173-174 -> :179-180 (8th circle 75-125;
  P20's "7th-circle mystic 60.7-110.7" is not the top: mystic 8th-circle scrolls are 75-125 at :608-609, :619-620).
- Crafting gain: P20 cited shard CraftItem.cs:855-913 as a full replacement; CraftItem.cs is now pinned plus
  P\CraftItem-shard-hooks.patch, gain at pinned CraftItem.cs:893 (post-patch line not computed).
- C\ArtificersImbueGump.cs: :85-92 -> :120-127 (SkillDifficulty); :1406 -> :1485; :1478 -> :1563; :1533 -> :1625;
  :1661-1665 -> :1760-1764; :53-60 (standing caps) -> :1766-1781.
- AnimalForm.cs:186 -> :194, and it is commented out on both commits; the live roll is :212 (old :204), 0-37.5.

Corrected ceilings: Resisting Spells 130 -> 120; Ninjitsu 137.5 -> 200.

## (iv) Batch sizing

| Batch | Size | Files (ours / pinned) | Facts a builder needs |
|---|---|---|---|
| R: Resist lift | S | C\ClusterFSkillGain.cs (ours). Optional fix shipped with it: NetherCycloneSpell.cs:81 clamp at 0 (pinned patch, argue first). | (1) Player R 119.9 cursed: the roll uses max 120 (pinned window). (2) R 150 and 199.9 cursed or Pain Spiked: a gain can occur. (3) R at Cap: no gain. (4) EvalInt's SpellHelper.cs:323/:370 0-120 rolls unchanged; creatures unchanged. (5) Spell outcome identical with and without the lift. (6) If the clamp ships: R 200 vs a 120/120 Nether Cyclone, victim stamina and mana do not rise. |
| W: Arcane Training Ward | M | new C\ArcaneTrainingWard.cs, one seeder line (C\ClusterFGuildHallSeeder.cs or League hall), all ours. No pinned file. | Per school, one spell per hook path: the ward rolls CheckSkill(school, T-40, T) when Value >= gate and does not roll below it; T 200 rolls at 199.9 and not at 200; the ward takes no damage and cannot die; it gives no Resist gain; anti-macro still applies; which spells count with from.Spell (record per school; delayed-damage spells expected not to). |
| N: Inscription recipes | M (L if the items need new behavior) | new C\Engines\Craft\InscriptionCraftRegistrations.cs plus item classes, ours. Touches the cc-P53 category paging only by adding a group. | Registration idempotent; windows as specified (no min below 120); a 199.9 scribe gains on the top recipe, a 200 does not; group visible on Inscription page 2. |
| I: Imbuing load term | S | C\ArtificersImbueGump.cs (ours). | Diff unchanged for items with 0-4 properties; 8th slot at 200 percent = 180; displayed chance equals the rolled chance; Imbuing 199.9 can gain on that imbue. |

cc-P53 overlap: none of these touch C\Meditation.cs or C\RegenRates.cs (the files cc-P53 changed). cc-P53 cites
C\ClusterFSkillGain.cs:141-147 (ShouldBoost) without changing it; batch R edits that file. Batch N meets cc-P53's
craft-gump paging (P\CraftGump-category-pages.patch) as a consumer, no edit.

Not proposed (already reach 200): Evaluating Intelligence, Meditation, Spirit Speak, Ninjitsu. Note for Ninjitsu: it
reaches 200 today, so its 160-200 effects are live now (Dog/Cat form regen +N/3 points outside the 18 cap,
C\RegenRates.cs:82: +66 points = about 6.7 HP/s at 200; Focus Attack +92 percent; Surprise Attack malus 33).
