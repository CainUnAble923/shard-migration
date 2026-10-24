# P569: weapon procs purchased at a levelable gear milestone

October 24, 2026. Design only. No code changes.

Recommendation: at item level 100, a player can spend 100 of that weapon's points to choose Stormstrike or Emberstrike. Each has a 5 percent chance on a damaging weapon hit to deal 12 extra elemental damage, with a shared 10 second cooldown. A weapon holds one choice. Its proc goes dormant below acting level 100, while the weapon remains wearable. The defaults below are proposals for Chase to approve, not previously approved balance numbers.

## What Chase already chose

Chase's October 22 answer was "a milestone purchase on levelable gear (no accessory charms)." He also chose item-level attunement with higher bonuses dormant and the item still wearable, and rejected sockets. These choices are settled. This design supplies the missing weapon rules and numbers without reopening them.

Evidence and path corrections:

- The requested `notes/cc-P405-servuo-batch-1022-research.md` does not exist in this work copy. The actual report is [cc-P405-servuo-batch-1022.md](cc-P405-servuo-batch-1022.md), particularly lines 535-587, 710-750, and question 8 at line 1184.
- Read `D:/UO/cc-prompts/completed/cc-P405-servuo-batch-1022-research.md`. That is the research prompt, not an answered questionnaire. Chase's answers are in `D:/UO/overseer/decisions-2026-10-22.md`, the 09:26 and 09:35 entries. The 09:35 entry explicitly records the proc, attunement, and no-sockets answers. The October 23 log, including its October 24 continuation, was also checked for later changes.
- [P534 design versus build](cc-P534-levelable-gear-design-vs-build.md) identifies the unbuilt milestone feature and recommends level 100 as a starting proposal. It also identifies existing progression and property-accounting gaps. Those are dependencies, not evidence that procs already work.
- Read `D:/UO/cc-prompts/design/f-levelable-gear.md`, [P72](cc-P72-level-items-research.md), and the P72 decision records in `testing/decisions.json`. Crafted-only eligibility, companion gear, preserved item history, and dormancy remain binding. P72's earlier exclusion of general weapon hit-effect purchases gets this narrow, later-approved milestone exception. It does not become an unrestricted Hit Lightning point menu.

For the source references below, `S/` is this prompt's ShatteredLegacy work copy, `M/` is its shard-migration work copy, and `U/` is read-only `D:/UO/ModernUO-pinned`. Shard HEAD and the local `main` ref both read `1020e36a42d31dde07612544ea2a6f9472911db8` at inspection. Migration HEAD read `fb5878ee4efa0d2a02406cfe9f4bb348fdd8cd16`. This is a source snapshot, not a claim about the deployed server. No fetch was performed.

## What P405's source contributes

The third-party implementation is reference material through P405, as this task requests. I did not open, extract, execute, or independently recount that download. Its implementation details below are historical P405 findings, not a new verification of third-party code.

P405 describes Natfoth's Passive Item System as carried items with a default 5 percent chance and individual cooldowns. Its examples summon spirits, heal, strike with lightning, or create gold. It reports that the dispatcher calling the damage callbacks was absent, that each item's independent cooldown permits stacking, and that cooldowns used `Stopwatch`. Relevant reported files are `PassiveItems/BasePassiveItem.cs:17,113-136`, `LightningImpPassiveItem.cs:54`, `GoldFinderPassiveItem.cs:53,94`, and `PassiveDragonSpirit.cs:13-19`. P405 also reports no stated license.

Borrow the chance-and-cooldown idea, not the package. Write native code in our gear system. There are no copied passive item classes, backpack scans, XmlSpawner attachments, gold payments, or proc summons. Healing and spirit summons can receive separate designs later. A summoned spirit would also overlap Chase's separately approved League reward, Echo of X, so it should not arrive through a gear proc by accident. No third-party runtime dependency or new art is required.

## What exists in main

These are findings from source, not from file names alone:

| Source | Verified behavior and design consequence |
| --- | --- |
| `S/server/customizations/LevelGear/ClusterFLevelGear.cs:39-85,206-312` | Settings and a `LevelGearStore : GenericPersistence` already exist. Item state is keyed by serial. Store version is 0, with aggregate purchased-property values. Add proc state here through a versioned extension, not fields or a new ancestor on every weapon. |
| Same file, `:328-380` | Sealing requires a player-constructed weapon, armor, shield, or jewel with zero artifact rarity. Procs narrow this to `BaseWeapon`. They do not widen sealing eligibility. |
| Same file, `:387-445` | Current progression starts at level 0, pays 4 points per level and 8 instead on every tenth level, and uses cumulative XP `100 * (level + 1)^2 - 100`. Proc unlock is separate from the every-ten-level bonus-point rule. |
| Same file, `:568-650` | Gear spending counts stored imbuing properties plus level-only properties, uses the base slot limit, and never writes level bonuses into the item's original attributes. Proc spending must follow the same separation. |
| `S/server/customizations/LevelGear/LevelGearGump.cs:31-110` | `[ItemLevel` has a spending menu and checks possession again on reply. Add a separate milestone page and a confirmation response with the same server-side checks. |
| `S/server/customizations/ArtificersImbueGump.cs:328-343,799-807,1012-1021,1797-1816` | Imbuing already offers Hit Magic Arrow, Hit Fireball, and Hit Lightning. Its UI and mutation path count stored properties only. The known reverse-order slot hole must be repaired before a proc can reserve a shared slot reliably. |
| `S/server/customizations/Imbuing/ClusterFImbueKnowledge.cs:214-229` | Imbuing has account-dependent Master Formulary slot or intensity allowances. Preserve those allowances; do not replace them with a universal five-slot cap. |
| `S/server/customizations/Imbuing/ClusterFImbueEffects.cs:364-381` and `S/server/patches/Imbue-custom-property-hooks.patch` | The existing weapon-hit custom-imbue callback serves Time Slip and Shatter, accepts players only, lacks the actual weapon and `damageGiven`, and runs after the weapon ability callback. Calling procs from it unchanged would lose companions and include unsuitable hits. |
| `S/server/customizations/Companions/BaseCompanion.cs:35,199` | Companion equipment uses a `BaseCreature` subclass with a control master. Resolve the player owner for attunement and cooldown sharing; the companion remains the actual damage source. |
| `S/server/customizations/ClusterFCreatureLevels.cs:41-78,98` | The con-color player level source is explicitly provisional and based on combat skills. It is not the actual F-12 player progression service. Do not ship proc dormancy against that substitute. |
| `S/server/customizations/Tutorial/ClusterFLoops.cs:30-42` | The loop ladder exists, but `ResetLevelAndSkillsForF12` is empty. A search of canonical customizations and patches found no replacement for the provisional `IPlayerLevelSource`. Actual reset integration remains a prerequisite. |
| `S/server/customizations/LevelGear/SmithsSealDeed.cs:1-5,31-70` | The sealing consumable exists but its normal acquisition path is absent in this snapshot. A proc menu alone will not make levelable weapons obtainable by players. |

Pinned engine facts were checked at `d4531cd94b739613155225c234900de9f47d2c88`, matching `S/docker/uo/Dockerfile:3`:

- `U/Projects/UOContent/Items/Weapons/BaseWeapon.cs:1732` is the weapon `OnHit` implementation. Its physical strike calls `AOS.Damage` at line 1993. The branch beginning at line 2009 only runs when `damageGiven > 0`. Ordinary weapon spell effects run inside that branch at lines 2152-2180. Creature and ability callbacks follow at lines 2205-2209.
- `U/Projects/UOContent/Items/Weapons/Ranged/BaseRanged.cs:105-133` calls `base.OnHit`, so the shared base hook reaches bows and crossbows. `U/Projects/UOContent/Items/Weapons/Throwing/BaseThrown.cs:7,113-121` derives from `BaseRanged` and its `OnHit` also calls the base implementation. These inspected files match the pinned Git tree without local changes. `U/Projects/UOContent/Items/Weapons/Abilities/DoubleStrike.cs:10-58` makes a second swing through the weapon; it is another strike, not a damage-event callback. The same directory's `WhirlwindAttack.cs:74` calls `weapon.OnHit` for additional creatures, so the primary-combatant filter below is necessary.
- `U/Projects/UOContent/Misc/AOS.cs:34,47-55,234-240` supplies elemental damage with an explicit source and returns applied damage. It also invokes standard leech logic at line 236. Using it preserves ordinary mitigation, attribution, and that existing interaction; it is not a promise of a completely isolated damage pipeline.
- `U/Projects/UOContent/Items/Weapons/BaseWeapon.cs:3362-3437` implements native hit spells, including their own damage calculations. Do not call `DoLightning` or `DoFireball` for a fixed 12-damage custom effect. Their visuals can be reused separately.

## Player experience and numbers

An eligible player seals a crafted weapon through the existing gear process, levels it, and opens `[ItemLevel`. The weapon's Milestone page is visible before level 100 and explains what remains. Reaching 100 unlocks the purchase; it does not grant a free proc or spend points automatically.

Recommended first-release rules:

