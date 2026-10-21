# cc-P169: Upgrade and restore menus: clear met / not met colours

2026-10-20. Server only (`D:\ShatteredLegacy`, branch `golem/Silver/P169`). Player-facing: every upgrade, restore and
rank-up menu. Chase, 2026-10-18 13:29, with the Hammer of Hephaestus "Upgrade to T2" screenshot.

## Headlines

- **One helper, one look** (`server\customizations\ClusterFRequirements.cs`, new): `RequirementList` builds a menu's
  lines and draws them as labels beside stock art. **Met:** green, the client's ticked check box (gump **211**), with
  the numbers ("Blacksmithy 119.0 / 80"). **Not met:** red, a stone box with an X (gump **5231**), with how much more
  ("Smithing Seals 10 / 25 (need 15 more)", "Rank: Journeyman (need 4,975 more Standing)"). **Info** (where the ingots
  are, "Gold counts from your pack and bank.") gray, indented under the art, no art. **Headings** ice white (1153).
  Under the lines, a **summary** ("All requirements met" green with a check, or "3 requirements not met" red with an
  X), then the action: a live button only when every line is met, otherwise the same button art and words in a dim
  gray with **no button behind them**. Every handler still checks everything on the press (tested).
- **Menus moved to it:** the Hammer of Hephaestus (instant restoration and the T2 upgrade), Jacob's Pickaxe upgrades
  T2, T3, T4 and T5, the Miners' Compact liaison's Restoration and Upgrade Ore Satchel (and satchel recovery), the Civic
  Mule Exchange (now one mule a page, Next / Previous), and the League Registrar's Rank page (the promotion report,
  `ClusterFLeagueRanks`). Searched for others with the pattern (`Clr(bool)` yellow / red HTML, "Requirements not met",
  "Upgrade to", "Restore", "Promote to"): none beyond these. The work-order ledger's turn-in lines are similar
  (green / red labels) but are a turn-in, not an upgrade; left as is (decisions).
- **Solid background:** the frame's inside is tile 2624, as P57 Part E did for the bulk order window
  (`RequirementStyle.AddSolidPanel`, replacing `AddAlphaRegion(6, 6, W - 12, H - 12)`), in all five menu classes
  (the liaison and the Registrar on every page they show).
