---
title: "wf_14_doc 命令完整示例库"
description: "智能文档生成命令的详细示例和输出样本"
type: "教程"
status: "完成"
priority: "中"
created_date: "2025-11-15"
last_updated: "2025-11-15"
related_documents: ["../../wf_14_doc.md"]
---

# /wf_14_doc 命令完整示例库

本文档包含 `/wf_14_doc` 命令的所有详细示例和输出样本，便于学习和参考。

---

## 核心命令示例

### Frontmatter 工具命令

```bash
# 为单个文档生成 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py generate docs/api/auth.md

# 批量生成 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py generate-batch docs/

# 验证 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/api/auth.md

# 批量验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 生成文档关系图（Mermaid格式）
python ~/.claude/commands/scripts/doc_graph_builder.py docs/ --format mermaid
```

---

## 1. 代码库分析输出示例

### 完整分析报告

```markdown
# 📊 代码库分析报告

## 项目概览
- **名称**: MyProject
- **类型**: Web Application
- **代码规模**: 12,450 LOC, 87 文件
- **模块数**: 6 个核心模块

## 技术栈
- **语言**: Python 3.11
- **框架**: FastAPI 0.104
- **数据库**: PostgreSQL 15 + Redis 7
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (PyJWT)
- **部署**: Docker + Kubernetes

## 架构
- **模式**: Clean Architecture
- **分层**:
  - API Layer (routes/)
  - Service Layer (services/)
  - Repository Layer (repositories/)
  - Domain Layer (models/)

## API 概览
- **端点数**: 12 个
- **认证**: Bearer Token (JWT)
- **新增端点**（未在文档中）:
  - POST /auth/refresh
  - GET /users/bulk
  - GET /admin/stats

## 配置
- **环境变量**: 8 个
- **新增变量**（未在文档中）:
  - REDIS_URL
  - SENTRY_DSN
  - SMTP_SERVER
```

---

## 2. 文档缺口分析示例

### 缺口检测结果

```markdown
# 📋 文档缺口分析

## ⚠️ 严重缺口 (2)
1. **API 文档缺失端点**
   - 类型: api
   - 影响: 开发者无法了解新 API 的使用方式
   - 缺失端点:
     * POST /auth/refresh
     * GET /users/bulk
     * GET /admin/stats

2. **部署文档缺少环境变量**
   - 类型: deployment
   - 影响: 部署时配置不完整，可能导致运行时错误
   - 缺失变量:
     * REDIS_URL
     * SENTRY_DSN
     * SMTP_SERVER

## ⚠️ 中等缺口 (2)
3. **README 技术栈过时**
   - 类型: overview
   - 当前文档: Python 3.9, FastAPI 0.95
   - 实际版本: Python 3.11, FastAPI 0.104

4. **开发指南依赖过时**
   - 类型: dev
   - 新增依赖: redis, sentry-sdk, celery
   - 移除依赖: flask-cors (已迁移到 FastAPI)

## ✅ 完整文档 (1)
5. **架构文档**
   - 最后更新: 2025-11-05
   - 状态: 与代码一致
```

---

## 3. 交互式文档向导示例

### 用户交互流程

```
📊 分析完成！发现 4 个文档缺口

📝 建议生成的文档:

[1] 🔴 API 文档更新 (docs/api/README.md)
    ├─ 严重程度: 高
    ├─ 内容: 添加 3 个新端点的文档
    ├─ 来源: 从路由定义和类型注解提取
    └─ 预计时间: 2 分钟

[2] 🔴 环境变量文档 (docs/deployment/env-vars.md)
    ├─ 严重程度: 高
    ├─ 内容: 3 个新环境变量的说明
    ├─ 来源: 从 .env.example 和代码引用提取
    └─ 预计时间: 1 分钟

[3] 🟡 README 更新
    ├─ 严重程度: 中
    ├─ 内容: 更新技术栈版本信息
    ├─ 来源: 从 pyproject.toml 提取
    └─ 预计时间: 1 分钟

[4] 🟡 开发指南更新 (docs/development/setup.md)
    ├─ 严重程度: 中
    ├─ 内容: 更新依赖列表和安装步骤
    ├─ 来源: 从 pyproject.toml 和 Makefile 提取
    └─ 预计时间: 3 分钟

请选择要生成的文档:
  [ ] 1. API 文档更新
  [ ] 2. 环境变量文档
  [ ] 3. README 更新
  [ ] 4. 开发指南更新
  [ ] all - 生成所有文档

输入选项 (1-4, all, 或逗号分隔如 1,2): _
```

