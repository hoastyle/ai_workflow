---
title: "AIRIS MCP Gateway 故障排查指南"
description: "完整的故障排查步骤、常见问题解决方案和调试技巧"
type: "故障排查"
status: "完成"
priority: "高"
created_date: "2025-12-30"
last_updated: "2025-12-30"
related_documents:
  - "README.md"
  - "QUICK_REFERENCE.md"
  - "PARAMETER_TRAPS.md"
related_code: []
---

# AIRIS MCP Gateway 故障排查指南

**版本**: v1.0
**最后更新**: 2025-12-30
**适用范围**: AIRIS MCP Gateway 所有版本

---

## 🚨 本文档创建背景

**发现问题**: 在 2025-12-30 的会话中，使用 `airis-find` 查询 Serena 工具时遇到多次失败，具体表现为：
- 带 `query: "serena"` 参数的查询返回 "Found 0 tools"
- 空查询（不带参数）反而成功返回所有工具
- 需要多次重试才能成功

这暴露了 AIRIS MCP Gateway 的潜在问题和文档缺失。

---

## 📋 快速诊断清单

### 1. Gateway 是否运行？

```bash
# 检查 Gateway 健康状态
curl http://localhost:9400/health

# 预期输出
{"status":"ok","timestamp":"2025-12-30T..."}
```

**如果失败**:
- Gateway 未启动 → 查看"Gateway 未运行"章节
- 端口被占用 → 查看"端口冲突"章节

### 2. MCP 服务器是否可用？

```typescript
// 使用 gateway-control 检查服务器状态
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

console.log(servers);
// 查看每个服务器的 status: ready/starting/failed
```

### 3. airis-find 是否正常工作？

```typescript
// 测试 1: 空查询（应该返回所有工具）
const allTools = await airis-find({ query: "" });
console.log(`总工具数: ${allTools.length}`);

// 测试 2: 带查询（可能失败）
const serenaTools = await airis-find({ query: "serena" });
console.log(`Serena 工具数: ${serenaTools.length}`);
```

**如果测试 1 成功但测试 2 失败** → 这是已知问题，查看"airis-find 查询失败"章节

---

## 🐛 常见问题和解决方案

### 问题 1: airis-find 查询特定服务器返回 0 结果

**现象**:
```typescript
const tools = await airis-find({ query: "serena" });
// 返回: Found 0 tools across 15 servers
```

**原因分析**:
- **已知 Bug**: AIRIS MCP Gateway 的 airis-find 工具在某些情况下查询特定关键词会失败
- **触发条件**: 查询 HOT 模式服务器（如 serena, memory）时更容易出现
- **根本原因**: Gateway 查询逻辑可能存在竞态条件或缓存问题

**解决方案（按优先级）**:

**方案 A: 使用空查询 + 手动过滤** (推荐)
```typescript
// 1. 获取所有工具
const allTools = await airis-find({ query: "" });

// 2. 手动过滤
const serenaTools = allTools.filter(t =>
  t.name.startsWith("serena:")
);

console.log(`找到 ${serenaTools.length} 个 Serena 工具`);
```

**方案 B: 重试机制**
```typescript
async function findWithRetry(query: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const tools = await airis-find({ query });

    if (tools.length > 0) {
      return tools;
    }

    console.log(`重试 ${i + 1}/${maxRetries}...`);
    await sleep(1000);
  }

  // 最后尝试空查询
  console.warn("使用空查询作为回退方案");
  const allTools = await airis-find({ query: "" });
  return allTools.filter(t => t.name.includes(query));
}

// 使用
const serenaTools = await findWithRetry("serena");
```

**方案 C: 直接使用工具名称**
```typescript
// 如果你知道工具的完整名称，直接调用 airis-schema
const schema = await airis-schema({
  tool: "serena:write_memory"
});

// 不需要 airis-find
```

**预防措施**:
- ✅ 在关键流程中使用方案 A（空查询 + 过滤）
- ✅ 为所有 airis-find 调用添加错误处理
- ✅ 文档化已知工具名称列表，避免依赖查询

---

### 问题 2: HOT 模式服务器显示 ready=false

**现象**:
```json
{
  "name": "serena",
  "mode": "HOT",
  "ready": false
}
```

**原因分析**:
- HOT 模式服务器应该常驻内存，但启动失败
- 可能原因：依赖未安装、配置错误、端口冲突

**解决方案**:

**Step 1: 检查服务器日志**
```bash
# Gateway 日志位置（根据安装方式）
# 方式 1: Docker
docker logs airis-mcp-gateway

# 方式 2: 本地运行
# 查看 Gateway 启动时的输出
```

**Step 2: 手动验证服务器可用性**
```typescript
// 尝试直接调用工具
try {
  const result = await airis-exec({
    tool: "serena:list_memories"
  });
  console.log("Serena 工具可用");
} catch (error) {
  console.error("Serena 工具不可用:", error.message);
}
```

**Step 3: 重启 Gateway**
```bash
# Docker 方式
docker restart airis-mcp-gateway

# 本地方式
# 停止 Gateway 进程并重新启动
```

