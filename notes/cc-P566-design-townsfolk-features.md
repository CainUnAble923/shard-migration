# P566: New Haven townsfolk conversations and inn rest

Written October 24, 2026. Design only. These features are proposed, not available to players yet. No code, client files, configuration, world, account, or service changed in this task.

## The decision this design carries forward

Give New Haven a small keyword conversation table and a paid, self-only rest service at its existing innkeeper. Build both after the tutorial core. Chase already chose both; the questions at the end concern the remaining details, not whether to build them.

The completed P405 prompt is `D:\UO\cc-prompts\completed\cc-P405-servuo-batch-1022-research.md`. It names its deliverable as `notes/cc-P405-servuo-batch-1022.md`, which is present. The P566 brief's `cc-P405-servuo-batch-1022-research.md` notes filename is absent. Use the actual [P405 research](cc-P405-servuo-batch-1022.md), especially its `conversational-townsperson` and `specialized-innkeeper` sections. Chase's answers are recorded in `D:\UO\overseer\decisions-2026-10-22.md:14`: both inn rest and the talk table, after P289 through P291. The completed prompt contains the research assignment; the overseer's decision log contains the answers.

These are native Shattered Legacy features inspired by the downloads. P405 describes unsafe reward actions, threaded conversation callbacks, double charging, and unrestricted combat healing. Carry the ideas forward, not that implementation. Third-party behavior and source locations below come from P405. The third-party scripts were not reread, executed, built, installed, or extracted in P566, as the brief directs us to work from P405's notes. Credit David and uploader Zavreyon for the conversation inspiration, and Zigholtul for the inn rest inspiration. P405 reports no stated licenses; no downloaded code or dialogue is part of this design's deliverable.

All numbers below are proposed defaults unless explicitly identified as existing source behavior. They are not playtest measurements or decisions already made by Chase.

## What exists now, and what to extend

