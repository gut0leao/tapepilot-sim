"""Modelo de caracterização do protótipo TapePilot.

As equações deste módulo são intencionalmente simples e estão documentadas em
``docs/simulation-model.md``. O módulo não depende de Qt para poder ser testado
e reutilizado separadamente da interface.
"""

import math

from .controller import DigitalServoController
from .encoder import DiscreteEncoder
from .faults import FaultModel
from .metrics import RollingRmsError
from .plant import FirstOrderPlant
from .runtime import FixedStepScheduler
from .state import SimState


class Simulator:
    """Simulador mínimo de velocidade, controle e movimento visual."""

    def __init__(self):
        self.s = SimState()
        self.controller = DigitalServoController()
        self.plant_max_rpm = 3000.0
        self.plant = FirstOrderPlant()
        self.faults = FaultModel()
        self.encoder = DiscreteEncoder()
        self.scheduler = FixedStepScheduler()
        self.rms_error = RollingRmsError()

    @property
    def Kp(self):
        """Mantém compatibilidade com o atributo público do protótipo."""
        return self.controller.kp

    @Kp.setter
    def Kp(self, value):
        self.controller.kp = value

    @property
    def tau(self):
        """Mantém compatibilidade com o atributo público do protótipo."""
        return self.plant.tau

    @tau.setter
    def tau(self, value):
        self.plant.tau = value

    def set_transport(self, mode: str):
        self.s.transport = mode

    def advance(self, elapsed: float):
        """Avança o núcleo em passos fixos a partir do tempo real transcorrido."""
        steps, dropped = self.scheduler.consume(elapsed)
        self.s.runtime_lagged = dropped > 0.0
        self.s.dropped_time_s = dropped
        for _ in range(steps):
            self.step(self.scheduler.step_seconds)
        return self.s

    def step(self, dt: float):
        if self.s.transport == "PLAY":
            self.s.rpm_setpoint = 1800.0
        elif self.s.transport in {"FF", "REW"}:
            self.s.rpm_setpoint = 2600.0
        elif self.s.transport == "PAUSE":
            self.s.rpm_setpoint = 300.0
        else:
            self.s.rpm_setpoint = 0.0

        self.s.err = self.s.rpm_setpoint - self.s.encoder_rpm_filtered
        nominal = self.s.rpm_setpoint / self.plant_max_rpm
        self.s.control_fallback = (
            self.s.digital_tach_enabled and self.s.encoder_dropout
        )
        self.controller.set_enabled(
            self.s.digital_tach_enabled and not self.s.control_fallback,
            self.s.rpm_setpoint,
            self.s.encoder_rpm_filtered,
        )
        control = self.controller.step(
            self.s.rpm_setpoint,
            self.s.encoder_rpm_filtered,
            nominal,
            dt,
            self.s.encoder_measurement_updated,
        )
        self.s.command_nominal = control.nominal
        self.s.pid_p = control.p
        self.s.pid_i = control.i
        self.s.pid_d = control.d
        self.s.transfer_bias = control.transfer_bias
        self.s.command_requested = control.requested
        self.s.command_applied = control.applied
        self.s.actuator_saturated = control.saturated
        self.s.integral_blocked = control.integral_blocked
        self.s.pwm = control.applied
        if control.saturated:
            self.s.saturated_time_s += dt

        target, self.s.tension = self.faults.apply_friction(
            max(self.s.command_applied, 0.0) * self.plant_max_rpm,
            self.s.pwm,
            self.s.tape_friction,
        )
        (
            target,
            self.s.wow_disturbance,
            self.s.flutter_disturbance,
            self.s.speed_disturbance,
        ) = self.faults.apply_speed_disturbance(target, dt)
        self.s.rpm = self.plant.advance(self.s.rpm, target, dt)
        rms_context = (
            self.s.digital_tach_enabled,
            self.s.tape_friction,
            self.s.encoder_jitter,
            self.s.encoder_pulse_loss,
            self.s.encoder_dropout,
            self.controller.kp,
            self.controller.ki,
            self.controller.kd,
            self.faults.disturbances.wow.frequency_hz,
            self.faults.disturbances.wow.amplitude,
            self.faults.disturbances.wow.occurrence,
            self.faults.disturbances.wow.mean_duration,
            self.faults.disturbances.flutter.frequency_hz,
            self.faults.disturbances.flutter.amplitude,
            self.faults.disturbances.flutter.occurrence,
            self.faults.disturbances.flutter.mean_duration,
        )
        self.s.rms_error_percent = self.rms_error.step(
            dt, self.s.rpm_setpoint, self.s.rpm, rms_context
        )

        (
            self.s.encoder_pulse_count,
            self.s.encoder_rpm_raw,
            self.s.encoder_rpm_filtered,
            self.s.encoder_measurement_updated,
        ) = self.encoder.step(
            self.s.rpm,
            dt,
            self.s.encoder_jitter,
            self.s.encoder_pulse_loss,
            self.s.encoder_dropout,
        )
        omega = (self.s.rpm * 2 * math.pi) / 60.0

        self.s.capstan_deg = (
            self.s.capstan_deg + math.degrees(omega * dt)
        ) % 360.0
        self.s.reel_l_deg = (
            self.s.reel_l_deg + math.degrees(0.6 * omega * dt)
        ) % 360.0
        self.s.reel_r_deg = (
            self.s.reel_r_deg + math.degrees(0.9 * omega * dt)
        ) % 360.0

        return self.s
