---
command: /wf_11_commit
index: 11
phase: "运维部署"
description: "Git提交管理，自动更新CONTEXT和格式化"
reads: [PLANNING.md(标准), TASK.md(任务), 代码更改]
writes: [CONTEXT.md, TASK.md, KNOWLEDGE.md(可能), README.md(可能), Git提交]
prev_commands: [/wf_05_code, /wf_06_debug, /wf_08_review, /wf_09_refactor, /wf_10_optimize]
next_commands: [/wf_02_task, /clear, /wf_03_prime]
model: haiku
token_budget: simple
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "提交前代码完整性验证和符号级变更检查"
docs_dependencies:
  guides:
    - docs/guides/wf_11_commit_workflows.md
  estimated_tokens: 800
  lazy_load: true
  note: "仅在需要深入指导时加载（如质量门控选择、MCP验证流程）"
context_rules:
  - "自动更新CONTEXT.md会话状态"
  - "遵守PLANNING.md质量标准"
  - "重要工作自动更新README.md"
  - "识别新模式添加KNOWLEDGE.md"
---

## 🔌 MCP 增强能力

本命令支持 Serena MCP 服务器的自动增强。

### Serena (代码完整性验证)

**启用**: 自动激活（在 /wf_11_commit 中）
**用途**: 提交前符号级别的代码完整性验证和变更检查
**自动激活**: 检测到代码改动时自动使用 Serena 验证引用完整性

**示例**:
```bash
# 自动激活（检测到符号修改）
/wf_11_commit "refactor: 重命名核心函数"

# 验证代码完整性
/wf_11_commit "feat: 添加新 API 端点"
```

**改进点**:
- 提交前自动检测符号级别的代码改动
- 验证所有符号引用的完整性（100% 覆盖率）
- 识别未完成的重构（遗漏的引用更新）
- 防止提交不一致的代码状态
- 自动发现跨文件的依赖关系

---

### 🔧 MCP Gateway 集成

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Serena 工具调用** (提交前验证):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 识别本次提交中修改的符号
    # 通过 git diff 获取修改的文件列表
    import subprocess

    diff_output = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        capture_output=True,
        text=True
    ).stdout.strip().split('\n')

    modified_files = [f for f in diff_output if f.endswith(('.py', '.ts', '.js'))]

    # Step 2: 对每个修改的文件，检查符号变更
    find_tool = gateway.get_tool("serena", "find_symbol")
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

    integrity_issues = []

    for file_path in modified_files:
        # 获取文件中的所有符号
        overview_tool = gateway.get_tool("serena", "get_symbols_overview")

        symbols = overview_tool.call(
            relative_path=file_path,
            max_answer_chars=-1
        )

        # 对每个符号，检查其引用是否完整
        for symbol in symbols:
            references = ref_tool.call(
                name_path=symbol["name_path"],
                relative_path=file_path
            )

            # 检查是否有未更新的引用
            # （例如：函数签名改变了，但某些调用点还用旧签名）
            for ref in references:
                if not is_reference_updated(ref, symbol):
                    integrity_issues.append({
                        "symbol": symbol["name_path"],
                        "file": file_path,
                        "reference": ref,
                        "issue": "Reference not updated with new signature"
                    })

    # Step 3: 报告完整性问题
    if integrity_issues:
        print("❌ 代码完整性验证失败！")
        print(f"发现 {len(integrity_issues)} 个未更新的引用：")
        for issue in integrity_issues:
            print(f"  - {issue['symbol']} in {issue['file']}")
            print(f"    → {issue['issue']}")
        print("\n💡 建议修复所有引用后再提交")
        exit(1)
    else:
        print("✅ 代码完整性验证通过")
        print(f"检查了 {len(modified_files)} 个文件，所有引用已正确更新")

else:
    print("⚠️ Serena MCP 不可用，跳过符号级完整性检查")
```

**典型场景 1: 函数重命名验证**
```python
# 场景：用户重命名了 getUserData() → fetchUserData()
# 但可能遗漏了某些调用点

