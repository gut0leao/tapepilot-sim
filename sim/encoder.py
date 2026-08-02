"""Encoder incremental discreto e falhas de medição."""

import math
import random


class DiscreteEncoder:
    """Converte rotação física em pulsos e estima RPM por janela."""

    def __init__(
        self,
        pulses_per_revolution: int = 100,
        measurement_window_s: float = 0.010,
        filter_time_constant_s: float = 0.050,
        random_seed: int = 3301,
    ):
        self.pulses_per_revolution = pulses_per_revolution
        self.measurement_window_s = measurement_window_s
        self.filter_time_constant_s = filter_time_constant_s
        self.random = random.Random(random_seed)
        self._pulse_phase = 0.0
        self._window_elapsed = 0.0
        self._window_pulses = 0
        self.total_pulses = 0
        self.raw_rpm = 0.0
        self.filtered_rpm = 0.0

    def step(
        self,
        physical_rpm: float,
        dt: float,
        jitter_level: float = 0.0,
        pulse_loss: float = 0.0,
        dropout: bool = False,
    ) -> tuple[int, float, float, bool]:
        """Devolve pulsos, RPM bruta/filtrada e sinal de nova medição."""
        jitter_level = min(max(jitter_level, 0.0), 1.0)
        pulse_loss = min(max(pulse_loss, 0.0), 1.0)
        generated = max(physical_rpm, 0.0) / 60.0 * dt
        generated *= self.pulses_per_revolution
        self._pulse_phase += generated
        whole_pulses = math.floor(self._pulse_phase)
        self._pulse_phase -= whole_pulses

        accepted = 0
        if not dropout:
            for _ in range(whole_pulses):
                if self.random.random() >= pulse_loss:
                    accepted += 1

        self.total_pulses += accepted
        self._window_pulses += accepted
        self._window_elapsed += dt

        measurement_updated = self._window_elapsed >= self.measurement_window_s
        if measurement_updated:
            rpm_from_pulses = (
                self._window_pulses
                * 60.0
                / (self.pulses_per_revolution * self._window_elapsed)
            )
            noise = self.random.gauss(0.0, 1.0) * jitter_level * 20.0
            self.raw_rpm = max(rpm_from_pulses + noise, 0.0)
            alpha = 1.0 - math.exp(
                -self._window_elapsed / self.filter_time_constant_s
            )
            self.filtered_rpm += alpha * (self.raw_rpm - self.filtered_rpm)
            self._window_elapsed = 0.0
            self._window_pulses = 0

        return (
            self.total_pulses,
            self.raw_rpm,
            self.filtered_rpm,
            measurement_updated,
        )
