# cc-P54 Part A: XP curve against F-12's 22-step ladder (decided 2026-10-03). Not part of the server tree.
# Deterministic: no randomness. Run: python xp_ladder.py > xp_ladder_out.md
#
# Decided inputs (docs\feature-queue.md F-12, "Ladder and reserve" and "Echo (loop memory) starting shape"):
#   ladder: loop 0 cap 50, loop 1 cap 100, loops 2..21 add +5 (200 at loop 21)
#   level resets to 1 every loop, for everyone
#   reserve at max level = 25% of the XP from the current cap to the next one
#   base echo (levels already reached): x1.5 at loop 1, +0.5 per loop, top x10 at loop 18; level XP uses it for everyone
# Modeling choices (ours, stated in the notes):
#   - "levels already reached" in loop N = levels below the previous loop's cap (the player reached that cap last loop)
#   - P20's +20%-per-loop bonus is dropped: the echo replaces it (F-12 2026-10-03)
#   - XP per kill = 5 x creature level (P20); profiles A and B from P20; C is new (crafter/gatherer)
#   - the reserve is filled at max level at the base rate, and credited as raw XP at the start of the next loop
#     (from level 1, not multiplied by the echo again)
import math

LOOPS = list(range(22))
def cap(n): return 50 if n == 0 else 100 if n == 1 else 100 + 5 * (n - 1)
CAPS = [cap(n) for n in LOOPS]
assert CAPS[21] == 200 and CAPS[2] == 105 and len(CAPS) == 22

def echo(n): return 1.0 if n == 0 else min(1.0 + 0.5 * n, 10.0)
def keeper_echo(n): return 1.0 if n == 0 else 1.5 + (50.0 - 1.5) * (n - 1) / 20.0
assert echo(1) == 1.5 and echo(4) == 3.0 and echo(10) == 6.0 and echo(18) == 10.0 and echo(21) == 10.0
assert abs(keeper_echo(21) - 50) < 1e-9 and abs(keeper_echo(11) - 25.75) < 1e-9

RESERVE_FRACTION = 0.25
HOURS_PER_WEEK = 10.0
TARGET_LOOP0 = (3, 6, 10)            # hours
TARGET_CAPSTONE_MONTHS = (3, 6, 12)  # months at 10 h/week
WEEKS_PER_MONTH = 52.0 / 12.0

# ---------------------------------------------------------------- player profiles (XP per hour at level L)
# A: steady, at-level: 120 kills/h, creatures at own level, 5 XP per creature level
# B: cautious: 60 kills/h, creatures at 75% of own level
# C: crafter/gatherer: 720 actions/h (one every 5 s, as P20's "one use every 5 seconds"),
#    0.5 XP x action level per craft or harvest, action level = own level (working at-level material);
#    plus XP for skill points gained (a bounded pool per loop, modeled separately below)
def rate_A(L): return 120 * 5 * max(1.0, L)
def rate_B(L): return 60 * 5 * max(1.0, 0.75 * L)
def rate_C(L): return 720 * 0.5 * max(1.0, L)
PROFILES = (("A", rate_A), ("B", rate_B), ("C", rate_C))

# ---------------------------------------------------------------- curve shapes: XP to go from level L to L+1
def shape_power(c=40.0, p=1.5):
    return lambda L: c * L ** p

def shape_later_slower(c=40.0, p=1.5, g=1.02):
    # the P20 power curve to 100, then +2% compounding per level above 100 (level 199 costs x7.2 the plain curve)
    return lambda L: c * L ** p * (g ** max(0, L - 100))

def shape_flat_loops(loop0_hours, loop_hours, rate=rate_A):
    """S2, a hand table: the P20 power curve L^1.5 for levels 1..99, scaled so loop 0 takes `loop0_hours` for
    profile A (loop 1 then follows from the curve), and above 100 each 5-level block solved so loops 2..21 take
    `loop_hours` for A with no reserve credit, never letting XP-to-next fall below the level before it.
    Returns (xp(L) function, feasible flag: False if some loop's echo re-climb alone exceeds loop_hours)."""
    t = {}
    s0 = sum(L ** 0.5 for L in range(1, 50))
    k = loop0_hours / s0
    for L in range(1, 100):
        t[L] = k * L ** 0.5      # hours at base rate for profile A; XP(L) = t * rate(L) = const * L^1.5
    feasible = True
    for n in range(2, 22):
        pre = sum(t[L] for L in range(1, CAPS[n - 1])) / echo(n)
        block = loop_hours - pre
        if block <= 0:
            feasible = False
        for L in range(CAPS[n - 1], CAPS[n]):
            want = max(block, 0.0) / 5.0
            floor_t = t[L - 1] * rate(L - 1) / rate(L)   # same XP as the level before
            t[L] = max(want, floor_t)
    return (lambda L: t[L] * rate(L)), feasible

