# MorphLLM MCP 使用注意事项

**版本**: 1.0
**最后更新**: 2025-12-29
**适用范围**: AIRIS MCP Gateway 中的 MorphLLM MCP 服务器

---

## 概述

MorphLLM MCP 是一个高级代码编辑和搜索服务器，提供快速文件编辑（10,500+ tokens/sec）和智能代码库搜索功能。

**服务器信息**:
- **Runner**: npx (@morphllm/morphmcp)
- **Mode**: COLD（按需启动）
- **端口**: 通过 AIRIS MCP Gateway 代理
- **工具数量**: 2 个工具

---

## 常见错误和修复

### 1. Cursor 编辑器兼容性问题

#### 错误示例

```
Error: File is not in an editable state
```

#### 原因分析

在 Cursor 编辑器中使用 `edit_file` 工具时，如果文件处于非编辑状态，工具会失败。这是 Cursor 的一个已知限制。

#### 修复方法

**步骤 1: 先使用 search_replace 添加空行**

```typescript
// 首先添加一个空行使文件进入可编辑状态
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:search_replace",  // 假设有此工具
  arguments: {
    path: "/path/to/file.ts",
    search: "import",
    replace: "\nimport"  // 添加空行
  }
})
```

**步骤 2: 然后使用 edit_file**

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/path/to/file.ts",
    code_edit: "...",
    instruction: "..."
  }
})
```

---

### 2. 占位符使用不当

#### 错误示例

```
Error: Unable to locate edit context
```

#### 原因分析

- 未使用 `// ... existing code ...` 占位符
- 占位符位置不正确
- 提供了过多或过少的上下文

#### 修复方法

**正确的占位符使用**:

```typescript
// ✅ 正确：使用占位符表示未更改的代码
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/path/to/file.ts",
    code_edit: `
function myFunction() {
  // ... existing code ...

  // 新增的代码
  const newVariable = 42;

  // ... existing code ...
}
`,
    instruction: "Add new variable declaration"
  }
})

// ❌ 错误：包含所有代码
code_edit: `
function myFunction() {
  const oldVar1 = 1;
  const oldVar2 = 2;
  const oldVar3 = 3;
  const newVariable = 42;  // 只需要添加这一行
  const oldVar4 = 4;
}
`
```

---

### 3. 大文件编辑失败

#### 错误示例

```
Error: File too large for edit_file tool
```

#### 原因分析

`edit_file` 工具对超过 2000 行的文件不适用。需要使用传统的搜索替换工具。

#### 修复方法

```typescript
// 对于 >2000 行的文件，使用搜索替换
// 注意：需要确认是否有 search_replace 工具
mcp__airis-mcp-gateway__airis-schema({
  tool: "morphllm:search_replace"  // 验证工具存在
})
```

---

### 4. 搜索路径错误

#### 错误示例

```
Error: repo_path must be an absolute path
```

#### 原因分析

`warpgrep_codebase_search` 工具要求 `repo_path` 必须是绝对路径。相对路径会导致错误。

#### 修复方法

```typescript
// ❌ 错误：相对路径
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "authentication logic",
    repo_path: "./src"  // 错误
  }
})

// ✅ 正确：绝对路径
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "authentication logic",
    repo_path: "/home/user/myapp/src"  // 正确
  }
})
```

---

## MorphLLM MCP 工具参考

### edit_file

**描述**: 主要的文件编辑工具 - 使用此工具积极编辑文件

**关键特性**:
- ⚡ 极快: 10,500+ tokens/sec
- 🎯 防止上下文污染: 无需读取整个文件
- ✅ 高准确率: 98% 成功率
- 📊 高效: 仅显示更改的行

**参数签名**:

