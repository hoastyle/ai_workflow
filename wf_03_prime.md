---
command: /wf_03_prime
index: 03
phase: "基础设施"
description: "加载项目管理文档到AI上下文（会话必备）| MCP: Serena (自动激活)"
reads: [PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md, CLAUDE.md]
writes: []
prev_commands: [/clear]
next_commands: [/wf_05_code, /wf_04_ask, /wf_02_task]
model: haiku
mcp_support:
  - name: "Serena"
    flag: "自动激活"
    detail: "语义级别的项目理解和代码索引"
context_rules:
  - "PRD.md是只读的，绝不修改"
  - "CONTEXT.md由/wf_11_commit自动管理"
  - "每次会话开始必须运行此命令"
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
1. **Read Core Management Documents** (Always Load):
   - Check for existence of PRD.md, PLANNING.md, TASK.md, CONTEXT.md, and KNOWLEDGE.md
   - Read PRD.md for project requirements (read-only, never modify)
   - Read CONTEXT.md as **pointer document** for session pointers (if exists)
     * NOTE: CONTEXT.md now contains only pointers and metadata (zero redundancy)
     * Pointers reference sections in TASK.md, PLANNING.md, KNOWLEDGE.md
     * Use pointers to navigate to actual content in source documents
   - Read PLANNING.md for architecture aligned with PRD requirements
   - Read TASK.md for current tasks and priorities
   - Read KNOWLEDGE.md for accumulated project knowledge and documentation index
   - Read CLAUDE.md for project-specific AI guidance (if exists)

2. **Parse Documentation Index** (NEW - Smart Loading):
   - Extract "📚 文档索引" section from KNOWLEDGE.md
   - Parse technical documentation map (path, priority, last_updated)
   - Parse task-document relationship mapping
   - Understand document dependency graph
   - Build available documentation catalog

3. **Context-Aware Document Loading** (NEW - On-Demand):
   - Analyze current active tasks from TASK.md
   - Match tasks with related technical documents (from KNOWLEDGE.md index)
   - Evaluate document priority (高/中/低) and relevance
   - Decision logic:
     * Priority=高 AND task-relevant → Load immediately
     * Priority=中 AND task-relevant → Load if context allows
     * Priority=低 OR task-irrelevant → Skip, note availability
   - Load selected technical documents from docs/ directory

4. **Context Analysis**:
   - Parse project architecture and technology stack from PLANNING.md
   - **Extract pointers from CONTEXT.md** (pointer document):
     * Identify active task pointer → Navigate to TASK.md section
     * Identify related architecture pointer → Navigate to PLANNING.md section
     * Identify related ADR pointers → Navigate to KNOWLEDGE.md ADR entries
     * Extract session metadata (Git baseline, commits count, change areas)
   - Extract architectural decisions and patterns from KNOWLEDGE.md
   - Understand current development phase from TASK.md
   - Identify active tasks and priorities
   - Note any blockers or dependencies
   - Review common issues and solutions from knowledge base

5. **Session State Recovery** (Using Pointers):
   - **Use CONTEXT.md pointers** to locate session state in source documents:
     * Active task pointer → Read task details from TASK.md
     * Git baseline → Understand what commits happened since last session
     * Next startup recommendation → Know which command to run next
   - Understand current development focus from TASK.md (not CONTEXT.md)
   - Identify where work was left off using task pointers
   - Restore development context by following pointers to source documents

6. **Working Memory Setup**:
   - Load relevant code patterns and conventions from KNOWLEDGE.md
   - Apply accumulated solutions to current context
   - Understand testing and deployment procedures
   - Note security considerations and constraints
   - Reference architectural decisions for consistency
   - Prepare for continuation of work with enhanced context
   - Remember available technical documents for on-demand access

7. **智能推荐下一步 (NEW - Phase 2 改进)**:
   - 解析 TASK.md 中的"🚀 下一步优先任务"部分
   - 提取"推荐工作流序列"中的第一个任务（最高优先级）
   - 检查任务是否已经被标记为"进行中"：
     * 如果有进行中的任务 → 推荐继续当前任务的下一步
     * 如果没有进行中的任务 → 推荐优先级最高的待做任务
   - 从任务的"基本信息"中提取：
     * 任务标题、优先级、预计时间
     * 工作流位置标记（[准备阶段] → [代码实现] 等）
     * 为什么优先的背景说明
   - 从任务的"推荐命令序列"中提取完整的命令步骤
   - 从任务的"验收标准"中提取检查清单
   - 在输出中突出显示这些信息，帮助用户立即知道下一步该做什么

