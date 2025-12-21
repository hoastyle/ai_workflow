# CLAUDE.md

AI 编程助手的项目指南 - Claude Code 核心执行规则

本文件是**全局默认配置**，所有使用 Claude Code Workflow 系统的项目共享。

---

## 🚨 强制执行规则（ZERO TOLERANCE）

**1. 文档读取保护**：
- ❌ **严格禁止**：直接 Read 任何 >300 行的文档
- ✅ **必须使用**：`python scripts/doc_guard.py` 工具或 DocLoader
- ⚠️ **违规后果**：上下文消耗 15,000-30,000 tokens，会话轮次减少 60%+

**2. 工具强制使用**：
```bash
# 正确：使用 Doc Guard 工具
python $HOME/.claude/commands/scripts/doc_guard.py --docs "PLANNING.md,TASK.md"

# 错误：直接 Read 大文档
Read docs/architecture/LARGE_FILE.md  # ❌ 禁止
```

---

## 📋 配置层级说明

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
| **AI 会话规则** | 全局固定 🔒 | 保证一致的工作流体验 |

### 如何创建项目级配置？

在项目根目录创建 `CLAUDE.md`，只写需要覆盖的部分：

```markdown
# 项目级 CLAUDE.md

## 语言规范
1. **交互沟通**: English (international open-source project)
2. **代码提交**: English with conventional commits
```

---

## 📚 文档路由规则

**AI在遇到以下场景时，必须主动使用Read工具读取对应文档**：

| 用户问题类型 | 应读取的文档 | 说明 |
|------------|-------------|------|
| "我应该用哪个命令？" | COMMANDS.md | 命令完整参考 |
| "如何实现XX功能？" | WORKFLOWS.md | 工作流指导 |
| "遇到XX错误" | TROUBLESHOOTING.md | 故障排查 |
| "这是新项目" | README.md | 项目介绍 |

---

## 🎨 设计哲学补充 (Ultrathink)

**核心文档**: PHILOSOPHY.md - 6 个设计原则和应用指南

**何时触发自动提醒**:
- 📐 **架构决策** - "从 ultrathink 角度考虑..."
- 💻 **关键实现** - "函数/模块名字优雅吗？"
- 👁️ **设计评审** - "代码设计的优雅度如何？"
- 🔄 **重构权衡** - "这个权衡清晰吗？"

**ADR记录**: 重要决策记录在 `docs/adr/` (参见模板)

---

## 项目规范

### 语言规范（全局默认，项目可覆盖）

**默认策略**：

1. **交互沟通**: 中文（除非项目明确使用英文）
2. **文档**: 遵循项目现有文档语言
3. **代码实现**: 英文（变量、函数、类名）
4. **代码提交**: 参考最近5次提交的语言风格

**自动检测逻辑**:
```bash
1. 读取 README.md 前100行，统计中英文比例
2. 检查最近5次 git commit message 的语言
3. 如果 >70% 为英文，切换到英文模式
4. 如果存在项目级 CLAUDE.md，优先使用其配置
```

### ⚠️ 强制语言规则

**原则**: 在关键命令执行时必须强制遵循统一的语言规范。

**适用场景**：
- `/wf_03_prime` - 加载项目上下文时
- `/wf_14_doc` - 生成项目文档时
- 其他需要统一输出格式的关键命令

**输出语言优先级**：
```
项目级 CLAUDE.md 规范 > 全局 ~/.claude/CLAUDE.md > 命令文件建议 > 内置默认
```

### 项目管理文档（推荐结构）

