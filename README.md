# Claude Code Workflow Commands

高频使用场景优化的闭环工作流系统，为 Claude Code 提供项目规划、任务管理和开发最佳实践的完整集成。

---

## 🎯 核心特点

- **会话连续性**: 通过 CONTEXT.md 跨越 `/clear` 边界保持工作状态
- **自动化追踪**: 开发周期全程自动更新进度
- **质量保证**: 内置格式化、测试、代码审查
- **文档驱动**: PRD.md → PLANNING.md → TASK.md 完整追溯链
- **智能文档管理**: 四层架构 + 按需加载，上下文成本最优
- **智能文档生成** (NEW): 从代码提取文档，而非凭空编造
- **高效简洁**: 14个工作流命令覆盖完整开发生命周期

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

| 文档 | 用途 | 适用场景 |
|------|------|---------|
| **[COMMANDS.md](COMMANDS.md)** | 15个命令完整参考 | 查询命令用法、参数、依赖 |
| **[WORKFLOWS.md](WORKFLOWS.md)** | 场景化工作流指导 | 实现功能、修复Bug、质量改进 |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | 故障排查和解决方案 | 遇到错误、问题诊断 |
| **[CLAUDE.md](CLAUDE.md)** | AI执行规则和权限 | AI行为规范、文件权限矩阵 |
| **[DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md)** | 文档架构最佳实践 (NEW) | 文档管理、上下文优化 |

**导航原则**：
- 🔍 **查命令** → COMMANDS.md
- 🛠️ **做开发** → WORKFLOWS.md
- 🐛 **解问题** → TROUBLESHOOTING.md
- 🤖 **AI规则** → CLAUDE.md
- 📚 **文档管理** → DOC_ARCHITECTURE.md (NEW)

---

## 📁 项目文件结构

```
.claude/
├── PRD.md              # 项目需求文档（只读）
├── PLANNING.md         # 技术架构和开发标准
├── TASK.md             # 任务追踪和进度管理
├── CONTEXT.md          # 会话上下文（自动管理）
├── KNOWLEDGE.md        # 知识库和ADR
└── commands/           # 工作流命令定义
    ├── wf_01_planning.md
    ├── wf_02_task.md
    ├── ... (其他命令)
    ├── COMMANDS.md
    ├── WORKFLOWS.md
    ├── TROUBLESHOOTING.md
    └── CLAUDE.md
```

---

## 📋 核心文件说明

### PRD.md ⚠️ 只读
- 项目需求和规范的权威数据源
- 业务目标和成功标准
- 利益相关者需求和约束
- **绝不自动修改**，所有决策必须对齐此文件

### PLANNING.md
- 技术架构和设计（满足PRD需求）
- 技术栈和工具选择
- 开发标准和模式
- 测试和部署策略

### TASK.md
- 任务列表（映射到PRD需求）
- 实时状态和进度
- 依赖和阻挡因素
- 完成历史记录

### CONTEXT.md ⭐ 会话管理器
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

### 场景4: 智能文档生成 ⭐ NEW
```bash
/wf_05_code "实现新功能"         # 完成代码
/wf_08_review                   # 代码审查
/wf_14_doc                      # 智能文档生成（交互式）
/wf_13_doc_maintain             # 文档结构检查
/wf_11_commit "docs: 更新文档"   # 提交
```
**核心理念**: 从代码中提取真实信息，而非基于通用模板编造
**详细流程**: 查看 [WORKFLOWS.md](WORKFLOWS.md#场景5智能文档生成)

---

## 💡 关键最佳实践

1. **每次会话开始运行 `/wf_03_prime`** - 加载所有项目上下文
2. **让 `/wf_11_commit` 处理一切** - 自动格式化、CONTEXT.md更新、质量检查
3. **PRD.md 是只读的** - 需求修改需授权人员处理
4. **提交前运行 `/wf_08_review`** - 确保代码质量
5. **使用 `--coverage` 关注测试覆盖率** - `/wf_07_test --coverage`

---

## 🛠️ 快速问题解决

| 问题 | 解决方案 |
|------|---------|
| 丢失项目上下文 | `/wf_03_prime` |
| 不清楚需求 | `/wf_04_ask "问题"` |
| 代码有问题 | `/wf_06_debug "错误描述"` |
| 需要帮助 | `/wf_99_help` |

**完整故障排查**: 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📖 系统优势

- **上下文保存**: CONTEXT.md 自动管理，跨会话无缝继续
- **进度追踪**: TASK.md 实时更新，始终清楚当前状态
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
- `/wf_04_ask` - 架构咨询（支持`--review-codebase`）
- `/wf_05_code` - 功能实现（自动格式化）
- `/wf_06_debug` - 调试修复（支持`--quick`）

### 质量保证 (7-10)
- `/wf_07_test` - 测试开发（支持`--coverage`）
- `/wf_08_review` - 代码审查
- `/wf_09_refactor` - 代码重构
- `/wf_10_optimize` - 性能优化

### 运维部署 (11-12)
- `/wf_11_commit` - 提交代码（自动更新CONTEXT.md）
- `/wf_12_deploy_check` - 部署检查

### 文档维护 (13) NEW
- `/wf_13_doc_maintain` - 文档结构维护和优化

### 支持命令 (99)
- `/wf_99_help` - 帮助系统

**详细说明**: 查看 [COMMANDS.md](COMMANDS.md)

---

## 🔗 扩展阅读

- **工作流指导**: [WORKFLOWS.md](WORKFLOWS.md)
- **故障排查**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **命令参考**: [COMMANDS.md](COMMANDS.md)
- **AI执行规则**: [CLAUDE.md](CLAUDE.md)

---

**最后更新**: 2025-11-07
**版本**: v3.3 (新增智能文档生成)
**架构**: 命令定义（commands/）与项目数据（根目录）清晰分离
**命令格式**: 统一使用 `/wf_XX_name` slash command 格式

**v3.3 新增** (2025-11-07):
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
