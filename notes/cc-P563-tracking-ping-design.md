# P563: Tracking Ping

October 24, 2026. Design only. All new numbers below are recommendations for Chase, not implemented behavior or settled tuning.

## Recommendation

Build the refreshed radar version. At 90 Base Tracking, a player can send a short pulse that finds many nearby creatures, counts them, and lights up every eligible result on TazUO's mini map. The dots move with the creatures during the pulse. A results gump lets the player choose one quarry for the normal tracking arrow. Clients without the new patch receive the same filtered count in chat and can open the results gump.

This is an invented shard ability inspired by Carl's map in Dungeon Crawler Carl. It is not an OSI content port. The mini map is the main display, not an optional replacement for a list. A text-only implementation is a useful first builder step, but does not complete Chase's October 24 direction.

## What exists today

Source snapshot: code work copy HEAD `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`; notes work copy HEAD `98bfd6cc157a0cc9f15a323412e14e5a8933b0c4`. Both were clean at entry. No remote freshness or deployment claim is made.

Paths below use `C/` for this work copy's `server/customizations/`, `P/` for `server/patches/`, and `U/` for read-only `D:/UO/ModernUO-pinned/Projects/UOContent/`. ModernUO HEAD is `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`. No `server/uo/` files were read.

### Server Tracking

- `U/Skills/Tracking/Tracking.cs:35-48,86-133`: using Tracking opens Animals, Monsters, Human NPCs, or Players and sets a 10 second skill delay. The first category check is Tracking 0..21.1.
- The same file, `:145-168,234-302`: after that check succeeds, the category search makes a passive 21.1..100 gain call, even if the search subsequently finds nothing. It keeps only the nearest 12 eligible mobiles. Categories use body type, not hostility. Under AOS it rejects dead targets and protects hidden staff. Ordinary hidden players are not categorically excluded. Player selection rolls Tracking and Detect Hidden against Hiding and Stealth, with elf and transformation adjustments (`:305-354`). It has no explicit line-of-sight, wall, or dungeon-floor filter in that search.
- [Tracking-radius-osi.patch](../../ShatteredLegacy/server/patches/Tracking-radius-osi.patch), registered by `docker/uo/apply-patches.sh:561`, changes the range input to `ClusterFSkillClamps.TrackingRangeSkill`. `C/ClusterFSkillClamps.cs:82-83` caps a player's input at 100. The formula remains `10 + floor(skill / 10) * 10`, so GM and higher players search at most 110 tiles. Ping's smaller range must be separate from this clamp.
- `U/Skills/Tracking/Tracking.cs:358-375` starts one `TrackArrow` at twice the search range and calls `Tracking.AddInfo` under SE. `TrackTimer.cs:15-54` first ticks after 0.25 seconds, then every 2.5 seconds. Its loss conditions include disconnection, deletion, map change, range, and hidden higher-access targets. It does not enforce Ping's proposed player visibility, floor, or lifetime rules. `TrackArrow.cs:19-45` provides right-click cancellation and tracking-info cleanup.
- [ClusterFSkillGain.cs](../../ShatteredLegacy/server/customizations/ClusterFSkillGain.cs), `:381-383`, extends the specific passive Tracking gain window through hook G. The customization search found no separate Ping implementation. Other Tracking references include starter skills, work orders, loot/equipment bonuses, treasure digging, and tutorial trials; a reference is not another Tracking handler.

### Skills and guild context

[P191](cc-P191-cont-earned-skill-gain.md) changed gain defaults to two attempts and stock-sized amounts. Its training times are modeled, and existing configuration can override defaults. Ping needs no rate increase or new cap-training shortcut.

[P283](cc-P283-skill-gain-paths-research.md), row 35 and its gain-window guidance, says normal Tracking already has a source-supported path to 200. [P535](cc-P535-skills-design-vs-build.md), the shared-rules and Tracking rows, distinguishes that gain machinery from unbuilt mastery rewards. Current caps are a flat configurable 200 by default (`C/ClusterFSkillCaps.cs:11,151-196`). The loop helper's proposed ladder is 50, 100, then +5 to 200; it is not today's cap-setting implementation.

[Skills design](skills-design.md), the Tracking proposal and October 2 decision, already approves con/health information past 100, stealth footsteps from 150, and double variant-tracking range at 200. P535 found those displays absent from the inspected Tracking route. Ping adds a separate many-target action. It neither claims those rewards are built nor silently cancels them. In particular, approved future footsteps should be a separate approximate trail feature, not permission for Ping to stream a hidden player's current coordinates.

