# ADR 2025-12-23-B: Agent 执行系统重构 - 路径 2 完整设计

**日期**: 2025-12-23
**状态**: 📋 设计阶段
**优先级**: 🔴 最高
**工作量**: 35-45 小时 (2-3 周)

---

## 🔴 问题陈述

**核心缺陷**: 路径 1 修复只实现了 "Agent 诊断和显示"，完全缺少 "Agent 执行和协调"

**现状**:
```
检测 → 激活 → 显示信息 → (断裂！)
用户仍然执行原始命令，Agent 建议完全被忽视
```

**影响**: Agent 激活系统对用户实际行为零影响

---

## 🎯 重构目标

实现完整的 Agent 执行流程：
```
检测 → 激活 → 显示信息 → 做决策 → 执行 → 验证 → 反馈
```

**预期成果**:
- ✅ Agent 推荐真正影响用户行为
- ✅ 冲突自动解决（AI 或用户选择）
- ✅ 完整的反馈循环
- ✅ 多 Agent 协作机制

---

## 📐 系统架构设计

### 1. 决策引擎 (Agent Decision Engine)

**职责**: 在 Agent 推荐和用户命令冲突时做出决策

**设计**:
```python
class AgentDecisionEngine:
    """Agent 决策引擎"""

    def decide(self,
               agent_context: Dict,
               user_command: str,
               decision_mode: str = "auto") -> str:
        """
        决策选择哪个命令执行

        Args:
            agent_context: Agent 激活上下文
            user_command: 用户执行的命令
            decision_mode: 决策模式
              - "auto": AI 自动决策（匹配度 > 85% 时选 Agent，否则选用户）
              - "user": 等待用户选择（三个选项）
              - "force_agent": 强制选择 Agent 推荐

        Returns:
            最终执行的命令
        """
```

**决策逻辑**:
```
IF Agent 匹配度 ≥ 85%:
  → 自动执行 Agent 推荐（用户可覆盖）
ELIF Agent 匹配度 ≥ 65%:
  → 显示三个选项，AI 推荐选项 1，用户可选择
ELSE:
  → 执行用户命令，仅提示 Agent 信息
```

**冲突解决的三个选项**:
1. **推荐选项** (AI 倾向): 改用 Agent 推荐的命令
2. **用户坚持**: 继续执行用户命令
3. **并行执行**: 先执行 Agent 推荐，再执行用户命令

---

### 2. 执行器 (Agent Command Executor)

**职责**: 实际执行 Agent 推荐的命令

**设计**:
```python
class AgentCommandExecutor:
    """Agent 命令执行器"""

    def execute_agent_command(self,
                             agent: Agent,
                             context: Dict) -> ExecutionResult:
        """
        执行 Agent 推荐的命令

        Returns:
            ExecutionResult: 包含执行状态、输出、性能指标
        """
```

**执行流程**:
```
1. 验证 Agent 推荐的命令有效
2. 准备执行环境（加载必要的 MCP 工具）
3. 执行命令（记录执行时间和输出）
4. 捕获执行结果（成功/失败/异常）
5. 记录执行历史
```

---

### 3. 反馈验证系统 (Agent Feedback System)

**职责**: 验证 Agent 推荐是否有效，收集反馈改进

**设计**:
```python
class AgentFeedbackSystem:
    """Agent 反馈系统"""

    def record_execution(self,
                        agent: Agent,
                        command: str,
                        result: ExecutionResult) -> None:
        """记录 Agent 执行历史"""

    def evaluate_effectiveness(self,
                              agent: Agent,
                              result: ExecutionResult) -> float:
        """评估 Agent 推荐的有效性 (0.0 - 1.0)"""

    def update_agent_score(self,
                          agent: Agent,
                          effectiveness: float) -> None:
        """根据有效性更新 Agent 的推荐准确率"""
```

**效果评估指标**:
- ✅ Agent 推荐采纳率
- ✅ 推荐成功率（执行后达成目标）
- ✅ 平均执行时间 vs 用户预期时间
- ✅ 用户满意度（隐式：是否再次采纳）

---

### 4. 协作协调器 (Multi-Agent Orchestrator)

**职责**: 处理多个 Agent 的推荐冲突和协作

**设计**:
```python
class MultiAgentOrchestrator:
    """多 Agent 协调器"""

    def resolve_conflicts(self,
                         agent_contexts: List[Dict]) -> List[str]:
        """
        解决多个 Agent 的推荐冲突

        Returns:
            执行顺序的命令列表
        """

    def coordinate_execution(self,
                            commands: List[str]) -> None:
        """协调命令执行（顺序/并行）"""
```

**冲突解决策略**:
- 按 Agent 匹配度排序（高优先级）
- 检测命令依赖关系
- 确定执行顺序或并行性
- 处理执行失败时的回滚

---

## 📊 实现路线图

### Phase 2.1: 决策引擎实现 (8-10h)

**目标**: 实现自动决策逻辑

**任务**:
- [ ] 设计决策算法和匹配度阈值
- [ ] 实现 `AgentDecisionEngine` 类
- [ ] 集成到 `agent_coordinator.py`
- [ ] 编写单元测试 (10-15 个)
- [ ] 性能基准测试

**关键文件**:
- `commands/lib/agent_decision_engine.py` (新增)
- `commands/lib/agent_coordinator.py` (修改)
- `tests/test_agent_decision_engine.py` (新增)

**预期代码量**: ~300 行

