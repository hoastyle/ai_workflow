# 知识库安装指南

## 概述

本知识库是一个 AI 工具和开发最佳实践的集合，专为 Claude Code 优化。

### 核心内容

- **设计哲学**: Ultrathink 设计思维框架（6 个核心原则）
- **MCP 集成**: AIRIS MCP Gateway 使用指南（13 个服务器，112 个工具）
- **最佳实践**: 文档架构、AI 协作模式、约束驱动开发
- **架构决策**: 17 个 ADR 记录技术决策的"为什么"
- **工具库**: DocLoader、AgentCoordinator 等可复用工具

---

## 🚀 快速安装

### 方法 1: 一键安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai_workflow.git
cd ai_workflow

# 运行安装脚本
bash scripts/install_knowledge_base.sh
```

**安装后结构**:
```
~/.claude/
├── CLAUDE.md -> knowledge-base/CLAUDE.md  # 软链接
└── knowledge-base/                        # 完整知识库
    ├── CLAUDE.md
    ├── KNOWLEDGE.md
    ├── docs/
    │   ├── airis-mcp-gateway/
    │   └── adr/
    ├── best-practices/
    ├── mcp-integration/
    └── scripts/
```

### 方法 2: 手动安装

```bash
# 1. 创建目录
mkdir -p ~/.claude/knowledge-base

# 2. 复制文件
cp -r ./* ~/.claude/knowledge-base/

# 3. 创建软链接
ln -s ~/.claude/knowledge-base/CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 📚 使用指南

### Claude Code 中使用

安装后，Claude Code 会自动读取 `~/.claude/CLAUDE.md`，并能够访问所有被索引的文档。

**快速访问路径**:
```
~/.claude/knowledge-base/
├── CLAUDE.md                           # 主入口（快速导航）
├── KNOWLEDGE.md                        # 完整索引
├── docs/airis-mcp-gateway/
│   ├── README.md                      # AIRIS MCP Gateway 使用指南
│   ├── QUICK_REFERENCE.md             # 快速参考
│   └── TOOL_INDEX.md                  # 工具索引
├── best-practices/
│   ├── philosophy.md                  # 设计哲学
│   ├── document-architecture.md       # 文档架构
│   └── ai-collaboration.md            # AI 协作模式
└── mcp-integration/
    ├── README.md                      # MCP 集成指南
    └── quick-start.md                 # 快速开始
```

### AIRIS MCP Gateway 使用

安装后即可使用三步工作流访问 112 个 MCP 工具：

```typescript
// Step 1: 发现工具
mcp__airis-mcp-gateway__airis-find({ query: "memory" })

// Step 2: 查看参数
mcp__airis-mcp-gateway__airis-schema({ tool: "serena:write_memory" })

// Step 3: 执行工具
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "project_notes.md",
    content: "# 项目笔记\n..."
  }
})
```

---

## 🔄 更新知识库

### 从 Git 更新

```bash
# 1. 进入源码目录
cd /path/to/ai_workflow

# 2. 拉取最新代码
git pull origin master

# 3. 重新安装（会自动备份旧版本）
bash scripts/install_knowledge_base.sh
```

### 查看安装信息

```bash
cat ~/.claude/knowledge-base/.install_info
```

---

## 🗑️ 卸载

```bash
# 运行卸载脚本（会自动备份）
bash scripts/uninstall_knowledge_base.sh
```

卸载后会保留备份在 `~/.claude/backup/`，可手动恢复。

---

## 🛠️ 故障排查

### 问题 1: CLAUDE.md 中的链接失效

**症状**: Claude Code 无法找到被索引的文档

**原因**: 知识库未安装到正确位置

**解决方案**:
```bash
# 验证安装路径
ls -la ~/.claude/knowledge-base/

# 验证软链接
ls -la ~/.claude/CLAUDE.md

# 重新安装
bash scripts/install_knowledge_base.sh
```

### 问题 2: 权限错误

**症状**: 安装脚本执行失败

**解决方案**:
```bash
# 设置脚本可执行权限
chmod +x scripts/install_knowledge_base.sh

# 检查目标目录权限
ls -la ~/.claude/
```

### 问题 3: 软链接冲突

**症状**: `~/.claude/CLAUDE.md` 已存在

**解决方案**:
```bash
# 备份现有文件
mv ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup

# 重新运行安装脚本
bash scripts/install_knowledge_base.sh
```

---

## 📊 安装验证

安装完成后，验证以下内容：

```bash
# 1. 验证主文件
ls ~/.claude/CLAUDE.md
ls ~/.claude/knowledge-base/CLAUDE.md

# 2. 验证 AIRIS MCP Gateway 文档
ls ~/.claude/knowledge-base/docs/airis-mcp-gateway/

# 3. 验证软链接
readlink ~/.claude/CLAUDE.md

# 4. 统计文件数量
find ~/.claude/knowledge-base -type f | wc -l
```

**预期结果**:
- 主文件存在且可访问
- AIRIS MCP Gateway 文档目录包含 12 个文件
- 软链接指向正确位置
- 文件总数 > 40 个

---

## 💡 最佳实践

### 1. 定期更新

建议每月更新一次知识库，获取最新的最佳实践和工具文档。

### 2. 备份重要内容

在更新前，脚本会自动备份到 `~/.claude/backup/`，保留 30 天。

### 3. 自定义配置

如需自定义，可直接编辑 `~/.claude/knowledge-base/` 中的文件。

### 4. 多环境使用

可以在不同机器上安装同一知识库，保持一致的开发环境。

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/yourusername/ai_workflow
- **问题反馈**: https://github.com/yourusername/ai_workflow/issues
- **贡献指南**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📝 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

**最后更新**: 2025-12-29
**版本**: v2.1 (Claude Code 优先)
**维护状态**: 持续更新中