The [guild skill table](../../ShatteredLegacy/server/customizations/ClusterFGuildStarterPath.cs), `:51`, assigns Tracking to the Rangers' League. `C/ClusterFGuildSystem.cs:195-203` registers the League with `OutridersGuildmaster`. Use that existing teacher and guild menu, without requiring a new guild or client art.

### What TazUO can show

The authoritative client base is `client/TAZUO_COMMIT`, `3212623f63436be1c0f4e3b308b202b29597c026`. Client source citations here were read with `git show` at that commit from `D:/UO/tazuo-sl-build/src`, because its working files are patched and the default source clone has a later HEAD. Paths are relative to `src/ClassicUO.Client/`.

- `Game/UI/Gumps/MiniMapGump.cs:122-189` already draws small colored dots from `World.Mobiles.Values`, using player-relative X/Y rotated onto the radar and notoriety hues. This only supplies mobiles already known to the client. It is not a server-directed remote sensing layer and has no Ping expiry or Ping target policy.
- `Game/UI/Gumps/WorldMapGump.cs:1147-1170,2603-2630,3054-3158` supports map markers with facet, coordinates, color, name, optional icon, and zoom behavior. Its normal mobile display also consumes `World.Mobiles`. Markers can render as solid-color squares with no icon. Existing marker files are not a suitable store for second-by-second creature locations.
- `Game/Data/NotorietyFlag.cs:9-79` defines innocent, ally, gray, criminal, enemy, murderer, and invulnerable states, with profile-controlled hues and text/color helpers. Ping must preserve these meanings for players rather than marking every player as hostile.
- [ClientCommand patch 0001](../../ShatteredLegacy/client/patches/0001-enhanced-packet-client-command.patch) and `C/TazUO/TazUOClientCommand.cs:68-90,117-130` establish an opt-in enhanced-packet handshake. Id 4 acknowledges ClientCommand only. Its whitelist can open the world map or run existing tile/radius commands, but does not transport a live collection of contacts or promise a mini map opener.
- [World-map fog patch 0004](../../ShatteredLegacy/client/patches/0004-world-map-fog-of-war.patch) adds the shard's 0xF4 exploration overlay and reset hooks. [Tree patch 0006](../../ShatteredLegacy/client/patches/0006-exhausted-trees.patch) extends that path for tree state. Neither implements Ping dots. Fog is currently a world-map feature in these patches, not a verified radar Ping capability.

Therefore no new bitmap art is needed. Solid-color dots, outlines, simple shapes, existing fonts, and standard server gump controls suffice. A client code patch and server protocol are needed for contacts outside the ordinary mobile stream. Sending fake mobiles, changing view range, writing marker CSV files, or repeatedly using `marktile` would not provide the required filtered, expiring radar layer.

## Proposed rules and numbers

### Use, cost, and progression

Add **Ping** beside the normal Tracking categories and expose the same server action as `[TrackingPing` for a macro. Both entry points share all checks. Using normal Tracking continues to offer its existing categories and single-target behavior.

Require an alive player with at least 90.0 Base Tracking. Begin a one second focus period; movement, damage, death, disconnection, or a map change cancels it. On successful focus, reveal a hidden caster, deduct 15 stamina, and start a 30 second cooldown measured from that pulse. Mana cost is zero. Insufficient stamina or an invalid/canceled focus costs nothing; an empty completed scan pays the full cost and cooldown. Allow one pending focus and one active pulse per character. Respect the normal skill-use delay and impose at least its existing 10 second delay when the pulse fires. Canceling cannot bypass an already active skill delay.

Use trained Base, not equipment Value, for unlocks, radius, duration, and player eligibility. Capture the tier at pulse start, recheck eligibility during refreshes, and cancel on a skill drop below the captured tier so unequipping or resetting cannot preserve a better pulse. Gear cannot buy the 90 or 120 unlock. This deliberate Ping rule does not change ordinary Tracking's Value reads.

Let `s = min(Base Tracking, 200)`. Radius is a square in map tiles, using the engine's ordinary X/Y range convention. At 90..100 it is `18 + floor(0.6 * (s - 90))`. Above 100 it is `24 + floor((s - 100) / 5)`. Lifetime is `6 + floor(max(0, s - 100) / 25)` seconds.

