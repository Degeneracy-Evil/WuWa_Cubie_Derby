from __future__ import annotations
import random
from typing import Any
from src.abilities.base import AbilityBase
from src.track import DeviceType


class LuAbility(AbilityBase):
    player_name = "陆"

    def on_device_trigger(self, device_type: DeviceType, mover_name: str, ctx: dict[str, Any]) -> int:
        if mover_name != self.player_name:
            return 0
        if device_type == DeviceType.FORWARD:
            return 3
        if device_type == DeviceType.BACKWARD:
            return -1
        return 0
