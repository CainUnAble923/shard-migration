# Companions, squires, and evo pets

Draft checked against project notes and source code on October 21, 2026. Features still to come are marked (planned). Running-shard availability and settings have not been checked. Configurable numbers below are source defaults.

## Choose your traveling partner

| Kind | What it does |
|---|---|
| Evo starter pet | An animal that earns its own combat XP and changes form as it evolves. It arrives bonded and costs 1 follower slot at every stage. |
| Ordinary tamed pet | An animal you control through Animal Taming. Eligible species can also use Animal Training to improve stats and abilities. |
| Squire or humanoid companion (planned) | An equipped adventuring partner with a class path, personality, ranks, and its own loops. The groundwork exists, but player hiring and promotion are not built. |
| Mount | A rideable creature, or a reward figurine that summons a mount. Riding uses follower capacity too. |

Your starter animal stays with you after the tutorial. Its evolution is separate from ordinary Animal Training and from the planned companion ranks.

## Getting your starter pet

The tutorial farm's Farmhand, **Wren Tallow**, offers a dog or cat during the animal lesson. The farm lesson is built, but its latest build note leaves world placement and a play-through pending. Its availability has not been verified for this draft.

Graduation offers a **dog, cat, fox, or bird** if your account did not already take its farm pet. Taking a dog or cat at the farm removes that graduation offer. These are alternative ways to receive the tutorial pet.

Keep a follower slot free before choosing. Your pet arrives bonded, follows you, and opens a color choice. Pick natural, shadow, snow, rust, sand, storm, or ember. The choice is permanent and carries through later forms.

If you close a color choice without picking, double-click your pet to reopen it. The same applies when a later evolution is waiting for a body choice. Choose carefully: players cannot change a saved body choice.

## How evolution works

An evo pet earns XP from creatures it helped damage and kill. Its share of the damage and the defeated creature's Fame affect the award. Following without fighting earns no evolution XP.

XP accumulates across stages. A new stage changes the pet's body and stats, heals it fully, and brings an Echo message. Skills it already learned above that stage's starting values are kept.

The intended roles are dog as protector, cat as striker, fox as trickster, and bird as scout **(planned)**. Their special role abilities are not built. All four currently use melee combat and the same stat curve for a given stage number.

### Forms

Stage numbers stay the same even when a form is still missing. Forms marked (planned) are skipped for now; the pet still needs the requirements of the next enabled stage.

| Stage | Dog | Cat | Fox | Bird |
|---|---|---|---|---|
| 1 | Pup: dog | Kitten: cat | Kit: small fox | Chick: crane |
| 2 | Young hound: leather wolf | Cub: baby tiger | Larger fox (planned) | Firebird: phoenix bird |
| 3 | Hound: choose a breed | Great cat: choose tiger or lion | Bake kitsune | Great bird (planned) |
| 4 | Guardian hound: cu sidhe | Sabertooth | Kitsune with a human follow form (planned) | Griffin (planned) |
| 5 | Windrunner | Manticore | No stage 5 listed | Hiryu: lesser hiryu |

The dog's stage 3 choices are Alaskan malamute, Great Dane, Saint Bernard, Newfoundland, Rottweiler, and Black Russian terrier. They are appearance choices within one stage.

The fox's planned final form can shift between a fighting fox and a woman with fox ears and one tail. Shapeshifting is not built.

### Requirements and current stopping points

| Stage entered | Total pet XP | Additional requirements in the stage rules |
|---|---:|---|
| 2 | 500 | None for enabled forms. |
| 3 | 3,000 | Dog or cat body choice; fox also requires owner loop 1. |
| 4 | 13,000 | Dog and cat require owner loop 1. The planned fox capstone requires owner loop 5 and the Bond Trial. |
| 5 | 53,000 | Owner loop 5 and the Bond Trial. |

**The loop requirements are not connected to player progression yet.** Tutorial graduation records your first loop, but pets still treat their owners as having no loops. The **Bond Trial (planned)** is also unavailable. Ordinary player progression therefore currently stops at **dog stage 3, cat stage 3, fox stage 1, and bird stage 2**.

