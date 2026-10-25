# P607: item identification and one Appraisal action

Written October 25, 2026, by the Golem's Codex lane. Design only. No code, client files, configuration, saves, or services changed. Nothing was built, deployed, or connected to Haven.

## Recommendation for Chase

Choose **Option B: shared discoveries with separate Appraisal and Arms Lore records**. New magic loot starts unidentified. Appraisal, the existing Item Identification skill under its P239 name, reveals magic properties. Arms Lore reveals armor resistances, weapon damage types, defensive properties, and physical condition. Learning one side does not unlock the other. A discovery stays with the item when it is traded.

Use the same Appraisal target for creatures and items. Keep P239's creature results. Add item results behind the existing skill callback. Offer a charged identification wand and a paid service at the existing League Appraiser. Crafted goods leave the crafter fully documented, including runic results. Existing goods keep their currently visible information when this system is introduced.

This follows the classic idea of finding an unknown magic item and identifying it. Extending that idea to AOS properties, splitting it from Arms Lore, staged discoveries, and a fee service are shard rules proposed here. They are not claims about historical OSI behavior. All numbers below are recommended starting values, not approved balance changes or measured estimates.

## What exists, checked against source

Source roots used below:

- **Code**: `D:\UO\golems\Valorite-tower\ShatteredLegacy`, HEAD `fcc658b` when read. Paths beginning `server/`, `client/`, and `player-package/` are in this work copy.
- **Notes**: this shard-migration work copy, HEAD `c24cc80` when read. P239, P226, P261, and P285 notes were read as context, then checked against current code.
- **Pinned**: `D:\UO\ModernUO-pinned`, verified HEAD `d4531cd94b739613155225c234900de9f47d2c88` with a clean working tree. Pinned paths below begin at its root. No generated `server/uo/` source was read.
- **Client snapshot**: `D:\UO\tazuo-sl-build\src\src`. This local source is readable but has no Git metadata at the inspected root. Its exact revision is unverified. The authoritative repository pin is `client/TAZUO_COMMIT`, `3212623f63436be1c0f4e3b308b202b29597c026`; snapshot observations below are labeled separately.