- **Why the headings were green:** TazUO draws a label of hue N with hues.mul entry N + 1, and the menus' headings
  used 1154, entry 1155 "green highlight". Headings are 1153 now (entry 1154, ice white #DEF6F6).
- **The rank line (part 4):** the met test was the same in every menu and in its handler (standing >= the rank's
  standing), and it was right: 25 / 5,000 was coloured `#FF6666` in the HTML, and my render of the old menu shows it
  red (`before-Hammer_of_Hephaestus.png`). I could not reproduce the yellow Chase saw (no TazUO source or client on
  this PC; see decisions). The lines are now labels, not HTML, so how the client colours HTML no longer decides it, and
  `RequirementList.Rank` is the one rank test every menu draws with; it is met only at the rank's standing (R1 below).
- **Tests: 7 new facts, all seen red first** (red A: the menus at HEAD and a deliberate fault in the helper, 6 failed;
  red B: the new code with a deliberate fault in the League report's lines, 1 failed). Full gate
  `docker/uo/build.sh -t sl-modernuo:cc-P169`: **1,635 tests, 1,631 passed, 4 skipped**, image built.
- **Before and after renders** of every menu for the screenshot's kind of character (rank short, seals or vouchers
  short, the rest met) are in `notes\cc-P169-requirement-colors\` (16 PNGs), drawn from each build's own gump entries
  with EA's gump art, unifont1 glyphs and hues.mul.

## Hues and art

Label hues as sent (the client draws entry N + 1 of `classic-client` hues.mul; the colour is that entry's brightest):

| Use | Label hue | hues.mul entry | Colour |
|---|---|---|---|
| Met | 0x44 (68) | 69 | #4AEE31 green |
| Not met | 0x22 (34) | 35 | #F66283 rose red |
| Info | 999 | 1000 | #ACACAC light gray |
| Heading | 1153 | 1154 "ice_hue_2" | #DEF6F6 ice white |
| Disabled action | 0x3B2 (946) | 947 | #5A5A5A dim gray (the button art drawn with the same hue) |

Red-green colour blindness: the check box (211) and the X box (5231) carry the meaning on every line and on the
summary; the green is also much brighter than the red. Art read from `gumpartLegacyMUL.uop` (7.0.117.0): 211 is 19 x 20
(the ticked check box; `SmithBulkOrderChoiceGump.CheckOn`), 5231 is 19 x 16. The vseUOAware MCP `render_gump` cannot
read that file (its entries are zlib + Mythic BWT, flag 3; it reports "Implausible gump dimensions"), so the art was
decoded with a port of `scripts\Shard-Console.ps1`'s BWT reader (`notes\cc-P169-requirement-colors\gumppng.py`).

## What changed, file:line

| File | Change |
|---|---|
| `server\customizations\ClusterFRequirements.cs` (new, 241 lines, 10 KB) | `RequirementState`, `RequirementLine`; `RequirementStyle` (hues, art, `AddSolidPanel` `:66`, `AddAction` `:72`); `RequirementList` (`:88`): `Amount`, `Skill`, `Rank` `:120`, `Has`, `Check`, `Price` `:136` (a GuildResources price as `CanPay` checks it), `Info`, `Draw`, `DrawFooter` `:230`, `Summary` |
| `server\customizations\HammerOfHephaestus.cs:1112-1231` | `HammerRestoreGump`: height from its lists (`:1136`), solid panel, 1153 headings, `RestoreRequirements` `:1158`, `UpgradeRequirements` `:1162`, the status rule moved to 112 (`:1205`; at 100 it crossed the second status line, in the old menu too) |
| `server\customizations\JacobsReinforcedPickaxe.cs:220, :265`; `JacobsProspectorPickaxe.cs:197, :240`; `JacobsDeepdelverPickaxe.cs:198, :242`; `JacobsWorldbreakerPickaxe.cs:201, :245` | each upgrade gump: `H` from its lines (first number), `Requirements` (second): rank, skill, `Price`, the previous pickaxe; the bonus text kept above in gray |
| `server\customizations\MinersCompactLiaisonGump.cs:114` | solid panel, 1153 headings (all views) |
| same, `:405-476` | Upgrade Ore Satchel: recovery and upgrade as requirement lines; `SatchelUpgradeRequirements` `:466` |
| same, `:550-603` | Restoration: requirement lines and footer; `RestoreRequirements` `:599` |
| `server\customizations\CrossGuildExchangeGump.cs:40, :59, :75-118` | solid panel; one mule a page with Next / Previous; requirement lines and footer per mule |
| `server\customizations\Mobiles\Mule\MuleUpgrades.cs:91` | `Requirements(pm, guild, step)`, the same tests as `Shortfalls` |
| `server\customizations\ClusterFLeagueRanks.cs:64, :94` | `LeagueCheck` carries `Have` / `Need` / `CountLabel` for the counts (optional, existing callers unchanged); `LeaguePromotionReport.Requirements()` |
| `server\customizations\LeagueRegistrarGump.cs:67, :247` | solid panel, 1153 headings; the Rank page draws `report.Requirements()` and the footer (Promote) |
| `server\tests\Misc\RequirementColorsVerification.cs` (new) | 7 facts and the render dump, below |
| `server\tests\Misc\LeagueLadderVerification.cs:640-646` | D6 reads the Rank page's new lines (one line a check, the summary) |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.20.16`: three Changed, two Fixed lines; VERSION `2026.10.20.16` |

## Tests

`server\tests\Misc\RequirementColorsVerification.cs`:

- **H1** `H1_TheHelpersLinesHaveTheirWordsHuesAndArt`: the words, state, hue and art of met, not met (amount, skill,
  rank, held item) and info lines; heading and info hues are neither met nor not met; the summary's words.
- **H2, H3** `H2_H3_DrawnLinesAndTheFooter`: a line is its art and a label 24 to the right on its row; an info line is
  a gray label without art; the footer's live button, or the disabled art and words with no button.
- **M1** `M1_EachMenuForACharacterWhoMeetsEverything`: the eight menus (Hammer, Jacob's T2-T5, liaison restoration T5,
  satchel upgrade, Mule Exchange tier 4 to 5): opaque (2624 under the inside, no alpha region), no 1154 label, every
  art beside its line in its colour, "All requirements met" and the live button for each action, every label inside the
  frame, clear of the footer rule and not crossing any rule.
- **M2** `M2_EachMenuForACharacterWhoMeetsNothing`: the same menus for a poor character: each summary counts the X's
  above it, no button, the disabled art; each button id pressed anyway changes nothing (output: "Hammer of Hephaestus:
  pressed 10, 20 anyway: still T1 True, T2 False, seals 0", "Mule Exchange (tier 4 to 5): pressed 100 anyway: still
  tier 4", and the same for the other six).
- **M1, M2 League** `M1_M2_TheLeagueRankPage`: a met and an unmet promotion report's lines ("Lifetime Renown 40 / 100
  (need 60 more)", "Guilds at Apprentice or higher 0 / 1 (need 1 more)", the job line, the waived trial as info), its
  summary, and AllMet equal to CanPromote. The Registrar page itself is D6 in `LeagueLadderVerification`.
- **R1** `R1_TheRankLineIsMetOnlyAtTheRanksStanding`: output "smithing 25: "Rank: Journeyman (need 4,975 more
  Standing)" hue 34", "smithing 4999: ... (need 1 more Standing)" hue 34, "smithing 5000: "Rank: Journeyman 5,000 /
  5,000 Standing" hue 68"; Jacob's T2 and the satchel upgrade at 999 (red) and 1,000 (green); the X or check beside it.
- `DumpsEachMenuForTheScreenshots` is not a fact: it writes each menu's entries as JSON for the renders.

Seen red first:

- **Red A** (the eight menu files at HEAD, the new helper with met drawn in the not-met hue, marked
  `RED-RUN MUTATION`, and all new tests): `Total tests: 1635, Passed: 1625, Failed: 6`: H1 (Expected (68, 211),
  Actual (34, 211)), H2_H3 (Expected (42, 68), Actual (42, 34)), M1 and M2 (`Assert.Empty() Failure`: the
  HammerRestoreGump's `GumpAlphaRegion`), R1 (no "Rank: " label: the old line was HTML), and D6 (the old Rank page's
  lines). `M1_M2_TheLeagueRankPage` passed: it reads the new report-to-lines code only, which A kept.
- **Red B** (all the new code, `LeaguePromotionReport.Requirements` treating a waived check as met, marked
  `RED-RUN B MUTATION`): `Total tests: 1635, Passed: 1630, Failed: 1`, that one `M1_M2_TheLeagueRankPage`. B also
  showed every other new fact green on the new code.
- **Green** (no mutation; `grep -rn RED-RUN server/` finds nothing): `Total tests: 1635, Passed: 1631, Skipped: 4`,
  "Built sl-modernuo:cc-P169 with patches applied and 1631 shard test(s) passing." (498 s).
- The "no label crosses a rule" check in M1 / M2 was added after the first green build, when the after render showed
  the Hammer's second status line through the rule at 100. I did not run a build with the check and the old layout;
  the first green build's dumped entries show the label at 90 and the rule at 100, which the check refuses
  (100 > 92 and 100 < 106). The final build has the check and the moved rule, green.

## Renders (before and after)

`notes\cc-P169-requirement-colors\before-*.png` and `after-*.png`, one pair a menu: Hammer_of_Hephaestus, Jacobs_T2 to
Jacobs_T5, Liaison_restoration_T5, Liaison_satchel_upgrade, Mule_Exchange_tier_4_to_5. The character: standing 25,
seals / vouchers 10, Blacksmithy 119, Mining 120, plenty of ingots and gold. "Before" is from red A's builder image
(the menus at HEAD), "after" from the final green one, by `DumpsEachMenuForTheScreenshots` and `render.py`
(`python -I render.py LOG OUTDIR PREFIX`). They are approximations: the backdrop is a made-up striped pattern so a
see-through window shows it; the alpha region is black at 50%; HTML is drawn as BASEFONT colours and line breaks with
word wrap; the old HTML's colours are drawn as written, so the before Hammer shows the rank red, not the yellow
Chase's client showed.

## Deviations and decisions for Chase

- **The yellow rank line is not explained.** In the old Hammer menu the rank line was `<BASEFONT COLOR=#FF6666>`
  whenever standing was under 5,000 (code unchanged since the migration), and the handler refused the same way. With
  no client source here (the TazUO clone `D:\UO\tazuo-sl-build` is not on this PC) I could not see why TazUO drew it
  yellow. The new menus draw no HTML for requirements, so whatever it was cannot recur there. If the new Hammer menu
  ever shows a rank line in the wrong colour, that is worth a bug with a screenshot.
- **Rank is standing, as before.** Every rank line (and its handler) compares guild standing with the rank's
  standing. It ignores the Apprentice task's bump (a player shown Apprentice at standing 25) and P78's craft
  promotion cap (standing past Journeyman but held back by skill). Keeping the rule unchanged was the safe reading of
  "fix the met test". If the rank shown in the guild menus should be the rule instead, that is one line in each
  `Requirements` method (`ClusterFGuildSystem.GuildRankIndex`), and the "need N more Standing" wording would change.
  The Mule Exchange already used the rank index (`MuleUpgrades.Shortfalls`); its line says "(you are Master)" when
  standing is enough but the rank is held.
- **"Smaller" info lines are not smaller.** TazUO draws server labels and HTML in one font (unicode font 1, P57), and
  I could not confirm the client honours `BASEFONT SIZE` without its source. Info lines are set apart by the gray
  hue and the indent under the art column instead.
- **The testing token** no longer paints unmet lines as met: the lines show the truth, the summary adds "(waived:
  Testing Token)", and the button stays live, as before.
- **The Mule Exchange shows one mule a page** (Next / Previous at the bottom). With every requirement on its own line,
  three mules no longer fit on one page.
- **Not changed:** the work-order ledger's turn-in lines (green / red labels, `GuildContractLedgerGump.cs:312`), the
  guild join screens' requirement text, and the liaison's member dashboard (yellow HTML, not requirements). Say if
  any should use the helper too (P177 plans the guild menus template on it).
- The restoration's old "Your Mining Vouchers: N" line is gone; the vouchers line shows the count.

## For Chase

Rebuild the test shard from `sl-modernuo:cc-P169` (or the merged main), then:

- **Hammer of Hephaestus menu:** at the Society of Smiths guildmaster, open the Hammer menu with a T1 hammer. Expect:
  solid window, white headings; each requirement green with a check or red with an X and "(need N more)"; gray
  pack / bank lines; "All requirements met" or "N requirements not met" under each list; the Restore and Upgrade
  buttons greyed out until met. With 25 standing the rank line reads "Rank: Journeyman (need 4,975 more Standing)" in
  red.
- **A Jacob's Pickaxe upgrade:** at the Miners' Compact liaison, Member Dashboard, the next tier's upgrade. Expect: the
  bonus text in gray, then the same look as the Hammer; the button live only when everything is met.
- **Miners' Compact liaison restoration and satchel:** Restoration and Upgrade Ore Satchel views. Expect: the same
  look, and a solid window on every page of the liaison.
- **Cross-guild (Civic Mule) Exchange:** from a trade guild's Member Dashboard, with your mule beside you. Expect: one
  mule a page, its next step's requirements a line each (Compact rank, each guild's scrip, gold), the summary, the
  Upgrade button greyed out until met.
- **League Registrar, Rank page:** Expect: Lifetime Renown and the guild count with numbers, the promotion job and
  story trial lines, the summary, and Promote only when all are met. `[version` shows 2026.10.20.16.

## Repo size rule

Largest new file: `notes\cc-P169-requirement-colors\before-Hammer_of_Hephaestus.png`, 71 KB (the 16 renders and two
scripts total 916 KB). In the code repo, `ClusterFRequirements.cs` is 10 KB and the test 22 KB. Scratch (logs, the
contact sheets of gump art) is in the session scratchpad under `%LOCALAPPDATA%\Temp\claude\`, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (commits nothing): code 15 files
pending (`CHANGELOG.md`, `VERSION`, the eleven customizations files, the two test files above), docs 19 (this note, the
16 renders and the two scripts in `notes\cc-P169-requirement-colors\`). Neither repo BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P169 DONE
