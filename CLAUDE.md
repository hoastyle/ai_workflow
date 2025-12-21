# CLAUDE.md

Claude Code Workflow 源码开发规范

本文件是**源码目录专用**，规定在该仓库中进行 Workflow 开发的规则。
部署到用户系统的全局规则见 CLAUDE_DEPLOY.md。

---

## 📌 核心说明

### 文件职责分离

| 文件 | 用途 | 应用场景 |
|------|------|---------|
| **CLAUDE.md**（本文件） | 源码开发规范 | 该 repo 中进行 Workflow 开发 |
| **CLAUDE_DEPLOY.md** | 全局通用规范 | 部署到用户系统 (`~/.claude/CLAUDE.md`) |

### 如何使用

1. **源码开发**: 在该 repo 中工作时，遵循本 CLAUDE.md
2. **部署**: 运行 `install.sh` 自动部署 CLAUDE_DEPLOY.md 到 `~/.claude/CLAUDE.md`
3. **用户项目**: 项目根目录创建 `CLAUDE.md` 来覆盖全局规则

---

## 📂 项目结构

该 repo 是 Claude Code Workflow 的源码目录，包含：

```
commands/
├── CLAUDE.md (本文件 - 源码规范)
├── CLAUDE_DEPLOY.md (部署规范)
├── install.sh (部署脚本)
├── commands/ (workflow 命令实现)
│   ├── wf_01_planning.md
│   ├── wf_02_task.md
│   ├── ... (wf_03 - wf_14)
├── commands/lib/ (工具库)
│   ├── agent_coordinator.py
│   ├── doc_loader.py
│   └── ... (其他工具)
├── scripts/ (辅助脚本)
│   ├── doc_guard.py
│   ├── frontmatter_utils.py
│   └── ... (其他脚本)
├── docs/ (技术文档)
│   ├── guides/ (工作流指南)
│   ├── adr/ (架构决策记录)
│   └── ... (其他文档)
└── tests/ (测试)
```

---

## 🚨 源码开发规则

### 命令开发标准

所有 `wf_*.md` 命令文件必须：

1. **遵循 Frontmatter 格式**
   ```markdown
   ---
   title: "命令标题"
   version: "1.0"
   context_rules:
     - "强制语言规则: 中文"
     - "其他规则..."
   ---
   ```

2. **实现标准流程结构**
   - Step 0: 加载工作流指南
   - Step 1: 任务确认
   - Step 2-N: 具体实现步骤
   - 最后: 后续路径推荐

3. **包含完整的 AI 执行协议**
   - 强制执行规则清单
   - 决策树和流程图
   - 输出模板

### 工具库开发标准

所有 `commands/lib/*.py` 文件必须：

1. **符合 PEP 8 规范**
2. **包含完整文档字符串**
3. **有单元测试覆盖 (≥80%)**
4. **支持错误处理和日志**

### 脚本开发标准

所有 `scripts/*.py` 文件必须：

1. **支持命令行参数**
2. **有 --help 选项**
3. **输出清晰的日志和错误信息**
4. **支持绝对路径 (使用 $HOME 扩展)**

### 文档开发标准

所有技术文档必须：

1. **有完整的 Frontmatter 元数据**
2. **遵循 Markdown 格式约束** (避免 emoji 编号)
3. **包含关键概念索引**
4. **链接到相关文档和代码**

---

## 📖 项目管理文档

### 推荐文档结构

| 文件 | 用途 | 维护规则 |
|-----|------|---------|
| **docs/management/PRD.md** | 项目需求 | 只读参考 |
| **docs/management/PLANNING.md** | 技术规划 | 重大决策后更新 |
| **docs/management/TASK.md** | 任务追踪 | 实时更新状态 |
| **docs/management/CONTEXT.md** | 会话指针 | 仅 /wf_11_commit 管理 |
| **KNOWLEDGE.md** | 知识库 | 发现新模式时添加 |

### 核心文件权限

