from __future__ import annotations
from typing import Any
from src.abilities.base import AbilityBase


class AiAbility(AbilityBase):
    player_name = "爱"
    MIDPOINT = 16

    def __init__(self) -> None:
        self._triggered: bool = False

    def on_step_end(self, mover_name: str, from_pos: int, to_pos: int, ctx: dict[str, Any]) -> bool:
        if mover_name != self.player_name:
            return False
        if self._triggered:
            return False
        if from_pos >= self.MIDPOINT:
            return False
        if to_pos < self.MIDPOINT:
            return False
        players = ctx["players"]
        stacks = ctx["stacks"]
        ai_pos = players[self.player_name].position
        nearest_name: str | None = None
        nearest_dist: int = 999
        for name, p in players.items():
            if name == self.player_name or p.is_interferer:
                continue
            if p.position > ai_pos:
                dist = p.position - ai_pos
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_name = name
        if nearest_name is None:
            return False
        self._triggered = True
        target_pos = players[nearest_name].position
        ai_stack = stacks.get(ai_pos)
        if ai_stack is not None and self.player_name in ai_stack:
            idx = ai_stack.index(self.player_name)
            ai_stack.pop(idx)
            if not ai_stack:
                del stacks[ai_pos]
        target_stack = stacks.get(target_pos)
        if target_stack is None:
            stacks[target_pos] = [self.player_name]
        else:
            target_stack.insert(0, self.player_name)
        players[self.player_name].position = target_pos
        return True