| 文件 | 用途 | 维护规则 | 必需性 |
|-----|------|---------|--------|
| **docs/management/PRD.md** | 项目需求 | ❌ 绝不自动修改 | 可选 |
| **docs/management/PLANNING.md** | 技术规划和架构 | ✅ 重大决策后更新 | 推荐 |
| **docs/management/TASK.md** | 任务追踪 | ✅ 实时更新状态 | 推荐 |
| **docs/management/CONTEXT.md** | 会话指针文档 | 🤖 仅由/wf_11_commit管理 | 自动创建 |
| **KNOWLEDGE.md** | 知识库+文档索引 | ✅ 发现新模式和ADR时添加 | 推荐 |
| **docs/** | 技术层文档 | 📖 按需加载 | 可选 |

**灵活性说明**:
- ✅ PRD 可选（小项目可用 README.md 代替）
- ✅ 位置可变（项目可使用 `docs/` 而非 `docs/management/`）
- ✅ 格式可变（可使用 YAML/JSON 代替 Markdown）

---

## AI 执行规则

### 文件操作权限矩阵

| 文件 | 读取 | 创建 | 修改 | 删除 | 特殊规则 |
|------|:----:|:----:|:----:|:----:|---------|
| **docs/management/PRD.md** | ✅ | ❌ | ❌ | ❌ | 只读参考 |
| **docs/management/PLANNING.md** | ✅ | ✅ | ✅ | ❌ | 重大决策后更新 |
| **docs/management/TASK.md** | ✅ | ✅ | ✅ | ❌ | 完成任务后更新 |
| **docs/management/CONTEXT.md** | ✅ | ❌ | ❌ | ❌ | 仅/wf_11_commit管理 |
| **KNOWLEDGE.md** | ✅ | ✅ | ✅ | ❌ | 发现新模式时添加 |
| **代码文件** | ✅ | ✅ | ✅ | ⚠️ | 删除需用户确认 |

### 文档读取保护规则 (MANDATORY)

**目的**: 防止大文档读取导致上下文爆炸

**AI在读取任何文档前必须执行强制检查**：

#### Step 1: 文档大小检测

```bash
lines=$(wc -l < "path/to/document.md")
echo "文档行数: $lines"
```

#### Step 2: 策略选择（强制执行）

| 文档大小 | 策略 | Token消耗 |
|---------|------|----------|
| **< 100行** | 直接读取 | ~300 tokens ✅ |
| **100-300行** | 摘要模式 | ~100 tokens ✅ |
| **300-800行** | 章节模式 | ~400 tokens ⚠️ |
| **> 800行** | 禁止完整读取 | ❌ **严格禁止** |

#### Step 3: 强制执行工具：Doc Guard

**工具路径**：`$HOME/.claude/commands/scripts/doc_guard.py`

**使用方式**：
```bash
# 基础用法
python $HOME/.claude/commands/scripts/doc_guard.py --docs "PLANNING.md,TASK.md"

# 指定章节（大文档必须）
python $HOME/.claude/commands/scripts/doc_guard.py \
  --docs "docs/guides/large_guide.md" \
  --sections '{"docs/guides/large_guide.md": ["Step 3", "MCP Integration"]}'
```

**AI 职责**：
- ✅ **必须使用** doc_guard.py 工具加载所有文档
- ❌ **不得直接** 调用 Read 工具读取 >100 行的文档
- ✅ 如果工具报错，根据提示指定 `--sections` 参数

**Token预算监控**：
- 单个会话总预算：200,000 tokens
- 单次文档读取上限：1,000 tokens（警告），2,000 tokens（强制阻止）
- 累计文档读取上限：20,000 tokens（10%预算）

---

### 会话生命周期规则

#### 🚀 会话开始时（每次必须检查）

```
1. 检查用户是否运行了 /wf_03_prime
   ├─ 如果是新会话且未运行
   │  └─ 主动提示: "建议先运行 /wf_03_prime 加载项目上下文"
   │
   └─ 如果已加载上下文
       └─ 简要总结: "已加载项目上下文。当前任务: ..."
```

#### ⚡ 会话进行中（持续监控）

**决策前检查**：
- 执行任何技术决策前，确认是否符合PRD要求
- 遇到模糊需求，使用`/wf_04_ask`分析
- 不确定时，主动询问用户而不是猜测

**进度追踪**：
- 完成任务后，主动提醒更新TASK.md
- 做重大技术决策后，建议更新PLANNING.md

#### 💾 会话结束前（主动建议）

```
如果用户完成了实际工作：
1. 提醒: "建议运行 /wf_11_commit 保存进度"
2. 说明: "这会自动更新CONTEXT.md，确保下次会话能恢复工作状态"
```

### 主动行为触发规则

| 场景 | 触发条件 | 提醒内容 |
|------|---------|---------|
| **会话启动** | 新会话且未运行prime | "建议先运行 /wf_03_prime 加载上下文" |
| **任务完成** | 用户说"完成了"、"做好了" | "建议运行 /wf_11_commit 保存进度" |
| **发现问题** | 代码有明显bug | "建议使用 /wf_06_debug 系统分析" |
| **需求不清** | 用户需求模糊 | "建议使用 /wf_04_ask 进行架构咨询" |

---

## 🔌 MCP 集成和增强功能

### 什么是 MCP？

MCP (Model Context Protocol) 是 SuperClaude Framework 提供的模型扩展协议。

**当前支持的 MCP 服务器**:
- **Sequential-thinking**: 结构化多步推理
- **Context7**: 官方库文档查询
- **Serena**: 语义代码理解和项目内存
- **Tavily**: Web 搜索和实时信息
- **Magic**: UI 组件生成

### MCP 激活机制

#### 显式激活 (用户标志)

```bash
# 启用结构化思考
/wf_04_ask "技术决策" --think

# 启用官方文档
/wf_04_ask "..." --c7

# 启用 Web 搜索
/wf_04_research "..." --research

# 启用深度代码分析
/wf_06_debug "..." --deep

# 启用 UI 生成
/wf_14_doc "..." --ui
```

#### 自动激活

某些 MCP 在特定条件下自动激活：
- **Sequential-thinking**: 检测复杂决策关键词时
- **Context7**: 检测框架/库名时
- **Serena**: 在 /wf_03_prime 中加载项目上下文时

### 支持 MCP 的 wf 命令

| 命令 | 支持的 MCP | 标志 |
|------|-----------|------|
| wf_03_prime | Serena (自动) | 无 |
| wf_04_ask | Sequential-thinking, Context7, Tavily | --think, --c7, --research |
| wf_04_research | Context7, Tavily | --c7, --research |
| wf_05_code | Magic | --ui |
| wf_06_debug | Sequential-thinking, Serena | --think, --deep |
| wf_14_doc | Magic | --ui |

---

## 🛠️ 技术选型规范

### 核心原则

本项目优先开源成熟方案：

1. **优先开源** - 除非有特殊理由，不自己造轮子
2. **成熟优先** - 选择有社区、有文档、活跃维护的项目
3. **标准优先** - 选择业界标准方案，避免冷门库
4. **可维护性优先** - 考虑 5 年后的维护成本
5. **权衡明确** - 记录"为什么选这个？为什么不用那个？"

### 工作流和流程

```
需求明确
  ↓
/wf_04_ask 初步咨询 (包含开源方案调研)
  ↓
[如果需要深度研究]
  → /wf_04_research 开源方案深度评估
  → PLANNING.md 中添加"技术栈决策"部分
  → [可选] /wf_05_code 实现 PoC
  → /wf_07_test 验证方案
  → /wf_08_review 最终确认
  ↓
[决策确认后]
  → 更新 PLANNING.md 技术栈部分
  → [重大决策] 创建 ADR 记录理由
```

---

## 命令索引（简化版）

### 基础设施（1-3）
- `/wf_01_planning` - 创建/更新项目规划
- `/wf_02_task` - 管理任务追踪
- `/wf_03_prime` ⭐ - **加载项目上下文**（每次会话开始必须）

### 开发实现（4-6）
- `/wf_04_ask` - 架构咨询
- `/wf_05_code` - 功能实现
- `/wf_06_debug` - 调试修复

### 质量保证（7-10）
- `/wf_07_test` - 测试开发
- `/wf_08_review` - 代码审查
- `/wf_09_refactor` - 代码重构
- `/wf_10_optimize` - 性能优化

### 运维部署（11-12）
- `/wf_11_commit` - 提交代码
- `/wf_12_deploy_check` - 部署检查

### 文档管理（13-14）
- `/wf_13_doc_maintain` - 文档维护
- `/wf_14_doc` - 文档生成

---

## 核心文件权限速查

| 文件 | 权限 | 关键规则 |
|------|------|---------|
| **docs/management/PRD.md** | 只读 | ❌ 绝不修改 |
| **docs/management/PLANNING.md** | 读写 | ✅ 重大决策更新 |
| **docs/management/TASK.md** | 读写 | ✅ 实时状态更新 |
| **docs/management/CONTEXT.md** | 只读 | 🤖 仅/wf_11_commit写入 |
| **KNOWLEDGE.md** | 读写 | ✅ 新模式/ADR添加 |
| **docs/** | 读写 | 📖 技术层文档 |

---

## 开发标准

### 代码质量

- 📚 遵循 PLANNING.md 的代码模式
- ✅ 维护测试覆盖率要求
- 🎨 自动格式化（通过 /wf_11_commit）
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
- 使用 `/wf_11_commit`（自动处理格式化和CONTEXT.md更新）
- 提交前运行 `/wf_08_review`

### 文档格式约束

**禁止使用的格式**:
- ❌ emoji编号作为前缀: `1️⃣:`, `2️⃣:`, `3️⃣:` 等
  * 问题：emoji与冒号组合会导致字符重叠
  * 修复：改用 `Step 1:`, `1.` 或 `### 步骤 1`

**推荐的替代方式**:
- 使用纯文本编号：`Step 1`, `Step 2`
- 使用有序列表：`1.`, `2.`, `3.`
- 使用标题：`### 步骤 1`, `### 步骤 2`

---

## 快速参考

### 记住这5件事

1. 🔄 会话开始时运行 `/wf_03_prime`
2. 💻 使用 `/wf_05_code` 实现功能
3. ✅ 提交前使用 `/wf_08_review`
4. 💾 完成后用 `/wf_11_commit` 保存
5. ❓ 不确定时：
   - 查看命令 → 读取 COMMANDS.md
   - 查看流程 → 读取 WORKFLOWS.md
   - 解决问题 → 读取 TROUBLESHOOTING.md

### 典型工作流

```
项目启动:
/wf_01_planning → /wf_02_task → /wf_03_prime

功能开发:
/wf_03_prime → /wf_05_code → /wf_07_test → /wf_08_review → /wf_11_commit

Bug修复:
/wf_06_debug → /wf_07_test → /wf_11_commit
```

---

**最后更新**: 2025-12-21
**版本**: v3.4-deploy (部署通用版本)

此配置为全局默认，所有使用 Claude Code Workflow 系统的项目共享。
项目可以在项目根目录创建 CLAUDE.md 来覆盖部分规则。
