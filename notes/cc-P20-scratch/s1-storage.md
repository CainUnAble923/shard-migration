# S1: Skill and stat storage, packets, client display (pinned ModernUO 7c9215d97 + shard overrides + TazUO)

Paths for pinned are relative to D:\UO\ModernUO-pinned\Projects unless stated. Shard paths are relative to
D:\ShatteredLegacy\server. Client paths are relative to the TazUO repo root (see section 3 for how it was read).

## Bottom line

- Storage: per-skill base and cap are `ushort` in tenths. The largest value is 65535, which is 6553.5. So 300.0 (3000) and 1000.0 (10000) both fit.
  Skills.Cap and Skills.Total are `int`. 58 x 300.0 = 174000 and 58 x 1000.0 = 580000 both fit easily.
- Wire: 0x3A sends value, base and cap as ushort tenths. Skills.Cap and Skills.Total are never sent to the client.
  There is no truncation below 6553.5.
- Client (TazUO): it reads ushort and divides by 10 for display. I found no hardcoded 100 or 120 in the skill gumps or the skill packet handler.
  The client never gets the server's total cap. The assistant tab shows "Total: sum(base) / sum(caps)", which is 17400 for us.
- Stats: raw stats are `int`, clamped 1..65000. The 0x11 status packet sends Str/Dex/Int, stam, mana, hits and StatCap as 16-bit fields.
  500, 1500 and the derived hits/mana/stam all fit. The client reads them as ushort; StatCap is cast to short.
- BLOCKER for natural stat gain: SkillCheck.CanRaise/IncreaseStat cap each raw stat at `stats.statMax`. The default is 125 when Core.LBR is true, otherwise 100.
  Nothing in customizations or patches overrides it. Unless the live modernuo.json sets `stats.statMax` to 500, stats cannot gain past 125 naturally,
  whatever the 500 getter clamp and 1500 StatCap say. The live config value is UNVERIFIED (see 4.4).
- Minor overflow found: the faction Election score (UOContent/Engines/Factions/Core/Election.cs:450-456) can overflow int with large Skills.Total. Details in section 5.

## 1. How pinned stores skills

### 1.1 Skill (Server/Skills.cs)
- Fields: `private ushort m_Base; private ushort m_Cap;` (Server/Skills.cs:89-90). Units are tenths of a point.
- `BaseFixedPoint` (int property). The setter clamps to 0..0xFFFF and casts to ushort (Server/Skills.cs:179).
  It updates `Owner.Total = Owner.Total - m_Base + sv` (Server/Skills.cs:185), then calls Owner.OnSkillChange (Server/Skills.cs:189).
- `Base` (double) is `m_Base / 10.0`. The setter is `BaseFixedPoint = (int)(value * 10.0)` (Server/Skills.cs:199-203), so it truncates.
- `CapFixedPoint` setter clamps to 0..0xFFFF (Server/Skills.cs:210). `Cap` = `m_Cap / 10.0` (Server/Skills.cs:222-226).
- Maximum per skill: 65535 fixed = 6553.5. 1000.0 (10000) fits with no overflow.
- The ctor `Skill(Skills, SkillInfo, int baseValue, int cap, SkillLock)` casts `(ushort)` with no clamp (Server/Skills.cs:155-156).
  Callers pass 0/1000 (Server/Skills.cs:561), so this is harmless.
- `Fixed => (int)(Value * 10)` (Server/Skills.cs:228).
- `Value` (double) = max(NonRacialValue, Owner.RacialSkillBonus) (Server/Skills.cs:231-247). It has no upper clamp.
- `NonRacialValue` (Server/Skills.cs:250-331):
  - The stat offset applies only while base < 100: `inv = 100.0 - baseValue; if (inv <= 0.0) statsOffset = 0.0` (Server/Skills.cs:259-263).
    This is a hardcoded 100 but it is harmless: above 100 the offset is simply 0.
  - SkillMods: an absolute mod replaces the value (Server/Skills.cs:308-313). Relative mods with ObeyCap are added only while value < Cap, then clamped to Cap (Server/Skills.cs:319-327).
    Relative mods with !ObeyCap are added unclamped (Server/Skills.cs:317).
  - Bonuses are therefore limited by the per-skill Cap (300.0 on the shard), not by 100 or 120.
