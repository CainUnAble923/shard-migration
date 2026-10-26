# P655: player guide draft for weapon milestones and archery buttes

Prepared October 26, 2026. Documentation only. Deliverable: [weapon-procs-buttes.md](wiki-drafts/weapon-procs-buttes.md).

The guide describes the merged source, including P647 fixes, and distinguishes test-only proc behavior, existing stock butte scoring, and the unbuilt scoring-butte gameplay. It makes no deployment claim. Code snapshot: `e4c2dd9f987534cd1775f7471cc2c0d6e3a359d0`. Notes snapshot before this task: `7cfd6696638269d8f0af12b98c2b8d658304a8a1`. Pinned ModernUO source is the read-only `D:/UO/ModernUO-pinned` tree, matching Docker's `d4531cd94b739613155225c234900de9f47d2c88` pin.

## Sources read

Read both work-copy AGENTS.md files first, then `docs/direction-decision.md`, the task list's working instructions, and `docs/README.md`. No `docs/` file was changed. Paths below beginning `server/`, `docker/`, or `player-package/` are in the code work copy; note links are in this repository. Pinned paths are relative to `D:/UO/ModernUO-pinned`.

Build, design, and review evidence:

- [P632 build](cc-P632-build-scoring-buttes.md): BUTTE-A art-only delivery and the remaining component, recipes, placement, and client-proof stages.
- [P633 build](cc-P633-build-procs-milestone.md): implemented purchase/combat slice, defaults, red/green evidence, and deferred dormancy, shared budget, combat coverage, and client/world acceptance.
- [P569 design](cc-P569-design-procs-levelable-milestone.md): player experience, proposed full release rules, attunement, budget, dispatch, persistence, and ordered follow-ups.
- [P571 design](cc-P571-design-butte-and-deed.md): stock firing/scoring numbers and proposed hit-display component, loan guards, deeds, acquisition, public yard, and acceptance stages.
- [P633 inline review](cc-P633-build-procs-milestone-codex-review.md), [P644 butte review](cc-P644-review-build-scoring-buttes.md), and [P645 proc review](cc-P645-review-build-procs-milestone.md): earlier findings checked against current source rather than repeated as current defects.
- [P647 fixes](cc-P647-fix-weekend-review-findings.md): test-world enforcement, connected tooltip, quoted confirmation terms, damage-immunity guard, bound-effect status, cooldown cleanup/persistence coverage, and butte mapping/record test improvements.

Canonical implementation read:

| File and location | Evidence used |
| --- | --- |
| `server/customizations/LevelGear/LevelGearProcs.cs:37` | Test-world-only effective enablement; default level 100, cost 100, chance 500/10000, cooldown 10 seconds, companion owner range 18, and raw damage 12 for each named choice |
| Same file, `:275`, `:333` | Living player, possession, levelable crafted weapon, no artifact, one purchase, item-level/point/slot validation and deduction |
| Same file, `:354`, `:435`, `:444`, `:462` | Damaging-strike hook, equipped/current weapon, player or companion owner, wild primary target, range/LOS/legal harm and CanBeDamaged checks, shared owner and weapon timers, fixed-element AOS call |
| Same file, `:151`, `:477`, `:492` | Absolute saved cooldowns, stable public tooltip, temporary GM switch and rejection off the test world |
| `server/customizations/LevelGear/LevelGearMilestoneGump.cs:32`, `:127` | Choice page, bound status, owner-only cooldown display, confirmation, saved price/unlock quote, revalidation and changed-terms refusal |
| `server/customizations/LevelGear/LevelGearGump.cs:44` | Milestone row appears while enabled or after purchase, including below the purchase threshold |
| `server/customizations/LevelGear/ClusterFLevelGear.cs:39`, `:206`, `:275`, `:365`, `:412`, `:608`, `:747`, `:771` | Default progression, versioned purchase row, crafted sealing, XP/point arithmetic, one milestone slot, tooltip call and ItemLevel possession/target flow |
| `server/customizations/LevelGear/SmithsSealDeed.cs:1`, `:31` | Staff-only acquisition comment, backpack use, eligible target and consumption only on success |
| `server/customizations/Imbuing/ImbuingTable.cs:110` | Default five base slots |
| `server/customizations/ArtificersImbueGump.cs:799`, `:1016`, `:1804` | Stored-property counting remains separate from level purchases and the milestone |
| `server/patches/BaseWeapon-level-gear-proc-hit.patch:1`; `docker/uo/apply-patches.sh:885` | Proc dispatch after native hit effects, inside positive-damage branch, before creature and special-move callbacks; patch registration |
| `server/customizations/Items/Addons/ScoringArcheryButteArt.cs:18`; `server/customizations/ShatteredRunestone.cs:70` | Display enum, picture mapping and tiledata application only; no interactive scoring component |
| `server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:186` | Stock ArcheryButteDeed reward at 80,000 cleanup points |
| `server/customizations/ClusterFSkillGain.cs:320` | No Archery practice-window extension in TryRow |
| `server/customizations/Tutorial/TutorialWingTrials.cs:43`, `:352`, `:634` | Current loan/trial code and echo damage completion path kept separate from stock butte scoring; no new butte completion integration |

Pinned engine read:

