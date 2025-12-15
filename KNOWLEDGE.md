# 知识库 (Knowledge Base)

**版本**: v1.8
**创建日期**: 2025-11-06
**最后更新**: 2025-12-14
**目的**: 项目架构决策、设计模式和技术文档的索引中心

> ℹ️ **注意**: 本文件为纯索引和指针，详细内容已分离到 `docs/knowledge/` 目录以减少维护成本和上下文消耗。

---

## 📚 文档索引

### 管理层文档 (prime自动加载)

| 主题 | 路径 | 优先级 |
|------|------|--------|
| 项目需求 | [docs/management/PRD.md](docs/management/PRD.md) | 高 |
| 技术规划 | [docs/management/PLANNING.md](docs/management/PLANNING.md) | 高 |
| 任务追踪 | [docs/management/TASK.md](docs/management/TASK.md) | 高 |
| 会话上下文 | [docs/management/CONTEXT.md](docs/management/CONTEXT.md) | 高 |
| AI执行规则 | [CLAUDE.md](CLAUDE.md) | 中 |
| 设计哲学 | [PHILOSOPHY.md](PHILOSOPHY.md) | 中 |

### MCP 集成参考 (新增 2025-12-08)

**完整 MCP 覆盖率** - 所有 14 个命令均已集成 MCP 支持:

| 命令 | MCP 服务器 | 文档路径 | 优先级 |
|------|-----------|---------|--------|
| wf_01_planning | Context7 + Tavily | [wf_01_planning.md](wf_01_planning.md) | 高 |
| wf_02_task | Serena | [wf_02_task.md](wf_02_task.md) | 高 |
| wf_03_prime | Serena | [wf_03_prime.md](wf_03_prime.md) | 高 |
| wf_04_ask | Sequential-thinking + Context7 + Tavily | [wf_04_ask.md](wf_04_ask.md) | 高 |
| wf_04_research | Context7 + Tavily | [wf_04_research.md](wf_04_research.md) | 高 |
| wf_05_code | Serena + Magic | [wf_05_code.md](wf_05_code.md) | 高 |
| wf_06_debug | Sequential-thinking + Serena | [wf_06_debug.md](wf_06_debug.md) | 高 |
| wf_07_test | Serena + Sequential-thinking | [wf_07_test.md](wf_07_test.md) | 高 |
| wf_08_review | Serena + Sequential-thinking | [wf_08_review.md](wf_08_review.md) | 高 |
| wf_09_refactor | Serena | [wf_09_refactor.md](wf_09_refactor.md) | 中 |
| wf_10_optimize | Serena | [wf_10_optimize.md](wf_10_optimize.md) | 中 |
| wf_11_commit | Serena | [wf_11_commit.md](wf_11_commit.md) | 高 |
| wf_12_deploy_check | Playwright | [wf_12_deploy_check.md](wf_12_deploy_check.md) | 高 |
| wf_14_doc | Magic | [wf_14_doc.md](wf_14_doc.md) | 高 |

**Gateway 使用模式** (统一实现):
```python
# 标准 Gateway 调用模式
from src.mcp.gateway import get_mcp_gateway

gateway = get_mcp_gateway()
if gateway.is_available("mcp_server_name"):
    tool = gateway.get_tool("mcp_server_name", "tool_name")
    result = tool.call(**parameters)
else:
    # 降级处理
```

**MCP 服务器功能总览**:
- **Serena**: 语义代码理解、符号操作、项目内存
- **Context7**: 官方库文档查询
- **Sequential-thinking**: 结构化多步推理
- **Tavily**: Web 搜索和实时信息
- **Playwright**: 浏览器自动化和 E2E 测试
- **Magic**: UI 组件生成

**关键文档**:
- MCP Gateway 实现: [src/mcp/gateway.py](src/mcp/gateway.py)
- MCP 集成策略: [docs/integration/MCP_INTEGRATION_STRATEGY.md](docs/integration/MCP_INTEGRATION_STRATEGY.md)

### 技术层文档 (按需加载)

