---
command: /wf_05_code
index: 05
phase: "开发实现"
reads: [PLANNING.md(开发标准), TASK.md(当前任务), KNOWLEDGE.md(代码模式)]
writes: [代码文件, TASK.md(状态更新)]
prev_commands: [/wf_03_prime, /wf_04_ask]
next_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
context_rules:
  - "遵循PLANNING.md的代码标准"
  - "满足PRD需求"
  - "更新TASK.md进度"
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

## Workflow Integration
- Reads context from PLANNING.md
- Updates progress in TASK.md
- Triggers `/wf_07_test` for validation
- Prepares for `/wf_08_review` cycle
- Leads to `/wf_11_commit` when complete