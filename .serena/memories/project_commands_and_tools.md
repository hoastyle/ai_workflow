# 项目常用命令和工具

## 完成任务后应运行的命令

### 标准开发流程

**代码完成后的完整流程**：

```bash
# 1. 代码审查（自动检查代码质量）
/wf_08_review

# 2. 运行测试（验证功能）
/wf_07_test "相关组件"

# 3. 运行覆盖率检查（确保测试充分）
/wf_07_test --coverage

# 4. 智能文档生成（如果需要）
/wf_14_doc

# 5. 提交代码（包含所有自动检查和更新）
/wf_11_commit "提交信息"
```

### 单个功能完整流程

```bash
/wf_03_prime                    # 加载项目上下文
/wf_04_ask "架构问题"            # 获取设计指导（可选）
/wf_05_code "功能描述"           # 实现功能
/wf_07_test "组件名"             # 添加测试
/wf_08_review                   # 代码审查
/wf_11_commit "feat: 功能名"    # 提交
```

### Bug 修复流程

```bash
/wf_06_debug "错误描述"           # 调试和修复
/wf_07_test "相关组件"            # 验证修复
/wf_08_review                   # 代码审查
/wf_11_commit "fix: Bug描述"     # 提交
```

### 文档生成流程

```bash
/wf_05_code "功能"               # 完成代码（步骤8自动决策树）
/wf_08_review                   # 代码审查（Dimension 6检查）
/wf_14_doc                      # 生成文档（三阶段门控）
/wf_13_doc_maintain             # 验证索引和链接
/wf_11_commit "docs: 新文档"    # 提交
```

## 项目特定的 Unix/Linux 命令

### Git 操作

```bash
# 查看当前状态
git status

# 查看最近 10 条提交
git log --oneline -10

# 查看本次会话的变更
git diff

# 查看已暂存的变更
git diff --staged

# 回退到最后一次提交
git reset --hard HEAD

# 查看分支
git branch -a
```

### 文件操作

```bash
# 列出项目根目录
ls -la

# 列出 docs 目录
ls -la docs/

# 查找 Markdown 文件
find . -name "*.md" -type f

# 搜索文本内容
grep -r "关键词" docs/

# 统计行数
wc -l *.md
```

### 项目特定操作

```bash
# 运行 pre-commit 检查（所有文件）
pre-commit run --all-files

# 运行 pre-commit 检查（已暂存文件）
pre-commit run

# 安装 pre-commit 钩子
pre-commit install

# 更新工具版本
pre-commit autoupdate

# 显示帮助
/wf_99_help
```

## 环境和路径

### 项目目录结构

```bash
# 项目根目录
/home/hao/Workspace/MM/utility/ai_workflow

# 工作流命令
wf_*.md 文件（根目录）

# 项目文档
docs/management/     # 项目管理文档
docs/adr/            # 架构决策记录
docs/guides/         # 工作流指导
docs/examples/       # 使用示例
docs/reference/      # 参考文档

# 脚本
scripts/             # 自动化脚本

# MCP 配置
src/mcp/configs/     # MCP 服务器配置
```

### 重要文件路径

```bash
# 项目管理
docs/management/PRD.md         # 项目需求（只读）
docs/management/PLANNING.md    # 技术规划
docs/management/TASK.md        # 任务追踪
docs/management/CONTEXT.md     # 会话上下文（自动管理）

# 知识库
KNOWLEDGE.md                   # 知识库和文档索引

# 核心文档
README.md                      # 项目介绍
COMMANDS.md                    # 命令完整参考
WORKFLOWS.md                   # 工作流指导
TROUBLESHOOTING.md             # 故障排查
CLAUDE.md                      # AI 执行规则
DOC_ARCHITECTURE.md            # 文档架构
PHILOSOPHY.md                  # 设计哲学
```

## 常见工具和快捷键

### 项目相关的文件和工具

| 工具/文件 | 用途 | 运行方式 |
|----------|------|--------|
| `pre-commit` | 自动质量检查 | `pre-commit run --all-files` |
| `git` | 版本控制 | `git status`, `git log`, etc. |
| `/wf_11_commit` | 提交代码 | `/wf_11_commit "消息"` |
| `/wf_08_review` | 代码审查 | `/wf_08_review` |
| `/wf_07_test` | 运行测试 | `/wf_07_test "组件"` |
| `/wf_14_doc` | 生成文档 | `/wf_14_doc` |
| `/wf_13_doc_maintain` | 文档维护 | `/wf_13_doc_maintain` |

### 常用命令行快捷方式

```bash
# 查看所有 wf_* 命令
ls -1 wf_*.md

# 快速查看命令列表
/wf_99_help

# 清理上下文（会话过大时）
/clear

# 重新加载项目上下文
/wf_03_prime
```

## 项目特定的最佳实践

1. **每次会话开始**: `/wf_03_prime`
2. **编码前获取指导**: `/wf_04_ask "问题"`
3. **代码完成后**: `/wf_08_review` → `/wf_07_test` → `/wf_11_commit`
4. **文档生成时**: 遵守约束规范（< 500 行/文件，< 30% 增长）
5. **提交前检查**: `pre-commit run --all-files`
6. **遇到问题**: `/wf_06_debug "错误"` 或查看 TROUBLESHOOTING.md

## Makefile 命令（如有）

项目使用 `Makefile` 进行构建和测试（如 Makefile 存在）：

```bash
# 查看可用 make 命令
make help

# 运行构建
make build

# 运行测试
make test

# 运行格式化
make format

# 清理构建产物
make clean
```

## 系统环境

- **操作系统**: Linux
- **Shell**: Bash/Zsh
- **Python**: 支持（使用 Black 格式化）
- **Node.js**: 支持（使用 Prettier 格式化）
- **Git**: 用于版本控制
- **Pre-commit**: 自动质量检查
