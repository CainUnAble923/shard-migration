# P702: tutorial text for someone who has never played UO

October 27, 2026. Suggestions only. No code, wiki draft, configuration, localization, world data, or file under `docs/` was changed.

The most urgent changes are to explain mouse actions before the farm, explain Young and bonded pets before the death lesson, and distinguish the Wakening Isle from Haven Island. The wiki drafts need their route updated before a newcomer can follow them. A glossary link alone will not help someone stuck in an open lesson window.

## Evidence and reading boundaries

Read both work copies' `AGENTS.md`, `docs/direction-decision.md`, and `docs/tasks.md`. Code snapshot: `ba80ec86de48fa5069d42133761f3e2d096f11eb`. Notes snapshot before this file: `76a0822059aa73456b054f113755330728469736`.

P480 and P609's implementation notes identify the earlier controls, supplies, farm, pet, and wording work. P588's text inventory and P619's review provide earlier proposals and known input problems. P525 and P577 explain the newer Markdown guide. The opening summaries of P276, P289, P290, P291, P453, and P475 supply historical context; their old placement and feature claims do not override today's source.

There is no P663 completion note in this notes checkout. Read its task prompt at `D:/UO/cc-prompts/merging/cc-P663-tutorial-moves-to-isle.md`, including the Siege of Sosaria addendum, then followed its current code. P663's implementation is present here: Tamsin teaches the main lessons on the Wakening Isle, the farm is required, and the dock gate is last. Rook handles graduation and optional lessons in New Haven. This is source availability, not proof of deployment or completed client testing.

Source locations below are relative to `server/customizations/Tutorial/` unless a different root is named. Locations identify the current line, not P588's or P609's older line numbers. Quoted fragments are enough to locate longer strings. Repeated wording is grouped with its other locations; each suggestion applies at each listed occurrence. Internal keys, staff commands, logs, HTML, ordinary item names, and already clear lines do not need rewriting. Technical terms in optional fallback data are included because that page can display them.

Canonical tutorial source inventory reviewed for player text:

```text
ClusterFLoops.cs
ClusterFTutorial.cs
HavenSpots.cs
TutorialCorePlacement.cs
TutorialCoreTrials.cs
TutorialCreature.cs
TutorialFarm.cs
TutorialFarmLayout.cs
TutorialGuide.cs
TutorialGumps.cs
TutorialIslandGate.cs
TutorialIsleFarmLayout.cs
TutorialLoans.cs
TutorialPetCare.cs
TutorialRecruiter.cs
TutorialStart.cs
TutorialStations.cs
TutorialStyle.cs
TutorialTradeTrials.cs
TutorialTrialProgress.cs
TutorialWingTrials.cs
TutorialWorld.cs
```

The layout, style, progress, and map-helper files have no additional explanatory player prose requiring a rewrite. Also followed `CharacterCreation.cs`'s delegation to `TutorialStart.Cities`, the starting-city descriptions in `player-package/vendor/shattered-legacy-cliloc/entries.json`, graduation's `Items/Consumables/ElixirOfRebirth.cs`, and the starter pet's `Mobiles/Evo/EvoPet.cs`. For the elixir's localized messages, the English is from the call-site source comments, not a loaded client localization file. Shared localization changes are not proposed.

Tutorial wiki drafts reviewed, kept distinct because their contents differ:

- **M:** `shard-migration/notes/wiki-drafts/new-player-tutorial.md`.
- **N:** `shard-migration/notes/wiki-drafts/pages/uo/drafts/tutorial.txt`.
- **W:** `ShatteredLegacy/docker/wiki/content/pages/uo/drafts/tutorial.txt`.

M is the fuller October 24 guide. N is an older outline. W has more detail than N but still calls working optional lessons previews. None reflects the current isle route. Line numbers in the wiki tables refer to those exact files.

## A small controls explanation to put before the first lesson

Suggested addition, not existing text:

> Click means press and release the left mouse button once. Double-click means two quick left clicks on the same person or object. To drag an item, hold the left button on it, move it to the destination, then release the button. Hold the right mouse button toward a place to move there, then release it to stop. When an item or spell asks you to choose a target, click the person, object, or ground it should affect.

The current welcome explains double-clicking, but the first required pet fight assumes targeting and the clothing and bank lessons assume dragging. Keep this explanation available from the lesson help. Spellbook labels and world characters do not always react to a single click in the same way; preserve the click count in each instruction.

## Start choice, guides, progress, and leaving

| Source | Current wording or fragment | Why it can stop a newcomer; suggested wording |
|---|---|---|
| `entries.json`, description 1900014 | "then take the moongate to New Haven" | Moongate is unexplained at character creation. "Start with the tutorial (recommended): learn the basics on the Wakening Isle, then use a glowing blue portal to reach New Haven." |
| `TutorialStart.cs:35`, `:62` | "Tutorial Island" / "The Wakening Isle" | Two names for one destination. Keep the selectable name and explain it: "Tutorial Island: the Wakening Isle, where you learn the controls." |
| `TutorialStart.cs:63` | "The Bountiful Harvest Inn" | The inn name does not explain the skip choice. Keep the place name, but retain the adjacent plain description "Skip the tutorial: start in New Haven." |
| `TutorialGuide.cs:22` | "the isle's guide" | Players may not yet connect the place names. "your tutorial guide" |
| `TutorialGuide.cs:56` | "My window shows your lessons; take them in order along the road." | Does not say how to begin. "Choose the lesson marked (next) in this window. Follow its arrow along the road." |
| `TutorialGuide.cs:57` | "The moongate at the end of the dock takes you to New Haven." | "The glowing blue portal at the end of the dock takes you to New Haven. It is called a moongate." |
| `TutorialRecruiter.cs:34` | "the League recruiter" | Rook has a tutorial role distinct from Elara's membership role. "the tutorial guide"; explain League membership on Elara's page. |
| `TutorialGumps.cs:55-57` | "Thieving and stealth", "Shard features", fallback heading "Bard" | "Stealing and moving unseen", "This server's extra features", and "Music skills". Shard means game server to veterans; bard means a musician using music skills. Keep the exact skill names in the lesson checklist. |
| `TutorialGumps.cs:144` | "Rook in New Haven graduates you and opens trade and skill lessons." | Implies graduation opens lessons. The active-state menu at `:75-77` stops offering them after graduation. "The blue portal on the dock is your last main lesson. In New Haven, Rook offers optional lessons before you choose Graduate." |
| `TutorialGumps.cs:145` | "Finish the main lessons to open trade and skill lessons." | Name the person and timing. "Finish the main lessons, then visit Rook in New Haven for optional lessons before you graduate." |
| `TutorialGumps.cs:166`; `ClusterFTutorial.cs:257` | "Graduate" / "Double-click Rook to graduate or try an optional lesson." | Explain that this finishes the tutorial, and optional lessons come first. Button suggestion: "Graduate: finish the tutorial". Message: "You finished the main lessons. Double-click Rook in New Haven to try optional lessons or choose Graduate to finish the tutorial." |
| `TutorialGumps.cs:279` | "Skip the remaining tutorial lessons?" | Explain the practical cost before confirmation. "Skip the remaining lessons and leave the tutorial? Skipping does not give the graduation reward box or pet choice; Rook in New Haven lets you return for the lessons and rewards later." |
| `TutorialGumps.cs:280` | "Skipping earns the Didn't Read the Manual achievement." | Achievement is a named progress award, not a manual to find. "Skipping records a progress award called Didn't Read the Manual. Skip now?" |
| `ClusterFTutorial.cs:281` | "You can now leave Haven Island. Your Young protection continues until its time runs out." | Haven Island is not the Wakening Isle; Young is unexplained. "You now start in New Haven and may travel beyond its island. Your account's remaining newcomer protection, called Young status, continues." |
| `ClusterFTutorial.cs:285` | "Finish the main lessons and graduate to leave Haven Island." | Explain both guides. "Ask Rook in New Haven to send you to Tamsin's lessons on the Wakening Isle. Finish them and return to Rook to graduate before traveling beyond New Haven's island." |
| `ClusterFTutorial.cs:309` | "its usual rewards ... the moongate on its dock brings you back" | "Rook is sending you to the Wakening Isle to restart the lessons and earn the tutorial rewards. The blue portal on the dock brings you back to New Haven after the main lessons." |
| `ClusterFTutorial.cs:374` | "Finish the main lessons listed in Rook's window before you graduate." | Rook redirects to Tamsin. "Finish Tamsin's main lessons on the Wakening Isle, then return to Rook in New Haven to finish the tutorial." |
| `ClusterFTutorial.cs:391`, both graduation variants | "You can now leave Haven Island." | "You finished the tutorial and may now travel beyond New Haven's island." Keep the returning-player acknowledgment if desired. |
| `TutorialIslandGate.cs:14` | "Finish the main tutorial lessons, then double-click Rook ... You can leave Haven Island afterward." | The refusal may appear on either island. "Finish Tamsin's main lessons on the Wakening Isle, then take the dock's blue portal to New Haven. Double-click Rook on the plaza and choose Graduate to unlock travel beyond New Haven's island." |
| `TutorialCoreTrials.cs:298-299` | "Next lesson / graduate" | Mixed action names hide that the button advances or points back to Rook. "Continue"; accompanying text: "Click Continue for the next step. After the last main lesson, return to Rook in New Haven to graduate." Rename the button and its quoted instructions together in any later implementation. |
| `TutorialGumps.cs:350-356` | "Go to", "Practice", "Related skills", "Learn about", "Lesson supplies" | The distinctions matter only on fallback pages. "Where to go", "Skills you practice", "Other skills used here", "Topics explained here", "Items lent for this lesson". Keep the clear unavailable-activity sentence. |

