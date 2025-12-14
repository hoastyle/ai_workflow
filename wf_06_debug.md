---
command: /wf_06_debug
index: 06
phase: "开发实现"
description: "系统化调试修复，支持快速修复模式 | MCP: --think | --deep"
reads: [PLANNING.md(系统设计), TASK.md(相关任务), KNOWLEDGE.md(已知问题)]
writes: [代码文件, TASK.md(修复记录), KNOWLEDGE.md(新解决方案)]
prev_commands: [/wf_05_code, /wf_07_test]
next_commands: [/wf_07_test, /wf_09_refactor, /wf_11_commit]
model: sonnet
token_budget: medium
mcp_support:
  - name: "Sequential-thinking"
    flag: "--think"
    detail: "结构化分析bug原因和解决方案"
  - name: "Serena"
    flag: "--deep"
    detail: "深度代码分析和符号级调试"
context_rules:
  - "使用KNOWLEDGE.md已知解决方案"
  - "修复根本原因，不是症状"
  - "新模式记录到KNOWLEDGE.md"
---

## 🔌 MCP 增强能力

本命令支持以下 MCP 服务器的可选增强：

### Sequential-thinking (结构化调试)

**启用**: `--think` 标志
**用途**: 复杂错误分析时使用结构化多步推理
**自动激活**: 检测到复杂错误或级联错误

**示例**:
```bash
# 启用结构化调试
/wf_06_debug "数据库连接超时错误" --think

# 组合启用
/wf_06_debug "..." --think --deep
```

**改进点**:
- 错误分解为系统化的分析步骤
- 假设生成和逐步验证
- 多种可能原因的优先级排序
- 基于证据的诊断路径

**输出示例**:
```
Step 1: 症状分析
  - 观察到的错误现象
  - 错误发生频率和条件

Step 2: 假设生成
  - 可能原因 A: 网络问题 (概率: 40%)
  - 可能原因 B: 数据库配置 (概率: 35%)
  - 可能原因 C: 超时设置 (概率: 25%)

Step 3: 验证步骤
  - 对每个假设的具体验证方法
  - 排查优先级和验证顺序

Step 4: 根因定位
  - 基于证据确定根本原因
  - 排除其他可能性的理由

Step 5: 解决方案
  - 针对根因的修复方案
  - 预防再次发生的措施
```

---

### Serena (深度代码理解)

**启用**: `--deep` 标志
**用途**: 语义级别的代码理解和问题定位
**自动激活**: 在 `/wf_06_debug` 命令中自动激活

**示例**:
```bash
# 启用深度代码分析
/wf_06_debug "类型错误" --deep

# 与 --think 组合
/wf_06_debug "性能问题" --think --deep
```

**改进点**:
- 语义级别的代码搜索和理解
- 精确定位错误相关的代码位置
- 识别代码间的依赖关系
- 跨文件的影响分析

**使用场景**:
- 错误涉及多个模块或文件
- 需要理解复杂的调用链
- 定位性能瓶颈
- 识别潜在的副作用

**Serena 工具**:
- `find_symbol`: 定位函数、类、变量定义
- `find_referencing_symbols`: 找到所有引用位置
- `search_for_pattern`: 搜索代码模式
- `get_symbols_overview`: 快速理解文件结构

---

### 组合使用

```bash
# 全面的调试分析
/wf_06_debug "复杂的系统错误" --think --deep

# 输出包含:
# 1. 结构化的错误分析 (Sequential-thinking)
# 2. 精确的代码定位和理解 (Serena)
# 3. 系统化的解决方案
# 4. 完整的验证计划
```

---

### 禁用 MCP

```bash
# 使用传统调试方法，不启用任何 MCP
/wf_06_debug "..." --no-mcp
```

---

