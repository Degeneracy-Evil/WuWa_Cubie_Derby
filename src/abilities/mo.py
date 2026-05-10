from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase


class MoAbility(AbilityBase):
    player_name = "莫"

    def __init__(self) -> None:
        self._cycle = [3, 2, 1]
        self._round_idx: int = 0

    def on_roll_dice(self, actor_name: str, default_roll: int, ctx: dict[str, Any]) -> int | None:
        if actor_name != self.player_name:
            return None
        val = self._cycle[self._round_idx % 3]
        self._round_idx += 1
        return val