# ---------------------------------------------------------------- the loop model
def loop_hours(xp, rate, n, reserve_in=0.0):
    """Hours to go from level 1 to the loop's cap. Levels below the previous cap earn at x echo(n).
    reserve_in (raw XP from the last loop's reserve) is spent first, from level 1."""
    prev = CAPS[n - 1] if n > 0 else 0
    hours = 0.0
    carry = reserve_in
    for L in range(1, CAPS[n]):
        need = xp(L)
        if carry >= need:
            carry -= need
            continue
        need -= carry
        carry = 0.0
        m = echo(n) if L < prev else 1.0
        hours += need / (rate(L) * m)
    return hours, carry  # carry > 0 would mean the reserve passed the cap (must never happen)

def reserve_xp(xp, n):
    if n >= 21:
        return 0.0  # no next cap on the ladder (loops after 200 keep cap 200): 25% of zero
    return RESERVE_FRACTION * sum(xp(L) for L in range(CAPS[n], CAPS[n + 1]))

def run(xp, rate):
    """Main rows: hours with NO reserve credit (a player who resets as soon as they hold the scroll).
    Also: hours to fill the reserve at max level, and the loop's hours if the last loop's reserve was full."""
    rows = []
    cum = 0.0
    prev_res = 0.0
    for n in LOOPS:
        h, _ = loop_hours(xp, rate, n, 0.0)
        h_cred, leftover = loop_hours(xp, rate, n, prev_res)
        assert leftover == 0.0, f"reserve carried past the cap at loop {n}"
        cum += h
        r = reserve_xp(xp, n)
        h_res = r / rate(CAPS[n])  # hours at max level to fill the reserve (at-cap XP rate)
        rows.append(dict(loop=n, cap=CAPS[n], hours=h, cum=cum, reserve=r, res_hours=h_res, hours_cred=h_cred))
        prev_res = r
    return rows

def total_xp_to(xp, N): return sum(xp(L) for L in range(1, N))

def fmt(x):
    if x >= 100: return f"{x:,.0f}"
    if x >= 10: return f"{x:.1f}"
    return f"{x:.2f}"

def months(h): return h / HOURS_PER_WEEK / WEEKS_PER_MONTH

KEY_LOOPS = (0, 1, 2, 5, 10, 18, 21)

