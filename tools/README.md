# Migration tools

Two converters carry real value across the migration. Neither is written yet.

## `spawner-json-to-xmlspawner`

Input: output of ModernUO's `[ExportSpawners]` command, serialized by `SpawnerJsonSerializer`.
Output: ServUO XmlSpawner XML.

This is what saves our spawn placement work. Write it **before** hand-placing anything in
ServUO. Reference the DTOs at `Projects/UOContent/Engines/Spawners/*.Dto.cs` on the MUO side
and `Scripts/Services/XmlSpawner/` on the ServUO side.

## `muo-accounts-to-servuo-xml`

A small exporter that runs inside ModernUO, walks accounts, and emits a ServUO-shaped
`Accounts/accounts.xml`.

Key detail: the SHA512 digests are byte-identical between the engines, but ServUO stores
`BitConverter.ToString` output (hyphenated hex, `A1-B2-C3`) and ModernUO stores unseparated
hex (`A1B2C3`). Insert a hyphen every two characters on the way out.

Only works for accounts hashed with SHA2. See the Phase 0 note in `../docs/migration-plan.md`.
