# P649: player guide draft for Persuasion

Written October 26, 2026. Deliverable: [wiki-drafts/social-skill.md](wiki-drafts/social-skill.md). This is a source-based draft for the merged stage 1 behavior, not a claim of deployment or client verification. No code changes.

## Sources read

Both work copies' `AGENTS.md`, plus this repo's `docs/direction-decision.md` and `docs/tasks.md`, were read before writing. The prompt's work-copy paths were used. Code HEAD was `a3f017e279e29eed0ac12c506ef51e6310291583`; notes HEAD was `49015d5742ba6cde464e7e278b5980dfd9065d87`. Read-only ModernUO was verified at the shard's pinned `d4531cd94b739613155225c234900de9f47d2c88`.

Build, design, and review notes:

- [cc-P626-build-social-skill.md](cc-P626-build-social-skill.md), including the built rules, reported tests and build, deviations, unverified items, and remaining-stage prompt drafts.
- [cc-P606-begging-skill-design.md](cc-P606-begging-skill-design.md), especially identity, charity, progression, and the proposed haggling, information, diplomacy, and training rules. Its proposals are not presented as implemented features.
- [cc-P626-build-social-skill-codex-review.md](cc-P626-build-social-skill-codex-review.md), for stale menu eligibility and backpack-only assignment tracking.
- [cc-P638-review-build-social-skill.md](cc-P638-review-build-social-skill.md), for town resolution, banker subclasses, lost rotation history, the bounded charity ledger, and missing runtime evidence.
- Existing `wiki-drafts/requisitions.md` and `wiki-drafts/thieves-den.md`, for the draft format and separation of source evidence from live availability.

Canonical shard sources, relative to the code work copy:

| File and locations | Evidence used |
| --- | --- |
| `server/customizations/ClusterFPersuasion.cs:36-71,87-195` | Constants, server rename in the same skill slot, callback, reveal, initial target eligibility, menu choices, and skill delay. |
| `server/customizations/ClusterFPersuasion.cs:200-364` | Effective skill and karma calculations, spawned civilian eligibility, account tags and UTC rollover, bounded taught-contact ledger, actual coins/bread, tutorial exception, and introductory practice. |
| `server/customizations/ClusterFPersuasion.cs:367-371` | Positive-bonus compensation and normal gain pipeline. |
| `server/customizations/ClusterFPersuasion.cs:375-552` | Hiring contacts, job difficulty unlocks, town lookup, backpack-only letter lookup, issue and expiry, destination selection and rotation, delivery validation, consumption before practice, and absence of job payouts. |
| `server/customizations/ClusterFExchangeLetter.cs` | Saved owner/type/town/facet/difficulty/expiry, blessed letter, exact recipient type check, instructions, remaining minutes, and drag/drop delivery. |
| `server/tests/Skills/PersuasionVerification.cs` | Read existing facts for identity, charity, account sharing, karma, practice limits, tier coverage, delivery, cap/lock, and tutorial behavior. The facts force gain rolls in training cases; their gains are not a guaranteed player reward. |
| `server/customizations/ClusterFSkillGain.cs:216-237` | Value-minus-Base bonus and `CheckSkillWornBonusIncluded` delegation to normal skill checks. Supporting rate and past-stock-ceiling code was also inspected. |
| `server/customizations/ClusterFSkillCaps.cs:11-31` | Default individual cap 200 and configurable cap settings. |
| `server/customizations/Items/Consumables/FrenchBread.cs` | `BegFrenchBread` inherits ordinary FrenchBread and adds its begging property. The old header saying staff-only predates P626's connected charity reward. |
| `player-package/payload/app/Build-UoOverrides.ps1:166-167,753` | Client skill renames currently cover Appraisal, not Persuasion. The guide tells players to use Begging if their list retains that name. |
| `server/customizations/CharacterCreation.cs:1018-1030` | Begging starter staff remains unchanged. |
| `server/customizations/ClusterFGuildStarterPath.cs:61,226` | Exchange skill association and New Haven bank contact. |
| `server/customizations/ClusterFGuildSystem.cs:215-223` | Separate 500-gold Exchange initiation task remains unchanged; courier issuance checks no membership or payment. |
| `server/patches/Begging-untrustworthy-achievement.patch` | Older refusal achievement hook; the new handler preserves its call. No hidden achievement discovery instructions were put in the player guide. |

Read-only pinned ModernUO sources:

- `Projects/UOContent/Skills/SkillCheck.cs:40-75`, for practice checks and the distinction between action success and a guaranteed skill gain.
- `Projects/Server/Regions/Region.cs:458-471`, for first matching region behavior rather than a search for a named town ancestor.
- `Distribution/Data/regions.json:3510-3522,3680-3695` and `Distribution/Data/Spawns/shared/malas/Vendors.json:237-250`, for Luna's unnamed bank subregion and the supplied Zento town data. Actual saved-world placement is unverified.
- `Projects/UOContent/Mobiles/Townfolk/Minter.cs` and `Projects/UOContent/Mobiles/Vendors/NPC/GypsyBanker.cs`, confirming both derive from Banker and therefore pass selection while failing an exact Banker type match at delivery.
- `Projects/UOContent/Mobiles/Vendors/GenericSell.cs:12-15`, for exact-type lookup in the standard sale-price table. This is not a complete custom-store or food resale audit.
- This repo's `tools/progress.py`, for its work-copy overrides and the write that occurs even with `--dry-run`.

