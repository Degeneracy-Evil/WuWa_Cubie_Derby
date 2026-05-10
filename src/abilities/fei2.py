from __future__ import annotations
import random
from src.abilities.base import AbilityBase


class Fei2Ability(AbilityBase):
    player_name = "菲"

    def on_dice_bonus(self, state, game_ctx) -> int:
        if state.name != self.player_name:
            return 0
        if random.random() < 0.5:
            return 1
        return 0
