---
command: /wf_14_doc
index: 14
phase: "文档管理"
description: "智能文档助手，从代码库提取信息生成和维护项目文档"
reads: [项目代码, PLANNING.md, KNOWLEDGE.md, 现有文档]
writes: [docs/, README.md, KNOWLEDGE.md(索引更新)]
prev_commands: [/wf_05_code, /wf_08_review]
next_commands: [/wf_13_doc_maintain, /wf_11_commit]
ultrathink_lens: "extract_not_create"
context_rules:
  - "文档从代码中提取，而非凭空生成"
  - "交互式选择，不是批量生成"
  - "支持增量更新，不是全量重写"
  - "自动更新KNOWLEDGE.md索引"
  - "遵循四层文档架构（管理/技术/工作/归档）"
---

## ⚠️ 强制语言规则

**无论本命令文件使用何种语言编写，AI的输出必须遵循以下规则**：
- ✅ **所有输出内容使用中文**（交互沟通、分析报告、文档生成等）
- ✅ **遵循项目CLAUDE.md的语言规范**
- ❌ 仅在代码片段、变量名、技术术语时使用英文

**输出语言优先级**: CLAUDE.md项目规范 > 本命令指令

---

## 执行上下文
**输入**: 项目代码库 + 现有文档 + PLANNING.md
**输出**: 项目文档 + KNOWLEDGE.md索引更新
**依赖链**: /wf_05_code → **当前（文档生成）** → /wf_13_doc_maintain → /wf_11_commit

## Usage
```bash
/wf_14_doc [OPTIONS]

OPTIONS:
  --update <type>     更新特定类型文档 (api|deployment|dev|architecture|overview)
  --check             只分析不生成，显示文档缺口
  --auto              自动模式，生成所有缺失的文档
  --template <name>   使用指定模板
```

## Purpose
智能文档助手，通过分析代码库来生成和维护项目文档。核心理念：

- **提取而非编造** - 从代码、配置、注释中提取真实信息
- **交互而非批量** - 用户选择需要的文档类型
- **增量而非全量** - 支持更新现有文档，不是重写
- **上下文感知** - 基于项目的技术栈、架构和风格

## Core Capabilities

### 1. 代码库分析器 (Codebase Analyzer)

**功能**: 全面扫描项目，理解结构和技术栈

**分析维度**:
```
📂 项目结构分析
  ├─ 目录组织（src/, lib/, tests/, docs/等）
  ├─ 文件类型分布（.py, .js, .rs, .go等）
  ├─ 模块数量和层次
  └─ 代码规模（LOC, 文件数）

🔧 技术栈识别
  ├─ 编程语言和版本
  │  - Python: pyproject.toml, requirements.txt
  │  - JavaScript/TypeScript: package.json
  │  - Rust: Cargo.toml
  │  - Go: go.mod
  │  - Java: pom.xml, build.gradle
  ├─ 框架检测
  │  - Web: FastAPI, Express, Flask, Django, Spring
  │  - CLI: Click, Clap, Commander
  │  - Desktop: Electron, Tauri, PyQt
  ├─ 数据库
  │  - SQL: PostgreSQL, MySQL, SQLite
  │  - NoSQL: MongoDB, Redis
  │  - ORM: SQLAlchemy, Prisma, Diesel
  └─ 第三方服务
     - AWS, GCP, Azure
     - Stripe, SendGrid, Twilio

🏗️ 架构分析
  ├─ 模块依赖关系（import/require 分析）
  ├─ 设计模式识别（MVC, Clean Architecture, etc.）
  ├─ 分层结构（Controller → Service → Repository）
  └─ 核心组件识别（认证、数据库、API 等）

🔌 API 提取
  ├─ REST 端点（路由定义、HTTP 方法）
  ├─ GraphQL Schema（如果存在）
  ├─ RPC 接口（gRPC, tRPC）
  ├─ 参数和返回类型（从类型注解提取）
  └─ 认证和授权机制

⚙️ 配置提取
  ├─ 环境变量（.env.example, config 文件）
  ├─ 配置项（config.yaml, settings.py）
  ├─ 部署配置（Dockerfile, docker-compose.yml）
  ├─ CI/CD 配置（.github/workflows/, .gitlab-ci.yml）
  └─ 监控和日志配置
```

