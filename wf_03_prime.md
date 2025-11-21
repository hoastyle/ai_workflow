---
command: /wf_03_prime
index: 03
phase: "基础设施"
description: "加载项目管理文档到AI上下文（会话必备）"
reads: [PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md, CLAUDE.md]
writes: []
prev_commands: [/clear]
next_commands: [/wf_05_code, /wf_04_ask, /wf_02_task]
model: haiku
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

本命令支持以下 MCP 服务器的增强，提供更智能的上下文加载：

### Serena (自动激活)

**启用**: 自动激活（无需标志）
**用途**: 语义级别的项目理解和代码索引
**自动激活**: 在 `/wf_03_prime` 执行时自动启用

**Serena 在上下文加载中的作用**:

1. **项目结构理解** – 语义层面理解代码组织:
   - 自动构建项目文件的语义索引
   - 识别核心组件和模块边界
   - 理解代码架构模式
   - 映射技术栈到代码实现

2. **知识图谱构建** – 建立项目知识网络:
   - 连接 PLANNING.md 架构与实际代码
   - 映射 KNOWLEDGE.md 决策到代码位置
   - 关联 TASK.md 任务与相关代码文件
   - 建立文档-代码双向索引

3. **智能文档加载** – 基于语义相关性选择文档:
   - 分析当前任务的代码关联
   - 智能选择相关的技术文档
   - 优先加载最相关的代码示例
   - 减少不必要的上下文加载

4. **上下文记忆持久化** – 跨会话的项目记忆:
   - 记住项目的架构模式和决策
   - 积累常用代码路径和关键位置
   - 学习团队的编码风格和偏好
   - 提供基于历史的智能建议

**Serena 增强的具体效果**:

```
无 Serena 时:
- 仅读取文本文档内容
- 依赖文件名和目录结构猜测关系
- 需要手动导航到相关代码

有 Serena 时:
- 理解文档描述的架构在代码中的位置
- 自动找到 TASK 相关的代码文件
- 快速定位 KNOWLEDGE.md 提到的模式的实现
- 提供语义级别的代码导航
```

**使用示例**:

```bash
# Serena 自动激活，无需特殊标志
/wf_03_prime

# 输出将包含:
# - 项目语义结构分析
# - 代码-文档映射关系
# - 基于当前任务的智能建议
# - 关键代码位置的快速链接
```

**Note**: Serena 在后台自动工作，提升上下文理解的深度和准确性，无需用户干预。

---

### 组合说明

`/wf_03_prime` 主要依赖 Serena 提供语义增强。不支持其他 MCP 标志，因为此命令的核心职责是加载项目上下文，而非执行分析或研究任务。

其他 MCP 服务器（Sequential-thinking, Context7, Tavily, Magic）在后续的工作命令中使用：
- `/wf_04_ask` 和 `/wf_04_research` 使用 Context7 和 Tavily
- `/wf_06_debug` 使用 Sequential-thinking 和 Serena
- `/wf_14_doc` 使用 Magic

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
10. **💡 智能推荐下一步 (NEW - Phase 2 改进)** - 基于 TASK.md 的优先任务推荐
    - 识别"🚀 下一步优先任务"部分中的第一个（最高优先级）任务
    - 显示任务名称、优先级、预计时间
    - 显示完整的"推荐命令序列"（从 TASK.md 提取）
    - 显示工作流位置标记（STEP X/Y）
    - 显示验收标准（可验证的检查清单）
    - 显示"为什么优先"的背景说明
