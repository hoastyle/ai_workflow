---
command: /wf_04_ask
index: 04
phase: "开发实现"
description: "架构咨询服务，支持技术决策和代码库审查，集成 Ultrathink 设计思维 | MCP: --think | --c7 | --research | --review-codebase"
reads: [PLANNING.md, TASK.md, KNOWLEDGE.md, PHILOSOPHY.md(可选), 代码库(--review-codebase)]
writes: [PLANNING.md(可能), KNOWLEDGE.md(可能), TASK.md(可能), docs/adr/(可能)]
prev_commands: [/wf_03_prime]
next_commands: [/wf_05_code, /wf_01_planning]
model: sonnet
token_budget: medium
ultrathink_lens: "architecture_design"
mcp_support:
  - name: "Sequential-thinking"
    flag: "--think"
    detail: "结构化多步推理分析复杂决策"
  - name: "Context7"
    flag: "--c7"
    detail: "获取官方框架和库的文档及最佳实践"
  - name: "Tavily"
    flag: "--research"
    detail: "搜索最新技术发展和社区讨论"
  - name: "特殊标志"
    flag: "--review-codebase"
    detail: "全面的代码库审查和质量分析"
context_rules:
  - "决策必须对齐PRD需求"
  - "重大架构决策更新PLANNING.md"
  - "新模式添加到KNOWLEDGE.md"
  - "重要决策考虑记录到 docs/adr/ (参见 PHILOSOPHY.md)"
  - "从 Ultrathink 角度深度分析（6原则：Think Different, Obsess Over Details 等）"
---

## 🔌 MCP 增强能力

本命令支持以下 MCP 服务器的可选增强：

### Sequential-thinking (结构化思考)

**启用**: `--think` 标志
**用途**: 复杂架构决策时使用结构化多步推理
**自动激活**: 检测到复杂决策关键词

**示例**:
```bash
# 启用深度思考
/wf_04_ask "选择 Web 框架" --think

# 组合启用
/wf_04_ask "..." --think --c7 --research
```

**改进点**:
- 问题分解为清晰的步骤
- 逐步分析每个选项
- 权衡明确和可追踪
- 建议基于结构化分析

---

### Context7 (官方文档)

**启用**: `--c7` 标志或自动检测
**用途**: 获取官方框架和库的文档、API 参考、最佳实践
**自动激活**: 检测到框架/库名

**示例**:
```bash
# 明确启用
/wf_04_ask "如何在 React 中实现路由？" --c7

# 自动启用 (检测到 React)
/wf_04_ask "React vs Vue，哪个更好？"
```

**改进点**:
- 官方文档链接
- 官方推荐的最佳实践
- API 参考
- 版本兼容性信息

---

### Tavily (Web 搜索)

**启用**: `--research` 标志
**用途**: 搜索最新的技术发展、社区讨论、性能对比
**自动激活**: 否 (用户明确启用)

**示例**:
```bash
/wf_04_ask "Rust vs Go for 2024" --research
```

**改进点**:
- 最新的社区讨论
- GitHub 趋势数据
- 性能对比报告
- 新版本发布信息

---

### 组合使用

```bash
# 全面的架构决策分析
/wf_04_ask "选择微服务框架" --think --c7 --research

# 输出包含:
# 1. 多步骤结构化分析 (Sequential-thinking)
# 2. 官方文档和最佳实践 (Context7)
# 3. 最新社区反馈 (Tavily)
# 4. 综合建议
```

---

### 禁用 MCP

```bash
# 使用纯文本分析，不启用任何 MCP
/wf_04_ask "..." --no-mcp
```

---

### 🔧 MCP Gateway 集成

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Sequential-thinking 工具调用** (--think):
```python
# 检查可用性
if gateway.is_available("sequential-thinking"):
    # 获取工具
    think_tool = gateway.get_tool("sequential-thinking", "sequentialthinking")

    # 调用工具进行结构化思考
    result = think_tool.call(
        thought="分析架构决策的第一步...",
        thoughtNumber=1,
        totalThoughts=5,
        nextThoughtNeeded=True
    )
else:
    print("⚠️ Sequential-thinking 不可用，使用标准分析")
```

