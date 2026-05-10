from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase


class AnAbility(AbilityBase):
    player_name = "岸"

    def on_roll_dice(self, actor_name: str, default_roll: int, ctx: dict[str, Any]) -> int | None:
        if actor_name != self.player_name:
            return None
        import random
        return random.choice([2, 3])