| 文件 | 权限 | 说明 |
|------|------|------|
| **CLAUDE.md** | 读写 | 源码规范，开发时遵循 |
| **CLAUDE_DEPLOY.md** | 读写 | 部署规范，部署时使用 |
| **install.sh** | 读写 | 部署脚本，执行安装 |
| **docs/adr/** | 读写 | 架构决策记录 |
| **commands/** | 读写 | 命令实现 |
| **commands/lib/** | 读写 | 工具库 |
| **scripts/** | 读写 | 辅助脚本 |

---

## 🔄 开发工作流

### 开发流程

```
任务确认 (TASK.md)
    ↓
设计架构 (PLANNING.md)
    ↓
实现功能 (/wf_05_code)
    ↓
编写测试 (/wf_07_test)
    ↓
代码审查 (/wf_08_review)
    ↓
提交代码 (/wf_11_commit)
    ↓
部署验证 (install.sh + 测试)
```

### 命令开发检查清单

在实现新命令或修改现有命令时，必须确认：

- [ ] ✅ 命令有完整的 Frontmatter
- [ ] ✅ 命令包含 AI 执行协议（Step 0-N）
- [ ] ✅ 包含任务确认流程 (Step 1)
- [ ] ✅ 包含后续路径推荐
- [ ] ✅ 所有超链接指向相对路径（支持部署后访问）
- [ ] ✅ 遵循强制语言规则 (中文)
- [ ] ✅ 无 emoji 编号 (改用纯文本)
- [ ] ✅ 在 /wf_08_review 中审查过
- [ ] ✅ 包含相关单元测试

### 部署前检查

在运行 `install.sh` 前，必须：

- [ ] ✅ 所有单元测试通过 (`pytest tests/`)
- [ ] ✅ 代码格式符合规范 (无尾部空格，LF 行结尾)
- [ ] ✅ 所有文档链接有效
- [ ] ✅ 文档中的脚本路径使用 `$HOME` 变量
- [ ] ✅ 本地 git 仓库无未提交的改动

---

## 📋 项目规范

### 本源码仓库的语言规范

**源码开发规范**:
1. **交互沟通**: 中文（所有命令、文档必须使用中文）
2. **代码实现**: 英文（变量、函数、类名遵循国际惯例）
3. **代码注释**: 中文（便于国内开发者理解）
4. **代码提交**: 中文（参考最近5次提交）

**全局规则**: 详见 CLAUDE_DEPLOY.md（部署后用于用户系统）

---

## ⚠️ 源码开发强制规则

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

### 📏 文档读取保护规则 (MANDATORY - 严格执行)

**目的**: 防止大文档读取导致上下文爆炸（单次可消耗 3,000-6,000 tokens）

**AI在读取任何文档前必须执行强制检查**：

#### Step 1: 文档大小检测

```bash
# 必须先检查文件行数
lines=$(wc -l < "path/to/document.md")
echo "文档行数: $lines"
```

#### Step 2: 策略选择（强制执行）

根据文档大小选择加载策略：

| 文档大小 | 策略 | 工具 | Token消耗 |
|---------|------|------|----------|
| **< 100行** | 直接读取 | `Read` tool | ~300 tokens ✅ 安全 |
| **100-300行** | 摘要模式 | `DocLoader.load_summary()` | ~100 tokens ✅ 推荐 |
| **300-800行** | 章节模式 | `DocLoader.load_sections()` | ~400 tokens ⚠️ 必须 |
| **> 800行** | 禁止完整读取 | 必须分段加载 | ❌ **严格禁止** |

### 文档读取保护

详见 CLAUDE_DEPLOY.md（部署到用户系统时使用的全局规则）

本源码仓库使用 `scripts/doc_guard.py` 工具进行文档加载管理。

---

## ✅ 开发检查清单

在提交代码前，确认以下项目：

- [ ] 所有源码遵循 PEP 8 规范
- [ ] 命令文件有完整的 Frontmatter
- [ ] 命令包含 AI 执行协议（Step 0-N）
- [ ] 所有文档链接使用相对路径
- [ ] 脚本路径使用 $HOME 变量
- [ ] 无 emoji 编号（改用纯文本）
- [ ] 所有单元测试通过
- [ ] 本地 git 仓库无未提交改动
- [ ] 经过 /wf_08_review 审查

---

**最后更新**: 2025-12-21
**版本**: v3.4-src (源码开发版本)