**Context7 工具调用** (--c7):
```python
# 检查可用性
if gateway.is_available("context7"):
    # Step 1: 解析库名到库 ID
    resolve_tool = gateway.get_tool("context7", "resolve-library-id")
    library_id_result = resolve_tool.call(libraryName="react")

    # Step 2: 获取官方文档
    docs_tool = gateway.get_tool("context7", "get-library-docs")
    docs = docs_tool.call(
        context7CompatibleLibraryID=library_id_result["library_id"],
        mode="code",  # or "info"
        topic="routing"
    )
else:
    print("⚠️ Context7 不可用，使用通用知识库")
```

**Tavily 工具调用** (--research):
```python
# 检查可用性
if gateway.is_available("tavily"):
    # 获取搜索工具
    search_tool = gateway.get_tool("tavily", "tavily-search")

    # 执行 Web 搜索
    results = search_tool.call(
        query="Rust vs Go for backend services 2025",
        search_depth="advanced",
        max_results=10,
        include_images=False
    )
else:
    print("⚠️ Tavily 不可用，使用有限的知识库")
```

**组合使用示例** (--think --c7 --research):
```python
# 初始化 Gateway
gateway = get_mcp_gateway()

# 检查所有 MCP 可用性
mcp_status = {
    "think": gateway.is_available("sequential-thinking"),
    "c7": gateway.is_available("context7"),
    "research": gateway.is_available("tavily")
}

# 根据可用性组合使用
if mcp_status["think"]:
    # Step 1: 结构化分解问题
    think_tool = gateway.get_tool("sequential-thinking", "sequentialthinking")
    # ...

if mcp_status["c7"]:
    # Step 2: 获取官方文档
    docs_tool = gateway.get_tool("context7", "get-library-docs")
    # ...

if mcp_status["research"]:
    # Step 3: Web 搜索最新信息
    search_tool = gateway.get_tool("tavily", "tavily-search")
    # ...
```

**Gateway 优势**:
- ✅ 统一的 MCP 管理接口
- ✅ 自动降级（MCP 不可用时回退到标准分析）
- ✅ 连接池复用（减少多次启动开销）
- ✅ 工具懒加载（按需初始化）

---

## 执行上下文
**输入**: 技术问题 + PLANNING.md架构 + KNOWLEDGE.md经验
**输出**: 架构建议 + 可能的PLANNING.md/KNOWLEDGE.md更新
**依赖链**: /wf_03_prime → **当前（架构咨询）** → /wf_05_code

## Usage
`/wf_04_ask <TECHNICAL_QUESTION> [--review-codebase]`

## Context
- Technical question or challenge: $ARGUMENTS
- PLANNING.md provides system architecture context
- TASK.md shows current development state
- Decisions should align with project guidelines
- Use `--review-codebase` flag for comprehensive codebase analysis before answering

## Your Role
You are a Senior Systems Architect providing consultation within project context:
1. **Systems Designer** – evaluates within existing architecture
2. **Technology Strategist** – recommends aligned with tech stack
3. **Scalability Consultant** – considers project performance targets
4. **Risk Analyst** – identifies impacts on current implementation
5. **Code Reviewer** – (when --review-codebase) performs comprehensive codebase analysis

## Process

⚠️ **AI执行强制规则**: 本命令的执行必须严格遵循以下步骤，不得跳过或随意解释。

### Step 0: 读取执行指南（强制）

**AI必须首先执行此步骤**，读取详细的执行流程文档：

```bash
# 强制执行 - 读取工作流指南的关键章节
python ~/.claude/commands/scripts/doc_guard.py \
  --docs "docs/guides/wf_04_ask_workflows.md" \
  --sections '{"docs/guides/wf_04_ask_workflows.md": ["AI执行协议", "MCP模式选择决策树", "咨询类型决策树", "后续路径决策树"]}'
```

**如果Doc Guard工具不可用**，降级使用Read工具读取完整文档（警告：token消耗会增加）

---

### Step 0.1: Agent 选择和激活 🤖

**目的**: 自动选择合适的 agent 协助咨询，提升架构决策的深度和专业性

**执行时机**: 在读取执行指南之后、开始咨询之前

**Agent 协调流程**:

```python
from commands.lib.agent_coordinator import get_agent_coordinator

# 1. 初始化协调器（单例模式）
coordinator = get_agent_coordinator()

# 2. 拦截命令执行，选择 agent
agent_context = coordinator.intercept(
    task_description=user_question,  # 用户提供的技术问题
    command_name="wf_04_ask",
    auto_activate=True,      # 自动激活高匹配度 agent
    min_confidence=0.85      # 最低置信度阈值（85%）
)

# 3. 显示 agent 信息
print(coordinator.format_agent_info(agent_context, verbose=True))
```

