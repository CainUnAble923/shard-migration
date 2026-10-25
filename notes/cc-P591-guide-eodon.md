# P591: player guide draft for Eodon

Written October 25, 2026. Docs-only task. Deliverable: `notes/wiki-drafts/eodon.md`.

## What the draft covers

- Public moongate travel through Ter Mur, the arrival and return-gate location, and what to do if the return gate is absent.
- Source-defined hunting areas, dinosaur hazards, tribal retaliation, and wandering shamans as healers.
- The Barako climbing vines, their range and height restrictions, and P458's paralysis, freeze, and casting refusals.
- Fresh-creature taming requirements, follower slots under pet training, first-tame losses, and the hatchling's corrected behavior.
- Tiger pelts and hatchling scutes, plus explicit limits on quests, champions, and creatures without regular Eodon spawns.

Plain American English throughout; no em dashes. No code, configuration, deployment, or task-list changes.

## Evidence checked

Read both work-copy `AGENTS.md` files first, then the migration copy's `docs/direction-decision.md` and `docs/tasks.md`. Read the P198, P354, and P458 implementation notes and the P407 and P583 reviews. Source behavior takes precedence over older comments and historical notes.

Code work-copy HEAD at inspection: `db4c85be142068d40895029d62407d2c13ad544e`. Pinned ModernUO HEAD: `d4531cd94b739613155225c234900de9f47d2c88`.

Paths in the following table are relative to the code work copy unless explicitly marked pinned. `TOL/` abbreviates `server/customizations/Services/Expansions/Time Of Legends/`; `PT/` abbreviates `server/customizations/Services/Pet Training/`. Each row names the files supporting its claims, rather than relying on keyword hits or prior port counts.

| Guide topic | Source read and result |
|---|---|
| Travel | Pinned `Projects/UOContent/Items/Misc/PublicMoongate.cs:268` defines `TerMurEodon`, including Royal City and Valley of Eodon at 719,1863,40; `:332` onward selects restricted menus and expansion/client-compatible lists. `TOL/EodonGeneration.cs:34` and `Run` place the return public gate at that location only when generated. A destination entry alone does not prove world placement. |
| Areas and regular encounters | `TOL/EodonSpawns.cs:69`, the entire `Definitions` array, supplies all guide coordinates and listed wildlife. Coordinates are approximate places to look, not routes tested in a client. Tribal and wildlife rows were read directly. The array contains no hatchling, saber-toothed tiger, greater phoenix, infernus, Dragon Turtle champion, Myrmidex creature, or Valley of One quest encounter entry. |
| Spawn proportions | `TOL/EodonSpawns.cs:151` weights each entry by its maximum count, the P458 correction. White and black tigers each have lower weights than ordinary wild tigers. No fixed sighting percentage is claimed: eligible entries and their caps affect each draw, and existing worlds may still hold earlier generated spawners. |
| Dinosaur hazards and taming | `server/customizations/Mobiles/Normal/Allosaurus.cs`, `Archaeosaurus.cs`, `Dimetrosaur.cs`, `Najasaurus.cs`, `Saurosaurus.cs`; `TOL/Mobiles/Anchisaur.cs` and `Gallusaurus.cs`. Read constructors, weapon abilities, poison properties, taming flags, and first-tame flags. Allosaurus has 18000 starting hits; Archaeosaurus can bleed; Dimetrosaur can Mortal Strike or Dismount; Najasaurus has lethal hit poison. Base taming values and the normal three-slot dinosaurs are from these files. No tameable flag is set for Allosaurus, Anchisaur, or Archaeosaurus. |
| Silverbacks | `server/customizations/Mobiles/Normal/SilverbackGorilla.cs`: no tameable flag; ranged banana attack with delayed damage. The guide avoids calling these safe because their ordinary melee damage is modest. |
| Desert poison | `TOL/Mobiles/DesertScorpion.cs`: lethal `HitPoison`; placement comes from the desert spawn rows. |
| Tribes | `TOL/Mobiles/EodonTribesman.cs`: tribe enum, `InitialInnocent`, aggressor-only `IsEnemy`, same-tribe idle allies rallied in `AggressiveAction`, and the shaman's mage AI. No claim of universal safety or immunity from criminal consequences. |
| Healers | `server/customizations/Mobiles/NPCs/WanderingShaman.cs` inherits WanderingHealer. Pinned `Projects/UOContent/Mobiles/Healers/WanderingHealer.cs:39` onward refuses resurrection for criminals and murderers. Distinguished from tribe shamans. |
| Vines | `TOL/EodonGeneration.cs:37` lists vines at 678,1759,z40 and z60, both leading to 679,1757,100. `TOL/Items/ClimbingVine.cs:37` checks range two, climber at or below the vine, and refuses paralysis, frozen state, or casting before movement. There is no reverse destination. |
| Tiger taming, riding, carving | `server/customizations/Mobiles/Normal/WildTiger.cs`, including WildWhiteTiger and WildBlackTiger: 95.1, two slots, default `CanRide=false`, and four matching pelts left on a wild corpse. `OnDoubleClick` does not make an ordinary tamed tiger rideable. The guide uses the exact controlled-state carving restriction rather than promising a yield from a controlled pet. |
| Slot ranges and training | `PT/BaseCreature.PetTraining.cs:95`, `:168`, `:200`, and `:247` derive lowered minimum slots and clamp first assignments; `PT/PetTrainingHelper.cs:151` enables the system with TOL. Its definition rows for Dimetrosaur, Gallusaurus, Najasaurus, Saurosaurus, WildTiger, and DragonTurtleHatchling provide slot minima and maxima. Najasaurus can start at one or two; hatchlings at three or four under training. These are not the hatchling constructor's literal five slots. `PT/Gumps.cs` provides Animal Lore/training information; `CurrentTameSkill` and the taming patch make trained requirements differ from base values. |
| Tame losses | Pinned `Projects/UOContent/Skills/AnimalTaming.cs:46` scales Str, Dex, Int, hit seed, and stamina seed. Its first-tame block at `:408` applies ordinary skill reduction and scales stats by 0.50 when `StatLossAfterTame` is true. Dimetrosaur and Saurosaurus still set that flag. Their old no-hook comments do not describe the now-available hook, but the flag remains the live implementation. |
| Hatchling correction | `TOL/Mobiles/DragonTurtleHatchling.cs`: 104.7; no substitute `StatLossAfterTame` flag; `OnAfterTame(Mobile, bool)` caps positive skills at 100 and retains 45% after ordinary scaling only on first tame; `OnCarve` drops four scutes when not controlled. `PT/PetTrainingHooks.cs:170` and `server/patches/AnimalTaming-pet-training.patch` carry the first-tame state. Ordinary non-paralyzed scaling 0.90 times 0.45 is 0.405; paralysis uses 0.86 instead. |
| Ability limits | Anchisaur and Saurosaurus implementations above omit the Rampage callback and natural Tail Swipe/Life Leech assignments respectively. The draft says these are not natural abilities, without claiming that the training ability system cannot offer them. |

