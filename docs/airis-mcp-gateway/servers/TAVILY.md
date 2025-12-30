---
title: "Tavily MCP 服务器"
description: "AI 优化的 Web 搜索和研究工具"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-29"
last_updated: "2025-12-31"
related_documents:
  - path: "../PARAMETER_TRAPS.md"
    type: "参考"
    description: "Tavily 参数使用指南"
  - path: "../QUICK_REFERENCE.md"
    type: "参考"
    description: "快速参考指南"
related_code: []
tags: ["tavily", "web-search", "research", "cold-mode"]
---

# Tavily MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 Tavily MCP 服务器

---

## 概述

Tavily MCP 是一个 Web 搜索和实时信息检索服务器，提供搜索、提取、爬取和网站映射功能。

**服务器信息**:
- **Runner**: npx (@tavily/mcp-server)
- **Mode**: COLD（按需启动）
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 4 个工具

---

## 常见错误和修复

### 1. API Key 未设置错误

#### 错误示例

```
Error: TAVILY_API_KEY environment variable is not set
```

#### 原因分析

Tavily MCP 需要有效的 API Key 才能工作。API Key 需要从 [Tavily](https://tavily.com) 获取并设置到环境中。

#### 修复方法

**步骤 1: 获取 API Key**

1. 访问 [https://tavily.com](https://tavily.com)
2. 注册账号（免费额度：1000 次/月）
3. 在 Dashboard 中复制 API Key

**步骤 2: 设置环境变量**

```bash
# 在 ~/.zshrc 中添加（使用 Zsh）
echo 'export TAVILY_API_KEY="tvly-你的API密钥"' >> ~/.zshrc
source ~/.zshrc

# 或在 ~/.bashrc 中添加（使用 Bash）
echo 'export TAVILY_API_KEY="tvly-你的API密钥"' >> ~/.bashrc
source ~/.bashrc
```

**步骤 3: 重启服务**

```bash
cd /path/to/airis-mcp-gateway
docker compose restart
```

---

### 2. API Key 无效错误

#### 错误示例

```
Error: Invalid Tavily API key
```

#### 原因分析

- API Key 格式不正确（应以 `tvly-` 开头）
- API Key 已过期或被撤销
- 复制时包含多余空格或字符

#### 修复方法

```bash
# 验证 API Key 格式
echo $TAVILY_API_KEY
# 应显示类似: tvly-XXXXXXXXXXXXXXXXXXXXXXXX

# 如果格式不对或无效，重新设置
export TAVILY_API_KEY="tvly-新的API密钥"

# 更新到配置文件
# 编辑 ~/.zshrc，修改 TAVILY_API_KEY 行
```

---

### 3. 搜索结果为空

#### 错误示例

```json
{
  "results": [],
  "query": "some query"
}
```

#### 原因分析

- 搜索关键词过于具体或拼写错误
- `search_depth` 设置为 `basic` 但需要 `advanced`
- `topic` 类型不匹配查询内容
- `exclude_domains` 错误地排除了相关结果

#### 修复方法

```typescript
// 调整搜索参数
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_search",
  arguments: {
    query: "your search query",
    search_depth: "advanced",  // 尝试 advanced
    max_results: 10,           // 增加结果数量
    topic: "general",          // 确保主题匹配
    time_range: "month"        // 调整时间范围
  }
})
```

---

## Tavily MCP 工具参考

### tavily_search

**描述**: 搜索 Web 获取实时信息

**参数签名**:

```json
{
  "required": ["query"],
  "properties": {
    "query": {
      "type": "string",
      "description": "搜索查询"
    },
    "max_results": {
      "type": "integer",
      "default": 5,
      "description": "返回的最大结果数"
    },
    "search_depth": {
      "type": "string",
      "enum": ["basic", "advanced"],
      "default": "basic",
      "description": "搜索深度"
    },
    "topic": {
      "type": "string",
      "enum": ["general", "news", "finance"],
      "default": "general",
      "description": "搜索类别"
    },
    "days": {
      "type": "integer",
      "default": 30,
      "description": "搜索回溯天数（仅 news 主题）"
    },
    "time_range": {
      "type": "string",
      "enum": ["day", "week", "month", "year", "d", "w", "m", "y"],
      "default": "month",
      "description": "时间范围（general 和 news 支持）"
    },
    "include_images": {
      "type": "boolean",
      "default": false
    },
    "include_image_descriptions": {
      "type": "boolean",
      "default": false
    },
    "include_raw_content": {
      "type": "boolean",
      "default": false,
      "description": "包含清理和解析的 HTML 内容"
    },
    "include_domains": {
      "type": "array",
      "items": {"type": "string"},
      "default": [],
      "description": "包含的域名列表"
    },
    "exclude_domains": {
      "type": "array",
      "items": {"type": "string"},
      "default": [],
      "description": "排除的域名列表"
    },
    "country": {
      "type": "string",
      "default": "",
      "description": "优先特定国家的结果（仅 general 主题）"
    },
    "include_favicon": {
      "type": "boolean",
      "default": false
    },
    "start_date": {
      "type": "string",
      "default": "",
      "description": "开始日期 (YYYY-MM-DD)"
    },
    "end_date": {
      "type": "string",
      "default": "",
      "description": "结束日期 (YYYY-MM-DD)"
    }
  }
}
```

**使用示例**:

```typescript
// 基础搜索
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_search",
  arguments: {
    query: "Python async await best practices"
  }
})

// 新闻搜索（最近 7 天）
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_search",
  arguments: {
    query: "AI technology news",
    topic: "news",
    time_range: "week",
    max_results: 10
  }
})

// 高级搜索（包含原始内容）
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_search",
  arguments: {
    query: "Rust vs C++ performance",
    search_depth: "advanced",
    include_raw_content: true,
    max_results: 5
  }
})

// 特定域名搜索
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_search",
  arguments: {
    query: "machine learning tutorials",
    include_domains: ["github.com", "stackoverflow.com"],
    max_results: 10
  }
})
```

---

### tavily_extract

**描述**: 从特定 URL 提取和处理内容

**参数签名**:

```json
{
  "required": ["urls"],
  "properties": {
    "urls": {
      "type": "array",
      "items": {"type": "string"},
      "description": "要提取内容的 URL 列表"
    },
    "extract_depth": {
      "type": "string",
      "enum": ["basic", "advanced"],
      "default": "basic",
      "description": "提取深度（LinkedIn URL 需使用 advanced）"
    },
    "include_images": {
      "type": "boolean",
      "default": false
    },
    "format": {
      "type": "string",
      "enum": ["markdown", "text"],
      "default": "markdown"
    },
    "include_favicon": {
      "type": "boolean",
      "default": false
    },
    "query": {
      "type": "string",
      "default": "",
      "description": "用于重新排序提取内容的自然语言查询"
    }
  }
}
```

**使用示例**:

```typescript
// 提取单个页面（Markdown 格式）
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_extract",
  arguments: {
    urls: ["https://example.com/article"]
  }
})

// 提取多个页面
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_extract",
  arguments: {
    urls: [
      "https://docs.python.org/3/library/asyncio.html",
      "https://docs.python.org/3/tutorial/index.html"
    ],
    format: "markdown"
  }
})

// LinkedIn 内容提取（需要 advanced）
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_extract",
  arguments: {
    urls: ["https://www.linkedin.com/pulse/..."],
    extract_depth: "advanced"
  }
})

// 使用查询重新排序结果
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_extract",
  arguments: {
    urls: ["https://blog.example.com/long-article"],
    query: "performance optimization tips",
    format: "markdown"
  }
})
```

---

### tavily_crawl

**描述**: 从网站爬取多个页面（内容截断为 500 字符/页）

**参数签名**:

```json
{
  "required": ["url"],
  "properties": {
    "url": {
      "type": "string",
      "description": "开始爬取的根 URL"
    },
    "max_depth": {
      "type": "integer",
      "default": 1,
      "minimum": 1,
      "description": "爬取深度"
    },
    "max_breadth": {
      "type": "integer",
      "default": 20,
      "minimum": 1,
      "description": "每层跟随的最大链接数"
    },
    "limit": {
      "type": "integer",
      "default": 50,
      "minimum": 1,
      "description": "处理的链接总数上限"
    },
    "instructions": {
      "type": "string",
      "default": "",
      "description": "爬虫的自然语言指令"
    },
    "select_paths": {
      "type": "array",
      "items": {"type": "string"},
      "default": [],
      "description": "选择特定路径的正则表达式（如 /docs/.*）"
    },
    "select_domains": {
      "type": "array",
      "items": {"type": "string"},
      "default": [],
      "description": "限制到特定域名的正则表达式"
    },
    "exclude_paths": {
      "type": "array",
      "items": {"type": "string"},
      "default": [],
      "description": "排除特定路径的正则表达式"
    },
    "exclude_domains": {
      "type": "array",
      "items": {"type": "string"},
      "default": [],
      "description": "排除特定域名的正则表达式"
    },
    "allow_external": {
      "type": "boolean",
      "default": true,
      "description": "是否返回外部链接"
    },
    "include_images": {
      "type": "boolean",
      "default": false
    },
    "extract_depth": {
      "type": "string",
      "enum": ["basic", "advanced"],
      "default": "basic"
    },
    "format": {
      "type": "string",
      "enum": ["markdown", "text"],
      "default": "markdown"
    },
    "include_favicon": {
      "type": "boolean",
      "default": false
    }
  }
}
```

**使用示例**:

```typescript
// 爬取文档站点（仅 /docs/ 路径）
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_crawl",
  arguments: {
    url: "https://project.example.com",
    select_paths: ["/docs/.*"],
    max_depth: 2,
    limit: 30,
    instructions: "Only return API documentation pages"
  }
})

// 爬取博客（排除特定路径）
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_crawl",
  arguments: {
    url: "https://blog.example.com",
    exclude_paths: ["/tag/.*", "/author/.*"],
    max_breadth: 15,
    limit: 20,
    format: "markdown"
  }
})
```

---

### tavily_map

**描述**: 映射网站结构，发现所有 URL（不提取内容）

**参数签名**:

```json
{
  "required": ["url"],
  "properties": {
    "url": {
      "type": "string",
      "description": "开始映射的根 URL"
    },
    "max_depth": {
      "type": "integer",
      "default": 1,
      "minimum": 1
    },
    "max_breadth": {
      "type": "integer",
      "default": 20,
      "minimum": 1
    },
    "limit": {
      "type": "integer",
      "default": 50,
      "minimum": 1
    },
    "instructions": {
      "type": "string",
      "default": ""
    },
    "select_paths": {
      "type": "array",
      "items": {"type": "string"},
      "default": []
    },
    "select_domains": {
      "type": "array",
      "items": {"type": "string"},
      "default": []
    },
    "exclude_paths": {
      "type": "array",
      "items": {"type": "string"},
      "default": []
    },
    "exclude_domains": {
      "type": "array",
      "items": {"type": "string"},
      "default": []
    },
    "allow_external": {
      "type": "boolean",
      "default": true
    }
  }
}
```

**使用示例**:

```typescript
// 映射文档站点结构
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_map",
  arguments: {
    url: "https://docs.example.com",
    max_depth: 3,
    limit: 100
  }
})

// 映射并过滤特定路径
mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_map",
  arguments: {
    url: "https://example.com",
    select_paths: ["/api/.*"],
    exclude_paths: ["/api/v1/.*"],
    instructions: "Only API v2+ endpoints"
  }
})
```

---

## 最佳实践

### 1. 工具选择决策树

```
需要 Web 信息？
│
├─ 搜索未知信息
│  └─ tavily_search (实时搜索)
│
├─ 已知 URL 需要内容
│  └─ tavily_extract (提取完整内容)
│
├─ 探索网站结构
│  └─ tavily_map (发现 URL)
│
└─ 从网站获取多个页面摘要
   └─ tavily_crawl (截断内容)
   然后用 tavily_extract 获取完整内容
```

### 2. 搜索参数优化

**通用搜索**:
```typescript
{ query: "...", search_depth: "basic", topic: "general" }
```

**最新新闻**:
```typescript
{ query: "...", topic: "news", time_range: "day", max_results: 10 }
```

**深度研究**:
```typescript
{
  query: "...",
  search_depth: "advanced",
  include_raw_content: true,
  max_results: 10
}
```

**特定网站**:
```typescript
{
  query: "...",
  include_domains: ["docs.python.org", "github.com"],
  exclude_domains: ["stackoverflow.com"]
}
```

### 3. 爬取与提取组合

```typescript
// 步骤 1: 映射网站
const mapResult = await mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_map",
  arguments: {
    url: "https://docs.example.com",
    select_paths: ["/api/.*"]
  }
})

// 步骤 2: 从映射结果提取完整内容
const urls = mapResult.links.map(l => l.url).slice(0, 10)
await mcp__airis-mcp-gateway__airis-exec({
  tool: "tavily:tavily_extract",
  arguments: {
    urls: urls,
    format: "markdown"
  }
})
```

---

## 常见问题 FAQ

### Q1: Tavily 免费额度是多少？

**答**: 免费账号每月 1000 次搜索请求。超出后需要付费升级。

### Q2: 如何查看剩余配额？

**答**: 访问 [Tavily Dashboard](https://tavily.com/dashboard) 查看使用情况。

### Q3: `search_depth` 的区别是什么？

**答**:
- **basic**: 快速搜索，返回摘要和关键信息
- **advanced**: 深度搜索，包含更多上下文和详细内容

### Q4: 为什么 `tavily_crawl` 内容被截断？

**答**: `tavily_crawl` 每页截断为 500 字符。获取完整内容：
1. 用 `tavily_map` 发现 URL
2. 用 `tavily_extract` 提取完整内容

### Q5: 如何只搜索特定时间范围？

**答**: 使用 `start_date` 和 `end_date`:
```typescript
{
  query: "...",
  start_date: "2025-01-01",
  end_date: "2025-12-31"
}
```

---

## 调试技巧

### 1. 检查 API Key

```bash
# 检查环境变量
echo $TAVILY_API_KEY

# 验证格式（应以 tvly- 开头）
echo $TAVILY_API_KEY | grep "^tvly-"

# 测试 API（需要 curl 和 jq）
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$TAVILY_API_KEY\",\"query\":\"test\",\"max_results\":1}" | jq
```

### 2. 查看服务器日志

```bash
# 查看 Tavily MCP 服务器日志
docker logs airis-mcp-gateway --tail 50 | grep tavily

# 或查看 ProcessRunner 日志
docker logs airis-mcp-gateway 2>&1 | grep -A5 "tavily"
```

### 3. 验证工具可用性

```typescript
// 列出所有 Tavily 工具
mcp__airis-mcp-gateway__airis-find({
  query: "tavily",
  server: "tavily"
})
```

---

## 相关文档

- [AIRIS MCP Gateway README](../../README.md)
- [Tavily 官方文档](https://docs.tavily.com)
- [Tavily API 参考](https://docs.tavily.com/docs/rest-api)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本，记录 4 个工具的完整参数签名和使用示例 |

---

**维护者**: 自动从使用经验中提炼
**反馈**: 如发现新的使用问题，请更新本文档
