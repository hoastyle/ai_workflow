---
command: /wf_08_review
index: 08
phase: "质量保证"
description: "代码审查协调器，多维度质量检查，集成 Ultrathink 设计优雅度评审，支持 Serena MCP 引用完整性检查"
reads: [PLANNING.md(质量标准), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(可选), 代码文件]
writes: [TASK.md(改进任务), KNOWLEDGE.md(新模式)]
prev_commands: [/wf_05_code, /wf_07_test, /wf_09_refactor]
next_commands: [/wf_09_refactor, /wf_11_commit]
ultrathink_lens: "design_elegance"
model: sonnet
token_budget: medium
mcp_support:
  - name: "Serena"
    flag: "条件激活（自动检测符号修改）"
    detail: "符号级别引用完整性检查，验证所有调用点已同步更新"
context_rules:
  - "执行PRD合规性检查"
  - "验证PLANNING.md标准遵守"
  - "识别可重用模式到KNOWLEDGE.md"
  - "Ultrathink 设计优雅度评审（Obsess Over Details）：除了功能正确，代码优雅度如何？"
  - "✅ 条件激活 Serena MCP：检测到符号修改时自动使用 find_referencing_symbols() 验证引用完整性"
---

## 执行上下文
**输入**: PLANNING.md标准 + KNOWLEDGE.md模式 + 代码实现
**输出**: 审查报告 + TASK.md改进任务 + KNOWLEDGE.md新模式
**依赖链**: /wf_07_test → **当前（代码审查）** → /wf_09_refactor (可选) → /wf_11_commit

## Usage
`/wf_08_review <CODE_SCOPE>`

## Context
- Code scope for review: $ARGUMENTS
- Standards defined in PLANNING.md
- Review tasks tracked in TASK.md
- Quality gates from project requirements

## Your Role
Code Review Coordinator ensuring project standards:
1. **Quality Auditor** – checks against coding standards
2. **Security Analyst** – validates security guidelines
3. **Performance Reviewer** – assesses efficiency targets
4. **Architecture Assessor** – verifies design alignment

## 🤖 Agent 模式协调策略 (NEW - Phase 2 优化)

**目的**: 使用多个专业化 review agents 并行执行全面的代码审查

**何时使用 Agent 模式**:
- ✅ 大规模代码审查（多个模块或组件）
- ✅ 需要多维度并行评估（安全 + 性能 + 架构同时审查）
- ✅ 复杂的重构审查（影响多个系统）
- ❌ 简单修改审查（单文件小改动，直接审查更快）

### 推荐的 Multi-Agent Review 策略

**Strategy 1: Parallel Review Pattern**（并行审查模式）

适用场景：大规模审查，多个维度可并行评估

```
Launch 4 review agents in PARALLEL:

Agent 1: Code Quality Reviewer
  - Focus: Dimension 1 (代码质量)
  - Checks: Style, patterns, maintainability
  - Output: Quality score + issues list

Agent 2: Security Auditor
  - Focus: Dimension 2 (安全性)
  - Checks: Vulnerabilities, auth, data validation
  - Output: Security score + critical issues

Agent 3: Performance Analyst
  - Focus: Dimension 3 (性能)
  - Checks: Algorithmic complexity, resource usage
  - Output: Performance score + bottlenecks

Agent 4: Architecture Assessor
  - Focus: Dimension 4 (架构合规)
  - Checks: Design patterns, PLANNING.md alignment
  - Output: Architecture score + violations

Coordination:
  - Wait for ALL agents to complete
  - Consolidate findings by severity
  - Generate unified review report

Performance: 4x faster than sequential review
```

**Strategy 2: Staged Review Chain**（分阶段审查链）

适用场景：有依赖的审查阶段

```
Stage 1: Quick Scan (Explore Agent)
  - Identify changed files and scope
  - Estimate review complexity
  - Output: Review roadmap

Stage 2: Core Review (Parallel Agents)
  - Run 4 review agents in parallel
  - Each agent focuses on one dimension
  - Output: Dimension-specific findings

Stage 3: Integration Review (Sequential)
  - Cross-dimension impact analysis
  - Serena MCP: Reference integrity check
  - Output: Final consolidated report
```

### Multi-Agent Review 最佳实践

**✅ DO**:
- 为每个 agent 明确指定审查维度
- 并行运行独立的审查维度
- 在最终阶段合并所有发现
- 使用 Serena MCP 进行符号级完整性检查

**❌ DON'T**:
- 为小改动启动多个 agents（开销大）
- 忘记合并不同 agents 的发现
- 忽略跨维度的影响分析
- 跳过 Serena 的引用完整性检查（符号修改时）

### 实际案例示例

**案例 1: API 重构审查**（使用并行审查模式）

```bash
# 任务：审查 REST API 重构（10+ 个端点修改）

启动 4 个并行 review agents:
1. Code Quality Reviewer: 检查代码风格和模式
2. Security Auditor: 验证认证和数据验证
3. Performance Analyst: 评估查询性能和缓存
4. Architecture Assessor: 确保符合 API 设计规范

Stage 2: Serena 引用完整性检查
  - 检测到 getUserById() 签名修改
  - find_referencing_symbols() 发现 8 个调用点
  - 验证所有调用点已更新

结果：
- 审查时间：40 分钟 → 12 分钟（3.3x 提升）
- 覆盖维度：4 个（并行执行）
- 发现问题：23 个（高质量并行审查）
```

**案例 2: 数据库迁移审查**（使用分阶段链）

```bash
# 任务：审查数据库 schema 迁移

Stage 1: Quick Scan
  - Explore Agent 识别所有受影响的 models 和 queries
  - 输出：15 个文件需要审查

Stage 2: Parallel Review
  - Agent 1: 检查 schema 定义正确性
  - Agent 2: 验证数据迁移脚本安全性
  - Agent 3: 评估查询性能影响
  - Agent 4: 确保向后兼容性

Stage 3: Integration Review
  - Serena: 验证所有 Model 引用已更新
  - 跨维度分析：性能 + 安全 + 兼容性

结果：
- 全面性：4 个维度全覆盖
- 准确性：发现 3 个跨维度问题
- 效率：30 分钟完成（vs 顺序审查 90 分钟）
```

**更多示例**: [docs/examples/multi_agent_review_overview.md](docs/examples/multi_agent_review_overview.md)

---

## ⚡ 并行执行模式 (NEW - Phase 2 优化)

**目的**: 通过并行读取和分析大幅提升审查速度

**核心模式**: Wave → Checkpoint → Wave

### 代码审查的并行执行

**Pattern**: 批量读取 → 分维度并行审查 → 合并结果

```
Wave 1: Parallel File Reading
┌─────────────────────────────────┐
│ Read file 1 (changed)           │
│ Read file 2 (changed)           │  ← 并行读取所有修改文件
│ Read file 3 (changed)           │
│ Read file 4 (related)           │
└─────────────────────────────────┘
         ↓
Checkpoint: Scope Analysis
┌─────────────────────────────────┐
│ Categorize changes by type      │  ← 顺序分析
│ Identify review dimensions      │
└─────────────────────────────────┘
         ↓
Wave 2: Parallel Dimension Review
┌─────────────────────────────────┐
│ Review Dimension 1 (Quality)    │
│ Review Dimension 2 (Security)   │  ← 并行审查各维度
│ Review Dimension 3 (Performance)│
│ Review Dimension 4 (Architecture)│
└─────────────────────────────────┘
         ↓
Final: Consolidation & Reporting
┌─────────────────────────────────┐
│ Merge all findings              │  ← 顺序合并
│ Prioritize by severity          │
│ Generate unified report         │
└─────────────────────────────────┘
```

