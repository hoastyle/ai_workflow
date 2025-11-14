# 知识库 (Knowledge Base)

**版本**: v1.0
**创建日期**: 2025-11-06
**目的**: 记录项目中的架构决策、设计模式、常见问题解决方案和技术文档索引

---

## 📚 文档索引

**管理层文档** (项目根目录 - prime自动加载):

| 主题 | 文档路径 | 说明 | 优先级 | 最后更新 |
|------|---------|------|--------|---------|
| 项目需求 | [docs/management/PRD.md](docs/management/PRD.md) | 产品需求文档（只读参考） | 高 | 待创建 |
| 技术规划 | [docs/management/PLANNING.md](docs/management/PLANNING.md) | 架构和开发标准 | 高 | 待创建 |
| 任务追踪 | [docs/management/TASK.md](docs/management/TASK.md) | 当前任务和进度 | 高 | 2025-11-11 |
| 会话上下文 | [docs/management/CONTEXT.md](docs/management/CONTEXT.md) | 工作进度和状态（自动管理） | 高 | - |
| AI执行规则 | [CLAUDE.md](CLAUDE.md) | 权限矩阵和执行规范 | 中 | 2025-11-11 |
| 设计哲学 | [PHILOSOPHY.md](PHILOSOPHY.md) | Ultrathink 6原则和应用指南 | 中 | 2025-11-06 |
| 文档架构 | [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md) | 四层文档架构和管理策略 | 中 | 待创建 |

**技术层文档** (docs/ - 按需加载):

| 主题 | 文档路径 | 说明 | 优先级 | 最后更新 |
|------|---------|------|--------|---------|
| 架构决策记录 | [docs/adr/](docs/adr/) | ADR 模板和已有决策 | 中 | 2025-11-06 |
| ADR 指南 | [docs/adr/README.md](docs/adr/README.md) | 如何编写和维护 ADR | 中 | 2025-11-06 |
| ADR 模板 | [docs/adr/TEMPLATE.md](docs/adr/TEMPLATE.md) | 新增 ADR 时使用的模板 | 中 | 2025-11-06 |
| Frontmatter 规范 | [docs/reference/FRONTMATTER.md](docs/reference/FRONTMATTER.md) | 文档元数据标准和验证规则 | 高 | 2025-11-11 |

**自动化脚本** (scripts/ - 工具集):

| 脚本 | 功能 | 主要用途 | 最后更新 |
|------|------|---------|---------|
| frontmatter_utils.py | Frontmatter 处理核心工具 | 验证、生成、关系图构建 | 2025-11-11 |
| doc_graph_builder.py | 文档关系图生成器 | 可视化文档关系网络 | 2025-11-11 |

---

## 🏗️ 架构决策记录 (ADR)

**已有决策**:

| 决策日期 | 标题 | 影响 | 状态 | 文档路径 |
|---------|------|------|------|---------|
| 2025-11-15 | Workflow 文档生成 SSOT 架构：消除系统性冗余 | 高 | Accepted | [docs/adr/2025-11-15-workflow-document-generation-ssot.md](docs/adr/2025-11-15-workflow-document-generation-ssot.md) |
| 2025-11-15 | CONTEXT.md 指针文档模式：消除 85% 冗余 | 高 | Accepted | [docs/adr/2025-11-15-context-md-pointer-document.md](docs/adr/2025-11-15-context-md-pointer-document.md) |
| 2025-11-13 | 在架构咨询工作流中优先考虑开源方案 | 高 | Accepted | [docs/adr/2025-11-13-prioritize-opensource-in-architecture.md](docs/adr/2025-11-13-prioritize-opensource-in-architecture.md) |
| 2025-11-11 | 命令文档必须明确指示使用项目工具 | 高 | Accepted | [docs/adr/2025-11-11-use-existing-tools-over-reimplementation.md](docs/adr/2025-11-11-use-existing-tools-over-reimplementation.md) |
| 2025-11-11 | 采用独立脚本而非嵌入文档 | 高 | Accepted | (见 TASK.md § 架构决策) |
| 2025-11-07 | 智能文档生成（提取而非编造） | 高 | Accepted | [docs/adr/2025-11-07-intelligent-doc-generation-over-template-based.md](docs/adr/2025-11-07-intelligent-doc-generation-over-template-based.md) |

