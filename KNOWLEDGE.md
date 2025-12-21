# 知识库 (Knowledge Base)

**版本**: v1.9-optimized
**创建日期**: 2025-11-06
**最后更新**: 2025-12-21
**目的**: 项目架构决策、设计模式和技术文档的索引中心

> ℹ️ **说明**: 本文件为纯索引和指针。详细内容已分离到各文件。

---

## 📚 文档索引

### 管理层文档

| 主题 | 路径 | 优先级 |
|------|------|--------|
| 项目需求 | [docs/management/PRD.md](docs/management/PRD.md) | 高 |
| 技术规划 | [docs/management/PLANNING.md](docs/management/PLANNING.md) | 高 |
| 任务追踪 | [docs/management/TASK.md](docs/management/TASK.md) | 高 |
| 会话上下文 | [docs/management/CONTEXT.md](docs/management/CONTEXT.md) | 高 |
| AI执行规则 | [CLAUDE.md](CLAUDE.md) | 中 |
| 设计哲学 | [PHILOSOPHY.md](PHILOSOPHY.md) | 中 |

### MCP 集成参考

| 命令 | MCP 服务器 | 优先级 |
|------|-----------|--------|
| wf_01_planning | Context7 + Tavily | 高 |
| wf_02_task | Serena | 高 |
| wf_03_prime | Serena | 高 |
| wf_04_ask | Sequential-thinking + Context7 + Tavily | 高 |
| wf_04_research | Context7 + Tavily | 高 |
| wf_05_code | Serena + Magic | 高 |
| wf_06_debug | Sequential-thinking + Serena | 高 |
| wf_07_test | Serena + Sequential-thinking | 高 |
| wf_08_review | Serena + Sequential-thinking | 高 |
| wf_09_refactor | Serena | 中 |
| wf_10_optimize | Serena | 中 |
| wf_11_commit | Serena | 高 |
| wf_12_deploy_check | Playwright | 高 |
| wf_14_doc | Magic | 高 |

**Gateway 使用模式**:
```python
from src.mcp.gateway import get_mcp_gateway
gateway = get_mcp_gateway()
if gateway.is_available("mcp_server_name"):
    tool = gateway.get_tool("mcp_server_name", "tool_name")
    result = tool.call(**parameters)
```

**MCP 服务器**:
- **Serena**: 语义代码理解、符号操作、项目内存
- **Context7**: 官方库文档查询
- **Sequential-thinking**: 结构化多步推理
- **Tavily**: Web 搜索和实时信息
- **Playwright**: 浏览器自动化和 E2E 测试
- **Magic**: UI 组件生成

### 技术层文档 (按需加载)

| 主题 | 路径 | 优先级 |
|------|------|--------|
| **AgentCoordinator 使用指南** | [docs/examples/agent_coordinator_usage.md](docs/examples/agent_coordinator_usage.md) | 最高 |
| **DocLoader 使用指南** | [docs/examples/doc_loader_usage.md](docs/examples/doc_loader_usage.md) | 最高 |
| **DocLoader 集成示例** | [docs/examples/wf_integration_example.md](docs/examples/wf_integration_example.md) | 最高 |
| 文档生成快速指南 | [docs/examples/doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md) | 高 |
| 文档维护流程 | [docs/guides/doc_maintenance_process.md](docs/guides/doc_maintenance_process.md) | 高 |
| wf_03_prime 工作流 | [docs/guides/wf_03_prime_workflows.md](docs/guides/wf_03_prime_workflows.md) | 高 |
| wf_04_research 工作流 | [docs/guides/wf_04_research_workflows.md](docs/guides/wf_04_research_workflows.md) | 高 |
| wf_05_code 工作流 | [docs/guides/wf_05_code_workflows.md](docs/guides/wf_05_code_workflows.md) | 高 |
| 部署兼容性指南 | [docs/guides/deployment_compatibility_guide.md](docs/guides/deployment_compatibility_guide.md) | 高 |
| 命令执行一致性策略 | [docs/guides/command_consistency_strategy.md](docs/guides/command_consistency_strategy.md) | 最高 |
| Frontmatter 规范 | [docs/reference/FRONTMATTER.md](docs/reference/FRONTMATTER.md) | 高 |
| Markdown 格式约束 | [docs/reference/MARKDOWN_STYLE.md](docs/reference/MARKDOWN_STYLE.md) | 高 |

