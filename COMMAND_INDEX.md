# Command Index - Lazy Loading Configuration

**Version**: 1.0
**Created**: 2025-12-08
**Purpose**: Enable command-level lazy loading to reduce session startup token consumption

## Optimization Target

**Baseline**: All 16 commands loaded at startup (~15,000 tokens)
**Target**: Load only essential command index (~500 tokens)
**Savings**: ~14,500 tokens (97% reduction)

## Always Load (Session Startup)

**Minimal essential metadata** - loaded in Quick Start mode:

- `COMMAND_INDEX.md` (this file) - ~500 tokens
- Essential context: PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md

**Philosophy**: Load command metadata, not full command content. Full commands loaded on-demand when invoked.

---

## Command Registry

### 01 - Foundation Commands (基础设施)

#### /wf_01_planning
- **Phase**: 基础设施
- **Model**: sonnet
- **Token Budget**: complex
- **Description**: 创建/更新项目规划文档，建立架构和开发标准
- **Usage**: `/wf_01_planning <PROJECT_NAME>`
- **Typical Use**: New project setup, major architecture changes
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,200

#### /wf_02_task
- **Phase**: 基础设施
- **Model**: haiku
- **Token Budget**: simple
- **Description**: 管理任务追踪系统，支持创建、更新和审查模式
- **Usage**: `/wf_02_task [update|create|review]`
- **Typical Use**: Task management throughout project
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 800

#### /wf_03_prime ⭐
- **Phase**: 基础设施
- **Model**: haiku
- **Token Budget**: medium
- **Description**: 加载项目管理文档到AI上下文（会话必备）| MCP: Serena (自动激活)
- **Usage**: `/wf_03_prime [--quick|--task|--full]` OR `/wf_03_prime --load-docs`
- **Typical Use**: **EVERY session start** (mandatory)
- **Load Trigger**: Auto-loaded in all modes (this is the entry point)
- **Estimated Tokens**: 1,000
- **Special**: This command controls loading strategy for entire session

---

### 02 - Development Commands (开发实现)

#### /wf_04_ask
- **Phase**: 开发实现
- **Model**: sonnet
- **Token Budget**: complex
- **Description**: 架构咨询服务，支持技术决策和代码库审查，集成 Ultrathink 设计思维 | MCP: --think | --c7 | --research | --review-codebase
- **Usage**: `/wf_04_ask "<question>" [--think] [--c7] [--research] [--review-codebase]`
- **Typical Use**: Technical decisions, architecture consultation
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,500

#### /wf_04_research
- **Phase**: 开发实现
- **Model**: sonnet
- **Token Budget**: complex
- **Description**: 开源方案深度研究，系统化评估和对比技术选项 | MCP: --c7 | --research
- **Usage**: `/wf_04_research "<topic>" [--c7] [--research]`
- **Typical Use**: Deep technology research, open-source solution comparison
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,400

#### /wf_05_code
- **Phase**: 开发实现
- **Model**: sonnet
- **Token Budget**: complex
- **Description**: 功能实现协调器，遵循架构标准编写代码，集成 Ultrathink 优雅实现 | MCP: --ui / --serena
- **Usage**: `/wf_05_code "<feature>" [--ui] [--serena]`
- **Typical Use**: Feature implementation, code writing
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,800
- **MCP Support**: Magic (--ui), Serena (--serena)

#### /wf_06_debug
- **Phase**: 开发实现
- **Model**: sonnet
- **Token Budget**: medium
- **Description**: 系统化调试修复，支持快速修复模式 | MCP: --think | --deep
- **Usage**: `/wf_06_debug "<error>" [--quick] [--think] [--deep]`
- **Typical Use**: Bug fixing, error diagnosis
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,200
- **MCP Support**: Sequential-thinking (--think), Serena (--deep)

---

### 03 - Quality Assurance Commands (质量保证)

#### /wf_07_test
- **Phase**: 质量保证
- **Model**: sonnet
- **Token Budget**: medium
- **Description**: 测试开发和覆盖率分析，支持coverage模式
- **Usage**: `/wf_07_test "<component>" [--coverage]`
- **Typical Use**: Test development, coverage analysis
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,000
- **MCP Support**: Serena (auto-activated)

