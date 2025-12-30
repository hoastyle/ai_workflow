---
title: "Memory MCP 服务器"
description: "知识管理和实体记忆存储工具"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-29"
last_updated: "2025-12-31"
related_documents:
  - path: "../PARAMETER_TRAPS.md"
    type: "参考"
    description: "Memory 参数陷阱（observations 数组）"
  - path: "../QUICK_REFERENCE.md"
    type: "参考"
    description: "快速参考指南"
  - path: "MINDBASE.md"
    type: "对比"
    description: "MindBase vs Memory 对比说明"
related_code: []
tags: ["memory", "knowledge-graph", "hot-mode", "entity-storage"]
---

# Memory MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 Memory MCP 服务器

---

## 概述

Memory MCP 是一个知识图谱管理服务器,提供实体、关系和观察的创建、查询和管理功能。它允许构建和维护结构化的知识网络。

**服务器信息**:
- **Runner**: npx (@modelcontextprotocol/server-memory)
- **Mode**: COLD (按需启动)
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 9 个工具
- **数据存储**: /app/data/memory.json

---

## 常见错误和修复

### 1. 实体名称冲突错误

#### 错误示例

```
Error: Entity with name "User" already exists
```

#### 原因分析

尝试创建已存在的实体,Memory MCP 不允许重复实体名称。

#### 修复方法

**方法 1**: 先搜索检查实体是否存在
```typescript
// 1. 先搜索
await airis-exec(tool: "memory:search_nodes", arguments: {
  query: "User"
})

// 2. 如果存在,使用 add_observations 添加新信息
await airis-exec(tool: "memory:add_observations", arguments: {
  entityName: "User",
  observations: ["新的观察信息"]
})
```

**方法 2**: 使用唯一的实体名称
```typescript
await airis-exec(tool: "memory:create_entities", arguments: {
  entities: [{
    name: "User-John-Doe",  // 使用更具体的名称
    entityType: "person",
    observations: ["Software engineer", "Lives in NYC"]
  }]
})
```

---

### 2. 关系类型不明确错误

#### 错误示例

```
Relation type "related_to" is too vague
```

#### 原因分析

关系类型应该使用主动语态,清晰描述实体间的关系。

#### 修复方法

**❌ 错误做法**:
```typescript
{
  from: "User",
  to: "Project",
  relationType: "related_to"  // 太模糊
}
```

**✅ 正确做法**:
```typescript
{
  from: "User",
  to: "Project",
  relationType: "works_on"  // 主动语态,清晰
}
```

**推荐的关系类型**:
- `works_on`, `manages`, `owns`
- `depends_on`, `uses`, `implements`
- `is_parent_of`, `is_child_of`
- `communicates_with`, `integrates_with`

---

### 3. 观察内容为空错误

#### 错误示例

```
Error: observations array cannot be empty
```

#### 原因分析

创建实体时必须提供至少一个观察(observation)。

#### 修复方法

```typescript
// ❌ 错误
{
  name: "NewUser",
  entityType: "person",
  observations: []  // 空数组
}

// ✅ 正确
{
  name: "NewUser",
  entityType: "person",
  observations: ["Created on 2025-12-29"]  // 至少一个观察
}
```

---

## 工具参考

### 1. create_entities

**描述**: 在知识图谱中创建多个新实体

**参数签名**:
```typescript
{
  entities: Array<{
    name: string;           // 实体名称(唯一)
    entityType: string;     // 实体类型
    observations: string[]; // 观察数组(至少一个)
  }>
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:create_entities", arguments: {
  entities: [
    {
      name: "AIRIS MCP Gateway",
      entityType: "project",
      observations: [
        "FastAPI-based MCP multiplexer",
        "Supports 60+ AI tools",
        "Dynamic MCP mode enabled"
      ]
    },
    {
      name: "Docker Gateway",
      entityType: "component",
      observations: [
        "Runs on port 9390",
        "Handles MCP routing"
      ]
    }
  ]
})
```

---

### 2. create_relations

**描述**: 在实体间创建关系,使用主动语态

**参数签名**:
```typescript
{
  relations: Array<{
    from: string;         // 起始实体名称
    to: string;           // 目标实体名称
    relationType: string; // 关系类型(主动语态)
  }>
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:create_relations", arguments: {
  relations: [
    {
      from: "AIRIS MCP Gateway",
      to: "Docker Gateway",
      relationType: "uses"
    },
    {
      from: "User",
      to: "AIRIS MCP Gateway",
      relationType: "develops"
    }
  ]
})
```

---

### 3. add_observations

**描述**: 向现有实体添加新的观察

