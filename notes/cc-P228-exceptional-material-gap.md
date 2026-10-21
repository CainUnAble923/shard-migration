# cc-P228: exceptional items get their material's bonuses x1.5, every material (F-29)

Copper Golem, 2026-10-20. Branch `golem/Copper/P228` in both repos. Server only.

Earlier today this task stopped before starting because P227 was not merged yet. It now is: ShatteredLegacy `origin/main` and
this branch both carry `147727e` (Merge golem/Copper/P227), and `server\customizations\ClusterFWoodBonuses.cs` is in the
tree. Both repos were clean except this note when I started.

## Headlines

1. **One rule, one place:** `server\customizations\ClusterFExceptionalMaterial.cs`. `Attrs(resource, exceptional)` returns
   the material's own `CraftAttributeInfo` for normal and low quality items (the same object pinned reads, so they read
   exactly what they read before), and for exceptional items a copy with every **positive** value **x1.5, rounded half up**
   (`(v * 3 + 1) / 2`). Runic ranges are copied unchanged. Penalties (negative values) are not changed.
2. **Pinned's eight live reads now ask it**: resists, durability, lower requirements and luck on armor; durability, lower
   requirements, element damage and luck on weapons. These are two small patches, each line replacing
   `CraftResources.GetInfo(_resource)?.AttributeInfo`. Because the read is live, every armor, shield and weapon of every
   ore, leather and scale gets the rule.
3. **The OSI woods needed a third, separate hook.** Their `CraftAttributeInfo` is empty, in pinned and in ours. Their
   bonuses are `BaseRanged`'s private craft-time switch (bows only), so one patch wraps that call: snapshot, switch, then
   x1.5 on what the switch added. An exceptional Oak bow reads luck 60 and damage 35 + 8; Frostwood reads 40 physical /
   60 cold and damage 35 + 18.
4. **Not multiplied:** runic properties, pinned's own exceptional bonuses (damage 35 plus Arms Lore, the resist points,
   +20 durability), and P227's extended-wood table (it applies before the snapshot, so the wrap never sees it).
5. **Cloth has no material values to scale.** Pinned has no cloth `CraftResource`, and `BaseClothing` reads no
   `CraftAttributeInfo`, not even for leather shoes. So nothing changes for cloth, and a test holds that.
6. **Caps hold:** the player's resist is capped by pinned's `Mobile` as before. A piece can show 75 fire but the wearer
   stays at 70.
7. **Tests:** `ExceptionalMaterialVerification`, 47 cases. Every case that tests the change was seen failing first in a
   red run; the 21 guard cases (normal rows, cloth, runic armor) pass either way, as they should. Two of P227's W3 rows
   (exceptional Oak and Frostwood bows) were updated to the new numbers. Full suite **1855 passed, 4 skipped** (the 4 are
   the existing `MapCheckRealDataVerification` skips) through `docker\uo\build.sh`; image `sl-modernuo:cc-P228` built.

Pinned source: `D:\UO\ModernUO-pinned` is not on this PC. I read pinned from `sl-uo-builder:cc-P227`
(`git archive HEAD` of `/build/modernuo`, which printed `d4531cd94b739613155225c234900de9f47d2c88`, the commit in
`docker\uo\Dockerfile:3`). I took the patched build files from the same image's working tree. Pinned line numbers below
are from that copy.

## Part 1: where the values are read (re-verified)

