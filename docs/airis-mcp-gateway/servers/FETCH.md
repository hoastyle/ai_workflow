# Fetch MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 Fetch MCP 服务器

---

## 概述

Fetch MCP 是一个网页抓取服务器,提供从互联网获取 URL 内容并转换为 Markdown 格式的功能。它支持内容分页和原始 HTML 提取。

**服务器信息**:
- **Runner**: uvx (mcp-server-fetch)
- **Mode**: COLD (按需启动)
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 1 个工具
- **功能**: 网页抓取、Markdown 转换、分页支持

---

## 常见错误和修复

### 1. URL 格式错误

#### 错误示例

```
Error: Invalid URL format
```

#### 原因分析

URL 格式不正确或缺少协议前缀。

#### 修复方法

```typescript
// ❌ 错误
url: "example.com"
url: "www.github.com"

// ✅ 正确
url: "https://example.com"
url: "https://www.github.com"
```

**规则**: 必须包含完整的协议 (`http://` 或 `https://`)

---

### 2. 内容截断问题

#### 错误示例

```
Content truncated at 5000 characters...
```

#### 原因分析

默认 `max_length` 为 5000 字符,长页面会被截断。

#### 修复方法

**方法 1**: 增加 `max_length`
```typescript
await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://example.com/long-article",
  max_length: 50000  // 增加到 50K
})
```

**方法 2**: 使用 `start_index` 分页获取
```typescript
// 第一页 (0-5000)
const page1 = await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://example.com/article",
  max_length: 5000,
  start_index: 0
})

// 第二页 (5000-10000)
const page2 = await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://example.com/article",
  max_length: 5000,
  start_index: 5000
})
```

---

### 3. 网络超时错误

#### 错误示例

```
Error: Request timeout after 30s
```

#### 原因分析

目标网站响应缓慢或不可达。

#### 修复方法

**检查清单**:
- [ ] URL 是否正确?
- [ ] 网站是否可访问? (使用浏览器测试)
- [ ] 是否有防火墙/代理限制?

**解决方案**:
```bash
# 测试网站可达性
curl -I https://example.com

# 检查 DNS 解析
nslookup example.com
```

---

### 4. Markdown 转换不完整

#### 错误示例

```
Returned HTML instead of clean markdown
```

#### 原因分析

某些复杂页面的 Markdown 转换可能不完美。

#### 修复方法

**使用 `raw` 参数获取原始 HTML**:
```typescript
await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://example.com",
  raw: true  // 获取原始 HTML
})
```

然后使用其他工具处理 HTML。

---

## 工具参考

### fetch

**描述**: 从互联网获取 URL 内容,可选地转换为 Markdown

**参数签名**:
```typescript
{
  url: string;           // 必需: URL (必须包含 http/https)
  max_length?: number;   // 可选: 最大字符数 (默认 5000, 最大 1,000,000)
  start_index?: number;  // 可选: 起始字符索引 (默认 0)
  raw?: boolean;         // 可选: 返回原始 HTML (默认 false)
}
```

**参数详解**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | string | - | 要获取的 URL (必需) |
| `max_length` | number | 5000 | 最大返回字符数 (1-1,000,000) |
| `start_index` | number | 0 | 分页起始索引 |
| `raw` | boolean | false | 是否返回原始 HTML |

---

## 使用示例

### 场景 1: 获取网页作为 Markdown

```typescript
const result = await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://github.com/agiletec-inc/airis-mcp-gateway"
})

// 返回: 清理后的 Markdown 格式内容
// 适合提取文本信息、文档、博客文章
```

---

### 场景 2: 获取长内容 (分页)

```typescript
// Step 1: 获取第一页
const page1 = await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://example.com/long-doc",
  max_length: 10000,
  start_index: 0
})

// Step 2: 检查是否有更多内容
if (page1.includes("...truncated")) {
  const page2 = await airis-exec(tool: "fetch:fetch", arguments: {
    url: "https://example.com/long-doc",
    max_length: 10000,
    start_index: 10000
  })
}
```

---

### 场景 3: 获取原始 HTML

```typescript
const rawHtml = await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://example.com",
  raw: true
})

// 返回: 原始 HTML 内容
// 适合需要解析特定 HTML 结构的场景
```

---

### 场景 4: 获取 API 响应

```typescript
const apiResponse = await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://api.github.com/repos/agiletec-inc/airis-mcp-gateway",
  raw: true  // API 通常返回 JSON
})

// 返回: JSON 字符串 (需要解析)
```

---

## 最佳实践

### 1. URL 验证

**推荐**: 使用前验证 URL 格式

```typescript
function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// 使用
if (isValidUrl(targetUrl)) {
  await airis-exec(tool: "fetch:fetch", arguments: { url: targetUrl })
}
```

---

### 2. 内容长度管理

**策略**:
- **短页面** (<5K): 使用默认 `max_length`
- **中等页面** (5K-50K): 设置 `max_length: 50000`
- **长页面** (>50K): 使用分页策略

**示例**:
```typescript
// 动态调整 max_length
const contentLength = estimatedPageSize  // 估计页面大小
const maxLength = Math.min(contentLength * 1.2, 100000)

await airis-exec(tool: "fetch:fetch", arguments: {
  url: targetUrl,
  max_length: maxLength
})
```

---

### 3. Markdown vs Raw HTML

**选择指南**:

| 场景 | 推荐格式 | 参数 |
|------|---------|------|
| 提取文本内容 | Markdown | `raw: false` (默认) |
| 解析结构化数据 | Raw HTML | `raw: true` |
| API 响应 | Raw | `raw: true` |
| 文档/博客 | Markdown | `raw: false` |

