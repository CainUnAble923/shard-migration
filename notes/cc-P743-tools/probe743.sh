#!/usr/bin/env bash
# cc-P743 (P714's probe714.sh shape): this branch's tutorial customizations and tests over sl-uo-builder's patched tree,
# with PlayerMobile.cs patched by PlayerMobile-private-mobile.patch; runs the tests matching $1.
#     bash probe743.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P753}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
APPLIED="${APPLIED:-C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-golems-Iron-shard-migration/6d4e7b5a-5442-4beb-9baa-2b87f19155fe/scratchpad/p743/applied/Projects/UOContent}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC/Tutorial:$UC/Tutorial" -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$APPLIED/Mobiles/PlayerMobile.cs:$UC/Mobiles/PlayerMobile.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
