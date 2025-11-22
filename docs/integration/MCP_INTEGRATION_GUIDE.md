# MCP 集成指南

**版本**: 1.0
**日期**: 2025-11-22
**适用范围**: AI Workflow Command System v3.4+

---

## 📖 目录

1. [什么是 MCP？](#什么是-mcp)
2. [前置条件](#前置条件)
3. [快速开始](#快速开始)
4. [可用的 MCP 服务器](#可用的-mcp-服务器)
5. [安装说明](#安装说明)
6. [使用示例](#使用示例)
7. [故障排查](#故障排查)
8. [最佳实践](#最佳实践)

---

## 什么是 MCP？

**MCP (Model Context Protocol)** 是 Anthropic 开源的标准协议，用于连接 AI 助手与外部数据源和工具。

### 核心优势

- ✅ **可选增强**: 完全可选，不启用时工作流保持原样
- ✅ **零破坏性**: 不改变现有命令的基本行为
- ✅ **自动降级**: MCP 失败时自动回退到标准功能
- ✅ **生态丰富**: Anthropic 官方 + 社区 + 企业集成

### MCP 能做什么

| 功能 | 说明 | 典型用途 |
|------|------|---------|
| **结构化推理** | 多步问题求解 | 复杂决策、架构分析 |
| **Web 搜索** | 实时信息检索 | 最新技术、社区反馈 |
| **Git 操作** | 版本控制集成 | 代码审查、提交管理 |
| **数据库** | SQL 查询执行 | 数据分析、数据库管理 |
| **浏览器自动化** | 网页交互 | Web 测试、内容提取 |
| **GitHub 集成** | 仓库管理 | Issue 处理、代码审查 |

---

## 前置条件

### 必需

1. **Claude CLI** (最新版本)
   ```bash
   # 检查是否安装
   claude --version
   ```

2. **Node.js 18+** (用于npm包)
   ```bash
   # 检查版本
   node --version
   npm --version
   ```

### 可选但推荐

- **Git** - 用于 GitHub MCP
- **PostgreSQL 客户端** - 用于 Postgres MCP
- **Chromium/Chrome** - 用于 Puppeteer MCP

### 快速检查

```bash
# 检查所有前置条件
make mcp-check
```

---

## 快速开始

### Step 1: 检查前置条件

```bash
make mcp-check
```

**输出示例**:
```
✅ Claude CLI found: version 0.1.0
✅ Node.js found: v18.20.0
✅ npm found: 10.7.0
```

### Step 2: 列出可用的 MCP 服务器

```bash
make mcp-list
```

**输出示例**:
```
📋 Available MCP Servers:

   sequential-thinking      ⬜ not installed
      Multi-step problem solving and systematic analysis
      Source: Anthropic Official
      Docs: https://github.com/modelcontextprotocol/servers

   github                   ⬜ not installed
      GitHub repository and issue management (requires GITHUB_TOKEN)
      Source: Anthropic Official
      Docs: https://github.com/modelcontextprotocol/servers

   [...]

Total: 5 servers available
```

### Step 3: 安装 MCP 服务器

**选项 A: 交互式安装 (推荐)**
```bash
make mcp-install
```

系统会提示你选择要安装的服务器。

**选项 B: 安装特定服务器**
```bash
python3 scripts/install_mcp.py --servers sequential-thinking,tavily,github
```

**选项 C: 安装所有**
```bash
make mcp-install-all
```

### Step 4: 验证安装

安装完成后，Claude CLI 会自动配置 MCP 服务器。

```bash
# 在 Claude Code 中验证
/wf_03_prime
# 输出应该显示已加载的 MCP 服务器
```

---

## 可用的 MCP 服务器

现在支持 **13 个 MCP 服务器**，包括 Anthropic 官方、社区和企业方案。

### Anthropic 官方服务器

#### 1. Sequential-Thinking (结构化推理)
- **功能**: 多步骤的结构化问题求解
- **使用场景**: 复杂决策、架构分析、根因分析
- **示例**:
  ```
  /wf_04_ask "选择微服务框架：Spring Cloud vs Kubernetes + Docker"
  ```

#### 2. GitHub (版本控制)
- **功能**: GitHub 仓库管理、Issue、Pull Request
- **API 密钥**: GITHUB_TOKEN (生成: https://github.com/settings/tokens)
- **使用场景**: 代码审查、Issue 跟踪、仓库分析

#### 3. PostgreSQL (数据库)
- **功能**: SQL 查询和数据库管理
- **API 密钥**: DATABASE_URL (postgresql://user:password@host/db)
- **使用场景**: 数据分析、数据库设计、性能优化

#### 4. Puppeteer (浏览器自动化)
- **功能**: 网页交互、内容提取、自动化测试
- **使用场景**: E2E 测试、Web 爬取、截图生成

#### 5. Google Drive (文件管理)
- **功能**: Google Drive 文件访问和管理
- **API 密钥**: GOOGLE_API_KEY (需要 OAuth2 设置)
- **使用场景**: 文档管理、文件同步、内容分析

#### 6. Slack (工作区管理)
- **功能**: Slack 工作区和消息管理
- **API 密钥**: SLACK_BOT_TOKEN (xoxb-...)
- **使用场景**: 团队协作、消息自动化、工作流集成

### 社区和企业方案

#### 7. Tavily (Web 搜索)
- **来源**: Community (Tavily)
- **功能**: 实时 Web 搜索和研究
- **API 密钥**: TAVILY_API_KEY (免费获取: https://app.tavily.com)
- **使用场景**: 最新信息、产品对比、技术研究
- **示例**:
  ```
  /wf_04_research "React vs Vue 2024 最新趋势"
  ```

#### 8. Context7 (官方文档)
- **来源**: Community (Upstash)
- **功能**: 官方库文档和代码示例
- **使用场景**: 快速查阅框架文档、API 参考

#### 9. Playwright (E2E 测试)
- **来源**: Community (Microsoft)
- **功能**: 跨浏览器端到端测试和自动化
- **使用场景**: 自动化测试、UI 验证、跨浏览器兼容性

#### 10. Magic (UI 组件生成)
- **来源**: Community (21st.dev)
- **功能**: 现代 UI 组件生成和设计系统
- **API 密钥**: TWENTYFIRST_API_KEY
- **使用场景**: 快速原型、UI 设计、组件库生成

#### 11. Serena (代码分析)
- **来源**: Community (Serena)
- **功能**: 语义代码分析和智能编辑
- **使用场景**: 代码理解、智能重构、模式识别

#### 12. Morph LLM Fast Apply (代码修改)
- **来源**: Community (Morph LLM)
- **功能**: 上下文感知的代码修改能力
- **API 密钥**: MORPH_API_KEY
- **使用场景**: 快速代码变更、批量重构

#### 13. Chrome DevTools (调试分析)
- **来源**: Community
- **功能**: Chrome DevTools 调试和性能分析
- **使用场景**: 性能监控、调试分析、性能优化

---

## 安装说明

### 方法 1: 使用 Makefile (推荐)

```bash
# 列出所有可用服务器
make mcp-list

# 交互式安装
make mcp-install

# 安装所有服务器
make mcp-install-all

# 检查前置条件
make mcp-check
```

### 方法 2: 使用 Python 脚本

```bash
# 查看帮助
python3 scripts/install_mcp.py --help

# 列出服务器
python3 scripts/install_mcp.py --list

# 交互式安装
python3 scripts/install_mcp.py

# 安装特定服务器
python3 scripts/install_mcp.py --servers sequential-thinking,github

# 安装所有
python3 scripts/install_mcp.py --all

# 干运行 (预览但不实际安装)
python3 scripts/install_mcp.py --all --dry-run
```

### 设置 API 密钥

某些 MCP 需要 API 密钥。安装时会提示输入。

也可以预先设置环境变量:

```bash
# Tavily
export TAVILY_API_KEY="your-api-key"

# GitHub
export GITHUB_TOKEN="your-github-token"

# PostgreSQL
export DATABASE_URL="postgresql://user:pass@localhost/db"

# 然后安装
python3 scripts/install_mcp.py --servers tavily,github,postgres
```

### 验证安装

安装完成后，Claude CLI 配置了 MCP 服务器。在命令中可以使用它们:

```bash
# 检查已安装的 MCP
claude mcp list

# 在 Claude Code 中使用
/wf_03_prime
# 输出应该包含已启用的 MCP 信息
```

---

## 使用示例

### 示例 1: 架构决策 (Sequential-Thinking)

**场景**: 需要选择数据库

```bash
# 前置条件: sequential-thinking 已安装
make mcp-install-all

# 使用
/wf_04_ask "PostgreSQL vs MongoDB: 选择合适的数据库"
```

**效果**:
- Sequential-Thinking MCP 会分步骤分析
- 提供结构化的权衡分析
- 给出明确的建议理由

### 示例 2: 技术研究 (Tavily)

**场景**: 了解最新的 Node.js 框架选择

```bash
# 前置条件: tavily 已安装，TAVILY_API_KEY 已设置
export TAVILY_API_KEY="your-api-key"
make mcp-install-all

# 使用
/wf_04_research "Node.js 框架对比 2024"
```

**效果**:
- Tavily 搜索最新信息
- 返回社区讨论、性能数据、采用率
- 基于最新信息的建议

### 示例 3: 仓库管理 (GitHub)

**场景**: 管理 GitHub 仓库

```bash
# 前置条件: github 已安装，GITHUB_TOKEN 已设置
export GITHUB_TOKEN="your-github-token"
make mcp-install-all

# 使用 (在 Claude Code 中)
# - 查看 Issues
# - 查看 Pull Requests
# - 分析代码变更
# - 生成 release notes
```

---

## 故障排查

### 问题 1: Claude CLI 未找到

**症状**:
```
Claude CLI not found - required for MCP server management
```

**解决**:
```bash
# 安装 Claude Code
# 参考: https://docs.claude.com/en/docs/claude-code/claude_code_docs_map

# 验证安装
which claude
claude --version
```

### 问题 2: Node.js 版本太低

**症状**:
```
Node.js version v16.x.x found, but version 18+ required
```

**解决**:
```bash
# 升级 Node.js
# 从 https://nodejs.org 下载 18+ 版本

# 验证
node --version  # 应该是 v18.0.0 或更高
```

### 问题 3: npm 包安装失败

**症状**:
```
Failed to install sequential-thinking: npm ERR! ...
```

**解决**:
```bash
# 清除 npm 缓存
npm cache clean --force

# 重试安装
make mcp-install-all

# 或检查网络连接
npm ping
```

### 问题 4: API 密钥问题

**症状**:
```
Tavily MCP 无法连接: 未获得有效的 API 密钥
```

**解决**:
```bash
# 检查环境变量是否设置
echo $TAVILY_API_KEY

# 重新设置
export TAVILY_API_KEY="your-valid-key"

# 重新安装
python3 scripts/install_mcp.py --servers tavily
```

### 问题 5: MCP 服务器启动失败

**症状**:
```
MCP server 'sequential-thinking' failed to start
```

**解决**:
```bash
# 检查前置条件
make mcp-check

# 查看 Claude 日志
# 通常在 ~/.claude/logs/ 或 ~/.cache/claude/

# 尝试手动启动测试
claude mcp list
```

---

## 最佳实践

### 1. 按需安装

不需要一次安装所有 MCP。根据实际需求选择:

```bash
# 如果主要做架构决策
python3 scripts/install_mcp.py --servers sequential-thinking

# 如果需要最新信息
python3 scripts/install_mcp.py --servers tavily

# 如果管理 GitHub 仓库
python3 scripts/install_mcp.py --servers github
```

### 2. 安全管理 API 密钥

```bash
# ✅ 推荐: 使用环境变量
export TAVILY_API_KEY="..."
export GITHUB_TOKEN="..."

# ❌ 不推荐: 硬编码在脚本
# 永远不要把密钥提交到 Git

# 💡 使用 .env 文件 (记得 .gitignore)
# .env
# TAVILY_API_KEY=...
# GITHUB_TOKEN=...
```

### 3. 定期更新

```bash
# MCP 服务器会定期更新，保持最新
npm update -g @modelcontextprotocol/server-sequential-thinking
```

### 4. 监控使用情况

注意 API 配额和成本:

- **Tavily**: 免费配额 (检查: https://app.tavily.com)
- **GitHub**: GitHub API 率限制 (60 req/hr 未认证, 5000 req/hr 已认证)
- **PostgreSQL**: 自托管，无额外成本
- **Puppeteer**: 自托管，无额外成本

### 5. 工作流集成

在你的工作流中使用 MCP:

```bash
# 工作流示例
/wf_01_planning                    # 规划 (可选使用 sequential-thinking)
/wf_03_prime                       # 加载上下文
/wf_04_ask "架构决策"             # 使用 sequential-thinking
/wf_04_research "技术选型"         # 使用 tavily + sequential-thinking
/wf_05_code "实现功能"            # 无需 MCP
/wf_08_review                      # 无需 MCP
/wf_11_commit                      # 可选使用 github
```

---

## 相关文档

- [Anthropic MCP 官方文档](https://modelcontextprotocol.io)
- [MCP 服务器仓库](https://github.com/modelcontextprotocol/servers)
- [Claude Code 文档](https://docs.claude.com/)
- [项目 README](../../README.md)

---

**最后更新**: 2025-11-22
**维护者**: AI Workflow Command System
**相关配置**: `src/mcp/configs/`, `scripts/install_mcp.py`
