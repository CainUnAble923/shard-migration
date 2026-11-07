#!/usr/bin/env bash
# Inside the container: the real sources and facts, then each mutant over them, and back. One line each.
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/StaffBuildTools
cp /m/t/Misc/StaffBuildToolsVerification.cs Projects/UOContent.Tests/Tests/Misc/
F='FullyQualifiedName~StaffBuildToolsVerification'
real() { cp /m/c/StaffBuildTools/*.cs $U/StaffBuildTools/; cp /m/c/ClusterFVisualBuilder.cs $U/Misc/; }
run() {
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "== $1: DID NOT COMPILE: $errs"; return; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$F" --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*Verification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $1: ${fails:-NONE RED}"
}
for d in /m/mut/*/; do
  real
  for f in "$d"*.cs; do if [ "$(basename $f)" = ClusterFVisualBuilder.cs ]; then cp $f $U/Misc/; else cp $f $U/StaffBuildTools/; fi; done
  run "$(basename "$d")"
done
real
run real
