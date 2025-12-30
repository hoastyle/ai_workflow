---
title: "AIRIS-Commands MCP 服务器"
description: "AIRIS MCP Gateway 配置管理和控制工具"
type: "系统集成"
status: "完成"
priority: "高"
created_date: "2025-12-31"
last_updated: "2025-12-31"
related_documents:
  - "docs/airis-mcp-gateway/README.md"
  - "docs/airis-mcp-gateway/BEST_PRACTICES.md"
related_code: []
---

# AIRIS-Commands MCP 服务器

**服务器名称**: airis-commands
**类型**: 内置服务器 (Gateway Control)
**模式**: HOT (常驻)

## 服务器概述

AIRIS-Commands 是 AIRIS MCP Gateway 的配置管理服务器，提供动态启用/禁用服务器、Profile 管理等高级功能。

## 核心工具

### 1. airis_config_get

获取当前 MCP 配置。

**参数**:
- `server_name` (可选): 指定服务器名

**示例**:
```typescript
await airis-exec({
  tool: "airis-commands:airis_config_get"
});
```

### 2. airis_config_set_enabled

启用或禁用服务器。

**参数**:
- `server_name` (必需): 服务器名
- `enabled` (必需): true/false

**示例**:
```typescript
await airis-exec({
  tool: "airis-commands:airis_config_set_enabled",
  arguments: {
    server_name: "playwright",
    enabled: true
  }
});
```

### 3. airis_profile_save

保存当前配置为 Profile。

**参数**:
- `profile_name` (必需): Profile 名称

### 4. airis_profile_load

加载已保存的 Profile。

**参数**:
- `profile_name` (必需): Profile 名称

### 5. airis_quick_enable

快速启用多个服务器。

**参数**:
- `server_names` (必需): 服务器名数组

### 6. airis_quick_disable_all

禁用所有服务器（最小配置）。

## 使用场景

- 动态调整服务器启用状态
- 创建不同工作场景的配置 Profile
- 快速切换开发/生产配置

## 最佳实践

1. 使用 Profile 管理不同场景配置
2. 禁用不需要的服务器以节省资源
3. 定期备份重要 Profile

---

**最后更新**: 2025-12-31
