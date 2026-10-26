# P637: Review of P625 Tracking Ping

Reviewed October 26, 2026. Notes only. No code changed.

P625 implements the first server stage of P563, with additional defects below. It does not complete Chase's moving mini map request. Its notes correctly identify that boundary and draft the remaining stages.

## New findings

### 1. Medium: player sensing bypasses the engine's visibility policy

**Location:** `server/customizations/ClusterFTrackingPing.cs:500-501`, reached for players at `:469-471` and nonparty player-owned creatures at `:484-492`.

`PlayerVisible` checks trained skill, range, and `InLOS`, but never `caster.CanSee(m)`. Those checks are not equivalent. Pinned `Projects/UOContent/Mobiles/PlayerMobile.cs:3251-3268` hides players from another duel context, and their pets, from an active tournament participant. `Projects/Server/Mobiles/Mobile.cs:3627-3629` and `Projects/Server/Maps/Map.cs:1695-1708` show that mobile LOS checks geometry without asking that visibility policy.

If an otherwise eligible player from another duel context stands within 12 tiles and LOS, Ping includes them, warns them, and exposes their name in results even though normal play hides them. A nonparty pet can expose the same excluded participant's presence. This violates P563's visible-player and normal-identity rules (`notes/cc-P563-tracking-ping-design.md:109` and `:115`) independently of the deferred floor-volume work.

**Fix:** Require `caster.CanSee(m)` in the player visibility helper, while retaining the explicit Hidden and staff exclusions. Keep remote PvE wall sensing separate so this does not impose normal visual restrictions on every wild creature.

**Missing regression:** An active tournament scout and a nearby player in another duel context, plus that player's nonparty pet. Establish that ordinary `CanSee` refuses them while range and LOS pass; assert that Ping excludes both and sends no watched warning. Also retain a visible participant as a positive control. The existing players fact at `server/tests/Skills/TrackingPingVerification.cs:298` covers range, Hidden, ownership, and warnings, but no engine visibility veto. Tournament availability on the deployed shard was not checked; this is a source-supported conditional defect.

### 2. Medium: timer catch-up can scan after the pulse deadline

**Location:** `server/customizations/ClusterFTrackingPing.cs:777-799`; the deadline is assigned at `:742`.

The pulse ends after a number of callbacks, using `_elapsed`, rather than checking `Core.Now >= End`. After an event-loop stall that crosses the deadline, early catch-up callbacks still run `Scan` and `Accept` until the callback count reaches the lifetime. They can perform repeated full scans and emit watched warnings for an already expired pulse. `SecondsLeft` can meanwhile report zero (`:163-164`). P563 requires refreshes strictly before expiry (`notes/cc-P563-tracking-ping-design.md:84`).

This follows the actual timer route: pinned `Projects/Server/Main.cs:711-725` sets the current wall clock before slicing; `Projects/Server/Timer/Timer.TimerWheel.cs:59-69` catches up missed wheel turns; `:146-169` executes and rearms repeating callbacks. The catch-up callbacks see the current clock, not their historical due times. This finding does not claim that Ping keeps running after the entire catch-up slice finishes. The defect is that it scans and can warn during that slice after its deadline.

**Fix:** Check the absolute deadline before any refresh or warning and finish immediately when it has passed. Keep the once-per-second schedule for timely callbacks. Future snapshot and selection paths should use that same deadline.

**Missing regression:** Stall the clock past an active pulse's end before letting its next callback execute. Assert that the first resumed callback ends it without another scan or watched warning. The current lifetime fact at `server/tests/Skills/TrackingPingVerification.cs:356` uses `ShardTestClock.AdvanceSeconds`, whose implementation at `server/tests/Route/ShardTestClock.cs:150-159` advances and slices every 8 ms. It therefore does not exercise a stalled loop. Extend the approved clock helper if needed rather than adding an unrelated direct timer-wheel driver.

### 3. Low: expired cooldown and warning records retain deleted characters

**Location:** `server/customizations/ClusterFTrackingPing.cs:96-97`, writes at `:378` and `:761`, and cleanup at `:840-855`.

