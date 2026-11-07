#!/usr/bin/env bash
# Inside the container: the real Pets sources and facts, first without the AOS patch, then each mutant over them. One line each.
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/Pets Projects/UOContent.Tests/Tests/Mobiles
cp /m/t/Mobiles/HorseBardingVerification.cs /m/t/Mobiles/PetPerchVerification.cs Projects/UOContent.Tests/Tests/Mobiles/
F='FullyQualifiedName~HorseBardingVerification|FullyQualifiedName~PetPerchVerification'
run() {
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "== $1: DID NOT COMPILE: $errs"; return; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$F" --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*Verification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $1: ${fails:-NONE RED}"
}
cp /m/c/Pets/*.cs $U/Pets/
run nopatch
sed 's/\r$//' /m/p/AOS-horse-barding.patch | patch -p1 --fuzz=0 --no-backup-if-mismatch >/dev/null || echo PATCH-FAILED
for d in /m/mut/*/; do
  cp /m/c/Pets/*.cs $U/Pets/
  cp "$d"*.cs $U/Pets/
  run "$(basename "$d")"
done
cp /m/c/Pets/*.cs $U/Pets/
run real
