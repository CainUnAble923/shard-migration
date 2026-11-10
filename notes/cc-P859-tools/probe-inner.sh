#!/usr/bin/env bash
# cc-P859: inside a builder image. Install the horn, Mister Gobbles, the store row, the Clean Up Britannia row and the facts,
# then run them. With RED=stub, the stubs replace the horn and Mister Gobbles and the image's store and CUB files stay.
cd /build/modernuo
U=Projects/UOContent
T=Projects/UOContent.Tests/Tests
mkdir -p $U/Items/Thanksgiving
cp /m/t/Misc/HornOfPlentyVerification.cs /m/t/Misc/RewardStoreVerification.cs $T/Misc/
cp /m/t/Services/CleanUpBritanniaPointsVerification.cs $T/Services/
if [ -n "${RED:-}" ]; then
  cp /m/red/$RED/HornOfPlenty.cs $U/Items/Thanksgiving/; cp /m/red/$RED/MisterGobbles.cs $U/Mobiles/Normal/; echo "== RED: $RED"
else
  cp /m/c/Items/Thanksgiving/HornOfPlenty.cs $U/Items/Thanksgiving/
  cp /m/c/Mobiles/Normal/MisterGobbles.cs $U/Mobiles/Normal/
  cp /m/c/RewardStores/AchievementStore.cs $U/RewardStores/
  cp /m/c/Services/PointsSystems/CleanUpBritanniaData.cs $U/Services/PointsSystems/
fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -20
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "FullyQualifiedName~HornOfPlentyVerification|FullyQualifiedName~RewardStoreVerification|FullyQualifiedName~CleanUpBritanniaPointsVerification" \
  --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1; grep -A12 'Failed ShatteredLegacy' /tmp/t.txt | head -80; grep -E '^\s+(Failed|Passed) ShatteredLegacy|Total tests|Passed:|Failed:' /tmp/t.txt | sed -E 's/^\s+//' | grep -vE '^Passed ShatteredLegacy' | head -60
