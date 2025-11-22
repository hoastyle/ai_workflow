---
command: /wf_04_ask
index: 04
phase: "开发实现"
description: "架构咨询服务，支持技术决策和代码库审查，集成 Ultrathink 设计思维"
reads: [PLANNING.md, TASK.md, KNOWLEDGE.md, PHILOSOPHY.md(可选), 代码库(--review-codebase)]
writes: [PLANNING.md(可能), KNOWLEDGE.md(可能), TASK.md(可能), docs/adr/(可能)]
prev_commands: [/wf_03_prime]
next_commands: [/wf_05_code, /wf_01_planning]
ultrathink_lens: "architecture_design"
model: sonnet
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

### Standard Consultation (default)
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
