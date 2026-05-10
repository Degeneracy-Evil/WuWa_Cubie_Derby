# 小团快跑 — 开发TODO

## 阶段一：核心框架

- [x] 设计项目结构（模块划分、类图）
- [x] 实现赛道模型（Track）：32格、装置定义与触发 — `src/track.py`
- [x] 实现堆叠系统（StackSystem）：堆叠合并、拆分、携带逻辑 — `src/game.py`内嵌
- [x] 实现排名系统（RankingSystem）：实时排名计算与维护 — `src/ranking.py`

## 阶段二：选手与能力系统

- [x] 设计选手基类（PlayerBase）：位置、状态、能力接口 — `src/player.py`
- [x] 实现能力基类（AbilityBase）：可插拔能力接口设计 — `src/abilities/base.py`
- [x] 实现陆的能力（LuAbility）：推进装置+3、阻遏装置-1 — `src/abilities/lu.py`
- [x] 实现西的能力（XiAbility）：标记高排名选手、步数-1 — `src/abilities/xi.py`
- [x] 实现娅的能力（YaAbility）：基础骰相同则+2 — `src/abilities/ya.py`
- [x] 实现绯的能力（FeiAbility）：与X相遇后永久+1（下轮生效） — `src/abilities/fei.py`
- [x] 实现卡的能力（KaAbility）：末位检测、60%概率+2 — `src/abilities/ka.py`
- [x] 实现菲的能力（Fei2Ability）：50%概率+1 — `src/abilities/fei2.py`
- [x] 实现干扰者X（Interferer）：反向移动、始终底层、传送机制 — `src/game.py`内嵌

## 阶段三：游戏流程

- [x] 实现回合流程控制器（RoundController） — `src/game.py`
- [x] 实现移动执行器（MoveExecutor） — `src/game.py`
- [x] 实现游戏主循环（Game） — `src/game.py`

## 阶段四：Monte Carlo模拟

- [x] 实现模拟器（MonteCarloSimulator） — `src/simulator.py`
- [x] 实现结果输出 — `src/main.py`

## 阶段五：验证与调优

- [x] 编写单元测试：堆叠逻辑、装置触发、各选手能力 — `tests/test_simulation.py`
- [x] 编写集成测试：完整游戏流程 — `tests/test_detailed.py`
- [x] 边界情况测试：X传送、多人同时到终点、装置连续触发等
- [x] 性能调优：100K局~53秒
- [x] 代码隔离验证：选手能力在abilities/目录独立模块

## 阶段六：性能优化

- [x] 消除_game_ctx热路径dict创建
- [x] __slots__优化Game类
- [x] 缓存_fei/_x引用
- [x] multiprocessing并行模拟
- [x] main.py支持-n/-w参数
- [x] 基准测试验证结果一致性

## 阶段七：代码审计与正确性验证

- [x] 全量审计：6个能力模块 + 游戏引擎 + 堆叠 + 排名 + X行为 + 胜负判定
- [x] 修复西标记逻辑bug：从"始终标记前2名"改为"标记紧邻西上方的最多2名"

## 后续可选优化

- [ ] C扩展/Cython加速核心游戏循环
- [ ] 详细统计输出：每名选手的平均回合数、能力触发次数等
- [ ] 可视化：单局游戏回放、堆叠状态动画
- [ ] 新选手接入：按规则文档要求，能力代码已隔离，可方便扩展
