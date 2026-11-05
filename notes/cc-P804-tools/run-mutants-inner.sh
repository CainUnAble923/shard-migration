#!/usr/bin/env bash
# Inside the container: the real sources, then each mutant over them, and back. Writes one line per mutant.
cd /build/modernuo
U=Projects/UOContent
for p in Skills-herbalism skills-json-herbalism FeatureFlagManager-skill-count Plants-herbalism-lane; do sed 's/\r$//' /m/p/$p.patch | patch -p1 --fuzz=0 --no-backup-if-mismatch >/dev/null || echo PATCH-FAILED $p; done
install_real() {
mkdir -p $U/Herbalism; cp /m/c/Herbalism/*.cs $U/Herbalism/
cp /m/c/ClusterFAchievements.cs /m/c/ClusterFGuildStarterPath.cs /m/c/ClusterFGuildSystem.cs $U/Misc/
cp '/m/c/Services/Plants/Raised Garden Beds/RaisedGardenPlantItem.cs' "$(find $U -name RaisedGardenPlantItem.cs)"
cp /m/c/Tutorial/TutorialTradeTrials.cs $U/Tutorial/
}
install_real
cp /m/t/Misc/HerbalismVerification.cs Projects/UOContent.Tests/Tests/Misc/
cp /m/t/Engines/Craft/CraftCeilingsVerification.cs Projects/UOContent.Tests/Tests/Engines/Craft/
for d in /m/mut/*/; do
  name=$(basename "$d"); target=$(cat "$d/target")
  install_real
  if [ "${target%%/*}" = Mound ]; then cp "$d/$target" "$(find $U -name RaisedGardenPlantItem.cs)"; else cp "$d/$target" "$U/$target"; fi
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "== $name: DID NOT COMPILE: $errs"; continue; fi
  cp Distribution/Data/skills.json Projects/UOContent.Tests/bin/Release/net10.0/Data/skills.json
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter 'FullyQualifiedName~HerbalismVerification' --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*HerbalismVerification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $name: ${fails:-NONE RED}"
done
