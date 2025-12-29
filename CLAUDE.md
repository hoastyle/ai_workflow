# AI 工具知识库 - 仓库开发指南

**版本**: v2.2 (仓库开发专用)
**最后更新**: 2025-12-29
**用途**: 指导如何开发和维护这个知识库仓库本身

> ⚠️ **注意**: 本文件是**仓库开发指南**，用于指导如何开发维护这个知识库仓库。
>
> 📚 **如果你是使用知识库的用户**，请查看安装后的 `~/.claude/knowledge-base/CLAUDE.md`

---

## 🏗️ 仓库架构

### 项目定位

**历史演变**:
- v1.0-v3.4: Workflow 命令系统（14 个 wf_* 命令）
- v4.0+ (2025-12): 转型为 AI 工具知识库

**当前定位**:
为 Claude Code 提供设计哲学、最佳实践、MCP 集成指南和工具库的完整知识库。

### 核心目录结构

```
ai_workflow/
├── CLAUDE.md                    # 🔵 本文件 - 仓库开发指南
├── CLAUDE_KBASE.md             # 🟢 知识库入口源文件（安装时重命名为 CLAUDE.md）
├── CLAUDE_DEPLOY.md            # 🟡 全局 Workflow 配置基线
├── KNOWLEDGE.md                # 📚 完整索引和工具库
├── PHILOSOPHY.md               # 🎨 Ultrathink 设计哲学
├── README.md                   # 📖 项目介绍
│
├── best-practices/             # 💡 最佳实践集合
│   ├── philosophy.md              - Ultrathink 设计思维详解
│   ├── document-architecture.md   - 文档架构和约束驱动生成
│   └── ai-collaboration.md        - AI 协作模式
│
├── mcp-integration/            # 🔌 MCP 集成专题
│   ├── README.md                  - Serena MCP 使用指南
│   ├── quick-start.md             - 快速开始
│   └── troubleshooting.md         - 故障排查
│
├── docs/                       # 📚 技术层文档
│   ├── adr/                       - 17 个架构决策记录（ADR）
│   ├── airis-mcp-gateway/         - AIRIS MCP Gateway 完整文档
│   ├── reference/                 - Frontmatter、Markdown 格式规范
│   └── examples/                  - 使用示例
│
├── commands/lib/               # 🛠️ 工具库（Python）
│   ├── doc_loader.py              - 智能文档加载
│   ├── agent_coordinator.py       - 多 Agent 协调器
│   ├── agent_decision_engine.py   - Agent 决策引擎
│   └── *.py
│
├── scripts/                    # 📜 实用脚本
│   ├── install_knowledge_base.sh  - 主安装脚本
│   ├── uninstall_knowledge_base.sh- 卸载脚本
│   ├── doc_guard.py               - 文档读取保护工具
│   ├── frontmatter_utils.py       - Frontmatter 验证工具
│   └── *.sh, *.py
│
├── archive/                    # 📦 归档内容
│   ├── workflow-commands/         - 历史 wf_* 命令文件
│   ├── workflow-guides/           - 工作流使用指南
│   └── project-history/           - 项目历史文档
│
└── Makefile                    # 🔧 便捷部署入口
```

**目录职责**:

| 目录 | 职责 | 维护规则 |
|------|------|---------|
| `best-practices/` | 设计哲学和最佳实践 | 新实践经验时添加 |
| `mcp-integration/` | MCP 集成指南 | MCP 配置变更时更新 |
| `docs/adr/` | 架构决策记录 | 重大决策时创建新 ADR |
| `docs/airis-mcp-gateway/` | AIRIS Gateway 文档 | 工具变更时更新 |
| `docs/reference/` | 规范文档 | 规范变更时更新 |
| `commands/lib/` | Python 工具库 | 添加新工具时扩展 |
| `scripts/` | 安装和实用脚本 | 部署逻辑变更时修改 |
| `archive/` | 历史内容 | 只读，不修改 |

---

## 🛠️ 开发流程

### 本地开发设置

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/ai_workflow.git
cd ai_workflow

# 2. 验证结构
ls -la best-practices/ docs/ commands/lib/ scripts/

