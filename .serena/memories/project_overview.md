# AI Workflow Project Overview

## 项目目标

Claude Code 工作流命令系统 - 为 Claude Code 提供项目规划、任务管理和开发最佳实践的完整集成。

## 核心特点

- **会话连续性**: 通过 CONTEXT.md 跨越 `/clear` 边界保持工作状态
- **自动化追踪**: 开发周期全程自动更新进度（TASK.md）
- **质量保证**: 内置格式化、测试、代码审查
- **文档驱动**: docs/management/ 下的 PRD → PLANNING → TASK 完整追溯链
- **智能文档管理**: 四层架构 + 按需加载，上下文成本最优
- **约束驱动文档生成** (NEW v3.4): 从代码提取文档，而非凭空编造

## 技术栈

- **核心系统**: Markdown 为基础的闭环工作流系统
- **集成框架**: Claude Code Slash Commands
- **文档管理**: 四层架构（管理/技术/工作/归档）
- **MCP 服务器**: Serena, Context7, Sequential-thinking, Tavily, Magic
- **验证系统**: pre-commit hooks，自动格式化和质量检查
- **项目数据存储**: JSON 配置文件（src/mcp/configs/）

## 项目结构

```
ai_workflow/
├── src/mcp/configs/          # MCP 服务器配置
│   ├── serena.json
│   ├── context7.json
│   ├── sequential-thinking.json
│   ├── tavily.json
│   └── ... (其他MCP配置)
├── docs/                     # 分层文档
│   ├── management/           # 项目管理文档（5个）
│   ├── adr/                  # 架构决策记录
│   ├── guides/               # 工作流指导
│   ├── examples/             # 使用示例
│   ├── reference/            # 参考文档
│   ├── integration/          # MCP集成文档
│   ├── knowledge/            # 知识库
│   └── templates/            # 文档模板
├── scripts/                  # 自动化脚本
├── wf_01_planning.md         # 14个工作流命令
├── wf_02_task.md
├── wf_03_prime.md
├── ... (wf_04 ~ wf_14)
├── wf_99_help.md
├── KNOWLEDGE.md              # 项目知识库和文档索引
├── CLAUDE.md                 # AI执行规则
├── README.md                 # 项目介绍
├── COMMANDS.md               # 命令完整参考
├── WORKFLOWS.md              # 场景化工作流
├── TROUBLESHOOTING.md        # 故障排查
├── DOC_ARCHITECTURE.md       # 文档架构最佳实践
├── PHILOSOPHY.md             # 设计哲学（Ultrathink）
└── CHANGELOG.md              # 版本历史
```

## 核心概念

### 1. 14个工作流命令

**基础设施 (1-3)**:
- `/wf_01_planning` - 创建/更新项目规划
- `/wf_02_task` - 管理任务追踪
- `/wf_03_prime` - **加载项目上下文**（智能按需加载）

**开发实现 (4-6)**:
- `/wf_04_ask` - 架构咨询（支持--review-codebase、--think、--c7）
- `/wf_05_code` - 功能实现（自动格式化，Step 8支持文档决策树）
- `/wf_06_debug` - 调试修复（支持--quick、--think、--deep）

**质量保证 (7-10)**:
- `/wf_07_test` - 测试开发（支持--coverage）
- `/wf_08_review` - 代码审查（Dimension 6验证文档约束）
- `/wf_09_refactor` - 代码重构
- `/wf_10_optimize` - 性能优化

**运维部署 (11-12)**:
- `/wf_11_commit` - 提交代码（自动更新CONTEXT.md、验证Frontmatter）
- `/wf_12_deploy_check` - 部署检查

**文档管理 (13-14)**:
- `/wf_13_doc_maintain` - 文档结构维护（清理过期、检查链接）
- `/wf_14_doc` - **智能文档生成**（约束驱动）

**支持 (99)**:
- `/wf_99_help` - 帮助系统

### 2. 项目管理文档 (docs/management/)

- **PRD.md** (只读) - 项目需求权威数据源
- **PLANNING.md** - 技术架构、开发标准、技术栈决策
- **TASK.md** - 任务列表、状态追踪、进度管理
- **CONTEXT.md** (自动管理) - 会话指针文档，由 /wf_11_commit 更新

