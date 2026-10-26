# P648: Tracking Ping player guide draft

Written October 26, 2026. Documentation only. Added [notes/wiki-drafts/tracking-ping.md](wiki-drafts/tracking-ping.md) from the merged implementation rather than treating the P563 design as delivered behavior. No existing guide, code, configuration, or file under `docs/` was changed.

## Source snapshot and scope

Both work copies were clean at entry. Code HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`. Notes HEAD: `49015d5742ba6cde464e7e278b5980dfd9065d87`. Read-only ModernUO HEAD: `d4531cd94b739613155225c234900de9f47d2c88`.

The draft covers access, commands and menu buttons, focus, stamina and reveal, cooldown, range and duration, fixed origin, manual results refresh, contact groups and difficulty, player/pet restrictions and warnings, and current failures and unfinished features. It does not claim the feature is deployed or client-tested. The older Rangers guide still describes the P563 proposal; refreshing that separate page was outside this prompt's requested files.

## Sources read

Paths starting with `server/` or `docker/` below are in the ShatteredLegacy work copy. Paths starting with `notes/`, `docs/`, or `tools/` are in this shard-migration work copy. `U/` means read-only `D:/UO/ModernUO-pinned/Projects/`.

- Both root `AGENTS.md` files; `docs/README.md`, `docs/direction-decision.md`, and `docs/tasks.md` for working agreements and settled scope.
- `notes/cc-P563-tracking-ping-design.md`, including use/cost/progression, contacts/walls/floors, categories/display, PvP/quarry rules, and implementation boundaries; its adjacent Codex review.
- `notes/cc-P625-build-tracking-ping.md`, the stage 1 explanation, tests and reported build, deviations, unverified items, and remaining-stage drafts. Its adjacent Codex review identifies overload refunds and the stale-menu skill-delay exemption.
- `notes/cc-P637-review-build-tracking-ping.md` and its adjacent Codex review: missing engine visibility veto, refresh after deadline, retained character references, deferred work, and verification limits.
- `server/customizations/ClusterFTrackingPing.cs`, read in full: constants/commands/formulas at lines 71-152; `Begin` and focus at 200-353; `Fire` payment at 356-387; scan and eligibility at 396-501; classification and labels at 503-626; summary at 664-717; pulse, warnings, and stop paths at 721-855; menus, paging, manual refresh, and row text at 859-1002.
- `server/patches/Tracking-ping-offer.patch`, `Tracking-radius-osi.patch`, and their registration at `docker/uo/apply-patches.sh:561-568`. Ping is an additive menu next to ordinary Tracking. Its range is independent of the normal Tracking clamp.
- `server/tests/Skills/TrackingPingVerification.cs`, read in full as source. The existing cases cover progression endpoints, gear exclusion, payment, canceled focus, cooldown, player/pet rules, refresh, menu access, and initial overload. These tests were not rerun.
- `server/customizations/ClusterFCreatureLevels.cs:43-78,95-119,206-225`: default provisional player comparison, configuration alternatives, and con bands. The canonical customization search found no assignment replacing `PlayerLevels` with an XP provider.
- `U/UOContent/Skills/Tracking/Tracking.cs:35-48`: stock menu and ten second skill delay; `U/UOContent/Multis/Houses/BaseHouse.cs:1421-1449`: location-based house lookup; `U/UOContent/Mobiles/PlayerMobile.cs:3239-3271`: tournament visibility veto absent from Ping's helper.
- `notes/wiki-drafts/rangers-custodians-healers.md`, including its planned Ping section and source/contradiction sections, for neighboring guide context.
- `tools/progress.py` to run the required reporter without changing generated output during this documentation-only task.

## Code versus design and build notes

- **Delivered stage:** code is the count and paged list foundation. There are no Ping map dots, client capability/protocol, radar opening/ring/countdown, world map overlay, quarry selection or guarded arrow, authored dungeon floors, League teaching entry, or automatically refreshed results header. P625 explicitly defers them. The guide does not promote them into player instructions.
- **Progression agrees:** code uses trained Base, 90 unlock, 120 player sensing, 15 stamina, one second focus, 30 second cooldown, and the design's square-radius and lifetime formulas capped at 200. Added 125 and 175 rows directly from the integer formula to show the seven and nine second steps. Equipment cannot extend a pulse; a drop below the captured Base ends it.
- **Floors and private areas:** all `DungeonRegion` casters are refused and all contacts in those regions are excluded. Elsewhere code checks only facet, square range, 16 Z, and house identity. The design's authored outdoor vertical-area handling and private camp/encounter-instance and restricted staff-area exclusions are absent. The guide describes height tolerance and explicitly avoids promising same-floor or instance isolation.
- **House wording:** P625 and code comments say the caster's own house. `IsEligible` actually compares `FindHouseAt(contact)` with `FindHouseAt(caster)`, with no ownership check. A contact inside the same house is allowed, subject to all other filters; owning the house while outside gives no exception. This is spatial scope, not property rights.
- **Players and pets:** 120 Base, 12 tile range from the caster's current position, and `InLOS` are implemented, but `CanSee` is not called. The conditional tournament visibility leak in P637 remains present. Hidden/staff-owner exclusion applies to a nonparty player's pet branch, not your own or party-owned pets. Only a player contact triggers the watched warning; sensing a pet alone does not warn its owner. The guide preserves these qualifications instead of repeating P625's opening blanket claim that no pet of a hidden owner is found.
- **Display and relation:** the actual list sorts hostiles, neutral animals, neutral NPCs, friendlies, then players, with distance ordering within each group. It has individual rows and ten per page, not expandable kind/threat groups. Friendly means own/party-owned creatures; the proposed explicitly allied NPC category is absent. Type-derived creature labels and player names/notoriety are implemented. Friendly pets have no threat band. Default difficulty comparison remains provisional combat skill, not player XP level or Tracking strength.
- **Skill-delay difference:** the command checks `NextSkillTime`, while every offer-menu press calls `Begin(pm, true)` and bypasses it without tying the exemption to that Tracking use. This contradicts the design's shared-delay requirement and the source header's claim that both routes share every check. Firing still raises the skill delay to at least ten seconds and both routes enforce the Ping cooldown. The guide states the current route difference without giving a bypass procedure.
- **Overload difference:** the design calls for cancellation and refund. Initial overload occurs before payment and costs nothing. Refresh overload calls `Finish(Overloaded)` after payment and leaves stamina and cooldown unchanged. The guide distinguishes them and omits the operational ceiling from its player-facing numbers, as the code explicitly requests. Other early endings likewise do not refund.
- **Expiry difference:** P625 says refreshes are strictly before expiry. Actual `OnTick` counts callbacks with `_elapsed` and does not compare `Core.Now` to `End`; P637's stalled-loop case remains applicable. The guide labels normal duration and notes the stall exception. The window itself is a snapshot until refreshed, including after concealment or expiry.
- **Resource cleanup:** P637's cooldown/warning dictionaries still retain expired records and character references. This remains an implementation follow-up, not a player mechanic. Nothing here repairs it or claims a measured memory incident.

## Verification and limits

No tests were added or run, consistent with lane tests of none. No build, client, live shard, tournament, real-map LOS/house check, dense-spawn benchmark, save/load, or memory probe was run. P625's reported gated build was read, not reproduced. Real client layout, deployed availability/settings, LOS and house behavior, broad classification coverage, and performance remain unverified; the draft identifies its source-only status.

No Haven connection, deployment, container operation, account/save operation, commit, merge, push, or branch switch was performed. No `server/uo/` files were read. All PowerShell commands used Windows PowerShell 5.1, reported as 5.1.26100.9711.

Final editorial review passed: plain ASCII, no em dashes or trailing whitespace, consistent Markdown table columns, local links resolving, and each requested file below 5 MB. Both work copies passed `git diff --check`; direct checks also covered these new untracked files. The code work copy is clean, and only the requested guide and this note are new in the notes work copy. The required progress reporter completed with work-copy path overrides and `--dry-run`; its known incidental `tools/progress.json` write was suppressed in memory, leaving generated files unchanged. No reporter inventory figures are used as feature evidence. Stop requests were checked between steps and were absent at the final check. There is no remaining work for P648; implementation repairs and later Ping stages remain outside this documentation task.

P648 DONE
