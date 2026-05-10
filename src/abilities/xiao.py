from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase


class XiaoAbility(AbilityBase):
    player_name = "咲"

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return 0
        base_dices = ctx.get("base_dices")
        if base_dices is None:
            return 0
        min_dice = min(base_dices.values())
        if base_dice == min_dice:
            return 2
        return 0
