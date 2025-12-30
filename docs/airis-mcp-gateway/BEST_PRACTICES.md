---
title: "AIRIS MCP Gateway 最佳实践"
description: "基于实际使用经验的最佳实践集合，包含三步工作流、错误处理、性能优化和常见陷阱规避"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-30"
last_updated: "2025-12-30"
related_documents:
  - "docs/airis-mcp-gateway/README.md"
  - "docs/airis-mcp-gateway/GETTING_STARTED.md"
  - "docs/airis-mcp-gateway/PARAMETER_TRAPS.md"
  - "docs/airis-mcp-gateway/TROUBLESHOOTING.md"
related_code: []
---

# AIRIS MCP Gateway 最佳实践

**目标**: 基于实际使用经验，提供可操作的最佳实践指南

**适用人群**: 已完成快速入门，希望提升使用效率和避免常见问题的用户

---

## 🎯 核心原则

### 1. 严格遵守三步工作流

**原则**: 永远不要跳过 Step 2 (airis-schema)

**为什么重要**:
- 90% 的参数错误都因跳过参数验证
- 参数名称往往不符合直觉（例如 `memory_file_name` 而非 `path`）
- 节省调试时间，第一次就做对

**实践示例**:

```typescript
// ❌ 错误：直接猜测参数
airis-exec({
  tool: "serena:read_memory",
  arguments: { path: "project_overview" }  // 错误！
})
// → Error: Field required [type=missing, input_value={'path': 'project_overview'}]

// ✅ 正确：先用 airis-schema 验证
airis-schema({ tool: "serena:read_memory" })
// → 返回: memory_file_name (必需)

airis-exec({
  tool: "serena:read_memory",
  arguments: { memory_file_name: "project_overview" }  // 正确！
})
// → Success!
```

---

### 2. 使用空查询避免 airis-find bug

**问题**: 带参数查询可能返回 0 结果

**解决方案**: 使用空查询 + 手动过滤

**实践示例**:

```typescript
// ❌ 可能失败：带参数查询
airis-find({ query: "memory" })
// → Found 0 tools (bug)

// ✅ 稳定方案：空查询 + 过滤
airis-find({ query: "" })
// → Found 112 tools
// → 然后手动筛选包含 "memory" 的工具
```

---

### 3. 理解并利用 HOT/COLD 模式

**原则**: 根据使用频率选择模式

**HOT 模式（5 个服务器）**:
- airis-agent
- memory
- gateway-control
- airis-commands
- **serena** (高频使用，实际配置为 HOT)

**优势**: 即时响应（<100ms）
**成本**: 持续占用内存

**COLD 模式（8 个服务器）**:
- playwright, tavily, context7, morphllm, magic, chrome-devtools, fetch, sequential-thinking

**优势**: 节省资源
**成本**: 首次调用需 2-10 秒

**实践建议**:

```json
// 如果 playwright 频繁使用，改为 HOT
{
  "mcpServers": {
    "playwright": {
      "enabled": true,
      "mode": "hot"  // 从 cold 改为 hot
    }
  }
}
```

---

## 🛡️ 错误处理策略

### 1. 参数验证错误

**场景**: 调用工具时参数名称错误

**诊断**:
```
Error: 1 validation error for applyArguments
memory_file_name
  Field required [type=missing, input_value={'path': 'project_overview'}]
```

**解决流程**:
1. 使用 `airis-schema` 查看正确参数名
2. 查阅 [PARAMETER_TRAPS.md](PARAMETER_TRAPS.md) 确认常见陷阱
3. 使用正确参数名重新调用

**防御性编程**:

```typescript
// ✅ 总是验证参数
async function safeExec(tool: string, rawArguments: any) {
  // Step 1: 获取 schema
  const schema = await airis-schema({ tool });

  // Step 2: 验证必需参数
  const required = schema.inputSchema.required || [];
  for (const param of required) {
    if (!(param in rawArguments)) {
      throw new Error(`Missing required parameter: ${param}`);
    }
  }

  // Step 3: 执行工具
  return await airis-exec({ tool, arguments: rawArguments });
}
```

---

### 2. API Key 未设置

**场景**: 调用需要 API Key 的服务器

**诊断**:
```
Error: Tavily API key not configured
```

**解决流程**:
1. 检查 `.env` 文件是否存在
2. 确认 API Key 已正确设置
3. 重启 Docker 容器（`docker compose restart api`）

**预防措施**:

```bash
# .env 文件模板
TAVILY_API_KEY=your-key-here
MORPH_API_KEY=your-key-here
MAGIC_API_KEY=your-key-here

# 验证环境变量
docker compose exec api env | grep _API_KEY
```

