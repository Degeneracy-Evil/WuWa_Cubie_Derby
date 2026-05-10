from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase


class FeiAbility(AbilityBase):
    player_name = "绯"

    def __init__(self) -> None:
        self.met_round: int | None = None

    def on_stack_event(self, event_kind: str, pos: int, stack: list[str], actor: str | None, ctx: dict[str, Any]) -> None:
        if self.met_round is not None:
            return
        if self.player_name in stack and "X" in stack:
            self.met_round = ctx["round"]

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        if actor_name != self.player_name:
            return 0
        if self.met_round is None:
            return 0
        if ctx["round"] <= self.met_round:
            return 0
        return 1
