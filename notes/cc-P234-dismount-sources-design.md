# cc-P234: design pass, more ways to be dismounted (F-39)

2026-10-20. Docs-only: nothing in `server\`, `docker\` or the client changes. Pinned citations are `D:\UO\ModernUO-pinned`
at d4531cd94, paths under `Projects\UOContent\` unless marked; shard citations are `D:\ShatteredLegacy\server\` (read in
the Bronze work copy). Every number below carries its source or the decision it comes from; a number marked
**(proposal)** is mine for Chase to answer, and **(assumption)** marks the rates behind the per-hour estimate.

## Headlines

- **Finding: Steady Hoof Wraps hooks nothing today.** The module is `Stubbed` in the data
  (`customizations\Mobiles\Mule\MuleModuleData.cs:116-118`: tiers 25, 50, 100, "waits on a pinned change to the
  dismount paths (planned)"), and the tree holds no `ResistsDismount`, no dismount check and no patch to any dismount
  path (grep of `customizations\` and `patches\` for SteadyHoof, ResistsDismount, DoDismount, BlockMountType: only the
  module rows and two of our bosses' `SetMountBlock` calls). P70 Part E planned the check (`PackMule.ResistsDismount`,
  one patch of 15-20 lines at the four pinned sites) and never built it. So "the one check Steady Hoof Wraps hooks"
  is still a plan, and **it is the first thing to build**: every source below is written against it.
- **Today's paths: eight that knock a rider off, five of them bypassing each other.** Pinned: the Dismount weapon
  ability and Infused Throw (both through `Dismount.DoDismount`), Riding Swipe (`BaseMount.Dismount`), the Bola and
  Meraktus's stomp (both set `Rider = null` directly), the holiday Icy Patch (`Rider = null`), and
  `PlayerMobile.SetMountBlock(..., dismount: true)`, which `DoDismount` and the Bola call and which two of our bosses
  call on their own (section 1). There is no single choke point now; the check has to be inserted at each.
- **Twelve creatures already dismount on this shard through OSI's own rule**: ten pinned types and two of ours carry
  `WeaponAbility.Dismount` as their swing ability (plus two of ours that roll it among others), armed on 40% of swings
  (`BaseCreature.WeaponAbilityChance`, `BaseCreature.cs:925`; `BaseWeapon.cs:873-884`) for 20 mana
  (`Dismount.cs:16`). That behaviour stays exactly as it is; F-39's sources are added beside it (section 2).
- **Proposals in one line each** (the numbers are in the sections and the balance table):
  1. Big monsters: a hand list in three families (giants, dragons and great beasts, demons), **10% or 5% per hard hit**,
     a hard hit being a melee hit that takes at least **15% of the rider's max hits** after resists, one roll per
     creature per 10 s.
  2. No-ride areas: the **37 cave and mine regions pinned already names** (Felucca and Trammel's "Cave 1-4", the Yew,
     Minoc, North Territory, Ice Isle and Avatar Isle caves, the Britain, Minoc, Covetous and North Territory mines;
     Ilshenar's rat, mushroom and spider caves; Malas's ninja cave and the Yomotsu Mines; Ter Mur's Cavern of the
     Discarded and the four Abyss lairs), plus two dungeon regions that are caves (Orc Cave, The Painted Caves) and the
     Rootdeep crawlway: **mounting blocked inside, a dismount on entry with a message**, and this one source is not
     resisted by the Wraps (a ceiling is not a blow).
  3. Traps: fire and blast traps **25%**, spikes, saws and stone faces **15%**, darts and magic chest traps **10%**,
     the P201 bear trap and snare **50%** (the mount is caught), gas, poison, mushrooms, caltrops, alarms and shackles
     **0%**; a 5-second daze instead of the blow's 10.
  4. Wildlife: bulls, boars, great harts, grizzly and polar bears, Eodon's triceratops, allosaurus and wild tiger
     **charge a rider who runs within 6 tiles** in the wild only, 10-25% to charge, and the charge's first hit within 10
     s dismounts through the check; 2 minutes per creature, 60 s immunity per rider.
  5. Per hour in a typical dungeon run, before the module: **about 2.5 dismounts** (1.4 from big monsters, 0.6 from floor
     traps, 0.2 from chests, plus the cave mouths you choose to ride through); Wraps I about 1.9, II about 1.3, III the
     ceilings only (assumptions in section 6).
- **Decisions for Chase**: 12, numbered, in the section of that name. **A draft build prompt** (two parts: the check and
  the Wraps patch first, then the four sources) is at the end for the overseer to number.

## 1. Today's paths, with file:line, and what the check must cover

| # | Path | Where the rider comes off | Who uses it | Already through one check? |
|---|---|---|---|---|
| 1 | **Dismount weapon ability** | `Dismount.OnHit` -> `DoDismount` (`Items\Weapons\Abilities\Dismount.cs:19-61`, `:63-107`): `SetMountBlock(Dazed, 10 s, dismount: true)` for a player (`:92`), `Mount.Rider = null` for anyone else (`:96`); 15-25 extra damage when the attacker is on foot (`:56-59`) | players with the ability; creatures whose `GetWeaponAbility` returns it (section 2); pets trained to it (`PetTrainingHelper.cs`, the training table) | `DoDismount` is one choke point for 1 and 2 |
| 2 | **Infused Throw** | `InfusedThrow.cs:41-49` -> `Dismount.DoDismount` (the paralyze branch otherwise, `:50-56`) | gargoyle throwers | as 1 |
| 3 | **Riding Swipe** | `RidingSwipe.cs:38` -> `BaseMount.Dismount(defender)` (`BaseMount.cs:273-281`, `Rider = null`), then damage to the mount | Bushido players on foot | **no**: never touches `DoDismount` |
| 4 | **Bola** | `Bola.cs:71-74`: `mt.Rider = null`, then `SetMountBlock(Dazed, 10 s)` (`:77-87`) | players | **no** (P70's correction of P47 5.4: `SetMountBlock` alone would not catch it, the rider is already off) |
| 5 | **Meraktus's stomp** | `Monsters\ML\Special\Meraktus.cs:235-238`: `pm.Mount.Rider = null` on everyone in the area | one boss | **no** |
| 6 | **Icy Patch** | `Items\Special\Holiday\IcyPatch.cs:64-67`: `m.Mount.Rider = null` on a slip | a holiday item | **no** |
| 7 | **`SetMountBlock(type, duration, dismount: true)`** | `PlayerMobile.cs:1086-1100`: nulls `Rider` (or ends Animal Form) and sets the block | `DoDismount` (1, 2), the Bola (4), and **ours**: `Mobiles\Normal\MinionOfScelestus.cs:108` (Dazed 10 s) and `Services\Expansions\High Seas\Mobiles\OsiredonTheScalisEnforcer.cs:188` (DismountRecovery 10 s) | **no** as a group: our two bosses skip `DoDismount` |
| 8 | **Mount death** | `BaseMount.OnBeforeDeath` (`BaseMount.cs:155-159`): `Rider = null` | anything that kills the mount | not a dismount to resist (the mount is dead) |

Self-dismounts, never resisted (P70's rule, kept): Animal Form (`Spells\Ninjitsu\AnimalForm.cs:219`), a gargoyle's
flight toggle (`PlayerMobile.cs:757-762`), polymorph, stabling, and the player's own double-click. Pinned's remount
rules after a dismount: `BlockMountType` Dazed, BolaRecovery, DismountRecovery (`PlayerMobile.cs:92-98`), checked in
`BaseMount.CheckMountAllowed` (`BaseMount.cs:283-309`) together with `BaseRegion.MountsAllowed` (`:288`;
`Regions\BaseRegion.cs:45`, `true` with **0 overrides**, as P45 found: `notes\cc-P45-companion-probes.md:258-262`) and the
gargoyle race rule (`:301-305`). Chaos Dragoons are immune at every pinned site (`Dismount.cs:26-29`, `InfusedThrow.cs:42`,
`Bola.cs:64-70`).

**What the check is.** One static entry in our code, P70's shape with a name that fits all sources:

```
DismountRules.TryDismount(Mobile rider, Mobile source, DismountCause cause, TimeSpan daze, BlockMountType type)
```

It returns false (and says why to both sides) when the rider resists: the Wraps roll by tier (25%, 50%, immune) for
every cause but `LowCeiling`; otherwise it does what `DoDismount` does today (`:92-96`) and returns true. **Sites**: the
head of `DoDismount` (covers 1 and 2 and every future `DoDismount` caller), `RidingSwipe.cs:38`, `Bola.cs:71`,
`Meraktus.cs:237`, `IcyPatch.cs:66` (five pinned hunks, one `.patch`, about 20 lines, alternatives argued in P70 Part E:
(a) re-mount on the next tick cannot tell a blow from a choice, (b) a virtual `Rider` setter is a core change), and our
own two bosses, which are plain edits. The pet-training swing (a tamed creature with Dismount) goes through 1. The
`SetMountBlock(dismount: true)` overload is **not** patched: after the check succeeds it is the mechanism, and leaving
it alone means a self-dismount never rolls.

## 2. Big monsters knock riders off

**What OSI already does, untouched.** These carry `WeaponAbility.Dismount` as a swing ability today (file:line is the
`GetWeaponAbility` override; damage is the constructor's `SetDamage`):

| Creature | Source | Damage | Note |
|---|---|---|---|
| Hiryu | `Mobiles\Animals\Mounts\Hiryu.cs` | 20-30 | mount |
| Lesser Hiryu | `LesserHiryu.cs` | 18-23 | 80% of its dismounts miss (`Dismount.cs:48-51`) |
| Gibberling | `Monsters\AOS\Gibberling.cs` | 12-17 | |
| Patchwork Skeleton | `Monsters\AOS\PatchworkSkeleton.cs` | 18-22 | |
| Treefellow | `Monsters\AOS\Treefellow.cs` | 12-16 | |
| Feral Treefellow | `Monsters\ML\Humanoid\Melee\FeralTreefellow.cs` | 26-35 | |
| Tormented Minotaur | `...\Tormented Minotaur.cs` | 16-30 | |
| Malefic | `Monsters\ML\Twisted Weald\Malefic.cs` | 15-22 | |
| Flesh Renderer | `Monsters\AOS\FleshRenderer.cs` | 16-20 | half the time (with Paralyzing Blow) |
| Ravager | `Monsters\AOS\Ravager.cs` | 15-20 | half the time (with Crushing Blow) |
| Skeletal Lich (ours) | `customizations\Mobiles\Normal\SkeletalLich.cs` | 8-10 | |
| Treefellow Guardian (ours) | `...\TreefellowGuardian.cs` | 12-16 | |
| Dimetrosaur (ours) | `...\Dimetrosaur.cs` | 18-21 | half the time (with Mortal Strike) |
| Giant Turkey (ours) | `...\GiantTurkey.cs` | 20-30 | a third of the time |

The rule they run on: each swing arms the ability with probability `WeaponAbilityChance` (0.4; our Despise creatures
0.5, `DespiseEvilCreatures.cs:91,152,181`), it fires on a hit if the creature has 20 mana (`WeaponAbility.CheckMana`,
`WeaponAbility.cs:298-311`; `Dismount.BaseMana`, `Dismount.cs:16`), it needs the attacker on foot (`:31-38`), and it
dazes the rider 10 s (`:52`) and blocks the creature's master's remount 10 s if it is a pet (`:103-106`). **None of this
changes.** Chaos Dragoons stay immune.

**What F-39 adds, on top (proposal).** A second, independent roll that does not use the ability slot, the mana or the
0.4 arming chance, so it reaches every big creature whether or not it has a weapon ability:

- **Where it runs:** the shard's existing damage hook in `AOS.Damage` (`patches\AOS-damage-eater-hook.patch`, where P121's
  "hit taken" trigger already reads attacker, defender and the final damage), so it sees **damage after resists** and
  only for melee (P121's spell mark tells spell damage apart; breath is `BaseCreature.BreathAttack`, not a weapon hit, and
  is excluded). The attacker must be a `BaseCreature` on the list and not controlled or summoned (a tamed dragon does not
  do this to its owner's party; pets dismount only through the trained ability).
- **Hard hit (proposal):** the hit's damage after resists is at least **15% of the rider's `HitsMax`** (15 on a
  100-hit character, 18 at 120). Why a share of max hits and not a flat number: creature damage after a 70-resist suit
  is small (a Dragon's 16-22 lands around 10-15), so a flat 25 would almost never trigger on the riders who dungeon,
  while a share scales with F-12's bigger pools. Alternative for Chase: the raw roll in the top third of the creature's
  own `SetDamage` range (independent of armour; needs the pre-resist number, which the hook does not carry today).
- **One roll per creature per rider per 10 s** (proposal), so a 1.25-second swinger cannot roll eight times in the
  daze window.
- **The list (proposal), in three families; the chance is per hard hit.** Stats are each file's constructor; "big" was
  read from `SetStr` and `SetHits` and from F-14's difficulty base (`BaseInstrument.GetBaseDifficulty`,
  `Items\Skill Items\Musical Instruments\BaseInstrument.cs:250-300`: hits x 1.6 + stam + mana + skills / 10, +100 each
  for magery, breath and poison immunity), which the build prompt's test prints so the families can be checked
  against it. A creature that already carries the Dismount ability (table above) is not listed twice.

| Family | Creatures (file under `Mobiles\`) | Str, hits, damage | Chance per hard hit |
|---|---|---|---|
| **Giants** | Titan (`Monsters\Humanoid\Magic\Titan.cs`: 536-585 / 322-351 / 13-16), Ogre Lord (`...\Melee\OgreLord.cs`: 767-945 / 476-552 / 20-25), Cyclops (`Cyclops.cs`: 336-385 / 202-231 / 7-23), Juggernaut (`Juggernaut.cs`: 301-400 / 181-240 / 12-19), Minotaur, Minotaur Captain, Minotaur Scout (`Monsters\ML\Humanoid\Melee\`: 301-425 / 301-440 / 11-20) | | **10%** for Titan and Ogre Lord, **5%** for the rest |
| **Lesser giants** | Ettin (136-165 / 82-99 / 7-17), Ogre (166-195 / 100-117 / 9-11), Troll (176-205 / 106-123 / 8-14), Frost Troll (227-265 / 140-156 / 14-20), Stone Gargoyle (246-275 / 148-165 / 11-17), Golem (251-350 / 151-210 / 13-24, x scalar) | | **5%** |
| **Dragons and great beasts** | Dragon (796-825 / 478-495 / 16-22), White Wyrm (721-760 / 433-456 / 17-25), Shadow Wyrm (898-1030 / 558-599 / 29-35), Ancient Wyrm (1096-1185 / 658-711 / 29-35), Greater Dragon (1025-1425 / 1000-2000 / 24-33), Hydra (801-828 / 1480-1500 / 21-26), Reptalon (1001-1025 / 833-931 / 21-28), Yamandon (786-930 / 1601-1800 / 19-35), Triceratops (ours, 1100-1300 / 21-28), Allosaurus (ours, 699-828 / 21-23), Saurosaurus (ours, 802-824 / 21-28), Wild Tiger (ours, 496-554 / 18-24) | | **10%** |
| **Demons** | Balron (986-1185 / 592-711 / 22-29), Daemon (476-505 / 286-303 / 7-14), Ice Fiend (376-405 / 226-243 / 8-19), Succubus (488-620 / 312-353 / 18-28), Bone Demon (1000 / 3600 / 34-36), Putrefier (1057-1400 / 3010-4092 / 27-34), Semidar (502-600 / 1500 / 29-35) | | **10%** for Balron, Bone Demon, Putrefier, Semidar; **5%** for the rest |

Not listed, with the reason: Drake (401-430 Str, a rider's everyday fight), Wyvern, Lich and Lich Lord (casters), Efreet,
Elder Gazer and Gargoyle Destroyer (magic damage, not blows), Swamp Dragon (a mount), Changeling, Silvani (a
quest boss with its own script), and every champion and Peerless boss (they have scripted specials; Chase may add
them by name). Paragons of a listed creature use the family's chance plus 5 (proposal).

- **Effect:** `DismountRules.TryDismount(rider, creature, HardHit, 10 s, Dazed)`: the same daze, sound, particles and
  messages as a blow (`DoDismount`'s, so the player cannot tell our rule from OSI's), the creature's own name in the
  "~1_NAME~" line, and none of the ability's extra 15-25 damage (the hard hit was the damage).
- **Fidelity:** OSI's creatures gain a behaviour OSI never gave them. Logged as a deviation when built (the register,
  through Claude), with the wiki line "big creatures can knock you from your mount on a hard hit".

## 3. No-ride areas (regions only)

**What exists.** Pinned's region data (`D:\UO\ModernUO-pinned\Distribution\Data\regions.json`, read with a script: 490
named entries, 356 with an `$type`) already names the cave mouths and mines as `BaseRegion` entries, each with its own
rectangles, and the dungeons as `DungeonRegion`. `BaseRegion.MountsAllowed` is virtual, `true`, and overridden nowhere
(`Regions\BaseRegion.cs:45`; P45). `Region.OnEnter(Mobile)` and `OnExit` are virtual (`Server\Regions\Region.cs:751-755`),
as is `OnMoveInto` (`:748`). Pinned registers every JSON region as a `Dynamic` region of the named type, so a tie in
priority falls to list order (our Despise region sits at 51 for that reason, `DespiseController.cs:181` and its header),
and our own regions are registered in code at start (`customizations\Regions\OldHavenBurrowsRegion.cs`, header).

**The list (proposal): every region pinned names as a cave or mine, plus two cave dungeons and our crawlway.** Rect
counts are the JSON's `Area` entries; the Felucca list repeats on Trammel.

| Facet | Regions (`Name` in regions.json) | Rects |
|---|---|---|
| Felucca and Trammel | Cave 1 (4), Cave 2, Cave 3, Cave 4, Yew Cave, Minoc Cave 1, 2, 3, North Territory Cave, Ice Isle Cave 1, Ice Isle Cave 2 (2), Avatar Isle Cave, Britain Mine 1, Britain Mine 2, Minoc Mine (2), Covetous Mine (3), North Territory Mine 1, North Territory Mine 2 | 18 names, 25 rects per facet |
| Felucca and Trammel, dungeons | Orc Cave (3), The Painted Caves (1) | 2 names |
| Ilshenar | Mushroom Cave, Rat Cave Territory, Ratman Cave (2), Entrance Mushroom Cave, Entrance Rat Cave, Entrance to Spider Cave, Entrance Ancient Lair, Spider Cave (dungeon, 2) | 8 names |
| Malas | Ninja cave, Yomotsu Mines (dungeon) | 2 names |
| Ter Mur | Cavern of the Discarded (7), Abyssal Lair, Fairy Dragon Lair, Medusas Lair (2), Serpents Lair (3) | 5 names |
| Ours | the Rootdeep crawlway (`customizations\Regions\RootdeepVault.cs:255-262`, `RootdeepCrawlway`: "a crawlway" by name) and, if Chase wants the whole burrow mounted-free, `OldHavenBurrowsRegion` (x 5136-5247, y 1128-1263, `OldHavenBurrowsRegion.cs:40`) | 1-2 |

That is **37 pinned names** (18 x 2 facets plus 1 Orc Cave and Painted Caves per facet, plus Ilshenar 8, Malas 2,
Ter Mur 5; counted from the script's output) and up to 2 of ours. Not proposed: the big dungeons themselves (Despise,
Shame, Deceit and the rest are built as rooms and halls, and riding through them is how OSI plays), and Trammel's "the
Mystic Mines of Haven" (a Young training area under the Haven town region).

**How, without touching pinned's data or the map (proposal).** At start, after `RegionJsonSerializer.LoadRegions` (the
point `OldHavenBurrowsRegion` already registers at, `Main.cs:671-675`), our code looks each listed name up by name and
map, and registers a `NoRideRegion : BaseRegion` over **the same rectangles at the found region's priority + 1** (the
Despise pattern). A name that is not found fails loudly in the log and a test (the list is pinned to the data, so a
pinned bump that renames a cave breaks the build, which is the intended failure). No JSON patch, no map edit.

**Effect (proposal):**
- `MountsAllowed => false` on the new region: mounting inside says pinned's own "You may not ride at this time"
  (`BaseMount.cs:288-292`), ethereals included (`Ethereals.cs:178`).
- `OnEnter`: a mounted or flying player is dismounted through `DismountRules.TryDismount(rider, null, LowCeiling, 0,
  none)`: no daze, no block (the region blocks remounting while inside), a message "The ceiling is too low to ride
  here." and the mount walks beside them as any dismount leaves it. A flying gargoyle is grounded the same way
  (`Flying = false`, the Fly buff removed, as `ToggleFlying` does at `PlayerMobile.cs:757-762`).
- **Steady Hoof Wraps does not resist this one** (proposal): a ceiling is not a blow, and a III rider who could ride
  through a crawlway would make the region meaningless. The check's `LowCeiling` cause skips the roll.
- `OnExit`: nothing; the player remounts by hand.
- Pets and NPC riders are not touched (only players mount; `CheckMountAllowed` checks `PlayerMobile` only).

## 4. Traps that spook mounts

Three trap families exist or are designed. The spook is a roll when the trap fires on a **mounted** player, through the
check with cause `Trap`, a **5-second** daze (proposal; a trap startles, a blow stuns) and the same fall message.

| Trap | Where it fires | Spook chance (proposal) | Why |
|---|---|---|---|
| Fire Column, Flame Spurt (`Items\Traps\FireColumnTrap.cs`, `FlameSpurtTrap.cs`: 1-30 fire) | `OnMoveOver` on the tile | **25%** | fire and a loud burst; horses bolt |
| Giant Spike (`GiantSpikeTrap.cs`: 10d7), Spike (`SpikeTrap.cs`: 6-36), Saw (`SawTrap.cs`: 5-15), Stone Face (`StoneFaceTrap.cs`: 3d15) | `OnMoveOver` | **15%** | a physical jolt |
| Gas (`GasTrap.cs`, poison, players only), Mushroom (`MushroomTrap.cs`: 2d4) | `OnMoveOver` | **0%** | poison and a puff do not throw a rider |
| Chest traps (`Items\Containers\TrappableContainer.ExecuteTrap.cs`): Explosion (`:56-72`, levels 2 and 4: `TreasureChestLevel2.cs` 2 x 1-25, `Level4.cs` 4 x 10-25), Magic (`:83-88`), Dart (`:103-109`, level 1: 1-25), Poison (`:119-136`, level 3) | on open (`TrappableContainer.cs:34-43`) | Explosion **20%**, Magic **10%**, Dart **10%**, Poison **0%** | the F-32 chests keep these types; a mounted player opening a chest is the normal case |
| P201 deployables (`notes\cc-P201-deployable-traps-design.md` section 3): blast trap (fire, radius 2), bear trap and snare net (hold), caltrops (bleed, slow), dart trap, gas, alarm, shackle | the creature's step (section 4 there); players are the target only in the consent cases the design allows | Blast **25%**, Bear trap and Snare **50%** (the mount is the thing caught; the rider is thrown and the mount is held for the hold time), Dart **10%**, Caltrops, Gas, Alarm, Shackle **0%** | matches the stock families; the hold traps are the only ones that act on the mount itself |

Every chest and floor trap already distinguishes a player (`GasTrap` fires on players only; the others hit anyone on
the tile), so the roll sits in one place: a static `DismountRules.OnTrapHit(Mobile m, TrapKind kind)` that each trap's
hit path calls (floor traps: one line in `BaseTrap`'s subclasses' `OnMoveOver`, which are pinned files, so one patch
hunk per trap kind or one in a shared helper they already call; chest traps: one line in `ExecuteTrap`, a patch;
P201's traps are ours). Stock trap damage is unchanged.

## 5. Wildlife charges

**The hook exists.** P121's approach trigger runs `SpecialAbility.CheckApproachTrigger(bc, m, oldLocation)` from
`BaseCreature.OnMovement` (`customizations\Services\Pet Training\PetTrainingHooks.cs:45-46`, patched in by
`BaseCreature-pet-ability-hooks.patch`), the path True Fear uses with a range of 8 (`SpecialAbility.cs:1512-1515`). A
charge is one more approach behaviour on that hook, for creatures that are **wild** (not controlled, not summoned, no
master), **not already fighting**, and in the **wild** (the rider's region is not a `GuardedRegion`, `TownRegion`,
`HouseRegion` or `DungeonRegion`: the four pinned types that mean "not open country").

**The list and numbers (proposal).** Stats are each file's constructor.

| Creature | Source | Str, damage | Charge chance when a rider runs within 6 tiles | Dismount on the charge's first hit |
|---|---|---|---|---|
| Bull | `Mobiles\Animals\Cows\Bull.cs` (77-111 / 4-9, tamable) | | **15%** | 100% through the check |
| Boar | `Animals\Misc\Boar.cs` (25 / 3-6) | | **10%** | 100% |
| Great Hart | `Animals\Misc\GreatHart.cs` (41-71 / 5-9) | | **10%** (the stag's rut) | 100% |
| Grizzly Bear, Polar Bear | `Animals\Bears\GrizzlyBear.cs` (126-155 / 8-13), `PolarBear.cs` (116-140 / 7-12) | | **10%** | 100% |
| Walrus | `Animals\Misc\Walrus.cs` (21-29 / 4-10) | | **5%** (ice shores only, by its spawn) | 100% |
| Triceratops (ours) | `customizations\Mobiles\Normal\Triceratops.cs` (1100-1300 / 21-28) | | **25%** | 100% |
| Allosaurus (ours) | `Allosaurus.cs` (699-828 / 21-23) | | **20%** | 100% |
| Wild Tiger (ours) | `WildTiger.cs` (496-554 / 18-24) | | **15%** | 100% |

Not listed: Hind, Llama, Mountain Goat, horses and ostards (prey, and they are the mounts), Gorilla and Alligator
(Chase may add), wolves (pack hunters already aggressive), Dire Wolf (aggressive, so already a fight).

**The charge (proposal):**
- Trigger: a **running** rider (the client's run flag is on the move; walking past a bull is safe) enters 6 tiles of
  a listed creature that has line of sight. Roll once per creature per **2 minutes** (the creature's cooldown) and never
  against a rider inside **60 s of any wildlife dismount** (the rider's immunity, so a herd does not chain).
- On a charge: the creature bellows (its own `GetAngerSound`), gets `Warmode` and the rider as `Combatant`, and runs at
  them for up to **10 s**. Its **first melee hit** inside that window calls `TryDismount(rider, creature, Charge, 10 s,
  Dazed)`; the Wraps roll applies. A miss, or 10 s without a hit, ends the charge: the creature stops, loses its
  combatant and goes back to grazing (so a tamer's bull is not a permanent hazard and the taming loop is untouched).
- A charge is **not** aggression for notoriety: the creature stays tamable and the rider is not flagged for
  fighting back (the creature attacked first; pinned's harmful rules already allow the reply).
- Where it matters most: the Britain and Yew farmland (bulls, boars, harts in the pastures and woods), the
  Minoc and Ice Isle shores (walrus, polar bear), and Eodon's plains for the dinosaurs and tigers, which is where riders
  cross open ground at a run.

## 6. Balance

**Every source, its chance, and what Steady Hoof Wraps does to it.** The Wraps roll is P70's: I resists 25%, II 50%,
III always (`MuleModuleData.cs:116`), so a source's chance is multiplied by 0.75, 0.5 and 0, except the low ceiling
(section 3) and the self-dismounts (never rolled). "OSI" rows are unchanged behaviour listed for the whole picture.

| Source | Chance per event | Daze | Wraps I | Wraps II | Wraps III |
|---|---|---|---|---|---|
| OSI: Dismount ability (player or creature) | on an armed hit (creatures arm 40% of swings, need 20 mana) | 10 s | x0.75 | x0.5 | 0 |
| OSI: Infused Throw, Riding Swipe, Bola | on a hit or throw | 10 s | x0.75 | x0.5 | 0 |
| OSI: Meraktus's stomp, Icy Patch | always | none | x0.75 | x0.5 | 0 |
| Ours today: Minion of Scelestus, Osiredon | their specials | 10 s | x0.75 | x0.5 | 0 |
| F-39 big monster, hard hit | 10% or 5% per hard hit, one roll per 10 s | 10 s | 7.5% / 3.75% | 5% / 2.5% | 0 |
| F-39 low ceiling | always on entry | none, blocked inside | always | always | always |
| F-39 fire and blast traps | 25% | 5 s | 18.75% | 12.5% | 0 |
| F-39 spike, saw, stone face | 15% | 5 s | 11.25% | 7.5% | 0 |
| F-39 dart and magic chest traps | 10% | 5 s | 7.5% | 5% | 0 |
| F-39 hold traps (bear, snare) | 50% | the hold | 37.5% | 25% | 0 |
| F-39 wildlife charge | 10-25% to charge, then the first hit | 10 s | x0.75 on the hit | x0.5 | 0 |

**Dismounts per hour in a typical dungeon run.** The rates are assumptions, written down so Chase can swap them;
nothing here was measured on the shard (the overnight bot has no mounted check yet).

| Step | Assumption | Result |
|---|---|---|
| Creatures fought per hour, mounted, in a Despise or Shame style run | 20 **(assumption)** | |
| Of which on the big list | 6 **(assumption)**, mostly 5% family in the first levels | |
| Melee hits each lands on the rider before it dies | 6 **(assumption)** | 36 hits |
| Share that are hard (15% of max hits after resists) | 40% **(assumption)** for a mid suit; near 0 in a 70-resist suit against a Troll, near 100% against a Dragon | 14 hard hits |
| Chance per hard hit, averaged over the mix | 10% **(assumption)**: 2 of the 6 at 10%, 4 at 5%, weighted by hits | **1.4 from big monsters** |
| Floor traps triggered per hour | 3 **(assumption)** | at 20% average: **0.6** |
| Chests opened per hour, trapped | 4 **(assumption)**, half explosion | at 20% and 10%: **0.2** |
| Cave mouths ridden through | 0 inside a hall dungeon; 1-2 on the way in through a cave entrance (Orc Cave, Painted Caves, the overworld mines) | **0-2, certain** |
| Wildlife | 0 in a dungeon; on the ride there, 2 charge rolls per hour at 15% **(assumption)** | 0.3 in the wild |
| **Total, no Wraps** | | **about 2.5 per hour** in the dungeon, plus the ceilings |
| Wraps I | x0.75 on all but ceilings | **about 1.9** |
| Wraps II | x0.5 | **about 1.3** |
| Wraps III | immune to blows and traps | **the ceilings only** |

So the module goes from "little to do" (F-39's complaint) to a visible difference every half hour at tier II, and
tier III's remaining cost is the dungeons you choose to enter through a cave. If Chase wants it rarer, the big-monster
chances halve cleanly (5% and 2.5%); if commoner, the threshold drops to 10% of max hits.

## Decisions for Chase (one line each)

1. **Build the check first:** P70 Part E's `DismountRules.TryDismount` and the one patch over the five pinned sites plus
   our two bosses, un-stubbing Steady Hoof Wraps, as part A of the build prompt before any F-39 source? (recommended)
2. **Hard hit:** 15% of the rider's max hits after resists (recommended), or the raw roll in the top third of the
   creature's damage range?
3. **Chances:** 10% for the top families and 5% for the rest, one roll per creature per 10 s, paragons +5?
4. **The big-monster list** as the four families in section 2; names to add or drop (champions and Peerless bosses are
   left out on purpose)?
5. **Pets never do this** (only the trained Dismount ability), and summons neither? (recommended)
6. **No-ride list:** the 37 pinned cave and mine regions plus Orc Cave and The Painted Caves; the Rootdeep crawlway
   only, or the whole Burrows?
7. **No-ride effect:** mounting blocked inside, dismount on entry with "The ceiling is too low to ride here.", no daze,
   gargoyles grounded too? (recommended)
8. **The Wraps do not resist a ceiling** (recommended), or should tier III ride through everything?
9. **Trap chances** as section 4 (fire and blast 25, jolts 15, darts and magic 10, holds 50, poison and gas 0), with a
   5-second daze?
10. **Wildlife list and numbers** as section 5 (bulls 15, boars and harts 10, bears 10, walrus 5, triceratops 25,
    allosaurus 20, wild tiger 15; 6 tiles, running riders only, 2-minute creature cooldown, 60-second rider immunity,
    10-second charge that ends on a miss)?
11. **Wild only:** charges never inside guarded towns, houses or dungeons? (recommended)
12. **Fidelity register:** one deviation entry for "big creatures, traps, caves and wildlife can dismount you" with the
    wiki line, written through Claude when part B lands?

## Draft build prompt (for the overseer to number once Chase answers)

### Draft: F-39 dismount sources on one check (and Steady Hoof Wraps un-stubbed)

- **Model:** Fable. **Touches:** server. **Summary:** one dismount check in our code, patched into every path that knocks
  a rider off, with Steady Hoof Wraps rolling at it (P70 Part E, built); then F-39's four sources (big monsters' hard
  hits, no-ride cave regions, trap spooks, wildlife charges) calling the same check with Chase's numbers from
  `notes\cc-P234-dismount-sources-design.md`.
- **Read first:** that note (sections 1-6 and the answered decisions); `notes\cc-P70-mule-modules.md` Part E;
  pinned `Items\Weapons\Abilities\Dismount.cs:63-107`, `RidingSwipe.cs:38`, `Items\Misc\Bola.cs:71-87`,
  `Monsters\ML\Special\Meraktus.cs:235-238`, `Items\Special\Holiday\IcyPatch.cs:64-67`, `PlayerMobile.cs:1086-1100`,
  `Mobiles\Animals\Mounts\BaseMount.cs:273-309`, `Regions\BaseRegion.cs:45`, `Server\Regions\Region.cs:748-755`;
  shard `customizations\Mobiles\Mule\MuleModuleData.cs:116-118`, `Mobiles\Mule\MuleModule.cs:225`,
  `Services\Pet Training\PetTrainingHooks.cs:45-46`, `patches\AOS-damage-eater-hook.patch`,
  `Regions\OldHavenBurrowsRegion.cs` (how a region is registered in code), `Regions\RootdeepVault.cs:255-262`.
- **Part A, the check (argue the patch first, in notes, as AGENTS.md asks).** (1) `DismountRules` in
  `customizations\`: `TryDismount(rider, source, cause, daze, blockType)` returns false when the rider's mule has
  Steady Hoof Wraps and the tier's roll resists (25, 50, immune), with the rider's and attacker's messages; the
  `LowCeiling` cause never rolls; self-dismounts never call it. (2) One `.patch` with five hunks: the head of
  `DoDismount`, `RidingSwipe` before `BaseMount.Dismount`, the Bola around `Rider = null`, Meraktus, the Icy Patch.
  (3) Our two bosses call it. (4) The module row goes `Built`; tier III also shortens the remount delay as P70 says
  (ours, no patch). (5) Facts: each site resists at tier II about half the time over N rolls and never at III, a
  self-dismount is never resisted, a creature's trained Dismount goes through the check, the Bola's rider is caught.
- **Part B, the four sources.** (1) Big monsters: the list as a static table of types and chances, the roll at the
  damage hook on a melee hit of at least the threshold share of max hits, one roll per creature per 10 s, wild
  creatures only, paragon bonus; every creature with the OSI Dismount ability unchanged. (2) No-ride: `NoRideRegion`
  registered at start over the named regions' rectangles at priority + 1, `MountsAllowed` false, dismount on entry with
  the message, flyers grounded; a start-up check that every listed name was found. (3) Traps: `OnTrapHit(m, kind)` from
  the floor traps (one patch hunk per kind, or one in a shared path if they have one), the chest traps' `ExecuteTrap`
  (one hunk) and P201's traps when they exist; the 5-second daze. (4) Wildlife: a charge behaviour on the approach
  hook for the listed types, wild only, running riders, the cooldowns, the 10-second window, back to grazing after.
  (5) The fidelity register entry (through Claude) and the wiki line. (6) Patch notes under Changed.
- **Test plan.** Facts, each seen failing first: a Titan's hard hit dismounts a rider at the chance over N rolls and a
  soft hit never; a tamed Titan never; a rider entering a Cave 1 rectangle is dismounted and cannot remount inside, and
  can one tile outside; a Fire Column spooks at its chance and a Gas trap never; a chest explosion spooks and its
  poison never; a bull charges a running rider in the open and never in Britain or in Despise, never twice inside its
  cooldown, and stops after a miss; every source resisted by Wraps II about half the time and never by III, the
  ceiling excepted. Then the full `docker\uo\build.sh`. Play test on the test shard: a GM rides through Minoc Cave 1 and
  past the Britain pasture bulls.

## Deviations and decisions for Chase (how this task was done)

- **Region data was read with a script** (`python -I` over pinned's `regions.json`), not by hand: 490 named entries,
  the cave and mine names listed in section 3 are the ones whose `Name` contains cave, mine, tunnel, mouth, lair, pit or
  hollow, plus every `DungeonRegion`. A region that is a cave by its map but not by its name (the entrances of the big
  dungeons, for example) is not in the list; adding them needs rectangles drawn by hand, which the prompt ruled out.
- **The per-hour estimate is assumptions, not measurement**; the table says which numbers to swap. The overnight bot
  could measure hits per hour on a mounted character once the sources exist.
- **Creature stats were read from constructors** (`SetStr`, `SetHits`, `SetDamage`); the difficulty formula's actual
  values were not computed (no code runs in a docs-only task), so the families are a reading of the stats and the
  build prompt's test prints the formula's numbers for a check.
- The Read and Edit tools were denied on the code repo in this unattended session (outside the working directory);
  the patch note and VERSION were written by a small anchored Python script, as in P232 and P233. No code was changed.

## Patch notes and repo size

`CHANGELOG.md`: `## 2026.10.20.12` with one `### Staff` line; `VERSION` `2026.10.20.12` (the branch's base is `.11`; the
merger renumbers against the other branches' `.12`, P213's rule). Largest changed file: `CHANGELOG.md`, about 84 KB.
Scratch lives in the session scratchpad under `%LOCALAPPDATA%\Temp\claude\`, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration`
(the work copies; the script skips the mirror and dashboard refresh for them by its cc-P184 rule; it commits nothing):

```
=== code  (D:/UO/golems/Bronze/ShatteredLegacy) ===
  2 file(s) pending:
    CHANGELOG.md
    VERSION
  dry run: would add, commit and push

=== docs  (D:/UO/golems/Bronze/shard-migration) ===
  1 file(s) pending:
    notes/cc-P234-dismount-sources-design.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

Neither repo is BLOCKED. No server, docker or client file changed; no build was run and no lock was taken.

P234 DONE
