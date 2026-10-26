# Codex review: P634

CC task P634: build Town Houses, stage 1. Reviewed by Codex (`codex exec review`, read-only) after P634 DONE and before the Golem's commit, 2026-10-26 03:42.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The core and staff tools are implemented, but test-only execution is not enforced, storage limits use the wrong AOS semantics, and placement does not establish guarded-town coverage. Client acceptance and a full world restart also remain explicitly unverified in the implementation notes.

- **high** [P1] Enforce the test-shard restriction at runtime (`server\customizations\Leaseholds\ClusterFLeaseSite.cs:345`)
  `Leaseholds` is registered unconditionally and its handler never checks `TestCenter.Enabled`, so staff can create sites and assign leases on the live shard despite the explicit test-only scope. `ShardCommandAttribute` is descriptive metadata, not an execution gate. Reject mutations outside the test shard, including outstanding target callbacks.
- **medium** [P2] Validate guarded-town coverage throughout the occupied volume (`server\customizations\Leaseholds\ClusterFLeaseSite.cs:113`)
  This check only establishes that the bottom layer matches the street region; it never requires that region to be a guarded town. Consequently, an empty wilderness rectangle passes creation and assignment, while a building whose upper floors intersect an excluded child region also passes. The leasehold then replaces the entire volume with a region parented to the street region. Validate the required town ancestry and exclusions across the occupied 3D area before activation, as required by P550's guard-coverage correction.
- **medium** [P2] Supply an AOS item-storage limit rather than a container count (`server\customizations\Leaseholds\ClusterFLeasehold.cs:132`)
  `GetAosMaxSecures()` is the total item-storage budget used by `BaseHouse.CheckAosStorage`, including lockdowns and secure-container contents, not the number of secure containers. Returning `MaxSecures` therefore gives a 16??16 site only 16 total storage items despite advertising 2,048 lockdowns; a site smaller than 16 tiles allows only one item. Provide an appropriate AOS storage budget and test actual lockdown and filled-container operations.

(1.9 minutes, 562,726 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The notes document substantial implementation and build evidence, but explicitly defer stage 1's required test-shard acceptance. Only the new notes file is present in this repository's changes; the server implementation and reported build results could not be independently reviewed here.

- **medium** [P2] Complete stage 1's test-shard acceptance before marking it done (`notes\cc-P634-build-town-houses.md:66`)
  P409's L1 acceptance explicitly requires creating a Britain site on the test shard and checking invisible-multi rendering, doors and lockdowns in the client. This note instead confirms that no shard was started and moves those checks into Draft A. The serializer and synthetic-region tests do not verify these integration behaviors, so the requested smallest playable slice remains unverified. Run and record L1's test-shard acceptance before declaring P634 complete.

(0.8 minutes, 121,010 tokens)
