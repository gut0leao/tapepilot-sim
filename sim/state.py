"""Estado compartilhado pelo núcleo da simulação."""

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
    wow_disturbance: float = 0.0
    flutter_disturbance: float = 0.0
    speed_disturbance: float = 0.0
    runtime_lagged: bool = False
    dropped_time_s: float = 0.0

    reel_l_deg: float = 0.0
    reel_r_deg: float = 0.0
    capstan_deg: float = 0.0
