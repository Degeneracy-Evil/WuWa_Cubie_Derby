from __future__ import annotations
import random
from src.abilities.base import AbilityBase
from src.ranking import compute_ranking, get_rank


class KaAbility(AbilityBase):
    player_name = "卡"

    def on_dice_bonus(self, state, game_ctx) -> int:
        if state.name != self.player_name:
            return 0
        if not state.ka_activated:
            return 0
        if random.random() < 0.6:
            return 2
        return 0

    def on_movement_end(self, state, game_ctx) -> None:
        if state.name != self.player_name:
            return
        if state.ka_triggered:
            return
        players = game_ctx["players"]
        stacks = game_ctx["stacks"]
        ranking = compute_ranking(players, stacks)
        ka_rank = get_rank(self.player_name, ranking)
        if ka_rank == len(ranking):
            state.ka_triggered = True
            state.ka_activated = True
