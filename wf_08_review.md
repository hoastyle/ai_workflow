---
command: /wf_08_review
index: 08
phase: "质量保证"
description: "代码审查协调器，多维度质量检查，集成 Ultrathink 设计优雅度评审"
reads: [PLANNING.md(质量标准), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(可选), 代码文件]
writes: [TASK.md(改进任务), KNOWLEDGE.md(新模式)]
prev_commands: [/wf_05_code, /wf_07_test, /wf_09_refactor]
next_commands: [/wf_09_refactor, /wf_11_commit]
ultrathink_lens: "design_elegance"
context_rules:
  - "执行PRD合规性检查"
  - "验证PLANNING.md标准遵守"
  - "识别可重用模式到KNOWLEDGE.md"
  - "Ultrathink 设计优雅度评审（Obsess Over Details）：除了功能正确，代码优雅度如何？"
---

## 执行上下文
**输入**: PLANNING.md标准 + KNOWLEDGE.md模式 + 代码实现
**输出**: 审查报告 + TASK.md改进任务 + KNOWLEDGE.md新模式
**依赖链**: /wf_07_test → **当前（代码审查）** → /wf_09_refactor (可选) → /wf_11_commit

## Usage
`/wf_08_review <CODE_SCOPE>`

## Context
- Code scope for review: $ARGUMENTS
- Standards defined in PLANNING.md
- Review tasks tracked in TASK.md
- Quality gates from project requirements

## Your Role
Code Review Coordinator ensuring project standards:
1. **Quality Auditor** – checks against coding standards
2. **Security Analyst** – validates security guidelines
3. **Performance Reviewer** – assesses efficiency targets
4. **Architecture Assessor** – verifies design alignment

## Process
1. **Review Preparation**:
   - Load standards from PLANNING.md
   - Check related tasks in TASK.md
   - Review existing patterns from KNOWLEDGE.md
   - Identify review scope

2. **Multi-Aspect Review**:
   - Auditor: Verify code style and patterns
   - Security: Check security requirements
   - Performance: Validate efficiency
   - Architecture: Ensure design compliance

3. **Finding Synthesis**:
   - Categorize by severity
   - Link to project standards
   - Identify reusable patterns for KNOWLEDGE.md
   - Prioritize fixes

4. **Action Planning**:
   - Create fix tasks for TASK.md
   - Update PLANNING.md if needed
   - Document patterns and standards for KNOWLEDGE.md
   - Document decisions

## Output Format
1. **Review Summary** – overall assessment
2. **Findings** – issues with standard references
3. **Pattern Analysis** – reusable patterns identified for KNOWLEDGE.md
4. **Required Changes** – must-fix items
5. **Recommendations** – improvement suggestions
6. **Task Generation** – new TASK.md entries
7. **👁️ Ultrathink 设计优雅度评审** (可选提醒) – 设计质量维度（参见 PHILOSOPHY.md）
   - 📐 **代码结构**: 是否流畅易懂？函数职责清晰吗？
   - ✨ **命名质量**: 变量名/函数名是否自然而消除歧义？
   - 🎯 **必然性**: 代码是否"不得不这样"，有没有不必要的复杂性？
   - ⚖️ **权衡认知**: 如果有性能/可读性权衡，是否明确且值得？

## Workflow Integration
- Enforces PLANNING.md standards
- Leverages patterns from KNOWLEDGE.md
- Contributes new patterns to KNOWLEDGE.md
- Generates tasks in TASK.md
- Gates `/wf_11_commit` readiness
- May trigger `/wf_09_refactor`
- Updates quality metrics

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[任务确认] → [架构咨询] → [代码实现] → [测试验证] → [代码审查 ← 当前] → [提交保存]
   STEP 1      STEP 2 (可选)   STEP 3        STEP 4          STEP 5        STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_08_review` 前，你应该已经完成：

1. ✅ **任务确认** (`/wf_02_task update`)
2. ✅ **架构咨询**（可选，`/wf_04_ask`）
3. ✅ **代码实现** (`/wf_05_code`)
4. ✅ **测试验证** (`/wf_07_test`)

### 📝 当前步骤

**正在执行**: `/wf_08_review "代码范围"`

- 多维度质量检查（代码风格、安全性、性能、架构）
- 验证 PLANNING.md 标准遵守
- 检查 PRD 合规性
- 识别代码中的优雅度问题

### ⏭️ 建议下一步

**代码审查完成后**，建议按以下顺序执行：

#### 路径 1：审查通过，无需改进 ✅
```bash
# 第6步: 直接提交
/wf_11_commit "feat/fix/test: [描述]"
```

#### 路径 2：发现必须修改的问题 🔴
```bash
# 回到代码实现修改问题
/wf_05_code "修复审查发现的问题"

# 重新运行测试确保没有回归
/wf_07_test "[相同功能]"

# 重新审查
/wf_08_review "[代码范围]"

# 审查通过后提交
/wf_11_commit "fix: 修复代码审查发现的问题"
```

#### 路径 3：发现可选改进项 ✨
```bash
# 创建改进任务（TASK.md 会自动生成）
# 或使用重构命令处理改进
/wf_09_refactor "[改进范围]"

# 改进后提交
/wf_11_commit "refactor: 代码优化改进"
```

### 📊 工作流进度提示

当你完成代码审查时，确保输出中包含：

✅ 已完成:
- 代码风格检查通过
- 安全性验证通过
- 性能检查无严重问题
- 架构设计符合标准
- PRD 合规性确认

⏭️ 下一步提示:
- 如果有必须修改的问题（🔴），说明需要回到代码实现
- 如果有可选改进（✨），说明可以创建重构任务
- 如果审查通过，准备进入最后的提交阶段

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 审查通过，无问题 | 路径 1 | /wf_11_commit "..." |
| 发现严重问题 | 路径 2 | /wf_05_code → /wf_07_test → /wf_08_review |
| 发现改进机会 | 路径 3 | /wf_09_refactor → /wf_11_commit |
| 无法决策 | 咨询 | /wf_04_ask "这个问题应该立即修复还是后续改进？" |

### 🔄 反馈循环

**审查发现的问题如何处理？**

1. **🔴 必须修改** - 立即执行修改
   ```bash
   /wf_05_code "修复 [具体问题]"
   /wf_07_test  # 确保测试不失败
   /wf_08_review  # 重新审查
   ```

2. **✨ 建议改进** - 后续迭代处理
   - 创建 TASK.md 记录
   - 下个迭代执行 /wf_09_refactor

3. **📚 模式/最佳实践** - 记录到 KNOWLEDGE.md
   - 识别可重用的好模式
   - 记录到知识库供后续参考

### 📚 相关文档

- **工作流指南**: WORKFLOWS.md
- **代码标准**: PLANNING.md (Code Quality, Development Standards)
- **质量指标**: PLANNING.md (Quality Gates)
- **设计原则**: PHILOSOPHY.md (Ultrathink)
- **模式库**: KNOWLEDGE.md
- **任务追踪**: TASK.md