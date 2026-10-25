# P588: tutorial text pass

Written 2026-10-25. Proposals only; no code, shared localization, configuration, or world data changed.

Read both work copies' AGENTS.md, the direction decision, and the task list. Sources are the canonical files under `ShatteredLegacy/server/customizations/Tutorial/`; the file:line column is relative to that folder. Line numbers refer to the unchanged source in this work copy.

Every proposed prose message has at most two short sentences. Headings, item names, buttons, and checklist labels stay short phrases. Repeated text is listed at each source location; strings assembled at runtime use their source placeholder names. A proposal identical to the current text means keep it. Internal keys, type names on the left side of name maps, command arguments, staff-only tools, logs, empty strings, separators, and HTML styling are excluded.

All 16 source files were reviewed, including conditional fallback pages, item and creature labels, arrow destination labels, and the localized messages called here. The localized English below comes from source comments, not a loaded client cliloc file. Existing shared message IDs are not a request to edit global localization.

Source file inventory (606 table entries, including repeated occurrences and enum display headings):

| Source file | Table entries |
|---|---|
| `ClusterFLoops.cs` | 4 |
| `ClusterFTutorial.cs` | 25 |
| `TutorialCorePlacement.cs` | 18 |
| `TutorialCoreTrials.cs` | 28 |
| `TutorialCreature.cs` | 1 |
| `TutorialFarm.cs` | 31 |
| `TutorialFarmLayout.cs` | 0 |
| `TutorialGumps.cs` | 49 |
| `TutorialIslandGate.cs` | 1 |
| `TutorialPetCare.cs` | 14 |
| `TutorialRecruiter.cs` | 5 |
| `TutorialStations.cs` | 218 |
| `TutorialStyle.cs` | 0 |
| `TutorialTradeTrials.cs` | 151 |
| `TutorialTrialProgress.cs` | 0 |
| `TutorialWingTrials.cs` | 61 |

## Welcome, progress, graduation, and the loop vision

| File:line | Current text | Proposed text |
|---|---|---|
| `ClusterFLoops.cs:71` | A vision. The sword strikes the Gem. The shards fly. You fall, and the world folds shut behind you. | You see a vision of a sword striking a gem. The gem breaks, and the world fades away. |
| `ClusterFLoops.cs:72` | You wake where you started, remembering. That is a loop. Your level goes back to 1; your skills go with it. | In the vision, you wake at the beginning with your level and skills reset. This is a preview of a future loop system. |
| `ClusterFLoops.cs:73` | What you keep: the League, your recipes, your achievements, your guild ranks. And me. Lucky you. | In this vision, your League progress, recipes, achievements, and guild ranks remain. Your companion stays with you too. |
| `ClusterFLoops.cs:74` | This was only a vision. Nothing about you has changed. Yet. | The vision is over. Your level, skills, and belongings have not changed. |
| `ClusterFTutorial.cs:88` | Welcome back. Your completed lessons are saved. Ask Rook for the next one. | Your finished lessons are saved. Double-click Rook to choose your next lesson. |
| `ClusterFTutorial.cs:93` | Your companion is still waiting. Double-click Rook on the New Haven plaza and choose one. | You still have a pet to choose. Double-click Rook on the New Haven plaza to open the choices. |
| `ClusterFTutorial.cs:121` | Welcome to New Haven. Rook, the League recruiter, is waiting by the plaza; they bill by the hour. | Welcome to New Haven. Rook Hallowell, your tutorial guide, is waiting on the town plaza. |
| `ClusterFTutorial.cs:122` | Follow the arrow and double-click Rook (two quick left clicks) to begin. You can skip it all there; Rook will ask twice. | Follow the arrow and double-click Rook with two quick left clicks. His window lets you start a lesson or skip the tutorial. |
| `ClusterFTutorial.cs:155` | You are not in the tutorial. | You do not have an active tutorial. Double-click Rook on the New Haven plaza to check your progress. |
| `ClusterFTutorial.cs:165` | This station has no lesson of its own. It is optional; graduation needs only the core. | This optional lesson has no activity yet. You can graduate after finishing the main lessons. |
| `ClusterFTutorial.cs:179` | Station done: {station?.Title ?? key}. Adequately. | Lesson finished: {station?.Title ?? key}. |
| `ClusterFTutorial.cs:184` | Core finished. The wings are open, and optional. You may graduate whenever you like. | You finished the main lessons. Double-click Rook to graduate or try an optional lesson. |
| `ClusterFTutorial.cs:202` | Skipped. Bold. The recruiter will still be here when you need remedial training. And you will. | You skipped the tutorial. Double-click Rook if you want to take the lessons and earn their rewards later. |
| `ClusterFTutorial.cs:207` | Your first loop is recorded. The island is open; your Young hours keep running. | You can now leave Haven Island. Your Young protection continues until its time runs out. |
| `ClusterFTutorial.cs:211` | Finish remedial training with the recruiter to leave the island. | Double-click Rook to restart the tutorial. Finish the main lessons and graduate to leave Haven Island. |
| `ClusterFTutorial.cs:235` | Remedial training. Welcome back. I saved your seat. | You have restarted the tutorial with its usual rewards. Choose the first lesson in Rook's window. |
| `ClusterFTutorial.cs:241` | dog | dog |
| `ClusterFTutorial.cs:241` | cat | cat |
| `ClusterFTutorial.cs:241` | fox | fox |
| `ClusterFTutorial.cs:241` | bird | bird |
| `ClusterFTutorial.cs:257` | You have earned a companion. Choose one: | You earned a pet. Choose one in the window. |
| `ClusterFTutorial.cs:264` | You have earned a companion. Choose one in the window that opened. | You earned a pet. Click Choose beside the pet you want in the window that opened. |
| `ClusterFTutorial.cs:281` | {TutorialPetCare.IfYourPetDiesLine} Your graduation box holds one elixir. | {TutorialPetCare.IfYourPetDiesLine} Your graduation reward box contains one elixir of rebirth. |
| `ClusterFTutorial.cs:293` | You are not in the tutorial. | You do not have an active tutorial. Double-click Rook on the New Haven plaza to check your progress. |
| `ClusterFTutorial.cs:298` | Finish the core first. | Finish the main lessons listed in Rook's window before you graduate. |
| `ClusterFTutorial.cs:315` | Graduated. Eventually. It counts. | You finished the tutorial after returning to it. You can now leave Haven Island. |
| `ClusterFTutorial.cs:315` | Graduated. New Haven survived you. Now the rest of Britannia gets a turn. | You finished the tutorial. You can now leave Haven Island. |
| `ClusterFTutorial.cs:325` | graduating the New Haven tutorial | finishing the New Haven tutorial |
| `ClusterFTutorial.cs:335` | Open that box here in town. Boxes only open in guarded towns and your own house. | Double-click your reward box here in town to open it. These boxes open only in guarded towns or your own house. |