The later dog, cat, bake kitsune, and hiryu forms have stage rules and bodies built, but their requirements prevent normal access. The missing fox and bird forms need further work as well. More XP alone does not bypass a loop requirement or the Bond Trial.

Keeping the pet's stage, XP, color, and choices through your future loop resets is decided. Full player loop resets are still (planned).

## Commands, care, and follower slots

Speak near your pets to give ordinary orders:

| Say | Result |
|---|---|
| `all follow me` | Your pets follow you. |
| `all come` | Calls your pets toward you. |
| `all stay` | Leaves them where they are. |
| `all attack` | Starts an attack order with a target choice. |

Bandages on these animals use **Veterinary and Animal Lore**. A bonded animal can become a ghost on death and be resurrected by a suitably skilled healer. Bonding does not make it invulnerable.

Animal Trainers provide stabling and claiming for ordinary pets. Stable storage is separate from the follower capacity used by animals traveling with you. Avoid releasing an evo starter pet: released evo pets cannot be tamed again.

The normal starting follower capacity is **5 slots**. Count slot costs rather than heads. For example, a starter pet and a normal horse use 2 slots together.

| Follower | Slot use |
|---|---|
| Evo starter pet | 1 at every stage. |
| Ordinary pet or living mount | Its own slot cost; Animal Training can increase it. Riding does not free those slots. |
| Compact Mule | 1, reduced to 0 with Trailwise Tack III. |
| Veteran reward mount figurine | 1 while ridden; no follower slot while put away. |
| Humanoid companion (planned) | Current draft costs are 1, 1, 2, 2, 3, 3 across ranks 0 through 5. |

Later companion limits and follower-capacity increases with loops are (planned). Graduation currently leaves those systems at their starting loop settings.

## Training an ordinary pet

Animal Training is built for eligible pets. **Evo starter pets and Compact Mules do not use it.** Their growth comes from evolution or mule upgrades instead. Some ordinary tameable species cannot train further either.

Use **Animal Lore** on your pet to inspect its attributes, skills, abilities, taming requirement, and Pet Slots range. When eligible, its window offers **Begin Animal Training**.

| Step | What to do |
|---|---|
| Begin | Choose Begin Animal Training. |
| Practice | Fight suitable creatures with your pet. Watch Pet Training Progress or open its progress tracker. |
| Choose | At 100 percent progress, open Pet Training Options and read the control-slot warning. |
| Spend | Choose an available improvement, set its value, press Train Pet, and confirm. Do this out of combat, with your pet nearby. |

The pet's species limits its training choices. Points can improve stats, resistances, and supported abilities, or raise eligible skill caps. Raising a skill cap needs the matching Power Scroll in the main level of your backpack; practice still raises the skill itself.

The first purchase in a training round adds a control slot. Training also raises the pet's taming requirement. Leave room in your follower allowance and check the new requirement before committing. Training stops offering new rounds when the pet reaches its slot maximum.

The **PLAN** window lets you enable planning, add proposed improvements, inspect their costs, and remove entries before spending. Planning does not itself apply the improvements. Canceling a training process removes its remaining points.

### Helping pet skills improve

Practicing a pet's skills is separate from filling its Animal Training bar or earning evo XP. Animal Lore's skill pages show **Learns x...**, the owner's extra multiplier on the pet's chance to gain skill.

Animal Taming and Animal Lore above 100, counted up to 200 each, improve that chance. Worn skill bonuses count. Membership and rank in the Rangers' League, also called the Outriders, add more.

| Owner, with no loop bonus | Extra gain-chance multiplier |
|---|---:|
| Taming and Lore at 100, no Outriders rank bonus | x1.00 |
| Taming and Lore at 120, no rank bonus | x1.16 |
| Taming and Lore at 200, no rank bonus | x1.80 |
| Taming and Lore at 200, Legendary Outrider | x2.40 |

