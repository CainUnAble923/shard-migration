# P622: review findings to fix-up drafts, round 7

October 25, 2026. Notes only. These are unnumbered drafts for the overseer. They do not queue work, authorize implementation, or authorize deployment.

## Result

The new drafts are U1-U7 and W1-W8, listed below. U1-U3 address duplicated fishing supplies, invalid shipping payments, and destructive automatic deed combining alongside Hammer lifecycle defects. U4 protects decision answers and unsaved text. U5-U6 cover recovery across disabled starts and successive saves. U7 addresses the prune's ability to borrow another process's build lock. That lock defect is confirmed in source; actual damage from concurrent pruning is unverified.

The other drafts cover cached payout text, effective extra-slot jewelry bonuses, the Tinker's complete timeout, Music Room commit validation and handoff coverage, tutorial wording/layout, the omitted Corgul book, real-overlay Rootdeep verification, and missing Alembic evidence. A1-A2 extend existing unissued mail/question drafts instead of creating competing owners. C1-C2 retain acquisition dependencies and policy choices. C3 corrects the disputed music-fallback claim and leaves an optional improvement unissued.

No P610-P613 fix is drafted again. Their later reviews identify specific paths or combinations that those implementations left uncovered. Completed implementation or review prompts are distinguished from a completed repair of the newly identified finding.

## Evidence and scope

Read both work-copy AGENTS.md files, the governing document index, direction decision, and task list. Code HEAD is `57924e6c965237f430f5229dd5c454d62b9c0d5c`; notes HEAD is `0ee9aa1fe79e35d56989aa9960a38bc3950d4be1`. Both work copies started clean. These are local source snapshots, not deployed-state claims.

The implementation reviews in range are P587 Hammer, P598 High Seas, P614 decor proof, P615 Tinker, P618 Music Room, P619 tutorial text, and P620 P610 follow-ups. Read each primary report and its adjacent Codex review. Also read the immediate implementation reviews for P587's separate High Seas merge fix-up, P597, P609, and P610. P611-P613 have implementation records but no adjacent Codex-review file in this snapshot; their records were read for deduplication, not treated as independent reviews.

Guides, proposed text passes, designs, stories, release summaries, question sweeps, and play-test plans are not new finding sources in this pass. In particular, P588-P596, P599-P608, P616, and P617 do not generate repair drafts here. P605's design review is excluded by the explicit instruction to skip designs. P596 was consulted only for existing question ownership. P609's implementation note was consulted for its saved-name handoff; its attached review is an input. P610-P613 are also exclusion evidence.

Checked the cited canonical implementations and relevant assertions. The Hammer implementation/test paths inspected have no diff from P587's reviewed `6b74371` to current HEAD. The High Seas customization directory, cooking registrations, and second-half fixture have no diff from P598's reviewed `8b0ccb8` to current HEAD. P618-P620 reviewed this same code HEAD. Read the current external lock, timeout, question, and mail functions for P615 rather than assuming its installed-kit snapshot was immutable. Inspected the saved Alembic JPEG: the popup still obscures west-row decor. No client or animation was run.