**输出示例**:
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

### 2. 文档缺口检测器 (Documentation Gap Detector)

**功能**: 对比现有文档与代码实际状态，识别缺失和过时

**检测逻辑**:
```python
def detect_gaps(codebase_info, existing_docs):
    gaps = []

    # 检查 1: API 文档完整性
    documented_endpoints = extract_endpoints_from_docs(existing_docs)
    actual_endpoints = codebase_info.api_endpoints
    missing_endpoints = actual_endpoints - documented_endpoints
    if missing_endpoints:
        gaps.append({
            'type': 'api',
            'severity': 'high',
            'message': f'API 文档缺失 {len(missing_endpoints)} 个端点',
            'details': missing_endpoints
        })

    # 检查 2: README 技术栈同步
    readme_tech_stack = parse_tech_stack(existing_docs['README.md'])
    actual_tech_stack = codebase_info.tech_stack
    if readme_tech_stack != actual_tech_stack:
        gaps.append({
            'type': 'overview',
            'severity': 'medium',
            'message': 'README 技术栈信息过时',
            'details': {
                'documented': readme_tech_stack,
                'actual': actual_tech_stack
            }
        })

    # 检查 3: 环境变量文档
    documented_env_vars = extract_env_vars_from_docs(existing_docs)
    actual_env_vars = codebase_info.env_vars
    missing_vars = actual_env_vars - documented_env_vars
    if missing_vars:
        gaps.append({
            'type': 'deployment',
            'severity': 'high',
            'message': f'部署文档缺少 {len(missing_vars)} 个环境变量',
            'details': missing_vars
        })

    # 检查 4: 开发指南依赖同步
    if 'docs/development/setup.md' in existing_docs:
        documented_deps = extract_dependencies_from_docs(existing_docs)
        actual_deps = codebase_info.dependencies
        if documented_deps != actual_deps:
            gaps.append({
                'type': 'dev',
                'severity': 'medium',
                'message': '开发指南依赖信息过时',
                'details': {
                    'added': actual_deps - documented_deps,
                    'removed': documented_deps - actual_deps
                }
            })
    else:
        gaps.append({
            'type': 'dev',
            'severity': 'medium',
            'message': '缺少开发指南',
            'details': 'docs/development/setup.md 不存在'
        })

    # 检查 5: 架构文档同步
    if 'docs/architecture/' in existing_docs:
        # 检查架构图是否反映当前模块结构
        pass

    return gaps
```

**输出示例**:
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

### 3. 交互式文档向导 (Interactive Documentation Wizard)

**功能**: 引导用户选择需要生成的文档

**交互流程**:
```
步骤 1: 展示分析结果
  └─ 代码库分析摘要
  └─ 文档缺口列表

步骤 2: 推荐文档生成计划
  └─ 按优先级排序（严重 → 中等 → 低）
  └─ 估算每个文档的生成时间

步骤 3: 用户选择
  └─ 交互式 checkbox 选择
  └─ 支持自定义选项

步骤 4: 确认和生成
  └─ 显示将要生成的文档列表
  └─ 确认后开始生成
```

**用户界面示例**:
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

### 4. 智能信息提取器 (Smart Information Extractor)

**功能**: 从代码、配置、注释中提取文档所需信息

#### 4.1 API 文档提取

**Python (FastAPI) 示例**:
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

**提取后的文档**:
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

#### 4.2 环境变量文档提取

**从代码中提取**:
```python
# settings.py
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SENTRY_DSN = os.getenv("SENTRY_DSN")  # Optional
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
```

**从 .env.example 提取**:
```bash
# .env.example
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=https://xxx@sentry.io/123  # Optional: Error tracking
SMTP_SERVER=smtp.gmail.com
```

