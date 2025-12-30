---
title: "MCP 工具参数陷阱速查"
description: "常见参数命名错误和正确用法的快速参考"
type: "API参考"
status: "完成"
priority: "高"
created_date: "2025-12-30"
last_updated: "2025-12-30"
related_documents:
  - "TROUBLESHOOTING.md"
  - "QUICK_REFERENCE.md"
  - "servers/SERENA.md"
related_code: []
---

# MCP 工具参数陷阱速查

**版本**: v1.0
**最后更新**: 2025-12-30
**目的**: 快速查询常见参数命名错误，避免 validation error

---

## 🎯 为什么需要这个文档？

**真实案例**（2025-12-30）:
```typescript
// ❌ 直觉性假设（错误但合理）
await airis-exec({
    tool: "serena:read_memory",
    arguments: { path: "project_overview" }
});

// 错误信息
Error: 1 validation error for applyArguments
memory_file_name
  Field required [type=missing]

// ✅ 正确用法（反直觉）
await airis-exec({
    tool: "serena:read_memory",
    arguments: { memory_file_name: "project_overview" }
});
```

**核心问题**: 各 MCP 服务器参数命名不统一，直觉性假设经常错误。

---

## 📋 高频参数陷阱（按 MCP 服务器分类）

### Serena MCP 服务器

#### 1. read_memory / write_memory

**常见错误**:
- `path` ❌
- `name` ❌
- `filename` ❌

**正确参数**:
- `memory_file_name` ✅ (必需)
- `content` ✅ (write_memory 必需)
- `max_answer_chars` (可选)

**正确用法**:
```typescript
// 读取记忆
await airis-exec({
    tool: "serena:read_memory",
    arguments: {
        memory_file_name: "project_overview"
    }
});

// 写入记忆
await airis-exec({
    tool: "serena:write_memory",
    arguments: {
        memory_file_name: "my_note",
        content: "# 笔记内容\n..."
    }
});
```

**验证方法**:
```typescript
const schema = await airis-schema({ tool: "serena:read_memory" });
console.log(schema.inputSchema.required);  // ["memory_file_name"]
```

---

#### 2. find_file

**常见错误**:
- `filename` + `path` ❌
- `name` + `directory` ❌

**正确参数**:
- `file_mask` ✅ (必需) - 文件名或通配符模式
- `relative_path` ✅ (必需) - 相对路径，"." 表示项目根目录

**正确用法**:
```typescript
// 查找所有 .md 文件
await airis-exec({
    tool: "serena:find_file",
    arguments: {
        file_mask: "*.md",
        relative_path: "."
    }
});

// 查找特定目录中的文件
await airis-exec({
    tool: "serena:find_file",
    arguments: {
        file_mask: "config.json",
        relative_path: "src/config"
    }
});
```

---

#### 3. find_symbol

**常见错误**:
- `name` ❌
- `symbol_name` ❌
- `class_name` ❌

**正确参数**:
- `name_path_pattern` ✅ (必需) - 符号路径模式
- `depth` (可选) - 获取子符号的深度
- `relative_path` (可选) - 限制搜索范围
- `include_body` (可选) - 是否包含源代码

**正确用法**:
```typescript
// 查找类定义
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name_path_pattern: "MyClass"
    }
});

// 查找类中的方法
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name_path_pattern: "MyClass/myMethod",
        depth: 1,
        relative_path: "src/services"
    }
});
```

---

### Magic MCP 服务器

#### 4. generate_ui

**常见错误**:
- `path` ❌
- `currentFile` ❌
- `file` ❌

**正确参数**:
- `absolutePathToCurrentFile` ✅ (必需) - **必须是绝对路径**
- `content` ✅ (必需) - 当前文件内容
- `prompt` ✅ (必需) - UI 生成提示

**正确用法**:
```typescript
await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
        absolutePathToCurrentFile: "/home/user/project/src/App.tsx",  // 绝对路径！
        content: "import React from 'react'...",
        prompt: "创建一个登录表单组件"
    }
});
```

**陷阱**: 参数名冗长且必须使用绝对路径，相对路径会失败。

---

### MorphLLM MCP 服务器

#### 5. query_codebase / get_file_content

**常见错误**:
- `path` ❌
- `project_path` ❌
- `directory` ❌

**正确参数**:
- `repo_path` ✅ (必需) - **必须是绝对路径**
- `query` ✅ (query_codebase 必需)
- `file_path` ✅ (get_file_content 必需)

**正确用法**:
```typescript
// 查询代码库
await airis-exec({
    tool: "morphllm:query_codebase",
    arguments: {
        repo_path: "/home/user/my-project",  // 绝对路径！
        query: "如何实现用户认证？"
    }
});

// 获取文件内容
await airis-exec({
    tool: "morphllm:get_file_content",
    arguments: {
        repo_path: "/home/user/my-project",
        file_path: "src/auth/login.ts"
    }
});
```

