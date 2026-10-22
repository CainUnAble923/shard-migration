"""Re-run the 10-05 approved S2 curve with P282's five-level reserve.

P54's historical script is imported read-only, with no main/output execution.
Retain its unrounded XP table for comparability; exported CSV is the numeric source.
Run python -B notes/cc-P282-scratch/approved_baseline.py.
"""
import importlib.util
from pathlib import Path

import xp_curve as comparison

SOURCE = Path(__file__).parents[1] / 'cc-P54-scratch' / 'xp_ladder.py'
spec = importlib.util.spec_from_file_location('p54', SOURCE)
p54 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p54)

# Exactly P54's chosen table construction, not a rounded re-fit of its prose.
power = p54.shape_power()
ratio01 = p54.loop_hours(power, p54.rate_A, 1)[0] / p54.loop_hours(power, p54.rate_A, 0)[0]
TARGET = (260.0 - 3.0 - 3.0 * ratio01) / 20.0
XP, _ = p54.shape_flat_loops(3.0, TARGET)


def bank(cap):
    return sum(XP(l) for l in range(cap, cap + 5)) if cap < 200 else 0.0


def remaining_after_credit(loop, credit):
    level = 1
    while level < p54.CAPS[loop] and credit >= XP(level):
        credit -= XP(level)
        level += 1
    return level, credit


def main():
    rows, bands, xp_rows = [], [], []
    for style, rate in (("steady", p54.rate_A), ("cautious", p54.rate_B)):
        cumulative = banked_cumulative = 0.0
        for loop, cap in enumerate(p54.CAPS):
            previous = p54.CAPS[loop - 1] if loop else 1
            old = sum(XP(l) / (rate(l) * p54.echo(loop)) for l in range(1, previous))
            new = sum(XP(l) / rate(l) for l in range(previous, cap))
            h = old + new
            cumulative += h
            incoming = bank(previous) if loop else 0.0
            filled = incoming / rate(previous) if loop else 0.0
            after_credit, leftover = p54.loop_hours(XP, rate, loop, incoming)
            banked_cumulative += after_credit + filled
            start, partial = remaining_after_credit(loop, incoming)
            rows.append(dict(style=style, loop=loop, cap=cap, echo=p54.echo(loop),
                             old_hours=old, new_hours=new, hours=h, cumulative_hours=cumulative,
                             casual_days=h, regular_days=h / 3, heavy_days=h / 6,
                             cumulative_casual_days=cumulative, cumulative_regular_days=cumulative / 3,
                             cumulative_heavy_days=cumulative / 6, incoming_bank_xp=incoming,
                             credited_start_level=start, credited_partial_xp=partial,
                             unused_after_cap_xp=leftover, fill_prior_hours=filled,
                             after_credit_hours=after_credit, cumulative_with_fill_hours=banked_cumulative))
            for low, high in comparison.BANDS:
                if low < cap:
                    bh = sum(XP(l) / (rate(l) * (p54.echo(loop) if l < previous else 1))
                             for l in range(low, min(high, cap)))
                    bands.append(dict(style=style, loop=loop, low=low, high=min(high, cap), hours=bh,
                                      casual_days=bh, regular_days=bh / 3, heavy_days=bh / 6))
    for level in range(1, 200):
        xp_rows.append(dict(level=level, xp_to_next=XP(level), total_xp_to_reach=p54.total_xp_to(XP, level)))
    for filename, data in (("approved-loops.csv", rows), ("approved-bands.csv", bands),
                            ("approved-xp-table.csv", xp_rows)):
        comparison.write_csv(filename, data)
    a, b = rows[:22], rows[22:]
    loop_table = comparison.table(
        ["Loop", "Cap", "Echo", "Old h", "New h", "Total h", "Cumulative h", "Cumulative days 1h/3h/6h"],
        [[r['loop'], r['cap'], f"{r['echo']:g}x", *(f"{r[k]:.2f}" for k in
          ('old_hours', 'new_hours', 'hours', 'cumulative_hours')),
          f"{r['cumulative_hours']:.2f} / {r['cumulative_hours']/3:.2f} / {r['cumulative_hours']/6:.2f}"] for r in a])
    reserve_table = comparison.table(
        ["Loop", "Bank XP", "Level after credit", "Fill prior h", "After credit h", "Cumulative incl. fill h"],
        [[r['loop'], f"{r['incoming_bank_xp']:.2f}", r['credited_start_level'],
          *(f"{r[k]:.2f}" for k in ('fill_prior_hours', 'after_credit_hours', 'cumulative_with_fill_hours'))] for r in a])
    band_table = comparison.table(
        ["Band", "Base h / days at 1h", "Base days at 3h", "Base days at 6h", "Old h at x10"],
        [[f'{low}->{high}', f'{h:.2f}', f'{h/3:.2f}', f'{h/6:.2f}', f'{h/10:.2f}']
         for low, high in comparison.BANDS
         for h in [sum(XP(l) / p54.rate_A(l) for l in range(low, high))]])
    sensitivity = comparison.table(
        ["Profile / reserve", "To 100 h", "To 200 h", "Days at 1h/3h/6h"],
        [[label, f'{h100:.2f}', f'{h200:.2f}', f'{h200:.2f} / {h200/3:.2f} / {h200/6:.2f}']
         for label, h100, h200 in (
             ('Steady empty', a[1]['cumulative_hours'], a[-1]['cumulative_hours']),
             ('Cautious empty', b[1]['cumulative_hours'], b[-1]['cumulative_hours']),
             ('Steady full banks incl. filling', a[1]['cumulative_with_fill_hours'], a[-1]['cumulative_with_fill_hours']),
             ('Cautious full banks incl. filling', b[1]['cumulative_with_fill_hours'], b[-1]['cumulative_with_fill_hours']))])
    text = ('# Approved S2 baseline re-run with five-level reserve, 2026-10-21\n\n'
            'Curve and raw reserve credit from level 1: Chase, 10-05. Reserve size: P282, five levels.\n'
            'Base echo and 21-reset ladder unchanged. Full banks are not multiplied by echo.\n'
            'Steady=120 kills/hour at own level; cautious=60/hour at 75% (floor 1).\n'
            'No extra global loop bonus. Main tables use empty banks, cumulative includes loop 0.\n'
            'Band A->B includes transitions A..B-1; divide remembered portions by eligible echo.\n'
            'Calendar days are active hours divided by 1/3/6. Every loop/band/style is in the CSVs.\n'
            'No noncombat XP, downtime, training or scroll wait is included.\n'
            'XP retains P54 floating precision; integer rounding belongs to a future config export.\n\n')
    for title, fragment in (('Loops', loop_table), ('Bands', band_table), ('Full reserves', reserve_table),
                             ('Sensitivity', sensitivity)):
        text += f'## {title}\n\n{fragment}\n\n'
    (Path(__file__).parent / 'approved-tables.md').write_text(text, encoding='utf-8', newline='\n')
    print(f'S2 target per loop={TARGET:.9f}; actual empty total={a[-1]["cumulative_hours"]:.9f}')
    print(sensitivity)
    print('Full incoming bank after credit at loop 2:', a[2]['credited_start_level'],
          'partial XP:', a[2]['credited_partial_xp'])


if __name__ == '__main__':
    main()
