---
title: "MindBase MCP 服务器 (Docker Gateway 专用)"
description: "知识图谱和向量搜索服务器，由 Docker Gateway 管理"
type: "系统集成"
status: "完成"
priority: "高"
created_date: "2025-12-31"
last_updated: "2025-12-31"
related_documents:
  - "docs/airis-mcp-gateway/README.md"
  - "docs/airis-mcp-gateway/PARAMETER_TRAPS.md"
related_code: []
---

# MindBase MCP 服务器

**服务器名称**: mindbase
**镜像**: ghcr.io/agiletec-inc/mindbase-mcp:latest
**管理方式**: Docker Gateway (非 ProcessManager)
**模式**: Docker 容器 (按需启动)
**依赖**: PostgreSQL + Ollama

⚠️ **重要**: MindBase 不在 AIRIS MCP Gateway 的 13 个 ProcessManager 管理的服务器中，而是由 **Docker Gateway** (airis-mcp-gateway-core) 专门管理。

---

## 架构说明

### 与 AIRIS MCP Gateway 的关系

```
Claude Code
    ↓
FastAPI (airis-mcp-gateway) - Port 9400
    ↓ (识别 mindbase: 前缀)
Dynamic MCP 路由层
    ↓ (代理到 Docker Gateway)
Docker Gateway (airis-mcp-gateway-core) - Port 9390
    ↓ (读取 airis-catalog.yaml)
启动 MindBase 容器
    ↓
MindBase MCP 服务器 (临时容器)
    - PostgreSQL 数据库
    - Ollama 向量引擎
```

### 关键配置

**mcp-config.json 中的状态**:
```json
{
  "mindbase": {
    "enabled": false,  // ProcessManager 中禁用
    "mode": "cold"
  }
}
```

**airis-catalog.yaml 中的定义**:
```yaml
mindbase:
  type: server  # Docker 容器类型
  image: ghcr.io/agiletec-inc/mindbase-mcp:latest
  env:
    - DATABASE_URL=postgresql://...
    - OLLAMA_URL=http://ollama:11434
```

**Docker Gateway 启动命令**:
```bash
/docker-mcp gateway run --servers=time,mindbase
```

---

## 核心功能

1. **语义记忆管理** - 存储和检索结构化知识
2. **向量搜索** - 基于语义相似度的搜索
3. **知识图谱** - 实体关系管理
4. **记忆持久化** - PostgreSQL 存储

---

## 常用工具 (~7-8 个)

### 1. store_memory

存储语义记忆。

**参数**:
- `content` (必需): 记忆内容
- `metadata` (可选): 元数据

### 2. search_memories

搜索相似记忆。

**参数**:
- `query` (必需): 搜索查询
- `limit` (可选): 返回数量

### 3. list_memories

列出所有记忆。

**参数**: 无

### 4. delete_memory

删除指定记忆。

**参数**:
- `memory_id` (必需): 记忆ID

---

## 实际调用日志证据

```
[Dynamic MCP] airis-exec: mindbase:memory_write -> server=mindbase, tool=memory_write
[Dynamic MCP] Proxying airis-exec to Docker Gateway: memory_write
[Dynamic MCP] airis-exec: mindbase:memory_search -> server=mindbase, tool=memory_search
```

**结论**: MindBase 工具完整可用，通过 Dynamic MCP 路由到 Docker Gateway。

---

## 与 Memory MCP 的区别

| 特性 | MindBase (Docker Gateway) | Memory (ProcessManager) |
|------|---------------------------|-------------------------|
| 管理方式 | Docker Gateway | ProcessManager (HOT 模式) |
| 存储后端 | PostgreSQL + Ollama | 内存 |
| 向量搜索 | ✅ 支持 | ❌ 不支持 |
| 持久化 | ✅ 数据库 | ❌ 进程内存 |
| 适用场景 | 长期知识管理 | 临时会话记忆 |

---

## 使用建议

1. **长期知识存储** - 使用 MindBase
2. **临时会话记忆** - 使用 Memory (HOT 模式，更快)
3. **向量搜索需求** - 必须使用 MindBase
4. **跨会话持久化** - 使用 MindBase

---

## 启动验证

```bash
# 检查 Docker Gateway 容器
docker ps | grep airis-mcp-gateway-core

# 检查 MindBase 是否在 Docker Gateway 管理下
docker exec airis-mcp-gateway-core cat /catalogs/airis-catalog.yaml | grep mindbase
```

---

**最后更新**: 2025-12-31
**注意**: MindBase 不在 AIRIS MCP Gateway 的 13 个服务器列表中，而是 Docker Gateway 的专用服务器。
