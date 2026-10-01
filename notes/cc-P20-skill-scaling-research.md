# cc-P20: skills past 120, research for the level and loop system

Written 2026-09-30 by Claude (cc-P20). Read-only: no code, config or world change, no commit. Scratch
scripts and the per-area working files are in `notes\cc-P20-scratch\`. Pinned ModernUO is
`D:\UO\ModernUO-pinned` at 7c9215d97; paths in citations are relative to its `Projects\` folder unless
they start with `customizations\` or `patches\` (`D:\ShatteredLegacy\server\...`).

How this was done: seven read-only sub-agents each covered one area (storage and client; combat,
magic, thief and healing, animal and bard and misc, crafting and gathering skills; scrolls;
creatures). Their sections are kept below with their citations. I re-read in pinned and our tree,
myself, the claims that drive a decision or a notification: Skill storage (`Server/Skills.cs:89-90,
:205-219`), the gain formula (`UOContent/Skills/SkillCheck.cs:53-145, :208-254`), `PowerScroll.cs:252,
:272`, the salvage bag ingot return (`customizations\SmithGuildSalvageBag.cs:139-148`), the Smith Seal
scroll catalog (`customizations\SmithSealCatalogGump.cs:104-107`), the Parry and Bushido block formula
(`Items/Weapons/BaseWeapon.cs:1515-1560`), the Discordance effect (`Skills/Discordance.cs:177-195,
:243`) and its use in swing speed (`BaseWeapon.cs:1404-1430`), and spell damage (`Spells/Base/Spell.cs:218-258`).
Everything else is the sub-agents' reading, cited, and not re-checked by me line by line.

**Nothing here was probed in a running server.** Every behaviour below is read from source. Per
AGENTS.md, a cause read from source is a hypothesis until a probe confirms it; the ones that would
change a decision are marked.

Live config (`modernuo.json`, `antimacro.json`) is inside the container and was not read: the
defaults in the code are assumed (individual cap 300, `stats.statMax` 125, anti-macro off). Unverified.

---

## 0. The one-page answer

**Can skills go to 1000 without engine changes?** Storage, packets and the client: **yes.** A skill's
base and cap are `ushort` tenths, so 6,553.5 is the ceiling (`Server/Skills.cs:89-90`, clamp `:179`,
`:210`); `Skills.Cap` and `Total` are `int` (`:538`, `:540`); packet 0x3A sends ushort tenths
(`Server/Network/Packets/OutgoingPlayerPackets.cs:119-176`); TazUO reads ushort / 10 with no 100 or 120
constants found (source read from GitHub, not from the installed binary; section 1). 58 skills at
1000 is a total of 580,000 tenths, which fits.

**Stats** fit too (status packet sends `short`, `OutgoingMobilePackets.cs:511-542`), but **no stat can
gain past 125 by use** unless the live config raises `stats.statMax` (default 125,
`UOContent/Skills/SkillCheck.cs:23`, enforced at `:337-341`); nothing of ours overrides it. Max hits
stay about 300-345 even at 500 Str under AOS (`Mobiles/PlayerMobile.cs:548-578`). Section 1.4.

**The game rules: no.** Read at 300 (live today), many formulas already break, and at 1000 most combat,
magic, bard and healing formulas run away. Counted from the section 2 tables: of the 58 skills,
**41 have at least one use that breaks by 1000, and 20 of those break already at 300 or below**
(two of the 20 through our own code, one through a pinned bug that skill only makes certain; counted
by hand in the section 2.0 table, one row per skill). The other 17 only clamp: they stop doing anything
between 100 and about 230, so points past that are wasted.

**What breaks already, live at the 300 cap** (these exist today, with no loop system):
- Parry plus Bushido with a one-handed weapon blocks 187 percent of hits at 300/300 (`BaseWeapon.cs:1552`).
- Feint at Bushido or Ninjitsu 237+ makes the target do no damage for 6 s (`Items/Weapons/Abilities/Feint.cs:41`).
- Hiding works in combat from Hiding 118 (`Skills/Hiding.cs:53-71`); Stealing is never caught from 150
  (`Skills/Stealing.cs:330`) and lifts 4,500 gold a try at 300 (`:264-300`).
- Every bard skill is a certain success from about 150-167 (Musicianship term has no cap), and
  Discordance at 300 gives a -100 effect: creature resists drop by 100, and in the ML swing formula
  `100 / (100 + bonus)` divides by zero (`Skills/Discordance.cs:183`, `BaseWeapon.cs:1430`). **Possible
  server exception, not probed** (section 2, animal and bard).
- Eval Int spell damage is x3.0 at 300 against x1.38 at 120 (`Spell.cs:251-254`), on top of an
  uncapped Int term (500 Int gives +50 percent).
- **Two live defects in our own code, found on the way, both sent to Chase:**
  1. `customizations\SmithGuildSalvageBag.cs:145-148` removes pinned's Mining cap of 100 in the
     ingot return. Above Mining about 143, salvage returns more ingots than the item cost: a 25-ingot
     item gives back 51 at 300. An ingot dupe.
  2. `customizations\SmithSealCatalogGump.cs:104-107` sells Blacksmithing power scrolls 305-320 for up
     to 10,000 seals. `PowerScroll.Use` sets the cap (`PowerScroll.cs:272`), and
     `ClusterFSkillCaps.Apply` puts it back to 300 at the next login or world load
     (`customizations\ClusterFSkillCaps.cs:107-124`). Buyers lose it.

**Gains** do not stall in the formula: it is relative to the cap (section 3). They stop because almost
every use has a fixed `maxSkill`, above which the check succeeds without a gain roll
(`SkillCheck.cs:58-61`). 39 of the 58 skills stop gaining at or below 160 today (counted from the section 2.0
gain-ceiling column; Taming's 181 with a creature that had 4 owners counted at its usual 157). **So by play, Base can pass about 160 only in Tactics, Anatomy, Eval Int, Spirit Speak, Meditation,
the six weapon skills (to about 220), Focus (200), Peacemaking, Provocation and Discordance (175-200 on
a target, falling as Musicianship rises), Parry (380, shield), Mining (sand, 400), Blacksmithy (BOD
and commission turn-ins, about 295) and Remove Trap (against tinker traps).** Any other live skill above
that came from a scroll, a gem, a Test Center tool or staff.

**The cheapest safe path:**
1. Store a per-character max level (keyed by serial in our account data, not a PlayerMobile core
   patch) and have `ClusterFSkillCaps.Apply` write `cap = maxLevel` per character instead of a flat 300.
   Small. Fixes the scroll reset at the same time. Grandfather live characters by setting their first
   max level from their highest skill: pinned never lowers Base when Cap drops (section 4.4).
2. Put **one shared soft-cap curve** on the effective skill inside the roughly 30 runaway formulas
   (an "effective skill" helper, e.g. `120 + k*ln(1 + (v-120)/k)`), and **hard caps on chances**
   (block, resist, bard success, steal-caught, hide-in-combat) at OSI-like ceilings. Most of these
   are pinned files, so they are patches; section 7 sizes them.
3. Give each skill a use whose `maxSkill` follows the cap (as our `Meditation.cs:92` already does), or
   the skill cannot climb past its ceiling at all.
4. Treat 500 to 1000 as **prestige, not content scaling** (section 5): the existing ~700 creatures
   cannot threaten a 300 character now, and rescaling them all is the most expensive option.

Until step 2 exists, **do not raise the cap above 300**, and consider whether the live 300 should be
lowered or the worst live breaks fixed first (section 7, items 1-4).

---

## 1. Storage, limits and the client (sub-agent report, cited)

Paths for pinned are relative to D:\UO\ModernUO-pinned\Projects unless stated. Shard paths are relative to
D:\ShatteredLegacy\server. Client paths are relative to the TazUO repo root (see section 3 for how it was read).

### Bottom line

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

### 1.1 How pinned stores skills

#### 1.1.1 Skill (Server/Skills.cs)
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

#### 1.1.2 Skills (Server/Skills.cs:455-)
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

#### 1.1.3 Every arithmetic use of Total/Cap found in pinned (grep `Skills.Total|Skills.Cap|SkillsTotal|SkillsCap|.Total`)
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

### 1.2 Packets

#### 1.2.1 Skills 0x3A (Server/Network/Packets/OutgoingPlayerPackets.cs)
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

#### 1.2.2 Status bar 0x11 (Server/Network/Packets/OutgoingMobilePackets.cs:450-576)
- Hits/HitsMax: `WriteAttribute(HitsMax, Hits, version == 0, true)` (:511). WriteAttribute writes two `(short)` values (:166-190).
  It is normalized to 25 only for the compact (other-mobile) version.
- Str, Dex, Int: `(short)` each (:523-525). Stam, StamMax, Mana, ManaMax: `(short)` each (:527-530). Gold is int (:532). AR/phys resist (short) (:533), weight (short) (:534).
- MaxWeight (short) and race byte at version >= 5 (:536-540).
- StatCap: `(short)beheld.StatCap` (:542). Followers and FollowersMax are bytes (:544-545).
- AOS fields (version >= 4) are all short except TithingPoints int (:547-563). The 15 extended statuses are short (version 6, :565-573).
- 0xA1/0xA2/0xA3 hits/mana/stam and 0x2D attributes use the same WriteAttribute (short) (OutgoingMobilePackets.cs:198-293).
- All are signed 16-bit on the server side, so the limit is 32767. Stat 500, StatCap 1500 and hits/mana/stam around 500 fit with large margin.
  Raw stats can be set up to 65000 (section 4), which WOULD wrap in these short casts, but that cannot happen at shard values.

### 1.3 TazUO / ClassicUO client

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

#### 1.3.1 0x3A parse: src/ClassicUO.Client/Network/PacketHandlers/UpdateSkills.cs
- `haveCap = (type != 0 && type <= 0x03) || type == 0xDF` (:20), `isSingleUpdate = type == 0xFF || type == 0xDF` (:21).
- Reads ushort id (:75), decrements it for types 0 and 0x02 (:83-84), matching the server's +1 for 0x02 and none for 0xDF.
- Reads `ushort realVal`, `ushort baseVal`, byte lock, then `ushort cap` (default 1000 if no cap) (:86-92).
- Stores them in Skill.ValueFixed, BaseFixed and CapFixed (:137-139), all `ushort` (src/ClassicUO.Client/Game/Data/Skill.cs:26-34).
- Display values are `float Value => ValueFixed / 10.0f`, `Base => BaseFixed / 10.0f` and `Cap => CapFixed / 10.0f` (Skill.cs:36-52).
- The "skill increased by" message computes `realVal / 10.0f - skill.Value` (UpdateSkills.cs:102). No clamping.
- Values up to 6553.5 round-trip exactly.

#### 1.3.2 Skill gumps
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

#### 1.3.3 0x11 parse: src/ClassicUO.Client/Network/PacketHandlers/CharacterStatus.cs
- Hits/HitsMax ushort (:26-27). Str/Dex/Int ushort (:57-59). Stam/StamMax/Mana/ManaMax ushort (:60-63). Weight ushort (:66). WeightMax ushort (:136).
- `StatsCap = (short)p.ReadUInt16BE()` (:156). Signed, so the limit is 32767; 1500 is fine.
- The status gumps print values with ToString() (src/ClassicUO.Client/Game/UI/Gumps/StatusGump.cs:332-386, 609-613, 1008, 1370, 1388, 1513-1541).
  No 100/125/150/225 constants were seen in that grep.

### 1.4 Stats

#### 1.4.1 Storage and clamps (Server/Mobiles/Mobile.cs)
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

#### 1.4.2 Natural gain: SkillCheck (UOContent/Skills/SkillCheck.cs)
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

#### 1.4.3 Hits/Stam/Mana max at 500
- Mobile base: HitsMax = 50 + Str/2 (Server/Mobiles/Mobile.cs:2051), StamMax = Dex (:2096), ManaMax = Int (:2151).
  Hits/Stam/Mana setters clamp to their max (:2011, :2067, :2112).
- PlayerMobile HitsMax (UOContent/Mobiles/PlayerMobile.cs:548-578):
  - AOS: Str (the clamped getter) / 2 + 50 + BonusHits. BonusHits is capped at 25 under ML for players (:560-563), plus 20 in BakeKitsune/GreyWolf form (:565-569).
  - Pre-AOS: RawStr/2 + 50 (:573), which is not clamped by the getter.
  - At Str 500 under AOS/ML: 300 + up to 25 (+20) = max 345.
- StamMax = Dex + BonusStam (:581). ManaMax = Int + BonusMana (+20 elf) (:584-585). About 500 plus item bonuses.
- All fit in the short packet fields (section 2.2). No size issue.

#### 1.4.4 Live config (UNVERIFIED)
- I could not find the live modernuo.json. D:\ShatteredLegacy\backups\sl-modernuo-rootfs-20260927.tar lists `modernuo/Configuration/` but no json files under it.
  A byte grep of the tar for "stats.statMax" found nothing as a json key.
- The shard expansion (and therefore Core.LBR) was not checked here. If the expansion is LBR or later, the default is 125; otherwise it is 100.
- To let stats gain toward 500, set `stats.statMax` to 500 in the live Configuration/modernuo.json. GetOrUpdateSetting writes the default there on first run.

### 1.5 Other caps or assumptions found in pinned

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

---

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

### 2.1 Combat skills (Swords, Macing, Fencing, Archery, Throwing, Wrestling, Tactics, Anatomy, Parry, Bushido, Focus, Arms Lore)

Skills: Swords, Macing, Fencing, Archery, Throwing, Wrestling, Tactics, Anatomy, Parry, Bushido, Focus, Arms Lore (+ Lumberjacking combat bonus, mentioned).
Paths: pinned = relative to D:\UO\ModernUO-pinned\Projects. Shard = D:\ShatteredLegacy\server\...
Expansion: AOS/SE/ML/SA/HS/TOL all on, so AOS/ML branches only. Pre-AOS branches (Fists stun/disarm, BaseAxe/BaseBashing/BaseSpear/BasePoleArm anatomy procs, BaseShield.OnHit pre-AOS, ScaleDamageOld, MageAI/ThiefAI wrestle moves) are dead code here and are ignored.

#### Shard overrides relevant to this group

- customizations\RegenRates.cs REPLACES UOContent/Misc/RegenRates.cs. Diff vs pinned: only the Meditation armor branch (customizations\RegenRates.cs:158-164). Focus code (stam :95-97, mana :152-154, CheckBonusSkill :28-41) is byte-identical to pinned UOContent/Misc/RegenRates.cs:95-97, :152-154.
- customizations\CraftItem.cs REPLACES pinned; it still calls craftable.OnCraft(..., from, ...) (customizations\CraftItem.cs:1194), so Arms Lore exceptional bonuses in BaseWeapon/BaseArmor.OnCraft still apply.
- customizations\ClusterFSkillGain.cs wraps the four SkillCheck handlers (:37-45) with extra attempts/multiplier but passes min/max/chance through unchanged, so every gain ceiling below still holds.
- customizations\ClusterFSkillCaps.cs sets per-skill cap (default 300, :10). Tactics/Anatomy combat gain uses Skills.X.Cap so they follow it.
- patches\BaseWeapon-talisman-durability.patch, patches\AOS-*.patch, patches\Mobile-set-item-resistance-hook.patch: no skill reads. Not relevant to scaling.
- Shard gargoyle weapons (customizations\Items\Equipment\Weapons\Gargish*.cs, Shortblade.cs) use DefSkill Swords/Fencing, not Throwing. GargishBattleAxe.cs:151-153 anatomy proc is the !Core.AOS copy (dead).
- customizations\PetMimicWeapon.cs:113-119 sets DefSkill by mimic category; it reads the wielder's skill only through the generic weapon path.
- No shard file reads Parry, Bushido, Focus, Tactics, Anatomy or Arms Lore values for gameplay other than CharacterCreation (start skills), ClusterFGuildSystem.cs:181/201/231/262 (guild join thresholds 30-50, clamps) and ClusterFGuildStarterPath.cs:46-56 (lists).

#### Shared formulas used below

Hit chance (AOS), pinned UOContent/Items/Weapons/BaseWeapon.cs:1233-1365:
  ourValue = (atk + 20) * (100 + HCI), HCI capped 45 (:1294)
  theirValue = (def + 20) * (100 + DCI), DCI capped 45 (:1343)
  chance = ourValue / (2 * theirValue), floor 0.02 (:1358-1362); CheckSkill(weapon skill, chance) (:1365)
  atk = Skills[GetUsedSkill].Value (:1178-1229); def = defender weapon skill (Fists: max(Wrestling, min((Anat+Eval+20)/2, 120)), Fists.cs:44-58).
  Gain ceiling: chance >= 1.0 at atk = 2*(def+20)*(100+DCI)/(100+HCI) - 20. Versus a 100-skill monster with no mods: 220. Versus 120: 260. With 45 HCI vs 100: 145.5.

Weapon damage (AOS), BaseWeapon.cs:2533-2603, GetBonus :2501-2511 (value*scalar, +offset at >=100):
  Str: 0.30*Str + 5 ; Anatomy: 0.50*v + 5 ; Tactics: 0.625*v + 6.25 ; Lumberjacking (axes only): 0.20*v + 10   (percent)
  "These are the bonuses given by the physical characteristics of the mobile. No caps apply." (comment :2552-2555)
  Only the item/spell part (WeaponDamage etc.) is capped at 100 (:2594-2597). The later percentageBonus cap of 300 (:1874) covers specials/moves/slayers, NOT tactics/anatomy.

Special-move mana, pinned UOContent/Items/Weapons/Abilities/WeaponAbility.cs:177-218:
  skillTotal = Swords+Macing+Fencing+Archery+Parry+Lumberjacking+Stealth+Poisoning+Bushido+Ninjitsu (:182-191). >=300 -> -10 mana, >=200 -> -5. Lowest BaseMana is 15 (InfusedStrike/MovingShot/WhirlwindAttack), so it never goes negative. Clamps at total 300 (one skill at 300 alone qualifies). Throwing is NOT in the list.
  Required weapon skill: Base >= 70 primary / 90 secondary (:122-138); Tactics Base >= 70/90 (:160-176, :235); secondary Bushido/Ninjitsu >= 50 (:145). All clamp.

Swing speed: no skill reads. SE/ML GetDelay (BaseWeapon.cs:1366-1460) reads Stam, SSI (capped 60 at :1419), HonorableExecution swing bonus (Bushido, folded into the 60 cap). Focus only matters indirectly via stamina.

---

#### Swords / Macing / Fencing / Archery / Throwing / Wrestling (weapon skills)

All six are read through the same generic path; only differences are noted.

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Attack hit chance vs 100-skill monster (no HCI/DCI) | BaseWeapon.cs:1299,1358 | (a+20)/(2*120) | scales: 58% | clamps: 133% -> always hits (100% reached at 220) | clamps (217%) | clamps (425%) | 220 vs 100-skill target, 260 vs 120, 145.5 with 45 HCI. To keep training at 300+ you need defenders with ~140+ skill; 1000 needs ~490-skill defenders |
| Defense: 100-skill monster hitting you (its chance) | BaseWeapon.cs:1348,1358 | 120/(2*(D+20)), /1.45 with 45 DCI, floor 2% | 43% (30% w/ DCI) | 19% (13%) | 11.5% (8.0%) | breaks: 5.9% (4.1%); near-immunity vs all normal monsters | (defense never gains) |
| PvP, equal skills | same | (a+20)/(2*(a+20)) | 50% | 50% | 50% | 50% | n/a - scales neutrally. Mismatch: 1000 vs 300 = 159% -> always hits; 300 vs 1000 = 15.7% |
| GetUsedSkill / UseBestSkill picks highest of Swords/Fencing/Macing | BaseWeapon.cs:1178-1229 | max | scales | scales | scales | scales | - |
| Weapon ability weapon-skill requirement | WeaponAbility.cs:122-138, 260-275 | Base >= 70/90 | clamps at 90 | clamps | clamps | clamps | - |
| Special-move mana discount (not Throwing, not Wrestling) | WeaponAbility.cs:182-200 | total>=300 -> -10 | -5 if total>=200 | clamps at 300 | clamps | clamps | - |
| Evasion cast / spell-evasion weapon gate | Spells/Bushido/Evasion.cs:56, :95 | Base >= 50 | clamps | clamps | clamps | clamps | - |
| Archery: Serpent Arrow poison level | Abilities/SerpentArrow.cs:25-31 | Archery+Poisoning > 199.8 -> Deadly (3) | scales | clamps at sum 199.8 | clamps | clamps | - |
| Throwing: DefSkill on BaseThrown (Boomerang, Cyclone, SoulGlaive) | Weapons/Throwing/BaseThrown.cs:38 | generic hit chance only | as above | as above | as above | as above | same as above |
| Wrestling: Fists defend value | Weapons/Fists.cs:44-58 | max(Wres, min((Anat+Eval+20)/2,120)) | scales | Anat/Eval part clamps at 120 | clamps (that part) | clamps | - |
| Wrestling: AOS Disarm / Paralyzing Blow on fists | Fists.cs:19-20; Abilities/Disarm.cs:18; ParalyzingBlow.cs:22 | Wrestling Base >= 70/90, no tactics needed | clamps | clamps | clamps | clamps | - |

Minor/cosmetic: tooltip "skill required" switch has no Throwing case (BaseWeapon.cs:3306-3328); BaseHire.cs:133-142 hireling pay (NPC only); AOS.cs:1095-1104 skill-name strings; BaseThrown inherits AccuracySkill => Archery from BaseRanged.cs:41, so old-style accuracy-level skill mods on a thrown weapon buff Archery not Throwing (minor bug, only legacy accuracy items).
Gaps (not breaks): Throwing is missing from the special-move mana skill total (WeaponAbility.cs:182-191) so a pure thrower never gets the -5/-10 mana discount that a pure archer gets. Wrestling is also missing.

Recommendation: soft-cap the hit-chance input past 120 (for example effective = 120 + 40*ln(1 + (v-120)/100)) or cap final hit chance at about 95% and floor defender-side at about 10% per attacker tier; otherwise defense past 500 makes normal monsters near-harmless. Re-think gain: weapon skills effectively stop gaining at 220-260 against normal content, so use a separate gain rule above 120 (e.g. gain on hit with a fixed small chance) or give gains vs high-tier creatures.

#### Tactics

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS damage bonus | BaseWeapon.cs:2558, total :2599-2602 | 0.625*v + 6.25 % (uncapped) | scales: +81.3% | scales: +193.8% | breaks: +318.8% | breaks: +631.3% | none: CheckSkill(Tactics, 0, Skills.Tactics.Cap) BaseWeapon.cs:2540 - follows the cap (300 now, 1000 later) |
| Weapon-ability tactics requirement | WeaponAbility.cs:235 | Base >= 70/90 | clamps | clamps | clamps | clamps | - |
| Evasion bonus gate (with Anatomy, Bushido>100) | Evasion.cs:167, :199 | >= 100 | clamps | clamps | clamps | clamps | - |

Combined example (Tactics = Anatomy = v, Str 125, 100% DI, non-axe): multiplier 3.89x at 120, 5.91x at 300, 8.16x at 500, 14.79x at 1000 (1.5x / 2.1x / 3.8x the 120 baseline). A weapon averaging 12 base damage: 47 / 71 / 98 / 178 per hit before resists; vs 70 physical resist: 14 / 21 / 29 / 53. Nothing caps this: the 100% DI cap and the 300% percentageBonus cap do not include it.
Recommendation: soft-cap with diminishing returns: keep 0.625*v up to 120, then add e.g. 25 * ln(1 + (v-120)/50) percent, or move tactics past 120 into a separate pool that counts toward the 100% DI cap.
Minor: BaseCreature.cs:2420 FightMode.Strongest target selection; AnimalLore gump display.

#### Anatomy

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS damage bonus | BaseWeapon.cs:2557 | 0.5*v + 5 % (uncapped) | scales: +65% | scales: +155% | breaks: +255% (see Tactics combined) | breaks: +505% | none: CheckSkill(Anatomy, 0, Cap) BaseWeapon.cs:2543 |
| Bandage heal (AOS, secondary skill) | Items/Skill Items/Misc/Bandage.cs:387-388 | min += v/8, max += v/6 | scales: 15-20 | scales: 37.5-50 | scales: 62.5-83 | scales: 125-167 (anatomy part only; Healing part covered by Healing audit) | Bandage.cs:444 CheckSkill(Anatomy, 0, 120) -> 120 |
| Bandage cure/res gates | Bandage.cs:240, :322 | >= 80 / >= 60 | clamps | clamps | clamps | clamps | - |
| Anatomy active use | Skills/Anatomy.cs:59, :97, :106 | margin = max(0, 25 - v/4); target check 0-100 | clamps at 100 | clamps | clamps | clamps | 100 |
| Fists defend value | Fists.cs:54-56 | min((Anat+Eval+20)/2,120) | clamps at Anat+Eval = 220 | clamps | clamps | clamps | - |
| Evasion bonus gate | Evasion.cs:167, :199 | >= 100 | clamps | clamps | clamps | clamps | - |
| BaseCreature self-heal (NPC only) | Mobiles/BaseCreature.cs:5367-5409 | v/10..v/8 | n/a players | | | | 100 |

Overall Anatomy gain ceiling: none (combat path uses Cap).
Recommendation: soft-cap the damage term like Tactics; let the bandage term scale (or give it a separate soft cap together with Healing).

#### Lumberjacking (combat part only, mentioned)

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Axe damage bonus | BaseWeapon.cs:2559-2561 | 0.2*v + 10 % | scales: +34% | scales: +70% | scales: +110% | breaks-ish: +210% on top of Tactics/Anatomy | combat gain CheckSkill(Lumberjacking, 0, 100) BaseWeapon.cs:2548 -> 100 (harvest gain is the gathering auditor's; shard ClusterFLumberjackingExtension reads Lumberjacking to 300) |
| Special-move mana total | WeaponAbility.cs:188 | counts | clamps at total 300 | | | | |

Recommendation: same soft-cap shape as Tactics.

#### Parry

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Block chance WITH shield (Bushido 0, Dex >= 80, no Evasion) | BaseWeapon.cs:1520-1540 | max((Parry - BushidoNonRacial)/400, 0) + 0.05 if Parry or Bushido >= 100 | scales: 35% | scales: 80% | breaks: 130% -> every weapon hit (melee AND ranged) blocked, damage set to 0 (:1599-1603) | breaks: 255% -> immune | direct chance: reaches 1.0 at Parry 380 (+BushidoNonRacial). Note Bushido SUBTRACTS here: Parry 300/Bushido 300 with shield = 5% |
| Block chance, 1H weapon no shield, Bushido = Parry | BaseWeapon.cs:1550-1585 | P*B/48000 (2H /41140) +0.05; Evasion scalar; Dex<80 penalty | scales: 35% (40% 2H) | breaks (live today): 1.875+0.05 -> 100% block | breaks | breaks | gain only if bushido-chance > aosChance; stops at P*B >= 45600 (1H) / 39083 (2H), e.g. 213.5/213.5 |
| Block chance, weapon, Parry only (Bushido 0) | BaseWeapon.cs:1554-1585 | Parry/800 + 0.05 | 20% | 42.5% | 67.5% | breaks: 130% -> immune (100% at Parry 760) | NO gain on this path (Utility roll, not CheckSkill :1585) |
| Evasion spell dodge (uses CheckParry) | Spells/Bushido/Evasion.cs:80-110; Spell.cs:320; FireBreath.cs:147 | while evading, CheckParry also blocks single-target spells and fire breath | scales | breaks when block chance >= 100%: immune to single-target spells while Evasion is up | breaks | breaks | - |
| Shield ArmorRating | Items/Shields/BaseShield.cs:24 | Parry*AR/200 + 1 | heater (23): 14.8 | 35.5 | 58.5 | 116 | - |
| Shield wear per block vs Bashing (AOS) | BaseShield.cs:30-45, 78-112 | rand(AR/2..AR)/2 durability | 3-7 | 8-17 | breaks (self-harm): 14-29 | breaks: 29-58 per block; heater has 50-65 HP so it hits 0 HP in about 2 mace blocks, then MaxHitPoints is eaten and the shield is deleted (:100-110) | - |
| Special-move mana total | WeaponAbility.cs:187 | counts | clamps at 300 | | | | |
| Counter Attack / Confidence triggers | BaseWeapon.cs:1593-1625 | fire on every successful block | see Bushido | | | | |

Recommendation: hard-cap final block chance (e.g. 50-60% shield, 40% weapon) and put a soft-capped curve on Parry past 120 (e.g. +0.05 per 100 points); decouple shield ArmorRating from Parry (use min(Parry,120)) so high Parry does not shred shields; fix the shield path subtracting Bushido.

#### Bushido

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| No-shield parry multiplier | BaseWeapon.cs:1552 | P*B/48000 | see Parry | breaks (with Parry 300) | breaks | breaks | - |
| Shield parry penalty | BaseWeapon.cs:1520 | (P - B_nonracial)/400 | reduces shield block | at B=P shield block = 5% | same | same | - (bad interaction, not abusable) |
| Evasion duration (s) | Evasion.cs:159-172 | (int)(3 + (B-60)/20) +1 w/ Anat&Tac>=100 | 6 (7) | 15 (16) | 25 (26) | 50 (51) | Evasion gain req+-: 47.5-97.5 |
| Evasion uptime vs 20 s cooldown | Evasion.cs:135-136 | duration >= 20 s at B >= 400 (380 with bonus) | scales | scales | breaks: permanent Evasion | breaks: permanent | - |
| Evasion parry scalar | Evasion.cs:175-204 | 1 + 0.16 + (B-60)*0.004 (+0.10) | 1.40 (1.50) | 2.12 (2.22) | 2.92 (3.02) | 4.92 (5.02) | - |
| Confidence regen (4 ticks, stops on damage) | Spells/Bushido/Confidence.cs:131-133, PlayerMobile.cs:2377 | per tick (15 + B^2/576)/4 | scales: 10/s, 40 total | scales: 42/s, 168 total | breaks: 112/s, 448 total, 10 mana | breaks: 437/s, 1748 total (full heal in 1 tick) | Confidence req 25 -> 62.5 |
| Confidence heal on block | BaseWeapon.cs:1615-1624 | Hits += 1..B/12, Stam += 1..B/5 | 1-10 hp, 1-24 stam | 1-25 hp, 1-60 stam | 1-41, 1-100 | breaks: 1-83 hp per block, with 100% block every enemy swing heals | - |
| Counter Attack | Spells/Bushido/CounterAttack.cs | free swing on block; no skill scaling | clamps | clamps (but fires on every block once block = 100%) | | | 40 -> 77.5 |
| Lightning Strike armor-ignore chance | Spells/Bushido/LightningStrike.cs:28-33 | B^2/72000 | 20% | clamps: 100% at 268.3 | clamps | clamps | 50 -> 87.5. PvP armor-ignore capped 35 dmg (Misc/AOS.cs:155-159) |
| Honorable Execution damage scalar | Spells/Bushido/HonorableExecution.cs:18-20 | 1 + B*0.002 | +24% | +60% | +100% | +200% (inside the 300% percentageBonus cap, BaseWeapon.cs:1874) - clamps there | 25 -> 62.5 |
| HE heal on kill | HonorableExecution.cs:38-41 | 20 + B^2/480 | 50 | scales: 207 (~full player HP) | breaks: 540 full heal per kill | breaks: 2103 | - |
| HE swing-speed bonus | HonorableExecution.cs:43; BaseWeapon.cs:1419 | max(1, B^2/720) % SSI | 20 | clamps (125 -> SSI cap 60, reached at B 208) | clamps | clamps | - |
| Momentum Strike damage | Spells/Bushido/MomentumStrike.cs:46-60 | damageBonus B/100 -> +(B-100)% | +20% | +200% | clamps at B 400 (300% cap) | clamps | MomentumStrike.cs:65-67 CheckSkill(Bushido, 70, 120) -> 120 |
| Honor Perfection ramp | Engines/Virtues/HonorContext.cs:117-129 | +B/10 per hit, cap 100 | 12/hit | 30/hit | 50/hit | clamps (100 in one hit) | - |
| Feint (max Bushido/Ninjitsu) | Weapons/Abilities/Feint.cs:35-41; applied BaseWeapon.cs:1994-1998 and Spells/Base/SpellHelper.cs:1029-1033 | reduction = (int)(20 + 3*(S-50)/7) % | 50% | breaks (live today): 127% -> damage <= 0, AOS.Damage returns 0 (Misc/AOS.cs:52-55): full immunity to that target's weapon AND spell damage for 6 s, repeatable | breaks: 212% | breaks: 427% | reaches 100% at S 236.7 |
| Defense Mastery phys resist | Abilities/DefenseMastery.cs:30-39 | 50 + 30*(S-50)/70 | 80 | 157 | 242 | 457 -> all clamp to player resist cap 70 (Server/Mobiles/Mobile.cs:431, :3251) at S 96.7 | - |
| Block (DCI) | Abilities/Block.cs:29-34 | 10*((S-50)/70 + 5) | 60 | 85 | 114 | 185 -> DCI cap 45 (BaseWeapon.cs:1343) - clamps from the start | - |
| Nerve Strike damage / paralyze | Abilities/NerveStrike.cs:54-71 | 15*(B-50)/70 + 0..9 armor-ignoring; para (150/7 + 4B/7)% | 15-24, 90% | 53-62, clamps 100% at 137.5 | 96-105 | 203-212 vs monsters (scales hard); PvP capped 35 | - |
| Riding Swipe damage | Abilities/RidingSwipe.cs:42, :60 | 10 + (int)(10*(B-50)/70 + 5) | 25 | 50 | 79 | 150 - scales | - |
| Frenzied Whirlwind total per target / 3 s | Abilities/FrenziedWhirlwind.cs:34-38 | 10*((S-50)/70 + 5) | 60 | 85 | 114 | 185 - scales | - |
| Whirlwind Attack bonus | Abilities/WhirlwindAttack.cs:58-64 | 1 + (n*B/60)^2/100, max 2.0 | scales | clamps (2.0 at n*B = 600) | clamps | clamps | - |
| Bladeweave pool | Abilities/Bladeweave.cs:44-46 | >= 50 | clamps | clamps | clamps | clamps | - |
| Samurai spell / move gating | Spells/Bushido/SamuraiSpell.cs:46,67; SamuraiMove.cs:9 | value >= req (25-70) | clamps | clamps | clamps | clamps | spells/moves gain in [req-12.5, req+37.5]; max is Momentum Strike 120 |
| Special-move mana total | WeaponAbility.cs:191 | counts | clamps at 300 | | | | |

Bushido GAIN CEILING: 120 (Momentum Strike). No other use gains Bushido above 107.5. Values above 120 can only come from scrolls/admin/bonuses.
Recommendation: give Bushido new effects past 120 rather than scaling these: hard-cap Feint at 50%, cap Evasion duration at 8 s (or below the cooldown), cap Confidence/HE heals (e.g. clamp B at 120 inside them), and keep the no-shield parry product P*B using min(P,120)*min(B,120).

#### Focus

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Stamina regen points (uncapped part) | customizations\RegenRates.cs:97 (= pinned Misc/RegenRates.cs:97) | (int)(F*0.1); interval 1/(0.1*(2+pts)) s | 12 -> 0.71 s/stam (1.4/s) | 30 -> 0.31 s (3.2/s) | 50 -> 0.19 s (5.2/s) | breaks: 100 -> 0.098 s (10.2 stam/s), stamina drain/leech effects become irrelevant | CheckBonusSkill chance = cur/max*(1-v)+v, v = sqrt(F*0.005) (:28-41): v = 1 at F 200 -> chance >= 1, no gain. Ceiling 200 |
| Mana regen points (uncapped part) | customizations\RegenRates.cs:154 (= pinned :154) | F*0.05 added to totalPoints; ML floors | 6 -> 1.25 s/mana (0.8/s) | 15 -> 0.59 s (1.7/s) | 25 -> 0.37 s (2.7/s) | breaks: 50 -> 0.19 s (5.2 mana/s from Focus alone, stacks with Meditation which is also uncapped) | same 200 |
| Item caps that do NOT apply to Focus | RegenRates.cs:118-121 (stam 24), :187-190 (mana 18) | caps only item/spell regen | - | - | - | - | - |

Note: pinned 18/24 player caps only touch cappedPoints, the skill points are added outside them. Our replacement file did not change this. Regen timers have no minimum interval (Server/Mobiles/Mobile.cs:8020, :8931-8940).
Recommendation: soft-cap with diminishing returns: points = 12 + 8*ln(1 + (F-120)/60) past 120 (about 20 at 300, 26 at 1000 for stamina; half that for mana), and fix the gain ceiling (chance hits 1.0 at Focus 200) by clamping v to 0.95.

#### Arms Lore

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Exceptional crafted weapon DI | Items/Weapons/BaseWeapon.cs:698-712 | 35 + (int)(AL/20), cap 50 | 41 | clamps: 50 (cap reached exactly at 300) | clamps | clamps | CheckSkill(ArmsLore, 0, 100) -> 100 |
| Exceptional crafted armor random resist points (not shields) | Items/Armor/BaseArmor.cs:595-632 | +(int)(AL/20) random points on top of 15 distributed; uncapped per item | +6 | +15 (30 bonus points per piece) | breaks: +25 (40 per piece) | breaks: +50 (65 per piece; 6 pieces = 390 bonus points, more than the 350 needed for 70 in all five) | CheckSkill(ArmsLore, 0, 100) -> 100 |
| Arms Lore active use | Skills/ArmsLore.cs:33, :89, :107 | target check 0-100; outputs clamp (Math.Min(..,30/35)) | clamps | clamps | clamps | clamps | 100 |
| Repair | Engines/Craft/Core/Repair.cs | does not read Arms Lore (grep) | - | - | - | - | - |
| Pre-AOS wrestling disarm, ThiefAI | Fists.cs:116, :216; ThiefAI.cs:58 | dead under AOS | - | | | | |

The per-player resist cap of 70 (Mobile.cs:431) limits the harm to players, but items become far above normal loot/imbue budget and tradeable.
Arms Lore GAIN CEILING: 100 (every use is 0-100).
Recommendation: cap the armor bonus like the weapon one (e.g. min(AL,300)/20 with a hard cap of +15 per piece) or give it new effects past 120 (durability, lower requirements). Fix gain ceiling if Arms Lore is meant to reach 300+.

---

#### Gain ceiling summary

| Skill | ceiling | from |
|---|---|---|
| Swords/Macing/Fencing/Archery/Throwing/Wrestling | ~220 vs 100-skill targets (260 vs 120; 145 with 45 HCI) | BaseWeapon.cs:1358-1365 direct chance |
| Tactics | none (follows Cap) | BaseWeapon.cs:2540 |
| Anatomy | none (follows Cap); bandage 120, active use 100 | BaseWeapon.cs:2543 |
| Lumberjacking (combat) | 100 | BaseWeapon.cs:2548 |
| Parry | 380 with shield (+Bushido non-racial); weapon path when P*B >= 45600 | BaseWeapon.cs:1540, :1581 |
| Bushido | 120 | MomentumStrike.cs:67 |
| Focus | 200 | RegenRates.cs:28-41 |
| Arms Lore | 100 | BaseWeapon.cs:711, BaseArmor.cs:631, ArmsLore.cs |

#### BREAKS list

1. Feint (Bushido or Ninjitsu >= 236.7): damage reduction >= 100% -> zero damage from the feinted target (weapons and spells) for 6 s. Already reachable at the live 300 cap (127%). Feint.cs:41, BaseWeapon.cs:1997, SpellHelper.cs:1032, AOS.cs:52.
2. Parry + Bushido without shield: P*B/48000 + 0.05 -> 100% block once P*B >= 45600; live at 300/300 (187%). Blocks every melee and ranged weapon hit. BaseWeapon.cs:1552.
3. Parry with shield >= 380, or Parry alone (weapon) >= 760: 100% block. BaseWeapon.cs:1520, :1554.
4. Evasion + 100% block: also evades every single-target spell and fire breath; Evasion duration >= its 20 s cooldown at Bushido >= 400 -> permanent. Evasion.cs:106, :136, :163.
5. Tactics + Anatomy damage uncapped: x5.9 at 300, x8.2 at 500, x14.8 at 1000 vs x3.9 at 120 (with 100 DI, 125 Str). BaseWeapon.cs:2557-2602.
6. Confidence: regen 112 hp/s at 500, 437 hp/s at 1000 (quadratic); heal on block up to B/12 hp and B/5 stam per block, which fires on every enemy swing once block = 100%. Confidence.cs:131; BaseWeapon.cs:1622-1623.
7. Honorable Execution heal on kill: 540 at 500, 2103 at 1000 (quadratic). HonorableExecution.cs:41.
8. Defender hit chance: at 1000 weapon skill, 100-skill monsters hit 5.9% (4.1% with 45 DCI). BaseWeapon.cs:1358.
9. Focus regen at 1000: 10.2 stam/s and 5.2 mana/s from Focus alone, outside the 18/24 item caps. customizations\RegenRates.cs:97, :154.
10. Arms Lore exceptional armor: +25 (500) / +50 (1000) resist points per piece uncapped; 70-cap trivial with any armor. BaseArmor.cs:597.
11. Shield durability: wear per block vs bashing scales with Parry (29-58 at 1000, shield gone in ~2 blocks). BaseShield.cs:24, :40-43.

Unverified: exact Katana/base damage values used in the damage example (illustrative 12 average); whether any client/other system clamps regen intervals (none found in Server Mobile.cs).

### 2.2 Magic skills (Magery, Eval Int, Resisting Spells, Meditation, Inscription, Necromancy, Spirit Speak, Chivalry, Spellweaving, Mysticism, Imbuing, Ninjitsu)

Skills: Magery, Evaluating Intelligence, Resisting Spells, Meditation, Inscription, Necromancy, Spirit Speak,
Chivalry, Spellweaving, Mysticism, Imbuing, Ninjitsu.

Paths for pinned code are relative to D:\UO\ModernUO-pinned\Projects. Shard files are under
D:\ShatteredLegacy\server\customizations (written "shard:"). Expansion = EJ (AOS/SE/ML/SA/HS/TOL all on).
Columns 120/300/500/1000 are the skill value (Skill.Value, includes item bonuses).

#### Common facts used below

- Gain wrapper: shard ClusterFSkillGain.cs:97-150 re-runs the pinned handler up to 3 times and multiplies the
  gain amount by 5, but calls the pinned handler with the SAME min/max, so every gain ceiling below is unchanged by it.
- Spell.CheckFizzle (UOContent/Spells/Base/Spell.cs:614-629): if DamageSkill != CastSkill it also calls
  CheckSkill(DamageSkill, 0, DamageSkill.Cap) (:623-626). So the damage skill of every spell school gains up to its own cap.
  Magery -> EvalInt, Necromancy -> Spirit Speak, Mysticism -> EvalInt (see Mysticism: quirk).
- AOS spell damage, Spell.GetNewAosDamage (Spell.cs:218-258):
  dmg = dice * (100 + inscBonus + Int/10 + SDI [+ReaperForm]) % * (30 + 0.09*evalFixed) % * scalar.
  - inscBonus = (inscFixed + 1000*(inscFixed/1000))/200 (:222-223). Integer division makes the intended one-time
    "+5 at GM" repeat every 100 points: 120 -> 11, 300 -> 30, 500 -> 50, 1000 -> 100. (BaseWeapon.GetAosDamage
    Items/Weapons/BaseWeapon.cs:2253-2258 uses the correct insc/200 + 5 once.)
  - evalScale = 30 + 9*evalFixed/100 (:250-251): 120 -> 138 %, 300 -> 300 %, 500 -> 480 %, 1000 -> 930 %.
  - No final cap on spell damage anywhere in pinned. Only caps: SDI 15 in PvP (:232-236), Mind Blast 60
    (Fifth/MindBlast.cs:43), Wither has its cap commented out (Necromancy/Wither.cs:123-125).
  - Combined multiplier (Int 125, SDI 0, Eval = Insc = X): 120 -> 1.70x, 300 -> 4.26x, 500 -> 7.78x, 1000 -> 19.7x.
  - In AOS no damage spell rolls CheckResisted (the resist branches are all !Core.AOS), so Resisting Spells never
    reduces spell damage; only elemental resists (cap 70) do.
- Melee percentage damage bonus (move scalars, slayers etc) is capped at +300 % (BaseWeapon.cs:1874).
- Player resists: Mobile.MaxPlayerResistance = 70 (Server/Mobiles/Mobile.cs:431). Resist > 100 on a creature makes
  AOS.Damage go to the floor of 1 (UOContent/Misc/AOS.cs:144); damage <= 0 is ignored entirely (AOS.cs:52).
- Any damage clears Paralyzed (Server/Mobiles/Mobile.cs:5932), so long paralyzes break on the first hit.
- Negative timer delays are rounded up to one tick (Server/Timer/Timer.TimerWheel.cs:176-179), so negative
  durations below just mean "instant expiry" (harmless immunity).
- Reference numbers: player HP about 150, a typical 8th-circle cast cycle is about 3 s.

---

#### Magery

Gain ceiling: 120.0 (8th circle from a book: min 80, max 120; scrolls max 92). Nothing else gains Magery.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | Spells/Base/MagerySpell.cs:15-17, :41-42 | ML table min = -18/-4/10/24/38/52/66/80 per circle (book), max = min+40 | 100 % all circles | clamps (100 % from 120) | clamps | clamps | 120 (8th circle) |
| Resist% vs target (caster side) | MagerySpell.cs:88-97 | second% = R - ((Mag-20)/5 + 5(c+1)); n = max(R/5, second)/2 | scales | scales: lowers target resist toward floor R/10 | clamps at floor R/10 | clamps (floor R/10 can't be beaten) | n/a |
| Earthquake radius | Spells/Eighth/Earthquake.cs:41, :56-65 | radius 1 + Mag/15; dmg = target Hits/2 (+0..15), NPC clamp 15-100 | 9 tiles | 21 tiles (past the 18-tile client view) | 34 tiles | BREAKS: 67-tile radius, halves the current HP of every player/creature in LOS, mostly off-screen | 120 |
| Reveal radius | Spells/Sixth/Reveal.cs:32 | 1 + Mag/20 | 7 | 16 | 26 | BREAKS (minor): 51-tile radius reveal, far past view range | 120 |
| Heal (1st) | Spells/First/Heal.cs:50-56 | Mag/12 + 1..4, x1.5 on others | 11-14 (16-21) | 26-29 (39-44) | 42-45 (63-68) | BREAKS: 84-87 self, 126-131 on others for 4 mana, 0.5 s cast | 120 |
| Greater Heal | Spells/Fourth/GreaterHeal.cs:51-52 | 0.4*Mag + 1..10 | 49-58 | 121-130 (near full HP) | BREAKS: 201-210, every cast is a full heal | BREAKS: 401-410 | 120 |
| Cure / Arch Cure | Spells/Second/Cure.cs:33-34, Fourth/ArchCure.cs:74 | (10000 + 75*Mag - (L+1)*3100..3300)/100 % | lethal 90 % | clamps 100 % (lethal at >= 206.7) | clamps | clamps | 120 |
| Poison spell level | Spells/Third/Poison.cs:75-81 | Mag+Poisoning > 200 -> level 3 (10 % lethal at <=2 tiles, SA) | level 2-3 | clamps (max level 3/4 at Mag+Pois 200) | clamps | clamps | 120 |
| Mind Blast (AOS) | Fifth/MindBlast.cs:43 | min((Mag+Int)/5, 60) | 49 | clamps 60 (at Mag+Int 300) | clamps | clamps | 120 |
| Fire Field duration | Fourth/FireField.cs:47-51 | 4 + 0.5*Mag s | 64 s | 154 s | 254 s | 504 s (scales, griefing) | 120 |
| Poison Field duration | Fifth/PoisonField.cs:44-48 | 3 + 0.4*Mag s; level by Mag+Pois (:124) | 51 s | 123 s | 203 s | 403 s (scales) | 120 |
| Energy Field duration | Seventh/EnergyField.cs:44-46 | (15 + 2*Mag)/7 s | 36 s | 88 s | 145 s | BREAKS: 288 s impassable wall, recastable; doorway/bank/spawn blocking for ~5 min | 120 |
| Paralyze Field duration | Sixth/ParalyzeField.cs:44-48 | 3 + Mag/3 s (each touch: see EvalInt) | 43 s | 103 s | 170 s | BREAKS: 336 s field, combined with 1000 EI touch = 90 s (player) / 270 s (NPC) paralyze per touch | 120 |
| Summon durations (elementals, daemon, Summon Creature) | Eighth/AirElemental.cs:49 etc, Fifth/SummonCreature.cs:77 | 4*Mag s | 8 min | 20 min | 33 min | 67 min (scales; summon stats NOT scaled: every call passes scaleStats=false, Base/SpellHelper.cs:520-537 unused) | 120 |
| Invisibility duration | Sixth/Invisibility.cs:55 | 1.2*Mag s | 144 s | 360 s | 600 s | 1200 s (scales; ends on action) | 120 |
| Incognito | Fifth/Incognito.cs:113 | min(1.2*Mag, 144) s | clamps 144 | clamps | clamps | clamps | 120 |
| Dispel / Mass Dispel | Sixth/Dispel.cs:35-36, Seventh/MassDispel.cs:47 | (50 + 100*(Mag-DD)/(2*DF))/100 | scales | clamps 100 % vs every summon | clamps | clamps | 120 |
| Crafted spellbook props | Items/Skill Items/Magical/Spellbook.cs:168-210 | Magery BaseFixed tiers, top tier at 120 | clamps at 120 | clamps | clamps | clamps | n/a |
| Chivalry FC cap | Spells/Base/Spell.cs:704-708 | Magery >= 70 -> FC cap 2 | gate | gate | gate | gate | n/a |
| Polymorph | Seventh/Polymorph.cs:170-177 | ML: no timer | n/a | n/a | n/a | n/a | n/a |

recommendation: soft-cap the radius/duration/heal reads with diminishing returns: e.g. effectiveMag = 120 + 60*ln(1 + (Mag-120)/60) for Earthquake/Reveal radius, field durations and heals (300 -> ~200, 1000 -> ~260), and hard-cap Earthquake/Reveal radius at 18. Past 120 give new effects instead (e.g. reduced reagent use, FC/FCR breakpoints, extra field tiles) because cast success already clamps at 120 and Magery cannot be gained past 120 by casting.

#### Evaluating Intelligence

Gain ceiling: Cap (CheckFizzle gains it up to its cap on every Magery cast, Spell.cs:623-626). Other gain uses: EvalInt skill use 120 (Skills/EvalInt.cs:75), stat buffs/curses 120 (Base/SpellHelper.cs:323, :370). So the effective ceiling is the skill cap (300 today, 1000 by design).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS spell damage | Spell.cs:250-253 | evalScale 30 + 0.09*fixed % | 138 % | 300 % | 480 % | 930 % | Cap |
| Energy Bolt (40+1d5) with Insc = Eval, Int 125 | Sixth/EnergyBolt.cs:38 + above | 43 * combined mult | 73 | 183 (55 vs 70 resist) | 334 (100 vs 70 resist) | BREAKS: 848, 254 after 70 resist = one-shot any player | Cap |
| Flame Strike (48+1d5) | Seventh/FlameStrike.cs:36 | 51 * mult | 87 | 217 (65) | 397 (119) | BREAKS: 1005 (301 after 70 resist) | Cap |
| Chain Lightning / Meteor / Hail Storm (51+1d5) | Seventh/ChainLightning.cs:59-71, MeteorSwarm.cs:62-75 | 54 * mult, x2/count if >2 targets | 92 | 230 | 420 | BREAKS: 1064 per target (1-2 targets), AoE | Cap |
| Stat buff % (Bless/Str/Agi/Cunning) | Base/SpellHelper.cs:382-391, :393-407 | 1 + EI/10 % of raw stat | 13 % | 31 % | 51 % | 101 % (doubles all 3 raw stats of any target incl. pets; scales but strong) | 120 |
| Stat curse % (Weaken/Clumsy/Feeble/Curse/Mass Curse) | SpellHelper.cs:384-385 | 8 + (EI - targetResist)/10 %, floor 0, NO cap | 8 % vs 120 R | 26 % vs 120 R | 46 % vs 120 R | BREAKS: 96 % vs 120 R: Str 125 -> 5 (HitsMax drops, overweight), Int -> 5 (no mana, cannot cast); Mass Curse does it in an area. Against a 0-resist NPC 108 % (stat clamps at 1, Server/Mobiles/Mobile.cs:1868) | 120 |
| Buff/curse duration | SpellHelper.cs:378-380 | 1.2*EI s | 144 s | 360 s | 600 s | 1200 s (scales) | 120 |
| Paralyze duration | Fifth/Paralyze.cs:42-55 | EI/10 - R/10 s, x3 vs NPC, floor 0 | 0 s vs 120 R | 18 s vs 120 R (60 s NPC R100) | 38 s (120 s NPC) | 88 s player / 270 s NPC (scales; broken by any damage, Mobile.cs:5932) | Cap |
| Paralyze Field per touch | Sixth/ParalyzeField.cs:149-160 | 2 + int(EI/10) - int(R/10), x3 NPC | 2 s | 20 s | 40 s | 90 s / 276 s (scales, see Magery field duration) | Cap |
| Mana Drain (AOS) | Fourth/ManaDrain.cs:41 | clamp(40 + EI - R, 0, mana), returned after 5 s | 40 | 220 (full pool) | clamps (full pool) | clamps | Cap |
| Mana Vampire (AOS) | Seventh/ManaVampire.cs:41-46 | EI - R (NPC /2), capped at target mana, permanent | 0 vs 120 R | 180 (full pool of a 120-R player) | clamps | clamps (relative to target resist; bounded by target mana) | Cap |
| Wrestling defense (Fists) | Items/Weapons/Fists.cs:54-56 | min((Anat+EI+20)/2, 120) | clamps 120 | clamps | clamps | clamps | n/a |
| EvalInt skill use | Skills/EvalInt.cs:55 | margin of error 20 - EI/5, floor 0 | clamps at 100 | clamps | clamps | clamps | 120 |

recommendation: soft-cap EvalInt's damage term: evalScale = 138 + 100*ln(1 + (EI-120)/100) (300 -> ~240 %, 1000 -> ~360 %) and cap the stat curse at about 25 % (OSI-like); keep stat buff linear but cap at 30-40 %. New effects past 120 (e.g. small spell penetration of resist, longer curse duration) are safer than raw damage.

#### Resisting Spells (MagicResist)

Gain ceiling: 130 (Magery CheckResisted only gains while R < (1+c)*10 + (1+c/6)*25, 8th circle = 130, MagerySpell.cs:77-83; Mystic same :116-122; GetResistSkill gate 121, MagerySpell.cs:51-56; curses/necro use fixed 120: SpellHelper.cs:371, Necromancy/PainSpike.cs:59, MindRot.cs:58, CorpseSkin.cs:70, BloodOathSpell.cs:85). Above 130 Resist cannot be gained from spells.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS resist floor (all 5 elemental resists) | Mobiles/PlayerMobile.cs:1203-1222 | fixed>=1000: 40 + (fixed-1000)/50, clamp to MaxPlayerResistance 70 | 44 | clamps at 70 (reached at 250.0) | clamps | clamps | 130 |
| side effect of the floor | Server/Mobiles/Mobile.cs:3228-3246 + PlayerMobile.cs:1221, :1133-1136 | if max < min then max = min; floor clamps to the static 70, not the cursed max | n/a | at 250+: every resist is 70 with no gear; Curse (-10 max), Corpse Skin, Magic Reflect/Reactive Armor/Protection maluses and other resist debuffs become no-ops | same | same | |
| Resist chance vs Magery spells (AOS: Poison spell; also Mystic Bombard) | MagerySpell.cs:61-97, Third/Poison.cs:35 | n = max(R/5, R - ((CasterSkill-20)/5 + 5(c+1)))/2; n >= 1 -> always resisted | 42 % vs equal 120 caster (3rd) | BREAKS: equal 300 caster -> 114 % (8th circle: 102 %), i.e. immune at equal skill | BREAKS | BREAKS: floor R/10 = 100 % -> immune to every Magery/Mystic CheckResisted regardless of caster skill | 130 |
| Stat curse reduction | SpellHelper.cs:384-388 | 8 + (EI-R)/10 % floor 0 | 8 % vs 120 EI | 0 % (immune) vs EI < 220 | immune vs EI < 420 | immune vs EI < 920 (relative only) | 120 |
| Paralyze / Paralyze Field / Bombard paralyze | Fifth/Paralyze.cs:42, ParalyzeField.cs:152, Mysticism/BombardSpell.cs:70 | EI/10 - R/10 (Bombard: Imb-or-Focus/10 - R/10) | relative | immune vs casters below 300 | relative | relative | 130 |
| Spell Plague explosion chance | Mysticism/SpellPlagueSpell.cs:148-155 | 90 - 30*n - ((Rfixed-700)/100)*3 | 75 % first | 21 % first | BREAKS: 0 % (immune from R 370) | BREAKS: immune | 130 |
| Nether Cyclone drain reduction | Mysticism/NetherCycloneSpell.cs:81 | drain - R/800 | -15 % | -37.5 % | -62.5 % | -125 % (once the result is negative the victim GAINS stam/mana, see note) | 130 |
| Necro: Pain Spike | Necromancy/PainSpike.cs:58 | max((SS-R)/10 + 18 player/30 NPC, 1) | relative | relative | relative | floor 1 dmg vs SS 120 | 120 |
| Necro: Mind Rot / Corpse Skin / Blood Oath durations | MindRot.cs:57, CorpseSkin.cs:72, BloodOathSpell.cs:84 | (SS-R)/5+20, (SS-R)/2.5+40, (SS-R)/80+8 s | relative | negative durations vs SS 120 (instant expiry, harmless immunity) | same | same | 120 |
| Evil Omen | EvilOmen.cs:57 | halves Resist via skill mod | scales | scales | scales | scales | |
| Protection malus | Second/Protection.cs:139 | -35 + caster Insc/20 resist skill | see Inscription | | | | |
| Revenant/AnimatedWeapon get resist = caster skill | Mobiles/Monsters/AOS/Revenant.cs:19-27, AnimatedWeapon.cs:65 | see Spirit Speak / Mysticism | | | | | |

Note on Nether Cyclone at very high target Resist: resistedReduction = reduction - R/800 can go negative; m.Stam -= (int)(StamMax * negative) ADDS stamina/mana to the victim (NetherCycloneSpell.cs:81-84). With caster 120/120 vs R 300: 0.2 - 0.375 = -0.175 -> victim gains 17 % stam and mana per cast. BREAKS (sign flip) at R >= ~200 vs a 120/120 mystic; this is the Resist side of the same formula.

recommendation: replace the floor R/10 term and the second% term with a curve that never reaches 100 %, e.g. resist% = 50 * (R - casterSkill/2) / (R + 100), cap 75 %; give the resist floor a lower slope (e.g. 40 + (R-100)/10, still clamped 70, reaching cap at 400) and do NOT let the floor override curse/debuff maxima (clamp min to the current max, not the static 70). Clamp Nether Cyclone resistedReduction at 0. Past 130 Resist needs a gain source (none exists).

#### Meditation (shard: Meditation.cs and RegenRates.cs replace pinned Skills/Meditation.cs and Misc/RegenRates.cs)

Diffs from pinned: Meditation.cs:46-59, :85-87, :92 (active gain max raised from 100 to the skill cap; armored meditation allowed above 200); RegenRates.cs:156-165 (armored medPoints kept at max(0.1, 1 - 0.02*armorOffset) when meditating above 200). Everything else in RegenRates is identical to pinned.

Gain ceiling: active use = skill Cap (shard Meditation.cs:92, chance = value/cap, true-no-gain at cap). Passive regen check = 200.0: CheckBonusSkill v = sqrt(S*0.005) (shard RegenRates.cs:35-41) reaches 1.0 at S = 200, so n >= 1 and the direct check returns true with no gain for every mana state. Same 200 ceiling for Focus (stam and mana regen checks).

Mana regen (shard RegenRates.cs:146-202), AOS: medPoints = (Int + 3*Med) * (Med < 100 ? 0.025 : 0.0275); meditating adds min(medPoints, 13); Focus adds 0.05*Focus; RegenMana items capped 18 (ML); floor(total); mana/s = 0.1*(2 + total).
Numbers below: Int 125, Focus 0, no items, unarmored.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Passive mana regen | shard RegenRates.cs:148-150, :167, :202 | see above | 13 pts -> 1.5 mana/s (2.8 meditating) | 28 -> 3.0/s (4.3 med) | 44 -> 4.6/s (5.9 med) | BREAKS: 85 -> 8.7/s (10.0 med); with Focus 1000 and MR 18: 166 -> 16.8 mana/s, enough to chain-cast 8th circle with no mana limit (8th = 50 mana per ~3 s) and infinite Energy Bolts with LMC 40 even without meditating | 200 (passive), Cap (active) |
| Active meditate chance | shard Meditation.cs:83 | (50 + (Med - missingMana)*2)/100 | 90 % at 100 missing | clamps 100 % unless >275 mana missing | clamps | clamps | Cap |
| Armored meditation (shard) | shard Meditation.cs:50-59, :86-87; RegenRates.cs:161-164 | allowed only at Med > 200; chance and medPoints x max(0.1, 1 - 0.02*armorOffset) | blocked | allowed, penalised | allowed | allowed (medPoints 85.9 x penalty: with offset 25 -> x0.5 -> still 43 pts = 4.5 mana/s in plate) | n/a |
| Focus stam regen (not in my list, same file) | shard RegenRates.cs:95-128 | points = 0.1*Focus + capped 24 | 12 -> 1.4 stam/s | 30 -> 3.2/s | 50 -> 5.2/s | 100 -> 10.2/s (12.6 with items) | 200 |
| Focus mana regen | RegenRates.cs:152-154 | +0.05*Focus pts | +0.6/s | +1.5/s | +2.5/s | +5.0/s | 200 |

recommendation: soft-cap with diminishing returns: medPoints = 13.3 * (1 + ln(1 + (Med-120)/120)) above 120 (300 -> ~25, 1000 -> ~40 pts, i.e. 4.2 mana/s), and keep the meditating bonus capped at 13. Note the passive gain ceiling of 200 is below the shard's 300 cap: points 200-300 come only from active use.

#### Inscription

Gain ceiling: 150.0 (Mystic Spellbook craft 50-150, Engines/Craft/DefInscription.cs:457; Spellbook 50-126 :439; 8th-circle scrolls 75-125 :173-174; Mystic 7th-circle scrolls 60.7-110.7; necro scrolls min..min+1). Crafting runs through the shard's CraftItem.cs (replaces pinned): shard CraftItem.cs:855-913 keeps CheckSkill(min, max) per craft skill, so the ceilings are unchanged; success chance > 1 above max is harmless.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Spell damage bonus | Spell.cs:222-224 | (fixed + 1000*(fixed/1000))/200 % (bug: +5 per 100 skill) | +11 % | +30 % | +50 % | +100 % (scales; multiplies with Eval, see EvalInt BREAKS) | 150 |
| Weapon hit-spell damage bonus | Items/Weapons/BaseWeapon.cs:2247-2283 | fixed/200 + 5 (once) | +11 % | +20 % | +30 % | +55 % (scales) | 150 |
| Reactive Armor (AOS) | Spells/First/ReactiveArmor.cs:192-195 | phys +15 + Insc/20, elem -5 | +21 | +30 | +40 | +65 (clamps at player cap 70) | 150 |
| Magic Reflect (AOS) | Spells/Fifth/MagicReflect.cs:86-87 | phys -25 + Insc/20, elem +10 | -19 | -10 | 0 | BREAKS: +25 phys AND +10 all elem; the intended drawback inverts into a pure buff (limited by the 70 cap) | 150 |
| Protection (AOS) | Spells/Second/Protection.cs:138-145 | phys -15 + Insc/20; Resist skill -35 + Insc/20; disrupt immunity 100 % | -9 / -29 | 0 / -20 | BREAKS: +10 phys / -10 | BREAKS: +35 phys and +15 Resisting Spells, plus no spell disruption; only cost left is -2 FC | 150 |
| Runebook charges | Items/Skill Items/Magical/Runebook.cs:104 | min(5 + quality + Insc/30, 10) | clamps 10 | clamps | clamps | clamps | n/a |
| Slayer spellbook | Spellbook.cs:168-210; Spell.cs:328-373 | slayer from crafted props (reads Magery, not Inscription); x2 damage | n/a | n/a | n/a | n/a | n/a |
| Scroll crafting success | shard CraftItem.cs:898-905 | (Insc - min)/(max - min) | 100 % all magery scrolls | clamps | clamps | clamps | 150 |

recommendation: fix the inscBonus integer bug (use fixed/200 + (fixed >= 1000 ? 5 : 0)) and soft-cap it (e.g. 10 + 10*ln(1 + (Insc-100)/100)); clamp the Magic Reflect and Protection maluses at 0 (they should never turn into bonuses). New effects past 150: scroll quality tiers or reduced mana on scribed scrolls.

#### Necromancy

Gain ceiling: 120.0 (Exorcism / Vengeful Spirit RequiredSkill 80 + 40, NecromancerSpell.cs:37-41; Vampiric Embrace override 80-120, VampiricEmbrace.cs:32-42). Necromancy itself only gates spells; spell power is Spirit Speak (DamageSkill, NecromancerSpell.cs:15).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | NecromancerSpell.cs:37-41 | min = req, max = req+40 | 100 % all | clamps | clamps | clamps | 120 |
| Animate Dead ability | Necromancy/AnimateDeadSpell.cs:313-317 | (30*Necro + 70*SS)/10*18, clamp to corpse Fame | ~21600 | clamps at corpse fame | clamps | clamps | 120 |
| Summon Familiar gates | SummonFamiliar.cs:140-148 | Necro/SS thresholds | clamps | clamps | clamps | clamps | n/a |
| Dispel Evil drain (target side) | Chivalry/DispelEvil.cs:105 | 0.5*Chiv/max(Necro,1) | relative | relative | relative | relative | n/a |
| Forms (Lich, Wraith, Vampiric, Horrific Beast) | LichForm.cs, VampiricEmbrace.cs, HorrificBeast.cs | fixed offsets; only Wraith reads SS (see Spirit Speak) | n/a | n/a | n/a | n/a | |
| Karma loss per cast | NecromancerSpell.cs:22-35 | fixed by cast time | n/a | | | | |

recommendation: Necromancy itself clamps at 120 harmlessly; give it new effects past 120 (e.g. extra Animate Dead slot, form bonuses scaling with (Necro-120)) rather than scaling, because Spirit Speak is where the runaway is.

#### Spirit Speak

Gain ceiling: Cap (necro casting gains it via CheckFizzle, Spell.cs:623-626). Other uses: ghost listening 100 (Skills/SpiritSpeak.cs:32), self-heal 120 (:159).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Spirit Speak heal | Skills/SpiritSpeak.cs:137-138, :159-176 | 1 + 0.25*SS .. +4 hits, 10 mana or free with a corpse, ~1 s cast | 31-35 | 76-80 (strong) | BREAKS: 126-130 (full heal) | BREAKS: 251-255 per ~1-2 s, free near corpses | 120 |
| Pain Spike | Necromancy/PainSpike.cs:58, :78-80, :105-113 | (SS-R)/10 + 18 (player) / 30 (NPC), raw damage ignoring resists, restored after 10 s, leeches | 18 vs R120 | 36 | 56 | BREAKS: 106 unresistable vs R120 player, 120 vs NPC R100, for 5 mana and a 1 s cast | Cap |
| Poison Strike | PoisonStrike.cs:61 | 32-40 * (300 + 9*SS)/1000 * SDI | ~50 | ~108 | ~173 | BREAKS: ~335 pre-resist (100 after 70 poison resist) | Cap |
| Wither (AoE cold) | Wither.cs:106-118 | 30-35 * (300 + Karma/100 + 10*SS)/1000, cap commented out | ~44 (vs -15000 karma) | ~102 | ~167 | BREAKS: ~330 AoE pre-resist | Cap |
| Strangle | Strangle.cs:86-95, :139-147, :186-200 | ticks = max(4, SS/10)-1; per tick (SS/10 -2..+1) * (3 - 2*stam%), x1.75 NPC; duration 3*SS/10 + 5 s; poison type | 11 ticks x 11.5 = ~127 over 41 s | ~856 over 95 s (7x baseline, quadratic) | BREAKS: ~2400 over 155 s, 50-150/tick | BREAKS: ~9850 over 305 s, 100-300 per tick (x1.75 NPC) | Cap |
| Mind Rot duration | MindRot.cs:57 | ((SS-R)/5 + 20) s, x2 NPC | 20 s | 56 s | 96 s | 196 s player / 392 s NPC (scales) | Cap |
| Blood Oath duration | BloodOathSpell.cs:84 | (SS-R)/80 + 8 s | 8 s | 10 s | 13 s | 19 s (scales) | Cap |
| Corpse Skin duration | CorpseSkin.cs:72 | (SS-R)/2.5 + 40 s | 40 s | 112 s | 192 s | 392 s (scales; resist mods nullified by the Resist floor on 250+ R players) | Cap |
| Evil Omen duration | EvilOmen.cs:62 | SS/12 + 1 s | 11 s | 26 s | 43 s | 84 s (scales) | Cap |
| Curse Weapon duration | CurseWeapon.cs:51 | SS/3.4 + 1 s (50 % life leech) | 36 s | 89 s | 148 s | 295 s (scales) | Cap |
| Wraith Form mana leech | WraithForm.cs:37-38 | 5 + 15*SS/100 % of melee damage dealt, capped by target mana | 23 % | 50 % | 80 % | BREAKS: 155 %, leeches more mana than damage dealt | Cap |
| Vengeful Spirit (Revenant) | VengefulSpirit.cs:49; Mobiles/Monsters/AOS/Revenant.cs:19-45 | duration SS*2/3 + 10 s; Resist/Swords = SS; resists 40+20*(SS/120)..50+... | 76 s, 60-70 resists | 210 s, phys/cold/energy 90-100 | BREAKS: 343 s, phys/cold/energy 123-133 % -> only 1 damage per hit (AOS.cs:144), Swords 500 | BREAKS: 677 s, resists 206-216 %, Swords/Resist 1000; effectively unkillable hunter | Cap |
| Ghost listening duration | SpiritSpeak.cs:37-39 | Base/50*90 s | 216 s | 540 s | 900 s | 1800 s (harmless) | 100 |
| Exorcism gate | Exorcism.cs:74 | SS >= 100 | gate | gate | gate | gate | |

recommendation: soft-cap Spirit Speak as a power stat: effSS = 120 + 80*ln(1 + (SS-120)/80) (300 -> ~200, 1000 -> ~290) for all damage/heal/leech formulas; hard-cap Wraith leech at 30-40 %, Pain Spike at about 40, Strangle tick count at 12 and per-tick power at 15, Revenant resists at 70 and skill at 120.

#### Chivalry

Gain ceiling: 115.0 (RequiredSkill + 50, Noble Sacrifice req 65, PaladinSpell.cs:126-130; DamageSkill == CastSkill so no extra gain). Note the HS Divine Fury upgrade needs Chivalry >= 120 (DivineFury.cs:46), which cannot be reached by casting.

Power value = sqrt(Karma + 20000 + 100*Chiv) (PaladinSpell.cs:136-146). With Karma 15000: 120 -> 216, 300 -> 254, 500 -> 291, 1000 -> 367 (sqrt growth, already soft).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | PaladinSpell.cs:126-130 | min = req, max = req+50 | 100 % | clamps | clamps | clamps | 115 |
| Close Wounds | CloseWounds.cs:65 | clamp(power/6 + 0..2, 7, 39) | 36-38 | clamps 39 (at ~143-198) | clamps | clamps | 115 |
| Consecrate Weapon duration | ConsecrateWeapon.cs:91 | clamp(power/20, 3, 11) s | 10 s | clamps 11 (at ~134) | clamps | clamps | 115 |
| Divine Fury duration | DivineFury.cs:44-48 | clamp(power/10, 7, 24) s; HS boost at Chiv>=120 and Karma>=10000 (15/20/15/10 vs 10/10/10/20) | 21 s, boost | clamps 24 (at ~226) | clamps | clamps | 115 |
| Enemy of One duration | EnemyOfOne.cs:42 | clamp(power/60, 1.5, 3.5) min | clamps 3.5 | clamps | clamps | clamps | 115 |
| Holy Light | HolyLight.cs:74 | clamp(power/10 + 0..2, 8, 24) | 21-23 | clamps 24 | clamps | clamps | 115 |
| Noble Sacrifice heal | NobleSacrifice.cs:102 | clamp(power/10 + 0..2, 8, 24) | 21-23 | clamps 24 | clamps | clamps | 115 |
| Cleanse by Fire cure / self-damage | CleanseByFire.cs:51, :97 | (10000 + 75*Chiv - (L+1)*2000)/100 %; self dmg clamp(50 - power/4, 13, 55) | lethal 90 %; 13 dmg | clamps 100 % (lethal at 133.3) | clamps | clamps | 115 |
| Dispel Evil: dispel summons | DispelEvil.cs:45, :65-66 | (50 + 100*(Chiv-DD)/(2*DF))/100 * power/200 | partial | clamps 100 % vs every summon in 8 tiles | clamps | clamps | 115 |
| Dispel Evil: flee | DispelEvil.cs:90-91 | (100 - sqrt(Fame/2)) * Chiv * power/2 / 1e6 | 17 % (fame 15000) | 51 % | 97 % | clamps 100 % | 115 |
| Dispel Evil: drain transformed necros | DispelEvil.cs:105-110 | 0.5*Chiv/Necro; drain 5*power/2/100 | relative | relative | relative | relative | 115 |

recommendation: Chivalry already clamps almost everywhere by 120-230 (harmless; points past ~230 are wasted). Let it scale nowhere new; give new effects past 120 instead (e.g. tithing cost reduction, extra Close Wounds cap, Consecrate damage bonus), and make 120 reachable by casting (raise the gain max) if the HS Divine Fury tier should be earnable.

#### Spellweaving

Gain ceiling: 117.5 (Word of Death req 80 + 37.5, ArcanistSpell.cs:85-89). DamageSkill == CastSkill. Wildfire is NOT implemented in pinned (no WildfireSpell; only a ConPVP option name, Engines/ConPVP/RulesetLayout.cs:255) - unverified on the shard side, nothing in customizations.

Focus level (Arcane Focus strength) comes from the number of arcanists in the circle, not from skill (ArcaneCircle.cs:55-56). Arcane Circle only accepts arcanists within 20 skill of the caster (ArcaneCircle.cs:113-117): a 300+ weaver can no longer circle with 120 players (side effect).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | ArcanistSpell.cs:85-89 | min = req-12.5, max = req+37.5 | 100 % | clamps | clamps | clamps | 117.5 |
| Resist check | ArcanistSpell.cs:127-139 | (50 + 2*(R - SW))/100 | 50 % at equal | relative (0 % vs R <= SW-25) | relative | relative | |
| Arcane Circle focus duration | ArcaneCircle.cs:50-53 | max(1, SW/24) hours | 5 h | 12 h | 20 h | 41 h (harmless) | 117.5 |
| Arcane Summon duration | ArcaneSummon.cs:35-36 | SW/24 + 2F min | 5 min | 12 min | 20 min | 41 min (scales) | 117.5 |
| Attune Weapon absorb | AttuneWeapon.cs:53-58 | 18 + 3*(SW-10)/10 + 6F melee damage absorbed, 60+12F s, recast after expiry | 51 | 105 | 165 (more than a player's HP) | BREAKS: 315-351 absorb pool (2x player HP) every ~60 s | 117.5 |
| Essence of Wind duration | EssenceOfWind.cs:34 | SW/24 + F s (damage fixed 25+F) | 5 s | 12 s | 20 s | 41 s (scales) | 117.5 |
| Ethereal Voyage | EtherealVoyage.cs:69 | 12 + SW/24 + 2F s | 17 s | 24 s | 32 s | 53 s (scales; 5 min cooldown) | 117.5 |
| Gift of Life hits on res | GiftOfLife.cs:30, :64; Gumps/ResurrectGump.cs:268-270 | (SW/2.4 + F)% of HitsMax; duration (SW/24)*2 + F min | 50 % | clamps 100 % (at 240) | clamps | clamps; duration 82 min | 117.5 |
| Gift of Renewal | GiftOfRenewal.cs:53-54 | 5 + SW/24 + F hits per 2 s for 30+10F s, 60 s cooldown | 10/2 s (150 total) | 17/2 s (255) | 25/2 s (375) | BREAKS: 46/2 s = 23 HP/s, 690 HP per cast (52/tick for 90 s at F6 = 2340) | 117.5 |
| Immolating Weapon | ImmolatingWeapon.cs:52-53 | dmg 5 + SW/24 + F fire per hit, 10 + SW/24 + F s | 10 dmg / 15 s | 17 / 22 s | 25 / 30 s | 46 fire per hit / 51 s (scales; 14 after 70 resist) | 117.5 |
| Nature's Fury duration | NatureFury.cs:46 | SW/24 + 25 + 2F s | 30 s | 37 s | 45 s | 66 s (scales) | 117.5 |
| Thunderstorm | Thunderstorm.cs:36 | max(11, 10 + SW/24) + F energy AoE | 15 | 22 | 30 | 51 (scales) | 117.5 |
| Word of Death | WordOfDeath.cs:46-66 | SW/5..SW/3 chaos (+SDI, 15 PvP); 300 flat if NPC below 5F % HP | 24-40 | 60-100 | 100-166 | 200-333 (scales, 60-100 vs 70-resist player) | 117.5 |
| Reaper Form | ReaperForm.cs:24-30 | focus only | n/a | | | | |

recommendation: soft-cap the SW/24 terms (e.g. 5 + 5*ln(1 + (SW-120)/120) beyond 120) and hard-cap Attune Weapon absorb at about 60 and Gift of Renewal per-tick at about 15. Widen or remove the +-20 skill window on Arcane Circle so high-skill weavers can still form circles.

#### Mysticism

Implemented in pinned: Animated Weapon, Bombard, Cleansing Winds, Eagle Strike, Hail Storm, Nether Cyclone, Spell Plague, Stone Form (Spells/Mysticism). NOT implemented: Nether Bolt, Healing Stone, Purge Magic, Enchant (Mystic Weapon), Sleep, Mass Sleep, Spell Trigger, Rising Colossus (only scroll items exist, e.g. Items/Skill Items/Magical/Scrolls/Mysticism/MassSleepScroll.cs). So "Sleep" and "Mystic weapon" have no formulas to audit (unverified on the shard: nothing in customizations).

Gain ceiling: 120.5 (8th circle req 83 + 37.5, MysticSpell.cs:9, :46-54).
Quirk: MysticSpell overrides GetDamageSkill/GetDamageFixed to max(Imbuing, Focus) (MysticSpell.cs:42-44) but not the DamageSkill property, which stays EvalInt (Spell.cs:52). CheckFizzle therefore gains EvalInt, not Imbuing/Focus, on every Mystic cast (Spell.cs:623-626). Damage scales with Imbuing/Focus through GetNewAosDamage.
Below, M = Mysticism, I = max(Imbuing, Focus), shown as M = I = X.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | MysticSpell.cs:46-54 | min = req-12.5, max = req+37.5 | 100 % | clamps | clamps | clamps | 120.5 |
| Spell damage (Hail Storm / Nether Cyclone 51+1d5, Bombard 40+1d5, Spell Plague, Eagle Strike) | HailStormSpell.cs:62, NetherCycloneSpell.cs:72, BombardSpell.cs:58, SpellPlagueSpell.cs:57/161, EagleStrikeSpell.cs:68 | GetNewAosDamage with I as eval | Hail 92 | 230 | 420 | BREAKS: Hail/Cyclone ~1064 AoE, Bombard ~848 | n/a (casting gains EvalInt, not I) |
| Resist% vs target (caster side) | MysticSpell.cs:127-136 | as Magery with M | | | | | |
| Bombard paralyze | BombardSpell.cs:67-75 | I/10 - R/10 s (no NPC x3) | relative | 18 s vs R120 | 38 s | 88 s (scales, breaks on damage) | |
| Bombard knockback | BombardSpell.cs:78-82 | (M + I - R)/20 used as a probability | already >= 1 at 120 (pinned bug: comment says 12 %) | always | always | always | |
| Nether Cyclone stam/mana drain | NetherCycloneSpell.cs:73-84 | (M+I)/1200 - R/800 of max stam and mana | 5 % vs R120 | 35 % | 68 % | BREAKS: 152 % -> wipes all stamina and mana of every target in the AoE (stam 0 = cannot move); negative values ADD stam/mana (see Resist) | 120.5 |
| Cleansing Winds heal | CleansingWindsSpell.cs:46-69 | ((M+I)/4 +-3)/targets, also cures/removes curses | 60 | 150 (full heal, single target) | BREAKS: 250 single / 62 each on 4 | BREAKS: 500 single / 125 each on 4 | 120.5 |
| Stone Form resist bonus | StoneFormSpell.cs:98-110 | +(M+I)/24 all resists | +10 | +25 | +41 | +83 (clamps at 70 cap); damageBonus and resistCap (:119-120) are only shown in the buff, never applied | 120.5 |
| Animated Weapon | AnimatedWeaponSpell.cs:43-45; Mobiles/Monsters/Misc/Melee/AnimatedWeapon.cs:14-66 | level (M+I)/2: Str/Dex 10+level, Hits 20+1.5*level, Wrestling and Resist = level, duration 10+level s; damage caps at 14-18 (level 120) | 200 HP, 130 s | 470 HP, 310 s | 770 HP, wrestling 500 | BREAKS: 1520 HP, Wrestling/Resist 1000 (attackers hit it ~10 % of the time), 17 min | 120.5 |
| Spell Plague | SpellPlagueSpell.cs:148-161 | damage via GetNewAosDamage | scales | scales | scales | as damage row | |

recommendation: same damage soft-cap as EvalInt applied to I; clamp Nether Cyclone drain to [0, 0.5]; cap Cleansing Winds heal (e.g. 60 + 20*ln(1+(X-120)/60)); cap Animated Weapon level at 120 and give extra weapons (count) instead. Fix DamageSkill so Imbuing/Focus gain from Mystic casting (or document that EvalInt gains instead).

#### Imbuing (shard system; pinned ModernUO has no Imbuing crafting: SkillName.Imbuing is read only by MysticSpell.cs:42-44 and UI/tables)

Gain ceiling: 140.0 (imbue check CheckSkill(diff-20, diff+20) with diff max 120 at intensity cap 200 %, shard ArtificersImbueGump.cs:85-92, :1406; disenchant/craft essence 20-80, :1478, :1533).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Imbue success | shard ArtificersImbueGump.cs:1406, :1661-1665 | (I - (diff-20))/40, diff = 40 + (maxDiff-40)*fraction, maxDiff 100..120 | 100 % up to diff 100 (max standing: 80 %) | clamps 100 % (from 140) | clamps | clamps | 140 |
| Intensity limits / property slots | shard ArtificersImbueGump.cs:53-60, :1667-1683 | by guild standing only (100-200 %, 5-8 slots) | n/a (not skill based) | n/a | n/a | n/a | |
| Mysticism damage skill | MysticSpell.cs:42-44 | see Mysticism | 138 % | 300 % | 480 % | BREAKS via Mysticism damage (930 % eval-equivalent) | |
| Failure item damage | shard ArtificersImbueGump.cs:1411-1412 | -10 durability | | | | | |

recommendation: imbuing success clamps harmlessly at 140; points past 140 only feed Mysticism damage. Either soft-cap the Mysticism read (see Mysticism) or give Imbuing new effects past 140 (e.g. cheaper shards, small intensity bonus within guild caps). Raise the imbue gain max if 300 should be reachable by imbuing.

#### Ninjitsu

Gain ceiling: 137.5 (Animal Form Kirin/Unicorn req 100 + 37.5, Spells/Ninjitsu/AnimalForm.cs:49-50, :186). Death Strike 122.5 (NinjaMove.cs:9 with req 85). Mirror Image/ShadowJump lower.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Animal Form Dog/Cat hits regen (shard RegenRates.cs is a copy of pinned here) | shard RegenRates.cs:80-85; pinned Misc/RegenRates.cs:82 | +N/3 regen points, added AFTER the ML cap of 18; HP/s = (1+points)/10 | +40 -> 4.1 HP/s | +100 -> 10.1 HP/s | BREAKS: +166 -> 16.7 HP/s | BREAKS: +333 -> 33.4 HP/s (full heal of 150 HP in 4.5 s) | 137.5 |
| Animal Form success | AnimalForm.cs:186-204 | req..req+37.5 | 100 % all forms | clamps | clamps | clamps | 137.5 |
| Death Strike hit chance | DeathStrike.cs:35-39 | 63 + 1.1*(N-100) % | 85 % | clamps 100 % (at 133.6) | clamps | clamps | 122.5 |
| Death Strike damage (ML) | DeathStrike.cs:128-137, :56 | min(60, N/3*(0.3+0.7*hide/stealth)) direct; repeat bonus N/15 unused in ML | 40 | clamps 60 (at 180) | clamps | clamps | 122.5 |
| Focus Attack damage | FocusAttack.cs:35-38; BaseWeapon.cs:1794, :1874 | +N^2/43636 (x100 %), total bonus cap +300 % | +33 % | +206 % | clamps +300 % (at 362) | clamps | 137.5 |
| Focus Attack property bonus | FocusAttack.cs:42-49; BaseWeapon.cs:2023-2046 | 1 + 3*N^2/43636 multiplies hit-leech/hit-effect chance | x2.0 | x7.2 (any leech -> 100 %) | clamps | clamps | 137.5 |
| Backstab | Backstab.cs:16-21 | +N/360 (+stalking), inside +300 % cap | +33 % | +83 % | +139 % | +278 % (scales up to the 300 cap) | 137.5 |
| Surprise Attack defense malus | SurpriseAttack.cs:57-59; BaseWeapon.cs:1327-1362 | malus = fixed/60 DCI on target for 8 s; their = (defSkill+20)*(100 + DCI - malus) | -20 | -50 | -83 (auto-hit) | BREAKS: -166: their value goes NEGATIVE so hit chance floors at 2 % for EVERY attacker (sign inversion); at exactly DCI-malus = -100 it divides by zero (infinite chance, auto-hit). Threshold: N >= ~600 + 0.6*DCI | 137.5 |
| Mirror Image absorb / duration | BaseWeapon.cs:1747; MirrorImage.cs:171 | N/150 absorb chance; 30 + N/4 s | 80 % / 60 s | clamps 100 % (at 150) / 105 s | clamps / 155 s | clamps / 280 s | 137.5 |
| Dual Wield SSI (weapon ability, Ninjitsu secondary) | Items/Weapons/Abilities/DualWield.cs:36-39; BaseWeapon.cs:1394-1421 | 20 + 3*(N-50)/7 %, SSI cap 60 | 50 % | clamps 60 (at 143) | clamps | clamps | n/a |
| Feint (max of Ninjitsu/Bushido) | Feint.cs:35-41; BaseWeapon.cs:1994-1997; Misc/AOS.cs:52 | damage reduction 20 + 3*(S-50)/7 % for 6 s | 50 % | BREAKS: 127 % -> damage <= 0 -> AOS.Damage ignores it: total melee immunity from the feinted target (from S 236.7) | BREAKS | BREAKS: 427 % | n/a |
| Block DCI bonus (max Bushido/Ninjitsu) | Block.cs:30-34; BaseWeapon.cs:1343 | 10*((S-50)/70 + 5) (= 50 + 10*(S-50)/70), DCI cap 45 | clamps 45 | clamps | clamps | clamps | n/a |
| Defense Mastery phys | DefenseMastery.cs:30-37 | 50 + 30*(S-50)/70 phys resist mod | 80 -> clamps 70 | clamps | clamps | clamps | n/a |
| Talon Strike DoT | TalonStrike.cs:36 | 10*(N-50)/70 + 5 | 15 | 40 | 69 | 140 (scales) | n/a |
| Frenzied Whirlwind DoT per adjacent target | FrenziedWhirlwind.cs:35-39 | 10*((S-50)/70 + 5) (comment says 5-15, code gives 50-60 at 50-120) | 60 | 85 | 114 | 185 (scales; AoE) | n/a |
| Shadowjump / Ki Attack | ShadowJump.cs, KiAttack.cs:93-103 | gate only / distance only | n/a | | | | |
| Animal form gump gate | AnimalForm.cs:389-394 | compares Ninjitsu Fixed (x10) to ReqSkill: always passes (display bug, harmless; real gate at :178) | | | | | |

recommendation: clamp Surprise Attack malus to (100 + DCI - 1) or a flat 40, clamp Feint reduction at about 50-60 %, cap the Dog/Cat regen term (e.g. min(N/3, 40) or include it under the 18 cap). Focus Attack and Death Strike already clamp; give new effects past ~140 (e.g. extra mirror image, shorter Shadowjump stealth requirement) instead.

---

#### BREAKS summary

1. EvalInt (and Inscription bonus) spell damage: no cap, x19.7 at 1000/1000; Energy Bolt 848, Flame Strike 1005, Chain Lightning/Meteor ~1064 pre-resist: one-shot through 70 resists (Spell.cs:218-258). Same path breaks Mysticism via Imbuing/Focus.
2. EvalInt stat curse: 8 + (EI-R)/10 % with no cap: 96 % at EI 1000 vs R 120 (Str/Int to ~5, Mass Curse AoE) (SpellHelper.cs:384-385).
3. Resisting Spells: equal-skill 300 vs 300 = always resisted (immunity) for Poison spell/8th-circle checks; R 1000 = immune to every Magery/Mystic CheckResisted regardless of caster (MagerySpell.cs:88-97).
4. Resisting Spells: Spell Plague immunity from R 370 (SpellPlagueSpell.cs:150-155); Nether Cyclone drain turns into a stam/mana GAIN when R/800 > caster term (NetherCycloneSpell.cs:81-84).
5. Magery: Earthquake radius 1 + Mag/15 = 67 tiles at 1000 (halves HP of everything in LOS); Reveal 51 tiles; Energy Field 288 s walls; Paralyze Field 336 s.
6. Magery heals: Greater Heal 201-210 at 500 and 401-410 at 1000 (full heal every cast); Heal 126-131 on others at 1000.
7. Meditation (shard RegenRates.cs): 8.7 mana/s at 1000 (16.8 with Focus 1000 and items) = mana no longer limits casting.
8. Inscription: Magic Reflect phys malus inverts to +25 at 1000; Protection inverts to +10 phys at 500 and +35 phys / +15 Resist at 1000 (MagicReflect.cs:86, Protection.cs:138-139).
9. Spirit Speak: SS heal 126-130 (500) / 251-255 (1000); Pain Spike 106 unresistable at 1000; Poison Strike and Wither ~335 pre-resist; Strangle quadratic (~2400 at 500, ~9850 at 1000); Wraith leech 155 %; Revenant resists > 100 % (immune) from SS 500.
10. Spellweaving: Attune Weapon absorb 315+ at 1000; Gift of Renewal 23 HP/s at 1000.
11. Mysticism: Nether Cyclone 152 % full stam/mana wipe at 1000/1000; Cleansing Winds 250/500 heal; Animated Weapon 1520 HP with Wrestling 1000.
12. Ninjitsu: Dog/Cat regen bypasses the 18 cap: 16.7 HP/s (500), 33 HP/s (1000); Surprise Attack malus > 100 + DCI inverts hit chance to 2 % (and divides by zero at exactly -100); Feint (Ninjitsu or Bushido) >= 236.7 = 100 %+ melee immunity.

Gain ceilings: Magery 120, EvalInt Cap, Resist 130, Meditation Cap active / 200 passive, Inscription 150, Necromancy 120, Spirit Speak Cap, Chivalry 115, Spellweaving 117.5, Mysticism 120.5, Imbuing 140 (shard), Ninjitsu 137.5. Points above these come only from other skills' casts, bonuses or admin edits.

### 2.3 Thief and healer skills (Hiding, Stealth, Detect Hidden, Snooping, Stealing, Lockpicking, Remove Trap, Poisoning, Healing, Veterinary, Begging, Forensics)

Skills: Hiding, Stealth, Detect Hidden, Snooping, Stealing, Lockpicking, Remove Trap, Poisoning, Healing, Veterinary, Begging, Forensic Evaluation.

Paths are relative to D:\UO\ModernUO-pinned\Projects unless marked SL: (D:\ShatteredLegacy\server).
Expansion is Endless Journey, so the AOS/SE/ML/SA branches apply.

#### Shard overrides checked

- I grepped SL:customizations and SL:patches for SkillName.X, Skills.X and Skills[SkillName.X] for all 12 skills. None of the shard files replaces or patches the handler for any of these skills (Hiding.cs, Stealth.cs, DetectHidden.cs, Snooping.cs, Stealing.cs, LockPick.cs, RemoveTrap.cs, Poisoning.cs, Bandage.cs, Begging.cs, ForensicEval.cs).
- SL:patches\Bandage-pet-mimic-targeting.patch only adds a PetMimic feed branch. It has no effect on the formulas.
- SL:patches\StealableArtifacts-servuo-entries.patch only adds stealable-artifact entries. It has no effect on the formulas.
- The shard reads these skills in these places:
  - Starter kits: SL:customizations\CharacterCreation.cs:1018-1339.
  - Guild starter paths: SL:customizations\ClusterFGuildStarterPath.cs:48-59.
  - Guild join gates: Healing 50 and Stealing 20 in SL:customizations\ClusterFGuildSystem.cs:151,171.
  - NPC SetSkill values and NPC AI calls to UseSkill(DetectHidden/Stealth) (OrcScout, GreenGoblinScout, KepetchAmbusher, TrapdoorSpider). These only use the skill as a threshold or a cosmetic.
- Item skill bonuses that raise Skill.Value:
  - Stealth +30 on each Assassin set piece and +40 on each Hunter set piece (SetSkillBonuses).
  - CloakOfSilence Stealth +10, RoyalGuardInvestigatorCloak Stealth +20.
  - MarkOfTravesty: Healing/Stealth/Stealing +10.
  - Whether the per-piece set bonuses stack, for example Hunter 4 x 40 = +160 Stealth, is unverified.
- Related shard change: SL:customizations\ClusterFStatCaps.cs:10 sets the individual stat cap to 500 (default; it is applied through SL:patches\PlayerMobile-individual-stat-cap.patch). Dex can therefore reach 500. Bandage delay is driven by Dex (see Healing).

#### Gain ceilings (summary)

| Skill | Gain ceiling | Where |
|---|---|---|
| Hiding | 100 (0 inside a house where you are a friend) | Skills/Hiding.cs:73 |
| Stealth | 60 + 2*AR. That is 60 unarmored and at most 142 (AR 41) | Skills/Stealth.cs:96-100 |
| Detect Hidden | 100 | Skills/DetectHidden.cs:159,183,228 |
| Snooping | 100 | Skills/Snooping.cs:84 |
| Stealing | 127.5 (10-stone item, iw=100) | Skills/Stealing.cs:309 |
| Lockpicking | 140 (TMap L5, Paragon L5, ToT chest) | Items/Containers/TreasureMapChest.cs:190 |
| Remove Trap | TrapPower+30. About 180 on world chests; on tinker-made traps it is 0.9*Tinkering+30, so unbounded (930 at Tinkering 1000) | Skills/RemoveTrap.cs:61 |
| Poisoning | 100 (Deadly, Darkglow and Parasitic potions use 95-100) | Skills/Poisoning.cs:124 |
| Healing | 120 | Items/Skill Items/Misc/Bandage.cs:444-445 |
| Veterinary | 120 | Items/Skill Items/Misc/Bandage.cs:444-445 |
| Begging | 100 | Skills/Begging.cs:111 |
| Forensics | 100 | Skills/ForensicEval.cs:36,54 |

Every skill except Remove Trap stops gaining from use somewhere between 100 and 142. Points above that have to come from some other source. Remove Trap is the only skill whose gain ceiling grows with another skill (Tinkering).

---

#### Hiding

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Hide success | Skills/Hiding.cs:73 | CheckSkill(0-bonus, 100-bonus); bonus 100 in a friend's house | clamps at 100 (always succeeds) | clamps | clamps | clamps | 100 |
| "Hide in combat" range | Skills/Hiding.cs:53-71 | range = min((int)((100-H)/2)+8, 18). Blocked if your combatant is in range and LOS, or if a mobile in range targets you | BREAKS: range = -2 | BREAKS: -92 | BREAKS: -192 | BREAKS: -442 | n/a |
| Stealth gate | Skills/Stealth.cs:77 | Hiding.Base >= 30 (ML) | clamps | clamps | clamps | clamps | - |
| Detect Hidden contest (active and passive) | Skills/DetectHidden.cs:124-127, 205-208 | reveal if DH+U(-10,10) >= H+U(-10,10) | see Detect Hidden | | | | - |
| Creature AI detect | Mobiles/AI/BaseAI/BaseAI.cs:942-955 | chance = max(DH/10, DH/1.2 - min(H/2.9, S/1.8))/100 | scales | clamps at the DH/10 floor | clamps | clamps | - |
| Reveal spell / Tracking difficulty | Spells/Sixth/Reveal.cs:63-82; Skills/Tracking/Tracking.cs:311-345 | 50*(Magery+DH)/(H+S) and 50*(2*Track+DH)/(H+S), all in Fixed units | scales (ratio) | scales | scales | scales | - |
| Snoop-fail reveal | Skills/Snooping.cs:97 | Hiding/2 < rand*100 | scales | clamps at 200 (never revealed) | clamps | clamps | - |
| Death Strike scalar | Spells/Ninjitsu/DeathStrike.cs:128 | min(1, (H+S)/220) | clamps at H+S=220 | clamps | clamps | clamps | - |
| SmokeBomb/EggBomb | Items/Skill Items/Ninjitsu/SmokeBomb.cs:40, EggBomb.cs:46 | call the same Hiding.OnUse | same as above | | | | |

**Hide-in-combat details**
- At Hiding 116-117 the range is 0. At 118 and above it is negative.
- `IEntity.InRange` with a negative range is always false (Server/IEntity.cs:100-104), so your combatant can never block the hide.
- `GetMobilesInRange` clamps the range to 0 (Server/Maps/Map.MobileEnumerator.cs:74). Only a mobile standing on your own tile can block it.
- Result: from about 118 skill (including item bonuses) you can hide in melee against anyone who is attacking you.
- There is a 10 s skill delay but no other limit.

recommendation: clamp the range at its pinned 100-skill value (8 tiles) and floor it at 1, for example `Math.Clamp(..., 8, 18)`. After that, give Hiding new effects past 100 instead of letting it shrink the combat range. Options: reduced reveal chance from damage, or a longer stealth step budget.

#### Stealth

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Stealth success | Skills/Stealth.cs:96-100 | CheckSkill(-20+2AR, 60+2AR); AR >= 42 blocks it outright (Stealth.cs:91) | clamps (always succeeds at 60+2AR, at most 142) | clamps | clamps | clamps | 60 unarmored / 142 max |
| Steps | Skills/Stealth.cs:102 | max((int)(S/5), 1) | scales: 24 steps | scales: 60 | scales: 100 | BREAKS (mild): 200 steps | - |
| Running while stealthed | Mobiles/PlayerMobile.cs:3523-3536 | running costs 2 steps and reveals at 0; walking at 0 re-runs Stealth.OnUse | 12 running tiles | 30 | 50 | 100 running tiles hidden | - |
| Creature AI detect | Mobiles/AI/BaseAI/BaseAI.cs:947 | see Hiding (S/1.8 term) | scales | clamps | clamps | clamps | - |
| Reveal / Tracking | see Hiding | ratio | scales | scales | scales | scales | - |
| ShadowStrike gate | Items/Weapons/Abilities/ShadowStrike.cs:26-28 | Stealth >= 80 | clamps | clamps | clamps | clamps | - |
| Death Strike | Spells/Ninjitsu/DeathStrike.cs:128 | (H+S)/220 capped at 1 | clamps | clamps | clamps | clamps | - |

- Walking stealth is already effectively unlimited at the pinned cap: when the steps run out, OnUse runs again and always succeeds above 60+2AR.
- The step count only matters in three places:
  - Running.
  - Backstab, SurpriseAttack and KiAttack, which need steps > 0 (Spells/Ninjitsu/Backstab.cs:25, SurpriseAttack.cs:20, KiAttack.cs:31).
  - Tracking/Reveal ratios.
- At 1000 a player can run 100 tiles while hidden.

recommendation: soft-cap the steps, for example `steps = 20 + 20*ln(1 + S/100)` (about 34 at 100, about 48 at 300, about 68 at 1000), or cap running steps separately. Otherwise let it scale.

#### Detect Hidden

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Area scan range | Skills/DetectHidden.cs:153, 183-186, 198, 223 | range = (int)(DH/10); halved on a failed check (no failures at 100+). Scans mobiles and items in a (2r+1)^2 square around the target point | scales: 12 | BREAKS: 30 tiles (beyond the 18-tile view) | BREAKS: 50 | BREAKS: 100 tiles (201x201 scan) | 100 |
| Contest vs hider | Skills/DetectHidden.cs:205-208 | reveal if DH+U(-10,10) >= H+U(-10,10) | scales (relative) | scales vs players; BREAKS vs fixed-skill NPC hiders/detectors (see below) | same | same | - |
| Passive detect (Felucca PvP, within 4 tiles) | Skills/DetectHidden.cs:69-136; Mobiles/PlayerMobile.cs:3552-3564 | same +/-10 contest, 3 s debounce | scales (relative) | scales | scales | scales | - |
| Trapped container | Skills/DetectHidden.cs:158-159 | in range DH/10 and CheckSkill(0,100) | clamps at 100 (always) | clamps | clamps | clamps | 100 |
| Dungeon traps | Skills/DetectHidden.cs:245 | HS: DH >= 75 | clamps | clamps | clamps | clamps | - |
| Faction traps | Skills/DetectHidden.cs:228; Engines/Factions/Items/Traps/BaseFactionTrap.cs:173 | CheckTargetSkill(80,100); passive (DH-80)/20 | clamps at 100 | clamps | clamps | clamps | 100 |
| Reveal spell / Tracking | Spells/Sixth/Reveal.cs:71; Skills/Tracking/Tracking.cs:312 | ratio with H+S | scales | scales | scales | scales | - |
| Remove Trap gate | Skills/RemoveTrap.cs:21 | DH >= 50 | clamps | clamps | clamps | clamps | - |

**Area range**
- At 300 the scan reaches hidden players and traps up to 30 tiles away, which is off screen.
- At 1000 the radius is 100 tiles. That reveals everyone hidden across a whole town or dungeon level.
- Each use also runs a 201x201 GetMobilesInRange plus GetItemsInRange scan (a performance cost).

**Contest**
- When the hider's skill exceeds the detector's by more than 20, reveal is impossible.
- When it is lower by 20 or more, reveal is certain.
- Between players this is a fair relative contest. Against fixed-skill NPCs it becomes immunity:
  - Archer and Warrior guards have DH 100 (Mobiles/Guards/ArcherGuard.cs:64,159; WarriorGuard.cs:81,170).
  - They can never reveal a hider at 121 or higher. At Hiding 120 the chance is about 0.2 percent.
  - The shard boss SlasherOfVeils (DH 127.1) is likewise blind to Hiding 148 and higher.
- Creature AI (BaseAI) uses a different formula with a DH/10 floor, so monsters keep at least a 10 percent chance (for DH 100).

recommendation: cap the scan radius at 18, for example `Math.Min(DH/10, 18)`, or scale it as `10 + 8*(1-e^(-(DH-100)/200))`. Scale guard and NPC DH with the expected player cap, or give guards a floor chance as BaseAI already does. Above 100, new effects would fit better than a bigger radius, for example revealing stealth steps or longer trap visibility.

#### Snooping

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Peek success | Skills/Snooping.cs:84 | CheckTargetSkill(0,100) | clamps at 100 | clamps | clamps | clamps | 100 |
| "You notice X peeking" | Skills/Snooping.cs:62-63 | only if snoop < 100 and snoop < rand*100 | clamps (never noticed at 100+) | clamps | clamps | clamps | - |

recommendation: let it scale (it is harmless). Possible new effect past 100: reduced trap trigger on snoop, or seeing the victim's bank or containers nested deeper.

#### Stealing

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Single item steal | Skills/Stealing.cs:309 | CheckTargetSkill(iw-22.5, iw+27.5), iw = ceil(weight)*10 <= 100 | clamps at 127.5 (every item up to 10 st is certain) | clamps | clamps | clamps | 127.5 |
| Max item weight | Skills/Stealing.cs:24,33,254-256 | config stealing.maxWeightToSteal = 10 (unit weight + contents) | clamps | clamps | clamps | clamps | - |
| Stack amount | Skills/Stealing.cs:264-300 | amount = RandomMinMax(1, clamp(S/10/unitWeight)); check (pile*10-22.5, pile*10+27.5), so stolen pile weight is up to S/10 stones | scales: 12 st | BREAKS: 30 st | BREAKS: 50 st | BREAKS: 100 st | - |
| Gold (ML gold weight 0.02/3) | Items/Misc/Gold.cs:22 | max = S*15 gold per attempt | 1800 | 4500 | 7500 | 15000 | - |
| Caught | Skills/Stealing.cs:330 | caught = S < Random(150) | scales: 19.3 percent | BREAKS: 0 percent | BREAKS: 0 | BREAKS: 0 | - |
| Stealable artifacts | Skills/Stealing.cs:228 | S >= 100 | clamps | clamps | clamps | clamps | - |
| Faction sigil | Skills/Stealing.cs:182 | CheckTargetSkill(80,80) = gate at 80 | clamps | clamps | clamps | clamps | 80 |
| Pickpocket dips | Items/Addons/PickpocketDips.cs:61,85 | training dummy MinSkill/MaxSkill | clamps (exact max unverified) | | | | dip MaxSkill |

**Caught**
- At 150 or above (strictly > 149) a thief is never caught.
- That means no "You notice X trying to steal" broadcast and no CriminalAction from being caught.
- PermaFlags against innocent player victims still apply (Stealing.cs:406-411).

**Stacks**
- The configured 10-stone limit applies to the unit weight, not to the pile.
- Pinned skill (100) gives at most a 10-stone pile, so the two limits agreed. Above 100 the stack path bypasses the configured limit.
- Example at 300: a thief takes up to 300 iron ingots (30 stones) or 4500 gold per attempt.
- Example at 1000: up to 100 stones or 15000 gold, with at least a 45 percent success chance for any amount rolled. The skill is always at least pile-22.5, so the chance is >= 22.5/50.

recommendation:
- Cap the caught roll, for example `caught = Random(100) >= min(S, 100)*0.9`, or keep a floor like 5 percent.
- Cap the stack amount at maxWeightToSteal/unitWeight.
- Past 100, scale with diminishing returns: for example, a lower caught chance that approaches a 5 percent floor, or new effects such as stealing from equipped containers.

#### Lockpicking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Pick lock | Items/Skill Items/Thief/LockPick.cs:121,128 | gate LP >= RequiredSkill; CheckTargetSkill(LockLevel, MaxLockLevel) | scales (TMap L5 90..140: 60 percent) | clamps at 140 (always) | clamps | clamps | 140 |
| Lock data | Items/Containers/TreasureMapChest.cs:178-190 (Req 36-100, Lock Req-10, Max Req+40); Items/Containers/ParagonChest.cs:100-111 (same); Engines/Treasures of Tokuno/LesserArtifacts.cs:465-466 (95..140); Items/Containers/BaseTreasureChest.cs:88-97 (LockLevel up to 120, Max 100 so min >= max: gate 120 then certain); Items/Containers/LockableContainer.cs:31-38 (tinker-made <= 95); Multis/Camps/*.cs (Max 116) | | | | | | |
| Power generator | Items/Misc/PowerGenerator.cs:389,427-436 | 40 + rand*80 < LP | clamps at 120 | clamps | clamps | clamps | - |
| Puzzle chest hints | Engines/Khaldun/PuzzleChest.cs:589,618-647 | Base thresholds 60-100 | clamps | clamps | clamps | clamps | - |
| Remove Trap gate | Skills/RemoveTrap.cs:17 | LP >= 50 | clamps | clamps | clamps | clamps | - |

recommendation: let it scale (it clamps harmlessly at 140). Possible new effects past 140: faster picks, no lockpick breakage, or new higher-tier locks such as higher treasure-map levels.

#### Remove Trap

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Disarm container trap | Skills/RemoveTrap.cs:61 | CheckTargetSkill(TrapPower, TrapPower+30) | scales | scales | scales | scales | TrapPower+30 |
| World TrapPower | TreasureMapChest.cs:176 (level*25), ParagonChest.cs:96 (level*25), LesserArtifacts.cs:471 (100), FillableContainer.cs:163 (level*10..30), Camps (30-40), TreasureChestLevel1-4 (up to 100), MagicTrap spell (10-50) | | certain on all of these at about 180 (TMap level 6 = 150+30; the maximum map level is unverified) | clamps | clamps | clamps | about 180 |
| Tinker-made traps | Engines/Craft/DefTinkering.cs:663-666 | TrapPower = (int)(Tinkering/10)*9 | vs Tinker 120: 108..138 | vs Tinker 300: 270..300 | 450..480 | 900..930 | 0.9*Tinkering+30 |
| Faction traps | Skills/RemoveTrap.cs:96-97 | CheckTargetSkill(80,100) and Tinkering(80,100), or ML owner | clamps at 100 | clamps | clamps | clamps | 100 |

- Remove Trap stays meaningful only as the counter to player tinker traps. There it scales one-to-one with the trapper's Tinkering.
- Cross-skill note for the Tinkering auditor (not a Remove Trap formula): tinker trap damage scales with TrapLevel = Tinkering/10 (Items/Containers/TrappableContainer.ExecuteTrap.cs:65,107).
  - Explosion trap: (10..30)*level, which is 300..900 fire damage at Tinkering 300 and 1000..3000 at 1000.
  - Dart trap: (5..15)*level.
  - Poison trap level is capped at 4 (ExecuteTrap.cs:128).
  - That is a BREAK in Tinkering.

recommendation: let it scale. Optionally add new effects past world-chest power (about 180), such as salvaging the trap or reduced damage when a disarm fails.

#### Poisoning

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Apply poison | Skills/Poisoning.cs:124; potions: Lesser 0-60, Regular 30-70, Greater 60-100, Deadly/Darkglow/Parasitic 95-100 | CheckTargetSkill(min,max) | clamps at 100 (always) | clamps | clamps | clamps | 100 |
| Charges | Skills/Poisoning.cs:133 | 18 - 2*level (no skill term) | - | - | - | - | - |
| Self-poison on fail | Skills/Poisoning.cs:159 | Base < 80 and 5 percent | clamps | clamps | clamps | clamps | - |
| Infectious Strike max level | Items/Weapons/Abilities/InfectiousStrike.cs:55-64 | Darkglow min(P/33.3, 3); Parasitic min(P/25, 4); standard P/20 (Lethal = 4 at 80) | clamps at 100 | clamps | clamps | clamps | - |
| Infectious Strike +1 level | Items/Weapons/Abilities/InfectiousStrike.cs:67-68 | chance P/100 to apply Poison.IncreaseLevel | clamps at 100 (always) and BREAKS: see the bug below | BREAKS | BREAKS | BREAKS | - |
| Serpent Arrow | Items/Weapons/Abilities/SerpentArrow.cs:25 | Archery+P > 199.8 gives level 3 | clamps at sum 200 | clamps | clamps | clamps | - |
| Poison Field | Spells/Fifth/PoisonField.cs:124 | Magery+P > 199.8 gives level 3 | clamps | clamps | clamps | clamps | - |
| Poison spell | Spells/Third/Poison.cs:48-89 | Magery+P (SA: minus 31 per tile beyond 2; AOS: level 0 at dist >= 3); > 200 at dist <= 2 gives level 3, with 10 percent for 4 | clamps at sum 200 | clamps | clamps | clamps | - |
| Pet poison gain | Mobiles/BaseCreature.cs:2354 | CheckSkill(0, cap) | - | - | - | - | pet cap |

**IncreaseLevel bug (pre-existing, made certain by skill)**
- The code is `Poison.IncreaseLevel(p) = Poisons[p.Index + 1]` (Server/Poison.cs:51-52).
- `Index` is the registration id (0-4, 10-13, 20-24 in UOContent/Misc/PoisonKinds.cs:80-106). It is used as if it were a list position. With AOS and ML, the list is Lesser..Lethal (0-4), LesserDG..DeadlyDG (5-8), LesserPara..LethalPara (9-13).
- Results:
  - Lethal (4) becomes LesserDarkglow (list position 5): a downgrade from level 4 to level 0.
  - LesserDarkglow (10) becomes GreaterParasitic.
  - RegularDarkglow (11) becomes DeadlyParasitic.
  - GreaterDarkglow (12) becomes LethalParasitic: a family jump to level 4 that heals the attacker.
  - DeadlyDarkglow and all Parasitic poisons do not change.
- At Poisoning 100 and above this happens on every Infectious Strike. For Lethal weapons it is a guaranteed downgrade. For Darkglow weapons it is a guaranteed jump to Parasitic.
- The same IncreaseLevel call makes Paragon HitPoison wrong (Mobiles/BaseCreature.cs:2345).

recommendation:
- Fix IncreaseLevel so it looks up the same family at level+1, which the existing GetPoisonByFamilyAndLevel in PoisonKinds.cs:59 can do.
- Otherwise Poisoning clamps at 100 everywhere.
- Possible new effects past 100: more charges per dose, for example `18-2L + (P-100)/50`, or a chance to not consume a charge. Do not raise the poison level: it is hard-capped at 4 by the families.

#### Healing (Bandage, Healing+Anatomy; Veterinary+AnimalLore on pets)

Numbers assume Anatomy equals Healing. With Anatomy at 120 and only Healing raised, see the parenthesized values.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Heal success | Items/Skill Items/Misc/Bandage.cs:377 | (H+10)/100 - 0.02*slips | clamps (100 percent at 90) | clamps | clamps | clamps | 120 |
| Heal amount (AOS) | Bandage.cs:387-396 | min = A/8 + H/5 + 4; max = A/6 + H/2.5 + 4; minus 35 percent per slip | 43..72 (avg 58) | BREAKS: 102..174 (avg 138) (A120: 79..144) | BREAKS: 167..287 (avg 227) (A120: 119..224) | BREAKS: 329..571 (avg 450) (A120: 219..424) | 120 |
| Cure | Bandage.cs:321-322 | (H-30)/50 - 0.1*poisonLevel - 0.02*slips; needs H, A >= 60 | clamps (Lethal certain at 100; at 120 slip-proof to 20 slips) | clamps | clamps | clamps | 120 |
| Resurrect | Bandage.cs:239-240 | (H-68)/50 - 0.02*slips; needs H, A >= 80 | clamps (certain at 118) | clamps | clamps | clamps | 120 |
| Delay, self (AOS) | Bandage.cs:493 | 5 + 0.05*(120-Dex), Dex only | Dex 150: 3.5 s | Dex 220: 0 s | Dex 500: -14 s | - | - |
| Delay, others (AOS) | Bandage.cs:506-512 | Dex < 204: 3.2 - sin(Dex/130)*2.5; otherwise 0.7 s | | | | | |
| Delay, pet (Vet) | Bandage.cs:500-502 | 2.0 s fixed | | | | | |
| Gain | Bandage.cs:442-445 | CheckSkill(primary, 0, 120), CheckSkill(secondary, 0, 120) | | | | | 120 |
| Creature self-heal (NPC/pet skill) | Mobiles/BaseCreature.cs:5366-5408 | min = A/10 + H/6 + 4; max = A/8 + H/3 + 4 (+10 on self) times HealScalar; gain 90 / 60+10*level | scales (pet skill caps limit it) | | | | 90 |
| Hireling cost | Mobiles/Hireables/BaseHire.cs:140 | sum/35 | cosmetic | | | | |
| Faction guard heal gate | Engines/Factions/Mobiles/Guards/GuardAI.cs:572 | Base > 20 | cosmetic | | | | |

**Runaway healing.** Healing has no cap other than HitsMax.
- Healing on another player:
  - The healer can reach Dex 204 because the shard individual stat cap is 500, which gives a 0.7 s delay.
  - At 300/300 that is about 138 HP per 0.7 s, roughly 197 HP/s.
  - At 1000/1000 it is about 640 HP/s.
- Self-healing:
  - At Dex 220 the delay reaches 0 s, and at higher Dex it goes negative (Dex 500 gives -14 s).
  - A Timer with a negative delay should fire on the next tick (unverified), so self-bandages become about as fast as the player can click and target. There is no other rate limit in Bandage.cs.
  - The delay is a Dex issue, not a Healing issue, but it multiplies the Healing break.
- For scale: a full AOS player (Str 150, +25 HP) has about 150 HitsMax (unverified for the shard's 500 Str cap). At 300 Healing, one bandage refills most of a bar.

recommendation:
- Soft-cap the heal amount with diminishing returns past 120, for example `bonus = 120-value + 60*ln(1 + (H-120)/120)`, which gives about 1.6x the 120 amount at 300 and about 2.5x at 1000.
- Or cap it as a percent of HitsMax per bandage.
- Clamp the self-bandage delay to at least 2 s and the other-target delay to at least 0.7 s, regardless of Dex.
- Possible new effects past 120: heal-over-time, removing debuffs (Mortal Strike), or area bandaging.

#### Veterinary

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Pet heal amount | Bandage.cs:387-401 | same as Healing with Vet/AnimalLore, + HitsMax/100 | 43..72 + HitsMax/100 | 102..174 (about 69 HP/s at 2 s) | BREAKS: 167..287 (about 113 HP/s) | BREAKS: 329..571 (about 225 HP/s) | 120 |
| Pet cure / resurrect / success | Bandage.cs:239-240, 321-322, 377 | same as Healing | clamps | clamps | clamps | clamps | 120 |
| Delay | Bandage.cs:500-502 | 2.0 s fixed | | | | | |
| Stable slots | Mobiles/Vendors/NPC/AnimalTrainer.cs:58-97 | +(int)((V-90)/10) when V >= 100 (Taming and Lore give the same) | +3 | +21 | +41 | +91 (about 278 total with Taming and Lore at 1000) | - |

- Pet healing has a fixed 2 s delay and no Dex term.
- At 500 and above, one tamer keeps a high-HitsMax pet (dragon class) effectively unkillable outside burst damage.
- Stable slots scale linearly. That is a save/storage concern, not an exploit.

recommendation: use the same diminishing-returns heal curve as Healing. Optionally cap stable slots, for example a total of 15-20. Possible new effects past 120: pet buffs, or faster pet resurrection without skill loss (Bandage.cs:272-275 currently costs the pet 0.1 in every skill).

#### Begging

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Beg success | Skills/Begging.cs:111 | CheckTargetSkill(0,100) | clamps at 100 | clamps | clamps | clamps | 100 |
| Gold amount | Skills/Begging.cs:113-118 | min(theirGold/10, clamp(10 + Fame/2500, 10, 14)); no skill term | clamps | clamps | clamps | clamps | - |
| Trick or Treat | Holiday Stuff/Halloween/2006/Engines/TrickOrTreat.cs:203 | Begging >= 100 gate, 1 percent | clamps | clamps | clamps | clamps | - |

recommendation: let it scale (it has no effect past 100). If the skill should matter, give it new effects past 100, for example a better gold cap or NPC vendor discounts.

#### Forensic Evaluation

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Identify thief | Skills/ForensicEval.cs:36 | CheckTargetSkill(40,100) | clamps at 100 | clamps | clamps | clamps | 100 |
| Corpse info (killer, looters) | Skills/ForensicEval.cs:54 | CheckTargetSkill(0,100) | clamps | clamps | clamps | clamps | 100 |
| Other reads | Misc/AOS.cs:1082 (name only); healer NPC teach lists | cosmetic | | | | | |

recommendation: let it scale (it is harmless and stops having any effect past 100). Possible new effects: detecting hidden thieves nearby, or extra corpse data such as the time of death.

---

#### BREAKS list

1. **Hiding, hide in combat.** The range goes to 0 at 116 and negative from 118: (int)((100-H)/2)+8 gives -2, -92, -192 and -442 at 120, 300, 500 and 1000. From 118 on, combatants never block the hide, so you can hide while being hit. Skills/Hiding.cs:53-71.
2. **Detect Hidden scan radius.** The radius is DH/10 tiles: 30, 50 and 100 at 300, 500 and 1000. It reveals hiders and traps far off screen, and at 1000 runs a 201x201 mobile and item scan. Skills/DetectHidden.cs:153,198,223.
3. **Detect Hidden vs Hiding contest (+/-10).** It gives total immunity once Hiding is more than DH+20. Guards (DH 100) can never reveal Hiding 121 or higher. SlasherOfVeils (127.1) can never reveal Hiding 148 or higher. Skills/DetectHidden.cs:205-208. BaseAI keeps a DH/10 floor, so monsters are fine.
4. **Stealing, never caught.** The rule is caught = S < Random(150), so from 150 on the thief is never caught: no broadcast and no criminal flag from being caught. Skills/Stealing.cs:330.
5. **Stealing, stack size.** The cap is S/10/unitWeight. That bypasses stealing.maxWeightToSteal=10, allowing 30, 50 and 100 stones per theft and up to 4500, 7500 and 15000 gold per attempt at 300, 500 and 1000. Skills/Stealing.cs:264-300.
6. **Healing amount.** The heal amount has no cap. Average heal is 138, 227 and 450 HP per bandage at 300, 500 and 1000 (Healing=Anatomy). With the shard's Dex cap of 500, the other-heal delay is 0.7 s (about 197 to 640 HP/s). The self-heal delay reaches 0 s at Dex 220 and goes negative above that (Dex-driven; timer behavior unverified). Bandage.cs:387-396, 493, 506-512.
7. **Veterinary.** The pet bandage delay is a fixed 2 s, giving about 113 and 225 HP/s at 500 and 1000. Bandage.cs:387-401, 500-502.
8. **Poisoning, Infectious Strike.** The level-up fires at chance P/100, so it is certain at 100 and above. Poison.IncreaseLevel uses Index+1 as a list position, so Lethal turns into LesserDarkglow and GreaterDarkglow turns into LethalParasitic. This is a pre-existing bug that skill makes deterministic. Items/Weapons/Abilities/InfectiousStrike.cs:67; Server/Poison.cs:51-52.
9. **Stealth steps (mild).** At 1000 there are 200 steps, which allows 100 running tiles while hidden. Skills/Stealth.cs:102; Mobiles/PlayerMobile.cs:3527-3531.

Cross-skill, for the Tinkering audit: tinker trap damage is (10..30)*(Tinkering/10), which is 1000..3000 at Tinkering 1000 (Items/Containers/TrappableContainer.ExecuteTrap.cs:65). Remove Trap is the only counter.

### 2.4 Animal, bard and misc skills (Taming, Animal Lore, Herding, Musicianship, Peacemaking, Provocation, Discordance, Tracking, Item ID, Taste ID, Camping, Cartography)

Skills: Animal Taming, Animal Lore, Herding, Musicianship, Peacemaking, Provocation, Discordance,
Tracking, Item Identification, Taste Identification, Camping, Cartography.

Paths are relative to D:\UO\ModernUO-pinned\Projects unless prefixed "shard:" (= D:\ShatteredLegacy\server).
Expansion assumed Endless Journey (AOS/SE/ML/SA/HS/TOL true). Values are Skill.Value (includes mods).
Gain rules: SkillCheck.cs:53-61 / :161-169 (value >= maxSkill -> true, no gain roll), :84-87 / :190-193
(direct chance >= 1.0 -> true, no gain).

Shard overrides touching these skills (grep of shard:customizations and shard:patches):
- None of the shard files replaces AnimalTaming.cs, AnimalLore.cs, BaseInstrument.cs, Peacemaking.cs,
  Provocation.cs, Discordance.cs, Tracking.cs, ItemIdentification.cs, TasteID.cs, Kindling.cs, TreasureMap.cs,
  BaseCreature.GetControlChance, AnimalTrainer.GetMaxStabled or Bandage heal math. Pinned behavior applies.
- shard:customizations/OutridersCrook.cs:82-85 adds +5/+10/+15 Taming, +5/+10/+15 Peacemaking, +10 Lore as
  DefaultSkillMod (relative). SkillMod._obeyCap defaults false (Server/Mobiles/Mods/SkillMod.cs:25,57), so these
  go past the skill cap. Raises effective Value; does not change any formula.
- shard:customizations/ClusterFRangersSystem.cs:53 HasPeacefulTaming() says it is "called from the AnimalTaming
  patch", but no AnimalTaming patch exists in shard:patches and nothing calls it (grep). Subdue bypass is
  unwired (unverified whether a build-time hook exists elsewhere).
- shard:customizations/Mobiles/Normal/Raptor.cs:50 MinTameSkill 107.1 (highest tame difficulty on the shard;
  pinned max is 106.0). Dimetrosaur/Najasaurus/Saurosaurus 102.0.
- shard:customizations/ClusterFWorkOrderSystem.cs:151,183 work-order gates (Taming/Lore/Tracking >= minSkill).
  ClusterFGuildSystem.cs:161 Musicianship 30 gate. Pure gates: clamp, harmless.
- Item bonuses: MarkOfTravesty (+10 bard/tamer), CollectionsBritLibraryTalismans (+5), LegendaryMapmakersGlasses
  (+1..5 Cartography). Only raise Value.
- Cartography crafting goes through shard:customizations/CraftItem.cs (replaces pinned) GetSuccessChance
  (CraftItem.cs:877-895): generic min/max craft check; not re-audited here.

---------------------------------------------------------------------------------------------------------------

#### Animal Taming

Taming rule (UOContent/Skills/AnimalTaming.cs):
- Hard gate ("too difficult" / "You have no chance"): Value < MinTameSkill -> refused (:185). Not owner-adjusted.
- Final roll (:397-407): minSkill = MTS + 6*Owners + 24.9; CheckTargetSkill(Taming, min-25, min+25)
  => range [MTS + 6*Owners - 0.1, MTS + 6*Owners + 49.9]; chance = (V - MTS - 6*Owners + 0.1) / 50.
  Owners < MaxOwners=5 (BaseCreature.cs:159), so a new tamer faces up to +24.
- CanAngerOnTame creatures: 95% anger roll before taming (:209), independent of skill.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Tame gate | AnimalTaming.cs:185 | V >= MTS | clamps (all tamable at 107.1) | clamps | clamps | clamps | n/a |
| Tame roll | AnimalTaming.cs:397-407 | (V-MTS-6*Own+0.1)/50 | scales: MTS 106 fresh = 28.2%; MTS 95.1 = 50% | clamps: 100% vs everything (needs V >= 157.0 fresh / 181.0 with 4 prior owners on Raptor) | clamps 100% | clamps 100% | 157.0 (Raptor 107.1, fresh); 181.0 (Raptor, 4 owners); pinned 155.9/179.9 |
| Control chance | Mobiles/BaseCreature.cs:1408-1474 | ML: bonus = 3*(T10+L10-2*MTS10) (tenths), chance = clamp(700+bonus,220,990) - (MaxLoyalty-Loyalty)*10, /1000 | clamps: 99% once T+L >= 2*MTS+9.7 (MTS 106: T+L >= 221.7) | clamps 99% | clamps 99% | clamps 99% | n/a (no skill check) |
| Bonding req | BaseCreature.cs:4304-4306 | Value >= MTS | clamps | clamps | clamps | clamps | n/a |
| Stable slots | Mobiles/Vendors/NPC/AnimalTrainer.cs:58-97 | 2..5 by T+L+V sum, + (int)((S-90)/10) per skill >=100 | scales: all three 120 -> 14 | 68 | 128 | 278 | n/a |
| Passive AnimalLore gain during taming | AnimalTaming.cs:373,394 | Lore 0-120 | see Lore | | | | |

Notes:
- 100% taming at ~157+ is the normal "overskilled tamer" state; no exploit beyond the fact that Taming can no
  longer gain past 157 (181 using 4-owner creatures). Control is clamped at 99%, never 100% (harmless).
- Stable slots grow without bound: 278 stabled pets per character at 1000/1000/1000 (91 extra per skill).
  BREAKS (low severity): storage/hoarding and save-size abuse. 300 live already gives 68.
- recommendation: let tame/control clamp as is; cap stable slots (e.g. bonus counts only skill up to 120,
  or flat max ~ 20); if desired give Taming >157 new effects (e.g. +control slots, faster bonding, pet stat
  retention on tame instead of 0.90 ScaleSkills).

#### Animal Lore

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Lore gump on wild tamable | Skills/AnimalLore.cs:49 | V >= 100 | clamps at 100 | clamps | clamps | clamps | |
| Lore gump on wild non-tamable | AnimalLore.cs:54 | V >= 110 | clamps at 110 | clamps | clamps | clamps | |
| Lore use check | AnimalLore.cs:59 | CheckTargetSkill 0-120 -> V/120 | clamps 100% at 120 | clamps | clamps | clamps | 120 |
| Control chance (half weight) | BaseCreature.cs:1426-1453 | see Taming | clamps 99% | clamps | clamps | clamps | n/a |
| Stable slots | AnimalTrainer.cs:61,90 | +(int)((L-90)/10) | +3 | +21 | +41 | +91 | n/a |
| Vet bandage heal (Lore = secondary) | Items/Skill Items/Misc/Bandage.cs:185-189, 375-393 | AOS: min = L/8 + Vet/5 + 4, max = L/6 + Vet/2.5 + 4 (+HitsMax/100 for animals), every 2.0 s (:500-502) | scales: L+Vet 120: 23-28 lore part 15-20, total 43-72 | L+Vet 300: 101.5-174 | L+Vet 500: 166.5-287.3 | L+Vet 1000: 329-570.7 | 120 (Bandage.cs:444 CheckSkill 0-120) |
| Vet resurrect gate | Bandage.cs:237-240 | Lore >= 80 | clamps | clamps | clamps | clamps | |
| Passive gain while taming | AnimalTaming.cs:373,394 | 0-120 | | | | | 120 |

- Lore's share of bandage healing at 1000 is 125-167 HP per bandage, every 2 s, uncapped. With Vet at the
  same value a pet heals 329-571 per 2 s: BREAKS (runaway healing, pets effectively unkillable) at 500+, already
  strong at 300 (101-174/2s). Overlaps the Veterinary auditor; Lore is half the formula.
- recommendation: Lore can clamp at 120 for gump/control; soft-cap its bandage contribution
  (e.g. L_eff = 120 + 30*ln(1 + (L-120)/30)) or move >120 into new effects (pet-info detail, small pet
  resist/regen aura, stable bonus capped).

#### Herding

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Shepherd's crook command | Items/Weapons/Staves/ShepherdsCrook.cs:133-146 | CheckTargetSkill(MTS-30, MTS+30+rand(10)) | scales: 100% vs MTS<=81 | clamps 100% vs all | clamps | clamps | 145.0 pinned (MTS 106 + 39); 146.1 shard Raptor |

Only reader. recommendation: let it clamp (harmless); optional new effect: herd multiple animals / longer range.

#### Musicianship

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| CheckMusicianship (all bard skills) | Items/Skill Items/Musical Instruments/BaseInstrument.cs:527-532 | gain CheckSkill 0-120 (result discarded); success = Mus/100 > rand | clamps: 100% at 100 | clamps | clamps | clamps | 120 |
| Bard difficulty reduction (peace target, provo, discord) | Peacemaking.cs:163-169, Provocation.cs:131-138, Discordance.cs:154-160 | diff -= (Mus-100)*0.5 if Mus>100 | -10 | -100 | -200 | -450 | n/a |
| Fire Horn success | Items/Skill Items/Misc/FireHorn.cs:72-77 | direct chance 0.5 + (Mus-77.5)*0.02 | clamps 100% at 102.5 | clamps | clamps | clamps | 102.5 |
| Fire Horn damage | FireHorn.cs:115-160 | see Provocation section | | | | | |
| Carpentry instrument recipes | Engines/Craft/DefCarpentry.cs:405-426 (shard dup CarpentryCraftRegistrations.cs:61) | secondary 45-50 | clamps | clamps | clamps | clamps | 50 |

- The diff reduction is unbounded; combined with the bard difficulty cap (160) it makes every bard check
  unfailable (see the table below). BREAKS (via the bard skills).
- recommendation: soft-cap the Musicianship reduction (e.g. -(Mus-100)*0.5 up to Mus 120, then
  -10 - 10*ln(1+(Mus-120)/50)), and keep CheckMusicianship clamped.

#### Bard difficulty (BaseInstrument.cs:250-306, GetDifficultyFor :308-350)

D = (HitsMax*1.6 + StamMax + ManaMax + SkillsTotal/10, compressed above 700 by 3/11, +100 each magery /
fire breath / poison immune / vampire bat, +20*poison level) / 10, +40 paragon, then capped at 160.0 (Core.SE,
:298-301). Instrument: exceptional -5, each slayer slot -10 if it slays, +10 if target is the opposing super-slayer
group. So D in practice: max 160 natural, max 180 with a double opposing-slayer instrument; D = 200 cannot occur
in pinned content (computed anyway as asked).

Range for all three skills: GetBardRange = 8 + (int)(V/15) (BaseInstrument.cs:213):
120 -> 16, 300 -> 28, 500 -> 41, 1000 -> 74 tiles.

##### Success chance table (formula used)

Overall success = P(Mus) * P(skill).
- P(Mus) = min(1, Mus/100) (BaseInstrument.cs:531).
- Peacemaking (target mode) and Discordance: diff = D - 10 - max(0,(Mus-100)/2); P = (S - (diff-25)) / 50,
  0 if S < diff-25 (too difficult), 1 if S >= diff+25 (Peacemaking.cs:163-171, Discordance.cs:154-168).
- Provocation: diff = (D1+D2)/2 - 5 - max(0,(Mus-100)/2); same 50-wide window (Provocation.cs:131-154).
  Table uses D1 = D2 = D.
- Peacemaking area mode: CheckSkill(Peacemaking, 0, 120) -> S/120 (Peacemaking.cs:83).
Assumption: the bard has Musicianship equal to the listed skill.

| bard skill (=Mus) | D=100 peace/discord | D=160 peace/discord | D=200 peace/discord | D=100 provo | D=160 provo | D=200 provo | area peace |
|---|---|---|---|---|---|---|---|
| 120 | 100% (130%, no gain) | 10% | 0% (too difficult) | 100% (120%) | 0% (S == min) | 0% (too difficult) | 100% |
| 300 | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| 500 | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| 1000 | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

Thresholds for guaranteed success (S = Mus = X): peace/discord X >= (D+65)/1.5 -> D160: 150.0, D180: 163.3;
provo X >= (D+70)/1.5 -> D160: 153.3, D180: 166.7. Even with Musicianship at only 100, bard skill >= D+15
(peace/discord) or D+20 (provo) is guaranteed: 175/180 for D160.

=> At 300 (live today) and above, NO creature can resist any bard skill: every Peacemaking, Provocation and
Discordance attempt succeeds against every creature that is not flagged Uncalmable / Unprovokable /
BardImmune (and Provocation's paragon-with-D>=160 refusal, Provocation.cs:66). BREAKS.

#### Peacemaking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Area peace success | Peacemaking.cs:83 | S/120 | clamps 100% | 100% | 100% | 100% | 120 |
| Area peace range | Peacemaking.cs:99, BaseInstrument.cs:213 | 8 + S/15 | 16 | 28 | 41 | 74 | n/a |
| Area peace effect | Peacemaking.cs:103-123 | every harmful-able mobile in range: Combatant=null, Warmode off; creatures pacified 1 s; repeat every 5 s | scales | breaks | breaks | breaks | |
| Target peace success | Peacemaking.cs:163-171 | see table | scales (10% vs D160) | breaks: 100% vs all | breaks | breaks | D+15 with Mus<=100 (175 for D160, 195 for D180); 150-163 when Mus = S |
| Target peace duration | Peacemaking.cs:190-201 | 100 - diff/1.5 clamped 10..120 s | D160: 10 s; D100: 46.7 s | D160: 66.7 s; D100: 106.7 s | 120 s cap | 120 s cap | |

- Area peace at 300: guaranteed, 28 tiles (beyond the 18-tile client view), every 5 s. At 1000: 74 tiles.
  Resets combatants of every creature and every attackable player in range, including fights of other players
  out of the bard's sight. BREAKS (griefing / spawn-wide aggro reset; also hits players in PvP areas).
- Target peace: guaranteed 66.7-120 s pacify of any calmable creature (bosses included) from 300. BREAKS.
- recommendation: cap range at e.g. 8 + min(S,120)/15 (=16) plus small log growth; keep area success at
  S/120 but add a per-target resist roll vs D; soft-cap the diff reduction from Musicianship; new effects past
  120 could be longer duration or reduced re-aggro rather than certainty.

#### Provocation

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Provoke success | Provocation.cs:131-154 | see table | scales (0% vs D160 pair) | breaks: 100% vs all | breaks | breaks | avgD+20 with Mus<=100 (180 for D160, 200 for D180); 153-167 when Mus = S |
| Target/pair range | Provocation.cs:93,122 | 8 + S/15 | 16 | 28 | 41 | 74 | n/a |
| Provoke duration | Mobiles/BaseCreature.cs:3742 | fixed 30 s | n/a | | | | |
| Fire Horn damage (Prov x3, Disc x3, Peace x1, Mus x1) | Items/Skill Items/Misc/FireHorn.cs:115-145 | per skill fixed f: scaled = f + max(0,f-900)*2; weightAvg = (M + 3P + 3D + Pe)/80; avg = weightAvg/2 PvM, /3 PvP; min = 0.9 avg, max = avg*10/9; split *2/n if n>1 targets; radius 2, every 6 s, 100% fire | all four at 120: PvM 81-100, PvP 54-66 | PvM 324-400, PvP 216-266 | PvM 594-733, PvP 396-488 | PvM 1269-1566, PvP 846-1044 | Mus 102.5 (only Musicianship gains here) |

- Fire Horn is the biggest numeric break in this slice: all-equal X gives weightAvg = 3X - 180. At 300 a single
  horn blast does 216-266 fire to a player (65-80 after a 70 fire resist cap) and 324-400 to a monster; at 1000,
  846-1044 PvP (254-313 after 70 resist) = one-shot every 6 s, costs 4 sulfurous ash. The f>900 tripling was a
  "GM bonus" that now multiplies everything above 90. BREAKS (runaway damage) from 300.
- Guaranteed provocation of any provokable creature (bosses with D 160 included, unless paragon) at 300+. BREAKS.
- recommendation: Fire Horn: clamp each skill input at 120 (or log soft-cap) before scaling; Provocation:
  soft-cap Musicianship reduction and keep a minimum fail chance (e.g. 5%) vs D>=160.

#### Discordance

Effect (AOS branch, Discordance.cs:177-201):
effect = (int)(S/-5) for S<=100, else -20 + (int)((S-100)/-2.5); halved if base D >= 160 (:190-193).
Applied as: all 5 resists +effect (ResistanceMod), every skill of target += Value * effect/100 (:234-241), and the
abs value is exposed via GetEffect to BaseWeapon (hit chance :1334-1340, swing speed :1405-1411 and :1464-1470,
damage :2586-2592) and NinjaWeapons.cs:255.

| S | effect (normal) | effect (D>=160) | skill scalar | target skills become |
|---|---|---|---|---|
| 120 | -28 | -14 | -0.28 / -0.14 | 72% / 86% |
| 300 | -100 | -50 | -1.00 / -0.50 | 0% / 50% |
| 500 | -180 | -90 | -1.80 / -0.90 | -80% (negative) / 10% |
| 1000 | -380 | -190 | -3.80 / -1.90 | -280% (negative) / -90% (negative) |

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Discord success | Discordance.cs:154-168 | see table | scales (10% vs D160) | breaks: 100% vs all | breaks | breaks | same as target peace: 175 (Mus<=100, D160), 195 (D180) |
| Resist reduction | Discordance.cs:197-201; Misc/AOS.cs:80-86; Mobile.GetMinResistance = int.MinValue (Server/Mobiles/Mobile.cs:3249) | creature resist R + effect, damage x (100-R')/100 | R60: 32 -> dmg x0.68 | R60 -> -40 -> dmg x1.40 (boss: 10 -> x0.90) | -120 -> x2.20 (boss -30 -> x1.30) | -320 -> x4.20 (boss -130 -> x2.30) | |
| Skill reduction | Discordance.cs:234-241, Server/Skills.cs:286-327 (no floor) | Value*scalar | -28% | all skills 0 (boss -50%) | skills negative | skills strongly negative | |
| Melee damage of discorded mob | BaseWeapon.cs:2586-2592, AOS.cs:52 (damage<=0 -> nothing) | damageBonus -= 2*effect (only capped above at +100) | -56% | -200% -> 0 damage (boss -100% -> ~0) | 0 | 0 | |
| Hit chance of discorded mob | BaseWeapon.cs:1334-1348, 1358-1363 | defender bonus = DCI - effect, theirValue = (def+20)*(100+bonus); chance = our/(their*2), min 0.02 | defender loses 28 DCI (mob hits MORE) | effect 100 vs 0-DCI defender: theirValue = 0 -> chance = +Infinity -> always hits | theirValue < 0 -> chance < 0 -> 2% floor | 2% | |
| Swing speed of discorded mob (SE/ML branch) | BaseWeapon.cs:1405-1450, 1496 | bonus = SSI - effect (no floor); ticks = floor((speed*4 - stam/30) * 100/(100+bonus)); min 5 ticks | x1.39 slower | 100/(100-100) = +Infinity -> TimeSpan.FromSeconds(+Inf) throws OverflowException | factor negative -> ticks < 5 -> clamped to 5 = 1.25 s, FASTEST swing | 1.25 s fastest | |
| Maintain range | Discordance.cs:60-66 | 8 + S/15 | 16 | 28 | 41 | 74 | |
| Target range | Discordance.cs:123-127 | 8 + S/15 | 16 | 28 | 41 | 74 | |

- At 300 (live): any non-boss creature is discorded with certainty to 0 skills, -100 all resists, 0 melee
  damage. Worse, effect exactly 100 hits two division-by-zero points: swing-delay ticks become +Infinity and
  TimeSpan.FromSeconds(+Inf) throws (crash/exception risk in the combat timer; unverified whether caught), and
  hit chance vs a 0-DCI defender becomes +Infinity (auto-hit). Players reach exactly 300.0 today.
- Above 300 the signs flip: discorded mobs swing at the 1.25 s cap and their hit chance drops to the 2% floor;
  their skills go negative; incoming damage is multiplied up to x4.2 (no min resist on creatures).
- Also note the hit-chance read uses GetEffect(attacker) to reduce the DEFENDER's DCI (BaseWeapon.cs:1336-1340),
  i.e. a discorded attacker hits more often at low skill (inherited RunUO behavior; looks like a bug).
- BREAKS at 300 / 500 / 1000 (immunity, negative values, divide by zero, runaway damage taken).
- recommendation: hard-cap |effect| at 28 (OSI value at 120) or soft-cap e.g. 28 + 10*ln(1+(S-120)/60) with an
  absolute max ~40; clamp scalar so skills never go below 0; floor (100+bonus) at e.g. 10 in swing speed and
  hit chance; give >120 new effects (longer maintain time after leaving range, or small extra effects) instead.

#### Tracking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Track success | Skills/Tracking/Tracking.cs:129 | CheckSkill 0-21.1 | clamps 100% at 21.1 | clamps | clamps | clamps | 21.1 |
| Passive gain | Tracking.cs:163 | CheckSkill 21.1-100 | clamps (no effect) | | | | 100.0 |
| Search range | Tracking.cs:166-168 | 10 + ((int)V/10)*10 | 130 | 310 | 510 | 1010 | n/a |
| Arrow range | Tracking.cs:374 | range*2 | 260 | 620 | 1020 | 2020 | n/a |
| Track players (AOS) | Tracking.cs:304-354 | chance% = 50*(2*T + DH)/(Hid + Stl) (fixed), elf halves T | scales | scales (75% at equal T=DH=Hid=Stl) | scales | scales; vs 120/120 hider: 625% -> always | n/a |
| Stalking bonus (ML) | Tracking.cs:58-71 | min(distance target moved, 10 + T/10) | 22 | 40 | 60 | 110 | |
| -> Backstab | Spells/Ninjitsu/Backstab.cs:20 | x(1 + Nin/360 + stalk/100) | +22% | +40% | +60% | +110% | |
| -> Surprise Attack malus | Spells/Ninjitsu/SurpriseAttack.cs:59 | Nin.Fixed/60 + stalk (no cap) -> defender DCI | ok | Nin300+T300: 90 | Nin500+T500: 143 -> theirValue < 0 -> attacker 2% hit | 277 -> 2% hit | |
| -> Death Strike | Spells/Ninjitsu/DeathStrike.cs:124-133 | capped 60/30 | clamps | clamps | clamps | clamps | |

- Tracking gains only up to 100.0 by use (the 0-21.1 roll is always true past 21.1); everything above 100 must
  come from scrolls/other sources.
- Search range 1010 at 1000: GetMobilesInRangeByDistance over a 2021x2021 area (about half of Felucca's width)
  every 10 s per player: server-cost and near map-wide player location. BREAKS (perf + information) from ~500;
  310 at live 300 is already 2-3 screens.
- Stalking bonus pushes Surprise Attack malus past 100 + DCI: at exactly 100 + DCI the defender value is 0
  (division by zero -> +Infinity -> auto-hit); above it the attacker's own hit chance inverts to 2%. BREAKS at
  500/1000 combined with Ninjitsu (shared with the Ninjitsu auditor).
- recommendation: soft-cap search range (e.g. 10 + min(V,120) + 20*ln(1+(V-120)/100), max ~200); cap stalking
  bonus at 22 (120 value); give >100 new effects (show target direction/health, reveal tracks of hidden).

#### Item Identification

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Identify IIdentifiable | Skills/ItemIdentification.cs:44 | CheckTargetSkill 0-100 -> V/100 | clamps 100% at 100 | clamps | clamps | clamps | 100 |
Cosmetic/gate reads: AnimalFormRestrictedSkills (PlayerMobile.cs:261), ClusterFGuildSystem.cs:221,251 (dummy 0.0 gate).
recommendation: let it clamp; optional new effect past 100 (e.g. reveal hidden item properties/durability).

#### Taste Identification

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Detect poison on food | Skills/TasteID.cs:37 | CheckTargetSkill 0-100 | clamps 100% at 100 | clamps | clamps | clamps | 100 |
No other gameplay reader in pinned (potion enhance uses Alchemy). recommendation: let it clamp; optional new effect
(detect poison strength / trapped containers).

#### Camping

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Light kindling | Items/Skill Items/Camping/Kindling.cs:38 | CheckSkill 0-100 | clamps 100% at 100 | clamps | clamps | clamps | 100 |
Campfire secure (Campfire.cs:18,122) and bedroll logout are not skill based. WanderingHealer teach list cosmetic.
recommendation: let it clamp; new effects possible (faster secure camp, campfire regen buff).

#### Cartography

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Treasure map decode | Items/Maps/TreasureMap.cs:371-417 | min by level: L1 -3, L2 41, L3 51, L4 61, L5/L6 70; CheckSkill(min, min+60) | scales: L5/6 83.3%; L1-L3 100% | clamps 100% all levels | clamps | clamps | 130 (L5/L6) |
| Dig/use gate | TreasureMap.cs:311,385,442,562 | V >= min | clamps at 70 | clamps | clamps | clamps | |
| Craft maps | Engines/Craft/DefCartography.cs:85-88 via shard CraftItem.cs:877-895 | min..max 10-70, 25-85, 35-95, 39.5-99.5 | clamps | clamps | clamps | clamps | 99.5 |
| Local map extent | Items/Maps/LocalMap.cs:18-21 | dist = 64 + 2V | 304 | 664 | 1064 | 2064 | |
| City map extent | Items/Maps/CityMap.cs:19-22 | dist = max(64+4V,200), size clamp 200-400 | 544 | 1264 | 2064 | 4064 | |
| Sea chart extent | Items/Maps/SeaChart.cs:19-22 | dist = max(64+10V,200) | 1264 | 3064 | 5064 | 10064 | |
| World map extent | Items/Maps/WorldMap.cs:21-25 | x20 = 20V, bounds 1344-x20 .. 1472+x20 | 2400 | 6000 | 10000 | 20000 | |

- Map extents grow without bound; display bounds go negative and past the facet edge (world map covers the whole
  facet at V ~182; at 1000 it is 41,000 tiles wide so the facet is ~12% of the image). Cosmetic BREAK (negative
  coords, maps become useless), no gameplay exploit (unverified how the client renders negative bounds).
- Treasure map levels 1-6 only; no level reads Cartography above 130.
- recommendation: clamp map dist at the 100-skill value; give >130 new effects (e.g. decode higher-tier maps,
  chance for bonus chest level, show dig radius).

---------------------------------------------------------------------------------------------------------------

#### BREAKS summary

1. Bard success (Peacemaking target, Provocation, Discordance): bard difficulty caps at 160 (180 with opposing
   slayer instrument); with skill = Musicianship >= 150-167 (or skill >= D+15/D+20 with Mus 100) success is 100%
   vs every creature. Live 300 already guarantees it. No creature is resistible except flag-immune ones and
   Provocation's paragon D>=160 refusal.
2. Area Peacemaking: 100% from 120, range 8+S/15 = 28 tiles at 300, 74 at 1000, every 5 s; resets all
   combatants (players included where harmful allowed).
3. Discordance effect uncapped: at 300 normal creatures get 0 skills, -100 resists, 0 melee damage; effect = 100
   divides by zero in swing speed (+Infinity -> TimeSpan overflow exception) and hit chance (+Infinity);
   above 300 skills go negative, resists to -320 (x4.2 damage taken), swing speed inverts to fastest, hit chance
   inverts to 2%.
4. Fire Horn damage: weightAvg = 3X - 180 for all-equal bard skills; 216-266 PvP / 324-400 PvM at 300,
   846-1044 PvP / 1269-1566 PvM at 1000, AoE every 6 s.
5. Musicianship diff reduction (Mus-100)/2 unbounded: root cause of (1).
6. Animal Lore (with Vet) pet bandage healing 101-174 per 2 s at 300, 329-571 at 1000.
7. Stable slots unbounded: 68 at 300, 278 at 1000.
8. Tracking search range 10 + V rounded: 310 at 300, 1010 at 1000 (server cost, map-wide player tracking);
   stalking bonus 10+T/10 drives Surprise Attack malus past 100 (div-by-zero / 2% inversion) with Ninjitsu.
9. Cartography map extents unbounded (cosmetic, negative bounds).

Gain ceilings: Taming 157.0 (181.0 with 4-owner creatures), Lore 120, Herding 146.1, Musicianship 120,
Peacemaking 120 area / up to 175-195 target (falls as Musicianship rises), Provocation up to 180-200,
Discordance up to 175-195, Tracking 100, ItemID 100, TasteID 100, Camping 100, Cartography 130.

### 2.5 Crafting and gathering skills (Alchemy, Blacksmithy, Fletching, Carpentry, Cooking, Tailoring, Tinkering, Mining, Lumberjacking, Fishing)

Skills: Alchemy, Blacksmithy, Bowcraft/Fletching, Carpentry, Cooking, Tailoring, Tinkering, Mining, Lumberjacking, Fishing.
Pinned paths are relative to D:\UO\ModernUO-pinned\Projects. "ours" = D:\ShatteredLegacy\server\customizations (cust\) or \patches.
Read-only audit. Expansion branches evaluated: AOS/SE/ML/SA (Core.AOS true).

#### 0. Shared mechanics

##### 0.1 Our CraftItem.cs vs pinned CraftItem.cs (full diff done)

cust\CraftItem.cs (1517 lines) REPLACES UOContent/Engines/Craft/Core/CraftItem.cs. `diff -w` shows the math is IDENTICAL to pinned. The only differences:
- m_TypesTable gains 8 extended log/board pairs (ours :71-79).
- ConsumeRes: GetAmount -> GetBestGroupAmount(..., CheckHueGrouping) for UseAllRes (ours :651).
- DevTestingCrystal bypasses: resources (ours :587-590) and skills/success = 1.0 (ours :860-866). Staff/dev only; make sure the crystal can never reach players.
- ClusterFCraftRun (Craft X runs) refusal/after-attempt hooks, no math (ours :921-1013, :1047-1125, :1307-1310, :1325-1386, :1438, :1493).
- Hammer of Hephaestus familiarity + BOD autofill + achievements hooks (ours :1157-1162, :1215-1237). No skill math.

So the formulas below are pinned's, cited at both:
- Success: `chance = minChance + (val - min)/(max - min) * (1 - minChance)` + talisman SuccessBonus. ours :906 / pinned :886. NOT clamped. val = Skills[mainSkill].Value (includes item/HoH mods).
  Only consumers: CheckSkills (`chance > Random`), Craft() gate `chance <= 0`, Enhance `<= 0`, BOD item filters, gump (clamped to 0..1 for display, CraftGumpItem.cs:207,211). So >100% is harmless: it just means "cannot fail".
- Gain call: `from.CheckSkill(craftSkill.SkillToMake, craftSkill.MinSkill, craftSkill.MaxSkill)` for EVERY skill on the recipe, each attempt (ours :893-896 / pinned :875). Gain ceiling per recipe = its MaxSkill. No shard change.
- Exceptional (ours :807-834 / pinned :794): ECA per system:
  - ChanceMinusSixtyToFortyFive (Blacksmithy, Tailoring, Cooking): `chance - clamp(0.60 - (Value-95)*0.03, 0.45, 0.60)` -> offset is 0.45 at Value >= 100.
  - FiftyPercentChanceMinusTenPercent (Fletching): `chance*0.5 - 0.1`.
  - default (Alchemy, Carpentry, Tinkering, Glassblowing, Masonry): `chance - 0.6`.
  - plus talisman ExceptionalBonus if > 0. Not clamped, only compared to Random, so >100% = always exceptional.
- GetChanceAtMin: Alchemy 0, Blacksmithy 0, Fletching 0.5, Carpentry 0.5, Cooking 0, Tailoring 0.5, Tinkering 0 (0.5 for potion keg / faction trap kit), Glassblowing 0 (0.5 HollowPrism), Masonry 0. (Def*.cs:23-47)
- Material (sub-resource) requirement: `Skills[mainSkill].BASE < subResource.RequiredSkill` -> refuse (ours :629 / pinned :616; gump CraftGump.cs:571,589). Materials do NOT change success or exceptional chance in ModernUO; they are a pure Base gate. Item skill mods (HoH +5/+10/+12.5 Value) do not help this gate. Enhance uses VALUE instead (Enhance.cs:349): a Base-290 smith with Reinforced HoH (+10) can Enhance with Celestial but not craft with it (minor inconsistency).
- Maker's mark: exceptional + Base >= 100 (ours :1487). Threshold.
- Exceptional item effects do not read the crafting skill: weapon DI 35 (+ArmsLore/20, capped 50, BaseWeapon.cs:700-711), armor DistributeBonuses(15) + ArmsLore/20 random resist points, UNCAPPED count (BaseArmor.cs:597). So crafting skill past the "always exceptional" point is wasted (clamps). ArmsLore note (not my skill): ArmsLore 300 -> +15 resist points, 1000 -> +50 points on exceptional armor; only the 70 resist cap limits it. ArmsLore gain from crafting CheckSkill(ArmsLore,0,100) (BaseWeapon.cs:709).

##### 0.2 Computed craft chances (success s / exceptional e; display-capped, raw in brackets)

| Item (system, min-max) | 120 | 300 | 500 | 1000 | e reaches 100% at |
|---|---|---|---|---|---|
| Dagger (Smith, -0.4-49.6) | s 241% e 100% | s 601% e 100% | s 1001% e 100% | s 2001% e 100% | 79.7 |
| PlateChest (Smith, 75-125) | s 90% e 45% | s 450% e 100% | s 850% | s 1850% | 147.6 |
| Plate Kabuto (Smith, 90-140) | s 60% e 15% | s 420% e 100% | s 820% | s 1820% | 162.6 |
| Bow (Fletch, 30-70) | s 162% e 71% | s 388% e 100% | 638% | 1262% | 166.1 |
| Yumi (Fletch, 90-130) | s 88% e 34% | s 312% e 100% | 562% | 1188% | 226.1 |
| Shirt (Tailor, 20.7-45.7) | s 249% e 100% | 609% | 1009% | 2009% | 75.8 |
| Gargish cloth chest (Tailor, ours 94-144) | s 76% e 31% | s 256% e 100% | 456% | 956% | 189.1 |
| Scissors (Tinker, 5-55) | s 230% e 100% | 590% | 990% | 1990% | 85.1 |
| Wind chimes (Tinker, 80-130) | s 80% e 20% | s 440% e 100% | 840% | 1840% | 160.1 |
| Quarter staff (Carp, 73.6-98.6) | s 143% e 83% | 503% e 100% | 903% | 1903% | 128.7 |
| Tetsubo (Carp, 80-140.3) | s 83% e 23% | s 232% e 100% | 398% | 813% | 212.7 |
| Bread loaf (Cook, 0-100) | s 120% e 75% | 300% e 100% | 500% | 1000% | 145.1 |
| Green tea (Cook, 80-130) | s 80% e 35% | 440% e 100% | 840% | 1840% | 152.6 |
| Greater heal (Alch, 55-105) | s 130% | 490% | 890% | 1890% | (potions not exceptional) |
| Deadly poison (Alch, 90-140) | s 60% | 420% | 820% | 1820% | - |
| Hollow prism (Glassblowing/Alch, 100-150) | s 70% e 10% | 250% e 100% | 450% | 950% | 210.1 |
| Any extended-ore item (e.g. Celestial PlateChest) | refused below Base 300 (Platinum 100 ... Celestial 300, ClusterFMiningExtension.cs:174-181) | same chances as iron once Base allows | | | |

All of these: clamps (success at item MaxSkill, exceptional at the value in the last column). No craft formula breaks at high skill; the risk is the opposite: everything past ~230 is wasted for crafting proper.

##### 0.3 Harvest mechanics (HarvestSystem.cs)
- Gate and gain: `skillBase >= resource.ReqSkill && CheckSkill(def.Skill, resource.MinSkill, resource.MaxSkill)` (HarvestSystem.cs:142-147). Base for the gate, Value for the roll. Gain ceiling per resource = MaxSkill.
- Amount per harvest is NOT skill-based: ConsumedPerHarvest (Fel amount, human racial x1.1 on 10%) (HarvestSystem.cs:167-194). Jacobs Deepdelver/Worldbreaker pickaxes add +1 ore (cust\JacobsDeepdelverPickaxe.cs:20, JacobsWorldbreakerPickaxe.cs:21-22), not skill-based.
- Vein choice is weight-based, not skill-based; fallback to Iron/Log if Value < primary ReqSkill/MinSkill or 50% vein fallback (HarvestSystem.cs:332-351).
- Bonus resources (gems/amber/pearl) need Base >= ReqSkill (100/80), fixed chance (:209-211). Clamp.
- cust\ClusterFSkillGain.cs wraps all four CheckSkill handlers (3 attempts, 5x amount) but calls the base handler, so the min/max early-outs and therefore every ceiling below are unchanged (ClusterFSkillGain.cs:63-112).

#### 1. Blacksmithy

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft success/exceptional | ours CraftItem.cs:906, :822-830 | see 0.1/0.2 | scales | clamps (all items 100% s/e by 162.6) | clamps | clamps | 140.0 (Plate kabutos, DefBlacksmithy.cs:251-257); ours adds Gargish items <=135 (cust\Engines\Craft\BlacksmithyCraftRegistrations.cs:91-125) |
| Material gate | ours CraftItem.cs:629; ClusterFMiningExtension.cs:174-181 | Base >= 0..99 vanilla, Platinum 100, Toxic 125, Blaze 150, Frost 175, Obsidian 200, Mythril 225, Adamantium 250, Celestial 300 | Platinum only | all | all | all | - |
| BOD turn-in gain | cust\ClusterFSmithBODSystem.cs:240,426, ranges :351-391 | CheckSkill(min,max) per material; exc +10 | scales | scales | no gain | no gain | 350 (Celestial exc 290-350); practically ~295, see BREAKS B3 |
| Commission gain | cust\ClusterFSmithCommissions.cs:616,687, ranges :772-800 | same idea | scales | scales | no gain | no gain | 335 (Celestial exc 300-335) |
| Large BOD roll | ClusterFSmithBODSystem.cs:95 | (Base-40)/300 > Random | 26.7% | 86.7% | 100% (>=340) | 100% | - | see BREAKS B4 |
| Small BOD exceptional | SmallSmithBOD.cs:126 | (Base+80)/200 | 100% (clamps at 120) | clamps | clamps | clamps | - |
| BOD post-Val material | patches\SmallSmithBOD-PostValorite.patch:27-48, patches\LargeSmithBOD.cs:84-110 | 30%/15% roll, then weights 50%..0.195% (Celestial) gated by Base 105..300 | Platinum/Toxic | all tiers possible | same | same | - |
| Commission material | ClusterFSmithCommissions.cs:429-445 | ladder by Base, 70/30 | Toxic/Platinum | 70% Celestial | same | same | - |
| Commission exceptional | ClusterFSmithCommissions.cs:463,511 | (Base-40)/100 | 80% | 100% (clamps at 140) | clamps | clamps | - |
| Enhance break chance | Enhance.cs:186-189, :314-330 | base 20 - (int)(Value-90)/10, + property; 10% fail per property separate | 17 | -1 (break ~0 for low props) | -21 (break 0) | -71 | - | clamps ~300-400 (break 0, 10% fail floor stays) |
| Repair | Repair.cs:41-75, :247 | weaken = 40 + missing - Value/10; difficulty window (d-25,d+25), d<=100 | scales | weaken only if missing > 10 | weaken only if missing > 10..; at 500 only if missing>10 | weaken only if missing > 60 | 125 (fully broken item) |
| HoH upgrade gates | cust\HammerOfHephaestus.cs:1122,1249 | thresholds | - | - | - | - | - |

recommendation: crafting itself clamps harmlessly; give 150-300+ smiths new outputs (extended-ore recipes with MaxSkill spread to 300+), and fix the gain path (B3) before anything else. Repair: floor weaken chance at e.g. 5% so durability stays a sink.

#### 2. Tailoring

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0.5 at min, ECA 45-60 | scales | clamps (100% s/e by 189.1) | clamps | clamps | 144.0 (ours Gargish cloth chest, cust\Engines\Craft\TailoringCraftRegistrations.cs:91-98); pinned max 121 (BoneChest, DefTailoring.cs:651) |
| Leather material gate | DefTailoring.cs:662-665 | Base >= 0/65/80/99 | all | all | all | all | - |
| ArcaneGem charges | Items/Misc/ArcaneGem.cs:35 | clamp(Value/5, 16, 24) | 24 | clamps at 120 | clamps | clamps | - |
| Tailor BOD exceptional/material | SmallTailorBOD.cs:72+ (unmodified) | like smith | clamps | clamps | clamps | clamps | (pinned BOD reward, no gain call) |
| Repair (cloth) | Repair.cs:391-434 | as smith | | | | | 125 |

recommendation: let it scale (harmless); add 150-300 content (recipes, extended leathers) or gains stop at 144.

#### 3. Tinkering

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0 at min, -0.6 | scales | clamps (by 160.1) | clamps | clamps | 130.0 (WindChimes, DefTinkering.cs:363); ours <=125 (TinkeringCraftRegistrations.cs:79-107) |
| Trap craft level | DefTinkering.cs:663-668 | level = (int)(Value/10); TrapPower = level*9 | L12, P108 | L30, P270 | L50, P450 | L100, P900 | - |
| Explosion trap dmg | TrappableContainer.ExecuteTrap.cs:63-72 | Random(10,30)*level, 100% fire | 120-360 | 300-900 | 500-1500 | 1000-3000 | BREAKS (B5) |
| Dart trap dmg | ExecuteTrap.cs:104-106 | Random(5,15)*level, physical | 60-180 | 150-450 | 250-750 | 500-1500 | BREAKS |
| Poison trap | ExecuteTrap.cs:128 | Poison level min(4, level-1) | Lethal | clamps at 50 | clamps | clamps | - |
| Remove Trap vs our trap | Skills/RemoveTrap.cs:61 | CheckTargetSkill(RemoveTrap, P, P+30) | needs RT 108 | needs RT 270 | needs RT 450 | needs RT 900 (untrappable) | - |
| Lockable container | Items/Containers/LockableContainer.cs:30-37 | level=0.8*Value; lock/req min(..., 95) | clamps ~136 | clamps | clamps | clamps | - |
| Golem repair | Repair.cs:183-203 | heal min(dmg, Value*0.3)+30 | 66 | 120 | 180 | 330 (limited by golem max hits) | 100 (CheckSkill 0-100) |
| Clockwork golem scalar | Items/Misc/ClockworkAssembly.cs:53-71 | step to 1.0 at 100 | clamps | clamps | clamps | clamps | - |
| Faction trap removal | RemoveTrap.cs:96-97 | CheckTargetSkill(Tinkering,80,100) | - | - | - | - | 100 |
| Weapon engraving | WeaponEngravingTool.cs:148 | Value/100 | 100% | clamps | | | - |

recommendation: cap trap level at 10 (vanilla GM) or soft-cap `level = 10 + sqrt(Value-100)/2`; then let craft scale and add new tinker content past 130.

#### 4. Carpentry (incl. Masonry, which uses Carpentry)

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0.5 at min, -0.6 | scales | clamps (by 212.7) | clamps | clamps | 140.3 (Tetsubo, DefCarpentry.cs:322); Masonry 132 (DefMasonry.cs:107-110); ours <=128.9 (CarpentryCraftRegistrations.cs:57) |
| Wood material gate | DefCarpentry.cs:601-607; ClusterFLumberjackingExtension.cs:274-281 | vanilla 0-100; ALL 8 extended boards = 100.0 | all | all | all | all | - |
| Extended wood properties | cust\ResourceInfo.cs (Ironwood..Starwood CraftAttributeInfo empty) | none | - | - | - | - | - |
| Log->board | Items/Skill Items/Lumberjack/Log.cs:92-93 | Carpentry or LJ Value >= wood req | threshold | | | | - |
| Taxidermy / Masonry book | TaxidermyKit.cs:39,88; MasonryBook.cs:24 | Base thresholds 90/100 | - | | | | - |

recommendation: harmless; spread extended board gates 100..300 and give them attributes if Carpentry is meant to grow past 140.

#### 5. Bowcraft/Fletching

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906, :824 | 0.5 at min, e = 0.5*s - 0.1 | scales | clamps (by 226.1) | clamps | clamps | 130.0 (Yumi / RepeatingCrossbow, DefBowFletching.cs:123,128) |
| Wood gate | ClusterFLumberjackingExtension.cs:302-309 | all extended logs 100.0 | all | all | all | all | - |
| JukaBow modify | Items/Weapons/Ranged/JukaBow.cs:35,62 | Base >= 100 | threshold | | | | - |

recommendation: same as Carpentry.

#### 6. Cooking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0 at min, ECA 45-60 | scales | clamps (by 152.6) | clamps | clamps | 130.0 (GreenTea, DefCooking.cs:143); WhiteChocolate 127.5 |
| Other reads | none in pinned or ours (grep) | - | | | | | - |

recommendation: harmless; no content past 130.

#### 7. Alchemy (incl. Glassblowing)

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft success | ours CraftItem.cs:906 | 0 at min | scales | clamps | clamps | clamps | 140.0 potions (DeadlyPoison, DefAlchemy.cs:194-199); 150.0 Glassblowing HollowPrism (DefGlassblowing.cs:123) |
| EnhancePotions skill part | Items/Skill Items/Magical/Potions/BasePotion.cs:207-218 | EP = item EP (cap 50) + (int)(Value*10/33), UNCAPPED | +36% | +90% | +151% | +303% | - |
| Greater Heal | Heal Potions/BaseHealPotion.cs:19-20, GreaterHealPotion.cs:13-14 | 20-25 * (1+EP) | 27-34 | 38-47 | 50-62 | 80-100 (90-113 w/ 50 EP), every 10 s | scales to 500; strong at 1000 |
| Greater Explosion (direct) | Explosion Potions/BaseExplosionPotion.cs:151-155, :180-189 | Scale(20..40) + Value/5 fire | 51-78 | 98-136 | 150-200 | 280-361 (70 fire resist: 84-108) | BREAKS at 500/1000, strong at 300 |
| Greater Conflagration tick | Conflagration Potions/BaseConflagrationPotion.cs:237-241, :258,:312 | (4..8 + F/125 + F/250) * (1+EP), F = Value*10; per second, 10 s field, 30 s reuse | 23-28/s | 76-83/s | 160-170/s | 499-515/s (70 resist: ~150/s) | BREAKS at 300+ |
| Cure chance | Cure Potions/BaseCurePotion.cs:39 | base chance * (1+EP) | Deadly 0.75->100% at ~112 | Lethal 0.25 -> 47% (60% w/ EP 50) | 63% | 100% lethal cure (~990) | clamps then trivialises lethal |
| Str/Agi offset | Strength/Agility potions :25, BasePotion.cs:242 | 20 * (1+EP) and duration *(1+EP) | +27 | +38 | +50 | +80 STR/DEX, 4x duration | soft-cap |
| Refresh | Refresh Potions/BaseRefreshPotion.cs:32 | Scale(Refresh*StamMax) | clamps at StamMax | | | | - |
| Glassblowing gate | DefGlassblowing.cs:38 | Base >= 100 + book | threshold | | | | - |
| InfusedAlchemistsGem | cust\Items\Artifacts\Consumables\InfusedAlchemistsGem.cs:28 | Skills.Alchemy.Base += 1, no cap check (Skill.BaseFixedPoint clamps only at 6553.5, Server/Skills.cs:179) | - | - | - | - | BREAKS (B7): bypasses individual cap and total cap |

recommendation: soft-cap the skill part of EnhancePotions: e.g. `skillEP = 30 * (1 - exp(-(Value)/100)) * ...` or simply `min(Value,120)*10/33` plus diminishing `sqrt(Value-120)`; cap explosion alchemyBonus and conflag bonus at their 120 values; then give alchemists new effects (potion duration, new potion types) past 120.

#### 8. Mining

Our patches\Mining.cs replaces pinned Engines/Harvest/Mining.cs; diff = only `partial` (adds hooks in cust\ClusterFMiningExtension.cs and cust\CompactOreSatchelRoutingHook.cs:51). Resource table identical to pinned (patches\Mining.cs:113-188).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Ore harvest (vanilla) | patches\Mining.cs:115-187 | Iron (0,0,100) ... Valorite (99,59,139): chance (V-min)/(max-min) | Iron 100%, Valorite 76% | 100% all | clamps | clamps | 139 |
| Ore harvest (extended) | cust\ClusterFMiningExtension.cs:84-94 | all ReqSkill 100 (Base); Platinum (65,140) ... Celestial (80,155) | Plat 73%, Celestial 53% | 100% | clamps | clamps | 155.0 (Celestial) |
| Vein weights | ClusterFMiningExtension.cs:108-118 | 8..1 of 1036, not skill-based; RandomizeVeins=false (:131) | - | - | - | - | - |
| Sand | patches\Mining.cs:252-255, :334-336 | ReqSkill 100 Base + SandMining; (70, 400) | 15% | 70% | 100% | 100% | 400.0 |
| Stone (granite) | patches\Mining.cs:284-288 | Base >= 100, 10% | threshold | | | | - |
| Smelt ore (pinned) | Items/Resources/Blacksmithing/Ore.cs:176-205 | diff+-25; vanilla 65..99; EXTENDED ores fall to default 50 -> (25,75), no skill gate (diff>50 check fails) | trivial | | | | 124 (Valorite) |
| Satchel smelt | cust\ReinforcedOreSatchel.cs:126-146 | Value >= difficulty, guaranteed, no gain | threshold | | | | none |
| Guild salvage resmelt | cust\SmithGuildSalvageBag.cs:145-148 | ingots = ((4+Value)*N - 4)*0.0068, NO 100 cap (pinned SalvageBag.cs:94-98 caps at 100) | 21 of 25 (84%) | 51 of 25 (206%) | 85 of 25 | 170 of 25 | BREAKS (B1) |
| Guild salvage difficulty | SmithGuildSalvageBag.cs:60-76,154 | Platinum 105 ... Celestial 300 | | | | | - |
| Treasure dig range | Items/Maps/TreasureMap.cs:585-593 | 4 at >=100 | clamps | | | | - |
| Jacobs pickaxes | cust\Jacobs*Pickaxe.cs (SkillBonuses +5..+25 Mining Value; upgrade gates 75/80/90/100 Value) | Value-only, so they raise roll chance but not Base gates | - | | | | - |
| Pinned salvage bag | Items/Containers/SalvageBag.cs:94-100 | capped 100 | clamps | | | | - |

recommendation: restore `Math.Min(Value,100)` (or a gentle cap that never exceeds ~95% return) in SmithGuildSalvageBag; give extended ores real smelt difficulties (e.g. 100..300 matching the ingot gates) in Ore.cs or a BaseOre override; past 155, give miners something (yield, rare-vein find chance) if Mining is to scale.

#### 9. Lumberjacking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Log harvest (vanilla) | Engines/Harvest/Lumberjacking.cs:71-77 | Log (0,0,100) ... Frostwood (100,60,140) | Frostwood 75% | 100% | clamps | clamps | 140 |
| Log harvest (extended) | cust\ClusterFLumberjackingExtension.cs:219-229 | ReqSkill 100; Ironwood (60,140) ... Starwood (68,148) | Starwood 65% | 100% | clamps | clamps | 148.0 |
| Discovery gate | ClusterFLumberjackingExtension.cs Give() | unreported extended log -> regular Log | - | | | | - |
| Amount | Lumberjacking.cs:53-54 | 10 (20 Fel), not skill | - | | | | - |
| Axe damage (AOS) | Items/Weapons/BaseWeapon.cs:2559-2561, :2599-2602 | lumberBonus = Value*0.2% + 10% at >=100; NOT inside the 100% DI cap ("No caps apply") | +34% | +70% | +110% | +210% | BREAKS (B2) |
| Axe passive gain | BaseWeapon.cs:2545-2549 | CheckSkill(LJ, 0, 100) | no gain | | | | 100 |
| Log->board | Log.cs:92-93 | threshold | | | | | - |

recommendation: soft-cap the axe bonus at its GM value (30%) or `30 + 10*ln(1 + (Value-100)/100)`; give extended logs attributes or spread their gates 100..300 if LJ is meant to grow.

#### 10. Fishing

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Fish harvest | Engines/Harvest/Fishing.cs:100 | Fish (0,0,100) | 100% | 100% | 100% | 100% | 100.0 (only gain source) |
| Deep-water rares (net, big fish, T-map, MIB) | Fishing.cs:15-18, :181-185 | each (Value-80)/4000, checked in order; ReqSkill Base 80/80/90/100 | 1% each, ~3.9% total | 5.5% each, ~20% of casts | 10.5% each, ~36% | 23% each, ~65% of casts | BREAKS economy at 1000 (B6) |
| Serpent spawn | Fishing.cs:324-366 | every net/map/MIB spawns a sea serpent (25% deep sea) | ~3% casts | ~15% | ~26% | ~47% | - |
| Magic fish | Fishing.cs:19-28 | (V-125)/(-2375) | 0.2% | 0 (clamps at 125) | 0 | 0 | - |
| Shoes | Fishing.cs:29 | (V-105)/(-525) | 0 | 0 | 0 | 0 | - |
| Null catch (fail) | Fishing.cs:30 | (V-200)/(-400) | 20% | 0 | 0 | 0 | - |
| White pearl | Fishing.cs:115-116 | Base >= 80, 0.6% | clamps | | | | - |
| T-map level | Fishing.cs:215-228 | always level 1 (0 on Haven young) | - | | | | - |
| SOS chest level | Fishing.cs:304 | min(4, sos.Level) | - | | | | - |
| Aquarium net | Items/Aquarium/AquariumFishingNet.cs:77-84 | Value/100 chance, species max Value/5 cap 20 | clamps at 100 | | | | - |

recommendation: Fishing cannot be gained past 100 at all today; if it should, add a resource with MaxSkill > 100. Cap the four rare mutate chances at their ~150 values (or diminishing returns) before 1000 is allowed.

#### 11. BREAKS findings

- B1 SmithGuildSalvageBag ingot dupe (Mining): cust\SmithGuildSalvageBag.cs:145-148 removed pinned's `if (mining > 100) mining = 100` (pinned Items/Containers/SalvageBag.cs:94-98). For a 25-ingot item: 21 ingots at 120, 25 (100%) at 147.1, 51 at 300 (LIVE), 85 at 500, 170 at 1000. Craft iron plate (Smith >= 125 = 100% success) -> salvage -> net +26 iron per cycle at 300, plus guild seals per item. Works for every extended metal too once gates are met.
- B2 Lumberjacking axe damage: BaseWeapon.cs:2559-2561 adds Value*0.2% (+10% at GM) to totalBonus outside the 100% DI cap: +70% at 300 (live), +110% at 500, +210% at 1000.
- B3 Blacksmithy progression wall (gains): crafting gains stop at 140; above that only BOD/commission turn-ins gain. Adamantium windows top out at 285 (commission exc) / 295 (BOD exc, but a post-Val Adamantium BOD is 0.3*0.78% = 0.23% of BODs). Celestial windows (280-350 BOD, 290-335 commission) are only offered at Base >= 300 (patches\SmallSmithBOD-PostValorite.patch:40-44, ClusterFSmithCommissions.cs:445) and Celestial needs Base 300 to craft (ClusterFMiningExtension.cs:181). So Base 295-300 has no gain source and Celestial crafting is unreachable by play. HoH Value mods make it worse (window max is checked against Value). Also Celestial BOD odds 0.06%.
- B4 Large BOD lock-out: ClusterFSmithBODSystem.cs:95 `(Base-40)/300` -> 86.7% at 300, 100% at >=340. When the 1-large cap is reached (:98-104) the request returns null instead of falling back to a small BOD, so at 300 87% of requests are refused, and at >=340 every request is refused until the large is done.
- B5 Tinker traps: DefTinkering.cs:663-668 trap level = Value/10 uncapped. Explosion trap 300-900 fire at 300, 1000-3000 at 1000; dart 150-450 at 300; TrapPower 270/900 needs Remove Trap 270/900 to disarm (RemoveTrap.cs:61). Already 120-360 at 120 (vanilla GM 100-300).
- B6 Fishing rares at high skill: (Value-80)/4000 per rare; at 1000 ~65% of deep-water casts are net/big fish/map/MIB and ~47% spawn a serpent. Not reachable today (Fishing gain ceiling 100) but breaks once 1000 is granted.
- B7 InfusedAlchemistsGem: Base += 1 with no cap check (cust\...\InfusedAlchemistsGem.cs:28); can push Alchemy past the 300 individual cap and the total cap. Severity depends on drop rate (unverified).
- B8 Alchemy potion power: EnhancePotions skill part uncapped (BasePotion.cs:210). Greater Conflagration 76-83 fire/s at 300 (vanilla ~20-26), 499-515/s at 1000; Greater Explosion 98-136 at 300, 280-361 at 1000; Greater Cure becomes a guaranteed lethal cure near 1000.

Design gaps (not "breaks" by the formula test, but they matter):
- Extended ore smelting has no skill gate: Ore.cs:176-186 default difficulty 50 -> any Mining >= 25 smelts Celestial ore (only the guild bag and satchel gate it).
- Extended woods all gate at 100 with empty CraftAttributeInfo (cust\ResourceInfo.cs extended lumber block), so they give nothing past 100 to Carpentry/Fletching.
- Material gate uses Base, Enhance gate uses Value (Enhance.cs:349 vs ours CraftItem.cs:629).
- Repair weaken chance reaches 0 for normal damage past ~400 (Repair.cs:41-42): durability sink disappears.
- The ore "0-300" ladder only exists on the smithing side (ingot gates 100-300); the mining side tops at 155 (harvest) and the design doc (D:\ShatteredLegacy\design\systems\extended_resources.md) specifies tiers and facets, not skill numbers.

#### 12. Gain ceilings (summary)

| Skill | Gain ceiling (highest MaxSkill) | Source | Notes |
|---|---|---|---|
| Alchemy | 150.0 | Glassblowing HollowPrism (DefGlassblowing.cs:123); potions 140 | nothing past 150; gem bypass B7 |
| Blacksmithy | 140 craft; 335 commission; 350 BOD | DefBlacksmithy.cs:251-257; ClusterFSmithCommissions.cs:797; ClusterFSmithBODSystem.cs:381 | practically ~295, dead zone to 300 (B3); repair 125 |
| Fletching | 130.0 | DefBowFletching.cs:123,128 | |
| Carpentry | 140.3 | DefCarpentry.cs:322 (Masonry 132) | |
| Cooking | 130.0 | DefCooking.cs:143 | |
| Tailoring | 144.0 | ours TailoringCraftRegistrations.cs:93 | pinned only 121 |
| Tinkering | 130.0 | DefTinkering.cs:363 | golem repair 100 |
| Mining | 400.0 (sand); 155 ore; 124 smelt | patches\Mining.cs:254; ClusterFMiningExtension.cs:93; Ore.cs:189-190 | sand needs Base 100 + SandMining book |
| Lumberjacking | 148.0 | ClusterFLumberjackingExtension.cs:228 | axe combat 100 |
| Fishing | 100.0 | Fishing.cs:100 | no gain past GM at all |

Unverified: Magic Untrap spell interaction with TrapPower 270-900; InfusedAlchemistsGem drop sources; whether any other gain source (scrolls) exists outside these files (grep for Transcendence/Alacrity in customizations found only a boss file, not checked).

---

## 3. Gains past 120

### 3.1 The formula (pinned) and our overrides

Pinned `UOContent/Skills/SkillCheck.cs`:

- A ranged check `CheckSkill(skill, min, max)` returns false with no gain roll when value < min, and
  **returns true with no gain roll when value >= max** (`:53-61` location, `:161-169` target).
  A direct-chance check returns true with no gain roll when chance >= 1.0 (`:84-87`, `:190-193`).
- Otherwise `CheckSkill` (`:94-145`): below 10.0 base every use gains (`:106-109`). Above it, if the
  region and the anti-macro check allow (`:104`, `:110`, `:198-206`):

      gc = ( (Skills.Cap - Skills.Total) / Skills.Cap  +  (skill.Cap - skill.Base) / skill.Cap ) / 2   (:112-114)
      gc = ( gc + (1 - chance) * (success ? 0.5 : 0.0) ) / 2                                          (:116-117, AOS)
      gc = gc * GainFactor, floor 0.01                                                                  (:119-124)

  Call the two halves A (total-cap headroom) and B (this skill's headroom). Both are **fractions of
  the cap**, so the formula has no absolute scale: a skill at 150 of cap 300 rolls exactly what a skill
  at 500 of cap 1000 rolls.
- `Gain` (`:208-254`) adds 1 fixed point (0.1) (1-4 below 10.0), clamped to `CapFixedPoint`
  (`:252`), and only while `Skills.Total < Skills.Cap` for players (`:250`).
- `GainFactor` is 1 for all 58 skills (`Distribution/Data/skills.json`, 58 entries counted, all `1`).
- Anti-macro is **off** by default (`AntiMacroSystem.cs:97`). Live value not checked (the live
  `Configuration/antimacro.json` is inside the container); unverified.

Ours, on top (`server\customizations\ClusterFSkillGain.cs`, live defaults):

- **3 gain rolls per use** (`chanceAttempts` 3, `:8`, `:97-112`): the base handler is re-run up to two
  more times while the skill is Up and below cap; only the first result counts for success.
- **5x amount per gain** (`amountMultiplier` 5, `:9`, `:127-139`): each gain calls `SkillCheck.Gain`
  four more times, so one gain is 0.5 points, not 0.1.
- `ClusterFSkillCaps.cs:82-89`: "unlimited" total means `Skills.Cap = 58 x individual cap` (17,400.0 at
  300). This keeps term A near 1 for any real character. **In OSI, A is the main brake** (it falls to 0
  as Total nears 700); here it never brakes.
- `TestCenterSkillGain.cs` multiplies GainFactor on a Test Center shard only.
- `customizations\Meditation.cs:92` passes the skill's own cap as maxSkill, so Meditation never hits
  the "no challenge" ceiling.

### 3.2 How the chance behaves toward 300, 500 and 1000

It does **not** stall and it **cannot go negative** (B >= 0 because `Gain` never passes the cap,
and the floor is 0.01). With A near 1, the lowest it reaches is about 0.24 per roll at the cap
itself. What stops gains past 120 is not the formula but **the gain ceiling**: every pinned use
with a fixed `maxSkill` below the player's value returns "no challenge" and never rolls. Section 2
lists each skill's ceiling. So the real question per skill is whether any use still has a
`maxSkill` (or a direct chance below 1.0) above 120.

### 3.3 Phase 4F's "natural gain slowdown past 200 is sufficient"

**False.** The formula is relative to the cap, so there is no slowdown that starts at 200. With a
cap of 500, a skill at 200 rolls B = 0.6, the same as 120 of 300 today. The two things that do slow a
player past 200 are (a) the gain ceilings, which stop gains entirely rather than slowing them, and (b)
the point count, which grows linearly with the cap (1000 points of skill is 2,000 gain events at 0.5
each). Neither is a tuning dial.

### 3.4 Estimated gain per use

Model: `notes\cc-P20-scratch\gain_model.py` (a direct transcription of `SkillCheck.cs:112-124` plus
ClusterFSkillGain). Assumptions: AOS rules, GainFactor 1, anti-macro off, a character with 7 skills at
the stated value (sets Total), an "easy" use the player succeeds at 90 percent of the time and a "hard"
use at 50 percent, **and a use whose maxSkill is above the player's value** (otherwise the answer is 0).
"gc" is the chance per roll; "pts/use" is expected skill points per use with 3 rolls and 0.5 per gain.

Live today, cap 300 (total cap 17,400):

| skill | A | B | gc easy | gc hard | pts/use easy | pts/use hard |
|---|---|---|---|---|---|---|
| 50 | 0.980 | 0.833 | 0.476 | 0.516 | 0.714 | 0.774 |
| 100 | 0.960 | 0.667 | 0.429 | 0.469 | 0.644 | 0.704 |
| 120 | 0.952 | 0.600 | 0.410 | 0.450 | 0.616 | 0.676 |
| 200 | 0.920 | 0.333 | 0.336 | 0.376 | 0.504 | 0.564 |
| 300 | 0.879 | 0.000 | 0.242 | 0.282 | 0.363 | 0.423 |

Cap 1000 (total cap 58,000):

| skill | A | B | gc easy | gc hard | pts/use easy | pts/use hard |
|---|---|---|---|---|---|---|
| 50 | 0.994 | 0.950 | 0.508 | 0.548 | 0.763 | 0.823 |
| 100 | 0.988 | 0.900 | 0.494 | 0.534 | 0.742 | 0.802 |
| 120 | 0.986 | 0.880 | 0.489 | 0.529 | 0.733 | 0.793 |
| 200 | 0.976 | 0.800 | 0.466 | 0.506 | 0.700 | 0.760 |
| 300 | 0.964 | 0.700 | 0.438 | 0.478 | 0.658 | 0.718 |
| 500 | 0.940 | 0.500 | 0.382 | 0.422 | 0.574 | 0.634 |
| 1000 | 0.879 | 0.000 | 0.242 | 0.282 | 0.363 | 0.423 |

For comparison, OSI rules (total cap 700, no ClusterF boost, 7 skills): gc hard 0.31 at 50, 0.11 at
90, 0.07 at 100, with 0.1 points per gain. **At 300 our rate per use is about 60 times OSI's at 100.**

Uses to climb from 0 to the cap, if a use at that success rate always exists: cap 50: 82-92; cap 100:
164-183; cap 300: 492-549; cap 500: 820-914; **cap 1000: 1,640-1,828 uses**. At one use every 5
seconds that is about 2.5 hours per skill to 1000.

So with today's gain settings, **skill gain is not what paces the loop system: the level cap is.** A
player will sit at each loop's skill cap long before the next loop, unless gains are slowed. That is
fine if intended (the cap is the gate) but it means the 50 -> 1000 skill journey is decided almost
entirely by the XP curve in section 6 and by whether content exists above each gain ceiling.

Recommendation: keep pinned's formula, but (1) make the total cap a real number per loop or apply a
per-loop gain divisor if gains should take time, and (2) give each skill at least one use whose
`maxSkill` follows the skill's cap (as `Meditation.cs:92` already does), or the skill cannot move past
its ceiling at all.


---

## 4. Power scrolls (sub-agent report, cited)

Read-only research, 2026-09-30. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects`.
Shard paths: `customizations\...` and `patches\...` are under `D:\ShatteredLegacy\server`.

