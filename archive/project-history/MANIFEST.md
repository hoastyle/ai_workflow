# 安装清单一致性保证指南

## 🎯 核心问题

当 `install.sh` 和 `uninstall.sh` 分别维护自己的文件清单时，存在一致性风险：

```bash
❌ 问题场景：
# install.sh 中
declare -a SCRIPT_FILES=("script1.sh" "script2.py" "script3.sh")

# uninstall.sh 中（遗漏了script3.sh）
declare -a SCRIPT_FILES=("script1.sh" "script2.py")

# 结果：安装了3个脚本，但卸载只删除2个 → 孤立文件！
```

## ✅ 解决方案：单一信息源 (Single Source of Truth)

使用**共享清单文件**确保两个脚本始终一致：

```
scripts/install.manifest    ← 📍 唯一的真实来源
    ↓ sourced by
install.sh + uninstall.sh   ← 👥 都从同一源读取
```

## 📋 当前架构

### 文件结构

```
ai_workflow/
├── install.sh                          # 主安装脚本（sources install.manifest）
├── uninstall.sh                        # 主卸载脚本（sources install.manifest）
└── scripts/
    ├── install.manifest               ✅ 单一清单源（DRY原则）
    ├── install_utils.sh               ✅ 工具函数库
    ├── verify_manifest.sh             ✅ 一致性验证脚本
    ├── install_utils.py
    ├── doc_graph_builder.py
    └── README.md
```

### install.manifest 内容

```bash
# 单一定义位置
declare -ga SCRIPT_FILES=(
    "install_utils.sh"
    "frontmatter_utils.py"
    "doc_graph_builder.py"
)

declare -ga CONFIG_FILES=(
    "CLAUDE.md"
)

declare -ga DOC_FILES=(
    "COMMANDS.md"
    "WORKFLOWS.md"
    ...
)
```

### 脚本集成方式

**install.sh**:
```bash
# Line 32-33
source "${SCRIPT_DIR}/scripts/install_utils.sh" || exit 1
source "${SCRIPT_DIR}/scripts/install.manifest" || exit 1
# 现在SCRIPT_FILES、CONFIG_FILES等都自动可用
```

**uninstall.sh**:
```bash
# Line 30-31
source "${SCRIPT_DIR}/scripts/install_utils.sh" || exit 1
source "${SCRIPT_DIR}/scripts/install.manifest" || exit 1
# 两个脚本用同样的数组
```

## 🔒 一致性保证机制

### 1️⃣ **源代码层次的一致性**

✅ **不可能不一致**，因为两个脚本都从同一个文件读取：

```bash
# 如果修改install.manifest中的SCRIPT_FILES
declare -ga SCRIPT_FILES=("script1.sh" "script2.py" "script3.sh" "NEW_SCRIPT.py")

# 两个脚本都会立即使用新列表
# ✅ 自动同步，无需手动修改两处
```

### 2. **验证脚本** (`scripts/verify_manifest.sh`)

自动检查一致性：

```bash
# 运行验证
./scripts/verify_manifest.sh

# 检查项：
# ✅ install.sh sources install.manifest
# ✅ uninstall.sh sources install.manifest
# ✅ install.manifest 可以正常source
# ✅ 所有数组都正确导出
# ✅ 脚本语法有效
```

### 3️⃣ **Pre-commit Hook** (可选)

将验证添加到 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
# 在提交前验证清单一致性
./scripts/verify_manifest.sh || exit 1
```

## 📝 如何添加新文件

### 步骤1：确定文件类型

| 类型 | 位置 | 数组字段 | 示例 |
|------|------|---------|------|
| **命令** | 根目录 | COMMAND_FILES | wf_15_new.md |
| **脚本** | scripts/ | SCRIPT_FILES | new_tool.py |
| **配置** | 根目录 | CONFIG_FILES | config.md |
| **文档** | 根目录 | DOC_FILES | NEW_DOC.md |

### 步骤2：放置文件

```bash
# 例：添加新脚本
cp my_new_tool.py scripts/
ls -la scripts/my_new_tool.py
```

### 步骤3：更新 install.manifest（唯一需要改动的地方！）

编辑 `scripts/install.manifest`：

```bash
# 找到 SCRIPT_FILES 数组（约第 33 行）
declare -ga SCRIPT_FILES=(
    "install_utils.sh"
    "frontmatter_utils.py"
    "doc_graph_builder.py"
    "my_new_tool.py"          # 🆕 新增这一行
)

