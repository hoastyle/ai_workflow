# Playwright MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 Playwright MCP 服务器

---

## 概述

Playwright MCP 是一个浏览器自动化服务器，提供网页导航、交互、截图和内容提取功能。

**服务器信息**:
- **Runner**: npx (@playwright/mcp)
- **Mode**: COLD（按需启动）
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 22 个工具

---

## 常见错误和修复

### 1. 浏览器未安装错误

#### 错误示例

```
Error: browserType.launchPersistentContext: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
Run "npx playwright install chrome"
```

#### 原因分析

Playwright MCP 需要安装 Chromium 浏览器才能工作。首次使用时需要显式安装浏览器二进制文件。

#### 修复方法

**步骤 1: 安装浏览器**

使用 `browser_install` 工具安装浏览器：

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_install",
  arguments: {}
})
```

**步骤 2: 验证安装**

安装完成后，尝试导航到测试页面：

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://example.com"
  }
})
```

---

### 2. 元素引用不存在错误

#### 错误示例

```
Error: Element with ref "abc123" not found on page
```

#### 原因分析

- 使用了过期的元素引用（`ref`）
- 页面已导航到新页面，之前的 `ref` 失效
- 元素还未加载完成

#### 修复方法

**步骤 1: 获取当前页面快照**

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {}
})
```

**步骤 2: 从快照中提取正确的 ref**

快照会返回页面的可访问性树，包含所有可交互元素的 `ref` 值。

**步骤 3: 使用新的 ref 进行交互**

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "Submit button",
    ref: "new_ref_from_snapshot"
  }
})
```

---

### 3. 页面导航超时

#### 错误示例

```
Error: Navigation timeout exceeded
```

#### 原因分析

- 网页加载时间过长
- 网络连接问题
- 页面中有阻塞的资源请求

#### 修复方法

```typescript
// 暂无超时参数配置
// 建议：先访问轻量级页面测试连接，或等待网络恢复
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://example.com"  // 轻量级测试页面
  }
})
```

---

## Playwright MCP 工具参考

### 核心导航工具

#### browser_navigate

**描述**: 导航到指定 URL

**参数签名**:

```json
{
  "required": ["url"],
  "properties": {
    "url": {
      "type": "string",
      "description": "要导航到的 URL"
    }
  }
}
```

**使用示例**:

```typescript
// 导航到网页
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://github.com/anthropics/anthropic-sdk-python"
  }
})
```

---

#### browser_navigate_back

**描述**: 返回上一页

**参数签名**: 无参数

**使用示例**:

```typescript
// 返回上一页
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_navigate_back",
  arguments: {}
})
```

---

### 页面内容获取

#### browser_snapshot

**描述**: 捕获页面的可访问性快照（优于截图，用于后续操作）

**参数签名**:

```json
{
  "properties": {
    "filename": {
      "type": "string",
      "description": "保存快照到 Markdown 文件而非返回响应"
    }
  }
}
```

**使用示例**:

```typescript
// 获取页面结构（返回可访问性树）
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {}
})

// 保存快照到文件
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {
    filename: "page_structure.md"
  }
})
```

---

#### browser_take_screenshot

**描述**: 对当前页面或元素截图（不能用于后续操作，仅可视化）

**参数签名**:

```json
{
  "properties": {
    "type": {
      "type": "string",
      "enum": ["png", "jpeg"],
      "default": "png"
    },
    "filename": {
      "type": "string",
      "description": "保存截图的文件名"
    },
    "element": {
      "type": "string",
      "description": "元素的人类可读描述"
    },
    "ref": {
      "type": "string",
      "description": "从页面快照获取的元素引用"
    },
    "fullPage": {
      "type": "boolean",
      "description": "截取整个页面（不能与元素截图同时使用）"
    }
  }
}
```

**使用示例**:

```typescript
// 截取整个视口
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_take_screenshot",
  arguments: {
    type: "png"
  }
})

// 截取完整页面
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_take_screenshot",
  arguments: {
    fullPage: true,
    filename: "full_page.png"
  }
})

// 截取特定元素
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_take_screenshot",
  arguments: {
    element: "Main navigation bar",
    ref: "ref_from_snapshot",
    filename: "navbar.png"
  }
})
```

---

### 页面交互工具

#### browser_click

**描述**: 点击页面元素

**参数签名**:

```json
{
  "required": ["element", "ref"],
  "properties": {
    "element": {
      "type": "string",
      "description": "元素的人类可读描述"
    },
    "ref": {
      "type": "string",
      "description": "从页面快照获取的精确元素引用"
    },
    "doubleClick": {
      "type": "boolean",
      "description": "是否执行双击"
    },
    "button": {
      "type": "string",
      "enum": ["left", "right", "middle"],
      "description": "要点击的鼠标按钮"
    },
    "modifiers": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["Alt", "Control", "ControlOrMeta", "Meta", "Shift"]
      },
      "description": "按住的修饰键"
    }
  }
}
```

