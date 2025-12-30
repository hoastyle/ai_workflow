---
title: "Sequential-Thinking MCP 服务器"
description: "结构化多步推理和思考过程管理工具"
type: "系统集成"
status: "完成"
priority: "中"
created_date: "2025-12-31"
last_updated: "2025-12-31"
related_documents:
  - "docs/airis-mcp-gateway/README.md"
  - "docs/airis-mcp-gateway/PARAMETER_TRAPS.md"
  - "docs/airis-mcp-gateway/TROUBLESHOOTING.md"
related_code: []
---

# Sequential-Thinking MCP 服务器

**服务器名称**: sequential-thinking
**包**: @modelcontextprotocol/server-sequential-thinking
**模式**: COLD (按需启动)
**启动方式**: npx -y @modelcontextprotocol/server-sequential-thinking

---

## 服务器概述

Sequential-thinking 是一个专门用于结构化多步推理的 MCP 服务器，提供思考过程管理、步骤记录和推理链追踪功能。适用于需要系统化分析、多步骤决策和复杂问题解决的场景。

### 核心功能

1. **思考会话管理** - 创建和管理结构化思考过程
2. **步骤追踪** - 记录每个推理步骤和中间结论
3. **推理链分析** - 分析思考链路，识别逻辑跳跃
4. **结论汇总** - 提取关键结论和决策点

---

## 工具列表

### 1. create_thinking_session

**用途**: 创建新的思考会话

**参数**:
```json
{
  "topic": "string",              // 思考主题（必需）
  "initial_thoughts": "string[]"  // 初始想法列表（可选）
}
```

**示例**:
```typescript
await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: {
    topic: "优化数据库查询性能",
    initial_thoughts: [
      "需要分析当前查询瓶颈",
      "考虑索引优化",
      "评估缓存策略"
    ]
  }
});
```

---

### 2. add_thinking_step

**用途**: 向思考会话添加新步骤

**参数**:
```json
{
  "session_id": "string",   // 会话ID（必需）
  "step": "string",         // 推理步骤内容（必需）
  "conclusion": "string"    // 步骤结论（可选）
}
```

**示例**:
```typescript
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: "session-123",
    step: "分析慢查询日志，发现 user_orders 表查询占 60% 时间",
    conclusion: "user_orders 表是主要瓶颈"
  }
});
```

---

### 3. get_thinking_chain

**用途**: 获取完整的思考链路

**参数**:
```json
{
  "session_id": "string"   // 会话ID（必需）
}
```

**返回**:
```json
{
  "topic": "优化数据库查询性能",
  "steps": [
    {
      "step_number": 1,
      "content": "分析慢查询日志...",
      "conclusion": "user_orders 表是主要瓶颈"
    },
    ...
  ]
}
```

---

### 4. analyze_thinking

**用途**: 分析思考链路，识别逻辑问题

**参数**:
```json
{
  "session_id": "string"   // 会话ID（必需）
}
```

**返回**:
```json
{
  "logic_gaps": [...],       // 逻辑跳跃
  "missing_steps": [...],    // 缺失步骤
  "recommendations": [...]   // 改进建议
}
```

---

## 常见错误和修复方法

### 错误 1: 会话ID不存在

**错误信息**:
```
Error: Session 'session-123' not found
```

**原因**: 引用了不存在的思考会话

**修复方法**:
```typescript
// 1. 先创建会话
const session = await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: { topic: "your-topic" }
});

// 2. 使用返回的 session_id
const sessionId = session.result.session_id;

// 3. 添加步骤时使用正确的 session_id
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: sessionId,
    step: "..."
  }
});
```

---

### 错误 2: 缺少必需参数

**错误信息**:
```
Error: 1 validation error for applyArguments
topic
  Field required [type=missing]
```

**原因**: 创建会话时未提供 topic 参数

**修复方法**:
```typescript
// ❌ 错误
await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: {}
});

// ✅ 正确
await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: {
    topic: "明确的思考主题"
  }
});
```

---

### 错误 3: 思考步骤为空

**错误信息**:
```
Error: Step content cannot be empty
```

**原因**: 添加步骤时 step 参数为空字符串

**修复方法**:
```typescript
// ❌ 错误
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: "session-123",
    step: ""  // 空字符串
  }
});

// ✅ 正确
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: "session-123",
    step: "具体的推理步骤内容"
  }
});
```

---

## 最佳实践

### 1. 系统化分析流程