| 主题 | 路径 | 优先级 |
|------|------|--------|
| **AgentCoordinator 使用指南** | [docs/examples/agent_coordinator_usage.md](docs/examples/agent_coordinator_usage.md) | 🔴 最高 |
| **DocLoader 使用指南** | [docs/examples/doc_loader_usage.md](docs/examples/doc_loader_usage.md) | 🔴 最高 |
| **DocLoader 集成示例** | [docs/examples/wf_integration_example.md](docs/examples/wf_integration_example.md) | 🔴 最高 |
| 文档生成快速指南 | [docs/examples/doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md) | 高 |
| 文档生成决策树 | [docs/examples/doc_generation_decision_tree.md](docs/examples/doc_generation_decision_tree.md) | 高 |
| Frontmatter 快速参考 | [docs/examples/frontmatter_quick_reference.md](docs/examples/frontmatter_quick_reference.md) | 高 |
| **文档维护详细流程** | [docs/guides/doc_maintenance_process.md](docs/guides/doc_maintenance_process.md) | 高 |
| **文档维护工作流指南** | [docs/guides/doc_maintenance_workflows.md](docs/guides/doc_maintenance_workflows.md) | 高 |
| **wf_03_prime MCP Serena 增强指南** | [docs/guides/wf_03_prime_mcp_serena.md](docs/guides/wf_03_prime_mcp_serena.md) | 高 |
| **wf_03_prime 工作流导航指南** | [docs/guides/wf_03_prime_workflows.md](docs/guides/wf_03_prime_workflows.md) | 高 |
| **wf_03_prime 智能加载详解** | [docs/guides/wf_03_prime_smart_loading.md](docs/guides/wf_03_prime_smart_loading.md) | 中 |
| **命令执行一致性策略** (NEW) | [docs/guides/command_consistency_strategy.md](docs/guides/command_consistency_strategy.md) | 🔴 最高 | 引用文档+强制约束模式，提升AI执行一致性 (2025-12-12) |
| **wf_04_research MCP 增强指南** | [docs/guides/wf_04_research_mcp_guide.md](docs/guides/wf_04_research_mcp_guide.md) | 高 |
| **wf_04_research 工作流和决策指南** | [docs/guides/wf_04_research_workflows.md](docs/guides/wf_04_research_workflows.md) | 高 |
| **wf_04_research 输出格式规范** | [docs/guides/wf_04_research_output_formats.md](docs/guides/wf_04_research_output_formats.md) | 高 |
| **wf_05_code 文档同步决策树指南** | [docs/guides/wf_05_code_doc_sync_guide.md](docs/guides/wf_05_code_doc_sync_guide.md) | 高 |
| **wf_05_code Serena MCP 使用指南** | [docs/guides/wf_05_code_serena_guide.md](docs/guides/wf_05_code_serena_guide.md) | 高 |
| **wf_05_code 工作流和决策路径指南** | [docs/guides/wf_05_code_workflows.md](docs/guides/wf_05_code_workflows.md) | 高 |
| **老版本部署兼容性指南** (NEW) | [docs/guides/deployment_compatibility_guide.md](docs/guides/deployment_compatibility_guide.md) | 高 | 环境版本检测、命令兼容性、迁移指南 (Task 2.11) |
| **兼容性验证脚本** (NEW) | [scripts/validate_command_compatibility.py](scripts/validate_command_compatibility.py) | 高 | 自动检测环境和MCP可用性、14命令验证 (Task 2.12) |
| **上下文加载优化脚本** (NEW) | [scripts/optimize_context_loading.py](scripts/optimize_context_loading.py) | 中 | Prime分析、Docs索引覆盖率、优化建议 (Task 2.12) |
| 架构决策记录 | [docs/adr/](docs/adr/) | 中 |
| Frontmatter 规范 | [docs/reference/FRONTMATTER.md](docs/reference/FRONTMATTER.md) | 高 |
| Markdown 格式约束 | [docs/reference/MARKDOWN_STYLE.md](docs/reference/MARKDOWN_STYLE.md) | 高 |
| MCP 集成 | [docs/integration/](docs/integration/) | 高 |

### Agent System (新增 2025-12-08)

**核心组件**:

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| **AgentRegistry** | [commands/lib/agent_registry.py](commands/lib/agent_registry.py) | 高 | 智能路由和自动激活引擎 |
| **TaskAnalyzer** | [commands/lib/task_analyzer.py](commands/lib/task_analyzer.py) | 高 | 任务分析和意图识别 (9种意图分类) |
| **AgentRouter** | [commands/lib/agent_router.py](commands/lib/agent_router.py) | 高 | Multi-agent协调和工作流编排 |
| **CoordinationEngine** | [commands/lib/coordination_engine.py](commands/lib/coordination_engine.py) | 高 | Multi-agent工作流执行引擎 (3种协调模式) |
| **Auto-Activation Demo** | [commands/lib/auto_activation_demo.py](commands/lib/auto_activation_demo.py) | 中 | 完整自动激活流程演示 |
| **PM Agent** | [commands/agents/pm_agent.md](commands/agents/pm_agent.md) | 高 | 项目管理和任务协调 |
| **Architect Agent** | [commands/agents/architect_agent.md](commands/agents/architect_agent.md) | 高 | 系统设计和技术选型 |
| **Code Agent** | [commands/agents/code_agent.md](commands/agents/code_agent.md) | 高 | 代码实现和功能开发 |
| **Debug Agent** | [commands/agents/debug_agent.md](commands/agents/debug_agent.md) | 高 | 错误分析和问题修复 |
| **Test Agent** | [commands/agents/test_agent.md](commands/agents/test_agent.md) | 高 | 测试开发和覆盖率分析 |
| **Review Agent** | [commands/agents/review_agent.md](commands/agents/review_agent.md) | 高 | 代码审查和质量检查 |
| **Refactor Agent** | [commands/agents/refactor_agent.md](commands/agents/refactor_agent.md) | 中 | 代码重构和技术债务 |
| **Doc Agent** | [commands/agents/doc_agent.md](commands/agents/doc_agent.md) | 中 | 文档生成和维护 |
| **Research Agent** | [commands/agents/research_agent.md](commands/agents/research_agent.md) | 中 | 技术调研和方案评估 |
| **Context Agent** | [commands/agents/context_agent.md](commands/agents/context_agent.md) | 高 | 上下文加载和会话管理 |

