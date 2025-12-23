# Agent 执行系统 Phase 2 详细实现计划

**项目**: Agent 执行系统完整重构（路径 2）
**创建时间**: 2025-12-23
**状态**: 🚀 进行中 - Phase 2.1 实现中
**总工时**: 40-50 小时（5 个 Phase）

---

## 🎯 Phase 2.1: 决策引擎实现 (8-10h)

### 核心目标

实现 Agent 决策引擎，使 Agent 推荐能够：
- 自动选择：推荐命令 vs 用户命令（基于匹配度）
- 决策路径：
  - 匹配度 ≥ 85%：自动执行推荐（用户可覆盖）
  - 匹配度 65-85%：显示 3 个选项让用户选择
  - 匹配度 < 65%：执行用户命令，仅提示信息

### 实现任务

#### Task 2.1.1: 设计决策算法 (1-2h)
**目标**: 定义匹配度评分和决策阈值

**任务清单**:
- [ ] 定义匹配度评分算法（0.0-1.0）
- [ ] 确认阈值（85%, 65%）
- [ ] 设计 DecisionResult 数据结构
- [ ] 编写设计文档

**设计要点**:
```python
# 匹配度评分组成
match_score = (
    keyword_match * 0.4 +      # 关键词匹配 (40%)
    context_match * 0.3 +       # 上下文匹配 (30%)
    frequency_bonus * 0.3       # 频率奖励 (30%)
)

# 决策规则
if match_score >= 0.85:
    → decision_mode = "auto"
elif 0.65 <= match_score < 0.85:
    → decision_mode = "prompt"
else:
    → decision_mode = "info"
```

**输出**: `docs/design/2025-12-23-decision-algorithm.md`

---

#### Task 2.1.2: 实现 AgentDecisionEngine 类 (2-3h)
**目标**: 核心决策引擎实现

**文件**: `commands/lib/agent_decision_engine.py` (新增)

**类结构**:
```python
class AgentDecisionEngine:
    """Agent 决策引擎"""

    def decide(self, agent_context: Dict, user_command: str,
               decision_mode: str = "auto") -> DecisionResult:
        """
        主决策方法

        Args:
            agent_context: Agent激活上下文 (agent_id, recommendation, score, etc)
            user_command: 用户执行的命令
            decision_mode: 决策模式 ("auto", "prompt", "force_agent", "force_user")

        Returns:
            DecisionResult: 决策结果
        """

    def calculate_match_score(self, agent_context: Dict,
                              user_command: str) -> float:
        """
        计算 Agent 匹配度 (0.0-1.0)

        Returns:
            匹配度分数
        """

    def get_decision_mode(self, match_score: float) -> str:
        """根据匹配度获取决策模式"""

    def format_options(self, agent_cmd: str, user_cmd: str) -> str:
        """格式化三个选项供用户选择"""

    def get_option_descriptions(self) -> List[str]:
        """获取三个选项的描述"""
```

**三个选项**:
1. **Option A** (推荐): 使用 Agent 推荐的命令
2. **Option B** (用户命令): 继续执行用户的原始命令
3. **Option C** (并行): 先执行 Agent 推荐，再执行用户命令

**实现要点**:
- 完整的错误处理
- 详细的日志输出
- 支持决策模式切换
- DecisionResult 数据结构定义

---

#### Task 2.1.3: 集成到 agent_coordinator.py (1-2h)
**目标**: 将决策引擎集成到现有的 Agent 激活流程

**文件**: `commands/lib/agent_coordinator.py` (修改)

**修改点**:
```python
# 在 AgentCoordinator 类中添加

def activate_agent(self, agent_name: str, context: Dict) -> None:
    """激活 Agent"""
    agent = self.find_agent(agent_name)

    # 原有逻辑：检测和激活
    is_activated = self._check_activation(agent, context)

    if is_activated:
        # 新增：决策逻辑
        decision_result = self.decision_engine.decide(
            agent_context=agent.context,
            user_command=context.get("user_command", ""),
            decision_mode="auto"  # 可配置
        )

        # 根据决策结果进行后续处理
        self._handle_decision(decision_result)
```

**集成要点**:
- 导入 AgentDecisionEngine
- 在 __init__ 中初始化决策引擎
- 保留现有的日志和上下文
- 确保向后兼容性

---

#### Task 2.1.4: 编写单元测试 (2-3h)
**目标**: 完整的单元测试覆盖

**文件**: `tests/test_agent_decision_engine.py` (新增)

**测试用例** (12-15 个):

**匹配度计算 (5 个)**:
- [ ] test_high_match_score (> 0.85)
- [ ] test_medium_match_score (0.65-0.85)
- [ ] test_low_match_score (< 0.65)
- [ ] test_exact_keyword_match
- [ ] test_partial_context_match

