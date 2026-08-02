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
    digital_tach_enabled: bool = False
    control_fallback: bool = False
    command_nominal: float = 0.0
    pid_p: float = 0.0
    pid_i: float = 0.0
    pid_d: float = 0.0
    transfer_bias: float = 0.0
    command_requested: float = 0.0
    command_applied: float = 0.0
    actuator_saturated: bool = False
    integral_blocked: bool = False
    saturated_time_s: float = 0.0
    rms_error_percent: float | None = None

    tape_friction: float = 0.0
    encoder_jitter: float = 0.0
    encoder_pulse_loss: float = 0.0
    encoder_dropout: bool = False
    encoder_pulse_count: int = 0
    encoder_rpm_raw: float = 0.0
    encoder_rpm_filtered: float = 0.0
    encoder_measurement_updated: bool = False
    wow_disturbance: float = 0.0
    flutter_disturbance: float = 0.0
    speed_disturbance: float = 0.0
    runtime_lagged: bool = False
    dropped_time_s: float = 0.0

    reel_l_deg: float = 0.0
    reel_r_deg: float = 0.0
    capstan_deg: float = 0.0