Read-only references: ModernUO `d4531cd94b739613155225c234900de9f47d2c88` and ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`. Confirmed `MysticSpellbook` and the source handbook/vendor definitions against those trees. Searches for the seasoning types across canonical customizations, patches, and pinned UOContent found declarations and recipe consumption but no acquisition caller. This establishes a source gap, not the inventory of any saved world. No source under server/uo/ was used.

Paths below use C for `server/customizations/`, T for `server/tests/`, P for `server/patches/`, N for this notes directory, and G for `D:/UO/golem/`. Other code paths are relative to the supplied code work copy. Confirmed means source inspection supports the reported mechanism. Runtime probes described by the reviews remain attributed historical evidence, not P622 results.

## Verdict table

| Finding | Current verdict and evidence | Disposition |
|---|---|---|
| P587 Hammer #1 | Confirmed stale held modifier: C/HammerOfHephaestus.cs:1065 checks exhaustion without checking positive uses; depletion does not trigger exhaustion until another double-click at :1187. The normal alternate-tool exploit proposed in the earlier P372 review is blocked by pinned CheckTool. | U3. Preserve the last legitimate attempt and enforce depletion on actual craft paths. Do not claim the disproved alternate-tool exploit. |
| P587 Hammer #2 | Confirmed stored full-capacity time: ApplyPassiveRegen at :1019 returns while full without resetting its time anchor. | U3, including full-to-partial and partial-interval cases. |
| P587 Hammer #3 | Confirmed destructive automatic selection: C/ClusterFCraftOrder.cs:177 offers every completed small deed to LargeBOD.EndCombine without a remaining-capacity check. | U3. Preserve a small deed that would overfill a partial large line. Manual combine behavior stays outside this repair. |
| P587 Hammer #4 | Confirmed cache dependency: C/Services/BulkOrders/BulkOrderGuildPay.cs:147 reads root holder, membership and payout mode; Refresh at :178 only handles the payout-setting path. | W1, testing the actual cached PropertyList across direct and container transfers. |
| P587 Hammer #5 | Confirmed forbidden property-build mutation: GetProperties at :1233 invokes regeneration, which sets invalidating UsesRemaining at :1028. Pinned Item rejects invalidation during cached-list construction. | U3. Move mutations outside property construction; DEBUG failure and RELEASE diagnostics remain runtime checks for the implementer. |
| P587 Hammer #6 | Coverage gap. The held-bonus factory covers T1/T2; order cases omit failed rolls, recipe transitions, positive colored refunds and mid-run removal. | U3. Mutation-prove the new cases; do not describe the correct paths as reproduced gameplay bugs. |
| P587 High Seas fix-up, attached review #1 | Same pending-hook duplication as P598 #1, still present in Hooks.cs:89-120. | U1, one owner. The two different P587 jobs are not interchangeable. |
| P587 High Seas fix-up, attached review #2 | Same crate-carving/payment defect as P598 #3. | U2, one owner. Retaining both patch blocks did not fix fish-order behavior. |
| P597 attached review | No findings. Its repository-only review explicitly did not inspect the installed scripts. | No merge-repair draft. P615's later installed-script findings are handled separately below. |
| P598 #1 | Confirmed: the hook target uses a captured source without deletion, ownership or remaining-use validation. | U1. |
| P598 #2 | Confirmed: Bait.cs:155 and :177 do not revalidate the captured cup and amount before destination changes. | U1, including prompt and target boundaries and cup-to-cup transfers. |
| P598 #3 | Confirmed: Fish.cs:29 carves crate fish; ShippingCrate.cs:289 ignores ConsumeTotal failure; ProfessionalFisherQuest.cs:173 rewards first. | U2, both carving prevention and independent payment-time content verification. |
| P598 #4 | Confirmed acquisition gap. BuildLines at :116 creates one 5-20-fish line, at most 60 points under PlayerFishingEntry.GetPointsAwarded. Tier 2 starts at 100; the copied ascending tier checks also make tier 4 unreachable. | C1. Galleon progression and the copied tier policy are prerequisites, not a small points rebalance. No new ship-build prompt. |
| P598 #5 | Confirmed: OnTalk's nearest-boat flag is reused for every order; Complete does not validate the recorded boat, cargo or destination response. | U2, including the two-boat and stale-response cases. |
| P598 #6 | Confirmed missing player cancellation. InProgress has only Close; the crate refuses drops; the test calls Delete directly. | U2. Provide an owner-validated player action and preserve the existing resignation rules. |
| P598 #7 | Confirmed false dependency. CorgulTheSoulbinder.cs:122 omits the Mysticism book; pinned MysticSpellbook already supplies its base behavior. | W6. Correct the proposed D-177 premise in new handoff notes, without editing docs/ or rewriting history. |
| P598 #8 | Confirmed missing ingredient acquisition. CookingCraftRegistrations consumes the seasoning types, with no source acquisition caller found in the searched trees. | C2, retaining P269 decision 1 and explicitly adding FreshGinger to its scope. |
| P609 attached implementation review #1 | Source supports clipping risk: TutorialGumps.cs:385 still allocates 300 by 40 pixels without scrolling for the longer pet descriptions. Actual rendering is unverified. | W5. Accommodate the copy and retain client proof as an explicit acceptance check. |
| P610 attached code review #1 | Coverage gap: RootdeepMapSafetyVerification.cs substitutes MapBuilt delegates instead of removing/restoring the real overlay. | W7. Preserve working fail-closed behavior and add the omitted independent verification. |
| P610 attached code review #2 | Confirmed unsaved-text loss: index.html:488 deletes the draft even when typing continued during the request. | U4. |
| P610 attached code review #3 | Confirmed missing effective reader: C/SAAbsorptionAttributes.cs:120 sums direct Mobile.Items only; accepted extra-slot absorption jewelry lives in a container. | W2. Stored property assertions are insufficient. |
| P610 attached notes review #1 | Confirmed stale take/undo identity: tools/decisions.py:547 resolves a positional ID before checking revisions, so equal revisions can target another saved answer. | U4, together with the separate answer/later request problem. |
| P614 #1 | Confirmed evidence gap in N/art/cc-P374/1-alembic.jpg. The saved still obscures west tanks and the reported GIF crop does not complete the requested proof. | W8. No template or animation-code defect is established. |
| P615 #1 | Confirmed lock defect: DockerPrune.ps1:79/:82 omit identity; Golems.ps1:854 renews by owner and :884 releases by owner without session checks. | U7. Revalidate mutable installed source and use fabricated lock state. No actual image-in-use deletion was demonstrated. |
| P615 #2 | Confirmed unbounded tail: TinkerLib.ps1:89-91 waits beyond the initial timed wait for process/output completion. | W3. One deadline must cover process exit, both pipes and bounded cleanup. |
| P615 #3 | Confirmed suppressed-event deletion: TinkerMail.ps1:410-411 consumes immediate-route events after a void sender can suppress them; scheduled briefs require tinkerOnlyMail. | A1, urgent addition to P533 W15's durable-mail owner. |
| P615 #4 | Confirmed missing question content: Round.questions has details, the ledger problem at TinkerLib.ps1:485 is generic, and the brief reads a different question source. | A2, extending P533 W12 with coordinated rendering in W15. Do not create another question lifecycle. |
| P615 #5 | Confirmed mode mismatch: the console trims mailMode, but sender gates compare the untrimmed string. | A1. Use the existing unknown-value default consistently; do not invent a new mail policy. |
| P618 #1 | Confirmed unchecked commit: MusicRoom.commit at web-console/music.py:497 never calls load_notes; an empty browser flush does not protect it or the hourly path. | W4. Validate under the notes lock before either commit route can stage damaged bytes. |
| P618 #2 and attached review #1 | The attached review's correction is supported. Registry lines 11-13 and Add-Track.ps1:78 explicitly define a filename fallback. The supplied britain1 fixture selects that filename as documented; no actual assignment establishes an intended stock-ID fallback. | No confirmed-bug repair. C3 records a possible portability improvement, not a requirement inherited from P456. |
| P618 #3 | Coverage gap: Check at ClusterFShardMusic.cs:592-596 carries fight.Before, but the test only exercises direct Engage takeover. | W4's separate mutation-proven handoff case. No current handoff bug claimed. |
| P619 #1 | Confirmed instruction mismatch with cited client handlers: move hints say click, where readying the move needs double-click. | W5. |
| P619 #2 | Confirmed toggle ambiguity and missing return to peace: hints treat Tab as entering war mode; completion says double-click Rook without leaving combat. | W5, without forcing or changing player key bindings. |
| P619 #3 | Confirmed missing purse location: the revised checklist at TutorialTradeTrials.cs:156 no longer says it is inside the unlocked chest. | W5. |
| P619 #4 | Confirmed incorrect handoff: Seed at TutorialCorePlacement.cs:71-80 skips existing markers/mobiles; constructor names do not update saved objects. | W5 corrects deployment advice and supplies a private-world rename/check handoff. No automatic saved-world rewrite is implied. |
| P620 #1 | Confirmed stale answer/later requests: server.py:535-540 resolves only the positional ID against current questions, not the question displayed by the browser. | U4. This precedes take/undo and is a separate regression case. |
| P620 #2 | Confirmed disabled-start recovery hole: CompanionParty.ReconcileAfterLoad and its OnOwnerLogout helper both return while disabled. Ghost abandonment is not prevented by KeepsLoyalty alone. | U5, enabled save followed by disabled restart for living and ghost companions. |
| P620 #3 | Confirmed compatibility-state loss: MiniChampionSpawn.cs:467 schedules an old-save restart without recording it in MiniChampRestarts. | U6, an intermediate save and second load before the original deadline. |
| P620 #4 | Confirmed set integration gap: SetHelper membership/application/removal and the AOS set-attribute patch still walk direct equipment, excluding accepted extra-slot set jewelry. | W2, distinct from the absorption reader. |

All adjacent reviews of the primary reports except P618's report no additional findings. Their verdicts do not substitute for the implementation evidence above.

## Existing owners and duplicate checks

Searched Markdown prompts recursively in `D:/UO/cc-prompts/queue`, `waiting`, `completed`, `claimed`, `held`, and `merging`. The catalog fingerprint was `a4433a18df13b18e0bb8e09d7c21e5e4475c38547e7abc72898ec6754c71fdb3`. Method: sort relative POSIX paths across those folders lexically; for each path hash its UTF-8 path, NUL, original file bytes, NUL, into one SHA-256. This is a local snapshot. Search hits were checked against actual briefs and the P429/P476/P477/P533/P556/P572/P586 draft ownership, not counted as completed fixes.

The final catalog fingerprint is `9201617c348d4f8d48b4b4af5a8754b34bb31048d28fb89c530be79ef4b98645`. During this task, the overseer reassigned P273 from Codex to Iron and Iron claimed it. The catalog diff from prompts commit `52c2341` to `7849b03` shows that assignment and move, with no new repair brief. Replacing only that file/path with its earlier CRLF work-tree form reproduces the initial fingerprint exactly. The final ownership check found no conflicting new fix prompt. No prompt file was changed by P622.

| Owner | Work that stays there |
|---|---|
| P610 | Its original companion, unravel, tutorial-loan/service, Exodus, Void Pool, Rootdeep, decision, accessory and Underworld changes. U4-U6 and W2/W7 only address the later identified gaps. Do not repeat transfers, ordinary loyalty protection, account-bound loans, existing archive joins, locked-slot removal or the first pending-restart store. |
| P611 | Hunter's Satchel admission, the launcher preparation changes, and P556 A1's bonded-corpse/exact-approval checks. None is redrafted. Its unbuilt Civic Contracts policy remains with P556 U1 and earlier question IDs. |
| P612 | No new implementation; P452 remains waiting and populated, with the Appraiser scope and access handoff retained. Its status is not proof P452 was built. |
| P613 | Failed bandage delivery and active orphan tutorial adoption. W5 changes surrounding instructions/layout and the saved-name advice only. No second bandage/recovery draft. |
| P476 U3 | Gravewater chance rolls, trap geography, sea-champion skull/lottery behavior, Charybdis teleport persistence and their original tests. U1/U2 concern supplies and order transactions; C1 is acquisition, not another P476 fishing bundle. |
| P476 W5 plus P610 A1 | Original Underworld/mini-champion fixes. P610 built the repeat guesses, controller-disable distinction, key cleanup and gem cancellation. U6 adds only the newly exposed compatibility-save interval. Remove completed portions before issuing the remaining P476 work. |
| P533 W12/W15 | Existing Tinker repair/question lifecycle and durable-mail work. Add A1-A2 below. P479/P597 are completed original implementation/merge verification, not repairs of P615's findings. |
| P478 | Wiki catch-up and integration of verified final wording, including tutorial names and real High Seas acquisition limitations. No new guide-writing prompt. |
| P481 and waiting P436 | Start-area design and chosen guild/League visual treatment. W5 fixes the existing tutorial pet layout; W8 completes existing proof. Neither builds a new start island or chooses the guild visual direction. |
| P623 | Queued play-test-plan writing for P374/P456/P609/P610. Coordinate eventual plan references; it neither fixes these implementations nor executes the missing proof. |
| P586 W1-W5; P533's other unissued sections; P556/P572 | Existing nonurgent tests, Artificers text, progression/policy and other drafts. P610-P613 implemented urgent scopes only. This pass does not rediscover and issue all the remaining older work. |
| P533 W24 | Every repeated progress.py dry-run write report. No new reporter repair draft. |

P610's in-passing Void Pool/top-20, deleted-controller, driver-text and cap-coverage notes and P597's soak-size/stale-fact notes are implementation handoffs, outside this reviews-only finding pass. They are not marked fixed or silently replaced. P584 is outside the requested numeric interval. No new builder, vendor, ship or art-generation task is inferred from the skipped guides/designs.

## Common instructions for issuing these drafts

Replace P?? consistently before issuing. Read both work-copy AGENTS.md files and recheck current code and prompt ownership. The existing no-Haven, no-deployment, no-live-account/save operations, no docs/ edits, no agent Git mutations, and file-size rules apply. Keep canonical ModernUO layering; read-only reference trees stay read only. Document alternatives before any upstream patch. Shared-kit work needs an explicitly writable kit work copy and a separate owner before issuance; the external G paths here are read-only evidence for P622.

Every new regression must be seen failing first. For a confirmed defect, use the original implementation; for coverage of working behavior, use the named temporary mutation, then restore it. Record both results and restore all mutations before the final gate. Run PowerShell scripts and tests with Windows PowerShell 5.1 (`powershell.exe`). Run server changes through `docker/uo/build.sh -t sl-modernuo:cc-P??`, with its test gate. Use fabricated stores, fake transports and disposable loopback-only fixtures. Large scratch fixtures must be ignored and proven with git check-ignore. No real locks, SMTP, pruning or remote calls are needed for these regressions.

For player-visible fixes, add a plain Fixed changelog line without exploit instructions. Coverage alone does not warrant a gameplay-fix claim. Report source, automated tests, private-world/client proof and deployed state separately. No historical build or review probe is a new test result.

## Urgent drafts

### U1. Fishing hooks and bait can only be spent once

```text
# CC task P??: High Seas supply follow-up: validate hook and bait sources at every delayed action
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P598 #1-#2 and the P587 High Seas attached review identify stale-source duplication. Fix the delayed source checks without changing reward rates or acquisition.

