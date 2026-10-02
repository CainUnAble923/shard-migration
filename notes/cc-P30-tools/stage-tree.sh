#!/usr/bin/env bash
# cc-P30: reproduce the Dockerfile's builder-stage staging on a local tree, for fast compile iteration.
# Exports <commit> from <clone>, copies migrations as the Dockerfile does, then runs <sl-copy>'s own
# apply-patches.sh with its fixed container paths pointed at the local copy. Nothing outside <stage> is written.
#
# Usage: stage-tree.sh <modernuo-clone> <commit> <sl-copy> <stage>
# The authoritative run is still <sl-copy>/docker/uo/build.sh; this only shortens the compile loop.
set -euo pipefail
CLONE="$1"; COMMIT="$2"; SL="$3"; STAGE="$4"
rm -rf "$STAGE"; mkdir -p "$STAGE/modernuo"
git -C "$CLONE" archive "$COMMIT" | tar -x -C "$STAGE/modernuo"
mkdir -p "$STAGE/patches"
cp -r "$SL/server/patches/." "$STAGE/patches/"
cp -r "$SL/server/migrations/." "$STAGE/modernuo/Projects/UOContent/Migrations/"
sed -e "s#^PATCHES=/patches#PATCHES='$STAGE/patches'#" \
    -e "s#^CUSTOMIZATIONS=/customizations#CUSTOMIZATIONS='$SL/server/customizations'#" \
    -e "s#^TESTS=/tests#TESTS='$SL/server/tests'#" \
    -e "s#^REPO=/build/modernuo#REPO='$STAGE/modernuo'#" \
    -e 's/\r$//' "$SL/docker/uo/apply-patches.sh" > "$STAGE/apply-patches.local.sh"
bash "$STAGE/apply-patches.local.sh"
