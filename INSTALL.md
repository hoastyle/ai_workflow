# AI Workflow 安装指南

欢迎使用 AI Workflow 命令系统！本文档将指导你如何安装和使用这个工作流系统。

## 📦 快速安装

```bash
# 从项目根目录运行安装脚本
./install.sh

# 加载项目上下文
/wf_03_prime
```

就这样！现在你可以使用所有 16 个工作流命令。

## 📖 详细安装步骤

### 第1步：下载项目

```bash
git clone <ai_workflow_repo>
cd ai_workflow
```

### 第2步：运行安装脚本

有两种安装方式可选：

#### 推荐方式：使用符号链接（默认）

```bash
./install.sh
```

**优势**：
- 命令文件保留在项目目录中
- 更新项目代码后命令自动更新
- 便于维护和版本控制

#### 备选方式：复制文件

```bash
./install.sh --copy
```

**优势**：
- 命令文件独立复制到 `~/.claude/commands/`
- 不依赖项目目录位置

### 第3步：验证安装

```bash
# 列出已安装的命令
ls ~/.claude/commands/

# 应该能看到 16 个 wf_*.md 文件
```

## 🎛️ 安装选项

### 基本选项

```bash
# 显示帮助信息
./install.sh --help

# 符号链接安装（推荐，默认）
./install.sh --link

# 文件复制安装
./install.sh --copy

# 跳过备份创建
./install.sh --no-backup

# 也安装文档文件
./install.sh --include-docs
```

### 高级选项

```bash
# 测试安装而不实际修改
./install.sh --dry-run

# 显示详细输出
./install.sh --verbose

# 组合选项
./install.sh --copy --no-backup --verbose
```

## 📋 安装目录结构

安装后你的 `~/.claude/` 目录结构如下：

```
~/.claude/
├── CLAUDE.md                    # 配置文件（全局）
├── commands/                    # 命令文件目录
│   ├── wf_01_planning.md
│   ├── wf_02_task.md
│   ├── wf_03_prime.md
│   ├── wf_04_ask.md
│   ├── wf_04_research.md
│   ├── wf_05_code.md
│   ├── wf_06_debug.md
│   ├── wf_07_test.md
│   ├── wf_08_review.md
│   ├── wf_09_refactor.md
│   ├── wf_10_optimize.md
│   ├── wf_11_commit.md
│   ├── wf_12_deploy_check.md
│   ├── wf_13_doc_maintain.md
│   ├── wf_14_doc.md
│   └── wf_99_help.md
├── docs/                        # 可选文档文件
│   ├── COMMANDS.md
│   ├── WORKFLOWS.md
│   ├── PHILOSOPHY.md
│   └── TROUBLESHOOTING.md
└── backup/                      # 备份目录
    ├── 2025-11-21_10-30-45/
    └── 2025-11-21_11-00-22/
```

## 🔄 更新现有安装

如果已经安装过，重新运行安装脚本会：

1. ✅ 创建现有文件的备份
2. ✅ 更新所有命令文件
3. ✅ 更新 CLAUDE.md 配置
4. ✅ 保留备份文件用于恢复

```bash
./install.sh  # 会自动创建新的备份
```

## 🗑️ 卸载

### 完全卸载

```bash
./uninstall.sh
```

会提示确认，然后删除所有命令文件。备份和配置文件保留用于恢复。

### 高级卸载选项

```bash
# 跳过确认提示
./uninstall.sh --force

# 卸载但保留 CLAUDE.md
./uninstall.sh --keep-config

# 同时删除备份目录
./uninstall.sh --clean-backup

# 测试卸载但不实际删除
./uninstall.sh --dry-run
```

## 💾 备份和恢复

### 查看备份

```bash
# 列出所有备份
ls -la ~/.claude/backup/

# 查看特定备份的内容
ls ~/.claude/backup/2025-11-21_10-30-45/
```

### 恢复备份