This makes gains more likely. It does not guarantee a fixed learning time, give larger skill increases, or speed stat gains. A further loop bonus up to the system's x3 cap is **(planned)**; graduation does not activate it yet.

## Squires and companion ranks (planned)

Companions are intended to let you build an adventuring party. Player hiring, a candidate board, class development, promotion, and their own loop actions remain (planned). The current groundwork is not a finished recruitment service.

The starter paths are **Blade, Bow, Arcane, Support, and Rogue**. The design gives them melee, archery, magic, healing or support, and rogue roles respectively. You choose a path; personality is fixed for the companion's life. Later branch choices and their abilities are (planned).

The rank track starts at **Squire** and ends at **Legend**. Current draft slot costs are:

| Companion rank | Slots each |
|---|---:|
| 0, Squire; and 1 | 1 |
| 2 and 3 | 2 |
| 4 and 5, ending at Legend | 3 |

How those ranks fit the newer player loop ladder remains unsettled. Do not read the rank numbers as player loop numbers.

The companion's level ceiling follows its own loop: 50 at loop 0, 100 at loop 1, then 5 more per loop, reaching 200 at loop 21. Its individual skill caps follow that ceiling in the built groundwork. The player actions that earn those levels and loops are (planned).

The decided design gives companions their own progress. They keep rank and strength when you reset, but cannot loop beyond the loops you have completed. The full party is intended to be **you plus 5 companions**, sharing follower capacity with pets and mounts.

Leaving and returning with the owner at logout and login is built in the groundwork. Inn rooms, courier-pigeon services, and companion riding are (planned). All class paths are intended to ride living and ethereal mounts when that work is built.

## Mounts and the Compact Mule

A living mount remains a pet while you ride it, with its own care and follower cost. An evo pet that looks like a cu sidhe or hiryu does not become rideable: the starter evo animals have no riding feature.

The **Compact Mule** is both a pack animal and a mount. At **Dull Copper League rank**, take **The Compact's Mule** errand from the League Registrar in New Haven. Deliver **50 Iron Ore and 25 Iron Ingots**, then collect your bonded mule with a follower slot free.

Its upgrade path runs Compact, Bronzeback, Shadowhide, Valorite-Barded, and Celestial. The **Civic Mule Exchange** handles upgrades. Mule tiers are independent of your loops. Guild modules fit into its module slots; Trailwise Tack III removes its follower-slot cost. Double-clicking your mule while riding opens its pack.

Steady Hoof Wraps' dismount resistance is **(planned)**. The broader new monster, wildlife, trap, and low-ceiling dismount systems are also **(planned)**.

### Veteran reward mounts

Veteran rewards use **real account age**, separately from League rank, AP, and Renown. The source default is **30 days per reward level**. When you have an unused reward choice, the login notice opens the selection menu. Claiming a mount spends a reward choice.

| Reward level | Account age at the default interval | Mount choices added |
|---|---:|---|
| 3 | 90 days | Ethereal horse, ostard, llama |
| 4 | 120 days | Ethereal kirin, unicorn, ridgeback |
| 5 | 150 days | Ethereal swamp dragon, beetle |
| 9 | 270 days | Rideable polar bear reward figurine |
| 10 | 300 days | Ethereal cu sidhe |
| 11 | 330 days | Ethereal reptalon |
| 12 | 360 days | Ethereal hiryu |

Carry the figurine and double-click it to summon and ride. These are blessed items rather than living pets to feed or resurrect. You need a free follower slot to summon one. A reward-marked mount checks the rider's account age too, so receiving one does not remove its age requirement.

### Boss reward statuettes

Boss reward code also includes these living mounts. Access to their encounters on the running shard has not been verified.

| Boss | Possible reward |
|---|---|
| Chief Paroxysmus | Paroxysmus' Swamp Dragon statuette |
| Monstrous Interred Grizzle | Grizzled Mare statuette |

