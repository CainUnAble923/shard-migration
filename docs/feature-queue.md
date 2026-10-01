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
**Next free: F-25.**

The fidelity test: could a player be misled by a difference they had no way to know about?
Port a gated item when the gate is small and near; skip it when the gate is a subsystem.

## Where things stand (handoff, updated 2026-10-01, 10:50)

For a new overseer chat: read this section, then the entries it names. The project-wide picture
(prompt states, bug numbers, the concurrency rule) is in `notes\passdown-overseer-2026-10-01.md`.

- **Prompt numbers moved overnight.** P23 is the live defect sweep (D42, D43, D41, D13, running) and P24
  the New Haven dungeon research (running, read only). P25 is reserved for the stats-above-125 research
  pass (F-12). F-8's prompt is cc-P26.
- **One builder at a time in `D:\ShatteredLegacy`.** Build order: P23, then **P22** (it shares
  `ClusterFGuildSystem.cs` and the starter-path quest arrow with P23), then P26 (F-8, written). Notes-only
  prompts (P24, P25) run alongside anything.
- **Batched:** F-9 (cc-P15, ran), F-7 + F-5 + F-1 (cc-P18), F-12 research only (cc-P20, done).
  **cc-P22-small-features-1**: F-16, F-19, the thief at the pit (F-9 follow-up), F-11, F-17, F-15.
