"""P282 research only: P20's curve on Chase's 21-reset ladder.

Run python -B notes/cc-P282-scratch/xp_curve.py to regenerate adjacent tables/CSVs.
Uses only stdlib; no server implementation, live telemetry or external input.
"""
import csv
import math
from pathlib import Path

CAPS = (50, 100, *range(105, 201, 5))
C = 24.0
EXPONENT = 1.5
XPK = 5.0
STYLES = {"steady": (120, 1.0), "cautious": (60, 0.75)}
BANDS = ((1, 10), (10, 25), (25, 50), (50, 75), (75, 100),
         *((l, l + 5) for l in range(100, 200, 5)))


def xp_next(level, coefficient=C):
    return math.floor(coefficient * level ** EXPONENT)


def xp_total(level, coefficient=C):
    return sum(xp_next(l, coefficient) for l in range(1, level))


def echo(loop):
    return min(10.0, 1.0 + 0.5 * loop)


def previous_peak(loop):
    return CAPS[loop - 1] if loop else 1


def raw_rate(level, kills_per_hour, level_ratio, content_top=None):
    creature_level = max(1.0, level_ratio * level)
    if content_top is not None:
        creature_level = min(creature_level, content_top)
    return kills_per_hour * XPK * creature_level


def band_hours(loop, low, high, kills_per_hour, level_ratio,
               content_top=None, coefficient=C, reserve_xp=0):
    """Clip to loop cap; reserve pays only new ground, without echo.

    Spend from the first frontier transition even if the selected band starts
    later, so summing bands never spends the same bank on different levels.
    """
    total = 0.0
    peak = previous_peak(loop)
    for level in range(1, CAPS[loop]):
        cost = xp_next(level, coefficient)
        if level >= peak and loop:
            spent = min(cost, reserve_xp)
            cost -= spent
            reserve_xp -= spent
        multiplier = echo(loop) if level < peak else 1.0
        if low <= level < high:
            total += cost / (raw_rate(level, kills_per_hour, level_ratio, content_top) * multiplier)
    return total


def loop_parts(loop, kills_per_hour, level_ratio, **kwargs):
    peak = previous_peak(loop)
    return (band_hours(loop, 1, peak, kills_per_hour, level_ratio, **kwargs),
            band_hours(loop, peak, CAPS[loop], kills_per_hour, level_ratio, **kwargs))


def loop_hours(loop, kills_per_hour, level_ratio, **kwargs):
    return sum(loop_parts(loop, kills_per_hour, level_ratio, **kwargs))


def reserve_cap(cap, coefficient=C):
    # Five future transitions at the outgoing cap; none beyond terminal 200.
    return (sum(xp_next(l, coefficient) for l in range(cap, cap + 5))
            if cap < 200 else 0)


def bank_hours(cap, kills_per_hour, level_ratio, content_top=None, coefficient=C):
    return reserve_cap(cap, coefficient) / raw_rate(cap, kills_per_hour, level_ratio, content_top)


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |",
                      *("| " + " | ".join(str(v) for v in row) + " |" for row in rows)])


def write_csv(name, rows):
    with (Path(__file__).parent / name).open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def calculate():
    loops, bands, banks = [], [], []
    for style, (kph, ratio) in STYLES.items():
        cumulative = cumulative_banked = cumulative_top160 = 0.0
        for loop, cap in enumerate(CAPS):
            old, new = loop_parts(loop, kph, ratio)
            hours = old + new
            cumulative += hours
            hours_top160 = loop_hours(loop, kph, ratio, content_top=160)
            cumulative_top160 += hours_top160
            loops.append(dict(style=style, loop=loop, cap=cap,
                              scroll_target=cap if loop >= 2 else "none", echo=echo(loop),
                              old_hours=old, new_hours=new, hours=hours, cumulative_hours=cumulative,
                              casual_days=hours, regular_days=hours / 3, heavy_days=hours / 6,
                              cumulative_casual_days=cumulative, cumulative_regular_days=cumulative / 3,
                              cumulative_heavy_days=cumulative / 6,
                              content_top160_hours=hours_top160,
                              content_top160_cumulative_hours=cumulative_top160))
            for low, high in BANDS:
                if low < cap:
                    h = band_hours(loop, low, high, kph, ratio)
                    bands.append(dict(style=style, loop=loop, cap=cap, low=low, high=min(high, cap),
                                      hours=h, casual_days=h, regular_days=h / 3, heavy_days=h / 6))
            incoming = reserve_cap(CAPS[loop - 1]) if loop else 0
            fill_previous = bank_hours(CAPS[loop - 1], kph, ratio) if loop else 0
            h_banked = loop_hours(loop, kph, ratio, reserve_xp=incoming)
            cumulative_banked += h_banked + fill_previous
            banks.append(dict(style=style, loop=loop, cap=cap, incoming_xp=incoming,
                              fill_previous_cap_hours=fill_previous, reclimb_hours=h_banked,
                              arrival_cost_hours=h_banked + fill_previous,
                              cumulative_including_fill_hours=cumulative_banked,
                              empty_reserve_cumulative_hours=cumulative))
    coefficients = []
    for coefficient in (20, 24, 30, 40):
        hs = [loop_hours(i, 120, 1, coefficient=coefficient) for i in range(len(CAPS))]
        coefficients.append(dict(coefficient=coefficient, loop0=hs[0], loop1=hs[1],
                                 through100=sum(hs[:2]), loop21=hs[-1], through200=sum(hs)))
    return loops, bands, banks, coefficients