| Subject | Evidence and current behavior |
|---|---|
| P239 creature Appraisal | `notes/cc-P239-creature-levels-appraisal.md`; `server/customizations/ClusterFCreatureLevels.cs:354-393` renames skill 3 and handles `BaseCreature` targets. `Describe` at `:395` adds level at 30 and stats/resists at 60; the card opens at 90. It calls a skill check for gain but does not gate creature information on the check's result. |
| Entry point | `server/patches/ItemIdentification-appraisal.patch:1-15` intercepts only mobiles. Pinned `Projects/UOContent/Skills/ItemIdentification.cs:20-66` uses an eight-tile target, permits nonlocal targeting and player-vendor targets, and checks ItemID at 0 to 100 on `IIdentifiable` items. On success it sets `Identified`; on AOS it does not explicitly display an item report. |
| Existing identification field | Pinned `Projects/UOContent/Items/Weapons/BaseWeapon.cs:111-118` and `Items/Armor/BaseArmor.cs:84-89` serialize `_identified`. Their legacy single-click branches use it: weapon `:3158-3197`, armor `:1358-1372`; pre-UOTD weapon labels at `:3225-3235` also hide old magic adjectives. This is reusable compatibility state, not an AOS concealment system. |
| AOS tooltips | Pinned `BaseWeapon.cs:2910-3123`, `BaseArmor.cs:1265-1323`, `Items/Clothing/BaseClothing.cs:702-764`, and `Items/Jewels/BaseJewel.cs:376-396` append attributes, resistances and durability without an identification guard. **Setting `Identified = false` alone will not hide these properties.** |
| Identification coverage | Pinned `IIdentifiable` declarations are on the weapon and armor bases, with inherited implementations such as wands. Jewelry and clothing do not declare it. Our `server/customizations/Tutorial/TutorialTradeTrials.cs:605-619` also implements it on `TutorialCurio`; it must retain its lesson behavior. Do not assume the interface means every possible magic item is supported. |
| Identification wand | Pinned `Projects/UOContent/Items/Wands/IDWand.cs:10-44` starts with 25 to 175 charges, has zero use delay, directly identifies weapons/armor, and returns success for any item. `BaseWand.cs:294-304` consumes a charge when that handler returns true. Extending only the skill would leave a separate, incomplete route. The availability and abundance of these wands in this shard's actual loot/economy were not verified. |
| P226 Arms Lore | `notes/cc-P226-arms-lore-matters.md`; `server/patches/ArmsLore-field-maintenance.patch` adds maintenance after stock successful weapon/armor inspection. `server/customizations/ClusterFArmsLore.cs:103-141` repairs the user's damaged pack/worn gear, with a cooldown and possible maximum durability loss. Its other methods adjust crafting, wear, repair and gain difficulty. Pinned `Projects/UOContent/Skills/ArmsLore.cs:29-118` reports coarse condition, weapon damage descriptions and poison, or armor rating. It does **not** already provide Chase's proposed detailed AOS resistance report. |
| Gain above 100 | `server/customizations/ClusterFSkillGain.cs:403-430` uses material/quality/magic difficulty for Arms Lore. Its ItemID row currently accepts only a creature and uses creature level plus/minus 25. Item targets have no equivalent advanced gain row. |
| Loot generation | Pinned `Projects/UOContent/Misc/LootPack.cs:689-824` applies runic attributes to weapons, armor, jewelry and hats under AOS; its older branch assigns old magic levels. Slayer instruments also pass through this method. Hiding only weapons or only this method would miss other families and reward sources. |
| Crafted magic | Pinned `BaseWeapon.cs:640-684` sets `Identified = true`, then applies runic attributes and exceptional damage. Armor `:539-572` sets it before exceptional resist distribution. Pinned `Projects/UOContent/Engines/Craft/Core/CraftItem.cs:1454-1459` and `:1748-1753` stamp `PlayerConstructed` and invoke `OnCraft`. Final disclosure must happen after all craft customization, not at the first identification assignment. |
| Material and exceptional gear | `server/patches/BaseWeapon-exceptional-material.patch` and `BaseArmor-exceptional-material.patch` alter material readers; P226 changes exceptional crafting bonuses. A nonzero attribute is not by itself proof of a random enchantment. Material, quality and magic need separate classification. |
| P261 and P285 levelable gear | `notes/cc-P261-levelable-gear-build.md` and `notes/cc-P285-cont-fixup-levelable-gear-build.md`; current `server/customizations/LevelGear/ClusterFLevelGear.cs:222-277` saves a serial-keyed `GenericPersistence` registry. Bonuses are applied at read time (`:654-702`), and `AddTooltip` (`:707-724`) independently appends level, XP and bonus values. `LevelGearGump.cs:48-85` also shows names, slots and effective bonuses. The engine is for crafted gear; this is a separate disclosure path even though ordinary crafted gear should already be known. |
| Other custom properties and sets | `server/patches/Imbue-custom-property-hooks.patch:54-65` adds `Item.ExtraProperties` inside the base `Item.GetProperties`, not after all derived property builders. `server/customizations/Imbuing/ClusterFImbueEffects.cs:79-84` emits its custom property directly. `server/customizations/Items/Artifacts/Equipment/Armor/Sets/BaseSetWeapon.cs:199-236` adds set and absorption properties around the stock call. A return from the stock base builder cannot stop a derived builder from appending more. |
| Loot boxes | `server/customizations/LootBoxes/LootBoxRoller.cs:357-390` rolls runic gear and slayers. `LootBoxItems.cs:218-282` delivers contents to pack or bank and presents the reveal gump/flying loot. `LootBoxRoller.Describe` (`:477-496`) reads `Name`, `DefaultName`, or even the CLR type name. It does not currently enumerate stats, but those names can disclose an identity. Box opening must not count as identification. |
| Existing League Appraiser | `server/customizations/Requisitions/Appraiser.cs:175-208` already offers a free quote, an explanation and a matching requisition. `RequisitionItems.cs:384-409` computes and explains count plus intensity. The matching failure at `:329-343` can also name a property's intensity. These are information leaks if left available on unknown items. This NPC already buys magic items; its name does not mean it currently identifies them. |
| Shops | Pinned `Projects/UOContent/Mobiles/Vendors/GenericSell.cs:12-83` uses quality and old magic levels for prices, with no identification discount; `:99` returns the actual name or label. `Mobiles/Vendors/BaseVendor.cs:943-944` and `:1065` use those price/name providers. Player vendors use a separate `PlayerVendor.cs`/`VendorItem.cs` path and require their own review. |
| Shared tooltip cache | Pinned `Projects/Server/Items/Item.cs:850-864` caches one `ObjectPropertyList` per item; `:1917-1919` sends that buffer. `InitializePropertyList` (`:2584-2597`) calls the complete virtual property builder and parent additions before termination. `InvalidateProperties` at `:2608` rebuilds/updates the hash; it must not be called during a property getter. |
| OPL requests and labels | Pinned `Projects/UOContent/Network/Packets/IncomingEntityPackets.cs:154-190` and `IncomingExtendedCommandPackets.cs:350-382` send properties through the item. Pinned `Item.cs:4282-4297` uses the OPL header for an AOS single click, while `:4301` begins a different legacy label route. Both must agree with concealment. |
| Curses and traps | Pinned `Item.cs:1958-1970` and `:2362-2370` disclose `LootType.Cursed` independently of enchantment identification. `Projects/UOContent/Items/Containers/TrappableContainer.cs:18-28` stores actual trap state; `:67-72` executes it on opening. Neither field means a curse binds on equip. No general bind-on-equip mechanism was established by this investigation. |
| Client patches | Inspected the tracked patch set and changed-file targets from `client/patches/0001-enhanced-packet-client-command.patch` through `0007-animated-external-art.patch`, and searched the changes for tooltip/OPL handling. They add client commands, paperdoll options, shard buttons, map fog, skins, exhausted trees and external art animation. No item-identification filter was found in these patches. The Appraisal rename is a package data override at `player-package/payload/app/Build-UoOverrides.ps1:154`, not tooltip protection. |
| Local TazUO snapshot | `ClassicUO.Client/Network/PacketHandlers/MegaCliloc.cs:26-59` reads serial, revision and server property entries; `Game/Managers/ObjectPropertiesListManager.cs:26-50` caches name/data, raises an OPL event and updates its item database. `Game/UI/Tooltip.cs:59-62` and `:258-265` render that data. `ToolTipOverrideManager.cs` supports local formatting overrides. These observations explain why hiding rendered lines would leave their values available to scripts/database consumers. They do not establish the exact behavior of the shipped pinned binary. |

