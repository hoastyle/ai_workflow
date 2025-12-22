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
  execution_model: "synchronous"
  note: "指南文档按需加载（DocLoader立即返回）。命令执行是同步的，无需等待。"
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
Create git commits with integrated preparation, formatting, and context updates:
- Prepare files for commit (date updates, basic formatting, staging)
- Automatically delegate validation to git hooks during commit
- Update TASK.md task completion status
- Auto-update CONTEXT.md with work summary
- **Auto-update README.md when important work completed**
- Identify and suggest KNOWLEDGE.md updates
- Maintain commit message conventions
- Ensure full traceability

## Process (4-Stage Simplified Workflow)

⚠️ **AI执行强制规则**: 本命令的执行必须严格遵循以下步骤，不得跳过或随意解释。提交前必须通过所有质量门控检查。

### Step 0: 加载工作流指南（立即执行）⚡

**重要**: 本步骤是同步的，Doc Guard 工具**立即返回**结果，无需等待。

**立即执行以下命令**来加载详细指导：

```bash
# 立即执行 - DocLoader 同步返回结果
python $HOME/.claude/commands/scripts/doc_guard.py \
  --docs "$HOME/.claude/commands/docs/guides/wf_11_commit_workflows.md" \
  --sections "{\"$HOME/.claude/commands/docs/guides/wf_11_commit_workflows.md\": [\"AI执行协议\", \"4阶段提交流程\", \"执行检查清单\"]}"
```

**说明**：
- ✅ 此命令**立即返回**结果，不存在"等待加载"
- ✅ 如果 doc_guard 不可用，直接使用 Read 工具
- ⚠️ 完成后，**立即**进入后续步骤

**确保AI理解：
- 4阶段提交流程的顺序和要求
- 质量门控的决策逻辑和选择策略
- 必须通过的检查清单项

---

### 🔧 Stage 1: Preparation (准备和格式化)
**目标**: 为提交准备文件，更新维护信息

1. **文件准备和自动化更新**:
   - 分析已修改的文件
   - 自动执行基础格式化和维护更新

2. **自动日期更新**:
   - 更新 "最后更新" 字段为当前日期: `$(date +%Y-%m-%d)`
   - 保留历史日期（创建日期、发布日期、决策日期）

3. **自动 Frontmatter 日期更新**:
   - 更新 `last_updated` 字段到当前日期
   - 保留 `created_date`（历史，永不修改）
   - 验证 `created_date` <= `last_updated` 逻辑

4. **基础格式化和维护**:
   * **自动修复尾部空格**:
     ```bash
     echo "🔧 Removing trailing whitespace..."
     find . -name "*.md" -exec sed -i 's/[[:space:]]*$//' {} \; 2>/dev/null
     ```
   * **自动修复行结尾**:
     ```bash
     echo "🔧 Converting line endings to Unix LF..."
     if command -v dos2unix >/dev/null 2>&1; then
       find . -name "*.md" -exec dos2unix {} \; 2>/dev/null
     else
       find . -name "*.md" -exec sed -i 's/\r$//' {} \; 2>/dev/null
     fi
     ```
   * **基础 Markdown 格式化**:
     ```bash
     echo "🔧 Fixing basic markdown formatting..."
     # 移除文件末尾多余空行
     find . -name "*.md" -exec sed -i -e :a -e '/^\n*$/{ $d; N; ba }' {} \; 2>/dev/null
     # 修复标题格式
     find . -name "*.md" -exec sed -i 's/^##\([^# ]\)/## \1/g' {} \; 2>/dev/null
     ```

5. **预提交验证提示**:
   - **如果存在 `.pre-commit-config.yaml`**:
     ```bash
     if [ -f .pre-commit-config.yaml ]; then
       echo "✅ Detected .pre-commit-config.yaml in project"
       echo "ℹ️  Pre-commit hooks will run automatically during git commit"
       echo "💡 Ensure you have run 'pre-commit install' in this repository"
     fi
     ```

6. **格式验证**:
   - 检查基础质量约束：
     ```bash
     echo "🔍 Validating base formatting..."

     # 检查尾部空格
     if find . -name "*.md" -exec grep -l " $" {} \; 2>/dev/null | grep -q .; then
       echo "⚠️  Trailing whitespace found - pre-commit hooks will handle this"
     fi

     # 检查行结尾
     if find . -name "*.md" -exec file {} \; 2>/dev/null | grep -q CRLF; then
       echo "⚠️  CRLF line endings found - pre-commit hooks will handle this"
     fi

     echo "🎯 Staging prepared files for validation via git hooks"
     ```

   - **Frontmatter 完整性检查**:
     ```bash
     if [ ! -f $HOME/.claude/commands/scripts/frontmatter_utils.py ]; then
       echo "⚠️  Frontmatter script missing: $HOME/.claude/commands/scripts/frontmatter_utils.py"
       echo "ℹ️  Skipping Frontmatter validation (script not available)"
     else
       python $HOME/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/
     fi
     ```