**陷阱**:
- `repo_path` 必须是绝对路径
- 文件大小限制：< 2000 行

---

### AIRIS Agent MCP 服务器

#### 6. index_repository

**常见错误**:
- `path` ❌
- `project_path` ❌

**正确参数**:
- `repo_path` ✅ (必需) - **必须是绝对路径**

**正确用法**:
```typescript
await airis-exec({
    tool: "airis-agent:index_repository",
    arguments: {
        repo_path: "/home/user/my-project"  // 绝对路径！
    }
});
```

---

### Memory MCP 服务器

#### 7. remember

**常见错误**:
- `text` ❌
- `content` ❌
- `message` ❌

**正确参数**:
- `observations` ✅ (必需) - 观察内容数组

**正确用法**:
```typescript
await airis-exec({
    tool: "memory:remember",
    arguments: {
        observations: [
            "用户偏好使用 TypeScript",
            "项目使用 React 18"
        ]
    }
});
```

**陷阱**: 必须是数组，不能是字符串。

---

### Playwright MCP 服务器

#### 8. navigate / wait

**常见错误**:
- `timeout_ms` ❌
- `waitFor` ❌
- `wait_condition` ❌

**正确参数**:
- `wait_until` ✅ (可选) - 严格值匹配：`"load"`, `"domcontentloaded"`, `"networkidle"`
- `timeout` (可选) - 超时时间（毫秒）

**正确用法**:
```typescript
await airis-exec({
    tool: "playwright:navigate",
    arguments: {
        url: "https://example.com",
        wait_until: "networkidle"  // 必须是精确值
    }
});
```

---

### Mindbase MCP 服务器（对比参考）

#### 9. memory_read / memory_write

**Mindbase 使用简洁命名**（与 Serena 对比）:

| 操作 | Serena | Mindbase |
|------|--------|----------|
| 读取记忆 | `memory_file_name` | `name` ✅ |
| 写入记忆 | `memory_file_name` + `content` | `name` + `content` ✅ |

**正确用法**:
```typescript
// Mindbase 读取（简洁）
await airis-exec({
    tool: "mindbase:memory_read",
    arguments: {
        name: "project_overview"  // 简单！
    }
});

// Serena 读取（冗长）
await airis-exec({
    tool: "serena:read_memory",
    arguments: {
        memory_file_name: "project_overview"  // 更长
    }
});
```

---

## 🔍 快速诊断流程

### 当你遇到 validation error 时

**Step 1: 使用 airis-schema 查看正确参数**
```typescript
const schema = await airis-schema({ tool: "serena:read_memory" });
console.log("必需参数:", schema.inputSchema.required);
console.log("所有参数:", Object.keys(schema.inputSchema.properties));
```

**Step 2: 对比你的参数名**
```typescript
// 你的参数
const myArgs = { path: "..." };

// 正确参数（从 schema 获取）
const correctParams = schema.inputSchema.required;  // ["memory_file_name"]

// 检查差异
console.log("你使用的参数:", Object.keys(myArgs));
console.log("正确的参数:", correctParams);
```

**Step 3: 修正并重试**
```typescript
// 修正参数名
const correctArgs = { memory_file_name: "..." };

await airis-exec({
    tool: "serena:read_memory",
    arguments: correctArgs
});
```

---

## 💡 防止参数陷阱的最佳实践

### 实践 1: 总是先用 airis-schema 验证

```typescript
// ✅ 好习惯：先查看 schema
async function callToolSafely(toolName: string, args: any) {
    // 1. 获取 schema
    const schema = await airis-schema({ tool: toolName });
    const required = schema.inputSchema.required || [];

    // 2. 验证参数
    for (const param of required) {
        if (!(param in args)) {
            throw new Error(
                `缺少必需参数: ${param}\n` +
                `你提供的: ${Object.keys(args).join(", ")}\n` +
                `正确参数: ${required.join(", ")}`
            );
        }
    }

    // 3. 执行工具
    return await airis-exec({ tool: toolName, arguments: args });
}
```

### 实践 2: 维护个人参数映射表

```typescript
// 创建快速查询表
const MY_TOOL_PARAMS = {
    "serena:read_memory": ["memory_file_name"],
    "serena:write_memory": ["memory_file_name", "content"],
    "serena:find_file": ["file_mask", "relative_path"],
    "magic:generate_ui": ["absolutePathToCurrentFile", "content", "prompt"],
    "morphllm:query_codebase": ["repo_path", "query"],
    "airis-agent:index_repository": ["repo_path"]
};

// 使用前查询
function checkParams(toolName: string) {
    const params = MY_TOOL_PARAMS[toolName];
    if (params) {
        console.log(`📋 ${toolName} 需要的参数:`, params);
    }
}
```

