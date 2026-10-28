"""cc-P676: register RegionJsonSerializer-shard-maps.patch in apply-patches.sh and copy regions-trammel.json into the
builder's Distribution/Data/ShatteredLegacy in the Dockerfile (beside townsfolk-talk.json)."""
import os

BS = chr(92)
REPO = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy'])


def edit(rel, old, new):
    p = os.path.join(REPO, rel)
    s = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(old) == 1, (rel, s.count(old))
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
    print('ok', rel)


edit('docker/uo/apply-patches.sh',
     'apply_patch "$PATCHES/GuardedRegion-witness-observe.patch"\n',
     'apply_patch "$PATCHES/GuardedRegion-witness-observe.patch"\n'
     '# cc-P676 (SoS swap S3): Trammel\'s regions on the Siege of Sosaria land. LoadRegions reads pinned\'s\n'
     '# Data/regions.json whole and registers each region as it is read, so a data file cannot replace one map\'s\n'
     '# regions without this: Data/ShatteredLegacy/regions-<map>.json takes the place of pinned\'s regions of each map it\n'
     '# names, and every other map keeps pinned\'s. The alternative, a merged copy of pinned\'s whole regions.json in the\n'
     '# repo, would hide upstream\'s region changes. Argued in shard-migration notes/cc-P676-sos-trammel-regions.md;\n'
     '# pinned by SosTrammelRegionsVerification.\n'
     'apply_patch "$PATCHES/RegionJsonSerializer-shard-maps.patch"\n')

edit('docker/uo/Dockerfile',
     'COPY server/data/townsfolk-talk.json /build/modernuo/Distribution/Data/ShatteredLegacy/townsfolk-talk.json\n',
     'COPY server/data/townsfolk-talk.json /build/modernuo/Distribution/Data/ShatteredLegacy/townsfolk-talk.json\n'
     '# cc-P676 (SoS swap S3): Trammel\'s regions on the SoS land, read by RegionJsonSerializer-shard-maps.patch in place of\n'
     '# pinned\'s Trammel regions (made by shard-migration notes/cc-P676-tools/gen_regions.py).\n'
     'COPY server/data/regions-trammel.json /build/modernuo/Distribution/Data/ShatteredLegacy/regions-trammel.json\n')
