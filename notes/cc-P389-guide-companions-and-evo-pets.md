# P389: player guide to companions, squires, and evo pets

October 21, 2026. Docs-only task in the Golem's Valorite work copies.

## Deliverables and scope

- Player draft: `notes/wiki-drafts/companions-and-evo-pets.md`.
- Work record: this file. File and line citations belong here, not on the player page.
- The page distinguishes built mechanics, source-derived availability limits, and decided
  future features marked (planned). It ends with Sources and Contradictions; no contradiction
  was resolved by changing code or deciding between competing plans.
- No code, tests, configuration, docs-directory files, VERSION, or CHANGELOG changed.
  No Haven connection, deployment, build, commit, merge, push, or branch switch.
- Initial work copies were clean. The session paused once when the Golem's stop file appeared
  with its budget notice. Chase's continuation authorized resuming after that file was removed.
  The checkpoint evidence below was retained and completed by the subsequent sections.

## Reading and source scope

Read both work-copy AGENTS.md agreements first. Reviewed the required direction and task
material, both model guide pages, and the feature queue's relevant F-12, F-13, F-33, F-35,
F-39 decisions. Consulted the companion design and P41 review alongside the notes. No upstream
coverage or historical completion count was treated as proof of player behavior.

Searched all `notes/cc-P*.md` for companions, squires, evo pets, follower slots, pet training,
and reward mounts, then read the relevant topic sections. Primary histories consulted:
P41, P45, P47, P59, P65, P69, P70, P75, P80, P120, P121, P129, P130, P138, P171, P172,
P234, P262, P276, P369, P371. Related topic passages in the broader research, intake, wiki,
playtest and progression notes were screened too; incidental port counts, staff-only
playtest recipes and unrelated build logs were not copied into the player guide.

The original `notes/cc-P264-companions-b1-base-and-record.md` is absent in this work copy
(explicit filename search). P369, current companion code, and CompanionBaseVerification
supply the evidence instead. P378 also records that original note's absence.

Canonical shard sources were read under `server/customizations/`, `server/tests/`, and
`server/patches/`. `server/uo/` was not read. Pinned ModernUO was inspected read-only at
`D:/UO/ModernUO-pinned`; `git rev-parse HEAD` confirmed
`d4531cd94b739613155225c234900de9f47d2c88`. Pinned citations below use that revision.

## Source evidence collected before the pause

Paths in this section are relative to the ShatteredLegacy code work copy unless specified.
Numbers are source defaults, not verified running settings. Line references are from this
session's source reads, not copied uncritically from older notes.

### Starter acquisition and plain-pet behavior

- `server/customizations/Tutorial/TutorialFarm.cs:53` offers dog and cat at the farm.
  `:171` implements the choice, checks the lesson step and allowed line, gives the pet,
  and records the farm choice only on success (`:186`). The Farmhand is Wren Tallow
  (`:9`), beside the field gate (`:55`). Placement on a running shard is unverified.
- `server/customizations/Tutorial/ClusterFTutorial.cs:210` lists dog, cat, fox, bird
  for graduation. `:249` awards the graduation box and opens the pet choice only if
  the account did not already take its farm pet (`:254`). Do not promise a second pet.
- `server/customizations/Tutorial/TutorialGumps.cs:228` implements that four-line picker.
  Its heading at `:236` says "Choose your companion", although these are ordinary evo pets.
  This is a candidate for the page's Contradictions list.
- `server/customizations/Mobiles/Evo/EvoPet.cs:23` derives from BaseCreature, not BaseMount.
  It uses melee AI (`:69`), one follower slot (`:78`), and is not tamable in the wild
  (`:79`). `:470` gives it to the owner already bonded (`:487`) and following (`:489`).
  A mount-like appearance does not give this class riding behavior.
- `EvoPet.cs:431` locks the owner's hue choice after the first selection.
  `:443` reopens an unfinished hue choice, then an eligible unfinished body choice,
  when the owner double-clicks. `:343` locks a stage's body choice once made.
- `EvoPetData.cs:177` lists natural, shadow, snow, rust, sand, storm, ember.
  `EvoPetGumps.cs:30` tells players the color stays at every stage.

