# P559: your first companion guide

October 24, 2026. Documentation only. Draft: [Your first companion](wiki-drafts/first-companion.md).

Read both work copies' AGENTS.md, the direction decision and task-list instructions, [P480's notes](cc-P480-tutorial-first-play-fixes.md), its Codex review, and the existing [companions guide](wiki-drafts/companions-and-evo-pets.md). Checked the relevant behavior against canonical shard customizations and patches, and read-only pinned ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`.

## Delivered

The short player guide covers the graduation pick, reopening it through Rook, follower space, the permanent color choice, bonding, basic orders, pet death, Wren's directions to Tobin, tutorial vets, the graduation elixir and replacement sellers, and stabling and claiming. It links to the longer guide for evolution and ordinary Animal Training instead of repeating its planned features.

The wrapper requests this notes filename; the embedded task requests `cc-P559-guide-first-companion.md`. Both are supplied, with that shorter file pointing here. No existing guide was rewritten.

## Source evidence

Paths below are relative to ShatteredLegacy unless prefixed with `ModernUO`. Line references describe the files read for this task.

| Guide claim | Evidence |
|---|---|
| Graduation offers dog, cat, fox, bird; a pending choice can be reopened; a farm pet suppresses the graduation offer | `server/customizations/Tutorial/ClusterFTutorial.cs:230` (pending state and offer), `:313` (box and reward logic), `:328` (farm-pet exclusion); `Tutorial/TutorialGumps.cs:147` (Rook's menu button), `TutorialPetPickGump` in that same file (pictures, choices, follower-space refusal) |
| Starter pet is bonded immediately, follows its owner, costs one slot, cannot be retamed after release | `server/customizations/Mobiles/Evo/EvoPet.cs:78` (ControlSlots, Tamable and MinTameSkill), `:470` (GivePet, IsBonded and follow order) |
| Color choice is permanent and can be reopened before choosing | `server/customizations/Mobiles/Evo/EvoPet.cs:431` (ChooseHue), `:443` (OnDoubleClick); `Mobiles/Evo/EvoPetGumps.cs:24` (color window) |
| Fighting earns evolution XP | `server/customizations/Mobiles/Evo/EvoPet.cs:238` (creature death hook and damage share) |
| Follow, stay and attack speech | `ModernUO/Projects/UOContent/Mobiles/AI/BaseAI/OnSpeech.cs:151` (keywords and command dispatch) |
| Bandages use Veterinary and Animal Lore for animals | `ModernUO/Projects/UOContent/Items/Skill Items/Misc/Bandage.cs:175` (GetPrimarySkill and GetSecondarySkill) |
| Farmhand directs ghost-pet owners to Tobin, with a fallback to the town vet | `server/customizations/Tutorial/TutorialFarm.cs:119` (NoticeGhostPet), `:138` (farm vet location), `:529` (Farmhand movement hook) |
| Tobin at the farm, tutorial vet at New Haven stables | `server/customizations/Tutorial/TutorialCorePlacement.cs:27`, `:79`, `:82`; town vet is seeded only if no Veterinarian exists within 60 tiles of the town center |
| Young fee waiver, fee shown in window, bank payment, corpse wait, skill loss | `server/customizations/Tutorial/TutorialPetCare.cs:28` (ghost pets within 12 tiles of owner), `:43` (fee), `:54` (offer window), `:99` (step within 3 tiles), `:110` (double-click within 4), `:136` (resurrection checks and 0.2 skill loss). Starter MinTameSkill is 0, so the fee is integer 100 + 1.1041^0 = 101 gold |
| Ordinary vets do not resurrect | `ModernUO/Projects/UOContent/Mobiles/Vendors/NPC/Veterinarian.cs` defines stock and training only; no shard Veterinarian resurrection patch was found. P480's shard-wide vet port remains a separate proposal |
| Graduation supplies a blessed elixir | `server/customizations/Tutorial/ClusterFTutorial.cs:313`; `Tutorial/TutorialPetCare.cs:206` (StarterElixirOfRebirth) |
| Elixir use: backpack, living user, ghost pet, corpse gone, two tiles, suitable location, consumed on success | `server/customizations/Items/Consumables/ElixirOfRebirth.cs:23` (OnDoubleClick), `:35` (TryResurrect) |
| Animal trainer lists elixir for 500 gold | `server/customizations/Tutorial/TutorialPetCare.cs:187` (SBPetRebirth); `server/patches/AnimalTrainer-elixir-of-rebirth.patch` adds that stock to AnimalTrainer |
| Rangers' League guildmaster sells to members for 375 gold | `server/customizations/OutridersGuildmasterGump.cs:259` (member menu), `:267` (500 * 3 / 4), `:366` (case 34 membership and payment checks) |
| Resurrection returns pet at 10 health; do not abandon a ghost | `ModernUO/Projects/UOContent/Mobiles/BaseCreature.cs:4126` (ResurrectPet), `:5987` (ghost abandonment handling) |
| Stable and claim commands, 30 gold, living pet and combat restrictions, follower capacity when claiming | `ModernUO/Projects/UOContent/Mobiles/Vendors/NPC/AnimalTrainer.cs`, methods BeginStable, EndStable, Claim, CanClaim, DoClaim and OnSpeech; `server/patches/AnimalTrainer-stable-slots-scaled-200.patch` changes the allowance calculation only |

## Limits and review

- Source review only. No running shard, client, live configuration, NPC placement, or vendor inventory was inspected. The guide says so. Tutorial configuration and seeding remain gated for test use; the draft is not a claim that these services have been launched.
- P480's earlier client evidence covers the companion picker and graduation box. Its notes explicitly leave the ghost-pet vet interaction and trainer purchase unplayed. This task adds no client verification.
- The existing longer companion draft predates P480. Its farm availability warning is retained; this new guide adds the newer resurrection route and does not promise the later evolution forms shown in the picker.
- P480's review flags retained vet offers allowing remote resurrection. Current `TutorialVeterinarian.Resurrect` still lacks a vet-proximity recheck. No code changed here; the guide teaches the intended nearby visit and does not describe the exploit.
- The elixir checks for a dead bonded pet but does not explicitly check ControlMaster. The guide targets the player's own starter pet without claiming an ownership enforcement rule.
- No lane tests, build, or new tests were needed for prose changes. Manually checked the guide against the sources above, local Markdown links, American spelling, absence of em dashes, file sizes, whitespace, and final changed-file scope.
- Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing to these work copies; exit 0. Despite its name, the tool writes `tools/progress.json` from build(). The resulting timestamp and queue-only diff was inspected and restored to the initially clean HEAD bytes to keep this task in notes. No progress-tool fix was attempted.
- No Haven connection, deployment, code change, commit, push, merge, or branch switch.

P559 DONE
