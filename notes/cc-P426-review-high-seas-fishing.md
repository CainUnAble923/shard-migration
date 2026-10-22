# P426: review of the High Seas fishing port and fix-up

Reviewed October 22, 2026 in the Valorite-tower work copies. Findings only. No code, tests, configuration, or deployment changed.

Read both AGENTS.md files, direction-decision.md, the task-list working agreement, P193's implementation notes, and P209's merge notes. No separate P193 or P209 Codex review was present beside those notes. P393's guide notes and its Codex review were also read; their acquisition and progression findings are not repeated here. P209 changed no fishing behavior, so this review checks the current P193 implementation after that merge.

## Source conventions

- `H/`: `ShatteredLegacy/server/customizations/Services/Expansions/High Seas/`.
- `C/`: the ShatteredLegacy work-copy root.
- `S/`: `D:/UO/ServUO-pub57/Scripts/`, read-only, HEAD `d76bf4443cf76d081ddaf8f57c87ff33749256af`.
- `U/`: `D:/UO/ModernUO-pinned/Projects/`, read-only, clean at HEAD `d4531cd94b739613155225c234900de9f47d2c88`.
- `T`: `C/server/tests/Services/HighSeasFishingVerification.cs`.

File and line references below identify the source reviewed, not a running-server observation. Items labeled risk need runtime verification. Inherited ServUO defects are identified explicitly; any fix should be justified under the existing rule for fixing broken behavior rather than silently changing fidelity.

## Findings

1. **bug | H/Items/Fish/FishInfo.cs:325 | Guaranteed rare and legendary catches at Gravewater Lake.** The location branch assigns the catch without calling `Roll`, so successful casts inside the coordinate rectangles give Holy Mackerel from Fishing 102.9 and Zombie Fish from 115.1, with the later Zombie Fish row replacing the mackerel instead of using its legendary chance; this is inherited from ServUO and is not explained in P193's deviations. Add the chance check to this branch and a regression that verifies a failed roll produces neither fish.

2. **bug | H/Items/Fish/FishInfo.cs:241; H/Items/LobsterTrap.cs:341 | A trap uses its owner's current location to choose its catch.** A deployed trap continues bobbing after its owner travels, but the catch selector reads the owner's map and region, allowing a trap left in ordinary water to roll Ice's Blue Lobster, for example, while the owner stands in Ice; this is also inherited from ServUO. Resolve trap habitat from the trap's map and position while retaining the owner's skill and attire, and cover owners traveling between regions and facets.

3. **risk | H/Mobiles/Charybdis.cs:46; H/Mobiles/Charybdis.cs:161; H/Mobiles/Charybdis.cs:597 | Saving during teleport can strand the boss on Map.Internal.** The boss internalizes for delayed callbacks, but its return map, return point, and pending return are not serialized or recovered on load, so a save in that interval followed by a restart can leave it hidden and absent from the encounter; the same transient-state omission exists in ServUO and has not been reproduced here. Persist enough return state with the appropriate ModernUO version bump and migration, recover an interrupted teleport after load, and verify it with a fresh-world reload during that interval.

4. **bug | H/Mobiles/BaseSeaChampion.cs:44; U/UOContent/Mobiles/Special/BaseChampion.cs:256 | Felucca sea champions drop a skull of type None.** The port returns `ChampionSkullType.None`, but its pinned parent unconditionally creates a skull on a Felucca death, whereas ServUO's parent suppresses that type, introducing an undocumented extra reward. Guard skull creation for None while preserving the other champion death behavior, and test an actual sea-champion death on Felucca rather than only asserting the SkullType property.

5. **bug | H/Mobiles/BaseSeaChampion.cs:149; H/Mobiles/BaseSeaChampion.cs:157 | The artifact lottery discards its final ticket.** `RandomMinMax(1, totalDamage)` includes the upper endpoint, but the cumulative comparison uses `>`, so a single eligible player registered for one damage never receives the artifact, and the existing 500-damage award assertions can fail randomly; this boundary defect is inherited from ServUO. Use an inclusive cumulative comparison for this ticket range and add deterministic first-ticket and last-ticket cases, separately from the already documented eligibility behavior.

