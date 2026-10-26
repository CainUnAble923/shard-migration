# P625: Tracking Ping, stage 1 (scan rules, cost, chat count, results list)

Written 2026-10-25 by the Iron Golem (Claude Code). Builds stage 1 of [cc-P563-tracking-ping-design.md](cc-P563-tracking-ping-design.md), Chase's option C (10-25 evening: live moving dots on the mini map for every found creature, same floor only, limits on showing players, no exact spot for hidden ones, chat count as the fallback). The design splits C into five prompts; this is its "(1) additive scan policy, costs, text, and gump". The later stages are drafted as prompts at the end of this note.

## In plain words

- Players with 90 Tracking (trained skill; gear does not count) get a new Ping. Use Tracking and a small Ping menu now appears under the usual Animals / Monsters / Human NPCs / Players menu, or type `[TrackingPing`. After a one second pause the player gets a chat line such as "Ping: 2 hostiles, 1 neutral animal, 1 friendly. Hostiles: 1 fair/even, 1 tough. 6 seconds.", and `[TrackingPing results` (or the menu's Results button) lists each one. It costs 15 stamina, reveals the player, and works once every 30 seconds.
- From 120 Tracking a ping also finds players the scout can see within 12 tiles, and they get "You feel watched." Hidden players are never found at any skill, and nor are the pets of hidden owners. Ping does not work inside dungeons yet: it says "Ping unavailable here: dungeon floor not mapped."
- There are no mini map dots yet. This stage is the server half (who is found and what it costs), so every client gets the chat count already. The dots need the client stages drafted below.
- For Chase: the image `sl-modernuo:cc-P625` is built and all 2,502 shard tests pass. It is test shard material: nothing is deployed and nothing needs deciding now. Try it on the test shard with a 90+ tracker near some animals and monsters outdoors. The overseer numbers the four drafted stages at the end.

## What changed (ShatteredLegacy, branch golem/Iron/P625)

| File | Change |
|---|---|
| `server/customizations/ClusterFTrackingPing.cs` (new) | The whole stage 1 server side, described below. |
| `server/patches/Tracking-ping-offer.patch` (new) | One call added to pinned `Skills/Tracking/Tracking.cs` `OnUse`, after the stock `TrackWhatGump` is sent: `ClusterFTrackingPing.OfferFromTracking(pm)`. |
| `docker/uo/apply-patches.sh` | Registers the patch right after `Tracking-radius-osi.patch` (same file, separate hunk), with the reasons for a patch. |
| `server/tests/Skills/TrackingPingVerification.cs` (new) | 9 facts (16 cases), below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.25.11, three Added lines. |

### The rules as built

Numbers are the design's (`cc-P563`, "Proposed rules and numbers"), unchanged:

- **Unlock:** 90.0 Base Tracking. Base, never Value, so a +20 skill item on 89.9 does not unlock it. The radius and lifetime come from the Base captured when the ping fires.
- **Radius** (square, in tiles): 18 at 90, `18 + floor(0.6 x (s - 90))` to 24 at 100, then `24 + floor((s - 100) / 5)`: 28 at 120, 34 at 150, 44 at 200 and above. **Lifetime:** 6 s, plus 1 per 25 points past 100: 8 at 150, 10 at 200. These are computed in whole tenths of a point, so 0.6 x 10 cannot come out as 5.999.
- **Focus:** one second. It sits in the caster's spell slot (`Mobile.Spell`, as an `ISpell`), so pinned `Mobile.Damage` (`OnCasterHurt`), a step (`OnCasterMoving`), death and a disconnect break it the way they break a spell being cast. A location or facet change at the end also breaks it. A broken focus costs nothing. Casting refuses a ping ("You cannot ping while casting.").
- **Cost when it fires:** reveal (`RevealingAction`), 15 stamina, 30 s cooldown from the pulse, and the skill delay raised to at least 10 s from the pulse. No mana. An empty scan pays in full. Too little stamina, an unmapped dungeon, a running cooldown, an active focus or pulse, or (command only) a running skill delay refuses with nothing paid. The button on the Tracking skill's own menu skips the skill-delay check, because that very skill use set its own 10 s delay; otherwise every press would be refused.
- **No skill gain** and no XP. Ping never calls `CheckSkill`.
- **Who is found** (one list feeds the chat count, the results gump and, later, the dots): alive, not hidden, not staff, not a dead bonded pet, on the caster's facet and not the internal map (so a ridden mount is never a second contact), inside the square radius around the spot the ping fired from, within 16 Z of that spot, not in any dungeon region, and not in a house unless it is the caster's own house too.
- **Players** only from 120 Base, and only within 12 tiles of where the caster stands *now*, in line of sight, re-read every second. Each is warned "You feel watched. Someone nearby is reading the trail." before their first contact, once per pulse, and at most once per 10 s across all trackers. The tracker's name and direction are not given.
- **Another player's pet or summon** (owner not the caster and not in the caster's party) follows the player rule: 120, 12 tiles, sight. It is never found while its owner is hidden or staff. A controlled or summoned creature whose master is gone is never found (fails closed).
- **Groups:** player; friendly (the caster's or a party member's pets and summons); hostile (an active aggressor on the caster or a party member, or an uncontrolled creature that would attack: `FightMode` not None or Aggressor, then pinned `BaseCreature.IsEnemy`; an Evil creature only against negative karma); neutral animal (`Body.IsAnimal`); neutral NPC or other. Invulnerable creatures (vendors) are never hostile. Uncertain cases are neutral.
- **Threat** (hostiles and neutrals): `ClusterFCreatureLevels.Con`, folded into "easy or below" (grey, green), "fair/even" (blue, yellow), "tough" (orange), "dangerous/deadly" (red, skull). No hit points, resists or loot.
- **Labels:** a creature's kind from its type ("Orc" is "orc", "GiantSpider" is "giant spider"), never its own name. The first test run showed an orc listed as "Zupgugh", so a remote sense would have read names. A player's pet is "your pet" or "a pet". A visible player shows their name and notoriety word.
- **The pulse** re-reads every second, strictly before its end. Arrivals are added and the dead, the newly hidden and the out of range are dropped. It ends with "Ping ended." at its lifetime. It stops early ("Your ping fades.") if the caster dies, leaves the facet, moves more than 16 Z from the origin, walks outside the radius, enters a dungeon, or drops below the Base it fired with. Logout and disconnect end it silently.
- **Overload:** above 1,024 eligible contacts (`OverloadCeiling`), "Too many trails to read here." and nothing is paid. Under it every contact is kept. Normal Tracking's 12-result cap does not apply.
- **Chat:** "Ping: 7 hostiles, 3 neutral animals, 2 friendlies, 1 player. Hostiles: 4 fair/even, 2 tough, 1 dangerous/deadly. 6 seconds." Groups with none are left out; neutral NPCs appear when there are any. An empty scan says "Ping: no eligible contacts on this floor."
- **Gumps:** the Ping menu (Ping, Ping results, and a one-line cost reminder) appears below the stock Tracking menu from 90 Base. The results gump shows the count line, ten rows a page ("orc - hostile, tough"; "Near - player, innocent"), Refresh, and previous and next. It is plain standard controls, so no art is needed. With no active ping it says how to start one.

