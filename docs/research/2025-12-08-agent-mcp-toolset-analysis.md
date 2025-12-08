---
title: "Agent-MCP 工具集分析报告"
description: "分析 10 个 Agent 的 MCP 工具集需求，为 MCPSelector 实现提供基础"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-08"
last_updated: "2025-12-08"
related_documents:
  - "commands/lib/agent_router.py"
  - "src/mcp/gateway.py"
  - "TASK.md"
related_code:
  - "commands/agents/*.md"
tags: ["MCP", "Agent", "工具集", "分析"]
authors: ["Claude"]
version: "1.0"
---

# Agent-MCP 工具集分析报告

**目标**: 为 Task 5.2 MCPSelector 实现提供完整的 Agent MCP 需求分析

## 📊 当前状态总览

### 10 个 Agent 的 MCP 集成现状

| Agent | 已声明 MCP 数量 | MCP 服务器 | 优先级 |
|-------|---------------|-----------|--------|
| **pm-agent** | 2 | Serena, Sequential-thinking | Critical |
| **architect-agent** | 4 | Sequential-thinking, Context7, Tavily, Serena | High |
| **code-agent** | 3 | Serena, Magic, Sequential-thinking | High |
| **debug-agent** | 3 | Sequential-thinking, Serena, Context7 | High |
| **test-agent** | 2 | Serena, Sequential-thinking | High |
| **review-agent** | 2 | Serena, Sequential-thinking | High |
| **refactor-agent** | 2 | Serena, Sequential-thinking | Medium |
| **doc-agent** | 3 | Serena, Magic, Sequential-thinking | Medium |
| **research-agent** | 3 | Context7, Tavily, Sequential-thinking | Medium |
| **context-agent** | 2 | Serena, Sequential-thinking | Critical |

### MCP 服务器使用频率统计

| MCP 服务器 | 使用 Agent 数量 | 占比 | 核心用途 |
|-----------|---------------|------|---------|
| **Serena** | 9/10 (90%) | 最高 | 代码理解、符号操作、覆盖率分析 |
| **Sequential-thinking** | 10/10 (100%) | 全覆盖 | 复杂推理、决策分析 |
| **Context7** | 3/10 (30%) | 中 | 官方文档查询 |
| **Tavily** | 2/10 (20%) | 低 | Web 搜索、实时信息 |
| **Magic** | 2/10 (20%) | 低 | UI 组件生成 |
| **Playwright** | 0/10 (0%) | 未使用 | (deploy-check 命令使用，非 Agent) |

**关键发现**:
- ✅ **Sequential-thinking**: 100% Agent 覆盖 → 应作为默认 MCP
- ✅ **Serena**: 90% Agent 覆盖 → 代码相关 Agent 的标配
- ⚠️ **Context7**: 仅 30% 覆盖 → 需要时显式激活
- ⚠️ **Tavily**: 仅 20% 覆盖 → 需要时显式激活
- ⚠️ **Magic**: 仅 20% 覆盖 → UI 相关任务专用

---

## 🔍 详细 Agent MCP 需求分析

### 1. PM Agent (项目管理协调器)

**角色**: 项目管理和任务协调

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "读取项目内存，理解代码库结构"
  - name: "Sequential-thinking"
    usage: "复杂项目规划时的结构化推理"
```

**MCP 使用场景**:
- **Serena**:
  - 评估任务复杂度（代码量分析）
  - 理解代码库架构（for 任务分解）
  - 识别模块依赖关系
- **Sequential-thinking**:
  - 复杂项目规划的多步推理
  - 任务分解决策树
  - 风险评估和优先级排序

**建议优化**: 当前配置已经合理 ✓

---

### 2. Architect Agent (解决方案架构师)

**角色**: 架构设计和技术决策

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Sequential-thinking"
    usage: "复杂架构决策的结构化推理"
  - name: "Context7"
    usage: "查询官方文档，验证技术方案"
  - name: "Tavily"
    usage: "Web 搜索最新技术趋势"
  - name: "Serena"
    usage: "分析现有代码库架构"
```