| Base Tracking | Creature radius | Lifetime | Nonparty players |
| --- | --- | --- | --- |
| Below 90 | Unavailable | None | None |
| 90 | 18 tiles | 6 seconds | None |
| 100, GM | 24 tiles | 6 seconds | None |
| 120 | 28 tiles | 6 seconds | Visible, within 12 tiles and line of sight |
| 150 | 34 tiles | 8 seconds | Same 12 tile restriction |
| 200 and above | 44 tiles | 10 seconds | Same 12 tile restriction |

Cooldown and cost do not improve above GM. Even at 200 there is a 20 second gap between pulses. No loop or player level independently grants Ping strength. If real level-derived caps later arrive, the trained skill still controls access. Do not add another variant radius multiplier to Ping at 200; the older variant reward belongs to ordinary quarry tracking and needs its own specification.

Ping itself grants no skill gain or XP, including per-contact or per-refresh gains. Normal Tracking remains the training path documented in P283. Selecting a quarry must not fabricate additional passive gain rolls.

### Contacts, walls, and floors

The server computes eligibility before counting or sending anything. All output modes use exactly that same result set.

Include living, nonhidden creatures: monsters, animals, human NPCs, controlled pets, and summons. Exclude the caster, dead mobiles and ghosts, hidden or invisible mobiles, staff characters, deleted/internal-map objects, and contacts outside the allowed facet, floor, or range. Count a mounted pet only once as part of its rider rather than as a second contact. Ordinary vendors can appear as neutral NPCs, but invulnerable NPCs are not selectable quarry.

PvE sensing can cross ordinary dungeon walls and closed dungeon doors. It gives presence and position, not a navigable route or authority to attack. It must not scan other floors, private houses, private camp/encounter instances, or restricted staff areas. House interiors outside the caster's own interior scope are excluded. A pet belonging to a nonparty player follows the player rule below, including 120 skill, 12 tiles, line of sight, and exclusion when its owner is hidden. This closes the obvious pet-dot proxy for locating a hidden owner. Unresolvable ownership fails closed.

Use explicit server-authored **floor volumes** for dungeon wall sensing. A volume identifies facet, instance, X/Y bounds, Z bounds, and a floor key; several volumes may share a key for one connected floor. Both caster and contact must resolve unambiguously to the same key. Overlaps, stairs, and bridges need authored boundaries. A region name or `abs(Z difference) < 16` alone is not proof of the same floor. Separate levels can share Z or a region.

Where no unambiguous dungeon floor mapping exists, report **"Ping unavailable here: dungeon floor not mapped."** Spend no stamina and start no Ping cooldown. Do not quietly scan all floors. The builder must ship mapped test areas and list enabled dungeons before calling wall sensing complete; exhaustive world coverage is separate content work. Outdoors, use the same facet and instance plus `abs(Z difference) <= 16`, with private-interior exclusions; this is a height tolerance, not a pathfinding guarantee. Mark vertically overlapping structures as floor-volume areas too, or disable Ping there until mapped. Entering another floor or instance cancels the pulse.

Fix the scan origin at the caster's tile when the pulse fires. Refresh eligibility and coordinates once per second at elapsed 0, 1, 2, and so on, strictly before expiry. The caster may move within that fixed radius; leaving it cancels the pulse. Contacts can enter or leave the origin's radius during the pulse. Each refresh adds eligible arrivals and removes departures, deaths, concealment, ownership changes, and other newly disallowed contacts. This is a brief active sweep, not an indefinitely moving radar aura.

Player and player-owned-contact eligibility also uses the caster's current position, 12 tile range, and current line of sight on every refresh. A fixed scan origin must not leave a player visible after the caster moves out of sight.

### Categories, threat, and the display

Relation and combat difficulty are different. Each result belongs to one mutually exclusive summary group, in this order: player, friendly creature, hostile creature, neutral animal, neutral NPC/other creature. Species subtotals are optional drill-down data and never add the same mobile twice.

Friendly means the caster's pets/summons or those of a party member, plus explicitly allied NPCs. Hostile means an active aggressor against the caster/party or an uncontrolled creature whose existing enemy logic treats them as enemies. Controlled creatures use their owner's relationship before wild-creature logic. Everything else is neutral. Body.IsMonster alone does not prove hostility; notoriety or attack permission alone does not either. The implementation prompt must exercise passive monsters, aggressive animals, guards, vendors, and pets against that policy without invoking AI actions that change combat state. Uncertain relations default to neutral.