11. **Ready Status** - Confirmation of context loading and readiness to continue

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[项目启动] → [任务规划] → [加载上下文 ← 当前] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [提交保存]
  STEP 0       STEP 0.5        STEP 1                STEP 2       STEP 3       STEP 4       STEP 5      STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_03_prime` 前，通常已经完成：

1. ✅ **项目启动** (STEP 0) - 项目规划已完成 (`/wf_01_planning`)
2. ✅ **任务规划** (STEP 0.5) - 任务列表已生成 (`/wf_02_task`)
   - 或者：直接从 `/clear` 后恢复工作（重新加载上下文）

### 📝 当前步骤

**正在执行**: `/wf_03_prime` (加载项目上下文)

**这个命令的职责**：
- 读取项目管理文档（PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md）
- 恢复会话状态和工作上下文
- 智能加载技术文档（基于当前任务相关性）
- 推荐下一步优先任务
- 为后续工作做好准备

### ⏭️ 建议下一步

**任务创建/更新完成后**，根据项目状态选择下一步：

#### 路径 1️⃣：有明确的建筑咨询需求 ✅
```bash
# 当前: 已加载项目上下文
# 下一步: 架构咨询或技术决策

/wf_04_ask "具体的技术问题或架构咨询"

# 后续: 基于咨询结果执行开发
/wf_05_code "开始功能实现"
```
**适用场景**: 需要在编码前进行技术验证、架构决策、或获取设计指导

#### 路径 2️⃣：直接开始编码实现 ✨
```bash
# 当前: 已加载项目上下文
# 下一步: 直接实现功能

/wf_05_code "实现指定的功能或任务"

# 后续: 测试和审查
/wf_07_test "功能测试验证"
/wf_08_review "代码审查"
/wf_11_commit "提交代码"
```
**适用场景**: 任务明确，不需要额外咨询，可以直接开始编码

#### 路径 3️⃣：更新任务状态后继续工作 📋
```bash
# 当前: 已加载项目上下文
# 下一步: 更新当前任务状态

/wf_02_task update "标记当前任务为活跃或更新进度"

# 然后: 根据任务选择路径1或路径2
/wf_04_ask "..." 或 /wf_05_code "..."
```
**适用场景**: 需要明确标记当前工作任务，确保任务追踪的连续性

### 📊 工作流进度提示

当你完成上下文加载时，确保输出中包含：

✅ 已完成:
- 项目需求和目标（来自 PRD.md）
- 项目架构和技术栈（来自 PLANNING.md）
- 当前任务列表和优先级（来自 TASK.md）
- 上一个会话的进度（来自 CONTEXT.md）
- 知识库和设计决策（来自 KNOWLEDGE.md）
- 相关的技术文档清单（来自文档索引）

⏭️ 下一步提示:
- 建议执行的命令（基于当前任务和项目状态）
- 推荐的工作流路径（3个选项之一）
- 当前任务的详细说明和验收标准

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 需要技术决策或架构讨论 | 路径 1 | /wf_04_ask → /wf_05_code |
| 任务明确，直接编码 | 路径 2 | /wf_05_code → /wf_07_test → /wf_08_review → /wf_11_commit |
| 需要更新任务状态 | 路径 3 | /wf_02_task update → 路径1或路径2 |
| 发现问题需要调试 | 特殊 | /wf_06_debug → /wf_07_test → /wf_11_commit |
| 不确定下一步 | 推荐 | 先执行 /wf_02_task update，再选择路径 |

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

## 智能推荐输出示例 (Phase 2 改进)

### 场景 1：P1 阶段完成，进入 P2 规划

**项目状态**：
- P1 阶段：100% 完成（所有功能实现测试）
- P2 阶段：规划中（待定义任务）

**改进后的 /wf_03_prime 输出**（第10部分）：

```
## 💡 智能推荐下一步

### ✅ **优先推荐**（基于 TASK.md 待做任务）

**任务**: 完善脚本类型注解 🔴 高优先级
- 预计时间: 30分钟
- 工作流位置: [准备阶段] → [代码实现] → [审查] → [提交]
- 为什么优先: 提高 IDE 支持和代码可维护性，为后续单元测试打基础

**推荐立即执行以下命令序列**:
```bash
# 第1步: 确认任务并标记为活跃
/wf_02_task update "完善脚本类型注解"

# 第2步: 代码实现 (主要工作)
/wf_05_code "为 scripts/frontmatter_utils.py 添加完整类型注解"

# 第3步: 代码审查
/wf_08_review

# 第4步: 提交并保存进度
/wf_11_commit "feat: 完善脚本类型注解"
```