**MCP 使用场景**:
- **Sequential-thinking**: 架构权衡分析、多方案对比
- **Context7**: 查询框架官方文档、验证 API 可用性
- **Tavily**: 搜索最佳实践、技术趋势、案例研究
- **Serena**: 分析现有代码架构模式、识别技术债务

**建议优化**:
- ✅ 最全面的 MCP 集成（4个）
- 💡 建议：根据任务类型动态选择
  - 新项目架构设计 → Context7 + Tavily + Sequential-thinking
  - 现有项目重构 → Serena + Sequential-thinking
  - 技术选型 → Context7 + Tavily + Sequential-thinking

---

### 3. Code Agent (代码实现工程师)

**角色**: 代码实现和功能开发

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "精确代码定位和智能插入点检测"
  - name: "Magic"
    usage: "UI 组件生成"
  - name: "Sequential-thinking"
    usage: "复杂实现的逻辑推理"
```

**MCP 使用场景**:
- **Serena**:
  - 精确代码定位（find_symbol）
  - 智能插入点检测（insert_before_symbol, insert_after_symbol）
  - 依赖分析（find_referencing_symbols）
- **Magic**:
  - UI 组件自动生成
  - 仅在 UI 相关任务时使用
- **Sequential-thinking**:
  - 复杂业务逻辑的实现推理
  - 算法设计

**建议优化**:
- ✅ 配置合理
- 💡 Magic 应该是**条件性激活**：
  - 任务包含 "UI", "组件", "界面" 关键词时启用
  - 否则跳过以节省资源

---

### 4. Debug Agent (调试专家)

**角色**: 调试和问题诊断

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Sequential-thinking"
    usage: "系统化错误分析和推理"
  - name: "Serena"
    usage: "代码理解和问题定位"
  - name: "Context7"
    usage: "查询官方文档和已知问题"
```

**MCP 使用场景**:
- **Sequential-thinking**: 根因分析、调试流程（6步法）
- **Serena**: 精确定位错误代码、追踪调用链
- **Context7**: 查询框架已知问题、错误代码说明

**建议优化**:
- ✅ 配置合理
- 💡 Context7 应该是**条件性激活**：
  - 错误涉及第三方库/框架时启用
  - 项目内部错误可能不需要

---

### 5. Test Agent (测试工程师)

**角色**: 测试开发和覆盖率分析

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "代码覆盖率分析和未测试路径识别"
  - name: "Sequential-thinking"
    usage: "测试用例设计推理"
```

**MCP 使用场景**:
- **Serena**:
  - 代码覆盖率分析（search_for_pattern, find_symbol）
  - 识别未测试路径
  - 提取公开 API 列表
- **Sequential-thinking**:
  - 测试用例设计（边界条件、异常情况）
  - 测试策略推理

**建议优化**: 当前配置已经合理 ✓

---

### 6. Review Agent (代码审查专家)

**角色**: 代码审查和质量检查

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "符号级代码审查和依赖分析"
  - name: "Sequential-thinking"
    usage: "深度分析的结构化推理"
```

**MCP 使用场景**:
- **Serena**:
  - 符号级审查（find_symbol, find_referencing_symbols）
  - 依赖分析（识别紧耦合）
  - 代码复杂度分析
- **Sequential-thinking**:
  - 7 维度审查的结构化分析
  - 安全漏洞推理
  - 性能问题识别

**建议优化**: 当前配置已经合理 ✓

---

### 7. Refactor Agent (重构专家)

**角色**: 代码重构和优化

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "符号重构和依赖分析 (rename_symbol, replace_symbol_body)"
  - name: "Sequential-thinking"
    usage: "重构策略推理"