The existing "Click", "Double-click", "Restart this lesson", "Hint and arrow", and character-ownership messages are otherwise plain once the initial controls explanation is present. Do not replace the actual achievement names merely because their jokes need explanation.

**Skip route checked in source:** `ClusterFTutorial.Skip` calls `TutorialStart.SendHome` before its messages, so a skipper on the isle is sent directly to New Haven with pets. A skip explanation should describe that trip rather than sending the player to the dock for unfinished lessons. This path was read, not exercised in a client.

## Main lesson instructions and the vision

| Source | Current wording or fragment | Suggested wording |
|---|---|---|
| `TutorialCoreTrials.cs:53` | "Hold the right mouse button toward the glowing blue floor tile ... Point farther ... to run." | "Put your mouse pointer on the glowing blue floor tile in the road and hold the right mouse button to move toward it. Release the button to stop, then do the same for the gold tile; holding the pointer farther from your character makes you run." |
| `TutorialCoreTrials.cs:54` | "character window ... its backpack picture" | Name the old term once so other help makes sense. "Follow the arrow to the roadside camp. Double-click your character to open the character window, also called the paperdoll; double-click its backpack picture, then double-click the blue practice bag inside." |
| `TutorialCoreTrials.cs:55` | "drag the blue practice cloak ... onto your character's picture" | "At the clothes rack, open your character window and backpack. Hold the left mouse button on the blue practice cloak, move it onto your character's picture, then release it; if you already wear a cloak, move that cloak into your backpack first." |
| `TutorialCoreTrials.cs:56` | "The Journal records what you say." | "At the signpost, press Enter, type 'I am ready to learn', then press Enter again. The Journal is a window that keeps spoken messages so you can read them again." Add a verified way to open it, rather than assuming the player can find it. |
| `TutorialCoreTrials.cs:57` | "Choose your pet, clear the pests ... then heal with a bandage." | "Follow the arrow to Wren, the farmer in a straw hat at the gate, and double-click Wren. Wren will guide you through choosing a pet, fighting pests, and using a bandage to restore health." |
| `TutorialCoreTrials.cs:58` | "After you die ... click Resurrect" | "Double-click the pale gray rat in the training yard and click Ready to begin a lesson that kills your character. As a ghost, double-click Sera beside the rat and click Resurrect, which brings you back to life." |
| `TutorialCorePlacement.cs:338` | "While you are Young, your belongings return to your backpack after death." | "Click Ready when you want the rat to kill your character for this lesson. Your character becomes a ghost; double-click Sera beside the rat and click Resurrect to return to life. While your account has newcomer protection, called Young status, your belongings return to your backpack after death." Avoid suggesting this remains true after Young ends. |
| `TutorialCorePlacement.cs:378`; `TutorialCoreTrials.cs:104`, `:266` | "Resurrect" / "return to life" | Keep the actual button name and define it beside it: "Click Resurrect to bring your character back to life." A label-only alternative is "Resurrect: return to life". |
| `TutorialCoreTrials.cs:59` | "through the practice bank's door ... say 'bank' ... Drag ... into that box" | "At the practice bank in the trades square, double-click the door to open it and stand near Merrin the banker. Press Enter, type bank, then press Enter again to open your bank storage; drag the small blue practice coins from your backpack into that window." |
| `TutorialCoreTrials.cs:60` | "League lodge ... read about the League without joining" | "At the League lodge, double-click the north door to enter, then double-click Elara Voss. The League offers jobs and rewards; reading Elara's page finishes this lesson without making you join." |
| `TutorialCoreTrials.cs:61`, `:231` | "knoll", "bright blue rune stone", "vision" | "Follow the arrow up the small hill to the standing stones and double-click the bright blue stone. Stay beside it to watch a short story scene; it does not change your character." Restart reminder: "Stay beside the blue stone until the scene ends. Double-click it to start the scene again." |
| `TutorialCoreTrials.cs:62` | "shimmering blue moongate" | "At the end of the dock, walk into the glowing blue portal, called a moongate, or double-click it. It takes you and your pets to Rook on New Haven's town plaza." |
| `TutorialCorePlacement.cs:241`, `:243` | "moongate to New Haven" | "blue portal to New Haven (moongate)" |
| `ClusterFLoops.cs:72` | "your level and skills reset ... future loop system" | "This story shows a planned way to start another journey, called a loop. In the story, your character's level and learned abilities return to the beginning; this reset system is not available yet." |
| `ClusterFLoops.cs:73` | "League progress, recipes, achievements, and guild ranks remain. Your companion stays ..." | "In this story, you keep your League progress, learned crafting instructions, progress awards, group ranks, and pet. Those are the things the planned loop system would carry into another journey." This explains the terms without promising that the planned reset already works. |
| `TutorialStations.cs:78` | "Watch a loop vision" | "Watch a story about starting another journey"; introduce the name loop in the scene. |
| `TutorialCoreTrials.cs:91`, `:132` | "Make room in your backpack" | "Your backpack is full. Move some items to your bank, then click Hint and arrow for a replacement practice item." For `:132`, keep the actual recovery action: "...then choose this lesson again in Tamsin's window." Do not tell players to drop valuable belongings. |

## Farm, pet choice, bandages, and pet death

| Source | Current wording or fragment | Suggested wording |
|---|---|---|
| `TutorialFarm.cs:101` | "your one tutorial pet" | "Choose a dog or cat to keep. Your account gets one tutorial pet, shared between this farm choice and the graduation choice." The required farm currently offers only dog or cat; do not promise a new trainee can simply save this choice for a fox or bird and still finish the main route. |
| `TutorialFarm.cs:102`; `TutorialGumps.cs:436` | "Stable one of your pets with an animal trainer" | "You are already using your available pet capacity. An animal trainer can look after one of your pets in a stable; leave a pet there, then return to choose this one." In the graduation message, finish with "ask Rook again." Verify a reachable trainer before sending an isle trainee away. |
| `TutorialFarm.cs:103` | "say 'all kill', then click a rat or grass snake" | "In the cabbage rows, press Enter, type all kill, then press Enter again to command your pets. When the game asks for a target, left-click a rat or grass snake; defeat {0} pests to finish." |
| `TutorialFarm.cs:104` | "Defeat {0} more rats or grass snakes" | "Defeat {0} more rats or grass snakes in the cabbage rows. To send your pets to attack, say all kill and click a pest when asked for a target." |
| `TutorialFarm.cs:105`; `TutorialWingTrials.cs:163`, `:610`, `:682` | "click yourself or an injured pet. A successful heal ..." | "Double-click a bandage in your backpack, then left-click yourself or an injured pet when asked for a target. Wait for the treatment to finish; this step counts when the bandage restores health." In the optional lesson, preserve its requirement to heal both yourself and the wounded villager. |
| `TutorialFarm.cs:106` | "buy more from a healer in town" | "Your account has used its free bandage allowance. Buy more bandages from a healer who sells supplies in New Haven." This is not proof that Sera sells them or that an isle trainee can reach that shop mid-lesson. Resolve access before publishing this instruction. |
| `TutorialFarm.cs:107` | "Your backpack is too full ... Make room" | "Your backpack has no room for the bandages. Put some items in bank storage, then double-click Wren again." |
| `TutorialFarm.cs:108` | "If your bonded pet dies, bring its ghost to Tobin the vet" | "You finished the farm lessons. Your pet is bonded, which lets it return as a ghost after death; once its body disappears, bring the ghost to Tobin beside Wren to restore it to life." |
| `TutorialFarm.cs:109` | "Say 'all follow me'" | "This pet is yours to keep. Press Enter, type all follow me, then press Enter again to call your pets to follow you." |
| `TutorialFarm.cs:152`, `:153` | "bring its ghost to ... the vet by the New Haven stables" | Isle version: "Wait for your pet's body to disappear, then say all follow me to bring its ghost to Tobin beside Wren. Double-click Tobin to ask for help." Haven version: "...bring its ghost to the veterinarian by the New Haven stables, where animal trainers keep pets." Do not conflate the two destinations. |
| `TutorialPetCare.cs:47`; `ClusterFTutorial.cs:357` | "take its ghost to a vet or use an elixir of rebirth" | "After your dead pet's body disappears, bring its ghost to Tobin the veterinarian beside Wren. You can also use an elixir of rebirth, a potion that brings a bonded pet back to life; your graduation reward box contains one." Keep the reward sentence only at graduation. |
| `TutorialPetCare.cs:63` | "It loses 0.2 points in every skill." | "Choose the pet to bring back to life. Its trained abilities each drop by 0.2 skill points." |
| `TutorialPetCare.cs:69` | "free while you are Young" | "free while your account has Young newcomer protection" |
| `TutorialPetCare.cs:69` | "{fee} gold from your bank" | "cost: {fee} gold, paid from your bank storage" |
| `TutorialPetCare.cs:222` | "Brings a bonded pet back after its body disappears" | "Brings your bonded pet back to life after its body disappears. Keep this potion in your backpack, double-click it, then click the pet's ghost." |
| `TutorialGumps.cs:401` | "A dog companion ... grows ... as you play together" | "A puppy you keep as a pet. It can grow into a larger hound by fighting creatures." Pet experience comes from fights it damages, not simply time together (`Mobiles/Evo/EvoPet.cs:238-256`). |
| `TutorialGumps.cs:402` | "A cat companion ... as you play together" | "A kitten you keep as a pet. It can grow into larger cats by fighting creatures." |
| `TutorialGumps.cs:403` | "fox kit ... After graduation and enough growth ... bake kitsune" | "A young fox you keep as a pet. A magical fox form is planned, but later forms still have unfinished requirements." The existing phrase defines bake kitsune but promises a usable graduation gate that the earlier notes explicitly leave unfinished. |
| `TutorialGumps.cs:404` | "A bird companion ... firebird; more stages ..." | "A young bird you keep as a pet. It can grow into a firebird; later growth stages are still being added." |
| `TutorialGumps.cs:413` | "Your pet grows as you play" | "Your pet gains experience by helping fight creatures. It is bonded to you, so it can return as a ghost and be brought back to life if it dies." |
| `TutorialLoans.cs:37` | "lent for the lesson's sewing" | "Use this borrowed cloth to make the lesson's skullcap. You cannot cut this practice cloth with scissors." |
| `TutorialLoans.cs:55` | "lent for the lesson's fletching" | "Use these borrowed logs to make kindling in the bow-making lesson. You cannot cut these practice logs into boards." |
| `Items/Consumables/ElixirOfRebirth.cs:17` | "elixir of rebirth" | Keep the item name. Suggested explanatory text: "A potion that brings a bonded pet back to life once its body disappears." |
| `Items/Consumables/ElixirOfRebirth.cs:28` | "Which pet do you wish to revive?" | "Click the ghost of the pet you want to bring back to life." |
| `Items/Consumables/ElixirOfRebirth.cs:46`, `:52`, `:68` | "This may only be used to resurrect dead pets." | "This potion works on the ghost of a bonded pet. Click the pet's ghost after its body disappears." |
| `Items/Consumables/ElixirOfRebirth.cs:56` | "That creature's spirit lacks cohesion. Try again in a few minutes." | "Your pet's body is still here. Wait for it to disappear, then use the potion on the pet's ghost again." |
| `Items/Consumables/ElixirOfRebirth.cs:60` | "Target is not close enough." | "Stand within two steps of your pet's ghost, then try again." |
| `Items/Consumables/ElixirOfRebirth.cs:64` | "The resurrecter must be alive." | "You must bring your own character back to life before using this potion." |
| `Items/Consumables/ElixirOfRebirth.cs:72` | "Target can not be resurrected at that location." | "Your pet cannot return to life in that spot. Move its ghost to clear ground and try again." The code uses message ID 501042 for both range and blocked location, so the comment text is not proof the client displays this particular sentence. A later change should use call-site wording if the two errors need different advice. |

