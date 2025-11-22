---
command: /wf_06_debug
index: 06
phase: "开发实现"
description: "系统化调试修复，支持快速修复模式"
reads: [PLANNING.md(系统设计), TASK.md(相关任务), KNOWLEDGE.md(已知问题)]
writes: [代码文件, TASK.md(修复记录), KNOWLEDGE.md(新解决方案)]
prev_commands: [/wf_05_code, /wf_07_test]
next_commands: [/wf_07_test, /wf_09_refactor, /wf_11_commit]
model: sonnet
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

## Workflow Integration
- References PLANNING.md for system design
- Leverages KNOWLEDGE.md for past solutions
- Updates TASK.md with debugging work
- Contributes new patterns to KNOWLEDGE.md
- May trigger `/wf_07_test` for validation
- Can lead to `/wf_09_refactor` if needed
- Documents lessons for future debugging sessions