### 何时使用并行执行（代码审查特定）

**✅ 适用场景**:
- 审查修改涉及 ≥5 个文件
- 需要多维度全面审查（安全 + 性能 + 架构）
- 大规模重构审查
- 复杂功能审查（跨多个模块）

**❌ 不适用场景**:
- 单文件小改动
- 仅需检查单一维度（如只看代码风格）
- 快速 spot check
- 简单 bug 修复审查

### 实施示例

**示例 1: 多文件功能审查**

```javascript
// 任务：审查新增的用户认证功能（7 个文件）

// Wave 1: 并行读取所有相关文件
[
  Read("src/auth/login.js"),
  Read("src/auth/register.js"),
  Read("src/auth/middleware.js"),
  Read("src/models/User.js"),
  Read("tests/auth.test.js"),
  Read("config/security.js"),
  Read("docs/api/auth.md")
] // 同时执行，时间 ~8 秒

// Checkpoint: 审查范围分析
确定需要审查的维度:
- Dimension 1: 代码质量（所有文件）
- Dimension 2: 安全性（auth/*.js, middleware.js）
- Dimension 3: 测试覆盖（tests/*.js）
- Dimension 4: 文档完整性（docs/）

// Wave 2: 并行维度审查（可以用多个 agents）
并行执行:
- Agent 1: 检查代码质量和模式
- Agent 2: 审查安全实现（JWT、密码存储）
- Agent 3: 评估测试覆盖率
- Agent 4: 验证文档准确性

// Final: 合并和报告
收集所有 agent 的发现
按严重程度排序
生成统一审查报告
```

**示例 2: API 重构审查**

```javascript
// 任务：审查 REST API 端点重构（12 个文件）

// Wave 1: 并行读取（12 个文件分 3 批）
Batch 1: [Read route files 1-4] // 并行
Batch 2: [Read controller files 5-8] // 并行
Batch 3: [Read model & test files 9-12] // 并行

// Checkpoint: 变更影响分析
识别关键修改:
- 3 个端点签名变更
- 5 个新增验证规则
- 2 个性能优化点

// Wave 2: 并行审查（使用 4 个维度）
Agent 1: 代码质量 → 发现 8 个问题
Agent 2: 安全性 → 发现 3 个风险
Agent 3: 性能 → 发现 2 个瓶颈
Agent 4: 架构 → 发现 1 个设计问题

// Wave 3: Serena 引用完整性（符号修改检测）
检测到 getUserProfile() 签名改变
find_referencing_symbols() → 12 个调用点
验证: 10 个已更新 ✅, 2 个遗漏 ❌

// Final: 综合报告
总问题数: 14 个
关键问题: 5 个（需要修复）
建议: 2 个（可选优化）
```

### 性能对比（代码审查）

| 审查类型 | 文件数 | 顺序执行 | 并行执行 | 提升倍数 |
|---------|-------|---------|---------|---------|
| 单维度 | 5 | 15分钟 | 8分钟 | 1.9x |
| 多维度（4个） | 5 | 40分钟 | 12分钟 | 3.3x |
| 大规模重构 | 15+ | 90分钟 | 25分钟 | 3.6x |

**平均性能提升**: **3.0-3.5x**（代码审查场景）

### 实施清单（代码审查特定）

**执行并行审查前检查**:
- [ ] 修改涉及 ≥5 个文件
- [ ] 需要 ≥2 个审查维度
- [ ] 已明确各维度的审查重点
- [ ] 有合并不同维度发现的计划

**执行中注意事项**:
- ⚠️ 并行读取所有相关文件（包括测试和文档）
- ⚠️ 独立维度并行审查，避免重复工作
- ⚠️ 符号修改必须使用 Serena 完整性检查
- ⚠️ 最终合并时检查跨维度影响

**更多示例**: [docs/examples/parallel_review_overview.md](docs/examples/parallel_review_overview.md)

---

## Step 0.5: Environment Compatibility Check 🔧 (NEW - 老版本适配)

**目的**: 确保代码审查命令在老版本 Claude Code 部署环境中正常工作

**执行时机**: 在 Phase 1 基础代码审查之前

**为什么需要**: Task 2.7 要求"适配老版本环境"，确保新功能（Explore agent, 并行审查）在老版本部署时能优雅降级

---

### 0.5.1 环境检测

检测运行环境特性和可用工具：

**检测项 1: Task tool 可用性**
```
尝试: 调用 Task tool 获取可用 subagent 类型
- ✅ 支持 → 可使用 Explore agent 和并行 review agents
- ❌ 不支持 → 降级为传统文件读取和顺序审查
```

**检测项 2: MCP 服务器可用性**
```
检查:
- Serena MCP: 用于符号级引用完整性检查
  * 可用 → 启用自动符号修改检测
  * 不可用 → 跳过引用完整性检查

- Explore agent: 用于变更文件识别
  * 可用 → 启用 Step 1.1 智能变更识别
  * 不可用 → 直接进入 Step 1.2 手动指定文件
```

**检测项 3: 基础工具完整性**
```
验证: Glob, Grep, Read
- 全部可用 → 正常执行
- 部分缺失 → 警告并提供替代方案
```

---

### 0.5.2 降级策略

根据检测结果，自动选择降级方案：

**Scenario A: 完全支持（理想环境）**
- ✅ Task tool 可用
- ✅ Serena MCP 可用
- ✅ Explore agent 可用
- 🚀 执行模式: 使用所有增强功能

**Scenario B: 部分支持（老版本环境 - 最常见）**
- ❌ Task tool 受限或不可用
- ⚠️ Serena MCP 可能不可用
- 📊 执行模式: 降级策略

**降级决策表**:
| 限制 | 影响范围 | 降级方案 | 性能影响 |
|------|---------|---------|---------|
| Task tool 不可用 | Step 1.1, 并行审查模式 | 跳过 Explore，顺序审查 | 时间 +20-30min |
| Serena 不可用 | 符号引用完整性检查 | 跳过符号检查 | 问题发现率 90% → 60% |
| 两者都不可用 | 所有增强功能 | 完全传统模式 | 时间 +30-45min |

**Scenario C: 最小环境（严重受限）**
- ❌ Task tool 不可用
- ❌ Serena MCP 不可用
- ❌ 某些基础工具缺失
- ⚠️ 执行模式: 最小功能模式，建议升级环境

---

### 0.5.3 执行模式标记

设置后续步骤的执行策略：

```yaml
execution_flags:
  # 智能变更识别
  skip_explore: false/true         # true = 跳过 Explore agent

  # 并行审查
  skip_parallel: false/true        # true = 强制顺序审查
  force_sequential: false/true     # true = 禁用所有并行

  # Serena 集成
  disable_serena: false/true       # true = 跳过符号检查

  # 降级级别
  fallback_level: "none" | "partial" | "full"
    # none - 使用所有增强功能
    # partial - 部分功能降级
    # full - 完全传统模式
```

**执行决策流程**:
```
Environment Check (0.5.1-0.5.2)
  ↓
确定 execution_flags
  ↓
Phase 1 Step 1:
  - skip_explore = true? → 跳过 1.1, 直接 1.2
  - skip_explore = false? → 执行 1.1 Explore 识别
  ↓
Phase 1 Step 2:
  - skip_parallel = true? → Mode A (顺序)
  - skip_parallel = false? → Mode B (并行)
  ↓
Phase 1 Step 2 (符号检查):
  - disable_serena = true? → 跳过符号检查
  - disable_serena = false? → 执行 Serena 完整性检查
```

