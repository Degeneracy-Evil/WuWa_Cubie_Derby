from __future__ import annotations
from src.player import PlayerState


def compute_ranking(players: dict[str, PlayerState], stacks: dict[int, list[str]]) -> list[str]:
    ranked: list[str] = []
    entries: list[tuple[int, int, str]] = []
    for name, p in players.items():
        if p.is_interferer:
            continue
        stack = stacks.get(p.position, [])
        try:
            height = stack.index(name)
        except ValueError:
            height = len(stack)
        entries.append((p.position, height, name))
    entries.sort(key=lambda e: (-e[0], e[1]))
    ranked = [e[2] for e in entries]
    return ranked


def get_rank(name: str, ranking: list[str]) -> int:
    if name in ranking:
        return ranking.index(name) + 1
    return len(ranking) + 1
