---
command: /wf_03_prime
index: 03
phase: "基础设施"
description: "加载项目管理文档到AI上下文（会话必备）"
model: haiku
reads: [PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md, CLAUDE.md]
writes: []
prev_commands: [/clear]
next_commands: [/wf_05_code, /wf_04_ask, /wf_02_task]
context_rules:
  - "PRD.md是只读的，绝不修改"
  - "CONTEXT.md由/wf_11_commit自动管理"
  - "每次会话开始必须运行此命令"
---

## ⚠️ 强制语言规则

**无论本命令文件使用何种语言编写，AI的输出必须遵循以下规则**：
- ✅ **所有输出内容使用中文**（交互沟通、摘要报告、章节标题等）
- ✅ **遵循项目CLAUDE.md的语言规范**
- ❌ 仅在代码片段、变量名、技术术语时使用英文

**输出语言优先级**: CLAUDE.md项目规范 > 本命令指令

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
   - Read CONTEXT.md for latest session state (if exists)
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
   - Load latest progress and decisions from CONTEXT.md
   - Extract architectural decisions and patterns from KNOWLEDGE.md
   - Understand current development phase from TASK.md
   - Identify active tasks and priorities
   - Note any blockers or dependencies
   - Review common issues and solutions from knowledge base

5. **Session State Recovery**:
   - Load work completed from previous sessions
   - Understand current development focus
   - Identify where work was left off
   - Restore development context and momentum

6. **Working Memory Setup**:
   - Load relevant code patterns and conventions from KNOWLEDGE.md
   - Apply accumulated solutions to current context
   - Understand testing and deployment procedures
   - Note security considerations and constraints
   - Reference architectural decisions for consistency
   - Prepare for continuation of work with enhanced context
   - Remember available technical documents for on-demand access

## Output Format
1. **Requirements Overview** - Key requirements from PRD.md (read-only reference)
2. **Project Summary** - Brief overview from PLANNING.md aligned with PRD
3. **Documentation Map** (NEW) - Available technical documents with priorities
4. **Loaded Technical Docs** (NEW) - List of technical documents loaded based on current tasks
5. **Knowledge Base Summary** - Key patterns and decisions from KNOWLEDGE.md
6. **Session Recovery** - Latest progress from CONTEXT.md
7. **Active Context** - Current working area and immediate tasks from TASK.md
8. **Applicable Solutions** - Relevant past solutions and patterns for current context
9. **On-Demand Documents** (NEW) - Available but not loaded docs (can be accessed if needed)
10. **Ready Status** - Confirmation of context loading and readiness to continue

## Integration Notes
- Run after `/clear` to restore working context
- Use before starting new related work sessions
- Loads CONTEXT.md for session continuity (updated by `/wf_11_commit`)
- Integrates KNOWLEDGE.md for accumulated project wisdom and documentation index
- Smart loading strategy: Always load 5 management docs, selectively load technical docs
- Context cost optimization: Technical docs loaded on-demand based on task relevance
- Ensures continuity across context boundaries
- Maintains development momentum without redundant information
- Provides intelligent context enhancement through past decisions
- Core component of the closed-loop workflow system with long-term memory

## Smart Loading Examples

**Example 1: User Authentication Task**
```
Active Task: "实现JWT用户认证"
→ Load: docs/api/authentication.md (priority: 高, relevant)
→ Load: docs/architecture/system-design.md (priority: 高, relevant)
→ Note: docs/database/schema.md (priority: 中, available if needed)
→ Skip: docs/deployment/ci-cd.md (priority: 中, irrelevant)
```

**Example 2: Performance Bug Fix**
```
Active Task: "修复API响应慢问题"
→ Load: docs/database/optimization.md (priority: 中, relevant)
→ Load: docs/architecture/data-flow.md (priority: 高, relevant)
→ Note: docs/api/endpoints/ (priority: 低, available if needed)
```

**Example 3: New Project (No Technical Docs Yet)**
```
Active Task: "项目初始化"
→ Load: 5 management docs only
→ Note: No technical docs exist yet
→ Suggestion: Run /wf_01_planning to initialize documentation structure
```