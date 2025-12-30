---
title: "AIRIS MCP Gateway 文档迁移总结"
description: "记录从源仓库到知识库的文档迁移过程"
type: "系统集成"
status: "完成"
priority: "低"
created_date: "2025-12-29"
last_updated: "2025-12-31"
related_documents:
  - path: "README.md"
    type: "迁移结果"
    description: "迁移后的主要文档"
  - path: "servers/"
    type: "迁移结果"
    description: "迁移后的服务器文档"
related_code: []
tags: ["migration", "documentation", "history"]
---

# AIRIS MCP Gateway 文档迁移总结

**迁移日期**: 2025-12-29
**版本**: v1.0
**状态**: 已完成

---

## 📊 迁移概览

从 `/home/hao/Downloads/airis-mcp-gateway` 前四个 commit 中的 MCP 使用指南完整迁移到本知识库。

### 迁移来源 Commits

| Commit | 日期 | 说明 |
|--------|------|------|
| `f6548eab` | 2025-12-29 | docs: enhance MCP usage notes with system-level optimization (v2.0) |
| `da29de59` | 2025-12-29 | docs: add 3 more MCP server documentation |
| `023796e4` | 2025-12-29 | docs: complete MCP server documentation (10/10 servers) |
| `071835a7` | 2025-12-29 | feat: complete MindBase verification with Ollama integration |

---

## 🎯 迁移内容

### 核心文档 (3 个)

| 文档 | 行数 | 说明 |
|------|------|------|
| [README.md](docs/airis-mcp-gateway/README.md) | ~520 | AIRIS MCP Gateway 完整使用指南 |
| [QUICK_REFERENCE.md](docs/airis-mcp-gateway/QUICK_REFERENCE.md) | ~380 | 快速参考和常用工具速查 |
| [TOOL_INDEX.md](docs/airis-mcp-gateway/TOOL_INDEX.md) | ~710 | 112 个工具完整索引 |

### 服务器文档 (8 个)

| 服务器 | 文档大小 | 工具数 | 模式 |
|--------|---------|--------|------|
| **Serena** | 6.1K | 23 | COLD |
| **Memory** | 13K | 9 | HOT |
| **Tavily** | 15K | 4 | COLD |
| **Playwright** | 16K | 22 | COLD |
| **Context7** | 8.0K | 2 | COLD |
| **Magic** | 15K | 3 | COLD |
| **MorphLLM** | 16K | 4 | COLD |
| **Fetch** | 11K | 1 | COLD |

**总计**: ~100K 文档，覆盖 68 个工具（占总工具数 112 的 61%）

---

## 📂 文档结构

```
docs/airis-mcp-gateway/
├── README.md                    # 主入口文档
├── QUICK_REFERENCE.md           # 快速参考
├── TOOL_INDEX.md                # 工具索引
└── servers/                     # 服务器详细文档
    ├── SERENA.md
    ├── MEMORY.md
    ├── TAVILY.md
    ├── PLAYWRIGHT.md
    ├── CONTEXT7.md
    ├── MAGIC.md
    ├── MORPHLLM.md
    └── FETCH.md
```

---

## 🔗 知识库集成

### 更新的文件

1. **KNOWLEDGE.md** - 添加 AIRIS MCP Gateway 专节
   - 新增"AIRIS MCP Gateway 集成"章节
   - 更新统计数据：+11 个文档

2. **CLAUDE.md** - 更新 MCP 集成卡片
   - 添加两种集成方式对比
   - 添加快速参考链接

3. **新建目录结构**
   - `docs/airis-mcp-gateway/` - 主目录
   - `docs/airis-mcp-gateway/servers/` - 服务器文档目录

---

## ✅ 核心特性

### 1. 三步工作流

所有 MCP 工具遵循统一的使用流程：

```typescript
// Step 1: 发现工具
airis-find(query: "keyword")

// Step 2: 查看参数
airis-schema(tool: "server:tool_name")

// Step 3: 执行工具
airis-exec(tool: "server:tool_name", arguments: {...})
```

### 2. HOT/COLD 模式优化

- **HOT 模式** (4 个服务器): 常驻内存，立即响应
  - airis-agent, memory, gateway-control, airis-commands
  - 35 个工具

- **COLD 模式** (9 个服务器): 按需启动，首次 2-5 秒
  - serena, playwright, tavily, context7, morphllm, magic, chrome-devtools, fetch, sequential-thinking
  - 77 个工具

### 3. 完整的错误参考

- 参数错误速查表
- 环境配置错误指南
- 使用模式错误说明
- 每个服务器的常见问题 FAQ

---

## 📚 使用场景覆盖

