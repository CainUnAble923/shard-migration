# cc-P857: the variable carpet, rebuilt as ours

## In plain words

- **A carpet deed for houses:** double-click it, pick a colour (seven, from "as woven" to gold) and one of six carpets
  (blue, red and gold borders, patterned or plain), then click two opposite corners on your house floor. A carpet of
  exactly that size goes down, from 3 to 18 tiles a side.
- **Only the house owner can lay or lift one.** Outside your house, next to a door, on anything that blocks the floor, or with someone
  standing on the spot, it says why and keeps the deed. Double-click the carpet (within 3 tiles) and it asks before
  rolling it back up into a deed; chopping it with an axe does the same.
- **The deed names its makers:** "After Manu, Draco van Peeble and Milva", whose old RunUO carpet this follows.
- **For you:** nothing sells the deed yet; staff can `[add VariableCarpetDeed`. Say which store and price you want
  (the League shop or the Festival store), and whether 18 tiles is the right cap (`variableCarpet.maxSide` in
  modernuo.json).

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy on `golem/Iron/P857`. Main only.
The download in `D:\UO\third-party\code\variable-carpet\` was read as reference; nothing built, run or copied from it.
All play on the private proof shard (2596). No client or player package change (stock art).

## In game (TazUO, `notes\cc-P857-shots\main\`)

Private proof shard (2596) only, under the test-shard lock, a fresh copy of the bot world on `sl-modernuo:cc-p857`.
The trainee "Iron Carpet" is on a Player account; staff hands (`kit\stage857.py`) only moved the trainee and put a
stone-and-plaster house deed and a carpet deed in the pack (`[AddToPack`). Everything else is the trainee's own
clicks (`kit\Walk857.py`). **Every check PASS** (`main\walk.txt`), and the server's own view after each step is in
`main\stage-out.txt` (house owner "Iron Carpet"; carpet at 1984,2240,7, width 4, hue 1157, then hue 0).

- The trainee places the house on open grass at 1986,2242 (Trammel; flat grass, no statics, by the map), so it is really theirs.
- `p857-gump.jpg`, `p857-gump-wine.jpg`: the gump; the Wine button redraws all six previews in wine.
- `p857-refused-outside.jpg`: corners on the grass outside: "You can only place this in a house that you own!", deed kept.
- `p857-carpet-laid.jpg`: inside, a 4 by 4 red patterned carpet in wine; "Your 4 by 4 carpet is down."
- `p857-remove-confirm.jpg`: double-clicking it asks; `p857-rolled-up.jpg`: yes, it is gone and a deed is back.
- `p857-carpet-blue-gold.jpg`: the same deed again, blue with gold, as woven.

`run1\` is the first run, kept: its gump shows the help text clipped at the bottom (fixed: the text got more room and
the final image was rebuilt and gated again). Three runs between were script faults, deleted: the house deed lookup
matched the carpet deed's tooltip ("your house floor"), and targeting the bare ground inside a house gives the land's
z 0, not the floor's z 7; a player's click on the floor sends the floor tile, which the final script does.


## What was built

`server/customizations/Items/Addons/VariableCarpet.cs` (new, ours):

- `VariableCarpetSettings`: the six styles as our own table (corner, edge and middle art: the stock carpet pieces
  0xABD-0xAF9, the same nine IDs per style the reference uses, which are just the client's carpet set), seven hues
  (names checked in our client's `hues.mul`: 1109 HairHue/charcoal, 1150 ice_hue_5, 1157 dark red, 1266, 1272, 2213),
  and the size rule: `CheckSize` (at least 3, at most `MaxSide`). `MaxSide` reads `variableCarpet.maxSide` from
  modernuo.json (written with 18 the first time it is read), never below 3.
- `VariableCarpetAddon : BaseAddon`: one stock `AddonComponent` per tile, `ArtAt` choosing corner, edge or middle;
  saves style, width and height (source-generated). The owner's double-click within 3 tiles of any tile opens the
  confirm; `TryRemove` re-checks owner and range, takes it out of the house's addon list, and gives a fresh deed.
  A visitor's double-click does nothing. Stock `OnChop` (axe) also works, since `Deed` is a carpet deed.
- `VariableCarpetDeed : BaseAddonDeed`: double-click in the pack opens the gump; a style button starts our own
  two-step corner target ("Target one corner", "Now target the opposite corner"); `Place` runs every check server
  side and returns why: the deed in the pack, one floor (both corners at one Z), the size, nobody standing on the
  area, then the stock `BaseAddon.CouldFit` (every tile inside a house the placer owns, not blocked, not next to a
  door). The deed is used up only when the carpet is down.
- `VariableCarpetGump` (a colour row that redraws the 3 by 3 previews in that colour; six style buttons) and
  `VariableCarpetRemoveGump` (roll it up / cancel), both `DynamicGump`.

`CHANGELOG.md` and `VERSION`: **2026.11.10.3** (P855 and P856, not merged here, take 2026.11.10 and .2).

## How it differs from the reference

- The reference (`VariableCarpetAddonDeed.cs`, `VariableCarpetAddon.cs`) targeted first and then showed the style
  gump; it had no hue choice, let a **co-owner** remove a carpet (and so walk off with the owner's deed), measured the
  3-tile removal range from the west corner only, and checked nothing about the size beyond a minimum. Ours: colour
  and style first, then the corners; owner only; range from any tile; a cap in settings; refusals keep the deed.
- The stock door rule stays: a carpet may not come within 1 tile of a door (ModernUO's `DoorTooClose`), so a carpet
  stops a tile short of the doorway.
- The gold carpet (`goldcarpetAddon.cs`, a fixed 5 by 5 of the gold style) is not ported: the deed makes it at any
  size.

## Tests

`server/tests/Items/Addons/VariableCarpetVerification.cs`, eight facts:

1. The six styles are stock carpet art; a 5 by 4 carpet lays each corner, edge and middle where it belongs, in its hue.
2. The size cap: 3 at least, 18 by default, a lower cap obeyed, never below 3.
3. The gump: only from the pack; a colour button redraws it in that colour; a style button starts the targets.
4. Two corner targets (either order) in the owner's house lay a 3 by 3: every tile in the house, in the house's
   addon list, the deed used up.
5. Every refusal keeps the deed and lays nothing: a visitor with their own deed in the owner's house, outside a house, too small, too big,
   two floors, the owner and then a friend standing on it, the deed out of the pack; then the same deed lays it.
6. The confirm: a visitor gets nothing (and `TryRemove` refuses), a far owner nothing, cancel leaves it, yes rolls it
   up: every tile gone, out of the addon list, a fresh deed.
7. An axe (stock `OnChop`): a visitor's does nothing, the owner's gives the deed back.
8. Style, size and the deed survive a save.

Watched red, then green (`notes/cc-P857-tools/red-all.txt`, one container on `sl-uo-builder:bot`, `red-all.sh`):

- **The code before the change** (`red/stub.cs`: only the names the facts use, all inert): **8 of 8 failed.**
- **Eleven mutants** (`make_red.py`), each breaking one rule, each caught: no occupied check (fact 5), no in-pack
  check (5), no one-floor check (5), the cap ignoring the setting (2, 5), no minimum (2, 5), anyone may remove (6), no
  confirm (6), no range check (6), the hue not applied (4), the house's addon list not told (4, 5, 6, 7), the middle
  laid as border (1, 4).
- **Green:** 8 of 8 on the real code.
- **Gated builds** (`gated-build.ps1`, docker-build lock, page cache dropped first; `latest` not moved): the final one,
  after the gump text fix, `sl-modernuo:cc-p857` **EXIT=0, 3365 passed, 0 failed, 6 skipped** (`gated-build.log`,
  UTF-16); the first (`gated-build-1.log`) was the same: EXIT=0, 3365 passed, 6 skipped. The eight carpet facts are
  among the passes in both logs. The final gate ran the gump text fix; the red and green runs above were on the code
  just before it (layout only: two numbers in `BuildLayout`).

## Files

- `ShatteredLegacy`: `server/customizations/Items/Addons/VariableCarpet.cs` (new),
  `server/tests/Items/Addons/VariableCarpetVerification.cs` (new), `CHANGELOG.md`, `VERSION`.
- `shard-migration`: this file; `notes/cc-P857-tools/` (probe, red stub and mutants, results, build wrapper and log,
  the TazUO kit: `kit/stage857.py`, `kit/Walk857.py`, P856's runner scripts repointed); `notes/cc-P857-shots/`.

P857 DONE
