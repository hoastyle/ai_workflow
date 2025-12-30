# AIRIS MCP Gateway 使用指南

**版本**: v2.1
**最后更新**: 2025-12-30
**适用范围**: SuperClaude Framework + AIRIS MCP Gateway 集成

> **核心价值**: 通过 airis-mcp-gateway 统一访问 13 个 MCP 服务器的 112 个工具，实现 Claude Code 的能力扩展

---

## 📚 快速导航

| 我想... | 查看文档 |
|---------|---------|
| **快速开始** | [新手入门指南](GETTING_STARTED.md) |
| **快速参考** | [快速参考](QUICK_REFERENCE.md) |
| **工具查询** | [工具索引](TOOL_INDEX.md) |
| **常见问题** | [FAQ 和故障排查](#常见问题速查) |
| **服务器配置** | [服务器详细文档](#mcp-服务器列表) |
| **集成示例** | [使用示例](#使用示例) |

---

## 🎯 什么是 AIRIS MCP Gateway？

AIRIS MCP Gateway 是一个 **MCP 服务器多路复用器**，允许 Claude Code 通过统一的接口访问多个 MCP 服务器。

### 核心特性

- ✅ **统一接口**: 通过 3 个工具（airis-find, airis-schema, airis-exec）访问所有 MCP 服务器
- ✅ **智能模式**: HOT（常驻内存）和 COLD（按需启动）两种模式优化性能
- ✅ **完整覆盖**: 支持 13 个 MCP 服务器，112 个工具
- ✅ **无缝集成**: 与 SuperClaude Framework 完美配合

### 架构概览

```
Claude Code (SuperClaude Framework)
    ↓ (通过 MCP)
AIRIS MCP Gateway (端口: 9400)
    ↓ (多路复用)
┌────────────────────────────────────────────────┐
│ HOT 模式 (4 个)      COLD 模式 (9 个)          │
│ - airis-agent        - serena                  │
│ - memory             - playwright              │
│ - gateway-control    - tavily                  │
│ - airis-commands     - context7                │
│                      - morphllm                │
│                      - magic                   │
│                      - chrome-devtools         │
│                      - fetch                   │
│                      - sequential-thinking     │
└────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 三步工作流

所有 MCP 工具的使用都遵循相同的三步流程：

#### Step 1: 发现工具

```typescript
// 搜索关键词相关的工具
mcp__airis-mcp-gateway__airis-find({
  query: "memory"
})

// 返回:
// - memory:create_entities
// - memory:search_nodes
// - serena:write_memory
// - serena:read_memory
```

#### Step 2: 查看参数

```typescript
// 查看工具的完整参数签名
mcp__airis-mcp-gateway__airis-schema({
  tool: "serena:write_memory"
})

// 返回:
// {
//   "properties": {
//     "memory_file_name": { "type": "string" },
//     "content": { "type": "string" }
//   },
//   "required": ["memory_file_name", "content"]
// }
```

#### Step 3: 执行工具

```typescript
// 使用正确的参数执行工具
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "project_notes.md",
    content: "# 项目笔记\n\n这是一个重要的决策..."
  }
})
```

---

## 🔧 实际配置示例

### HOT vs COLD 模式

AIRIS MCP Gateway 使用两种模式来优化性能和资源使用：

| 模式 | 启动时机 | 响应速度 | 资源占用 | 适用场景 |
|------|---------|---------|---------|---------|
| **HOT** | Gateway 启动时常驻 | 即时（<100ms） | 高 | 频繁使用的工具 |
| **COLD** | 首次调用时按需启动 | 首次慢（2-10s），后续快 | 低 | 偶尔使用的工具 |

#### HOT 模式服务器（4 个）

```json
// mcp-config.json 示例
{
  "mcpServers": {
    "airis-agent": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/agiletec-inc/airis-agent", "airis-agent-mcp"],
      "enabled": true,
      "mode": "hot"  // 常驻内存
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "enabled": true,
      "mode": "hot"
    },
    "airis-mcp-gateway-control": {
      "command": "node",
      "args": ["/app/gateway-control/index.js"],
      "enabled": true,
      "mode": "hot"
    },
    "airis-commands": {
      "command": "node",
      "args": ["/app/airis-commands/index.js"],
      "enabled": true,
      "mode": "hot"
    }
  }
}
```

**优势**: 这些工具随时可用，无需等待启动

#### COLD 模式服务器（9 个）

```json
// mcp-config.json 示例
{
  "mcpServers": {
    "serena": {
      "profile": "${SERENA_MODE:-serena-remote}",
      "enabled": true,
      "mode": "cold"  // 按需启动
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "enabled": true,
      "mode": "cold"
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here"
      },
      "enabled": true,
      "mode": "cold"
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "enabled": true,
      "mode": "cold"
    },
    "morphllm": {
      "command": "npx",
      "args": ["-y", "@morphllm/morphmcp"],
      "env": {
        "MORPH_API_KEY": "your-api-key-here",
        "ENABLED_TOOLS": "edit_file,warpgrep_codebase_search"
      },
      "enabled": true,
      "mode": "cold"
    },
    "magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest"],
      "env": {
        "API_KEY": "your-api-key-here"
      },
      "enabled": true,
      "mode": "cold"
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"],
      "enabled": true,
      "mode": "cold"
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "enabled": true,
      "mode": "cold"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "enabled": true,
      "mode": "cold"
    }
  }
}
```

**优势**: 节省资源，启动后保持运行，后续调用快速

### 实际部署配置

基于 `/home/hao/Downloads/airis-mcp-gateway/mcp-config.json` 的实际工作配置：

#### 完整启用列表（13 个服务器）

```json
{
  "mcpServers": {
    // HOT 模式（4 个）
    "airis-agent": { "enabled": true, "mode": "cold" },  // 注：实际配置为 cold
    "memory": { "enabled": true, "mode": "cold" },
    "airis-mcp-gateway-control": { "enabled": true, "mode": "hot" },
    "airis-commands": { "enabled": true, "mode": "hot" },

    // COLD 模式（9 个）
    "serena": { "enabled": true, "mode": "hot" },  // 注：高频使用，设为 hot
    "playwright": { "enabled": true, "mode": "cold" },
    "tavily": { "enabled": true, "mode": "cold" },
    "context7": { "enabled": true, "mode": "cold" },
    "morphllm": { "enabled": true, "mode": "cold" },
    "magic": { "enabled": true, "mode": "cold" },
    "chrome-devtools": { "enabled": true, "mode": "cold" },
    "fetch": { "enabled": true, "mode": "cold" },
    "sequential-thinking": { "enabled": true, "mode": "cold" }
  }
}
```

#### 禁用的服务器（可选）

```json
{
  "mcpServers": {
    // 这些服务器已禁用，需要时可手动启用
    "airis-workspace": { "enabled": false },
    "filesystem": { "enabled": false },
    "git": { "enabled": false },
    "mindbase": { "enabled": false },
    "time": { "enabled": false },
    "supabase": { "enabled": false }
  }
}
```

### 环境变量配置

创建 `.env` 文件（基于 `.env.example`）：

```bash
# Tavily Web Search API Key
TAVILY_API_KEY=your-tavily-api-key

