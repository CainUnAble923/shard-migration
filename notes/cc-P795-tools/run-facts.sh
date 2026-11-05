#!/usr/bin/env bash
# cc-P795: the handbook facts over sl-uo-builder:cc-p794's patched tree, in one throwaway container: this copy's Drover code and
# facts, and the three patched sources. For quick red and green; the gate is the gated build.
# Usage: run-facts.sh <folder with Drover/ and the patched sources> <log> [filter]
set -u
SRC="$1"; LOG="$2"; FILTER="${3:-FullyQualifiedName~DroversHandbookVerification}"
TESTS="D:/UO/golems/Iron/ShatteredLegacy/server/tests/Drover"
B=/build/modernuo/Projects
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SRC/Drover:/m/Drover:ro" -v "$TESTS:/m/tests:ro" -v "$SRC/pat:/m/pat:ro" \
  sl-uo-builder:cc-p794 bash -c "cd /build/modernuo && mkdir -p $B/UOContent/Drover $B/UOContent.Tests/Tests/Drover
cp /m/Drover/*.cs $B/UOContent/Drover/; cp /m/tests/*.cs $B/UOContent.Tests/Tests/Drover/
cp /m/pat/Spellbook.cs.new '$B/UOContent/Items/Skill Items/Magical/Spellbook.cs'
cp /m/pat/AnimalTaming.cs.new $B/UOContent/Skills/AnimalTaming.cs
cp /m/pat/SBAnimalTrainer.cs.new $B/UOContent/Mobiles/Vendors/SBInfo/SBAnimalTrainer.cs
dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning" > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):| error ' "$LOG" | sed -E 's/\[\/build.*//' | sort -u | cut -c1-200 | head -30
