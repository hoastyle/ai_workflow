# 技术栈 (Tech Stack)

## 主要语言

- **Python** (3.8+)
  - 用途: 工具库开发 (commands/lib/)
  - 用途: 实用脚本 (scripts/)
  - 关键库: 无重外部依赖，使用标准库

- **Bash/Shell**
  - 用途: 安装脚本
  - 版本: Bash 4.0+
  - 平台: Linux

- **Markdown**
  - 用途: 所有文档
  - 格式: GitHub-flavored Markdown
  - 规范: docs/reference/MARKDOWN_STYLE.md

## 文档系统

- **Frontmatter** (元数据)
  - 7 个必需字段: title, description, type, status, priority, created_date, last_updated
  - 规范: docs/reference/FRONTMATTER.md

- **文档分层**
  - 管理层: < 200 行
  - 技术层: < 500 行
  - 超过限制时拆分文件

## MCP (Model Context Protocol)

### 直接集成
- **Serena** - 语义代码理解、项目内存
- **Context7** - 官方库文档查询
- **Sequential-thinking** - 结构化多步推理
- **Tavily** - Web 搜索
- **Magic** - UI 组件生成

### AIRIS MCP Gateway 集成
- **13 个 MCP 服务器**: 统一访问接口
- **112 个工具**: 通过 airis-find/airis-schema/airis-exec 三步工作流
- **HOT/COLD 模式**: 区分常驻和按需启动的服务

## 工具和脚本

### Python 工具库 (commands/lib/)
- **DocLoader** - 智能文档加载（摘要/章节模式）
- **AgentCoordinator** - 多 Agent 协调器
- **AgentDecisionEngine** - Agent 决策引擎

### Bash 脚本 (scripts/)
- **install_knowledge_base.sh** - 主安装脚本
- **doc_guard.py** - 文档读取保护工具
- **frontmatter_utils.py** - Frontmatter 验证工具

## 版本控制

- **Git**
  - 分支策略: dev/master (开发), master (稳定)
  - 提交格式: [type] 描述 (type: feat, fix, docs, refactor, release)

## 部署和安装

- **安装目标**: ~/.claude/knowledge-base/
- **软链接**: ~/.claude/CLAUDE.md → ~/.claude/knowledge-base/CLAUDE.md
- **全局配置**: ~/.claude/CLAUDE_DEPLOY.md (可选)

## 开发环境

- **操作系统**: Linux (5.15.0-139-generic)
- **Python 版本**: 3.8+
- **Bash 版本**: 4.0+
- **编码**: UTF-8