---
command: /wf_11_commit
index: 11
phase: "运维部署"
description: "Git提交管理，自动更新CONTEXT和格式化"
model: haiku
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
`/wf_11_commit [message]`

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

## Process (4-Stage Simplified Workflow)

### 🔧 Stage 1: Preparation (修复和校验)
**目标**: 清理代码、修复常见问题、校验质量

1. **Pre-Commit Auto-Repair & Validation**:
   - Check git status for changes
   - Identify files for staging
   - **Run enhanced pre-commit hooks with auto-repair**:
     * **Auto-fix Trailing Whitespace**: 100% safe, automatic removal
     * **Auto-fix Line Endings**: Convert CRLF to Unix LF automatically
     * **Auto-fix Markdown Formatting**: Basic formatting improvements
   - Apply language-specific formatting:
     * Python: black formatter
     * JavaScript/TypeScript: prettier
     * C++: clang-format
     * Go: gofmt
     * Other: project-specific formatters
   - **Auto-Update Maintenance Dates**:
     * Update "最后更新" fields to current date: `$(date +%Y-%m-%d)`
     * Preserve historical dates (创建日期、发布日期、决策日期)
   - **Auto-Update Frontmatter Dates**:
     * Update `last_updated` field in all modified docs/ files: `$(date +%Y-%m-%d)`
     * Preserve `created_date` (historical, never modify)
     * Validate `created_date` <= `last_updated` logic

2. **Validation & Error Handling**:
   - **Run enhanced pre-commit validation** on all staged files
   - **Frontmatter Script Dependency Check** (⚠️ NEW):
     ```bash
     if [ ! -f "scripts/frontmatter_utils.py" ]; then
       echo "⚠️ Frontmatter script missing: scripts/frontmatter_utils.py"
       echo "Skipping Frontmatter validation (script not available)"
     else
       python scripts/frontmatter_utils.py validate-batch docs/
     fi
     ```
   - **If validation fails**:
     * Display specific error messages with file:line locations
     * Provide auto-repair suggestions for common issues
     * Offer automated recovery for safe problems (whitespace, line endings)
     * For unsafe problems: pause and require user confirmation to proceed
     * Document failure reason for troubleshooting
   - **If validation passes**: Proceed to Stage 2

---

### 📊 Stage 2: Analysis & Generation (分析和更新)
**目标**: 理解变更内容、生成文档、评估README更新需求

1. **Change Analysis**:
   - Group related changes by file type and scope
   - Identify completed tasks linked to TASK.md
   - Check for excluded files (third-party, generated)
   - Validate code formatting applied successfully
   - **Analyze changes for knowledge extraction opportunities**

2. **README Update Assessment** (if applicable):
   - **Check if changes trigger README update**:
     * New core features (feat commits affecting main files)
     * PLANNING.md architecture changes
     * API/interface modifications
     * Dependency or installation requirement changes
   - **If triggered, generate updated README.md**:
     * Project overview from PLANNING.md
     * Installation requirements from dependencies
     * Feature list from completed TASK.md items
     * Architecture overview from PLANNING.md
   - **Quality validation**: No trailing whitespace, valid markdown, current dates

---

### 💾 Stage 3: Commit & Update (提交和保存)
**目标**: 生成提交、更新上下文、记录完成

1. **Commit Preparation**:
   - Stage formatted files (including README if updated)
   - Generate semantic commit message:
     ```
     [<type>] <subject>

     <body>

     Tasks: #task-id-1, #task-id-2
     Refs: PLANNING.md updates, TASK.md completions
     ```

2. **Context Update** (Pointer Document - Zero Redundancy):
   - Create/update CONTEXT.md as a **pointer document** (NOT content duplication):
     * **Last session timestamp** - When the session ended
     * **Git baseline** - Latest commit hash as reference point
     * **Active task pointer** - Reference to TASK.md section (e.g., "TASK.md § 任务1️⃣ Line 361")
     * **Related architecture pointer** - Reference to PLANNING.md sections (if applicable)
     * **Related ADR pointers** - References to KNOWLEDGE.md ADR entries (if applicable)
     * **Session commits summary** - Count and main change area (e.g., "2 commits, 文档架构优化")
     * **Modified files summary** - Count only (details in Git log)
     * **Next startup recommendation** - Suggested command sequence for /wf_03_prime
   - **IMPORTANT**: Do NOT duplicate content from TASK.md, PLANNING.md, or KNOWLEDGE.md
   - **SSOT Principle**: All content should be pointers or metadata, not duplicated information

3. **Task & Knowledge Updates**:
   - Update TASK.md with completions (following SSOT principles):
     * ✅ Mark task status as [x] completed
     * ✅ Record completion date (Completed: YYYY-MM-DD)
     * ✅ Add Git commits hash references (Git commits: abc1234)
     * ✅ Link related ADR if architectural decision (Related ADR: docs/adr/...)
     * ✅ Keep key metrics if significant (e.g., Token savings: 97.5%)
     * ❌ DO NOT record implementation details (query with `git log [hash]`)
     * ❌ DO NOT duplicate Git commit message content
     * ❌ DO NOT record code line counts, technical minutiae
   - Identify architectural decisions worthy of ADR documentation
   - Detect new problem-solution patterns
   - Suggest KNOWLEDGE.md updates if applicable
   - Document significant changes