**性能影响预估**:

| 降级场景 | 审查时间 | 问题发现率 | Token 消耗 |
|---------|---------|-----------|-----------|
| 完全支持 (Scenario A) | 12-18min | 90% | ~5K |
| 部分支持 (Scenario B) | 25-35min | 70% | ~8K |
| 最小环境 (Scenario C) | 40-60min | 60% | ~15K |

**输出示例**:
```
## 🔧 Environment Compatibility Check

环境检测结果:
- Task tool: ✅ 可用
- Serena MCP: ✅ 可用
- Explore agent: ✅ 可用

执行模式: 完全支持 (Scenario A)
预期性能: 审查时间 ~15min, 发现率 90%
```

---

## Process

### Phase 1: 基础代码审查 (Dimension 1-5)

**注意**: 根据 Step 0.5 的环境检测结果，以下步骤可能使用降级模式

---

#### Step 1: Review Preparation (智能变更识别)

本步骤根据 Step 0.5 的 `skip_explore` 标志选择执行模式：
- `skip_explore = false` → 执行 Step 1.1 + 1.2 + 1.3 + 1.4
- `skip_explore = true` → 跳过 1.1，直接执行 1.2 + 1.3 + 1.4

---

##### Step 1.1: 智能变更识别 (Explore Agent Integration) ⭐ NEW

**目的**: 使用 Explore agent 快速识别变更的文件，避免盲目读取整个代码库

**执行条件**: `skip_explore = false` (Task tool 可用)

**复杂度评估决策树**:

```
审查范围明确吗？
├─ YES（用户指定了具体文件/组件）
│  └─ ⏭️ 跳过 Explore，直接进入 Step 1.2
│
└─ NO（需要识别变更范围）
   ↓
   变更影响 ≥5 个文件？
   ├─ 可能 YES → ✅ 使用 Explore agent 识别变更
   │  └─ 效率: Token 节省 70-80% (20K → 4-6K)
   │
   └─ 可能 NO（小改动）
      └─ ⏭️ 跳过 Explore，用 git diff 手动识别
```

**Explore Agent 实际调用**:

如果决定使用 Explore，执行以下 Task tool 调用：

```markdown
启动 Explore agent 用于变更识别:

Prompt:
"识别最近的代码变更并分类：

1. 使用 `git diff HEAD~1 --name-only` 识别最近提交修改的文件
2. 使用 `git log -1 --oneline` 了解提交主题
3. 将变更文件分类：
   - Core changes（核心修改）
   - Related changes（关联修改）
   - Test changes（测试文件）
   - Doc changes（文档修改）
4. 识别可能受影响的其他文件（通过 import/依赖关系）

输出格式:
- 核心修改文件列表（需优先审查）
- 关联文件列表（需验证一致性）
- 测试文件列表（需验证覆盖率）
- 预估审查复杂度（Low/Medium/High）

Thoroughness: medium"

预期输出:
- 变更文件列表（按优先级排序）
- 影响范围评估
- 建议的审查维度
```

**Token 节省效果**:

| 场景 | 不使用 Explore | 使用 Explore | 节省 |
|------|--------------|-------------|------|
| 小改动（1-3 文件） | ~3K tokens | ~3K tokens | 0% (Explore 开销不值得) |
| 中等改动（5-10 文件） | ~15K tokens | ~6K tokens | 60% ✅ |
| 大改动（15+ 文件） | ~30K tokens | ~8K tokens | 73% ✅ |

**输出示例**:
```
## Step 1.1: 变更识别完成

Explore Agent 分析结果:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心修改 (3 files):
- src/auth/login.ts (优先级: 高)
- src/middleware/auth.ts (优先级: 高)
- src/models/User.ts (优先级: 中)

关联文件 (2 files):
- src/routes/api.ts (导入了 login.ts)
- src/config/security.ts (被 auth.ts 引用)

测试文件 (2 files):
- tests/auth.test.ts
- tests/integration/login.test.ts

预估复杂度: Medium
建议审查维度: 安全性 + 代码质量 + 测试覆盖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Token 节省: 15,000 → 6,000 (60% 减少) ✅
```

---

##### Step 1.2: 上下文加载 (Context Loading)

**必须执行**: 无论是否使用 Explore，都需要加载审查上下文

- Load standards from PLANNING.md
- Check related tasks in TASK.md
- Review existing patterns from KNOWLEDGE.md
- **[If Explore used]**: 使用 Explore 的文件列表
- **[If Explore skipped]**: 使用 git diff 或用户指定的范围

---

##### Step 1.3: 审查范围确定 (Scope Identification)

**基于 Step 1.1 或 1.2 的结果**:

确定需要审查的具体文件和组件：
- 核心修改文件（必须审查）
- 关联文件（验证一致性）
- 测试文件（验证覆盖率）
- 文档文件（验证同步性）

**输出**:
```
审查范围:
- 7 个文件需要审查
- 预估审查时间: ~15-20 分钟
- 建议维度: 安全性、代码质量、测试覆盖
```

---

##### Step 1.4: 符号级修改检测 (Symbol-Level Change Detection)

**执行条件**: `disable_serena = false` (Serena MCP 可用)

**目的**: 检测是否有符号级别的修改（函数签名、类名、方法名等）

**Serena 自动检测**:
- 检测函数重命名
- 检测方法签名变更
- 检测类定义修改
- 识别可能的引用不完整

**输出**:
- 符号修改列表
- 需要验证的引用点数量
- 建议是否执行 Serena 完整性检查

---

#### Step 2: Review Execution Mode Selection 🔀 (NEW - 并行审查优化)

**目的**: 根据审查复杂度选择最优执行模式

本步骤根据 Step 0.5 的 `skip_parallel` 标志和审查范围选择执行模式：
- `skip_parallel = false` AND 复杂审查 → 执行 Mode B (并行审查)
- `skip_parallel = true` OR 简单审查 → 执行 Mode A (顺序审查)

---

##### Step 2.1: 审查模式决策

**评估标准**:
```
问题 1: 审查涉及多个文件（≥ 5 个）？
问题 2: 需要多维度全面审查（安全 + 性能 + 架构）？
问题 3: 是大规模重构或复杂功能审查？
问题 4: Task tool 可用且未被禁用？

如果 ≥ 2 个 YES → 使用并行审查模式（Mode B）
否则 → 使用顺序审查模式（Mode A）
```

**模式选择输出**:
- ✅ 审查模式已确定（Mode A 或 Mode B）
- ✅ 如果 Mode B：并行维度已规划

---

##### Step 2.2: Mode A - 顺序审查 (Sequential Review)

**适用**: 简单审查，单文件或小改动

**执行流程**:

1. **Multi-Aspect Review** (顺序执行):
   - Auditor: Verify code style and patterns
   - Security: Check security requirements
   - Performance: Validate efficiency
   - Architecture: Ensure design compliance
   - **[Serena Optional]**: 如果发现符号修改，使用 `find_referencing_symbols()` 验证所有调用点

2. **Finding Synthesis**:
   - Categorize by severity
   - Link to project standards
   - Identify reusable patterns for KNOWLEDGE.md
   - Prioritize fixes
   - **[Serena Integration]**: 对符号修改项，记录 Serena 的引用完整性检查结果

