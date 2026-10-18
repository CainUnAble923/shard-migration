# Art brief: the Achievements paperdoll button (cc-P147)

For Chase's AI art chat. The button that ships now is a placeholder: the Help button's frame with "Achievements" in a
plain narrow face (`placeholder-states-x6.png`, six times size). This brief is for the real one.

## What it is

The ninth function on the classic paperdoll. In our TazUO, on our shard, it takes the **Help** button's slot (top of
the button column, x 185, y 44 on the 262 x 324 paperdoll background). `options-ABC.png` shows it in place;
`option-A-every-body.png` shows it beside all six Siege of Sosaria bodies.

## Size and states

- **64 x 21 pixels**, exactly the size of the Help, Options, Guild and Quests buttons, so it lines up in the column.
- **Three states**, three separate PNGs with a transparent background (no anti-aliased halo onto a colour):
  - **normal** (gump 22456): pale parchment label, RGB about (191, 175, 146);
  - **pressed** (22457): orange label, about (255, 164, 0), moved 1 px down and right, as the stock pressed states are;
  - **hover** (22458): orange label, not moved.
- The frame (the grey stone border and the dark field inside it) must match the stock buttons pixel for pixel at the
  edges, so the column reads as one set. The simplest path: keep our placeholder's frame (it *is* the stock frame) and
  redraw only the label.

## Style

- **Reference:** Castiel's "Classic Desktop Missing Paperdoll buttons" (servuo.dev 1519), gumps 22450 to 22455
  (Guild, Quests), and the stock Help, Options, Log Out, Skills and Status buttons. All use a blackletter label
  ("Help", "Guild" in a Fraktur-like face) about 10 px tall, with a 1 px dark shadow.
- **The problem:** "Achievements" is 12 letters, and the label field is about 54 px wide. A blackletter at the stock
  height does not fit. Options for the artist, in order of preference:
  1. a condensed blackletter at 8 to 9 px that still reads at 100 percent;
  2. a short word in the stock face: "Deeds" or "Feats" (our server page is still called Achievements);
  3. a small trophy or laurel icon left of a shorter word.
- Hand-placed pixels, no blur, as the stock labels are. It must read at 1x on a 1080p screen.

## Deliverable

Three PNGs named `22456.png`, `22457.png`, `22458.png`, 64 x 21, RGBA. They replace the placeholders in
`D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art\gumps\`. Nothing else changes: the IDs are registered
and the client already shows them. Credit line for `SOURCE.txt`: who made it, and "style after Castiel's Classic
Desktop paperdoll buttons".