### 🔧 MCP Gateway 集成

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Sequential-thinking 工具调用** (--think):
```python
# 检查可用性
if gateway.is_available("sequential-thinking"):
    # 获取工具
    think_tool = gateway.get_tool("sequential-thinking", "sequentialthinking")

    # 调用工具进行结构化调试
    result = think_tool.call(
        thought="分析错误的第一步...",
        thoughtNumber=1,
        totalThoughts=5,
        nextThoughtNeeded=True
    )
else:
    print("⚠️ Sequential-thinking 不可用，使用标准调试分析")
```

**Serena 工具调用** (--deep):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 精确定位错误代码位置
    find_tool = gateway.get_tool("serena", "find_symbol")
    symbol_result = find_tool.call(
        name_path_pattern="error_function_name",
        include_body=True
    )

    # Step 2: 查找所有引用位置
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")
    references = ref_tool.call(
        name_path="error_function_name",
        relative_path="src/module.py"
    )

    # Step 3: 搜索相关代码模式
    search_tool = gateway.get_tool("serena", "search_for_pattern")
    patterns = search_tool.call(
        substring_pattern="error.*handling",
        relative_path="src/"
    )
else:
    print("⚠️ Serena MCP 不可用，使用 Grep/Read 工具")
```

**组合使用示例** (--think --deep):
```python
# 初始化 Gateway
gateway = get_mcp_gateway()

# 检查所有 MCP 可用性
mcp_status = {
    "think": gateway.is_available("sequential-thinking"),
    "deep": gateway.is_available("serena")
}

# 根据可用性组合使用
if mcp_status["think"]:
    # Step 1: 结构化分析错误
    think_tool = gateway.get_tool("sequential-thinking", "sequentialthinking")
    # ...

if mcp_status["deep"]:
    # Step 2: 深度代码定位
    find_tool = gateway.get_tool("serena", "find_symbol")
    # ...
```

**Gateway 优势**:
- ✅ 统一的 MCP 管理接口
- ✅ 自动降级（MCP 不可用时回退到标准工具）
- ✅ 连接池复用（减少多次启动开销）
- ✅ 工具懒加载（按需初始化）

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

⚠️ **AI执行强制规则**: 本命令的执行必须严格遵循以下步骤，不得跳过或随意解释。调试过程必须理解根本原因，而非仅修复症状。

### Step 0.0: 读取执行指南（强制）

**AI必须首先执行此步骤**，读取详细的调试流程文档：

```bash
# 强制执行 - 读取调试工作流指南的关键章节
python ~/.claude/commands/scripts/doc_guard.py \
  --docs "~/.claude/commands/docs/guides/wf_06_debug_workflows.md" \
  --sections '{"~/.claude/commands/docs/guides/wf_06_debug_workflows.md": ["AI执行协议", "模式选择决策树", "执行检查清单"]}'
```

**本步骤为强制性**，确保AI理解：
- 三种调试模式的适用场景和决策树
- 每种模式的标准输出模板
- 必须通过的检查清单项

---

### Step 0.1: Agent 选择和激活 🤖

**目的**: 自动选择合适的 agent 协助调试，提升问题诊断和修复的效率

**执行时机**: 在读取执行指南之后、开始调试分析之前

**Agent 协调流程**:

```python
from commands.lib.agent_coordinator import get_agent_coordinator

# 1. 初始化协调器（单例模式）
coordinator = get_agent_coordinator()

# 2. 拦截命令执行，选择 agent
agent_context = coordinator.intercept(
    task_description=error_description,  # 用户提供的错误描述
    command_name="wf_06_debug",
    auto_activate=True,      # 自动激活高匹配度 agent
    min_confidence=0.85      # 最低置信度阈值（85%）
)

# 3. 显示 agent 信息
print(coordinator.format_agent_info(agent_context, verbose=True))
```

**输出示例**:
```markdown
## 🤖 Agent 协助

**使用 Agent**: Debug Specialist (`debug-agent`)
**匹配度**: 91% 🟢 自动激活
**专长**: 系统化错误诊断, 根因分析, 快速问题修复

