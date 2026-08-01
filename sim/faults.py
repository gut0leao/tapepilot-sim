"""Efeitos vigentes de atrito e tensão simulada."""


class FaultModel:
    """Calcula carga e tensão sem alterar as fórmulas do baseline."""

    def apply_friction(
        self, setpoint_rpm: float, pwm: float, tape_friction: float
    ) -> tuple[float, float]:
        friction_load = tape_friction * 600.0
        tension = tape_friction * (0.3 + 0.7 * abs(pwm))
        target_rpm = setpoint_rpm - friction_load * abs(pwm)
        return max(target_rpm, 0.0), tension
