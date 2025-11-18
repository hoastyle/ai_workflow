# CLAUDE.md

AI 编程助手的项目指南 - Claude Code 核心执行规则

This file provides essential execution rules for Claude Code when working with this repository's workflow command system.

---

## 📋 配置层级说明

本文件是**全局默认配置**，通过软链接 `~/.claude/CLAUDE.md` 使所有使用命令系统的项目共享。

### 配置优先级

```
项目级 CLAUDE.md (最高优先级)
    ↓ 覆盖
全局 ~/.claude/CLAUDE.md (默认配置，本文件)
    ↓ 覆盖
Claude Code 内置默认
```

### 哪些规则可以被项目覆盖？

| 规则类型 | 全局/项目 | 说明 |
|---------|----------|------|
| **语言规范** | 项目可覆盖 ✅ | 团队项目可能使用英文 |
| **文档结构** | 项目可覆盖 ✅ | 项目可使用简化或扩展结构 |
| **Git 提交格式** | 项目可覆盖 ✅ | 遵循团队规范 |
| **命令系统核心** | 全局固定 🔒 | /wf_* 命令的存在和基本行为 |
| **文件权限矩阵** | 全局建议 ⚠️ | 项目可调整，但需谨慎 |
| **AI 会话规则** | 全局固定 🔒 | 保证一致的工作流体验 |

### 如何创建项目级配置？

**步骤 1**: 在项目根目录创建 `CLAUDE.md`
```bash
cd /path/to/your/project
touch CLAUDE.md
```

**步骤 2**: 只写需要覆盖的部分
```markdown
# 项目级 CLAUDE.md

## 语言规范
1. **交互沟通**: English (international open-source project)
2. **代码提交**: English with conventional commits

## 项目管理文档
- **README.md** - Project overview and requirements
- **docs/design/** - Architecture decisions
- **GitHub Issues** - Task tracking
```

**步骤 3**: AI 会自动合并配置
- 读取全局 `~/.claude/CLAUDE.md`（默认）
- 读取项目级 `./CLAUDE.md`（覆盖）
- 合并后执行

**注意**:
- ⚠️ 项目级配置只需写差异部分，不需要完整复制
- ✅ 未覆盖的规则仍然使用全局默认
- 💡 建议在项目 README 中说明自定义配置

---

## 📚 文档路由规则

**AI在遇到以下场景时，必须主动使用Read工具读取对应文档**：

| 用户问题类型 | 应读取的文档 | 文档路径 |
|------------|-------------|---------|
| "我应该用哪个命令？"<br/>"有哪些命令？" | 命令完整参考 | [COMMANDS.md](COMMANDS.md) |
| "如何实现XX功能？"<br/>"工作流程是什么？" | 工作流指导 | [WORKFLOWS.md](WORKFLOWS.md) |
| "遇到XX错误"<br/>"为什么失败？" | 故障排查 | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| "这是新项目"<br/>"如何开始？" | 项目介绍和快速开始 | [README.md](README.md) |

**重要**：
- 这些文档不会自动加载到AI上下文
- AI必须根据对话判断并主动使用Read工具读取
- 读取后基于文档内容回答用户问题

---

## 🎨 设计哲学补充 (Ultrathink)

> **可选的设计思维框架**，补充工作流执行规范，帮助做出更优雅的架构决策。

**核心文档**: [PHILOSOPHY.md](PHILOSOPHY.md) - 包含 6 个设计原则和应用指南

**何时触发自动提醒**:
- 📐 **架构决策** (通常在 /wf_04_ask) - "从 ultrathink 角度考虑..."
- 💻 **关键实现** (/wf_05_code) - "函数/模块名字优雅吗？"
- 👁️ **设计评审** (/wf_08_review) - "代码设计的优雅度如何？"
- 🔄 **重构权衡** (/wf_09_refactor, /wf_10_optimize) - "这个权衡清晰吗？"

**使用方式**:
1. **主动询问**: "从设计哲学的角度，怎么看这个问题？"
2. **AI自动提醒**: 遇到关键决策点时，提示考虑 ultrathink 视角
3. **ADR记录**: 重要决策的"为什么"沉淀到 docs/adr/ (见下文)

**与 CLAUDE.md 规范的关系**: **互补不冲突**
- **CLAUDE.md** = 执行规范 (何时用哪个命令、权限矩阵、文件管理)
- **PHILOSOPHY.md** = 设计思维 (如何思考、如何决策、如何优雅)

**architecture 决策记录 (ADR)**: 重要决策的"背景、选择、权衡"记录在 `docs/adr/` (参见模板)
- 🗂️ 位置: `docs/adr/` (相对于项目根目录)
- 📝 模板: `docs/adr/TEMPLATE.md`
- 📚 指南: `docs/adr/README.md`

---

## 项目规范

### 语言规范（全局默认，项目可覆盖）

