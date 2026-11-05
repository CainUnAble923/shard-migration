# cc-P800 plan: the League sash upgrades over time

**Headline: one sash per character, earned in six steps at the League's milestone ranks. Elara upgrades it for a Renown fee, each step changes its name and hue, and each adds a very small Renown bonus while worn.** That's my recommendation, option 1. Chase picks; nothing is built until he does.

## What's there today

- The League sash is a `BoundCosmeticSash`, label "League": blessed, bound to the **account**, no perks.
- **It isn't for sale.** The prompt says the League shop, but the shop only uses it as a loot box prize (`LeagueShop.BoxPool`, in the League's blue). A second route, `@leaguecloak` in `LootBoxRoller`, gives it in the character's rank hue. So a player can hold several, or none.
- **The League has 17 ranks,** each hued by its metal, and six milestone ranks: Dull Copper, Bronze, Verite, Blaze, Mythril, Celestial. Lifetime Renown only rises; spending comes from a separate balance, so spending never lowers rank.
- **Loops:** F-12 isn't built, so a loop only adds to a count today. League rank, Renown and achievements sit outside the loop by F-12's rules (`notes\f12-levels-loops-caps.md`).
- **The test shard's release branch** has ranks, Renown, Elara's gump and loops. It does **not** have the League hunts (P780) or the steward at headquarters. So hunts can't be a requirement there.

## The steps

The ranks and their first-guess fees. Every number goes in `Configuration/league-sash.json`.

| Step | Opens at rank | Name | Hue | Fee (option 1) | Renown bonus |
|---|---|---|---|---|---|
| 0 | Iron | a League sash | League blue | free | none |
| 1 | Dull Copper | a Dull Copper League sash | the metal's | 50 | +1% |
| 2 | Bronze | a Bronze League sash | the metal's | 250 | +2% |
| 3 | Verite | a Verite League sash | the metal's | 1,000 | +3% |
| 4 | Blaze | a Blaze League sash | the metal's | 3,000 | +4% |
| 5 | Mythril | a Mythril League sash | the metal's | 6,000 | +5% |
| 6 | Celestial | a Celestial League sash | the metal's | 10,000 | +6% |

A title line under the name says what the wearer is, such as "Sash of a Verite Citizen, step 3 of 6", and the loop count once the character has looped, such as "Worn through 3 loops".

**What is never on it:** skill or stat points, item properties, or anything that would make it a property artifact. The bonus adds to Renown earned from achievements and League jobs, not to Renown paid by other players. It's a plain percentage in the file, and setting it to 0 turns it off. It does shorten the climb a little, so it's Chase's call; options 2 and 3 show the alternatives.

## In every option

- **One per character.** Blessed, bound to the character instead of the account. It stays on the character through any loop, keeping its step, as rank and Renown do.
- **Getting the first one:** free from Elara's League menu, once, for any registered citizen. A lost sash can be replaced there at the character's step.
- **Loot boxes:** the sash leaves the box pools once a character has one, and the box gives its other prizes.
- **Old sashes convert in place at world load, once.** A sash held by a character (worn, in pack or bank) becomes that character's new sash, at step 0, or at the highest step their rank allows for free in option 2. If a character holds two, the first converts and the rest stay as plain keepsakes labelled "old League". One sitting in a house converts when its owner next picks it up.
- **Other sashes aren't touched:** Box, Loop and Achievement Store sashes stay as they are.

## The options

**Option 1, recommended: earned at Elara.** Rank opens a step; the player visits Elara and pays Renown from the balance. There's a small effect and sound, and the League announces it to them. It feels earned, gives Renown a new use, and works on both branches. Small Renown bonus as above.

**Option 2: by itself.** It changes on promotion with no visit and no fee. It follows every one of the 17 ranks in hue and name. Simplest, and always current, but nothing to do and so less "earned". No perk.

**Option 3: earned with deeds.** As option 1, with extra needs: the higher steps also ask for great hunts done, and the top steps for loops. The most earned, but hunts aren't on the release, so those needs stay off there until it catches up. Bigger build and more to explain.

## Build outline, after his answer

1. A `LeagueSash` class (new saved type, source-generated serialization per D40), keeping `BoundCosmeticSash`'s binding pattern but bound to the character.
2. `Configuration/league-sash.json`, written with defaults on first start and refused whole if bad, as `league-ladder.json` is.
3. A League Sash row in Elara's menu, on `LeagueRegistrarGump`.
4. The conversion after world load, idempotent, logging a count.
5. Facts for each step, the conversion, binding, blessing and a loop; watched red first.
6. Main, then a resolved diff for `release/isle-20261028`, built as `sl-modernuo:cc-p800-isle`; shots of each step in `notes\cc-P800-shots\`.