- `Projects/UOContent/Items/Addons/ArcheryButteAddon.cs`, complete file: 2-second target-wide delay; east/south axis checks; exactly 5 or 6 tiles; backpack ammo consumption; skill window -25 to 25; conditional ring thresholds and split scores; stored ammo recovery; per-shooter scores cleared by gathering; saved ammo fields and unsaved score/LastUse state. No new display callback or close-click reset is present.
- `Projects/UOContent/Skills/SkillCheck.cs:43`: effective skill at or above max succeeds without the challenge/gain roll.
- `Projects/UOContent/Items/Weapons/Ranged/BaseRanged.cs:105` and `Projects/UOContent/Items/Weapons/Throwing/BaseThrown.cs:113`: ranged and thrown OnHit delegate to the shared base path. This is source reachability, not a new runtime pass.
- `Projects/UOContent/Misc/AOS.cs:47`, `:234`: normal elemental damage entry, leech interaction and Mobile.Damage call. Fixed raw damage is not a guarantee of final hit-point loss.

Focused source checks also located current regression methods in `server/tests/Misc/LevelGearProcVerification.cs` and `server/tests/Items/ScoringArcheryButteArtVerification.cs`. Existing test names and historical build reports were consulted; no test was run or added by P655.

## Code versus design and older notes

1. **Butte gameplay is unbuilt.** P571 describes the complete target, house deeds, Carpentry rows, New Haven placement, tutorial-loan refusals, gather/reset visuals, and ammo-before-chop behavior. P632 explicitly delivers artwork only. A read-only search of canonical customizations and patches found only the art table and its application call, no scoring component, scoring deeds, recipe registration, placement command, or practice-display hook. The guide supplies current stock practice instructions without presenting proposed craft requirements or yard coordinates as usable instructions.
2. **Stock rules and proposed new guards differ.** The pinned stock Gather path has no P571-style local living-player, map, LOS, or active-trial guard. Close-click gathering requires stored ammo; a miss-only session cannot use the proposed empty-ammo reset. The guide does not attribute these future protections or reset behavior to existing buttes. Gathering clears all scores, and does not reset LastUse.
3. **Dormancy is absent.** P569 requires the shared real player-level/acting-level service and dormant procs below the saved threshold. P633 deliberately omits that dependency. Current OnWeaponHit does not compare player level, Arms Lore, acting level, or even the saved required level; the item threshold is enforced at purchase. The saved requirement is history and a future integration input. No loop-reset reactivation promise is made.
4. **Only the gear side reserves the slot.** Current SlotsUsed includes the milestone, even if disabled. Imbuing still uses CountActiveProperties independently. P569's shared union accounting, intensity reservation, and intensityCost setting are not implemented. The guide records this limit rather than claiming both menus enforce the same budget.
5. **The entry is visible before 100.** P633's plain-language summary suggests the button appears at 100. Current LevelGearGump shows it on levelable weapons while the feature is on, before unlock; the purchase validator supplies the level refusal. A bound choice keeps the entry visible while disabled.
6. **P647 supersedes the old proc review defects.** Current effective Enabled requires a test world, direct enabling refuses elsewhere, the tooltip is called, changed price/unlock terms require reconfirmation, targets must pass CanBeDamaged, bound pages show unavailable status, and cooldown pruning exists. These are verified in current source, not assumed from P647's summary alone. The page reports only the viewer's owner timer, so it can say ready while a transferred weapon's timer still blocks use; the guide explains both timers.
7. **Published art and installed gameplay are distinct.** P632 has no package publication or installed-client proof. P647 improves regression checks without adding butte gameplay. The guide does not claim the pictures are visible in a current player install or that the new range exists in a running world.

Arithmetic independently recomputed from current defaults: `((100 + 1) * 10)^2 - 100 = 1,020,000` cumulative XP; `90 * 4 + 10 * 8 = 440` earned points before spending. These are item progression defaults, not a time-to-level estimate or deployment observation. All score and chance values in the guide were checked against the actual pinned Fire implementation.

The Smith's Seal's staff-only source statement was checked against canonical customization/patch references: only its own item implementation names SmithsSealDeed, with no normal vendor, drop, reward, or recipe reference found. This is a source finding, not an inspection of existing world inventories.

## Verification and limits

No server/client/package build, test-world start, world command, account access, live configuration inspection, map walk, or full world save/restart was performed. The guide is a source-based draft. Broader ranged/thrown/special-move runtime behavior, actual UI rendering and visuals, lifecycle persistence, combat balance, installed player-package state, art distribution permission, and actual server deployment remain unverified here. Historical P632/P633/P647 test results are not claimed as fresh passes.

Ran the required `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE set to these work copies; exit 0. Its incidental tools/progress.json write was suppressed in memory by intercepting only that destination's Path.write_text, leaving generated files untouched. No inventory totals from that reporter are used as feature evidence.

No code changed, no new tests, and lane tests are none. Document checks passed under Windows PowerShell 5.1.26100.9711: strict UTF-8 decoding, no em dashes or replacement characters, no trailing whitespace, both requested files below 5 MB, and independently recomputed progression arithmetic. Local Markdown links resolve. Both repositories passed `git diff --check`; the untracked documents were checked directly as well. The code work copy is clean, and only the requested guide and this note were added in the notes work copy.

No Haven connection, deployment, service action, commit, merge, push, branch switch, or `docs/` edit. Stop-request checks between steps found no request.

P655 DONE