**输出示例**:
```markdown
## 🤖 Agent 协助

**使用 Agent**: Software Architect (`architect-agent`)
**匹配度**: 96% 🟢 自动激活
**专长**: 系统架构设计, 技术选型和评估, 微服务和分布式系统

**MCP 工具**:
  - Sequential-thinking: 复杂架构决策的结构化推理
  - Context7: 查询最新技术文档和最佳实践
  - Tavily: 社区方案和开源项目研究

**建议协作**:
  - sequential: code-agent (设计后实现)
  - sequential: review-agent (架构审查)
```

**Agent 上下文使用**:

如果 agent 成功激活，后续步骤应参考其建议：

```python
if agent_context['auto_activated']:
    agent = agent_context['agent']

    # 1. 参考 agent 的咨询重点
    expertise = agent.expertise
    # 例如: ["系统架构设计", "技术选型和评估", ...]

    # 2. 调整咨询深度和方向
    # architect-agent 可能建议重点关注架构模式和扩展性

    # 3. 使用 MCP 工具增强咨询
    mcp_hints = agent_context['mcp_hints']
    # 例如: 使用 Context7 查询最新技术文档
```

**降级处理**:

如果未匹配到合适的 agent (匹配度 < 85%)：
- ℹ️ 显示: "未匹配到合适的 agent，使用标准咨询流程"
- 继续执行后续步骤，不影响命令功能

**相关文档**: [AgentCoordinator 使用指南](docs/examples/agent_coordinator_usage.md)

---

### Step 1-N: 按指南执行

**详细执行流程**: 所有步骤必须严格遵循 [wf_04_ask 工作流指南](docs/guides/wf_04_ask_workflows.md) 中的"AI执行协议"部分

**快速参考**（仅供理解，不得作为执行依据）:

**六种执行模式**:
1. **标准咨询模式**: 无MCP标志，基于项目上下文
2. **结构化推理模式 (--think)**: Sequential-thinking MCP
3. **官方文档模式 (--c7)**: Context7 MCP
4. **社区研究模式 (--research)**: Tavily MCP
5. **代码审查模式 (--review-codebase)**: 代码库分析
6. **综合分析模式**: 组合多个MCP标志

**三个关键决策点**:
1. **MCP模式选择**: 根据问题类型和用户标志（标准/--think/--c7/--research/--review-codebase/组合）
2. **咨询类型识别**: 技术选型/架构设计/实现方案/代码质量
3. **后续路径选择**: 直接实现/更新规划/深度研究/修复问题

**所有详细规范**: 必须参照 [工作流指南](docs/guides/wf_04_ask_workflows.md)

### 执行检查清单（AI必须验证）

在输出结果前，AI必须确认以下所有项目：

- [ ] ✅ 已读取 docs/guides/wf_04_ask_workflows.md
- [ ] ✅ 已完成 Confidence Check 并输出评估结果
- [ ] ✅ 已根据决策树选择MCP模式并说明理由
- [ ] ✅ 已加载项目上下文（PLANNING.md, KNOWLEDGE.md）
- [ ] ✅ 如果是技术选型，已完成开源方案调研（3+个候选方案）
- [ ] ✅ 输出格式完全符合对应场景的标准模板
- [ ] ✅ 已根据后续路径决策树选择并说明下一步
- [ ] ✅ 已添加明确的后续命令和替代选项
- [ ] ✅ 遵循CLAUDE.md语言规范

**如果任何检查项未通过，必须重新执行对应步骤**

### 故障排除

| 问题 | 解决方案 |
|------|--------------|
| PLANNING.md不存在 | 提示运行 `/wf_01_planning` 建立项目规划 |
| KNOWLEDGE.md中无类似决策 | 标注为新决策，建议记录到ADR |
| 问题表述不清楚 | Confidence Check 低于70%，暂停并询问 |
| MCP工具不可用 | 自动降级到标准咨询模式，警告功能受限 |
| 无法找到开源方案 | 说明研究不足，建议使用 /wf_04_research 深度调研 |
| 代码库审查失败 | 检查项目结构，提供基本建议 |

---

### Step 0.2: Confidence Check (Pre-Execution Assessment) 🎯

**目的**: 在开始架构咨询前评估信心水平，避免盲目推进导致错误方向