## Output Format
1. **Requirements Overview** - Key requirements from PRD.md (read-only reference)
2. **Project Summary** - Brief overview from PLANNING.md aligned with PRD
3. **Documentation Map** (NEW) - Available technical documents with priorities
4. **Loaded Technical Docs** (NEW) - List of technical documents loaded based on current tasks
5. **Knowledge Base Summary** - Key patterns and decisions from KNOWLEDGE.md
6. **Session Recovery** - Pointers from CONTEXT.md to locate session state in source documents
7. **Active Context** - Current working area and immediate tasks from TASK.md
8. **Applicable Solutions** - Relevant past solutions and patterns for current context
9. **On-Demand Documents** (NEW) - Available but not loaded docs (can be accessed if needed)
10. **🔍 Serena LSP 初始化信息** (NEW - LSP 增强输出)
    - **LSP 初始化状态** - 显示语言服务器的启动进度
      * LSP 服务器类型（Pyright for Python, TypeScript LS, etc.）
      * 启动耗时（通常 2-5 秒）
    - **符号索引状态** - 显示代码扫描和索引进度
      * 已扫描的文件数和符号数
      * 索引耗时（通常 5-25 秒，取决于项目大小）
      * 符号表构建完成情况
    - **性能基准** - 显示 LSP 工具的预期性能
      * 符号查询延迟（find_symbol: ~100-300ms）
      * 符号概览延迟（get_symbols_overview: ~200-500ms）
      * 引用查找延迟（find_referencing_symbols: ~300-1000ms）
    - **缓存策略** - 显示后续激活的预期表现
      * 首次激活耗时（~8-30 秒）
      * 缓存激活耗时（< 1 秒）
    - **就绪确认** - 显示 LSP 是否准备好进行符号级操作
      * "✅ Serena ready for tool calls" 表示可以使用所有 23 个工具
      * 如果显示等待中，说明正在进行索引和缓存

11. **💡 智能推荐下一步 (NEW - Phase 2 改进)** - 基于 TASK.md 的优先任务推荐
    - 识别"🚀 下一步优先任务"部分中的第一个（最高优先级）任务
    - 显示任务名称、优先级、预计时间
    - 显示完整的"推荐命令序列"（从 TASK.md 提取）
    - 显示工作流位置标记（STEP X/Y）
    - 显示验收标准（可验证的检查清单）
    - 显示"为什么优先"的背景说明

12. **Ready Status** - Confirmation of context loading and readiness to continue

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

## Integration Notes
- Run after `/clear` to restore working context
- Use before starting new related work sessions
- Loads CONTEXT.md as pointer document for quick session navigation (updated by `/wf_11_commit`)
- Integrates KNOWLEDGE.md for accumulated project wisdom and documentation index
- Smart loading strategy: Always load 5 management docs, selectively load technical docs
- Context cost optimization: Technical docs loaded on-demand based on task relevance
- Ensures continuity across context boundaries
- Maintains development momentum without redundant information
- Provides intelligent context enhancement through past decisions
- Core component of the closed-loop workflow system with long-term memory

## 智能加载详解

**执行策略**: 总是加载5个管理层文档，根据当前任务相关性智能选择技术文档

| 任务类型 | 加载策略示例 | 详细说明 |
|---------|------------|--------|
| **用户认证** | Load: API文档、架构设计 Note: 数据库模式 | 实现JWT认证时的文档选择 |
| **性能优化** | Load: 数据库优化、数据流 Note: API端点 | 修复响应慢问题时的文档选择 |
| **新项目** | Load: 5个管理层文档 Note: 暂无技术文档 | 初始化项目时的加载策略 |

**详细的智能加载策略、决策逻辑和完整示例请参考**: [§ wf_03_prime 智能加载详解](docs/guides/wf_03_prime_smart_loading.md)

## 💡 智能推荐下一步 (Phase 2 改进)

命令执行时会基于 TASK.md 中的待做或进行中任务自动生成智能推荐：

| 场景 | 输出内容 | 推荐命令序列 |
|------|---------|-----------|
| **待做任务** | 任务名、优先级、预计时间 | 完整的命令序列和验收标准 |
| **进行中任务** | 任务名、进度(X/Y步) | 下一步建议和工作流位置 |
| **全部完成** | "任务已全部完成！" | 项目统计信息和下阶段建议 |

**详细的推荐算法、提取步骤、验证检查表和错误处理请参考**: [§ wf_03_prime 工作流导航指南 § 智能推荐输出规范](docs/guides/wf_03_prime_workflows.md#智能推荐输出规范)