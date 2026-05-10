import random
from src.game import Game
from src.player import PlayerState
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
    normal = PlayerState(name="陆")
    assert normal.dice_range() == (1, 3)
    x = PlayerState(name="X", is_interferer=True)
    assert x.dice_range() == (1, 6)


def test_prev_base_dice_tracking():
    p = PlayerState(name="娅")
    assert p.prev_base_dice == 0
    assert p.last_base_dice == 0
    random.seed(42)
    r1 = p.roll_base_dice()
    assert p.last_base_dice == r1
    assert p.prev_base_dice == 0
    r2 = p.roll_base_dice()
    assert p.last_base_dice == r2
    assert p.prev_base_dice == r1


def test_ranking_order():
    g = Game()
    g.players["陆"].position = 20
    g.players["西"].position = 15
    g.players["娅"].position = 20
    g.players["绯"].position = 10
    g.players["卡"].position = 5
    g.players["菲"].position = 20
    g.stacks = {20: ["陆", "娅", "菲"], 15: ["西"], 10: ["绯"], 5: ["卡"]}
    ranking = compute_ranking(g.players, g.stacks)
    assert ranking[0] == "陆"
    assert ranking[-1] == "卡"
    assert get_rank("陆", ranking) == 1
    assert get_rank("卡", ranking) == 6


def test_x_always_bottom_after_disruption():
    random.seed(999)
    for _ in range(200):
        g = Game()
        g.run()
        for pos, stack in g.stacks.items():
            if "X" in stack and len(stack) > 1:
                assert stack[-1] == "X", f"X not bottom after disruption at {pos}: {stack}"


def test_fei_bonus_after_meeting():
    random.seed(777)
    fei_bonus_count = 0
    total_after_meet = 0
    for _ in range(1000):
        g = Game()
        g.run()
        fei = g.players["绯"]
        if fei.met_x and g.round_num > fei.met_x_round:
            total_after_meet += 1
    assert total_after_meet > 0, "绯 never has rounds after meeting X"


def test_ka_ability_triggers_once():
    random.seed(555)
    for _ in range(200):
        g = Game()
        g.run()
        ka = g.players["卡"]
        if ka.ka_triggered:
            assert ka.ka_activated


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
        test_prev_base_dice_tracking,
        test_ranking_order,
        test_x_always_bottom_after_disruption,
        test_fei_bonus_after_meeting,
        test_ka_ability_triggers_once,
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