- **cc-P26-animated-runestone (F-8) is written** (`D:\UO\cc-prompts\`, 2026-10-01). Runs after P23 and
  P22 commit. It builds the art pipeline: our PNGs ship, the player's own tiledata and animdata are
  patched locally, TazUO starts with `-uofilesoverride`. F-21, F-22 and F-23 wait on it. **F-22 has a
  date: on the test shard before December 1.**
- **Next prompt to write:** none queued. Candidates in order: F-14, then F-24; F-3; F-18.
- **Ready to batch, no open questions, each its own batch:**
  - F-3 (Clean Up Britannia with the Custodian layer; about 20 units).
  - F-18 then F-20 (BODs for growth, smithing and tailoring; then other crafts, Carpentry and
    Tinkering first). After P22, which changes the same BOD gumps.
  - F-14 (Appraisal and con colors; the level number waits on F-12).
  - F-24 (League work: jobs, realm-wide boards, guild currency and banked reputation). After F-14,
    with F-12's XP in place; dives after the P24 dungeon work.
  - F-6 (fog of war with the Cartography tie-ins; the TazUO client half to scope first).
  - F-22 (winter decor Dec 1 to Jan 6, both layers; art in `D:\UO\third-party\winter-holiday\`;
    skip Vrark's two animated trees). After F-8.
- **F-12 and F-13 are redesigned** in `notes\f12-levels-loops-caps.md` (max level 200; vet reward is now
  +50 total stat cap). The queue entries carry pointers; that doc governs. F-13 is no longer "ready":
  re-read it against the new doc before batching.
- **Waiting on downloads** (servuo.dev daily limit hit 2026-09-30): the rest of F-21's packs (farm carts
  are in `D:\UO\third-party\farm-carts\`) and F-23's Siege of Sosaria paperdoll kit. Downloads land in
  Chase's Downloads folder; the overseer copies them to `D:\UO\third-party\`.
- **Waiting on Chase:**
  - F-9 follow-up: confirm the pit stool at 3440,2558,55 in game (`[go 3440 2558 55`).
  - F-12: the three placeholder numbers (reserve cap, echo multipliers, step size above 100); how
    each League metal rank is earned.
  - F-23: paperdoll kit for everyone, or opt-in? NSFW paperdoll question still unanswered.
  - F-4, F-10: not scheduled.
- **Free art slots:** OSI's "UNUSED" placeholder art marks free slots in `artLegacyMUL.uop` (found
  checking the farm carts, F-21).
- **Fixed 2026-10-01:** the F-9 "Open gap" note had been inserted mid-sentence into the 15-minute
  acceleration decision; the two are separated again.

## Open

### F-1: Craft X, keep going on failure (added 2026-09-29)

**Batched: cc-P18** (2026-09-30).

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

Answered 2026-09-30 (Chase): **consumable prices approved as proposed**: 100 bandages 15, 5 refresh
potions 3, 3 greater heal potions 5.

Open questions: none.

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

**Batched: cc-P18** (2026-09-30).

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

Answered 2026-09-30 (Chase): **2 weeks of time played**, i.e. `YoungDuration` 40 hours -> 336 hours
of game time. Same counter OSI uses, so only the number and the skill rule change. Login message
should show days and hours (14 days of play will take most players months).

Answered 2026-09-30 (Chase): **Young stays per account**, as pinned has it. Account game time counts,
and ending Young ends it for every character on the account.

Open questions: none.

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

Answered 2026-09-30 (Chase): **exploring earns something**, so option **B** (the server tracks, TazUO
draws). **Dungeons and every facet**, not only the surface. **Tie it into Cartography.**

Found 2026-09-30: the tracker already stores chunks per facet for all six (Felucca, Trammel, Ilshenar,
Malas, Tokuno, Ter Mur; `ClusterFExplorationManager.cs:31-38`). The Felucca and Trammel dungeons sit on
the same maps east of x 5120, so they are covered. The account data is already large (cc-P15 measured a
912 KB blob, mostly exploration bits); keep an eye on it.

Suggested (overseer), for Chase to react to:
- **Cartographers sell what they have walked.** A map a cartographer draws (local, city, sea or world,
  as in OSI) records the chunks its maker explored inside its bounds. Reading it reveals those chunks
  for the reader. Higher skill, bigger map. A player can buy a map of Ilshenar instead of walking it.
- **Decoding a treasure map** reveals the chunks around the chest.
- **Exploration achievements by percent explored**, per facet, per dungeon and **per town** (Chase,
  2026-09-30) (25 / 50 / 75 / 100), paying AP and Renown like the rest. The seven exploration
  achievements today only mark a visit. Towns and dungeons are bounded by their regions in pinned.
- Maybe: walking an unexplored chunk gives a small chance at a Cartography gain. That changes OSI's
  gain rules, so only if Chase wants it.

Answered 2026-09-30 (Chase): **all four approved**: cartographers' maps reveal what their maker
walked; decoding a treasure map reveals the area around the chest; percent-explored achievements per
facet, dungeon and town; a small Cartography gain chance on new chunks (a deviation; register it).
**Only walked chunks count** for achievements; map reveals do not.

Open questions: none. Ready to batch once the TazUO client half is scoped (check first, above).

### F-7: Player-usable account reset, for play testing (added 2026-09-30)

**Batched: cc-P18** (2026-09-30).

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

Answered 2026-09-30 (Chase): **per character for now.** Guild data moves from the account to the
character, keyed by character serial the way exploration already is (`_exploredChunks`).
Overseer: move **joined guilds, guild reputation and guild currency together**; membership without
its reputation, or reputation shared across characters, would be half the fix. Guild work orders
likely follow. Keep it easy to fold back to account-wide when F-4 lands. Existing saves: clear guild
data rather than guess which character it belonged to. Fits F-9, which already makes starter kits
and items per character.

Open questions: none.

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

**Art downloaded 2026-09-30** (Chase, logged in to ServUO): `D:\UO\third-party\animated-runestone\`.
The zip holds four GIFs and four zips of PNG frames. Unpacked (overseer) to `frames\stone1` to
`frames\stone4`: **four stone designs, 11 frames each**, RGBA PNG, sizes 66x115, 94x117, 66x124 and
80x111, frame time 80 to 90 ms (from the GIFs). Preview: `contact-sheet.png`. **No license file in the
download and none on the page**; the resource is posted for the ServUO community to use. Overseer
suggests a thank-you post on the thread asking whether shard use is fine, for the record.

Answered 2026-09-30 (Chase): **all four, as variations** of the one item (like OSI items that turn
between graphics; the reset stone can pick one, or the player turns it).

**Found writing cc-P26 (overseer, 2026-10-01), verified in code:**
- **The plan's step 1 breaks a package rule.** "Add the art to the client files" means shipping a
  modified `artLegacyMUL.uop`, but the player package ships **nothing of EA's**; the player's own EA
  install supplies the data (`player-package\Build-PlayerPackage.ps1:19`, `payload\app\Setup.ps1:33-34`).
- **Still art has a clean route.** TazUO loads PNG overrides by art ID from
  `ExternalImages\art\<id>.png` (key is id + 0x4000), checked **before** EA's art, for any ID inside
  the art file's range (TazUO 7deed69, `ClassicUO.Assets/ExternalImageLoader.cs:299-313`,
  `ClassicUO.Renderer/Arts/Art.cs:183-193`). Our build already ships Fiddle-Me-This's gump PNGs this way
  from `vendor\`; art PNGs would go the same way. Our own PNGs are not EA's files.
- **Animation does not.** A static animates only when its `tiledata.mul` entry has the Animation flag
  and `animdata.mul` lists its frames (`AnimatedStaticsManager.cs:20-46`, `AnimDataLoader.cs:33-48`).
  Both are EA files and an UNUSED slot has neither. TazUO accepts `-uofilesoverride <file>`, a list of
  `name=path` lines that redirects any data file (`Main.cs:267-270`, `UOFilesOverrideMap.cs`).
  So the route that keeps the rule: **ship only our records** (4 tiledata entries, 4 animdata entries)
  and have Setup/Update **build patched copies on the player's machine from their own EA files**, then
  launch with `-uofilesoverride`. Play.ps1 starts TazUO at `payload\app\Play.ps1:303`.
- **The Reset Stone is a test-shard tool** that comes out at the live rebirth
  (`server\customizations\ClusterFResetStone.cs:3-6`), so art that lives only on it leaves with it.
  Its graphic is one constant for F-8 to change (`:115-117`).
- Frame data: animdata stores up to 64 frames as signed offsets from the base ID, so each stone wants
  11 free IDs close together; 4 stones need 44. Free slots: OSI's UNUSED placeholders (F-21 note).

**Decided 2026-10-01 (Chase):**
1. **Build on the player's machine.** Ship our PNG frames and our own tiledata and animdata records
   only; Play.ps1 builds patched copies of the player's own EA files and starts TazUO with
   `-uofilesoverride`. This is the pipeline F-21 to F-23 reuse.
2. **Its own item** (a standalone runestone, expected to become the F-12 loop stone later); the Reset
   Stone borrows its look on the test shard.
3. **Staff choose the design** per stone; players do not turn public stones.

Batched: **cc-P26-animated-runestone**, written 2026-10-01. Runs after P23 and P22 are committed.

Open questions: none. Ready to batch.

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
  **Decided 2026-09-30 (Chase): leave it out, deliberately.** Fifteen minutes is too short to matter, and at
  our skill rates the difference is not observable in play. Do not build parity, and do not treat the absence
  as an oversight later. The wiki should say the two routes differ only in this, and that it is intentional.
  At our gain rate this is accepted, and is part of the deviation.
- **Open gap found in play, 2026-10-01: nothing points a player to the League of Extraordinary
  Citizens.** F-9 specified that the Registrar shows the **guild** list, a second doorway inward. It
  never specified the reverse, so cc-P15 built what it was told and this is **not a defect**. But the
  League has a registrar, member passes, its own system and a field office being decorated in cc-P19,
  and a new character has no way to learn any of it exists. That is the same visibility problem the
  Guild Directory was built to solve, one level up. **For the features chat to decide**: does the
  League belong in the directory, does it get its own entry point, or is it meant to be found only by
  walking into the office? Related: T-040, and verify separately that the Registrar does show the
  guild list as F-9 specified; if it does not, that part **is** a cc-P15 defect.
  **Decided 2026-10-01 (Chase):** the League is open from day one, and it is **the guild for the
  guilds**, the organization that ties them all together (not one more guild beside them). Entry
  points:
  1. **Guild Directory:** one League row, set apart **at the top** as the umbrella over the guild rows
     (overseer placed it at the top to match "guild for the guilds"; Chase can move it), with
     **Show me the way** to the League Registrar.
  2. **First-login welcome page** names the League in one line next to the Guild Board line.
  3. **A sign outside the field office** (cc-P19's office), readable from the street.
  4. The Registrar's greeting introduces the League. Note: this only reaches a player who has
     already found the office, so 1 to 3 are the real pointers.
  Same rule as Decision 2.3: `[guild`, the board and the Registrar show the same rows.
  Size: small, likely folds into the next batch that touches the directory. What the League hands out
  is F-24.
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
- Answered 2026-09-30 (Chase): the guildmaster stays in the tavern's back room (cc-P15 seeded it in
  the inn's stone storeroom, 3495,2515,27). The NPC by the fighting pit is a **lower-rank Thieves' Den
  member** who sends players to the guildmaster. The pit is "behind the healers": read from the client
  map 2026-09-30, it is the sunken floor in the building west of the Healer's Hall, **3442-3448,
  2554-2560, z30**, with blood stains on it and benches around it at z55. Snapshot:
  `D:\UO\snapshots\newhaven-pit-closeup.png`. Chase to confirm in game with `[go 3445 2557 30`.
  **The thief sits on a stool by the pit** (Chase, 2026-09-30). Pick: the stool at **3440,2558,55**
  (static 0xA2A, upper floor, west of the bench ring, facing east over the pit); CC sets the Z from
  the stool's tiledata height. Goes in a later batch as a small seeder addition.
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

### F-11: Guild upgrades draw resources from the bank as well as the backpack (added 2026-09-30)

**Ours** (guild upgrades are our systems; OSI crafting stays pack-only and is not touched).

What Chase wants:
- Guild item upgrades (and restorations) count and consume resources from the bank box as well as
  the backpack.

What exists (read 2026-09-30):
- **Gold already does this** for the Miners' Compact: `CompactGoldHelper.cs` counts backpack plus bank
  balance and consumes backpack first, then withdraws the shortfall from the bank. Used by
  `MinersCompactLiaisonGump.cs`, `ArtificersImbueGump.cs`, `CrossGuildExchangeGump.cs` and the four
  Jacob's pickaxes.
- **Resources do not**: e.g. `MinersCompactLiaisonGump.cs:536-549` and `:675-689` check
  `Backpack.GetAmount` for ingots, and `:871-873`, `:1021-1039` consume with `pack.ConsumeTotal`.
  Other backpack-only consumers: `ClusterFGuildSystem.cs`, `ClusterFWorkOrderSystem.cs`,
  `HammerOfHephaestus.cs`, the Jacob's pickaxes.

Suggested (overseer):
- **One shared helper** beside `CompactGoldHelper` (or generalize it): count a resource type across
  backpack and bank box, consume backpack first, then bank, and **all-or-nothing** (check the total
  before consuming anything, so a failure never takes half). Every guild upgrade uses it, so they
  cannot drift.
- The gump shows where the materials will come from ("60 valorite: 20 in pack, 40 in bank").
- Scope: guild upgrades, restorations **and work order turn-ins** (Chase, 2026-09-30).

Check first:
1. Every guild upgrade and restoration path that consumes resources (list above is a start).
2. Whether our resource satchels (ore, lumber) in the pack or bank should count too, and how
   `GetAmount` treats nested containers in pinned (cite).
3. Whether the bank box is always loaded for an online player in pinned, or only after it is opened.

Answered 2026-09-30 (Chase):
- **Resources inside satchels count too** (ore satchel, lumber satchel and the like), in the pack or
  the bank. Consume loose resources first, then satchels, so a player's sorted stock is used last.
- **Work order turn-ins draw from the bank too.** For turn-ins that need specific crafted items
  (not raw resources), the same rule: pack first, then bank, all or nothing. Items that are equipped,
  blessed, or inside a locked or secure container are never taken.

Open questions: none.

### F-12: Player levels and XP, modeled on ServUO's Level System Extreme (added 2026-09-30)

> **REVISED 2026-10-01. Max level is 200, not 1000, and the ladder below is superseded.**
> The current design is `notes\f12-levels-loops-caps.md`, decided from cc-P20's research.
> Where that doc and this entry disagree, that doc governs until this entry is rewritten.

**Ours.** OSI has no levels. Fits the vision (LitRPG, levels, prestige, Dungeon Crawler Carl).

What Chase wants:
- A level system like **Level System Extreme** (Kamras, v4.0,
  https://www.servuo.dev/threads/level-system-extreme.12815/): XP from combat and skills, levels,
  points on level-up, titles by level, pet levels, daily login bonus scaled by level, level
  requirements on equipment.

Overseer: **borrow the design, not the code.** It needs edits to ServUO core files (SkillCheck,
BaseArmor, BaseWeapon, BaseClothing, BaseJewel), relies on XmlAttach, and users report data loss
from serialization changes on its major updates. Built our way it sits on what we have: the
achievement system (`ClusterFAchievements.cs`, about 80 achievements, AP and Renown), league, and
the System's snarky voice for level-up messages.

Suggested:
- XP from what players already do (kills, skill gains, crafting, gathering, discoveries), fed by the
  hooks the achievement system already has (`NotifyKill`, `NotifyCraftedItem`, `NotifyMining`...).
- Level-up popup in the System's voice, like the achievement earned popup.
- **Titles earned** (by level and by achievement), chosen by the player and shown under the name.
- Level requirements on gear only for **our** items, never OSI items (fidelity).

**Merge direction (Chase, 2026-09-30):** possibly a merge of Level System Extreme and the Mythik
Achievement System (DarkLotus, MIT, https://github.com/DarkLotus/MythikAchievmentSystem), on top of
our own achievement system. Chase wants Mythik's achievement framework as the base rather than
reinventing it.

What each offers (read 2026-09-30):
- **Level System Extreme** v4.0, updated 2026-05-27, ServUO 57.4, needs XmlSpawner/XmlAttach and
  distro edits (reduced over time to about one). Features: player and pet levels, XP from skills and
  from bulk order deeds, dynamic equipment level requirements, mount level requirements, vendor
  discounts by level, pet special attacks, bonus stats from pets, pet stealing, level items (level
  bags, coins and tokens, a weightless blessed TreasureTrove at level 100+), an in-game control item
  (`[levelcontrol`) for settings, a tracking and teleport gump. Terms and XP formulas not visible
  without the download.
- **Mythik** (706 lines, cloned and read): achievements are **typed classes**, one line each to
  define: `HunterAchievement` (kill N of a creature type), `HarvestAchievement` (gather N of a
  resource type), `DiscoveryAchievement` (enter a named region), `ItemCraftedAchievement` (craft N
  of an item type), `SkillProgressAchievement` (reach a skill value; disabled in ServUO for lack of
  a SkillGain event). Each has an ID, **sub-categories** (parent/child tree), an item icon, **hidden
  until complete**, reward points, a completion target, reward items, a completion date, and the
  `[feats` / `[achievements` command. Stored per character serial.
  Gaps found: its prerequisite parameter is accepted but never stored (prereqs do not work); only
  the first reward item is ever given; points are a flat number per achievement (5 in every
  example), with no point thresholds or gates; about 30 example achievements; stock gump art only.
- **Ours already has**: about 80 achievements, AP and Renown, working prerequisites, progress bars,
  reward items, the System's voice. What Mythik adds is the **typed, data-driven definitions,
  sub-categories, hidden achievements and icons**.

**Level System Extreme source read 2026-09-30** (downloaded by Chase; unpacked at
`D:\UO\third-party\level-system-extreme\src\`, 83 files, about 24,000 lines, version of
2026-05-27). **No license file**, only a credits list: take design, not code.
- **Levels**: default max 150, raisable to 200 with a `RaiseMaxLevelScroll`
  (`LevelControlSys.cs:54-56`).
- **XP to next level = level x tier multiplier**, 100 at levels 2-20 up to 6,000 at 191-200
  (`LevelHandlerExt.cs:300-333`, `LevelControlSys.cs:66-82`).
- **XP sources**: kills, by monster tier tables (e.g. 20-40 XP for weak creatures up to 200-225 for
  the strongest, some creatures none; `LevelCore.cs:93-108`, `ExpTables.cs`), skill use (needs a
  SkillCheck core edit), crafting armor, bulk order deeds, party sharing, power-hour tokens.
- **Each level-up grants 4 skill points and 3 stat points** by default (`LevelControlSys.cs:265-300`).
  **Skill points are spent in its gump to raise a chosen skill by +1.0 directly**
  (`PlayerLevelGump.cs:486-488`), within configurable total caps that default very high. Also
  follower slots at every tenth level.
- **Storage**: a hidden LevelSheet item in the backpack plus an XmlSpawner fork. A hidden control
  item at Trammel 5427,1081,5 holds all settings (`LevelControlSys.cs`, 5,219 lines).
- **Extras**: level-gated vendors (19 of them, levels 10 to 250), level gates and tiles, level bags,
  XP and skill coins, boots of travel, skill-reset and set-level tokens, TreasureTrove (weightless,
  blessed, level 100+), pet levels with orbs, pet special attacks, pet lock picks (pet stealing).
- **Core edits** for full features: BaseArmor, BaseClothing, BaseJewel, BaseWeapon (level
  requirements), SkillCheck (skill XP), Titles (level in name).

**Balance note (overseer):** its core reward is skill and stat points you spend to raise skills
directly. That replaces UO's use-based skill gain, which is the heart of "stubborn skill grinder".
Whatever a level gives here should sit beside skill gain, not replace it.

Check first:
1. Level System Extreme's source: its XP curve, what a level grants, and its level-up and title
   gumps, as design reference (license first).
2. How it gates equipment, and whether a customizations hook exists in pinned for the same
   (`OnEquip` / `CanEquip`) without core edits.
3. How XP and levels relate to AP and Renown: replace, sit beside, or feed each other.

Answered 2026-09-30 (Chase): **what a level gives**
- **Titles.**
- **Follower slots.**
- **Access to gear, vendors and areas** (level requirements on our own gear, level-gated vendors,
  level gates to areas).
- **Small perks.**
- **Level-gated League shop tiers** (F-13: AP and level both gate tiers; Renown buys).
- **Not** skill or stat points: skills stay earned by use (overseer's reading of Chase's list; the
  "stubborn skill grinder" core is untouched).
- **More ways to raise the level cap** (Chase). Overseer suggests cultivation-style
  **breakthroughs**: the cap rises in steps (for example 50, 75, 100, 125, 150...), each opened by a
  trial rather than bought: a boss, a quest, an AP threshold, a set of achievements, or a
  Raise-Max-Level scroll as a rare drop (Level System Extreme has one). A player at the cap keeps
  banking XP toward the next level, so nothing is wasted while they work on the breakthrough.

Answered 2026-09-30 (Chase): **the breakthrough is a reset.** Level goes back to 1 and the max level
advances: the shard's time loop as a prestige system. **First cap 50**, unless resets argue for lower.
Overseer:
- Keep 50. Each reset raises the cap by a step (for example 50, 75, 100, 125, 150); an optional
  "raise max level" scroll can still exist as a rare find.
- A reset is chosen by the player at the cap, never forced, with a confirm step.
- Make later loops faster (for example bonus XP per past reset), so repeating 1 to 50 feels like
  progress, not punishment.
- What resets and what stays needs deciding (see below).

Answered 2026-09-30 (Chase):
- **Everything stays through a reset** (titles, perks, follower slots, AP, Renown, shop tiers), but
  **gear above the player's current level can no longer be used** until they level back up.
- **A reset needs rewards of its own, possibly tiered.** Chase's candidates: stat cap, skill cap,
  stat points, skill points, follower slots.

Overseer proposal for the reset rewards (a tier per loop, to react to):
- **Skill cap is the headline reward.** It fits the vision exactly: one character that can do
  anything, over and over. Each loop raises the total skill cap (for example +50 per loop from
  700), so a looped character can hold more skills, but **still has to grind them by use**.
- **Stat cap** rises by a smaller step (for example +5 per loop, from 225).
- **Follower slots** at some loops (for example loops 2 and 4).
- **No free skill or stat points**: points would skip the grind, and the cap raise already gives
  the grind somewhere to go. (Chase to confirm.)
- A loop counter in the title ("Looped x3") and a loop achievement per tier.
- Example ladder: loop 1: cap 75, +50 skill cap, +5 stat cap. Loop 2: cap 100, +50, +5, +1
  follower slot. Loop 3: cap 125, +50, +5. Loop 4: cap 150, +50, +5, +1 follower slot, a unique
  title. Numbers are placeholders.

Chase's idea (2026-09-30, "maybe"): **each skill is capped at the player's level cap.** Overseer's
reading: the **max level** (which only rises through loops), not the current level, so a reset never
lowers skills. With the ladder above: loop 0 cap 50 means no skill above 50.0; loop 2 cap 100 is the
first chance to GM a skill.
Overseer notes:
- It ties the two systems into one number, and makes the loop the gate to mastery. Strong fit for
  "stubborn skill grinder with time loops".
- **Map it, do not copy it past 120**: per-skill cap = min(level cap, 120). OSI's per-skill ceiling
  is 120 (power scrolls), and plenty of pinned formulas assume it. Loops beyond cap 120 raise the
  **total** skill cap instead.
- Power scrolls then only work up to the current level cap (a 120 scroll needs level cap 120).
- Cost: a new player cannot reach GM in anything until their second loop. Needs the first loops to
  be quick enough (F-12 later-loop XP bonus, and a first cap reached in days, not weeks), or new
  players will bounce.
- A large deviation from OSI; register it and explain it on the wiki's first page.
- Check first: how pinned stores per-skill caps (`Skill.Cap`, default 100) and whether setting it per
  player needs a core edit.

**Decided 2026-09-30 (Chase):**
- **Individual skill cap = the player's level cap (max level).** At cap 50 no skill goes above 50.0;
  looping is the only way to raise it. This **forces an early loop** by design.
- **Reset rewards as proposed**, with the individual skill cap taking the place of the "+50 total
  skill cap per loop" line: stat cap rises per loop, follower slots at some loops, loop counter in
  the title and a loop achievement per tier, **no free skill or stat points**.

**Decided 2026-09-30 (Chase):**
- **Total skill cap: unlimited.** (One character that can do everything.)
- **No 120 ceiling.** Individual skill cap follows the max level all the way up, and the **max level
  itself lands somewhere between 500 and 1000** (to settle).
- **Past OSI's 120, progression needs power scrolls, or a rebranded version of them**, for the later
  loops.
- **First, find out how skills behave past 120** in pinned and what has to be added so going
  further works.

Overseer: this is the shard's biggest design commitment, so it gets its own research task before
anything is built (a read-only cc prompt):
1. **Storage and client:** how pinned stores skill values and caps (`Skill.Base`, `Skill.Cap`,
   `SkillsCap`), their numeric limits (tenths of a point in an unsigned 16-bit value would allow up
   to 6,553.5), what the skill packets send, and whether TazUO shows values over 120 correctly.
2. **Every skill's formulas past 120**, sorted into: scales sensibly; clamps harmlessly at 100 or
   120 (no effect past it); **breaks** (chances over 100 percent, divide-by-zero, negative values,
   overflow, immunity: e.g. Resisting Spells reducing damage to nothing, Parry always blocking,
   Hiding never failing, damage bonuses running away, crafting exceptional chance past certain).
   One table per skill with file:line.
3. **Gains past 120:** how pinned's gain chance behaves as skill rises (it may stall or go
   negative), since it was tuned for 0 to 120.
4. **Power scrolls:** how pinned's power scrolls and stat scrolls are defined, what caps them at
   120, and what a "rebranded" line of scrolls for higher tiers would touch.
5. **Creatures:** whether creature stats and F-14 levels need to scale to challenge a 500-skill
   character, or whether the level range is mostly prestige.
Output: a report and a recommendation per skill (let it scale, soft-cap it with diminishing
returns, or give it new effects past 120), plus a first XP curve for a 500 to 1000 level range.

**Prior work found 2026-09-30 (read before designing further):**
- **Skill caps are already raised today**: `server\customizations\ClusterFSkillCaps.cs` sets every
  skill's cap to **300** and the total to unlimited (config `clusterf.skillCaps.individualCap` 300,
  `totalCap` 0), re-applied to every player at login and world load (`Apply`, `:106-123`).
  `ClusterFStatCaps.cs`: individual stat cap 500, total 1500. So "skills past 120" is live now.
- **Content already uses 0-300**: `roadmap.md:455-470` (mining progression over 0-300, extended ore
  chain), `ClusterFSmithBODSystem.cs:374` ("extended skill can exceed 300").
- **Phase 4F, locked 2026-05-20** (`design\phases\phase_4_smiths_guild_extended_crafting.md:746`):
  individual cap 300 -> 500 through additive scrolls (+5 / +10 / +15 / +20, 200 points of scrolls
  per skill), from champion spawns and guild reward vendors; achievements at 350/400/450/500 with
  titles already sketched; claims "natural gain slowdown past 200 is sufficient". Not built.
- **Roadmap "Champion Spawn and Mastery Rewrite"** (`roadmap.md:915-930`): replace or supplement the
  105-120 power scrolls with additive "Legacy Scrolls / Mastery Scrolls / Ascendant Scrolls".
- **Roadmap "Legacy Awakening"** (`roadmap.md:333-362`): the shard's long-term progression concept,
  cultivation-inspired, with stages Soul Awakening, Foundation Tempering, Inner Core, Spirit
  Ascension, Legacy Embodiment. It says: **"Do not make it a mandatory treadmill or infinite stat
  reset loop"** and **"Avoid mandatory resets ... If resets exist, they should be optional and
  preserve history."**
- **Mythik already reviewed**: `design\systems\achievement_expansion_mythik_integration.md` (323
  lines) reached the same conclusion as this entry: take typed categories, do not replace
  ClusterFAchievements.
- `design\systems\league_of_extraordinary_citizens.md`: the League's full design (Renown "is not
  intended to function as gold", citizen ranks). Read before F-13.

**Settled 2026-09-30 (Chase):**
- **Mandatory resets, yes.** The new cap rule needs them; this **replaces the roadmap's "avoid
  mandatory resets" line** (`roadmap.md:339` and `:360`), which should be updated to match.
- **Content behind loops is fine** (0-300 content waits for the loops that reach it).
- **Max level 1000, and so individual skill cap up to 1000.**

**Conflicts to settle with Chase** (1, 2 settled above; 3 and 4 open):
1. The early forced loop (skills capped at the level cap, first cap 50) contradicts the roadmap's
   "avoid mandatory resets" line. Chase's new decision would replace it; confirm.
2. Today every skill can reach 300. Under the new rule a first-loop character stops at 50. Content
   tuned for 0-300 (mining tiers, smith BODs) would sit behind loops.
3. Phase 4F's scrolls (300 -> 500) and the loop caps (50 ... 500-1000) are two ladders for the same
   number; they need to become one (for example: loops raise the cap, scrolls fill the last stretch
   of each loop's cap, or scrolls are the loop's gate).
4. The Legacy Awakening stage names may be the loop names.

**Conflict 3 settled 2026-09-30 (Chase): loops set the cap; scrolls are needed to loop higher.**
Phase 4F's additive cap scrolls are replaced. A scroll (Legacy Scroll or similar) is the key to start
the next loop past some point. **Scroll merging**: lower scrolls can be combined into higher scrolls
later on. `D:\ShatteredLegacy\roadmap.md` updated to match (principles, Extended Resources, Champion
Spawn and Mastery Rewrite, Legacy Awakening).

Answered 2026-09-30 (Chase):
- ~~Scrolls required from past 200~~ **Changed: scrolls required from past 100** (the loop that raises
  the cap above 100), with the lowest tier **much easier to find than champion spawns**: "akin to
  paragons or worse" (Chase, 2026-09-30).
- **OSI's 105/110/115/120 power scrolls fold into the new line**; no scroll gates at 105-120.
- **Merging is a League service**, gated by League rank and paid in Renown.
- Chase asked for a list of loop names and tiers (overseer draft below).

Overseer draft, loop ladder (to react to; numbers placeholders):

| Loop | Cap (level and each skill) | Realm and stage | Key to enter |
|---|---|---|---|
| 0 | 50 | Unawakened | none (start) |
| 1 | 100 | Soul Awakening I | none |
| 2 | 150 | Soul Awakening II | Awakening Scroll |
| 3 | 200 | Soul Awakening III | Awakening Scroll |
| 4 | 250 | Foundation Tempering I | Tempering Scroll |
| 5 | 300 | Foundation Tempering II | Tempering Scroll |
| 6 | 350 | Foundation Tempering III | Tempering Scroll |
| 7 | 400 | Inner Core I | Core Scroll |
| 8 | 500 | Inner Core II | Core Scroll |
| 9 | 600 | Inner Core III | Core Scroll |
| 10 | 700 | Spirit Ascension I | Ascension Scroll |
| 11 | 800 | Spirit Ascension II | Ascension Scroll |
| 12 | 900 | Spirit Ascension III | Ascension Scroll |
| 13 | 1000 | Legacy Embodiment | Embodiment Scroll |

Realm names are the roadmap's Legacy Awakening stages. Steps of 50 up to 400, then 100, so the early
loops come quickly and the late ones stretch. 13 loops; scrolls gate 12 of them (all but loop 1).

Scroll line (draft): Awakening, Tempering, Core, Ascension, Embodiment (could be called "Legacy
Scroll of Tempering" and so on, or "Sigils").
Sources (draft):
- **Awakening Scrolls, the common tier**: **paragons** drop them at a good rate (pinned already has
  paragons: the gold-hued, stronger versions of ordinary creatures, with their own loot rules; check
  `Paragon.cs`), plus a small chance from any creature at or above the player's level (F-14), League
  contracts, and treasure chests. Easy enough that a steady player finds the two they need for loops
  2 and 3 without hunting for them.
- **Tempering and Core**: champion spawns (replacing old power scroll drops), bosses, high-level
  paragons, and merging.
- **Ascension and Embodiment**: mostly merging, plus rare drops from the hardest content.

Merging at the League (draft): 3 of one tier into 1 of the next, for Renown, needing a League rank
per target tier, using the League's existing ore-named citizen ranks
(`design\systems\league_of_extraordinary_citizens.md`): Core needs Agapite Citizen, Ascension
needs Platinum Citizen, Embodiment needs Mythril Citizen, and Tempering (from Awakening) needs
Copper Citizen. Chase (2026-09-30): yes, and **League ranks must sync with our custom metals**.
Checked 2026-09-30: the League design's 17 citizen ranks are already the shard's full metal chain,
in order (Iron, Dull Copper, Shadow Iron, Copper, Bronze, Gold, Agapite, Verite, Valorite, then our
customs Platinum, Toxic, Blaze, Frost, Obsidian, Mythril, Adamantium, Celestial), matching
`server\customizations\ResourceInfo.cs:9-27` and `design\systems\extended_resources.md:27-50`.
But **only three statuses are built** (`ClusterFLeagueSystem.cs:51-55`: Unregistered, Registered
Citizen, Recognized Citizen); the metal ranks are design only. Building them (and the rule for
earning each) is part of this feature or F-13. Keep them generated from the metal list so a future
metal gets a rank automatically.
Sources noted: pinned paragons are `Mobiles/Special/Paragon.cs` and `Items/Containers/ParagonChest.cs`.

Open questions:
- React to the ladder, names and merge rule above.
- Conflict 4 (loop names) answered by the draft if accepted.
- Power scrolls kept as they are for 105 to 120 (OSI), with a new, rebranded line beyond 120? Or
  rebrand the whole line?
- **What does a level give?** (answered above; kept for the record of options) Stat or skill points would change UO's caps (skill cap 700, stat
  cap), which is a big balance decision. Alternatives: titles and cosmetics only, access to
  content or areas, higher caps in steps (a cultivation-style breakthrough), or perks.
- Per character or per account? (Achievements are per account today.)
- Pet levels in the first version, or later?
- Does the "time loop" / prestige idea reset levels (prestige resets for a permanent bonus)?

### F-13: Achievement reward shop and AP-gated titles (added 2026-09-30)

**Ours.** Goes with F-12 (levels) but can ship without it.

What Chase wants:
- Achievement points **required** for titles and rewards.
- An **achievement reward shop**.

What exists (read 2026-09-30, `ClusterFAccountData.cs:5-20`): the design already has two numbers.
- **AP (Achievement Points): "permanent prestige score, not spendable."** Earned per achievement
  (`ClusterFAchievements.cs:837`). Only used today for two League achievements at 100 and 500 AP
  (`:1038-1039`) and shown in the achievements gump (`:1628`).
- **Renown: "spendable achievement currency."** Earned with each achievement, and
  `SpendRenown` exists (`:460`), but **nothing spends it yet.** The shop is what it was made for.

Suggested (overseer):
- **AP unlocks, Renown buys.** AP is a lifetime score, so thresholds on it never go backwards: a
  title or a shop tier opens at 100, 250, 500... AP and stays open. Renown is what the shop charges,
  so buying never lowers a player's standing.
- **Titles**: earned by AP thresholds and by specific achievements; the player picks one to show
  under their name. Could also be bought in the shop, gated by AP.
- **Shop tiers by AP**: each item has a Renown price and an AP requirement. Locked items are shown
  greyed with "Requires 500 AP", so players see what is coming.
- One store window, shaped like the Clean Up Britannia store (F-3), so the shard's stores feel alike.
- Content in the System's voice (Dungeon Crawler Carl-style loot boxes would fit: a box whose tier
  depends on AP, opened with a snarky line).
- Prices set with the same care as F-3: nothing that breaks OSI balance (no power scrolls or
  artifacts sold outright). Cosmetics, titles, conveniences, house decor, hues.

Check first:
1. How much Renown and AP each achievement gives today, and the totals a player could reach, so
   prices and thresholds are set against real numbers.
2. How titles can be shown in pinned (the name suffix / title property on `PlayerMobile`) without
   a core edit.
3. Where the shop lives: an NPC in New Haven, the achievements gump, or both.

Answered 2026-09-30 (Chase): **AP unlocks, Renown buys.** AP thresholds gate titles and shop tiers
and never go backwards; Renown is the price.

- **The shop lives with the League, which is the shard's adventurers' guild** (Chase, 2026-09-30):
  the League Registrar opens it
  (`ClusterFLeagueSystem.cs`, `LeagueRegistrarGump`). Fits: the achievement system already has a
  League category, and the 100 and 500 AP achievements are League achievements. Overseer suggests a
  button in the achievements gump that opens the same store too.

Read 2026-09-30 (`ClusterFAchievements.cs`): 74 achievements; a player who earns all of them has
**2,505 AP and 6,505 Renown**. Most pay 10 to 100 Renown; Skills is about half of it (3,280).

Draft list (overseer, 2026-09-30), for Chase to react to. AP opens the tier and never closes it;
Renown is the price. Totals about 4,400 Renown, so a completionist can buy most of it, not all.

| AP needed | Item | Renown | Kind |
|---|---|---|---|
| 0 | Title: "Registered Adventurer" | 25 | title |
| 0 | League tabard, League hue, cannot be dyed | 50 | cosmetic |
| 0 | System's Loot Box, Bronze | 40 | loot box |
| 100 | Hair restyling deed (pinned `HairRestylingDeed`) | 75 | convenience |
| 100 | League rune: blessed recall rune marked to the League Registrar | 60 | convenience |
| 250 | League banner, wall decor | 150 | decor |
| 250 | League cloak in a hue sold nowhere else | 200 | cosmetic |
| 250 | System's Loot Box, Silver | 150 | loot box |
| 500 | Achievement trophy: statuette showing the owner's name and AP | 250 | decor |
| 500 | League-hue pigment, one use (like the Clean Up pigments) | 300 | cosmetic |
| 500 | Title: "Veteran of the League" | 200 | title |
| 1000 | System's Loot Box, Gold | 400 | loot box |
| 1750 | League regalia: robe, cloak and sandals in a unique hue | 1000 | cosmetic |
| 1750 | Title: "the System's Favorite" | 500 | title |

Guardrails: no item properties, power scrolls, artifacts, bless deeds, or skill and stat items.
Loot boxes draw only from the kinds above, with a line in the System's voice.

Account age (veteran) rewards:
- Answered 2026-09-30 (Chase): **include account age (veteran) rewards, with a short account age.**
  Found: pinned already has OSI's veteran reward system **on**, one level per **30 days**
  (`Engines/Veteran Rewards/RewardSystem.cs:559-564`; `vetRewards.rewardInterval` in `modernuo.json`).
  It gives ethereal mounts, monster statues, cloaks and robes, special dye tubs and house add-ons. It
  also raises the skill cap by 5 per level up to 720 and gives +5 stat cap once at half a level
  (`RewardSystem.cs:576-594`, `vetRewards.skillCapRewards: True`). So the ethereal mount comes off the
  League list (the veteran rewards give it), and the shop can show the veteran rewards beside the
  League items.
- Reward level N needs N x 30 days of real account age (Chase, 2026-09-30); that is pinned's current
  setting, no change.
- **SUPERSEDED 2026-10-01 (Chase): the veteran reward now raises the total stat cap by 50.** Base total stat cap is 325 and the veteran reward takes it to 375, which is 125 in each stat; the per-stat 125 never moves. This is the stat cap mechanism, and a deviation from OSI's +5 for the register. See `notes\f12-levels-loops-caps.md`. The 2026-09-30 decision below is kept for the reasoning only.
- ~~Decided 2026-09-30 (Chase): no skill cap or stat cap bonuses.~~ F-12 already makes the total skill
  cap unlimited with each skill capped by max level, and the stat cap is a loop reward, so vet cap
  bonuses would do nothing or compete with loops. **Instead, +1% XP per reward level, up to +12% at
  one year**, applied to F-12 XP. Until F-12 ships, vet levels give only their reward items.
- Turning the bonuses off: set `vetRewards.skillCapRewards` to False, and stop the one-time +5 stat
  cap through a hook, not a pinned edit. Check first what existing characters already got (the stat
  bonus sets `HasStatReward`) and whether any need putting back.

Answered 2026-09-30 (Chase): **the draft list is approved as a starter**; prices get tuned in play
testing. Loot boxes draw only from the kinds on the list (overseer default; Chase did not ask for a
separate pool). Level gates from F-12 get added when levels exist.

Open questions: none. Ready to batch (the shop at the League Registrar, with a button from the
achievements gump).

### F-14: Creature levels, so players can tell what they can fight (added 2026-09-30)

**Ours.** Goes with F-12 (player levels). OSI shows no creature levels.

What Chase wants:
- Every monster and NPC gets a level, so a player can judge whether they can take it on.

Bases found (read 2026-09-30):
- **OSI's own difficulty formula, already in pinned:** `BaseInstrument.GetBaseDifficulty`
  (`Items/Skill Items/Musical Instruments/BaseInstrument.cs:250`), the Bard difficulty used by
  Provocation, Peacemaking and Discordance. It scores any creature from its stats: max hits,
  stamina and mana, total skills, then +100 each for magery, fire breath, poison immunity, +20 per
  poison level, with a soft cap and a paragon bonus. **Works on every creature automatically,
  including our custom ones and anything added later.** Recommended base.
- **Fame**: every OSI creature has a Fame value (used for titles and loot); a second opinion.
- **Level System Extreme's XP tiers** (`ExpTables.cs`): about 280 creature types hand-sorted into
  ten tiers (38 no-XP, then 26 / 68 / 4 / 46 / 34 / 17 / 10 / 21 / 11 / 5 from lowest to highest).
  Useful as a cross-check, not complete.

Suggested (overseer):
- **Creature level = a mapping of Bard difficulty** onto the player level range (F-12), with a
  **hand override** for bosses, champions and story NPCs. Computed, so it never goes stale.
- **"Con" colors** (EverQuest and Dungeon Crawler Carl style), relative to the player's level: grey
  (trivial), green, blue, yellow (even), orange, red, skull (deadly). Shown in the name or the
  tooltip, e.g. "a troll [Lv 34]".
- XP from kills (F-12) scales from the same level, so both systems read one number.
- A report command for staff listing every creature with its computed level, to review outliers.

Check first:
1. Run `GetBaseDifficulty` over every creature type in pinned plus customizations (a test or a
   report command) and look at the spread: does it rank them sensibly (a rat below a dragon below
   an ancient wyrm)? Where does it go wrong (creatures whose danger is in special abilities the
   formula ignores)?
2. How to show a level in pinned without a core edit: name suffix, the property list (tooltip),
   or both; how name hue interacts with notoriety colors (which must not be broken).

Answered 2026-09-30 (Chase): **color** (con colors relative to the player's level), and **NPCs
too**, not only things that fight.

Chase's idea: **an Identify skill**, or **repurpose Item Identification**, to learn more than the
color. Overseer:
- Suggested split: the **con color is free** for everyone (a glance at the name). The **exact level
  and details** (level number, notable abilities) need a skill.
- **Repurposing Item Identification** is a deviation from OSI (register it). Since AOS, item
  properties show on hover, so the skill does very little today, which makes it the cheapest skill
  to give a new job without taking anything away. It could identify creatures (level, abilities)
  and items (level requirements, loop requirements).
- Alternative without a deviation: add the level to what **Anatomy, Animal Lore and Evaluating
  Intelligence** already show when used on a creature. Less flavor, no rule change.
- Check first: what Item Identification does in pinned today (cite), and what uses it (Imbuing,
  quests, anything else), before taking it over.

Answered 2026-09-30 (Chase): **repurpose Item Identification** (a deviation; register it when
batched). Two more ideas from Chase:
- **Rename it after a quest.** Overseer: the name in the skills window comes from the client's files,
  not the server, so it cannot differ from player to player. Options: (a) rename it for everyone
  through the updater (for example "Identification" or "Appraisal"), and a quest unlocks the creature
  half; (b) keep the client's name and mark the quest another way (a title, or a line in the skill's
  gump). Check first: where TazUO reads skill names (`skills.mul` or cliloc) and whether our updater
  (cc-P5) can ship that change.
- **What it shows grows with skill**, from a line like the existing lore skills to a stat card.
  Proposed steps:
  - 0 to 29.9: the con color, plus one vague line ("It looks like it could hurt you.").
  - 30 to 59.9: the level number and a line in the style of Anatomy and Animal Lore.
  - 60 to 89.9: adds hits, main stats and resistances as short text.
  - 90 and up: a stat card gump: level, hits, stats, resists, damage types, special abilities, and
    whether it is a paragon or a boss.
  On items it keeps its current use and adds level and loop requirements (F-12) from 30.

Answered 2026-09-30 (Chase): **(a), rename it for everyone** through the updater. **Every creature
shows its con color against the player's level**, whatever its level and whatever the player's skill;
the skill adds detail on top of the color.

Answered 2026-09-30 (Chase): the new name is **Appraisal**.

Answered 2026-09-30 (Chase): **skill steps approved** as written.

Open questions: none. Ready to batch (needs F-12 levels for the level number; the con color and
the stat card can come first if levels are computed from Bard difficulty).

### F-15: Version number and patch notes in the MOTD, linked to the website (added 2026-09-30)

**Ours.** Test shard only (the only world that matters).

What Chase wants:
- A **version** for the test server.
- A **MOTD** on login showing what was **updated, fixed and added**, with **expanded notes on the
  website**.

What exists (read 2026-09-30):
- **The MOTD system is built**: `server\customizations\ClusterFBulletin.cs` (449 lines). Bulletins
  with categories (critical, dispatch, guild, event, personal), an unread gump on login (tracked by
  `LastSeenBulletinId` per account), admin commands `[ClusterFBulletin add/list/remove/load`, and a
  file source `Configuration/bulletins.txt` (one line per bulletin, `category|message`).
- **Pinned can open a web page from the game**: `Mobile.LaunchBrowser(url)`
  (`Server/Mobiles/Mobile.cs:7812`), so a gump button can open the full notes.
- **The website is live on Haven** (`shatteredlegacyuo.com`, `wiki.`), deployed by hand with
  `D:\UO\haven-migration\Deploy-Website.ps1`; `status.json` (P6) is already published there.
- **No version exists** anywhere today.

Suggested (overseer):
- **One source of truth: `D:\ShatteredLegacy\CHANGELOG.md`**, newest first, one section per
  version: Added, Changed, Fixed, each a one-line player-facing item, optionally with a link anchor.
  The version lives in its heading (and a one-line `VERSION` file the build reads).
- ~~Version scheme `0.MINOR.PATCH`~~ superseded: date versions (see answers below).
- **In game**: on first login after an update, the bulletin gump shows "Shattered Legacy 2026.10.02" and
  the short list, with a **"Full notes" button** that opens the version's section of the wiki
  patch-notes page via `LaunchBrowser`. Generated from the
  changelog at build or load time, so nobody types it twice. A `[version` player command shows the
  current version and reopens the notes.
- **Wiki**: the patch-notes page rendered from the same `CHANGELOG.md`; the version also goes in
  `status.json`, so the website's "Online now" widget can show it.
- **Workflow**: at each batch, the overseer drafts the player-facing notes from the cc notes and the
  bug list, Chase approves, it goes in with the commit. Internal detail stays out of player notes.

Check first:
1. How `bulletins.txt` gets into the image (and whether `load` must be run by hand), so a new version
   posts itself.
2. Whether TazUO honors the launch-browser packet (and asks the player first).
3. How the website is built today (static page or generated), to render the changelog there.

Answered 2026-09-30 (Chase):
- **Date versions**, e.g. `2026.09.30`. Overseer: a second update the same day gets a suffix,
  `2026.09.30.2`.
- **Expanded notes on the wiki**, not the website: a patch-notes page on `wiki.shatteredlegacyuo.com`,
  one section per version. Check how DokuWiki forms heading anchors (dots may be dropped), and
  generate the MOTD link to match.
- **Start fresh at the next batch after this is implemented.** No baseline entry for earlier work.

Open questions: none.

### F-16: Jacob's Pickaxe restoration cheaper at the lower tiers (added 2026-09-30)

**Ours.** Tiers and restoration are our Miners' Compact system; OSI's Jacob's Pickaxe has neither.

What Chase wants:
- Restoring (fixing) an exhausted Jacob's Pickaxe should cost less at the lower tiers.

Today (read 2026-09-30, code repo 29cb496): every tier's restoration is about 20% of that tier's
upgrade cost (`MinersCompactLiaisonGump.cs:41-69`).

| Tier | Uses | Restoration today |
|---|---|---|
| T1 Jacob's Pickaxe | 150 (`patches/JacobsPickaxe.cs:37`) | 5 vouchers, 100 iron, 2,000 gp |
| T2 Reinforced | 400 | 10 vouchers, 200 iron, 40 dull copper, 5,000 gp |
| T3 Prospector | 600 | 40 vouchers, 300 iron, 100 agapite, 10,000 gp |
| T4 Deepdelver | 800 | 70 vouchers, 400 iron, 100 valorite, 30,000 gp |
| T5 Worldbreaker | 1,200 | 100 vouchers, 600 iron, 200 valorite, 40 adamantium, 60,000 gp |

The problem (overseer): a new player starts with no gold (cc-P15), and the first Compact work order
(50 iron) pays 5 vouchers and 75 gp. So T1 costs about 27 work orders' worth of gold for 150 uses,
while a plain pickaxe from a vendor is a few dozen gold. Players will throw T1 away instead.

Proposed (overseer), for Chase to react to:
- **T1: 1 voucher, 25 iron, 100 gp.** About what the same uses cost in plain pickaxes, so fixing is
  always the better deal but never free.
- **T2: 4 vouchers, 100 iron, 15 dull copper, 1,000 gp.**
- **T3 to T5 unchanged.** By then a player is a Surveyor or higher and earning at that scale.

Check first: that the Liaison gump reads the constants above and nothing else prices restoration (the
admin tools' bypass, the Hammer of Hephaestus restore at `HammerOfHephaestus.cs:1003-1004` is a
separate item); a test that each tier charges its new price and refuses with one short.

Answered 2026-09-30 (Chase): **T1 and T2 prices approved as proposed**; T3 to T5 unchanged.

Open questions: none. Ready to batch.

### F-17: Fill a BOD from the backpack (added 2026-09-30)

**Ported, if OSI's version fits.** Later OSI (the bulk order revamp, after pinned's era) added a
second button to the BOD gump, "Combine this deed with contained items": target a container and every
matching item inside goes into the deed. **Confirmed 2026-09-30** on the uo.com wiki (Bulk Orders):
"if your crafted items are contained in a pack within your back pack you can choose the option
'Combine this deed with contained items'", a targeting cursor that combines every item in the
targeted pack; the one-item option is "Combine this deed with the item requested".

What Chase wants:
- A **fill from backpack** button on **every BOD**.

Found 2026-09-30:
- Pinned has only the one-item combine: `SmallBODGump.cs:81` and `LargeBODGump.cs:102` call
  `BeginCombine`, which targets one item at a time (`SmallBOD.cs:117`, `LargeBOD.cs:94` `EndCombine`).
- "Every BOD" today means the smith and tailor deeds, small and large (pinned has no other crafts'
  BODs). We patch `LargeSmithBOD` already (`patches/LargeSmithBOD.cs`).
- Our guild work orders (`ClusterFWorkOrderSystem.cs:216-248`, Artificer orders) already take what
  they need straight from the backpack on turn-in, so they need nothing.

Suggested (overseer):
- **Port OSI's button**: target a container; targeting your own backpack fills from the backpack.
  For large BODs it takes the filled small deeds in the container. The fill stops when the deed is
  full and says how many it took.
- Each item goes through the same checks as the one-item combine (`EndCombine`): type, exceptional,
  material, not in someone else's container. Items that fail stay where they are.
- If Chase prefers one click with no target, that is a small deviation from OSI (register it):
  the button reads "Fill from backpack" and uses the backpack directly.
- Tests: a small deed fills from a mixed pack and leaves the wrong material behind; a deed stops at
  its amount; a large deed takes its small deeds from a bag; nothing outside the targeted container
  is touched.

Answered 2026-09-30 (Chase): **stick with OSI.** ModernUO does not have it, so it is folded in.
**Port source found:** `D:\UO\ServUO-pub57\Scripts\Services\BulkOrders\SmallBODs\SmallBODGump.cs:102-103`
(button, cliloc 1157304 "Combine this deed with contained items") and `:168-176` (case 4: target a
container, run each item in it through the combine); the large deed's version is in
`LargeBODs\LargeBODGump.cs`. Port it onto pinned's gumps through partials or patches.

Open questions: none. Ready to batch.

### F-18: BODs as a way to grow skill, not just easy items (added 2026-09-30)

**Ours.** Smith BODs are already ours (guild-only, Seals instead of OSI rewards); this goes further
from OSI, whose BODs pick any item you can make and give no skill on turn-in.

What Chase wants:
- BODs should **raise skill** and be **a way to grow at low skill**, not orders for easy things.

Found 2026-09-30 (code repo 29cb496):
- `ClusterFSmithBODSystem.cs` already moved smith BODs to the Blacksmith Guildmaster (3 small, 1 large
  at a time, no cooldown) and **turn-in already gives a skill check**: 1 per small deed, 2 per large
  (3 from gold up), in a skill window by material (`GetSkillRange`, `:343`; plain iron 0 to 55).
- **The item choice is still OSI's** (pinned `SmallSmithBOD.CreateRandomFor`, `:75-170`): any item
  with a success chance above 0, picked at random. At low skill that is mostly items the player
  already makes every time, which give no gain while crafting them. That is the "easy things" problem.
- **Tailor BODs are still vanilla**: no guild system, no turn-in skill check.
- Pinned has BODs for smithing and tailoring only.

Suggested (overseer):
- **Pick items the player can still learn from.** When a BOD is made, prefer items whose crafting
  skill range contains the player's skill (that is where crafting gains happen), weighted toward the
  upper half of that range. Fall back to OSI's pick only when none fits. Each order then means
  real practice: making 15 of them is where the growth comes from.
- **Turn-in check scales with the size of the order**: 1 check per 5 items (2 / 3 / 4 for 10 / 15 /
  20), large deeds the sum of their parts. Keeps the existing material windows.
- **Low-skill track**: under 50 skill, orders are plain material, never exceptional, and smaller
  (10 items), so a new crafter can finish one in a sitting.
- **Tailoring joins the same system** under the Tailors' Circle, the way smithing moved to the
  Society of Smiths.
- Tests: a 30-skill smith never gets an order for an item at 100% success when a gain-range item
  exists; turn-in check counts follow the amount; tailor deeds get the same rules.

Check first: how the craft system exposes each item's skill range (`CraftItem` skill min and max) and
that "gain range" matches how pinned's crafting gain works.

Answered 2026-09-30 (Chase): **tailoring in the same batch as smithing.** **Other crafts: yes**,
as their own entry (F-20).

Answered 2026-09-30 (Chase): **proposal approved** (gain-range items, 1 check per 5 items, low-skill
track under 50).

Open questions: none. Ready to batch (smithing and tailoring together).

### F-19: Banks hold far more items (added 2026-09-30)

**Ours** (a deviation from OSI's 125-item bank; register it).

What Chase wants:
- Banks able to hold **way more items**.

Found 2026-09-30 (pinned):
- The bank has **no weight limit** (`Server/Items/Containers.cs:23`, `DefaultMaxWeight => 0`) and a
  **125-item limit** from `Container.GlobalMaxItems` (`Server/Items/Container.cs:154-159`), which
  counts items inside bags too, so bags do not help.
- `MaxItems` can be set per container and is saved (`Container.cs:88-103`), so a bank can be given its
  own number without touching any other container.
- Pinned already has commodity deeds, which turn a stack into one item; they stay useful.

Suggested (overseer):
- **Base bank size 1,000 items**, set on the bank box only (a partial or patch on `BankBox`
  overriding `DefaultMaxItems`), never by raising `GlobalMaxItems`, which would change every
  container in the game.
- **It grows**, so there is something to earn: +100 per League rank, or bank upgrades in the League
  shop (F-13), or +50 per account age reward level. One of these, not all.
- Watch the client: opening a bank sends every item in it. A thousand is fine; tens of thousands would
  make the bank slow to open. Test opening a full bank in TazUO before going higher.
- Fits F-11 (guild upgrades draw from the bank), which makes the bank the shard's storehouse.
- **Test Center note** (Chase, 2026-09-30: after `[TCFill` he cannot add items by hand). `[TCFill`
  (`TestCenter/TestCenterFillCommand.cs`) runs pinned's `TestCenter.FillBankbox`
  (`Special Systems/Engines/TestCenter.cs:549`, about 255 drop calls plus loops, so several hundred
  items) and our Test Kit, and puts them in with `DropItem`, which skips the 125 limit. The bank ends
  far over 125, so every hand drop is refused. Each use adds again without clearing. F-19 fixes it for
  testing; until then, empty some of the fill to make room.
- Tests: a bank takes item 1,000 and refuses 1,001 with OSI's message; a backpack and a house
  container keep 125.

Answered 2026-09-30 (Chase): **base 1,000 items**, **+100 per League rank**. Found 2026-09-30: League
ranks do not exist yet (`ClusterFLeagueSystem.cs:51-66` has only citizen status; F-12's metal ranks
are undecided), so cc-P22 builds the base and leaves the rank bonus as a method returning 0.

Open questions: none. Ready to batch.

### F-20: BODs for the other crafts (added 2026-09-30)

**Ported.** OSI has bulk orders for eight crafts (uo.com wiki, Bulk Orders): Alchemy, Blacksmithy,
Bowcraft (Fletching), Carpentry, Cooking, Inscription, Tailoring, Tinkering. Pinned has only
Blacksmithy and Tailoring.

What Chase wants (2026-09-30): BODs for the other crafts too.

Suggested (overseer):
- Port OSI's six missing crafts: which items each asks for, materials, amounts, from the wiki and the
  later ServUO code (check `D:\UO\ServUO-pub57` and `ServUO-ShatteredLegacy` for an existing port
  before writing new).
- Run them through our guild system and F-18's rules, not OSI's NPC rewards: each guild issues its
  craft's orders and pays in its own currency. Likely homes: Carpentry and Bowcraft with the Foresters'
  Union, Tinkering with the Tinkers' Union, Inscription and Alchemy with the Arcane Society, Cooking
  with the Merchants' Exchange. Chase to confirm.
- F-17's "contained items" button covers these too.
- Large job; one or two crafts per batch, Carpentry and Tinkering first (most players craft them).

Check first: ServUO's later BOD code (the 2016 revamp) and how much of it fits pinned's
`SmallBOD` / `LargeBOD` base; reward books (`Books`) for the new crafts.

**Port source found 2026-09-30:** `D:\UO\ServUO-pub57\Scripts\Services\BulkOrders` has all eight
crafts, small and large (`SmallCarpentryBOD.cs`, `SmallTinkerBOD.cs`, `SmallFletchingBOD.cs`,
`SmallAlchemyBOD.cs`, `SmallInscriptionBOD.cs`, `SmallCookingBOD.cs` and the large ones), plus
`BulkOrderSystem.cs`.

Answered 2026-09-30 (Chase): **Carpentry and Tinkering first**, one or two crafts per batch. **Guild
homes approved as suggested.**

Open questions: none. Ready to batch after F-18.

### F-21: Community art in and around New Haven (added 2026-09-30)

**Ours** (new art; nothing OSI has is replaced unless noted). Follows F-8, which proves the updater
can ship new art; do F-8 first.

What Chase wants: art updates in and around New Haven.

Candidates (overseer, from the servuo.dev Art category, 2026-09-30; each needs its license checked):

| Pack | Author | Fit for New Haven |
|---|---|---|
| Farm carts | Moonrose | The farms and the market square |
| Oil lantern | Ems | Street and dock lighting |
| Satchel | Ems | Art for our ore and lumber satchels |
| Marble Railings, Bannisters, Ladder | OUTLANDSOwyn | The Registrar's office (P19) and guild halls |
| Paintings (several sets) | Odin, Hestia | The inn, the Registrar's office, guild halls |
| Bridge support beam | golfin | The docks |
| Orc encampment | Vrark | A camp on the outskirts, or the road to the new dungeon |
| Spooky Graveyard (41 graphics) | DRC1K | The Keepers of the Last Door's grounds |
| The Ultimate Dungeon Wall Set, New Gray Rocks | DRC1K | The New Haven dungeon (design doc in the overseer's project) |
| Free Halloween Asset Pack | DRC1K | A seasonal October event in New Haven |

Two kinds, handled differently:
- **New art** (all of the above): added in free art slots, used by items we place. Only where we put
  it changes.
- **Replacements** (for example Zigholtul's static replacements, "Tall Trees & Stuff", the "Trees of
  Verdant and Autumn leaves" set): change the look of existing art everywhere, not just New Haven.
  Zigholtul's set is already the back-pocket option in the state doc, with license questions.

Check first, per pack: license or terms; file format (PNG frames, or .mul/.uop already); free art IDs
from F-8's map, so packs never collide; total size the updater must ship.

**Downloads pending** (Chase hit servuo.dev's daily download limit, 2026-09-30): all but the farm
carts.

**Farm carts, downloaded 2026-09-30** (`D:\UO\third-party\farm-carts\`): 4 TIFFs named for the art
slots they are made for, **6784, 6785** (fruit cart, two facings) and **6807, 6808** (vegetable cart,
two facings). Checked in our client (`artLegacyMUL.uop`): all four slots exist and hold OSI's
**"UNUSED" placeholder** art, with no tiledata name, so the carts replace nothing. Tip for F-8 and the
rest: scanning for that placeholder finds free slots. Links are on each pack's servuo.dev page; save to Downloads and the overseer moves
them to `D:\UO\third-party\`.

Answered 2026-09-30 (Chase): **decorate New Haven appropriately with these packs.** The Halloween pack
is **kept in the back pocket**, not used this October. Winter and Christmas art is its own entry, F-22.

Open questions: none. Ready to batch after F-8. Placement is the overseer's draft for Chase to walk
in game before it goes on a world.

### F-22: Winter holiday decorations for New Haven (added 2026-09-30)

**Ported base, ours on top.** Chase, 2026-09-30: Christmas and winter may be the first holiday the
shard decorates for.

Found 2026-09-30:
- **Pinned already has OSI's holiday decor**, art that is already in every client: holiday trees
  (`Items/Special/Holiday/Christmas/HolidayTree.cs`, `Items/Deeds/HolidayTreeDeed.cs`), wreaths,
  stockings, snowmen, snow globes, snowflakes, poinsettias, holiday bells, holiday foods, the
  gingerbread house (`Items/Special/Holiday/`), and the 2004 and 2010 winter sets (snow piles,
  glacial snow, snowy trees, mistletoe, the Light of the Winter Solstice, festive cactus, decorative
  topiary, rocking horse, angel decoration; `Holiday Stuff/Christmas/`). Pinned also has
  `WinterGiftGiver`. **A first winter decoration needs no new art at all.**
- Community art (servuo.dev, licenses to check):
  - **[MrRiots] Winter/Christmas Related stuff** (2024): snow-covered paintings and shields, snow
    patches, holiday food, eggnog trays, gingerbread house, candy cane arch, animated stoves, an
    animated Father Christmas statue, an animated raised firepit, gift wrapping.
    https://www.servuo.dev/archive/mrriots-winter-christmas-related-stuff.2388/
  - **Christmas sprites** by Vrark (2025): static sprites and two animated Christmas trees, several
    directions. Some come from other games (DarkEden) and the Kingdom Reborn client; those carry
    rights questions, prefer the rest.
    https://www.servuo.dev/archive/christmas-sprites.2545/
  - **Publish 103 holiday clothes and mailboxes** (Sareus), **Some 2016 gift items** and **2016
    holiday bells and ribbon** (Shazzy): smaller sets, mostly OSI publishes.

Suggested (overseer):
- **Layer 1, OSI art only**: a holiday tree in the square, wreaths on the guild halls, snow piles and
  snowy trees, holiday bells, a snowman by the inn. Placed by an event seeder that can be switched
  on and off by date, so it comes down after the holidays without anyone cleaning up by hand.
- **Layer 2, community art** after F-8 proves the updater: MrRiots' animated Father Christmas and
  firepit in the square, the candy cane arch at the town entrance.
- A small event (gift giver, a snowball fight) is its own entry if wanted.

Check first: what `WinterGiftGiver` and the 2004/2010 sets do in pinned and whether they are hooked
to dates; which of the items above are placeable decorations versus player rewards; the license of
each community pack.

Answered 2026-09-30 (Chase): **up December 1, down January 6.** **All appropriate decor, both layers.**

**Art downloaded 2026-09-30** (Chase), copied by the overseer to `D:\UO\third-party\winter-holiday\`
(originals in `_zips\`, unpacked beside them, contact sheets `sheet-*.png`). BMPs use black as
transparent, as UO art does.
- **MrRiots, "For ServUO 2"** (87 BMP): candy cane arches and small canes, mistletoe, gift wrap,
  holiday food (gingerbread houses, eggnog trays, cookie pans, candy cane trays, fruitcake, pie,
  turkey, platters), **animated raised firepit** (5 frames), snow-covered shields and paintings, snow
  patches, **animated Father Christmas statue** (5 frames, several facings), **two animated stoves**
  (stone and metal, 4 frames each). Remade from OSI items; the best fit.
- **Vrark, "Christmas sprites"** (241 BMP, 1 PNG, usually 2 or 4 facings each): Christmas trees in
  several styles, wreaths, garland, sleighs, gift boxes and sacks, Santa's bag, stockings, a Christmas
  fireplace, ornaments, poinsettias, holly, gnomes, snowmen, snowflakes, toys (rocking horse,
  nutcracker, teddy bear, drum, trumpet), an advent calendar, 16 holiday paintings. Rendered from 3D
  assets (the file prefixes look like Daz Studio product codes).
- **Vrark, "Christmas tree 1 (animated)"** (5 BMP frames) and **"Christmas tree 2 (animated)"**
  (4 PNG frames). **Vrark's page says the two animated trees come from other games** (DarkEden is
  named): **leave them out** unless their source is cleared. Use the static trees instead.
- None of the downloads carries a license file.

Placement draft (overseer, for CC to propose tile by tile and Chase to walk in game):
- **The square by the quest board (3502,2573)**: a large static tree from Vrark's set with presents
  and Santa's bag, the animated Father Christmas statue, MrRiots' animated firepit, a snowman.
- **Town entrances and main road**: candy cane arches, OSI holiday bells and wreaths on posts.
- **Bountiful Harvest Inn**: holiday food and eggnog trays on tables, stockings, the Christmas
  fireplace, an animated stove in the kitchen, mistletoe in the doorway.
- **Guild halls and the Registrar's office**: OSI wreaths on doors, garland, holiday paintings and
  snow-covered paintings and shields.
- **Everywhere outdoors**: OSI snow piles and snowy trees, MrRiots' snow patches, light enough not to
  hide paths or block movement.
- **The docks**: a sleigh as a joke "delivery" on the pier.
- All of it from one event seeder keyed to the dates, every item flagged as event decor so take-down
  removes exactly what was placed and nothing else.

Open questions: none. Ready to batch after F-8.

### F-23: Paperdoll art replacements (added 2026-09-30)

**Client art only** (UI, like Fiddle-Me-This), so the fidelity rule is not touched; it changes how
every player's paperdoll looks.

Chase, 2026-09-30: find paperdoll replacers.

Candidates (servuo.dev, 2026-09-30):
- **UO Paperdoll Project (Siege of Sosaria) Builder's Kit**, Zigholtul (updated 2026-09-10): replaces
  the whole paperdoll gump set (bodies, hair, clothing, armor) for humans, elves and gargoyles, through
  Endless Journey and New Legacy items, plus spell icons, a "Dragon Desktop" and a login splash. PNG.
  https://www.servuo.dev/archive/uo-paperdoll-project-siege-of-sosaria-builders-kit-pngs-etc-included.2426/
- **UO Paperdoll Project (Classic UO)**, Zigholtul (2026-08-02): extra hairstyles, weapons, race art,
  PNG, installed with UOFiddler. https://www.servuo.dev/archive/uo-paperdoll-project-classic-uo.2662/
- Single pieces: Beholder armor (Cerrera), Lion Masks and Wings (Odin), Polar Bear Mask (Vert-I-Go),
  Female kimono (Ems), Orc male and female gump art (Odin).

Notes (overseer):
- **PNG gump art can ship the way Fiddle-Me-This does** (TazUO's `ExternalImages\gumps`, by gump ID),
  so no client file has to be edited and the updater ships small files. Check each pack's file names
  map to gump IDs.
- Fiddle-Me-This already restyles the paperdoll **frame** (P4); these replace what is drawn inside it.
  Check for overlap.
- Zigholtul states no license, and the state doc already notes some of his art comes from EA's
  Enhanced Client. Same caution as the static replacements.

Answered 2026-09-30 (Chase): **the Siege of Sosaria Builder's Kit look.** Not downloaded yet
(servuo.dev daily limit); save to Downloads when it resets.

Check first, once downloaded: file names against gump IDs (so it ships through `ExternalImages\gumps`);
overlap with Fiddle-Me-This; which pieces come from EA's Enhanced Client; whether its login splash
and "Dragon Desktop" are wanted or left out; total size for the updater.

Open questions:
- Everyone, or an opt-in download?

### F-24: League work: guild quests, monster hunts, culling and dungeon dives (added 2026-10-01)

**Ours.** OSI has nothing like it; closest are the Clean Up Britannia and bounty-style systems.

What Chase wants (2026-10-01): the League of Extraordinary Citizens is the guild for the guilds and
hands out the shard's adventuring work: **quests for the guilds, monster hunts for monster parts,
monster culling, dungeon dives, and similar.**

Overseer feedback:
- This makes the League the shard's main repeatable-content hub, and the natural XP and Renown source
  for F-12 and the spend side of F-13's shop. Worth designing as one contract framework with types,
  not four systems.
- **Hunts** (a named or elite target, drops parts) and **culls** (kill N of a species in a region)
  both need F-14's creature levels to be sized to the player. Order: F-14 before F-24's hunts and culls.
- **Dungeon dives** depend on the New Haven dungeon (P24 research) and, for the deeper version, on
  whether TazUO can read Trammel map edits from the player package.
- **Monster parts** need a sink: crafting recipes, guild turn-ins, or the F-13 shop. Without one they
  are vendor trash.
- Overlap to settle: guildmasters already hand out guild contracts (F-9, Decision 2.5).

Answered 2026-10-01 (Chase):
1. **Board contents:** the board shows **League jobs**, with tabs for jobs that cross guilds or serve two
   guilds at once. Start there and expand later.
2. **Realm-wide boards** in towns, taverns and dungeons, not only the field office.
3. **Rewards:** Renown, XP and League rank, **plus gold or another currency**, especially when the job
   is done for a guild other than the player's own (the overseer reads "another currency" as that
   guild's own scrip or seals, e.g. Smith Seals; confirm when specifying).
4. **Unlimited** jobs, but a **cap on how many a player holds at once**.
5. **Dive objectives:** resource gathering, a monster kill limit (culling), and **investigation, which
   spawns a temporary mini boss**.
6. **Solo, but shareable with the player's party.**

Decided 2026-10-01 (Chase), confirming the overseer's defaults:
- **Active-job cap: 3 to start, +1 per League rank.** Some jobs are **locked behind League ranks**.
- **Currency is the paying guild's own** (Smith Seals and the like), **plus that guild's reputation.**
  If the player is not in that guild, both are **banked and paid out when they join.**

Overseer suggestions (Chase to confirm or change when the prompt is written):
- Party sharing: party members inside range at the moment of a kill or gather all get progress; each
  member who accepted the shared job gets the full reward (no splitting), so grouping is never a loss.
- Investigation mini boss: spawns for the job holder's party only, despawns after a timer if not
  engaged, drops the parts that hunts are for.
- Board placement: one board per town bank or tavern, one at each dungeon entrance, starting with New
  Haven and the dungeons the starter guilds point to.

- **Banked reputation waits for the Apprentice task** (Chase, 2026-10-01). Joining is still free and
  instant at Initiate; the banked reputation (and seals) pay out once the Apprentice task is done, and
  can then lift the player past Apprentice at once. Chase's picture: a veteran mercenary joining the
  adventurers' guild after years in the field starts at first rank, then jumps up after onboarding.

Open questions: none. Overseer suggestions above (party sharing, mini boss, board placement) stand
as defaults unless Chase changes them when the prompt is written.
Order: after F-14 (job sizing by creature level) and with F-12's XP in place; dives after the P24
dungeon work.

Check first: the League design doc (`design\systems\league_of_extraordinary_citizens.md`, in
`D:\ShatteredLegacy`), F-3's Clean Up Britannia, pinned's quest and bounty code, and F-14.

## Batched

| ID | Batch prompt | Notes |
|---|---|---|
| F-9 | cc-P15-guild-starter-path | Written 2026-09-30. Entry kept under Open while its open questions stand. |
| F-7 | cc-P18-reset-stone-young-craftx | Written 2026-09-30. Part 1 of 3. Runs after P15 is committed. |
| F-5 | cc-P18-reset-stone-young-craftx | Written 2026-09-30. Part 2 of 3. Pinned rules changed via a patch or hook. |
| F-12 (research only) | cc-P20-skill-scaling-research | Written 2026-09-30. Read-only: skills past 120, gains, power scrolls, creatures, first XP curve. |
| F-1 | cc-P18-reset-stone-young-craftx | Written 2026-09-30. Part 3 of 3; may stop at findings if larger than expected. Custodian trash bag route held back until F-3. |
| F-16 | cc-P22-small-features-1 | Written 2026-09-30. Part 1 of 6. |
| F-19 | cc-P22-small-features-1 | Written 2026-09-30. Part 2 of 6. League rank bonus stubbed at 0 until F-12. |
| F-9 (thief at the pit) | cc-P22-small-features-1 | Written 2026-09-30. Part 3 of 6. Stool 3440,2558,55 from map data; Chase to confirm in game. |
| F-11 | cc-P22-small-features-1 | Written 2026-09-30. Part 4 of 6; may stop at findings if large. |
| F-17 | cc-P22-small-features-1 | Written 2026-09-30. Part 5 of 6. Port from ServUO-pub57. |
| F-15 | cc-P22-small-features-1 | Written 2026-09-30. Part 6 of 6. No deploy; Chase publishes the wiki page. |
| F-8 | cc-P26-animated-runestone | Written 2026-10-01. Runs after P23 and P22 are committed. Builds the art pipeline F-21 to F-23 reuse. |

## Dropped

| ID | Why |
|---|---|
| F-2 | Diminishing returns (with fractional credit) on Custodian tokens for repeated items. Dropped 2026-09-29 by Chase: F-3 folds the Custodians into Clean Up Britannia, whose valuation pays crafted gear only what its ingots were worth, so crafting cannot farm points and the curve has nothing to stop. |
