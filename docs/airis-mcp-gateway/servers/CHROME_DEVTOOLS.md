---
title: "Chrome-DevTools MCP 服务器"
description: "Chrome 浏览器调试和自动化工具"
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

# Chrome-DevTools MCP 服务器

**服务器名称**: chrome-devtools
**包**: chrome-devtools-mcp@latest
**模式**: COLD (按需启动)

## 服务器概述

提供 Chrome DevTools Protocol 集成，支持浏览器调试、网络监控、性能分析等功能。

## 核心功能

1. **浏览器控制** - 页面导航、脚本执行
2. **网络监控** - 请求拦截、响应分析
3. **性能分析** - CPU/内存分析
4. **控制台访问** - 日志捕获

## 常用工具

- `navigate`: 导航到URL
- `execute_script`: 执行JavaScript
- `capture_screenshot`: 截图
- `get_console_logs`: 获取控制台日志

## 最佳实践

总是在使用前确保 Chrome 已启动并启用远程调试。

---

**最后更新**: 2025-12-31
