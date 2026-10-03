# Companions: Squire + EvoMerc hybrid (research, 2026-10-02)

Written 2026-10-02 from a design chat with Chase. Status: **feature idea, not queued.** Hand to the
features chat for an F-number and to the overseer for a prompt number. Do not claim a cc-PNN here.

## What Chase asked for

- A companion that is "a pet you can equip" with player-like AI roles.
- A **hybrid of the Squire System and Xanthos EvoMerc**: "a Squire shouldn't stay a squire."
- **Companions loop like players.**
- **The point (Chase, 12:13): it lets a player build their own adventuring party of companions.**
- Decisions (Chase, 2026-10-02 11:44):
  1. **Each loop promotes the companion one rank.** Rank and loop are one track, not two.
  2. **Higher ranks cost more follower slots.**
- Decision (Chase, 2026-10-02 11:53): **squires are breedable, and one player can breed alone.**
- Decision (Chase, 2026-10-02 11:53): **the companion keeps its rank when the owner resets, and loops
  on its own.** In character, a companion **will not loop until its owner has looped that far first**
  ("not wanting to loop without you trying it first"): it says so when asked to loop early.
- Decisions (Chase, 2026-10-02 12:01):
  - **A high-rank companion stays at full strength beside a freshly reset owner.** No scaling in
    level-gated content. Carrying the owner through the re-climb is intended, with flavor speech.
  - **Breeding is designed in its own chat.** This system only marks squires as breedable and records
    the fields breeding will need (see Breeding).