### 实践 3: 建立"三步工作流"习惯

```typescript
// 标准工作流
async function standardWorkflow() {
    // Step 1: 发现工具
    const allTools = await airis-find({ query: "" });
    const tool = allTools.find(t => t.name === "serena:read_memory");

    // Step 2: 验证参数 ⭐ 关键步骤
    const schema = await airis-schema({ tool: "serena:read_memory" });
    console.log("必需参数:", schema.inputSchema.required);

    // Step 3: 执行工具
    await airis-exec({
        tool: "serena:read_memory",
        arguments: { memory_file_name: "..." }  // 使用正确的参数名
    });
}
```

---

### Sequential-Thinking MCP 服务器

#### create_thinking_session

**常见错误**:
- `name` ❌
- `title` ❌

**正确参数**:
- `topic` ✅ (必需) - 思考主题

**正确用法**:
```typescript
await airis-exec({
    tool: "sequential-thinking:create_thinking_session",
    arguments: {
        topic: "数据库性能优化方案"
    }
});
```

---

### Chrome-DevTools MCP 服务器

#### navigate

**常见错误**:
- `address` ❌
- `target` ❌

**正确参数**:
- `url` ✅ (必需) - 目标URL

**正确用法**:
```typescript
await airis-exec({
    tool: "chrome-devtools:navigate",
    arguments: {
        url: "https://example.com"
    }
});
```

---

### AIRIS-Commands MCP 服务器

#### airis_config_set_enabled

**常见错误**:
- `name` ❌
- `server` ❌
- `enable` ❌ (单数)

**正确参数**:
- `server_name` ✅ (必需)
- `enabled` ✅ (必需) - 布尔值

**正确用法**:
```typescript
await airis-exec({
    tool: "airis-commands:airis_config_set_enabled",
    arguments: {
        server_name: "playwright",
        enabled: true
    }
});
```

---

### MindBase MCP 服务器 (Docker Gateway)

⚠️ **特别说明**: MindBase 不在 AIRIS Gateway 的 13 个 ProcessManager 管理的服务器中，而是由 **Docker Gateway** (airis-mcp-gateway-core) 专门管理。

#### store_memory

**常见错误**:
- `text` ❌
- `data` ❌

**正确参数**:
- `content` ✅ (必需)
- `metadata` (可选)

**正确用法**:
```typescript
await airis-exec({
    tool: "mindbase:store_memory",
    arguments: {
        content: "记忆内容"
    }
});
```

---

### Time MCP 服务器 (Docker Gateway)

⚠️ **特别说明**: Time 不在 AIRIS Gateway 的 13 个 ProcessManager 管理的服务器中，而是由 **Docker Gateway** 内置支持。

#### get_current_time

**常见错误**:
- `tz` ❌
- `zone` ❌
- `time_zone` ❌ (下划线)

**正确参数**:
- `timezone` ✅ (必需) - IANA 时区名

**正确用法**:
```typescript
await airis-exec({
    tool: "time:get_current_time",
    arguments: {
        timezone: "America/New_York"  // IANA 格式
    }
});
```

---

## 🎓 参数命名模式总结

### 常见模式分类

| 命名模式 | 示例工具 | 参数风格 |
|---------|---------|---------|
| **简洁派** | Mindbase (外部) | `name`, `content` |
| **描述派** | Serena | `memory_file_name`, `name_path_pattern` |
| **冗长派** | Magic | `absolutePathToCurrentFile` |
| **统一派** | MorphLLM, AIRIS Agent | `repo_path` (一致使用) |

**注意**: Mindbase 不在 AIRIS Gateway 的 13 个 ProcessManager 管理的服务器中，而是由 Docker Gateway (airis-mcp-gateway-core) 专门管理。本文档包含 Mindbase 仅作为参数命名模式的对比参考。

### 参数命名规律

1. **文件/路径相关**:
   - 简洁: `path`, `filename`
   - 描述: `file_mask`, `relative_path`
   - 冗长: `absolutePathToCurrentFile`

2. **内容/数据相关**:
   - 统一: `content` (大多数服务器)
   - 特殊: `observations` (Memory)

3. **查询/搜索相关**:
   - 简洁: `query`, `name`
   - 描述: `name_path_pattern`

---

## 📞 获取更多帮助

### 相关文档

- **TROUBLESHOOTING.md** - 完整故障排查指南
- **QUICK_REFERENCE.md** - 常用工具快速参考
- **servers/SERENA.md** - Serena 服务器详细文档

### 报告新陷阱

如果发现本文档未覆盖的参数陷阱，请：

1. 使用 `airis-schema` 验证正确参数
2. 记录错误参数和正确参数
3. 提交 PR 更新本文档

---

**维护说明**: 本文档根据实际使用经验持续更新
**最后验证**: 2025-12-30
**贡献者**: 基于真实错误案例整理
