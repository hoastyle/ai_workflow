# Magic MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 Magic MCP 服务器

---

## 概述

Magic MCP 是一个 UI 组件生成和搜索服务器，提供从 21st.dev 库搜索和生成 React 组件、Logo 搜索、组件优化等功能。

**服务器信息**:
- **Runner**: npx (@21st-dev/magic)
- **Mode**: COLD（按需启动）
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 4 个工具

---

## 常见错误和修复

### 1. 路径参数错误

#### 错误示例

```
Error: absolutePathToCurrentFile is required
```

#### 原因分析

Magic MCP 的组件构建工具需要绝对路径参数来确定在哪里应用更改。相对路径会导致错误。

#### 修复方法

**步骤 1: 获取当前工作目录**

```typescript
// 使用绝对路径
const currentDir = "/home/user/project"
const targetFile = `${currentDir}/src/components/Button.tsx`
```

**步骤 2: 使用绝对路径调用工具**

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_builder",
  arguments: {
    message: "Create a modern button component",
    searchQuery: "button",
    absolutePathToCurrentFile: "/home/user/project/src/components/Button.tsx",
    absolutePathToProjectDirectory: "/home/user/project",
    standaloneRequestQuery: "Create a reusable button component with variants"
  }
})
```

---

### 2. 搜索查询过于宽泛

#### 错误示例

```
Error: Too many results, please refine your search query
```

#### 原因分析

- 搜索关键词太通用（如 "component"）
- 没有指定具体的组件类型

#### 修复方法

```typescript
// ❌ 错误：搜索太宽泛
searchQuery: "component"

// ✅ 正确：具体的组件类型
searchQuery: "modal dialog"
searchQuery: "data table"
searchQuery: "file upload"
```

---

### 3. Logo 格式不匹配

#### 错误示例

```
Warning: Logo not found for query "XYZ"
```

#### 原因分析

- Logo 名称拼写错误
- Logo 不在 21st.dev 的 Logo 库中
- 搜索使用了非官方品牌名称

#### 修复方法

```typescript
// ✅ 使用官方品牌名称
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:logo_search",
  arguments: {
    queries: ["github", "discord", "slack"],  // 小写，官方名称
    format: "TSX"
  }
})

// ❌ 错误：使用非标准名称
queries: ["GitHub Inc.", "Discord App"]  // 太具体或包含额外词汇
```

---

## Magic MCP 工具参考

### 21st_magic_component_builder

**描述**: 当用户请求新的 UI 组件时使用（例如提到 /ui、/21、/21st，或要求按钮、输入框、对话框、表格等）

**关键特性**:
- 从 21st.dev 库搜索匹配的组件
- 仅返回文本片段（需手动集成到代码库）
- 支持 React 组件生成

**参数签名**:

```json
{
  "required": [
    "message",
    "searchQuery",
    "absolutePathToCurrentFile",
    "absolutePathToProjectDirectory",
    "standaloneRequestQuery"
  ],
  "properties": {
    "message": {
      "type": "string",
      "description": "用户的完整消息"
    },
    "searchQuery": {
      "type": "string",
      "description": "为 21st.dev 生成的搜索查询（2-4 个词）"
    },
    "absolutePathToCurrentFile": {
      "type": "string",
      "description": "要应用更改的当前文件的绝对路径"
    },
    "absolutePathToProjectDirectory": {
      "type": "string",
      "description": "项目根目录的绝对路径"
    },
    "standaloneRequestQuery": {
      "type": "string",
      "description": "基于用户消息、搜索查询和对话历史，提取创建 UI 组件所需的额外上下文"
    }
  }
}
```

**使用示例**:

```typescript
// 创建按钮组件
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_builder",
  arguments: {
    message: "I need a primary button with loading state",
    searchQuery: "button loading",
    absolutePathToCurrentFile: "/home/user/myapp/src/components/Button.tsx",
    absolutePathToProjectDirectory: "/home/user/myapp",
    standaloneRequestQuery: "Create a reusable button component with variants (primary, secondary) and loading state indicator"
  }
})

// 创建数据表格
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_builder",
  arguments: {
    message: "Create a sortable data table with pagination",
    searchQuery: "table pagination",
    absolutePathToCurrentFile: "/home/user/myapp/src/components/DataTable.tsx",
    absolutePathToProjectDirectory: "/home/user/myapp",
    standaloneRequestQuery: "Build a data table component with sortable columns, pagination controls, and row selection"
  }
})