if gateway.is_available("serena"):
    # Step 1: 检测重命名的函数
    find_tool = gateway.get_tool("serena", "find_symbol")

    new_function = find_tool.call(
        name_path_pattern="fetchUserData",
        relative_path="src/services/user.ts",
        include_body=False
    )

    if new_function:
        # Step 2: 查找所有引用
        ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

        all_references = ref_tool.call(
            name_path="fetchUserData",
            relative_path="src/services/user.ts"
        )

        # Step 3: 检查是否还有旧名称的残留
        old_function_check = find_tool.call(
            name_path_pattern="getUserData",
            substring_matching=True
        )

        if old_function_check:
            print("❌ 发现未完成的重命名！")
            print(f"旧函数名 'getUserData' 仍在以下位置使用：")
            for old_ref in old_function_check:
                print(f"  - {old_ref['file']}:{old_ref['line']}")
            print("\n💡 建议完成所有重命名后再提交")
            exit(1)
        else:
            print(f"✅ 函数重命名验证通过")
            print(f"   所有 {len(all_references)} 个引用已更新")
```

**典型场景 2: API 签名变更验证**
```python
# 场景：用户修改了 API 方法签名
# authenticate(username, password) → authenticate(credentials: {...})

if gateway.is_available("serena"):
    # Step 1: 获取修改的函数定义
    find_tool = gateway.get_tool("serena", "find_symbol")

    modified_api = find_tool.call(
        name_path_pattern="authenticate",
        relative_path="src/api/auth.ts",
        include_body=True
    )

    # Step 2: 分析函数签名
    # 提取参数列表（简化示例）
    new_signature = extract_signature(modified_api["body"])

    # Step 3: 查找所有调用点
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

    call_sites = ref_tool.call(
        name_path="authenticate",
        relative_path="src/api/auth.ts"
    )

    # Step 4: 验证每个调用点是否使用新签名
    incompatible_calls = []
    for call in call_sites:
        call_signature = extract_call_signature(call["code_snippet"])
        if not is_signature_compatible(call_signature, new_signature):
            incompatible_calls.append(call)

    if incompatible_calls:
        print(f"❌ 发现 {len(incompatible_calls)} 个未更新的 API 调用！")
        for call in incompatible_calls:
            print(f"  - {call['file']}:{call['line']}")
            print(f"    旧调用: {call['code_snippet']}")
        print("\n💡 建议更新所有调用点以匹配新签名")
        exit(1)
    else:
        print(f"✅ API 签名变更验证通过")
        print(f"   所有 {len(call_sites)} 个调用点已更新")
```

**Gateway 优势**:
- ✅ 统一的 MCP 管理接口
- ✅ 自动降级（MCP 不可用时跳过符号检查）
- ✅ 连接池复用（减少多次启动开销）
- ✅ 工具懒加载（按需初始化）
- ✅ 符号级精确验证（准确率 100%）
- ✅ 防止不一致代码提交（错误率从 5-10% → 0%）

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

⚠️ **AI执行强制规则**: 本命令的执行必须严格遵循以下步骤，不得跳过或随意解释。提交前必须通过所有质量门控检查。

### Step 0: 读取执行指南（强制）

**AI必须首先执行此步骤**，读取详细的提交流程文档：

```bash
# 强制执行 - 读取提交工作流指南的关键章节
python ~/.claude/commands/scripts/doc_guard.py \
  --docs "docs/guides/wf_11_commit_workflows.md" \
  --sections '{"docs/guides/wf_11_commit_workflows.md": ["AI执行协议", "4阶段提交流程", "执行检查清单"]}'
