---
command: /wf_10_optimize
index: 10
phase: "质量保证"
description: "性能优化协调器，满足性能目标"
reads: [PLANNING.md(性能目标), TASK.md(优化任务), 代码文件]
writes: [代码文件, TASK.md(优化完成), 性能报告]
prev_commands: [/wf_08_review]
next_commands: [/wf_09_refactor, /wf_07_test, /wf_11_commit]
model: sonnet
token_budget: medium
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "性能瓶颈定位和热点函数分析"
context_rules:
  - "满足PRD性能要求"
  - "遵循PLANNING.md性能目标"
  - "保持功能正确性"
---

## 🔌 MCP 增强能力

本命令支持 Serena MCP 服务器的自动增强。

### Serena (性能瓶颈识别和热点分析)

**启用**: 自动激活（在 /wf_10_optimize 中）
**用途**: 语义级别的代码理解和性能热点定位
**自动激活**: 执行性能优化命令时

**示例**:
```bash
# 自动激活（检测到性能优化需求）
/wf_10_optimize "API 响应时间从 500ms 降至 200ms"

# 显式优化特定模块
/wf_10_optimize "优化数据库查询性能"
```

**改进点**:
- 精确定位性能瓶颈函数和热点代码路径
- 自动识别高频调用的函数和方法
- 分析函数调用关系识别优化机会
- 符号级代码结构理解辅助算法优化
- 验证优化后的代码完整性

---

### 🔧 MCP Gateway 集成 (NEW - Task 3.2)

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Serena 工具调用** (性能瓶颈定位):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 获取模块的代码结构概览
    overview_tool = gateway.get_tool("serena", "get_symbols_overview")

    overview = overview_tool.call(
        relative_path="src/services/api_handler.py",
        max_answer_chars=-1  # 获取完整概览
    )

    # Step 2: 定位可能的性能瓶颈函数
    find_tool = gateway.get_tool("serena", "find_symbol")

    # 定位高频调用的函数
    hot_function = find_tool.call(
        name_path_pattern="process_request",
        relative_path="src/services/api_handler.py",
        include_body=True  # 获取函数体以分析算法复杂度
    )

    # Step 3: 分析函数的调用关系
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

    call_sites = ref_tool.call(
        name_path="process_request",
        relative_path="src/services/api_handler.py"
    )

    # 分析调用频率和上下文
    # 识别是否在循环中被调用（性能热点）

else:
    print("⚠️ Serena MCP 不可用，使用传统 Grep/Read 工具分析性能")
```

**性能优化工作流示例** (数据库查询优化):
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 定位所有数据库查询函数
    find_tool = gateway.get_tool("serena", "find_symbol")

    # 查找所有包含 "query" 的函数（使用子串匹配）
    query_functions = find_tool.call(
        name_path_pattern="query",
        substring_matching=True,
        include_body=True
    )

    # Step 2: 分析每个查询的调用模式
    ref_tool = gateway.get_tool("serena", "find_referencing_symbols")

    for func in query_functions:
        references = ref_tool.call(
            name_path=func["name_path"],
            relative_path=func["relative_path"]
        )

        # 识别在循环中的查询（N+1 问题）
        # 识别未使用索引的查询
        # 识别可以批量执行的查询

    # Step 3: 优化查询后，使用 replace_symbol_body 更新
    replace_tool = gateway.get_tool("serena", "replace_symbol_body")

    optimized_body = """
    def query_users_batch(self, user_ids):
        '''优化后：批量查询代替循环单次查询'''
        # 使用 IN 语句批量查询
        return self.db.query(
            "SELECT * FROM users WHERE id IN (%s)" %
            ','.join(map(str, user_ids))
        )
    """

    replace_tool.call(
        name_path="query_users_batch",
        relative_path="src/services/database.py",
        body=optimized_body
    )

    # Step 4: 验证所有调用点已更新
    updated_refs = ref_tool.call(
        name_path="query_users_batch",
        relative_path="src/services/database.py"
    )

    # Serena 自动确保引用完整性
    # 性能提升: N次查询 → 1次批量查询

else:
    print("⚠️ Serena MCP 不可用，使用手动性能优化")
```

**算法复杂度优化示例**:
```python
# 检查可用性
if gateway.is_available("serena"):
    # Step 1: 定位算法实现
    find_tool = gateway.get_tool("serena", "find_symbol")

    algorithm_func = find_tool.call(
        name_path_pattern="find_duplicates",
        include_body=True,
        depth=1  # 包括内部辅助函数
    )

    # Step 2: 分析当前算法复杂度
    # 当前实现: O(n²) 嵌套循环

    # Step 3: 使用 replace_symbol_body 替换为优化算法
    replace_tool = gateway.get_tool("serena", "replace_symbol_body")

    optimized_algorithm = """
    def find_duplicates(self, items):
        '''优化后：O(n) 使用集合代替 O(n²) 嵌套循环'''
        seen = set()
        duplicates = set()

        for item in items:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)

        return list(duplicates)
    """

    replace_tool.call(
        name_path="find_duplicates",
        relative_path="src/utils/data_processing.py",
        body=optimized_algorithm
    )

    # 性能改进: O(n²) → O(n)
    # 对于 10,000 项: 100,000,000 操作 → 10,000 操作 (10,000x 提升)
```

