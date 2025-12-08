---
title: "案例1: 多文件日志功能添加"
description: "在3个模块中统一添加日志功能的并行执行实战案例"
type: "示例文档"
status: "完成"
priority: "中"
created_date: "2025-12-03"
last_updated: "2025-12-07"
related_documents:
  - "wf_05_code.md"
  - "docs/examples/parallel_execution_overview.md"
tags: ["并行执行", "代码实现", "日志功能", "多文件", "实战案例"]
---

# 案例1: 多文件日志功能添加

**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07

## 📋 目录

- [场景描述](#场景描述)
- [并行执行方案](#并行执行方案)
- [性能对比](#性能对比)

---

## 场景描述

**任务**: 在认证、API 和数据库3个模块中统一添加日志功能

**问题**:
- 需要修改 3 个文件：`auth.js`, `api.js`, `db.js`
- 每个文件需要：导入 logger、添加日志调用、配置日志级别
- 顺序执行预计需要 30 分钟

---

## 并行执行方案

### Wave 1: 并行读取所有文件（5秒）

```javascript
// 同时读取3个需要修改的文件
[
  Read("src/auth.js"),
  Read("src/api.js"),
  Read("src/db.js")
]

// 读取结果汇总
auth.js: 150 行（认证模块）
api.js:  200 行（API 路由）
db.js:   180 行（数据库操作）

// 识别关键函数
auth.js: login(), register(), validateToken()
api.js:  handleRequest(), parseBody(), sendResponse()
db.js:   connect(), query(), disconnect()
```

### Checkpoint: 设计日志策略（顺序，3分钟）

```javascript
日志需求分析:
┌─────────────────────────────────────┐
│ 模块      日志级别    关键操作       │
├─────────────────────────────────────┤
│ auth.js   INFO       登录、注册      │
│ api.js    DEBUG      请求、响应      │
│ db.js     WARN       查询、错误      │
└─────────────────────────────────────┘

统一日志格式:
logger.info('操作描述', { 上下文数据 });

需要添加的位置:
auth.js:
  - Line 25: 用户登录开始
  - Line 45: 密码验证完成
  - Line 67: Token 生成成功

api.js:
  - Line 15: 请求接收
  - Line 30: 请求处理中
  - Line 50: 响应发送

db.js:
  - Line 10: 数据库连接
  - Line 40: 查询执行
  - Line 70: 错误处理
```

### Wave 2: 并行编辑文件（8秒）

```javascript
// 同时编辑3个文件
[
  Edit("src/auth.js", add_logging_auth),
  Edit("src/api.js", add_logging_api),
  Edit("src/db.js", add_logging_db)
]

// 编辑内容示例（auth.js）
// Line 1: import logger from './utils/logger';
// Line 25: logger.info('User authentication started', { userId });
// Line 45: logger.info('Password validation completed');
// Line 67: logger.info('JWT token generated', { tokenExpiry });
```

**auth.js 具体修改**:

```javascript
// 添加导入
import logger from './utils/logger';

// 在关键位置添加日志
async function login(username, password) {
  logger.info('User authentication started', { username });

  const user = await findUser(username);
  if (!user) {
    logger.warn('User not found', { username });
    throw new Error('Invalid credentials');
  }

  const isValid = await validatePassword(password, user.passwordHash);
  logger.info('Password validation completed', { username, isValid });

  if (!isValid) {
    throw new Error('Invalid credentials');
  }

  const token = generateToken(user);
  logger.info('JWT token generated', { userId: user.id, tokenExpiry: '1h' });

  return token;
}
```

**api.js 具体修改**:

```javascript
import logger from './utils/logger';

async function handleRequest(req, res) {
  logger.debug('Request received', {
    method: req.method,
    path: req.path,
    headers: req.headers
  });

  try {
    const body = await parseBody(req);
    logger.debug('Request body parsed', { bodySize: JSON.stringify(body).length });

    const result = await processRequest(body);

    logger.debug('Response sending', { statusCode: 200, resultSize: result.length });
    res.status(200).json(result);
  } catch (error) {
    logger.error('Request handling failed', { error: error.message });
    res.status(500).json({ error: error.message });
  }
}
```

**db.js 具体修改**:

```javascript
import logger from './utils/logger';

async function connect() {
  logger.info('Database connection initiated', { host: DB_HOST });

  try {
    const conn = await createConnection();
    logger.info('Database connected successfully');
    return conn;
  } catch (error) {
    logger.error('Database connection failed', { error: error.message });
    throw error;
  }
}

async function query(sql, params) {
  logger.debug('Query executing', { sql, paramCount: params.length });

  try {
    const result = await executeQuery(sql, params);
    logger.debug('Query completed', { rowCount: result.length });
    return result;
  } catch (error) {
    logger.warn('Query failed', { sql, error: error.message });
    throw error;
  }
}
```

### Final: 验证（1分钟）

```
验证清单:
✅ 所有文件都成功导入 logger
✅ 日志级别配置正确（auth=info, api=debug, db=warn）
✅ 日志格式一致（使用统一的消息模板）
✅ 无语法错误
✅ 代码格式化一致

日志输出测试:
auth.js → INFO: User authentication started { username: 'alice' }
api.js  → DEBUG: Request received { method: 'POST', path: '/api/users' }
db.js   → INFO: Database connected successfully
```

---

## 性能对比

| 指标 | 顺序执行 | 并行执行 | 提升 |
|------|---------|---------|------|
| 总时间 | 30 分钟 | 10 分钟 | 3.0x |
| 读取时间 | 15s | 5s | 3.0x |
| 编辑时间 | 24s | 8s | 3.0x |
| Token 消耗 | 12,000 | 12,000 | 相同 |

**关键成果**:
- 日志功能在3个模块中一致实现
- 开发时间节省 67%
- 零错误率（所有验证通过）
- 日志格式统一，易于维护

**适用场景**:
- 跨模块添加相同功能
- 文件间无依赖关系
- 修改模式相似

---

## 相关资源

- **主命令文档**: [wf_05_code.md](../../wf_05_code.md)
- **并行执行概览**: [parallel_execution_overview.md](./parallel_execution_overview.md)
- **其他案例**:
  - [案例2: 组件重构](./parallel_execution_case2_component_refactor.md)
  - [案例3: API 批量修改](./parallel_execution_case3_api_batch.md)
  - [案例4: 测试套件更新](./parallel_execution_case4_test_update.md)
- **优化技巧**: [parallel_execution_tips.md](./parallel_execution_tips.md)

---

**维护者**: AI Workflow System
**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07