```json
{
  "required": ["path", "code_edit", "instruction"],
  "properties": {
    "path": {
      "type": "string",
      "description": "文件路径"
    },
    "code_edit": {
      "type": "string",
      "description": "更改的行，最少上下文。使用 '// ... existing code ...' 占位符表示未更改的代码"
    },
    "instruction": {
      "type": "string",
      "description": "简短的第一人称单句指令，描述对文件的更改"
    },
    "dryRun": {
      "type": "boolean",
      "default": false,
      "description": "预览更改而不应用"
    }
  }
}
```

**占位符规则**:
- 始终使用 `// ... existing code ...` 表示未更改的代码块
- 添加描述性提示（可选）: `// ... keep auth logic ...`
- 保留精确缩进
- 包含足够的上下文以精确定位每个编辑
- 尽可能简洁
- 批量编辑同一文件的所有修改

**删除代码的方式**:
- 选项 1: 显示上下 1-2 行上下文，省略要删除的代码
- 选项 2: 明确标记: `// removed BlockName`

**使用示例**:

```typescript
// 示例 1: 添加新函数
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/home/user/myapp/src/utils.ts",
    code_edit: `
// ... existing code ...

export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}

// ... existing code ...
`,
    instruction: "Add formatDate utility function"
  }
})

// 示例 2: 修改现有函数
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/home/user/myapp/src/auth.ts",
    code_edit: `
async function login(username: string, password: string) {
  // ... existing validation code ...

  // 添加速率限制
  await rateLimiter.check(username);

  // ... existing authentication code ...
}
`,
    instruction: "Add rate limiting to login function"
  }
})

// 示例 3: 删除代码
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/home/user/myapp/src/config.ts",
    code_edit: `
export const config = {
  apiUrl: process.env.API_URL,
  // removed debugMode
  timeout: 5000,
};
`,
    instruction: "Remove debugMode from config"
  }
})

// 示例 4: 批量修改
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/home/user/myapp/src/api.ts",
    code_edit: `
// ... existing imports ...

import { logger } from './logger';

// ... existing code ...

export async function fetchData(url: string) {
  logger.info(\`Fetching: \${url}\`);  // 添加日志

  // ... existing fetch logic ...

  logger.info('Fetch completed');  // 添加日志
  return response;
}
`,
    instruction: "Add logging to fetchData function at entry and exit points"
  }
})

// 示例 5: 预览更改（dry run）
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/home/user/myapp/src/app.ts",
    code_edit: `
// ... existing code ...

const PORT = 4000;  // 从 3000 改为 4000

// ... existing code ...
`,
    instruction: "Change server port to 4000",
    dryRun: true  // 仅预览，不实际应用
  }
})
```

**性能对比**:

| 操作 | 传统方法 | edit_file | 提升 |
|------|---------|-----------|------|
| 读取大文件 | 2000+ tokens | 0 tokens | 100% |
| 编辑速度 | 慢 | 10,500+ tokens/sec | 10x+ |
| 上下文污染 | 高 | 低 | 显著改善 |
| 成功率 | 变化 | 98% | 稳定 |

**重要提示**:
- ⚠️ **Cursor 用户**: 必须先使用其他工具添加一个空行，使文件进入可编辑状态
- ⚠️ **大文件**: 超过 2000 行的文件使用传统搜索替换工具
- ✅ **优先使用**: 相比传统 Edit 工具，优先使用此工具

---

### warpgrep_codebase_search

**描述**: 代码库搜索子代理（用户称为 'WarpGrep'），基于请求探索代码库

**关键特性**:
- 🔍 并行 grep 和 readfile 调用
- 🎯 多轮搜索定位相关文件和行范围
- 🤖 智能子代理自动推理
- 📍 返回精确的文件和行范围

**参数签名**:

```json
{
  "required": ["search_string", "repo_path"],
  "properties": {
    "search_string": {
      "type": "string",
      "description": "搜索问题陈述，子代理将研究此问题"
    },
    "repo_path": {
      "type": "string",
      "description": "执行搜索的文件夹的绝对路径"
    }
  }
}
```

**何时使用**:
- ✅ **总是首先使用此工具**开始搜索
- 基于自然语言请求探索代码库
- 查找特定功能的实现位置
- 定位需要修改的相关代码

**搜索查询建议**:
- 使用有针对性的自然语言查询
- 包含上下文和目标
- 提供尽可能多的细节帮助子代理

**示例查询**:
- "Find where authentication requests are handled in the Express routes"
- "Modify the agentic rollout to use the new tokenizer and chat template"
- "Fix the bug where the user gets redirected from the /feed page"
- "Locate all database query functions that use raw SQL"
- "Find components that handle file uploads"

**使用示例**:

```typescript
// 示例 1: 查找认证逻辑
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "Find where user authentication and JWT token validation are handled in the API routes",
    repo_path: "/home/user/myapp/src"
  }
})