The source files above are the evidence inventory, not a claim to have audited every item type or every gump in the shard. This design does not quote a tree-wide item count from keyword matches.

## Player rules

### Two independent discoveries

Use two persistent public tracks on each supported item:

| Track | States | What it controls |
|---|---|---|
| Magic appraisal | Unidentified, Named, Values known, Hazards assessed | Magic identity, property names, magic values, charges/effect details, actual supported curses and magical hazards |
| Arms inspection | Uninspected, Assessed, Measured | Physical condition and durability, armor resistance values, weapon damage types, resistance-related effects |

An Arms Lore success can reveal the resist side while the item is still magically unidentified. Appraisal can reveal its magic while its resist side remains uninspected. This is the recommended interpretation of Chase's 11:36 split. Neither skill substitutes for the other just because an effect is stored in an AOS attribute collection.

Discoveries are permanent for the item's current property revision and are visible to everyone. A lower-skill buyer sees what a prior expert established. This supports player appraisal services and avoids a second client-specific tooltip cache for every viewer. A failed attempt never removes a prior discovery. Display current values at the unlocked stage rather than a stale numeric certificate.

### Which information belongs to which skill

| Information | Authority |
|---|---|
| Visible item family, amount, weight, handedness, ordinary use, access/quest restrictions | Public from the start |
| Magic title; damage/swing/spell bonuses; leeches and hit spells; stat and skill bonuses; luck; slayers; custom imbued effects | Appraisal |
| Armor's physical, fire, cold, poison and energy resistance values, including material, exceptional, enchantment and level contributions | Arms Lore |
| Weapon damage percentages, including elemental, chaos and direct damage where supported | Arms Lore |
| Resist bonuses, resistance caps, physical reflection and defensive absorption/eater properties | Arms Lore, with descriptions taken from their real readers. Do not call a delayed damage-eater heal immediate damage reduction. |
| HCI, DCI, Hit Lower Attack, Hit Lower Defense and offensive procs | Appraisal. These are combat modifiers, not elemental resistance values. |
| Physical current/maximum durability, wear condition, ordinary weapon damage range and speed | Arms Lore; generic base use/handedness can stay public |
| Magical durability enhancement, Self Repair, magical lower requirements | Appraisal. Actual condition is still Arms Lore. |
| Actual curse flags, magical trap presence and any implemented binding behavior | Advanced Appraisal hazard report; separate from physical resistance inspection |

Use a property catalog with an explicit owner for every supported property, including set, imbued and level bonuses. Do not classify by tooltip wording or by which C# collection holds a value. New properties need an owner before they become visible.

Intrinsic equip requirements should remain public enough to use an item. If an exact effective requirement exposes a hidden lower-requirements enchantment, show the base requirement while unidentified and explain failed equip attempts without printing the hidden bonus. Once that bonus is appraised, show the effective requirement. Race/sex, quest, account and transfer restrictions remain public at every stage.

### Names and example tooltips

On a new magic longsword, every client should initially receive:

```text
a longsword
Unidentified
Resistance and condition: uninspected
Weight: 7 stones
```

Do not send its current magic title, property count, intensity, rarity score, sell premium, or exact magic values in another hidden packet field. Use an explicit safe base-family label. `Name`, a custom `LabelNumber`, `DefaultName`, an inscription supplied by game code, and a CLR type name are not safe generic fallbacks. Preserve player engraving as quoted player text only if it cannot be confused with the server's appraisal certificate.

After names are learned, a possible report is:

```text
a longsword
Appraised traits: Hit Life Leech, Swing Speed Increase
Magic values unknown
Resistance and condition: uninspected
Hazards not assessed
```

After magic values and Arms Lore measurements are learned:

```text
a longsword
Hit Life Leech: 20%
Swing Speed Increase: 10%
Physical damage: 80%   Fire damage: 20%
Durability: 31 / 40
Hazards not assessed
```

The values above are illustrative. Only show the damage percentages and physical durability after Arms Lore measurement, regardless of the Appraisal stage. For a resist-only magic item, Appraisal may say its magic concerns resistance and direct the player to Arms Lore, without listing that track's names or numbers.

Unique art and material hue remain visible. An experienced player may recognize an artifact or infer a material from its appearance. Concealing tooltip properties cannot make recognizable art anonymous.

### Skill stages and the check

Use effective skill Value, as P239/P226 do, bounded to the shard's 200-point scale. Recommended item stages:

| Skill | Appraisal on an item | Arms Lore on gear |
|---|---|---|
| 0 to 29.9 | A quick supported-item check says "This item is not magic" or "You sense magic, but cannot identify it." No values or automatic identification. | Coarse visible condition from stock inspection; no exact resist or damage-type values. |
| 30 to 59.9 | On success, magic identity and Appraisal-owned property names, with values still hidden. | On success, broad resistance/damage-type descriptions and wear condition. |
| 60 to 89.9 | On success, exact Appraisal-owned property values and utility effects/charges. | On success, exact item resistance totals, damage percentages and current/maximum physical durability. |
| 90 and up | On success, assess the hazard types the item's adapter can actually inspect and open an item report card. | A detailed item report, including known defensive effect values and durability. Does not reveal Appraisal-owned magic or certify curses. |
| Above 100 to 200 | Harder magic can be identified reliably in the field; harder-item checks can train the skill. No extra property slots or stronger item stats. | Preserve P226's existing scaling for crafting, wear, repairs and training. |