**参数签名**:
```typescript
{
  entityName: string;     // 实体名称
  observations: string[]; // 新观察数组
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:add_observations", arguments: {
  entityName: "AIRIS MCP Gateway",
  observations: [
    "Added MindBase integration",
    "Verified 10 MCP servers"
  ]
})
```

---

### 4. read_graph

**描述**: 读取整个知识图谱

**参数签名**:
```typescript
{}  // 无参数
```

**使用示例**:
```typescript
const graph = await airis-exec(tool: "memory:read_graph", arguments: {})

// 返回结构:
// {
//   entities: [...],
//   relations: [...]
// }
```

---

### 5. search_nodes

**描述**: 基于查询搜索知识图谱节点

**参数签名**:
```typescript
{
  query: string;  // 搜索查询(匹配名称、类型、观察内容)
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:search_nodes", arguments: {
  query: "MCP"
})

// 返回匹配 "MCP" 的所有实体
```

---

### 6. open_nodes

**描述**: 通过名称打开特定节点

**参数签名**:
```typescript
{
  names: string[];  // 实体名称数组
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:open_nodes", arguments: {
  names: ["AIRIS MCP Gateway", "Docker Gateway"]
})
```

---

### 7. delete_entities

**描述**: 删除多个实体及其关联关系

**参数签名**:
```typescript
{
  entityNames: string[];  // 要删除的实体名称数组
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:delete_entities", arguments: {
  entityNames: ["OldEntity", "DeprecatedComponent"]
})
```

**⚠️ 警告**: 删除实体会同时删除所有相关的关系。

---

### 8. delete_observations

**描述**: 从实体中删除特定观察

**参数签名**:
```typescript
{
  entityName: string;     // 实体名称
  observations: string[]; // 要删除的观察数组
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:delete_observations", arguments: {
  entityName: "AIRIS MCP Gateway",
  observations: ["Outdated observation"]
})
```

---

### 9. delete_relations

**描述**: 删除多个关系

**参数签名**:
```typescript
{
  relations: Array<{
    from: string;
    to: string;
    relationType: string;
  }>
}
```

**使用示例**:
```typescript
await airis-exec(tool: "memory:delete_relations", arguments: {
  relations: [
    {
      from: "OldService",
      to: "Database",
      relationType: "uses"
    }
  ]
})
```

---

## 使用示例

### 场景 1: 构建项目知识图谱

```typescript
// Step 1: 创建核心实体
await airis-exec(tool: "memory:create_entities", arguments: {
  entities: [
    {
      name: "AIRIS MCP Gateway",
      entityType: "project",
      observations: [
        "Main API on port 9400",
        "Hybrid MCP multiplexer"
      ]
    },
    {
      name: "FastAPI",
      entityType: "framework",
      observations: [
        "Python web framework",
        "Used for API server"
      ]
    },
    {
      name: "Docker",
      entityType: "technology",
      observations: [
        "Container platform",
        "Used for deployment"
      ]
    }
  ]
})

// Step 2: 建立关系
await airis-exec(tool: "memory:create_relations", arguments: {
  relations: [
    {
      from: "AIRIS MCP Gateway",
      to: "FastAPI",
      relationType: "uses"
    },
    {
      from: "AIRIS MCP Gateway",
      to: "Docker",
      relationType: "deployed_on"
    }
  ]
})

// Step 3: 查询验证
const result = await airis-exec(tool: "memory:search_nodes", arguments: {
  query: "AIRIS"
})
```

---

### 场景 2: 更新实体信息

```typescript
// 添加新的观察
await airis-exec(tool: "memory:add_observations", arguments: {
  entityName: "AIRIS MCP Gateway",
  observations: [
    "Added Memory MCP documentation",
    "Total 13 MCP servers documented"
  ]
})

// 读取完整图谱检查
const graph = await airis-exec(tool: "memory:read_graph", arguments: {})
```

---

### 场景 3: 清理过期数据

```typescript
// 删除过期观察
await airis-exec(tool: "memory:delete_observations", arguments: {
  entityName: "OldProject",
  observations: ["Deprecated feature"]
})

// 删除整个实体
await airis-exec(tool: "memory:delete_entities", arguments: {
  entityNames: ["DeprecatedService"]
})
```

---

## 最佳实践

### 1. 实体命名规范

**推荐**:
- 使用清晰、唯一的名称
- 包含上下文信息: `"User-John"` 而非 `"User"`
- 使用 PascalCase 或 kebab-case

**示例**:
```typescript
// ✅ 好的命名
"AIRIS-MCP-Gateway"
"Docker-Gateway-9390"
"User-Authentication-Service"

// ❌ 不好的命名
"gateway"  // 太模糊
"service1" // 无意义
```