**Gateway 优势**:
- ✅ 统一的 MCP 管理接口
- ✅ 自动降级（MCP 不可用时回退到标准工具）
- ✅ 连接池复用（减少多次启动开销）
- ✅ 工具懒加载（按需初始化）
- ✅ 符号级精确定位（准确率 100%）
- ✅ 性能瓶颈识别效率提升 70-90%

---

## 执行上下文
**输入**: PLANNING.md性能目标 + 性能分析数据
**输出**: 优化代码 + 性能改进报告 + TASK.md更新
**依赖链**: **当前（性能优化）** → /wf_07_test (验证) → /wf_11_commit

## Usage
`/wf_10_optimize <PERFORMANCE_TARGET>`

## Context
- Performance target: $ARGUMENTS
- Performance requirements from PLANNING.md
- Optimization tasks in TASK.md
- System constraints and targets

## Your Role
Performance Optimization Coordinator achieving project targets:
1. **Profiler Analyst** – measures against requirements
2. **Algorithm Engineer** – optimizes per constraints
3. **Resource Manager** – manages within limits
4. **Scalability Architect** – ensures target scale

## Process
1. **Performance Baseline**:
   - Review targets in PLANNING.md
   - Check optimization tasks in TASK.md
   - Measure current performance

2. **Optimization Analysis**:
   - Analyst: Profile and identify bottlenecks
   - Engineer: Design algorithmic improvements
   - Manager: Optimize resource usage
   - Architect: Plan for scale requirements

3. **Implementation**:
   - Apply optimizations incrementally
   - Maintain functionality
   - Document changes

4. **Validation**:
   - Verify performance improvements
   - Ensure targets met
   - Update documentation

## Output Format
1. **Performance Analysis** – current vs. target metrics
2. **Optimization Plan** – improvement strategy
3. **Implementation** – optimized code
4. **Results** – achieved improvements
5. **Task Updates** – TASK.md completions

## Workflow Integration
- Targets from PLANNING.md requirements
- Updates optimization tasks in TASK.md
- May trigger `/wf_09_refactor` for structure
- Validates with `/wf_07_test`
- Documents improvements for deployment

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行以下阶段（通常在主流程之外）：

```
主流程: [代码实现] → [测试] → [审查] → [提交]

优化流程: [代码审查] → [性能优化 ← 当前] → [再次测试] → [再次审查] → [提交]
           STEP 5      STEP 5.8        STEP 5.9     STEP 5.10    STEP 6
```

### ✅ 触发条件

通常在以下情况下执行此命令：

1. ✅ PLANNING.md 中有性能目标需要达成
2. ✅ TASK.md 中有优化任务待完成
3. ✅ 用户反馈或基准测试显示性能瓶颈

### 📝 当前步骤

**正在执行**: `/wf_10_optimize "性能目标"`

- 按照 PLANNING.md 的性能要求优化
- 分析性能瓶颈并实施优化
- 更新优化任务状态
- 记录性能改进指标

### ⏭️ 建议下一步

**优化完成后**，必须执行：

```bash
# 第1步: 运行性能测试验证优化结果
/wf_07_test "[相同功能] - 性能回归测试"

# 第2步: 代码审查优化代码
/wf_08_review "优化代码"

# 第3步: 审查通过后提交
/wf_11_commit "perf: [性能优化说明]"
```

### 📊 工作流进度提示

优化完成时，确保：

✅ 已完成:
- 优化代码符合 PLANNING.md 标准
- 性能指标达到或超过目标
- TASK.md 优化任务已更新
- 准备进入性能验证

⏭️ 下一步提示:
- 必须运行 /wf_07_test 验证性能改进
- 然后运行 /wf_08_review 审查代码
- 审查通过后运行 /wf_11_commit 提交

### 💡 决策指南

| 情况 | 建议 | 命令 |
|------|------|------|
| 性能目标未达 | 优化 | /wf_10_optimize → /wf_07_test → /wf_08_review → /wf_11_commit |
| 需要重构优化 | 两步 | /wf_09_refactor → /wf_10_optimize → /wf_07_test |
| 优化效果有限 | 咨询 | /wf_04_ask "还有其他优化方向吗？" |

### 📚 相关文档

- **性能要求**: PLANNING.md (Performance Requirements)
- **优化策略**: PLANNING.md (Optimization Strategy)
- **任务追踪**: TASK.md
- **架构指南**: PLANNING.md (Architecture)
