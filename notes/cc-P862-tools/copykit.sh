#!/usr/bin/env bash
# cc-P862: copy P867's proof kit (Iron's own, origin/golem/Iron/P867 notes/cc-P867-tools/kit) into kit/ here and point
# its tool paths at this folder.
cd D:/UO/golems/Iron/shard-migration
K=notes/cc-P862-tools/kit
mkdir -p "$K"
for f in make_create_bin.py proof-shard.ps1 run-tazuo.ps1 tazuo-walk.ps1 ui.ps1; do
  git show "origin/golem/Iron/P867:notes/cc-P867-tools/kit/$f" > "$K/$f"
  sed -i 's/cc-P867-tools/cc-P862-tools/g' "$K/$f"
done
grep -n "cc-P8[0-9][0-9]" "$K"/*.ps1 "$K"/*.py | grep -v "cc-P862" | head
ls -la "$K"
