# cc-P50: The chest mimic as a monster (F-32), from Archaaz's Animated Mimic art

Run 2026-10-12 by Claude Code (autopilot hand-off by hand: Chase said "continue prompt que"). Gates checked at start:
the art and its `SOURCE.txt` are at `D:\UO\third-party\animated-mimic\`; `git -C D:\ShatteredLegacy status --short`
was empty; `D:\UO\ModernUO-pinned` is at `d4531cd94b739613155225c234900de9f47d2c88`; P44 is committed (`completed\`
holds its prompt), so Part B was allowed. P49's notes exist and are cited (section 5.3, 5.5).

**Where the citations come from.** Part A's reading was split across three research subagents in this session (the
art and pipeline, the combat route in pinned and TazUO, the creature's stats); each reported file:line. I re-read
myself every citation the build depends on: the target handler and `Target.Invoke` (3.1 b), TazUO's 0xAA handler and
health-bar option, `MageAI.OnFailedMove` (5.3), the door sounds (5.4), the stock chest tiledata, the Flippable pairs,
and the art geometry (1.3, measured again). The rest is as the agents read it.

Short names: **P** = `D:\UO\ModernUO-pinned\Projects`, **T** = TazUO at our shipped commit,
`D:\UO\cc-p40-work\tazuo-3212623f\src`, **S** = `D:\UO\ServUO-pub57`, **C** = `D:\ShatteredLegacy\server\customizations`,
**pkg** = `D:\ShatteredLegacy\player-package`.

## Summary

| Part A question | Answer in one line | Biggest risk |
|---|---|---|
| 1. The art | 20 BMPs: 6 NS + 6 WE frames (WE an exact mirror of NS) and 8 extras. **Frame 1 is, pixel for pixel, the stock wooden chest** 0xE43 (NS) / 0xE42 (WE). Terms: none stated. | The WE frames and the dead frames needed placement padding to stand where the stock chest stands (done, measured). |
| 2. The pipeline | The P26 route works unchanged: 18 new IDs `0x3C70-0x3C81`, 16 tiledata and 2 animdata records. **Animdata only loops**, in step for every item of an ID, so one-shots (waking, bite, hurt) are server ItemID swaps on a timer. | Swap speed and flicker in a real client are not measured (no client in this session); the server sends a swap within one tick. |
| 3. How it fights | **A hybrid**: a normal mage-AI creature whose body (239) draws nothing, plus an item "shell" on its tile that shows the art and takes the clicks. Targets aimed at the shell land on the creature through **one 7-line patch**; a war-mode double-click attacks; the combatant packet opens the health bar. | Players cannot drag a health bar off the chest (only the attack opens one); a client other than TazUO is untested with body 239. |
| 4. Fallback body | Not needed. A real body would need anim frames for at least 4 actions in 5 directions plus `Bodyconv.def`/`mobtypes.txt` entries, and TazUO has no loose override for them (P40 B.1). | - |
| 5. The creature | Level 4 = OSI's Mimic exactly; levels 1-3 scale down to Gazer/Wisp/Lich class, 5-6 up to Lich Lord/Ancient Lich class. Rooted with `DisallowAllMoves` (as stock Reaper and Corpser), not `CantWalk` alone: **`CantWalk` lets MageAI teleport**. Out of reach: the lid shuts, it takes no damage and heals 5% every 2 s. | The level 1-3 and 5-6 numbers are mine, untested in play. |
| 6. Clashes | No ID clash. Two package tests hard-coded the art counts and ranges (updated). F-32's "stock chest art with a hue per level" does not carry onto the coloured mimic art. | - |

Part B **built** the route: `ChestMimic`, `ChestMimicShell`, `[MimicChest`, the art, the patch and the facts. Build and
test results are in section 8.

## 1. The art

### 1.1 Inventory (counted: 20 images plus SOURCE.txt)

All 20 are uncompressed bottom-up BMPs on pure black (0,0,0), drawn in colour, not a gray palette.

| File | Size | Bits | What it shows |
|---|---|---|---|
| `Animations NS\1-6.bmp` | 50x70 | 32 | 1 closed, 2 teeth showing, 3 mouth open, 4-6 tongue out and lashing |
| `Animations WE\1-6.bmp` | 50x70 | 32 | the same; each WE frame is the exact mirror of its NS frame (0 px differ) |
| `Extra\1.bmp`, `2.bmp` | 50x70 | 32 | the lid alone (1 WE, 2 NS) |
| `Extra\3.bmp`, `4.bmp` | 50x70 | 32 | spike-trap chest (3 WE, 4 NS): frame 1 plus spikes |
| `Extra\5.bmp`, `6.bmp` | 65x70 | 32 | dead, lid flung open, empty |
| `Extra\7.bmp` | 72x76 | 24 | dead, tongue hanging out |
| `Extra\8.bmp` | 72x78 | 24 | the same, other facing |

In the 18 32-bit files alpha is 0 on exactly the pure-black pixels. Every frame has 12 empty rows under the art except
Extra 7 (15) and Extra 8 (16).

**Corrections to the overseer's read:** confirmed 6+6 frames, the order and the Extra pairs. "50x70" holds only for the
animations and Extra 1-4. Extra 7/8 are 24-bit. Frames 3 to 4 differ by only 40 px, so the tongue starts small.

**Which dead pair is which facing** (not in the download): I matched frame 1 of each facing against each dead frame.
Extra 5 and 7 match WE (409 and 371 of 1,043 chest pixels identical, against 24 for NS); Extra 6 and 8 match NS. The
same test put the chest body at x offset 15 (Extra 5), 0 (6), 19 (7) and 3 (8), and 3 or 4 rows up in the tongue frames.

**Terms** (`D:\UO\third-party\animated-mimic\SOURCE.txt`, Chase at download): none stated on the page or in the
download. Treated as community art: credit Archaaz, ship only inside the package, never repost. Nothing forbids edits
or redistribution, so the task went on. The art is built from EA's chest, slith tongue and tooth graphics, so it ships
as our PNGs over placeholder IDs, never in an EA file (client policy).

### 1.2 Frame 1 is the stock wooden chest

Compared in UO's 5-bit colour against all 105 stock art IDs named "chest" plus 0x0E3C-0x0E43, 0x0E75-0x0E80 and
0x09AB, in both `client-data\classic-client` and `classic-client-7.0.117.0` (same result in both):

- **NS frame 1 = 0xE43 "wooden chest": 0 pixels differ**, the same 1,043-pixel mask.
- **WE frame 1 = 0xE42 "wooden chest": 0 pixels differ.**
- Next closest: 0xA761 (993 px differ), 0x0E41 and 0xA305 (1,014), 0x0E40 (1,027).
- Pinned: `P\UOContent\Items\Containers\Container.cs:481` `[Flippable(0xe43, 0xe42)]` on `WoodenChest`.
- Stock tiledata for both (read from 7.0.117.0's `tiledata.mul` this session): flags `0x00204040` (Container |
  ArticleA | Impassable), weight 255, height 4, name "wooden chest".

So **the mimic must spring from a wooden chest** for the change to be seamless, and the shard draws the closed mimic
(resting, lid shut) with the stock art. A client without our package sees a normal chest until it wakes.

### 1.3 Placement (measured)

TazUO puts a static's canvas centre column on the tile centre and its bottom row on the tile's bottom tip (P26 note
section 1). Measured this session:

| | canvas | empty rows under the art |
|---|---|---|
| stock 0xE43 | 50x58 | 12 |
| stock 0xE42 | 50x62 | **16** |
| every NS and WE animation frame | 50x70 | 12 |

So, as shipped, the WE mimic would stand 4 px off the stock WE chest, and the wider dead frames would jump sideways.
`notes\cc-P50-tools\convert_art.py` adds transparent rows or columns, or cuts empty rows, before the converter runs:

| Frames | Placement |
|---|---|
| NS animation | none |
| WE animation | +4 rows under |
| Extra 6 (NS dead) | +15 columns left |
| Extra 8 (NS dead, tongue) | +16 columns left, 4 empty bottom rows cut |
| Extra 5 (WE dead) | +15 columns right, +4 rows under |
| Extra 7 (WE dead, tongue) | +16 columns right, 3 empty bottom rows cut, +4 rows under |

No pixel of the art changes. A preview with the stock chest's outline drawn over each frame (scratch, not committed)
showed the chest body on the outline in all 18 frames, both facings, dead ones included.

### 1.4 The states, filled in

| State | When | Shown as (built) | IDs (NS / WE) |
|---|---|---|---|
| Resting | before it springs | the chest itself (P49 5.3); after a spring, the shell shows the chest's own graphic and hue | the chest's |
| Waking | once, when the chest changes, and when the lid reopens | teeth, then mouth open, 250 ms each, then idle | 0x3C70, 0x3C71 / 0x3C79, 0x3C7A |
| Idle | in the fight | animdata loop: teeth and mouth open, interval 4 (about 400 ms a frame) | 0x3C75 / 0x3C7E (frame 2 at +1) |
| Bite / cast | each melee hit it gives and each spell it casts | tongue 1, 2, 3, 2, mouth open, 150 ms each, then idle | 0x3C72-74, 0x3C71 / 0x3C7B-7D, 0x3C7A |
| Hurt | a hit of 5% of its hits or more | teeth, closed, teeth, 120 ms each (a shudder) | 0x3C70, 0xE43 / 0x3C79, 0xE42 |
| Lid shut | an attacker it cannot reach (section 5.4) | the stock closed chest | 0xE43 / 0xE42 |
| Dead | on death | the corpse takes one of the two dead tiles at random | 0x3C77 or 0x3C78 / 0x3C80 or 0x3C81 |

**Missing from the art:** a real hurt frame (the shudder borrows frames 2 and 1); a hue flash was rejected because the
art is coloured and a hue repaints the whole sprite. The lid alone (Extra 1-2) is unused. **The spike-trap chest
(Extra 3-4) is a candidate look for F-32's trapped chests: for P49's build, not built here.**

## 2. The item-art pipeline

**Same route as P26 and P34**, nothing new in it:

- PNGs in `pkg\vendor\shattered-legacy-art\art\<decimal id>.png`, made by `scripts\anchor-art-frames.py --keep-geometry
  --black-transparent` (called by `notes\cc-P50-tools\convert_art.py`), which re-reads each PNG and checks it pixel for
  pixel against its (placed) source.
- `registry.csv`: 18 rows, `none stated; see SOURCE.txt`, source naming Archaaz and the BMP.
- `records.json`: 16 tiledata, 2 animdata. `SOURCE.txt`: an Archaaz section.
- Server copy of the tiledata: `ChestMimicArt.Records`, applied by `ShatteredLegacyArt.Apply` (so the shell blocks on
  the server as on the client; the server reads EA's unpatched tiledata otherwise).

**IDs: 18, `0x3C70-0x3C81` (15472-15489).** `find-free-art.py --placeholder --run 26 --from 0x3C00 --to 0x3E00` found
`0x3C6F-0x3D11` free (163 IDs); `--check-registry` after the change: **"0 of 112 registered IDs are no longer free"**.
Nine per facing (NS at `0x3C70`, WE at `0x3C79`): +0..+4 stills (frames 2-6), +5 the idle loop's base (frame 2), +6
its second frame (frame 3, no record, never an item's ID), +7 and +8 the dead tiles. Frame 1 is not shipped.

**Can a one-shot play once and stop? No.** An animdata record is 64 frame offsets, a count, an interval and a start
byte (`T\...\AnimDataLoader.cs:56-63`); the start byte is never read, and `AnimatedStaticsManager.cs:105-108` wraps the
frame back to 0. The frame counter is one per graphic (`:102`), so every item of an ID animates in step, and an item
switched onto an animated ID joins mid-cycle. Hence: the idle state is a loop, every one-shot is a server swap.
A fixed graphic effect (packet 0x70/0xC0) does start at frame 0 (`T\...\GameEffect.cs:24-26`) and was the other
option; it would need its own frame IDs and the item hidden while it plays. Not built.

**How fast a swap reaches clients.** `Item.ItemID`'s setter queues `Delta(ItemDelta.Update)` (`P\Server\Items\Item.cs:628-645`),
sent by `Item.ProcessDeltaQueue` once per main loop (`P\Server\Main.cs:721`), before the same loop's network slice
(`:730`). TazUO updates the existing item's graphic in place (`T\...\ObjectHelpers.cs:104-170`), not by recreating it,
so a swap should not flicker. **Unverified in a client**: no client ran in this session. Chase's checklist covers it.

## 3. How something drawn as item art fights

### 3.1 The candidates

**(a) A creature whose body draws nothing.**
- In TazUO a mobile is drawn from its animation frames; with none, nothing is drawn (`T\ClassicUO.Renderer\Animations\Animation.cs:154-170`,
  `MobileView.cs:721-723`).
- **But TazUO picks a mobile only by the pixels of its drawn frame**: `CheckMouseSelection` needs the mouse inside the
  frame, then a per-pixel check (`MobileView.cs:1112-1125, 1214-1235`). A frameless mobile can never be selected: no
  single click, no target cursor, no double click, no health bar dragged off it. Only TazUO's optional nameplates reach
  it (`NameOverheadGump.cs:387-520`).
- Hue 0x4001 is not invisible: TazUO keeps the 0x4000 bit and draws a dark translucent ghost (`Entity.cs:97-107`,
  `ShaderHueTranslator.cs:53-55`). Hidden is out: a player cannot target what they cannot see (`P\Server\Targeting\Target.cs:181-184`).
- **Body 239.** I listed every body 1-2047 with no data anywhere in 7.0.117.0 (`anim*.idx` entries, `AnimationFrame*.uop`
  hashes, and not named in `Body.def`, `Bodyconv.def` or `mobtypes.txt`): **596 bodies**, the first 239, 274, 275,
  294-299. Pinned's `bodyTable.cfg` does not list 239 and no script uses it; the server types it `BodyType.Empty`
  (`P\Server\Mobiles\Body.cs:77`), which only matters for summoned creatures' notoriety (`P\UOContent\Misc\Notoriety.cs:444`),
  so it shows as any stock monster does. Script: `scratchpad\p50\emptybody.py` (not committed).
- **So (a) alone fails**: nothing can be clicked.

**(b) The item takes the clicks and forwards them.**
- Spells: `SpellTarget<Mobile>` refuses an item (`P\UOContent\Spells\Targeting\SpellTarget.cs:7-9, 41-42`), and
  `Target.Invoke` stops there before any item hook runs (`P\Server\Targeting\Target.cs:163-178`; `Item.CheckTarget` is
  only reached at :198). Pets' "all kill" takes only `o is Mobile` (`AIControlMobileTarget.cs:31-33`). **No override
  can forward a target.** The one clean point is the target packet handler, right after it resolves the serial
  (`P\UOContent\Network\Packets\IncomingTargetingPackets.cs:120-123`).
- Attacks: TazUO sends an attack request only for a mobile serial (`T\...\GameActions.cs:681-685`); double-clicking an
  item sends a use request, which reaches `Item.OnDoubleClick` (`P\Server\Items\Item.cs:4450`).
- Health bar: none can be dragged off an item. **But the server's combatant packet opens one**: setting a player's
  `Combatant` sends 0xAA (`P\Server\Mobiles\Mobile.cs:753`); TazUO's handler sets `LastAttack`
  (`T\ClassicUO.Client\Network\PacketHandlers\AttackCharacter.cs:12`), which opens a health bar when the default option
  `OpenHealthBarForLastAttack` is on (`T\...\TargetManager.cs:177-193`; default true, `Profile.cs:714`).

**(c) Anything better.** ServUO's damageable items are core-wide plumbing (world packet type 3 for IDamageable items,
`S\Server\Network\Packets.cs:1346-1349`; `S\Scripts\Items\Damageable\DamageableItem.cs:19`); pinned has no IDamageable,
so porting it is a large core change. Pinned has no Mimic. Nothing better found.

### 3.2 Recommended and built: the hybrid

A normal `BaseCreature` (body 239) and a `ChestMimicShell` item on its tile:
- the shell shows every state and takes the clicks; its `ItemID` is what the server swaps;
- `ITargetRedirect` on the shell, and **one hunk** in the target packet handler: an item that implements it hands the
  target to the mobile it names (`server\patches\IncomingTargetingPackets-target-redirect.patch`, 7 added lines). That
  covers spells, area spells cast on it, pets' commands, taming (for F-32), provocation and last-target macros;
- a war-mode double-click on the shell calls `from.Attack(mimic)`, as the attack request does
  (`P\UOContent\Network\Packets\IncomingPlayerPackets.cs:69-83`); the combatant packet opens the health bar;
- single click shows the mimic's own label in its notoriety colour (`OnSingleClick` forwards);
- everything else is the stock creature: damage, resists, notoriety, aggression, the corpse, loot rights.

**The patch argument** (AGENTS.md: a pinned change only as a patch, argued first): there is no hook. `Target.Invoke`
decides by the object's type before any virtual on the item runs, and the handler is a static packet function. The
alternatives were a creature body (section 4) and ServUO's damageable items (3.1 c); both are far larger. The hunk only
acts for an item that opts in, so no other item changes behaviour. Named in `apply-patches.sh` with this reasoning.

**What an unpatched or other client shows:** without our package, the stock chest until it wakes, then OSI's gray
"UNUSED" placeholder for each mimic ID (the P26 situation). Body 239 in a client other than TazUO: **unverified**.

## 4. Fallback: a real creature body (not needed)

Sized only. A new body needs frames for at least stand, attack, hit and die in five directions (mirrored to eight)
written into `anim*.mul` or `AnimationFrame*.uop`, plus `Body.def`/`Bodyconv.def` and `mobtypes.txt` lines. P40 B.1
found TazUO has no loose override for creature bodies, so it would mean shipping a patched animation file (our
`sl-anim7` route, P62, carries worn-item animations through `Bodyconv.def`, and a creature might ride the same slot
mechanism) and hand-drawing the missing directions, since Archaaz's art has two facings and no walk or die sequence.
Days of art work for nothing the hybrid lacks.

## 5. The creature

### 5.1 OSI's Mimic, verified

`S\Scripts\Mobiles\Normal\Mimic.cs` (97 lines): AI_Mage, FightMode.Closest, perception 10, fight range 1 (:11); body 729
(:14); Str 281, Dex 140, Int 261 (:16-18); 543 hits (:20); damage 13-20 (:22), 20% each of the five types (:24-28);
resists 63/43/36/37/42 (:30-34); EvalInt 100, Magery 107.5, Meditation 100, MagicResist 126.5, Tactics 98.5, Wrestling
92.2 (:36-41); PackReg(20) (:43); FilthyRich x4 plus MedScrolls (:53-54); 3% LuckyCoin (:56-62); sounds idle 1561, anger
1558, hurt 1560, death 1559 (:65-83). **Fame, Karma and VirtualArmor are not set (all 0).** Every brief figure is right.
Body 729 is a pink king crab (P49 5.4), not a chest.

### 5.2 Stats by chest level (built as data: `ChestMimic.Levels`)

Damage 20/20/20/20/20 at every level. Resists P/F/C/Po/E. The bard difficulty column is pinned's
`BaseInstrument.GetBaseDifficulty` formula (`P\UOContent\Items\Skill Items\Musical Instruments\BaseInstrument.cs:249-305`)
at the hits midpoint, the input F-14 will map to a creature level.

| | L1 | L2 | L3 | L4 (OSI) | L5 | L6 |
|---|---|---|---|---|---|---|
| Hits | 90-110 | 180-220 | 330-370 | 543 | 750-800 | 1000-1100 |
| Str/Dex/Int | 110/75/120 | 160/85/160 | 220/110/210 | 281/140/261 | 330/150/400 | 400/160/550 |
| Damage | 5-9 | 8-12 | 10-16 | 13-20 | 16-23 | 19-27 |
| Resists | 30/20/15/15/20 | 40/28/22/23/28 | 52/35/29/30/35 | 63/43/36/37/42 | 68/50/45/45/50 | 72/57/52/52/57 |
| EvalInt/Magery/Med | 50/55/50 | 70/72/70 | 90/90/85 | 100/107.5/100 | 110/115/105 | 120/120/110 |
| Resist/Tactics/Wrestling | 60/50/50 | 85/70/65 | 105/85/80 | 126.5/98.5/92.2 | 145/105/100 | 165/110/110 |
| Fame (Karma the negative) | 3,000 | 6,000 | 10,000 | 15,000 (OSI: 0) | 19,000 | 23,000 |
| Virtual armor | 30 | 36 | 44 | 50 (OSI: 0) | 55 | 60 |
| Bard difficulty | 77.0 | 88.1 | 99.5 | 112.5 | 128.2 | 146.1 |

One line each:
- **L1** crate tier for new players, beside Gazer and Gargoyle (75.8 and 78.6). Magery 55 casts circles 1-4.
- **L2** Wisp class (88.8). Magery 72 adds Energy Bolt and Explosion. About double L1's hits.
- **L3** between Lich and Elder Gazer (94.4 and 96.5). Magery 90 first reaches Flamestrike.
- **L4** OSI's Mimic, except Fame and armour, which OSI leaves at 0. 15,000 matches Ogre Lord; 112.5 matches Lich Lord (112.8).
- **L5** about +40% hits, higher resists and resist skill. Magery above 94.3 adds no new spell (MageAI's circle cap,
  `P\UOContent\Mobiles\AI\MageAI.cs:278-295`), so the extra threat is hits, Int and damage.
- **L6** Ancient Lich class (145.6, Fame 23,000). Resists kept at 72 or below.

Comparables cited from pinned: Gazer.cs:19-38, Gargoyle.cs:19-39, Wisp.cs:24-46, Lich.cs:19-45, ElderGazer.cs:18-41,
LichLord.cs:19-45, AncientLich.cs:19-46 (all under `P\UOContent\Mobiles\Monsters\`).

**Deviation from OSI, for `docs\fidelity-principle.md` (the overseer's to write):** Fame/Karma and VirtualArmor set at
L4 where OSI's are 0, so the creature gives fame and karma like any other of its strength. The whole creature is ours
(OSI's Mimic is a crab that does not come from chests), so the rest is not a deviation but new content.

**Loot:** out of scope. OSI's Mimic's loot (FilthyRich x4, MedScrolls, 20 reagents, 3% LuckyCoin) stands in at every
level until F-32 sets its own. `LuckyCoin` is ours (`C\Items\Quest\LuckyCoin.cs:7`).

**F-14 level:** not built anywhere (no `CreatureLevel`, `ConColor` or `GetBaseDifficulty` use in `C`). F-14 will compute
it from the stats, so `ChestMimic` declares only its `ChestLevel` (1-6), a separate field.

### 5.3 AI, and why `DisallowAllMoves` and not `CantWalk`

- **`CantWalk` alone is unsafe on mage AI.** It blocks steps (`P\UOContent\Engines\Pathing\Movement.cs:496, 525, 554`)
  but a failed move calls `OnFailedMove`, which casts Teleport (`MageAI.cs:210-219`), and Teleport sets the location
  directly (`P\UOContent\Spells\Third\Teleport.cs:73`). The dispel branch also picks Teleport (`MageAI.cs:357-359`).
  Both are gated only by `!DisallowAllMoves`.
- **`DisallowAllMoves`** is how stock roots the Reaper (`...\Plant\Magic\Reaper.cs:53`), the Corpser and the Harrower's
  tentacles. With it, every move path returns early (`P\UOContent\Mobiles\AI\AIMovement.cs:130, 184-186, 365, 464, 613,
  705`; `WalkRandomLogic.cs:25, 54`); in combat a failed run re-acquires a target instead of teleporting
  (`MageAI.cs:223-228`) and **it keeps casting whenever its target is in spell range** (`:776-783`). Out of line of sight
  it simply does not cast (`:700-711`); past its perception it changes or drops target (`:673-692`). It does not stall.
- **Flee:** MageAI flees at 20% hits with a 10% chance (`MageAI.cs:23-24`), and fleeing only moves, never casts
  (`BaseAI.cs:633-648`): a rooted mimic would sit silent. **`CanFlee => false`** (`BaseCreature.cs:1444`, checked at
  `BaseAI.cs:793`).
- **Belt and braces:** `OnMove(Direction) => false` (`P\Server\Mobiles\Mobile.cs:4116`), and `Home` = its tile,
  `RangeHome` = 0. The return-home logic needs it away from home first (`BaseCreature.cs:3918-3926, 4202-4206`;
  `BaseAI.cs:1176-1191`), so nothing moves it. Not audited: monster abilities of other creatures that move mobiles.
- **Invisibility:** MageAI casts it (`MageAI.cs:444-457`). Hidden, it could not be targeted at all, so
  `OnHiddenChanged` undoes it on the next tick.

### 5.4 Out of reach: the lid shuts

A creature that cannot move can be cheesed from range. Its **reach** is its perception (10 tiles, OSI's Mimic's) in line
of sight. When it takes damage from someone it cannot reach, and none of its attackers (its combatant or any aggressor
of the last two minutes) is in reach, **the lid snaps shut**:
- it shows the closed chest, plays a dark wood door's close sound (0xF1; 0xEA opens it; `P\UOContent\Items\Construction\Doors\Doors.cs:150-151`,
  `BaseDoor.cs:64` names the order) and emotes;
- it takes no damage (`CanBeDamaged() => false` while shut; checked in `Mobile.Damage` and `Kill`, `Mobile.cs:5954-5963,
  4717`). **Not `Blessed`**: that would stop it attacking and turn the health bar yellow (`Mobile.cs:8340, 1114-1123`);
- it heals 5% of its hits every 2 seconds;
- it opens again (door-open sound 0xEA, then the waking frames) as soon as any attacker is in reach.

The hit that makes it shut still lands. Chase may want a different heal rate (section 10).

### 5.5 Sounds (stock, by ID)

OSI's Mimic's own set, which no pinned creature uses: idle 1561 (0x619), anger 1558 (0x616), hurt 1560 (0x618), death
1559 (0x617), wired through `GetIdleSound` etc. The bite plays through the stock attack sound and the AI's own casting;
the lid uses 0xEA and 0xF1. **How they sound is unverified until heard.**

### 5.6 The swap, chest to mimic, in one step

`ChestMimic.Spring(chest, level)`: the mimic is built at the chest's level with the chest's facing; `MoveToWorld` to the
chest's tile creates the shell there **showing the chest's own graphic and hue**; then `chest.Internalize()`
(`P\Server\Items\Item.cs:2689-2692`); then the waking frames. Mobile and item world packets go out immediately
(`Mobile.cs:2592-2645`; `Item.cs:1174-1240, 1553`), so a client receives the mimic, the shell (looking like the chest, on
the chest's tile) and the chest's removal from the same call: no moment with neither, and the moment with both shows
two identical chests on one tile. **Unverified in a client.**

**What F-32 needs, per P49 5.3:** the internalized chest is the record (type, level, items, and its own location
kept by the spawner). `ChestMimic` keeps `SourceChest` and its `HomeMap`, and calls `IMimicSource.OnMimicGone(mimic,
killed)` when it goes, if the chest implements it. A chest that does not (a stock chest staff turned with
`[MimicChest`) has its contents moved into the corpse on death and is then deleted; on a staff delete it is put back on
its tile.

## 6. Clashes

- **P36:** none (no shared file).
- **P49:** agrees with P49 5.3 (spawn the creature only at spring time, internalize the chest, `SourceChest` plus a
  delete callback). One difference: P49 expected "a `ChestMimic`" to be the whole thing; it is two objects here, and
  "nothing left behind" means the shell goes with the mimic (it does: facts 6 and 7). F-32's tame (P49 5.5) needs the
  redirect for the taming target, which this patch already gives.
- **F-32 decision (15), stock chest art with a hue per level:** the mimic springs best from an **unhued wooden chest**
  (0xE43/0xE42). A hued or other chest still works (the shell starts as that chest), but the waking frames are the
  wooden-chest mimic, unhued: the art is coloured and a hue would repaint it whole. F-32 should keep mimic-capable
  chests as wooden chests, or accept the change of look.
- **The F-8 art registry:** no ID clash (highest before was 15470). Two package tests hard-coded the counts (94 rows,
  92 art rows) and assumed only one record outside the runestone and winter ranges; both updated, and the winter fact's
  animdata filter bounded to its own range. A new fact checks the mimic's records against `ChestMimicArt.Records`.
- **Install steps (P44, P35):** none changed. `Build-UoOverrides.ps1:201-219` skips an animation if any of its frames has
  a record; the loop's second frame has none (a fact checks it).

## 7. What Part B built

**`D:\ShatteredLegacy`:**
- `server\customizations\Mobiles\Normal\ChestMimic.cs`: `ITargetRedirect`, `IMimicSource`, `ChestMimicArt` (IDs,
  records, facing table), `ChestMimic` (levels as data, states, lid, swap, `[MimicChest`), `ChestMimicShell`.
- `server\customizations\ShatteredRunestone.cs`: `ShatteredLegacyArt.Apply` also applies `ChestMimicArt`.
- `server\patches\IncomingTargetingPackets-target-redirect.patch` and its `apply_patch` line with the argument.
- `server\tests\Mobiles\Normal\ChestMimicVerification.cs`: 8 facts.
- `player-package\vendor\shattered-legacy-art\`: 18 PNGs, 18 registry rows, 16 tiledata and 2 animdata records,
  `SOURCE.txt` section.
- `player-package\tests\Build-UoOverrides.Tests.ps1`: counts, ranges, and the new mimic fact.
- `CHANGELOG.md` (2026.10.12.6, a staff line) and `VERSION`.

**`D:\UO\shard-migration`:** this note and `notes\cc-P50-tools\convert_art.py`.

Facing of other stock chests: the first ID of each pinned `[Flippable(a, b)]` chest/crate pair faces as 0xE43 does
(checked on a render of the eight pairs, scratch); `ChestMimicArt.FacingOf` uses that.

**Not tameable** (`Tamable = false`); **PetMimic untouched** (fact 7 checks no field, property or method of the three
classes mentions it, and no PetMimic appears in the world across a spring and a kill).

## 8. Build and tests

All through `docker\uo\build.sh -t sl-modernuo:cc-p50`; `sl-modernuo:latest` not moved, nothing deployed or restarted.
Logs in `D:\UO\cc-p50-build*.log` (not committed).

| Run | What | Result |
|---|---|---|
| 1, 2 | first builds | compile errors, fixed: `OnLocationChange`/`OnMapChange` are protected in BaseCreature; an xUnit analyzer rule (`Assert.Empty` on a filter) |
| 3 **red** (`--tests-only`) | `ChestMimic.cs` deliberately broken three ways: every level given level 1's row, the shell never made, the art records never applied | **all 8 mimic facts failed**, each for the broken reason (543 expected, 103 actual; null shell; tiledata not Impassable). Also failed: `WispOrbPossessionVerification...(ForestNymph, Phantom)`, the known flaky fact (D56; P52 notes, headline 7), unrelated |
| 4 | the real file restored | 1050/1052: two real findings, below |
| 5 (`--tests-only`) | diagnosis | the move fact fixed; the facing defect found |
| **6** | full build | **1052/1052 passed, image `sl-modernuo:cc-p50` built** ("Built sl-modernuo:cc-p50 with patches applied and 1052 shard test(s) passing"; "All 64 patches applied successfully") |

**What run 4 found:**
- **A real defect:** a west-east mimic showed the north-south idle art. The base constructor places a new mobile on the
  internal map through the same virtual map-change path, so the shell was made **before** the constructor set the
  facing. Fixed: the shell is never made on the internal map, only when the mimic is placed in the world.
- **A wrong fact:** `Mobile.Move` turns a creature that faces another way and returns true without stepping (pinned
  `Mobile.cs:4340`). The fact now asks twice per direction (turn, then the real step, refused) and checks the tile
  never changes.

**Package tests:** `player-package\tests\Build-UoOverrides.Tests.ps1`: **12 facts, 12 passed** (one failed first: the
winter fact's animdata filter had no upper bound and took in the mimic's loops; bounded). `find-free-art.py
--check-registry`: **0 of 112 registered IDs are no longer free**. `Build-PlayerPackage.ps1` was not run (it builds the
package); its PNG-count and registered-ID gates are the same checks the package tests make.

**Facts (`server\tests\Mobiles\Normal\ChestMimicVerification.cs`), all watched red then green:**
1. Each level 1-6 constructs with its row of `Levels`; level 4 is OSI's Mimic (543 hits, Str 281, Magery 107.5,
   Resist 126.5); levels 0 and 7 are refused.
2. It round-trips with its level, facing, shell and chest; the shell round-trips with its mimic and graphic.
3. A chest becomes a mimic on its tile and facing (0xE43 to NS, 0xE42 to WE): mimic and shell on the chest's tile,
   chest on the internal map, the first waking frame showing and the chest's hue cleared. A chest not on the ground is refused.
4. Every state shows the registered IDs in both facings; the shut lid shows the stock chest, refuses damage and blocks
   one-shots; the lid opens into the waking frames.
5. It never leaves its tile (`DisallowAllMoves`, no flee, home range 0, shell on the same tile).
6. Death: the corpse is a dead-mimic tile on the chest's tile, holds the chest's gold, and the shell and the chest are
   gone. A staff delete puts the chest back where it stood and leaves nothing. Deleting the shell deletes the mimic.
7. A target on the shell lands on the mimic, and on nothing once it is dead; no field, property or method of
   `ChestMimic`, `ChestMimicShell` or `ChestMimicArt` mentions PetMimic, and no PetMimic appears.
8. The server's tiledata for the 16 records is ours; the stills and loops block, the dead tiles do not, the loops'
   second frames have no record; the facing table.

**Not testable on the test host:** anything a client draws (swap flicker, alignment in game, the health bar), the AI
in a real fight (timers do not run there), line of sight on real map data. Chase's checklist covers them.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last change:

```
Repo Result
---- ------
code dry run
docs dry run
```

29 files pending in code (18 PNGs of 4 KB or less), 2 in docs. Nothing refused.

## 9. Checklist for Chase (test shard, `sl-modernuo:cc-p50`)

1. Install the updated player package on the test client (the 18 PNGs and records go in through the existing patch step).
2. `[add ChestMimic` (level 4) and `[add ChestMimic 1`: it appears as the idle mimic, mouth breathing. **Click it**: its
   name in red. Hover with tooltips on: its name.
3. Fight it in war mode by **double-clicking it**: a health bar should open (TazUO's "open health bar for last attack",
   on by default). Watch: **bite** frames when it hits or casts, a **shudder** on a big hit, the **waking** frames after the
   lid opens. Look for flicker on each swap.
4. **Spells**: a single-target spell (Magic Arrow) on the chest, an area spell (Chain Lightning) beside it, and a pet's
   "all kill" on it: all should hit the mimic.
5. **Range**: step back past 10 tiles or behind a wall and shoot it: the lid should **snap shut** (emote and sound), take no
   damage and heal; walk back in: it creaks open and fights again. Recall away and back: it is still on its tile.
6. **Kill it**: the corpse is a dead mimic (lid flung open, sometimes the tongue out), lootable as usual.
7. **A chest that comes alive**: `[add WoodenChest`, put something in it, `[MimicChest 2` and target it: it should change
   on the spot, same facing (try both facings by flipping the chest first), with no blink. Kill it: the chest's
   contents are in the corpse. Do it again and `[delete` it instead: the chest comes back.
8. **An unpatched client** (no package update): the chest before it wakes, then OSI's gray "UNUSED" placeholder.
9. Check the **WE facing** stands on the stock chest's spot (the 4 px placement fix) and the dead tiles do not jump sideways.
10. Listen: sounds 1558-1561 (OSI's Mimic's), 0xEA/0xF1 (the lid). Say if any are wrong.

## 10. Numbers and choices that still need Chase

1. **Level 1-3 and 5-6 stats** (section 5.2): mine, scaled from comparables; level 4 is OSI's. Tune in play.
2. **Fame/Karma and virtual armour at level 4** where OSI's are 0: keep (it then gives fame like its peers) or set 0.
   Either way, a line for `docs\fidelity-principle.md` (overseer).
3. **The lid**: reach 10 tiles, heals 5% every 2 s while shut, the shutting hit still lands. All tunable.
4. **Hurt threshold** (a hit of 5% of its hits) and the frame timings (250 / 150 / 120 ms, idle loop interval 4).
5. **Loot**: OSI's Mimic's loot stands in at every level until F-32 sets its own.
6. **The name**: "a chest mimic", corpse "a dead chest mimic" (OSI's "a mimic" left free for a port of OSI's creature).
7. **F-32's hued chests** (decision 15): mimic-capable chests should be unhued wooden chests for a seamless change, or
   accept that the waking mimic is the unhued wooden-chest art (section 6).
8. **Peace-mode double-click** on it says "That chest is alive!" and does not attack (as UO, where only war mode attacks).
   Say if it should attack.

P50 DONE
