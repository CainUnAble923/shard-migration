# cc-P201: deployable traps (design pass)

2026-10-20. Prompt: `D:\UO\cc-prompts\claimed\Gold\cc-P201-deployable-traps-design.md`. Model: Fable (the Gold Golem).
Kind: design, docs-only. Nothing built, nothing placed, no code touched. A build prompt follows once Chase answers the
decision list. Both repos were clean at the start (`git --no-optional-locks status --short`, code and docs).

## Headlines

1. **Recommendation in one line:** tinkers craft trap kits, a thief sets them with **Remove Trap** (the skill with no
   active use today), Poisoning and Alchemy load the payloads, the Thieves' Den owns the craft and the Tinkers' Union
   the kits. Eight traps: snare net, caltrops, gas, blast, dart, bear trap, alarm and shackle. Monsters trigger them,
   players and pets never (a Felucca switch is offered, default off). The owner must be within 12 tiles or the trap
   lies dormant, every trap has charges and must be re-set by hand, so there is no AFK farming at all.
2. **OSI has done this three times and always for PvP:** faction traps (Pub 8), the goblin floor trap kit (Pub 70)
   and Vice vs Virtue traps (Pub 86) all fire on enemy players only (section A.3). No OSI trap ever fires on a monster
   for a player. This design is ours, built on their mechanics (BaseTrap's movement hook, the hidden-item reveal
   window, the Tinkering trap crafts) with the target flipped.
3. **The art is mostly stock.** The client already holds a bear trap open and shut (0xB2C5 and 0xB2C3, 44 x 44), floor
   spikes for caltrops (0x119A-0x11A5), a powder keg for the blast trap (0x1940), a folded fishing net (0x0DC8), a
   cowbell for the alarm (0x4C5A) and the dart hole (0x112C). Four art requests are left (section 7): the sprung snare,
   a floor dart launcher, the gas canister and the shackle's rune ring, plus eight pack icons. `ART-LIBRARY.md` and
   `D:\UO\third-party\servuo-ideas.md` do not exist on this PC (section 11); the wishlist line is written here for the
   integrator to append.
4. **Rootdeep gets eight stock floor traps as hazards** (mushroom puffs by the decoy chests, spikes on the Warren's
   descents, a saw at the Thicket's gap, gas on the Gloom ring, the stone face at the Queen's door), all seeder rows,
   no code. **The tutorial moment is The Stacks:** the Echo hands a trainee two practice nets at the aisle mouth and the
   Hoarding Rat, which runs, is the lesson (section 6).
5. **Kill credit needs no new rule.** A trap deals its damage *from the owner*, so pinned's looting rights, the loot
   boxes, Clean Up Britannia's corpse points and the coming F-24 culls all credit the trapper through the one path
   they already use (`GetLootingRights`, section A.5). Presence is the whole credit rule: no owner within 12 tiles, no
   trigger.
6. **Two things this PC lacked:** `D:\UO\ModernUO-pinned` and `D:\UO\ServUO-pub57` were not on the Gold Golem's PC
   (the join kit lists them as "clone when the PC takes server prompts"). I cloned both (section 11). Every pinned
   citation below is at `d4531cd94`, every ServUO one at pub57 `d76bf444`.

## Decision list for Chase

| # | Decision | Recommendation | The alternative |
|---|---|---|---|
| D1 | **The skill** | **Remove Trap arms and disarms** deployables (it gains on both). Tinkering crafts the kits (new recipes on the Tinkering ladder). Poisoning sets a gas trap's poison, Alchemy brews the gas and blast payloads. Hiding and Stealth are the rogue's edge (D2) | Tinkering both crafts and sets (one skill, a tinker build; the thief then has no part). Or a new "Trapping" skill: no, the client's skill list is fixed |
| D2 | **The guild** | **The Thieves' Den owns it** (Remove Trap is the Den's skill, `ClusterFGuildStarterPath.cs:55`), the Tinkers' Union makes the kits. No rank is needed to set a trap; Den rank adds perks: Journeyman +1 trap out, **Master: traps work on bosses** (the same rank monster stealing uses for bosses, `ThievesDenStealRules.cs:55`) | A new trapper path or guild: no, the Den is thin today and this gives it a second trade |
| D3 | **The trap list** | **Eight:** snare net, caltrops, gas, blast, dart, bear trap, alarm, shackle (section 3). The alarm and the shackle are the "alarm trap" and "binding trap" Chase noted on 2026-10-02 for high tinkers | Cut the shackle (a magic hold, the only one needing a scroll) for a first build; add a bait item later |
| D4 | **PvP** | **Monster-only everywhere.** Players, pets and summons never trigger a deployable, on any facet. A `traps.pvp` setting (default off) lets Felucca traps hit anyone the owner may harm, flagging the owner as a thrown potion does | Felucca-on from day one. Not recommended: the shard has no written PvP policy (section A.5) and OSI's own PvP traps were a griefing surface |
| D5 | **Credit** | **The owner within 12 tiles, same map, alive and logged in, or the trap does not fire.** Trap damage registers from the owner, so loot rights, boxes, Clean Up and culls follow pinned's rules unchanged. Charges, not timers, stop farming: a trap fires its charges and then waits for a hand re-set | Credit without presence (the trap fires alone, the kill counts): no, that is the AFK farm |
| D6 | **The Rootdeep moment** | **The Stacks** (x 5156-5168, y 1132-1142): on a trainee's first step into the aisles the Echo drops two practice nets and names the Hoarding Rat, which runs; netting any rat completes the station. Plus eight stock floor traps as hazards (section 6) | The Warren's Tunnel Foot (after graduation, Burrow Scamps): later, less safe, and the Vault's rats are the gentler teacher |
| D7 | **Art** | Stock art for six of eight; four requests through P152's pipeline plus icons (section 7). The bear trap needs one client check: its ids sit above 0x8000 | Request everything new for a matched set (more money, later) |

Say yes, or change any row, and the build prompt is written from this document.

---

## 0. Before starting