## Combat and magic

Keep the skill and spell names that players must find in their menus. Explain what they do rather than replacing every name with a different label.

| Source | Current wording or fragment | Suggested wording |
|---|---|---|
| `TutorialWingTrials.cs:42-43` | "tutorial loan" / "tutorial loaner:" | "borrowed for this lesson" / "borrowed: "; do not change the internal skill-mod name as part of a later prose edit. |
| `TutorialWingTrials.cs:69` | "Macing: a mace" | "Macing: fight with a mace, a heavy club" |
| `TutorialWingTrials.cs:70` | "Fencing: a narrow kryss sword" | "Fencing: fight with a narrow sword called a kryss" |
| `TutorialWingTrials.cs:72` | "Throwing: a boomerang for gargoyles" | "Throwing: a boomerang, usable only by characters of the gargoyle race" |
| `TutorialWingTrials.cs:462-463`, supply labels | "buckler", "kryss", "katana" | Keep the item names, with a first-use gloss where they are introduced: "buckler, a small shield"; "kryss, a narrow thrusting sword"; "katana, a curved sword". These are not three additional skills. |
| `TutorialWingTrials.cs:77` | "Resisting Spells ... resist some spell effects" | "Resisting Spells is a skill that helps protect you from some magic effects. It can improve when certain spells are cast on you; this lesson does not practice it." |
| `TutorialWingTrials.cs:79` | "Spellweaving starts with a quest ... Heartwood ... Patience" | "Spellweaving is another kind of magic. To begin learning it later, visit Heartwood and find the quest named Patience, a task offered by a game character." Add directions in a later guide rather than making this a task during the current lesson. |
| `TutorialWingTrials.cs:159` | "blue human figure named 'a sparring echo'" | "Choose a borrowed weapon below. The blue figure named a sparring echo is your practice opponent; hit it three times with that weapon, or use empty hands for Wrestling." |
| `TutorialWingTrials.cs:161` | "Press Tab to enter war mode ... {Weapons[choice].Skill}" | "Open your character window and drag the borrowed weapon onto your character's picture, or remove both hand items for Wrestling. Turn on war mode, which makes double-clicking a creature attack it, then double-click the blue sparring echo and land three hits using {Weapons[choice].Skill}." Add: "With the usual toggle setting, Tab switches war mode on or off; check your controls if Tab is set differently." |
| `TutorialWingTrials.cs:165` | "double-click Magic Arrow, then click ... sulfurous ash" | "In your backpack, double-click the borrowed spellbook, then double-click Magic Arrow. When the spell asks for a target, left-click the blue training echo; the lesson provides sulfurous ash, the spell ingredient it uses." |
| `TutorialWingTrials.cs:167` | "Pain Spike ... grave dust and pig iron" | "Open the borrowed Necromancy spellbook and double-click Pain Spike. When asked for a target, click the blue training echo; the lesson provides the grave dust and pig iron spell ingredients." |
| `TutorialWingTrials.cs:169` | "Close Wounds ... tithing points" | "Stand within two steps of the wounded villager, open the borrowed Book of Chivalry, and double-click Close Wounds. Click the villager when asked for a target; the lesson supplies tithing points, the credit this kind of magic spends." |
| `TutorialWingTrials.cs:171` | "click Honorable Execution. Press Tab for war mode" | "Equip the borrowed katana by dragging it onto your character's picture in the character window. Open the Book of Bushido and double-click Honorable Execution to prepare that special attack, then turn war mode on if needed and double-click the blue training echo." Apply the conditional Tab explanation above. |
| `TutorialWingTrials.cs:173` | "click Focus Attack. Press Tab for war mode" | "Equip the borrowed katana and open the Book of Ninjitsu. Double-click Focus Attack to prepare that special attack, then turn war mode on if needed and double-click the blue training echo." |
| `TutorialWingTrials.cs:175` | "Eagle Strike ... bloodmoss, bone, spider's silk, and mandrake root" | "Open the borrowed Mysticism spellbook and double-click Eagle Strike. Click the blue training echo when asked for a target; the lesson supplies the bloodmoss, bone, spider's silk, and mandrake root spell ingredients." |
| `TutorialWingTrials.cs:186` | "Sera the healer at the farm gate" | Sera moved to the isle yard in the main route; optional lessons stay in New Haven. Suggested safe placeholder: "You must return to life before starting this lesson. Visit a healer and choose Resurrect." Supply a verified reachable healer and arrow before publishing a precise destination. |
| `TutorialWingTrials.cs:321`; `TutorialTradeTrials.cs:440` | "Keep the loaned supplies with you in this lesson area." | "These borrowed items work only during this lesson. Keep them in your backpack or equipped; they disappear when the lesson ends, you leave its area, or you log out." |
| `TutorialWingTrials.cs:404` | "Your backpack has no room ... starts again by itself" | "Your backpack is full. Store some of your own items in the bank, then return to the lesson area; the lesson will try to give you supplies again." Verify the player's current area before changing the existing automatic-retry promise. |
| `TutorialWingTrials.cs:575` | "Keep lesson supplies equipped" | "Keep borrowed items in your backpack or worn on your character. Moving them onto the ground, into the bank, or to another person makes them disappear." |
| `TutorialWingTrials.cs:705` | "Double-click Rook to choose another lesson." | "This lesson is finished and its borrowed supplies have been removed. Return to peace mode before double-clicking Rook in New Haven to choose another lesson." |
| `TutorialWingTrials.cs:755` | "Lesson stopped ... Double-click Rook" | "This lesson stopped and its borrowed supplies were removed. Return to peace mode before double-clicking Rook to choose another lesson." |
| `TutorialWingTrials.cs:728` | "Back to Rook" | "Show the way to Rook" if the action points rather than transports. Preserve the actual behavior; do not imply a teleport. |

The single-click spell-move and unconditional Tab problems were already reported in P619. They still occur in these current strings, so this pass keeps them on the rewrite list. The local TazUO source confirms Tab can toggle or be held (`Game/Scenes/GameSceneInputHandler.cs`, `HoldDownKeyTab`; `Game/GameActions.cs:32` toggles the current mode). The published client's bindings and behavior were not exercised.

## Gathering, crafting, animal, music, and thieving lessons

The first use of Skills needs this short introduction: "Double-click your character, then click Skills to open the list of abilities. For an ability you can activate, use its action button, then click the requested target." The exact action-button appearance needs a check in the player client. Passive abilities do not all have an action button.

