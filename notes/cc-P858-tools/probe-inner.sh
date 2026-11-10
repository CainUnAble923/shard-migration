#!/usr/bin/env bash
# cc-P858: inside a builder image. Install the copy's lamps, wagon and the two stores, and the facts; RED overlays a red
# copy; then build and run.
cd /build/modernuo
U=Projects/UOContent
TT=Projects/UOContent.Tests/Tests
mkdir -p $U/ShardLamps $U/FestivalWagon $TT/P858
cp /m/c/Items/Lights/ShardLamps.cs $U/ShardLamps/
cp /m/c/FestivalWagon/*.cs $U/FestivalWagon/
cp /m/c/RewardStores/AchievementStore.cs /m/c/RewardStores/FestivalStore.cs $U/RewardStores/
cp /m/t/Items/LampsAndWagonVerification.cs /m/t/Misc/RewardStoreVerification.cs $TT/P858/
rm -f $TT/Misc/RewardStoreVerification.cs
if [ -n "${RED:-}" ]; then
  echo "== RED: $RED"
  [ -f /m/red/$RED/ShardLamps.cs ] && cp /m/red/$RED/ShardLamps.cs $U/ShardLamps/
  [ -d /m/red/$RED/FestivalWagon ] && rm -f $U/FestivalWagon/*.cs && cp /m/red/$RED/FestivalWagon/*.cs $U/FestivalWagon/
  for f in AchievementStore.cs FestivalStore.cs; do [ -f /m/red/$RED/$f ] && cp /m/red/$RED/$f $U/RewardStores/; done
fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -20
F=${FILTER:-"FullyQualifiedName~LampsAndWagonVerification|FullyQualifiedName~RewardStoreVerification"}
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$F" \
  --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
grep -E '^\s+(Passed|Failed) ShatteredLegacy' /tmp/t.txt | sort -u | sed 's/ \[.*//'
grep -A8 'Failed ShatteredLegacy' /tmp/t.txt | grep -v "^\s*at System" | head -80
grep -E '^\s+(Total tests|Passed|Failed):' /tmp/t.txt | head -3
