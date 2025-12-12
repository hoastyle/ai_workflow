---
command: /wf_07_test
index: 07
phase: "质量保证"
description: "测试开发和覆盖率分析，支持coverage模式"
reads: [PLANNING.md(测试策略), TASK.md(测试任务), 代码文件]
writes: [测试文件, TASK.md(测试状态), 覆盖率报告]
prev_commands: [/wf_05_code, /wf_06_debug, /wf_09_refactor]
next_commands: [/wf_08_review, /wf_09_refactor, /wf_11_commit]
model: sonnet
token_budget: medium
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "代码覆盖率分析和测试生成"
  - name: "Sequential-thinking"
    flag: "--think"
    detail: "结构化测试策略分析"
context_rules:
  - "遵循PLANNING.md测试策略"
  - "满足PRD覆盖率要求"
  - "--coverage模式分析测试覆盖率"
---

## 🔌 MCP 增强能力

本命令支持以下 MCP 服务器的可选增强：

### Serena (深度代码理解)

**启用**: 自动激活（在 /wf_07_test 中）
**用途**: 语义级别的代码理解和测试生成

**改进点**:
- 精确定位需要测试的函数和类
- 自动识别代码依赖关系
- 生成针对性强的测试用例
- 分析代码覆盖率缺口

**使用场景**:
- 为复杂函数生成测试
- 识别未测试的代码路径
- 理解函数调用关系以生成集成测试

### Sequential-thinking (结构化测试策略)

**启用**: `--think` 标志（可选）
**用途**: 结构化多步推理分析测试策略

**示例**:
```bash
# 启用结构化测试策略
/wf_07_test "复杂组件" --think

# 组合启用
/wf_07_test "..." --think --coverage
```

**改进点**:
- 系统化分解测试需求
- 优先级排序测试用例
- 覆盖率提升策略规划
- 测试场景全面性分析

**输出示例**:
```
Step 1: 测试需求分析
  - 识别核心功能和边界条件
  - 列出潜在的失败场景

Step 2: 测试用例设计
  - 正常路径测试
  - 异常路径测试
  - 边界条件测试

Step 3: 优先级排序
  - 关键功能优先
  - 高风险场景优先
  - 覆盖率缺口优先

Step 4: 实施计划
  - 单元测试生成
  - 集成测试设计
  - 验证策略
```

---

### 禁用 MCP

```bash
# 使用传统测试方法，不启用任何 MCP
/wf_07_test "..." --no-mcp
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

**Serena 工具调用** (自动启用):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 定位需要测试的函数
    find_tool = gateway.get_tool("serena", "find_symbol")

    target_function = find_tool.call(
        name_path_pattern="target_function_name",
        include_body=True
    )

    # Step 2: 查找函数的所有引用
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

    references = ref_tool.call(
        name_path="target_function_name",
        relative_path="src/module.py"
    )

    # Step 3: 分析依赖关系生成测试
    # 基于函数体和引用关系设计测试用例

else:
    print("⚠️ Serena MCP 不可用，使用传统 Grep/Read 工具")
```

**Sequential-thinking 工具调用** (--think):
```python
# 检查可用性
if gateway.is_available("sequential-thinking"):
    # 获取工具
    think_tool = gateway.get_tool("sequential-thinking", "sequentialthinking")

    # 调用工具进行结构化测试策略
    result = think_tool.call(
        thought="分析测试需求的第一步...",
        thoughtNumber=1,
        totalThoughts=5,
        nextThoughtNeeded=True
    )
else:
    print("⚠️ Sequential-thinking 不可用，使用标准测试策略")
```

