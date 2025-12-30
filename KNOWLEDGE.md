# 知识库索引 (Knowledge Base Index)

**版本**: v2.0 (AI 工具知识库)
**创建日期**: 2025-11-06
**最后更新**: 2025-12-29
**目的**: AI 工具和开发最佳实践的知识库索引中心

> 本仓库已从 Workflow 命令系统转型为 AI 工具知识库。历史内容已归档到 `archive/` 目录。

---

## 📚 知识库结构

### 核心内容区域

| 区域 | 路径 | 说明 |
|------|------|------|
| **最佳实践** | [best-practices/](best-practices/) | 设计哲学、文档架构、AI 协作模式 |
| **MCP 集成** | [mcp-integration/](mcp-integration/) | MCP 服务器使用指南和故障排查 |
| **架构决策** | [docs/adr/](docs/adr/) | 17 个架构决策记录 (ADR) |
| **参考文档** | [docs/reference/](docs/reference/) | Frontmatter、Markdown 格式等规范 |
| **工具库** | [commands/lib/](commands/lib/) | DocLoader、AgentCoordinator 等工具 |

### 归档内容

| 区域 | 路径 | 说明 |
|------|------|------|
| **Workflow 命令** | [archive/workflow-commands/](archive/workflow-commands/) | 14 个 wf_ 命令文件 |
| **Workflow 指南** | [archive/workflow-guides/](archive/workflow-guides/) | 工作流使用指南和示例 |
| **项目历史** | [archive/project-history/](archive/project-history/) | PRD、TASK、CONTEXT 等历史文档 |

---

## 🎯 最佳实践索引

### 设计哲学和原则

| 主题 | 文档 | 核心价值 |
|------|------|----------|
| **Ultrathink 设计思维** | [best-practices/philosophy.md](best-practices/philosophy.md) | 6 个核心原则：质疑假设、明确权衡、持续打磨 |
| **文档架构设计** | [best-practices/document-architecture.md](best-practices/document-architecture.md) | 四层文档架构、SSOT 原则、约束驱动文档生成 |
| **AI 协作模式** | [best-practices/ai-collaboration.md](best-practices/ai-collaboration.md) | 上下文管理、约束驱动交互、质量门控 |

### 核心设计原则

**1. Ultrathink 设计思维** (来自 [PHILOSOPHY.md](PHILOSOPHY.md))
- Think Different - 质疑假设，追求最优
- Balance Trade-offs - 明确权衡，记录决策
- Iterate to Excellence - 持续打磨
- Context Aware - 理解环境
- Document Decisions - 沉淀学习
- Test Assumptions - 验证假设

**2. 约束驱动文档生成** (来自 [ADR 2025-11-18](docs/adr/2025-11-18-constraint-driven-documentation-generation.md))
- 三阶段门控：决策 → 估计 → 验证
- 成本约束：文档大小 < 500 行，增长率 < 30%
- Frontmatter：7 个必需字段 + 关系网络

**3. 优先开源方案** (来自 [ADR 2025-11-13](docs/adr/2025-11-13-prioritize-opensource-in-architecture.md))
- 优先开源，成熟优先，标准优先
- 记录决策理由和权衡
- 通过 PoC 验证关键假设

---

## 🔌 MCP 集成索引

### AIRIS MCP Gateway 集成

> **NEW**: 通过 AIRIS MCP Gateway 统一访问 13 个 MCP 服务器的 112 个工具

| 资源 | 说明 | 链接 | 优先级 |
|------|------|------|--------|
| **完整指南** | AIRIS MCP Gateway 使用指南 | [docs/airis-mcp-gateway/README.md](docs/airis-mcp-gateway/README.md) | ⭐⭐⭐ |
| **故障排查** | 常见问题和解决方案（含参数陷阱） | [docs/airis-mcp-gateway/TROUBLESHOOTING.md](docs/airis-mcp-gateway/TROUBLESHOOTING.md) | ⭐⭐⭐ |
| **参数陷阱** | 常见参数命名错误和正确用法速查 | [docs/airis-mcp-gateway/PARAMETER_TRAPS.md](docs/airis-mcp-gateway/PARAMETER_TRAPS.md) | ⭐⭐⭐ |
| **快速参考** | 常用工具和参数速查 | [docs/airis-mcp-gateway/QUICK_REFERENCE.md](docs/airis-mcp-gateway/QUICK_REFERENCE.md) | ⭐⭐ |
| **工具索引** | 112 个工具按字母排序 | [docs/airis-mcp-gateway/TOOL_INDEX.md](docs/airis-mcp-gateway/TOOL_INDEX.md) | ⭐⭐ |
| **服务器文档** | 8 个核心服务器详细说明 | [docs/airis-mcp-gateway/servers/](docs/airis-mcp-gateway/servers/) | ⭐ |
| **文档缺失分析** | 文档完成进度和后续工作 | [docs/airis-mcp-gateway/DOCUMENTATION_GAP_ANALYSIS.md](docs/airis-mcp-gateway/DOCUMENTATION_GAP_ANALYSIS.md) | ⭐ |