| Source | Current wording or fragment | Suggested wording |
|---|---|---|
| `TutorialTradeTrials.cs:72` | "Imbuing ... at a soul forge" | "Imbuing is a crafting skill that adds magical properties to equipment at a special workstation called a soul forge. This lesson does not practice it." Do not imply the player has learned the process from this sentence. |
| `TutorialTradeTrials.cs:74` | "Forensic Evaluation ... who looted a body" | "Forensic Evaluation is a skill for examining bodies and locks. It can reveal who took items from a body or picked a lock; this lesson has no practice task for it." |
| `TutorialTradeTrials.cs:80-81`; `:311` | "dig ore", "practice vein" | Checklist: "Mining: dig metal-bearing rock from the gray stone patch". Hint: "Double-click the borrowed pickaxe, then click the gray stone patch labeled practice vein when asked for a target. Try again until you collect ore, rock containing metal that you can keep." Prop name suggestion: "practice ore deposit"; update hint and label together. |
| `TutorialTradeTrials.cs:84` | "click the walnut tree beside you" | "Double-click the borrowed hatchet, then click the tree labeled practice tree when asked for a target. Repeat until you collect logs to keep." The displayed prop name is practice tree, not walnut tree (`:317-318`). |
| `TutorialTradeTrials.cs:87` | "click the water ... catch something" | "Double-click the borrowed fishing pole, then click the small practice pond when asked for a target. Repeat until you catch something to keep." |
| `TutorialTradeTrials.cs:70`, `:89-90` | "kindling" | "Herbalism is not available yet. Double-click the borrowed kindling, small pieces of wood in your backpack, to light a campfire." Checklist: "Camping: light a fire with small pieces of wood called kindling". |
| `TutorialTradeTrials.cs:95` | "Arms Lore: use on the dagger you made" | "Arms Lore: inspect the dagger you made using the skill of that name" |
| `TutorialTradeTrials.cs:96` | "choose Bladed, then make a Dagger ... use Arms Lore" | "Beside the anvil and forge, double-click the borrowed smith's hammer to open the crafting menu; choose Bladed, then the action to make a Dagger. Open Skills, activate Arms Lore, then click your dagger when asked for a target." |
| `TutorialTradeTrials.cs:99-100` | "Tailoring ... skullcap" | "Tailoring: sew a close-fitting cap called a skullcap". Hint: "Double-click the borrowed sewing kit to open its crafting menu. Choose Hats, then make a Skullcap using the borrowed cloth." |
| `TutorialTradeTrials.cs:103-104` | "barrel staves" | "Carpentry: make the wooden strips used for a barrel, called barrel staves". Hint: "Double-click the borrowed saw, choose Other in its crafting menu, then make Barrel Staves with the borrowed boards." |
| `TutorialTradeTrials.cs:107-108` | "Item Identification ... odd blue curio" | "Double-click the borrowed tinker's tools, choose Tools, then make Scissors. Open Skills, activate Item Identification to examine an item, then click the odd blue object in your backpack when asked for a target." Checklist: "Item Identification: examine the odd blue object". |
| `TutorialTradeTrials.cs:111-112` | "refresh potion ... Taste Identification" | "Double-click the borrowed mortar and pestle to open its crafting menu, choose Refresh, then make a Refresh Potion. Open Skills, activate Taste Identification, then click the borrowed apple when asked for a target." Checklist: "Taste Identification: examine the borrowed apple with this skill". Keep Refresh Potion as the recipe name; do not imply it heals health. |
| `TutorialTradeTrials.cs:115-116`; `TutorialStations.cs:127` | "Fletching" / "Bowcraft and Fletching" | Title: "Bowcraft and Fletching: making bows and arrows". Checklist: "Fletching: make kindling, small pieces of wood for a fire". Hint: "Double-click the borrowed fletcher's tools, the tools for making bows and arrows. Choose Materials, then make Kindling with the borrowed logs." |
| `TutorialTradeTrials.cs:120` | "skillet ... Ingredients ... Dough" | "Double-click the borrowed skillet, a cooking pan, to open its crafting menu. Choose Ingredients, then make Dough using the borrowed flour and water." |
| `TutorialTradeTrials.cs:123-124` | "Inscription", "First Circle", "Magic Arrow scroll" | "Inscription: write a spell on a scroll". Hint: "Double-click the borrowed scribe's pen to open its crafting menu. Choose First Circle, the first group of spells, then make a Magic Arrow scroll with the borrowed supplies." |
| `TutorialTradeTrials.cs:127-128`; `TutorialStations.cs:133` | "Cartography" / "Local Map" | Title: "Cartography: drawing maps". Hint: "Double-click the borrowed mapmaker's pen to open its crafting menu. Choose Maps, then make a Local Map using a borrowed blank map." |
| `TutorialTradeTrials.cs:134` | "use the crook on the goat, then click a spot" | "Herding: double-click the borrowed shepherd's crook, click the practice goat, then click the ground where it should go" |
| `TutorialTradeTrials.cs:135` | "Animal Taming: use on the practice goat" | "Animal Taming: activate this skill in Skills, then click the practice goat to try to make it follow your commands" |
| `TutorialTradeTrials.cs:136` | "Animal Lore: use on your goat or gain it while taming" | "Animal Lore: activate this skill and click your goat to examine it; improving the skill while taming also counts" |
| `TutorialTradeTrials.cs:137` | "Veterinary: double-click a bandage, then your goat" | "Veterinary: double-click a bandage, then click your injured goat once and wait for treatment" |
| `TutorialTradeTrials.cs:139` | "Use Animal Taming and Animal Lore from Skills, then bandage the goat; it stays at the farm." | "Use the borrowed crook to send the practice goat to a spot on the ground. In Skills, activate Animal Taming and target the goat, then activate Animal Lore and target it; use a bandage to treat it, but remember that this practice goat stays at the farm." |
| `TutorialTradeTrials.cs:144` | "Peacemaking: use on a blue training echo" | "Peacemaking: use this music skill on a blue practice figure to calm it" |
| `TutorialTradeTrials.cs:145` | "Provocation: use on one echo, then the other" | "Provocation: use this music skill to make one blue practice figure attack the other; click the first, then the second when asked" |
| `TutorialTradeTrials.cs:146` | "Discordance: use on a blue training echo" | "Discordance: use this music skill on a blue practice figure to weaken it" |
| `TutorialTradeTrials.cs:148` | "Choose the loaned lute when asked" | "In Skills, activate Peacemaking, Provocation, and Discordance for the checklist tasks. If asked to choose an instrument, click the borrowed lute in your backpack; Provocation then asks you to click one blue practice figure and the other." Explain that a lute is the borrowed musical instrument. |
| `TutorialStations.cs:141` | "Music and bard skills" | "Music: calm, provoke, and weaken creatures". Keep Peacemaking, Provocation, and Discordance as the exact skill names in the checklist. |
| `TutorialTradeTrials.cs:153` | "Detecting Hidden: use on the wooden practice chest" | "Detecting Hidden: activate this skill, then click the wooden practice chest to search for a trap" |
| `TutorialTradeTrials.cs:154` | "Remove Trap: use on the wooden practice chest" | "Remove Trap: activate this skill, then click the wooden practice chest to disable its trap" |
| `TutorialTradeTrials.cs:155` | "Lockpicking: use a loaned lockpick on the chest" | "Lockpicking: double-click a borrowed lockpick, then click the wooden practice chest to unlock it" |
| `TutorialTradeTrials.cs:156` | "Stealing: empty your hands and steal the purse" | "Stealing: open the unlocked wooden practice chest, move both hand items into your backpack, then activate Stealing and click the purse inside the chest" |
| `TutorialTradeTrials.cs:157` | "Snooping: double-click the mark's backpack" | "Snooping: double-click the blue practice person to open its character window, then double-click its backpack to look inside" |
| `TutorialTradeTrials.cs:158` | "Begging: use on the blue practice person" | "Begging: activate this skill, then click the blue practice person to ask for money" |
| `TutorialTradeTrials.cs:159` | "Poisoning: select the loaned poison, then the dagger" | "Poisoning: activate this skill, click the borrowed poison potion, then click the borrowed dagger when asked" |
| `TutorialTradeTrials.cs:160` | "Tracking: use the skill and choose a category" | "Tracking: activate this skill and choose which kind of creature to search for" |
| `TutorialTradeTrials.cs:161` | "Hiding: use the skill until you hide" | "Hiding: activate this skill to try to become hidden from view; try again if it fails" |
| `TutorialTradeTrials.cs:162` | "Stealth: hide, then use Stealth" | "Stealth: use Hiding first, then activate Stealth to try moving while hidden" |
| `TutorialTradeTrials.cs:164` | "snooping and poisoning can lower your karma" | "Use the Skills window for these practice tasks on the wooden chest and blue practice person. Snooping means looking inside someone else's backpack; Snooping and Poisoning can lower karma, your character's good-or-bad reputation score, even in this lesson." |
| `TutorialTradeTrials.cs:272` | "recall rune" | "recall rune, a stone that can store a travel destination" |
| `TutorialTradeTrials.cs:273`, `:624` | "odd curio", "a brass curio with no value", "unidentified" | "odd blue object"; after examination, "a brass object with no value"; before examination, "an odd blue object (not yet examined)". If changing the label, update the identification checklist and hint too. |
| `TutorialTradeTrials.cs:470` | "a tutorial mark" | "a practice person for the thieving lesson". Mark means a target of theft to veterans. |
| `TutorialTradeTrials.cs:471`, `:480` | "tutorial prop: a brass trinket", "a purse of glass coins" | Prefix suggestion: "practice item:". Keep the purse and trinket names, but say which is in the chest and which is in the practice person's backpack; they are different targets. |

The menu categories and product names above should keep their exact capitalization so a player can match them to crafting menus. A later implementation should verify each make-action button in the client rather than guessing that clicking a recipe name always makes it.

## Housing, travel, reputation, and server-feature tours

