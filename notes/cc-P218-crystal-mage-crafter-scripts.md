# cc-P218: Crystal writes SL_Mage and SL_Crafter (stopped: the design docs are out of the cloud's reach)

2026-10-20. Prompt: `shattered-legacy-prompts/claimed/Crystal/cc-P218-crystal-mage-crafter-scripts.md` (claimed from
`queue/` at 21:22 UTC). Golem: Crystal, a Claude Code cloud session (machine `CLOUD`). Branches cut from `origin/main`:
`golem/Crystal/P218` in `shattered-legacy-scripts` (no change, not pushed) and in `shard-migration` (this note only).

## Why it stopped

The prompt builds the two scripts "as the design docs say": `sl-mage-script.md`, `sl-crafter-script.md`,
`new-legion-script-kickoff.md` and `legion-scripts-immortal-realms.md`, "in the claude.ai Project if you can reach it,
otherwise ask Chase to paste them". A cloud session cannot open the claude.ai Project, and the four documents are not
anywhere it can reach:

- not in any of the four repos (`grep -rli` over `shattered-legacy-infrastructure`, `shard-migration`,
  `shattered-legacy-scripts` and `shattered-legacy-prompts` for the four names and for `SL_Mage` / `SL_Crafter`: the
  only hit is the P218 prompt itself);
- not in Chase's Google Drive (two searches through the Drive connector, by title and by full text: nothing).

Writing a Mage and a Crafter helper without their design would be guessing at what Chase decided, and a home Golem
would then test the wrong thing. So this is the prompt's own "ask Chase to paste them" branch, with nothing built.

**For Chase:** put the four documents where a Golem can read them, for example `shard-migration/docs/legion-scripts/`
(the repo is public, so only if they hold nothing private) or `shard-migration/notes/design/`, commit and push, then
put P218 back in `queue/` (or re-queue it with a line naming the paths). The next Crystal run picks it up with the
preparation below already done.

## What was prepared (so the next run starts further along)

### The Legion API, as the existing scripts use it

Counted over `SL_Combat.py`, `SL_Loot.py`, `SL_Lumberjack.py`, `SL_Mining.py` and `SL_Retaliate.py` at the scripts
repo's `main` (11,017 lines in all): **94 distinct `API.*` names**. The ones a Mage or Crafter script will lean on, with
how often the five scripts call them:

| Name | Calls | Used for |
|---|---|---|
| `API.Player` | 347 | the character: hits, mana, stamina, weight, position, name |
| `API.Pause` | 101 | every wait |
| `API.PersistentVar` / `GetPersistentVar` / `SavePersistentVar` | 56 / 29 / 27 | settings that survive a restart (SL_Mining's `TOOL_ORDER_VAR` pattern) |
| `API.SysMsg`, `API.HeadMsg`, `API.Msg` | 40 / 28 / 3 | status lines; `Msg` says things in game |
| `API.InJournal`, `API.InJournalAny`, `API.ClearJournal`, `API.GetJournalEntries` | 30 / 30 / 17 / 6 | reading the server's replies (the way a craft result or a fizzle is detected) |
| `API.Backpack`, `API.FindItem`, `API.ItemsInContainer`, `API.FindLayer` | 30 / 24 / 19 / 17 | finding reagents, tools, the spellbook, resources |
| `API.UseObject`, `API.MoveItem`, `API.QueueMoveItem`, `API.EquipItem` | 25 / 9 / 2 / 3 | using tools, moving stacks |
| `API.Target`, `API.WaitForTarget`, `API.HasTarget`, `API.CancelTarget`, `API.RequestTarget`, `API.TargetTileRel`, `API.TargetLandRel` | 12 / 12 / 5 / 13 / 8 / 1 / 1 | targeting |
| `API.CastSpell` | 2 | casting (SL_Combat only; a Mage script makes this the main call) |
| `API.UseSkill` | 2 | skills by name |
| `API.HasGump`, `API.GetGump`, `API.GumpContains`, `API.ReplyGump`, `API.CloseGump`, `API.GetGumpContents`, `API.Gumps` | 7 / 4 / 11 / 6 / 6 / 2 / 3 | the craft menu and other server gumps (SL_Mining's tinkering path is the model for a Crafter) |
| `API.ContextMenu` | 2 | a context-menu entry by index (the satchel's Smelt) |
| `API.CreateGump`, `AddGump`, `CreateGumpTTFLabel`, `CreateGumpColorBox`, `CreateSimpleButton`, `CreateGumpCheckbox`, `CreateCooldownBar`, `AddControlOnClick`, `AddControlOnDisposed` | 3 / 3 / 15 / 6 / 5 / 2 / 2 / 5 / 3 | the control window every script has |
| `API.OnHotKey`, `API.OnStop`, `API.StopRequested`, `API.ProcessCallbacks` | 8 / 5 / 17 / 13 | hotkeys, clean stops, the main loop |
| `API.SetSharedVar`, `API.GetSharedVar` | 20 / 9 | how scripts talk to each other (SL_Mining asks SL_Combat to guard; SL_Combat drives SL_Loot) |
| `API.FindMobile`, `API.NearestMobiles`, `API.GetAllMobiles`, `API.Notoriety`, `API.IsFriend`, `API.Attack`, `API.SetWarMode`, `API.BandageSelf` | 14 / 8 / 4 / 10 / 3 / 6 / 11 / 6 | the combat side |
| `API.Pathfind`, `API.Pathfinding`, `API.PathfindEntity`, `API.CancelPathfinding`, `API.Walk`, `API.GetMap`, `API.GetTile`, `API.GetStaticsInArea`, `API.MarkTile`, `API.RemoveMarkedTile`, `API.TrackingArrow` | 5 / 11 / 8 / 4 / 10 / 14 / 2 / 2 / 12 / 12 / 16 | movement and the map |
| `API.RequestOPLData`, `API.ItemNameAndProps` | 5 / 6 | reading an item's properties |
| `API.ScriptPath` | 2 | where the script's own log goes (`SL_Combat.log`, `SL_Loot.log`) |

The full list is one command away: `grep -oh 'API\.[A-Za-z_]*' *.py | sort -u` in the scripts repo. The static
check the prompt asks for ("no name used that the Legion API does not have") can be done the same way: every name a new
script uses must be in that list, or in `API.py`, which only a TazUO client writes (it is git-ignored, so the cloud
never sees it; a name not in the five scripts' usage cannot be checked here and must be flagged for the home Golem).

### The house pattern (from SL_Mining, the reference)

- A header comment that says what the script does and how to start it, then a `CONFIG` block of plain constants a
  player can edit, each with a one-line comment.
- `GUI = True` control window with Start / Pause / Stop and the script's own buttons; settings the window changes are
  remembered with `PersistentVar`s named `SL_<Script>_<Setting>`.
- Safety stops: weight (`WEIGHT_STOP`), tools gone, a cap on tries per step (`MAX_SWINGS_TILE`), `StopRequested`
  checked in every loop, `OnStop` to clean up marks and the window.
- Journal checks for the server's exact lines, with the line quoted in the code.
- Errors to `SL_<Script>.log` beside the script (SL_Combat and SL_Loot do; SL_Mining does not).
- Item graphics as hex lists (`ORE_GRAPHICS`, `INGOT_GRAPHICS`) with the shard's own items included (Jacob's dead hue
  `0x0415`, the Reinforced Ore Satchel's Smelt entry).

### What the shard's code says that a design doc may not

- **There is no Herbalism and no herbalism reagents in `main`.** The only mentions are the tutorial's gathering wing
  (`Tutorial/TutorialStations.cs:108`, "Herbalism (Order of the Alembic, not built)") and the Alembic guild. If
  `sl-mage-script.md` relies on herbalism reagents, the code wins and that part waits.
- Reagent and spell handling for players is stock ModernUO: no patch under `server/patches/` touches spell circles,
  reagent costs or player mana (the three `Spell*` patches are the Urali trance, pet ability hooks and the spellbook
  talisman), and the `Reagent` hits in `server/customizations/` are imbuing and requisition property names, not
  spell reagents. Lower Reagent Cost and Lower Mana Cost are imbuable
  (`Imbuing/ImbuingTable.cs:161-177`).
- The craft menu is changed in three ways a Crafter script must know: **recipe gating** hides unknown items and adds
  hint rows to the item list (`server/patches/CraftGump-recipe-gating.patch`, `Engines/Craft/ClusterFRecipeGate.cs:4-8`,
  hint buttons from id `1_000_000`), **category pages** (`CraftGump-category-pages.patch`: long category lists page
  instead of running into the notices box, CHANGELOG 2026.10.05) and **Make X** (`CraftGumpItem-MakeX.patch`,
  `CraftGump-MakeXClear.patch`, `ClusterFCraftRun.cs`: craft a number and keep going on failure, F-1). Material names in
  the menu read in Title Case ("Dull Copper", D-114), and the sub-resource lists run to Celestial and Starwood
  (`ClusterFMiningExtension.cs`, `ClusterFLumberjackingExtension.cs:288-340`).
- Crafting past an item's top in a shard metal or wood raises the skill to the next material's requirement
  (`ClusterFMetalTiers.cs:70-81`, `ClusterFWoodTiers.cs:54-65`): a Crafter script that trains should pick the material
  by `ClusterFMetalTiers.RequiredSkill` and stop at `GainCeiling`, not at the item's own range.
- The Society of Smiths' "Orders that still teach me" already picks a training item for smiths (D-109); a Crafter
  script can read the deed instead of choosing an item itself.

### The test-prompt rule

The prompt's home-Golem test prompt takes "the next free number from queue, claimed, completed, held and _superseded
after a pull". At 21:25 UTC the highest numbers in use were P219, P220 and P221 (two different P221 files are in
`queue/`: `cc-P221-cont-fixup-port-wrong-and-covetous-void.md` and `cc-P221-tinker-golem-watchdog.md`, which the
overseer may want to know about), so the test prompt would be **P222** or higher once P218 runs. No test prompt was
written, because there is nothing to test yet.

## Working as a cloud Golem, this prompt

Same as P217 (`notes/cc-P217-crystal-wiki-catch-up.md`, section 6): the claim went through the GitHub API tool because
`git push` to the prompts repo's `main` is refused in the cloud session. The claim was three API commits (the file at its
new path, the `.status`, the delete at the old path) rather than one `git mv`; the merger and the queue readers see the
same end state.

The one thing that would have let this prompt run: the design docs in a repo. A cloud Golem can read everything that is
committed and nothing that is not.

P218 STOPPED: the four design docs (sl-mage-script.md, sl-crafter-script.md, new-legion-script-kickoff.md, legion-scripts-immortal-realms.md) are in the claude.ai Project, which the cloud session cannot reach, and in no repo or Drive folder it can; paste them into a repo and re-queue.