- Serialization (Server/Skills.cs:345-387): it writes 0xFF if default (base 0, cap 1000, lock Up). Otherwise it writes a flag byte, then `(short)m_Base`, `(short)m_Cap` and the lock byte.
  Deserialize reads `ReadUShort()` (Server/Skills.cs:103-104, 123, 128). The short/ushort pair round-trips all 16 bits, so values above 32767 (3276.7) also survive. Default cap on load is 1000 (Server/Skills.cs:112, 132).

### 1.2 Skills (Server/Skills.cs:455-)
- `public int Cap { get; set; }` (Server/Skills.cs:538). The default is 7000 in the ctor (Server/Skills.cs:463) and in old saves (Server/Skills.cs:489).
- `public int Total { get; set; }` (Server/Skills.cs:540). It is the sum of BaseFixedPoint only (not Value, not mods).
  It is maintained incrementally (Server/Skills.cs:185), recomputed on deserialize (Server/Skills.cs:513) and recomputed on Serialize (Server/Skills.cs:818, 836).
- Serialization writes `Cap` as int (Server/Skills.cs:822). Total is not saved (version 3; Server/Skills.cs:492-496).
- Int range: 174000 (shard) and 580000 (58 x 1000.0) are far below int.MaxValue.
- Skill count is 58: SkillName enum 0..57 (Server/Skills.cs:17-77). The table is loaded from Data/skills.json (UOContent/Skills/SkillsInfo.cs:135).
  D:\UO\ModernUO-pinned\Distribution\Data\skills.json has 58 entries.
- Mobile wrappers: `SkillsTotal => Skills?.Total` and `SkillsCap` get/set map to Skills.Cap (Server/Mobiles/Mobile.cs:477-490).
- Shard override: customizations\ClusterFSkillCaps.cs:107-124 sets every skill's CapFixedPoint to round(300.0*10), clamped to ushort.MaxValue (ClusterFSkillCaps.cs:85-86).
  It sets Skills.Cap = 58*300*10 = 174000 (ClusterFSkillCaps.cs:82-89). It runs on login (ClusterFSkillCaps.cs:30-38) and WorldLoad (ClusterFSkillCaps.cs:26, 91-105).
  `skills[i]` materializes every Skill object via the indexer (Server/Skills.cs:557-562). A cap change fires Owner.OnSkillChange, which sends a 0xDF skill update (Server/Skills.cs:216, 853).

### 1.3 Every arithmetic use of Total/Cap found in pinned (grep `Skills.Total|Skills.Cap|SkillsTotal|SkillsCap|.Total`)
All are int or double arithmetic. None casts to short or ushort.
- UOContent/Skills/SkillCheck.cs:96 (`Cap == 0` means no gain at all), :112 `(double)(Cap - Total) / Cap`, :231 `Total / (double)Cap`, :250 `Total < Cap`. All safe.
- UOContent/Mobiles/BaseCreature.cs:4436, 4489 (teaching free points), 4766, 4784 (SetSkill raises SkillsCap). Int, safe.
- UOContent/Items/Special/SoulStone.cs:636 and UOContent/Items/Special/Special Scrolls/ScrollofTranscendence.cs:94. Int, safe.
- UOContent/Engines/Veteran Rewards/RewardSystem.cs:576-586: `if (pm.SkillsCap is 7000 or 7050 ... 7200) pm.SkillsCap = 7000 + level*50`.
  With 174000 the pattern does not match, so it leaves the shard cap alone (good). ClusterFSkillCaps also reapplies at login.
- UOContent/Mobiles/PlayerMobile.cs:2626 `(int)Math.Pow(Skills.Total / 250.0, 2)`: 174000 gives 484416 and 580000 gives 5.38M. Safe.
- UOContent/Items/Skill Items/Musical Instruments/BaseInstrument.cs:262 `val += targ.SkillsTotal / 10.0`. This is provoke/peace difficulty.
  It is double, so no overflow, but a target with a huge skill total gets a large difficulty (compressed above 700 at :264). Gameplay note only.
