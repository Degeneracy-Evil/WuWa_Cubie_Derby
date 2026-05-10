from __future__ import annotations
import random
from typing import Any
from src.abilities.base import AbilityBase
from src.ranking import compute_ranking, get_rank


class KaAbility(AbilityBase):
    player_name = "卡"

    def __init__(self) -> None:
        self.activated: bool = False
        self.triggered_once: bool = False

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return 0
        if not self.activated:
            return 0
        if random.random() < 0.6:
            return 2
        return 0

    def on_movement_end(self, mover_name: str, ctx: dict[str, Any]) -> None:
        if mover_name != self.player_name:
            return
        if self.triggered_once:
            return
        players = ctx["players"]
        stacks = ctx["stacks"]
        ranking = compute_ranking(players, stacks)
        ka_rank = get_rank(self.player_name, ranking)
        if ka_rank == len(ranking):
            self.triggered_once = True
            self.activated = True
