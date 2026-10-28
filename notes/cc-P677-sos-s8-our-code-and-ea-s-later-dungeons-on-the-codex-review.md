# Codex review: P677

CC task P677: Our code and EA's later dungeons on the new land (SoS swap S8). Reviewed by Codex (`codex exec review`, read-only) after P677 DONE and before the Golem's commit, 2026-10-28 16:34.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The changes address most requested relocations, but parking artifacts breaks their removal command and the coordinate proof omits important placement formats. Build success is recorded in the task artifacts; I did not independently rerun the build.

- **medium** [P2] Include the relocated layout records in the coordinate fact (`server\customizations\ClusterFMineCampLayout.cs:18`)
  The required fact over every remaining coordinate does not cover these records: `spots.py` only recognizes point constructors, numeric tuples, rectangles and go commands, so all 43 tent/decor components are invisible. Its recorded output contains only the four NPC move points for this file; it also misses the institution seeder's named coordinates and the New Haven `SeedEntry` rows. Consequently, invalidating a relocated component would still leave the new fact green. Extend extraction to these placement formats, with appropriate height-offset handling for roofs and stacked decoration, and prove an invalid placement fails.
- **medium** [P2] Handle parked artifacts when removing the spawner (`server\patches\StealableArtifacts-servuo-entries.patch:95`)
  After `GenStealArties` runs, the nine parked entries permanently have null `Item` values because of this return. Pinned ModernUO's `RemoveStealableArtifacts()` unconditionally evaluates `item.Deleted` for every entry, so `RemoveStealArties` now throws on the first parked slot, leaving removal incomplete. Extend the patch to skip null items during removal and test generating then removing artifacts with parked entries.

(1.2 minutes, 528,853 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The recorded build is green, but the required coordinate proof misses important changed placements. The delegated hall proof can also use unrelated inputs or pass from a stale checked-in report.

- **medium** [P2] Pass the selected map and checkout into the hall checker (`notes\cc-P677-tools\p281sos\hallbase.py:13`)
  The test advertises `SL_SOS_MAP` and `SL_SHARD_REPO`, but the hall checker uses the hardcoded `p677-work/sosclient` here and a hardcoded Iron code checkout in `check.py`. Thus selecting another overlay or checkout still checks Iron's old hall placements against its scratch map, not the inputs the other facts verify. The notes explicitly say this scratch folder can be deleted. Parameterize these paths and pass the selected inputs through to the subprocess.
- **medium** [P2] Reject checker failures instead of reading a stale report (`tools\tests\test_s8_spots.py:116`)
  If `check.py` crashes before writing its report, this test ignores the subprocess failure and reads the checked-in `check.out.txt`, which already satisfies the assertion. I confirmed the fact still passes when the subprocess returns 1 without producing output. This can report green with missing map data or a broken checker. Require a freshly generated complete report and distinguish checker errors from the expected P708 hall failures; this also follows the failure-proof requirement in [AGENTS.md:341???343](AGENTS.md#L341-L343).
- **medium** [P2] Extract the coordinate formats used by the changed seeders (`notes\cc-P677-tools\spots.py:40`)
  The extractor misses the actual placements in several required files: `ClusterFInstitutionSeeder.cs` uses named `x: ..., y: ..., z: ...` arguments, the mine-camp components use `new("tent", id, name, x, y, z)`, and New Haven's entries put `Direction` before Z. Running `literals()` finds only two old-world source positions in InstitutionSeeder and four NPC move positions in MineCampLayout, with none of its tent components. Consequently the new fact does not verify the placements this task changes, despite the requirement to cover every remaining coordinate literal. Add extraction and coverage assertions for these formats.

(1.6 minutes, 531,448 tokens)