- UOContent/Special Systems/Engines/TestCenter.cs:176. Int, safe.
- UOContent/Engines/Factions/Core/Election.cs:450-456. OVERFLOW RISK, see section 5.
- Skills.Cap and Skills.Total are NOT sent in any packet. No reference appears in Server/Network/Packets (grep).

## 2. Packets

### 2.1 Skills 0x3A (Server/Network/Packets/OutgoingPlayerPackets.cs)
- Full list `SendSkillsUpdate` (OutgoingPlayerPackets.cs:119-149):
  - Type byte 0x02, "absolute, capped" (:130).
  - Per skill: ushort (SkillID+1) (:139), ushort value (:140), ushort BaseFixedPoint (:141), byte lock (:142), ushort CapFixedPoint (:143). Terminated by short 0 (:146).
  - Value = `Math.Clamp((int)(NonRacialValue * 10), 0, 0xFFFF)` (:136-137). Value therefore excludes the racial bonus and includes mods.
  - Length is 6 + 9*58 = 528 bytes, stackalloc (:126-127). Fine.
  - Sent from Mobile.OnSkillsQuery (Server/Mobiles/Mobile.cs:7868-7873), which is triggered by the 0x34 skills query (UOContent/Network/Packets/IncomingPlayerPackets.cs:402).
- Single update `SendSkillChange` (OutgoingPlayerPackets.cs:154-176):
  - Type 0xDF, "delta, capped" (:168). Fields: ushort SkillID with no +1 (:169), ushort value clamped 0..0xFFFF (:165-170), ushort base (:171), byte lock (:172), ushort cap (:173).
  - Called from Skills.OnSkillChange (Server/Skills.cs:853).
- Truncation threshold: only above 6553.5 (ushort). Nothing wraps or truncates at 100, 120, 300 or 1000.
- Incoming 0x3A is a lock change only: ReadInt16 id, ReadByte lock (UOContent/Network/Packets/IncomingPlayerPackets.cs:38, 331-335).

### 2.2 Status bar 0x11 (Server/Network/Packets/OutgoingMobilePackets.cs:450-576)
- Hits/HitsMax: `WriteAttribute(HitsMax, Hits, version == 0, true)` (:511). WriteAttribute writes two `(short)` values (:166-190).
  It is normalized to 25 only for the compact (other-mobile) version.
- Str, Dex, Int: `(short)` each (:523-525). Stam, StamMax, Mana, ManaMax: `(short)` each (:527-530). Gold is int (:532). AR/phys resist (short) (:533), weight (short) (:534).
- MaxWeight (short) and race byte at version >= 5 (:536-540).
- StatCap: `(short)beheld.StatCap` (:542). Followers and FollowersMax are bytes (:544-545).
- AOS fields (version >= 4) are all short except TithingPoints int (:547-563). The 15 extended statuses are short (version 6, :565-573).
- 0xA1/0xA2/0xA3 hits/mana/stam and 0x2D attributes use the same WriteAttribute (short) (OutgoingMobilePackets.cs:198-293).
- All are signed 16-bit on the server side, so the limit is 32767. Stat 500, StatCap 1500 and hits/mana/stam around 500 fit with large margin.
  Raw stats can be set up to 65000 (section 4), which WOULD wrap in these short casts, but that cannot happen at shard values.

## 3. TazUO / ClassicUO client

How I checked: no client source is on disk. D:\UO\ClassicUO, D:\UO\CUO-Admin and D:\UO\TazUO\client contain only binaries (TazUO.dll, TazUO.exe, TazUO.pdb).
`find` over D:\UO, excluding the ModernUO and ServUO trees, found no SkillGumpAdvanced.cs, StandardSkillsGump.cs, PacketHandlers.cs or ClassicUO csproj.
The installed version is D:\UO\TazUO\client\v.txt = "26.0909.63".