---

### 📋 TASK.md Update Format Template

**Recommended format for completed tasks**:
```markdown
- [x] **Task name**
  - Completed: 2025-11-15
  - Priority: High
  - Git commits: abc1234, def5678
  - Related ADR: docs/adr/2025-11-15-decision.md (if applicable)
  - Key metrics: Token savings 97.5% (if significant achievement)
  - Details: `git log abc1234..def5678`
```

**AVOID this redundant format**:
```markdown
❌ - [x] **Task name**
  - Implemented XX class        ← DELETE, check Git log
  - Created XX file             ← DELETE, check Git log
  - Modified XX module          ← DELETE, check Git log
  - Code changes: 534 lines     ← DELETE, check Git log
```

---

### 🚀 Stage 4: Completion & Continuity (完成和延续)
**目标**: 确认提交成功、准备下一步工作

1. **Commit Execution**:
   - Execute git commit with semantic message
   - Verify commit hash and completion

2. **Post-Commit Validation**:
   - Confirm CONTEXT.md updated successfully
   - Verify TASK.md status changes applied
   - Check KNOWLEDGE.md additions if any

3. **Next Steps Guidance**:
   - Display remaining work items from TASK.md
   - Suggest next priority actions
   - Remind: `/clear` → `/wf_03_prime` for session continuity

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

### Stage 1: Preparation Output
1. **Auto-Repair Report** – automatic fixes applied (whitespace, line endings, formatting)
2. **Formatting Report** – language-specific auto-formatting applied
3. **Date Update Report** – maintenance and frontmatter dates synchronized
4. **Validation Report** – quality gate checks, error handling if needed

### Stage 2: Analysis & Generation Output
5. **Change Summary** – grouped files and modifications by scope
6. **README Update Report** – generation details (if triggered)
7. **Knowledge Extraction** – identified patterns and decisions

### Stage 3: Commit & Update Output
8. **Commit Message** – formatted semantic message with task references
9. **Context Update** – CONTEXT.md pointer document refresh (timestamp, Git baseline, task pointers)
10. **Task Updates** – TASK.md completions
11. **Knowledge Updates** – KNOWLEDGE.md suggestions or updates

### Stage 4: Completion Output
12. **Commit Result** – success confirmation with hash
13. **Post-Commit Validation** – CONTEXT/TASK/KNOWLEDGE verification
14. **Next Steps** – remaining work items and recommended actions

## 📌 工作流导航

**在工作流中的位置**:
```
/wf_08_review (代码审查通过)
  ↓
/wf_11_commit (提交保存) ← 当前
  ↓
/wf_02_task update (更新任务状态)
  ↓
/clear (清理上下文)
  ↓
/wf_03_prime (加载上下文，开始下一轮)
```

**工作流集成**:
- ✅ **接收**: 来自 /wf_08_review 的代码审查通过信号
- ✅ **核心价值**: 通过4阶段简化流程，自动化修复、格式化、验证、更新
- ✅ **输出**: Git提交 + CONTEXT.md更新 + TASK.md完成标记
- ✅ **关键特性**:
  - 自动修复尾部空格、行结尾、格式问题（Stage 1）
  - Frontmatter脚本依赖检查，安全地处理缺失情况（Stage 1）
  - 智能README更新，仅当有重要变更时触发（Stage 2）
  - 完整的错误处理和恢复机制（Stage 1-2）
  - 自动更新CONTEXT.md实现会话连续性（Stage 3）
- ✅ **下一步**: `/wf_02_task update` 标记任务完成，或直接 `/clear` 清理上下文

## Workflow Integration
- **Auto-Repair System**: Automatically fixes trailing whitespace, line endings, basic formatting
- **Quality Gates**: Enforced through enhanced pre-commit hooks with validation
- **Error Handling**: Comprehensive validation with clear recovery paths for failures
- **Script Dependencies**: Checks for required tools (e.g., Frontmatter script) before execution
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

## CONTEXT.md Pointer Document Template

**New Format** (Zero Redundancy - SSOT Compliant):
```markdown
# CONTEXT.md

**最后会话**: 2025-11-14 16:45
**Git 基准**: commit 9d99506

## 📍 上下文指针 (Context Pointers)

### 当前工作焦点
- 活跃任务: TASK.md § 任务1️⃣ 完善脚本类型注解 (Line 361)
- 相关架构: PLANNING.md § 技术栈 (待创建)
- 相关 ADR: KNOWLEDGE.md § ADR 2025-11-13 (开源优先)

### 会话状态
- Git commits (本次会话): 2 commits (9d99506, 292a57a)
- 修改文件数: 8 files
- 主要变更领域: 文档架构优化

### 下次启动时
- 推荐命令: /wf_03_prime
- 推荐下一步: 执行 TASK.md § 任务1️⃣ 的推荐命令序列
```

**Key Principles**:
- ✅ All content is **pointers** or **metadata**
- ✅ Zero duplication from TASK.md, PLANNING.md, KNOWLEDGE.md
- ✅ File size target: < 50 lines (vs. 300+ in old format)
- ✅ Single Source of Truth (SSOT) compliant

---

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