```

**本步骤为强制性**，确保AI理解：
- 4阶段提交流程的顺序和要求
- 质量门控的决策逻辑和选择策略
- 必须通过的检查清单项

---

### 🔧 Stage 1: Preparation (修复和校验)
**目标**: 清理代码、修复常见问题、校验质量

1. **Dynamic Pre-Commit Detection & Execution** (NEW):
   - Check git status for changes
   - Identify files for staging
   - **Detect pre-commit configuration**:
     ```bash
     # Step 1.1: Check for .pre-commit-config.yaml
     if [ -f .pre-commit-config.yaml ]; then
       echo "✅ Detected .pre-commit-config.yaml in project"

       # Step 1.2: Check if pre-commit tool is installed
       if command -v pre-commit >/dev/null 2>&1; then
         echo "✅ pre-commit tool is installed"
         echo "🚀 Using project's pre-commit configuration..."

         # Path A: Use pre-commit framework (STAGED FILES ONLY)
         # ⚠️ IMPORTANT: NO --all-files flag allowed
         pre-commit run

         echo "✅ pre-commit hooks executed on staged files"
       else
         echo "⚠️  pre-commit tool NOT installed (despite .pre-commit-config.yaml exists)"
         echo "💡 Install: pip install pre-commit && pre-commit install"
         echo "🔄 Falling back to basic self-managed fixes..."

         # Path B: Fallback to self-managed fixes
         USE_FALLBACK=true
       fi
     else
       echo "ℹ️  No .pre-commit-config.yaml found in project"
       echo "🔄 Using self-managed quality fixes..."

       # Path B: Fallback to self-managed fixes
       USE_FALLBACK=true
     fi
     ```

   - **Path A (Recommended): Use Pre-Commit Framework**:
     * Execute `pre-commit run` (staged files only, NO --all-files)
     * Hooks defined in .pre-commit-config.yaml will handle:
       - Trailing whitespace removal
       - Line ending fixes (CRLF → LF)
       - Markdown formatting
       - File format validation
       - Custom project checks
     * Language-specific formatting (if configured):
       - Python: black formatter
       - JavaScript/TypeScript: prettier
       - C++: clang-format
       - Go: gofmt

   - **Path B (Fallback): Self-Managed Basic Fixes** (when pre-commit unavailable):
     * **Auto-fix Trailing Whitespace**:
       ```bash
       echo "🔧 Removing trailing whitespace..."
       find . -name "*.md" -exec sed -i 's/[[:space:]]*$//' {} \; 2>/dev/null
       ```
     * **Auto-fix Line Endings**:
       ```bash
       echo "🔧 Converting line endings to Unix LF..."
       if command -v dos2unix >/dev/null 2>&1; then
         find . -name "*.md" -exec dos2unix {} \; 2>/dev/null
       else
         find . -name "*.md" -exec sed -i 's/\r$//' {} \; 2>/dev/null
       fi
       ```
     * **Basic Markdown Formatting**:
       ```bash
       echo "🔧 Fixing basic markdown formatting..."
       # Remove excessive blank lines at end of files
       find . -name "*.md" -exec sed -i -e :a -e '/^\n*$/{ $d; N; ba }' {} \; 2>/dev/null
       # Fix header spacing (## Header → ## Header)
       find . -name "*.md" -exec sed -i 's/^##\([^# ]\)/## \1/g' {} \; 2>/dev/null
       ```

   - **Auto-Update Maintenance Dates** (applies to both paths):
     * Update "最后更新" fields to current date: `$(date +%Y-%m-%d)`
     * Preserve historical dates (创建日期、发布日期、决策日期)

   - **Auto-Update Frontmatter Dates** (applies to both paths):
     * Update `last_updated` field in all modified docs/ files: `$(date +%Y-%m-%d)`
     * Preserve `created_date` (historical, never modify)
     * Validate `created_date` <= `last_updated` logic

2. **Validation & Error Handling** (Adaptive to Execution Path):
   - **Path A Validation** (when using pre-commit framework):
     ```bash
     # pre-commit run already performs validation
     # Check exit code to ensure all hooks passed
     if [ $? -eq 0 ]; then
       echo "✅ All pre-commit hooks passed"
     else
       echo "❌ Some pre-commit hooks failed"
       echo "💡 Review the output above for specific issues"
       echo "💡 Fix issues and retry, or use 'git commit --no-verify' to skip (not recommended)"
       exit 1
     fi
     ```

   - **Path B Validation** (when using self-managed fixes):
     * **Basic Quality Checks**:
       ```bash
       echo "🔍 Validating self-managed fixes..."

       # Check for remaining trailing whitespace
       if find . -name "*.md" -exec grep -l " $" {} \; 2>/dev/null | grep -q .; then
         echo "❌ Trailing whitespace still present after fixes"
         exit 1
       fi

       # Check for remaining CRLF line endings
       if find . -name "*.md" -exec file {} \; 2>/dev/null | grep -q CRLF; then
         echo "❌ CRLF line endings still present after fixes"
         exit 1
       fi

       echo "✅ Self-managed quality checks passed"
       ```

   - **Frontmatter Script Dependency Check** (applies to both paths):
     ```bash
     if [ ! -f ~/.claude/commands/scripts/frontmatter_utils.py ]; then
       echo "⚠️  Frontmatter script missing: ~/.claude/commands/scripts/frontmatter_utils.py"
       echo "ℹ️  Skipping Frontmatter validation (script not available)"
     else
       python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/
     fi
     ```

   - **Common Error Handling** (applies to both paths):
     * **If validation fails**:
       - Display specific error messages with file:line locations
       - Provide auto-repair suggestions for common issues
       - Path A: Suggest reviewing pre-commit hook output
       - Path B: Offer automated recovery for safe problems (whitespace, line endings)
       - For unsafe problems: pause and require user confirmation to proceed
       - Document failure reason for troubleshooting
     * **If validation passes**: Proceed to Stage 2

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

### 🔄 Dynamic Detection and Smart Execution (NEW)

**wf_11_commit** now intelligently detects and adapts to your project's setup:

1. **Auto-Detection**:
   - Checks for `.pre-commit-config.yaml` in project root
   - Verifies `pre-commit` tool installation
   - Selects optimal execution path automatically

2. **Execution Paths**:
   - **Path A (Recommended)**: Uses pre-commit framework when available
   - **Path B (Fallback)**: Self-managed fixes when pre-commit unavailable

### Path A: Pre-Commit Framework (Recommended)

**When to use**:
- ✅ `.pre-commit-config.yaml` exists in project
- ✅ `pre-commit` tool is installed (`pip install pre-commit`)

**Behavior**:
```bash
# Automatically executes (STAGED FILES ONLY):
pre-commit run