6. **risk | T:348 | The fishing-patch test skips the bottle and SOS reward path.** It calls `GetResourceType`, `MutateType`, and `Give` separately without exercising `Construct` or `FinishHarvesting`, so it cannot detect repeated chest awards, failure to consume an SOS, or changed serpent delivery of a message in a bottle. Add integration coverage for an SOS yielding pre-loot followed by one chest and deletion, a subsequent cast without that SOS, and bottle delivery through the serpent path, including the modified rare-fish branch.

7. **risk | T:406 | Trap access and resumed timers have no behavioral regression coverage.** The trap fact sets Owner, InUse, and ItemID directly and calls `OnTick`, so it never exercises deployment, owner/guild/party/stranger retrieval, Felucca criminal retrieval, telekinesis, or whether a loaded active trap actually resumes bobbing. Add player-facing target and retrieval cases plus a timer-driven reload case, including rejection of a deployment cursor after the trap leaves the player's backpack.

8. **nit | H/Mobiles/BaseSeaChampion.cs:289; H/Mobiles/BaseSeaChampion.cs:298 | Another spawn-point correction is undocumented.** The port replaces ServUO's compound assignments inside the random bounds with ordinary subtraction and addition, changing where tentacles and teleport destinations are sampled, but P193 records only the separate mixed-axis correction in SpawnTentacle. Keep the correction if intended and record its reason alongside D-138, with a focused bounds check to preserve that decision.

## Supporting evidence

| Finding | Source evidence and current coverage |
|---|---|
| 1 | `H/Items/Fish/FishInfo.cs:58`, `:86`, `:283`, `:325`, `:437` show skills, row order, location assignment, and rectangles. `S/Services/Expansions/High Seas/Items/Fish/FishInfo.cs:308` has the same missing roll. `T:215` covers shore catches and a Twisted Weald region, not Gravewater. |
| 2 | `H/Items/Fish/FishInfo.cs:241` reads owner map/location/region; `:330` reads `from.Region` again. `H/Items/LobsterTrap.cs:341` passes the owner and trap position without a proximity or same-facet requirement. `S/Services/Expansions/High Seas/Items/Fish/FishInfo.cs:235` and `S/Services/Expansions/High Seas/Items/LobsterTrap.cs:268` contain the same split. |
| 3 | `H/Mobiles/Charybdis.cs:158` captures the return point, `:161` internalizes, `:165` schedules the callback, `:180` refuses a null return map, and `:597` restores only cooldowns. `U/Server/Mobiles/Mobile.cs:2441` saves the current map; `:6637` implements Internalize by setting Map.Internal. `S/Services/Expansions/High Seas/Mobiles/Charybdis.cs:665` saves the tentacle list without the return state. `T:663` round-trips an idle champion. |
| 4 | `S/Mobiles/Bosses/BaseChampion.cs:267` checks `SkullType != ChampionSkullType.None`; the pinned parent lacks that check. `T:610` only checks the enum value, and `T:589` never kills a champion. |
| 5 | `U/Server/Utilities/Utility.cs:860` includes both bounds. `S/Services/Expansions/High Seas/Mobiles/BaseSeaChampion.cs:116` and `:124` contain the same ticket/comparison pair. `T:649` registers 500 damage before calling AwardArtifact twice. The port's eligibility mismatch is already explicitly described in its source comment and is not a new finding here. |
| 6 | `U/UOContent/Engines/Harvest/Fishing.cs:231` handles bottle construction, `:241` begins SOS recovery, and `:314` deletes the SOS when awarding its chest. `:324` handles serpent delivery. `U/UOContent/Engines/Harvest/Core/HarvestSystem.cs:158` constructs the selected catch and `:199` delivers it. |
| 7 | `H/Items/LobsterTrap.cs:223` handles deployment, `:413` handles access, and `:517` handles post-load recovery. `T:413` instead sets deployment state directly; `T:454` round-trips the trap without advancing a resumed timer. The stale-cursor case is a missing regression scenario, not a claim of a reproduced theft. |
| 8 | Compare `S/Services/Expansions/High Seas/Mobiles/BaseSeaChampion.cs:236` and `:243`. At distance 10 on a classic boat, the source's modified axis samples offsets -13 through -10 or +3 through +13; the port samples -10 through -3 or +3 through +10. |

## Serialization and reward checks with no additional finding

