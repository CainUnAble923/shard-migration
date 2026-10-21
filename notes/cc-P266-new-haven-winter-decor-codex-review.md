# Codex review: P266

CC task P266: New Haven winter holiday decorations (F-22), ready to switch on December 1. Reviewed by Codex (`codex exec review`, read-only) after P266 DONE and before the Golem's commit, 2026-10-21 17:21.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The change substantially implements the requested registration, placement and seasonal switch, but has lighting, upgrade-state and calendar-validation defects. Tests were not rerun; the notes also explicitly leave the requested in-client screenshot unverified, supplying offline renders instead.

- **medium** [P2] Check the calendar's facet before awarding a gift (`server\customizations\WinterAdventCalendar.cs:202`)
  If a player opens the calendar and then travels to matching coordinates on another facet, the retained gump still awards gifts: `Mobile.InRange(Point3D, int)` compares only X/Y, not maps. Require `from.Map == _calendar.Map` when handling the response (and when opening the calendar) so the distance check actually requires proximity to this item.
- **medium** [P2] Migrate the existing winter persistence before switching stores (`server\customizations\ClusterFWinterDecorSeeder.cs:117`)
  For an existing P34 save, removing `ClusterFWinterDecorState` discards the saved automatic state in `WinterDecor/WinterDecor.bin`; the shared store starts winter at null instead. If the old save last had winter up and this build first loads outside the window, `ClusterFSeasonalSwitch.Sync` records false without calling `Down`, leaving the old decorations up until another full season passes or staff clear them. Import the old automatic state and adopt the existing winter items into the serial list before the first shared-switch sync.
- **medium** [P2] Set the light shape on each placed candle item (`server\customizations\ClusterFWinterDecorSeeder.cs:227`)
  The newly placed candles remain ordinary `WinterDecor` items with `Light` defaulting to zero. Updating tiledata's quality byte does not set the light shape for dynamic items: TazUO's `GameScene` uses `item.LightID`, populated from the item's transmitted direction, and ModernUO exposes that through `Item.Light`. Consequently these candles render the default window-shaped light instead of the configured circular lights. Set each light-emitting item's `Light` from its record when constructing it, and test the placed item's value rather than only tiledata.

(2 minutes, 1,363,215 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The placement knowingly reuses artwork that the task requires clearing or skipping, and the required client screenshot is missing. The new validation tool also bypasses registration checks for its own art block. Server implementation correctness was not established by this docs-repository review.

- **high** [P1] Exclude uncleared REG artwork from the placement (`notes\cc-P266-new-haven-winter-decor.md:52`)
  The prompt explicitly requires skipping the REG portion unless its terms clearly allow use and changes. These notes instead acknowledge that its licence is unspecified and reuse it because it was previously registered. The new placement also adds presents and snow patches from that block. Prior registration does not establish permission; exclude those pieces or record readable clearance before enabling this layout.
- **medium** [P2] Check registration for the new art block as well (`notes\cc-P266-tools\validate.py:48`)
  When a placement uses an ID in the new 0x3388???0x33B6 block, this branch accepts it without checking `REGISTERED`; only P34's IDs receive that check. Consequently, removing or omitting a new registry row still lets `validate.py` pass and `gen_layout.py` write the layout, defeating its advertised registration gate. Apply the membership check to both winter blocks.
- **medium** [P2] Supply the required client preview screenshot (`notes\cc-P266-new-haven-winter-decor.md:46`)
  The completion criteria require both a preview screenshot and a top-down render, but all supplied previews are offline renders and no client was run. Those renders cannot verify the installed overrides, animation, lighting or calendar gump as actually displayed. Capture the placement in the test client before declaring this deliverable complete.

(0.9 minutes, 398,411 tokens)
