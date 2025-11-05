---
command: /wf_08_review
index: 08
phase: "质量保证"
description: "代码审查协调器，多维度质量检查"
reads: [PLANNING.md(质量标准), KNOWLEDGE.md(代码模式), 代码文件]
writes: [TASK.md(改进任务), KNOWLEDGE.md(新模式)]
prev_commands: [/wf_05_code, /wf_07_test, /wf_09_refactor]
next_commands: [/wf_09_refactor, /wf_11_commit]
context_rules:
  - "执行PRD合规性检查"
  - "验证PLANNING.md标准遵守"
  - "识别可重用模式到KNOWLEDGE.md"
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

## Workflow Integration
- Enforces PLANNING.md standards
- Leverages patterns from KNOWLEDGE.md
- Contributes new patterns to KNOWLEDGE.md
- Generates tasks in TASK.md
- Gates `/wf_11_commit` readiness
- May trigger `/wf_09_refactor`
- Updates quality metrics