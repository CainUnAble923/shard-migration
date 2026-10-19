"""mapbuild: the general parts of the Rootdeep map build (cc-P167, P180, P181), kept as a module so the next dungeon,
building or hole starts from tested code instead of a copy. Read notes/map-building-playbook.md first.

    uofiles    read and write the client map files (map uop land, statics mul, tiledata), the walkable-set gate
    walls      the wall rule measured on OSI buildings (notes/uo-wall-orientation.md), corners, doorway frames
    scatter    seeded weighted placement: clusters with gaps, no two identical pieces side by side
    isorender  an isometric renderer with the client's tile layout and sloped land
    survey     tools for studying OSI rooms: decoration files, corner and density survey, land grids
    audit      the land slope audit (ring steps, spikes) and the wall-piece check

Nothing here knows about the Burrows; notes/cc-P167-tools/build_burrows.py is the Rootdeep-specific driver.
ASCII only. Run scripts with python -P (the -I flag hides the user-site numpy and Pillow).
"""
