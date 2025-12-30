---
title: "AIRIS MCP Gateway 快速入门指南"
description: "5-10 分钟快速上手 AIRIS MCP Gateway，从安装到第一个工具调用"
type: "教程"
status: "完成"
priority: "高"
created_date: "2025-12-30"
last_updated: "2025-12-30"
related_documents:
  - "docs/airis-mcp-gateway/README.md"
  - "docs/airis-mcp-gateway/QUICK_REFERENCE.md"
  - "docs/airis-mcp-gateway/TROUBLESHOOTING.md"
related_code: []
---

# AIRIS MCP Gateway 快速入门指南

**目标**: 5-10 分钟内完成安装、注册和第一个工具调用

**适用人群**: 从未使用过 AIRIS MCP Gateway 的 Claude Code 用户

---

## 🎯 学习目标

完成本指南后，你将能够：

- ✅ 安装并启动 AIRIS MCP Gateway
- ✅ 将 Gateway 注册到 Claude Code
- ✅ 验证安装成功
- ✅ 使用三步工作流调用第一个 MCP 工具

**预计时间**: 5-10 分钟

---

## 📋 前提条件

在开始之前，请确保你有：

- [ ] **Docker 和 Docker Compose** 已安装
- [ ] **Claude Code CLI** 已安装
- [ ] **Internet 连接**（用于下载依赖）
- [ ] **端口 9400 可用**（Gateway 默认端口）

**验证方法**:

```bash
# 检查 Docker
docker --version    # 应显示版本号

# 检查 Docker Compose
docker compose version

# 检查 Claude Code
claude --version

# 检查端口占用
lsof -i :9400      # 应显示无结果（端口未被占用）
```

---

## 🚀 第一步：安装 AIRIS MCP Gateway

### 1.1 克隆仓库

```bash
# 克隆官方仓库
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git

# 进入目录
cd airis-mcp-gateway
```

### 1.2 启动 Docker 容器

```bash
# 后台启动所有服务
docker compose up -d

# 预期输出：
# [+] Running 3/3
#  ✔ Container airis-mcp-gateway-db      Started
#  ✔ Container airis-mcp-gateway-api     Started
#  ✔ Container airis-mcp-gateway-serena  Started
```

**⏱️ 预计时间**: 1-2 分钟（首次启动需下载 Docker 镜像）

### 1.3 验证容器运行

```bash
# 检查容器状态
docker ps | grep airis-mcp-gateway

# 预期输出：
# airis-mcp-gateway-api      Up 10 seconds   0.0.0.0:9400->9400/tcp
# airis-mcp-gateway-db       Up 10 seconds   5432/tcp
# airis-mcp-gateway-serena   Up 10 seconds   8000/tcp
```

**✅ 成功标准**: 所有容器状态为 "Up"

---

## 🔗 第二步：注册到 Claude Code

### 2.1 注册 Gateway

```bash
# 使用 SSE 传输协议注册
claude mcp add --scope user --transport sse airis-mcp-gateway http://localhost:9400/sse
```

**预期输出**:
```
✓ MCP server 'airis-mcp-gateway' added successfully
```

### 2.2 验证注册

```bash
# 列出所有已注册的 MCP 服务器
claude mcp list

# 预期输出应包含：
# - airis-mcp-gateway (http://localhost:9400/sse)
```

**✅ 成功标准**: `claude mcp list` 显示 airis-mcp-gateway

---

## ✅ 第三步：验证安装

### 3.1 健康检查（命令行）

```bash
# 检查 Gateway API 状态
curl -s http://localhost:9400/api/tools/status | jq '.roster.summary'

# 预期输出：
# {
#   "hot_count": 4,
#   "cold_count": 9,
#   "total_enabled": 13
# }
```

**✅ 成功标准**: 返回 JSON 数据，`total_enabled >= 13`

### 3.2 健康检查（Claude Code）

启动 Claude Code 并发送：

```
请列出所有可用的 MCP 工具
```

**预期行为**:
- Claude 应该能够列出 `airis-find`, `airis-schema`, `airis-exec` 这三个工具
- 如果使用 Dynamic MCP 模式（默认），只会看到这 3 个工具

**✅ 成功标准**: Claude Code 能够响应并列出工具

---

## 🎯 第四步：第一个工具调用

现在让我们使用三步工作流调用第一个 MCP 工具。

### 4.1 发现工具（Step 1: airis-find）

在 Claude Code 中：

```
请使用 airis-find 工具搜索 "memory" 相关的工具
```

**Claude 的行为**:
```typescript
mcp__airis-mcp-gateway__airis-find({
  query: "memory"
})
```

**预期结果**:
```
找到以下 memory 相关工具：
- memory:create_entities
- memory:search_entities
- serena:write_memory
- serena:read_memory
- serena:list_memories
```

### 4.2 查看参数（Step 2: airis-schema）

继续在 Claude Code 中：

```
请使用 airis-schema 查看 serena:list_memories 工具的参数
```

**Claude 的行为**:
```typescript
mcp__airis-mcp-gateway__airis-schema({
  tool: "serena:list_memories"
})
```

**预期结果**:
```
serena:list_memories 工具参数：
- 无需参数
```

### 4.3 执行工具（Step 3: airis-exec）

最后在 Claude Code 中：

```
请使用 airis-exec 调用 serena:list_memories 列出所有记忆
```

**Claude 的行为**:
```typescript
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:list_memories",
  arguments: {}
})
```

**预期结果**:
```
记忆列表：
- project_overview
- tech_stack
- code_style_conventions
- (其他记忆...)
```

