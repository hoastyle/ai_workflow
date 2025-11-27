---
command: /wf_13_doc_maintain
index: 13
phase: "文档维护"
description: "文档架构维护，索引更新和归档管理"
reads: [PLANNING.md, KNOWLEDGE.md, docs/, TASK.md]
writes: [KNOWLEDGE.md, docs/archive/, 维护报告]
prev_commands: [/wf_11_commit, /wf_03_prime]
next_commands: [/wf_03_prime]
model: haiku
context_rules:
  - "定期执行（每10次提交或季度末）"
  - "自动识别文档问题，提供优化建议"
  - "归档操作需用户确认"
---

## 执行上下文
**输入**: 项目所有文档 + KNOWLEDGE.md索引
**输出**: 文档维护报告 + 优化建议 + 更新的索引
**依赖链**: /wf_11_commit (多次) → **当前（定期维护）** → /wf_03_prime (重新加载)

## Usage
`/wf_13_doc_maintain [--auto] [--dry-run]`

## Purpose
Maintain project documentation architecture to ensure:
- Documents follow the four-layer structure (Management/Technical/Working/Archive)
- Documentation index in KNOWLEDGE.md is up-to-date and accurate
- Outdated content is identified and archived appropriately
- Duplicate content is detected and consolidated
- Orphaned documents are discovered and linked properly
- AI context cost remains optimized (management layer < 100KB)

## Process

**完整的六步维护流程详见**: [docs/guides/doc_maintenance_process.md](docs/guides/doc_maintenance_process.md)

**流程概览表**:

| 步骤 | 名称 | 职责 | 关键输出 | 详细说明 |
|-----|------|------|---------|---------|
| **Step 1** | Structure Audit | 验证四层架构合规性 | 📍 **CRITICAL**: KNOWLEDGE.md 位置验证<br/>📊 结构合规性评分<br/>📋 错位文档清单 | [§ 1 - Structure Audit](docs/guides/doc_maintenance_process.md#1-structure-audit-结构审计) |
| **Step 2** | Content Analysis | 检测过期、重复、孤立文档 | 📃 过期文档清单<br/>🔁 重复内容对<br/>🔗 孤立文档列表 | [§ 2 - Content Analysis](docs/guides/doc_maintenance_process.md#2-content-analysis-内容分析) |
| **Step 3** | Index Verification | 验证 KNOWLEDGE.md 索引准确性 | ✅ 索引准确性报告<br/>➕ 缺失条目<br/>🔄 过时条目 | [§ 3 - Index Verification](docs/guides/doc_maintenance_process.md#3-index-verification-索引验证) |
| **Step 3.1** | Frontmatter 一致性检查 | 验证所有技术文档的元数据完整性 | ✓ Frontmatter 验证报告<br/>❌ 错误和警告清单<br/>📈 文档关系图 | [§ 3.1 - Frontmatter Check](docs/guides/doc_maintenance_process.md#31-frontmatter-一致性检查-new) |
| **Step 4** | Optimization Suggestions | 提供可执行的优化建议 | 📊 优先级建议<br/>💡 估计影响<br/>📝 实施步骤 | [§ 4 - Optimization](docs/guides/doc_maintenance_process.md#4-optimization-suggestions-优化建议) |
| **Step 5** | Archive Execution | 归档过期文档（需确认） | 📦 归档清单<br/>✏️ 更新的 KNOWLEDGE.md<br/>📁 归档层结构 | [§ 5 - Archive](docs/guides/doc_maintenance_process.md#5-archive-execution-归档执行) |
| **Step 6** | Generate Report | 生成综合维护报告 | 📋 健康报告<br/>📊 Executive Summary<br/>⏭️ 下一步建议 | [§ 6 - Report](docs/guides/doc_maintenance_process.md#6-generate-maintenance-report-生成维护报告) |

**关键检查点**:
- 🚨 **CRITICAL**: KNOWLEDGE.md 必须在根目录（不在 docs/management/）
- ✅ 管理层文档 < 100KB（根目录 + docs/management/）
- ✅ 所有技术文档有完整 Frontmatter（7个必需字段）
- ✅ KNOWLEDGE.md 索引准确率 > 90%
- ✅ 文档结构合规性 > 90%

---

## Output Format

| 输出类型 | 内容 | 位置 |
|---------|------|------|
| **Console Summary** | 高级统计和警告 | 终端输出 |
| **Detailed Report** | 完整发现清单和建议 | `docs/maintenance-report-YYYY-MM-DD.md` |
| **Action Plan** | 优先级排序的建议操作 | 报告中 § Proposed Actions |
| **Updated Files** | 修正后的索引（如果 --auto） | `KNOWLEDGE.md` |
| **Archive Manifest** | 归档文件清单（如果执行归档） | 报告中 § Archive |

**完整报告示例**: 详见 [doc_maintenance_process.md § 6 - Generate Report](docs/guides/doc_maintenance_process.md#6-generate-maintenance-report-生成维护报告)

---

## Command Options

### `--auto`
Execute safe automatic fixes:
- Update KNOWLEDGE.md index (add missing, fix timestamps)
- Move misplaced files to correct directories
- Archive documents with clear criteria (>6 months, no refs)
- Requires confirmation for destructive actions

### `--dry-run`
Show what would be changed without making changes:
- Generate full report
- Show proposed actions
- Display updated KNOWLEDGE.md (preview)
- No files are modified

**Default**: Interactive mode - report + ask for confirmation

---

## 📌 工作流导航

**完整的工作流路径、示例场景和最佳实践详见**: [docs/guides/doc_maintenance_workflows.md](docs/guides/doc_maintenance_workflows.md)

### 维护完成后的 4 种路径

| 路径 | 场景 | 下一步命令 | 说明 |
|-----|------|----------|------|
| **路径 1** | 检查无问题 | `/wf_03_prime` | 重新加载上下文，继续开发 |
| **路径 2** | 需手动处理 | 手动修复 → `/wf_03_prime` | 按优先级处理发现的问题 |
| **路径 3** | 季度末维护 | `--dry-run` → `--auto` → `/wf_03_prime` | 全面清理和优化 |
| **路径 4** | 发布前清理 | `--dry-run` → `--auto` → `/wf_11_commit` | 清理旧版本文档 |

**详细工作流步骤、决策指南和示例**: 参见 [doc_maintenance_workflows.md](docs/guides/doc_maintenance_workflows.md)

---

## Integration Notes

### When to Run
- **Automatic Trigger**: After every 10 commits (tracked in CONTEXT.md)
- **Scheduled**: End of each quarter (Q1/Q2/Q3/Q4)
- **Manual**: When documentation feels cluttered or disorganized
- **Before Major Release**: Ensure documentation is clean

### Integration with Other Commands
- **After `/wf_11_commit`**: Count commits, suggest maintenance if threshold reached
- **Before `/wf_03_prime`**: Clean docs ensure optimal context loading
- **Updates `/wf_01_planning`**: May suggest updates to Documentation Architecture section
- **Complements `/wf_08_review`**: Code review + doc review = complete quality check

### Success Metrics
- Management layer size < 100KB ✓
- All technical docs indexed in KNOWLEDGE.md ✓
- <5% duplicate content ✓
- <10% orphaned documents ✓
- Structure compliance >90% ✓
- **All technical docs have valid Frontmatter ✓ (NEW)**
- **Frontmatter reference accuracy >95% ✓ (NEW)**
- **反向引用一致性 >90% ✓ (NEW)**

---

## Example Scenarios

**完整示例和命令输出详见**: [docs/guides/doc_maintenance_workflows.md § Example Scenarios](docs/guides/doc_maintenance_workflows.md#example-scenarios-示例场景)

| 场景 | 触发时机 | 预期结果 | 详细说明 |
|------|---------|---------|---------|
| **Scenario 1** | 季度末维护 | 发现过期文档，建议归档 | [Quarterly Maintenance](docs/guides/doc_maintenance_workflows.md#scenario-1-quarterly-maintenance) |
| **Scenario 2** | 发布前清理 | 清理旧版本文档 | [Pre-Release Cleanup](docs/guides/doc_maintenance_workflows.md#scenario-2-pre-release-cleanup) |
| **Scenario 3** | 日常检查 | 健康度 95%，无需维护 | [Daily Check](docs/guides/doc_maintenance_workflows.md#scenario-3-daily-check-no-issues) |
| **Scenario 4** | 检测关键错误 | KNOWLEDGE.md 位置错误 | [CRITICAL Check](docs/guides/doc_maintenance_workflows.md#scenario-4-critical---knowledgemd-misplaced) |

---

## Best Practices

**完整最佳实践详见**: [docs/guides/doc_maintenance_workflows.md § Best Practices](docs/guides/doc_maintenance_workflows.md#best-practices-最佳实践)

**核心原则**:
1. 🚨 **CRITICAL**: KNOWLEDGE.md 必须在根目录（第一优先级检查）
2. 📅 定期运行（每 10 次提交/季度末/发布前）
3. 👀 先 --dry-run 预览，再 --auto 执行
4. 📦 归档而非删除（保留历史）
5. 📑 手动修改文档后更新索引
6. 💬 归档共享文档前通知团队
7. 🏗️ 理解层级分离（根目录索引 vs docs/management/ 管理文档）

---

**See Also**:
- [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md) - Documentation structure reference
- [/wf_01_planning](wf_01_planning.md) - Initialize documentation
- [/wf_03_prime](wf_03_prime.md) - Context loading with smart doc selection
- [/wf_11_commit](wf_11_commit.md) - Updates CONTEXT.md and KNOWLEDGE.md
