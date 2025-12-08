---
title: "Agent 模式协调实战示例"
description: "wf_05_code 中 Agent 模式的完整实施案例和最佳实践"
type: "示例文档"
status: "完成"
priority: "中"
created_date: "2025-12-03"
last_updated: "2025-12-03"
related_documents:
  - "wf_05_code.md"
  - "docs/examples/parallel_execution_overview.md"
related_code: []
tags: ["Agent模式", "并行开发", "Phase2优化"]
authors: ["Claude"]
version: "1.0"
---

# Agent 模式协调实战示例

本文档提供 wf_05_code.md 中 Agent 模式协调策略的完整实施案例。

## 目录

- [Strategy 1: Explore-First Pattern（探索优先模式）](#strategy-1-explore-first-pattern)
- [Strategy 2: Parallel Development Pattern（并行开发模式）](#strategy-2-parallel-development-pattern)
- [Strategy 3: Sequential Agent Chain（顺序代理链模式）](#strategy-3-sequential-agent-chain)
- [常见问题和解决方案](#常见问题和解决方案)

---

## Strategy 1: Explore-First Pattern

### 案例 1: 添加用户认证功能到未知代码库

**场景**: 需要在一个中型 Node.js 项目中添加 JWT 认证，但不熟悉代码库结构。

**问题**:
- 代码库有 50+ 个文件
- 不清楚认证逻辑应该放在哪里
- 不知道现有的用户管理实现在哪里

**解决方案**: 使用 Explore-First Pattern

```bash
# 步骤 1: 启动 Explore Agent
/wf_05_code "在项目中添加 JWT 用户认证"

# AI 自动执行的 Agent 协调：
Step 1: Launch Explore Agent (thoroughness: "medium")
  Task: "探索代码库，定位用户管理和路由相关代码"
  Input:
    - Feature: "JWT authentication"
    - Path: "src/"

  Agent Output (3分钟后):
    ✅ 相关文件识别:
      - src/routes/users.js (用户路由)
      - src/models/User.js (用户模型)
      - src/middleware/ (中间件目录，当前为空)
      - src/config/database.js (数据库配置)

    ✅ 架构理解:
      - Express.js 框架
      - MongoDB 数据库
      - 现有路由结构: src/routes/*.js
      - 中间件模式: app.use() 在 src/app.js

    Token 节省: ~15,000 tokens (未读取其他 42 个无关文件)

Step 2: 基于探索结果实施 JWT 认证
  目标文件:
    - src/middleware/auth.js (新建)
    - src/routes/users.js (修改，添加 /login, /register)
    - src/models/User.js (修改，添加密码哈希)
    - package.json (添加 jsonwebtoken, bcrypt)
```

**成果**:
- 上下文加载时间: 10 分钟 → 3 分钟
- Token 消耗: 20,000 → 5,000 (75% 节省)
- 准确性: 100% (所有文件定位正确)

---

### 案例 2: 重构支付处理模块

**场景**: 现有支付模块性能差，需要重构，但代码分散在多个目录。

**问题**:
- 支付相关代码可能在 src/payments/, src/services/, src/models/ 等多处
- 有第三方库依赖，不清楚哪些文件引用了
- 不知道测试文件在哪里

**解决方案**: Explore-First + Comprehensive Analysis

```bash
/wf_05_code "重构支付处理模块，提升性能"

# Agent 协调流程：
Step 1: Explore Agent (thoroughness: "medium")
  Task: "识别所有支付相关代码和依赖"

  Output:
    支付核心文件:
      - src/payments/stripe.js (Stripe 集成)
      - src/payments/paypal.js (PayPal 集成)
      - src/services/PaymentService.js (支付服务)
      - src/models/Transaction.js (交易模型)

    依赖分析:
      - 8 个文件引用了 PaymentService
      - 3 个测试文件: tests/payments/*.test.js
      - 配置文件: config/payment.config.js

    Token 节省: ~18,000 tokens

Step 2: 重构实施
  Strategy: 渐进式重构
    Phase A: 抽象支付接口 (PaymentProvider)
    Phase B: 重构 Stripe 集成
    Phase C: 重构 PayPal 集成
    Phase D: 更新所有 8 个引用点
```

**成果**:
- 所有依赖识别准确
- 避免了遗漏文件导致的运行时错误
- 重构后性能提升 40%

---

## Strategy 2: Parallel Development Pattern

### 案例 3: 实现用户注册功能（完整流程）

**场景**: 从零实现用户注册，包括 API、数据库、测试和文档。

**问题**:
- 需要同时编写代码、测试和文档
- 顺序执行耗时长（估计 60 分钟）
- 希望加速开发流程

**解决方案**: Parallel Development Pattern (3 agents)

```bash
/wf_05_code "实现完整的用户注册功能"

# AI 自动启动 3 个并行 Agents:

┌─────────────────────────────────────────────────────────┐
│ Agent 1: Implementation Agent (并行运行)                │
├─────────────────────────────────────────────────────────┤
│ Task: 实现核心注册逻辑                                   │
│ Files to Create/Edit:                                   │
│   - src/routes/auth.js (POST /register)                │
│   - src/controllers/authController.js (registerUser)   │
│   - src/models/User.js (schema + validation)           │
│   - src/middleware/validation.js (input validation)    │
│                                                         │
│ Standards: PLANNING.md § 开发标准                       │
│ Duration: ~15 分钟                                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Agent 2: Test Agent (并行运行)                          │
├─────────────────────────────────────────────────────────┤
│ Task: 编写完整测试套件                                   │
│ Files to Create:                                        │
│   - tests/auth/register.test.js                        │
│     * 正常注册流程                                       │
│     * 重复邮箱验证                                       │
│     * 无效输入处理                                       │
│     * 密码强度检查                                       │
│                                                         │
│ Coverage Target: >90%                                   │
│ Duration: ~15 分钟                                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Agent 3: Documentation Agent (并行运行)                 │
├─────────────────────────────────────────────────────────┤
│ Task: 更新 API 文档和使用说明                            │
│ Files to Create/Edit:                                  │
│   - docs/api/authentication.md                         │
│     * POST /api/auth/register 端点说明                 │
│     * 请求/响应格式                                      │
│     * 错误代码说明                                       │
│   - README.md (添加注册功能说明)                        │
│                                                         │
│ Duration: ~15 分钟                                      │
└─────────────────────────────────────────────────────────┘

# 协调阶段 (所有 agents 完成后):
Step 4: Consistency Verification
  ✅ Agent 1 代码 ↔ Agent 2 测试: 接口一致
  ✅ Agent 1 代码 ↔ Agent 3 文档: 端点描述准确
  ✅ 所有测试通过
  ✅ 文档示例可运行

Step 5: Integration
  合并所有 agent 输出
  运行完整测试套件
  提交代码
```

**成果**:
- 开发时间: 60 分钟 → 18 分钟 (3.3x 提升)
- 代码质量: 更高（专业化分工）
- 文档同步: 自动完成，无遗漏
- 测试覆盖: 95% (超过目标)

---

### 案例 4: API 重构（10 个端点）

**场景**: 重构 REST API，统一错误处理和响应格式。

**问题**:
- 10 个端点分散在 5 个文件
- 需要同时更新代码、测试和文档
- 顺序执行估计 2 小时

**解决方案**: Parallel Development Pattern (扩展版)

```bash
/wf_05_code "重构 REST API 统一错误处理和响应格式"

# 3 个并行 Agents:
Agent 1 (Implementation):
  - 创建统一错误处理中间件
  - 创建标准响应格式工具函数
  - 重构 10 个端点使用新格式

Agent 2 (Test):
  - 更新所有端点的测试用例
  - 验证错误响应格式一致性
  - 添加边界情况测试

Agent 3 (Documentation):
  - 更新 API 文档的错误代码表
  - 更新所有端点的响应示例
  - 添加迁移指南

# 结果（40 分钟完成）:
  - 10 个端点全部重构 ✅
  - 83 个测试用例更新 ✅
  - 文档完全同步 ✅
  - 零回归问题 ✅
```

**成果**:
- 开发时间: 120 分钟 → 40 分钟 (3x 提升)
- 一致性: 100% (所有端点格式统一)
- 文档准确性: 100%

---

## Strategy 3: Sequential Agent Chain

### 案例 5: 新功能架构设计 → 实现 → 集成

**场景**: 实现复杂的实时通知系统，需要架构设计、核心实现、系统集成三个阶段。

**问题**:
- 三个阶段有依赖关系（设计 → 实现 → 集成）
- 不能并行执行
- 但每个阶段内部可以优化

**解决方案**: Sequential Agent Chain

```bash
/wf_05_code "实现实时通知系统"

# Sequential Chain:

┌─────────────────────────────────────────────────────────┐
│ Stage 1: Architect Agent                                │
├─────────────────────────────────────────────────────────┤
│ Task: 设计通知系统架构                                   │
│ Output:                                                 │
│   - 技术选型: WebSocket vs Server-Sent Events          │
│   - 组件设计:                                           │
│     * NotificationService (核心服务)                    │
│     * NotificationStore (持久化)                        │
│     * WebSocketServer (实时推送)                        │
│   - 数据模型: Notification schema                       │
│   - API 设计: 5 个端点定义                              │
│                                                         │
│ Duration: 20 分钟                                       │
└─────────────────────────────────────────────────────────┘
            ↓ (等待 Stage 1 完成)
┌─────────────────────────────────────────────────────────┐
│ Stage 2: Implementation Agent                           │
├─────────────────────────────────────────────────────────┤
│ Task: 实现核心组件（基于 Stage 1 设计）                  │
│ Input: Stage 1 的架构设计                                │
│ Files Created:                                          │
│   - src/services/NotificationService.js                │
│   - src/models/Notification.js                         │
│   - src/websocket/NotificationServer.js                │
│   - src/routes/notifications.js                        │
│                                                         │
│ Duration: 30 分钟                                       │
└─────────────────────────────────────────────────────────┘
            ↓ (等待 Stage 2 完成)
┌─────────────────────────────────────────────────────────┐
│ Stage 3: Integration Agent                              │
├─────────────────────────────────────────────────────────┤
│ Task: 集成到现有系统                                     │
│ Input: Stage 2 的实现代码                                │
│ Integration Points:                                     │
│   - app.js (初始化 WebSocket server)                    │
│   - 现有 API routes (触发通知)                          │
│   - 前端组件 (接收和显示通知)                            │
│   - 数据库迁移 (添加 notifications 表)                  │
│                                                         │
│ Duration: 25 分钟                                       │
└─────────────────────────────────────────────────────────┘

# 总耗时: 75 分钟（vs 顺序手工 150 分钟）
```

**成果**:
- 架构清晰，三阶段分离
- 每个阶段专注于特定目标
- 集成顺畅，无冲突
- 总时间节省 50%

---

### 案例 6: 数据库迁移（复杂重构）

**场景**: 从 MongoDB 迁移到 PostgreSQL，需要分阶段执行。

**问题**:
- 需要先设计新 schema
- 然后编写数据迁移脚本
- 最后更新应用代码
- 三个阶段严格顺序依赖

**解决方案**: Sequential Agent Chain (3 stages)

```bash
/wf_05_code "将数据库从 MongoDB 迁移到 PostgreSQL"

# Stage 1: Schema Design Agent
  Input: 现有 MongoDB schema
  Output: PostgreSQL schema 设计
    - SQL DDL 脚本
    - 索引策略
    - 关系定义

  ↓ (等待完成)

# Stage 2: Migration Script Agent
  Input: Stage 1 的 schema 设计
  Output: 数据迁移脚本
    - 提取 MongoDB 数据
    - 转换格式
    - 导入 PostgreSQL
    - 验证脚本

  ↓ (等待完成)

# Stage 3: Application Code Agent
  Input: Stage 2 的迁移结果
  Output: 更新应用代码
    - 替换 Mongoose → Sequelize
    - 更新所有查询逻辑
    - 更新测试用例
    - 更新配置

# 总耗时: 2 小时（vs 手工 5+ 小时）
```

**成果**:
- 迁移零数据丢失
- 应用功能 100% 兼容
- 性能提升 60%
- 开发时间节省 60%

---

## 常见问题和解决方案

### Q1: 何时使用 Explore-First vs Parallel Development？

**决策树**:
```
代码库熟悉度？
├─ 不熟悉 → Explore-First Pattern
│   └─ 先探索，再实施
│
└─ 熟悉 → Parallel Development Pattern
    └─ 直接并行开发
```

**示例**:
- 新加入项目 → Explore-First
- 自己的项目或熟悉的代码库 → Parallel Development

---

### Q2: Parallel Development 何时会失败？

**失败场景**:
1. **任务有隐藏依赖**
   - 问题: Agent 2 (Test) 需要 Agent 1 (Implementation) 的接口定义
   - 解决: 改用 Sequential Chain，或先设计接口

2. **文件冲突**
   - 问题: 两个 agent 同时修改同一文件
   - 解决: 明确分工，避免重叠

3. **简单任务过度使用**
   - 问题: 单文件修改也启动 3 个 agents
   - 解决: 简单任务直接实现，不用 agents

---

### Q3: 如何验证 Agent 输出的一致性？

**验证清单**:
```bash
# 在所有 agents 完成后执行：

1. 接口一致性检查
   ✅ Implementation 的 API ↔ Test 的测试用例
   ✅ Implementation 的 API ↔ Documentation 的端点说明

2. 运行测试
   bash test command
   ✅ 所有测试通过

3. 文档验证
   ✅ 文档中的示例可运行
   ✅ 错误代码与代码匹配

4. 代码审查
   /wf_08_review
```

---

### Q4: Sequential Chain 的最佳阶段数？

**推荐**:
- **2-3 个阶段**: 最佳（清晰且高效）
- **4-5 个阶段**: 可接受（复杂任务）
- **6+ 个阶段**: 避免（过度复杂，考虑拆分任务）

**示例**:
```
✅ 好的 3 阶段:
   Design → Implement → Integrate

❌ 过度的 7 阶段:
   Research → Design → Prototype → Implement → Test → Document → Deploy
   (建议拆分成 2-3 个独立任务)
```

---

## 性能对比总结

| Agent 模式 | 适用场景 | 时间节省 | 复杂度 |
|-----------|---------|---------|--------|
| **Explore-First** | 不熟悉代码库 | 50-70% | 低 |
| **Parallel Development** | 多维度开发 | 60-70% | 中 |
| **Sequential Chain** | 有依赖的阶段 | 40-50% | 高 |

---

## 下一步

- 阅读 [并行执行模式示例](./parallel_execution_overview.md) 了解 Wave→Checkpoint→Wave 模式
- 参考 wf_05_code.md 的完整 Agent 协调策略说明
- 实践：在下一个功能开发中尝试使用 Agent 模式

---

**相关文档**:
- [wf_05_code.md](../../wf_05_code.md) - 功能实现协调器
- [并行执行模式示例](./parallel_execution_overview.md)
- [PLANNING.md](../management/PLANNING.md) - 开发标准

**最后更新**: 2025-12-03