I read the source from GitHub using curl against raw.githubusercontent.com and api.github.com, not WebFetch.
The repo bittiez/TazUO now redirects to PlayTazUO/TazUO. I used main at commit 7deed693c3015c1e8b491006a6540f3a2b630471 (fetched 2026-09-30).
The GitHub commits API shows the last changes to the relevant files as follows:
- UpdateSkills.cs, SkillGumpAdvanced.cs, Skill.cs and CharacterStatus.cs: 2026-08-06.
- StandardSkillsGump.cs: 2026-03-24.
- UpdateMobileStatus.cs: 2026-08-27.
None changed since 2026-09-01. So these files are very likely identical in the installed 26.0909 build.
That mapping between installed build and source is an inference (UNVERIFIED by binary inspection).

### 3.1 0x3A parse: src/ClassicUO.Client/Network/PacketHandlers/UpdateSkills.cs
- `haveCap = (type != 0 && type <= 0x03) || type == 0xDF` (:20), `isSingleUpdate = type == 0xFF || type == 0xDF` (:21).
- Reads ushort id (:75), decrements it for types 0 and 0x02 (:83-84), matching the server's +1 for 0x02 and none for 0xDF.
- Reads `ushort realVal`, `ushort baseVal`, byte lock, then `ushort cap` (default 1000 if no cap) (:86-92).
- Stores them in Skill.ValueFixed, BaseFixed and CapFixed (:137-139), all `ushort` (src/ClassicUO.Client/Game/Data/Skill.cs:26-34).
- Display values are `float Value => ValueFixed / 10.0f`, `Base => BaseFixed / 10.0f` and `Cap => CapFixed / 10.0f` (Skill.cs:36-52).
- The "skill increased by" message computes `realVal / 10.0f - skill.Value` (UpdateSkills.cs:102). No clamping.
- Values up to 6553.5 round-trip exactly.

### 3.2 Skill gumps
- src/ClassicUO.Client/Game/UI/Gumps/SkillGumpAdvanced.cs:
  - Per-skill labels `skill.Base.ToString()`, `skill.Value.ToString()` and `skill.Cap.ToString()` (:638-640), at fixed X 205/255/305 (:662-669).
  - Totals are float sums of Base and Value, shown with "F1" (:477-478, 496-501). Group sums are shown at :390-391, 456-457.
  - There is no 100/120 constant and no colouring by cap.
  - Only cosmetic risk: columns are 50 px apart. "300" fits like "100". A 7-character total such as "17400.0" sits in the bottom row at the same X.
    Possible visual overlap is UNVERIFIED (not run).
- src/ClassicUO.Client/Game/UI/Gumps/StandardSkillsGump.cs:
  - Per-skill text `$"{val:F1}"`, right-aligned at S(250) (:943-955). It shows Value, Base or Cap depending on the checkboxes.
  - The total label is `Skills.Sum(s => real ? s.Base : s.Value).ToString("F1")` (:107, :411).
  - No 100/120 constants and no total-cap display or colouring.
- src/ClassicUO.Client/Game/UI/Gumps/SkillProgressBar.cs:70-73: bar width = `barBounds.Width * (s.Value / s.Cap)`, clamped to the width.
  It uses the server-sent cap, so it scales correctly at 300.
- src/ClassicUO.Client/Game/UI/MyraWindows/Widgets/Assistant/Skills/SkillsTabContent.cs:288-306: "Total: {sum Base:F1} / {sum Cap:F1}".
  This is the sum of per-skill caps (17400.0 on the shard), not the server's Skills.Cap, which the client never receives.
  It happens to equal the shard's 174000/10 because the shard total cap = 58 x individual cap.
- No client-side clamp of skills to 100 or 120 was found in these files.
  I did not read every TazUO file (e.g. scripting APIs, title bar). Other references are UNVERIFIED.

### 3.3 0x11 parse: src/ClassicUO.Client/Network/PacketHandlers/CharacterStatus.cs
- Hits/HitsMax ushort (:26-27). Str/Dex/Int ushort (:57-59). Stam/StamMax/Mana/ManaMax ushort (:60-63). Weight ushort (:66). WeightMax ushort (:136).
- `StatsCap = (short)p.ReadUInt16BE()` (:156). Signed, so the limit is 32767; 1500 is fine.
- The status gumps print values with ToString() (src/ClassicUO.Client/Game/UI/Gumps/StatusGump.cs:332-386, 609-613, 1008, 1370, 1388, 1513-1541).
  No 100/125/150/225 constants were seen in that grep.