| Contact | Dot | Detail |
| --- | --- | --- |
| Hostile creature | Red filled circle | Kind and relative threat |
| Neutral animal or NPC | Yellow hollow circle | Animal/NPC label |
| Friendly creature | Green square | Friendly or own pet |
| Player | Blue diamond | Border in actual notoriety hue; text names the flag |

Keep the caster's normal white radar dot. Use shapes and text as well as color. Reuse `ClusterFCreatureLevels.Con(viewer, target)` and `Word` (`C/ClusterFCreatureLevels.cs:206-247`) for relative creature difficulty in the gump: easy or below, fair/even, tough, dangerous/deadly. Preserve the existing provisional player-strength provider until real levels exist (`:46-78`); do not describe the current estimate as player XP level. Red relation dots stay red even for an easy hostile. Tough contacts get an extra simple outline and dangerous/deadly contacts a double outline, with full words in the result list. No exact HP, resist, loot, or player combat-strength data is granted by Ping.

Example chat at pulse start: **"Ping: 7 hostiles, 3 neutral animals, 2 friendlies, 1 player. Hostiles: 4 fair/even, 2 tough, 1 dangerous/deadly. 6 seconds."** If neutral NPCs exist, add that group. This is an example, not a measured population.

The patched radar shows every eligible creature as a dot, even beyond normal visual range, clipped to the map's drawable area. Show a small remaining-seconds label and a radius ring. The maximum scan area must fit the large radar: reuse the existing large-map frame and add a Ping-specific projection scale if required, without changing the normal radar's terrain-to-dot alignment. The implementation must demonstrate the four corners at radius 44. If the radar is closed, open its existing frame when the player explicitly invokes Ping. Do not force the full world map open.

The full world map can draw the same transient contacts using its own facet, zoom, pan, and rotation transform. This companion overlay does not replace the radar. Draw after fog so a sensed contact can appear over unexplored terrain; do not clear exploration bits or reveal terrain. Closing a map does not extend the pulse. Contacts already represented by ordinary mobile dots must not draw twice; normal mobile rendering resumes when the Ping layer expires.

Provide a standard **Ping results** gump with current counts, grouped expandable kind/threat rows, and paged individual quarry rows. Use existing controls and fonts. Refresh the count header while open without stealing input focus or changing a selected row to a different quarry. Unknown remote contacts get broad type labels such as "orc" or "animal," not hidden names or special loot hints. Visible players use the identity already visible through normal play. Dot click and gump selection are convenience routes to the same server validation.

On clients without the specific Ping capability, send only the initial chat count and a final **"Ping ended"** message. A normal Tracking gump button opens the same paged results for selecting quarry. There is no attempt to draw dots on an unsupported client. Server gumps need no client patch. Chat-only users get one summary, not one line per contact per second. An empty scan says **"Ping: no eligible contacts on this floor."** A count is not a promise that hidden creatures do not exist.

## Track a quarry and protect PvP

At 120 Base Tracking, visible living players may appear, including innocent, gray, criminal, enemy, murderer, and friendly players. All have a blue player center with their real notoriety border and flag text; the display never implies that an innocent is legal to attack. Keep the 12 tile and line-of-sight restriction in PvP and protected facets alike. Party members are also player contacts and use these rules; existing party map sharing is separate.

A player first included in a pulse receives **"You feel watched. Someone nearby is reading the trail."** Notify before sending their first contact, once per pulse, with a 10 second per-recipient notification limit across trackers. Do not reveal the tracker's identity or direction. Warning suppression never allows a hidden player into results. Multiple scouts can cover for each other's cooldowns; personal cooldowns cannot eliminate coordinated scouting, but visibility, range, stamina, caster reveal, and warnings still apply to each scout.

Hiding, Stealth while hidden, and magical invisibility always beat Ping at every skill, even 200. A player who becomes hidden is removed at the next server refresh, and stale client contacts expire within the packet's short validity window. Never include their existence in a hidden-player subtotal. Ping never sets a target's Hidden state false. Detect Hidden remains the reveal skill. The older 150 footsteps reward can later supply coarse historical traces under separate rules; it must not turn these exclusions into precise remote coordinates.

Choose a result while the pulse is active to start one ordinary Tracking arrow, replacing the previous quarry. Resolve a server-held contact token, then recheck death, concealment, floor, map, range, skill, ownership, and player visibility. Reject stale, forged, or expired tokens with **"That trail is gone."** A marker is not a target cursor, combat target, spell lock, or line-of-sight bypass.

