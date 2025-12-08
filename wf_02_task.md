---
command: /wf_02_task
index: 02
phase: "基础设施"
description: "管理任务追踪系统，支持创建、更新和审查模式"
reads: [PLANNING.md, TASK.md]
writes: [TASK.md]
prev_commands: [/wf_01_planning, /wf_05_code, /wf_06_debug]
next_commands: [/wf_03_prime, /wf_05_code]
model: haiku
token_budget: simple
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "任务关联代码符号和进度跟踪"
context_rules:
  - "从PLANNING.md生成任务列表"
  - "任务必须映射到PRD需求"
  - "实时更新任务状态"
---

## 🔌 MCP 增强能力

本命令支持 Serena MCP 服务器的自动增强。

### Serena (语义代码理解)

**启用**: 自动激活（检测到任务操作时）
**用途**: 任务关联到具体代码符号，基于代码变更跟踪进度
**自动激活**: 创建、更新或审查任务时

**示例**:
```bash
# 创建任务并自动关联代码
/wf_02_task create "实现用户认证API"

# 更新任务并追踪代码进度
/wf_02_task update "完成登录功能"

# 审查任务时分析代码覆盖率
/wf_02_task review
```

**改进点**:
- 任务自动关联到具体代码符号（类、函数、模块）
- 进度跟踪基于实际代码变更
- 符号级依赖分析（find_referencing_symbols）
- 代码覆盖率评估（未测试路径识别）
- 智能任务拆分建议（基于代码复杂度）

---

### 🔧 MCP Gateway 集成 (NEW - Task 3.2)

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Serena 工具调用** (任务-代码关联):
```python
# 检查可用性
if gateway.is_available("serena"):
    # 任务关联到代码符号
    find_symbol_tool = gateway.get_tool("serena", "find_symbol")
    get_overview_tool = gateway.get_tool("serena", "get_symbols_overview")

    # 示例1：关联任务到类
    task_name = "实现用户认证"
    symbol_result = find_symbol_tool.call(
        name_path_pattern="AuthService",
        include_body=False,
        depth=1
    )
    # 将 task_name 关联到 symbol_result 中的符号

    # 示例2：追踪任务进度（基于代码变更）
    file_path = "src/auth/auth_service.py"
    overview_result = get_overview_tool.call(
        relative_path=file_path
    )
    # 分析 overview_result 判断任务完成度

    # 示例3：查找任务相关的所有引用
    find_refs_tool = gateway.get_tool("serena", "find_referencing_symbols")
    refs_result = find_refs_tool.call(
        name_path="AuthService/login",
        relative_path=file_path
    )
    # 识别任务影响范围

else:
    # 降级到手动任务管理
    print("⚠️ Serena MCP 不可用，使用标准任务追踪流程")
```

**Gateway 优势**:
- ✅ 统一的 MCP 服务器管理
- ✅ 自动降级机制（MCP 不可用时）
- ✅ 连接池复用（减少启动开销）
- ✅ 工具懒加载（按需初始化）

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