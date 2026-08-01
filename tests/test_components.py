import unittest
from unittest.mock import patch

from sim.controller import ProportionalController
from sim.encoder import VisualEncoder
from sim.faults import EpisodeGate, FaultModel, NaturalDisturbance, WowFlutterGenerator
from sim.plant import FirstOrderPlant
from sim.runtime import FixedStepScheduler


class ExtractedComponentTests(unittest.TestCase):
    def test_controller_preserves_gain_and_saturation(self):
        controller = ProportionalController(kp=0.02)

        self.assertEqual(controller.command(10.0), 0.2)
        self.assertEqual(controller.command(100.0), 1.0)
        self.assertEqual(controller.command(-100.0), -1.0)

    def test_plant_preserves_first_order_response(self):
        plant = FirstOrderPlant(tau=0.25)

        self.assertEqual(plant.advance(0.0, 1800.0, 0.25), 900.0)

    def test_fault_model_preserves_friction_and_tension(self):
        target, tension = FaultModel().apply_friction(1800.0, 1.0, 1.0)

        self.assertEqual(target, 1200.0)
        self.assertEqual(tension, 1.0)

    @patch("sim.encoder.random.gauss", return_value=1.0)
    def test_encoder_preserves_visual_jitter(self, _gauss):
        measured = VisualEncoder().measured_rpm(100.0, 0.5)

        self.assertEqual(measured, 110.0)

    def test_disturbance_is_deterministic(self):
        first = WowFlutterGenerator()
        second = WowFlutterGenerator()
        first.wow.set_occurrence(1.0)
        first.flutter.set_occurrence(1.0)
        second.wow.set_occurrence(1.0)
        second.flutter.set_occurrence(1.0)

        self.assertEqual(first.step(0.001), second.step(0.001))

    def test_frequency_change_preserves_phase(self):
        disturbance = NaturalDisturbance(
            0.5, 0.01, (0.1, 2.0), (0.0, 0.03), 1, 0.15, 2.0, 1.0, 3.0
        )
        disturbance.set_occurrence(1.0)
        disturbance.step(0.1)
        phase_before = disturbance.phase

        disturbance.set_frequency(1.0)

        self.assertEqual(disturbance.phase, phase_before)

    def test_disturbance_parameters_are_clamped(self):
        disturbance = NaturalDisturbance(
            0.5, 0.01, (0.1, 2.0), (0.0, 0.03), 1, 0.15, 2.0, 0.0, 3.0
        )

        disturbance.set_frequency(10.0)
        disturbance.set_amplitude(1.0)

        self.assertEqual(disturbance.frequency_hz, 2.0)
        self.assertEqual(disturbance.amplitude, 0.03)

    def test_disturbance_modulates_physical_target(self):
        faults = FaultModel()
        faults.disturbances.wow.set_occurrence(1.0)
        target = 1800.0

        for _ in range(125):
            disturbed, _, _, _ = faults.apply_speed_disturbance(target, 0.001)

        self.assertNotEqual(disturbed, target)

    def test_wow_and_flutter_are_independent_and_additive(self):
        generator = WowFlutterGenerator()
        generator.flutter.set_occurrence(1.0)

        wow, flutter, total = generator.step(0.001)

        self.assertEqual(wow, 0.0)
        self.assertEqual(total, flutter)

        generator.wow.set_occurrence(1.0)
        wow, flutter, total = generator.step(0.001)

        self.assertAlmostEqual(total, wow + flutter)

    def test_natural_disturbance_is_reproducible(self):
        first = WowFlutterGenerator()
        second = WowFlutterGenerator()
        first.wow.set_occurrence(1.0)
        second.wow.set_occurrence(1.0)
        first.flutter.set_occurrence(1.0)
        second.flutter.set_occurrence(1.0)

        first_values = [first.step(0.001) for _ in range(1000)]
        second_values = [second.step(0.001) for _ in range(1000)]

        self.assertEqual(first_values, second_values)

    def test_wow_and_flutter_use_independent_random_streams(self):
        generator = WowFlutterGenerator()

        for _ in range(1000):
            generator.step(0.001)

        self.assertNotEqual(
            generator.wow.noise.value,
            generator.flutter.noise.value,
        )

    def test_wow_is_not_a_repeating_sine(self):
        generator = WowFlutterGenerator()
        generator.wow.set_occurrence(1.0)

        values = [generator.step(0.001)[0] for _ in range(4001)]

        self.assertNotAlmostEqual(values[2000], values[4000])

    def test_zero_occurrence_keeps_disturbance_off(self):
        generator = WowFlutterGenerator()

        values = [generator.step(0.001) for _ in range(1000)]

        self.assertTrue(all(value == (0.0, 0.0, 0.0) for value in values))

    def test_episode_gate_is_reproducible(self):
        first = EpisodeGate(10)
        second = EpisodeGate(10)

        first_values = [first.step(0.1, 0.5, 1.0) for _ in range(100)]
        second_values = [second.step(0.1, 0.5, 1.0) for _ in range(100)]

        self.assertEqual(first_values, second_values)

    def test_full_occurrence_keeps_episode_active(self):
        gate = EpisodeGate(10)

        self.assertTrue(all(gate.step(0.1, 1.0, 1.0) for _ in range(100)))

    def test_partial_occurrence_has_active_and_inactive_episodes(self):
        gate = EpisodeGate(10)

        values = [gate.step(0.1, 0.5, 1.0) for _ in range(100)]

        self.assertIn(True, values)
        self.assertIn(False, values)

    def test_scheduler_converts_gui_time_to_fixed_steps(self):
        scheduler = FixedStepScheduler()

        steps, dropped = scheduler.consume(0.016)

        self.assertEqual(steps, 16)
        self.assertEqual(dropped, 0.0)

    def test_scheduler_limits_catch_up(self):
        scheduler = FixedStepScheduler()

        steps, dropped = scheduler.consume(0.25)

        self.assertEqual(steps, 100)
        self.assertAlmostEqual(dropped, 0.15)


if __name__ == "__main__":
    unittest.main()