These are floors for the amount of information, not promises that a 60-skill character identifies every artifact. For item magic only, use one difficulty-based success check per action. A successful check promotes to the highest requested attainable stage and includes its earlier stages. A failure gives "You cannot determine more" and exposes no next-stage clues. Do not roll once per property, and do not grant an extra gain for every line displayed.

For a tunable first model, normalize supported enchantments to their catalog ceilings. Let N be the number of distinct enchantments, including those assigned to Arms Lore, and I the largest intensity percent, clamped to 0 to 100. Start with `D = clamp(15 * N + 0.75 * I, 10, 175)`. Names use `max(0, D - 60)`, values use D, hazards use `min(175, D + 20)`, each with a plus/minus 25 success window and the stage's skill floor. An item must not become easier by concealing a property in another storage system. This formula needs a real-item spread and balance review before implementation, especially for artifacts and boolean properties.

An ordinary one-trait item at 20% has D 30, so a 60-skill appraiser can read its values. A five-trait item with a 100% trait has D 150, so it requires an expert. Known items can always be reread without another check. P239 creature information stays threshold-based and keeps its existing gain/check semantics; this proposal does not silently make creature reports fail.

### Mundane items, general items and hazards

Plain gear says **Uninspected**, not Unidentified. Quick Appraisal reports "not magic" without a random failure. It can still have physical properties worth Arms Lore inspection. Craftsmanship and ordinary material bonuses are not automatically random enchantments. Build classification from item type, material, quality, rolled attributes, slayers, custom stores and actual behavior. The existing imbuing and requisition catalogs are useful inputs, not a universal magic detector.

Use adapters for weapons, armor/shields, jewelry, clothing, spellbooks, wands, slayer instruments and trappable containers. Utility items can have magic appraisal without an Arms Lore track. Ordinary furniture/resources return a short ordinary-item description and "not magic" only when their type is covered by the classification rules. For an unsupported special item, say "You cannot assess this kind of item". Never certify it mundane or safe because the catalog lacks its effect. Keep labeled consumable use instructions and spellbook spell access usable; this is not a proposal to hide every item instruction or recipe.

At 90+, a successful hazard assessment can disclose an actual curse flag, a supported magical trap, or a binding rule if one exists. It never casts Remove Curse, executes a trap, opens a locked container, or removes a binding. "No magical hazard detected" is different from "safe to open": a dart or other mechanical trap remains Detect Hidden/Remove Trap work. An ordinary trapped chest can be nonmagical and dangerous at the same time. Appraisal must not replace those skills by revealing mechanical trap type, power, or disarm difficulty.

Do not create bind-on-equip curses in this task's follow-up by implication. `LootType.Cursed`, negative modifiers, quest nontransferability and a binding curse are separate things. Report only verified behaviors. A bind-capable item added later needs an adapter and its own approved design. Until a hazard adapter can inspect all relevant behavior, report the remaining uncertainty instead of "no curse".

Keep equip and combat effects working while unidentified. Equipping does not auto-identify the item. Stat changes, attacks and visible procs can let a player infer effects; absolute secrecy during use would require blocking equipment or changing combat/status packets, which this recommendation does not do. Give one clear acknowledgement before first equipping gear with unassessed hazards, rechecked against that item/revision. It must not claim that a binding curse exists. Existing public quest, blessed/insurance, and nontransferable restrictions remain public; optionally hiding the generic cursed loot-type label must cover every label route and is a separate Chase choice below.

## One Appraisal action and the alternative identification routes

Keep `SkillName.ItemID`, skill slot 3 and the existing Appraisal client rename. There is no new skill, skill-point pool or separate creature/item command.

1. Selecting Appraisal opens one target: "What creature or item do you wish to appraise?"
2. A `BaseCreature` goes through P239 unchanged. A player keeps the stock response.
3. An item goes through a shared item-appraisal service. Unsupported tutorial `IIdentifiable` targets retain their explicit existing handler, especially `TutorialCurio`; they are not accidentally swallowed by a generic "not magic" return.
4. An item card shows magic knowledge and a separate "Use Arms Lore for resistances and condition" section. It prints only already learned Arms Lore details. Arms Lore can similarly point to Appraisal for unknown magic. Opening a report card itself rolls neither skill.

Appraisal does not call the Arms Lore handler or perform field maintenance. Preserve P226's maintenance on an actual successful Arms Lore use, including its ownership, cooldown and durability-loss rules. Adding the new resistance report must not accidentally perform a second check, repair twice, or turn Appraisal into a way to repair gear.

Retain the existing eight-tile Appraisal target range for reachable/visible items. Require same map, line of sight where appropriate, and permission to view the actual container. A visible corpse item is eligible once the player may access it; a closed/locked container or someone else's bank is not. Keep public player-vendor inspection and visible trade inspection, with no gains there. Do not treat `AllowNonlocal` as blanket authorization to target any serial.

