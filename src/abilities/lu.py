from __future__ import annotations
import random
from src.abilities.base import AbilityBase
from src.track import DeviceType


class LuAbility(AbilityBase):
    player_name = "陆"

    def on_device_trigger(self, device_type: DeviceType, state, game_ctx) -> int:
        if state.name != self.player_name:
            return 0
        if not game_ctx.get("is_mover", False):
            return 0
        if device_type == DeviceType.FORWARD:
            return 3
        if device_type == DeviceType.BACKWARD:
            return -1
        return 0
