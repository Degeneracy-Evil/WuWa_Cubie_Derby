from __future__ import annotations
from src.abilities.base import AbilityBase


class YaAbility(AbilityBase):
    player_name = "娅"

    def on_dice_bonus(self, state, game_ctx) -> int:
        if state.name != self.player_name:
            return 0
        round_num = game_ctx.get("round", 1)
        if round_num <= 1:
            return 0
        if state.prev_base_dice == 0:
            return 0
        current_base = game_ctx.get("base_dice", 0)
        if current_base == state.prev_base_dice:
            return 2
        return 0