# 3. 检查依赖（可选）
python3 --version  # Python 3.8+
bash --version     # Bash 4.0+
```

### 添加新文档

**步骤**:

1. **确定文档类型和位置**:
   ```
   设计哲学/最佳实践 → best-practices/
   MCP 集成指南 → mcp-integration/
   架构决策 → docs/adr/
   技术参考 → docs/reference/
   使用示例 → docs/examples/
   ```

2. **创建文档并添加 Frontmatter**:
   ```markdown
   ---
   title: "文档标题"
   description: "一句话描述"
   type: "技术设计 | 架构决策 | 最佳实践"
   status: "草稿 | 完成"
   priority: "高 | 中 | 低"
   created_date: "2025-12-29"
   last_updated: "2025-12-29"
   related_documents: []
   related_code: []
   ---
   ```

3. **更新 KNOWLEDGE.md 索引**:
   ```markdown
   | 主题 | 文档路径 | 说明 | 优先级 | 最后更新 |
   |------|---------|------|--------|---------|
   | 新主题 | docs/xxx/new-doc.md | 简要说明 | 高 | 2025-12-29 |
   ```

4. **验证 Frontmatter**:
   ```bash
   python scripts/frontmatter_utils.py validate docs/xxx/new-doc.md
   ```

### 创建架构决策记录（ADR）

**何时创建 ADR**:
- 技术栈的重大决策（选择框架、数据库等）
- 多个方案间的权衡涉及长期影响
- 决策与标准有偏差需要解释

**步骤**:

1. **使用模板**:
   ```bash
   cp docs/adr/TEMPLATE.md docs/adr/2025-12-29-your-decision.md
   ```

2. **填写 ADR 内容**:
   - 背景（为什么需要决策）
   - 决策（选择了什么方案）
   - 候选方案（还有哪些选择）
   - 权衡（优势和劣势）
   - 实施（如何执行）

3. **更新 KNOWLEDGE.md**:
   ```markdown
   | 日期 | 主题 | ADR |
   |------|------|-----|
   | 2025-12-29 | 你的决策 | [2025-12-29-your-decision.md](docs/adr/2025-12-29-your-decision.md) |
   ```

### 修改安装脚本

**主安装脚本**: `scripts/install_knowledge_base.sh`

**关键逻辑**:
```bash
# 1. 复制核心文件（注意：CLAUDE_KBASE.md → CLAUDE.md）
cp "$SOURCE_DIR/CLAUDE_KBASE.md" "$INSTALL_DIR/CLAUDE.md"

# 2. 创建软链接
ln -s "$INSTALL_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"

# 3. 可选安装全局配置
cp "$SOURCE_DIR/CLAUDE_DEPLOY.md" "$HOME/.claude/CLAUDE_DEPLOY.md"
```

**修改后测试**:
```bash
# 全新安装测试
rm -rf ~/.claude/knowledge-base
bash scripts/install_knowledge_base.sh

# 验证
readlink ~/.claude/CLAUDE.md
cat ~/.claude/knowledge-base/CLAUDE.md | head -5
```

### 开发新工具

**Python 工具** (`commands/lib/`):

1. **创建新模块**:
   ```python
   # commands/lib/your_tool.py
   """
   简要说明工具功能
   """

   class YourTool:
       def __init__(self):
           pass

       def process(self, input_data):
           # 实现逻辑
           pass
   ```

2. **添加测试**（可选）:
   ```bash
   # 创建测试文件
   # tests/test_your_tool.py
   ```

3. **更新文档**:
   - 在 KNOWLEDGE.md 的"🛠️ 工具库"部分添加说明
   - 在 docs/examples/ 添加使用示例

**Bash 脚本** (`scripts/`):

1. **遵循现有风格**:
   ```bash
   #!/bin/bash
   set -e  # 遇到错误立即退出

   # 颜色定义
   RED='\033[0;31m'
   GREEN='\033[0;32m'
   NC='\033[0m'

   # 主逻辑
   ```

2. **添加帮助信息**:
   ```bash
   if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
       echo "Usage: $0 [options]"
       exit 0
   fi
   ```

---

## 📦 部署和发布

### 安装脚本维护

**核心脚本**:
- `scripts/install_knowledge_base.sh` (146 行) - 主安装
- `scripts/uninstall_knowledge_base.sh` - 卸载
- `scripts/install_utils.sh` (550 行) - 公共函数库

**关键文件重命名逻辑**:
```bash
# CLAUDE_KBASE.md 在安装时重命名为 CLAUDE.md
cp "$SOURCE_DIR/CLAUDE_KBASE.md" "$INSTALL_DIR/CLAUDE.md"
```

**为什么这样设计**:
- 源码仓库：`CLAUDE.md` = 仓库开发指南
- 安装后：`~/.claude/knowledge-base/CLAUDE.md` = 知识库入口
- 避免混淆：不同位置，不同职责

### 版本管理

**语义化版本** (Semantic Versioning):
```
v{MAJOR}.{MINOR}.{PATCH}

