# cc-P451: League Register fix-up (repair targets, Field Satchel holding and fees, safe delivery)

## In plain words

- The League Field Satchel works as it was meant to. It takes a guild satchel however full that satchel is, and ore,
  logs, hides and essences mined or dropped go into the satchels inside it. A satchel it refuses no longer costs the
  merge fee, and moving one around inside it is free.
- Buying from the League Registrar, or taking a guild out of the Register, with a full pack now says "Make room in your
  pack first." and takes nothing. Before, it took the price and dropped the item at the player's feet.
- The Blaze repair on the Register is free, as you decided, but now repairs only the gear the member is wearing. The
  Field Satchel counts as one item only in the player's own backpack; in the bank or a house's secure storage,
  everything in it counts.
- Nothing for you to do. The wiki's League Register page has one line changed, which goes live at the next wiki
  publish.

## What changed

All in `server/customizations/LeagueRegister/` (ShatteredLegacy, branch golem/Iron/P451). Pinned is ModernUO
d4531cd; no patch touches the pinned files cited below.

| # | Finding (P418) | Fix |
|---|---|---|
| 1 | #1 Repair target checks only the target | `LeagueRepair.BeginTarget(from, source, used)`. When the target lands, the deed or kit must not be deleted, must still be in that player's backpack and, for a kit, `UsesRemaining > 0`. All three are checked before `Repair` and `used()`. The deed and kit pass `this`. |
| 2 | #2 `CheckHold` refuses resources on the parent walk | `LeagueFieldSatchel.CheckHold` runs the family and limit checks only for a guild satchel. Anything else is on its way into a satchel inside (pinned `Container.cs:274` walks the parents with the item being inserted), so it is passed to the containers above. A non-satchel dropped on the Field Satchel itself is refused at the drop (`Insert`, from `OnDragDropInto` and the 4-argument `TryDropItem`, which `OnDragDrop` and `PlaceInBackpack` reach). |
| 3 | #3 MaxItems 4 counted against `TotalItems + 1` | Pinned's item test (`Container.cs:247`) is no longer used here. `RefuseSatchel` counts satchels held (`Items`, not counting the one being moved) against `MaxItems` (4) and refuses a second of a family. The walk up passes `plusItems -= item.TotalItems + 1` while the satchel is in its owner's pack, so the backpack sees +0 items and still checks weight. |
| 4 | #4 Fee spent before the insertion | `Insert` checks the fee can be paid, inserts, and only then spends it. There is no fee when the satchel is already inside, or was lifted from it (`item.Parent == null && GetBounce().Parent == this`; pinned clears bounce after every drop, `Mobile.cs:5362`, `:5399`, `:5436`). Staff still pay nothing. |
| 5 | #5 Pay, delete, unbind, then unchecked `AddToBackpack` | `LeagueConsolidation.Deliver` calls `PlaceInBackpack` first. If that fails, it deletes the new item and returns `MakeRoom` ("Make room in your pack first.") before anything is paid. Only then come the payment and the deletion of the old logbooks. `Unbind` places the fresh book before removing the key. I applied the same order to `Issue` (the Register itself), which had the same delete-then-drop shape; the prompt did not list it. |
| 6 | #6 The 0-items discount everywhere | `InOwnersPack`: directly in a `PlayerMobile`'s own `Backpack`. Pack animals and vendors do not qualify, nor do the bank, a bag or a house container. Only there does `GetTotal(Items)` return 0 and are item deltas swallowed. Anywhere else it returns the children's totals (+1 each), and deltas pass up. Pinned sets `Parent` before an add's totals and clears it after a removal's (`Item.cs:3439` then `:3452-3454`; `:3566-3568` then `:3571`), so both sides of a move agree. |
| 7 | #7 Turn-in scans top-level items only | `TurnInAll` uses `Backpack.FindItemsByType<Item>(true, ...)`, which takes deeds in bags and in the Smith Guild Book, as `ClusterFSmithBODPayout.CanPay` does (`:129-130`, "a guild book in the pack counts"). |
| Chase | #8 Blaze repair | Free, and now worn gear only: `LeagueRepair.RepairWorn` (non-container items on the mobile). The remote repair deed keeps the whole pass (`RepairAll`). The message is "Nothing you are wearing needs repair." |