## Rook's menu, confirmation prompts, and pet choices

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialGumps.cs:48` | Thieving and stealth | Thieving and stealth |
| `TutorialGumps.cs:49` | Shard systems | Shard features |
| `TutorialGumps.cs:55` | You are in the core lessons. | Finish the main lessons in order. |
| `TutorialGumps.cs:56` | Core done. The optional lessons are open, and you may graduate. | You finished the main lessons and can graduate. Optional lessons are also open. |
| `TutorialGumps.cs:57` | Remedial training: the core again, with its rewards. | You restarted the tutorial and can earn its usual rewards. |
| `TutorialGumps.cs:58` | You skipped the tutorial. | You skipped the tutorial. |
| `TutorialGumps.cs:59` | You have graduated. | You finished the tutorial. |
| `TutorialGumps.cs:60` | Not started. | You have not started the tutorial. |
| `TutorialGumps.cs:99` | Rook Hallowell, League recruiter: New Haven orientation | Rook Hallowell: New Haven tutorial |
| `TutorialGumps.cs:100` | You have no account record. | You have not started the tutorial on this account. |
| `TutorialGumps.cs:105` | another character | another character |
| `TutorialGumps.cs:106` | Your account's tutorial belongs to {name}. | This account's tutorial was started by {name}. |
| `TutorialGumps.cs:107` | Only that character can take its lessons, skip, graduate or choose its companion. | Use that character to take lessons, skip, graduate, or choose a pet. |
| `TutorialGumps.cs:111` | The core lessons (in order) | Main lessons: take these in order |
| `TutorialGumps.cs:120` | {i + 1}. {s.Title}{(done ? " (done)" : s == next ? " (next)" : "")} | {i + 1}. {s.Title}{(done ? " (done)" : s == next ? " (next)" : "")} |
| `TutorialGumps.cs:125` | Trade and skill lessons (optional) | Optional trade and skill lessons |
| `TutorialGumps.cs:134` | The trade and skill lessons open after the core. | Finish the main lessons to open trade and skill lessons. |
| `TutorialGumps.cs:142` | Skip the tutorial | Skip the tutorial |
| `TutorialGumps.cs:148` | Graduate | Graduate |
| `TutorialGumps.cs:154` | Remedial training (the full tutorial, with its rewards) | Restart the tutorial and earn its rewards |
| `TutorialGumps.cs:159` | Choose your companion | Choose your pet |
| `TutorialGumps.cs:160` | You have earned a pet. It is waiting until you pick one. | You earned a pet and still need to choose one. |
| `TutorialGumps.cs:164` | Nothing more to teach you here. Go and be extraordinary. | You can check your tutorial progress here whenever you return to New Haven. |
| `TutorialGumps.cs:180` | {s.Title}{(done ? " (done)" : "")} | {s.Title}{(done ? " (done)" : "")} |
| `TutorialGumps.cs:209` | Return to Rook on the New Haven plaza to graduate. | Follow the arrow back to Rook on the New Haven plaza. Double-click him and choose Graduate. |
| `TutorialGumps.cs:246` | You want to skip the tutorial. Everyone who skips it says they know what they are doing. Skip? | Skip the remaining tutorial lessons? You can return to Rook later to take them and earn their rewards. |
| `TutorialGumps.cs:247` | Really? There is an achievement for this, and it is not a compliment. Last chance. Skip? | Skipping earns the Didn't Read the Manual achievement. Skip the tutorial now? |
| `TutorialGumps.cs:257` | Yes, skip | Yes, skip |
| `TutorialGumps.cs:257` | Yes. Really. | Skip now |
| `TutorialGumps.cs:259` | No, teach me | Keep learning |
| `TutorialGumps.cs:283` | https://tazuo.org/ | https://tazuo.org/ |
| `TutorialGumps.cs:289` | Open the World Map | Open the World Map |
| `TutorialGumps.cs:290` | Open the Journal | Open the Journal |
| `TutorialGumps.cs:291` | Open the options | Open Options |
| `TutorialGumps.cs:317` | Where: {s.Where}. | Go to: {s.Where}. |
| `TutorialGumps.cs:318` | Hands-on: {string.Join(", ", s.HandsOn)}. | Practice: {string.Join(", ", s.HandsOn)}. |
| `TutorialGumps.cs:319` | Also gains: {string.Join(", ", s.Covered)}. | Related skills: {string.Join(", ", s.Covered)}. |
| `TutorialGumps.cs:320` | Explained: {string.Join(", ", s.Explained)}. | Learn about: {string.Join(", ", s.Explained)}. |
| `TutorialGumps.cs:321` | TazUO: {string.Join(", ", s.TazUO)}. Guides: &lt;a href="{WikiBase}"&gt;tazuo.org&lt;/a&gt; | TazUO features: {string.Join(", ", s.TazUO)}. Help: &lt;a href="{WikiBase}"&gt;tazuo.org&lt;/a&gt; |
| `TutorialGumps.cs:322` | You will be given: {s.Tool}. | Lesson supplies: {s.Tool}. |
| `TutorialGumps.cs:323` | This station has no lesson of its own. It is optional; graduation needs only the core. | This optional lesson has no activity yet. You can graduate after finishing the main lessons. |
| `TutorialGumps.cs:368` | The protector. Grows from a pup into a hound, and one day a windrunner. | A dog companion, shown as a puppy. It grows into a larger hound as you play together. |
| `TutorialGumps.cs:369` | The striker. Grows from a kitten into a great cat, and one day a manticore. | A cat companion, shown as a kitten. It grows into larger cats as you play together. |
| `TutorialGumps.cs:370` | The trickster. Grows from a kit into a fox, and one day a bake kitsune. | A fox companion, shown as a fox kit. After graduation and enough growth, it can become a bake kitsune, a magical fox. |
| `TutorialGumps.cs:371` | The scout. Grows from a chick into a firebird, and one day a hiryu. | A bird companion, shown as a chick. It can grow into a firebird; more stages are still being added. |
| `TutorialGumps.cs:379` | You have earned a companion. Choose one: | You earned a pet: choose one |
| `TutorialGumps.cs:380` | It is bonded to you and grows as you play together. | Your pet grows as you play and can be brought back after death. |
| `TutorialGumps.cs:388` | Choose | Choose |
| `TutorialGumps.cs:403` | No room for a pet right now. Free a follower slot, then ask Rook again. | You cannot control another pet right now. Stable one of your pets with an animal trainer, then ask Rook again. |

## Main lesson hints, status, and controls

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialCoreTrials.cs:17` | I am ready to learn | I am ready to learn |
| `TutorialCoreTrials.cs:50` | Walk onto the glowing blue floor tile beside Rook, then the gold one. Hold the right mouse button where you want to go; point farther away to run. | Hold the right mouse button toward the glowing blue floor tile beside Rook to walk onto it, then walk onto the gold tile. Point farther from your character while holding the button to run. |
| `TutorialCoreTrials.cs:51` | Double-click yourself to open your paperdoll, then double-click the backpack on it. Inside, double-click the blue practice bag. | Double-click your character to open the character window, then double-click its backpack picture. Inside your backpack, double-click the blue practice bag. |
| `TutorialCoreTrials.cs:52` | A blue practice cloak is in your backpack. Drag it onto your paperdoll (double-click yourself to open it); take off your own cloak first if you wear one. | Double-click your character to open the character window, then drag the blue practice cloak from your backpack onto your character's picture. If you already wear a cloak, drag it into your backpack first. |
| `TutorialCoreTrials.cs:53` | Press Enter, type '{Phrase}' and press Enter again. Your Journal keeps what was said. | Press Enter, type '{Phrase}', then press Enter again to speak. The Journal records what you say. |
| `TutorialCoreTrials.cs:54` | Follow the arrow to the farm gate, double-click the pale gray echo (a ghostly rat) and press Ready. As a ghost, double-click Sera the healer beside it and press Resurrect; while you are Young, your things come back to your backpack. | Follow the arrow to the pale gray rat at the farm gate, double-click it, and click Ready. After you die, double-click Sera beside it and click Resurrect to return to life. |
| `TutorialCoreTrials.cs:55` | A blue practice token (a small pile of coins) is in your backpack. Walk to the banker, say 'bank', and drag the token into your bank box. | Follow the arrow to the banker and say 'bank' to open your bank box. Drag the blue practice token, a small blue pile of coins in your backpack, into that box. |
| `TutorialCoreTrials.cs:56` | Follow the arrow to the farm gate and double-click the moongate there, a tall blue shimmering arch. It brings you back to the New Haven plaza. | Follow the arrow to the tall, shimmering blue arch at the farm gate. Double-click it to return to the New Haven plaza. |
| `TutorialCoreTrials.cs:57` | Follow the arrow to Elara Voss, inside the Registrar's house; double-click its door, on the north side, to open it. Double-click her to read about the League; joining is your choice. | Follow the arrow to Elara Voss and double-click the door on the north side of her house to enter. Double-click Elara to finish this lesson; you can read about the League without joining. |
| `TutorialCoreTrials.cs:58` | Follow the arrow to the bright blue rune stone at the farm gate. Double-click it and stay beside it until the vision ends; it changes nothing about you. | Follow the arrow to the bright blue rune stone at the farm gate. Double-click it and stay nearby until the vision ends; it will not change your character. |
| `TutorialCoreTrials.cs:59` | Ask Rook for this lesson. | Double-click Rook on the New Haven plaza to choose this lesson. |
| `TutorialCoreTrials.cs:66` | blue practice bag | blue practice bag |
| `TutorialCoreTrials.cs:87` | Make room in your backpack, then press Hint and arrow again. | Make room in your backpack. Click Hint and arrow to get another practice item. |
| `TutorialCoreTrials.cs:91` | A new one is in your backpack. | A replacement practice item is in your backpack. |
| `TutorialCoreTrials.cs:100` | Visit the tutorial healer first. A ghost can still double-click the healer. | Follow the arrow to Sera the healer and double-click her. Click Resurrect to return to life before starting a lesson. |
| `TutorialCoreTrials.cs:101` | the tutorial healer | Sera the healer |
| `TutorialCoreTrials.cs:108` | First finish: {next?.Title}. | Finish {next?.Title} before starting this lesson. |
| `TutorialCoreTrials.cs:128` | Make room in your backpack, then try this lesson again. | Make room in your backpack, then choose this lesson again in Rook's window. |
| `TutorialCoreTrials.cs:202` | Now the glowing gold tile. | Now walk onto the glowing gold floor tile. |
| `TutorialCoreTrials.cs:202` | the gold tile | the glowing gold floor tile |
| `TutorialCoreTrials.cs:222` | Stay beside the vision marker. Double-click it to begin again. | Stay beside the bright blue rune stone until the vision ends. Double-click it to restart the vision. |
| `TutorialCoreTrials.cs:257` | You are a ghost. Double-click Sera the healer, beside you, and press Resurrect. | You are a ghost. Double-click Sera beside you and click Resurrect to return to life. |
| `TutorialCoreTrials.cs:258` | Sera the healer | Sera the healer |
| `TutorialCoreTrials.cs:282` | Done. Your next lesson is ready. | Lesson finished. Click Next lesson / graduate to continue. |
| `TutorialCoreTrials.cs:283` | Next lesson / graduate | Next lesson / graduate |
| `TutorialCoreTrials.cs:283` | Hint and arrow | Hint and arrow |
| `TutorialCoreTrials.cs:284` | Reset this lesson | Restart this lesson |
| `TutorialCoreTrials.cs:297` | Core finished. Return to Rook on the New Haven plaza to graduate. The wings are optional. | You finished the main lessons. Follow the arrow to Rook on the New Haven plaza and choose Graduate, or try an optional lesson. |

