# P24 section 5: dungeon starter set gear, upgrades, jewelry, replacement quest

Date: 2026-10-01. Agent: Claude Code. Read-only research; nothing outside this scratch folder changed.
Engine authority: `D:\UO\ModernUO-pinned` at `7c9215d97` (checked with `git log -1`).
Path shorthands: `P:` = `D:\UO\ModernUO-pinned\Projects\`, `C:` = `D:\ShatteredLegacy\server\customizations\`,
`PA:` = `D:\ShatteredLegacy\server\patches\`. `server\uo` was not read.

Context taken from the brief and from `notes/f12-levels-loops-caps.md:92-95` (uncommitted, read as-is): the
dungeon's Tier 1 set carries no level requirement and is "blessed, no-trade and re-obtainable from the repeatable
quest", the guaranteed floor of every loop.

## Headline

- Pinned already has a real no-trade mechanism: `Item.Nontransferable` (`P:Server/Items/Item.cs:522`). It blocks
  drop on another mobile (which is how secure trade starts), drop into any container except the owner's top-level
  backpack, drop to the ground, and splitting, and keeps the item on death. 25 overrides in 24 files use it
  (list in 1.2). `LootType.Blessed` and `BlessedFor` do NOT block trade; they only keep the item on death and
  block stealing/insurance.
- Our P15/F-9 starter kit does not bind items at all. It binds the *grant* to the character (a per-character
  record keyed by serial) and replaces a lost item for scrip only when the player no longer owns a copy. That
  "still owns one?" check is reusable for the set's replacement quest.
- Upgrades fit pinned's `CustomCraft` path (only user: `TrapCraft`, `P:UOContent/Engines/Craft/DefTinkering.cs:590`):
  a craft menu entry with resources (parts) and a skill threshold, then a target, then modify the targeted item.
  Additive registration without patching pinned is an established pattern in our tree
  (`C:Engines/Craft/TinkeringCraftRegistrations.cs:29-32`).
- Recommended crafter flow: option (b), owner-initiated consent, item never moves. Cheapest safe variant described
  in 2(b).
- Durability: armour and clothing with `MaxHitPoints == 0` never wear (`P:UOContent/Items/Armor/BaseArmor.cs:771`).
  Weapons do NOT have that guard (see 4.2). No durability loss on death exists in pinned (4.3).
- Replacement quest: ML Quests (the New Haven board's engine) supports repeatable quests directly
  (`OneTimeOnly=false`, optional `HasRestartDelay` + virtual `GetRestartDelay`), and both `CanOffer` and
  `BaseReward.AddRewardItems` are overridable, so "only replace what is missing" is a small override.

---

## 1. No-trade

### 1.1 What pinned has

| Mechanism | Where | What it does | Blocks trade? |
|---|---|---|---|
| `LootType.Blessed` | enum `P:Server/Items/Item.cs:80`; `CheckBlessed` `:4196-4197` | Stays in pack on death (`OnParentDeath` `:2178`/`:2190`, `OnInventoryDeath` `:2208`/`:2220`); cannot be stolen (`P:UOContent/Skills/Stealing.cs:220`); cannot be insured (`P:UOContent/Mobiles/PlayerMobile.cs:3817`); skipped by monster `DestroyEquipment` (`P:UOContent/Mobiles/Abilities/DestroyEquipment.cs:21`) | No |
| `BlessedFor` (Mobile) | `P:Server/Items/Item.cs:767`; saved `:914-916`, `:1068-1070` | Counts as blessed only for that mobile (`CheckBlessed` `:4197`). Talismans also refuse `CanEquip` for anyone else (`P:UOContent/Items/Talismans/BaseTalisman.cs:340-346`) and auto-bind on first equip (`:358-361`) | No |
| `Nontransferable` (virtual bool, default `QuestItem`) | `P:Server/Items/Item.cs:522` | See next rows | Yes |
| ... drop on a mobile | `OnDroppedToMobile` `:3400-3409`, called from `DropToMobile` `:3414-3415` | Refused for players. `Mobile.OnDragDrop` opens secure trade only via this path (`P:Server/Mobiles/Mobile.cs:7560-7568`), so the item never reaches a trade window | Yes |
| ... drop into a container | `OnDroppedInto` `:3424` and `OnDroppedOnto` `:3461` | Refused unless the target is exactly `from.Backpack`: no sub-bags, no bank box, no trade container, no vendor | Yes |
| ... drop to world | `OnDroppedToWorld` `:3513` | Refused | Yes |
| ... lift part of a stack | `P:Server/Mobiles/Mobile.cs:5033` | Refused | n/a |
| ... death | `:2200`, `:2230` | Moved to backpack | n/a |
| `HandleInvalidTransfer` | `:3132-3141` | Message only when `QuestItem`; override to give our own message | n/a |
| `AllowSecureTrade` / `OnSecureTrade` | `:1783`, `:1788`; checked at `P:Server/SecureTrade.cs:210`, `:230` | Veto at accept time. Only the trade container's top-level items are checked (loops over `Container.Items`) | Optional second guard |
| `PlayerMobile.CheckTrade` | `P:UOContent/Mobiles/PlayerMobile.cs:2138` | Per-trade checks (holding, already trading, RefuseTrades, item/weight caps); nothing item-binding | No |
| `AllowItemUse` / `CheckItemUse` | `P:UOContent/Mobiles/PlayerMobile.cs:1778-1787`; `P:Server/Items/Item.cs:4007`; `P:Server/Mobiles/Mobile.cs:4931-4934`, `:7678`, `:7689` | Double-click gates (duel, house design) | No |
| `IsAccessibleTo` | `P:Server/Items/Item.cs:3940-3947` | Region accessibility only; the secure-trade ownership check is commented out (`:3949-3954`) | No |
| `Insured` | `CheckBlessed` `:4197` | Death keep only, and blessed items cannot be insured (above) | No |

No "bind on pickup/equip" flag exists beyond `BlessedFor` + the talisman `CanEquip` pattern. `PlayerMobile` has no
`CheckTrade` rule on item type.

### 1.2 Pinned precedents for `Nontransferable`
Counted: `grep "override bool Nontransferable => true"` = 25 hits in 24 files: 22 in
`P:UOContent/Engines/ML Quests/Items/` (AlchemistsBandage, APersonalLetterAddressedToAhie, BasinOfCrystalClearWater,
BridesLetter, CompletedTuitionReimbursementForm, CrateForSledge, DreadSpiderSilk, FragmentOfAMapDelivery,
FriendsOfTheLibraryApplication, GiftForArielle, NotarizedApplication, OfficialSealingWax, PortraitOfTheBride,
QuestGiverItem x2, ReginasLetter, ReginasRing, SealedNotesForJamal, SealingWaxOrderAddressedToPetrus,
SignedTuitionReimbursementForm, SpiritBottle, TaintedTreeSample, TuitionReimbursementForm) plus two non-quest items:
`P:UOContent/Spells/Spellweaving/Items/ArcaneFocus.cs:32` and `TransientItem.cs:24`. ArcaneFocus is the closest
precedent: an ordinary non-quest item that cannot leave its owner.

### 1.3 What our code does (P15/F-9)
- `C:ClusterFGuildStarterPath.cs:12-14`, `:254-262`: the record is per character (`GuildStarterRecord` keyed by
  `pm.Serial` in `ClusterFAccountData`). The kit items themselves get no `Nontransferable`, no `BlessedFor`; the
  only loot-type change in the kit path is pre-AOS `Newbied` (`C:CharacterCreation.cs:734-736`, `:760-762`).
- Replacement: `ReplaceStarterItem` (`C:ClusterFGuildStarterPath.cs:437-490`) costs `ReplacementScrip = 10`
  (`:250`) and refuses if the player still owns a copy: it builds the quest's reward items to learn their types,
  deletes them, then checks `OwnsCopy` (`:423-431`: worn, backpack recursive, bank). Reusable for the set.
- Our existing set pieces are blessed, not no-trade: e.g. `C:Items/Artifacts/Equipment/Armor/Sets/Initiation/InitiationChest.cs:19`
  (`LootType.Blessed`), on our `BaseSetArmor` (`C:Items/Artifacts/Equipment/Armor/Sets/BaseSetArmor.cs:17-18`).
- No `Nontransferable`, `AllowSecureTrade` or `BlessedFor` anywhere in `C:` or `PA:` (grep, 0 hits for the three).

### 1.4 Recommendation for the set
New piece classes (on `BaseSetArmor`/`BaseSetClothing`/`BaseSetWeapon`, `C:Items/Artifacts/Equipment/Armor/Sets/`)
with `LootType = Blessed`, `BlessedFor = owner` set at grant, `override bool Nontransferable => true`, a
talisman-style `CanEquip` owner check, and an `AllowSecureTrade => false` belt-and-braces override. Two UX costs of
stock `Nontransferable` to decide on: the piece can live only in the top-level backpack or worn (no bank, no bags,
`:3424`, `:3461`). If that is too harsh, override `OnDroppedInto`/`OnDroppedOnto` to also allow
`target.IsChildOf(from.Backpack)` and the owner's own `BankBox`. Not prototyped.

---

## 2. Crafter upgrades on no-trade gear

Ground rules in pinned that shape all three options:
- Targeting another player's item: `Target.CanTarget` refuses an item whose `RootParent` is another mobile unless
  `AllowNonlocal` is set (`P:Server/Targeting/Target.cs:115-120`, property `:28`). Then range/LOS/`CanSee`
  (`:180-188`), `IsAccessibleTo` (`:196`), `Item.CheckTarget` (`:200`). `Mobile.CanSee(Item)` walks the parent chain
  (`P:Server/Mobiles/Mobile.cs:7114-7136`), so a *worn* piece is visible; a piece inside someone's pack is visible
  only if its container is open to the viewer (snooping).
- Stock repair and enhance both require the item in the crafter's own pack or worn by the crafter:
  `P:UOContent/Engines/Craft/Core/Repair.cs:269`, `:343`, `:414`; `P:UOContent/Engines/Craft/Core/Enhance.cs:34`. So
  OSI's model is "hand it over", which a no-trade item cannot do.
- `Mobile.CheckNonlocalLift` / `CheckNonlocalDrop` refuse non-staff touching items on another mobile
  (`P:Server/Mobiles/Mobile.cs:7508-7509`, `:7675-7676`).

**(a) Owner upgrades own piece only.** Allowed by everything above with no special handling: the craft entry
targets an item in `from.Backpack` or worn. Cost: lowest (the CustomCraft class of section 3 only). Gameplay cost:
the owner needs the matching craft skill at 30/50/70, which removes the crafter economy the brief wants.

**(b) Owner + crafter together, consent, item never moves.** Two shapes:
- (b1) Crafter-initiated: the crafter's upgrade target sets `AllowNonlocal = true`, range 2, and accepts only a
  set piece *worn* by the target player (visible on paperdoll; pack contents are not, see above). Owner gets a
  consent gump; on yes, the crafter's craft entry has already passed skill and consumed parts (CustomCraft flow,
  3.1) and the level is applied. Risk: consume-before-consent ordering; consent must happen before
  `CompleteCraft` is invoked, i.e. inside the target callback, before calling `CraftItem.CompleteCraft`
  (as `TrapCraft` does at `DefTinkering.cs:682-695`).
- (b2) Owner-initiated (simpler, recommended): owner double-clicks the piece, targets a crafter within 2 tiles of a
  forge/loom; crafter gets a gump naming piece, next level, parts needed; on accept, the code checks the crafter's
  skill against the threshold, consumes parts from the crafter's pack (or the owner's, a design choice), raises
  the level. No item moves, no targeting rule is bent. This bypasses the CraftSystem menu, so it does not get
  craft-menu skill gain or the craft gump UI; it would call `CheckSkill` directly as our Imbue gump does
  (`C:ArtificersImbueGump.cs:1406`).
Cost: (b2) roughly one gump + one target + the upgrade routine, an estimate of 150-250 lines, unverified;
(b1) similar plus nonlocal targeting edge cases.

**(c) Let no-trade gear pass through secure trade.** Stock path: the drop that opens trade calls
`OnDroppedToMobile` (`P:Server/Items/Item.cs:3414-3415`), dropping into an open trade uses `OnDroppedInto`/`Onto`
(`:3424`, `:3461`), and on accept items move by `AddToBackpack` (`P:Server/SecureTrade.cs:293-297`, `:315-319`;
cancel returns at `:102-106`, `:124-128`) after `AllowSecureTrade` vetoes (`:210`, `:230`). To whitelist, the piece
would override `OnDroppedToMobile` and `OnDroppedInto/Onto` to allow a `SecureTradeContainer` target when the
counterparty qualifies (crafter with skill, or the piece's `BlessedFor` owner on the way back), and
`AllowSecureTrade` to enforce the same at accept. Problem: once in the crafter's pack the piece is a hostage; the
owner's only recourse is the replacement quest (which would then see "does not own a copy" and replace it, at base
level). Needs a return mechanism (timer or "return to owner" on logout). Cost: moderate, plus abuse surface. Not
recommended.

---

## 3. Applying an upgrade

### 3.1 Pinned craft-system support
- `CustomCraft` (`P:UOContent/Engines/Craft/Core/CustomCraft.cs:6-34`): abstract `EndCraftAction()` and
  `CompleteCraft(out int message)`. The craft item's `ItemType` is the CustomCraft subclass; the craft engine
  instantiates it after the craft timer (`P:UOContent/Engines/Craft/Core/CraftItem.cs:1370-1380`).
- The only pinned users: `TrapCraft` (`DefTinkering.cs:590`) and its 3 subclasses Dart/Poison/Explosion
  (`:728`, `:741`, `:754`), registered with `AddCraft(typeof(DartTrapCraft), ...)` (`:416`). Flow: `EndCraftAction`
  sets a target (`:651-655`), `Acquire`/`Verify` checks the target (`:601-649`), then calls
  `CraftItem.CompleteCraft(..., customCraft)` (`:682-695`), whose override modifies the target (`:657-674`).
  This is exactly "target an item, consume resources, modify it".
- Our tree carries its own `CraftItem.cs` (`C:CraftItem.cs`); in it `CompleteCraft` checks resources (`:1066`),
  checks skills (`:1107`), consumes (`:1109`), then calls `customCraft.CompleteCraft` (`:1176-1178`). How this file
  supersedes pinned's at build time was not checked here.
- Skill threshold: `AddCraft(..., minSkill, maxSkill, ...)` (`P:UOContent/Engines/Craft/Core/CraftSystem.cs:126-177`)
  plus `AddSkill` (`:258-260`); below `minSkill` the player gets 1044153 "You don't have the required skills"
  (`C:CraftItem.cs:881`, `:948-955`). Draft 30/50/70 = three entries (one per level band) with `minSkill` 30/50/70.
  Extra parts: `AddRes(index, typeof(Part), ...)` (`CraftSystem.cs:253-255`), any number per entry.
- Station: blacksmithy's `CanCraft` already demands anvil + forge (`P:UOContent/Engines/Craft/DefBlacksmithy.cs:110-117`).
  Tailoring demands none (`DefTailoring.cs` CanCraft, lines ~39-47); a loom check would go in our `Verify`, looking
  for an `ILoom` within range (`P:UOContent/Items/Addons/LoomEastAddon.cs:5`).
- Additive registration without patching pinned: `C:Engines/Craft/TinkeringCraftRegistrations.cs:29-55`
  (`EventSink.ServerStarted += Register`, idempotent, then `tinkering.AddCraft/AddRes/AddSkill`); same pattern in
  `BlacksmithyCraftRegistrations.cs` and `TailoringCraftRegistrations.cs`.
- Other paths considered: `Repair.cs` (restores HP only, own items only, `:151-`, `:343`); `Enhance.cs` (runic
  resource enhancement, own backpack only, `:34`, consumes at `:91-97`, `:244-300`); `Resmelt.cs` (exists, not a
  modifier). Runic tools only change the crafted item's resource/attributes at make time. None of them is a
  better fit than CustomCraft.
- Our Imbuing: `C:ArtificersImbueGump.cs` (1683 lines) is a stand-alone gump, not a CraftSystem entry: own target
  (`:1590-1610`, requires `item.RootParent == from`), own `CheckSkill(SkillName.Imbuing, ...)` (`:1406`, `:1478`),
  property setters via lambdas (`:114-314`). `C:ArtificersToolkit.cs` (70 lines) is a blessed item that opens it.
  This is the template for option 2(b2) if the CraftSystem menu is skipped.

So: no new engine is needed. Either (a)/(b1) a CustomCraft subclass per craft (smith, tailor, maybe tinker), added
by a registration file; or (b2) a small tool/gump like the Imbue gump.

### 3.2 Storing the upgrade level
- ModernUO source-generated serialization: `BaseArmor` is `[SerializationGenerator(9, false)]`
  (`P:UOContent/Items/Armor/BaseArmor.cs:15-16`) with `[SerializableField(n)]` + `[SerializableFieldSaveFlag(n)]`
  pairs (`:90-108`). Our `BaseSetArmor` is its own `[SerializationGenerator(0, false)]` layer with fields
  (`C:Items/Artifacts/Equipment/Armor/Sets/BaseSetArmor.cs:17-44`), and each set piece is again version 0
  (`InitiationChest.cs:12`). Each class in the chain versions independently.
- Changing an existing type's fields requires a version bump, a schema file and `MigrateFrom(VnContent)`: our only
  example is PetMimic, `[SerializationGenerator(9, false)]` (`C:PetMimic.cs:40`) with `MigrateFrom(V0..V8Content)`
  (`:477-788`) and 9 schema files `D:\ShatteredLegacy\server\migrations\Server.Items.PetMimic.v0.json` .. `v8.json`
  (counted: 9 files, the whole folder).
- Recommendation: new types only. A new abstract `BaseDungeonSetArmor : BaseSetArmor` (and clothing/weapon
  siblings) at `[SerializationGenerator(0, false)]` with `[SerializableField(0)] private int _upgradeLevel;` and the
  part family as a second field if needed. No existing type changes, so no migration and no schema file now; the
  first later field change bumps to 1 with one `MigrateFrom(V0Content)`. Apply level effects in a single
  `ApplyLevel()` that recomputes from base each time (not incremental) so a replacement "starts at base level"
  trivially and a GM `[props` edit cannot desync.
- Per-character "has had the set" bookkeeping, if needed, belongs in `ClusterFAccountData` beside the starter
  record (P11 serializer, version-bumped there) or simply in `MLQuestContext` done-quest records (section 6).

---

## 4. Durability

### 4.1 Armour and clothing: "never breaks" is free
- Initial durability is `RandomMinMax(InitMinHits, InitMaxHits)` (`P:UOContent/Items/Armor/BaseArmor.cs:164`), both
  default 0 (`:730-731`). Wear in `OnHit` only happens `if (wear > 0 && _maxHitPoints > 0)`
  (`:771`); `MaxHitPoints == 0` hides the durability line (`:1473-1475`) and repair says "already in full repair"
  (`Repair.cs:347`). `OnHit` is `virtual` (`:753`), so a piece can also override it.
- Clothing: same guard (`P:UOContent/Items/Clothing/BaseClothing.cs:368`, init `:120`, `InitMinHits` `:339`).
- Shields: `if (wear <= 0 || MaxHitPoints <= 0)` return early (`P:UOContent/Items/Shields/BaseShield.cs:80`).
- Other HP sinks found by grep: Ilhenir only hits items with `HitPoints >= 10`
  (`P:UOContent/Mobiles/Monsters/ML/Special/Ilhenir.cs:351-353`), so 0/0 is immune; `DestroyEquipment` skips blessed
  (`DestroyEquipment.cs:21`).
- "Indestructible" in pinned is only a durability-bonus tier (+120%, `BaseArmor.cs:907-914`), not unbreakable.
  `ArmorAttributes.SelfRepair` adds 2 HP on a 25% wear roll (`:763-765`; our `PA:BaseArmor-set-self-repair.patch`
  adds the set's self repair there). `ScaleDurability`/`UnscaleDurability` (`:733-748`) rescale max HP on
  resource/quality changes. `CanFortify` (`:696`) gates Powder of Temperament.
- Note our existing set pieces DO wear: e.g. Initiation `InitMinHits/InitMaxHits => 150` (`InitiationChest.cs:37-38`).
  For the dungeon set use 0/0 (or override `OnHit`) and `CanFortify => false`.

### 4.2 Weapons: 0/0 is NOT safe
`BaseWeapon` wear on hit (`P:UOContent/Items/Weapons/BaseWeapon.cs:2076-2108`): on a 1-in-25 roll (or acid
monster, which does require `_maxHitPoints > 0`, `:2077`), if `_hitPoints > 0` decrement, else if
`_maxHitPoints > 1` decrement max, **else `Delete()`** (`:2108`). A weapon with 0/0 would be deleted on that roll by
my reading. Not runtime-verified. Set weapons must override this (the method is not separately virtual here; I did
not check which enclosing method is overridable) or use high durability plus `SelfRepair`. Also see our
`PA:BaseWeapon-talisman-durability.patch` (not read).

### 4.3 Death
No durability loss on death in pinned: no `HitPoints` writes in `PlayerMobile.cs` (grep: 0 hits). Blessed and
insured items stay with the player (`FindItems_Callback`, `PlayerMobile.cs:2419`); insurance is re-bought or lost
on death (`CheckInsuranceOnDeath`, `:2473-2512`) but blessed items cannot be insured (`:3817`). Shard customizations
were not searched for a death-durability rule; none is known.

---

## 5. Jewelry

- Tinkering makes jewelry: `AddJewelrySet(GemType, Type)` (`P:UOContent/Engines/Craft/DefTinkering.cs:145-`, first
  entry `GoldRing` at `:149-160` with `IronIngot` x2 then the gem via `AddRes` `:160`), called 9 times (`:380-388`,
  one per gem). Our `TinkeringCraftRegistrations.cs:58-61` adds 4 gargish jewelry entries.
- Multi-ingredient precedent with monster drops: ML magic jewelry (`DefTinkering.cs:511-567`), e.g.
  `ResilientBracer` = IronIngot x2 + `CapturedEssence` x1 + `BlueDiamond` x10 + `Diamond` x50, skill 100-125,
  rare recipe, `ForceNonExceptional`. A dungeon recipe is the same shape: `AddCraft(typeof(NewRing), ..., IronIngot)`
  then `AddRes(index, typeof(PartX), ...)` per part, plus `AddRecipe` if it should be learned.
- Adding properties on craft: `ICraftable.OnCraft` (`P:UOContent/Engines/Craft/Core/CraftItem.cs:19-25`), called at
  `C:CraftItem.cs:1192-1194`. `BaseJewel.OnCraft` is **not virtual** (`P:UOContent/Items/Jewels/BaseJewel.cs:128`)
  and reads `Resources[1]` as the gem (`:144-153`), unlike `BaseArmor`/`BaseWeapon`/`BaseClothing` whose `OnCraft`
  is virtual (`BaseArmor.cs:558`, `BaseWeapon.cs:665`, `BaseClothing.cs:187`). Options: a new jewel class that
  re-implements `ICraftable` (C# interface re-implementation; compiles in principle, not tested) or, simpler, apply
  properties in the constructor/`OnAdded`, or make the recipe a `CustomCraft` that builds the item itself.
  Jewelry is tradeable per the brief, so no binding.

---

## 6. Repeatable replacement quest

### 6.1 ML Quests (recommended; the New Haven board's engine)
- Our board is `C:Engines/ML Quests/Items/NewHavenQuestBoard.cs:50` (`NewHavenQuestBoard : QuestGiverItem`),
  registering stock quests via `MLQuestSystem.Register` (`:98-99`); see `notes/new-haven-quest-board.md`.
- Repeatability on `MLQuest` (`P:UOContent/Engines/ML Quests/MLQuest.cs`): `OneTimeOnly` (`:61`), `HasRestartDelay`
  (`:63`), `RecordCompletion => OneTimeOnly || HasRestartDelay` (`:71`), `virtual GetRestartDelay()` default
  30-150 s (`:240`). With both false, completion is not recorded and the quest is re-offerable at once. With
  `HasRestartDelay`, completion is logged when objectives finish with `Core.Now + GetRestartDelay()`
  (`MLQuestEntry.cs:337-339`) and `CanOffer` refuses until then (`MLQuest.cs:153-163`). Pinned uses
  `HasRestartDelay = true` 50 times in 3 files (Heartwood.cs, NewHavenTraining.cs, Sanctuary.cs; counted).
- Gate on "lost a piece": `virtual CanOffer(quester, pm, context, message)` (`MLQuest.cs:117-183`); override to
  refuse when the player owns every piece (reuse `OwnsCopy`, `C:ClusterFGuildStarterPath.cs:423-431`).
- Conditional rewards: `BaseReward.AddRewardItems(PlayerMobile, List<Item>)` is abstract (`Rewards/BaseReward.cs:20`);
  `ItemReward` implements it (`Rewards/ItemReward.cs:68`). `ClaimRewards` (`MLQuestEntry.cs:354-`) calls every
  reward's `AddRewardItems` (`:365`), handles an empty list fine (`:368` guards only the non-empty path), then
  `Quest.OnRewardClaimed` (`:416`). A custom `MissingSetPieceReward : BaseReward` that adds only the pieces the
  player lacks, at base level and bound (`BlessedFor = pm`), is the whole replacement path. `GetRewards`
  (`MLQuest.cs:219-222`) and `OnRewardClaimed` (`:224`) are also virtual.
- Our starter path already ties MLQuest completion to its own ledger (`MLQuestContext.SetDoneQuest`, cited in
  `C:ClusterFGuildStarterPath.cs:16-18`).

### 6.2 Old QuestSystem (`P:UOContent/Engines/Quests/`)
Abstract `RestartDelay` per quest (`Core/QuestSystem.cs:61`), done list on the player (`:356-380`,
`From.DoneQuests`), `CanOfferQuest(check, type, out inRestartPeriod)` (`:439-476`). Every quest is bespoke
(objectives, conversations, quester classes; the folder has 13 entries, 11 of them quest folders once Core and Regions are
excluded). Heavier to author and not what our board
uses; not recommended.

---

## Not verified
- Nothing was built or run. All behaviour is from reading source.
- Weapon 0/0 deletion (4.2) is a reading of `BaseWeapon.cs:2076-2108`; enclosing method name and overridability not
  checked.
- How `C:CraftItem.cs` replaces pinned's `CraftItem.cs` in the build; I cited both.
- ICraftable re-implementation on a `BaseJewel` subclass (5) not compiled.
- Whether NPC vendors would buy the pieces: `BaseVendor.cs` has no blessed/Nontransferable check (grep), but sale
  depends on the vendor's sell list, which would not list new types; not traced.
- Line estimates in 2(b) are guesses.
- `PA:BaseWeapon-talisman-durability.patch` and `notes/s5-quest-spike.md` were not read in full.
