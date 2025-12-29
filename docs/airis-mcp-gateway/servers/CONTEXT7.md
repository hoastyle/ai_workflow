# Context7 MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 Context7 MCP 服务器

---

## 概述

Context7 MCP 是一个官方库文档查询服务器，提供实时访问各种编程库和框架的最新文档。

**服务器信息**:
- **Runner**: npx (@context7/mcp-server)
- **Mode**: COLD（按需启动）
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 2 个工具

---

## 常见错误和修复

### 1. Library ID 未解析错误

#### 错误示例

```
Error: Invalid library ID format
或
Error: Library not found
```

#### 原因分析

Context7 需要特定格式的 Library ID（如 `/org/project` 或 `/org/project/version`）。直接使用库名称会失败。

#### 修复方法

**步骤 1: 解析库名称到 Library ID**

```typescript
// 必须先调用 resolve-library-id
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    libraryName: "react"
  }
})

// 返回示例: { libraryId: "/facebook/react" }
```

**步骤 2: 使用 Library ID 获取文档**

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/facebook/react",
    query: "useState hook"
  }
})
```

---

### 2. 查询结果为空

#### 错误示例

```json
{
  "results": [],
  "message": "No documentation found"
}
```

#### 原因分析

- 查询关键词过于模糊或拼写错误
- Library ID 不正确
- 库版本过旧或不支持

#### 修复方法

```typescript
// 1. 确认 Library ID 正确
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    libraryName: "react"
  }
})

// 2. 使用更具体的查询
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/facebook/react",
    query: "useState hook usage example"  // 更具体
  }
})
```

---

## Context7 MCP 工具参考

### resolve-library-id

**描述**: 将库名称解析为 Context7 兼容的 Library ID

**参数签名**:

```json
{
  "required": ["libraryName"],
  "properties": {
    "libraryName": {
      "type": "string",
      "description": "要搜索的库名称"
    }
  }
}
```

**使用示例**:

```typescript
// 解析 React
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    libraryName: "react"
  }
})
// 返回: { libraryId: "/facebook/react", ... }

// 解析 Vue
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    libraryName: "vue"
  }
})
// 返回: { libraryId: "/vuejs/vue", ... }

// 解析 Express
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    libraryName: "express"
  }
})
// 返回: { libraryId: "/expressjs/express", ... }
```

---

### get-library-docs

**描述**: 获取库的最新文档

**参数签名**:

```json
{
  "required": ["libraryId", "query"],
  "properties": {
    "libraryId": {
      "type": "string",
      "description": "Context7 兼容的 Library ID（从 resolve-library-id 获取）"
    },
    "query": {
      "type": "string",
      "description": "文档查询字符串"
    }
  }
}
```

**使用示例**:

```typescript
// React Hooks 文档
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/facebook/react",
    query: "useState hook"
  }
})

// Vue Composition API
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/vuejs/vue",
    query: "composition api ref reactive"
  }
})

// Express 路由
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/expressjs/express",
    query: "router middleware"
  }
})
```

---

## 最佳实践

### 1. 两步查询流程

**标准流程**:
```
Step 1: resolve-library-id → 获取 Library ID
Step 2: get-library-docs → 使用 Library ID 查询文档
```

**示例**:
```typescript
// Step 1: 解析库名称
const resolveResult = await mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: { libraryName: "react" }
})

// Step 2: 查询文档
const docs = await mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: resolveResult.libraryId,
    query: "useState hook"
  }
})
```

### 2. 查询优化

**具体查询**:
```typescript
// ✅ 好的查询
query: "useState hook usage example"
query: "express router middleware setup"
query: "vue composition api reactive ref"

// ❌ 模糊查询
query: "react"
query: "how to use"
query: "tutorial"
```

### 3. 支持的库

**常用库**:
- **React**: `/facebook/react`
- **Vue**: `/vuejs/vue`
- **Angular**: `/angular/angular`
- **Express**: `/expressjs/express`
- **Next.js**: `/vercel/next.js`
- **TypeScript**: `/microsoft/typescript`
- **Node.js**: `/nodejs/node`

**查询支持的库**:
```typescript
// 搜索库名称
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    libraryName: "your-library-name"
  }
})
```

---

## 常见问题 FAQ

### Q1: Context7 支持哪些编程语言？

**答**: 主要支持 JavaScript/TypeScript 生态系统的库和框架，包括：
- 前端框架（React, Vue, Angular）
- 后端框架（Express, Nest.js, Fastify）
- 工具库（Lodash, Axios, Moment.js）
- 构建工具（Webpack, Vite, Rollup）

### Q2: 如何查询特定版本的文档？

**答**: 在 Library ID 中指定版本：
```typescript
{
  libraryId: "/facebook/react/18.2.0",  // 特定版本
  query: "..."
}
```

### Q3: 查询结果包含什么信息？

**答**: 通常包括：
- 代码示例
- API 参考
- 使用说明
- 相关链接

### Q4: Context7 是否需要 API Key？

**答**: 不需要。Context7 是免费服务，无需配置 API Key。

### Q5: 如何处理多个匹配结果？

**答**: `resolve-library-id` 会返回最相关的匹配。如果有多个候选：
```typescript
// 返回示例
{
  "libraryId": "/facebook/react",
  "alternatives": [
    "/preactjs/preact",
    "/infernojs/inferno"
  ]
}
```

---

## 调试技巧

### 1. 验证 Library ID

```typescript
// 测试 Library ID 是否有效
mcp__airis-mcp-gateway__airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/facebook/react",
    query: "documentation"
  }
})
```

### 2. 查看服务器日志

```bash
# 查看 Context7 MCP 服务器日志
docker logs airis-mcp-gateway --tail 50 | grep context7

# 或查看 ProcessRunner 日志
docker logs airis-mcp-gateway 2>&1 | grep -A5 "context7"
```

### 3. 验证工具可用性

```typescript
// 列出所有 Context7 工具
mcp__airis-mcp-gateway__airis-find({
  query: "context7",
  server: "context7"
})
```

---

## 使用场景

### 场景 1: 学习新框架

```typescript
// 1. 解析框架名称
const { libraryId } = await airis-exec({
  tool: "context7:resolve-library-id",
  arguments: { libraryName: "vue" }
})

// 2. 查询入门文档
await airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId,
    query: "getting started tutorial"
  }
})
```

### 场景 2: 查找 API 用法

```typescript
// 查询特定 API
await airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/facebook/react",
    query: "useEffect cleanup function"
  }
})
```

### 场景 3: 解决错误

```typescript
// 查询错误相关文档
await airis-exec({
  tool: "context7:get-library-docs",
  arguments: {
    libraryId: "/expressjs/express",
    query: "error handling middleware"
  }
})
```

---

## 相关文档

- [AIRIS MCP Gateway README](../../README.md)
- [Context7 官方网站](https://context7.com)
- [MCP 使用注意事项索引](./README.md)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本，记录 2 个工具的完整参数签名和使用示例 |

---

**维护者**: 自动从使用经验中提炼
**反馈**: 如发现新的使用问题，请更新本文档
