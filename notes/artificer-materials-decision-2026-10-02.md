# Artificers: imbuing materials and currency (Chase, 2026-10-02, 11:41)

Recorded by the overseer from the P29 testing conversation. For the features chat to enter in `docs\feature-queue.md`
(it owns that file) and for a later prompt.

- **Imbuing materials become OSI's three physical tiers:** Magical Residue, Enchanted Essence, Relic Fragment, from
  unraveling, spent by imbuing, as OSI does. They replace the "Essence Shards" balance as the imbuing material
  (today a number in `GuildCurrency["artificers"]`, shown on the Imbuing Table).
- **The Artificers get a new currency of their own: Artificer's Marks** (Chase, 12:02), separate from the materials.
  **For now it buys from an Artificers' shop**, the way Smith Seals buy from the Seal catalog. What earns Marks and
  what the shop stocks: open, for the features chat and a later brief.
- Fact found 2026-10-02: the three item types already exist in ours, as ported quest items
  (`server\customizations\Items\Quest\MagicalResidue.cs`, `EnchantedEssence.cs`, `RelicFragment.cs`, each
  `Item, ICommodity`). Pinned has none of them. Whether they are reachable today, and how OSI's unravel decides which
  tier an item yields, is for the brief to check.
- Context: this moves imbuing closer to OSI. Physical materials work with F-11's pack-then-bank costs as built.
- Open questions for Chase: what earns Marks and what the shop sells; whether OSI's unravel tiering (by item intensity) is used
  as is; Smith Seals and Mining Vouchers stay balances unless Chase says otherwise; existing shard balances are
  cleared at the fresh world.
