"""Numerical checks for P282's research model, not server/lane tests."""
import contextlib
import io
import math
import unittest

with contextlib.redirect_stdout(io.StringIO()):
    import xp_curve as curve
    import approved_baseline as approved


class CurveChecks(unittest.TestCase):
    def test_approved_s2_pace_and_monotonic_table(self):
        self.assertAlmostEqual(approved.p54.loop_hours(approved.XP, approved.p54.rate_A, 0)[0], 3)
        hours = sum(approved.p54.loop_hours(approved.XP, approved.p54.rate_A, i)[0] for i in range(22))
        self.assertAlmostEqual(hours, 334.018284442, places=6)
        self.assertTrue(all(approved.XP(l + 1) >= approved.XP(l) - 1e-8 for l in range(1, 199)))

    def test_approved_five_level_bank_credits_from_level_one(self):
        bank = approved.bank(100)
        self.assertAlmostEqual(bank, sum(approved.XP(l) for l in range(100, 105)))
        level, partial = approved.remaining_after_credit(2, bank)
        self.assertEqual(level, 101)
        self.assertAlmostEqual(partial, 96668.18815487987)
        self.assertEqual(approved.bank(200), 0)
        for loop in range(1, 22):
            incoming = approved.bank(approved.p54.CAPS[loop - 1])
            self.assertEqual(approved.p54.loop_hours(approved.XP, approved.p54.rate_A, loop, incoming)[1], 0)

    def test_chase_ladder_has_twenty_scroll_steps(self):
        self.assertEqual(list(curve.CAPS), [50, 100, *range(105, 201, 5)])
        self.assertEqual(len(curve.CAPS[2:]), 20)

    def test_echo_starts_at_one_point_five_and_stops_at_ten(self):
        expected = [1, 1.5, 2, 3, 6, 9.5, 10, 10]
        self.assertEqual([curve.echo(i) for i in (0, 1, 2, 4, 10, 17, 18, 21)], expected)

    def test_proposed_xp_rounding_and_transition_index(self):
        self.assertEqual(curve.xp_next(1), 24)
        self.assertEqual(curve.xp_next(25), 3000)
        self.assertEqual(curve.xp_total(3), 24 + 67)
        self.assertEqual(curve.xp_next(50), math.floor(24 * 50 ** 1.5))

    def test_first_cap_has_no_echo_or_global_bonus(self):
        expected = sum(math.floor(24 * l ** 1.5) / (600 * l) for l in range(1, 50))
        self.assertAlmostEqual(curve.loop_hours(0, 120, 1), expected)

    def test_echo_stops_exactly_at_previous_peak(self):
        old, new = curve.loop_parts(2, 120, 1)
        expected_old = sum(math.floor(24 * l ** 1.5) / (1200 * l) for l in range(1, 100))
        expected_new = sum(math.floor(24 * l ** 1.5) / (600 * l) for l in range(100, 105))
        self.assertAlmostEqual(old, expected_old)
        self.assertAlmostEqual(new, expected_new)

    def test_full_bank_cannot_buy_old_ground_and_covers_only_five_new_levels(self):
        bank = curve.reserve_cap(100)
        old, new = curve.loop_parts(2, 120, 1, reserve_xp=bank)
        self.assertEqual(new, 0)
        self.assertEqual(old, curve.loop_parts(2, 120, 1)[0])
        self.assertGreater(curve.loop_parts(1, 120, 1, reserve_xp=curve.reserve_cap(50))[1], 0)
        half_new = curve.loop_parts(2, 120, 1, reserve_xp=bank / 2)[1]
        self.assertGreater(half_new, 0)
        self.assertLess(half_new, curve.loop_parts(2, 120, 1)[1])
        self.assertEqual(curve.reserve_cap(200), 0)

    def test_bank_fill_is_charged_at_cap_without_echo(self):
        expected = sum(math.floor(24 * l ** 1.5) for l in range(195, 200)) / (600 * 195)
        self.assertAlmostEqual(curve.bank_hours(195, 120, 1), expected)
        self.assertGreater(curve.bank_hours(195, 120, 1), curve.loop_parts(21, 120, 1)[1])

    def test_bands_partition_every_loop_and_content_ceiling_costs_time(self):
        for loop, cap in enumerate(curve.CAPS):
            parts = sum(curve.band_hours(loop, low, high, 120, 1)
                        for low, high in curve.BANDS)
            self.assertAlmostEqual(parts, curve.loop_hours(loop, 120, 1))
        self.assertGreater(curve.loop_hours(21, 120, 1, content_top=160),
                           curve.loop_hours(21, 120, 1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
