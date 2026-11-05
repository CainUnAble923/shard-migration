#!/usr/bin/env bash
# Inside the container: install the real sources, then each mutant over them, and restore.
cd /build/modernuo
U=Projects/UOContent
install_real() {
cp /m/c/ClusterFAchievements.cs /m/c/LeagueRegistrarGump.cs $U/Misc/
cp /m/c/LeagueShop/LeagueSash.cs /m/c/LeagueShop/LeagueShop.cs $U/LeagueShop/
cp /m/c/LootBoxes/LootBoxItems.cs /m/c/LootBoxes/LootBoxRoller.cs $U/LootBoxes/
cp /m/c/Requisitions/RequisitionSystem.cs /m/c/Requisitions/LeagueHunts.cs $U/Requisitions/
cp /m/c/Tutorial/ClusterFLoops.cs $U/Tutorial/
}
install_real
cp /m/t/LeagueSashVerification.cs Projects/UOContent.Tests/Tests/Misc/
for d in /m/mut/*/; do
  name=$(basename "$d"); target=$(cat "$d/target")
  install_real
  cp "$d/$target" "$U/$target"
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "== $name: DID NOT COMPILE: $errs"; continue; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter 'FullyQualifiedName~LeagueSashVerification' --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*LeagueSashVerification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $name: ${fails:-NONE RED}"
done
