# AIRIS MCP Gateway 快速参考

**版本**: v2.1
**最后更新**: 2025-12-30
**目的**: 快速查询常用工具和参数

---

## ⚡ HOT vs COLD 模式

| 模式 | 响应速度 | 服务器（13 个） | 说明 |
|------|---------|----------------|------|
| **🔥 HOT** | 即时（<100ms） | airis-agent, memory, gateway-control, airis-commands, **serena** | Gateway 启动时常驻，立即响应 |
| **❄️ COLD** | 首次慢（2-10s）<br>后续快（<500ms） | playwright, tavily, context7, morphllm, magic, chrome-devtools, fetch, sequential-thinking | 按需启动，节省资源 |

**选择建议**:
- ✅ 频繁使用 → 改为 HOT 模式（修改 `mcp-config.json`）
- ✅ 偶尔使用 → 保持 COLD 模式（节省资源）
- ⚠️ COLD 模式首次调用需等待 2-10 秒（正常行为）

---

## 🚀 三步工作流

```typescript
// Step 1: 发现工具
airis-find(query: "keyword")

// Step 2: 查看参数
airis-schema(tool: "server:tool_name")

// Step 3: 执行工具
airis-exec(tool: "server:tool_name", arguments: {...})
```

---

## 📚 常用工具速查

### 代码理解

| 工具 | 服务器 | 用途 | 示例 |
|-----|--------|------|------|
| `semantic_search` | Serena | 语义搜索代码 | `query: "用户认证"` |
| `repo_query` | MorphLLM | 仓库查询 | `question: "如何实现登录？"` |
| `grep_search` | MorphLLM | 全文搜索 | `pattern: "function.*login"` |

### 记忆管理

| 工具 | 服务器 | 用途 | 关键参数 |
|-----|--------|------|---------|
| `write_memory` | Serena | 写入记忆 | `memory_file_name`, `content` |
| `read_memory` | Serena | 读取记忆 | `memory_file_name` |
| `list_memories` | Serena | 列出记忆 | 无参数 |

### 知识图谱

| 工具 | 服务器 | 用途 | 关键参数 |
|-----|--------|------|---------|
| `create_entities` | Memory | 创建实体 | `entities` (数组) |
| `search_nodes` | Memory | 搜索节点 | `query` |
| `create_relations` | Memory | 创建关系 | `relations` (数组) |

### Web 搜索

| 工具 | 服务器 | 用途 | 关键参数 |
|-----|--------|------|---------|
| `search` | Tavily | Web 搜索 | `query`, `max_results` |
| `extract` | Tavily | 内容提取 | `urls` (数组) |
| `fetch` | Fetch | 获取 Markdown | `url`, `max_length` |

### 浏览器自动化

| 工具 | 服务器 | 用途 | 关键参数 |
|-----|--------|------|---------|
| `browser_navigate` | Playwright | 导航页面 | `url` |
| `browser_snapshot` | Playwright | 获取状态 | 无参数 |
| `browser_click` | Playwright | 点击元素 | `ref` |
| `browser_fill` | Playwright | 填充表单 | `ref`, `value` |

### 文档查询

| 工具 | 服务器 | 用途 | 关键参数 |
|-----|--------|------|---------|
| `resolve-library-id` | Context7 | 获取库 ID | `library_name` |
| `query-docs` | Context7 | 查询文档 | `library_id`, `query` |

### UI 生成

| 工具 | 服务器 | 用途 | 关键参数 |
|-----|--------|------|---------|
| `generate_ui` | Magic | 生成 UI | `absolutePathToCurrentFile`, `description` |
| `search_logos` | Magic | 搜索 Logo | `query` |

---

## ⚠️ 关键注意事项

### Serena MCP

```typescript
// ❌ 错误：使用常规参数名
airis-exec(tool: "serena:write_memory", arguments: {
  filename: "file.md",  // 错误！
  content: "..."
})

// ✅ 正确：使用 MCP 特定参数名
airis-exec(tool: "serena:write_memory", arguments: {
  memory_file_name: "file.md",  // 正确！
  content: "..."
})
```

### Magic MCP

```typescript
// ❌ 错误：使用相对路径
airis-exec(tool: "magic:generate_ui", arguments: {
  absolutePathToCurrentFile: "./components/Button.tsx"  // 错误！
})

// ✅ 正确：使用绝对路径
airis-exec(tool: "magic:generate_ui", arguments: {
  absolutePathToCurrentFile: "/home/user/project/components/Button.tsx"  // 正确！
})
```

### Memory MCP

```typescript
// ❌ 错误：缺少 observations
airis-exec(tool: "memory:create_entities", arguments: {
  entities: [
    { name: "User", entityType: "Concept" }  // 错误！缺少 observations
  ]
})

// ✅ 正确：必须提供 observations
airis-exec(tool: "memory:create_entities", arguments: {
  entities: [
    {
      name: "User",
      entityType: "Concept",
      observations: ["用户实体", "包含认证信息"]  // 正确！
    }
  ]
})
```

