# cc-P227: bonuses for the 8 extended woods (F-28), and D88

Copper Golem, 2026-10-20. Branch `golem/Copper/P227` in both repos. Server only.

## Headlines

1. **Ironwood to Starwood now give their F-28 bonuses** on bows, staves, clubs and wooden shields, from one table we
   own: `server\customizations\ClusterFWoodBonuses.cs`. Normal items get the "Normal" column; exceptional items get
   "Normal" plus "Exceptional adds". Both F-28 tables (weapon and shield) are in it exactly as approved.
2. **P36 never built a `BaseRanged` fall-through.** It shipped Rootwood with no bonus on purpose: `notes\cc-P36-dungeon-build-1.md`
   "Numbers" table, Rootwood row: "Bonuses: none (cosmetic, item 12)". No shard patch touches `BaseRanged`. So there was
   nothing to build on; the table starts here, and Rootwood keeps its row (none).
3. **The hook is two one-line patches, not a `BaseRanged` patch**: a call at the end of `BaseWeapon.OnCraft` (covers
   bows, because `BaseRanged.OnCraft` calls `base.OnCraft` first, and staves and clubs) and at the end of
   `BaseArmor.OnCraft` (wooden shields). `BaseRanged` itself is untouched, so OSI woods on bows run pinned's own switch
   exactly as before.
4. **D88 can be closed.** cc-P36 (F3) already widened the wood range to `<= Rootwood`; every lookup returns a name,
   hue, index and attribute info for all eight woods (fact W6). P67's finding was against the tree before P36 merged.
