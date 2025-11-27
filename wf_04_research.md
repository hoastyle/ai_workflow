---
command: /wf_04_research
index: 04.5
phase: "开发实现"
description: "开源方案深度研究，系统化评估和对比技术选项 | MCP: --c7 | --research"
reads: [PLANNING.md, KNOWLEDGE.md, TASK.md]
writes: [KNOWLEDGE.md, PLANNING.md(可能), docs/adr/(可能), TASK.md(可能)]
prev_commands: [/wf_04_ask]
next_commands: [/wf_01_planning, /wf_05_code]
model: sonnet
mcp_support:
  - name: "Context7"
    flag: "--c7"
    detail: "查询官方文档和API参考"
  - name: "Tavily"
    flag: "--research"
    detail: "深度搜索社区讨论和性能数据"
context_rules:
  - "系统化评估开源方案，记录决策过程"
  - "更新KNOWLEDGE.md中的方案对比表"
  - "重大决策创建ADR记录"
  - "输出结构化的评估报告"
---

## 🔌 MCP 增强能力

本命令支持以下 MCP 服务器的可选增强，提供全方位的技术研究支持：

| MCP 服务器 | 标志 | 主要用途 | 自动激活 |
|-----------|------|--------|--------|
| **Context7** | `--c7` | 官方文档、API、最佳实践查询 | 检测到框架/库名 |
| **Tavily** | `--research` | 社区讨论、GitHub 趋势、性能数据 | 否（需明确启用） |
| **组合使用** | `--c7 --research` | 官方+社区双重验证的综合研究 | 二者结合 |
| **禁用 MCP** | `--no-mcp` | 基于项目经验的纯文本分析 | 不启用 |

### 快速参考 - Context7 vs Tavily

**Context7** (官方文档查询):
- ✅ API 参考和使用指南
- ✅ 官方性能基准和推荐配置
- ✅ 版本兼容性和升级路径

**Tavily** (实时市场数据):
- ✅ GitHub Stars 趋势和活跃度
- ✅ Stack Overflow 和 Reddit 社区反馈
- ✅ 真实 benchmark 测试和采用案例
- ✅ 已知问题和社区抱怨

**推荐用法**: 重要决策时使用 `--c7 --research` 获得官方+社区的双重验证

详见: [§ wf_04_research MCP 增强指南](docs/guides/wf_04_research_mcp_guide.md)

---

## 执行上下文
**输入**: 技术需求 + 候选开源方案列表
**输出**: 详细的方案对比分析 + 推荐方案 + 评估报告 + KNOWLEDGE.md更新
**依赖链**: /wf_04_ask → **当前（开源方案深度研究）** → /wf_01_planning/wf_05_code

## Usage
`/wf_04_research <TECH_TOPIC> [<CANDIDATE_COUNT>]`

## Context
- Technology topic or challenge: $ARGUMENTS
- Candidate solutions count: $ARGV[1] (default: 3-5 solutions)
- PLANNING.md provides project context and constraints
- KNOWLEDGE.md contains historical decisions and tech comparisons
- Goal: Deep evaluation of open-source options with structured analysis

## Your Role
You are a Senior Technology Research Specialist providing comprehensive analysis:
1. **Solution Researcher** – discovers relevant open-source projects
2. **Comparative Analyst** – evaluates solutions against requirements
3. **Risk Assessor** – identifies integration and maintenance risks
4. **Documentation Expert** – records decisions for future reference
5. **OpenSource Strategist** – evaluates long-term viability

## Process

### 1. 需求澄清
- 明确需要什么功能
- 理解项目约束和限制
- 定义评估标准（功能、性能、维护性、成本等）

### 2. 方案发现
- [必须] 发现至少 5 个相关的开源项目
- [推荐] 包括市场领导者、新兴项目、小众方案
- [推荐] 考虑不同的技术路线（例：查询语言有 SQL vs NoSQL）
- [必须] 记录发现来源（GitHub Star、PyPI、npm、Crates.io 等）

### 3. 深度评估
对每个候选方案评估以下维度：

#### 功能维度
- 核心功能是否满足需求
- 缺少哪些功能
- 扩展性（插件、中间件等）
- 文档完整性和质量

#### 社区维度
- GitHub Stars / Fork 数量趋势
- 最近更新时间（活跃度）
- Issue / PR 响应速度
- 贡献者数量和多样性
- 社区规模和论坛活跃度

#### 技术维度
- 代码质量（复杂度、测试覆盖率）
- 依赖数量和依赖质量
- 性能基准（如果重要）
- 安全性审计记录
- 架构设计是否清晰

#### License和法务
- License 类型（MIT、Apache、GPL 等）
- 与项目 License 的兼容性
- 商业使用限制
- 贡献者协议（CLA）

