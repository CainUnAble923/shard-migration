#!/usr/bin/env bash
# cc-P814: each fix put back in the builder image's tree, the new facts run, in throwaway containers. Writes red.txt.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P814-tools
OUT="$T/red.txt"
: > "$OUT"
run() { # name image sed-expression file
  echo "== $1" >> "$OUT"
  MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= "$2" bash -c "cd /build/modernuo
sed -i -E '$3' Projects/UOContent/Tutorial/$4
touch Projects/UOContent/Tutorial/$4
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter 'FullyQualifiedName~HavenSignTileVerification|FullyQualifiedName~NewHavenFixesVerification' --logger 'console;verbosity=normal' 2>&1 | grep -E '^\s+Failed ShatteredLegacy|Total tests:|^\s+Passed:|^\s+Failed:' | sed -E 's/ \[.*//'" >> "$OUT" 2>&1
}
run 'clean, release' sl-uo-builder:cc-p814-isle 's/xxnothingxx//' NewHavenLessons.cs
run 'release: stop 1 sign back on the bench' sl-uo-builder:cc-p814-isle 's/Point3D\(3471, 2588, 0\)/Point3D(3469, 2589, 0)/' NewHavenLessons.cs
run 'release: old sign not taken away' sl-uo-builder:cc-p814-isle 's/if \(!dryRun\) \{ item\.Delete\(\); \}/if (false) { item.Delete(); }/' NewHavenLessons.cs
run 'release: stop 1 three tiles from its sign' sl-uo-builder:cc-p814-isle 's/Ground\(3470, 2590\)/Ground(3468, 2591)/' NewHavenLessons.cs
run 'main: stables sign back under the eave' sl-uo-builder:cc-p814 's/Point3D\(3609, 2614, 0\)/Point3D(3608, 2614, 0)/' NewHavenLessons.cs
echo finished >> "$OUT"