**设计决策**: 参见 ADR 2025-12-08 Agent System Architecture

### 并行开发和审查示例 (新增 2025-12-07)

**多代理审查模式** (Multi-agent Review):

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| 多代理审查概览 | [docs/examples/multi_agent_review_overview.md](docs/examples/multi_agent_review_overview.md) | 高 | Agent 协调和角色分工策略 |
| 案例1: API重构审查 | [docs/examples/multi_agent_review_case1_api_refactor.md](docs/examples/multi_agent_review_case1_api_refactor.md) | 中 | 5个专家并行审查REST API |
| 案例2: 数据库迁移审查 | [docs/examples/multi_agent_review_case2_database_migration.md](docs/examples/multi_agent_review_case2_database_migration.md) | 中 | MongoDB→PostgreSQL迁移验证 |
| 案例3: 安全加固审查 | [docs/examples/multi_agent_review_case3_security.md](docs/examples/multi_agent_review_case3_security.md) | 中 | 6个安全维度并行评估 |
| 案例4: 性能优化审查 | [docs/examples/multi_agent_review_case4_performance.md](docs/examples/multi_agent_review_case4_performance.md) | 中 | 5倍性能提升方案验证 |
| 多代理审查技巧 | [docs/examples/multi_agent_review_tips.md](docs/examples/multi_agent_review_tips.md) | 中 | Agent选择、避坑和最佳实践 |

**并行审查模式** (Parallel Review - Wave→Checkpoint→Wave):

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| 并行审查概览 | [docs/examples/parallel_review_overview.md](docs/examples/parallel_review_overview.md) | 高 | Wave→Checkpoint→Wave模式 |
| 案例1: 多文件代码审查 | [docs/examples/parallel_review_case1_multifile.md](docs/examples/parallel_review_case1_multifile.md) | 中 | 8文件并行读取和4维度审查 |
| 案例2: 大规模重构审查 | [docs/examples/parallel_review_case2_refactoring.md](docs/examples/parallel_review_case2_refactoring.md) | 中 | 15文件React Hooks重构验证 |
| 案例3: 测试覆盖率审查 | [docs/examples/parallel_review_case3_test_coverage.md](docs/examples/parallel_review_case3_test_coverage.md) | 中 | 78%→92%覆盖率提升路线图 |
| 案例4: 文档代码同步审查 | [docs/examples/parallel_review_case4_doc_sync.md](docs/examples/parallel_review_case4_doc_sync.md) | 中 | API文档与代码一致性验证 |
| 并行审查技巧 | [docs/examples/parallel_review_tips.md](docs/examples/parallel_review_tips.md) | 中 | 性能优化和决策树 |

**并行执行模式** (Parallel Execution):

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| 并行执行概览 | [docs/examples/parallel_execution_overview.md](docs/examples/parallel_execution_overview.md) | 高 | Wave→Checkpoint→Wave核心机制 |
| 案例1: 功能开发 | [docs/examples/parallel_execution_case1_feature_development.md](docs/examples/parallel_execution_case1_feature_development.md) | 中 | 3 agents并行开发注册功能 |
| 案例2: 数据迁移 | [docs/examples/parallel_execution_case2_migration.md](docs/examples/parallel_execution_case2_migration.md) | 中 | 顺序链模式迁移3阶段 |
| 案例3: 测试开发 | [docs/examples/parallel_execution_case3_testing.md](docs/examples/parallel_execution_case3_testing.md) | 中 | 并行测试策略和覆盖率 |
| 案例4: 系统集成 | [docs/examples/parallel_execution_case4_integration.md](docs/examples/parallel_execution_case4_integration.md) | 中 | 微服务集成3阶段协调 |
| 并行执行技巧 | [docs/examples/parallel_execution_tips.md](docs/examples/parallel_execution_tips.md) | 中 | 性能优化和常见问题 |

**Agent协调示例**:

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| Agent模式协调实战 | [docs/examples/agent_coordination_examples.md](docs/examples/agent_coordination_examples.md) | 高 | 3种策略6个完整案例 |