Source snapshot: code work copy `1c9c5d8`, documentation work copy `7941129`; pinned ModernUO verified at `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`. Code paths in this note are relative to the ShatteredLegacy work copy unless marked `pinned/`. That prefix means `D:\UO\ModernUO-pinned\Projects\`.

| Existing source read | Consequence for this build |
|---|---|
| `Tutorial/ClusterFTutorial.cs`, `TutorialCoreTrials.cs`, `TutorialWingTrials.cs`, `TutorialTradeTrials.cs`, `TutorialGumps.cs`, `TutorialStations.cs` under `server/customizations/` | The tutorial core and wings are implemented in this snapshot. Conversations add flavor and directions. They do not complete lessons, advance loops, award graduation rewards, lend skills, or replace Rook's menus. |
| `server/customizations/Tutorial/TutorialRecruiter.cs:24`, `TutorialCorePlacement.cs:19`, `:31`, `:66` | Rook stands at `(3500,2572,14)`. Core props occupy nearby tiles. Follow the existing test-world and whole-plan placement checks; do not put a greeter on the arrival tile or lesson marks. |
| `server/customizations/ClusterFNewHavenSeeder.cs:27`, `:70`, `:85` | Asandos already occupies the inn; the League registrar has a canonical anchor. Leave both alone. Use existing anchors in directions rather than duplicating a registrar or quest giver. |
| `server/customizations/ClusterFNewHavenServicesSeeder.cs:212`, `:244` | Town services already have an idempotent seeder and dry run. The new residents need a separate, narrow seeder, not a rerun of all town decoration. |
| `pinned/UOContent/Mobiles/Vendors/NPC/InnKeeper.cs:7` | `InnKeeper` is partial and has no speech or context-menu override of its own. Add a partial extension in our canonical tree. Existing saved innkeepers keep their type, inventory, vendor behavior, and save chain. |
| `pinned/../Distribution/Data/Spawns/post-uoml/trammel/Vendors.json:658` | Stock innkeeper spawner GUID `32b9ee94-88a7-4591-ad3c-898b09d9f053`, anchor `(3501,2517,27)` Trammel, walking range 4. This is a data declaration, not proof an innkeeper is present in a running world. |
| `pinned/../Distribution/Data/regions.json:1631` | The inn is the child region `the New Haven Inn`, under `New Haven`. Its area is two rectangles, not the entire bounding box. Use region membership. |
| `pinned/Server/Regions/Region.cs:545` | `IsPartOf(string)` follows the region ancestry. A child region inside the inn or town must work. Check Trammel separately. |
| `pinned/UOContent/Mobiles/BaseCreature.cs:2874`, `:2878`; `pinned/UOContent/Mobiles/AI/VendorAI.cs:89`, `:100` | Speech reaches a creature's speech type and AI. Vendor buy and sell commands must retain priority. Do not replace the stock speech handler or vendor AI. |
| `pinned/Server/Mobiles/Mobile.cs:5590`, `:5728`; `pinned/Server/Events/SpeechEvent.cs:21` | The global speech event precedes NPC dispatch; NPC dispatch is sorted by distance. Prefer the NPC overrides below and explicit selection of one resident. No global speech listener is needed. |
| `pinned/Server/Events/AggressiveActionEvent.cs:22`, `:67`; `pinned/Server/Mobiles/Mobile.cs:3803`, `:2060`, `:8599` | There is a real aggression event and a virtual `OnHitsChange(int oldValue)` hook. Together they can remember recent harm without copying or patching engine combat code. |
| `pinned/Server/Mobiles/AggressorInfo.cs:30`, `:93`; `pinned/Server/Mobiles/Mobile.cs:2043` | Aggression expires after two minutes by default. Full health clears damage entries. Neither the current combat target nor the damage list alone is reliable recent-combat history. |
| `pinned/UOContent/Mobiles/PlayerMobile.cs:391`, `:3467`; `pinned/UOContent/Mobiles/BaseCreature.cs:1158`, `:2625`, `:3333` | `AllFollowers` contains creatures registered through the shared master field, including summons. `GetMaster()` resolves control or summon ownership. Use this existing collection for admission checks. |
| `server/customizations/ClusterFAccountData.cs:1081`; `Tutorial/ClusterFTutorial.cs:54` | `ClusterFAccountPersistence.Get` is read-only. `ClusterFTutorial.RecordOf` calls `GetOrCreate`, so it is unsuitable for our read-only flavor lookup. |
| `pinned/Server/Items/Container.cs:796` | `ConsumeTotal(typeof(Gold), fee)` prechecks the total, then consumes across stacks. Use its one Boolean result, once. |
| `pinned/UOContent/Items/Weapons/Abilities/BleedAttack.cs:59`, `MortalStrike.cs:42` | `IsBleeding` and `IsWounded` are available. Rest must respect these effects and poison. |
| `server/customizations/ClusterFCreatureLevels.cs:259`; `Tutorial/TutorialStyle.cs`; `Tutorial/ClusterFTutorial.cs:64` | Private NPC overhead text and readable tutorial gump styling already exist. Reuse their patterns. |
| `server/customizations/ShardClilocs.cs`; `player-package/vendor/shattered-legacy-cliloc/entries.json`, `registry.csv` | A literal Rest context entry needs a shard cliloc and package update. Ordinary gump strings and speech do not. |
| `docker/uo/Dockerfile:51`, `:94`; `docker/uo/apply-patches.sh` | C# customizations and tests are mirrored, but an arbitrary new JSON file is not. Budget an explicit data-copy step into both builder distribution data and the runtime image. |

Also read P80, P289, P475, P480 and the current tutorial guide evidence in P525. The later tutorial reviews P420, P503 and P523 describe unresolved concerns and runtime limits. P566 does not certify those issues fixed. The prerequisite has landed in source; the build prompts must recheck main and its tutorial fix queue before integration. P481's proposed secluded starting area is separate. Townsfolk remain in public New Haven and never become a condition for entering or graduating from a future tutorial area.

## What players see

### Conversations

A player can stand within three tiles of a resident and say `hello`, `name`, `job`, `rumors`, `help`, `inn`, or `goodbye`. Double-clicking a new resident, or choosing the existing localized Talk context entry, opens a compact topic menu with those same topics. The menu is the discoverable route for a player who does not know a keyword. It has no text-entry box and grants no reward.

Launch profiles are `plaza`, `trades`, and `innkeeper`. The first two belong to new, stationary residents. The third belongs to stock innkeepers while they are inside the New Haven inn. Do not attach the generic talk menu to every trainer, banker, quest giver, Rook, or the Farmhand. Their existing interactions stay authoritative.

One accepted topic produces one private overhead line from the chosen NPC, visible to the speaking player and recorded normally in that player's journal. Use the NPC as the speaker. Ordinary residents speak as people; they do not impersonate the System or an Echo. The table can provide dry humor consistent with the setting, but it must not add `System:` prefixes, global announcements, reward fanfare, or tutorial completion claims. Keep the existing Echo and System voices in their established tutorial paths.

Suggested opening content, written for us rather than copied:

| Profile and topic | Proposed line or behavior |
|---|---|
| Plaza, hello | "Welcome to New Haven. The paperwork survived. We are still checking on everything else." |
| Plaza, help, this character is in the core | "Rook Hallowell is the League recruiter by the plaza. Double-click him to continue your lessons." |
| Plaza, help, visitor or graduate | "The bank is by the plaza. The League registrar keeps an office to the south. Ask me about the inn if you need a rest." |
| Trades, job | "I keep the work moving. Tools, materials, then practice. The guilds can help with the first two." |
| Trades, help | "Speak to the guildmaster for the craft you want to learn. Your tutorial's optional lessons are still with Rook." |
| Any profile, inn | "The Bountiful Harvest Inn is north of the plaza. Its innkeeper offers a paid rest once you are safely out of a fight." |
| Innkeeper, job | "Food, drink, and a place to catch your breath. Say rest if that last part needs help." |
| Innkeeper, rumors | "People arrive with empty pockets and very full plans. We sell breakfast to both." |
| Any profile, goodbye | "Safe travels. Come back with a story you can tell indoors." |

The release data must supply name, job, hello, help, inn, rumors, and goodbye for each launch profile, using the actual NPC name for the name response. Supply at least two rumor lines per profile. Directions must describe landmarks visible in the current map. They must not advertise unfinished sockets, Town Houses, inn rooms, League summons, or other planned features as available. No exact time-of-day topic in version one; add it only when useful content needs it.

### Inn rest

At the Bountiful Harvest Inn, saying exactly `rest` or choosing Rest on the innkeeper opens a confirmation window. The innkeeper's Talk menu also has a clearly labeled `Rest...` button. All routes open the same quote. They never debit on speech or on opening the menu, and they never ask the player to target another character.

The quote says:

> Rest at the Bountiful Harvest Inn
>
> Restore your health, stamina, and mana to their current maximums. Cost: 25 gold from your backpack.
>
> You must be out of combat for two minutes. Rest does not cure poison, bleeding, or mortal wounds. You can rest again after one minute.
>
> Pay 25 gold and rest | Cancel

On success, set the three pools to their current maximums and say privately, "You rest at the inn. Health, stamina, and mana restored. Paid 25 gold." Restoration is immediate after confirmation; there is no channel, teleport, bed allocation, lodging contract, bonus regeneration, or temporary maximum-stat buff. Rest restores only the payer. Pets and companions receive nothing. Young, tutorial, veteran, skipped-tutorial and remedial characters pay the same fee. A character with all three pools full gets "You are already rested" without a charge or cooldown.

This is a town convenience and a small gold sink. It gives no XP, skill gain, level progress, renown, achievement, item, or League credit. It does not replace healer resurrection, veterinary care, the tutorial farm's teaching, or the separate F-44 inn-room proposal.

## Numbers and eligibility

| Setting or rule | Proposed default |
|---|---|
| `clusterf.townsfolk.enabled` | `false` until the isolated acceptance pass and Chase's activation |
| `clusterf.townsfolk.rest.enabled` | `false`, independent of conversations |
| `clusterf.townsfolk.seedOnWorldLoad` | `false`; never seed on an ordinary load by default |
| Conversation and menu interaction range | 3 tiles, with same map, visibility, and line of sight |
| Speech accepted | Regular speech or whisper; no yell, spell, emote, guild, alliance, command, or ghost speech |
| Conversation cooldown | 3 seconds per player across all profiles and both input routes |
| Repeated identical topic | 15 seconds per player/NPC/topic; silence on throttled speech |
| Rest fee | 25 backpack gold, flat fee, no bank withdrawal or bank check |
| Rest quiet period | 120 seconds after the most recent harmful action involving the character or its controlled/summoned creature, or any decrease in the character's hits |
| Successful rest cooldown | 60 seconds per character across every eligible innkeeper |
| Quote lifetime | 30 seconds; one outstanding quote per player |
| Startup rest hold | 120 seconds from world load, to cover transient combat history lost on restart |
| New residents | Two, listed in the placement section; no ambient speech timer |

Expose fee, ranges, conversation cooldowns, quiet period, rest cooldown and quote lifetime through `ServerConfiguration.GetOrUpdateSetting`, using the prefix above (`rest.fee`, `talkRange`, `talkCooldownSeconds`, `repeatCooldownSeconds`, `rest.quietSeconds`, `rest.cooldownSeconds`, `rest.quoteSeconds`). The startup hold must be at least `rest.quietSeconds`. Validate the entire settings group: positive durations, fee at least 1, range 1 through 3. If invalid, disable the affected feature with a clear startup diagnostic instead of silently clamping a price or enabling free healing. These are independent settings, not a new console UI.

Both payer and innkeeper must be alive, undeleted, on Trammel, and in `the New Haven Inn` or one of its descendants at quote and confirmation. The innkeeper must be an `InnKeeper`, including a derived stock-compatible type such as our `GargoyleInnKeeper`. Check region membership, three-tile range, visibility and LOS again at confirmation. The inn's stock spawner can wander, so a vendor outside the inn cannot offer rest. The broad town region alone is insufficient. The two inn rectangles in source are the authority; do not use the approximate rectangle reported in P405 as an access check.

Refuse rest while the payer is criminal, has five or more kills, has a combatant, has an unexpired incoming or outgoing aggression entry, is inside the remembered quiet period, is poisoned, is bleeding, or is mortally wounded. Refuse while any currently controlled or summoned creature owned by that payer has a combatant or active aggression. Remembering the owner's timestamp prevents dismissing, stabling, releasing, killing, or deleting the creature from instantly clearing the quiet period. Track aggression involving the player as victim as well as attacker, including lawful monster combat and zero-damage harmful attempts. Rest is not permitted while hidden; require the player to reveal normally rather than silently revealing them as a side effect.

Use refusal messages that explain what the player can do: "Step inside the inn and come closer," "Leave combat before resting," "Wait 43 more seconds before resting," "Have your poison treated before resting," "You need 25 gold in your backpack," or "This offer expired. Ask the innkeeper again." No charge, restoration, or success cooldown on refusal. Report the longest remaining combat/cooldown/startup wait, rounded up to whole seconds. Do not promise an exact timer while an active combat target or aggression record still blocks rest.

## Implementation shape

All paths in this section are proposed additions or edits, not files created by P566.

| Path | Responsibility |
|---|---|
| `server/customizations/Townsfolk/ClusterFTalkRules.cs` | JSON model, strict validation, immutable loaded table, topic normalization, profile and tutorial-phase filtering, reload diagnostics |
| `server/customizations/Townsfolk/ClusterFTownsfolk.cs` | New resident class with serialized stable `TownsfolkTag`; fixed identity/outfit by tag, stationary, invulnerable, no loot or skill teaching; NPC speech, double-click and Talk context hooks |
| `server/customizations/Townsfolk/ClusterFTownsfolkService.cs` | Eligible candidate selection, cooldowns, private responses, shared eligibility checks, topic-menu responses |
| `server/customizations/Townsfolk/ClusterFInnKeeperExtension.cs` | Partial `Server.Mobiles.InnKeeper`; gated talk/rest speech and context entries on existing instances, delegating to services |
| `server/customizations/Townsfolk/ClusterFInnRest.cs` | Quote, player-bound confirmation, eligibility, single gold debit, pool restoration and cooldown |
| `server/customizations/Townsfolk/ClusterFInnRestCombat.cs` | Aggression subscription, transient per-character timestamps, partial `PlayerMobile.OnHitsChange` override and pet-owner checks |
| `server/customizations/Townsfolk/ClusterFTownsfolkSeeder.cs` | Test-only dry run and placement of the two owned residents; report existing innkeeper/spawner without replacing them |
| `server/data/townsfolk-talk.json` | Canonical authored dialogue table |
| `docker/uo/Dockerfile` | Copy dialogue into builder `Distribution/Data/ShatteredLegacy/` before publish/tests; make the identical file available at runtime `/modernuo/Data/ShatteredLegacy/townsfolk-talk.json` |
| `server/customizations/ShardClilocs.cs`, package cliloc `entries.json` and `registry.csv` | One new Rest label; allocate an unused number in the existing block at implementation |
| `server/tests/Townsfolk/` | Behavioral, persistence and integration facts described below |

Subdirectories mirror into ModernUO's UOContent project through the existing assembly pattern. Namespaces must match the extended types: `Server.Mobiles.InnKeeper` and `Server.Mobiles.PlayerMobile`. Do not add a second serialization-generator attribute or serializable member to those partial stock classes. The new resident uses ModernUO generated serialization with a stable tag. Never change its parent after release.

No upstream patch is required by this design. We checked that pinned PlayerMobile and our canonical files do not already implement `OnHitsChange`. An additive partial can override it, record a hit decrease, then call base. Subscribe once to `EventSink.AggressiveAction` during configuration. Record both principals and their player masters when applicable, using `BaseCreature.GetMaster`; do not retain the pooled event-args object. Keep timestamp state directly on the player partial as ordinary, nonserialized fields. This avoids an ever-growing dictionary and does not change account or mobile save layouts. Health reductions from noncombat causes also begin the quiet period; that conservative rule is intentional.

At admission also inspect the player's and owned creatures' current combat state. Iterate `PlayerMobile.AllFollowers` if non-null, selecting undeleted `BaseCreature` instances whose `GetMaster()` is the payer. This covers the shared control/summon master registration in pinned `BaseCreature.AddFollowers`; check no unrelated stale entry grants a block. A pet can fight outside the inn, so do not filter by map or distance. The existing companions code also uses this collection in `Companions/CompanionParty.cs:36`. No new ownership index, world scan or periodic scan is needed. Reconcile the latest source for signature collisions before building; a new upstream override should fail compilation rather than hide a second implementation.

Rejected approaches: replacing or subclass-swapping saved innkeepers would require avoidable world edits; a global speech hook runs before NPC/region handling; copying VendorAI would drift; a PlayerMobile damage patch is unnecessary when the virtual hit-change hook covers our rule; account persistence is unnecessary for a one-minute service cooldown. Transient timestamps survive ordinary logout on the same mobile, and the world-load hold covers restarts. No existing combat, healing or skill-gain calculation changes.

### Speech and menu contract

Normalize at most 160 characters by invariant case folding, trimming, punctuation-to-space and collapsed whitespace. Compare whole words or explicitly listed phrases, never unanchored substrings or author-supplied regular expressions. Examples: `hello`, `hello there`, `what is your name`, `what is your job`, `any rumors`, `where is the inn`, and `goodbye`. `forest` must not match `rest`, and an ordinary sentence containing `job` must not automatically trigger a reply. Overlength or unknown input gets no automatic answer. The Talk menu can always show the supported topic names.

Reserve `rest` as an exact service command, plus the exact optional form `<current innkeeper name> rest`. It opens the quote, never the dialogue table. Reserve vendor buy/sell keywords, training, bank, guards, pet orders, guild commands and tutorial commands from generic topic matching. For reserved non-rest speech, call the inherited behavior and do nothing else. For an eligible topic, use a shared selector across nearby registered residents and eligible innkeepers: an explicitly addressed full NPC name wins; otherwise choose shortest squared tile distance, then lowest mobile serial. Only that NPC handles the topic. Do not let engine iteration order determine who replies.

`HandlesOnSpeech` adds our narrow eligibility to `base.HandlesOnSpeech`. For speech the service owns, the selected NPC marks `e.Handled` and replies privately; it never sets `e.Blocked`. For unrecognized speech, call base unchanged. An already handled event produces no additional flavor response. Innkeeper overrides must preserve the stock speech-type/AI path for all unrelated commands. Test the actual dispatch path, not only direct calls to a matcher, including two equally close residents and an innkeeper using normal buy/sell speech.

Double-click/Talk targets a specific resident and therefore needs no nearest-NPC arbitration. Every topic button rechecks the player's identity, NPC existence, same map, range, visibility, LOS and region; it shares speech cooldowns. Opening/reopening the menu has no greeting side effect and does not reset cooldowns. Menus expire on logout or deletion and are bound to the current NetState, player and NPC. A stale menu after reload resolves its topic against the current valid table; a removed topic closes cleanly.

All matching and responses run synchronously on the game thread. There is no worker, task, sleep, dynamic type creation, reward action, item filter, AI change, access-level change or delayed reward. Random selection is among currently matching authored responses, excluding the most recent line when alternatives exist. Keep only the latest topic/response timestamps per profile on each player; the launch profile/topic set is finite. No raw player speech is logged.

### Dialogue data contract

Use `schemaVersion: 1`, with a profile list keyed by `tag`. Each profile declares an allowed region key and topic list. Each topic has a unique `id`, an allowlisted alias list, and a response list. A response contains plain `text` and `phase`, where phase is `any`, `core`, or `afterCore`. An exact phase response takes precedence over `any`; otherwise fall back to `any`. There must be an `any` fallback for each topic. Profile tags are exactly the launch tags above until a later prompt extends the allowlist. Unknown action fields and unknown enum values are errors, not ignored instructions.

For phase selection, read `ClusterFAccountPersistence.Get(account)?.Tutorial` if the player has an account, then require the record's `CharacterSerial` to match that player. Do not use `ClusterFTutorial.RecordOf`, because its `GetOrCreate` call can allocate account data. `core` means an active unfinished core for that character; `afterCore` means `CoreDone(record)` for that character. Everyone else, including another character on the same account or an account with no stored record, uses `any`. These checks are read-only. They do not call `Observe`, `CompleteStation`, `Graduate`, or any reward API.

Example entry fragment:

```json
{
  "id": "help",
  "aliases": ["help", "where do i start"],
  "responses": [
    {"phase": "core", "text": "Rook Hallowell is the League recruiter by the plaza. Double-click him to continue your lessons."},
    {"phase": "any", "text": "The bank is by the plaza. The League registrar keeps an office to the south."}
  ]
}
```

Limit the full file to 256 KiB, 8 profiles, 16 topics per profile, 12 aliases per topic, 8 responses per topic, 80 characters per alias, and 240 characters per response. These are parser limits, not claimed present content counts. Reject duplicate profile/topic/alias keys, missing launch topics, conflicting aliases, absent fallbacks, markup, control characters, and reserved commands. Escape any dynamic NPC name before putting it in gump HTML. The only runtime substitution initially needed is the NPC's name; no arbitrary template expressions or type names.

Load `Data/ShatteredLegacy/townsfolk-talk.json` once at startup and allow an Administrator-only `[ClusterFTownsfolk reload` command on the game thread. Load and validate a candidate table before swapping it. Invalid reload retains the previous table with a filename and concise validation errors. Missing or invalid initial data disables talk and its menus with a clear diagnostic; it does not crash the shard, overwrite the canonical data, or silently create generic filler. Inn rest continues independently. No file watcher, HTTP endpoint, Haven service, new volume or new port is needed. The build must exercise the shipped data path as well as the parser so a missing Docker copy cannot pass unnoticed.

### Payment and confirmation contract

The outstanding quote holds player, issuing NetState/session, innkeeper, fee, settings generation, issued time and a one-use token. A new quote invalidates the old one. Confirmation consumes that token before attempting any mutation. Cancel, logout, expiry and duplicate response consume or invalidate it without payment. Neither the button ID nor a saved reference to another player is authority to pay.

At confirm, validate the session, token, settings generation and deadline, then repeat every eligibility check and reread current pool maximums. A configuration/fee change expires the quote and asks the player to reopen it. Regeneration to all-full cancels without charge. One missing pool is enough to use rest; all three do not have to be missing. If at least one is missing, the flat fee remains 25, regardless of the quoted deficits.

On the game thread, with no yield or timer between checks and effects: call `payer.Backpack?.ConsumeTotal(typeof(Gold), quotedFee)` once; only if it returns true, set Hits, Stam and Mana to their current maxima and record the success cooldown. Never perform an additional stack search or `Consume` call. Never use `Banker.Withdraw`, target another mobile, or consume a practice-token item as gold. Rest adds no maximum-stat modifier. The hit-change hook must record decreases only, so our own healing cannot set the combat timestamp. Record a concise internal diagnostic if an unexpected exception occurs; do not swallow it and charge again on a retry. Preserve engine single-threaded payment semantics rather than adding background operations.

## Placement and safe world adoption

Proposed resident identities and candidate positions:

| Stable tag | Display identity | Candidate position on Trammel |
|---|---|---|
| `plaza` | Mara, the town steward | `(3508,2582, ground Z)` just south of the plaza |
| `trades` | Ellis, the workshop runner | `(3474,2544, ground Z)` near the smithy |
| `innkeeper` | Existing innkeeper's current name and title | Stock spawn anchor `(3501,2517,27)`; do not move the vendor |

Mara and Ellis are proposed new names. The two new positions have not been checked against loaded maps or current props. Their XY values are concrete first candidates, not instructions to force placement. Compute ground Z from the loaded map and require `CanFit`, town-region membership, no door/stairs obstruction, no tutorial mark or NPC collision, and a reachable adjacent interaction tile. If any candidate fails, the entire seed refuses without placing either resident. Report the offending point and choose a corrected point in the implementation note after map inspection. Do not fall back to `(0,0,0)`, slide silently, alter terrain, or move existing objects.

Use `[ClusterFSeedTownsfolk dryrun]` and `[ClusterFSeedTownsfolk]`, Administrator only and test-world only, with the same `ClusterFStaffHub.IsTestShard` guard used by tutorial placement. Dry run reports proposed placements, matching existing tags, blockers, missing data and the innkeeper/spawner status. A rerun identifies our residents by type and serialized tag, never by display name. Existing duplicates or moved residents are reported, not automatically deleted or relocated. A saved resident needs no spawner or respawn timer because it is invulnerable and cannot be killed normally. If it is missing, a deliberate rerun can restore it. Do not automatically create an innkeeper: report a missing stock spawner/vendor for staff to resolve through the existing stock-spawn tools.

Provide `[ClusterFRemoveTownsfolk dryrun]` and `[ClusterFRemoveTownsfolk]`, under the same test-only and Administrator gates, limited to these owned resident tags. Removal never deletes a stock innkeeper, spawner, quest giver, or an unrecognized custom resident. Setting talk/rest off immediately prevents new responses or payments, invalidates quotes, and leaves saved residents harmless. That is the normal rollback; it needs no save conversion. Administrator commands use existing command discovery. No new Shard Console button is planned. If a later prompt adds one, P187 requires its web twin through the same action functions.

## Art and client needs

Use existing human bodies, clothing, hair, standard item hues, context menus, gump background and button art. Make the new NPC outfits fixed by tag, with a readable name and role. Reuse `TutorialStyle` for light text and clear action labels on a dark panel; long text must wrap and a small client window must not clip buttons. No new bitmap, sprite, animation, map patch, sound, music, body ID or tiledata entry is needed. There is no art Chase needs to make, so no art request is required for this scope.

Talk uses verified stock cliloc 3006146, as `LeagueRegistrar.cs:96` already does. Rest needs one new cliloc. At this snapshot 1900014 is absent from both the server constants and package registry, but the implementation must recheck and reserve the next free number rather than assume it remains free. Keep the constant, `entries.json` and append-only `registry.csv` synchronized. Include the client text before players rely on the new context row. An older package may show an empty Rest row, as documented in `ShardClilocs.cs`; exact speech `rest` and the server-rendered Talk menu button remain usable. No TazUO source patch or custom packet is needed. This design does not publish a player package.

## Tests required at implementation

P566 adds or runs no lane tests. The following are future behavioral tests, not assertions already verified. Every new test must be observed failing before its production change, then passing. Record the failed assertion and successful run. A compile error alone is not evidence of the intended behavior failing. For a brand-new type, add a minimal callable no-op surface if necessary to obtain a real failing assertion, then implement it. Use the existing sequential shard test host, controlled clock and fake NetState patterns; do not let wall-clock sleeps make cooldown tests flaky.

| Area | Required observable cases |
|---|---|
| Table and packaging | Shipped launch table loads from the builder's distribution data path; strict size/schema/alias/fallback checks; invalid startup disables talk; invalid reload keeps the old table; successful reload swaps atomically; missing file is not silently fabricated. Verify the same data bytes in the final throwaway image. |
| Speech delivery | Whole-word/phrase matches, punctuation and case, `forest` not `rest`, overlength and unknown input; nearest and equal-distance tie selection; explicit name selection; one private reply to the right NetState; no reply to ghosts/yell/spell traffic or through walls; normal buy/sell/teach/bank/guards/pet commands unaffected. |
| Talk menu | Same eligibility/cooldowns as speech; stale NPC, map/range/LOS change, table reload, logout/reconnect, closed/replayed gump, wrong player/session all refuse safely; opening a menu grants nothing. |
| Tutorial integration | Own in-core record gets the core help line; another character on the account gets visitor text; graduate gets general directions; an account with no stored record gets visitor text without creating one; reading any topic leaves tutorial state, lesson evidence, account data and reward counters unchanged. |
| Rest success and money | Each one-pool deficit and a three-pool deficit; exact fee across multiple/nested gold stacks; insufficient gold leaves all stacks unchanged; bank-only funds fail; one successful response removes exactly one fee and restores the payer only; unrelated players, pets and companions unchanged. |
| Rest callback races | All-full before/after quote, expired quote, changed price/settings, replaced quote, duplicate confirm, second innkeeper, moved/deleted vendor, map/LOS/region change, logout/reconnect and foreign session. None can charge twice or use stale eligibility. |
| Combat and effects | Player attacker and victim; lawful monster fight; zero-damage aggression; pet/summon owner attribution; combatant still active; poison, bleeding, mortal wound, hidden, criminal and murderer refusal; lost health from a trap; enemy/pet deleted or released after combat; full heal and clearing a combatant do not erase remembered harm. Exercise the real aggression event and Hits setter, not just a directly assigned timestamp. |
| Time boundaries | Quiet period and success cooldown one tick before, at and after expiry; latest harm extends the deadline; ordinary logout preserves the mobile timestamp; world load imposes its hold after restart; failed requests never set success cooldown. |
| World and save | Test-only gate, all-or-nothing preflight, dry run has no mutations, rerun is idempotent, moved/duplicate residents reported, missing stock innkeeper not replaced; resident tag/outfit round-trip; existing InnKeeper and GargoyleInnKeeper save chains unchanged; removal touches only owned residents. |

Run `docker/uo/build.sh` with a unique task tag, its required locks and the full shard gate. Do not replace it with direct `docker build` or a zero-test filter. Use Windows PowerShell 5.1 for the package Pester cliloc checks, including an intentional missing-entry failure before the new label passes. The existing cliloc test path is `player-package/tests/Cliloc-Overrides.Tests.ps1`.

Finish with a private, loopback-only throwaway shard, scratch saves, no copied live accounts, and a current player client. Check actual journal/overhead text, topic menu contrast, stock buy/sell, Rest label with updated package, fallback routes with the prior package, payment, walking out of the inn before confirming, combat and pet combat refusal, then restart and repeat placement. Save/reload must retain both residents without duplicate creation. Record which client/package was used and what remains unverified. No Haven connection, live-stack build, deployment, restart, or activation is authorized by those build prompts.

## Ordered Golem prompts

These are prompt outlines for the overseer to number after Chase reviews the defaults. Touches lines include the real build surface; every implementation prompt also writes its own `notes/` evidence. Keep this sequence, since later prompts consume earlier APIs. Recheck current main and open tutorial fixes at claim time.

1. **Townsfolk table, speech and topic menus.**

   **Touches:** server

   Add the table, strict loader/reload, resident type, dialogue/menu service and canonical JSON. Wire the builder/runtime data copies. Use the three launch profiles and content contract above, but do not seed a world or add the inn service yet. Settings default off. Prove parser, shipped-data, speech dispatch, privacy, cooldown and tutorial-read-only behavior red then green. Run the full build gate. Deliver code and the completed source/behavior note, with no deployment.

2. **Inn rest and existing-innkeeper integration.**

   **Touches:** server, client-package

   Depend on prompt 1. Add the gated InnKeeper partial with talk and rest, transient combat history using the verified event and virtual hook, pet-owner eligibility, quotes, atomic gold payment and restore, and one Rest cliloc across server and package. Preserve saved vendor types and ordinary vendor speech. Implement all rest and callback tests plus real hook-reachability tests, seeing them fail first. Run the full build gate and PS 5.1 cliloc checks. Keep features off by default. Do not publish the package or start a live shard.

3. **Placement and isolated acceptance.**

   **Touches:** server

   Depend on prompts 1 and 2, including the updated local client text. Add the narrow test-only seeder and owned-resident removal/dry run. Verify candidate tiles against loaded maps; publish the final point list beside the map checks. Prove seed refusal, dry run, idempotence and save round-trip red then green. Run the full build gate, then the isolated client/server acceptance described above. Report acceptance blockers as blockers; do not enable the service on a running shared shard. Deliver the exact later activation/rollback instructions for Chase using existing settings and commands.

4. **Player guide and overseer handoff.**

   **Touches:** docs-only

   Depend on prompt 3's verified behavior. Write `notes/wiki-drafts/new-haven-townsfolk-and-rest.md` and a handoff note listing actual names, locations, phrases, price, timers, backpack payment, refusal rules, package label requirement and activation status. Cross-check the tutorial guide so it directs players to the same recruiter and inn. Mark these features planned until Chase activates them. Supply a proposed invented-content fidelity-register entry for the overseer to promote; do not edit `docs/` or publish to Haven. No new tests are needed for this prose prompt.

The fidelity-register handoff should say: custom New Haven resident dialogue and a paid out-of-combat self restore are native shard content, independently disabled by default; stock NPC services, account progression and OSI quests are unchanged. The overseer assigns any D-number at implementation. P566 neither reserves one nor edits the register.

## Validation and limits of this design

Read both work-copy AGENTS.md files first, the governing-document index, direction decision, task list, subsystem policy, fidelity principle and standing question answers. Checked the actual P405 filename, completed prompt, overseer answer log, current canonical shard sources, related tutorial notes and pinned engine sources listed above. No `server/uo/` build tree or live configuration was read. No online search was needed for this local design.

Unverified: presence and position of the stock innkeeper in a running world; the two proposed resident tiles; gump/overhead appearance and old-package fallback in a client; actual runtime combat, payment, serialization and restart behavior. These are explicit implementation acceptance requirements, not completed P566 checks. No art was generated, no account-affecting action was taken, and no service was contacted. No code or tests were changed.

Validation: the requested UTF-8 note is below 5 MB and has no em dashes, replacement characters or trailing whitespace. Both repositories passed `git diff --check`; the code work copy is unchanged and the documentation work copy contains only this new note. No `docs/` file changed. Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies; exit 0. That tool writes `tools/progress.json` even in dry-run mode. Captured and restored its original bytes, confirming an exact match, so the requested note remains the only deliverable. No commits, merges, pushes or branch switches were made. Stop-request checks between steps found no request.

## Questions for Chase

These are design choices for the next build prompts. The recommended answers above make the design implementable without reopening the approval of both features.

1. **What should rest cost?** Recommended: **25 gold flat, paid from the backpack, with no Young/tutorial exemption.** Alternative: price by missing pool points. Flat pricing is easy to understand, quote and verify. No live economy measurement supports a finer formula yet.
2. **Should restoration take time?** Recommended: **instant on confirmation after 120 seconds free of harm, then a 60-second reuse cooldown.** Alternative: add a short interruptible rest channel. The quiet period and effect checks protect combat; a channel adds cancellation and payment state without a distinct player benefit in this first release.
3. **How many NPCs should answer at launch?** Recommended: **Mara by the plaza, Ellis by the smithy, and the existing innkeeper only.** Alternative: also add profile hooks to trainers and quest givers after this release. The small roster lets us verify voice, directions and speech-command coexistence before expansion.
4. **Who speaks in the dialogue?** Recommended: **ordinary residents use their own voices, with understated humor; the existing tutorial keeps its System/Echo speakers.** Alternative: explicitly author a separate Echo resident later. No random resident should silently become an omniscient tutorial narrator.
5. **Where should rest be available?** Recommended: **only the Bountiful Harvest Inn in New Haven at first, including its stock-compatible gargoyle innkeeper if present there.** Alternative: expand to selected inns after the first acceptance pass. This does not create a rented room or Town House.
6. **Should there be a literal Rest context entry?** Recommended: **yes, with one package cliloc update; keep exact speech and the Talk-menu button as fallback routes.** Alternative: ship only the server-rendered Talk menu and speech, which avoids the label update. No new art is needed either way.

P566 DONE