---

### 4. 错误处理

**推荐模式**:
```typescript
try {
  const content = await airis-exec(tool: "fetch:fetch", arguments: {
    url: targetUrl,
    max_length: 10000
  })

  // 处理内容
  processContent(content)

} catch (error) {
  if (error.message.includes("timeout")) {
    console.log("网站响应超时,请稍后重试")
  } else if (error.message.includes("Invalid URL")) {
    console.log("URL 格式错误")
  } else {
    console.log("未知错误:", error.message)
  }
}
```

---

## FAQ

### Q1: Fetch MCP 和 Tavily MCP 有什么区别?

**答**:
- **Fetch MCP**: 直接获取 URL 内容,转换为 Markdown
- **Tavily MCP**: Web 搜索引擎,查找相关网页

**使用场景**:
- 已知 URL → 使用 Fetch
- 搜索信息 → 使用 Tavily

**组合使用**:
```typescript
// 1. 使用 Tavily 搜索
const searchResults = await tavily_search({ query: "AIRIS MCP Gateway" })

// 2. 使用 Fetch 获取第一个结果的内容
const content = await fetch({ url: searchResults.results[0].url })
```

---

### Q2: 可以获取需要登录的页面吗?

**答**: 不可以。Fetch MCP 是无状态的,不支持:
- Cookie 管理
- 登录认证
- Session 维护

**替代方案**: 使用 Playwright MCP 进行浏览器自动化。

---

### Q3: 支持哪些协议?

**答**: 支持 HTTP 和 HTTPS。

**不支持**:
- FTP
- File:// (本地文件)
- WebSocket

---

### Q4: 返回内容的格式是什么?

**答**:
- **默认** (`raw: false`): 清理后的 Markdown
- **原始** (`raw: true`): 原始 HTML 或响应内容

**Markdown 转换包含**:
- 标题 (`#`, `##`, 等)
- 链接 (`[text](url)`)
- 列表 (`-`, `1.`)
- 代码块 (` ``` `)

---

### Q5: 有请求频率限制吗?

**答**: Fetch MCP 本身没有频率限制,但:
- 目标网站可能有 rate limiting
- 建议添加适当延迟(如 1-2 秒间隔)

**最佳实践**:
```typescript
for (const url of urls) {
  await airis-exec(tool: "fetch:fetch", arguments: { url })
  await sleep(1000)  // 1秒延迟
}
```

---

### Q6: 如何处理重定向?

**答**: Fetch MCP 自动跟随 HTTP 重定向(如 301, 302)。

**示例**:
```typescript
// 短 URL 会自动跟随重定向
await airis-exec(tool: "fetch:fetch", arguments: {
  url: "https://bit.ly/shortened-url"
})
// 返回最终目标页面的内容
```

---

## 调试技巧

### 1. 验证 URL 可达性

```bash
# 方法 1: 使用 curl
curl -I https://example.com

# 方法 2: 使用 wget
wget --spider https://example.com

# 方法 3: 浏览器测试
# 直接在浏览器中打开 URL
```

---

### 2. 检查内容长度

```typescript
// 先获取少量内容测试
const sample = await airis-exec(tool: "fetch:fetch", arguments: {
  url: targetUrl,
  max_length: 1000  // 仅 1K 测试
})

// 检查是否截断
if (sample.includes("...")) {
  console.log("需要增加 max_length")
}
```

---

### 3. 调试 Markdown 转换

```typescript
// Step 1: 获取原始 HTML
const rawHtml = await airis-exec(tool: "fetch:fetch", arguments: {
  url: targetUrl,
  raw: true
})

// Step 2: 获取 Markdown 版本
const markdown = await airis-exec(tool: "fetch:fetch", arguments: {
  url: targetUrl,
  raw: false
})

// Step 3: 对比差异
compareContent(rawHtml, markdown)
```

---

### 4. 处理特殊字符

**问题**: 某些页面包含特殊字符导致解析错误

**解决**:
```typescript
// 使用 raw 模式获取,然后手动清理
const raw = await airis-exec(tool: "fetch:fetch", arguments: {
  url: targetUrl,
  raw: true
})

// 清理特殊字符
const cleaned = raw
  .replace(/[\u0000-\u001F\u007F-\u009F]/g, "")  // 移除控制字符
  .trim()
```

---

## 性能考虑

### 1. 网络延迟

**影响因素**:
- 目标网站响应速度
- 网络连接质量
- 页面大小

**优化建议**:
- 仅获取必要的内容长度
- 使用分页而非一次获取全部
- 考虑缓存常访问的页面

---

### 2. 内存使用

**建议**:
- `max_length` 不要超过 100,000 (100K)
- 超大页面使用分页策略
- 及时释放不需要的内容

---

## 相关文档

- **主文档**: [README.md](../../README.md)
- **MCP 索引**: [docs/mcp-usage-notes/README.md](README.md)
- **Tavily MCP**: [TAVILY_MCP_USAGE_NOTES.md](TAVILY_MCP_USAGE_NOTES.md) (Web 搜索)
- **Playwright MCP**: [PLAYWRIGHT_MCP_USAGE_NOTES.md](PLAYWRIGHT_MCP_USAGE_NOTES.md) (浏览器自动化)
- **Context7 MCP**: [CONTEXT7_MCP_USAGE_NOTES.md](CONTEXT7_MCP_USAGE_NOTES.md) (也包含 fetch 功能)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本,包含 1 个工具的完整文档 |

---

**文档状态**: ✅ 已验证
**测试覆盖**: 1/1 工具已通过 `airis-schema` 验证
**最后审查**: 2025-12-29
