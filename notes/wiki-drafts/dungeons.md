# Dungeons in Shattered Legacy

Draft checked against project notes, source code, and existing tests through October 22, 2026. Features still to come are marked (planned). Access, spawns, and settings on the running shard have not been checked.

## Start with the Rootdeep Burrows

The Rootdeep Burrows are the starter dungeon beneath Old Haven on Trammel. The entrance is a hole in the ruined Second Bank of Haven, reached through its collapsed south wall. A rope ladder inside returns you to Old Haven. The landing has an ankh.

The Vault is the tutorial section. It admits tutorial participants and their pets. Defeating the Overdraft gives participating attackers credit, including credit through their pets, and briefly opens a one-way crawlway onward. Once credited, you cannot reenter the Vault. Tutorial graduates cannot enter it either. The rest of the Burrows is separate from this tutorial-only room.

Beyond the Vault, the Burrows have burrowing creatures, living roots, stone creatures, and spiders. Named opponents include the Burrow Mother and the Gloom Queen. Expect poison, webs, and floor traps. Bring healing supplies and a way to deal with poison; take the harder fights with friends.

Young status does not make you safe here. Monsters can attack Young players. The Burrows limit the hostile creatures attacking one Young player at once to **3**, but that is protection against a crowd, not a promise that a fight is safe.

Enter physically. Recall, Sacred Journey, gates, and teleporting from outside cannot bring you in. You cannot Mark a rune inside or cast a gate out. You can walk out or Recall out, subject to the tutorial island rule below.

New characters must graduate with the League recruiter in New Haven before leaving the island under the default tutorial rules. Rootdeep counts as part of the island for this restriction. Graduation records your first loop; it currently does not reset skills or apply the planned character-level system.

The dungeon also supplies starter materials:

| Material | What it is for |
|---|---|
| Dawnstone | A starter metal, mined in the Burrows. |
| Burrowhide | Leather carved from supported Burrows creatures. |
| Rootwood | A starter wood, harvested in the Burrows. |
| Gloomsilk | Cosmetic cloth dropped by the spider family. |

Dawnstone and Rootwood harvesting require **45.0** in the matching gathering skill. Their crafting material gates, and Burrowhide's Tailoring material gate, are **45.0**. Rootwood and Gloomsilk do not add special combat bonuses. The proposed personal starter-set upgrade system is (planned); gathering these materials is not a promise of an available upgrade quest.

## Classic dungeons and the newer ports

Classic dungeon data remains part of the shard's build. Deceit, Destard, Hythloth, Fire, Ice, Orc Cave, and Terathan Keep have stock spawn definitions on both Trammel and Felucca. These are places to explore after graduation, not a level-ordered route. Felucca has different combat rules from Trammel.

The following dungeon additions are implemented. This table describes the checked build, not a confirmation that each encounter has been placed and opened on the running shard.

| Dungeon | Facet | What the build supports |
|---|---|---|
| Rootdeep Burrows | Trammel | Starter creatures, tutorial Vault, bosses, resources, traps, entrance, and exit. |
| Despise Revamped | Trammel | Wisp-orb creature control, opposing alignments, and overlord encounters. Felucca retains the classic population. |
| Shame Revamped | Trammel and Felucca | New creatures, separate treasure chests, cave-troll barriers, and guardian encounters. Player summoning of altar guardians is not enabled in the checked code. |
| Wrong Revamped | Trammel and Felucca | Prison creatures, prisoner escorts, maze features, and jail rules. A death in its lower prison area can lead to capture and resurrection in a cell. |
| Covetous and the Void Pool | Trammel and Felucca | Changed creatures, Cora, and a wave-defense encounter with scores and reward points. |
| Exodus encounter | Ilshenar; ritual begins in Trammel or Felucca | Dungeon creatures, ritual supplies, a party ritual, and Clockwork Exodus. |
| Blackthorn Dungeon | Trammel and Felucca | Dungeon creatures, Minax artifact awards, and Agent of the Crown rewards. The invasion and beacon event are (planned). |

Underworld puzzle rooms and mini champion encounters in the Stygian Abyss and Malas are unfinished additions (planned). Their player access and encounter behavior have not been verified.

In Despise, use an ankh matching your positive or negative karma to receive a wisp orb. The orb lets you control a Despise creature and build its strength. The overlords Adrian and Andros take damage from Despise creatures, so ordinary direct attacks are not the way to fight them. Stock treasure chests remain separate from the revamped creature population.

