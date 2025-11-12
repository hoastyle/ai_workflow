---
command: /wf_04_research
index: 04.5
phase: "开发实现"
description: "开源方案深度研究，系统化评估和对比技术选项"
reads: [PLANNING.md, KNOWLEDGE.md, TASK.md]
writes: [KNOWLEDGE.md, PLANNING.md(可能), docs/adr/(可能), TASK.md(可能)]
prev_commands: [/wf_04_ask]
next_commands: [/wf_01_planning, /wf_05_code]
context_rules:
  - "系统化评估开源方案，记录决策过程"
  - "更新KNOWLEDGE.md中的方案对比表"
  - "重大决策创建ADR记录"
  - "输出结构化的评估报告"
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

### 1. 研究总结
- 研究的技术主题
- 评估的候选方案数量
- 最终推荐方案

### 2. 需求和评估标准
- 明确的功能需求
- 非功能性需求（性能、可维护性等）
- 项目特定的约束条件

### 3. 候选方案详细评估

**格式**（对每个方案）:
```markdown
## 方案 X: [项目名称]

**基本信息**:
- 主页: [URL]
- GitHub: [URL]
- 开发语言: [Language]
- 最新版本: [Version]
- 最近更新: [Date]
- License: [Type]

**功能评估** (满足需求程度):
- [功能1]: ✅ 完全支持 / ⚠️ 部分支持 / ❌ 不支持
- [功能2]: ...
- 缺少功能: [列表]

**社区活跃度**:
- GitHub Stars: [Number] (趋势: ↑/→/↓)
- 最近更新: [Days] 前
- 活跃贡献者: [Number]
- Issue 响应时间: [Average]
- 社区规模评价: 🔴 衰落 / 🟡 稳定 / 🟢 活跃 / 🟣 非常活跃

**技术质量**:
- 代码质量: [评价] (基于 [指标])
- 依赖数量: [数字] (是否过多？)
- 测试覆盖率: [数字或评价]
- 安全性: [是否有已知安全问题]

**集成成本**:
- 学习曲线: [简陡/中等/陡峭]
- API 复杂度: [简单/中等/复杂]
- 所需代码改动: [少/中等/大量]
- 迁移成本（如有现有方案）: [成本评估]

**优势**:
1. [优势1]
2. [优势2]
3. [优势3]

**劣势和风险**:
1. [劣势1]
2. [劣势2]
3. [风险]

**总体评价**: [简短评价]
**推荐指数**: ⭐⭐⭐⭐⭐ (5星)
```

### 4. 对比矩阵
创建表格对比所有方案的关键维度

### 5. 推荐方案
- **推荐**: [方案名]
- **理由**: [清晰的推荐理由]
- **风险和缓解措施**: [可能的问题 + 如何应对]
- **备选方案**: [如果推荐方案有问题时的替代方案]

### 6. 后续行动
- [ ] 是否需要 PoC 验证？ (如果是，为什么？)
- [ ] 是否需要创建 ADR？ (重大决策时)
- [ ] 建议的下一步命令：
  - 如果需要验证: → /wf_05_code 实现 PoC
  - 如果确认无误: → /wf_01_planning 更新技术栈决策
  - 如果有新问题: → /wf_04_ask 架构再咨询

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

## 工作流导航

### 工作流位置指示
```
技术需求明确
  ↓
/wf_04_ask 初步咨询 (快速评估)
  ↓
[需要深度研究时]
→ /wf_04_research (当前) ← 系统化详细评估
  ↓
[评估完成后]
→ /wf_01_planning 更新 PLANNING.md
  ↓
→ [可选] /wf_05_code 实现 PoC 验证
  ↓
→ [重大决策] 创建 ADR 记录
```

### 成功指标
- ✅ 发现了 5+ 个相关开源方案
- ✅ 为每个方案创建了详细评估
- ✅ 创建了对比矩阵方便决策
- ✅ 给出了明确的推荐和理由
- ✅ 更新了 KNOWLEDGE.md
- ✅ [重大决策] 创建了 ADR

## 相关文档
- **项目规划**: PLANNING.md (技术栈部分)
- **知识库**: KNOWLEDGE.md (方案对比表)
- **架构决策**: docs/adr/ (技术选型 ADR)
- **技术规范**: CLAUDE.md (技术选型规范)
