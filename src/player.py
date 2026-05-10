from __future__ import annotations
import random
from dataclasses import dataclass, field
from src.track import DeviceType, get_device


@dataclass
class PlayerState:
    name: str
    position: int = 0
    is_interferer: bool = False
    last_base_dice: int = 0
    prev_base_dice: int = 0
    met_x: bool = False
    met_x_round: int = -1
    ka_triggered: bool = False
    ka_activated: bool = False

    def dice_range(self) -> tuple[int, int]:
        if self.is_interferer:
            return (1, 6)
        return (1, 3)

    def roll_base_dice(self) -> int:
        lo, hi = self.dice_range()
        self.prev_base_dice = self.last_base_dice
        self.last_base_dice = random.randint(lo, hi)
        return self.last_base_dice