**决策逻辑 (5 个)**:
- [ ] test_auto_mode_high_score
- [ ] test_prompt_mode_medium_score
- [ ] test_info_mode_low_score
- [ ] test_force_agent_mode
- [ ] test_force_user_mode

**选项格式 (3 个)**:
- [ ] test_format_three_options
- [ ] test_option_descriptions
- [ ] test_option_selection_validation

**错误处理 (2 个)**:
- [ ] test_invalid_context
- [ ] test_invalid_user_command

**性能 (1 个)**:
- [ ] test_decision_engine_performance (< 5ms)

**测试框架**: pytest
**覆盖率目标**: ≥ 90%

---

#### Task 2.1.5: 性能基准测试 (1h)
**目标**: 验证性能指标

**文件**: `tests/performance/test_decision_engine_perf.py` (新增)

**性能指标**:
```
决策引擎执行时间:
- 平均: < 5ms ✅
- P95: < 10ms ✅
- P99: < 20ms ✅

匹配度计算:
- 平均: < 2ms ✅
- 单个关键词: < 0.1ms ✅
```

**测试方法**:
- 基准测试 (100,000 次调用)
- 输出性能报告
- 确保符合性能目标

---

## 📊 代码结构概览

```
commands/
├── lib/
│   ├── agent_coordinator.py (修改)
│   ├── agent_decision_engine.py (新增 ~300 行)
│   └── ...
│
└── tests/
    ├── test_agent_decision_engine.py (新增 ~400 行)
    ├── performance/
    │   └── test_decision_engine_perf.py (新增 ~100 行)
    └── ...

docs/
└── design/
    └── 2025-12-23-decision-algorithm.md (新增)
```

---

## ✅ Phase 2.1 完成标准

### 功能完成
- [ ] AgentDecisionEngine 类完全实现
- [ ] 匹配度评分算法有效
- [ ] 三个决策模式正常工作
- [ ] 与 agent_coordinator 集成成功

### 测试完成
- [ ] 12-15 个单元测试全部通过
- [ ] 测试覆盖率 ≥ 90%
- [ ] 性能测试通过（< 5ms）
- [ ] 无代码异常或崩溃

### 文档完成
- [ ] 设计文档完整
- [ ] 代码注释清晰
- [ ] API 文档清楚
- [ ] 集成指南可用

### 代码质量
- [ ] 通过 black 格式化
- [ ] 通过 pre-commit 检查
- [ ] 无 type hint 警告（可选）
- [ ] 日志输出完整

---

## 🚀 执行步骤

### Step 1: 架构设计 (1h)
```bash
# 理解现有的 agent_coordinator.py
Read commands/lib/agent_coordinator.py

# 创建设计文档
Write docs/design/2025-12-23-decision-algorithm.md
```

### Step 2: 核心实现 (3h)
```bash
# 实现 AgentDecisionEngine
Write commands/lib/agent_decision_engine.py

# 集成到 agent_coordinator
Edit commands/lib/agent_coordinator.py
```

### Step 3: 测试开发 (3h)
```bash
# 编写单元测试
Write tests/test_agent_decision_engine.py

# 编写性能测试
Write tests/performance/test_decision_engine_perf.py

# 运行测试
pytest tests/test_agent_decision_engine.py -v --cov
```

### Step 4: 代码审查 (1h)
```bash
/wf_08_review
```

### Step 5: 提交
```bash
/wf_11_commit
```

---

## 🔗 后续 Phase 依赖

**Phase 2.2 - 执行器** (需要 Phase 2.1 完成)
- 使用 AgentDecisionEngine 的决策结果
- 实现真正的命令执行

**Phase 2.3 - 反馈系统** (需要 Phase 2.2 完成)
- 收集执行结果
- 反馈给决策引擎改进匹配度评分

**Phase 2.4 - 多 Agent 协调** (需要 Phase 2.1 完成)
- 处理多个 Agent 的冲突
- 使用决策引擎的逻辑进行协调

---

## 📝 估算细分

| 任务 | 时间 | 备注 |
|------|------|------|
| 2.1.1 算法设计 | 1-2h | 关键决策 |
| 2.1.2 核心实现 | 2-3h | ~300 行代码 |
| 2.1.3 集成 | 1-2h | 保证兼容性 |
| 2.1.4 单元测试 | 2-3h | ~400 行测试 |
| 2.1.5 性能测试 | 1h | 基准验证 |
| **总计** | **8-10h** | **完整工作** |

---

**下一步**: 立即开始 Task 2.1.1 - 算法设计
**推荐命令**: `/wf_05_code`

**最后更新**: 2025-12-23
