# Claude Code Workflow Commands

高频使用场景优化的闭环工作流系统，为 Claude Code 提供项目规划、任务管理和开发最佳实践的完整集成。

---

## 🎯 核心特点

- **会话连续性**: 通过 CONTEXT.md 跨越 `/clear` 边界保持工作状态
- **自动化追踪**: 开发周期全程自动更新进度
- **质量保证**: 内置格式化、测试、代码审查
- **文档驱动**: docs/management/ 下的 PRD → PLANNING → TASK 完整追溯链
- **智能文档管理**: 四层架构 + 按需加载，上下文成本最优
- **智能文档生成** (NEW): 从代码提取文档，而非凭空编造
- **高效简洁**: 14个工作流命令覆盖完整开发生命周期

---

## 📦 安装

### 方式1：从项目目录安装（推荐）

```bash
# 克隆项目
git clone <ai_workflow_repo>
cd ai_workflow

# 运行安装脚本
./install.sh

# 加载项目上下文
/wf_03_prime
```

### 方式2：自定义安装选项

```bash
# 查看所有选项
./install.sh --help

# 示例：复制文件而不是使用符号链接
./install.sh --copy

# 示例：不创建备份
./install.sh --no-backup

# 示例：包含文档文件
./install.sh --include-docs
```

### 卸载

```bash
# 从项目目录卸载
./uninstall.sh

# 查看卸载选项
./uninstall.sh --help
```

**更多安装说明**: 查看 [INSTALL.md](./INSTALL.md)

---

## ⚠️ 开发者重要提示

**如果你要修复或扩展 workflow 本身（而非使用 workflow 开发项目）**，请务必理解以下关系：

| 你的工作 | 工作目录 | 说明 |
|---------|---------|------|
| 🔧 **修复 workflow bug** | 本 repo (`/path/to/commands`) | ✅ 在此修改源码，然后 `make install` |
| 🚀 **使用 workflow** | 任意项目目录 | ✅ 执行 `/wf_*` 命令，自动从 `~/.claude/commands/` 加载 |

**关键区别**:
- 本 repo 是**源码目录**（开发 workflow 系统）
- `~/.claude/commands/` 是**安装目录**（存放可执行命令）
- 你的项目目录是**使用目录**（调用 workflow 命令）

