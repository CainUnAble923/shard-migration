# Codex review: P678

CC task P678: New Haven moves into the author's Haven, and Rootdeep's way in (SoS swap S7). Reviewed by Codex (`codex exec review`, read-only) after P678 DONE and before the Golem's commit, 2026-10-28 00:53.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.92). Most relocation work is implemented, but the animal wing lesson remains at the obsolete farm instead of moving with New Haven. Build and live-client proofs were not independently rerun during this review.

- **medium** [P2] Move the animal wing trial along with the other trials (`server\customizations\Tutorial\TutorialTradeTrials.cs:40`)
  The animal lesson still uses `FarmField = (3390,2606)` and `GoatSpot = (3395,2606)`: starting `animals.taming` directs players to the old farm and creates its goat there, outside the new town. `TutorialFarm.SeedHaven` also still places the old farm layout there, although the housing tour now uses the new farmhouse. Complete the requested wing-trial relocation by moving the animal lesson to the new town and updating or retiring its old farm-prop seeder.

(3.1 minutes, 2,264,651 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The four Python tests pass against the Iron shard checkout, but the new combined-layout proof omits shipped blockers and verifies planned rather than implemented NPC positions. Required live proofs also remain explicitly outstanding; this review does not establish correctness of the separate code-repository changes.

- **medium** [P2] Keep completion pending until the required play proofs exist (`notes\cc-P678-new-haven-moves.md:237`)
  The notes explicitly leave the server-side P289 route, Rootdeep walk into the Landing, and TazUO screenshots undone, although task section 6 requires them. The offline route stops at the hatch and cannot establish the complete requested journey. Record these as outstanding gated work rather than declaring the task finished; [AGENTS.md:44???46](../../AGENTS.md#L44-L46) specifically prohibits the completion marker before work is finished because it triggers Golem action.
- **medium** [P2] Validate NPC homes against the actual seeder definitions (`notes\cc-P678-tools\crosscheck.py:38`)
  NPC positions come exclusively from the checked-in planning CSV, rather than the selected shard checkout. Consequently, an omitted or incorrect edit in `ClusterFNewHavenSeeder`, `GuildLocations`, `Appraiser`, or `ClusterFInstitutionSeeder` still passes this proof: it checks the intended position instead of the position players receive. Read the implemented coordinates or assert that every CSV row matches its corresponding source entry before checking reachability and collisions.
- **medium** [P2] Apply custom tiledata before selecting blocking props (`notes\cc-P678-tools\crosscheck.py:68`)
  The whole-town proof uses pristine client tiledata, omitting custom-art blockers defined in the package's `records.json`. Verified examples include `market-fruit`, `healer-rail-1`, and `bank-tree`: applying the shipped records increases the blocking-prop count from 36 to 76. Load those overrides before filtering and surveying movement, as `art_validate.py` already does; otherwise the new test does not exercise its promised combined seasonal layout.

(1.7 minutes, 750,026 tokens)
