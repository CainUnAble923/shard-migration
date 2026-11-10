#!/usr/bin/env bash
# cc-P856: inside a builder image. Install the copy's winter set (WinterSet/), the seeder, the Festival store and the
# facts, then run them. With RED=<mutant>, red/<mutant>/ holds the files that replace the copy's (the code before the
# change, with only what the facts need to compile).
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/WinterSet
cp /m/t/WinterSetVerification.cs /m/t/WinterDecorVerification.cs /m/t/RewardStoreVerification.cs Projects/UOContent.Tests/Tests/Misc/
cp /m/c/WinterSet/*.cs $U/WinterSet/
cp /m/c/ClusterFWinterDecorSeeder.cs $U/Misc/
cp /m/c/RewardStores/FestivalStore.cs $U/RewardStores/
if [ -n "${RED:-}" ]; then
  echo "== RED mutant: $RED"
  rm -f $U/WinterSet/*.cs
  cp /m/red/$RED/WinterSet/*.cs $U/WinterSet/
  cp /m/red/$RED/ClusterFWinterDecorSeeder.cs $U/Misc/
  cp /m/red/$RED/FestivalStore.cs $U/RewardStores/
fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1; grep -E 'CS8785|CS8784|[Gg]enerator|WinterSet' /tmp/b.txt | sort -u | head -8; grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -5
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "FullyQualifiedName~WinterSetVerification|FullyQualifiedName~WinterDecorVerification|FullyQualifiedName~RewardStoreVerification" \
  --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1; grep -A10 'Failed ShatteredLegacy' /tmp/t.txt | head -80; grep -E 'Total tests|Passed:|Failed:' /tmp/t.txt
