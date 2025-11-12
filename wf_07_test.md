---
command: /wf_07_test
index: 07
phase: "质量保证"
description: "测试开发和覆盖率分析，支持coverage模式"
reads: [PLANNING.md(测试策略), TASK.md(测试任务), 代码文件]
writes: [测试文件, TASK.md(测试状态), 覆盖率报告]
prev_commands: [/wf_05_code, /wf_06_debug, /wf_09_refactor]
next_commands: [/wf_08_review, /wf_09_refactor, /wf_11_commit]
context_rules:
  - "遵循PLANNING.md测试策略"
  - "满足PRD覆盖率要求"
  - "--coverage模式分析测试覆盖率"
---

## 执行上下文
**输入**: PLANNING.md测试策略 + 代码实现
**输出**: 测试代码 + 覆盖率报告 + TASK.md更新
**依赖链**: /wf_05_code → **当前（测试开发）** → /wf_08_review → /wf_11_commit

## Usage
`/wf_07_test <COMPONENT_OR_FEATURE> [--coverage]`

## Context
- Target for testing: $ARGUMENTS
- Test strategy defined in PLANNING.md
- Test tasks tracked in TASK.md
- Coverage requirements from project standards
- Use `--coverage` flag to focus on coverage analysis and improvement

## Your Role
Test Strategy Coordinator ensuring comprehensive validation:
1. **Test Architect** – designs tests per PLANNING.md strategy
2. **Unit Test Specialist** – creates tests following project patterns
3. **Integration Engineer** – validates system interactions
4. **Quality Validator** – ensures coverage meets requirements

## Process

### Standard Testing (default)
1. **Test Planning**:
   - Review testing strategy in PLANNING.md
   - Check TASK.md for test requirements
   - Identify coverage gaps

2. **Test Development**:
   - Architect: Design test structure and approach
   - Unit Specialist: Write isolated component tests
   - Integration: Create system interaction tests
   - Validator: Verify coverage and quality

3. **Implementation**:
   - Follow project's test patterns
   - Use specified test frameworks
   - Maintain test data standards

4. **Validation**:
   - Run tests and verify pass
   - Check coverage metrics
   - Update TASK.md status

### Coverage Analysis Mode (--coverage flag)
1. **Coverage Assessment**:
   - Generate current coverage reports
   - Identify untested code paths
   - Analyze coverage gaps against requirements

2. **Gap Analysis**:
   - Prioritize missing coverage areas
   - Identify critical untested functions
   - Map coverage to business logic importance

3. **Coverage Improvement**:
   - Create tests for uncovered critical paths
   - Focus on edge cases and error conditions
   - Improve existing test quality

4. **Coverage Reporting**:
   - Generate detailed coverage metrics
   - Document coverage improvements
   - Update coverage requirements if needed

## Output Format

### Standard Testing Output
1. **Test Strategy** – approach aligned with project
2. **Test Implementation** – concrete test code
3. **Coverage Report** – basic metrics against requirements
4. **Task Updates** – TASK.md test completions
5. **Next Steps** – remaining test work

### Coverage Analysis Output (--coverage flag)
1. **Coverage Summary** – current coverage statistics
2. **Gap Analysis** – detailed uncovered areas
3. **Priority Recommendations** – critical missing tests
4. **Improvement Plan** – tests to add for better coverage
5. **Coverage Trends** – comparison with previous runs

## Workflow Integration
- Follows PLANNING.md test strategy
- Updates test tasks in TASK.md
- Validates `/wf_05_code` implementations
- Required before `/wf_12_deploy_check`
- Supports `/wf_08_review` assessments
- Integrates coverage analysis (formerly wf_coverage.md functionality)
- Coverage reports inform `/wf_09_refactor` decisions

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[任务确认] → [架构咨询] → [代码实现] → [测试验证 ← 当前] → [代码审查] → [提交保存]
   STEP 1      STEP 2 (可选)   STEP 3        STEP 4          STEP 5     STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_07_test` 前，你应该已经完成：

1. ✅ **任务确认** (`/wf_02_task update`)
2. ✅ **架构咨询**（可选，`/wf_04_ask`）
3. ✅ **代码实现** (`/wf_05_code`)

### 📝 当前步骤

**正在执行**: `/wf_07_test "组件或功能名称" [--coverage]`

**模式说明**：
- **标准模式**（默认）：编写和运行单元测试
- **覆盖率模式**（`--coverage`）：分析测试覆盖率并生成报告

### ⏭️ 建议下一步

**测试完成后**，建议按以下顺序执行：

#### 路径 1：测试通过 ✅
```bash
# 第5步: 代码审查
/wf_08_review

# 第6步: 提交保存进度
/wf_11_commit "test: 为 [功能] 添加测试"
```

#### 路径 2：测试发现问题 🐛
```bash
# 回到代码实现修改代码
/wf_05_code "修复失败的测试"

# 重新运行测试
/wf_07_test "[相同功能]"

# 然后继续审查和提交
/wf_08_review
/wf_11_commit "test: [功能] - 修复失败测试"
```

#### 路径 3：覆盖率不达标 📊
```bash
# 使用覆盖率模式分析
/wf_07_test "[功能]" --coverage

# 根据报告添加缺失测试
/wf_07_test "[功能] - 增加覆盖率"

# 覆盖率达标后继续
/wf_08_review
/wf_11_commit "test: 提升 [功能] 覆盖率"
```

### 📊 工作流进度提示

当你完成测试时，确保输出中包含：

✅ 已完成:
- 所有测试通过 ✓
- 覆盖率达标（如有要求）
- TASK.md 已更新

⏭️ 下一步提示:
- 如果覆盖率不达标，说明需要添加更多测试
- 如果所有测试通过，准备进入代码审查
- 显示推荐的下一个命令

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 所有测试通过 | 路径 1 | /wf_08_review → /wf_11_commit |
| 测试失败 | 路径 2 | /wf_05_code → /wf_07_test → /wf_08_review |
| 覆盖率不达标 | 路径 3 | /wf_07_test --coverage → 添加测试 → /wf_08_review |
| 需要覆盖率分析 | 分析模式 | /wf_07_test "[功能]" --coverage |
| 不确定 | 咨询 | /wf_04_ask "测试策略是否完善？" |

### 🔄 回到上一步

如果测试发现设计缺陷：
```bash
/wf_04_ask "测试发现的设计问题..."
# 修改代码或测试后重新运行此命令
```

### 📚 相关文档

- **工作流指南**: WORKFLOWS.md
- **测试策略**: PLANNING.md (Testing Strategy)
- **任务追踪**: TASK.md
- **代码质量**: PLANNING.md (Code Quality)