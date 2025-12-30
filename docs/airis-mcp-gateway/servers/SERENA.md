---
title: "Serena MCP 服务器"
description: "语义代码理解和项目内存管理工具"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-29"
last_updated: "2025-12-31"
related_documents:
  - path: "../PARAMETER_TRAPS.md"
    type: "参考"
    description: "Serena 参数陷阱和最佳实践"
  - path: "../QUICK_REFERENCE.md"
    type: "参考"
    description: "快速参考指南"
related_code: []
tags: ["serena", "code-understanding", "memory", "hot-mode"]
---

# Serena MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-31
**适用范围**: AIRIS MCP Gateway 中的 Serena MCP 服务器

---

## 概述

Serena MCP 是一个语义代码理解和项目内存管理服务器，提供代码检索、编辑和会话记忆功能。

**服务器信息**:
- **Runner**: mcp-remote
- **Mode**: COLD（按需启动）
- **端口**: 通过 AIRIS MCP Gateway 代理

---

## 常见错误和修复

### 1. 参数名称不匹配错误

#### 错误示例

```
Error: Error executing tool write_memory: 1 validation error for applyArguments
memory_file_name
  Field required [type=missing, input_value={'filename': 'lcps_blackb...
```

#### 原因分析

Serena MCP 的工具参数名称与常见工具不同：
- ❌ 错误参数名: `filename`
- ✅ 正确参数名: `memory_file_name`

#### 修复方法

**步骤 1: 查询工具签名**

使用 `airis-schema` 查询正确的参数名：

```typescript
// Claude Code 中执行
mcp__airis-mcp-gateway__airis-schema({
  tool: "serena:write_memory"
})
```

**步骤 2: 使用正确的参数**

```typescript
// ❌ 错误调用
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:write_memory",
  arguments: {
    filename: "my_memory.md",  // 错误的参数名
    content: "..."
  }
})

// ✅ 正确调用
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "my_memory.md",  // 正确的参数名
    content: "..."
  }
})
```

---

## Serena MCP 工具参考

### write_memory

**描述**: 将项目相关信息写入内存文件（Markdown 格式）

**参数签名**:

```json
{
  "properties": {
    "memory_file_name": {
      "title": "Memory File Name",
      "type": "string"
    },
    "content": {
      "title": "Content",
      "type": "string"
    },
    "max_answer_chars": {
      "default": -1,
      "title": "Max Answer Chars",
      "type": "integer"
    }
  },
  "required": [
    "memory_file_name",
    "content"
  ]
}
```

**使用示例**:

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "session_summary_20251229.md",
    content: "# 会话摘要\n\n本次会话完成了...",
    max_answer_chars: -1  // 可选，默认无限制
  }
})
```

### read_memory

**描述**: 读取已保存的内存文件

**参数签名**:

```json
{
  "properties": {
    "memory_file_name": {
      "title": "Memory File Name",
      "type": "string"
    }
  },
  "required": [
    "memory_file_name"
  ]
}
```

**使用示例**:

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:read_memory",
  arguments: {
    memory_file_name: "session_summary_20251229.md"
  }
})
```

---

## 最佳实践

### 1. 文件命名规范

**推荐格式**: `{主题}_{日期}.md`

```
✅ 推荐:
- lcps_blackbox_evaluation_20251229.md
- security_analysis_20251229.md
- session_summary_20251229.md

❌ 不推荐:
- memo.md (太模糊)
- 2025-12-29.md (缺少主题)
- blackbox-eval.md (缺少日期)
```

### 2. 内容结构建议

```markdown
# [主题标题]

**会话日期**: YYYY-MM-DD
**范围**: [简短描述]
**方法**: [使用的方法或工具]

---

## 核心发现摘要

### 1. [发现点 1]
- 详细说明...

### 2. [发现点 2]
- 详细说明...

---

## 关键技术洞察

[技术细节和深度分析]

---

## 待办事项

### P0 - 必须立即修复
1. [ ] 任务 1
2. [ ] 任务 2

### P1 - 短期关键改进
3. [ ] 任务 3

---

## 下次会话重点

1. **如果继续 X 工作**:
   - 步骤 1
   - 步骤 2

2. **如果转向 Y**:
   - 步骤 1

---

## 参考文档

- `/path/to/doc1.md`
- `/path/to/doc2.md`

---

**会话成果**:
- 成果 1
- 成果 2
```

### 3. 查询工具前先搜索

```bash
# 第一步：搜索相关工具
airis-find(query: "memory")

# 第二步：查看工具签名
airis-schema(tool: "serena:write_memory")

# 第三步：执行工具
airis-exec(tool: "serena:write_memory", arguments: {...})
```

---

## 常见问题 FAQ

### Q1: 内存文件保存在哪里？

**答**: 默认保存在项目的 `.serena/memories/` 目录下。

```bash
# 查看已保存的内存文件
ls -la .serena/memories/
```

### Q2: 如何列出所有可用的 Serena 工具？

**答**: 使用 `airis-find` 搜索：

```typescript
mcp__airis-mcp-gateway__airis-find({
  query: "serena",
  server: "serena"  // 可选，过滤到特定服务器
})
```

### Q3: 参数名称不确定时怎么办？

**答**: 永远先查询工具签名：

```typescript
mcp__airis-mcp-gateway__airis-schema({
  tool: "serena:tool_name"
})
```

### Q4: 如何删除或更新已保存的内存？

**答**:
- **更新**: 再次调用 `write_memory` 使用相同的 `memory_file_name`（会覆盖）
- **删除**: 直接删除文件系统中的文件

```bash
# 删除内存文件
rm .serena/memories/old_memory.md
```

### Q5: 内存文件大小有限制吗？

**答**: 理论上没有硬性限制，但建议：
- 单个文件 < 100KB（可读性）
- 使用 `max_answer_chars` 参数控制返回内容大小

---

## 调试技巧

### 1. 启用详细日志

```bash
# 在 airis-mcp-gateway 中启用调试模式
export LOG_LEVEL=DEBUG
docker compose up -d
```

### 2. 检查 Serena MCP 服务器状态

```bash
# 查看服务器日志
docker compose logs serena

# 检查服务器是否启动
docker compose ps
```

### 3. 验证参数格式

使用 `airis-schema` 获取完整的 JSON Schema，确保参数类型正确：

```json
{
  "memory_file_name": "string",  // ✅ 正确
  "memory_file_name": 12345,     // ❌ 错误（应为字符串）
  "content": "string",           // ✅ 正确
  "content": ["array"],          // ❌ 错误（应为字符串）
}
```

---

## 相关文档

- [AIRIS MCP Gateway README](../../README.md)
- [Intent Routing 文档](../intent-routing.md)
- [迁移指南](../MIGRATION.md)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本，记录 `write_memory` 参数名称问题 |

---

**维护者**: 自动从使用经验中提炼
**反馈**: 如发现新的使用问题，请更新本文档
