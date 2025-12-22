---
command: /wf_03_prime
index: 03
phase: "基础设施"
description: "加载项目管理文档到AI上下文（会话必备）| MCP: Serena (自动激活)"
reads: [PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md, CLAUDE.md, PROJECT_INDEX.md]
writes: []
prev_commands: [/clear]
next_commands: [/wf_05_code, /wf_04_ask, /wf_02_task]
model: sonnet
token_budget: medium
context_loading: smart
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "语义级别的项目理解和代码索引"
docs_dependencies:
  guides:
    - docs/guides/wf_03_prime_mcp_serena.md
    - docs/guides/wf_03_prime_smart_loading.md
    - docs/guides/wf_03_prime_workflows.md
  estimated_tokens: 766
  lazy_load: true
  execution_model: "synchronous"
  doc_loader_integrated: true
  token_savings:
    quick_start: "74% (766→200 tokens)"
    full_context: "50% (2400→1200 tokens)"
    task_focused: "60% (1500→600 tokens)"
  note: "指南文档按需加载（DocLoader立即返回）。命令执行是同步的，无需等待。"
context_rules:
  - "PRD.md是只读的，绝不修改"
  - "CONTEXT.md由/wf_11_commit自动管理"
  - "每次会话开始必须运行此命令"
  - "优先使用轻量级模式（PROJECT_INDEX.md），需要详情使用 --full"
---

## ⚠️ 强制语言规则

