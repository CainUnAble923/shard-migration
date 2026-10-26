# P651: player guide draft for League warrants and the friendly Echo

Written October 26, 2026. Docs-only task. Output: [League Investigation Warrants and the friendly Echo](wiki-drafts/league-warrants-echo.md).

## Scope and result

The guide describes the merged stage 1 implementations, including their disabled defaults and missing player access. It does not turn the P565/P567 designs or the future-stage prompts appended to the build notes into released behavior. No code, configuration, tests, services, accounts, saves, or migration `docs/` were changed. Nothing was published or activated.

Code work-copy HEAD at inspection: `a3f017e279e29eed0ac12c506ef51e6310291583`. Migration work-copy HEAD: `24b3ae392c7d37ebee9870ba666c6b672b30da51`. These identify local merged source, not the running shard or remote deployment.

## Sources read

Paths beginning `server/` below are in the sibling ShatteredLegacy work copy. All other relative paths are in this migration work copy. Method names locate the specific evidence where a whole-file range would be less useful.

| Source | Evidence used |
|---|---|
| Both work copies' `AGENTS.md`; `docs/direction-decision.md`; `docs/tasks.md` | Working agreements, ModernUO direction, task context, writable notes scope. |
| [P629 build notes](cc-P629-build-league-warrants.md) | Stage 1 boundaries, accepted default numbers, Covetous relocation and reported offline map evidence, build claims, later-stage drafts. |
| [P630 build notes](cc-P630-build-echo-summon.md) | Packet 1 boundaries, accepted defaults, reported tests/build, missing Tome/player pages, deferred client, lifecycle, and balance evidence. |
| [P565 warrant design](cc-P565-design-league-reward-tokens.md), especially "What players see," "Numbers and encounter catalog," and "State, cancellation, and restart" | Intended purchase, consent, timers, rewards, ownership, persistence, and refunds, compared with actual implementation. |
| [P567 Echo design](cc-P567-design-summons-league-reward.md), especially "What players see," "Where it works and what it can attack," and "Call transaction and cleanup" | Intended free Tome issue/replacement and UI, profile, per-action eligibility, disconnect cleanup, no-award contract, release gates. |
| `server/customizations/LeagueInvestigations/LeagueInvestigationCatalog.cs:31` (`Settings`), `:67` (`Sites`), `:83` (`Encounters`), `CheckSite`, `SpawnTiles` | Off switch; constants; exact boss names and Trammel centers; data versus runtime validation. These are the two encounter entries counted for the guide: `investigation.siegebreaker` and `investigation.hollow-oak`. |
| `server/customizations/LeagueInvestigations/LeagueInvestigationWarrant.cs` (`GetProperties`, `CheckUse`, `Message`, `Directions`, both `OnDoubleClick` methods, binding overrides) | Tooltip promises versus actual checks; backpack ancestry, registration, owner, four-tile range; informational use only; marker behavior; no consumption. |
| `server/customizations/LeagueInvestigations/LeagueInvestigationSeeder.cs` (`Configure`, `Seed`, `FindMarker`) | Explicit marker placement only, no automatic placement or boss runner. No command was run. |
| `server/customizations/LeagueEchoes/LeagueEchoSettings.cs` | False by default, Mythril, 20 seconds, 1,800 seconds, 2 slots, 12-tile leash; settings are read on use. |
| `server/customizations/LeagueEchoes/LeagueEchoPolicy.cs` (`AllowedFacet`, `IsForbiddenRegion`, `TryFindSpawnTile`, `IsLegalTarget`) | Facet and region list, adjacent placement and line of sight, precise wild-creature filter. |
| `server/customizations/LeagueEchoes/LeagueEchoSystem.cs` (`Configure`, `Check`, `TryCall`, `Message`, `Dismiss`, `WhyEnd`, `Watch`, `OnCommand`) | Only staff command access; per-character rank; account active limit/cooldown; successful-call timing/reveal; refusal behavior; logout/death hooks; one-second checks and missing disconnect check. |
| `server/customizations/Mobiles/LeagueEchoes/LeagueDragonEcho.cs` | Exact profile, fixed melee AI, direct BaseCreature ancestry, no boss attacks, dissolution, no corpse/resources, target/owner harm checks, post-load deletion. |
| `server/customizations/ClusterFAccountData.cs:230`, `:474`, `:631`, `:733`, `:770`, `:794` | Persistent account Echo deadline and reserved character Tome serial, with older-version defaults. The serial field is not a delivered Tome. |
| `server/customizations/ClusterFLeagueRanks.cs` (`GetRank`, `RankName`, default Mythril row); `LeagueRegister/LeagueRegisterSettings.cs` (`Rank`) | Character-based rank and rank-key resolution. The guide avoids quoting an unverified live promotion table. |
| `server/customizations/LeagueShop/LeagueShop.cs` (`LeagueShopKind`, `Stock`); `server/customizations/LeagueRegistrarGump.cs` (menu and response definitions) | No investigation purchase row or Echo issue page. A source search for `LeagueEchoSystem`, `TomeOfEchoes`, warrant keys, warrant type, and `EchoTomeSerial` across tracked customizations confirms only the foundation integrations shown above. |
| [P629 initial review](cc-P629-build-league-warrants-codex-review.md); [P630 initial review](cc-P630-build-echo-summon-codex-review.md); [P641 warrant review](cc-P641-review-build-league-warrants.md); [P642 Echo review](cc-P642-review-build-echo-summon.md) | Existing defects and acceptance gaps. Review findings are attributed to their source reviews; no new runtime reproduction is claimed. |
| [Existing Register guide](wiki-drafts/league-register.md), opening sections | Existing wiki-draft tone and default-versus-live distinction. |
| `tools/progress.py`, opening and final functions | Work-copy path overrides and the reporter's dry-run write behavior. |

