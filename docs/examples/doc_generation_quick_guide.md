---
title: "文档生成快速指南（约束驱动）"
description: "5 分钟快速理解和执行约束驱动的文档生成工作流"
type: "教程"
status: "完成"
priority: "高"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/examples/doc_generation_decision_tree.md"
  - "docs/examples/frontmatter_quick_reference.md"
  - "wf_14_doc.md"
related_code:
  - "scripts/frontmatter_utils.py"
tags: ["文档生成", "工作流", "快速开始"]
---

# 文档生成快速指南

## 一句话说明

**约束驱动文档生成**: 代码完成后 → 决策是否需要文档 → 成本估计 → 生成 → 验证约束

## 三阶段快速流程

### Phase 1：代码完成后（/wf_05_code Step 8）

改动了什么？→ 决定是否需要文档：

```
改动类型          → 文档类型 → 位置               → 约束
─────────────────────────────────────────────────────
公开 API         → Type C   → docs/api/          → <500行
现有行为改变      → Type A/D → PLANNING/FAQ       → <50行
新技术/库         → Type B   → docs/adr/          → <200行
系统架构改变      → Type A   → PLANNING.md        → <50行
新配置/环境变量   → Type C   → docs/deployment/  → <500行
代码优化         → Type E   → 无                 → -
```

**关键问题**: 下一个维护者需要了解"为什么"和"如何用"吗？ → YES → 需要文档 | NO → 不需要

### Phase 2：生成文档（/wf_14_doc）

运行命令：
```bash
/wf_14_doc
```

工作流：
1. **成本估计** - 自动检查是否超过约束
2. **用户确认** - 展示预估成本，让用户选择
3. **生成文档** - 自动提取信息并生成
4. **添加 Frontmatter** - 自动填充文档元数据

### Phase 3：验证约束（/wf_08_review Dimension 6）

检查清单：
```
✅ Frontmatter 完整（7个必需字段）
✅ 文档大小 < 约束
✅ related_documents 路径有效
✅ 索引已更新
✅ 所有约束符合
```

## 约束规则（必须遵守）

| 约束 | 限制 | 目的 |
|------|------|------|
| KNOWLEDGE.md | < 200 行 | 保持纯索引 |
| 单个文件 | < 500 行 | 易于阅读和维护 |
| 每 commit 增长率 | < 30% | 避免爆炸增长 |
| Frontmatter | 必需 | 自动化索引和追踪 |

**超限解决**: 拆分文件 → 删除非核心内容 → 清理旧文档

## Frontmatter 必需字段

```yaml
---
title: "文档标题"
description: "一句话描述核心内容"
type: "技术设计|系统集成|API参考|教程|故障排查|架构决策"
status: "草稿|完成|待审查"
priority: "高|中|低"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/xxx.md"        # 最多 3-5 个
related_code:
  - "src/xxx/"
---
```

## 常见约束冲突解决

**问题**: 文档会超过 500 行
**解决**:
1. 拆分为 2-3 个小文件（推荐）
2. 删除非核心部分
3. 分多个 commit 生成

**示例**: 大 API 文档拆分
```
endpoints.md (~250行)        ← 列出所有端点
authentication.md (~200行)   ← 认证机制
error_codes.md (~150行)      ← 错误处理
```

## 快速命令参考

```bash
# 交互式生成（推荐）
/wf_14_doc

# 只检查不生成
/wf_14_doc --check

# 自动模式（无交互）
/wf_14_doc --auto

# 验证 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/xxx.md

# 批量验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 更新索引
python ~/.claude/commands/scripts/frontmatter_utils.py update-index KNOWLEDGE.md
```

## 实战例子

**场景**: 添加新 API 端点

```
Step 1: 代码完成后识别改动
  问: 改动了公开 API？答: YES
  决定: Type C（API 文档）

Step 2: 成本估计
  当前 docs/ 规模: 12,484 行
  新增文档: ~150 行（50 行端点 + 50 行参数 + 50 行示例）
  增长率: 150/12,484 = 1.2% ✅ 符合 < 30% 约束

Step 3: 生成
  /wf_14_doc
  → 自动提取路由定义
  → 生成 docs/api/new_endpoint.md
  → 添加 Frontmatter
  → 更新 KNOWLEDGE.md 索引

Step 4: 验证
  验证 Frontmatter ✅
  检查约束符合 ✅
  索引更新 ✅
  完成！
```

## 何时不需要文档（Type E）

- 代码优化（内部改进，无用户影响）
- 变量改名（符合现有模式）
- 性能调优（内部实现细节）
- 代码风格改进

## 团队最佳实践

1. **每个 commit 都检查**: 是否需要同步文档？
2. **及早生成**: 代码完成立即生成，不要延迟
3. **遵守约束**: 宁可拆分也不要超限
4. **定期审查**: 每月检查文档的 last_updated 字段

## 快速链接

- 详细工作流 → [docs/examples/doc_generation_decision_tree.md](doc_generation_decision_tree.md)
- Frontmatter 规范 → [docs/reference/FRONTMATTER.md](../../reference/FRONTMATTER.md)
- 完整命令参考 → [wf_14_doc.md](../../wf_14_doc.md)
- 约束设计原理 → [docs/adr/](../../adr/)

---

**记住**: 约束是为了让文档保持简洁、易维护、自动化索引！

**版本**: v1.0 | **更新**: 2025-11-24