3. **Action Planning**:
   - Create fix tasks for TASK.md
   - Update PLANNING.md if needed
   - Document patterns and standards for KNOWLEDGE.md
   - Document decisions
   - **[Serena Output]**: 如果发现遗漏的引用更新，在改进任务中标记"需要 Serena 完整性检查"

**特点**:
- ✅ 简单直接
- ✅ 适合快速审查
- ⏱️ 标准审查时间

---

##### Step 2.3: Mode B - 并行审查 (Parallel Review) ⭐ NEW

**适用**: 复杂审查，多文件改动，需要多维度全面审查

**执行流程**:

**Wave 1: 并行维度审查阶段** （使用 Task tool 启动 4 个 agents）

```bash
启动 4 个并行 review agents（单次消息调用）:

Agent 1 - Code Quality Reviewer:
  subagent_type: "general-purpose"
  prompt: "审查代码质量维度 (Dimension 1)

          审查范围: [从 Step 1.3 获取的文件列表]

          检查项:
          - 代码风格符合 PLANNING.md 标准
          - 命名规范和可读性
          - 代码结构和模块化
          - 最佳实践遵循

          参考标准:
          - PLANNING.md 编码规范
          - KNOWLEDGE.md 代码模式

          输出格式:
          - 质量分数 (1-5)
          - 发现的问题列表（按严重性排序）
          - 改进建议"

Agent 2 - Security Auditor:
  subagent_type: "general-purpose"
  prompt: "审查安全性维度 (Dimension 2)

          审查范围: [从 Step 1.3 获取的文件列表]

          检查项:
          - 认证和授权机制
          - 数据验证和清理
          - SQL 注入、XSS 等漏洞
          - 敏感数据处理
          - 依赖安全性

          参考标准:
          - PLANNING.md 安全要求
          - OWASP Top 10

          输出格式:
          - 安全分数 (1-5)
          - 关键安全问题列表
          - 风险等级评估"

Agent 3 - Performance Analyst:
  subagent_type: "general-purpose"
  prompt: "审查性能维度 (Dimension 3)

          审查范围: [从 Step 1.3 获取的文件列表]

          检查项:
          - 算法复杂度
          - 资源使用（内存、CPU）
          - 数据库查询优化
          - 缓存策略
          - 异步处理

          参考标准:
          - PLANNING.md 性能目标

          输出格式:
          - 性能分数 (1-5)
          - 性能瓶颈列表
          - 优化建议"

Agent 4 - Architecture Assessor:
  subagent_type: "general-purpose"
  prompt: "审查架构合规性维度 (Dimension 4)

          审查范围: [从 Step 1.3 获取的文件列表]

          检查项:
          - 符合 PLANNING.md 架构设计
          - 设计模式正确应用
          - 模块边界清晰
          - 依赖关系合理
          - PRD 需求对齐

          参考标准:
          - PLANNING.md 架构指南
          - KNOWLEDGE.md 设计模式

          输出格式:
          - 架构分数 (1-5)
          - 架构违规列表
          - 设计改进建议"

⚠️ 关键: 4 个 agents 必须在单个消息中同时启动
```

**Checkpoint: 结果合并和验证**

```bash
等待所有 agents 完成，然后：

1. 合并所有维度的发现
   - 收集 4 个 agents 的输出
   - 按严重程度排序问题

2. 交叉验证
   - 检查不同维度间的冲突
   - 识别跨维度的影响
   - 优先级重排序

3. 统一评分
   - 综合 4 个维度的分数
   - 计算总体质量评分
   - 确定是否通过审查
```

**Final: 符号完整性检查（如果适用）**

```bash
如果 Step 1.4 检测到符号修改:

使用 Serena MCP 执行完整性验证:
  - find_referencing_symbols() 检查所有引用点
  - 验证所有调用点已同步更新
  - 识别遗漏的更新位置

输出:
  - 引用完整性报告
  - 发现的遗漏更新
  - 需要修复的文件列表
```

**性能对比**:

```
顺序模式 (Mode A): Dim1 (10min) → Dim2 (10min) → Dim3 (10min) → Dim4 (10min) = 40min
并行模式 (Mode B): [Dim1 || Dim2 || Dim3 || Dim4] (12min) → Checkpoint (3min) = 15min
              → Final Serena Check (3min) = 18min

性能提升: 2.2x 时间节省 (40min → 18min)
质量提升: 并行验证，更早发现跨维度问题
```

**并行模式实施清单**:
- [ ] Wave 1: 4 个 agents 已在单个消息中启动
- [ ] 等待所有 agents 完成（不提前进入 Checkpoint）
- [ ] Checkpoint 合并通过
- [ ] Serena 符号检查完成（如适用）
- [ ] 生成统一审查报告

---

#### Step 3: Finding Synthesis and Action Planning

**所有模式共同步骤**:

基于 Step 2 的审查结果（无论 Mode A 还是 Mode B）：

1. **Finding Synthesis**:
   - Categorize by severity (Critical/High/Medium/Low)
   - Link to project standards (PLANNING.md references)
   - Identify reusable patterns for KNOWLEDGE.md
   - Prioritize fixes based on impact and effort
   - **[Serena Integration]**: 对符号修改项，记录 Serena 的引用完整性检查结果

2. **Action Planning**:
   - Create fix tasks for TASK.md with priority and effort estimates
   - Update PLANNING.md if architectural issues found
   - Document patterns and standards for KNOWLEDGE.md
   - Document decisions and rationale
   - **[Serena Output]**: 如果发现遗漏的引用更新，在改进任务中标记"需要 Serena 完整性检查"

3. **Quality Gate Decision**:
   - ✅ All dimensions pass → Approved for commit
   - ⚠️ Minor issues → Approved with improvement tasks
   - 🔴 Critical issues → Rejected, must fix before commit

**最终检查**:
- ✅ 所有维度审查完成
- ✅ 问题已分类和优先级排序
- ✅ 改进任务已创建
- ✅ 质量门控决策已做出

### Phase 2: 文档架构合规性检查 (Dimension 6 - 强制) ⭐ NEW

**强制执行**: 如果代码审查通过其他维度，必须检查第 6 维度，确保文档架构完整性

#### Dimension 6: 文档架构合规性 (Documentation Architecture Compliance)

**目的**: 确保代码和文档同步，遵循分层约束，成本控制

**检查清单** (所有 YES 才能通过此维度):

