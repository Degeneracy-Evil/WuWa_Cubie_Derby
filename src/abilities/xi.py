from __future__ import annotations
from src.abilities.base import AbilityBase
from src.ranking import compute_ranking, get_rank


class XiAbility(AbilityBase):
    player_name = "西"
    _marked: set[str] = set()

    def on_round_start(self, state, game_ctx) -> None:
        self._marked = set()
        players = game_ctx["players"]
        stacks = game_ctx["stacks"]
        ranking = compute_ranking(players, stacks)
        xi_rank = get_rank(self.player_name, ranking)
        if xi_rank > len(ranking):
            return
        xi_idx = xi_rank - 1
        for offset in (1, 2):
            above_idx = xi_idx - offset
            if above_idx >= 0:
                self._marked.add(ranking[above_idx])

    def on_dice_bonus(self, state, game_ctx) -> int:
        if state.name in self._marked:
            return -1
        return 0

    @property
    def marked(self) -> set[str]:
        return self._marked