The prompt's lines were from 7c9215d97; today's pinned is `d4531cd9`. Paths relative to `Projects\UOContent\`.

| Read | Pinned (d4531cd9) | After the shard's existing patches (P226, P227) |
|---|---|---|
| `CraftAttributeInfo` class | ours replaces it: `server\customizations\ResourceInfo.cs:80-573` (values `:97-526`) | same |
| armor resists | `Items/Armor/BaseArmor.cs:484-497` via `GetResourceAttrs()` `:859-860` | `:484-497`, `:871-872` |
| armor durability | `GetDurabilityBonus` `:893-894` | `:905-906` |
| armor lower requirements | `GetLowerStatReq` `:956-962` | `:968-974` |
| armor luck | `GetLuckBonus` `:1263` | `:1275` |
| weapon durability | `Items/Weapons/BaseWeapon.cs:939-940` | `:945-946` |
| weapon lower requirements | `GetLowerStatReq` `:955-959` | `:961-965` |
| weapon element damage | `GetDamageTypes` `:2366-2377`, `ApplyCraftAttributeElementDamage` `:2384` | `:2387-2398`, `:2405` |
| weapon luck | `GetLuckBonus` `:2908` | `:2930` |
| OSI wood bow bonuses | `Items/Weapons/Ranged/BaseRanged.cs:207-210` (call), `:215-258` switch, `:260-295` Heartwood | unpatched |

Other readers of `AttributeInfo`, checked so I would not miss one: `Engines/Craft/Core/Enhance.cs:143-181` (only asks
whether a value is above 0, to pick what enhancing can add, so it is unaffected), `BaseRunicTool.cs:267-278` and
`:597-608` (runic ranges from the tool's resource), and ours `ClusterFCompactAdminTools.cs:451` (an admin dump) and
`Items\Functional\Automaton\KotlAutomaton.cs:150` (a creature, no quality). `WeaponGoldIncrease` and `ArmorGoldIncrease`
are **read nowhere** in pinned, and no material sets them. They are scaled in the copy for completeness, but gold increase
does nothing today.

`ResourceInfo.cs:502-525`: the six OSI woods, the eight extended woods and Rootwood all have empty `CraftAttributeInfo`.

## What changed (parts 2 to 4)

ShatteredLegacy:

| File | Change |
|---|---|
| `server\customizations\ClusterFExceptionalMaterial.cs` (new, 159 lines) | `Scale` `:41`, `Attrs(resource, exceptional)` `:45` (cached scaled copy per material), `Attrs(BaseArmor)` `:62`, `Attrs(BaseWeapon)` `:65`, `Scaled` `:68` (runic ranges copied unchanged), `BeginWoodBonus` `:105`, `EndWoodBonus` `:113`, `Rescale` `:158` |
| `server\patches\BaseArmor-exceptional-material.patch` (new) | `GetResourceAttrs()` asks `Attrs(this)` (built tree `:871-873`); durability `:906`, lower requirements `:968` and luck `:1273` now go through it too |
| `server\patches\BaseWeapon-exceptional-material.patch` (new) | durability `:945-946`, lower requirements `:961`, element damage `:2387`, luck `:2930` ask `Attrs(this)` |
| `server\patches\BaseRanged-exceptional-wood.patch` (new) | `BeginWoodBonus` / `ApplyWoodBonuses` / `EndWoodBonus` around pinned's one call (`:209-212`) |
| `docker\uo\apply-patches.sh:784-793` | the three patches, applied last, after the arms-lore and wood-bonus patches, with the reason |
| `server\tests\Items\ExceptionalMaterialVerification.cs` (new) | facts X1-X7 below |
| `server\tests\Items\ExtendedWoodBonusesVerification.cs` | W3's exceptional Oak and Frostwood rows: `Damage=43 Luck=60`, `Cold=60 Damage=53 Physical=40` (were 40/40 and 40/47/60), with a comment |
| `CHANGELOG.md`, `VERSION` | new section 2026.10.20.23 (Changed, Staff); VERSION from 2026.10.20.22 |

Clash with P226 (Arms Lore): its hunks are in `OnCraft`, `OnHit` and `TryLowerDurability`; mine are in the four read
methods. No hunk shares lines, and all three patches dry-ran clean with `--fuzz=0` on the patched tree before the build.
All three applied in the build.

How each part of the prompt is met:
- **Part 2, rounding:** half up, `(v * 3 + 1) / 2`: 1→2, 2→3, 3→5, 5→8, 15→23, 40→60. Applied per value, at the read.
- **Part 3:** runic properties are written into the item's `Attributes` at craft time; the rule never touches those. The
  runic **ranges** in the scaled copy are pinned's (X6). Pinned's exceptional damage is set in `BaseWeapon.OnCraft`,
  before the bow wrap takes its snapshot, so the wrap never sees it (X3: Oak is 35 + 8, not 40 x1.5). The P227 table
  runs at the end of `BaseWeapon.OnCraft`/`BaseArmor.OnCraft`, also before the snapshot, and writes `Attributes`, never
  `CraftAttributeInfo` (X4).
- **Part 4, caps:** item resists are not capped by the item in pinned (they never were); the wearer's total is capped by
  `Mobile.UpdateResistances`/`GetMaxResistance` (`Projects/Server/Mobiles/Mobile.cs:3276`, `:3296`). X7 holds it.
- **Part 4, element damage:** the material's element share is **scaled as a bonus**, and physical gives up the
  difference. Pinned's `ApplyCraftAttributeElementDamage` takes each share out of what physical has left and stops at 0,
  so the split always totals 100 (X2 asserts the sum on every row). Results: Valorite 40 physical / 10/20/10/20
  becomes 10 / 15/30/15/30, Celestial 40 / 15x4 becomes 8 / 23x4, Mythril 50/50 becomes 25/75. The largest ore share
  sum is 92 (Celestial), so physical never runs out today. Frostwood bows follow the same rule: its 40 cold is the share,
  60 exceptional, physical 40.

### Part 5: existing items in the test world

The read is live, so an exceptional armor, shield or weapon already in the world shows the new resists, luck, lower
requirements, element damage and durability bonus as soon as it is next read. Two things were fixed at craft time and do
**not** change:
- **Maximum hit points.** They were scaled once, when crafted, with the old durability bonus. A later quality or
  resource change, or a durability-bonus change, unscales with the new, larger bonus, so such an item can drift a few
  points lower. New crafts are exact, because each setter rescales.
- **An exceptional Oak to Frostwood bow's wood bonuses** stay at pinned's values; only new crafts get x1.5.

The fresh-world wipe makes both moot.

## Tests

`server\tests\Items\ExceptionalMaterialVerification.cs`, 47 cases. Every expected number is written out from pinned's
values, not computed by the rule's code. Arms Lore 0 and an Elf crafter, so the exceptional damage is exactly 35. A Human
crafter reads 36, because Jack of All Trades counts Arms Lore as 20; that cost me one build.

| Fact | Cases | What |
|---|---|---|
| X1 | 14 | Armor, normal and exceptional: Valorite, Gold, Dull Copper (OSI ores), Celestial (shard ore) plate chests; Spined (OSI) and Burrowhide (shard) leather chests; Red scales dragon chest. Normal = pinned exactly; exceptional = x1.5 on resists, durability, luck, lower requirements; red scales' -3 cold unchanged |
| X2 | 10 | Broadsword, normal and exceptional: Valorite, Gold, Dull Copper, Celestial, Mythril: element split (totals 100), durability, luck, lower requirements |
| X3 | 10 + 6 | Oak, Ash, Yew, Bloodwood, Frostwood bows normal (= pinned) and exceptional (x1.5); Heartwood all six rolls both ways |
| X4 | 1 | Ironwood (shard wood) exceptional bow and shield = F-28 exactly, not x1.5; no live material value either |
| X5 | 3 | Robe and Boots in no resource, Spined, Barbed: exceptional reads the same as normal (cloth has nothing to scale) |
| X6 | 2 | Runic ranges unscaled for every resource, and a normal item reads pinned's own `CraftAttributeInfo` object; a Valorite runic-hammer plate chest's runic properties are the same normal or exceptional |
| X7 | 1 | A red-scale chest bringing a player's fire to the cap exactly: exceptional, the chest reads cap + 5 and the player stays at the cap |

**Seen failing first.** I ran red with three temporary mutations, each tagged `RED-RUN`, then reverted them from saved
copies (`grep RED-RUN` found 0 afterwards):
1. the BaseArmor and BaseWeapon patches skipped by name (the live read as pinned);
2. `Scaled` doubling `RunicMinIntensity`;
3. `Rescale` ignoring the snapshot (scaling everything on the bow, not just what the wood added).

Red run 1: 37 failed / 1818 passed. Red run 2, after fixing a test bug (X7 used `EquipItem`, which did not equip, so it
failed on the normal step for the wrong reason; it now uses `AddItem` as `ArmourSetBonusVerification` does): the same 37
failed. X7 now failed for the right reason: "Expected: 75, Actual: 70", the chest without the x1.5. The failing new cases
are every exceptional row of X1 (7) and X2 (5), all 11 X3 exceptional cases, X4, the X6 runic-range fact and X7. Samples:
X1 Valorite: expected "Phys=11 Fire=3 Cold=7 Poison=8 Energy=7", actual "Phys=9 Fire=3 Cold=5 Poison=6 Energy=5"; X2
Celestial: expected "Phys=8 Fire=23 ...", actual "Phys=40 Fire=15 ..."; X3 Oak: expected "Damage=43 Luck=60", actual
"Damage=62 Luck=60"; X4: expected "Damage=49 Durability=50 LowerStatReq=20", actual "Damage=75 ... LowerStatReq=30"; X6:
expected (1, 2, 40, 100), actual (1, 2, 80, 100). The other 11 red failures were P227's W1 exceptional rows (8) and W3's
exceptional Oak, Frostwood and Rootwood rows, all from mutation 3, as expected.

The red runs crafted with a Human (36 damage, see above), so X3's and X4's red failures carried that offset as well as
the mutation. The green run uses an Elf; I did not repeat the red run with the Elf.

**Guards that cannot fail from this change** (21 cases): the normal rows of X1, X2 and X3 (they prove normal is
untouched), X5 (nothing in the change reaches clothing) and X6's runic armor fact (the runic tool reads `GetInfo`
directly). They passed in the red runs and the green run.

**Green:** `docker/uo/build.sh -t sl-modernuo:cc-P228`: 1855 passed, 4 skipped, image built. Logs are in my scratchpad
(`red-run.log`, `red-run2.log`, `green-run.log`), not in either repo.

## Deviations and decisions for Chase

Register line for `docs\fidelity-principle.md` (agents do not edit `docs\`; the overseer adds it):
- **Exceptional material gap (cc-P228, F-29):** an exceptional item reads its material's bonuses x1.5 (half up) for
  every ore, leather, scale and wood, OSI's included: resists, durability, luck, lower requirements and element damage
  (live, `ClusterFExceptionalMaterial`), and the OSI woods' bow bonuses (at craft). Normal items read OSI's values. OSI
  gives the same material bonus at any quality. Ours, and a deviation for OSI's materials.

Decisions I made:
1. **Penalties are not multiplied.** The scales' -3 resist and Frost's -2 fire stay as they are on exceptional pieces.
   F-29 says "bonuses x1.5", and making exceptional worse at anything goes against "widen the gap". If you want the
   penalty x1.5 too (-3 → -5), it is a single change in `Scale`.
2. **Rounding half up** (the prompt's default): 3 → 5, 1 → 2. Small values gain the most (a Copper chest's 1 fire becomes
   2).
3. **Element damage scales as a share taken from physical.** This is what pinned's read does, and the split stays at 100.
   Frostwood bows follow the same rule (60 cold / 40 physical exceptional) rather than keeping the 60/40 split.
4. **OSI woods: x1.5 at craft time, bows only**, because that is where pinned gives them anything. Staves, clubs and
   shields in OSI woods still get nothing, as in pinned and in P227.
5. **Heartwood's random extra is scaled too** (it is the wood's bonus): luck 60, durability 75, LSR 30, speed 15, hit
   chance 8, leech 15.
6. **The exceptional bow's damage can pass 50**, as P227's note 4 already flags: Yew exceptional at Arms Lore 0 is
   35 + 15 = 50, Frostwood 35 + 18 = 53, and at Arms Lore 200 Frostwood is 50 + 18 = 68. Pinned already stacks wood
   damage outside the cap.
7. **Durability is scaled as a material bonus**, so exceptional pieces of Dull Copper, Valorite, the post-Valorite ores
   and Adamantium weapons get more maximum hit points (an exceptional Adamantium plate chest: bonus 225 + 20 instead of
   150 + 20).
8. **Gold increase** is scaled in the copy but read nowhere in pinned, and no material sets it, so it does nothing.

Found, not fixed: none.

## For Chase (in the client, on the test shard)

1. `[add PlateChest`, then `[props` it: set Resource Valorite. It reads physical 9, cold 5, poison 6, energy 5. Set
   Quality Exceptional and it reads 11 / 7 / 8 / 7 (fire stays 3).
2. Craft a Golden broadsword until you have a normal and an exceptional one: luck 40 and lower requirements 50% normal;
   luck 60 and 75% exceptional.
3. A Celestial weapon: normal 40% physical and 15% each element; exceptional 8% physical and 23% each.
4. Fletching: an exceptional Oak bow reads luck 60 and damage increase 43% (at Arms Lore 0); a normal one 40 and 5%. An
   exceptional Frostwood bow reads 40% physical / 60% cold.
5. A red dragon-scale chest: fire 13 normal, 18 exceptional; cold stays 0 (the -3 is not made worse).
6. Wear enough exceptional pieces to pass 70 in a resist: your status shows 70, not more.
7. An exceptional Ironwood bow still reads exactly what P227 showed (damage 49%, durability 50%, lower requirements 20%).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-20. Neither repo
BLOCKED. Code: 9 files pending (CHANGELOG.md, VERSION, docker/uo/apply-patches.sh, ExtendedWoodBonusesVerification.cs,
ClusterFExceptionalMaterial.cs, the three patches, ExceptionalMaterialVerification.cs). Docs: this note. No file is over
5 MB (the largest new file is the 489-line test).

```
Repo Result
---- ------
code dry run
docs dry run
```

P228 DONE
