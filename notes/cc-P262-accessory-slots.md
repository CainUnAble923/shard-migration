# cc-P262: accessory slots (extra rings, bracelets, toe rings), server first

Copper, 2026-10-21. Brief: `D:\UO\cc-prompts\claimed\Copper\cc-P262-accessory-slots.md`. Spec:
`D:\UO\cc-prompts\design\accessory-slots-spec.md` (decided 2026-10-11). Context:
`D:\UO\cc-prompts\design\f-exploit-achievements-accessory-slots.md`. Code repo branch `golem/Copper/P262`, based on main
`2ab20d7`. Not committed (the Golem commits).

**Pinned source.** `D:\UO\ModernUO-pinned` is not on this PC. I read pinned from two patched build trees:
- `sl-uo-builder:cc-P231`, copied to the session scratchpad;
- `AOS.cs` and `PlayerMobile.cs` from `sl-uo-builder:cc-P278`, which is main with P238. Both patches were generated
  against that tree.

## Headlines

1. **Built, player side:**
   - an invisible **accessory container** on the unused layer 0x0F, holding extra rings, a second bracelet and toe rings;
   - their attributes, resists, skill bonuses and stat bonuses count like paperdoll jewellery, and every stock cap still
     applies;
   - a **`[accessories` gump**;
   - **toe rings** (Tinkering, under the recipe gate), **Plate Socks**, and the **Singed** and **Mood Toe Rings**;
   - five **hidden achievements** in P231's shared Mischief ("Noted by the System") category, plus the title
     **"the Unshod"**.
2. **Slots, now:**
   - toe rings work today (their two achievements unlock them);
   - the second bracelet works today, at League rank 9 (a setting);
   - the extra ring slots wait for loops (F-12 is not built), behind `clusterf.accessories.loopSlotsEnabled` (false). The
     gump shows each locked slot's hint.
3. **Stubbed:** companions do not exist yet. Their side is code ready for the companion type:
   - slots by companion rank;
   - the foot lines, as data, word for word from the spec;
   - the Equip, Smothered and Bare calls;
   - Hot and Cold with their cooldowns.

   There is **no companion personality field** in this build, so a companion reads as Stoic, as the spec says for one
   with none set. The "Accessories" **context-menu entry is not built**: no cliloc reading "Accessories" could be
   verified on this PC (see "Stubbed").
4. **Two new pinned patches, both small:**
   - `AOS-accessory-container-aggregation.patch`: 1 hunk in `AosAttributes.GetValue`;
   - `PlayerMobile-accessory-hooks.patch`: 2 one-line hunks in `OnItemAdded` and `OnItemRemoved`.

   Resists need no patch. The container reports its jewels' resists through its own `PhysicalResistance`..., which
   `Mobile.ComputeResistances` already reads for every worn item.
5. **Tests:** 7 facts in `server\tests\Misc\AccessorySlotsVerification.cs`, each seen failing first. In the red run, 7
   marked breaks gave exactly these 7 failures. `AchievementEarnedLineVerification`'s two counts moved from 95 to 100 for
   the 5 new achievements. Full `docker\uo\build.sh -t sl-modernuo:cc-P262`: **1,924 tests, 1,920 passed, 0 failed, 4
   skipped; image built.**

## The "today" report (spec: before building, report how these work today)

