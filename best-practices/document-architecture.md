# 文档架构最佳实践

**来源**: [ADR 2025-11-15](../docs/adr/2025-11-15-workflow-document-generation-ssot.md)
**版本**: v1.0
**日期**: 2025-12-29

---

## 📚 四层文档架构

### 层级定义

| 层级 | 位置 | 职责 | 加载策略 | 示例 |
|------|------|------|----------|------|
| **管理层** | 项目根目录 | 项目需求、技术规划、任务追踪 | 会话开始自动加载 | PRD.md, PLANNING.md, TASK.md |
| **技术层** | docs/ | API、架构、部署细节 | 按需加载 | api/auth.md, architecture/system.md |
| **工作层** | docs/research/ | 临时探索和 Spike | 不自动加载 | 2025-11-10-cache-research.md |
| **归档层** | docs/archive/ | 历史文档和废弃内容 | 不加载 | 2024-Q1-old-design.md |

### SSOT 原则 (Single Source of Truth)

**核心思想**: 每个信息只有一个权威来源，通过索引和指针关联。

**CONTEXT.md 指针文档模式**:
- 记录会话的指针和元信息
- 所有内容都是指针，不重复其他文档内容
- 信息量减少 80% (300+ 行 → ~50 行)

**示例**:
```markdown
# CONTEXT.md

## 当前工作焦点
- 活跃任务: TASK.md § 任务1 (Line 36)
- 相关架构: PLANNING.md § 技术栈 (Line 45)
- 相关 ADR: KNOWLEDGE.md § ADR 2025-11-13

## 会话状态
- Git commits: 2 commits (9d99506, 292a57a)
- 修改文件数: 8 files
```

**SSOT 映射**:
| 信息类型 | SSOT 来源 | CONTEXT.md 处理 |
|---------|----------|----------------|
| 任务状态 | TASK.md | 指针：Line X |
| 架构决策 | KNOWLEDGE.md | 指针：ADR YYYY-MM-DD |
| 代码变更 | Git log | 元数据：commits count |

---

## 🎯 约束驱动文档生成

### 三阶段门控

**Phase 1: 代码完成后的文档决策树**
```
Q1: 改动了公开 API/函数/类?
├─ YES → Type C (功能文档) 或 B (ADR)
└─ NO → Q2

Q2: 改变了现有功能的行为?
├─ YES → Type A (架构) 或 D (最佳实践)
└─ NO → Q3

Q3: 使用了新的库/框架/技术?
├─ YES → Type B (ADR)
└─ NO → Q4

Q4: 改变了系统架构或设计?
├─ YES → Type A (更新 PLANNING.md)
└─ NO → Q5

Q5: 引入了新的配置或部署流程?
├─ YES → Type C (部署文档)
└─ NO → Type E (无需文档)
```

**Phase 2: 文档生成时的成本估计和门控**
- 估计每个文档的 token 成本
- 计算对 KNOWLEDGE.md 和 docs/ 的影响
- 判断是否超过约束阈值

**Phase 3: 审查时的架构合规性检查**
- 验证 Frontmatter 完整性
- 重新计算成本影响
- 检查分层正确性
- 验证无重复内容

### 成本约束规范

| 文档类型 | 位置 | 约束 | 说明 |
|---------|------|------|------|
| 类型 A (架构) | PLANNING.md | < 50 行 | 仅"为什么"和"架构影响" |
| 类型 B (决策) | docs/adr/ | < 200 行 | 遵循 ADR 模板 |
| 类型 C (功能) | docs/ | < 500 行 | 复杂 API 分多文件 |
| 类型 D (问题) | KNOWLEDGE.md | < 50 行 | 月末批量审查 |
| 类型 E (无文档) | - | - | 代码优化等 |

**增长率约束** (per commit):
- KNOWLEDGE.md 增长: < 20%
- docs/ 增长: < 30%

**索引约束**:
- KNOWLEDGE.md 总行数: < 200 行（仅索引和摘要）
- 所有新文档: 必须有完整 Frontmatter（7个必需字段）

