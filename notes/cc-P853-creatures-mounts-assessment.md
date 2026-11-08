# cc-P853: creatures, mounts and gear systems from the 11-07 and 11-08 scout, assessed

## In plain words

- **12 downloads were looked at:** three mounts, a Thanksgiving horn, four bosses or champion spawns, a monster
  ability kit, crafted mechanical pets, and two gear systems.
- **Worth taking:** the **Horn of Plenty**, OSI's Thanksgiving horn that gives holiday food, turkeys and a roasting
  pig. It fills an empty slot: our Clean Up Britannia reward list already names it but marks it missing. Also a
  **live ridable polar bear**, which could be the source for the ice bloodline with no new art.
- **Ideas only:** a boss that comes out after a set number of kills (fits the League dungeon dives), a dragon turtle
  boss fought from boats, a silver steed that works like a unicorn for any tamer, and crafted mechanical pets.
- **Not worth it:** the soulbound evolving weapons and the random magic gear grant far too much (the gear gives
  skill and stat points), two bosses drop power scrolls or artifacts, and the shard already has the Dread
  Warhorse, the High Seas bosses and a better monster ability system.
- **For you:** pick from the four "port first" items below. The breeding design also needs one decision from you:
  polar bear or a new ice steed for the ice line.

Iron Golem, 2026-11-08. Assessment only: no code, nothing built, run or copied out of `D:\UO\third-party`. Docs copy
`D:\UO\golems\Iron\shard-migration` on `golem/Iron/P853`; code copy `D:\UO\golems\Iron\ShatteredLegacy` read only.
`docs\` not edited. The 12 rows are now in `D:\UO\third-party\CODE-INTAKE.md` (none existed; backup
`CODE-INTAKE.md.bak-20261108-p853`).

## What was read

- Each folder's `SOURCE.txt`, README or info file, and the main `.cs` (classes, bodies, stats, loot, properties).
- **Pet breeding notes:** the claude.ai project doc `claude/pet-breeding-design-notes.md` is not on this disk, so I
  used the prompt's summary (bloodlines from nightmare, fire steed, unicorn and a new ice steed into mounts and
  mules, rare mutations, pet training), plus `design/systems/pet_progression_breeding.md` (fresh-bloodline rule,
  20% hue mutation) and the trait list in `design/companions/compact_mule.md` (Nightmare-Kin, Emberblood,
  Celestial Tempered and so on).
- **Ours, to compare:** `DreadWarhorse.cs` and `Turkey.cs` (`server/customizations/Mobiles/Normal`), the P193 High
  Seas port (`Services/Expansions/High Seas`: Osiredon, Corgul, Charybdis, `BaseSeaChampion`), the Clockwork
  Scavenger (P808), LevelGear (P261, P534), the loot boxes (P759, P763), F-24's dives (`docs/feature-queue.md`),
  `ThanksGivingFood.cs` and `CleanUpBritanniaData.cs`.
- **Pinned ModernUO** (`D:\UO\ModernUO-pinned`): `SilverSteed`, `Unicorn` (no male tamer or rider), `Kirin`,
  `Meraktus` and `TormentedMinotaur` (stock ML), the ethereal polar bear (`Ethereals.cs:499`, body and mount item
  0x3EC5), and `Mobiles/Abilities` (the MonsterAbility system).
- Body 1288 (the turtle) is `Dragon_Turtle` in our client's `mobtypes.txt` and `Bodyconv.def`.

## Every folder

Terms: no folder states a license. The scout's default applies: community work, credit the author, ship only
inside the player package or the private repo, do not repost. "Ser" counts hand-written Serialize overrides.

| Folder | What it is | Fit | Port cost | Terms | Recommendation |
|---|---|---|---|---|---|
| `dread-nightmare` (Lady Raven) | A Nightmare copy as the OSI Dread Warhorse: body 0x74/179, 3 slots, tame 107.1, flat 60 damage, +14,000 karma | Nightmare bloodline source | 1 .cs, 122 lines, 2 Ser | credit Lady Raven | **Skip.** Our `DreadWarhorse` is already the faithful port (tame 108, 20-26 damage). The flat 60 damage is a bug. Use our Dread Warhorse as the nightmare line's rare source. |
| `silver-steed` (mordredrs) | Silver steed (body 0x75) with unicorn stats, mage AI, 2 slots, tame 103.1, no gender rule | Unicorn bloodline source for male tamers (the unicorn refuses them; the kirin refuses women) | 1 .cs, 134 lines, 2 Ser; class clashes with pinned's `SilverSteed` (1 slot, animal AI) | credit mordredrs | **Idea only.** If the unicorn line should be open to every tamer, tune pinned's Silver Steed as its second source. Never a second class. |
| `ridable-polar-bear` (Milva) | Tamable ridable polar bear: body 213, mount item 0x3EC5, 1 slot, tame 29.1, 70-84 hits | Ice bloodline source; a starter cold-region mount | Small: one mount class as ours. Stock art: the ethereal polar bear uses the same body and mount item | credit Milva | **Port (rebuild as ours).** The ice line could start from a bear instead of new ice-steed art. Tame and slot numbers to set in the prompt; the download's are a starter animal's. |
| `horn-of-plenty` (Nuggzy) | OSI Thanksgiving 2012 Horn of Plenty: 10 charges, refills in November; each use gives a holiday food, a turkey, Mister Gobbles, a 10-second nap, or (9%) a Roasting Pig on a Spit deed that gives pork once a day | Clean Up Britannia reward (our data marks `HornOfPlenty = 2500.0` MISSING); an autumn item | Small: the horn, Mister Gobbles, the roasting pig addon and its two pork foods. We already have the four foods (`ThanksGivingFood.cs`) and `Turkey`. The pig is a heat source only if the craft heat table gets its art | credit Nuggzy | **Port.** It fills a hole in a built system. The horn's "refill in November" uses one timer per use; rebuild it as a date check. |
| `sea-turtle-champ` (Dweeb) | Turtle Of Doom: 4,500-hit dragon turtle (body 1288) champion meant to be fought from boats, with sea serpents and water elementals | League sea work; a sea champion | 1 .cs, 89 lines, 2 Ser. A `BaseChampion` with ML artifact lists | credit Dweeb | **Idea only.** A dragon turtle on our `BaseSeaChampion` with our own loot. The artifact lists (property artifacts) and power scrolls go. Wait for a League sea job. |
| `bone-master` (Dweeb) | The Bone Master: 4,200-hit bone demon champion; summons undead knights; power scrolls and a gold burst | Bosses | 2 .cs, 273 lines, 2 Ser | credit Dweeb | **Skip.** Power scrolls and ML artifacts. The undead-summon fight already exists as a MonsterAbility. |
| `high-seas-bosses` (Tacurumin) | Osiredon, Corgul (altar, map, minions), Charybdis (oracle, tentacles), all High Seas artifacts | Sea bosses | 40 .cs, 14.8k lines, 37 Ser; replaces BaseAI, MapItem, FishingPole and DefCooking | credit Tacurumin, Koluch, Erevan; EA bosses | **Skip.** P193 already ported all three bosses from ServUO stock. The artifacts are property artifacts. |
| `labyrinth-champion-spawn` (Denjiki) | Altar-less Labyrinth champion: 50 minotaur kills near Malas 388,1920 summon Meraktus; tormented minotaurs slam | League dives and culls | 6 .cs, 905 lines, 5 Ser. Replaces 4 stock minotaurs; a static kill counter that is not saved; Meraktus is in pinned | credit Denjiki and Gizmo | **Idea only.** The useful part is "kill N in a region and a boss comes out". F-24 wants exactly that for dives (culling, then an investigation mini boss for the party). Build it generic, keyed by region and data, not by edits to stock monsters. |
| `special-abilities` (Omni) | `BaseSpecialCreature`: teleport, nox strike, life drain, triple bolt, multi fire breath, earthquake, summons as on/off switches | Boss design | 1 .cs, 536 lines, 2 Ser | credit Omni | **Skip.** Pinned's `Mobiles/Abilities` MonsterAbility system does all of this. League bosses should use it. |
| `mechanical-pet-crafting` (Milva) | A craft system at Tinkering 110 for pre-bonded combat constructs: a 4-slot golem, a bone demon, a black widow, a frenzied ostard and a hell steed, from gears, clockwork assemblies and power crystals | Tinkers' Union | 12 .cs, 1,269 lines, 11 Ser; its own CraftSystem and tool | credit Milva | **Idea only.** No overlap with the Clockwork Scavenger (P808): the Scavenger loots and does not fight; these fight and come pre-bonded. Stock ML tinkering already makes a golem from a clockwork assembly. Keep the construct looks for a later Tinkers' Union rank, never as pre-bonded crafted pets. |
| `soulbound-evo-weapons` (JBob, from Mortis) | Sword and bow that bind on equip and grow on hits: up to 50 in hit harm, magic arrow, lightning and fireball, damage +50, 100 luck, 100 self repair, spell channeling; an unbinding deed | Levelable gear | 3 .cs, 462 lines, 3 Ser | credit JBob and Mortis | **Skip.** It grows into a property artifact far past every cap. Our LevelGear (P261) is the same idea done with caps, dormancy and Chase's P72 decisions. |
| `random-magic-gear` (thor86) | 18 "Artifact" armour, clothing, jewellery and weapon pieces with random hues, art, names, up to 7 random properties, a random artifact deed, and a "Gollum" mob | Loot | 19 .cs, 3,895 lines, 19 Ser | credit thor86; Tolkien name | **Skip.** It rolls random `SkillBonuses` (378 lines) and +Str/Dex/Int: skill and stat points. Our loot boxes (P759, P763) already roll gear by tier. |

Totals: **port 2, idea only 4, skip 6.** None that grants skill or stat points, power scrolls, bless deeds or property
artifacts is marked port: `random-magic-gear` (skill and stats), `bone-master` (power scrolls), `soulbound-evo-weapons`
and `high-seas-bosses` (property artifacts) are all skip. The turtle's artifacts and scrolls are dropped from its
idea.

## The questions the prompt asked

- **Bloodline sources:**
  - dread nightmare: **our Dread Warhorse** already fills it, as a rare nightmare-line parent;
  - silver steed: pinned's Silver Steed could be a **second unicorn-line source** for male tamers, if Chase wants
    that;
  - polar bear: a **live polar bear mount** could start the ice line instead of a new ice steed, so no new art.
- **Mechanical pets and the Clockwork Scavenger (P808, Tinkers' Union):** no overlap. They share a theme (gears,
  Tinkering) only. The Scavenger is a non-combat looter, one per character. These are bonded combat pets made by
  crafting.
- **Soulbound evo weapons and random magic gear against LevelGear and the loot boxes:** both are older, uncapped
  versions of what we built. Nothing to take; the soulbound idea (binds on equip) was already weighed in P72's
  tradeability decisions.
- **Bosses and champions for League dungeons:**
  - the Labyrinth's kill-count trigger fits the F-24 dives best (cull, then a boss);
  - the dragon turtle fits a later sea job;
  - Bone Master and the High Seas package do not.

## Port first (for the overseer to put to Chase)

1. **Horn of Plenty, Mister Gobbles and the Roasting Pig on a Spit.** *Why:* our Clean Up Britannia table already
   lists the horn at 2,500 points as missing, and the foods and turkey it hands out are built. Small: about four
   classes and facts. November is now.
2. **A live ridable polar bear.** *Why:* the cheapest ice-line source for breeding: stock art and one mount class.
   Ask Chase first: polar bear, or wait for a new ice steed?
3. **A kill-count boss trigger for League dives** (from the Labyrinth idea, rebuilt). *Why:* F-24 asks for dives that
   cull, then spawn an investigation mini boss for the party. A data-driven "kill N here, boss for this party"
   trigger serves every dive. Medium, and only once dives are queued (after F-14 and the P24 dungeon work).
4. **A dragon turtle sea champion** (from the Turtle of Doom idea). *Why:* a boat fight on our existing
   `BaseSeaChampion` with our loot. Later, when a League sea job is queued.

## Not done

- No body or mount check in the game client for the polar bear (the ethereal polar bear uses the same IDs, so it
  should work); the port prompt should ride one.
- The claude.ai breeding doc itself was not read (not on this disk); the prompt's summary was used.

P853 DONE