**MCP 工具**:
  - Sequential-thinking: 复杂错误的结构化诊断
  - Serena: 精确定位错误代码位置
  - Context7: 查询库/框架的已知问题和解决方案

**建议协作**:
  - sequential: code-agent (修复后实现改进)
  - sequential: test-agent (修复后验证)
```

**Agent 上下文使用**:

如果 agent 成功激活，后续步骤应参考其建议：

```python
if agent_context['auto_activated']:
    agent = agent_context['agent']

    # 1. 参考 agent 的调试重点
    expertise = agent.expertise
    # 例如: ["系统化错误诊断", "根因分析", "快速问题修复"]

    # 2. 调整调试策略
    # debug-agent 可能建议重点关注系统化诊断和根因分析

    # 3. 使用 MCP 工具增强调试
    mcp_hints = agent_context['mcp_hints']
    # 例如: 使用 Sequential-thinking 进行结构化错误分析
```

**降级处理**:

如果未匹配到合适的 agent (匹配度 < 85%)：
- ℹ️ 显示: "未匹配到合适的 agent，使用标准调试流程"
- 继续执行后续步骤，不影响命令功能

**相关文档**: [AgentCoordinator 使用指南](docs/examples/agent_coordinator_usage.md)

---

### Step 0.2: Confidence Check (Pre-Debugging Assessment) 🎯

**目的**: 在开始调试前评估信心水平，避免盲目修复导致更多问题

**执行时机**: 在读取错误信息和 KNOWLEDGE.md 之前执行

**评估维度** (调试特定):

1. **错误清晰度** (Error Clarity)
   - ✅ 错误信息完整，堆栈跟踪清晰 (+30%)
   - ⚠️ 错误信息模糊，需要更多日志 (-10%)
   - ❌ 仅有症状描述，无具体错误信息 (-30%)

2. **根因理解** (Root Cause Understanding)
   - ✅ 有类似问题的解决经验 (+25%)
   - ✅ KNOWLEDGE.md 有相关问题记录 (+20%)
   - ⚠️ 需要逐步诊断 (+5%)
   - ❌ 完全未知的错误类型 (-35%)

3. **修复范围** (Fix Scope)
   - ✅ 修复范围明确，影响有限 (+20%)
   - ⚠️ 可能涉及多个模块 (-5%)
   - ❌ 影响范围不明，可能级联 (-25%)

4. **可测试性** (Testability)
   - ✅ 有明确的验证方法 (+15%)
   - ⚠️ 需要设计验证步骤 (+0%)
   - ❌ 难以复现或验证 (-20%)

5. **回归风险** (Risk of Regression)
   - ✅ 修复不影响其他功能 (+10%)
   - ⚠️ 可能影响相关功能 (-5%)
   - ❌ 高概率引入新问题 (-20%)

**信心水平计算**:
```
基础信心: 50%
最终信心 = 基础信心 + Σ(各维度分数)
```

**决策树**:

```
信心水平 ≥ 90%?
├─ YES → 🟢 直接开始调试
│         - 使用标准调试流程
│         - 预期快速解决
│
├─ 70% ≤ 信心 < 90%?
│  └─ YES → 🟡 建议准备工作
│            - 主要修复方案 + 风险点
│            - 建议: "使用 --think 系统化分析" 或 "使用 --deep 定位根源"
│            - 准备回滚方案（如果修复失败）
│
└─ 信心 < 70%?
   └─ YES → 🔴 暂停并收集信息
            - 停止修复
            - 列出需要收集的信息
            - 建议: "先收集完整日志和堆栈跟踪" 或 "先运行 /wf_04_ask 咨询解决思路"
```

**示例 1: 高信心场景 (93%)**
```
错误: "ImportError: No module named 'requests'"
评估:
- 错误清晰: +30% (明确缺少依赖)
- 根因理解: +25% (常见依赖问题)
- 修复范围: +20% (安装依赖即可)
- 可测试性: +15% (重新运行验证)
- 回归风险: +10% (不影响其他代码)
总信心: 50% + 100% = 150% → Cap at 93%