## Code versus design and build prose

1. **Only stage 1 is merged.** The menu has Ask for help and Ask about work. The design's haggling, rumors, terms, calm, guard interaction, permanent Base-200 discount, titles, richer upper jobs, and tutorial relocation are future work. Their proposed numbers are excluded from the guide. There is no added NPC Persuasion context entry in this implementation; the guide uses the skill button.
2. **Courier work is unpaid.** The build note discloses this, but tutorial and expiry dialogue still refer to paid work or payment. `Deliver` deletes the letter and calls practice, without paying gold, standing, scrip, or Renown. The guide states the implemented reward explicitly.
3. **The tier thresholds are derived from the selector.** Unlock is `max(0, difficulty - 25)`, and the board chooses the hardest unlocked tier. This puts difficulty 110 at Base 85, difficulty 185 at 160, and difficulty 195 at 170. The design's broad profession bands and example at Base 100 are not the exact courier thresholds. The guide's table lists every current tier and covers through 200 subject to cap and destination availability.
4. **One letter is enforced only in the backpack.** `CarriedLetter` searches that container, not all outstanding work. The P626 review's stockpiling finding remains visible in source. The guide describes the backpack check and normal delivery flow without teaching the stockpiling exploit or claiming a durable one-job limit.
5. **Conversation validation is incomplete on menu response.** `Open` checks human body, uncontrolled/unsummoned status, life, range, and sight. `OnResponse` rechecks the NPC's life and coordinate range, but not all original conditions or matching maps/player life. This is the earlier P626 review finding, not repaired here. The guide explains the normal nearby conversation flow without promising comprehensive revalidation or describing a bypass.
6. **Route availability is conditional.** `TownOf` takes the first TownRegion name even if null. Luna's supplied bank is inside an unnamed town subregion. Non-novice selection accepts Banker subclasses but addresses the result to exact Banker; delivery checks exact type. The guide includes ordinary-banker troubleshooting, the Luna limitation, and the need for another recognized town after Base 10. Its Zento caveat refers to supplied content, not verified live placement. The board has no lower-tier fallback when the chosen tier has no destination.
7. **Rotation is not persistent.** The previous issued destination is only a static dictionary, so restart clears it. The guide qualifies rotation accordingly. Letter fields and charity tags have persistence support in source, but no save/load round trip was performed here.
8. **Charity practice is not a permanent once-ever contact ledger.** The design asks for distinct successful contacts below Base 20. Code remembers at most 200 account-wide taught contacts; eviction can allow old contacts to teach again. The set is a HashSet, so the build note's description of the retained entries as the newest 200 should not be treated as an ordered guarantee. Receiving help consumes the contact's practice credit even if the skill is locked or the gain fails. The guide qualifies the history and separates practice from gaining a point.
9. **Charity food has no complete economy restriction.** `BegFrenchBread` only adds a property to ordinary FrenchBread. It does not itself impose the design's no resale, salvage, requisition, or gifting rule. Standard vendor pricing uses exact types, but custom-store coverage was not exhaustively audited. The guide promises bread to eat and does not assert blanket nontransferability or zero resale value. Likewise, ExchangeLetter has no custom sale restriction in its class; no universal vendor-value claim is made for letters.
10. **Client identity and compatibility are partial.** Server skill name and callback change while saved slot, Base, cap, lock, and modifiers remain. The package rename table has not added Persuasion. The guide accommodates the Begging label and preserves the current thief-trial demonstration, which gives no coins, bread, or skill. Courier work does not replace the separate Exchange initiation task.

## Verification and limits

Read and compared the guide's amounts, UTC reset, eligibility, tier table, expiry, recipient rules, reward, and current feature scope against canonical implementation. No new tests or gates were added; this documentation-only task has no lane tests. P626's reported red/green tests and gated build were read, not rerun. No build, container, deployment, live-server connection, or client session was needed.

Unverified: deployed version/settings, live NPC placement and route completeness, real-client labels/menu/drag-drop appearance, actual training speed, persistence round trips, and a complete food/letter economy audit. The guide labels live availability unverified and makes no training-time promise.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these work copies; exit 0. The reporter still writes `tools/progress.json` in dry-run mode, so its original bytes were saved in memory and restored in a finally block; byte equality was confirmed. Its aggregate counts are not needed for this player guide and are not quoted as new evidence.

Final checks: both repositories' `git diff --check`, changed-file scope, ASCII/no-em-dash scan, file sizes below 5 MB, guide/source comparison, and stop-request checks. Only the requested guide and this note are changed. No code, `docs/`, services, saves, accounts, commits, merges, pushes, or branches were changed. All shell commands ran under Windows PowerShell 5.1. Completion marker is added only after these checks finish.

P649 DONE