| Rule | Proposed default |
| --- | --- |
| Eligible gear | Sealed, crafted, zero-rarity `BaseWeapon`, excluding `Fists`. Includes melee weapons, bows, crossbows, and `BaseThrown` descendants that retain the inspected base hit path. |
| Unlock | Item level 100; one proc selection per weapon; no second selection at 150 or 200 |
| Price | 100 unspent item points, paid once on confirmation; no gold, Seals, essence, or new consumable cost |
| Point budget reference | Current level 100 earnings total 440 points: 90 ordinary levels times 4 plus 10 milestones times 8. Price is about 23 percent of those earnings. Current cumulative XP at 100 is 1,020,000. These are current-code arithmetic, not a promised progression curve or time estimate. |
| Property cost | One distinct property slot, retained while dormant or globally disabled. In imbuing intensity mode it also reserves 100 percentage points of Full intensity. |
| Chance | 500 out of 10,000, or 5 percent, per eligible damaging weapon strike |
| Cooldown | 10 seconds after a successful roll; shared by a player and that player's companions, and also recorded against the triggering weapon |
| Stormstrike | 12 raw energy damage to the struck creature, with normal resistance and standard damage rules |
| Emberstrike | 12 raw fire damage to the struck creature, with normal resistance and standard damage rules |
| Scaling | Fixed damage. Item quality, material, item levels above 100, spell damage increase, weapon damage increase, ability property multipliers, and Luck do not raise this raw amount or chance. Target mitigation and existing AOS interactions still apply. |
| Combat scope | PvE only for the first release. No player, player-owned pet, companion, summoned creature, invulnerable NPC, or `NoKillAwards` target. |
| Replacement | Choice is permanent in this first release. A future paid respec may support changing it using saved purchase-time costs. No free swap, refund button, or point grant is added here. |

Stormstrike and Emberstrike are alternative damage types with the same price and strength. They are custom milestone effects, visibly named separately from ordinary Hit Lightning and Hit Fireball. An existing imbued hit spell may coexist and roll on the original strike. Its property is separate; neither its chance nor the milestone's chance is added to the other.

Before purchase, show: `Weapon milestone: level 100`, `Choose one effect`, `Cost: 100 item points and 1 property slot`, and each effect's chance, raw damage type, cooldown, and PvE restriction. At level 99 the button is disabled with `Reach item level 100`. With too few points or no spare slot, explain that exact reason. Armor and jewelry show no weapon milestone purchase buttons.

Selecting a choice opens confirmation: `Bind Stormstrike to this weapon for 100 item points? This choice is permanent until a paid respec is available.` Display the live remaining points and occupied slots. A player may buy on an earned level-100 weapon while its proc would be dormant for that player; show that dormant status before confirmation. The item milestone, not the wearer's current level, qualifies the purchase. A stale confirmation must recheck everything and fail without spending anything. Success sends one message: `Stormstrike is bound to your weapon.`

After purchase, the menu shows the saved effect, its saved unlock, current active/dormant status, and the owner's shared cooldown remaining. Do not resend a gump or invalidate tooltips every combat tick. Tooltips show stable public facts, for example `Milestone: Stormstrike (requires acting level 100)` and `5% on a damaging weapon hit; 10s shared cooldown; PvE`. The wearer-specific menu shows `Dormant: acting level 95 of 100 required`. Item property lists are cached and shared, so never put a viewer-specific acting level or ticking cooldown in a common tooltip.

For pacing, ignoring cooldown, 20 eligible hits is the expected wait for a 5 percent roll, not a guarantee. At one eligible hit each second and continuous combat, a success followed by a 10 second cooldown gives an average interval of about 29 seconds, or about 0.41 raw extra damage per second. The exact result depends on strike timing and encounter downtime. Fast weapons and Double Strike get more attempts. No damage-per-minute normalization is proposed for this first release. The cooldown puts a hard ceiling on successful frequency even when several companions contribute strikes. These are modeled values; combat balance is unverified until measured.

## Attunement, transfers, and helper rules

Use the shared acting-level service from the F-12 and P568 attunement work. Its contract is `min(item level, player current level + Arms Lore margin)`, with the accepted margins of +5 at Arms Lore 100 and +10 at 200. P569 does not choose interpolation between those thresholds or implement another player-level reader. P568 owns that detail and the aggregate-to-ledger conversion for ordinary property purchases.

The proc records `RequiredActingLevel = 100` when purchased. It activates only if the current acting level reaches that saved threshold. A level-150 weapon on a level-95 wearer with the +5 margin can proc. At wearer level 94 with the same margin it cannot. The weapon stays equipped, and its original crafted or imbued properties continue under their existing rules.

Buying late does not raise this particular unlock: a player buying the milestone at item level 150 still gets the level-100 proc. Save the actual purchase level for history, but keep required acting level 100. This is an explicit milestone rule for Chase's review. It differs from assuming every purchase requires the item's level on the day the button was pressed.

On a loop reset, change no proc choice, item level, XP, points, or raw weapon property. Recompute eligibility against the wearer's new acting level on every attempt. The proc returns automatically when the wearer again meets 100. A missing real player-level service means dormant and purchases unavailable, not a fallback to combat skill. The feature remains disabled until its dependencies pass their gates.

Transfers keep the item choice, saved unlock, and purchase history. Attunement belongs to the new wearer. The League sealing unlock, when built, is checked when sealing; this design does not add a second quest requirement to using a legitimately traded sealed weapon. A staff dupe with a new serial does not inherit another serial's proc row. Repair and insurance recovery of the same serial retain it; deleting or destroying the weapon leaves no redeemable proc essence.

