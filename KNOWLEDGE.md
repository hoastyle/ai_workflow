# 知识库 (Knowledge Base)

**版本**: v1.2
**创建日期**: 2025-11-06
**最后更新**: 2025-11-23
**目的**: 项目架构决策、设计模式和技术文档的索引中心

> ℹ️ **注意**: 本文件为纯索引和指针，详细内容已分离到 `docs/knowledge/` 目录以减少维护成本和上下文消耗。

---

## 📚 文档索引

### 管理层文档 (prime自动加载)

| 主题 | 路径 | 优先级 |
|------|------|--------|
| 项目需求 | [docs/management/PRD.md](docs/management/PRD.md) | 高 |
| 技术规划 | [docs/management/PLANNING.md](docs/management/PLANNING.md) | 高 |
| 任务追踪 | [docs/management/TASK.md](docs/management/TASK.md) | 高 |
| 会话上下文 | [docs/management/CONTEXT.md](docs/management/CONTEXT.md) | 高 |
| AI执行规则 | [CLAUDE.md](CLAUDE.md) | 中 |
| 设计哲学 | [PHILOSOPHY.md](PHILOSOPHY.md) | 中 |

### 技术层文档 (按需加载)

| 主题 | 路径 | 优先级 |
|------|------|--------|
| 架构决策记录 | [docs/adr/](docs/adr/) | 中 |
| Frontmatter 规范 | [docs/reference/FRONTMATTER.md](docs/reference/FRONTMATTER.md) | 高 |
| MCP 集成 | [docs/integration/](docs/integration/) | 高 |

### 知识库详细文档 (docs/knowledge/)

- 📋 [设计模式](docs/knowledge/DESIGN_PATTERNS.md) - 工作流、权限、架构
- 📝 [文档最佳实践](docs/knowledge/DOCUMENTATION_PRACTICES.md) - 约束、流程
- 🐛 [常见问题](docs/knowledge/FAQ.md) - 系统、设计、架构问题
- 🆕 [版本历史](docs/knowledge/CHANGELOG.md) - 新增功能、设计决策

---

## 🏗️ 架构决策记录 (ADR)

**已有决策** (9个):

| 日期 | 标题 | 影响 | 状态 |
|------|------|------|------|
| 2025-11-23 | Serena 三层角色模型 | 高 | Accepted |
| 2025-11-21 | MCP 集成策略 | 全局 | Accepted |
| 2025-11-18 | 约束驱动的文档生成 | 高 | Accepted |
| 2025-11-15 | Workflow 文档生成 SSOT | 高 | Accepted |
| 2025-11-15 | CONTEXT.md 指针文档 | 高 | Accepted |
| 2025-11-13 | 架构咨询优先开源方案 | 高 | Accepted |
| 2025-11-11 | 使用项目工具而非重新实现 | 高 | Accepted |
| 2025-11-07 | 智能文档生成 | 高 | Accepted |

详见: [docs/adr/](docs/adr/)

**触发条件**:
- 多个技术选项间的权衡
- 架构有重大改变
- 复杂的重构/优化权衡
- 决策影响多个组件

---

## 🔗 工作流和核心参考

**工作流命令**: `/wf_01_planning` → `/wf_02_task` → `/wf_03_prime` → `/wf_05_code` → `/wf_08_review` → `/wf_11_commit`

**核心参考**:
- [CLAUDE.md](CLAUDE.md) - AI 执行规则
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计思维
- [docs/adr/README.md](docs/adr/README.md) - ADR 指南

---

**最后更新**: 2025-11-23
**维护者**: Knowledge Base Management System
**版本**: v1.2