**生成的文档**:
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

#### 4.3 依赖和技术栈提取

**从 pyproject.toml 提取**:
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
sqlalchemy = "^2.0.0"
redis = "^5.0.0"
sentry-sdk = "^1.38.0"
```

**生成的文档**:
```markdown
## 技术栈

### 核心框架
- **Python**: 3.11+
- **Web 框架**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+

### 数据存储
- **主数据库**: PostgreSQL 15+
- **缓存**: Redis 7+

### 监控和日志
- **错误追踪**: Sentry (sentry-sdk 1.38+)

### 安装依赖

使用 Poetry:
```bash
poetry install
```

或使用 pip:
```bash
pip install -r requirements.txt
```
```

#### 4.4 从测试代码提取使用示例

**测试代码**:
```python
def test_refresh_token(client, test_user):
    # 先登录获取 refresh token
    login_response = client.post("/auth/login", json={
        "username": "test@example.com",
        "password": "password123"
    })
    refresh_token = login_response.json()["refresh_token"]

    # 使用 refresh token 获取新的 access token
    response = client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
```

**生成的文档示例**:
```markdown
### 使用示例

**刷新令牌**:
```bash
# 1. 先登录获取 refresh token
curl -X POST https://api.example.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "your_password"}'

# 响应:
# {
#   "access_token": "eyJ...",
#   "refresh_token": "dGh...",
#   "expires_in": 3600
# }

# 2. 使用 refresh token 获取新的 access token
curl -X POST https://api.example.com/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "dGh..."}'

# 响应:
# {
#   "access_token": "eyJ...",  # 新的 access token
#   "refresh_token": "abc...",  # 新的 refresh token
#   "expires_in": 3600
# }
```
```

---

### 5. 文档生成器 (Document Generator)

**功能**: 基于提取的信息和项目风格生成文档

#### 5.0 Frontmatter 元数据生成 (NEW)

**功能**: 为所有技术文档自动生成标准 Frontmatter 头

**📋 标准规范**: 详见 [Frontmatter规范参考](docs/reference/FRONTMATTER.md)

**快速参考**:
- 必需字段（7个）: title, description, type, status, priority, created_date, last_updated
- Type枚举（6种）: 技术设计 | 系统集成 | API参考 | 教程 | 故障排查 | 架构决策
- Status枚举（3种）: 草稿 | 完成 | 待审查
- Priority枚举（3种）: 高 | 中 | 低

完整模板和字段说明见规范文档 § 标准模板 § 字段说明

**生成逻辑**（使用标准规范函数，见 FRONTMATTER.md § 工具和脚本）:
```python
def generate_frontmatter(doc_info, codebase_analysis, knowledge_md):
    """
    生成标准 frontmatter

    使用标准模板和枚举值（见 FRONTMATTER.md）
    """
    from generate_frontmatter import generate_default_frontmatter  # 标准生成函数

    # 1. 加载标准模板
    frontmatter = generate_default_frontmatter(doc_info.path)

    # 2. 填充基础信息
    frontmatter['title'] = doc_info.title or infer_from_filename(doc_info.path)
    frontmatter['description'] = extract_first_paragraph(doc_info.content)

    # 3. 智能提取关系网络
    frontmatter['related_documents'] = find_related_docs(doc_info, knowledge_md)
    frontmatter['related_code'] = extract_code_references(doc_info, codebase_analysis)

    # 4. 提取元数据
    frontmatter['tags'] = extract_tags(doc_info, codebase_analysis.tech_stack)

    return format_yaml_frontmatter(frontmatter)
```

**类型和优先级判定逻辑**（见 FRONTMATTER.md § 枚举值定义）:
```python
# Type 自动分类（基于路径）
type_mapping = {
    'docs/api/': 'API参考',
    'docs/architecture/': '技术设计',
    'docs/deployment/': '系统集成',
    'docs/development/': '教程',
    'docs/troubleshooting/': '故障排查',
    'docs/adr/': '架构决策'
}

