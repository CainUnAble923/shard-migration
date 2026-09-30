# Feature queue

Running list of feature ideas from play testing. Kept by the overseer (Claude); agents never edit
`docs\`. Bugs and game-breaking problems do not go here: they go in `bug-list.md`.

## How this list works

1. Chase brings an idea to the overseer chat. The overseer adds it here with the next F-number,
   with feedback, suggestions and questions, and records Chase's answers.
2. Each entry says whether it is **ported** (must stay faithful to what the existing wikis describe)
   or **ours** (free to design, documented on our own wiki), and what has to be checked first.
3. When Chase calls a batch, the overseer sorts it, flags conflicts and fidelity problems, and writes
   the next cc-P prompt from it. Entries in that batch move to **Batched**, with the prompt named.
4. Chase commits with `Commit-ShardWork.ps1`.

F-numbers are their own series, separate from deviations (D-n), bugs (Dn) and questions (Q-n).
**Next free: F-11.**

The fidelity test: could a player be misled by a difference they had no way to know about?
Port a gated item when the gate is small and near; skip it when the gate is a subsystem.

## Open

### F-1: Craft X, keep going on failure (added 2026-09-29)

**Ours.** Quality of life for bulk order deeds and skill training. Nothing a player could be misled by.

What Chase wants:
- A make-X option in the craft menu that keeps crafting through failed attempts.
- **Count mode:** X finished items by default, with a toggle to count X attempts instead.
- **Exceptional only:** an option to keep going until X exceptional items are made.
- **A cap** on X: 100 in items-made mode (including exceptional only), 500 in attempts mode.
  "For now": make both one obvious constant each so they are easy to change.
- **Rejects bag** (added 2026-09-29, exceptional-only mode): non-exceptional results go to a bag
  the player picks, so they can be smelted or salvaged in one go. Only items made by this run are
  moved; nothing else in the pack is touched. Keeps the pack from hitting the weight stop.
  Chase's answer on what happens to them, by skill:
  - **Smithing: recycle on the spot.** Smithing already needs a forge in range, so smelting's
    condition is always met.
  - **Recyclable elsewhere** (e.g. tailoring cut back to cloth): recycle on the spot when the
    normal conditions are met (scissors in the pack), otherwise move to the bag.
  - **Not recyclable: into the player's Custodian trash bag** (Chase, 2026-09-29). The bag already
    exists (`server\customizations\TrashBag.cs`, part of `ClusterFCustodianSystem.cs`): the player
    dumps it for Custodian tokens. So nothing is deleted by the craft run itself; the player still
    empties the bag. Off by default, chosen per run; summary line says how many went in.
  - **Salvage bag integration is the preferred route** (Chase). Pinned has the OSI salvage bag
    (`ModernUO-pinned/Projects/UOContent/Items/Containers/SalvageBag.cs`): Salvage Ingots needs an
    anvil and forge within 2 and checks Mining; Salvage Cloth needs scissors in the pack. Rejects go
    into the player's salvage bag and are salvaged through its own code paths, not a copy of them.
    A player without a salvage bag (or trash bag) gets the plain rejects bag.

Suggested (overseer, accepted in principle):
- Normal craft delay between attempts: it saves clicks, not time.
- Stop cleanly on the first hard stop with a clear message: out of materials, tool worn out,
  backpack full or overweight, player moved or died, menu closed.
- A summary line at the end, e.g. "Made 20 (7 failed, 1 exceptional)."
- Failures and non-exceptional results use materials exactly as normal crafting does.

Check first:
1. Does pinned ModernUO's craft gump already have a make-X or make-last option, and what does it
   do on failure? Build on it rather than beside it. Verify in `D:\UO\ModernUO-pinned`, not from
   ServUO names.
2. Where the exceptional chance comes from per recipe; hide or disable "exceptional only" for items
   that cannot be exceptional.
3. Whether the toggles are remembered per player.
4. Salvage bag: confirmed present in pinned (see above). Check how to call its salvage methods
   (they are private today) without changing pinned; a small public hook in customizations or a
   documented patch, and which is cleaner.
6. Custodian trash bag: does `ClusterFCustodianSystem.IsEligible` accept freshly crafted items, or
   does it exclude them (it may, to stop crafting for tokens)? If it excludes them, that is the
   intended behavior and the rejects stay in the plain bag. Crafting junk for tokens must not
   become a token farm.

Open questions: none.

Check first (added with the rejects bag):
5. Which craft skills' results can be recycled in pinned, and by what path (smelt, cut, salvage),
   so the per-skill rule above is built from the real list, not from memory.

### F-3: Custodians folded into Clean Up Britannia (added 2026-09-29, was: Custodian scoring by value, cost and rarity)

**Clean Up Britannia is ported; the Custodian layer on it is ours.** Replaces the token math in
`ClusterFCustodianSystem.cs`. F-1's trash bag route depends on it being farm-proof.

What Chase wants:
- A scoring system for Civic Tokens that accounts for an item's cost, rarity and so on.

What the code does today (read 2026-09-29, `ClusterFCustodianSystem.cs:99-160`):
- Weapons and armor: tokens by material (`MaterialTokens(Resource)`), whatever the item is.
- Stackables: amount / 10, at least 1. Everything else: 1 token.
- Corpses: 2 + 1 per 50 gp of estimated vendor value of the contents (`EstimateVendorGold`).
- Eligibility already excludes blessed, quest, named, exceptional weapons and armor, gold,
  and non-empty containers. Crafted non-exceptional weapons and armor are eligible today.

Suggested (overseer):
- **One valuation for everything**, the corpse method: estimated vendor sell value, converted at a
  fixed rate. Two systems (material table for gear, vendor value for corpses) will drift apart.
- **The hard rule: a crafted item must be worth fewer tokens than the materials it used**, after
  what salvage gives back. Otherwise crafting to trash is a farm no matter what curve sits on top.
  This should be a test, not a hope.
- **Rarity as multipliers on the base value**, each an obvious constant: resource tier
  (iron up to valorite), magic properties or item intensity, artifact or rare flag. Exceptional
  stays excluded as it is today.
- **A cap per item**, so one lucky artifact does not pay a week's worth.

Check first:
1. What pinned already offers for an item's value (vendor sell info, `GenericSellInfo`, loot
   intensity, artifact rarity) so the score is read from the game, not from a hand table.
2. What Civic Tokens buy today and roughly what one token is worth in gold. That sets the rate
   and the cap.
3. Whether any other custom system already scores items (work orders, guild) that should share
   this function.

Prior art found 2026-09-29: **OSI's Clean Up Britannia** (ServUO pub57, not in pinned).
- Valuation: `ServUO-pub57/Scripts/Services/PointsSystems/CleanUpBritanniaData.cs`, 980 lines.
  `GetPoints(item)` = a per-type table (`Entries`, e.g. iron ingot 0.10, valorite 10.0) plus special
  cases (runic tools by uses, power scrolls, treasure maps by level, monster statuettes).
- Crafted gear (`GetPointsForEquipment`, `:748`): looks the item up in every craft system and pays
  **resource amount x the per-ingot value** of its material. So a crafted item is worth what its
  ingots were worth. Crafting to trash earns nothing the ingots would not. That is the anti-farm rule
  above, already built in.
- Points are doubles: fractional credit is native to it.
- No diminishing returns. The only brake is that crafting never adds value.
- Turn-in: trash barrels with "Appraise for Cleanup" (`Items/Containers/BaseTrash.cs`), rewards at the
  Cleanup Officer. Built on ServUO's `PointsSystem`, which pinned does not have.
- Already known in our docs: bug-list D33 ranks Clean Up Britannia as a ~20-unit subsystem gate, and
  records (2026-09-29) that its `Entries` table is points earned, not a reward table.

Decision for Chase (overseer recommends A):
- **A. Borrow the valuation only.** Port `GetPoints` and its table as a plain function in
  customizations and have Civic Tokens use it (at a conversion rate). Our Custodian system keeps its
  own turn-in and rewards. Ours, so the fidelity rule does not bind the numbers. Small.
- **B. Port Clean Up Britannia whole.** Faithful OSI system with its own points, barrels and reward
  vendor, beside or instead of the Custodian system. Brings its rewards into reach. It is a
  subsystem (points framework plus rewards), so under the corollary it is a separate decision, not
  part of F-3.

**Decided 2026-09-29 (Chase): neither A nor B as written. Fold the Custodians into Clean Up
Britannia.** Port Clean Up Britannia, and make the Custodian system a layer on it.

Shape (overseer's reading, to confirm):
- **Clean Up Britannia is ported faithfully**: its point table, trash barrels, Appraise for Cleanup,
  the Cleanup Officer and its rewards. The wikis document it, so the fidelity rule binds it: its
  point values and reward prices are not ours to tune.
- **The Custodian layer is ours, added on top**, each addition registered as a deviation and written
  up on our wiki:
  - ground cleanup and the Custodian trash bag earn Clean Up points (valued by Clean Up's own table);
  - corpse cleanup keeps a rule of its own (Clean Up has none for corpses);
  - Custodian ranks are keyed on lifetime Clean Up points; the Sanitation Warden stays as the
    guild's face and his shop is priced in Clean Up points;
  - Civic Tokens retire.
- F-1's trash bag and salvage bag routes plug in unchanged.
- **F-2 dropped** (see Dropped): Clean Up pays crafted gear what its ingots were worth, so crafting
  cannot farm points.

What exists today (read 2026-09-29):
- `ClusterFCustodianSystem.AwardTokens` (`:216`) adds to **account-level** reputation and currency
  (`ClusterFAccountPersistence`, key "custodians"). Ranks (`:228`): Volunteer, Junior Custodian 100,
  Custodian 500, Senior 2,000, Chief 5,000. The Warden sells bandages, refresh and heal potions,
  and the trash bag for tokens (`SanitationWardenGump.cs:254-310`).
- ServUO's Clean Up points live on the **character** (`PointsSystem`), and pinned has no points
  framework (`class PointsSystem` absent from pinned `Projects`).

Size: this is the Clean Up Britannia subsystem gate from bug-list D33 (about 20 units), plus the
Custodian rework. Its own batch, not bundled with small items.

Check first (added):
4. The smallest faithful points framework ModernUO needs for Clean Up alone, and whether any other
   queued port (Virtue Artifacts, bug-list D33) needs the same framework, so it is built once.
5. Every Clean Up reward in pub57 and whether pinned has each item: rewards that do not exist are
   the D32/D33 reachability question again.
6. Rank thresholds rescaled to Clean Up points (a token was 1 per item or more; an iron ingot is
   0.10 points).

Answered 2026-09-29 (Chase):
- **Per character, as OSI does.** The shard will eventually allow one character per account, so the
  per-account question goes away. The Cleanup Point Exchange stone has no use with one character;
  overseer suggests leaving it out and registering that as a deviation, so a wiki reader looking for
  it is told why.
- **Civic Token balances: cleared.** A fresh world is coming, so nothing is converted.
- **One store.** The Warden's shop and the Cleanup Officer's rewards merge: everything OSI offers, plus
  what the Custodians sell now (bandages, refresh and heal potions, the trash bag), plus what we add
  later. OSI's items keep OSI's prices; ours are priced in Clean Up points. Overseer suggests both
  NPCs open the same store, with our items in their own section or marked, so the OSI list stays
  recognizable.

- **Both NPCs** (Cleanup Officer and Sanitation Warden) open the one store (Chase, 2026-09-29).
- **Store order may be sorted by price.** That is the only deviation in the store itself (Chase).
  OSI's items, prices and point values stay exactly as OSI has them.
- **Our items priced close to OSI's model** (Chase). OSI's catalog (pub57
  `CleanUpBritanniaRewards.cs`, 134 rewards): 6 at 1,000; 7 at 5,000; 39 at 10,000; 3 at 15,000;
  10 at 20,000; 30 at 50,000; 2 at 75,000; 2 at 80,000; 4 at 150,000; 24 at 250,000 (pigments);
  6 at 300,000; 1 at 500,000. It sells no consumables.
  Anchor: an iron ingot earns 0.10 points and a blacksmith sells it for 5 gp, so 1 point is about
  50 gp of junk. A dumped iron weapon earns about 1 point.
  Proposed (overseer, awaiting Chase): consumables at about gold value, rounded up, so the store is
  never cheaper than a vendor: 100 bandages 15 (vendor 500 gp), 5 refresh potions 3 (vendor 75 gp),
  3 greater heal potions 5 (no vendor sells them).
- **Trash bag: always free, one per character at a time** (Chase, 2026-09-29). Overseer suggests
  enforcing it by owner, not by searching the pack: the bag records its owner, and asking for a new
  one deletes the old one wherever it is (house, bank, lost on the ground). That also covers a lost
  bag with no special case.

Open questions:
- Approve or change the proposed consumable prices above (15 / 3 / 5).

### F-4: One character per account (added 2026-09-29)

**Ours.** OSI allows several characters per account; this shard will allow one. Fits the vision
("One life. Every skill."). Decided by Chase; timing "eventually", not yet scheduled.

What it touches (overseer, to check when it is scheduled):
- ModernUO's character-slot limit on the login side (verify the real setting in pinned, do not reason
  from ServUO's names), and what an account with more than one character does after the change.
- The fresh world makes the migration question small: set it before the fresh world opens.
- `maxAccountsPerIP` (raised to 25) and bug-list D21: every client arrives from one Docker address, so
  one character per account is not enforceable per person. Alts are one new account away. Decide
  whether that matters for a family shard.
- The launcher, README and wiki account pages, which may describe multiple characters.
- Anything account-wide in our own systems (`ClusterFAccountPersistence`) that becomes simply
  per character.
- F-3: with one character, the Cleanup Point Exchange stone is left out (a registered deviation).

Open questions:
- When: with the fresh world, or later?
- Staff and test accounts exempt?

### F-5: Young status by time only, 2 weeks (added 2026-09-30)

**Ours** (a deviation from OSI's rules, to register and document on the wiki).

What Chase wants:
- Young status ends by **time only, not skill**: **2 weeks**, unless the player ends it early by
  saying **"I want to grow up!"**

What pinned does today (read 2026-09-30):
- `Accounting/Account.cs:21` `YoungDuration = 40 hours`, measured in **account game time played**
  (`CheckYoung`, `:835`). Login message counts down the hours left (`:788`).
- `Mobiles/PlayerMobile.cs:4149`: skill total 450.0 ends Young. This is the rule to remove.
- `PlayerMobile.cs:4121`: gaining a murder count ends Young.
- `Misc/Keywords.cs:40`: "I renounce my young player status" opens `RenounceYoungGump` to confirm.

Suggested (overseer):
- Keep the confirm gump for the new phrase, so a typo or a joke does not end it. Match the phrase
  loosely (case and the "!" optional).
- Keep OSI's phrase working too, so a player reading the wikis is not stuck.
- Keep the murder rule: attacking players while protected should still end protection.
- Update the login countdown to days and hours, and the wiki's Young page.

Check first:
1. Whether our `CharacterCreation.cs` (`:218`) or any custom system also sets or checks Young.
2. Where "created" is stored (account creation date) if the 2 weeks are calendar time.

Open questions:
- **2 weeks of calendar time from account creation, or 2 weeks (336 hours) of time played?**
  OSI counts time played. Calendar time is simpler to explain; played time protects a player who
  logs in once a week.

### F-6: Fog of war on the world map (added 2026-09-30)

**Ours.** OSI has no fog of war; the world map shows everything.

What Chase wants:
- The world map starts dark and reveals the areas a player has actually visited.

The hard part (overseer): **the world map is drawn by the client, not the server.** The family package
ships TazUO; its world map renders straight from the map files on the player's machine. The server
cannot hide part of it. So the options are:
- **A. Client side, in TazUO.** The world map darkens unexplored areas, revealed as the player walks.
  Best result, but it means carrying our own changes to TazUO (a fork, or an upstream feature if
  TazUO already has or would take one), and every TazUO update has to be merged.
- **B. Server tracked, client drawn.** The server records explored areas per character (so it survives
  reinstalls and cannot be edited locally) and sends them to the client; TazUO still has to draw the
  fog, so this is A plus a server half. Only worth it if exploration should count for something.
- **C. Server only, no client change.** An in-game explorer's atlas item whose gump shows the
  explored regions (per region or per grid square, not per tile). Crude next to A, but it touches no
  client code.
Whatever is chosen, a player can still open an outside map (wiki, UOAM). Fog is for fun and
immersion, not secrecy.

Check first:
1. Whether TazUO (the version we ship) already has a fog or explored-area option on its world map.
2. Whether TazUO's world map supports overlays or plugins we could use without a fork.
3. How our package pins and updates TazUO today, i.e. what a fork would cost to keep current.

**Found 2026-09-30: most of the server half already exists.** `ClusterFExplorationManager.cs`
tracks which 8x8-tile chunks each character has walked through, stores them per character serial
in `ClusterFAccountData` (`_exploredChunks`), and sends them on move and login to "the ClusterF
custom client (ClassicUO fork)" over packet 0xF4, whose side is named `FogOfWarManager`. So option B
was started under ClusterF. Chase (2026-09-30): the fork's fog code did not make it into TazUO. So the
server half exists and the client half has to be ported to TazUO. Check first: where that fork's
source is (for `FogOfWarManager` and its 0xF4 handler), and how much of it carries over to TazUO.

Open questions:
- Just the look, or should exploring count for something (a cartographer's reward, an achievement,
  Custodian-style points for mapping)? That decides A versus B.
- Dungeons and other facets too, or the surface first?
- Can a player reveal areas without walking them (buy or craft a regional map, cartography)?

### F-7: Player-usable account reset, for play testing (added 2026-09-30)

**Ours. Test tool.** Chase is play testing with new characters on one account, and guild membership
carries across them because our systems store it per account.

What Chase wants:
- A stone in New Haven, or a player-level command, that wipes the account's stats.

What exists (read 2026-09-30):
- `ClusterFDevTools.cs`: `[ClusterFReset [username]` (**Administrator only**) opens a reset gump with
  checkboxes (Skills, Stats, Achievements, Account Data, Bulletins, Quest History) and a confirm step
  listing what will be cleared. `ExecuteReset` does the work. So this feature is mostly **exposing
  that to players**, not writing a reset.
- `ClusterFAccountData.cs`: account-wide today are Renown, achievement points, guild reputation and
  currency, **joined guilds**, restoration registry, flags, work orders, ore, wood and imbuing
  discoveries, smith commissions, encountered creatures. Exploration is already per character.

Suggested (overseer):
- **A stone in New Haven that opens the same gump**, limited to the user's own account, plus a
  `[ResetMyAccount` command for the same thing. Same code path as the admin tool, so they cannot
  drift.
- ~~Test shard only, behind a config switch.~~ Not needed (Chase, 2026-09-30): only the test shard
  matters; the live shard will be reborn from the test shard's work. When that rebirth happens,
  the stone and command should come out as part of the go-live checklist.
- **Exploration (fog of war) is included in the reset** (Chase). It is stored per character serial
  (`_exploredChunks`), so an account reset clears it for every character on the account.
- Keep the confirm step, and say plainly that it affects every character on the account.
- **Fix the existing reset: "Account Data" does not clear joined guilds.** Confirmed 2026-09-30,
  `ClusterFDevTools.cs:95-102` clears only Renown, guild reputation, guild currency and the
  restoration registry. `JoinedGuilds`, work orders, discoveries, commissions and encountered
  creatures survive it. So today's admin reset would not have fixed Chase's problem either. Add
  joined guilds and work orders at least; decide per item for discoveries and the rest.

Related: F-4 (one character per account) makes the account-versus-character question go away for
players. Until then, the alternative is moving joined guilds (and maybe more) to per character, the
way exploration already is.

Answered 2026-09-30: stone plus command, as suggested; test shard only is the only case.

Open questions:
- Reset tool only, or also make guild membership per character now? (F-9 makes starter kits and
  items per character either way.)

### F-8: Animated runestone, first custom-art test of the client updater (added 2026-09-30)

**Ours.** Purpose: prove the player updater ships a client art change end to end.

Chosen (Chase, 2026-09-30) from a list of ServUO community art: **Animated runestone** by Vrark,
https://www.servuo.dev/archive/animated-runestone.2564/ (art only, no script). Fits the shard as a
time-loop anchor or respawn shrine.

Plan (overseer):
- Add the art to the client files in free art slots, write one small server item that uses it, and
  place one in New Haven (it could be F-7's reset stone, which gives the art a job straight away).
- Ship through the updater; success is a player who updates seeing it animate, and a player who has
  not updated seeing the wrong art (so the test proves the updater, not luck).
- Second, harder test later: an animation pack (e.g. Beholder & Beholder-Kin), which touches more
  files.

Check first:
1. The resource's license or terms on its page.
2. Free art IDs in our client files, so it collides with nothing (including TazUO's own replacements).
3. Which client file it lands in (.mul or .uop) and that file's size, since the updater ships it
   whole.

Open questions: none.

### F-9: Guilds replace the New Haven training quests as the starter path (added 2026-09-30)

**Batched: cc-P15** (2026-09-30).

**Ours** (the guild system, the board's front page). The 26 training quests underneath stay
**ported** and keep working. Decided by the overseer from Chase's brief and confirmed by Chase in
the same conversation, 2026-09-30.

Why: at about 15x skill gain the quests' skill thresholds are passed before the quest registers,
so the quests are only a way to hand out starter items. Guild membership hands them out instead,
and gives the player somewhere to belong from the first few minutes.

What exists (read 2026-09-30):
- `ClusterFGuildSystem.cs`: 15 `GuildDef`s, each mapped to one NPC type. Membership, standing and
  scrip live in `ClusterFAccountData` **per account** (`JoinedGuilds`, `:40`).
- **A guild can already hand items on joining.** `ClusterFGuildSystem.Join` drops kits for mining
  (ore satchel, prospector's logbook, dispatch ledger), smithing (`SmithGuildBook`,
  `SmithGuildSalvageBag`), rangers (Outrider's Crook, Hunter's Satchel), foresters (logbook, lumber
  satchel), artificers (satchel, toolkit) and custodians (trash bag). So the hand-over exists; what is
  missing is per-character tracking and the quest items.
- Our `BaseGuildmaster` extension adds "Talk" to **every** stock guildmaster whose type has a
  `GuildDef`, not just the four custom NPCs. Pinned's post-UOML Trammel spawns put Mage, Healer,
  Tinker, Tailor and two Blacksmith guildmasters in New Haven (`Distribution/Data/Spawns/post-uoml/
  trammel/Vendors.json`; one Blacksmith at 3526,2536 is in the Warrior's Guild Hall). Whether those
  spawns are loaded in our worlds is unchecked (see PT-01).
- `ClusterFNewHavenSeeder.cs` places the quest trainers by hall; `ClusterFInstitutionSeeder.cs`
  places the Miners' Compact Liaison, Outriders', Foresters' and Artificers' guildmasters and the
  Sanitation Warden. `LeagueRegistrarGump` already has "Guild Referrals" and a quest arrow to one
  liaison (`MinersCompactDirectionArrow`); that is the pattern to generalize.
- **Likely cause of PT-06:** membership is per account, so a new character on an account whose other
  character joined the Miners' Compact is already a member and never gets the kit. Confirm with Chase.

**Facts from `notes/cc-P14-newhaven-guild-mapping.md` (CC, 2026-09-30) that bind the build:**
- The Necromancy reward is a **complete** Necromancer spellbook made by the quest's own
  `InternalReward.CreateItem` (all spells set). The guild must reproduce that step or it hands out an
  empty book.
- **Jacob's Pickaxe and the Hammer of Hephaestus are already ours** (replaced at build,
  `apply-patches.sh:241-249`). The pickaxe unlocks `legacy.jacobs_pickaxe` on first `OnAdded`, and the
  Miners' Compact Liaison already reissues it to unlocked members; the smiths recharge the hammer.
  The guild route gives the **first** copy; both keep their existing reissue and recharge rules
  instead of the scrip replacement below.
- Each quest also gives a 15-minute skill-gain acceleration on accept. The guild route does not.
  At our gain rate this is accepted, and is part of the deviation.
- New characters arrive at 3503,2574,14 (`CharacterCreation.cs:114`); the board is 1 tile away.
- Deviation text is drafted in P14 section 5 as **D-92**. The overseer promotes it with F-9's
  answers filled in, after confirming the number is still free.

#### Decision 1: which guilds get a guildmaster, and in what order

Every guild gets one. The rule for order: **guilds that carry a New Haven starter item first**, since
they replace the board, then the rest by how soon a new player needs them.

Two guilds are added, because New Haven has a hall and trainers for each and no existing guild fits
without bending its theme: **the Dojo** (Bushido, Ninjitsu) and **the Necromancers** (Necromancy,
Spirit Speak). Names to be settled with Chase. That makes 17.

Each guildmaster stands in the New Haven hall where that guild's quest trainers already stand
(one hall, one guild), so the building, the trainers and the guild agree.

The 26 quest items, by guild (quest classes from pinned `NewHavenSkillTraining.cs`):

| Order | Guild | Hall (from the seeder) | Starter items (skill) |
|---|---|---|---|
| 1 | Warriors' Brotherhood | Warrior's Guild Hall | Bulwark Leggings (Chivalry), Gloves of Safeguarding (Wrestling), Churchill's War Mace (Macing), Recaro's Riposte (Fencing), Arms of Armstrong (Tactics), Jockles' Quicksword (Swords), Escutcheon de Ariadne (Parry), Clasp of Concentration (Focus) |
| 2 | Arcane Society | Magery School | Bracelet of Resilience (Resist), Philosopher's Hat (Meditation), Hallowed Spellbook (Inscription), Ember Staff (Magery), Ring of the Savant (Eval Int) |
| 3 | Healers' Covenant | Healer's Hall | Tunic of Guarding (Anatomy), Healer's Touch (Healing) |
| 4 | Rangers' League (Outriders) | stays at the animal stables (3524,2574), Chase 2026-09-30 | Heartseeker (Archery), Walker's Leggings (Tracking) |
| 5 | Miners' Compact | Mine camp, south mountains | Jacob's Pickaxe (Mining) |
| 6 | Smiths' Fellowship | Forge and Anvil | Hammer of Hephaestus (Blacksmithy; our override of the pinned item) |
| 7 | Tinkers' Union | Springs N Things | Amelia's Toolbox (Tinkering) |
| 8 | Thieves' Den | new NPC in the back room of the Bountiful Harvest Inn (3493-3510, 2513-2530), Chase 2026-09-30 | Bag of Smoke Bombs (Hiding), Twilight Jacket (Stealth) |
| 9 | Twin Paths Dojo (new) | Ninja Dojo | Silver Serpent Blade (Ninjitsu), The Dragon's Tail (Bushido) |
| 10 | Keepers of the Last Door (new) | Necromancers Guild Hall | the Allure of Dark Magic reward (Necromancy; pinned uses an `InternalReward`, check what it gives), Bag of Necromancer Reagents (Spirit Speak) |

Placements decided by Chase, 2026-09-30, for the rest: **Maritime** on the docks (pinned spawns two
Fishermen there, 3504,2612 and 3520,2598); **Bards** in the Bardic Guild building (3408-3421,
2598-2612); **Merchants** at the provisioner. Pinned spawns no provisioner in New Haven, so CC finds
the provisioner's building (or the nearest general store) and says where; the bank is the fallback.
**Fix while there:** the New Haven Artificers' Guildmaster stands in the water
(`ClusterFInstitutionSeeder.cs`, 3490,2627,0; reported by Chase 2026-09-30). **Move it into the Magery
School**, with the magery quest trainers (Chase, 2026-09-30). Say how the one already placed on each
world gets moved (a world-state step, Chase's call). The Ter Mur one stays.

Then, with no quest item but useful early: 11 Foresters' Union, 12 Tailors' Circle, 13 Maritime
Brotherhood, 14 Custodians (Sanitation Warden), 15 Merchants' Exchange, 16 Bards' Consortium,
17 Artificers' Order (advanced; keeps its Ter Mur post and its New Haven office).

Where a stock guildmaster type already maps to a guild (Mage, Healer, Tinker, Tailor, Blacksmith,
Warrior, Thief, Bard, Fisher, Merchant, Miner), use it rather than writing a new NPC. Placement goes in
our seeder, never in pinned spawn data.

#### Decision 2: how a new player finds a guildmaster in the first few minutes

1. **The board stays the front door.** Same item, same spot (3502,2573,14, beside Sir Helper). Its
   first page becomes a **Guild Directory**: one row per guild, the skills it teaches, where its hall
   is, and **Show me the way**, which starts a quest arrow to that guildmaster (generalize
   `MinersCompactDirectionArrow`). A row the player has joined shows their rank instead.
2. **First login points at it.** A new character's first login opens a one-page welcome ("Every skill
   has a guild in New Haven. The Guild Board in the square will point you to them.") with a button that
   sets the arrow to the board. Once per character, never again.
3. **The same directory everywhere.** `[guild` (`GuildProgressGump`) and the League Registrar's Guild
   Referrals show the same rows with the same arrow, so no route leads to a different list.
4. **Trainers point home.** Each New Haven quest trainer's talk adds one line naming the guild whose
   hall they stand in.
5. Joining happens at the guildmaster, not the board. The walk teaches the town, and the guildmaster
   is where contracts and services live. The arrow keeps the walk short.

#### Decision 3: what joining requires

**Nothing.** Any character can join any guild, free, with one click, at rank Initiate. The current
skill-or-tribute tasks (Mining 50 or 20 iron ore, 500 gold for the Merchants, Stealing 20 for the
Thieves) become the **Apprentice task**: meeting it later raises the rank and pays the reputation and
scrip that joining pays today. Nothing is consumed to join.

The stock NPC guild (say the guildmaster's name and "join", pay 500 gold, one guild at a time, shop
discount) stays as it is: it is ported and the wikis describe it. Our join gump says in one line that
the two are separate.

#### Decision 4: how starter items change hands

- **Tools on joining = the character-creation items for the guild's skills** (Chase, 2026-09-30).
  One list, not a second copy: our `CharacterCreation.cs:916` `AddSkillItems(Mobile, SkillName)`
  (today `private`, called at `:476`) is made callable and the guild calls it once per skill in its
  list below. So joining the Healers gives exactly what picking Healing and Anatomy at creation gives
  (50 bandages, scissors, 3 bandages, a robe). Items whose slot is taken go to the pack
  (`EquipItem`, `:697-722`, already falls back to the pack). An item type already handed over in the
  same kit is not given twice (Tactics and Swords both give a sword). Skills with no creation items
  (Meditation, Eval Int, Resist, Focus, Stealth and others) add nothing. The existing guild join
  bonuses (satchels, logbooks, crook) are kept on top.
- **Signature items on request.** The guildmaster's "Starter items" page lists that guild's quest
  items; the player takes each one when they want it (keeps the pack light and lets them pick a
  weapon line). No task, no skill gate.
- **Once per loop, free** (Chase, 2026-09-30). The tools and each signature item are free once in
  each loop; the record resets when a new loop starts. Until loops exist, a loop is a character.
  Tracked per character, not per account, whatever F-4 and F-7 decide about membership. A second character on a member account can still take its kit and items ("Welcome
  back" rather than "already a member"). This also fixes PT-06.
- **One ledger shared with the quests.** Taking an item from the guild marks the matching MLQuest done
  for that character (`MLQuestContext.SetDoneQuest`; pinned does the same thing from outside the quest
  system in `Heritage.cs:424`). Finishing the quest first shows the item as already received at the
  guild. So each item is paid once, by either route. Register this as a deviation (the quest counts as
  done without being done); take the next free D-n when writing it.
- **Lost items can be replaced** within the same loop for guild scrip, at the guildmaster (except
  Jacob's Pickaxe and the Hammer of Hephaestus, which keep their own rules, above). A family tester who loses a
  weapon to a death should not be locked out.

#### Skills per guild (proposed; decides each guild's creation kit)

Every one of pinned's 58 skills (`Server/Skills.cs`, `enum SkillName`) belongs to exactly one guild.
The last three placed were Forensics, Taste ID and Spellweaving (overseer, 2026-09-30; Chase to confirm).
Chase adjusts; the table is data, one line per guild.

| Guild | Skills |
|---|---|
| Warriors' Brotherhood | Swords, Macing, Fencing, Wrestling, Tactics, Parry, Chivalry, Focus, Throwing |
| Arcane Society | Magery, Eval Int, Meditation, Resist, Inscription, Mysticism, Spellweaving (the guildmaster also points to pinned's unlock chain in `Engines/ML Quests/Definitions/Spellweaving.cs`, starting with `Patience`, with a quest arrow if the giver is on the same map) |
| Healers' Covenant | Healing, Anatomy, Alchemy, Taste ID |
| Rangers' League | Archery, Tracking, Animal Taming, Animal Lore, Herding, Veterinary, Camping |
| Miners' Compact | Mining |
| Smiths' Fellowship | Blacksmithy, Arms Lore |
| Tinkers' Union | Tinkering |
| Thieves' Den | Hiding, Stealth, Stealing, Snooping, Lockpicking, Poisoning, Detect Hidden, Remove Trap |
| Twin Paths Dojo | Bushido, Ninjitsu |
| Keepers of the Last Door | Necromancy, Spirit Speak, Forensics |
| Foresters' Union | Lumberjacking, Carpentry, Fletching |
| Tailors' Circle | Tailoring |
| Maritime Brotherhood | Fishing, Cartography, Cooking |
| Merchants' Exchange | Item ID, Begging |
| Bards' Consortium | Musicianship, Peacemaking, Provocation, Discordance |
| Artificers' Order | Imbuing |
| Custodians | none (keeps its trash bag) |

#### Gargoyles (Chase, 2026-09-30: gargoyle options must be included)

The three gargoyle skills have homes: **Throwing** with the Warriors (it is a weapon skill; moved off
the Dojo), **Mysticism** with the Arcane Society, **Imbuing** with the Artificers. Rules:
- **Creation kits are already race-aware.** `AddSkillItems` gives gargoyles their own items (gargish
  shield for Parry, gargish arms for Wrestling, DreadSword, DiscMace, BloodBlade, SerpentstoneStaff,
  GlassStaff, Boomerang for Throwing). Calling it for guild tools keeps that for free. A test joins each
  guild as a gargoyle and asserts every item handed over can be equipped or used by a gargoyle.
- **Mysticism's creation kit is empty today** (`CharacterCreation.cs:1325-1329`, the book line is
  commented out). Pinned has 8 Mysticism spell files (`Spells/Mysticism`) and no mystic spellbook
  type was found. Check what book, if any, pinned or our tree has (ours has
  `FallenMysticsSpellbook`, an artifact, not a starter), and give gargoyle Mysticism starters a
  book and reagents if one exists; say so if not.
- **Signature items must fit gargoyles.** Several of the 26 quest items are human or elf wear
  (leggings, tunic, jacket, hat, gloves) a gargoyle cannot equip. Check each against pinned's race
  rules. Where a gargoyle cannot use one, the guild hands a gargish equivalent with the same
  properties (ours; register with the quest-done deviation), or says plainly there is none. The
  choice is shown before the item is taken.
- **Where gargoyles start: New Haven, for now** (Chase, 2026-09-30, as observed; CC confirms in
  `CharacterCreation.cs`). So gargoyles use the same board and guildmasters as everyone else.
- **Ter Mur may come later** (Chase: gargoyles may start there, with their own quest givers and
  guildmasters). Build for it now so it is data, not a rewrite: a guild can have more than one
  guildmaster location (the Artificers already do: New Haven and Ter Mur), the directory lists each
  location with its own arrow, and the first-login welcome points to the board in the character's
  starting town. Membership, tools and starter items are the same whichever guildmaster a player uses.
  Ter Mur's own content is F-10.

#### Decision 5: what happens to the New Haven quest board

**Kept, repurposed, never removed** (bug-list E3: held quests are saved by giver serial). The
Guild Directory becomes its first page; the 26-quest picker stays as its second tab, "Training
quests", unchanged, for players following the wikis. PT-03 (board and trainers interchangeable)
still applies to that tab. Nothing is placed or removed on live by this change.

#### Check first

1. `SetDoneQuest` from our code: confirm the 26 are `OneTimeOnly` (the first three are, `:15`,
   `:38`, `:62`) and that marking done has no side effect beyond the record (no reward, no
   achievement double-count).
2. What `TheAllureOfDarkMagic`'s `InternalReward` gives, and whether each of the 26 items is blessed
   or insured by default (decides how often replacement is needed).
3. Whether pinned's post-UOML vendor spawns are loaded on the test and live worlds, so we know which
   stock guildmasters already stand in New Haven and which our seeder must place (ties to PT-01).
4. Which GuildDef points at which NPC: mining's def names `MinerGuildmaster` while the liaison is a
   separate `MinersCompactLiaison` type. One guild, one NPC type, or the directory's arrow may point
   at the wrong one.
5. The Warrior's Guild Hall already has a spawned Blacksmith guildmaster (3526,2536). Decide who
   stands where before placing a Warrior guildmaster there.
6. Every new per-character record must be cleared by the reset in F-7 (and the dev reset's
   "Account Data" defect, `ClusterFDevTools.cs:95-102`, fixed with it), or the flow cannot be re-tested.
7. Which skill each creation kit belongs to is the table above; check every `case` in
   `AddSkillItems` lands in exactly one guild, as a test, so a new skill case cannot go homeless.

#### Tests (watched red, then green)

- A fresh character joins with no skill and no gold, and gets its tools once.
- A second character on the same account gets its own tools and items.
- An item taken from the guild marks the quest done; the quest then pays nothing more. The reverse
  also holds.
- The board's directory arrow points at a guildmaster that exists; a missing one says so instead of
  failing silently.

Open questions:
- The exact tile for the Thieves' Den guildmaster by the fighting pit.
- Answered 2026-09-30: tools are the creation items (above); starter items are free once per loop.
- Answered 2026-09-30: the new guilds are named **the Twin Paths Dojo** and **the Keepers of the
  Last Door**.

### F-10: Ter Mur as a second starting town for gargoyles (added 2026-09-30)

**Ours** for new NPCs, guildmasters and any starter path; **ported** for Ter Mur itself and any SA
quests pinned already has there. Not scheduled. Chase: gargoyles start in New Haven today; that may
change, with quest givers and guildmasters in Ter Mur.

What it would mean:
- Gargoyle characters start in Ter Mur (the Royal City), everyone else in New Haven. Or a choice at
  creation. Chase decides.
- Ter Mur gets its own guild presence: a board and guildmasters for the guilds a gargoyle is most
  likely to join (at least Warriors for Throwing, Arcane for Mysticism, Artificers for Imbuing,
  which already has its Ter Mur guildmaster at 797,3431,-10). F-9 is built so this is a list of
  locations, not new code: a guild can have several guildmasters, and every one hands out the same
  tools and items.
- Gargish starter items: F-9 already requires a gargish equivalent where a New Haven item cannot be
  worn by a gargoyle. Ter Mur would hand out the same ones.
- A way between the two towns early on (a moongate route or a ferry NPC), so a gargoyle can reach the
  guilds that stay New Haven only.

Check first (when scheduled):
1. What pinned already has in Ter Mur for new characters: SA starting quests, their givers and
   rewards (`Engines/Quests`, `Engines/ML Quests`), and pinned's Ter Mur spawns
   (`Distribution/Data/Spawns/.../termur`). Build on those rather than beside them.
2. Where pinned's character creation can place a gargoyle (start locations list), and our override in
   `CharacterCreation.cs`.
3. Whether Ter Mur's decoration and spawns are present in our worlds (PT-01 found New Haven's missing).
4. Young status and the Ter Mur region: whether Young protection applies there as in New Haven.

Open questions:
- Gargoyles always start in Ter Mur, or they choose?
- Which guilds get a Ter Mur guildmaster, and does Ter Mur get its own starter quests (like New Haven's
  26) or only the guild route?

## Batched

| ID | Batch prompt | Notes |
|---|---|---|
| F-9 | cc-P15-guild-starter-path | Written 2026-09-30. Entry kept under Open while its open questions stand. |

## Dropped

| ID | Why |
|---|---|
| F-2 | Diminishing returns (with fractional credit) on Custodian tokens for repeated items. Dropped 2026-09-29 by Chase: F-3 folds the Custodians into Clean Up Britannia, whose valuation pays crafted gear only what its ingots were worth, so crafting cannot farm points and the curve has nothing to stop. |