MAJOR: 不兼容的 API 修改
MINOR: 向下兼容的功能性新增
PATCH: 向下兼容的问题修正
```

**当前版本**: v2.2 (知识库模式 + CLAUDE.md 分离)

**版本更新位置**:
- `CLAUDE_KBASE.md` 第 3 行
- `KNOWLEDGE.md` 第 3 行
- `scripts/install_knowledge_base.sh` 第 90 行

### 发布流程

```bash
# 1. 更新版本号
# 修改 CLAUDE_KBASE.md, KNOWLEDGE.md, install_knowledge_base.sh

# 2. 更新 CHANGELOG（如果有）
# 记录新功能、修复、改进

# 3. 测试安装
bash scripts/install_knowledge_base.sh

# 4. 提交更改
git add .
git commit -m "[release] v2.2 - CLAUDE.md 分离和角色明确化"

# 5. 创建标签
git tag -a v2.2 -m "Version 2.2: CLAUDE.md separation"

# 6. 推送
git push origin dev/master
git push origin v2.2
```

### 使用 Makefile（便捷入口）

```bash
# 安装
make install

# 卸载
make uninstall

# 测试
make test

# 帮助
make help
```

---

## 🤝 贡献指南

### PR 流程

1. **Fork 仓库并创建分支**:
   ```bash
   git checkout -b feature/your-feature
   ```

2. **进行修改**:
   - 遵循现有代码风格
   - 添加必要的文档
   - 更新 KNOWLEDGE.md 索引

3. **本地测试**:
   ```bash
   # 测试安装
   bash scripts/install_knowledge_base.sh

   # 验证 Frontmatter（如果修改了文档）
   python scripts/frontmatter_utils.py validate-batch docs/
   ```

4. **提交更改**:
   ```bash
   git add .
   git commit -m "[type] 描述"
   # type: feat, fix, docs, refactor, test
   ```

5. **创建 Pull Request**:
   - 描述修改内容和动机
   - 引用相关 Issue（如果有）
   - 等待审查

### 代码规范

**Python**:
- 遵循 PEP 8
- 使用 type hints（Python 3.8+）
- 添加 docstrings

**Bash**:
- 使用 `set -e`（遇到错误退出）
- 添加注释说明复杂逻辑
- 使用颜色输出提升可读性

**Markdown**:
- 遵循 `docs/reference/MARKDOWN_STYLE.md`
- 所有文档添加 Frontmatter
- 使用相对路径链接

### 文档标准

1. **Frontmatter 必需字段**（7 个）:
   ```yaml
   title, description, type, status, priority,
   created_date, last_updated
   ```

2. **文档大小约束**:
   - 管理层文档：< 200 行
   - 技术层文档：< 500 行
   - 超过限制时拆分文件

3. **索引更新**:
   - 新增文档必须更新 KNOWLEDGE.md
   - 删除文档必须从索引移除
   - 重命名文档必须更新所有引用

### 测试检查清单

在提交 PR 前，确保：

- [ ] 代码通过本地测试
- [ ] 文档有完整的 Frontmatter
- [ ] KNOWLEDGE.md 索引已更新
- [ ] 安装脚本可正常运行
- [ ] 没有破坏现有功能
- [ ] Git 提交信息清晰

---

## 📊 项目统计

| 类型 | 数量 |
|------|------|
| 最佳实践文档 | 4 |
| MCP 集成文档 | 15+ |
| 架构决策记录 | 17 |
| 参考文档 | 3 |
| 工具库 | 5+ |
| 归档文档 | 30+ |

**AIRIS MCP Gateway 覆盖**:
- 核心指南: 3 个
- 服务器文档: 8 个
- 工具总数: 112 个 across 13 个 MCP 服务器

---

## 🔗 快速链接

**开发相关**:
- [KNOWLEDGE.md](KNOWLEDGE.md) - 完整索引
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计哲学
- [docs/adr/](docs/adr/) - 架构决策记录
- [scripts/](scripts/) - 安装和实用脚本

**用户相关**:
- [CLAUDE_KBASE.md](CLAUDE_KBASE.md) - 知识库入口源文件
- [README.md](README.md) - 项目介绍
- [best-practices/](best-practices/) - 最佳实践

**部署相关**:
- [scripts/install_knowledge_base.sh](scripts/install_knowledge_base.sh) - 主安装脚本
- [Makefile](Makefile) - 便捷入口

---

**最后更新**: 2025-12-29
**版本**: v2.2 (仓库开发专用)
**维护状态**: 持续更新中
