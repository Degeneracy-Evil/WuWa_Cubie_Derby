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
│   ├── player.py            # PlayerState dataclass — name, position, is_interferer only
│   ├── track.py             # Track model — 32 positions, device map (forward/backward/disruption)
│   ├── ranking.py           # Ranking — sort by position desc + stack height asc, X excluded
│   ├── simulator.py         # Monte Carlo runner — sequential or multiprocessing Pool
│   └── abilities/
│       ├── __init__.py      # ALL_ABILITIES registry — list of all ability classes
│       ├── base.py          # AbilityBase — hook interface
│       ├── xiao.py          # 咲 — base dice is min among all → steps+2
│       ├── mo.py            # 莫 — 3→2→1 fixed cycle
│       ├── lin.py           # 琳 — 60% double / 20% skip / 20% normal
│       ├── ai.py            # 爱 — teleport to nearest ahead player after crossing pos 16
│       ├── an.py            # 岸 — dice only 2 and 3
│       └── ke.py            # 珂 — 28% double / 72% normal
├── tests/
│   ├── test_simulation.py   # Core invariants — winner validity, positions, stacking, ranking
│   └── test_detailed.py     # Ability-specific — device positions, dice range, cycle, etc.
├── 规则.md                   # Complete rules document (Chinese) — authoritative spec
├── 新选手.md                 # Current season player abilities
├── 退役选手.md               # Retired player archive (陆/西/娅/绯/卡/菲)
├── PROCESS.md               # Development log with benchmarks and bug fixes
├── TODO.md                  # Task tracker
└── pyproject.toml           # Project config (Python 3.13, no deps)
```

---

## Key Files — What to Read First

| If you need to... | Read these files |
|---|---|
| Understand the game rules | `规则.md` (authoritative) |
| Understand current players | `新选手.md` |
| Understand game flow | `game.py` → `player.py` → `track.py` → `ranking.py` |
| Understand ability system | `abilities/base.py` → any ability module |
| Add a new player/ability | `abilities/base.py` (interface) → `abilities/__init__.py` (registry) — that's it! |
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
_roll_and_resolve()        # roll dice → on_roll_dice overrides → on_round_start → bonuses → finalize
for each player in order:
    _execute_movement()    # step-by-step movement with stacking + device chain + on_step_end
    on_movement_end()      # e.g. post-movement checks
_apply_x_teleport()       # if X below last place with nothing above → teleport to 31
```

### Ability Hook Lifecycle

```
on_game_start(ctx)              # called once at game start
on_roll_dice(actor, default, ctx) -> int|None  # override base dice roll
on_round_start(ctx)             # called once per round after dice roll, before movement
on_dice_bonus(actor, base, cur, ctx) -> int    # additive bonus during dice resolution
on_dice_finalize(actor, base, cur, ctx) -> int # transform final value (clamp, etc.)
on_device_trigger(device, mover, ctx) -> int   # called when mover lands on device
on_step_end(mover, from, to, ctx) -> bool      # called after each step, True=interrupt
on_movement_end(mover, ctx)     # called after a player finishes moving
on_stack_event(kind, pos, stack, actor, ctx)   # called after every stack mutation
on_round_end(ctx)               # called at end of round (currently unused)
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

The system is fully modular. Adding a new player requires ONLY:

1. Create `src/abilities/newplayer.py` inheriting `AbilityBase`
2. Add class to `ALL_ABILITIES` in `src/abilities/__init__.py`

No changes to `game.py`, `player.py`, or `main.py` needed.

### Available Hooks

| Hook | Use When |
|------|----------|
| `on_roll_dice` | Player has custom dice (fixed cycle, different range, dice transformation) |
| `on_dice_bonus` | Player gets additive step bonus (+N) |
| `on_dice_finalize` | Player applies non-additive transform (clamp, multiply) |
| `on_device_trigger` | Player has device-related ability |
| `on_step_end` | Player needs per-step interception (teleport, position-based triggers) |
| `on_movement_end` | Player checks state after own movement |
| `on_stack_event` | Player reacts to positional events (meeting X, etc.) |
| `on_round_start` | Player needs per-round setup (marking, etc.) |

---

## Conventions

- Language: Python 3.13, `from __future__ import annotations` in all source files
- No external dependencies — stdlib only
- Player names are Chinese characters (咲/莫/琳/爱/岸/珂/X)
- Dice: normal players 1-3 (unless overridden by on_roll_dice), X is 1-6
- Track: positions 0-31, devices at 2,5,9,10,15,19,22,27
- Tests: `pytest`, 19 tests in `tests/`
- Run: `.venv/bin/python -m src.main -n 10000000 -w 120`
