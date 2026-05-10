import sys
import time
import multiprocessing as mp
from src.game import NORMAL_NAMES
from src.simulator import Simulator


def main():
    num_games = 1_000_000
    workers = min(mp.cpu_count(), 64)

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ("-n", "--num-games") and i + 1 < len(args):
            num_games = int(args[i + 1])
            i += 2
        elif args[i] in ("-w", "--workers") and i + 1 < len(args):
            workers = int(args[i + 1])
            i += 2
        else:
            num_games = int(args[i])
            i += 1

    print(f"\n=== WuWa Cubie Derby (小团快跑) — Monte Carlo Simulation ===")
    print(f"Games: {num_games:,}  |  Workers: {workers}")

    t0 = time.perf_counter()
    sim = Simulator(num_games=num_games, workers=workers)
    rates = sim.run()
    elapsed = time.perf_counter() - t0

    print(f"\n{'Player':<6} {'Wins':>10} {'Win Rate':>10}")
    print("-" * 28)
    for name in NORMAL_NAMES:
        wins = sim.win_counts.get(name, 0)
        rate = rates.get(name, 0.0)
        print(f"{name:<6} {wins:>10,} {rate:>10.4%}")
    print(f"\nTime: {elapsed:.2f}s  |  {sim.total_games / elapsed:,.0f} games/s")


if __name__ == "__main__":
    main()