// 创建对话框
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_builder",
  arguments: {
    message: "Add a confirmation dialog with yes/no buttons",
    searchQuery: "modal dialog",
    absolutePathToCurrentFile: "/home/user/myapp/src/components/ConfirmDialog.tsx",
    absolutePathToProjectDirectory: "/home/user/myapp",
    standaloneRequestQuery: "Create a reusable confirmation dialog with title, message, and action buttons"
  }
})
```

---

### logo_search

**描述**: 搜索并返回指定格式的 Logo（JSX、TSX、SVG）

**关键特性**:
- 支持单个或多个 Logo 搜索
- 支持类别过滤
- 可返回亮色/暗色主题变体

**参数签名**:

```json
{
  "required": ["queries", "format"],
  "properties": {
    "queries": {
      "type": "array",
      "items": {"type": "string"},
      "description": "要搜索 Logo 的公司名称列表"
    },
    "format": {
      "type": "string",
      "enum": ["JSX", "TSX", "SVG"],
      "description": "输出格式"
    }
  }
}
```

**何时使用**:
1. 用户输入 "/logo" 命令（例如 "/logo GitHub"）
2. 用户要求添加项目中不存在的公司 Logo

**示例查询**:
- 单个公司: `["discord"]`
- 多个公司: `["discord", "github", "slack"]`
- 特定品牌: `["microsoft office"]`
- 命令风格: "/logo GitHub" → `["github"]`
- 请求风格: "Add Discord logo to the project" → `["discord"]`

**使用示例**:

```typescript
// 搜索单个 Logo（TSX 格式）
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:logo_search",
  arguments: {
    queries: ["github"],
    format: "TSX"
  }
})

// 搜索多个 Logo（JSX 格式）
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:logo_search",
  arguments: {
    queries: ["discord", "slack", "github", "figma"],
    format: "JSX"
  }
})

// 获取 SVG 格式
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:logo_search",
  arguments: {
    queries: ["react", "vue", "angular"],
    format: "SVG"
  }
})
```

**返回格式示例**:

```typescript
// TSX 格式返回
{
  "logos": [
    {
      "name": "GitHub",
      "componentName": "GitHubIcon",
      "code": "export const GitHubIcon = () => (\n  <svg ...>...</svg>\n);",
      "import": "import { GitHubIcon } from './icons/GitHubIcon';"
    }
  ]
}
```

---

### 21st_magic_component_inspiration

**描述**: 当用户想查看组件、获取灵感或从 21st.dev 获取数据和预览时使用

**关键特性**:
- 返回匹配组件的 JSON 数据（不生成新代码）
- 用于浏览和探索现有组件
- 提供组件预览和数据

**参数签名**:

```json
{
  "required": ["message", "searchQuery"],
  "properties": {
    "message": {
      "type": "string",
      "description": "用户的完整消息"
    },
    "searchQuery": {
      "type": "string",
      "description": "21st.dev 的搜索查询（2-4 个词）"
    }
  }
}
```

**使用示例**:

```typescript
// 浏览卡片组件
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_inspiration",
  arguments: {
    message: "Show me some card component examples",
    searchQuery: "card component"
  }
})

// 查看表单设计灵感
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_inspiration",
  arguments: {
    message: "I want to see different form layouts",
    searchQuery: "form layout"
  }
})

// 探索导航栏样式
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_inspiration",
  arguments: {
    message: "What navigation bar designs are available?",
    searchQuery: "navigation bar"
  }
})
```

---

### 21st_magic_component_refiner

**描述**: 当用户请求用 /ui 或 /21 命令重新设计/优化/改进当前 UI 组件时使用

**关键特性**:
- 改进 React 组件的 UI
- 返回重新设计的组件版本
- 提供实施说明

**参数签名**:

```json
{
  "required": ["userMessage", "absolutePathToRefiningFile", "context"],
  "properties": {
    "userMessage": {
      "type": "string",
      "description": "关于 UI 优化的完整用户消息"
    },
    "absolutePathToRefiningFile": {
      "type": "string",
      "description": "需要优化的文件的绝对路径"
    },
    "context": {
      "type": "string",
      "description": "基于用户消息、代码和对话历史，提取需要改进的具体 UI 元素和方面"
    }
  }
}
```

**使用示例**:

```typescript
// 改进按钮样式
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_refiner",
  arguments: {
    userMessage: "/ui make the button more modern",
    absolutePathToRefiningFile: "/home/user/myapp/src/components/Button.tsx",
    context: "User wants to modernize the Button component styling - improve colors, shadows, hover effects, and overall visual appeal"
  }
})

// 优化表单布局
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_refiner",
  arguments: {
    userMessage: "Improve the form layout to be more user-friendly",
    absolutePathToRefiningFile: "/home/user/myapp/src/components/ContactForm.tsx",
    context: "Enhance form layout with better spacing, field grouping, validation feedback, and responsive design"
  }
})

// 重新设计卡片组件
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_refiner",
  arguments: {
    userMessage: "/21 redesign this card to match modern design trends",
    absolutePathToRefiningFile: "/home/user/myapp/src/components/ProductCard.tsx",
    context: "Redesign ProductCard with modern aesthetics: gradient backgrounds, rounded corners, subtle shadows, and improved typography"
  }
})
```

---

## 最佳实践

### 1. 组件构建工作流

```
Step 1: 明确组件需求
  - 确定组件类型（按钮、表格、对话框等）
  - 列出所需功能（加载状态、排序、验证等）

