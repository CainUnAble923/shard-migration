# CC6 batch 7 — the eight remaining aliases (Q-055 yes), the leaf-creature row, and one leaf item

This task closed **17 spawn names, 31 entries** in three parts, each proved in the gate and the last two in a headless
run: **Part A**, the eight `[TypeAlias]` files batch 6 §9 sized (Q-055 answered yes, recorded verbatim in
`notes/codex-questions.md`), 16 entries, nothing ported; **Part B**, the leaf-creature row — ServUO's
`DragonsFlameGrandMage` on our `DragonsFlameMage` with its `DragonFlameKey`, and the seven Clan ratmen — 11 entries,
9 files; **Part C**, `TreasureLevel1h` into the `TreasureChestMod.cs` we already carry, 4 entries. `tools/spawn-orphans.txt`
went **40 → 32 → 24 → 23** by the script, one regeneration per part. Part A was built and committed on its own
(`d6344ac` / `acad1a0`) before Part B touched the tree.

Three things this note corrects or adds to the earlier batches, counted rather than described:

- **Batch 6 §9 sized `magedragonsflamemage` as "one leaf file". It is two.** The ServUO file drops a `DragonFlameKey`
  on every death, and no tree here had one (`Items/Quest/DragonFlameKey.cs`, 39 lines, `: PeerlessKey`). Batch 6 read
  the parent and the line count, not the file's `new X(` list — the recipe's first rule, skipped in a sizing note.
  Cheap here because `PeerlessKey` is ours (P9, batch 4) and `SerpentFangKey` is the same shape.
- **Batches 2 and 5 never recorded a loss they carried.** ServUO's `Items/Equipment/Talismans/TalismanSlayer.cs` lists
  `ClanRibbonPlagueRat` (batch 2), `VitaviRenowned` and `RakktaviRenowned` (batch 5) as Vermin-talisman targets; pinned's
  list stops at `Rat`/`GiantRat` with upstream's own `// , typeof( Chiikkaha )` stub. Neither note mentions talismans.
  **D-78** below covers all ten of ours now. A documentation defect of `docs/bug-list.md` §1b's kind: the grep for what
  the *stock tree* does with a type (not just what the type does) was not run.
- **ServUO's `ClanCT` names itself wrong, and the fidelity principle decides it, not the D-4 rule.** Batch 6 §2 flagged
  the disagreement (class `ClanCT`, `Name = "Clan Scratch Tinkerer"`, spawn name `ClanChitterTinkerer`). UOGuide's page
  is "Clan Chitter Tinkerer" and no "Clan Scratch Tinkerer" page exists (fetched 2026-09-21); the spawner sits with the
  Chitter clan's boss. The port carries the OSI name (**D-76**), a ServUO bug fixed, §4's kind in the bug list.

## 1. The selection, from batch 6 §9 by closure

| part | what closes it | names | entries | source |
|---|---|---|---|---|
| A | an alias on a pinned type | 8 | 16 | `DryadA` → `MLDryad`; `abbein`, `alethanian`, `aneen`, `jothan`, `mallew`, `taellia`, `vicaie` → the Heartwood seven |
| B | a leaf creature port, no subsystem | 8 | 11 | `magedragonsflamemage` (4), the seven Clan rats (1 each) |
| C | a leaf item port | 1 | 4 | `treasurelevel1h` |

## 2. Part A: the eight mappings, re-verified before a file was written

Batch 6 said three of these were corroborated only by name strings and that §2c's quest lists were never compared.
Both done now; nothing went back to the unresolved bucket.

**The Heartwood seven.** ServUO's `Mobiles/NPCs/{Abbein,Alethanian,Aneen,Jothan,Mallew,Taellia,Vicaie}.cs` are each a
`BaseVendor` with an **empty `InitSBInfo` and no quest list at all** — no `typeof` in any of the seven files. They sell
nothing and offer nothing; they are set dressing with the right name, title, race and sex. Pinned's `ElderAbbein` …
`LorekeeperAneen` (`Engines/ML Quests/Definitions/Heartwood.cs:3294-3606`) are `BaseCreature` (`IQuestGiver`) with
`AI_Vendor`, `IsInvulnerable`, `Race.Elf`, and the same `Title` ("the wise"; Aneen "the keeper of tradition"). **Sex
agrees on all seven**: ServUO's `Female = true` for Abbein, Alethanian, Taellia, Vicaie and `false` for Aneen, Jothan,
Mallew is pinned's body 0x25E / 0x25D respectively. So the "quest list comparison" is: ServUO gives none. And pinned?