- `git --no-optional-locks status --short`: both repos clean (code `golem/Gold/P201`, docs `golem/Gold/P201`).
- Read: skills-design.md (Tinkering "55", the Thief section and the higher-poisons draft), P15 (guild starter path),
  P80 (tutorial stations), P139-P141 (Rootdeep creatures, Vault, layout), P142 (monster stealing's shard rules),
  P47/P48/P75 and feature-queue F-24 (hunts and culls), P79 and P175 (loot boxes, Clean Up corpse credit), P152 (the
  art pipeline), the playbook, community-scripts-wishlist.md, fidelity-principle.md's register format, the CHANGELOG
  comment (no code changed, so no patch note).
- Engine reading is in section A at the end (pinned first, ServUO as port source), cited file:line. Three search
  agents gathered the citations; I re-read the ones the design leans on (`BaseTrap.cs:36-65`, `DefTinkering.cs:672-688`,
  `Hiding.cs:50-73`, `DetectHidden.cs:234-252`, `Notoriety.cs:207-242`, `TileData.cs:288-317`, `GoblinFloorTrap.cs:20-200`,
  `VvVTraps.cs:85-110`, `ClusterFSkillClamps.cs:86-96`, `SpiderWebbing.cs:67-84`, `ClusterFCorpseValue.cs:60-70`).
- P199 (the trap training kits) has not run: it is still in `D:\UO\cc-prompts\queue\` with no notes file, so the
  Publish 97 kits are not ported. Nothing here depends on them; section 1 says where they would plug in.

## 1. Who and how

**The parts, and which skill each one is.**

| Part | Skill | What it decides |
|---|---|---|
| Craft the kit | **Tinkering** (Tinkers' Union recipes on the ladder, section 3 gates 30 to 110) | Whether the kit exists; **exceptional** = +1 charge and x1.2 damage (the tinker's mark, as with tools and jewelry) |
| Brew the payload | **Alchemy** (a poison potion for the gas trap, an explosion potion for the blast trap: the two potions OSI's container traps already take, `DefTinkering.cs:434-450`) | The gas trap's poison family and the blast trap's base (lesser, normal, greater) |
| Load the poison | **Poisoning** (arming a gas trap is a Poisoning use with the potion's own window, `Skills/Poisoning.cs:124`) | The poison level the gas trap can carry: `min(potion level, Poisoning / 25)` (Lesser at 0, Regular 25, Greater 50, Deadly 75; the higher poisons ride their gates 140/170/200 when they exist). Poisoning gains on every arming, as on a weapon |
| **Set the trap** | **Remove Trap** (D1) | Arming time, trigger size, hold durations, damage scale, concealment, how many out at once, and the gain path (section 1.2) |
| Set it unseen | **Hiding** and **Stealth** | Whether placing keeps you hidden, and the hidden edge (section 2) |
| Spot it, pick it up | **Detect Hidden** (reveal, as faction traps) and **Remove Trap** (disarm and salvage) | Another player's reveal and salvage (section 4) |

**Why Remove Trap and not Tinkering for the setting.** Remove Trap is the one thief skill with no active use except
disarming (pinned `Skills/RemoveTrap.cs`), it needs Lockpicking 50 and Detect Hidden 50 to use at all (`:17-21`), so it
already marks a thief build, and the skills design (decided 2026-10-02) gives it two things this design completes: its
gain path "climbs on tinker traps and ladder chests" (skills-design.md:1294) and its mastery reward is "a disarmed
trap can be salvaged into a trap kit (for tinkers)" (`:1307`). A tinker still has a whole trade here: every kit is a
tinker craft and nobody else can make one. A pure tinker who wants to set their own traps takes Remove Trap; the two
skills are cheap to hold together (Tinkering, Lockpicking, Detect Hidden, Remove Trap is a classic UO template).

### 1.1 What Remove Trap scales (numbers)

Let `RT` be the setter's Remove Trap value (0 to 200).

| Thing | Formula | At 0 | 50 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|
| Traps out at once | `1 + floor(RT / 50)` (+1 at Den Journeyman) | 1 | 2 | 3 | 4 | 5 |
| Arming time (in the open) | `4 - RT / 100` s | 4 s | 3.5 | 3 | 2.5 | 2 |
| Trigger radius, single-target traps (snare, dart, bear, shackle) | 0 below 100, 1 from 100, 2 from 200 (the creature steps within that many tiles of the trap) | 0 | 0 | 1 | 1 | 2 |
| Effect radius, area traps (gas, blast, caltrops) | fixed per trap (section 3); RT does not grow it | | | | | |
| Damage scale | `0.5 + RT / 200` | x0.5 | x0.75 | x1.0 | x1.25 | x1.5 |
| Hold duration (snare, bear, shackle) | base + `RT / 50` s | base | +1 | +2 | +3 | +4 |
| Concealment (what Detect Hidden rolls against) | `RT` (+20 when placed hidden, section 2) | 0 | 50 | 100 | 150 | 200 |
| Set-skill gain | `CheckSkill(RemoveTrap, kit.Min, kit.Max)` on arming; on a hit `CheckSkill(RemoveTrap, kit.Min + 40, kit.Max + 70)` | the shackle's hit window reaches 200 | | | | |

Tinkering decides nothing after the craft (quality only): the skills design already split "power" from "damage" for
container traps so a 200 tinker is "hard to beat, not kills you" (skills-design.md:586-591, the built clamp
`ClusterFSkillClamps.cs:86-96` caps the damage level at 12). Deployables keep that: damage is the kit's number times the
setter's scale, never times Tinkering.

### 1.2 Guild and rank gates (D2)

- **Setting needs no guild.** Remove Trap 30 and a kit (the kit's own minimum, section 3) is enough, the same way
  Hiding or Poisoning need no membership. The Den's refusal lines are for places, as monster stealing does
  (`ThievesDenStealRules.cs:6-20`).
- **Den perks** (the Den's ladder is the generic one: Initiate below 1,000 reputation, Apprentice 1,000, Journeyman
  5,000, Master 15,000, Grandmaster 50,000, Legendary 100,000, `ClusterFGuildSystem.cs:618, :749-757`):
  - Apprentice: sees party members' armed traps (section 2 gives this to the party by default; Apprentice adds the
    overhead "[set by <name>]" on hover).
  - Journeyman: +1 trap out at once.
  - **Master: traps affect bosses** (ClusterFLootBoxes.IsBoss plus ShardBossTypes, `ThievesDenStealRules.cs:166-167`), at
    half hold and half damage. Below Master a boss walks through every trap, the trap stays armed, the owner reads
    "The <boss> does not notice your <trap>. The Den would not trust you with that one yet."
  - Grandmaster: salvaging another player's trap (section 4) always succeeds.
- **Tinkers' Union:** the recipes are plain Tinkering ladder rows (section 3); the Union's rank does nothing extra.
- **The tutorial's practice net** (section 6) needs nothing: Remove Trap 0, it is the "I set a trap once" lesson.

Where P199's training kits fit when they land: the Circuit, Cylinder and Slider kits gain Remove Trap 0-100 on a solve
(ServUO `CircuitTrapTrainingKit.cs:85-87`); deployables gain 0 to 200 on sets and hits, so the kits are the townside
practice and the dungeon is the field; nothing here conflicts.

## 2. Placing hidden or in the open

**Either works.** Anyone with the skill and a kit double-clicks it, targets a tile within 2 (the goblin kit's reach,
`GoblinFloorTrap.cs:188`) and arms it over the arming time (an "arming" progress line, cancelled by moving or taking
damage, like a bandage). Placing in the open is the ordinary case and reveals nothing new: a visible player set a trap.

**Placing while hidden is the rogue's edge.** Three things it adds, and one it costs:

| | In the open | While hidden |
|---|---|---|
| Arming time | `4 - RT / 100` s | **1 s flat** (the set is a stealth motion, not a build) |
| Concealment | `RT` | `RT + 20` |
| The ambush | | the trap's **first hit on a creature with no combatant** is x1.5 (a sneak attack: the thing never saw it coming) |
| The cost | | **one stealth step.** Arming while hidden runs the exact stealth step check, `CheckSkill(Stealth, -20 + ar*2, 60 + ar*2)` (pinned `Skills/Stealth.cs:96-100`), and spends one of `Stealth / 5` allowed steps (`:102`). Pass: you stay hidden and the trap is set. Fail: `RevealingAction`, the trap is set anyway. At 0 steps left it reveals you as running does (`PlayerMobile.cs:3420-3441`) |

So "placing does not reveal you if a check passes": the check is the stealth step, not a fresh Hiding roll, because
Hiding's own check is refused while anything is fighting you within `(100 - Hiding) / 2 + 8` tiles (`Hiding.cs:53-55`),
which is exactly when a trapper wants to work. Nothing in pinned reveals a player for double-clicking or targeting an
item (`RevealingAction` has 54 callers in UOContent, none for an ordinary item use, section A.4); the build must not add
one.

**For both:** the trap is `Visible = false` and `Movable = false`, so monsters do not path around it (creatures never
scan for items: `BaseAI.DetectHidden` scans players only, `BaseAI.cs:1142-1143`) and other players do not see it.
**The owner and the owner's party see it** through a `CanSeeStaffOnly` override (pinned `Server/Items/Item.cs:471`, the
virtual that `Mobile.CanSee(Item)` ends in, `Mobile.cs:7190-7229`): no client change, the owner's client simply gets
the item. Staff see everything. Another player finds it only with an active Detect Hidden scan against the trap's
concealment (section 4). The "trap monsters cannot see" idea from the prompt is already true for every trap: a creature
only ever "sees" one through the detect roll in section 4.

**Overhead text.** Armed, to the owner only: "You set the <trap>." (in the open) or "You set the <trap> without a
sound." (hidden, passed) and "You set the <trap>, and something hears you." (hidden, failed). The trap's name on hover
for the owner and party: "a snare net [armed, 1 charge]"; sprung and empty: "a snare net [spent]".

## 3. The traps

Common rules: a kit is a stackable-by-type item in the pack (one kit, one trap); exceptional kits carry +1 charge and
x1.2 damage; damage is `kit x scale(RT)` where scale is 0.5 to 1.5 (section 1.1); a hidden placement's first hit is
x1.5; the trigger is a creature's step (section 4). "Charges" is how many times it fires before it needs a hand
re-set (section 5). Tinkering gates are craft minimums; the gain window is gate to gate + 50 on the Tinkering ladder,
so the eight recipes carry Tinkering from 30 to 160. Ingredients are OSI items with their sources named.

| Trap | Art (stock) | Trigger / effect area | Effect | Numbers at RT 100 (x scale) | Charges | Tinkering / Remove Trap to set | Ingredients (source) | Who shrugs it off |
|---|---|---|---|---|---|---|---|---|
| **Snare net** | set: folded fishing net 0x0DC8; sprung: request (section 7) | single, trigger radius 0 (1 at RT 100, 2 at 200); holds the creature that steps in | **Hold:** `Frozen = true` (the Burrows' spider webs use `Frozen`, `SpiderWebbing.cs:35-45`; the Gloomspinner's web uses `Paralyze`, `GloomCreatures.cs:29`): cannot move, can still swing at anyone adjacent | hold 4 + RT/50 s = **6 s**; no damage | 1 (2 exceptional) | 30 / 0 | 10 cloth (Tailoring) + 2 spider's silk (reagent vendor, spiders) | bosses below Den Master; **flying** creatures (`CanFly` or `Flying`: 25 pinned overrides plus the Burrows' bats and crows) walk over it; **incorporeal** list (section 3.1) pass through |
| **Caltrops** | floor spikes 0x119A-0x11A5 (12 facings of scattered spikes) | **patch**, radius 1 (3 x 3 tiles); every creature stepping in | 5-10 physical + **bleed** (`BleedAttack.BeginBleed`, `Items/Weapons/Abilities/BleedAttack.cs:61`) + **slow**: the creature's active speed doubled for 8 s (a timer restores it; never saved) | 5-10 + bleed (3 ticks) | 5 steps, then the patch is spent | 40 / 20 | 10 iron ingots (Mining) + 1 springs (Tinkering part, `DefTinkering.cs:273`) | flying; incorporeal; bosses below Master; paragons take half the slow |
| **Gas trap** | set: request (a small canister); cloud effect 0x113A, sound 0x231 (the OSI poison trap's, `TrappableContainer.ExecuteTrap.cs:119-144`) | area, radius 2; a **cloud lingers 3 s** and poisons anything that enters | `ApplyPoison(owner, level)`; level = `min(potion, Poisoning / 25)` (section 1) | Deadly at Poisoning 75 with a Deadly potion; Lethal needs a Lethal potion (none in pinned: the higher-poisons draft adds them) | 1 (2 exceptional) | 60 / 40 | 5 iron ingots + 1 gears (`DefTinkering.cs:270`) + 1 poison potion of the wanted family (Alchemy, nightshade) | the 58 pinned creatures with `PoisonImmune` at or above the level (paragons +1 level, `BaseCreature.cs:1932-1933`); the Rootdeep bosses as set per creature |
| **Blast trap** | keg 0x1940 (a powder keg reads as a bomb); explosion effect 0x36BD, sound 0x307 | area, radius 2 (the explosion potion's own range, `BaseExplosionPotion.cs:13`) | **fire** damage to every creature in range, no split (a bomb, not a thrown flask) | lesser 20-40, normal 30-60, greater 40-80 fire, x scale: **30-60 at RT 100** with a normal potion, 60-120 at RT 200 with a greater | 1 | 90 / 60 | 5 iron ingots + 1 gears + 1 explosion potion of the wanted strength (Alchemy, sulfurous ash) | fire-immune creatures (fire resist 100, elementals of fire); bosses below Master; nothing else |
| **Dart trap** | set: request (a floor launcher); the dart hole 0x112C is wall art | single, trigger radius as the snare; fires one dart at the creature that steps in | physical; **loads up to 5 fukiya darts** (stock 0x2806, ninja vendors), and a dart poisoned by Poisoning (darts are a legal Poisoning target, `Skills/Poisoning.cs:59-73`) carries its poison | 25-50 physical per dart, plus the dart's poison | 1 per loaded dart, up to 5 | 50 / 30 | 5 iron ingots + 1 springs + 1 crossbow bolt (Fletching) for the mechanism; darts are the ammunition | incorporeal; bosses below Master; the ambush x1.5 applies |
| **Bear trap** (ours) | **stock:** open 0xB2C5 "Bear Trap On", shut 0xB2C3 "Bear Trap Off" (44 x 44, section 7) | single, the trap's own tile only (radius 0 at every RT: jaws, not a tripwire) | **hold** 6 + RT/50 s and **15-30 physical** on the snap, then bleed; releases, then springs open again by itself (the next charge) | hold 8 s, 15-30 | **3** (4 exceptional); re-arms itself between snaps | 80 / 50 | 10 iron ingots + 2 springs + 1 gears | flying; incorporeal; bosses below Master (a Master's bear trap holds a boss 4 s) |
| **Alarm trap** (ours, Chase 2026-10-02 "an alarm trap, tells the owner who tripped it and where") | cowbell 0x4C5A / 0x4C5B (stock), sound 0x495 "trap" is a client sound, or a bell | area, radius 2; **no damage** | the owner (anywhere on the map, this one ignores the 12-tile rule because nothing is farmed) reads "Your alarm at <region>, <x>,<y>: a <creature>." with a private sound; the creature flashes hue for 10 s to the owner's party; the trap re-arms | | **10** | 70 / 30 | 4 iron ingots + 1 gears + 1 springs | nothing: an alarm notices everything, including bosses and flyers (it is a bell, not a jaw) |
| **Shackle trap** (ours, Chase's "binding trap, paralyzes for a few seconds") | set: request (a rune ring on the floor) | area, radius 1 (3 x 3); every creature in it when it fires | **hold** 3 + RT/50 s (`Frozen`), the group-control trap: a pack stops, the party kills it | 5 s at RT 100, 7 s at 200 | 1 (2 exceptional) | 110 / 80 | 8 iron ingots + 2 gears + 1 Paralyze scroll (Inscription) | bosses below Master (a Master's shackle holds a boss 2 s); paragons half; nothing else |

A ninth row is deliberately not a trap: **bait** (a cooked lure that draws creatures within 8 tiles to walk over your
tile) is the trapper's natural combo piece but needs an AI hook pinned does not have cleanly (`BaseCreature` has no
"walk to this point" order for wild creatures short of a Home change). It is listed for the second build.

### 3.1 Who resists, in one place

- **Bosses:** `ClusterFLootBoxes.IsBoss` (`ClusterFLootBoxes.cs:157`, high-end sources, paragons left out) plus
  `ThievesDenStealRules.ShardBossTypes` (the Burrow Mother, the Gloom Queen, `ThievesDenStealRules.cs:74`): every
  trap but the alarm ignores them below Den Master; at Master, half hold and half damage.
- **Flying:** `BaseCreature.CanFly` (`BaseCreature.cs:993`, 25 overrides in pinned, the Burrows' Crop Crow and Ledger
  Bat, `FarmCreatures.cs:80`, `VaultCreatures.cs:39`) or `Mobile.Flying` (`Server/Mobiles/Mobile.cs:1193`): ground traps
  (snare, caltrops, bear) never fire; gas, blast, dart, alarm and shackle do. A flyer that "lands when it enters
  warmode" (`BaseCreature.cs:3041-3043`) is on the ground once it fights, so a second trap behind the first works.
- **Incorporeal:** pinned has no flag, so the build keeps a type list (a static `HashSet<Type>`: Shade, Spectre, Wraith,
  Ghost, Bogle, Wisp, Energy Vortex, Blade Spirits, the air and poison elementals, and ours as named). Nets, caltrops,
  bear jaws and darts pass through them; gas, blast, alarm and shackle work.
- **Poison-immune:** `PoisonImmune` at or above the gas level (`BaseCreature.cs:972`); the gas still fires and is spent.
- **Monsters with Detect Hidden** (section 4) may spot a trap instead of stepping in it.
- **Paragons:** half the slow and hold, +1 poison immunity (pinned's own rule).

## 4. Triggering, credit and gains

**What triggers.** The trap is a `BaseTrap`-style item (`HandlesOnMovement`, pinned `BaseTrap.cs:18`) with the same Z
window (`Z + 8 >= loc.Z && loc.Z + 16 > Z`, `:39-41`) and the edge rule (fires on the step that *enters* the trigger
radius, `:36-37`). A mover triggers it when **all** of these hold:

1. it is a `BaseCreature` with `IsMonster` (`BaseCreature.cs:3335`: not controlled, or controlled by a monster), not
   summoned, alive, `AccessLevel == Player`, not a vendor or invulnerable NPC, not a `TutorialCreature` of another
   player's tutorial (`TutorialCreature.cs:35-48` already filters by participant);
2. the owner is **on the same map, within 12 tiles, alive and logged in** (D5); otherwise the trap is **dormant**: it
   stays armed and silent, and the creature walks over it;
3. `owner.CanBeHarmful(creature, false)` is true (pinned's harm rule, so Young protection and the Burrows' 3-hostile
   limit for Young players still hold: a trap is the owner's harmful act);
4. the creature did not **spot** it: a creature with Detect Hidden above 0 (`BaseAI.CanDetectHidden`, `BaseAI.cs:57`)
   rolls `DH + Random(21) - 10` against `concealment + Random(21) - 10` (the player formula, `DetectHidden.cs:197-211`)
   once per trap; a spot reveals the trap to everyone for 10 s (the pinned reveal window, `DetectHidden.cs:234-252`)
   and the creature stops 1 tile short for 2 s, then walks on around it. The owner reads "The <creature> sniffs out
   your <trap>."

**Players and pets never trigger** (D4): a `PlayerMobile`, a controlled or summoned creature, or a dead bonded pet is
ignored on every facet. With `traps.pvp` on and the trap in Felucca, rule 1 widens to "any mobile the owner may harm"
(`Mobile_AllowHarmful`'s "anything goes" branch, `Notoriety.cs:209-212`) and the hit calls `owner.DoHarmful(victim)` so
the owner goes grey or red as a thrown explosion potion does (`BaseExplosionPotion.cs:180-202`). Rootdeep is Trammel
(`OldHavenBurrowsRegion.cs:5`), so the switch never touches the tutorial.

**Credit.** Every point of trap damage is dealt **from the owner**: `AOS.Damage(creature, owner, amount, ...)` for
physical and fire, `creature.ApplyPoison(owner, poison)` for gas. That writes the owner into the creature's
`DamageEntries` (`Server/Mobiles/Mobile.cs:5895-5935`), and from there:

- **loot rights** are pinned's `GetLootingRights` (players only, the top damager / 2 under 200 hits, / 4 to 1000, / 8 to
  3000, / 16 above, the latest damager x1.25; `BaseCreature.cs:3344-3455`), so a trapper who did a real share loots;
- the **corpse** carries the rights holders as aggressors for 2 minutes (`Corpse.cs:295-312, :92`);
- the **loot boxes** credit every rights holder plus `LastKiller` (`ClusterFLootBoxes.cs:159-185`);
- **Clean Up Britannia** pays the corpse to any rights holder or party member (`ClusterFCorpseValue.cs:60-70`);
- **F-24 culls and hunts** are not built (feature-queue.md:1918-1931); their credit rule is "party members within 18
  tiles at the kill" (P47 spec), which a present trapper satisfies by definition.

A hold (snare, bear, shackle) deals no damage, so a hold alone earns nothing; the kill does. That is right: the net is
the setup, the party's blades are the credit, and a trapper who wants the loot adds a dart or a bear trap.

**Gains.** Remove Trap gains on the set (`kit.Min`-`kit.Max`) and on each hit (`kit.Min + 40`-`kit.Max + 70`, section 1.1)
while the owner is present (dormant traps do not fire, so there is no absent gain to forbid). Poisoning gains on
loading a gas trap or poisoning a dart (its own windows). Tinkering gains on the craft. Hiding and Stealth gain as
they do today (a hidden set spends a step, it does not roll a gain).

## 5. Anti-exploit

| Rule | Number | Why this number |
|---|---|---|
| Owner presence | within **12 tiles**, same map, alive, online, or the trap is dormant | the update range is 18 (`Item.cs:3306`); 12 keeps the trapper on screen but lets a stealther sit a room away. The alarm is exempt (it farms nothing) |
| Charges, not time | each trap fires its charges (section 3) and then is **spent**: it does nothing until the owner double-clicks it to re-set (a new arming, a new set-gain roll) | a hand re-set is an input; no macro-free farm exists. The bear trap's self re-arm between its 3 snaps is the one exception and it is 3 |
| Decay | a set trap decays **30 minutes** after arming (refreshed by a re-set); a spent trap decays after **2 minutes**; the owner reads "Your <trap> at <x>,<y> is losing its set" at 1 minute | litter control, not farm control (presence does that). Faction traps decayed in a day (`BaseFactionTrap.cs:129-132`); 30 minutes fits a dungeon crawl |
| Out at once | `1 + floor(RT / 50)`, +1 Journeyman, so 1 to 6 | one trap a rank; a sixth trap needs the Den |
| Per area | at most **6 armed traps within 8 tiles** of a new placement, any owners; refusal "There are enough traps here already." | a party of five cannot carpet a spawn room |
| No town, no house | refused in a `GuardedRegion` with guards enabled (the goblin kit's rule, `GoblinFloorTrap.cs:146`) and in any `HouseRegion` | OSI's own line for the goblin kit |
| No door, no teleporter | refused on a tile holding a `BaseDoor`, `Teleporter`, `Moongate`, the Rootdeep crawlway, or any item that overrides `OnMoveOver`; and on the tile in front of or behind a door | a snare in a doorway blocks a corridor for everyone; a trap on a teleporter fires on arrival |
| No mounted or flying setter | refused while mounted or flying (`GoblinFloorTrap.cs:142`, cliloc 1113319) | OSI's rule, and the arming animation needs feet |
| Not on a mobile | refused if any mobile stands on the tile | the "drop it under the boss" trick |
| Logout | the trap is dormant while the owner is offline and decays on its own clock; it never fires for a logged-out owner | the other half of presence |
| Save and restart | traps are saved items (owner serial, kind, charges, armed-at, hidden flag, quality) with a version; a restart reloads them armed and the presence check resumes on the next step | no world event; the AGENTS.md rule |
| Young | a Young trapper's traps obey the Burrows' `MaxHostilesOnYoung` through `CanBeHarmful` (rule 3 above) | nothing new |

## 6. Rootdeep

### 6.1 Floor traps as hazards ("watch the floor")

All eight are stock pinned classes (`Items/Traps/`, section A.2) placed as seeder rows in `ClusterFRootdeepSeeder.cs`
(the P141 pattern: data, idempotent, `[ClusterFSeedRootdeep dryrun` then `[ClusterFSeedRootdeep`, Administrator, test
shard first). No code. They are visible items (only the FlameSpurtTrap is invisible in pinned, and it is not used),
so the lesson is literally to look at the floor. Damage is matched to the zone's tier (P140: Warren 1, Tangle and
Dawnseam 2, Gloom 3). Each sits outside every spawner's home range (the seeder already checks ranges, P141 section 3)
so a wandering spawn does not die on a trap with nobody to credit.

| # | Zone | Tile(s) | Class (pinned) | What it does | Why there |
|---|---|---|---|---|---|
| T1, T2 | The Vault, Deposit Hall | 5146,1134 and 5151,1139 | `MushroomTrap` (0x1125, passive range 2, `Dice(2,4)` = 2-8, resets 2 s, `MushroomTrap.cs:16-40`) | a puff when anyone comes within 2 tiles, 2-8 damage, creatures too | the gentlest trap in the engine, next to the decoy chests: "the floor near the chests is not your friend either". A trainee with 30-50 hits feels it and learns it |
| T3, T4 | The Warren, the two descents | 5161,1195 and 5201,1195 (one tile of each 4-wide descent, x 5160-5163 and 5200-5203, y 1193-1197) | `SpikeTrap` floor (4506 WF / 4512 NF, `RandomMinMax(1,6) * 6` = 6-36, reset 6 s, extends 1 s after the step, `SpikeTrap.cs:55-119`) | spikes on one tile of the way down; three tiles beside it are safe | the first "there is a safe path, find it" moment, tier 1, after graduation |
| T5 | The Tangle, the Thicket's gap | 5157,1222 (the gap is x 5157, y 1222-1223; the trap takes the north tile) | `SawTrap` floor (0x11AC, 5-15, `SawTrap.cs:54-62`) | a floor saw on the Bramblehulk's doorstep | the boss-room door costs a little blood, tier 2 |
| T6, T7 | The Gloom, the ring | 5165,1235 (north run) and 5232,1252 (east run) | `GasTrap` floor (0x11A8) with `Poison.Greater` (players only, `GasTrap.cs:64`) | greater poison on a step | tier 3, the Gloom is poison and webs; a cure potion lesson |
| T8 | The Queen's lair mouth | 5183,1247 (the mouth is x 5183, y 1246-1248; the trap takes the middle tile) | `StoneFaceTrap` (0x10FC, passive range 2, `Dice(3,15)` = 3-45 fire breath at 1 s, `StoneFaceTrap.cs:49-110`) | a stone face breathes fire at anyone within 2 of the door | the Queen's doorstep, tier 3 |

The map batch sets Z from the floor it draws (the seeder reads `GetAverageZ` for the ankh already). Detect Hidden is
not needed for any of them (they are visible); a player who wants the OSI "[trapped]" reveal practice gets it from
the decoy chests. Two caveats for the build: pinned's `MushroomTrap`, `SpikeTrap`, `SawTrap` and `StoneFaceTrap` hurt
creatures too (section A.2), so the tiles above are chosen off every home range; and the `GasTrap` is players only.

### 6.2 The tutorial moment: The Stacks (D6)

The Vault is the League's trainee run (bats in the Counting Room, rats in The Stacks, decoy chests in the Deposit
Hall, the Overdraft in the Strongroom; P141 section 3). The Stacks are three 3-tile aisles between two shelf rows, a
serpentine, with two Penny Rats and the Hoarding Rat (which "calls 2 Penny Rats" and spawns alone, P141 row 3). A rat
in a 3-tile aisle is the cleanest possible snare lesson, and it is before the Deposit Hall's mushroom puffs, so the
floor lesson comes right after the "set something on the floor yourself" lesson.

The step, as a tutorial station (`TutorialStations.Handlers`, key `burrows.trap`, a trial like P80's others):

1. **Trigger:** a participant's first step into x 5156-5168, y 1132-1142 (The Stacks).
2. **The Echo** (the "System:" voice, decided 2026-10-14 item 3): "The Stacks. The rats run the aisles, and one of them
   runs with the money. Here. Two practice nets. Put one down in an aisle, step back, and let the rat come to you."
   Two **practice nets** drop into the pack: a snare net kit flagged `Practice` (Remove Trap 0, no craft, 1 charge, hold
   4 s, decays in 30 minutes, cannot leave the Burrows: it deletes on any map change, and it is never salvageable).
3. **Done when** any rat (Penny or Hoarding) is held by the participant's net. The Echo: "Held. That is the whole trick:
   the floor does the waiting. Remember the floor. It does not only wait for rats." The station key lands in
   `TutorialRecord.StationsDone` (the P141 pattern, no schema change).
4. **The Hoarding Rat** is the named target of the line, and a trainee who nets it before it calls its two Penny Rats
   has done the fight the easy way, which is the point of a trap. Nothing requires it: any rat completes the station.
5. **What it hands on:** a graduate buys real kits from tinkers (none are sold by NPCs: a player trade from day one),
   and the Den's recruiter line gains one sentence: "Remove Trap sets them as well as pulls them."

Where this sits in P80's list: the "Thieving and stealth: one trial (ten skills)" wing station stays as it is (the
ten skills' trial is still a TODO); `burrows.trap` is a new core-adjacent station inside the Vault run, because every
trainee walks The Stacks and not every trainee takes the thief wing.

## 7. Art and feel

### 7.1 Stock first: what the client has (tiledata search, `tiledata.mul` of client 7.0.117.0; renders in `notes\art\deployable-traps\`)

Item ids below are art ids (the tiledata list reports them +0x4000; the render names carry the art id).

| Need | Stock art found | Render | Verdict |
|---|---|---|---|
| Bear trap, open and shut | **"Bear Trap On" 0xB2C5 / 0xB2C6 and "Bear Trap Off" 0xB2C3 / 0xB2C4** (two facings each, 44 x 44) | `stock-0xB2C5-bear-trap-on.png`, `stock-0xB2C3-bear-trap-off.png` | **use as is.** One check for the build: the ids are above 0x8000. Pinned reads 0x10000 tiledata entries for a 7.0.9.0 or newer file (`Server/TileData.cs:288-317`), so the server knows them; whether our TazUO draws a static at 0xB2C5 is unverified until `[add Static 0xB2C5` is seen on the test shard (a play-test item) |
| Snare net, set | fishing net 0x0DC8-0x0DD5 (a folded net, 44 x 34) | `stock-0x0DC8-fishing-net.png` | use for the set net; the hanging "net" 0x1EA3-0x1EA6 (45 x 115) is wall art, no |
| Snare net, sprung | none (the webs 0x10B8-0x10D7 are spider webs) | `stock-0x10D2-small-web.png` for contrast | **request** |
| Caltrops | **floor spikes 0x119A-0x11A5** (12 facings, small scattered spikes, 45 x 75) | `stock-0x119A-floor-spikes.png` | use as is (set and spent: two of the facings) |
| Gas trap | gas trap 0x113A-0x113E, 0x1145-0x114A, 0x11A6-0x11AB are the wall-vent animation frames (near-empty stills) | `stock-0x113A-gas-trap.png` | the cloud effect 0x113A plays on firing; the set item needs a **request** (a small canister) |
| Blast trap | **keg 0x1940** (44 x 49) | `stock-0x1940-keg.png` | use as is, hued dark; the explosion effect 0x36BD is stock |
| Dart trap | dart trap 0x112C-0x1132 is a wall hole (45 x 54); fukiya darts 0x2806 are the ammunition icon | `stock-0x112C-dart-trap.png`, `stock-0x2806-fukiya-darts.png` | **request** a floor launcher |
| Alarm | **cowbell 0x4C5A / 0x4C5B** | not rendered (the id resolves by name) | use as is |
| Shackle | the Magic Trap scroll 0x1F39 and spell icon 0x208C are not floor art | | **request** a rune ring |
| Spike and saw floor traps (Rootdeep) | spike trap 0x1108-0x110E and 0x111B-0x1121, floor saw 0x11AC-0x11B5, mushroom 0x1125-0x112A, stone face 0x10F5-0x10FC and firing 0x10F7, axe 0x1133-0x1139, boulder 0x11B7-0x11BB | `stock-0x1108-spike-trap.png`, `stock-0x110E-spike-trap-up.png`, `stock-0x11AC-floor-saw.png`, `stock-0x1125-mushroom-trap.png`, `stock-0x10F7-fire-trap.png`, `stock-0x1133-axe-trap.png`, `stock-0x11B7-boulder-trap.png` | all stock, used by the pinned classes in 6.1 |
| Also looked at | bolas 0x26AC, rope 0x14F8, gears 0x1053, the potions 0x0F0A and 0x0F0D, the new spike 0x1D99 | rendered beside the rest | not needed |

The art library (`ART-LIBRARY.md`) could not be checked: it is not on this PC (section 11). What P50 recorded is that
the mimic pack's spike-trap chest (`Extra\3.bmp`, `4.bmp`, 50 x 70) is unused (`SOURCE.txt:232-233`); it is a trapped
chest look, not a floor trap, and stays where it is. The scout's backlog is the same file, also absent.

### 7.2 Art requests for P152's pipeline (`New-ArtRequest.ps1`, `D:\UO\art\requests\<id>.json`, schema 1)

Each request: destination `game-item`, kind `static`, two sizes 44 x 44 (ground) and 44 x 44 (pack icon), transparent,
style "UO classic isometric statics, 2:1 dimetric, hard black outline, 16-bit palette, no anti-aliased halo",
reference "the stock bear trap 0xB2C5 and floor spikes 0x119A as the size and shading key". Budget 8 KB a slot.

| Id | Title | Slots | Prompt core |
|---|---|---|---|
| `trap-snare-net` | Snare net, sprung | ground sprung, icon | a rope net bundled tight round nothing, pegs pulled, lying on stone; icon: a folded net with a wooden peg |
| `trap-dart-launcher` | Dart trap, floor launcher | ground set, ground sprung (lid open, spring out), icon | a palm-sized iron plate with a spring tube and a dart tip showing, half-buried; sprung: the tube open and empty |
| `trap-gas-canister` | Gas trap, canister | ground set, ground sprung (cracked, a green stain), icon | a squat iron canister with a cork and a tiny bellows, green glass window |
| `trap-shackle-ring` | Shackle trap, rune ring | ground set (a faint chalk rune circle, 3 x 3 tiles suggested by one tile), ground sprung (the circle broken), icon | a chalk circle with four small rune marks, blue-grey; sprung: scuffed through |
| `trap-icons` | Pack icons for the stock ones | bear trap, caltrops, blast keg, alarm bell, practice net | 44 x 44 pack icons matching the ground art of each |

Registration follows P152 (`find-free-art.py`, `registry.csv`, the next player package build); the build prompt
creates the five JSON files with `New-ArtRequest.ps1` on Chase's PC, where `D:\UO\art` lives.

### 7.3 Effects, sounds and text when it fires

| Trap | Effect | Sound | Overhead (public, on the creature) | To the owner |
|---|---|---|---|---|
| Snare net | 0x376A, 10, 16 (the web's, `SpiderWebbing.cs:80`) | 0x204 | "*tangled*" | "Your net has the <creature>." |
| Caltrops | a blood splat (`Blood`, the goblin trap's) | 0x22B (goblin trap) | "*limps*" | none (a patch) |
| Gas | 0x113A | 0x231 | "*coughs*" | "Your gas trap fires." |
| Blast | 0x36BD | 0x307 | "*burns*" | "Your blast trap fires." |
| Dart | moving effect 0x1BFE (a bolt) from the trap to the creature | 0x223 | "*struck*" | "Your dart trap fires." |
| Bear trap | the item swaps 0xB2C5 to 0xB2C3 | 0x22C (spike trap) | "*snap*" | "Your bear trap has the <creature>." |
| Alarm | the creature hue 0x21 flash, 10 s, to the party | 0x495 "trap" (client sound 495, soundLegacyMUL) to the owner only | none | "Your alarm at <region>, <x>,<y>: a <creature>." |
| Shackle | 0x376A on each held creature | 0x204 | "*bound*" | "Your shackle holds <n>." |

### 7.4 The scout's wishlist line

`D:\UO\third-party\servuo-ideas.md` is not on this PC. The line to append there (the integrator, or Chase, on the PC
that holds it), in that file's own row style:

`| Deployable floor traps | A player-set trap item that fires on monsters (not players): snare, caltrops, gas, blast,
dart, bear trap; a kit crafted by Tinkering, armed by a thief skill, revealed by Detect Hidden, charges and decay |
cc-P201 design 2026-10-20: look for any shard's "hunter trap" or "trapper" system, a bear-trap or caltrop art pack, and
a creature "walk to this point" lure hook |`

## 8. Fidelity: what this deviates from, and how it sits beside OSI's traps

**This is ours.** Register one D-number for the system and list these as its rows (the overseer edits `docs\`):

| | Deviation | OSI | Ours |
|---|---|---|---|
| 1 | Player traps that fire on monsters | faction, goblin and VvV traps fire on enemy players only (section A.3) | monsters only, players never (a Felucca switch, off) |
| 2 | Remove Trap arms traps | disarm only (`Skills/RemoveTrap.cs`) | arms, disarms and salvages; gains on sets and hits |
| 3 | Poisoning loads a gas trap | weapons, food, darts, shuriken (`Poisoning.cs:59-73`) | plus the gas trap, same windows |
| 4 | Trap damage is the owner's | the goblin trap damages the victim from the victim (`GoblinFloorTrap.cs:53`) | from the owner, so credit flows |
| 5 | Eight new Tinkering recipes | dart, poison, explosion container traps (`DefTinkering.cs:430-450`) | the container traps stay exactly as they are; the kits are new rows beside them |
| 6 | The owner sees an invisible item | `Visible = false` is staff-only (`Item.cs:471`) | a `CanSeeStaffOnly` override for owner and party |
| 7 | Rootdeep floor traps | stock classes in OSI dungeons | the same classes in our dungeon: not a behaviour deviation, a placement |
| 8 | Den rank gates bosses | no OSI rule | Master, as monster stealing (P142) |

**OSI's container traps are untouched:** Tinkering's dart, poison and explosion traps on lockable chests, Magic Trap
and Magic Untrap, Remove Trap's disarm check at power to power + 30, the GM damage cap already decided. A deployable
and a container trap never share a class; the only shared piece is the Detect Hidden reveal window (10 s), which
pinned already applies to every invisible `BaseTrap` (`DetectHidden.cs:234-252`), and the goblin kit's placement
refusals (guard zone, mounted, flying, 2-tile reach), reused for their clilocs.

**Wiki debt** (the fidelity principle's price): one page, "Deployable traps", with the table in section 3 and the
rules in sections 4 and 5. Nothing else a player reads on UOGuide changes.

## 9. What the build prompt must contain (so the decisions turn into code)

- Types: `TrapKit : Item` (kind, charges, exceptional, practice flag, crafter) and `DeployedTrap : Item` (kind, owner,
  charges left, armed at, placed hidden, concealment, quality; `HandlesOnMovement`, `Visible = false`, `Movable = false`,
  a `CanSeeStaffOnly` override), both serialized at version 0 with a round-trip test with every field non-default.
- `DefTinkering` additions through `TinkeringCraftRegistrations.cs` (our registration file, skills-design.md:525-526):
  eight rows with the gates and ingredients in section 3.
- The Remove Trap skill handler gains a kit branch before the container branch (pinned's handler stays; ours is a
  patch or a wrapper, decided in the build with the patch-backlog rules).
- Settings: `traps.pvp` (false), `traps.presenceRange` (12), `traps.decayMinutes` (30), `traps.areaCap` (6 within 8).
- Rootdeep: eight seeder rows (6.1), the `burrows.trap` station and the practice net (6.2), `[ClusterFSeedRootdeep
  dryrun` as the placement command.
- Tests the build must see red first: the trigger filter (player, pet, summon, flyer, boss below Master, dormant owner
  at 13 tiles, spotted by a DH creature), the credit (owner in `DamageEntries`, rights at the threshold), the charge
  and decay clocks, the area cap, the refusals (guard zone, door tile, teleporter, mounted), the hidden set's stealth
  step, the round trips.
- Play-test items: the bear trap art at 0xB2C5 in TazUO; a hidden set staying hidden; a net on a Penny Rat in The
  Stacks; the alarm line's coordinates.

## 10. Tests

None: design only, no code. The list above is the build's test list.

## 11. Deviations in how the work was done, and decisions for Chase

1. **The source trees were missing on this PC.** `D:\UO\ModernUO-pinned` and `D:\UO\ServUO-pub57` were not present on
   the Gold Golem's PC (the join kit's path list marks both "clone when the PC takes server prompts",
   `golem-paths.json` entries at lines 611-640). I cloned both from GitHub: ModernUO checked out at
   `d4531cd94b739613155225c234900de9f47d2c88` (4,214 `.cs` files under `Projects`, the AGENTS.md count), ServUO's `pub57`
   branch at `d76bf4443cf76d081ddaf8f57c87ff33749256af` (6,144 `.cs` under `Scripts`), shallow. Both are read-only
   sources; neither is in a repo. If Chase's own ServUO copy is a different pub57 commit, ServUO line numbers here may
   drift by a few lines; pinned ones will not.
2. **`ART-LIBRARY.md` and `D:\UO\third-party\servuo-ideas.md` do not exist on this PC** (searched D:\UO and
   D:\ShatteredLegacy to depth 5; `D:\UO\third-party` holds only `code\`). The art check used the client's tiledata and
   P50/P152's notes instead, and the wishlist line is written in 7.4 for whoever holds the file. **Decision:** should
   the join kit carry `ART-LIBRARY.md` and `servuo-ideas.md` (or the whole `D:\UO\third-party`) so a Golem on another
   PC can read and append them?
3. **The vseUOAware MCP server ignores the output path** on `render_art_tile` and writes to
   `D:\UO\tools\vseUOAware\exports\Art\`; the renders were moved into `notes\art\deployable-traps\` by hand (24 PNGs,
   8.4 KB the largest). Its `get_localized_string` finds nothing in this client's `Cliloc.enu` (the 7.0.117 cliloc is
   the newer compressed format); cliloc texts above are from the source comments.
4. **No task list tool exists in this session**, so progress was not posted as tasks; the Golem hand-off asked for it.
5. **Two unverified items for the build:** whether TazUO draws statics at ids above 0x8000 (the bear trap), and the
   exact pinned behaviour of `Frozen` on a creature mid-attack (the spider web uses it on players; the build tests it
   on a `BaseCreature`).
6. Decisions D1 to D7 at the top.

## For Chase

- The decision table at the top is the whole ask. The recommendation column is one coherent system; swapping a row
  (say, Tinkering sets as well as crafts) changes section 1 only.
- Two cheap wins to approve on their own: the eight Rootdeep floor traps (6.1) are seeder rows with no code and can
  ride the next map batch; the bear-trap art check (`[add Static 0xB2C5` on the test shard) takes a minute and decides
  whether the shard's best-looking trap costs nothing.
- Money: four art requests plus icons at P152's rates; nothing else costs anything but a build prompt.
- The wishlist line (7.4) and the two missing files (11.2) want a minute on your PC.

## 12. Repo size

The largest new file is `notes\art\deployable-traps\stock-0x11B7-boulder-trap.png` at 8,416 bytes; 24 PNGs, 30 KB in
all. Nothing near 5 MB; no scratch in either repo (the session scratchpad holds the draft sections).

## 13. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, result table pasted below
after the final run.

Second run, after the notes were written (the first run, before them, read the same for code):

```
Repo Result
---- ------
code clean
docs dry run
```

Docs: 25 files pending (the notes file and the 24 renders under `notes\art\deployable-traps\`), "dry run: would
add, commit and push". Code: "nothing to commit". No BLOCKED, no REFUSING lines. (Section A, the engine reference,
follows; the DONE line is the file's last line, after it.)

---

## A. How traps work today (pinned ModernUO d4531cd9, cited file:line under `Projects\UOContent` unless marked `Server/`)

### A.1 Container traps (OSI's only player-made trap)

- Types: None, MagicTrap, ExplosionTrap, DartTrap, PoisonTrap (`Items/Containers/TrappableContainer.cs:6-13`); fields
  TrapLevel, TrapPower, TrapType (`:20-28`). Opening fires the trap and the box only opens if nothing fired (`:67-73`);
  Telekinesis fires it too (`:36-45`); a lockpick fires it when `TrapOnLockpick` is set (`LockableContainer.cs:94-103`).
- `ExecuteTrap` (`TrappableContainer.ExecuteTrap.cs`): only the opener is ever hit, there is no area in any branch;
  staff at GameMaster and up open it unharmed and the trap stays (`:15-19`); after firing the trap is cleared, so it is
  single-use (`:49-51`). Explosion: in range 3, `RandomMinMax(10,30) * level` as 100 percent fire, effect 0x36BD, sound
  0x307 (`:56-80`). Dart: range 3, `RandomMinMax(5,15) * level` physical, sound 0x223 (`:103-116`). Poison: range 3,
  `Poison.GetPoison(clamp(level-1, 0, 4))`, so level 1 is Lesser and level 5 and up is Lethal, effect 0x113A, sound
  0x231 (`:119-144`). Magic: range 1, `Damage(TrapPower)` unresisted (`:83-100`).
- Tinkering makes them (`Engines/Craft/DefTinkering.cs`): dart 30-80 (1 iron ingot + 1 bolt, `:430-432`), poison 30-80
  (ingot + any poison potion, `:434-436`), explosion 55-105 (ingot + any explosion potion, `:438-450`). The target must be
  a lockable, movable, unlocked, untrapped container you may access, within 2 tiles (`Verify`, `:617-648`). Level =
  `(int)(Tinkering / 10)`, power = level x 9, armed only once the chest is locked (`:672-688`). Faction trap deeds and the
  removal kit sit at `:452-525` (dead code on this shard: no factions). Gears and springs are Tinkering parts at 5-55
  from 2 ingots (`:270, :273`).
- Remove Trap (`Skills/RemoveTrap.cs`): needs Lockpicking 50 and Detect Hidden 50 (`:17-21`), 10 s delay (`:31`), range 2
  (`:36`), check `CheckTargetSkill(RemoveTrap, targ, TrapPower, TrapPower + 30)` (`:61`), failure never sets it off
  (`:70`). Magic Trap sets power 10-50 and level 0 (`Spells/Second/MagicTrap.cs:37-39`); Magic Untrap clears a None or
  Magic trap with no skill check (`Spells/Second/RemoveTrap.cs:24-49`).
- The shard's decision on these (skills-design.md "55. Tinkering", decided 2026-10-02 12:50): damage caps at the GM value
  (built as level 12, `ClusterFSkillClamps.cs:86-96`), power keeps scaling to 200, and "new non-lethal trap types at 150
  and 200, for example an alarm trap and a binding trap" are noted for later. The deployable alarm and shackle are
  those two ideas on the floor; the container versions stay a later Tinkering row.

### A.2 Floor traps (`Items/Traps/`, the OSI dungeon hazards)

`BaseTrap` sets `Movable = false` (`BaseTrap.cs:11`), `HandlesOnMovement => true` (`:18`), and a Z window of
`Z + 8 >= loc.Z && loc.Z + 16 > Z` (`:39-41`). It fires on the step that enters its own tile when the reset has
passed, and, if `PassivelyTriggered`, on the step that enters `PassiveTriggerRange` (`:43-65`). BaseTrap itself has no
player or creature filter; each subclass filters.

| Trap | Ids | Trigger | Who | Damage | Reset |
|---|---|---|---|---|---|
| FireColumnTrap | 0x1B71 | passive range 3, 2 s delay | anyone alive at range 0, creatures included (`:38, :48`) | 10-40 fire (`:25-26, :50-54`) | 0.5 s |
| FlameSpurtTrap | 0x1B71, `Visible = false` (`:16`) | OnMoveOver plus range-1 edge | players only (`:111-116, :133`) | 1-30 / 1-10 | 1 s refresh |
| GasTrap | 0x113C, 0x1147, 0x11A8 (`:36-57`) | step on the tile | players only (`:64`) | its Poison, default Lesser (`:21`) | none |
| GiantSpikeTrap | id 1 (`:11`) | passive range 3 | anyone alive at range 0 (`:22, :29`) | `Dice(10,7)` (`:31`), effect 0x1D99 | none |
| MushroomTrap | 0x1125 armed, 0x1126 fired (`:12, :28`) | passive range 2 | any living non-staff mobile (`:23`) | `Dice(2,4)` (`:31`) | 2 s (`:33, :40`) |
| SawTrap | 0x1103, 0x1116, 0x11AC, 0x11B1 (`:28-48`) | step on the tile | alive, non-staff (`:54`) | 5-15 (`:62`), sound 0x21C | none |
| SpikeTrap | 4360, 4379, 4506, 4512 and +5/+6 extended (`:28-84`) | step on the tile | every Player-access mobile on the tile (`:97-102`) | `RandomMinMax(1,6) * 6` (`:108`), sound 0x22C | 6 s (`:55-58`) |
| StoneFaceTrap | 0x10F5, 0x10FC, 0x110F, firing 0x10F7, 0x10FE, 0x1111 (`:26-71`) | passive range 2 | alive, non-staff, range 1 (`:78, :99-101`) | `Dice(3,15)` (`:110`) | 2 s |

Detect Hidden reveals an invisible `BaseTrap` for 10 s, and on HS and later only at skill 75 and up
(`Skills/DetectHidden.cs:234-252`). A trapped container targeted directly gets a private "[trapped]" (cliloc 500813)
on a 0-100 check (`:147-163`).

### A.3 The OSI precedents for a player-placed floor trap (ServUO pub57 `d76bf444`, `Scripts\`, port source only)

- **Goblin floor trap kit** (Publish 70, `Items/Functional/GoblinFloorTrap.cs`): a quest reward (Tobin, `Mobiles/NPCs/
  Tobin.cs:43`); needs Tinkering 80 (`:138`), not mounted or flying (`:142`), not in an enabled guarded region
  (`:146`); placed by target within 2 tiles (`:188`), the kit is consumed (`:196`); the trap is `Visible = false`, passive
  range 1, 1 s delay, 1 s reset (`:28-34`); it fires only on players (`AccessLevel == Player && Alive`) who are not the
  owner, not the owner's guild, and whom the owner may harm (`:38-49`); 50-75 physical, "You stepped onto a goblin
  trap!" (1095157), visible for 10 s with "[Trapped]" (500813), a blood splat (`:51-64`); Detect Hidden 50-100 reveals it
  (`:66-69`); no decay; Remove Trap within 3 tiles deletes it with no check (`Skills/RemoveTrap.cs:209-227`).
  Also a bug: the placement `if` at `:188` is not an `else if`, so a failed check still places (noted for the build).
- **Faction traps** (`Services/Factions/Items/Traps/`): explosion 0x11C1, gas 0x113C, saw 0x11AC, spike 0x11A0, each a
  Tinkering 65-115 deed for silver plus 10 ingots and one part (a poison potion, an explosion potion, gears, springs;
  `DefTinkering.cs:679-696`); placed at the placer's feet, instantly, "You arm the trap and carefully hide it from view"
  (1010360, `BaseFactionTrapDeed.cs:75-85`); 15 per faction (`Faction.cs:1115-1119`); fire only on enemy-faction mobiles
  (`BaseFactionTrap.cs:340-357`); `Dice(6,10,40)` = 46-100 or Lethal poison; decay after 1 day on AOS (`:129-132`);
  revealed by Detect Hidden 80-100 and re-hidden after 1 minute (`:256-270`); disarmed with Remove Trap 80-100 and
  Tinkering 80-100 (`RemoveTrap.cs:148`).
- **Vice vs Virtue traps** (`Services/ViceVsVirtue/Items/Rewards/VvVTraps.cs`): explosion, poison, cold (5 s paralyze),
  energy (3 s mortal wound), blade (bleed), 25-50 damage; proximity range 3 or a tripwire within 3 tiles; 20 per battle
  (`VvVBattle.cs:37`) and a 30 s per-player cooldown (`VvVTrapKit.cs:55`); revealed on `Random(100) <= DetectHidden`
  (`:103`); the owner, or a `(RemoveTrap - 80) / 20` roll, gets the kit back on disarm, else 10 percent detonation
  (`RemoveTrap.cs:171-207`).
- **Bola** (`Items/Consumables/Bola.cs`): thrown at a mounted or flying target within 15 tiles, 3 s flight, 10-20 damage,
  dismount, 10 s remount block, no skill check (`:112-170`).
- **Remove Trap training kits** (Publish 97, item 0xA393, `Items/Functional/CircuitTrapTrainingKit.cs`,
  `CylinderTrapTrainingKit.cs`, `SliderTrapTrainingKit.cs`): puzzle gumps that gain Remove Trap 0-100 on a solve;
  sold by the Collector of Oddities for 99,375 gold each (`Quests/Eodon/MyrmidexThreat/Mobiles/Questers.cs:252-254`).
  P199 (the base-items remainder) is still in the queue, so they are not ported yet.

Nothing in either tree holds a snare, net, caltrop, bear trap or tripwire item; the only "throw a thing at the ground"
items are the bola and the fishing nets (`SpecialFishingNet.cs`: moved to the water, 14 ticks of 1.25 s, spawns 3-6
sea creatures). The shard's own closest thing is P121's `SpiderWebbing` (`Items/Functional/SpiderWebbing.cs:67-84`):
a web that holds a player up to 10 s with `Frozen` and lets monsters through, deleted on load.

### A.4 Hiding, Stealth, Detect Hidden and what reveals you

- Hiding is refused while your Combatant, or anyone whose Combatant you are, is within
  `min((100 - Hiding) / 2 + 8, 18)` tiles with line of sight (`Skills/Hiding.cs:53-70`); the check is
  `CheckSkill(Hiding, 0 - bonus, 100 - bonus)` (`:73`); 10 s delay.
- Stealth needs Hiding 30 on ML (`Skills/Stealth.cs:11-12`), armor of 42 or more blocks it (`:91`), the check is
  `CheckSkill(Stealth, -20 + ar*2, 60 + ar*2)` (`:96-100`), steps = `Stealth / 5` (`:102`). Running costs 2 steps and
  reveals at 0 (`Mobiles/PlayerMobile.cs:3420-3441`).
- `RevealingAction` is called by a weapon swing (`Server/Mobiles/Mobile.cs:805`), speech (`:6968`), a spell cast with
  `RevealOnCast` (`Spells/Base/Spell.cs:530-533`), potions (`BasePotion.cs:192`), bandages (`Bandage.cs:43, :74`), and 54
  UOContent files in all (Stealing, Snooping, harvesting, fields). Nothing in the engine reveals you for dropping or
  double-clicking an ordinary item: that is a design choice per item.
- Detect Hidden active: range `skill / 10` (`Skills/DetectHidden.cs:145`), per hidden mobile `skill + Random(21) - 10`
  against `Hiding + Random(21) - 10` (`:197-211`). Passive player-versus-player detection is Felucca only, 4 tiles
  (`:61-128`, `PlayerMobile.cs:3447-3464`).
- Creatures: `BaseAI.CanDetectHidden => DetectHidden > 0` (`Mobiles/AI/BaseAI/BaseAI.cs:57`); a scan every
  `min(30000 / Int, 120)` s (`AITimer.cs:225-248`) of players only (`BaseAI.cs:1142-1143`), chance
  `max(DH / 10, DH / 1.2 - min(Hiding / 2.9, Stealth / 1.8))` percent (`:1149-1151`). Creatures never scan for items.
  A trapper at Hiding 100 and Stealth 60 against a creature with Detect Hidden 50 is found 8.3 percent of the time per
  scan; against the Burrows' creatures (Detect Hidden 0) never.
- `Mobile.LastMoveTime` (`Server/Mobiles/Mobile.cs:582`, set on every step at `:4318`) exists if the build wants an idle
  clock; this design does not use one (charges and presence do the job, and a hidden trapper stands still by design).

### A.5 Poison, explosions, harm rules, kill credit

- Poisoning: a 2 s timer then `CheckTargetSkill(Poisoning, target, potion.Min, potion.Max)` (`Skills/Poisoning.cs:113-124`);
  charges `18 - level * 2` (`:133-147`); below 80 base skill a 1 in 20 failure poisons you (`:159-162`). Potion windows:
  Lesser 0-60, Regular 30-70, Greater 60-100, Deadly, Darkglow and Parasitic 95-100. Valid targets are food, fukiya darts,
  shuriken and Infectious Strike weapons (`:59-73`).
- Explosion potions: range 2 (`BaseExplosionPotion.cs:13`), 12-tile throw (`:213`), fuse 1 s then 1.25 s x 5 on ML
  (`:85-91`), hits every mobile in range the thrower may harm, the thrower included (`:160-166`), damage split by
  `targets - 1` past 2 targets (`:180-202`); Lesser 5-10, Normal 10-20, Greater 20-40, plus `Alchemy / 5` on a thrown
  detonation (`:151-155`).
- Harm: `CanBeHarmful` (`Server/Mobiles/Mobile.cs:8333-8376`) defers to `Mobile_AllowHarmful` (`Misc/Notoriety.cs:154-242`):
  on a map without `HarmfulRestrictions` "anything goes" (`:209-212`); otherwise a player may not harm another player,
  a controlled pet or a player's summon unless same guild, ally or enemy guild (`:221-239`); a creature may be harmed if
  `InitialInnocent` or not Innocent (`:241`). Only Felucca runs `FeluccaRules` (`Distribution/Data/map-definitions.json:10`);
  the other five maps are `TrammelRules`, and the shard overrides no map definition (P76). **No shard document states a
  PvP policy** (grep of docs and notes for PvP, Felucca rules, consensual, flagging: skill-math mentions only), which is
  why D4 recommends monster-only with a switch rather than a Felucca rule nobody has written.
- Kill credit: `DamageEntry.ExpireDelay` 2 minutes (`Server/Mobiles/Mobile.cs:55-59`), entries cleared at full health
  (`:2043`); a pet's damage is logged under its master as `Responsible` (`:5895-5935`, `BaseCreature.cs:3992-4006`).
  `GetLootingRights` (`BaseCreature.cs:3344-3455`): only players count, the latest damager is weighted x1.25, and the
  threshold is the top damage / 2 (under 200 hits), / 4 (200+), / 8 (1000+), / 16 (3000+). Rights holders join the
  corpse's aggressor list (`Items/Misc/Corpses/Corpse.cs:295-312`), so anyone else looting a fresh corpse is criminal for
  2 minutes (`Misc/Notoriety.cs:311-345`, `Corpse.cs:92`). The shard's loot boxes (`ClusterFLootBoxes.cs:159-185`) and
  Clean Up corpse points (`ClusterFCorpseValue.cs:60-70`) read the same rights; the Overdraft credits every damager
  (P141).

### A.6 Movement and visibility hooks a floor trap can use

- `Item.OnMoveOver` (returning false blocks the step) is called for items on the destination tile with
  `item.Z == newZ || item.Z + Height > newZ && newZ + 15 > item.Z` (`Server/Mobiles/Mobile.cs:4225-4239`); after the
  step, every item with `HandlesOnMovement` within the update range gets `OnMovement(mover, oldLocation)` (`:4394-4438`).
  Uncontrolled creatures cannot walk through a living mobile (`BaseCreature.cs:2811-2826`).
- Visibility: `Mobile.CanSee(Item)` ends in `item.Visible || item.CanSeeStaffOnly(this)` (`Server/Mobiles/Mobile.cs:7190-7229`),
  and `CanSeeStaffOnly` is virtual (`Server/Items/Item.cs:471`). So an invisible trap can override it to show itself to
  its owner (and the owner's party) with no client change. There is no `IsVisibleTo` hook; this override is the one.
  The mule's notes wanted exactly this ("owner-only needs a pinned hook", `MuleModules.cs:816-818`): it is this virtual.
- Holds: `Mobile.Frozen` (`Server/Mobiles/Mobile.cs:617`) stops movement and is not cleared by damage; `Paralyzed`
  (`:585`) is cleared at `:3683, :4771, :5988` (damage paths). The design uses `Frozen` for every hold so a held creature
  stays held while the party hits it; bleed is `BleedAttack.BeginBleed(m, from)` (`Items/Weapons/Abilities/BleedAttack.cs:61`).
- Creature flags for resistances: `PoisonImmune` (`BaseCreature.cs:972`, paragons +1 level `:1932-1933`), `CanFly`
  (`:993`) and `Mobile.Flying` (`Server/Mobiles/Mobile.cs:1193`), `IsParagon` (`:930`), `IsMonster` (`:3335`), bosses as
  `BaseChampion` (`Mobiles/Special/BaseChampion.cs:11`). There is no `IsBoss` flag in pinned; the shard's own markers
  (`ClusterFLootBoxes.IsBoss`, `ThievesDenStealRules.IsBoss`) are the ones to use.
- Tiledata: the server reads 0x10000 item entries from a 7.0.9.0 or newer `tiledata.mul` (`Server/TileData.cs:288-317`),
  so art ids above 0x8000 (the bear trap) are known to the server.

P201 DONE
