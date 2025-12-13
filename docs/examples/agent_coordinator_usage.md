---
title: "Agent Coordinator 使用指南"
description: "AgentCoordinator 统一协调器的使用示例和最佳实践"
type: "教程"
status: "完成"
priority: "高"
created_date: "2025-12-12"
last_updated: "2025-12-12"
related_documents:
  - "docs/adr/2025-12-08-agent-system-architecture.md"
  - "PLANNING.md § Agent 系统架构"
related_code:
  - "commands/lib/agent_coordinator.py"
  - "commands/lib/agent_registry.py"
  - "commands/agents/*.md"
tags: ["agent", "coordinator", "tutorial", "integration"]
authors: ["Claude"]
version: "1.0"
---

# Agent Coordinator 使用指南

## 概述

AgentCoordinator 是 AI Workflow 命令系统的统一 agent 协调器，负责：
- 自动选择合适的 agent
- 提供 agent 上下文给命令执行
- 记录 agent 使用情况
- 建议下一步协作

## 快速开始

### 基础用法

```python
from commands.lib.agent_coordinator import get_agent_coordinator

# 获取协调器实例（单例模式）
coordinator = get_agent_coordinator()

# 拦截命令执行，选择 agent
agent_context = coordinator.intercept(
    task_description="实现用户登录功能",
    command_name="wf_05_code",
    auto_activate=True,
    min_confidence=0.85
)

# 显示 agent 信息
print(coordinator.format_agent_info(agent_context, verbose=True))
```

### 输出示例

```markdown
## 🤖 Agent 协助

**使用 Agent**: Implementation Engineer (`code-agent`)
**匹配度**: 92% 🟢 自动激活
**专长**: 功能实现和代码编写, 设计模式应用, 代码质量和可读性

**MCP 工具**:
  - Serena: 精确代码定位和智能插入点检测
  - Magic: UI 组件生成
  - Sequential-thinking: 复杂实现的逻辑推理

**建议协作**:
  - sequential: architect-agent (架构设计后实现)
  - parallel: test-agent (同时编写代码和测试)
```

## 在命令文件中集成

### Step 1: 导入协调器

在命令文件的 Process 章节开头添加：

```markdown
### Step 0: Agent 选择和激活

```python
from commands.lib.agent_coordinator import get_agent_coordinator

# 初始化协调器
coordinator = get_agent_coordinator()

# 拦截并选择 agent
agent_context = coordinator.intercept(
    task_description=user_task_description,  # 从命令参数获取
    command_name="wf_05_code",
    auto_activate=True,
    min_confidence=0.85
)

# 显示 agent 信息
print(coordinator.format_agent_info(agent_context, verbose=True))
```
```

### Step 2: 使用 Agent 上下文

在后续步骤中，可以访问 agent 信息：

```python
# 如果 agent 激活，根据其 expertise 调整提示
if agent_context['auto_activated']:
    agent = agent_context['agent']

    # 1. 调整 MCP 使用优先级
    mcp_priority = [mcp['name'] for mcp in agent.mcp_integrations]

    # 2. 根据 expertise 增强提示
    expertise_hints = f"作为 {agent.role}，重点关注: {', '.join(agent.expertise)}"

    # 3. 验证工具使用
    if current_tool not in agent.available_tools:
        print(f"⚠️ Agent 建议使用 {agent.available_tools[0]} 而非当前工具")
```

## 使用场景

### 场景 1: 自动选择最合适的 Agent

```python
coordinator = get_agent_coordinator()

# 不同任务会自动选择不同的 agent
tasks = [
    ("实现用户注册功能", "wf_05_code"),      # → code-agent
    ("修复登录 bug", "wf_06_debug"),          # → debug-agent
    ("编写单元测试", "wf_07_test"),           # → test-agent
    ("代码审查", "wf_08_review"),             # → review-agent
    ("架构设计", "wf_04_ask"),                # → architect-agent
]

for task, command in tasks:
    context = coordinator.intercept(task, command)
    print(f"{task} → {context['agent'].name if context['agent'] else 'None'}")
```

### 场景 2: 协作建议

```python
coordinator = get_agent_coordinator()

# 执行当前任务
context = coordinator.intercept(
    task_description="实现支付模块",
    command_name="wf_05_code"
)

# 获取下一步建议
next_agent = coordinator.suggest_next_agent()
print(f"建议下一步使用: {next_agent}")

# 查看所有协作选项
collaborators = context['collaborators']
for collab in collaborators:
    print(f"{collab['mode']}: {collab['agent']} - {collab['scenario']}")
```

**输出**:
```
建议下一步使用: test-agent
sequential: architect-agent - 架构设计后实现
parallel: test-agent - 同时编写代码和测试
sequential: review-agent - 实现完成后审查
```

### 场景 3: 使用统计

```python
coordinator = get_agent_coordinator()

# 执行一系列任务
# ...

# 查看统计
stats = coordinator.format_usage_stats(limit=10)
print(stats)
```

**输出**:
```markdown
## 📊 Agent 使用统计

**总记录数**: 25
**显示最近**: 10 条

| 时间 | Agent | 匹配度 | 激活 | 任务 |
|------|-------|--------|------|------|
| 2025-12-12T15:30:22 | code-agent | 92% | ✅ | 实现用户注册 |
| 2025-12-12T15:35:15 | test-agent | 88% | ✅ | 编写单元测试 |
| 2025-12-12T15:40:08 | review-agent | 85% | ✅ | 代码审查 |
...
```

### 场景 4: 低置信度处理