| Topic | Today (read 2026-10-21) | Used |
|---|---|---|
| **Equipped property totals** | Attributes go through `AosAttributes.GetValue(Mobile, AosAttribute)` (`Misc/AOS.cs:644`). It sums the `Attributes` of every item in `m.Items`, weapon, armour, jewel, clothing, spellbook, quiver and talisman. Shard hunks add set bonuses, PetMimic, Pet Training debuffs and the grapes of wrath. A container's contents are **not** in `m.Items`. **Skill bonuses** are SkillMods added by the item's own `OnAdded(Mobile)` (`BaseJewel.cs:326`: `SkillBonuses.AddTo`, plus Str, Dex and Int StatMods named by serial) and removed by `OnRemoved`. They are not saved; `BaseJewel` re-adds them on load. **Resists** come from `Mobile.ComputeResistances`, which reads each worn item through the shard's `GetItemResistance` virtual (`Mobile-set-item-resistance-hook.patch`); that returns `item.PhysicalResistance` and the rest | All three: a GetValue hunk, the jewel's own `OnAdded`/`OnRemoved` called with the wearer, and the container's own resistance properties |
| **Squire and merc companions, personality** | **None.** No companion type exists: `grep "class \w*Companion"` over `server/customizations` finds nothing, and P41 and P45 are research and probes. "Personality" appears only in three achievement and loot box text lines. **There is no personality field** | The companion side is built as code ready for the type (below). Personality is an injectable `AccessoryFootLines.PersonalityOf`, Stoic when unset |
| **Achievement system** | `ClusterFAchievements.cs`. Achievements are registered with `Reg` (key, title, description, category, AP, Renown, trigger, flavor, hidden, prerequisite, progress counter). Account-wide counters use `Increment`. Granting goes through `GrantCounted`/`GrantEvent` and `TryGrant`. `TriggerKind` drives the "(Earned: ...)" line. P231 added the hidden **Mischief** category (enum value 9, no tab of its own, listed under All) for joke achievements. **Titles** are `LeagueTitles` (`LeagueShop.cs`, cc-P229), held per account and shown through `Mobile.Title` | All five achievements are in Mischief, so "Noted by the System" is shared, not doubled. Five new trigger kinds with their Earned lines. "the Unshod" is a new `LeagueTitles` row |
| **Loop tracking, companion rank** | **Neither exists.** F-12 player levels and loops are not built (`ClusterFAccountData.cs:110`: "Once per loop is once per character until loops exist"). There is no companion rank | Ring slots are locked behind `loopSlotsEnabled`, with `LoopOf` returning 0 (`LoopOverride` for tests). Companion rank thresholds are settings ready for the type |
| **League rank** | **Exists:** `PlayerMobile.LeagueRank` (`ClusterFLeagueRanks.cs:809`), 1 to 17. The ladder is one rank per metal from Iron to Celestial, Dawnstone excluded (`TopRank = Ladder.Count`; 17 counted from the `CraftResource` enum, `ResourceInfo.cs:9-27`) | Bracelet slot 2 at rank `braceletLeagueRank`, default 9 (Valorite Citizen, the middle of 17) |
| **Recipe gating** | **Exists:** cc-P78, `Engines/Craft/ClusterFRecipeGate.cs`. Every Tinkering item above skill 30 is gated by its band's book (`Classify`, `RecipeKind.Book`). Pinned recipes keep their scroll. `RequiredKeys` adds an extra key | The toe ring is a Tinkering item at a gold ring's skill (40 to 90), so the Tinkering band book covering skill 40 gates it, as it gates the rings. No new recipe |

## What was built (ShatteredLegacy)

| File | What |
|---|---|
| `server/customizations/Accessories/ClusterFAccessories.cs` (new) | `AccessorySettings` (every threshold) and `ClusterFAccessories`: kinds, slots, which jewels count, totals, `Refresh` (applies and removes mods), `Equip`/`Unequip`, the two PlayerMobile hooks, the jewellery achievements, the barefoot step test and movement handler, `[accessories`, the world-load re-apply, `CompanionSlots` |
| `.../Accessories/AccessoryContainer.cs` (new) | The container |
| `.../Accessories/ToeRings.cs` (new) | `ToeRing`, `SingedToeRing`, `MoodToeRing`, `PlateSocks` |
| `.../Accessories/AccessoriesGump.cs` (new) | The gump |
| `.../Accessories/AccessoryAchievements.cs` (new) | The five achievements (partial `ClusterFAchievementSystem`), the counters and the Unshod title |
| `.../Accessories/AccessoryFootLines.cs` (new) | The companions' foot lines (data), personality and event enums, and `Say` with the Hot and Cold cooldowns |
| `.../Accessories/AccessoryCraftRegistrations.cs` (new) | Tinkering: toe ring, Jewelry group, 40 to 90, 2 iron ingots |
| `server/customizations/ClusterFAchievements.cs` | 4 `TriggerKind`s, their Earned lines, and the `RegisterAccessories()` call |
| `server/customizations/LeagueShop/LeagueShop.cs`, `LeagueShopGumps.cs` | The `TitleDef` record gets `HiddenUntilHeld` (default false); the "the Unshod" row; the title picker lists a hidden title only once it is held, so it never gives the achievement away |
| `server/patches/AOS-accessory-container-aggregation.patch`, `PlayerMobile-accessory-hooks.patch` (new) | Applied last in `docker/uo/apply-patches.sh`, with the usual comment |
| `server/tests/Misc/AccessorySlotsVerification.cs` (new); `AchievementEarnedLineVerification.cs` | 7 facts; the two counts (95 to 100) |
| `CHANGELOG.md`, `VERSION` | `2026.10.21.8` (VERSION was `2026.10.21.7`): Added (players) and Staff |

