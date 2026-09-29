# cc-P8: the loot-table patches Chase approved, and the D35 removal

2026-09-29. Server tree `D:\ShatteredLegacy`. Pinned is `7c9215d97` (`D:\UO\ModernUO-pinned`, verified at HEAD).

## 0. Summary

| Gate | Audit predicted | Delivered | Why |
|---|---|---|---|
| 3, treasure chests | 24 files | **0. Stopped, not patched** | Pinned has **none** of the lists gate 3 was costed as. Every one of the 24 needs new *logic* in pinned's chest or map, not an entry in a list. Section 2 |
| 5, stealables | 17 files, 55 types | **17 files, 55 types, 58 entries** | Reproduced exactly. Not a weighted pool: each entry is its own fixed spawn with its own timer. Section 3 |
| `OrcMask` / `TribalMask` | 1 item | **2 items** (`OrcMask` ours, `TribalMask` pinned's) | Section 4. **It is also the only change here that moves treasure-chest odds** |
| D35 | drop 2 types | **dropped, both** | All three preconditions established before removal. Section 5 |

The build numbers and red/green runs are in section 7.

**Two figures in the brief and the audit were wrong when counted:** pinned's stealable table has **80** entries, not 81
(counted from `Entries`, lines 71-173, and matched by the save file's slot count, section 3.4). And gate 3's "entries into
pinned's lists" does not describe pinned's code (section 2).

---

## 1. Rules applied

- Each type name in a patch is spelled by `typeof(...)` in a test, so a transposition fails compilation (section 6's
  irony, handled structurally rather than by care).
- Every patch was dry-run at `--fuzz=0` against a pristine copy of the pinned file before the build, then applied by
  `apply-patches.sh` in the builder (`[patches] Applied: ...` in the log). One patch per file, each as small as its edit.
- Existing entries are not touched, not even where ServUO differs from pinned (section 3.3).

---

## 2. Gate 3, treasure chests: stopped, with the measurement

### 2.1 What the chest rolls today (pinned, this shard: AOS, SE, ML all on)

`TreasureMapChest.Fill` (`Items/Containers/TreasureMapChest.cs:157-292`) has exactly one list, `Artifacts` (19 types, level
6 only). Everything else is a fixed count of draws from `Loot`'s shared pools:

| Level | Gold | Scrolls (uniform over 64 regular) | Magic items | Reagent stacks (40-60 each) | Gems | Artifact |
|---|---|---|---|---|---|---|
| 0 | 50-100 | 0 | 0 | 12 | 2 | no; 75% a level-0 map |
| 1 | 1,000 | 5 | 5 | 3 | 3 | no |
| 2 | 2,000 | 10 | 10 | 6 | 6 | no |
| 3 | 3,000 | 15 | 15 | 9 | 9 | no |
| 4 | 4,000 | 20 | 38 | 12 | 12 | no |
| 5 | 5,000 | 25 | 50 | 15 | 15 | no |
| 6 | 6,000 | 30 | 60 | 18 | 18 | **1 of 19, each 1/19** |

Each magic item is one uniform draw from `_aosWeaponOrRangedOrArmorOrHatOrShieldOrJewelryTypes`, **118 types, each
1/118** before this task. Section 4 changes that pool to 120; nothing else in this task touches the chest.

### 2.2 Why "entries in pinned's lists" does not exist

The 24 files (audit Appendix, "Treasure chests") and what each actually needs, against ServUO pub57's
`Services/TreasureMaps/`:

| Files | ServUO's mechanism | In pinned? | What adding it would be |
|---|---|---|---|
| 10 essences (`EssenceAchievement` ... `EssenceSingularity`) | `ImbuingIngreds`, 12 types; **a new block**: if level > 1, one stack of `level` of one type (`TreasureMapChest.cs:393-400`) | no list, no block | ~8 lines of new logic. **2 of the 12 (`AbyssalCloth`, `EssencePersistence`) exist in neither tree**, so faithful means porting two more types, and dropping them changes the other ten's odds from 1/12 to 1/10 |
| `KelpWovenLeggings`, `ValkryieArmor`, `AntiqueWeddingDress`, `RunedDriftwoodBow`, `GrapeVine`, `LargeFishingNet` (+ `GrapeBunch`, which `GrapeVine` makes) | `SOSArtifacts` at 0.4% x level, `SOSDecor` at 0.6% x level, **only on the `isSos` path** | **no SOS path.** Pinned's fished-up chest calls the ordinary `Fill` with the level clamped to 1-4 (`Engines/Harvest/Fishing.cs:304`) | a new `isSos` parameter, a patch to `Fishing.cs` as well, and ServUO's whole SOS branch (its gold, scroll, item and reagent counts all differ too) |
| `CoffinPiece` | `ArtifactsLevelSeven`, level 7 only | **no level 7** (pinned's item-count switch ends at 6, `TreasureMapChest.cs:203-212`) | a new map tier |
| `CreepingVine` | `GetRandomSpecial`, one of 8 cases | no specials roll | the specials roll; **4 of its 8 cases (`Skeletonkey`, `TastyTreat`, `ScrollOfAlacrity`, `ScrollOfTranscendence`) exist in neither tree** |
| `Allosaurus`, `Dimetrosaur`, `Saurosaurus`, `SilverbackGorilla` (+ `PerfectBanana`, which the gorilla drops) | `m_EodonSpawnTypes`, selected when `SpellHelper.IsEodon(map, p)` (`TreasureMap.cs:152-161, 705-723`) | pinned has **one** guardian table for every facet (`TreasureMap.cs:22-31`), and **its maps only ever point at Trammel or Felucca** (192 points from `Data/treasure.cfg`; labels at `:480` are Felucca/Trammel only) | per-facet selection plus a treasure-map location system that can send a player to Eodon. **No chest is ever dug in Eodon today**, so a guardian table alone reaches nothing |

**Delivered as list entries: 0 of 24.** No subset is a list entry. The nearest thing is the imbuing block, which is new
logic with two absent types in it.

### 2.3 The fidelity fork nobody has decided

On this shard's expansion ServUO does **not** run the code above. `TreasureMapInfo.NewSystem => Core.EJ`
(`TreasureMapInfo.cs:54`), and the shard runs Endless Journey. So "match ServUO" means ServUO's rewrite, which the audit
itself said to leave (24 files alone, three after gate 3, "Leave"). In the rewrite, imbuing ingredients come only from
Ter Mur-facet chests (`TreasureMapInfo.cs:582`), not from every chest over level 1. The legacy block and the rewrite put
the essences in different chests at different rates. **Which ServUO is "ServUO" here is a decision, and the approval did
not make it.**

### 2.4 What each option would do to the odds (for Chase)

| Option | Existing chest contents | New | Reach |
|---|---|---|---|
| **Leave (what I did)** | unchanged except section 4's 118 -> 120 | none | 0 |
| Imbuing block, legacy | **none diluted**: it is an extra drop, not a pool entry | levels 2-6: one stack of `level` essences, each type 1/12 (or 1/10 without the two absent types) | 10 files. Essences are near-worthless without imbuing (audit gate 6) |
| SOS branch | changes every SOS chest's gold, scrolls, items and reagents to ServUO's SOS numbers | per SOS chest at level L (1-4 after pinned's clamp): artifact 0.4L%, decor 0.6L% | 6-7 files; two patched pinned files |
| Specials, level 7, Eodon guardians | new rolls on 10-25% of chests; a new tier; guardians on four other facets change too if ServUO's per-facet tables are matched | | each needs absent types or a map system; not costable as "one unit" |

The approval was for "entries into pinned's lists". What exists is a choice among logic ports with a fidelity fork. That
is a different thing from what was approved, so I stopped, per the brief ("An approval given without a number is not an
approval of the number"). **Chase decides; nothing here is built.** The dinosaurs as guardians are a separate, visible
gameplay change and are unreachable without a map-location system as well (row 5 above).

---

## 3. Gate 5, stealable artifacts: delivered

### 3.1 Not a weighted pool, confirmed from the code

`StealableArtifacts.Entries` (`Engines/Stealables/StealableArtifacts.cs:68-174`) is a list of **fixed placements**. Each
`StealableInstance` spawns its own item at its own `Location` and, once stolen, respawns after its own
`RandomMinMax(MinDelay, MaxDelay)` minutes (`:379-419`). No draw chooses between entries. Adding entries changes **no
existing entry's item, place or timer**. The brief's reading holds.

### 3.2 What was added

ServUO pub57's `Items/Functional/StealableArtifactsSpawner.cs:11-223` has 158 entries, 66 types pinned's table lacks.
Classified by `class <Name>\b` in each tree:

- **55 ours, in 17 files** (the audit's file list, reproduced exactly): the 40 in `SADecorationArtifacts.cs`, plus
  `CarvedMyrmydexGlyph`, `DragonTurtleHatchlingNet`, `FigureheadOfBmvArarat`, `KingsGildedStatue` (`GildedStatue.cs`),
  `KingsPainting1`/`2`, `SacredLavaRock`, `ShipsBellOfBmvArarat`, `SternAnchorOfBmvArarat`, `StretchedDinosaurHide`,
  `WakuOnASpit`, `WhiteTigerFigurine`, `CrownOfArcaneTemperament`, `MysticsGuard`, `LightInTheVoid`, `StaffOfResonance`,
  `ValkyriesGlaive`. The full list is `OursAdded` in the test.
- **58 entries** for them: the three Blackthorne types appear on both Trammel and Felucca, as in ServUO.
- **Not added, 11:** `ArcaneTable`, `ArtifactBookshelf`, `BambooStoolArtifact`, `BlanketOfDarkness`,
  `HangingPlatemail{Arms,Leggings,Tunic}`, `IncenseBurner`, `TortureRack{East,South}` exist in neither tree;
  `AcademicBooksArtifact` is **pinned's** (three Bedlam entries). It is outside this gate's 55 but the same approval would
  cover it: a one-line follow-up if wanted.

Entries are ServUO's values unchanged (map, point, delays), in ServUO's order, with ServUO's section comments.

### 3.3 Appended, not interleaved: the save is why

`Serialize` writes one slot per entry **by index** (`:246-264`) and `Deserialize` hands saved slot `i` to `Entries[i]`,
creating fresh instances for any index past the saved length (`:279-299`). **The live world has the spawner enabled with
80 saved slots**: `Saves/StealableArtifacts/StealableArtifacts.bin` is 963 bytes = version 1, enabled 1, count 0x50, then
80 x (4-byte serial + 8-byte delta time). An entry inserted mid-table would give every later saved item to the wrong
entry, so the 58 are appended after pinned's 80. On the next live load, the 58 get fresh instances and spawn at the next
15-minute check. The test world has the spawner **off** (`0100`, enabled 0), in `Saves-test` and all three set-aside
copies, so nothing spawns there until a developer runs `[GenStealArties`.

**Not done, deliberately:** ServUO moves five *existing* Doom entries under `Core.TOL` (Brazier, StuddedTunic,
ZyronicClaw, TitansHammer, IncenseBurner). Changing an existing entry's location is not adding content; left for a
separate decision.

### 3.4 Each entry reachable: three guards checked

1. **The place exists.** Configured is not present (AGENTS.md). Read from the shard's own client files
   (`D:\ShatteredLegacy\client-data\classic-client`): the statics index at every one of the 58 points. 54 sit in blocks
   with statics; the other four (`CrownOfArcaneTemperament` 877,527; `StaffOfResonance` 585,853; `ValkyriesGlaive`
   843,665; `GargishMemorialStatueArtifact` 948,393) have none, so I read their land tiles from `map5LegacyMUL.uop`
   (all 21 UOP chunks resolved by hash): real floor at **z -13, -45, 26, 88**, the entries' own Z (27 against 26 for the
   glaive). Eodon (TerMur y 1496-2125), the Underworld, Ararat (Trammel x 6303) and Blackthorne (x 6298-6455) are all
   built in these files. Scripts: scratchpad `statics_probe.py`, `land_probe.py`.
2. **It can be stolen.** `Stealing.cs:256` refuses anything over `stealing.maxWeightToSteal`, default 10, not overridden
   in any shard JSON. Weights: every decorative type 10 (`DefaultWeight`), `SoulGlaive` 8, `GargishWoodenShield` 5,
   `GargishTalwar` 4 (client tiledata row 0x908; no code override). The test asserts it for all 58; see its header for the
   one it can only bound. Beyond that, the stealables branch needs Stealing 100 (`:228`), as for pinned's own.
3. **The system runs.** On the live world, yes (3.3). On the test world, only after `[GenStealArties`.

**Delivered 55 of 55 types, 17 of 17 files, predicted 17.**

---

## 4. `OrcMask` and `TribalMask` in `Loot.HatTypes`

Pinned `Misc/Loot.cs:313-319` confirmed (the brief's lines are right). ServUO's `Misc/Loot.cs:407-412` ends
`typeof(JesterHat), typeof(OrcMask), typeof(TribalMask)`. `TribalMask` is pinned's (`Items/Clothing/Hats.cs:302`),
`OrcMask` ours (CC9 close). Both appended, in ServUO's order. Both handled, as the brief asked.

**The brief undersold the reach.** `HatTypes` is not only the random-hat roll: **18** private composite pools hold the
same array object (`Loot.cs:470-642`), and `Construct(params Type[][])` draws uniformly over their concatenation
(`:790-815`). So every one of them grows by 2. Counted from the source and asserted at runtime:

| Pool (this shard's usual branch in bold) | N before -> after | each existing entry | each mask |
|---|---|---|---|
| **`_aosHatTypes`** (`RandomHat`) | 15 -> 17 | 6.67% -> 5.88% | 5.88% (masks 11.8% of random hats together) |
| `_seHatTypes` (Tokuno) | 17 -> 19 | 5.88% -> 5.26% | 5.26% |
| **`_aosArmorOrHatTypes`** | 56 -> 58 | 1.79% -> 1.72% | 1.72% |
| **`_aosArmorOrHatOrShieldOrJewelryTypes`** | 69 -> 71 | 1.45% -> 1.41% | 1.41% |
| **`_aosWeaponOrRangedOrArmorOrHatOrShieldTypes`** | 114 -> 116 | 0.877% -> 0.862% | 0.862% |
| **`_aosWeaponOrRangedOrArmorOrHatOrShieldOrJewelryTypes`** (treasure chests, monster loot) | **118 -> 120** | **0.847% -> 0.833%** | 0.833% |
| the 12 other ML/SE/pre-AoS variants | +2 each | falls 1.2-3.6% relative | |

**For the treasure chest (section 2.1):** each existing type's chance per magic-item draw falls by 1.7% relative (1/118 to
1/120). A level-5 chest's 50 draws now include **0.83 masks on average**; a level-6 chest's 60, 1.0. That is the number
the approval did not have. It is small per item and certain to be noticed: masks go from never to about one per
high-level chest.

Alternatives considered before patching:
- **A runtime hook replacing `HatTypes`.** Impossible cleanly: it is a get-only auto-property, and the 18 composites
  captured the original array at type initialisation, so a replacement would reach `HatTypes` and none of the pools.
- **Reflection writing into the array.** Arrays are fixed-length. Rejected.
- **A patch appending two entries.** Chosen: two lines, and the composites follow because they hold the reference.

## 3a. Stealables: alternatives considered

- **A second, additive spawner of ours** with its own persistence: copies upstream logic and runs two respawn timers;
  `docs/subsystem-policy.md` prefers a failing patch to copied upstream logic. Rejected.
- **An extension point.** `Entries` is a get-only array initialised in place; none exists. Rejected.
- **Patch in ServUO's interleaved order.** Breaks the live save's index mapping (3.3). Rejected.
- **Patch appending.** Chosen.

---

## 5. D35: dropped, with the three preconditions established first

**1. Nothing in our tree references either type.** `grep -rn` for all four spellings across `D:\ShatteredLegacy`
(excluding `server/uo`, `server/lib`, `client-data`): the two class files themselves, and **one** test fact,
`TypeIdentityVerification.D35_BothSpellingsAreDistinctTypesAndNeitherShadowsTheOther`, whose own comment says "When D35
is decided and one of each pair goes, delete this fact with it." No loot list, craft entry, spawn row or other test. The
fact was replaced (section 6), not left dangling. (A binary match in `backups/sl-modernuo-rootfs-20260927.tar` is an image
backup holding the compiled DLL, not a save.)

**2. No save holds one.** `tools/save_instance_check.py GauntletsOfAnger ShroudOfDeceit GuantletsOfAnger ShroudOfDeciet`,
plus the three `Saves-test.aside-*` copies and `Snapshots/test/...` by the same parse: **115 type tables**, every one with
the `Server.Items.Dagger` control present, **zero hits for any of the four spellings.** Live `Saves` (1,460 names),
`Saves-test` (202), 3 set-aside test saves, 1 snapshot, 10 `Backups/Automatic`, 99 archived tables (Daily, Hourly,
Monthly). Checked at about 14:50 on 2026-09-29.

**3. No orphaned alias or migration.** No `[TypeAlias]` names any of the four in pinned, ServUO or ours (re-grepped; agrees
with `type-identity.md` 3.1). `server/migrations` has nine files, all `PetMimic`; none for either type.

Then `git rm` of `Items/Artifacts/Equipment/Armor/GauntletsOfAnger.cs` and `.../ShroudOfDeciet.cs`. Pinned's
`GuantletsOfAnger` and `ShroudOfDeciet` are untouched.

**A premise in the brief I cannot confirm:** "A fresh world is imminent" contradicts AGENTS.md rule 7 and
`docs/direction-decision.md`, as `type-identity.md` section 4 already recorded. It does not matter to this removal, which
is safe on the evidence above whichever world comes next.

---

## 6. Tests

`server/tests/Misc/P8LootTablesVerification.cs`, namespace `ShatteredLegacy.Tests`:

- `HatTypesIsPinnedsTwelveThenOrcMaskAndTribalMask`: 14 entries, pinned's 12 in order, then the two.
- `EachAddedHatConstructsThroughLoot` (x2).
- `EveryPoolThatNamesHatTypesSeesBothMasks`: finds by reflection every composite holding the `HatTypes` array (asserts
  18), prints N before/after for each, asserts `_aosHatTypes` = 17 and the chest pool = 120.
- `PinnedsEightyAreUnchangedAndOursFollowThem`: 138 entries; indices 0-79 equal pinned's 80 in order (hard-coded
  `typeof` list); the types after them are exactly the 55.
- `EachAppendedEntrySpawnsItsItemWhereServUOPutsIt` (x58): `CreateInstance` builds the type, immovable, at the entry's map
  and point; delays sane; weight within the steal cap.

`server/tests/TypeIdentity/TypeIdentityVerification.cs`: the D35 fact replaced by `D35_OursAreGoneAndPinnedsRemain` (x2).
**Gone, not unreferenced:** case-sensitive and insensitive full-name lookups and the short-name lookup all return null,
and a reflection scan of every loaded assembly finds no type by either name. Pinned's still resolve, are not ours, and
carry 1094902 / 1094914.

---

## 7. Build, red, green

All `docker/uo/build.sh --tests-only -t sl-modernuo:p8-*`: no runtime image built, nothing live touched. Logs in
the session scratchpad (`build1.log`, `build2.log`, `red.log`).

- **Build 1: builder green, both patches `Applied`, tests 189/248, 59 failed, all mine and all test bugs:**
  - 57 of 58 `EachAppendedEntry...`: "weighs 10, over the **0** stone steal cap". `Stealing.Configure` never runs in the
    test host, so `MaxWeightToSteal` is 0 there. Now asserted against Configure's default, 10 (test header). The 58th,
    `LightInTheVoid`, "passed" only because its tiledata weight reads **0** in the host; the header says so.
  - 2 `D35_OursAreGone...`: `NullReferenceException` in the assembly scan. `Core.Assembly` is null in the test host.
    Filtered.
- **Build 2 (green): 248/248.** 63 P8 facts, 2 D35 facts. The total includes P7's in-flight tests, which were in the
  tree at the same time (section 8).
- **Red run**, from a copy of the tree in the scratchpad with its own builder tag (`sl-uo-builder:p8-red`) so the breaks
  could not reach P7's concurrent builds in the shared tree. Four breaks, six facts expected red:
  1. Loot patch without `TribalMask` -> `HatTypesIsPinnedsTwelve...` ("Expected: 14") and
     `EveryPoolThatNamesHatTypes...` (TribalMask not found).
  2. First appended stealable moved above `ManStatuetteEastArtifact` (an insertion at index 79) ->
     `PinnedsEightyAreUnchanged...` (differs at pos 79) and `EachAppendedEntry...(80, ManStatuetteEastArtifact)`.
  3. `GauntletsOfAnger.cs` restored -> `D35_OursAreGone...(GauntletsOfAnger)` ("Assert.Null() Failure"); Shroud green.
  4. `CarvedMyrmydexGlyph` weight 11 -> `EachAppendedEntry...(133, CarvedMyrmydexGlyph)` ("weighs 11, over the 10").

  **Result: 242/248, exactly those six failed, each on its own break.** The real tree was never broken; it is green
  as build 2.
- **Not watched red:** `EachAddedHatConstructsThroughLoot`. Its only failure mode is a type vanishing, which is a
  compile error before it is a test failure.

---

## 8. What a reader should not trust, and what happened to the tree

- **An automated "Shard work, 2026-09-29 14:56" commit (`d8077d7`) swept up the tree mid-task**: my staged D35
  deletions, both patches, the `apply-patches.sh` lines, and **the build-1 tests with both bugs**, together with P7's
  uncommitted files. I did not rewrite it. The next commit carries the two test fixes. Between the two, `HEAD` does not
  pass its own gate.
- P7 was editing `apply-patches.sh` in the same place at the same time. My block is separate and follows theirs.
- The weight check is exact for 54 of the 55 types and trivial for `LightInTheVoid` (test header).
- The map probe reads the client files in `client-data/classic-client`, which the server is assumed to load. I did not
  read the server's own map path.
- Nothing was placed in a world. The stealables go live only on the next deploy, which is not mine to do. On the live
  world they will spawn within 15 minutes of that load.

---

## 9. Proposed rows (text only; `docs/` untouched)

**`docs/bug-list.md`, D35**, replace the closing clause:

> | **D35** | ... *(existing text)* ... | **DONE 2026-09-29 (cc-P8).** Both of ours removed after (1) the only reference, the
> D35 identity fact, was replaced; (2) 115 save type tables, control present in each, held none of the four
> spellings; (3) no alias or migration names either. `D35_OursAreGoneAndPinnedsRemain` asserts gone, watched red.
> `notes/cc-P8-loot-tables-and-d35.md` §5 |

**`notes/cc9-close.md` deviation row for `OrcMask`**, reversed: now in `Loot.HatTypes` with `TribalMask`
(`Loot-hat-types-orc-tribal-mask.patch`). Where a doc records the deviation, mark it reversed with that patch.

**A decision for Chase, gate 3** (for wherever open decisions are kept): "Treasure-chest content from ServUO: which
ServUO, the legacy `Fill` or the EJ `TreasureMapInfo` rewrite this shard's expansion would run? Pinned has neither's
lists. Options and their odds in `notes/cc-P8-loot-tables-and-d35.md` §2.4. Nothing built."

**`docs/client-test-queue.md`**, numbered at promotion as highest-in-file plus one (T-022 was highest when read):

| T-??? | ⬜ OPEN | **Stealables: ours spawn and can be stolen** | On the test shard as a GM, `[GenStealArties`, wait for the next 15-minute check, go to TerMur 1134 1204 7 (Underworld, `HalfEatenSupperArtifact`) and Trammel 6303 1664 11 (Ararat, `SternAnchorOfBmvArarat`); with a 100 Stealing player, steal one | Each item is present and immovable, sits on the floor at its point (not floating or buried), and the theft succeeds or fails like pinned's Doom stealables | cc-P8, `StealableArtifacts-servuo-entries.patch` |
| T-??? | ⬜ OPEN | **Masks in random loot** | `[add TreasureMapChest 5` a few times and open them as a GM | Orc and tribal masks turn up among the magic items (about one per chest on average), each with random properties like other hats | cc-P8, `Loot-hat-types-orc-tribal-mask.patch` |
