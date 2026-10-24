# P568: attunement for levelable crafted gear

Design prepared October 24, 2026. Notes only. No code or configuration changed.

Attunement limits the extra power bought with an item's level points. The item keeps its level, XP, purchases, and unspent points through a character's loop reset. It stays wearable under the ordinary equipment rules. As the character levels again, its higher bonuses wake up. Arms Lore provides the approved head start: five levels at 100 skill and ten at 200. There are no sockets.

This is a native extension of the existing LevelGear system. It needs real F-12 current and maximum player levels, a purchase ledger, and refresh calls when those inputs change. It is not an equipment-score system or a port of the third-party equip checks.

## Authority and evidence

Paths below use `S/` for this code work copy and `M/` for this migration work copy. `U/` means the read-only `D:/UO/ModernUO-pinned` checkout; its paths start below `Projects/`. Code was read at `1020e36a42d31dde07612544ea2a6f9472911db8`, also the main checkout's HEAD at `D:/ShatteredLegacy` when checked. Migration HEAD was `378c0ea6bd871aed26a1e5a87e23270b1be30796`. The ModernUO checkout and `S/docker/uo/Dockerfile:3` both identify `d4531cd94b739613155225c234900de9f47d2c88`. No fetch or branch change was needed. These are source findings, not claims about a deployed build.

The prompt's `notes/cc-P405-servuo-batch-1022-research.md` is not present. The actual research is [cc-P405-servuo-batch-1022.md](cc-P405-servuo-batch-1022.md). The completed prompt, `D:/UO/cc-prompts/completed/cc-P405-servuo-batch-1022-research.md`, names that destination. Read both, the P405 Codex review, and the overseer's recorded answers.