**🎉 恭喜！你已成功完成第一个 MCP 工具调用！**

---

## 📚 下一步学习

完成快速入门后，推荐你继续学习：

### 基础进阶
1. **[README.md](README.md)** - 了解 AIRIS MCP Gateway 的完整功能
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 常用工具和参数速查
3. **[TOOL_INDEX.md](TOOL_INDEX.md)** - 所有 112 个工具的完整列表

### 避免常见问题
4. **[PARAMETER_TRAPS.md](PARAMETER_TRAPS.md)** - 参数命名陷阱和正确用法
5. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - 故障排查和常见问题

### 实际应用
6. **服务器文档** - 查看 `docs/airis-mcp-gateway/servers/` 了解各个 MCP 服务器的详细用法

---

## 🛠️ 常见问题（FAQ）

### Q1: Gateway 启动失败怎么办？

**问题**: `docker compose up -d` 失败

**排查步骤**:
```bash
# 1. 查看日志
docker compose logs api

# 2. 检查端口占用
lsof -i :9400

# 3. 重新启动
docker compose down
docker compose up -d
```

**详细排查**: [TROUBLESHOOTING.md - 问题 1](TROUBLESHOOTING.md#问题-1-gateway-启动失败)

### Q2: Claude Code 无法连接到 Gateway

**问题**: Claude Code 提示连接错误

**排查步骤**:
```bash
# 1. 验证 Gateway 健康状态
curl http://localhost:9400/api/tools/status

# 2. 重新注册
claude mcp remove airis-mcp-gateway
claude mcp add --scope user --transport sse airis-mcp-gateway http://localhost:9400/sse

# 3. 重启 Claude Code
```

**详细排查**: [TROUBLESHOOTING.md - 问题 2](TROUBLESHOOTING.md#问题-2-claude-code-无法连接)

### Q3: 工具调用返回参数错误

**问题**: 调用工具时提示参数验证错误

**解决方案**:
- ✅ **总是使用 airis-schema 验证参数**
- ✅ **查阅 [PARAMETER_TRAPS.md](PARAMETER_TRAPS.md)** 避免常见参数命名错误
- ✅ **遵循三步工作流**: airis-find → airis-schema → airis-exec

**详细排查**: [TROUBLESHOOTING.md - 问题 5](TROUBLESHOOTING.md#问题-5-参数验证错误)

### Q4: COLD 模式服务器第一次调用很慢

**问题**: 调用 playwright 或 tavily 等工具需要等待 10+ 秒

**原因**: COLD 模式服务器按需启动

**解决方案**:
- 这是正常行为
- 后续调用会快很多（服务器保持运行）
- 如需常驻，可在 `mcp-config.json` 中将 `mode` 改为 `hot`

**了解更多**: [README.md - HOT vs COLD 模式](README.md#hot-vs-cold-模式)

---

## 🎓 三步工作流的重要性

**为什么总是使用三步工作流？**

| 步骤 | 工具 | 作用 | 跳过的后果 |
|------|------|------|-----------|
| 1️⃣ | airis-find | 发现工具 | 不知道有哪些工具可用 |
| 2️⃣ | airis-schema | 查看参数 | 🔴 90% 的参数错误都因跳过此步 |
| 3️⃣ | airis-exec | 执行工具 | - |

**最佳实践**:
```typescript
// ❌ 错误：直接猜测参数
airis-exec({
  tool: "serena:read_memory",
  arguments: { path: "project_overview" }  // 错误！应该是 memory_file_name
})

// ✅ 正确：先用 airis-schema 验证
airis-schema({ tool: "serena:read_memory" })
// → 返回: memory_file_name (必需)

airis-exec({
  tool: "serena:read_memory",
  arguments: { memory_file_name: "project_overview" }  // 正确！
})
```

---

## 📝 快速参考卡片

### 安装命令速查

```bash
# 克隆并启动
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
docker compose up -d

# 注册到 Claude Code
claude mcp add --scope user --transport sse airis-mcp-gateway http://localhost:9400/sse

# 验证安装
curl -s http://localhost:9400/api/tools/status | jq '.roster.summary'
claude mcp list
```

### 三步工作流速查

```typescript
// Step 1: 发现工具
airis-find({ query: "关键词" })

// Step 2: 查看参数
airis-schema({ tool: "server:tool_name" })

// Step 3: 执行工具
airis-exec({
  tool: "server:tool_name",
  arguments: { /* 使用 schema 返回的正确参数名 */ }
})
```

### 常用诊断命令

```bash
# 检查容器状态
docker ps | grep airis-mcp-gateway

# 查看日志
docker compose logs -f api

# 重启 Gateway
docker compose restart api

# 完全重启（清理状态）
docker compose down
docker compose up -d
```

---

## ✅ 检查清单

在进入下一步之前，确认以下项目：

- [ ] Docker 容器运行正常（`docker ps` 显示 3 个容器 Up）
- [ ] Gateway 健康检查通过（`curl http://localhost:9400/api/tools/status` 返回 JSON）
- [ ] Claude Code 成功注册 Gateway（`claude mcp list` 显示 airis-mcp-gateway）
- [ ] 能够在 Claude Code 中列出 MCP 工具
- [ ] 成功完成一次三步工作流调用
- [ ] 理解三步工作流的重要性（尤其是 Step 2: airis-schema）

**如果所有项目都 ✅，恭喜你已成功入门 AIRIS MCP Gateway！**

---

**下一步**: 查看 [README.md](README.md) 了解更多功能和配置选项

**遇到问题**: 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 获取帮助

**最后更新**: 2025-12-30
**版本**: v1.0
