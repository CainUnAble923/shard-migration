#!/usr/bin/env bash
# cc-P687 probe: the code copy's fence region and its facts over sl-uo-builder's copies; runs the tests matching $1.
# FENCE (default: the code copy's SosFenceRegions.cs) may point at a mutant copy (a red run).
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P685}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
FENCE="${FENCE:-$CODE/customizations/Regions/SosFenceRegions.cs}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$FENCE:$UC/Regions/SosFenceRegions.cs:ro" \
  -v "$CODE/tests/Regions/SosFenceRegionsVerification.cs:$UT/Regions/SosFenceRegionsVerification.cs:ro" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