### 1. The container

`AccessoryContainer : Container`:
- **Layer and visibility:** on `Layer.Unused_xF` (0x0F; no stock item uses it). `Visible = false`, so pinned's
  `CanSee(Item)` never sends it to a player's client; staff see it.
- **Not touchable:** `Movable = false` and blessed. `OnDragLift`, `CheckLift`, `IsAccessibleTo` and `CheckHold` are all
  false, and `OnDoubleClick` and `DisplayTo` do nothing. It cannot be stolen (it is not in the backpack) or looted (it
  never reaches a corpse).
- **Created** the first time a jewel needs it.
- **Death:** `OnParentDeath` asks the wearer's own `GetParentMoveResultFor(jewel)`. That is the rule a paperdoll jewel
  gets: PlayerMobile's insurance check (charged once) and the Young rule. A jewel bound for the corpse is dropped into
  the backpack, and `Mobile.Kill`'s backpack pass (which runs after the worn-items pass, `Mobile.cs:4801-4845`) puts it on
  the corpse. A blessed or insured jewel **stays in its slot**. A paperdoll one would go to the backpack instead; same
  result, kept, and no re-equip needed. The container itself returns `RemainEquipped`.

### 2. Totals and caps

- **Attributes:** `AttributeTotal`, called by the GetValue hunk after pinned's loop, sums the `Attributes` of the active
  jewels.
- **Resists:** the container's resistance properties sum the active jewels'.
- **Skill and stat bonuses:** `Refresh` calls the jewel's own `OnAdded(wearer)` when it becomes active and
  `OnRemoved(wearer)` when it stops, tracked in a memory-only set. Mods are not saved, so `OnWorldLoad` re-applies them
  for every container's wearer.
- **When bonuses change:** `Refresh` runs on every equip, unequip and shoe change. It also runs on any item added to or
  removed from a wearer that has a container. It ends with `UpdateResistances` and `Delta`.
- **Caps:** every cap is read on the summed values by the stock readers (resist max, HCI and DCI 45, and the rest),
  so they all still apply. Fact 2 shows a container ring's fire resist of 200 stopping at the wearer's cap of 70.
- **Inactive toe rings** contribute nothing to any of the three.

### 3. Slots (every threshold a setting)

| Kind | Rule | Today |
|---|---|---|
| Rings | 1 (the paperdoll ring) + 1 at each of `ringLoop1/2/3` (1, 5, 10), max 4, only when `loopSlotsEnabled` | **1**: loops do not exist. Waits for F-12's loop counter (`ClusterFAccessories.LoopOf`, one line to wire) |
| Bracelets | 1 (paperdoll) + 1 at League rank `braceletLeagueRank` (9) | **Works** |
| Toe rings | 0 + 1 for Plate Bottoms Only + 1 for Iron Soles | **Works** |
| Companions | rings and bracelets by companion rank (`companionRingRank1/2/3` 1, 5, 10; `companionBraceletRank` 5); toe rings as many as the owner has | Ready (`CompanionSlots`); waits for the companion type and its rank |

