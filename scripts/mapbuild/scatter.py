"""Seeded, weighted placement (cc-P180): clusters with gaps, mixed pieces, never two identical pieces side by side.
One random.Random per zone, seeded from the rules file, so a rebuild with the same seed is the same map."""


def hx(v):
    return int(v, 16) if isinstance(v, str) else int(v)


def weighted(rng, table):
    """One id drawn from {"0x..": weight} (or {int: weight})."""
    ids = [hx(k) for k in table]
    return rng.choices(ids, weights=[table[k] for k in table])[0]


def pick_unlike(rng, table, c, by_tile, tries=8):
    """A weighted draw that avoids the ids already on the 8 neighbouring tiles (no two identical pieces side by side)."""
    x, y = c
    near = set()
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            near.update(by_tile.get((x + a, y + b), []))
    tid = weighted(rng, table)
    for _ in range(tries):
        if tid not in near:
            break
        tid = weighted(rng, table)
    if tid in near:
        # the weighted draws kept colliding (few ids, a dense cluster): take any id clear of the 8 neighbours, else
        # any clear of the 4 orthogonal ones, so identical pieces never touch side by side
        ids = [hx(k) for k in table]
        orth = set()
        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            orth.update(by_tile.get((x + a, y + b), []))
        free = [i for i in ids if i not in near] or [i for i in ids if i not in orth]
        if free:
            tid = rng.choice(free)
    return tid


def scatter(rng, rule, eligible, taken, by_tile, put, roomy, impassable, decor_blocked):
    """Clusters with gaps: cluster centres at least rule['spacing'] apart, each with rule['cluster'] = [min, max]
    pieces within rule['radius'] (Chebyshev), ids by weight from rule['ids'] and never equal to a neighbour's, z from
    rule['z']. Density: rule['count'] clusters, or rule['density'] clusters per eligible tile. An impassable piece
    goes only where roomy(tile) is true and is recorded in decor_blocked; put(x, y, id, why, z=...) places."""
    elig = [c for c in eligible if c not in taken]
    eligset = set(elig)
    n = rule.get("count") or int(round(len(elig) * rule["density"]))
    spacing, radius, size = rule.get("spacing", 3), rule.get("radius", 1), rule.get("cluster", [1, 1])
    rng.shuffle(elig)
    centres = []
    for c in elig:
        if len(centres) >= n:
            break
        if all(max(abs(c[0] - o[0]), abs(c[1] - o[1])) >= spacing for o in centres):
            centres.append(c)
    for c in centres:
        k = rng.randint(size[0], size[1])
        cand = [(c[0] + a, c[1] + b) for a in range(-radius, radius + 1) for b in range(-radius, radius + 1) if (a, b) != (0, 0)]
        cand = [t for t in cand if t in eligset and t not in taken]
        rng.shuffle(cand)
        for t in [c] + cand[:k - 1]:
            if t in taken:
                continue
            tid = pick_unlike(rng, rule["ids"], t, by_tile)
            if impassable(tid):
                if not roomy(t):
                    continue
                decor_blocked.add(t)
            put(t[0], t[1], tid, rule["name"], z=rng.choice(rule.get("z", [0])))
            taken.add(t)