```python
coordinator = get_agent_coordinator()

# 模糊的任务描述
context = coordinator.intercept(
    task_description="帮我做点什么",
    command_name="wf_05_code",
    auto_activate=True,
    min_confidence=0.85
)

if not context['auto_activated']:
    print(f"⚠️ 匹配度 {context['match_score']:.0%} 低于阈值，未自动激活")
    print(f"建议明确任务描述，或手动选择 agent")

    # 显示备选 agents
    if context['alternatives']:
        print("\n可选 Agents:")
        for alt in context['alternatives']:
            print(f"  - {alt.role} ({alt.name})")
```

### 场景 5: 手动控制

```python
coordinator = get_agent_coordinator()

# 禁用自动激活
context = coordinator.intercept(
    task_description="实现新功能",
    command_name="wf_05_code",
    auto_activate=False  # 仅匹配，不激活
)

# 用户手动决定是否使用
if context['match_score'] > 0.90:
    print(f"推荐使用 {context['agent'].role}")
    # 用户确认后再激活
else:
    print("不推荐使用 agent，建议优化任务描述")
```

## 最佳实践

### ✅ DO

1. **在命令开头调用 intercept()**
   - 尽早获取 agent 上下文
   - 在读取项目文档之后，实际实现之前

2. **使用详细的任务描述**
   - 包含关键动作词（实现、修复、测试、审查等）
   - 说明具体功能或目标

3. **根据 agent 建议调整流程**
   - 参考 mcp_hints 优先使用推荐的 MCP
   - 遵循 collaborators 建议的协作模式

4. **记录和分析统计数据**
   - 定期查看 usage_stats
   - 识别常用 agents 和优化机会

### ❌ DON'T

1. **不要跳过 agent 选择**
   - 即使是简单任务，也应尝试匹配
   - 可以使用低阈值或禁用自动激活

2. **不要忽略命令对齐警告**
   - 如果 `command_alignment.aligned == False`
   - 考虑使用推荐的命令

3. **不要过度依赖自动激活**
   - 复杂任务可能需要手动选择
   - 低置信度时人工判断更可靠

4. **不要修改协调器状态**
   - 除了测试，不要调用 reset()
   - 保持单例的完整性

## API 参考

### AgentCoordinator

#### `intercept(task_description, command_name, auto_activate=True, min_confidence=0.85)`

拦截命令执行，选择合适的 agent

**参数**:
- `task_description` (str): 用户任务描述
- `command_name` (str): 当前执行的命令名（如 `wf_05_code`）
- `auto_activate` (bool): 是否自动激活（默认 True）
- `min_confidence` (float): 最低置信度阈值（默认 0.85）

**返回**: Dict[str, Any]
```python
{
    'agent': Agent,              # 选中的 agent 对象
    'match_score': float,        # 匹配分数 (0-1)
    'auto_activated': bool,      # 是否自动激活
    'alternatives': List[Agent], # 备选 agents
    'mcp_hints': List[str],      # MCP 使用建议
    'collaborators': List[Dict], # 协作建议
    'command_alignment': Dict    # 命令对齐检查
}
```

#### `format_agent_info(context, verbose=True)`

格式化 agent 信息输出

**参数**:
- `context` (Dict): intercept() 返回的上下文
- `verbose` (bool): 是否显示详细信息（默认 True）

**返回**: str - 格式化的 Markdown 字符串

#### `suggest_next_agent()`

根据当前 agent 建议下一步协作

**返回**: Optional[str] - 下一步建议的 agent 名称

#### `get_usage_stats(limit=10)`

获取 agent 使用统计

**参数**:
- `limit` (int): 返回最近的 N 条记录

**返回**: List[Dict] - 使用统计列表

#### `format_usage_stats(limit=10)`

格式化使用统计输出

**参数**:
- `limit` (int): 显示最近的 N 条记录

**返回**: str - 格式化的统计信息

### get_agent_coordinator()

获取全局 AgentCoordinator 实例（单例模式）

**返回**: AgentCoordinator

## 故障排除

### 问题 1: Agent 匹配度太低

**原因**: 任务描述不够明确或缺少关键词

**解决方案**:
```python
# ❌ 不好
task = "做点什么"

# ✅ 好
task = "实现用户认证功能，包括登录和注册"
```

### 问题 2: 选择了错误的 Agent

**原因**: 任务描述与多个 agent 的关键词重叠

**解决方案**:
```python
# 检查备选 agents
if context['alternatives']:
    print("其他可选:")
    for alt in context['alternatives']:
        print(f"  - {alt.name}: {alt.role}")

# 或者手动指定
context = coordinator.intercept(
    task_description="...",
    command_name="wf_05_code",
    auto_activate=False  # 手动控制
)
```

### 问题 3: AgentRegistry 加载失败

**原因**: agents/ 目录不存在或 agent 定义文件有错误

**解决方案**:
```bash
# 检查 agents 目录
ls -la ~/.claude/commands/commands/agents/

# 验证 agent 定义
python -c "from commands.lib.agent_registry import AgentRegistry; r = AgentRegistry(); print(f'Loaded {len(r.agents)} agents')"
```

### 问题 4: 单例状态混乱

**原因**: 在测试中多次初始化

**解决方案**:
```python
# 仅在测试中重置
coordinator = get_agent_coordinator()
coordinator.reset()  # 清理状态，保留 registry
```

## 相关文档

- [Agent System Architecture ADR](../adr/2025-12-08-agent-system-architecture.md)
- [AgentRegistry API](agent_registry_api.md)
- [Agent 定义规范](agent_definition_spec.md)
- [多 Agent 协作示例](agent_coordination_examples.md)

## 更新日志

- 2025-12-12: 初始版本，包含完整使用指南和 API 参考