| Route | Proposed behavior |
|---|---|
| Skill, single target | One ItemID/Appraisal check, at least one second between item attempts, and the stage limits above. No reagent. Gains only through the limited rules below. |
| Identification wand | Use the same service and fully reveal the magic and supported hazard track, including jewelry/clothing/utility adapters. It does not measure resistances or physical condition. Consume one charge only if it increases knowledge; no charge for invalid, mundane, unsupported, already fully appraised or inaccessible targets. No skill gains. Preserve existing charge rolls initially; replace the zero-delay item use with the shared one-second limit. Balance wand supply after measuring real sources. |
| League Appraiser or configured mage | Extend the existing NPC service, rather than introduce a similarly named second Appraiser. Offer **Identify magic: 100 gold** and optional **Inspect arms: 50 gold** per supported item, fixed by the published service, independent of hidden stats. Identification certifies magic/hazards as far as the adapter supports; the arms service measures the other track. No fee for mundane magic checks or a track already complete. Other mage vendors opt in through the same service; Magery skill alone does not become an identification route. |
| Crafting | The maker knows the finalized craft, including random runic outcomes. Recommended shared-record interpretation: the finished craft is documented for everyone, with no appraisal skill check, fee or gain. Stamp actual crafter identity through craft completion, not the mutable maker-name string. |

For the paid service, present the item by its safe name and quote the fixed service price before payment. On confirmation recheck NPC distance/map, item ownership, item revision, knowledge and gold, then charge and reveal once. Follow the existing backpack ownership rule for a transaction. A stale reply cannot identify an item the player sold or charge twice. A nonmagic item can still be charged for a requested Arms Lore inspection, but never for the free "not magic" answer.

The current free price breakdown and "Which requisition wants this?" are not a free identification substitute. On unknown magic, show only the published blind-buy price and offer paid identification. Require the needed knowledge before detailed quotes, property-specific matching messages, imbuing, unravel previews, reforging and level-spending screens. Authoritative backend match/effect calculations can still read full values; their player-facing responses must not disclose them. A blind sale can be consumed without revealing properties to the seller. Requisition turn-in requires known magic and measured resistance information if the request specifically depends on that track.

## State, persistence and tooltips

### Store knowledge, leave the item intact

Use an additive `GenericPersistence` registry, following `LevelGearStore`, rather than replacing the base of every item family. Persist a format version, an adoption marker, and per-item rows containing serial, property revision, magic stage, Arms Lore stage, hazard coverage/revision, provenance and bounded gain-attempt flags. Store only discovery metadata. Preserve real attributes, effects, combat calculations, value calculations and actual trap state on their current objects/stores.

Treat knowledge as item-global. Do not put private crafter knowledge into the shared OPL. The crafted-item recommendation deliberately documents goods globally. Truly private maker knowledge belongs to Option C.

The old `Identified` field is a compatibility projection, not the authority: synchronize it when the magic values become known and route existing skill/wand assignments through the service. It cannot represent the two tracks or hazard coverage. Review other direct identification setters before implementation. Never infer "all properties and curses known" merely from an old true bit.

On delete, drop the registry/gain metadata; also prune dead rows on save. Duplication, staff copies, stack splits/merges and serial reuse need explicit rules and tests. A new item must not inherit an old serial's certificate. For any supported stackable magic items, merge only identical effects and knowledge, or prevent merging until their policies match. Do not manufacture appraisable training objects by splitting one stack.

### Put concealment before the full property builder

The recommended implementation seam is a small core hook in `Item.InitializePropertyList`, before its complete virtual `GetProperties`/parent-property chain. A core-owned delegate/interface can ask the content layer to supply the entire safe list for a managed item. The core cannot reference a UOContent appraisal class directly. If handled, do not enter the unrestricted virtual chain; still terminate/hash the resulting list normally. For managed known items, the policy renderer emits both tracks according to their stages. Unmanaged items take the normal path.

This central seam is necessary because a derived artifact can append properties after a stock base returns, and our `ExtraProperties` hook runs inside that base. The policy renderer needs explicit family adapters and the existing value readers for materials, sets, level bonuses and custom imbues. It must not just discard unknown cliloc numbers after building a full list, because arbitrary strings and names can contain values too. Unknown derived properties stay concealed until their adapter is reviewed. Keep indispensable parent/vendor/security metadata by adding only approved fields; do not invoke an unrestricted parent property builder from a concealed list.

Alternatives considered before proposing a core patch:

- **Set `Identified` only:** fails the observed AOS builders and does not cover jewelry/clothing.
- **Return early in each stock gear `GetProperties`:** derived set/artifact overrides and independent custom properties can append secret information afterward; this is not a complete boundary.
- **Use only `Item.ExtraProperties`:** it adds lines; it cannot stop later property builders.
- **Filter in TazUO:** full values still reach OPL scripts/database consumers, and other clients expose them.
- **Filter only `SendPropertiesTo`:** misses shared cache/header construction and other consumers. It also invites cache/hash mismatch unless every path is audited.

Keep the actual changes as small hook patches with the policy and adapters under `server/customizations/`. Preserve the pinned ModernUO layering and `apply-patches.sh` failure behavior. This is a proposed seam, not a verified working patch.

Also guard legacy `OnSingleClick`/equipment-info routes, including wand overrides and custom item labels, AOS OPL headers, shop packet names, the loot-box description/reveal and flying-loot producers, and item-specific report screens. Use one disclosure/name policy across them. Staff inspection gets a private diagnostic report; do not build a privileged shared OPL that a player can receive later.