5. **Labels:** logs and boards name their wood (they fall back to `GetName` since the woods' cliloc is 0). Weapons and
   shields show **no** wood name for any wood in pinned, OSI woods included, so ours already match the OSI woods there.
   Nothing added; see decisions.
6. Tests: 41 new cases in `ExtendedWoodBonusesVerification`, all seen failing first; full suite **1803 passed, 4
   skipped** through `docker\uo\build.sh`, image `sl-modernuo:cc-P227` built.

Pinned source: `D:\UO\ModernUO-pinned` is **not on this PC**. I read pinned from the builder image instead
(`git archive HEAD` of `/build/modernuo` in `sl-uo-builder:latest`, which printed `d4531cd94b739613155225c234900de9f47d2c88`,
the commit in `docker\uo\Dockerfile:3`), into my scratchpad. Every pinned file:line below is from that copy.

## What pinned does today (re-verified)

- `UOContent/Items/Weapons/Ranged/BaseRanged.cs:195-213` `OnCraft`: `base.OnCraft(...)` then, when `Core.ML`,
  `ApplyWoodBonuses(typeRes)` (`:207-210`), regardless of quality. The prompt's `:230-234` has moved to `:206-210`.
- `:215-258` the switch: Oak luck 40, damage 5; Ash speed 10, LSR 20; Yew hit chance 5, damage 10; Bloodwood regen hits
  2, leech 16; Heartwood the random pick; Frostwood 60 physical / 40 cold, damage 12. Default: nothing. (Prompt's
  `:239-281`.)
- `:260-295` `ApplyHeartwoodBonus`, **private**: one `Utility.Random(6)`: luck 40, durability 50, LSR 20, speed 10, hit
  chance 5, hit life leech 10. (Prompt's `:284-320`.)
- `Items/Weapons/BaseWeapon.cs:639-764` `OnCraft`: sets Quality, Resource (under `Core.AOS`), runic attributes, then the
  exceptional 35 damage increase; ends `return quality;` at `:763`.
- `Items/Armor/BaseArmor.cs:533-615` `OnCraft`: Quality, Resource, exceptional resists (not for ML shields), runic;
  ends `return quality;` at `:614`.
- `Misc/AOS.cs:1640-1650`: setting a weapon or armor `DurabilityBonus` rescales hit points itself.
- `BaseWeapon.AddNameProperty` `:2838-2883` and `BaseArmor.AddNameProperty` `:1193-1250`: the material prefix exists only
  for the eight OSI metals, three leathers and six scales. No wood, OSI or ours.
- `Log.cs:49-63`, `Board.cs:55-69` `GetProperties`: a non-standard wood adds its cliloc, or `CraftResources.GetName` when
  the cliloc is 0.

## What changed

ShatteredLegacy:

| File | Change |
|---|---|
| `server/customizations/ClusterFWoodBonuses.cs` (new, 279 lines) | `WoodBonus` (one row's numbers), `WoodRow(Normal, ExceptionalAdds)`; `WeaponRow` `:75` and `ShieldRow` `:113`, F-28's two tables; `IsWoodWeapon` `:150`, `IsWoodShield` `:154`; `OnCraft(BaseWeapon)` `:158`, `OnCraft(BaseArmor)` `:181`; `Apply` `:203`, `:233`; `HeartwoodExtra` `:255` |
| `server/patches/BaseWeapon-wood-bonuses.patch` (new) | one call, `ClusterFWoodBonuses.OnCraft(this);`, before `return quality;` in `BaseWeapon.OnCraft` (pinned `:763`) |
| `server/patches/BaseArmor-wood-bonuses.patch` (new) | the same in `BaseArmor.OnCraft` (pinned `:614`) |
| `docker/uo/apply-patches.sh:771-778` | the two patches applied after the arms-lore ones, with the reason |
| `server/tests/Items/ExtendedWoodBonusesVerification.cs` (new) | facts W1-W6 below |
| `CHANGELOG.md`, `VERSION` | new section 2026.10.20.22 (Added, Staff); VERSION bumped from 2026.10.20.21 |

Both patches were generated against pinned with the shard's other `BaseWeapon`/`BaseArmor` patches already applied, and
dry-run clean with `patch -p1 --forward --ignore-whitespace --fuzz=0` before the build; both applied in the build.

How the numbers map to properties (F-28 word → property): damage → `Attributes.WeaponDamage` (as pinned's Oak); hit
chance → `AttackChance`; defense chance → `DefendChance`; swing speed → `WeaponSpeed`; LSR → `LowerStatReq`;
durability → `DurabilityBonus`; "50 phys / 50 fire" → `AosElementDamages`, set (not added) as pinned sets Frostwood's;
hit fire area, hit lower attack, hit life/mana/stamina leech → the `WeaponAttributes` of those names; shield resists →
`PhysicalBonus` .. `EnergyBonus` ("all resists +n" adds n to each of the five); reflect physical → `ReflectPhysical`;
mana/hit point regen → `RegenMana`/`RegenHits`.

Exceptional damage stacks on pinned's exceptional 35 (plus Arms Lore) after its cap of 50, the same way pinned's Oak
and Frostwood bow damage already does (an exceptional Frostwood bow at Arms Lore 0 is 47; at 200 it is 62). So an
exceptional Starwood bow at Arms Lore 200 reads 50 + 25 = 75 damage increase. That is what the table says; flagged
below in case it is more than intended.

### Which items count as wood (prompt part 3)

Rule (`IsWoodWeapon`, `IsWoodShield`): a `BaseRanged`, `BaseStaff` or `BaseBashing` weapon, or a `BaseShield`, **whose
crafted `Resource` is a wood** (`CraftResources.GetType == Wood`). How I decided: F-28 names bows, staves, clubs and
shields, so the class picks the kind; the resource decides whether it is wooden, because metal maces and metal shields
never carry a wood resource (they are crafted from ingots). Counted from pinned `DefCarpentry.cs:296-358`,
`DefBowFletching.cs` and the shard's `CarpentryCraftRegistrations.cs`:

- Bows (Fletching, `BaseRanged`), 13 in pinned `DefBowFletching.cs`'s `AddCraft` lines: Bow, CompositeBow, Crossbow,
  HeavyCrossbow, RepeatingCrossbow, Yumi, BarbedLongbow, FrozenLongbow, LongbowOfMight, MysticalShortbow,
  RangersShortbow, SlayerLongbow, TheNightReaper. The rule covers any other `BaseRanged` crafted from wood.
- Staves (Carpentry, `BaseStaff`), 10: ShepherdsCrook, QuarterStaff, GnarledStaff, WildStaff, PhantomStaff,
  ArcanistsWildStaff, AncientWildStaff, ThornedWildStaff, HardenedWildStaff, and GargishGnarledStaff (shard
  `CarpentryCraftRegistrations.cs`). BlackStaff is `BaseStaff` but no craft makes it.
- Clubs (Carpentry, `BaseBashing`), 1 craftable: Tetsubo. `Club` is `BaseBashing` but no craft makes it.
- Shields (Carpentry, `BaseShield`), 1: WoodenShield (`DefCarpentry.cs:356`). WoodenKiteShield is a smith's item (iron).
- **Not** included: Bokuto (`BaseSword`) and Fukiya (`Item`, not a weapon class), both Carpentry wood items F-28 did not
  name; the Woodland armor and other wooden armor (not shields).

### Rules from the entry (part 4)

- **No Self Repair from wood:** no row sets it and the Heartwood pick has none. Runic tools cannot add it either
  (`BaseRunicTool-no-random-self-repair.patch`, existing). Fact W5 crafts 528 wood items and finds none.
- **Lower level requirement** is stored (`WoodBonus.LowerLevelReq`: Ironwood 2, Starwood 5 on both rows) and applies
  nothing. F-12 is not built, so there is no level to lower.
- **Starwood's extra** is pinned's Heartwood pick: `HeartwoodExtra` is a copy of the private
  `BaseRanged.ApplyHeartwoodBonus`, same six outcomes, same single `Utility.Random(6)`. It had to be a copy because the
  pinned method is private and only on bows, and Starwood staves and clubs need it too. Fact W4 holds the copy to pinned
  by calling pinned's private method through reflection for each of the six rolls.

### D88 (part 5)

`server\customizations\ResourceInfo.cs:1174`: `>= CraftResource.RegularWood and <= CraftResource.Rootwood => Wood`
("cc-P36 F3: was <= Frostwood"). With that, for Ironwood to Starwood (and Rootwood): `GetType` is Wood, `GetStart` is
RegularWood (`:1182-1190`), `GetIndex` is `resource - RegularWood` (`:1195-1205`), `GetInfo` returns the `m_WoodInfo`
entry (`:1141-1163`), `GetHue` its hue, `GetName` its name. `GetLocalizationNumber` returns **0** for them: their
`m_WoodInfo` entries have cliloc 0 (`:1018-1087`) because the client has no cliloc for them, which is why logs and
boards fall back to the name. Fact W6 checks all of it, plus `GetFromType` for each log and board, and each log's and
board's hue and name line. Nothing needed fixing. **D88 can be closed** (fixed by cc-P36 F3, verified by cc-P227).

### Labels (part 6)

- **Logs and boards:** the property list has the wood's name ("Ironwood"); hue is the table's. Checked by W6 through
  the real property list (`PropertyListReader`). Same as the OSI woods, except theirs come from a cliloc.
- **Bows, staves, clubs, shields:** pinned adds no wood name to any wood weapon or shield (`AddNameProperty` only knows
  metals, leathers and scales), so an Oak bow and an Ironwood bow both read "bow". Ours already behave "the way the OSI
  woods do". Their bonuses now show as normal property lines. Chase's answer 4 on F-28 says "labeled" meant the stats.
  F-28's overseer note "pinned shows the OSI woods' names through `CraftResources` clilocs" is true for logs and boards
  only.

## Tests

`server\tests\Items\ExtendedWoodBonusesVerification.cs`, 41 cases. Each drives pinned's real `OnCraft` with the wood's
log (Fletching, bows) or board (Carpentry), with Arms Lore 0 so the exceptional damage increase is exactly 35. The
expected rows are written out in the test from F-28 independently of the table.

| Fact | Cases | What |
|---|---|---|
| W1 | 16 | each of the 8 woods, normal and exceptional: a Bow, QuarterStaff and Tetsubo get exactly the weapon row (every other tracked property 0) |
| W2 | 16 | the same for a WoodenShield and the shield row |
| W3 | 6 | Oak and Frostwood bows match pinned exactly, normal and exceptional (Oak 5 / 40 damage and luck 40; Frostwood 60/40, 12 / 47); their staff, club and shield get nothing; Rootwood gets nothing anywhere |
| W4 | 1 | Starwood's extra equals pinned's private Heartwood pick for each of the 6 rolls |
| W5 | 1 | 528 items (11 woods x 2 qualities x 6 rolls x 4 items): no Self Repair |
| W6 | 1 | resource info for the 8 woods and Rootwood: type, index, name, hue, attribute info, `GetFromType` for log and board, log and board hue and name line |

**Seen failing first.** One red run (`build.sh --tests-only`) with five temporary mutations, each tagged `RED-RUN` and
reverted from saved copies afterwards (`git status` showed `ResourceInfo.cs` unmodified after the revert):
the wood range back to `<= Frostwood`; Oak, Frostwood and Rootwood given Ironwood's rows; Rootwood treated as wood; a
Self Repair line in `Apply`; Heartwood rolls 0 and 1 swapped. Result: **all 41 new cases failed**, each for its own
reason (W1 Ironwood exceptional: expected "Damage=49 Durability=50 LowerStatReq=20", actual "Damage=35"; W2 Runewood:
expected the row, actual ""; W3 Rootwood: actual "Durability=50 SelfRepair=1"; W4 roll 0: expected "Luck=40", actual
"Durability=50"; W5: "OakWood Bow (exceptional False, roll 0): self repair 1"; W6: expected Wood, actual None). The
range mutation also failed the existing guards on it (CleanUpPropertyWeight `AnExtendedWoodResolves` x8, three
StarterResources facts), as it should.

**Green.** Two full runs of `build.sh -t sl-modernuo:cc-P227`:
- Run 1: 1802 passed, 1 failed, 4 skipped. The failure was
  `CovetousVoidSpawnVerification.SetupPlacesTheControllersThePoolTheSpawnersAndThePaths`: "a vortex elemental at
  (5500, 1815, 0)" outside `Level3Bounds` (a randomly placed spawn). It passed in the red run and in run 2; nothing here
  touches it. In the red run `LootBoxFanfareVerification` failed the same way (a random count 4 against 5-6) and passed
  in both green runs. Both look flaky; worth a bug row if they recur.
- Run 2: **1807 total, 1803 passed, 4 skipped, 0 failed**; image `sl-modernuo:cc-P227` built.

After run 2 I changed comments only: `ClusterFWoodBonuses.cs` (the header's pinned line numbers and the register
wording) and one comment in the test (pinned Log/Board line numbers). No code changed after the green build.

## Deviations and decisions for Chase

Register line for `docs\fidelity-principle.md` (agents do not edit `docs\`; the overseer adds it):
- **Extended wood bonuses (cc-P227, F-28):** Ironwood to Starwood give bonuses on bows, staves, clubs and wooden shields
  from `ClusterFWoodBonuses`; normal gets the theme line, exceptional adds a second line. OSI has six woods and gives
  bonuses to bows only; the OSI woods are unchanged. Ours.

Decisions I made:
1. **Hook in `BaseWeapon.OnCraft`/`BaseArmor.OnCraft`, not a `BaseRanged` fall-through.** The prompt and F-28 say
   "the `BaseRanged` fall-through". That would have needed three patches (`BaseRanged`, plus `BaseWeapon` for staves and
   clubs, plus `BaseArmor` for shields) and changing pinned's switch. Two one-line calls at the end of the two base
   `OnCraft`s reach all four kinds and leave `BaseRanged` untouched. Effect is the same: applied once at craft time,
   after quality, Resource, runic and exceptional bonuses. Pinned's switch still runs after ours on bows, and does
   nothing for our woods.
2. **Starwood's Heartwood pick is a copy**, held to pinned by W4 (pinned's is private and bows-only).
3. **Runewood shield "spell channeling, faster casting 0":** sets Spell Channeling with no -1 faster casting (a runic's
   spell channeling carries -1; ours does not). If a runic already gave the shield spell channeling, it keeps the
   runic's -1. Small edge; say if it should clear it.
4. **Exceptional damage is uncapped above 50**, like pinned's own Oak/Yew/Frostwood bows. Starwood exceptional at Arms
   Lore 200 reaches 75 damage increase. Say if the wood's damage should count inside the 50 cap instead.
5. **Bokuto and Fukiya are left out** (not a bow, staff or club). Easy to add a class if wanted.
6. **No wood name on weapons or shields**, because pinned shows none for any wood. If you want "Ironwood bow" style
   names (for all woods, OSI included), it is a `BaseWeapon`/`BaseArmor` `AddNameProperty` patch and a visible
   deviation; say so and it is a short prompt.
7. **Order with P228 (F-29):** this table carries its own exceptional gap and is not scaled by P228's x1.5, which works
   on `GetResourceAttrs()`. The extended woods' `CraftAttributeInfo` entries are still empty (`ResourceInfo.cs:516-525`,
   "hue only"), so P228 multiplies nothing for them.

Not fixed, noted: an extended log's commodity deed description is `1075062 + (resource - RegularWood)` (pinned
`Log.cs:43-45`), i.e. 1075070-1075077 for our woods, which may be another item's cliloc or none. I could not read the
client's `Cliloc.enu` here (the vseUOAware lookup returned "No cliloc entry" even for known numbers, and the files look
compressed), so this is **unverified**; cc-P24 flagged the same. Out of this task's scope.

## For Chase (in the client, on the test shard)

1. `[add IronwoodBoard 50`, `[add StarwoodLog 50`: the board and log show their wood name and hue.
2. With Fletching 200: craft a Bow from Ironwood logs until you have one normal and one exceptional. Normal: durability
   +50%. Exceptional: also damage increase 35+ and +14, lower requirements 20%.
3. Starwood bow, exceptional: luck 100 + damage 25 + hit chance 8 + one random extra (luck, durability, LSR, swing
   speed, hit chance or hit life leech).
4. Carpentry: a Quarter Staff and a Tetsubo in Emberbark: damage shown as 50% physical, 50% fire; exceptional adds
   hit fire area 10%.
5. Carpentry: a Wooden Shield in Runewood: energy resist +4, mana regeneration 1; exceptional also spell channeling and
   no faster casting -1. Voidwood: every resist +1 (exceptional +2 and hit point regen 2).
6. An Oak bow still reads luck 40, damage 5, and an Oak quarter staff reads nothing extra.
7. No wood item ever shows Self Repair.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-20. Neither repo
BLOCKED. Code: 7 files pending (CHANGELOG.md, VERSION, docker/uo/apply-patches.sh, ClusterFWoodBonuses.cs, the two
patches, the test). Docs: this note.

```
Repo Result
---- ------
code dry run
docs dry run
```

Repo size rule: the largest file touched is `CHANGELOG.md` (94 KB); every new file is under 20 KB. Scratch (the pinned
source copy, build logs) stayed in my session scratchpad, outside both repos.

P227 DONE