| Source | Current wording or fragment | Suggested wording |
|---|---|---|
| `TutorialTradeTrials.cs:174` | "Use a house deed ... lock items in place and secure containers" | "A house deed is an item for placing a house on land where building is allowed. House controls can keep furnishings in place and protect storage containers; this tour does not practice those controls." Put the optional roof setting in a separate help line: "TazUO's Options can make roofs and walls transparent so you can see inside." Verify the actual housing placement and upkeep rules before presenting this tour as a housing guide. |
| `TutorialTradeTrials.cs:176` | "refresh it and prevent decay" | "Keep a house deed safe in your bank until you are ready to use it. Houses can fall apart if their upkeep rules are not met; check the housing guide for the rules for your house." Do not promise that visiting alone refreshes every house without checking the housing system. |
| `TutorialTradeTrials.cs:180` | "blank recall rune ... is a loan" | "Follow the arrow to each stop and read the travel lesson there. The borrowed stone called a recall rune can store a travel destination, but this tour only explains it and takes it back afterward." |
| `TutorialTradeTrials.cs:185` | "public moongate ... Shipwrights ... boat deeds" | "This public moongate is a portal with a choice of destinations; the tutorial isle's portal goes only to Rook in New Haven. Boat builders, called shipwrights, sell deeds used to place boats for sea travel." |
| `TutorialTradeTrials.cs:187` | "cast Mark ... Recall, Gate Travel, or Sacred Journey; a runebook stores up to 16 runes" | "A recall rune is a stone that remembers a place when you cast the Mark spell on it. Recall and Sacred Journey are travel spells that can take you back, and Gate Travel opens a portal; a runebook holds up to 16 marked runes." A separate practice or linked guide is needed for opening the book, charges, ingredients, costs, and travel restrictions. |
| `TutorialTradeTrials.cs:195` | "Blue names usually mean innocent; gray names can be attacked ..." | "A name's color can show a character's legal status: blue usually means innocent, gray can mean a legal attack target, and red marks a murderer. The area's combat rules still apply; harming an innocent can temporarily turn your name gray." Do not teach color alone as permission to attack everywhere. |
| `TutorialTradeTrials.cs:197` | "Karma and fame affect your title ... Five murder counts ..." | "Karma measures good-or-bad reputation, while fame measures renown; both affect the title shown with your name. Killing innocent players can add murder counts, a record of unlawful kills; five make your name red, and some healers refuse murderers." Verify thresholds and which counters matter before expanding this into a rules guide. |
| `TutorialTradeTrials.cs:199` | "say 'guards' ... Trammel ... Felucca" | "In a guarded town, press Enter, type guards, then press Enter again to call for help against an unlawful attack. Trammel and Felucca are different world maps: Trammel usually blocks attacks on other players, while Felucca permits them." This does not promise protection from every threat or in every town. |
| `TutorialTradeTrials.cs:209` | "reward boxes ... guarded towns ... Autoloot, Scavenger, Nearby loot" | "Double-click a reward box in a town protected by guards or a house where you have permission to open it. TazUO, your game client, also offers tools for collecting loot and shopping; those tools are optional and need their own setup instructions." Verify the precise house-permission rule before changing the existing own-house wording. |
| `TutorialTradeTrials.cs:211` | "type [accessories ... first loop ... higher level caps" | "Achievements are progress awards. Press Enter, type [accessories including the opening bracket, then press Enter again to view extra jewelry slots; graduation records your first loop, but the planned level resets and higher level limits are not active yet." This is the whole command, not a missing closing bracket. |
| `ClusterFTutorial.cs:411` | "These boxes open only in guarded towns or your own house." | "Double-click your reward box here in New Haven to open it. Reward boxes open in towns protected by guards or in houses where you have the required permission." Do not expand permissions solely from this tutorial string; confirm the box-opening code. |

## Optional fallback skill names and client feature lists

`TutorialStationGump` displays station data as text at `TutorialGumps.cs:351-355`. Even if all current lessons have handlers, fallback text should explain these labels when it is used. These are display suggestions, not requests to rename enums, keys, skills, or client settings.

| Data location in `TutorialStations.cs` | Current terms | Suggested display or first-use explanation |
|---|---|---|
| `:63` | "Options", "Global Scaling", "Hotkeys" | "Options (game settings), Global Scaling (change the size of the interface), Hotkeys (keys assigned to actions)" |
| `:65`, `:75` | "Grid Containers", "Item comparison" | "Grid Containers (show stored items in a grid), Item comparison (compare equipment)" |
| `:67` | "Alternate Paperdoll", "Durability gump" | "Alternate Paperdoll (another layout for your character window), Durability gump (a window showing equipment wear)". Prefer "equipment durability window" in prose. |
| `:69` | "Journal and filters", "TTF fonts", "Nameplates" | "Journal and filters (read messages and choose which kinds to show), TTF fonts (another text style), Nameplates (labels above characters)" |
| `:71`, `:138` | "Pet scaling", "Follow mode" | "Pet scaling (change how large pets look), Follow mode (a client movement aid)". Verify how Follow mode is enabled and behaves before recommending it; it is different from the spoken pet command all follow me. |
| `:73` | "Info Bar" | "Info Bar (a display of character information)" |
| `:79`, `:157` | "Skill progress bar" | "Skill progress bar (watch a skill's progress)" |
| `:81` | "World Map", "Macros" | "World Map (view where you are), Macros (saved sequences of actions)" |
| `:85` | "Swords", "Macing", "Fencing", "Archery", "Throwing", "Wrestling" | "Swords (sword fighting), Macing (clubs and maces), Fencing (thrusting weapons), Archery (bows), Throwing (thrown weapons), Wrestling (empty-hand fighting)" |
| `:85`, `:89` | "Tactics", "Anatomy", "Parrying", "Focus" | "Tactics (combat technique), Anatomy (knowledge of bodies), Parrying (blocking attacks), Focus (helps recovery of mana and stamina)". Use as basic orientation, not a formula or training guarantee. |
| `:86` | "Resisting Spells" | "Resisting Spells (protection against some spell effects)" |
| `:87` | "Custom health bars", "Nameplate healthbars", "Damage hues", "Buff and cooldown bars" | "Custom health bars (choose how health is shown), Nameplate healthbars (health above characters), Damage hues (colors for damage numbers), Buff and cooldown bars (show temporary effects and time before actions are ready)" |
| `:90` | "Auto Bandage" | "Auto Bandage (a client tool for using bandages automatically)". Do not make this a prerequisite for learning manual bandaging. |
| `:93` | "Magery", "Meditation", "Evaluating Intelligence" | "Magery (spellcasting), Meditation (recovering mana used by magic), Evaluating Intelligence (a skill used with Magery)" |
| `:94` | "SpellBar", "Quick spell cast", "Spell indicators", "Counter bar" | "SpellBar (shortcuts to spells), Quick spell cast (a casting shortcut), Spell indicators (visual spell cues), Counter bar (counts chosen supplies)" |
| `:95` | "Necromancy", "Spirit Speak" | "Necromancy (death-related magic), Spirit Speak (a skill used with Necromancy)" |
| `:97` | "Chivalry" | "Chivalry (holy magic using tithing points)" |
| `:99`, `:101` | "Bushido", "Ninjitsu" | "Bushido (samurai combat skills), Ninjitsu (ninja combat skills)" |
| `:103` | "Mysticism", "Spellweaving (start with a quest)" | "Mysticism (another school of magic), Spellweaving (magic unlocked by a starting quest)" |
| `:117` | "Blacksmithy", "Arms Lore", "Imbuing" | "Blacksmithy (making metal equipment), Arms Lore (examining weapons and armor), Imbuing (adding magical equipment properties)" |
| `:118` | "Grid highlighting by property", "Item database", "Organizer agent" | "Grid highlighting by property (mark items with chosen attributes), Item database (look up items), Organizer agent (a tool for moving groups of items)" |
| `:119`, `:121`, `:123`, `:125` | "Tailoring", "Carpentry", "Tinkering", "Alchemy" | "Tailoring (sewing), Carpentry (woodworking), Tinkering (making tools and small objects), Alchemy (making potions)" |
| `:123`, `:125` | "Item Identification", "Taste Identification" | "Item Identification (examining an item), Taste Identification (examining food and drink)" |
| `:127`, `:131`, `:133` | "Fletching", "Inscription", "Cartography" | "Fletching (making bows and arrows), Inscription (writing spell scrolls), Cartography (drawing maps)" |
| `:134` | "Treasure maps and SOS", "SOS locator" | "Treasure maps and SOS (distress messages with shipwreck locations), SOS locator (help finding those locations)" |
| `:137` | "Animal Taming", "Animal Lore", "Veterinary", "Herding" | "Animal Taming (gaining control of an animal), Animal Lore (examining animals), Veterinary (treating animals), Herding (directing animals with a shepherd's crook)" |
| `:141` | "Musicianship", "Peacemaking", "Provocation", "Discordance" | "Musicianship (playing instruments), Peacemaking (calming with music), Provocation (making creatures fight), Discordance (weakening a creature with music)" |
| `:146-147` | thieving skill list; "Forensic Evaluation"; "Hidden characters" | Use the individual explanations in the thieving table above. "Forensic Evaluation (examining bodies and locks), Hidden characters (client settings for displaying hidden characters)"; verify what that client setting actually displays before promising it reveals other players. |
| `:151` | "Transparent houses", "Circle of transparency" | "Transparent houses (see through house graphics), Circle of transparency (see through nearby obstacles)" |
| `:152-153` | "Runes, gates and boats", "blank recall rune" | "Travel stones, portals, and boats"; supplies: "a borrowed blank recall rune, a stone for saving a travel destination" |
| `:157` | "Autoloot", "Scavenger", "Nearby loot", "Vendors: advanced shop, trade, auto buy and sell" | "Autoloot (collect items from bodies), Scavenger (pick up selected ground items), Nearby loot (view nearby loot), Vendor tools (shop and trade with merchants)". Each requires its own setup and permission checks. |
| `:158` | "Legion scripting (advanced)", "Script library browser (advanced)" | "Legion scripting (advanced: run scripts to automate actions), Script library browser (advanced: find scripts)". Keep these out of the required beginner controls. |
| `TutorialGumps.cs:354` | "TazUO features ... Help: tazuo.org" | "Optional tools in TazUO, your game client: ... Select Help to read the client guide." Keep the actual clickable help destination visible. |