### 文档生成模板和工作流 (新增 2025-11-27)

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| **文档模板库** | [docs/examples/doc_templates/](docs/examples/doc_templates/) | 高 | 5种标准文档模板 (README, API, DEV_GUIDE, DEPLOYMENT, ARCHITECTURE) |
| README 模板 | [docs/examples/doc_templates/README_template.md](docs/examples/doc_templates/README_template.md) | 高 | 项目概览文档模板 |
| API 文档模板 | [docs/examples/doc_templates/API_template.md](docs/examples/doc_templates/API_template.md) | 高 | API 端点文档模板 |
| 开发指南模板 | [docs/examples/doc_templates/DEV_GUIDE_template.md](docs/examples/doc_templates/DEV_GUIDE_template.md) | 高 | 开发环境设置模板 |
| 部署文档模板 | [docs/examples/doc_templates/DEPLOYMENT_template.md](docs/examples/doc_templates/DEPLOYMENT_template.md) | 高 | 部署指南模板 |
| 架构文档模板 | [docs/examples/doc_templates/ARCHITECTURE_template.md](docs/examples/doc_templates/ARCHITECTURE_template.md) | 高 | 系统架构模板 |
| **约束驱动工作流** | [docs/examples/doc_generation_workflow.md](docs/examples/doc_generation_workflow.md) | 高 | 6步约束驱动文档生成流程 |
| **输出格式参考** | [docs/examples/doc_generation_outputs.md](docs/examples/doc_generation_outputs.md) | 高 | 3种标准报告格式 |
| **后续步骤指南** | [docs/examples/doc_generation_next_steps.md](docs/examples/doc_generation_next_steps.md) | 高 | 4种后续路径和决策表 |
| **最佳实践** | [docs/examples/doc_generation_best_practices.md](docs/examples/doc_generation_best_practices.md) | 高 | 使用时机、审查流程、性能优化 |
| **故障排查** | [docs/examples/doc_generation_troubleshooting.md](docs/examples/doc_generation_troubleshooting.md) | 高 | 限制说明和常见问题解决 |
| **UI 增强模板** | [docs/examples/doc_templates/ui_enhanced/](docs/examples/doc_templates/ui_enhanced/) | 中 | Magic MCP UI 组件模板 (4种) |
| **完整示例库** | [docs/examples/wf_14_doc_examples.md](docs/examples/wf_14_doc_examples.md) | 中 | /wf_14_doc 执行示例和参考 |

### 知识库详细文档 (docs/knowledge/)

- 📋 [设计模式](docs/knowledge/DESIGN_PATTERNS.md) - 工作流、权限、架构
- 📝 [文档最佳实践](docs/knowledge/DOCUMENTATION_PRACTICES.md) - 约束、流程
- 🐛 [常见问题](docs/knowledge/FAQ.md) - 系统、设计、架构问题
- 🆕 [版本历史](docs/knowledge/CHANGELOG.md) - 新增功能、设计决策

---

## 🏗️ 架构决策记录 (ADR)

**已有决策** (14个):

| 日期 | 标题 | 影响 | 状态 |
|------|------|------|------|
| 2025-12-12 | 命令执行一致性策略 | 全局 | Accepted |
| 2025-12-09 | Workflow 系统三层架构迁移策略 | 全局 | Proposed |
| 2025-12-08 | Agent System Architecture | 全局 | Accepted |
| 2025-12-03 | SuperClaude Framework 对比分析与优化决策 | 全局 | Proposed |
| 2025-11-27 | Serena MCP 集成扩展策略 | 高 | Proposed |
| 2025-11-24 | 约束驱动的文档生成最佳实践 | 高 | Accepted |
| 2025-11-23 | MCP 与管理文档的互补架构 | 高 | Accepted |
| 2025-11-23 | Serena 三层角色模型 | 高 | Accepted |
| 2025-11-21 | MCP 集成策略 | 全局 | Accepted |
| 2025-11-18 | 约束驱动的文档生成 | 高 | Accepted |
| 2025-11-15 | Workflow 文档生成 SSOT | 高 | Accepted |
| 2025-11-15 | CONTEXT.md 指针文档 | 高 | Accepted |
| 2025-11-13 | 架构咨询优先开源方案 | 高 | Accepted |
| 2025-11-11 | 使用项目工具而非重新实现 | 高 | Accepted |
| 2025-11-07 | 智能文档生成 | 高 | Accepted |

详见: [docs/adr/](docs/adr/)

### 最新决策亮点 (2025-12-12)

**命令执行一致性优化** (引用文档 + 强制约束模式):
- ✅ **问题**：wf_03_prime 等命令执行结果不一致，AI 理解存在随机性
- ✅ **核心原因**：
  - 命令文件详细描述不足 → AI 自由解释
  - 缺少强制验证点 → AI 可能跳过步骤
  - 输出格式描述模糊 → 结果格式不统一