Step 2: 生成搜索查询
  - 使用 2-4 个关键词
  - 具体而非通用（"button loading" 而非 "button"）

Step 3: 调用 component_builder
  - 提供绝对路径
  - 详细的 standaloneRequestQuery

Step 4: 集成到代码库
  - 手动将返回的代码片段添加到文件
  - 调整导入和样式

Step 5: 优化（可选）
  - 使用 component_refiner 改进设计
```

### 2. Logo 搜索最佳实践

| 场景 | 推荐做法 |
|------|---------|
| 需要多个 Logo | 一次调用传入数组 `["github", "discord", "slack"]` |
| TypeScript 项目 | 使用 `format: "TSX"` |
| JavaScript 项目 | 使用 `format: "JSX"` |
| 需要原始 SVG | 使用 `format: "SVG"` |
| Logo 名称不确定 | 使用官方品牌名称小写（github 而非 GitHub Inc.） |

### 3. 搜索查询优化

**组件类型关键词**:
- 按钮: "button", "button loading", "button group"
- 表单: "form input", "form validation", "file upload"
- 导航: "navbar", "sidebar", "breadcrumb"
- 数据展示: "table", "data grid", "card list"
- 反馈: "modal", "toast", "notification", "alert"
- 布局: "grid layout", "flex container", "responsive layout"

**组合关键词示例**:
- "modal dialog confirm"
- "table sortable pagination"
- "form multi-step wizard"
- "card hover animation"

### 4. 组件 vs 灵感 vs 优化

| 工具 | 场景 | 输出 |
|------|------|------|
| `component_builder` | 创建新组件 | 可集成的代码片段 |
| `component_inspiration` | 浏览设计参考 | JSON 数据和预览 |
| `component_refiner` | 改进现有组件 | 重新设计的代码 + 说明 |

---

## 常见问题 FAQ

### Q1: Magic MCP 需要 API Key 吗？

**答**: 不需要。Magic MCP 直接访问 21st.dev 的公开库，无需注册或配置 API Key。

### Q2: 如何查看可用的组件类型？

**答**: 使用 `component_inspiration` 浏览：

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_inspiration",
  arguments: {
    message: "Show me all available components",
    searchQuery: "components"
  }
})
```

### Q3: 返回的代码是什么框架？

**答**: 默认返回 React 组件（JSX/TSX）。需要其他框架请在 `standaloneRequestQuery` 中说明。

### Q4: 生成的组件可以直接使用吗？

**答**: 基本可以，但可能需要：
- 调整导入路径
- 添加项目特定的样式类
- 配置状态管理
- 处理类型定义（TypeScript）

### Q5: Logo 库包含哪些品牌？

**答**: 包含主流科技公司、框架和工具的 Logo。完整列表可通过搜索探索，常见的包括：
- 科技公司: GitHub, Discord, Slack, Microsoft, Google
- 开发工具: React, Vue, Angular, Node.js, Docker
- 设计工具: Figma, Sketch, Adobe XD

### Q6: 如何定制生成的组件？

**答**:
1. 在 `standaloneRequestQuery` 中详细描述需求
2. 使用 `component_refiner` 进一步优化
3. 手动修改生成的代码

---

## 调试技巧

### 1. 检查 Magic MCP 服务器状态

```bash
# 查看服务器是否启动
curl -s http://localhost:9400/process/servers | jq '.servers[] | select(.name == "magic")'

# 查看工具列表
curl -s http://localhost:9400/process/tools?server=magic | jq '.tools[].name'
```

### 2. 验证路径参数

```bash
# 确保使用绝对路径
pwd  # 获取当前目录
# 输出: /home/user/myapp

# 构建绝对路径
absolutePathToCurrentFile="/home/user/myapp/src/components/Button.tsx"
absolutePathToProjectDirectory="/home/user/myapp"
```

### 3. 搜索查询调试

```typescript
// 先用 inspiration 测试搜索查询
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:21st_magic_component_inspiration",
  arguments: {
    message: "Test search",
    searchQuery: "your test query"
  }
})

// 如果返回结果，说明查询有效
// 然后用于 component_builder
```

### 4. Logo 搜索故障排除

```typescript
// 测试常见 Logo（应该都能找到）
mcp__airis-mcp-gateway__airis-exec({
  tool: "magic:logo_search",
  arguments: {
    queries: ["github", "react", "typescript"],
    format: "TSX"
  }
})

// 如果失败，检查：
// 1. 拼写是否正确
// 2. 是否使用小写
// 3. 是否使用官方品牌名称
```

---

## 相关文档

- [AIRIS MCP Gateway README](../../README.md)
- [21st.dev 官网](https://21st.dev)
- [21st.dev 组件库](https://21st.dev/components)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本，记录 4 个工具的完整参数和使用模式 |

---

**维护者**: 自动从使用经验中提炼
**反馈**: 如发现新的使用问题，请更新本文档