### 4.1 How pinned defines the scrolls

#### SpecialScroll (base)
`UOContent/Items/Special/Special Scrolls/SpecialScroll.cs`
- `:7-18` abstract, `[SerializationGenerator(0, false)]`, two serialized fields: `Skill` (SkillName) and
  `Value` (double). No version beyond 0.
- `:22` LootType.Cursed by default.
- `:49-63` `CanUse`: only checks Deleted and "in your backpack".
- `:69-77` double click -> `CanUse` -> confirmation gump; `:133-139` Yes button -> `Use(from)`.
- `Use` is virtual and empty (`:65-67`); subclasses do all the work.

#### PowerScroll
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

#### StatCapScroll (TypeAlias "Server.Items.StatScroll")
`UOContent/Items/Special/Special Scrolls/StatCapScroll.cs`
- `:12` ctor, default 230; Skill field unused (Alchemy). Titles/names for 230/235/240/245/250
  (+5..+25 over 225) at `:23-83`.
- `:85-106` CanUse: `newValue = Value (+5 if PlayerMobile.HasStatReward)`; **refuses if
  `StatCap >= newValue`** (msg 1049510).
- `:108-124` Use: **`StatCap = Value + 5` if HasStatReward, else `StatCap = Value`** (absolute).
- So stat scrolls raise StatCap to 230..250 (255 with the veteran half-level reward).