1. In Hooks.cs, validate a live source with positive uses still in the actor's backpack before returning the previous pole hook or changing any pole field. Spend the source once. Preserve existing target/tool access rules.
2. In Bait.cs, validate the source after the amount prompt and again at target resolution. Require a positive requested amount within the cup's current supply and current backpack ownership. Reject a stale amount without changing source, target, hue, enhanced state or charges. Use the same rule for poles, lobster traps and cup transfers.
3. Red-first regressions through real prompt/target callbacks: A opens a cursor, transfers the source to B, B spends or combines it, A finishes the old cursor. Cover a deleted source, a live transferred source, reduced charges, zero/negative requests and an ordinary successful application. For hooks, start with an existing pole hook and assert no replacement hook was issued on rejection. For bait, cover both equipment kinds and cup-to-cup movement.
4. Assert total item/charge conservation, not just that the source was deleted. Repeated or overlapping cursors must not spend it twice. Keep legitimate hook swapping, original pole hue and ordinary bait combining intact.
5. Compare the inherited ServUO omission and explain why duplication is a broken result to fix. Run focused High Seas fixtures and the normal build gate. Notes: notes/cc-P??-high-seas-supply-validation.md, with red/green evidence and no claim about current player exploitation. End P?? DONE.

**Done means:** a consumed, moved or depleted source cannot supply another target through an old prompt or cursor; valid supply still works once.
```

### U2. Shipping orders validate cargo and destination before payment and expose cancellation

```text
# CC task P??: fishing-order follow-up: actual fish, the recorded boat and a usable cancel action
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P598 #3/#5/#6 and the P587 High Seas attached review identify payment without cargo, remote delivery and inaccessible resignation. Keep points, reward odds and the standalone order framework unchanged.