```bash
# 从最新备份恢复
cp ~/.claude/backup/2025-11-21_10-30-45/* ~/.claude/

# 或者完全恢复某个时间点的配置
rm -rf ~/.claude/commands
cp -r ~/.claude/backup/2025-11-21_10-30-45/* ~/.claude/
```

## 🚀 首次使用

安装完成后，按照以下步骤开始：

### 1. 加载项目上下文

```bash
# 从任何目录运行（假设 commands 在 PATH 中）
/wf_03_prime

# 或从项目目录运行
cd ~/path/to/ai_workflow
/wf_03_prime
```

### 2. 查看可用命令

```bash
# 显示帮助和命令列表
/wf_99_help

# 查看完整命令参考
cat ~/.claude/docs/COMMANDS.md
```

### 3. 开始使用工作流

```bash
# 示例：启动功能开发流程
/wf_03_prime                              # 加载上下文
/wf_04_ask "my_feature"                  # 架构咨询
/wf_05_code "implement_feature"          # 代码实现
/wf_07_test "test_feature"               # 编写测试
/wf_08_review                            # 代码审查
/wf_11_commit "add: my_feature"          # 提交代码
```

## ⚙️ 配置

### 全局配置（CLAUDE.md）

`~/.claude/CLAUDE.md` 包含全局配置，用于所有使用此工作流系统的项目。

**主要设置**：
- 语言规范（中文/英文）
- 文件权限矩阵
- AI 执行规则
- 工作流命令列表

### 项目级配置

某些项目可能有自己的 `CLAUDE.md` 来覆盖全局配置。项目级配置优先级更高。

## 🔧 故障排查

### 安装失败

**问题**：权限不足
```bash
# 解决方案
chmod +x ./install.sh ./uninstall.sh ./scripts/install_utils.sh
./install.sh
```

**问题**：找不到脚本
```bash
# 确保在项目根目录
ls CLAUDE.md install.sh  # 应该能看到这些文件

# 如果找不到，确保下载了正确的项目
git clone <ai_workflow_repo>
cd ai_workflow
```

### 命令不可用

**问题**：安装后仍找不到 wf_* 命令

```bash
# 检查安装目录
ls ~/.claude/commands/wf_*.md

# 检查 PATH 设置（如果需要）
echo $PATH | grep -q ".claude/commands" || echo ".claude/commands not in PATH"
```

**解决方案**：
- 重新运行 `/wf_03_prime` 加载上下文
- 确保使用 `/wf_*` 语法（斜杠前缀）调用命令

### 备份文件过多

```bash
# 清理旧备份
rm -rf ~/.claude/backup/  # 删除所有备份

# 或保留最新备份
ls -t ~/.claude/backup | tail -n +2 | xargs -I {} rm -rf ~/.claude/backup/{}
```

## 📚 更多信息

- **快速开始**: 见 `README.md`
- **工作流指南**: `~/.claude/docs/WORKFLOWS.md`
- **命令参考**: `~/.claude/docs/COMMANDS.md`
- **故障排查**: `~/.claude/docs/TROUBLESHOOTING.md`
- **设计哲学**: `~/.claude/docs/PHILOSOPHY.md`

## 🤝 获取帮助

```bash
# 查看帮助菜单
/wf_99_help

# 查看特定命令的帮助
/wf_01_planning --help  # 如果命令支持

# 检查安装脚本的帮助
./install.sh --help
./uninstall.sh --help
```

## ✅ 验证清单

安装完成后，检查以下项目：

- [ ] 脚本执行成功（无错误提示）
- [ ] `~/.claude/commands/` 目录存在
- [ ] 16 个 `wf_*.md` 文件已安装
- [ ] `~/.claude/CLAUDE.md` 存在
- [ ] 备份目录已创建（`~/.claude/backup/`）
- [ ] `/wf_03_prime` 命令可运行
- [ ] `/wf_99_help` 显示帮助信息

## 📝 许可证和贡献

此项目遵循与 Utility 项目相同的许可证。

---

**最后更新**: 2025-11-21
**版本**: 1.0

有任何问题或建议，欢迎提交 Issue 或 PR！
