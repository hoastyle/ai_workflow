---
title: "代码审查 - 并行审查模式"
description: "Step 2.3 并行审查策略：4 维度同时审查，2.2x 性能提升，跨维度问题早发现"
type: "参考"
status: "完成"
priority: "高"
created_date: "2025-12-09"
last_updated: "2025-12-09"
related_documents:
  - "wf_08_review.md"
  - "docs/examples/parallel_review_overview.md"
  - "PLANNING.md"
related_code: []
tags: ["code-review", "parallel-execution", "multi-agent", "performance"]
authors: ["Claude"]
version: "1.0"
---

# 并行审查模式 (Mode B - Parallel Review)

## 概述

**适用场景**: 复杂审查，多文件改动，需要多维度全面审查

**核心策略**: Wave → Checkpoint → Final 模式

**性能优势**: 2.2x 时间节省（40min → 18min）

**质量提升**: 并行验证，更早发现跨维度问题

---

## 执行流程

### Wave 1: 并行维度审查阶段

**关键**: 使用 Task tool 在单个消息中启动 4 个 agents

**审查维度**:
- Dimension 1: Code Quality
- Dimension 2: Security
- Dimension 3: Performance
- Dimension 4: Architecture Compliance

---

## Agent 规格说明

### Agent 1 - Code Quality Reviewer

**维度**: Dimension 1 - 代码质量

**Prompt 规格**:
```
审查代码质量维度 (Dimension 1)

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
- 改进建议
```

**Agent 配置**:
- `subagent_type`: "general-purpose"
- `description`: "审查代码质量维度"

---

### Agent 2 - Security Auditor

**维度**: Dimension 2 - 安全性

**Prompt 规格**:
```
审查安全性维度 (Dimension 2)

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
- 风险等级评估
```

**Agent 配置**:
- `subagent_type`: "general-purpose"
- `description`: "审查安全性维度"

---

### Agent 3 - Performance Analyst

**维度**: Dimension 3 - 性能

**Prompt 规格**:
```
审查性能维度 (Dimension 3)

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
- 优化建议
```

**Agent 配置**:
- `subagent_type`: "general-purpose"
- `description`: "审查性能维度"

---

### Agent 4 - Architecture Assessor

**维度**: Dimension 4 - 架构合规性

**Prompt 规格**:
```
审查架构合规性维度 (Dimension 4)

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
- 设计改进建议
```

**Agent 配置**:
- `subagent_type`: "general-purpose"
- `description`: "审查架构合规性维度"

---

## 并行启动关键要求

⚠️ **关键**: 4 个 agents 必须在单个消息中同时启动

**正确示例**:
```python
# ✅ 正确: 单个消息中启动 4 个 agents
response = send_message([
    Task(subagent_type="general-purpose", prompt="Agent 1: Code Quality..."),
    Task(subagent_type="general-purpose", prompt="Agent 2: Security..."),
    Task(subagent_type="general-purpose", prompt="Agent 3: Performance..."),
    Task(subagent_type="general-purpose", prompt="Agent 4: Architecture...")
])
```

**错误示例**:
```python
# ❌ 错误: 顺序启动
send_message([Task(...)])  # Agent 1
send_message([Task(...)])  # Agent 2
send_message([Task(...)])  # Agent 3
send_message([Task(...)])  # Agent 4
```

---

## Checkpoint: 结果合并和验证

**执行时机**: 等待所有 agents 完成后

**步骤 1: 合并所有维度的发现**
```
收集 4 个 agents 的输出:
- Agent 1 输出: 代码质量问题列表
- Agent 2 输出: 安全问题列表
- Agent 3 输出: 性能瓶颈列表
- Agent 4 输出: 架构违规列表

合并操作:
- 按严重程度排序所有问题
- 生成统一问题清单
```

**步骤 2: 交叉验证**
```
检查不同维度间的冲突:
- 示例冲突: 安全加密 (Dim 2) vs 性能优化 (Dim 3)
- 识别跨维度的影响
- 优先级重排序（安全 > 性能 > 架构 > 代码质量）
```

**步骤 3: 统一评分**
```
综合 4 个维度的分数:
- Dimension 1 (Code Quality): X/5
- Dimension 2 (Security): Y/5
- Dimension 3 (Performance): Z/5
- Dimension 4 (Architecture): W/5

总体质量评分 = (X + Y + Z + W) / 4

通过标准:
- 总分 >= 3.5/5
- 无 Security 或 Architecture 严重问题 (score < 2)
```

---

## Final: 符号完整性检查

**执行条件**: 如果 Step 1.4 检测到符号修改（函数/类签名变更）

**使用 Serena MCP 执行验证**:

```python
# 使用 Serena find_referencing_symbols() 检查所有引用点
referencing_symbols = serena.find_referencing_symbols(
    symbol_name="modified_function_name",
    relative_path="src/module.py"
)

验证内容:
- 所有调用点已同步更新
- 识别遗漏的更新位置
- 检查跨模块影响
```

**输出**:
- 引用完整性报告
- 发现的遗漏更新
- 需要修复的文件列表

**严重度**: 🔴 CRITICAL（符号不完整 = 功能破损）

---

## 性能对比

### 顺序模式 (Mode A)

```
执行流程: 顺序审查
Dimension 1 (10min) →
Dimension 2 (10min) →
Dimension 3 (10min) →
Dimension 4 (10min)
────────────────────
总耗时: 40 分钟
```

### 并行模式 (Mode B)

```
执行流程: 并行审查
Wave 1: [Dim1 || Dim2 || Dim3 || Dim4] → 12min
Checkpoint: 结果合并和交叉验证 → 3min
Final: Serena 符号完整性检查 → 3min
─────────────────────────────────────
总耗时: 18 分钟
```

