# 安装系统可扩展性指南

## 📋 概述

安装/卸载系统采用**配置驱动的设计**，使得添加新的文件、脚本或命令无需修改主脚本逻辑。

## 🔧 配置文件

### install.conf（配置参考）

位置：`install.conf`

记录了所有待安装组件的清单（参考用）。虽然当前脚本采用数组定义方式，但此文件为未来升级到完整配置驱动系统做准备。

## 📦 目前支持的文件类型

### 1. **命令文件** (Commands)

**何时添加新命令**：
1. 在项目根目录创建 `wf_<number>_<name>.md` 文件
2. 脚本会自动通过glob模式 `wf_*.md` 检测
3. 重新运行 `./install.sh` 时自动安装

```bash
# 示例：添加新命令 wf_15_deploy.md
touch wf_15_deploy.md
./install.sh --dry-run  # 会显示新命令
```

### 2. **配置文件** (Config)

**修改配置清单**：在 `install.sh` 中编辑 `CONFIG_FILES` 数组：

```bash
declare -a CONFIG_FILES=("CLAUDE.md" "new_config.md")
```

### 3. **脚本文件** (Scripts)

**添加新的工具脚本**：

#### 步骤1：将脚本文件放在 `scripts/` 目录

```bash
scripts/
├── install_utils.sh        ✅ 已有
├── frontmatter_utils.py    ✅ 已有
├── doc_graph_builder.py    ✅ 已有
├── new_tool.py             🆕 新增
└── helper_script.sh        🆕 新增
```

#### 步骤2：编辑 `install.sh` 和 `uninstall.sh` 中的数组

**在 install.sh 中**（约第 57 行）：
```bash
declare -a SCRIPT_FILES=(
    "install_utils.sh"
    "frontmatter_utils.py"
    "doc_graph_builder.py"
    "new_tool.py"           # 新增
    "helper_script.sh"      # 新增
)
```

**在 uninstall.sh 中**（约第 50 行）：同样更新

#### 步骤3：验证安装

```bash
./install.sh --dry-run --verbose
# 应显示: [DRY RUN] Would install: new_tool.py
# 应显示: [DRY RUN] Would install: helper_script.sh
```

### 4. **文档文件** (Docs)

**添加可选文档**：编辑 `DOC_FILES` 数组

**在 install.sh 中**（约第 58 行）：
```bash
declare -a DOC_FILES=(
    "COMMANDS.md"
    "WORKFLOWS.md"
    "TROUBLESHOOTING.md"
    "PHILOSOPHY.md"
    "API_REFERENCE.md"      # 新增
    "FAQ.md"                # 新增
)
```

使用 `--include-docs` 标志安装：
```bash
./install.sh --include-docs
```

## 🔍 当前架构（简化可扩展）

### 文件清单定义

```bash
# install.sh 和 uninstall.sh 中的定义
declare -a COMMAND_FILES=("wf_*.md")              # 支持glob
declare -a CONFIG_FILES=("CLAUDE.md")             # 逐项定义
declare -a SCRIPT_FILES=("...")                   # 逐项定义
declare -a DOC_FILES=("...")                      # 逐项定义
```

### 安装/卸载函数

每种文件类型都有对应的函数：
- `install_commands()` / `uninstall_commands()`
- `install_claude_md()` / `uninstall_claude_md()`
- `install_scripts()` / `uninstall_scripts()` ⭐ **新增**
- `install_documentation()` / `uninstall_documentation()`

函数自动遍历相应的数组，无需修改循环逻辑。

## 🚀 未来升级路径

### 从数组定义 → 完整配置驱动（可选）

当文件清单变得复杂时，可升级到 `install.conf` 配置文件方式：

```ini
[commands]
pattern=@PROJECT_ROOT/wf_*.md:@COMMANDS_DIR/:link

[scripts]
install_utils.sh=@PROJECT_ROOT/scripts/install_utils.sh:@SCRIPTS_DIR/:link
new_tool.py=@PROJECT_ROOT/scripts/new_tool.py:@SCRIPTS_DIR/:link
```