---

## 4. 信息提取示例

### Python FastAPI 代码示例

```python
# 代码:
@app.post("/auth/refresh", response_model=TokenResponse, tags=["Authentication"])
async def refresh_token(
    refresh_token: str = Body(..., description="Refresh token from login"),
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    刷新访问令牌

    使用有效的 refresh token 获取新的 access token，
    无需重新输入用户名和密码。

    Args:
        refresh_token: 登录时获得的刷新令牌

    Returns:
        新的访问令牌和刷新令牌

    Raises:
        401: 刷新令牌无效或已过期
    """
    # ... implementation
```

#### 提取后的 API 文档

```markdown
### POST /auth/refresh

刷新访问令牌

使用有效的 refresh token 获取新的 access token，无需重新输入用户名和密码。

**请求体**:
```json
{
  "refresh_token": "string"  // 登录时获得的刷新令牌
}
```

**响应** (200 OK):
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**错误响应**:
- `401 Unauthorized`: 刷新令牌无效或已过期

**标签**: Authentication
```

### 环境变量提取示例

```python
# settings.py
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SENTRY_DSN = os.getenv("SENTRY_DSN")  # Optional
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
```

```bash
# .env.example
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=https://xxx@sentry.io/123  # Optional: Error tracking
SMTP_SERVER=smtp.gmail.com
```

#### 生成的文档

```markdown
## 环境变量配置

### REDIS_URL
- **描述**: Redis 数据库连接 URL
- **类型**: String
- **必需**: 否
- **默认值**: `redis://localhost:6379/0`
- **示例**: `redis://user:pass@redis-host:6379/0`

### SENTRY_DSN
- **描述**: Sentry 错误追踪 DSN
- **类型**: String
- **必需**: 否（用于生产环境监控）
- **默认值**: 无
- **示例**: `https://xxx@sentry.io/123`

### SMTP_SERVER
- **描述**: 邮件发送服务器地址
- **类型**: String
- **必需**: 否
- **默认值**: `smtp.gmail.com`
- **示例**: `smtp.sendgrid.net`
```

---

## 5. 完整执行示例

### 示例 1: 新项目首次生成文档

```bash
$ /wf_14_doc

📊 正在分析代码库...
✓ 项目结构扫描完成 (87 文件)
✓ 技术栈识别完成 (Python 3.11 + FastAPI)
✓ API 提取完成 (12 端点)
✓ 配置分析完成 (8 环境变量)

📋 文档缺口分析:

⚠️ 严重缺口 (3)
1. 缺少 API 文档 (docs/api/README.md)
2. 缺少环境变量文档 (docs/deployment/env-vars.md)
3. 缺少开发指南 (docs/development/setup.md)

⚠️ 中等缺口 (1)
4. README.md 不存在

📝 建议生成的文档:

[1] 🔴 API 文档 (docs/api/README.md)
    ├─ 严重程度: 高
    ├─ 内容: 12 个端点的完整文档
    ├─ 来源: 从路由定义和类型注解提取
    └─ 预计时间: 5 分钟

[2] 🔴 环境变量文档 (docs/deployment/env-vars.md)
    ├─ 严重程度: 高
    ├─ 内容: 8 个环境变量的说明
    ├─ 来源: 从 .env.example 和代码提取
    └─ 预计时间: 2 分钟

