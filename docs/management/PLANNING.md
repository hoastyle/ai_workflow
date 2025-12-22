# 项目规划 (Project Planning)

**项目名称**: AI Workflow Command System
**版本**: v1.2
**创建日期**: 2025-12-05
**最后更新**: 2025-12-22
**状态**: Phase 7 文档管理优化 (Phase 2-3) 进行中

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
| 归档层 | docs/archives/ | 历史存档 | ❌ 不加载 | 归档 |

### 文档行数限制规范 (Phase 2)

**核心原则**: 防止文档过大影响可读性和加载性能

#### 行数限制配置

| 文档 | 行数限制 | 当前状态 | 存档策略 | 理由 |
|------|---------|---------|---------|------|
| **TASK.md** | 200 行 | 222 行 ⚠️ | 按阶段存档 | 持续增长，历史任务价值低 |
| **PLANNING.md** | 300 行 | 236 行 ✅ | 按季度存档 | 架构演进历史有价值 |
| **CONTEXT.md** | 50 行 | 25 行 ✅ | 按周存档 | 指针文档，零冗余 |
| **KNOWLEDGE.md** | 200 行 | 149 行 ✅ | 不存档 | 纯索引，增长缓慢 |
| **PRD.md** | 无限制 | N/A | 不存档 | 需求定义，基本不变 |

#### 存档目录结构

```
docs/
├── management/ (活跃文档 - 行数受限)
│   ├── TASK.md (≤200 行)
│   ├── PLANNING.md (≤300 行)
│   ├── CONTEXT.md (≤50 行)
│   └── PRD.md (无限制)
│
├── archives/ (历史存档 - 无限制)
│   ├── tasks/ (TASK.md 历史)
│   │   ├── index.md (存档索引)
│   │   ├── 2025-q4-phases-1-5.md
│   │   └── 2025-q3-initial-setup.md
│   │
│   ├── planning/ (PLANNING.md 历史架构)
│   │   ├── index.md
│   │   └── 2025-11-architecture-v1.md
│   │
│   └── context/ (CONTEXT.md 历史会话)
│       ├── index.md
│       └── 2025-12-week-*.md
```

#### 存档触发条件

1. **自动触发**: 文档行数超过限制的 80%
2. **手动触发**: 通过 `/wf_13_doc_maintain archive <文档>` 命令
3. **阶段性触发**: 每个 Phase 完成时

#### 存档内容规则

**TASK.md 示例**:
- **保留**: 项目概览、当前阶段、最近 1-2 个阶段
- **存档**: 更早的阶段任务（完整详情）
- **索引**: 在主文档中保留指向存档的链接

**PLANNING.md 示例**:
- **保留**: 当前架构、技术栈、开发标准
- **存档**: 历史架构版本、过时的决策
- **索引**: 在 KNOWLEDGE.md 中维护 ADR 链接

**CONTEXT.md 示例**:
- **保留**: 最近 2 周的会话指针
- **存档**: 更早的会话记录（按周）
- **索引**: 在存档 index.md 中提供快速查找

### 自动化检查和存档机制 (Phase 3)

#### 配置文件

**位置**: `.claude/doc_limits.yaml`

```yaml
document_limits:
  "docs/management/TASK.md": 200
  "docs/management/PLANNING.md": 300
  "docs/management/CONTEXT.md": 50
  "KNOWLEDGE.md": 200

archive_rules:
  TASK.md:
    keep_recent: 2  # 保留最近2个Phase
    archive_path: "docs/archives/tasks"
    archive_by: "phase"  # 按阶段存档

  PLANNING.md:
    keep_recent: 1  # 保留当前版本
    archive_path: "docs/archives/planning"
    archive_by: "quarter"  # 按季度存档

  CONTEXT.md:
    keep_recent_weeks: 2  # 保留最近2周
    archive_path: "docs/archives/context"
    archive_by: "week"  # 按周存档
```

#### 自动检查脚本

**位置**: `scripts/check_doc_size.sh`

**功能**:
1. 读取 `.claude/doc_limits.yaml` 配置
2. 检查每个文档的当前行数
3. 如果超过限制的 80%，发出警告
4. 提供存档建议

**集成点**:
- `/wf_11_commit`: 提交前检查（警告）
- `/wf_02_task update`: 更新任务时检查
- `/wf_13_doc_maintain`: 文档维护专用

#### 存档命令

**手动存档**:
```bash
/wf_13_doc_maintain archive TASK.md
# → 自动将历史Phase移至 docs/archives/tasks/
# → 更新主文档的索引链接
# → 生成或更新 index.md
```

**批量检查**:
```bash
/wf_13_doc_maintain check
# → 检查所有文档大小
# → 显示超限文档列表
# → 提供存档建议
```

#### 实施优先级

**P0 - 立即实施** (本周):
1. TASK.md 存档（当前 222 行，超限）
2. 创建存档目录结构
3. 更新 KNOWLEDGE.md 添加档案索引

**P1 - 近期实施** (下周):
4. 创建 `.claude/doc_limits.yaml` 配置文件
5. 开发 `scripts/check_doc_size.sh` 检查脚本

**P2 - 长期实施** (下下周):
6. 集成到 `/wf_11_commit` 命令
7. 扩展 `/wf_13_doc_maintain` 命令
8. 建立定期审查机制

### 文档生命周期

1. **创建**: `/wf_14_doc` 生成 + Frontmatter
2. **维护**: `/wf_11_commit` 更新时间戳
3. **监控**: 自动检查脚本监控文档大小
4. **存档**: 超限时通过 `/wf_13_doc_maintain` 存档
5. **归档**: 6个月未更新 → archives/

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

| 决策 | ADR 文件 | 状态 |
|------|----------|------|
| 文档行数限制和存档机制 | 2025-12-21 (待创建) | 📝 规划中 |
| 双 CLAUDE 架构反转 | 2025-12-21 (待创建) | 📝 规划中 |
| 约束驱动文档生成 | 2025-11-24 | ✅ 已完成 |
| MCP 集成策略 | 2025-11-21 | ✅ 已完成 |
| 开源优先 | 2025-11-13 | ✅ 已完成 |
| Serena 三层角色 | 2025-11-23 | ✅ 已完成 |

详见 [docs/adr/](../adr/)

---

## 🔗 相关文档

**核心**: [CLAUDE.md](../../CLAUDE.md) | [PHILOSOPHY.md](../../PHILOSOPHY.md) | [KNOWLEDGE.md](../../KNOWLEDGE.md)

**参考**: [COMMANDS.md](../../COMMANDS.md) | [WORKFLOWS.md](../../WORKFLOWS.md) | [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)

**技术**: [docs/guides/](../guides/) | [docs/examples/](../examples/) | [docs/adr/](../adr/)

---