---

### 3. 服务器未启动

**场景**: COLD 模式服务器首次调用超时

**诊断**:
```
Error: Tool execution timeout (waited 30s)
```

**正确理解**:
- ⚠️ 这是 COLD 模式的正常行为
- ⚠️ 首次调用需要 2-10 秒启动服务器
- ✅ 后续调用会很快

**最佳实践**:

```typescript
// ❌ 不要：盲目重试
await airis-exec({ tool: "playwright:browser_navigate", ... });
// → Timeout!
await airis-exec({ tool: "playwright:browser_navigate", ... });
// → Still timeout!

// ✅ 应该：给予足够的启动时间
// 方案 1: 使用更长的超时时间（首次调用）
await airis-exec({ tool: "playwright:browser_navigate", ... }, { timeout: 15000 });

// 方案 2: 改为 HOT 模式（频繁使用）
// 修改 mcp-config.json: "mode": "hot"
```

---

## ⚡ 性能优化

### 1. 优先使用 HOT 模式服务器

**策略**: 能用 HOT 就用 HOT

**实例**:

```typescript
// ✅ 优先使用 memory（HOT）存储知识
airis-exec({
  tool: "memory:create_entities",
  arguments: { entities: [...] }
})

// 而非 serena（COLD，但实际配置为 HOT）
airis-exec({
  tool: "serena:write_memory",
  arguments: { memory_file_name: "...", content: "..." }
})
```

---

### 2. 批量操作的并发控制

**问题**: 同时调用多个 COLD 模式服务器可能导致资源竞争

**解决方案**: 限制并发数

**实践示例**:

```typescript
// ❌ 避免：同时启动多个 COLD 服务器
await Promise.all([
  airis-exec({ tool: "playwright:browser_navigate", ... }),
  airis-exec({ tool: "tavily:search", ... }),
  airis-exec({ tool: "context7:query-docs", ... })
]);
// → 可能导致资源竞争，所有调用都变慢

// ✅ 推荐：顺序执行或限制并发
for (const tool of ["playwright:browser_navigate", "tavily:search", "context7:query-docs"]) {
  await airis-exec({ tool, arguments: {...} });
}

// 或使用并发控制（例如 p-limit）
import pLimit from 'p-limit';
const limit = pLimit(2);  // 最多2个并发
await Promise.all(tools.map(tool => limit(() => airis-exec({ tool, ... }))));
```

---

### 3. 缓存常用 schema

**优化**: 避免重复调用 airis-schema

**实践示例**:

```typescript
// ✅ 建立 schema 缓存
const schemaCache = new Map<string, any>();

async function getCachedSchema(tool: string) {
  if (!schemaCache.has(tool)) {
    const schema = await airis-schema({ tool });
    schemaCache.set(tool, schema);
  }
  return schemaCache.get(tool);
}

// 使用缓存
const schema = await getCachedSchema("serena:read_memory");
```

---

## 🚨 常见陷阱规避

### 1. 参数命名陷阱

**高频陷阱**（查看完整列表：[PARAMETER_TRAPS.md](PARAMETER_TRAPS.md)）:

| 服务器 | 工具 | ❌ 错误参数 | ✅ 正确参数 |
|--------|------|-----------|-----------|
| Serena | read_memory | `path`, `name` | `memory_file_name` |
| Magic | generate_ui | `path`, `file` | `absolutePathToCurrentFile` |
| MorphLLM | query_codebase | `path` | `repo_path`（绝对路径） |
| Memory | remember | `text`, `content` | `observations`（数组） |
| Playwright | navigate | `timeout_ms` | `wait_until` |

**防御措施**:
- ✅ 总是使用 `airis-schema` 验证
- ✅ 查阅 PARAMETER_TRAPS.md
- ✅ 建立个人"陷阱笔记"

---

### 2. 路径类型陷阱

**问题**: 部分工具要求绝对路径

**识别方法**:

```typescript
// Magic: 要求绝对路径
airis-exec({
  tool: "magic:generate_ui",
  arguments: {
    absolutePathToCurrentFile: "/home/user/project/app.tsx"  // 绝对路径
  }
})

// MorphLLM: 要求绝对路径
airis-exec({
  tool: "morphllm:repo_query",
  arguments: {
    repo_path: "/home/user/project"  // 绝对路径
  }
})
```

**解决方案**:

```typescript
import path from 'path';

// 转换相对路径为绝对路径
const relativePath = "src/components/App.tsx";
const absolutePath = path.resolve(process.cwd(), relativePath);

airis-exec({
  tool: "magic:generate_ui",
  arguments: { absolutePathToCurrentFile: absolutePath }
});
```

---

### 3. 混淆工具用途

**场景**: 使用错误的工具完成任务

**常见错误**:

| ❌ 错误用法 | ✅ 正确用法 |
|-----------|-----------|
| 用 `screenshot` 做操作 | 操作用 `snapshot`，展示用 `screenshot` |
| 用 Memory 存储长文本 | 长文本用 Serena `write_memory`，结构化数据用 Memory |
| 用 Context7 搜索代码 | Context7 查库文档，代码搜索用 Serena/MorphLLM |

**选择工具的决策树**:

```
需要做什么？
├── 代码搜索 → Serena `semantic_search` 或 MorphLLM `repo_query`
├── 文档查询 → Context7 `query-docs`
├── Web 搜索 → Tavily `search`
├── 浏览器操作 → Playwright `browser_*`
├── 知识管理 → Memory `create_entities`（结构化）或 Serena `write_memory`（文本）
└── UI 生成 → Magic `generate_ui`
```

---

## 📊 调试和诊断

### 1. 系统化调试流程

**步骤**:

1. **确认服务器状态**
   ```bash
   curl -s http://localhost:9400/api/tools/status | jq '.roster.summary'
   ```

2. **验证工具可用性**
   ```typescript
   airis-find({ query: "" })  // 列出所有工具
   ```

3. **检查参数正确性**
   ```typescript
   airis-schema({ tool: "server:tool_name" })
   ```

4. **查看错误日志**
   ```bash
   docker compose logs -f api
   ```

5. **查阅故障排查文档**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

### 2. 日志分析技巧

**实践示例**:

```bash
# 过滤特定服务器的日志
docker compose logs api | grep "serena"

# 查看最近的错误
docker compose logs --tail=100 api | grep -i "error"

# 实时监控
docker compose logs -f api | grep -E "(error|warning|failed)"
```

---

## 🎓 高级技巧

### 1. 使用 AIRIS Agent 编排复杂任务

**场景**: 需要多步骤操作

**实践**:

```typescript
// 使用 AIRIS Agent 的高级工具
airis-exec({
  tool: "airis-agent:deep-research",
  arguments: {
    topic: "React 18 Concurrent Features",
    max_iterations: 5
  }
})
// → Agent 自动编排 Tavily 搜索、Context7 文档查询、Serena 代码搜索
```

---

### 2. 自定义配置 Profile

**使用 AIRIS Commands**:

```typescript
// Step 1: 保存当前配置为 Profile
airis-exec({
  tool: "airis-commands:airis_profile_save",
  arguments: { profile_name: "my-custom-profile" }
})

// Step 2: 切换配置
airis-exec({
  tool: "airis-commands:airis_profile_load",
  arguments: { profile_name: "my-custom-profile" }
})
```

---

### 3. 动态启用/禁用服务器

**节省资源**:

```typescript
// 临时禁用不需要的服务器
airis-exec({
  tool: "airis-commands:airis_config_set_enabled",
  arguments: {
    server_name: "chrome-devtools",
    enabled: false
  }
})

// 需要时重新启用
airis-exec({
  tool: "airis-commands:airis_config_set_enabled",
  arguments: {
    server_name: "chrome-devtools",
    enabled: true
  }
})
```

---

## 📝 检查清单

### 每次调用工具前

- [ ] 使用 `airis-find` 确认工具存在
- [ ] 使用 `airis-schema` 验证参数名
- [ ] 检查是否需要绝对路径
- [ ] 确认环境变量已设置（如需 API Key）

### 遇到错误时

- [ ] 检查参数名是否正确（参考 PARAMETER_TRAPS.md）
- [ ] 确认服务器是否启用（`mcp-config.json`）
- [ ] 查看 Docker 日志（`docker compose logs api`）
- [ ] 查阅 TROUBLESHOOTING.md

### 性能优化

- [ ] 频繁使用的服务器改为 HOT 模式
- [ ] 缓存常用 schema
- [ ] 限制并发调用数量
- [ ] 监控资源使用情况

---

## 🔗 相关资源

- **快速入门**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **参数陷阱**: [PARAMETER_TRAPS.md](PARAMETER_TRAPS.md)
- **故障排查**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **完整文档**: [README.md](README.md)

---

**最后更新**: 2025-12-30
**版本**: v1.0
**贡献**: 欢迎基于实际使用经验提交最佳实践