**Pinned binds no quest to any of the seven either.** `MLQuestSystem`'s static constructor reads `Data/MLQuests.cfg`
(quest type, then quester types, tab-separated; `MLQuestSystem.cs:25-110`) and that is the only binding route in the
stock tree (`RegisterQuestGiver` has no other caller). Measured: the file has 265 rows, registers **99 of the 100** quest
types `Heartwood.cs` declares, and names **27 of its 48 NPC types** as questers. The 21 unbound include all seven here
plus `ElderAcob`, `Athailon`, `Bolaevin`, `Cloorne`, `Daelas`, `Mielan`, `Olaeni`, `Rebinil`, `Tillanil`, `Tyeelor`.
So on both trees the elders stand in Heartwood and give nothing; the mapping holds on everything a player sees, and the
missing quests are upstream's own gap (in the upstream report, §8). The test logs the bound count per elder and does not
assert it, so a pinned bump that binds them stays green.

**`DryadA`.** ServUO's Weald XML is at the repo root, `D:\UO\ServUO-pub57\Spawns\twistedweald.xml`, not under
`Scripts` (batch 6 cited the right file by the wrong path); it names `MLDryad` (MX=3) and `mldryad` at the `dryad2`
spawner (2203,1161), with `changeling` beside it, against pinned's [2171,1181] ×8 and [2207,1180] ×12 with `CuSidhe`,
`Changeling`, `Satyr`, `DireWolf`. `MLDryad`'s `DefaultName` is "a dryad", body 266. Pinned's `Dryad` is Haven's Anwin
Brenna. Unchanged from batch 6, re-read.

| spawn name | entries | stock type | alias string | one test fact each |
|---|---|---|---|---|
| `DryadA` / `Dryada` | 2 | `MLDryad` | `Server.Mobiles.DryadA` | both spellings resolve; a spawner at [2171,1181] Ilshenar fills with an `MLDryad` |
| `abbein` | 2 | `ElderAbbein` | `Server.Engines.MLQuests.Definitions.Abbein` | resolves; a spawner at [7048,382] Trammel fills with an `ElderAbbein` named "Elder Abbein" |
| `alethanian` | 2 | `ElderAlethanian` | `…Definitions.Alethanian` | same shape |
| `aneen` | 2 | `LorekeeperAneen` | `…Definitions.Aneen` | same, at [7053,338] |
| `jothan` | 2 | `ElderJothan` | `…Definitions.Jothan` | same |
| `mallew` | 2 | `ElderMallew` | `…Definitions.Mallew` | same |
| `taellia` | 2 | `ElderTaellia` | `…Definitions.Taellia` | same |
| `vicaie` | 2 | `ElderVicaie` | `…Definitions.Vicaie` | same |

Every file is batch 6 §3's four lines of code plus the **condition-1 comment** (what it reconciles, that the defect is
pinned's data disagreeing with pinned's assembly, that it is expected to be deleted once upstream fixes it, pointing at
`notes/upstream-spawn-misnames.md`). The spike's header was rewritten to the same shape. `TypeAliasAttribute` allows
one per class; none of the eight stock types carried one (grepped), so no CS0579.

**Condition 2** is `notes/upstream-spawn-misnames.md`: drafted, not filed, Chase's call.

## 3. Pre-flight for B and C: what the ten ServUO files needed, checked in `D:\UO\ModernUO-pinned` AND `server/customizations`