---

### 2. 关系类型选择

**原则**: 使用主动语态,清晰描述动作

**示例**:
```typescript
// ✅ 主动、清晰
"uses", "manages", "depends_on", "communicates_with"

// ❌ 被动、模糊
"is_used_by", "related_to", "connected_to"
```

---

### 3. 观察内容组织

**推荐结构**:
- 每个观察一个明确的事实
- 包含时间信息(如果相关)
- 避免冗长的描述

**示例**:
```typescript
// ✅ 清晰、简洁
observations: [
  "Created on 2025-12-29",
  "Handles MCP routing",
  "Supports 60+ tools"
]

// ❌ 冗长、模糊
observations: [
  "This is a gateway that was created recently and it handles various things"
]
```

---

### 4. 定期维护

**建议**:
- 定期运行 `read_graph` 审查知识图谱
- 删除过期的实体和关系
- 更新观察内容保持最新

---

## FAQ

### Q1: Memory MCP 和 Serena MCP 的 memory 有什么区别?

**答**:
- **Memory MCP**: 知识图谱,用于构建实体-关系网络
- **Serena MCP**: 项目记忆,用于存储项目相关的文本信息

**使用场景**:
- Memory MCP: 适合结构化知识(如项目架构、组件依赖)
- Serena MCP: 适合非结构化记忆(如会话总结、工作进展)

---

### Q2: 如何查看知识图谱的结构?

**答**: 使用 `read_graph` 工具:

```typescript
const graph = await airis-exec(tool: "memory:read_graph", arguments: {})

// 返回:
// {
//   entities: [{ name, entityType, observations }, ...],
//   relations: [{ from, to, relationType }, ...]
// }
```

---

### Q3: 可以创建循环关系吗?

**答**: 可以,Memory MCP 支持有向图,包括循环关系:

```typescript
{
  relations: [
    { from: "ServiceA", to: "ServiceB", relationType: "calls" },
    { from: "ServiceB", to: "ServiceA", relationType: "responds_to" }
  ]
}
```

---

### Q4: 数据存储在哪里?

**答**: 存储在容器内的 `/app/data/memory.json` 文件中。

**注意**:
- 容器重启数据会丢失(除非挂载 volume)
- 建议定期导出重要知识图谱

---

### Q5: 如何备份知识图谱?

**答**:

```typescript
// 1. 读取完整图谱
const graph = await airis-exec(tool: "memory:read_graph", arguments: {})

// 2. 保存到文件(使用其他工具)
// 或复制 JSON 输出到安全位置
```

---

## 调试技巧

### 1. 实体创建失败

**检查清单**:
- [ ] 实体名称是否唯一? (使用 `search_nodes` 检查)
- [ ] `observations` 数组是否为空?
- [ ] `entityType` 是否有意义?

**调试命令**:
```bash
# 搜索冲突实体
airis-exec tool="memory:search_nodes" arguments='{"query":"实体名称"}'
```

---

### 2. 关系创建失败

**检查清单**:
- [ ] `from` 和 `to` 实体是否存在?
- [ ] `relationType` 是否使用主动语态?

**调试流程**:
```typescript
// 1. 验证实体存在
await airis-exec(tool: "memory:open_nodes", arguments: {
  names: ["EntityA", "EntityB"]
})

// 2. 创建关系
await airis-exec(tool: "memory:create_relations", arguments: {
  relations: [{ from: "EntityA", to: "EntityB", relationType: "uses" }]
})
```

---

### 3. 搜索无结果

**可能原因**:
- 查询关键词不匹配
- 实体尚未创建
- 大小写不匹配

**解决方法**:
```typescript
// 使用更宽泛的查询
await airis-exec(tool: "memory:search_nodes", arguments: {
  query: "MCP"  // 而非 "AIRIS MCP Gateway"
})

// 或读取完整图谱
await airis-exec(tool: "memory:read_graph", arguments: {})
```

---

## 相关文档

- **主文档**: [README.md](../../README.md)
- **MCP 索引**: [docs/mcp-usage-notes/README.md](README.md)
- **Serena MCP**: [SERENA_MCP_USAGE_NOTES.md](SERENA_MCP_USAGE_NOTES.md) (项目记忆)
- **AIRIS Agent MCP**: [AIRIS_AGENT_MCP_USAGE_NOTES.md](AIRIS_AGENT_MCP_USAGE_NOTES.md) (包含 airis_record 工具)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本,包含 9 个工具的完整文档 |

---

**文档状态**: ✅ 已验证
**测试覆盖**: 9/9 工具已通过 `airis-schema` 验证
**最后审查**: 2025-12-29
