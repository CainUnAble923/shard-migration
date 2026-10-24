# P532: open-questions sweep record

October 24, 2026. Notes only. The decision list is [cc-P532-open-questions-for-chase.md](cc-P532-open-questions-for-chase.md).

## Result and scope

The list contains 199 question rows: 10 Now, 66 Build, 48 Future only, and 75 No. Of these, 77 retain P392 identifiers and 122 are additions or narrower consolidated questions. The primary screen contains 400 newly tracked Markdown notes; the broader date/change screen adds 24 supplemental notes. The 48 added text files are listed separately. These counts were computed from the manifests and final table, not from earlier estimates.

The list keeps one row per distinct choice, consolidates repeated asks, supplies a one-sentence question, condensed options, a recommended answer, and an explicit blocking consequence. Recommendations are this sweep's proposals, not Chase's decisions. "Now" is a reported unavailable player path, "Build" is a specification dependency for a later builder, "Future only" concerns proposed follow-up work, and "No" means an existing default can continue. The list includes optional questions explicitly offered in this week's notes; they are not silently promoted to blockers.

Read both work-copy AGENTS.md files first, followed by docs/README.md, direction-decision.md and tasks.md. No skill was needed for the explicitly requested Markdown deliverables. The working copies are the only write destinations. Source snapshot: code `70df7c5add59d18310be69b1950d06558f6ed6cd`, notes `42d9618445c7a0505af6ef51101ac435cb74eeb6`. No fetch, branch switch, commit, merge, or push occurred.

### How notes were selected

Used local Git history for October 20 at 00:00 through October 25 at 00:00, America/Chicago, inclusive of October 24. The primary manifest below lists existing Markdown files added in that window. A broader screen also checked changed notes and notes containing an October 20-24 date. That supplemental set includes older files with updates or mere date references, so it is not presented as newly authored work. File modification times were not used to date a note.

Searched headings and inline text for For Chase, Decisions for Chase, Open questions, Chase decides, unanswered, choices, recommendations, and conditional requests. Inspected candidate sections and followed repeats into P392, later audits, and answer records. The added text-file manifest covers wiki seed/draft text checked for direct For Chase/Open questions sections; none added another question. Review findings without a question are defect backlog, not a new request for Chase to decide. Administrative secret files were included by Git metadata only and were not used as substantive sources; no secret or fountain location from those files appears in this report.

P392 is itself an October 22 note. Its inherited questions therefore belong in this week's sweep even when the original note predates October 20. Retained U identifiers link to the exact P392 row and its original-note history. New S identifiers cite the direct note and line. Multiple later occurrences, such as P519's Herbalism recommendations and P528's Dented Box question, are consolidated rather than counted again.

## Answers and exclusions checked

The main answer sources were the relevant entries in docs/feature-queue.md, the dated decision logs in notes, notes/codex-questions.md, testing/decisions.json, P392's settled-items section, and later notes P478, P514-P519, P526, P528-P530. Followed the explicit later-answer references into the read-only prompts checkout where needed. A queued repair does not prove that the repair shipped, but an explicit recorded answer still removes the old question.