1. Restore the source ShippingCrate carving restriction in BaseHighseasFish.Carve. Independently preflight every required line against actual crate contents at delivery, consume the validated fish successfully, then grant reputation and rewards exactly once. A shortage must pay nothing and must not partly consume otherwise valid lines. Do not trust cached OrderHave alone.
2. Validate the order's recorded live boat, hold and crate at its destination on the correct map. Another owned boat at that port cannot substitute. Recheck the actor, ownership, actual destination monger and local interaction range on the gump response, including movement or boat/cargo changes after opening it. Carry sufficient destination context to do this; Complete(player, order) alone currently lacks it.
3. Add Cancel Order to the existing player order window or crate menu, with confirmation and ownership/state checks on response. Follow the existing source resignation penalties once, delete the crate through that action, and leave unrelated cargo intact. Preserve the existing distinction for completed orders; do not invent a fresh completed-order penalty. Keep cancellation usable when the player no longer wants the order, rather than requiring staff deletion.
4. Red-first player-path cases: carve credited fish then try delivery; force a content shortage independently of the carve guard; a multi-line shortage leaves all lines/payment unchanged; a filled boat A stays at departure while boat B is at delivery; wrong facet and a stale completion window; successful local delivery and repeated response. Assert exact reward/reputation and fish/steak outcomes.
5. Replace the direct-Delete-only cancellation proof with the actual player action. Cover cancel, confirmation refusal, repeated confirmation, and a different actor. Assert one appropriate penalty, no reward and release of the unwanted hold crate. Keep normal dry-docking rules untouched.
6. Run focused fishing-order/High Seas tests and the normal build gate. Coordinate edits with U1 and retain P476 U3's separate scope. Notes: notes/cc-P??-fishing-order-transactions.md, including inherited-source comparison and runtime limits. End P?? DONE.

**Done means:** missing fish or a remote recorded boat cannot earn payment, and an owner can actually abandon an unfinished order through the player UI.
```

### U3. Hammer charge state, regeneration and automatic deed use agree with actual crafting

```text
# CC task P??: Hammer follow-up: depletion, capped regeneration, safe automatic combines and real order coverage
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P587 Hammer #1/#2/#3/#5/#6. Automatic combining can destroy excess small-deed value; charge state also remains stale or mutates inside property construction. Preserve the accepted T3 values and Craft This Order behavior.

1. Immediately reconcile exhaustion and remove the held modifier when a real successful or failed attempt spends the last use. The final permitted attempt uses the intended pre-depletion skill. Require positive uses when applying/restoring the modifier and when actual crafting validates the tool, including a retained craft gump. Pinned DefBlacksmithy accepts zero uses, so double-click checks alone are insufficient. Do not claim ordinary alternate-tool use bypasses CheckTool.
2. Stop banking regeneration time while full. Start the missing-charge interval at the full-to-partial transition, preserve an earned partial interval while below full, and discard surplus intervals on reaching the cap. Preserve existing capacities, intervals, familiarity, restore charges and save compatibility. Review T1/T2's same pattern alongside T3; repair the shared defect consistently without changing tier balance.
3. Move regeneration/exhaustion mutations out of GetProperties. A suitable timer or action path must make progress without needing a tooltip to mutate state. Cached PropertyList construction reads only. Reconcile equipped empty hammers after load before applying their modifiers; no preparatory double-click is allowed in the regression.
4. Before automatically combining a completed small smith deed, verify its whole amount fits the matching large line's remaining capacity and that it otherwise matches. Preserve an overlarge small deed and craft only the shortfall. Example: 8/10 gorgets plus a completed 10/10 small deed must leave that small deed intact and finish with two newly crafted items. Preserve the accepted sequence of fitting small deeds before new crafts. Manual combining is separate scope.
5. Red-first actual successful and failed last-use cases; stale craft-window rejection at zero; equipped empty save/load; full idle for several intervals then one use spent; partial regeneration and cap overflow; due regeneration followed by a real cached PropertyList read. Check uses, exhaustion, effective Blacksmithy, hue and time anchoring. Prove the property read neither throws nor changes charge state; cover release diagnostics if the build configuration uses them.
6. Extend held-bonus lifecycle selection to all three tiers: equip/remove, re-equip, held load, restoration and regeneration. Verify an Ancient Smithy Hammer with a backpack T3 contributes only the held tool's modifier, then move T3 into hand and check the transition.
7. Add the remaining order coverage: a genuinely failed roll loses the proper materials and one use, refunds no ingots, advances no deed, then can continue to success; a large order crafts more than one unfinished recipe; a colored deed including a post-Valorite metal completes using that material with a positive familiar-metal refund; deed and hammer removal during an active run stop later attempts. A successful normal item rejected by an exceptional deed is not a failed-roll fixture.
8. Mutation-prove coverage of correct paths by disabling the recipe transition, misselecting/refunding the material, or bypassing the relevant mid-run stop one at a time. Restore each mutation. Use deterministic clock/RNG seams scoped to tests and restore global state. Run focused craft/BOD fixtures and the normal build gate. Notes: notes/cc-P??-hammer-charge-order-followup.md. End P?? DONE.

**Done means:** real crafting respects exhaustion immediately, full time cannot fund later charges, cached properties are read-only, automatic combines preserve excess small deeds, and the newly covered order transitions fail under their targeted mutations.
```

### U4. Decision requests carry the identity the user actually saw

```text
# CC task P??: decisions follow-up: displayed identity on answer, later, take and undo; preserve edits during saves
**Model:** Opus
**Touches:** migration tools, docker/test-queue
**Agent:** Codex OK
**Summary:** P610's attached reviews and P620 #1 expose request-time identity and draft-loss gaps left after the saved-answer join fix. Preserve the existing archives, escaping and stored answers.

1. Carry the displayed question identity/version on answer and Ask me later requests, rather than resolving a positional ID and assuming it is what the page displayed. Check that expectation before mutation. Editing an existing answer also carries its stable answer key and expected revision. A changed or ambiguous question must be refused without saving against another card.
2. Bind take and undo expectations to the saved answer's stable key as well as revision/status/takenInto. Validate under the answer-store lock. Positional display numbers may change; equal revisions or equal destination prompts must not allow an old request to mutate a different answer. Update copy/export, CLI expectation builders and browser callers together.
3. Track the submitted draft version. A successful save clears only that version if no later edit superseded it. Typing while a save is pending, including typing back to empty, must survive refresh under the stable question key. Preserve drafts on errors, stale responses, filter changes and other cards' saves. Keep explicit Discard working.
4. Red-first endpoint tests through the actual loopback queue service: load old page state, insert/reorder/reword source questions, then send answer and later requests from that state. Include an unchanged question as a positive control. Two answered cards with equal revisions must reject stale take and undo expectations after reordering. Rejected batches change nothing.
5. Actual local DOM/browser regression: submit text, hold the response, type newer text, then complete the request and reload. Assert the newer draft survives and the stored answer remains the submitted version until another save. Include choice buttons, a second card's save, cleared text and an error response. Do not replace this with source-string inspection.
6. Use fabricated notes/data and no real decision records. Run focused Python identity/revision/service tests and the browser check. Record any preexisting real-data failures separately. Document that server, page and tools need a coordinated later release; do not deploy. Notes: notes/cc-P??-decision-request-identity.md. End P?? DONE.

