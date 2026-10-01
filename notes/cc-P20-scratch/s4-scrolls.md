# S4: Power scrolls, stat scrolls, cap writers, and the Legacy Scroll line

Read-only research, 2026-09-30. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects`.
Shard paths: `customizations\...` and `patches\...` are under `D:\ShatteredLegacy\server`.

## 1. How pinned defines the scrolls

### SpecialScroll (base)
`UOContent/Items/Special/Special Scrolls/SpecialScroll.cs`
- `:7-18` abstract, `[SerializationGenerator(0, false)]`, two serialized fields: `Skill` (SkillName) and
  `Value` (double). No version beyond 0.
- `:22` LootType.Cursed by default.
- `:49-63` `CanUse`: only checks Deleted and "in your backpack".
- `:69-77` double click -> `CanUse` -> confirmation gump; `:133-139` Yes button -> `Use(from)`.
- `Use` is virtual and empty (`:65-67`); subclasses do all the work.

### PowerScroll
`UOContent/Items/Special/Special Scrolls/PowerScroll.cs`
- Skills (`:9-54`, assembled by era in `:115-162`): 22 pre-AOS (Blacksmith, Tailoring, Swords, Fencing,
  Macing, Archery, Wrestling, Parry, Tactics, Anatomy, Healing, Magery, Meditation, EvalInt,
  MagicResist, AnimalTaming, AnimalLore, Veterinary, Musicianship, Provocation, Discordance,
  Peacemaking) + 6 AOS (Chivalry, Focus, Necromancy, Stealing, Stealth, SpiritSpeak) + 2 SE (Ninjitsu,
  Bushido) + 1 ML (Spellweaving) = 31. SA/HS skills commented out (`:56-68`).
- `:72-81` ctor: hue 0x481; LootType Regular (tradeable) for 105 scrolls and for any Blacksmith or
  Tailoring scroll, otherwise Cursed.
- Values: `CreateRandom(min,max)` / `CreateRandomNoCraft(min,max)` (`:164-185`) give
  `100 + 5*k`, so 105/110/115/120. Nothing stops other values (the constructor takes any double).
- Names/titles (`:90-111`, `:187-236`): localized "wondrous/exalted/mythical/legendary" only for exactly
  105/110/115/120; any other value shows "a power scroll of <skill> (N Skill)".
- `:238-260` **CanUse refuses if `skill.Cap >= Value`** (msg 1049511 "too high for this power scroll").
  There is no upper bound and no check that the new cap is a valid step.
- `:262-272` **Use sets `from.Skills[Skill].Cap = Value`** (absolute set, not additive), effects, `Delete()`.
- What "caps them at 120" is only the values the creators pick; the class itself has no 120 limit.

### StatCapScroll (TypeAlias "Server.Items.StatScroll")
`UOContent/Items/Special/Special Scrolls/StatCapScroll.cs`
- `:12` ctor, default 230; Skill field unused (Alchemy). Titles/names for 230/235/240/245/250
  (+5..+25 over 225) at `:23-83`.
- `:85-106` CanUse: `newValue = Value (+5 if PlayerMobile.HasStatReward)`; **refuses if
  `StatCap >= newValue`** (msg 1049510).
- `:108-124` Use: **`StatCap = Value + 5` if HasStatReward, else `StatCap = Value`** (absolute).
- So stat scrolls raise StatCap to 230..250 (255 with the veteran half-level reward).

### ScrollofTranscendence (SoT)
`UOContent/Items/Special/Special Scrolls/ScrollofTranscendence.cs`
- `:30-31` `CreateRandom(min,max)` -> random skill (`SkillsInfo.RandomSkill()`), value = `rand/10.0`
  (so 0.1..1.0 points; champion range 1-5 Fel, 6-10 elsewhere).
- `:39-71` CanUse: PlayerMobile only; refuses during an ML skill-gain quest objective or an active
  Alacrity.
- `:73-128` Use: adds Base (not cap). Clamps the add to `Cap - Base` (`:87-89`), needs `Base < Cap` and
  Lock Up (`:92`), and if total would pass SkillsCap it lowers a Down-locked skill (`:94-110`).
  `:128` `Skills[Skill].Base += newValue`. Never touches Cap.

### ScrollofAlacrity
`UOContent/Items/Special/Special Scrolls/ScrollofAlacrity.cs`
- `:37-69` CanUse: as SoT (quest/alacrity already active).
- `:71-98` Use: refuses if `Base >= Cap` or lock not Up (`:82`); sets `pm.AcceleratedSkill` and
  `AcceleratedStart = now + 15 min`; SkillCheck multiplies gains x2-5 (`UOContent/Skills/SkillCheck.cs`
  ~`:245-248`). No pinned code creates one (no drop site found).

### Every pinned source that creates scrolls
| Source | file:line | What |
|---|---|---|
| Champion boss death | `UOContent/Mobiles/Special/BaseChampion.cs:58-68` (CreateRandomPowerScroll), `:70-133` (GivePowerScrolls), `:205-207` (called on death unless NoKillAwards) | **Felucca only** (`:72`). 6 PowerScrolls, no craft skills: 110 (60%), 115 (35%), 120 (5%). Spread over looters. |
| Justice protector dupe | `BaseChampion.cs:136-197` (GivePowerScrollTo), dupe at `:184` | `new PowerScroll(ps.Skill, ps.Value)` for the protector, 60/80/100% by Justice level. |
| Champion spawn per-kill | `UOContent/Engines/CannedEvil/ChampionSpawn.cs:612-625` | ML only. Chance per kill 0.1% Felucca, 0.15% Ilshenar/Tokuno, none elsewhere. Fel: 50% PowerScroll 105 (`:421` CreateRandomPS = CreateRandomNoCraft(5,5)) / 50% SoT; Ilsh/Tok: SoT (`:414-419`). |
| Champion spawn justice dupe | `ChampionSpawn.cs:422-488` (GiveScrollTo), dupe `:474-481` | Reflection clone `scroll.GetType().CreateEntityInstance<SpecialScroll>()`, copies Skill/Value. Works for any SpecialScroll subclass. |
| Harrower death | `UOContent/Mobiles/Special/Harrower.cs:237-300`, called `:320-322` | 16 StatCapScrolls, `225 + level` with level 5 (30%), 10 (25%), 15 (20%), 20 (15%), 25 (10%); Justice dupe `:299`. |
| Smith BOD rewards | `UOContent/Engines/Bulk Orders/Rewards.cs:534-541` (CreatePowerScroll), table `:384-398` | Blacksmith PS 105/110/115/120. Reached on the shard through `patches\LargeSmithBOD.cs:120` (`SmithRewardCalculator.LookupRewards`) if that reward path is still offered. |
| Tailor BOD rewards | `Rewards.cs:849-856`, table `:700-706` | Tailoring PS 105-120. |
| Test Center bank | `UOContent/Special Systems/Engines/TestCenter.cs:657-668` (AddPowerScrolls) | One 120 PS per PS skill + StatCapScroll 250. |
| Test Center AOS fill | `TestCenter.cs:220-231` (FillBankAOS) | No items: writes caps directly (see writers). |
| WelcomeTimer | `UOContent/Misc/WelcomeTimer.cs:33` | Message text only. |

Not sources: **Paragon** (`UOContent/Mobiles/Special/Paragon.cs:19-32` artifact list has no scrolls;
`GiveArtifactTo` `:214`) and **ParagonChest** (`UOContent/Items/Containers/ParagonChest.cs:113-183`:
gold, spell scrolls via `Loot.RandomScroll` `:117`, gear, reagents, gems; no power scrolls). Doom /
Gauntlet: no scroll creation found. No pinned code creates ScrollofAlacrity.

Shard sources (customizations):
- `customizations\SmithSealCatalogGump.cs:99-108` sells **Blacksmith PowerScroll 305 / 310 / 315 / 320**
  for Smithing Seals (750 / 2,000 / 4,500 / 10,000). Phase 4F remnant. See the bug in section 2.
- `customizations\Mobiles\Bosses\Navery\NavreyNightEyes.cs:163` drops `ScrollofTranscendence.CreateRandom(30,30)`
  (3.0 points).
- No shard override of BaseChampion, ChampionSpawn, Harrower or Paragon scroll code.

### Every writer of Skill.Cap / Skills.Cap / StatCap
Engine:
- `Server/Skills.cs:205-219` `Skill.CapFixedPoint` setter (ushort clamp 0..65535, then
  `Owner.OnSkillChange` which only updates the Highest tracker and the client, `:841-851`);
  `:222-226` `Skill.Cap` (double) wraps it. Serialized as ushort tenths (`:92-148`, `:345-385`).
- `Server/Skills.cs:538` `Skills.Cap` (int auto property, tenths; serialized `:822`, default 7000 `:463`).
  `Server/Mobiles/Mobile.cs:480-489` `Mobile.SkillsCap` wraps it.
- `Server/Mobiles/Mobile.cs:1731-1743` `StatCap` setter (no clamp of stats; just Delta);
  load `:6332`, legacy default 225 `:6357`, new mobile default 225 `:7720`.

Players (pinned):
- `UOContent/Items/Special/Special Scrolls/PowerScroll.cs:272` Skill.Cap = Value.
- `UOContent/Items/Special/Special Scrolls/StatCapScroll.cs:119,123` StatCap = Value (+5).
- `UOContent/Engines/Veteran Rewards/RewardSystem.cs:566-599` OnLogin (PlayerLoginEvent):
  `:576-588` only if `SkillsCap is 7000/7050/7100/7150/7200`, sets `7000 + level*50` (or 7000);
  `:590-594` once per character: if ML and not HasStatReward and HasHalfLevel -> `HasStatReward = true;
  StatCap += 5`.
- `UOContent/Special Systems/Engines/TestCenter.cs:226-231` FillBankAOS: every PS skill Cap = 120,
  StatCap = 250.

Creatures / clones (not players, listed for completeness):
- `UOContent/Mobiles/BaseCreature.cs:4762-4787` (raises Cap to Base and adjusts SkillsCap).
- `UOContent/Skills/AnimalTaming.cs:88-92` (tamed creature cap scaling).
- `UOContent/Spells/Ninjitsu/MirrorImage.cs:150` (clone copies caster cap).
- Test only: `UOContent.Tests/Tests/Skills/SkillPacketsTests.cs:23`.

Shard:
- `customizations\ClusterFSkillCaps.cs:107-124` Apply: every skill CapFixedPoint = flat config
  (`clusterf.skillCaps.individualCap`, default 300.0 `:10`), Skills.Cap = totalCap or
  `SkillInfo.Table.Length * individual` (`:82-89`). Runs at PlayerLoginEvent (`:30-38`), WorldLoad for all
  players (`:26`, `:91-105`), and `[ClusterFSkillCaps [all]` (`:40-80`).
- `customizations\ClusterFStatCaps.cs:105-108` Apply: `StatCap = totalCap` (1500); same triggers
  (`:26`, `:30-38`, `:80-101`). Individual stat cap (500) is enforced by
  `patches\PlayerMobile-individual-stat-cap.patch` (Str/Dex/Int getters `Math.Min(base.X, IndividualStatCap)`).
- `customizations\TestCenter\TestCenterKit.cs:141-176` RefillBank: snapshots caps, runs pinned fill,
  restores any cap the fill lowered (keeps the higher).
- `customizations\Mobiles\Bosses\Medusa.cs:677` clone copies a player's caps onto a creature.

## 2. Interaction with ClusterFSkillCaps / ClusterFStatCaps today

- **OSI power scrolls (105-120) are dead items today.** Every player skill cap is 300 after login, so
  `PowerScroll.CanUse` (`PowerScroll.cs:252`) refuses: 300 >= 120. Champion drops, BOD rewards and Test
  Center bags all produce unusable scrolls.
- **Stat scrolls are dead too.** StatCap is 1500 after login, `StatCapScroll.CanUse` (`:99`) refuses
  1500 >= 230..255. Harrower's 16 scrolls are useless.
- **Any per-player cap raise is wiped at the next login and at every world load.** Apply writes the flat
  value unconditionally (`ClusterFSkillCaps.cs:118-121`), including lowering a cap that a scroll raised.
- **Live bug: the Smith Seal power scrolls are lost.** `SmithSealCatalogGump.cs:104-107` sells PS 305-320.
  They pass CanUse (300 < 305), set Blacksmith cap to e.g. 310 and are deleted, then the next login or
  restart resets the cap to 300. The player paid up to 10,000 seals for a raise that lasts one session.
  (The catalog comment at `:100-101` describes the Phase 4F additive model, but pinned Use is an absolute
  set, so buying +10 after +5 is "310", not 315.) Recommend hiding that category until the new line exists.
- **Veteran +5 stat reward is lost.** RewardSystem.OnLogin (`RewardSystem.cs:590-594`) adds 5 once and
  sets HasStatReward; ClusterFStatCaps.Apply sets StatCap = 1500 flat. Whichever login handler runs
  first, by the next login (or world load) the cap is 1500 again and HasStatReward is already true, so
  the +5 never comes back. (Order between the two OnEvent handlers is generator-defined; ClusterF uses
  `[CallPriority(100)]` but I could not verify the CodeGeneratedEvents generator honors it. The outcome is
  the same either way.) The veteran skill-cap branch (`:576-588`) never fires on a ClusterF-touched
  character because SkillsCap is no longer 7000-7200; if it fired first on a brand-new character it would
  be overwritten by Apply anyway.
- Medusa clone, MirrorImage and TestCenterKit are compatible (they copy or keep the higher value).

## 3. What the new scroll line ("Legacy Scroll", key to the next loop) must touch

### Design target (decided 2026-09-30)
Per-skill cap = character's MaxLevel (50, 100, 150 ... up to 500-1000); loops raise MaxLevel; past cap 100
the next loop needs a scroll; lower scrolls merge into higher ones at a League NPC; OSI 105-120 PS fold
into the line. Sources: `roadmap.md` "Legacy Awakening" (`:333`), "Champion Spawn and Mastery Rewrite"
(`:915-943`), "Extended Resources and Mining" (`:457-466`), `feature-queue.md` F-12 (`:763` onward).
Phase 4F (`phase_4_smiths_guild_extended_crafting.md:746-797`, additive +5..+20, cap 500) is superseded.

### Classes
- **New `LegacyScroll : SpecialScroll`** in customizations (SerializationGenerator, its own version). Reuse
  `SpecialScroll.Value` as the **MaxLevel it unlocks** (e.g. 150, 200, ...); `Skill` unused (or used only
  if a future design wants skill-themed scrolls). Override Title/DefaultTitle/AddNameProperty (the base
  gump shows `DefaultTitle` when `Title == 0`, `SpecialScroll.cs:116-123`) and `SkillLabel => 0` like
  StatCapScroll does (`StatCapScroll.cs:14`).
- Its `Use` should **not** write Skill.Cap. Either (a) it is consumed by the loop-reset flow (reset gump
  looks for a LegacyScroll with `Value >= nextMaxLevel` in the pack), or (b) Use records
  "unlocked next loop" in the per-character record. (a) is simpler and keeps one writer of caps.
- Do not subclass PowerScroll: existing PowerScroll instances stay PowerScroll, and PowerScroll.Use is
  the thing that must stop writing caps.
- **PowerScroll and StatCapScroll themselves** (pinned) need one small patch, because under the loop
  rule they become usable again: a MaxLevel-100 character passes `Cap(100) >= 120` false and the scroll
  sets that skill to 120 until the next login (a session-long bypass of the loop gate, plus the scroll
  is consumed and the gain is lost). Patch `PowerScroll.CanUse` (`:238-260`) to refuse with "Bring this
  to the League to fold it into a Legacy Scroll", and the same for `StatCapScroll.CanUse` (`:85-106`) if
  stat caps also become per-loop. This one patch neutralises every drop site at once without patching
  BaseChampion / ChampionSpawn / Harrower / Rewards.

### Drop sites that create PowerScrolls / stat scrolls today
If the line should drop LegacyScrolls directly (instead of PS that get folded at the League), these are
the sites to change (each is pinned code, so a patch per file, or a shard subclass where one exists):
- `UOContent/Mobiles/Special/BaseChampion.cs:58-68`, `:127-133`, `:184` (Fel champion boss, 6 scrolls +
  Justice dupe). `GivePowerScrollTo(Mobile, PowerScroll)` is typed to PowerScroll.
- `UOContent/Engines/CannedEvil/ChampionSpawn.cs:421`, `:618-625` (per-kill PS 105 / SoT). `GiveScrollTo`
  takes any SpecialScroll and its Justice dupe is reflection-based (`:474`), so a LegacyScroll works here
  unchanged.
- `UOContent/Mobiles/Special/Harrower.cs:273`, `:299` (StatCapScrolls).
- `UOContent/Engines/Bulk Orders/Rewards.cs:538`, `:853` (BOD PS); shard path via `patches\LargeSmithBOD.cs:120`.
- `UOContent/Special Systems/Engines/TestCenter.cs:228-231`, `:663-666` (test only; TestCenterKit already
  protects caps).
- `customizations\SmithSealCatalogGump.cs:104-107` (shard; replace entries with LegacyScroll or fold
  tokens, or remove).
- Paragon (`Paragon.cs`, `ParagonChest.cs`): no scroll today. If Paragons should feed the line, add it in
  the shard's own loot hook (e.g. where `customizations\Mobiles\Bosses\StygianDragon.cs:145-147` drops a
  ParagonChest) or in `BaseCreature.cs:3209-3211` (Paragon artifact roll), not by changing pinned Paragon.
- Recommended minimal path: **leave pinned drop sites alone**, patch PS/StatCap `CanUse`, and treat PS
  105/110/115/120 (and stat scrolls) as **tier-0 inputs** the League NPC folds into LegacyScrolls (e.g.
  N x 120 PS -> one Legacy Scroll of the first scroll-gated loop). Replace drop sites later with the
  Champion Spawn rewrite.

### League NPC merging
- Shard NPC: `customizations\LeagueRegistrar.cs` / `LeagueRegistrarGump.cs` / `ClusterFLeagueSystem.cs`.
  Add "Fold scrolls": consume K scrolls of tier T (LegacyScroll Value T, or PowerScroll Value 105-120
  mapped to tier 0) from the backpack, give one of tier T+1. Use `Item.Delete()` on consumed scrolls
  and `AddToBackpack` for the result.

### Existing PowerScroll items in the world
- They are unusable today, so nothing has been lost by holders except the Smith Seal ones (section 2).
- Options: (1) keep them as fold inputs (recommended; no world edit, works with the CanUse patch); or
  (2) a one-time WorldLoad converter that iterates `World.Items.Values`, replaces each PowerScroll /
  StatCapScroll with an equivalent LegacyScroll fragment in the same parent/location, and logs a count
  (pattern: `ClusterFSkillCaps.ApplyToLoadedPlayers` uses `EventSink.WorldLoad`, `:26`, `:91-105`).
- Refund the Smith Seal PS buyers (the 305-320 scrolls were consumed) if any exist in live saves.

### Where per-player MaxLevel must live
- Today per-character shard data lives **inside the account record, keyed by character serial**:
  `customizations\ClusterFAccountData.cs:121-137` (`Dictionary<uint, CharacterGuildData>`,
  `GetOrCreateGuildData(Serial)`), serialized from version 15 at `:305-311`, accessed via
  `ClusterFAccountPersistence.GetOrCreateGuild(m)` / `GetGuild(m)` (`:687-704`). The persistence item
  (`:677-770`) writes all accounts into the world save. Versioning is strict (`:152-158` refuses newer
  saves), so a new field means `CurrentVersion` 16 plus a guarded read.
- ClusterFAchievements stores per-account (username key) dictionaries (`ClusterFAchievements.cs:122-133`,
  save `:1261-1271`, load `:1419-1437`), not per character.
- PlayerMobile partials in customizations exist (`customizations\Mobiles\PlayerMobileSetResistances.cs`)
  but only add methods; PlayerMobile has hand-written Serialize/Deserialize (pinned
  `UOContent/Mobiles/PlayerMobile.cs:2869`, `:3218`), so a serialized field there needs a core patch.
  Avoid.
- **Recommendation:** add `CharacterLegacyData { int MaxLevel; int Loop; int Level; long Xp; ... }` keyed
  by serial in ClusterFAccountData (v16), mirroring CharacterGuildData, with
  `ClusterFAccountPersistence.GetOrCreateLegacy(m)`. F-12 levels/XP need the same record anyway.

### Minimal ClusterFSkillCaps change
- In `Apply` (`ClusterFSkillCaps.cs:107-124`) replace `IndividualSkillCapFixedPoint` with
  `Math.Clamp(GetMaxLevel(player) * 10, 0, ushort.MaxValue)`, where `GetMaxLevel` reads
  `CharacterLegacyData.MaxLevel` (default: first cap 50 for new characters; migration default for
  existing characters, see section 4). Keep `Skills.Cap` = unlimited (total cap decided unlimited).
- Keep Apply authoritative: it runs at login and world load, so it is also the enforcement that undoes
  any stray cap write. Call it immediately after a loop reset changes MaxLevel.
- Note the world-load path runs before or after ClusterFAccountPersistence deserializes? Both are in the
  world load: persistence data is read during item deserialization, `EventSink.WorldLoad` fires after, so
  the record is available. (`ClusterFAccountData` is created on demand via `GetOrCreate`, which needs
  `m.Account` non-null; guard for account-less players.)
- Same shape for ClusterFStatCaps if the stat cap becomes per loop (`:105-108`), and add the veteran +5
  there (`HasStatReward ? +5 : 0`) so that reward stops being lost.

## 4. What happens when Skill.Cap is lowered below Base (migration of 300-skill characters)

Pinned **keeps Base**; nothing clamps or blocks:
- `Server/Skills.cs:205-219` CapFixedPoint setter only stores the value and calls `Owner.OnSkillChange`
  (`:841-851`, Highest-skill tracking). It never reads or writes `m_Base`.
- Load (`Skills.cs:92-148`) reads Base and Cap independently, no clamp. Packets send both as ushort
  (`Server/Network/Packets/OutgoingPlayerPackets.cs:141-143`, `:171-173`), so the client just shows
  Base 300.0 with cap 50.0.
- No pinned code lowers a player's Base to Cap (grep for `Base > ... Cap`: only creature code in
  `BaseCreature.cs:4762-4787` and `AnimalTaming.cs:90`, which **raise Cap to Base**).
- Effective value (`Skills.cs` NonRacialValue, `:255-330`): Value = Base (stat offset is 0 when Base >= 100,
  `:263-267`) plus non-ObeyCap mods. **ObeyCap mods are dropped** when value >= Cap (`:319-327`). AOS item
  skill bonuses are ObeyCap (`UOContent/Misc/AOS.cs:1123`), so a 300 character capped at 50 keeps 300
  effective skill but gets **no item skill bonus** on that skill.
- Gains: `SkillCheck.Gain` needs `Base < Cap` (`UOContent/Skills/SkillCheck.cs:220`), so the skill is
  frozen (no gain). Gain chance math `:112-113` goes negative ((Cap-Base)/Cap) but is floored at 0.01
  (`:120-123`) and gain is blocked anyway. Shard `customizations\ClusterFSkillGain.cs:145-147` also
  requires `Base < Cap`.
- Lowering still works: Lock Down atrophy in `SkillCheck.cs:231-243` does not look at cap, so the player
  can lower it by gaining other skills; once Base drops below Cap it can regain only up to Cap.
- SoT and Alacrity refuse (`ScrollofTranscendence.cs:92`, `ScrollofAlacrity.cs:82`).
- Numeric limits: Base and Cap are ushort tenths, so up to 6,553.5; 1000.0 = 10000 fits.

Implication for migration: setting cap 50 on a live 300 character silently **grandfathers** the 300
(frozen, still fully effective, minus item bonuses). Choose one explicitly:
1. **Grandfather by MaxLevel (recommended):** on first Apply, if no CharacterLegacyData exists, set
   MaxLevel to the smallest ladder step >= the character's highest Base (a 300 character gets 300, so
   nothing freezes and no item bonus is lost), and Loop accordingly.
2. **Clamp:** a one-time migration that sets Base = min(Base, Cap) per skill (and logs/refunds), which is
   what "cap = max level" literally implies. Must be an explicit migration, not part of Apply, because
   Apply runs every login.
3. **Freeze:** do nothing; accept frozen over-cap skills and lost ObeyCap bonuses (likely confusing).
Whatever is chosen, Apply must never lower Base itself.
