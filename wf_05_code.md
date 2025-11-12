---
command: /wf_05_code
index: 05
phase: "开发实现"
description: "功能实现协调器，遵循架构标准编写代码，集成 Ultrathink 优雅实现"
reads: [PLANNING.md(开发标准), TASK.md(当前任务), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(可选)]
writes: [代码文件, TASK.md(状态更新)]
prev_commands: [/wf_03_prime, /wf_04_ask]
next_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
ultrathink_lens: "craft_elegance"
context_rules:
  - "遵循PLANNING.md的代码标准"
  - "满足PRD需求"
  - "更新TASK.md进度"
  - "Ultrathink 优雅实现（Craft, Don't Code）：函数名清晰、抽象自然、错误处理优雅"
---

## 执行上下文
**输入**: PLANNING.md标准 + TASK.md任务 + KNOWLEDGE.md模式
**输出**: 代码实现 + TASK.md更新
**依赖链**: /wf_04_ask (可选) → **当前（代码实现）** → /wf_07_test → /wf_08_review

## Usage
`/wf_05_code <FEATURE_DESCRIPTION>`

## Context
- Feature/functionality to implement: $ARGUMENTS
- PLANNING.md defines architecture and standards
- TASK.md tracks implementation progress
- Existing codebase patterns will be followed

## Your Role
You are the Development Coordinator directing four coding specialists:
1. **Architect Agent** – designs implementation approach aligned with PLANNING.md
2. **Implementation Engineer** – writes code following project standards
3. **Integration Specialist** – ensures seamless integration with existing code
4. **Code Reviewer** – validates quality and updates TASK.md progress

## Process
1. **Context Loading**:
   - Read relevant sections from PLANNING.md
   - Check TASK.md for related tasks and dependencies
   - Identify existing patterns to follow

2. **Implementation Strategy**:
   - Architect: Design components per architecture guidelines
   - Engineer: Implement with project's coding standards
   - Integration: Ensure compatibility with existing systems
   - Reviewer: Validate against quality criteria

3. **Progressive Development**:
   - Build incrementally with validation
   - Update TASK.md after each milestone
   - Document significant decisions

4. **Quality Validation**:
   - Ensure code meets PLANNING.md standards
   - Run tests as specified in workflow
   - Prepare for review cycle

## Output Format
1. **Implementation Plan** – approach aligned with project architecture
2. **Code Implementation** – working code following standards
3. **Task Updates** – TASK.md updates for completed work
4. **Integration Notes** – how code fits into system
5. **Next Actions** – remaining tasks and dependencies
6. **📚 Documentation Reminder** (NEW) – if technical docs were created:
   - ✅ All docs/ files have complete Frontmatter metadata
   - ✅ Required fields: title, description, type, status, priority, created_date, last_updated
   - ✅ Recommended fields: related_documents, related_code, tags
   - ⚠️ If missing: Run `/wf_14_doc` to auto-generate or manually add from CLAUDE.md template
7. **🎨 Ultrathink 设计检查** (可选提醒) – 代码优雅度自检（参见 PHILOSOPHY.md）
   - ✅ 函数/变量名字是否自然而清晰？(Obsess Over Details)
   - ✅ 代码结构是否流畅易懂？(Craft, Don't Code)
   - ✅ 错误处理是否优雅而有用？(Craft, Don't Code)
   - ✅ 有没有不必要的复杂性能移除？(Simplify Ruthlessly)

## Workflow Integration
- Reads context from PLANNING.md
- Updates progress in TASK.md
- Triggers `/wf_07_test` for validation
- Prepares for `/wf_08_review` cycle
- Leads to `/wf_11_commit` when complete

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[任务确认] → [架构咨询] → [代码实现 ← 当前] → [测试验证] → [代码审查] → [提交保存]
   STEP 1      STEP 2 (可选)   STEP 3        STEP 4      STEP 5     STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_05_code` 前，你应该已经完成：

1. ✅ **任务确认** (`/wf_02_task update`)
   - 从 TASK.md 选择并标记待做任务

2. ✅ **架构咨询**（可选，`/wf_04_ask`）
   - 如果需要设计指导，已运行咨询
   - 如果任务明确，可以跳过

### 📝 当前步骤

**正在执行**: `/wf_05_code "功能描述"`

- 遵循 PLANNING.md 的开发标准
- 实现功能并更新代码
- 符合 PRD 需求
- 准备进入测试阶段

### ⏭️ 建议下一步

**代码实现完成后**，建议按以下顺序执行：

#### 选项 A：先测试再审查（推荐）✅
```bash
# 第4步: 添加测试（如果功能较复杂）
/wf_07_test "为 [功能] 添加单元测试"

# 第5步: 代码审查
/wf_08_review

# 第6步: 提交保存进度
/wf_11_commit "feat: [功能描述]"
```

#### 选项 B：先审查再测试
```bash
# 第5步: 代码审查
/wf_08_review

# 第4步: 根据审查意见添加测试
/wf_07_test "为 [功能] 添加测试"

# 第6步: 提交
/wf_11_commit "feat: [功能描述]"
```

#### 选项 C：简单功能跳过测试
```bash
# 第5步: 代码审查
/wf_08_review

# 第6步: 提交
/wf_11_commit "feat: [功能描述]"
```

### 📊 工作流进度提示

当你完成代码实现时，确保输出中包含：

✅ 已完成:
- 代码实现完成
- TASK.md 已更新
- 代码符合 PLANNING.md 标准

⏭️ 下一步提示:
- 显示推荐的下一个命令
- 说明选择的原因
- 提供替代选项

### 💡 决策指南

**我应该执行哪个选项？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 功能复杂且新增 | 选项 A | /wf_07_test → /wf_08_review → /wf_11_commit |
| 功能修改已有代码 | 选项 B | /wf_08_review → /wf_07_test → /wf_11_commit |
| 简单功能/文档修改 | 选项 C | /wf_08_review → /wf_11_commit |
| 不确定 | 咨询 | /wf_04_ask "我应该先测试还是先审查？" |

### 🔄 回到上一步

如果需要修改设计或架构：
```bash
/wf_04_ask "需要重新讨论的架构问题..."
# 修改代码后继续当前步骤
```

### 📚 相关文档

- **工作流指南**: WORKFLOWS.md
- **代码标准**: PLANNING.md (Development Standards)
- **任务追踪**: TASK.md
- **设计原则**: PHILOSOPHY.md (Ultrathink)