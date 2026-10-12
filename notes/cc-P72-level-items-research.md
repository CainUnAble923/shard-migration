# cc-P72: leveling gear research (ServUO XmlLevelItems to ModernUO, under Chase's five rules)

Notes only, 2026-10-10, by Claude (cc-P72). Brief: `D:\UO\cc-prompts\cc-P72-level-items-research.md`. Nothing built,
nothing in `D:\ShatteredLegacy` written, built, deployed or committed; no worktree was needed (no throwaway code beyond a
pacing script in the session scratchpad, reproduced in Part C.5). `CHANGELOG.md` and `VERSION` not touched.

- **Engine authority: `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`** (`git rev-parse HEAD`,
  2026-10-10). Every pinned file:line below is on that commit, paths relative to `Projects\`.
- **Shard read at `D:\ShatteredLegacy` HEAD `a6e17fd`** ("Shard work, 2026-10-10 15:35"; `git status` clean when read, so
  P67's work is now committed). `C\` = `server\customizations`, `P\` = `server\patches`.
- **XmlLevelItems source:** where it came from, and what could not be fetched, is in Part A.0. Nothing about it here is
  reconstructed from memory.

---

## Headlines

1. **XmlLevelItems is an XmlSpawner attachment** (`XmlLevelItem : XmlAttachment`) holding four ints (XP, level, max
   level, points), version 0 only. It is not an item subclass, and it needs XmlSpawner's attach engine, which ModernUO
   does not have. **Port the design, not the code:** a save-file registry of our own (`GenericPersistence`, keyed by item
   Serial) replaces the attachment with **no change to any stock item's save chain**.
2. **As shipped it breaks rules 2 and 5, and half of rule 4.** XP comes only from the **killing blow** (one line added to
   `BaseCreature.OnDamage`), so **pets' and summons' kills pay their owner nothing** (rule 5; a forum thread reports
   exactly this); the deed works on **any** weapon, armour or jewel, artifacts included (rule 2); clothing refuses it
   (rule 4's "every item"). It does pay every equipped levelable item the full XP (rule 4), a pet's own gear can level
   from the pet's kills (rule 3), and its default max level is 200 (rule 1), though only
   because the constructor hard-codes 200 and ignores its own setting.
3. **Rule 5 needs no pinned patch.** Pinned's damage list already records every contributor and the master behind each
   pet, summon and provoked creature (`DamageEntry.Responsible`, filled by `GetDamageMaster`). Paying item XP at the
   creature's death from that list credits hits as well as kills, the owner's gear and the companion's own gear, the way
   pinned's looting rights already merge damage. Armour "on being hit" reads the wearer's own damage list at the same death.
4. **Pinned patches needed: one new (a tooltip line, 5 one-line hunks), one hunk in an existing patch (bonuses added in
   `AosAttributes.GetValue` beside the set-bonus hunk).** The context-menu entry, the XP handler, the gumps, the registry
   and the config are all ours. Estimated build: 5 batches, about 2 M, 1 L, 2 S (Part D).
5. **Inside the shard's caps** (Part C.3): levels buy only AosAttribute properties and resists, never skill bonuses (they
   would pass 200 by D-113) and never Self Repair (F-27); a property's imbued value plus its level bonus never passes the
   imbuing table's ceiling for it, x1.5 for exceptional (F-29); the material sets the point budget.
6. **Loop resets** (C.4): recommended, the item keeps its level, and bonuses above the wearer's level plus Arms Lore
   attunement go dormant; the item never becomes unwearable. **Pacing** (C.5): at creature level 100 a steady player
   (cc-P54 profile A) takes about 5 h to item level 50, 28 h to 100 and 150 h to 200; the live x1 gain rate does not touch
   item XP, which is kill-based.

---

## Part A: what XmlLevelItems is

### A.0 Sources (read; nothing reconstructed from memory)

A read-only sub-agent found and downloaded the sources to the session scratchpad (`levelitems-src\`, one folder per
source; treated as untrusted data, never built or run). I re-read the claims that drive the headlines myself in the
downloaded files (the class line, the hard-coded 200, the save order, the XP table, the per-kill cap, the points, the
command access level, the settings, the `OnDamage` hook): every one holds.

| Short | Source | What it is |
|---|---|---|
| **R** (main) | github.com/ruaduck/xmlspawner @ `d288c39ba7113610702007cd1ea25071cb6ea77d` (2022-01-02), `XmlSpawner/XmlSpawner Extras/XmlLevelItem/`, 13 files; added in `d3c685de` (2021-11-19, "Pub 57") | the ServUO pub 57 copy |
| J | JustUO/JustUO @ `c577f53d9b1c93dd9a64d07c2fbf56e4d4643154`, `Scripts/Mobiles/BaseCreature.cs`, `BaseWeapon.cs` | the distro edits as merged |
| N, I | UONelderim/xmlspawner @ `4ff76b88`, pallop/Ultima-Iberia-Server @ `29846a1b` | same logic, reformatted; differ only in fire-breath detection |
| UA | FinalTwist/Ultima-Adventures @ `29b88c79` | a non-attachment variant on `ILevelable` (A.7) |
| Forums | runuo.com threads 480733 (LordHogFred, "Xml Level Items", 2011-06-27) and 71218 (dracana, "Levelable Items System 3.0", 2006-07-21), via Wayback; servuo.dev threads 14129, 4867, 10810, 3650 p.10 | history and bug reports |

**Could not fetch:** the original zip/rar attachments (archived only as 403 login pages); runuo.com thread 61734 "Level
items Redux" (no snapshots); uofreeshards.net (DNS failure); downloads.runuo.net (DNS failure); ServUO/ServUO master
`d76bf444` has no XmlLevelItem at all, so this is an add-on, not distro. `D:\UO\ServUO-pub57` has none either (grep of
every local ServUO tree for `LevelItem`: 0 hits).

**Lineage:** TheOutkastDev's "Levelable Items" (source not found) -> dracana 3.0 (2006, item subclasses on `ILevelable`)
-> LordHogFred's XML attachment "replica" (2011) -> XmlSpawner extras -> JustUO, ServUO addon packs, ruaduck pub 57.
`ILevelable.cs` still ships in R and nothing uses it.

### A.1 Data model

- `public class XmlLevelItem : XmlAttachment` (`R/Attachments/XmlLevelItem.cs:12`).
- Four ints: experience, level, max level, points (`:14-17`), GM-level command properties.
- `[Attachable] XmlLevelItem() : this(200)` (`:38`): **max level hard-coded to 200**; the setting `DefaultMaxLevel = 200`
  (`R/LevelableItemSettings.cs:9`) is referenced nowhere (grep of all R files: only its declaration).
- `OnAttach` keeps the attachment only on `BaseWeapon`, `BaseArmor`, `BaseJewel` (`:57`); on anything else, clothing
  included, it deletes itself.
- **Save format:** version int 0, then experience, level, max level, points (`:78-83`); load reads the version and ignores
  it (`:90-95`). One version in all four copies.

### A.2 How items gain XP

- **The hook** is one line in `BaseCreature.OnDamage`: `if (!Summoned && willKill) LevelItemManager.CheckItems(from,
  this);` (`J/Scripts/Mobiles/BaseCreature.cs:1520-1521`). R's install text omits this step (`R/XmlLevelItem Install
  NEW.txt`), which forum users hit ("Items not gaining exp?", thread 480733 #24).
- **Credit:** `CheckItems(killer, killed)` (`R/LevelItemManager.cs:124`) walks the **killer's** layers and pays each
  equipped item with the attachment the **full** XP (`:130`). Last hit only; no damage list; backpack items nothing.
- **Pets and summons:** `killer` is never mapped to a master, so a pet's kill looks at the pet's own layers and the owner
  gets nothing. Reported: servuo.dev thread 4867 (2016). Killing summoned creatures pays nothing (`!Summoned` is the
  victim). Nothing stops XP from killing your own pets (sub-agent's reading of the code; not tested).
- **XP per kill** (`CalcExp`, `:84-113`): hits + stamina + mana + total base skills, compressed above 700 (`:92`),
  +100 each for a mage, a fire-breather, poison immunity, vampire bats, +20 per poison level, then /10 (`:110`). **This
  is OSI's Bard difficulty, copied:** pinned `BaseInstrument.GetBaseDifficulty` (`Items\Skill Items\Musical
  Instruments\BaseInstrument.cs:248-300`) has the same terms (pinned reads `HitsMax x 1.6` where XmlLevelItems reads current `Hits`), the same 700 knee with the same factor (3/11 = 1/3.66667)
  and the same /10, plus a paragon bonus. F-14 already recommends that function for creature levels, so item XP and
  creature level can read one number, as XmlLevelItems effectively did. No Fame.
- **Per-kill cap** (`CalcExpCap`, `:115-119`): `ExpToLevel(level + 1) / 20`, applied when `EnableExpCap` (`:161-164`).

### A.3 What a level buys

- **XP table** (`:30-47`): `ExpToLevel(n) = ((n + 1) x 10)^2 - 100`, a table of `MaxLevelsCap` (1000) rows. About 4.0
  million XP at level 200.
- **Points** (`OnLevel`, `:187-194`): 4 per level (`PointsPerLevel`, settings `:15`), 8 on every tenth level. Points are
  paid once per kill, so a kill that jumps two levels pays one level's points (sub-agent's reading; consistent with the
  code at `:161-170`).
- **Spending** (`R/LevelAttributes.cs`): +1 per click at a cost in points, up to a max per property. Examples: Hit Chance
  10 pts / max 15 (`:27`), Damage Increase 5 / 50 (`:34`), Luck 2 / 100 (`:43`), weapon Self Repair 2 / 10 (`:52`),
  every hit spell and leech 3 / 50 (`:53` on), Resist Physical Bonus 40 / 20 (`:68`, an outlier), armour Self Repair 2 / 5
  (`:82`), resists 2 / 20 on jewellery and clothing. **Artifacts cost double** when `DoubleArtifactCost` and rarity >= 10.
  No limit on stacking hit spells (asked for, thread 480733 #21). The caps are its own table, not the item's.

### A.4 Gumps, commands, items, settings

- **Commands** `[itemexp` and `[ixp`, registered at **Counselor** (`R/ItemExpCommand.cs:23-24`), so players cannot use
  them (dracana's original had them as player commands); players reach the gump through the context-menu entry
  `LevelInfoEntry`.
- **Gumps:** `ItemExperienceGump` (categories left, 10 properties a page right, "+" buttons); `LevelUpAcceptGump` (sent
  to a blacksmith, cannot be closed); `AwaitingSmithApprovalGump`.
- **Items:** `LevelItemDeed` (blessed; attaches the system to a targeted weapon, armour, clothing piece or jewel; deletes
  itself), and `LevelUpScroll` (+5/10/15/20 max level, validated by a 100-Blacksmithy smith who is paid a 500-gold check).
  Nothing in the package drops the scrolls.
- **Settings** (`R/LevelableItemSettings.cs:9-22`): DefaultMaxLevel 200 (unused), MaxLevelsCap 1000, EnableExpCap true,
  DisplayExpProp true, PointsPerLevel 4, DoubleArtifactCost true, BlacksmithOnly true, BlacksmithSkillRequired 100,
  RewardBlacksmith true, BlacksmithRewardAmt 500 (the last four `const`).

### A.5 Distro edits it needs

1. `GetContextMenuEntries` in BaseWeapon (and BaseArmor, BaseClothing, BaseJewel per the install text): add
   `LevelInfoEntry` when the attachment is present (J `BaseWeapon.cs:585-589`).
2. Optional: `BaseWeapon.GetProperties` shows level and XP (J `BaseWeapon.cs:4511-4517`).
3. Not in the install text but required: the `BaseCreature.OnDamage` line (A.2).
No PlayerMobile, crafting, repair or loot edits.

### A.6 Known bugs and exploits

From the forums (quotes kept short):
- Max level always 200 (thread 480733 #7, 2011; servuo.dev 14129, 2021; fix given there: `: this(LevelItems.DefaultMaxLevel)`).
- The original zip did not compile: "'ChangeName' does not exist" (480733 #3).
- No XP without the undocumented `OnDamage` edit (480733 #24, servuo.dev 14129).
- Pets and summons give no XP (servuo.dev 4867).
- Clothing refuses the attachment (480733 #7).
- `HasBreath` compile error on newer ServUO (servuo.dev 3650 p.10); ruaduck's `d288c39` fixes it.
- Deeds level artifacts (servuo.dev 10810, about a custom exceptional-only deed; the stock deed checks only the item's
  base type, `R/Items/LevelItemDeed.cs:23`, so it takes artifacts too).
- dracana's version crashed at start with `MaxLevelsCap` 1,000,000 (thread 71218 p.3).
- No forum report found of duplication, level transfer or training-dummy XP.

From reading the code (sub-agent, not tested in a game; I spot-checked the clothing one):
1. The deed accepts clothing, the attachment deletes itself, and the deed is used up anyway.
2. **Gold farm:** before a smith accepts, the scroll owner can target the smith again and again; each opens another accept
   gump and each Accept pays 500 gold; nothing re-checks the scroll (`R/LevelUpAcceptGump.cs:53-73`).
3. The experience gump trusts the button id: an index is used before its bounds check, and several branches cast the item
   without a type check. A crafted reply may throw. The gump never re-checks that the player still holds the item.
4. A multi-level jump loses points (A.3). 5. XP from killing your own pets. 6. Durability cap read from max hit points
   while raising the durability bonus. 7. Levels travel with the item on trade, by design.

### A.7 Variants

- **dracana 3.0 (2006):** item subclasses (`LevelKryss`...) on `ILevelable`, player commands, 5 points per level, a
  champion that drops scrolls, a modified `Repair.cs`. Same hook and gump design. Attachments not recoverable.
- **Ultima Adventures "God" items** (UA `LevelItemManager.cs`): `ILevelable`, XP = Fame / 225 divided among worn levelable
  items, **pet kills credit the owner** through `GetMaster()` (UA `BaseCreature.cs:5150-5161`) with a 20 % chance per
  item, Stealing also pays XP. The one variant that credits pets; still last-hit.

---

## Part B: porting to ModernUO

### B.1 The rule that decides the shape: no new fields on stock item types

ServUO's version stores its state as an XmlSpawner attachment (Part A.1). ModernUO ships no XmlSpawner and no attachment
system: pinned has no `XmlAttach` type anywhere under `Projects\` (grep of `class XmlAttach`: 0 hits). The three ways to
give an item a level on ModernUO, and why only one survives the repo's rules:

| Option | What it is | Verdict |
|---|---|---|
| Fields on `BaseWeapon`/`BaseArmor`/`BaseJewel`/`BaseClothing` | a patch adding `[SerializableField]`s and a version bump to four pinned files | **Rejected.** Changes four stock save chains in pinned files we patch; every upstream bump that touches those classes (they move often) breaks the patch, and a broken serialization patch is a save-loss risk, not a build error. AGENTS: "Nothing ... should ever require a migration event." |
| Item subclasses (`LevelableLongsword : Longsword`) | ServUO-era "level item" style | **Rejected.** Rule 2 says a crafted item becomes levelable *later*, by a quest or process. Turning an existing item into a subclass means replacing the object (new Serial, lost history, every craft table untouched). Also hundreds of types. |
| **A registry of our own** (`GenericPersistence`, keyed by the item's `Serial`) | pinned `Server\Serialization\GenericPersistence.cs:23` (abstract, `Serialize`/`Deserialize` of its own `.bin`); stock users: `UOContent\Engines\CannedEvil\ChampionTitleSystem.cs:9`, `Engines\Factions\Core\FactionSystem.cs:5`, `Engines\Player Murder System\PlayerMurderSystem.cs:13`; shard precedent `C\Services\PointsSystems\PointsSystem.cs`, `C\Misc\WeakEntityCollection.cs` | **Recommended.** No stock type changes; the save format is ours and versioned in one file; "make levelable" is adding a row; removing the feature is deleting a file. |

**Cleanup without a delete event.** Pinned has no global item-deleted event (grep of `Server\` for `ItemDeleted`,
`OnItemDeleted`, `event.*Delete`: 0 hits). So the registry prunes at save time: any row whose `World.FindItem(serial)`
(`Server\World\World.cs:590`) is null or deleted is dropped. Serials are never reused while an entity with that serial
exists, and a row is only read through a live item, so a stale row is harmless until pruned.

**What the registry holds per item** (proposal): `Serial`, level, XP, unspent points, the points bought per property
(so bonuses can be recomputed, made dormant after a loop reset, or refunded by a respec), the date it was made levelable
and by whom (audit), and a small version byte. The item's own `Attributes` are **never written**: level bonuses are added
at read time (B.2), so an item that leaves the registry is exactly the crafted item it was.

### B.2 Each XmlLevelItems dependency and its ModernUO equivalent

Sizes: S = under a day of builder work with its facts; M = one batch; L = a batch on its own.

| ServUO dependency (A.5) | ModernUO equivalent (pinned file:line) | Patch? | Size |
|---|---|---|---|
| `XmlAttach` attachment on the item, saved in XmlSpawner's attachment file | our registry on `GenericPersistence` (B.1) | none | M |
| Hand-written `Serialize`/`Deserialize` with a version int | `GenericPersistence` writes its own payload; a version byte at the head of our payload, `MigrateFrom` style by hand (the generator does not cover a persistence's payload) | none | S |
| XP on the killing blow, one line in `BaseCreature.OnDamage` (A.2) | **XP at the creature's death from its damage list**, ours only: subscribe to `CreatureEvents.CreatureDeathEvent` (`UOContent\Mobiles\CreatureEvents.cs:8-9`, raised at `BaseCreature.cs:3540` and `:3669`; the shard already subscribes, `C\ClusterFAchievements.cs` `OnCreatureDeath`). Who hit it: `Mobile.DamageEntries` (`Server\Mobiles\Mobile.cs:974`), each `DamageEntry` has `Damager`, `DamageGiven`, `LastDamage`, expiry 2 min (`Mobile.cs` top, `ExpireDelay`), and **`Responsible`**: the master behind a pet or summon, filled by `RegisterDamage` through `GetDamageMaster` (`Mobile.cs:5895-5935`; `BaseCreature.GetDamageMaster` `:3992-4006` returns the provoker for a provoked creature, else `GetMaster()` = `ControlMaster ?? SummonMaster`, `:3333`). Pinned's own looting rights walk exactly this (`BaseCreature.GetLootingRights`, `:3344`) | none | M |
| Armor XP when the wearer is hit | at the same death: the **defender's** damage list holds what this creature did to them: `defender.FindDamageEntryFor(creature).DamageGiven` (`Mobile.cs:5878`) | none | S |
| (option) XP on every hit, paid at once | `AOS.Damage` is where nearly all AOS damage passes; the shard already patches it (`P\AOS-damage-eater-hook.patch`, hunk at `Misc\AOS.cs:226`). One more line there. `Mobile.OnDamage` (`Mobile.cs:5950`) is virtual but `BaseCreature` and `PlayerMobile` already override it (`BaseCreature.cs:1941`, `PlayerMobile.cs:2347`), so a partial class cannot hook it | one line in an existing patch | S |
| Level bonuses applied to the item's attributes | **read-time aggregation**: `AosAttributes.GetValue(Mobile, AosAttribute)` (`Misc\AOS.cs:621`) sums every equipped item; the shard already adds set bonuses there (`P\AOS-set-attribute-aggregation.patch`, hunk before the `BaseWeapon` branch) and pet-mimic attributes (`P\AOS-pet-mimic-attribute-aggregation.patch`). A third hunk adds our level bonuses. Resists: `Mobile.GetItemResistance` (our virtual, `P\Mobile-set-item-resistance-hook.patch`), overridden in `C\Mobiles\PlayerMobileSetResistances.cs`; add the level resists there | one hunk in an existing patch, plus ours | M |
| Weapon attributes (hit spells, leeches) and skill bonuses | read straight from `weapon.WeaponAttributes` all over `BaseWeapon` (`AosWeaponAttribute.GetValue`, `AOS.cs:976`, is not the only reader) | **out of scope by recommendation** (C.3): levels buy `AosAttribute` properties and resists only | 0 |
| Tooltip line ("Level 37, 1,204 / 3,050 XP") | `Item.GetProperties(IPropertyList)` is virtual (`Server\Items\Item.cs:874`) and overridden in `BaseWeapon.cs:2910`, `BaseArmor.cs:1265`, `BaseJewel.cs:376`, `BaseClothing.cs:702`, `BaseTalisman.cs:552`. No global property-list event (grep: 0 hits). One line per override calling our hook | **new patch, 4-5 one-line hunks** | S |
| Context-menu entry `LevelInfoEntry` added in four distro `GetContextMenuEntries` (A.5) | `Item.GetContextMenuEntries(Mobile, ref PooledRefList<ContextMenuEntry>)` is virtual (`Server\Items\Item.cs:2265`) and **none** of `BaseWeapon`, `BaseArmor`, `BaseJewel`, `BaseClothing` overrides it (grep: 0 hits); all four are `partial` (`BaseWeapon.cs:31`, `BaseArmor.cs:16`, `BaseJewel.cs:22`, `BaseClothing.cs:26`). So a `partial class` of ours can add the override with **no patch** (a subclass that overrides it and calls base still gets the entry; one that does not call base would not: check at build) | none | S |
| Gumps (level view, point spending) | pinned `DynamicGump`/`StaticGump` builders; shard gumps are the model (`C\ArtificersImbueGump.cs`, 1,782 lines, already lists every property with caps and slots) | none | M |
| Commands (`[levelinfo`-style, staff set-level) | `[ShardCommand]` (`C\ShardCommandAttribute.cs`) or pinned `CommandSystem.Register` | none | S |
| Config values (max level, XP table, points per level) | JSON through pinned `JsonConfig`, the P41 pattern (`notes\cc-P41-companions-research.md` row 7): shipped table plus a bind-mounted live override, a shard test that validates the table, and "log and keep the last good table" on a bad live file | none | S |
| Equip gate by level (ServUO: usually in `OnEquip`/`CanEquip`) | `Item.CanEquip` (`Item.cs:2251`) and `OnEquip` (`:3622`) are virtual but overridden by the bases; `PlayerMobile.ValidateEquipment` (`PlayerMobile.cs:1290-1306`) is the stock "drop what you can no longer wear" pass. **Not needed** under the recommendation in C.4 (dormant bonuses, never an unusable item) | 0 | 0 |
| "Is this crafted?" | `Item.PlayerConstructed` (`Server\Items\Item.cs:798`), set by the craft engine (`Engines\Craft\Core\CraftItem.cs:1455`, `:1749`); `BaseWeapon` also keeps `Crafter` (`BaseWeapon.cs:104-109`). Artifacts: `ArtifactRarity` (`BaseWeapon.cs:231`, `BaseArmor.cs:476`, both virtual, 0 for ordinary items) | none | S |

**Pinned patches this needs: one new (tooltips, 4-5 one-line hunks), one hunk in an existing patch (attribute
aggregation), and optionally one line in another existing patch (per-hit XP).** Everything else is ours.

### B.3 Where it collides with the shard's systems

| System | Collision | Resolution proposed |
|---|---|---|
| **P53: 200 cap, D-113 worn bonuses above the cap** | If levels bought `+Skill`, every levelable jewel would push skills past 200 by D-113 (`C\ClusterFSkillBonusAboveCap.cs:1`), straight into the effects P66 had to clamp (`C\ClusterFSkillClamps.cs`) | **Levels never buy skill bonuses.** |
| **P66 clamps and hook G** | Hook G reads `Cap + (Value - Base)`, so extra worn skill never stops a gain; no clash once skill bonuses are excluded | none |
| **P56 to P61 smith economy** | P56 raised Seal income a lot (its headline 3: small iron 10 regular 3 to 52 Seals); P57 tripled prices | A Seal fee for "make levelable" (C.1 option B) is a sink in the currency that grew. Fee numbers set against P57's prices at build time |
| **F-29 exceptional gap (x1.5)** | Chase: exceptional widens the gap | The level **budget** and each property's **ceiling** are x1.5 for exceptional (C.3) |
| **Imbuing** (`C\ArtificersImbueGump.cs`: per-property `MaxVanilla` / `MaxGuild` at `:185-330`, intensity cap 100 to 200 % by Artificer standing `:1766-1773`, 5 to 8 property slots `:1775-1781`) | Both systems raise the same properties on the same item | **One ceiling, both systems:** a property's imbued value plus its level bonus never passes that property's ceiling (C.3), and a level-bought property takes a property slot like an imbued one. Pinned jewellery has no quality (`BaseJewel.cs`: no `Exceptional`), so jewellery always uses the regular ceiling |
| **F-27 Self Repair rare** | a buyable Self Repair would undo F-27 | Self Repair is not on the level menu |
| **F-12 levels, loops, echo** | Gear "above the character's level becomes unusable" (F-12, 2026-09-30); level resets every loop | C.4: item level kept; bonuses above the wearer's level plus attunement go **dormant**; no echo for item XP (item level never resets) |
| **F-12 rule 16: XP for the act, damage-list credit** | Item XP must not double-pay a turn-in | Item XP only from combat (kill and damage), never from a quest turn-in or a currency; making an item levelable pays no XP |
| **F-26 Arms Lore attunement** (+5 levels at 100, +10 at 200) | Already decided for gear above level | Reused unchanged as the dormant-bonus margin |
| **Seals and Renown** | Renown is per account and League-only (`C\ClusterFAccountData.cs:516-524`) | C.1 option A pays Renown for the League quest once, not per item |
| **F-37 Client Commissions** | the overseer's note already foresees "a level on levelable gear" as a commission ask | Later: a commission can ask for "levelable, level 25+"; out of scope here |
| **Companions** (P41, P45) | companions are `BaseCreature`s; pinned `AosAttributes.GetValue` walks `m.Items` for any mobile, and melee uses the creature's `SetDamage`, not the weapon (P41 row 2) | C.2: companion gear earns XP; whether its bonuses act depends on P41's parity work (decision 6) |

---

## Part C: our design under the five rules

### C.1 How a crafted item becomes levelable

Eligible items, under rule 2: `PlayerConstructed` true and `ArtifactRarity == 0`, a weapon, armour piece, shield,
jewel or clothing piece (talismans: no pinned craft table makes one, grep of `Engines\Craft` for `Talisman`: 0 hits,
so they never qualify). Not eligible: anything found, bought, a reward,
an artifact, or a staff-made item (staff create sets `PlayerConstructed` false). Runic-crafted and imbued items are
crafted, so they qualify.

Three options:

- **A. A League quest, once per character, then per item at the League.** "The Bond" (working name): a short League job
  that teaches the character the rite; afterwards the League Registrar makes any eligible item they hold levelable for a
  fee in gold or Renown. Fits F-24 (League work) and pays Renown once (A.1 of P54: Renown pays for the job, never XP).
- **B. A guild process with a Seal fee.** At the crafter's guildmaster (Smiths for metal, Tailors for cloth and
  leather, later Carpenters and Fletchers for wood): hand over the item and Seals or the guild's currency, and it comes
  back levelable. A sink for P56's raised Seal income; ties levelable gear to the guild that made it.
- **C. A consumable a crafter makes.** A "Bonding Oil" (working name) made by a high-skill crafter (e.g. Tinkering or
  Imbuing 120+) from rare ingredients; the owner uses it on the item. Puts the gate in the crafters' market.

**Recommendation: A then C.** The quest makes it a goal ("a quest or a process", rule 2) and teaches the rule; the
consumable makes every later item a craft-economy purchase rather than an errand. B is the fallback if the League
contract engine is not ready when this is built.

### C.2 Where XP comes from (rule 4 and rule 5)

**One event: a creature's death.** At `CreatureDeathEvent` our handler reads the creature's damage list and pays item
XP. Paying at death from the damage list, not on each swing, is how rule 5 is met with no pinned patch: every hit by
every contributor (players, their pets, their summons, provoked creatures) is already in that list with its master.

**Credit (F-12 rule 16, damage list, not last hit):**
- A **contributor** is a player whose own damage plus the damage of everything they are `Responsible` for (pets,
  summons, provoked creatures; the `Responsible` sub-entries, `Mobile.cs:5911-5935`) is at least **10 %** of the
  creature's max hits. Pinned's looting rights merge damage the same way (`BaseCreature.cs:3344-3420`).
- **Each contributor's equipped levelable items each get the full award** (rule 4: every equipped levelable item gets
  XP, so a full suit levels with the weapon, not slower). Recommended over splitting by share: it matches rule 16
  ("kills credit everyone on the damage list"), keeps parties and pet users even with soloists, and the 10 % floor stops
  a one-hit tag.
- **A companion's own equipped items** get the same award when the companion is itself on the damage list (its own
  entry) or took damage from the creature (its damage list). Its master is credited separately through `Responsible`.
- **Weapon and shield**: paid if the wearer or anything they are responsible for damaged the creature.
- **Armour and clothing**: paid if the wearer **took** damage from the creature (`wearer.FindDamageEntryFor(creature)`),
  or dealt it. "On being hit", read at the death.
- **Jewellery and the rest**: paid on participation (either of the above).

**Award:** `item XP = creature level` (F-14: a mapping of Bard difficulty, `BaseInstrument.GetBaseDifficulty`,
`Items\Skill Items\Musical Instruments\BaseInstrument.cs:250`; until F-14 ships, that difficulty scaled to 1..200
directly). One number for player XP and item XP, as F-14 asks.

**Anti-farm rules** (each a single test in the handler):
1. Only `BaseCreature` deaths; never a player, never a creature with `GetMaster()` that is a player (no XP from your own
   or anyone's pets or summons, which also removes pet-killing farms).
2. **Blessed** targets cannot be damaged at all (`Mobile.CanBeDamaged() => !m_Blessed`, `Mobile.cs:5953`), so they
   never reach a damage list: covered by construction. **Paralyzed** targets cannot be tested at death: every hit clears
   paralysis (`Paralyzed = false` inside `Damage`, `Mobile.cs:5988`). A paralyze-and-beat farm is a farm of ordinary
   kills of creatures at a fair level, which rules 4 and 6 already bound; no separate rule proposed (decision 7).
3. Training dummies and archery buttes are items (`Items\Addons\ArcheryButteAddon.cs:9`, the dummies likewise), never on
   a damage list: no XP by construction.
4. **A floor: no item XP from a creature whose level is below `item level / 4`** (an item at 100 learns nothing from
   creatures under level 25). Keeps high items off trivial spawns.
5. No XP from summoned creatures (`BaseCreature.Summoned`, `BaseCreature.cs:485-489`) or creatures flagged
   `NoKillAwards` (`:1315`, pinned's own "no rewards for this kill" flag).
6. Per-item cap per minute (soft): at most N awards a minute, against AFK spawns stacked on one spot.

**Per-hit XP (decision 3).** Rule 5 says hits "as well as kills". Paid at death, a hit on a creature that dies within
2 minutes (the damage list expiry) earns its share even if someone else lands the kill; a hit on a creature that never
dies earns nothing. Paying on every hit instead needs one line in `P\AOS-damage-eater-hook.patch` and a hit-rate cap,
and opens a farm on anything that heals or cannot die (a healer's patient, a blessed or invulnerable NPC). Recommended:
death-paid.

### C.3 What a level gives

- **Points: 1 per level**, spent in a gump, on **AosAttribute properties and the five resists only** (not weapon hit
  effects, not skill bonuses, not Self Repair; B.2, B.3).
- **The ceiling per property** is the imbuing table's own number for it (`C\ArtificersImbueGump.cs:185-330`): an item's
  imbued value **plus** its level bonus never passes `MaxVanilla` on a regular item, `min(MaxVanilla x 1.5, MaxGuild)`
  on an exceptional one. Exceptional widens the gap exactly as F-29 does for materials.
- **The material sets the budget**: total points an item can hold = `level x material factor`, factor from the
  material's place in its chain (OSI's metals, woods, leathers in order, then the shard's tiers from
  `C\ClusterFMetalTiers.cs` and `C\ClusterFWoodTiers.cs`), a proposed linear 0.5 for Iron, plain wood and plain
  leather up to 1.0 for Celestial and Starwood; cloth items, which have no material tier, take 0.5, times 1.5 if exceptional. So an iron regular sword at 200 has 100 points to place, a
  Celestial exceptional one 300 (and still meets every property's ceiling first).
- **Cost per point varies by property**, so a point is roughly one imbue "intensity" step: the cost of +1 is
  `ceiling / 100` of a point-pool share (e.g. Luck, ceiling 100, costs 1 point per +1; Swing Speed, ceiling 30, about
  3.3 points per +1). This is the XmlLevelItems idea (points priced per property, A.3) put on the imbuing table's scale.
- **Slots**: a property the item does not have yet takes one of the imbuing slot cap's places (5 base; an item that is
  already at its slot cap can only raise properties it has).
- **Level 200 cap** (rule 1), as a config value. Nothing in the table above depends on 200, so raising it later is a
  config change plus the XP table's new rows.
- **Respec**: a paid reset of spent points (gold or Seals), never free; points come back, levels stay.

### C.4 Loop resets

F-12 (2026-09-30): "gear above the player's current level can no longer be used until they level back up". F-26 b:
Arms Lore lets a character use gear up to +5 levels above them at 100, +10 at 200.

Recommended for levelable gear:
- **Item level is kept through every reset** (it is the item's history, not the character's).
- **Item XP has no echo**: the item never re-climbs, so there is nothing to echo.
- **Bonuses go dormant, the item stays wearable.** Effective level = `min(item level, wearer's current level +
  attunement)`; the bonuses bought at levels above it are inactive (the registry stores points in purchase order, so the
  "first N levels' purchases" are well defined). The tooltip shows "Level 120 (acting 54)". Rule: the base crafted item
  (what it was before it was made levelable) is never gated, so a reset never strips a player bare.
- **Item XP is still earned while dormant**, but **an item cannot level past its owner's max level** (the loop cap), so
  a loop-0 character cannot farm a level-200 item they could not use.
- Companions: the companion's gear acts at its owner's current level plus the owner's attunement.

The alternative (decision 5): **item level is the equip requirement** (F-12 read literally). Then a level-150 sword is
unusable after a reset until 140 or 145, and an item at 200 is usable only from loop 21's capstone climb. That makes
high item levels capstone-only.

### C.5 Pacing estimate

**The live x1 gain rate does not touch item XP**: x1 is a skill-gain setting (`Configuration\modernuo.json`, cc-P54
A.2), and item XP comes only from kills (C.2). The rate that matters is kills per hour and creature level. Profiles as
cc-P54 A.2: **A** 120 kills an hour at own level, **B** 60 kills an hour at 75 % of own level.

Curve (proposed, a config table like F-12's S2): XP to next item level `n` = `13 x n^1.4`. Script (session scratchpad,
`p72\pace.py`), output:

| level | XP to next | total to reach |
|---|---|---|
| 1 | 13 | 0 |
| 10 | 327 | 1,201 |
| 25 | 1,178 | 11,685 |
| 50 | 3,108 | 63,206 |
| 75 | 5,483 | 168,615 |
| 100 | 8,202 | 337,676 |
| 150 | 14,470 | 897,156 |
| 200 | 21,646 | 1,793,054 |

Hours of hunting to item level 50, 100 and 200, by the level of creature hunted (every equipped levelable item levels
at this pace together, rule 4):

| creature level | A: 50 | A: 100 | A: 200 | B: 50 | B: 100 | B: 200 |
|---|---|---|---|---|---|---|
| 25 | 21.1 | 113 | 598 | 56.2 | 300 | 1,594 |
| 50 | 10.5 | 56.3 | 299 | 28.1 | 150 | 797 |
| 100 | 5.3 | 28.1 | 149 | 14.0 | 75.0 | 399 |
| 150 | 3.5 | 18.8 | 99.6 | 9.4 | 50.0 | 266 |
| 200 | 2.6 | 14.1 | 74.7 | 7.0 | 37.5 | 199 |

Reading it:
- A steady player hunting at level 100 gets an item to 50 in an evening (5 h), to 100 in about 28 h, to 200 in about
  150 h: under half of F-12's 334 h capstone (decided default), so a set of gear is a long goal inside the loop ladder,
  not beyond it.
- **The loop ladder slows it on purpose**: in loop 0 the cap is 50 and creatures hunted are about level 25 to 50, so item
  level 50 takes 10 to 21 h for A; past 50 the item waits for the owner's next loop (C.4).
- With full credit per contributor (C.2), a party levels at the party's kill rate, not a quarter of it. With a split by
  share, a four-player party would need 113 h to 100 at creature level 100 (computed in the same script), which is why
  C.2 recommends full credit.
- Unverified: the kill rates are cc-P54's modelling profiles, not measured play.

---

## Part D: a build plan

Order: after F-14's creature level (or with the Bard-difficulty stand-in), independent of F-12's player levels except
L5. Each batch builds with `docker\uo\build.sh` and ships its facts red-then-green.

| Batch | Contents | Size | Facts (shard test route) |
|---|---|---|---|
| **L1 Registry and eligibility** | `C\LevelItems\LevelItemRegistry.cs` (`GenericPersistence`, versioned payload, prune at save); eligibility (`PlayerConstructed`, not artifact, slot types); staff command to make an item levelable and set its level; JSON config with validation; the tooltip patch (new `P\LevelItems-tooltip.patch`, one line in each of five `GetProperties`) | M | save and load round trip; a deleted item's row pruned; a found or artifact item refused; a crafted one accepted; tooltip line present only on registered items; bad config rejected with the last good table kept. **Red:** registry off |
| **L2 XP from deaths** | `CreatureDeathEvent` handler; contributor rule with `Responsible`; armour on damage taken; companion gear; the six anti-farm rules; per-item level cap at the owner's max level (inert until F-12) | M | solo kill pays every equipped levelable item; pet kill credits the owner's items; summon kill likewise; a 5 % tagger gets nothing; own-pet and a player-owned creature pay nothing; dummies pay nothing; floor rule; armour paid only when hit. **Red:** handler unsubscribed |
| **L3 Levels and points** | XP table, level-up message in the System's voice, the spending gump, ceilings from the imbue table with x1.5 exceptional, material budget, slot rule, respec; the aggregation hunk in `P\AOS-set-attribute-aggregation.patch` and the resist branch in `C\Mobiles\PlayerMobileSetResistances.cs` | L | each property stops at its ceiling with and without imbuing on the item; exceptional ceiling x1.5 capped at `MaxGuild`; budget by material; the worn value moves by exactly the bought amount; unequipped item gives nothing; a skill bonus or Self Repair cannot be bought. **Red:** aggregation hunk removed |
| **L4 Making items levelable** | the chosen path (C.1: League quest plus consumable, or the guild Seal fee) | M | quest grants the rite once; consumable refuses ineligible items; fee charged once |
| **L5 Loops** (needs F-12) | dormant bonuses by effective level; Arms Lore attunement; tooltip "acting N" | S | at a reset the bonuses above level + attunement are off and the item stays equipped; back on when the level returns |

**Register lines it needs** (in the shapes they land in; drafted here, promoted by the overseer):
- `docs\fidelity-principle.md`, a new deviation (next free D-number): "Levelable crafted gear (ours; OSI has none).
  Crafted items made levelable by quest or consumable earn XP from combat and buy AosAttribute properties and resists
  within the imbuing table's ceilings. Reverses when: delete `C\LevelItems\` and the two patch hunks; registry rows
  orphan harmlessly." Plus one line for Item ID/Appraisal if it later reads item level (F-14).
- `docs\patch-backlog.md`: `P\LevelItems-tooltip.patch` (5 hunks, `BaseWeapon.cs:2910`, `BaseArmor.cs:1265`,
  `BaseJewel.cs:376`, `BaseClothing.cs:702`, `BaseTalisman.cs:552`), and the extra hunk in
  `P\AOS-set-attribute-aggregation.patch` (`Misc\AOS.cs:621`), alternatives argued in the L1 and L3 notes.
- `docs\feature-queue.md`: a new F-entry "Levelable crafted gear" pointing here, with Chase's five rules.

---

## Decisions for Chase

1. **Port the code or the design?** Recommended: **the design.** The code needs XmlSpawner's attach engine, breaks rules
   2 and 5 as shipped, and has a gold-farm and an unchecked gump (A.6); what is worth keeping (points priced per property,
   every worn item levels, a 200 default, XP from creature difficulty) is a page of rules, all in Part C.
2. **How an item becomes levelable** (C.1). Recommended: **A League quest once per character, then a crafter-made
   consumable per item**. Fallback: a guild Seal fee.
3. **Hits: paid at death, or on every hit?** (C.2). Recommended: **at death, from the damage list**: no patch, and a hit
   on a creature that dies within 2 minutes earns its share even if someone else kills it. Per-hit needs a line in
   `P\AOS-damage-eater-hook.patch` and opens farms on things that heal or cannot die.
4. **Credit per contributor: full or split by damage share?** Recommended: **full**, to every contributor with 10 % or
   more of the creature's max hits (their pets and summons counting as theirs), matching F-12 rule 16; split by share
   makes a party of four four times slower (C.5).
5. **Loop resets** (C.4). Recommended: **item level kept, bonuses above the wearer's level + attunement dormant, item
   always wearable; an item cannot level past its owner's max level.** Alternative: item level is the equip requirement
   (F-12 read literally), which makes high item levels capstone-only.
6. **Companions' gear:** recommended that it **earns XP now and its bonuses act** through the same aggregation (pinned
   sums any mobile's items). How much a companion's weapon matters depends on P41's parity work (melee uses `SetDamage`,
   not the weapon), so confirm that companions' levelable weapons are worth building before that work lands.
7. **Anti-farm list** (C.2): own and player-owned creatures, summons, `NoKillAwards`, a creature-level floor of item
   level / 4, a per-minute award cap. Recommended as listed; no separate paralysis rule (it cannot be read at death).
8. **What points may buy** (C.3). Recommended: **AosAttribute properties and the five resists only**, within the imbuing
   table's ceilings (x1.5 exceptional, never above the guild maximum), sharing the item's property slots with imbuing; **no**
   skill bonuses, **no** Self Repair, **no** weapon hit effects. (XmlLevelItems sells all three.)
9. **XP curve** (C.5): `13 x n^1.4` as a config table, about 150 h to 200 for a steady player at creature level 100.
   XmlLevelItems' own curve is quadratic, about 4.0 million XP at 200 (A.3), with XP per kill of the same order as F-14's
   creature level, so it would be several times slower. Playtest sets the number.
10. **Trade:** recommended that levelable items **stay tradeable** (crafted-gear market; the wearer-level gate in C.4 stops
    a high item helping a new character). Alternative: bind on first level.

---

## Unverified

- **Nothing was built or probed.** Every pinned behaviour here is read from source at `d4531cd94`, including that a
  `partial class BaseWeapon` of ours can override `GetContextMenuEntries` (no stock base overrides it, but a stock
  subclass that overrides it without calling base would hide the entry), and that the damage list still holds its entries
  when `CreatureDeathEvent` fires (pinned's own looting rights read it inside `OnDeath`, before the event at
  `BaseCreature.cs:3669`).
- **XmlLevelItems in a game:** none of the code-reading bugs in A.6 (gold farm, gump index, lost points, own-pet XP) was
  tested; they are readings of R. The forum bugs are as reported.
- The original 2011 zip and dracana's attachments could not be recovered (A.0); R and its three copies agree on the logic.
- **Pacing** uses cc-P54's modelled kill rates (120 and 60 kills an hour), not measured play, and assumes F-14's creature
  level lands on a 1-200 scale.
- The material factor (0.5 to 1.0), the 10 % contributor floor, the level / 4 creature floor and the point prices are
  proposals with no measurement behind them.
- Whether TazUO shows a long extra tooltip line cleanly on all five base types: not checked.

P72 DONE