Jewels in the container count in order. If a slot count drops (a setting change), the jewels past it stop counting but
stay worn.

### 4. Toe rings and Plate Socks

- **`ToeRing : BaseJewel`.** Not a `BaseRing`, so it never counts as a ring. Its `CanEquip` is false, with "Toe rings go
  on toes. Use [accessories.", so it can never go on the paperdoll. It takes any jewel property.
- **When it counts:** only when the shoes layer is empty or holds `PlateSocks`.
- **Shoes over counting toe rings** send "Your toe rings have been suffocated. They will remember this." and add one to
  Smothered.
- **Plate Socks** are `BaseShoes`, cosmetic, 0 armour, with the tooltip "Technically shoes. The System will allow it."
- **The joke rings:** the **Singed Toe Ring** has no properties. The **Mood Toe Ring** changes hue every
  `moodRingMinutes` (3), on a timer restarted after load.
- **Art:** there is no toe ring art, so all three use the gold ring graphic. Plate Socks use the shoes graphic, hued iron
  grey.
- **Sources:** the spec gives none for the socks or the joke rings, so they are `[add` only.

### 5. The gump

`[accessories` (Player access) lists every slot:
- rings 1 to 4 (1 is the paperdoll ring), bracelets 1 and 2 (1 is the paperdoll bracelet), toe rings 1 and 2;
- a filled slot shows the jewel and a Remove button (it goes back to the backpack);
- an open slot reads "empty";
- a locked slot shows its one-line hint ("Unlocks with loops (not yet open on this shard).", "Unlocks at League rank
  Valorite Citizen.", "The System has noted that your feet are not yet qualified.");
- a toe ring that does not count is grayed, "(inactive: smothered by footwear)".

**Equip** takes a target cursor and puts the jewel in the first free slot, the paperdoll layer first. **Dragging onto a
slot is not possible** in a server gump, because a gump takes no drops; it comes with the TazUO paperdoll slots, the later
client item.

### 6. Companion foot lines

`AccessoryFootLines.Lines` holds the spec's 36 lines word for word: 6 personalities x Equip (male), Equip (female),
Smothered, Bare, Hot and Cold. `Say` speaks the line overhead:
- Hot is at most once per `companionHotSeconds` (60) and Cold once per `companionColdSeconds` (300);
- female picks the female Equip line;
- the personality comes from `PersonalityOf`, or Stoic.

Equip, Smothered and Bare are already called from `ClusterFAccessories` for any `BaseCreature` with accessories. No
creature has any until the companion type equips them. `OnStep` (Hot on lava or fire, Cold in the snow region) is for the
companion type's movement and has no caller yet.

### 7. Achievements (hidden, Mischief / "Noted by the System")

| Key | Title | Trigger | Flavor (snark) and plain description | AP / Renown |
|---|---|---|---|---|
| `noted.plate_bottoms_only` | Plate Bottoms Only | 1,000 counting tiles | "Two hundred pounds of steel protecting everything except the part touching the ground." / "Ran 1,000 tiles in plate armor with no shoes." Toe ring slot 1 | 10 / 2 |
| `noted.iron_soles` | Iron Soles | 25,000 counting tiles (after Plate Bottoms Only) | "Your feet have filed for guild status." / "Ran 25,000 tiles in armor with no shoes." Toe ring slot 2, title "the Unshod" | 25 / 10 |
| `noted.ring_bearer` | Ring Bearer | four rings worn | "Your fingers are now load-bearing." / "Wore four rings at once." | 10 / 2 |
| `noted.fully_accessorized` | Fully Accessorized | every jewelry slot filled | "The System estimates you are 30% jewelry by weight." / "Filled every jewelry slot." | 15 / 3 |
| `noted.smothered` | Smothered | 10 smotherings | "They trusted you." / "Put shoes on over your toe rings 10 times." | 5 / 0 |

**A counting tile** is a `EventSink.Movement` step (fired after pinned's `CheckMovement`, `Mobile.cs:4327`, so a blocked
step never counts) that meets all of these:
- the running flag is set;
- not mounted, and alive;
- the shoes layer is empty (Plate Socks are shoes, so they do not count);
- at least 4 armour pieces worn (`BaseArmor`, not shields), with the legs and chest among them. The pieces counted are
  helm, gorget, chest, arms, gloves and legs.

The counter is per account, as every achievement counter is. Grants are checked every 100th tile, and both thresholds
are multiples of 100.

**"Every jewelry slot"**, as read here: the paperdoll ring, bracelet, earrings and a necklace (a `BaseJewel` on the neck
layer, so a gorget does not count), every ring and bracelet slot the character has, and at least one toe ring slot with
every toe ring slot filled and counting.

The achievement reward sizes are mine, at P231's scale (5 to 25 AP).

## Stubbed, and why

- **Companions:** no type, rank or personality field exists. What is ready: `CompanionSlots`, `AccessoryFootLines`
  (data, `Say` and `OnStep`), and the creature branches in the hooks. A companion with no personality is Stoic, per the
  spec. **Flag:** the spec says a personality field exists; it does not in this build.
- **Ring slots 2 to 4:** loops are not built. Wiring them is one line in `LoopOf` plus `loopSlotsEnabled`.
- **The "Accessories" context-menu entry, on yourself and your companions:** not built. A context entry shows a cliloc
  number. On this PC I could not find one reading "Accessories":
  - the client's `Cliloc.enu` (`client-data\classic-client`) is compressed;
  - the vseUOAware `search_localized_strings` tool returns nothing for it, not even for "Imbue Item" (1114267, which
    cc-P29 verified);
  - a plain parse of the 7.0.117.0 copy gives garbage counts.

  A guessed number would show the wrong word, as cc-P29 found with 6277. **Needs:** a verified cliloc, or the TazUO item.
  It is then a one-line hook after `VoidPoolContextMenu.AddEntries` in `PlayerMobile.GetContextMenuEntries`.
- **Drag onto a slot:** not possible in a server gump (above). The target cursor is the way to equip for now.
- **Hot and Cold** are companion-only by the spec, so they have no caller until the companion type exists.

## Patches, argued (AGENTS.md: alternatives first)

**`AOS-accessory-container-aggregation.patch`** (1 hunk, `Misc/AOS.cs` in `GetValue`, after the Pet Training line):
- *Customizations alone:* no. `GetValue` is static with no event.
- *Move the jewels onto real paperdoll layers:* no. There is one ring layer and one bracelet layer.
- *Copy the jewels' attributes into a phantom item's `Attributes`:* rejected. It doubles state that must then be kept in
  sync on every change, enhance and imbue.

The hunk sits after the loop, far from P261's hunk at the top of the loop (that branch, not yet merged, also patches
`GetValue`), so the two patches' contexts do not overlap.

**`PlayerMobile-accessory-hooks.patch`** (2 one-line hunks, `OnItemAdded` and `OnItemRemoved`):
- *Customizations alone:* there is no equip or unequip event, and a partial class cannot override a method
  `PlayerMobile` already overrides.
- *Recompute toe rings lazily at read time:* that works for attributes and resists. Skill and stat mods, the suffocation
  message and Smothered all need the moment shoes go on.
- *Hook from the existing `ClusterFImbueEffects.OnEquipped` line:* covers only the add, and couples two systems.

**Resists:** no patch. The container overrides `PhysicalResistance` and the rest, so P261's edit to
`PlayerMobileSetResistances.cs` is untouched and cannot conflict.

**Merge note for the integrator:** P261 and P262 both append a block after `HousePlacement-climbed-tile.patch` in
`apply-patches.sh`, and both add `CHANGELOG.md`/`VERSION` sections. Keep both blocks, in either order, because they
touch different `AOS.cs` lines.

## Settings (`Configuration/modernuo.json`, all `clusterf.accessories.*`, written at start by `AccessorySettings.Configure`)

| Setting | Default | What |
|---|---|---|
| `loopSlotsEnabled` | false | Ring slots by loop: on once loops exist |
| `ringLoop1`, `ringLoop2`, `ringLoop3` | 1, 5, 10 | The loops that add ring slots 2, 3, 4 |
| `braceletLeagueRank` | 9 | League rank for bracelet slot 2 (9 = Valorite Citizen, middle of 17; 0 = off) |
| `companionRingRank1/2/3` | 1, 5, 10 | Companion ranks for companion ring slots 2 to 4 (ready) |
| `companionBraceletRank` | 5 | Companion rank for the second bracelet (ready). The spec says "the same thresholds"; the bracelet's is a League rank, so this is a guess for Chase |
| `barefootArmorPieces` | 4 | Armour pieces for a counting barefoot tile (legs and chest always required) |
| `moodRingMinutes` | 3 | The Mood Toe Ring's hue change |
| `companionHotSeconds`, `companionColdSeconds` | 60, 300 | Foot line cooldowns |

The achievement thresholds (1,000, 25,000, 10) are the achievements' own, in their definitions, as every achievement's
are.

## Tests

`server/tests/Misc/AccessorySlotsVerification.cs`, 7 facts:
1. `AJewelInTheContainerCountsLikeAPaperdollOne`:
   - paperdoll ring DCI 5 plus a container ring with DCI 7, physical 6 and Magery +10: DCI reads 12, resist +6, Magery 60;
   - removed, they read 5, the base resist and 50.
2. `TheWearersCapsStillApply`: a container ring with fire 200 leaves fire resist at the wearer's cap (70).
3. `ToeRingsCountBarefootAndInPlateSocksAndNotUnderShoes`:
   - barefoot: LMC 4, Meditation +5;
   - under shoes: 0 and +0, with Smothered +1;
   - shoes off: counting again;
   - in Plate Socks: counting, and no Smothered.
4. `OnlyARunningBarefootStepInFourArmourPiecesWithLegsAndChestCounts`:
   - counts: running in plate legs, chest, helm and gloves;
   - does not count: walking, shod, mounted, no legs, no chest, 3 pieces;
   - through the real `EventSink.Movement`: 999 runs and a walk give 999 and no slot; the 1,000th earns Plate Bottoms
     Only and slot 1; 25,000 earns Iron Soles, slot 2 and "the Unshod".
5. `TheContainerCannotBeTouchedAndFollowsTheDeathRules`:
   - layer 0x0F, invisible, not movable, unliftable, inaccessible, holds nothing dropped;
   - after `Kill()`, the plain container ring has left the player and the blessed one is still in its slot.
6. `SlotsFollowTheirThresholdsAndAFullKindRefusesMore`:
   - 1 ring slot with loops off, and a second ring refused ("full");
   - with loop slots on: loops 0, 1, 4, 5, 9, 10, 50 give 1, 2, 2, 3, 3, 4, 4;
   - the bracelet: 1 at rank 8, 2 at rank 9;
   - a toe ring is refused with no slots and never goes on the paperdoll.
7. `RingBearerAndSmotheredAreEarned`: the fourth ring earns Ring Bearer; the tenth pair of sandals earns Smothered.

**The test host has no tile data**, so armour has no layer there (D27). The test sets each piece's layer, as P231's
meditation fact does. The first green attempt found two things:
- **my own bug:** `Equip` refused every container ring with "You cannot wear that.". It asked the ring's `CanEquip`,
  which is false once the paperdoll ring layer is taken. The check is removed;
- the armour layers above.

**Seen failing first.** I put 7 marked breaks (`P262-BREAK 1` to `7`) into `ClusterFAccessories.cs` and
`AccessoryContainer.cs` and ran `--tests-only`. The result: 1,924 tests, 1,913 passed, **7 failed, exactly the 7 new
facts**. I then copied the green files back (`cmp` identical, no marker left).

| Fact | Break | Line | Failure |
|---|---|---|---|
| 1 | 2: the container reports no resist | 139 | Expected 6, actual 0 |
| 2 | 2 | 165 | Expected 70, actual 0 |
| 3 | 1: `Refresh` never applies mods (break 3, feet always free, is behind it) | 183 | Expected 45, actual 40 |
| 4 | 4: the running flag ignored | 225 | A walk counted |
| 5 | 5: death moves nothing out of the container | 306 | The plain ring stayed on the player |
| 6 | 6: bracelet slots ignore League rank | 335 | Expected 2, actual 1 |
| 7 | 7: no jewellery achievement checks | 357 | Ring Bearer not earned |

Breaks 1 and 3 are each behind an earlier assertion in their fact, so fact 1's Magery check and fact 3's shoes check were
not separately seen red. Each fact was seen red.

**Runs:**

| Run | Result |
|---|---|
| 1 to 3 | Compile errors: `LRReason` and `MessageType` namespaces, and a missing `Server.Gumps` using. Fixed |
| 3 | 8 failed: 6 of mine (the `Equip` bug and armour layers) and the two achievement counts (95 to 100, updated) |
| 4 | 1 failed: the armour layers. Fixed |
| 5 | **Green: 1,924 tests, 1,920 passed, 4 skipped.** `[patches] Applied:` both new patches |
| red | As above |
| full | **1,924 tests, 1,920 passed, 0 failed, 4 skipped; "Built sl-modernuo:cc-P262 with patches applied and 1920 shard test(s) passing."** The patch step was a cached layer from run 5, the same green tree |

## Deviations and register lines (drafted for the overseer)

- `docs\fidelity-principle.md`, next free D-number: "Accessory slots (ours; OSI has one ring and one bracelet). Extra
  rings by loop, a second bracelet by League rank, and toe rings by two hidden barefoot achievements, held in an
  invisible container on layer 0x0F and counted like worn jewellery within every cap. Reverses when: delete
  `server/customizations/Accessories/`, `AOS-accessory-container-aggregation.patch` and `PlayerMobile-accessory-hooks.patch`
  and their `apply-patches.sh` lines, and the cc-P262 lines in `ClusterFAchievements.cs` and `LeagueShop*.cs`. A worn
  container then deserializes as nothing: **move the jewels out first**, `[accessories` or a staff sweep."
- `docs\patch-backlog.md`: the two patches above, alternatives argued here.
- A blessed or insured container jewel stays in its slot at death, where a paperdoll one goes to the backpack. It is kept
  either way.

## For Chase

1. **The extra ring slots** wait for loops. They can open now if you like, by another rule (League rank, an achievement)
   until loops exist. It is a setting plus one line.
2. **The bracelet's League rank:** 9 (Valorite Citizen) of 17 for now. The companion bracelet rank (5) is a guess.
3. **Where Plate Socks, the Singed Toe Ring and the Mood Toe Ring come from.** The spec gives no source, so today they
   are `[add` only. The spec's own context suggests the Dented Box's joke-item roll.
4. **The context-menu entry:** it needs a cliloc reading "Accessories" verified on the client. Or skip it and let the
   TazUO paperdoll slots carry it.
5. **Art:** toe rings use the gold ring graphic and Plate Socks the shoes graphic. Should I file art requests for a toe
   ring and socks?
6. **Companion personality:** the spec expected one to exist. When the companion type is built, it needs a personality
   field (Stoic, Cheerful, Grumpy, Vain, Timid, Zealous) for the foot lines to read.

## Unverified

- **Not tried in a client:**
  - the gump layout;
  - that a `Visible = false` item on layer 0x0F is never drawn by TazUO (pinned's `CanSee(Item)` should keep it from
    ever being sent to a player);
  - the Mood Toe Ring's timer over real minutes;
  - the toe ring messages.
- **Insurance** on a container jewel at death goes through `PlayerMobile.GetParentMoveResultFor`, read from pinned. Fact
  5 tests blessed and plain only.
- **Re-applying mods after a restart** (`OnWorldLoad`) is read, not tested: the test host never loads a world.
- The Mood Toe Ring's timer and the companion foot lines are not covered by a fact. The lines are data, compared with the
  spec by eye.
- `tools/progress.py` was not run, as for P261 (its README block conflicts between Golems working at once).

P262 DONE
