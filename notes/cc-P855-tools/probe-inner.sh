#!/usr/bin/env bash
# cc-P855: inside a builder image. Install the copy's ShardDecor addon, store rows, data and facts, then run them. With
# RED=<mutant>, red/<mutant>/ShardDecorAddon.cs replaces the addon and the image's own store files stay (the data is installed).
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/Items/Addons/ShardDecor
cp /m/t/ShardDecorAddonVerification.cs /m/t/LeagueShopVerification.cs /m/t/RewardStoreVerification.cs Projects/UOContent.Tests/Tests/Misc/
if [ -n "${RED:-}" ]; then
  cp /m/red/$RED/ShardDecorAddon.cs $U/Items/Addons/ShardDecor/; echo "== RED mutant: $RED"
  mkdir -p Distribution/Data/ShatteredLegacy/Decoration/Addons; cp /m/d/*.cfg Distribution/Data/ShatteredLegacy/Decoration/Addons/
else
  cp /m/c/Items/Addons/ShardDecor/ShardDecorAddon.cs $U/Items/Addons/ShardDecor/
  cp /m/c/LeagueShop/LeagueShop.cs $U/LeagueShop/
  cp /m/c/RewardStores/AchievementStore.cs /m/c/RewardStores/GuildStores.cs /m/c/RewardStores/FestivalStore.cs $U/RewardStores/
  mkdir -p Distribution/Data/ShatteredLegacy/Decoration/Addons; cp /m/d/*.cfg Distribution/Data/ShatteredLegacy/Decoration/Addons/
fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -20
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "FullyQualifiedName~ShardDecorAddonVerification|FullyQualifiedName~LeagueShopVerification|FullyQualifiedName~RewardStoreVerification" \
  --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1; grep -A12 'Failed ShatteredLegacy' /tmp/t.txt | head -60; cat /tmp/t.txt | grep -E '^\s+(Failed|Passed) ShatteredLegacy|Total tests|Passed:|Failed:|error|Assert|Expected|Actual' | sed -E 's/^\s+//' | grep -vE '^Passed ShatteredLegacy' | head -80
