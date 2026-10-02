#!/usr/bin/env bash
# cc-P30 patch survey. Applies the 30 apply_patch lines of apply-patches.sh, in file order,
# cumulatively, to a fresh export of a ModernUO commit, exactly as the gate does
# (-p1 --forward --ignore-whitespace --batch), first at --fuzz=0 then at --fuzz=3.
# Also diffs every full-file replacement target between pinned and the target commit.
#
# Usage: patch-survey.sh <modernuo-clone> <commit> <workdir>
# Reads D:\ShatteredLegacy read-only. Writes only under <workdir>.
set -uo pipefail
CLONE="$1"; COMMIT="$2"; WORK="$3"
SL=/d/ShatteredLegacy
PIN=7c9215d97
TREE="$WORK/tree-$COMMIT"
rm -rf "$TREE"; mkdir -p "$TREE"
git -C "$CLONE" archive "$COMMIT" | tar -x -C "$TREE"

PATCHDIR="$WORK/patches-lf"
rm -rf "$PATCHDIR"; mkdir -p "$PATCHDIR"
cp "$SL"/server/patches/*.patch "$PATCHDIR/"
sed -i 's/\r$//' "$PATCHDIR"/*.patch

cd "$TREE"
n=0
grep '^apply_patch "' "$SL/docker/uo/apply-patches.sh" | sed 's/.*PATCHES\/\(.*\)".*/\1/' | while read -r name; do
    n=$((n+1))
    f="$PATCHDIR/$name"
    targets=$(grep '^+++ ' "$f" | awk '{print $2}' | sed 's#^b/##' | tr '\n' ' ')
    if out=$(patch -p1 --forward --ignore-whitespace --fuzz=0 --batch --dry-run < "$f" 2>&1); then
        patch -p1 --forward --ignore-whitespace --fuzz=0 --batch < "$f" >/dev/null
        res="CLEAN"
        if echo "$out" | grep -q 'offset'; then res="CLEAN(offset)"; fi
    elif out3=$(patch -p1 --forward --ignore-whitespace --fuzz=3 --batch --dry-run < "$f" 2>&1); then
        patch -p1 --forward --ignore-whitespace --fuzz=3 --batch < "$f" >/dev/null
        res="FUZZ"
        out="$out3"
    else
        res="FAIL"
        out="$out3"
    fi
    printf '%02d\t%s\t%s\t%s\n' "$n" "$name" "$res" "$targets"
    printf '%s\n' "$out" | sed 's/^/        | /' >> "$WORK/survey-detail-$COMMIT.txt"
    echo "== $n $name $res" >> "$WORK/survey-detail-$COMMIT.txt"
done

echo
echo "== full-file replacement targets: lines changed upstream between $PIN and $COMMIT"
for p in \
  "Projects/UOContent/Engines/Character Creation/CharacterCreation.cs" \
  "Projects/UOContent/Engines/Craft/Core/CraftItem.cs" \
  "Projects/UOContent/Engines/Craft/Core/CraftContext.cs" \
  "Projects/UOContent/Items/New Haven Quest Rewards/HammerOfHephaestus.cs" \
  "Projects/UOContent/Skills/Meditation.cs" \
  "Projects/UOContent/Engines/Harvest/Mining.cs" \
  "Projects/UOContent/Mobiles/Vendors/NPC/Guildmasters/BaseGuildmaster.cs" \
  "Projects/UOContent/Engines/Bulk Orders/BulkMaterialType.cs" \
  "Projects/UOContent/Engines/Bulk Orders/LargeSmithBOD.cs" \
  "Projects/UOContent/Items/New Haven Quest Rewards/JacobsPickaxe.cs" \
  "Projects/UOContent/Misc/RegenRates.cs" \
  "Projects/UOContent/Misc/ResourceInfo.cs" \
  "Projects/UOContent/Engines/Harvest/Lumberjacking.cs" ; do
    if [ ! -f "$TREE/$p" ]; then echo "MISSING-AT-TARGET  $p"; continue; fi
    stat=$(git -C "$CLONE" diff --shortstat "$PIN" "$COMMIT" -- "$p")
    commits=$(git -C "$CLONE" log --format='%h' "$PIN..$COMMIT" -- "$p" | tr '\n' ' ')
    echo "${stat:- unchanged}  | $p | $commits"
done