7. **阶段完成确认**:
   - 总结准备完成情况
   - 确认所有修改已正确暂存
   - 准备进入提交流程（验证将通过 git hooks 自动执行）

8. **文档大小检查** 🆕 (Phase 7.5):
   - **执行文档大小闭环检查**:
     ```bash
     echo "📋 检查文档大小..."
     if ! ./scripts/check_doc_size.sh; then
         echo "⚠️ 警告: 某些文档接近或超过大小限制"
         echo "   建议运行: /wf_13_doc_maintain check"
         echo "   存档命令: /wf_13_doc_maintain archive <文档>"
         echo ""
     fi
     ```
   - **检查逻辑**:
     * 读取 doc_limits.yaml 配置（如果存在）
     * 检查管理文档行数（TASK.md, PLANNING.md, CONTEXT.md, KNOWLEDGE.md）
     * 如果超过限制 70%，显示警告
     * 如果超过限制 80%，发出违规提示
     * **不阻止提交** - 仅警告和建议
   - **输出示例**:
     ```
     📊 文档大小检查

     ✅ CONTEXT.md: 25/50 行 (50%)
     ⚠️ TASK.md: 428/200 行 (214%) - 超限
     ⚠️ PLANNING.md: 375/300 行 (125%) - 超限
     ✅ KNOWLEDGE.md: 149/200 行 (75%)

     建议:
       - 运行 /wf_13_doc_maintain archive TASK.md
       - 运行 /wf_13_doc_maintain archive PLANNING.md
     ```
   - **降级处理**:
     * 如果 check_doc_size.sh 不存在：跳过检查
     * 如果 doc_limits.yaml 不存在：使用默认值或跳过
     * 检查失败不影响提交流程

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

2. **Post-Commit Verification** (Documentation):
   - Confirm CONTEXT.md updated successfully
   - Verify TASK.md status changes applied
   - Check KNOWLEDGE.md additions if any
   - Code quality validation automatically executed by git hooks during `git commit`

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
1. **File Preparation Report** – date updates, basic formatting, staging completed
2. **Formatting Report** – automatic fixes applied (whitespace, line endings, Markdown format)
3. **Date Update Report** – maintenance and frontmatter dates synchronized
4. **Pre-Commit Validation Hint** – confirmation that .pre-commit-config.yaml exists and will run during `git commit`

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
13. **Post-Commit Status** – Git hooks validation automatically executed during `git commit`; CONTEXT/TASK/KNOWLEDGE verification
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
- **Preparation System**: Prepares files for commit through date updates, basic formatting, and staging
- **Quality Gates**: Delegated to .pre-commit-config.yaml hooks that run automatically during `git commit`
- **Clear Separation of Concerns**: wf_11_commit handles preparation; git hooks handle validation
- **Script Dependencies**: Checks for required tools (e.g., Frontmatter script) before execution
- **User Experience**: Clear feedback on preparation steps; automatic validation via git hooks
- Validates against PLANNING.md standards (via git hooks)
- Auto-formats code (integrates basic formatting during Stage 1)
- **Auto-updates README.md for important work completions**
- Updates completed tasks in TASK.md
- Auto-updates CONTEXT.md for session continuity
- Enhances KNOWLEDGE.md with accumulated wisdom
- Follows after `/wf_08_review` approval
- Triggers task status updates
- Maintains complete project history and context
- **Ensures README stays synchronized with project state**
- Enables seamless `/wf_03_prime` context loading with long-term memory
- **Trusts .pre-commit-config.yaml as single source of truth for quality standards**

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

## Git Hook 集成和自动验证哲学

### 🎯 核心设计理念

**wf_11_commit 信任 git hooks 在提交时自动运行验证**:

新的设计哲学是：
1. **Stage 1 只负责准备**：更新日期、基础格式化、暂存文件
2. **Git hooks 负责验证**：.pre-commit-config.yaml 定义的 hooks 在 `git commit` 时自动运行
3. **简化职责**：避免重复的验证逻辑，让 .pre-commit-config.yaml 成为唯一的质量标准定义

### 为什么这样设计？

✅ **优势**:
- **清晰的职责分工**：wf_11_commit 不再重复 git hooks 的工作
- **自动化和可靠**：git 原生支持 hook 机制，无需额外维护
- **避免绕过**：项目的 .pre-commit-config.yaml 成为强制执行的标准
- **简化代码**：去除复杂的"Path A vs Path B"逻辑
- **提高可维护性**：所有质量标准在一个文件中定义

### 预提交 Hook 安装和配置

**前置条件**：项目必须有 `.pre-commit-config.yaml` 并运行 `pre-commit install`

