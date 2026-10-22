# P439: Fountain of Youth review

Reviewed 2026-10-22. Notes only; no code changes.

Read both work copies' AGENTS.md, the direction decision and task list, and `notes/cc-P192-cont-fountain-of-youth.md`. No separate P192 Codex review was found beside that note. The findings below do not repeat P192's recorded concerns about repeatable tutorial and trainer rewards, disabled abuse limits, or the Young timer waiting for the next connection.

1. **Bug: a low-skill alternate character bypasses the configured skill limit.** `server/customizations/FountainOfYouth/FountainOfYouth.cs:388` checks only the drinker's skills, while `:469-474` makes every character on the account Young and `:500-511` clears their trainer completion records, so an account with a character above `maxSkillTotal` can receive those benefits by drinking on a new character. Check every character receiving the reset against the configured limit, and add a case with a low-skill drinker and an alternate character above the limit.

2. **Bug: players can drink through walls or from another floor.** `server/customizations/FountainOfYouth/FountainOfYouth.cs:113-114` uses a range check that ignores height, and the speech path at `:346-357` and confirmation at `:425` never check line of sight, so a player near the fountain's X/Y coordinates can drink without reaching its surface. Require visibility and a suitable height difference from a usable component when offering and confirming, with wall and different-floor regression cases.

3. **Bug: an outbound gate permits inbound travel into the sanctum.** `server/customizations/FountainOfYouth/FountainSanctumRegion.cs:57-65` refuses `GateTo` but permits `GateFrom`, so at a spot where the parent region permits gating out, a finder can cast an outbound gate whose other half brings more players directly back beside the fountain without another travel check. Refuse player `GateFrom` in the sanctum, following the existing Burrows rule, and test travel through the resulting gate pair rather than only calling `SpellHelper.CheckTravel`.

4. **Risk: the persistence test does not cover the account reset.** `server/tests/Misc/FountainOfYouthVerification.cs:493-525` reloads only the fountain addon, while Y2 at `:181-209` changes account play time in memory, leaving the saved Young clock, drink cooldown, character flags, tutorial reset, and trainer completion reset untested across a restart. Add a save/load regression covering those records together, then verify the remaining Young time, cooldown refusal from another character, quest availability, and eventual expiry after loading.

5. **Nit: the preservation test never exercises an unrelated quest or stats.** `server/tests/Misc/FountainOfYouthVerification.cs:134-164` names `TheArtOfWar` as `otherQuest` but correctly expects its removal because it is another trainer quest, and the preservation assertions at `:166-171` never inspect stats. Use a completed quest outside `ApprenticeTraining.Areas` and assert it remains completed, and set and verify raw Strength, Dexterity, and Intelligence.

Source evidence for the travel findings:

- `D:/UO/ModernUO-pinned/Projects/Server/Mobiles/Mobile.cs:3076-3080`: `InRange(Point3D, int)` compares X and Y only.
- `D:/UO/ModernUO-pinned/Projects/UOContent/Spells/Seventh/GateTravel.cs:43-47`, `:86-95`: the spell checks the source and destination before creating linked gates in both directions.
- `D:/UO/ModernUO-pinned/Projects/UOContent/Items/Skill Items/Magical/Misc/Moongate.cs:87-123`: using an existing gate moves the player without calling `SpellHelper.CheckTravel`.
- `server/customizations/Regions/OldHavenBurrowsRegion.cs:110-114`: the existing `GateFrom` refusal explains and prevents the same paired-gate route.

Scope and verification: read `FountainOfYouth.cs`, `FountainPool.cs`, `FountainSanctumRegion.cs`, `ClusterFYoungPlayer.cs`, both fountain-related patches, their `apply-patches.sh` registrations, the achievement registration and earned-line tests, and `FountainOfYouthVerification.cs`. Also traced the relevant account, player, quest-context, tutorial, account-persistence, apprentice-training, and Burrows source paths. No direct skill or stat reset was found, and no additional restart defect was established from the source. Account tags and the existing tutorial and quest serializers provide persistence paths, but actual restart behavior remains unverified.

No tests were added or run, as requested for this notes-only review. No game client, throwaway shard, or live service was used, so the listed behavior has not been reproduced in game. Ran `tools/progress.py --dry-run` against these work copies and restored its generated `tools/progress.json` side effect; no progress artifact is part of this review.

P439 DONE
