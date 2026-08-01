"""Agendamento determinístico do núcleo da simulação."""


class FixedStepScheduler:
    """Converte tempo real em uma quantidade limitada de passos fixos."""

    def __init__(self, step_seconds: float = 0.001, max_catch_up: float = 0.1):
        self.step_seconds = step_seconds
        self.max_catch_up = max_catch_up
        self.accumulator = 0.0

    def consume(self, elapsed: float) -> tuple[int, float]:
        accepted = min(max(elapsed, 0.0), self.max_catch_up)
        dropped = max(elapsed - accepted, 0.0)
        self.accumulator += accepted
        steps = int((self.accumulator + 1e-12) / self.step_seconds)
        self.accumulator -= steps * self.step_seconds
        return steps, dropped
