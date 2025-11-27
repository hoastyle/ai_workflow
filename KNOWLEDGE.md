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
| 文档生成快速指南 | [docs/examples/doc_generation_quick_guide.md](docs/examples/doc_generation_quick_guide.md) | 高 |
| 文档生成决策树 | [docs/examples/doc_generation_decision_tree.md](docs/examples/doc_generation_decision_tree.md) | 高 |
| Frontmatter 快速参考 | [docs/examples/frontmatter_quick_reference.md](docs/examples/frontmatter_quick_reference.md) | 高 |
| **文档维护详细流程** | [docs/guides/doc_maintenance_process.md](docs/guides/doc_maintenance_process.md) | 高 |
| **文档维护工作流指南** | [docs/guides/doc_maintenance_workflows.md](docs/guides/doc_maintenance_workflows.md) | 高 |
| **wf_03_prime MCP Serena 增强指南** | [docs/guides/wf_03_prime_mcp_serena.md](docs/guides/wf_03_prime_mcp_serena.md) | 高 |
| **wf_03_prime 工作流导航指南** | [docs/guides/wf_03_prime_workflows.md](docs/guides/wf_03_prime_workflows.md) | 高 |
| **wf_03_prime 智能加载详解** | [docs/guides/wf_03_prime_smart_loading.md](docs/guides/wf_03_prime_smart_loading.md) | 中 |
| **wf_04_research MCP 增强指南** | [docs/guides/wf_04_research_mcp_guide.md](docs/guides/wf_04_research_mcp_guide.md) | 高 |
| **wf_04_research 工作流和决策指南** | [docs/guides/wf_04_research_workflows.md](docs/guides/wf_04_research_workflows.md) | 高 |
| **wf_04_research 输出格式规范** | [docs/guides/wf_04_research_output_formats.md](docs/guides/wf_04_research_output_formats.md) | 高 |
| 架构决策记录 | [docs/adr/](docs/adr/) | 中 |
| Frontmatter 规范 | [docs/reference/FRONTMATTER.md](docs/reference/FRONTMATTER.md) | 高 |
| Markdown 格式约束 | [docs/reference/MARKDOWN_STYLE.md](docs/reference/MARKDOWN_STYLE.md) | 高 |
| MCP 集成 | [docs/integration/](docs/integration/) | 高 |

### 文档生成模板和工作流 (新增 2025-11-27)

| 主题 | 路径 | 优先级 | 说明 |
|------|------|--------|------|
| **文档模板库** | [docs/examples/doc_templates/](docs/examples/doc_templates/) | 高 | 5种标准文档模板 (README, API, DEV_GUIDE, DEPLOYMENT, ARCHITECTURE) |
| README 模板 | [docs/examples/doc_templates/README_template.md](docs/examples/doc_templates/README_template.md) | 高 | 项目概览文档模板 |
| API 文档模板 | [docs/examples/doc_templates/API_template.md](docs/examples/doc_templates/API_template.md) | 高 | API 端点文档模板 |
| 开发指南模板 | [docs/examples/doc_templates/DEV_GUIDE_template.md](docs/examples/doc_templates/DEV_GUIDE_template.md) | 高 | 开发环境设置模板 |
| 部署文档模板 | [docs/examples/doc_templates/DEPLOYMENT_template.md](docs/examples/doc_templates/DEPLOYMENT_template.md) | 高 | 部署指南模板 |
| 架构文档模板 | [docs/examples/doc_templates/ARCHITECTURE_template.md](docs/examples/doc_templates/ARCHITECTURE_template.md) | 高 | 系统架构模板 |
| **约束驱动工作流** | [docs/examples/doc_generation_workflow.md](docs/examples/doc_generation_workflow.md) | 高 | 6步约束驱动文档生成流程 |
| **输出格式参考** | [docs/examples/doc_generation_outputs.md](docs/examples/doc_generation_outputs.md) | 高 | 3种标准报告格式 |
| **后续步骤指南** | [docs/examples/doc_generation_next_steps.md](docs/examples/doc_generation_next_steps.md) | 高 | 4种后续路径和决策表 |
| **最佳实践** | [docs/examples/doc_generation_best_practices.md](docs/examples/doc_generation_best_practices.md) | 高 | 使用时机、审查流程、性能优化 |
| **故障排查** | [docs/examples/doc_generation_troubleshooting.md](docs/examples/doc_generation_troubleshooting.md) | 高 | 限制说明和常见问题解决 |
| **UI 增强模板** | [docs/examples/doc_templates/ui_enhanced/](docs/examples/doc_templates/ui_enhanced/) | 中 | Magic MCP UI 组件模板 (4种) |
| **完整示例库** | [docs/examples/wf_14_doc_examples.md](docs/examples/wf_14_doc_examples.md) | 中 | /wf_14_doc 执行示例和参考 |

