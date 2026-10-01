# New Haven dungeon: Chase's decisions on cc-P24 6.2 (2026-10-01)

Recorded by the architecture chat from Chase's answers. For the dungeon chat and the overseer. All twelve items of cc-P24 6.2 are now
decided (items 5-12 at 10:47).

## Decided

1. **Server data moves to 7.0.117.0** (Q-063, cc-P24 1b.6), **and the client floor follows to 117** (Chase,
   10:22). The player package enforces it: `player-package\payload\app\Setup.ps1:30` `$minVersion` goes from
   7.0.114.40 to 7.0.117.0, with its comment (`:26-29`) updated. Play.ps1 runs Setup.ps1 on every launch
   (`Play.ps1:231`) and Setup re-tests even a remembered folder (`Setup.ps1:63, 80`), so an old client is refused
   at launch with "Open the Ultima Online launcher ... and let it finish updating" (`:56`) instead of being kicked
   20 seconds after login. **Order matters:** publish the package carrying the new floor first, then raise
   `clientVerification.minRequired` on the server. **Settled (Chase, 11:26):** `D:\UO\UltimaOnlineVanilla` is a
   plain install patched by EA's own launcher, so EA's launcher delivers 117 or newer. This answers cc-P24's
   "Not verified" on those UOPs' origin: they are EA's, not a local edit.
2. **Young players:** keep stock `DungeonRegion` behavior: monsters may attack Young, and the warning gump shows on
   entry (`BaseRegion.cs:76-81`). **Plus a limit on how many monsters can attack one Young player at once.** That
   is a deviation; register it. Hook to evaluate: `Region.AllowHarmful(from, target)` is virtual
   (`Server/Regions/Region.cs:802`). Count the Young player's current hostile creature aggressors, and refuse a new
   one past N. **N is 2 to 3** (Chase, 10:22); pick 3 unless play-testing says otherwise.
3. **Travel:** block arrival, allow leaving. Not `NoTravelSpellsAllowedRegion`, which blocks everything for players
   (`NoTravelSpellsAllowedRegion.cs:23-27`). Our region's `CheckTravel` override returns false for `RecallTo`,
   `GateTo` and `Mark` when `newLocation` is inside the region, and true for `RecallFrom` and `GateFrom`.
   Note: `SpellHelper.CheckTravel` asks both the destination and the current region with the same type
   (`SpellHelper.cs:673-680`), so the override must decide by `newLocation`, not by type alone.
   **Mark must be blocked** or a rune marked inside becomes a way in. *Open: gate out (below).*
4. **Crafter option:** (a), owner upgrades their own gear as the main path, through `CustomCraft`
   (cc-P24 5.3). (b2), owner-to-crafter consent, is **tabled until a "mentor" role is designed.**

5. **Interior: candidate A**, Trammel 5136-5247 x 1128-1263 (cc-P24 2.1). Keep building at least 20 tiles from
   x 5120.
6. **Entrance: B1**, the ruined Second Bank of Haven, hole at 3619,2620 (cc-P24 2.2). Its known neighbors (the
   Healer and Banker spawners in the room, the Skeleton spawner at 3635,2625, the `BarredMetalDoor` at 3626,2621)
   are for the map batch to resolve.
7. **Widen the wood range (F3)**, `ResourceInfo.cs:1095`, **after checking the 8 extended woods in a client** before
   and after.
8. **Gloomsilk: cosmetic** (option A, a `Cloth` subclass with a hue).
9. **Starter craft gate 45**, with the cc-P24 3.7 numbers: Dawnstone harvest 45/5/85, Burrowhide carved, Rootwood
   harvest 45/5/85; bonuses about half of the lowest existing tier. Every number is a deviation to register.
10. (item 4 above)
11. **No-trade storage: worn, any bag in the owner's pack, or the owner's own bank.** Never to another player, a
    vendor, a house container or the ground. Stock `Nontransferable` refuses bags and the bank
    (`Server/Items/Item.cs:3424, 3461`), so the set pieces leave it false and enforce the rule in their own
    `OnDroppedToMobile`, `OnDroppedInto`, `OnDroppedOnto`, `AllowSecureTrade` and `CanEquip` overrides, plus
    `Blessed` and `BlessedFor`. Additive, a deviation to register. Tests: each allowed place takes the item, each
    refused place rejects it, a secure trade cannot start, death keeps it.
12. **Rootwood: cosmetic**, no `BaseRanged` patch. Its 3.7 bow bonuses (luck +20, damage +2) are dropped until a
    patch is worth it.
2b. **Package ships EA's Trammel files and `tiledata.mul`** (cc-P24 6.2 item 2). A package-policy exception that
    replaces `Build-PlayerPackage.ps1:20`'s premise; the overseer records it in `docs\`.

## Item 3, settled: no magical entry of any kind

Chase, 10:23: "You can only exit magically or physically, you can not enter magically." The rule for players
(staff exempt, as in `NoTravelSpellsAllowedRegion`):

- **Refuse, when the destination is inside the region:** `RecallTo` (spell, scroll, runebook, and Sacred Journey,
  which uses the same type, `Spells/Chivalry/SacredJourney.cs:51-55`), `GateTo`, `TeleportTo` from outside.
- **Refuse inside:** `Mark`.
- **Allow:** `RecallFrom`. Physical entry and exit through the B1 teleporters.
- **Refuse `GateFrom` inside, so no gate out.** A gate cast from inside opens a linked pair, and anyone outside can
  use the outer half for 30 seconds (`Spells/Seventh/GateTravel.cs:156-171`). Using a moongate never consults
  `CheckTravel` (`Items/Skill Items/Magical/Misc/Moongate.cs:73-130`: `CheckGate`, `UseGate`, `ValidateUse`,
  no travel check), so the region cannot refuse the inbound use. Making the outer half one-way would need a pinned
  patch or a sweep for new gates, neither worth it. Recall out covers leaving magically; each party member
  recalls for themselves.

Tests for whoever builds it: each refused type from outside and inside, each allowed one, a GM bypass, and a
gate cast inside fails with the stock message. Watch each red with the override removed.

## Flavored failure messages (Chase, 10:26)

The region's `CheckTravel` override sets its own `message`; pinned uses the stock text only when the region leaves
it null (`SpellHelper.cs:676-679`, `message ??= InvalidTravelMessage(type)`). So each refusal can say its own line
with no patch. Drafts for Chase to edit; one per refused case:

| Case | Draft |
|---|---|
| Recall or Sacred Journey in | "The rune finds only earth and root. Something below will not let you be pulled down." |
| Gate in | "The gate tears open onto packed soil, and collapses." |
| Gate out | "The burrow swallows the light before the gate can take shape. Walk out, or recall." |
| Mark | "The rune will not take. The ground here does not want to be remembered." |
| Teleport in | "You cannot reach through the earth." |

Tests should assert the exact message per case, so a later change to the override cannot fall back to the stock
text unnoticed.

## Architecture verdict on the optional pinned patches

Items 8 (Gloomsilk as a real tier) and 12 (Rootwood bow bonus): **decline both for now.** They add one to five pinned
patches at `--fuzz=0` while F-12 adds about thirty. Keep both cosmetic unless Chase wants the mechanic for itself.