def print_full(title, xp):
    print(f"### {title}\n")
    print("Hours from level 1 to the loop's cap, no reserve credit. \"res fill\" = hours at max level to fill the "
          "reserve (25% of the XP from this cap to the next). \"w/ res\" = this loop's hours if the previous loop's "
          "reserve was full. C = crafts and harvests only (the skill-gain pool is A.2c).\n")
    print("| loop | cap | echo | A h | A cum | A res fill | A w/ res | B h | B cum | C h | C cum |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    ra, rb, rc = run(xp, rate_A), run(xp, rate_B), run(xp, rate_C)
    for a, b, c in zip(ra, rb, rc):
        print(f"| {a['loop']} | {a['cap']} | x{echo(a['loop']):g} | {fmt(a['hours'])} | {fmt(a['cum'])} | "
              f"{fmt(a['res_hours'])} | {fmt(a['hours_cred'])} | {fmt(b['hours'])} | {fmt(b['cum'])} | "
              f"{fmt(c['hours'])} | {fmt(c['cum'])} |")
    print()
    return ra, rb, rc

def print_key(title, xp):
    ra, rb, rc = run(xp, rate_A), run(xp, rate_B), run(xp, rate_C)
    print(f"| {title} | " + " | ".join(fmt(ra[n]['hours']) for n in KEY_LOOPS) +
          f" | {fmt(ra[21]['cum'])} | {fmt(rb[21]['cum'])} | {fmt(rc[21]['cum'])} | {ra[21]['cum']/ra[0]['hours']:.0f} |")
    return ra

# ---------------------------------------------------------------- profile C's skill-gain pool (gain_model.py port)
# Pinned SkillCheck.CheckSkill (UOContent/Skills/SkillCheck.cs:126-137 at d4531cd94, AOS branch) and Gain (:236-282),
# plus ClusterFSkillGain (attempts, amount). Expected values, no randomness.
RATES = {
    "test":  dict(attempts=3, amount=5, gf=5.0),   # Configuration-test: ClusterF 3 / x5, testCenter.skillGainMultiplier 5.0
    "live":  dict(attempts=3, amount=5, gf=1.0),   # Configuration: ClusterF 3 / x5, Test Center off
    "plain": dict(attempts=1, amount=1, gf=1.0),   # pinned alone, GainFactor 1 (no ClusterF, no Test Center)
}

def gc(base, cap, total, totalcap, chance, success, gf):
    g = (totalcap - total) / totalcap
    g += (cap - base) / cap
    g /= 2
    g += (1.0 - chance) * (0.5 if success else 0.0)
    g /= 2
    g *= gf
    return max(g, 0.01)

def points_per_use(base, cap, total, totalcap, chance, r, echo_amount=1.0):
    """Expected skill points per use. Below 10.0 base every roll gains Random(4)+1 tenths (mean 0.25);
    the amount bonus repeats Gain() amount-1 more times. Echo is modeled as an extra amount multiplier
    (see Part C for why not as a chance multiplier)."""
    if base < 10.0:
        p = 1.0
        per_gain = 0.25 * r["amount"]
    else:
        p = chance * min(1.0, gc(base, cap, total, totalcap, chance, True, r["gf"])) + \
            (1 - chance) * min(1.0, gc(base, cap, total, totalcap, chance, False, r["gf"]))
        per_gain = 0.1 * r["amount"]
    return r["attempts"] * p * per_gain * echo_amount

def uses_to(target, cap, chance, r, start=0.0, echo_amount=1.0, others=6):
    """Uses to climb one skill from start to target (<= cap), with `others` other skills already at the cap
    (sets Total). Total cap = 58 x cap (ClusterFSkillCaps, unlimited total)."""
    totalcap = 58 * cap
    b, n = start, 0
    while b < target - 1e-9:
        b = min(cap, b + points_per_use(b, cap, others * cap + b, totalcap, chance, r, echo_amount))
        n += 1
        if n > 10_000_000: return float("inf")
    return n

def pool_C(xp, n, r, skills=6, action_s=5.0, chance=0.7, xp_per_point=10.0):
    """Profile C trains `skills` craft/gather skills from 0 to the loop's cap in turn, one action every action_s.
    XP: 0.5 x level per action (rate_C) plus xp_per_point x level per skill point gained, both x base echo on
    levels already reached. Returns (hours to the loop's cap, share of XP from skill points, hours spent before
    every trained skill reached the cap or None)."""
    cap_ = CAPS[n]; prev = CAPS[n - 1] if n > 0 else 0
    L, into, t = 1, 0.0, 0.0
    sk = [0.0] * skills; idx = 0
    xp_skill = xp_act = 0.0
    t_skills_done = None
    dt = action_s / 3600.0
    while L < cap_:
        m = echo(n) if L < prev else 1.0
        gained = 0.0
        if idx < skills:
            b = sk[idx]
            step = points_per_use(b, cap_, sum(sk), 58 * cap_, chance, r)
            sk[idx] = min(cap_, b + step)
            gained = sk[idx] - b
            if sk[idx] >= cap_:
                idx += 1
                if idx == skills: t_skills_done = t
        a = 0.5 * L * m
        g = xp_per_point * L * gained * m
        xp_act += a; xp_skill += g
        into += a + g
        t += dt
        while L < cap_ and into >= xp(L):
            into -= xp(L); L += 1
    return t, xp_skill / (xp_act + xp_skill), t_skills_done

if __name__ == "__main__":
    print("## A.2 XP model on the 22-step ladder (generated by notes\\cc-P54-scratch\\xp_ladder.py)\n")
    print("Ladder: " + ", ".join(f"{n}:{c}" for n, c in zip(LOOPS, CAPS)) + "\n")
    print("Base echo by loop: " + ", ".join(f"{n}:x{echo(n):g}" for n in LOOPS) + "\n")
    print("Keeper echo by loop (skills only): " + ", ".join(f"{n}:x{keeper_echo(n):.2f}" for n in LOOPS) + "\n")

    p20 = shape_power()
    print("### XP table, P20 power curve XP(L) = 40 x L^1.5\n")
    print("| level | XP to next | total XP to reach |")
    print("|---|---|---|")
    for L in (1, 10, 25, 50, 100, 105, 120, 150, 195, 200):
        print(f"| {L} | {p20(L):,.0f} | {total_xp_to(p20, L):,.0f} |")
    print()

    print_full("S1 at P20's constant (C = 40), on the 22-step ladder", p20)

    print("### Where a loop's time goes (S1 at C = 40, profile A, no reserve credit)\n")
    print("| loop | re-climb 1..prev cap at echo, h | new levels at base, h | re-climb share |")
    print("|---|---|---|---|")
    for n in KEY_LOOPS[1:]:
        prev = CAPS[n - 1]
        rec = sum(p20(L) / (rate_A(L) * echo(n)) for L in range(1, prev))
        new = sum(p20(L) / rate_A(L) for L in range(prev, CAPS[n]))
        print(f"| {n} | {fmt(rec)} | {fmt(new)} | {rec/(rec+new):.0%} |")
    print()

    print("### Edge checks: the reserve (S1 at C = 40; the ratios hold for any curve)\n")
    print("| loop | reserve XP | XP of the next loop's new levels | reserve / new levels | levels the reserve covers from 1 next loop |")
    print("|---|---|---|---|---|")
    for n in (0, 1, 2, 10, 20, 21):
        r = reserve_xp(p20, n)
        if n < 21:
            new_next = sum(p20(L) for L in range(CAPS[n], CAPS[n + 1]))
            acc, L = 0.0, 1
            while L < CAPS[n + 1] and acc + p20(L) <= r:
                acc += p20(L); L += 1
            print(f"| {n} | {r:,.0f} | {new_next:,.0f} | {r/new_next:.2f} | 1 to {L} |")
        else:
            print(f"| {n} | 0 | 0 (no next cap) | - | - |")
    print()
    raw = total_xp_to(p20, 195); disc = raw / echo(21)
    print(f"Loop 21 re-climb 1..195: raw {raw:,.0f} XP; at x10 echo it costs {disc:,.0f} earned XP; "
          f"the 5 new levels cost {sum(p20(L) for L in range(195,200)):,.0f}.\n")

    print("### A.3 Curve shapes: profile A hours per loop at key loops, and totals to the capstone\n")
    print("No reserve credit. The last column is capstone total / loop 0 for profile A: fixed by the shape, so a "
          "one-constant shape (S1, S3) can hit a loop-0 target or a capstone target, not both.\n")
    print("| shape | " + " | ".join(f"loop {n}" for n in KEY_LOOPS) + " | total A | total B | total C | total/loop0 |")
    print("|" + "---|" * (len(KEY_LOOPS) + 5))
    s1 = shape_power(40.0)
    s3 = shape_later_slower(40.0)
    ra1 = print_key("S1 power L^1.5, C = 40", s1)
    ra3 = print_key("S3 later slower (L^1.5, +2%/level past 100), C = 40", s3)
    ratio01 = ra1[1]['hours'] / ra1[0]['hours']
    REC0 = 3.0
    per_default = (260.0 - REC0 - REC0 * ratio01) / 20.0
    s2, ok = shape_flat_loops(REC0, per_default)
    print_key("S2 hand table: loop 0 = 3 h, loops 2-21 aim 12.5 h", s2)
    print()

    print("### A.4 Against Chase's candidate targets (profile A; B takes 2.67x A's hours on every row, C 1.67x)\n")
    print("Capstone targets at 10 h/week: 3 months = %.0f h, 6 months = %.0f h, 12 months = %.0f h.\n" %
          tuple(m * WEEKS_PER_MONTH * HOURS_PER_WEEK for m in TARGET_CAPSTONE_MONTHS))
    print("| shape | fit to | loop 0 h | loop 1 h | capstone h | months at 10 h/wk | constant or table |")
    print("|---|---|---|---|---|---|---|")
    for name, ra, base_c in (("S1 power", ra1, 40.0), ("S3 later slower", ra3, 40.0)):
        l0, l1, tot = ra[0]['hours'], ra[1]['hours'], ra[21]['cum']
        for t in TARGET_LOOP0:
            k = t / l0
            print(f"| {name} | loop 0 = {t} h | {t} | {fmt(l1*k)} | {fmt(tot*k)} | {months(tot*k):.1f} | C = {base_c*k:.1f} |")
        for mo in TARGET_CAPSTONE_MONTHS:
            target = mo * WEEKS_PER_MONTH * HOURS_PER_WEEK
            k = target / tot
            print(f"| {name} | capstone = {mo} mo | {fmt(l0*k)} | {fmt(l1*k)} | {fmt(target)} | {mo} | C = {base_c*k:.1f} |")
    for t in TARGET_LOOP0:
        for mo in TARGET_CAPSTONE_MONTHS:
            target = mo * WEEKS_PER_MONTH * HOURS_PER_WEEK
            per = (target - t - t * ratio01) / 20.0
            xp, ok = shape_flat_loops(t, per)
            r = run(xp, rate_A)
            print(f"| S2 hand table | loop 0 = {t} h, capstone = {mo} mo | {fmt(r[0]['hours'])} | {fmt(r[1]['hours'])} | "
                  f"{fmt(r[21]['cum'])} | {months(r[21]['cum']):.1f} | loops 2-21 aim {per:.1f} h each"
                  f"{'' if ok else '; INFEASIBLE: the echo re-climb alone is longer'} |")
    print()

    xp, ok = shape_flat_loops(REC0, per_default)
    print_full(f"S2 recommended default: loop 0 = 3 h, loops 2-21 aim {per_default:.1f} h (profile A)", xp)
    print("XP to next level in that table (what a builder would ship as config):\n")
    print("| level | XP to next | total to reach | | level | XP to next | total to reach |")
    print("|---|---|---|---|---|---|---|")
    lv = [1, 10, 25, 49, 50, 75, 99, 100, 105, 120, 150, 175, 195, 199]
    half = len(lv) // 2
    for i in range(half):
        a, b = lv[i], lv[i + half]
        print(f"| {a} | {xp(a):,.0f} | {total_xp_to(xp, a):,.0f} | | {b} | {xp(b):,.0f} | {total_xp_to(xp, b):,.0f} |")
    print()
    mono = all(xp(L + 1) >= xp(L) - 1e-6 for L in range(1, 199))
    print(f"XP to next never falls from one level to the next: {mono}.\n")
    pre = sum(xp(L) / (rate_A(L) * echo(21)) for L in range(1, 195))
    print(f"S2 loop 21: the echo re-climb 1..195 takes {pre:.1f} h of the loop's {run(xp, rate_A)[21]['hours']:.1f} h for profile A.\n")

    print("### A.2c Profile C with its skill-gain pool (S2 default table)\n")
    print("C trains 6 craft/gather skills from 0 to the loop's cap in turn, one action every 5 s at 70% success, "
          "earning 0.5 x level XP per action plus k x level XP per skill point gained (both x base echo on levels "
          "already reached). Gain rates from the gain model at three settings.\n")
    print("| XP per skill point | loop | cap | rates | C h (actions + skill pool) | C h (actions only) | share of XP from skill points | hours until all 6 skills capped |")
    print("|---|---|---|---|---|---|---|---|")
    rc_only = run(xp, rate_C)
    for k in (2.0, 10.0):
        for n in (0, 1, 2, 10, 21):
            for rn in ("test", "live", "plain"):
                h, share, tdone = pool_C(xp, n, RATES[rn], xp_per_point=k)
                print(f"| {k:g} x level | {n} | {CAPS[n]} | {rn} | {fmt(h)} | {fmt(rc_only[n]['hours'])} | {share:.0%} | "
                      f"{'skills not all capped when the loop ends' if tdone is None else fmt(tdone)} |")
    print()
