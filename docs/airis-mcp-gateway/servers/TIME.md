---
title: "Time MCP 服务器 (Docker Gateway 内置)"
description: "时间和时区管理服务器，由 Docker Gateway 原生支持"
type: "系统集成"
status: "完成"
priority: "中"
created_date: "2025-12-31"
last_updated: "2025-12-31"
related_documents:
  - "docs/airis-mcp-gateway/README.md"
  - "docs/airis-mcp-gateway/PARAMETER_TRAPS.md"
related_code: []
---

# Time MCP 服务器

**服务器名称**: time
**类型**: Docker Gateway 内置服务器
**管理方式**: Docker Gateway (非 ProcessManager)
**模式**: 原生支持

⚠️ **重要**: Time 不在 AIRIS MCP Gateway 的 13 个 ProcessManager 管理的服务器中，而是由 **Docker Gateway** 原生支持。

---

## 架构说明

### 与 AIRIS MCP Gateway 的关系

```
Claude Code
    ↓
FastAPI (airis-mcp-gateway) - Port 9400
    ↓ (识别 time: 前缀)
Dynamic MCP 路由层
    ↓ (代理到 Docker Gateway)
Docker Gateway (airis-mcp-gateway-core) - Port 9390
    ↓ (内置支持)
Time 工具 (原生)
```

### 关键配置

**mcp-config.json 中的状态**:
```json
{
  "time": {
    "enabled": false,  // ProcessManager 中禁用
    "mode": "cold"
  }
}
```

**Docker Gateway 启动命令**:
```bash
/docker-mcp gateway run --servers=time,mindbase
```

---

## 核心功能

1. **时区转换** - 获取不同时区的当前时间
2. **时区列表** - 查询可用时区
3. **格式化时间** - 自定义时间格式输出

---

## 常用工具 (~7-8 个)

### 1. get_current_time

获取指定时区的当前时间。

**参数**:
```json
{
  "timezone": "string"  // IANA 时区名（必需）
}
```

**示例**:
```typescript
await airis-exec({
  tool: "time:get_current_time",
  arguments: {
    timezone: "America/New_York"
  }
});
```

**重要**: 如果用户未提供时区，使用 `UTC` 作为默认值。

---

### 2. get_timezones

获取所有可用时区列表。

**参数**: 无

**返回**:
```json
{
  "timezones": [
    "America/New_York",
    "Europe/London",
    "Asia/Shanghai",
    ...
  ]
}
```

---

### 3. convert_time

转换时间到不同时区。

**参数**:
- `from_timezone` (必需): 源时区
- `to_timezone` (必需): 目标时区
- `time` (可选): 时间字符串（默认当前时间）

---

## 常见时区示例

| 时区 | IANA 名称 | 说明 |
|------|----------|------|
| 东部时间 | America/New_York | 美国东部 (ET) |
| 太平洋时间 | America/Los_Angeles | 美国西部 (PT) |
| 伦敦 | Europe/London | 英国 (GMT/BST) |
| 巴黎 | Europe/Paris | 中欧 (CET/CEST) |
| 上海 | Asia/Shanghai | 中国 (CST) |
| 东京 | Asia/Tokyo | 日本 (JST) |
| UTC | UTC | 协调世界时 |

---

## 常见错误

### 错误: 时区名称无效

```
Error: Invalid timezone: 'EST'
```

**修复**:
```typescript
// ❌ 错误 - 使用缩写
timezone: "EST"

// ✅ 正确 - 使用 IANA 名称
timezone: "America/New_York"
```

---

## 使用场景

- 多时区团队协作
- 全球事件日程安排
- 日志时间戳规范化
- 用户本地时间显示

---

## 启动验证

```bash
# 检查 Docker Gateway 容器
docker ps | grep airis-mcp-gateway-core

# 验证 time 服务器启用
docker logs airis-mcp-gateway-core | grep "time"
```

---

**最后更新**: 2025-12-31
**注意**: Time 不在 AIRIS MCP Gateway 的 13 个服务器列表中，而是 Docker Gateway 的内置服务器。