# Priority 自动判定（基于类型和引用数）
high_priority_types = ['API参考', '系统集成', '架构决策']
```

**集成到文档模板**:
所有生成的技术文档（docs/下的文件）都应该在文件顶部包含 Frontmatter。

---

#### 5.1 文档类型模板

**1. 📚 项目概览 (README.md)**
```markdown
# {project_name}

{project_description}

## 特性

{extracted_features}

## 技术栈

{tech_stack_from_analysis}

## 快速开始

### 前置要求

{requirements_from_dependencies}

### 安装

```bash
{install_commands_from_package_manager}
```

### 运行

```bash
{run_commands_from_scripts}
```

## 项目结构

```
{directory_tree_from_analysis}
```

## 文档

- [API 文档](docs/api/README.md)
- [开发指南](docs/development/setup.md)
- [部署文档](docs/deployment/README.md)
- [架构设计](docs/architecture/README.md)

## 许可证

{license_from_package_file}
```

**2. 🔌 API 文档 (docs/api/README.md)**
```markdown
# API 文档

## 概览

{api_summary_from_analysis}

## 认证

{auth_mechanism_from_code}

## 端点

{endpoints_extracted_from_routes}

### {endpoint_category}

{endpoints_in_category}

## 错误码

{error_codes_from_exception_handlers}

## 限流

{rate_limit_info_from_middleware}
```

**3. ⚙️ 开发指南 (docs/development/setup.md)**
```markdown
# 开发环境设置

## 系统要求

{system_requirements_from_analysis}

## 安装步骤

### 1. 克隆仓库

```bash
git clone {repo_url}
cd {project_name}
```

### 2. 安装依赖

{dependency_installation_from_package_manager}

### 3. 配置环境

```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的环境变量
```

### 4. 数据库设置

{database_setup_from_migrations}

### 5. 运行开发服务器

```bash
{dev_server_command}
```

## 开发工作流

{workflow_from_planning_md}

## 代码规范

{code_standards_from_planning_md}

## 测试

{test_commands_from_package_scripts}

## 常见问题

{common_issues_from_knowledge_md}
```

**4. 🚀 部署文档 (docs/deployment/README.md)**
```markdown
# 部署指南

## 环境变量

{env_vars_from_extraction}

## Docker 部署

{docker_instructions_from_dockerfile}

## Kubernetes 部署

{k8s_instructions_from_manifests}

## 监控

{monitoring_setup_from_config}

## 备份

{backup_procedures_from_scripts}
```

**5. 🏗️ 架构文档 (docs/architecture/README.md)**
```markdown
# 系统架构

## 概览

{architecture_summary_from_analysis}

## 分层设计

{layer_diagram_from_module_analysis}

## 核心组件

{components_from_module_analysis}

## 数据流

{data_flow_from_dependency_graph}

## 设计模式

{patterns_from_code_analysis}

## 架构决策记录 (ADR)

{adr_list_from_docs_adr}
```

#### 5.2 风格适配

**学习项目风格**:
```python
def learn_doc_style(existing_docs, planning_md):
    style = {
        'heading_style': 'atx',  # # 还是 underline
        'code_fence': '```',     # ``` 还是 ~~~
        'list_marker': '-',      # - 还是 *
        'emphasis': '*',         # * 还是 _
        'language': 'zh-CN',     # 从 CLAUDE.md 读取
        'emoji_usage': True,     # 是否使用 emoji
        'tone': 'professional'   # 从现有文档学习语气
    }

    # 分析现有文档的风格
    for doc in existing_docs:
        # ... 提取风格特征

    return style
```

**应用风格生成**:
```python
def generate_with_style(content, style):
    # 应用学习到的风格
    if style['language'] == 'zh-CN':
        # 使用中文
        content = translate_to_chinese(content)

    if style['emoji_usage']:
        # 添加 emoji
        content = add_emojis(content)

    # ... 应用其他风格

    return content
