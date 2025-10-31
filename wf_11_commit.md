---
command: /wf_11_commit
index: 11
phase: "运维部署"
reads: [PLANNING.md(标准), TASK.md(任务), 代码更改]
writes: [CONTEXT.md, TASK.md, KNOWLEDGE.md(可能), README.md(可能), Git提交]
prev_commands: [/wf_05_code, /wf_06_debug, /wf_08_review, /wf_09_refactor, /wf_10_optimize]
next_commands: [/wf_02_task, /clear, /wf_03_prime]
context_rules:
  - "自动更新CONTEXT.md会话状态"
  - "遵守PLANNING.md质量标准"
  - "重要工作自动更新README.md"
  - "识别新模式添加KNOWLEDGE.md"
---

## 执行上下文
**输入**: 代码更改 + PLANNING.md标准 + TASK.md任务
**输出**: Git提交 + CONTEXT.md + 可能的README.md/KNOWLEDGE.md更新
**依赖链**: /wf_08_review → **当前（提交保存）** → /wf_02_task update (可选)

## Usage
`@wf_commit.md [message]`

## Purpose
Create git commits with integrated formatting, validation, and context updates:
- Validate changes against standards
- Auto-format code before commit
- Update TASK.md task completion status
- Auto-update CONTEXT.md with work summary
- **Auto-update README.md when important work completed**
- Identify and suggest KNOWLEDGE.md updates
- Maintain commit message conventions
- Ensure full traceability

## Process
1. **Pre-Commit Auto-Repair & Validation**:
   - Check git status for changes
   - Identify files for staging
   - **Run enhanced pre-commit hooks with auto-repair**:
     * **Auto-fix Trailing Whitespace**: 100% safe, automatic removal
     * **Auto-fix Line Endings**: Convert CRLF to Unix LF automatically
     * **Auto-fix Markdown Formatting**: Basic formatting improvements
     * **Enhanced Validation**: Comprehensive quality checks after auto-repair
     * **Link & Reference Validation**: Manual review recommendations
   - Validate against PLANNING.md standards
   - Check related tasks in TASK.md

2. **Auto-Formatting & Time Sync**:
   - Apply language-specific formatting:
     * Python: black formatter
     * JavaScript/TypeScript: prettier
     * C++: clang-format
     * Go: gofmt
     * Other: project-specific formatters
   - **Pre-commit auto-repair ensures**: Zero trailing whitespace, consistent line endings
   - **Auto-Update Maintenance Dates**:
     * Update "最后更新" fields to current date: `$(date +%Y-%m-%d)`
     * Update "Last Updated" fields to current date: `$(date +%Y-%m-%d)`
     * Preserve historical dates (创建日期、发布日期、决策日期)
     * Validate date format consistency across all .md files
     * Check for and flag any outdated year references

3. **Change Analysis**:
   - Group related changes
   - Identify completed tasks
   - Check for excluded files
   - Validate code formatting applied
   - **README Update Assessment**: Check if changes trigger README update:
     * New core features (feat commits affecting main files)
     * PLANNING.md architecture changes
     * API/interface modifications
     * Dependency or installation requirement changes
     * Major version milestones
   - Analyze changes for knowledge extraction opportunities
   - **Time Point Validation**: Verify all dates are current and accurate

4. **README Update (If Triggered)**:
   - **Content Generation**: Generate updated README.md:
     * Project overview from PLANNING.md
     * Installation requirements from dependencies
     * Core usage examples from available commands
     * Feature list from completed TASK.md items
     * Architecture overview from PLANNING.md
     * Troubleshooting from KNOWLEDGE.md
   - **Quality Validation**: Ensure README meets standards:
     * No trailing whitespace (enforced by pre-commit)
     * Valid markdown formatting
     * Working internal links
     * Current date references
   - **Integration**: Include updated README in commit

5. **Final Pre-Commit Validation**:
   - **Run enhanced pre-commit validation** on all staged files:
     * **Auto-repair hooks**: Fix trailing whitespace, line endings, basic formatting
     * **Validation hooks**: Verify fixes were successful, check remaining quality gates
     * **Final quality check**: Comprehensive validation ensuring all standards met
   - **If validation fails**: Review specific error messages, manual intervention if needed
   - **If validation passes**: All auto-repairs completed successfully, proceed to commit

6. **Commit Preparation**:
   - Stage formatted files (including README if updated)
   - Generate semantic commit message
   - Link to TASK.md items
   - Add task references