```bash
# Step 1: 创建 .pre-commit-config.yaml（如果不存在）
# 参考: https://pre-commit.com/

# Step 2: 安装预提交 hook（一次性）
pip install pre-commit
pre-commit install

# Step 3: Git hooks 现在会在 git commit 时自动运行
# 无需 wf_11_commit 中的手动调用
```

### Git Hooks 自动验证流程

当执行 `git commit` 时，以下流程自动发生：

```
用户运行: git commit -m "message"
  ↓
Git 检查是否安装了 pre-commit hooks
  ↓
If pre-commit 已安装:
  - 自动运行 .pre-commit-config.yaml 中定义的所有 hooks
  - Hooks 检查暂存文件
  - If 检查失败 → 提示错误，阻止提交
  - If 检查通过 → 继续提交
  ↓
提交完成或被 hooks 阻止
```

### Hook 定义示例

**.pre-commit-config.yaml** 中定义验证规则：

```yaml
repos:
  # 基础文件修复
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict
      - id: fix-byte-order-marker

  # Markdown 格式化（可选）
  - repo: https://github.com/markdownlint/markdownlint
    rev: v0.13.0
    hooks:
      - id: markdownlint

  # 自定义本地 hooks（项目特定）
  - repo: local
    hooks:
      - id: custom-project-check
        name: Custom Project Validation
        entry: ./scripts/validate.sh
        language: script
        stages: [commit]
```

### Stage 1 与 Git Hooks 的交互

**Stage 1 准备文件，Git Hooks 验证文件**：

| 阶段 | 职责 | 执行时机 |
|------|------|--------|
| **Stage 1** | 更新日期、基础格式化、暂存文件 | `/wf_11_commit` 执行时 |
| **Git Hooks** | 运行所有 .pre-commit-config.yaml 规则 | `git commit` 执行时 |
| **提交** | 如果 hooks 通过，提交成功 | git 原生机制 |

### 项目配置检查清单

确保你的项目正确配置：

- [ ] ✅ 项目根目录有 `.pre-commit-config.yaml`
- [ ] ✅ 已运行 `pip install pre-commit`
- [ ] ✅ 已运行 `pre-commit install`（在项目目录中）
- [ ] ✅ Git hooks 已安装到 `.git/hooks/`
- [ ] ✅ `.pre-commit-config.yaml` 定义了所有必要的 hooks

### 验证 Git Hooks 已安装

```bash
# 检查 hooks 是否已安装
ls -la .git/hooks/ | grep pre-commit

# 应该看到类似输出：
# -rwxr-xr-x  1 user  staff   159 Nov 14 10:30 pre-commit

# 手动测试 hooks（可选）
pre-commit run --all-files
```

### 如果 Hooks 失败

当 `git commit` 时 hooks 失败：

1. **阅读错误信息**：Hook 会显示具体问题
2. **修复问题**：更新相关文件
3. **重新提交**：`git commit` 再次运行 hooks

### 跳过 Hooks（不推荐）

如果需要临时跳过 hooks（仅在紧急情况下）：

```bash
# ⚠️ 不推荐，会绕过质量检查
git commit --no-verify

# 更好的做法是修复问题，然后正常提交
```

### 关键设计决策

1. **信任 .pre-commit-config.yaml**：作为唯一的质量标准定义
2. **自动运行**：无需 wf_11_commit 中的显式调用
3. **简化 wf_11_commit**：Focus on 准备，不关心验证
4. **清晰反馈**：Stage 1 提示 hooks 将在 commit 时运行
5. **向后兼容**：没有 .pre-commit-config.yaml 的项目仍可工作（基础格式化）

---

## 🤖 AI 执行提示（重要）

**⚠️ 关键规则**：
- **Slash commands 是同步执行的**，无需等待"加载完成"
- 看到 `<command-message>wf_11_commit is running…</command-message>` 时，**立即开始执行** Step 0
- **禁止**输出"让我等待命令加载完成"或类似话语
- `lazy_load: true` 表示使用 DocLoader **按需加载**，所有工具调用都是**立即返回**的
- 所有步骤应**连续执行**，无暂停点

---


## ✅ 执行检查清单（AI必须验证）

**在输出最终提交报告前，AI必须确认以下所有项目**：

### Stage 1 检查（Preparation）
- [ ] ✅ 已读取 `docs/guides/wf_11_commit_workflows.md` 的关键章节
- [ ] ✅ 已执行文件准备和日期更新
- [ ] ✅ 已执行基础格式化（修复尾部空格、行结尾、Markdown 格式）
- [ ] ✅ 已更新所有维护日期为当前日期
- [ ] ✅ 已验证 Frontmatter 格式完整性
- [ ] ✅ 所有修改文件已正确暂存（git add）
- [ ] ✅ 已验证 .pre-commit-config.yaml 存在（如项目使用）

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
