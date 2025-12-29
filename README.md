# AI 工具知识库 (AI Tools Knowledge Base)

**版本**: v2.2 (Claude Code 优先 + CLAUDE.md 分离)
**创建日期**: 2025-12-05
**最后更新**: 2025-12-29
**状态**: 活跃维护中

> 本仓库已从 Workflow 命令系统转型为 AI 工具和开发最佳实践的知识库。

---

## 📋 文件说明（重要）

本仓库包含三个 CLAUDE.md 相关文件，各有不同用途：

| 文件 | 角色 | 受众 | 位置 |
|------|------|------|------|
| **CLAUDE.md** | 🔵 仓库开发指南 | 贡献者、维护者 | 仅在源码仓库 |
| **CLAUDE_KBASE.md** | 🟢 知识库入口源文件 | 使用知识库的开发者 | 源码 → 安装时重命名为 CLAUDE.md |
| **CLAUDE_DEPLOY.md** | 🟡 全局 Workflow 配置 | 所有项目通用配置 | 可选安装到 ~/.claude/ |

**安装后的文件映射**:
```
源码仓库                     安装后
CLAUDE.md         →         (仅在源码)
CLAUDE_KBASE.md   →         ~/.claude/knowledge-base/CLAUDE.md
CLAUDE_DEPLOY.md  →         ~/.claude/CLAUDE_DEPLOY.md (可选)
```

**重要**:
- 📚 如果你是**使用知识库的用户**，安装后查看 `~/.claude/knowledge-base/CLAUDE.md`
- 🔧 如果你是**开发这个仓库的贡献者**，查看源码中的 `CLAUDE.md`

---

## 🚀 快速开始

### 一键安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai_workflow.git
cd ai_workflow

# 运行安装脚本
bash scripts/install_knowledge_base.sh
```

安装后，Claude Code 将自动读取知识库，并能访问所有 MCP 工具和最佳实践文档。

**详细安装指南**: [INSTALL.md](INSTALL.md)

---

## 🎯 项目定位

本知识库专注于收集和整理：

- **设计哲学和原则** - Ultrathink 设计思维框架（6 个核心原则）
- **开发最佳实践** - 文档架构、AI 协作模式、代码质量规范
- **MCP 集成经验** - Model Context Protocol 的使用指南和故障排查
- **AIRIS MCP Gateway** - 统一访问 13 个 MCP 服务器的 112 个工具
- **架构决策记录** - 17 个技术决策的"为什么"和权衡
- **工具和脚本** - DocLoader、AgentCoordinator 等可复用工具

**核心价值**: 从实践中提取的经验教训，而非凭空编造的理论。

---

## 📚 知识库结构

### 核心内容

```
ai_workflow/
├── best-practices/          # 最佳实践集合
│   ├── philosophy.md        # Ultrathink 设计思维（6 个核心原则）
│   ├── document-architecture.md  # 文档架构和 SSOT 原则
│   └── ai-collaboration.md  # AI 协作模式和质量门控
│
├── mcp-integration/         # MCP 集成专题
│   ├── MCP_ARCHITECTURE.md  # MCP 架构设计
│   ├── README.md            # Serena 使用指南
│   ├── quick-start.md       # MCP 快速开始
│   └── troubleshooting.md   # 故障排查
│
├── docs/
│   ├── adr/                 # 17 个架构决策记录
│   │   ├── 2025-11-13-prioritize-opensource-in-architecture.md
│   │   ├── 2025-11-18-constraint-driven-documentation-generation.md
│   │   └── ...
│   └── reference/           # 参考文档
│       ├── FRONTMATTER.md   # 元数据规范
│       └── MARKDOWN_STYLE.md # 格式约束
│
├── commands/
│   └── lib/                 # 工具库
│       ├── doc_loader.py    # 智能文档加载
│       ├── agent_coordinator.py  # Agent 协调器
│       └── agent_decision_engine.py  # 决策引擎
│
├── scripts/                 # 实用脚本
│   ├── doc_guard.py         # 文档读取保护
│   └── frontmatter_utils.py # Frontmatter 验证
│
└── archive/                 # 归档内容
    ├── workflow-commands/   # 历史的 14 个 wf_ 命令
    ├── workflow-guides/     # 工作流使用指南
    └── project-history/     # PRD, TASK, CONTEXT 等
```

---

## 🎯 核心内容

### 1. Ultrathink 设计哲学

**来源**: [best-practices/philosophy.md](best-practices/philosophy.md)

**6 个核心原则**:
1. **Think Different** - 质疑假设，追求最优
2. **Balance Trade-offs** - 明确权衡，记录决策
3. **Iterate to Excellence** - 持续打磨
4. **Context Aware** - 理解环境
5. **Document Decisions** - 沉淀学习
6. **Test Assumptions** - 验证假设

**应用场景**: 架构设计、技术选型、系统边界划分

### 2. 约束驱动文档生成

**来源**: [best-practices/document-architecture.md](best-practices/document-architecture.md)

**核心思想**: 在文档生成时就内置约束检查，而非事后清理

**三阶段门控**:
- Phase 1: 文档决策树（确定文档类型和位置）
- Phase 2: 成本估计和门控（生成前预估）
- Phase 3: 架构合规性检查（验证 Frontmatter 和分层）

**成本约束**:
- 架构文档: < 50 行
- ADR: < 200 行
- 功能文档: < 500 行
- 增长率: 单次 < 30%

### 3. MCP 集成经验

**来源**: [mcp-integration/](mcp-integration/)

**支持的 MCP 服务器**:
- **Serena** - 语义代码理解、项目内存
- **Context7** - 官方库文档查询
- **Sequential-thinking** - 结构化多步推理
- **Tavily** - Web 搜索
- **Magic** - UI 组件生成

**Gateway 使用模式**:
```python
from src.mcp.gateway import get_mcp_gateway

