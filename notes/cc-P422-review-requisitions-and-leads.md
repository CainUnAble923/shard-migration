# P422: review of requisitions and Leads

2026-10-22. Docs-only review of code `da1a0cb` and migration notes `b21db84`.
`C/` below means `server/customizations/`, `T/` means `server/tests/Misc/`, and
`P/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`, verified at
`d4531cd94b739613155225c234900de9f47d2c88`.

Read both work copies' AGENTS.md, the direction decision and task list, P150's
implementation notes, and P203's follow-up. No separate Codex review of P150 was
found beside those notes; the wrong-guild view, death-event delivery, and flaky
corpse assertion already recorded there are not new findings here.

## Findings

1. **bug**, `C/Requisitions/RequisitionItems.cs:316`, also
   `C/Requisitions/Appraiser.cs:125`: the blanket blessed-item refusal blocks
   ordinary crafted spellbooks and every spellbook made by a Lead, since
   `P/Items/Skill Items/Magical/Spellbook.cs:122` makes them blessed and
   `RequisitionItems.cs:74` and `:75` use those constructors, so Arcane and Keepers
   book requests reject their intended items even after pity pays out.
   Allow the intended ordinary spellbooks through a shared eligibility rule while
   retaining protection for other blessed items, and add real book turn-in,
   Appraiser sale, and Lead-drop-to-turn-in tests for both book categories.

2. **bug**, `C/Requisitions/RequisitionItems.cs:389`: quality-only exceptional
   iron daggers qualify as magic and sell indefinitely for at least 85 gold each
   against three ingots with a base NPC purchase cost of 15 gold, because the
   formula pays for their ordinary exceptional Damage Increase as a magic
   property and `Appraiser.Sell` has no purchase budget or daily limit.
   Remove ordinary crafting bonuses from the Appraiser's magic eligibility and
   premium calculation, or impose a sustainable purchase budget, and add an
   economy regression using an ordinary tool's actual crafted output rather than
   staff-set attributes.

3. **risk**, `C/Requisitions/RequisitionSystem.cs:127`: changing the supported
   refresh hour from 05:00 to 06:00 at 05:30 moves the day index backward, so a
   character who filled today's slots gets another set on the next read and yet
   another at 06:00; a clock correction across the boundary has the same effect.
   Keep a monotonic last-issued day for automatic refreshes, leaving forced staff
   rerolls explicit, and test backward time and refresh-hour reloads after fills.

4. **risk**, `C/Requisitions/RequisitionTable.cs:440`, also `:470` and `:541`:
   otherwise valid configuration with `"themes": null` or `"areas": null` passes
   validation, replaces `Current`, and then throws when reload reports the counts,
   leaving board or Lead lookups using a broken table instead of preserving the
   old one.
   Reject required null collections and null rows before publishing the table,
   and test the real reload path for refusal without changing `Current`.

## Evidence and requested checks

The dagger calculation follows `P/Engines/Craft/DefBlacksmithy.cs:302` (three
ingots), `P/Mobiles/Vendors/SBInfo/SBBlacksmith.cs:16` (base buy price five per
ingot), and `P/Items/Weapons/BaseWeapon.cs:671` (exceptional Damage Increase starts
at 35). The applied `server/patches/BaseWeapon-arms-lore.patch:9` calls
`C/ClusterFArmsLore.cs:52` for the additional bonus; it does not remove the base.
`C/ArtificersImbueGump.cs:211` reads Damage Increase with Full 50, and `:799`
counts it as one active property. With the defaults in
`C/Requisitions/RequisitionTable.cs:99`, `:103`, and `:104`, the prices are:

| Arms Lore | Damage Increase | Intensity | Appraiser gold |
|---|---:|---:|---:|
| 0 | 35 | 70 | 85 |
| 100 | 42 | 84 | 92 |
| 200 | 50 | 100 | 100 |

These are source calculations, not measured live vendor quotes; town price
modifiers, tool costs, and throughput were not measured. The gap exists before
any runic property or rare material is involved. Crafting qualifying items for
the daily board is explicitly allowed by F-47 and is not itself a fake turn-in.

