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
token_budget: medium
mcp_support:
  - name: "Magic"
    flag: "--ui"
    detail: "UI文档和组件示例生成"
docs_dependencies:
  examples:
    - docs/examples/doc_generation_quick_guide.md
    - docs/examples/doc_generation_decision_tree.md
    - docs/examples/frontmatter_quick_reference.md
  references:
    - docs/reference/FRONTMATTER.md
  estimated_tokens: 1728
  lazy_load: true
  note: "仅在需要详细指导时加载（如Frontmatter规范、决策树）"
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

**标准文档模板库**：详见 [docs/examples/doc_templates/](docs/examples/doc_templates/)

本命令支持以下5种标准文档类型，每种类型都有专门的模板文件：

| 文档类型 | 模板文件 | 用途 |
|---------|---------|------|
| 📚 项目概览 | [README_template.md](docs/examples/doc_templates/README_template.md) | 项目主文档 (README.md) |
| 🔌 API 文档 | [API_template.md](docs/examples/doc_templates/API_template.md) | API 端点文档 (docs/api/) |
| ⚙️ 开发指南 | [DEV_GUIDE_template.md](docs/examples/doc_templates/DEV_GUIDE_template.md) | 开发环境设置 (docs/development/) |
| 🚀 部署文档 | [DEPLOYMENT_template.md](docs/examples/doc_templates/DEPLOYMENT_template.md) | 部署指南 (docs/deployment/) |
| 🏗️ 架构文档 | [ARCHITECTURE_template.md](docs/examples/doc_templates/ARCHITECTURE_template.md) | 系统架构 (docs/architecture/) |

所有模板都包含完整的章节结构和占位符，可以直接使用或根据项目需求调整。

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

**完整的6步约束驱动工作流**：详见 [docs/examples/doc_generation_workflow.md](docs/examples/doc_generation_workflow.md)

**概要**：

| 步骤 | 名称 | 职责 | 关键点 |
|-----|------|------|-------|
| Step 1 | 代码库分析和成本估计 | 扫描项目、识别技术栈、估计文档成本 | 约束检查表（KNOWLEDGE.md <200行，docs/ 增长<30%） |
| Step 2 | 文档缺口检测和分层建议 | 对比实际与文档、自动分层建议 | Type A/B/C/D/E 决策树 |
| Step 3 | 交互式用户确认 | 展示成本估计、用户选择 | 门控点（确认或取消） |
| Step 4 | 智能提取和生成 | 提取信息、学习风格、生成文档 | 自动调用 frontmatter_utils.py |
| Step 5 | 约束检查和验证 | Frontmatter 验证、成本重算 | 强制门控（超限拒绝） |
| Step 6 | 最终确认和报告 | 生成报告、提供后续建议 | 建议运行 /wf_08_review |

详细的每个步骤的子步骤、约束表格、检查清单见工作流文档。

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

**完整的输出格式示例和报告模板**：详见 [docs/examples/doc_generation_outputs.md](docs/examples/doc_generation_outputs.md)

本命令在不同阶段生成3种标准报告格式：

| 报告类型 | 阶段 | 用途 | 包含内容 |
|---------|------|------|---------|
| **成本估计和分层建议报告** | Step 1-2 | 生成前的约束检查和成本预测 | 现有文档规模、预算约束、文档需求表、成本影响预测 |
| **分析和选择报告** | Step 3 | 交互式用户确认 | 代码库概览、文档缺口分析、建议生成的文档、交互式确认选项 |
| **生成和验证报告** | Step 5-6 | 约束驱动的完成报告 | 生成的文档清单、Frontmatter 验证、成本验证、索引更新、下一步建议 |

详细的报告格式、示例文本、约束表格见输出格式文档。

---

### 4. Enhanced Output with --ui (Magic)

**完整的 UI 增强文档和成本分析**：详见 [docs/examples/doc_templates/ui_enhanced/](docs/examples/doc_templates/ui_enhanced/)

当使用 `--ui` 标志启用 Magic MCP 时，文档生成将包含交互式 UI 组件：

| UI 组件类型 | 模板文件 | 用途 | 特性 |
|-----------|---------|------|------|
| 🔌 交互式 API 浏览器 | [API_explorer_template.md](docs/examples/doc_templates/ui_enhanced/API_explorer_template.md) | API 文档增强 | Swagger 风格界面、在线测试、代码沙盒 |
| 🏗️ 交互式架构图 | [ARCHITECTURE_diagram_template.md](docs/examples/doc_templates/ui_enhanced/ARCHITECTURE_diagram_template.md) | 架构文档可视化 | 可点击架构图、动态流程图、组件浏览器 |
| ⚙️ 交互式开发向导 | [DEV_wizard_template.md](docs/examples/doc_templates/ui_enhanced/DEV_wizard_template.md) | 开发指南增强 | 环境检测、步骤引导、故障排查工具 |
| 💰 成本和限制分析 | [UI_COST_ANALYSIS.md](docs/examples/doc_templates/ui_enhanced/UI_COST_ANALYSIS.md) | 决策参考 | Token 成本 (3.5x)、时间成本 (3x)、质量提升、推荐场景 |

详细的 UI 组件特性、使用方式、文件结构、成本对比见 UI 增强模板文档。

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

**完整的最佳实践指南**：详见 [docs/examples/doc_generation_best_practices.md](docs/examples/doc_generation_best_practices.md)

**核心要点**:

1. **何时运行** - 完成新功能、添加 API 端点、重构架构后
2. **审查流程** - AI 生成是基础，需人工审查技术准确性和完整性
3. **增量更新** - 使用 `--update <type>` 而非全量重新生成
4. **工作流集成** - 配合 /wf_05_code → /wf_07_test → /wf_08_review → /wf_14_doc → /wf_11_commit

完整内容包括：使用时机、审查检查清单、增量更新策略、CI/CD 集成、性能优化等

---

## Limitations and Troubleshooting

**完整的故障排查和限制说明**：详见 [docs/examples/doc_generation_troubleshooting.md](docs/examples/doc_generation_troubleshooting.md)

**当前限制**:
- **语言**: 主要支持 Python/JS/Rust/Go，部分支持 Java/C#
- **框架**: Web (FastAPI, Express, Flask), CLI (Click, Clap), 其他需手动完善
- **准确性**: 依赖代码注释质量，动态端点可能遗漏

**常见问题**: 端点遗漏、风格不一致、自定义模板、性能优化、敏感信息处理等（详见故障排查文档）

---

## 📌 Workflow Navigation

**完整的工作流导航和后续步骤指南**：详见 [docs/examples/doc_generation_next_steps.md](docs/examples/doc_generation_next_steps.md)

**工作流位置**: `/wf_05_code → /wf_07_test → /wf_08_review → /wf_14_doc (当前) → /wf_13_doc_maintain → /wf_11_commit`

**四种后续路径**:
1. **路径 1** - 文档维护：`/wf_13_doc_maintain --auto` → `/wf_11_commit`
2. **路径 2** - 人工完善：手动调整 → 验证 → `/wf_13_doc_maintain`
3. **路径 3** - 修复问题：`/wf_06_debug` 或 `/wf_09_refactor` → 重新生成
4. **路径 4** - 直接提交：验证 Frontmatter → `/wf_03_prime` → `/wf_11_commit`

**路径选择决策表**和完整命令序列详见后续步骤文档

---

**See Also**:
- [/wf_05_code](wf_05_code.md) - 代码实现
- [/wf_13_doc_maintain](wf_13_doc_maintain.md) - 文档维护
- [/wf_11_commit](wf_11_commit.md) - 提交更改
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计哲学指南
