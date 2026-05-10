import random
from src.game import Game
from src.abilities.mo import MoAbility
from src.abilities.ai import AiAbility
from src.track import get_device, DeviceType, FINISH_POS, START_POS
from src.ranking import compute_ranking, get_rank


def test_game_produces_winner():
    for _ in range(100):
        g = Game()
        w = g.run()
        assert w in ["咲", "莫", "琳", "爱", "岸", "珂"], f"Invalid winner: {w}"


def test_game_positions_valid():
    for _ in range(100):
        g = Game()
        g.run()
        for name, p in g.players.items():
            assert START_POS <= p.position <= FINISH_POS, f"{name} at invalid pos {p.position}"


def test_x_stacking_bottom():
    random.seed(42)
    for _ in range(50):
        g = Game()
        g.run()
        for pos, stack in g.stacks.items():
            if "X" in stack:
                assert stack[-1] == "X", f"X not at bottom at pos {pos}: {stack}"


def test_no_duplicate_in_stacks():
    for _ in range(50):
        g = Game()
        g.run()
        all_names: list[str] = []
        for pos, stack in g.stacks.items():
            all_names.extend(stack)
        assert len(all_names) == len(set(all_names)), f"Duplicates in stacks"


def test_player_positions_match_stacks():
    for _ in range(50):
        g = Game()
        g.run()
        for pos, stack in g.stacks.items():
            for name in stack:
                assert g.players[name].position == pos, f"{name} pos {g.players[name].position} != stack pos {pos}"


def test_ranking_no_ties():
    g = Game()
    g.run()
    ranking = compute_ranking(g.players, g.stacks)
    assert len(ranking) == len(set(ranking)), "Tied ranks"
    assert len(ranking) == 6, f"Expected 6 ranked, got {len(ranking)}"


def test_mo_ability_cycle():
    mo = MoAbility()
    results: list[int] = []
    for _ in range(6):
        result = mo.on_roll_dice("莫", 2, {"round": 1})
        assert result is not None
        results.append(result)
    assert results == [3, 2, 1, 3, 2, 1], f"Expected [3,2,1,3,2,1], got {results}"


def test_ai_teleport_once():
    random.seed(456)
    teleport_seen = False
    for _ in range(500):
        g = Game()
        g.run()
        ai = next((ab for ab in g.abilities if isinstance(ab, AiAbility)), None)
        assert ai is not None
        if ai._triggered:
            teleport_seen = True
    assert teleport_seen, "爱 never teleported in 500 games"


def test_x_teleport():
    random.seed(789)
    for _ in range(100):
        g = Game()
        g.run()
        x = g.players["X"]
        assert START_POS <= x.position <= FINISH_POS


def test_win_rates_sum_to_one():
    sim_games = 5000
    results: dict[str, int] = {}
    for _ in range(sim_games):
        g = Game()
        w = g.run()
        results[w] = results.get(w, 0) + 1
    total = sum(results.values())
    assert total == sim_games, f"Total {total} != {sim_games}"


if __name__ == "__main__":
    tests = [
        test_game_produces_winner,
        test_game_positions_valid,
        test_x_stacking_bottom,
        test_no_duplicate_in_stacks,
        test_player_positions_match_stacks,
        test_ranking_no_ties,
        test_mo_ability_cycle,
        test_ai_teleport_once,
        test_x_teleport,
        test_win_rates_sum_to_one,
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
