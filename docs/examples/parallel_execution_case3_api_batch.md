---
title: "案例3: API 端点批量修改"
description: "统一10个REST API端点错误处理和响应格式的分批并行执行案例"
type: "示例文档"
status: "完成"
priority: "中"
created_date: "2025-12-03"
last_updated: "2025-12-07"
related_documents:
  - "wf_05_code.md"
  - "docs/examples/parallel_execution_overview.md"
tags: ["并行执行", "代码实现", "API标准化", "批量修改", "实战案例"]
---

# 案例3: API 端点批量修改

**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07

## 📋 目录

- [场景描述](#场景描述)
- [并行执行方案](#并行执行方案)
- [性能对比](#性能对比)

---

## 场景描述

**任务**: 统一修改10个 REST API 端点的错误处理和响应格式

**问题**:
- 10个端点分散在5个路由文件中
- 每个端点需要：统一错误格式、添加 HTTP 状态码、标准化响应结构
- 顺序执行预计需要 90 分钟

---

## 并行执行方案

### Wave 1: 批量读取路由文件（12秒）

```javascript
// 分3批并行读取（避免单次读取过多）
Batch 1: [
  Read("routes/auth.js"),
  Read("routes/users.js")
]

Batch 2: [
  Read("routes/posts.js"),
  Read("routes/comments.js")
]

Batch 3: [
  Read("routes/settings.js")
]

// 识别到的10个端点
auth.js: POST /login, POST /register
users.js: GET /users/:id, PUT /users/:id, DELETE /users/:id
posts.js: GET /posts, POST /posts, GET /posts/:id
comments.js: POST /posts/:id/comments, DELETE /comments/:id
```

### Checkpoint: 设计统一格式（顺序，8分钟）

```javascript
// 统一错误处理中间件
function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message,
      details: err.details || null
    },
    timestamp: new Date().toISOString()
  });
}

// 统一成功响应格式
function successResponse(data, message = 'Success') {
  return {
    success: true,
    data: data,
    message: message,
    timestamp: new Date().toISOString()
  };
}

// 修改策略
每个端点需要:
1. 移除旧的 try-catch
2. 使用新的 errorHandler
3. 包装响应为 successResponse 格式
4. 添加正确的 HTTP 状态码
```

**标准化示例（旧 vs 新）**:

```javascript
// 旧端点格式
router.get('/users/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    res.json(user);  // 直接返回数据
  } catch (error) {
    res.status(500).json({ error: error.message });  // 错误格式不一致
  }
});

// 新端点格式
router.get('/users/:id', async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      const error = new Error('User not found');
      error.statusCode = 404;
      error.code = 'USER_NOT_FOUND';
      throw error;
    }
    res.status(200).json(successResponse(user, 'User retrieved successfully'));
  } catch (error) {
    next(error);  // 交给统一错误处理中间件
  }
});

// 响应格式对比
旧响应: { id: 1, name: "Alice" }

新响应: {
  success: true,
  data: { id: 1, name: "Alice" },
  message: "User retrieved successfully",
  timestamp: "2025-12-07T10:00:00.000Z"
}
```

### Wave 2: 并行修改（分2个波次）

**Wave 2.1: 前5个端点（15秒）**

```javascript
[
  Edit("routes/auth.js", standardize_endpoints),      // 2个端点
  Edit("routes/users.js", standardize_endpoints),     // 3个端点
]
```

**auth.js 标准化示例**:

```javascript
// POST /login
router.post('/login', async (req, res, next) => {
  try {
    const { username, password } = req.body;

    // 验证输入
    if (!username || !password) {
      const error = new Error('Username and password required');
      error.statusCode = 400;
      error.code = 'MISSING_CREDENTIALS';
      throw error;
    }

    // 认证逻辑
    const user = await authenticate(username, password);
    if (!user) {
      const error = new Error('Invalid credentials');
      error.statusCode = 401;
      error.code = 'INVALID_CREDENTIALS';
      throw error;
    }

    const token = generateToken(user);
    res.status(200).json(successResponse(
      { token, user },
      'Login successful'
    ));
  } catch (error) {
    next(error);
  }
});

// POST /register
router.post('/register', async (req, res, next) => {
  try {
    const { email, password } = req.body;

    // 验证输入
    if (!email || !password) {
      const error = new Error('Email and password required');
      error.statusCode = 400;
      error.code = 'MISSING_FIELDS';
      throw error;
    }

    // 检查重复
    const exists = await User.findOne({ email });
    if (exists) {
      const error = new Error('Email already registered');
      error.statusCode = 409;
      error.code = 'EMAIL_EXISTS';
      throw error;
    }

    const user = await createUser({ email, password });
    res.status(201).json(successResponse(
      { user },
      'User registered successfully'
    ));
  } catch (error) {
    next(error);
  }
});
```

**Wave 2.2: 后5个端点（15秒）**

```javascript
[
  Edit("routes/posts.js", standardize_endpoints),     // 3个端点
  Edit("routes/comments.js", standardize_endpoints),  // 2个端点
]
```

### Wave 3: 创建中间件文件（5秒）

```javascript
Write("middleware/errorHandler.js", error_handler_code)
Write("utils/response.js", response_helper_code)
```

**middleware/errorHandler.js**:

```javascript
function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode || 500;

  // 日志记录
  console.error('[Error Handler]', {
    statusCode,
    code: err.code,
    message: err.message,
    path: req.path,
    method: req.method
  });

  res.status(statusCode).json({
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message,
      details: err.details || null
    },
    timestamp: new Date().toISOString()
  });
}

module.exports = errorHandler;
```

**utils/response.js**:

```javascript
function successResponse(data, message = 'Success') {
  return {
    success: true,
    data: data,
    message: message,
    timestamp: new Date().toISOString()
  };
}

function paginatedResponse(data, pagination) {
  return {
    success: true,
    data: data,
    pagination: {
      page: pagination.page,
      limit: pagination.limit,
      total: pagination.total
    },
    timestamp: new Date().toISOString()
  };
}

module.exports = { successResponse, paginatedResponse };
```

### Final: 集成测试（5分钟）

```
测试场景:
┌─────────────────────────────────────┐
│ Scenario 1: 成功请求                 │
│   - GET /users/1                    │
│   - 期望: 200 + successResponse     │
│   - 结果: ✅ Pass                    │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Scenario 2: 验证错误（400）          │
│   - POST /register (无效邮箱)        │
│   - 期望: 400 + error code          │
│   - 结果: ✅ Pass                    │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Scenario 3: 未找到资源（404）        │
│   - GET /users/99999                │
│   - 期望: 404 + NOT_FOUND           │
│   - 结果: ✅ Pass                    │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Scenario 4: 服务器错误（500）        │
│   - 模拟数据库连接失败               │
│   - 期望: 500 + INTERNAL_ERROR      │
│   - 结果: ✅ Pass                    │
└─────────────────────────────────────┘

总测试用例: 48 个
通过: 48 ✅
失败: 0 ❌
```

---

## 性能对比

| 指标 | 顺序执行 | 并行执行 | 提升 |
|------|---------|---------|------|
| 总时间 | 90 分钟 | 35 分钟 | 2.6x |
| 读取阶段 | 25s | 12s | 2.1x |
| 编辑阶段 | 50s | 30s | 1.7x |
| 端点修改数 | 10 | 10 | 相同 |

**关键成果**:
- 所有端点响应格式统一
- 错误处理标准化
- API 文档自动更新（基于新格式）
- 零回归问题

**技术亮点**:
- 分批读取避免超时
- 统一中间件简化维护
- 错误码体系化
- 响应格式一致性

---

## 相关资源

- **主命令文档**: [wf_05_code.md](../../wf_05_code.md)
- **并行执行概览**: [parallel_execution_overview.md](./parallel_execution_overview.md)
- **其他案例**:
  - [案例1: 多文件日志功能](./parallel_execution_case1_logging.md)
  - [案例2: 组件重构](./parallel_execution_case2_component_refactor.md)
  - [案例4: 测试套件更新](./parallel_execution_case4_test_update.md)
- **优化技巧**: [parallel_execution_tips.md](./parallel_execution_tips.md)

---

**维护者**: AI Workflow System
**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07
