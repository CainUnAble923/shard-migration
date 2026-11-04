#!/usr/bin/env bash
# cc-P794: the route facts on the unmutated copy (_base) and each mutant (mutate794routes.py), over sl-uo-builder:cc-p794's
# copies, one container and one log each. The image is older than the mounts: all three route files, both test files and the
# shop test are mounted. Touching inside the container makes them newer than the image's build output.
# Usage: run-route-mutants.sh <mutants folder> <log folder> [mutant names]
set -u
MUT="$1"; LOGS="$2"; shift 2
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
FILTER='FullyQualifiedName~EtherealRoutesVerification|FullyQualifiedName~EveryMountHasItsRoute|FullyQualifiedName~TheStockIsF13sStarterTable'
mkdir -p "$LOGS"
if [ $# -gt 0 ]; then names="$*"; else names=$(ls "$MUT"); fi
for name in $names; do
  d="$MUT/$name"
  MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
    -v "$d/EtherealLooks.cs:$UC/Mobiles/Mounts/EtherealLooks.cs" \
    -v "$d/ClusterFAchievements.cs:$UC/Misc/ClusterFAchievements.cs" \
    -v "$d/LeagueShop.cs:$UC/LeagueShop/LeagueShop.cs" \
    -v "$CODE/tests/Mobiles/Mounts/EtherealRoutesVerification.cs:$UT/Mobiles/Mounts/EtherealRoutesVerification.cs" \
    -v "$CODE/tests/Mobiles/Mounts/RewardMountVerification.cs:$UT/Mobiles/Mounts/RewardMountVerification.cs" \
    -v "$CODE/tests/Misc/LeagueShopVerification.cs:$UT/Misc/LeagueShopVerification.cs" \
    sl-uo-builder:cc-p794 bash -c "cd /build/modernuo && touch Projects/UOContent/Mobiles/Mounts/EtherealLooks.cs; dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning" > "$LOGS/$name.log" 2>&1
  failed=$(grep -a -E '^\s+Failed ShatteredLegacy' "$LOGS/$name.log" | sed -E 's/^\s+Failed ShatteredLegacy\.Tests\.[A-Za-z]+\.//; s/\(.*$//; s/ \[.*$//' | sort -u | tr '\n' ';')
  echo "$name: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/$name.log" | tr -s ' ' | tr '\n' ' ') $(grep -a -c ' error ' "$LOGS/$name.log") errors | $failed"
done