## Lesson props, Sera, death, and resurrection

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialCorePlacement.cs:77` | Merrin | Merrin |
| `TutorialCorePlacement.cs:79` | Tobin | Tobin |
| `TutorialCorePlacement.cs:156` | glowing gold floor tile | glowing gold floor tile |
| `TutorialCorePlacement.cs:157` | glowing gold floor tile | glowing gold floor tile |
| `TutorialCorePlacement.cs:164` | glowing blue floor tile | glowing blue floor tile |
| `TutorialCorePlacement.cs:171` | tutorial moongate to New Haven | tutorial moongate to New Haven |
| `TutorialCorePlacement.cs:179` | The gate's landing is blocked. Ask a member of staff. | The place where this gate sends you is blocked. Ask a staff member for help. |
| `TutorialCorePlacement.cs:203` | blue practice cloak | blue practice cloak |
| `TutorialCorePlacement.cs:211` | blue practice token | blue practice token |
| `TutorialCorePlacement.cs:221` | the pale death echo | the pale gray rat |
| `TutorialCorePlacement.cs:240` | Death and resurrection | Death and resurrection |
| `TutorialCorePlacement.cs:241` | The echo will kill you for this lesson; while you are Young, your things come back to your backpack. Sera the healer, beside it, will bring you back. Ready? | Click Ready to die for this lesson, then double-click Sera beside the pale gray rat and click Resurrect. While you are Young, your belongings return to your backpack after death. |
| `TutorialCorePlacement.cs:242` | Ready | Ready |
| `TutorialCorePlacement.cs:243` | Not yet | Not yet |
| `TutorialCorePlacement.cs:257` | Sera | Sera |
| `TutorialCorePlacement.cs:257` | the tutorial healer | the tutorial healer |
| `TutorialCorePlacement.cs:280` | Ready to return to life? | Ready to return to life? |
| `TutorialCorePlacement.cs:281` | Resurrect | Resurrect |
| `TutorialCreature.cs:63` | an echo of a rat | a ghostly rat |
| `TutorialFarm.cs:581` | [500446] That is too far away. | Move closer, then double-click Wren the Farmhand again. |
| `TutorialIslandGate.cs:14` | Graduate with the League recruiter in New Haven before leaving the island. | Finish the main tutorial lessons, then double-click Rook on the New Haven plaza and choose Graduate. You can leave Haven Island afterward. |
| `TutorialRecruiter.cs:30` | Rook Hallowell | Rook Hallowell |
| `TutorialRecruiter.cs:31` | the League recruiter | the League recruiter |
| `TutorialRecruiter.cs:59` | [500446] That is too far away. | Move closer, then double-click Rook again. |
| `TutorialRecruiter.cs:63` | Ah, a new face. Or an old one. It is hard to tell anymore. | Welcome to New Haven. My window shows your tutorial progress. |
| `TutorialRecruiter.cs:77` | the League recruiter | Rook Hallowell, the tutorial guide |

## Wren the Farmhand, pests, and the farm pet

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialFarm.cs:57` | dog | dog |
| `TutorialFarm.cs:57` | cat | cat |
| `TutorialFarm.cs:85` | Farm's for the League's trainees. Nothing personal. The pests would only embarrass you. | These farm lessons are for characters taking the tutorial. Double-click Rook on the plaza to check your progress. |
| `TutorialFarm.cs:86` | Every farm needs a dog. Or a cat, if you like being ignored. Pick one; it's yours to keep. | Choose a dog or cat in the window. This is your one tutorial pet, which you keep after graduation. |
| `TutorialFarm.cs:87` | You've no room for another follower. Come back with a free slot. | You cannot control another pet right now. Stable one of your pets with an animal trainer, then come back. |
| `TutorialFarm.cs:88` | Rats in the cabbages again. Take your friend into the rows and clear out {0}. They don't hit back hard. | Walk into the cabbage rows, say 'all kill', then click a rat or grass snake for your pet to attack. Defeat {0} pests to finish this step. |
| `TutorialFarm.cs:89` | {0} more. Mind the snake; it sulks. | Defeat {0} more rats or grass snakes in the cabbage rows. |
| `TutorialFarm.cs:90` | You're bleeding on my carrots. Here, bandages. Patch yourself up, or your friend. Then we're square. | Double-click a bandage in your backpack, then click yourself or an injured pet. A successful heal finishes this step. |
| `TutorialFarm.cs:91` | That's all the bandages I can spare. The healer in town sells them. | I have no more free bandages for you. You can buy more from a healer in town. |
| `TutorialFarm.cs:92` | That's the farm. If your friend ever falls, Tobin the vet beside me can bring them back; the Bond Trial's mine to give, when it's time. | You finished the farm lessons. If your bonded pet dies, bring its ghost to Tobin the vet beside me. |
| `TutorialFarm.cs:93` | A pet. It will follow you through every loop. Try to be worth following. | This pet is yours to keep. Say 'all follow me' to have it follow you. |
| `TutorialFarm.cs:94` | Three vermin dead. A career is born. | You cleared the farm pests. Return to Wren the Farmhand at the gate. |
| `TutorialFarm.cs:95` | Bandaged. You will do that a great deal. | Your bandage restored health and finished the farm's healing lesson. |
| `TutorialFarm.cs:136` | Oh no, your friend's taken a bad turn. Tobin the vet, just beside me, can bring them back. | Your pet has died. Wait for its body to disappear, then bring its ghost to Tobin the vet beside me. |
| `TutorialFarm.cs:137` | Oh no, your friend's taken a bad turn. The vet in New Haven, by the stables, can bring them back. | Your pet has died. Wait for its body to disappear, then bring its ghost to the vet by the New Haven stables. |
| `TutorialFarm.cs:184` | The farm is west of town, past the Bardic Guild. The Farmhand is at the gate. Follow the arrow. | Follow the arrow west of town, past the Bardic Guild, to the farm gate. Double-click Wren the Farmhand, who wears a straw hat and carries a pitchfork. |
| `TutorialFarm.cs:187` | the Farmhand | Wren the Farmhand |
| `TutorialFarm.cs:265` | Pests cleared: {n} of {PestsToClear}. | Farm pests defeated: {n} of {PestsToClear}. |
| `TutorialFarm.cs:273` | Go back to the Farmhand. | Return to Wren the Farmhand at the farm gate and double-click her. |
| `TutorialFarm.cs:486` | The Farmhand's dog or cat | Choose your farm pet |
| `TutorialFarm.cs:490` | Choose the {TutorialFarm.FarmPetLines[i]} | Choose the {TutorialFarm.FarmPetLines[i]} |
| `TutorialFarm.cs:523` | the League farm | the League farm |
| `TutorialFarm.cs:539` | Wren Tallow | Wren Tallow |
| `TutorialFarm.cs:540` | the League farmhand | the League farmhand |
| `TutorialFarm.cs:623` | a farm rat | a farm rat |
| `TutorialFarm.cs:635` | a rat corpse | a rat corpse |
| `TutorialFarm.cs:644` | a field rat | a field rat |
| `TutorialFarm.cs:656` | a rat corpse | a rat corpse |
| `TutorialFarm.cs:665` | a grass snake | a grass snake |
| `TutorialFarm.cs:678` | a snake corpse | a snake corpse |