**Done means:** a stale page cannot answer, defer, take or undo another question's answer, and a save response cannot erase text typed after submission.
```

### U5. Existing companions recover across a disabled restart

```text
# CC task P??: companion recovery follow-up: enabled save followed by a disabled start
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P620 #2 finds that ReconcileAfterLoad and OnOwnerLogout both skip recovery while disabled. Existing ghost companions can then reach the abandoned-ghost sweep.

1. Recover existing owned in-world companions for offline owners independently of CompanionSettings.Enabled. Factor or adjust the internalization helper as well as the caller; removing only the outer return is insufficient. Keep enablement restrictions on new companion activity and retain released, deleted, online-owner and roomed exclusions.
2. Red-first living and ghost fixtures saved while enabled with owner/companion in the world, then loaded while disabled and owner offline. Use the real after-load path and abandonment/loyalty sweep. Assert away/stabled/internal state, survival past BondingAbandonDelay, unchanged owner/bond/equipment and one recovery at login.
3. Repeated reconciliation and login must be idempotent and must not duplicate followers or revive a ghost. Include a roomed companion and a released creature as negatives. Preserve the already working disabled-login recovery for companions saved away.
4. Run focused companion lifecycle tests and the normal build gate. No saved-player survey or repair is authorized. Notes: notes/cc-P??-companion-disabled-restart.md, distinguishing synthetic persistence proof from live-world state. End P?? DONE.

**Done means:** disabling the system between an enabled save and restart cannot strand or expose an owned ghost to abandonment removal.
```

### U6. An old-save mini-champion restart survives the next save too

```text
# CC task P??: mini-champion compatibility follow-up: persist the inherited pending restart immediately
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P620 #3 finds a second-load hole in the pre-store compatibility branch, not a failure of the already fixed disabled-controller distinction.

1. Whenever ResumeAfterLoad schedules the compatibility restart for a save without MiniChampRestarts, persist the same deadline through the normal pending-restart path. Keep one timer, cancellation, manual Start/Stop and deletion cleanup coherent. Do not assign new restarts to controllers intentionally disabled in saves that already have the store.
2. Red-first fixture: load an old controller save without the store; let the real deferred load callback schedule its timer; advance partway; save both controller and store; clear process-local state; reload before the deadline. Assert one restart at the original deadline, not no restart or a newly extended delay.
3. Separate cancellation branch: Stop or delete the controller during that inherited interval, then save/load and prove no restart. Retain the existing first-load compatibility and deliberately disabled-controller cases. Read serialization sentinels and restore test clock/store state.
4. Run focused Underworld/mini-champion persistence tests and the normal build gate. Do not rebuild P610's other A1 fixes or rewrite real world saves. Notes: notes/cc-P??-mini-champion-second-load.md. End P?? DONE.

**Done means:** a compatibility restart remains pending through an intermediate save, at its original due time, and cancellation remains durable.
```

### U7. Pruning owns its own build lease

```text
# CC task P??: Docker prune coordination follow-up: explicit identity and process-owned build leases
**Model:** Opus
**Touches:** Golem kit tooling and tests
**Golem:** home
**Agent:** Codex OK
**Summary:** P615 #1 shows that a prune can renew and release a builder's docker-build lock by sharing its inferred Golem owner. No actual removal of an in-use image was proved.

1. Re-read the installed DockerPrune, Use-GolemLock, golem and Golems functions and record their hashes. Work in the assigned writable kit copy. Give take and release an explicit prune identity independent of GOLEM_NAME, current directory or the registry's home Golem.
2. Bind renewal and release to the acquiring process/session or an unguessable returned lease token, not just the Golem name. Carry the same lease through the wrapper subprocesses and finally block. A second prune with the same identity must also wait rather than borrow the first prune's lease. Preserve atomic acquisition, expiry, legitimate renewal and existing builder callers; document compatibility for older lock records.
3. Red-first tests using the real lock logic with a synthetic lock directory: a builder session holds the resource, a pruner inherits its GOLEM_NAME, and acquisition must wait/refuse without changing the builder's record. Releasing a non-owned lease must leave it intact. Cover same-name different-session contention and stale release after a new lease acquires the resource.
4. Test Invoke-DockerPrune through the actual lock adapter, with Docker execution stubbed. Lock refusal makes zero prune calls; success releases only its own lease, including on exceptions. Do not substitute a Boolean-only lock hook for the collision regression. Keep container image-ID, latest and good-tag protections unchanged.
5. Run focused kit lock/prune facts and affected existing callers under Windows PowerShell 5.1. No real locks, Docker pruning, builds, remote calls or service restarts. Notes: notes/cc-P??-prune-owned-lease.md, with red/green proof, source hashes and unverified real concurrency clearly stated. End P?? DONE.

**Done means:** no independently running builder or pruner can have its lease renewed or released by this prune merely because the Golem name matches.
```

## Other drafts

### W1. Cached deed tooltips follow holder and guild changes

```text
# CC task P??: BOD payout-text follow-up: invalidate cached properties when the root holder or membership changes
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P587 Hammer #4. Payout calculation and gump text are already fresh; the real cached property list has untracked holder/membership dependencies.

1. Make deed payout property text refresh after direct transfer, transfer of an enclosing container, and relevant guild join/leave, as well as payout-mode changes. Cover bank/backpack movement where the quote's holder rule changes. Use narrow hooks or dependency invalidation, documenting alternatives before any upstream patch. Avoid a global property rebuild on every tick.
2. Red-first: build deed.PropertyList for a member on Always bank, transfer it to a member on Always cash out, then read the same cached path and verify the new quote. Include non-member-to-member, join/leave and nested-container transfer. Assert the old cached line is gone and the resulting line matches the real turn-in quote.
3. Do not replace the cache access with GetProperties(new ObjectPropertyList(...)); that bypasses the defect. Preserve reward amounts, membership gates and manual combine behavior. Run BOD/guild-payout tests and the normal build gate. Notes: notes/cc-P??-bod-holder-property-cache.md. End P?? DONE.

