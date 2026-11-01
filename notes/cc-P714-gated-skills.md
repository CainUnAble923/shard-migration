# cc-P714: the Chivalry and Necromancy initiation gates, their two quests, and the shorter start

## In plain words

- **Chivalry and Necromancy now each start with a teacher's quest on the test shard.** Until a character finishes the quest, the game refuses that school's spells and the skill cannot rise, whatever books or scrolls the character carries. The refusal names the teacher:
  - Sister Aveline at Fort Whitestone teaches Chivalry ("A Place on the Watch");
  - Oren Pike at the Dhampire Ruins teaches Necromancy ("Names for the Last Door").
  - Each quest gives the school's book and a few supplies, once. The skill starts at zero.
- **New characters on the test shard start from four packages or a shorter custom list.** The packages are Fighter, Archer (Thrower for gargoyles), Mage and Maker. Paladin, Necromancer, Samurai and Ninja are no longer starting choices.
  - The game's own character screen still lists those four old choices (and has no Archer) until the player package ships its own profession list. Picking one of them disconnects with "Character creation blocked." No character slot is used.
- **In the tutorial, the Chivalry and Necromancy lessons show the school and send you to its teacher.** The casting lesson opens after you learn the school. Skipping or graduating gives neither school.
- **For you:**
  1. On the test shard, run `[Initiation place` as an admin to put the teachers, the patrol, the courtyard ankh and the Dhampire graves in the world.
  2. Queue the client follow-up below, so the character screen matches.
  3. Before this goes live, check that the live world has no playing characters whose Chivalry or Necromancy should be kept: the gates are off there until then.

## What was built

The design is P709's (`notes\cc-P709-gated-skills-and-start-choices.md`), with Chase's answers of 2026-10-27. The code is in the code copy's `server/` folder.

### 1. The gate (`customizations/ClusterFSchoolGate.cs`)

- **General by design.**
  - A school is a row in `ClusterFSchoolGate.Schools`: its id, skill, teacher, place and quest. The permission is a per-character flag in a new save file (`SchoolGateStore`, "SchoolGates").
  - A quest opens a school by calling `Grant`.
  - Adding Bushido or Ninjitsu later means a new row and a quest, with no new plumbing.
- **Who is gated:** only player characters below staff, only Chivalry and Necromancy, and only while the gate is in force.
- **The switch:**
  - In force by default on the test shard only (`TestCenter.Enabled`).
  - `clusterf.schoolGates.enabled` = `on` or `off` in the config overrides that; `[SchoolGate on|off|auto` sets it in game. The switch is saved.
  - Off, every check passes and character creation is stock.
- **Enforcement points:**

| Route | How it is held |
|---|---|
| Casting from a book, scroll, hotkey or macro | `server/patches/Spell-school-gate.patch`: one more `else if` in pinned `Spell.Cast`, beside the feature-flag spell block, before mana, reagents or a skill check. Every cast route goes through `Cast()`. The refusal names the teacher, at most every 5 s per school. |
| Skill gain | The four skill-check handlers `ClusterFSkillGain` already wraps return false for the school before any roll (no new patch). |
| NPC teaching, Scrolls of Transcendence, soulstones | The cap policy (`ClusterFSkillCaps.Apply`: login, world load, the command) now ends with `ApplyCaps`, which holds each unearned school's cap at the character's own base. Pinned's teaching (`BaseCreature.CheckTeachSkills`), transcendence and soulstone code all stop at the cap. A base above zero is never taken away. |
| Power scrolls | `server/patches/PowerScroll-school-gate.patch`: `PowerScroll.CanUse` refuses before the scroll is used. Otherwise its cap raise would last until the next login. |
| Tutorial loans | The two school lessons no longer lend anything before initiation (part 5). |

- **Granting:**
  - It changes no skill.
  - It re-applies the cap policy, so the school gets the shard's normal cap.
  - It is logged ("School gate: X may now learn Chivalry (initiation quest)").
- **The permission lasts:** death, restarts, resets, karma and guilds don't touch it. A deleted character's rows are dropped at the next save.
- **Staff tools:**
  - `[SchoolGate status|grant <school>|revoke <school>` targets one player; grants are logged as staff test grants.
  - Positive skill is never treated as an implicit permission.

### 2 and 3. The quests (`customizations/ClusterFInitiation.cs`)