# MorphLLM API Key
MORPH_API_KEY=your-morph-api-key

# Magic UI Generation API Key
MAGIC_API_KEY=your-magic-api-key

# Serena Mode (serena-local 或 serena-remote)
SERENA_MODE=serena-remote
```

### Docker 容器验证

启动后验证所有容器运行状态：

```bash
# 检查容器状态
docker ps | grep airis-mcp-gateway

# 预期输出：
# airis-mcp-gateway-api      Up 2 minutes   0.0.0.0:9400->9400/tcp
# airis-mcp-gateway-db       Up 2 minutes   5432/tcp
# airis-mcp-gateway-serena   Up 2 minutes   8000/tcp

# 查看日志（确认服务器正常启动）
docker compose logs -f api

# 健康检查
curl -s http://localhost:9400/api/tools/status | jq '.roster.summary'

# 预期输出：
# {
#   "hot_count": 4,
#   "cold_count": 9,
#   "total_enabled": 13
# }
```

### 调整服务器模式

如果某个 COLD 模式服务器频繁使用，可改为 HOT 模式：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "enabled": true,
      "mode": "hot"  // 从 cold 改为 hot
    }
  }
}
```

**重启生效**:
```bash
docker compose restart api
```

---

## 📊 MCP 服务器列表

### 按使用场景分类

