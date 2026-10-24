# P567: summons as a high League rank reward

Written 2026-10-24. Design only. No code, client files, configuration, accounts, or world state changed.

## Recommendation and decision boundary

At Mythril Citizen, the League Registrar issues a reusable, character-bound **Tome of Echoes**. It calls one **Echo of the Stygian Dragon** for 20 seconds, using two ordinary follower slots. The account can call again 30 minutes after a successful call. The Echo is a modest melee helper wearing the dragon's appearance. It leaves no loot and grants no rewards when destroyed.

Chase already chose the feature. `D:\UO\overseer\decisions-2026-10-22.md:15-16` records his 09:35 answers: a high League rank reward, one weak Echo, no loot, long cooldown, normal follower cost, the name pattern "Echo of X," and the item name "Tome of Echoes." These are settled requirements. Mythril, the dragon choice, the exact numbers, free issue, binding, and the PvE limits below are proposed defaults for Chase to review.

This is native custom League content inspired by TwilightRaven's summoning-system-v2 idea. Write new code. Keep the real Stygian Dragon and ordinary summon schools working as they do today. The overseer should register this invented feature and its guide requirements in the fidelity register when implementation is approved; agents put that proposed entry in notes.

The hostile investigation boss and its single-use warrant belong to the separate P565 design, `notes/cc-P565-design-league-reward-tokens.md`. That item buys an encounter with normal encounter rewards. This Tome calls a friendly, temporary helper. Their cooldowns, eligibility, and item identities are separate. An Echo participating in an investigation must obey that encounter's existing helper and roster rules through its owner.

## Evidence and limits

The prompt's `notes/cc-P405-servuo-batch-1022-research.md` is absent in this work copy. The completed prompt, `D:\UO\cc-prompts\completed\cc-P405-servuo-batch-1022-research.md`, explicitly names its output as `notes/cc-P405-servuo-batch-1022.md`. Its summoning section at lines 450-531 and question 3 at lines 1169-1171 are the third-party evidence used here. The completed prompt contains the assignment, not an answer transcript; Chase's answer is in the overseer's decision log above.

As directed, third-party code was assessed through P405's notes, not opened or executed. P405 reports whole-file replacements of BaseCreature, SpellHelper, Spellbook, Initializer, Reagent, and SpellRegistry; an absent Druid dependency; a global command-prefix change; and summoned boss copies with loot and death drops. Its reported Stygian summon has 30,000 hits, costs two slots, and lasts 20 seconds. These are P405's findings, not fresh measurements. Its unstated license gives no reason to copy the download. Credit the idea in the implementation note.

