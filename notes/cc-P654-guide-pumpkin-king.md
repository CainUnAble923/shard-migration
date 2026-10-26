# P654: Pumpkin King player guide draft

Written October 26, 2026. Docs-only work. Draft: [wiki-drafts/pumpkin-king.md](wiki-drafts/pumpkin-king.md).

## Scope and source snapshots

The guide describes the checked merged implementation, including P624's PK1 work. It does not describe PK2-PK5 as finished. The existing [Sorcerer's Dungeon draft](wiki-drafts/sorcerers-dungeon.md) was read for context and left unchanged. No code, configuration, docs/, service inventory, or published wiki changed.

- Code work copy HEAD: `e4c2dd9f987534cd1775f7471cc2c0d6e3a359d0`.
- Notes work copy HEAD before this task: `2f77cabeaeed0f5d8da8c67503bf6f3cde145aa8`.
- Latest commit touching the canonical event directory: `feadac2`, P624's implementation. Later merged work has not completed the deferred event stages in these files.

Read both work-copy AGENTS.md files, docs/direction-decision.md, and the opening working-agreement/task sections of docs/tasks.md. Canonical code was read from server/customizations/, never server/uo/. `rg` was unavailable; source discovery used git ls-files, git grep, and PowerShell Select-String.

Below, `event/` means `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/` in the code work copy. `pinned/` means the read-only `D:/UO/ModernUO-pinned/` tree. Line numbers refer to the checked sources.

## Notes and design sources read

- [P564 design](cc-P564-design-pumpkin-king.md), including its player flow, numbers, remaining-stage specifications, and acceptance limits.
- [P624 build notes](cc-P624-build-pumpkin-king.md) and [inline review](cc-P624-build-pumpkin-king-codex-review.md).
- [P636 review](cc-P636-review-build-pumpkin-king.md) and [its inline review](cc-P636-review-build-pumpkin-king-codex-review.md).
- [P647 fixes note](cc-P647-fix-weekend-review-findings.md), checked for later event work. Its claim that no P636 note exists is stale relative to this work copy: P636 and its review are present. Current event source, rather than that claim, determines the cleanup limits below.
- [Existing player draft](wiki-drafts/sorcerers-dungeon.md).

## Code evidence for the guide

| Guide subject | Files and implementation read |
| --- | --- |
| Annual window and time zone | `server/customizations/ClusterFHalloweenDecorSeeder.cs:34` defines 10-24 and 11-02. `event/Generate.cs:55` borrows those dates. `server/customizations/ClusterFSeasonalSwitch.cs` implements inclusive dates, local time, world-load/hourly checks, and seasonal-transition-only automatic changes. `docker/uo/.env.example:21`, `docker/uo/docker-compose.test.yml:57`, and the retired live compose file default TZ to America/Chicago. These are source defaults, not inspected live settings. |
| Entrance and Researcher | `pinned/Distribution/Data/regions.json:3323` lists Ilshenar entrance 546,455,0. `event/Generate.cs:40` places the Researcher at 536,456,-53; its Dressing table supplies the entrance pumpkins and scarecrows. `event/SorcerersDungeonResearcher.cs` supplies the visible trader label, context-menu text, redemption, and reward menu. |
| Shared rotation | `event/Spawner.cs`, especially OnTick, Reset, OnCreatureDeath, and CreateEntries: nine entries, each with 80 tracked deaths and 15 regular spawns; 3-8 second regular-spawn delay; 1-3 minute room transition; survivors and hatchlings are owned separately from progression. The guide does not promise a fixed completion time or maximum total dungeon population. |
| Boss hit points | Constructor SetHits calls in `event/Creatures/AbominableSnowman.cs:31`, `GarishGingerman.cs:28`, `HeadlessElf.cs:30`, `JackInTheBox.cs:33`, `NightmareFairy.cs:28`, `RabidReindeer.cs:27`, `StockingSerpent.cs:28`, and `TwistedHolidayTree.cs:28` each set 8,000; `JackThePumpkinKing.cs:50` sets 26,000. These are the complete nine files behind the guide's boss table. |
| Jack and carving | Read `event/Creatures/JackThePumpkinKing.cs` in full: resistances and skills, OnDamage retaliation, 5% delayed throw, placement, 5-10 second hatch, twelve-entry undead selection, and 30% carving for 25-100 gold. `event/Spawner.cs` MayThrowPumpkins and MayPlacePumpkin add active-encounter and region checks. The retaliation number is a raw physical roll, not percentage reflection or guaranteed final damage. |
| Award eligibility and chance | `event/SorcerersDungeonData.cs:85` and its death snapshot, death hook, ProcessKill, and persistence code: living players with looting rights, victim death region, controlled/summoned exclusions, per-player Fame/Luck tally, chance after the increment, backpack/bank/ground fallback, and reset only on award. `server/customizations/Services/PointsSystems/PointsSystem.cs` keys spendable points by PlayerMobile. |
| Award identity and pool | Read `event/EnchantedOriginArtifacts.cs`: saved registration, name/hue application, the two-argument loot selector, and existing Minax property application calls. Read `pinned/Projects/UOContent/Misc/Loot.cs:668` selector body: ML, Tokuno, AOS, and ordinary branches, with no SA branch. No complete OSI reforging or equipment-pool equivalence is claimed. |
| Turn-in and purchase | Read `server/customizations/Mobiles/NPCs/BaseTurnInMobile.cs`: top-level backpack scan, two-tile context entries, five-tile reward double-click, immediate consume-on-selection, and one point per item. Read `server/customizations/Gumps/BaseRewardGump.cs`: selection affordability, confirmation, backpack-only delivery, and deduction after delivery. `event/SorcerersDungeonRewards.cs` provides the catalog and inherits that callback. |
| Reward prices and behavior | Read `event/SorcerersDungeonRewards.cs` and all four event item files: `Items/EscapingAndSterlingRewards.cs`, `Items/JacksBagOfTricks.cs`, `Items/JackInTheBox.cs`, and `Items/ShackledHeartOfThePumpkinKing.cs`. The complete seven-row catalog is reproduced in the guide. Read `server/customizations/Items/Functional/SerpentsJawbone.cs` for house placement, range, destinations, and travel checks. |
| Shutdown and redemption | `event/Generate.cs` Down and Remove; `event/Spawner.cs` Deactivate, ownership, and version-zero load behavior; `event/SorcerersDungeonResearcher.cs` has no season gate for turn-in/rewards. Points, tally, and artifact persistence contain no season-expiration action. |
| Spell-summon exception | Rechecked P636 against Spawner.Deactivate and the ownership registration paths. Read `pinned/Projects/UOContent/Mobiles/AI/MageAI.cs:252`, `Spells/Necromancy/VengefulSpirit.cs:41`, and `Mobiles/Monsters/AOS/Revenant.cs:60` onward. Vengeful Spirit can create an unregistered Revenant; its lifetime/target checks do not depend on the caster remaining alive. The guide does not promise all combat ends at shutdown. |

