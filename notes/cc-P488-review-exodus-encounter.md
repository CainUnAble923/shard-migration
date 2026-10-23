# P488: Exodus encounter code review

Reviewed 2026-10-23. Notes only; no code changes.

Read both work copies' AGENTS.md, the direction decision and task list, P271's merge note, P195's implementation note, and P379's review of the merge. The findings below exclude the deviations and merge issues those notes already describe.

Paths below are relative to the code work copy unless marked ServUO or pinned. ServUO means `D:/UO/ServUO-pub57/Scripts/`; pinned means `D:/UO/ModernUO-pinned/Projects/`. The pinned checkout reports commit `d4531cd94b739613155225c234900de9f47d2c88`.

## Findings

1. **bug** | `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Region.cs:140`, `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/VerLorRegController.cs:129`: Saving after Exodus dies and restarting before the ten-minute exit completes leaves the saved controller stopped with no boss, while the region's unsaved exit timer disappears, so the encounter never restarts without staff intervention. Save the exit deadline and restore its warning, evacuation, and restart after world load, with a test that reloads during both exit phases; this is an inherited ServUO defect, not a newly introduced difference.

2. **bug** | `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Loot/Asclepius.cs:27`, `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Loot/GargishAsclepius.cs:27`: Both staves display the bandage healing bonus, but the port omitted ServUO's bandage consumer, so equipping either staff gives no such bonus. Add the held-staff check to the bandage healing calculation, preserving the shard's skill scaling, and test healing with each staff and without one; ServUO `Items/Resource/Bandage.cs:495` adds 15 to effective healing, while pinned `UOContent/Items/Skill Items/Misc/Bandage.cs:375` and the shard's Bandage patches do not.

3. **bug** | `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusChest.cs:244`: A revealed chest that is still locked when saved survives a restart with no deletion timer, remains visible indefinitely, and occupies its spawner slot instead of expiring and allowing a fresh hidden chest. Persist and resume the reveal expiry, or delete already-visible chests after load without rolling another ritual item, and test this reload case; ServUO `Services/Revamped Dungeons/TheExodusEncounter/Items/ExodusChest.cs:200` has the same defect.

4. **bug** | `server/customizations/Services/PointsSystems/CleanUpBritanniaData.cs:851`: The newly available Asclepius, BracersofAlchemicalDevastation, GargishAsclepius, GargishBracersofAlchemicalDevastation, HygieiasAmulet, and ScrollofValiantCommendation still have only MISSING comments, so they fall through to generic equipment valuation or zero instead of ServUO's 5,000-point reward value. Register those types in the existing table and test each value, matching ServUO `Services/PointsSystems/CleanUpBritanniaData.cs:656`; this is a missed port integration, absent from P195's deviation list.

5. **risk** | `server/tests/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs:818`: The once-per-character stat reward test checks only the current process, and the item round trip at line 392 saves only the scroll's owner, so neither tests the separate GenericPersistence store that prevents another +5 from a fresh scroll after restart. Add a persistence test that saves a rewarded character and the ExodusEncounter store, clears the in-memory reward set, reloads both, and verifies a fresh scroll is refused; a repeat-grant defect is not established by this review.

## Scope and limits

Read the encounter's controller, region, generator, spawn and decoration definitions, shared state, mining hook, items, creatures, resources, artifacts, and `server/tests/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs`. Also traced the shared decay helper, Nexus addon, AbyssalCloth, reveal interface and Detect Hidden patch, craft registrations, zealot stealing hooks, boss loot tier, bandage patches and scaling helper, and Clean Up valuation.

Compared the encounter with the corresponding ServUO source and checked the relevant pinned implementations, including DemonKnight reward selection, BaseCreature death callbacks and abilities, and BaseSpawner deletion. The existing death test at line 539 completes the exit in one process and round-trips the controller only after the replacement boss is alive; the chest tests round-trip a hidden chest or expire a revealed chest without reloading, which explains why the restart cases above are uncovered.

No new solo boss reward farming exploit or accumulating mobile spawn leak was established. The artifact roll selects a player with looting rights through pinned `UOContent/Mobiles/Monsters/AOS/DemonKnight.cs:133`; encounter spawner deletion reaches `UOContent/Engines/Spawners/BaseSpawner.cs:1285` and its `RemoveSpawns` at line 1245, and controller deletion removes its current boss.

These are source-level findings. Runtime reproduction, save/restart behavior in a running shard, map-dependent placement, and client behavior remain unverified in this task; no build, tests, new probes, or service connections were run. Suggested tests are follow-up work, not tests added here.

Ran `tools/progress.py --dry-run` with both work-copy paths supplied. It completed successfully, but also rewrote `tools/progress.json`; restored that incidental rewrite byte-for-byte from HEAD, leaving only this requested note changed.

P488 DONE