## 4. Stats

### 4.1 Storage and clamps (Server/Mobiles/Mobile.cs)
- `private int m_Str, m_Dex, m_Int` (:341). `private int m_StatCap` (:340).
- RawStr/RawDex/RawInt setters clamp 1..65000 (:1833, :1891, :1949).
- Str getter `Math.Clamp(m_Str + GetStatOffset, 1, 65000)` (:1868). Dex and Int clamp 0..65000 (:1926, :1984).
- RawStatTotal = RawStr + RawDex + RawInt (:1762).
- StatCap is an int property; it raises MobileDelta.StatCap, which resends status (:1731-1741).
  It is serialized as int (:2365, :6332). The default is 225 (:6357, :7720). Stats serialize as int (:2387-2389, :6382-6384).
- PlayerMobile getters: `if (Core.ML && AccessLevel == Player) return Math.Min(base.Str, 150)` (UOContent/Mobiles/PlayerMobile.cs:588-600). Int and Dex are the same (:603-630).
  Shard patch patches\PlayerMobile-individual-stat-cap.patch replaces 150 with `ClusterFStatCaps.IndividualStatCap`.
  That is 500 if enabled, else 150 (customizations\ClusterFStatCaps.cs:10, 103). The clamp applies to raw stat plus mods (base.Str includes GetStatOffset).
- Shard StatCap: customizations\ClusterFStatCaps.cs:105-108 sets `player.StatCap = 1500` (DefaultTotalStatCap :11). It applies on login (:30-38) and WorldLoad (:26, 80-101).

### 4.2 Natural gain: SkillCheck (UOContent/Skills/SkillCheck.cs)
- `_statMax = ServerConfiguration.GetOrUpdateSetting("stats.statMax", Core.LBR ? 125 : 100)` (:23).
- CanRaise: false if RawStatTotal >= StatCap (non-pet) (:327-333). Otherwise it requires `RawStr < _statMax` (and the same for Dex and Int) (:335-341).
- IncreaseStat: `from.RawStr = Math.Min(from.RawStr + 1, _statMax)` (:366, and :387 and :408 for Dex and Int).
  Atrophy is forced when RawStatTotal >= StatCap (:346).
- GainStat: atrophy chance is `RawStatTotal / (double)StatCap` (:473). With StatCap 1500, atrophy almost never triggers.
- So, YES: with the default config each raw stat stops gaining at 125. The maximum natural total is 375, far below the 1500 StatCap.
  The 500 getter clamp only matters for stats raised by other means (GM set, items or mods, stat balls, etc.).
- The shard does not override this. A grep for `statMax` in customizations and patches finds nothing.
  customizations\ClusterFSkillGain.cs wraps the SkillCheck handlers (ClusterFSkillGain.cs:38-46) and calls SkillCheck.Gain (:132), so pinned's stat path still applies.
- The skill-gain side is fine for the shard caps:
  - Gain requires `skill.Base < skill.Cap` (:220) and `Total < Cap` for players (:250).
  - It sets `Math.Min(BaseFixedPoint + toGain, CapFixedPoint)` (:252).
  - The gain chance uses `(Cap - Total)/Cap` and `(skill.Cap - skill.Base)/skill.Cap` (:112-113). No 100/120.

### 4.3 Hits/Stam/Mana max at 500
- Mobile base: HitsMax = 50 + Str/2 (Server/Mobiles/Mobile.cs:2051), StamMax = Dex (:2096), ManaMax = Int (:2151).
  Hits/Stam/Mana setters clamp to their max (:2011, :2067, :2112).
- PlayerMobile HitsMax (UOContent/Mobiles/PlayerMobile.cs:548-578):
  - AOS: Str (the clamped getter) / 2 + 50 + BonusHits. BonusHits is capped at 25 under ML for players (:560-563), plus 20 in BakeKitsune/GreyWolf form (:565-569).
  - Pre-AOS: RawStr/2 + 50 (:573), which is not clamped by the getter.
  - At Str 500 under AOS/ML: 300 + up to 25 (+20) = max 345.