The promised 2x natural chance is already recorded as an unresolved design
departure in P150's decisions, P376 Q7, and P392 U78. It is not listed again as a
new finding. A concrete comparison: pinned Orc has Fame 1,500 and Meager loot
(`P/Mobiles/Monsters/Humanoid/Melee/Orc.cs:37`, `:83`), whose SE instrument entry
is 0.10% (`P/Misc/LootPack.cs:273`, selected by `:495`). A matching instrument
Lead adds a guaranteed matching instrument at a 5% first-kill chance
(`C/Requisitions/RequisitionTable.cs:78`), independent of that natural roll.
Without Luck or other modifiers, the chance of at least one instrument becomes
`1 - (1 - 0.001) * (1 - 0.05) = 5.095%`, or 50.95 times the natural type chance,
before considering how rare the requested slayer is. Thus the extra roll is not
a verified 2x multiplier.

The actual integer pity formula is
`extra + floor((100 - extra) * (kills - 1) / 39)`, with an explicit 100% at kill
40 (`C/Requisitions/RequisitionLeads.cs:211`). An offline Python calculation of
the survival probabilities gave:

| Fame band | Kill 1 | Kill 20 | Kill 39 | Kill 40 | Expected kills to a Lead drop |
|---|---:|---:|---:|---:|---:|
| 1,000 to 4,999 | 5% | 51% | 97% | 100% | 6.970801 |
| 5,000 to 14,999 | 10% | 53% | 97% | 100% | 5.704676 |
| 15,000 and up | 20% | 58% | 97% | 100% | 4.003324 |

The expected values assume constant Fame band, qualifying kills, and successful
item construction and delivery. Forty is the maximum wait, not the average, and
the endpoint math is correct. Finding 1 still defeats the promise that the
guaranteed item fills its request. Drops reset the pity count and leave the Lead
live (`RequisitionLeads.cs:263`), so a held request can keep generating items for
sale until expiry; this matches P150's stated behavior and is not a new duplicate
turn-in defect.

No additional client-reachable fake or repeated turn-in was found in the reviewed
paths. `RequisitionSystem.cs:226` checks current ownership of the request,
`:233` checks the backpack and deletion state, and `:252` removes the request and
deletes the item. The target checks counter proximity again at response time
(`C/Requisitions/RequisitionsBoard.cs:321`); the Appraiser rechecks ownership,
proximity, and the current price when selling (`Appraiser.cs:111`). Under a fixed
refresh hour and forward-moving time, the daily boundary, completed-slot behavior,
and retention of live Leads have no additional defect found by this review.

## Tests and limits

Reviewed `T/RequisitionsVerification.cs`, the account serializer coverage in
`T/AccountDataSerializerVerification.cs`, all files under `C/Requisitions/`, and
the P150 hooks in `ClusterFAccountData.cs`, `ClusterFDevTools.cs`,
`ClusterFGuildSystem.cs`, and `LeagueRegistrarGump.cs`. The relevant pinned item,
crafting, loot, and vendor implementations and their shard patches were also
checked.

The existing Lead integration test at `T/RequisitionsVerification.cs:539` makes
only an HCI sword; it does not check every default theme/category through factory,
matching, and turn-in. The pricing test at `:479` sets properties directly and
misses ordinary exceptional crafting. The refresh test at `:289` only advances
time, and the invalid-file test at `:166` calls Parse rather than Reload. Those
gaps explain why the findings above are not covered; the suggested regression
tests belong with the later fixes and must be seen failing first.

No code or tests were changed, and no shard build, runtime reproduction, or client
session was run. Runtime effects remain unverified beyond the source paths and
offline arithmetic described here. No connection to Haven was made.

Ran `tools/progress.py --dry-run` with both work-copy paths supplied. It completed,
but still wrote `tools/progress.json`; that incidental snapshot was restored to
its initially clean contents so the only deliverable is this note.

P422 DONE