Knowledge changes call `InvalidateProperties` outside getters. Both OPL hash announcements and subsequent property queries must represent the new safe list. Refresh open report/vendor/trade views after disclosure changes. A restart restores the same stages; moving an item into a container does not rebuild it as a fresh mystery.

### Changes to an item

Normal durability wear/repair updates known condition numbers and invalidates tooltips without requiring repeated magical identification. If an enchantment, damage distribution, set membership or hazard is added/changed, advance the corresponding revision and invalidate the affected certificate. Hazard checks expire on retrapping or a changed curse. The report must show "not assessed" for a new hazard rather than reuse an old clean report. Do not silently change a certified item in a pending trade.

For deliberate crafting/imbuing/reforging by its owner, keep the result documented after completion, including both affected tracks. These actions require the input's relevant knowledge first. A random or hostile change invalidates its affected knowledge. Never reset a training allowance merely because a player repairs, dyes, renames, levels, rerolls or re-imbues the same item.

Levelable crafted gear stays documented through transfers. Earning XP does not make it mysterious again. Spending a level point records the chosen change as known; Appraisal-owned bonuses remain on the magic side, resistance bonuses on the Arms Lore side. The report must include the effective capped contribution from the level registry, not just the item's stored AOS attributes. If a staff command deliberately creates unknown levelable gear, gate `[ItemLevel` and its responses so slots, ceilings and bought values cannot bypass discovery. This does not change XP, prices, caps or P261's eligibility.

## Trade, shops, banks and containers

- **Secure trade:** permit unknown items with prominent server-generated Unidentified/Uninspected labels. Both parties see the same record. Revalidate the item, knowledge/revision and price-dependent state, and clear both acceptances if anything changes, including appraisal during the trade. A player's sales description is not a server certificate.
- **Player vendors:** owners may sell unknown gear at a chosen price. Display unknown status before purchase and use safe names. A visible vendor item can be appraised with the skill under existing vendor-target permissions, making the discovery public, without training gains. Sale and movement never reset knowledge. Audit the separate player-vendor gump and child-property paths.
- **NPC blind sales:** unidentified magic sells for less through a published base-category price, initially 25% of the category's ordinary buy schedule. The offer cannot use property count, hidden rarity, intensity, actual slayers or concealed resistances. Validate the schedule below the minimum identified payout for each accepted family before launch; refuse unsupported families instead of secretly clamping to their real value. No blind buy/resell arbitrage should be introduced.
- **Known magic sales:** keep the existing property-based League Appraiser formula after identification, but withhold breakdowns and property-specific matching until that information is known. If the price depends on an unmeasured resistance, request Arms Lore/service first. Prices at confirmation use the same validated disclosure and schedule as the quote.
- **Merchant resale:** buying an unknown item into a merchant's inventory does not automatically identify it for free. If merchant certification is offered later, charge its published service cost in the resale price and make that an explicit separate purchase, not an implicit free quote.
- **Bank and containers:** moving, banking, nesting, death/corpse transfer, mailing where supported, and pack-versus-bank reward delivery preserve metadata. Access checks still apply. A report cannot enumerate unseen contents or reveal their properties through container totals/search. Owned bank contents may be inspected only through an actually open, authorized bank view. Paid services use the backpack transaction rule above.
- **Loot boxes:** mark rolled gear unknown before any content description/packet is produced. Opening a box, flying loot and a fanfare may reveal that an item is special but must not reveal an actual magic name or values. The outer box's known rarity/theme is not a promise that its contents have been appraised.

The blind price is intentionally coarse. Taking a fraction of the real hidden magic price would still reveal information and let players sort loot by free vendor quotes. Both ordinary shopkeepers and the existing League Appraiser need this rule, not just one NPC.

## Skill gain and why players would train it

Use the shard's existing earned-gain machinery. Successful identification does not grant flat skill points. Extend the ItemID gain route for eligible item work; preserve P239's creature route and P226's Arms Lore behavior. Verify the exact check kind/window and update its call-site verification when implementing, rather than assume the current `(0, 100)` row will accept the new difficulty windows.

For item Appraisal, recommend one gain opportunity per genuine loot item's discovery stage, shared across accounts, consumed by the first eligible attempt whether it succeeds or fails. Only grant it when that stage can teach the user's current skill, and only on an item they possess with legitimate access. The allowance is separate from the unlimited right to retry an identification check. A failed first attempt can still be retried to identify, but retries do not train forever. Persist the attempt bits so restarting or handing it to an alt cannot refill them.

Grant these opportunities only to gear stamped by verified loot/reward creation paths. Crafted, bought, staff-created, tutorial, already known, mundane and unsupported items provide no item gain. Wands, NPC services, report rereads, public vendor targets and trade targets give no gain. Mutation of the same object never refreshes its origin token or allowances. A per-account one-second action limit and the existing skill gain throttle apply in addition to the per-item limit; neither alone prevents a bag-of-swords macro.

Use the stage's difficulty window for the normal gain calculation. A specialist must handle new, harder finds to train above 100; easy loot stops teaching. Creatures already provide a way to begin training before the item-name stage. Existing creature-repeat gain behavior and any anti-macro coverage are outside the item-gain change and remain unverified here. This proposal does not claim to solve farming elsewhere in P239.

