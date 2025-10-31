---
command: /wf_09_refactor
index: 09
phase: "质量保证"
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