The Field Satchel no longer checks a weight limit of its own. Its guild satchels' caps bound it, and so do the
containers above it (the backpack's weight is still checked on the walk). Giving it `MaxWeight` 0 instead would have
removed the guild satchels' own caps, because pinned's `MaxWeight` returns 0 under a parent of 0 (`Container.cs:141`).

One case I left alone: if staff take a backpack off its mobile while a Field Satchel is inside, that pack's cached item
count is stale until the next `UpdateTotals` (the guild satchels call it on every add and remove, and so does world
load). Players cannot lift their backpack.

Also changed: `CHANGELOG.md` (2026.10.24.10: two Changed and four Fixed lines, in player words, with no description of
the repair exploit), `VERSION`, and one line of `docker/wiki/content/pages/uo/systems/league_register.txt`. That line
now says the satchel holds one of each kind and counts as one item while it is in the backpack. The wiki already
described Blaze as worn gear only.

## Tests

`server/tests/Misc/LeagueRegisterVerification.cs` (fact group 10). Each new fact goes through the real paths:
`OnDragDrop`, `OnDragDropInto`, `TryDropItem`, the target callback (`Target.Invoke`), `BuySatchel`, `BuyLogbook`,
`Unbind`, `Issue`, `TurnInAll`.

1. `ARepairTargetNeedsItsDeedOrKitStillInThePack`: deed handed over while A's target is pending (B repairs, A's target
   does nothing); deed banked after the target opened (no repair, deed kept); a kit's last charge spent by B while A's
   target is pending.
2. `OreDroppedOnASatchelInsideTheFieldSatchelLandsThere`: ore by `OnDragDrop`, ingots by `OnDragDropInto`, ore and logs
   by `TryDropItem` (what both routing hooks call), into satchels inside the Field Satchel. Gold dropped directly on it
   is still refused.
3. `TheFieldSatchelCountsAsOneAndChargesTheMergeFee` (rewritten off `Merge` + `DropItem`): a 20-stack satchel is
   accepted by drop, the fee is 50, and the pack's item total is unchanged.
4. `AFifthSatchelIsRefusedWithNoCharge`: four families in (one with 20 stacks); a fifth refused by both drops with no
   charge; a satchel lifted and dropped back inside is free; a satchel the pack has no weight for is refused with no
   charge, then accepted (and charged) once there is room.
5. `AFullPackTakesNothingAndDropsNothing`: full by items, then by weight. Satchel, logbook, unbind and re-issue are all
   refused with Renown, gold, old logbooks, binding and the current Register untouched, and nothing new on the ground.
6. `ABankCountsAPopulatedFieldSatchelsContents`: the bank counts 22 (field + satchel + 20). An ingot added while banked
   counts there. The round trip back leaves both totals where they began. In a bag in the pack the contents count.
   The cached total equals a fresh `UpdateTotals`.
7. `ANestedCompleteDeedIsTurnedIn`: a complete smith deed in a bag in the pack.
8. `BlazeRepairsOnlyTheGearTheMemberWears` (replaces `BlazeRepairsWornCarriedAndBankedGear`): only the worn sword is
   repaired. Carried, bagged, banked and another player's worn gear stay at 10.
9. `TheLeagueItemsSaveAndLoad` (P418 #10): the Register's owner, a kit at 4 charges, a Field Satchel holding a satchel,
   and a pack at MaxItems 250. Each is round-tripped through `Serialize`/`Deserialize`, and the reader ends at the
   writer's position.

**Red first.** I ran `docker/uo/build.sh -t sl-modernuo:cc-P451` under the `docker-build` lock (taken, then released).
I dropped the Docker VM's page cache before each run. Free memory was 11.7 GB, then 5.9 GB, then 4.7 GB.

- Red run 1: the new facts against the unchanged code. To make the save fact red, I added a mutant that took the
  Register's owner and the kit's charges out of the save. **9 failed, 2,292 passed, 4 skipped, and no other test
  failed.** Seven facts failed at the bug they target:
  - repair: A's sword was 50, expected 10
  - ore into the inner satchel: refused
  - 20-stack satchel: refused
  - full pack: the satchel was bought
  - nested deed: 0 turned in
  - Blaze: 4 repaired, expected 1
  - save: the owner was null

  The fee fact and the bank fact stopped earlier, at the 20-stack refusal (bug 3).
- Green: all fixes. **2,305 tests, 2,301 passed, 0 failed, 4 skipped**, and the image `sl-modernuo:cc-P451` was built.
- Red run 2 (`--tests-only`): all fixes, except three mutants:
  - the discount in any container (6 off)
  - the fee taken before the insertion (4 off)
  - the kit's charges not saved

  **Exactly 3 failed, 2,298 passed.** The bank fact counted 1 where it expected 22. The fifth-satchel fact found
  currency 0 where it expected 50 (refused drops were charged). The save fact found 0 charges where it expected 4.
  I restored the fixed files after this run and checked that no `MUTANT` text is left in the tree.

So each of the seven bugs, and the Blaze change, has a fact I saw fail at its own check, then pass.

`CHANGELOG.md`, `VERSION` and the wiki line were edited after the green build.

## Not done here

- Blaze repair being free with no cooldown (P418 #8) is P280's design. Chase decided on 10-22: free, worn gear only.
  That is built.

P451 DONE