- **Where:**
  - Both places are Zigholtul's, on his SoS map: Fort Whitestone at 890,1055 and the Dhampire Ruins at 1469,2515.
  - Every spot was checked standable, under open sky, and joined on foot to its way in (`notes\cc-P714-tools\sites.py`, `spots.json`, `sites.txt`):
    - Fort Whitestone's spots from the Yew Forest Guardpost (74,162 tiles reached);
    - Dhampire's from the Shrine of Spirituality (59,513 tiles).
  - Renders: `notes\cc-P714-tools\renders\`.
- **A Place on the Watch** (Chivalry, tuned for about 20-40):
  1. Sister Aveline Hart (893,1036,32, in the fort's courtyard) hands over three relief bundles and replaces any that are lost.
  2. Hendric Ash, the watch quartermaster (888,1038,32), names the scouts and the patrol.
  3. Sergeant Tobin (889,1078,11, on the road south of the fort) takes the bundles. Three road scavengers rise on the road and must be driven off.
  4. Aveline explains tithing.
  5. The player tithes 100 gold at the courtyard ankh (an AnkhWest placed at 890,1034). The balance must rise by 100 after this step began; an old balance is not proof.
     - The Codex P709 fix: a balance too full to take 100 more (the tithing gump's cap is 100,000) offers "Give 100 gold to the relief fund" instead.
  6. Confirm, or "Not yet". The permission is saved, then a Book of Chivalry (stock, all ten abilities) is delivered once. The player's own tithe stays as their 100 points.
- **Names for the Last Door** (Necromancy, about 25-45):
  1. Oren Pike (1458,2512,15, at the ruins) lends a copy of the burial register.
  2. Three disturbed graves (1455,2500; 1486,2499; 1484,2527) each raise a grave robber the first time. Once the robber is beaten, the grave gives up its nameplate.
  3. Oren takes the three plates and points to the collector's skull candle east of the ruins (1492,2521). Snuffing it raises the collector's guardian; beating it lays the shade to rest.
  4. Oren reads Warden Morrow's terms, with the karma warning (Chivalry's effects weaken with lower karma; learning changes no karma now). Confirm, or "Not yet".
     - The permission is saved, then a Necromancer spellbook (Curse Weapon and Evil Omen) and ten each of pig iron, bat wing, grave dust, daemon blood and nox crystal are delivered once.
- **Rules in the code:**
  - No step needs a gated spell, and friends may fight alongside.
  - A field foe counts only for the player it was raised for, and only if that player damaged it or killed it. One killed by a helper alone says so, and the patrol raises a replacement.
  - Foes drop no loot or gold and expire after 10 minutes or when their player leaves. Any left by a restart are deleted at world load.
  - Quest items are blessed and owned, can't be dropped, and are replaced if lost.
  - The supplies go into the pack in one bag. A full pack leaves them with the teacher ("make room, then speak to me again"). The once-flag is set only after the bag is in the pack, so a repeat talk or a second "learn" gives nothing.
- **Placement:**
  - `[Initiation place` places the four NPCs, the ankh, the skull candle and the three graves (9 pieces). It is idempotent: a second run places 0. It runs on the test shard only.
  - `[Initiation dry|status|clear|reset <school>` are the other forms.
- **NPC art:** existing bodies and clothes; a dirt patch (0x0913) for the graves; a skull with candle (0x1853) for the binding; a bag, a book and a rune-sized plate for the quest items. No new art.

### 4. Creation (`customizations/ClusterFStartChoices.cs`, `CharacterCreation.cs`)

- **Templates:** while the gate is in force, a player start resolves before any character is made.
  - Four templates of four skills at 30 (120 points), with stats totalling 90:
    - Fighter (profession 1, the client's Warrior) and Archer (profession 8, a new client entry): 45/35/10;
    - Mage (2): 25/20/45;
    - Maker (3, the client's Blacksmith): 60/15/15.
  - A gargoyle asking for Archer gets Thrower: Throwing for Archery, same budget.
  - The kits are the existing race-aware ones: the warrior armour for Fighter, and the per-skill items for the rest (bow, arrows, boomerang, bandages, tools).
- **Custom (profession 0):**
  - The whitelist is P709's: six weapon skills subject to race, Tactics, Anatomy, Parrying, Healing, Magery, Evaluating Intelligence, Meditation, Mining, Lumberjacking, Fishing, Blacksmithy, Tailoring, Tinkering, Carpentry, Hiding and Tracking.
  - At most 50 in one skill, no repeats.
  - 120 points and 90 stats on a four-slot client; 100 and 80 on a legacy three-slot client. No extra 20 is added.
  - Archery is never a gargoyle's, and Throwing only a gargoyle's.
- **Refusals:**
  - Professions 4-7 (Necromancer, Paladin, Samurai, Ninja), a skill off the list, a wrong total, a repeat, a race's wrong weapon and bad stats are all refused.
  - The old code silently turned some of these into Alchemy at 0, or a skill-less character.
  - A refused request makes no character, so no slot is used and nothing is half made. Pinned's handler disconnects with "Character creation blocked.", and the server log says why.
- **Not changed:** with the gate off, creation is exactly as before. Staff creation is untouched. No free respec after a gate, and no grandfathering: nothing reads old skills as a permission.

### 5. The tutorial

- `TutorialWingTrials.Start` calls the new `Preview` first.
  - Before initiation, "magic.chivalry" and "magic.necromancy" show a demonstration: a particle effect and a line describing Close Wounds or Pain Spike, tithing or reagents, karma and Spirit Speak. Then the referral.
  - There is no loan, no trial, no tithing points and no station credit. It marks the introduction as viewed (`InitiationProgress.IntroViewed`), which is not a permission.
- After initiation the lesson runs as before, under its existing loan rules.
- Graduation and a skip each add Rook's lead (P709's text, naming Oren Pike as the Keepers' local teacher) and grant nothing. Main graduation never needed either lesson.

## Tests

`server/tests/Misc/SchoolGateVerification.cs`, 12 facts:

| # | Fact |
|---|---|
| 1 | Without the permission, a Close Wounds or Curse Weapon cast is refused at `Spell.Cast` with the teacher's name; a Necromancy power scroll is refused before use; Magery is untouched; after a grant the cast passes the gate (it then stops at the mana check); staff, a lich and the switch off are never refused. |
| 2 | Five Necromancy checks gain nothing before the grant; after it they gain (pinned's handlers wrapped by ours, rolls held at 0). |
| 3 | The cap policy holds Chivalry at 0 and Necromancy at a pre-gate base of 12.3 (kept, not cut), Magery at the normal cap. A Mage vendor's Chivalry lesson fails before the grant and succeeds after it. Grant puts the normal cap back, changes no base, and is once. |
| 4 | Permission per character, kept through death and resurrection and a save round trip of the store; both schools on one character; the other character has neither. |
| 5 | A Place on the Watch played through: a lost bundle replaced; a helper's lone kill gives no credit and a replacement rises; an old tithing balance is not proof, +100 after the step is; "Not yet" keeps the work; a full pack keeps the permission but holds the book; the book arrives once; the skill stays 0 and the cap is normal. |
| 5b | A full tithing balance gives 100 gold to the relief fund instead (refused with no gold). |
| 6 | Names for the Last Door played through: a guarded grave gives no plate and no second robber; each plate once; Oren takes the plates; the binding raises the guardian; the karma warning is said; "Not yet" keeps the work; karma unchanged; the book holds exactly Curse Weapon and Evil Omen; 10 of each reagent; nothing more on a second talk or "learn". |
| 6b | `[Initiation place` places 9 pieces, and a second place places 0. |
| 7 | Creation: professions 4-7 refused; the five templates (Thrower for a gargoyle) at 30 each with no gated skill; custom rules: off-list (Necromancy, Chivalry, Bushido, Ninjitsu, Mysticism, Imbuing, Spirit Speak, Alchemy), over 50, a repeat, totals 120/100, race weapons, stats. |
| 7b | Through the real creation event: a Paladin request and a custom Necromancy request make no character (no new mobile, slot 0 empty); a Fighter start gets its skills and 45/35/10 and no permission. |
| 8 | Before initiation the Chivalry lesson leaves no trial, no tithing points, no book and no skill loan, marks the introduction viewed, and gives no station credit; the same for Necromancy. After the grant the lesson arms and lends its 100 tithing points. |
| 8b | A skip grants neither school. |

- **Green:** 12 of 12 on `sl-uo-builder:cc-P753` with this branch's files (`notes\cc-P714-tools\probe714.sh`, `green\probe-2.txt`), then 36 of 36 with the related suites (`green\probe-3.txt`).
- **Red:** one mutant run (`red\red-mutants-ABCDEF.txt`) with:
  - A: both patches off;
  - B: the gain guard off;
  - C: the cap hook off;
  - D: `CharacterCreation.cs` from before this task;
  - E: the tutorial preview off;
  - F: the personal-credit check off.
  
  Exactly the six facts aimed at them failed (1, 2, 3, 5, 7b and 8); the other six passed.
- **Gated build** (`notes\cc-P714-tools\gated-build.ps1`, `docker/uo/build.sh -t sl-modernuo:cc-P714`, under the `docker-build` lock, released after):
  - Runs 1 and 2 stopped at `apply-patches.sh`'s known flake: "never applied" for a patch whose "Applied:" line is in the log (`gated-build-1-flake.log`, `gated-build-2-flake.log`).
    - The cause is a pipe: `printf ... | grep -Fxq` under `pipefail`. `grep -q` leaves at its first match, and `printf` can then die of SIGPIPE.
    - My two new patches lengthened the list, and it failed twice in a row, so I fixed it: the check now reads a here-string, with no pipe. Two other `| grep -q` pipes in the script check short code strings, where a miss would be a quiet pass, not a false failure; left alone.
  - Run 3 compiled and ran: 1 failed, `TestCenterVerification` (`gated-build-3-testcenter.log`).
    - That test turns the test center on, which puts the gate in force. Its helper then created a character with no skills and no profession, which the shorter creation refuses by design.
    - The helper now asks for the Fighter template. The test checks the bank and the kit, not the skills.
  - Run 4: **EXIT=0, 2,866 tests: 2,860 passed, 6 skipped, 0 failed** (`green\gated-build-summary.txt`; the 12 new facts are listed in `green\gated-build-schoolgate-facts.txt`).
- **Not run:** a live play-through on a private shard (both quests, both creation routes, two players helping each other), which P709's build acceptance asks for. The facts drive the real NPC, site, foe, death, gump-button and creation-event code, but not a client.
- **CHANGELOG** `2026.10.31.8` (three test-shard lines and a Staff line); VERSION 2026.10.31.8.

## Deviations and decisions for Chase

- **Oren closes the Necromancy lesson on Warden Morrow's behalf.** P709 has Morrow refer and close it. But Morrow stands in Umbra on Malas, and P709 also says no trip to Malas. So Oren reads "Warden Morrow's terms" at the ruins, and Morrow's own NPC is unchanged.
  - Rook's lead names Oren for the same reason.
  - If you want the close at Morrow, it is one branch in `OrenTalk` plus the existing Keepers guildmaster.
- **The client follow-up (not done here, as the prompt says).** A client-package prompt should ship a profession file (TazUO reads `Prof.txt`) through the package's `uo-overrides`, listing:
  - Fighter (1), Mage (2) and Maker (3) with P709's descriptions and the creation text in `ClusterFStartChoices.CreationText`;
  - a new Archer entry (8);
  - and dropping Necromancer (4), Paladin (5), Samurai (6) and Ninja (7).
  
  It would also limit the custom picker to the whitelist if TazUO allows that. Until then, the stock screen offers four choices the test shard refuses, and has no Archer.
- **The gates are on by default only on the test shard.** "Auto" follows `TestCenter.Enabled`.
  - The live shard keeps today's creation and schools until someone sets `clusterf.schoolGates.enabled` to `on` (or runs `[SchoolGate on`).
  - Teachers must also be placed there: `[Initiation place` is test-shard only today, and its spots are on the SoS land.
- **Fresh launch:** I could not check the live world for playing characters with Chivalry or Necromancy. The world on Haven is not reachable from here.
  - Nothing is migrated or grandfathered, and nothing erases a skill: a character with a base above zero keeps it, but can't cast or raise it until initiated.
  - Staff can grant a logged permission with `[SchoolGate grant`.
- **Beginner routes:**
  - Both sites are reachable on foot from their way in.
  - Fort Whitestone's courtyard has an OrderGuard spawner at 892,1035, beside Aveline.
  - The Dhampire area sits inside a stock outdoors spawner (`Spawns/shared/trammel/Outdoors.json`, 1427,2525, range 150: orcs, ettins, ratmen, giant spiders, reapers), so a 25-45 character may meet more than the quest's own foes.
  - No harder P672 encounter exists there yet to keep apart from.
  - Foe numbers (50-95 hits, 4-10 damage) were not tuned in play.
- **What I did not cover:**
  - **Stock books:** `[add`-style staff creation and stock "set skill" test-center speech can still raise a base directly. These are staff and test tools; casting stays refused.
  - **Guild starter kits:** the guild kits that hand out a Necromancy book still do. A book grants nothing, and joining the Keepers stays separate from the permission.
  - **A Training Ward:** not part of this; the skill rises by ordinary practice and trainers after initiation.
- **Not verified:** the shop sources for a replacement Book of Chivalry or Necromancy scrolls on the new map. The teachers point to "mages and provisioners" and "reagent sellers and mages" in general terms.

## Files

- **Code copy:**
  - new: `server/customizations/ClusterFSchoolGate.cs`, `ClusterFInitiation.cs`, `ClusterFStartChoices.cs`, `server/patches/Spell-school-gate.patch`, `PowerScroll-school-gate.patch`, `server/tests/Misc/SchoolGateVerification.cs`;
  - changed: `CharacterCreation.cs`, `ClusterFSkillCaps.cs`, `ClusterFSkillGain.cs`, `Tutorial/ClusterFTutorial.cs`, `Tutorial/TutorialWingTrials.cs`, `docker/uo/apply-patches.sh` (the two patches and the here-string fix), `server/tests/Misc/TestCenterVerification.cs`, CHANGELOG.md, VERSION.
- **Docs copy:**
  - `notes/cc-P714-tools/`: `sites.py`, `spots.json`, `sites.txt`, `renders/`, `mkpatch.py` (a patch from one replacement, checked at fuzz 0), `probe714.sh`, `gated-build.ps1` (logs git-ignored), `red/`, `green/`;
  - this file.

P714 DONE
