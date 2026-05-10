# WuWa Cubie Derby (小团快跑) — Agent Navigation

## Project Overview

Monte Carlo simulation of a board game ("小团快跑") with 6 players + 1 interferer (X).
Simulates millions of games with completely random dice to compute win rates.

**Stack**: Python 3.13, no external dependencies, multiprocessing parallelism.

---

## Directory Map

```
WuWa_Cubie_Derby/
├── src/
│   ├── main.py              # CLI entry point (-n games, -w workers)
│   ├── game.py              # Game engine — round loop, movement, stacking, devices, win
│   ├── player.py            # PlayerState dataclass — position, dice, per-ability state
│   ├── track.py             # Track model — 32 positions, device map (forward/backward/disruption)
│   ├── ranking.py           # Ranking — sort by position desc + stack height asc, X excluded
│   ├── simulator.py         # Monte Carlo runner — sequential or multiprocessing Pool
│   └── abilities/
│       ├── __init__.py      # ALL_ABILITIES registry — list of all ability classes
│       ├── base.py          # AbilityBase — hook interface (on_dice_bonus, on_device_trigger, on_round_start, on_movement_end, on_round_end)
│       ├── lu.py            # 陆 — forward device +3, backward device -1 (mover only)
│       ├── xi.py            # 西 — mark 2 players immediately above in ranking, their steps -1
│       ├── ya.py            # 娅 — if base dice equals previous base dice, +2
│       ├── fei.py           # 绯 — after meeting X, +1 from next round (permanent, non-cumulative)
│       ├── ka.py            # 卡 — if last place after own movement, activate; then 60% chance +2
│       └── fei2.py          # 菲 — 50% chance +1
├── tests/
│   ├── test_simulation.py   # Core invariants — winner validity, positions, stacking, ranking
│   └── test_detailed.py     # Ability-specific — device positions, dice range, prev_base_dice, etc.
├── 规则.md                   # Complete rules document (Chinese) — authoritative spec
├── PROCESS.md               # Development log with benchmarks and bug fixes
├── TODO.md                  # Task tracker
└── pyproject.toml           # Project config (Python 3.13, no deps)
```

---

## Key Files — What to Read First

| If you need to... | Read these files |
|---|---|
| Understand the game rules | `规则.md` (authoritative) |
| Understand game flow | `game.py` → `player.py` → `track.py` → `ranking.py` |
| Understand ability system | `abilities/base.py` → any ability module |
| Add a new player/ability | `abilities/base.py` (interface) → `abilities/__init__.py` (registry) → `game.py` (integration points) |
| Fix a bug in movement/stacking | `game.py` (`_execute_movement`, `_move_group_to`, `_extract_moving_group`) |
| Fix a bug in dice resolution | `game.py` (`_roll_and_resolve`) |
| Change track layout | `track.py` (`DEVICE_MAP`) |
| Run simulations | `main.py` → `simulator.py` → `game.py` |
| Write tests | `tests/test_simulation.py` (invariants), `tests/test_detailed.py` (ability-specific) |

---

## Architecture

### Game Flow (per round)

```
_generate_order()          # random movement order (round 3+ includes X)
_roll_and_resolve()        # roll dice → apply bonuses → apply 西 penalty
for each player in order:
    _execute_movement()    # step-by-step movement with stacking + device chain
    on_movement_end()      # e.g. 卡 last-place check
_apply_x_teleport()       # if X below last place with nothing above → teleport to 31
```

### Ability Hook Lifecycle

```
on_round_start(state, ctx)     # called once per round after dice roll, before movement
on_dice_bonus(state, ctx)      # called during dice resolution, returns int bonus
on_device_trigger(device, state, ctx)  # called when mover lands on device, returns int delta
on_movement_end(state, ctx)    # called after a player finishes moving
on_round_end(state, ctx)       # called at end of round (currently unused)
```

### Stacking Convention

- Stack is a `list[str]` where **index 0 = top**, **last index = bottom**
- X is always forced to the bottom of any stack
- Lower positions carry upper positions when moving
- `_extract_moving_group(mover)` returns `[top, ..., mover]` — everyone above mover goes along

### Ranking

- `compute_ranking()` returns `list[str]` sorted rank 1 first (index 0 = highest rank)
- Sort key: `(-position, height_in_stack)` — closer to finish = higher rank, same position = higher in stack = higher rank
- X is excluded from ranking

---

## Adding a New Player

### Current coupling issues (being refactored)

The game engine has several hardcoded references that need updating when adding a player:

1. **`game.py` line 9**: `NORMAL_NAMES` tuple — must add new name
2. **`game.py` line 34**: `self._fei = self.players["绯"]` — 绯 cached for meeting detection
3. **`game.py` line 38**: `self._xi_ability = next(...)` — 西 cached for marking penalty
4. **`game.py` lines 107-112**: 西's `-1` penalty applied as special case outside bonus loop
5. **`game.py` line 280**: `"绯" in stack and "X" in stack` — 绯-X meeting hardcoded
6. **`main.py` line 34**: Display order hardcoded
7. **`player.py`**: Ability-specific fields (`met_x`, `ka_triggered`, etc.) on all PlayerStates
8. **`abilities/__init__.py`**: `ALL_ABILITIES` list must be updated

### Steps to add a new player (current state)

1. Create `src/abilities/newplayer.py` inheriting `AbilityBase`
2. Add class to `ALL_ABILITIES` in `src/abilities/__init__.py`
3. Add name to `NORMAL_NAMES` in `src/game.py`
4. Add name to display list in `src/main.py`
5. If ability needs per-player state, add fields to `PlayerState` in `src/player.py`
6. If ability needs special game-engine hooks, add code to `src/game.py`

---

## Conventions

- Language: Python 3.13, `from __future__ import annotations` in all source files
- No external dependencies — stdlib only
- Player names are Chinese characters (陆/西/娅/绯/卡/菲/X)
- Dice: normal players 1-3, X is 1-6
- Track: positions 0-31, devices at 2,5,9,10,15,19,22,27
- Tests: `pytest`, 19 tests in `tests/`
- Run: `.venv/bin/python -m src.main -n 10000000 -w 120`
