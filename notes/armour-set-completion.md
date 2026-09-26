# Armour set completion: the five candidates, the kilts, and what was ported

Task: finish the armour sets that cannot be completed. Chase saw Virtue at "6 of 8" in game; the overseer's
filename diff of ServUO's set folders against ours found four sets short and two absent. The first job was
to check that diff, because a filename diff is evidence about names.

**Result in one paragraph.** The diff was right about four of the five files and wrong about the fifth,
and it was right for a reason nobody had written down. Virtue's two pieces are **not missing**: pinned
ModernUO ships both, as standalone armour with the set bonus folded in, so they exist and never count.
`BestialKilt` and `VirtuososKilt` are **genuinely absent** from both trees, by name and by alias, and each
is the fourth piece of its set's *gargoyle* half, so a gargoyle cannot finish either set. `VirtuousEpiphany`
is **not a set piece at all**: it is a twelve-piece suite, the Good twin of the Villainous one we already
have, and no set is short without it. DaemonBone and Ranger are stock ModernUO, exactly as guessed. Part B
has a common cause, and it took more than kilts.

---

## Part A: the five candidates, each checked in both trees

The check for each was: declared by name in pinned or ours; resolvable through a `[TypeAlias]` string in
either (the batch 5 trap, `AssemblyHandler.cs:251-263`); referenced by anything that hands it to a player;
and, where it exists, whether it behaves as a member of the set.

| Candidate | Pinned ModernUO | Ours | Verdict |
|---|---|---|---|
| `SpiritualityHelm` | **declared**, `UOContent/Items/Armor/Sets/SpiritualityHelm.cs:7`, `: BaseArmor`, no `SetID` | no | **exists, but not in the set.** See A.1 |
| `ValorGauntlets` | **declared**, `UOContent/Items/Armor/Sets/ValorGauntlets.cs:7`, `: BaseArmor`, no `SetID` | no | **exists, but not in the set.** See A.1 |
| `BestialKilt` | no declaration, no alias | no | **absent.** Ported |
| `VirtuososKilt` | no declaration, no alias | no | **absent.** Ported |
| `VirtuousEpiphany.cs` | none of its 12 types | none of its 12 types | **absent, and not a set piece.** Not ported here; A.4 |

### A.1 Virtue: real, and not the shape the diff implied

The diff read "two files missing". The pieces are present. Pinned's folder `UOContent/Items/Armor/Sets/`
holds exactly two files, these two, and `HeritageTokenGump.cs:22-23` offers both as 8th-anniversary rewards.
What pinned does not have is a set system, so it modelled each piece standalone with the set bonus baked in:

| | ServUO (set piece) | pinned (standalone) |
|---|---|---|
| `SpiritualityHelm` resists | 8 / 8 / 7 / 9 / 8, + `SetPhysicalBonus` etc. 5 each with the full set | **13 / 13 / 12 / 14 / 13** always |
| `ValorGauntlets` resists | 6 / 6 / 8 / 9 / 6, + 5 each with the full set | **11 / 11 / 13 / 14 / 10** always |
| self repair | `SetSelfRepair = 5`, full set only | `ArmorAttributes.SelfRepair = 5`, always |
| `SetID` / `Pieces` | `Virtue` / 8 | none |

Every pinned resist is ServUO's plus 5 except Valor's energy (6 + 5 = 11, pinned 10), which is either a
typo upstream or a deliberate round; it does not matter once the ServUO values are used. Our six Virtue
pieces (CC9 batch 4) are ServUO ports on `BaseSetArmor` declaring `Pieces => 8`. So with all eight worn,
`SetHelper.FullSetEquipped` (`SetItem.cs:327`) counts six `ISetItem`s with `SetID == Virtue` and can never
reach eight. **Chase's report is exactly right and the set cannot complete.** The fix is not a port; it is
making pinned's two types members of the set (A.1.1).

**Reachability, stated because the brief's test is "does a player get the piece".** No player gets any
Virtue piece on this shard today. ServUO's six come from `VirtueArtifactsSystem` and `CleanUpBritanniaData`
(and `HumilityCloak` from `HumilityShrinePersistence`); none of those is in pinned or ours, so our six are
`[add`-only. Pinned's two come only from a `HeritageToken`, and nothing in pinned creates one. Chase's "6 of 8"
was a GM-built character. The set still matters: it is the one that will be wrong the day any of those
droppers lands.

#### A.1.1 How to make the stock pieces count: four routes, one taken

The repo rule is that a patch to an upstream file has its alternatives argued before it is written. They
were, in this order:

1. **Partial-class the stock types onto `ISetItem`** (the batch 3 marker-interface trick; both pinned
   types are `partial`). **Rejected.** The stock files already declare every resist override with the bonus
   folded in and set `ArmorAttributes.SelfRepair = 5` in the constructor. A partial cannot redeclare an
   override, so the full set would pay the +5 twice, and self repair would stay always-on. Carrying the set
   state would also mean writing `BaseSetArmor`'s eleven serialized fields a second time, which the brief
   forbids ("do not build a second path") and which is the copied-logic shape `docs/subsystem-policy.md`
   ranks below a patch.
2. **Lower our six pieces to `Pieces => 6`.** **Rejected.** It invents a six-piece Virtue set no wiki
   describes; the fidelity principle exists to prevent exactly that.
