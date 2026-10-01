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
:272`, the Smith Seal scroll catalog (`customizations\SmithGuildSalvageBag.cs:139-148`,
`customizations\SmithSealCatalogGump.cs:104-107`), the Parry and Bushido block formula
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