**Done means:** a cached tooltip cannot continue describing the previous holder or membership after a supported transition.
```

### W2. Active extra jewelry contributes absorption and complete-set bonuses exactly once

```text
# CC task P??: accessory follow-up: effective absorption and set activation in extra slots
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P610's attached absorption finding and P620 #4. KindOf now accepts these jewels, but their effective readers and set lifecycle still omit active container pieces.

1. Include active extra-slot IAbsorptionItem jewelry in SAAbsorptionAttributes.GetValue exactly once. Preserve direct equipment and exclude locked/inactive/stored items. Test the wearer's effective reader and delayed Damage Eater behavior, not just the bracelet's stored property. Damage Eater is a delayed heal; do not assert immediate damage reduction.
2. Give SetHelper membership, AddSetBonus, RemoveSetBonus and effective AOS set-attribute aggregation one consistent view of actually worn direct and active extra-slot pieces. Keep last-piece semantics, stat/skill bonus cleanup and appearance coherent. Avoid double enumeration, duplicate bonuses or counting inactive pieces after a rank/settings change.
3. Red-first BraceletOfPrimalConsumption in an unlocked extra bracelet slot contributes its eater through the real reader; locking/removing it removes that contribution. Compare paperdoll and extra-slot paths and a delayed-heal outcome with a controlled clock/damage fixture.
4. Red-first Luck-set case: ordinary bracelet on the paperdoll, Etoile Bleue as the ring, Novo Bleue in the active extra bracelet slot. Test both equip orders and the relevant effective Luck/regen/casting values, moving between paperdoll/container, removing either piece, locking/reopening the slot and repeated refresh. Bonuses appear once and disappear completely when the set is incomplete. Retain stock paperdoll-set controls.
5. Document patch alternatives, run focused accessory/set/absorption fixtures and the normal build gate. Do not rebuild P610's accepted equip validation, slot recovery or ordinary custom-imbue integration. Notes: notes/cc-P??-accessory-effective-set-absorption.md. End P?? DONE.

**Done means:** qualifying active extra jewels have the same effective absorption/set contribution as worn pieces, once, and inactive ones contribute none.
```

### W3. The Tinker's deadline includes output collection

```text
# CC task P??: Tinker timeout follow-up: bound inherited output handles and descendant cleanup
**Model:** Opus
**Touches:** Golem kit tooling and tests
**Golem:** home
**Agent:** Codex OK
**Summary:** P615 #2. The timed parent wait does not bound the later WaitForExit/output tasks, so a child retaining a pipe can keep the wrapper blocked.

1. Apply one elapsed-time deadline across process exit, stdout, stderr and cleanup. An exited parent with open inherited pipes must time out. Do not add an unlimited drain or another full wait after the deadline. Preserve useful completed output and accurate Code/TimedOut results.
2. Establish process containment that can close/terminate owned descendants even after the original parent exits. Disposal and cancellation must not block past the documented bounded cleanup allowance. Avoid killing unrelated processes or relying only on taskkill against a parent PID that no longer exists.
3. Red-first local fixture under Windows PowerShell 5.1: a parent exits promptly while its child keeps stdout open beyond a short limit. Repeat for stderr and both pipes, plus an ordinary successful child and a genuinely hung parent. Assert total wrapper elapsed time, TimedOut and that no fixture descendant is left running. Use only local processes with no network traffic.
4. Exercise local-script, SSH and SCP adapters using local executable substitutes; no actual SSH/SCP connection. Run focused Tinker timeout facts. Notes: notes/cc-P??-tinker-output-deadline.md with original failure, final elapsed bounds, source hashes and cleanup proof. End P?? DONE.

**Done means:** inherited pipe handles cannot extend a call indefinitely after the configured process limit.
```

### W4. Music Room validates commit snapshots and tests the watch handoff

```text
# CC task P??: Music follow-up: reject invalid notes at commit and protect the watch's remembered town track
**Model:** Opus
**Touches:** web-console, server tests
**Golem:** any
**Summary:** P618 #1/#3. Save to repo and hourly commits bypass notes validation; the correct Check handoff has no independent regression. The filename fallback is not a confirmed defect and is outside this task.

1. Validate the current notes file in the shared MusicRoom.commit path before button or hourly commit can stage it. Hold the notes lock across validation and the protected commit snapshot, using a consistent lock order with the repo lock. Return the notes error without touching invalid bytes or reporting success. Existing save_note validation alone is insufficient.
2. Red-first tests: load a modified file containing {"tracks": []}, make no track edit, then invoke Save to repo through its route and the hourly caller. Neither reaches a Git mutation and both report the schema error. Include malformed JSON/read errors, missing-file semantics and valid pending notes. Stub all Git mutation; do not create real commits. Exercise the browser's empty-flush case and a concurrent save versus snapshot deterministically.
3. Add a separate server regression through Check: enter a mapped town; leave another mapped live creature as combatant while a boss is watched; delete the boss without a death event setting EndedAt; move to the default region and let Check hand off. End the replacement fight, wait ReturnDelay, and assert the original town track returns.
4. Temporarily remove only fight.Before from Check's Engage call. Watch the new handoff regression fail, restore it, then pass. Keep the direct-Engage test. No production handoff change is needed unless a new defect is reproduced.
5. Run focused Music Room/browser checks and ShardMusic tests, with the normal server build gate for changed C# tests. No Haven, real notes, Git commits or audible-playback claim. Notes: notes/cc-P??-music-commit-handoff.md. End P?? DONE.

**Done means:** both commit routes refuse invalid notes without a preceding edit, and loss of Check's remembered-music argument is caught by a failing test.
```

### W5. Tutorial instructions and layout support the actions they describe

```text
# CC task P??: tutorial text follow-up: double-click moves, conditional war mode, the purse and readable pet choices
**Model:** Opus
**Touches:** server, handoff notes
**Golem:** any
**Summary:** P619 #1-#4 and P609's attached clipping finding. Apply narrow instruction/layout corrections; preserve lesson evidence, eligibility, rewards and P613's delivery/recovery behavior.

1. Say double-click Honorable Execution and Focus Attack to ready the moves. Explain turning war mode on only if it is off, with Tab described as the default switch rather than an unconditional Enter combat command. Account for hold-to-use/custom bindings without changing settings. Tell combat students to return to peace before double-clicking Rook.
2. Restore the stealing sequence: open the unlocked wooden chest, empty both hands, use Stealing on the purse inside. Keep Skills-window guidance and distinguish the practice person's separate trinket.
3. Increase the pet-description space and row/panel layout, or use another readable layout, so every offered description including the fox growth sentence is visible and Choose buttons remain accessible. Do not truncate the approved copy or hide growth requirements to make it fit.
4. Red-first existing tutorial text/layout assertions for the missing action/location distinctions, then verify the corrected compiled gumps. Layout assertions should check actual gump geometry/available content; source constants alone do not prove wrapping. On a disposable loopback test world, capture the pet-choice window and walk the move/war-peace/purse sequence in the supported client. Record rendering/interaction as unverified if it cannot actually be checked, not as a passed source test.
5. Correct P609's saved-name handoff in a new note: reseeding only fills missing objects and does not rename an existing TutorialDeathEcho or station marker. Give staff an explicit per-object rename or deliberate replacement checklist for the private test copy and verify displayed names afterward. No automatic broad rename, deletion/reseed of the real world, or save migration belongs to this wording task. If an automatic name upgrade is later preferred, scope it separately to known old defaults with red-first persistence tests.
6. Run relevant tutorial suites and the normal build gate. Supply final wording and the saved-name caveat to P478's existing integration owner without writing another guide. Notes: notes/cc-P??-tutorial-instructions-layout.md. End P?? DONE.