**创建 ADR 的触发点**:
- 需要在多个技术选项间权衡时 (选数据库、框架等)
- 架构设计有重大改变时
- 重构或优化涉及权衡时
- 遇到重复的设计问题时
- AI 执行行为与预期不符时（如本次工具集成问题）

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
| **docs/management/PRD.md** | ✅ | ❌ | ❌ | ❌ | 只读参考 |
| **docs/management/PLANNING.md** | ✅ | ✅ | ✅ | ❌ | 重大决策后更新 |
| **docs/management/TASK.md** | ✅ | ✅ | ✅ | ❌ | 实时更新状态 |
| **docs/management/CONTEXT.md** | ✅ | ❌ | ❌ | ❌ | 仅/wf_11_commit写入 |
| **KNOWLEDGE.md** | ✅ | ✅ | ✅ | ❌ | ADR和文档索引中心 |
| **代码文件** | ✅ | ✅ | ✅ | ⚠️ | 删除需确认 |

### 文档管理规则 (来自 CLAUDE.md v3.1+)

**四层文档架构**:
1. **管理层** (docs/management/) - PRD, PLANNING, TASK, CONTEXT + (根目录) KNOWLEDGE
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

### Q1: AI 为什么重新实现功能而不使用项目工具？

**A**: 这是命令文档不够明确导致的。当命令文档只包含伪代码示例而没有明确指示使用工具路径时，AI 会认为需要自己实现。

**解决方案**:
1. 在命令文档中添加 "🛠️ 可用工具" 部分
2. 列出工具的实际路径和使用命令
3. 用实际 Bash 命令替换伪代码
4. 添加明确的执行规则（✅ 必须使用 / ❌ 禁止重新实现）

**效果**: Token 消耗减少 97.5%（8000 → 200 tokens）

**参考**: [ADR: 使用项目工具而非重新实现](docs/adr/2025-11-11-use-existing-tools-over-reimplementation.md)

### Q2: 如何判断何时需要 ADR？

**A**: 当面对以下情况时，考虑创建 ADR:
- 多个技术选项需要权衡
- 架构有重大改变
- 重构/优化有复杂的权衡
- 决策影响多个组件或团队
- AI 执行行为与预期不符

简单的 bug 修复或小功能不需要 ADR。

### Q3: Ultrathink 会不会让开发变慢？

**A**: 短期可能慢，长期能省时间。设计不优雅的系统，后期维护和扩展成本极高。提前投入时间做好设计，后面的日子更轻松。

### Q4: 什么时候应该停止打磨代码？

**A**: 当代码达到"不得不这样"的程度时。追求必然优雅，而不是完美。如果继续改进带不来显著收益，就该发布了。

### Q5: 团队成员对设计理念的理解不同怎么办？

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
- `/wf_14_doc` - 智能文档生成（从代码提取）

**核心文档**:
- [CLAUDE.md](CLAUDE.md) - AI 执行规则和权限矩阵
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计思维指南
- [COMMANDS.md](COMMANDS.md) - 命令完整参考
- [WORKFLOWS.md](WORKFLOWS.md) - 工作流场景指导
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查

---

**最后更新**: 2025-11-07
**维护**: Knowledge Base Management System
**相关**: [CLAUDE.md](CLAUDE.md), [PHILOSOPHY.md](PHILOSOPHY.md), [docs/adr/](docs/adr/)

---

## 🆕 新增功能 (v1.1)

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

**设计决策** (ADR 候选):
- 为什么不集成现有通用 prompts？
  * 通用模板缺乏项目特定性
  * 不支持增量更新和文档同步
  * "提取"优于"编造"
- 为什么是新命令而非增强现有？
  * 文档生成是独立的关键阶段
  * 保持命令职责单一性
  * 符合工作流模块化原则