No serialization-version mismatch was found. The new persistent classes in the reviewed port files use `[SerializationGenerator(0, false)]`; FishInfo itself is not persistent. Fisher/date, trap bait/owner/use state, trophy identity/metadata, and spawned creatures' master references have declared fields. The Fishing and TaxidermyKit patches add no saved fields to existing types, so those hooks do not require stock-type version bumps. Finding 3 concerns missing transient recovery state, not disagreement between existing field layouts and their declared versions.

No new message-in-a-bottle or SOS duplication path was found by source inspection. The pinned bottle replaces itself with an SOS, and the chest branch deletes the SOS before returning the chest. The fishing port retains those paths. This does not establish runtime correctness; finding 6 records the missing regression coverage. The deferred bikini/SOS-artifact expansion, baits, pies, and encounter acquisition are already documented and are not reported again.

FishInfo's normalized source table matched ServUO in row order, hue, type, label, habitat, deep-water requirement, chance constant, and minimum skill. The fish classes' labels, carving outputs, and default weights were compared with the source, and the artifact and human-set values were checked against their source and pinned parents. No additional unexplained value difference was found in those checks. The changed trophy housing permission, fishing-skill clamp, missing attributes, and deferred content have reasons in P193 and are excluded from the findings.

## Files reviewed

The port files below are relative to `H/`; each was checked against the corresponding ServUO file. Trophies also uses `S/Items/Consumables/TaxidermyKit.cs` for its table and kit behavior.

| Group | Files |
|---|---|
| Fish | `Items/Fish/Fish.cs`, `Items/Fish/CrabsAndLobsters.cs`, `Items/Fish/RareFish.cs`, `Items/Fish/LegendaryFish.cs`, `Items/Fish/FishInfo.cs`, `Items/Fish/Trophies.cs` |
| Traps | `Items/LobsterTrap.cs`, `Items/LavaLobsterTrap.cs` |
| Champions and spawn | `Mobiles/BaseSeaChampion.cs`, `Mobiles/Charybdis.cs`, `Mobiles/OsiredonTheScalisEnforcer.cs` |
| Artifacts | `Items/Artifacts/CullingBlade.cs`, `Items/Artifacts/RuneEngravedPegLeg.cs`, `Items/Artifacts/HelmOfVengence.cs`, `Items/Artifacts/SmilingMoonBlade.cs`, `Items/Artifacts/WandOfThunderingGlory.cs`, `Items/Artifacts/EnchantedCoralBracelet.cs`, `Items/Artifacts/RingOfTheSoulbinder.cs`, `Items/Artifacts/LeviathanHideBracers.cs`, `Items/Artifacts/EnchantedBlade.cs`, `Items/Artifacts/EnchantedVortex.cs` |
| Other content | `Items/SOS Artifacts/YellowPolkaDotBikini.cs`, `Items/Sets/FishermansSet.cs`, `Items/Resources/Cooking Ingrediants.cs` |
| Integration | `C/server/patches/Fishing-high-seas-fish.patch`, `C/server/patches/TaxidermyKit-fish-trophies.patch`, `C/server/patches/Fishing-deep-water-finds-osi.patch`, their registration in `C/docker/uo/apply-patches.sh`, and `T` |

Supporting pinned code read: Fishing, HarvestSystem, TaxidermyKit, MessageInABottle, SOS, SpecialFishingNet, BaseChampion, ChampionSkull, BaseCreature, NPCSpeeds, Item.ScissorHelper, Mobile.Internalize/serialization, Utility.RandomMinMax, Hats, LeatherArms, LeatherGloves, LeatherChest, and StuddedLegs. The custom BaseSetClothing carrier was also checked.

## Verification limits and housekeeping

This was a static review. No tests were added or run, as specified by the prompt's lane tests; P193/P209's passing builds are historical results, not verification performed here. Runtime reproduction, live placements, reachable fishing tiles, a client session, and an actual save/restart during teleport remain unverified. No Haven connection, Docker action, live-stack action, account change, branch change, or commit was performed. The stale generated server/uo tree was not read.

Commands ran in Windows PowerShell 5.1. Ripgrep was unavailable, so searches used PowerShell and Python. Progress generation was omitted because this task changes only this review note and the existing dry-run command is documented in P393 as writing progress.json. The STOP-REQUESTED path was checked between review steps and before writing.

Final checks: the code work copy is clean; the docs work copy contains only this new note. Both `git diff --check` commands passed, and the note was checked directly for trailing whitespace, ASCII text, no em dashes, and size below 5 MB.

P426 DONE
