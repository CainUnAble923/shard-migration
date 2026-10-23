# P491: Underworld mini champions, second review

Reviewed 2026-10-23. Notes only; no code changed.

Read both work copies' AGENTS.md, direction-decision.md, tasks.md, the P197 implementation note, and both P445 review notes. The findings below do not repeat P445. All `server/` paths refer to the code work copy. The read-only ModernUO tree's HEAD matches the Dockerfile pin, `d4531cd94b739613155225c234900de9f47d2c88`.

## Findings

1. **bug** - `server/customizations/Services/Underworld/PuzzleRoom/MastermindPuzzleItem.cs:57`, through `D:/UO/ModernUO-pinned/Projects/UOContent/Engines/Khaldun/PuzzleChest.cs:344`: A player's second incorrect mastermind guess calls `Dictionary.Add` for the same player again and throws `ArgumentException` instead of recording the new guess and returning feedback. Patch the base to replace that player's entry, as ServUO does, and cover two consecutive wrong guesses on the same board.

2. **bug** - `server/customizations/Services/MiniChampionSystem/MiniChampionSpawn.cs:236`, `:444`: Setting Active to false during the completion cooldown leaves the scheduled restart running because Stop returns immediately for an inactive controller, and a controller explicitly disabled before a save also starts again after loading and waiting RestartDelay because every saved inactive controller schedules Start. Cancel pending restarts even when already inactive, persist whether a completion restart is actually pending, and test both disabling during cooldown and loading an explicitly disabled controller.

3. **bug** - `server/customizations/Services/Underworld/PuzzleRoom/MagicKey.cs:102`: Expiring or consuming the magic key removes puzzle keys and boards only from the backpack's top level, so putting them in a nested bag preserves progress that the next visit's recursive key searches still accept, until the preserved items' own lifespans expire. Remove the matching session items recursively and cover a nested gold key and board when the magic key expires or is consumed on success.

4. **risk** - `server/customizations/Services/Underworld/ExperimentalRoom/ExperimentalGem.cs:168`, `:177`, `:408`: Deleting an activated gem before its five-second startup callback runs leaves that callback queued, which then starts a repeating timer for the deleted gem; the timer checks only for null and can keep ticking indefinitely. Retain and cancel the startup callback on deletion, guard delayed callbacks and timer ticks against Deleted or inactive gems, and cover deletion between Activate and BeginRoom_Callback.

## Evidence and limits

- Finding 1 is a ModernUO base-class defect reached by this port. `PuzzleChest.cs:334` uses the same player as the dictionary key for every submission, while `D:/UO/ServUO-pub57/Scripts/Services/Khaldun/PuzzleChest.cs:364` assigns through the indexer. The shard's `server/patches/PuzzleChest-trap-training-kit.patch` changes the damage hook and exposes the gump but does not change this insertion. `server/tests/Items/Functional/TrapTrainingKitVerification.cs:306` submits one wrong cylinder guess followed by a correct one, so it does not exercise the duplicate insertion.
- Finding 2 is inherited broken behavior. ServUO's `Scripts/Services/MiniChampionSystem/MiniChampionSpawn.cs:450` also schedules a restart for every inactive controller on load. The port's completion path schedules Start after Stop, while its Active setter calls that same Stop for an explicit administrative shutdown; the saved active flag cannot distinguish those cases.
- Finding 3 is also inherited broken behavior: ServUO's `Scripts/Services/Underworld/PuzzleRoom/MagicKey.cs:77` takes the same shallow snapshot. The port's `PuzzleBox.cs:46` and `:74` use recursive searches, whose default is verified in `D:/UO/ModernUO-pinned/Projects/Server/Items/Container.cs:903` and `:947`; `MastermindPuzzleItem.cs:108` consumes the magic key through the same Decay path on success. The preserved keys still have their own expiration timers, so this finding does not claim unlimited retention.
- Finding 4 retains ServUO's delayed startup and null-only timer check in `Scripts/Services/Underworld/ExperimentalRoom/ExperimentalGem.cs:134`, `:143`, and `:405`. The port stops only the already-created room timer in OnDelete at line 380; its base class's OnAfterDelete stops a separate lifespan timer, not the queued startup callback.

Reviewed the canonical MiniChampionSystem and Underworld files listed by P197, InvisibleTile.cs, NavreyNightEyes.cs, the relevant base classes and patch, and the existing creature and trap training tests. The Navrey cases in `server/tests/Mobiles/Bosses/CC6Batch8Verification.cs` cover her values, serialization, drops, and independent stock spawner; the Renowned cases in `server/tests/Mobiles/Normal/CC6Batch5CreatureVerification.cs` cover creatures and rewards. No direct controller or Underworld puzzle tests were found, as P197 and P445 already report; that general gap is not a new finding here.

These are source-based findings. Runtime reproduction, save/load behavior in a running host, client behavior, and actual world placement remain unverified. No build or behavioral tests were run and no tests were added for this notes-only review. No additional finding was established in the maze reward arithmetic or the teleporter placement after tracing the called hooks.

Ran the progress reporter with the work-copy paths and --dry-run, suppressing its unconditional progress.json write in memory to keep this note the only deliverable. No Haven connection, deployment, code edit, docs/ edit, branch change, commit, merge, or push was made.

P491 DONE