---

## 📝 Frontmatter 元数据规范

### 标准模板

```yaml
---
# 必需字段（7个）
title: "文档标题"
description: "一句话描述文档的核心内容"
type: "技术设计 | 系统集成 | API参考 | 教程 | 故障排查 | 架构决策"
status: "草稿 | 完成 | 待审查"
priority: "高 | 中 | 低"
created_date: "2025-11-10"
last_updated: "2025-11-10"

# 推荐字段（关系网络）
related_documents: []  # 相关文档
related_code: []       # 实现代码

# 可选字段
tags: []
authors: ["Claude"]
version: "1.0"
---
```

### 字段说明

**必需（7个）**:
- `title`: 文档标题
- `description`: 一句话描述核心内容
- `type`: 文档类型
- `status`: 当前状态
- `priority`: 优先级
- `created_date`: 创建日期
- `last_updated`: 最后更新日期

**推荐（2个）**:
- `related_documents`: 相关文档列表
- `related_code`: 相关代码列表

**使用规则**:
1. 创建: `/wf_14_doc` 自动生成标准 frontmatter
2. 修改: `/wf_11_commit` 自动更新 `last_updated`
3. 发布: `/wf_11_commit` 验证完整性
4. 维护: `/wf_13_doc_maintain` 定期检查一致性

---

## 🔍 文档索引维护

### KNOWLEDGE.md 索引中心

**核心职责**:
- ADR 索引和摘要
- 问题解决方案索引
- 设计模式索引
- **文档索引中心**

### 维护规则

**创建技术文档时**:
1. 在 KNOWLEDGE.md 中添加索引条目
2. 建立任务-文档关联
3. 添加 Frontmatter 元数据

**维护 KNOWLEDGE.md**:
- 新技术文档 → 添加索引条目
- 文档更新 → 更新 last_updated 字段
- 文档废弃 → 移动到 archive/，从索引移除
- 定期运行 `/wf_13_doc_maintain` 检查一致性

### 索引模板

```markdown
## 📚 文档索引

### 技术层文档

| 主题 | 路径 | 说明 | 优先级 | 最后更新 |
|------|------|------|--------|----------|
| 用户认证 | docs/api/authentication.md | JWT实现 | 高 | 2025-11-10 |
| 缓存策略 | docs/architecture/caching.md | Redis设计 | 中 | 2025-11-15 |

### 任务-文档关联

| 任务类型 | 相关文档 |
|---------|----------|
| 实现登录功能 | architecture/system-design.md, api/authentication.md |
| 优化查询性能 | docs/architecture/database.md, docs/research/2025-11-10-index-research.md |
```

---

## 🎯 应用场景

### 场景 1: 创建新的 API 文档

**步骤**:
1. 确定文档类型: Type C (功能文档)
2. 检查约束: < 500 行
3. 生成 Frontmatter (7个必需字段)
4. 添加到 KNOWLEDGE.md 索引
5. 相关代码添加到 `related_code`

### 场景 2: 记录架构决策

**步骤**:
1. 确定文档类型: Type B (ADR)
2. 使用 ADR 模板 (< 200 行)
3. 记录背景、选择、权衡
4. 添加到 KNOWLEDGE.md
5. 更新相关 PLANNING.md

### 场景 3: 更新现有文档

**步骤**:
1. 更新 `last_updated` 字段
2. 更新 KNOWLEDGE.md 索引
3. 检查文档大小是否超限
4. 验证 Frontmatter 完整性

---

## 📊 成功指标

- 管理层文档总大小 < 100KB
- 80% 的任务只需加载 0-2 个技术文档
- 文档索引准确率 > 90%
- 所有技术文档都有完整的 Frontmatter
- KNOWLEDGE.md < 200 行（仅索引）

---

**最后更新**: 2025-12-29
**相关 ADR**: [2025-11-15-workflow-document-generation-ssot.md](../docs/adr/2025-11-15-workflow-document-generation-ssot.md)
