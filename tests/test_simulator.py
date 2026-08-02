import unittest

from sim import Simulator


class SimulatorCharacterizationTests(unittest.TestCase):
    def test_transport_setpoints_match_current_prototype(self):
        expected = {
            "STOP": 0.0,
            "PLAY": 1800.0,
            "PAUSE": 300.0,
            "FF": 2600.0,
            "REW": 2600.0,
        }

        for mode, setpoint in expected.items():
            with self.subTest(mode=mode):
                simulator = Simulator()
                simulator.set_transport(mode)
                self.assertEqual(simulator.step(0.01).rpm_setpoint, setpoint)

    def test_pwm_is_saturated(self):
        simulator = Simulator()
        simulator.set_transport("PLAY")
        self.assertEqual(simulator.step(0.01).pwm, 1.0)

        simulator.s.rpm = 3000.0
        self.assertEqual(simulator.step(0.01).pwm, -1.0)

    def test_first_order_response_uses_elapsed_time(self):
        simulator = Simulator()
        simulator.set_transport("PLAY")

        state = simulator.step(0.25)

        self.assertAlmostEqual(state.rpm, 900.0)

    def test_friction_reduces_speed_and_produces_tension(self):
        no_friction = Simulator()
        no_friction.set_transport("PLAY")
        no_friction_state = no_friction.step(0.25)

        with_friction = Simulator()
        with_friction.set_transport("PLAY")
        with_friction.s.tape_friction = 1.0
        friction_state = with_friction.step(0.25)

        self.assertLess(friction_state.rpm, no_friction_state.rpm)
        self.assertGreater(friction_state.tension, 0.0)

    def test_stop_converges_toward_zero(self):
        simulator = Simulator()
        simulator.s.rpm = 1000.0
        simulator.set_transport("STOP")

        first = simulator.step(0.1).rpm
        second = simulator.step(0.1).rpm

        self.assertGreater(first, second)
        self.assertGreaterEqual(second, 0.0)

    def test_angles_advance_in_current_positive_direction(self):
        simulator = Simulator()
        simulator.set_transport("PLAY")

        state = simulator.step(0.01)

        self.assertGreater(state.capstan_deg, 0.0)
        self.assertGreater(state.reel_l_deg, 0.0)
        self.assertGreater(state.reel_r_deg, 0.0)

    def test_encoder_dropout_does_not_control_the_current_plant(self):
        simulator = Simulator()
        simulator.set_transport("PLAY")
        simulator.s.encoder_dropout = True

        for _ in range(10):
            state = simulator.step(0.001)

        self.assertEqual(state.encoder_pulse_count, 0)
        self.assertEqual(state.encoder_rpm_raw, 0.0)
        self.assertEqual(state.encoder_rpm_filtered, 0.0)
        self.assertGreater(state.rpm, 0.0)
        self.assertEqual(state.pwm, 1.0)


if __name__ == "__main__":
    unittest.main()