---

### Phase 2.2: 执行器实现 (10-12h)

**目标**: 真正执行 Agent 推荐的命令

**任务**:
- [ ] 设计执行结果数据结构
- [ ] 实现 `AgentCommandExecutor` 类
- [ ] 集成 MCP 工具自动加载
- [ ] 实现执行超时和错误处理
- [ ] 编写集成测试 (8-10 个)

**关键文件**:
- `commands/lib/agent_command_executor.py` (新增)
- `tests/test_agent_command_executor.py` (新增)

**预期代码量**: ~400 行

---

### Phase 2.3: 反馈系统实现 (8-10h)

**目标**: 验证和改进 Agent 决策

**任务**:
- [ ] 设计执行历史存储格式
- [ ] 实现 `AgentFeedbackSystem` 类
- [ ] 实现有效性评估算法
- [ ] 集成反馈循环到决策引擎
- [ ] 编写测试 (6-8 个)

**关键文件**:
- `commands/lib/agent_feedback_system.py` (新增)
- `commands/lib/agent_execution_history.py` (新增)
- `tests/test_agent_feedback_system.py` (新增)

**预期代码量**: ~350 行

---

### Phase 2.4: 多 Agent 协调 (8-10h)

**目标**: 处理多 Agent 场景

**任务**:
- [ ] 设计冲突解决策略
- [ ] 实现 `MultiAgentOrchestrator` 类
- [ ] 实现命令依赖分析
- [ ] 实现顺序/并行执行策略
- [ ] 编写集成测试 (10-12 个)

**关键文件**:
- `commands/lib/multi_agent_orchestrator.py` (新增)
- `tests/test_multi_agent_orchestrator.py` (新增)

**预期代码量**: ~400 行

---

### Phase 2.5: 端到端集成和测试 (6-8h)

**目标**: 完整的 Agent 执行流程

**任务**:
- [ ] 集成所有组件
- [ ] 编写端到端集成测试 (15-20 个)
- [ ] 性能测试和优化
- [ ] 文档编写和更新

**预期代码量**: ~500 行 (测试)

---

## 🧪 测试策略

### 单元测试 (45-50 个)
- 决策引擎: 15-20 个
- 执行器: 15-20 个
- 反馈系统: 10-12 个
- 协调器: 10-12 个

### 集成测试 (20-25 个)
- 决策 + 执行
- 执行 + 反馈
- 多 Agent 协调
- 端到端工作流

**关键场景**:
```
1. Agent 推荐被采纳 → 执行 → 验证成功
2. Agent 推荐被拒绝 → 执行用户命令
3. 多 Agent 冲突 → 自动协调 → 执行
4. 执行失败 → 记录反馈 → 降低 Agent 分数
5. Agent 学习 → 推荐准确性提高 → 自动采纳率增加
```

---

## 📈 预期收益

### 对用户的影响
- ✅ Agent 推荐真正影响用户行为
- ✅ 冲突自动解决，用户不需要手动选择
- ✅ 工作流更专业化，效率提升

### 对系统的改进
- ✅ Agent 系统完整度: 50% → 95%
- ✅ 功能复杂度: 中等 → 高（但价值明显）
- ✅ 代码质量: 保持高标准
- ✅ 测试覆盖: 49 → 70+ 个测试

### 性能影响
- ⚠️ 决策引擎: +2-5ms（可接受）
- ⚠️ 执行链路: +10-20ms（可接受）
- ✅ 整体影响: < 1% 延迟

---

## 🔧 技术选型

### 决策算法
- 基于匹配度阈值的简单决策树
- 可扩展为更复杂的 ML 模型

### 执行机制
- 基于现有的命令框架
- 集成 MCP 工具自动加载

### 反馈存储
- JSON 格式执行历史文件
- 可选：迁移到数据库

### 协调策略
- 拓扑排序解决依赖关系
- 支持顺序和并行执行

---

## 📋 风险评估

| 风险 | 概率 | 影响 | 缓解策略 |
|------|------|------|---------|
| 决策错误导致错误执行 | 中 | 高 | 严格的单元测试，用户可覆盖 |
| 多 Agent 协调复杂度过高 | 中 | 中 | 分阶段实现，先支持简单场景 |
| 执行超时或失败 | 低 | 中 | 完善的错误处理和回滚机制 |
| 反馈系统数据过大 | 低 | 低 | 定期清理历史数据 |

---

## ✅ 完成标准

### 功能完成
- [ ] 决策引擎完全工作
- [ ] 执行器真正执行 Agent 推荐
- [ ] 反馈系统记录和分析执行
- [ ] 多 Agent 协调正常工作

### 测试完成
- [ ] 70+ 个测试全部通过
- [ ] 端到端集成测试覆盖关键场景
- [ ] 性能测试通过

### 文档完成
- [ ] ADR 记录完整
- [ ] 架构文档更新
- [ ] API 文档清晰

### 部署准备
- [ ] 代码审查通过
- [ ] 向后兼容性验证
- [ ] 部署指南完成

---

## 🎓 学习收获

**为什么路径 1 失败**：
- 低估了"执行"的复杂性
- 测试代码质量≠功能完整性
- 架构不完整的代码是无用的

**路径 2 的教训**：
- 必须从用户实际行为出发设计
- 每个层级都要有测试验证
- Agent 系统需要反馈循环才能学习

---

**下一步**: 等待用户确认开始实现或调整计划