→ 🟢 直接修复
   预期: 5 分钟内完成
   方案: pip install requests
```

**示例 2: 中等信心场景 (77%)**
```
错误: "Segmentation fault (core dumped)"
评估:
- 错误清晰: -10% (需要更多调试信息)
- 根因理解: +5% (需要逐步诊断)
- 修复范围: -5% (可能涉及内存管理)
- 可测试性: +15% (可以复现)
- 回归风险: -5% (修复可能影响相关功能)
总信心: 50% + 0% = 50% → 调整为 77%

→ 🟡 建议准备
   主要方案: 检查内存访问和指针使用
   风险点: 可能涉及多处代码
   建议: 使用 --deep 定位精确错误位置
   Plan B: 如果修复复杂，考虑代码重构
```

**示例 3: 低信心场景 (38%)**
```
错误: "系统偶尔崩溃，无明确错误信息"
评估:
- 错误清晰: -30% (仅症状，无错误信息)
- 根因理解: -35% (未知错误类型)
- 修复范围: -25% (影响范围不明)
- 可测试性: -20% (难以复现)
- 回归风险: -20% (盲目修复可能引入新问题)
总信心: 50% - 130% = -80% → 底线 38%

→ 🔴 暂停并收集信息
   需要收集:
   1. 完整的系统日志和堆栈跟踪
   2. 崩溃时的环境状态（内存、CPU、进程）
   3. 复现步骤和触发条件
   4. 相关的系统事件记录
   建议: 先运行 /wf_04_ask "如何诊断偶发性系统崩溃？" --research
```

**ROI 分析** (调试特定):
```
Confidence Check 成本: ~120-200 tokens
节省成本 (如果避免错误修复):
  - 避免盲目修复: 8,000-20,000 tokens
  - 避免引入新bug: 30,000-70,000 tokens
  - 避免级联错误: 50,000-150,000 tokens

ROI: 40-750x token 节省
Break-even: 只需避免 1 次错误修复
```

**输出格式**:
```
## 🎯 Debugging Confidence

**信心水平**: 85% 🟡

**评估明细**:
- ✅ 错误清晰度: +30%
- ✅ 根因理解: +25%
- ⚠️ 修复范围: -5%
- ✅ 可测试性: +15%
- ✅ 回归风险: +10%

**决策**: 建议准备工作

**建议**: 使用 --think 系统化分析根本原因，准备回滚方案

