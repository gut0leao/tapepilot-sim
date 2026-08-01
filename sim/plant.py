"""Dinâmica vigente da planta simulada."""


class FirstOrderPlant:
    """Resposta de primeira ordem usada pelo protótipo atual."""

    def __init__(self, tau: float = 0.25):
        self.tau = tau

    def advance(self, current_rpm: float, target_rpm: float, dt: float) -> float:
        alpha = dt / (self.tau + dt)
        return (1 - alpha) * current_rpm + alpha * target_rpm