- StamMax = Dex + BonusStam (:581). ManaMax = Int + BonusMana (+20 elf) (:584-585). About 500 plus item bonuses.
- All fit in the short packet fields (section 2.2). No size issue.

### 4.4 Live config (UNVERIFIED)
- I could not find the live modernuo.json. D:\ShatteredLegacy\backups\sl-modernuo-rootfs-20260927.tar lists `modernuo/Configuration/` but no json files under it.
  A byte grep of the tar for "stats.statMax" found nothing as a json key.
- The shard expansion (and therefore Core.LBR) was not checked here. If the expansion is LBR or later, the default is 125; otherwise it is 100.
- To let stats gain toward 500, set `stats.statMax` to 500 in the live Configuration/modernuo.json. GetOrUpdateSetting writes the default there on first run.

## 5. Other caps or assumptions found in pinned

- Faction election overflow: UOContent/Engines/Factions/Core/Election.cs:450-456.
  - The code is `factorSkills = 50 + Total*100/10000`, then `factorSkills * factorKillPts * Math.Max(factorGameTime, 100) / 10000`, all int, where `factorGameTime = 50 + gameTime.Ticks*100/TicksPerDay`.
  - With Total 174000, factorSkills is 1790. With kp = 0 the product exceeds int.MaxValue once gameTime is above roughly 120 days, and it wraps (possibly negative, then Math.Clamp to 0).
  - Stock 7000 gives factorSkills 120, which is safe for about 5 years.
  - This only matters if factions and elections are active.
- Titles: UOContent/Misc/Titles.cs:438 `Math.Min(skill.BaseFixedPoint, 1200)` for the title table index. Skills above 120 just get the top (Legendary) title. Safe, with no crash.
- Teaching (BaseCreature.cs:4397-4411): an NPC teaches at most 42.0 (420) and limits to the student's cap. Not a problem.
- BaseCreature.SetSkill (UOContent/Mobiles/BaseCreature.cs:4758-4789): if base > cap it raises the cap to base and, under SE, raises SkillsCap. Creatures only.
- AosSkillBonuses (UOContent/Misc/AOS.cs:1109-1123): item skill bonuses are DefaultSkillMod relative with ObeyCap = true. They are limited by the per-skill Cap (300 on the shard), not by 120.
- SkillMod (Server/Mobiles/Mods/SkillMod.cs): no value cap. Changes call Skill.Update (:29-51).
- PowerScroll (UOContent/Items/Special/Special Scrolls/PowerScroll.cs:252, 272): refuses if `skill.Cap >= Value`, else sets Cap = Value.
  With a cap of 300, every power scroll is "useless", and ClusterFSkillCaps would reset the cap at login anyway.
  StatCapScroll (StatCapScroll.cs:99, 119-123): refuses if StatCap >= value, so it is useless at 1500.
  customizations\TestCenter\TestCenterKit.cs:141-174 already guards TestCenter fills so they do not lower caps.
- ScrollofTranscendence (ScrollofTranscendence.cs:81-94): uses skill.Cap and SkillsCap. Generic, no 120.
- Content thresholds, not clamps: Bushido.Base >= 120 (UOContent/Mobiles/Animals/Mounts/LesserHiryu.cs:118), Chivalry.Value >= 120 (UOContent/Spells/Chivalry/DivineFury.cs:46),
  Polymorph duration `Math.Max(Magery.Value, 120)` (UOContent/Spells/Seventh/Polymorph.cs:177), and various >= 100 checks (CraftItem.cs:1393, Mining.cs:284, Evasion.cs:167).
  These are "at least" checks. Values above 120 simply pass, and formulas that scale with Value scale beyond the design range (balance, not storage).
- In-server SkillsGump (UOContent/Gumps/SkillsGump.cs:32, 54, 237): shows and sets Base via "F1" and Convert.ToDouble. No limit beyond the ushort clamp.
- RacialSkillBonus (UOContent/Mobiles/PlayerMobile.cs:266) is a floor (Value = max), not a cap.