| Earlier ask | Answer or disposition used | Effect on this sweep |
|---|---|---|
| P376 Q1-Q9 and P392 U26/U30/U31/U77-U79 | [Feature queue:2018](../docs/feature-queue.md#L2018), October 23: named chapter ranks, six chapters, milestone bonuses, commission rank mapping, delivered shop, no AP/title totals, Leads as built, immediate requisition standing, no Warehouse/Featherweight, Scavenger retained. [P515:37](cc-P515-league-design-vs-build.md#L37) applies all nine. | No repeat approval question. Posting fees and future commission mechanics remain separate. |
| P179 Register decisions | [P280:54](cc-P280-league-register-build.md#L54) records the answered capacity/action/currency tables; [P515:35](cc-P515-league-design-vs-build.md#L35) identifies the October 21 answers. The formerly open bank question was answered October 23 above. | Keep the unanswered repair-number proposal, not another Register-design approval sheet. |
| P151 hall picks and P392 U69/U70/U72-U75 | [P281:1](cc-P281-guild-halls-placement.md#L1), [P516:19](cc-P516-guild-halls-design-vs-build.md#L19) and its per-guild table: keep, Felucca Den, shared Rangers/Dojo/Alembic, larger Artificers hall. | Do not repeat site alternatives. Maritime is now a Sea Market/site-validation follow-up, not the old Ocllo facet vote. NPC identity, travel and unassigned decor remain open. |
| P429 Blaze repair | [P478:34](cc-P478-wiki-catch-up-3.md#L34); queued P451:61, "Chase decided (10-22 15:50)": free, worn gear only. | Keep implementation defects out of the decision list. |
| P429 recycling ownership | [P528:97](cc-P528-achievements-loot-design-vs-build.md#L97); queued P457:44: own crafts or loot, not another player's fresh craft. | Do not ask whether any crafted item should count. |
| P429 large commission cooldown | [P478:60](cc-P478-wiki-catch-up-3.md#L60); queued P454:34: share the small commission reroll cooldown. | Accepted behavior, still implementation work where absent. |
| P429 farm pen | Queued P453:66: stock animals, open to visitors, no change. P476's instructions also repeat this answer. | No repeat pen-stock/visitor question. Future Rangers' delivered-animal fiction is a different choice. |
| P429/P392 tower walkability | [P516:67](cc-P516-guild-halls-design-vs-build.md#L67); queued P459:32: real door, walkable inside, floors/stairs and rendered/tested routes. | Walkability is answered. Which halls get which tower is still a later layout choice. |
| P289's old loop placeholder | [P371:11](cc-P371-graduation-is-the-first-loop.md#L11) records graduation as loop 1. P282 and f12-levels-loops-caps preserve approved S2, the ladder and raw reserve credit. | Do not ask for loop-zero/first-loop approval again. The current-level-50 prerequisite is still U01; saying graduation records loop 1 does not answer that prerequisite. Reserve valuation, current-level gate values, and skip/remedial handling are also separate retained questions. |
| P392 U15/U16 and P261's repeated acquisition/reset questions | Decision inbox P72-D2/D4/D5/D6/D7/D8/D9/D10 accepts acquisition, full contributor credit, dormancy, property kinds/limits, curve, helper gear and trading. [P392:220](cc-P392-open-design-questions.md#L220) explains the distinction. | Follow the accepted answer; a contrary implementation or overseer suggestion does not make the choice unanswered. Retain only numerical budgets and Echo-property conflict. P65-D5 keeps the deferred staff Bond Trial flag; U08 asks only about the eventual playable trial, not whether to keep that accepted flag. |
| P392 U20/U21 and P212/P405's inn-region alternatives | F-4's October 3 answer sets one player character with exemptions. [F-44:3287](../docs/feature-queue.md#L3287) settles an instanced, non-growing room through any inn, weekly rent and the real-house exit. | Do not reopen the answered shape or invent a new character count from an "open" reminder. Rent values, limits, visitors and loop persistence remain unanswered. |
| P392 U34/U35/U43/U44 and the scope of U37 | P417:586-596 revises the gathering proposal; [P518:84](cc-P518-skill-gain-paths-vs-code.md#L84) says the wood tier ladder already has approval. | Consolidate old pay/schedule/check proposals into the later economy/credit/check choices. U37 retains only the exact teaching-window question; do not ask for the approved harvest ladder again. P235's distinct Rush, Survey, Haul, gem, discovery and granite choices remain future inputs. |
| P392 U29 | October 23 retains the Scavenger. | Drop the replacement-for-Scavenger premise; retain separate sorting/ranged-bandaging enhancements only. |
| P201 trap table | [P275:14](cc-P275-deployable-traps-build.md#L14): Chase approved D1-D7. | No repeated approval of the skill/guild/monster-only/practice design. Proposed PvP exclusions are a separate later policy. |
| P214 tool-trial choices | [P214:123](cc-P214-tool-trials.md#L123), "Phase 1 decisions and Chase's answers (2026-10-20 17:07)." | The answered trial plan is not open. |
| P218 missing Mage/Crafter designs | P286 documents/tests the supplied SL_Mage and SL_Crafter designs. | An obsolete missing-input stop is not an unanswered Chase design question. |
| P158/P159 lane sign-in, old SMB setup and enabling | P373 finishes and enables the named lanes; the current task runs through that arrangement. P159 already says P184/P186 superseded its old SMB shape. | Do not ask again for sign-in/enabling or replacement by obsolete lane architecture. Owner-specific hours/Docker and password command-line exposure remain separate. |
| P188 approval of the old way in | The earlier round-four renders were approved; queued P413 replaces the hole/ladder entrance with an anthill direction. | Do not ask again to widen the superseded gap/hole. A fresh render review belongs to the new map task. |
| P405 Halloween lane | P408 implements the faithful Pumpkin King event. | Do not repeat the original this-year lane choice. Other intake ideas remain separate options. |
| P405 levelable-gear gate and inn/hall Town House alternatives | P72-D5 accepts wearable items with dormant excess bonuses; F-44 accepts instancing and P281 uses the chosen native halls. | Preserve those answers. Additional gate tiles, sockets, leaseholds and other new ideas still appear separately. |
| P529's Young-death routing concern | Decision inbox P141-D2 explicitly says keep built: stock New Haven healer routing. | Excluded even though the newer audit calls it a decision remaining. This is a concrete answered-question correction. |
| P476's spawn-bounds documentation row | P476:1028 asks to record the discrepancy beside D-138. | Recordkeeping work, not a missing choice. |
| Publication/build/world-state questions | P526:116/119/122/123 needs running-build, boss-drop, spawn and veteran-config evidence. P377/P478 also request publication or screenshots. | Unverified factual checks and actions, not opinion questions. Keep the actual Tamer-box route, retroactive mount policy and dragon design questions. |
| Known defects and ordinary follow-ups | P429/P476/P480 and review notes describe fixes, prefix cleanup, dark text, tests and deployments. | Do not ask Chase to vote on confirmed defects. Do not turn deployment or play-test instructions into unanswered product policy. |

P234's required fidelity recording and the standing rule to send art through Chase's art workflow are already instructions, not new permission questions. No art was generated or requested by this sweep.

## Verification and limits

Lane tests: none. No new test was added; there is no red/green claim. Editorial checks validate the report, not shard behavior: unique IDs, six columns, one question sentence per row, nonempty options/recommendations/blocking fields, local source existence and line bounds, blocker ordering, no em dashes, no trailing whitespace, and files below 5 MB. No code, configuration, accounts, saves, generated server/uo files, docs/ files, or services were edited. No Haven connection, Docker command, deployment, restart, or external message was made.

Ran tools/progress.py --dry-run with SL_SHARD and SL_MIGRATE pointing to the two assigned work copies. Exit 0. The reporter still attempts to write tools/progress.json before honoring --dry-run. A process-local Path.write_text guard suppressed that one known write and refused any other text write. The original progress.json bytes stayed identical. Its aggregate content counts are not used as question evidence. Windows PowerShell reports 5.1.26100.9711; Python ran with -B for the reporter.

This is a local written-record sweep. It cannot verify private chats or decisions not saved in the checked records, actual save contents, whether a planned reward is deployed, owner preferences never recorded, or current running configuration. "No later explicit answer found" is not a claim that Chase never answered elsewhere. Headline source/line references are for the snapshot above and may move in later prompts. No bug described in an input was reproduced here.

Stop-request checks at step boundaries were clear while preparing the report. Final scope and whitespace checks are recorded after the manifests below.

## Primary source manifest

All paths below are relative to shard-migration. This is the file list beside the primary source count, including review-only notes and notes with no remaining question. Inclusion in the manifest does not mean a file contributed a decision row.

- `notes/admin/secrets.md`
- `notes/art/guild-menus/art-requests.md`
- `notes/cc-P149-away-mode-and-email-controls.md`
- `notes/cc-P151-guild-halls-survey.md`
- `notes/cc-P153-queue-notes-and-package-whats-new.md`
- `notes/cc-P156-night-shift-batches.md`
- `notes/cc-P157-plain-english-emails.md`
- `notes/cc-P158-codex-second-agent-codex-review.md`
- `notes/cc-P158-codex-second-agent.md`
- `notes/cc-P159-codex-lane-second-pc-codex-review.md`
- `notes/cc-P159-codex-lane-second-pc.md`
- `notes/cc-P169-requirement-colors.md`
- `notes/cc-P172-pet-gain-speed.md`
- `notes/cc-P177-guild-menus-template-mockups.md`
- `notes/cc-P179-league-design-pass.md`
- `notes/cc-P187-cont-web-console-parity.md`
- `notes/cc-P188-cont-rootdeep-goes-in.md`
- `notes/cc-P189-cont-old-haven-new-player-safe.md`
- `notes/cc-P190-cont-test-crystal.md`
- `notes/cc-P192-cont-fountain-of-youth.md`
- `notes/cc-P193-port-high-seas-fishing.md`
- `notes/cc-P194-port-wrong-and-covetous-void.md`
- `notes/cc-P195-port-exodus-encounter.md`
- `notes/cc-P196-port-blackthorn-dungeon-codex-review.md`
- `notes/cc-P196-port-blackthorn-dungeon.md`
- `notes/cc-P197-port-underworld-mini-champions.md`
- `notes/cc-P198-port-eodon-remainder.md`
- `notes/cc-P199-port-base-items-remainder.md`
- `notes/cc-P200-cont-marathon-mode.md`
- `notes/cc-P201-deployable-traps-design.md`
- `notes/cc-P204-cont-fixup-cont-fixup-cont-earned-skill-gain.md`
- `notes/cc-P207-golem-card-glow.md`
- `notes/cc-P208-cont-shadow-iron-merger.md`
- `notes/cc-P211-svdungeon-070-assessment.md`
- `notes/cc-P212-code-intake-batch-1.md`
- `notes/cc-P213-cont-changelog-version-merges.md`
- `notes/cc-P214-tool-trials.md`
- `notes/cc-P215-golem-test-accounts-codex-review.md`
- `notes/cc-P215-golem-test-accounts.md`
- `notes/cc-P216-golem-questions-in-console.md`
- `notes/cc-P217-crystal-wiki-catch-up.md`
- `notes/cc-P218-crystal-mage-crafter-scripts.md`
- `notes/cc-P219-tazuo-script-test-harness.md`
- `notes/cc-P220-crystal-status-page-judgments.md`
- `notes/cc-P221-cont-fixup-port-wrong-and-covetous-void.md`
- `notes/cc-P222-tinker-golem-watchdog.md`
- `notes/cc-P224-playtest-bot-checks-second.md`
- `notes/cc-P226-arms-lore-matters.md`
- `notes/cc-P227-extended-wood-bonuses.md`
- `notes/cc-P228-exceptional-material-gap.md`
- `notes/cc-P229-league-reward-shop.md`
- `notes/cc-P230-staff-hub-events-tab.md`
- `notes/cc-P231-osi-joke-achievements.md`
- `notes/cc-P232-pkcs-pin-drop-audit-flag.md`
- `notes/cc-P233-props-ability-profile.md`
- `notes/cc-P234-dismount-sources-design.md`
- `notes/cc-P235-work-order-numbers-pass.md`
- `notes/cc-P236-satchel-icons-ship-codex-review.md`
- `notes/cc-P236-satchel-icons-ship.md`
- `notes/cc-P237-new-haven-community-art-codex-review.md`
- `notes/cc-P237-new-haven-community-art.md`
- `notes/cc-P238-climbing-boots.md`
- `notes/cc-P239-creature-levels-appraisal.md`
- `notes/cc-P240-fog-of-war-client-half.md`
- `notes/cc-P241-achievement-category-icons.md`
- `notes/cc-P243-league-hall-decor-rewards.md`
- `notes/cc-P260-herbalism-research.md`
- `notes/cc-P261-levelable-gear-build.md`
- `notes/cc-P262-accessory-slots.md`
- `notes/cc-P263-noted-by-the-system-achievements.md`
- `notes/cc-P265-guild-hall-decor-packs.md`
- `notes/cc-P266-new-haven-winter-decor-codex-review.md`
- `notes/cc-P266-new-haven-winter-decor.md`
- `notes/cc-P267-halloween-bank-decor.md`
- `notes/cc-P268-high-seas-ships-assessment.md`
- `notes/cc-P274-fable-week-tracking-codex-review.md`
- `notes/cc-P274-fable-week-tracking.md`
- `notes/cc-P275-deployable-traps-build.md`
- `notes/cc-P276-tutorial-farm-build.md`
- `notes/cc-P277-rideable-red-dragon-codex-review.md`
- `notes/cc-P277-rideable-red-dragon.md`
- `notes/cc-P280-league-register-build.md`
- `notes/cc-P281-guild-halls-placement-codex-review.md`
- `notes/cc-P281-guild-halls-placement.md`
- `notes/cc-P282-f12-numbers-and-level-gates-codex-review.md`
- `notes/cc-P282-f12-numbers-and-level-gates.md`
- `notes/cc-P282-scratch/approved-tables.md`
- `notes/cc-P282-scratch/proposal-template.md`
- `notes/cc-P282-scratch/tables.md`
- `notes/cc-P283-skill-gain-paths-research-codex-review.md`
- `notes/cc-P283-skill-gain-paths-research.md`
- `notes/cc-P286-crystal-mage-crafter-docs-and-tests.md`
- `notes/cc-P286-test-plans.md`
- `notes/cc-P287-golem-weekend-days-and-self-idle.md`
- `notes/cc-P288-package-notes-autofill-codex-review.md`
- `notes/cc-P288-package-notes-autofill.md`
- `notes/cc-P289-tutorial-core-trials-playable-codex-review.md`
- `notes/cc-P289-tutorial-core-trials.md`
- `notes/cc-P290-tutorial-wing-trials-combat-magic.md`
- `notes/cc-P291-tutorial-wing-trials-trades-and-more-codex-review.md`
- `notes/cc-P291-tutorial-wing-trials-trades.md`
- `notes/cc-P352-cont-fog-of-war-client-half.md`
- `notes/cc-P353-cont-golem-questions-install-and-round.md`
- `notes/cc-P357-cont-fog-of-war-client-half.md`
- `notes/cc-P359-chopped-tree-stumps-codex-review.md`
- `notes/cc-P359-chopped-tree-stumps.md`
- `notes/cc-P362-ui-skins-player-options.md`
- `notes/cc-P364-league-bestiary-batch-2.md`
- `notes/cc-P365-reward-mounts-and-evo-stages.md`
- `notes/cc-P366-cont-fixup-cont-loot-box-flying-loot.md`
- `notes/cc-P367-music-room-console-page.md`
- `notes/cc-P368-added-music-areas-monsters-bosses-codex-review.md`
- `notes/cc-P368-added-music-areas-monsters-bosses.md`
- `notes/cc-P369-cont-fixup-companions-b1-base-and-record.md`
- `notes/cc-P370-golem-fixes-flaky-builds-reclaims-codex-review.md`
- `notes/cc-P370-golem-fixes-flaky-builds-reclaims.md`
- `notes/cc-P371-graduation-is-the-first-loop-codex-review.md`
- `notes/cc-P371-graduation-is-the-first-loop.md`
- `notes/cc-P373-codex-golems-finish-and-enable-codex-review.md`
- `notes/cc-P373-codex-golems-finish-and-enable.md`
- `notes/cc-P374-league-player-guide-draft.md`
- `notes/cc-P376-league-decisions.md`
- `notes/cc-P377-crystal-wiki-catch-up-2.md`
- `notes/cc-P378-playtest-plans-10-21-codex-review.md`
- `notes/cc-P378-playtest-plans-10-21.md`
- `notes/cc-P379-crystal-review-10-21-merges.md`
- `notes/cc-P381-guild-guide-society-of-smiths-codex-review.md`
- `notes/cc-P381-guild-guide-society-of-smiths.md`
- `notes/cc-P382-guild-guide-order-of-the-alembic-codex-review.md`
- `notes/cc-P382-guild-guide-order-of-the-alembic.md`
- `notes/cc-P383-guild-guide-artificers-order-codex-review.md`
- `notes/cc-P383-guild-guide-artificers-order.md`
- `notes/cc-P384-guild-guide-thieves-den-codex-review.md`
- `notes/cc-P384-guild-guide-thieves-den.md`
- `notes/cc-P385-guide-gathering-guilds-codex-review.md`
- `notes/cc-P385-guide-gathering-guilds.md`
- `notes/cc-P386-guide-rangers-custodians-healers-codex-review.md`
- `notes/cc-P386-guide-rangers-custodians-healers.md`
- `notes/cc-P387-guide-achievements-and-loot-boxes-codex-review.md`
- `notes/cc-P387-guide-achievements-and-loot-boxes.md`
- `notes/cc-P388-guide-levels-loops-and-scrolls-codex-review.md`
- `notes/cc-P388-guide-levels-loops-and-scrolls.md`
- `notes/cc-P389-guide-companions-and-evo-pets-codex-review.md`
- `notes/cc-P389-guide-companions-and-evo-pets.md`
- `notes/cc-P390-guide-crafting-changes-codex-review.md`
- `notes/cc-P390-guide-crafting-changes.md`
- `notes/cc-P391-guide-new-haven-start-codex-review.md`
- `notes/cc-P391-guide-new-haven-start.md`
- `notes/cc-P392-open-design-questions-codex-review.md`
- `notes/cc-P392-open-design-questions.md`
- `notes/cc-P393-guide-high-seas-fishing-codex-review.md`
- `notes/cc-P393-guide-high-seas-fishing.md`
- `notes/cc-P394-shard-glossary-codex-review.md`
- `notes/cc-P394-shard-glossary.md`
- `notes/cc-P395-wiki-drafts-cross-check-codex-review.md`
- `notes/cc-P395-wiki-drafts-cross-check.md`
- `notes/cc-P396-guide-dungeons-codex-review.md`
- `notes/cc-P396-guide-dungeons.md`
- `notes/cc-P397-new-player-faq-codex-review.md`
- `notes/cc-P397-new-player-faq.md`
- `notes/cc-P398-feature-queue-audit-codex-review.md`
- `notes/cc-P398-feature-queue-audit.md`
- `notes/cc-P399-guild-index-page-codex-review.md`
- `notes/cc-P399-guild-index-page.md`
- `notes/cc-P400-review-p380-stumps-code-codex-review.md`
- `notes/cc-P400-review-p380-stumps-code.md`
- `notes/cc-P401-review-p282-loop-scrolls-code-codex-review.md`
- `notes/cc-P401-review-p282-loop-scrolls-code.md`
- `notes/cc-P402-review-noted-achievements-code-codex-review.md`
- `notes/cc-P402-review-noted-achievements-code.md`
- `notes/cc-P403-review-music-room-and-area-music-codex-review.md`
- `notes/cc-P403-review-music-room-and-area-music.md`
- `notes/cc-P404-review-bestiary-batch-2-codex-review.md`
- `notes/cc-P404-review-bestiary-batch-2.md`
- `notes/cc-P405-servuo-batch-1022-research-codex-review.md`
- `notes/cc-P405-servuo-batch-1022.md`
- `notes/cc-P406-patch-notes-2026-10-22-codex-review.md`
- `notes/cc-P406-patch-notes-2026-10-22.md`
- `notes/cc-P407-review-eodon-port-code-codex-review.md`
- `notes/cc-P407-review-eodon-port-code.md`
- `notes/cc-P408-sorcerers-dungeon-halloween-codex-review.md`
- `notes/cc-P408-sorcerers-dungeon-halloween.md`
- `notes/cc-P410-tinker-only-email-codex-review.md`
- `notes/cc-P410-tinker-only-email.md`
- `notes/cc-P417-gathering-orders-design-codex-review.md`
- `notes/cc-P417-gathering-orders-design.md`
- `notes/cc-P418-review-league-register-code-codex-review.md`
- `notes/cc-P418-review-league-register-code.md`
- `notes/cc-P419-review-guild-hall-decor-packs-codex-review.md`
- `notes/cc-P419-review-guild-hall-decor-packs.md`
- `notes/cc-P420-review-tutorial-framework-codex-review.md`
- `notes/cc-P420-review-tutorial-framework.md`
- `notes/cc-P421-review-tutorial-farm-codex-review.md`
- `notes/cc-P421-review-tutorial-farm.md`
- `notes/cc-P422-review-requisitions-and-leads-codex-review.md`
- `notes/cc-P422-review-requisitions-and-leads.md`
- `notes/cc-P423-review-bulk-orders-port-codex-review.md`
- `notes/cc-P423-review-bulk-orders-port.md`
- `notes/cc-P424-review-fog-of-war-client-codex-review.md`
- `notes/cc-P424-review-fog-of-war-client.md`
- `notes/cc-P425-review-rootdeep-way-in-codex-review.md`
- `notes/cc-P425-review-rootdeep-way-in.md`
- `notes/cc-P426-review-high-seas-fishing-codex-review.md`
- `notes/cc-P426-review-high-seas-fishing.md`
- `notes/cc-P428-crystal-review-10-22-merges.md`
- `notes/cc-P429-crystal-codex-findings-to-fixes.md`
- `notes/cc-P430-review-rootdeep-burrows-build-codex-review.md`
- `notes/cc-P430-review-rootdeep-burrows-build.md`
- `notes/cc-P431-review-guild-starter-path-codex-review.md`
- `notes/cc-P431-review-guild-starter-path.md`
- `notes/cc-P432-review-clean-up-britannia-codex-review.md`
- `notes/cc-P432-review-clean-up-britannia.md`
- `notes/cc-P433-review-dungeon-build-1-codex-review.md`
- `notes/cc-P433-review-dungeon-build-1.md`
- `notes/cc-P434-review-recipe-gating-codex-review.md`
- `notes/cc-P434-review-recipe-gating.md`
- `notes/cc-P435-review-smith-orders-2-codex-review.md`
- `notes/cc-P435-review-smith-orders-2.md`
- `notes/cc-P437-review-league-reward-shop-codex-review.md`
- `notes/cc-P437-review-league-reward-shop.md`
- `notes/cc-P438-review-deployable-traps-build-codex-review.md`
- `notes/cc-P438-review-deployable-traps-build.md`
- `notes/cc-P439-review-cont-fountain-of-youth-codex-review.md`
- `notes/cc-P439-review-cont-fountain-of-youth.md`
- `notes/cc-P440-review-arms-lore-matters-codex-review.md`
- `notes/cc-P440-review-arms-lore-matters.md`
- `notes/cc-P441-review-extended-wood-bonuses-codex-review.md`
- `notes/cc-P441-review-extended-wood-bonuses.md`
- `notes/cc-P442-review-exceptional-material-gap-codex-review.md`
- `notes/cc-P442-review-exceptional-material-gap.md`
- `notes/cc-P443-review-cont-earned-skill-gain-codex-review.md`
- `notes/cc-P443-review-cont-earned-skill-gain.md`
- `notes/cc-P444-review-port-blackthorn-dungeon-codex-review.md`
- `notes/cc-P444-review-port-blackthorn-dungeon.md`
- `notes/cc-P445-review-port-underworld-mini-champions-codex-review.md`
- `notes/cc-P445-review-port-underworld-mini-champions.md`
- `notes/cc-P446-review-creature-levels-appraisal-codex-review.md`
- `notes/cc-P446-review-creature-levels-appraisal.md`
- `notes/cc-P447-review-cont-old-haven-new-player-safe-codex-review.md`
- `notes/cc-P447-review-cont-old-haven-new-player-safe.md`
- `notes/cc-P448-review-pet-gain-speed-codex-review.md`
- `notes/cc-P448-review-pet-gain-speed.md`
- `notes/cc-P449-review-graduation-is-the-first-loop-codex-review.md`
- `notes/cc-P449-review-graduation-is-the-first-loop.md`
- `notes/cc-P450-review-monster-stealing-shard-rules-codex-review.md`
- `notes/cc-P450-review-monster-stealing-shard-rules.md`
- `notes/cc-P461-review-sorcerers-dungeon-halloween-codex-review.md`
- `notes/cc-P461-review-sorcerers-dungeon-halloween.md`
- `notes/cc-P462-review-rideable-red-dragon-codex-review.md`
- `notes/cc-P462-review-rideable-red-dragon.md`
- `notes/cc-P463-review-guild-halls-placement-codex-review.md`
- `notes/cc-P463-review-guild-halls-placement.md`
- `notes/cc-P464-review-package-notes-autofill-codex-review.md`
- `notes/cc-P464-review-package-notes-autofill.md`
- `notes/cc-P465-review-staff-hub-events-tab-codex-review.md`
- `notes/cc-P465-review-staff-hub-events-tab.md`
- `notes/cc-P466-review-osi-joke-achievements-codex-review.md`
- `notes/cc-P466-review-osi-joke-achievements.md`
- `notes/cc-P467-review-new-haven-community-art-codex-review.md`
- `notes/cc-P467-review-new-haven-community-art.md`
- `notes/cc-P468-review-league-hall-decor-rewards-codex-review.md`
- `notes/cc-P468-review-league-hall-decor-rewards.md`
- `notes/cc-P469-review-tool-trials-codex-review.md`
- `notes/cc-P469-review-tool-trials.md`
- `notes/cc-P470-review-work-order-numbers-pass-codex-review.md`
- `notes/cc-P470-review-work-order-numbers-pass.md`
- `notes/cc-P471-review-requirement-colors-codex-review.md`
- `notes/cc-P471-review-requirement-colors.md`
- `notes/cc-P472-review-away-mode-and-email-controls-codex-review.md`
- `notes/cc-P472-review-away-mode-and-email-controls.md`
- `notes/cc-P473-review-halloween-bank-decor-codex-review.md`
- `notes/cc-P473-review-halloween-bank-decor.md`
- `notes/cc-P474-review-league-bestiary-batch-2-codex-review.md`
- `notes/cc-P474-review-league-bestiary-batch-2.md`
- `notes/cc-P476-crystal-codex-findings-round-2.md`
- `notes/cc-P477-crystal-review-10-23-merges.md`
- `notes/cc-P478-wiki-catch-up-3.md`
- `notes/cc-P480-tutorial-first-play-fixes-codex-review.md`
- `notes/cc-P480-tutorial-first-play-fixes.md`
- `notes/cc-P482-review-levelable-gear-build-codex-review.md`
- `notes/cc-P482-review-levelable-gear-build.md`
- `notes/cc-P483-review-flying-loot-codex-review.md`
- `notes/cc-P483-review-flying-loot.md`
- `notes/cc-P484-review-climbing-boots-codex-review.md`
- `notes/cc-P484-review-climbing-boots.md`
- `notes/cc-P486-review-accessory-slots-codex-review.md`
- `notes/cc-P486-review-accessory-slots.md`
- `notes/cc-P487-review-companions-b1-base-codex-review.md`
- `notes/cc-P487-review-companions-b1-base.md`
- `notes/cc-P488-review-exodus-encounter-codex-review.md`
- `notes/cc-P488-review-exodus-encounter.md`
- `notes/cc-P489-review-wrong-and-covetous-void-codex-review.md`
- `notes/cc-P489-review-wrong-and-covetous-void.md`
- `notes/cc-P490-review-achievement-category-icons.md`
- `notes/cc-P491-review-underworld-mini-champions-2-codex-review.md`
- `notes/cc-P491-review-underworld-mini-champions-2.md`
- `notes/cc-P492-review-tinker-golem-watchdog-codex-review.md`
- `notes/cc-P492-review-tinker-golem-watchdog.md`
- `notes/cc-P493-review-golem-test-accounts-codex-review.md`
- `notes/cc-P493-review-golem-test-accounts.md`
- `notes/cc-P494-review-artificers-unravel-container-codex-review.md`
- `notes/cc-P494-review-artificers-unravel-container.md`
- `notes/cc-P495-review-usable-ankhs-codex-review.md`
- `notes/cc-P495-review-usable-ankhs.md`
- `notes/cc-P496-review-props-ability-profile-codex-review.md`
- `notes/cc-P496-review-props-ability-profile.md`
- `notes/cc-P497-review-pkcs-pin-drop-audit-flag-codex-review.md`
- `notes/cc-P497-review-pkcs-pin-drop-audit-flag.md`
- `notes/cc-P498-review-web-console-parity-codex-review.md`
- `notes/cc-P498-review-web-console-parity.md`
- `notes/cc-P499-review-marathon-mode-codex-review.md`
- `notes/cc-P499-review-marathon-mode.md`
- `notes/cc-P500-review-changelog-version-merges-codex-review.md`
- `notes/cc-P500-review-changelog-version-merges.md`
- `notes/cc-P501-review-achievements-button-codex-review.md`
- `notes/cc-P501-review-achievements-button.md`
- `notes/cc-P502-review-tutorial-first-play-fixes-codex-review.md`
- `notes/cc-P502-review-tutorial-first-play-fixes.md`
- `notes/cc-P503-review-tutorial-wing-combat-magic-codex-review.md`
- `notes/cc-P503-review-tutorial-wing-combat-magic.md`
- `notes/cc-P504-review-rootdeep-goes-in-codex-review.md`
- `notes/cc-P504-review-rootdeep-goes-in.md`
- `notes/cc-P505-review-kitsune-paperdoll-refit-codex-review.md`
- `notes/cc-P505-review-kitsune-paperdoll-refit.md`
- `notes/cc-P506-review-plain-english-emails-codex-review.md`
- `notes/cc-P506-review-plain-english-emails.md`
- `notes/cc-P507-review-night-shift-batches-codex-review.md`
- `notes/cc-P507-review-night-shift-batches.md`
- `notes/cc-P508-review-vseuoaware-staff-commands-codex-review.md`
- `notes/cc-P508-review-vseuoaware-staff-commands.md`
- `notes/cc-P509-review-playtest-decisions-inbox-codex-review.md`
- `notes/cc-P509-review-playtest-decisions-inbox.md`
- `notes/cc-P510-review-queue-notes-and-package-whats-new.md`
- `notes/cc-P511-review-package-builds-from-tazuo-codex-review.md`
- `notes/cc-P511-review-package-builds-from-tazuo.md`
- `notes/cc-P512-play-test-plans-for-the-10-22-codex-review.md`
- `notes/cc-P512-play-test-plans-for-the-10-22.md`
- `notes/cc-P513-patch-notes-2026-10-23.md`
- `notes/cc-P513-patch-notes-for-10-23.md`
- `notes/cc-P514-feature-queue-audit-2.md`
- `notes/cc-P514-feature-queue-audit-round-2-codex-review.md`
- `notes/cc-P514-feature-queue-audit-round-2.md`
- `notes/cc-P515-league-design-vs-build.md`
- `notes/cc-P515-the-league-design-against-what-is-built-codex-review.md`
- `notes/cc-P515-the-league-design-against-what-is-built.md`
- `notes/cc-P516-guild-halls-design-vs-build.md`
- `notes/cc-P516-guild-halls-survey-and-design-against-what-codex-review.md`
- `notes/cc-P516-guild-halls-survey-and-design-against-what.md`
- `notes/cc-P517-f-12-numbers-against-the-code-codex-review.md`
- `notes/cc-P517-f-12-numbers-against-the-code.md`
- `notes/cc-P517-f12-numbers-vs-code.md`
- `notes/cc-P518-skill-gain-paths-research-against-the-code-codex-review.md`
- `notes/cc-P518-skill-gain-paths-research-against-the-code.md`
- `notes/cc-P518-skill-gain-paths-vs-code.md`
- `notes/cc-P519-herbalism-research-against-what-is-built-codex-review.md`
- `notes/cc-P519-herbalism-research-against-what-is-built.md`
- `notes/cc-P519-herbalism-vs-build.md`
- `notes/cc-P521-review-reward-mounts-evo-stages-codex-review.md`
- `notes/cc-P521-review-reward-mounts-evo-stages.md`
- `notes/cc-P522-review-quest-markers-codex-review.md`
- `notes/cc-P522-review-quest-markers.md`
- `notes/cc-P523-review-tutorial-trades-wing-codex-review.md`
- `notes/cc-P523-review-tutorial-trades-wing.md`
- `notes/cc-P524-review-golem-fixes-flaky-builds-codex-review.md`
- `notes/cc-P524-review-golem-fixes-flaky-builds.md`
- `notes/cc-P525-guide-new-player-tutorial-codex-review.md`
- `notes/cc-P525-guide-new-player-tutorial.md`
- `notes/cc-P526-guide-mounts-and-reward-mounts-codex-review.md`
- `notes/cc-P526-guide-mounts-and-reward-mounts.md`
- `notes/cc-P526-guide-mounts.md`
- `notes/cc-P528-achievements-loot-design-vs-build.md`
- `notes/cc-P528-design-vs-build-achievements-loot-codex-review.md`
- `notes/cc-P528-design-vs-build-achievements-loot.md`
- `notes/cc-P529-design-vs-build-new-haven-dungeon-codex-review.md`
- `notes/cc-P529-design-vs-build-new-haven-dungeon.md`
- `notes/cc-P529-new-haven-dungeon-design-vs-build.md`
- `notes/cc-P530-clean-up-britannia-design-vs-build.md`
- `notes/cc-P530-design-vs-build-clean-up-britannia.md`
- `notes/feature-queue-audit-2026-10-22.md`
- `notes/patch-notes-2026-10-22.md`
- `notes/wiki-drafts/achievements-and-loot-boxes.md`
- `notes/wiki-drafts/artificers-order.md`
- `notes/wiki-drafts/companions-and-evo-pets.md`
- `notes/wiki-drafts/crafting-changes.md`
- `notes/wiki-drafts/cross-check-2026-10-22.md`
- `notes/wiki-drafts/dungeons.md`
- `notes/wiki-drafts/gathering-guilds.md`
- `notes/wiki-drafts/glossary.md`
- `notes/wiki-drafts/guilds.md`
- `notes/wiki-drafts/high-seas-fishing.md`
- `notes/wiki-drafts/league.md`
- `notes/wiki-drafts/levels-loops-and-scrolls.md`
- `notes/wiki-drafts/mounts.md`
- `notes/wiki-drafts/new-haven-start.md`
- `notes/wiki-drafts/new-player-faq.md`
- `notes/wiki-drafts/new-player-tutorial.md`
- `notes/wiki-drafts/order-of-the-alembic.md`
- `notes/wiki-drafts/rangers-custodians-healers.md`
- `notes/wiki-drafts/society-of-smiths.md`
- `notes/wiki-drafts/thieves-den.md`

## Supplemental date/change screen

- `notes/cc-P136-status-page-self-judging.md`
- `notes/cc-P160-plan-usage-pacing.md`
- `notes/cc-P202-cont-fixup-cont-earned-skill-gain.md`
- `notes/cc-P203-cont-fixup-requisitions-and-leads.md`
- `notes/cc-P209-cont-fixup-port-high-seas-fishing.md`
- `notes/cc-P225-cont-fixup-cont-test-crystal.md`
- `notes/cc-P244-cont-fixup-tinker-golem-watchdog.md`
- `notes/cc-P245-cont-fixup-port-base-items-remainder.md`
- `notes/cc-P271-cont-fixup-port-exodus-encounter.md`
- `notes/cc-P272-cont-fixup-codex-second-agent-codex-review.md`
- `notes/cc-P272-cont-fixup-codex-second-agent.md`
- `notes/cc-P278-cont-fixup-climbing-boots.md`
- `notes/cc-P284-cont-fixup-satchel-icons-ship.md`
- `notes/cc-P285-cont-fixup-levelable-gear-build.md`
- `notes/cc-P354-cont-fixup-port-eodon-remainder.md`
- `notes/cc-P356-cont-fixup-golem-questions-in-console.md`
- `notes/cc-P358-cont-fixup-playtest-bot-checks-second.md`
- `notes/cc-P380-cont-fixup-chopped-tree-stumps-codex-review.md`
- `notes/cc-P380-cont-fixup-chopped-tree-stumps.md`
- `notes/cc-P475-cont-fixup-tutorial-core-trials-playable-codex-review.md`
- `notes/cc-P475-cont-fixup-tutorial-core-trials-playable.md`
- `notes/cc-P80-new-player-tutorial.md`
- `notes/f12-levels-loops-caps.md`
- `notes/map-building-playbook.md`

## Added text-file screen

- `notes/art/cc-P281/proof-log.txt`
- `notes/cc-P216-golem-stage/base-sha256.txt`
- `notes/cc-P237-tools/README.txt`
- `notes/cc-P237-tools/facts.out.txt`
- `notes/cc-P237-tools/validate.out.txt`
- `notes/cc-P239-files/bard-difficulty-spread.txt`
- `notes/cc-P266-tools/README.txt`
- `notes/cc-P266-tools/validate.out.txt`
- `notes/cc-P267-tools/gen.out.txt`
- `notes/cc-P267-tools/render.out.txt`
- `notes/cc-P267-tools/validate.out.txt`
- `notes/cc-P281-tools/README.txt`
- `notes/cc-P281-tools/check.out.txt`
- `notes/cc-P289-tools/playlog-core.txt`
- `notes/cc-P289-tools/playlog-final.txt`
- `notes/cc-P289-tools/playlog-seed.txt`
- `notes/cc-P289-tools/playlog-skip-remedial.txt`
- `notes/cc-P290-tools/playlog-final.txt`
- `notes/cc-P290-tools/playlog-run1.txt`
- `notes/cc-P290-tools/playlog-run2.txt`
- `notes/cc-P291-tools/playlog-alchemy-rerun.txt`
- `notes/cc-P291-tools/playlog-final.txt`
- `notes/cc-P291-tools/playlog-run1.txt`
- `notes/cc-P362-tools/skintable.cs.txt`
- `notes/cc-P480-tools/playlog-final.txt`
- `notes/cc-P480-tools/shots/shots-log-companion.txt`
- `notes/cc-P480-tools/shots/shots-log-core.txt`
- `notes/wiki-drafts/pages/sidebar.txt`
- `notes/wiki-drafts/pages/uo/drafts/levelable_gear.txt`
- `notes/wiki-drafts/pages/uo/drafts/start.txt`
- `notes/wiki-drafts/pages/uo/drafts/tutorial.txt`
- `notes/wiki-drafts/pages/uo/guides/league.txt`
- `notes/wiki-drafts/pages/uo/guides/start.txt`
- `notes/wiki-drafts/pages/uo/professions/bulk_orders.txt`
- `notes/wiki-drafts/pages/uo/professions/climbing_boots.txt`
- `notes/wiki-drafts/pages/uo/professions/start.txt`
- `notes/wiki-drafts/pages/uo/professions/traps.txt`
- `notes/wiki-drafts/pages/uo/start.txt`
- `notes/wiki-drafts/pages/uo/systems/accessories.txt`
- `notes/wiki-drafts/pages/uo/systems/achievements.txt`
- `notes/wiki-drafts/pages/uo/systems/creature_levels.txt`
- `notes/wiki-drafts/pages/uo/systems/league.txt`
- `notes/wiki-drafts/pages/uo/systems/league_register.txt`
- `notes/wiki-drafts/pages/uo/systems/league_shop.txt`
- `notes/wiki-drafts/pages/uo/systems/loot_boxes.txt`
- `notes/wiki-drafts/pages/uo/systems/start.txt`
- `notes/wiki-drafts/pages/uo/world/seasonal.txt`
- `notes/wiki-drafts/pages/uo/world/start.txt`

## Final validation

Final editorial checks passed on both artifacts: unique question IDs, complete six-column rows, one question sentence per row, source-file/line bounds, blocker ordering, no em dashes or trailing whitespace, and sizes below 5 MB. Both repositories pass git diff --check. The code work copy is clean; the notes work copy has only the two requested new Markdown files. Stop-request checks stayed clear through completion. No new tests were required or added.

P532 DONE
