---
command: /wf_06_debug
index: 06
phase: "开发实现"
description: "系统化调试修复，支持快速修复模式"
reads: [PLANNING.md(系统设计), TASK.md(相关任务), KNOWLEDGE.md(已知问题)]
writes: [代码文件, TASK.md(修复记录), KNOWLEDGE.md(新解决方案)]
prev_commands: [/wf_05_code, /wf_07_test]
next_commands: [/wf_07_test, /wf_09_refactor, /wf_11_commit]
context_rules:
  - "使用KNOWLEDGE.md已知解决方案"
  - "修复根本原因，不是症状"
  - "新模式记录到KNOWLEDGE.md"
---

## 执行上下文
**输入**: 错误描述 + PLANNING.md系统设计 + KNOWLEDGE.md已知问题
**输出**: 代码修复 + TASK.md记录 + KNOWLEDGE.md新模式
**依赖链**: **当前（错误修复）** → /wf_07_test (验证) → /wf_11_commit

## Usage
`/wf_06_debug <ERROR_DESCRIPTION> [--quick]`

## Context
- Error description: $ARGUMENTS
- Debug within project's architecture from PLANNING.md
- Track debugging work in TASK.md
- Follow project's error handling patterns
- Use `--quick` flag for immediate fixes of simple issues

## Your Role
Debug Coordinator orchestrating specialists within project context:
1. **Error Analyzer** – identifies root cause per system design
2. **Code Inspector** – examines using project conventions
3. **Environment Checker** – validates against PLANNING.md specs
4. **Fix Strategist** – proposes solutions maintaining standards

## Process

### Standard Debugging (default)
1. **Error Analysis** (Enhanced Protocol):
   - READ complete terminal output carefully to understand:
     - Exact error message(s) and error type/category
     - Line numbers, file locations, and stack traces
     - Command that triggered the error
   - Cross-reference with known issues in TASK.md
   - Check KNOWLEDGE.md for similar problem-solution patterns
   - Review relevant PLANNING.md sections for system context

2. **Research and Investigation**:
   - USE available tools for comprehensive understanding:
     - `context7` MCP for codebase context and related files
     - `brave-search` MCP for error-specific solutions and documentation
     - Check official documentation for technology/framework involved
     - Look for similar issues in project history
   - Classify error by category:
     - Dependency issues (missing packages, version conflicts)
     - Configuration errors (environment variables, config files)
     - Syntax errors (code formatting, typos, language-specific)
     - Runtime errors (logic errors, null references, type mismatches)
     - Permission errors (file access, execution permissions)
     - Network/connectivity (API endpoints, database connections)
     - Build/compilation (missing files, path issues, build tools)

3. **Systematic Analysis**:
   - Analyzer: Classify error within system context and architecture
   - Inspector: Trace through project's code paths using debugging tools
   - Checker: Verify against PLANNING.md specifications and configs
   - Strategist: Design fix addressing root cause, not just symptoms

4. **Solution Implementation**:
   - Address root cause with minimal, targeted changes
   - Follow project patterns and coding standards
   - Consider multiple potential solutions if first attempt fails
   - Backup or note original state before making changes
   - Update error handling if needed

5. **Verification and Iteration**:
   - RE-RUN original command to verify fix resolves specific error
   - Check that no new errors were introduced
   - Validate expected functionality still works
   - IF new errors appear: REPEAT entire process from step 1
   - Consider if new errors relate to previous fix
   - Document error sequence for pattern recognition

6. **Documentation and Prevention**:
   - Update TASK.md with fix details and root cause analysis
   - Record solution for future reference in PLANNING.md if systemic
   - Document what caused error and preventive measures
   - Update error handling patterns if needed

### Quick Fix Mode (--quick flag)
1. **Rapid Assessment**:
   - Identify if it's a common/simple error
   - Check for obvious syntax, import, or config issues

2. **Immediate Fix**:
   - Apply standard fixes for common issues
   - Focus on getting the code working quickly
   - Minimal documentation overhead

3. **Fast Validation**:
   - Quick test to ensure fix works
   - Update TASK.md with brief fix note

## Output Format
1. **Debug Analysis** – root cause within system context
2. **Fix Implementation** – solution following standards
3. **Knowledge Capture** – new problem-solution patterns for KNOWLEDGE.md
4. **Task Updates** – TASK.md entries for fixes
5. **Prevention Notes** – updates for PLANNING.md
6. **Test Requirements** – validation needed

## Workflow Integration
- References PLANNING.md for system design
- Leverages KNOWLEDGE.md for past solutions
- Updates TASK.md with debugging work
- Contributes new patterns to KNOWLEDGE.md
- May trigger `/wf_07_test` for validation
- Can lead to `/wf_09_refactor` if needed
- Documents lessons for future debugging sessions