**升级优势**：
- ✅ 无需修改脚本代码添加文件
- ✅ 支持glob模式和更复杂的规则
- ✅ 单一信息源

**升级成本**：约 2-3 小时重写脚本逻辑

## 📋 快速参考：添加新文件

| 文件类型 | 位置 | 如何添加 | 重新安装 |
|---------|------|--------|--------|
| **命令** | 根目录 | 创建 `wf_*.md` | 自动检测 |
| **脚本** | scripts/ | 放置文件 + 编辑 SCRIPT_FILES | `./install.sh` |
| **文档** | 根目录 | 放置文件 + 编辑 DOC_FILES | `./install.sh --include-docs` |
| **配置** | 根目录 | 放置文件 + 编辑 CONFIG_FILES | `./install.sh` |

## 🛠️ 实战示例

### 示例1：添加新的Python工具

```bash
# 1. 创建工具文件
cp /path/to/my_tool.py scripts/my_tool.py

# 2. 编辑 install.sh（第57行）
declare -a SCRIPT_FILES=("install_utils.sh" "frontmatter_utils.py" "doc_graph_builder.py" "my_tool.py")

# 3. 编辑 uninstall.sh（第50行）
# 同样的数组定义

# 4. 测试
./install.sh --dry-run

# 5. 提交
git add install.sh uninstall.sh scripts/my_tool.py
git commit -m "feat: 添加新的 my_tool.py 脚本"
```

### 示例2：添加新的命令文件

```bash
# 1. 创建新命令（自动被发现）
touch wf_15_integration.md

# 2. 编辑命令内容...

# 3. 测试（无需修改脚本！）
./install.sh --dry-run
# 输出: [DRY RUN] Would install: wf_15_integration.md

# 4. 提交
git add wf_15_integration.md
git commit -m "feat: 新增 /wf_15_integration 命令"
```

### 示例3：添加可选文档

```bash
# 1. 创建文档
echo "# API Reference" > API_REFERENCE.md

# 2. 编辑 install.sh（第58行）
declare -a DOC_FILES=("..." "API_REFERENCE.md")

# 3. 编辑 uninstall.sh（第51行）
# 同样的数组定义

# 4. 安装时包含文档
./install.sh --include-docs
```

## ⚠️ 注意事项

### 脚本变量同步

**重要**：`install.sh` 和 `uninstall.sh` 中的数组定义**必须保持一致**

```bash
# ❌ 不一致（会导致卸载不完整）
# install.sh
declare -a SCRIPT_FILES=("script1.sh" "script2.py" "script3.sh")

# uninstall.sh
declare -a SCRIPT_FILES=("script1.sh" "script2.py")  # 缺少 script3.sh
```

### 验证清单

添加新文件时，需要检查：

- [ ] 文件已放置在正确目录
- [ ] `install.sh` 中的相应数组已更新
- [ ] `uninstall.sh` 中的相应数组已更新
- [ ] `--dry-run` 测试显示新文件
- [ ] 实际安装成功
- [ ] 文件已出现在 `~/.claude/` 中

## 📚 相关文件

- `install.sh` - 主安装脚本（包含文件清单）
- `uninstall.sh` - 主卸载脚本（包含文件清单）
- `install.conf` - 配置参考文件（未来升级用）
- `scripts/install_utils.sh` - 工具库（核心函数）

## 🤝 贡献新脚本

如果你想为项目贡献新的工具脚本：

1. **创建脚本**：在 `scripts/` 目录中创建
2. **编写说明**：在脚本注释中说明用途
3. **更新清单**：添加到 `SCRIPT_FILES` 数组
4. **测试**：运行 `--dry-run` 验证
5. **提交**：创建Pull Request

---

**最后更新**: 2025-11-21
**设计原则**: 配置驱动、零修改扩展、逐步演进