Reuse `TrackArrow` and the normal `Tracking.AddInfo` bookkeeping. Creature arrow range is twice the captured Ping radius, using the normal 2.5 second arrow update. A creature arrow can outlive the dots, but an additional server guard must stop it on hiding, death, prohibited ownership/interior changes, floor changes, or loss of normal arrow conditions. Player and nonparty player-owned quarry arrows additionally retain the 12 tile/line-of-sight restrictions and end when this pulse expires. Recheck the guard at least every 0.25 seconds so the stock timer cannot continue streaming a hidden player's location. Right-click cancels normally. Ordinary Tracking's existing behavior is not rewritten by this feature.

The Rangers' League teaches the ability through an **Explain Ping** entry on `OutridersGuildmaster` and a brief practice instruction at the hall. Automatically unlock the skill action at 90 Base for any character; neither membership nor currency is required. This is the recommended nonexclusive teaching role, not a new saved unlock or invented rank requirement. A future League quest may teach the existing action without granting a stronger PvP sensor.

## Implementation boundary and delivery options

Keep server logic additive under `server/customizations/`, with targeted registered patches only where necessary. Do not copy the whole upstream Tracking handler to add one button. Before that patch, argue alternatives in implementation notes: a player command alone avoids it but is less discoverable; a new standalone skill handler would replace the stock menu; a small extra gump button plus the additive action preserves the existing categories. Client changes belong in a new ordered `client/patches/` patch against the pinned base plus the existing patches, not a vendored TazUO fork.

Use a new independently acknowledged enhanced-packet capability for Ping. Id 4 support does not prove Ping support. Reserve its exact id/version after checking the server and client's registries in the implementation prompt. Unsupported or opt-out clients receive no Ping extension payload. Extend the shared handshake dispatcher rather than registering a second competing 0xCE handler.

Proposed version 1 messages: Begin, complete Snapshot, Clear, and optional Select. Carry pulse id, sequence, facet, origin, radius, remaining lifetime, and contacts containing pulse-local token, X/Y, relation, threat band, and player notoriety where allowed. Do not send real serials, hidden contacts, HP, or a global candidate list. Tokens are authorized only for that character, connection, and pulse. Count and snapshot filters must be identical. The client never decides who is discoverable.

Refresh full filtered snapshots once a second. A contact's client lease ends after 1.5 seconds without a valid refresh and never later than the pulse deadline. Clear immediately on cancellation and reset at logout, new login, disconnect, map/instance transition, or a new pulse. Ignore old sequences and malformed coordinates. Reject requests to select an unknown token; rate-limit requests separately from the 30 second action cooldown. Do not persist contacts or add them to map marker files.

Page large snapshots into bounded transport chunks, for example 128 contacts each, with a declared chunk count and atomic replacement only after a complete valid sequence arrives. Never silently apply normal Tracking's 12-result cap to Ping. A provisional overload ceiling of 1,024 eligible contacts per pulse is an operational safeguard, not a target limit advertised to players: above it, cancel with **"Too many trails to read here"** and refund stamina/cooldown. Never send a misleading partial count. Share the ceiling and filtering across text and patched modes. Profile dense-spawn cases before choosing a production ceiling. Normal-size scans must show every eligible contact.

Effort estimates are Golem implementation prompts, not measured days. They include failing-first regression coverage and the appropriate gated server/client builds, but exclude deployment and Chase's live playtest. Options are cumulative alternatives; do not add their totals together.

| Option | Delivered behavior | Estimated prompts | What remains |
| --- | --- | --- | --- |
| A. Text and quarry selection | All eligibility/cost/PvP rules, initial chat count, paged server results, guarded normal arrow, initial floor-volume support | 2 | No map dots. This is a foundation, not completion of Chase's radar request. |
| B. Snapshot radar | A plus every found creature drawn on the radar at its initial position for the tier's lifetime, with expiry and capability fallback | 3 to 4 total | Dots are a momentary snapshot, not moving contacts. Must label them "snapshot" and would need Chase to accept the reduced scope. |
| C. Refreshed radar and world map, recommended | All rules above, every eligible creature refreshed once a second, radar and companion world-map overlay, selection, stale-data removal, fallback | 5 to 6 total | Broader dungeon floor authoring and real-client tuning continue as content/verification work. |

For C, split the work into reviewable prompts: (1) additive scan policy, costs, text, and gump; (2) floor volumes, exclusions, quarry guards, and enabled-area fixtures; (3) capability and bounded snapshot protocol; (4) radar draw/scale/lifetime/selection; (5) world-map companion, fallback, fog and package integration. A sixth prompt is contingency for client acceptance fixes or floor coverage in the chosen launch dungeons. Each intermediate state must be explicitly labeled as such. Deploying an incomplete PvP filter is not an acceptable intermediate state.

