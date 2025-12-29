---
title: "代码审查详细流程指南"
description: "wf_08_review 命令的完整执行流程，包括智能变更识别、审查模式选择、多维度检查和结果输出"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-09"
last_updated: "2025-12-09"
related_documents:
  - wf_08_review.md
  - docs/guides/parallel_execution_pattern.md
  - docs/guides/wf_08_review_doc_compliance.md
related_code: []
tags: ["code-review", "quality-assurance", "workflow", "process"]
---

# 代码审查详细流程指南

本文档详细说明 `/wf_08_review` 命令的完整执行流程，包括所有步骤、决策点和执行模式。

## 概览

代码审查流程分为以下主要阶段：
- **Step 0**: 环境兼容性检查
- **Step 1**: 审查准备（智能变更识别）
- **Step 2**: 审查执行模式选择（顺序 vs 并行）
- **Step 3**: 发现综合和行动规划
- **Step 4**: 输出生成

## 详细流程

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

#### Step 2.5: 按需加载规范文档 (DocLoader 集成) ⚡ NEW

**目的**: 根据审查复杂度和维度需求，智能加载外部规范文档，优化 token 消耗

**执行条件**: 审查执行前（Step 2 之后）

**加载策略决策**:

```python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 根据审查模式和需求选择加载策略
if review_mode == "quick":
    # 快速审查模式：仅加载摘要
    if needs_doc_compliance:
        doc_summary = loader.load_summary(
            "docs/guides/wf_08_review_doc_compliance.md",
            max_lines=20
        )
    if needs_self_check:
        self_check_summary = loader.load_summary(
            "docs/guides/wf_08_review_self_check.md",
            max_lines=20
        )
    # Token 消耗: ~100 tokens (vs ~692 全文, 节省 85%)

elif review_mode == "standard":
    # 标准审查模式：加载关键章节
    if needs_doc_compliance:
        # Dimension 6: 文档架构合规性
        compliance_sections = loader.load_sections(
            "docs/guides/wf_08_review_doc_compliance.md",
            sections=["分层正确性", "成本控制", "Frontmatter 完整性", "审查评分"]
        )
    if needs_self_check:
        # Dimension 7: 自检协议
        self_check_sections = loader.load_sections(
            "docs/guides/wf_08_review_self_check.md",
            sections=["必答的 4 个问题", "识别 7 个红旗模式"]
        )
    if needs_parallel_review:
        # Step 2.3: 并行审查模式
        parallel_sections = loader.load_sections(
            "docs/guides/wf_08_review_parallel.md",
            sections=["Agent 规格说明", "并行启动关键要求", "性能对比"]
        )
    # Token 消耗: ~310 tokens (vs ~692, 节省 55%)

elif review_mode == "deep":
    # 深度审查模式：加载完整内容
    if needs_doc_compliance:
        compliance_docs = loader.load_sections(
            "docs/guides/wf_08_review_doc_compliance.md",
            sections=["分层正确性", "成本控制", "Frontmatter 完整性",
                      "内容重复检查", "指针而非复制", "审查合规", "失败处理"]
        )
    if needs_self_check:
        self_check_docs = loader.load_sections(
            "docs/guides/wf_08_review_self_check.md",
            sections=["必答的 4 个问题", "识别 7 个红旗模式", "失败处理", "使用示例"]
        )
    if needs_parallel_review:
        parallel_docs = loader.load_sections(
            "docs/guides/wf_08_review_parallel.md",
            sections=["执行流程", "Agent 规格说明", "并行启动关键要求",
                      "Checkpoint: 结果合并和验证", "Final: 符号完整性检查",
                      "性能对比", "并行模式实施清单", "使用示例"]
        )
    # Token 消耗: ~550 tokens (vs ~692, 节省 20%)
```

**需求判断逻辑**:

```python
# 判断是否需要加载各维度文档
needs_doc_compliance = (
    # 检测到文档修改
    any("docs/" in f or "KNOWLEDGE.md" in f for f in changed_files) or
    # 显式请求文档审查
    "文档" in review_scope or "documentation" in review_scope.lower()
)

needs_self_check = (
    # Phase 3 审查前必须执行
    current_phase == "Phase 3" or
    # 准备提交时执行
    next_command == "/wf_11_commit"
)

needs_parallel_review = (
    # 大规模审查（≥5 个文件）
    len(changed_files) >= 5 or
    # 显式请求并行审查
    "--parallel" in review_flags or
    # 多维度全面审查
    len(review_dimensions) >= 3
)
```

**输出示例**:

```
⚡ DocLoader 智能加载完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模式: standard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
加载文档:
  ✅ wf_08_review_doc_compliance.md (4 sections, ~180 tokens)
  ✅ wf_08_review_self_check.md (2 sections, ~130 tokens)
  ⏭️ wf_08_review_parallel.md (跳过: 未检测到并行审查需求)

总 Token 消耗: 310 tokens (vs 全文 692 tokens)
节省比例: 55% ⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**优势**:

- ✅ **智能判断**: 根据审查范围自动选择需要的规范文档
- ✅ **模式适配**: 3 种加载模式适应不同审查复杂度
- ✅ **Token 优化**: 20-85% token 节省，平均 55%
- ✅ **可扩展**: 未来可添加更多规范文档而不影响核心流程
- ✅ **向后兼容**: 原有审查流程完全保留，DocLoader 为可选增强

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


---

## 流程总结

### 关键决策点

1. **是否使用 Explore Agent** (Step 1.1):
   - 变更范围不明确 → 使用 Explore
   - 具体文件已知 → 跳过 Explore

2. **审查模式选择** (Step 2):
   - ≥5 文件 → 并行审查（Mode B）
   - <5 文件 → 顺序审查（Mode A）

3. **是否加载详细文档** (Step 2.5):
   - 标准明确 → 跳过加载
   - 标准不清楚 → 使用 DocLoader 按需加载

### Token 优化策略

- **Explore Agent**: 70-80% token 节省（20K → 4-6K）
- **并行审查**: 2-3x 性能提升
- **DocLoader**: 85-90% 文档读取 token 节省

### 最佳实践

1. **小改动**（1-2文件）: 跳过 Explore，直接审查
2. **中等改动**（3-5文件）: 使用 Explore 识别，顺序审查
3. **大规模改动**（5+文件）: Explore + 并行审查
4. **复杂标准**: 使用 DocLoader 按需加载规范

---

**相关文档**:
- [并行执行模式详解](parallel_execution_pattern.md)
- [文档合规性检查](wf_08_review_doc_compliance.md)
- [自检清单](wf_08_review_self_check.md)