For a companion strike, the attacker must be a controlled `Server.Companions.BaseCompanion` whose `ControlMaster` is a living player. That owner must be online, on the same map, and within 18 tiles. Use that player's acting-level allowance and cooldown. The weapon must actually be equipped and be the companion's current weapon. Other pets, summons, provoked creatures, and wild humanoids do not gain this player progression benefit by holding an item. Resolving the owner never changes the damage source: call damage with the companion as `from` so the engine's existing responsible-master accounting handles credit. Normal follower limits remain in force.

## Combat dispatch

Add a focused `BaseWeapon-level-gear-proc-hit.patch` in `S/server/patches/`, applied by `S/docker/uo/apply-patches.sh` after existing patches that touch `BaseWeapon`. Its single call belongs at the end of the `damageGiven > 0` branch, after ordinary hit properties and before `bcAtt.OnGaveMeleeAttack`, `bcDef.OnGotMeleeAttack`, and ability callbacks. Pass `this`, `attacker`, `defender`, and `damageGiven` to the new service.

This is a UOContent patch. No ModernUO core edit, full-file replacement, or damage-method copy is needed. Generate it against the assembled pinned tree after the earlier weapon patches, with `--fuzz=0`. Recheck the exact insertion against all current patches during implementation; the line numbers above describe pristine pinned source. Add it to the existing patch reconciliation notes for the next pinned-commit bump.

The service does these steps on the game thread:

1. Return immediately if gear or procs are disabled. Resolve the proc row by the supplied weapon serial. Do not enumerate inventory or all saved rows.
2. Require the attacker and weapon to be alive/not deleted as applicable, the weapon directly equipped by the attacker, and `attacker.Weapon == weapon`. Recheck crafted, zero-rarity, non-`Fists` weapon eligibility and require positive `damageGiven`. Never infer a weapon from damage delivered by spells.
3. Resolve the eligible player or companion owner and real acting level. Require the saved unlock, a recognized enabled proc choice, and valid owner presence. Unknown choices remain saved but inactive.
4. Require a living, nondeleted wild `BaseCreature` target with no player control or summon ownership, no invulnerability, and no `NoKillAwards`. Require the supplied defender to be the attacker's current combatant, on the same map, in the weapon's legal range and line of sight, and still allowed by `CanBeHarmful(defender, false)`. This also rejects a redirected clone or secondary ability target. Recheck after native hit spells, which may already have killed the creature.
5. Require `now >= ownerNextProcAt` and `now >= weaponNextProcAt`, and no proc execution already in progress. Read UTC `Core.Now` through an internal testable clock. Ineligible attempts and cooldown attempts draw no random number.
6. Draw exactly one `Random(10000)` for this strike; values below 500 succeed with defaults. Misses do not start cooldown. Double Strike's second successful physical strike may make another attempt if the first did not proc. Ability splash damage, reflected damage, poison ticks, spells, native hit-spell damage, and damage received have no direct entry to this hook.
7. On a successful roll, set both timestamps to `now + 10 seconds` before any effect callback. Set a scoped reentry guard with `try/finally`. Mark harmful action through the normal API and apply one 12-damage AOS call with 100 percent of the selected element. No armor-ignore, direct-damage component, spell-damage calculation, separate XP payment, or new random damage roll is involved. Consume the cooldown even if resistance, immunity, or a later callback reduces that extra damage to zero. Never roll again to compensate.
8. Show the selected stock visual once. Clear the guard in `finally`. Native AOS leech and the existing damage-eater hook retain their usual behavior. The milestone does not call `OnHit`, `OnWeaponHit`, or `SpellHelper.Damage`, so it does not itself start another weapon proc or the custom Spell Leech spell callback. A regression must cover indirect reentry too.

One player's and all their companions' weapons share the owner's timer. Swapping weapons cannot clear it. The weapon timer prevents handing a recently triggered weapon to a different player for an immediate second trigger. Both timers run during logout, death, stabling, dormancy, and server downtime. Reequipping, trading, and changing maps do not reset them.

The hook runs before ability callbacks so a Double Strike's nested second swing sees the first proc's reserved cooldown. A lethal primary strike produces no milestone effect on the now-dead target. A milestone that kills the target must not prevent the normal remainder of the base hit method from running; do not insert a new early return into upstream combat code. Test that native callbacks still run safely after a proc kill.

Alternatives considered before this patch:

- A general `Mobile.OnDamage` or AOS damage hook reaches spells, reflection, poison, and damage taken, then needs extra provenance tracking to recover a weapon strike. P405 suggested it for carried passive items. The weapon-only decision makes that broader patch unnecessary.
- Reuse the current custom-imbue callback unchanged: rejected because it has no weapon or positive-damage argument, runs later, and refuses companions. Changing that callback for this feature would couple its existing effects to new proc eligibility rules.
- Feed chance into `AosWeaponAttributes.GetValue`: rejected because those native effects have their own damage and no saved shared cooldown. It would turn a distinct milestone choice into an ordinary weapon attribute.
- Override every crafted weapon or copy `BaseWeapon.OnHit`: rejected because existing sealed weapons and descendant classes would need broad changes, and copied upstream combat logic drifts silently. One targeted patch fails visibly on a conflicting pin bump.

