# 知识库 (Knowledge Base)

**版本**: v1.0
**创建日期**: 2025-11-06
**目的**: 记录项目中的架构决策、设计模式、常见问题解决方案和技术文档索引

---

## 📚 文档索引

**管理层文档** (项目根目录 - prime自动加载):

| 主题 | 文档路径 | 说明 | 优先级 | 最后更新 |
|------|---------|------|--------|---------|
| 项目需求 | [PRD.md](PRD.md) | 产品需求文档（只读参考） | 高 | 待创建 |
| 技术规划 | [PLANNING.md](PLANNING.md) | 架构和开发标准 | 高 | 待创建 |
| 任务追踪 | [TASK.md](TASK.md) | 当前任务和进度 | 高 | 待创建 |
| 会话上下文 | [CONTEXT.md](CONTEXT.md) | 工作进度和状态（自动管理） | 高 | - |
| AI执行规则 | [CLAUDE.md](CLAUDE.md) | 权限矩阵和执行规范 | 中 | 2025-11-06 |
| 设计哲学 | [PHILOSOPHY.md](PHILOSOPHY.md) | Ultrathink 6原则和应用指南 | 中 | 2025-11-06 |
| 文档架构 | [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md) | 四层文档架构和管理策略 | 中 | 待创建 |

**技术层文档** (docs/ - 按需加载):

| 主题 | 文档路径 | 说明 | 优先级 | 最后更新 |
|------|---------|------|--------|---------|
| 架构决策记录 | [docs/adr/](docs/adr/) | ADR 模板和已有决策 | 中 | 2025-11-06 |
| ADR 指南 | [docs/adr/README.md](docs/adr/README.md) | 如何编写和维护 ADR | 中 | 2025-11-06 |
| ADR 模板 | [docs/adr/TEMPLATE.md](docs/adr/TEMPLATE.md) | 新增 ADR 时使用的模板 | 中 | 2025-11-06 |

---

## 🏗️ 架构决策记录 (ADR)

目前还没有正式的 ADR。首个 ADR 应该记录"采用 Ultrathink 设计哲学"这个决策。

**创建 ADR 的触发点**:
- 需要在多个技术选项间权衡时 (选数据库、框架等)
- 架构设计有重大改变时
- 重构或优化涉及权衡时
- 遇到重复的设计问题时

**参考**: `docs/adr/README.md` 中的指南和模板

---

## 📋 设计模式和最佳实践

### 工作流模式

**标准功能开发流程** (来自 CLAUDE.md):
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

**快速 Bug 修复路径**:
```
/wf_06_debug (调试分析)
  ↓
/wf_07_test (验证修复)
  ↓
/wf_11_commit (提交)
```

### 文件权限矩阵 (来自 CLAUDE.md)

| 文件 | 读取 | 创建 | 修改 | 删除 | 特殊规则 |
|------|:----:|:----:|:----:|:----:|---------|
| **PRD.md** | ✅ | ❌ | ❌ | ❌ | 只读参考 |
| **PLANNING.md** | ✅ | ✅ | ✅ | ❌ | 重大决策后更新 |
| **TASK.md** | ✅ | ✅ | ✅ | ❌ | 实时更新状态 |
| **CONTEXT.md** | ✅ | ❌ | ❌ | ❌ | 仅/wf_11_commit写入 |
| **KNOWLEDGE.md** | ✅ | ✅ | ✅ | ❌ | ADR和文档索引中心 |
| **代码文件** | ✅ | ✅ | ✅ | ⚠️ | 删除需确认 |

### 文档管理规则 (来自 CLAUDE.md v3.1+)

**四层文档架构**:
1. **管理层** (根目录) - PRD, PLANNING, TASK, CONTEXT, KNOWLEDGE
2. **技术层** (docs/) - API, 数据库, 部署等详细文档
3. **工作层** (docs/research/) - 临时探索, spike 笔记
4. **归档层** (docs/archive/) - 历史文档

**AI 加载策略**:
- 优先级=高 + 任务相关 → 立即加载
- 优先级=中 + 任务相关 → 询问或按需加载
- 其他情况 → 仅记录存在，不加载

