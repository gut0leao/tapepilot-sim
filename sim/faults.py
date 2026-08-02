"""Efeitos de atrito, tensão, wow e flutter."""

import math
import random


class SmoothRandomSource:
    """Produz variação pseudoaleatória filtrada e reproduzível."""

    def __init__(self, seed: int):
        self.random = random.Random(seed)
        self.elapsed = 0.0
        self.value = 0.0
        self.target = self.random.uniform(-1.0, 1.0)

    def step(
        self, dt: float, update_interval: float, smoothing_seconds: float
    ) -> float:
        self.elapsed += dt
        while self.elapsed >= update_interval:
            self.elapsed -= update_interval
            self.target = self.random.uniform(-1.0, 1.0)
        blend = min(max(dt / smoothing_seconds, 0.0), 1.0)
        self.value += (self.target - self.value) * blend
        return self.value


class EpisodeGate:
    """Liga e desliga episódios com duração e ocorrência médias."""

    def __init__(self, seed: int):
        self.random = random.Random(seed)
        self.active = False
        self.remaining = 0.0
        self.initialized = False
        self.last_occurrence = 0.0

    def _varied(self, mean: float) -> float:
        return max(mean * self.random.uniform(0.5, 1.5), 0.001)

    def step(self, dt: float, occurrence: float, mean_duration: float) -> bool:
        occurrence = min(max(occurrence, 0.0), 1.0)
        if occurrence != self.last_occurrence:
            self.initialized = False
            self.remaining = 0.0
            self.last_occurrence = occurrence
        if occurrence <= 0.0:
            self.active = False
            self.remaining = 0.0
            self.initialized = False
            return False
        if occurrence >= 1.0:
            self.active = True
            self.remaining = 0.0
            self.initialized = False
            return True

        mean_off = mean_duration * (1.0 - occurrence) / occurrence
        if not self.initialized:
            self.active = self.random.random() < occurrence
            mean_state_duration = mean_duration if self.active else mean_off
            self.remaining = self._varied(mean_state_duration)
            self.initialized = True

        self.remaining -= dt
        if self.remaining <= 0.0:
            self.active = not self.active
            if self.active:
                self.remaining = self._varied(mean_duration)
            else:
                self.remaining = self._varied(mean_off)
        return self.active


class NaturalDisturbance:
    """Perturbação irregular com pequena componente periódica."""

    def __init__(
        self,
        frequency_hz: float,
        amplitude: float,
        frequency_range: tuple[float, float],
        amplitude_range: tuple[float, float],
        random_seed: int,
        periodic_fraction: float,
        envelope_interval: float,
        occurrence: float,
        mean_duration: float,
        ramp_seconds: float = 0.1,
    ):
        self.frequency_range = frequency_range
        self.amplitude_range = amplitude_range
        self.ramp_seconds = ramp_seconds
        self.phase = 0.0
        self.current_amplitude = 0.0
        self.occurrence = occurrence
        self.mean_duration = mean_duration
        self.periodic_fraction = periodic_fraction
        self.envelope_interval = envelope_interval
        self.noise = SmoothRandomSource(random_seed)
        self.envelope = SmoothRandomSource(random_seed + 1)
        self.episodes = EpisodeGate(random_seed + 2)
        self.set_frequency(frequency_hz)
        self.set_amplitude(amplitude)

    def set_frequency(self, value: float):
        self.frequency_hz = min(
            max(value, self.frequency_range[0]), self.frequency_range[1]
        )

    def set_amplitude(self, value: float):
        self.amplitude = min(
            max(value, self.amplitude_range[0]), self.amplitude_range[1]
        )

    def set_occurrence(self, value: float):
        self.occurrence = min(max(value, 0.0), 1.0)

    def set_duration(self, value: float):
        self.mean_duration = max(value, 0.001)

    def step(self, dt: float) -> float:
        active = self.episodes.step(dt, self.occurrence, self.mean_duration)
        target = self.amplitude if active else 0.0
        blend = min(max(dt / self.ramp_seconds, 0.0), 1.0)
        self.current_amplitude += (target - self.current_amplitude) * blend
        characteristic_period = 1.0 / self.frequency_hz
        irregular = self.noise.step(
            dt,
            update_interval=characteristic_period / 2.0,
            smoothing_seconds=characteristic_period / (2.0 * math.pi),
        )
        envelope_noise = self.envelope.step(
            dt,
            update_interval=self.envelope_interval,
            smoothing_seconds=self.envelope_interval,
        )
        envelope = 0.65 + 0.35 * envelope_noise
        self.phase = (self.phase + 2.0 * math.pi * self.frequency_hz * dt) % (
            2.0 * math.pi
        )
        periodic = math.sin(self.phase)
        mixed = (
            (1.0 - self.periodic_fraction) * irregular
            + self.periodic_fraction * periodic
        )
        return self.current_amplitude * envelope * mixed


class WowFlutterGenerator:
    """Soma os componentes independentes de wow e flutter."""

    def __init__(self):
        self.wow = NaturalDisturbance(
            0.5, 0.01, (0.1, 2.0), (0.0, 0.03), 1103, 0.15, 2.0, 0.0, 3.0
        )
        self.flutter = NaturalDisturbance(
            8.0, 0.003, (2.0, 20.0), (0.0, 0.01), 2207, 0.10, 0.5, 0.0, 0.5
        )

    def step(self, dt: float) -> tuple[float, float, float]:
        wow = self.wow.step(dt)
        flutter = self.flutter.step(dt)
        return wow, flutter, wow + flutter


class FaultModel:
    """Calcula carga, tensão e perturbações físicas."""

    def __init__(self):
        self.disturbances = WowFlutterGenerator()

    def apply_friction(
        self, setpoint_rpm: float, pwm: float, tape_friction: float
    ) -> tuple[float, float]:
        friction_load = tape_friction * 600.0
        tension = tape_friction * (0.3 + 0.7 * abs(pwm))
        target_rpm = setpoint_rpm - friction_load * abs(pwm)
        return max(target_rpm, 0.0), tension

    def apply_speed_disturbance(
        self, target_rpm: float, dt: float
    ) -> tuple[float, float, float, float]:
        wow, flutter, total = self.disturbances.step(dt)
        return max(target_rpm * (1.0 + total), 0.0), wow, flutter, total