// 示例 2: 定位 Bug
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "Fix the bug where users get a 404 error when navigating to the profile page after login",
    repo_path: "/home/user/myapp"
  }
})

// 示例 3: 功能修改
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "Modify the email notification system to support HTML templates instead of plain text",
    repo_path: "/home/user/myapp/src/services"
  }
})

// 示例 4: 多仓库工作区（指定子文件夹）
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "Find all API endpoints that require admin privileges",
    repo_path: "/home/user/monorepo/packages/backend"  // 指定特定仓库
  }
})

// 示例 5: 数据库查询定位
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "Locate all database queries that fetch user profile data and check if they properly handle null values",
    repo_path: "/home/user/myapp/src/database"
  }
})
```

**结果处理**:
- ⚠️ **注意**: 子代理可能会犯错误，需要仔细评估结果的相关性
- ✅ 返回的文件和行范围可能是需要的**部分**，不一定是全部
- 🔍 如果需要，考虑使用传统搜索工具补充查找其余部分

**工作流建议**:

```
Step 1: 使用 warpgrep_codebase_search 初步定位
  → 获取相关文件列表和行范围

Step 2: 分析结果
  → 评估返回文件的相关性
  → 确定是否需要进一步搜索

Step 3: 补充搜索（如果需要）
  → 使用传统 grep 工具定位遗漏的部分

Step 4: 使用 edit_file 修改
  → 对定位的文件进行编辑
```

---

## 最佳实践

### 1. 编辑工作流

```
Step 1: 明确编辑目标
  - 确定需要修改的功能
  - 列出具体的更改点

Step 2: 使用 warpgrep 定位代码
  - 编写清晰的搜索查询
  - 获取文件路径和行范围

Step 3: 构建 code_edit
  - 使用 // ... existing code ... 占位符
  - 仅包含更改的行和最少上下文
  - 保持精确缩进

Step 4: 执行 edit_file
  - 提供简洁的 instruction
  - 批量编辑同一文件的所有更改

Step 5: 验证（可选）
  - 先使用 dryRun: true 预览
  - 确认无误后应用更改
```

### 2. 占位符使用模式

**基本模式**:
```typescript
// ... existing code ...
新代码
// ... existing code ...
```

**带提示的模式**:
```typescript
// ... keep imports ...
新导入
// ... keep function declarations ...
```

**删除模式**:
```typescript
函数开始
// removed oldFunction
函数结束
```

**批量修改模式**:
```typescript
// ... existing code ...
修改点 1
// ... existing code ...
修改点 2
// ... existing code ...
```

### 3. 搜索查询优化

**好的查询**:
- ✅ "Find where user authentication requests are handled and validated in Express routes"
- ✅ "Locate the database connection pooling configuration and check for memory leaks"
- ✅ "Fix the bug where the shopping cart total is calculated incorrectly when applying discount codes"

**不好的查询**:
- ❌ "authentication"（太宽泛）
- ❌ "find code"（无具体目标）
- ❌ "error"（需要更多上下文）

**查询结构建议**:
```
[动作] + [具体功能/组件] + [上下文/目的]