## Wiki draft rewrites

These are suggestions for a later wiki refresh, not edits to those drafts. Where a whole obsolete paragraph would mislead a new player, replace the paragraph rather than defining its outdated terms. All locations in a grouped row receive the suggestion. Exact server button labels should match the current code.

### M: fuller Markdown guide

| Line | Current wording or fragment | Suggested wording |
|---|---|---|
| `:3` | "test world ... New Haven lessons ... P481 is planned" | "This draft describes tutorial code available in the test-world build. The main lessons now follow one road across the Wakening Isle; optional lessons and graduation are in New Haven. Availability on a running server has not been checked for this guide." |
| `:5`, `:21` | "core lessons", "death and resurrection", "graduate" | "Finish the required main lessons to complete the tutorial. They introduce movement, carrying items, speaking, pets, restoring health, returning to life after death, bank storage, the League, a story scene, and portal travel." Heading: "Main lessons". |
| `:9` | "Rook Hallowell, the League recruiter ... first tutorial login" | "For a new account, choosing Tutorial Island at character creation starts the main lessons with Tamsin on the Wakening Isle. Follow the arrow, double-click Tamsin with two quick left clicks, and choose the lesson marked (next); Rook is the guide for optional lessons and graduation in New Haven." Explain returning-account exceptions nearby, using `TutorialStart.Eligibility`, not a promise that every new character starts the tutorial. |
| `:11` | "start remedial training" | "restart the tutorial after skipping it"; keep the existing explanation that only the recorded character can use the active tutorial. |
| `:13` | "core", "bank token", "Reset this lesson" | "Take the main lessons in order. Hint and arrow repeats the directions and can replace a missing blue practice item; Restart this lesson starts the current lesson over." Explain the bank token as the small blue practice coins. The current button is Restart, not Reset. |
| `:17` | "Yes. Really.", "first loop", "Young protection" | "Choose Skip the tutorial, then confirm Yes, skip and Skip now to start in New Haven. Skipping records the Didn't Read the Manual progress award and, under the current default rules, your first loop, a journey milestone; it does not grant the graduation reward box or pet choice. Young is your account's temporary newcomer protection, which continues for its remaining time." |
| `:19` | "Remedial training (the full tutorial, with its rewards)" | "At Rook, choose Restart the tutorial and earn its rewards to return to the Wakening Isle. Your account keeps its pet claim and used free-bandage allowance, so restarting does not grant extra pets or a fresh allowance." |
| `:25` | "Walking, running and the camera ... beside Rook" | "Walk and run: on the road above the beach, hold the right mouse button toward the blue floor tile, then the gold tile. Release it to stop; point farther from your character to run." The current lesson does not teach camera controls. |
| `:26` | "backpack on your paperdoll" | "At the roadside camp, double-click your character to open its character window, also called the paperdoll. Double-click the backpack picture, then double-click the blue practice bag inside." |
| `:27` | "Your paperdoll ... drag ... onto your paperdoll" | "Your character window and clothes: at the clothes rack, open your character window and backpack. Hold the left mouse button on the blue practice cloak, move it onto your character's picture, and release; remove an existing cloak first." |
| `:28` | "your Journal keeps what was said" | "At the signpost, press Enter, type I am ready to learn, then press Enter again to speak. The Journal is a window where you can read past spoken messages." Add verified opening instructions. |
| `:29` | "At the farm gate ... Resurrect" | "After the required farm lesson, follow the arrow to the pale gray rat in the training yard and double-click it. Click Ready for the death lesson; as a ghost, double-click Sera beside it and click Resurrect to return to life." |
| `:30` | "say bank ... bank box" | "At the practice bank in the trades square, double-click the door, stand near Merrin, and say bank by pressing Enter, typing bank, and pressing Enter again. Drag the blue practice coins from your backpack into the bank storage window." |
| `:31` | "moongate at the farm gate ... plaza" | "The final main lesson is at the dock. Walk into or double-click the glowing blue portal to travel with your pets to Rook on New Haven's town plaza." Move this row to the end. |
| `:32` | "Registrar's house ... north door" | "At the League lodge on the Wakening Isle, double-click the north door, then double-click Elara Voss to read about League jobs and rewards. You do not have to join to finish the lesson." |
| `:33` | "loop ... rune stone at the farm gate" | "At the standing stones on the small hill, double-click the bright blue stone and stay nearby for a short story about a planned way to start another journey, called a loop. Watching changes nothing about your character." |
| `:25-33`, missing row | No main farm step | Insert after speaking: "The farm: follow the arrow to Wren in a straw hat at the gate. Choose your tutorial pet, defeat pests in the cabbage rows, and use a bandage to restore health, following Wren's instructions." The current main lesson list must include this step. |
| `:35` | "While you are Young ... ghost" | "The death lesson really kills your character, leaving you as a ghost until a healer brings you back to life. While your account has Young newcomer protection, your belongings return to your backpack after death; this is not the ordinary rule after that protection ends." |
| `:37`, `:39`, `:43` | "Optional wings", "core", "Remedial trainees" | "Optional lessons"; "After the main lessons, Rook in New Haven offers optional lessons before you graduate. Players restarting after a skip can see optional lessons from the start." Column heading: "Lesson group". |
| `:41` | "east of the farm gate ... Animals use the farm pen" | "The optional combat, magic, trade, and goat lessons stay in New Haven, separate from the Wakening Isle's main route. Follow each lesson's arrow to its practice area." Do not send players back to the isle farm for the optional goat. |
| `:45` | "macing, fencing ... Equip ... Tab for war mode ... sparring echo" | "Pick a weapon skill, such as Swords, Macing for clubs, Fencing for thrusting weapons, or Archery for bows. Wear the borrowed weapon by dragging it onto your character's picture; turn war mode on if needed, then double-click the blue practice opponent and land three hits. Tab switches war and peace with the usual toggle setting. The separate bandage lesson asks you to restore health to yourself and a wounded villager." |
| `:46` | school names, "cast", "tiles", "readied" | "Try one spell or special attack from each offered school of magic. Open the borrowed book and double-click the named spell or move; spells ask you to click a target, while Bushido and Ninjitsu prepare a special weapon attack before you fight. For Close Wounds, stand within two steps of the wounded villager." Retain the exact school and spell names in a companion list. |
| `:48` | "barrel staves", "refresh potion", "Arms Lore", "curio", "Taste Identification" | "Each craft lesson lends tools and materials for one named recipe. Barrel Staves are wooden barrel parts; a curio is the odd blue practice object. The smithing, tinkering, and alchemy lessons also ask you to activate a named examination skill in Skills and click the item you made or were lent." Keep the recipe and skill names beside their explanations. |
| `:49` | "Herd, tame, study, and bandage" | "Use a shepherd's crook to direct the practice goat, use Animal Taming to control it, use Animal Lore to examine it, and treat it with a bandage. This goat stays at the New Haven farm after the lesson." |
| `:50` | "Bard", "Peacemaking, Provocation, and Discordance" | "Music skills: use the borrowed lute to calm a practice figure with Peacemaking, make two practice figures fight with Provocation, and weaken one with Discordance. Musicianship is the skill used to play the instrument." |
| `:51` | thieving skill list | "Practice hiding, moving while hidden, finding and removing a trap, picking a lock, stealing a purse, looking in a practice person's backpack, begging, applying poison, and tracking. The checklist gives the exact skill names to choose in Skills." |
| `:52` | "deeds" | "Learn what house-placement deeds and protected house storage are. This is a walking explanation, not a house-placement practice task." |
| `:53` | "runes, runebooks, travel spells" | "Learn about stones that save travel locations, books that hold those stones, travel spells, portals, and boats. The tour explains these tools but does not have you cast the travel spells." |
| `:54` | "karma, fame, name colors, murder counts, and guards" | "Learn how good-or-bad reputation, renown, name colors, unlawful-kill records, and town guards affect play." Keep the corresponding terms karma, fame, and murder counts in parentheses on first use. |
| `:55` | "Shard systems ... loot boxes ... TazUO tools" | "This server's extra features: learn about reward boxes, progress awards, extra jewelry slots, and the planned level and loop systems. TazUO is the client program you use to play, with optional collection and shopping tools." |
| `:57` | "temporary skill loans" | "These lessons temporarily boost the abilities needed to practice and lend tools and supplies. The boost ends and borrowed items disappear when the lesson ends, you leave, or you log out; moving borrowed items to the ground, bank, or another person also removes them. You keep items you actually gather or craft." |
| `:59` | "snooping ... karma ... levels and loop reset system" | "Looking inside someone else's backpack and using Poisoning can lower karma, your character's good-or-bad reputation score, even on these practice targets. Some subjects are explained rather than practiced; the full system for leveling and restarting a journey is still planned." Keep the explained-only skill list, with the definitions above. |
| `:63` | "a separate pet and practice route" | "The farm is now a required main lesson on the Wakening Isle. Double-click Wren Tallow in the straw hat at the gate and follow these steps." |
| `:65` | "one follower slot free ... wait for graduation if you want a fox or bird" | "Choosing a dog or cat uses your account's one tutorial pet choice. Pets take follower capacity, the limit on animals and other followers you can control at once; this pet needs one available slot." Remove the advice to wait for a fox or bird unless the required farm is given a way to proceed without claiming its pet. |
| `:66` | "animals station" | "Defeat the required number of farm pests yourself or with your pet, then return to Wren. These farm tasks are distinct from the optional lesson with a practice goat." |
| `:67` | "A failed treatment does not finish this step" | "Double-click a bandage, click yourself or an injured pet, and wait. The step finishes only when the bandage restores health." |
| `:69` | "three stacks of ten per account" | "When you need bandages for this step, Wren can supply ten at a time, up to three times for your entire account under the default settings. Moving a stack elsewhere does not restore that allowance." Keep the shop advice pending reachable-supply verification on the isle. |
| `:71` | "Graduation and your companion pick" | "Finishing the tutorial and choosing a pet" |
| `:73` | "first loop ... skills, stats, level, or XP ... Young hours" | "After the main lessons, take the dock portal to Rook in New Haven. Try any optional lessons you want before choosing Graduate. Graduation records your first loop, a journey milestone, without resetting learned abilities, character attributes, level, or experience points; your remaining Young newcomer protection continues." |
| `:75` | "loot box containing a blessed elixir of rebirth ... guarded towns" | "Your graduation reward box includes an elixir of rebirth, a potion that brings a bonded pet back to life. The potion is blessed, meaning it stays with you through death. Double-click the box here in New Haven, where guards protect the town, to open it." Verify the item's blessed behavior before using this as a general item-loss guide. |
| `:77` | "bonded evo starter pet ... follower slot ... companion" | "If your account has not already claimed its tutorial pet, the graduation window offers a pet choice. It is an evolving animal that can grow through fighting, arrives bonded so it can return after death, and uses one follower slot from your pet-capacity limit." The normal fresh main route now claims a farm dog or cat first; do not advertise four graduation choices to every new trainee. |
| `:79` | "Choose your companion", "picker" | "To reopen a waiting graduation choice, double-click Rook with the character who took the tutorial and choose Choose your pet. If you closed the separate color-choice window, double-click your living pet to open that window again." |
| `:81` | "evolution stages and their requirements" | "Some later pet forms and the conditions for reaching them are unfinished. Do not choose a pet on the promise of an unavailable form." |
| `:85` | "bonded ... body to fade" | "Your tutorial pet is bonded to you, which lets it return as a ghost after death. Wait until its dead body disappears before trying to bring the ghost back to life." |
| `:87` | "resurrection window ... Young ... 0.2 from each pet skill" | "Keep your pet's ghost near Tobin beside Wren and double-click Tobin, then choose the pet's name in the window. Bringing it back is free during Young newcomer protection; otherwise the displayed fee comes from your bank. Each of the pet's trained abilities drops by 0.2 points." |
| `:88` | "target ... within two tiles ... resurrection" | "Keep the potion in your backpack and stand within two steps of the pet's ghost. Double-click the potion, then left-click the ghost when asked for a target; you must be alive, and success uses up the potion." |
| `:90` | "spirit lacks cohesion", "corpse" | "If a message says the pet's spirit lacks cohesion, its dead body is still present. Wait until the body disappears, then try again." Retain the actual error phrase as a recognizable quote, followed immediately by the explanation. |
| `:92-94` | "Planned start area ... facet ... proposals ... Use Rook and the New Haven route" | "The main route in this source build is on the Wakening Isle, a separate game map, with Tamsin's lessons and a portal to New Haven. Private lesson copies and later story changes need their own implementation and deployment checks; this guide does not certify them." Remove the obsolete instruction to use the plaza route. |