#### ScrollofTranscendence (SoT)
`UOContent/Items/Special/Special Scrolls/ScrollofTranscendence.cs`
- `:30-31` `CreateRandom(min,max)` -> random skill (`SkillsInfo.RandomSkill()`), value = `rand/10.0`
  (so 0.1..1.0 points; champion range 1-5 Fel, 6-10 elsewhere).
- `:39-71` CanUse: PlayerMobile only; refuses during an ML skill-gain quest objective or an active
  Alacrity.
- `:73-128` Use: adds Base (not cap). Clamps the add to `Cap - Base` (`:87-89`), needs `Base < Cap` and
  Lock Up (`:92`), and if total would pass SkillsCap it lowers a Down-locked skill (`:94-110`).
  `:128` `Skills[Skill].Base += newValue`. Never touches Cap.

#### ScrollofAlacrity
`UOContent/Items/Special/Special Scrolls/ScrollofAlacrity.cs`
- `:37-69` CanUse: as SoT (quest/alacrity already active).
- `:71-98` Use: refuses if `Base >= Cap` or lock not Up (`:82`); sets `pm.AcceleratedSkill` and
  `AcceleratedStart = now + 15 min`; SkillCheck multiplies gains x2-5 (`UOContent/Skills/SkillCheck.cs`
  ~`:245-248`). No pinned code creates one (no drop site found).

