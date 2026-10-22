# Codex review: P368

CC task P368: added music for areas, monsters and bosses (new tracks, stock music kept). Reviewed by Codex (`codex exec review`, read-only) after P368 DONE and before the Golem's commit, 2026-10-21 21:58.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The empty assignment table matches the missing Music Room selections, and the package infrastructure is present. However, the server implementation has reproducible priority, opt-out, layer-switch, and sub-area gameplay defects. Tests were inspected but not rerun in this read-only review.

- **medium** [P2] Stop active fight music when its layer is disabled (`server\customizations\Music\ClusterFShardMusic.cs:565`)
  If staff disable `clusterf.music.bossLayer`, `monsterLayer`, or `enabled` during an existing fight, `Check` never checks the setting and keeps the track active until combat ends. Only new engagements honor the switches. Reevaluate the active fight's enabled state in the watch and restore the appropriate lower-priority music when it is disabled; the current layer test only covers disabling before engagement.
- **medium** [P2] Allow explicit child assignments to override inherited mappings (`server\customizations\Music\ClusterFShardMusic.cs:238`)
  If a parent region row precedes a row for one of its children, mapping the parent recursively inserts the child into `_stock`. The child's explicit row then returns here without applying its chosen track, although the application log reports that track. This makes valid parent-and-child assignment tables depend on row order. Keep the original stock value separately from whether an explicit assignment may update the region's music.
- **medium** [P2] Preserve gameplay properties in music sub-areas (`server\customizations\Music\ClusterFShardMusic.cs:54`)
  Adding a music box inside a dungeon changes young-player protection: `ShardMusicRegion` inherits `BaseRegion.YoungProtected == true`, whereas `DungeonRegion` overrides it to false. Pinned `PlayerMobile.CheckYoungProtection` reads the current region's property directly, so young players gain protection inside the music box. These BaseRegion properties do not automatically delegate to Parent as the comment assumes. Delegate the relevant gameplay properties or use a music mechanism that does not change them.
- **medium** [P2] Preserve fight music when the player changes regions (`server\customizations\Music\ClusterFShardMusic.cs:565`)
  During a mapped fight, crossing a region or sub-area boundary lets pinned `Region.OnRegionChange` send the area's track over the boss or monster track. The watch then returns immediately while `IsLive` remains true, and repeated engages with the same creature do not resend music either. Consequently area music wins for the remainder of that fight, contrary to the required priority. Handle region changes while fight music is active and preserve the higher-priority track.
- **medium** [P2] Correct opted-out music when mapped tracks differ (`server\customizations\Music\ClusterFShardMusic.cs:439`)
  When an opted-out player walks between two mapped regions with the same original stock music but different shard tracks, pinned sends the destination's shard track because their current `Music` values differ. This stock-value comparison then skips the correction, leaving shard music playing indefinitely despite `[ShardMusic off`. This also occurs between a mapped region and its differently mapped sub-area. Determine whether pinned changed the music before skipping the stock resend.

(2.1 minutes, 484,219 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.92). This repository's only change is the P368 notes file; no actionable defects were found in it. The server and player-package implementation resides in the separate code repository, so this review does not verify that implementation or its reported test results.

No findings.

(0.5 minutes, 105,864 tokens)