Appraisal earns its skill cost through free field identification, fewer wand charges and NPC fees, expert discovery on strong loot, hazard information, and P239's creature reports. It supports a party expert or town service character without requiring every fighter to buy the skill. Arms Lore retains P226's crafting, maintenance, repair and wear benefits as well as the newly assigned inspection detail. No direct damage bonus is added to Appraisal to make it worthwhile.

If this gain allowance feels too scarce after measuring drop volume, increase eligible new-item opportunities or add a finite NPC training lesson. Do not solve scarcity by allowing repeated rolls on one identified sword. Difficulty and allowance tuning require observed loot samples, not an assumption that current box and wand supply are balanced.

## Introduction, fidelity and verification plan

Do not retroactively hide the world. At the first authorized introduction, build and persist an explicit LegacyKnown record for supported items already in the world, including banked, vendor and unopened-box contents. Preserve all their currently public magic/resist information. Their hidden hazards are not newly certified safe. Items created after the adoption boundary default to concealed according to their adapters before they can send a label or OPL; crafting completion explicitly documents its output.

Do not use mutable item names, a naked `Identified` bit, or an unverified wall-clock `Created` timestamp to decide which objects are legacy. Adoption must happen after registry/world load and before accepting players or generating exposed rewards. Save the adoption marker with the registry. Once enabled, a missing/corrupt registry is an error to investigate, not permission to repeat grandfathering and reveal all new loot. Deleting the registry must not become an identification exploit.

Roll this out through a disabled-by-default server policy tested in a throwaway loopback instance. Disabling the feature restores ordinary display and cannot make a player forget information already received. Preserve metadata when disabled. Re-enable only with a defined policy for items exposed during the disabled period. No live save scan or deployment is authorized by P607.

Proposed fidelity entry for the overseer to promote if implementation is approved: "P607 introduces unidentified AOS magic loot and a separate Arms Lore inspection track. Appraisal, already the shard's Item Identification name, reveals item magic in stages; Arms Lore reveals resistances and condition. Discovered facts persist with the item. Paid NPC services, changed identification-wand coverage, documented crafted goods and blind-sale prices are shard-specific behavior." This note leaves `docs/fidelity-principle.md` untouched.

Future tests must each be seen failing against the pre-change behavior and then passing. The implementation acceptance set should cover:

1. Capture real OPL buffers, legacy equipment-info labels and AOS headers for unknown, named, appraised and inspected gear. Include jewelry, clothing, a derived artifact/set piece, wand, slayer instrument, custom imbue and level registry bonuses. Assert actual hidden values/names are absent, including before a malicious/raw property query.
2. Use two viewers with different skills and a staff observer. Check shared stages, changed hashes, already cached tooltips, private staff diagnostics, reconnect and registry save/load. Never let viewer order determine the public cache.
3. Exercise independent skill tracks at the stage boundaries and hard-item failure windows. Appraisal must not leak measured resistances; Arms Lore must not reveal leeches/slayers. P239 creature messages/card and `TutorialCurio` must still work.
4. Run real loot, box, craft/runic, reforge/imbue and level-point paths. Before publication, new found gear is unknown and finished crafts are known. Verify material/exceptional effects are classified correctly and level contributions are counted once.
5. Cover the free League Appraiser quote, price explanation, requisition match/failure, imbuing and level gumps, shop names and player-vendor child properties. Unknown information must not be inferable from a hidden-value-dependent quote or a detailed refusal.
6. Prove one gain opportunity is consumed per eligible origin/stage, including a failed attempt, trade/alt reuse, restart, split/merge and reroll. Repeated item reads must not call gain logic. Preserve the existing creature/Arms Lore gain regressions.
7. Confirm wand charge use and NPC payment are atomic, permission checked and idempotent on stale replies. Test no charge/fee for no-op magic checks, target movement/deletion and already known tracks.
8. Test secure trade acceptance reset; bank/container/corpse movement; unsupported-item uncertainty; actual cursed loot-type labels; magical versus mechanical traps; and expired hazard certificates after retrapping. Appraising a chest must not open or disarm it.
9. Test initial adoption with existing gear, missing/corrupt metadata after adoption, serial lifecycle, duplication, and disable/re-enable behavior. Use scratch saves only.
10. Observe the supported TazUO package and a client without shard patches in a loopback session. Check hover, journal, single click, open bank, vendor and trade refreshes. Client formatting can rearrange known data; it must have no hidden stats to retrieve. Older clients without AOS OPL get safe legacy labels and the server's Appraisal report. Skill names may still say Item Identification without the package rename.

Run the eventual code gate through `docker/uo/build.sh`, with the Golem's required locks and no live stack. Run any PowerShell checks through Windows PowerShell 5.1. P607 adds no tests and has no lane tests; these are requirements for a later implementation, not tests executed here.

## Three implementation choices

Effort means focused engineering days for one implementer, including red/green tests and loopback checks. These are planning estimates, not measured task costs or a release promise. None includes deployment or a new binding-curse subsystem.