#### Every pinned source that creates scrolls
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

#### Every writer of Skill.Cap / Skills.Cap / StatCap
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

### 4.2 Interaction with ClusterFSkillCaps / ClusterFStatCaps today

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

### 4.3 What the new scroll line ("Legacy Scroll", key to the next loop) must touch

#### Design target (decided 2026-09-30)
Per-skill cap = character's MaxLevel (50, 100, 150 ... up to 500-1000); loops raise MaxLevel; past cap 100
the next loop needs a scroll; lower scrolls merge into higher ones at a League NPC; OSI 105-120 PS fold
into the line. Sources: `roadmap.md` "Legacy Awakening" (`:333`), "Champion Spawn and Mastery Rewrite"
(`:915-943`), "Extended Resources and Mining" (`:457-466`), `feature-queue.md` F-12 (`:763` onward).
Phase 4F (`phase_4_smiths_guild_extended_crafting.md:746-797`, additive +5..+20, cap 500) is superseded.

#### Classes
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

#### Drop sites that create PowerScrolls / stat scrolls today
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

#### League NPC merging
- Shard NPC: `customizations\LeagueRegistrar.cs` / `LeagueRegistrarGump.cs` / `ClusterFLeagueSystem.cs`.
  Add "Fold scrolls": consume K scrolls of tier T (LegacyScroll Value T, or PowerScroll Value 105-120
  mapped to tier 0) from the backpack, give one of tier T+1. Use `Item.Delete()` on consumed scrolls
  and `AddToBackpack` for the result.

