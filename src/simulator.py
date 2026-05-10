from __future__ import annotations
import multiprocessing as mp
import random
from src.game import Game


def _worker(args: tuple[int, int]) -> dict[str, int]:
    num_games, seed = args
    random.seed(seed)
    counts: dict[str, int] = {}
    for _ in range(num_games):
        g = Game()
        w = g.run()
        counts[w] = counts.get(w, 0) + 1
    return counts


class Simulator:
    def __init__(self, num_games: int = 1_000_000, workers: int | None = None):
        self.num_games = num_games
        self.workers = workers or min(mp.cpu_count(), 64)
        self.win_counts: dict[str, int] = {}
        self.total_games = 0

    def run(self) -> dict[str, float]:
        if self.workers <= 1:
            self._run_sequential()
        else:
            self._run_parallel()
        return self.win_rates()

    def _run_sequential(self) -> None:
        for _ in range(self.num_games):
            g = Game()
            w = g.run()
            self.win_counts[w] = self.win_counts.get(w, 0) + 1
            self.total_games += 1

    def _run_parallel(self) -> None:
        n = self.num_games
        w = self.workers
        base = n // w
        remainder = n % w
        chunks: list[tuple[int, int]] = []
        for i in range(w):
            size = base + (1 if i < remainder else 0)
            if size > 0:
                chunks.append((size, random.randint(0, 2**63 - 1)))

        with mp.Pool(w) as pool:
            results = pool.map(_worker, chunks)

        for partial in results:
            for name, count in partial.items():
                self.win_counts[name] = self.win_counts.get(name, 0) + count
            self.total_games += sum(partial.values())

    def win_rates(self) -> dict[str, float]:
        if self.total_games == 0:
            return {}
        return {name: count / self.total_games for name, count in self.win_counts.items()}