**执行时机**: 在 Agent 选择之后、读取项目文档之前执行

**评估维度**:

1. **问题清晰度** (Problem Clarity)
   - ✅ 问题表述清晰，目标明确 (+30%)
   - ⚠️ 问题模糊，需要澄清 (-20%)
   - ❌ 问题不完整，缺少关键信息 (-40%)

2. **现有知识** (Existing Knowledge)
   - ✅ 对问题领域有官方文档支持 (+20%)
   - ✅ KNOWLEDGE.md 有类似决策记录 (+15%)
   - ⚠️ 需要研究但有明确方向 (+5%)
   - ❌ 完全未知领域 (-30%)

3. **项目对齐** (Project Alignment)
   - ✅ 符合 PLANNING.md 架构方向 (+20%)
   - ✅ 有现有技术栈支持 (+10%)
   - ⚠️ 需要引入新技术 (-10%)
   - ❌ 与现有架构冲突 (-20%)

4. **可验证性** (Verifiability)
   - ✅ 有官方文档可验证 (+15%)
   - ✅ 有开源实现可参考 (+10%)
   - ⚠️ 需要实验验证 (+0%)
   - ❌ 无法验证，只能猜测 (-30%)

5. **复杂度评估** (Complexity)
   - ✅ 简单问题，明确答案 (+10%)
   - ⚠️ 中等复杂，需要权衡 (-5%)
   - ❌ 高度复杂，多方依赖 (-15%)

**信心水平计算**:
```
基础信心: 50%
最终信心 = 基础信心 + Σ(各维度分数)
```

**决策树**:

```
信心水平 ≥ 90%?
├─ YES → 🟢 直接执行咨询流程
│         理由: 高信心，风险低，ROI 高
│
├─ 70% ≤ 信心 < 90%?
│  └─ YES → 🟡 提供备选方案
│            - 主要建议 (基于当前知识)
│            - 替代方案 (如果主要建议失败)
│            - 建议: "考虑使用 --c7 获取官方文档" 或 "--research 搜索最新实践"
│
└─ 信心 < 70%?
   └─ YES → 🔴 暂停并询问
            - 停止猜测
            - 列出需要澄清的问题
            - 建议用户提供更多上下文
            - 或建议: "先运行 /wf_04_research 深度研究该领域"
```

**示例 1: 高信心场景 (95%)**
```
问题: "如何在 React 中实现客户端路由？"
评估:
- 问题清晰: +30% (明确目标)
- 官方文档支持: +20% (React Router 官方文档)
- 项目对齐: +20% (PLANNING.md 使用 React)
- 可验证: +15% (官方文档 + 开源示例)
- 复杂度: +10% (标准实现)
总信心: 50% + 95% = 145% → Cap at 95%

→ 🟢 直接执行，提供官方推荐方案
```

**示例 2: 中等信心场景 (75%)**
```
问题: "如何优化数据库查询性能？"
评估:
- 问题清晰: +30%
- 现有知识: +5% (需要查看具体查询)
- 项目对齐: +10% (现有数据库)
- 可验证: +10% (需要性能测试)
- 复杂度: -5% (需要权衡)
总信心: 50% + 50% = 100% → 调整为 75%

→ 🟡 提供主要建议 + 备选方案
   主要: 索引优化
   备选: 查询重写、缓存策略
   建议: 使用 /wf_10_optimize 进行性能分析
```

**示例 3: 低信心场景 (40%)**
```
问题: "应该选择哪个 AI 模型？"
评估:
- 问题清晰: -20% (缺少使用场景)
- 现有知识: -30% (未知领域)
- 项目对齐: -10% (需引入新技术)
- 可验证: +0% (需实验)
- 复杂度: -15% (高度复杂)
总信心: 50% - 75% = -25% → 底线 40%

→ 🔴 暂停并询问
   需要澄清:
   1. 使用场景和目标是什么？
   2. 数据类型和规模？
   3. 性能和成本预算？
   4. 部署环境限制？
   建议: 先运行 /wf_04_research "AI 模型选型" --research
```

**ROI 分析**:
```
Confidence Check 成本: ~100-200 tokens
节省成本 (如果避免错误方向):
  - 避免错误实现: 5,000-10,000 tokens
  - 避免返工: 20,000-50,000 tokens
  - 避免架构返工: 50,000+ tokens

ROI: 25-250x token 节省
Break-even: 只需避免 1 次错误方向
```