## State, settings, and property accounting

Proposed additive source file names are interfaces for the build prompts, not claims that these files already exist:

| Location under `S/` | Responsibility |
| --- | --- |
| `server/customizations/LevelGear/ClusterFLevelGear.cs` | Extend `LevelGearState` and `LevelGearStore`; retain ordinary gear APIs. Coordinate the store format with the P568 purchase ledger. |
| `server/customizations/LevelGear/LevelGearProcCatalogue.cs` | Stable keys `stormstrike` and `emberstrike`, names, element, setting-backed defaults, and the purchase validator. |
| `server/customizations/LevelGear/LevelGearProcs.cs` | Owner resolution, attempt eligibility, shared timers, RNG and clock seams, effect application, and cooldown persistence. |
| `server/customizations/LevelGear/LevelGearGump.cs` | Milestone page, preview, confirmation, live status, and reply validation. Add pagination instead of making the existing property list taller. |
| `server/customizations/LevelGear/LevelGearPropertyBudget.cs` | Shared union of stored and purchased properties for gear and imbuing. Keep ordinary catalogue consumers, loot valuation, and extraction separate from purchased gear investments. |
| `server/customizations/ArtificersImbueGump.cs` | Use that shared budget reader in display and server-side mutations; show a reserved milestone slot without offering a proc essence or ordinary imbue row. |
| `server/patches/BaseWeapon-level-gear-proc-hit.patch` and `docker/uo/apply-patches.sh` | The one new combat call and its explicit patch registration. |
| `server/tests/Misc/LevelGearProcVerification.cs` | Proc purchases, eligibility, cooldowns, persistence, and actual combat integration. Extend existing gear/imbuing tests where they own the shared budget regression. |

Use a named `ProcPurchase` record on each gear row: stable proc key, saved required acting level, purchase item level, purchase UTC time, and paid point cost. A null record means no proc. If P568 supplies a general purchase ledger, put this as one typed ledger entry with the same fields and derive the selected proc from it. Do not store two independent authoritative proc selections.

The next store version appends the optional record after each row's existing data. If the ledger work already consumed version 1, choose the next unused version instead. A version-0 record loads with all old values unchanged and no proc. Never infer a free purchase because an old weapon is above level 100. Preserve unknown proc keys with their saved costs for future repair; leave them dormant. Reject unsupported future versions explicitly, as the store does now. No stock weapon save chain or `server/migrations/` item migration is needed.

Persist owner and weapon `NextProcAt` UTC maps in a separate `GenericPersistence` named `LevelGearProcs`, version 0. Keys are player serial and item serial respectively, never the current account, companion serial, or an in-memory stopwatch. Write only unexpired entries for still-existing players/items; prune expired/deleted entries in memory on access and on save. Load the saved absolute timestamp; do not start a fresh 10 seconds at load or clear a cooldown at login. A save/restart 3 seconds into cooldown leaves 7 seconds if downtime was zero; longer downtime consumes the remaining wait. Crash recovery follows the shard's last completed save, with no new per-hit disk writes. Rolling back world state can roll back these timers too.

Purchase validation must be one synchronous operation: living player, feature enabled, item still directly worn or in that player's backpack, eligible crafted weapon, existing levelable row, item level at least unlock, real attunement prerequisites available, no proc already bought, enough points, and room in the shared budget. Re-read on confirmation, deduct once, save the record, invalidate properties, and refresh the menu. Never trust a client-supplied key, price, required level, or earlier gump state. A repeated reply cannot charge twice. Companions use purchased gear, but only a player holding the weapon buys the choice. Reclaim it from the companion to purchase.

Shared budget rules must work in either purchase order:

- A stored property and a purchased increase to that same property use one slot. Each different ordinary level-only property uses one slot. The milestone is an additional distinct slot even when the weapon already has Hit Lightning. Count all purchased investments regardless of dormancy or feature toggles.
- Level spending and milestone purchases use `ImbuingTable.Current.BaseSlots`, currently 5. Imbuing retains the current actor's `ClusterFImbueKnowledge.MaxSlots` allowance, including the Master Formulary. Thus a master may imbue a sixth slot where allowed; that does not grant an unqualified gear menu a sixth purchase. An existing six-property weapon cannot buy a new milestone against a five-slot gear allowance.
- In intensity mode, sum the combined stored plus purchased value once per ordinary catalogue property, using that row's intensity function, then add 100 for a proc. Gear-side purchases use the base intensity allowance `BaseSlots * 100`; imbuing uses its current account's existing intensity allowance. Dormancy does not free budget. Do not count only the currently acting portion, which would let a reset make room for more permanent purchases.
- Imbuing a property already supplied by levels must project the combined value and ceiling before accepting the change. Do not charge a second slot for the same property or hide the proc reservation in imbuing's display. Existing over-limit investments are preserved, with new purchases refused until the proposed result fits; do not delete or refund history automatically.
- The proc is not an `ImbuePropertyDef`, essence source, Clean Up value multiplier, or loot-affix roll. Extraction of an ordinary imbued property changes that stored property only. Destroying the item destroys its effective proc investment. Do not alter every `CountActiveProperties` consumer globally just to fix the two spending surfaces.

