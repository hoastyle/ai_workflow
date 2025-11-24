---
title: "约束驱动的文档生成最佳实践"
description: "确保文档生成过程可控、可验证的约束设计和实施规范"
type: "架构决策"
status: "完成"
priority: "高"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/examples/doc_generation_quick_guide.md"
  - "docs/examples/doc_generation_decision_tree.md"
  - "wf_14_doc.md"
related_code:
  - "scripts/frontmatter_utils.py"
tags: ["文档生成", "约束", "质量"]
---

# 架构决策：约束驱动的文档生成

**决策日期**: 2025-11-24
**状态**: Accepted
**影响范围**: 高（全部文档生成工作流）

## 背景

文档与代码不同步的常见原因：
1. 文档无上界 → 无限膨胀
2. 信息重复 → 维护困难
3. 质量不稳定 → 标准缺失
4. 链接破损 → 用户困惑

## 决策

**采用约束驱动的文档生成范式**：所有文档生成必须通过三阶段门控

### 约束规则

| 约束 | 限制 | 目的 |
|------|------|------|
| KNOWLEDGE.md | < 200 行 | 保持纯索引 |
| 单个文件 | < 500 行 | 易于阅读 |
| 增长率/commit | < 30% | 避免爆炸 |
| Frontmatter | 必需 | 自动化索引 |

### 三阶段门控

**Phase 1** (/wf_05_code Step 8): 代码完成后，使用决策树判断是否需要文档

**Phase 2** (/wf_14_doc): 生成前进行成本估计，确认不超过约束

**Phase 3** (/wf_08_review Dimension 6): 生成后验证约束和索引

## 正当理由

**为什么约束驱动？**
- ✅ 自动化 + 可控（避免完全手动或完全自动的两个极端）
- ✅ 强制简洁（约束迫使只写必要内容）
- ✅ 可验证（三阶段门控确保质量）
- ✅ 零冗余（Frontmatter 建立关系，避免重复）

**为什么这些数字？**
- 200 行 KNOWLEDGE.md：足以容纳 30-50 个索引条目
- 500 行单文件：人类易于阅读的上限
- 30% 增长率：防止单个 commit 爆炸增长

## 实施

**工具**:
- `frontmatter_utils.py` - 生成、验证 Frontmatter，更新索引
- 决策树 - 判断文档需求
- 约束检查 - 验证符合性

**流程**：
1. 代码完成后→识别改动类型→确定文档类型
2. 成本估计→生成前检查约束→用户确认
3. 生成文档→添加 Frontmatter→验证约束
4. 更新 KNOWLEDGE.md→完成

## 权衡

**收益**:
- 成本可控（不超过约束）
- 质量保证（三阶段门控）
- 自动化（Frontmatter、索引）
- 易维护（简洁文档）

**代价**:
- 需学习决策树（一次性 30 分钟）
- 需拆分超限文档（但更优雅）
- 需遵守约束（但合理的约束）

## 成功标准

- ✅ KNOWLEDGE.md 保持 < 200 行
- ✅ 100% 新文档都有完整 Frontmatter
- ✅ > 99% 的文档链接有效
- ✅ 每个 commit 的增长率 < 30%

## 相关资源

- [快速指南](../examples/doc_generation_quick_guide.md)
- [决策树详解](../examples/doc_generation_decision_tree.md)
- [Frontmatter 参考](../examples/frontmatter_quick_reference.md)
- [完整工作流](../wf_14_doc.md)

---

**版本**: v1.0 | **更新**: 2025-11-24
