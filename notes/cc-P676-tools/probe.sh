#!/usr/bin/env bash
# cc-P676 probe (P675's probe.sh): this prompt's facts over a builder image, with its loader and data bind-mounted.
#   MODE=green|red IMAGE=<builder> probe.sh <filter>
# green: the patched RegionJsonSerializer.cs (p676-work/patch/b) and server/data/regions-trammel.json in the builder's
#        Distribution/Data/ShatteredLegacy. red: red-stub/RegionJsonSerializer.cs (MergeShardRegions returns pinned's
#        list unchanged) and no data file, as before this prompt.
set -u
FILTER="$1"
MODE="${MODE:-green}"
IMAGE="${IMAGE:-sl-uo-builder:cc-P720}"
CODE="${CODE:-D:/UO/golems/Iron/ShatteredLegacy/server}"
HERE="$(cd "$(dirname "$0")" && pwd -W)"
SER=/build/modernuo/Projects/Server/Regions/RegionJsonSerializer.cs
UT=/build/modernuo/Projects/UOContent.Tests/Tests
args=(-v "$CODE/tests/Regions/SosTrammelRegionsVerification.cs:$UT/Regions/SosTrammelRegionsVerification.cs")
if [ "$MODE" = green ]; then
  args+=(-v "D:/UO/golems/Iron/p676-work/patch/b/Projects/Server/Regions/RegionJsonSerializer.cs:$SER"
         -v "$CODE/data/regions-trammel.json:/build/modernuo/Distribution/Data/ShatteredLegacy/regions-trammel.json:ro")
else
  args+=(-v "$HERE/red-stub/RegionJsonSerializer.cs:$SER")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${args[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