The code work-copy HEAD and local `main` both resolve to `1020e36a42d31dde07612544ea2a6f9472911db8`. The migration work-copy HEAD and local `main` both resolve to `8356b8b4b2cfe7ce4d83776342ea9acced8e0c69`. No branch was switched or fetched. These identify the local source inspected, not the running shard or remote main. Pinned ModernUO resolves to `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.

Shard paths below are relative to the code repo. Engine paths are relative to `D:\UO\ModernUO-pinned\Projects`, except where stated otherwise.

| Source read | What it establishes |
|---|---|
| `server/customizations/ClusterFLeagueRanks.cs:228`, `:405`, `:485` | League rank belongs to the character. Promotion reads account LifetimeRenown and the character's guild, job, and trial requirements. Mythril's default row is 76,000 lifetime Renown, Master in four guilds, and chapter 5. These are configurable defaults, not a verified live table. |
| `server/customizations/ResourceInfo.cs:11`; `ClusterFLeagueRanks.cs:121`, `:146` | The ladder follows metal enum order, excluding Dawnstone. Mythril is rank 15 in the inspected ladder. Resolve the gate by metal key, following `LeagueRegisterSettings.Rank`, rather than hard-coding 15. |
| `server/customizations/ClusterFAccountData.cs:220`, `:467`, `:503`, `:688` | Account data currently writes version 22. CharacterLeagueData writes version 2 and already stores a current Register serial. Account and character additions need their own compatible versioned reads. |
| `server/customizations/LeagueRegister/LeagueRegister.cs:82`, `:352` | The Register supplies a useful issue/reissue precedent: character owner, current serial, blessed item, and a successful backpack placement before replacing the old copy. |
| `server/customizations/LeagueRegistrarGump.cs:26`, `:134`, `:234`, `:417` | The Registrar has menu, rank, and Register issue paths. The rank page returns early for the highest rank, so a new reward must remain accessible there too. |
| `server/customizations/LeagueShop/LeagueShop.cs:1`, `:93`, `:139` | The AP shop is a different reward track with an explicit starter-stock policy against combat power. Issue this rank ability through the Registrar, with no shop row or loot-box factory. |
| `server/customizations/Companions/CompanionParty.cs:62`, `:82` | Companions and pets consume FollowersMax. Loop progression may raise that cap; this feature must read it, never grant or reserve extra slots. |
| `UOContent/Mobiles/BaseCreature.cs:3808-3864` | `Summon` checks follower capacity, sets controlled/summoned/master state, clears backpack items, starts an UnsummonTimer, and moves the creature. The shown overload does not validate the placement tile. |
| `UOContent/Spells/UnsummonTimer.cs:15-41`; `BaseCreature.cs:2708`, `:3672` | Expiry deletes the summon; deletion stops its timer and clears its master. The optional callback runs on timer expiry, so it cannot be the only cleanup path for dispel, death, or direct deletion. |
| `UOContent/Mobiles/BaseCreature.cs:864`, `:3220`, `:3475`, `:3662` | Construction can generate spawn loot. Death has awards and events beyond GenerateLoot. A loot override alone is insufficient. |
| `server/customizations/Mobiles/Bosses/StygianDragon.cs:39`, `:120`, `:140` | The real boss has a boss parent, powerful timed attacks, resources, and an OnDeath trophy drop. A subclass would inherit behavior this reward does not want. |
| `UOContent/Mobiles/Monsters/Summons/SummonedDaemon.cs:9-76` | A direct BaseCreature summon is an established shape. Its AOS melee damage is 14-21 plus mage AI, and its SE slot cost is four. This is a source comparison, not measured combat balance. |
| `UOContent/Mobiles/BaseCreature.cs:1365`, `:1389`, `:3717`; `Server/Mobiles/Mobile.cs:8333` | Summons are dispellable and normally not bondable. The harmful-action check is virtual and can enforce the Echo's target policy locally. |
| `UOContent/Mobiles/AI/BaseAI/ContextMenu.cs:57`; `OnSpeech.cs:378`, `:422`; `PetOrders.cs:476`, `:538` | Summoned followers cannot gain friends, transfer, or rename through these ordinary pet paths; release calls Kill. The Echo's death override must handle that release path. |
| `UOContent/Mobiles/PlayerMobile.cs:625`; `UOContent/Spells/Base/SpellHelper.cs:839` | A player exposes DuelContext; CheckTown refuses guarded-town casting. CheckTown alone does not prove a tile is valid or cover all special regions. |
| `UOContent/Engines/ConPVP/SafeZone.cs:7`, `:16`; `UOContent/Systems/JailSystem/JailRegion.cs:6`; `UOContent/Regions/HouseRegion.cs:10`; `server/customizations/Tutorial/TutorialWingTrials.cs:686`; `Regions/ApprenticeTraining.cs:288` | SafeZone can have guards disabled, so a town check alone misses it. JailRegion, HouseRegion, TutorialYardRegion, and ApprenticeTrainingRegion are concrete location-policy seams. |
| `server/patches/BaseCreature-PlayerMobile-can-auto-stable.patch:10` | Our existing patch exposes CanAutoStable. The Echo can override it without another upstream patch. |
| `server/customizations/ClusterFAchievements.cs:1387`, `:1503`; `ClusterFLeagueBestiary.cs:148`, `:171` | CreatureDeathEvent feeds kill rewards. The generic achievement counter does not itself reject summons. Preventing a corpse alone does not establish no rewards. |
| `server/customizations/LevelGear/ClusterFLevelGear.cs:461`, `:475`; `Requisitions/RequisitionLeads.cs:181`; `Mobiles/Evo/EvoPet.cs:243` | Existing award paths have summon/player-pet exclusions. Level gear reads CreatureDeletedEvent before the master is cleared. Preserve Summoned and NoKillAwards through deletion and test these consumers. |
| `server/customizations/ClusterFCreatureLevels.cs:98`, `:175` | Appraisal derives ordinary creature levels unless a type override or boss ancestry applies. A direct BaseCreature Echo avoids the real boss's level classification. |
| Pinned `Distribution/Data/bodyTable.cfg:988` | Body 826 is already typed Monster for the Stygian Dragon. No new server body-table entry is needed for this proposal. |

Not verified here: current live rank settings and waivers, player-package rendering of the proposed body/hue/book combination, combat performance, physical map tiles, full world save/load behavior for the new types, or future code. No build or client session was run for a design-only task. The implementation gates below must establish those facts.

## What players see

The Registrar gets an **Echo reward** menu entry, visible at every rank. Below Mythril its page says, "At Mythril Citizen, the League will teach you to call a brief Echo." It shows the rank name and explains that this is a friendly helper. At or above Mythril it offers **Claim Tome of Echoes**, or **Replace Tome of Echoes** when a copy has already been issued. Existing qualified characters can claim it immediately. There is no new trial-completion requirement beyond the rank system's own promotion policy and waivers.

Claim and replacement are free. The reward is the earned ability, not a consumable purchase. Require the living character to stand on the Registrar's map within her existing four-tile interaction distance and in line of sight when claiming, including on gump response. Recheck the current rank and pack capacity. A full pack leaves the old Tome and recorded serial intact. Successful replacement makes the previous copy unusable and deletes it if it can be found. Replacement never resets the account cooldown or dismisses a running Echo.

The Tome is blessed, weighs 1 stone, uses book art `0xEFA`, and displays its character owner's name. It can be banked, but must be in that owner's backpack to work. Physical movement or a copied/stale item grants nobody else permission to use it. A deleted owner or missing account makes it inert. The Tome has no charges, skill bonus, equipment slot, or sell value.

Double-clicking opens a compact page with:

- **Echo of the Stygian Dragon** and "A brief memory of the dragon, bound to help you."
- "Lasts up to 20 seconds. Uses 2 follower slots. Your account can call once every 30 minutes."
- "Fights wild creatures. Cannot fight players or their followers. Leaves no loot. Can be dispelled."
- Current follower use, the character's rank, and **Ready**, **Ready in 12m 08s**, or **Echo active: 11s remaining**.
- **Call Echo**, **Dismiss Echo** while this character owns the active one, and **Close**.

The Call button is immediate, with no ground target, mana charge, reagents, or skill roll. It may be used during PvE combat and while mounted. A successful call reveals the caller. It places the Echo on a valid adjacent tile, starts following, and prints, "The Echo answers. It will remain for 20 seconds." Ordinary Attack, Follow, Come, Guard, Stay, Stop, and Release orders work within the policy below. Dismiss and Release dissolve it. The Echo shows its full name and temporary nature, never the real boss's name alone.

Refusals explain the failed rule, for example "The Tome requires Mythril Citizen," "That Tome belongs to someone else," "You need 2 free follower slots," "Your account can call again in 12m 08s," "There is no room beside you," or "The Echo cannot be called here." A stale page, losing the Tome, or moving it to the bank after opening cannot call or dismiss through that page. Reopening shows fresh state; the server never trusts a displayed countdown or enabled button.

The guide must distinguish this combat Echo from F-12's loop-memory echo and the tutorial's Echo voice. Neither level resets nor changing a Tome resets this ability's cooldown.

## Proposed numbers and rules

| Rule | First implementation default |
|---|---|
| Unlock | Current character is Mythril Citizen or higher, resolved by `Mythril` metal key |
| Issue and replacement price | 0 Renown, 0 gold, 0 AP; no per-use charge |
| Available forms | One: Echo of the Stygian Dragon; no stronger form at Celestial |
| Lifetime | 20 seconds from successful spawn, never extended by healing or commands |
| Cooldown | 1,800 seconds from successful spawn, shared by all characters and Tomes on that account |
| Active limit | One Echo per account; independent accounts may each use theirs |
| Follower cost | 2 slots against current FollowersMax, with pets and companions still counted |
| AI and opening order | AI_Melee, FightMode.None; Follow its caller, fight only by legal Attack/Guard or retaliation |
| Strength / Dexterity / Intelligence | 200 / 100 / 50 |
| Hits / Stamina / Mana | 300 / 100 / 0 |
| Base melee damage | 12-16, 75% physical and 25% fire; ordinary hit and armor calculations still apply |
| Resistances | 35 physical, fire, cold, poison, and energy |
| Skills | Wrestling 80, Tactics 80, Magic Resist 80; other skills zero; lock skills against gain |
| Other combat | No spells, breath, poison attack, poison immunity, aura, weapon ability, healing AI, boss attacks, or death attack; VirtualArmor 0; cannot flee |
| Dispel | IsDispellable true while summoned; difficulty 100 and focus 20, using ordinary dispel resolution |
| Body / hue / sound | 826 / 1323 (League blue) / BaseSoundID 362; summon sound `0x216` |
| Leash | Dissolve when more than 12 tiles from the caller, on another map, or otherwise ineligible |
| Awards and resources on the Echo | Fame 0, Karma 0, NoKillAwards true; no maps, meat, hides, scales, feathers, trophies, parts, gold, or inventory |

These are nominal creature inputs, not a damage-per-second promise. Skills, resistances, hits, and available commands need a real fight check. At uninterrupted maximum use, 20/1,800 is about 1.1% uptime. The low uptime, short duration, melee-only attack, ordinary dispel, and two occupied slots make this a brief intervention rather than a replacement for a trained pet or summon school. Healing from otherwise legal sources may restore hits but never life duration; no bonding, resurrection, taming, pet training, feeding benefit, equipment, mounting, or cargo.

Do not scale strength or duration by Magery, Spellweaving focus, player level, loops, Renown, or higher League rank. Group balance assumes one Echo for each eligible account, not one for an entire party. Test that case rather than silently adding an undisclosed party restriction.

### Where it works and what it can attack

First release is PvE only. Allow Trammel, Ilshenar, Malas, Tokuno, and Ter Mur when the map exists and all other rules allow the use. Refuse Felucca, Internal, unknown/custom facets, houses, guarded towns, jail, safe regions, and an owner with a non-null DuelContext. Inspect both the caller's tile and the proposed spawn tile. Do not promise a blanket prohibition of New Haven Island: its wilderness remains ordinary PvE unless a tutorial or other protected region covers the tile.

Keep the special-region checks in one Echo policy helper. Refuse any region whose parent chain contains HouseRegion, JailRegion, ConPVP.SafeZone, TutorialYardRegion, or ApprenticeTrainingRegion. SafeZone must be refused even with its guards disabled. Use SpellHelper.CheckTown for guarded towns in addition to those type checks. Here "jail" means the staff JailRegion, not an ordinary dungeon cell such as WrongJailRegion. An encounter that forbids followers also forbids the Echo; it must not bypass existing interaction rules because it came from an item. Before enabling, the implementation must name any additional encounter region types inspected on its then-current main and prove their refusal cases.

For placement, examine the eight adjacent X/Y positions, testing the caller's Z and the map's average Z for each. Require a valid mobile spawn tile, caller line of sight, and permitted region. Do not fall back to an invalid tile or the caller's occupied tile. If all candidates fail, nothing spawns and no cooldown starts. Recheck follower space and eligibility immediately before calling BaseCreature.Summon.

An outgoing target must be a living, wild BaseCreature with no controller or master, not Summoned, bonded, invulnerable, or initially innocent. Require the owner's ordinary CanBeHarmful check and the Echo's base CanBeHarmful implementation to pass, with no recursive call back into the Echo override. Reject players, player-owned followers, vendors, guards, escorts, TutorialCreature instances, and other protected NPCs. The Echo's local CanBeHarmful override must enforce that filter for Attack, Guard, retaliation, and bard-induced combat. Clear an illegal Combatant before attacking. Re-evaluate on every harmful action so a creature tamed or transferred after targeting becomes ineligible. Do not treat an owner-directed attack as permission to hurt another player.

Use the same location and owner checks during its life, before harmful actions and on a one-second watchdog. Crossing into a forbidden area dissolves it. Owner logout or death dissolves it immediately through events; map change, owner deletion, duel enrollment, excessive distance, revoked rank, or disabled feature also dissolve it through the watchdog. A player may attack or dispel an Echo only under ordinary world harmful-action rules; it never retaliates against a player or their pet. This is not a new invulnerability or criminality exception.

## Implementation and save contract

Use namespace `Server.Engines.LeagueEchoes` for the service and UI and `Server.Mobiles` for the creature. Proposed new canonical files:

| File under `server/customizations/` | Responsibility |
|---|---|
| `LeagueEchoes/LeagueEchoSettings.cs` | Enabled switch and validated numeric settings; defaults above |
| `LeagueEchoes/LeagueEchoSystem.cs` | Rank check, issue/reissue, current-copy check, spawn transaction, account cooldown, runtime active registry, owner events, and watchdog |
| `LeagueEchoes/LeagueEchoPolicy.cs` | Shared location, spawn-candidate, and legal-target rules |
| `LeagueEchoes/TomeOfEchoes.cs` | Generated item serialization, character owner, properties, and item-use checks |
| `LeagueEchoes/TomeOfEchoesGump.cs` | Reward claim/explanation and carried-Tome Call/Dismiss views, all routed to the same service |
| `Mobiles/LeagueEchoes/LeagueDragonEcho.cs` | Direct BaseCreature child, fixed weak profile, loot-free death, generated serialization, and deletion cleanup |

Existing edit points are `ClusterFAccountData.cs` and `LeagueRegistrarGump.cs`. No new stock-file patch or full-file replacement is expected. The existing mirror copies these paths into UOContent. No custom spell registration, spellbook enum, player command, command-prefix change, new AI engine, XmlSpawner, or Druid dependency is needed. If an actual engine seam proves insufficient, record the evidence and alternatives before proposing a separate targeted patch.

Use `clusterf.leagueEchoes.enabled`, default **false** until acceptance is complete; `requiredRank`, default `Mythril`; `durationSeconds`, default 20; and `cooldownSeconds`, default 1800. Read settings through ServerConfiguration, following the League settings style. Fix the initial form and combat profile in the creature code rather than exposing a staff-entered type name. Reject unknown rank keys, duration outside 1-60 seconds, and cooldown outside 300-86400 seconds, logging the reason and refusing new calls. Capture validated duration and next-use time at spawn; later changes do not extend an existing Echo or shorten a recorded cooldown. Disabling refuses issue/call and clears active Echoes within one watchdog tick. Cleanup and Dismiss must remain available while disabled.

### Storage

Append an account-level `DateTime LeagueEchoNextUseUtc` after the present v22 payload and advance ClusterFAccountData to its next unused version, presently 23. Earlier account records default to DateTime.MinValue, meaning ready. Preserve the future-version refusal. Store an absolute UTC deadline based on Core.Now, not ticks left or a timestamp on the Tome. Normal save/restart preserves it. A crash can restore the last world save's deadline, as with other world state; do not claim stronger durability or trigger a world save on each call.

Append `uint EchoTomeSerial` to CharacterLeagueData and advance its next unused version, presently 3. Versions 0-2 default to zero. The Tome uses `[SerializationGenerator(0, false)]` with an owner Mobile reference. Eligibility remains the character's current League rank, not a permanent account unlock or a claimed flag. Compare the carried item's serial to this character's current EchoTomeSerial on every use and response. Rebase the proposed version numbers on intervening work before implementation; never reuse another task's schema version.

Issue in this order: validate caller and Registrar, construct the new bound item, place it successfully in the pack, record its serial, then invalidate/delete the old item. Never delete the old copy or change its serial before placement succeeds. Free replacements do not alter LeagueEchoNextUseUtc. No extra claim event is sent through generic AP/loot-box rewards.

Active creatures live in a runtime dictionary keyed by IAccount, holding the exact owner and creature references. Keep the account identity on the Echo for cleanup even after BaseCreature clears its master. Do not persist that dictionary or a second timer on the item. LeagueDragonEcho also uses generated serialization so a save taken during its short life remains readable. Its post-load callback schedules Delete for the first timer slice after world load; no saved Echo resumes or registers as active. Test this with actual world save/load and verify follower reconciliation, not just a field round-trip.

The one current Tome serial and cooldown are the only new persistent player state. There is no retroactive world grant, save re-parenting, wipe, spawn seeder, or account conversion job. Qualified players claim on demand. After a new-version save, keep schema readers in any disabled build; an old binary cannot safely read that save. Rollback restores a matching full save and binary under Chase's separate procedure, rather than deleting the reader fields.

### Call transaction and cleanup

On the game thread, revalidate the feature, exact character/account, living online state, current carried Tome, rank, non-duel and location policy, no active account Echo, elapsed account cooldown, and two free follower slots. Reject callers who are frozen, paralyzed, or already casting. Reserve the account in the runtime registry against duplicate responses; validate a placement tile; construct the Echo; invoke the controlled BaseCreature.Summon overload with the captured 20-second duration. Check its result and resulting owner, Summoned state, location, and existence. Only a complete success sets LeagueEchoNextUseUtc to Core.Now plus 1,800 seconds and reveals the caller. Follow order is explicit.

A refusal or exception deletes the temporary creature, clears only that attempt's reservation, frees any slots through normal deletion, and leaves the cooldown unchanged. Never use the void SpellHelper.Summon wrapper as proof of success. Duplicate/reentrant replies, two Tomes, and a different character on the same account still get one success and one deadline. Death, dispel, early dismissal, replacement, and logout do not refund or reduce a successful call's cooldown.

Make all cleanup idempotent. LeagueDragonEcho.OnAfterDelete removes only a registry entry that still refers to that same Echo, stops its own watchdog work, and calls base cleanup. BaseCreature handles its summon timer and follower accounting. Never manually subtract follower slots in addition to base deletion, and never clear a newer Echo's entry from an older callback. Do not rely on the optional onUnsummon callback, which is only called by expiry.

For lethal damage and Release, override OnBeforeDeath to show the dissolve effect, Delete, and return false without calling the normal death pipeline. The result is disappearance with no corpse, CreatureDeathEvent, or boss death code. Keep GenerateLoot empty from construction onward, NoKillAwards true, all resource yields zero, and DeleteCorpseOnDeath true as a defensive fallback. The deletion event still runs, so its consumers must see the summon and no-awards flags. No code may clear them to turn the Echo wild. Reject inventory drops and leave ordinary summoned-follower transfer/friend restrictions in place. A skill-gain lock and null TrainingDefinition prevent reward progression into a permanent pet.

When an Echo helps kill a real eligible wild creature, existing master/damage attribution and encounter rules apply. Do not grant automatic owner kill credit, AP, Renown, parts, or gear XP just for summoning, and do not replace the shard's existing last-hit or damage-share rules. Destroying the Echo itself must grant none of them. Verify both directions separately.

## Art and client work

Use existing Stygian Dragon animation body 826, book art 0xEFA, League hue 1323 (`LeagueShop.LeagueHue`), and existing summon/dissolve effects. The server already types the body as Monster. Reuse the same hue on the Tome and Echo; do not copy the download's unverified hues. Body choice is appearance only and does not import the real boss's AI or attacks.

No new art, animation slots, clilocs, client protocol, TazUO patch, map edits, or art request is required by this proposal. No art was generated or requested. Client validation still must show the installed player package renders the body at this hue, book, labels, attacks, movement, and disappearance correctly. If it fails, record the observed failure and investigate the existing asset mapping. Do not silently allocate a new body or start art generation. A later approved custom-art change gets its own art request through New-ArtRequest.ps1 and the appropriate client scope.

The gump must fit at the player's normal window size, use words with any color cues, and keep Call and Dismiss unambiguous. Book double-click and ordinary pet commands are sufficient for launch; no new macro spell IDs or hotkeys. The Registrar explanation and player wiki draft must call it a friendly, dispellable helper and repeat the account cooldown, follower cost, PvE restrictions, replacement rule, and no-loot rule.

## Tests and acceptance

No lane tests are required for P567 and no tests were added. These are required implementation tests, not claims of current coverage. Put meaningful subsystem tests in `server/tests/Misc/LeagueEchoesVerification.cs` and `server/tests/Mobiles/LeagueDragonEchoVerification.cs`, namespace `ShatteredLegacy.Tests`, using the sequential host, accounts, test NetState, and ShardTestClock patterns already used by LeagueRegisterVerification. Timer.Slice alone does not advance Core.Now.

Every new test must be observed failing and then passing. Add runnable regressions before each behavior change; for a new API, first provide only the minimum compilable inert seam and observe the behavioral failure before implementing it. Where a guard already passes, temporarily remove that guard to demonstrate that the new test detects its loss, then restore it. Record the exact red assertion, fault, and final pass in that implementation prompt's notes. A compile error or zero selected tests does not count as the behavioral red run.

| Test group | Required evidence |
|---|---|
| Rank and issue | Below Mythril refused; Mythril and Celestial accepted; same-account low-rank alt refused; existing qualified character can claim with trial waivers; unknown configured rank refuses. Registrar moved away and forged claim responses fail. |
| Tome ownership and replacement | Wrong character, copied item, obsolete serial, banked/missing/deleted item, and stale page refused. Successful free replacement invalidates the old copy. Full pack preserves old copy, serial, and cooldown; no ground drop. |
| Follower and concurrency | Two slots are charged once; insufficient capacity refuses without a deadline; mule/companion slots count. Duplicate replies, another Tome, and a qualified account alt cannot create a second Echo. Other accounts remain independent. FollowersMax never changes. |
| Clock and persistence | Ready at the exact deadline, refused one tick before. Replacement, alt login, death, logout, and reload retain the account deadline. Old v22 account / v2 character fixtures default correctly; new fields round-trip; unknown versions still refuse. |
| Spawn and region policy | Every adjacent candidate blocked means no creature, slots, or cooldown. Wrong facet, house, guards, jail, safe/tutorial region, duel, and follower-forbidden encounter refused. Valid wilderness and dungeon tiles work. Parent regions and different Z floors are covered. |
| Target policy | Wild hostile target takes ordinary melee damage; player, companion, pet, summon, vendor, guard, escort, and initially innocent target do not. Exercise Attack, Guard, retaliation, bard manipulation, and a target becoming tame between selection and swing. No area or delayed attack can hit bystanders. |
| Lifetime and cleanup | Natural expiry, lethal damage, Release, Dismiss, dispel, direct deletion, owner death/logout/deletion, map/leash/region change, revoked rank, and disabled setting each delete the Echo and restore the exact prior follower count. Repeated and stale callbacks cannot remove a newer registry entry or subtract twice. |
| No farming | Backpack empty at construction and after Summon. Lethal damage, owner/friend kill, release, dispel, and expiry leave no corpse, carvables, trophy, map, or parts. Compare pre/post kill counters, AP, Renown, loot-box ledger, bestiary, requisition Leads, evo XP, and level-gear XP. Include a deletion-event case with Hits at zero. |
| Normal victims and coexistence | Echo damage to an ordinary victim uses normal master attribution; no automatic extra reward. A real Stygian Dragon retains its existing stats and death drops. Ordinary summon spells, pets, companions, League promotion, Register issue, and shop rows still pass existing regressions. |
| Real world save/load | Save during an active Echo and with the Tome in a nested pack. Reload into scratch state: Tome owner/current serial/deadline survive, Echo vanishes, registry is empty, no corpse appears, and follower slots reconcile correctly. |

Build changes through `docker/uo/build.sh` with a task-specific image and builder tag. Do not replace its test gate with direct docker build. All PowerShell verification uses `powershell.exe` 5.1. Run any runtime probe only in a throwaway, loopback-only, scratch-save container under the Golem's build lock. No Haven connection or deployment is part of these prompts.

Balance acceptance uses the same test character and equipment for repeated baseline and Echo-assisted fights, recording damage, time to kill, damage received, dispel timing, and deaths. Include an ordinary melee monster, a caster, a miniboss, and the real Stygian Dragon, then a party with several independently eligible accounts. Record actual values rather than promise a percentage improvement before measuring. Pass means the nominal profile has no hidden boss attacks, the Echo cannot solo a fresh test miniboss in its lifetime, it respects ordinary boss dispel, and a baseline losing party cannot turn a full-health boss into a trivial win just by rotating account Echoes. If it fails, tune the Echo's damage/hits first, document the new numbers, and rerun affected tests. Do not nerf the real creatures or add global pet restrictions.

The full world reload and appearance checks remain explicit release gates even after unit tests pass. The feature stays disabled until the separate activation decision; passing a build does not authorize changing a running configuration.

## Ordered Golem prompts

The overseer assigns real prompt numbers. These are sequential work packets with their intended scope, not newly queued jobs. Re-read main, applicable agreements, and this design before each. Keep each new prompt's notes in `shard-migration/notes/`; never edit migration `docs/`. No packet commits, deploys, or connects to Haven.

1. **Build Echo storage, runtime, and weak creature, disabled.**

   **Touches:** server

   Add settings, service, policy, and direct BaseCreature creature in the new paths above. Append the account deadline and character current-Tome serial with compatible schema reads. Implement summon transaction, timer/death cleanup, owner events, region/target policy, no-loot behavior, and load deletion. Include the runtime, schema, target, cleanup, and reward-exclusion tests. Observe red behavior before implementation and pass build.sh. Record the exact source seams, special-region types, schema versions, and mutation evidence. No Registrar entry or player-accessible call until packet 2. The feature defaults off.

2. **Build Tome issue, replacement, and player pages.**

   **Touches:** server

   Depends on packet 1. Add TomeOfEchoes and its gump; wire an Echo reward view into LeagueRegistrarGump. Reserve unused response IDs after inspecting current main. Keep rewards accessible at Celestial despite DrawRank's early return. Route claim, replacement, call, and dismiss through the service, with response-time owner, item, rank, and Registrar-range checks. No AP-shop row, loot-box source, new trial gate, or promotion grant hook. Add red-first ownership, full-pack, stale-reply, replacement, and slot/cooldown integration tests, then pass build.sh and existing League regressions. Keep enabled false.

3. **Prove full lifecycle, appearance, and combat balance.**

   **Touches:** server

   Depends on packet 2. Under the Golem's local build/test lock, use a disposable loopback-only shard with scratch saves. Run real save/reload during an active call, ordinary dispel, Release, all cleanup cases, no-reward probes, target restrictions, and group balance checks. Inspect the player package's book/body/hue rendering in a test client, without rebuilding or publishing the client. Record exact results and remaining failures. Tune only the Echo defaults or repair this feature, adding red-first regressions for defects found, and pass build.sh after any change. If a client asset change is actually required, report it and scope a separate client prompt; do not expand this server packet into client/map work. Leave activation off.

4. **Write the finished player guide and activation handoff.**

   **Touches:** docs-only

   Depends on packet 3's evidence. Put the wiki-ready guide, release-note text, proposed fidelity-register entry, verified numeric table, and test/client evidence in notes. State the enabled setting and how to disable while retaining schema readers; list any unverified checks. For future operator approval, identify the specific setting change and build already tested. Do not activate, publish, or use this packet as implied permission to touch a running shard. There are no service-inventory or console-button changes in the proposed implementation.

## P567 verification

Both work-copy AGENTS.md files, governing direction/task guidance, the relevant P405 sections, completed prompt, overseer answers, P565 boundary, and cited shard/pinned sources were read. `python tools/progress.py --dry-run` succeeded with SL_SHARD and SL_MIGRATE set to these work copies. Contrary to its help text, build() writes tools/progress.json at line 722 before main() checks --dry-run at line 737. The starting work copies were clean; that generated snapshot was restored to its exact starting contents so this task changes only the requested note. This is a reporter defect confirmed from its source and observed output, recorded here for the overseer, with no code fix in this design task. No new content counts are claimed from that output. No code tests, builds, deployments, or external-source execution were performed.

Final review confirmed the ordered prompts have Touches lines, the note contains no em dashes and is below 5 MB, the code work copy is clean, and the only pending migration-repo change is this note. The generated progress snapshot matches its starting bytes. Whitespace checks passed. The stop-request file was absent at the final step.

## Questions for Chase, with recommended answers

These questions finish the design; none blocks the requested notes task. The following defaults are proposals, while the high-rank weak Echo decision remains settled.

1. **Which high rank unlocks the Tome: Blaze, Mythril, or Celestial?** Recommend **Mythril**, the chapter 5 milestone, currently rank 15. It is late in the ladder and leaves time to use the reward before the last rank. Require current character rank, with no extra chapter replay for citizens promoted while trials were waived.
2. **Which appearance launches first?** Recommend **Echo of the Stygian Dragon only**, using existing body 826 and League blue. Keep later appearances cosmetic unless separately designed; no boss abilities or stronger Celestial upgrade.
3. **Are 20 seconds, two slots, and a 30-minute account cooldown the right starting numbers?** Recommend **yes**, with fixed weak stats above, no skill roll or mana cost, and the clock starting only on a successful spawn. Death, dispel, dismissal, and logout do not refund it. Confirm after the measured solo and party checks.
4. **Free earned ability or paid consumable?** Recommend **a reusable Tome issued and replaced free by the Registrar**, character-bound with one current serial. Rank earns it; copying, replacing, banking, or changing characters cannot buy another call. Leave the AP shop's existing policy intact.
5. **Where may it fight?** Recommend **PvE only on the five named non-Felucca facets**, outside houses and protected regions, with no player/pet attacks and no bypass of encounter follower rules. Use it against real monsters, including bosses, under their normal dispel and participation rules.
6. **What happens on travel, disconnect, death, or restart?** Recommend **the Echo dissolves and the recorded cooldown remains**. Keep the Tome and rank entitlement. No persistence of an active fighter and no automatic re-summon on login or load.

P567 DONE