#### /wf_08_review
- **Phase**: 质量保证
- **Model**: sonnet
- **Token Budget**: medium
- **Description**: 代码审查协调器，多维度质量检查，集成 Ultrathink 设计优雅度评审
- **Usage**: `/wf_08_review`
- **Typical Use**: Code review before commit
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,300
- **MCP Support**: Serena (conditional activation)

#### /wf_09_refactor
- **Phase**: 质量保证
- **Model**: sonnet
- **Token Budget**: medium
- **Description**: 代码重构服务，保持架构一致性
- **Usage**: `/wf_09_refactor "<scope>"`
- **Typical Use**: Code structure improvement
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,000
- **MCP Support**: Serena (auto-activated)

#### /wf_10_optimize
- **Phase**: 质量保证
- **Model**: sonnet
- **Token Budget**: medium
- **Description**: 性能优化协调器，满足性能目标
- **Usage**: `/wf_10_optimize "<target>"`
- **Typical Use**: Performance optimization
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 900

---

### 04 - Operations Commands (运维部署)

#### /wf_11_commit
- **Phase**: 运维部署
- **Model**: haiku
- **Token Budget**: simple
- **Description**: Git提交管理，自动更新CONTEXT和格式化
- **Usage**: `/wf_11_commit [message]`
- **Typical Use**: Save progress, update session state
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 700

#### /wf_12_deploy_check
- **Phase**: 运维部署
- **Model**: haiku (inferred)
- **Token Budget**: simple
- **Description**: 部署就绪检查，多层验证和Go/No-Go决策
- **Usage**: `/wf_12_deploy_check "<target>"`
- **Typical Use**: Deployment readiness validation
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 600

---

### 05 - Documentation Commands (文档管理)

#### /wf_13_doc_maintain
- **Phase**: 文档维护
- **Model**: haiku
- **Token Budget**: simple
- **Description**: 文档架构维护，索引更新和归档管理
- **Usage**: `/wf_13_doc_maintain [--auto] [--dry-run]`
- **Typical Use**: Periodic documentation cleanup (every 10 commits or quarterly)
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 800

#### /wf_14_doc
- **Phase**: 文档管理
- **Model**: sonnet (inferred)
- **Token Budget**: medium
- **Description**: 智能文档助手，从代码库提取信息生成和维护项目文档 | MCP: --ui
- **Usage**: `/wf_14_doc [--ui]`
- **Typical Use**: Generate/update project documentation from code
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 1,200
- **MCP Support**: Magic (--ui)

---

### 06 - Support Commands (支持命令)

#### /wf_99_help
- **Phase**: 支持命令
- **Model**: haiku
- **Token Budget**: simple
- **Description**: 工作流帮助系统，提供命令参考和使用指导
- **Usage**: `/wf_99_help [command|guide|quick]`
- **Typical Use**: Get help on commands, workflows
- **Load Trigger**: User invokes command explicitly
- **Estimated Tokens**: 500

---

## Phase Grouping

### 基础设施 (Foundation) - Always Needed
- `/wf_01_planning` - Project setup
- `/wf_02_task` - Task tracking
- `/wf_03_prime` ⭐ - **Context loading (MANDATORY every session)**

### 开发实现 (Development) - Load on Demand
- `/wf_04_ask` - Architecture consultation
- `/wf_04_research` - Technology research
- `/wf_05_code` - Feature implementation
- `/wf_06_debug` - Bug fixing

### 质量保证 (Quality) - Load on Demand
- `/wf_07_test` - Testing
- `/wf_08_review` - Code review
- `/wf_09_refactor` - Refactoring
- `/wf_10_optimize` - Performance optimization

### 运维部署 (Operations) - Load on Demand
- `/wf_11_commit` - Git commits
- `/wf_12_deploy_check` - Deployment validation

### 文档管理 (Documentation) - Load on Demand
- `/wf_13_doc_maintain` - Documentation maintenance
- `/wf_14_doc` - Documentation generation

### 支持命令 (Support) - Lightweight, Always Available
- `/wf_99_help` - Help system

---

## Token Budget Classification

