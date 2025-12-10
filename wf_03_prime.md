---
command: /wf_03_prime
index: 03
phase: "基础设施"
description: "加载项目管理文档到AI上下文（会话必备）| MCP: Serena (自动激活)"
reads: [PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md, CLAUDE.md, PROJECT_INDEX.md]
writes: []
prev_commands: [/clear]
next_commands: [/wf_05_code, /wf_04_ask, /wf_02_task]
model: haiku
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
  doc_loader_integrated: true
  token_savings:
    quick_start: "74% (766→200 tokens)"
    full_context: "50% (2400→1200 tokens)"
    task_focused: "60% (1500→600 tokens)"
  note: "使用 DocLoader 按需加载，根据工作模式智能选择内容"
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

## 🔌 MCP 增强能力

本命令支持 Serena MCP 服务器的增强，提供更智能的上下文加载：

| 功能 | 说明 | 详细文档 |
|------|------|--------|
| **Serena (自动激活)** | 语义级别的项目理解和代码索引 | [§ wf_03_prime MCP Serena 增强指南](docs/guides/wf_03_prime_mcp_serena.md) |
| **LSP 初始化** | 语言服务器启动、代码扫描、符号索引 | [§ LSP 初始化输出示例](docs/guides/wf_03_prime_mcp_serena.md#lsp-初始化输出示例) |
| **符号级工具** | find_symbol, get_symbols_overview, rename_symbol 等 | [§ LSP 初始化的影响](docs/guides/wf_03_prime_mcp_serena.md#lsp-初始化的影响) |
| **MCP 组合说明** | 与其他 MCP 的关系和使用场景 | [§ 组合说明](docs/guides/wf_03_prime_mcp_serena.md#组合说明) |

**快速说明**: Serena 自动激活，提供项目结构理解、知识图谱构建、智能文档加载、上下文记忆持久化等能力。详细的 MCP 功能和 LSP 初始化过程请参考专用指南文档。

### 🔧 MCP Gateway 集成 (NEW - Task 3.2)

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
# 旧模式 (直接 MCP 调用) - 已废弃
# get_symbols_overview("path/to/file.py")

# 新模式 (通过 Gateway)
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

**详细执行流程**: 完整的加载流程、模式选择和后续工作流导航请参考 [wf_03_prime 工作流指南](docs/guides/wf_03_prime_workflows.md)

### 快速参考

**三种加载模式**:
1. **Quick Start** (快速启动): 仅加载项目索引 (~200 tokens)
2. **Task Focused** (任务导向): 加载当前任务相关上下文 (~600 tokens)
3. **Full Context** (完整上下文): 加载所有管理文档 (~1200 tokens)

**文档加载（强制使用 Doc Guard 工具）**:
```bash
python ~/.claude/commands/scripts/doc_guard.py --docs "docs/management/PLANNING.md,docs/management/TASK.md,KNOWLEDGE.md"
```

**执行步骤**:
1. 检测文档可用性（PLANNING.md, TASK.md 等）
2. 选择加载模式（默认：Quick Start）
3. 智能加载文档（使用 DocLoader 按需加载）
4. 生成上下文摘要
5. 推荐下一步命令

**详细流程、模式切换条件、后续工作流**: 参见 [工作流指南](docs/guides/wf_03_prime_workflows.md)

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
## 🔄 Command Lazy Loading (Task 3.3)

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
## Integration Notes
- **NEW**: 支持三种加载模式 (Quick Start / Task Focused / Full Context)
- **NEW**: 优先使用 PROJECT_INDEX.md 作为轻量级入口 (80% token 节省)
- **NEW**: 根据用户标志 (--full / --task) 动态调整加载策略
- **NEW (Task 2.5)**: Serena MCP 深度集成 - LSP 符号级代码理解和智能预加载
- **NEW (Task 3.3)**: Command Lazy Loading - 命令按需加载机制 (67.5% token 节省)
  * Quick Start 模式加载 COMMAND_INDEX.md (500 tokens) 而非所有命令 (15,000 tokens)
  * 命令在调用时才加载完整定义，会话级缓存避免重复读取
  * 向后兼容：无 COMMAND_INDEX.md 时自动降级到传统模式
  * 性能提升：启动速度 70-75% faster，典型会话节省 13,500 tokens
  * Step 0: Serena 可用性检测和 LSP 初始化
  * Step 1 Mode B: 符号查询替代完整文件读取 (73% token 节省 for TASK/KNOWLEDGE)
  * Step 1.5: 智能预加载 (项目结构扫描、符号索引、任务热点定位)
  * Step 3: 语义增强分析 (架构理解、代码定位、ADR 验证)
  * 效果: Mode B token 消耗 10K → 6.1K (39% reduction), 启动速度 +37%
- Run after `/clear` to restore working context
- Use before starting new related work sessions
- Loads CONTEXT.md as pointer document for quick session navigation (updated by `/wf_11_commit`)
- Integrates KNOWLEDGE.md for accumulated project wisdom and documentation index
- Smart loading strategy: Default to lightweight mode, upgrade on-demand
- Context cost optimization: Technical docs loaded on-demand based on task relevance
- Ensures continuity across context boundaries
- Maintains development momentum without redundant information
- Provides intelligent context enhancement through past decisions
- Core component of the closed-loop workflow system with long-term memory