#### Existing PowerScroll items in the world
- They are unusable today, so nothing has been lost by holders except the Smith Seal ones (section 2).
- Options: (1) keep them as fold inputs (recommended; no world edit, works with the CanUse patch); or
  (2) a one-time WorldLoad converter that iterates `World.Items.Values`, replaces each PowerScroll /
  StatCapScroll with an equivalent LegacyScroll fragment in the same parent/location, and logs a count
  (pattern: `ClusterFSkillCaps.ApplyToLoadedPlayers` uses `EventSink.WorldLoad`, `:26`, `:91-105`).
- Refund the Smith Seal PS buyers (the 305-320 scrolls were consumed) if any exist in live saves.

#### Where per-player MaxLevel must live
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

#### Minimal ClusterFSkillCaps change
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

### 4.4 What happens when Skill.Cap is lowered below Base (migration of 300-skill characters)

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

---

## 5. Creatures (sub-agent report, cited; CSV and script in notes\cc-P20-scratch\)

Read-only research. Authority: pinned ModernUO (`D:\UO\ModernUO-pinned\Projects`, paths below are relative
to it). Shard creatures from `D:\ShatteredLegacy\server\customizations`. Era: EJ (expansion Id 11 per
AGENTS.md), so Core.LBR, Core.AOS, Core.SE, Core.ML are all true. Shard caps: 300.0 per skill
(customizations\ClusterFSkillCaps.cs:10), 500 per stat / 1500 total (ClusterFStatCaps.cs:10-11). No shard
patch touches the bard skills, BaseInstrument, CheckHit or ScaleDamageAOS (checked patches\ and a grep of
customizations).

