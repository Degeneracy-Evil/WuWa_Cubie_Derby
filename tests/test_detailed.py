import random
from src.game import Game
from src.player import PlayerState
from src.abilities.mo import MoAbility
from src.abilities.an import AnAbility
from src.abilities.ke import KeAbility
from src.abilities.ai import AiAbility
from src.track import get_device, DeviceType, FINISH_POS, START_POS
from src.ranking import compute_ranking, get_rank


def test_device_positions():
    assert get_device(2) == DeviceType.FORWARD
    assert get_device(10) == DeviceType.FORWARD
    assert get_device(15) == DeviceType.FORWARD
    assert get_device(22) == DeviceType.FORWARD
    assert get_device(9) == DeviceType.BACKWARD
    assert get_device(27) == DeviceType.BACKWARD
    assert get_device(5) == DeviceType.DISRUPTION
    assert get_device(19) == DeviceType.DISRUPTION
    assert get_device(0) is None
    assert get_device(31) is None


def test_player_dice_range():
    normal = PlayerState(name="咲")
    assert normal.dice_range() == (1, 3)
    x = PlayerState(name="X", is_interferer=True)
    assert x.dice_range() == (1, 6)


def test_mo_ability_cycle_detailed():
    mo = MoAbility()
    for i in range(9):
        result = mo.on_roll_dice("莫", 2, {"round": 1})
        assert result is not None
        expected = [3, 2, 1][i % 3]
        assert result == expected, f"Cycle index {i}: expected {expected}, got {result}"


def test_ranking_order():
    g = Game()
    g.players["咲"].position = 20
    g.players["莫"].position = 15
    g.players["琳"].position = 20
    g.players["爱"].position = 10
    g.players["岸"].position = 5
    g.players["珂"].position = 20
    g.stacks = {20: ["咲", "琳", "珂"], 15: ["莫"], 10: ["爱"], 5: ["岸"]}
    ranking = compute_ranking(g.players, g.stacks)
    assert ranking[0] == "咲"
    assert ranking[-1] == "岸"
    assert get_rank("咲", ranking) == 1
    assert get_rank("岸", ranking) == 6


def test_x_always_bottom_after_disruption():
    random.seed(999)
    for _ in range(200):
        g = Game()
        g.run()
        for pos, stack in g.stacks.items():
            if "X" in stack and len(stack) > 1:
                assert stack[-1] == "X", f"X not bottom after disruption at {pos}: {stack}"


def test_an_ability_dice_range():
    an = AnAbility()
    for _ in range(1000):
        result = an.on_roll_dice("岸", 2, {"round": 1})
        assert result in (2, 3), f"岸's dice was {result}, expected 2 or 3"


def test_ke_ability_dice_range():
    ke = KeAbility()
    bonus_sum = 0
    count = 0
    for base in [1, 2, 3]:
        for _ in range(1000):
            bonus = ke.on_dice_bonus("珂", base, base, {"round": 1})
            assert bonus in (0, base), f"珂 bonus was {bonus}, expected 0 or {base}"
            bonus_sum += bonus
            count += 1
    assert bonus_sum > 0, "珂 should sometimes get double bonus"


def test_first_round_order_matches_stack():
    random.seed(321)
    for _ in range(50):
        g = Game()
        initial_stack = g.stacks.get(START_POS, [])
        assert g.first_round_order == initial_stack


def test_game_ends_in_reasonable_rounds():
    random.seed(111)
    max_round = 0
    for _ in range(200):
        g = Game()
        g.run()
        max_round = max(max_round, g.round_num)
    assert max_round < 100, f"Game took too many rounds: {max_round}"


if __name__ == "__main__":
    tests = [
        test_device_positions,
        test_player_dice_range,
        test_mo_ability_cycle_detailed,
        test_ranking_order,
        test_x_always_bottom_after_disruption,
        test_an_ability_dice_range,
        test_ke_ability_dice_range,
        test_first_round_order_matches_stack,
        test_game_ends_in_reasonable_rounds,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {t.__name__} - {e}")
        except Exception as e:
            print(f"ERROR: {t.__name__} - {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