**使用示例**:

```typescript
// 左键单击
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "Login button",
    ref: "button_ref_123"
  }
})

// 右键点击
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "Context menu trigger",
    ref: "menu_ref_456",
    button: "right"
  }
})

// Ctrl + 点击（新标签页打开）
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "External link",
    ref: "link_ref_789",
    modifiers: ["Control"]
  }
})
```

---

#### browser_type

**描述**: 在可编辑元素中输入文本

**参数签名**:

```json
{
  "required": ["element", "ref", "text"],
  "properties": {
    "element": {
      "type": "string",
      "description": "元素的人类可读描述"
    },
    "ref": {
      "type": "string",
      "description": "从页面快照获取的元素引用"
    },
    "text": {
      "type": "string",
      "description": "要输入的文本"
    },
    "submit": {
      "type": "boolean",
      "description": "是否在输入后按 Enter 提交"
    },
    "slowly": {
      "type": "boolean",
      "description": "是否逐字符输入（触发键盘事件）"
    }
  }
}
```

**使用示例**:

```typescript
// 输入文本
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_type",
  arguments: {
    element: "Search input field",
    ref: "input_ref_abc",
    text: "Playwright automation"
  }
})

// 输入并提交
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_type",
  arguments: {
    element: "Username field",
    ref: "username_ref",
    text: "user@example.com",
    submit: true
  }
})

// 逐字符输入（触发键盘事件）
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_type",
  arguments: {
    element: "Auto-complete search",
    ref: "search_ref",
    text: "Python",
    slowly: true
  }
})
```

---

#### browser_fill_form

**描述**: 填充多个表单字段

**参数签名**: （需要通过 airis-schema 查询）

**使用示例**:

```typescript
// 查询完整参数
mcp__airis-mcp-gateway__airis-schema({
  tool: "playwright:browser_fill_form"
})
```

---

#### browser_hover

**描述**: 悬停在元素上

**参数签名**: （需要通过 airis-schema 查询）

**使用示例**:

```typescript
// 悬停显示工具提示
mcp__airis-mcp-gateway__airis-schema({
  tool: "playwright:browser_hover"
})
```

---

#### browser_select_option

**描述**: 在下拉菜单中选择选项

**参数签名**: （需要通过 airis-schema 查询）

**使用示例**:

```typescript
// 选择下拉选项
mcp__airis-mcp-gateway__airis-schema({
  tool: "playwright:browser_select_option"
})
```

---

### 高级操作

#### browser_evaluate

**描述**: 在页面或元素上执行 JavaScript 表达式

**参数签名**:

```json
{
  "required": ["function"],
  "properties": {
    "function": {
      "type": "string",
      "description": "() => { /* code */ } 或 (element) => { /* code */ }"
    },
    "element": {
      "type": "string",
      "description": "元素的人类可读描述"
    },
    "ref": {
      "type": "string",
      "description": "从页面快照获取的元素引用"
    }
  }
}
```

**使用示例**:

```typescript
// 获取页面标题
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_evaluate",
  arguments: {
    function: "() => document.title"
  }
})

// 获取元素文本内容
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_evaluate",
  arguments: {
    element: "Article heading",
    ref: "heading_ref",
    function: "(element) => element.textContent"
  }
})

// 执行复杂脚本
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_evaluate",
  arguments: {
    function: "() => { return Array.from(document.querySelectorAll('a')).map(a => a.href); }"
  }
})
```

---

#### browser_run_code

**描述**: 运行 Playwright 代码片段

**参数签名**: （需要通过 airis-schema 查询）

---

#### browser_console_messages

**描述**: 返回所有控制台消息

**参数签名**: 无参数

**使用示例**:

```typescript
// 获取控制台输出
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_console_messages",
  arguments: {}
})
```

---

#### browser_network_requests

**描述**: 返回自加载页面以来的所有网络请求

**参数签名**: 无参数

**使用示例**:

```typescript
// 查看网络请求
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_network_requests",
  arguments: {}
})
```

---

### 其他工具

| 工具名 | 描述 |
|--------|------|
| `browser_close` | 关闭页面 |
| `browser_resize` | 调整浏览器窗口大小 |
| `browser_handle_dialog` | 处理对话框（alert/confirm/prompt） |
| `browser_press_key` | 按键盘按键 |
| `browser_drag` | 在两个元素间拖放 |
| `browser_file_upload` | 上传文件 |
| `browser_install` | 安装浏览器（首次使用必须） |

