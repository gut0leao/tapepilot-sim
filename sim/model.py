"""Modelo de caracterização do protótipo TapePilot.

As equações deste módulo são intencionalmente simples e estão documentadas em
``docs/simulation-model.md``. O módulo não depende de Qt para poder ser testado
e reutilizado separadamente da interface.
"""

import math
import random
from dataclasses import dataclass


@dataclass
class SimState:
    """Estado instantâneo da simulação."""

    transport: str = "STOP"
    rpm_setpoint: float = 0.0
    rpm: float = 0.0
    pwm: float = 0.0
    err: float = 0.0
    tension: float = 0.0

    tape_friction: float = 0.0
    encoder_jitter: float = 0.0

    reel_l_deg: float = 0.0
    reel_r_deg: float = 0.0
    capstan_deg: float = 0.0


class Simulator:
    """Simulador mínimo de velocidade, controle e movimento visual."""

    def __init__(self):
        self.s = SimState()
        self.Kp = 0.02
        self.tau = 0.25

    def set_transport(self, mode: str):
        self.s.transport = mode

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
        self.s.pwm = max(min(self.Kp * self.s.err, 1.0), -1.0)

        friction_load = self.s.tape_friction * 600.0
        self.s.tension = self.s.tape_friction * (
            0.3 + 0.7 * abs(self.s.pwm)
        )

        target = self.s.rpm_setpoint - friction_load * abs(self.s.pwm)
        target = max(target, 0.0)

        alpha = dt / (self.tau + dt)
        self.s.rpm = (1 - alpha) * self.s.rpm + alpha * target

        jitter = random.gauss(0.0, 1.0) * self.s.encoder_jitter * 20.0
        rpm_for_visual = max(self.s.rpm + jitter, 0.0)
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