```

---

### 6. 文档质量保证 (Quality Assurance)

**功能**: 确保生成的文档高质量

**检查项**:
```
✓ Frontmatter 完整性 (NEW)
  ├─ 必需字段都存在（title, description, type, status, priority, created_date, last_updated）
  ├─ 字段值格式正确（日期格式、枚举值）
  ├─ related_documents 路径有效
  ├─ related_code 路径存在
  └─ related_tasks 在 TASK.md 中存在

✓ 语言一致性
  ├─ 遵循 CLAUDE.md 语言规范
  └─ 术语使用一致

✓ 链接有效性
  ├─ 内部链接指向存在的文件
  └─ 外部链接可访问

✓ 代码示例可运行
  ├─ 语法正确
  └─ 与实际代码一致

✓ 结构完整性
  ├─ 必需章节都存在
  └─ 章节顺序合理

✓ 遵循四层架构
  ├─ 管理层文档在根目录
  ├─ 技术层文档在 docs/
  └─ 更新 KNOWLEDGE.md 索引
```

**Frontmatter 验证**:

使用标准验证函数（见 [FRONTMATTER.md § 验证逻辑](docs/reference/FRONTMATTER.md)）

**⚠️ Execution Context**: 验证脚本必须从**项目根目录**运行（详见规范文档 § 执行上下文）

```python
from frontmatter_validator import validate_frontmatter  # 使用标准验证函数

# 验证示例
validation_result = validate_frontmatter(doc_path, frontmatter)
if not validation_result['valid']:
    for error in validation_result['errors']:
        print(f"错误: {error}")
    for warning in validation_result['warnings']:
        print(f"警告: {warning}")
```

**验证内容**（详见规范文档）:
- ✅ 7个必需字段完整性
- ✅ 枚举值有效性（type/status/priority）
- ✅ 日期格式（YYYY-MM-DD）
- ✅ 日期逻辑（created_date <= last_updated）
- ✅ 引用路径存在性（related_documents/code/tasks）

---

### 7. 索引管理器 (Index Manager)

**功能**: 自动更新 KNOWLEDGE.md 的文档索引

**更新逻辑**:
```python
def update_knowledge_index(new_docs, knowledge_md):
    # 解析现有索引
    current_index = parse_doc_index(knowledge_md)

    # 添加新文档条目
    for doc in new_docs:
        if doc.path not in current_index:
            current_index.append({
                '主题': doc.topic,
                '文档路径': doc.path,
                '说明': doc.description,
                '优先级': doc.priority,
                '最后更新': today()
            })
        else:
            # 更新现有条目
            current_index[doc.path]['最后更新'] = today()

    # 写回 KNOWLEDGE.md
    write_doc_index(knowledge_md, current_index)
```

---

## Process

### 标准流程 (默认)

**步骤 1: 代码库分析**
```
1.1 扫描项目结构
    - 识别目录组织
    - 统计文件类型和规模

1.2 识别技术栈
    - 解析依赖文件 (package.json, pyproject.toml, etc.)
    - 检测框架和库

1.3 分析架构
    - 构建模块依赖图
    - 识别分层结构

1.4 提取 API
    - 扫描路由定义
    - 提取端点、参数、返回类型

1.5 读取配置
    - 解析环境变量
    - 提取部署配置
```

**步骤 2: 文档缺口检测**
```
2.1 读取现有文档
    - README.md
    - docs/ 目录下的所有文档

2.2 对比分析
    - API 文档 vs 实际端点
    - README 技术栈 vs 实际依赖
    - 环境变量文档 vs 实际配置
    - 开发指南 vs 当前工具链

2.3 生成缺口报告
    - 按严重程度分类
    - 提供详细说明
```

**步骤 3: 交互式选择**
```
3.1 展示分析结果
    - 代码库概览
    - 文档缺口列表

3.2 推荐生成计划
    - 按优先级排序
    - 估算生成时间

3.3 用户选择
    - 显示选项列表
    - 用户输入选择
    - 确认生成计划