Shame's Quartz, Flame, and Wind Elemental guardians are built. However, the altar currency connection is disabled: Crystals of Shame do not currently become spendable altar points. Keep the crystals. Flame and Wind Elementals also occur as ordinary spawns, separate from summoned guardian fights.

At the Void Pool, defend the pool against incoming waves. The encounter awards its own points, and Vela in Cove offers its rewards. These points are separate from League Renown.

For Exodus, gather the Summoning Altar, Summoning Rite, Sacrificial Dagger, and Robe of Rite. Combat, stealing, and chest looting provide routes to ritual supplies. Crafting recipes are registered too, but the robe recipe's Abyssal Cloth supply remains unverified.

Build the altar at a supported virtue shrine in Trammel or Felucca while in a party. Each member must complete the rite and dagger steps and wear the robe. The altar owner begins the ritual once the party is close together. The ritual takes the party to the encounter and consumes the robes. These supplies expire, so organize the party before beginning.

Blackthorn Dungeon is reached through Castle Blackthorn in Britain. The Trammel castle restricts spells, mounts, and pets; pets may be stabled or sent outside. The dungeon itself blocks Recall, gates, and Mark, reveals hidden players, and punishes prolonged standing still with relocation and poison. Use the physical exits.

Eligible kills there can award artifacts bearing Minax's crest. Turn them in to an Agent of the Crown for Blackthorn points, then choose rewards through the Agent. This reward route is built even though the invasion event is still (planned).

## Dungeon chests, traps, and keys

A dungeon chest can be locked and trapped. Opening the lock does not mean the trap is gone. Double-click a lockpick and target a pickable chest. Bring spare picks and use Remove Trap before opening a trapped container.

These are the minimum Lockpicking requirements for **classic stock dungeon chests**, not every chest that looks like one:

| Stock chest level | Lockpicking | Trap |
|---|---:|---|
| 1 | 57.0 | Dart |
| 2 | 72.0 | Explosion |
| 3 | 84.0 | Poison |
| 4 | 92.0 | Explosion |

Meeting the requirement allows an attempt; it does not guarantee success. Under the shard's Endless Journey rules, Remove Trap does not require 50.0 Lockpicking and 50.0 Detect Hidden first. The disarm check depends on Remove Trap and the trap's power. Even 100.0 Remove Trap does not guarantee every stock level 4 trap.

Classic chests contain gold and other loot such as gems, equipment, reagents, or scrolls according to their level. They decay whether looted or untouched and are replaced by their spawners. Emptying one does not start a personal refill timer.

Shame's revamped treasure chests use a separate system, with different locks, traps, and loot. They disappear a few minutes after first opening. Do not apply the classic chest table to them. Treasure-map chests and encounter-specific chests also have their own rules.

Skeleton keys and master skeleton keys are implemented and appear in treasure-map reward tables. They are limited-use lockpicks, not universal dungeon entrance keys. Each starts with **10 successful uses**. A skeleton key lowers the minimum Lockpicking gate by 10 points and still makes a skill roll. A master skeleton key lowers the gate by 100 and succeeds on an eligible pickable lock. Neither opens an unpickable or magically locked target.

The unified dungeon-chest overhaul is (planned). Its decided features include harder locks deeper in dungeons, level 5 and 6 chests, extra currencies and rare rewards, and a **30 to 60 minute** refill timer starting on first access. Those rules are not the current behavior of all dungeon chests.

A hostile animated chest mimic has been built. Finding one through a random dungeon chest, then fighting and taming it into a PetMimic, is (planned). This draft cannot direct you to a working player acquisition route.

## Levels, loops, and League work

Creature difficulty labels and Appraisal are built. Single-clicking a creature can show a word such as **easy**, **even match**, or **deadly**. Under the default rules, that comparison uses your best combat skill as a temporary measure. It is not an earned XP level. Appraisal reveals more about a creature as the skill rises.

The broader character-level and XP system, skill resets, and loop-based caps are (planned). The tutorial already records graduation as loop 1, but it does not perform those resets. This guide therefore gives no required character levels or XP payments for dungeon kills.

Dungeon loot can help with the League's existing requisitions. Check the League office for requested equipment and any Lead before setting out. Leads can point toward suitable hunting areas, including dungeons. Turn-ins connect that loot to Renown and guild standing. See the [League guide](league.md) for the current rules.

