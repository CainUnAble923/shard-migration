# P660: review of P656 safeguards

Reviewed October 26, 2026. Two findings: a replacement bag can take another
player's belongings, and the fallback can bypass bank storage limits. Both
are in our new replacement logic. No code changed for this review.

Reviewed P656 commit `13a20692302f34f7a2ab413d3d921a69a717708b`, merged at
code HEAD `3b4d3218c8e9f4d29888dbaaceaac92385315e94`. Pinned ModernUO is
`d4531cd94b739613155225c234900de9f47d2c88`. File references below are relative
to the code work copy unless marked as pinned.

Read both work-copy AGENTS.md files, the direction decision and task list,
both `cc-P656-*.md` notes, and `cc-P574-questions-for-chase-2.md`. Also checked
P432, P476 U2, P547 and P556 A1 to distinguish new findings from earlier
reviews. P656's existing Codex review reported no findings. The original
barrel overpayment, ordinary merged-stack loss, bag contents wipe, sweep
access defects and store facet check are not reported again here.

## Findings

1. **High (P1): replacement can steal contents from another player's pack.**
   `server/customizations/TrashBag.cs:95`, `:104`.

   `OwnedBy` selects bags solely by their saved `Owner` (`:75`), regardless
   of who currently holds them. A trash bag remains an ordinary transferable
   container. Player A can give their empty bag to B, let B store belongings
   in it, then request a replacement. The new loop moves B's belongings
   directly into A's new bag, backpack or bank before deleting the old bag.
   There is no current-possession, access or consent check. Distance and
   facet do not limit that transfer. This adds theft to the previously
   reviewed remote deletion defect.

   Pinned `Projects/Server/Items/Item.cs:569` makes ordinary items
   nontransferable only when they are quest items; TrashBag adds no transfer
   restriction or ownership change on transfer. Pinned
   `Projects/Server/Items/Container.cs:426` checks destination capacity, not
   permission to remove the source item. Its `DropItem` at `:464` reaches
   `Item.AddItem` at `Item.cs:3391`, which removes the item from its current
   parent without asking the other character.

   **Fix:** preflight the old bags before changing anything. Refuse
   replacement while a bag is held by another character, in their bank or
   trade, or behind access restrictions the requester cannot satisfy.
   Leave that bag and its contents intact. Preserve safe recovery from the
   requester's own accessible storage. A saved bag owner alone must not
   authorize taking its current contents.

   **Missing regression:** transfer A's bag to B, add a unique item belonging
   to B, then answer A's Warden replacement button. Assert that B retains the
   item and A receives none of it. Include B's bank and a restricted ancestor.
   P656's replacement fact at
   `server/tests/Services/CleanUpSafeguardsVerification.cs:228` covers only
   the owner's bank and the ground, with available destination capacity.

2. **Medium (P2): the bank fallback creates repeatable storage beyond the cap.**
   `server/customizations/TrashBag.cs:104`, `:106`.

   Fill the backpack and bank to their item limits, leave the owned trash
   bag on the ground with ordinary nonstackable contents, and request a new
   bag. Both `TryDropItem` calls refuse the contents. The fallback uses
   `BankBox.DropItem`, which inserts them even though the bank is full.
   Refill the replacement bag on the ground and repeat to keep adding bank
   storage beyond its limit. The new bag itself is also force-inserted into
   a full backpack at `:93`.

   Pinned `Projects/Server/Items/Containers.cs:8` derives BankBox from
   Container; its `CheckHold` at `:93` delegates ordinary item capacity
   checks to the base. Those checks are in
   `Projects/Server/Items/Container.cs:230`. `DropItem` at `:464` calls
   `AddItem` without those checks. A bank fallback was requested by P476 U2,
   but bypassing capacity is a new consequence of this implementation.

   **Fix:** plan all destinations, including the new bag, under their normal
   capacity limits before moving or deleting anything. If the contents
   cannot fit, refuse replacement and retain the existing bag and contents.
   P476 U2 explicitly permits refusal as the safe alternative. Do not solve
   this by deleting overflow or by creating unrestricted overflow storage.

   **Missing regression:** use full backpack and bank containers, a grounded
   owned bag and distinct nonstackable contents. Answer the Warden button
   twice. Assert that item totals never exceed the applicable limits, items
   survive, and refusal leaves the old bag and contents intact. The P656
   replacement fact never exercises either capacity failure or the bank
   fallback.

## Coverage and limits

Read P656's implementation and test files:

- `server/customizations/Services/CleanUpBritannia/CleanUpTrash.cs`
- `server/patches/TrashBarrel-clean-up-britannia.patch`
- `server/customizations/TrashBag.cs`
- `server/customizations/SanitationWardenGump.cs`
- `server/customizations/ClusterFCustodianSystem.cs`
- `server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs`
- `server/tests/Services/CleanUpSafeguardsVerification.cs`
- P656's `CHANGELOG.md` changes and `VERSION`.

Also inspected the shared valuation, immediate cleanup barrel, trash chest
patch, existing barrel and bag tests, and pinned container, item, bank,
trade and trash barrel behavior. Findings follow those source paths.
Gameplay reproduction, actual affected inventories and deployed behavior
remain unverified. No tests were added or executed and no build ran for
this notes-only task. P656's reported red/green tests and gated build were
not rerun. The proposed regressions must fail before fixes and pass after.

No Haven connection, deployment, account operation, code edit, docs/ edit,
commit, merge, push or branch switch occurred. Commands used Windows
PowerShell 5.1. Stop-request checks were made between steps.

Ran `tools/progress.py --dry-run` with both work-copy path overrides. Its
incidental progress.json write was suppressed in memory; the existing file
remained byte-identical. No generated progress files changed.

Final checks: the code work copy is clean, and the migration work copy has
only this new note. Whitespace checks passed. The note is ASCII, has no em
dashes or trailing whitespace, and is below 5 MB. No stop request was
present at the completion check. No P660 review work remains.

P660 DONE