### Agent System

| 组件 | 路径 | 优先级 |
|------|------|--------|
| **AgentRegistry** | [commands/lib/agent_registry.py](commands/lib/agent_registry.py) | 高 |
| **TaskAnalyzer** | [commands/lib/task_analyzer.py](commands/lib/task_analyzer.py) | 高 |
| **AgentRouter** | [commands/lib/agent_router.py](commands/lib/agent_router.py) | 高 |
| **CoordinationEngine** | [commands/lib/coordination_engine.py](commands/lib/coordination_engine.py) | 高 |

### 并行审查和执行示例

| 主题 | 路径 | 优先级 |
|------|------|--------|
| 多代理审查概览 | [docs/examples/multi_agent_review_overview.md](docs/examples/multi_agent_review_overview.md) | 高 |
| 并行审查概览 | [docs/examples/parallel_review_overview.md](docs/examples/parallel_review_overview.md) | 高 |
| 并行执行概览 | [docs/examples/parallel_execution_overview.md](docs/examples/parallel_execution_overview.md) | 高 |
| Agent协调示例 | [docs/examples/agent_coordination_examples.md](docs/examples/agent_coordination_examples.md) | 高 |

### 文档生成工作流

| 主题 | 路径 | 优先级 |
|------|------|--------|
| 文档模板库 | [docs/examples/doc_templates/](docs/examples/doc_templates/) | 高 |
| 约束驱动工作流 | [docs/examples/doc_generation_workflow.md](docs/examples/doc_generation_workflow.md) | 高 |
| /wf_14_doc 示例 | [docs/examples/wf_14_doc_examples.md](docs/examples/wf_14_doc_examples.md) | 中 |

### 知识库文档

- 📋 [设计模式](docs/knowledge/DESIGN_PATTERNS.md)
- 📝 [文档最佳实践](docs/knowledge/DOCUMENTATION_PRACTICES.md)
- 🐛 [常见问题](docs/knowledge/FAQ.md)
- 🆕 [版本历史](docs/knowledge/CHANGELOG.md)

---

## 🏗️ 架构决策记录 (ADR)

| 日期 | 标题 | 状态 |
|------|------|------|
| 2025-12-21 | 双 CLAUDE 架构反转 | Proposed |
| 2025-12-17 | Agent 中文支持改进 | Accepted |
| 2025-12-12 | 命令执行一致性策略 | Accepted |
| 2025-12-08 | Agent System 架构 | Accepted |
| 2025-12-01 | MCP 深度集成 | Accepted |

详见 [docs/adr/](docs/adr/)

---

## 📊 项目统计

- **命令数**: 14 个 (wf_01 - wf_14)
- **Agent 数**: 10 个 (PM, Architect, Code, Debug, Test, Review, Refactor, Doc, Research, Context)
- **MCP 服务器**: 6 个 (Serena, Context7, Sequential-thinking, Tavily, Playwright, Magic)
- **MCP 命令覆盖**: 14/14 (100%)
- **技术文档**: 113 个
- **ADR**: 14 个

---

## 🚀 快速导航

**新用户**: 从 [README.md](README.md) 开始
**开发者**: 查看 [CLAUDE.md](CLAUDE.md) 执行规则
**架构师**: 参考 [PLANNING.md](docs/management/PLANNING.md)
**项目经理**: 查看 [TASK.md](docs/management/TASK.md)

---

**维护者**: AI Workflow System
**版本**: v1.9-optimized (精简版本)
**最后更新**: 2025-12-21
