from __future__ import annotations
from src.track import DeviceType


class AbilityBase:
    player_name: str = ""

    def on_dice_bonus(self, state, game_ctx) -> int:
        return 0

    def on_device_trigger(self, device_type: DeviceType, state, game_ctx) -> int:
        return 0

    def on_round_start(self, state, game_ctx) -> None:
        pass

    def on_movement_end(self, state, game_ctx) -> None:
        pass

    def on_round_end(self, state, game_ctx) -> None:
        pass
