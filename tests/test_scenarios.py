import tempfile
import unittest
from pathlib import Path

from tools.run_scenarios import run_scenario


class HeadlessScenarioTests(unittest.TestCase):
    def test_all_declared_scenarios_pass(self):
        scenario_dir = Path(__file__).with_name("scenarios")
        with tempfile.TemporaryDirectory() as output:
            summaries = [
                run_scenario(path, Path(output))
                for path in sorted(scenario_dir.glob("*.json"))
            ]

        self.assertTrue(all(summary["passed"] for summary in summaries))


if __name__ == "__main__":
    unittest.main()
