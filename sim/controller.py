"""Controladores de velocidade do núcleo."""

from dataclasses import dataclass


class ProportionalController:
    """Controlador proporcional vigente, com saída normalizada e saturada."""

    def __init__(self, kp: float = 0.02):
        self.kp = kp

    def command(self, error: float) -> float:
        return max(min(self.kp * error, 1.0), -1.0)


@dataclass
class ControlOutput:
    nominal: float = 0.0
    p: float = 0.0
    i: float = 0.0
    d: float = 0.0
    transfer_bias: float = 0.0
    requested: float = 0.0
    applied: float = 0.0
    saturated: bool = False
    integral_blocked: bool = False


class DigitalServoController:
    """PID somado ao comando nominal, com transferência suave."""

    def __init__(
        self,
        kp: float = 0.001,
        ki: float = 0.002,
        kd: float = 0.0,
        transition_seconds: float = 0.250,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.transition_seconds = transition_seconds
        self.enabled = False
        self.integral = 0.0
        self.previous_measurement = None
        self._measurement_elapsed = 0.0
        self._derivative_term = 0.0
        self.transfer_bias = 0.0
        self._bias_decay_rate = 0.0
        self._exit_correction = 0.0
        self._exit_remaining = 0.0
        self._just_enabled = False
        self.last = ControlOutput()

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return min(max(value, lower), upper)

    def set_enabled(self, enabled: bool, setpoint: float, measurement: float):
        if enabled == self.enabled:
            return
        if enabled:
            error = setpoint - measurement
            p = self.kp * error
            d = 0.0
            self.transfer_bias = -(p + self.integral + d)
            self._bias_decay_rate = (
                abs(self.transfer_bias) / self.transition_seconds
                if self.transition_seconds > 0.0
                else abs(self.transfer_bias)
            )
            self.previous_measurement = measurement
            self._measurement_elapsed = 0.0
            self._derivative_term = 0.0
            self._exit_remaining = 0.0
            self._just_enabled = True
        else:
            self._exit_correction = self.last.applied - self.last.nominal
            self._exit_remaining = self.transition_seconds
            self.transfer_bias = 0.0
            self.integral = 0.0
            self.previous_measurement = None
            self._measurement_elapsed = 0.0
            self._derivative_term = 0.0
        self.enabled = enabled

    def _decay_bias(self, dt: float):
        amount = self._bias_decay_rate * dt
        if self.transfer_bias > 0.0:
            self.transfer_bias = max(self.transfer_bias - amount, 0.0)
        else:
            self.transfer_bias = min(self.transfer_bias + amount, 0.0)

    def step(
        self,
        setpoint: float,
        measurement: float,
        nominal: float,
        dt: float,
        measurement_updated: bool = True,
    ) -> ControlOutput:
        nominal = self._clamp(nominal, -1.0, 1.0)
        if not self.enabled:
            correction = 0.0
            if self._exit_remaining > 0.0:
                fraction = self._exit_remaining / self.transition_seconds
                correction = self._exit_correction * fraction
                self._exit_remaining = max(self._exit_remaining - dt, 0.0)
            requested = nominal + correction
            applied = self._clamp(requested, -1.0, 1.0)
            self.last = ControlOutput(
                nominal=nominal,
                transfer_bias=correction,
                requested=requested,
                applied=applied,
                saturated=requested != applied,
            )
            return self.last

        error = setpoint - measurement
        p = self.kp * error
        self._measurement_elapsed += dt
        if measurement_updated and self._measurement_elapsed > 0.0:
            measurement_rate = 0.0
            if self.previous_measurement is not None:
                measurement_rate = (
                    measurement - self.previous_measurement
                ) / self._measurement_elapsed
            self._derivative_term = -self.kd * measurement_rate
            self.previous_measurement = measurement
            self._measurement_elapsed = 0.0
        d = self._derivative_term

        lower_i = -1.0 - nominal
        upper_i = 1.0 - nominal
        candidate_i = self.integral
        if not self._just_enabled:
            candidate_i = self._clamp(
                self.integral + self.ki * error * dt, lower_i, upper_i
            )
        candidate_requested = nominal + p + candidate_i + d + self.transfer_bias
        integral_blocked = (
            candidate_requested > 1.0 and error > 0.0
        ) or (candidate_requested < -1.0 and error < 0.0)
        if not integral_blocked:
            self.integral = candidate_i

        requested = nominal + p + self.integral + d + self.transfer_bias
        applied = self._clamp(requested, -1.0, 1.0)
        output = ControlOutput(
            nominal=nominal,
            p=p,
            i=self.integral,
            d=d,
            transfer_bias=self.transfer_bias,
            requested=requested,
            applied=applied,
            saturated=requested != applied,
            integral_blocked=integral_blocked,
        )
        self._decay_bias(dt)
        self._just_enabled = False
        self.last = output
        return output