**默认策略**（适用大多数项目）：

1. **交互沟通**: 中文（除非检测到项目主要语言为其他语言）
2. **文档**: 遵循项目现有文档语言
   - 检测方法：分析 README.md 前100行的主要语言
   - 如无法确定，使用中文
3. **代码实现**: 英文（变量、函数、类名）- 国际惯例
4. **代码提交**: 参考最近5次提交的语言风格

**自动检测逻辑**:
```bash
# AI 应执行的检测
1. 读取 README.md 前100行，统计中英文比例
2. 检查最近5次 git commit message 的语言
3. 如果 >70% 为英文，切换到英文模式
4. 如果存在项目级 CLAUDE.md，优先使用其配置
```

**项目级覆盖示例**:
如果项目需要不同的语言策略，在项目根目录创建 `CLAUDE.md`:
```markdown
# 项目级配置示例
## 语言规范
1. **交互沟通**: English (international team)
2. **文档**: English
3. **提交信息**: English (conventional commits)
```

### ⚠️ 强制语言规则

**原则**: 在某些命令执行时，必须强制遵循统一的语言规范，确保 AI 输出的一致性。

**适用场景**：
- `/wf_03_prime` - 加载项目上下文时（关键会话启动命令）
- `/wf_14_doc` - 生成项目文档时（必须风格一致）
- 其他需要统一输出格式的关键命令

**强制语言规则**（优先级顺序）：

1. **项目级 CLAUDE.md 优先**
   - 如果项目根目录存在 `CLAUDE.md`，其语言规范覆盖全局默认
   - 优先级：项目级 > 全局默认 > 内置默认

2. **统一性原则**
   - ✅ **所有输出内容遵循一致的语言**（交互沟通、摘要报告、章节标题等）
   - ✅ **遵循项目 CLAUDE.md 的语言规范**
   - ❌ **仅在特定情况下使用其他语言**（代码片段、变量名、技术术语）

3. **输出语言优先级**
   ```
   项目级 CLAUDE.md 规范 > 全局 ~/.claude/CLAUDE.md > 命令文件建议 > 内置默认
   ```

4. **命令级强制规则**
   - 某些关键命令可在其 Frontmatter 中定义 **强制语言规则**
   - 通过 `context_rules` 字段的 "⚠️ 强制语言规则" 部分指定
   - 示例（见 wf_03_prime.md）：
     ```
     context_rules:
       - "⚠️ 强制语言规则: 所有输出使用中文"
       - "遵循项目CLAUDE.md的语言规范"
     ```

**实施方法**：
1. 每个项目根据其 CLAUDE.md（或全局默认）选择语言
2. 在关键命令执行时（如 /wf_03_prime），AI 必须严格遵循
3. 如果命令文件中有明确的强制规则，不允许例外
4. 在输出前检查：是否符合项目级 > 全局 > 命令级的优先级

**示例检查清单**：
- [ ] 项目是否有 CLAUDE.md？ → 使用项目规范
- [ ] 全局 ~/.claude/CLAUDE.md 中的语言规范是什么？ → 作为备选
- [ ] 当前命令是否有 `context_rules` 中的强制规则？ → 严格遵循
- [ ] 当前输出是否符合优先级规则？ → 确认后输出

### 项目管理文档（推荐结构）

**标准文档结构**（命令系统推荐，项目可调整）：