**覆盖的 MCP 服务器** (13 个):
- **HOT 模式** (4): airis-agent, memory, gateway-control, airis-commands
- **COLD 模式** (9): serena, playwright, tavily, context7, morphllm, magic, chrome-devtools, fetch, sequential-thinking

**三步工作流**:
```typescript
// Step 1: 发现工具
airis-find(query: "keyword")

// Step 2: 查看参数
airis-schema(tool: "server:tool_name")

// Step 3: 执行工具
airis-exec(tool: "server:tool_name", arguments: {...})
```

### MCP 服务器（传统集成）

| MCP | 功能 | 配置文件 | 指南 |
|-----|------|----------|------|
| **Serena** | 语义代码理解、项目内存 | [src/mcp/configs/serena.json](src/mcp/configs/serena.json) | [mcp-integration/](mcp-integration/) |
| **Context7** | 官方库文档查询 | [src/mcp/configs/context7.json](src/mcp/configs/context7.json) | [mcp-integration/](mcp-integration/) |
| **Sequential-thinking** | 结构化多步推理 | [src/mcp/configs/sequential-thinking.json](src/mcp/configs/sequential-thinking.json) | - |
| **Tavily** | Web 搜索 | [src/mcp/configs/tavily.json](src/mcp/configs/tavily.json) | - |
| **Magic** | UI 组件生成 | [src/mcp/configs/magic.json](src/mcp/configs/magic.json) | - |

### MCP 使用指南

| 主题 | 文档 |
|------|------|
| **MCP 架构** | [mcp-integration/MCP_ARCHITECTURE.md](mcp-integration/MCP_ARCHITECTURE.md) |
| **快速开始** | [mcp-integration/quick-start.md](mcp-integration/quick-start.md) |
| **Serena 指南** | [mcp-integration/README.md](mcp-integration/README.md) |
| **故障排查** | [mcp-integration/troubleshooting.md](mcp-integration/troubleshooting.md) |

### Gateway 使用模式

```python
from src.mcp.gateway import get_mcp_gateway

gateway = get_mcp_gateway()

# 检查 MCP 可用性
if gateway.is_available("serena"):
    # 获取工具
    tool = gateway.get_tool("serena", "find_symbol")
    # 调用工具
    result = tool.call(name="MyClass")
```

---

## 📖 架构决策记录 (ADR)

### 核心决策

| 日期 | 主题 | ADR |
|------|------|-----|
| 2025-11-07 | 智能文档生成 vs 模板驱动 | [2025-11-07-intelligent-doc-generation-over-template-based.md](docs/adr/2025-11-07-intelligent-doc-generation-over-template-based.md) |
| 2025-11-13 | 优先开源方案的架构原则 | [2025-11-13-prioritize-opensource-in-architecture.md](docs/adr/2025-11-13-prioritize-opensource-in-architecture.md) |
| 2025-11-15 | CONTEXT.md 指针文档模式 | [2025-11-15-context-md-pointer-document.md](docs/adr/2025-11-15-context-md-pointer-document.md) |
| 2025-11-15 | 工作流文档生成 SSOT | [2025-11-15-workflow-document-generation-ssot.md](docs/adr/2025-11-15-workflow-document-generation-ssot.md) |
| 2025-11-18 | 约束驱动文档生成 | [2025-11-18-constraint-driven-documentation-generation.md](docs/adr/2025-11-18-constraint-driven-documentation-generation.md) |
| 2025-11-21 | MCP 集成策略 | [2025-11-21-mcp-integration-strategy.md](docs/adr/2025-11-21-mcp-integration-strategy.md) |
| 2025-12-03 | SuperClaude 优化总结 | [2025-12-03-superclaude-optimization-learnings.md](docs/adr/2025-12-03-superclaude-optimization-learnings.md) |
| 2025-12-08 | Agent 系统架构 | [2025-12-08-agent-system-architecture.md](docs/adr/2025-12-08-agent-system-architecture.md) |
| 2025-12-23 | Agent 执行系统重构 | [2025-12-23-agent-execution-system-redesign.md](docs/adr/2025-12-23-agent-execution-system-redesign.md) |