The reverse-order hole and incomplete level-bonus intensity accounting already exist. Repair them in a shared-budget prompt before enabling proc purchases. This is a concrete prerequisite from P534, not an invitation to rebuild unrelated imbuing behavior.

All new balance values use `ServerConfiguration.GetOrUpdateSetting` under `clusterf.levelGear.procs.*`, materialized during configure like existing gear settings:

| Suffix | Default and meaning |
| --- | --- |
| `enabled` | `false` during implementation and until a separately authorized release after dependencies and client checks |
| `unlockLevel` | `100`, stamped into new purchases |
| `pointCost` | `100`, saved at purchase time |
| `chanceBasisPoints` | `500`; valid 0-10,000 |
| `cooldownSeconds` | `10`; valid 1-3,600 |
| `intensityCost` | `100`; valid 1-1,000; shared current reservation rule |
| `companionOwnerRange` | `18`; valid 1-24 tiles |
| `stormstrike.enabled`, `emberstrike.enabled` | `true`; each choice may be disabled without erasing purchases |
| `stormstrike.rawDamage`, `emberstrike.rawDamage` | `12` each; valid 1-100 |

Validate unlock within 1 through the configured item cap and cost within 1-10,000 points. Invalid proc settings disable the feature with a clear startup diagnostic. Never enable a zero or negative cost/cooldown by accident. The one-choice and PvE-only rules are code policy for this release, not hidden tuning switches. Test-only RNG overrides must not become a player or GM command.

Cost and unlock changes affect new purchases. Existing purchases keep their saved unlock and paid cost. Chance, damage, choice enablement, and future cooldown durations use current settings. Existing cooldown end times stay as saved; adjusting cooldown length does not clear them. Slot reservation always remains one; a changed intensity reservation affects admission for future purchases but never silently removes an existing choice.

The current 100-point proposal assumes the existing 4/8 earnings scale. P534 documents an accepted XP-curve conflict and an unresolved alternative material-sensitive point budget. Before release, reconcile that budget with P568 and the gear progression work. If the point scale changes, approve the corresponding proc price in the same balance table and preserve historical paid costs. Do not silently take 100 points from a new 100-point lifetime budget.

## Art, client, and player documentation

No new bitmap, item ID, gump ID, animation body, cliloc entry, client binary patch, or map edit is needed. Use the existing gump background/buttons/text, `BoltEffect(0)` for Stormstrike, and a stock fire effect for Emberstrike. The existing fireball code uses particle item `0x36D4` and sound `0x15E`; reuse the visual with immediate damage and no delayed spell call. Stormstrike can use the existing lightning visual without its damage helper. Check appearance in the packaged TazUO client; source IDs alone do not prove appearance or timing.

This design needs no art for Chase to generate, so there is no art request. If custom icons become a later requirement, file an art request with `scripts/art/New-ArtRequest.ps1`; do not generate or invent unapproved assets as part of this build.

The Milestone page must fit beside the current property page at the supported client window sizes, state cooldown sharing in plain language, and show exact refusal reasons. Verify one player and a companion in the client, including a loop reset. No new Shard Console controls are proposed, so there is no console/web twin work.

Prepare wiki-ready text in migration `notes/` explaining acquisition prerequisites, level 100, the price, one slot, permanent choice, PvE scope, native hit-spell coexistence, shared companion cooldown, and acting-level dormancy. The overseer can promote the custom-system entry and fidelity register entry under the existing rules. Agents do not edit migration `docs/` or publish/deploy the wiki from this prompt. The feature is invented shard progression, not an OSI proc port, and needs that custom-system register entry when implemented.

## Tests and acceptance

P569 adds no tests and runs no shard build. Lane tests are none. Every new implementation regression must be seen failing against the prior behavior, then passing with the change, with the failing assertion and passing run recorded. A noncompiling reference to a missing new API alone is not the behavioral red proof. Build inert interfaces first if needed, show an assertion fail, then implement. For a hook gate, temporarily remove the dispatcher call after implementation and prove the actual-hit test fails again. PowerShell scripts and checks run with `powershell.exe` 5.1.