**详细说明**: 参见 [CLAUDE.md § 注意事项](./CLAUDE.md#注意事项)

---

## 🚀 快速开始

### 新项目初始化
```bash
/wf_01_planning "项目名称"    # 创建技术规划
/wf_02_task create           # 初始化任务追踪
```

### 日常开发流程
```bash
# 1. 会话开始（必须）
/wf_03_prime                 # 加载项目上下文

# 2. 功能开发
/wf_05_code "功能描述"       # 实现代码（自动格式化）
/wf_07_test "组件名称"       # 添加测试

# 3. 保存进度
/wf_11_commit "提交信息"     # 提交并自动更新 CONTEXT.md
```

### 会话恢复（上下文过大时）
```bash
/clear                       # 清理上下文
/wf_03_prime                 # 重新加载，无缝继续
```

---

## 📚 文档导航

本系统采用分层文档架构，各司其职：

### 核心参考文档

| 文档 | 用途 | 适用场景 |
|------|------|---------|
| **[COMMANDS.md](COMMANDS.md)** | 14个命令完整参考 | 查询命令用法、参数、依赖 |
| **[WORKFLOWS.md](WORKFLOWS.md)** | 场景化工作流指导 | 实现功能、修复Bug、质量改进、文档生成 |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | 故障排查和解决方案 | 遇到错误、问题诊断 |
| **[CLAUDE.md](CLAUDE.md)** | AI执行规则和权限 | AI行为规范、文件权限矩阵、约束规范 |
| **[DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md)** | 文档架构最佳实践 | 文档管理、上下文优化、四层架构 |

### 教程和参考文档 ⭐ NEW (2025-11-24)

约束驱动的文档生成系统 - 确保文档可控、可验证：

| 文档 | 用途 | 适用场景 |
|------|------|---------|
| **[docs/examples/doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md)** | 5分钟快速入门 | 快速理解约束驱动文档生成工作流 |
| **[docs/examples/doc_generation_decision_tree.md](docs/examples/doc_generation_decision_tree.md)** | 详细决策树和示例 | 判断是否需要文档及选择文档类型 |
| **[docs/examples/frontmatter_quick_reference.md](docs/examples/frontmatter_quick_reference.md)** | Frontmatter快速参考 | 文档元数据字段定义、常用模板、常见错误 |
| **[docs/adr/2025-11-24-constraint-driven-doc-generation.md](docs/adr/2025-11-24-constraint-driven-doc-generation.md)** | 架构决策记录 | 理解约束驱动范式的设计原因和权衡 |

**导航原则**：
- 🔍 **查命令** → COMMANDS.md
- 🛠️ **做开发** → WORKFLOWS.md
- 🐛 **解问题** → TROUBLESHOOTING.md
- 🤖 **AI规则** → CLAUDE.md
- 📚 **文档管理** → DOC_ARCHITECTURE.md
- 📝 **文档生成** → 教程和参考文档（快速指南、决策树、参考）

---

## 📁 项目文件结构

```
project/
├── docs/
│   ├── management/          # 项目管理文档
│   │   ├── PRD.md           # 项目需求文档（只读）
│   │   ├── PLANNING.md      # 技术架构和开发标准
│   │   ├── TASK.md          # 任务追踪和进度管理
│   │   └── CONTEXT.md       # 会话上下文（自动管理）
│   ├── adr/                 # 架构决策记录
│   ├── reference/           # 参考文档
│   └── ...
├── scripts/                 # 自动化工具脚本
├── KNOWLEDGE.md             # 知识库和文档索引
├── CLAUDE.md                # AI执行规则
├── wf_*.md                  # 工作流命令
└── ...
```

---

## 📋 核心文件说明

### docs/management/PRD.md ⚠️ 只读
- 项目需求和规范的权威数据源
- 业务目标和成功标准
- 利益相关者需求和约束
- **绝不自动修改**，所有决策必须对齐此文件

### docs/management/PLANNING.md
- 技术架构和设计（满足PRD需求）
- 技术栈和工具选择
- 开发标准和模式
- 测试和部署策略

### docs/management/TASK.md
- 任务列表（映射到PRD需求）
- 实时状态和进度
- 依赖和阻挡因素
- 完成历史记录

### docs/management/CONTEXT.md ⭐ 会话管理器
- 最近会话完成的工作
- 关键决策和PRD对齐注释
- 当前关注点和下一步优先项
- **由 `/wf_11_commit` 自动更新**

### KNOWLEDGE.md
- 架构决策记录（ADR）
- 常见问题解决方案
- 可重用代码模式
- 项目特定最佳实践
- **📚 文档索引中心**（NEW）: 维护技术文档地图和任务-文档关联关系

---

## 🎓 典型使用场景

### 场景1: 新功能开发
```bash
/wf_03_prime                    # 加载上下文
/wf_04_ask "架构设计问题"        # 获取设计建议（可选）
/wf_05_code "实现用户认证"       # 编写代码
/wf_07_test "认证模块"           # 添加测试
/wf_08_review                   # 代码审查
/wf_11_commit "feat: 用户认证"   # 提交保存
```
**详细流程**: 查看 [WORKFLOWS.md](WORKFLOWS.md#功能开发完整流程)

### 场景2: Bug修复
```bash
/wf_06_debug "登录500错误"       # 调试修复
/wf_07_test "登录场景"           # 验证修复
/wf_11_commit "fix: 登录问题"    # 提交
```
**详细流程**: 查看 [WORKFLOWS.md](WORKFLOWS.md#bug-修复快速路径)

### 场景3: 代码质量改进
```bash
/wf_08_review                   # 质量分析
/wf_09_refactor "组件名"         # 重构
/wf_10_optimize "性能目标"       # 优化
/wf_07_test --coverage          # 验证覆盖率
/wf_11_commit "refactor: 改进"  # 提交
```
**详细流程**: 查看 [WORKFLOWS.md](WORKFLOWS.md#代码质量改进流程)

### 场景4: 智能文档生成 ⭐ NEW (约束驱动)
```bash
# Step 1: 代码实现
/wf_03_prime                     # 加载项目上下文
/wf_05_code "实现新功能"         # 完成代码
                                # Step 8: 自动执行文档决策树判断

# Step 2: 代码审查
/wf_08_review                   # 代码审查
                                # Dimension 6: 验证文档约束合规

# Step 3: 智能文档生成（三阶段门控）
/wf_14_doc                      # Phase 1: 确定文档需求
                                # Phase 2: 成本估计 + 约束检查
                                # Phase 3: 生成文档 + Frontmatter

# Step 4: 文档维护和提交
/wf_13_doc_maintain             # 验证索引和链接
/wf_11_commit "docs: 约束驱动文档生成"  # 提交（自动验证Frontmatter）
```

**核心理念**:
- 约束驱动（KNOWLEDGE.md < 200行、单文件 < 500行、增长 < 30%）
- 从代码中提取真实信息，而非基于通用模板编造
- 三阶段门控确保文档质量和可验证性
- 自动生成元数据（Frontmatter）和索引更新

**关键文档**:
- 快速指南: [doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md) (5分钟上手)
- 决策树: [doc_generation_decision_tree.md](docs/examples/doc_generation_decision_tree.md) (判断是否需要文档)
- Frontmatter参考: [frontmatter_quick_reference.md](docs/examples/frontmatter_quick_reference.md) (元数据字段)
- ADR: [2025-11-24-constraint-driven-doc-generation.md](docs/adr/2025-11-24-constraint-driven-doc-generation.md) (设计原理)

**详细流程**: 查看 [WORKFLOWS.md](WORKFLOWS.md#场景5智能文档生成)

---

## 💡 关键最佳实践

1. **每次会话开始运行 `/wf_03_prime`** - 加载所有项目上下文
2. **让 `/wf_11_commit` 处理一切** - 自动格式化、CONTEXT.md更新、质量检查
3. **PRD.md 是只读的** - 需求修改需授权人员处理
4. **提交前运行 `/wf_08_review`** - 确保代码质量（含Dimension 6文档约束检查）
5. **使用 `--coverage` 关注测试覆盖率** - `/wf_07_test --coverage`
6. **遵守文档约束规范** - 确保文档可控和可验证（见下文）

---

## 📐 文档生成约束规范

为了确保文档系统的可控性和可验证性，所有文档生成必须遵守以下约束：

### 约束规则（硬限制）

| 约束项 | 限制值 | 目的 | 检查点 |
|--------|--------|------|--------|
| **KNOWLEDGE.md** | < 200 行 | 保持纯索引（不包含详细内容） | /wf_11_commit |
| **单个文档** | < 500 行 | 易于阅读和维护 | /wf_08_review Dimension 6 |
| **单次增长** | < 30% | 避免文档爆炸 | /wf_14_doc Phase 2 |
| **Frontmatter** | 必需（7字段） | 自动化索引和链接 | /wf_11_commit |
| **文档分层** | 管理/技术/工作/归档 | 智能按需加载 | /wf_03_prime |

### 文档类型和约束

- **Type A（架构更新）** → PLANNING.md, < 50 行 (仅"为什么"和"影响")
- **Type B（ADR）** → docs/adr/, < 200 行 (按ADR模板)
- **Type C（功能文档）** → docs/, < 500 行 (超大文件需拆分)
- **Type D（FAQ）** → KNOWLEDGE.md, < 50 行 (简洁明了)
- **Type E（无需文档）** → 代码优化、性能改进等

### 三阶段门控

1. **Phase 1** (`/wf_05_code` Step 8) - 代码完成后的文档决策树判断
2. **Phase 2** (`/wf_14_doc`) - 生成前的成本估计和约束检查
3. **Phase 3** (`/wf_08_review` Dimension 6) - 生成后的验证

### 约束超限处理

| 超限情况 | 处理方案 |
|----------|---------|
| KNOWLEDGE.md 增长 > 50% | 🔴 立即失败，需修改范围或拆分 |
| 单文件 > 500 行 | 🟠 建议拆分为多文件 |
| 无 Frontmatter | 🔴 立即失败，必须补充 |
| 内容在多处重复 | 🔴 立即失败，需使用关系链接 |

**核心理念**: 宁可拆分，也不要超限。宁可简洁，也不要冗余。

参考: [docs/adr/2025-11-24-constraint-driven-doc-generation.md](docs/adr/2025-11-24-constraint-driven-doc-generation.md)

---

## 🛠️ 快速问题解决

### 开发相关
| 问题 | 解决方案 |
|------|---------|
| 丢失项目上下文 | `/wf_03_prime` |
| 不清楚需求 | `/wf_04_ask "问题"` |
| 代码有问题 | `/wf_06_debug "错误描述"` |
| 需要帮助 | `/wf_99_help` |

### 文档生成相关 ⭐ NEW
| 问题 | 解决方案 |
|------|---------|
| 不知道是否需要文档 | 查看 [doc_generation_decision_tree.md](docs/examples/doc_generation_decision_tree.md) |
| 文档超过约束 | 参考 [约束超限处理](#约束超限处理) - 拆分或简化 |
| 不知道如何填Frontmatter | 查看 [frontmatter_quick_reference.md](docs/examples/frontmatter_quick_reference.md) |
| 想5分钟快速上手文档生成 | 查看 [doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md) |
| 想理解约束设计的原因 | 查看 [2025-11-24-constraint-driven-doc-generation.md](docs/adr/2025-11-24-constraint-driven-doc-generation.md) |
| 文档生成时提示约束违反 | 在 `/wf_14_doc` Phase 2 修改范围，或在 `/wf_13_doc_maintain` 清理旧文档后重试 |

**完整故障排查**: 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📖 系统优势

- **上下文保存**: docs/management/CONTEXT.md 自动管理，跨会话无缝继续
- **进度追踪**: docs/management/TASK.md 实时更新，始终清楚当前状态
- **质量强制**: 自动格式化、pre-commit检查、代码审查集成
- **完整闭环**: 从规划到部署的完整生命周期覆盖
- **高频优化**: 为日常高频使用场景设计，命令记忆负担最小
- **智能文档管理** (NEW): 四层架构（管理/技术/工作/归档）+ 按需加载，AI上下文成本 < 100KB

---

## 🔧 开发标准

- **代码格式**: 自动格式化（Python: black, JS/TS: prettier, C++: clang-format, Go: gofmt）
- **行结尾**: 统一Unix LF
- **尾部空格**: 零容忍（pre-commit自动检查）
- **提交信息**: `[type] subject` 格式（feat, fix, docs, refactor, test）
- **质量门控**: pre-commit钩子自动验证

---

## 📅 时间管理规范

**核心原则**: 绝不手动输入日期，总是使用命令动态获取

```bash
TODAY=$(date +%Y-%m-%d)              # 标准日期
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S) # 完整时间戳
```

**日期类型**:
- **历史日期**（创建时间、发布日期）- 创建时固定，永不修改
- **维护日期**（最后更新）- 每次编辑自动更新为当前日期
- **ADR决策日期** - 决策当天的日期

---

## 🎯 命令速查（14个）

### 基础设施 (1-3)
- `/wf_01_planning` - 创建/更新项目规划（含文档架构初始化）
- `/wf_02_task` - 管理任务追踪
- `/wf_03_prime` ⭐ - **加载项目上下文**（智能按需加载技术文档）

### 开发实现 (4-6)
- `/wf_04_ask` - 架构咨询（支持`--review-codebase`、`--think`、`--c7`）
- `/wf_05_code` - 功能实现（自动格式化，Step 8支持文档决策树）
- `/wf_06_debug` - 调试修复（支持`--quick`、`--think`、`--deep`）

### 质量保证 (7-10)
- `/wf_07_test` - 测试开发（支持`--coverage`）
- `/wf_08_review` - 代码审查（Dimension 6验证文档约束）
- `/wf_09_refactor` - 代码重构
- `/wf_10_optimize` - 性能优化

### 运维部署 (11-12)
- `/wf_11_commit` - 提交代码（自动更新CONTEXT.md、验证Frontmatter）
- `/wf_12_deploy_check` - 部署检查

### 文档管理 (13-14) ⭐ NEW
- `/wf_13_doc_maintain` - 文档结构维护和优化（清理过期文档、检查链接）
- `/wf_14_doc` ⭐ NEW - **智能文档生成**（约束驱动，从代码提取而非编造）
  - 交互式文档生成（选择类型和范围）
  - 自动成本估计和约束检查
  - 完整Frontmatter元数据生成
  - 支持 `--ui` 标志

### 支持命令 (99)
- `/wf_99_help` - 帮助系统

**详细说明**: 查看 [COMMANDS.md](COMMANDS.md)

**文档生成工作流**: 详见 [docs/examples/doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md)

---

## 🔗 扩展阅读

- **工作流指导**: [WORKFLOWS.md](WORKFLOWS.md)
- **故障排查**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **命令参考**: [COMMANDS.md](COMMANDS.md)
- **AI执行规则**: [CLAUDE.md](CLAUDE.md)

---

**最后更新**: 2025-11-24
**版本**: v3.4 (约束驱动文档生成完善版)
**架构**: 命令定义（commands/）与项目数据（根目录）清晰分离
**命令格式**: 统一使用 `/wf_XX_name` slash command 格式

**v3.4 新增** (2025-11-24) ⭐ 约束驱动文档生成系统完善:
- 📚 约束驱动文档生成详细文档（4份）:
  - `doc_generation_quick_guide.md` - 5分钟快速入门
  - `doc_generation_decision_tree.md` - 详细决策树和示例
  - `frontmatter_quick_reference.md` - Frontmatter快速参考
  - `2025-11-24-constraint-driven-doc-generation.md` - ADR记录
- 📐 完整约束规范（KNOWLEDGE.md < 200行、单文件 < 500行、增长 < 30%）
- 🔄 三阶段门控系统（Phase 1: 决策树、Phase 2: 成本估计、Phase 3: 验证）
- ✅ 100% Frontmatter完整性检查
- 🎯 约束超限处理指南

**v3.3 新增** (2025-11-21):
- 📝 `/wf_14_doc` - 智能文档生成助手（从代码提取而非编造）
- 🔍 代码库分析（技术栈、架构、API自动识别）
- 📋 文档缺口检测（对比代码 vs 现有文档）
- 🤝 交互式文档生成（用户选择需要的类型）
- 🔄 增量更新支持（不是全量重写）

**v3.2 新增** (2025-11-06):
- 🎨 Ultrathink 设计哲学（6个核心原则）
- 📚 PHILOSOPHY.md（设计思维指南）
- 🗂️ docs/adr/（架构决策记录）

**v3.1 新增**:
- 📚 四层文档架构（详见 [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md)）
- 🔍 智能按需加载（/wf_03_prime 优化）
- 📑 KNOWLEDGE.md 作为文档索引中心
- 🔄 /wf_13_doc_maintain 定期文档维护命令
- 💡 上下文成本优化（管理层 < 100KB）