---

## 最佳实践

### 1. 工作流程

```
Step 1: 安装浏览器（首次使用）
  → browser_install

Step 2: 导航到目标页面
  → browser_navigate

Step 3: 获取页面结构
  → browser_snapshot

Step 4: 分析快照，提取元素 ref

Step 5: 执行交互操作
  → browser_click / browser_type / browser_select_option

Step 6: 验证结果
  → browser_snapshot / browser_take_screenshot
```

### 2. 元素定位策略

**关键原则**: 永远先获取快照，再提取 ref

```typescript
// ❌ 错误：猜测 ref
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "Button",
    ref: "button123"  // 错误！这是猜的
  }
})

// ✅ 正确：从快照获取 ref
// 1. 获取快照
const snapshot = await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {}
})

// 2. 分析快照，找到元素的实际 ref
// 3. 使用实际 ref
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "Submit button",
    ref: "actual_ref_from_snapshot"
  }
})
```

### 3. 截图 vs 快照选择

| 场景 | 工具 | 原因 |
|------|------|------|
| 需要后续操作（点击、输入） | `browser_snapshot` | 返回可访问性树和 ref |
| 仅需可视化展示 | `browser_take_screenshot` | 返回图片 |
| 调试布局问题 | `browser_take_screenshot` | 直观看到视觉效果 |
| 获取页面文本内容 | `browser_snapshot` | 结构化文本数据 |

### 4. 表单填充组合

```typescript
// 方式 1: 逐字段填写
// 1. 填写用户名
await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_type",
  arguments: {
    element: "Username",
    ref: "user_ref",
    text: "user@example.com"
  }
})

// 2. 填写密码
await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_type",
  arguments: {
    element: "Password",
    ref: "pass_ref",
    text: "SecurePassword123"
  }
})

// 3. 提交
await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    element: "Login button",
    ref: "login_ref"
  }
})

// 方式 2: 使用 browser_fill_form（批量填写）
await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_fill_form",
  arguments: {
    // 查询完整参数结构
  }
})
```

---

## 常见问题 FAQ

### Q1: 如何安装浏览器？

**答**: 使用 `browser_install` 工具：

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_install",
  arguments: {}
})
```

### Q2: 如何获取元素的 ref？

**答**: 使用 `browser_snapshot` 获取页面的可访问性树，从中提取元素的 `ref` 值。

```typescript
const snapshot = await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {}
})
// 分析返回的快照内容，找到目标元素的 ref
```

### Q3: 支持哪些浏览器？

**答**: 默认使用 Chromium。可以通过配置使用 Firefox 或 WebKit（需查阅 Playwright 官方文档）。

### Q4: 如何处理弹窗（alert/confirm）？

**答**: 使用 `browser_handle_dialog` 工具：

```typescript
mcp__airis-mcp-gateway__airis-schema({
  tool: "playwright:browser_handle_dialog"
})
```

### Q5: 如何等待页面加载完成？

**答**: Playwright 默认会等待页面的 `load` 事件。对于 SPA（单页应用），可以使用 `browser_evaluate` 检查特定元素是否存在。

### Q6: 如何在新标签页打开链接？

**答**: 使用 `browser_click` 并设置 `modifiers: ["Control"]`（Windows/Linux）或 `["Meta"]`（macOS）。

---

## 调试技巧

### 1. 启用详细日志

```bash
# 在 airis-mcp-gateway 中启用调试模式
export LOG_LEVEL=DEBUG
docker compose up -d
```

### 2. 检查 Playwright MCP 服务器状态

```bash
# 查看服务器是否启动
curl -s http://localhost:9400/process/servers | jq '.servers[] | select(.name == "playwright")'

# 查看工具列表
curl -s http://localhost:9400/process/tools?server=playwright | jq '.tools[].name'
```

### 3. 保存快照到文件进行分析

```typescript
// 保存快照到 Markdown 文件
mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {
    filename: "debug_snapshot.md"
  }
})
```

### 4. 使用控制台和网络工具调试

```typescript
// 查看控制台错误
const console = await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_console_messages",
  arguments: {}
})

// 查看网络请求（检查 API 调用）
const network = await mcp__airis-mcp-gateway__airis-exec({
  tool: "playwright:browser_network_requests",
  arguments: {}
})
```

---

## 相关文档

- [AIRIS MCP Gateway README](../../README.md)
- [Playwright 官方文档](https://playwright.dev)
- [Playwright MCP GitHub](https://github.com/playwright-community/mcp-server-playwright)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本，记录 22 个工具的核心参数和使用模式 |

---

**维护者**: 自动从使用经验中提炼
**反馈**: 如发现新的使用问题，请更新本文档
