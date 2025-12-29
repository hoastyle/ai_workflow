# 最佳实践集合 (Best Practices)

**版本**: v1.0
**创建日期**: 2025-12-29
**来源**: 从项目 ADR 和设计哲学中提取

---

## 📚 文档索引

| 主题 | 文档 | 核心价值 |
|------|------|----------|
| **设计哲学** | [philosophy.md](philosophy.md) | Ultrathink 设计思维和 6 个核心原则 |
| **文档架构** | [document-architecture.md](document-architecture.md) | 四层文档架构和 SSOT 原则 |
| **约束驱动开发** | [constraint-driven.md](constraint-driven.md) | 从代码提取文档，而非凭空编造 |
| **AI 协作模式** | [ai-collaboration.md](ai-collaboration.md) | 与 AI 高效协作的最佳实践 |
| **上下文管理** | [context-management.md](context-management.md) | 会话连续性和上下文优化 |
| **代码质量** | [code-quality.md](code-quality.md) | 代码规范、格式化和质量门控 |

---

## 🎯 核心原则

### 1. Ultrathink 设计思维

**来源**: [PHILOSOPHY.md](../PHILOSOPHY.md)

**6 个核心原则**:

1. **Think Different** - 质疑假设，追求最优
   - 第一个能工作的方案往往不是最优的
   - 应用场景：架构设计、算法选择、系统边界划分

2. **Balance Trade-offs** - 明确权衡，记录决策
   - 每个决策都涉及取舍
   - 使用 ADR 记录"为什么"而非"是什么"

3. **Iterate to Excellence** - 持续打磨
   - 不懈地打磨细节，直到"不得不这样"
   - 拒绝"能工作就行"的心态

4. **Context Aware** - 理解环境
   - 技术选型必须考虑项目实际需求
   - 不盲目跟风新技术

5. **Document Decisions** - 沉淀学习
   - 记录决策的"为什么"
   - 形成项目资产，避免重复讨论

6. **Test Assumptions** - 验证假设
   - 通过 PoC 验证技术方案
   - 基于数据而非直觉做决策

### 2. 文档架构原则

**来源**: [ADR 2025-11-15](../docs/adr/2025-11-15-workflow-document-generation-ssot.md)

**四层文档架构**:

| 层级 | 位置 | 职责 | 加载策略 |
|------|------|------|----------|
| **管理层** | 项目根目录 | PRD, PLANNING, TASK, CONTEXT | 会话开始自动加载 |
| **技术层** | docs/ | API、架构、部署细节 | 按需加载 |
| **工作层** | docs/research/ | 临时探索和 Spike | 不自动加载 |
| **归档层** | docs/archive/ | 历史文档和废弃内容 | 不加载 |

**SSOT (Single Source of Truth) 原则**:
- 每个信息只有一个权威来源
- CONTEXT.md 是指针文档，不重复内容
- 使用索引而非复制来关联信息

### 3. 约束驱动文档生成

**来源**: [ADR 2025-11-18](../docs/adr/2025-11-18-constraint-driven-documentation-generation.md)

**核心思想**: 在文档生成时就内置约束检查，而非事后清理

**三阶段门控**:

1. **Phase 1**: 代码完成后的文档决策树
   - 确定需要哪些文档（类型、位置、大小）

2. **Phase 2**: 文档生成时的成本估计和门控
   - 生成前预估成本，超限时拒绝

3. **Phase 3**: 审查时的架构合规性检查
   - 验证 Frontmatter、分层、约束

**成本约束**:
- 类型 A (架构): PLANNING.md < 50 行
- 类型 B (决策): docs/adr/ < 200 行
- 类型 C (功能): docs/ < 500 行
- 类型 D (问题): KNOWLEDGE.md < 50 行
- 增长率: 单次 commit < 30%

### 4. 优先开源方案

**来源**: [ADR 2025-11-13](../docs/adr/2025-11-13-prioritize-opensource-in-architecture.md)

**核心原则**:

1. **优先开源** - 除非有特殊理由，不自己造轮子
2. **成熟优先** - 选择有社区、有文档、活跃维护的项目
3. **标准优先** - 选择业界标准方案，避免冷门库
4. **可维护性优先** - 考虑 5 年后的维护成本
5. **权衡明确** - 记录"为什么选这个？为什么不用那个？"