```

**MCP 使用场景**:
- **Serena**:
  - rename_symbol（重命名符号）
  - replace_symbol_body（替换符号体）
  - find_referencing_symbols（影响范围分析）
- **Sequential-thinking**:
  - 重构策略推理
  - 风险评估

**建议优化**: 当前配置已经合理 ✓

---

### 8. Doc Agent (文档专家)

**角色**: 文档生成和维护

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "代码分析和 API 提取"
  - name: "Magic"
    usage: "UI 文档生成"
  - name: "Sequential-thinking"
    usage: "文档结构规划"
```

**MCP 使用场景**:
- **Serena**:
  - 提取 API 端点和参数
  - 识别公开接口
  - 分析代码结构
- **Magic**:
  - UI 组件文档生成
  - 仅在 UI 文档时使用
- **Sequential-thinking**:
  - 文档结构规划
  - 内容组织推理

**建议优化**:
- 💡 Magic 应该是**条件性激活**（同 Code Agent）

---

### 9. Research Agent (技术研究员)

**角色**: 技术研究和方案评估

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Context7"
    usage: "查询官方文档"
  - name: "Tavily"
    usage: "Web 搜索和实时信息"
  - name: "Sequential-thinking"
    usage: "系统化研究推理"
```

**MCP 使用场景**:
- **Context7**: 查询框架/库官方文档
- **Tavily**: Web 搜索最佳实践、案例研究、技术对比
- **Sequential-thinking**: 方案对比分析、优缺点推理

**建议优化**: 当前配置已经合理 ✓

---

### 10. Context Agent (上下文管理专家)

**角色**: 上下文加载和会话管理

**当前 MCP 集成**:
```yaml
mcp_integrations:
  - name: "Serena"
    usage: "加载项目内存，初始化语义代码理解"
  - name: "Sequential-thinking"
    usage: "复杂项目状态分析时的结构化推理"
```

**MCP 使用场景**:
- **Serena**:
  - 项目内存激活
  - LSP 初始化
  - 加载语义代码理解
- **Sequential-thinking**:
  - 复杂项目状态分析
  - 会话恢复策略推理

**建议优化**: 当前配置已经合理 ✓

---

## 🎯 MCPSelector 设计建议

### 核心原则

1. **默认 MCP** (所有 Agent):
   - Sequential-thinking: 100% 覆盖，所有 Agent 默认启用

2. **代码相关 MCP** (9/10 Agent):
   - Serena: Code, Debug, Test, Review, Refactor, Doc, Architect, PM, Context
   - 仅 Research Agent 不需要

3. **条件性 MCP**:
   - **Magic**: 仅在任务包含 UI 关键词时启用
     - 关键词: "UI", "组件", "界面", "按钮", "表单", "页面"
   - **Context7**: 仅在涉及第三方库/框架时启用
     - 关键词: 框架名 (React, Vue, Django, etc.)
   - **Tavily**: 仅在需要 Web 搜索时启用
     - 关键词: "最新", "最佳实践", "对比", "趋势"

### MCPSelector 算法

```python
class MCPSelector:
    """
    基于 Agent 类型和任务特征自动选择 MCP 工具
    """

    def select_tools(self, agent: Agent, task: Task) -> List[str]:
        """
        选择 MCP 工具集

        Returns:
            List[str]: MCP 服务器名称列表
        """
        tools = []

        # 1. 默认 MCP (所有 Agent)
        tools.append("sequential-thinking")

        # 2. 代码相关 MCP (除 Research Agent 外)
        if agent.name != "research-agent":
            tools.append("serena")

        # 3. Agent 特定 MCP
        agent_specific = {
            "architect-agent": ["context7", "tavily"],
            "research-agent": ["context7", "tavily"],
        }
        if agent.name in agent_specific:
            tools.extend(agent_specific[agent.name])

        # 4. 任务条件性 MCP
        task_lower = task.description.lower()

        # UI 相关任务 → Magic
        if any(kw in task_lower for kw in ["ui", "组件", "界面", "按钮", "表单", "页面"]):
            if agent.name in ["code-agent", "doc-agent"]:
                tools.append("magic")

        # 第三方库相关 → Context7
        if agent.name in ["debug-agent", "architect-agent"]:
            frameworks = ["react", "vue", "django", "express", "flask"]
            if any(fw in task_lower for fw in frameworks):
                if "context7" not in tools:
                    tools.append("context7")

        # Web 搜索关键词 → Tavily
        if agent.name in ["architect-agent", "research-agent"]:
            search_keywords = ["最新", "最佳实践", "对比", "趋势", "调研"]
            if any(kw in task_lower for kw in search_keywords):
                if "tavily" not in tools:
                    tools.append("tavily")

        return list(set(tools))  # 去重