### 知识库详细文档 (docs/knowledge/)

- 📋 [设计模式](docs/knowledge/DESIGN_PATTERNS.md) - 工作流、权限、架构
- 📝 [文档最佳实践](docs/knowledge/DOCUMENTATION_PRACTICES.md) - 约束、流程
- 🐛 [常见问题](docs/knowledge/FAQ.md) - 系统、设计、架构问题
- 🆕 [版本历史](docs/knowledge/CHANGELOG.md) - 新增功能、设计决策

---

## 🏗️ 架构决策记录 (ADR)

**已有决策** (11个):

| 日期 | 标题 | 影响 | 状态 |
|------|------|------|------|
| 2025-11-27 | Serena MCP 集成扩展策略 | 高 | Proposed |
| 2025-11-24 | 约束驱动的文档生成最佳实践 | 高 | Accepted |
| 2025-11-23 | MCP 与管理文档的互补架构 | 高 | Accepted |
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

## ❓ 文档生成常见问题

### Q1：如何判断某个代码改动是否需要文档？

**A**: 使用决策树判断：
- **改动了公开 API** → 需要（Type C - API文档）
- **改变了现有行为** → 需要（Type A/D - 架构或FAQ）
- **使用了新技术** → 需要（Type B - ADR）
- **改变了系统架构** → 需要（Type A - 规划文档）
- **新增配置选项** → 需要（Type C - 部署文档）
- **代码优化** → 不需要（Type E - 无文档）

**经验法则**：如果下一个维护者需要了解"为什么"和"如何用"，就需要文档。

### Q2：为什么文档有大小约束？

**A**: 约束的三个价值：
1. **成本控制** - 管理人员和上下文消耗
2. **强制简洁** - 短文档更容易维护
3. **可验证性** - 提供自动化检查点

**约束规则**：
- KNOWLEDGE.md < 200 行（纯索引和摘要）
- 单个文件 < 500 行（复杂内容拆分）
- 每 commit 增长 < 30%（避免爆炸）

### Q3：文档生成超过约束怎么办？

**A**: 有三个解决方案：
1. **减少内容** - 删除非关键部分，保留核心
2. **拆分文件** - 大文档分为 2-3 个小文档
3. **清理旧文档** - 运行 `/wf_13_doc_maintain` 清理

### Q4：AI 生成的文档需要人工审查吗？

**A**: **是的**。约束驱动生成提供基础，需要 5-10 分钟的人工审查：
- [ ] 验证技术细节准确性
- [ ] 补充业务背景说明
- [ ] 添加图表或实例
- [ ] 验证代码示例可运行

### Q5：如何填写 Frontmatter 中的 related_documents？

**A**: 只列出真正相关的文档，最多 3-5 个：
```yaml
related_documents:
  - "docs/api/authentication.md"      # 认证机制
  - "docs/adr/2025-11-24-xxx.md"     # 设计决策
  - "KNOWLEDGE.md"                    # 知识库
```

**规则**：
- 使用相对路径（从项目根目录）
- 过多相关说明设计有问题

详见 [Frontmatter 实例集合](docs/examples/frontmatter_examples.md)

---

## 🔗 工作流和核心参考

**工作流命令**: `/wf_01_planning` → `/wf_02_task` → `/wf_03_prime` → `/wf_05_code` → `/wf_08_review` → `/wf_11_commit`

**核心参考**:
- [CLAUDE.md](CLAUDE.md) - AI 执行规则
- [PHILOSOPHY.md](PHILOSOPHY.md) - 设计思维
- [docs/adr/README.md](docs/adr/README.md) - ADR 指南

---

**最后更新**: 2025-11-24
**维护者**: Knowledge Base Management System
**版本**: v1.4 (新增文档生成完整工作流、决策树、Frontmatter 参考和 ADR)
