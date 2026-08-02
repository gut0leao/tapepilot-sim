import unittest

from sim.metrics import RollingRmsError


class RollingRmsErrorTests(unittest.TestCase):
    def test_waits_for_settling_period(self):
        metric = RollingRmsError(window_seconds=5.0, settling_seconds=3.0)

        for _ in range(2999):
            value = metric.step(0.001, 1800.0, 1798.2)

        self.assertIsNone(value)

    def test_reports_percentual_rms_after_settling(self):
        metric = RollingRmsError(window_seconds=5.0, settling_seconds=3.0)

        for _ in range(3001):
            value = metric.step(0.001, 1800.0, 1798.2)

        self.assertAlmostEqual(value, 0.1)

    def test_resets_when_setpoint_changes(self):
        metric = RollingRmsError(window_seconds=5.0, settling_seconds=3.0)
        for _ in range(3001):
            metric.step(0.001, 1800.0, 1798.2)

        value = metric.step(0.001, 2600.0, 2600.0)

        self.assertIsNone(value)

    def test_remains_numerically_stable_across_many_windows(self):
        metric = RollingRmsError(window_seconds=5.0, settling_seconds=3.0)

        for _ in range(30000):
            value = metric.step(0.001, 1800.0, 1800.0)

        self.assertEqual(value, 0.0)

    def test_resets_when_configuration_context_changes(self):
        metric = RollingRmsError(window_seconds=5.0, settling_seconds=3.0)
        for _ in range(3001):
            metric.step(0.001, 1800.0, 1798.2, context=(False, 0.001))

        value = metric.step(0.001, 1800.0, 1798.2, context=(True, 0.001))

        self.assertIsNone(value)


if __name__ == "__main__":
    unittest.main()