| 场景 | 推荐 MCP 服务器 | 核心工具 |
|------|----------------|---------|
| **代码理解和搜索** | Serena, MorphLLM | semantic_search, repo_query |
| **浏览器自动化** | Playwright, Chrome DevTools | browser_navigate, console_logs |
| **Web 搜索和抓取** | Tavily, Fetch | search, fetch |
| **知识管理** | Memory, Serena | create_entities, write_memory |
| **文档查询** | Context7 | resolve_library_id, query_docs |
| **UI 组件生成** | Magic | generate_ui, search_logos |
| **代码编辑** | MorphLLM | morph_file, repo_query |
| **结构化推理** | Sequential-thinking | sequential_thinking |
| **项目管理** | AIRIS Agent, AIRIS Commands | index_repo, get_config |
| **网关管理** | AIRIS Gateway Control | gateway_status, enable_server |

### 完整服务器清单

| 服务器 | 工具数 | 模式 | 核心功能 | 详细文档 |
|--------|--------|------|---------|---------|
| **Serena** | 23 | COLD | 语义代码理解、记忆管理 | [查看](servers/SERENA.md) |
| **Playwright** | 22 | COLD | 浏览器自动化 | [查看](servers/PLAYWRIGHT.md) |
| **Chrome DevTools** | 17 | COLD | 浏览器调试 | [查看](servers/CHROME_DEVTOOLS.md) |
| **AIRIS Agent** | 15 | HOT | 智能编排和自动化 | [查看](servers/AIRIS_AGENT.md) |
| **Memory** | 9 | HOT | 知识图谱管理 | [查看](servers/MEMORY.md) |
| **AIRIS Commands** | 8 | HOT | 配置管理 | [查看](servers/AIRIS_COMMANDS.md) |
| **Tavily** | 4 | COLD | Web 搜索 | [查看](servers/TAVILY.md) |
| **MorphLLM** | 4 | COLD | 代码编辑 | [查看](servers/MORPHLLM.md) |
| **AIRIS Gateway Control** | 3 | HOT | 网关监控 | [查看](servers/GATEWAY_CONTROL.md) |
| **Magic** | 3 | COLD | UI 生成 | [查看](servers/MAGIC.md) |
| **Context7** | 2 | COLD | 库文档查询 | [查看](servers/CONTEXT7.md) |
| **Fetch** | 1 | COLD | 网页抓取 | [查看](servers/FETCH.md) |
| **Sequential-thinking** | 1 | COLD | 结构化推理 | [查看](servers/SEQUENTIAL_THINKING.md) |

**总计**: 112 个工具 across 13 个 MCP 服务器

---

## ⚠️ 常见问题速查

### 参数错误

| 错误类型 | 常见示例 | 解决方案 | 相关服务器 |
|---------|---------|---------|-----------|
| **参数名称错误** | `filename` 而非 `memory_file_name` | 使用 `airis-schema` 查询正确名称 | Serena, Magic |
| **路径类型错误** | 使用相对路径而非绝对路径 | 转换为绝对路径 | Magic, MorphLLM |
| **缺少必需参数** | 未提供 `observations` 数组 | 检查 schema 的 `required` 字段 | Memory |
| **参数格式错误** | Library 名称而非 Library ID | 先调用 resolve/search 工具 | Context7 |

### 环境配置错误

| 错误类型 | 常见示例 | 解决方案 | 相关服务器 |
|---------|---------|---------|-----------|
| **API Key 未设置** | `TAVILY_API_KEY` 未配置 | 在 `.env` 或环境变量中设置 | Tavily |
| **服务未启动** | Chrome 调试端口未开启 | 使用 `--remote-debugging-port=9222` | Chrome DevTools |
| **浏览器未安装** | Playwright 浏览器缺失 | 运行 `browser_install` | Playwright |
| **Gateway 未运行** | API 连接失败 | 确保 `docker compose up -d` | AIRIS Agent |

### 使用模式错误