**此命令为强制语言规则的关键执行命令**。详细的强制语言规则定义请参考 [CLAUDE.md § 强制语言规则](CLAUDE.md#⚠️-强制语言规则)。

**简版要点**：
- ✅ **所有输出内容遵循项目 CLAUDE.md 的语言规范**
- ✅ **优先级**: 项目级 CLAUDE.md > 全局默认 > 命令建议
- ❌ **无例外**: 关键会话启动命令必须严格遵循

---

## 🤖 AI 执行提示（重要）

**⚠️ 关键规则**：
- **Slash commands 是同步执行的**，无需等待"加载完成"
- 看到 `<command-message>wf_03_prime is running…</command-message>` 时，**立即开始执行** Step 0
- **禁止**输出"让我等待命令加载完成"或类似话语
- `lazy_load: true` 表示使用 DocLoader **按需加载**，所有工具调用都是**立即返回**的
- 所有步骤应**连续执行**，无暂停点

---

## 🔌 MCP 增强能力

本命令支持 Serena MCP 服务器的增强，提供更智能的上下文加载：

| 功能 | 说明 | 详细文档 |
|------|------|--------|
| **Serena (自动激活)** | 语义级别的项目理解和代码索引 | [§ wf_03_prime MCP Serena 增强指南](docs/guides/wf_03_prime_mcp_serena.md) |
| **LSP 初始化** | 语言服务器启动、代码扫描、符号索引 | [§ LSP 初始化输出示例](docs/guides/wf_03_prime_mcp_serena.md#lsp-初始化输出示例) |
| **符号级工具** | find_symbol, get_symbols_overview, rename_symbol 等 | [§ LSP 初始化的影响](docs/guides/wf_03_prime_mcp_serena.md#lsp-初始化的影响) |
| **MCP 组合说明** | 与其他 MCP 的关系和使用场景 | [§ 组合说明](docs/guides/wf_03_prime_mcp_serena.md#组合说明) |

**快速说明**: Serena 自动激活，提供项目结构理解、知识图谱构建、智能文档加载、上下文记忆持久化等能力。详细的 MCP 功能和 LSP 初始化过程请参考专用指南文档。

### 🔧 MCP Gateway 集成

**Gateway 初始化** (所有模式开始前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()

# 检查 Serena 可用性
serena_available = gateway.is_available("serena")
```

**Serena 工具调用模式**:
```python
if gateway.is_available("serena"):
    # 获取工具
    symbols_tool = gateway.get_tool("serena", "get_symbols_overview")

    # 调用工具
    result = symbols_tool.call(relative_path="path/to/file.py")
else:
    # 降级到传统文件读取
    print("⚠️ Serena MCP 不可用，使用传统 Read 工具")
```

**Gateway 优势**:
- ✅ 统一的 MCP 服务器管理
- ✅ 自动降级机制（Serena 不可用时）
- ✅ 连接池复用（减少启动开销）
- ✅ 工具懒加载（按需初始化）

---

## 执行上下文
**输入**: 所有项目管理文档
**输出**: AI工作记忆中的项目上下文
**依赖链**: /clear (可选) → **当前（会话启动）** → /wf_05_code / /wf_04_ask

## Usage
`/wf_03_prime`

## Purpose
Prime the AI assistant with comprehensive project context by reading core project files to understand:
- Current project state and architecture
- Completed work and remaining tasks
- Development guidelines and standards
- Active working context
- Accumulated project knowledge and patterns

## Process

⚠️ **AI执行强制规则**: 本命令的执行必须严格遵循以下步骤，不得跳过或随意解释。

### Step 0: 加载工作流指南（立即执行）⚡

**重要**: 本步骤是同步的，Doc Guard 工具**立即返回**结果，无需等待。

**立即执行以下命令**来加载详细指导：

```bash
# 立即执行 - DocLoader 同步返回结果（~200 tokens，vs 完整文档 ~766 tokens）
python $HOME/.claude/commands/scripts/doc_guard.py \
  --docs "$HOME/.claude/commands/docs/guides/wf_03_prime_workflows.md" \
  --sections "{\"$HOME/.claude/commands/docs/guides/wf_03_prime_workflows.md\": [\"AI执行协议\", \"模式选择决策树\", \"执行流程\"]}"
```

**说明**：
- ✅ 此命令**立即返回**结果，不存在"等待加载"
- ✅ 如果 doc_guard 不可用，直接使用 Read 工具
- ⚠️ 完成后，**立即**进入 Step 1-5（按指南执行）

### Step 1-5: 按指南执行

**详细执行流程**: 所有步骤必须严格遵循 [wf_03_prime 工作流指南](docs/guides/wf_03_prime_workflows.md) 中的"AI执行协议"部分

**快速参考**（仅供理解，不得作为执行依据）:

**三种加载模式**:
1. **Quick Start** (快速启动): 仅加载项目索引 (~200 tokens)
2. **Task Focused** (任务导向): 加载当前任务相关上下文 (~600 tokens)
3. **Full Context** (完整上下文): 加载所有管理文档 (~1200 tokens)

**关键步骤**:
1. 模式选择（根据决策树）
2. 文档可用性检查
3. 按模式加载文档（使用Doc Guard）
4. 生成标准化输出
5. 添加模式切换提示
6. 文档健康检查 🆕 (Phase 7.5)

**所有详细规范**: 必须参照 [工作流指南](docs/guides/wf_03_prime_workflows.md)

---

### Step 6: 文档健康检查 (NEW - Phase 7.5)

**目的**: 在会话启动时自动检查文档大小，及时提醒存档

**执行**:
```bash
echo ""
echo "## 📊 文档健康检查"
echo ""

# 检查 check_doc_size.sh 是否存在
if [ -f "./scripts/check_doc_size.sh" ]; then
    # 执行检查
    ./scripts/check_doc_size.sh

    # 如果有超限文档，提供建议
    if [ $? -ne 0 ]; then
        echo ""
        echo "💡 建议: 运行 /wf_13_doc_maintain check 查看详情"
        echo "   或使用 /wf_13_doc_maintain archive <文档> 执行存档"
    fi
else
    echo "✅ 文档健康检查工具未配置（跳过）"
fi

echo ""
```

**输出示例**:
```
## 📊 文档健康检查

✅ CONTEXT.md: 25/50 行 (50%)
⚠️ TASK.md: 428/200 行 (214%) - 超限
⚠️ PLANNING.md: 375/300 行 (125%) - 超限
✅ KNOWLEDGE.md: 149/200 行 (75%)

建议:
  - 运行 /wf_13_doc_maintain archive TASK.md
  - 运行 /wf_13_doc_maintain archive PLANNING.md

💡 建议: 运行 /wf_13_doc_maintain check 查看详情
   或使用 /wf_13_doc_maintain archive <文档> 执行存档
```

**降级处理**:
- 如果 check_doc_size.sh 不存在：显示"未配置"并跳过
- 如果执行失败：不影响其他步骤

---

### 执行检查清单（AI必须验证）

在输出结果前，AI必须确认以下所有项目：

- [ ] ✅ 已读取 docs/guides/wf_03_prime_workflows.md
- [ ] ✅ 已根据决策树选择模式并说明理由
- [ ] ✅ 已检查文档可用性
- [ ] ✅ 已按选定模式加载文档
- [ ] ✅ 输出格式符合指南中的标准模板
- [ ] ✅ 已添加模式切换提示
- [ ] ✅ 遵循CLAUDE.md语言规范

**如果任何检查项未通过，必须重新执行对应步骤**

---
## Output Format

**详细输出格式**: 完整的输出格式、章节结构和内容示例请参考 [wf_03_prime 工作流指南](docs/guides/wf_03_prime_workflows.md)

### 标准输出结构

```markdown
# 项目上下文摘要

## 📋 项目概览
- 项目名称、目标、当前阶段

## 📐 架构要点
- 技术栈、核心模块、关键决策

## 📝 当前任务
- 进行中的任务、优先级、阻塞问题

## 🎯 推荐下一步
- 基于任务状态的命令推荐

## 🔗 关键文档索引
- 快速访问路径

## 📊 文档健康检查 🆕 (Phase 7.5)
- 运行 check_doc_size.sh 检查文档大小
- 显示超限文档列表
- 提供存档建议
```

**详细格式规范、Serena MCP 输出和模式选择**: 参见 [工作流指南](docs/guides/wf_03_prime_workflows.md)

---
## 📌 工作流导航 (Phase 3 - 闭环工作流)

当使用此命令时，你正在标准开发流程的以下阶段执行：

```
[项目启动] → [任务规划] → [加载上下文 ← 当前] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [提交保存]
  STEP 0       STEP 0.5        STEP 1                STEP 2       STEP 3       STEP 4       STEP 5      STEP 6
```

**完整的工作流导航、路径选择、决策矩阵和实现规范请参考**: [§ wf_03_prime 工作流导航指南](docs/guides/wf_03_prime_workflows.md)

### 快速参考 - 3条后续工作路径

| 路径 | 场景 | 建议命令 | 说明 |
|------|------|--------|------|
| **路径 1** | 需要技术咨询 | `/wf_04_ask` | 架构咨询、技术决策、获取设计指导 |
| **路径 2** | 直接编码 | `/wf_05_code` | 任务明确，不需额外咨询，直接开始编码 |
| **路径 3** | 更新任务 | `/wf_02_task update` | 明确标记当前任务，确保任务追踪连续性 |

**详细说明**: 工作流位置指示、已完成步骤、下一步建议、工作流进度提示、完整决策指南见专用指南文档。

---

## 🎯 使用示例和最佳实践

**详细示例和场景**: 完整的使用示例、最佳实践和后续工作流路径请参考 [wf_03_prime 工作流指南](docs/guides/wf_03_prime_workflows.md)

### 典型场景

**会话开始**: `/wf_03_prime` → 加载上下文 → 推荐下一步
**功能开发**: prime → `/wf_05_code` → 实现 → 测试 → 提交
**Bug修复**: prime → `/wf_06_debug` → 修复 → 验证
**详细示例、命令参数、后续工作流决策**: 参见 [工作流指南](docs/guides/wf_03_prime_workflows.md)

---
## 🔄 Command Lazy Loading

**详细说明**: 完整的智能加载机制、DocLoader 使用和性能优化请参考 [智能加载策略指南](docs/guides/wf_03_prime_smart_loading.md)

### 快速参考

**核心机制**: DocLoader 智能文档加载工具

**三种加载模式**:
- **summary**: 仅摘要（50行以内，~100 tokens）
- **sections**: 按章节加载（指定章节，~400 tokens）
- **full**: 完整文档（<300行才允许，~900 tokens）

**性能优化**:
- Quick Start: 74% token 节省（766→200 tokens）
- Task Focused: 60% token 节省（1500→600 tokens）
- Full Context: 50% token 节省（2400→1200 tokens）

**使用示例**:
```python
from commands.lib.doc_loader import DocLoader
loader = DocLoader()
summary = loader.load_summary("docs/guides/large_doc.md", max_lines=50)
```

**详细 API、配置和最佳实践**: 参见 [智能加载策略指南](docs/guides/wf_03_prime_smart_loading.md)

---