```

**步骤 4: 智能提取**
```
4.1 根据选择的文档类型，提取相应信息
    - API 文档 → 从路由定义提取
    - 环境变量 → 从 .env.example 和代码提取
    - 开发指南 → 从依赖文件和脚本提取
    - 架构文档 → 从模块分析提取

4.2 学习项目风格
    - 分析现有文档的写作风格
    - 提取术语表
    - 识别常用模式
```

**步骤 5: 文档生成**
```
5.1 选择合适的模板
5.2 填充提取的信息
5.3 应用项目风格
5.4 生成文档文件
```

**步骤 6: 质量检查**
```
6.1 验证文档结构
6.2 检查链接有效性
6.3 确保代码示例可运行
6.4 检查语言一致性
```

**步骤 7: 索引更新**
```
7.1 解析 KNOWLEDGE.md
7.2 添加或更新文档条目
7.3 更新最后修改日期
7.4 写回文件
```

**步骤 8: 生成报告**
```
8.1 总结生成的文档
8.2 列出更新的文件
8.3 提供后续建议
```

---

### 更新模式 (--update)

**快速更新特定类型的文档**

```bash
# 只更新 API 文档
/wf_14_doc --update api

# 流程:
1. 提取 API 端点信息
2. 读取现有 API 文档
3. 识别变化（新增、修改、删除）
4. 更新文档
5. 更新 KNOWLEDGE.md
```

---

### 检查模式 (--check)

**只分析不生成，用于 CI/CD 检查**

```bash
/wf_14_doc --check

# 流程:
1. 执行完整的代码库分析
2. 执行文档缺口检测
3. 生成报告但不生成文档
4. 返回状态码（0 = 无缺口，1 = 有缺口）
```

---

### 自动模式 (--auto)

**无交互，自动生成所有缺失文档**

```bash
/wf_14_doc --auto

# 流程:
1. 代码库分析
2. 文档缺口检测
3. 自动生成所有缺失/过时的文档
4. 更新索引
5. 生成报告
```

---

## Output Format

### 1. 分析报告
```markdown
# 📊 代码库分析报告

## 项目概览
- 名称: {project_name}
- 类型: {project_type}
- 规模: {loc} LOC, {files} 文件
- 模块: {modules} 个

## 技术栈
{tech_stack_summary}

## 架构
{architecture_summary}

## API 概览
{api_summary}

## 配置
{config_summary}
```

### 2. 缺口报告
```markdown
# 📋 文档缺口分析

## ⚠️ 严重缺口 ({count})
{critical_gaps}

## ⚠️ 中等缺口 ({count})
{medium_gaps}

## ✅ 完整文档 ({count})
{complete_docs}
```

### 3. 生成计划
```markdown
# 📝 建议生成的文档

[1] 🔴 {doc_type} ({file_path})
    ├─ 严重程度: {severity}
    ├─ 内容: {description}
    ├─ 来源: {source}
    └─ 预计时间: {time}

[2] ...

请选择要生成的文档: _
```

### 4. 生成报告
```markdown
# ✅ 文档生成完成

## 生成的文档 ({count})
1. ✅ {file_path} - {description}
2. ✅ ...

## 更新的文档 ({count})
1. 🔄 {file_path} - {changes}
2. 🔄 ...

## 索引更新
- KNOWLEDGE.md: 添加 {new_count} 个条目，更新 {updated_count} 个条目

## 后续建议
- 运行 /wf_13_doc_maintain 检查文档结构
- 运行 /wf_11_commit 提交更改
- 审查生成的文档，完善细节
```

---

## 💡 Ultrathink 设计检查

生成文档后，AI 会进行设计优雅度自检：

- ✅ **提取而非编造** - 所有信息都来自代码和配置吗？
- ✅ **项目特定** - 文档是否反映了这个项目的特点？
- ✅ **风格一致** - 文档风格是否与现有文档保持一致？
- ✅ **必要而简洁** - 有没有不必要的内容？能否更简洁？
- ✅ **可维护性** - 文档结构是否清晰，方便后续更新？

---

## Workflow Integration

**在工作流中的位置**:
```
/wf_05_code (实现功能)
  ↓
