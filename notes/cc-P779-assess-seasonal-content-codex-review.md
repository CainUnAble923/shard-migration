# Codex review: P779

CC task P779: assess seasonal content for festival stores and boxes. Reviewed by Codex (`codex exec review`, read-only) after P779 DONE and before the Golem's commit, 2026-11-02 19:55.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The note broadly supplies the requested assessments and ranked recommendations, but its saved-type counts and art evidence are materially inaccurate. Those errors affect port sizing and the proposed prerequisite check.

- **medium** [P2] Correct the art evidence and check the complete ID set (`notes\cc-P779-assess-seasonal-content.md:107`)
  The cited tiledata file does not name these IDs ship hulls: decoding its 64-bit-flags format yields `lamp_blood` at 0x9DE7, `wall_christmas_bells` at 0x9DC0, and `sculpture_wood_valor` at 0x9E80. Also, the package includes later-year art beyond the stated range, including PrideSculpture's lit ID 42153 (0xA4A9). Correct the lookup and enumerate all constructor, flip and lit/unlit IDs before defining the follow-up art gate; the current sketch checks only 0x9DE7???0x9E80 before authorizing all 64 pieces. Actual client rendering can remain explicitly unverified.
- **medium** [P2] Recount saved types without counting archive copies (`notes\cc-P779-assess-seasonal-content.md:105`)
  The requested sizing understates serialization work: each Artisan file declares 16 serializable classes, not 4; the Halloween package has 10 saved types, not 7, because its three addons also declare deeds; and the swamp package has 6, not 5. Conversely, ChristmasGift.cs has 196 lines and one saved type???the reported 392/2 counts its `_zips` copy twice. Recount the distinct source files and publish their filenames alongside the counts, as required by [AGENTS.md:61???65](../AGENTS.md#L61-L65), so Chase can use these estimates to scope ports.

(2 minutes, 591,620 tokens)