**技术选型流程**:
```
需求明确 → /wf_04_ask 初步咨询 → [如需深度研究] → /wf_04_research 开源方案评估
→ PLANNING.md 记录决策 → [可选 PoC] → /wf_07_test 验证 → 更新 ADR
```

### 5. AI 协作模式

**核心实践**:

1. **明确的上下文加载**
   - 每次会话开始运行 `/wf_03_prime`
   - 使用 CONTEXT.md 跨 `/clear` 边界保持状态

2. **约束驱动交互**
   - 在 CLAUDE.md 中明确 AI 执行规则
   - 使用 Frontmatter 定义文档元数据
   - 设置权限矩阵防止意外修改

3. **渐进式自动化**
   - 从简单任务开始自动化
   - 使用 MCP 扩展 AI 能力
   - 保持人工审查关键决策

4. **质量门控**
   - Pre-commit hooks 自动检查
   - 代码审查作为必须步骤
   - 测试覆盖率作为质量指标

---

## 📖 相关文档

### 架构决策记录 (ADR)

| 主题 | ADR | 日期 |
|------|-----|------|
| 智能文档生成 | [2025-11-07-intelligent-doc-generation-over-template-based.md](../docs/adr/2025-11-07-intelligent-doc-generation-over-template-based.md) | 2025-11-07 |
| 优先开源方案 | [2025-11-13-prioritize-opensource-in-architecture.md](../docs/adr/2025-11-13-prioritize-opensource-in-architecture.md) | 2025-11-13 |
| CONTEXT.md 指针文档 | [2025-11-15-context-md-pointer-document.md](../docs/adr/2025-11-15-context-md-pointer-document.md) | 2025-11-15 |
| SSOT 文档生成 | [2025-11-15-workflow-document-generation-ssot.md](../docs/adr/2025-11-15-workflow-document-generation-ssot.md) | 2025-11-15 |
| 约束驱动文档生成 | [2025-11-18-constraint-driven-documentation-generation.md](../docs/adr/2025-11-18-constraint-driven-documentation-generation.md) | 2025-11-18 |
| MCP 集成策略 | [2025-11-21-mcp-integration-strategy.md](../docs/adr/2025-11-21-mcp-integration-strategy.md) | 2025-11-21 |
| Agent 系统架构 | [2025-12-08-agent-system-architecture.md](../docs/adr/2025-12-08-agent-system-architecture.md) | 2025-12-08 |
| 优化策略总结 | [2025-12-03-superclaude-optimization-learnings.md](../docs/adr/2025-12-03-superclaude-optimization-learnings.md) | 2025-12-03 |

### 参考文档

| 文档 | 用途 |
|------|------|
| [CLAUDE.md](../CLAUDE.md) | AI 执行规则（源码开发规范） |
| [CLAUDE_DEPLOY.md](../CLAUDE_DEPLOY.md) | AI 执行规则（全局部署规范） |
| [PHILOSOPHY.md](../PHILOSOPHY.md) | Ultrathink 设计哲学 |
| [DOC_ARCHITECTURE.md](../DOC_ARCHITECTURE.md) | 文档架构设计 |
| [KNOWLEDGE.md](../KNOWLEDGE.md) | 知识库索引 |

---

## 🎯 应用场景

### 场景 1: 技术选型

**问题**: 需要选择一个新库/框架

**最佳实践**:
1. 使用 Ultrathink 原则质疑需求
2. 列出 3 个以上开源方案
3. 使用 `--research` 标志深度调研
4. 记录决策到 ADR
5. 通过 PoC 验证关键假设

### 场景 2: 文档生成

**问题**: 代码完成后需要生成文档

**最佳实践**:
1. 使用文档决策树确定文档类型
2. 估计文档成本，检查约束
3. 生成文档时添加完整 Frontmatter
4. 更新 KNOWLEDGE.md 索引
5. 运行 `/wf_13_doc_maintain` 验证

### 场景 3: 项目重构

**问题**: 需要重构代码结构

**最佳实践**:
1. 先用 Ultrathink 分析为什么需要重构
2. 记录当前架构问题到 ADR
3. 设计新架构并记录权衡
4. 渐进式重构，保持测试覆盖
5. 更新文档和索引

---

**最后更新**: 2025-12-29
**维护**: 根据新的 ADR 和经验持续更新