| Test group | Required acceptance cases |
| --- | --- |
| Purchase | Level 99 refused; 100 accepted; exact price 100 accepted; 99 points refused; zero changes on all refusals; one choice saved; duplicate/replayed replies charge once; crafted-only/rarity checks remain; armor, jewelry, fists, backpack-only effects, and found weapons never proc. Validate forged button/key, transfer between preview and confirmation, death, deletion, and a setting change between replies. A dormant wearer's purchase succeeds on an eligible earned-level-100 item but does not activate it. |
| Shared budget | Level-first and imbue-first order give the same occupied-slot count. Four existing slots allow a proc; five refuse it. Native Hit Lightning plus a milestone uses two slots. Dormant and globally disabled purchases still count. Master Formulary's allowed extra imbue slot remains usable. In budget mode verify the 100-intensity reservation and ordinary combined values at the exact limit and one above it. |
| Chance and clocks | Inject RNG and UTC time. Roll 499 succeeds and 500 fails at 500/10,000. Cooldown at 9.999 seconds refuses; exactly 10 seconds allows. No RNG consumption for blocked attempts. Reserve cooldown before effect/reentry, even if extra damage is later zero. Avoid a probabilistic test that occasionally fails. |
| Combat reachability | Drive actual `BaseWeapon.OnHit` with a sealed equipped weapon and a deterministic positive physical hit, then real ranged hits through `BaseRanged` and a crafted `BaseThrown` descendant. Assert one elemental increment and the correct source. Miss, parry/zero physical damage, dead target, illegal harm, out-of-range/LOS, native spell damage, DoT, reflection, and received damage never independently trigger it. A direct call to the proc service alone is insufficient. |
| Special moves | Native hit effects still work. Double Strike can attempt on its second strike after a failed first roll; a successful first roll blocks the second through the shared timer. An ability splash target is not eligible. A primary or native-proc lethal hit does not trigger on a corpse. A milestone kill retains normal death credit and does not break later ability/creature callbacks. |
| Ownership and transfers | Player, controlled companion, second companion, weapon swap, and new wearer share the specified owner/item restrictions. Unowned, offline-owner, distant-owner, summoned, provoked, and ordinary pet cases refuse. Swapping or trading during cooldown does not clear either applicable timer. Different players with different weapons have independent timers. |
| Attunement | Acting 99 dormant; acting 100 active. At wearer 95 with +5 active; wearer 94 with +5 dormant. Purchase at item 150 keeps required acting level 100. Reset keeps XP/choice/points and makes the proc dormant, then it returns at threshold. A transferred companion weapon follows the new owner's acting level. Missing real F-12 provider refuses use and purchase. |
| Persistence | Read an actual version-0-shaped buffer without a proc. Round-trip new purchases and both timer maps after clearing memory. Preserve unknown keys dormant, reject unsupported versions, omit deleted items and expired timers, and verify UTC remainder across a simulated restart. Then verify a full scratch world save/restart separately; buffer tests alone do not prove lifecycle registration. |
| Effects and restrictions | Stormstrike is 100 percent energy and Emberstrike 100 percent fire at raw 12, with expected target resistance. No new skill scaling, mana cost, heal, summon, gold, resource, or loot object. Players and controlled targets are excluded even in a PvP facet. Standard AOS leech and damage-eater interactions are explicitly exercised. No recursive milestone activation. |
| UI and configuration | Choice preview and confirmation show current costs, reservations, and refusal reasons. Tooltip is owner-neutral. Invalid config disables safely; globally disabled or unknown effects retain state and reservations. Feature disable/enable, price tuning, and unlock tuning do not rewrite old paid costs/requirements or clear existing cooldowns. |

Use the existing sequential UOContent fixture conventions from `S/server/tests/Misc/LevelGearVerification.cs`. New test classes stay in namespace `ShatteredLegacy.Tests`, and the normal test mirror reaches `Projects/UOContent.Tests/Tests`. Run `docker/uo/build.sh` with a prompt-specific image tag for each implementation task, including the actual combat integration fact. Do not use direct `docker build` as the test gate.

Before any separately authorized player release, use a throwaway loopback-only shard with scratch saves to verify menu clicks, companion behavior, stock visuals, an actual save/restart during cooldown, and a reset/dormancy round trip. Record the packaged client version and observations. Do not connect to Haven, restart a live shard, alter live accounts, or enable live settings as part of these build prompts.

## Ordered Golem prompts

These are proposed titles for the overseer to number, not newly created queue entries. Each implementation prompt writes its own migration notes, records red/green evidence, and ends under that prompt's own completion rules. `Touches: server` includes canonical customizations, patches, test sources, and the patch application route. The prompts must not run concurrently on these shared files.

1. **Gear progression and attunement prerequisites, follow P534 and P568.**

   **Touches:** server

   Require the real F-12 current/max-level provider, approved acting-level rules, a versioned purchase ledger, deterministic treatment of old aggregate rows, and a coherent point/XP budget. P568's design is a sibling dependency, not completed implementation in this snapshot. Reuse its service and conversion instead of building a proc-only player-level service. Resolve P534's known award/anti-farm defects in their own prerequisite slices before a player progression release. The accepted League unlock and crafted sealing consumable acquisition must also be implemented before release, with reachable resources. Do not add proc behavior here. Stop this sequence's release gate if those dependencies are absent; an isolated disabled proc build may still be reviewed.

