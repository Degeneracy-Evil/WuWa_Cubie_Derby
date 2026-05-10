from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase


class YaAbility(AbilityBase):
    player_name = "娅"

    def __init__(self) -> None:
        self.prev_base: int = 0
        self.last_base: int = 0

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return 0
        self.prev_base, self.last_base = self.last_base, base_dice
        if self.prev_base == 0:
            return 0
        if base_dice == self.prev_base:
            return 2
        return 0