3. **A full-file replacement** (the `Mining.cs` route in `apply-patches.sh`). **Rejected in favour of 4.**
   It would work, but a replacement silently overrides any upstream change to the file, and
   `docs/subsystem-policy.md` is explicit: a failing patch beats copied upstream logic. With `--fuzz=0` a
   bump that touches either file stops the build and names it.
4. **A `.patch` re-parenting both onto `BaseSetArmor` with ServUO's values.** **Taken.**
   `server/patches/Virtue-stock-pieces-set-carrier.patch`, two hunks, one per file.

Route 4 inserts an ancestor, which changes the save chain and is **free only while no instance exists in
any save** (`docs/gap-register.md`, "The re-parenting window closes on the next deploy"). Measured, not
assumed, the CC9 batch 4 way, at 2026-09-26 18:03 CDT (`savecheck.py`, read-only):

| Artefact | How | Result |
|---|---|---|
| Live `server/lib/uo/modernuo/Saves/SerializedTypes.db` (written 18:00 today) | parsed as a type table | 1,461 names, `Server.Items.Dagger` present; **no** `SpiritualityHelm`, `ValorGauntlets`, `HeritageToken`, or any Virtue/Bestial/Virtuoso type |
| `Saves-test` | same | 188 names, control present, none |
| `Backups/Automatic`, every snapshot (2026-09-16 to 2026-09-26 23:00) | same, each | control present in all, none in any |
| `Archives/Daily` (2026-09-24, -25), `Hourly` (2026-09-26-21, -22), `Monthly` (2026-06, 2026-07) | stream-decompressed, every `SerializedTypes.db` member | control present in all, none in any |
| Containers | `docker inspect` | live `sl-modernuo` runs image **`uo-modernuo`** (the old one; its type table has no CC9 type at all, not even `GargishDagger`); `sl-modernuo-test` runs `sl-modernuo:latest` on `Saves-test` |

**120 type tables, every one positive-controlled, zero instances.** The window is open for these two types.
It closes the first time a player on the live world receives one after a deploy that predates this patch,
which is the same deadline `docs/gap-register.md` already carries for the CC9 re-parents.

**What changes for a player, which is the point of doing it:** the heritage-token helm and gauntlets become
ServUO's pieces. Worn alone they are 5 lower per resist than pinned's and self-repair only with the full set;
worn with the other seven the total is identical to pinned's figure and the set finally completes. That is
removing a pinned deviation from OSI, not adding one, so it takes no D-number. It is player-visible, and it is
recorded here so nobody reads the lower solo numbers as a regression.

### A.2 `BestialKilt`: absent, and the gargoyle half cannot finish

ServUO's Bestial set is two four-piece sets under one `SetID`, each piece declaring `Pieces => 4`: the human
`BestialGloves/Gorget/Helm/Legs` and the gargoyle `BestialArms/Earrings/Necklace/Kilt`. We had seven of the
eight, so the human half completes and the **gargoyle half stops at three of four**. No declaration of
`BestialKilt` in pinned (`class BestialKilt`: 0 hits in 3,991 files), none in ours, and no `[TypeAlias]`
string naming it in either (parsed, not grepped: `aliases.py`). Genuinely missing.

### A.3 `VirtuososKilt`: absent, same shape

Human `VirtuososCap/Collar/KidGloves/Tunic`, gargoyle `VirtuososArmbands/Earpieces/Necklace/Kilt`, all
`Pieces => 4`. Same three checks, same zero. The gargoyle half stopped at three of four.

Both kilts reach a ServUO player through `CleanUpBritanniaRewards.cs:117` and `:126`, as do the rest of both
sets; that system is not ported, so all sixteen pieces are `[add`-only here. Porting the kilt is still right:
it is the piece that makes the set finishable on the day the rewards arrive.

### A.4 `VirtuousEpiphany.cs`: not a piece, and the brief's figure is batch 4's, already corrected

Opened, not sized. Twelve classes: `Helm/Gorget/Breastplate/Arms/Gauntlets/LegsOfVirtuousEpiphany` on stock
plate, and `Kilt/Earrings/GargishBreastplate/GargishArms/Necklace/GargishLegsOfVirtuousEpiphany` on the
gargish bases. **None declares a `SetID` or `Pieces`.** They implement `IEpiphanyArmor` with
`Alignment.Good`, and `EpiphanyHelper` groups by alignment and surge type, so this is the Good twin of the
`VillainousEpiphany.cs` we ported in CC9 batch 5 and nothing on the `SetItem` system is short for want of it.
Our `EpiphanyHelper` already carries `Alignment.Good` and the karma-positive branch of `GetBonus`, inert with
the rest of the mechanic.

**The brief's "Niporailem's 14 unique pieces are the Villainous set and we are 2 items short" is CC9 batch
4's figure, and CC6 batch 8 §9 already corrected it:** `Niporailem.cs:13-20` lists **24** unique pieces, the
12 Villainous (ours) and the 12 Virtuous (absent), and the sword batch 4 thought missing is ours. Counted
again here from the file: 24. `Niporailem` is the only thing in ServUO that references either suite.