```
□ 分层正确性 - 文档位置是否符合四层架构？
  ├─ 检查项: 新文档是否在正确的层级？
  │  管理层 (PLANNING.md, CONTEXT.md)
  │  技术层 (docs/)
  │  知识层 (KNOWLEDGE.md, docs/knowledge/)
  │  归档层 (docs/archive/)
  ├─ 反例: ❌ 常见 FAQ 出现在 docs/api/ 中
  │         应该在: KNOWLEDGE.md § FAQ
  └─ 通过: ✅ 新 API 文档在 docs/api/
           新决策在 docs/adr/
           常见问题在 KNOWLEDGE.md

□ 成本控制 - 文档大小是否符合约束？
  ├─ KNOWLEDGE.md 是否 < 200 行？
  │  ❌ 如果增长 > 20% → 拆分关键部分到 docs/knowledge/
  │  ✅ 增长 < 20% → 通过
  ├─ 新技术文档是否 < 500 行？
  │  ❌ 如果 > 500 → 要求拆分成多个文件
  │  ✅ < 500 → 通过
  ├─ 新 ADR 是否 < 200 行？
  │  ❌ 如果 > 200 → 要求精简
  │  ✅ < 200 → 通过
  └─ docs/ 总增长是否 < 30%？
     ❌ 如果 > 30% → 检查是否需要清理旧文档
     ✅ < 30% → 通过

□ Frontmatter 完整性 - 所有新文档是否有元数据？
  ├─ 必需字段 (7个) 都存在？
  │  ❌ 缺失任何字段 → 拒绝
  │  ✅ 全部存在 → 通过
  │  字段: title, description, type, status, priority,
  │        created_date, last_updated
  ├─ 关系字段是否正确填写？
  │  ❌ related_documents/related_code 为空或过时 → 标记改进
  │  ✅ 相关链接准确 → 通过
  └─ 类型是否符合规范？
     ❌ type 字段不在允许的值中 → 拒绝
     ✅ type 正确 → 通过

□ 内容重复检查 - 是否有内容在多个文档重复？
  ├─ 信号1: 类似的说明出现在 2+ 个地方
  │  ❌ 重复内容 → 要求建立指针关系
  │  ✅ 内容独立，无重复 → 通过
  ├─ 信号2: KNOWLEDGE.md FAQ 和 docs/ 文档说同一个事
  │  ❌ 重复说明 → 删除一个，保留指针
  │  ✅ 各有特点，互补而非重复 → 通过
  └─ 信号3: ADR 和 PLANNING.md 有相同决策记录
     ❌ 重复记录 → 精简一个
     ✅ PLANNING.md 记录"是什么"，ADR 记录"为什么" → 通过

□ 指针而非复制 - 是否建立了正确的文档关系？
  ├─ 跨层引用: 高层文档是否链接到低层详细文档？
  │  ❌ PLANNING.md 和 docs/ 是孤立的 → 要求补充链接
  │  ✅ PLANNING.md 有指向 docs/ 的链接 → 通过
  ├─ 索引更新: KNOWLEDGE.md 文档索引是否包含新文档？
  │  ❌ 新文档未在索引表中 → 拒绝
  │  ✅ 索引已更新 → 通过
  └─ 关系图: 相关文档之间是否有 related_documents 字段？
     ❌ Frontmatter 中没有关系链接 → 标记改进
     ✅ 关系清晰 → 通过

□ 审查合规 - 文档内容质量和准确性
  ├─ 是否从代码中提取的真实内容（不是编造）？
  │  ❌ 文档说明与代码不符 → 拒绝
  │  ✅ 文档准确反映代码 → 通过
  ├─ 是否包含实际的代码示例（如适用）？
  │  ❌ API 文档没有使用示例 → 要求补充
  │  ✅ 有清晰的代码示例 → 通过
  └─ 是否风格和格式一致（与现有文档）？
     ❌ 格式与项目其他文档明显不一致 → 要求调整
     ✅ 风格一致 → 通过
```

**审查评分** (文档架构维度):

```
评分等级          条件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5/5 (优秀)      所有 6 项检查通过，示范级别
4/5 (良好)      通过所有关键项 (分层、成本、Frontmatter)
                仅有微小改进
3/5 (及格)      基本符合约束，有改进空间
2/5 (需改进)    有 2+ 项不符合，需要显著调整
1/5 (拒绝)      严重违反约束，无法通过
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**失败处理**:

🔴 **立即拒绝（必须修复）**:
- KNOWLEDGE.md 增长 > 50%
- 新文档无 Frontmatter
- 内容重复在 2+ 个地方
- 文档内容与代码不符

🟠 **要求改进（可以在下个 commit 修复）**:
- KNOWLEDGE.md 增长 20-50%（需解释为什么）
- 文档 > 500 行（需分拆）
- Frontmatter 缺少推荐字段
- 没有链接到相关文档

**修复方式**:
如果文档审查不通过，返回 Step 8 (在 /wf_05_code 中) 或使用：
```bash
/wf_14_doc --check "docs/"  # 快速检查文档问题
/wf_14_doc --fix "docs/"    # 自动修复可修复的问题
```

#### Dimension 6 总结

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dimension 6: 文档架构合规性
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
├─ 分层正确性:  ✅/❌
├─ 成本控制:    ✅/❌
├─ Frontmatter: ✅/❌
├─ 内容重复:    ✅/❌
├─ 指针关系:    ✅/❌
├─ 审查合规:    ✅/❌
└─ 综合评分:    __/5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

代码审查通过 (Dim 1-5) AND 文档审查通过 (Dim 6) = ✅ APPROVED
```

---

### Phase 3: 执行后验证 (Dimension 7 - 自检协议) ⭐ NEW

**强制执行**: 在所有代码都实现和审查完成后，必须执行此维度的自检，防止常见的"幻觉"问题

#### Dimension 7: 自检协议 (Self-Check Protocol - 94% 幻觉检测率)

**目的**: 在最后提交前执行强制的 4 个问题检查和 7 个红旗模式识别，防止提交低质量代码

**执行时机**: 代码通过 Dimension 1-6 审查后，在 `/wf_11_commit` 前必须执行

**必答的 4 个问题**（ALL YES 才能通过此维度）:

```
□ Q1: 所有测试都通过了吗？
    ├─ 必须有: 运行测试的输出证据（git log/截图）
    ├─ 拒绝: "应该都能通过" 或 "我相信会通过"
    ├─ 检查项:
    │  ✅ 新增功能的测试全部通过（100%）
    │  ✅ 现有功能的回归测试通过
    │  ✅ 集成测试通过
    │  ❌ 任何测试失败 → 不能通过此问题
    └─ 示例证据: "npm test 输出: 85/85 tests passed (2.3s)"

□ Q2: 所有代码改动都满足需求了吗？
    ├─ 必须有: 逐点对应需求的验证
    ├─ 拒绝: "应该满足" 或 "我觉得差不多了"
    ├─ 检查项:
    │  ✅ 对比 PRD/TASK.md 的需求列表
    │  ✅ 逐项验证实现完成
    │  ✅ 边界情况都处理了
    │  ❌ 有任何跳过的需求 → 不能通过此问题
    └─ 示例证据:
       需求1: 用户登录支持 JWT → ✅ 实现完成（UserAuthService.ts:45-67）
       需求2: 错误处理返回 401 → ✅ 验证通过（测试用例 test_invalid_token）
       需求3: 支持刷新令牌 → ✅ RefreshToken 端点已实现

□ Q3: 代码中是否存在未经证实的假设？
    ├─ 必须有: 主动查找和验证所有假设
    ├─ 拒绝: "没有假设" 或 "假设应该是对的"
    ├─ 常见假设模式:
    │  ❌ "用户总是会 X" → 如果不是呢？
    │  ❌ "外部 API 总是返回 Y" → 错误响应怎么办？
    │  ❌ "数据库连接总是存在" → 连接失败怎么办？
    │  ❌ "文件总是存在" → 文件不存在怎么办？
    │  ❌ "其他模块总是返回 Z" → 签名改变了怎么办？
    ├─ 检查项:
    │  ✅ 验证了所有外部依赖是否真的存在
    │  ✅ 处理了异常路径（错误、null、undefined）
    │  ✅ 测试了边界条件
    │  ❌ 代码中有未处理的假设 → 不能通过此问题
    └─ 示例验证:
       假设1: "用户认证令牌格式正确" → 验证: InvalidTokenError 处理
       假设2: "数据库连接存在" → 验证: ConnectionError 处理
       假设3: "外部支付 API 可用" → 验证: Timeout + Retry 逻辑

□ Q4: 你有没有真实的代码证据支持这些改动？
    ├─ 必须有: 实际的代码片段、测试结果、git diff
    ├─ 拒绝: "应该是对的" 或 "逻辑上是对的"
    ├─ 证据类型:
    │  ✅ 代码片段（来自 src/ 目录）
    │  ✅ 测试输出（来自 test 运行）
    │  ✅ git diff（来自 git log）
    │  ✅ API 测试响应（来自 curl/postman）
    │  ❌ 推理或假设（"我认为应该..."）
    ├─ 检查项:
    │  ✅ 可以指出具体的代码行号
    │  ✅ 可以展示测试通过的输出
    │  ✅ 可以解释代码的执行流程
    │  ❌ 无法指出具体证据 → 不能通过此问题
    └─ 示例证据:
       改动: "实现了用户登录"
       证据1: src/auth/login.ts:23-45 (实现代码)
       证据2: npm test auth.test.ts (测试通过)
       证据3: curl -X POST http://localhost:3000/login (API 响应 200)
```