示例:
- 动作: Find, Locate, Modify, Fix
- 功能: user authentication, database queries, file uploads
- 上下文: in Express routes, for memory optimization, when user clicks submit
```

### 4. 多仓库工作区处理

```typescript
// 项目结构
/home/user/monorepo/
  ├── packages/frontend/
  ├── packages/backend/
  └── packages/shared/

// ❌ 错误：搜索整个 monorepo
repo_path: "/home/user/monorepo"  // 会搜索所有仓库

// ✅ 正确：指定特定仓库
repo_path: "/home/user/monorepo/packages/backend"  // 仅搜索 backend
```

---

## 常见问题 FAQ

### Q1: edit_file 和传统 Edit 工具有什么区别？

**答**:
- **速度**: edit_file 快 10 倍以上（10,500+ tokens/sec）
- **上下文**: edit_file 不读取整个文件，避免上下文污染
- **准确性**: 98% 成功率
- **推荐**: 优先使用 edit_file，除非文件 >2000 行

### Q2: 什么时候用 edit_file，什么时候用搜索替换？

**答**:
- **edit_file**: 文件 ≤ 2000 行，所有编辑场景
- **search_replace**: 文件 > 2000 行，或简单的全局替换

### Q3: 如何在 Cursor 中使用 edit_file？

**答**: 先用其他工具（如 search_replace）添加一个空行，使文件进入可编辑状态。

### Q4: warpgrep 返回的结果不准确怎么办？

**答**:
1. 评估返回结果的相关性
2. 使用传统搜索工具补充查找
3. 优化搜索查询，提供更多上下文

### Q5: 如何预览更改而不实际应用？

**答**: 使用 `dryRun: true` 参数：

```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/path/to/file.ts",
    code_edit: "...",
    instruction: "...",
    dryRun: true  // 仅预览
  }
})
```

### Q6: 可以批量编辑多个文件吗？

**答**: 不能在单次调用中编辑多个文件。需要对每个文件分别调用 `edit_file`。但可以在一次调用中批量编辑同一文件的多个位置。

---

## 调试技巧

### 1. 检查 MorphLLM MCP 服务器状态

```bash
# 查看服务器是否启动
curl -s http://localhost:9400/process/servers | jq '.servers[] | select(.name == "morphllm")'

# 查看工具列表
curl -s http://localhost:9400/process/tools?server=morphllm | jq '.tools[].name'
```

### 2. 验证路径参数

```bash
# 获取当前工作目录
pwd
# 输出: /home/user/myapp

# 构建绝对路径
file_path="$(pwd)/src/utils.ts"
repo_path="$(pwd)/src"
```

### 3. 调试编辑失败

```typescript
// 步骤 1: 使用 dryRun 预览
const preview = await mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:edit_file",
  arguments: {
    path: "/path/to/file.ts",
    code_edit: "...",
    instruction: "...",
    dryRun: true
  }
})

// 步骤 2: 检查预览输出
// 如果预览正确，移除 dryRun 应用更改
// 如果预览不正确，调整 code_edit
```

### 4. 搜索结果调试

```typescript
// 步骤 1: 使用 warpgrep 搜索
const results = await mcp__airis-mcp-gateway__airis-exec({
  tool: "morphllm:warpgrep_codebase_search",
  arguments: {
    search_string: "your search query",
    repo_path: "/absolute/path"
  }
})

// 步骤 2: 分析返回的文件和行范围
// 步骤 3: 如果结果不完整，使用传统搜索补充

// 示例：使用 Grep 工具补充
// Grep({ pattern: "specific_function", path: "/absolute/path" })
```

---

## 相关文档

- [AIRIS MCP Gateway README](../../README.md)
- [MorphLLM 官方文档](https://morphllm.com)
- [MorphLLM MCP GitHub](https://github.com/morphllm/mcp)

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0 | 2025-12-29 | 初始版本，记录 2 个工具的完整参数和使用模式 |

---

**维护者**: 自动从使用经验中提炼
**反馈**: 如发现新的使用问题，请更新本文档