Files in this folder:
- `s5_bard_difficulty.py` - the parser/calculator (re-runnable, read-only on sources).
- `s5-creature-difficulty.csv` - 694 rows, one per computed creature, sorted by uncapped difficulty.
- `s5-parse-failures.txt` - 215 classes not computed, with the reason.
- `s5-run-output.txt` - console summary of the last run.

### 5.1 The formula, exactly (UOContent/Items/Skill Items/Musical Instruments/BaseInstrument.cs:250-306)

```
val  = HitsMax * (Core.LBR ? 1.6 : 0.625) + StamMax + ManaMax        (:260)
val += SkillsTotal / 10.0                                              (:262)
if val > 700: val = 700 + (int)((val - 700) * 3/11)                    (:264-267, soft cap)
+100 if IsMageryCreature:  AI == AI_Mage && Skills.Magery.Base > 5.0   (:242, :271)
+100 if IsFireBreathingCreature: GetAbility(MonsterAbilityType.FireBreath) != null   (:244, :276)
+100 if PoisonImmune != null                                           (:246, :281)
+100 if VampireBat or VampireBatFamiliar                               (:286)
+ (HitPoison.Level + 1) * 20   (no HitPoison -> 0)                     (:248, :291)
val /= 10                                                              (:293)
+40 if IsParagon                                                       (:295-298)
cap 160 if Core.SE                                                     (:300-303)
```