---

## 🎨 Ultrathink 设计哲学 (v3.2 新增)

**核心原则** (详见 PHILOSOPHY.md):
1. **Think Different** - 质疑假设，追求最优
2. **Obsess Over Details** - 观察细节，理解灵魂
3. **Plan Like Da Vinci** - 精心规划，清晰架构
4. **Craft, Don't Code** - 优雅实现，自然抽象
5. **Iterate Relentlessly** - 迭代完善，不断精进
6. **Simplify Ruthlessly** - 无情简化，去除复杂性

**与工作流的对应**:
- `/wf_04_ask` (架构咨询) → Think Different + Plan Like Da Vinci
- `/wf_05_code` (代码实现) → Craft, Don't Code
- `/wf_08_review` (代码审查) → Obsess Over Details
- `/wf_09_refactor` (重构) → Simplify Ruthlessly + Iterate Relentlessly
- `/wf_10_optimize` (优化) → Iterate Relentlessly + 权衡意识

**何时应用**:
- ✅ 架构决策时 (多个选项需权衡)
- ✅ 关键抽象设计时 (影响整个模块)
- ✅ 代码审查时 (检查设计优雅度)
- ✅ 重构/优化时 (明确权衡)
- ❌ 简单 bug 修复时 (直接修即可)
- ❌ 例行小任务时 (代码改动小)

---

## 🐛 常见问题和解决方案

### Q1: 如何判断何时需要 ADR？

**A**: 当面对以下情况时，考虑创建 ADR:
- 多个技术选项需要权衡
- 架构有重大改变
- 重构/优化有复杂的权衡
- 决策影响多个组件或团队

简单的 bug 修复或小功能不需要 ADR。

### Q2: Ultrathink 会不会让开发变慢？

**A**: 短期可能慢，长期能省时间。设计不优雅的系统，后期维护和扩展成本极高。提前投入时间做好设计，后面的日子更轻松。

### Q3: 什么时候应该停止打磨代码？

**A**: 当代码达到"不得不这样"的程度时。追求必然优雅，而不是完美。如果继续改进带不来显著收益，就该发布了。

### Q4: 团队成员对设计理念的理解不同怎么办？

**A**: 这就是为什么要把决策记录到 ADR。写清楚权衡和理由，新成员能学到团队的设计理念。PHILOSOPHY.md 也能帮助统一认识。

---

## 📌 待完成的文档

这些文档在项目初期还不存在，当创建时应该遵循以下规范：

- **PRD.md** - 产品需求文档（仅 AI 读，不修改）
- **PLANNING.md** - 技术规划和开发标准（重大决策后更新）
- **TASK.md** - 任务追踪（实时更新）
- **CONTEXT.md** - 会话上下文（仅 /wf_11_commit 修改）
- **DOC_ARCHITECTURE.md** - 文档架构详细指南

---

## 🔗 相关文档和命令

**工作流命令参考**:
- `/wf_01_planning` - 创建项目规划
- `/wf_02_task` - 管理任务
- `/wf_03_prime` - 加载上下文
- `/wf_04_ask` - 架构咨询（与 Ultrathink 深度结合）
- `/wf_05_code` - 实现功能
- `/wf_06_debug` - 调试修复
- `/wf_07_test` - 测试开发
- `/wf_08_review` - 代码审查（检查优雅度）
- `/wf_09_refactor` - 代码重构
- `/wf_10_optimize` - 性能优化
- `/wf_11_commit` - 提交代码
- `/wf_13_doc_maintain` - 文档维护

**核心文档**:
- [CLAUDE.md](CLAUDE.md) - AI 执行规则和权限矩阵
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计思维指南
- [COMMANDS.md](COMMANDS.md) - 命令完整参考
- [WORKFLOWS.md](WORKFLOWS.md) - 工作流场景指导
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查

---

**最后更新**: 2025-11-06
**维护**: Knowledge Base Management System
**相关**: [CLAUDE.md](CLAUDE.md), [PHILOSOPHY.md](PHILOSOPHY.md), [docs/adr/](docs/adr/)