### 性能提升指标

| 指标 | 顺序模式 | 并行模式 | 提升 |
|------|---------|---------|------|
| **总耗时** | 40 min | 18 min | **2.2x** |
| **并发度** | 1 | 4 | 4x |
| **问题发现** | 顺序发现 | 同时发现 | 更早 |
| **跨维度问题** | 后期发现 | Checkpoint 发现 | 更早 |

---

## 并行模式实施清单

执行前检查:
- [ ] 审查范围明确（文件列表已准备）
- [ ] PLANNING.md 和 KNOWLEDGE.md 已加载
- [ ] Step 1.3 文件列表已获取
- [ ] Step 1.4 符号分析已完成（如适用）

Wave 1 执行:
- [ ] 4 个 agents 已在单个消息中启动
- [ ] 每个 agent 的 prompt 包含完整检查项
- [ ] 每个 agent 的参考标准明确

Checkpoint 执行:
- [ ] 等待所有 agents 完成（不提前进入 Checkpoint）
- [ ] 收集并合并 4 个维度的输出
- [ ] 执行交叉验证，识别冲突
- [ ] 计算统一评分

Final 执行（如适用）:
- [ ] Serena 符号检查完成
- [ ] 引用完整性验证通过
- [ ] 遗漏更新已识别并修复

输出生成:
- [ ] 生成统一审查报告
- [ ] 所有问题按严重性排序
- [ ] 总体质量评分计算完成

---

## 使用示例

### 示例 1: 并行审查通过

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parallel Review Mode (Mode B)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Wave 1: 并行维度审查
  Agent 1 (Code Quality):     ✅ 4.2/5 (3 个小问题)
  Agent 2 (Security):         ✅ 4.5/5 (无严重问题)
  Agent 3 (Performance):      ✅ 3.8/5 (1 个优化建议)
  Agent 4 (Architecture):     ✅ 4.0/5 (符合设计)
  耗时: 12 分钟

Checkpoint: 结果合并
  合并问题数: 4 个（3 小 + 1 中）
  跨维度冲突: 无
  优先级排序: 完成
  耗时: 3 分钟

Final: 符号完整性检查
  符号修改检测: 发现 2 个函数签名变更
  Serena 引用检查: 5/5 调用点已更新
  完整性状态: ✅ 完整
  耗时: 3 分钟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总体评分: 4.1/5 ⭐
总耗时: 18 分钟
状态: ✅ PASSED - 可以进入 Dimension 5-7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 示例 2: 并行审查发现跨维度冲突

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parallel Review Mode (Mode B)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Wave 1: 并行维度审查
  Agent 1 (Code Quality):     ✅ 4.0/5
  Agent 2 (Security):         🟠 3.0/5 (需要加密)
  Agent 3 (Performance):      ✅ 4.5/5 (建议移除加密)
  Agent 4 (Architecture):     ✅ 4.0/5
  耗时: 12 分钟

Checkpoint: 结果合并
  ⚠️ 跨维度冲突检测:
    Dimension 2 (Security): 要求对敏感数据加密
    Dimension 3 (Performance): 建议移除加密以提升性能

  冲突解决:
    优先级: Security (Dim 2) > Performance (Dim 3)
    决策: 保留加密，优化加密算法（使用硬件加速）
    影响: 安全合规 + 可接受的性能损失 (< 10%)

  重新评分:
    Dimension 2: 3.0 → 4.5/5 (采纳加密建议)
    Dimension 3: 4.5 → 4.0/5 (采纳硬件加速优化)

  耗时: 5 分钟（额外 2 分钟用于冲突解决）

Final: 符号完整性检查
  符号修改检测: 无
  跳过 Serena 检查
  耗时: 0 分钟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总体评分: 4.1/5 ⭐
总耗时: 17 分钟
状态: ✅ PASSED - 冲突已解决，可以进入 Dimension 5-7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 何时使用并行模式

### ✅ 推荐使用场景

- 多文件改动（>5 个文件）
- 复杂功能实现（涉及多个模块）
- 架构级别的重构
- 新功能开发（需要全面审查）
- 安全敏感的改动（需要深度检查）

### ⚠️ 不推荐使用场景

- 单文件小改动（<50 行）
- 简单 bug 修复
- 文档更新
- 配置文件修改
- 快速热修复（使用 Mode A - Quick Review）

---

## 故障排查

### 问题 1: Agents 未并行启动

**症状**: 4 个 agents 顺序执行而非并行

**原因**: 未在单个消息中启动所有 agents

**修复**:
```python
# ❌ 错误
for agent in [agent1, agent2, agent3, agent4]:
    send_message([agent])

# ✅ 正确
send_message([agent1, agent2, agent3, agent4])
```

---

### 问题 2: Checkpoint 耗时过长

**症状**: Checkpoint 阶段超过 5 分钟

**原因**: 问题数量过多或跨维度冲突复杂

**建议**:
- 如果问题 > 20 个，考虑先修复明显问题再审查
- 如果冲突 > 3 个，使用 `/wf_04_ask` 进行架构咨询

---

### 问题 3: Serena 符号检查失败

**症状**: Final 阶段 Serena 报告引用不完整

**原因**: 函数/类签名变更但未更新所有调用点

**修复**:
```bash
# 使用 Serena 找出所有引用点
serena.find_referencing_symbols(symbol_name, relative_path)

# 更新所有调用点
/wf_05_code "修复符号引用完整性"

# 重新审查
/wf_08_review
```

---

**创建日期**: 2025-12-09
**版本**: 1.0
**维护者**: AI Workflow Team