| 文件 | 用途 | 维护规则 | 必需性 |
|-----|------|---------|--------|
| **docs/management/PRD.md** | 项目需求 | ❌ 绝不自动修改 | 可选 |
| **docs/management/PLANNING.md** | 技术规划和架构 | ✅ 重大决策后更新 | 推荐 |
| **docs/management/TASK.md** | 任务追踪 | ✅ 实时更新状态 | 推荐 |
| **docs/management/CONTEXT.md** | 会话指针文档 | 🤖 仅由/wf_11_commit自动管理 | 自动创建 |
| **KNOWLEDGE.md** | 知识库+文档索引 | ✅ 新模式和ADR时添加<br/>📚 维护技术文档索引 | 推荐 |
| **docs/** | 技术层文档 | 📖 按需加载，通过KNOWLEDGE.md索引 | 可选 |

**灵活性说明**:
- ✅ **PRD 可选**: 小项目可用 README.md 代替，或需求在 GitHub Issues
- ✅ **位置可变**: 项目可使用 `docs/` 而非 `docs/management/`
- ✅ **格式可变**: 可使用 YAML/JSON 代替 Markdown
- 💡 **AI 行为**:
  - 首次接触项目时，使用 Glob 工具探索实际结构
  - 如果推荐文件不存在，询问："是否需要创建 [文件]？"
  - 不强制创建，除非用户确认

**项目级覆盖示例**:
```markdown
# 项目级 CLAUDE.md
## 项目管理文档

本项目使用简化结构：
- **README.md** - 包含需求和架构说明
- **TODO.md** - 任务追踪
- **CHANGELOG.md** - 变更历史
```

---

## AI 执行规则

### 文件操作权限矩阵

**严格遵守以下权限规则**：

| 文件 | 读取 | 创建 | 修改 | 删除 | 特殊规则 |
|------|:----:|:----:|:----:|:----:|---------|
| **docs/management/PRD.md** | ✅ | ❌ | ❌ | ❌ | 只读参考。如用户要求修改，必须明确确认并警告影响 |
| **docs/management/PLANNING.md** | ✅ | ✅ | ✅ | ❌ | 重大技术决策后必须更新。记录"为什么"和PRD对齐理由 |
| **docs/management/TASK.md** | ✅ | ✅ | ✅ | ❌ | 完成任务后立即更新状态。每项任务关联PRD需求 |
| **docs/management/CONTEXT.md** | ✅ | ❌ | ❌ | ❌ | 指针文档（零冗余）。仅由`/wf_11_commit`自动管理。其他命令不得写入 |
| **KNOWLEDGE.md** | ✅ | ✅ | ✅ | ❌ | 发现架构决策、新模式或问题解决方案时添加ADR |
| **代码文件** | ✅ | ✅ | ✅ | ⚠️ | 遵循PLANNING.md标准。删除需用户确认 |

#### CONTEXT.md 指针文档模式 (SSOT 架构)

**核心原则**: CONTEXT.md 是**指针文档**而非内容文档，遵循 SSOT (Single Source of Truth) 原则。

**新职责** (零冗余):
- 记录会话的指针和元信息
- 所有内容都是指针或元数据，不重复其他文档内容

**标准模板** (~50 行，vs 旧版 300+ 行):
```markdown
# CONTEXT.md

**最后会话**: 2025-11-14 16:45
**Git 基准**: commit 9d99506

## 📍 上下文指针 (Context Pointers)

### 当前工作焦点
- 活跃任务: TASK.md § 任务1️⃣ 完善脚本类型注解 (Line 361)
- 相关架构: PLANNING.md § 技术栈 (待创建)
- 相关 ADR: KNOWLEDGE.md § ADR 2025-11-13 (开源优先)

### 会话状态
- Git commits (本次会话): 2 commits (9d99506, 292a57a)
- 修改文件数: 8 files
- 主要变更领域: 文档架构优化

### 下次启动时
- 推荐命令: /wf_03_prime
- 推荐下一步: 执行 TASK.md § 任务1️⃣ 的推荐命令序列
```

**禁止内容** (冗余信息):
- ❌ 项目状态和进度百分比 → 改为从 TASK.md 推断
- ❌ 待办任务列表 → 改为指向 TASK.md § 待做任务
- ❌ 下一步优先事项详情 → 改为指向 TASK.md § 推荐任务
- ❌ 架构决策详情 → 改为指向 KNOWLEDGE.md § ADR
- ❌ 关键学习和模式 → 改为指向 KNOWLEDGE.md § 设计模式
- ❌ 最近修改文件详情 → 改为 Git log 查询

**SSOT 映射**:
| 信息类型 | SSOT 来源 | CONTEXT.md 处理 |
|---------|----------|----------------|
| 任务状态 | TASK.md | 指针：Line X |
| 架构决策 | KNOWLEDGE.md | 指针：ADR YYYY-MM-DD |
| 代码变更 | Git log | 元数据：commits count |
| 设计模式 | KNOWLEDGE.md | 指针：§ 章节 |

**效果**:
- ✅ 信息量减少 **80%** (300+ 行 → ~50 行)
- ✅ 冗余率从 **85%** → **0%**
- ✅ 维护成本降低 **90%**
- ✅ /wf_03_prime 快速定位关键信息

**相关 ADR**: [docs/adr/2025-11-15-context-md-pointer-document.md](docs/adr/2025-11-15-context-md-pointer-document.md)

---

### 会话生命周期规则

#### 🚀 会话开始时（每次必须检查）

```
1. 检查用户是否运行了 /wf_03_prime
   ├─ 如果是新会话且未运行
   │  └─ 主动提示: "建议先运行 /wf_03_prime 加载项目上下文"
   │
   ├─ 如果是全新项目（管理文档不存在）
   │  └─ 引导: "这是新项目，建议运行 /wf_01_planning 建立规划"
   │
   └─ 如果已加载上下文
       └─ 简要总结: "已加载项目上下文。当前任务: [从docs/management/TASK.md读取]"
```

#### ⚡ 会话进行中（持续监控）

**决策前检查**：
- 执行任何技术决策前，确认是否符合PRD要求
- 遇到模糊需求，使用`/wf_04_ask`的架构师角色分析
- 不确定时，主动询问用户而不是猜测

**进度追踪**：
- 完成任务后，主动提醒更新TASK.md
- 做重大技术决策后，建议更新PLANNING.md

#### 💾 会话结束前（主动建议）

```
如果用户完成了实际工作（写代码、修复Bug、重构等）:
1. 提醒: "建议运行 /wf_11_commit 保存进度"
2. 说明: "这会自动更新CONTEXT.md，确保下次会话能恢复工作状态"
```

### 主动行为触发规则

**何时主动提醒用户**：

| 场景 | 触发条件 | 提醒内容 |
|------|---------|---------|
| **会话启动** | 新会话且未运行prime | "建议先运行 /wf_03_prime 加载上下文" |
| **任务完成** | 用户说"完成了"、"做好了" | "建议运行 /wf_11_commit 保存进度" |
| **发现问题** | 代码有明显bug | "发现潜在问题，建议使用 /wf_06_debug 系统分析" |
| **需求不清** | 用户需求模糊 | "建议使用 /wf_04_ask 进行架构咨询" |
| **PRD冲突** | 用户要求与PRD冲突 | 明确指出冲突，询问是否覆盖规则 |
| **测试缺失** | 实现功能但无测试 | "建议运行 /wf_07_test 添加测试" |

### 冲突处理决策树

```
用户请求与规则冲突
│
├─ 第1步: 识别冲突类型
│  ├─ PRD冲突: 用户要求与需求文档不符
│  ├─ 标准冲突: 违反PLANNING.md中的开发标准
│  └─ 权限冲突: 要求修改只读文件（如PRD.md）
│
├─ 第2步: 暂停执行，向用户解释
│  └─ 说明: "这个操作会 [具体影响]，因为 [规则原因]"
│
├─ 第3步: 询问确认
│  ├─ 用户明确确认 → 执行 + 记录到KNOWLEDGE.md
│  ├─ 用户取消 → 建议符合规则的替代方案
│  └─ 用户不确定 → 使用 /wf_04_ask 深入分析
```

### 异常处理规则

#### 文件不存在时的处理

| 文件 | 处理方式 |
|------|---------|
| **docs/management/PRD.md, PLANNING.md** | 提示新项目，建议: "/wf_01_planning 建立项目规划" |
| **docs/management/TASK.md** | 创建空白模板，添加初始任务: "开始第一个功能开发" |
| **docs/management/CONTEXT.md** | 正常情况，首次运行不存在。忽略 |
| **KNOWLEDGE.md** | 创建空白文件，说明: "将在工作中积累知识和决策" |

#### 命令执行失败时的处理

```
1. 使用 /wf_06_debug 的调试协调员角色分析错误
2. 尝试自动修复（如格式问题、依赖缺失）
3. 如果无法自动修复:
   ├─ 向用户清晰解释问题和原因
   ├─ 提供具体的解决步骤
   └─ 建议是否需要手动处理
4. 将问题和解决方案记录到KNOWLEDGE.md
```

### 文档管理规则 (NEW)

> 📚 基于四层文档架构的智能加载和维护策略（详见 [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md)）

#### 文档架构层次

使用workflow的项目应遵循四层文档架构：

| 层级 | 位置 | 职责 | AI加载策略 |
|------|------|------|-----------|
| **管理层** | 项目根目录 | PRD, PLANNING, TASK, CONTEXT, KNOWLEDGE | ✅ prime自动加载（5个文件） |
| **技术层** | docs/ | 技术细节文档 | 🔍 按需加载（通过KNOWLEDGE.md索引） |
| **工作层** | docs/research/ | 临时探索 | ❌ 不加载（用户可指定） |
| **归档层** | docs/archive/ | 历史文档 | ❌ 不加载 |

#### 文档读取原则

**AI在不同场景的文档加载策略**：

| 场景 | 加载策略 | 说明 |
|------|---------|------|
| **会话开始（/wf_03_prime）** | 自动加载5个管理层文档 | 成本可控，~100KB以内 |
| **解析文档索引** | 从KNOWLEDGE.md提取"📚 文档索引"章节 | 理解可用技术文档 |
| **任务相关技术实现** | 根据docs/management/TASK.md当前任务判断相关性 | 优先级=高 且 相关 → 加载 |
| **架构咨询（/wf_04_ask）** | 优先读取docs/management/PLANNING.md，必要时读取docs/architecture/ | 深度分析才加载详细文档 |
| **调试问题（/wf_06_debug）** | 查阅KNOWLEDGE.md已知问题，按需读取技术文档 | 避免盲目加载 |
| **工作层/归档层** | 不主动加载，除非用户明确指示 | 控制上下文成本 |

**加载决策逻辑**：
```
文档优先级 = 高 AND 任务相关 → 立即加载
文档优先级 = 中 AND 任务相关 → 询问或按需加载
文档优先级 = 低 OR 任务无关 → 仅记录存在，不加载
```

#### 文档维护规则

**创建技术文档时**：
- ✅ 必须在KNOWLEDGE.md中添加索引条目
  ```markdown
  | 主题 | 文档路径 | 说明 | 优先级 | 最后更新 |
  | 用户认证 | docs/api/authentication.md | JWT实现 | 高 | 2024-10-31 |
  ```
- ✅ 在KNOWLEDGE.md中建立任务-文档关联
  ```markdown
  | 任务类型 | 相关文档 |
  | 实现登录功能 | architecture/system-design.md, api/authentication.md |
  ```

**维护KNOWLEDGE.md文档索引**：
- ✅ 新技术文档 → 添加索引条目
- ✅ 文档更新 → 更新last_updated字段
- ✅ 文档废弃 → 移动到archive/，从索引移除
- ✅ 定期运行 `/wf_13_doc_maintain` 检查一致性

**定期文档整理**：
- 📅 每10次提交后提示运行 `/wf_13_doc_maintain`
- 📅 季度末（Q1/Q2/Q3/Q4）执行文档维护
- 🔍 识别过期、重复、孤立文档
- 📦 归档到docs/archive/YYYY-QX/

#### 文档分层放置规则

**何时放在管理层（根目录）**：
- ✅ 核心架构概述（不超过500行）
- ✅ 关键决策记录（ADR摘要）
- ❌ 详细技术实现（应放docs/）

**何时放在技术层（docs/）**：
- ✅ API详细文档
- ✅ 数据库设计细节
- ✅ 部署流程和配置
- ✅ 架构深度分析

**何时放在工作层（docs/research/）**：
- ✅ 技术探索Spike（前缀日期：2024-10-XX-name.md）
- ✅ 原型验证文档
- ✅ 临时研究笔记
- ⏰ 超过3个月未使用 → 考虑归档或转正

**何时归档（docs/archive/）**：
- ✅ 超过6个月未更新且无引用
- ✅ 功能已废弃
- ✅ 被新文档完全取代

#### 文档Frontmatter元数据规范

**为什么使用Frontmatter？**

Frontmatter是一种标准化的文档元数据格式（YAML），用于：
- ✅ 快速定位文档与代码的关系
- ✅ 自动化维护文档间的交叉引用
- ✅ 支持脚本化的文档分析和查询
- ✅ 降低人工维护成本
- ✅ 在单个文件内部定义关系，易于版本控制

**标准Frontmatter模板**

**📋 完整规范**: 详见 [commands/docs/reference/FRONTMATTER.md](commands/docs/reference/FRONTMATTER.md)

**快速参考**：
```yaml
---
# 必需字段（7个）
title: "文档标题"
description: "一句话描述文档的核心内容"
type: "技术设计 | 系统集成 | API参考 | 教程 | 故障排查 | 架构决策"
status: "草稿 | 完成 | 待审查"
priority: "高 | 中 | 低"
created_date: "2025-11-10"
last_updated: "2025-11-10"

# 推荐字段（关系网络）
related_documents: []  # 相关文档
related_code: []       # 实现代码

# 可选字段
tags: []
authors: ["Claude"]
version: "1.0"
---
```

**字段说明**（完整版见规范文档）：
- **必需（7个）**: title, description, type, status, priority, created_date, last_updated
- **推荐（2个）**: related_documents（文档关系）, related_code（代码链接）
- **可选（4个）**: tags, authors, version, next_review_date

**使用规则**（详见规范文档 § 使用规则）：

1. **创建**: `/wf_14_doc` 自动生成标准 frontmatter
2. **修改**: `/wf_11_commit` 自动更新 `last_updated`
3. **发布**: `/wf_11_commit` 验证完整性（⚠️ 从项目根目录运行）
4. **维护**: `/wf_13_doc_maintain` 定期检查一致性

**成本分析**（详见规范文档 § 成本分析）：
- 创建成本：低（自动生成）
- 维护成本：极低（自动更新）
- 查询收益：10倍+效率提升

#### 上下文成本优化

**成功指标**：
- 管理层文档总大小 < 100KB ✓
- 80%的任务只需加载0-2个技术文档 ✓
- 文档索引准确率 > 90% ✓
- 所有技术文档都有完整的frontmatter ✓

**AI主动提醒**：
- 管理层文档 > 100KB → 建议精简或外放到技术层
- 发现未索引的技术文档 → 提醒更新KNOWLEDGE.md
- 发现文档缺少frontmatter → 提醒补充
- 提交次数达到10次 → 提示运行 `/wf_13_doc_maintain`

#### 文档生成约束规范（约束驱动） (NEW - 2025-11-18)

**核心原则**: 在文档生成时就内置约束检查，而非事后清理（详见 ADR 2025-11-18-constraint-driven-documentation-generation）

**三阶段约束执行系统**:

| 阶段 | 执行命令 | 职责 | 输出 |
|------|--------|------|------|
| **Phase 1** | `/wf_05_code` Step 8 | 代码完成后的文档决策树 | 确定需要哪些文档（类型、位置、大小）|
| **Phase 2** | `/wf_14_doc` | 文档生成的成本估计和门控 | 生成前预估成本，超限时拒绝 |
| **Phase 3** | `/wf_08_review` Dimension 6 | 审查时的架构合规性检查 | 再次验证 Frontmatter、分层、约束 |

**成本约束规范（硬限制）**:

```
文档大小约束:
┌────────────────────────────────┬────────┬──────────────┐
│ 文档类型 | 位置 | 约束 | 说明 |
├────────────────────────────────┼────────┼──────────────┤
│ 类型A (架构) | PLANNING.md | < 50行 | 仅"为什么"和"架构影响" |
│ 类型B (决策) | docs/adr/ | < 200行 | 遵循 ADR 模板 |
│ 类型C (功能) | docs/ | < 500行 | 复杂 API 分多文件 |
│ 类型D (问题) | KNOWLEDGE.md | < 50行 | 月末批量审查 |
│ 类型E (无文档) | - | - | 代码优化、变量改进等 |
└────────────────────────────────┴────────┴──────────────┘

增长率约束 (per commit):
  - KNOWLEDGE.md 增长: < 20%
  - docs/ 增长: < 30%

索引约束:
  - KNOWLEDGE.md 总行数: < 200 行（仅索引和摘要）
  - 所有新文档: 必须有完整 Frontmatter（7个必需字段）
```

**执行流程**:

```
代码实现完成
  ↓
Step 1 (在 /wf_05_code Step 8.1-8.2):
  确定文档需求（Q1-Q5检查清单）
  按 A/B/C/D/E 类型分层
  ↓
Step 2 (在 /wf_14_doc 中):
  ✅ 估计每个文档的成本
  ✅ 计算对 KNOWLEDGE.md 和 docs/ 的影响
  ✅ 判断是否超过约束阈值

  若超限 → 提示用户：
    ① 修改文档范围（减少内容）
    ② 拆分成多个 commit
    ③ 先清理旧文档，再添加新文档

  若符合 → 生成文档 + 生成 Frontmatter
  ↓
Step 3 (在 /wf_08_review Dimension 6 中):
  ✅ 验证 Frontmatter 完整性
  ✅ 重新计算成本影响
  ✅ 检查分层正确性
  ✅ 验证无重复内容

  若不符合 → 返回改进要求
  若符合 → 提示进入 /wf_11_commit
  ↓
Step 4 (在 /wf_11_commit 中):
  在 commit message 中记录文档决策：
    - 类型和位置
    - 成本影响
    - 决策时间戳
```

**文档分类决策树（来自 /wf_05_code Step 8.2）**:

```
改动类型 → 文档类型 → 位置 → 约束 → 自动分层

Q1: 改动了公开 API/函数/类?
├─ YES → Type C 或 B (看是否有设计决策)
└─ NO → Q2

Q2: 改变了现有功能的行为?
├─ YES → Type A 或 D (架构变化 vs 最佳实践)
└─ NO → Q3

Q3: 使用了新的库/框架/技术?
├─ YES → Type B (创建 ADR 记录决策原因)
└─ NO → Q4

Q4: 改变了系统架构或设计?
├─ YES → Type A (更新 PLANNING.md)
└─ NO → Q5

Q5: 引入了新的配置或部署流程?
├─ YES → Type C (部署/配置文档)
└─ NO → Type E (无需文档)
```

**强制门控点（三个地方必须通过）**:

1. **生成时** (/wf_14_doc):
   ```bash
   成本估计 → 判断超限 → 若超限拒绝生成
   python scripts/frontmatter_utils.py validate docs/
   ```

2. **审查时** (/wf_08_review Dimension 6):
   ```
   6项检查清单 → 必须全部通过
   ✅ 分层正确性
   ✅ 成本控制
   ✅ Frontmatter 完整性
   ✅ 内容重复检查
   ✅ 指针关系
   ✅ 审查合规
   ```

3. **提交时** (/wf_11_commit):
   ```
   自动检查：
   - Frontmatter 验证
   - 索引更新（python scripts/frontmatter_utils.py update-index）
   - 无破损链接
   ```

**相关命令和工具**:

| 命令 | 用途 | 约束检查 |
|------|------|--------|
| `/wf_05_code` Step 8 | 代码后的文档决策 | Step 8.4 成本门控 |
| `/wf_14_doc` | 文档生成 | 步骤 1.5 + 5.1-5.2 |
| `/wf_08_review` Dimension 6 | 代码审查 | 6项检查清单 |
| `/wf_11_commit` | 提交代码 | Frontmatter 验证 |

**工具脚本**:

```bash
# Frontmatter 生成和验证
python scripts/frontmatter_utils.py generate <doc_path>
python scripts/frontmatter_utils.py validate <doc_path>
python scripts/frontmatter_utils.py validate-batch docs/
python scripts/frontmatter_utils.py update-index KNOWLEDGE.md

# 文档关系图
python scripts/doc_graph_builder.py generate docs/
```

**超限处理**:

🔴 **立即失败** (必须立即修复):
- KNOWLEDGE.md 增长 > 50%
- 新文档无 Frontmatter
- 内容在 2+ 个地方重复
- 文档内容与代码不符

🟠 **要求改进** (可在下个 commit 修复):
- KNOWLEDGE.md 增长 20-50%
- 文档 > 500 行
- Frontmatter 缺少推荐字段
- 没有链接到相关文档

**修复选项**:
1. 减少文档范围（删除非关键部分）
2. 拆分成多个 < 500 行的文件
3. 先清理旧文档（运行 `/wf_13_doc_maintain`）
4. 分多个 commit 逐步添加

### 命令调用规则

**工作流命令是Slash Commands**：
- 格式: `/wf_XX_name`（不是文件路径）
- 按需调用，详细步骤在命令文件中
- AI负责判断"何时调用哪个命令"

**示例**：
```
❌ 错误: "运行 wf_03_prime.md"
✅ 正确: "运行 /wf_03_prime"
```

---

## 🛠️ 技术选型规范 (NEW - 优先开源方案)

### 核心原则

本项目在选择技术栈时遵循以下原则，**优先开源成熟方案**：

1. **优先开源** - 除非有特殊理由，不自己造轮子
2. **成熟优先** - 选择有社区、有文档、活跃维护的项目
3. **标准优先** - 选择业界标准方案，避免冷门库
4. **可维护性优先** - 考虑 5 年后的维护成本
5. **权衡明确** - 记录"为什么选这个？为什么不用那个？"

### 工作流和流程

**完整的技术选型流程**:

```
需求明确 (功能需求、约束条件)
  ↓
/wf_04_ask 初步咨询 (包含开源方案调研)
  ↓
[如果需要深度研究]
  → /wf_04_research 开源方案深度评估
  ↓
  → PLANNING.md 中添加"技术栈决策"部分记录
  ↓
  → [可选] /wf_05_code 实现 PoC 验证方案可行性
  ↓
  → /wf_07_test 验证方案解决方案可行性
  ↓
  → /wf_08_review 最终确认方案是否满足需求
  ↓
[决策确认后]
  → 更新 PLANNING.md 技术栈部分
  → [如果重大决策] 创建 ADR 记录决策和理由
  → /wf_02_task 添加库集成、依赖管理任务
```

### 文档规范

**PLANNING.md 中的技术栈部分模板**:

```markdown
## 技术栈决策

### 功能 X - 库选择

**需求**: [简述需要什么]
**候选方案**:
- 方案 A: [库名] (优势/劣势)
- 方案 B: [库名] (优势/劣势)
- 方案 C: [库名] (优势/劣势)

**选择**: [推荐的库]
**理由**:
- ✅ [优势1]
- ✅ [优势2]
- ✅ [优势3]

**成本**: [集成成本、学习曲线]
**风险**: [潜在问题、社区稳定性、版本升级风险]
**决策日期**: YYYY-MM-DD
**相关ADR**: [如果有]
```

### 架构咨询清单

在执行 `/wf_04_ask` 进行技术咨询时，确保：

- [ ] 列举了至少 3 个相关开源方案
- [ ] 分析了各方案的优缺点（功能、性能、社区活跃度、维护状态）
- [ ] 查阅了 License 兼容性（MIT、Apache、GPL 等）
- [ ] 评估了集成成本 vs 自己实现的成本对比
- [ ] 查询了 KNOWLEDGE.md 中的类似决策历史
- [ ] 记录了最终决策和选择理由
- [ ] [重大决策] 考虑是否需要创建 ADR

### 架构决策记录 (ADR)

**何时创建 ADR**:
- 技术栈的重大决策（选择新框架、数据库等）
- 多个方案间的权衡涉及长期影响
- 决策与公司/项目标准有偏差需要解释

**ADR 文件位置**: `docs/adr/YYYY-MM-DD-technology-choice.md`

**参考**: `docs/adr/TEMPLATE.md` 中的完整模板

---

## 命令索引（简化版）

**完整参考**: 查询详细说明时，主动读取 [COMMANDS.md](COMMANDS.md)

### 基础设施（1-3）
- `/wf_01_planning` - 创建/更新项目规划
- `/wf_02_task` - 管理任务追踪
- `/wf_03_prime` ⭐ - **加载项目上下文**（每次会话开始必须）

### 开发实现（4-6）
- `/wf_04_ask` - 架构咨询（支持`--review-codebase`）
- `/wf_05_code` - 功能实现（自动格式化）
- `/wf_06_debug` - 调试修复（支持`--quick`）

### 质量保证（7-10）
- `/wf_07_test` - 测试开发（支持`--coverage`）
- `/wf_08_review` - 代码审查
- `/wf_09_refactor` - 代码重构
- `/wf_10_optimize` - 性能优化

### 运维部署（11-12）
- `/wf_11_commit` - 提交代码（自动更新CONTEXT.md）
- `/wf_12_deploy_check` - 部署检查

### 文档管理（13-14）
- `/wf_13_doc_maintain` - 文档结构维护和优化
- `/wf_14_doc` - 智能文档生成（从代码提取）

### 支持命令（99）
- `/wf_99_help` - 帮助系统

**命令详细说明**: 当用户询问具体命令时，读取 [COMMANDS.md](COMMANDS.md)

---

## 核心文件权限速查

| 文件 | 权限 | 关键规则 |
|------|------|---------|
| **docs/management/PRD.md** | 只读 | ❌ 绝不修改 |
| **docs/management/PLANNING.md** | 读写 | ✅ 重大决策更新 |
| **docs/management/TASK.md** | 读写 | ✅ 实时状态更新 |
| **docs/management/CONTEXT.md** | 只读 | 🤖 仅/wf_11_commit写入 |
| **KNOWLEDGE.md** | 读写 | ✅ 新模式/ADR添加<br/>📚 文档索引中心 |
| **docs/** | 读写 | 📖 技术层文档，按需加载 |

---

## 开发标准

### 代码质量

- 📚 遵循PLANNING.md的代码模式
- ✅ 维护测试覆盖率要求
- 🎨 自动格式化（通过`/wf_11_commit`）
- 🚫 零容忍尾部空格
- 📝 统一Unix行结尾（LF）

### Git提交工作流

**提交信息格式**：
```
[type] subject

body
```

**类型标签**：
- `[feat]` - 新功能
- `[fix]` - Bug修复
- `[docs]` - 文档更新
- `[refactor]` - 代码重构
- `[test]` - 测试添加

**最佳实践**：
- 使用`/wf_11_commit`（自动处理格式化和CONTEXT.md更新）
- 提交前运行`/wf_08_review`

### 时间点管理规范

**核心原则**：绝不手动输入日期，总是使用命令动态获取

```bash
# 标准时间获取
TODAY=$(date +%Y-%m-%d)              # 今天
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S) # 完整时间戳
```

**日期类型规则**：
1. **历史日期**（创建时间、发布日期）- 一旦确定，永不修改
2. **维护日期**（最后更新）- 每次修改时自动更新为当前日期
3. **ADR决策日期** - 决策当天的日期

---

## 快速参考

### 记住这5件事

1. 🔄 会话开始时运行 `/wf_03_prime`
2. 💻 使用 `/wf_05_code` 实现功能
3. ✅ 提交前使用 `/wf_08_review`
4. 💾 完成后用 `/wf_11_commit` 保存
5. ❓ 不确定时：
   - 查看命令 → 读取 [COMMANDS.md](COMMANDS.md)
   - 查看流程 → 读取 [WORKFLOWS.md](WORKFLOWS.md)
   - 解决问题 → 读取 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### 典型工作流

```
项目启动:
/wf_01_planning → /wf_02_task → /wf_03_prime

功能开发:
/wf_03_prime → /wf_05_code → /wf_07_test → /wf_08_review → /wf_11_commit

Bug修复:
/wf_06_debug → /wf_07_test → /wf_11_commit

会话管理:
/wf_03_prime (开始) → 工作 → /wf_11_commit (保存) → /clear → /wf_03_prime (恢复)
```

**详细工作流**: 用户询问具体场景时，读取 [WORKFLOWS.md](WORKFLOWS.md)

---

**最后更新**: 2025-11-07
**版本**: v3.3 (增加智能文档生成)

该系统确保开发连续性、质量维护和高效的进度追踪，同时通过文档路由机制和四层架构减少AI上下文消耗。

**新增功能** (v3.3):
- 📝 `/wf_14_doc` - 智能文档生成助手（从代码提取而非编造）
- 🔍 代码库分析（技术栈、架构、API自动识别）
- 📋 文档缺口检测（对比代码与现有文档）
- 🤝 交互式文档生成（用户选择需要的类型）
- 🔄 增量更新支持（不是全量重写）

**既有功能** (v3.2):
- 🎨 Ultrathink 设计哲学补充（6个核心原则）
- 📚 PHILOSOPHY.md（设计思维指南）
- 🗂️ docs/adr/ 目录（架构决策记录）
- 🤖 自动提醒机制（关键决策点提示 ultrathink 视角）

**既有功能** (v3.1):
- 📚 四层文档架构（管理层/技术层/工作层/归档层）
- 🔍 智能按需加载（基于任务相关性和文档优先级）
- 📑 KNOWLEDGE.md作为文档索引中心
- 🔄 `/wf_13_doc_maintain` 定期文档维护命令
