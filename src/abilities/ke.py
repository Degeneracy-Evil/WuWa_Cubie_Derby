from __future__ import annotations
import random
from typing import Any
from src.abilities.base import AbilityBase


class KeAbility(AbilityBase):
    player_name = "珂"

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return 0
        if random.random() < 0.28:
            return base_dice
        return 0
