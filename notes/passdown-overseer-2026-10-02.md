# Overseer pass-down, 2026-10-02

Supersedes `passdown-overseer-2026-10-01.md` for queue state and numbers; its "how this chat works" section still
holds. Read `claude/shattered-legacy-state.md` in the project for machines and the web stack (dated 2026-09-29).

## Numbers (re-derive before trusting: `grep -rhoE "\b(D|Q|F|T)-?[0-9]+\b" notes docs | sort -u`)

- Bugs: **next free D49** (D44 talisman leak, D45 meditation, D46 tool suite, D47 ddns follows a VPN, D48 extract durability, all 2026-10-02).
- Deviations: **next free D-105** (D-92 to D-104 registered 2026-10-02).
- Features: the **features chat** owns `docs\feature-queue.md` and is writing to it (it took F-25 and F-26 on
  2026-10-02). Do not write there concurrently; hand feature requests to that chat.
- Prompts: P1 to P32 exist (P29 defect batch 2 done `56cae9d`; P30 ModernUO upgrade research; P31 registrar office cleanup; P32 spawner importer, BODs, Self Repair; P33 F-3 Clean Up Britannia). **Next free P34.** Another chat also writes prompts: re-check `cc-prompts\` and `completed\` right before saving a new one.

## Queue

| Prompt | State |
|---|---|
| P22 small features 1 | done, committed `fd88276`; decisions `p22-decisions-2026-10-01.md`; only the 1,000-item bank check is left |
| P23 live defect sweep | done, committed `70f01e3`; Chase's client checks 10-14 not reported yet |
| P24 New Haven dungeon research | done; Chase's decisions `dungeon-decisions-2026-10-01.md` |
| P25 stats above 125 | done; **Chase decided no stat ceilings** (`p25-decisions-2026-10-02.md`) |
| P26 animated runestone | done, committed `0f4c989`; **all T-rows pass** (`p26-decisions-2026-10-02.md`); package can publish |
| P27 defect batch 1 | done, committed `eccf5af`; in-game checks pending (fountain reach, imbue split) |
| P28 launcher account profiles | done, committed `e2ca43d`; needs package build, install update, then `scripts\Make-SLAccountShortcuts.ps1` |

Nothing is building. **One builder at a time in `D:\ShatteredLegacy`.** Notes-only prompts run alongside.

## Next builds, in order

1. **Defect batch 2:** D44 (fact first), D45, D46 (tools), plus anything from Chase's P23/P27 checks.
2. **F-3** Clean Up Britannia with the Custodian layer (ready, about 20 units, ported, base game).
3. **F-12**, blocked on Chase: reserve cap, echo multipliers, step size above 100, how League metal ranks are
   earned. The stat half is now simple (`f12-levels-loops-caps.md`, Stats, rewritten 2026-10-02).
4. Parked: F-18/F-20 BODs (after F-12 caps), F-14 (Bard base now, level number after F-12), F-21/F-22 decor on
   P26's pipeline (F-22 dated: test shard before Dec 1), F-25 launcher progress (features chat).

## Open and owned

- **Conflict to resolve before the dungeon map batch:** P26 built the art pipeline on "the package ships nothing of
  EA's" (`Build-PlayerPackage.ps1:19`, gated), while dungeon decision 2b says the package ships EA's Trammel files
  and `tiledata.mul`. Both are Chase's decisions. When the dungeon map work is briefed, settle which wins (or
  whether 2b becomes "patch the player's own files locally", the P26 route) and record it in `docs\`.
- Dungeon deviations (Young aggro limit 3, no magical entry, no-trade storage, starter craft numbers, client floor
  7.0.117.0) are decided, not built. Register them when built.
- D34 tabled (race work last). Q-009 compose mount still Chase's, oldest item.
- D43 refunds: Chase runs `[SmithSealScrollCensus` if he wants them.
- `feature-queue.md` "Where things stand" is stale (still says P23 running, P22/P26 queued). The features chat
  owns that file; ask it to refresh, or refresh it when it is idle.

## Lessons from 2026-10-01/02

- **Run git in Chase's repos only with `--no-optional-locks`.** A plain `git status` from the device shell left an
  `index.lock` it could not delete (deletion is off by default), which blocks commits.
- **Chase's commit script ran mid-build during P26** and committed a red run (`c386e3c`). Briefs now warn about it;
  remind Chase to commit only after the builder says done.
- **Check a row before citing it.** On 10-02 I told Chase D34 and D35 had to land before the fresh world; D35 was
  done (cc-P8) and D34 tabled. Same failure the 10-01 pass-down warned about.
- **The stat cap was 500, not 125,** in every note until cc-P25 read the config. Read configs, not prior notes.
- An unpublished package is tested by unzipping it to its own folder; the launcher's update check only asks
  get.shatteredlegacyuo.com.