### Context7 MCP

```typescript
// ❌ 错误：直接使用库名称
airis-exec(tool: "context7:query-docs", arguments: {
  library_id: "react",  // 错误！这是库名称，不是 ID
  query: "useState"
})

// ✅ 正确：先获取库 ID
// Step 1:
airis-exec(tool: "context7:resolve-library-id", arguments: {
  library_name: "react"
})
// 返回: { library_id: "xxx" }

// Step 2:
airis-exec(tool: "context7:query-docs", arguments: {
  library_id: "xxx",  // 正确！使用返回的 ID
  query: "useState"
})
```

### MorphLLM MCP

```typescript
// ❌ 错误：不使用占位符
airis-exec(tool: "morphllm:morph_file", arguments: {
  repo_path: "/path/to/repo",
  file_path: "src/file.ts",
  operations: [{
    type: "replace",
    old_content: "整个文件内容...",  // 错误！太长
    new_content: "整个修改后内容..."
  }]
})

// ✅ 正确：使用占位符
airis-exec(tool: "morphllm:morph_file", arguments: {
  repo_path: "/path/to/repo",
  file_path: "src/file.ts",
  operations: [{
    type: "replace",
    old_content: "function oldName() {",
    new_content: "function newName() {"
  }]
})
// 使用 "... existing code ..." 表示未更改部分
```

---

## 🔍 常见场景快速指南

### 场景 1: 完整的 Web 研究

```typescript
// Step 1: 搜索
airis-exec(tool: "tavily:search", arguments: {
  query: "React Server Components",
  max_results: 5
})

// Step 2: 提取内容
airis-exec(tool: "tavily:extract", arguments: {
  urls: ["https://react.dev/blog/..."]
})

// Step 3: 保存到记忆
airis-exec(tool: "serena:write_memory", arguments: {
  memory_file_name: "react_research.md",
  content: "# React Server Components\n\n..."
})
```

### 场景 2: 代码搜索和编辑

```typescript
// Step 1: 语义搜索
airis-exec(tool: "morphllm:semantic_query", arguments: {
  repo_path: "/path/to/repo",
  query: "用户登录函数"
})

// Step 2: 编辑文件
airis-exec(tool: "morphllm:morph_file", arguments: {
  repo_path: "/path/to/repo",
  file_path: "src/auth.ts",
  operations: [...]
})
```

### 场景 3: 知识整理

```typescript
// Step 1: 创建实体
airis-exec(tool: "memory:create_entities", arguments: {
  entities: [
    {
      name: "React Hooks",
      entityType: "Concept",
      observations: ["状态管理", "副作用处理"]
    }
  ]
})

// Step 2: 创建关系
airis-exec(tool: "memory:create_relations", arguments: {
  relations: [
    {
      from: "React Hooks",
      to: "useState",
      relationType: "includes"
    }
  ]
})

// Step 3: 搜索知识
airis-exec(tool: "memory:search_nodes", arguments: {
  query: "React"
})
```

### 场景 4: 浏览器测试

```typescript
// Step 1: 导航
airis-exec(tool: "playwright:browser_navigate", arguments: {
  url: "https://example.com/login"
})

// Step 2: 获取状态
const snapshot = airis-exec(tool: "playwright:browser_snapshot", arguments: {})

// Step 3: 填充表单
airis-exec(tool: "playwright:browser_fill", arguments: {
  ref: snapshot.elements.find(e => e.name === "username").ref,
  value: "testuser"
})

// Step 4: 点击提交
airis-exec(tool: "playwright:browser_click", arguments: {
  ref: snapshot.elements.find(e => e.role === "button").ref
})
```

---

## 📊 服务器模式对照

### HOT 模式（常驻内存，立即响应）

| 服务器 | 工具数 | 核心用途 |
|--------|--------|---------|
| airis-agent | 15 | 项目索引、代码生成 |
| memory | 9 | 知识图谱 |
| airis-commands | 8 | 配置管理 |
| gateway-control | 3 | 网关监控 |

**总计**: 35 个工具

### COLD 模式（按需启动，首次 2-5 秒）

| 服务器 | 工具数 | 核心用途 |
|--------|--------|---------|
| serena | 23 | 代码理解、记忆 |
| playwright | 22 | 浏览器自动化 |
| chrome-devtools | 17 | 浏览器调试 |
| tavily | 4 | Web 搜索 |
| morphllm | 4 | 代码编辑 |
| magic | 3 | UI 生成 |
| context7 | 2 | 库文档 |
| fetch | 1 | 网页抓取 |
| sequential-thinking | 1 | 结构化推理 |

**总计**: 77 个工具

---

## 🔗 相关资源

- **完整文档**: [README.md](README.md)
- **工具索引**: [TOOL_INDEX.md](TOOL_INDEX.md)
- **服务器详情**: [servers/](servers/)
- **全局参考**: `~/.claude/mcp-notes/QUICK_REFERENCE.md`

---

**最后更新**: 2025-12-29
**维护者**: 从实践经验中提炼