## Code and design differences, and unfinished work

1. **Only PK1 is implemented by P624.** P564 describes later purchase safeguards, a ring confirmation guard, expanded SA equipment selection, timed-reward coverage, client acceptance, and optional titles. P624 explicitly defers those stages; current event code agrees. The guide retains current prices and behavior and labels the equipment expansion and confirmation safeguards unfinished.
2. **Reward confirmations remain unchecked at final debit.** `SorcerersDungeonRewardGump` overrides GetPoints and RemovePoints, not OnConfirmed. The inherited callback delivers before calling the void RemovePoints override, which discards DeductPoints' bool result. It does not implement P564's checked debit/delivery/refund transaction. The guide advises completing one confirmation at a time and makes no overspend-prevention claim. A full backpack does delete the undelivered reward without a debit in this implementation.
3. **The ring is intended as a permanent choice, but its final callback does not enforce the unset slot.** Double-click checks HasSkillBonus; the WarningGump callback only checks deletion and possession. A pending choice can overwrite an earlier choice. The guide says there is no normal reset option and advises finishing one choice at a time, without advertising a guaranteed one-time guard.
4. **Artifact authenticity is registration only.** P564's text describes the registry plus hue/name checks. Actual IsEnchantedOrigin only checks non-null, non-deleted membership in the saved registry. Mark applies hue/name when possible, but those are not redemption conditions. The guide says unrelated renamed or dyed items do not qualify, without telling players an authentic item must retain its hue/name.
5. **The SA branch and death-context factory changes are pending.** ProcessKill uses captured death context for eligibility but still calls CreateForKill with the deleted creature; the factory reads its region/map and calls the pinned two-argument selector. It is not the complete source equipment pool. Existing Minax property generation remains the documented approximation, not full ServUO reforging.
6. **Shutdown is narrower than the design's complete-combat promise.** PK1 removes owned regulars, bosses, pumpkins, and hatchlings. P636's missing Revenant ownership is still present. Version-zero saves also cannot reconstruct already-forgotten earlier-room survivors or old pumpkin hatchlings. No broad cleanup sweep exists. The guide warns that enemies may remain without presenting staff repair instructions as player steps.
7. **October-only bag behavior is intentional.** The event's November 1-2 window does not extend bag use. The saved NextUse is per bag and advances by a full day after an item is produced. The bag's fallback is the ground, not the bank.
8. **Three title deeds remain omitted.** The catalog has no Hero of the Unloved, Savior of the Demented, or Slayer of the Pumpkin King deed. None is a direct Jack kill award. Winter-themed bosses are already part of this Halloween rotation.
9. **The guide is authorized separately from client acceptance.** P564/P624 propose writing a guide after later acceptance work. P654 explicitly requests a source-based draft now. This task produces that draft and preserves the unverified status instead of claiming acceptance was completed.

## Verification and limits

No lane tests were requested, added, or run. No build, server, client, Docker operation, Haven connection, deployment, save/account action, Git commit, push, merge, or branch change was performed. P624's test/build results are prior evidence, not independently rerun results. Guide numbers were checked against the source tables and formulas; current public OSI behavior was not researched.

Live event availability, deployed version, settings/time zone, entrance travel, client art/localization, real-map placement, full server reload, and exploit behavior in a running shard remain unverified. This is an unpublished draft. Source comments and prior notes are not treated as observations of the running shard.

Document review confirmed the boss and reward tables against their source entries and recalculated the three chance examples from the code constants. Both new Markdown files have valid local links, no em dashes, no trailing whitespace, a final newline, and sizes below 5 MB. Windows PowerShell reported version 5.1.26100.9711. No new tests or test gates were created, so no red/green cycle applies to this writing task.

Ran the required progress calculation with SL_SHARD and SL_MIGRATE pointing to these work copies, using --dry-run and an in-memory Path.write_text replacement. The tool still attempts to write tools/progress.json during --dry-run; that generated write was discarded. The calculation completed successfully without changing README, progress artifacts, or any other file.

Final scope review found only the two requested new Markdown files in the notes repository; the code work copy remained clean. Stop-request checks between work steps were clear.

P654 DONE
