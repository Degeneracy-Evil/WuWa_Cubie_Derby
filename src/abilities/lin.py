from __future__ import annotations
import random
from typing import Any
from src.abilities.base import AbilityBase


class LinAbility(AbilityBase):
    player_name = "琳"

    def __init__(self) -> None:
        self._mode: str = "normal"

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return 0
        r = random.random()
        if r < 0.6:
            self._mode = "double"
            return base_dice
        if r < 0.8:
            self._mode = "skip"
            return 0
        self._mode = "normal"
        return 0

    def on_dice_finalize(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return current
        if self._mode == "skip":
            return 0
        return current