**输出格式**:
```
## 🎯 Confidence Assessment

**信心水平**: 85% 🟡

**评估明细**:
- ✅ 问题清晰度: +30%
- ✅ 官方文档支持: +20%
- ✅ 项目对齐: +20%
- ✅ 可验证: +15%
- ⚠️ 复杂度: -5%

**决策**: 提供主要建议 + 备选方案

**建议**: 考虑使用 --c7 获取 React Router 官方最佳实践
```

---

### Step 1: Standard Consultation (default)

**加载项目上下文（使用 Doc Guard）**:
```bash
python ~/.claude/commands/scripts/doc_guard.py --docs "docs/management/PLANNING.md,KNOWLEDGE.md"
```

1. **Context Integration**:
   - Review relevant PLANNING.md sections
   - Consider current TASK.md progress
   - Consult KNOWLEDGE.md for past architectural decisions and patterns
   - Understand project constraints and technology stack

2. **开源方案调研** (NEW - 优先级优化):
   - [必须] 列举市面上的 3+ 个相关开源项目/库
   - [必须] 分析各方案的优缺点（功能、性能、社区活跃度、License 兼容性）
   - [必须] 评估集成成本 vs 自己实现的成本
   - [可选] 搜索已有的对标产品或参考实现
   - [可选] 查阅 KNOWLEDGE.md 中的类似决策历史
   - **输出**: 候选方案对比表 + 推荐理由
   - **原则**: 优先开源成熟方案，除非有特殊理由自己实现

3. **Expert Consultation**:
   - Systems Designer: Analyze within system boundaries
   - Technology Strategist: Align with chosen stack
   - Scalability Consultant: Match performance requirements
   - Risk Analyst: Assess project-specific risks
   - **新增**: OpenSource Strategist - 评估开源方案的长期可维护性

4. **Solution Synthesis**:
   - Provide guidance consistent with project
   - Prefer proven open-source solutions when applicable
   - Update PLANNING.md if decisions made (including tech stack choices)
   - Document significant architectural decisions for KNOWLEDGE.md
   - Identify new tasks for TASK.md (如果需要集成某个库)
   - Create/update ADR if making important tech choices

### Comprehensive Codebase Review (--review-codebase flag)
1. **Discovery Phase**:
   - Scan project structure (README, package.json, configuration files)
   - Identify entry points (main application files, API endpoints)
   - Check dependencies (outdated packages, security advisories)
   - Review recent changes (git history, pull requests)

2. **Deep Analysis**:
   - **Security audit**: Authentication, authorization, input validation
   - **Performance analysis**: Database queries, algorithmic complexity, memory usage
   - **Code quality assessment**: Complexity metrics, duplication, maintainability
   - **Testing evaluation**: Coverage, test quality, missing scenarios
   - **Architecture review**: Component structure, design patterns, scalability

3. **Issue Classification**:
   - **🔴 Critical Priority**: Security vulnerabilities, data corruption risks, breaking bugs
   - **🟠 High Priority**: Architectural problems, significant code quality issues, missing error handling
   - **🟡 Medium Priority**: Minor bugs, style inconsistencies, missing tests, documentation gaps
   - **🟢 Low Priority**: Code cleanup, refactoring opportunities, minor optimizations

4. **Technology-Specific Analysis**:
   - **Frontend**: Component lifecycle, state management, performance, accessibility
   - **Backend**: API design, database optimization, caching, security middleware
   - **Database**: Query performance, indexing, data integrity constraints

5. **TASK.md Integration**:
   - Check existing tasks to avoid duplication
   - Create categorized, actionable tasks with specific solutions
   - Include impact assessment and estimated effort
   - Follow priority-based task format with clear labels

## Output Format

### Standard Consultation Output (Without MCP)
1. **Contextual Analysis** – question within project scope
2. **开源方案评估** (NEW) – candidate solutions with pros/cons:
   - 候选方案 1: XXX (优势/劣势/License)
   - 候选方案 2: YYY (优势/劣势/License)
   - 候选方案 3: ZZZ (优势/劣势/License)
   - **推荐**: 理由 (功能完整性、社区活跃度、集成成本、长期维护)
   - **风险**: 潜在问题（版本升级、破坏性变更、社区衰退等）