gateway = get_mcp_gateway()
if gateway.is_available("serena"):
    tool = gateway.get_tool("serena", "find_symbol")
    result = tool.call(name="MyClass")
```

### 4. 架构决策记录 (ADR)

**来源**: [docs/adr/](docs/adr/)

**核心决策** (17 个):
- 智能文档生成 vs 模板驱动
- 优先开源方案的架构原则
- CONTEXT.md 指针文档模式
- 约束驱动文档生成
- MCP 集成策略
- Agent 系统架构
- SuperClaude 优化总结

---

## 🛠️ 工具和脚本

### 核心工具

| 工具 | 功能 | 文档 |
|------|------|------|
| **DocLoader** | 智能文档加载（摘要/章节模式） | [commands/lib/doc_loader.py](commands/lib/doc_loader.py) |
| **AgentCoordinator** | 多 Agent 协调器 | [commands/lib/agent_coordinator.py](commands/lib/agent_coordinator.py) |
| **DocGuard** | 文档读取保护（防止上下文爆炸） | [scripts/doc_guard.py](scripts/doc_guard.py) |
| **FrontmatterUtils** | Frontmatter 验证和管理 | [scripts/frontmatter_utils.py](scripts/frontmatter_utils.py) |

### 使用示例

**DocLoader - 智能文档加载**:
```python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 摘要模式（100-300行文档）
summary = loader.load_summary(doc_path, max_lines=50)

# 章节模式（300-800行文档）
content = loader.load_sections(
    doc_path,
    sections=["Step 3", "MCP Integration"]
)
```

**DocGuard - 文档读取保护**:
```bash
# 基础用法
python scripts/doc_guard.py --docs "PLANNING.md,TASK.md"

# 指定章节（大文档必须）
python scripts/doc_guard.py \
  --docs "docs/guides/large_guide.md" \
  --sections '{"docs/guides/large_guide.md": ["Step 3", "MCP Integration"]}'
```

---

## 📖 快速导航

### 按需求查找

**我想...**

- 了解设计哲学 → [best-practices/philosophy.md](best-practices/philosophy.md)
- 学习文档架构 → [best-practices/document-architecture.md](best-practices/document-architecture.md)
- 查看 MCP 集成 → [mcp-integration/](mcp-integration/)
- 查阅架构决策 → [docs/adr/](docs/adr/)
- 使用工具库 → [commands/lib/](commands/lib/)
- 查看历史内容 → [archive/](archive/)

### 按主题查找

**设计原则**:
- Ultrathink 设计思维
- 约束驱动文档生成
- 优先开源方案

**技术集成**:
- MCP 集成策略
- Serena 使用指南
- Gateway 模式

**开发规范**:
- 文档架构设计
- Frontmatter 规范
- Markdown 格式约束

---

## 🔄 项目历史

本仓库曾是一个完整的 Workflow 命令系统，包含 14 个 wf_ 命令用于项目规划、任务管理和开发工作流。

**转型原因**: 从实践中发现，最有价值的部分是设计哲学、架构决策和工具库，而非命令本身。

**保留内容**:
- 所有架构决策记录 (ADR)
- Ultrathink 设计哲学
- 最佳实践和经验教训
- 可复用的工具和脚本
- MCP 集成经验

**归档内容**:
- 14 个 wf_ 命令实现
- 工作流使用指南
- 安装和部署脚本
- 项目管理文档 (PRD, TASK, CONTEXT)

---

## 📊 知识库统计

| 类型 | 数量 |
|------|------|
| **最佳实践文档** | 3 |
| **MCP 集成文档** | 4 |
| **架构决策记录** | 17 |
| **工具库** | 5 |
| **参考文档** | 3 |
| **归档文档** | 30+ |

---

## 🤝 贡献指南

本知识库欢迎贡献：

1. **新的架构决策记录** - 遵循 [docs/adr/README.md](docs/adr/README.md) 模板
2. **最佳实践补充** - 基于实践经验，而非理论
3. **工具和脚本改进** - 保持代码质量 > 80% 测试覆盖
4. **文档改进** - 遵循 Frontmatter 和 Markdown 格式约束

**贡献流程**:
1. Fork 项目
2. 创建分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m '[feat] Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📝 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式

- **问题反馈**: 请创建 GitHub Issue
- **功能建议**: 请创建 GitHub Discussion
- **安全问题**: 请发送私有邮件给维护者

---

**最后更新**: 2025-12-29
**版本**: v2.0 (AI 工具知识库)
**维护状态**: 持续更新中