### N: older DokuWiki outline

| Line | Current wording or fragment | Suggested wording |
|---|---|---|
| `:1`, `:3`, `:5` | "The New Haven Tutorial", "framework", "stations are placeholders", "every account is wiped", "recruiter" | Title: "The beginner tutorial". Opening: "The main lessons in this test-world source build are on the Wakening Isle with Tamsin. Rook in New Haven handles optional lessons and graduation; running-server availability has not been checked here." Remove the obsolete placeholder and account-wipe assertions from this player guide unless a current release notice independently confirms them. |
| `:9` | "core ... camera ... paperdoll ... vision of the loop" | "Required main lessons: move, open your backpack, dress your character, speak, care for a pet, return to life after death, use bank storage, meet the League, watch a story, and travel through a portal to New Haven." |
| `:10` | "Optional wings" | "Optional lesson groups in combat, magic, gathering, crafting, animals, music, thieving, housing, travel, reputation, and this server's extra features." |
| `:11` | "loot box ... guard zone ... pet stays with you" | "Finishing the tutorial gives a reward box; double-click it in New Haven, where the town guards protect the area, to open it. Your account gets one tutorial pet, shared between the farm and graduation choices." Do not imply a pet cannot die or that four graduation choices remain available after a farm claim. |
| `:17`, `:19` | "West of town, past the Bardic Guild ... League farmhand" | "The required farm lesson is on the Wakening Isle, east along the road. Wren Tallow, the farmer in a straw hat, waits at its gate." |
| `:21` | "bonded to you at once and grows as it fights" | "Choose a dog or cat to keep. It grows through fighting and arrives bonded, which lets it return as a ghost after death and be brought back to life." |
| `:23` | "Kill three ... you and your pet together" | "Defeat the required number of rats or grass snakes in the cabbage rows, yourself or with your pet. To send your pets to attack, say all kill and click a pest when asked for a target." Do not hard-code a configurable count without naming it as the default. |
| `:25` | "Healing or Veterinary" | "Double-click a bandage and click yourself or an injured pet, then wait for treatment. Healing treats people and Veterinary treats animals; this step needs an actual restoration of health." |
| `:27` | "client's map update ... two trees" | "Use the current player package so the game map matches the tutorial server." Keep the old tree-removal history in implementation notes, not as the new isle's installation requirement. |
| `:31` | "The System asks twice ... remedial training" | "Choose Skip the tutorial and confirm twice to record the Didn't Read the Manual progress award. To take the lessons later, visit Rook and choose Restart the tutorial and earn its rewards; finishing then also records Read the Manual Eventually." |
| `:35` | "Gem ... world folds shut ... loop ... Young status" | "The story shows a planned way to begin another journey, called a loop, while keeping some long-term progress and your pet. It changes nothing about your character and does not end Young, your account's temporary newcomer protection." |
| `:40` | "the tutorial's Vault" | "The Rootdeep Burrows are a separate optional dungeon area near Old Haven. Their trainee-only Vault is not required for graduation." Verify current access and map placement before including a route from the isle. |

### W: code-repo DokuWiki draft

