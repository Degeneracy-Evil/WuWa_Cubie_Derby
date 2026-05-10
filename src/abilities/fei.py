from __future__ import annotations
from src.abilities.base import AbilityBase


class FeiAbility(AbilityBase):
    player_name = "绯"

    def on_dice_bonus(self, state, game_ctx) -> int:
        if state.name != self.player_name:
            return 0
        if not state.met_x:
            return 0
        current_round = game_ctx.get("round", 1)
        if current_round <= state.met_x_round:
            return 0
        return 1