The broader League dungeon dives are (planned): gathering, culling, and investigation jobs that can be shared with a party. Milestone story trials are also (planned). They are separate from the ordinary dungeon encounters above.

The Setting is a decided dungeon design (planned), with **20 floors** opening across loops **2 through 21**. Its final floor holds the planned epilogue, **The Unbroken**. This is not an available entrance or a reason to wait for a later loop before exploring the classic dungeons.

## Sources

Paths below are relative to the shard-migration repository. Code and existing tests were also read; file and line evidence, verification limits, and additional source paths are in the [P396 work notes](../cc-P396-guide-dungeons.md).

- [Dungeon decisions](../dungeon-decisions-2026-10-01.md), [P24 research](../cc-P24-new-haven-dungeon-research.md), and [P36 build](../cc-P36-dungeon-build-1.md): entrance choice, travel, Young rules, resources, and early starter-dungeon scope.
- [P140 creatures](../cc-P140-rootdeep-burrows.md), [P141 Vault and spawns](../cc-P141-rootdeep-burrows.md), and [P188 way in](../cc-P188-cont-rootdeep-goes-in.md): later Rootdeep content, access, and remaining client checks.
- [P49 chest research](../cc-P49-dungeon-chests-research.md) and [P50 mimic monster](../cc-P50-chest-mimic-monster.md): current chest families, decided overhaul, and the built monster's limited scope.
- [Despise](../cc4-despise.md), [Shame](../cc4-shame.md), [P194 Wrong and Covetous](../cc-P194-port-wrong-and-covetous-void.md), and [P221 integration](../cc-P221-cont-fixup-port-wrong-and-covetous-void.md): ported encounters and their limits.
- [P195 Exodus](../cc-P195-port-exodus-encounter.md), [P271 integration](../cc-P271-cont-fixup-port-exodus-encounter.md), and [P196 Blackthorn](../cc-P196-port-blackthorn-dungeon.md): rituals, encounters, rewards, and unfinished invasion work.
- [P197 Underworld and mini champions](../cc-P197-port-underworld-mini-champions.md) and [P199 base items](../cc-P199-port-base-items-remainder.md): unfinished dungeon work, skeleton keys, and the later Remove Trap patch.
- [P239 creature levels and Appraisal](../cc-P239-creature-levels-appraisal.md), [P371 first loop](../cc-P371-graduation-is-the-first-loop.md), [P150 requisitions and Leads](../cc-P150-requisitions-and-leads.md), and [P203 integration](../cc-P203-cont-fixup-requisitions-and-leads.md): current difficulty information, island graduation, and League loot turn-ins.
- [P211 dungeon-generator assessment](../cc-P211-svdungeon-070-assessment.md): a proposed tool for future dives, not an available generated dungeon service.
- [Feature queue](../../docs/feature-queue.md), F-12, F-14, F-24, F-32, F-35, F-45, F-47, and F-48: decided progression, dungeon, tutorial, and League work.
- [League](league.md) and [High Seas fishing](high-seas-fishing.md): companion drafts and the distinction between built features and unverified live access.

## Contradictions

These differences remain on record without deciding between the sources.

- **Shame points:** the older port comments say guardian points await the points framework. That framework now exists, but the Shame connection still returns no points and remains disabled. Built guardians and a built points framework do not establish enabled altar summoning.
- **Chest rules:** F-32 decides one dungeon-chest system, depth scaling, and first-access refill. P49 and the current implementations describe separate classic and Shame chest families with different locks and deletion rules.
- **Remove Trap prerequisites:** P49 reports the pinned engine's 50.0 Lockpicking and Detect Hidden requirements. The later P199 patch removes both prerequisites under Endless Journey.
- **The Burrow Mother:** P24 proposes making her the final boss of a mini champion encounter. The checked Rootdeep implementation places her as an ordinary boss spawn with her own brood behavior. The separately ported mini champion system does not put her in its encounter table.
- **Loop timing:** older F-12 passages put the Setting after a separate set of post-cap loops. The later decision places its floors on loops 2 through 21. Current tutorial code records a first loop at graduation while leaving level and skill resets unimplemented.
- **Built versus open:** P211 describes Rootdeep as built, while P188 still leaves the client walk, package publication, and world placement as separate checks or handoff steps. The source and notes do not establish which dungeon setups are currently open on the running shard.