## Important distinctions and unverified behavior

- P198 described a hatchling stat-loss substitute that P458 removed. The guide follows the current override, not that older note.
- P583 identifies a retained ModernUO re-tame difference from ServUO and an unasserted total skill cap. The draft only says the hatchling's extra first-tame cut does not repeat. It does not claim every re-tame follows OSI, promise a total training cap, or advertise release/re-tame as a training method.
- P458 analyzed a walking descent from the Barako platform using map data and movement code. It did not verify the step in a client or the running server's data match. The guide therefore calls the descent unconfirmed in a game client and advises bringing a way home. It does not present the inferred walk-off as a proven route or invent a down-vine.
- No running-shard access or game-client play-through was performed. Gate placement, current spawn mix, sightings, player travel, climbing, pet behavior, and carving were checked in source only. Historical P198/P354/P458 runtime and red/green reports were read, not rerun or independently certified.
- The guide is a draft, not a statement that every Eodon subsystem is installed or every ported type has a normal player acquisition route. No blanket future promise is attached to omitted quest or champion content.

## Validation

Read the full guide back against the source evidence above. `git diff --no-index --check -- NUL <file>` passed for both new Markdown files. Confirmed Windows PowerShell 5.1. Scope and file-size checks leave only the requested guide and this note; neither contains an em dash or approaches 5 MB.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these work copies: exit 0. The tool still writes `tools/progress.json` before its dry-run return, so its original bytes were preserved in memory and restored afterward. No generated status files are part of this docs-only change.

No tests added or run: this task specifies no lane tests and changes only Markdown. No new gate requires red/green evidence. No builds, containers, Haven connections, account actions, commits, merges, pushes, or branch switches. The stop-request file was checked between steps and was absent.

P591 DONE
