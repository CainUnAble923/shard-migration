#!/usr/bin/env bash
# Inside the container: the real StaffHub sources and facts, then each mutant over them, and back. One line each.
cd /build/modernuo
U=Projects/UOContent
cp /m/t/Misc/ColorWarsVerification.cs Projects/UOContent.Tests/Tests/Misc/
F='FullyQualifiedName~ColorWarsVerification'
run() {
  if ! dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q > /tmp/b.log 2>&1; then
    echo "== $1: DID NOT COMPILE: $(grep -E ' error ' /tmp/b.log | sort -u | head -2)"; return; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$F" --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*Verification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $1: ${fails:-NONE RED}"
}
for d in /m/mut/*/; do
  cp /m/c/StaffHub/*.cs $U/StaffHub/
  cp "$d"*.cs $U/StaffHub/
  run "$(basename "$d")"
done
cp /m/c/StaffHub/*.cs $U/StaffHub/
run real
