---
title: "案例4: 测试套件更新"
description: "更新测试套件以匹配新API响应格式的并行执行实战案例"
type: "示例文档"
status: "完成"
priority: "中"
created_date: "2025-12-03"
last_updated: "2025-12-07"
related_documents:
  - "wf_05_code.md"
  - "docs/examples/parallel_execution_overview.md"
  - "docs/examples/parallel_execution_case3_api_batch.md"
tags: ["并行执行", "代码实现", "测试更新", "API测试", "实战案例"]
---

# 案例4: 测试套件更新

**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07

## 📋 目录

- [场景描述](#场景描述)
- [并行执行方案](#并行执行方案)
- [性能对比](#性能对比)

---

## 场景描述

**任务**: 更新整个测试套件以匹配新的 API 响应格式（来自案例3）

**问题**:
- 需要修改 8 个测试文件（覆盖所有端点）
- 每个测试需要：更新响应断言、修改 mock 数据、调整测试工具
- 顺序执行预计需要 75 分钟

---

## 并行执行方案

### Wave 1: 并行读取测试文件（10秒）

```javascript
[
  Read("tests/auth.test.js"),
  Read("tests/users.test.js"),
  Read("tests/posts.test.js"),
  Read("tests/comments.test.js"),
  Read("tests/integration/api.test.js"),
  Read("tests/helpers/mockData.js"),
  Read("tests/helpers/testUtils.js"),
  Read("jest.config.js")
]

// 识别测试覆盖
总测试用例数: 127
需要更新: 83 个（涉及 API 响应）
无需更新: 44 个（单元测试，不涉及 API）
```

### Checkpoint: 更新策略（顺序，10分钟）

```javascript
// 旧断言格式
expect(response.body).toHaveProperty('user');
expect(response.status).toBe(200);

// 新断言格式
expect(response.body).toMatchObject({
  success: true,
  data: expect.objectContaining({
    user: expect.any(Object)
  }),
  message: expect.any(String),
  timestamp: expect.any(String)
});
expect(response.status).toBe(200);

// Mock 数据更新策略
旧格式 mock:
  { id: 1, name: 'John', email: 'john@example.com' }

新格式 mock:
  {
    success: true,
    data: { id: 1, name: 'John', email: 'john@example.com' },
    message: 'User retrieved successfully',
    timestamp: '2025-12-03T10:00:00.000Z'
  }
```

**详细断言更新示例**:

```javascript
// 旧测试（直接响应）
it('should get user by id', async () => {
  const response = await request(app)
    .get('/users/1')
    .expect(200);

  expect(response.body).toHaveProperty('id', 1);
  expect(response.body).toHaveProperty('name');
  expect(response.body).toHaveProperty('email');
});

// 新测试（包装响应）
it('should get user by id', async () => {
  const response = await request(app)
    .get('/users/1')
    .expect(200);

  expect(response.body).toMatchObject({
    success: true,
    data: expect.objectContaining({
      id: 1,
      name: expect.any(String),
      email: expect.stringMatching(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)
    }),
    message: 'User retrieved successfully',
    timestamp: expect.any(String)
  });

  // 验证 timestamp 格式
  expect(new Date(response.body.timestamp).toString()).not.toBe('Invalid Date');
});
```

### Wave 2: 并行更新工具和 Mock（5秒）

```javascript
// 先更新共享的工具和 mock（被测试文件依赖）
[
  Edit("tests/helpers/mockData.js", update_mock_format),
  Edit("tests/helpers/testUtils.js", add_response_matchers)
]
```

**testUtils.js 新增匹配器**:

```javascript
// 原 testUtils.js（基础工具）
module.exports = {
  createTestServer,
  generateTestUser
};

// 新 testUtils.js（添加自定义匹配器）
expect.extend({
  toBeSuccessResponse(received) {
    const pass = received.success === true &&
                 typeof received.data !== 'undefined' &&
                 typeof received.timestamp === 'string';

    return {
      pass,
      message: () => pass
        ? 'Expected not to be a valid success response'
        : 'Expected a valid success response format'
    };
  },

  toBeErrorResponse(received, expectedCode) {
    const pass = received.success === false &&
                 received.error &&
                 received.error.code === expectedCode;

    return {
      pass,
      message: () => pass
        ? `Expected error code not to be ${expectedCode}`
        : `Expected error code ${expectedCode}, got ${received.error?.code}`
    };
  }
});

module.exports = {
  createTestServer,
  generateTestUser
};
```

**mockData.js 格式更新**:

```javascript
// 旧 mock 数据
const mockUser = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com'
};

const mockPost = {
  id: 1,
  title: 'Test Post',
  content: 'Test content'
};

// 新 mock 数据（包装格式）
const mockUserResponse = {
  success: true,
  data: {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com'
  },
  message: 'User retrieved successfully',
  timestamp: '2025-12-07T10:00:00.000Z'
};

const mockPostResponse = {
  success: true,
  data: {
    id: 1,
    title: 'Test Post',
    content: 'Test content'
  },
  message: 'Post retrieved successfully',
  timestamp: '2025-12-07T10:00:00.000Z'
};

// 辅助函数：快速生成响应格式
function createSuccessResponse(data, message = 'Success') {
  return {
    success: true,
    data,
    message,
    timestamp: new Date().toISOString()
  };
}

function createErrorResponse(code, message, details = null) {
  return {
    success: false,
    error: { code, message, details },
    timestamp: new Date().toISOString()
  };
}
```

### Wave 3: 并行更新测试文件（分2批）

**Batch 1: API 测试（15秒）**

```javascript
[
  Edit("tests/auth.test.js", update_assertions),
  Edit("tests/users.test.js", update_assertions),
  Edit("tests/posts.test.js", update_assertions),
  Edit("tests/comments.test.js", update_assertions)
]
```

**auth.test.js 更新示例**:

```javascript
// 旧测试
describe('POST /login', () => {
  it('should login successfully', async () => {
    const response = await request(app)
      .post('/login')
      .send({ username: 'alice', password: 'password123' })
      .expect(200);

    expect(response.body).toHaveProperty('token');
    expect(response.body).toHaveProperty('user');
  });

  it('should reject invalid credentials', async () => {
    const response = await request(app)
      .post('/login')
      .send({ username: 'alice', password: 'wrong' })
      .expect(401);

    expect(response.body).toHaveProperty('error');
  });
});

// 新测试（使用自定义匹配器）
describe('POST /login', () => {
  it('should login successfully', async () => {
    const response = await request(app)
      .post('/login')
      .send({ username: 'alice', password: 'password123' })
      .expect(200);

    expect(response.body).toBeSuccessResponse();
    expect(response.body.data).toMatchObject({
      token: expect.any(String),
      user: expect.objectContaining({
        id: expect.any(Number),
        username: 'alice'
      })
    });
  });

  it('should reject invalid credentials', async () => {
    const response = await request(app)
      .post('/login')
      .send({ username: 'alice', password: 'wrong' })
      .expect(401);

    expect(response.body).toBeErrorResponse('INVALID_CREDENTIALS');
    expect(response.body.error.message).toBe('Invalid credentials');
  });
});
```

**Batch 2: 集成测试（8秒）**

```javascript
[
  Edit("tests/integration/api.test.js", update_assertions)
]
```

**api.test.js 端到端测试更新**:

```javascript
// 旧集成测试
it('should complete full user workflow', async () => {
  // 注册
  const registerRes = await request(app)
    .post('/register')
    .send({ email: 'test@example.com', password: 'pass123' });
  expect(registerRes.status).toBe(201);

  // 登录
  const loginRes = await request(app)
    .post('/login')
    .send({ username: 'test@example.com', password: 'pass123' });
  expect(loginRes.body.token).toBeDefined();

  // 获取用户
  const userRes = await request(app)
    .get('/users/me')
    .set('Authorization', `Bearer ${loginRes.body.token}`);
  expect(userRes.body.email).toBe('test@example.com');
});

// 新集成测试
it('should complete full user workflow', async () => {
  // 注册
  const registerRes = await request(app)
    .post('/register')
    .send({ email: 'test@example.com', password: 'pass123' })
    .expect(201);

  expect(registerRes.body).toBeSuccessResponse();
  expect(registerRes.body.data.user).toBeDefined();

  // 登录
  const loginRes = await request(app)
    .post('/login')
    .send({ username: 'test@example.com', password: 'pass123' })
    .expect(200);

  expect(loginRes.body).toBeSuccessResponse();
  const token = loginRes.body.data.token;

  // 获取用户
  const userRes = await request(app)
    .get('/users/me')
    .set('Authorization', `Bearer ${token}`)
    .expect(200);

  expect(userRes.body).toBeSuccessResponse();
  expect(userRes.body.data.email).toBe('test@example.com');
});
```

### Final: 测试验证（3分钟）

```bash
# 运行完整测试套件
npm test -- --coverage

# 结果
Test Suites: 8 passed, 8 total
Tests:       127 passed, 127 total
Snapshots:   0 total
Time:        18.543 s
Coverage:    94.2% (提升 1.5%)

详细结果:
✅ auth.test.js: 15/15 passed
✅ users.test.js: 28/28 passed
✅ posts.test.js: 32/32 passed
✅ comments.test.js: 18/18 passed
✅ api.test.js: 34/34 passed
```

---

## 性能对比

| 指标 | 顺序执行 | 并行执行 | 提升 |
|------|---------|---------|------|
| 总时间 | 75 分钟 | 28 分钟 | 2.7x |
| 读取阶段 | 20s | 10s | 2.0x |
| 编辑阶段 | 40s | 23s | 1.7x |
| 测试更新数 | 83 | 83 | 相同 |

**关键成果**:
- 所有测试通过新格式验证
- 测试覆盖率提升 1.5%
- 测试可读性提升（使用新的 matcher）
- 零失败用例

**技术亮点**:
- 自定义 Jest 匹配器简化断言
- 共享 mock 数据工具函数
- 分批更新避免混乱
- 端到端测试保证集成正确

---

## 相关资源

- **主命令文档**: [wf_05_code.md](../../wf_05_code.md)
- **并行执行概览**: [parallel_execution_overview.md](./parallel_execution_overview.md)
- **相关案例**: [案例3: API 批量修改](./parallel_execution_case3_api_batch.md)（本案例的前置任务）
- **其他案例**:
  - [案例1: 多文件日志功能](./parallel_execution_case1_logging.md)
  - [案例2: 组件重构](./parallel_execution_case2_component_refactor.md)
- **优化技巧**: [parallel_execution_tips.md](./parallel_execution_tips.md)

---

**维护者**: AI Workflow System
**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07