**预期**: 需要 20-40 分钟调试和验证
```

---

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

### Standard Debugging Output (Without MCP)
1. **Debug Analysis** – root cause within system context
2. **Fix Implementation** – solution following standards
3. **Knowledge Capture** – new problem-solution patterns for KNOWLEDGE.md
4. **Task Updates** – TASK.md entries for fixes
5. **Prevention Notes** – updates for PLANNING.md
6. **Test Requirements** – validation needed

### Enhanced Output with --think (Sequential-thinking)
**Additional sections when using `--think` flag**:

1. **Structured Error Analysis** – systematic symptom breakdown:
   - Observed error manifestation
   - Error frequency and triggering conditions
   - Initial impact assessment

2. **Hypothesis Generation** – multiple potential causes with probability:
   - Hypothesis A: [Description] (Probability: X%)
   - Hypothesis B: [Description] (Probability: Y%)
   - Hypothesis C: [Description] (Probability: Z%)

3. **Verification Plan** – systematic testing approach:
   - Step-by-step verification for each hypothesis
   - Evidence collection methods
   - Priority-based investigation order

4. **Root Cause Identification** – evidence-based conclusion:
   - Confirmed root cause with supporting evidence
   - Reasons for ruling out alternative hypotheses
   - Confidence level in diagnosis

5. **Solution Design** – comprehensive fix strategy:
   - Immediate fix for the root cause
   - Prevention measures for recurrence
   - Related issues to monitor

### Enhanced Output with --deep (Serena)
**Additional sections when using `--deep` flag**:

1. **Code Location Analysis** – precise error localization:
   - Exact file paths and line numbers
   - Function/method context
   - Symbol definitions involved

2. **Dependency Analysis** – code relationship mapping:
   - Functions/classes calling the error location
   - Functions/classes called from error location
   - Cross-module dependencies

3. **Impact Assessment** – potential side effects:
   - Other code that might be affected by the fix
   - Test files that need attention
   - Documentation that needs updates

4. **Code Pattern Analysis** – similar code locations:
   - Other places with similar patterns
   - Related bugs that might exist
   - Opportunities for systematic fixes

### Combined Output (--think --deep)
When both MCP services are enabled, the output provides:
- **Comprehensive diagnosis** combining structured reasoning and deep code understanding
- **High-confidence root cause** backed by both logical analysis and code evidence
- **Systematic fix strategy** addressing immediate issue and preventing recurrence
- **Complete impact analysis** identifying all affected code areas

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程中的**错误修复环节**：

```
[项目启动] → [任务规划] → [加载上下文] → [架构咨询] → [代码实现] → [测试验证] → [调试修复 ← 当前] → [代码审查] → [提交保存]
  STEP 0       STEP 0.5        STEP 1         STEP 2       STEP 3       STEP 4            STEP 3.5*          STEP 5      STEP 6

* 注：调试修复是在开发过程中动态触发的，可能发生在任何阶段
```

### ✅ 已完成的步骤

执行 `/wf_06_debug` 前，通常已经完成：

- ✅ **代码实现** (STEP 3) - 实现了新功能 (`/wf_05_code`)
  - 或者：测试中发现错误 (`/wf_07_test`)
  - 或者：代码审查时发现问题 (`/wf_08_review`)

### 📝 当前步骤

**正在执行**: `/wf_06_debug <ERROR_DESCRIPTION> [--quick]` (系统化调试修复)

**这个命令的职责**：
- 分析错误的根本原因（而非症状）
- 查阅 KNOWLEDGE.md 中的已知解决方案
- 实施最小化的有效修复
- 在修复后进行验证
- 记录新的问题-解决方案模式
- 更新 TASK.md 和 KNOWLEDGE.md

### ⏭️ 建议下一步

**错误修复完成后**，根据修复的影响范围选择下一步：

#### 路径 1️⃣：快速验证并继续 ⚡
```bash
# 当前: 简单错误已修复，使用 --quick 模式
# 下一步: 快速验证修复

/wf_07_test "验证修复后的功能"

# 如果测试通过，继续开发或审查
/wf_08_review
/wf_11_commit "fix: 修复简单错误"
```
**适用场景**: 使用 `--quick` 快速修复模式，修复的是简单的 bug 或语法错误

#### 路径 2.：完整测试验证修复 ✅
```bash
# 当前: 复杂错误已系统调试，完整修复
# 下一步: 全面验证修复

/wf_07_test "全面测试修复和相关功能"

# 检查是否有新错误
# 如果有新错误: /wf_06_debug "新错误描述" → 重复验证
# 如果测试通过: 进入审查
/wf_08_review "审查调试修复的代码"

# 最后提交
/wf_11_commit "fix: 修复系统性错误"
```
**适用场景**: 修复的是复杂的系统性问题，需要全面测试确保无副作用

#### 路径 3️⃣：错误根源导致需要重构 🔧
```bash
# 当前: 修复过程中发现代码架构需要改进
# 下一步: 进行代码重构

/wf_09_refactor "根据调试发现重构相关代码"

# 重构后验证
/wf_07_test "测试重构后的功能"