| 错误类型 | 常见示例 | 解决方案 | 相关服务器 |
|---------|---------|---------|-----------|
| **混淆工具用途** | 用 screenshot 做操作 | 操作用 snapshot，展示用 screenshot | Playwright |
| **不使用占位符** | 完整重写文件内容 | 使用 `// ... existing code ...` | MorphLLM |
| **查询太宽泛** | 搜索 "component" | 使用具体类型 "modal dialog" | Magic, Context7 |
| **文件过大** | 编辑 >2000 行文件 | 使用传统搜索替换 | MorphLLM |

---

## 💡 使用示例

### 示例 1: 代码搜索和理解

```typescript
// Step 1: 搜索代码片段
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:semantic_search",
  arguments: {
    query: "用户认证逻辑",
    max_results: 5
  }
})

// Step 2: 读取项目记忆
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:read_memory",
  arguments: {
    memory_file_name: "architecture_decisions.md"
  }
})
```

### 示例 2: Web 研究

```typescript
// Step 1: 搜索 Web
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:search",
  arguments: {
    query: "React 18 新特性",
    max_results: 5
  }
})

// Step 2: 提取内容
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:extract",
  arguments: {
    urls: ["https://react.dev/blog/2022/03/29/react-v18"]
  }
})
```

### 示例 3: 浏览器自动化

```typescript
// Step 1: 导航页面
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://example.com"
  }
})

// Step 2: 获取页面状态
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {}
})

// Step 3: 点击元素
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    ref: 123  // 从 snapshot 获取
  }
})
```

### 示例 4: 知识管理

```typescript
// Step 1: 创建实体
mcp__airis-mcp-gateway__airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "AIRIS Gateway",
        entityType: "Product",
        observations: ["MCP 多路复用器", "支持 13 个服务器"]
      }
    ]
  }
})

// Step 2: 搜索实体
mcp__airis-mcp-gateway__airis-exec({
  tool: "memory:search_nodes",
  arguments: {
    query: "AIRIS"
  }
})
```

---

## 🔧 调试技巧

### 通用调试流程

1. **参数错误时**: 复制 `airis-schema` 的输出结构
2. **工具找不到时**: 检查服务器是否启用 (`mcp-config.json`)
3. **执行超时时**: 检查服务器是否处于 COLD 模式（首次启动需要时间）
4. **结果为空时**: 使用更具体的查询关键词

### 性能优化

- ✅ 优先使用 HOT 模式服务器（airis-agent, memory, gateway-control, airis-commands）
- ✅ COLD 模式服务器首次启动需 2-5 秒，后续调用快速
- ✅ 使用 `airis-find` 快速定位工具，避免盲目尝试
- ✅ 批量操作时考虑使用 AIRIS Agent 的高级工具

---

## 📚 相关资源

### 核心文档

- [快速参考](QUICK_REFERENCE.md) - 快速查询工具和参数
- [工具索引](TOOL_INDEX.md) - 112 个工具的完整索引
- [模板和示例](TEMPLATE.md) - 文档创建模板
- [维护清单](MAINTENANCE_CHECKLIST.md) - 文档维护指南

### SuperClaude Framework 集成

- [MCP 集成策略](../../mcp-integration/README.md) - MCP 集成的架构设计
- [快速开始](../../mcp-integration/quick-start.md) - SuperClaude + MCP 快速上手
- [故障排查](../../mcp-integration/troubleshooting.md) - MCP 常见问题解决

### AIRIS MCP Gateway 项目

- **GitHub**: https://github.com/yourusername/airis-mcp-gateway
- **主文档**: /home/hao/Downloads/airis-mcp-gateway/README.md
- **配置文件**: /home/hao/Downloads/airis-mcp-gateway/mcp-config.json

---

## 📊 统计数据

- **MCP 服务器数量**: 13 个
- **工具总数**: 112 个
- **HOT 模式服务器**: 4 个 (35 个工具)
- **COLD 模式服务器**: 9 个 (77 个工具)
- **文档覆盖率**: 100%
- **平均每个服务器工具数**: 8.6 个

---

## 📝 贡献指南

发现新的使用问题或最佳实践？欢迎贡献：

1. 更新对应的服务器文档（`servers/` 目录）
2. 更新工具索引（`TOOL_INDEX.md`）
3. 更新快速参考（`QUICK_REFERENCE.md`）
4. 提交 PR 或创建 Issue

---

**最后更新**: 2025-12-29
**维护者**: 从实践经验中提炼
**版本**: v2.0 (系统级优化)