| 场景 | MCP 服务器 | 文档位置 |
|------|-----------|---------|
| **代码理解** | Serena, MorphLLM | [servers/SERENA.md](docs/airis-mcp-gateway/servers/SERENA.md) |
| **浏览器自动化** | Playwright | [servers/PLAYWRIGHT.md](docs/airis-mcp-gateway/servers/PLAYWRIGHT.md) |
| **Web 搜索** | Tavily, Fetch | [servers/TAVILY.md](docs/airis-mcp-gateway/servers/TAVILY.md) |
| **知识管理** | Memory, Serena | [servers/MEMORY.md](docs/airis-mcp-gateway/servers/MEMORY.md) |
| **文档查询** | Context7 | [servers/CONTEXT7.md](docs/airis-mcp-gateway/servers/CONTEXT7.md) |
| **UI 生成** | Magic | [servers/MAGIC.md](docs/airis-mcp-gateway/servers/MAGIC.md) |
| **代码编辑** | MorphLLM | [servers/MORPHLLM.md](docs/airis-mcp-gateway/servers/MORPHLLM.md) |

---

## ⚠️ 关键注意事项

### Claude Code 使用时的常见陷阱

1. **Serena MCP** - 参数名称不匹配
   - ❌ `filename` → ✅ `memory_file_name`
   - 解决: 使用 `airis-schema` 查询正确参数名

2. **Magic MCP** - 路径类型错误
   - ❌ 相对路径 → ✅ 绝对路径
   - 解决: 使用 `absolutePathToCurrentFile`

3. **Memory MCP** - 缺少必需参数
   - ❌ 未提供 `observations` → ✅ 必须提供数组
   - 解决: 检查 schema 的 `required` 字段

4. **Context7 MCP** - 参数格式错误
   - ❌ 库名称 → ✅ 库 ID
   - 解决: 先调用 `resolve-library-id`

---

## 🔍 验证清单

### 文档完整性

- [x] 所有核心文档已迁移 (README, QUICK_REFERENCE, TOOL_INDEX)
- [x] 8 个最常用服务器文档已复制
- [x] 知识库索引已更新 (KNOWLEDGE.md, CLAUDE.md)
- [x] 文档结构清晰，易于导航

### 内容准确性

- [x] 三步工作流示例可运行
- [x] 参数签名来自 `airis-schema` 验证
- [x] 常见错误来自实际测试
- [x] 工具数量和分类准确

### 集成完整性

- [x] 所有内部链接正确
- [x] 与现有 MCP 集成文档不冲突
- [x] 快速导航路径完整
- [x] 统计数据准确

---

## 📊 统计数据

### 迁移文档统计

| 指标 | 数量 |
|------|------|
| **核心文档** | 3 个 |
| **服务器文档** | 8 个 |
| **总文档量** | ~100K |
| **覆盖工具数** | 68 个 (61%) |
| **覆盖服务器数** | 8 个 (62%) |

### 知识库新增

| 类型 | 新增数量 |
|------|---------|
| **文档** | +11 个 |
| **目录** | +2 个 |
| **索引条目** | +13 个服务器 |
| **工具索引** | +112 个工具 |

---

## 🚀 后续工作

### 可选的补充文档 (剩余 5 个服务器)

如果需要，可以补充以下服务器的文档：

- **AIRIS Agent** (15 个工具, HOT) - 项目索引、代码生成
- **AIRIS Commands** (8 个工具, HOT) - 配置管理
- **AIRIS Gateway Control** (3 个工具, HOT) - 网关监控
- **Chrome DevTools** (17 个工具, COLD) - 浏览器调试
- **Sequential-thinking** (1 个工具, COLD) - 结构化推理

### 维护建议

1. **定期同步**: 当 airis-mcp-gateway 更新时，同步文档
2. **验证工具**: 定期使用 `airis-find` 验证工具可用性
3. **更新示例**: 根据实际使用经验更新最佳实践
4. **收集反馈**: 记录 Claude Code 使用时的问题和解决方案

---

## 📝 迁移决策记录

### 为什么迁移 AIRIS MCP Gateway 文档？

1. **统一访问**: 通过 Gateway 统一访问 13 个 MCP 服务器
2. **经验沉淀**: 文档包含真实的使用经验和错误解决方案
3. **知识集中**: 将 MCP 使用知识集中到本知识库
4. **SuperClaude 集成**: 确保 Claude Code 能正常使用所有 MCP 工具

### 为什么选择这 8 个服务器？

1. **使用频率**: 最常用的服务器优先
2. **功能覆盖**: 覆盖主要使用场景（代码、Web、浏览器、知识）
3. **文档质量**: 包含完整的参数签名和错误解决方案
4. **工具数量**: 覆盖 61% 的工具数量

---

## 🔗 相关资源

- **源仓库**: /home/hao/Downloads/airis-mcp-gateway
- **迁移目标**: docs/airis-mcp-gateway/
- **知识库入口**: [CLAUDE.md](CLAUDE.md)
- **完整索引**: [KNOWLEDGE.md](KNOWLEDGE.md)

---

**迁移完成**: 2025-12-29
**验证状态**: ✅ 通过
**维护状态**: 持续更新中