3. **Knowledge Base Review** – relevant past decisions from KNOWLEDGE.md (包括历史技术选型)
4. **Recommendations** – solutions aligned with architecture (优先推荐开源方案)
5. **Decision Impact** – effects on current implementation
6. **Architecture Documentation** – ADR entries for KNOWLEDGE.md if significant
7. **Documentation Updates** – PLANNING.md amendments needed (including tech stack section)
8. **Task Generation** – new TASK.md items if required (库集成、PoC 验证等)
9. **💡 Ultrathink 视角** (可选提醒) – 从设计哲学角度深度分析（参见 PHILOSOPHY.md）
   - 是否质疑了所有假设？(Think Different) → 是否考虑了开源方案？
   - 方案的优雅度如何？(Craft, Don't Code) → 使用成熟库 > 自己实现
   - 有没有更简洁的设计？(Simplify Ruthlessly) → 减少依赖数量，择优而用
   - 这个权衡是否明确？(值得记录到 docs/adr/ 吗？)

### Enhanced Output with --think (Sequential-thinking)
**Additional sections when using `--think` flag**:

1. **Problem Decomposition** – break down the decision into clear steps:
   - Step 1: Understanding the requirement
   - Step 2: Identifying constraints
   - Step 3: Listing evaluation criteria
   - Step 4: Analyzing each option systematically

2. **Option Analysis** – systematic evaluation of each candidate:
   - Option A: Detailed analysis with scoring
   - Option B: Detailed analysis with scoring
   - Option C: Detailed analysis with scoring

3. **Trade-off Analysis** – explicit pros/cons comparison:
   - Performance vs Complexity
   - Learning curve vs Long-term maintainability
   - Community support vs Feature completeness
   - License implications

4. **Structured Recommendation** – based on step-by-step analysis with clear reasoning chain

### Enhanced Output with --c7 (Context7)
**Additional sections when using `--c7` flag**:

1. **Official Documentation** – links and references:
   - Official docs URLs for each candidate solution
   - API reference documentation
   - Official tutorials and guides

2. **Best Practices** – from official sources:
   - Recommended patterns from official docs
   - Common pitfalls to avoid
   - Configuration best practices

3. **API Reference** – key technical details:
   - Core API methods and usage
   - Integration points
   - Configuration options

4. **Version Information** – compatibility notes:
   - Current stable version
   - Breaking changes in recent versions
   - Compatibility matrix
   - Upgrade path considerations

### Enhanced Output with --research (Tavily)
**Additional sections when using `--research` flag**:

1. **Community Feedback** – what developers are saying:
   - Stack Overflow discussions
   - Reddit developer opinions
   - Blog post analyses

2. **Performance Data** – latest benchmarks:
   - Performance comparison charts
   - Real-world benchmark results
   - Scalability reports

3. **Adoption Trends** – GitHub and ecosystem stats:
   - GitHub stars and growth trends
   - NPM download statistics
   - Active contributor counts
   - Community activity metrics

4. **Recent Updates** – new versions and changes:
   - Latest release information
   - Breaking changes and migration guides
   - Roadmap and future plans
   - Security advisories

### Combined Output (--think --c7 --research)
When all three MCP services are enabled, the output provides:
- **Comprehensive analysis** combining structured reasoning, official docs, and real-world data
- **Multi-dimensional evaluation** from theory to practice
- **High-confidence recommendations** backed by multiple authoritative sources
- **Complete decision documentation** suitable for ADR records

### Codebase Review Output (--review-codebase)
1. **Review Summary**:
   - Codebase overview and technologies
   - Review scope and limitations
   - Overall health assessment

2. **Key Findings**:
   - Critical issues count and descriptions
   - Major patterns and architectural concerns
   - Positive aspects and good practices observed

3. **Recommendations**:
   - Immediate actions for critical fixes
   - Medium-term architectural improvements
   - Long-term technical debt planning

4. **Updated TASK.md**:
   - Complete updated TASK.md with prioritized tasks
   - Each task includes impact, solution, and effort estimate
   - Tasks categorized by priority with clear labels

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[项目启动] → [任务规划] → [加载上下文] → [架构咨询 ← 当前] → [代码实现] → [测试验证] → [代码审查] → [提交保存]
  STEP 0       STEP 0.5        STEP 1            STEP 2                STEP 3       STEP 4       STEP 5      STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_04_ask` 前，应该已经完成：

1. ✅ **项目启动** (STEP 0) - 项目规划已完成 (`/wf_01_planning`)
2. ✅ **任务规划** (STEP 0.5) - 任务列表已生成 (`/wf_02_task`)
3. ✅ **加载上下文** (STEP 1) - 项目上下文已加载 (`/wf_03_prime`)

### 📝 当前步骤

**正在执行**: `/wf_04_ask <TECHNICAL_QUESTION> [--review-codebase]` (架构咨询)

**这个命令的职责**：
- 提供技术架构咨询（对齐项目规划和需求）
- 评估开源方案和技术选型
- 支持全面的代码库审查（使用 `--review-codebase` 标志）
- 识别技术风险和改进机会
- 更新项目文档（PLANNING.md, KNOWLEDGE.md, TASK.md）
- 记录重要决策到架构决策记录（ADR）

### ⏭️ 建议下一步

**架构咨询完成后**，根据咨询结果选择下一步：

#### 路径 1️⃣：直接进入代码实现 ✅
```bash
# 当前: 架构咨询完成，决策明确
# 下一步: 开始功能实现

/wf_05_code "实现已决策的功能"

# 后续: 测试和审查
/wf_07_test "编写测试验证"
/wf_08_review "代码审查"
/wf_11_commit "提交代码"
```
**适用场景**: 咨询已解决问题，可以立即开始编码，无需进一步讨论

#### 路径 2.：需要更新规划和设计 📐
```bash
# 当前: 架构咨询揭示需要规划调整
# 下一步: 更新项目规划

/wf_01_planning "根据咨询结果更新架构和技术栈"

# 然后: 重新加载上下文
/wf_03_prime

# 最后: 开始实现
/wf_05_code "实现更新后的功能"
```
**适用场景**: 咨询建议对现有规划进行调整，需要重新对齐项目架构

#### 路径 3️⃣：进行深度研究和对比 🔬
```bash
# 当前: 需要对多个技术方案进行深度评估
# 下一步: 执行深度研究

/wf_04_research "深度研究并对比技术方案"

# 然后: 回到咨询
/wf_04_ask "根据研究结果进行最终决策"

# 最后: 更新规划并实现
/wf_01_planning "更新基于研究的决策"
/wf_05_code "开始实现"
```
**适用场景**: 面对重大技术决策，需要系统化评估多个方案

#### 路径 4️⃣：发现代码质量问题 🐛
```bash
# 当前: 代码库审查发现问题
# 下一步: 根据优先级修复

# 如果发现 bug
/wf_06_debug "修复发现的 bug"

# 如果需要重构
/wf_09_refactor "根据建议进行代码重构"

# 完成后
/wf_07_test "测试验证修改"
/wf_11_commit "提交修复"
```
**适用场景**: 使用 `--review-codebase` 进行代码审查时发现问题

### 📊 工作流进度提示

当你完成架构咨询时，确保输出中包含：

✅ 已完成:
- 问题的清晰分析（在项目上下文中）
- 开源方案的对比评估（3+个候选方案）
- 技术决策的推荐理由
- 风险和限制说明
- 后续行动清单

⏭️ 下一步提示:
- 建议执行的路径（4个选项之一）
- 是否需要更新 PLANNING.md
- 是否需要创建或更新 ADR
- 是否需要添加新任务到 TASK.md

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 咨询已解决问题，可直接编码 | 路径 1 | /wf_05_code → /wf_07_test → /wf_08_review → /wf_11_commit |
| 咨询建议更新项目规划和架构 | 路径 2 | /wf_01_planning → /wf_03_prime → /wf_05_code |
| 面对重大技术决策需要深度研究 | 路径 3 | /wf_04_research → /wf_04_ask → /wf_01_planning → /wf_05_code |
| 代码库审查发现 bug 或质量问题 | 路径 4 | /wf_06_debug 或 /wf_09_refactor → /wf_07_test → /wf_11_commit |
| 需要记录重大技术决策 | 特殊 | 创建或更新 ADR 到 docs/adr/ |
| 不确定应该选择哪个方案 | 建议 | 使用 /wf_04_research 进行更系统的评估 |

**何时使用 --review-codebase 标志？**
- 需要全面分析代码库现状
- 想要识别代码质量问题和技术债务
- 需要为代码重构或优化生成任务清单
- 定期的代码健康检查

---

## Workflow Integration
- Consults PLANNING.md for context
- May trigger PLANNING.md updates
- Can generate new tasks in TASK.md
- Informs `/wf_05_code` implementation
- Documents decisions for future `/wf_03_prime`