Inputs, as pinned computes them:
- `HitsMax` (Mobiles/BaseCreature.cs:579-580): `HitsMaxSeed <= 0 ? Str : HitsMaxSeed + StatOffset(Str)`.
  `SetHits` writes HitsMaxSeed (BaseCreature.cs:4599-4620); the pre-AOS x100/60 rescale (:4601, :4612) is
  off in EJ. With no SetHits, a creature's HitsMax is its Str (not 50 + Str/2, which is Mobile.cs:2051 and
  is overridden).
- `StamMax` / `ManaMax` (BaseCreature.cs:586-594): seed from SetStam/SetMana, else Dex / Int.
- `SkillsTotal` (Server/Mobiles/Mobile.cs:477) = `Skills.Total`, the sum of BaseFixedPoint (Server/Skills.cs:513,
  :836), i.e. tenths; `/10.0` makes it skill points. So a creature with 600.0 total skill adds 600.
- Fire breath: any ability whose AbilityType is FireBreath, which includes FireBreath, ChaosBreath,
  ColdBreath and every subclass (Mobiles/Abilities/Fire Breath/*.cs, e.g. Leviathan's nested breath, the
  shard's CrystalHydraBreath). There is no `HasBreath` property anywhere in pinned or customizations.
- Poison levels (Misc/PoisonKinds.cs:80-92): Lesser 0, Regular 1, Greater 2, Deadly 3, Lethal 4, so Lethal
  HitPoison adds 100 raw (10 final).
- Not in the formula (the TODO at :252-255 admits it): aura damage, summoning, life drain, stun, AoE
  specials, weapon abilities, damage output, resistances, attack skill.

Hand check, Dragon: hits 486.5*1.6 + 95.5 + 455.5 + 359.75 skill = 1689 raw -> 700 + int(989*3/11) = 969
-> +100 mage +100 breath = 1169 -> 116.9. Matches the CSV.

### 5.2 Method and approximations

Static parse, no build. The script strips comments/strings from every .cs in pinned UOContent (whole tree,
not just Mobiles, so Engines/ quest and champion creatures are included; the `category` column says where
each lives) and in customizations, finds every class, resolves inheritance to BaseCreature, drops abstract
classes, then for each concrete class walks the chain root-first, applying each class's chosen constructor.

Approximations:
1. Every `SetX(min, max)` uses the midpoint; `SetSkill` midpoint in fixed point (same as RandomMinMax of
   fixed values).
2. Constructor choice: the `[Constructible]` one, else the one with most Set calls; `: this(...)` chains are
   followed inside the class. If a Set call appears more than once (if/else branches) the last one wins
   (7 rows; flagged in `notes`).
3. `Core.X ? a : b` takes `a` (all era flags true). Golem's `scalar` parameter defaults to 1.0.
4. Stat offsets, equipment and buffs ignored (GetStatOffset = 0).
5. AI type: the literal `AIType.AI_x` in the base(...) call or an `AI = ` assignment; classes that pass AI
   as a parameter inherit it, and `ForcedAI` overrides are ignored (8 rows show `param`).
6. Breath/PoisonImmune/HitPoison are textual matches on the class body, inherited down the chain. A
   random HitPoison (`RandomBool() ? Lesser : Regular`) uses the average level.
7. Paragon is not applied to the main value; the `paragon` column is value + 40, capped at 160.
8. The `uncapped` column is the formula without the final 160 cap (so the top end can be ranked); `diff`
   is the in-game value.
9. Combat columns (sec. 6) use the creature's best of Wrestling/Swords/Macing/Fencing/Archery, SetDamage
   midpoint, and Str/Tactics/Anatomy bonuses from ScaleDamageAOS.

Parse failures: 215 classes. 175 are vendors, townsfolk, quest NPCs, talisman summons and the shard's
33 gargoyle vendors, whose stats are set in a base-class virtual (BaseVendor.InitBody etc.), not in the
constructor. About 40 are combat-relevant and were not computed: the 16 Despise power-scaled creatures
and DespiseBoss base (stats come from virtual StrStart/HitsStart properties scaled by power level), MedusaClone,
ShameGuardian, the 6 Meer "Enraged" animals (SetHits(50, Str)), Revenant (skills copied from the target),
4 war horses, Golem-derived summons, Parrot/SeaHorse/HellSteed/SilverSteed/GrizzledMare (stats in a shared
base), Clone (Mirror Image). Full list with reasons: `s5-parse-failures.txt`.

### 5.3 Results

Computed: 694 creatures (559 pinned, 135 custom). Categories: monster 279, other (Engines/quests/etc) 167,
custom 135, animal 70, npc 24, special (champions, Harrower etc) 14, familiar 5.

In-game difficulty (capped at 160):

| set | n | min | Q1 | median | Q3 | max | at cap 160 |
|---|---|---|---|---|---|---|---|
| all computed | 694 | 3.9 | 42.5 | 76.7 | 103.8 | 160 | 70 |
| combat set (monsters+animals+special+custom) | 498 | 3.9 | 58.4 | 85.0 | 120.0 | 160 | 68 |
| custom only | 135 | 26.0 | 74.8 | 103.6 | 160 | 160 | 34 |

Histogram, combat set (498), buckets of 10 on the in-game value:

```
  0- 9  14  ##############
 10-19  14  ##############
 20-29  26  ##########################
 30-39  22  ######################
 40-49  28  ############################
 50-59  25  #########################
 60-69  39  #######################################
 70-79  50  ##################################################
 80-89  58  ##########################################################
 90-99  40  ########################################
100-109 37  #####################################
110-119 21  #####################
120-129 18  ##################
130-139  8  ########
140-149 19  ###################
150-159 11  ###########
  =160  68  ####################################################################
```

Uncapped spread of the same set in buckets of 20: 0-19: 28, 20-39: 48, 40-59: 53, 60-79: 89, 80-99: 98,
100-119: 58, 120-139: 26, 140-159: 30, 160-179: 14, 180-199: 8, 200+: 46. The pile at 160 is real: 68
creatures (34 of them the shard's own) are indistinguishable to the bard formula. With the paragon +40,
112 of the combat set reach 160.

Top 20 (uncapped; every one is 160 in game):

| # | creature | src | uncapped | HitsMax | notes |
|---|---|---|---|---|---|
| 1 | AdrianTheGloriousLord | custom | 3317.6 | 60000 | mage |
| 2 | AndrosTheDreadLord | custom | 3317.6 | 60000 | mage |
| 3 | SlasherOfVeils | custom | 2876.2 | 57500 | mage |
| 4 | Medusa | custom | 2740.2 | 60000 | mage, poison immune, Deadly-or-Lethal HitPoison, BardImmune |
| 5 | RakktaviRenowned | custom | 2257.5 | 50000 | |
| 6 | TikitaviRenowned | custom | 2249.2 | 50000 | |
| 7 | VitaviRenowned | custom | 2160.1 | 47500 | mage |
| 8 | DemonKnight | pinned | 1546.6 | 30000 | mage, poison immune |
| 9 | NavreyNightEyes | custom | 1530.4 | 32500 | mage, poison immune, Lethal HitPoison |
| 10 | MinionOfScelestus | custom | 1420.4 | 30000 | mage, poison immune, Lethal HitPoison |
| 11 | StygianDragon | custom | 1400.0 | 30000 | breath |
| 12 | ChaosVortex | custom | 1257.0 | 27000 | poison immune |
| 13 | UnboundEnergyVortex | custom | 951.5 | 20000 | poison immune |
| 14 | Allosaurus | custom | 859.5 | 18000 | |
| 15 | Niporailem | custom | 580.9 | 10250 | |
| 16 | PixieRenowned | custom | 512.6 | 9150 | mage |
| 17 | Ilhenir | pinned | 502.6 | 9000 | mage, poison immune |
| 18 | Serado | pinned | 488.4 | 9000 | poison immune, Lethal HitPoison |
| 19 | EternalGazer | custom | 481.7 | 7425 | mage |
| 20 | Twaulo | pinned | 434.8 | 7500 | poison immune |

The ranking above the cap is almost purely HitsMax: past raw 700 every point counts 3/11, and the 1.6x hits
term dominates, so this is a "how big is the HP bar" list, not a danger list.

Sanity check (in-game values): Rat 6.2 < GiantRat 23.1 < Orc 43.5 < Troll 46.9 < Ogre 49.0 < OrcishLord 65.6
< Daemon 105.1 < Dragon 116.9 < Balron 126.6 < AncientWyrm 152.7 < AncientLich 155.6 < GreaterDragon /
Harrower / Semidar / Leviathan 160. The asked order rat < orc < troll < dragon < ancient wyrm holds. Oddities
the formula produces: Troll is barely above Orc (Orc's dex/skills offset the Troll's hits); WhiteWyrm 107.9 is
below Dragon; GreaterDragon (172.7 uncapped) outranks AncientWyrm.

### 5.4 Danger the formula misses

- Only four ability flags count. Not counted: DrainLife / mass drain (4+1 users), ColossalBlow stun (3),
  PoisonGas / mass poison, DeathExplosion, summon counters (Pixies, Skeletons, Lesser Undead), DestroyEquipment,
  BloodBath, GraspingClaw / RuneCorruption / FanningFire resist debuffs, ReflectPhysicalDamage, MagicalBarrier,
  weapon special moves, auras.
- Scripted boss mechanics in custom code: StygianDragon's crimson meteor (fire), stygian fireball (120-150
  chaos, StygianDragon.cs:438-442), fire column; Medusa (stone gaze, clones; BardImmune); Navrey; Slasher of
  Veils; the Despise bosses; Shame revamped guardians. All score 160 the same as a GreaterDragon.
- Damage output is absent: FierceDragon (Engines/Quests/Haochi's Trials/Mobiles/FierceDragon.cs:15-19, Str
  6000, damage 50-80) scores 160 like the rest but hits for roughly 1290 before resists, about 390 through 70
  resists, more than a 300-skill character's maximum HP. It is a quest creature meant to be fled from.
- Necro or other caster AIs get no mage bonus (only AI_Mage counts, :242), and the paragon bonus is a flat
  +40 although paragons get far more HP and damage.
- Health-pool sponges (the 47500-60000 HP bosses) score the same as a 160 creature with 1/50th the HP.

### 5.5 Bard success for a 300 bard

Peacemaking (Skills/Peacemaking.cs:163-170) and Discordance (Skills/Discordance.cs:154-170):
`diff = GetDifficultyFor - 10 - (Musicianship - 100) * 0.5`, success = CheckTargetSkill(diff - 25, diff + 25),
which is an automatic success once skill >= diff + 25 (Skills/SkillCheck.cs:166-169). Provocation
(Skills/Provocation.cs:131-138, :154): diff = mean of the two targets' difficulties - 5 - the same
musicianship term. The musicianship gate (BaseInstrument.cs:527-532) is `Musicianship / 100 > random`, so it
always passes at 100+.

| bard skill (all bard skills equal) | Peace/Discord vs 160 | Provoke 160 vs 160 |
|---|---|---|
| 100 | diff 150, window 125-175: 0% | 0% |
| 120 | diff 140, window 115-165: 10% | 0% (diff 145, window 120-170) |
| 150 | diff 125, window 100-150: 100% | 90% (diff 130) |
| 154 | 100% | 100% |
| 300 | diff 50, window 25-75: 100% | 100% (diff 55) |

So every creature that is not flagged is a guaranteed peace / provoke / discord from about skill 150-154 up.
At 300 the diff for the hardest target is 50, so even an exceptional-bonus, slayer-penalised instrument
changes nothing. What still blocks a bard: `BardImmune` (38 computed classes, e.g. Medusa, Meraktus,
WyvernRenowned, Revenant, KhaldunRevenant, faction NPCs), explicit `Unprovokable` / `Uncalmable` (15 / 3), and
paragons scoring >= 160, which cannot be provoked (Provocation.cs:66, BaseCreature.cs:3746) and take half
discord (Discordance.cs:190-193).

Discordance magnitude is uncapped above 100 (Discordance.cs:181-193): `effect = -20 + (skill-100)/-2.5`.
At 300 that is -100 to every resist, -100% to every skill (skill mod = Value * -1.0, :239) and, via
ScaleDamageAOS (Items/Weapons/BaseWeapon.cs:2586-2592), -200% damage bonus; halved for 160 targets (-50
resist). Creature resists have no floor (Server/Mobiles/Mobile.cs:3249 GetMinResistance = int.MinValue), so
a discorded dragon at 60 physical sits at -40 and takes 1.4x raw damage instead of 0.4x (3.5x more).
Odd detail worth a look: CheckHit subtracts the attacker's discord effect from the defender's
defense-chance bonus (BaseWeapon.cs:1334-1340, comment says the defender should be the one affected). At
300 discord this drives (100 + DCI - 100) to DCI, so a discorded creature swinging at a 0-DCI defender
gets theirValue 0 and an infinite hit chance. At OSI magnitudes (max 28) this was minor.

### 5.6 Can anything threaten a 300 / 500-stat character?

Player side, from pinned:
- HP: PlayerMobile.HitsMax = Str/2 + 50 + min(BonusHits, 25) (Mobiles/PlayerMobile.cs:548-576): 500 Str ->
  300, 325 with items. HP does not grow with skill.
- Resists capped at 70 (Server/Mobiles/Mobile.cs:431); AOS.Damage takes (100 - resist)% per type
  (Misc/AOS.cs:126-132), so at least 30% of every resisted hit lands.
- Hit chance (AOS, BaseWeapon.cs:1299, :1348, :1358-1363): `chance = (atk+20)(100+HCI) / (2 (def+20)(100+DCI))`,
  floor 2%. Defense skill 300 -> def term 320.
- Player damage (ScaleDamageAOS, BaseWeapon.cs:2556-2602, "No caps apply"): Str 500 +1.55, Anatomy 300 +1.55,
  Tactics 300 +1.94, plus capped DI 100% -> about 7.0x weapon base. Player vs a 120-wrestling creature:
  320/280 > 1, a guaranteed hit.

Creature side (computed for all 694; columns atkskill, dmghit, dmg70, hit_vs300, hit_vs300dci45):
- Highest attack skill is KhaldunRevenant at 145 -> 25.8% to hit a 300 defender (17.8% with 45 DCI). The
  median creature (80) hits 15.6%. Only 4 creatures reach 25%.
- Highest melee per landed hit through 70 resists: StygianDragon 59, WyvernRenowned 57, Navrey 55, Rend 54,
  Putrefier 53. Seven creatures exceed 50; none reaches 100 except the quest FierceDragon (~390).
- Expected melee per swing (hit chance x damage): top is Rend 14, StygianDragon 12.4, Putrefier 11.7,
  Medusa 10.8, GreaterDragon 10.8. Against 325 HP that is about 25+ swings to kill, with no healing.
- Fire breath is capped at 200 (Mobiles/Abilities/Fire Breath/FireBreath.cs:207-216), 30-45 s cooldown:
  about 60 through 70 fire resist.
- Spells: AOS spell damage = dice x (1 + Int/10 % + inscription) x (30 + 9 x EvalInt/100)%
  (Spells/Base/Spell.cs:218-257); MagicResist skill does not reduce AOS damage. A 100-EvalInt, 700-Int
  creature's Flamestrike is about 51 x 1.7 x 1.2 = 104, about 31 after 70 fire resist. Harrower (Int 1100)
  about 38.

Verdict: with a 300 template nothing in pinned or the shard's content threatens the character one on one,
and nothing resists the bard. What can still hurt:
1. Scripted boss specials in custom code that stack with melee and spells (StygianDragon meteor/fireball,
   Medusa, Navrey, Slasher of Veils, Despise bosses, Shame guardians), especially if several fire at once.
2. Numbers: several 150+ creatures, or a champion spawn wave, at 10-14 expected damage per swing each.
3. Lethal HitPoison carriers (Navrey, MinionOfScelestus, Serado, DarknightCreeper) if the player cannot cure.
4. Non-resisted damage paths (direct damage, `target.Damage` without AOS types) and anything that removes
   the 70 cap, e.g. resist debuffs (GraspingClaw, RuneCorruption, FanningFire).
5. FierceDragon, by design.
6. BardImmune bosses, which the bard simply cannot touch (Medusa, Meraktus, WyvernRenowned).
The big custom bosses are HP sponges: their threat is time, not danger.

### 5.7 What would have to scale for 500-1000 to matter

Formula by formula, what more skill buys a player and what a creature would need to keep pace:

| lever | player 300 -> 1000 | creature needed to keep pace |
|---|---|---|
| Hit chance vs player (ratio of atk+20 to def+20) | defense 320 -> 1020 | attack skill ~ the player's (1000) to keep ~50%; at 120 it sits at the 2% floor at 1000 |
| Player hit chance | already 100% | creature defense skill near the player's |
| Player melee damage (uncapped Str/Tactics/Anatomy) | x7.0 -> x14.9 | HP x2 again over today's |
| Player spell damage (EvalScale 30+9E/100) | x3.0 -> x9.3 eval term | HP / resists x3 |
| Bard success | saturated from ~150 | the 160 cap and the -(M-100)/2 term make it unwinnable; needs formula change |
| Discordance | -100 resist at 300, -380 at 1000 | no creature value survives; needs a clamp |
| Player HP / resists | fixed (Str-bound, 70 cap) | creature damage does not need to scale for the player to die faster; it needs to land |

To keep 500-1000 "meaningful" by scaling content, every creature's attack skill, defense skill, HP and
damage would need to rise roughly in proportion to the player's skill (attack skill alone x3-8), the bard
difficulty cap and formula would need replacing, and discord would need a clamp. That is a rewrite of about
700 creature definitions plus the bard skills, and it would make all existing content dead for anyone
under 300.

Recommendation: treat the upper range as prestige, and do it on purpose rather than by accident:
- Clamp the effective skill used by a few formulas that run away, not the displayed skill: Discordance
  effect (hold it at the OSI -28% or a modest extension), the Peacemaking/Provocation/Discord musicianship
  term, ScaleDamageAOS Tactics/Anatomy bonuses, and EvalInt scaling. A soft curve (full value to 120,
  then diminishing, e.g. 120 + sqrt(skill - 120) x k) keeps 300-1000 visible and slightly better without
  breaking the creature table.
- Let skills above ~150 pay out in non-combat or sideways ways (titles, cosmetic, crafting quality tiers,
  gathering yield, access to prestige content), not raw power.
- If endgame danger is wanted, build a small tier of new encounters whose threat is mechanics (unresisted
  or resist-piercing specials, adds, timed AoEs, BardImmune) plus attack skills of 300+, rather than more
  HP. The current 47k-60k HP bosses show that HP alone only adds time.
- Before any of this, decide whether the CheckHit discord sign quirk (BaseWeapon.cs:1337) is meant to be
  attacker or defender. It changes outcomes once discord exceeds about 45.

---

## 6. A first XP curve (FIRST DRAFT for Chase)

Script: `notes\cc-P20-scratch\xp_curve.py`. Every number is a placeholder to react to.

- **XP to the next level: `XP(L) = 40 x L^1.5`** (rounded down). Total to reach level N is about
  `16 x N^2.5`.
- **XP per kill: `5 x creature level`** (F-14 creature level), so XP per kill grows with the player.
  Time per level then grows as `L^0.5`, and a loop to cap N takes time proportional to `N^1.5`.
- **Later loops faster**: +20 percent XP per completed loop (loop 13 earns 3.6x).
- **Echo XP**: x2 XP on levels the character already reached in an earlier loop, so the replayed
  1 to (previous cap) stretch goes quickly and the new levels carry the weight.
- XP from skill gains, crafting, gathering and discoveries can feed the same pool; not modeled here.

| level | XP to next | total XP to reach |
|---|---|---|
| 1 | 40 | 0 |
| 5 | 447 | 680 |
| 10 | 1,264 | 4,439 |
| 25 | 5,000 | 47,513 |
| 50 | 14,142 | 275,783 |
| 100 | 40,000 | 1,580,001 |
| 200 | 113,137 | 8,994,376 |
| 300 | 207,846 | 24,837,556 |
| 500 | 447,213 | 89,218,979 |
| 1000 | 1,264,911 | 505,331,643 |

Two assumptions:
- **A, steady**: 120 kills an hour, creatures at the player's own level.
- **B, cautious**: 60 kills an hour, creatures at 75 percent of the player's level.
- A third column shows A if the strongest content sits at level 300 (so kills past 300 earn a 300
  rate). That is the real risk: see section 5 on whether content exists that high.

| loop | cap | hours A | hours B | hours A, content tops at 300 | cumulative A | cumulative B |
|---|---|---|---|---|---|---|
| 0 | 50 | 15 | 41 | 15 | 15 | 41 |
| 1 | 100 | 30 | 81 | 30 | 46 | 122 |
| 2 | 150 | 42 | 113 | 42 | 88 | 235 |
| 3 | 200 | 53 | 141 | 53 | 141 | 376 |
| 4 | 250 | 63 | 167 | 63 | 203 | 542 |
| 5 | 300 | 71 | 190 | 71 | 275 | 733 |
| 6 | 350 | 80 | 212 | 82 | 354 | 945 |
| 7 | 400 | 87 | 233 | 95 | 442 | 1,178 |
| 8 | 500 | 123 | 327 | 154 | 564 | 1,505 |
| 9 | 600 | 144 | 385 | 207 | 709 | 1,890 |
| 10 | 700 | 165 | 441 | 268 | 874 | 2,331 |
| 11 | 800 | 185 | 495 | 337 | 1,060 | 2,826 |
| 12 | 900 | 205 | 546 | 412 | 1,265 | 3,372 |
| 13 | 1000 | 224 | 596 | 493 | 1,488 | 3,968 |

Reading it: loop 0 is two to five evenings to a week, which meets F-12's "first cap in days, not
weeks". GM (100) arrives after about 46 to 122 hours. Max level is a long-term prestige goal of
1,500 to 4,000 hours. The single coefficient 40 scales every row linearly; the exponent 1.5 sets how
much the late loops stretch.

---

## 7. Ranked changes the level and loop system needs

Sizes: S = under a day for an implementer with `build.sh`, one or two files; M = a few days, several
files or a patch set with tests; L = a week or more. "Patch" means a change to a pinned file (needs its
alternatives argued in `notes/` first, AGENTS.md). Ranked by risk removed per unit of work; the first
four are live today and do not wait for the level system.

| Rank | Change | Why | Size |
|---|---|---|---|
| 1 | Restore a Mining cap in `customizations\SmithGuildSalvageBag.cs:145-148` (pinned uses 100, `Items/Containers/SalvageBag.cs:94-98`; any cap that keeps the return under the input works) | live ingot dupe above Mining ~143 | S, ours |
| 2 | Hide or refund the Smith Seal power scroll tab (`SmithSealCatalogGump.cs:104-107`) until per-character caps exist | live: bought caps vanish at next login | S, ours |
| 3 | Probe, then clamp, the Discordance effect (hard cap 28, OSI at 120) | possible exception in the swing timer at exactly 300 (`Discordance.cs:183`, `BaseWeapon.cs:1430`); certain wrong behaviour above | S, patch; probe first |
| 4 | Clamp the chance breaks live at 300: Parry/Bushido block, Feint, Hiding combat range, Stealing caught and weight, Detect Hidden radius, bard success (Musicianship term), Resisting Spells | each is an exploit at today's cap | M, about 8 pinned files, patches |
| 5 | Per-character max level, stored keyed by serial in our account data (`ClusterFAccountData`, as `CharacterGuildData` does), and `ClusterFSkillCaps.Apply` writing `cap = maxLevel` per character | the foundation of F-12; fixes rank 2 properly | S-M, ours |
| 6 | First max level for existing characters = the lowest ladder cap at or above their highest Base (grandfather) | avoids a clamp or compensation pass (AGENTS.md rule 7); pinned never lowers Base (`Server/Skills.cs:205-219`) | S, ours |
| 7 | One "effective skill" helper (soft curve past 120) and route the ~30 runaway magnitudes through it: Tactics, Anatomy, Lumberjacking damage; EI and Inscription spell damage; Spirit Speak; Mysticism; heals (Bandage, Magery, Chivalry, Bushido); regen (Focus, Meditation: ours); ranges and radii (Tracking, Peacemaking, Earthquake, Reveal, Detect Hidden); tinker trap level; potion enhancement; Arms Lore armor; stable slots; fishing rares | without it, nothing past 300 is safe | L, patches across ~25 pinned files plus ours (RegenRates, Meditation); one test per formula |
| 8 | Fix the subtractions that cross zero: Surprise Attack malus, Reflect/Protection maluses, Hiding range floor, self-bandage delay floor | the remaining throw / inversion risks | S-M, patches |
| 9 | Gain paths above each skill's ceiling: a use per skill whose maxSkill follows the cap (pattern: `customizations\Meditation.cs:92`), or content (recipes, ores, locks, maps) with maxSkill up to the loop caps; fix Blacksmithy's 295-300 dead zone and our large BOD lock-out first | otherwise 39 skills cannot climb past 160 no matter the cap | L, mostly ours (craft registrations, harvest tables), some patches |
| 10 | Patch `PowerScroll.CanUse` / `StatCapScroll.CanUse` so OSI scrolls never raise a cap; make them merge inputs | under loop caps a 120 scroll becomes usable and skips the loop gate | S, patch |
| 11 | Legacy Scroll line: one `SpecialScroll` subclass whose value is the max level it unlocks, consumed by the loop reset; League merge service; drops at champion, paragon and boss sites | F-12 decision | M, ours |
| 12 | Level, XP and loop reset itself (F-12): XP sources from the achievement hooks, reset gump, loop rewards, stat cap per loop | F-12 | L, ours |
| 13 | Gain pacing decision: with ClusterFSkillGain (3 rolls, 5x) and total cap 58 x cap, a skill reaches any cap in under 2,000 uses where content exists. Decide whether the level cap alone should pace skills | design, not code; affects how loops feel | S once decided (config) |
| 14 | `stats.statMax` (default 125) if stats are meant to gain toward 500 by use | live value unverified | S, config |
| 15 | Creature levels for F-14 need a scale past Bard difficulty's hard cap of 160 (68 creatures sit on it, 34 of them ours) | F-14 assumed Bard difficulty spans the range | M, ours |
| 16 | Prestige-tier encounters whose danger is mechanics, not HP, for 500 to 1000 | section 5 recommendation | L, content |

## 8. Contradictions with F-12's decisions and the prior designs

1. **Phase 4F's "natural gain slowdown past 200 is sufficient" is wrong** (section 3.3). The gain formula
   is relative to the cap; there is no slowdown at 200. What exists instead is a hard stop at each use's
   maxSkill, which by itself would make most skills unable to reach any cap above about 160.
2. **F-12 "max level 1000, so each skill up to 1000" is safe in storage but not in the rules.** 41 of 58
   skills break by 1000 (section 2.0). Raising the cap past 300 before rank 7 above would make the
   breaks worse. This does not contradict the decision; it orders the work.
3. **F-14 plans creature levels from `BaseInstrument.GetBaseDifficulty`.** It hard-caps at 160 and 68
   creatures sit on the cap, including every big boss (section 5). It cannot map onto 1000 player
   levels, or tell a 47k HP boss from a 2k HP one. F-14 needs its own scale above about 120.
4. **AGENTS.md rule 7 ("nothing should ever require a migration event ... or a compensation pass")
   against F-12's first cap of 50 for everyone.** Live characters already hold skills up to 300 (and at
   least the achievements `skills.grandmaster` and `skills.triple_grandmaster` at 300,
   `customizations\ClusterFAchievements.cs:950`, `:984-993`). Clamping them to 50 would be a
   compensation pass. Grandfathering by first max level (rank 6) avoids it, and pinned keeps Base when
   Cap is lowered, so even doing nothing does not destroy skill (it freezes it; item bonuses on that
   skill stop applying, `Server/Skills.cs:319-327`, `AOS.cs:1123`). **Chase to confirm grandfathering.**
5. **Roadmap "Extended Resources and Mining" (`roadmap.md:457-500`) says Mining progression should use the
   full 0-300 range.** The mining side tops out at 155 for ore (`ClusterFMiningExtension.cs:93`); only the
   smithing ingot gates run 100-300 (`ClusterFMiningExtension.cs:148-181`), and extended ores smelt at the
   default difficulty 50 (`Ore.cs:176-186`). So 0-300 exists on paper and on one side only.
6. **`ClusterFMiningExtension.cs:148-150` still says power scrolls raise the cap to 500** (Phase 4F), which
   F-12 replaced. Comment only.
7. **Roadmap "Champion Spawn and Mastery Rewrite" still lists "keep OSI's 105-120 power scrolls ... or fold
   them" as open** (`roadmap.md:915-930`); F-12 settled it (fold them in). The roadmap line is stale.
8. **F-13's veteran reward change** ("no skill cap or stat cap bonuses") already has a live side effect:
   `ClusterFStatCaps` sets a flat 1500, so the veteran +5 stat reward is lost for anyone who had it, and
   `HasStatReward` stops it being re-granted (section 4). F-13 asked to "check what existing characters
   already got"; this is the answer for the stat part.
9. **Gain speed and the loop design pull against each other.** F-12 wants skill growth "earned by use"
   (the stubborn skill grinder). With today's ClusterFSkillGain settings, a skill climbs to any cap in
   under 2,000 suitable uses (section 3.4), so within a loop the grind is short and the level cap does
   all the gating. Not a contradiction of any written decision, but worth Chase knowing before tuning.
10. **Roadmap "Avoid: disposable progression loops"** (`roadmap.md`, World Identity) sits beside the
    new mandatory loops. The Legacy Awakening section already reconciles it (history preserved), so only
    the wording is in tension.
