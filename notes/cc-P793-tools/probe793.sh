#!/usr/bin/env bash
# cc-P793 probe (P764's method): a mutant's Peacock files, ShardBodyTypes.cs and shrink.json, and the code copy's facts,
# over sl-uo-builder:cc-p793's copies; runs the tests matching $1, $3 times (default 1).
# Usage: SRC=<mutant folder> probe793.sh <filter> [image] [times]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p793}"
TIMES="${3:-1}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=()
if [ -n "$SRC" ]; then
  M+=(-v "$SRC/Mounts/Peacock.cs:$UC/Mobiles/Mounts/Peacock.cs")
  M+=(-v "$SRC/Mounts/PeacockTable.cs:$UC/Mobiles/Mounts/PeacockTable.cs")
  M+=(-v "$SRC/Mounts/PeacockSystem.cs:$UC/Mobiles/Mounts/PeacockSystem.cs")
  M+=(-v "$SRC/ShardBodyTypes.cs:$UC/Mobiles/Evo/ShardBodyTypes.cs")
  M+=(-v "$SRC/shrink.json:/build/modernuo/Distribution/Data/ShatteredLegacy/shrink.json")
  # the tests read the copy beside their own build, and a build does not copy a mount older than it
  M+=(-v "$SRC/shrink.json:/build/modernuo/Projects/UOContent.Tests/bin/Release/net10.0/Data/ShatteredLegacy/shrink.json")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  "${M[@]}" \
  -v "$CODE/tests/Mobiles/Mounts/PeacockVerification.cs:$UT/Mobiles/Mounts/PeacockVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; for i in \$(seq 1 $TIMES); do dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning; done"
