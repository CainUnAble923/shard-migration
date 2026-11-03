#!/usr/bin/env bash
# cc-P787 probe (P785's): runs the tests matching $1 in the builder image of this branch's base (P786) with the
# beekeeping sources and test mounted over it. PROBE_MODE=red mounts the new test file alone (the code before the
# change); PROBE_MODE=green (default) mounts the change too: the Beekeeping folder (SRC=<dir> for a mutant) and
# Beekeeper.cs with Beekeeper-beekeeping.patch applied (Beekeeper.patched.cs here; VEND=<file> for another, as a mutant).
# PATCHCHECK=1 checks the patch itself with --fuzz=0. Touch mounted files first: a file older than the image build is
# not recompiled.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p786}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
HERE="D:/UO/golems/Iron/shard-migration/notes/cc-P787-tools"
SRC="${SRC:-$CODE/customizations/Beekeeping}"
VEND="${VEND:-$HERE/Beekeeper.patched.cs}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
if [ "${PATCHCHECK:-0}" = 1 ]; then
  MSYS_NO_PATHCONV=1 docker run --rm --network=none -v "$CODE/patches/Beekeeper-beekeeping.patch:/p.patch" "$IMAGE" \
    bash -c "cd /build/modernuo && patch -p1 -R --dry-run --fuzz=0 < /p.patch && echo REVERSE-OK-ALREADY-APPLIED || patch -p1 --dry-run --fuzz=0 < /p.patch"
  exit
fi
M=(-v "$CODE/tests/Misc/BeekeepingVerification.cs:$UT/Misc/BeekeepingVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC:$UC/Beekeeping" -v "$VEND:$UC/Mobiles/Vendors/NPC/Beekeeper.cs")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -40 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -40 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
