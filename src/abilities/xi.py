from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase
from src.ranking import compute_ranking, get_rank


class XiAbility(AbilityBase):
    player_name = "西"
    def __init__(self) -> None:
        self.marked: set[str] = set()

    def on_round_start(self, ctx: dict[str, Any]) -> None:
        self.marked = set()
        players = ctx["players"]
        stacks = ctx["stacks"]
        ranking = compute_ranking(players, stacks)
        if self.player_name not in ranking:
            return
        xi_idx = ranking.index(self.player_name)
        for offset in (1, 2):
            above_idx = xi_idx - offset
            if above_idx >= 0:
                self.marked.add(ranking[above_idx])

    def on_dice_finalize(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name in self.marked:
            return max(1, current - 1)
        return current
