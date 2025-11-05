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
     - Notes: Implementation details or blockers
   ```

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