---

### 问题 3: COLD 模式服务器启动超时

**现象**:
```
Error: Server 'playwright' startup timeout
```

**原因分析**:
- COLD 模式服务器按需启动，但启动时间过长
- 常见于 Playwright（需要下载浏览器）

**解决方案**:

**方案 A: 增加超时时间**
```typescript
async function waitForServerReady(serverName: string, maxWait = 30000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWait) {
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });

    const server = servers.find(s => s.name === serverName);

    if (server && server.ready) {
      console.log(`✅ ${serverName} 已就绪`);
      return true;
    }

    console.log(`⏳ 等待 ${serverName} 启动...`);
    await sleep(2000);
  }

  throw new Error(`${serverName} 启动超时`);
}

// 使用
await waitForServerReady("playwright", 30000);  // 30 秒超时
```

**方案 B: 预启动服务器**
```typescript
// 在工作流开始时预启动所有 COLD 模式服务器
const coldServers = ["playwright", "morphllm", "serena"];

await Promise.all(
  coldServers.map(name => waitForServerReady(name, 60000))
);

console.log("✅ 所有 COLD 模式服务器已就绪");
```

---

### 问题 4: Gateway 未运行

**现象**:
```
Error: Failed to connect to AIRIS MCP Gateway
Error: ECONNREFUSED localhost:9400
```

**解决方案**:

**Step 1: 检查 Gateway 是否在运行**
```bash
# 检查端口
lsof -i :9400
# 或
netstat -an | grep 9400
```

**Step 2: 启动 Gateway**
```bash
# Docker 方式
docker ps | grep airis-mcp-gateway
docker start airis-mcp-gateway

# 本地方式
# 根据你的安装方式启动 Gateway
```

**Step 3: 验证启动成功**
```bash
curl http://localhost:9400/health
```

---

### 问题 5: 参数验证错误（validation error）⭐ 高频问题

**现象**:
```typescript
await airis-exec({
    tool: "serena:read_memory",
    arguments: { path: "project_overview" }  // 直觉性参数名
});

// 错误信息
Error: 1 validation error for applyArguments
memory_file_name
  Field required [type=missing, input_value={'path': 'project_overview'}]
```

**原因分析**:
- **核心问题**: MCP 服务器参数命名不统一，直觉性假设经常错误
- **常见错误**: 假设参数名是 `path`, `name`, `filename`
- **实际要求**: Serena 使用 `memory_file_name`（反直觉但必需）

**解决方案**:

**方案 A: 使用 airis-schema 验证参数** (推荐 ⭐⭐⭐⭐⭐)
```typescript
// Step 1: 先查看正确的参数名
const schema = await airis-schema({ tool: "serena:read_memory" });
console.log("必需参数:", schema.inputSchema.required);
// 输出: ["memory_file_name"]

// Step 2: 使用正确的参数名
await airis-exec({
    tool: "serena:read_memory",
    arguments: {
        memory_file_name: "project_overview"  // 正确
    }
});
```

**方案 B: 查阅参数陷阱文档**
```bash
# 查看常见参数错误和正确用法
cat docs/airis-mcp-gateway/PARAMETER_TRAPS.md
```

**高频参数陷阱**:
| 工具 | 常见错误 | 正确参数 |
|------|---------|---------|
| `serena:read_memory` | `path`, `name` | `memory_file_name` ✅ |
| `serena:find_file` | `filename`, `path` | `file_mask`, `relative_path` ✅ |
| `magic:generate_ui` | `path`, `file` | `absolutePathToCurrentFile` ✅ |
| `morphllm:query_codebase` | `path` | `repo_path` (绝对路径) ✅ |

**预防措施**:
- ✅ 总是使用 `airis-schema` 验证参数
- ✅ 建立三步工作流习惯：airis-find → airis-schema → airis-exec
- ✅ 查阅 PARAMETER_TRAPS.md 快速参考

**详细说明**: 查看 [PARAMETER_TRAPS.md](PARAMETER_TRAPS.md) 获取完整的参数陷阱列表

---

### 问题 6: 工具执行返回空结果

**现象**:
```typescript
const result = await airis-exec({
  tool: "serena:find_symbol",
  arguments: { name: "MyClass" }
});

console.log(result);  // 空或 undefined
```

**可能原因**:

**原因 1: 项目未激活（Serena）**
```typescript
// 检查当前项目
const config = await airis-exec({
  tool: "serena:get_current_config"
});

console.log("Active project:", config.active_project);

// 如果没有激活项目，先激活
await airis-exec({
  tool: "serena:activate_project",
  arguments: { name: "my-project" }
});
```

**原因 2: 项目未索引（MorphLLM）**
```typescript
// MorphLLM 需要先索引项目
await airis-exec({
  tool: "airis-agent:index_repository",
  arguments: { repo_path: "/absolute/path/to/project" }
});
```

