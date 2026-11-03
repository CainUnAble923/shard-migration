#!/usr/bin/env bash
# cc-P788 probe: runs the tests matching $1 in the isle release's builder image (sl-uo-builder:cc-p788-isle, the resolved
# release built green) with the encounter source swapped for the mutant in mutant/ when PROBE_MODE=mutant.
# UOContent is built, then the test project, and the run uses that build.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p788-isle}"
MODE="${PROBE_MODE:-mutant}"
HERE="D:/UO/golems/Iron/shard-migration/notes/cc-P788-tools"
UC=/build/modernuo/Projects/UOContent
M=()
if [ "$MODE" = mutant ]; then
  M+=(-v "$HERE/mutant/ClusterFEncounters.cs:$UC/Encounters/ClusterFEncounters.cs")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && grep -c 'P788 MUTANT' $UC/Encounters/ClusterFEncounters.cs; dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -20 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -20 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