## Differences between designs, build notes, and current code

1. **Warrants are directions, not an encounter service yet.** P565 describes buying, consenting, starting, fighting, looting, and restoring a warrant after interruption. Current `OnDoubleClick` only calls `CheckUse` and sends a message. The AP/price/cooldown/roster/timer values are catalog constants, not implemented sales or timer enforcement. Even setting the switch true would only produce the informational "can be called here" message, not a spawn. No runner, run store, consent page, tracked combat policy, consumption, protected corpse, completion credit, or restart refund is present. The guide labels these as inactive rules.

2. **The built Covetous site differs from the design candidate.** P565 proposes Trammel 5440/2023 at the lake shore; the catalog uses 5472/1877/0 in the harpy hall. P629 explains the move because the shore overlaps the Void Pool event region. Yew remains 1059/1166/5; its catalog key is `yew-woods`, rather than the design candidate's `yew-investigation`. The guide uses catalog locations. P629's binary map checks were read as reported evidence, not independently rerun.

3. **Marker behavior is narrower than the design.** P565 describes directions and a warrant-use screen. The current marker sends a site/boss sentence and a closed-feature sentence when applicable. It never opens consent or starts a boss. Markers are not placed automatically. P629 says its seeder was not run; world placement is unverified here.

4. **Account binding does not guarantee custody through nested bags.** The direct warrant handlers refuse trade, ground drops, and foreign containers, but P641 finds that moving an ancestor bag bypasses those handlers. The recipient still fails ownership. The guide says another account cannot use it, describes direct restrictions, and mentions the nested-bag defect rather than promising complete nontransferability. No reproduction or fix was attempted in this docs-only task.

5. **Site validation has reviewed gaps.** P641 reports missing-map fallback acceptance and restricted-region overlaps hidden by priority or height. `CheckUse` checks the site's static flag; it does not call `CheckSite`. The draft does not certify live terrain, houses, regions, or safe spawning. These are later validation/integration requirements, not evidence that either coordinate is presently broken.

6. **The Tome and reward pages are still design-only.** P567 describes a free, reusable, character-bound book, issue/replacement, current-copy checks, and Call/Dismiss pages. P630 implements the runtime and reserves `EchoTomeSerial`; no item or UI consumes that field. The guide does not tell players to claim or replace a nonexistent Tome. Rank remains character-based; activity and cooldown remain account-based. No player command is present.

7. **Staff-only does not prove test-world-only.** The initial reviews report that command metadata does not enforce direct-command shard restrictions for either feature. The guide calls access staff-only without certifying that command handlers are restricted to the test shard. It provides no activation recipe or staff command walkthrough.

8. **Echo ending is not uniformly immediate.** P630's plain-language overview says it fades at once for distance, facet, or protected-place changes; source actually uses a one-second watchdog for those cases. P567 also requires eligibility before each harmful action, but the current override does not recheck all owner eligibility there, as the initial P630 review reports. The guide distinguishes event cleanup from periodic cleanup and mentions the brief enforcement gap.

9. **Disconnect is not logout.** P567 requires disconnect dissolution. `Configure` subscribes to Logout only, `Check`/`WhyEnd` do not check online state, and P642 traces the delayed-logout defect. The guide explicitly says an Echo may remain during the logout delay until its lifetime ends. It does not repeat P630's "fades at once if you log out" as an immediate-disconnect guarantee.

10. **No corpse or loot does not prove no rewards.** Source dissolves instead of normal death and returns no resources. P642 traces zero-hit deletion through the pet-loss achievement subscriber, which can award achievements/AP/Renown and related loot-box rewards. The guide preserves the verified no-corpse/no-loot statement, discloses the reviewed reward path, and avoids the design's absolute no-rewards promise. P642 remains the detailed defect evidence; this task does not claim a new reproducer or repeat build acceptance.

11. **PvE rules are specific type checks.** Active guarded regions are refused; a guarded region with guards disabled is permitted unless another listed restriction applies. SafeZone is refused even with its guards off. There is no blanket New Haven island prohibition or general rejection of every special encounter region. The draft names the implemented checks rather than promising the broader design acceptance cases are complete.

## Verification and limits

No lane tests are assigned. No tests, gates, or code were added, and no build, container, shard, or client was run. Red-first test requirements therefore do not apply to a new test in this task. P629/P630 build and test results are historical reports, not fresh P651 passes.

Unverified: live configuration and deployment, actual marker placement, current world houses/region composition, site walkability in a running world, client rendering, pet command behavior in a real fight, full world reload/follower reconciliation, and measured solo/party combat balance. The guide keeps these limits explicit and does not claim either foundation is ready for activation.

Windows PowerShell was confirmed as 5.1.26100.9711 using `powershell.exe`. The required `tools/progress.py --dry-run` ran with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0, report produced, no stderr. The reporter rewrites `tools/progress.json` even in dry-run mode; its exact starting bytes were restored. No generated progress or README change is retained, and no content-coverage totals are claimed.

Document checks passed for both requested files: UTF-8 decoding, ASCII-only text, no em dashes, no trailing whitespace, final newline, all Markdown links resolve locally, and each file is below 5 MB. Both repositories passed `git diff --check`; an explicit whitespace scan also covered the new untracked documents. Final status showed the code work copy clean and only the two requested Markdown files added in the migration work copy. The stop-request file was absent at the checkpoints, including the final validation step.

No Haven contact, deployment, account action, commit, merge, push, or branch switch was performed.

P651 DONE