- ✅ **方案**：引用文档 + 强制约束模式
  - **Step 0.0**: 强制读取工作流指南（使用 Doc Guard）
  - **执行检查清单**: AI 必须验证的检查项
  - **标准输出模板**: 明确的输出格式
  - **决策树**: 替代模糊的自然语言描述

**实施成果** (2025-12-12):
- ✅ **标准化模板创建**: `docs/guides/_TEMPLATE_workflows.md`
- ✅ **wf_06_debug 优化完成**:
  - 创建：`docs/guides/wf_06_debug_workflows.md` (524行)
  - 修改：添加强制规则 + 执行检查清单
  - 三种调试模式决策树（Quick Fix / Standard / Deep Analysis）
- ✅ **wf_08_review 优化完成**:
  - 创建：`docs/guides/wf_08_review_workflows.md` (321行)
  - 修改：添加强制规则 + 7维度审查检查清单
  - 明确的评分标准和输出模板
- ✅ **已应用命令** (5/15):
  - wf_03_prime.md ✅（之前已优化）
  - wf_04_ask.md ✅（之前已优化）
  - wf_05_code.md ✅（之前已优化）
  - wf_06_debug.md ✅（本次优化）
  - wf_08_review.md ✅（本次优化）

**待优化命令** (10/15 - 优先级排序):
- 🔴 **高优先级** (>500行):
  - wf_11_commit.md (773行) - Git 提交，多验证步骤
  - wf_14_doc.md (822行) - 文档生成，复杂度高
  - wf_12_deploy_check.md (508行) - 部署检查，多层验证
- 🟡 **中优先级** (300-500行):
  - wf_07_test.md (382行) - 测试开发
  - wf_09_refactor.md (395行) - 代码重构
  - wf_10_optimize.md (341行) - 性能优化
  - wf_01_planning.md (353行) - 项目规划
  - wf_99_help.md (334行) - 帮助系统
- ⚪ **低优先级** (~300行):
  - wf_02_task.md (301行) - 任务管理

**预期效果**:
- 一致性提升：执行结果稳定性 70% → >90%
- Token 优化：主命令文件轻量（~300行），详细指南按需加载
- 维护成本降低：详细指南集中管理，减少重复

详见: [docs/guides/command_consistency_strategy.md](docs/guides/command_consistency_strategy.md)

---

### 前次决策亮点 (2025-12-09)

**Workflow 系统优化策略**:
- ✅ **问题**：命令文件膨胀（>1000行），文档读取上下文超限
- ✅ **方案**：两阶段优化（短期DocLoader + 长期三层架构）
- ✅ **参考**：SuperClaude Framework三层架构模式
- ✅ **阶段1**：DocLoader实现 ✅ **已完成**（2025-12-09）
- 🟡 **阶段2**：命令/逻辑/配置分离（2-3周，减少70%）

**阶段1实现成果** (2025-12-09):
- ✅ DocLoader 类实现（361行，12个方法）
- ✅ 核心功能：章节加载、摘要模式、Token估算、缓存
- ✅ 测试覆盖：4/4 测试通过
- ✅ 使用文档：[docs/examples/doc_loader_usage.md](docs/examples/doc_loader_usage.md)
- ✅ Token优化：章节加载80%节省，摘要模式95%节省

**阶段2A实现成果** (2025-12-09) - wf_03_prime.md 集成:
- ✅ **集成完成**: Step 3.5 添加 DocLoader 智能加载逻辑
- ✅ **文件更新**: 1093 → 1198 行（+105行集成代码）
- ✅ **Token节省**:
  - Quick Start 模式: 74% 节省 (766→200 tokens)
  - Full Context 模式: 50% 节省 (2400→1200 tokens)
  - Task Focused 模式: 60% 节省 (1500→600 tokens)
- ✅ **Frontmatter更新**: 添加 doc_loader_integrated 和 token_savings 字段

**阶段2B实现成果** (2025-12-09) - wf_08_review.md 集成:
- ✅ **集成完成**: Step 2.5 添加 DocLoader 智能加载逻辑
- ✅ **文件更新**: 1764 → 1905 行（+141行集成代码）
- ✅ **外部文档创建**: 3个规范文档（692行 → 按需加载）
  - wf_08_review_doc_compliance.md (246行) - Dimension 6 检查清单
  - wf_08_review_self_check.md (270行) - Dimension 7 自检协议
  - wf_08_review_parallel.md (230+行) - Step 2.3 并行审查模式
- ✅ **Token节省**:
  - Quick 模式: 85% 节省 (692→100 tokens)
  - Standard 模式: 55% 节省 (692→310 tokens)
  - Deep 模式: 20% 节省 (692→550 tokens)
- ✅ **Frontmatter更新**: 添加 docs_dependencies 和 token_savings 字段
- ✅ **智能判断**: 3种审查需求自动识别（doc_compliance/self_check/parallel_review）