**组合使用示例** (--think + Serena):
```python
# 初始化 Gateway
gateway = get_mcp_gateway()

# 检查所有 MCP 可用性
mcp_status = {
    "think": gateway.is_available("sequential-thinking"),
    "serena": gateway.is_available("serena")
}

# 根据可用性组合使用
if mcp_status["think"]:
    # Step 1: 结构化分析测试策略
    think_tool = gateway.get_tool("sequential-thinking", "sequentialthinking")
    # ...

if mcp_status["serena"]:
    # Step 2: 精确定位测试目标
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
**输入**: PLANNING.md测试策略 + 代码实现
**输出**: 测试代码 + 覆盖率报告 + TASK.md更新
**依赖链**: /wf_05_code → **当前（测试开发）** → /wf_08_review → /wf_11_commit

## Usage
`/wf_07_test <COMPONENT_OR_FEATURE> [--coverage]`

## Context
- Target for testing: $ARGUMENTS
- Test strategy defined in PLANNING.md
- Test tasks tracked in TASK.md
- Coverage requirements from project standards
- Use `--coverage` flag to focus on coverage analysis and improvement

## Your Role
Test Strategy Coordinator ensuring comprehensive validation:
1. **Test Architect** – designs tests per PLANNING.md strategy
2. **Unit Test Specialist** – creates tests following project patterns
3. **Integration Engineer** – validates system interactions
4. **Quality Validator** – ensures coverage meets requirements

## Process

### Standard Testing (default)
1. **Test Planning**:
   - Review testing strategy in PLANNING.md
   - Check TASK.md for test requirements
   - Identify coverage gaps

2. **Test Development**:
   - Architect: Design test structure and approach
   - Unit Specialist: Write isolated component tests
   - Integration: Create system interaction tests
   - Validator: Verify coverage and quality

3. **Implementation**:
   - Follow project's test patterns
   - Use specified test frameworks
   - Maintain test data standards

4. **Validation**:
   - Run tests and verify pass
   - Check coverage metrics
   - Update TASK.md status

### Coverage Analysis Mode (--coverage flag)
1. **Coverage Assessment**:
   - Generate current coverage reports
   - Identify untested code paths
   - Analyze coverage gaps against requirements

2. **Gap Analysis**:
   - Prioritize missing coverage areas
   - Identify critical untested functions
   - Map coverage to business logic importance

3. **Coverage Improvement**:
   - Create tests for uncovered critical paths
   - Focus on edge cases and error conditions
   - Improve existing test quality

4. **Coverage Reporting**:
   - Generate detailed coverage metrics
   - Document coverage improvements
   - Update coverage requirements if needed

## Output Format

### Standard Testing Output
1. **Test Strategy** – approach aligned with project
2. **Test Implementation** – concrete test code
3. **Coverage Report** – basic metrics against requirements
4. **Task Updates** – TASK.md test completions
5. **Next Steps** – remaining test work

### Coverage Analysis Output (--coverage flag)
1. **Coverage Summary** – current coverage statistics
2. **Gap Analysis** – detailed uncovered areas
3. **Priority Recommendations** – critical missing tests
4. **Improvement Plan** – tests to add for better coverage
5. **Coverage Trends** – comparison with previous runs

## Workflow Integration
- Follows PLANNING.md test strategy
- Updates test tasks in TASK.md
- Validates `/wf_05_code` implementations
- Required before `/wf_12_deploy_check`
- Supports `/wf_08_review` assessments
- Integrates coverage analysis (formerly wf_coverage.md functionality)
- Coverage reports inform `/wf_09_refactor` decisions

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[任务确认] → [架构咨询] → [代码实现] → [测试验证 ← 当前] → [代码审查] → [提交保存]
   STEP 1      STEP 2 (可选)   STEP 3        STEP 4          STEP 5     STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_07_test` 前，你应该已经完成：

1. ✅ **任务确认** (`/wf_02_task update`)
2. ✅ **架构咨询**（可选，`/wf_04_ask`）
3. ✅ **代码实现** (`/wf_05_code`)

### 📝 当前步骤

**正在执行**: `/wf_07_test "组件或功能名称" [--coverage]`

**模式说明**：
- **标准模式**（默认）：编写和运行单元测试
- **覆盖率模式**（`--coverage`）：分析测试覆盖率并生成报告

### ⏭️ 建议下一步

**测试完成后**，建议按以下顺序执行：

#### 路径 1：测试通过 ✅
```bash
# 第5步: 代码审查
/wf_08_review

# 第6步: 提交保存进度
/wf_11_commit "test: 为 [功能] 添加测试"
```

#### 路径 2：测试发现问题 🐛
```bash
# 回到代码实现修改代码
/wf_05_code "修复失败的测试"

# 重新运行测试
/wf_07_test "[相同功能]"

# 然后继续审查和提交
/wf_08_review
/wf_11_commit "test: [功能] - 修复失败测试"
```

#### 路径 3：覆盖率不达标 📊
```bash
# 使用覆盖率模式分析
/wf_07_test "[功能]" --coverage

# 根据报告添加缺失测试
/wf_07_test "[功能] - 增加覆盖率"

# 覆盖率达标后继续
/wf_08_review
/wf_11_commit "test: 提升 [功能] 覆盖率"
```

### 📊 工作流进度提示

当你完成测试时，确保输出中包含：

✅ 已完成:
- 所有测试通过 ✓
- 覆盖率达标（如有要求）
- TASK.md 已更新

⏭️ 下一步提示:
- 如果覆盖率不达标，说明需要添加更多测试
- 如果所有测试通过，准备进入代码审查
- 显示推荐的下一个命令

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 所有测试通过 | 路径 1 | /wf_08_review → /wf_11_commit |
| 测试失败 | 路径 2 | /wf_05_code → /wf_07_test → /wf_08_review |
| 覆盖率不达标 | 路径 3 | /wf_07_test --coverage → 添加测试 → /wf_08_review |
| 需要覆盖率分析 | 分析模式 | /wf_07_test "[功能]" --coverage |
| 不确定 | 咨询 | /wf_04_ask "测试策略是否完善？" |

### 🔄 回到上一步

如果测试发现设计缺陷：
```bash
/wf_04_ask "测试发现的设计问题..."
# 修改代码或测试后重新运行此命令
```

### 📚 相关文档

- **工作流指南**: WORKFLOWS.md
- **测试策略**: PLANNING.md (Testing Strategy)
- **任务追踪**: TASK.md
- **代码质量**: PLANNING.md (Code Quality)
