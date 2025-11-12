---
command: /wf_09_refactor
index: 09
phase: "质量保证"
description: "代码重构服务，保持架构一致性"
reads: [PLANNING.md(架构设计), TASK.md(技术债), KNOWLEDGE.md(代码模式)]
writes: [代码文件, TASK.md(重构完成), PLANNING.md(可能)]
prev_commands: [/wf_08_review]
next_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
context_rules:
  - "对齐PLANNING.md架构"
  - "应用KNOWLEDGE.md最佳实践"
  - "保持PRD功能不变"
---

## 执行上下文
**输入**: PLANNING.md架构 + TASK.md技术债 + KNOWLEDGE.md模式
**输出**: 重构代码 + TASK.md更新 + 可能的PLANNING.md改进
**依赖链**: /wf_08_review → **当前（代码重构）** → /wf_07_test (回归)

## Usage
`/wf_09_refactor <REFACTOR_SCOPE>`

## Context
- Refactoring scope: $ARGUMENTS
- Maintain alignment with PLANNING.md architecture
- Track refactoring in TASK.md
- Preserve functionality while improving structure

## Your Role
Refactoring Coordinator ensuring project consistency:
1. **Structure Analyst** – evaluates against planned architecture
2. **Code Surgeon** – transforms per project patterns
3. **Pattern Expert** – applies patterns from PLANNING.md
4. **Quality Validator** – ensures standards compliance

## Process
1. **Current State Analysis**:
   - Review code against PLANNING.md ideals
   - Check TASK.md for related debt items
   - Identify improvement opportunities

2. **Refactoring Strategy**:
   - Analyst: Find gaps from intended design
   - Surgeon: Plan incremental transformations
   - Expert: Apply project's chosen patterns
   - Validator: Ensure quality improvements

3. **Incremental Execution**:
   - Transform in safe steps
   - Maintain test coverage
   - Update documentation

4. **Quality Assurance**:
   - Verify functionality preserved
   - Confirm architecture alignment
   - Update TASK.md progress

## Output Format
1. **Refactoring Plan** – steps aligned with architecture
2. **Implementation** – transformed code per standards
3. **Architecture Alignment** – how changes improve design
4. **Task Completion** – TASK.md updates
5. **Documentation** – PLANNING.md refinements

## Workflow Integration
- Guided by PLANNING.md architecture
- Updates technical debt in TASK.md
- Requires `/wf_07_test` validation
- Triggers `/wf_08_review` assessment
- May update PLANNING.md patterns

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行以下阶段（通常在主流程之外）：

```
主流程: [代码实现] → [测试] → [审查] → [提交]

附加流程: [代码审查] → [重构改进 ← 当前] → [再次测试] → [再次审查] → [提交]
           STEP 5      STEP 5.5        STEP 5.6     STEP 5.7     STEP 6
```

### ✅ 触发条件

通常在以下情况下执行此命令：

1. ✅ 代码审查发现改进机会（`/wf_08_review` 建议）
2. ✅ TASK.md 中有重构任务待完成
3. ✅ 需要优化技术债务或性能

### 📝 当前步骤

**正在执行**: `/wf_09_refactor "重构范围"`

- 按照 PLANNING.md 的架构指导重构
- 改进代码质量和可维护性
- 更新技术债务追踪
- 保持功能不变的前提下优化结构

### ⏭️ 建议下一步

**重构完成后**，必须执行：

```bash
# 第1步: 运行测试确保功能没有改变
/wf_07_test "[相同功能] - 验证重构未破坏功能"

# 第2步: 代码审查重构结果
/wf_08_review "重构代码"

# 第3步: 审查通过后提交
/wf_11_commit "refactor: [改进说明]"
```

### 📊 工作流进度提示

重构完成时，确保：

✅ 已完成:
- 重构代码符合 PLANNING.md 标准
- TASK.md 已更新（技术债务减少）
- 准备进入重新测试

⏭️ 下一步提示:
- 必须运行 /wf_07_test 验证功能不变
- 然后运行 /wf_08_review 最终审查
- 审查通过后运行 /wf_11_commit 提交

### 💡 决策指南

| 情况 | 建议 | 命令 |
|------|------|------|
| 审查建议改进 | 执行重构 | /wf_09_refactor → /wf_07_test → /wf_08_review → /wf_11_commit |
| 有技术债务任务 | 执行重构 | /wf_09_refactor → /wf_07_test → /wf_08_review → /wf_11_commit |
| 重构发现新问题 | 循环 | /wf_05_code → /wf_07_test → /wf_09_refactor |

### 📚 相关文档

- **架构指南**: PLANNING.md
- **设计原则**: PHILOSOPHY.md
- **任务追踪**: TASK.md
- **模式库**: KNOWLEDGE.md