# 审查和提交
/wf_08_review
/wf_11_commit "refactor: 改进代码架构，修复错误"
```
**适用场景**: 错误根源暴露了代码设计问题，需要重构而非简单修复

#### 路径 4️⃣：多个连续错误的级联修复 🔄
```bash
# 当前: 修复第一个错误，但发现或导致了新错误
# 下一步: 继续调试新错误

/wf_06_debug "新错误描述"

# 修复后再次验证
/wf_07_test "验证所有修复"

# 完成后进入审查
/wf_08_review
/wf_11_commit "fix: 修复多个级联错误"
```
**适用场景**: 一个错误的修复导致了新错误，需要多轮调试

### 📊 工作流进度提示

当你完成调试修复时，确保输出中包含：

✅ 已完成:
- 清晰的错误分类（依赖、配置、语法、运行时等）
- 根本原因分析
- 修复方案及实施细节
- 修复后的验证结果
- 新的问题-解决方案记录（保存到 KNOWLEDGE.md）
- TASK.md 中的修复记录

⏭️ 下一步提示:
- 建议执行的路径（4个选项之一）
- 是否需要全面测试还是快速验证
- 是否发现了架构问题需要重构
- 预防措施和防止再次发生的方案

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 快速修复简单错误 | 路径 1 | /wf_07_test → /wf_11_commit |
| 修复复杂的系统错误 | 路径 2 | /wf_07_test → /wf_08_review → /wf_11_commit |
| 发现代码设计问题 | 路径 3 | /wf_09_refactor → /wf_07_test → /wf_11_commit |
| 多个级联错误 | 路径 4 | /wf_06_debug (循环) → /wf_07_test → /wf_11_commit |
| 修复过程中出现新错误 | 迭代 | 返回第1步重新分析 |

**何时使用 --quick 标志？**
- 错误是明显的语法或导入错误
- 修复是单行或几行的简单改动
- 对代码架构没有影响
- 团队规模小，修复风险低

**何时需要完整的调试过程？**
- 错误的根本原因不明显
- 涉及多个模块或系统组件
- 有潜在的副作用风险
- 需要学习新的问题模式

---

## ✅ 执行检查清单（AI必须验证）

在输出调试报告前，AI必须确认以下所有项目：

### 通用检查项
- [ ] ✅ 已读取 docs/guides/wf_06_debug_workflows.md 的关键章节
- [ ] ✅ 已执行 Confidence Check 并记录信心水平
- [ ] ✅ 已根据决策树选择正确的调试模式
- [ ] ✅ 已完整阅读错误输出和堆栈跟踪
- [ ] ✅ 理解根本原因（而非仅修复症状）
- [ ] ✅ 输出格式符合对应模式的标准模板
- [ ] ✅ 遵循CLAUDE.md语言规范

### 模式特定检查项

**Quick Fix Mode** (如果使用):
- [ ] ✅ 确认错误属于常见类型
- [ ] ✅ 已验证修复成功（重新运行原始命令）
- [ ] ✅ 提供预防措施

**Standard Debugging** (如果使用):
- [ ] ✅ 已进行系统化分析（Analyzer → Inspector → Checker → Strategist）
- [ ] ✅ 已验证无新错误引入
- [ ] ✅ 已更新相关文档（TASK.md, KNOWLEDGE.md）

**Deep Analysis** (如果使用):
- [ ] ✅ 已收集完整的诊断信息
- [ ] ✅ 已使用结构化推理（如果启用 --think）
- [ ] ✅ 已评估多个解决方案
- [ ] ✅ 已部署监控（如果适用）

**如果任何检查项未通过，必须重新执行对应步骤**

---

## Workflow Integration
- References PLANNING.md for system design
- Leverages KNOWLEDGE.md for past solutions
- Updates TASK.md with debugging work
- Contributes new patterns to KNOWLEDGE.md
- May trigger `/wf_07_test` for validation
- Can lead to `/wf_09_refactor` if needed
- Documents lessons for future debugging sessions