**原因 3: 参数命名错误**
```typescript
// ❌ 错误：使用 filename
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    filename: "test.md",  // 错误！
    content: "..."
  }
});

// ✅ 正确：使用 memory_file_name
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "test.md",  // 正确
    content: "..."
  }
});
```

---

## 🔧 高级调试技巧

### 1. 启用详细日志

```bash
# 设置环境变量启用 Gateway 详细日志
export AIRIS_LOG_LEVEL=debug

# 重启 Gateway
```

### 2. 使用 gateway-control 诊断

```typescript
// 获取完整的 Gateway 状态
const status = await airis-exec({
  tool: "gateway-control:health"
});

console.log("Gateway 状态:", JSON.stringify(status, null, 2));

// 列出所有服务器及其状态
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

for (const server of servers) {
  console.log(`${server.name}: ${server.mode} - ${server.ready ? "✅" : "❌"}`);
}
```

### 3. 测试工具可用性

```typescript
// 创建一个测试函数
async function testTool(toolName: string) {
  try {
    // 1. 检查工具是否存在
    const allTools = await airis-find({ query: "" });
    const tool = allTools.find(t => t.name === toolName);

    if (!tool) {
      console.error(`❌ 工具 ${toolName} 不存在`);
      return false;
    }

    // 2. 获取工具 schema
    const schema = await airis-schema({ tool: toolName });
    console.log(`✅ ${toolName} schema:`, schema.inputSchema.required);

    return true;
  } catch (error) {
    console.error(`❌ ${toolName} 测试失败:`, error.message);
    return false;
  }
}

// 测试所有 Serena 工具
const serenaTools = [
  "serena:write_memory",
  "serena:read_memory",
  "serena:list_memories",
  "serena:find_symbol"
];

for (const tool of serenaTools) {
  await testTool(tool);
}
```

---

## 📊 已知问题和限制

### 1. airis-find 查询不稳定 (严重)

**问题描述**:
- 带 query 参数的 airis-find 调用可能返回 0 结果
- 特别是查询 HOT 模式服务器（serena, memory）时

**影响范围**: 所有版本

**临时解决方案**: 使用空查询 + 手动过滤（见"问题 1"）

**长期修复**: 等待 AIRIS MCP Gateway 修复查询逻辑

### 2. HOT 模式服务器启动慢 (中等)

**问题描述**:
- HOT 模式服务器（如 Serena）首次启动需要 2-5 秒
- 期望是即时可用，但实际有延迟

**临时解决方案**:
- 工作流开始时预热服务器
- 使用重试机制

### 3. COLD 模式服务器超时 (低)

**问题描述**:
- Playwright 首次启动可能需要 8+ 秒
- 默认超时可能不够

**解决方案**: 增加超时时间或预启动

---

## 🚀 最佳实践

### 1. 防御性编程

```typescript
// ✅ 总是使用空查询
const allTools = await airis-find({ query: "" });
const targetTools = allTools.filter(t => t.name.includes("serena"));

// ❌ 不要依赖带参数的查询
// const tools = await airis-find({ query: "serena" });  // 可能失败
```

### 2. 完整的错误处理

```typescript
async function robustToolCall(tool: string, arguments: any) {
  try {
    // 1. 健康检查
    const health = await airis-exec({
      tool: "gateway-control:health"
    });

    if (!health.ok) {
      throw new Error("Gateway 不健康");
    }

    // 2. 验证参数
    const schema = await airis-schema({ tool });
    // ... 参数验证逻辑 ...

    // 3. 执行工具
    return await airis-exec({ tool, arguments });

  } catch (error) {
    console.error(`工具调用失败 (${tool}):`, error.message);

    // 4. 诊断信息
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });
    console.log("服务器状态:", servers);

    throw error;
  }
}
```

### 3. 预启动关键服务器

```typescript
// 在工作流开始时预启动
async function warmUpGateway() {
  console.log("🔥 预热 AIRIS MCP Gateway...");

  // 1. 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // 2. 预启动关键服务器
  const criticalServers = ["serena", "memory", "playwright"];

  for (const serverName of criticalServers) {
    await waitForServerReady(serverName, 30000);
  }

  console.log("✅ Gateway 预热完成");
}

// 在 main 函数开始时调用
await warmUpGateway();
```

---

## 📞 获取帮助

### 报告 Bug

如果遇到新问题，请收集以下信息：

1. **Gateway 版本**:
   ```bash
   curl http://localhost:9400/version
   ```

2. **服务器状态**:
   ```typescript
   await airis-exec({ tool: "gateway-control:list-servers" })
   ```

3. **错误日志**: 完整的错误消息和堆栈跟踪

4. **复现步骤**: 详细的操作步骤

5. **环境信息**: 操作系统、Node.js 版本、Docker 版本等

### 联系渠道

- **GitHub Issues**: https://github.com/airis-mcp-gateway/issues
- **文档更新**: 提交 PR 到 ai_workflow 仓库

---

**文档维护**: 根据实际使用经验持续更新
**最后验证日期**: 2025-12-30
**测试环境**: AIRIS MCP Gateway v2.0 + SuperClaude Framework
