import unittest
from unittest.mock import patch

from sim.controller import ProportionalController
from sim.encoder import VisualEncoder
from sim.faults import FaultModel
from sim.plant import FirstOrderPlant


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


if __name__ == "__main__":
    unittest.main()
