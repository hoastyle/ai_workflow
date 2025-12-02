---
command: /wf_01_planning
index: 01
phase: "基础设施"
description: "创建/更新项目规划文档，建立架构和开发标准"
reads: [PRD.md, 现有PLANNING.md, 项目代码结构]
writes: [PLANNING.md]
prev_commands: []
next_commands: [/wf_02_task]
model: sonnet
token_budget: complex
context_rules:
  - "PRD.md是只读的，绝不修改"
  - "PLANNING.md必须对齐PRD.md所有需求"
  - "这是项目架构的权威文档"
---

## 执行上下文
**输入**: PRD.md需求 + 现有项目结构分析
**输出**: PLANNING.md (项目架构和开发标准)
**依赖链**: **当前（项目启动）** → /wf_02_task (任务规划)

## Usage
`/wf_01_planning <PROJECT_NAME>`

## Purpose
Create or update PLANNING.md to establish comprehensive project documentation that:
- Defines project architecture and technical decisions
- Documents development workflow and standards
- Provides context for AI assistants and developers
- Maintains project continuity across sessions

## Process
1. **Requirements Analysis**:
   - Read PRD.md for official project requirements (read-only, never modify)
   - Check for existing PLANNING.md
   - Analyze project structure and codebase
   - Identify technology stack and frameworks
   - Review existing documentation
   - Ensure all PRD requirements are addressed in planning

2. **Document Structure Creation**:
   ### Project Overview
   - Purpose and goals (derived from PRD.md)
   - Target audience/users (per PRD requirements)
   - Key features and functionality (aligned with PRD)
   - Success criteria (mapped from PRD objectives)
   - PRD compliance checklist

   ### Architecture
   - System design and patterns
   - Core components and modules
   - Data models and storage
   - External integrations
   - Technology decisions (What, not Why)
     * 📋 List current technology choices
     * 🔗 Architecture decision rationale → See ADR
     * ❌ DO NOT duplicate decision background and trade-offs here

   ### Technology Stack
   - Programming languages and versions
   - Frameworks and libraries
   - Database and storage systems
   - Development and deployment tools
   - Third-party services

   **Architecture Decision Records (ADR)**:
   - Detailed "Why" → See KNOWLEDGE.md § ADR
   - Major technical choices → Create ADR: docs/adr/YYYY-MM-DD-title.md
   - PLANNING.md records "What it is", NOT "Why we chose it"
   - Example reference format:
     ```markdown
     ## Technology Stack
     - Frontend: React 18
     - Backend: Node.js + Express
     - Database: PostgreSQL

     **Architecture Decisions**: See following ADRs
     - [Why React?](docs/adr/2025-01-01-choose-react.md)
     - [Why PostgreSQL?](docs/adr/2025-01-02-choose-postgresql.md)
     ```

   ### Development Workflow
   - Setup instructions
   - Build commands
   - Test execution
   - Deployment process
   - Git workflow

   ### Code Standards
   - Naming conventions
   - File organization
   - Code style guidelines
   - Documentation requirements
   - Review process

   ### Testing Strategy
   - Unit test approach
   - Integration testing
   - E2E testing (if applicable)
   - Coverage requirements
   - Test data management

   ### Security Guidelines
   - Authentication approach
   - Authorization patterns
   - Data protection measures
   - Security best practices
   - Vulnerability management

   ### Performance Targets
   - Response time requirements
   - Throughput expectations
   - Resource constraints
   - Optimization priorities
   - Monitoring approach

   ### Documentation Architecture (NEW)
   - Four-layer documentation structure (Management/Technical/Working/Archive)
   - Document organization principles (see DOC_ARCHITECTURE.md)
   - AI context optimization strategy (on-demand loading)
   - Document lifecycle and maintenance schedule
   - KNOWLEDGE.md as documentation index center

3. **Documentation Architecture Setup**:
   - Create initial docs/ directory structure (architecture, api, database, deployment)
   - Initialize KNOWLEDGE.md with documentation index template
   - Explain four-layer architecture to user (refer to DOC_ARCHITECTURE.md)
   - Set up document organization rules in PLANNING.md

4. **Interactive Refinement**:
   - Mark sections as TBD initially
   - Collaborate with user to fill details
   - Validate technical decisions
   - Ensure completeness and accuracy

5. **Integration Setup**:
   - Link with TASK.md creation
   - Establish update procedures
   - Define review cycles
   - Initialize KNOWLEDGE.md documentation index

## Output Format
1. **PLANNING.md File** - Complete project planning document
2. **Summary Report** - Key decisions and action items
3. **Next Steps** - Immediate tasks based on planning
4. **Integration Guide** - How to use with other workflow commands

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[项目启动 ← 当前] → [任务规划] → [加载上下文] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [提交保存]
   STEP 0            STEP 0.5       STEP 1          STEP 2       STEP 3       STEP 4       STEP 5      STEP 6
```

### ✅ 已完成的步骤

这是新项目的起点，通常没有前置步骤。如果是更新现有规划：

1. ✅ **加载上下文**（可选，`/wf_03_prime`）
   - 如果这是现有项目，先加载上下文

### 📝 当前步骤

**正在执行**: `/wf_01_planning "<项目描述>"`

- 分析需求和项目结构
- 制定技术规划和架构
- 定义开发标准和流程
- 建立 PLANNING.md 作为权威参考

### ⏭️ 建议下一步

**规划完成后**，建议按以下顺序执行：

#### 路径 1：新项目启动（推荐）✅
```bash
# 第 0.5 步: 创建任务追踪
/wf_02_task create "项目任务初始化"

# 第 1 步: 加载上下文
/wf_03_prime

# 第 2 步: 架构咨询（可选，如需要验证）
/wf_04_ask "这个架构设计是否合理？"

# 第 3 步: 开始编码实现
/wf_05_code "实现第一个功能"
```

#### 路径 2：更新现有规划
```bash
# 更新规划后
/wf_03_prime

# 继续当前工作
/wf_05_code "继续实现"
```

### 📊 工作流进度提示

当你完成规划时，确保输出中包含：

✅ 已完成:
- PLANNING.md 已生成或更新
- 架构清晰且符合 PRD 需求
- 开发标准已定义

⏭️ 下一步提示:
- 推荐执行 `/wf_02_task create` 初始化任务
- 如果是现有项目，建议先运行 `/wf_03_prime`

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 全新项目启动 | 路径 1 | /wf_02_task → /wf_03_prime → /wf_04_ask (可选) → /wf_05_code |
| 更新项目规划 | 路径 2 | /wf_03_prime → /wf_05_code |
| 需要验证设计 | 咨询 | /wf_04_ask "设计是否合理？" |

## Workflow Integration
- Creates foundation for `/wf_02_task`
- Referenced by `/wf_03_prime` for context loading
- Updated through `/wf_08_review` cycles
- Drives `/wf_05_code` implementation standards