So Virtuous Epiphany is content that only exists as Niporailem's loot, and Niporailem is still an orphan.
Porting the suite without the boss ships twelve `[add`-only items; porting the boss without the suite ships a
loot table with twelve holes. **They belong in one change, and batch 8 §9 already scheduled it that way**
("batch 9's first row: ~220 lines + the Virtuous set + one treasure item"). Not ported here, and nothing
about that is broken today: the Villainous half is complete on its own, and nobody can collect part of a
suite that does not exist.

### A.5 DaemonBone and Ranger: the guess was right

All ten types are declared in pinned: `Items/Armor/DaemonBone/Daemon{Arms,Chest,Gloves,Legs}.cs`,
`Items/Armor/Helmets/DaemonHelm.cs`, `Items/Armor/Ranger/Ranger{Arms,Chest,Gloves,Gorget,Legs}.cs`. ServUO
files them under `Sets/` but **none of the ten carries a set member** (the carrier regex over all ten
files: zero hits). They are plain armour. Resists, strength requirement and armour base compared on four
of the ten (`DaemonArms`, `DaemonChest`, `RangerChest`, `RangerGorget`): identical. S3's filter excluded
them correctly and nothing is half-finished. Nothing ported, nothing to ask Chase.

---

## Part B: the kilts had a common cause, and it is the instrument

Four kilt incidents in a tree where kilts are about one per cent of the items. **One cause, two blind
spots of the same index.** Layer was not it (`Layer.Gloves` is the gargoyle kilt slot on both emulators,
and nothing in S3, S9 or CC9 keys on layer), and no name pattern was involved. The index S3 built and S9
rebuilt knows **type declarations, one primary type per file, and nothing else**. Two things in pinned
ModernUO do not look like that, and ServUO's gargoyle kilts sit in both.

### B.1 Blind spot one: the index never read `[TypeAlias]`

**The proof is in S9's own appendix.** `notes/s9-backlog-remeasure.md` lists

    Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialKilt.cs    <- upstream: GargishClothKilt
    Items/Artifacts/Equipment/Armor/Sets/Virtuosos/VirtuososKilt.cs  <- upstream: GargishClothKilt
    Items/Artifacts/Equipment/Armor/SummonersKilt.cs                 <- upstream: GargishClothKilt
    Items/Artifacts/Equipment/Armor/MantleOfTheFallen.cs             <- upstream: GargishClothChest

A name is only reported as a blocker when "neither pinned ModernUO nor `server/customizations` contains it
anywhere" (S9 §2). `GargishClothKilt` is in pinned, as a string inside
`[TypeAlias("Server.Items.GargishClothKilt", ...)]` on `GargishClothKiltType1`, and S9's string-literal
stripping removed it before indexing. So it looked missing, its owning file (`OuterLegs.cs`) had a primary
type pinned declares, and S9 bucketed the kilts as **"needs an upstream member, a carrier, or reading"**: the
44-file bucket CC9 batch 4 §14.9 records as "upstream/carrier 44 untouched". The label was wrong twice over:
`GargishClothKilt` is a type, not a member, and it already resolves. **What the two kilts actually needed
was the SummonersKilt treatment, which is ordinary content work.** Nobody read them because the bucket said
patch.

The same blindness produced batch 5's third incident: CC9 §2b / S9 §7 listed `GargishClothKilt` as "an
extract still to do", which batch 5 found was an alias (`docs/bug-list.md` §1b already carries that row).

**How big the blind spot is**, measured (`aliases.py`): pinned declares **126** names only as alias strings.
**45** of them are ServUO type names. 30 of the 45 are gargoyle armour and clothing (the `Gargish{Cloth,
Leather,Stone}{Arms,Chest,Kilt,Legs}` family and its female variants), which is why gargoyle gear keeps
producing these; the rest are spinning wheels, `Pizza`, `SerpentStoneStaff`, `Sewerrat`, `ToxicElemental` and
friends. Two consequences, both counted:

- **26 ServUO files whose primary type is alias-only** survive the step-1 filter as candidates although
  porting any of them would put a second type under one name. CC9 caught these by reading (§6 "already in
  ModernUO") and batch 5 by reading; the instrument never did.
- **19 ServUO classes derive directly from an alias-only type.** 8 are ours (`CastOffZombieSkin`,
  `GargishCuffsOfTheArchmage`, `MantleOfTheFallen`, `BestialArms`, `SpinedBloodwormBracers`, `SummonersKilt`,
  `GiantSteps`, `PetrifiedSnake`). **After this task, 2 more** (the kilts). The other 9: four
  `FemaleGargishCloth*Armor` in `GargishClothArmor.cs` (covered by pinned's `Type2` items, which is the
  alias design working), and five that are real content outside this task's row: `FishermansArms` and
  **`FishermansKilt`** (High Seas, `FishermansSet.cs`), `GargishStoneChestBearingTheCrestOfBlackthorn`
  (CC4), `GargishBracersofAlchemicalDevastation` (Exodus), `VvVGargishStoneChest`.

### B.2 Blind spot two: one primary type per file

S9 §7 already states that the step-1 filter discards a file when pinned declares its primary type, taking the
file's other types with it. What it measured was **the secondary types some candidate references**: "149
blocked-file references ... resolve to 28 such types". That method cannot see a secondary type **nobody
references**, and a leaf item nobody references is precisely what a gargoyle twin or a craftable garment is.
Measured directly instead (`secondary.py`): of the **3,133** files the filter discards (S9 reproduced 3,134;
the one-file difference is my comment stripping, not investigated further), **234 hold 482 types that neither
pinned nor ours declares or aliases**, 170 of them in 81 files under `Items/`.

**482 is an upper bound, not a backlog.** It contains helper types (`UnBlessEntry`, `SetFlag`, context menu
entries), interfaces AGENTS.md already maps to equivalents (`ITool`, `IFlipable`, `ItemQuality`), hair and
beard types ModernUO models differently, and gumps. It has not been resolved type by type and must not be
quoted as content. The file list is in the appendix so the next measurement can disagree precisely.

**What it took that is kilt-shaped or set-shaped, read one by one:**

| Hidden type | Where | What it is |
|---|---|---|
| **`GargishKiltOfMining`** | `GlovesOfMining.cs`, primary `LeatherGlovesOfMining` (pinned) | the gargoyle twin of the Gloves of Mining. **Kilt number five**, found by this task |
| **`GuildedKilt`, `CheckeredKilt`, `FancyKilt`** | `OuterLegs.cs`, primary `BaseOuterLegs` (pinned) | three human kilts, `0x781B-D`. Tailoring recipes (`DefTailoring.cs:376-383`, recipes 562-564); `FancyKilt` is also worn by an NPC in `APleaFromMinocQuest.cs:317`. Absent from both trees |
| `MaleGargishClothKilt`, `FemaleGargishClothKilt` | `OuterLegs.cs` | vendor clothing (`BaseVendor.cs:859`); pinned's `GargishClothKiltType1/2` cover the graphics. Equivalent, not lost |
| `GargishCrimsonCincture`, `GargishTangle1`, `GargishLieutenantOfTheBritannianRoyalGuard`, `GargishBrightsightLenses`, `GargishFoldedSteelGlasses` | the human artifact's own file, whose primary pinned ships | gargoyle twins of five stock artifacts |
| `GargishClothWingArmor`, `GargishRobe`, `GargishFancyRobe`, `GargishSash`, `GargoyleHalfApron`, `GargishApron`, `GargishEpaulette` | `Cloaks.cs`, `MiddleTorso.cs`, `Waist.cs`, `OuterTorso.cs` | gargoyle clothing bases with **no** pinned equivalent. **26** ServUO classes absent from both trees descend from them (`secondary.py desc`), 18 of them Blackthorn/CC4, plus `GargishShadowCloakOfRejuvenation`, `OzymandiasObiGargoyle`, `GargishRangersGuildSash`, `WingArmorOfLight`, `VvVGargishEpaulette` |
| `ZooMember*`, `LibraryFriend*`, `OdricsRobe`, `BaronLenshiresCloak`, `JesterShoes`, `ThreeTieredCake`, `Plum`, `StatuePegasus*`, `TerMurStyleChair/Table`, `GargishChest`, ... | multi-type files under `Items/` | collection rewards, food, decorations; appendix |

**So the answer to "what else it took": every gargoyle twin that ServUO declares inside the human
artifact's file, and every gargoyle clothing base pinned did not merge into an alias.** That is where the
kilts came from, and it is why they clustered: ModernUO's alias-merge and ServUO's twin-in-one-file habit
both concentrate on gargoyle wearables, and the kilt is the gargoyle wearable that exists in the most
parallel forms (cloth clothing, cloth armour, leather, stone, plate, female of each, and the artifact twins).

### B.3 The fourth incident: not explained, and not claimed

"The gargoyle leggings were missing the kilt section" is recorded only as a phrase in
`docs/client-test-sheet-cc6.md:6` and `:13`, with no item name. Checked what can be checked: our
`GargishPlateLegs` (`0x30E`) and `GargishPlateKilt` (`0x30C`) match ServUO's graphics exactly, and on both
emulators gargoyle legs and gargoyle kilt are **separate items on separate layers** (legs on the leg layer,
kilt on `Layer.Gloves`). A gargoyle wearing only leggings shows only the leggings, and that is correct. **My
hypothesis is that this was the design, not a defect**, but it rests on reading source, and "a cause deduced
from reading source is a hypothesis" (AGENTS.md). It needs Chase to say which item he wore. Q-061.

### B.4 What to change in the instrument, shaped for `docs/bug-list.md`

Proposed as **D20** (see "Numbering" below for why not D19):

| # | Defect | What proved it | Kind | Fix |
|---|---|---|---|---|
| D20 | **The S3/S9 content index cannot see `[TypeAlias]` names or unreferenced secondary types.** It strips string literals before indexing (so alias names vanish) and resolves one primary type per file (so the rest of a filtered file vanishes unless a candidate references it) | S9's appendix prints `upstream: GargishClothKilt` for three kilts; 45 alias-only names, 26 alias-primary files, 19 alias-derived classes (`aliases.py`); 482 unreferenced secondary types in 234 discarded files (`secondary.py`) | ours | index alias strings as declarations of the aliased type; report every secondary type of a discarded file, not only referenced ones. Both scripts are in this task's scratch and ~80 lines together |

---

## Part C: what was ported, and what was not

| What | How | Why |
|---|---|---|
| `BestialKilt` | new, `Sets/Bestial/BestialKilt.cs`, `: BaseSetClothing` | A.2 |
| `VirtuososKilt` | new, `Sets/Virtuosos/VirtuososKilt.cs`, `: BaseSetClothing` | A.3 |
| `SpiritualityHelm`, `ValorGauntlets` | `server/patches/Virtue-stock-pieces-set-carrier.patch`, onto `BaseSetArmor` with ServUO values | A.1.1 |
| `VirtuousEpiphany` (12 types) | **not ported** | A.4: belongs with `Niporailem` |
| DaemonBone, Ranger | **not ported** | A.5: stock |
| B.2's hidden kilts and twins | **not ported** | out of scope; they are Part B's answer, not this task's content. Q-062 |

### C.1 The two kilts

Both are the `SummonersKilt` shape (CC6 batch 5), because their ServUO parent is the same `GargishClothKilt`
that pinned registers as an alias of its stock armour kilt: **straight onto `BaseSetClothing`** (S10), ServUO's
parent members inlined (`0x408`, `Layer.Gloves`, gargoyles only), never a ported clothing base. Checked against
the carrier-parent rule: `GargishClothKilt`'s ServUO descendants are the three kilts and nothing else, and the
carrier regex hits all three (`SetID`, `Pieces`, and `SetHue` on the Virtuoso). Every `new X(` in both files is
`BaseSetClothing` or pinned. Neither name collides in `tools/modernuo-stems.txt` or by alias.

- **`BestialKilt`**: ServUO's resists (24/10/9/10/9), hits 125, hue 2010, weight 5 (ServUO's constructor
  overrides the stock kilt's 2.0), label 1151546, `BestialSetHelper.OnAdded/OnRemoved` as its seven siblings
  call them. ServUO resets the hue to 2010 in `Deserialize`; all seven ported siblings carry that reset in
  `OnRemoved` instead (CC9 batch 4's translation), and this one matches them rather than being the one piece
  that behaves differently. The two are indistinguishable while D-14 keeps the berserk hue from ever being
  applied. **When D-14 reverses, that translation stops being invisible**: a piece worn through a restart
  mid-rage keeps the rage hue until it is taken off. It belongs on the set-mechanic hooks row, for all eight
  pieces at once, and is written here so the hooks task finds it.
- **`VirtuososKilt`**: 7/8/21/8/8, hits 125, hue and set hue 1374, weight 5, label 1151559, `BardMasteryBonus`
  true (the carrier's default already answers true for `SetItem.Virtuoso`; stated explicitly as
  `VirtuososCap` does).

Neither carries absorption, a slayer, or any set hook beyond the ones its siblings already have, so the brief's
D-14/D-15/D-24/D-26/D-27/D-28 treatment has nothing new to apply to. The Bestial kilt's tooltip does carry the
"Berserk 5 (total)" line that D-14 leaves without a mechanic, exactly as its seven siblings do.

### C.2 Deviations

| # | Deviation | Player notices | Visibility | Reverses when |
|---|---|---|---|---|
| **D-91** | **Gargish cloth *clothing* artifacts do not swap to the female graphic.** ServUO's clothing bases (`GargishClothArms`, `GargishClothChest`, `GargishClothKilt`, `GargishClothLegs`: `Arms.cs`, `Shirts.cs`, `OuterLegs.cs`, `Pants.cs`) set `ItemID` to the female art in `OnAdded` when a female gargoyle equips them. The five ports that sit on a carrier instead do not: `SpinedBloodwormBracers` (CC9), `MantleOfTheFallen`, `SummonersKilt` (CC6 batch 5, recorded there in §5 without a number), and now `BestialKilt`, `VirtuososKilt` | a female gargoyle wearing one sees the male art (`0x408` kilt rather than `0x407`) | `visible`, cosmetic | an `OnAdded(IEntity)` override on `Mobile.Female` in each of the five, ~6 lines each and no patch; plus Chase's decision whether gargish gear should swap when pinned's own stock gargish gear (`Type1`/`Type2`, separate items) does not. ServUO reach: the four clothing bases have exactly these 5 descendants, all now ported |

D-1 (`IsArtifact`, `BestialKilt` only) and D-2 (`CanBeWornByGargoyles`, both) gain a file each. The Virtue
patch removes a pinned deviation rather than adding one (A.1.1). Nothing in this task needed a slayer,
absorption or set-hook D-number.

### C.3 The property-list gap: closed, not deferred

The brief said close it if small. It was about forty lines, and the premise that made it look large was wrong.
`notes/new-haven-quest-picker.md` §6 says asserting a property list "means implementing `IPropertyList` in the
test". It does not: pinned's own `ObjectPropertyList` (`Server/PropertyList/ObjectPropertyList.cs`) is a plain
class that needs no network, map or client, builds the 0xD6 packet into a public `Buffer`, and lays the entries
out flat after a 15-byte header as big-endian cliloc, big-endian byte length, UTF-16LE argument, ending at a
zero cliloc. `server/tests/Route/PropertyListReader.cs` builds the real list through the real `GetProperties`
and decodes it; it re-implements nothing on the path it checks. Its first read, from the red run below:

    helm alone: 1075237 | 1038021 | 1072789:6 | 1060448:8 | 1060447:8 | 1060445:7 | 1060449:9 | 1060446:8 | 1061170:25 | 1060639:255	255

That is the helm's label, blessed, weight 6, the five resists, strength 25 and durability 255/255 in the order
the client shows them. Arguments come back exactly as sent: tab-separated where a cliloc takes several, `#n` for
a localized argument. **Proved able to fail**: the red run's `TheVirtueTooltipSaysEightPiecesAndThenFullSet` went
red at "Part of an Armor Set (8 pieces)", which is the tooltip line Chase would have seen missing. Every later
test that needs a tooltip can use it, the New Haven board's five-line ceiling (B.7 on the CC6 sheet) included.

It asserts **what the server sends**, not what the client draws: truncation, wrapping and cliloc text are still
client checks.

### C.4 What was verified, and how

| Claim | Evidence |
|---|---|
| The patch applies at `--fuzz=0` | dry run against copies of the pinned files; the builder stage log, `[patches] Applied: Virtue-stock-pieces-set-carrier.patch` |
| The new test is a gate | **red run**, `sl-modernuo:setcomplete-red`, `--tests-only`, with two deliberate tampers that compile: the patch's helm `SetID` set to `None`, and `BestialKilt.SetID` set to `None`. **146 tests, 141 passed, 5 failed, the five new facts**, each at the assertion the tamper breaks: `SetID` expected `Virtue` got `None` (line 52); `FullSetEquipped` false with all eight worn (131, output `full=False helm.SetEquipped=False`); the tooltip missing 1072376 "8" (179); `SetID` expected `Bestial` (232); the kilt not completing the gargoyle half (280). Build stopped, no image. Tampers reverted; the patch byte-compared against its backup |
| Green | `docker/uo/build.sh -t sl-modernuo:setcomplete`, all three stages: patch applied, **146 tests, 146 passed**, runtime image `sha256:a63b135a…` built 2026-09-26 18:17. `sl-modernuo:latest` untouched (still `9e027935…`, 16:37). No flake: the 141 facts not touched by the tampers passed in both runs, and the gate is deterministic, so a red was always going to mean something |

**One count fixed on the way.** `tools/progress.py` reported 147 tests when the gate ran 146: it counted the
substring `[Fact]`, and `AthenaeumIsleQuestVerification.cs:7` has one in a comment. It now counts attribute lines
(`[Fact]` or `[Theory]` at the start of a line) and reports 146. The earlier figures it published were one high
since that comment landed.

### C.5 Not verified, and what a reader should not trust

- **No client has seen any of this.** Kilt art on a gargoyle, the female-art loss (D-91), the Virtue helm's
  tooltip and the full-set hue are all headless. Client-backlog lines are in C.6.
- **Part B's 482 is an upper bound** and has not been resolved type by type. The kilt- and twin-shaped rows
  were read one by one; the rest were not.
- **`secondary.py` finds 3,133 filtered files where S9 found 3,134.** Not investigated; the index is mine and
  differs in comment handling. The alias and kilt findings do not depend on that one file.
- **The fourth kilt incident is unexplained** (B.3, Q-061).
- **The pinned Valor energy resist (10 rather than 6 + 5)** is noted, not explained. It does not affect the
  result because the patch uses ServUO's value.
- **Reachability** is "nothing in pinned or ours hands these out", checked by grepping both trees for each
  type's references. ServUO's droppers were read; ours were not built.

### C.6 For the client backlog

On a **gargoyle**: `[add BestialKilt`, `[add VirtuososKilt`: kilt art in the glove slot, and again on a female
gargoyle (expect the male art; D-91). Wear `BestialArms`, `BestialEarrings`, `BestialNecklace`, `BestialKilt`:
"Full Armor Set Present" on all four. On a **human**: all eight Virtue pieces
(`CompassionArms HonestyGorget HonorLegs HumilityCloak JusticeBreastplate SacrificeSollerets SpiritualityHelm
ValorGauntlets`): the helm's tooltip reads "Part of an Armor Set (8 pieces)" before and "Full Armor Set
Present" after, which is Chase's original report closed. The headless test proves the server sends both.

---

## Numbering

- **D-91** taken. `grep -rhoE "\b[DQ]-[0-9]+\b" notes docs | sort -u` gave D-90 as the highest before this task.
- **Q-061, Q-062** taken; Q-060 was the highest.
- **`docs/bug-list.md` D20** proposed (B.4), not written there (`docs/` is not mine). **The brief and the file
  disagree:** the file's header says "the next free number here is **D19**" and holds no D19 row anywhere, while
  the latest commit, `b7f1c67`, is titled "docs: D19, the board's client pass ..." and changes only
  `docs/client-test-sheet-cc6.md`. So D19 appears to be claimed in intent and not yet written. I used D20 so the
  two cannot collide; whoever writes D19 should also move the header to D21.

## Reproducing this

- Part A: `grep -rE "class (SpiritualityHelm|ValorGauntlets|BestialKilt|VirtuososKilt)\b"` over pinned and
  `server/customizations`, then `python tools/index_blindspots/aliases.py` for the alias check.
- Part B: `python tools/index_blindspots/aliases.py`; `python tools/index_blindspots/secondary.py garg|items|desc`.
- The save check: `python tools/save_instance_check.py SpiritualityHelm ValorGauntlets BestialKilt VirtuososKilt`.

## Appendix: Part B file lists

**Alias-primary ServUO files (26):** `Items/Addons/{Elven,}Spinningwheel{East,South}Addon.cs` (4),
`Items/Consumables/TelekinisisScroll.cs`, `Items/Equipment/Armor/{,Female}Gargish{Leather,Stone}{Arms,Chest,Kilt,Legs}.cs`
(16), `Items/Equipment/Armor/GargishClothArmor.cs`, `Items/Equipment/Clothing/Arms.cs`,
`Items/Equipment/Weapons/SerpentStoneStaff.cs`, `Mobiles/Normal/SewerRat.cs`, `Mobiles/Normal/ToxicElemental.cs`.

**Hidden secondary types under `Items/` (81 files, 170 types):** the output of
`python tools/index_blindspots/secondary.py items`, reproduced here as run on 2026-09-26.

```
Items\Addons\AddonComponent.cs | primary AddonComponent | InstrumentedAddonComponent
Items\Addons\ArcaneBookshelfEastAddon.cs | primary ArcaneBookshelfEastAddon | ArcaneBookShelfAddonEast, ArcaneBookShelfDeedEast
Items\Addons\ArcaneBookshelfSouthAddon.cs | primary ArcaneBookshelfSouthAddon | ArcaneBookShelfAddonSouth, ArcaneBookShelfDeedSouth
Items\Addons\DawnsMusicBox\DawnsMusicBox.cs | primary DawnsMusicBox | StopMusic
Items\Addons\DawnsMusicBox\RewardVersion\DawnsMusicBox.cs | primary DawnsMusicBox | PlayingTimer, MusicGump
Items\Addons\ElvenDresserEastAddon.cs | primary ElvenDresserEastAddon | ElvenDresserAddonEast, ElvenDresserDeedEast
Items\Addons\ElvenDresserSouthAddon.cs | primary ElvenDresserSouthAddon | ElvenDresserAddonSouth, ElvenDresserDeedSouth
Items\Addons\HauntedMirror.cs | primary HaunterMirrorComponent | HauntedMirrorDeed
Items\Addons\MiniHouses.cs | primary MiniHouseType | MiniHouseAddonComponent
Items\Addons\ParrotPerchAddon.cs | primary ParrotPerchAddon | ParrotPerchAddonDeed
Items\Addons\SHTeleporter.cs | primary SHTeleporter | SHTeleporterCreator
Items\Addons\SacrificialAltar.cs | primary SacrificialAltarAddon | AppraiseforCleanup
Items\Artifacts\Decorative\DoomDecorationArtifacts.cs | primary BackpackArtifact | HangingPlatemailArms, HangingPlatemailLeggings, HangingPlatemailTunic, ArcaneTable, ArtifactBookshelf, IncenseBurner, BambooStoolArtifact
Items\Artifacts\Equipment\Armor\GlovesOfMining.cs | primary LeatherGlovesOfMining | GargishKiltOfMining
Items\Artifacts\Equipment\Clothing\CrimsonCincture.cs | primary CrimsonCincture | GargishCrimsonCincture
Items\Artifacts\Equipment\Clothing\LieutenantOfTheBritannianRoyalGuard.cs | primary LieutenantOfTheBritannianRoyalGuard | GargishLieutenantOfTheBritannianRoyalGuard
Items\Artifacts\Equipment\Glasses\BrightsightLenses.cs | primary BrightsightLenses | GargishBrightsightLenses
Items\Artifacts\Equipment\Glasses\FoldedSteelGlasses.cs | primary FoldedSteelGlasses | GargishFoldedSteelGlasses
Items\Books\BaseBook.cs | primary BaseBook | SaveFlags
Items\Consumables\BankCheck.cs | primary BankCheck | BankCheckExtensions
Items\Consumables\Beverage.cs | primary BeverageType | HotCocoaMug, BasketOfGreenTeaMug, CoffeeMug
Items\Consumables\Bowls.cs | primary EmptyWoodenBowl | BowlOfRotwormStew, BowlOfBlackrockStew
Items\Consumables\Chocolatiering.cs | primary CocoaLiquor | SweetCocoaButter
Items\Consumables\CommodityDeed.cs | primary CommodityDeed | CommodityDeedExtensions
Items\Consumables\CookableFood.cs | primary CookableFood | RawRotwormMeat
Items\Consumables\Firebomb.cs | primary Firebomb | FirebombField
Items\Consumables\Food.cs | primary Food | ThreeTieredCake, Hamburger, HotDog, CookableSausage, PulledPorkPlatter, PulledPorkSandwich
Items\Consumables\Fruits.cs | primary FruitBasket | Plum
Items\Consumables\HairDye.cs | primary HairDye | HairDyeEntry
Items\Consumables\OrangePetals.cs | primary OrangePetals | OrangePetalsContext
Items\Consumables\PromotionalToken.cs | primary PromotionalToken | IPromotionalToken
Items\Consumables\RecipeScroll.cs | primary RecipeScroll | DoomRecipeScroll
Items\Consumables\SoulStone.cs | primary SoulStone | VioletSoulstone
Items\Consumables\SpecialBeardDye.cs | primary SpecialBeardDye | SpecialBeardDyeEntry
Items\Containers\BaseTreasureChest.cs | primary BaseTreasureChest | TreasureResetTimer
Items\Containers\Container.cs | primary BaseContainer | GargishChest, AcademicBookCase, EnchantedPicnicBasket
Items\Decorative\Chairs.cs | primary FancyWoodenChairCushion | TerMurStyleChair
Items\Decorative\GlassItems.cs | primary SmallFlask | EmptyVenomVial, VenomTarget
Items\Decorative\MonsterStatuette.cs | primary MonsterStatuette | OnOffGump
Items\Decorative\Origami.cs | primary OrigamiPaper | OrigamiDragon, OrigamiBunny
Items\Decorative\Statues.cs | primary StatueSouth | StatuePegasusSouth, StatuePegasusEast, StatueGargoyleEast, StatueGargoyleSouth, StatueGryphonEast, StatueGryphonSouth
Items\Decorative\Tables.cs | primary ElegantLowTable | TerMurStyleTable
Items\Decorative\WindChimes.cs | primary WindChimes | OnOffGump
Items\Equipment\Armor\BaseArmor.cs | primary BaseArmor | UnBlessEntry, SetFlag
Items\Equipment\Clothing\BaseClothing.cs | primary BaseClothing | UnBlessEntry, SetFlag
Items\Equipment\Clothing\Cloaks.cs | primary BaseCloak | GargishClothWingArmor, GargishFancyRobe, GargishRobe
Items\Equipment\Clothing\MiddleTorso.cs | primary BaseMiddleTorso | GargishSash
Items\Equipment\Clothing\OuterLegs.cs | primary BaseOuterLegs | FemaleGargishClothKilt, MaleGargishClothKilt, GuildedKilt, CheckeredKilt, FancyKilt
Items\Equipment\Clothing\OuterTorso.cs | primary BaseOuterTorso | ZooMemberSkirt, ZooMemberBodySash, ZooMemberRobe, ZooMemberCloak, LibraryFriendBodySash, LibraryFriendDoublet, LibraryFriendSurcoat, LibraryFriendCloak, Adranath, OdricsRobe, BaronLenshiresCloak, RewardGargishRobe, RewardGargishFancyRobe, FloweredDress, EveningGown, Epaulette, GargishEpaulette
Items\Equipment\Clothing\Shirts.cs | primary BaseShirt | MaleGargishClothChest
Items\Equipment\Clothing\Shoes.cs | primary Shoes | ZooMemberThighBoots, JesterShoes
Items\Equipment\Clothing\Waist.cs | primary BaseWaist | GargoyleHalfApron, GargishApron
Items\Equipment\Jewelry\BaseJewel.cs | primary BaseJewel | UnBlessEntry
Items\Equipment\Jewelry\Necklace.cs | primary Necklace | OctopusNecklace
Items\Equipment\Quivers\BaseQuiver.cs | primary BaseQuiver | IRangeDamage, RefillQuiverEntry
Items\Equipment\Spellbooks\NecromancerSpellbook.cs | primary NecromancerSpellbook | CompleteNecromancerSpellbook
Items\Equipment\Talismans\BaseTalisman.cs | primary BaseTalisman | TalismanSkill
Items\Equipment\Talismans\TalismanAttribute.cs | primary TalismanAttribute | ITalismanProtection, ITalismanKiller
Items\Equipment\Weapons\BaseWeapon.cs | primary BaseWeapon | UnBlessEntry, SetFlag
Items\Functional\Ankhs.cs | primary Ankhs | MemorialStone
Items\Functional\HouseRaffleStone.cs | primary HouseRaffleStone | RaffleContextMenuEntry
Items\Functional\PowerGenerator.cs | primary PowerGenerator | Node, GameGump
Items\Internal\Beard.cs | primary Beard | GenericBeard, LongBeard, ShortBeard, Goatee, Mustache, MediumShortBeard, MediumLongBeard, Vandyke
Items\Internal\Blocker.cs | primary Blocker | GMItemPacket
Items\Internal\Hair.cs | primary Hair | GenericHair, Mohawk, PageboyHair, BunsHair, LongHair, ShortHair, PonyTail, Afro, ReceedingHair, TwoPigTails, KrisnaHair
Items\Internal\ItemInterfaces.cs | primary IUsesRemaining | IAccountRestricted, IVvVItem, IOwnerRestricted, IFlipable, IQuality, IResource, IConditionalVisibility, IImbuableEquipement, ICombatEquipment, ItemQuality, DirectionType
Items\Internal\LOSBlocker.cs | primary LOSBlocker | GMItemPacket
Items\Internal\Teleporter.cs | primary Teleporter | ClickTeleporter
Items\Resource\Bandage.cs | primary Bandage | BandageTimerPacket
Items\Resource\Board.cs | primary Board | BaseWoodBoard
Items\Resource\Cloth.cs | primary Cloth | CutUpCloth, CombineCloth
Items\Resource\Log.cs | primary Log | BaseLog
Items\Resource\RecallRune.cs | primary RecallRune | RecallRuneType
Items\Tools\BaseHarvestTool.cs | primary BaseHarvestTool | MiningType
Items\Tools\BaseTool.cs | primary BaseTool | ITool
Items\Tools\Clocks.cs | primary MoonPhase | ClockTime, LargeGrandfatherClock, SmallGrandfatherClock, WhiteGrandfatherClock
Items\Tools\DisguiseKit.cs | primary DisguiseKit | DisguiseTimers
Items\Tools\MapItem.cs | primary MapItem | NewMapDetails
Items\Tools\SledgeHammer.cs | primary SledgeHammer | SledgeHammerWeapon
Items\Tools\SmithHammer.cs | primary SmithHammer | SmithyHammer
Items\Tools\TinkerTools.cs | primary TinkerTools | ToggleRepairContextMenuEntry
```