# 就这样！无需修改install.sh或uninstall.sh
```

### 步骤4：验证一致性

```bash
# 运行验证脚本
./scripts/verify_manifest.sh

# 预期输出：
# ✅ All manifest consistency checks passed!
```

### 步骤5：测试安装

```bash
# 干运行测试
./install.sh --dry-run --verbose

# 应显示:
# [DRY RUN] Would install: my_new_tool.py
```

### 步骤6：提交

```bash
git add scripts/install.manifest scripts/my_new_tool.py
git commit -m "feat: 添加 my_new_tool.py 脚本

- 放置脚本文件到 scripts/ 目录
- 在 install.manifest 中添加到 SCRIPT_FILES
- 验证一致性通过"
```

## 🔄 变更场景对比

### ❌ 旧方式（容易出错）

添加新脚本需要修改 3 个地方：

```bash
# 1. scripts/install.sh
declare -a SCRIPT_FILES=("..." "new_tool.py")

# 2. scripts/uninstall.sh（容易遗漏！）
declare -a SCRIPT_FILES=("..." "new_tool.py")

# 3. 脚本本身
scripts/new_tool.py
```

**风险**: 容易在其中一个地方遗漏，导致卸载不完整

### ✅ 新方式（自动一致）

添加新脚本只需修改 1 个地方：

```bash
# 1. scripts/install.manifest（唯一！）
declare -ga SCRIPT_FILES=("..." "new_tool.py")

# 2. 脚本本身
scripts/new_tool.py

# install.sh 和 uninstall.sh 自动从 install.manifest 读取
# ✅ 零遗漏风险
```

## 🧪 验证工具

### 完整的一致性验证

```bash
# 运行所有验证
bash scripts/verify_manifest.sh

# 逐项检查：
✅ Source statements       - 两个脚本都source manifest
✅ Manifest file          - 清单文件存在且有效
✅ Array exports          - 所有数组都正确导出
✅ Script syntax          - 所有脚本语法有效
✅ Script sourcing        - 脚本可以成功source
```

### 快速验证（编写提交前）

```bash
# 快速检查
bash -n scripts/install.manifest
bash -n install.sh
bash -n uninstall.sh
./install.sh --dry-run  # 预演安装
```

## 📊 一致性保证总结

| 维度 | 机制 | 保证程度 |
|------|------|---------|
| **源代码** | 单一源文件 | 🟢 100% |
| **语法** | bash -n验证 | 🟢 100% |
| **逻辑** | verify脚本 | 🟢 100% |
| **自动化** | 无需手动同步 | 🟢 100% |

## 🚨 如果遇到不一致

如果验证失败：

```bash
# 诊断
bash scripts/verify_manifest.sh

# 常见问题：
# ❌ "install.sh sources install.manifest" → 检查第32行
# ❌ "install.manifest can be sourced" → 检查manifest语法
# ❌ "array exports" → 检查declare -ga 语句
```

## 🎯 最佳实践

1. ✅ **总是修改install.manifest** - 不要直接修改install.sh或uninstall.sh中的数组
2. ✅ **添加前验证** - 每次添加文件都运行 `verify_manifest.sh`
3. ✅ **提交前测试** - 运行 `--dry-run` 验证
4. ✅ **保持源文件同步** - 如果手动修改了脚本，重新检查manifest

## 📚 相关文件

- `scripts/install.manifest` - 清单定义（SSOT）
- `scripts/verify_manifest.sh` - 验证脚本
- `install.sh` - 源表脚本（第32-33行）
- `uninstall.sh` - 源表脚本（第30-31行）
- `EXTENSIBILITY.md` - 可扩展性指南

---

**最后更新**: 2025-11-21
**一致性保证等级**: ⭐⭐⭐⭐⭐ 自动化完全一致
