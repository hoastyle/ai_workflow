---
command: /wf_04_ask
index: 04
phase: "开发实现"
description: "架构咨询服务，支持技术决策和代码库审查，集成 Ultrathink 设计思维"
reads: [PLANNING.md, TASK.md, KNOWLEDGE.md, PHILOSOPHY.md(可选), 代码库(--review-codebase)]
writes: [PLANNING.md(可能), KNOWLEDGE.md(可能), TASK.md(可能), docs/adr/(可能)]
prev_commands: [/wf_03_prime]
next_commands: [/wf_05_code, /wf_01_planning]
ultrathink_enabled: true
context_rules:
  - "决策必须对齐PRD需求"
  - "重大架构决策更新PLANNING.md"
  - "新模式添加到KNOWLEDGE.md"
  - "重要决策考虑记录到 docs/adr/ (参见 PHILOSOPHY.md)"
  - "可选：从 Ultrathink 角度深度分析（6原则：Think Different, Obsess Over Details 等）"
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

### Standard Consultation Output
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

#### 路径 2️⃣：需要更新规划和设计 📐
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