Double-click the statuette in your backpack and confirm to release its bonded mount. This consumes the statuette after a successful summoning and needs enough follower capacity. These mounts disappear if you release them from your control. They are different from reusable veteran reward figurines.

## Sources

Links are relative to the shard-migration repository. Code paths name files in ShatteredLegacy or the pinned ModernUO source. Detailed file and line evidence is in the [P389 work notes](../cc-P389-guide-companions-and-evo-pets.md).

- [League guide](league.md) and [Society of Smiths guide](society-of-smiths.md): format and related services.
- [Feature queue](../../docs/feature-queue.md), F-12, F-13, F-33, F-35, and F-39: loop, party, starter-pet, mule, reward, and dismount decisions.
- [P41](../cc-P41-companions-research.md), [P45](../cc-P45-companion-probes.md), and [companion design](../../docs/companions/companions-squire-evo-research.md): companion research and planned behavior. [P369](../cc-P369-cont-fixup-companions-b1-base-and-record.md) records the built groundwork.
- [P59](../cc-P59-evo-pet-body-sheet.md) and [P65](../cc-P65-evo-pets-framework.md): body research, evolution, choices, and unfinished stages.
- [P80](../cc-P80-new-player-tutorial.md), [P276](../cc-P276-tutorial-farm-build.md), and [P371](../cc-P371-graduation-is-the-first-loop.md): tutorial acquisition and graduation.
- [P120](../cc-P120-port-pet-training.md), [P121](../cc-P121-pet-ability-core.md), [P130](../cc-P130-pet-training.md), and [P172](../cc-P172-pet-gain-speed.md): training and skill gains.
- [P129](../cc-P129-port-creatures-part2.md): boss creatures and their reward statuettes.
- [P69](../cc-P69-mule-core.md), [P70](../cc-P70-mule-modules.md), and [P234](../cc-P234-dismount-sources-design.md): mule progression, modules, and planned dismount work.
- Current shard code: `server/customizations/Mobiles/Evo/`, `Companions/`, `Tutorial/`, `Services/Pet Training/`, `ClusterFPetGainSpeed.cs`, `PackMule.cs`, and `Mobiles/Mule/`, with their matching verification files under `server/tests/` and applicable patches under `server/patches/`.
- Boss rewards: `server/customizations/Mobiles/Bosses/ChiefParoxysmus.cs`, `MonstrousInterredGrizzle.cs`, `Items/Addons/ParoxysmusSwampDragonStatuette.cs`, and `Mobiles/Normal/ParoxysmusSwampDragon.cs`.
- Pinned ModernUO: `Projects/UOContent/Engines/Veteran Rewards/`, `Mobiles/Animals/Mounts/Ethereals.cs`, `BaseMount.cs`, `GrizzledMare.cs`, `Items/Special/ML/` statuette code, `Gumps/ConfirmBreakCrystalGump.cs`, pet speech handling, bandaging, and Animal Trainer code.

## Contradictions

These differences remain on record without deciding between the sources.

- **Pet naming:** the graduation picker says "Choose your companion". F-35 and the evo implementation treat the starter animal as a plain pet, separately from humanoid companions.
- **Loop access:** P371 records graduation as loop 1. Pet evolution, pet learning bonuses, and companion capacity still read separate, unconnected loop sources as zero.
- **Ranks and loops:** the early companion design gives one rank per loop on a six-step ladder. Current groundwork has separate rank and loop fields and the newer ladder ending at loop 21; the rank mapping remains open.
- **Party budget:** P41's addendum uses 4 companions and a final evolution mount costing 4 slots. The companion design and current groundwork use 5 companions; P47's follower curve reserves a placeholder 3 slots for an evolution mount. The separate evolution mount is not built.
- **Bird and fox forms:** P59 proposed a peacock stage and a three-stage fox line. F-35's later picks and P65's table use a phoenix bird and a separate fourth fox stage. Several table entries remain pending rather than available evolutions.
- **Reward labels:** the veteran menu and item labels retain year-based wording, while the source default and F-13 use a 30-day reward interval.