| Option | Scope and tradeoff | Estimated effort |
|---|---|---|
| A. Binary identification | One shared magic known/unknown bit, a separate binary Arms Lore inspection, the common server disclosure boundary, all required leak closures, skill/wand/NPC routes and documented crafts. Easiest to explain; omits the progressive names/values/hazard experience requested in the brief. It still needs jewelry, derived-item and vendor coverage, so flipping the old flag is not a valid cheap implementation. | 3 to 5 days |
| **B. Staged shared discoveries, recommended** | The design above: independent staged tracks, explicit item adapters, public persistent discoveries, skill-based expert checks, guarded services and limited gain opportunities. Satisfies the requested progression and fits the existing shared OPL model. Its main cost is auditing every supported family/output path and maintaining a disclosure catalog. | 6 to 10 days |
| C. Personal knowledge | Each viewer, or account, knows different facts; the crafter privately knows their output; optional certificates convey knowledge to buyers. Requires viewer-specific OPL generation, cache/hash and header handling, transfer rules, and more legacy-client testing. Information can still be shared by screenshots or players, so privacy does not prevent knowledge transfer in practice. | 12 to 20 days |

For B, finish the disclosure policy/registry and a red leak test first, then the complete gear families and non-OPL outputs, then utility/trap adapters and economy/gain routes, then adoption and both-client verification. Keep the policy disabled until the whole supported surface is covered. Deferred special item types must return uncertainty and use an explicit concealment/exemption policy, not silently bypass the system. Do not publish a partially protected feature on the assumption the client will cover the holes.

The scope can be reduced by deferring new hazard mechanics or optional batch appraisal. It cannot be reduced by leaving the existing quote or derived-property leaks open.

## Questions for Chase, with recommended answers

These are design choices for review, not blockers to completing P607. No answer is treated as permission to implement or deploy.

| Question | Recommended answer |
|---|---|
| Should a discovery belong to an item or to each viewer? | The item, Option B. It stays known through sale, theft and bank moves. |
| Can Arms Lore expose the resist side before magic is appraised? | Yes. It is an independent track, matching the requested split. Appraisal never unlocks exact resistance or damage-type values. |
| Should every magic craft be known only to its crafter? | The crafter always knows it, and the completed craft is publicly documented. This avoids private OPL state and supports artisan sales, including runic goods. |
| Should new magic from loot boxes, rewards and artifacts also be unknown? | Yes for supported magic families, with safe family names. Box fanfare/rarity remains; it does not identify contents. Known consumable instructions/cosmetics are explicit exemptions. |
| What about existing equipment and old unopened boxes? | Preserve their public properties through explicit legacy records; do not make players pay to recover information they already had. Do not certify old hidden hazards safe. |
| Are 30/60/90 stages suitable on a 200 cap? | Yes as ordinary-detail floors; hard magic uses higher difficulty through 200. Measure a real loot spread before fixing the proposed formula. |
| Should the identification wand bypass skill? | Yes for magic and supported hazards, one charge only when it adds knowledge. It gives no resistance inspection or skill gain. Measure its actual supply before changing drop rates or charges. |
| Which NPC and what fee? | Add identification to the existing League Appraiser, 100 gold for magic and 50 for a separate arms inspection. Fixed fees, free mundane/no-op magic checks, and no free hidden-value quote. |
| Should unidentified items get a discounted real-value offer? | Use a published blind category price instead, initially 25% of the ordinary category buy schedule. A discount of the secret real value would still reveal it. Validate prices per family before launch. |
| Can players equip unknown gear? | Yes, with an acknowledgement for unassessed hazards and no auto-identification. Accept that use can reveal observable effects. |
| Do we hide `LootType.Cursed` and add curses that bind on equip? | Keep public death/transfer restriction labels for now and keep genuinely hidden hazards separate. Do not add a binding system as part of identification. If hiding that existing label is wanted, explicitly approve the behavior and audit every label route. |
| Does Appraisal find and remove all traps? | It can detect supported magical hazards at the advanced stage. Mechanical trap inspection/removal remains with Detect Hidden/Remove Trap. No appraisal action opens a chest or disarms anything. |
| How much repeat item training should be allowed? | One eligible opportunity per genuine loot item per discovery stage, consumed even on failure. Unlimited identification retries, no repeat gain, no new allowances from crafted or altered copies. |

## Verification and limits of this design pass

Verified by source inspection: the pinned revision and clean source tree; the stock identification and wand routes; the unguarded AOS property builders; P239/P226 hooks; the current level registry and its independent tooltips/gump; box generation/reveal names; existing Appraiser pricing/matching leaks; and the shared OPL construction path. The evidence table identifies the files read.

Unverified: live server state, actual wand/drop frequency, every derived artifact's override, every vendor/trade packet and administrative tool, the exact shipped TazUO binary behavior, packet captures, runtime cache refreshes, performance, serial reuse behavior under a new registry, the full item difficulty spread, fee affordability, and a general binding-curse mechanism. Those are implementation checks, not presumed working behavior. No code or live-client test was run for this design-only task.

The progress reporter completed with the two work-copy paths supplied through `SL_SHARD` and `SL_MIGRATE`. It was run with `--dry-run` and a process-local `Path.write_text` suppression because its current report builder still writes `tools/progress.json` even in dry-run mode. That suppressed write was observed. The reporter's existing review reminders remain outside P607; no progress, README, dashboard or decision files were changed.

Final review passed: the note uses American English, contains no em dashes or trailing whitespace, is below 5 MB, and includes the source findings, proposed rules, three options, recommendation, questions and verification limits. The code work copy is clean; this note is the only new or changed file in either work copy. Git whitespace checks passed. No decision document under `docs/` is changed. This pass adds no test files and runs no lane tests, as requested.

P607 DONE
