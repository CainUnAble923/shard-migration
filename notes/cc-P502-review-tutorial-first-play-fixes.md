# P502: review of the tutorial first-play fixes

Reviewed October 23, 2026. P480 code commit `381082f879eb753e31c7320e2dafdb38b19609b3` is in local `main`; the reviewed work copy and local `main` both point to `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`.

Read `cc-P480-tutorial-first-play-fixes.md` and `cc-P480-tutorial-first-play-fixes-codex-review.md` first. The earlier review's findings and P480's acknowledged follow-up work are not repeated here.

## Findings

1. **bug** | `server/customizations/OutridersGuildmasterGump.cs:377`: A member can open the elixir purchase menu, leave the guildmaster, and keep buying elixirs anywhere using bank gold because each purchase opens another menu without checking distance, map, or whether the buyer is alive. Keep the guildmaster reference and require a living buyer near that NPC on the same map before charging or delivering, with a test that moves the buyer away before replying.

2. **bug** | `server/customizations/OutridersGuildmasterGump.cs:383`: A member with a full backpack and enough bank gold pays 375 gold, but the unchecked `AddToBackpack` call drops the unblessed elixir at the buyer's feet while the message says the guildmaster handed it over, leaving it available for someone else to take. Check capacity before charging and use delivery that does not drop the item on failure, refunding any charge if delivery fails; cover a full backpack funded from the bank.

3. **bug** | `server/customizations/Tutorial/ClusterFTutorial.cs:264`: If the graduate leaves the companion unchosen, another character on the same account can ask Rook for it and consume the pending claim, since the shared account record is checked without matching `CharacterSerial`, leaving the graduate without the promised pet. Apply the character check to companion reminders, menu visibility, offers, and claims, and test that a second character cannot consume the graduate's saved pending claim.

4. **risk** | `server/tests/Tutorial/TutorialFirstPlayVerification.cs:452` and `:397`: The trainer test checks only that an elixir is stocked, the guild test subtracts the production price constant itself at line 464, and the vet test exercises only a Young owner, so zero elixir prices or free vet resurrection for every owner would still pass these checks. Assert the intended 500 and 375 gold prices independently, exercise a paying non-Young owner with an exact bank debit, and cover insufficient funds and nonmember purchase rejection.

## Checks with no additional finding

- **Lesson order and saved progress:** No additional defect found. `TutorialRecord` saves string keys (`ClusterFAccountData.cs:1288`, `:1300`), and `CoreLeft` selects unfinished keys in the current order (`ClusterFTutorial.cs:117`), so completed paperdoll progress survives the backpack reorder; P480's test also round-trips that old-order example at `TutorialFirstPlayVerification.cs:205`.
- **Core lessons and lost supplies:** No additional blocker or unintended lesson skip found in the reviewed paths. Later unfinished core lessons are refused, and the new supply replacement retains the active trial when the backpack is full.
- **Farmhand repetition:** No additional spam defect found. `TutorialFarm.cs:128` checks a shared owner cooldown before speaking, so additional steps or multiple dead pets do not bypass the two-minute interval.
- **Fees and membership:** No additional free-service or nonmember discount bypass found in the current checks. The Young fee waiver, 500 gold trainer base price, and 375 gold member price match P480's recorded choices; their regression coverage is finding 4.

## Evidence and limits

Reviewed the P480 source changes and both listed test files, including the lesson hints and supplies, menus, placement, companion persistence, vet service, elixir stock patch, and guild purchase handler. Also followed the account record, pet creation, graduation box delivery, and existing core action tests.

Pinned ModernUO source confirms the delivery behavior in finding 2: `D:/UO/ModernUO-pinned/Projects/Server/Mobiles/Mobile.cs:7594` moves an item into the world when backpack placement fails. Its gump reply handler, `Projects/UOContent/Gumps/Base/GumpSystem.IncomingPackets.cs:166`, calls the response after validating the submitted controls without adding an NPC distance check, supporting finding 1.

This was a source review only. No tests, build, client session, save load, or live-world reproduction was run; runtime behavior remains unverified here. No code or existing tests were changed, and no connection to Haven was made. Progress files were not regenerated because this task requests only this review note.

P502 DONE
