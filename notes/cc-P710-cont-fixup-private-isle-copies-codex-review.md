# Codex review: P710

CC task P710: fix-up for P664 (CC task P664: Private copies of the isle (P481 F4)): its branch did n. Reviewed by Codex (`codex exec review`, read-only) after P710 DONE and before the Golem's commit, 2026-10-27 15:41.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The conflict resolutions preserve both sides, but the newly integrated copy manager has actionable queue, seeding-failure and pet-deletion defects. The reported successful build was not independently rerun during this read-only review.

- **medium** [P2] Protect controlled animals in the seeded-entity deletion pass (`server\customizations\Tutorial\TutorialCopies.cs:288`)
  If a trainee tames one of the initially spawned pen animals and it is still on the copy when reset runs, this deletes the pet before the later controlled-pet rescue branch can move it home. `Seed` records all initially spawned mobiles in `Placed`, including those tameable animals. Apply the controlled-pet protection before deleting recorded entities as well as during the stray sweep.
- **medium** [P2] Reject copy assignment when its seeder refuses (`server\customizations\Tutorial\TutorialCopies.cs:325`)
  `SeedCopy` can return a refusal from `TutorialCorePlacement.SeedOn` (for example, when an isle tile fails its fit check), but this method ignores that result and subsequently marks the slot seeded. `Claim` then assigns the copy and moves the trainee onto an isle without its lesson NPCs, props or exit gate; subsequent claims do not retry seeding. Propagate seeding success and leave refused copies unseeded and unassigned.
- **medium** [P2] Restore waiting trainees after an offline queue removal (`server\customizations\Tutorial\TutorialCopies.cs:258`)
  If a waiting trainee disconnects before a copy becomes available, this removes their queue entry without assigning them a copy. On their next login they remain on map 32: `TutorialCopies.OnLogin` only handles private-copy maps, and the consumed start choice does not enqueue them again. Preserve offline entries or explicitly re-enqueue waiting trainees at login so they are not stranded on the shared beach.

(1.2 minutes, 390,872 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.9). No actionable defects were found in this repository???s changes. The new note records the conflict resolutions, combined test run and remaining client verification; the code-repository merge and reported build results were not independently verified in this review.

No findings.

(0.3 minutes, 93,199 tokens)