Builder acceptance should cover unlock boundaries, all table endpoints, empty scans, cancel/refund behavior, cooldown sharing between entry points, exact count/dot membership, and actual multi-creature refreshes. Watch new tests fail before implementing each behavior. Include hidden players and hidden owners with pets, staff, innocents, concealment during an arrow, forged selections, player LOS loss, walls versus floors with identical Z, private houses, and missing floor data. Client cases include no acknowledgement, opt-out, stale sequences, lost chunks, disconnect, login, facet switch, expiry, duplicate normal dots, fog, zoom/rotation, and maximum-radius radar corners. Use `docker/uo/build.sh` for the gated server build and `client/Build-Client.ps1` for the client patch/build route, with PowerShell scripts/tests run by Windows PowerShell 5.1. A real patched-client check must show several moving contacts at once; passing parser tests alone is not visual acceptance.

## Questions for Chase

These are review questions with recommended answers. No answer is needed to finish this design task.

1. **Build the full moving radar or accept a smaller release?** Recommend C, with A as its first internal milestone. A list alone misses the requested experience.
2. **Where should access start and how strong should it become?** Recommend 90 Base, 18 tiles, 6 seconds, reaching 44 tiles and 10 seconds at 200; 15 stamina and a fixed 30 second cooldown. Tune after playtesting without lifting normal Tracking's range clamp.
3. **Should Ping find players?** Recommend yes from 120, but only visible players within 12 tiles and line of sight, with a warning. This makes PvE scouting the large-area reward. If Chase prefers no player sensing at all, remove the player branch and retain all other rules.
4. **Should 150 or 200 Tracking defeat Hiding?** Recommend no precise hidden contacts at any tier. Preserve the approved 150 historical-footstep idea for its own design and keep Detect Hidden relevant.
5. **Should walls block it, and which dungeons launch first?** Recommend through-wall PvE sensing on authored same-floor volumes. Pick one launch dungeon and one outdoor/vertical-structure fixture in the builder prompt, then expand coverage. Unmapped dungeon areas explicitly reject Ping rather than leaking other floors.
6. **Does the Rangers' League own the unlock?** Recommend the League teaches it, while any character at 90 Base can use it. Avoid a new membership, rank, currency, or loop-state gate for the first version.
7. **Does Ping grant extra information or party sharing?** Recommend relative creature threat only, personal results, and no exact health/loot data. Leave ordinary arrow health/con, rare-variant range, and later footsteps as separate approved rewards to implement deliberately.

## Verification and limits

Read both work-copy AGENTS files, the governing document index, direction record, and task guidance. Inspected canonical Tracking references and the registered radius patch, the matching pinned Tracking/arrow sources, skill/guild/creature-level helpers, P191/P283/P535 and related skills decisions, pinned TazUO radar/marker behavior, client patches, and TazUO implementation/package notes. `client/README.md` has an older "Not yet" package paragraph; P124/P511 describe later packaging work. This design does not infer the installed client's capabilities from that paragraph or an executable folder. It requires the specific runtime acknowledgement.

Unverified: deployed config and client version, visual fit of the full radius on the radar, performance under real dense spawns, exact runtime enemy classifications for every creature, and floor-volume coverage. Floor-volume resolution and transient Ping contacts are proposed work, not existing APIs verified here. No client was launched, no runtime behavior was claimed, and no art request is needed.

No code, configuration, existing design decisions, or files under `docs/` were changed. No tests were added or run; lane tests are none. No build, container operation, Haven connection, deployment, account/save operation, commit, merge, push, or branch switch was performed. Final editorial and scope checks are recorded below before the completion marker is added.

Final review passed: plain ASCII punctuation with no em dashes, no trailing whitespace, consistent Markdown tables, all local Markdown links resolving, cited source files present, and this note below 5 MB. `git diff --check` passed in both work copies; direct whitespace checks also covered this new untracked note. Windows PowerShell reports version 5.1.26100.9711. The required progress reporter completed with work-copy path overrides and `--dry-run`; its known incidental `tools/progress.json` write was suppressed in the invocation, leaving generated files unchanged. No reporter inventory counts are used as feature evidence. Final scope checks found the code work copy clean and only this new note in the migration work copy. The stop-request file was absent at the final stopping-point check.

P563 DONE