```

### 性能优化建议

1. **批量查询**:
   - 如果 Agent 需要多个 MCP 工具，并行初始化
   - 使用 `asyncio.gather()` 并发调用

2. **缓存**:
   - MCP 工具实例缓存（avoid 重复初始化）
   - 查询结果缓存（避免重复查询相同信息）

3. **懒加载**:
   - 仅在实际调用时初始化 MCP 工具
   - 使用 Gateway 的 `is_available()` 检查可用性

---

## 📋 实施计划

### Step 1: 实现 MCPSelector 类 ✅ (下一步)

**文件**: `commands/lib/mcp_selector.py`

**功能**:
- `select_tools(agent, task)` - 核心选择逻辑
- `_is_ui_task(task)` - UI 任务检测
- `_has_framework_reference(task)` - 框架引用检测
- `_needs_web_search(task)` - Web 搜索需求检测

### Step 2: 集成到 AgentRouter

**文件**: `commands/lib/agent_router.py`

**修改**:
```python
class AgentRouter:
    def __init__(self, registry: Optional[AgentRegistry] = None):
        self.registry = registry or AgentRegistry()
        self.mcp_selector = MCPSelector()  # 新增

    def route(self, task_description: str, mode: Optional[str] = None) -> AgentWorkflow:
        # ... 现有逻辑 ...

        # 为每个 step 选择 MCP 工具
        for step in workflow.steps:
            step.mcp_tools = self.mcp_selector.select_tools(
                step.agent,
                Task(description=task_description)
            )

        return workflow
```

### Step 3: 性能优化

**批量初始化**:
```python
async def initialize_mcp_tools(tools: List[str]) -> Dict[str, MCPTool]:
    gateway = get_mcp_gateway()

    async def init_tool(tool_name: str):
        if gateway.is_available(tool_name):
            return tool_name, gateway.get_tool(tool_name)
        return tool_name, None

    results = await asyncio.gather(*[init_tool(t) for t in tools])
    return {name: tool for name, tool in results if tool is not None}
```

### Step 4: 更新 Agent 文档

**标准化 `mcp_integrations` 字段**:
- 添加 `activation_condition` 字段
- 区分 "always", "conditional", "optional"

### Step 5: 集成测试

**测试场景**:
- 测试 10 个 Agent 的 MCP 工具选择正确性
- 测试条件性激活逻辑
- 测试性能优化效果

---

## 📊 预期成果

### 量化目标

| 指标 | 当前 | 目标 | 改进 |
|------|------|------|------|
| Agent-MCP 协同效率 | Baseline | +50% | 自动选择工具 |
| MCP 工具使用率 | ~40% | 3x (120%) | 智能激活 |
| 资源浪费 | 高 (不必要的 MCP 加载) | 低 | 条件性激活 |
| 开发者体验 | 手动指定 MCP | 自动化 | 无需关心 MCP |

### 关键成果

1. ✅ **自动化**: Agent 激活时自动选择合适的 MCP 工具
2. ✅ **智能化**: 基于任务特征动态调整 MCP 工具集
3. ✅ **高效化**: 避免不必要的 MCP 加载和调用
4. ✅ **标准化**: 统一的 Agent-MCP 协同模式

---

**维护者**: AI Workflow System
**版本**: 1.0
**最后更新**: 2025-12-08