#### 成本评估
- 学习成本（文档、社区、教程质量）
- 集成成本（需要多少改动）
- 维护成本（升级频率、破坏性变更、迁移成本）
- 替代方案的转换成本

### 4. 对比分析
- 创建详细的对比表格
- 突出显示优势和劣势
- 分析不同方案的权衡

### 5. 推荐和决策
- [必须] 给出明确的推荐
- [必须] 解释推荐理由
- [可选] 列出备选方案及其适用场景
- [推荐] 记录是否需要 PoC 验证

### 6. 文档和记录
- 更新或创建 KNOWLEDGE.md 中的方案对比表
- [重大决策] 创建 ADR 记录
- 更新 PLANNING.md（如果已有初步决策）
- 为后续集成创建任务

## Output Format

本命令的输出分为 6 个标准部分，具体内容根据是否启用 MCP 而略有不同：

| 部分 | 标准输出 | +--c7 增强 | +--research 增强 | +--c7 --research |
|------|--------|----------|-----------------|-----------------|
| **1. 研究总结** | ✅ | ✅ 添加官方资源链接 | ✅ 添加社区认可度 | ✅✅ 全面摘要 |
| **2. 需求和标准** | ✅ | ✅ | ✅ | ✅ |
| **3. 方案评估** | ✅ 基础评估 | ✅ 官方文档 | ✅ 社区反馈 | ✅✅ 官方+社区 |
| **4. 对比矩阵** | ✅ 基础对比 | ✅ 文档链接 | ✅ 趋势数据 | ✅✅ 综合评分 |
| **5. 推荐方案** | ✅ | ✅ | ✅ | ✅ |
| **6. 后续行动** | ✅ | ✅ | ✅ | ✅ |

### 详细格式说明

每个输出部分的模板、示例和最佳实践详见：

**[§ wf_04_research 输出格式规范](docs/guides/wf_04_research_output_formats.md)**

关键内容包括：
- 标准输出格式模板
- MCP 增强的额外内容
- 符号和指数使用规范
- KNOWLEDGE.md 方案对比表格式
- 输出验证检查清单

## KNOWLEDGE.md 更新

**添加或更新方案对比表**:

```markdown
## 方案对比：[技术主题]

| 方案 | 功能完整性 | 社区活跃度 | 集成成本 | 总体评分 | 备注 |
|------|----------|----------|--------|--------|------|
| 方案A | ✅✅✅ | 🟢 活跃 | 低 | ⭐⭐⭐⭐⭐ | 推荐 |
| 方案B | ✅✅ | 🟡 稳定 | 中 | ⭐⭐⭐⭐ | 备选 |
| 方案C | ✅ | 🔴 衰落 | 高 | ⭐⭐ | 不推荐 |

**评估日期**: YYYY-MM-DD
**评估者**: [AI/Team]
**决策状态**: 待确认 / 已选择: [方案名]
**相关ADR**: [如果有]
**最后更新**: YYYY-MM-DD
```

## 何时需要研究

- 系统中引入新技术栈的组件
- 现有方案需要替换升级
- 多个可行方案需要权衡决策
- 团队对技术选型有疑问

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[启动] → [规划] → [加载] → [咨询] → [深度研究 ← 当前] → [实现] → [测试] → [审查] → [提交]
STEP 0   STEP 0.5   STEP 1   STEP 2     STEP 2.5              STEP 3   STEP 4   STEP 5   STEP 6
```

### 工作流进度和路径选择

深度研究完成后有 4 条建议工作流路径，选择取决于研究结果的确定性、风险等级和决策重要性：

| 路径 | 场景 | 下一步命令 | 适用条件 |
|------|------|----------|--------|
| **路径 1** | 推荐明确，无需验证 | `/wf_01_planning` → `/wf_05_code` | 信息充分，可直接推进 |
| **路径 2** | 需要 PoC 验证可行性 | `/wf_05_code` (PoC) → `/wf_07_test` → `/wf_04_ask` | 有技术风险需验证 |
| **路径 3** | 方案权衡需讨论 | `/wf_04_ask` → 根据结果选择 | 多个方案各有优缺点 |
| **路径 4** | 重大决策需记录 | 创建 ADR → `/wf_01_planning` | 关键组件替换或架构影响 |

### 详细工作流指南

包括完整的命令序列、决策矩阵、输出检查清单等详见：

**[§ wf_04_research 工作流和决策指南](docs/guides/wf_04_research_workflows.md)**

关键决策点：
- [ ] 何时需要 PoC 验证？
- [ ] 何时需要创建 ADR？
- [ ] 如何选择最合适的工作流路径？
- [ ] 输出中应包含哪些内容？

## 相关文档
- **项目规划**: PLANNING.md (技术栈部分)
- **知识库**: KNOWLEDGE.md (方案对比表)
- **架构决策**: docs/adr/ (技术选型 ADR)
- **技术规范**: CLAUDE.md (技术选型规范)
