"""Controladores de velocidade do núcleo."""


class ProportionalController:
    """Controlador proporcional vigente, com saída normalizada e saturada."""

    def __init__(self, kp: float = 0.02):
        self.kp = kp

    def command(self, error: float) -> float:
        return max(min(self.kp * error, 1.0), -1.0)