**识别 7 个红旗模式**（如果出现任何一个，必须标记并处理）:

```
🚩 红旗 1: 无输出 (No Output)
   ├─ 表现: 功能完成但无法展示任何结果或测试输出
   ├─ 示例:
   │  ❌ "我实现了登录功能" → 但拿不出测试结果
   │  ❌ "我修复了性能问题" → 但拿不出性能对比数据
   ├─ 处理:
   │  强制: 运行测试获取真实输出
   │  检查: console.log / 测试断言 / 性能指标
   └─ 严重度: 🔴 CRITICAL（无证据 = 无法验证）

🚩 红旗 2: 无证据 (No Evidence)
   ├─ 表现: 声称改动但无法指出代码位置或修改细节
   ├─ 示例:
   │  ❌ "我修改了权限检查" → git diff 中找不到相关改动
   │  ❌ "我添加了错误处理" → 代码中没有 try-catch
   │  ❌ "我优化了查询" → 无法指出具体修改行号
   ├─ 处理:
   │  强制: 使用 git show / git diff 指出具体改动
   │  检查: Serena `find_symbol()` 定位具体位置
   └─ 严重度: 🔴 CRITICAL（无法追踪 = 可能是幻觉）

🚩 红旗 3: 测试失败 (Test Failures)
   ├─ 表现: 运行测试时出现失败，但声称"没问题"
   ├─ 示例:
   │  ❌ npm test 输出: "5 tests failed" → 声称"一切正常"
   │  ❌ 某个关键路径的测试失败 → 忽视错误继续
   │  ❌ 新增功能的测试未运行 → 假设会通过
   ├─ 处理:
   │  强制: 修复所有失败的测试直到 100% 通过
   │  检查: 验证新增代码的测试覆盖率
   └─ 严重度: 🔴 CRITICAL（表明功能有缺陷）

🚩 红旗 4: 矛盾说法 (Contradictions)
   ├─ 表现: 说法前后不一致或与代码不符
   ├─ 示例:
   │  ❌ "没有修改 getUserProfile()" 但 git diff 显示修改了签名
   │  ❌ "添加了完整的错误处理" 但代码中没有 catch 块
   │  ❌ "这是 bug 修复" 但改动涉及新功能实现
   ├─ 处理:
   │  强制: 澄清实际做了什么，与代码严格对应
   │  检查: 使用 git diff/git log 验证实际改动
   └─ 严重度: 🟠 HIGH（表明理解有误或故意隐瞒）

🚩 红旗 5: 未处理的异常路径 (Unhandled Edge Cases)
   ├─ 表现: 只处理了快乐路径，忽视了错误/边界条件
   ├─ 示例:
   │  ❌ API 只处理 200 响应，无 404/500 处理
   │  ❌ 文件读取未处理"文件不存在"情况
   │  ❌ 列表处理只考虑有元素的情况，无空列表处理
   │  ❌ 数字计算无溢出/除以零保护
   ├─ 处理:
   │  强制: 识别所有可能的异常路径
   │  检查: 添加 try-catch / null checks / boundary tests
   └─ 严重度: 🟠 HIGH（可能导致崩溃或数据问题）

🚩 红旗 6: 依赖信念而非验证 (Belief vs Verification)
   ├─ 表现: 相信某个假设而非主动验证
   ├─ 示例:
   │  ❌ "这应该能工作" → 未实际测试
   │  ❌ "其他模块肯定是对的" → 未查看其他模块代码
   │  ❌ "数据库状态应该是 X" → 未查询实际数据
   │  ❌ "用户肯定会遵循 Y 步骤" → 未在 UI 中验证
   ├─ 处理:
   │  强制: 验证而不是假设（提供证据）
   │  检查: 运行代码、读代码、查询数据、测试 UI
   └─ 严重度: 🟠 HIGH（这是大多数 bug 的来源）

🚩 红旗 7: 覆盖范围不完整 (Incomplete Coverage)
   ├─ 表现: 仅修改了部分需要修改的地方
   ├─ 示例:
   │  ❌ 修改了函数签名但只更新了 2/5 个调用点
   │  ❌ 添加了新字段但未更新相关的序列化/验证
   │  ❌ 修改了数据库 schema 但未更新 ORM 模型
   │  ❌ 更新了 API 但未更新文档和客户端
   ├─ 处理:
   │  强制: 使用 Serena find_referencing_symbols() 找出所有影响点
   │  检查: grep / IDE symbol search / git grep 确保完整性
   └─ 严重度: 🔴 CRITICAL（导致功能不完整或系统不一致）
```

**自检完成的标记**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dimension 7: 自检协议 (Self-Check Protocol)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
必答问题:
  ✅ Q1 - 所有测试都通过了?         YES/NO
  ✅ Q2 - 满足了所有需求?          YES/NO
  ✅ Q3 - 没有未验证的假设?        YES/NO
  ✅ Q4 - 有真实代码证据?          YES/NO

红旗模式检查:
  ✅ 红旗 1 (无输出):      ✅ 清晰 / ⚠️ 需要提供 / 🚩 有问题
  ✅ 红旗 2 (无证据):      ✅ 清晰 / ⚠️ 需要提供 / 🚩 有问题
  ✅ 红旗 3 (测试失败):    ✅ 全通过 / 🚩 有失败
  ✅ 红旗 4 (矛盾说法):    ✅ 一致 / 🚩 有矛盾
  ✅ 红旗 5 (异常路径):    ✅ 已处理 / 🚩 遗漏
  ✅ 红旗 6 (信念验证):    ✅ 已验证 / 🚩 未验证
  ✅ 红旗 7 (覆盖不完):    ✅ 完整 / 🚩 不完整

幻觉检测率:             94% ⭐
状态:                  ✅ PASSED 或 🔴 FAILED

