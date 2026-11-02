#!/usr/bin/env bash
# cc-P773 probe (P769's): a mutant's PlayTest folder and the code copy's P773 facts over sl-uo-builder:cc-p773's copies;
# builds UOContent, then the tests, then runs the tests matching $1 with --no-build (the image's UOContent.dll is
# otherwise reused: memory probe-env-mode-and-stale-uocontent).
# Usage: SRC773=<mutant customizations folder> probe773.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p773}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC773:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SRC/PlayTest:$UC/PlayTest" \
  -v "$CODE/tests/PlayTest:$UT/PlayTest" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
