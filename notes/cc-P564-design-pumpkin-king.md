# P564: Pumpkin King event design and remaining build work

Written October 24, 2026. Design only. No code, configuration, world, client package, or service changed.

## What Chase gets

Use Treasures of Sorcerer's Dungeon, the OSI event represented by ServUO pub57. Players fight through a shared rotation of nine rooms in Ilshenar, collect equipment of Enchanted Origin, and trade it to the researcher for the source's rewards. Jack the Pumpkin King is the ninth boss. Keep the source's combat numbers, reward prices, and names.

**The event is already implemented in main by P408.** This is a design for finishing and verifying it, not another port. Its remaining work is encounter cleanup and kill eligibility, reward confirmation fixes, the missing Stygian Abyss artifact selection, and an isolated server and client acceptance pass. Title deeds remain a separate optional subsystem. No custom art is required.

Chase's choice is settled. The overseer's `D:\UO\overseer\decisions-2026-10-22.md:14` records his answer as "OSI Pumpkin King first" and assigns P408. The completed P408 prompt records his 09:24 choice and explicitly chooses our Halloween dates. Do not reopen the Hollow Rider, import the third-party Headless Horseman, or bring the parked Great Pumpkin into this task.

The proposed fixes below have not been implemented or run in P564. Existing implementation, prior test reports, and proposed acceptance requirements are identified separately.

## Evidence and scope

Read both work copies' AGENTS.md, the direction decision, task list, governing-document index, fidelity principle, subsystem policy, and standing questions. The named `notes/cc-P405-servuo-batch-1022-research.md` does not exist. The actual deliverable is [cc-P405-servuo-batch-1022.md](cc-P405-servuo-batch-1022.md), as the [completed P405 prompt](../../../../cc-prompts/completed/cc-P405-servuo-batch-1022-research.md) specifies. Its Bosses section identifies this event at lines 282-285. Third-party behavior is taken only from that note; no third-party download was executed, installed, extracted, or used as source code.

Also read:

- [P408 implementation and evidence](cc-P408-sorcerers-dungeon-halloween.md) and [its Codex review](cc-P408-sorcerers-dungeon-halloween-codex-review.md).
- [P461 source review](cc-P461-review-sorcerers-dungeon-halloween.md) and its review. P461 already identifies the reward, pumpkin, artifact pool, ring, and timer-coverage issues discussed below. These are follow-through work, not new P564 discoveries.
- The completed P408 and P461 prompts, and the overseer's October 22 and October 23 decisions. P564 is the later design follow-up, not evidence that P408 is absent.

Source snapshots checked locally:

| Tree | Revision and meaning |
|---|---|
| ShatteredLegacy work copy and local main | Both `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`; clean when research began |
| shard-migration work copy and local main | Both `e208e5b697b81397605711080a30484ed459c74d`; clean when research began |
| Read-only ModernUO-pinned | `d4531cd94b739613155225c234900de9f47d2c88`; clean; matches `docker/uo/Dockerfile:3` |
| Read-only ServUO-pub57 | `d76bf4443cf76d081ddaf8f57c87ff33749256af` |

