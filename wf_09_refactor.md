---
command: /wf_09_refactor
index: 09
phase: "质量保证"
description: "代码重构服务，保持架构一致性"
reads: [PLANNING.md(架构设计), TASK.md(技术债), KNOWLEDGE.md(代码模式)]
writes: [代码文件, TASK.md(重构完成), PLANNING.md(可能)]
prev_commands: [/wf_08_review]
next_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
model: sonnet
token_budget: medium
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "符号级别代码重构和依赖分析"
context_rules:
  - "对齐PLANNING.md架构"
  - "应用KNOWLEDGE.md最佳实践"
  - "保持PRD功能不变"
  - "✅ 自动激活 Serena MCP 用于符号级操作（rename_symbol等）"
---

## 执行上下文
**输入**: PLANNING.md架构 + TASK.md技术债 + KNOWLEDGE.md模式
**输出**: 重构代码 + TASK.md更新 + 可能的PLANNING.md改进
**依赖链**: /wf_08_review → **当前（代码重构）** → /wf_07_test (回归)

## Usage
`/wf_09_refactor <REFACTOR_SCOPE>`

**Serena MCP 集成** (⭐ 自动激活):
- 重构命令自动启用 Serena MCP，用于精确的符号级操作
- 对于涉及重命名、移动、提取等符号操作的重构，Serena 会：
  - `find_symbol()` - 精确定位符号位置
  - `rename_symbol()` - 自动重命名所有引用（消除遗漏）
  - `find_referencing_symbols()` - 验证所有调用点已更新

## Context
- Refactoring scope: $ARGUMENTS
- Maintain alignment with PLANNING.md architecture
- Track refactoring in TASK.md
- Preserve functionality while improving structure
- **Serena MCP Integration**: Automatically enabled for symbol-level operations

## Your Role
Refactoring Coordinator ensuring project consistency:
1. **Structure Analyst** – evaluates against planned architecture
2. **Code Surgeon** – transforms per project patterns
3. **Pattern Expert** – applies patterns from PLANNING.md
4. **Quality Validator** – ensures standards compliance

## Process

### Step 0.1: Agent 选择和激活 🤖 **[强制执行]**

⚠️ **AI 强制规则**: 此步骤**必须实际执行**，不得跳过或视为示例

**目的**:{1}

**执行时机**:{2}

**执行要求**:
1. ✅ 必须实际调用 `get_agent_coordinator().intercept()`
2. ✅ 必须输出 agent 信息（使用 `format_agent_info()`）
3. ✅ 如果跳过此步骤，视为执行协议违规

**执行代码** (必须运行):

```bash
python -c "
from commands.lib.agent_coordinator import get_agent_coordinator

coordinator = get_agent_coordinator()
agent_context = coordinator.intercept(
    task_description='代码重构和优化',
    command_name='wf_09_refactor',
    auto_activate=True,
    min_confidence=0.85
)
print(coordinator.format_agent_info(agent_context, verbose=True))
"
```

**Agent 协调流程**:

```python
from commands.lib.agent_coordinator import get_agent_coordinator

# 1. 初始化协调器（单例模式）
coordinator = get_agent_coordinator()

# 2. 拦截命令执行，选择 agent
agent_context = coordinator.intercept(
    task_description=refactor_target,  # 用户提供的重构目标
    command_name="wf_09_refactor",
    auto_activate=True,      # 自动激活高匹配度 agent
    min_confidence=0.85      # 最低置信度阈值（85%）
)

# 3. 显示 agent 信息
print(coordinator.format_agent_info(agent_context, verbose=True))
```

**输出示例**:
```markdown
## 🤖 Agent 协助

**使用 Agent**: Refactoring Specialist (`refactor-agent`)
**匹配度**: 90% 🟢 自动激活
**专长**: 代码重构和优化, 设计模式应用, 架构改进

**MCP 工具**:
  - Serena: 符号级精确重构（find_symbol, rename_symbol, find_referencing_symbols）
  - Sequential-thinking: 系统化重构策略规划
  - Context7: 查询重构最佳实践

**建议协作**:
  - sequential: test-agent (重构后验证)
  - sequential: review-agent (重构质量审查)
```

**Agent 上下文使用**:

如果 agent 成功激活，后续步骤应参考其建议：

```python
if agent_context['auto_activated']:
    agent = agent_context['agent']

    # 1. 参考 agent 的重构重点
    expertise = agent.expertise
    # 例如: ["代码重构和优化", "设计模式应用", "架构改进"]

    # 2. 调整重构策略
    # refactor-agent 可能建议重点关注代码结构和可维护性

    # 3. 使用 MCP 工具增强重构
    mcp_hints = agent_context['mcp_hints']
    # 例如: 使用 Serena 进行符号级精确重构
```

**降级处理**:

如果未匹配到合适的 agent (匹配度 < 85%)：
- ℹ️ 显示: "未匹配到合适的 agent，使用标准重构流程"
- 继续执行后续步骤，不影响命令功能

**相关文档**: [AgentCoordinator 使用指南](docs/examples/agent_coordinator_usage.md)

---

### Serena MCP 驱动的重构工作流

