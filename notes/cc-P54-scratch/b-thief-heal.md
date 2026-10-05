# cc-P54 b: thief and healer group, can each skill still gain to 200?

Skills: Hiding, Stealth, Detect Hidden, Snooping, Stealing, Lockpicking, Remove Trap, Poisoning, Healing, Veterinary,
Begging, Forensic Evaluation.

Paths: pinned = D:\UO\ModernUO-pinned\Projects at d4531cd94b739613155225c234900de9f47d2c88 (verified with
`git rev-parse HEAD`). C\ = D:\ShatteredLegacy\server\customizations, P\ = D:\ShatteredLegacy\server\patches.
Read-only research; nothing was built or run.

## Ground rules used (re-verified on d4531cd94)

- CheckLocation / CheckTarget read `skill.Value` (SkillCheck.cs:58, :180), not Base. `value < min` gives false and no
  gain (:62, :184). `value >= max` or `min >= max` gives true with NO gain roll (:67, :189). Direct-chance checks:
  `chance >= 1.0` gives no gain roll (:100, :220). Gain needs `skill.Base < skill.Cap` (:248).
- Because the ceiling test uses Value, every +X item or Animal Form bonus lowers the Base ceiling by X. cc-P53 Part C
  lets item bonuses run above cap, so this matters more now. Of my 12 skills, the random-item pool can roll Healing,
  Veterinary, Stealing and Stealth (pinned `Items/Skill Items/Tools/BaseRunicTool.cs:26,33,41,42`). Animal Form adds
  Stealth +20 and Stealing +10 (per cc-P53 table, `AnimalForm.cs:237,245`, not re-read). I found no pinned or C\ source
  of a Hiding or Detect Hidden bonus (searched SetValues / SkillMod / `SkillName.Hiding,` in pinned UOContent and C\).
- C\ClusterFSkillGain.cs wraps all four handlers (:63-95), repeats the attempt up to `_chanceAttempts` times and
  multiplies the gain amount (:97-137). It passes min/max/chance through unchanged. `ShouldBoost` (:141-147) is
  players only, Base < Cap.
- C\Meditation.cs:115 (not :92) is the pattern (a) reference: `m.CheckSkill(SkillName.Meditation, 0.0, Cap)`.
- AntiMacro is off by default (pinned `Skills/AntiMacroSystem.cs:96`). I did not check the shard's modernuo.json.
- Shard code search: I grepped all of C\ and P\ for `SkillName.<each of the 12>` and for every
  `Check(Target|Direct)?Skill` call. C\ has no gain call that names any of the 12 skills. The only C\ files that
  replace pinned files and contain a CheckSkill are C\Meditation.cs and C\RegenRates.cs:41 (Meditation / Focus regen,
  not in my group). Patches that touch my files: P\Bandage-pet-mimic-targeting.patch (adds a PetMimic branch; hunks
  `@@ -118,6 +118,12 @@` and `@@ -130,6 +136,10 @@`, so in the patched build Bandage.cs:444-445 sits at 454-455;
  computed from the hunk headers, not built), and P\BaseCreature-PlayerMobile-can-auto-stable.patch (shifts
  BaseCreature.cs lines; not my formulas). No shard file replaces Hiding, Stealth, DetectHidden, Snooping, Stealing,
  LockPick, RemoveTrap, Poisoning, Begging or ForensicEval (`replace_file` list in
  D:\ShatteredLegacy\docker\uo\apply-patches.sh:233-245).
- Shard chests: C\Items\Containers\TreasureChestMod.cs (Shame "Treasure Chest Pack") sets `MaxLockLevel =
  RequiredSkill` (52/56/72/84/92, :24-26, :59-61, :106-108, :150-152, :245-247) and `TrapPower = level *
  Utility.Random(1, 25)` (top: 4 x 25 = 100, :249). F-32 Despise chests are pinned `TreasureChestLevel1-4`
  (C\ClusterFDespiseStockSpawns.cs:37-38). C\Mobiles\Bosses\StygianDragon.cs:147 drops a pinned ParagonChest level 5.
  C\ClusterFWorkOrderSystem.cs uses `skillRequired` only as a gate and makes no gain call. No League, contract,
  trainer or dummy code in C\ names any of my skills.

