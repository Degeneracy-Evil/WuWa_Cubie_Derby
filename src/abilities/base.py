from __future__ import annotations
from typing import Any
from src.track import DeviceType


class AbilityBase:
    player_name: str = ""

    def on_game_start(self, ctx: dict[str, Any]) -> None:
        pass

    def on_round_start(self, ctx: dict[str, Any]) -> None:
        pass

    def on_roll_dice(self, actor_name: str, default_roll: int, ctx: dict[str, Any]) -> int | None:
        return None

    def on_dice_bonus(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        return 0

    def on_dice_finalize(self, actor_name: str, base_dice: int, current: int, ctx: dict[str, Any]) -> int:
        return current

    def on_stack_event(self, event_kind: str, pos: int, stack: list[str], actor: str | None, ctx: dict[str, Any]) -> None:
        pass

    def on_device_trigger(self, device_type: DeviceType, mover_name: str, ctx: dict[str, Any]) -> int:
        return 0

    def on_movement_end(self, mover_name: str, ctx: dict[str, Any]) -> None:
        pass

    def on_step_end(self, mover_name: str, from_pos: int, to_pos: int, ctx: dict[str, Any]) -> bool:
        return False

    def on_round_end(self, ctx: dict[str, Any]) -> None:
        pass