### ADR 分类

**文档和架构**:
- 智能文档生成、SSOT 原则、约束驱动生成
- 四层文档架构、CONTEXT.md 指针模式

**技术选型**:
- 优先开源方案
- 使用现有工具而非重新实现

**MCP 集成**:
- MCP 集成策略
- Serena 三层角色模型
- MCP 和文档互补架构

**Agent 系统**:
- Agent 系统架构
- Agent 执行系统重构

**性能优化**:
- SuperClaude 优化总结
- 命令优化策略

---

## 🛠️ 工具和脚本索引

### 核心工具

| 工具 | 路径 | 说明 |
|------|------|------|
| **DocLoader** | [commands/lib/doc_loader.py](commands/lib/doc_loader.py) | 智能文档加载（摘要/章节模式） |
| **AgentCoordinator** | [commands/lib/agent_coordinator.py](commands/lib/agent_coordinator.py) | 多 Agent 协调器 |
| **AgentDecisionEngine** | [commands/lib/agent_decision_engine.py](commands/lib/agent_decision_engine.py) | Agent 决策引擎 |
| **DocGuard** | [scripts/doc_guard.py](scripts/doc_guard.py) | 文档读取保护工具 |
| **FrontmatterUtils** | [scripts/frontmatter_utils.py](scripts/frontmatter_utils.py) | Frontmatter 验证和管理 |

### 使用示例

**DocLoader**:
```python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 摘要模式（100-300行文档）
summary = loader.load_summary(doc_path, max_lines=50)

# 章节模式（300-800行文档）
content = loader.load_sections(
    doc_path,
    sections=["Step 3", "MCP Integration"]
)
```

**AgentCoordinator**:
```python
from commands.lib.agent_coordinator import AgentCoordinator

coord = AgentCoordinator()
result = coord.coordinate_agent(
    agent_name="architect",
    task="设计用户认证系统",
    context={"requirements": [...]}
)
```

---

## 📖 参考文档

### 核心文档

| 文档 | 用途 |
|------|------|
| [README.md](README.md) | 项目介绍和快速开始 |
| [PHILOSOPHY.md](PHILOSOPHY.md) | Ultrathink 设计哲学 |
| [CLAUDE.md](CLAUDE.md) | AI 执行规则（源码开发规范） |
| [CLAUDE_DEPLOY.md](CLAUDE_DEPLOY.md) | AI 执行规则（全局部署规范） |
| [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md) | 文档架构设计 |

### 规范文档

| 文档 | 用途 |
|------|------|
| [docs/reference/FRONTMATTER.md](docs/reference/FRONTMATTER.md) | Frontmatter 元数据规范 |
| [docs/reference/MARKDOWN_STYLE.md](docs/reference/MARKDOWN_STYLE.md) | Markdown 格式约束 |
| [docs/adr/README.md](docs/adr/README.md) | ADR 模板和指南 |

---

## 🎯 快速导航

### 我想...

**了解设计哲学** → [best-practices/philosophy.md](best-practices/philosophy.md)

**学习文档架构** → [best-practices/document-architecture.md](best-practices/document-architecture.md)

**查看 MCP 集成** → [mcp-integration/](mcp-integration/)

**查阅架构决策** → [docs/adr/](docs/adr/)

**使用工具库** → [commands/lib/](commands/lib/)

**查看历史内容** → [archive/](archive/)

---

## 📊 知识库统计

| 类型 | 数量 |
|------|------|
| **最佳实践文档** | 3 |
| **MCP 集成文档** | 4 |
| **AIRIS MCP Gateway 文档** | 13 (NEW) |
| **架构决策记录** | 17 |
| **工具库** | 5 |
| **参考文档** | 3 |
| **归档文档** | 30+ |

**AIRIS MCP Gateway 覆盖**:
- 核心指南: 3 个 (README, QUICK_REFERENCE, TOOL_INDEX)
- 服务器文档: 8 个 (Serena, Memory, Tavily, Playwright, Context7, Magic, MorphLLM, Fetch)
- 工具总数: 112 个 across 13 个 MCP 服务器

---

**最后更新**: 2025-12-29
**版本**: v2.0 (AI 工具知识库)
