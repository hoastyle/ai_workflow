---
title: "设计模式和最佳实践"
description: "项目中使用的工作流模式、文件权限管理和设计哲学"
type: "设计模式"
status: "完成"
priority: "中"
created_date: "2025-11-23"
last_updated: "2025-11-23"
related_documents:
  - ../../PHILOSOPHY.md
  - ../../CLAUDE.md
tags:
  - workflow
  - patterns
  - design
authors:
  - Claude Code
version: "1.0"
---

## 工作流模式

### 标准功能开发流程
```
/wf_03_prime (加载上下文)
  ↓
[可选] /wf_04_ask (架构咨询)
  ↓
/wf_05_code (实现功能)
  ↓
/wf_07_test (编写测试)
  ↓
/wf_08_review (代码审查)
  ↓
[可选] /wf_09_refactor (重构) 或 /wf_10_optimize (优化)
  ↓
/wf_11_commit (提交)
```

### 快速 Bug 修复路径
```
/wf_06_debug (调试分析)
  ↓
/wf_07_test (验证修复)
  ↓
/wf_11_commit (提交)
```

## 文件权限矩阵

| 文件 | 读取 | 创建 | 修改 | 删除 | 特殊规则 |
|------|:----:|:----:|:----:|:----:|---------|
| **docs/management/PRD.md** | ✅ | ❌ | ❌ | ❌ | 只读参考 |
| **docs/management/PLANNING.md** | ✅ | ✅ | ✅ | ❌ | 重大决策后更新 |
| **docs/management/TASK.md** | ✅ | ✅ | ✅ | ❌ | 实时更新状态 |
| **docs/management/CONTEXT.md** | ✅ | ❌ | ❌ | ❌ | 仅/wf_11_commit写入 |
| **KNOWLEDGE.md** | ✅ | ✅ | ✅ | ❌ | ADR和文档索引中心 |
| **代码文件** | ✅ | ✅ | ✅ | ⚠️ | 删除需确认 |

## 文档管理规则

**四层文档架构**:
1. **管理层** (docs/management/) - PRD, PLANNING, TASK, CONTEXT + (根目录) KNOWLEDGE
2. **技术层** (docs/) - API, 数据库, 部署等详细文档
3. **工作层** (docs/research/) - 临时探索, spike 笔记
4. **归档层** (docs/archive/) - 历史文档

**AI 加载策略**:
- 优先级=高 + 任务相关 → 立即加载
- 优先级=中 + 任务相关 → 询问或按需加载
- 其他情况 → 仅记录存在，不加载

## Ultrathink 设计哲学

**核心原则** (详见 PHILOSOPHY.md):
1. **Think Different** - 质疑假设，追求最优
2. **Obsess Over Details** - 观察细节，理解灵魂
3. **Plan Like Da Vinci** - 精心规划，清晰架构
4. **Craft, Don't Code** - 优雅实现，自然抽象
5. **Iterate Relentlessly** - 迭代完善，不断精进
6. **Simplify Ruthlessly** - 无情简化，去除复杂性

**何时应用**:
- ✅ 架构决策时 (多个选项需权衡)
- ✅ 关键抽象设计时 (影响整个模块)
- ✅ 代码审查时 (检查设计优雅度)
- ✅ 重构/优化时 (明确权衡)
- ❌ 简单 bug 修复时 (直接修即可)
- ❌ 例行小任务时 (代码改动小)