2. **Shared gear and imbuing budget accounting.**

   **Touches:** server

   Fix reverse-order slot admission and display, preserve Master Formulary allowances, and add the reserved-proc input to the shared projected slot/intensity reader. Cover same-property union, full investment while dormant, and both purchase orders. Do not globally change loot/extraction valuation. This can be built with zero reserved proc input before proc state exists. Keep procs disabled.

3. **Saved milestone choice and guarded purchase flow.**

   **Touches:** server

   Add the catalogue/settings, next-version purchase record, migration reader, atomic validator, Milestone page, confirmation, and owner-neutral tooltip. Use step 1's ledger/acting-level APIs and step 2's budget reader. Feature stays off by default. Verify legacy row preservation, duplicate replies, affordability, exact unlock boundary, settings validation, and saved unlock versus late purchase level. No combat effect yet.

4. **Weapon proc dispatch and persistent cooldowns.**

   **Touches:** server

   Add the targeted weapon patch, explicit assembler registration, service, persistence, and two fixed elemental effects. Test actual melee/ranged hooks, zero damage, PvE filters, companions and owner presence, swapping/trading, recursion, Double Strike, native proc coexistence, kill credit, and restart remainder. Prove the hook regression fails with its call removed, restore it, then run the build gate. Keep release enablement off.

5. **Scratch-world acceptance and release evidence.**

   **Touches:** server

   Requires steps 1-4 passing and explicit task authorization to run the disposable local acceptance shard. Use loopback-only networking and scratch saves. Run the full world restart, companion/reset, packaged-client UI/visual, and cooldown checks. Record timing samples for slow and fast weapons and a companion party; tune only if Chase approves changed defaults. Produce a concrete release configuration proposal and wiki/fidelity text in notes. Leave live enablement to a separately authorized release. No Haven connection or publication.

The full slot/ledger/F-12 work is larger than the narrow proc service. Do not describe the complete feature as a small standalone port merely because P405's original idea was small. Cost estimates: shared-budget repair M, saved choices/UI M, combat/timers M, prerequisite progression work L across existing tasks. These are planning estimates, not measured effort.

## Verification and remaining uncertainty

Read both work-copy `AGENTS.md` files and the migration direction, task list, governing-document index, subsystem policy, and fidelity rules. Inspected the code and patch routes cited above and the actual pinned combat implementations. No `server/uo/` source was read. No code, config, migration `docs/`, queue file, branch, commit, or service was changed.

Unverified: live settings and existing sealed-item population, full player acquisition, actual F-12 integration, P568's eventual chosen ledger details, client rendering/timing, every weapon subclass's override path, and combat balance. The base thrown-weapon path was traced in source, but representative melee, bow, crossbow, and thrown-weapon runtime checks are still required before release. The third-party download's exact contents and licensing were not rechecked beyond P405. No build, runtime test, or client session is claimed by this design.

Document review passed under Windows PowerShell 5.1.26100.9711: no em dashes, no trailing whitespace, file below 5 MB, clean code work copy, and only this requested note added in the migration copy. `git diff --check` also passed; the untracked note's whitespace was checked directly. The required progress reporter completed with `--dry-run` and both work-copy path overrides. Its incidental `progress.json` write was suppressed in memory, so it changed no generated files. Its broad inventory totals are not feature verification and are not repeated here. No tests were added, so there is no new test requiring a red/green run in this docs-only task. The stop-request file was absent at the completion check.

Questions below are review questions requested by this design task, not a request to pause unattended work or reopen settled choices.

## Questions for Chase

1. **Unlock and cost: level 100 for 100 item points?** Recommended: yes on the present 4/8 point scale, about 23 percent of earnings by 100. If the separate gear budget changes, approve a matching price before release. Keep reaching the milestone and purchasing the effect separate.
2. **First choices: Stormstrike and Emberstrike at 5 percent, 12 raw damage, 10 seconds shared cooldown?** Recommended: yes as a conservative initial test table, fixed damage and normal mitigation. Start with these damage choices; give healing and summons separate balance designs.
3. **One permanent choice per weapon, one ordinary property slot, and 100 intensity in budget mode?** Recommended: yes. Respect existing Master Formulary allowances through the shared budget reader. Add a paid change only when saved-cost respec is built, not a free switch now.
4. **PvE only, with players and their controlled creatures excluded?** Recommended: yes for this release. PvP can receive a separate reviewed ruleset after actual combat samples. Native weapon attributes continue under their existing rules.
5. **Player and companions share one cooldown, with a weapon timer to prevent trade resets?** Recommended: yes. Companions use their owner's attunement and require the owner online within 18 tiles; the companion stays the damage source.
6. **A late purchase still requires acting level 100, even if bought at item level 150?** Recommended: yes. Save the milestone threshold separately from purchase level, and preserve both through trades and resets.
7. **Fast weapons and Double Strike receive more attempts per second?** Recommended: yes initially, with the shared cooldown bounding successes. Measure the difference before adding weapon-speed normalization, which would need a separate formula and updated player wording.

P569 DONE
