#!/usr/bin/env bash
# cc-P803: each fix put back (a sed on one file inside a throwaway container), the new facts run. Writes red.txt.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P803-tools
OUT="$T/red.txt"; : > "$OUT"
REPO=D:/UO/golems/Iron/p803-isle; IMG=sl-uo-builder:isle12-20261107
STAGE=$(mktemp -d)
cd "$REPO"
for f in $(git status --porcelain | awk '{print $2}' | grep -E '^server/(customizations|tests)/.*\.cs$'); do
  case "$f" in
    server/customizations/*/*) d="Projects/UOContent/${f#server/customizations/}";;
    server/customizations/*) d="Projects/UOContent/Misc/${f#server/customizations/}";;
    server/tests/*) d="Projects/UOContent.Tests/Tests/${f#server/tests/}";;
  esac
  mkdir -p "$STAGE/$(dirname "$d")"; cp "$f" "$STAGE/$d"
done
W=$(cygpath -m "$STAGE")
run() { # name sed-expression file-in-tree
  echo "== $1" >> "$OUT"
  MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -v "$W:/stage:ro" "$IMG" bash -c "cd /build/modernuo
cp -r /stage/. .
sed -i -E '$2' $3
grep -c -E '$2' $3 >/dev/null; touch $3
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter 'FullyQualifiedName~LeagueOfficeDecorVerification' --logger 'console;verbosity=normal' 2>&1 | grep -E '^\s+Failed ShatteredLegacy|Total tests:|^\s+Passed:|^\s+Failed:' | sed -E 's/ \[.*//'" >> "$OUT" 2>&1
}
A=Projects/UOContent/Requisitions/Appraiser.cs
S=Projects/UOContent/Misc/ClusterFRegistrarOfficeSeeder.cs
L=Projects/UOContent/Misc/ClusterFRegistrarOfficeLayout.cs
run 'clean' 's/xxnothingxx//' $A
run 'board back on the front door tile' 's/1, 3458, 2598, 18, Direction.East/1, 3459, 2596, 18, Direction.East/' $A
run 'board keeps the north-wall art on a west wall' 's/OfficeBoardItemID = 0x1E5E/OfficeBoardItemID = 0x1E5F/' $A
run 'an old board is not moved' 's/if \(old == null\)/if (true)/' $A
run 'candelabra back on the east window tile' 's/0x0B26, "candelabra", 3461, 2601, 18/0x0B26, "candelabra", 3461, 2602, 18/g' $L
run 'office bookcase back to the east-facing case' 's/0x0A98, "bookcase", 3461, 2597, 18/0x0A99, "bookcase", 3461, 2597, 18/g' $L
run 'no upgrade on load' 's/var found = FindOfficeAddons\(\);\n?$/var found = FindOfficeAddons(); found.Clear();/' $S
echo finished >> "$OUT"
rm -rf "$STAGE"