#### 阶段 1: 符号定位与分析 (Serena find_symbol)
1. **Current State Analysis**:
   - Review code against PLANNING.md ideals
   - Check TASK.md for related debt items
   - Identify improvement opportunities
   - **Serena**: 使用 `find_symbol()` 精确定位所有相关符号，理解符号树

2. **Refactoring Strategy**:
   - Analyst: Find gaps from intended design
   - **Serena 支持**: 自动获取符号的所有引用关系
   - Surgeon: Plan incremental transformations
   - Expert: Apply project's chosen patterns
   - Validator: Ensure quality improvements

#### 阶段 2: 符号级重构执行 (Serena rename_symbol)
3. **Incremental Execution**:
   - Transform in safe steps
   - **Serena 自动化**:
     - 对于重命名操作: 调用 `rename_symbol()` 自动更新所有 N+ 个引用位置
     - 时间节省: 70-90% (手动查找 10-30 分钟 → 自动完成 1-2 分钟)
     - 错误率: 5-10% → 0% (完全消除遗漏)
   - Maintain test coverage
   - Update documentation

#### 阶段 3: 完整性验证 (Serena find_referencing_symbols)
4. **Quality Assurance**:
   - **Serena 验证**: 使用 `find_referencing_symbols()` 确认所有调用点已更新
   - Verify functionality preserved
   - Confirm architecture alignment
   - Update TASK.md progress

## Output Format
1. **Refactoring Plan** – steps aligned with architecture
2. **Implementation** – transformed code per standards
3. **Architecture Alignment** – how changes improve design
4. **Task Completion** – TASK.md updates
5. **Documentation** – PLANNING.md refinements
6. **Serena Verification** – symbol-level changes validation report

## 🔌 MCP 增强能力

本命令支持 Serena MCP 服务器的自动增强。

### Serena (语义代码重构)

**启用**: 自动激活（在 /wf_09_refactor 中）
**用途**: 符号级别的精确代码重构操作
**自动激活**: 执行重构命令时

**示例**:
```bash
# 重命名函数
/wf_09_refactor "将 getUserData 重命名为 fetchUserData"

# 提取方法
/wf_09_refactor "从 processOrder 中提取验证逻辑"

# 重构类结构
/wf_09_refactor "重构 User 类，分离数据访问层"
```

**改进点**:
- 符号精确定位（find_symbol）
- 自动重命名所有引用（rename_symbol）- 错误率从 5-10% → 0%
- 依赖关系分析（find_referencing_symbols）
- 代码结构理解（get_symbols_overview）
- 时间节省 70-90%（手动 10-30 分钟 → 自动 1-2 分钟）

---

### 🔧 MCP Gateway 集成

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Serena 工具调用** (符号重构操作):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 精确定位需要重构的符号
    find_tool = gateway.get_tool("serena", "find_symbol")

    target_symbol = find_tool.call(
        name_path_pattern="getUserData",
        relative_path="src/services/user.ts",
        include_body=True
    )

    # Step 2: 查找所有引用该符号的位置
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

    references = ref_tool.call(
        name_path="getUserData",
        relative_path="src/services/user.ts"
    )

    # Step 3: 执行符号重命名（自动更新所有引用）
    rename_tool = gateway.get_tool("serena", "rename_symbol")

    result = rename_tool.call(
        name_path="getUserData",
        relative_path="src/services/user.ts",
        new_name="fetchUserData"
    )

    # Step 4: 验证完整性
    # Serena 自动更新了所有 N+ 个引用位置
    # 错误率: 0% vs 手动 5-10%
    # 时间节省: 70-90%

else:
    print("⚠️ Serena MCP 不可用，使用手动代码重构")
    # 降级到传统 Grep/Read/Edit 工具链
```

**replace_symbol_body 工具调用** (提取方法重构):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 获取原始方法体
    find_tool = gateway.get_tool("serena", "find_symbol")

    original_method = find_tool.call(
        name_path_pattern="processUserData",
        include_body=True,
        depth=1
    )

    # Step 2: 提取验证逻辑到新方法
    # 手动创建新方法 validateUserData

    # Step 3: 修改原方法体，调用新方法
    replace_tool = gateway.get_tool("serena", "replace_symbol_body")

    new_body = """
    def processUserData(self, data):
        # 调用提取的验证方法
        self.validateUserData(data)

        # 继续处理逻辑
        ...
    """

    replace_tool.call(
        name_path="processUserData",
        relative_path="src/services/user.py",
        body=new_body
    )

else:
    print("⚠️ Serena MCP 不可用，使用 Edit 工具手动重构")
```

**insert_after_symbol 工具调用** (添加新方法):
```python
# 在提取方法后，插入新方法到类中
if gateway.is_available("serena"):
    insert_tool = gateway.get_tool("serena", "insert_after_symbol")

    new_method_body = """
    def validateUserData(self, data):
        '''提取的验证逻辑'''
        if not data:
            raise ValueError("Data cannot be empty")
        # 更多验证逻辑...
    """

    insert_tool.call(
        name_path="processUserData",  # 在此方法之后插入
        relative_path="src/services/user.py",
        body=new_method_body
    )
```

