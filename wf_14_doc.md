---
command: /wf_14_doc
index: 14
phase: "文档管理"
description: "智能文档助手，从代码库提取信息生成和维护项目文档 | MCP: --ui"
reads: [项目代码, PLANNING.md, KNOWLEDGE.md, 现有文档]
writes: [docs/, README.md, KNOWLEDGE.md(索引更新)]
prev_commands: [/wf_05_code, /wf_08_review]
next_commands: [/wf_13_doc_maintain, /wf_11_commit]
ultrathink_lens: "extract_not_create"
mcp_support:
  - name: "Magic"
    flag: "--ui"
    description: "UI文档和组件示例生成"
context_rules:
  - "文档从代码中提取，而非凭空生成"
  - "交互式选择，不是批量生成"
  - "支持增量更新，不是全量重写"
  - "自动更新KNOWLEDGE.md索引"
  - "遵循四层文档架构（管理/技术/工作/归档）"
---

## 🔌 MCP 增强能力

本命令支持以下 MCP 服务器的可选增强：

### Magic (UI 组件生成)

**启用**: `--ui` 标志
**用途**: 为文档生成交互式 UI 组件和可视化界面
**自动激活**: 否（用户明确启用）

**示例**:
```bash
# 生成带有交互式 UI 的 API 文档
/wf_14_doc --update api --ui

# 生成交互式架构文档
/wf_14_doc --update architecture --ui
```

**改进点**:
- **交互式 API 浏览器**: 生成 Swagger/OpenAPI UI 风格的交互式 API 探索界面
- **可视化组件**: 为复杂概念生成图表和交互式示例
- **代码示例增强**: 提供可运行、可修改的代码沙盒
- **架构图生成**: 基于代码结构自动生成架构图和流程图
- **配置向导**: 生成交互式配置引导界面

**Magic 在文档生成中的具体应用**:
- **API 文档**: 生成可以直接测试 API 端点的交互式界面
- **开发指南**: 提供可交互的设置向导和故障排查工具
- **架构文档**: 生成可点击、可缩放的架构图和组件关系图
- **配置文档**: 创建表单式的配置生成器

**使用场景**:
- 需要用户友好的文档展示
- API 文档需要提供在线测试功能
- 复杂架构需要可视化展示
- 配置过程需要引导式体验

---

### 禁用 MCP

```bash
# 使用标准文档生成，不启用 MCP
/wf_14_doc --no-mcp
```

---

## ⚠️ 强制语言规则

