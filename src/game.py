from __future__ import annotations
import random
from src.track import DeviceType, get_device, FINISH_POS, START_POS
from src.player import PlayerState
from src.ranking import compute_ranking, get_rank
from src.abilities.base import AbilityBase
from src.abilities import ALL_ABILITIES

NORMAL_NAMES = ("陆", "西", "娅", "绯", "卡", "菲")
FINISH = FINISH_POS
START = START_POS


class Game:
    __slots__ = (
        "round_num", "winner", "players", "stacks", "abilities",
        "_xi_ability", "first_round_order", "_fei", "_x",
    )

    def __init__(self) -> None:
        self.round_num = 1
        self.winner: str | None = None

        start_order = list(NORMAL_NAMES)
        random.shuffle(start_order)
        self.first_round_order = start_order

        self.players: dict[str, PlayerState] = {}
        for name in NORMAL_NAMES:
            self.players[name] = PlayerState(name=name, position=START)
        x_state = PlayerState(name="X", position=FINISH, is_interferer=True)
        self.players["X"] = x_state
        self._x = x_state
        self._fei = self.players["绯"]

        self.stacks: dict[int, list[str]] = {START: start_order[:]}
        self.abilities = [cls() for cls in ALL_ABILITIES]
        self._xi_ability = next((a for a in self.abilities if a.player_name == "西"), None)

    def run(self) -> str:
        while self.winner is None:
            self._run_round()
            if self.round_num > 500:
                break
        return self.winner or "UNKNOWN"

    def _run_round(self) -> None:
        order = self._generate_order()
        steps_map = self._roll_and_resolve(order)
        players = self.players
        stacks = self.stacks
        abilities = self.abilities
        round_num = self.round_num

        for name in order:
            if self.winner is not None:
                return
            steps = steps_map[name]
            if steps > 0:
                self._execute_movement(name, steps)
            if self.winner is not None:
                return
            mover = players[name]
            if not mover.is_interferer:
                ctx = {"players": players, "stacks": stacks, "round": round_num, "is_mover": True}
                for ab in abilities:
                    ab.on_movement_end(mover, ctx)

        self._apply_x_teleport()
        self.round_num += 1

    def _generate_order(self) -> list[str]:
        if self.round_num == 1:
            return self.first_round_order[:]
        order = list(NORMAL_NAMES)
        if self.round_num >= 3:
            order.append("X")
        random.shuffle(order)
        return order

    def _roll_and_resolve(self, order: list[str]) -> dict[str, int]:
        players = self.players
        stacks = self.stacks
        round_num = self.round_num
        abilities = self.abilities
        xi = self._xi_ability

        base_dices: dict[str, int] = {}
        for name in order:
            base_dices[name] = players[name].roll_base_dice()

        ctx_base = {"players": players, "stacks": stacks, "round": round_num}
        for ab in abilities:
            ab.on_round_start(None, ctx_base)

        results: dict[str, int] = {}
        for name in order:
            p = players[name]
            base = base_dices[name]
            bonus = 0
            for ab in abilities:
                if ab is xi:
                    continue
                bonus += ab.on_dice_bonus(p, {"players": players, "stacks": stacks, "round": round_num, "base_dice": base})
            results[name] = base + bonus

        if xi:
            marked = xi.marked
            for name in order:
                if name in marked:
                    v = results[name] - 1
                    results[name] = v if v > 1 else 1

        return results

    def _execute_movement(self, mover_name: str, steps: int) -> None:
        mover = self.players[mover_name]
        is_x = mover.is_interferer
        direction = -1 if is_x else 1
        moving_group = self._extract_moving_group(mover_name)
        current_pos = mover.position

        for step_idx in range(steps):
            if self.winner is not None:
                return
            next_pos = current_pos + direction
            if not is_x and next_pos >= FINISH:
                self._move_group_to_finish(moving_group, current_pos, mover_name)
                return
            if is_x and next_pos < START:
                next_pos = START

            self._move_group_to(moving_group, current_pos, next_pos, mover_name, is_x)
            self._check_fei_meets_x(next_pos)

            current_pos = next_pos
            if step_idx < steps - 1:
                moving_group = self._extract_moving_group(mover_name)

        self._resolve_device_chain(mover_name, is_x)

    def _resolve_device_chain(self, mover_name: str, is_x: bool) -> None:
        players = self.players
        stacks = self.stacks
        abilities = self.abilities
        round_num = self.round_num

        while True:
            if self.winner is not None:
                return
            mover = players[mover_name]
            device = get_device(mover.position)
            if device is None:
                return

            if device == DeviceType.DISRUPTION:
                ctx = {"players": players, "stacks": stacks, "round": round_num, "is_mover": True}
                for ab in abilities:
                    ab.on_device_trigger(device, mover, ctx)
                self._apply_disruption(mover.position)
                self._check_fei_meets_x(mover.position)
                return

            delta = 1 if device == DeviceType.FORWARD else -1
            ctx = {"players": players, "stacks": stacks, "round": round_num, "is_mover": True}
            for ab in abilities:
                delta += ab.on_device_trigger(device, mover, ctx)

            if delta == 0:
                return

            moving_group = self._extract_moving_group(mover_name)
            step_dir = 1 if delta > 0 else -1
            current_pos = mover.position

            for step_idx in range(abs(delta)):
                if self.winner is not None:
                    return
                next_pos = current_pos + step_dir
                if not is_x and next_pos >= FINISH:
                    self._move_group_to_finish(moving_group, current_pos, mover_name)
                    return
                if is_x and next_pos < START:
                    next_pos = START

                self._move_group_to(moving_group, current_pos, next_pos, mover_name, is_x)
                self._check_fei_meets_x(next_pos)

                current_pos = next_pos
                if step_idx < abs(delta) - 1:
                    moving_group = self._extract_moving_group(mover_name)

    def _extract_moving_group(self, mover_name: str) -> list[str]:
        mover = self.players[mover_name]
        pos = mover.position
        stacks = self.stacks
        stack = stacks.get(pos)
        if stack is None or mover_name not in stack:
            return [mover_name]
        idx = stack.index(mover_name)
        moving = stack[:idx + 1]
        remaining = stack[idx + 1:]
        if remaining:
            stacks[pos] = remaining
        else:
            del stacks[pos]
        return moving

    def _move_group_to(self, moving_group: list[str], from_pos: int, to_pos: int, mover_name: str, is_x: bool) -> None:
        stacks = self.stacks
        players = self.players

        if from_pos != to_pos:
            stack_from = stacks.get(from_pos)
            if stack_from is not None:
                mg_set = set(moving_group)
                remaining = [n for n in stack_from if n not in mg_set]
                if remaining:
                    stacks[from_pos] = remaining
                else:
                    del stacks[from_pos]

        existing = stacks.get(to_pos)
        if existing is None:
            existing = []

        if is_x:
            without_x = [n for n in moving_group if n != "X"]
            combined = without_x + existing
            combined.append("X")
        else:
            combined = moving_group + existing

        stacks[to_pos] = combined
        for name in combined:
            players[name].position = to_pos

    def _move_group_to_finish(self, moving_group: list[str], from_pos: int, mover_name: str) -> None:
        stacks = self.stacks
        players = self.players

        if from_pos != FINISH:
            stack_from = stacks.get(from_pos)
            if stack_from is not None:
                mg_set = set(moving_group)
                remaining = [n for n in stack_from if n not in mg_set]
                if remaining:
                    stacks[from_pos] = remaining
                else:
                    del stacks[from_pos]

        existing = stacks.get(FINISH)
        if existing is None:
            existing = []

        combined = moving_group + existing
        stacks[FINISH] = combined
        for name in combined:
            players[name].position = FINISH

        self._check_win()

    def _apply_disruption(self, pos: int) -> None:
        stacks = self.stacks
        stack = stacks.get(pos)
        if stack is None or len(stack) <= 1:
            return
        if "X" in stack:
            normal = [n for n in stack if n != "X"]
            random.shuffle(normal)
            normal.append("X")
            stacks[pos] = normal
        else:
            shuffled = stack[:]
            random.shuffle(shuffled)
            stacks[pos] = shuffled

    def _check_fei_meets_x(self, pos: int) -> None:
        stack = self.stacks.get(pos)
        if stack is not None and "绯" in stack and "X" in stack:
            fei = self._fei
            if not fei.met_x:
                fei.met_x = True
                fei.met_x_round = self.round_num

    def _check_win(self) -> None:
        players = self.players
        for name in NORMAL_NAMES:
            if players[name].position >= FINISH:
                ranking = compute_ranking(players, self.stacks)
                self.winner = ranking[0] if ranking else name
                return

    def _apply_x_teleport(self) -> None:
        if self.round_num < 3:
            return
        x = self._x
        players = self.players
        stacks = self.stacks
        ranking = compute_ranking(players, stacks)
        if not ranking:
            return
        last_place_pos = players[ranking[-1]].position
        x_pos = x.position
        if x_pos >= last_place_pos:
            return
        x_stack = stacks.get(x_pos)
        if x_stack is not None and "X" in x_stack and x_stack.index("X") > 0:
            return

        if x_stack is not None:
            new_stack = [n for n in x_stack if n != "X"]
            if new_stack:
                stacks[x_pos] = new_stack
            else:
                del stacks[x_pos]
        x.position = FINISH
        existing = stacks.get(FINISH)
        if existing is None:
            stacks[FINISH] = ["X"]
        else:
            existing.append("X")
            stacks[FINISH] = existing
        self._check_fei_meets_x(FINISH)
