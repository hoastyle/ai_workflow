---
title: "新增功能和版本历史"
description: "项目新增功能、版本更新和设计决策历史"
type: "新闻"
status: "完成"
priority: "低"
created_date: "2025-11-23"
last_updated: "2025-11-23"
tags:
  - changelog
  - features
  - versions
authors:
  - Claude Code
version: "1.0"
---

## v1.1 新增功能

### `/wf_14_doc` - 智能文档生成助手

**添加日期**: 2025-11-07

**核心理念**: "提取而非编造"
- 从代码库中提取真实信息生成文档
- 交互式选择需要的文档类型
- 支持增量更新，不是全量重写
- 项目特定，不是通用模板

**主要功能**:
1. 代码库分析（技术栈、架构、API）
2. 文档缺口检测（对比代码 vs 现有文档）
3. 智能信息提取（从代码、配置、注释提取）
4. 交互式文档生成
5. 自动更新 KNOWLEDGE.md 索引

**支持的文档类型** (5个核心):
- 📚 项目概览 (README.md)
- 🔌 API 文档 (docs/api/)
- ⚙️ 开发指南 (docs/development/)
- 🚀 部署文档 (docs/deployment/)
- 🏗️ 架构设计 (docs/architecture/)

**使用场景**:
- 项目初始化时生成基础文档
- 功能实现后更新相关文档
- 代码重构后同步架构文档
- CI/CD 检查文档完整性

**工作流位置**:
```
/wf_05_code → /wf_08_review → /wf_14_doc → /wf_13_doc_maintain → /wf_11_commit
```

**设计决策**:
- 为什么不集成现有通用 prompts？
  * 通用模板缺乏项目特定性
  * 不支持增量更新和文档同步
  * "提取"优于"编造"
- 为什么是新命令而非增强现有？
  * 文档生成是独立的关键阶段
  * 保持命令职责单一性
  * 符合工作流模块化原则