### Why a patch for the menu, and why this one

The design asked for the alternatives to be argued:

- A **command alone** (`[TrackingPing`) needs no patch but nobody would find it. It exists anyway, for macros.
- **Replacing the skill callback** from customizations would also avoid a patch. But pinned `Tracking.Initialize` sets the same callback, and the order between two `Initialize` methods is not something to rely on.
- A **fifth button inside `TrackWhatGump`** is a `StaticGump`, whose layout is built once per type. It cannot depend on the user's skill, and it would copy the stock gump.
- **One call after the stock menu**, a separate small gump: one hunk, stock categories untouched. Chosen.

## Tests: red first, then green

How I ran them: the builder image `sl-uo-builder:cc-P436` (built from this branch's base, `9cc69ca`), with `ClusterFTrackingPing.cs`, the test file and (where named) the patched `Tracking.cs` bind-mounted, `dotnet test` filtered to `TrackingPingVerification`. The script (`probe.sh`), the stub, the mutants and every log are in the session scratchpad.

| Fact | What it pins |
|---|---|
| `RadiusAndLifetimeMatchTheTable` (8 cases) | 89.9 gives 0/0; 90 18/6; 95 21/6; 100 24/6; 120 28/6; 150 34/8; 200 44/10; 250 44/10. |
| `GearCannotBuyTheUnlock` | 89.9 Base with a +20 skill mod (Value 109.9) is refused; 90 Base starts. |
| `OnePingFindsTheEligibleCountsThemAndPaysOnce` | Two orcs (one 20 tiles off), a wild horse and the caster's pet are found, exactly. A hidden orc, an orc 25 tiles off (radius 24), one 20 Z up, one on Felucca, a GM, a plain player (below 120) and a dead orc are not. The groups, "orc" not the orc's own name, "your pet", the chat line's start and "6 seconds." The focus pays nothing; then 85 stamina, revealed, 29-30 s cooldown, skill delay of at least 10 s, Tracking Base unchanged, the hidden orc still hidden, the bystander not warned, and the spell slot given back. |
| `AFocusThatBreaksOrIsRefusedCostsNothing` | Moving breaks it; damage breaks it at once, even though the host heals the hit straight back; one at a time; too tired; the command respects a running skill delay while the Tracking menu's button does not; a registered dungeon region refuses with the unmapped line. No stamina or cooldown spent in any of them. |
| `TheCooldownHoldsThirtySecondsFromThePulse` | "Ping ended." at the end; refused at 8 s with "You must wait ... before you can ping again."; allowed again at 31 s. |
| `PlayersFrom120OnlyNearInSightNeverHiddenAndWarnedOnce` | At 119.9 no player and no other player's pet. At 120: the player 8 tiles off and a visible owner's pet 5 tiles off are found. Not found: the player 15 tiles off, the hidden player, the hidden owner's pet, the visible owner 20 tiles off, and that owner's pet 18 tiles off. Exactly one warning to the near player, none to the hidden or far one, the hidden one still hidden. A second tracker 2 s later does not warn again. When the scout walks to 13 tiles away, the near player drops out at the next refresh. |
| `ThePulseFollowsArrivalsAndDeparturesThenEnds` | An arrival appears at the next second; a contact that hides leaves; one "Ping ended." and an empty list after 6 s. Walking 30 tiles off, climbing 20 Z, and a Base drop to 95 each end it early. |
| `TheTrackingSkillOffersPingFrom90AndItsButtonSharesTheChecks` | Through the real (patched) `Tracking.OnUse` with a test NetState: no Ping menu at 89.9; at 90 the stock menu and the Ping menu. The Ping button works with the skill delay set; Results opens the results gump; after the pulse the cooldown refuses both the command and the button. |
| `OverTheCeilingNothingIsPaidUnderItEveryContactIsKept` | 23 orcs with the ceiling at 22: refused, nothing paid. At 23: all 23 found (not 12), "Ping: 23 hostiles.", and each row reads "orc - hostile, ...". |

**Red on the old code.** A stub `ClusterFTrackingPing` with the same public names and no behaviour, and pinned's `Tracking.cs` without the new patch: 15 of 16 failed. The one that passed is the 89.9 row of the table (0/0 is also what the stub returns). The offer fact failed at "Assert.NotNull() Failure" on the Ping menu; the others at their first Begin or table value.

**Mutations of the finished code**, each run alone, each red in exactly the fact meant to catch it (15 passed, 1 failed every time):

| Mutant | Red fact |
|---|---|
| m0: real code, pinned `Tracking.cs` without the patch | the Tracking menu fact |
| m1: the player rule drops the 12-tile range | the players fact |
| m2: a hidden owner's pet may be found | the players fact |
| m3: the focus is not put in the spell slot | the focus fact |
| m4: the 16 Z floor tolerance is dropped | the find-and-pay fact |
| m5: a Base drop below the captured value no longer ends the pulse | the pulse fact |

**Green:** 16 of 16.

Two things the first green runs found, both fixed before the red run above. First, damage in the focus was missed: pinned clears a mobile's damage entries when it is back at full hits (`Mobile.cs:2043`), and the test host heals instantly. On a live shard a heal within the second could hide a hit the same way. That is why the focus uses the spell slot, which pinned `Mobile.Damage` calls directly. Second, creature names leaked into the labels (the "Zupgugh" orc above). The test host also gives stamina back every wheel tick, which would have hidden every cost. The facts hold stamina regeneration at one point an hour (`Mobile.StamRegenRateHandler`, restored in `Dispose`).

**Gated build:** I took the `docker-build` lock (11.9 GB available at launch), ran `docker\uo\build.sh -t sl-modernuo:cc-P625` detached with its log on disk, and released the lock afterwards. It finished with EXIT=0: "Built sl-modernuo:cc-P625 with patches applied and 2502 shard test(s) passing". Of 2,506 tests, 2,502 passed and 4 were skipped (the real-map-data facts); none failed. All 16 Ping cases passed in it, and `Tracking-ping-offer.patch` applied right after `Tracking-radius-osi.patch`. The images are `sl-modernuo:cc-P625` = `ea40d2c84149` and `sl-uo-builder:cc-P625` = `1ebfc38052bb`. The log is `build-P625.log` in the session scratchpad.

## Deviations and decisions for Chase

- **Deliberate, invented ability** (not an OSI port). The overseer may want a line for `docs/fidelity-principle.md`: Tracking gains a Ping menu and command from 90 Base; ordinary Tracking is unchanged.
- **Dungeons are refused for now.** The design forbids scanning other floors, and a region name or a Z difference is not proof of a floor. There are no authored floor volumes yet (stage 2), so a caster in any `DungeonRegion` gets "Ping unavailable here: dungeon floor not mapped." and anyone in a dungeon region is never found. Outdoors uses the design's same facet plus 16 Z rule.
- **Wall sensing outdoors:** creatures are found through walls (the design's PvE rule). Players and other players' pets need line of sight. The test host has no map data, so `InLOS` is always true there: the LOS branch is in the code but **unverified** by a fact. Stage 2 should prove it on real map data or a test tile layout.
- **Not in stage 1:** picking a quarry for the tracking arrow (and its guards), floor volumes, private camp or encounter instances, explicitly allied NPCs, the Rangers' League "Explain Ping", the live-refreshing gump header (the gump has a Refresh button instead), and everything client side. Each is in the stage drafts below. No arrow means no stream of anyone's location yet. That is deliberate: the design says the arrow needs its 0.25 s hidden-target guard first.
- **Read tool denied:** this unattended run auto-denied the Read tool on `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\ClusterFTrackingPing.cs` (a read of lines 165-325 before an edit). I wrote the file myself in this session, so I made the later edits with a scratchpad script (`apply.py`), which applies exact text replacements and refuses any that do not match exactly once. Nothing was skipped because of this.
- **A finishing line written too early, then removed:** my first write of this note ended with the finishing line while the gated build was still running. I took it out within a minute, and it is back only now that everything is done. If the Golem acted on it in that minute, the work it saw was the same, minus the build result.

## Unverified

- Real client: the Ping menu's position beside the stock Tracking menu, and how the results gump reads. Both are standard controls; nobody has looked at them in a client yet.
- Line of sight for players (see above), and house exclusion. `BaseHouse.FindHouseAt` is called, but no fact builds a house.
- Classification on real creatures beyond orcs, horses and pets: passive monsters, guards, vendors and Evil-mode creatures follow the rules above, but no fact covers each one. Stage 2's draft lists them.
- Performance in a dense spawn at radius 44, re-read once a second. The scan is one `GetMobilesInRange` per second per active pinger.

## Checks before handing over

`git diff --check` is clean in shard-migration. In ShatteredLegacy it flags one line, and it is expected: a unified diff's blank context line is a single space (`Tracking-ping-offer.patch` line 11), and the existing patches (for example `AOS-fish-pies.patch`) have the same. The new and changed files are plain ASCII with no trailing whitespace otherwise. Nothing was committed, nothing was deployed, and Haven was not touched. `notes/cc-P481-tools/` was untracked in this work copy before I started; it is not mine and I left it alone.

## Remaining stages, as prompt drafts for the overseer to number

These follow the design's split of option C (its section "Implementation boundary and delivery options"), carried forward with what stage 1 now provides. `P<nn>` is for the overseer to fill in.

---

### Draft: Tracking Ping stage 2: floor volumes, quarry selection and its guards, the League

```
# CC task P<nn>: Tracking Ping stage 2: dungeon floor volumes, pick a quarry for the arrow, the Rangers' League teaches it

**Model:** Opus

**Touches:** server

**Summary:** Stage 2 of `notes\cc-P563-tracking-ping-design.md` (option C, Chase 10-25), after P625's stage 1 (`notes\cc-P625-build-tracking-ping.md`). Stage 1 refuses every dungeon and has no quarry selection. This stage adds authored floor volumes so Ping works through walls on one mapped dungeon floor, lets a player pick one result for the normal tracking arrow with server guards, and gives the Rangers' League an Explain Ping entry.

## The work

1. Read the design's "Contacts, walls, and floors" and "Track a quarry and protect PvP" sections and P625's notes. Add server-authored floor volumes (facet, X/Y bounds, Z bounds, floor key; several volumes may share a key) as data in `server/customizations/` with a loader and a staff `[PingFloors` diagnostic (Diagnostic category). Caster and contact must both resolve unambiguously to the same key; overlaps fail closed. Ship one launch dungeon floor (propose Covetous level 1 or Despise upper, and say why) and one outdoor vertical-structure fixture, with the list of enabled areas in the notes. Unmapped dungeon areas keep refusing with stage 1's line. Entering another floor key cancels the pulse.
2. Quarry selection: each contact gets a pulse-local token (never a serial) authorised only for that character, connection and pulse. A Track button on each results row resolves the token, then rechecks death, concealment, floor, map, range, captured skill, ownership and player visibility; a stale, forged or expired token says "That trail is gone." Start one ordinary `TrackArrow` with `Tracking.AddInfo` (replacing the previous quarry), at twice the captured radius for creatures. Add a server guard checked at least every 0.25 s that ends the arrow on hiding, death, floor or interior change, and for a player or a nonparty player's pet also on leaving 12 tiles or sight and at the pulse's end. Rate-limit select requests separately from the 30 s cooldown. Ordinary Tracking's arrow is not changed. No skill gain from selecting.
3. Private camp and encounter instances: find how the shard marks them (search customizations for instance regions) and exclude contacts in them unless the caster is in the same one; fail closed where unclear.
4. `OutridersGuildmaster` (Rangers' League, `ClusterFGuildSystem.cs:195-203`) gets an "Explain Ping" entry in its existing menu: what it does, 90 Base, cost, the player rules. No membership, rank or currency gate.
5. Red-then-green tests, extending `server/tests/Skills/TrackingPingVerification.cs`: walls versus floors with identical Z inside the launch volume; missing and overlapping floor data; a forged, stale and expired token; concealment during an arrow (ends within 0.25 s); player LOS loss on real map data or a test tile layout (stage 1 could not prove LOS in the host); a house interior; passive monsters, aggressive animals, a guard, a vendor and an Evil-mode creature against the grouping policy, without invoking AI that changes combat state. Seen failing first; mutation evidence for guards that pass on the old code.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG player lines (Ping works on the launch floor; picking a quarry).
7. Notes `notes\cc-P<nn>-tracking-ping-stage-2.md` with the enabled-area list. Last line `P<nn> DONE`.

Do not change stage 1's numbers or the normal Tracking range clamp.
```

---

### Draft: Tracking Ping stage 3: the client capability and the snapshot protocol

```
# CC task P<nn>: Tracking Ping stage 3: a Ping capability in the enhanced-packet handshake and bounded snapshot messages

**Model:** Opus

**Touches:** server, client-package

**Summary:** Stage 3 of `notes\cc-P563-tracking-ping-design.md`. The server must know which clients can draw Ping contacts and send them a filtered, expiring snapshot once a second. Clients without the capability keep stage 1's chat count and results gump.

## The work

1. Read the design's "Implementation boundary and delivery options", `server/customizations/TazUO/TazUOClientCommand.cs` and `client/patches/0001-enhanced-packet-client-command.patch`. Check both registries and reserve a new capability id and version for Ping (id 4 is ClientCommand only). Extend the shared handshake dispatcher; do not register a second 0xCE handler. Unsupported or opted-out clients get no Ping payload.
2. Server messages, version 1: Begin, Snapshot, Clear, optional Select. They carry pulse id, sequence, facet, origin, radius, remaining lifetime, and contacts: pulse-local token, X/Y, relation, threat band, and notoriety for players. No serials, no hidden contacts, no HP. The source is stage 1's one `Scan` list, so the count and the snapshot are identical by construction. Chunks of at most 128 contacts with a declared count; send once a second from the pulse's refresh. Clear on cancellation, expiry, logout, disconnect, map change and a new pulse.
3. A client patch (new ordered file under `client/patches/`, against `client/TAZUO_COMMIT` plus the existing patches) that acknowledges the capability and parses the messages into an in-memory contact layer: atomic replacement only after a complete valid chunk sequence, ignore old sequences and malformed coordinates, a 1.5 s lease per contact and never past the pulse deadline, reset on login, logout, disconnect and facet change. No drawing yet (stage 4); a debug counter is enough to see it.
4. Tests: server facts for the handshake (no ack means no payload), byte-exact message layout, chunking at 128 and 129 contacts, sequence numbers, Clear on every end path, and identical membership to the chat count. Client-side parser tests in the patch's test route for lost chunks, stale sequences and the lease. Seen failing first.
5. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock; `client/Build-Client.ps1` builds the patched client (Windows PowerShell 5.1) under the package lock if it packages. CHANGELOG Staff line only (nothing visible yet).
6. Notes `notes\cc-P<nn>-tracking-ping-stage-3.md` with the reserved id and the message layout. Last line `P<nn> DONE`.
```

---

### Draft: Tracking Ping stage 4: dots on the mini map

```
# CC task P<nn>: Tracking Ping stage 4: draw every found creature as a live dot on the TazUO mini map

**Model:** Opus

**Touches:** client-package, server

**Summary:** Stage 4 of `notes\cc-P563-tracking-ping-design.md`, the heart of Chase's option C: every contact from stage 3's snapshots drawn on the mini map, moving once a second, gone at the pulse's end.

## The work

1. Read the design's "Categories, threat, and the display" section and `Game/UI/Gumps/MiniMapGump.cs:122-189` at `client/TAZUO_COMMIT`. In a new client patch, draw the contact layer: hostile red filled circle, neutral yellow hollow circle, friendly green square, player blue diamond with its real notoriety hue as the border; one outline for tough, two for dangerous/deadly; the caster's white dot unchanged. Solid shapes only, no new art.
2. A radius ring and a small remaining-seconds label. The largest radius (44) must fit the large radar: add a Ping-only projection scale if needed without moving the normal terrain-to-dot alignment. Prove all four corners at radius 44. Open the existing radar frame when the player explicitly pings; never force the world map open.
3. A contact the client already draws as an ordinary mobile is not drawn twice; ordinary drawing resumes when the layer expires.
4. Clicking a dot sends Select with its token; the server runs stage 2's same validation and starts the arrow ("That trail is gone." otherwise).
5. Tests: client unit tests for projection, rotation and corner clipping, de-duplication and expiry. A real patched-client check on a scratch shard (under the test-shard lock, never Haven) must show several moving contacts at once, as a frame burst, not one still. Seen failing first.
6. `client/Build-Client.ps1` green; server build green if the server changed. CHANGELOG player line (Ping dots on the mini map in the Shattered Legacy client).
7. Notes `notes\cc-P<nn>-tracking-ping-stage-4.md` with the proof frames. Last line `P<nn> DONE`.
```

---

### Draft: Tracking Ping stage 5: the world map, fallback check, fog, packaging

```
# CC task P<nn>: Tracking Ping stage 5: world map companion overlay, unsupported-client fallback, fog, package

**Model:** Opus

**Touches:** client-package, server

**Summary:** Stage 5 of `notes\cc-P563-tracking-ping-design.md`, the last of option C: the same transient contacts on the full world map, a final check that unpatched clients keep the chat count, fog untouched, and the patched client in the player package.

## The work

1. In a new client patch, draw the contact layer on `WorldMapGump` with its own facet, zoom, pan and rotation transform. Draw after the fog overlay (patch 0004) so a contact can show over unexplored ground, but never clear exploration bits or reveal terrain. Closing a map does not extend the pulse. No marker files.
2. Unsupported clients: verify on a stock ClassicUO or unpatched TazUO that they get only the chat count and "Ping ended.", never a Ping payload, and that the results gump works.
3. Packaging: the patched client in the player package through the usual package route (package lock), with the client README's Ping paragraph.
4. A sixth, contingency prompt is reserved by the design for client acceptance fixes or floor coverage in the chosen launch dungeons; list anything for it in the notes.
5. Tests: transform tests at several zooms and rotations, fog order, expiry on facet change. Patched-client frame burst on a scratch shard (test-shard lock). Seen failing first.
6. Builds green (client; server if changed). CHANGELOG player lines.
7. Notes `notes\cc-P<nn>-tracking-ping-stage-5.md`. Last line `P<nn> DONE`.
```

P625 DONE