**预期效果**:
- 阶段1：命令文件10,027 → 5,000行（50%减少）✅ **工具就绪**
- 阶段2A：wf_03_prime.md 集成 ✅ **已完成** (35-40% token 节省)
- 阶段2B：wf_08_review.md 集成 ✅ **已完成** (20-85% token 节省)
- 阶段2C：wf_05_code.md 集成 🟡 **待实施**
- 文档加载：按需章节加载（70%减少）✅ **已实现并集成**
- Token消耗：每命令减少2k-5k tokens ✅ **wf_03_prime 已验证**

**下一步行动**:
1. ~~集成 DocLoader 到 wf_03_prime.md~~（✅ 已完成）
2. ~~集成 DocLoader 到 wf_08_review.md（按需加载规范文档）~~（✅ 已完成）
3. 集成 DocLoader 到 wf_05_code.md（渐进式文档加载）
4. 收集实际使用数据，验证Token节省效果

详见: [docs/adr/2025-12-09-workflow-three-tier-architecture.md](docs/adr/2025-12-09-workflow-three-tier-architecture.md)

### 前次决策亮点 (2025-12-03)

**SuperClaude Framework 借鉴**:
- ✅ PROJECT_INDEX.md 模式（70-80% token节省）
- ✅ PM Agent 模式（ConfidenceChecker, Self-Check, Reflexion）
- ✅ Parallel-First 执行（3.5x 性能提升）
- ✅ Evidence-Based Development（防止基于假设的实现）
- ✅ CLI 工具链（健康检查和MCP管理）

**三个立即优化**:
1. 实现 PROJECT_INDEX.md（30分钟，75% token节省）
2. 集成 Confidence Check（45分钟，25-250x ROI）
3. 添加 Self-Check Protocol（30分钟，94% 幻觉检测率）

详见: [docs/adr/2025-12-03-superclaude-optimization-learnings.md](docs/adr/2025-12-03-superclaude-optimization-learnings.md)

**触发条件**:
- 多个技术选项间的权衡
- 架构有重大改变
- 复杂的重构/优化权衡
- 决策影响多个组件

---

## ❓ 文档生成常见问题

### Q0：wf_11_commit 什么时候使用 pre-commit，什么时候使用自行修复？(NEW - 2025-12-05)

**A**: wf_11_commit 现在会**自动检测并智能选择**执行路径：

**路径 A（推荐）- 使用 pre-commit 框架**：
- ✅ 条件：项目根目录存在 `.pre-commit-config.yaml`
- ✅ 条件：`pre-commit` 工具已安装 (`pip install pre-commit`)
- ✅ 执行：仅运行 `pre-commit run`（staged 文件）
- ⚠️ **禁止**：`pre-commit run --all-files`（避免性能问题）

**路径 B（Fallback）- 自行修复**：
- ⚠️ 条件：无 `.pre-commit-config.yaml` 或 pre-commit 未安装
- ✅ 执行：基础质量修复（尾部空格、行结尾、格式）
- 💡 提示：建议安装 pre-commit 框架升级到路径 A

**为什么禁止 --all-files？**
1. 性能问题：大型代码库会非常慢
2. 意外修改：可能修改未暂存的文件
3. 部分提交冲突：破坏 partial commit 工作流

**如何切换到路径 A？**
```bash
# 创建 .pre-commit-config.yaml（参考模板）
# 安装 pre-commit 工具
pip install pre-commit
pre-commit install

# wf_11_commit 会自动检测并使用路径 A
```