- Decisions (Chase, 2026-10-02 12:04):
  - **Companions are gendered, and speech has gendered variants.**
  - **Lineages are wanted:** "lines of squires and legendary squire lineages" (for the breeding chat).
  - **Companions get personalities that set how they speak** (Chase's examples: a depressed one in the
    vein of the gloomy robot from Hitchhiker's Guide, ditzy, noble, commoner). See Personalities.
- Decisions (Chase, 2026-10-02 12:06): **personalities are speech only for now, and fixed for life.**
- Decisions (Chase, 2026-10-02 12:09):
  - **Personality passes down through lineage.**
  - **Gloomy (the mopey one) is rare. Isekai'd is extra rare.**
- Decisions (Chase, 2026-10-02 12:12 to 12:13):
  - **Agreed:** rare personalities pass down at a lower rate, with a throwback chance (for breeding).
  - **Funny PG lines when a companion is tagged to be bred**, for every personality.
  - **Classes:** once a companion takes a class it is locked in and evolves along that path.
  - **Starter paths and branches.**
  - **Class governs the companion's play style** (its AI and how it fights).
  - **Several companions per character, forming a party.**
- Decision (Chase, 2026-10-02 12:31): **the Support healing branch is Cleric, rising to Saint.**
- Decisions (Chase, 2026-10-02 12:34):
  1. **A full party is 6 including the player** (5 companions). **Add the Rogue path.**
  2. **Lower the per-companion slot costs.** A full party of 6 needs a higher-level owner; **party size
     grows with the owner's level.**
- Decisions (Chase, 2026-10-02 12:35):
  - **Map personalities to classes** ("the more I think the more we need to map personalities to
    classes"). Rare personalities unlock rare classes (12:34). This supersedes "speech only": a
    personality now also decides which classes a companion can take. Its behavior still comes from
    the class.
  - **Class titles have male and female versions.**
- Decision (Chase, 2026-10-02 12:45): **Gloomy can take all five paths**, like Isekai'd.
- Request (Chase, 2026-10-02 16:06): **companions can mount up, including on ethereal mounts** (see Mounts).
- Decisions (Chase, 2026-10-02 16:34):
  - **Mount shrinking item comes from Beastcraft** (the Shrink Potion).
- Decisions (Chase, 2026-10-02 16:45):
  - **Also a more expensive, craftable, reusable shrinking item** that squires use themselves.
  - **Training contracts: rework. Room attendant: keep** ("stabling seems inhumane"). **Carrier pigeon:
    rework. Skill instructors: rework.**
  - **Companions are bought from the League or from a board of candidates.**
  - **Death: companions become ghosts and are resurrected like players and pets.**
- Decisions (Chase, 2026-10-02 16:21): **ethereals and real mounts both; all classes ride.** A tamed mount
  given to a companion becomes its mount; re-shrinking needs a skill or item (proposed: item).
- Decision (Chase, 2026-10-02 12:56): **Penitent off any path is a possibility; Isekai'd gets a matching
  exclusive with "The Hero" as its Legend** (Otherworlder, below).
- Decision (Chase, 2026-10-02 12:52): **epithets show in the lore window or as a title** (the line under
  the name), not as part of the name.
- Decision (Chase, 2026-10-02 12:44): **when buying a companion, the buyer picks only the base class**
  (the starter path). The personality is not chosen; it rolls (see Buying a companion).

- Decisions (Chase, 2026-10-03 07:25, after the P41 research):
  1. **Logout: companions log out with their owner** (leave the world at logout, return at login).
     Never auto-stabled.
  2. **Free casting for now:** companions cast with no reagents and cannot be disturbed (engine default for
     creatures, `Spell.cs:260-263`). A recorded deviation from player parity, to revisit later.
  3. **Probe the risky classes first**, before any build (healer, bard and stealth rogue on a creature).

## Engine facts from P41 (pinned d4531cd94; spot-checked by the design chat 2026-10-03)

Full detail: `notes\cc-P41-companions-research.md`; review: `claude/p41-companions-review.md`.

- **Controlled pets run `Obey()`, not their class AI** (`AITimer.cs:149`), and on follow, come or stay they
  never fight back (`PetOrders.cs:37-39`). Every class needs our own `ForcedAI` (pattern: ours
  `DespiseMeleeAI`).
- **No pinned AI for healer, bard or stealth rogue.** `HealerAI` heals only same-`Team` creatures
  (`HealerAI.cs:138`). No `AI_Paladin` (`AIType.cs`).
- **Bushido is player-only** (`SamuraiSpell.cs:28-29`): Blademaster needs a pinned patch.
- **Parity patches needed (decided full parity 16:49):** pet gain x2 (`SkillCheck.cs:140-143`), pet stat
  delay 5 min, Bushido, resurrection loss at 2 loops with the Healing rule. Spell reagents and disturb are
  **not** patched (free casting, 07:25).
- **A companion never calls `SetDamage`** (it overrides the weapon, `BaseWeapon.cs:2430-2437`) and must get
  the player `Skills.Cap` and player hit, stamina and mana formulas.
- **Record on the companion** (`[SerializableField]`s), plus a never-reused `LineageId` for breeding.
- **Rooms: our own registry**, never pinned stabling (stabling would expose companions at Animal Trainers).
- **Mounts:** ethereal and real both ride by code; following the owner's mounted state is ours to write.
- **`ShrunkPet` has two defects** (restore drops the follow order; follower count drifts after restart) and
  cannot shrink a companion-mastered mount. Also affects Beastcraft's Shrink Potion. Route to the overseer.
- **Security:** the Squire lore gump never re-checks ownership; ours must.
- **Do not carry:** steal, peacemaking or provoke on players, looting that ignores notoriety, pigeon as an
  ownership token. Auto-loot respects notoriety and looting rights.

## Sources pulled (all in `C:\Users\ckfle\Downloads`, from servuo.dev, Chase signed in)

| File | Origin | Contents |
|---|---|---|
| `SquireSystem_2021-06.zip` | unblest, 2021-06-01, thread 12364 (newest build) | 35 .cs, about 21,900 lines |
| `EVO System.rar` | Milva, 2015-05-23, thread 2966 | Xanthos Evo framework, about 70 files |
| `Utilities.rar` | Milva, 2015-05-23 | Xanthos utilities (required by Evo) |
| `Mercenary.7z` | Jarick, 2016-06-10 | one file: `Mercenary.cs` (662 lines) |
| `Mercenary.cs` | capnblk, 2018-11-23, thread 10391 | same script with the ServUO timing fix; use this one |

Safety sweep: no network, file, process, reflection, registry or account-modifying calls in any
file. Reference source only; nothing is to be dropped in as-is.

## Findings

1. **Neither package drops in. The shard is ModernUO** (`shattered-legacy-state.md`); both are ServUO
   (RunUO-lineage) scripts. Expect a port: hand-written `Serialize`/`Deserialize` (Squire is at version
   16) versus ModernUO's generated serialization, the old gump API, `DateTime.Now` timers, and
   ServUO-only types. Treat as a rewrite that borrows behavior, not a translation.
2. **The EvoMerc download is incomplete.** `MercenarySpec` (its stage table), `MercenaryEgg` and
   `HairstylistBuyGump` exist in none of the packages. Its shrink and mount code also depends on a
   Xanthos ShrinkItem system that is not included. What it does show is the pattern: a `BaseEvo`
   subclass that earns points on melee, evolves through spec-defined stages, and takes a
   stage-based title suffix ("..., [Title] of [Owner]" at the last two stages).
3. **The Evo framework is largely breeding machinery.** Reusable here: `BaseEvoSpec` (a per-stage table
   of title, thresholds and gains) and `Evolve()` applying the next stage. That spec-table idea is the
   natural home for the class tree below. The mating, term and egg logic belongs to the breeding chat.
   Not wanted anywhere: dust, mounts, training elementals.
4. **The Squire is the body worth keeping.** `Squire : BaseCreature`, starts weak (Str 45-55, skills
   20-30 in 11 combat skills including Chivalry, Bushido, Necromancy), gains skills by use, bonded,
   3 control slots, switches to archer AI when given a bow. Large voice-command set (Chivalry and
   Bushido abilities, Provoke, Meditate), auto-heal / auto-cure / ammo pickup / flee-to-master
   toggles, looting, equipping, and lore and stats gumps. `Skills.Cap = 50000` and `StatCap = 450`
   are hard-set in the constructor; those must come from our caps instead. The package's four
   instructors (combat, healing, barding, thieving) line up with the class paths.
5. **Squire's own AI is `AIType.AI_Paladin`.** Check that type exists in `D:\UO\ModernUO-pinned`
   before assuming it (not verified here). With class governing play style, each class needs an AI.
6. **Trim candidates** (mostly flavor or vendor plumbing): `RoomAttendant` (1,049 lines) and its
   contract and SB, `SS_InnKeeper`, `CarrierPigeon`, the EC squire book, and `SquireTitle.cs` (5,403
   lines of title gump, replaced by our class titles). The four instructors may survive as class
   trainers. `SquireDialog.cs` (1,980 lines) is the model for how speech is triggered; its text is
   replaced by per-personality line sets (see Personalities).

## Hybrid shape

The F-12 ladder has six loops, one rank per loop. **Ranks come from the class tree** (below).

| Loop | Companion max level | Class step | Follower slots per companion (placeholder, lowered 12:34) |
|---|---|---|---|
| 0 | 50 | Squire of its base class (path **picked at purchase**, 12:44) | 1 |
| 1 | 100 | Path rank 1 | 1 |
| 2 | 125 | Path rank 2 | 2 |
| 3 | 150 | **Choose a branch** within the path (locked) | 2 |
| 4 | 175 | Branch rank 2 | 3 |
| 5 | 200 | Branch Legend title | 3 |

- **Same rules as players** (`f12-levels-loops-caps.md`; confirmed by Chase 16:49): individual skill cap =
  the companion's max level; a loop wipes skills and level and keeps stats; loop memory makes the
  re-climb faster; **and the same skill math as a player when using skills** (gain chance, success,
  effects).
- **Where creatures and players differ in the engine (to verify, not assumed):** creature skill gain may
  carry its own multiplier for controlled pets in `SkillCheck.cs`; stat gain may be player-only; a
  creature's melee can come from `SetDamage` instead of its weapon; F-12's per-character record and
  `ClusterFSkillCaps.Apply` are keyed to player characters; the Squire's own `Skills.Cap = 50000` and
  `StatCap = 450` must go. Each needs a companion path that matches the player one.
- **The companion loops on its own** (decided). Its loop count, class, level and skills are its own and
  are untouched when the owner resets.
- **Gate (decided): a companion's loop count can never exceed its owner's loop count.** Asked to loop
  early, the companion refuses in character.
- **No scaling after an owner reset (decided 12:01).**
- **Promotion cost mirrors players:** reaching 100 is earned; each step above 100 consumes the same
  level scroll a player would use. (Open: same scroll type, or a companion variant.)
- Pets already gain to the same cap as players (F-12 Stats), so this is consistent.

## The party (decided 12:13 and 12:34)

- **A full party is 6: the player plus 5 companions** (decided 12:34).
- **Party size grows with the owner's level** (decided 12:34); only a high-level owner fields all five.
- **Slots are the limiter.** Companions and pets share `FollowersMax`, which F-12 already ties to the
  owner's **max level** (never current level, so a reset never strands a party).
- Draft table (placeholders). `FollowersMax` is sized so the party fits when every companion is at
  the owner's own loop, which is the most it can cost (companions cannot out-loop their owner):

| Owner max level (loop) | Party size incl. player | Companions | Cost each at owner's loop | `FollowersMax` |
|---|---|---|---|---|
| 50 (0) | 3 | 2 | 1 | 2 |
| 100 (1) | 4 | 3 | 1 | 3 |
| 125 (2) | 5 | 4 | 2 | 8 |
| 150 (3) | 5 | 4 | 2 | 8 |
| 175 (4) | 6 | 5 | 3 | 15 |
| 200 (5) | 6 | 5 | 3 | 15 |

- Consequences to check: at max level 50 the cap is 2, which squeezes a new player's horse or pack
  animal. Options: a separate small mount allowance, or start the cap at 3 to 4. Stock
  `FollowersMax` is 5 and tamer pets cost 1 to 5 slots, so a tamer at 15 slots trades party members
  for pets by design. F-12 notes stable slots need their own patch (`AnimalTrainer.GetMaxStabled`).
- Group commands for a party (proposal, later): "all follow", "all guard me", "all attack", and
  class-aware ones such as "healers, heal".

## Mounts (requested 16:06: companions mount up, including ethereals)

- **Source code exists:** the Mercenary rides a mount it is given (`MountTarget`, `FindMyMount` in
  `Mercenary.cs`), and the Squire has mount handling for its archer swap. Both are ServUO and need the
  same port check as the rest.
- **Ethereal mounts are the better fit.** A ridden real mount is a creature with its own control slots,
  which eats the party's tight slot budget. An ethereal is an item, so it costs no slots and cannot die.
- **Proposal:** the owner hands the companion an ethereal (or a real mount) by drag-and-drop; the
  companion mounts when the owner mounts and dismounts when the owner does, and always dismounts where
  mounts are not allowed. A dismounted companion keeps the ethereal in its pack.
- **To verify in pinned:** whether `EtherealMount` allows a non-player rider (its use path may assume a
  `PlayerMobile`), and how a real `BaseMount` behaves when its rider is a controlled creature.
- **Decided 16:21: both ethereals and real mounts, and every class can ride.**
- **Real mount flow (Chase 16:21, details proposed):** the owner tames a mount and gives it to a
  companion; it becomes that companion's mount. Proposed rules:
  - **Free while ridden or shrunk**, so it does not eat the party slot budget.
  - **Auto-shrinks** into a figurine in the companion's pack when the companion dismounts, so no extra
    pets wander behind the party.
  - **Re-shrinking by item, not skill:** companion skills are class-locked. **Decided 16:34: the item
    comes from Beastcraft**, the Taming craft system approved in `skills-design.md` (16:30), whose
    **Shrink Potion** makes our existing `customizations\ShrunkPet.cs` figurine. Used by the owner on the
    companion's mount, or automatic on dismount as above.
  - **Reusable option (decided 16:45):** a more expensive craftable item the companion carries and uses on
    its own mount, for example a **Rider's Charm**, crafted in Beastcraft at a higher skill gate. Single
    use potions stay the cheap path; the charm is the convenience upgrade.
  - Who "owns" it in engine terms is a research question: a creature controlled by another creature is
    unusual. Fallback: the mount stays owner-controlled but is assigned to that companion.
- **Shrinking already exists in our tree:** `customizations\ShrunkPet.cs` (made today by the Outrider's
  Crook "Shrink Pet" option, Rangers system). Verify it accepts a mount assigned to a companion.
- **Backward-riding easter egg (asked 16:21):** in the client a rider always faces the same way as its
  mount, so true backward riding would need custom animation art shipped in the player package, which
  collides with the "package ships nothing of EA's" rule. Not worth it for a gag. Cheap version
  instead: on rare mount-ups a Ditzy (or Isekai'd) companion gets an emote and a line ("*mounts
  backward*" ... "Wait. Where's the head?") and a quick dismount and remount. Speech moment added.

## Classes (decided 12:12, 12:31, 12:34, 12:35; tree is a first draft)

- **Locked once taken** (decided). The path is set at purchase (12:44) and the branch at loop 3; both
  are permanent. A bred heir has no purchase, so its path choice is for the breeding chat (proposal:
  the owner picks from the heir's personality paths when it is first redeemed).
- **Class governs play style** (decided 12:12): AI, how it fights, what it prioritizes.
- **Personality decides which classes are offered** (decided 12:35; mapping below is a draft).
- **What a class does (proposal):** sets the class skill list (only those skills gain), its AI, its rank
  titles, and the abilities and commands it unlocks. Squire-stage companions train generally.
- **Choosing the branch (proposal):** at loop 3 the owner picks at a League class trainer from the
  branches its path and personality allow, with a confirmation that warns the choice is permanent.
- **Party roles:** five paths for five companion seats: tank and melee, ranged, caster, healer or
  support, and rogue.
- **Titles are gendered** (decided 12:35; see Gendered titles).

Draft tree, five starter paths, two branches each, plus two rare branches:

| Starter path (loop 1-2) | Play style | Core skills | Branch (loop 3-4) | Legend title (loop 5) |
|---|---|---|---|---|
| **Blade** (Man-at-Arms, Swordsman) | Front line, holds aggro | Swords, Macing, Fencing, Tactics, Anatomy, Parry | **Knight**: Chivalry, shield, guards the owner | Paladin |
| | | | **Blademaster**: Bushido, burst damage | Sword Saint |
| **Bow** (Archer, Marksman) | Keeps range, kites | Archery, Tactics, Anatomy | **Ranger**: tracking, hunting, wilds | Warden |
| | | | **Sharpshooter**: precision, focus fire | Deadeye |
| **Arcane** (Apprentice, Battlemage) | Back line, spells | Magery, Eval Int, Meditation, Resist | **Spellsword**: magery plus a blade | Arcane Knight |
| | | | **Necromancer**: Necromancy, Spirit Speak | Deathlord |
| **Support** (Acolyte, Medic) | Heals and cures the party | Healing, Anatomy, Resist | **Cleric** (decided 12:31): healing plus Chivalry | Saint |
| | | | **Troubadour**: Musicianship, Peacemaking, Provocation | Bard of Legend |
| **Rogue** (Cutpurse, Rogue) (added 12:34) | Flanks, strikes from stealth, opens locks and traps | Hiding, Stealth, Fencing, Poisoning, Lockpicking, Remove Trap | **Assassin**: poison, burst from stealth | Nightblade |
| | | | **Trickster**: traps, locks, distraction | Master Thief |
| (rare) | | | **Penitent** (Gloomy only; see Penitent below): pain becomes power and protection | Martyr |
| (extra rare) | | | **Otherworlder** (Isekai'd only, off any path; see Otherworlder below): cheat skill, plot armor, power of friendship | The Hero / The Heroine |

Open: the remaining branch and title names, and whether class restricts skill gain (proposed: yes).

## Squire System extras: keep or cut (explained 16:34; recommendations for Chase)

What the downloaded Squire System adds beyond a basic follower, read from the source:

| Extra | What it does | Recommendation |
|---|---|---|
| Auto-heal (self, owner, others) | Bandages on its own when someone is hurt | **Keep**, toggles per companion; Support classes do it better |
| Auto potions | Drinks heal and cure potions when needed | **Keep**, toggle |
| Ammo pickup | Picks arrows and bolts back up | **Keep** (Bow path) |
| Flee to owner | Runs to its master when near death | **Keep**, toggle |
| Auto-loot | Loots corpses, or gold and maps only | **Keep with care**: five looting companions is a lot; maybe one designated looter per party |
| Voice commands | Casts Chivalry, Bushido and Necromancy abilities, Provoke, Meditate on command | **Keep**, filtered by class |
| Skill locks in the lore window | Owner sets each skill up, down or locked | **Keep**; fits class skill lists |
| Stats spyglass, Squire care book | Item to view stats; in-game command guide | **Keep the book** as the League's companion guide; the lore window replaces the spyglass |
| Training contracts | Consumables that raise a squire's skill to a set level | **Rework (decided 16:45).** Proposal: **Drill Orders**, a League-sold consumable that gives one class skill a period of faster gain, never past the companion's previous peak or current cap, so it speeds a re-climb without skipping it |
| Room attendant and "room" command | Inn NPC that rents rooms to store squires | **Keep (decided 16:45: "stabling seems inhumane").** Companions are stored by renting an inn room, not stabled. Proposal: room slots follow the same max-level rule as F-12 stable slots, and a small daily rent comes from the bank (the stock attendant already takes gold from the bank) |
| Carrier pigeon | Calls a stored squire to you from afar | **Rework (decided 16:45).** Proposal: send a letter by pigeon to a roomed companion; it arrives at your side after a short travel delay, and the same pigeon can send a companion back to its room. The stock "sold into slavery" text is dropped |
| Skill instructors (combat, healing, barding, thieving) | NPCs that sell squire training | **Rework (decided 16:45)** as the League class trainers: one per path (Blade, Bow, Arcane, Support, Rogue), where branches are chosen and Drill Orders are sold |
| Death shroud | Item for a dead squire | **Cut**; ghosts are handled like pets |
| Title gump | Large custom title picker | **Cut**; our class titles and epithets replace it |

## Penitent, the Gloomy-only branch (draft, explained 12:52)

The fantasy: a companion so used to suffering that it turns pain into strength and takes the party's
hurts onto itself. It fits Gloomy's voice and reuses an existing UO idea, Chivalry's Noble Sacrifice
(already one of the Squire's commands).

Proposed mechanics (numbers are placeholders):
1. **Wrath of the Wounded:** the lower its health, the harder it hits (or heals, on a Support base),
   for example up to +30% at 25% health. Rewards keeping it in danger rather than safe.
2. **Shared Burden:** a share of the damage dealt to nearby party members (for example 15%) is moved to
   the Penitent instead, which feeds Wrath of the Wounded.
3. **Martyr (loop 5 Legend):** **Last Rites**, once per long cooldown: when the Martyr would die, it
   instead drops to 1 health and heals the whole party. A Gloomy Martyr is the safety net the party
   never thanks.

**Possibility (Chase, 12:56): Penitent off any path.** Gloomy reaches all five paths, so a Penitent could
keep its base path's weapons and AI and layer the mechanics above (a pain-fueled archer, mage or rogue).
The fallback is the original draft, Blade and Support only.

## Otherworlder, the Isekai'd-only branch (draft, requested 12:56: "like 'The Hero'")

The fantasy: the summoned hero of every isekai story, who arrives with an unfair gift, refuses to die
before the plot is done, and gets stronger with friends. Legend title **The Hero / The Heroine**.
Available off any path (Isekai'd reaches all five), keeping that path's weapons and AI.

Proposed mechanics (numbers are placeholders):
1. **Cheat Skill:** on taking the branch, rolls one "cheat" for life, from a short list grounded in UO:
   *Appraisal* (sees item properties and loot quality at a glance), *Item Box* (a much larger, lighter
   pack), *Fortune* (better loot luck for the party), or *Quick Study* (faster skill gain for the whole
   party). Rolled, not chosen, so two Otherworlders can differ.
2. **Plot Armor:** once per long cooldown, survives a killing blow at 1 health with a short burst of
   invulnerability. Unlike the Martyr's Last Rites it saves only itself.
3. **Power of Friendship:** a small buff for every other companion in the party, largest with a full
   party of 6.
4. **The Hero (loop 5 Legend): Protagonist Moment.** When the owner drops below a health threshold, the
   Hero gets a large temporary surge and shouts a line. Once per long cooldown.

Open: whether the cheat list is right, and whether Penitent and Otherworlder should share a cooldown rule
so a party with both is not immortal.

## Personality to class map (decided 12:35 in principle; mapping is a draft)

Proposed shape: **each common personality opens two of the five paths**, so the owner still chooses at
loop 1, but every personality has an identity. **Rare personalities open more, plus an exclusive
branch.**

| Personality | Tier | Paths it can take | Exclusive branch | Why |
|---|---|---|---|---|
| Noble | Common | Blade, Support | | Oath and honor; knights and clerics |
| Commoner | Common | Bow, Rogue | | Poacher's aim, back-alley sense |
| Devout | Common | Support, Blade | | Faith that heals, faith that fights |
| Sellsword | Common | Blade, Rogue | | Paid to fight, paid to vanish |
| Scholar | Common | Arcane, Support | | Books of spells, books of medicine |
| Braggart | Common | Blade, Bow | | Loud and in front, or loud from range |
| Ditzy | Common | Arcane, Bow | | Wild magic; accidentally great aim |
| Gloomy | **Rare** | **All five** (12:45) | **Penitent** | Suffering made useful, in any role |
| Isekai'd | **Extra rare** | **All five** | **Otherworlder** | Read every guide back home |

Path coverage across commons: Blade 4, Support 3, Bow 3, Arcane 2, Rogue 2 (both rares open all five). Roughly
27% of new companions can be Rogues and 27% Arcane, so those two seats are the hardest to fill. Tune
by swapping a path, or leave it so a good mage is a find.

### Buying a companion (decided 12:44 and 16:34)

Two sources (16:34):
- **League vendor:** buy a path contract. The buyer picks the path only; everything else rolls.
- **Board of candidates (proposal for the details):** a League notice board lists a few named recruits
  that rotate daily. Each shows name, gender and path; **personality stays hidden until hired**, so the
  12:44 rule (only the base class is chosen) holds. A candidate costs more than a contract because you
  can see the name and gender. Optional flavor: a one-line "references" hint that narrows the
  personality without naming it ("Former employer says: never stops talking about pamphlets").

Contract details:

- The buyer chooses a **path contract** (Blade, Bow, Arcane, Support or Rogue). The companion arrives
  as a Squire of that path.
- **Personality rolls** from the personalities that allow that path, keeping the tier odds (rare 5%,
  extra rare 1%, commons share the rest).
- Draft odds per contract (placeholders, from the map above):

| Contract | Possible personalities and chance |
|---|---|
| Blade | Noble, Devout, Sellsword, Braggart 23.5% each; Gloomy 5%; Isekai'd 1% |
| Bow | Commoner, Braggart, Ditzy about 31.3% each; Gloomy 5%; Isekai'd 1% |
| Arcane | Scholar, Ditzy 47% each; Gloomy 5%; Isekai'd 1% |
| Support | Noble, Devout, Scholar about 31.3% each; Gloomy 5%; Isekai'd 1% |
| Rogue | Commoner, Sellsword 47% each; Gloomy 5%; Isekai'd 1% |

- **What personality still decides for a bought companion:** its voice, its branch options (Penitent and
  Otherworlder), and the paths its heirs can take. Its second path matters only for heirs.
- **Flavor for every personality x branch combination** (requested 12:44): 46 pairings, each with an
  epithet and a signature line, in `claude/companions-combo-lines.md` (50 after Gloomy opened all paths).
- Since 12:45 both rare personalities can roll from any contract (5% and 1%).

Effects to note:
- **Personality now matters for class access.** Its behavior still comes only from the class.
- Because personality is inherited, **class access becomes a lineage trait**: a Scholar line stays a
  line of mages and healers, and a Gloomy line keeps producing Penitents. This revisits "lineage does
  not matter" (12:12): class itself is still chosen, never inherited, but the menu is.

## Gendered titles (decided 12:35; names are a draft)

Shown as male / female. One word where the title already fits both.

| Path or branch | Rank titles (male / female) | Legend (male / female) |
|---|---|---|
| Squire (loop 0) | Squire | |
| Blade | Man-at-Arms / Woman-at-Arms; Swordsman / Swordswoman | |
| Knight | Knight / Dame | Paladin |
| Blademaster | Blademaster / Blademistress | Sword Saint |
| Bow | Archer; Marksman / Markswoman | |
| Ranger | Ranger | Warden |
| Sharpshooter | Sharpshooter | Deadeye |
| Arcane | Apprentice; Battlemage | |
| Spellsword | Spellsword | Arcane Knight / Arcane Dame |
| Necromancer | Necromancer | Deathlord / Deathlady |
| Support | Acolyte; Medic | |
| Cleric | Cleric | Saint |
| Troubadour | Troubadour | Bard of Legend |
| Rogue | Cutpurse; Rogue | |
| Assassin | Assassin | Nightblade |
| Trickster | Trickster | Master Thief / Mistress Thief |
| Penitent (rare) | Penitent | Martyr |
| Otherworlder (extra rare) | Otherworlder; Summoned Hero / Summoned Heroine | The Hero / The Heroine |

## Personalities (decided 12:04 to 12:35; lines and odds are a first draft)

- **Rolled at creation, fixed for life**, stored on the companion, shown in its lore window.
- **Sets how the companion speaks and which classes it can take** (12:35). Class sets play style.
- Each personality has its own line set per trigger, with male and female variants where gendered.
- **Rarity tiers:** seven common, **Gloomy rare**, **Isekai'd extra rare**.
- **Passes down through lineage**, only at birth.
- All lines are original. Gloomy is inspired by Chase's Hitchhiker's Guide reference but uses no quotes
  or names from the book.

### Roll odds for a contract-bought companion (placeholders)

| Tier | Personalities | Chance |
|---|---|---|
| Common | Ditzy, Noble, Commoner, Devout, Sellsword, Scholar, Braggart | 94% total (about 13.4% each) |
| Rare | Gloomy | 5% |
| Extra rare | Isekai'd | 1% |

Agreed 12:12 for breeding: rare personalities pass down at a lower rate than common ones, plus a small
throwback chance to roll fresh (which is also how a rare personality can appear in a common line).

### Line table

| Personality | Tier | Voice | Asked to loop early | After the owner resets |
|---|---|---|---|---|
| Ditzy | Common | Cheerful, distracted, easily lost | "Loop? Is that the one with the hoops? Oh! After you, I meant." | "Did you get a haircut? You look... smaller." |
| Noble | Common | Formal, oath-bound, "my lord" / "my lady" | "I'll not walk that road before you have." | "I remember you strong. You will be again." |
| Commoner | Common | Farmhand plain talk, loyal | "Not 'fore you, boss. Me mum'd skin me." | "Back to the plow, then. I'll take the heavy end." |
| Devout | Common | Virtue-quoting, earnest | "Humility forbids the student passing the master." | "A rebirth! The Virtues smile on you!" |
| Sellsword | Common | Mercenary, everything has a price | "Go first? Not on my wages." | "Weaker employer, same pay. Noted." |
| Scholar | Common | Precise, footnotes everything | "Squires who loop before their masters die young. I wrote a paper." | "Remarkable. Your skills have reverted entirely." |
| Braggart | Common | Loud, boastful, secretly loyal | "Me? Loop first? I could. Easily. I'm letting you have this one." | "Don't worry, I'm strong enough for both of us." |
| Gloomy | **Rare** | Weary, sighing, sure everything ends badly | "Forget everything again? Before you? No. I'd only be miserable alone." | "You've forgotten it all. How restful that must be." |
| Isekai'd | **Extra rare** | From another world; treats Britannia like a game, talks of stats, respawns, NPCs and "back home" | "No way. You haven't cleared that loop yet. I'm not skipping the tutorial again." | "Oh, you hit New Game Plus! Okay, I'm carrying. This is literally my whole isekai arc." |

### Tagged to be bred (requested 12:12; PG, played for awkwardness)

| Personality | Lines |
|---|---|
| Ditzy | "Ooh, a baby? Do we get to pick the color?" / "Wait, is this the thing with the bees? I never understood the bees." |
| Noble | "For the good of the house, I shall... first request the honor of a dinner." / "I must write to my mother. Formally." |
| Commoner | "Right then. I'll wash behind me ears." / "Me mum'll want to meet 'em. Brace yourself." |
| Devout | "Compassion is a Virtue. I shall be very, very compassionate. Respectfully." / "I will need to pray about this. At length." |
| Sellsword | "Is this hazard pay or overtime?" / "Fine. But the kid's not getting my cut." |
| Scholar | "I've prepared a pamphlet on the subject. Several pamphlets." / "Fascinating. For science, then. Strictly for science." |
| Braggart | "Naturally. The world needs more of me." / "Tell the bards. They'll want this one for a song." |
| Gloomy (rare) | "Bring another one of me into the world? Well. Someone should know what disappointment feels like." / "I suppose I'll have to smile at the ceremony. I've been practicing. It hurts." |
| Isekai'd (extra rare) | "Wait, this game has a breeding mechanic? That explains the stables." / "Okay, this is not how dating worked back home. At all." |

More Isekai'd drafts, to seed its set:
- Idle: "I had a desk job. And a microwave. I really miss the microwave."
- Idle: "Why does everyone here talk like a Ren Faire?"
- Promotion: "Class change! Okay, okay, be cool. Be cool."
- Companion loops: "Respawn at level one. Classic. At least I keep my stats."
- Catch-up: "We're the same level now. This is the part where we get a theme song."

### Speech moments (each personality needs a set for each)

1. Asked to loop before the owner has.
2. Owner has just reset (first sight after the reset).
3. Companion loops (owner went first).
4. Promoted to a new rank (gendered class title substituted).
5. Chooses a path or branch.
6. Owner's current level catches up to the companion's after a reset.
7. Tagged to be bred (lines above; breeding chat owns when it fires).
8. Idle chatter (frequency open). With a party, companions could also banter with each other
   (later idea: a Gloomy and a Ditzy companion trading lines).
9. Mounting up (rare backward-mount gag for Ditzy and Isekai'd).
10. Likely later: combat start, low health, owner dies, companion resurrected, level up.

Earlier Noble-voice drafts kept for the Noble set:
- Loop early: "Lead and I follow. That is the oath." / "When you have gone through and come back, ask me
  again." / "A squire who outpaces his (her) knight is no squire at all."
- Owner reset: "Fresh as a new blade. Stay close; I'll keep the wolves off you." / "Your hands have
  forgotten. Mine have not. Lean on me a while." / "Start again, then. I have nowhere better to be."
- Companion loops: "You went first. Now it's my turn to forget." / "Teach me again, as you were taught."
- Promotion: "A Knight. I'll carry the name with honor." / "I was a boy (girl) with a borrowed sword when
  you found me."
- Catch-up: "There. Now we stand level again."

## Breeding (decided: breedable, solo; designed in its own chat)

This system does **not** build breeding. It only makes squires ready for it:

- **Mark squires breedable** (a flag on the companion type).
- **Give every companion a sex at creation** (decided 12:04: gendered companions).
- **Record lineage on every companion from day one:** parent 1 and parent 2 (serial or null),
  generation (0 for a contract-bought companion). A companion created before these fields exist has no
  parents to fill in, so they ship with the first build.

Handoff to the breeding chat (research already done here):
- **Stock Evo supports solo breeding.** `MatingTarget_Callback` (`EVO System/BaseEvo.cs:425-452`): when
  the female's owner also owns the male, it sets `Pregnant = true` directly; the `MatingGump` consent
  flow only runs when the male has a different owner. The female runs a `PregnancyTimer` (term from
  `spec.PregnancyTerm`, in days) and yields a `BaseEvoEgg` that hatches a new stage-0 creature, which
  inherits nothing. Both parents must be at the final stage.
- **Chase wants named lineages and legendary lines** (12:04). Ideas: a family name passed down, a
  lineage record viewable in the lore window, "legendary" status for lines with several Legend-rank
  members.
- **Personality is inherited** (12:09), with lower pass rates for rare tiers and a throwback chance
  (12:12). **Since personality maps to classes (12:35), inheriting personality passes down the class
  menu**, which makes breeding the way to build a line of mages, healers or rare Penitents.
- **Class itself is not inherited**: every heir starts as a classless Squire.
- **Tagged-to-be-bred lines** for all nine personalities are in Personalities above.
- Proposals to start from: gate on a minimum rank (for example the loop-2 step) rather than final stage;
  a **Squire's Heir contract** redeemed at the League instead of an egg; a per-parent cooldown and a
  cost to stop solo farming.
- Questions: what else an heir inherits; what parents pay; male and female required or any two; whether
  heirs can be traded (a breeding economy, which rare personalities would drive).

## Open questions for Chase

1. Class tree: the remaining branch and title names, and whether class restricts skill gain
   (proposed: yes).
2. **Personality to class map:** two paths per common personality (as drafted), or a different shape;
   the pairings themselves; the two rare branches.
3. How a companion is first obtained: bought (the Squire's 100k bonded contract), earned from a
   League quest, or both. The League is the natural home. (Answered 12:44: when buying, the buyer picks
   the base class only and the personality rolls.)
4. Party table numbers above, and whether new players get a mount allowance outside the party cap.
5. ~~Death~~ **answered 16:34:** ghosts, resurrected like players and pets (the Squire's bonded model).
   **Decided 16:49: resurrection costs skill as it does a pet, and Healing removes the loss** (the human
   counterpart of Vet removing it for pets). Companions are bonded on purchase, so they never go wild.
6. ~~Squire extras~~ **answered 16:45** (see the table). The remaining keep rows stand as proposed unless Chase changes them.
7. Address form: "my lord/lady", the owner's name, or the owner's League rank? Idle line frequency?

## Suggested next step

A **notes-only research prompt** (overseer to number it): read the Squire System, Mercenary and Evo
source from `C:\Users\ckfle\Downloads` against `D:\UO\ModernUO-pinned`; list every ServUO API they use
with its ModernUO equivalent or "missing" (cite file:line on both sides); confirm `AI_Paladin` and what
AI types pinned offers for each class's play style (melee, archer, mage, healer, bard, stealth rogue);
size the port of `Squire.cs`, `SquireFunctions.cs`, `SquireTargets.cs`, `SquireGump.cs`,
`SquireDialog.cs` and `BaseEvoSpec.cs`; propose data-driven tables for speech (personality x moment x
gender), the personality roll (tier and weight), the class tree (path, branch, skills, AI, gendered
titles), the personality to class map, and the party size and `FollowersMax` by max level, so all of
them can be edited without code changes; check how pinned handles several controlled followers at once
(commands to all, `FollowersMax`), whether `EtherealMount` and `BaseMount` accept a controlled companion as rider; and propose where the companion class, loop, personality and
lineage record lives (alongside F-12's per-character record). Breeding's Evo path (`BaseEvo.cs` mating,
`BaseEvoEgg.cs`) is sized by the breeding chat's own prompt. No build until Chase answers the open
questions and F-12's numbers settle.
