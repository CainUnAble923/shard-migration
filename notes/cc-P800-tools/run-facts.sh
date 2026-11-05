#!/usr/bin/env bash
# cc-P800 (P795's): the sash facts over a builder image's patched tree, in one throwaway container, with this copy's changed sources
# and the facts. For quick red and green; the gate is the gated build.
# Usage: run-facts.sh <builder image> <log> [filter] [customizations folder]
set -u
IMG="$1"; LOG="$2"; FILTER="${3:-FullyQualifiedName~LeagueSashVerification}"
CUST="${4:-D:/UO/golems/Iron/ShatteredLegacy/server/customizations}"
TESTS="D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc"
U=Projects/UOContent
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$CUST:/m/c:ro" -v "$TESTS:/m/t:ro" "$IMG" bash -c "cd /build/modernuo
cp /m/c/ClusterFAchievements.cs /m/c/LeagueRegistrarGump.cs $U/Misc/
cp /m/c/LeagueShop/LeagueSash.cs /m/c/LeagueShop/LeagueShop.cs $U/LeagueShop/
cp /m/c/LootBoxes/LootBoxItems.cs /m/c/LootBoxes/LootBoxRoller.cs $U/LootBoxes/
cp /m/c/Requisitions/RequisitionSystem.cs $U/Requisitions/
[ -f $U/Requisitions/LeagueHunts.cs ] && cp /m/c/Requisitions/LeagueHunts.cs $U/Requisitions/
cp /m/c/Tutorial/ClusterFLoops.cs $U/Tutorial/
cp /m/t/LeagueSashVerification.cs Projects/UOContent.Tests/Tests/Misc/
dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning" > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+(Passed|Failed) | error |Assert\.|Expected:|Actual:|Exception' "$LOG" | sed -E 's/\[\/build.*//' | sort -u | cut -c1-220 | head -50
