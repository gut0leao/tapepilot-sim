"""Medição visual vigente associada ao encoder."""

import random


class VisualEncoder:
    """Aplica o jitter apenas visual do baseline atual."""

    def measured_rpm(self, physical_rpm: float, jitter_level: float) -> float:
        jitter = random.gauss(0.0, 1.0) * jitter_level * 20.0
        return max(physical_rpm + jitter, 0.0)
