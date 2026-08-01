"""Modelo de caracterização do protótipo TapePilot.

As equações deste módulo são intencionalmente simples e estão documentadas em
``docs/simulation-model.md``. O módulo não depende de Qt para poder ser testado
e reutilizado separadamente da interface.
"""

import math

from .controller import ProportionalController
from .encoder import VisualEncoder
from .faults import FaultModel
from .plant import FirstOrderPlant
from .runtime import FixedStepScheduler
from .state import SimState


class Simulator:
    """Simulador mínimo de velocidade, controle e movimento visual."""

    def __init__(self):
        self.s = SimState()
        self.controller = ProportionalController()
        self.plant = FirstOrderPlant()
        self.faults = FaultModel()
        self.encoder = VisualEncoder()
        self.scheduler = FixedStepScheduler()

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

        self.s.err = self.s.rpm_setpoint - self.s.rpm
        self.s.pwm = self.controller.command(self.s.err)

        target, self.s.tension = self.faults.apply_friction(
            self.s.rpm_setpoint,
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

        rpm_for_visual = self.encoder.measured_rpm(
            self.s.rpm, self.s.encoder_jitter
        )
        omega = (rpm_for_visual * 2 * math.pi) / 60.0

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