Throughout this note, `event/` means `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/` in the code work copy. `ServUO event/` means the same relative folder below `D:\UO\ServUO-pub57\Scripts\`. `pinned/` means `D:\UO\ModernUO-pinned\Projects\`. Source behavior is verified against these local files, not independently against an OSI server or a current public wiki.

## What players see

1. Travel to Sorcerer's Dungeon in Ilshenar. The stock region lists an entrance at `(546,455,0)` and a dungeon go location at `(429,108,-28)` in `ModernUO-pinned/Distribution/Data/regions.json:3323`. The researcher stands outside at `(536,456,-53)`. Retain the stock travel route; no new gate, quest prerequisite, level requirement, or League currency is proposed. The actual walk through the entrance still needs a client check.
2. The entrance has the researcher and seven pieces of seasonal dressing. The researcher offers Turn In Artifacts of Enchanted Origin and Claim Rewards. This is one public event shared by players, with one active room and one progression count, not a separate instance per party.
3. The current room fills with undead. Defeating its event-spawned creatures advances the room. Other dungeon kills may earn artifacts but do not advance that room's kill count. A boss appears at the room threshold. Kill it to move to the next room after the source's delay. After Jack, the rotation returns to room one.
4. Eligible kills sometimes put a registered artifact of Enchanted Origin into the player's backpack, with a sound and message. There is no guaranteed artifact per kill or per Jack. A full backpack falls back to the bank, then the player's feet. Keep the source's behavior and explain this fallback in the player guide.
5. Hand an artifact to the researcher for one point. Points are per character. Spend them on the reward list below. The equipment is consumed on turn-in. Hue or an item name alone does not make an item redeemable.
6. When the season ends, event combat ends and the normal dungeon spawners resume. The researcher and entrance dressing remain, as in the source. Players retain their artifacts, unspent points, purchased rewards, and kill tallies. They can still redeem and spend after the season. Staff `remove` is a separate teardown that also removes the tracked researcher and dressing.

Describe Jack as a group encounter, with no claimed party size or completion time until playtesting. His 26,000 hits and retaliation make him materially different from the eight earlier bosses. Do not invent solo scaling or add the League boss-token feature here.

## Schedule and progression numbers

The event uses `clusterf.seasonal.halloween.start = "10-24"`, `.end = "11-02"`, and `.automatic = true` by default. Dates are inclusive, use the shard's local time, and repeat annually. The existing compose configuration is intended to use America/Chicago. Settings and running time zone were not inspected in a live container during P564.

`event/Generate.cs:55` borrows Halloween settings through `ClusterFSeasonalSwitch` but saves state under `sorcerersdungeon`. The switch checks on world load and hourly. Therefore the opening and closing can occur on the first hourly check after the date changes, rather than precisely at midnight. An explicit staff on or off persists through checks in the same season state, including restart; the next seasonal transition changes it again. Changing the Halloween dates also changes bank decor. Do not introduce a second independent calendar by accident.

ServUO uses October 1 for 60 days (`Scripts/Services/Seasonal Events/SeasonalEventSystem.cs:68`). Our shorter window was explicitly requested by P408. Its winter-themed bosses belong to this same rotation. ServUO's Krampus entry is a different event, not a second half to activate in December.

`event/Spawner.cs:369` and ServUO event `Spawner.cs:249` supply these room rectangles. Values are `(x,y,width,height)`, not entrance positions. Preserve the source's inclusive random-point calculation and validate candidate spawn tiles; do not silently reinterpret the far edge while fixing lifecycle behavior.

| Order | Boss | Room rectangle | Hits | Melee damage | Defining behavior |
|---|---|---|---:|---|---|
| 1 | Nightmare Fairy | `(327,26,29,32)` | 8,000 | 21-27 | Life Leech and Life Drain |
| 2 | Jack in the Box | `(296,10,17,26)` | 8,000 | 21-27 | Necromancy caster; Armor Ignore or Bleed Attack |
| 3 | Headless Elf | `(271,4,20,33)` | 8,000 | 21-27 | Wrestling Mastery; effective melee AI |
| 4 | Abominable Snowman | `(227,39,21,19)` | 8,000 | 21-27 | True Fear; Concussion Blow or Crushing Blow |
| 5 | Twisted Holiday Tree | `(251,68,25,32)` | 8,000 | 21-27 | Explosive Goo |
| 6 | Rabid Reindeer | `(144,5,23,19)` | 8,000 | 22-29 | Venomous Bite; lethal hit poison |
| 7 | Garish Gingerman | `(60,53,13,34)` | 8,000 | 21-27 | Magery Mastery |
| 8 | Stocking Serpent | `(152,48,16,23)` | 8,000 | 22-29 | Vicious Bite; lethal hit poison |
| 9 | Jack the Pumpkin King | `(291,73,37,36)` | 26,000 | 22-26 | Necromancy caster; retaliation and unholy pumpkins |

Each room requires 80 tracked regular-creature deaths and maintains up to 15 regular creatures, drawn from Zombie, Skeleton, Gargoyle, Lich, and LichLord. A regular spawn is attempted after 3-8 seconds, on a one-second controller tick; placement can fail after 20 attempts. After a boss disappears, the controller advances and waits 1-3 minutes before resuming its timer. Regular creatures can continue to refill during the boss fight under the source's conditions. Eighty is the boss trigger, not a cap on all deaths in that room.

The nine thresholds sum to 720 regular deaths for a complete rotation, plus the bosses; extra creatures can make the actual death total higher. All bosses have 12,000 fame, -12,000 karma, AlwaysMurderer, and two UltraRich loot packs. Keep their existing source values and ability profiles. The creature called Jack in the Box is `JackInTheBoxMonster` internally to avoid colliding with the reward toy; its visible name stays unchanged.

### Jack's exact contract

`event/Creatures/JackThePumpkinKing.cs:37` matches ServUO event `Creatures/JackThePumpkinKing.cs:20`:

- Strength 500, dexterity 200, intelligence 1,200; 26,000 hits; damage 22-26, 100% physical.
- Resistances: physical, fire, and cold 70-80 each; poison 60-70; energy 40-50. Immune through deadly poison.
- Skills: Anatomy 25; Resist 120; Tactics 100-110; Wrestling 130-140; Parry 20-30; Magery, Eval Int, Necromancy, Spirit Speak, and Meditation 120 each; Focus 70-80.
- Human body `0x190`, skin hue, cloth ninja hood hue 1281, bone chest/arms/gloves hue 1175, thigh boots, and scepter. He is not a custom pumpkin-headed rider.
- Each qualifying incoming damage call returns a separate 8-20 physical damage roll to the attacker, using AOS damage resolution. It is not a percentage reflect, and 8-20 is the raw roll before the victim's mitigation. The recursion guard prevents a damage loop.
- On that call, a 5% roll schedules pumpkins one second later. It attempts 1-3 pumpkins at offsets -1 to +1 around the target, with fit checks. A pumpkin hatches after 5-10 seconds into one of Skeleton, Zombie, Wraith, Spectre, Ghoul, Mummy, Bogle, RottingCorpse, BoneKnight, SkeletalKnight, Lich, or LichLord, selected uniformly.
- Carving has a 30% success chance per attempt: destroy the pumpkin and put 25-100 gold on its tile. Failure damages it only in the message. Preserve these source numbers. This is separate from P405's third-party exploding pumpkin bomb.

The lifecycle fixes must retain these mechanics while preventing an event callback from creating pumpkins outside the active dungeon encounter or after shutdown. Record that confinement as a deliberate repair of broken source behavior.

## Artifact currency and rewards

`event/SorcerersDungeonData.cs:127` and ServUO event `SorcerersDungeonData.cs:35` define the earning rules. While Enabled, a living player with looting rights to a noncontrolled, nonsummoned creature killed inside the Sorcerer's Dungeon region receives a personal tally increment:

```text
base = integer division of victim fame by 4
increment = truncate(base * (1 + sqrt(max(0, player luck)) / 100))
tally += increment
drop chance = 0.000863316841 * 10^(0.00000425531915 * tally)
```

Evaluate the chance after adding the kill. It is about 0.0863% at tally zero, 1% at 250,000, and 11.5832% at 500,000. These are formula examples, not fixed per-kill rates or time-to-reward promises. Each eligible player rolls separately; a room death counts once regardless of the number of eligible players. A successful item award clears that player's tally. Taming someone else's creature and killing it must not become a currency source after deletion clears its control state.

The current item factory uses `MinaxArtifacts.GetDifficultyFor`, `LootPack.GetLuckChanceForKiller`, and `MinaxArtifacts.ApplyProperties`; the existing approximation uses pinned runic properties rather than the complete ServUO reforging engine. Keep that documented P408/P196 boundary. Current authentication is the saved `EnchantedOriginArtifacts` registry, plus hue 1171 and the display name where localization resolves. Renaming or dyeing unrelated equipment must not forge currency. Do not replace registration with a hue test.

The current researcher sells seven rewards. Verified from `event/SorcerersDungeonRewards.cs:32`; source prices, including the three omitted titles, are in ServUO event `SorcerersDungeonRewards.cs:19`.

| Reward | Points | Player result |
|---|---:|---|
| Jack's Bag of Tricks | 75 | Per-bag 24-hour cooldown, usable by players only in calendar October. A 10% treat roll; otherwise one of six oddities: rancid meat, glass candy cane, named elf ears, suspicious gift box, insulting doll, or spiked egg nog. Its next-use time is saved. |
| Serpent's Jawbone | 50 | Existing house teleporter. Must be locked down or secured, with its existing distance, access, and travel checks. Reuse `Items/Functional/SerpentsJawbone.cs`; do not port a second copy. |
| Jack in the Box | 20 | Toy opens after 9 seconds, closes 5 seconds later, with a 20-second reuse limit. |
| Shackled Heart of the Pumpkin King | 20 | Five blood effects at two-second intervals; no hit-point damage. |
| Sterling Silver Ring | 50 | Hit regeneration 3, mana regeneration 5, damage increase 75, durability 255; one confirmed +20 choice in Archery, Fencing, Macing, Swords, Throwing, or Wrestling. |
| Talons of Escaping | 50 | Gargoyle footwear; dexterity +4 and stamina regeneration 1. |
| Boots of Escaping | 50 | Thigh boots; dexterity +4 and stamina regeneration 1. |
| Hero of the Unloved title deed, omitted | 20 | Source title cliloc 1157649; requires reward-title storage and selection. |
| Savior of the Demented title deed, omitted | 30 | Source title cliloc 1157651; same prerequisite. |
| Slayer of the Pumpkin King title deed, omitted | 50 | Source title cliloc 1157650; purchased for points, not automatically granted for killing Jack. |

November 1-2 are deliberately different: the event can still run, but the bag tells ordinary players it works only in October. Do not silently extend it to the season window. Also keep the ring's source attributes; its high damage increase is not a reason to substitute the third-party sword or rebalance OSI rewards in a lifecycle task.

## Code placement and dependency boundaries

There are 19 event `.cs` files in the current canonical tree, counted for this note. This is the complete list beside that count:

| Files relative to event/ | Responsibility |
|---|---|
| `Generate.cs` | Season registration, entrance dressing, staff and console verbs, status |
| `Spawner.cs` | Room entries, timers, boss and regular spawn lifecycle, paused stock spawners, staff gump |
| `SorcerersDungeonData.cs` | Points subclass, death hooks, earning formula, saved controller |
| `EnchantedOriginArtifacts.cs` | Item generation, authenticity registry, persistence, GM test item command |
| `SorcerersDungeonResearcher.cs` | Turn-in NPC, context menus, reward previews |
| `SorcerersDungeonRewards.cs` | Prices and event reward gump |
| `Creatures/AbominableSnowman.cs`, `Creatures/GarishGingerman.cs`, `Creatures/HeadlessElf.cs` | Existing bosses |
| `Creatures/JackInTheBox.cs`, `Creatures/JackThePumpkinKing.cs`, `Creatures/NightmareFairy.cs` | Existing bosses; Jack's file also contains UnholyPumpkin |
| `Creatures/RabidReindeer.cs`, `Creatures/StockingSerpent.cs`, `Creatures/TwistedHolidayTree.cs` | Existing bosses |
| `Items/EscapingAndSterlingRewards.cs`, `Items/JackInTheBox.cs`, `Items/JacksBagOfTricks.cs`, `Items/ShackledHeartOfThePumpkinKing.cs` | Existing reward items and ring selection gump |

Use these files and the existing verification file at `server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs`. New event-local helpers belong beside them and are mirrored by path by `docker/uo/apply-patches.sh`. Do not edit `server/uo/`, reparent existing saved items, add a ServUO base, or replace upstream files to implement these repairs.

The relevant extension points are present:

- `pinned/UOContent/Mobiles/BaseCreature.cs:3669` raises CreatureDeathEvent after base death. CreatureDeletedEvent at line 3674 occurs before `SetControlMaster(null)` at line 3688. `pinned/Server/Mobiles/Mobile.cs:2489` calls OnDelete before Map is cleared at line 2506. Capture the needed pre-clear state there, rather than patching global death behavior.
- Existing points expose `bool DeductPoints` in `server/customizations/Services/PointsSystems/PointsSystem.cs:119` and `AwardPoints` for a refund. `server/customizations/Gumps/BaseRewardGump.cs:186` has a virtual OnConfirmed. An event-specific transaction can replace that callback without changing other collections.
- `pinned/UOContent/Misc/Loot.cs:811` exposes weighted construction over type arrays. The event can add its own complete SA pool without modifying global loot selection. Array selection is weighted by total entries, not equal probability per category.
- Existing `ClusterFSeasonalSwitch.cs`, `BaseTurnInMobile.cs`, the points framework, ability profile, `MinaxArtifacts`, and `SerpentsJawbone` remain dependencies, not duplicate deliverables.

## Build specification for the remaining defects

### Encounter ownership and kill eligibility

P408's review and P461 both remain applicable to the inspected main revision. `Spawner.Reset` at line 283 forgets living regular creatures from a completed room. `Deactivate` at line 136 only knows the current list and boss. Jack's hatch at line 217 registers no ownership, and the delayed throw at line 98 has no event or destination guard. These are source-confirmed paths; P564 did not reproduce them in a running server.

Add controller-owned cleanup collections separate from room progression:

- Keep `Spawn` as the current room's regular creatures. Only removal from this list through a genuine death advances KillCount.
- Add saved collections for all event-owned creatures and outstanding pumpkins. Register regular spawns and bosses when placed. Register Jack's pumpkins and transfer ownership to the undead they hatch. Prune dead and deleted references. A room reset clears progression references but retains cleanup ownership of survivors. Hatched undead and survivors from previous rooms must not increment the new room's counter.
- A delayed throw captures the owning controller when scheduled. For an event-owned Jack, execute only while that same controller is active, Enabled is true, Jack is alive and still its current boss, and the attacker is alive, not deleted, and inside the Ilshenar Sorcerer's Dungeon region. Check each destination against that region and the existing fit test. Do not redirect a pumpkin onto another facet. Keep manually added, unowned test creatures distinguishable from event-owned creatures.
- Disable earning and invalidate controller callbacks before deleting owned entities. Stop its timers, delete its tracked pumpkins and creatures, then restore exactly the stock spawners it paused. A callback from an old controller must not populate a newly started event. Never sweep the region for all Zombies, pets, or same-art pumpkins.
- Preserve `off` versus `remove`: both clean event combat; only remove deletes tracked entrance entities. Status should report current-room counts and owned cleanup counts separately. The room's total world population is not a cleanup oracle because normal spawns return.

Keep the controller's original version-0 field sequence, then append the ownership lists in a version-1 format. The version-0 reader seeds ownership from its saved Spawn and Boss. The version-1 reader restores the complete cleanup collections before gameplay callbacks can act. Preserve points, tallies, room index, kills, registered currency, paused-spawner references, and the original entity types. Test both versions. The containing points system can continue to frame the nested controller as before; a new global save migration is not required merely for a versioned nested object.

Version 0 cannot identify creatures it already forgot in earlier rotations or unregistered hatches. Do not pretend loading it can recover those references, and do not automatically delete ordinary dungeon creatures to compensate. If an existing world needs cleanup, report the evidence and request a separate, explicitly authorized staff action. P564 did not inspect any existing world.

For currency eligibility, extend the existing deletion snapshot beyond Map to include the victim's controlled and summoned flags and death location before deletion clears state. Consume only a snapshot matching that creature; the nondeleted bonded-pet path reads its current state. Ordinary deletion must not grant credit. Keep the capture ephemeral and bounded, with no accumulating cache of staff-deleted creatures. Verify actual death event ordering, including another creature dying during a handler, before choosing whether the existing single-slot capture needs keyed storage. All credited players use the same captured eligibility and region. The room controller still receives a single death notification.

Replace the flaky tally assertion at `SorcerersDungeonVerification.cs:679`: it assumes a legitimate random drop did not occur. Provide an injected roll for the decision, scoped and restored in tests, so fail and succeed branches can be exercised through real death dispatch. Production still uses Utility.RandomDouble. Do not merely rerun until green or force all production rolls to fail.

### Reward confirmations

P461's pending-purchase case is supported by `BaseRewardGump.cs:186`, `:254`, and `event/SorcerersDungeonRewards.cs:56`. Affordability at menu opening is insufficient. The confirmation currently delivers before an unchecked deduction. For the event-specific reward gump, override OnConfirmed and make one server-loop transaction:

1. Validate the current user, live researcher, same facet, allowed distance, valid catalog row, and current point balance.
2. Construct the selected item, then require a successful `DeductPoints` before delivery. Reject a failed debit and delete the unused item.
3. Attempt backpack delivery. On failure delete the item and refund the exact debit once. On success retain the debit and send the source's success message and sound. Do not call base delivery and debit a second time.

With 50 points and two pending 50-point ring confirmations, at most one ring is delivered. This is an event-local repair of a shared inherited defect; a later shared-gump fix can replace it after equivalent coverage. Do not widen this prompt into changing every collection.

At the ring's final confirmation (`Items/EscapingAndSterlingRewards.cs:172`), recheck the bonus slot is still unset, in addition to possession and deletion. A second pending choice must not replace the first. Preserve cancel, transfer, and failed confirmation behavior. These two repairs enforce the advertised purchase and one-time choice contracts, rather than changing reward prices or stats.

### Restore the artifact equipment pool

P461 identifies a separate fidelity gap from the property-roll approximation. ServUO event `SorcerersDungeonData.cs:72` passes a third, Stygian-selection argument; `Scripts/Misc/LootPack.cs:578` chooses it randomly half the time for a non-Tokuno, non-ML location such as this dungeon. Pinned's two-argument selector at `pinned/UOContent/Misc/Loot.cs:668` never uses the SA tables. Our current call at `event/EnchantedOriginArtifacts.cs:88` therefore omits SA-only equipment.

Add an event-local selector, preserving that branch probability and ServUO's within-pool entry weights. The SA branch consists of these arrays in source order (`ServUO Scripts/Misc/Loot.cs:783`): SA weapons, AOS weapons, ordinary weapons, SA ranged, AOS ranged, ordinary ranged, SA armor, ordinary armor, AOS hats, ordinary hats, AOS shields, ordinary shields, ordinary jewelry, SA jewelry, SA shields. The ordinary branch keeps the existing era selection. Do not implement this as a 50% chance of an SA-only item: the source's SA branch includes ordinary equipment too.

Resolve the SA-specific entries as follows. These declared classes or pinned aliases were checked in the current source trees; there is no new content subsystem prerequisite:

| Source table | Entries to use |
|---|---|
| SA weapons | DiscMace, GargishTalwar, Shortblade, DualPointedSpear, GlassStaff, StoneWarSword, DualShortAxes, GlassSword, GargishDagger. Pinned's public SAWeaponTypes omits Shortblade, StoneWarSword, and GargishDagger; those already live in our `Items/Equipment/Weapons/`. Build the full event table, not the shorter pinned table. |
| SA ranged | Boomerang, Cyclone, SoulGlaive, all already in pinned |
| SA armor | Pinned GargishLeatherChestType1, GargishLeatherLegsType1, GargishLeatherArmsType1, GargishLeatherKiltType1; GargishStoneChestType1, GargishStoneLegsType1, GargishStoneArmsType1, GargishStoneKiltType1; our GargishPlateChest, GargishPlateLegs, GargishPlateArms, GargishPlateKilt, GargishNecklace, GargishEarrings |
| SA jewelry | Our GargishRing and GargishBracelet |
| SA shields | Our GargishChaosShield, GargishKiteShield, GargishOrderShield, LargeStoneShield; pinned GargishWoodenShield |

The eight Type1 aliases are declared in pinned `Items/Armor/Leather/GargishLeather*Type1.cs` and `Items/Armor/Stone/GargishStone*Type1.cs`. Do not create duplicate ServUO-named armor. Other custom entries are in `Items/Equipment/Armor/`, `Items/Equipment/Jewelry/`, and `Items/Equipment/Weapons/`. Keep the shard's already-applied global hat-table additions as an existing boundary (`server/patches/Loot-hat-types-orc-tribal-mask.patch`); do not change global loot while restoring the event's missing branch. Record any residual table differences explicitly.

Carry the death snapshot's region/facet into factory selection rather than asking a deleted creature for its region. Preserve artifact authentication, property application, and successful-award tally reset. A test must exercise both branch choices deterministically and enumerate expected tables, not depend on repeatedly rolling until a boomerang appears.

## Art and client acceptance

Use existing EA assets. No generated art, new animation body, custom item ID allocation, cliloc rewrite, client patch, or package rebuild is part of this design. Consequently no art request is needed now. If client inspection finds a missing asset, report its exact ID and stop that asset's acceptance claim; any newly requested custom art must go through New-ArtRequest.ps1 and Chase's Generate action.

P408 reports reading tiledata and rendering the bag from `D:\UO\UltimaOnlineVanilla`, checking body names, and booting with UOAlive 7.0.116.0 data. It explicitly did not verify the server's other client-data folder or see the event in a client. Treat those as prior observations, not proof that the currently distributed package renders everything correctly.

Check the supported player package in an isolated session for:

- All nine bodies, especially Jack in the Box body 1428, Stocking Serpent body 1289, and Jack's human outfit; pumpkin missiles `0xC6A-0xC6C` and sounds `0x491` and `0x48F`.
- Entrance dressing: `0x9D2B-0x9D2D` at `(546,460,6)`, `(548,460,6)`, `(548,458,6)`; two `0x9F34` at `(545,462,-53)` and `(550,462,-53)`; `0x9F28` at `(545,463,-55)` and `0x9F24` at `(550,463,-55)`.
- Bag `0x9F85`, jawbone `0x9F74`, toy `0x9F64/0x9F65`, heart `0x4A9C`, ring `0x1F09`, boots `0x1711`, and talons `0x41D8`. Check the bag's oddities too, including candy cane `0x9DC3/0x9DC4`, elf ears `0x312D/0x312E`, and doll `0x48E2/0x48E3`.
- Researcher context menus, the complete reward list and prices, item names and Enchanted Origin message, ring selection and confirmation, and the effects actually visible to a normal player. Check localization 1157613, 1157614, 1157653-1157657, and the bag's October refusal 1157632. P408 could not directly verify the suffix's cliloc text.

Record client version, package version, facet, coordinates, and which checks passed. A type constructing or an art ID appearing in source does not establish correct rendering.

## Verification requirements

No lane tests are required or run for this design-only prompt. Future code prompts must add regressions to the existing event test file, watch each new defect test fail against the old behavior, then pass after the fix. For additional coverage of already-correct timer behavior, deliberately break that behavior first and record the failure before restoring it. Use `ShardTestClock.Arm()` before creating timed objects and `Advance()` to drive callbacks; do not sleep through tests or slice the wheel directly.

| Area | Required evidence |
|---|---|
| Room progression | 80th tracked death raises one boss; extra looting-rights players do not multiply room kills; old-room survivor deaths and pumpkin children do not advance the new room; ninth boss wraps to first |
| Cleanup | Complete at least one room with survivors, then off and remove; delete all owned survivors, boss, pumpkins, and hatches, preserve an unrelated same-type creature and same-art item; no resurrection of spawns after advancing all pending delays |
| Save compatibility | Load controller v0; load v1 with old-room survivors, current creatures, boss, outstanding pumpkin, paused spawners, points, tally, and artifact registry; remove after reload leaves no owned combat entity; second load does not duplicate timers or entities |
| Kill eligibility | Real nonbonded controlled-creature death gives no tally or artifact, including after control is cleared; summoned and bonded victims excluded; ordinary NPC death credited; dead player and outside-region cases excluded; nested death does not mix snapshots |
| Deterministic drops | Real death hook with forced fail retains the exact tally; forced success awards and resets it; backpack, bank, and ground fallbacks; forged hue/name rejected and spent artifact cannot redeem twice |
| Reward transactions | Two pending 50-point purchases with only 50 points deliver once; insufficient funds, cancel, moved/deleted researcher, other facet, and full backpack do not lose points or grant free items; refund exactly once on delivery failure |
| Ring | Drive real selection and confirmation callbacks, including two pending different skills, cancellation, deletion, and transfer; the first valid choice persists and cannot be overwritten |
| Timed rewards | Toy opens at about 9 seconds and resets 5 seconds later; heart creates five blood effects without damage and then stops; restored pumpkin hatches exactly once and deletes itself |
| Artifact pool | Both ordinary and SA branches, all expected source entries and alias mappings, full SA weapon list, weighting by entries, property roll and saved registry on a throwing weapon |
| Calendar | October 23 off, October 24 on, November 2 on, November 3 off; restart and staff override; Halloween decor has independent state; October-only bag restriction remains |

Each code prompt finishes with `docker/uo/build.sh -t sl-modernuo:<assigned-prompt>` under the docker-build lock. This means the patch gate, compiler, all shard tests, and image gate, not a direct docker build. Any PowerShell helper or test runs through Windows PowerShell 5.1 (`powershell.exe`). Inspect the Docker daemon before test use; never select a Haven context.

The runtime pass uses a throwaway loopback-only container and scratch saves, under the required local locks. Do not copy, edit, start, stop, or deploy a shared shard as part of it. Save/reload the scratch event and confirm actual entity ownership counts, not just room population after ambient spawns resume. Chase separately authorizes any release or real-world action.

## Ordered Golem prompt drafts

These are sequencing labels, not allocated P numbers or newly queued prompts. If a fix has landed since this source snapshot, recheck it and carry its evidence forward rather than reimplementing it. Each implementation prompt writes its own notes, includes red-before-green evidence, and leaves the shard buildable. None authorizes Haven access, deployment, shared-world placement, or commits by the agent.

### PK1: Finish encounter ownership, shutdown, and kill credit

**Touches:** server

**Depends on:** existing P408.

Implement the encounter and death-snapshot specification above in `event/Spawner.cs`, `Creatures/JackThePumpkinKing.cs`, `Generate.cs`, and `SorcerersDungeonData.cs`. Extend the existing event verification file. Preserve source combat math and room thresholds. Persist ownership separately from progression with a version-0-compatible version-1 reader. Confine event pumpkin callbacks to their active dungeon encounter and invalidate callbacks before cleanup. Make real-death drop tests deterministic. Cover both P408 review lifecycle findings and P461's pumpkin findings together so there is one ownership model.

**Done means:** the specified real-death, rotation, shutdown, delayed-callback, and old/new-save regressions have been seen red and green; the full build gate passes; notes state that already-untracked v0 survivors cannot be inferred safely. No broad world sweep or new upstream patch.

### PK2: Enforce purchases and the ring's one-time choice

**Touches:** server

**Depends on:** PK1 for the integrated event suite.

Implement the event-specific checked debit/delivery/refund transaction in `event/SorcerersDungeonRewards.cs` and the final unset-slot guard in `Items/EscapingAndSterlingRewards.cs`. Drive actual confirmation callbacks in regression tests. Keep prices, reward attributes, and the seven-item catalog. Prefer the existing virtual callback over changing shared BaseRewardGump; document that the inherited defect can affect other systems separately.

**Done means:** queued purchases and queued skill choices cannot overspend or overwrite; delivery failure refunds once; stale, transferred, and cross-facet cases are rejected; each regression is red before the fix and green after it; the full build passes.

### PK3: Restore SA artifact selection and cover delayed reward behavior

**Touches:** server

**Depends on:** PK1's death context and PK2's reward regressions.

Add the event-local source-equivalent equipment selector in `event/EnchantedOriginArtifacts.cs` or a sibling `EnchantedOriginLoot.cs`, using the complete arrays and existing types identified above. Thread captured death-region context from `SorcerersDungeonData.cs`. Preserve the existing reforging approximation and saved registry. Add deterministic branch/table tests and actual timer assertions for the toy, heart, and restored pumpkin, rather than constructor-only checks. Do not add a global loot patch or duplicate aliased armor.

**Done means:** the missing SA branch has a baseline failing regression; all expected entries resolve and construct, branches and weights match the source; existing behavior has meaningful mutation evidence; the full build passes. Notes list any remaining property-roll and table deviations for overseer promotion.

### PK4: Verify the playable event and prepare its player guide

**Touches:** server

**Depends on:** PK1-PK3.

Use only an isolated local container and scratch saves for the on, room rotation, boss, off, remove, and reload checklist. Under the normal local test locks, inspect the supported client package using test staff and normal-player views. Exercise earning, turn-in, purchases, ring selection, bag, toy, heart, and entrance travel. Use the existing commands: `[SorcerersDungeon status|on|off|remove|boss 9`, each mutation's `dryrun`, console `tosd`, `[TOSDSpawner`, and GM `[EnchantedOriginArtifact`. Test-only generated currency must remain in scratch saves. Do not add Shard Console controls solely for this test.

Write the evidence and a concise player guide in `shard-migration/notes/`, including dates, entrance, shared progression, earning versus spending, prices, October-only bag, and omitted titles. Prepare release notes in the normal code-repo files only if the assigned prompt requests them. Do not publish to Haven or a wiki from this task. If no usable client is available, finish the server evidence and explicitly leave client acceptance open; do not report the event fully verified.

**Done means:** the acceptance matrix has measured results and remaining limits; no event-owned combat entities survive shutdown/reload in the scratch world; supported-client rendering and player flow are actually observed or clearly open. A build being present in main never establishes what is deployed.

### PK5, optional: Size the shared reward-title system

**Touches:** docs-only

**Depends on:** Chase requesting titles; does not block PK1-PK4.

Measure the smallest faithful saved title collection, title selection/display integration, and BaseRewardTitleDeed port against pinned's existing title paths. Inventory consumers and alternatives before proposing any PlayerMobile or paperdoll patch. Supply a file list, patch arguments, save/load design, tests, and a separately reviewable implementation prompt. Then an approved server task can add the three event deeds and source prices to both the reward list and researcher previews. Do not sell inert deeds or insert a new saved ancestor to avoid doing that work.

**Done means:** measured subsystem scope with an implementation draft, not an invented title API or an implied approval to patch PlayerMobile. Current source searches found only comments for AddRewardTitle in the shard and no BaseRewardTitleDeed declaration in pinned or the canonical shard tree. Existing achievement titles are not evidence of a compatible reward-title collection.

## Deviation and handoff notes

Keep the P408 deviations visible: our chosen calendar; absent title deeds; internal JackInTheBoxMonster rename; registered artifact identity and property-roll approximation; stock BaseSpawner pause/restore instead of XmlSpawner; generator safety fixes and staff commands. PK1 adds explicit ownership cleanup and confines pumpkin placement; PK2 closes inherited confirmation holes; PK3 removes the separate missing SA-selection gap. Record the precise end state and reversal condition for each remaining difference in implementation notes. The overseer promotes durable entries into `docs/fidelity-principle.md` and bug tracking. Agents must not edit docs/.

No external art, service, or hosting change is proposed, so neither services.json nor the Haven runbook needs an edit. No new Shard Console window button is proposed. If a later prompt adds one, it also needs its web console twin and the P187 check.

P564 verification: inspected the source paths and revisions above, checked the room and reward tables, calculated the chance examples directly from the constants, and checked that the remaining review findings still match the inspected main. Ran the required progress calculation against these work copies with output writes suppressed in memory, because progress.py --dry-run still attempts to rewrite tools/progress.json. It completed; that generated write was discarded. No test suite or build was run and no new tests were added. The only intended repository change is this notes file.

Unverified: deployed event version, live Halloween settings, current-world spawns or leftovers, the distributed client's actual rendering, runtime exploit reproduction, and current official OSI behavior beyond the ServUO reference. P408's prior green build and headless smoke results remain prior evidence, not tests rerun by P564. No connection to Haven was made.

## Questions for Chase

These are nonblocking recommendations for scheduling the follow-up work, not requests to stop this design task.

1. **Should the next event prompt finish the existing port's lifecycle and reward defects?** Recommended: yes, PK1 then PK2, followed by the pool and acceptance work. Keep the chosen OSI event and source difficulty; no second Halloween boss build.
2. **Should this first version keep October 24 through November 2?** Recommended: keep the already-chosen shared Halloween window. A longer window should be a separate recorded schedule decision because those settings also move bank decor.
3. **Should title deeds block the event?** Recommended: no. Keep them absent and offer PK5 separately if reward titles matter. Do not claim the full OSI reward catalog while the three deeds are missing.
4. **Should the missing SA equipment branch be restored?** Recommended: yes, PK3. All of its listed types already exist or resolve to verified pinned equivalents; restoring the source pool does not require new art or a reforging subsystem.
5. **Should the Bag of Tricks work on November 1-2 too?** Recommended: keep the source's October-only rule and explain it in the guide. Extending it would be a new deliberate deviation, not a bug fix.
6. **Should the researcher and entrance pieces remain after the season?** Recommended: yes, retain the source behavior and year-round redemption. Use the existing tracked remove command only for a separately authorized teardown.

P564 DONE

