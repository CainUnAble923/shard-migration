#!/usr/bin/env bash
# cc-P675 probe (P678's probe.sh): this prompt's tests, and its code or the red stub, bind-mounted over a builder image.
#   MODE=green|red DATA=sos|stock|none IMAGE=<builder> probe.sh <filter>
# green: server/customizations/Fold and /Maps from the code copy. red: the image's own Fold code and red-stub/Maps.
# sos: the vanilla client with the server's map overlay (map1LegacyMUL.uop, statics1.mul, staidx1.mul) mounted over it,
# as dataDirectories puts the overlay first. stock: the vanilla client alone. none: no client data (the gate's host).
set -u
FILTER="$1"
MODE="${MODE:-green}"
DATA="${DATA:-sos}"
IMAGE="${IMAGE:-sl-uo-builder:cc-P681}"
CODE="${CODE:-D:/UO/golems/Iron/ShatteredLegacy/server}"
HERE="$(cd "$(dirname "$0")" && pwd -W)"
OVERLAY="${OVERLAY:-C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-golems-Iron-shard-migration/010b2204-7c4d-4613-86c5-8288f972be7b/scratchpad/overlay}"
EA=D:/UO/UltimaOnlineVanilla
C="$CODE/customizations"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
args=(-v "$CODE/tests/Regions/FoldVerification.cs:$UT/Regions/FoldVerification.cs"
      -v "$CODE/tests/Misc/SosMapsVerification.cs:$UT/Misc/SosMapsVerification.cs"
      -v "$CODE/tests/Misc/MapCheckRealDataVerification.cs:$UT/Misc/MapCheckRealDataVerification.cs")
if [ "$MODE" = green ]; then
  args+=(-v "$C/Fold:$UC/Fold" -v "$C/Maps:$UC/Maps")
else
  args+=(-v "$HERE/red-stub/Maps:$UC/Maps")
fi
case "$DATA" in
  sos) args+=(-v "$EA:/clientdata:ro" -e MODERNUO_TEST_DATA_DIR=/clientdata
              -v "$OVERLAY/map1LegacyMUL.uop:/clientdata/map1LegacyMUL.uop:ro"
              -v "$OVERLAY/statics1.mul:/clientdata/statics1.mul:ro"
              -v "$OVERLAY/staidx1.mul:/clientdata/staidx1.mul:ro") ;;
  stock) args+=(-v "$EA:/clientdata:ro" -e MODERNUO_TEST_DATA_DIR=/clientdata) ;;
  none) ;;
esac
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${args[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