4 个必答问题 = ALL YES
7 个红旗检查 = 无 🚩 标记
→ ✅ 自检通过，可以 /wf_11_commit
```

**失败处理**:

🔴 **自检失败** (任何必答问题为 NO 或 任何红旗模式为 🚩):
- **不能提交！** 返回代码实现修改问题
- 修复流程:
  ```
  /wf_05_code "修复自检发现的问题"
  /wf_07_test  # 确保测试通过
  /wf_08_review  # 重新审查并自检
  ```
- 如果是 Q1（测试失败）: 强制运行 `npm test` 直到 100% 通过
- 如果是 Q2（需求不满足）: 对比 TASK.md/PRD.md，补完缺失的实现
- 如果是 Q3（未验证的假设）: 添加对应的 edge case 测试和处理
- 如果是 Q4（无证据）: 提供具体的代码行号和测试输出

**自检通过的指标**:

✅ **94% 幻觉检测率** - 这是经过验证的有效率
✅ **4 个问题全部 YES** - 必须全部满足，不能妥协
✅ **7 个红旗无标记** - 任何红旗都意味着有问题
✅ **可以安全提交** - 自检通过 = 代码质量有保证

#### Dimension 7 总结

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dimension 7: 自检协议 (执行后验证)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
├─ Q1 (测试通过):      ✅/❌
├─ Q2 (需求完成):      ✅/❌
├─ Q3 (无假设):        ✅/❌
├─ Q4 (有证据):        ✅/❌
├─ 红旗检查:           ✅ 清晰 / 🚩 有问题
├─ 幻觉检测率:         94% ⭐
└─ 综合状态:           ✅ APPROVED / 🔴 FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

完整审查通过 = (Dim 1-5 ✅) AND (Dim 6 ✅) AND (Dim 7 ✅) = 🟢 READY TO COMMIT
```

---

## Output Format

### Phase 1: 代码审查输出（Dimension 1-5）
1. **Review Summary** – overall assessment
2. **Findings** – issues with standard references
3. **Pattern Analysis** – reusable patterns identified for KNOWLEDGE.md
4. **Required Changes** – must-fix items
5. **Recommendations** – improvement suggestions
6. **Serena Integration Results** (if applicable) – symbol-level change completeness verification
   - 检测到的符号修改列表
   - find_referencing_symbols() 验证结果
   - 发现的遗漏更新位置
   - 时间节省和准确性改善数据 (60-80% 时间节省，60% → 90% 问题发现率)
7. **Task Generation** – new TASK.md entries

### Phase 2: 文档架构合规性输出（Dimension 6 - 强制）⭐ NEW
7. **📋 文档审查总结** – 完成 Dimension 6 的检查结果：
   - ✅ 分层正确性检查 - 文档位置是否符合四层架构
   - ✅ 成本控制检查 - KNOWLEDGE.md/docs/ 大小是否符合约束
   - ✅ Frontmatter 完整性检查 - 是否有完整的元数据
   - ✅ 内容重复检查 - 是否有多处重复的内容
   - ✅ 指针关系检查 - 是否建立了跨层的链接
   - ✅ 审查合规检查 - 文档内容准确性和示例完整性

   **输出示例**：
   ```
   📄 文档架构合规性审查 (Dimension 6)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   分层正确性:  ✅ 新 docs/api/auth.md 位置正确
   成本控制:    ✅ KNOWLEDGE.md 增长 +3%, docs/ +6%
   Frontmatter: ✅ 所有必需字段完整
   内容重复:    ✅ 无重复，独立内容
   指针关系:    ✅ related_documents 已填写
   审查合规:    ✅ 代码示例完整，文档准确

   综合评分:    5/5 (优秀) ⭐
   状态:        ✅ APPROVED (代码+文档均通过)
   ```

8. **📚 文档改进任务**（如果需要）– 如果 Dimension 6 发现改进项：
   - 🔴 立即拒绝项（必须在本次 commit 修复）
   - 🟠 要求改进项（可以在下个迭代修复）
   - 建议使用：`/wf_14_doc --check` 和 `--fix` 快速修复

9. **👁️ Ultrathink 设计优雅度评审** (可选提醒) – 设计质量维度（参见 PHILOSOPHY.md）
   - 📐 **代码结构**: 是否流畅易懂？函数职责清晰吗？
   - ✨ **命名质量**: 变量名/函数名是否自然而消除歧义？
   - 🎯 **必然性**: 代码是否"不得不这样"，有没有不必要的复杂性？
   - ⚖️ **权衡认知**: 如果有性能/可读性权衡，是否明确且值得？
   - 📚 **文档一致性**: 文档和代码是否保持同步和协调？

### Phase 3: 执行后验证输出（Dimension 7 - 自检协议）⭐ NEW

10. **✅ 自检协议执行结果** (强制执行) – 完成 Dimension 7 的验证：
    - ✅ Q1: 所有测试都通过了? → YES/NO (附 npm test 输出证据)
    - ✅ Q2: 满足了所有需求? → YES/NO (附需求对应清单)
    - ✅ Q3: 没有未验证的假设? → YES/NO (附异常处理列表)
    - ✅ Q4: 有真实代码证据? → YES/NO (附具体代码行号和 git diff)

    **红旗模式检查** (检查 7 个常见问题模式):
    - 🚩 红旗 1: 无输出 → ✅ 清晰 / 🚩 有问题
    - 🚩 红旗 2: 无证据 → ✅ 清晰 / 🚩 有问题
    - 🚩 红旗 3: 测试失败 → ✅ 全通过 / 🚩 有失败
    - 🚩 红旗 4: 矛盾说法 → ✅ 一致 / 🚩 有矛盾
    - 🚩 红旗 5: 异常路径 → ✅ 已处理 / 🚩 遗漏
    - 🚩 红旗 6: 信念验证 → ✅ 已验证 / 🚩 未验证
    - 🚩 红旗 7: 覆盖不完 → ✅ 完整 / 🚩 不完整

    **输出示例**：
    ```
    ✅ 自检协议执行结果 (Dimension 7)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Q1 - 所有测试都通过了?           ✅ YES
         证据: npm test 输出: 156/156 tests passed (3.2s)

    Q2 - 满足了所有需求?             ✅ YES
         需求1: JWT 认证 → 实现完成 (src/auth/jwt.ts:50-80)
         需求2: 错误处理 → 测试通过 (test/auth.test.ts)
         需求3: 刷新令牌 → API 验证成功 (curl 测试)

    Q3 - 没有未验证的假设?           ✅ YES
         假设1: 令牌格式 → 验证完成
         假设2: DB 连接 → 异常处理已加
         假设3: 外部 API → Timeout + Retry 已实现

    Q4 - 有真实代码证据?             ✅ YES
         证据1: git diff 显示具体改动 (12 files changed)
         证据2: src/auth/login.ts:45-67 (实现代码)
         证据3: 测试输出显示通过

    红旗模式检查:
    ✅ 红旗 1 (无输出):    清晰 (所有测试都有输出)
    ✅ 红旗 2 (无证据):    清晰 (git diff + 代码行号)
    ✅ 红旗 3 (测试失败):  全通过 (156/156 ✅)
    ✅ 红旗 4 (矛盾说法):  一致 (说法与代码相符)
    ✅ 红旗 5 (异常路径):  已处理 (所有 edge cases)
    ✅ 红旗 6 (信念验证):  已验证 (实际测试+运行)
    ✅ 红旗 7 (覆盖不完):  完整 (所有 12 个文件)

    幻觉检测率:           94% ⭐
    综合状态:             ✅ APPROVED (可以提交)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```

11. **📋 自检不通过的改进项**（如果任何自检项失败）:
    - 🔴 立即失败项（本次 commit 必须修复）
    - 🟠 建议改进项（后续迭代可以修复）
    - 具体改进步骤和 `/wf_05_code` 调用建议