7. **Context Update**:
   - Create/update CONTEXT.md with:
     * Work completed this session
     * Tasks finished and remaining
     * Key decisions made
     * Next priority items
   - Include progress summary

8. **Knowledge Extraction**:
   - Identify architectural decisions worthy of ADR documentation
   - Detect new problem-solution patterns
   - Recognize reusable code patterns or conventions
   - Suggest KNOWLEDGE.md updates if applicable

9. **Post-Commit Actions**:
   - Update TASK.md with completions
   - Document significant changes
   - Update KNOWLEDGE.md if new patterns or decisions identified
   - Prepare for next work cycle

## Commit Message Format
```
[<type>][(<scope>)] <subject>

<body>

Tasks: #task-id-1, #task-id-2
Refs: PLANNING.md updates, TASK.md completions
```

Types:
- feat: New feature implementation
- fix: Bug fix
- refactor: Code restructuring
- test: Test additions/changes
- docs: Documentation updates
- perf: Performance improvements
- chore: Maintenance tasks

## Output Format
1. **Auto-Repair Report** – automatic fixes applied (whitespace, line endings, formatting)
2. **Pre-commit Validation Report** – quality gate checks and results
3. **Formatting Report** – language-specific auto-formatting applied
4. **Change Summary** – files and modifications
5. **README Update Report** – README generation details (if triggered)
6. **Knowledge Extraction** – identified patterns and decisions
7. **Commit Message** – formatted message
8. **Task Updates** – TASK.md completions
9. **Context Update** – CONTEXT.md refresh
10. **Knowledge Updates** – KNOWLEDGE.md suggestions or updates
11. **Commit Result** – success confirmation
12. **Next Steps** – remaining work items

## Workflow Integration
- **Auto-Repair System**: Automatically fixes trailing whitespace, line endings, basic formatting
- **Quality Gates**: Enforced through enhanced pre-commit hooks with validation
- **User Experience**: Reduces manual fixes, provides clear feedback on auto-repairs
- Validates against PLANNING.md standards
- Auto-formats code (integrates wf_format.md functionality)
- **Auto-updates README.md for important work completions**
- Updates completed tasks in TASK.md
- Auto-updates CONTEXT.md for session continuity
- Enhances KNOWLEDGE.md with accumulated wisdom
- Follows after `/wf_08_review` approval
- Triggers task status updates
- Maintains complete project history and context
- **Ensures README stays synchronized with project state**
- Enables seamless `/wf_03_prime` context loading with long-term memory

## Pre-commit Framework Integration

### Installation & Setup
```bash
# Install pre-commit framework
pip install pre-commit

# Install the hooks in your repository
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files

# Run hooks on staged files only
pre-commit run
```

### Auto-Repair Capabilities
- **Trailing Whitespace**: 100% safe automatic removal using sed
- **Line Endings**: Automatic CRLF to Unix LF conversion (dos2unix or sed fallback)
- **Markdown Formatting**: Basic formatting improvements (blank lines, header spacing)
- **Smart Detection**: Only attempts repairs when issues are found
- **Clear Feedback**: Detailed reporting of what was fixed

### Quality Gates Enforced
- **Post-Repair Validation**: Ensures all auto-repairs were successful
- **File Format Validation**: Ensures consistent file formats across the project
- **Line Ending Verification**: Confirms Unix LF line endings after conversion
- **Markdown Links**: Validates external and internal links
- **Command References**: Ensures consistent command references across documentation
- **Final Quality Check**: Comprehensive validation ensuring all standards met

### Enhanced Hook Configuration
The `.pre-commit-config.yaml` file contains:
- **Auto-repair hooks**: 3 safe automatic repair operations
- **Validation hooks**: 4 comprehensive quality validation steps
- **Progressive reporting**: Clear feedback on each operation
- **Fallback mechanisms**: Multiple tools available for each repair type
- **Fail-fast behavior**: Stops on critical errors that cannot be auto-repaired

### Integration Benefits
- **Automated Quality Control**: No manual checks needed for common issues
- **Instant Fixes**: Most formatting problems resolved automatically
- **User-Friendly**: Clear feedback on what was repaired
- **Consistent Standards**: Enforced across all commits
- **Early Detection**: Issues caught and fixed before commit
- **Reduced Overhead**: Minimal user intervention required
- **Reliable Enforcement**: Zero tolerance for remaining quality issues