| Line | Current wording or fragment | Suggested wording |
|---|---|---|
| `:1`, `:3`, `:5` | "test shard", "nine core lessons", "optional wings are still previews", "real world" | "This draft describes tutorial code enabled for the test server, not a confirmed live release. Tamsin teaches the required main lessons on the Wakening Isle; Rook in New Haven offers optional lessons and graduation." Remove the old nine-lesson count, preview claim, and unverified account-reset notice. |
| `:5` | "Double-click him to open New Haven orientation" | "Follow the arrow to Tamsin on the Wakening Isle and double-click with two quick left clicks. In New Haven, double-click Rook for the window titled Rook Hallowell: New Haven tutorial." |
| `:9` | "first login ... System line ... Rook" | "A new account starts the tutorial by choosing Tutorial Island at character creation. The game points the tutorial character to Tamsin; returning accounts may start in New Haven according to their saved tutorial progress." |
| `:11` | "Two voices ... System: ... Echo ... dry commentator" | "Teachers speak directly to your character. The game also sends lesson instructions and progress messages, which you can reread in the Journal." Server text no longer carries its own System prefix; do not teach an obsolete joke as a control. |
| `:12` | "League Registrar ... League field office" | "Elara Voss handles joining the League, the organization offering jobs and rewards. Rook guides the tutorial in New Haven; reading about the League does not require joining." Distinguish the isle lodge from the New Haven office when giving directions. |
| `:14`, `:16` | "nine core lessons", "Reset this lesson" | "Main lessons"; "Take Tamsin's main lessons in order, following each arrow along the road. Hint and arrow repeats directions; Restart this lesson begins that lesson again." |
| `:19` | "camera", "blue mark", "gold mark" | Use M `:25`'s Walk and run rewrite, with visible floor tiles above the beach and release-to-stop instructions. |
| `:20` | "paperdoll" before the backpack lesson | Use M `:27`'s character-window and drag explanation, after the backpack row. |
| `:21` | "Open your backpack" | Use M `:26`'s full sequence through the character window and backpack picture. |
| `:22` | "say I am ready to learn", "Journal" | Use M `:28`'s Enter, type, Enter sequence and message-history explanation. |
| `:23` | "pale echo", "accept resurrection", "Young" | Use M `:29`'s rat and Sera instructions and M `:35`'s definition of Young protection. |
| `:24` | "banker ... practice token ... bank box" | Use M `:30`'s Merrin, speech, blue coins, and bank-storage rewrite. |
| `:25` | "blue tutorial moongate ... farm gate" | Use M `:31`'s dock portal rewrite and make this the last main row. |
| `:26` | "Elara Voss ... League" | Use M `:32`'s isle lodge rewrite. |
| `:27` | "vision marker at the farm gate" | Use M `:33`'s standing-stones story rewrite. |
| `:19-27`, missing row | No required farm step | Insert M's proposed farm row after speaking; do not leave the required pet, pests, and bandage tasks only in the optional section. |
| `:31` | "loop count or Young time" | "This story changes none of your character's abilities, belongings, journey milestones, or remaining newcomer protection." Introduce loop and Young by name in their explanations, not as unexplained counters. |
| `:35`, `:37` | "wings", "wing station", "previews" | "Optional lessons"; "Before graduating, visit Rook in New Haven for optional practice and walking explanations. Choose only the subjects that interest you." Remove the claim that almost every optional lesson is unbuilt. |
| `:41` | "West of town, past the Bardic Guild ... Choose Animals" | "Wren's required pet-care lesson is at the farm on the Wakening Isle. The optional Animals lesson in New Haven uses a separate practice goat; follow that lesson's own arrow." |
| `:44` | "follower slot", "bonded" | Use M `:65`'s capacity explanation and M `:85`'s bonded-pet explanation. State that the farm choice uses the account's tutorial pet claim. |
| `:45` | "Three kills where you or your pet did damage finish the Animals lesson" | "Defeat the required number of pests yourself or with your pet, then return to Wren. This is the farm step; it is separate from the optional goat checklist." |
| `:46` | "Healing or Veterinary ... finishes the Bandages lesson" | Use M `:67`'s double-click, target, and wait instructions. Explain that the separate optional bandage lesson has its own checklist; do not promise the entire optional lesson is completed by one farm heal. |
| `:50` | "outside the guarded town ... Young ... two trees" | "Young newcomer protection does not prevent the tutorial pests from hurting you. Use the current player package so the tutorial map matches the server." The old New Haven tree patch is not the new isle's complete map requirement. |
| `:54`, `:56`, `:58` | "System asks twice", "first loop", "provisional", "Remedial training" | Use M `:17` and `:19`'s exact current confirmation and restart labels, define loop as a journey milestone, and explain that skipping sends the player to New Haven. Keep default skip rules distinct from future proposals. |
| `:62` | "nine core lessons ... wing" | "After Tamsin's main lessons, use the dock portal to reach Rook in New Haven. Try any optional lessons you want before choosing Graduate." |
| `:65` | "loop 0 to loop 1" | "Graduation records your first journey milestone, called loop 1. It does not reset your character's abilities or experience." |
| `:66` | "Loop box ... fanfare" | "A reward box and a celebration message for recording your first loop, once per character." Check the reward subsystem before promising contents or a rarity from the table alone. |
| `:67` | "tier 1 Explorer's box ... Achievements" | "An Explorer's reward box for finishing the tutorial. Other progress awards may already have given you reward boxes." Tier is not helpful without an explained reward scale. |
| `:68` | "starter pet ... dog, cat, fox or bird" | "Your account has one tutorial pet claim, shared between farm and graduation choices. New trainees normally use it for a dog or cat in the required farm lesson, so graduation does not give them a second animal." |
| `:69` | "The way off the island ... normal route" | "After graduation, travel beyond New Haven's island is unlocked. Graduation itself does not move your character." Keep Wakening Isle and Haven Island separate. |
| `:70` | "Your Young time" | "Your remaining newcomer protection, called Young status, continues." |
| `:72` | "guarded town ... owner, co-owner or friend" | "Open reward boxes in a town protected by guards or in a house where you have the required permission." Verify the exact permitted house roles in the box implementation before listing them. |
| `:74` | "skills, stats or experience ... level ladder and loop resets" | "Recording a loop currently leaves learned abilities, character attributes, and experience points unchanged. The planned system for leveling and resetting a journey is unfinished." |
| `:76` | "Later characters ... first loop ... Explorer's box" | "Later characters on an account that finished the tutorial do not repeat its lessons or receive its graduation reward box or pet choice. Their first loop is recorded separately when the login rules apply." Recheck login behavior before promising an award to every later character. |
| `:80` | "evo pet", "1 follower slot", "bonded", "hue" | "This is an evolving animal: it can grow through fighting. It uses one slot from your follower-capacity limit and is bonded so it can return after death. Choose its color in the offered window; double-click the living pet to reopen that choice if you closed it." |
| `:84` | "Mainland moongates, recall, boats ... System line ... Rootdeep" | "Until graduation, the travel rules block routes beyond New Haven's island and direct you back to the tutorial. Recall is a travel spell; a moongate is a portal. The optional Rootdeep dungeon near Old Haven is a separate destination, not the Wakening Isle's main route." Do not promise all island and dungeon access before checking the current map and gate rules. |
| `:88` | "trainee-only Vault ... landing ... nets ... Overdraft ... crawlway ... Warren" | "The Rootdeep Burrows have a separate practice area called the Vault for tutorial characters. It is optional and not needed for graduation; use the Rootdeep guide for its entrance, practice nets, named enemy, and exit to the next dungeon area." The Overdraft is an enemy name, not an actual bank penalty. Verify access before publishing these directions. |
| `:33`, image placeholders under Needed images | "TODO image", "Hint and Reset", "marks", "orientation" | Keep unfinished image requests out of published player instructions. Suggested captions for later verified images: "A lesson window with Hint and arrow and Restart this lesson", "The blue and gold floor tiles", "Tamsin on the beach", "Wren at the isle farm", and "Rook's graduation window in New Haven". No art was requested or generated by this text review. |

## Concepts not taught as usable first-hour steps

This list describes gaps in the reviewed tutorial text, not claims that the entire server or every external guide lacks the information. Each item distinguishes what is already introduced from the missing explanation or practice. An optional feature name is not a completed lesson in using that feature.

1. **Reading character status and deciding when to retreat.** Show health, stamina, and mana, how to recognize low health or poison, and how to leave a fight. The required farm fight comes before the optional combat lesson, so basic attack, stop, peace-mode, and pet-recall controls need an introduction before the pests.
2. **Targeting, canceling, and recovering from the wrong click.** Several hints say what to click, but they do not introduce the targeting cursor or teach canceling a pending target. Demonstrate those controls and explain the difference between a failed attempt and waiting until an action is ready again. Confirm the actual keys in the shipped client and current profile. Merely saying use a skill does not teach finding and activating it.
3. **Ordinary inventory and equipment safety.** Opening the backpack and moving a cloak are taught. Opening a body, taking loot, understanding weight limits, checking equipment wear, and identifying which possessions stay after death are not practiced. Explain blessed items and the ordinary item-loss rules after Young protection ends; the borrowed-item cleanup messages cover a different rule.
4. **Using a merchant and keeping money safe.** Walk through buying bandages, paying for a service, selling an unwanted item, and moving gold into bank storage. The farm sends players to buy more bandages and the vet can charge the bank, but the bank lesson only moves a practice token.
5. **Stopping a pet fight and using a stable.** The farm teaches all kill and all follow me, and pet-death messages mention a vet. It does not demonstrate calling a fighting pet safely away, reading its health, understanding follower capacity, or storing and reclaiming it at an animal trainer. Add those steps before making pet-capacity or ghost-recovery instructions depend on them.
6. **Opening navigation tools and asking for help.** The main route teaches arrows and opening doors. It names the Journal without explaining how to open it, and it does not practice reading the world map, finding the player's position, asking another player or staff for help, or logging out safely. Demonstrate those actions and distinguish Tamsin's isle, Rook's New Haven, and the mainland before restricting travel between them.
7. **Making the first real choice after graduation.** Offer a few reachable beginner activities with directions and enough explanation to choose among fighting, gathering, crafting, and League work. Explain that learning abilities through use and choosing equipment are separate from the unfinished level-reset plan. State what Young protection does and does not protect before the player leaves the tutorial.

These are suggestions for short demonstrations, not requests to add all optional systems to the required route. Housing upkeep, advanced client scripts, the entire magic catalog, and the full loop design can wait for later guides.

## Verification and limits

This is a text review against checked-out source. No server, Docker build, client playthrough, account operation, deployment, or Haven connection was needed or performed. No tests or gates were added, and lane tests are none, so no red/green test cycle applies. Suggested wording has not been checked for clipping, wrapping, button width, localization, or readability in the shipped client. Saved NPC and prop names, actual world placements, live settings, exact housing rules, public travel reachability, and client key customizations remain unverified.

Where the prose appears to promise behavior that the current code may not deliver, the table calls for verification instead of silently treating the wording suggestion as a fix. In particular: a full-backpack bank trip, replacement bandage access, a reachable animal trainer, optional-lesson resurrection directions, and four pet choices after the now-required farm need behavior or placement checks before their final player instructions are approved.

Final checks ran under Windows PowerShell 5.1. The note has no em dashes or trailing whitespace, its tables have consistent columns, its named source locations exist, and its size is below 5 MB. Whitespace checks produced no diagnostics, including the new untracked file. `tools/progress.py --dry-run` completed with exit 0 using these work copies' path overrides; its incidental `tools/progress.json` write was restored byte-for-byte. The reporter's project-wide numbers are not evidence for this review. The code work copy is clean, and the notes work copy contains only this new file. No commit, merge, push, or branch change was performed.

P702 DONE
