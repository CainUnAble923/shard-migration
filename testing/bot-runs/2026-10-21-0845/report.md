# Overnight play tests, 2026-10-21-0845

**19 pass, 6 fail, 0 flaky, 1 could not run** (26 checks, each run 1 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: commit 62c675d (-Commit, a worktree in D:\UO\bot-shard\src)
- World: a copy of the test world's automatic backup 2026-10-21-13-45-00, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| T-001 | PASS | 1/1 | TinkerTools: item page of 'jointing plane' has MAKE X: True; SmithHammer: item page of 'ringmail gloves' has MAKE X: True | [1](transcripts/T-001-run1.txt) | T-001: the MAKE X label draws in the client (the original bug was a drawing one) |
| T-004 | FAIL | 0/1 | 42 of our entries read on 678 listed items across 4 systems; Tailoring: 'leather talons' not listed; Tinkering: 'gargish butcher knife' not listed | [1](transcripts/T-004-run1.txt) |  |
| T-005 | PASS | 1/1 | 678 items and their materials scanned across 4 systems; none | [1](transcripts/T-005-run1.txt) |  |
| T-013 | PASS | 1/1 | graphic 0xE3C; locked to the player: True; opened after unlock: True; trap bit: hits 55 -> 49, messages ['You set off a trap!']; contents 4 (gold True, bolts True) | [1](transcripts/T-013-run1.txt) | T-013: each of its three crate graphics draws as a proper crate or chest |
| T-027 | PASS | 1/1 | chests: 106 items, 0 masks; 106 items, 2 masks; 106 items, 1 masks; 106 items, 0 masks; 106 items, 1 masks; masks 4, with properties beyond the name 4; e.g. [('0x141b', 10, ['orc mask', 'Weight: 4 stones', 'lower reagent cost 4%']), ('0x154b', 10, ['tribal mask', 'Weight: 2 stones', 'reflect phys... | [1](transcripts/T-027-run1.txt) |  |
| T-048 | PASS | 1/1 | status: ['(seeded and moved first)', 'MinersCompactTentAddon: already on the world at (3494, 2744, 5) (Trammel); nothing placed.']; Liaison ("Garrett Ashveil the Miners' Compact Liaison", 3498, 2744); Archivist ('Velara Thorne the Survey Archivist', 3496, 2754); tent wall pieces in the camp box: ... | [1](transcripts/T-048-run1.txt) | T-048: the two tents look right on the ground |
| P56-7 | PASS | 1/1 | trash bag: entry True, opens True; pet mimic: entry True, opens True; pack mule: entry True, opens True | [1](transcripts/P56-7-run1.txt) | P56-7: the entries read as words in the client (ours are custom clilocs the package adds) |
| P57-5 | PASS | 1/1 | mule menu has 1900000: True; satchel has 1900001: True; hammer has 1900002: True; panel opened: True | [1](transcripts/P57-5-run1.txt) | P57-5: the words draw in our client, and a client started without the launcher shows a blank row |
| P61-4 | PASS | 1/1 | Platinum: tooltip #1900003, gump shows it True; Frost: tooltip #1900006, gump shows it True; Celestial: tooltip #1900010, gump shows it True (our clilocs read as #19000xx here: the bot has EA's cliloc table, the package adds the words) | [1](transcripts/P61-4-run1.txt) | P61-4: the line is blank in a client started without the launcher |
| P67-3 | PASS | 1/1 | materials ['Iron (0)', 'Toxic (0)', 'Dull Copper (0)', 'Blaze (0)', 'Shadow Iron (0)', 'Frost (200)', 'Copper (0)', 'Obsidian (0)', 'Bronze (0)', 'Mythril (0)', 'Gold (0)', 'Adamantium (0)', 'Agapite (0)', 'Celestial (0)', 'Verite (0)', 'Dawnstone (0)', 'Valorite (0)', 'Platinum (0)'] (post-Valor... | [1](transcripts/P67-3-run1.txt) |  |
| T-044 | FAIL | 0/1 | as a plain gargoyle: {'gargish cloth arms': 0, 'gargish cloth chest': 0, 'gargish cloth kilt': 0, 'gargish cloth leggings': 0} (gate lines []); after [Recipes learnall: {'gargish cloth arms': 2, 'gargish cloth chest': 2, 'gargish cloth kilt': 2, 'gargish cloth leggings': 2}; garments listed none;... | [1](transcripts/T-044-run1.txt) |  |
| T-003 | PASS | 1/1 | gargish platemail arms: made, worn on layer 19; gargish cloth arms: made, worn on layer 19; the patterns were granted with [Recipes learnall first (the recipe gate hides them from a plain gargoyle) | [1](transcripts/T-003-run1.txt) |  |
| T-041 | PASS | 1/1 | guildmaster 'Ginton the blacksmith guildmaster'; tools line: 'The Society of Smiths hands you the tools of its trade: 6 items.'; new items in pack 7 ['0xfbb', '0xe86', '0xe86', '0x1bf2', '0x13b4', '0x2259']; ingots 374 -> 424 | [1](transcripts/T-041-run1.txt) |  |
| T-042 | PASS | 1/1 | first ask: 1 item(s) ['0x13cc']; page after: ['Lost one? A replacement costs 10 guild scrip.', 'Taken. The matching training quest now counts as done.', 'Taken']; second ask: 0 item(s), said [] | [1](transcripts/T-042-run1.txt) |  |
| T-045 | PASS | 1/1 | second character offered Join: True (gump: ['Joining is free. After you join, the Apprentice task:', 'Anyone may join. You start as an Initiate.', 'Join the Society of Smiths']); tools line 'The Society of Smiths hands you the tools of its trade: 6 items.'; 7 new item(s) | [1](transcripts/T-045-run1.txt) |  |
| P66-1 | PASS | 1/1 | at 5 tiles: "You can't seem to hide right now."; at 10 tiles: 'You have hidden yourself well.'; base 99.5 -> 100.5 over 2 hides | [1](transcripts/P66-1-run1.txt) |  |
| P66-2 | PASS | 1/1 | empty spot x5: ['You can see nothing hidden there.'], base 150.0 -> 150.0; hider vanished True, found again True (hider told True); chest: '[trapped]'; 15 tiles: revealed False | [1](transcripts/P66-2-run1.txt) |  |
| P66-4 | PASS | 1/1 | base 119.9 -> 120.9 after 5 plays (Peacemaking 200 vs 120 success rates: not measured by this check) | [1](transcripts/P66-4-run1.txt) |  |
| P71-4 | PASS | 1/1 | quiet steps per batch at 200: [35, 35] (mean 35.0, 34 expected); at 120: [25, 25] (mean 25.0, 24 expected); -1 = stealth never started (a batch ends at the next 'You begin to move quietly' or at 'You have been revealed!') | [1](transcripts/P71-4-run1.txt) |  |
| P71-5 | PASS | 1/1 | heals: [('You finish applying the bandages.', 68), ('You finish applying the bandages.', 67), ('You finish applying the bandages.', 67), ('You finish applying the bandages.', 80), ('You finish applying the bandages.', 76)], mean 71.6 (54 to 90 expected; the old band was 69 to 117); hits max 175 | [1](transcripts/P71-5-run1.txt) |  |
| P61-1 | FAIL | 0/1 | 150.0 in Frost: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)'; 162.5 in Frost: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)'; 162.5 in Obsidian: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)'; 140.0 in Valorite: None -> None (0 m... | [1](transcripts/P61-1-run1.txt) |  |
| P67-4 | FAIL | 0/1 | hammer worn True; base None -> None over 0 made / 0 failed / 0 other no item 'platemail (tunic)' | [1](transcripts/P67-4-run1.txt) |  |
| P67-1 | ERROR | 0/1 | AssertionError: double-clicking the tool opened no craft gump (0 gumps since: []) | [1](transcripts/P67-1-run1.txt) |  |
| P67-2 | PASS | 1/1 | 150.0 in Frostbark bows: 150.0 -> 155.0 (0 made, 0 failed, 16 other); 150.0 in Frostbark kindling: 150.0 -> 150.0 (0 made, 0 failed, 15 other) | [1](transcripts/P67-2-run1.txt) |  |
| T-024 | FAIL | 0/1 | spawner lists ['Miasma']; Miasma fighter died (by the player); corpse False | [1](transcripts/T-024-run1.txt) |  |
| T-025 | FAIL | 0/1 | spawner lists ['LadyLissith']; LadyLissith fighter died (by the player); corpse False | [1](transcripts/T-025-run1.txt) |  |

## Fail, Flaky and could-not-run, every run

- **T-004 FAIL** (Our smith, tailor, tinker and carpentry entries show at their registered skill, not 0 or 120)
  - run 1 FAIL: 42 of our entries read on 678 listed items across 4 systems; Tailoring: 'leather talons' not listed; Tinkering: 'gargish butcher knife' not listed ([transcript](transcripts/T-004-run1.txt))
- **T-044 FAIL** (A gargoyle's Tailoring lists the gargish cloth armor (two of each of four pieces) once the patterns are known, one crafts; robe, sash and half apron are absent)
  - run 1 FAIL: as a plain gargoyle: {'gargish cloth arms': 0, 'gargish cloth chest': 0, 'gargish cloth kilt': 0, 'gargish cloth leggings': 0} (gate lines []); after [Recipes learnall: {'gargish cloth arms': 2, 'gargish cloth chest': 2, 'gargish cloth kilt': 2, 'gargish cloth leggings': 2}; garments listed none; crafted arms: (False, [], []) ([transcript](transcripts/T-044-run1.txt))
- **P61-1 FAIL** (Blacksmithy: Frost plate gains at 150, none at 162.5, Obsidian gains again; Valorite at 140 gains nothing)
  - run 1 FAIL: 150.0 in Frost: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)'; 162.5 in Frost: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)'; 162.5 in Obsidian: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)'; 140.0 in Valorite: None -> None (0 made, 0 failed, 0 other) no item 'platemail (tunic)' ([transcript](transcripts/P61-1-run1.txt))
- **P67-4 FAIL** (Blacksmithy 187 with a +10 hammer: the base rises and stops at 187.5)
  - run 1 FAIL: hammer worn True; base None -> None over 0 made / 0 failed / 0 other no item 'platemail (tunic)' ([transcript](transcripts/P67-4-run1.txt))
- **P67-1 ERROR** (Carpentry: Frostbark stools gain at 150, none at 155, Shadowbark gains; Ironwood at 99.9 says 'You cannot work this strange and unusual wood.')
  - run 1 ERROR: AssertionError: double-clicking the tool opened no craft gump (0 gumps since: []) ([transcript](transcripts/P67-1-run1.txt))
- **T-024 FAIL** (Labyrinth: a spawner holds Miasma, it spawns and is killable)
  - run 1 FAIL: spawner lists ['Miasma']; Miasma fighter died (by the player); corpse False ([transcript](transcripts/T-024-run1.txt))
- **T-025 FAIL** (Twisted Weald: a spawner holds Lady Lissith, she spawns and is killable)
  - run 1 FAIL: spawner lists ['LadyLissith']; LadyLissith fighter died (by the player); corpse False ([transcript](transcripts/T-025-run1.txt))

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-21T13:44:00.080547593Z sha256:c6733afcdd530fbe083b181700b0ba3e1ad79d7670573ae1d7633384e9c41605"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-21T13:44:00.080547593Z sha256:c6733afcdd530fbe083b181700b0ba3e1ad79d7670573ae1d7633384e9c41605"}`