**Done means:** the instructions identify the required clicks, mode and purse, pet text fits, and the handoff no longer promises that reseeding renames saved objects.
```

### W6. Restore Corgul's Mysticism handbook using the existing ModernUO base

```text
# CC task P??: Corgul loot follow-up: port the omitted Mysticism handbook onto MysticSpellbook
**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P598 #7 disproves the missing-base premise. MysticSpellbook already has the Mystic type, offset 677 and 16 spells; no new spellbook subsystem is needed.

1. Port CorgulsHandbookOnMysticism additively under the High Seas artifact path, deriving from pinned MysticSpellbook. Preserve ServUO's label 1149779, hue 1159, RegenMana 3, DefendChance 5, LowerManaCost 10 and LowerRegCost 20, with ModernUO serialization and collision checks.
2. Restore it alongside CorgulsEnchantedSash and CorgulsHandbookOnTheUndead in UniqueList without changing the guaranteed unique award count or selection rules. Review the existing MISSING cleanup-table row for the artifact and restore its source integration/value where appropriate; do not silently change the other artifacts' rates.
3. First update the existing two-entry unique-list expectation so it fails against the current incomplete roster. Use name/type resolution for a missing-type assertion if needed so the old implementation can run the regression. After porting, verify the full roster, book attributes/type and ordinary Corgul award path. Run focused artifact/High Seas checks and the normal build gate. No unrelated subsystem tests are required for a leaf item.
4. Remove false missing-MysticBook comments in changed current source. Put a correction to proposed D-177's book omission and the old missing-base claim in the new handoff note for the overseer, preserving its unrelated aura/boat limitations. Do not edit docs/ or rewrite the original reports.
5. This does not build the Corgul island, altar, boat warp or player access chain. Notes: notes/cc-P??-corgul-mysticism-book.md, with source comparison and acquisition limits. End P?? DONE.

**Done means:** the existing boss can award the faithful Mysticism handbook, and no documentation handoff still attributes that omission to a nonexistent base-class gap.
```

### W7. Rootdeep safety is verified with the actual overlay absent and restored

```text
# CC task P??: Rootdeep safety coverage follow-up: real overlay files and saved entrance state
**Model:** Opus
**Touches:** server tests, private local test tooling
**Golem:** any
**Summary:** P610's attached review finds omitted U7 acceptance evidence. The delegate-based unit test is useful but cannot prove real map detection at startup.

1. Build an isolated loopback startup fixture using copied saved entrance state and the actual server map-overlay loading route. Remove/restore only the fixture's overlay files between fresh starts. Keep the production MapBuilt detector active; do not replace it with a constant delegate or edit the real shard's map/save directories.
2. With the overlay absent, saved active downward entries are disabled, the upward route remains available, and a player cannot enter void terrain. With it restored, only entries disabled for map absence reopen; a staff-disabled entry stays off. Assert state and a real entry movement/teleport result after each startup, plus the intended inside-character reporting without forced relocation.
3. See the new check fail first with the relevant startup safety hook or real readiness detection deliberately bypassed in a disposable build; restore the code and prove both missing/restored runs pass. Retain existing focused unit tests and the Young warning test.
4. Use ignored, size-checked scratch fixtures and the normal gated build. Report exact overlay files/loading route and startup logs. No stricter client-map installation policy, whole-shard startup refusal, live overlay edits or deployment. Notes: notes/cc-P??-rootdeep-real-overlay-proof.md. End P?? DONE.

**Done means:** independent real-file startup evidence catches removal of Rootdeep's safety integration and proves recovery when the files return.
```

### W8. Complete the Alembic tank evidence

```text
# CC task P??: guild hall proof follow-up: unobscured Alembic tanks and a complete west-row animation capture
**Model:** Opus
**Touches:** notes evidence, private local proof tooling if needed
**Golem:** home
**Summary:** P614 #1 finds incomplete retained proof, not an established decor/client defect. Keep P374's working animation patch and templates unchanged unless fresh evidence proves a separate fault.

1. Use P374's private loopback test-copy setup, compatible patched client and scratch save. Dismiss login, changelog and achievement windows before capturing. Do not use the actual shard or live account and do not connect to Haven.
2. Save a clear still showing all eight tanks and their full supports. Capture a sufficiently wide animation or a separate west-row view showing complete tanks/supports through a full animation cycle. Check every retained frame/crop for occlusion before declaring the proof complete. Placement logs alone do not establish appearance or movement.
3. Keep images/animations below 5 MB each and link the exact files in a new proof note. State which visible tanks moved and how the capture covers their supports; describe the earlier still/crop limitation accurately. Do not claim the earlier image showed all decor or that a partial burst proves a complete cycle.
4. No new automated test is needed for a capture-only repair. If tooling changes, run its appropriate existing local checks; any new test must fail first. Notes: notes/cc-P??-alembic-west-row-proof.md. End P?? DONE.

