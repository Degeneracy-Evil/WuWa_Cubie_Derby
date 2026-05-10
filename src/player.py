from __future__ import annotations
import random
from dataclasses import dataclass


@dataclass
class PlayerState:
    name: str
    position: int = 0
    is_interferer: bool = False

    def dice_range(self) -> tuple[int, int]:
        if self.is_interferer:
            return (1, 6)
        return (1, 3)

    def roll_base_dice(self) -> int:
        lo, hi = self.dice_range()
        return random.randint(lo, hi)