| Source | What governs this design |
| --- | --- |
| `D:/UO/overseer/decisions-2026-10-22.md:15-27` | Chase chose item-level attunement, the base item wearable, higher bonuses dormant, no sockets, and a proc purchase at a levelable milestone. Gear score remains an option only. |
| `M/testing/decisions.json:200-233`, P72-D5 through D7 | Keep item history; do not level items beyond the owner's permanent maximum; companions receive item XP and bonuses; retain the approved anti-farm requirements. |
| `M/testing/decisions.json:144-282`, P72-D1 through D10 | Native design, League unlock and crafted consumable, death-paid XP, full credit at 10 percent contribution, permitted properties, proposed item XP curve, and tradeability are recorded choices. Attunement does not revoke them. |
| [P72, C.4](cc-P72-level-items-research.md#c4-loop-resets) | Acting level is the lesser of item level and owner current level plus Arms Lore margin. Companion gear uses the owner's levels and Arms Lore. Item XP has no player re-climb echo. |
| `M/docs/feature-queue.md:2172-2185`, F-26 b | Chase approved +5 at Arms Lore 100 and +10 at 200. The later October 22 wearable/dormancy choice refines the older word "unusable." |
| [F-12 levels and loops](f12-levels-loops-caps.md), current/max/loop distinctions | Current level resets; permanent maximum follows 50, 100, then +5 to 200. Tier 1 newbie gear has no level requirement. Reserve credit can raise current level immediately after reset. |
| [P534 comparison](cc-P534-levelable-gear-design-vs-build.md), [P517 comparison](cc-P517-f12-numbers-vs-code.md) | Prior gap analysis, checked against the current files below. These reports do not establish implementation or runtime success. |

The third-party assessment is used through P405, as requested. Its `level-system-3` section describes `LevelEquipXMLDynamic.cs` and `ConfiguredEquipment.cs`: an attachment-driven score/equip gate, which is not this design. Its `equipment-level-requirements` section describes whole BaseArmor, BaseWeapon, and BaseJewel replacements with missing dependencies and a bad player cast. Its `xmlsockets` section describes direct attribute mutation and recovery. None should be copied. P72 C.4 is the useful design source. No third-party archive was opened, executed, built, installed, or newly verified here. Source behavior attributed to those downloads remains P405's research evidence. The intended implementation is original code in our existing layer.

Approved rules above are distinct from the implementation recommendations below. In particular, rounding between the approved Arms Lore anchors, which skill value to read, purchase allocation, and conversion of old records still need the decisions listed at the end.

## What players see

A player uses the existing `[ItemLevel` command and targets a carried or worn levelable item. The window shows the item's history and the power available to this wearer, for example:

```text
Longsword
Item level: 120 of 200
Your current level: 49    Arms Lore head start: +5
Acting level: 54
Your permanent maximum: 150

Property              Bought     Active     Dormant
Damage Increase          +12         +7          +5
Fire Resist               +4         +2          +2

Base crafted and imbued properties always work.
Higher level bonuses wake as your acting level rises.
```

The property amounts above illustrate a possible purchase history, not a proposed default weapon. The actual menu derives each amount from the saved ledger and the item's present property ceilings. It distinguishes bonuses dormant for level from bonuses limited by a property ceiling. Show the next purchase's required acting level and whether it will work now before the player buys it. Retain the existing price, available points, and shared property-slot display.

Attunement is passive. It costs no gold, consumable, cast, or maintenance charge. It adds no binding: a traded item uses the recipient's current level and Arms Lore. The original crafter and `MadeBy` field remain provenance, not authorization. Repair and player death/recovery retain the same item serial and progression record. Destruction of the item ends its progression under the existing lifecycle rules.

Reset confirmation should say, for example, "Your levelable gear keeps its progress. Its bonuses will act at your new level plus your Arms Lore head start." Preview the final reset result after any approved reserve credit and skill retention. Refresh once after the completed transaction. Do not present a temporary level-1 state as the final result if reserve credit immediately raises it. A failed or canceled reset changes nothing.

No new attunement requirement is added to OSI items, found gear, artifacts, ordinary crafted gear without a LevelGear record, or the newbie Tier 1 set. Existing strength, race, layer, expansion, and other equip requirements still apply. Attunement changes only the bonuses recorded by LevelGear; it does not turn off an item's ordinary damage, armor, imbued properties, set bonus, material bonus, or durability behavior.

The shared item tooltip must remain viewer independent. It shows stored item level, XP, bought totals, and "Level bonuses depend on the wearer. Use [ItemLevel." Do not put "your acting level" or an active amount calculated from the last viewer into `Item.ExtraProperties`. `U/Server/Items/Item.cs:850-874` caches the object's shared property list, and the current hook has no viewer parameter. Personal active/dormant amounts belong in the command's gump. Opening a backpack item's gump previews how it would act if worn; it does not apply its bonuses.

Extend the target rule to the owner's controlled companion gear. The owner may inspect and spend on a companion's worn item while the living companion is on the same map and within two tiles. Recheck control, distance, possession, and the exact item on every reply. Transfer, dismissal, removal of the item, or a stale reply must stop the purchase. Inspecting ordinary possessions keeps the current carry/wear check. Active accessory jewels use their real container owner and activity checks. This is ownership validation, not a permanent item bind.

## Numbers and evaluation order

Recommended formula, with integer acting levels:

```text
I = the item's stored level, normally 0 through 200
L = the responsible player's real F-12 current level
C = that player's permanent F-12 maximum level
A = clamp(player.Skills.ArmsLore.BaseFixedPoint, 0, 2000)
margin = floor(A / 200)
acting = min(I, L + margin)
earning ceiling = min(item.MaxLevel, LevelGearSettings.MaxLevel, C)
```

`BaseFixedPoint` is in tenths of a skill point. The recommended interpolation is one extra level per 20 trained Arms Lore, capped at ten. Use trained Base, not effective Value, for this feature. This avoids stat offsets, the Human racial floor, and temporary equipment bonuses changing the progression gate. This is a deliberate recommendation specific to attunement: existing Arms Lore crafting and upkeep formulas use Value and are outside this task. `U/Server/Skills.cs:174-203,231-268` verifies the distinction.

| Arms Lore Base | Head start | Current 1, item 120 | Current 49, item 120 | Current 195, item 200 |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | 0 | 1 | 49 | 195 |
| 19.9 | 0 | 1 | 49 | 195 |
| 20.0 | 1 | 2 | 50 | 196 |
| 99.9 | 4 | 5 | 53 | 199 |
| 100.0 | 5 | 6 | 54 | 200 |
| 199.9 | 9 | 10 | 58 | 200 |
| 200.0 or higher | 10 | 11 | 59 | 200 |

Current level and permanent maximum are separate inputs. A level-120 item at current 49, Arms Lore 100, acts at 54. Its stored level remains 120. A transferred level-200 item remains 200 even when the recipient's maximum is 50. It earns nothing while at or above that recipient's earning ceiling; it is not reduced to 50. The head start can activate existing gear a few levels above the owner's maximum because the approved activation formula is `L + margin`. It never raises that maximum or permits additional item leveling beyond it.

Resolve the responsible player as follows:

1. A PlayerMobile wearing the item uses itself.
2. A controlled companion or other controlled creature with a direct PlayerMobile master uses that player. A summoned creature with a direct player master uses the same rule if it can wear supported gear. Do not use the creature's own level, combat skills, con color, or former owner.
3. An unowned creature, a non-player master, or an unresolved/deleted owner supplies no attunement and receives no new item XP while the feature is enabled. The base item's properties continue to work. This closes release and transfer shortcuts without adding a creature progression system. Do not recursively chase arbitrary master chains.

Companion owner resolution follows P72 C.4. The extension to other player-controlled gear wearers follows the existing common BaseCreature readers and is an explicit recommendation. No new ability for companions or pets to equip otherwise invalid items is implied.

For each bought numeric property, first sum purchases with `UnlockLevel <= acting`. Then clamp that sum through the existing applicability and `a.MaxBuy(item)` ceiling logic. Add it to the item's ordinary contribution through the current aggregation hooks. Dormancy does not refund a purchase, free a property slot, change its price, or overwrite any item attribute. A ceiling-limited early purchase stays in its historical position; it does not fund or advance a later purchase.

Retain the current supported numeric property catalog. Attunement adds no STR/DEX/INT, skill bonuses, Self Repair, or unrestricted hit effects. The later milestone proc must store its own unlock level and test this same acting-level predicate before dispatch. P569 owns its milestone, effects, cost, and cooldown design. Do not silently choose those values here or treat an eight-point milestone payout as a proc.

## Define the first levels' purchases before changing a reader

Current state cannot answer which purchases came first. `S/server/customizations/LevelGear/ClusterFLevelGear.cs:207-219,260-309` saves `Bought` as property totals and `Points` as one balance. It has no purchase level or purchase-time price. Reading dictionary order cannot recover history.

For new points, recommend **funding by the earliest unspent level points**. Each level payout creates a funding lot with that item level and its actual point amount. A buy consumes the oldest lots first. Its unlock level is the highest level of any points consumed for that purchase. This makes "the first N levels' purchases" precise while allowing a player to save points and spend them later. Opening the menu at item level 120 does not automatically make a purchase funded entirely by level-10 points require 120.

Use the current source defaults only to illustrate this rule: four points at each ordinary level, eight instead at each tenth; Damage Increase costs five points for +1. These are in `ClusterFLevelGear.cs:58-60,117,398-401`. The example does not ratify the current quadratic XP curve, change P72's approved XP curve, or settle the wider point-budget review.

| Event | Funding consumed or retained | Purchase unlock |
| --- | --- | ---: |
| Reach item level 1 | Four level-1 points retained | No purchase yet |
| Reach level 2; buy +1 Damage Increase | Four level-1 points and one level-2 point consumed | 2 |
| Reach level 3; buy another +1 | Three remaining level-2 points and two level-3 points consumed | 3 |
| Save those same payouts until level 10 before buying | Consume the same oldest points in the same order | Still 2, then 3 |

At acting level 1 this example adds no level Damage Increase, at acting 2 it adds one, and at acting 3 it adds two. The ordinary weapon's own Damage Increase remains present throughout. A purchase is atomic: never activate a fractional Faster Casting point or skip an expensive early purchase to activate a cheaper later one. New purchases consume real points at their saved price, so price changes affect later purchases without rewriting old unlock levels.

### Proposed LevelGear store version 1

Keep GenericPersistence keyed by item serial. Add the following to each row, after the existing version-0 fields. The version-1 reader branches explicitly; do not infer the format from remaining bytes.

| Field | Contents and invariant |
| --- | --- |
| Unspent funding lots | Stable FIFO sequence of `(earned item level, point amount)`. Sum equals `Points`. Append the actual payout on every crossed item level, including multi-level gains. Coalesce adjacent lots at the same level. |
| Purchase ledger | Stable append order of `(property key, amount, unlock level, paid points, origin)`. A normal buy is +1 with its actual positive price. Adjacent identical entries may be combined without changing unlock level or total cost. |
| Origin | `Purchased` or `LegacyAggregate`. Serialize unknown legacy paid cost as the reserved sentinel `-1`, permitted only for that origin. It is not zero or today's price. |

`Bought` remains the stored aggregate used by slot checks and compatibility callers; verify that it equals ledger totals on load and after each transaction. Do not maintain two independent editable authorities. `Points` is the cached sum of funding lots. Make payout, FIFO debit, ledger append, aggregate update, and refresh one game-thread transaction. A rejected buy changes none of them. Reject nonpositive configured prices and negative payouts before mutation. Existing price/max/slot checks still apply, including when a purchased bonus will be dormant.

Do not persist acting level, owner serial, active bonus totals, or cached character maximums in the item row. They are derived from the current wearer. Keeping those out avoids stale trade power and save/reload drift. `MadeBy` continues to be the original audit field.

### Existing version-0 records

Recommended conservative conversion: preserve all recorded level, XP, maximum, points, provenance, and bought amounts exactly. Give each known positive aggregate one `LegacyAggregate` ledger entry with `UnlockLevel = stored item level`. Make the existing unspent point balance one legacy funding lot at that same level. Use catalog order for deterministic output, not as a claim about historical purchase order. Do not invent historical prices or reconstruct spending from today's rates.

This has a visible cost: a legacy level-120 item has its old bonuses dormant until acting level 120, then recovers all of them subject to current ceilings. It does not gradually reveal a fictional early purchase history. New points and purchases use the normal FIFO rule. A legacy unspent balance also spends with its recorded item level as the earliest known unlock. Show "Legacy purchases: unlock at item level 120" in the detail window. The normal player source for the current seal is still absent, but that does not prove there are no staff-created items or saved records. Do not assume an empty registry.

The data prompt must supply a read-only report over a supplied COPY of LevelGear data before activation: item serial/type, level, points, property totals, planned unlocks, and anomalies. Do not inspect or write live saves as part of this design or silently delete any record. Unknown keys remain preserved with an administrative warning. Negative balances/amounts, level-0 bought bonuses, inconsistent version-1 aggregates, unknown keys, and out-of-range unlocks require explicit repair or quarantine of that row before activation; report them rather than minting replacement points. A quarantined row retains its saved data but supplies no level-bought power and allows no new XP, point spending, or imbuing until resolved. Its ordinary item properties still work. This also prevents an unknown property from silently freeing a slot. Do not fail the entire world load because one row needs review. Unknown future store versions still fail loudly to prevent destructive downgrade reads.

A legacy purchase is not automatically eligible for a paid refund because its paid cost is unknown. A later respec prompt must decide that policy. Staff setters must preserve these invariants: raising item level alone mints no funding; lowering it does not refund purchases; explicitly assigning an unspent point balance replaces the funding lots with an audited lot at the assigned level. Existing purchases retain unlock levels. Out-of-normal-range staff fixtures are reported and excluded from ordinary player earning. Do not let `[LevelGearSet` leave `Points` and lots disagreeing.

Version-1 conversion is automatic on loading an old store and writing the next ordinary save, not a fresh world or item replacement. A data-only deployment can leave combat behavior unchanged while building the ledger. Never write the new version with an older writer. Rollback after the first version-1 save requires a version-1-aware build or restoration of the matched test save and build, not simply selecting an old image. This is a documented save-format constraint, not permission to touch a running stack.

## Where it belongs in our code

All proposed new filenames below are implementation destinations, not existing APIs. The existing files and behavior in the first column were read directly.

| Existing seam | Planned change |
| --- | --- |
| `S/server/customizations/LevelGear/ClusterFLevelGear.cs:207-312` | Version the existing state/store; add funding lots and purchases. A new additive `LevelGear/LevelGearPurchases.cs` can hold the record types and pure allocation helpers. |
| Same file, `AddXp:409-449`, `Buy:627-645`, staff setter `:740-769` | Write the ledger and lots at the existing mutations. Resolve the responsible wearer explicitly for XP. Keep the underlying award/share and XP curve fixes in their own prerequisite work. |
| Same file, `EffectiveBonus:654-663` | Split the stored/capped total from the wearer-dependent active total. Add an explicit `ActiveBonus(Mobile wearer, Item item, LevelGearAttribute property)` or equivalent. No runtime effect path may use the ownerless total as active power. |
| Same file, `AttributeBonus:666-683` | Use its already available Mobile argument. Keep `AOS-level-gear-attribute-aggregation.patch` as the dispatch seam. No new CanEquip patch is needed. |
| Same file, `ResistBonus:686-703`; `S/server/customizations/Mobiles/PlayerMobileSetResistances.cs:19-22`; `LevelGear/LevelGearCreatureResistances.cs:13-14` | Pass the wearer into the resist helper. Preserve the existing set-aware base contribution exactly. These additive overrides already sit behind `Mobile-set-item-resistance-hook.patch`; no new core resistance hook is needed. |
| `S/server/customizations/Accessories/ClusterFAccessories.cs:242-331` | Use `ActiveJewels`/`IsActive` for supported extra-slot jewels and include each eligible item's active level contribution exactly once. Do not count a smothered toe ring, locked slot, inactive jewel, or the AccessoryContainer itself as equipped gear. Resolve this existing integration gap before claiming all eligible jewelry works. |
| `S/server/customizations/LevelGear/LevelGearGump.cs:31-110`; engine tooltip `:707-724` and target `:772-795` | Replace the currently ownerless effective-value display with bought/active/dormant/ceiling-limited detail and personal context. Keep shared tooltip totals neutral. Recheck sender identity, possession, companion ownership, active accessory state, price, slots, and points on a reply. |
| `S/server/customizations/Tutorial/ClusterFLoops.cs:40-42,47-61` | The reset hook is empty today. F-12 must finish the real level/reset transaction and invoke attunement refresh after final level, retained skills, caps, and reserve credit are committed. |
| `S/server/customizations/ClusterFCreatureLevels.cs:41-76,98` | `IPlayerLevelSource` exposes only a level, and its current implementation is best Base combat skill. It is not sufficient for enforcement or the permanent maximum. Do not use it as a fallback. F-12 can separately replace the con-color provider. |
| `S/server/customizations/Companions/BaseCompanion.cs:238-248,251 onward` | Preserve companion skill-peak and weapon logic. Gear power uses the player owner. Owner level changes refresh already-equipped companion gear as well as the player's gear. |

Add `LevelGear/LevelGearAttunement.cs` for the pure acting-level calculation, owner resolution, and one F-12 adapter. Proposed adapter contract: `TryGetLevels(PlayerMobile, out currentLevel, out maximumLevel)`, readiness, and notification after a committed level/reset change. Bind it to the actual F-12 service when built; do not introduce a second player level store inside LevelGear. Validate `1 <= current <= maximum <= configured player maximum`. Use the actual service's names if they differ from this proposed contract.

Add `clusterf.levelGear.attunement.enabled`, default false while prerequisites are unfinished. On false, preserve the old power readers and existing item/global XP ceilings; data-ledger collection can still run without an F-12 provider. On true, enforce both acting level and the additional owner XP ceiling. An activation request must verify the real F-12 provider and row invariants before succeeding. Once enabled, an individual player with missing/invalid progression data receives no level-bought bonus and no new item XP, with one deduplicated administrative diagnostic. Do not silently fall back to skill-based level or grant full power. The UI reports "Attunement unavailable" and retains the item's history. A later valid login/record repair refreshes it.

Expose `armsLorePerLevel = 20.0` and `armsLoreMaxBonus = 10` under that same settings prefix with validated positive divisor and nonnegative cap. These are proposed defaults, not live settings. Configure changes must refresh affected wearers. Avoid adding a Shard Console button for this feature; if a later prompt adds one, it must include the mandated web twin and console fact.

### New XP limits

Evaluate the owner ceiling at the award, never at sealing time. When item level is below it, accept at most the XP remaining to that ceiling, after the existing award validation and caps. If the item already has higher level or XP, retain it and award zero. Do not accrue a hidden reserve above the ceiling or bank discarded XP for the next owner/reset. Reaching a higher permanent maximum permits future XP again. Dormant gear below the permanent maximum may continue earning normal item XP; the character's current level only limits active bonuses.

Calculate the remaining XP with the item engine's selected cumulative-XP table. P72-D9 chose `13 x n^1.4` transitions, while current `XpForLevel` is quadratic. Align that separately and do not bake either curve into attunement math. Likewise preserve the approved no-player-echo rule. Contributor qualification, anti-farm limits, presence checks, and the accepted obtainable seal are prerequisites for a public release, not new mechanics introduced by this note.

### Refresh the actual wearer, not just the menu

Resistances are cached: `U/Server/Mobiles/Mobile.cs:3109-3150` invalidates through `UpdateResistances` and otherwise reuses cached values. `MobileDelta` alone is not enough. A level loss, skill loss, transfer, or activity change must invalidate that cache before another combat read.

Use one game-thread helper to refresh the player and its affected gear-wearing followers. Call it after committed F-12 level/max/reset changes, an Arms Lore Base change that crosses a margin boundary, equip/unequip, accessory activation changes, ownership/control changes, item level change, purchase, staff edit, login/world load, and attunement configuration changes. Refresh the old and new wearers during a transfer. Clear/rebuild any in-memory owner-to-gear-wearer index on load and ownership changes; do not scan all world mobiles on every hit or every attribute read.

The helper calls `UpdateResistances`, queues Hits/Stam/Mana/status changes, and clamps current resources down to any reduced maxima through the normal setters. It never heals, restores mana/stamina, or removes ordinary gear. Rising maxima do not refill bars. Cover both PlayerMobile and the actual BaseCompanion resource readers. Opening a gump or reading a property must be side-effect free; it must not refresh, award points, invalidate properties recursively, or send diagnostic chat.

Prefer existing events and additive calls. The concrete exceptions needing targeted UOContent patches are:

- `U/UOContent/Mobiles/PlayerMobile.cs:3796`: add a call in the existing `OnSkillChange` override for Arms Lore. Another additive override would duplicate it; the base setter already calls this hook (`U/Server/Skills.cs:193`). Do not change other Arms Lore formulas or override a core skill setter.
- `U/UOContent/Mobiles/BaseCreature.cs:1158-1181,442-446,491-496`: capture the former owner before Master changes, then refresh/reindex after assignment and after the Controlled/Summoned change callbacks. Cached gear power must update on ownership loss as well as direct transfer. These are existing callbacks, not a new serialization field. Changing only the companion trade menu would miss staff setters, release, and summons.

Proposed patch files: `PlayerMobile-level-gear-attunement-hooks.patch` and `BaseCreature-level-gear-attunement-hooks.patch`, applied through `docker/uo/apply-patches.sh` against the fully patched pinned tree. Document alternatives in the implementing notes before writing them: polling leaves stale power between ticks; copying PlayerMobile/BaseCreature hides upstream drift; editing CanEquip misses already-worn gear and violates the wearable rule; a core skill event widens the surface unnecessarily. Use small dispatch calls and keep logic in customizations. Preserve the existing tutorial, quest-skill, follower, and companion hooks. Recheck these locations on a pin bump.

## Art, client, and release needs

No new art, item ID, animation, hue allocation, cliloc, map, packet, launcher feature, or client rebuild is required. The existing DynamicGump background/buttons and literal text support the view. Extend or paginate the existing menu so the added columns and notes fit the normal player window; do not make a screen-height list that clips the buy controls. No art request is needed because no new asset production is proposed. Do not generate art.

Check the gump in the supported player TazUO package, including a small window and a fresh login. A stock legacy-client smoke check is useful if that client is still supported, but its rendering is unverified here. The feature should work through ordinary server gumps and property lists. Verify that two viewers see the same neutral tooltip while their own previews differ. No client source work is a prerequisite for server enforcement.

This invented feature needs a shard wiki explanation, including the difference between current/max/item/acting levels, base gear preservation, legacy purchases, trading, and the companion owner rule. The implementing notes should provide the prose and the fidelity-register entry for overseer promotion; agents must not edit migration `docs/`. Website source changes can be prepared in a later authorized prompt. No Haven connection or deployment is part of this work.

## Tests to add during implementation

No tests were added or run for this documentation task. Every implementation prompt must first show each new regression failing against the previous behavior, then passing after the change. A first compile failure for a nonexistent API is not sufficient evidence of the behavior defect. Start with existing public readers or a minimal inert seam so the regression reaches its assertion. Run the shard gate with `docker/uo/build.sh` and a unique image tag, using the approved isolated test route, never a live stack. Any PowerShell harness or test runs in Windows PowerShell 5.1.

Proposed test file: `S/server/tests/Misc/LevelGearAttunementVerification.cs`, alongside the existing `LevelGearVerification.cs`. Add focused tests to the existing accessory/companion suites when those paths change. Save/load tests use buffers and scratch copies, not live save files.

| Behavior | Required evidence |
| --- | --- |
| Formula boundaries | Table above, inclusive unlock equality, item level 0, item below player level, and out-of-range Arms Lore. Effective skill/racial/stat changes alone do not change the Base-based margin. |
| Actual combat readers | Equip a crafted weapon with an ordinary attribute plus ledger bonuses and read `AosAttributes.GetValue`; prime armor/shield resist caches and read them after a real F-12 change. Prove ordinary properties remain and only eligible level purchases disappear. Do not test just the pure calculator. |
| Funding | Demonstrate the level-1/2/3 example, delayed spending, a buy spanning lots, multi-level payouts, price changes, and insufficient points. Ledger, bought totals, and unspent sum agree after every accepted/rejected transaction. |
| Legacy data | Use an actual version-0 byte layout; preserve every old field. Existing level-120 bonuses are inactive at acting 119 and restored at 120. Unknown keys and malformed rows follow the explicit report/quarantine policy. New format round-trips and a future version fails loudly. |
| Owner limits | Cap-50 wearer cannot grow an item to 51 even with a +10 margin. Transfer of a level-200 item retains all history and gives zero XP under cap 50. Dormant items below the maximum still earn; raising the maximum resumes awards without paying discarded XP. |
| Reset and reserve | Use the real confirmed F-12 reset with gear already worn. Final current level and retained/reset Arms Lore drive power; canceled reset changes nothing. Stats, item history, and base gear survive; reduced resource maxima do not leave excess current bars. Reserve may legitimately activate more bonuses immediately. |
| Companions and other owners | Use a real BaseCompanion, not just the existing horse test. Owner level/Base change refreshes its worn stats/resists. Transfer between players, dismiss/release, controlled/summoned flag change, and missing owner cannot retain the previous owner's cached power. |
| Extra accessories | Active extra bracelet gets exactly one bought contribution, ordinary backpack jewel gets none, and a toe ring becomes inactive when shoes smother it. Losing a slot refreshes cached effects. XP eligibility follows the same active item enumeration. |
| Ceilings and slots | Clamp active purchases after an item is imbued higher. Dormant and legacy purchases still occupy slots. Both imbue-then-buy and buy-then-imbue honor the shared slot ceiling. A level loss never opens another property channel. |
| Menu security and shared lists | Target/reply after item trade, removal, deletion, companion transfer, or range change does not buy. Invalid/hidden IDs and mismatched sender do not mutate state. Shared tooltip output is viewer neutral; personal gumps calculate for the correct prospective wearer. |
| Lifecycle | Repair, trade, player death/recovery, full isolated world save/reload, and re-equip preserve serial, level, XP, points, ledger, and provenance. Active effects are derived anew after loading. Turning attunement off/on refreshes caches and adds no points. |
| Proc boundary | When P569 adds a proc, use the shared acting-level test at dispatch and show it cannot fire below its saved unlock, including already-worn gear after reset. Dormancy UI alone is not enforcement. |

Material Luck and global wearer caps retain their own consumers. The existing material-Luck ceiling concern from P482 is not proven fixed by an attunement test; settle the per-item ceiling promise in the foundation prompt and test the selected behavior. Do not claim all scalar attribute consumers are validated merely because the aggregation test passes.

## Ordered Golem prompt plan

These are prompt specifications for the overseer to number and queue, not new task files. Each is independently stoppable and leaves the feature disabled until its dependencies work. Recheck merged fixes before authoring a prompt; do not repeat P427's already-landed pet-death correction. Do not deploy, commit, push, or edit migration `docs/` from these prompts.

### A. Finish the prerequisite F-12 progression contract

**Touches:** server

Complete the actual current/max-level service, committed-level/reset notification, login availability, and the real reset hook using the approved F-12 work. Reuse the existing progression build if already queued; this is a dependency, not permission for an attunement prompt to build an alternate F-12. Include reserve and retained-skill ordering. Expose an adapter usable by attunement and P570's tiles/mounts. Gate: actual level, maximum, reset, and cancellation tests fail first and then pass. A provisional skill-based provider does not satisfy it.

### B. Close the shared LevelGear release gaps

**Touches:** server

Use P534's source-checked backlog to align the accepted XP source/curve/contributor rules and anti-farm controls, shared slot counting, material-Luck policy, and active extra-accessory enumeration. Split this specification into separate numbered server prompts for XP and property/accessory work if needed; complete both before activation. Settle any revised point-budget table before ledger allocation defaults are finalized. Preserve item serials and ordinary properties. Gate: both purchase orders, active/inactive accessories, real death awards, helper ownership, and approved XP rules are observed failing and passing. Acquisition remains its own later player-release requirement.

### C. Build the versioned funding and purchase ledger

**Touches:** server

Implement version 1, FIFO point lots, purchase snapshots, and the explicit version-0 conversion/report. Update payout, buy, and staff mutation paths together. Keep activation off and the old power readers in service. Gate: real version-0 fixture, new round trip, exact balances, multi-level awards, delayed spending, invalid settings, unknown keys/versions, and the report. Record save compatibility and rollback limitations. Do not run a report against live saves without separate authorization.

### D. Apply attunement and owner XP ceilings through every reader

**Touches:** server

Implement the adapter, validated settings, owner resolution, active bonus helper, owner-aware resist path, and owner XP ceiling. Update ordinary and active extra-slot readers once each. Keep the switch off by default. Gate: formula examples plus actual attribute/resist reads, permanent-max XP boundaries, legacy unlocks, companion owner behavior, and dormant-slot accounting. Retain all stored progress on trade/reset. P569 may depend on this shared predicate but need not ship with it.

### E. Refresh live gear and finish the player view

**Touches:** server

Add the targeted PlayerMobile/BaseCreature refresh dispatch patches, their alternatives argument, and patch-runner entries. Wire F-12, accessory, equip, ownership, purchase, and load notifications to one refresh helper. Build the personal gump and neutral tooltip, including controlled-companion targeting. Gate: warmed resistance caches, resource clamps without refills, ownership loss/transfer, reset with reserve, stale replies, and lifecycle round trips. Show each new regression red before implementing its fix, then run the full build gate. The default remains off until the acceptance step.

### F. Accept in an isolated shard and prepare player documentation

**Touches:** server

Exercise C through E together using a throwaway loopback-only shard and scratch saves. Inspect a supplied copy of legacy data if authorized, resolve reported anomalies, enable attunement only in that isolated configuration, and run the manual player/companion/two-viewer checks above. Record exactly what was seen in a client and what remains unverified. Supply the wiki and fidelity-register prose in the notes for promotion. No production start/restart/configuration write is authorized. Gate: full build plus recorded client checks; production activation is a later Chase decision. Normal player release also waits for the approved League unlock/crafted-consumable acquisition path, not a staff-only seal.

P569's milestone proc implementation follows D and E and shares the saved unlock predicate, registry, and refresh rules. Paid respec is a separate prompt after a legacy refund policy is approved. No socket, gear-score gate, gate tile, or mount implementation belongs to these attunement prompts.

## Work performed and verification limits

Read both work-copy AGENTS.md files first, followed by the required direction, task list, governing-doc index, relevant fidelity/subsystem rules, P405 research and completed prompt, October 22 decisions, P72 recorded answers, F-12/P282 and subsequent comparisons. Read the canonical code files named above and the corresponding pinned engine seams. No `server/uo/` build-tree files were read. No agents were delegated, external messages sent, Haven connection made, or game/client/build process started.

The progress dry run completed. Its implementation writes `tools/progress.json` even with `--dry-run` (`tools/progress.py:722,737`); restored that incidental generated change byte-for-byte to the initially clean HEAD and separately called its read-only `counted()` function against this exact code work copy. This design does not publish a new backlog count or treat progress metadata as runtime evidence.

Only this note is intended to change. Lane tests are none. No new test or gate was created for this note; future test specifications above are not passing results. The proposed journal layout, migration report, F-12 adapter, refresh wiring, resource behavior, gump layout, and client compatibility are unimplemented and unverified at runtime. Legacy save contents and deployed configuration were not inspected. Final checks passed in Windows PowerShell 5.1.26100.9711: local source links resolve, the arithmetic examples match the formula, there is no trailing whitespace or em dash, and this note is below 5 MB. The code work copy is clean; the migration work copy contains only this new note. No stop request was present at completion.

## Questions for Chase

The main choices are settled: wearable base item, dormant excess bonuses, owner-based companion power, item history retained, owner maximum on new XP, tradeability, and no sockets. These questions settle implementation details. They do not block completion of this design.

1. **Should each 20 trained Arms Lore grant one extra acting level, up to ten, using Base skill?** Recommended: yes. It hits the approved +5/+10 anchors, is easy to explain, and cannot be raised by wearing temporary skill bonuses. Existing crafting/upkeep formulas continue to use their current effective skill rules.
2. **Should saved points fund purchases from their earliest earned levels?** Recommended: yes, FIFO funding lots and an explicit unlock level per purchase. Saving points for a later menu visit should not penalize the item's low-level usefulness. Do not substitute proportional scaling or fractional bonuses.
3. **How should aggregate-only existing items acquire unlock levels?** Recommended: preserve all progress and unlock each legacy aggregate and its unknown-age unspent balance at the item's recorded level. Report the affected rows and label the rule in the UI before activation. This is conservative but honest about missing history. Any alternate synthetic distribution needs an approved conversion rule; do not guess one from dictionary order.
4. **Should other player-controlled gear wearers follow the companion owner rule too?** Recommended: yes, using the direct current player master. Unowned or unresolved creatures get no level-bought power or XP while enforcement is enabled. This prevents a transfer/release shortcut and keeps one shared reader policy.
5. **May players spend points on a bonus that will be dormant now?** Recommended: yes, with its required acting level and current inactive status shown before purchase. Ownership, funds, slot limits, and item ceilings remain enforced. Spending does not unlock it early or refund it on the next reset.
6. **Should activation wait for real F-12, legacy review, and full isolated acceptance?** Recommended: yes. Collect the ledger first with enforcement off, then activate only against the real level service after the cache, transfer, reset, and client checks. The League/crafted-consumable source is additionally required before advertising ordinary player acquisition.

P568 DONE
