#!/usr/bin/env bash
# Inside the container: the real sources, then each mutant over them, and back. One line per mutant.
cd /build/modernuo
U=Projects/UOContent
install_real() {
mkdir -p $U/Mobiles/ClockworkScavenger; cp /m/c/Mobiles/ClockworkScavenger/*.cs $U/Mobiles/ClockworkScavenger/
cp /m/c/Mobiles/Mule/MuleModuleData.cs $U/Mobiles/Mule/
cp /m/c/ClusterFGuildmasterExtension.cs $U/Misc/
}
install_real
cp /m/t/Mobiles/ClockworkScavengerVerification.cs Projects/UOContent.Tests/Tests/Mobiles/
for d in /m/mut/*/; do
  name=$(basename "$d"); target=$(cat "$d/target")
  install_real
  cp "$d/$target" "$U/$target"
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "== $name: DID NOT COMPILE: $errs"; continue; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter 'FullyQualifiedName~ClockworkScavengerVerification' --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*ClockworkScavengerVerification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $name: ${fails:-NONE RED}"
done
