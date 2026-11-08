# cc-P801 plan: the New Haven jail teaches name colors, reputation and guards

**Headline:** the three blank stops go away. One new stone jail holds the whole lesson: you click five people to learn the
five name colors, take from a marked crate and watch your own name turn gray, read your own karma, fame and murder counts
in the warden's ledger, then call the guards on a thief and see him cut down.

## Why the old lesson failed

It is a walking tour (`TutorialTradeTrials.cs`, row `reputation.wing`): the training yard, the healer, Rook's bench, with
one system message at each. Nothing to see at any stop, and the words scroll away. Chase, 11-05: "It's easy to miss what
you're supposed to learn."

## The place

One layout, 11 by 9 tiles, placed by the server on both maps and seeded on load so it appears on an existing world.
Grey brick walls, shingle roof, door in the south wall, three barred cells along the north wall, a guard hall south of
them with the warden's table, a bench, torches and hay in the cells.

| Branch | Plot (north-west post) | Land | Walk from the moongate exit | Mockups in `notes\cc-P801-review\` |
|---|---|---|---|---|
| Main (Haven on the SoS land) | 3702,2634 | flat at Z 20, on the dirt road beside the east farm field | 38 steps | `plan-sos.jpg`, `plan-sos-roofless.jpg` |
| `release/isle-20261028` (stock New Haven) | 3469,2597 | Z 8 to 10, the open yard inside the palisade | 35 steps | `plan-stock.jpg`, `plan-stock-roofless.jpg` |

The walks are from the map reader, not yet a real client. A named sign stands on the north side of the road or walk.

## Who is there

Name colors come from the real name color system, so what the player sees is the real thing.

| Color | Who | Where | Their line says |
|---|---|---|---|
| Yellow | Warden Hale | at the table | Yellow means nobody can harm me. Shopkeepers, guards and guides like me. |
| Blue | Mirren, visiting her brother | in the hall, at the bars | Blue is an honest name. Attack me and you are the criminal. |
| Gray | Finn the pickpocket | west cell | Gray is a criminal for now, or someone you may attack freely. It wears off in a couple of minutes. |
| Orange | a captured raider | middle cell | Orange is an enemy of your guild. You may fight without being a criminal. |
| Red | Black Tam | east cell | Red is a murderer: five murder counts. Anyone may kill me, and guards attack me on sight in town. |

The prisoners cannot be harmed, the bars keep them in, and every person answers a single click or a double-click.

## The lesson, step by step

A **lesson window** (a gump, not system messages) opens at the door, stays until closed, shows the five colors with a
checklist, and reopens from the quest or lesson command. The Guide's voice throughout; the System's voice only for the
completion line.

1. **Names.** Click each of the five people. Each says their line and ticks off in the window.
2. **The marked crate.** Take the marked pouch from the crate. Your name turns gray and a guard warns you. Click yourself
   to see it, and put the pouch back. Your name goes blue again.
3. **The ledger.** Double-click the warden's ledger. Your own karma, fame and murder counts appear with what moves each,
   and Black Tam's page shows five counts and how they wear off.
4. **Guards.** A thief only you can see grabs a purse in the hall. Say "guards". A guard flashes in and cuts him down at
   once. The window then says what real guards do, and that Trammel stops most attacks on players while Felucca does not.
5. **Done.** The System's completion line, and the next step said plainly: back to Rook for another lesson.

## No real penalties

The gray in step 2 is staged: no real criminal flag, no timer, no karma change, no guard attacks. Only the trainee sees it.
The thief is a lesson creature only the trainee sees, and "guards" there is a lesson response, not a crime report. Nobody
gets a murder count. The tests prove this by reading the player's real values before and after each step.

## What it costs

- A small server patch so a lesson person can show a set name color (and the trainee's staged gray). P743's private-horse
  patch is the same size of change. The patch must also apply to the release branch.
- The building, the people, the window and the steps replace the `reputation.wing` row and its text. Older characters who
  finished the old lesson keep it as done.
- P799 and P806 have **not** merged to main: P807's review of P806 failed on one sign. They do not touch the
  `reputation.wing` row, so no conflict is expected, but that is not yet tested. If they merge first I rebuild on them.

## Options for Chase

- **A: the whole jail lesson (recommended).** Everything above.
- **B: jail without the staged parts.** The jail, the five people, the window and the ledger. No gray name and no thief, so
  no server patch for the staged gray, and less to go wrong, but the player only reads about crime and guards.
- **C: the whole lesson, in the open.** The same people and steps at a small guard post and fenced pen, not a building.
  Cheaper to build, and it loses what you asked for: a jail.