**Gateway 优势**:
- ✅ 统一的 MCP 管理接口
- ✅ 自动降级（MCP 不可用时回退到标准工具）
- ✅ 连接池复用（减少多次启动开销）
- ✅ 工具懒加载（按需初始化）
- ✅ 符号级操作准确率 100%（vs 手动 90-95%）
- ✅ 重构时间节省 70-90%

---

## 🔧 Serena MCP 使用示例

### 场景 1: 重命名函数（最常见）
```bash
# 用户请求
/wf_09_refactor "将 getUserData() 重命名为 fetchUserData()"

# Serena 自动执行的步骤
1. find_symbol("getUserData")
   → 定位到 src/services/user.ts:42 的函数定义

2. find_referencing_symbols("getUserData")
   → 发现 12 个引用位置：
      - src/components/UserProfile.tsx:8 (import)
      - src/pages/Dashboard.tsx:15 (call)
      - ... (总计12处)

3. rename_symbol("getUserData" → "fetchUserData")
   → 自动更新所有 12 处引用
   → 错误率: 0% (vs 手动 5-10%)

4. 验证输出:
   ✅ 所有引用已更新
   ✅ 导入语句已更新
   ✅ 类型定义已更新（如有泛型）
```

### 场景 2: 提取方法（复杂重构）
```bash
# 用户请求
/wf_09_refactor "从 processUserData() 中提取验证逻辑到独立方法"

# Serena 协助的步骤
1. find_symbol("processUserData", depth=1)
   → 获取方法体及内部结构

2. 识别验证代码块位置

3. 提取到新方法 validateUserData()

4. find_referencing_symbols("processUserData")
   → 更新所有调用点（如有必要）

5. 验证: 新方法正确插入，调用关系完整
```

### 场景 3: 重构类名和命名空间
```bash
# 用户请求
/wf_09_refactor "重构 User 类：重命名为 UserEntity，移动到 entities/ 目录"

# Serena 支持的操作
1. find_symbol("User") with filtering
   → 只找到类定义（排除同名变量）

2. rename_symbol("User" → "UserEntity")
   → 更新类定义 + 所有 30+ 处引用

3. 更新导入路径

4. 验证完整性
   ✅ 30+ 个引用全部更新
   ✅ 导入路径已调整
   ✅ 类型注解已更新
```

## Workflow Integration
- Guided by PLANNING.md architecture
- Updates technical debt in TASK.md
- **Serena MCP automatically enabled** for symbol-level operations:
  - `find_symbol()` - precise code location identification
  - `rename_symbol()` - automatic reference updates (100% coverage)
  - `find_referencing_symbols()` - completeness verification
- Requires `/wf_07_test` validation (verify no functionality breaking)
- Triggers `/wf_08_review` assessment (review refactoring quality)
- May update PLANNING.md patterns (document architectural improvements)

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行以下阶段（通常在主流程之外）：

```
主流程: [代码实现] → [测试] → [审查] → [提交]

附加流程: [代码审查] → [重构改进 ← 当前] → [再次测试] → [再次审查] → [提交]
           STEP 5      STEP 5.5        STEP 5.6     STEP 5.7     STEP 6
```

### ✅ 触发条件

通常在以下情况下执行此命令：

1. ✅ 代码审查发现改进机会（`/wf_08_review` 建议）
2. ✅ TASK.md 中有重构任务待完成
3. ✅ 需要优化技术债务或性能

### 📝 当前步骤

**正在执行**: `/wf_09_refactor "重构范围"`

- 按照 PLANNING.md 的架构指导重构
- 改进代码质量和可维护性
- 更新技术债务追踪
- 保持功能不变的前提下优化结构

### ⏭️ 建议下一步

**重构完成后**，必须执行：

```bash
# 第1步: 运行测试确保功能没有改变
/wf_07_test "[相同功能] - 验证重构未破坏功能"

# 第2步: 代码审查重构结果
/wf_08_review "重构代码"

# 第3步: 审查通过后提交
/wf_11_commit "refactor: [改进说明]"
```

### 📊 工作流进度提示

重构完成时，确保：

✅ 已完成:
- 重构代码符合 PLANNING.md 标准
- TASK.md 已更新（技术债务减少）
- 准备进入重新测试

⏭️ 下一步提示:
- 必须运行 /wf_07_test 验证功能不变
- 然后运行 /wf_08_review 最终审查
- 审查通过后运行 /wf_11_commit 提交

### 💡 决策指南

| 情况 | 建议 | 命令 |
|------|------|------|
| 审查建议改进 | 执行重构 | /wf_09_refactor → /wf_07_test → /wf_08_review → /wf_11_commit |
| 有技术债务任务 | 执行重构 | /wf_09_refactor → /wf_07_test → /wf_08_review → /wf_11_commit |
| 重构发现新问题 | 循环 | /wf_05_code → /wf_07_test → /wf_09_refactor |

### 📚 相关文档

- **架构指南**: PLANNING.md
- **设计原则**: PHILOSOPHY.md
- **任务追踪**: TASK.md
- **模式库**: KNOWLEDGE.md