### 3. 知识库系统

- **KNOWLEDGE.md** - 架构决策、问题解决方案、设计模式、**文档索引中心**
- **docs/adr/** - 架构决策记录详情
- **docs/knowledge/** - 知识库内容

### 4. 约束驱动文档生成 (v3.4)

**约束规则**:
- KNOWLEDGE.md < 200 行（纯索引，无内容）
- 单个文档 < 500 行（便于维护）
- 单次增长 < 30%（避免文档爆炸）
- 必需 Frontmatter（7个字段）
- 四层分层（管理/技术/工作/归档）

**三阶段门控**:
1. Phase 1 (`/wf_05_code` Step 8) - 文档决策树
2. Phase 2 (`/wf_14_doc`) - 成本估计和约束检查
3. Phase 3 (`/wf_08_review` Dimension 6) - 验证

## 开发规范

### 代码风格

- **语言**: 中文交互、英文代码注释
- **格式化**: 自动应用（Black for Python, Prettier for JS/TS）
- **行尾**: Unix LF
- **尾部空格**: 零容忍（pre-commit检查）

### 提交规范

```
[type] subject

body
```

**类型**: [feat], [fix], [docs], [refactor], [test]

### 质量检查

- pre-commit hooks 自动验证
- `/wf_08_review` 代码审查（含Dimension 6文档约束检查）
- `/wf_07_test --coverage` 测试覆盖率

## 关键命令

### 日常工作流

```bash
# 会话开始
/wf_03_prime

# 功能开发
/wf_05_code "功能描述"

# 测试验证
/wf_07_test "组件名"

# 代码审查
/wf_08_review

# 提交保存
/wf_11_commit "提交信息"
```

### 文档管理

```bash
# 文档生成
/wf_14_doc

# 文档维护
/wf_13_doc_maintain

# 任务追踪
/wf_02_task update "任务描述"
```

## 重要文件

| 文件 | 用途 | 权限 |
|------|------|------|
| COMMANDS.md | 14个命令完整参考 | 读取 |
| WORKFLOWS.md | 场景化工作流指导 | 读取 |
| TROUBLESHOOTING.md | 故障排查方案 | 读取 |
| CLAUDE.md | AI执行规则和权限 | 读取 |
| DOC_ARCHITECTURE.md | 文档架构最佳实践 | 读取 |
| README.md | 项目介绍和快速开始 | 读取 |
| KNOWLEDGE.md | 知识库和文档索引 | 读写 |
| docs/management/PRD.md | 项目需求（只读） | 读取专用 |
| docs/management/PLANNING.md | 技术规划 | 读写 |
| docs/management/TASK.md | 任务追踪 | 读写 |
| docs/management/CONTEXT.md | 会话指针（自动管理） | 读取 |

## MCP 集成

配置位置: `src/mcp/configs/`

- **serena.json** - 语义代码理解
- **context7.json** - 官方库文档查询
- **sequential-thinking.json** - 结构化推理
- **tavily.json** - Web 搜索
- **magic.json** - UI 组件生成

## 版本信息

**当前版本**: v3.4 (2025-11-24)

**新增功能 (v3.4)**:
- 约束驱动文档生成完善版
- 4份详细文档（快速指南、决策树、Frontmatter参考、ADR）
- 三阶段门控系统
- 100% Frontmatter 完整性检查

**关键更新时间线**:
- v3.3 (2025-11-21): 智能文档生成、MCP集成
- v3.2 (2025-11-06): Ultrathink设计哲学
- v3.1: 四层文档架构、智能按需加载

## 最佳实践

1. **每次会话开始运行 `/wf_03_prime`** - 加载所有项目上下文
2. **让 `/wf_11_commit` 处理一切** - 自动格式化、CONTEXT.md更新、质量检查
3. **PRD.md 是只读的** - 需求修改需授权人员
4. **提交前运行 `/wf_08_review`** - 确保代码质量（含Dimension 6）
5. **遵守文档约束规范** - 确保文档可控和可验证
6. **使用 `--coverage` 关注测试覆盖率** - `/wf_07_test --coverage`
