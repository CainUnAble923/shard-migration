#!/usr/bin/env bash
# cc-P741 probe (P732 and P728s, cut down): the code copy's Tutorial customizations and Tutorial tests over sl-uo-builder's copies
# (an image with P728's PlayerMobile patch built in); runs the tests matching $1. Usage: probe.sh <filter> [image].
# SRC (default: the code copy's customizations) may point at a mutant copy.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P738}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