Both static dictionaries use strong `Mobile` keys. Cooldown expiry only changes what `CooldownLeft` returns; it never removes the entry. Warning timestamps are likewise retained indefinitely. `Stop`, including its logout and disconnect callers, removes only the focus and pulse. The only dictionary clear is in `ResetAll`, explicitly documented as test-only at `:169`.

Every distinct caster and warned player therefore remains referenced until process exit, including after character deletion. Character churn grows these tables and retains deleted player objects and any objects still reachable from them. This is a resource cleanup defect, not a claim of a measured live memory incident.

**Fix:** Prune expired cooldown and warning records and remove both records when a character is deleted. Do not simply clear an unexpired cooldown on disconnect, which would create a relog bypass. Pinned `Projects/UOContent/Mobiles/PlayerMobile.cs:3285-3292` exposes `PlayerDeletedEvent` for the deletion path.

**Missing regression:** Expire and prune records for distinct characters, then delete a caster and a warned recipient and verify their entries are gone. Include a disconnect/reconnect control proving that an unexpired cooldown and warning throttle still hold. The fixture's unconditional `ResetAll` in `server/tests/Skills/TrackingPingVerification.cs:56-64` masks retention across character lifecycles.

## Scope and prior review

Read both work-copy AGENTS files, the direction record and task list, `notes/cc-P625-build-tracking-ping.md`, its adjacent Codex review, the P563 design and its adjacent review, and the Ping rows in P572/P574. Chase's option C answer is recorded in P625's opening paragraph and the implementation's header. I found no separate later Ping answer in the checked notes; P572/P574 recommendations are not treated as new answers.

The earlier P625 review already owns the refresh-overload refund and stale-menu skill-delay exemption findings. They are not reissued here. P563's adjacent review and P602's guide review report no findings to carry forward.

Code inspected: `server/customizations/ClusterFTrackingPing.cs`, `server/patches/Tracking-ping-offer.patch`, its registration and patch ordering in `docker/uo/apply-patches.sh`, and `server/tests/Skills/TrackingPingVerification.cs`. Also checked `CHANGELOG.md`, `VERSION`, `ClusterFCreatureLevels.cs`, `ClusterFSkillClamps.cs`, and the pinned Tracking, mobile visibility, LOS, and timer implementations. Code HEAD was `a3f017e279e29eed0ac12c506ef51e6310291583`; notes HEAD was `782363353dc7c3e394b61925f34878f7c672f6f5`. The read-only ModernUO checkout was clean at `d4531cd94b739613155225c234900de9f47d2c88`.

The full design still requires floor volumes and outdoor vertical-area handling, private-instance and staff-area exclusions, quarry selection and guards, League teaching, richer and automatically refreshed results, and the client protocol and map overlays. P625 explicitly defers the main implementation areas and does not claim them delivered. Keep those acceptance requirements with the remaining stages. Its already disclosed lack of real LOS, house, classification, performance, and client acceptance evidence remains open; it is not presented here as newly discovered runtime failure.

## Save/load and verification limits

Focuses, pulses, contacts, cooldowns, and warning timestamps are process-local dictionaries and timers. A restart drops them. The design forbids persisting transient contacts and introduces no saved unlock, so I found no new serialized-type or save-chain defect in this stage. Restart durability of the short cooldown is not specified; I have not invented that requirement. Logout and disconnect do have explicit stop handlers, but their runtime behavior and a save/reload cycle were not independently exercised.

This was a source review. No tests were added or run, consistent with this prompt's lane tests of none. No build, live shard, client, tournament, dense-spawn, or memory probe was run. P625's reported gated build was read, not independently reproduced. The proposed regressions above still need failing-first execution in their repair tasks.

No files under `docs/` or the code work copy were changed. No Haven connection, deployment, account/save operation, commit, merge, push, or branch switch was performed.

Final checks: both work copies passed `git diff --check`. The new note passed a separate ASCII, no-em-dash, trailing-whitespace, and size check. The only work-copy change is this note. Windows PowerShell was 5.1.26100.9711. The required progress reporter completed with work-copy path overrides and `--dry-run`; its incidental `tools/progress.json` write was suppressed in memory, leaving generated files unchanged. Its inventory figures are not used as review evidence. The stop-request file was absent at the final stopping-point check.

P637 DONE