### Simple Commands (< 800 tokens)
- `/wf_02_task` (800)
- `/wf_11_commit` (700)
- `/wf_12_deploy_check` (600)
- `/wf_99_help` (500)

### Medium Commands (800-1,300 tokens)
- `/wf_03_prime` (1,000)
- `/wf_06_debug` (1,200)
- `/wf_07_test` (1,000)
- `/wf_08_review` (1,300)
- `/wf_09_refactor` (1,000)
- `/wf_10_optimize` (900)
- `/wf_13_doc_maintain` (800)
- `/wf_14_doc` (1,200)

### Complex Commands (> 1,300 tokens)
- `/wf_01_planning` (1,200)
- `/wf_04_ask` (1,500)
- `/wf_04_research` (1,400)
- `/wf_05_code` (1,800)

---

## Lazy Loading Strategy

### Session Startup (Quick Start Mode)
**Load**:
- This index file (`COMMAND_INDEX.md`) - ~500 tokens
- Core management docs (via `/wf_03_prime --quick`) - ~2,000 tokens
- **Total**: ~2,500 tokens

### On Command Invocation
**Load**:
- Full command file (frontmatter + implementation steps)
- Associated guides (if `docs_dependencies` specified)
- MCP configurations (if MCP support enabled)

### Example Flow
```
Session start:
  → Load COMMAND_INDEX.md (500 tokens)
  → Run /wf_03_prime --quick (loads core docs, 2,000 tokens)
  → TOTAL: 2,500 tokens loaded

User runs /wf_05_code "implement feature":
  → Load wf_05_code.md (1,800 tokens)
  → Load guides if --serena flag (1,243 tokens, optional)
  → Execute implementation

User runs /wf_08_review:
  → Load wf_08_review.md (1,300 tokens)
  → Execute review
```

**Savings**:
- **Before**: All 16 commands loaded (~15,000 tokens)
- **After**: Index + invoked commands only (~2,500 base + ~1,500 per command)
- **Typical session (3-4 commands)**: ~7,000 tokens vs 15,000 = **~8,000 tokens saved (53%)**

---

## MCP-Enabled Commands

Commands with MCP (Model Context Protocol) integration:

| Command | MCP Servers | Flags | Auto/Manual |
|---------|-------------|-------|-------------|
| `/wf_03_prime` | Serena | 自动激活 | Auto |
| `/wf_04_ask` | Sequential-thinking, Context7, Tavily | --think, --c7, --research | Manual |
| `/wf_04_research` | Context7, Tavily | --c7, --research | Manual |
| `/wf_05_code` | Magic, Serena | --ui, --serena | Manual |
| `/wf_06_debug` | Sequential-thinking, Serena | --think, --deep | Manual |
| `/wf_07_test` | Serena | 自动激活 | Auto |
| `/wf_08_review` | Serena | 条件激活 | Conditional |
| `/wf_09_refactor` | Serena | 自动激活 | Auto |
| `/wf_14_doc` | Magic | --ui | Manual |

**Note**: MCP server initialization is also lazy-loaded via `src/mcp/gateway.py`

---

## Implementation Notes

1. **Backward Compatibility**: If `COMMAND_INDEX.md` not found, fall back to loading all commands
2. **Cache Strategy**: Command content cached after first load in session
3. **Update Mechanism**: When command files updated, regenerate this index
4. **Validation**: Run `/wf_03_prime --verify` to check index consistency
5. **Token Tracking**: Monitor actual vs estimated token usage for accuracy

---

## Usage in /wf_03_prime

**Quick Start Mode** (default):
```bash
/wf_03_prime
# Loads: COMMAND_INDEX.md + core management docs
# Token cost: ~2,500 tokens
```

**Full Mode** (comprehensive loading):
```bash
/wf_03_prime --full
# Loads: All commands + all docs
# Token cost: ~25,000 tokens (for deep work sessions)
```

**Command-Specific Loading**:
- Commands automatically load their full definition when invoked
- Associated guides load via `docs_dependencies` declarations
- MCP configurations load on-demand based on flags

---

**Maintenance**: Update this index when:
- New commands added
- Command descriptions/usage changes
- Token estimates need adjustment (after usage analytics)
- MCP integration changes

**Version Control**: Track changes to this file for command evolution history.