/wf_07_test (测试)
  ↓
/wf_08_review (代码审查)
  ↓
/wf_14_doc (生成/更新文档) ← 当前
  ↓
/wf_13_doc_maintain (维护文档结构)
  ↓
/wf_11_commit (提交)
```

**与其他命令的交互**:
- **读取** PLANNING.md - 了解项目架构和标准
- **读取** KNOWLEDGE.md - 学习文档索引和项目知识
- **写入** docs/ - 生成技术层文档
- **更新** KNOWLEDGE.md - 添加新文档索引
- **触发** /wf_13_doc_maintain - 完成后建议运行维护
- **触发** /wf_11_commit - 完成后建议提交

---

## Examples

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

## Best Practices

### 1. 何时运行

**推荐时机**:
- ✅ 完成新功能实现后
- ✅ 添加新 API 端点后
- ✅ 修改配置或环境变量后
- ✅ 重构架构后
- ✅ 项目初始化时

**不推荐时机**:
- ❌ 代码频繁变动中（等稳定后再生成）
- ❌ 正在调试 bug 时（专注修复，不要分心）

### 2. 审查和完善

**AI 生成的文档是基础，需要人工审查和完善**:
- 检查技术细节是否准确
- 添加使用建议和最佳实践
- 补充业务背景说明
- 添加图表和示例（如果需要）

### 3. 增量更新

**不要全量重新生成，使用增量更新**:
```bash
# 好的做法
/wf_14_doc --update api

# 避免（除非重大重构）
/wf_14_doc --auto  # 重新生成所有文档
```

### 4. 配合其他命令

**文档生成是工作流的一部分**:
```bash
# 完整流程
/wf_05_code        # 实现功能
/wf_07_test        # 测试
/wf_08_review      # 代码审查
/wf_14_doc         # 生成文档
/wf_13_doc_maintain # 维护文档结构
/wf_11_commit      # 提交
```

---

## Limitations

### 当前限制

1. **语言支持**
   - 主要支持: Python, JavaScript/TypeScript, Rust, Go
   - 部分支持: Java, C#
   - 不支持: 冷门语言

2. **框架支持**
   - Web: FastAPI, Express, Flask, Django, Spring
   - CLI: Click, Clap, Commander
   - 其他框架需要手动完善

3. **提取准确性**
   - 依赖代码注释和类型注解的质量
   - 动态生成的端点可能遗漏
   - 复杂的配置可能需要人工补充

### 未来改进方向

- [ ] 支持更多编程语言和框架
- [ ] 集成 OpenAPI/Swagger 自动同步
- [ ] 支持生成架构图（基于模块依赖）
- [ ] AI 驱动的文档质量评分
- [ ] 文档变更自动检测和提醒

---

## Troubleshooting

### 常见问题

**Q: 为什么某些端点没有被提取到？**
A: 可能是因为：
- 端点是动态生成的
- 路由定义在非标准位置
- 使用了自定义装饰器

解决方法：手动补充，或在代码中添加更多注释。

**Q: 生成的文档风格不一致怎么办？**
A: 确保现有文档有足够的示例供 AI 学习。如果是新项目，第一次生成后手动调整风格，后续生成会学习这个风格。

**Q: 如何自定义文档模板？**
A: 使用 `--template` 参数指定模板文件。模板使用 Jinja2 语法。

**Q: 文档生成时间太长怎么办？**
A: 使用 `--update` 参数只更新特定类型的文档，而不是全量生成。

---

**See Also**:
- [/wf_05_code](wf_05_code.md) - 代码实现
- [/wf_13_doc_maintain](wf_13_doc_maintain.md) - 文档维护
- [/wf_11_commit](wf_11_commit.md) - 提交更改
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计哲学指南
