"""Métricas quantitativas da resposta da simulação."""

import math
from collections import deque


class RollingRmsError:
    """Erro RMS percentual após estabilização, em uma janela móvel."""

    def __init__(self, window_seconds: float = 5.0, settling_seconds: float = 3.0):
        self.window_seconds = window_seconds
        self.settling_seconds = settling_seconds
        self.setpoint = None
        self.context = None
        self.elapsed = 0.0
        self.samples = deque()
        self.sum_squares = 0.0

    def reset(self, setpoint: float, context=None):
        self.setpoint = setpoint
        self.context = context
        self.elapsed = 0.0
        self.samples.clear()
        self.sum_squares = 0.0

    def step(
        self, dt: float, setpoint: float, actual: float, context=None
    ) -> float | None:
        if setpoint != self.setpoint or context != self.context:
            self.reset(setpoint, context)
        self.elapsed += dt
        if setpoint == 0.0 or self.elapsed < self.settling_seconds:
            return None

        error_percent = (setpoint - actual) / abs(setpoint) * 100.0
        squared = error_percent * error_percent
        self.samples.append((self.elapsed, squared))
        self.sum_squares += squared
        cutoff = self.elapsed - self.window_seconds
        while self.samples and self.samples[0][0] < cutoff:
            _, expired = self.samples.popleft()
            self.sum_squares -= expired
        # A soma é não negativa por definição, mas subtrações repetidas da
        # janela podem produzir um resíduo negativo na ordem do erro de ponto
        # flutuante depois de milhares de passos.
        self.sum_squares = max(self.sum_squares, 0.0)
        return math.sqrt(self.sum_squares / len(self.samples))
