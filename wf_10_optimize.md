---
command: /wf_10_optimize
index: 10
phase: "质量保证"
description: "性能优化协调器，满足性能目标"
reads: [PLANNING.md(性能目标), TASK.md(优化任务), 代码文件]
writes: [代码文件, TASK.md(优化完成), 性能报告]
prev_commands: [/wf_08_review]
next_commands: [/wf_09_refactor, /wf_07_test, /wf_11_commit]
model: sonnet
token_budget: medium
context_rules:
  - "满足PRD性能要求"
  - "遵循PLANNING.md性能目标"
  - "保持功能正确性"
---

## 执行上下文
**输入**: PLANNING.md性能目标 + 性能分析数据
**输出**: 优化代码 + 性能改进报告 + TASK.md更新
**依赖链**: **当前（性能优化）** → /wf_07_test (验证) → /wf_11_commit

## Usage
`/wf_10_optimize <PERFORMANCE_TARGET>`

## Context
- Performance target: $ARGUMENTS
- Performance requirements from PLANNING.md
- Optimization tasks in TASK.md
- System constraints and targets

## Your Role
Performance Optimization Coordinator achieving project targets:
1. **Profiler Analyst** – measures against requirements
2. **Algorithm Engineer** – optimizes per constraints
3. **Resource Manager** – manages within limits
4. **Scalability Architect** – ensures target scale

## Process
1. **Performance Baseline**:
   - Review targets in PLANNING.md
   - Check optimization tasks in TASK.md
   - Measure current performance

2. **Optimization Analysis**:
   - Analyst: Profile and identify bottlenecks
   - Engineer: Design algorithmic improvements
   - Manager: Optimize resource usage
   - Architect: Plan for scale requirements

3. **Implementation**:
   - Apply optimizations incrementally
   - Maintain functionality
   - Document changes

4. **Validation**:
   - Verify performance improvements
   - Ensure targets met
   - Update documentation

## Output Format
1. **Performance Analysis** – current vs. target metrics
2. **Optimization Plan** – improvement strategy
3. **Implementation** – optimized code
4. **Results** – achieved improvements
5. **Task Updates** – TASK.md completions

## Workflow Integration
- Targets from PLANNING.md requirements
- Updates optimization tasks in TASK.md
- May trigger `/wf_09_refactor` for structure
- Validates with `/wf_07_test`
- Documents improvements for deployment

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行以下阶段（通常在主流程之外）：

```
主流程: [代码实现] → [测试] → [审查] → [提交]

优化流程: [代码审查] → [性能优化 ← 当前] → [再次测试] → [再次审查] → [提交]
           STEP 5      STEP 5.8        STEP 5.9     STEP 5.10    STEP 6
```

### ✅ 触发条件

通常在以下情况下执行此命令：

1. ✅ PLANNING.md 中有性能目标需要达成
2. ✅ TASK.md 中有优化任务待完成
3. ✅ 用户反馈或基准测试显示性能瓶颈

### 📝 当前步骤

**正在执行**: `/wf_10_optimize "性能目标"`

- 按照 PLANNING.md 的性能要求优化
- 分析性能瓶颈并实施优化
- 更新优化任务状态
- 记录性能改进指标

### ⏭️ 建议下一步

**优化完成后**，必须执行：

```bash
# 第1步: 运行性能测试验证优化结果
/wf_07_test "[相同功能] - 性能回归测试"

# 第2步: 代码审查优化代码
/wf_08_review "优化代码"

# 第3步: 审查通过后提交
/wf_11_commit "perf: [性能优化说明]"
```

### 📊 工作流进度提示

优化完成时，确保：

✅ 已完成:
- 优化代码符合 PLANNING.md 标准
- 性能指标达到或超过目标
- TASK.md 优化任务已更新
- 准备进入性能验证

⏭️ 下一步提示:
- 必须运行 /wf_07_test 验证性能改进
- 然后运行 /wf_08_review 审查代码
- 审查通过后运行 /wf_11_commit 提交

### 💡 决策指南

| 情况 | 建议 | 命令 |
|------|------|------|
| 性能目标未达 | 优化 | /wf_10_optimize → /wf_07_test → /wf_08_review → /wf_11_commit |
| 需要重构优化 | 两步 | /wf_09_refactor → /wf_10_optimize → /wf_07_test |
| 优化效果有限 | 咨询 | /wf_04_ask "还有其他优化方向吗？" |

### 📚 相关文档

- **性能要求**: PLANNING.md (Performance Requirements)
- **优化策略**: PLANNING.md (Optimization Strategy)
- **任务追踪**: TASK.md
- **架构指南**: PLANNING.md (Architecture)
