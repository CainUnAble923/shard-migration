# cc-P29: defect batch 2 (D44, D45, D48, D14 stepping stones, [GuildStanding, the Imbuing Table label, D46)

2026-10-02. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P29-defect-batch-2.md`. Pinned ModernUO `7c9215d97`; pinned
paths below are under `D:\UO\ModernUO-pinned\Projects\`. "Ours" paths are under `D:\ShatteredLegacy\`; HEAD is `e2ca43d`.
Built in `D:\ShatteredLegacy`, **not committed**. Nothing was placed in any world; no shard was deployed, restarted or
recreated. `sl-modernuo:latest` was not moved (`d353a3fb86f2` before and after). Tools: `notes\cc-P29-tools\`.

> **Headlines**
>
> 1. **All seven parts are done. 408 shard tests pass** (391 before, 17 new). Image `sl-modernuo:cc-p29` =
>    `84728659bf35`. Two red runs: red 1 failed the 7 facts of Parts A-C against the unfixed code; red 2 failed the 7
>    facts of Parts D-F against deliberate breaks, each on its target assertion; every broken file came back
>    byte-identical by SHA-256 (section 8). Tool suite: 28 / 28 (27 before, one failing).
> 2. **Part A (D44): confirmed, and worse than read.** The talisman's Str offset was 20 on its second equip, in a
>    test. `GetHashCode()` is the object's default hash, never the serial, and the formats differ anyway (decimal
>    against `0x` hex). **Our Pet Mimic leaked the same way, and on every absorb while worn, not only on re-equip.**
>    Fixed by a 4-line pinned patch, `AOS-stat-bonus-names.patch` (no hook reachable from our code; five alternatives
>    argued in 1.2 before the patch). Before the fix the leak is bounded only by today's 500 clamp; with no clamp,
>    only by `Mobile.Str`'s 65000.
> 3. **Part B (D45):** above a 150-mana pool the deficit is scaled to a 150 pool; at or below 150 it is OSI's formula
>    exactly (a fact checks every mana level at pools 100, 125 and 150). Int 500 at Med 120 needs 17 mana to have a
>    chance, down from 356.
> 4. **Part C (D48):** extraction now brings current durability down with the maximum. A Longsword at 89 / 89 read
>    **89 / 72** after one extraction in red 1, exactly Chase's shape; now 58 / 58 after two. The failure path never
>    had the gap. No other place in ours lowers a maximum durability.
> 5. **Part D (D14): the stepping stones are decoration in OSI's data too.** All twelve are rocks 0x1363-0x136D,
>    tiledata **Impassable, no Surface**, identical in the server's data (7.0.114.40) and EA's 7.0.117.0; the map and
>    statics in the box are identical too. Under a line-for-line port of pinned's movement code, **no reachable tile
>    is within 3 of the fountain: the nearest is 8, on the south shore** (both data sets), matching Chase. P27's five
>    "shore" tiles are not reachable on foot. New command **`[ClusterFSeedFountainSteps [dryrun]`** lays twelve
>    walkable pavers (existing art "PaverStones Natural") over the rocks; with them the walk reaches the end tile, one
>    from the fountain, in both data sets. A deviation, text in section 7.
> 6. **Part E:** `[GuildStanding <guildKey> [amount]` (GameMaster, test shard). Unknown keys are refused with the
>    list. `[CompactStanding` unchanged.
> 7. **Part F: cliloc 1114267, "Imbue Item".** I ported pinned's own cliloc reader (`BwtDecompress.cs` and
>    `Localization.cs`; P22 thought no decoder existed). That decoded both client files and confirmed what Chase saw:
>    6277 goes out as 3006277, "Salvage Ingots". The code's TODO said "Smelt Metal", which was wrong. Chase checks
>    the new label in game.
> 8. **Part G:** the twin fact names a live pair (`GlassesOfTheArts`/`ArtsGlasses`, kept by the audit on purpose);
>    `SatchelTypes` is a reader site; the audit's reproduction line needs `docker/uo/apply-patches.sh` in the export,
>    and fails without it (checked).

---

## 0. Before starting, and during

- `git --no-optional-locks status` in `D:\ShatteredLegacy`: clean at `e2ca43d` (P28) at 09:35. Nothing else was building.
- Read: `p25-decisions-2026-10-02.md`, `cc-P25-stats-above-125-research.md` 2.6 and Part 5, `cc-P27-defect-batch-1.md`
  sections 1 and 3.5, `p27-p28-checks-2026-10-02.md`.
- **Numbering:** no clash. P28 is `e2ca43d`; this is P29.
- **No commit landed in either repo during the task** (`e2ca43d` and `77ded46` at start and at 10:09).
- **Not mine: `D:\ShatteredLegacy\design\registrar-office\cleanup\`** (`clean.py`, two PNGs) appeared untracked at 09:41,
  mid-task. I did not create, read into the build, or touch it. Chase should know it is there before committing.

---

## 1. Part A: D44, the talisman and quiver stat-bonus leak

### 1.1 The overseer's reading, verified

- Add path, `UOContent/Misc/AOS.cs:590-616` (`AosAttributes.AddStatBonuses`): `var hashCode = GetHashCode();` (`:598`),
  mods named `$"{hashCode}Str"`, `Dex`, `Int` (`:601`, `:606`, `:611`).
- Remove path, `:618-627` (`RemoveStatBonuses`): `var serial = Owner.Serial;` (`:620`), removes `$"{serial}Str"` etc.
  (`:622-624`).
- **Does `GetHashCode()` equal the owner's serial? No, on two counts.** `BaseAttributes` (`AOS.cs:1349`) and
  `AosAttributes` declare no `GetHashCode` override, so the call is `object.GetHashCode()`, the runtime's per-object
  hash. And even if it were the serial's value, the strings differ in format: an `int` interpolates as decimal, while
  `Serial.ToString()` is hex with `0x` (`Server/Serial.cs:121-130`). Only `Serial` itself overrides `GetHashCode`
  (`Serial.cs:50`), and that is not what is called.
- `Mobile.AddStatMod` appends without replacing a same-named mod (`Server/Mobiles/Mobile.cs:8388-8400`);
  `RemoveStatMod(string)` removes every mod with that exact name (`:8344-8367`).
- Callers on this path: talisman `OnAdded`/`OnRemoved` (`UOContent/Items/Talismans/BaseTalisman.cs:356`, `:379`) and
  its `AfterDeserialization` (`:758`); quiver `OnAdded`/`OnRemoved` (`UOContent/Items/Quivers/BaseQuiver.cs:206`,
  `:214`); and **ours**, `server\customizations\PetMimic.cs:1029` / `:1042` (equip, unequip) and `:1318-1319`,
  `:1383-1384` (remove-then-add while worn, on every absorb and on a purge). So the Pet Mimic leaked too, and not only
  on re-equip: every absorb while worn stacked another copy.
- Every other item type names its mods by serial on both sides: `BaseClothing.cs:526`/`:625`, `BaseJewel.cs:220`/`:246`,
  `BaseArmor.cs:1056`/`:1205`, `Spellbook.cs:573`/`:599`, `BaseWeapon.cs:1082`/`:1145`.
- **Runtime-verified (red 1):** talisman, quiver and Pet Mimic each read Str offset 10 worn, **10 after removal**, and
  **20** on the second equip.

### 1.2 Fixing it: alternatives argued before the patch

Written here before the build that first applied the patch (green 1, 09:51).

1. **Our own unequip hook that removes the add-path names.** There is nowhere to hang it. The removal happens in
   `Item.OnRemoved` of the talisman or quiver, pinned classes with many subclasses, and loot creates the stock types.
   `Mobile.OnItemRemoved` (`Mobile.cs:6583`) is virtual, but its override for players is pinned
   `PlayerMobile.OnItemRemoved` (`UOContent/Mobiles/PlayerMobile.cs:1701`), so hooking it is a pinned patch anyway,
   and a bigger one. Pinned has no equip or unequip event (`Server/Events/` holds account login, aggressive action,
   movement, crash, socket and speech events only). **Rejected: not reachable from our code.**
2. **A periodic sweep that removes orphaned hash-named mods.** The bonus would still apply between sweeps while the
   item sits in the pack, it must guess mod names by pattern (`-?\d+(Str|Dex|Int)`), and it cannot tell a live mod
   from an orphan without recomputing every equipped item's hash. **Rejected: fragile, and still wrong between sweeps.**
3. **Patch the remove path to use `GetHashCode()` instead.** Also small, but it keeps a name that is not unique across
   objects (default hashes can collide) and differs from every other item type. **Rejected.**
4. **Replace `AOS.cs` wholesale from customizations.** A 1,400-line file that already carries three of our patches
   (`AOS-pet-mimic-attribute-aggregation`, `AOS-set-attribute-aggregation`, `AOS-damage-eater-hook`); a replacement
   would silently drop upstream changes on a bump. **Rejected.**
5. **Patch the add path to name the mods by `Owner.Serial`** (chosen). The hunk is the name mismatch and nothing else:
   `var hashCode = GetHashCode();` becomes `var serial = Owner.Serial;` and the three names follow. It fixes the
   talisman, the quiver and our Pet Mimic at once, and matches every other item type.

**Whose bug:** ModernUO's (a pinned defect, not ServUO content). Worth reporting upstream.

### 1.3 What changed

- `server\patches\AOS-stat-bonus-names.patch` (new, one hunk, `@@ -595,20 +595,23 @@`; SHA-256 `73d86413c0d6ee0d...`).
  Applies after the other three `AOS.cs` patches with an offset and `--fuzz=0`; the build log says
  `[patches] Applied: AOS-stat-bonus-names.patch`.
- `docker\uo\apply-patches.sh`: one `apply_patch` line after `AOS-damage-eater-hook`, with its reason. This file is
  outside the brief's listed folders; a patch cannot reach the build without it (the runner fails any patch file it was
  not told about).
- No saved type changed: StatMods are not saved (a loaded mobile starts with an empty list, `Mobile.cs:6419`), and the
  talisman's `AfterDeserialization` re-adds its bonus under the new name. **A live shard carrying leaked copies loses
  them at the next restart, as it always did.**

### 1.4 How high a looping equip could push a stat before the fix

- **Each unequip and re-equip leaves one more full copy** of the item's bonus. Nothing removes the copies until a
  restart (StatMods are not saved).
- **Today:** effective Str, Dex and Int read `Math.Min(base.Str, ClusterFStatCaps.IndividualStatCap)`
  (`patches\PlayerMobile-individual-stat-cap.patch`, pinned `PlayerMobile.cs:594`, `:609`, `:624`). That is 500 on
  the live config (`Configuration\modernuo.json:112`, `"clusterf.statCaps.individualCap": "500"`). So the visible
  stat stops at 500, but the hidden offset keeps growing.
- **With no clamp** (p25-decisions item 3, not yet built), the only bound is `Mobile.Str`'s `Math.Clamp(..., 1, 65000)`
  (`Mobile.cs:1868`). The offset itself is an `int` sum (`GetStatOffset`), which does not overflow first.
- **The client breaks first.** The status packet writes Str, Dex, Int, HitsMax and MaxWeight as signed 16-bit
  (`Server/Network/Packets/OutgoingMobilePackets.cs:523-542`).
  - Str passes 32767 after about 3,250 cycles of a +10 item.
  - MaxWeight (`100 + 3.5 x Str`, ours `ClusterFBackpack.cs:33-42`) passes 32767 from Str of about 9,330, so after
    about 900 cycles.
  - HitsMax (`50 + Str / 2` under AOS) stays below 32767 even at 65000.
- **Speed: not measured.** At an unmeasured one cycle a second from a scripted client, 900 cycles is 15 minutes.

### 1.5 Facts (`server\tests\Items\StatBonusLeakVerification.cs`)

Each equips and removes the item three times, asserts the offset is exactly the bonus while worn, and at the end
asserts raw stats unchanged and offset 0.
1. `ATalismansStrDexIntBonusesComeOffEveryTime`: `BaseTalisman` with BonusStr 10, Dex 7, Int 5.
2. `AQuiversStrBonusComesOffEveryTime`: `ElvenQuiver`, BonusStr 10.
3. `APetMimicsStrBonusComesOffEveryTime`: our `PetMimic`, `AccStrBonus` 10.

Red 1: all three "Expected 10, Actual 20" on cycle 2. Green from green 1 on.

---

## 2. Part B: D45, Meditation gets worse as Int rises

### 2.1 Facts re-read

- Ours `server\customizations\Meditation.cs:83` (HEAD), a full replacement of pinned `UOContent/Skills/Meditation.cs`
  (same formula at `:76`): `chance = (50 + (skill - (ManaMax - Mana)) * 2) / 100`, compared to `Utility.RandomDouble()`.
- cc-P25 Part 5 row 7 proposed `(ManaMax - Mana) * 125 / ManaMax`. **I did not use it as written:** at a pool of 100 it
  multiplies the deficit by 1.25, so an OSI-scale character (Int 100, Med 100, empty pool) would drop from 0.50 to
  0.00. The brief asks for OSI-scale pools unchanged.

### 2.2 What changed

- `Meditation.StartChance(skill, mana, manaMax)`: the deficit is `ManaMax - Mana`; **if ManaMax is above 150** it is
  scaled by `150 / ManaMax`. 150 is OSI's effective Int cap (pinned `PlayerMobile.cs:594`, ML).
  - At or below 150 the formula is OSI's exactly, not "within rounding".
  - Above 150, the chance depends only on the fraction of the pool missing, so it no longer falls as the pool grows.
- `OnUse` calls it instead of the inline line. The armored-meditation penalty after it is unchanged.

### 2.3 The table (`cc-P29-tools\med_table.py`; human, no Mana Increase, ManaMax = Int; chances clamped to 0..1)

| Int (= ManaMax) | Med | chance at 0 mana, before -> after | at half, before -> after | least mana for any chance, before -> after |
|---|---|---|---|---|
| 100 | 50 | 0.00 -> 0.00 | 0.50 -> 0.50 | 26 -> 26 |
| 100 | 100 | 0.50 -> 0.50 | 1.00 -> 1.00 | 0 -> 0 |
| 100 | 120 | 0.90 -> 0.90 | 1.00 -> 1.00 | 0 -> 0 |
| 125 | 50 | 0.00 -> 0.00 | 0.24 -> 0.24 | 51 -> 51 |
| 125 | 100 | 0.00 -> 0.00 | 1.00 -> 1.00 | 1 -> 1 |
| 125 | 120 | 0.40 -> 0.40 | 1.00 -> 1.00 | 0 -> 0 |
| 200 | 50 | 0.00 -> 0.00 | 0.00 -> 0.00 | 126 -> 101 |
| 200 | 100 | 0.00 -> 0.00 | 0.50 -> 1.00 | 76 -> 34 |
| 200 | 120 | 0.00 -> 0.00 | 0.90 -> 1.00 | 56 -> 7 |
| 500 | 50 | 0.00 -> 0.00 | 0.00 -> 0.00 | 426 -> 251 |
| 500 | 100 | 0.00 -> 0.00 | 0.00 -> 1.00 | 376 -> 84 |
| 500 | 120 | 0.00 -> 0.00 | 0.00 -> 1.00 | 356 -> 17 |

An empty pool above 150 still cannot start at Med 120, exactly as an empty OSI pool of 150 cannot
(`50 + (120 - 150) * 2 < 0`).

### 2.4 Facts (`server\tests\Misc\MeditationStartChanceVerification.cs`)

1. `AtOsiScalePoolsTheChanceIsOsis` (theory, pools 100, 125, 150): every mana level, Med 50, 100, 120, equals OSI's
   formula. Green before and after (it pins what must not move).
2. `AFiveHundredPoolAtHalfManaStartsLikeAOneFiftyPoolAtHalfMana`: Med 120, 1.4 both. **Red 1: -2.1.**
3. `ForAFixedFractionMissingTheChanceNeverFallsAsThePoolGrows`: pools 150 to 2,000, 10% to 100% missing, within 0.02
   (whole-mana rounding). **Red 1:** "Med 50, 10 % missing: pool 200 chance 1.100, previous 1.200".

---

## 3. Part C: D48, extracting a property leaves durability above its maximum

### 3.1 Facts re-read

- Ours `server\customizations\ArtificersImbueGump.cs:1524-1528` (HEAD), `HandleExtractProperty`: lowers `MaxHitPoints` by
  a fifth, weapon and armour, and never touches `HitPoints`.
- Pinned's setters clamp only the value assigned: `BaseWeapon.HitPoints` (`Items/Weapons/BaseWeapon.cs:386-388`),
  `BaseArmor.HitPoints` (`Items/Armor/BaseArmor.cs:716-718`). `MaxHitPoints` is a generated property with no clamp
  (`BaseWeapon.cs:66-69`, `BaseArmor.cs:93-96`).
- **The failure path (`:1410-1411`) has no gap:** it lowers `HitPoints` only, through the setter, and leaves the max.
- **No other place in ours lowers a maximum durability:** `grep` for `MaxHitPoints =`, `-=`, `--` and `MaxHP` writes over
  `server\customizations` finds only `:1526`, `:1528`, and `PetMimic`. `PetMimic`'s `IDurability.MaxHitPoints` setter
  (`PetMimic.cs:391-395`) can lower its max without clamping `CurrentHP`. Nothing calls it to lower: pinned's
  lowering writers (`Repair.cs:289`, `:359`, `:430`; the wear paths in `BaseArmor.cs:788`, `BaseClothing.cs:385`,
  `BaseShield.cs:103`) all take concrete weapon, armour or clothing types. Recorded, not changed.

### 3.2 What changed

After lowering the max: `HitPoints = Math.Min(HitPoints, MaxHitPoints)`, weapon and armour. (Assigning `HitPoints`
to itself would do nothing: the setter returns early on an equal value.)

### 3.3 Facts (`server\tests\Misc\ImbueExtractDurabilityVerification.cs`)

Through the table's own buttons (Disenchant target, the property's Extract row, Apply), as P27's imbue facts do.
1. `ALongswordExtractedTwiceNeverReadsAboveItsMaximum`: 89 / 89 with two properties; after one, current <= max; after
   two, 58 / 58. **Red 1: "89 / 72 after one".**
2. `APlateChestExtractedOnceNeverReadsAboveItsMaximum`: 60 / 60, one property; 48 / 48. **Red 1: 60 (expected 48).**

---

## 4. Part D: D14, the Fountain of Fortune's stepping stones

### 4.1 The stones (`cc-P29-tools\stones.py`, both data sets)

- Server data: `D:\ShatteredLegacy\client-data\classic-client`, client 7.0.114.40. EA: `D:\UO\UltimaOnlineVanilla`,
  `client.exe` 7.0.117.0 (file version read 2026-10-02).
- **The line from the south shore to the fountain is twelve rocks:**

  | tile | static | z | height |
  |---|---|---|---|
  | 1121,965 | 0x136C rock | -43 | 2 |
  | 1122,965 | 0x1363 rock | -43 | 3 |
  | 1123,965 | 0x1365 rock | -43 | 2 |
  | 1122,964 | 0x136B rock | -43 | 2 |
  | 1123,964 | 0x1369 rock | -43 | 2 |
  | 1123,963 | 0x1367 rocks | -42 | 2 |
  | 1123,962 | 0x136A rocks | -42 | 2 |
  | 1122,961 | 0x1369 rock | -43 | 2 |
  | 1123,961 | 0x1366 rock | -43 | 2 |
  | 1121,960 | 0x1368 rock | -43 | 2 |
  | 1122,960 | 0x136D rocks | -43 | 2 |
  | 1121,959 | 0x1366 rock | -43 | 2 |

  Every one sits on water land (0xA8-0xAB, Impassable and Wet).
- **Every rock ID, 0x1363-0x136D, is tiledata Impassable, with no Surface flag, in both files.** Names and heights are
  identical too. `stones.py` lists all 47 static IDs in the box: **none differs** between the two tiledata files.
- `statics5.mul` and `staidx5.mul` are byte-identical between the two (SHA-256). `map5LegacyMUL.uop` and
  `tiledata.mul` differ as files, but **0 land tiles differ** in the box 1111..1131 x 949..967.
- **So the stones are decoration in OSI's data as well.** The data version is not the cause, and Q-063 (the 7.0.117
  move) would not change this.

### 4.2 The walk, under pinned's movement rules (`cc-P29-tools\walk.py`, `fountain_walk.py`)

- **The port.** `walk.py` is a line-for-line port of pinned `MovementImpl`
  (`UOContent/Engines/Pathing/Movement.cs`: `CheckMovement` `:42-176`, `IsOk` `:182-235`, `Check` `:237-480`,
  `GetStartZ` `:486-580`) and `Map.GetAverageZ` (`Server/Maps/Map.cs:243-297`). It covers a walking player (StepHeight
  2, PersonHeight 16, a player diagonal needs both sides clear) over the client map, statics and tiledata. It
  replaces P15's approximation.
- **Starts.** Every teleporter landing into the `Underworld` region box (898,808 to 1280,1231, `regions.json:3938`)
  from outside it, in pinned `teleporters.json`: the Trammel entrance at 1127,1215 / 1129,1215 and 1128,1213 /
  1129,1213, and the Ter Mur entrance at 1125-1126, 1075-1076. The walk follows all 37 teleporters inside the box.
- **Result: 17,897 tiles reached, and none within 3 of a component, in both data sets.** The nearest are
  1121..1124, 966, z -42, **8 tiles** from the fountain's south edge. This matches Chase (09:04, 09:25).
- **P27's five shore tiles (1116,952 and the rest) are not reached at all.** P27 said its walk needed a step-up of 6
  or more to reach them, and pinned's step is 2.
- **Not modelled:** world items (pinned ships no Ter Mur decoration; any staff-placed item near the pool is not in
  it) and mobiles.
- **Validation is weak.** The port has not been checked against NPC positions the way P15's `fit.py` was. Its only
  agreement with the world is Chase's report.

### 4.3 The fix: walkable pavers, by a staff command

- **Art:** "PaverStones Natural", 0x47DC-0x47E0 and 0x47E5: tiledata **Surface only, height 1**, the same in both
  files. They are cycled over the twelve tiles.
- **z -41**, so a player stands at -40:
  - That clears the tallest rock: 0x1363 at -43 with height 3, and 0x136A / 0x1367 at -42 with height 2, all top -40.
    `IsOk` blocks only when the rock's top is above the standing z.
  - It is a step of 2 up from the shore's -42.
- **Simulated (`steps_walk.py`), both data sets:**
  - All twelve stones are reached, at z -40. The end tile, **1121,959, is 1 from the component at 1121,958.**
  - Path tail: 1123,966 shore, then 1123,965 / 964 / 963 / 962 / 961, 1122,961, 1122,960, 1121,960, 1121,959.
  - The shore tile 1117,961 also becomes reachable, 3 from the fountain.
- **Command `[ClusterFSeedFountainSteps [dryrun]`** in `server\customizations\ClusterFFountainStepsSeeder.cs`:
  - Administrator, like P27's seeder.
  - Declared `[ShardCommand(WorldSetup, Rerun = Skips, Shard = TestFirst, DryRun = "dryrun", Summary = ...)]`; P21's
    gate passes.
  - Never runs at world load: it registers a command and nothing else.
  - Duplicate-safe: a `Static` of the paver art already on a stone's tile (any z) counts as that stone.
  - If Ter Mur is not loaded it reports that and places nothing. If no fountain is near the point, it says to run
    `[ClusterFSeedFountainOfFortune` too.
  - Each paver is a `Static` named "stepping stone", not movable.
- **The fountain stays at OSI's point.** P27's seeder and its facts are untouched. A separate command keeps "where the
  fountain is" and "how you reach it" apart. The cost is that **both commands must be run** on any shard.
- **Alternative not taken:** a longer coin range (ours `LuckyCoin.cs:35`, range 3) would need 8 or more with no
  change to the world. That is a different deviation, a rule change, and the brief named the stones.
- **What only the client can confirm:** that the client's own movement prediction lets a player onto a paver item,
  and that the pavers look right over the rocks.

### 4.4 Facts (`server\tests\Items\Addons\FountainStepsVerification.cs`)

The test host has no map files and no item tiledata (`TestHostTileDataVerification`), so it cannot walk; these test
placement and range.
1. `ADryRunPlacesNothing`: nothing placed; "would place 12, already there 0". **Red 2 (dry run places): "Collection
   was not empty".**
2. `RunTwiceItLaysTwelveStonesInOneChain`: twelve stones, one per tile, z -41, unmovable, of the art; second run
   "placed 0, already there 12"; each step is next to the shore (1122,966) or an earlier step. **Red 2 (find never
   matches): "Expected 12, Actual 14".**
3. `ALuckyCoinThrownFromTheEndStoneReachesTheSuccessPath`: fountain and steps seeded; a player on 1121,959,-40
   uses a coin through its own target on the nearest component; one coin spent and the cooldown set. **Red 2 (the line
   stops five stones short, at 1123,962): "the end stone is 4 from the fountain".**

**Recorded, not changed:** P27's `ALuckyCoinThrownFromTheShoreReachesTheSuccessPath` stands at 1117,952, which its
comment calls "the nearest shore tile". It is in range, but under pinned's rules **it is not reachable on foot**
(4.2). The fact tests range, which is still true; its comment is now misleading.

---

## 5. Part E: `[GuildStanding <guildKey> [amount]`

- `server\customizations\ClusterFGuildStandingCommand.cs`:
  - GameMaster. Declared `[ShardCommand(CommandCategory.Grant, Shard = CommandShard.TestOnly)]`: a test-shard
    command, Grant ("hands a player ... standing", `ShardCommandAttribute.cs:46`).
  - The key is checked first. An unknown key is refused with every valid key listed, sorted, and no target cursor
    opens. The keys come from `ClusterFGuildSystem.AllGuilds` (17 today: arcane, artificers, bards, custodians,
    dojo, foresters, healers, keepers, maritime, merchants, mining, rangers, smithing, tailoring, thieves, tinkers,
    warriors). Keys match without regard to case.
  - Then it targets a player. With an amount it sets `GetOrCreateGuildData(pm.Serial).GuildReputation[key]`; without,
    it reports standing and rank.
  - A non-number amount is refused with the usage.
- **Rank names:** each guild's own ladder through `ClusterFGuildSystem.GetRankName(key, standing)` (`:575-584`), which
  already routes artificers to `ArtificersGuildmasterGump.GetRankName`, and smithing, rangers, foresters and
  custodians to theirs.
  - **Mining is the exception:** that switch has no mining case, so it would show the generic ladder.
  - The command uses `MinersCompactLiaisonGump.GetRankName`, as `[CompactStanding` does (`ClusterFCompactAdminTools.cs:72`).
- **Found, not changed:** the Guild Directory (`ClusterFGuildSystem.cs:814`, `:963`) shows the miners' rank from the
  generic ladder ("Initiate/Apprentice/..."), not the Compact's ("Surveyor" at 16,000). Whether that is wanted is the
  overseer's call.
- `[CompactStanding` is untouched.
- Facts, `server\tests\Misc\GuildStandingCommandVerification.cs`:
  - They run the real handler by reflection and answer its cursor.
  - `Mobile.SendMessage` is not virtual in pinned (`Mobile.Messages.cs:212`), so the lines are read from the methods
    that build them.
  1. `SettingArtificersTo15000MakesAMasterArtificer`. **Red 2 (wrong key written): "Expected 15000, Actual 0".**
  2. `WithNoAmountItReadsStandingAndTheGuildsOwnRankBack`: artificers 5,200 reads "Artificer", mining 16,000 reads
     "Surveyor", and reading changes nothing. **Red 2 (mining on the generic ladder): "Rank=Surveyor" not found.**
  3. `AnUnknownGuildKeyIsRefusedWithTheValidKeys` ("artificer", singular). **Red 2 (unknown key falls back): "an
     unknown key opened a target cursor".**

---

## 6. Part F: the Imbuing Table's context menu label

- **The decoder.** P22 had none. Pinned has one: `Server/Client/BwtDecompress.cs`, called from
  `Server/Localization/Localization.cs:105-110`. It handles a header that is not `2, 1`: skip 4 bytes, a
  move-to-front pass, then `InternalDecompress`, then entries of `int number, byte flag, ushort length, UTF-8`.
  - `cc-P29-tools\cliloc.py` is a port of both.
  - It decodes the server's `Cliloc.enu` (123,489 entries) and EA's (124,000).
  - Known numbers read back: 1113369 is "That is not sacred waters. Try looking in the Underworld.", 3000000 is
    "Quit Ultima Online?".
- **Why it read "Salvage Ingots".** `new ContextMenuEntry(6277)` stores 3006277, since numbers at or below 0x7FFF get
  3000000 added (`Server/ContextMenus/ContextMenuEntry.cs:40-48`). **3006277 is "Salvage Ingots"** in both files
  (3006276 "Salvage All", 3006278 "Salvage Cloth"). The code's TODO said "Smelt Metal"; that was wrong.
- **The candidates:**
  - A number above 0x7FFF is sent as-is. It forces the version 2 context packet (`ContextMenu.cs:51`), which pinned
    already uses for `EndlessDecanter` (1115891 "Link", 1115930 "Unlink").
  - From `cliloc.py --grep`: 1114267 "Imbue Item"; 1044116, 1079507 and 1079712 "Imbuing"; 1079588
    "<CENTER>IMBUING MENU</CENTER>" (markup, unsuitable).
  - All read the same in both files.
- **Chosen: 1114267 "Imbue Item".** It says what clicking does. It is `ArtificersGuildmaster.LabelCliloc`; the TODO is
  gone.
- **No deviation.** The guildmaster's table is ours; OSI has no such menu entry.
- **Fact, `server\tests\Misc\ImbuingTableLabelVerification.cs`:** `TheImbuingTableEntrySaysImbueItem` builds the
  private entry by reflection: number 1114267, range 5. **Red 2 (back to 6277): "Expected 1114267, Actual 3006277".**
- **Chase checks the label in game.**

---

## 7. Deviations for the register (`docs\fidelity-principle.md`)

- **D45, Meditation start chance (ours `Meditation.cs`, `StartChance`).** "OSI uses the absolute mana deficit,
  `(50 + (Meditation - (ManaMax - Mana)) * 2) / 100`. With no stat ceiling (p25-decisions item 3) a large pool had to
  be nearly full before a trance could start: Int 500 at Meditation 120 needed 356 mana. Above a 150-mana pool (OSI's
  effective Int cap) the deficit is scaled to a 150 pool, so the chance depends on the fraction of the pool missing.
  At or below 150 the formula is OSI's exactly. Reverses by deleting the scaling branch in `StartChance`."
- **D14, stepping stones to the Fountain of Fortune (ours `ClusterFFountainStepsSeeder.cs`).** "OSI's fountain stands
  at Ter Mur 1121, 957, -42, in a pool. The line of rocks from the south shore is decoration in OSI's own client data
  (tiledata Impassable, no Surface, 7.0.114.40 and 7.0.117.0 alike), and with ServUO's coin range of 3 no tile a
  player can walk to is in range; the nearest is 8 tiles away. We lay twelve walkable pavers of existing art
  ('PaverStones Natural', 0x47DC-0x47E0, 0x47E5) over those rocks at z -41, by staff command, ending one tile from
  the fountain. The fountain itself is at OSI's point. Reverses by deleting the twelve `Static` pavers at those tiles."
- **Not deviations:** Part A fixes a pinned defect toward correct behaviour; Part C fixes ours; Parts E and F are ours
  with no OSI counterpart.

---

## 8. Builds, red and green (`docker\uo\build.sh -t sl-modernuo:cc-p29`, Git Bash)

| Run | Time | Result | Notes |
|---|---|---|---|
| red 1 (`--tests-only`) | 09:46-09:48 | **7 failed / 397 passed (404)** | the facts of A, B, C against the code as it was; the three Part E facts were green |
| green 1 (`--tests-only`) | 09:51-09:53 | **404 / 404** | fixes A, B, C; patch applied |
| red 2 (`--tests-only`, `cc-P29-tools\mutate.py apply R2`) | 10:02-10:06 | **7 failed / 401 passed (408)** | seven breaks, each failing only its target fact, messages in sections 4.4, 5, 6 |
| restore R2 | 10:06 | three files "identical" by SHA-256 | |
| final (full, image) | 10:06-10:09 | **408 / 408**, `sl-modernuo:cc-p29` = **`84728659bf35`** | after one cosmetic change: the steps report names its first and last tile from the table instead of a literal |

- **Test totals: 391 before (P27), 408 after**, 17 new: A 3, B 5 (one theory of 3 plus 2), C 2, D 3, E 3, F 1.
- No red run built an image (the test gate stopped them).
- The `Item.Amount <= 0 error` lines in every log (109 in the final) come from the CC6 creature facts and predate this
  task.
- `sl-modernuo:latest` = `d353a3fb86f2` before and after.

---

## 9. Part G: the content index (tools only)

- `tools\test_content_index.py`:
  - The twin fact is now `test_twin_sweep_finds_a_pinned_type_under_another_name`. It expects
    `('GlassesOfTheArts', 'cliloc', 'ArtsGlasses')` and that `GauntletsOfAnger` is no longer reported.
  - The pair was picked because the audit kept both on purpose (`reachability-audit.md:335`, "ServUO keeps both"), so
    it will not go stale the way the D35 deletion did.
  - **No live misspelling twin remains.** Today's sweep reports 14 hits: 12 cliloc, among them the ten glasses and
    `HumanFeyLeggings` (all judged not twins by the audit), plus the two D34 aliases.
- `tools\content_index.py`: `'SatchelTypes'` added to `READER_SITES`, with its reason.
  - New fact `test_reach_the_guild_satchel_list_reads_types_and_makes_none`: the `GuildResources` reference to
    `GemologistsSatchel` is `('check', 'SatchelTypes')`, and closing over `GuildResources` alone creates no satchel.
  - The satchel is still reached, correctly, by `new` in `FountainOfFortune.cs:90`.
- **Watched red** (`cc-P29-tools\tool_red.py`, monkeypatching in-process, tools untouched):
  - `red-satchel`, without `SatchelTypes`: the satchel fact fails with `('typeof', 'SatchelTypes')` where `check` was
    expected.
  - `red-twin`, with pinned's labels hidden: the twin fact fails with only the two aliases found.
  - In both runs the other fact stays green. `green`: both pass.
- **Suite: 28 / 28** (`python -m unittest test_content_index`, 26 s). It was 27 with one failure.
- **The audit's reproduction line** (`notes\reachability-audit.md`, section 9, "Reproduce") must export
  `apply-patches.sh` with the tree:

  ```
  git -C D:\ShatteredLegacy archive HEAD server docker/uo/apply-patches.sh | tar -x -C <dir>
  python tools/content_index.py reach --ours <dir>/server/customizations --sources --twins
  ```

  Checked both ways: the old line (`archive HEAD server`) stops with "apply-patches.sh not found"; the new one runs.
  The other two lines of that block are unchanged.

---

## 10. File by file

```
D:\ShatteredLegacy
  server\patches\AOS-stat-bonus-names.patch                    NEW  Part A, one hunk
  docker\uo\apply-patches.sh                                   M    Part A, one apply_patch line + reason
  server\customizations\Meditation.cs                          M    Part B, StartChance (an upstream replacement file)
  server\customizations\ArtificersImbueGump.cs                 M    Part C, current durability follows the max
  server\customizations\ClusterFFountainStepsSeeder.cs         NEW  Part D, [ClusterFSeedFountainSteps
  server\customizations\ClusterFGuildStandingCommand.cs        NEW  Part E, [GuildStanding
  server\customizations\ArtificersGuildmaster.cs               M    Part F, label 1114267
  server\tests\Items\StatBonusLeakVerification.cs              NEW  A, 3 facts
  server\tests\Misc\MeditationStartChanceVerification.cs       NEW  B, 3 facts (5 cases)
  server\tests\Misc\ImbueExtractDurabilityVerification.cs      NEW  C, 2 facts
  server\tests\Items\Addons\FountainStepsVerification.cs       NEW  D, 3 facts
  server\tests\Misc\GuildStandingCommandVerification.cs        NEW  E, 3 facts
  server\tests\Misc\ImbuingTableLabelVerification.cs           NEW  F, 1 fact
D:\UO\shard-migration
  tools\content_index.py, tools\test_content_index.py          M    Part G
  notes\cc-P29-defect-batch-2.md                               NEW  this note
  notes\cc-P29-tools\                                          NEW  uodata.py, stones.py, walk.py, fountain_walk.py,
                                                                    steps_walk.py, cliloc.py, med_table.py, mutate.py,
                                                                    tool_red.py (R2's backups deleted after the SHA-256 match)
```

No saved type changed (the pavers are pinned `Static`; the commands add no fields). `docs\` not touched.
`tools\progress.py` not run (it rewrites `README.md` and `tools\progress.json`; Chase's commit script owns that).

---

## 11. Left for the overseer

- **Bug-list rows:** D44, D45, D48 fixed (built, not client-verified). D14 needs `[ClusterFSeedFountainSteps` run and a
  walk in a client. D46 fixed.
- **Two register texts** (section 7).
- **Report D44 upstream** (ModernUO's defect; the patch is the diff).
- The Guild Directory's mining rank ladder (section 5). P27's coin fact's misleading comment (4.4).
- The `PetMimic` `IDurability.MaxHitPoints` setter (3.1), unreachable today.
- The untracked `design\registrar-office\cleanup\` in the shard repo (section 0).

---

## Checklist for Chase (test shard, after deploying `sl-modernuo:cc-p29`)

1. **Talisman (D44).** Give yourself a talisman with Str: `[add RandomTalisman` (BaseTalisman itself is not
   constructible), then `[props` it and set Attributes > BonusStr 10. Note your Str on the status bar. Equip and unequip it four or five times. **Pass:** worn,
   Str is base + 10 every time; off, Str is back to base every time. (Before the fix it climbed 10 per cycle.) A
   quiver with BonusStr works the same.
2. **Meditation at high Int (D45).** `[set Int 500` (or as high as the test character allows) and Meditation 120.
   Cast until mana is about half, then use Meditation. **Pass:** "You enter a meditative trance" almost every try. At
   about 20 mana out of 500 it should still sometimes start (before, nothing below 356). At Int 100 nothing should
   feel different.
3. **Extraction (D48).** `[GuildStanding artificers 15000` on yourself first if needed. Take a weapon with two
   properties, note its durability (e.g. 89 / 89), and extract both at the Imbuing Table. **Pass:** durability reads
   like 72 / 72, then 58 / 58; the first number is never above the second.
4. **Fountain on foot (D14).** As staff: `[ClusterFSeedFountainSteps dryrun` should say "would place 12, already there
   0". Then `[ClusterFSeedFountainSteps` ("placed 12"), and a second time ("placed 0, already there 12").
   - As a player, enter the Underworld by the Trammel entrance and walk to the pool's south shore (about 1122, 966).
   - Step onto the pavers and walk north along them to the last one (1121, 959), next to the fountain.
   - Throw a lucky coin. **Pass:** the coin is used and the fountain's blessing applies.
   - **Report:** whether the client lets you onto the first paver, any paver you cannot step onto, and how they look.
5. **Guild standing (Part E).** `[GuildStanding artificers 15000` and target yourself. It should say "... standing to
   15,000 (Master Artificer)". `[GuildStanding artificers` reads it back. `[GuildStanding artificer 5` should be
   refused with the list of keys. Then run P27's imbue split test: 1 Swing Speed Increase essence in the pack, 2 in
   the bank, imbue a weapon. **Pass:** the confirm page says "3 essences of Swing Speed Increase: 1 in pack, 2 in
   bank", and the pack's one is used.
6. **Imbuing Table label (Part F).** Single-click the Artificers guildmaster's context menu. **Pass:** the entry reads
   **"Imbue Item"** (it read "Salvage Ingots") and opens the Imbuing Table.
