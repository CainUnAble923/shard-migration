# Architecture verdict: F-12 per-stat ceilings by stat lock (2026-10-01)

Architecture chat. Read only. Answers the pass-down's question on `f12-levels-loops-caps.md` lines 64-74, and folds
in cc-P23's finding on `ClusterFStatCaps`. No D or Q number taken.

## Verdict: unsound as written; sound with one additive handler

**As written, a player defeats it with one click.** The lock is client-controlled. Packet 0xBF sub 0x1A,
`StatLockChange` (pinned `UOContent/Network/Packets/IncomingExtendedCommandPackets.cs:301-322`), writes
`from.StrLock = (StatLockType)lockValue` with no check. The setter (`Server/Mobiles/Mobile.cs:628-640`) is not
virtual and raises no event. So a player at their personal ceiling flips the arrow back to Up, `CanRaise` passes
(`UOContent/Skills/SkillCheck.cs:337-339`), and they gain to the global `stats.statMax` of 200.

**The fix needs no pinned patch.** Extended handlers live in an overwritable table:
`RegisterExtended` assigns `_extendedHandlers[packetID]` (`IncomingExtendedCommandPackets.cs:77-83`), and pinned
registers 0x1A in its `Configure` (`:41`, `:54`). Ours re-registers 0x1A from an `Initialize`, which runs after every
`Configure` (`Server/Main.cs:441,448`). Our handler refuses Up for a stat at or above the character's personal ceiling
and otherwise does what pinned's does. Plus: on login and on level-up, a stat at its ceiling with lock Up is set to
Locked; Down is never touched, so lowering still works.

**Other raise paths checked.** Player stat gain goes only through `SkillCheck` (`:366,387,408`, each also clamped
to `_statMax`). Pinned also sets `RawStr` in `Special Systems/Engines/TestCenter.cs` and ours in
`TestCenter/TestCenterKit.cs:174` and `ClusterFDevTools.cs:122-124`; all staff or test-center paths. The rest of
pinned's hits are creatures, resurrection loss and spells on non-players.

**Required tests for whoever builds it:** a player at ceiling sends 0x1A Up and the lock stays Locked; a player
below ceiling sends Up and it takes; a stat at ceiling never gains over N forced gain rolls; Down still lowers.
Watch each red with the handler unregistered.

## cc-P23's finding, confirmed: the 500 is live

`f12-levels-loops-caps.md:166-167` calls `DefaultIndividualStatCap = 500` dead config. It is not.
`patches/PlayerMobile-individual-stat-cap.patch` replaces pinned's `Math.Min(base.Str, 150)` (and Dex, Int) in
`PlayerMobile` with `ClusterFStatCaps.IndividualStatCap`, which is 500 when enabled
(`customizations/ClusterFStatCaps.cs:10,103`). `base.Str` includes item and buff offsets (`Mobile.cs:1866-1868`).
So today the **effective** stat a player gets from gear and buffs is clamped at 500, not OSI's 150. Gain is
still stopped at 125 by `_statMax`, so this bites only through offsets.

- **It is a live deviation and is not in `docs\` (grep for the patch and the setting, 2026-10-01).** Register it.
- **F-12 must set it deliberately.** With a per-stat raw ceiling of 200, the read clamp should be the raw ceiling
  plus OSI's offset headroom (OSI: 125 raw, 150 effective, so +25), or an explicit number Chase picks. Leaving
  500 means gear can push effective stats to 500 after the F-12 build.
- The patch is one of the pinned patches applied at `--fuzz=0`; F-12 touches the same property block. Fold any
  change into this patch rather than adding a second one on the same hunk.

## Two cc-P23 side findings that are F-12 input, not defects

- Stock power scrolls (105-120) are unusable while every cap is 300 (`PowerScroll.cs:252`). F-12 repoints scrolls
  at level, so leave until then.
- `InfusedAlchemistsGem.cs:28` adds to Alchemy Base past the cap (cc-P23 1, sub-agent). Under F-12 the skill cap
  is the level, so this becomes a way past the level. Rank 4's exploit list should include it.