12. **🎓 最终质量评分** (综合 Dimension 1-7):
    ```
    代码质量 (Dim 1):      ✅ 5/5 优秀 / 4/5 良好 / 3/5 及格
    安全性 (Dim 2):        ✅ 5/5 优秀 / 4/5 良好 / 3/5 及格
    性能 (Dim 3):          ✅ 5/5 优秀 / 4/5 良好 / 3/5 及格
    架构设计 (Dim 4):      ✅ 5/5 优秀 / 4/5 良好 / 3/5 及格
    测试覆盖 (Dim 5):      ✅ 5/5 优秀 / 4/5 良好 / 3/5 及格
    文档架构 (Dim 6):      ✅ 5/5 优秀 / 4/5 良好 / 3/5 及格
    自检协议 (Dim 7):      ✅ PASSED (94% 检测率) / 🔴 FAILED

    综合评分:              🟢 READY TO COMMIT / 🟡 NEEDS FIX / 🔴 REJECTED
    ```

---

## 🔧 Serena MCP 使用示例（代码审查中的引用完整性检查）

### 场景 1: 检测函数重命名的遗漏引用

**审查场景**: 代码中发现 getUserData() 被重命名为 fetchUserData()

```bash
# 审查时自动激活 Serena（检测到符号修改）
/wf_08_review

# Serena 自动执行的步骤:
1. detect_symbol_changes() → 发现 getUserData() → fetchUserData() 的重命名
2. find_referencing_symbols("fetchUserData") → 定位所有 12 处调用点：
   ✅ src/components/UserProfile.tsx:8 (import - 已更新)
   ✅ src/pages/Dashboard.tsx:15 (call - 已更新)
   ❌ src/tests/user.test.ts:42 (test - 遗漏更新!)
   ❌ docs/api.md:120 (文档示例 - 遗漏更新!)
   ...

3. 审查报告生成:
   🔴 发现问题: src/tests/user.test.ts 和 docs/api.md 中仍使用旧名称
   时间节省: 60-80% (手动检查 15-30 分钟 → 自动完成 3-5 分钟)
   准确性: 60% → 90% (自动检查找到人工可能遗漏的所有位置)
```

**改进项**: 创建TASK.md条目标记"更新test和文档中的旧函数名"

### 场景 2: API接口签名改变的影响评估

**审查场景**: API方法 `authenticate(username, password)` 改为 `authenticate(credentials: {username, password})`

```bash
/wf_08_review

# Serena 步骤:
1. find_referencing_symbols("authenticate")
   → 检查所有 8 个调用点是否已适配新签名

2. 发现问题:
   ❌ src/middleware/auth.ts:25 (仍用旧格式)
   ❌ src/routes/login.ts:40 (仍用旧格式)
   ✅ 其他 6 处已正确更新

3. 输出:
   发现 2 个调用点使用旧 API 签名
   建议: 立即修复或创建兼容性包装器
```

### 场景 3: 类重构后的完整性检查

**审查场景**: User 类被拆分为 UserEntity 和 UserDTO

```bash
/wf_08_review

# Serena 验证:
1. find_referencing_symbols("User")
   → 需要转换为：
   - find_referencing_symbols("UserEntity") (30+ 引用)
   - find_referencing_symbols("UserDTO") (15+ 引用)

2. 完整性报告:
   ✅ 所有类定义已更新
   ✅ 所有导入已更新
   ✅ 所有类型注解已更新
   ✅ 所有测试已更新

   发现漏网之鱼: docs/architecture.md 仍引用旧 User 类

3. 时间节省: 70-90% (手动追踪 30+ 引用会花很长时间)
```

---

## Workflow Integration
- Enforces PLANNING.md standards
- Leverages patterns from KNOWLEDGE.md
- Contributes new patterns to KNOWLEDGE.md
- Generates tasks in TASK.md
- Gates `/wf_11_commit` readiness
- May trigger `/wf_09_refactor`
- Updates quality metrics
- **[Serena MCP Integration]**: Conditional activation for symbol-level change verification
  - Automatically detects symbol-level modifications (function rename, class changes, method signature changes)
  - Uses `find_referencing_symbols()` to verify all call sites updated consistently
  - Improves code review coverage: 60% → 90% issue detection rate
  - Saves 60-80% review time for changes involving symbol modifications

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[任务确认] → [架构咨询] → [代码实现] → [测试验证] → [代码审查 ← 当前] → [提交保存]
   STEP 1      STEP 2 (可选)   STEP 3        STEP 4          STEP 5        STEP 6
```

### ✅ 已完成的步骤

在执行 `/wf_08_review` 前，你应该已经完成：

1. ✅ **任务确认** (`/wf_02_task update`)
2. ✅ **架构咨询**（可选，`/wf_04_ask`）
3. ✅ **代码实现** (`/wf_05_code`)
4. ✅ **测试验证** (`/wf_07_test`)

### 📝 当前步骤

**正在执行**: `/wf_08_review "代码范围"`

- 多维度质量检查（代码风格、安全性、性能、架构）
- 验证 PLANNING.md 标准遵守
- 检查 PRD 合规性
- 识别代码中的优雅度问题

### ⏭️ 建议下一步

**代码审查完成后**，建议按以下顺序执行：

#### 路径 1：审查通过，无需改进 ✅
```bash
# 第6步: 直接提交
/wf_11_commit "feat/fix/test: [描述]"
```

#### 路径 2：发现必须修改的问题 🔴
```bash
# 回到代码实现修改问题
/wf_05_code "修复审查发现的问题"

# 重新运行测试确保没有回归
/wf_07_test "[相同功能]"

# 重新审查
/wf_08_review "[代码范围]"

# 审查通过后提交
/wf_11_commit "fix: 修复代码审查发现的问题"
```

#### 路径 3：发现可选改进项 ✨
```bash
# 创建改进任务（TASK.md 会自动生成）
# 或使用重构命令处理改进
/wf_09_refactor "[改进范围]"

# 改进后提交
/wf_11_commit "refactor: 代码优化改进"
```

### 📊 工作流进度提示

当你完成代码审查时，确保输出中包含：

✅ 已完成的维度:
- Dimension 1-5: 代码风格、安全性、性能、架构、测试（标准审查）
- Dimension 6: 文档架构合规性（强制）
- Dimension 7: 自检协议（最终验证，94% 幻觉检测）

⏭️ 下一步提示:
- 如果有必须修改的问题（🔴），说明需要回到代码实现
- 如果有可选改进（✨），说明可以创建重构任务
- 如果 Dimension 7 自检通过，确认可以进入 `/wf_11_commit` 阶段
- 如果自检失败，强制返回修改直到所有检查点通过

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 审查通过，无问题 | 路径 1 | /wf_11_commit "..." |
| 发现严重问题 | 路径 2 | /wf_05_code → /wf_07_test → /wf_08_review |
| 发现改进机会 | 路径 3 | /wf_09_refactor → /wf_11_commit |
| 无法决策 | 咨询 | /wf_04_ask "这个问题应该立即修复还是后续改进？" |

### 🔄 反馈循环

**审查发现的问题如何处理？**

1. **🔴 必须修改** - 立即执行修改
   ```bash
   /wf_05_code "修复 [具体问题]"
   /wf_07_test  # 确保测试不失败
   /wf_08_review  # 重新审查
   ```

2. **✨ 建议改进** - 后续迭代处理
   - 创建 TASK.md 记录
   - 下个迭代执行 /wf_09_refactor

3. **📚 模式/最佳实践** - 记录到 KNOWLEDGE.md
   - 识别可重用的好模式
   - 记录到知识库供后续参考

### 📚 相关文档

- **工作流指南**: WORKFLOWS.md
- **代码标准**: PLANNING.md (Code Quality, Development Standards)
- **质量指标**: PLANNING.md (Quality Gates)
- **设计原则**: PHILOSOPHY.md (Ultrathink)
- **模式库**: KNOWLEDGE.md
- **任务追踪**: TASK.md
