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
**Next free: F-5.**

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
  3 greater heal potions 5 (no vendor sells them). Trash bag: first one free from either NPC,
  replacements 1,000 (OSI's lowest tier; it is a tool that earns points, not a consumable).

Open questions:
- Approve or change the proposed prices above.

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

## Batched

| ID | Batch prompt | Notes |
|---|---|---|

## Dropped

| ID | Why |
|---|---|
| F-2 | Diminishing returns (with fractional credit) on Custodian tokens for repeated items. Dropped 2026-09-29 by Chase: F-3 folds the Custodians into Clean Up Britannia, whose valuation pays crafted gear only what its ingots were worth, so crafting cannot farm points and the curve has nothing to stop. |