## (i) Table

| Skill | Gain calls (file:line, pinned/ours, min/max or chance) | Ceiling now | P20 ceiling | Reaches 200? |
|---|---|---|---|---|
| Hiding | Skills/Hiding.cs:73, pinned, (0-bonus, 100-bonus); bonus = 100 in a house where you are a friend (:34-37), so (-100, 0) there. SmokeBomb.cs:40 and EggBomb.cs:46 go through UseSkill(Hiding), the same call | 100 (0 in a friend's house) | 100: confirmed | STALLED at 100 |
| Stealth | Skills/Stealth.cs:96-100, pinned, (-20+2AR, 60+2AR); AR >= 42 blocks the use (:91) | 60+2AR: 60 unarmored, max 142 at AR 41 | 60 / 142: confirmed | STALLED at 142 |
| Detect Hidden | Skills/DetectHidden.cs:151 pinned (0,100) trapped container; :175 pinned (0,100) area scan (fail halves range); :220 pinned CheckTarget (80,100) faction trap | 100 | 100: confirmed, lines moved | STALLED at 100 |
| Snooping | Skills/Snooping.cs:84, pinned, CheckTarget (0,100) | 100 | 100: confirmed | STALLED at 100 |
| Stealing | Skills/Stealing.cs:185 pinned (80,80) sigil, min >= max so no gain ever; :285-289 and :300-304 pinned, stacks, (pile-22.5, pile+27.5) with pile = ceil(unitWeight x amount) x 10, amount = RandomMinMax(1, (int)(Value/10/unitWeight)) (:272-278); :316 pinned single item (iw-22.5, iw+27.5), iw = ceil(weight) x 10 <= 100 (:263 limit 10 stones, :33); Items/Addons/PickpocketDips.cs:61 pinned (MinSkill, MaxSkill) = (-25, +25) by default (:22-23), refused at Base >= MaxSkill (:85) | single item 127.5; stacks: no fixed ceiling (pile max is ceil(S/10) x 10, so max = that + 27.5 > S at every S) | 127.5: CORRECTED (P20 counted only the single-item path) | REACHES 200 via stacks (see note) |
| Lockpicking | Items/Skill Items/Thief/LockPick.cs:128, pinned, CheckTarget (LockLevel, MaxLockLevel); gate Value >= RequiredSkill (:121). Highest MaxLockLevel that exists: 140 (TreasureMapChest.cs:197-207 level 5-6 Req 100 -> 90..140; ParagonChest.cs:100-111 level 5 same; LesserArtifacts.cs:465-467 ToT 95..140). Others: camps 66..116; BaseTreasureChest.cs:88-97 Req = LockLevel up to 120 with Max 100 (min >= max, no gain); TreasureChestLevel1-4 Req 92 +/-10 -> max 102; tinker-made LockableContainer.cs:34-38 max 95; ours TreasureChestMod max 92 | 140 | 140: confirmed (TMap line moved 190 -> 197-207) | STALLED at 140 |
| Remove Trap | Skills/RemoveTrap.cs:61, pinned, CheckTarget (TrapPower, TrapPower+30); :96 pinned (80,100) faction trap (plus Tinkering (80,100) at :97). TrapPower sources: TreasureMapChest.cs:194 level x 25 (max level 6 -> 150); ParagonChest.cs:96 (L5 125); LesserArtifacts.cs:471 100; FillableContainer.cs:167 level x 10..30 (max level 3 -> 90); TreasureChestLevel4.cs:16 4 x 10..25 -> 100; camps 30-40; MagicTrap 10-50; ours TreasureChestMod max 100; tinker trap DefTinkering.cs:678-681 TrapPower = (int)(Tinkering/10) x 9 | world 180 (TMap L6); tinker traps 9 x floor(T/10) + 30: 201 at Tinkering 190-199.9, 210 at 200 | ~180 world / 0.9T+30: confirmed; max TMap level 6 now verified (P20 said unverified); DefTinkering line moved | REACHES 200 only if a Tinkering >= 190 trapper exists (conditional) |
| Poisoning | Skills/Poisoning.cs:124, pinned, CheckTarget (potion Min, Max): Lesser 0-60, Regular 30-70, Greater 60-100, Deadly / Darkglow / Parasitic 95-100 (the six potion files, :13-16). Mobiles/BaseCreature.cs:2695 pinned (0, Cap), controlled pets only | 100 (players) | 100: confirmed (pet line moved 2354 -> 2695) | STALLED at 100 |
| Healing | Items/Skill Items/Misc/Bandage.cs:445 (primary) / :444 (secondary), pinned-but-patched (P\Bandage-pet-mimic-targeting.patch shifts to :455/:454), CheckLocation (0,120), result ignored; fires when a heal, cure or res is attempted with checkSkills true (:240 res, :322 cure, :372 heal). BaseCreature.cs:5773 (0, 60+10 x poisonLevel) and :5805 (0,90): creature self-heal, not players | 120 (players) | 120: confirmed (BaseCreature lines moved 5366-5408 -> 5773, 5805) | STALLED at 120 |
| Veterinary | Bandage.cs:444-445 (same call; primary = Veterinary on animal patients, :179) (0,120) | 120 | 120: confirmed | STALLED at 120 |
| Begging | Skills/Begging.cs:111, pinned, CheckTarget (0,100) | 100 | 100: confirmed | STALLED at 100 |
| Forensic Evaluation | Skills/ForensicEval.cs:36 pinned (40,100) on a mobile; :54 pinned (0,100) on a corpse | 100 | 100: confirmed | STALLED at 100 |

Counts: 12 skills. REACHES 200: 1 (Stealing). Conditional: 1 (Remove Trap, needs a Tinkering 190+ trapper; otherwise
180). STALLED: 10 (Hiding 100, Stealth 142, Detect Hidden 100, Snooping 100, Lockpicking 140, Poisoning 100,
Healing 120, Veterinary 120, Begging 100, Forensics 100).

**Stealing note (the surprise).** Take a thief at Stealing 199 and a pile of iron ingots (0.1 stone each, Ingots.cs:17).
maxAmount = (int)(199/10/0.1) = 199. A roll of 171-199 ingots gives pile 180-200 and max 207.5-227.5. That is above
199, so the gain roll happens: 29 of 199 rolls (about 15 percent), with success chance about 0.83. Gold under ML weighs
0.02/3 (Gold.cs:22): a roll of 2551 or more gold out of a 2985 max gives the same result. The victim's pile must be at
least that large. Neither branch has a stealing-specific gate: at :285 (whole pile) and :300 (part of a pile) the only
limit is that the unit weight fits under 10 stones (:263). The target may also be an item in an unlocked container on
the ground. Then root is the container and mobRoot is null, so being caught has no effect: only the root == null and
corpse branches set criminal (:390-392). Young players are blocked only from mobiles (:107). Whether a container
locked down or secured in a house blocks this was not checked in-game (unverified). The code path in Stealing.cs has
no house check. So Stealing already trains to 200 on a player's own gold or ingot pile.

## (ii) Proposals for the stalled skills

### One shared mechanism: a gain-only "shadow roll" in our skill-gain hook

Pattern (a) taken literally (pass Cap as maxSkill at the call site) breaks fidelity for every stalled skill except
Healing and Veterinary. Their CheckSkill result is the use's success: Hiding hides, Detect Hidden halves the radius
on a fail, Snooping opens the pack, Poisoning applies the poison, Begging gets gold, Forensics gets the info. Hiding
(0,200) would fail 50 percent of hides at 100. Healing and Veterinary are the exception: their result is discarded
(Bandage.cs:444-445).

The smallest change that keeps every success roll exactly pinned:

- Where: in C\ClusterFSkillGain.cs, in `ClusterFSkillCheckLocation` / `ClusterFSkillCheckTarget` (:63-88). One file,
  ours, no pinned patch.
- When: the player's Value is >= maxSkill (pinned "no challenge"), the skill is in an allowlist, and both Value and
  maxSkill pass that skill's floors (table below).
- What: call the public `SkillCheck.CheckSkill(from, skill, target-or-loc, chance)` (pinned SkillCheck.cs:108) with
  chance = (Value - minSkill) / (maxEff - minSkill), and return the original `true`.
- maxEff = skill.Cap + max(0, Value - Base). Without this, an item bonus stops the roll Base-bonus short of 200. The
  same flaw is in C\Meditation.cs:115.
- Call CheckSkill directly, not the base handler, so `SkillEvents.InvokeSkillUsed` does not fire twice.
- Gate the shadow roll with `from.Player`.
- Put it inside the `RunBoostedCheck` lambda so it gets the same 3 attempts and 5x amount as other gains. Decide
  whether it should still run when ClusterF gain is disabled (`_enabled`).

Floors, per skill:

| Skill | Value floor | maxSkill floor | Effect |
|---|---|---|---|
| Hiding | 100 | 100 | excludes the friend's-house call (max 0), so macroing hides at home still gains nothing, as pinned |
| Stealth | 142 | 60 | past 142, any stealth attempt rolls; 60-142 stays the pinned armor ladder |
| Detect Hidden | 100 | 100 | covers all three calls |
| Snooping | 100 | 100 | |
| Poisoning | 100 | 100 | only Greater, Deadly, Darkglow and Parasitic potions qualify, and the potion's min (60 or 95) still sets the chance, so the harder potions keep a different gain rate |
| Healing / Veterinary | 120 | 120 | excludes creature calls (90 and 100 maxes) |
| Begging | 100 | 100 | |
| Forensics | 100 | 100 | |
| Lockpicking | only if (b) below is rejected | | |

Against the brief's rule, "(a) only when difficulty still means something past 160": for Hiding, Snooping, Begging,
Forensics and Detect Hidden it does not. Their difficulty is fixed and is met at 100. So the shadow roll is formally a
practice gain, closer to (c), at the cost of (a). (b) has nothing to offer them: no harder hide, snoop, beg, corpse or
faction-trap target exists in pinned or C\. (c) as a new item (practice targets, training devices) costs a new class,
placement or sale, and tests per skill, for the same result. I recommend the shadow roll and flag it as a design
call: past 100 these skills climb by repetition alone. A middle ground for Detect Hidden: shadow-roll only when the
scan found at least one hidden mobile or trap. Then AFK self-target macros get nothing, and the hider's Hiding acts
as the difficulty.

### Hiding (stalled 100): shadow roll, floors 100/100

- Files: C\ClusterFSkillGain.cs (ours). Prerequisite in the same batch: pinned Skills/Hiding.cs:53 (patch).
- Fidelity: nothing changes below Value 100. At 100 to 120 an OSI player would see Hiding keep rising. That is
  intended. OSI has no Hiding power scroll ceiling the shard copies (unverified).
- Exploit check (directly involved):
  - Hide in combat. `range = Math.Min((int)((100 - H)/2) + 8, 18)` (Hiding.cs:53) gives 8 at 100, 3 at 110, 1 at
    114, 0 at 116 and -1 at 118. With a negative range, `InRange` is always false (Server/IEntity.cs:100-104) and the
    combatant check (:55) never blocks. Today a player's Base stops at 100 and I found no Hiding bonus source. So this
    exploit is NOT reachable by players today, and the proposal makes it reachable by plain training.
    Must ship with (or after) a clamp: `Math.Clamp(..., 8, 18)` keeps the pinned 100-skill range forever.
  - Guards cannot reveal hiders from 121. Guards have DetectHidden.Base 100 (Guards/ArcherGuard.cs:64,
    WarriorGuard.cs:81). The contest is +/-10 (DetectHidden.cs:197-198), so Hiding 121+ is immune. Also unreachable
    today, opened by this proposal.
  - Player Detect Hidden is also stuck at 100. If Hiding opens and Detect Hidden does not, no player can reveal a
    Hiding 121+ hider with the skill. Only BaseAI's DH/10 floor (BaseAI.cs:1151 area), Reveal and Tracking ratios
    remain.
  - So: open Hiding and Detect Hidden in the same batch, and either raise guard DH to the cap or add a floor chance
    for guards as BaseAI has.
  - Shard NPC hiders top out at about 125 (C\Mobiles\Normal\KepetchAmbusher.cs:52; OrcScout 100-120). SlasherOfVeils
    has DH 127.1 (C\Mobiles\Bosses\SlasherOfVeils.cs:75), so it is blind to Hiding 148+.
- New break between 160 and 200: none beyond the range bug. Snoop-fail reveal (Snooping.cs:97, Hiding/2 < rand x 100)
  becomes 80-100 percent safe. Death Strike already clamps at H+S = 220.

### Stealth (stalled 142): shadow roll, floors 142/60

- Files: C\ClusterFSkillGain.cs.
- Why not (b): heavier armor is the existing difficulty, but AR >= 42 blocks the use outright (Stealth.cs:91). Making
  it reach 200 needs AR 70, which means changing the AOS block. That is a fidelity change at every skill.
- Fidelity: nothing changes below 142. The 60 to 142 armor ladder is pinned.
- Base ceiling with bonuses: our Assassin (+30 per piece) and Hunter (+40 per piece) sets, CloakOfSilence +10,
  RoyalGuardInvestigatorCloak +20, Animal Form +20, and the random-item pool all raise Value. Today they lower the
  Base ceiling below 142. The maxEff rule above fixes that for the shadow roll.
- Exploit check:
  - No listed exploit is Stealth's.
  - New effect 160-200: steps = Value/5 (Stealth.cs:102) gives 32 at 160 and 40 at 200. Running costs 2 steps
    (PlayerMobile.cs:3428), so 20 hidden running tiles at 200, against 14 at 142. Mild.
  - Set bonuses push Value well past 200, and steps grow with Value, not Base. A Hunter set worn at Base 200 is
    unverified for stacking.
  - Backstab, Surprise Attack and Ki only need steps > 0. A step soft-cap (P20) is optional.

### Detect Hidden (stalled 100): shadow roll, floors 100/100 (optionally "only when something was found")

- Files: C\ClusterFSkillGain.cs. Prerequisite: pinned Skills/DetectHidden.cs:145 radius clamp (patch).
- Fidelity: nothing changes below 100.
- Exploit check (directly involved):
  - Opening Detect Hidden is the counter to opening Hiding. Do both together.
  - New break 160-200: radius = (int)(DH/10) (DetectHidden.cs:145) is 16 at 160, 19 at 190 and 20 at 200. From 190
    it reveals hiders and traps off screen (view 18). Clamp with `Math.Min((int)(DH/10), 18)`, or hold at 10.
  - The contest stays relative between players. DH 200 reveals every shard NPC hider (max about 125) with certainty.
  - The passive Felucca detect (:116-117) uses the same contest. No change in kind.

### Snooping (stalled 100): shadow roll, floors 100/100

- Files: C\ClusterFSkillGain.cs.
- Fidelity: nothing below 100. The "you notice X peeking" check only fires below 100 (Snooping.cs:62-63), so it is
  unchanged.
- Exploit check: nothing past 100 reads Snooping. No new break 160-200.

### Lockpicking (stalled 140): (b) tinker-made boxes scale above Tinkering 120

- Why not (a): the lock's own min/max is the success roll. Changing it changes how often every chest opens below
  140.
- (b), existing material: pinned LockableContainer.OnCraft (LockableContainer.cs:31-38) sets level = (int)(T x 0.8),
  Req = min(level-4, 95), Max = min(level+35, 95), Lock = min(level-14, 95). Keep that exactly for T <= 120 (at 120:
  Req 92, Lock 82, Max 95).
- Above 120, interpolate to T = 200: Req 160, Lock 150, Max 210. That is Max = 95 + 1.4375 x (T-120), and Req and
  Lock move linearly from 92/82 to 160/150.
- A thief-tinker or a guild tinker then makes boxes the thief locks with the key and picks. That gains to 200 once a
  Tinkering of about 193+ is available (Max >= 200 needs T >= 193.1).
- Files: pinned Items/Containers/LockableContainer.cs (new patch, one hunk). No serialization change, since the
  fields already exist.
- Dependency: Tinkering must reach about 193 by use. That belongs to another group's audit (unverified here).
- Cheaper alternative if that dependency fails: shadow roll at floors 140/140. Only Req-100 chests (TMap L5-6, Paragon
  L5, ToT) count, so content still gates it, but by the brief's rule difficulty means nothing past 160.
- (c) a practice lockbox (ours, auto-relocks, Lock 150 / Max 210, sold by the thieves' guild) needs no Tinkering, but
  it is a new class plus a vendor entry.
- Fidelity: unchanged for Tinkering <= 120, which covers OSI Tinkering power scrolls.
- Exploit check: none of the rank-4 list. Picking a trapped box still triggers the trap (TrapOnLockpick), whose damage
  scales with the box maker's Tinkering, the P20 "uncapped from 120" item. Practicing on your own trapped box would
  hurt, so the exploit does not get worse.

### Poisoning (stalled 100): shadow roll, floors 100/100

- Files: C\ClusterFSkillGain.cs.
- Fidelity: nothing below 100. Lesser and Regular potions never qualify.
- Exploit check: nothing reads Poisoning past 100.
  - Infectious Strike levels clamp at 80-100 (InfectiousStrike.cs:55-59). The level-up roll is P/100 (:68), already
    certain at 100.
  - Serpent Arrow and Poison Field use sum > 199.8. Poison spell (Spells/Third/Poison.cs:58-86) is level 0 at
    distance >= 3 under AOS, and sums above 200 only matter at distance <= 2, which OSI's 120/120 already meets.
  - So no new break 160-200.
- The pinned IncreaseLevel lookup (Server/Poison.cs:51-52, `GetPoisonByIndex(oldPoison.Index + 1)`) is unchanged at
  this commit. Whether Index is now a list position was not re-checked (out of scope).

### Healing and Veterinary (stalled 120): (a), Meditation pattern with a 120 floor

- Change Bandage.cs:444-445 to `CheckSkill(skill, 0.0, Value < 120 ? 120.0 : skill.Cap + bonus)`.
- This is true (a): the result is discarded, so the check is a pure gain roll. The shadow roll in the hook is the same
  thing and avoids a second patch on Bandage.cs. Use the hook unless the builder prefers it visible in Bandage.
- Fidelity: the plain Meditation pattern (max = Cap at every Value) would change gain rates below 120. For example,
  the expected success-term at Healing 60 drops from 0.125 to 0.105. The 120 floor avoids that. Nothing changes below
  120.
- Exploit check:
  - Not in the rank-4 list.
  - New growth 160-200: AOS heal = min A/8+H/5+4, max A/6+H/2.5+4 (Bandage.cs:387-388). Average 57.5 at 120/120,
    81.5 at H 200 / A 120, 93.2 at 200/200, plus HitsMax/100 on animals (:398-401).
  - The delay is the real multiplier and is Dex-driven, not Healing-driven: 0.7 s on others from Dex 204 (:506-512),
    and self delay 5 + 0.05 x (120-Dex) (:493) reaches 0 at Dex 220 and goes negative above. The shard's stat cap of
    500 makes both reachable. This is a live break today, independent of this proposal. Recommend a delay floor in
    the same batch.
  - Veterinary has a fixed 2.0 s (:502).
  - Stable slots +(int)((V-90)/10) per skill (Vendors/NPC/AnimalTrainer.cs:86-96) give +11 each at 200 (Taming,
    Lore, Vet), so +33, against +9 at 120. Flag for the save-size owner.

### Begging (stalled 100): shadow roll, floors 100/100

- Files: C\ClusterFSkillGain.cs.
- Fidelity: none below 100. The gold amount has no skill term (Begging.cs:113-118).
- Exploit check: none.

### Forensic Evaluation (stalled 100): shadow roll, floors 100/100

- Files: C\ClusterFSkillGain.cs.
- Fidelity: none below 100.
- Exploit check: none. Nothing reads Forensics past 100.

### Already reaching 200 (no gain proposal), exploit notes

- **Stealing** reaches 200 now via stacks. Rank-4 "never caught from 150": `caught = Value < Random(150)`
  (Stealing.cs:337).
  - This was reachable before only with +50 of bonuses. Since cc-P53's cap of 200 it is reachable by Base alone,
    training on your own pile.
  - It is live today and not caused by any proposal here. Fix it before or with this batch: cap it at the
    100-skill odds, or keep a floor.
  - New break 100-200: stack theft takes up to Value/10 stones, 20 stones and 3000 gold a try at 200. That bypasses
    `stealing.maxWeightToSteal` = 10, which only tests unit weight (:263). Clamp maxAmount to MaxWeightToSteal /
    unitWeight (:272-276).
  - Fidelity: both fixes are invisible below 100 (caught odds unchanged up to 100; the stack cap equals Value/10 at
    100).
- **Remove Trap**: conditional on a Tinkering 190+ trapper.
  - If Tinkering cannot reach 190, the world ceiling is 180 (TMap L6). The (b) fix would be to raise TrapPower on our
    top chests (C\Items\Containers\TreasureChestMod.cs:249), but they cap at 130 today, so it needs a new tier.
  - Exploit: "Tinkering trap damage uncapped from 120" is a Tinkering issue. Remove Trap is its counter, and parity
    holds: the disarm window is TrapPower to TrapPower+30.

## (iii) Line moves vs P20 (pinned 7c9215d97 -> d4531cd94)

Moved:
- DetectHidden.cs:
  - Gain calls 159, 183, 228 -> 151, 175, 220.
  - Range 153 -> 145.
  - Contest 205-208 -> 197-198.
  - Passive contest 124-127 -> 116-117.
  - HS gate 245 -> 237.
- Stealing.cs:
  - Single-item check 309 -> 316.
  - Caught 330 -> 337.
  - Sigil 182 -> 185.
  - Weight limit 254-256 -> 263.
  - Stack block 264-300 -> 272-307.
  - Artifact gate 228 -> 231.
  - PermaFlags 406-411 -> not line-checked.
- TreasureMapChest.cs: 176 / 178-190 -> 194 (TrapPower), 197-207 (lock).
- Engines/Craft/DefTinkering.cs: 663-666 -> 677-681.
- LockableContainer.cs: 31-38 -> 34-38 (same block).
- BaseCreature.cs: 2354 (pet poisoning) -> 2695; 5366-5408 (creature heal) -> 5773 / 5805; 2345 (Paragon
  HitPoison) -> 2687.
- PlayerMobile.cs: 3523-3536 (stealth steps) -> 3428-3433; 3552-3564 (passive detect) -> 3457-3462.
- BaseAI.cs: 942-955 -> about 1151 (trgHiding line).

Unchanged (verified): SkillCheck.cs:62, 67, 100, 189, 220, 248; Hiding.cs:53, 73; Stealth.cs:91, 96-100, 102;
Snooping.cs:62-63, 84, 97; PickpocketDips.cs:61, 85; LockPick.cs:121, 128; RemoveTrap.cs:17, 21, 61, 96-97;
Poisoning.cs:124, 133, 159; ParagonChest.cs:96, 100-111; LesserArtifacts.cs:465-471; BaseTreasureChest.cs:88-97;
Bandage.cs:239-240, 321, 377, 387-388, 400, 444-445, 493, 500-502, 506-512; Begging.cs:111; ForensicEval.cs:36, 54;
Server/IEntity.cs:100-104; Server/Poison.cs:51-52; Guards ArcherGuard.cs:64, WarriorGuard.cs:81.

Not re-checked: InfectiousStrike.cs line ranges beyond :55-68, Reveal.cs, Tracking.cs, AnimalForm.cs.

C\Meditation.cs: the brief's ":92" is :115 now.

## (iv) Batch sizing

**Batch A, exploit prerequisites. M. Pinned patches. Must land before or with B.**
- Hiding.cs:53 range clamp.
- DetectHidden.cs:145 radius clamp.
- Guard DH: ArcherGuard.cs:64 and WarriorGuard.cs:81 to the cap, or a guard floor.
- Stealing.cs:337 caught floor and :272-276 stack clamp.
- Optional: Bandage.cs:493 / :506-512 delay floors. Bandage.cs already carries P\Bandage-pet-mimic-targeting.patch,
  so add a second patch or extend that one.

Facts:
- Hiding 150 next to an attacking combatant fails, as at 100.
- DH 200 scan radius is 18.
- Guard reveals Hiding 200 with chance > 0.
- Stealing 200 is caught at the same rate as 100 (or the chosen floor).
- Stealing 200 cannot take a pile over 10 stones.
- Values below 100 behave exactly as pinned (regression).

**Batch B, shadow roll. S-M. One file, ours: C\ClusterFSkillGain.cs.**
- Contents: an allowlist of the 9 skills with Value and maxSkill floors, a gain-only roll via
  SkillCheck.CheckSkill, and maxEff = Cap + bonus.

Facts, per skill:
- (1) Value 150, a no-challenge use: gain fires (seed RNG or loop N tries); return value still true.
- (2) Value 99, same use: identical pinned result and no extra roll.
- (3) Hiding in a friend's house at 150: no gain.
- (4) Stealth at 120 with AR 0: no gain (the pinned ladder holds).
- (5) Poisoning at 150 with a Lesser potion: no gain; with a Deadly potion: gain.
- (6) A bonus item (+15) at Base 190: gain still possible.
- (7) A creature (non-player) healing: no shadow roll.
- (8) SkillEvents fires once per use.

**Batch C, Lockpicking (b). S. Pinned patch on Items/Containers/LockableContainer.cs.**

Facts:
- Box made at Tinkering 120 or less has pinned Req / Lock / Max.
- At 200: 160 / 150 / 210.
- A Lockpicking 199 player picking that box gets a gain roll.

**cc-P53 overlap.**
- No file proposed here is one cc-P53 changed: P53 changed C\ClusterFSkillCaps.cs, C\Meditation.cs, C\RegenRates.cs,
  P\PlayerMobile-skill-bonus-above-cap.patch and the smithing files.
- cc-P53 cites C\ClusterFSkillGain.cs:141-147 (ShouldBoost) in its Part C reasoning and has facts in
  T\Misc\SkillBonusAboveCapVerification.cs. Batch B edits ClusterFSkillGain.cs, so re-run P53's C facts.
- The maxEff = Cap + bonus rule should also be applied to C\Meditation.cs:115, a P53 file. That is a one-line
  follow-up; flag it rather than mix it in.
- The Remove Trap and Lockpicking reach both depend on Tinkering reaching about 190-193, which is the crafting
  group's question.