# ⚠️ IMPORTANT: --all-files flag is NEVER used
# This prevents:
# - Performance issues on large codebases
# - Unexpected modifications to unstaged files
# - Conflicts with partial commits
```

**What it handles** (defined in your .pre-commit-config.yaml):
- ✅ Trailing whitespace removal
- ✅ Line ending fixes (CRLF → LF)
- ✅ Markdown formatting
- ✅ File format validation
- ✅ Custom project-specific checks
- ✅ Language-specific formatting (black, prettier, clang-format, gofmt)

### Path B: Self-Managed Fixes (Fallback)

**When to use**:
- ⚠️ No `.pre-commit-config.yaml` in project
- ⚠️ `pre-commit` tool not installed

**Behavior**:
```bash
# Executes basic quality fixes:
1. Remove trailing whitespace (sed)
2. Convert line endings CRLF → LF (dos2unix or sed)
3. Fix basic markdown formatting (sed)
4. Validate results
```

**Installation Recommendation**:
```bash
# If you see "Falling back to self-managed fixes", consider:
pip install pre-commit
pre-commit install
```

### Installation & Setup (for Path A)

```bash
# Step 1: Install pre-commit framework
pip install pre-commit

# Step 2: Install hooks in your repository (one-time)
pre-commit install

# Step 3: (Optional) Test hooks manually
pre-commit run  # Runs on staged files only
```

### Auto-Repair Capabilities

**Path A (Pre-Commit Framework)**:
- All capabilities defined in `.pre-commit-config.yaml`
- Customizable per project
- Extensible with additional hooks

**Path B (Self-Managed Fallback)**:
- **Trailing Whitespace**: sed-based removal
- **Line Endings**: dos2unix or sed fallback
- **Markdown Formatting**: Basic sed fixes
- **Limited Scope**: Only essential fixes

### Quality Gates Enforced

**Path A**:
- All hooks in `.pre-commit-config.yaml`
- Pre-commit framework's built-in validation
- Custom project-specific checks

**Path B**:
- Basic quality checks (whitespace, line endings)
- Manual validation after self-managed fixes
- Frontmatter validation (if script available)

### Integration Benefits

**Path A (Pre-Commit Framework)**:
- ✅ **Automated Quality Control**: Comprehensive project-specific checks
- ✅ **Instant Fixes**: Auto-repair defined in config
- ✅ **Consistent Standards**: Framework-enforced consistency
- ✅ **Extensible**: Easy to add new hooks
- ✅ **Community Support**: Well-documented, widely adopted

**Path B (Self-Managed Fallback)**:
- ✅ **No Dependencies**: Works without pre-commit installation
- ✅ **Basic Coverage**: Essential quality fixes
- ⚠️ **Limited Scope**: Only fundamental checks
- 💡 **Upgrade Path**: Easy to migrate to Path A later

### Migration from Manual to Pre-Commit

If your project uses self-managed fixes (Path B), consider migrating:

```bash
# 1. Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: trailing-whitespace
        name: Remove Trailing Whitespace
        entry: sed -i 's/[[:space:]]*$//'
        language: system
        files: \.md$
      # Add more hooks as needed