**此命令为强制语言规则的关键执行命令**。详细的强制语言规则定义请参考 [CLAUDE.md § 强制语言规则](CLAUDE.md#⚠️-强制语言规则)。

**简版要点**：
- ✅ **所有输出内容（分析报告、文档生成等）遵循项目 CLAUDE.md 的语言规范**
- ✅ **优先级**: 项目级 CLAUDE.md > 全局默认 > 命令建议
- ❌ **无例外**: 关键文档生成命令必须严格遵循

---

## 执行上下文
**输入**: 项目代码库 + 现有文档 + PLANNING.md
**输出**: 项目文档 + KNOWLEDGE.md索引更新
**依赖链**: /wf_05_code → **当前（文档生成）** → /wf_13_doc_maintain → /wf_11_commit

## 🛠️ 可用工具

**⚠️ 重要执行规则**：本命令使用以下项目工具，**必须调用而不是重新实现**

| 工具 | 路径 | 功能 | 使用方式 |
|------|------|------|---------|
| **Frontmatter 处理** | `scripts/frontmatter_utils.py` | 验证、生成、关系图 | `python ~/.claude/commands/scripts/frontmatter_utils.py [command]` |
| **文档关系图** | `scripts/doc_graph_builder.py` | 可视化文档网络 | `python ~/.claude/commands/scripts/doc_graph_builder.py [options]` |

**核心命令示例**：

> 详见 [完整示例库 - 核心命令示例](docs/examples/wf_14_doc_examples.md#核心命令示例)

**AI 执行规则**：
- ✅ **必须使用**：调用上述脚本工具完成 Frontmatter 相关操作
- ✅ **优先检查**：执行前确认 `~/.claude/commands/scripts/frontmatter_utils.py` 存在
- ❌ **绝不允许**：重新实现 Frontmatter 生成/验证功能
- ❌ **绝不允许**：创建临时脚本 `/tmp/generate_frontmatter.sh` 等替代已有工具
- ❌ **绝不允许**：在 Bash 中使用 cat/echo 等手动生成 Frontmatter

**Token 效率对比**：
- 调用工具脚本：~200 tokens
- 重新实现功能：~8000 tokens
- **节省比例**：97.5%

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

**输出示例**: 详见 [完整示例库 - 代码库分析输出](docs/examples/wf_14_doc_examples.md#1-代码库分析输出示例)

---

### 2. 文档缺口检测器 (Documentation Gap Detector)

**功能**: 自动对比代码与文档，识别以下缺口：

**检测维度**:
- ✓ **API文档** - 实际端点 vs 文档中的端点（缺失、变化、过时）
- ✓ **技术栈版本** - README 中的版本 vs 实际依赖版本
- ✓ **环境变量配置** - .env.example vs 代码中的实际环境变量
- ✓ **依赖关系同步** - 文档中的依赖 vs 实际安装的包
- ✓ **架构文档** - 架构图是否反映当前模块结构

**检测过程**:
1. 扫描代码库识别实际状态（API、依赖、配置等）
2. 读取现有文档提取已记录的状态
3. 对比两者，识别不一致
4. 按严重程度分类（高/中/低）
5. 生成详细的缺口报告

**工具实现**: 待实现脚本 `scripts/doc_gap_analyzer.py`
- 详细的检测逻辑见脚本实现
- 集成到 `/wf_14_doc` 的执行流程中

**输出示例**: 详见 [完整示例库 - 文档缺口分析](docs/examples/wf_14_doc_examples.md#2-文档缺口分析示例)

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

**用户界面示例**: 详见 [完整示例库 - 交互式向导](docs/examples/wf_14_doc_examples.md#3-交互式文档向导示例)

---

### 4. 智能信息提取器 (Smart Information Extractor)

**功能**: 从代码、配置、注释中提取文档所需信息

#### 4.1 API 文档提取

从 FastAPI、Express 等框架的路由定义自动提取 API 文档。

**示例**: 详见 [完整示例库 - API 提取示例](docs/examples/wf_14_doc_examples.md#4-信息提取示例)

#### 4.2 环境变量文档提取

从 .env.example 和代码中自动提取环境变量配置。

**示例**: 详见 [完整示例库 - 环境变量提取](docs/examples/wf_14_doc_examples.md#4-信息提取示例)

#### 4.3 依赖和技术栈提取

从 pyproject.toml、package.json、Cargo.toml 等自动提取技术栈信息。

**示例**: 详见 [完整示例库 - 信息提取示例](docs/examples/wf_14_doc_examples.md#4-信息提取示例)

#### 4.4 从测试代码提取使用示例

从现有的测试代码自动生成真实的使用示例。

**示例**: 详见 [完整示例库 - 信息提取示例](docs/examples/wf_14_doc_examples.md#4-信息提取示例)

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

**生成逻辑**（⚠️ 必须使用项目工具 `~/.claude/commands/scripts/frontmatter_utils.py`）:

**实际执行方式**：
```bash
# AI 应该执行的实际命令（不是伪代码）
python ~/.claude/commands/scripts/frontmatter_utils.py generate docs/api/new-endpoint.md

# 批量生成
python ~/.claude/commands/scripts/frontmatter_utils.py generate-batch docs/api/

# 验证生成结果
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/api/new-endpoint.md
```

**AI 执行检查清单**：
- [ ] 确认 `~/.claude/commands/scripts/frontmatter_utils.py` 文件存在
- [ ] 使用 Bash 工具调用脚本，而非重写功能
- [ ] 检查命令执行返回码（0 = 成功）
- [ ] 验证生成的 Frontmatter 格式正确
- [ ] 不创建临时脚本如 `/tmp/generate_frontmatter.sh`

**详细的生成逻辑和类型判定规则见**: [Frontmatter规范参考](docs/reference/FRONTMATTER.md) § 标准模板 § 枚举值定义

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

**学习和应用项目风格**:
1. **分析现有文档** - 提取标题、代码栅栏、列表标记、强调风格
2. **识别写作风格** - 语言选择、emoji使用、语气（专业/轻松）
3. **应用到生成** - 新生成的文档自动使用同样的风格

**自动检测的风格特征**:
- 标题风格（# 还是 underline）
- 代码栅栏（``` 还是 ~~~）
- 列表标记（- 还是 *）
- 强调方式（* 还是 _）
- 语言选择（从 CLAUDE.md 读取）
- Emoji使用（是否启用）
- 整体语气（专业/友好）

**工具实现**: 见 `scripts/doc_style_learner.py`（待实现）

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

⚠️ **必须使用项目工具** `~/.claude/commands/scripts/frontmatter_utils.py`（见 [FRONTMATTER.md § 验证逻辑](docs/reference/FRONTMATTER.md)）

**⚠️ Execution Context**: 验证脚本必须从**项目根目录**运行（详见规范文档 § 执行上下文）

**实际执行方式**：
```bash
# AI 应该执行的实际命令（不是伪代码）

# 验证单个文档
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/api/auth.md

# 批量验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 检查命令返回码
if [ $? -eq 0 ]; then
    echo "验证通过"
else
    echo "验证失败，请检查输出的错误信息"
fi
```

**工具输出示例**:
- ✓ docs/api/auth.md - 验证通过（必需字段完整、枚举值有效、日期格式正确）
- ✗ docs/api/users.md - 验证失败（缺少必需字段 'priority'，related_code 路径无效）

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

### 标准流程：约束驱动的文档生成（强制执行）⭐ NEW

**核心理念**: 在生成文档时就内置成本检查和约束验证，而非事后清理

**整体流程**:
```
代码实现（已完成）
    ↓
[Phase 1 from /wf_05_code Step 8]
文档同步决策树（确定需要生成哪些文档）
    ↓
[Phase 2 from /wf_14_doc 开始]
→ 成本估计和分层建议（自动）
→ 交互式用户确认（用户选择）
→ 生成 + 约束检查（自动）
→ 最后验证和提示（确认）
    ↓
[Phase 3 from /wf_08_review Dimension 6]
文档架构合规性检查（审查时再次验证）
    ↓
提交和保存（/wf_11_commit）
```

---

### 标准流程详细步骤

**步骤 1: 代码库分析和成本估计（约束驱动）**

本步骤在生成前估计文档成本，确保符合约束条件。

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

1.4 提取 API 和配置
    - 扫描路由定义
    - 提取端点、参数、返回类型
    - 解析环境变量
    - 提取部署配置

1.5 估计文档成本（强制执行）
    - 分析当前 KNOWLEDGE.md 大小 (行数)
    - 分析当前 docs/ 目小 (总行数)
    - 预估每个可能文档的大小
      * Type A (PLANNING.md): ~20-50 行
      * Type B (ADR): ~100-200 行
      * Type C (docs/ 文档): ~150-500 行
      * Type D (FAQ): ~20-50 行
    - 计算生成后的预期大小
    - 计算百分比增长（KNOWLEDGE.md + docs/）
    - 判断是否会超过约束阈值（见下表）

约束检查表:
┌─────────────────────────────────────────────────┐
│ 约束项 | 现有值 | 预估增加 | 生成后 | 限制 | 通过 │
├─────────────────────────────────────────────────┤
│ KNOWLEDGE.md 行数 | ? | ? | ? | <200 | ✅/❌ │
│ docs/ 总行数 | ? | ? | ? | N/A | ✅ │
│ docs/ 增长率 | ? | ? | ?% | <30% | ✅/❌ │
│ KNOWLEDGE.md 增长率 | ? | ? | ?% | <20% | ✅/❌ │
│ 新文档单个大小 | N/A | ? | ? | <500 | ✅/❌ │
└─────────────────────────────────────────────────┘

🔴 若超限: 返回错误，提示用户修改范围或分多个 commit
✅ 若符合: 继续进行步骤 2
```

**步骤 2: 文档缺口检测和分层建议（约束驱动）**

```
2.1 读取现有文档
    - README.md (如果存在)
    - docs/ 目录下的所有文档
    - KNOWLEDGE.md 已有索引

2.2 对比分析
    - API 文档 vs 实际端点
    - README 技术栈 vs 实际依赖
    - 环境变量文档 vs 实际配置
    - 开发指南 vs 当前工具链

2.3 自动分层建议（使用 Step 8.2 的决策树）
    对于每个检测到的缺口，自动确定：
    ├─ Type A: 项目级架构改动 → PLANNING.md (< 50行)
    ├─ Type B: 架构决策 → docs/adr/ (< 200行)
    ├─ Type C: API/功能文档 → docs/ (< 500行)
    ├─ Type D: 常见问题 → KNOWLEDGE.md FAQ (< 50行)
    └─ Type E: 无需文档

2.4 生成缺口报告（含成本信息）
    - 按严重程度分类
    - 显示建议的文档位置
    - 预估每个文档的大小
    - 显示总体成本影响
```

**步骤 3: 交互式用户确认（门控）**

```
3.1 展示分析结果和成本估计
    - 代码库概览
    - 文档缺口列表
    - 建议的文档和预估大小
    - 总体成本影响（百分比增长）

3.2 用户选择
    └─ 交互式确认
       ├─ 同意全部生成
       ├─ 选择部分生成（取消某些高成本项）
       └─ 取消生成（返回）

3.3 最终确认
    - 显示将要生成的最终文档列表
    - 最终的成本估计
    - 用户确认后继续，否则返回
```

**步骤 4: 智能提取和生成（约束驱动）**

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

4.3 文档生成
    - 选择合适的模板
    - 填充提取的信息
    - 应用项目风格
    - 生成文档文件

4.4 自动添加 Frontmatter
    ✅ **必须调用**：~/.claude/commands/scripts/frontmatter_utils.py

    对每个生成的文档:
    python ~/.claude/commands/scripts/frontmatter_utils.py generate <doc_path>
```

**步骤 5: 约束检查和验证（强制门控）**

```
5.1 验证 Frontmatter 完整性
    python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/

    必须全部通过:
    - ✅ 7 个必需字段完整
    - ✅ 枚举值有效
    - ✅ 日期格式正确
    - ✅ 关联路径存在

    ❌ 如果验证失败 → 返回错误，要求修复

5.2 重新计算成本影响
    - 统计实际生成的文档大小
    - 重新计算 KNOWLEDGE.md 增长率
    - 重新计算 docs/ 增长率

    🔴 若超过约束 → 请求用户:
        ① 减少文档范围
        ② 拆分成多个 commit
        ③ 先清理旧文档再提交

    ✅ 若符合约束 → 继续

5.3 更新 KNOWLEDGE.md 索引
    python ~/.claude/commands/scripts/frontmatter_utils.py update-index KNOWLEDGE.md

    必须通过:
    - ✅ 索引表已更新
    - ✅ 无重复条目
    - ✅ 链接有效
```

**步骤 6: 最终确认和报告**

```
6.1 生成最终报告
    - 总结生成的文档列表
    - 显示最终的成本影响
    - 列出更新的文件

6.2 提供后续建议
    - "文档已生成！"
    - "下一步：运行 /wf_08_review 进行代码审查"
    - "审查包括 Dimension 6 文档架构合规性检查"
    - "如果审查通过，运行 /wf_11_commit 保存进度"

6.3 记录到 KNOWLEDGE.md 文档决策
    - 类型和位置
    - 成本影响
    - 决策时间戳
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

### 1. 成本估计和分层建议报告（约束驱动 - NEW）

此报告在生成前展示成本估计，确保符合约束：

```markdown
# 📊 文档生成成本估计

## 现有文档规模
- KNOWLEDGE.md: {current_lines} 行
- docs/ 总计: {current_docs_lines} 行
- 总规模: {total_lines} 行

## 预算约束
- KNOWLEDGE.md 上限: < 200 行 (当前 {pct}% 使用)
- KNOWLEDGE.md 增长限制: < 20% per commit
- docs/ 增长限制: < 30% per commit
- 单个文档限制: < 500 行

## 检测到的文档需求

| # | 类型 | 建议位置 | 预估大小 | 约束 | 状态 |
|---|------|--------|---------|-----|------|
| 1 | Type A | PLANNING.md | ~30行 | <50 | ✅ |
| 2 | Type B | docs/adr/ | ~150行 | <200 | ✅ |
| 3 | Type C | docs/api/ | ~400行 | <500 | ✅ |
| 4 | Type D | KNOWLEDGE.md FAQ | ~25行 | <50 | ✅ |

## 成本影响预测

```
KNOWLEDGE.md:
  当前: 155 行
  增加: +25 行 (Type D)
  预计: 180 行
  增长率: +16.1% (符合 <20% 约束) ✅

docs/:
  当前: 2450 行
  增加: +580 行 (Types A,B,C)
  预计: 3030 行
  增长率: +23.7% (符合 <30% 约束) ✅

总体: 所有约束符合 ✅
```

## 后续步骤

这个估计将在用户确认后执行实际生成。
如果有文档被取消或修改，成本估计会重新计算。
```

### 2. 分析和选择报告

```markdown
# 📋 文档生成选择

## 代码库概览
- 项目: {project_name}
- 规模: {loc} LOC
- 技术栈: {tech_stack}

## 检测到的文档缺口

### ⚠️ 严重缺口 ({count})
- API 文档过时 (3 个新端点未记录)
- 环境变量文档缺失

### 📝 中等缺口 ({count})
- 开发指南需要更新
- 部署文档部分缺失

### ✅ 完整文档 ({count})
- 项目 README
- 架构决策已记录

## 建议生成的文档

```
[1] API 文档更新 (Type C)
    位置: docs/api/endpoints.md
    大小估计: ~400 行
    原因: 检测到 3 个新的 REST 端点

[2] 架构决策 (Type B)
    位置: docs/adr/2025-11-18-xxx.md
    大小估计: ~150 行
    原因: 最近的技术选型决策

[3] FAQ 更新 (Type D)
    位置: KNOWLEDGE.md § 常见问题
    大小估计: ~25 行
    原因: 3 个常见开发问题

成本影响: KNOWLEDGE.md +8%, docs/ +15% (均符合约束)
```

## 确认选择

请从下列选项中选择:

```
[ ] (1) 生成全部建议的文档
[ ] (2) 自定义选择 (输入编号, 如: 1,3)
[ ] (3) 取消 (返回不生成)
```
```

### 3. 生成和验证报告（约束驱动）

```markdown
# ✅ 文档生成完成（约束已验证）

## 生成的文档 ({count})
1. ✅ docs/api/endpoints.md (400 行) - Type C
2. ✅ docs/adr/2025-11-18-xxx.md (145 行) - Type B
3. ✅ KNOWLEDGE.md FAQ 补充 (24 行) - Type D

## Frontmatter 验证
- ✅ 所有文档都有完整的 Frontmatter
- ✅ 7 个必需字段完整
- ✅ 枚举值有效，日期格式正确
- ✅ related_documents 和 related_code 已填写

## 成本验证（约束检查）
```
约束检查结果:
  ✅ KNOWLEDGE.md 行数: 155 → 179 (< 200)
  ✅ KNOWLEDGE.md 增长: +15.5% (< 20%)
  ✅ docs/ 增长: +18.7% (< 30%)
  ✅ 单个文档: 400 < 500, 145 < 200, 24 < 50

所有约束符合 ✅
```

## 索引更新
- KNOWLEDGE.md 索引: 添加 3 个条目（API, FAQ, ADR）
- 文档关系图: 已更新

## 下一步（强制工作流）

```
✅ 文档已生成且通过约束检查！

推荐工作流:
1. /wf_08_review          ← 执行 Dimension 6 文档架构合规性检查
2. [审查通过]
3. /wf_11_commit          ← 提交文档和记录决策

命令序列:
  /wf_08_review
  /wf_11_commit "docs: 生成 API 和 FAQ 文档"
```
```
```

---

### 4. Enhanced Output with --ui (Magic)

**当使用 `--ui` 标志时，文档生成额外包含交互式 UI 组件**:

#### 4.1 交互式 API 文档

```markdown
# ✅ 生成交互式 API 文档

## 生成的文档
1. ✅ docs/api/endpoints.md (标准 Markdown)
2. ✅ docs/api/explorer.html (交互式 API 浏览器)

## 交互式组件特性
- **API 浏览器**: Swagger/OpenAPI UI 风格的界面
  - 可以直接在浏览器中测试 API
  - 自动生成请求示例
  - 显示响应状态和数据
  - 支持认证 token 配置

- **代码示例沙盒**: 可运行的代码片段
  - 支持多种编程语言
  - 可修改和立即执行
  - 实时显示输出结果

- **参数配置器**: 表单式的请求构建
  - 自动验证输入
  - 提供默认值建议
  - 生成 cURL 命令

## 使用方式
```bash
# 启动本地文档服务器
cd docs/api
python -m http.server 8000

# 浏览器访问
open http://localhost:8000/explorer.html
```
```

#### 4.2 交互式架构文档

```markdown
# ✅ 生成交互式架构文档

## 生成的文档
1. ✅ docs/architecture/system-design.md (标准 Markdown)
2. ✅ docs/architecture/interactive-diagram.html (交互式架构图)

## 可视化组件
- **架构图**: 可点击、可缩放的系统架构图
  - 组件间的依赖关系
  - 数据流向可视化
  - 模块详情弹窗

- **流程图**: 动态展示业务流程
  - 步骤间的条件分支
  - 错误处理路径
  - 时序图展示

- **组件浏览器**: 分层展示系统组件
  - 可折叠的组件树
  - 组件详情面板
  - 代码链接跳转
```

#### 4.3 交互式开发指南

```markdown
# ✅ 生成交互式开发指南

## 生成的文档
1. ✅ docs/development/setup.md (标准 Markdown)
2. ✅ docs/development/setup-wizard.html (交互式设置向导)

## 交互式向导特性
- **环境检测**: 自动检测用户系统环境
  - 操作系统识别
  - 依赖版本检查
  - 配置冲突检测

- **步骤引导**: 逐步完成环境设置
  - 进度条显示
  - 命令自动生成
  - 一键复制执行

- **故障排查工具**: 交互式问题诊断
  - 常见问题自动检测
  - 解决方案建议
  - 日志分析辅助
```

#### 4.4 成本和限制

**使用 Magic 的额外考虑**:

```
Token 成本:
  标准文档生成: ~2000 tokens
  + Magic UI 生成: ~5000 tokens
  总计: ~7000 tokens (约 3.5x)

时间成本:
  标准文档生成: ~30 秒
  + Magic UI 生成: ~60 秒
  总计: ~90 秒 (约 3x)

质量提升:
  - 用户体验: +80% (交互式 vs 静态文档)
  - 文档可用性: +60% (可测试、可验证)
  - 学习效率: +50% (可视化、可实验)

推荐使用场景:
  ✅ 面向外部用户的 API 文档
  ✅ 复杂架构需要可视化
  ✅ 开发指南需要逐步引导
  ❌ 内部简单文档 (成本/收益不划算)
  ❌ 频繁变更的文档 (维护成本高)
```

**生成的文件结构**:
```
docs/
├── api/
│   ├── endpoints.md         (标准 Markdown)
│   └── explorer.html        (交互式 UI)
├── architecture/
│   ├── system-design.md     (标准 Markdown)
│   └── interactive-diagram.html
└── development/
    ├── setup.md             (标准 Markdown)
    └── setup-wizard.html    (交互式向导)
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

详见 [完整示例库 - 完整执行示例](docs/examples/wf_14_doc_examples.md#5-完整执行示例)

包含以下 3 个完整场景：
- 新项目首次生成文档
- 代码更新后更新 API 文档
- CI/CD 检查模式

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

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[项目启动] → [任务规划] → [加载上下文] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [文档生成 ← 当前] → [文档维护] → [提交保存]
  STEP 0       STEP 0.5        STEP 1         STEP 2       STEP 3       STEP 4       STEP 5        STEP 8.5            STEP 8      STEP 6
```

### ✅ 已完成的步骤

执行 `/wf_14_doc` 前，应该已经完成：

1. ✅ **代码实现** (STEP 3) - 功能开发完成 (`/wf_05_code`)
2. ✅ **测试验证** (STEP 4) - 所有测试通过 (`/wf_07_test`)
3. ✅ **代码审查** (STEP 5) - 代码审查通过 (`/wf_08_review`)
4. ✅ **代码提交** (STEP 6 前置) - 代码已保存 (`/wf_11_commit`)

### 📝 当前步骤

**正在执行**: `/wf_14_doc [OPTIONS]` (智能文档生成和维护)

**这个命令的职责**：
- 分析代码库结构和技术栈
- 识别文档缺口
- 从代码和配置中智能提取信息
- 生成或更新项目文档
- 为技术文档自动生成 Frontmatter 元数据
- 更新 KNOWLEDGE.md 文档索引
- 遵循"提取而非编造"原则

### ⏭️ 建议下一步

**文档生成完成后**，根据生成结果选择下一步：

#### 路径 1️⃣：文档生成完成，进入维护 ✅

```bash
# 当前: 文档已成功生成或更新
# 下一步: 文档结构维护和优化

/wf_13_doc_maintain --auto

# 或者使用 --dry-run 预览可能的改动
/wf_13_doc_maintain --dry-run

# 维护完成后重新加载上下文
/wf_03_prime

# 然后提交
/wf_11_commit "docs: 生成和优化项目文档"
```

**适用场景**: 文档生成或更新完成，需要进行文档结构维护和审查

#### 路径 2.：需要调整和完善生成的文档 🔧

```bash
# 当前: AI 生成的文档需要人工审查和完善
# 下一步: 手动调整文档细节

# 1. 审查生成的文档
# 2. 补充业务背景、使用建议、最佳实践
# 3. 添加图表或自定义示例
# 4. 验证代码示例的准确性

# 完成调整后运行验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 然后进行文档维护
/wf_13_doc_maintain --auto

# 最后提交
/wf_11_commit "docs: 完善自动生成的文档"
```

**适用场景**: AI 生成的文档需要人工补充或调整，不是简单的生成而已

#### 路径 3️⃣：发现文档结构或架构问题 🐛

```bash
# 当前: 文档生成过程中发现代码结构或架构问题
# 下一步: 修复根本问题

# 如果是代码问题
/wf_06_debug "文档生成时发现的问题描述"

# 或需要代码重构
/wf_09_refactor "根据文档生成需要重构的部分"

# 修复完成后重新生成文档
/wf_14_doc

# 然后进行维护和提交
/wf_13_doc_maintain --auto
/wf_11_commit "refactor: 改进代码结构，更新文档"
```

**适用场景**: 文档生成过程暴露了代码或架构问题，需要先修复代码

#### 路径 4️⃣：文档完成，进入提交流程 📝

```bash
# 当前: 文档已完成并验证（通过 Frontmatter 验证）
# 下一步: 提交所有更改

# 1. 确认所有文档都有有效的 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 2. 重新加载上下文（如果有大量文档变化）
/wf_03_prime

# 3. 提交更改
/wf_11_commit "docs: 自动生成和更新项目文档"

# 4. 后续继续开发
/wf_05_code "实现下一个功能"
```

**适用场景**: 所有文档都已完成、验证，准备提交

### 📊 工作流进度提示

当你完成文档生成时，确保输出中包含：

✅ 已完成:
- 代码库分析报告（技术栈、架构、API 识别）
- 文档缺口分析（识别缺失和过时的文档）
- 生成或更新的文档清单
- KNOWLEDGE.md 索引更新情况
- 所有生成文档的 Frontmatter 验证结果
- 文档生成时间统计

⏭️ 下一步提示:
- 建议执行的路径（4 个选项之一）
- 是否需要人工完善文档
- 是否发现了代码结构问题
- 推荐使用 `/wf_13_doc_maintain` 进行结构整理

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 文档生成完成，无问题 | 路径 1 | /wf_13_doc_maintain → /wf_11_commit |
| 文档生成有问题需完善 | 路径 2 | 手动调整 → 验证 → /wf_13_doc_maintain → /wf_11_commit |
| 发现代码结构问题 | 路径 3 | /wf_06_debug 或 /wf_09_refactor → /wf_14_doc → /wf_13_doc_maintain |
| 文档完成准备提交 | 路径 4 | 验证 → /wf_03_prime → /wf_11_commit |

**何时生成文档？**
- ✅ 完成新功能实现后
- ✅ 添加新 API 端点后
- ✅ 修改配置或环境变量后
- ✅ 重构架构后
- ✅ 项目初始化时

**何时使用不同的选项？**
- `--update <type>` - 只更新特定类型文档（快速更新）
- `--check` - 只检查不生成（用于 CI/CD）
- `--auto` - 自动生成所有缺失文档（无交互）
- （默认）- 交互式选择要生成的文档

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
