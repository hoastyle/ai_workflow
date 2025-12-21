# 项目规划 (Project Planning)

**项目名称**: AI Workflow Command System
**版本**: v1.1
**创建日期**: 2025-12-05
**最后更新**: 2025-12-21
**状态**: Phase 7 双 CLAUDE 架构实现进行中

---

## 📋 项目概览

**目标**: 为 Claude Code 提供高频使用场景优化的闭环工作流系统

**核心价值**:
1. **会话连续性** - 通过 CONTEXT.md 跨越 `/clear` 边界
2. **自动化追踪** - 全程自动更新进度
3. **质量保证** - 内置格式化、测试、审查
4. **文档驱动** - PRD → PLANNING → TASK 完整追溯链
5. **智能文档管理** - 四层架构 + 按需加载

**成功标准**:
- ✅ 14 个工作流命令完整
- ✅ 管理层文档完整（5/5）
- ✅ Token 消耗优化 60-80%
- ✅ 文档约束合规 100%

---

## 🏗️ 系统架构

### 核心组件

```
AI Workflow Command System
├── 14 个命令 (wf_01 - wf_14 + wf_99)
├── 管理层: PRD, PLANNING, TASK, CONTEXT, KNOWLEDGE
├── 技术层: guides, examples, adr, reference, integration
├── 工具层: Python 脚本和 Makefile
└── 集成层: 6 个 MCP 服务器（可选）
```

### 技术栈

| 组件 | 技术 |
|------|------|
| 命令定义 | Markdown + Frontmatter |
| 自动化 | Python 3.8+, Bash 4.0+ |
| 质量控制 | pre-commit, black, markdownlint |
| 版本控制 | Git + hooks |
| MCP 集成 | Serena, Context7, Sequential-thinking, Tavily, Magic |

---

## 🔄 开发工作流

### 标准开发流程

```bash
/wf_03_prime              # 会话开始
/wf_05_code "功能"        # 代码实现
/wf_07_test "组件"        # 添加测试
/wf_08_review             # 代码审查
/wf_11_commit "消息"      # 提交
```

### 提交消息格式

```
[type] subject

body (optional)
```

**类型**: feat, fix, docs, refactor, test, chore

### Git 工作流

- 功能分支: `feature/xxx`
- 提交前运行: `pre-commit run`
- 使用 `/wf_08_review` 审查代码

---

## 📐 代码标准

### 命名约定

- 命令文件: `wf_<编号>_<名称>.md`
- 指南文档: `<主题>_guide.md`
- ADR 文档: `YYYY-MM-DD-<标题>.md`
- 函数: `snake_case`, 类: `PascalCase`

### 文档要求

**Frontmatter 必需** (7 字段):
```yaml
---
title: "标题"
description: "一句话"
type: "技术设计 | API参考 | 教程 | 故障排查 | 架构决策"
status: "草稿 | 完成 | 待审查"
priority: "高 | 中 | 低"
created_date: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---
```

**约束**:
- KNOWLEDGE.md < 200 行
- 单个文档 < 500 行
- 每 commit 增长 < 30%

### 代码风格

- Markdown: 最多 3 级标题，2 空格缩进
- Python: black 格式化，88 字符行长
- Bash: `set -euo pipefail`, 错误处理完整

### 代码审查清单

- [ ] 符合命名约定
- [ ] 文档有完整 Frontmatter
- [ ] 符合文档大小约束
- [ ] 通过 pre-commit 检查
- [ ] 测试覆盖关键路径
- [ ] 提交消息清晰

---

## 🧪 测试策略

### 测试方法

**命令测试**: 手动验证每个 `/wf_*` 命令
**文档验证**: Frontmatter 完整性 + 链接有效性
**集成测试**: 完整工作流验证

### 测试覆盖目标

- 命令覆盖: 100% (14/14)
- Frontmatter 完整性: 100%
- Pre-commit 通过率: 100%
- 管理层文档: 100% (5/5)

---

## 📚 文档架构

### 四层文档结构

| 层级 | 位置 | 职责 | 加载策略 | 约束 |
|------|------|------|---------|------|
| 管理层 | 根目录 + docs/management/ | PRD, PLANNING, TASK, CONTEXT, KNOWLEDGE | ✅ prime 自动 | <100KB |
| 技术层 | docs/ | guides, examples, adr, reference, integration | 🔍 按需 | <500 行 |
| 工作层 | docs/research/ | 临时探索 | ❌ 不加载 | 清理 |
| 归档层 | docs/archive/ | 历史 | ❌ 不加载 | 归档 |

### 文档生命周期

1. **创建**: `/wf_14_doc` 生成 + Frontmatter
2. **维护**: `/wf_11_commit` 更新时间戳
3. **整理**: 定期 `/wf_13_doc_maintain`
4. **归档**: 6个月未更新 → archive/

---

## 📐 性能目标

| 操作 | 目标 | 当前 |
|------|------|------|
| `/wf_03_prime` | <2s | ~1s ✅ |
| `/wf_05_code` | <60s | ~55s ✅ |
| `/wf_08_review` | <30s | ~18s ✅ |
| `/wf_11_commit` | <10s | ~5s ✅ |

**Token 优化**:
- 会话启动: 10K → 2.5K (75% 节省)
- 代码实现: 30K → 6K (80% 节省)
- 代码审查: 20K → 6K (70% 节省)

**资源约束**:
- 管理层: <100KB
- KNOWLEDGE.md: <200 行
- 单个文档: <500 行

---

## 🔐 安全指南

### 文件权限

| 文件 | 权限 | 说明 |
|------|------|------|
| PRD.md | 只读 | ❌ 绝不修改 |
| PLANNING.md | 读写 | ✅ 重大决策更新 |
| TASK.md | 读写 | ✅ 实时状态更新 |
| CONTEXT.md | 只读 | 🤖 仅 /wf_11_commit |
| KNOWLEDGE.md | 读写 | ✅ 新 ADR 时添加 |

### 最佳实践

- 所有更改通过 `/wf_08_review` 审查
- 不存储密钥或凭证
- 最小化第三方依赖
- MCP 服务器可选且可降级

---

## 🎯 技术决策 (ADR)

| 决策 | ADR 文件 |
|------|----------|
| 双 CLAUDE 架构反转 | 2025-12-21 (待创建) |
| 约束驱动文档生成 | 2025-11-24 |
| MCP 集成策略 | 2025-11-21 |
| 开源优先 | 2025-11-13 |
| Serena 三层角色 | 2025-11-23 |

详见 [docs/adr/](../adr/)

---

## 🔗 相关文档

**核心**: [CLAUDE.md](../../CLAUDE.md) | [PHILOSOPHY.md](../../PHILOSOPHY.md) | [KNOWLEDGE.md](../../KNOWLEDGE.md)

**参考**: [COMMANDS.md](../../COMMANDS.md) | [WORKFLOWS.md](../../WORKFLOWS.md) | [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)

**技术**: [docs/guides/](../guides/) | [docs/examples/](../examples/) | [docs/adr/](../adr/)

---

**维护者**: AI Workflow System
**版本**: v1.1
**最后更新**: 2025-12-21