**Done means:** the committed proof visibly covers every tank/support and the missing west-row animation, without changing templates or asserting an unproved client bug.
```

## Additions to existing drafts

### A1. Extend P533 W15 with suppressed-event durability and one mailMode interpretation

P615 #3 overlaps W15's existing durable-queue/sender-result ownership. Treat its acceptance additions as urgent because the current briefs path deletes news without sending or holding it. Add these cases to W15 before issuance; do not issue a second mail-queue rewrite:

1. Have the sender distinguish sent, suppressed/held and failed. A mail round acknowledges/deletes only sent events or an explicitly documented discard policy. In briefs mode, replies and direct-routing fallback events must reach durable held storage and the next successful brief even with `tinkerOnlyMail=false`. Failed or suppressed brief sends must not archive events as delivered or advance the sent-slot marker. Keep new events arriving during a send for the next batch.
2. P615 #5 adds shared mode normalization for the console, Tinker sender, Golem direct sender and outbox fallback. Trim and normalize case once, with the existing missing/unknown-value fallback to `all`; keep `off` meaning no transport and `briefs` meaning scheduled briefs only. Preserve events rather than treating suppression as SMTP success. Do not silently choose a different unknown-value policy from the existing console fact.
3. Red-first full mail-round cases: a reply in briefs mode; a finish fallback with tinkerOnlyMail false in briefs mode; scheduled brief failure/retry; off with no transport; surrounding whitespace and uppercase, missing and unknown settings. Assert durable event state and exact sender calls, not just outbox creation or a generic subject. Use fake settings roots and fake transport under Windows PowerShell 5.1. No actual email, credentials, task changes or remote calls.

Record P615 attribution and the installed-source hashes in W15's eventual note. Coordinate any question rendering with A2 below, retain W15's redaction/diagnostic requirements, and keep P476 W18's Away-mail scope with its existing owner.

### A2. Extend P533 W12's question lifecycle with complete brief content

P615 #4 does not need another question subsystem. W12 already calls for Questions.ps1 and the normal answer lifecycle. Ensure its Tinker question representation carries cause, proposed action and choices, including questions with no prompt. W15's brief renderer must read that canonical representation or an equivalent durable complete record, rather than only the generic ledger problem subject. Coordinate the producer/renderer change as one acceptance dependency.

Add a red-first full-question-to-brief fact: a fabricated Copper question asks about a failing disk check, proposes retrying it, and offers retry/wait. The brief must contain the cause, proposed action, choices and existing answer location exactly once, without an additional generic problem line. Repeat on a later round while still open. Preserve day/Golem/prompt deduplication; do not restore the old changing-cause mail key. Keep answerable desktop/web behavior with W12 and P187's existing twin rule. Use stubs only. This extends W12/W15, whose original unbuilt requirements remain intact.

## For Chase and the overseer

These are proposed future scope decisions, not questions that block completion of this unattended synthesis. Earlier settled decisions are not reopened.

| ID | Finding, recommendation and existing owner | Consequence |
|---|---|---|
| C1 | P598 #4: retain faithful classic-boat limits until P268's ship scope has an approved, obtainable multi-line boat route. P532 S004/S005 already own naval scope and galleon acquisition. Separately choose whether to correct the explicitly copied ascending reward-tier bug or define another earned Charybdis-bait route. Recommend a narrowly documented tier correction when the progression prerequisite is built, with original points thresholds and reward odds. | No reputation-as-order-points substitution, free hooks, tier rebalance or implicit galleon build. Until earned acquisition is proven, keep hooks/Oracle/Charybdis bait and the resulting summoning chain labeled unavailable through current ordinary orders. A future test must earn them from an available boat/order chain, not construct them directly. |
| C2 | P598 #8 extends P269 decision 1, which already asks who sells pie seasonings. Recommend the original Sea Market tavern-keeper stock for MentoSeasoning, SamuelsSecretSauce and DarkTruffle, plus source baker/farmer FreshGinger stock. Verify the actual market/vendor footprint before choosing placement; no invented cheaper/general-vendor substitute. | After that scope is chosen, a bounded vendor-content prompt should test ordinary purchase and recipe-gated pie crafting with no staff-created ingredients. Until then, describe ingredient acquisition as missing. Charybdis loot does not supply a usable general workaround while C1's summoning chain is unavailable. No vendor placement or service change is authorized here. |
| C3 | P618 #2 is not a demonstrated filename-interface bug. Recommend retaining the documented basename format until actual assignments show a need for per-install stock-slot preservation. Stock-ID resolution with that installation's loop flag could be proposed later as a portability feature. P532 U96 retains track/area selection. | No corrective launcher or registry-format prompt from this fixture. If the improvement is chosen later, define migration/compatibility and test a stock slot whose filename differs from the enum name. Do not label the current britain1 behavior a confirmed wrong-track defect. |

P596's reconciliation already says Hammer findings are repairs/tests, not a new T3 approval. Preserve manual deed-combine behavior. Saved-name verification and unobscured screenshots are operational proof, not votes on a new template or client fix.

## Input inventory

Finding inputs read, relative to notes/:

```text
cc-P587-review-hammer-t3.md
cc-P587-review-hammer-t3-codex-review.md
cc-P587-cont-fixup-high-seas-fishing-second-half-codex-review.md
cc-P597-cont-fixup-tinker-docker-prune-codex-review.md
cc-P598-review-high-seas-second-half.md
cc-P598-review-high-seas-second-half-codex-review.md
cc-P609-apply-tutorial-text-pass-codex-review.md
cc-P610-fix-drafts-from-p533-codex-review.md
cc-P614-review-guild-hall-decor-proof.md
cc-P614-review-guild-hall-decor-proof-codex-review.md
cc-P615-review-tinker-fixes-p479.md
cc-P615-review-tinker-fixes-p479-codex-review.md
cc-P618-review-music-room-fixes.md
cc-P618-review-music-room-fixes-codex-review.md
cc-P619-review-tutorial-text-applied.md
cc-P619-review-tutorial-text-applied-codex-review.md
cc-P620-review-fix-drafts-p533.md
cc-P620-review-fix-drafts-p533-codex-review.md
```

Implementation/exclusion support in the requested range:

```text
cc-P587-cont-fixup-high-seas-fishing-second-half.md
cc-P596-questions-for-chase-3.md
cc-P597-cont-fixup-tinker-docker-prune.md
cc-P609-apply-tutorial-text.md
cc-P610-fix-drafts-from-p533.md
cc-P611-fix-drafts-from-p556.md
cc-P612-fix-drafts-from-p572.md
cc-P613-fix-drafts-from-p586.md
```

Earlier synthesis ownership was read from cc-P429-crystal-codex-findings-to-fixes.md, cc-P476-crystal-codex-findings-round-2.md, cc-P477-crystal-review-10-23-merges.md and the P533/P556/P572/P586 findings-to-fixes reports. P586's work record supplied the dual-filename deliverable convention. P269 supplied its existing acquisition decisions and copied-tier rationale. P532/P574/P596 supplied existing question IDs. Relevant current prompt briefs are named in the ownership table; P456's actual fallback requirement was checked against the registry interface.

## Verification and limits

Lane tests: none. No executable test or gate was added; P622 therefore has no red/green cycle. Every regression and mutation above is future work. No server build, runtime reproduction, gameplay test, browser test, cold world restart, map-file removal, mail send, lock acquisition, Docker operation, client launch or animation capture was performed. Source confirmation does not establish deployed prevalence or current saved-world contents.

Only this report and [the wrapper work record](cc-P622-codex-findings-to-fix-drafts-7.md) are intended changes. No code, guide, prompt, configuration, service or docs/ file changed. No Haven connection, deployment, account operation, commit, merge, push or branch switch occurred. Final editorial/scope checks and progress-reporter handling are recorded in the work record.

P622 DONE