## Tobin, pet resurrection, and the starter elixir

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialPetCare.cs:47` | If your pet dies, wait a few minutes for its body to fade, then visit a vet or use an elixir of rebirth. | If your pet dies, wait for its body to disappear, then take its ghost to a vet or use an elixir of rebirth. |
| `TutorialPetCare.cs:62` | The vet can bring your pet back | Bring your pet back to life |
| `TutorialPetCare.cs:63` | Choose a pet. It loses a little skill (0.2 in each) when it comes back. | Choose the pet you want to bring back. It loses 0.2 points in every skill. |
| `TutorialPetCare.cs:69` | Bring back {pets[i].Name} ({(fee == 0 ? "free while you are Young" : $"{fee} gold from your bank")}) | Bring back {pets[i].Name} ({(fee == 0 ? "free while you are Young" : $"{fee} gold from your bank")}) |
| `TutorialPetCare.cs:73` | Not now | Not now |
| `TutorialPetCare.cs:129` | Ah, your friend's in a bad way. Let me see what I can do. | I can bring your pet back. Choose its name in the window. |
| `TutorialPetCare.cs:141` | [501041] Target is not dead. | Your pet is still alive. |
| `TutorialPetCare.cs:145` | [500643] Target is too far away. | Bring your pet closer to you, then try again. |
| `TutorialPetCare.cs:149` | [1113200] You must be the owner of that pet to have it resurrected. | Only this pet's owner can ask the vet to bring it back. |
| `TutorialPetCare.cs:153` | [1113279] That creature's spirit lacks cohesion. Try again in a few minutes. | Wait until your pet's body disappears, then ask the vet again. |
| `TutorialPetCare.cs:157` | [1060020] Unfortunately, you do not have enough cash in your bank to cover the cost of the healing. | You need more gold in your bank to pay the vet. |
| `TutorialPetCare.cs:175` | [1060398] ~1_AMOUNT~ gold has been withdrawn from your bank box. | You paid the vet ~1_AMOUNT~ gold from your bank. |
| `TutorialPetCare.cs:178` | There. Good as new, or near enough. | Your pet is alive again. |
| `TutorialPetCare.cs:214` | Brings your dead bonded pet back, once its body has faded | Brings a bonded pet back after its body disappears |

## Combat and magic lesson instructions

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialWingTrials.cs:43` | tutorial loaner:  | tutorial loaner:  |
| `TutorialWingTrials.cs:68` | Swords: a longsword | Swords: a longsword |
| `TutorialWingTrials.cs:69` | Macing: a mace | Macing: a mace |
| `TutorialWingTrials.cs:70` | Fencing: a kryss | Fencing: a narrow kryss sword |
| `TutorialWingTrials.cs:71` | Archery: a bow and arrows | Archery: a bow and arrows |
| `TutorialWingTrials.cs:72` | Throwing: a boomerang (gargoyles) | Throwing: a boomerang for gargoyles |
| `TutorialWingTrials.cs:73` | Wrestling: your fists | Wrestling: fight with empty hands |
| `TutorialWingTrials.cs:77` | Resisting Spells is not trained here: it grows when spells are cast at you, and it softens what they do. | Resisting Spells helps you resist some spell effects. It can improve when certain spells are cast on you; this lesson does not train it. |
| `TutorialWingTrials.cs:79` | Spellweaving is not taught by a book: it opens with the Arcanist's quest, "Patience", in the Heartwood, the elven city in Ilshenar. | Spellweaving starts with a quest, not just a spellbook. In Heartwood, look for the quest called Patience to begin learning it. |
| `TutorialWingTrials.cs:153` | Pick a weapon on this page; the yard lends it (and a buckler for one hand). Then land three hits on the sparring echo with it. | Choose a weapon below; it is loaned for this lesson. Hit the blue human figure named 'a sparring echo' three times with that weapon, or with empty hands for Wrestling. |
| `TutorialWingTrials.cs:155` | Equip the loaned weapon if it is not in your hand, press Tab for war mode and double-click the sparring echo. Three hits with {Weapons[choice].Skill} finish it. | Drag the loaned weapon onto your character's picture if needed, or empty your hands for Wrestling. Press Tab to enter war mode, then double-click the blue sparring echo and land three hits. |
| `TutorialWingTrials.cs:157` | Double-click a loaned bandage and target yourself, then the wounded villager beside you. The yard lends you some Healing for the lesson. | Double-click a loaned bandage in your backpack, then click yourself and wait for it to heal you. Use another bandage on the wounded villager beside you. |
| `TutorialWingTrials.cs:159` | Open the loaned spellbook, double-click Magic Arrow and click the training echo. Its reagent, sulfurous ash, is loaned too. | Double-click the loaned spellbook, double-click Magic Arrow, then click the blue human figure named 'a training echo'. The sulfurous ash needed for this spell is in your backpack. |
| `TutorialWingTrials.cs:161` | Open the loaned necromancer's book, double-click Pain Spike and click the training echo. Its reagents, grave dust and pig iron, are loaned too. | Double-click the loaned necromancer spellbook, double-click Pain Spike, then click the blue training echo. The grave dust and pig iron needed for this spell are in your backpack. |
| `TutorialWingTrials.cs:163` | Stand next to the wounded villager (Close Wounds reaches two steps), open the loaned Book of Chivalry, double-click Close Wounds and click the villager. The yard lends you tithing points to pay for it. | Stand within two steps of the wounded villager, double-click the loaned Book of Chivalry, then double-click Close Wounds and click the villager. The lesson supplies the tithing points this spell costs. |
| `TutorialWingTrials.cs:165` | Equip the loaned katana, click Honorable Execution in the Book of Bushido, then press Tab and double-click the training echo to strike. | Drag the loaned katana onto your character's picture, then double-click the Book of Bushido and click Honorable Execution. Press Tab for war mode, then double-click the blue training echo. |
| `TutorialWingTrials.cs:167` | Equip the loaned katana, click Focus Attack in the Book of Ninjitsu, then press Tab and double-click the training echo to strike. | Drag the loaned katana onto your character's picture, then double-click the Book of Ninjitsu and click Focus Attack. Press Tab for war mode, then double-click the blue training echo. |
| `TutorialWingTrials.cs:169` | Open the loaned mystic book, double-click Eagle Strike and click the training echo. Its reagents (bloodmoss, bone, spider's silk, mandrake root) are loaned too. | Double-click the loaned mystic book, double-click Eagle Strike, then click the blue training echo. The bloodmoss, bone, spider's silk, and mandrake root needed for this spell are in your backpack. |
| `TutorialWingTrials.cs:180` | Visit a healer first. A ghost can double-click the tutorial healer. | Visit Sera the healer at the farm gate and double-click her. Click Resurrect to return to life before starting a lesson. |
| `TutorialWingTrials.cs:218` | the training echo | the blue training echo |
| `TutorialWingTrials.cs:236` | The training yard is blocked just now. Ask a member of staff. | There is no room to set up this lesson in the training yard. Ask a staff member for help. |
| `TutorialWingTrials.cs:308` | The yard's loans are yours until the lesson ends. They stay here: leave the yard and they go back. | Keep the loaned supplies with you in this lesson area. They disappear when you leave or finish the lesson. |
| `TutorialWingTrials.cs:327` | You have a weapon for this lesson. Reset it to pick another. | You already chose a weapon for this lesson. Click Restart this lesson to choose another. |
| `TutorialWingTrials.cs:334` | Throwing weapons are for gargoyles. Pick another weapon. | Only gargoyles can use throwing weapons. Choose a different weapon for this lesson. |
| `TutorialWingTrials.cs:386` | spellbook | spellbook |
| `TutorialWingTrials.cs:386` | necromancer spellbook | necromancer spellbook |
| `TutorialWingTrials.cs:386` | book of chivalry | book of chivalry |
| `TutorialWingTrials.cs:387` | book of bushido | book of bushido |
| `TutorialWingTrials.cs:387` | book of ninjitsu | book of ninjitsu |
| `TutorialWingTrials.cs:387` | mystic book | mystic book |
| `TutorialWingTrials.cs:388` | sulfurous ash | sulfurous ash |
| `TutorialWingTrials.cs:388` | grave dust | grave dust |
| `TutorialWingTrials.cs:388` | pig iron | pig iron |
| `TutorialWingTrials.cs:388` | bloodmoss | bloodmoss |
| `TutorialWingTrials.cs:389` | bone | bone |
| `TutorialWingTrials.cs:389` | spider's silk | spider's silk |
| `TutorialWingTrials.cs:389` | mandrake root | mandrake root |
| `TutorialWingTrials.cs:389` | bandage | bandage |
| `TutorialWingTrials.cs:390` | arrow | arrow |
| `TutorialWingTrials.cs:390` | buckler | buckler |
| `TutorialWingTrials.cs:390` | longsword | longsword |
| `TutorialWingTrials.cs:390` | mace | mace |
| `TutorialWingTrials.cs:390` | kryss | kryss |
| `TutorialWingTrials.cs:391` | bow | bow |
| `TutorialWingTrials.cs:391` | boomerang | boomerang |
| `TutorialWingTrials.cs:391` | katana | katana |
| `TutorialWingTrials.cs:419` | {trial.Station.Title}: done. The yard has its loans back. | {trial.Station.Title}: finished. The loaned supplies have been returned. |
| `TutorialWingTrials.cs:494` | Loaned things stay with you in the yard; that one went back. | That loaned item disappeared because you dropped it or moved it out of your belongings. Keep lesson supplies equipped or in your backpack. |
| `TutorialWingTrials.cs:529` | Good. Now the wounded villager. | You healed yourself. Double-click another bandage, then click the wounded villager beside you. |
| `TutorialWingTrials.cs:567` | Hit {trial.Hits} of {HitsToFinish}. | Hits landed: {trial.Hits} of {HitsToFinish}. |
| `TutorialWingTrials.cs:601` | Good. Now bandage yourself. | You healed the villager. Double-click another bandage, then click yourself. |
| `TutorialWingTrials.cs:624` | Done. The yard has its loans back. Rook has the next lesson. | Lesson finished and loaned supplies returned. Double-click Rook to choose another lesson. |
| `TutorialWingTrials.cs:647` | Back to Rook | Back to Rook |
| `TutorialWingTrials.cs:647` | Hint and arrow | Hint and arrow |
| `TutorialWingTrials.cs:648` | Reset this trial | Restart this lesson |
| `TutorialWingTrials.cs:649` | Stop and return the loans | Stop and return supplies |
| `TutorialWingTrials.cs:674` | Stopped. The yard has its loans back. | Lesson stopped and loaned supplies returned. Double-click Rook to start another lesson. |
| `TutorialWingTrials.cs:688` | the training yard | the training yard |
| `TutorialWingTrials.cs:736` | a wounded villager | a wounded villager |
| `TutorialWingTrials.cs:736` | a sparring echo | a sparring echo |
| `TutorialWingTrials.cs:736` | a training echo | a training echo |

## Gathering, crafting, animals, and skill checklists

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialTradeTrials.cs:38` | tutorial prop:  | tutorial prop:  |
| `TutorialTradeTrials.cs:65` | the trades yard, south-east of the training yard | the trades yard, southeast of the training yard |
| `TutorialTradeTrials.cs:70` | Herbalism is not built here yet: the Order of the Alembic will teach it. Camping is your fire, your rest and your safe logout outdoors. | Herbalism is not available yet. In this lesson, double-click kindling to light a campfire. |
| `TutorialTradeTrials.cs:72` | Imbuing is not taught in this yard: it puts magic properties on crafted gear at a soul forge, and gargoyle cities teach it. | Imbuing adds magical properties to equipment at a soul forge. This tutorial does not teach it. |
| `TutorialTradeTrials.cs:74` | Forensic Evaluation is explained, not trained here: it tells you who looted a corpse and who picked a lock. | Forensic Evaluation can reveal who looted a body or picked a lock. This tutorial explains it without giving you a practice task. |
| `TutorialTradeTrials.cs:80` | Mining: dig ore from the practice vein | Mining: dig ore from the gray stone patch |
| `TutorialTradeTrials.cs:81` | Double-click the loaned pickaxe and click the practice vein (the gray cave floor beside you). Keep digging until ore comes up; the ore is yours to keep. | Double-click the loaned pickaxe in your backpack, then click the gray stone patch named practice vein. Repeat until you dig up ore, which you can keep. |
| `TutorialTradeTrials.cs:83` | Lumberjacking: chop logs from the practice tree | Lumberjacking: chop logs from the practice tree |
| `TutorialTradeTrials.cs:84` | The loaned hatchet is in your hands. Double-click it and click the walnut tree beside you until logs come down; the logs are yours to keep. | Double-click the loaned hatchet, then click the walnut tree beside you. Repeat until you get logs, which you can keep. |
| `TutorialTradeTrials.cs:86` | Fishing: catch something in the practice pond | Fishing: catch something in the small practice pond |
| `TutorialTradeTrials.cs:87` | Double-click the loaned fishing pole and click the water of the practice pond beside you. Keep casting until you catch something; it is yours to keep. | Double-click the loaned fishing pole in your backpack, then click the water in the small practice pond. Repeat until you catch something, which you can keep. |
| `TutorialTradeTrials.cs:89` | Camping: light a campfire | Camping: light a campfire with kindling |
| `TutorialTradeTrials.cs:90` | Double-click the loaned kindling in your backpack to light a campfire on the ground beside you. | Double-click the loaned kindling in your backpack to light a campfire beside you. |
| `TutorialTradeTrials.cs:95` | Blacksmithy: make a dagger at the anvil | Blacksmithy: make a dagger at the anvil |
| `TutorialTradeTrials.cs:95` | Arms Lore: study your dagger | Arms Lore: use on the dagger you made |
| `TutorialTradeTrials.cs:96` | Stand by the anvil and forge. Double-click the loaned smith's hammer, open Bladed and make a dagger from the loaned iron ingots. Then use Arms Lore on it. | Beside the anvil and forge, double-click the loaned smith's hammer, choose Bladed, then make a Dagger. Open Skills on your character window, use Arms Lore, and click your dagger. |
| `TutorialTradeTrials.cs:99` | Tailoring: sew a skullcap | Tailoring: sew a skullcap |
| `TutorialTradeTrials.cs:100` | Double-click the loaned sewing kit, open Hats and make a skullcap from the loaned cloth. | Double-click the loaned sewing kit in your backpack. Choose Hats, then make a Skullcap with the loaned cloth. |
| `TutorialTradeTrials.cs:103` | Carpentry: cut barrel staves | Carpentry: make barrel staves |
| `TutorialTradeTrials.cs:104` | Double-click the loaned saw, open Other and make barrel staves from the loaned boards. | Double-click the loaned saw in your backpack. Choose Other, then make Barrel Staves with the loaned boards. |
| `TutorialTradeTrials.cs:107` | Tinkering: make scissors | Tinkering: make scissors |
| `TutorialTradeTrials.cs:107` | Item Identification: identify the odd curio | Item Identification: use on the odd blue curio |
| `TutorialTradeTrials.cs:108` | Double-click the loaned tinker's tools, open Tools and make scissors from the loaned ingots. Then use Item Identification on the odd curio in your backpack. | Double-click the loaned tinker's tools, choose Tools, then make Scissors. Open Skills on your character window, use Item Identification, and click the odd blue curio in your backpack. |
| `TutorialTradeTrials.cs:111` | Alchemy: brew a refresh potion | Alchemy: make a refresh potion |
| `TutorialTradeTrials.cs:111` | Taste Identification: taste the apple | Taste Identification: use on the loaned apple |
| `TutorialTradeTrials.cs:112` | Double-click the loaned mortar and pestle, open Refresh and brew a refresh potion (black pearl and an empty bottle). Then use Taste Identification on the loaned apple. | Double-click the loaned mortar and pestle, choose Refresh, then make a Refresh Potion. Open Skills on your character window, use Taste Identification, and click the loaned apple. |
| `TutorialTradeTrials.cs:115` | Fletching: make kindling | Fletching: make kindling |
| `TutorialTradeTrials.cs:116` | Double-click the loaned fletcher's tools, open Materials and make kindling from the loaned logs. | Double-click the loaned fletcher's tools in your backpack. Choose Materials, then make Kindling with the loaned logs. |
| `TutorialTradeTrials.cs:119` | Cooking: make dough | Cooking: make dough |
| `TutorialTradeTrials.cs:120` | Double-click the loaned skillet, open Ingredients and make dough from the loaned flour and the pitcher of water. | Double-click the loaned skillet in your backpack. Choose Ingredients, then make Dough with the loaned flour and water. |
| `TutorialTradeTrials.cs:123` | Inscription: write a Magic Arrow scroll | Inscription: write a Magic Arrow scroll |
| `TutorialTradeTrials.cs:124` | Double-click the loaned scribe's pen, open First Circle and write Magic Arrow (the loaned spellbook holds the spell; it needs a blank scroll and sulfurous ash). | Double-click the loaned scribe's pen in your backpack. Choose First Circle, then make a Magic Arrow scroll with the loaned supplies. |
| `TutorialTradeTrials.cs:127` | Cartography: draw a local map | Cartography: draw a local map |
| `TutorialTradeTrials.cs:128` | Double-click the loaned mapmaker's pen, open Maps and draw a local map on a loaned blank map. | Double-click the loaned mapmaker's pen in your backpack. Choose Maps, then make a Local Map on a loaned blank map. |
| `TutorialTradeTrials.cs:132` | the tutorial farm's field, beside the animal pen (enter by the gate) | the farm's animal pen, through the gate |
| `TutorialTradeTrials.cs:134` | Herding: move the tutorial goat with the crook | Herding: use the crook on the goat, then click a spot |
| `TutorialTradeTrials.cs:135` | Animal Taming: tame the tutorial goat | Animal Taming: use on the practice goat |
| `TutorialTradeTrials.cs:136` | Animal Lore: it rolls as you tame; or study your goat | Animal Lore: use on your goat or gain it while taming |
| `TutorialTradeTrials.cs:137` | Veterinary: bandage it | Veterinary: double-click a bandage, then your goat |
| `TutorialTradeTrials.cs:139` | The tutorial goat is in the pen. Double-click the loaned crook, click the goat, then a spot to send it. Then use Animal Taming on it (taming rolls Animal Lore too; or use Animal Lore on it once it is yours) and a loaned bandage on it. It goes back to the farm when the lesson ends. | Double-click the loaned crook, click the practice goat, then click a place to send it. Use Animal Taming and Animal Lore from Skills, then bandage the goat; it stays at the farm. |
| `TutorialTradeTrials.cs:144` | Peacemaking: calm an echo | Peacemaking: use on a blue training echo |
| `TutorialTradeTrials.cs:145` | Provocation: turn one echo on the other | Provocation: use on one echo, then the other |
| `TutorialTradeTrials.cs:146` | Discordance: weaken an echo | Discordance: use on a blue training echo |
| `TutorialTradeTrials.cs:148` | Use Peacemaking, Provocation and Discordance on the two training echoes (Provocation: the first echo, then the second). Pick the loaned lute when asked for an instrument; Musicianship rolls every time. | Open Skills on your character window and use Peacemaking, Provocation, and Discordance on the two blue human figures. Choose the loaned lute when asked; for Provocation, click one figure, then the other. |
| `TutorialTradeTrials.cs:153` | Detecting Hidden: target the practice chest | Detecting Hidden: use on the wooden practice chest |
| `TutorialTradeTrials.cs:154` | Remove Trap: disarm the practice chest | Remove Trap: use on the wooden practice chest |
| `TutorialTradeTrials.cs:155` | Lockpicking: a loaned lockpick on the chest | Lockpicking: use a loaned lockpick on the chest |
| `TutorialTradeTrials.cs:156` | Stealing: lift the purse from the chest (hands free) | Stealing: empty your hands and steal the purse |
| `TutorialTradeTrials.cs:157` | Snooping: open the mark's backpack | Snooping: double-click the mark's backpack |
| `TutorialTradeTrials.cs:158` | Begging: beg from the mark | Begging: use on the blue practice person |
| `TutorialTradeTrials.cs:159` | Poisoning: the loaned poison on the loaned dagger | Poisoning: select the loaned poison, then the dagger |
| `TutorialTradeTrials.cs:160` | Tracking: use it and pick a kind | Tracking: use the skill and choose a category |
| `TutorialTradeTrials.cs:161` | Hiding: hide | Hiding: use the skill until you hide |
| `TutorialTradeTrials.cs:162` | Stealth: while hidden, use Stealth | Stealth: hide, then use Stealth |
| `TutorialTradeTrials.cs:164` | Ten small steps on the practice chest and the mark (a tutorial-only dummy). Nothing here touches another player. Snooping and poisoning cost a little karma, as they always do. Stand beside the chest to pick it and to steal. | Use Skills in your character window for the checklist tasks on the wooden chest and blue practice person. For Snooping, double-click the person, then its backpack; snooping and poisoning can lower your karma. |
| `TutorialTradeTrials.cs:264` | pickaxe | pickaxe |
| `TutorialTradeTrials.cs:264` | hatchet | hatchet |
| `TutorialTradeTrials.cs:264` | fishing pole | fishing pole |
| `TutorialTradeTrials.cs:264` | kindling | kindling |
| `TutorialTradeTrials.cs:265` | smith's hammer | smith's hammer |
| `TutorialTradeTrials.cs:265` | sewing kit | sewing kit |
| `TutorialTradeTrials.cs:265` | saw | saw |
| `TutorialTradeTrials.cs:265` | tinker's tools | tinker's tools |
| `TutorialTradeTrials.cs:266` | mortar and pestle | mortar and pestle |
| `TutorialTradeTrials.cs:266` | fletcher's tools | fletcher's tools |
| `TutorialTradeTrials.cs:266` | skillet | skillet |
| `TutorialTradeTrials.cs:267` | scribe's pen | scribe's pen |
| `TutorialTradeTrials.cs:267` | mapmaker's pen | mapmaker's pen |
| `TutorialTradeTrials.cs:267` | iron ingots | iron ingots |
| `TutorialTradeTrials.cs:267` | cloth | cloth |
| `TutorialTradeTrials.cs:268` | boards | boards |
| `TutorialTradeTrials.cs:268` | logs | logs |
| `TutorialTradeTrials.cs:268` | black pearl | black pearl |
| `TutorialTradeTrials.cs:268` | empty bottles | empty bottles |
| `TutorialTradeTrials.cs:268` | apple | apple |
| `TutorialTradeTrials.cs:269` | sack of flour | sack of flour |
| `TutorialTradeTrials.cs:269` | pitcher of water | pitcher of water |
| `TutorialTradeTrials.cs:269` | blank scrolls | blank scrolls |
| `TutorialTradeTrials.cs:270` | blank maps | blank maps |
| `TutorialTradeTrials.cs:270` | shepherd's crook | shepherd's crook |
| `TutorialTradeTrials.cs:270` | lute | lute |
| `TutorialTradeTrials.cs:270` | lockpicks | lockpicks |
| `TutorialTradeTrials.cs:271` | dagger | dagger |
| `TutorialTradeTrials.cs:271` | lesser poison potion | lesser poison potion |
| `TutorialTradeTrials.cs:271` | recall rune | recall rune |
| `TutorialTradeTrials.cs:272` | odd curio | odd curio |

## Walking tours and stop text

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialTradeTrials.cs:168` | the first stop | the first stop |
| `TutorialTradeTrials.cs:169` | The farmhouse porch | The farmhouse porch |
| `TutorialTradeTrials.cs:169` | The bank | The bank |
| `TutorialTradeTrials.cs:170` | A short walk. Follow the arrow to each stop. | Follow the arrow to the first stop. Walk close to each stop to read its lesson. |
| `TutorialTradeTrials.cs:173` | the farmhouse porch | the farmhouse porch |
| `TutorialTradeTrials.cs:174` | A house is placed from a deed on open land. Inside it you lock things down, secure containers and name co-owners and friends; boxes open in your own house, too. TazUO: Options can make roofs and walls transparent near you. | Use a house deed on open land where housing is allowed, then lock items in place and secure containers inside. TazUO's Options can make nearby roofs and walls transparent. |
| `TutorialTradeTrials.cs:175` | the bank | the bank |
| `TutorialTradeTrials.cs:176` | House deeds come from architects and real estate brokers in the big cities. Keep a deed in your bank box until you place it; a house must be refreshed by visiting it, or it decays. | Keep a house deed in your bank until you are ready to use it. Visit your house regularly to refresh it and prevent decay. |
| `TutorialTradeTrials.cs:178` | the first stop | the first stop |
| `TutorialTradeTrials.cs:179` | The moongate | The moongate |
| `TutorialTradeTrials.cs:179` | The plaza | The plaza |
| `TutorialTradeTrials.cs:180` | A short walk. Follow the arrow to each stop. The loaned rune is a blank recall rune: look at it, then it goes back. | Follow the arrow to each stop and read the lesson when you arrive. The blank recall rune in your backpack is a loan and disappears when the tour ends. |
| `TutorialTradeTrials.cs:183` | the moongate | the moongate |
| `TutorialTradeTrials.cs:184` | Moongates link the cities and the facets: step in and pick where to go. Boats sail from the docks; a ship's deed comes from a shipwright. | This practice gate works only during the main travel lesson and returns you to the plaza. For travel elsewhere, public moongates offer destinations and shipwrights sell boat deeds. |
| `TutorialTradeTrials.cs:185` | the plaza | the plaza |
| `TutorialTradeTrials.cs:186` | A recall rune remembers a place: Mark it (Magery, fourth circle), then Recall or Gate Travel to it; Sacred Journey does it for paladins. A runebook holds sixteen. TazUO: the World Map shows where you are. | A recall rune stores a location when you cast Mark on it. Return with Recall, Gate Travel, or Sacred Journey; a runebook stores up to 16 runes. |
| `TutorialTradeTrials.cs:188` | the first stop | the first stop |
| `TutorialTradeTrials.cs:189` | The training yard | The training yard |
| `TutorialTradeTrials.cs:189` | The healer | The healer |
| `TutorialTradeTrials.cs:189` | The plaza | The plaza |
| `TutorialTradeTrials.cs:190` | A short walk. Follow the arrow to each stop. | Follow the arrow to the first stop. Walk close to each stop to read its lesson. |
| `TutorialTradeTrials.cs:193` | the training yard | the training yard |
| `TutorialTradeTrials.cs:194` | Names have colors. Blue is innocent; gray may be attacked (a criminal, or a monster); red is a murderer. Attack or steal from a blue and you turn gray for a while. | Blue names usually mean innocent; gray names can be attacked, and red names mark murderers. Harming an innocent can make you gray for a while. |
| `TutorialTradeTrials.cs:195` | the healer | the healer |
| `TutorialTradeTrials.cs:196` | Karma is your good name, fame your renown; together they give your title. Killing innocents earns murder counts, and five make you red. Healers resurrect the dead, but not the red. | Karma and fame affect your title; killing innocent players can give you murder counts. Five murder counts make your name red, and some healers will refuse to help you. |
| `TutorialTradeTrials.cs:197` | the plaza | the plaza |
| `TutorialTradeTrials.cs:198` | Towns have guards. If a gray or red attacks you here, say "guards". Trammel, this facet, forbids attacking other players at all; Felucca allows it. | In a guarded town, say 'guards' if someone attacks you unlawfully. Trammel generally prevents attacks on other players; Felucca allows them. |
| `TutorialTradeTrials.cs:200` | the first stop | the first stop |
| `TutorialTradeTrials.cs:201` | The League field office | The League field office |
| `TutorialTradeTrials.cs:201` | The bank | The bank |
| `TutorialTradeTrials.cs:201` | Rook | Rook |
| `TutorialTradeTrials.cs:202` | A short walk. Follow the arrow to each stop. | Follow the arrow to the first stop. Walk close to each stop to read its lesson. |
| `TutorialTradeTrials.cs:205` | the League field office | the League field office |
| `TutorialTradeTrials.cs:206` | The League of Extraordinary Citizens: ranks, jobs and their rewards. Elara Voss signs you up when you choose. | Double-click Elara Voss to read about the League's jobs, ranks, and rewards. You can choose whether to join. |
| `TutorialTradeTrials.cs:207` | the bank | the bank |
| `TutorialTradeTrials.cs:208` | Loot boxes open only in a guarded town or your own house. TazUO: Autoloot, the Scavenger and Nearby loot gather for you; vendors take advanced shop, trade and auto buy and sell. | Double-click reward boxes in guarded towns or your own house to open them. TazUO also has Autoloot, Scavenger, Nearby loot, and vendor shopping tools. |
| `TutorialTradeTrials.cs:209` | Rook | Rook |
| `TutorialTradeTrials.cs:210` | Levels and loops: each loop raises your level cap, and the world remembers you. Achievements pay as you play. Extra ring, bracelet and toe ring slots open as you earn them: type [accessories. TazUO: the skill progress bar, and Legion scripting for the advanced. | Achievements reward your progress; type [accessories to see your extra jewelry slots. Graduation records your first loop, but level resets and higher level caps are not active yet. |

## Shared optional-lesson directions, progress, and practice labels

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialTradeTrials.cs:229` | Follow the arrow to the training yard, east of the farm gate. The lesson starts there. | Follow the arrow to the training yard, east of the farm gate. Your lesson begins when you arrive. |
| `TutorialTradeTrials.cs:230` | Follow the arrow to {t.Where}. The lesson starts there. | Follow the arrow to {t.Where}. Your lesson begins when you arrive. |
| `TutorialTradeTrials.cs:233` | You left the training yard, so the lesson stopped and the yard took its loans back. Start it again at Rook. | You left the training yard, so this lesson stopped and its loaned supplies disappeared. Double-click Rook to start it again. |
| `TutorialTradeTrials.cs:235` | You went too far from New Haven, so the tour stopped. Start it again at Rook. | You went too far from New Haven, so the tour stopped. Double-click Rook to start it again. |
| `TutorialTradeTrials.cs:236` | You left {t.Where}, so the lesson stopped and its loans went back. Start it again at Rook. | You left {t.Where}, so this lesson stopped and its loaned supplies disappeared. Double-click Rook to start it again. |
| `TutorialTradeTrials.cs:241` | the training yard | the training yard |
| `TutorialTradeTrials.cs:248` | the farm's animal pen | the farm's animal pen |
| `TutorialTradeTrials.cs:248` | the trades yard | the trades yard |
| `TutorialTradeTrials.cs:251` | This station has no lesson. Ask a member of staff. | This lesson has no activity yet. Ask a staff member for help. |
| `TutorialTradeTrials.cs:258` | Done:  | Done:  |
| `TutorialTradeTrials.cs:258` | To do:  | To do:  |
| `TutorialTradeTrials.cs:298` | This lesson's place is blocked just now. Ask a member of staff. | There is no room to set up this lesson here. Ask a staff member for help. |
| `TutorialTradeTrials.cs:309` | practice vein | practice vein |
| `TutorialTradeTrials.cs:315` | practice tree | practice tree |
| `TutorialTradeTrials.cs:316` | practice tree | practice tree |
| `TutorialTradeTrials.cs:326` | practice pond | practice pond |
| `TutorialTradeTrials.cs:341` | anvil | anvil |
| `TutorialTradeTrials.cs:342` | forge | forge |
| `TutorialTradeTrials.cs:432` | The yard's loans are yours until the lesson ends. They stay here: leave and they go back. | Keep the loaned supplies with you in this lesson area. They disappear when you leave or finish the lesson. |
| `TutorialTradeTrials.cs:461` | a tutorial mark | a tutorial mark |
| `TutorialTradeTrials.cs:462` | a brass trinket | a brass trinket |
| `TutorialTradeTrials.cs:470` | practice chest | practice chest |
| `TutorialTradeTrials.cs:471` | a purse of glass coins | a purse of glass coins |
| `TutorialTradeTrials.cs:595` | Step done: {label} ({trial.Steps.Count} of {t.Steps.Length}). | Finished: {label} ({trial.Steps.Count} of {t.Steps.Length}). |
| `TutorialTradeTrials.cs:616` | a brass curio, worth nothing at all | a brass curio with no value |
| `TutorialTradeTrials.cs:616` | an odd curio (unidentified) | an odd blue curio (unidentified) |
| `TutorialTradeTrials.cs:635` | a tutorial goat | a tutorial goat |

## Lesson titles, skill lists, supplies, and fallback-page locations

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialStations.cs:59` | Walking, running and the camera | Walk and run |
| `TutorialStations.cs:60` | Options | Options |
| `TutorialStations.cs:60` | Global Scaling | Global Scaling |
| `TutorialStations.cs:60` | Hotkeys | Hotkeys |
| `TutorialStations.cs:60` | New Haven plaza | New Haven plaza |
| `TutorialStations.cs:61` | Your backpack | Your backpack |
| `TutorialStations.cs:62` | Grid Containers | Grid Containers |
| `TutorialStations.cs:62` | Item comparison | Item comparison |
| `TutorialStations.cs:62` | New Haven plaza | New Haven plaza |
| `TutorialStations.cs:63` | Your paperdoll | Your character window and clothes |
| `TutorialStations.cs:64` | Alternate Paperdoll | Alternate Paperdoll |
| `TutorialStations.cs:64` | Durability gump | Durability gump |
| `TutorialStations.cs:64` | New Haven plaza | New Haven plaza |
| `TutorialStations.cs:65` | Speaking and the journal | Speak and read your Journal |
| `TutorialStations.cs:66` | Journal and filters | Journal and filters |
| `TutorialStations.cs:66` | TTF fonts | TTF fonts |
| `TutorialStations.cs:66` | Nameplates | Nameplates |
| `TutorialStations.cs:66` | New Haven plaza | New Haven plaza |
| `TutorialStations.cs:67` | Death and resurrection | Death and resurrection |
| `TutorialStations.cs:68` | Info Bar | Info Bar |
| `TutorialStations.cs:68` | the Healer's Hall and the graveyard | the farm gate, beside Sera the healer |
| `TutorialStations.cs:69` | The bank | The bank |
| `TutorialStations.cs:70` | Grid Containers | Grid Containers |
| `TutorialStations.cs:70` | New Haven Bank | New Haven Bank |
| `TutorialStations.cs:71` | Getting around | Getting around |
| `TutorialStations.cs:72` | World Map | World Map |
| `TutorialStations.cs:72` | Macros | Macros |
| `TutorialStations.cs:72` | the moongate | the moongate |
| `TutorialStations.cs:73` | The League of Extraordinary Citizens | The League of Extraordinary Citizens |
| `TutorialStations.cs:74` | the League field office | the League field office |
| `TutorialStations.cs:75` | The loop (a vision) | Watch a loop vision |
| `TutorialStations.cs:76` | Skill progress bar | Skill progress bar |
| `TutorialStations.cs:76` | a vision near the sword fragment | the bright blue rune stone at the farm gate |
| `TutorialStations.cs:79` | Pick your weapon | Pick your weapon |
| `TutorialStations.cs:80` | Swords | Swords |
| `TutorialStations.cs:80` | Macing | Macing |
| `TutorialStations.cs:80` | Fencing | Fencing |
| `TutorialStations.cs:80` | Archery | Archery |
| `TutorialStations.cs:80` | Throwing | Throwing |
| `TutorialStations.cs:80` | Wrestling | Wrestling |
| `TutorialStations.cs:80` | Tactics | Tactics |
| `TutorialStations.cs:80` | Anatomy | Anatomy |
| `TutorialStations.cs:80` | Parrying | Parrying |
| `TutorialStations.cs:80` | Focus | Focus |
| `TutorialStations.cs:81` | Resisting Spells | Resisting Spells |
| `TutorialStations.cs:82` | Custom health bars | Custom health bars |
| `TutorialStations.cs:82` | Nameplate healthbars | Nameplate healthbars |
| `TutorialStations.cs:82` | Damage hues | Damage hues |
| `TutorialStations.cs:82` | Buff and cooldown bars | Buff and cooldown bars |
| `TutorialStations.cs:82` | a starter weapon of your pick | a loaned weapon you choose |
| `TutorialStations.cs:83` | the combat yard | the training yard, east of the farm gate |
| `TutorialStations.cs:84` | Bandages | Bandages |
| `TutorialStations.cs:84` | Healing | Healing |
| `TutorialStations.cs:84` | Anatomy | Anatomy |
| `TutorialStations.cs:85` | Auto Bandage | Auto Bandage |
| `TutorialStations.cs:85` | bandages | loaned bandages |
| `TutorialStations.cs:85` | the combat yard | the training yard, east of the farm gate |
| `TutorialStations.cs:88` | Magery | Magery |
| `TutorialStations.cs:88` | Magery | Magery |
| `TutorialStations.cs:88` | Meditation | Meditation |
| `TutorialStations.cs:88` | Eval Int | Evaluating Intelligence |
| `TutorialStations.cs:89` | SpellBar | SpellBar |
| `TutorialStations.cs:89` | Quick spell cast | Quick spell cast |
| `TutorialStations.cs:89` | Spell indicators | Spell indicators |
| `TutorialStations.cs:89` | Counter bar | Counter bar |
| `TutorialStations.cs:89` | a spellbook and reagents | a loaned spellbook and reagents (spell ingredients) |
| `TutorialStations.cs:89` | the Magery school | the training yard, east of the farm gate |
| `TutorialStations.cs:90` | Necromancy | Necromancy |
| `TutorialStations.cs:90` | Necromancy | Necromancy |
| `TutorialStations.cs:90` | Spirit Speak | Spirit Speak |
| `TutorialStations.cs:91` | SpellBar | SpellBar |
| `TutorialStations.cs:91` | a necromancer spellbook | a loaned necromancer spellbook |
| `TutorialStations.cs:91` | the Necromancers Guild Hall | the training yard, east of the farm gate |
| `TutorialStations.cs:92` | Chivalry | Chivalry |
| `TutorialStations.cs:92` | Chivalry | Chivalry |
| `TutorialStations.cs:93` | SpellBar | SpellBar |
| `TutorialStations.cs:93` | a book of chivalry | a loaned Book of Chivalry |
| `TutorialStations.cs:93` | the Warrior's Guild Hall | the training yard, east of the farm gate |
| `TutorialStations.cs:94` | Bushido | Bushido |
| `TutorialStations.cs:94` | Bushido | Bushido |
| `TutorialStations.cs:95` | Buff and cooldown bars | Buff and cooldown bars |
| `TutorialStations.cs:95` | a book of bushido | a loaned Book of Bushido |
| `TutorialStations.cs:95` | the Ninja Dojo | the training yard, east of the farm gate |
| `TutorialStations.cs:96` | Ninjitsu | Ninjitsu |
| `TutorialStations.cs:96` | Ninjitsu | Ninjitsu |
| `TutorialStations.cs:97` | Buff and cooldown bars | Buff and cooldown bars |
| `TutorialStations.cs:97` | a book of ninjitsu | a loaned Book of Ninjitsu |
| `TutorialStations.cs:97` | the Ninja Dojo | the training yard, east of the farm gate |
| `TutorialStations.cs:98` | Mysticism | Mysticism |
| `TutorialStations.cs:98` | Mysticism | Mysticism |
| `TutorialStations.cs:98` | Spellweaving (its quest) | Spellweaving (start with a quest) |
| `TutorialStations.cs:99` | SpellBar | SpellBar |
| `TutorialStations.cs:99` | a mysticism spellbook | a loaned mystic book |
| `TutorialStations.cs:99` | the Magery school | the training yard, east of the farm gate |
| `TutorialStations.cs:102` | Mining | Mining |
| `TutorialStations.cs:102` | Mining | Mining |
| `TutorialStations.cs:103` | Counter bar | Counter bar |
| `TutorialStations.cs:103` | a pickaxe | a loaned pickaxe |
| `TutorialStations.cs:103` | the mine camp | the trades yard, southeast of the training yard |
| `TutorialStations.cs:104` | Lumberjacking | Lumberjacking |
| `TutorialStations.cs:104` | Lumberjacking | Lumberjacking |
| `TutorialStations.cs:105` | a hatchet | a loaned hatchet |
| `TutorialStations.cs:105` | the tutorial farm's edge | the trades yard, southeast of the training yard |
| `TutorialStations.cs:106` | Fishing | Fishing |
| `TutorialStations.cs:106` | Fishing | Fishing |
| `TutorialStations.cs:107` | a fishing pole | a loaned fishing pole |
| `TutorialStations.cs:107` | New Haven docks | the trades yard, southeast of the training yard |
| `TutorialStations.cs:108` | Camping | Camping |
| `TutorialStations.cs:108` | Camping | Camping |
| `TutorialStations.cs:108` | Herbalism (Order of the Alembic, not built) | Herbalism (not available yet) |
| `TutorialStations.cs:109` | kindling | loaned kindling |
| `TutorialStations.cs:109` | the tutorial farm | the trades yard, southeast of the training yard |
| `TutorialStations.cs:112` | Blacksmithy | Blacksmithy |
| `TutorialStations.cs:112` | Blacksmithy | Blacksmithy |
| `TutorialStations.cs:112` | Arms Lore | Arms Lore |
| `TutorialStations.cs:112` | Imbuing | Imbuing |
| `TutorialStations.cs:113` | Counter bar | Counter bar |
| `TutorialStations.cs:113` | Grid highlighting by property | Grid highlighting by property |
| `TutorialStations.cs:113` | Item database | Item database |
| `TutorialStations.cs:113` | Organizer agent | Organizer agent |
| `TutorialStations.cs:113` | a smith's hammer | a loaned smith's hammer |
| `TutorialStations.cs:113` | Forge and Anvil | the trades yard, southeast of the training yard |
| `TutorialStations.cs:114` | Tailoring | Tailoring |
| `TutorialStations.cs:114` | Tailoring | Tailoring |
| `TutorialStations.cs:115` | Counter bar | Counter bar |
| `TutorialStations.cs:115` | a sewing kit | a loaned sewing kit |
| `TutorialStations.cs:115` | A Stitch In Time | the trades yard, southeast of the training yard |
| `TutorialStations.cs:116` | Carpentry | Carpentry |
| `TutorialStations.cs:116` | Carpentry | Carpentry |
| `TutorialStations.cs:117` | a saw | a loaned saw |
| `TutorialStations.cs:117` | Carpenters of New Haven | the trades yard, southeast of the training yard |
| `TutorialStations.cs:118` | Tinkering | Tinkering |
| `TutorialStations.cs:118` | Tinkering | Tinkering |
| `TutorialStations.cs:118` | Item ID | Item Identification |
| `TutorialStations.cs:119` | tinker's tools | loaned tinker's tools |
| `TutorialStations.cs:119` | Springs N Things | the trades yard, southeast of the training yard |
| `TutorialStations.cs:120` | Alchemy | Alchemy |
| `TutorialStations.cs:120` | Alchemy | Alchemy |
| `TutorialStations.cs:120` | Taste ID | Taste Identification |
| `TutorialStations.cs:121` | a mortar and pestle | a loaned mortar and pestle |
| `TutorialStations.cs:121` | the Little Shop of Alchemy | the trades yard, southeast of the training yard |
| `TutorialStations.cs:122` | Bowcraft and Fletching | Bowcraft and Fletching |
| `TutorialStations.cs:122` | Fletching | Fletching |
| `TutorialStations.cs:123` | fletcher's tools | loaned fletcher's tools |
| `TutorialStations.cs:123` | the Bowyer | the trades yard, southeast of the training yard |
| `TutorialStations.cs:124` | Cooking | Cooking |
| `TutorialStations.cs:124` | Cooking | Cooking |
| `TutorialStations.cs:125` | a skillet | a loaned skillet |
| `TutorialStations.cs:125` | the Bountiful Harvest Inn | the trades yard, southeast of the training yard |
| `TutorialStations.cs:126` | Inscription | Inscription |
| `TutorialStations.cs:126` | Inscription | Inscription |
| `TutorialStations.cs:127` | a scribe's pen | a loaned scribe's pen |
| `TutorialStations.cs:127` | the Magery school | the trades yard, southeast of the training yard |
| `TutorialStations.cs:128` | Cartography | Cartography |
| `TutorialStations.cs:128` | Cartography | Cartography |
| `TutorialStations.cs:129` | Treasure maps and SOS | Treasure maps and SOS |
| `TutorialStations.cs:129` | SOS locator | SOS locator |
| `TutorialStations.cs:129` | a mapmaker's pen | a loaned mapmaker's pen |
| `TutorialStations.cs:129` | the Mapmaker | the trades yard, southeast of the training yard |
| `TutorialStations.cs:132` | Animals | Animals |
| `TutorialStations.cs:132` | Animal Taming | Animal Taming |
| `TutorialStations.cs:132` | Animal Lore | Animal Lore |
| `TutorialStations.cs:132` | Veterinary | Veterinary |
| `TutorialStations.cs:132` | Herding | Herding |
| `TutorialStations.cs:133` | Pet scaling | Pet scaling |
| `TutorialStations.cs:133` | Follow mode | Follow mode |
| `TutorialStations.cs:133` | a shepherd's crook | a loaned shepherd's crook |
| `TutorialStations.cs:133` | the tutorial farm pen | the farm's animal pen, through the gate |
| `TutorialStations.cs:136` | The bard's trial | Music and bard skills |
| `TutorialStations.cs:136` | Musicianship | Musicianship |
| `TutorialStations.cs:136` | Peacemaking | Peacemaking |
| `TutorialStations.cs:136` | Provocation | Provocation |
| `TutorialStations.cs:136` | Discordance | Discordance |
| `TutorialStations.cs:137` | a lute | a loaned lute |
| `TutorialStations.cs:137` | the Bardic Guild | the trades yard, southeast of the training yard |
| `TutorialStations.cs:140` | The thief's trial | Thieving and stealth |
| `TutorialStations.cs:141` | Hiding | Hiding |
| `TutorialStations.cs:141` | Stealth | Stealth |
| `TutorialStations.cs:141` | Detecting Hidden | Detecting Hidden |
| `TutorialStations.cs:141` | Lockpicking | Lockpicking |
| `TutorialStations.cs:141` | Remove Trap | Remove Trap |
| `TutorialStations.cs:141` | Snooping | Snooping |
| `TutorialStations.cs:141` | Stealing | Stealing |
| `TutorialStations.cs:141` | Poisoning | Poisoning |
| `TutorialStations.cs:141` | Tracking | Tracking |
| `TutorialStations.cs:141` | Begging | Begging |
| `TutorialStations.cs:142` | Forensic Evaluation | Forensic Evaluation |
| `TutorialStations.cs:142` | Hidden characters | Hidden characters |
| `TutorialStations.cs:142` | lockpicks | loaned lockpicks |
| `TutorialStations.cs:142` | the Bountiful Harvest Inn, back room | the trades yard, southeast of the training yard |
| `TutorialStations.cs:145` | Houses | Houses |
| `TutorialStations.cs:146` | Transparent houses | Transparent houses |
| `TutorialStations.cs:146` | Circle of transparency | Circle of transparency |
| `TutorialStations.cs:146` | a model house | the farmhouse porch, then the bank |
| `TutorialStations.cs:147` | Runes, gates and boats | Runes, gates and boats |
| `TutorialStations.cs:148` | World Map | World Map |
| `TutorialStations.cs:148` | a recall rune | a loaned blank recall rune |
| `TutorialStations.cs:148` | the moongate | the farm gate, then the New Haven plaza |
| `TutorialStations.cs:149` | Karma, fame, flagging and guards | Name colors, reputation, and guards |
| `TutorialStations.cs:150` | the town guard post | the training yard, Sera the healer, then the plaza |
| `TutorialStations.cs:151` | Levels, loops, loot boxes, achievements, ring slots | Rewards and extra jewelry slots |
| `TutorialStations.cs:152` | Skill progress bar | Skill progress bar |
| `TutorialStations.cs:152` | Autoloot | Autoloot |
| `TutorialStations.cs:152` | Scavenger | Scavenger |
| `TutorialStations.cs:152` | Nearby loot | Nearby loot |
| `TutorialStations.cs:152` | Vendors: advanced shop, trade, auto buy and sell | Vendors: advanced shop, trade, auto buy and sell |
| `TutorialStations.cs:153` | Legion scripting (advanced) | Legion scripting (advanced) |
| `TutorialStations.cs:153` | Script library browser (advanced) | Script library browser (advanced) |
| `TutorialStations.cs:153` | the League field office | Elara Voss's house, the bank, then Rook |

## Wing headings rendered from enum names

| File:line | Current text | Proposed text |
|---|---|---|
| `TutorialStations.cs:22` | Combat | Combat |
| `TutorialStations.cs:23` | Magic | Magic |
| `TutorialStations.cs:24` | Gathering | Gathering |
| `TutorialStations.cs:25` | Crafting | Crafting |
| `TutorialStations.cs:26` | Animals | Animals |
| `TutorialStations.cs:27` | Bard | Bard |
| `TutorialStations.cs:29` | Housing | Housing |
| `TutorialStations.cs:30` | Travel | Travel |
| `TutorialStations.cs:31` | Reputation | Reputation |

## Notes for the applying Claude

These are copy proposals for our tutorial, with no behavior changes requested. Keep station keys, skill enum identifiers, pet-line keys, command names, and the required chat phrase unchanged. The pet-line values at ClusterFTutorial.cs:241 are displayed with initial capitals by TutorialGumps.cs:385; they are not proposals to rename internal pet lines.

Keep `tutorial loaner: ` and `tutorial prop: ` exactly, including the trailing space. TutorialWingTrials.cs:135 uses them to remove abandoned lesson supplies and props; TutorialTradeTrials.cs:478 also uses the prop prefix when naming objects. Keep the progress prefix `Done: ` because TutorialWingTrials.cs:634 uses it to choose the completed-step color. The `Hint and arrow`, `Next lesson / graduate`, `Graduate`, `Choose`, `Ready`, and `Resurrect` labels stay consistent with their proposed instructions.

Localized-message rows identify the tutorial call site and message ID. Their proposals are for tutorial-specific wording if applied later, not global replacements in the shared client localization files. The fallback page's lists keep the recognizable TazUO option names; those lists do not prove that the active trial teaches or opens every named feature.

## Source findings behind the proposals

These are defects in our tutorial wording, recorded here for the writing pass. No implementation was changed.

- Loop resets and cap increases are described as working in the current copy. ClusterFLoops.cs:40 has an empty reset hook, while ClusterFLoops.cs:59 only calls that hook before recording the loop; the vision itself does not reset the character. The proposals call the reset a preview and describe graduation's actual island access instead.
- The Farmhand claims to give the Bond Trial. TutorialFarm.cs:192 handles the pet, pests, bandages, and completion dialogue; Mobiles/Evo/EvoPet.cs:50 identifies the Bond Trial as an unbuilt staff-set flag. The proposed completion line gives the useful vet direction without sending a player to request an unavailable trial.
- Pet descriptions name forms beyond current progression gates. Mobiles/Evo/EvoPetData.cs:95 defines the dog stages, :110 the cat, :119 the fox, and :138 the bird. The final stages have loop and Bond Trial requirements, and some intermediate artwork is pending. NextEnabled at :49 skips art-pending stages; EvoPet.cs:294 applies progression gates, so the fox can reach its bake kitsune stage after graduation and enough XP. The proposed descriptions keep attainable growth clear without promising the final forms immediately.
- TutorialWingTrials.cs:79 places Heartwood in Ilshenar. Pinned ModernUO's Distribution/Data/regions.json:34 and :1205 put its regions in Felucca and Trammel. Pinned Projects/UOContent/Engines/ML Quests/Definitions/Spellweaving.cs:91 defines Patience and its follow-on quest chain; the proposal names that starting quest and drops the incorrect facet.
- TutorialStations.cs contains old location placeholders. TutorialCorePlacement.cs:33 selects the real main-lesson destinations, TutorialWingTrials.cs:49 selects the training yard, and TutorialTradeTrials.cs:79 and :241 supply the trades, animal, and tour destinations. The fallback-location proposals follow those handlers instead of sending players to unused schools or shops.
- Action wording was checked against the completion paths, not just lesson titles: TutorialTrialProgress.cs:20 for the main lessons, TutorialWingTrials.cs:523 for bandaging and combat/spell evidence, TutorialTradeTrials.cs:530 for products and tour stops, and TutorialFarm.cs:301 for a bandage that actually restores health. Pet commands are present in pinned Projects/UOContent/Mobiles/AI/BaseAI/OnSpeech.cs:157 and :193. Wren's hat and pitchfork are constructed in TutorialFarm.cs:554; the rat, tiles, token, and gate descriptions follow their item/body IDs and hues in TutorialCorePlacement.cs.

## Review and verification

The inventory has 606 table entries; the complete file list and per-file entry counts are above. Repeated literals are separate entries, while assembled lines use templates so the applying agent can preserve substitutions. All proposed text is plain ASCII and contains no em dashes. Prose proposals use no more than two sentences; the pet-death line and graduation-box suffix also remain two sentences when combined.

Reviewed every non-comment string-bearing source line for omissions, including arrays, item names, arrow labels, conditional pages, and localized-message calls. Remaining exclusions are identifiers, staff-only commands and seed reports, formatting, and the invisible farm spawner's administrative name (pinned Engines/Spawners/BaseSpawner.cs:686 sets Visible to false). TutorialFarmLayout.cs has layout data, TutorialTrialProgress.cs has action identifiers, and TutorialStyle.cs has HTML/color formatting; none supplies additional readable text.

No code was changed and no new tests or gates were added. Lane tests are none for this notes-only task, so no build or gameplay test was run. Shell commands ran in Windows PowerShell 5.1. The required tools/progress.py --dry-run completed with exit 0; its generated progress.json side effect was restored to its original bytes, leaving only this note as a deliverable.

Unverified: the proposed copy has not been applied or viewed in a client, so text wrapping, exact client-localized English, and current client key bindings remain unverified. No shard was started and no connection to Haven was made.

P588 DONE