**验收标准** (完成后可验证):
- [ ] 所有函数/方法都有完整的类型注解
- [ ] 修正 `any` → `Any` (大写)
- [ ] 代码审查通过
- [ ] 提交到仓库

**📊 工作流进度**:
- 当前: 项目上下文加载完成
- 下一步: 执行上述命令序列
- 工作流位置: [加载阶段] → [任务执行] → [验收] → [提交]

### 📋 其他待做任务 (优先级顺序)
2. 增强脚本错误处理 (🔴 高优先级, 45分钟)
3. 添加单元测试 (🟠 中优先级, 2小时)
```

### 场景 2：某个任务进行中，显示下一步

**项目状态**：
- 当前任务：完善脚本类型注解 (进行中 ⏳)

**改进后的 /wf_03_prime 输出**（第10部分）：

```
## 💡 智能推荐下一步

### ✅ **当前任务进度**

**任务**: 完善脚本类型注解 🔴 高优先级
- 状态: 进行中 ⏳ (第2步/4步)
- 工作流位置: [准备阶段] → [代码实现 ← 当前] → [审查] → [提交]

**建议继续执行**:
```bash
# 当前完成: /wf_02_task update "..."
# 当前完成: /wf_05_code "..."
# 下一步:
/wf_08_review

# 然后:
/wf_11_commit "feat: 完善脚本类型注解"
```

**📊 工作流进度**:
- 已完成: 任务确认 + 代码实现
- 下一步: 代码审查
- 工作流位置: [加载] → [执行] → [验收 ← 当前] → [提交]
```

## 实现规范 (Phase 2 - AI 执行指南)

### 提取算法

当生成"💡 智能推荐下一步"部分时，AI 应该按以下步骤操作：

1. **读取 TASK.md**
   - 定位到"## 🚀 下一步优先任务"部分
   - 检查是否存在"进行中的任务"（marked as `[⏳]` 或 `[进行中]`）

2. **任务选择逻辑**
   ```
   if 有进行中的任务:
       当前任务 = 进行中的任务
       状态 = "进行中"
       显示: 任务名 + 当前步骤进度 + 下一步建议
   else if 有待做任务:
       当前任务 = 优先级最高的待做任务 (第一个)
       状态 = "待开始"
       显示: 任务名 + 完整命令序列 + 验收标准
   else:
       显示: "所有待做任务已完成！" + 项目统计信息
   ```

3. **信息提取**
   - **任务标题**: 从"#### 任务 X️⃣：[名称]"提取
   - **优先级**: 从"[🔴 高优先级]"或"[🟠 中优先级]"提取
   - **预计时间**: 从"预计时间: X分钟"提取
   - **工作流位置**: 从"工作流位置: [...]"提取
   - **为什么优先**: 从"为什么优先:"提取
   - **命令序列**: 从"推荐命令序列"中的 bash 代码块提取
   - **验收标准**: 从"验收标准:"后的列表提取

4. **输出格式**
   - 使用 markdown 格式，清晰的层级结构
   - 使用 emoji 标记（✅、🔴、🟠、⏳、→ 等）
   - 使用代码块显示命令序列
   - 使用复选框 `[ ]` 显示验收标准

### 验证检查表

生成输出前，验证以下内容：

- [ ] 从 TASK.md 正确读取了任务信息
- [ ] 优先级标记准确（🔴 高、🟠 中、🟡 低）
- [ ] 命令序列完整且正确（包含所有步骤）
- [ ] 工作流位置标记清晰
- [ ] 验收标准可验证（不含歧义）
- [ ] 如果有多个待做任务，列出其他任务的简表
- [ ] 输出清晰易读，符合中文文档规范

### 错误处理

- **TASK.md 格式不匹配**: 提示用户"检查 TASK.md 格式是否符合 Phase 1 标准"
- **没有待做任务**: 显示"项目任务已全部完成！"并询问用户是否需要进入下一阶段
- **任务信息不完整**: 显示可用信息，并标记缺失的部分