```typescript
// Step 1: 创建思考会话
const session = await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: {
    topic: "API 性能优化方案",
    initial_thoughts: [
      "识别性能瓶颈",
      "分析根本原因",
      "提出优化方案",
      "评估实施风险"
    ]
  }
});

// Step 2: 逐步添加推理过程
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: session.result.session_id,
    step: "使用 APM 工具分析，发现数据库查询占 70% 响应时间",
    conclusion: "数据库查询是主要瓶颈"
  }
});

// Step 3: 分析思考链路
const analysis = await airis-exec({
  tool: "sequential-thinking:analyze_thinking",
  arguments: {
    session_id: session.result.session_id
  }
});

// Step 4: 获取完整推理链
const chain = await airis-exec({
  tool: "sequential-thinking:get_thinking_chain",
  arguments: {
    session_id: session.result.session_id
  }
});
```

---

### 2. 复杂决策辅助

**适用场景**: 技术选型、架构设计、问题诊断

```typescript
// 创建决策会话
const decision = await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: {
    topic: "数据库选型：PostgreSQL vs MongoDB",
    initial_thoughts: [
      "分析数据模型特点",
      "评估查询模式",
      "考虑扩展性需求",
      "对比运维成本"
    ]
  }
});

// 逐步分析每个维度
// ... 添加多个推理步骤 ...

// 分析决策链路完整性
const analysis = await airis-exec({
  tool: "sequential-thinking:analyze_thinking",
  arguments: { session_id: decision.result.session_id }
});

// 检查是否有逻辑跳跃
if (analysis.result.logic_gaps.length > 0) {
  console.log("发现逻辑跳跃:", analysis.result.logic_gaps);
  // 补充缺失的推理步骤
}
```

---

### 3. 问题诊断记录

**适用场景**: Bug 排查、系统故障分析

```typescript
// 创建诊断会话
const diagnosis = await airis-exec({
  tool: "sequential-thinking:create_thinking_session",
  arguments: {
    topic: "生产环境 API 响应慢问题诊断",
    initial_thoughts: [
      "收集日志和监控数据",
      "识别异常模式",
      "定位根本原因",
      "验证假设"
    ]
  }
});

// 记录诊断过程
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: diagnosis.result.session_id,
    step: "检查 APM，发现 12:00-13:00 响应时间飙升至 2s",
    conclusion: "问题集中在午高峰时段"
  }
});

await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: diagnosis.result.session_id,
    step: "分析数据库慢查询日志，发现 user_search 查询占 80%",
    conclusion: "user_search 查询是根本原因"
  }
});

// 获取完整诊断记录
const record = await airis-exec({
  tool: "sequential-thinking:get_thinking_chain",
  arguments: { session_id: diagnosis.result.session_id }
});
```

---

## 使用场景

| 场景 | 工具组合 | 说明 |
|------|---------|------|
| **技术调研** | create_session → add_step (多次) → analyze | 系统化记录调研过程和结论 |
| **架构设计** | create_session → add_step → get_chain | 追踪设计决策链路 |
| **问题诊断** | create_session → add_step → analyze | 记录诊断步骤，避免遗漏 |
| **代码审查** | create_session → add_step → get_chain | 记录审查发现和改进建议 |
| **性能优化** | create_session → add_step → analyze | 系统化分析优化路径 |

---

## 与其他 MCP 服务器的配合

### 与 Serena 配合

```typescript
// 1. 使用 Serena 搜索代码
const codeSearch = await airis-exec({
  tool: "serena:semantic_search",
  arguments: { query: "数据库连接池配置" }
});

// 2. 记录分析过程
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: sessionId,
    step: `代码搜索发现 ${codeSearch.result.files.length} 个相关文件`,
    conclusion: "连接池配置分散在多个文件中"
  }
});
```

---

### 与 Tavily 配合

```typescript
// 1. 使用 Tavily 搜索最佳实践
const webSearch = await airis-exec({
  tool: "tavily:search",
  arguments: { query: "PostgreSQL connection pooling best practices" }
});

// 2. 记录调研发现
await airis-exec({
  tool: "sequential-thinking:add_thinking_step",
  arguments: {
    session_id: sessionId,
    step: `调研发现: ${webSearch.result.summary}`,
    conclusion: "业界推荐连接池大小为 CPU 核心数 * 2"
  }
});
```

---

## 参数速查

| 工具 | 必需参数 | 可选参数 |
|------|---------|---------|
| create_thinking_session | `topic` | `initial_thoughts` |
| add_thinking_step | `session_id`, `step` | `conclusion` |
| get_thinking_chain | `session_id` | - |
| analyze_thinking | `session_id` | - |

---

## 注意事项

1. **会话生命周期**: 思考会话在服务器重启后会丢失，重要内容应保存到 Serena memory
2. **步骤粒度**: 每个步骤应包含明确的推理内容和结论，避免过于简略
3. **逻辑连贯性**: 定期使用 `analyze_thinking` 检查推理链路完整性
4. **并发限制**: COLD 模式首次调用需要 2-5 秒启动时间

---

**最后更新**: 2025-12-31
**版本**: v1.0
**维护状态**: 活跃
