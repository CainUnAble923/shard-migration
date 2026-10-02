# PT-07 and PT-11: Chase's decisions (2026-10-02, 10:26)

Recorded by the overseer. Feeds cc-P32 (renumbered from a duplicate P30, 2026-10-02).

1. **PT-11, smith BODs: both paths on purpose.** Regular smiths keep giving and taking smith BODs and pay
   OSI's rewards; the Blacksmith Guildmaster pays Smith Seals. Reason (Chase): "guild master isnt everywhere
   smiths are". Nothing to remove. To do: confirm no deed can pay twice or dodge the guildmaster's limits
   through the other path, and register the two paths as a deviation.
2. **PT-07, spawner importer: patch it** ("if you think it needs it"). The overseer read pinned
   `UOContent/Commands/ImportSpawnersCommand.cs` 2026-10-02: the import deletes every existing spawner of the
   same type found by `map.GetItemsAt<BaseSpawner>(location)`, which matches on x,y and ignores z (cc-P17 1.2
   cites `Map.ItemEnumerator.cs:31`). Pinned's data stacks spawners at one x,y on z, z+1, z+2, so each later one
   deletes the one before. cc-P17 counted the loss: Trammel 136 of 2,137, Felucca 127 of 2,122, Ilshenar 27,
   Malas 13, Tokuno 39, Ter Mur 0. It needs the patch: the deletion is silent and cannot be undone by any
   setting. A one-comparison pinned patch, plus a re-run of spawner generation on the test world.
