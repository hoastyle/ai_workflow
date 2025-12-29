---
title: "wf_03_prime 智能加载详解"
description: "文档智能加载策略、输出格式和实现示例"
type: "技术设计"
status: "完成"
priority: "中"
created_date: "2025-11-27"
last_updated: "2025-11-27"
related_documents:
  - "../../wf_03_prime.md"
  - "../../KNOWLEDGE.md"
  - "../reference/FRONTMATTER.md"
related_code: []
---

# wf_03_prime 智能加载详解

本文档说明 `/wf_03_prime` 中的智能文档加载策略、输出格式和实现示例。

---

## 执行上下文

**输入**: 所有项目管理文档
**输出**: AI工作记忆中的项目上下文
**依赖链**: /clear (可选) → **当前（会话启动）** → /wf_05_code / /wf_04_ask

---

## Process (6-7 步详细过程)

### 1. **Read Core Management Documents** (Always Load)
   - Check for existence of PRD.md, PLANNING.md, TASK.md, CONTEXT.md, and KNOWLEDGE.md
   - Read PRD.md for project requirements (read-only, never modify)
   - Read CONTEXT.md as **pointer document** for session pointers (if exists)
   - Read PLANNING.md for architecture aligned with PRD requirements
   - Read TASK.md for current tasks and priorities
   - Read KNOWLEDGE.md for accumulated project knowledge and documentation index
   - Read CLAUDE.md for project-specific AI guidance (if exists)

### 2. **Parse Documentation Index** (NEW - Smart Loading)
   - Extract "📚 文档索引" section from KNOWLEDGE.md
   - Parse technical documentation map (path, priority, last_updated)
   - Parse task-document relationship mapping
   - Understand document dependency graph
   - Build available documentation catalog

### 3. **Context-Aware Document Loading** (NEW - On-Demand)
   - Analyze current active tasks from TASK.md
   - Match tasks with related technical documents (from KNOWLEDGE.md index)
   - Evaluate document priority (高/中/低) and relevance
   - Decision logic:
     * Priority=高 AND task-relevant → Load immediately
     * Priority=中 AND task-relevant → Load if context allows
     * Priority=低 OR task-irrelevant → Skip, note availability
   - Load selected technical documents from docs/ directory

### 4. **Context Analysis**
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

### 5. **Session State Recovery** (Using Pointers)
   - **Use CONTEXT.md pointers** to locate session state in source documents:
     * Active task pointer → Read task details from TASK.md
     * Git baseline → Understand what commits happened since last session
     * Next startup recommendation → Know which command to run next
   - Understand current development focus from TASK.md (not CONTEXT.md)
   - Identify where work was left off using task pointers
   - Restore development context by following pointers to source documents

### 6. **Working Memory Setup**
   - Load relevant code patterns and conventions from KNOWLEDGE.md
   - Apply accumulated solutions to current context
   - Understand testing and deployment procedures
   - Note security considerations and constraints
   - Reference architectural decisions for consistency
   - Prepare for continuation of work with enhanced context
   - Remember available technical documents for on-demand access

---

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
    - **符号索引状态** - 显示代码扫描和索引进度
    - **性能基准** - 显示 LSP 工具的预期性能
    - **缓存策略** - 显示后续激活的预期表现
    - **就绪确认** - 显示 LSP 是否准备好进行符号级操作
11. **💡 智能推荐下一步 (NEW - Phase 2 改进)** - 基于 TASK.md 的优先任务推荐
12. **Ready Status** - Confirmation of context loading and readiness to continue

---

## 智能加载示例

### Example 1: User Authentication Task
```
Active Task: "实现JWT用户认证"
→ Load: docs/api/authentication.md (priority: 高, relevant)
→ Load: docs/architecture/system-design.md (priority: 高, relevant)
→ Note: docs/database/schema.md (priority: 中, available if needed)
→ Skip: docs/deployment/ci-cd.md (priority: 中, irrelevant)
```

### Example 2: Performance Bug Fix
```
Active Task: "修复API响应慢问题"
→ Load: docs/database/optimization.md (priority: 中, relevant)
→ Load: docs/architecture/data-flow.md (priority: 高, relevant)
→ Note: docs/api/endpoints/ (priority: 低, available if needed)
```

### Example 3: New Project (No Technical Docs Yet)
```
Active Task: "项目初始化"
→ Load: 5 management docs only
→ Note: No technical docs exist yet
→ Suggestion: Run /wf_01_planning to initialize documentation structure
```

---

## 智能加载决策逻辑

### 加载决策流程

```
对于 KNOWLEDGE.md 索引中的每个文档:
1. 检查文档优先级 (高/中/低)
2. 检查文档与当前任务的相关性
3. 计算加载优先级:
   - 高优先级 + 高相关性 → 立即加载
   - 中优先级 + 高相关性 → 询问或加载
   - 中优先级 + 中相关性 → 注记为可用
   - 低优先级 或 无相关性 → 不加载

4. 估计上下文成本:
   - 管理层文档: 固定 ~50KB
   - 每个加载的技术文档: 10-50KB
   - 总预算: 100-150KB

5. 按优先级加载文档，直到接近预算上限
```

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

---

**See Also**:
- [wf_03_prime.md](../../wf_03_prime.md) - 主命令文档
- [wf_03_prime_mcp_serena.md](wf_03_prime_mcp_serena.md) - MCP Serena 增强指南
- [wf_03_prime_workflows.md](wf_03_prime_workflows.md) - 工作流导航指南
- [KNOWLEDGE.md](../../KNOWLEDGE.md) - 知识库索引