EOF

# 2. Install pre-commit
pip install pre-commit
pre-commit install

# 3. Test
pre-commit run

# 4. wf_11_commit will now auto-detect and use Path A
```

### Key Design Decisions

1. **No --all-files Flag**: Prevents performance issues and unexpected file modifications
2. **Staged Files Only**: Respects partial commits and staged changes
3. **Smart Fallback**: Ensures basic quality even without pre-commit
4. **Clear Feedback**: Shows which path is being used
5. **Zero Breaking Changes**: Existing projects continue to work

---

## ✅ 执行检查清单（AI必须验证）

**在输出最终提交报告前，AI必须确认以下所有项目**：

### Stage 1 检查（Preparation）
- [ ] ✅ 已读取 `docs/guides/wf_11_commit_workflows.md` 的关键章节
- [ ] ✅ 已检测项目的质量门控配置（pre-commit vs self-managed）
- [ ] ✅ 已执行相应的质量修复流程
- [ ] ✅ 已更新所有维护日期为当前日期
- [ ] ✅ 已验证 Frontmatter 格式完整性
- [ ] ✅ 所有质量检查通过（无 trailing whitespace, 正确 line endings）

### Stage 2 检查（Analysis）
- [ ] ✅ 已分析变更影响范围（代码/文档/配置）
- [ ] ✅ 已确定文档更新需求（README/KNOWLEDGE/PLANNING）
- [ ] ✅ 如使用 Serena MCP，已执行符号完整性检查
- [ ] ✅ 已识别新的设计模式或解决方案（如适用）

### Stage 3 检查（Commit）
- [ ] ✅ 已生成语义化提交消息（[type] subject 格式）
- [ ] ✅ 提交消息包含 Co-Authored-By 签名
- [ ] ✅ 已成功执行 `git commit`
- [ ] ✅ 已验证提交哈希和内容

### Stage 4 检查（Finalization）
- [ ] ✅ 已按指针文档模式更新 CONTEXT.md（~50行，无冗余）
- [ ] ✅ CONTEXT.md 包含正确的 git 基准和会话状态
- [ ] ✅ 已基于 TASK.md 提供下一步建议
- [ ] ✅ 已更新相关文档（README/KNOWLEDGE，如适用）

### 输出格式检查
- [ ] ✅ 使用了工作流指南提供的标准输出模板
- [ ] ✅ 提交报告包含完整的4阶段执行总结
- [ ] ✅ 提供了明确的后续工作建议
- [ ] ✅ 错误和警告都有清晰的解决方案

### 质量验证检查
- [ ] ✅ 所有文件无 trailing whitespace
- [ ] ✅ 所有文件使用统一的 line endings (LF)
- [ ] ✅ Markdown 格式符合项目标准
- [ ] ✅ Git 仓库状态clean（无未提交的临时更改）

### MCP 使用检查（如适用）
- [ ] ✅ Serena MCP 用于符号完整性验证（如可用）
- [ ] ✅ 代码重构的引用完整性已验证
- [ ] ✅ 如 MCP 不可用，已使用标准工具替代

**如果任何检查项未通过，必须重新执行对应阶段**