def sections(loops, bands, banks, coefficients):
    steady = [r for r in loops if r["style"] == "steady"]
    cautious = [r for r in loops if r["style"] == "cautious"]
    banked = [r for r in banks if r["style"] == "steady"]
    result = {}
    result["coefficients"] = table(
        ["C", "Loop 0 h", "Loop 1 h", "Creation to 100 h", "Loop 21 h", "Creation to 200 h"],
        [[r["coefficient"], *(f'{r[k]:.2f}' for k in ("loop0", "loop1", "through100", "loop21", "through200"))]
         for r in coefficients])
    result["loops"] = table(
        ["Loop", "Cap", "Scroll target", "Echo", "Old h", "New h", "Loop h", "Cumulative h"],
        [[r["loop"], r["cap"], r["scroll_target"], f'{r["echo"]:g}x',
          *(f'{r[k]:.2f}' for k in ("old_hours", "new_hours", "hours", "cumulative_hours"))] for r in steady])
    result["calendar"] = table(
        ["Loop", "Loop days 1h", "3h", "6h", "Cumulative days 1h", "3h", "6h",
         "Cautious loop h", "Cautious cumulative h"],
        [[a["loop"], *(f'{a[k]:.2f}' for k in ("casual_days", "regular_days", "heavy_days",
          "cumulative_casual_days", "cumulative_regular_days", "cumulative_heavy_days")),
          f'{b["hours"]:.2f}', f'{b["cumulative_hours"]:.2f}'] for a, b in zip(steady, cautious)])
    band_rows = []
    for low, high in BANDS:
        base = band_hours(21, low, high, 120, 1) * (echo(21) if high <= 195 else 1)
        band_rows.append([f"{low}->{high}", f"{base:.2f}", f"{base / 3:.2f}", f"{base / 6:.2f}",
                          f"{base / 10:.2f}"])
    result["bands"] = table(["Band", "Base h / days at 1h", "Base days at 3h", "Base days at 6h",
                             "Old-ground h at x10"], band_rows)
    result["reserve"] = table(
        ["Arrive loop", "Cap", "Incoming XP", "Fill prior cap h", "Re-climb h", "Arrival incl. fill h",
         "Cumulative incl. fill h"],
        [[r["loop"], r["cap"], f'{r["incoming_xp"]:,}',
          *(f'{r[k]:.2f}' for k in ("fill_previous_cap_hours", "reclimb_hours", "arrival_cost_hours",
                                   "cumulative_including_fill_hours"))] for r in banked])
    result["sensitivity"] = table(
        ["Efficiency / reserve", "To 100 h", "To 200 h", "Days at 1h", "3h", "6h"],
        [[label, f"{h100:.2f}", f"{h200:.2f}", f"{h200:.2f}", f"{h200 / 3:.2f}", f"{h200 / 6:.2f}"]
         for label, h100, h200 in (
             ("Steady, empty", steady[1]["cumulative_hours"], steady[-1]["cumulative_hours"]),
             ("Cautious, empty", cautious[1]["cumulative_hours"], cautious[-1]["cumulative_hours"]),
             ("Steady, full banks incl. filling", banked[1]["cumulative_including_fill_hours"],
              banked[-1]["cumulative_including_fill_hours"]),
             ("Cautious, full banks incl. filling", banks[len(CAPS) + 1]["cumulative_including_fill_hours"],
              banks[-1]["cumulative_including_fill_hours"]),
             ("Steady, content tops at 160, empty", steady[1]["content_top160_cumulative_hours"],
              steady[-1]["content_top160_cumulative_hours"]))])
    return result


def main():
    loops, bands, banks, coefficients = calculate()
    for filename, rows in (("loops.csv", loops), ("bands.csv", bands),
                           ("reserve.csv", banks), ("coefficients.csv", coefficients)):
        write_csv(filename, rows)
    fragments = sections(loops, bands, banks, coefficients)
    text = ("# P282 generated XP tables, 2026-10-21\n\n"
            "Research assumptions, not measured gameplay. C=24; exponent=1.5; XP/kill=5*creature level.\n"
            "Steady=120 kills/h at own level; cautious=60 kills/h at 75% of own level (floor 1).\n"
            "No global loop bonus. Echo=min(10,1+0.5*loop), below previous peak only.\n"
            "Hours are active XP-earning hours; calendar days divide hours by 1, 3 or 6.\n"
            "Tables exclude scroll acquisition delays, travel, training downtime and noncombat XP.\n"
            "Main tables enter each loop at level 1 with an empty reserve; cumulative includes loop 0.\n"
            "Band A->B includes transitions A through B-1. At echo E divide base band time by E\n"
            "only below the old peak; bands.csv gives every reachable band in every loop/style.\n"
            "Full-bank tables charge capped farming to the arriving loop, before its reset/re-climb.\n"
            "The final arrival at 200 includes no outgoing bank. No echo on bank fill or release.\n\n")
    for name, fragment in fragments.items():
        text += f"## {name.capitalize()}\n\n{fragment}\n\n"
    (Path(__file__).parent / "tables.md").write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote tables.md; {len(loops)} loop rows, {len(bands)} band rows, "
          f"{len(banks)} reserve rows, {len(coefficients)} coefficient rows.")
    print(fragments["coefficients"])
    print(fragments["sensitivity"])


if __name__ == "__main__":
    main()