### Evolution stages and current limits

- `server/customizations/Mobiles/Evo/EvoPetData.cs:93`: dog stages 1 through 5 are pup
  (dog), young hound (leather wolf), hound (owner's breed choice), guardian hound
  (cu sidhe), windrunner. Stage 3 breeds at `:98`: Alaskan malamute, Great Dane,
  Saint Bernard, Newfoundland, Rottweiler, Black Russian terrier.
- `EvoPetData.cs:105`: cat stages are kitten, cub (baby tiger), great cat (tiger or
  lion choice), sabertooth, manticore.
- `EvoPetData.cs:114`: fox stage 1 kit; stage 2 fox is art pending; stage 3 bake kitsune
  requires owner loop 1; stage 4 kitsune is art pending and requires loop 5 plus Bond Trial.
  Shapeshifting rules at `:120` are comments describing future work, not implemented behavior.
- `EvoPetData.cs:133`: bird stage 1 chick (crane), stage 2 firebird (phoenix bird),
  stages 3 great bird and 4 griffin art pending, stage 5 hiryu (lesser hiryu).
- `EvoPetData.cs:49` skips art-pending stages and uses the gates of the stage entered.
  Never renumber fox/bird stages or describe every listed body as player-reachable now.
- `EvoPetData.cs:215` gives cumulative XP defaults 500 / 3,000 / 13,000 / 53,000
  for stages 2 / 3 / 4 / 5. `EvoPet.cs:268` retains total XP; `:298` checks the
  next enabled stage against its own threshold.
- `EvoPetData.cs:101` and `:110`: dog/cat stage 4 also requires loop 1;
  `:102`, `:111`, `:141`: final dog/cat/bird stage requires loop 5 and Bond Trial.
- `EvoPet.cs:28` still defaults the owner loop source to zero. Repository searches
  found no production assignment wiring it to the new graduation counter. Tests replace
  it temporarily. `EvoPet.cs:50` explicitly says Bond Trial is not designed yet.
  Thus tables must distinguish coded future gates from currently reachable progression.
- P371's note explicitly leaves evo owner-loop integration for later. Graduation records
  loop 1 now, but it does not unlock these pets' loop gates. The actual
  `ClusterFLoops` source was checked on resumption as documented below.
- `EvoPet.cs:241` awards evo XP only to controlled evo pets in the victim's damage list;
  it uses their damage share (`:256`) and excludes pets/summons (`:243`). Gear's Bond
  effect modifies XP there. Do not publish exploit details.
- `EvoPetData.cs:159` uses a common placeholder stat curve for all lines.
  Role abilities at `:36` are an empty future slot. Protector/striker/trickster/scout
  labels are planned roles, not functioning special abilities. `EvoPet.cs:146` applies
  stage stats, fully heals, and raises but never lowers the listed learned skills.

### Companions and squires

- Only groundwork is built. `server/customizations/Companions/CompanionParty.cs:164`
  explicitly says there is no hiring yet. Do not include its staff commands on the page.
  `Tutorial/ClusterFTutorial.cs:13` says the squire comes from a later early-League quest,
  not built. Present acquisition, class development, room services, and companion riding
  as (planned), not as instructions a new player can follow now.
- `CompanionSettings.cs:23` has Blade, Bow, Arcane, Support, Rogue starter paths.
  Branches are enumerated at `:34`; their enum presence is not a player choice UI.
- `CompanionSettings.cs:74` implements max-level defaults 50 at loop 0, 100 at loop 1,
  then +5 per loop to 200. `:81` has rank slot costs 1,1,2,2,3,3.
  `BaseCompanion.cs:64` identifies ranks 0 Squire through 5 Legend but explicitly
  leaves their placement on the newer loop ladder open. Do not invent intermediate
  generic rank names or assign rank promotions to particular newer loops.
- `CompanionSettings.cs:85` party-size defaults include the player: 3,4,5,5,6,6.
  The code's full party is five companions plus the player, not P41's four-companion
  placeholder. `:91` follower-cap defaults end at 18 for loop 11 and 19 for loop 21.
  These are groundwork defaults, not current loop unlocks: `:121` still has an unset
  owner-loop provider, read as zero by `:123`.
- `CompanionParty.cs:59` checks both companion count and shared follower slots.
  `:81` raises the follower cap without lowering an existing value.
- `BaseCompanion.cs:163` and `:173` set loop and rank independently. There is no
  player loop/promotion action here. `:238` remembers skill peaks. Record storage
  does not prove that future loop reset/XP mechanics are implemented.
- `CompanionParty.cs:116` takes owned companions out of the world at owner logout;
  `:139` restores them on login. `BaseCompanion.cs:234` excludes auto-stabling.
- Design decisions read in migration `docs/companions/companions-squire-evo-research.md`:
  `:16` keeps companion rank when owner resets; `:20` keeps its strength;
  `:42` full party six including player; `:59` League/board acquisition;
  `:61` all classes ride real and ethereal mounts; `:168` companion cannot loop
  past its owner. These are decisions for future behavior, not completed player systems.
  Its old six-step ladder (`:148`) conflicts with the newer ladder; retain the conflict.

## Completed source checks after resuming

Paths beginning `server/` are relative to ShatteredLegacy. Pinned paths are relative to
`D:/UO/ModernUO-pinned/Projects/UOContent/`. These complete the initial checkpoint above.

### Progression reachability and decisions

- `server/customizations/Tutorial/ClusterFLoops.cs:25` reads the real per-character loop
  record; `:34` graduates through CompleteLoop(1), which records it at `:60`.
  `:31` supplies the 50/100/+5/200 ladder; `:40` is still an empty reset integration hook.
- A fresh search across canonical customizations and patches found no production assignment
  connecting `EvoPet.OwnerLoopsSource` or `CompanionSettings.OwnerLoopProvider` to that record.
  The evo source initializes its delegate to zero (`EvoPet.cs:28`); companion provider access
  falls back to zero (`CompanionSettings.cs:121`). Test fixtures inject their own values.
- The guide's normal stopping points (dog 3, cat 3, fox 1, bird 2) are a **source-derived
  reachability inference**, not a measured in-client play-through. They follow the unconnected
  owner-loop source, enabled rows, XP thresholds and choice rules already cited above.
  Full later forms are not described as unfinished bodies merely because they are gated.
- Migration `docs/feature-queue.md:1225` gives the revised ladder. `:2576` decides the
  mule slot reduction, `:2584` the long-term party-plus-mount budget, `:2920` the four
  evo roles, `:2984` the chosen bodies and `:2995` the pending-art/stats-only first build.
- Migration `docs/companions/companions-squire-evo-research.md:150` starts at Squire;
  `:155` ends at Legend. `:16` and `:20` retain rank/strength across the owner's reset;
  `:168` imposes the owner-loop ceiling. These player progression actions remain planned.
- Companion design `:177` says player plus five companions; its old loop table at `:148`
  conflicts with the current 21-loop top. P41's section 11.2 instead uses four companions
  and a four-slot final evo mount; P47 section 6 uses five companions and an unknown mount
  cost, with 3 as its curve placeholder. The draft records all of these without settling them.
- P276's placement/play-through remains pending in that note's Continuation section.
  Therefore the page does not claim the Farmhand is present on the running shard.
- P138 adds wearable kitsune art. It does not activate the evo table's art-pending flag
  or implement shapeshifting, so the planned fox capstone is not advertised as usable.

### Animal Training and skill gains

- `server/customizations/Services/Pet Training/PetTrainingHelper.cs:153` excludes EvoPet
  and PackMule; `:180` gives a tameable without a definition an Untrainable default.
  Companion groundwork is not tameable, has no species row or training UI of its own.
- `Gumps.cs:110` limits the training section to the controlling owner. `:142` offers Begin
  only below the slot maximum; `:120` shows progress; `:133` exposes options when ready.
  `:615` begins training through the actual lore reply. `:522` displays Learns on skill pages.
- `TrainingProfile.cs:137` initializes a round; `:149` applies a purchase. Its first purchase
  adds a slot through RemoveFollowers/ControlSlots++/AddFollowers (`:153`), then raises
  CurrentTameSkill (`:171`). `:199` cancels remaining points. Battle progress is `:245`;
  choice spending requires a completed bar (`:63`). The page gives no fixed battle duration.
- `Gumps.cs:1758` validates Train Pet: ownership, proximity, combat, available slot, points,
  matching scroll and projected tame requirement. It sends the final confirmation (`:1804`).
  `:1821` applies the improvement, consumes a skill scroll (`:1852`) and invokes OnTrain.
- `PetTrainingHelper.cs:1039` checks projected Animal Taming. The guide does not repeat the
  P120 survey's more general statement that both Lore and Taming gate spending: the current
  implementation specifically checks Taming here.
- `PetTrainingHelper.cs:1360` raises a skill CAP, not its practiced base. `Gumps.cs:1901`
  searches top-level backpack PowerScroll items matching the skill and target cap.
- `Gumps.cs:1934` is the planning ENABLE/DISABLE control; `:2001` toggles planning;
  `:2024` removes an entry. Selections in planning use Add To Plan (`:1723`) rather than
  ApplyTraining. `PlanningProfile.cs` persists the entries. No planning action is claimed
  to grant stats or abilities for free.
- `server/customizations/ClusterFPetGainSpeed.cs:26` sets the +0.1/+0.004/+0.1/x3
  defaults. `:45` counts Taming/Lore above 100 through 200; `:49` combines bonuses;
  `:57` reads the owner's effective skills; `:68` still reads the unconnected evo loop
  source; `:75` onward requires Rangers membership and walks the Outriders rank rungs.
  Thus x1.00/x1.16/x1.80/x2.40 in the page follows actual defaults at zero loops.
- `server/patches/SkillCheck-pet-gain-speed.patch` multiplies the controlled creature's
  gain CHANCE. The page does not call it a guaranteed time reduction, a gain-size change,
  an evo-XP multiplier or a stat-gain boost. The coded loop bonus is labeled (planned)
  because normal progression is not connected to it.
- `AnimalTrainer.PetTraining.cs:1` records the omitted ML teaching quests, despite the
  Quest Giver property. The page does not direct players to those absent quests.

### Commands, care, stabling and slot accounting

- Pinned `Mobiles/AI/BaseAI/OnSpeech.cs:137` handles nearby pet speech, with the owner
  checks at `:144`. `:166`, `:187`, `:193`, `:198` carry come, attack, follow me, stay.
- Pinned `Items/Skill Items/Misc/Bandage.cs:175` and `:185` select Veterinary and Animal
  Lore for animal/monster non-player patients. `Mobiles/BaseCreature.cs:4126` restores
  a dead bonded pet; the guide does not invent a resurrection success threshold.
- Pinned `Mobiles/Vendors/NPC/AnimalTrainer.cs` handles stable/claim storage. The current
  shard stable-cap patch calls ClusterFSkillClamps, not player loops:
  `server/patches/AnimalTrainer-stable-slots-scaled-200.patch:10`, and
  `server/customizations/ClusterFSkillClamps.cs:244`. The page deliberately gives no
  universal stable count or promises of loop-raised stable storage.
- Pinned `Mobiles/Animals/Mounts/BaseMount.cs:77` internalizes/moves the mount when Rider
  changes without releasing its master or follower count. Ethereals instead explicitly
  add/remove their slot from Rider (`Ethereals.cs:154`, `:162`). `:69` defaults that cost
  to one and `:201` checks capacity before summoning.
- Starting five slots and the horse-plus-pet example are also exercised in
  `server/tests/Mobiles/Companions/CompanionBaseVerification.cs:220` (two one-slot
  companions, then a horse takes the count from two to three).
- The evo class is BaseCreature (`EvoPet.cs:23`) and has no mounting override. Its appearance
  does not turn it into BaseMount. No later evo form is advertised as a free mount.

### Compact Mule

- `server/customizations/Mobiles/Mule/MuleErrand.cs:25` sets Dull Copper rank, 50 ore,
  25 ingots; `:50` checks League registration/rank; `:82` consumes the turn-in;
  `:107` grants the bonded mule only at the delivered step. No repeat reward is promised.
- `server/customizations/PackMule.cs:35` defaults its computed slot cost to one;
  `:351` applies it; `:369` re-counts the owner when changing it. `:560` opens the pack
  if double-clicked by the rider, otherwise delegates to normal mounting.
- `server/customizations/Mobiles/Mule/MuleData.cs:56` lists Compact, Bronzeback,
  Shadowhide, Valorite-Barded, Celestial tiers. ModuleSlots are tier values (`PackMule.cs:162`),
  separate from follower slots. `MuleModules.cs:122` checks owner, life, tier, guild and
  capacity; `:259` sets the follower cost to zero at Trailwise Tack III (`:264`).
- P69 section 2 and current MuleUpgrades/Civic Mule Exchange flow support upgrades independent
  of owner loops. The page avoids quoting provisional prices for every upgrade or module.
- `MuleModuleData.cs:117` still labels Steady Hoof Wraps stubbed/planned, agreeing with P234.
  The proposed extra dismount systems are not advertised as deployed behavior.

### Veteran rewards and boss reward mounts

- Pinned `Engines/Veteran Rewards/RewardSystem.cs:560` defaults rewards on;
  `:562` uses a 30-day interval. `:95` divides real account age by it.
  Pinned `Accounting/Account.cs:283` defines AccountAge as Core.Now minus Created.
  `RewardList.cs:9` multiplies the interval by list index. Table ages in the guide are
  computed from those defaults, not a read of running configuration.
- RewardSystem list entries: `:393` level 3 (horse/ostard/llama at `:406`);
  `:413` level 4 (kirin/unicorn/ridgeback at `:431`); `:439` level 5
  (swamp dragon/beetle at `:461`); `:496` level 9 (polar bear at `:500`);
  `:505` level 10 (cu sidhe at `:531`); `:539` level 11 (reptalon at `:543`);
  `:548` level 12 (hiryu at `:552`). This enumerates the rows behind the table.
- `RewardSystem.cs:566` shows a login notice while choices remain. RewardNoticeGump's
  OnResponse opens RewardChoiceGump. RewardConfirmGump.OnResponse checks access,
  consumes a reward point and gives the constructed item. `RewardSystem.cs:172`
  checks age again for use of a reward-marked item.
- Pinned `Mobiles/Animals/Mounts/Ethereals.cs:11` is an Item, not a living creature;
  `:38` sets Blessed. `:178` validates reward age; `:210` casts on double-click.
  `:495` specifically makes RideablePolarBear an EtherealMount too. The default one-slot
  rule at `:69` has no per-species override in this file.
- F-13's reward default decision is `docs/feature-queue.md:1359`; labels remain
  year-based in the pinned UI/item code (`Ethereals.cs:150`, RewardSystem's year label
  helper). Those are recorded as a presentation contradiction, without changing them.
- No reward-mount sale was found in current LeagueShop catalog code. P229's Parts 5/6
  explicitly leave veteran rewards unchanged. The page does not invent an AP/Renown price.
- `server/customizations/Mobiles/Bosses/ChiefParoxysmus.cs:99` drops its swamp-dragon
  statuette; `MonstrousInterredGrizzle.cs:109` drops the Grizzled Mare statuette.
  The page says possible reward and makes no encounter-access or drop-rate guarantee.
- `server/customizations/Items/Addons/ParoxysmusSwampDragonStatuette.cs:22` constructs
  ParoxysmusSwampDragon; its creature implementation derives SwampDragon (`:12`) and
  deletes on release (`:26`). Pinned `Items/Special/ML/GrizzledMareStatuette.cs:17`
  constructs GrizzledMare, whose `Mobiles/Animals/Mounts/GrizzledMare.cs:6` derives
  HellSteed and `:15` deletes on release.
- Pinned `Items/Special/ML/BaseImprisonedMobile.cs:17` opens confirmation from the backpack.
  `Gumps/ConfirmBreakCrystalGump.cs:28` checks follower capacity through SetControlMaster;
  `:37` bonds the created pet; `:54` consumes the statuette only on success.
  Reusable ethereals and one-use boss statuettes therefore have separate instructions.

## Verification and limits

Existing verification files were inspected as source, not executed. No tests or gates were
added, so there is no new red/green cycle to claim; the prompt specifies no lane tests.
Useful inspected cases and their scope:

- `server/tests/Mobiles/Evo/EvoPetVerification.cs:188`: dog XP, permanent pick, loop and
  Bond Trial gates; `:252`: skipped pending fox/bird rows with later gates retained;
  `:290`: hue permanence; `:313`: owner Reset Stone stand-in leaves pet state intact.
  The latter is not proof of a full future F-12 reset, which does not exist yet.
- `server/tests/Mobiles/Companions/CompanionBaseVerification.cs:203`: rank costs,
  party-vs-slot limits, ladder and follower re-counting; its logout/record cases supply
  groundwork evidence, not proof of hiring or player promotion.
- `server/tests/Services/PetTraining/PetTrainingVerification.cs:383`: battle bar and
  slot/tame requirement changes; `:447`: planning/abilities; `:653`: evo/mule exclusions;
  `:728`: actual Animal Lore target and Begin button.
- `server/tests/Skills/PetGainSpeedVerification.cs:137`: default multiplier cases;
  `:200`: owner inputs; `:297`: skill-check hook; `:371`: Learns text on skill pages.
- `server/tests/Tutorial/TutorialFarmVerification.cs:272`: no graduation pet offer
  after the farm; `:295`: approved dog/cat forms and gates.
- `server/tests/Mobiles/Mule/MuleVerification.cs:118`: one slot and re-count;
  `:514`: errand gates/turn-in/collection; `MuleModuleVerification.cs:241`: Tack III
  zero slots; `:387`: Wraps remain stubbed.

Unverified: running configuration and account ages; placement and accessibility of the
farm, recruitment services and boss encounters on any running shard; in-client appearance,
animations, UI, audio and a complete player play-through. No external wiki or memory was
used to fill those gaps. The guide's introductory availability caveat and explicit farm/boss
statements preserve these limits.

Progress report: ran `tools/progress.py --dry-run` in-process with SL_SHARD/SL_MIGRATE set
to these work copies. The tool writes `tools/progress.json` inside build() even with --dry-run
(`tools/progress.py:722`, before the return at `:737`). A temporary in-memory Path.write_text
wrapper suppressed only that known snapshot write and rejected any other write, preserving
this task's requested docs-only scope. It completed and printed its report; one snapshot
write was suppressed. No tool/repository source was edited. Artifact counts from that stem
proxy are not used as evidence of game behavior in this guide.

### Final document checks and second pause

Both deliverables are written. Document review passed: relative Sources links resolve;
Sources and Contradictions are the final sections; required topics are present; the page
has no em dashes, staff commands, file:line citations, trailing whitespace, or control
characters. Both new files are below 5 MB. Existing tests were inspected only, not run.

`git diff --check` passed in both repositories. Both untracked documents were also checked
with `git diff --no-index --check -- NUL <file>`: no whitespace diagnostics (the usual
no-index exit 1 indicates differences from the empty file). Windows PowerShell was confirmed
as 5.1.26100.9444. Git status shows only the two requested new notes files in shard-migration;
the ShatteredLegacy work copy remains clean.

The stop file reappeared during these final checks. Its reason is recorded below. This
review step is complete. No substantive guide writing remains; on authorized continuation,
check the stop file and work-copy status, make any needed final corrections, then append
P389 DONE only when handing off the finished prompt. Do not repeat the source survey or run
server tests/builds for this docs-only task.


Stop-file reason: "Find a stopping point: the 5-hour window is at 95% (the hard stop is 95%: past 100% Codex spends credits)".

## Completed handoff, October 22, 2026

Resumed with the Golem's authorization. Rechecked both saved deliverables, all relative
source links, section order, style restrictions, whitespace, file sizes, both repositories'
status, and stop-file absence. All checks passed. The code work copy is clean; only the
requested guide and this work record are new in shard-migration. No further corrections
were needed. No code changed, tests/builds ran, or live services were contacted. The draft
remains unpublished, with running-shard availability and client behavior explicitly unverified.

P389 DONE