[3] 🔴 开发指南 (docs/development/setup.md)
    ├─ 严重程度: 高
    ├─ 内容: 环境设置和开发工作流
    ├─ 来源: 从 pyproject.toml 和 Makefile 提取
    └─ 预计时间: 4 分钟

[4] 🟡 README.md
    ├─ 严重程度: 中
    ├─ 内容: 项目概览和快速开始
    ├─ 来源: 从项目分析和 PLANNING.md 提取
    └─ 预计时间: 3 分钟

请选择要生成的文档 (1-4, all, 或逗号分隔): all

✅ 开始生成文档...

✓ [1/4] 生成 docs/api/README.md (5.2 秒)
✓ [2/4] 生成 docs/deployment/env-vars.md (1.8 秒)
✓ [3/4] 生成 docs/development/setup.md (3.5 秒)
✓ [4/4] 生成 README.md (2.9 秒)

✓ 更新 KNOWLEDGE.md 索引 (添加 3 个条目)

✅ 文档生成完成！

生成的文档:
1. ✅ docs/api/README.md - API 完整文档
2. ✅ docs/deployment/env-vars.md - 环境变量说明
3. ✅ docs/development/setup.md - 开发环境设置
4. ✅ README.md - 项目概览

后续建议:
- 审查生成的文档，完善细节
- 运行 /wf_13_doc_maintain 检查文档结构
- 运行 /wf_11_commit 提交更改
```

### 示例 2: 代码更新后更新 API 文档

```bash
$ /wf_14_doc --update api

📊 分析 API 变化...

发现 3 个新端点:
  + POST /auth/refresh
  + GET /users/bulk
  + GET /admin/stats

发现 1 个端点修改:
  ~ PUT /users/{id} - 添加了新参数 'role'

✅ 更新 docs/api/README.md...

✓ 添加 3 个新端点文档
✓ 更新 1 个端点文档
✓ 更新 KNOWLEDGE.md (最后更新时间)

✅ API 文档更新完成！
```

### 示例 3: CI/CD 检查模式

```bash
$ /wf_14_doc --check

📊 分析代码库...
📋 检测文档缺口...

⚠️ 发现 2 个文档缺口:

1. API 文档缺少 1 个新端点
   - POST /webhooks/stripe

2. 环境变量文档缺少 1 个变量
   - STRIPE_WEBHOOK_SECRET

❌ 文档检查失败 (退出码 1)

建议: 运行 /wf_14_doc 更新文档
```

---

## 6. Frontmatter 验证示例

### 验证输出

```bash
$ python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

✓ docs/api/auth.md - 验证通过
  - 所有 7 个必需字段完整
  - 枚举值有效
  - 日期格式正确
  - 引用路径存在

✓ docs/api/users.md - 验证通过

✗ docs/api/webhooks.md - 验证失败
  - 缺少必需字段: priority
  - related_code 路径无效: ./models/webhook.py (应为 src/models/webhook.py)

✓ docs/deployment/README.md - 验证通过

✅ 验证完成: 3 成功, 1 失败
```

---

## 使用建议

### 何时参考这些示例？

- **学习命令用法**: 查看"完整执行示例"部分
- **了解 API 提取**: 参考"信息提取示例"部分
- **验证文档结构**: 参考"代码库分析输出示例"
- **排查文档问题**: 参考"文档缺口分析示例"
- **处理 Frontmatter**: 参考"Frontmatter 验证示例"

### 与主文档的关系

本文档中的所有示例都来自 `/wf_14_doc` 主文档，已为了简洁性被提取到此。详细的说明和原理仍在主文档中：

- **流程说明**: 主文档的"## Process"章节
- **工具清单**: 主文档的"## 🛠️ 可用工具"章节
- **核心功能**: 主文档的"## Core Capabilities"章节
- **最佳实践**: 主文档的"## Best Practices"章节

---

**参考**: [wf_14_doc 主文档](../../wf_14_doc.md)
