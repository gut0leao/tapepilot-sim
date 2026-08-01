"""Núcleo independente da interface gráfica do TapePilot."""

from .model import Simulator
from .state import SimState

__all__ = ["SimState", "Simulator"]
