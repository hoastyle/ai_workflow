---
command: /wf_02_task
index: 02
phase: "基础设施"
description: "管理任务追踪系统，支持创建、更新和审查模式"
model: haiku
reads: [PLANNING.md, TASK.md]
writes: [TASK.md]
prev_commands: [/wf_01_planning, /wf_05_code, /wf_06_debug]
next_commands: [/wf_03_prime, /wf_05_code]
context_rules:
  - "从PLANNING.md生成任务列表"
  - "任务必须映射到PRD需求"
  - "实时更新任务状态"
---

## 执行上下文
**输入**: PLANNING.md (create模式) 或 TASK.md (update/review模式)
**输出**: TASK.md (任务跟踪文档)
**依赖链**: /wf_01_planning → **当前** → /wf_03_prime / /wf_05_code

## Usage
`/wf_02_task [update|create|review]`

## Purpose
Manage TASK.md to track project progress and maintain task continuity:
- Create comprehensive task lists from PLANNING.md
- Update task status and add new tasks
- Review progress and identify blockers
- Maintain context across development sessions

## Process
### Create Mode
1. **Read PLANNING.md** thoroughly
2. **Generate Task Categories**:
   - **Setup & Configuration** - Environment, tools, dependencies
   - **Core Development** - Main features and functionality
   - **Data Layer** - Database, models, migrations
   - **API Development** - Endpoints, contracts, validation
   - **Testing** - Unit, integration, E2E tests
   - **Documentation** - Technical docs, API docs, user guides
   - **Security** - Auth, validation, security measures
   - **Performance** - Optimization, caching, monitoring
   - **Deployment** - CI/CD, environments, scripts
   - **Maintenance** - Refactoring, debt, improvements
   - **Completed** - Finished tasks with dates

3. **Task Format**:
   ```markdown
   - [ ] Clear, actionable task description
     - Acceptance criteria
     - Dependencies: [task references]
     - Priority: High/Medium/Low
     - Effort: S/M/L/XL
     - Status: Not Started/In Progress/Blocked/Done
     - Git commits: [commit hash] (completed tasks only)
     - Related ADR: [ADR link] (if architectural decision)
     - Blockers: [reason] (if Status=Blocked)
   ```

   **IMPORTANT - SSOT Principles**:
   - ✅ **DO** record: Task name, status, priority, Git commits hash
   - ❌ **DON'T** record: Implementation details (use `git log [hash]` instead)
   - ❌ **DON'T** record: Code changes, file lists (already in Git commits)
   - ❌ **DON'T** duplicate: Git commit messages content

   **Query implementation details**: Use `git log [commit hash]` to see full details

### Update Mode
1. **Read Current TASK.md**
2. **Update Task Status**:
   - Mark completed tasks with date
   - Update in-progress tasks
   - Add new discovered tasks
   - Document blockers

3. **Reorganize if Needed**:
   - Move completed to archive section
   - Reprioritize based on dependencies
   - Group related tasks

### Review Mode
1. **Analyze Progress**:
   - Calculate completion percentage
   - Identify critical path
   - Find blockers and dependencies

2. **Generate Report**:
   - Sprint/iteration summary
   - Velocity metrics
   - Risk assessment
   - Recommendations

## Output Format
### Create/Update
1. **TASK.md File** - Updated task document
2. **Change Summary** - What was added/modified
3. **Priority Tasks** - Next immediate actions
4. **Blockers** - Issues requiring attention

### Review
1. **Progress Report** - Completion metrics and trends
2. **Risk Analysis** - Potential delays or issues
3. **Recommendations** - Process improvements
4. **Next Sprint** - Suggested task prioritization

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[项目启动] → [任务规划 ← 当前] → [加载上下文] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [提交保存]
  STEP 0       STEP 0.5        STEP 1          STEP 2       STEP 3       STEP 4       STEP 5      STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_02_task` 前，你应该已经完成：

1. ✅ **项目规划** (`/wf_01_planning`)
   - PLANNING.md 已生成或更新

### 📝 当前步骤

**正在执行**: `/wf_02_task [create|update|review]`

- **Create 模式**: 从 PLANNING.md 生成初始任务列表
- **Update 模式**: 更新任务状态和添加新任务
- **Review 模式**: 分析进度和风险

### ⏭️ 建议下一步

**任务创建/更新完成后**，建议按以下顺序执行：

#### 路径 1：新项目初始化（推荐）✅
```bash
# 当前: 已创建初始任务列表
/wf_03_prime  # 加载上下文

# 可选: 验证架构
/wf_04_ask "任务分解是否合理？"

# 开始开发
/wf_05_code "实现第一个任务"
```

#### 路径 2：更新现有任务
```bash
# 当前: 已更新任务状态
/wf_03_prime  # 重新加载上下文

# 继续开发
/wf_05_code "继续当前任务"
```

#### 路径 3：任务审查和规划
```bash
# 当前: 审查任务进度和风险
# 根据审查结果调整任务优先级
/wf_03_prime  # 刷新上下文

# 继续工作
/wf_05_code  或  /wf_06_debug  或其他命令
```

### 📊 工作流进度提示

当你完成任务管理时，确保输出中包含：

✅ 已完成:
- TASK.md 已生成或更新
- 任务优先级清晰
- 依赖关系已识别

⏭️ 下一步提示:
- 推荐执行 `/wf_03_prime` 加载新的任务上下文
- 准备开始 `/wf_05_code` 实现

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 新项目首次创建任务 | 路径 1 | /wf_03_prime → /wf_05_code |
| 更新现有任务状态 | 路径 2 | /wf_03_prime → /wf_05_code |
| 定期审查进度 | 路径 3 | /wf_03_prime → 相应命令 |
| 需要重新规划 | 咨询 | /wf_04_ask "如何重新组织任务？" |

## Integration Notes
- Depends on PLANNING.md for initial creation
- Used by `/wf_03_prime` to understand current state
- Updated after each `/wf_05_code` completion
- Reviewed before `/wf_11_commit` operations
- Drives sprint planning and daily work

## Task State Transitions
```
Not Started → In Progress → Review → Done
           ↓                ↓
         Blocked         Rework
```

## Priority Matrix
- **High**: Core functionality, blockers, security
- **Medium**: Features, improvements, tests
- **Low**: Nice-to-have, optimizations, debt