| ServUO reference | pinned / ours | what was done |
|---|---|---|
| `DragonFlameKey` (`DragonsFlameGrandMage.OnDeath`) | **absent from both trees**; `PeerlessKey` is ours (P9), `SerpentFangKey` (batch 4) is the identical shape | ported, `Items/Quest/DragonFlameKey.cs`, 0x2002, hue 42, blessed, label 1074343. On ServUO `Items/Functional/CitadelAltar.cs` consumes it; no altar here, as batch 4 recorded for the fang key |
| `DragonFlameSectBadge`, `LootPack.AosFilthyRich` | stock / stock | as written |
| `AlwaysMurderer`, `ShowFameTitle` (re-overridden on the child) | `BaseCreature.cs:558`, `Mobile.cs:1724` | as written; they repeat the parent's |
| `CanRummageCorpses`, `HideType.Spined`, `TreasureMapLevel`, `PackInstinct.Canine`, `AIType.AI_Archer` | all present (`BaseCreature.cs:873, 2261`) | as written |
| `SetWeaponAbility(WeaponAbility.ParalyzingBlow)` (`ClanSSW`) | recipe: `GetWeaponAbility` override | `=> WeaponAbility.ParalyzingBlow` |
| `Deserialize` body fixup `if (Body == 42) { Body = 0x8E; Hue = 0; }` (`ClanCA`, `ClanCT`) | a save-upgrade path for ServUO's own older saves | not ported; version-0 content never runs it (recipe) |
| `SetStr(231)`, `SetResistance(Physical, 40)`, `SetSkill(Anatomy, 0)` single-argument forms | `BaseCreature.cs:4646, 4724, 4758` | as written |
| `Bow`, `Arrow(int)` | stock | as written |
| ServUO `Abilities/SlayerGroup.cs:49-51` lists the six ratmen under **Repond** | pinned `Items/Weapons/SlayerGroup.cs`, a static `typeof` list: `Ratman`, `RatmanMage`, `RatmanArcher` and no way to register | **D-77** |
| ServUO `Items/Equipment/Talismans/TalismanSlayer.cs:50-53` lists the six ratmen (and the plague rat, the two renowned, Chiikkaha) under **Vermin**; `:131` lists `ClanSSW` under **Wolf** | pinned `Items/Talismans/TalismanSlayer.cs`: Vermin ends at `GiantRat // , typeof( Chiikkaha )`; the enum has **no `Wolf`** (nine members, `None`…`Bovine`, against ServUO's nineteen) | **D-78** |
| `Shoes(int)`, `Sandals(int)`, `BeverageBottle(BeverageType)`, `Jug(BeverageType)`, `Gold(int,int)`, `Bolt(int)` | `Items/Clothing/Shoes.cs:154, 168`, `Items/Food/Beverage.cs:41, 75` | as written |
| `BaseTreasureChestMod` | ours (CC4) | as written |

No `Set{Special,Magical}Ability`, no `SetAreaEffect`, no missing body, hue or sound. Bodies 0x8E (ratman archer), 42
(ratman), 98 (wolf) and 0x190/0x191 (the mage, via `Race.Human`) are stock.

## 4. The batch, and what each file needed

**The naming decision (Q-056), recommended and flagged, not settled.** Eight of the nine types have one name in ServUO
and another in the spawn data, and neither is OSI's. Batch 7 built **option 2: the type takes the spawn-data spelling,
no alias.** Why: the spawn data is the consumer, it is pinned, and for a type upstream does not ship it will never be
corrected, so the spelling that has to resolve is the durable one; it keeps `[TypeAlias]` to its two meanings in our
tree (a type's own earlier spelling; reconciling upstream's data with upstream's own types) and never puts one on a
type we author; and the ratmen's full-word names match how both trees already name the family's eighth member,
`ClanRibbonPlagueRat`. The cost is one odd class name, `MageDragonsFlameMage` for ServUO's `DragonsFlameGrandMage`,
and a ServUO-habituated GM's `[add ClanCA`. Every file header carries the ServUO name for grep. If Q-056 says option 1,
each file gains one `[TypeAlias]` line and its class name changes; no save exists. **This binds** the Underworld NPCs
(`ElderDugan`/`Dugan`, `FiddlingTobin`/`Tobin`, `NevilleBrightwhistle`/`Neville`, `NavreyNightEyes`/`Navrey`) and
`escortablewanderinghealer`/`EscortableHealer` when their rows come up.

| # | file (ServUO → ours) | spawn entries | ServUO lines → ours | notes |
|---|---|---|---|---|
| 1 | `Mobiles/Normal/DragonsFlameGrandMage.cs` → `MageDragonsFlameMage.cs` | Citadel 4 spawners, 13 max | 62 → 62 | `: DragonsFlameMage` (ours), batch 4 §2's rule: own attribute, own `(Serial)`, own version slot; "Black Order Grand Mage", 800 hits, fame 25000, `AosFilthyRich` ×6; key every death, badge 50% on top of the parent's 30% |
| 2 | `Items/Quest/DragonFlameKey.cs` → same | — | 39 → 22 | the forced dependency; P9's shape |
| 3 | `ClanCA.cs` → `ClanChitterAssistant.cs` | Abyss [982,491] with `RakktaviRenowned`, 15 | 97 → 61 | archer: bow, 50-70 arrows, `AI_Archer`, rummages, 8 spined hides, `Rich` |
| 4 | `ClanCT.cs` → `ClanChitterTinkerer.cs` | same spawner | 96 → 66 | as 3 with 2025-2068 hits, `Rich` ×2; **D-76** name |
| 5 | `ClanRC.cs` → `ClanRibbonCourtier.cs` | Abyss [919,502] with `VitaviRenowned`, 15 | 88 → 55 | melee, body 42 hue 2207, 2054-2100 hits, `Rich` + `Average` |
| 6 | `ClanRS.cs` → `ClanRibbonSupplicant.cs` | same spawner | 87 → 55 | body 42 hue 2952, 127 hits, cold 80-85, `Rich` ×3 |
| 7 | `ClanSH.cs` → `ClanScratchHenchrat.cs` | Abyss [949,555] with `TikitaviRenowned`, 15 | 86 → 55 | body 42, 2065 hits, `Rich` ×3 |
| 8 | `ClanSS.cs` → `ClanScratchScrounger.cs` | same spawner | 96 → 62 | archer as 3, 135 hits, treasure map 2, `Rich` ×2 |
| 9 | `ClanSSW.cs` → `ClanScratchSavageWolf.cs` | Abyss [950,555], 18 | 91 → 58 | body 98 hue 0x2C, 20% physical / 80% cold, Swords 99-100, `ParalyzingBlow`, canine pack, meat 1 |
| 10 | `Items/Containers/TreasureChestMod.cs:63` → the same file, after `TreasureLevel1` | Sea Market [4534,2349], [4535,2349] × Fel/Tram, 4 | 55 → 42 | skill 56, magic trap 1-25, gold 10-40, 5 bolts, shoes or sandals in hue 1 or 2 (`Utility.Random(1, 2)`, as written), ale, liquor or cider |

Range perception dropped (all pass 10), speeds dropped (Q-008), serialization by the generator, `this.` removed. Every
one of the ten compiled the first time; the one red compile of the batch was the test file (§6).

## 5. Deviations — note-local numbering, for `docs/fidelity-principle.md`

Batch 5 ended at D-75; D-76 was left free by the follow-up. Every "reverses when" names a patch and its reach, measured
from `D:\UO\ServUO-pub57\Scripts`, and every loss below was proved by grepping pinned for what the thing *does* before
it was numbered.

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-76** | `ClanChitterTinkerer` is named "Clan Chitter Tinkerer" with "a clan chitter tinkerer corpse"; ServUO's `ClanCT.cs` says "Clan Scratch Tinkerer" / "a clan scratch tinkerer corpse" | the OSI name, which UOGuide has and ServUO's does not; the creature sits with the Chitter clan's Rakktavi | **never wanted**: two strings. A ServUO bug fixed, `docs/bug-list.md` §4's kind (a wrong clan on a named creature, not a typo in one) |
| **D-77** | The six ratmen (`ClanChitterAssistant`, `ClanChitterTinkerer`, `ClanRibbonCourtier`, `ClanRibbonSupplicant`, `ClanScratchHenchrat`, `ClanScratchScrounger`) are not **Repond** slayer targets; ServUO's `Abilities/SlayerGroup.cs:49-51` lists them | a Repond weapon or spellbook does normal damage to them; ServUO's doubles it. `SlayerEntry.Slays` matches by `IsAssignableFrom` (`SlayerEntry.cs:111`) and they derive from `BaseCreature` directly, so no stock ratman entry catches them | **1 patch hunk**: six `typeof` lines in the `Repond` entry of pinned `Items/Weapons/SlayerGroup.cs` (a static list built in `static SlayerGroup()`, `:8`; nothing registers into it). Reach: **6 files**, all here; the wolf is not a Repond target on either emulator |
| **D-78** | The seven ratmen, plus `ClanRibbonPlagueRat` (batch 2), `VitaviRenowned` and `RakktaviRenowned` (batch 5), are not **Vermin** talisman targets (ServUO `Items/Equipment/Talismans/TalismanSlayer.cs:50-53`); `ClanScratchSavageWolf` is not a **Wolf** talisman target (`:131`) | a Vermin-slayer talisman (crafted, or the Totem of the Void family) gives no bonus against any of the ten; nothing at all for the wolf | Vermin: **1 patch hunk**, ten `typeof` lines in pinned `Items/Talismans/TalismanSlayer.cs:35-37`, where upstream's own `// , typeof( Chiikkaha )` stub already marks the spot. Reach: **10 of our types** + `Chiikkaha` (not ours). Wolf: **not a hunk** — pinned's `TalismanSlayerName` has nine members (`None`…`Bovine`) against ServUO's nineteen (`Wolf`, `Undead`, `Goblin`, `Repond`, `Elemental`, `Demon`, `Arachnid`, `Reptile`, `Fey` absent), so the wolf's group needs the enum and its table; that is the SA talisman-slayer set, its own backlog row, and the wolf is one creature of it |

D-77 and the Vermin half of D-78 are together a **new small row for `docs/patch-backlog.md`** (two hunks in two static
lists, 16 lines, reach 16 types), proposed in §8; Chase's to add. **No P6 deviation from this batch** and no D-41.

**Bugs, by kind:**

- *Ours:* none found.
- *ServUO's, copied faithfully (bug-list §3):* `ClanRibbonCourtier` and `ClanScratchHenchrat` have over 2000 hits at
  fame 1500 beside a 127-hit supplicant at the same fame; `ClanChitterTinkerer` has 2025-2068 hits at fame 6500 beside
  its 120-145-hit assistant. Every value is ServUO's and is pinned by the test. `ClanCA` carries a commented-out
  `InhumanSpeech.Ratman` line, kept out. **`ClanSS` is an `AI_Archer` holding a bow with no Archery skill set at all**
  (Anatomy, MagicResist, Tactics, Wrestling only), so the scrounger shoots at 0.0 Archery; the two Chitter archers have
  80.1-90. Found by a test assertion written for all three (build C3), pinned as 0.0 on the scrounger. The hybrid chest's shoes are hue 1 or 2 (a dye-tub grey and a near-black),
  `Utility.Random(1, 2)` where `Utility.RandomNeutralHue()` was surely meant; as written.
- *ServUO's, fixed:* D-76.
- *ModernUO's, to report:* the nine spawn misnames (`notes/upstream-spawn-misnames.md`) and, in the same document as a
  related note, `Data/MLQuests.cfg` binding 27 of `Heartwood.cs`'s 48 NPC types.

## 6. What was proved

| Gate | Result |
|---|---|
| **Build A** (Part A, `--tests-only`, the five pins deliberately left at 40) | **red as intended: Passed 99, Failed 5**, `BUILD FAILED … No image was built.` The five failures were exactly the count pins in batches 1-5 (`Expected: 40 / Actual: 32`, five times); batch 7's four Part A facts and batch 6's three were green. The gate is live and the eight aliases resolve |
| **Build B** (Part A, full, pins at 32) | green: 17 patches applied, **104 tests passed** (100 + 4), `structured customizations installed: 613` (605 + the 8 aliases), image `sl-modernuo:latest`, tagged `sl-modernuo:cc6b7-a` (3b54354e99fd). Committed as `d6344ac` |
| **Build C** (B and C in the tree, `--tests-only`, pins at 32) | **red at compile**, twice, both mine and both in the test file: C, `SerializationGeneratorAttribute` without `using ModernUO.Serialization;` (8 errors); C2, the two xUnit analyzer rules batch 4 warned about (`xUnit2029` `Assert.Empty` over a filter, `xUnit2031` `Where` before `Assert.Single`). **All ten content files compiled the first time.** |
| **Build C3** (same, compiling) | **red as intended: Passed 103, Failed 6** — the five pins (`Expected: 32 / Actual: 23`, five times) plus one of mine: `TheRatmenKeepTheirServUOShape` asserted Archery ≥ 80.1 on all three archers and `ClanSS` has no Archery skill (§5, ServUO's, now pinned as 0.0). The eight other B/C and A facts and batch 6's three (control now `genericguard`) green |
| **Build D** (probe in the tree, full, pins at 23) | green: **109 tests passed** (104 + 5), `structured customizations installed: 623` (613 + 9 + the probe), image `sl-modernuo:cc6b7-probe` (ccb1082858d0) |
| Test `CC6Batch7Verification` (9 facts) | **A**: each of the eight spawn spellings (and its upper-case form, and the alias by full name) resolves to its stock type, the attribute on that type carries exactly that one alias, `FullName` is untouched, the instance's `Name` is the stock `DefaultName`, and `Dryada` is the same key; a `Spawner` at each name's first stock location (Ilshenar [2171,1181], Trammel [7048,382] / [7053,338]) with that entry returns true with `EntryFlags.None` and holds one instance of the type at that spot, registered against the entry; the seven elders are `IQuestGiver`s with `AI_Vendor`, invulnerable, elves, the right titles, and the log shows 0 quests bound to each by `Data/MLQuests.cfg`; the control `athialon` is null and a spawner carrying it returns false with `InvalidType`. **B**: all eight construct with ServUO's name, corpse name, body, hue, fame and karma (the mage a human body), hits > 0, Medium speed (Q-008), resolve by the JSON's own spelling, and each carries its own generator attribute and its own `(Serial)` constructor; **every stock spawn entry naming one of the seventeen resolves**, 31 entries, and exactly 23 names remain (the run lists them); the grand mage is a generated subclass of our mage with its title, 800 hits, `AlwaysMurderer`, hidden fame title, `AI_Mage`, the parent's kasa, and **10 real kills through `Kill()` and a real corpse put a `DragonFlameKey` (blessed, hue 42, 0x2002, label 1074343) on all 10 corpses**; the three archers have a bow, 50-70 arrows, `AI_Archer`, rummage, 8 spined hides; the tinkerer's hits and OSI name (D-76); the scrounger's treasure map 2, 135 hits and 0.0 Archery; the three melee ratmen on body 42 with no weapon; the courtier's 2054-2100 hits and 113.5+ resist, the supplicant's 127 hits and 80-85 cold, the henchrat's 2065; the wolf's `ParalyzingBlow`, meat 1, meat diet, canine pack, 20/80 physical/cold, sound 229, Swords 99+, 65 hits. **C**: `treasurelevel1h` resolves; 20 chests each on `BaseTreasureChestMod`, item id in the three crate ids, gump 0x49, locked, immovable, skill 56, lock 46-55 / 56, magic trap 1-25, 10-40 gold, 5 bolts, shoes or sandals in hue 1-2, and exactly one of bottle/jug |
| `CC6Batch1..5CreatureVerification` | their pinned orphan count moved 40 → 32 → 23 in step; **all five went red on the old figure first, twice** (build A on 40, build C3 on 32) |
| `CC6Batch6SpawnAliasVerification` | its control moved from `magedragonsflamemage` (now a type) to `genericguard`; green |
| **Headless run 1** (`sl-modernuo:cc6b7-probe`, fresh save; the probe imports TwistedWeald, Trammel TownsPeople, Citadel, Abyss and Trammel Vendors 3 s after start, reports at 93 s) | `Loading world done (618 items, 90 mobiles)`; `Generated 14 / 48 / 15 / 22 / 95 spawners (0 failures)`; **186 spawners, 343 entries, 7 entries flagged `InvalidType`** — exactly the seven remaining orphans those five files carry (`athialon`; `SlasherOfVeils`, `StygianDragon`, `Medusa`; `bodysculptor`, `dockmaster`, `boatpainter`), counted from the list; 840 mobiles, 4,196 items. **17 of 17 live, every instance owned by its stock spawner, placed by the real map**: 5 dryads in the Weald (e.g. 2160,1170,−46, not the spawner's own tile); **the seven elders standing in Heartwood** at 7036-7058 / 343-393 with their titles, elf bodies 605/606 and random skin hues; 5 grand mages in the Citadel (182,1924,0, "Black Order Grand Mage", "of the Dragon's Flame Sect", body 401); the Abyss ratmen — 7 assistants, 2 tinkerers ("Clan Chitter Tinkerer"), 5 courtiers (hue 2207), 1 supplicant (2952), 4 henchrats, 7 scroungers, **18 savage wolves** (hue 44 = 0x2C, body 98); 2 hybrid chests at the Sea Market (4534,2349,−2, item 0xE3C). `Saving world done`, `Shutting down`; no warning but the usual three |
| **Headless run 2**, reload run 1's save | `Loading world done (4202 items, 841 mobiles)`; "14 spawners naming this batch present from save"; **0 entries flagged**; **every one of the 17 per-type lines identical to run 1, byte for byte** (diffed). Save, shutdown, clean |
| **FINAL build** (probe deleted) | green: 17 patches applied, **109 tests passed**, `structured customizations installed: 622` (613 + 9), image `sl-modernuo:latest` (7cac801aa15a), tagged `sl-modernuo:cc6b7`. Parts B and C committed as `0373f75` |
| **Headless run 3**, the final image, fresh save | `Loading world done (617 items, 90 mobiles)`, listeners on 127.0.0.1:2593, `Saving world done`, `Shutting down`; **no `[cc6b7]` line**, no warning but the usual three (`stats` already registered, no accounts, no owner account) |

Probe (`server/customizations/Probe/CC6Batch7Probe.cs`, deleted before FINAL, never committed): batch 5's shape.
`Initialize` arms a 3 s timer; on a fresh world (no spawner naming a batch entry) it makes a Developer-access
`PlayerMobile` and runs `CommandSystem.Handle` for `[GenerateSpawners` on the five files; on a reloaded world it says
how many spawners naming the batch are present. Ninety seconds later it counts spawners, entries, entries flagged
`InvalidType`, mobiles and items, then per name: the resolved type, entries, live instances (mobiles or items),
spawner-owned instances, maps, and a sample with location, hue, name, title and body. Harness in
`%LOCALAPPDATA%\Temp\cc6b7\` (`run.sh`, the loopback `conf` copied from batch 5's, the logs, `saves`, `saves-final`).

**Not verified, per the standing rule, and batched for the client spot check:** appearance of the seven elders'
outfits and hair; the wolf's 0x2C hue on body 98; the ratman bodies with the Abyss lighting; the hybrid chest's
crate graphic and its lock/trap in play; whether a Repond weapon visibly does normal damage to a ratman (D-77); and
whether the live world's Citadel, Weald, Heartwood, Abyss and Sea Market spawners are populated (Q-048 says
`shared/**` was generated, not read here, and the five files here include two `post-uoml/**` ones).

## 7. What it cost

| what | time |
|---|---|
| orientation: `AGENTS.md`, batch 6 whole, the recipe, batch 4 §2, batch 2 and 5 §6, the orphan script and list, the spike and its test | ~25 min |
| Part A re-verification: the seven ServUO NPC files, `Heartwood.cs`, `MLQuests.cfg` measured, `MLQuestSystem`, the Weald XML at its real path, UOGuide for the tinkerer | ~20 min |
| Part B/C pre-flight: the ten ServUO files, every `new X(` and member against pinned, the slayer and talisman lists in both trees | ~20 min |
| the eight alias files (generated from one template), the test's four A facts, five pins moved | ~15 min |
| build A 16:46 (tests-only, red on the pins as intended, 5 min) and build B 16:51 (full, green, 6 min) | ~11 min |
| the ten B/C files, the probe, the five B/C facts, batch 6's control retargeted | ~25 min |
| build C 16:57 and C2 16:58 (red at compile, my test file both times, ~1.5 min each), C3 17:01 (red on the pins as intended, 4 min), D 17:05 (probe image, green, 3.5 min), FINAL 17:16 (green, 2.5 min) | ~13 min |
| headless runs 1 (17:08), 2 (17:12), 3 (17:18): 3.5 + 2.5 + 2 min | ~8 min |
| this note, the two Q entries, the upstream report, progress | ~45 min |

## 8. Questions

- **Q-055**: answered yes; the answer is recorded verbatim in `notes/codex-questions.md`, both conditions met here.
- **Q-056** (non-blocking, Chase's): the naming rule for a ported type whose ServUO name and spawn entry disagree.
  Built as option 2; §4 has both sides.
- **For `docs/patch-backlog.md` (Chase adds rows; agents do not edit `docs/`):** a row for **slayer-list membership of
  ported creatures** — D-77's Repond hunk and D-78's Vermin hunk, two static lists, 16 `typeof` lines, reach 16 of our
  types today and every ratman, goblin or vermin ported later. Separately, the SA talisman-slayer groups pinned lacks
  (nine enum members and their tables) are a subsystem-sized row, of which the wolf is one creature.
- **For `docs/bug-list.md` §1b:** batches 2 and 5 did not grep the stock slayer and talisman lists for the types they
  ported; three creatures carried an unrecorded loss for two days. The check is one grep of the ServUO type name over
  `Abilities/SlayerGroup.cs` and `Items/Equipment/Talismans/TalismanSlayer.cs`, and belongs in the pre-flight.
- **For upstream, with the misnames:** the Heartwood `MLQuests.cfg` gap, §2.

## 9. What is left, honestly — the 23, re-cut by closure

| what closes it | names | entries | members | cost, measured |
|---|---|---|---|---|
| **the quest/escort engine** (S5, Q-025) | 12 | 14 | `athialon`, `Barreraak`, `Garamon`, `Gretchen`, `Jaacar`, `QuartermasterFlint`, `Xenrr`, `Vernix`, `ElderDugan`, `FiddlingTobin`, `NevilleBrightwhistle`, `escortablewanderinghealer` | unchanged from batch 6 §9; five of them are Q-056's shape (ServUO name ≠ spawn name) |
| **bosses** (Q-052) | 5 | 5 | `Medusa`, `SlasherOfVeils`, `StygianDragon`, `Niporailem`, `NavreyNightEyes` | Q-052 plus Navrey's lair (651 lines) |
| **High Seas** | 2 | 4 | `dockmaster` (236 lines), `boatpainter` (42) | a subsystem question, unchanged |
| **`Sphynx`** | 1 | 1 | `Services/Malas/Sphynx/` (572 lines) | a leaf with its own service; unchanged |
| **P6** | 1 | 1 | `IronBeetle` | unchanged |
| **nothing to map: a spawn-data finding** | 2 | 4 | `genericguard`, `bodysculptor` | in the upstream report's last section; nothing to build |

12 + 5 + 2 + 1 + 1 + 2 = 23; 14 + 5 + 4 + 1 + 1 + 4 = 29. With this batch the orphan list has **no row left that a
leaf port or an alias closes**: every remaining name is gated on a decision (Q-052, the High Seas and Sphynx
subsystems, P6) or on S5's engine. **Batch 8, if there is one, is not a CC6 batch by the old rule**; it is S5's quest
row or Q-052's answer. The cheapest thing left on the list is `Sphynx` at 572 lines, and it is one entry.