详见: [wf_11_commit.md § Pre-commit Framework Integration](wf_11_commit.md#pre-commit-framework-integration)

---

### Q1：doc_guard.py 提供了 sections 参数但仍报错 (NEW - 2025-12-16)

**症状**:
```
❌ 文档 /path/to/doc.md 有 946 行，超过限制（800行）
  建议: 必须指定 --sections 加载部分章节
```
即使在命令中已经指定了 `--sections` 参数。

**根本原因**:
- 位置: `scripts/doc_guard.py:166-170`
- 问题: 当文档 > 800 行时，代码无条件抛出错误
- 缺陷: **没有检查 sections 参数是否已提供**

**修复方案** (已在源码中修复):
```python
else:  # lines > 800
    if not sections:
        raise DocGuardError(...)  # 只在没有 sections 时报错

    # 如果提供了 sections，则加载指定章节
    strategy = f"章节模式（大文档，{lines}行） {sections}"
    section_dict = self.loader.load_sections(doc_path, sections)
    content = "\n\n".join(section_dict.values())
```

**修复后效果**:
- ✅ 可以正确处理 > 800 行的文档（如 946 行）
- ✅ 正确加载指定的 sections
- ✅ Token 消耗：~345 tokens（仅加载指定章节）

---

### Q2：Agent 协调器导入失败 "No module named 'lib'" (NEW - 2025-12-16)

**症状**:
```python
from lib.agent_coordinator import get_agent_coordinator
ModuleNotFoundError: No module named 'lib'
```

**根本原因**:
- **导入路径错误**（非安装问题）
- 安装目录正确: `~/.claude/commands/commands/lib/agent_coordinator.py` ✅ 存在
- 错误的导入: `from lib.agent_coordinator import ...` ❌
- 正确的导入: `from commands.lib.agent_coordinator import ...` ✅

**修复方案**:
```python
# ❌ 错误的导入
from lib.agent_coordinator import get_agent_coordinator

# ✅ 正确的导入
from commands.lib.agent_coordinator import get_agent_coordinator
```

**验证命令**:
```bash
cd ~/.claude/commands && python3 -c "
from commands.lib.agent_coordinator import get_agent_coordinator
coordinator = get_agent_coordinator()
print('✅ Agent 协调器导入成功！')
"
```

---

### Q3：如何判断某个代码改动是否需要文档？

**A**: 使用决策树判断：
- **改动了公开 API** → 需要（Type C - API文档）
- **改变了现有行为** → 需要（Type A/D - 架构或FAQ）
- **使用了新技术** → 需要（Type B - ADR）
- **改变了系统架构** → 需要（Type A - 规划文档）
- **新增配置选项** → 需要（Type C - 部署文档）
- **代码优化** → 不需要（Type E - 无文档）

**经验法则**：如果下一个维护者需要了解"为什么"和"如何用"，就需要文档。

### Q4：为什么文档有大小约束？

**A**: 约束的三个价值：
1. **成本控制** - 管理人员和上下文消耗
2. **强制简洁** - 短文档更容易维护
3. **可验证性** - 提供自动化检查点

**约束规则**：
- KNOWLEDGE.md < 200 行（纯索引和摘要）
- 单个文件 < 500 行（复杂内容拆分）
- 每 commit 增长 < 30%（避免爆炸）

### Q3：文档生成超过约束怎么办？

**A**: 有三个解决方案：
1. **减少内容** - 删除非关键部分，保留核心
2. **拆分文件** - 大文档分为 2-3 个小文档
3. **清理旧文档** - 运行 `/wf_13_doc_maintain` 清理

### Q4：AI 生成的文档需要人工审查吗？

**A**: **是的**。约束驱动生成提供基础，需要 5-10 分钟的人工审查：
- [ ] 验证技术细节准确性
- [ ] 补充业务背景说明
- [ ] 添加图表或实例
- [ ] 验证代码示例可运行

### Q5：如何填写 Frontmatter 中的 related_documents？

**A**: 只列出真正相关的文档，最多 3-5 个：
```yaml
related_documents:
  - "docs/api/authentication.md"      # 认证机制
  - "docs/adr/2025-11-24-xxx.md"     # 设计决策
  - "KNOWLEDGE.md"                    # 知识库
```

**规则**：
- 使用相对路径（从项目根目录）
- 过多相关说明设计有问题

详见 [Frontmatter 实例集合](docs/examples/frontmatter_examples.md)

---

## 🔧 技术模式参考 (NEW - 2025-12-08)

### 环境和依赖检测模式

**Python 模块可用性检测** (推荐模式 - Task 2.12):
```python
import importlib.util

# 检测模块是否可用
if importlib.util.find_spec("module_name") is not None:
    # 模块可用
    import module_name
else:
    # 使用降级方案
```

**Python 版本检测** (兼容性检查):
```python
import sys

# 十六进制版本比较
if sys.hexversion >= 0x030A00F0:  # Python 3.10+
    # 使用高级特性
else:
    # 使用兼容模式
```

**包版本查询** (依赖验证):
```python
from importlib.metadata import version

try:
    ver = version('package_name')  # '2.22.0'
except ImportError:
    # 包未安装
```

### 测试模式

**条件测试跳过** (Pytest - Task 2.12):
```python
import pytest
import sys

# 基于 Python 版本跳过
@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="requires python3.10 or higher"
)
def test_function(): ...

# 基于环境变量跳过
@pytest.mark.skipif(
    not is_mcp_available("serena"),
    reason="Serena MCP not available"
)
def test_serena_integration(): ...

# 基于平台跳过
@pytest.mark.darwin  # macOS only
def test_macos_specific(): ...
```

**Tox 多环境测试矩阵** (跨版本兼容):
```ini
[tox]
envlist = py{39,310,311}-{with_mcp,no_mcp}

[testenv]
deps =
    pytest
    with_mcp: mcp-servers
commands =
    pytest tests/
```

### 降级和容错模式

**Circuit Breaker 模式** (MCP 故障处理 - Task 2.11):
```python
class MCPCircuitBreaker:
    def __init__(self, threshold=5, timeout=60):
        self.state = "CLOSED"  # CLOSED/OPEN/HALF-OPEN
        self.failure_count = 0
        self.threshold = threshold

    def call_with_fallback(self, mcp_func, fallback_func):
        try:
            if self.state == "CLOSED":
                result = mcp_func()
                self.failure_count = 0
                return result
        except Exception:
            self.failure_count += 1
            if self.failure_count > self.threshold:
                self.state = "OPEN"

        # 使用降级方案
        return fallback_func()
```

**Graceful Degradation 策略** (Task 2.11):
1. **缓存数据降级**: MCP 不可用时使用本地缓存
2. **默认值降级**: 返回安全的默认值而非失败
3. **功能降级**: 提供基础功能，标注高级功能不可用

**相关文档**:
- Task 2.11 文档: deployment_compatibility_guide.md (完整降级场景)
- Task 2.12 脚本: validate_command_compatibility.py (自动检测实现)

**应用场景**:
- 老版本环境部署 (v1.0-v1.6)
- MCP 服务器不可用
- 网络环境受限
- CI/CD 流程中的兼容性测试

**研究来源**: Context7 (Python/pytest 官方文档) + Tavily (graceful degradation 最佳实践)

---

## 🔗 工作流和核心参考

**工作流命令**: `/wf_01_planning` → `/wf_02_task` → `/wf_03_prime` → `/wf_05_code` → `/wf_08_review` → `/wf_11_commit`

**核心参考**:
- [CLAUDE.md](CLAUDE.md) - AI 执行规则
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计思维
- [docs/adr/README.md](docs/adr/README.md) - ADR 指南

---

**最后更新**: 2025-12-08
### 路径管理最佳实践 (NEW - 2025-12-14)

**问题背景**: Doc Guard 工具在多个命令中因路径问题失效，导致强制文档加载步骤失败。

**发现和修复过程**:
- ✅ **根本原因**:
  1. 相对路径 (`docs/guides/...`) 仅适用于特定工作目录
  2. Python 脚本中 `~` 不被展开（bash 特性，Python 字符串不处理）
  3. 命令可能从任意目录调用（安装后位于 `~/.claude/commands/`）
- ✅ **解决方案**: 统一使用 `$HOME/.claude/commands/...` 格式
  - `$HOME` 会被 bash 展开（提供绝对路径）
  - 与安装目录位置保持一致
  - 支持任意工作目录调用

**受影响命令文件 (7个) 和修复结果**:
| 命令文件 | Doc Guard 调用路径修复 | 状态 |
|---------|----------------------|------|
| wf_03_prime.md | `$HOME/.claude/commands/docs/guides/wf_03_prime_workflows.md` | ✅ 已修复 |
| wf_04_ask.md | `$HOME/.claude/commands/docs/guides/wf_04_ask_workflows.md` | ✅ 已修复 |
| wf_05_code.md | `$HOME/.claude/commands/docs/guides/wf_05_code_workflows.md` | ✅ 已修复 |
| wf_06_debug.md | `$HOME/.claude/commands/docs/guides/wf_06_debug_workflows.md` | ✅ 已修复 |
| wf_07_test.md | `$HOME/.claude/commands/docs/guides/wf_07_test_workflows.md` | ✅ 已修复 |
| wf_08_review.md | `$HOME/.claude/commands/docs/guides/wf_08_review_workflows.md` | ✅ 已修复 |
| wf_11_commit.md | `$HOME/.claude/commands/docs/guides/wf_11_commit_workflows.md` | ✅ 已修复 |

**最佳实践模式**:
```bash
# ✅ 正确做法（统一使用 $HOME）
python $HOME/.claude/commands/scripts/doc_guard.py \
  --docs "$HOME/.claude/commands/docs/guides/wf_XX_workflows.md" \
  --sections ...

# ❌ 错误做法（相对路径）
python ~/.claude/commands/scripts/doc_guard.py \
  --docs "docs/guides/wf_XX_workflows.md"  # 仅适用于源码目录
```

**执行影响**:
- ✅ **兼容性**: 支持从任意目录调用 workflow 命令
- ✅ **可靠性**: 消除 "文档不存在" 错误
- ✅ **维护性**: 统一的绝对路径标准
- ✅ **性能**: 避免路径解析失败重试

**学习要点**:
1. **执行上下文**: CLI 命令可能在任意 PWD 执行
2. **参数扩展**: Python 脚本不自动展开 `~`
3. **系统设计**: 路径必须基于安装位置，而非源代码位置

**相关参考**:
- 修复提交: `e622487` - `重新设计 wf_11_commit 命令（Stage 1 准备阶段 + Git Hook 哲学）`
- 实施过程: 全面实施 7 个命令文件的路径修复
- 验证方法: `grep -n "python.*doc_guard" *.md | grep -v "$HOME"`
