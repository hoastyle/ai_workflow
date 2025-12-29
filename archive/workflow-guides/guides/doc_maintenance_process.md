---
title: "文档维护详细流程"
description: "wf_13_doc_maintain.md 的六步维护流程完整指南"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-11-27"
last_updated: "2025-11-27"
related_documents:
  - "../../wf_13_doc_maintain.md"
  - "../reference/FRONTMATTER.md"
  - "../../KNOWLEDGE.md"
related_code: []
---

# 文档维护详细流程

本文档详细说明 `/wf_13_doc_maintain` 命令的六步维护流程。

---

## 1. Structure Audit (结构审计)

Verify four-layer architecture compliance:

```
✓ 管理层 - 全局索引文件（项目根目录，⚠️ 不在 docs/management/ 中）:
  - 根目录/KNOWLEDGE.md       (必须在根目录！索引所有层级文档)
  - 根目录/CLAUDE.md          (全局 AI 执行规范)
  - 根目录/PHILOSOPHY.md      (设计哲学指南)
  - 根目录/README.md          (项目入口文档)
  - Check file sizes (warn if >20KB for single file)
  - Total size should be <100KB for AI context efficiency

✓ 项目管理文档（docs/management/ 目录）:
  - docs/management/PRD.md       (产品需求文档)
  - docs/management/PLANNING.md  (技术规划)
  - docs/management/TASK.md      (任务追踪)
  - docs/management/CONTEXT.md   (会话上下文指针)
  - Total size should be <80KB

✓ Technical Layer (docs/):
  - docs/architecture/
  - docs/api/
  - docs/database/
  - docs/deployment/
  - docs/reference/            (参考文档，如 FRONTMATTER.md, AI_ROLES_LIBRARY.md)
  - docs/examples/             (示例文档)
  - docs/adr/                  (架构决策记录)
  - Check for misplaced files (should be in appropriate subdirectories)

✓ Working Layer (docs/research/):
  - docs/research/spikes/
  - docs/research/prototypes/
  - Check for files with date prefixes (2024-10-XX-name.md)
  - Identify files older than 3 months

✓ Archive Layer (docs/archive/):
  - docs/archive/YYYY-QX/
  - docs/archive/deprecated/
  - Verify archived files have metadata (reason, replacement)

⚠️ 关键警告：
  - KNOWLEDGE.md 必须保持在项目根目录，绝不移动到 docs/management/
  - 原因：它是全局文档索引中心，需要索引所有四层（管理/技术/工作/归档）的文档
  - 如果发现 KNOWLEDGE.md 在 docs/management/，这是错误，必须移回根目录
```

**Output**:
- List of misplaced documents with suggested locations
- **CRITICAL**: KNOWLEDGE.md 位置验证（必须在根目录）
- Management layer size report (分别统计根目录和 docs/management/)
- Structure compliance score (0-100%)

---

## 2. Content Analysis (内容分析)

### A. Outdated Content Detection

Identify documents that may need updating or archiving:

```
Criteria for "Outdated":
- Last modified > 6 months AND no references in TASK.md or code
- Marked as "deprecated" but not in archive/
- Related feature removed from codebase
- Superseded by newer document (check git history)
```

**Analysis**:
- Scan all technical documents for last modification date
- Cross-reference with TASK.md active tasks
- Check git log for related code changes
- Identify documents with "TODO" or "WIP" markers older than 3 months

**Output**:
- List of potentially outdated documents with:
  * Last modified date
  * Reference count (TASK.md, KNOWLEDGE.md, code comments)
  * Suggested action (update / archive / delete)

### B. Duplicate Content Detection

Find and consolidate redundant information:

```
Detection Methods:
1. Exact duplicates: Same file content (MD5 hash)
2. Near duplicates: Similar headings and structure (>80% similarity)
3. Redundant sections: Same content across multiple files
```

**Analysis**:
- Compare all markdown files in technical layer
- Identify common sections across files
- Suggest consolidation strategies (merge / link / extract to shared doc)

**Output**:
- Pairs of duplicate/similar documents
- Redundant sections with consolidation suggestions
- Recommended refactoring actions

### C. Orphaned Documents

Discover documents without proper indexing or linking:

```
Orphan Criteria:
- Not listed in KNOWLEDGE.md documentation index
- No incoming links from other documents
- Not referenced in PLANNING.md or TASK.md
- Not mentioned in code comments or README
```

**Analysis**:
- Build document reference graph
- Identify documents with zero incoming edges
- Check if orphaned docs are still relevant

**Output**:
- List of orphaned documents
- Suggested index entries for KNOWLEDGE.md
- Recommendation: keep and link / archive / delete

---

## 3. Index Verification (索引验证)

Ensure KNOWLEDGE.md documentation index is accurate:

```
Checks:
✓ All technical documents listed in index
✓ Index paths are valid (files exist)
✓ Priorities are assigned (高/中/低)
✓ Last updated dates are accurate
✓ Task-document mappings are current
✓ No broken links in documentation map
✓ Frontmatter metadata is present and valid (NEW)
```

**Process**:
- Parse "📚 文档索引" section from KNOWLEDGE.md
- Verify each entry:
  * File exists at specified path
  * Priority is reasonable (based on reference count)
  * Last updated matches git log
  * Related tasks still exist in TASK.md
- Identify missing entries (technical docs not in index)

**Output**:
- Index accuracy report
- Missing entries to add
- Outdated entries to update/remove
- Auto-generated index updates

---

## 3.1. Frontmatter 一致性检查 (NEW)

验证所有技术文档的 frontmatter 元数据完整性和一致性。

**⚠️ 执行要求**: 必须从**项目根目录**运行（详见 [Frontmatter规范参考](../reference/FRONTMATTER.md) § 执行上下文）

### 运行验证命令

```bash
# 批量验证所有 docs/ 下的 markdown 文件
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 以 JSON 格式保存详细报告
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/ --format json > frontmatter-validation.json

# 查看报告
cat frontmatter-validation.json | jq '.'
```

**检查内容**:
- ✓ **Frontmatter 存在性** - 所有 docs/ 中的 .md 文件都包含 frontmatter
- ✓ **必需字段完整性** - 包含全部 7 个必需字段（title, description, type, status, priority, created_date, last_updated）
- ✓ **字段值有效性** - type/status/priority 使用标准枚举值
- ✓ **日期逻辑性** - created_date ≤ last_updated，日期格式正确
- ✓ **关系引用有效性** - related_documents 和 related_code 指向的文件存在
- ✓ **任务引用有效性** - related_tasks 在 TASK.md 中能找到

### 问题分类和处理

**返回结果格式**:
```json
[
  {
    "file": "docs/api/auth.md",
    "validation": {
      "valid": true,
      "errors": [],
      "warnings": [
        "建议添加推荐字段: related_documents"
      ]
    }
  },
  {
    "file": "docs/api/webhooks.md",
    "validation": {
      "valid": false,
      "errors": [
        "缺少必需字段: title",
        "缺少必需字段: description"
      ],
      "warnings": []
    }
  }
]
```

**基于错误类型的处理流程**:

| 错误类型 | 原因 | 解决方案 |
|---------|------|--------|
| **缺少 Frontmatter** | 文档没有元数据块 | 运行 `/wf_14_doc --update` 自动生成 |
| **缺少必需字段** | 字段不完整 | 运行 `/wf_14_doc --update` 补充或手动编辑 |
| **无效的枚举值** | type/status/priority 值错误 | 查看 FRONTMATTER.md § 枚举值定义，手动修正 |
| **引用文件不存在** | related_documents/code 指向的文件已删除 | 移除引用或更新路径 |
| **日期格式错误** | 日期不符合 YYYY-MM-DD 格式 | 手动修改为正确格式 |
| **日期逻辑错误** | created_date > last_updated | 调整日期使其符合逻辑 |

### 常见问题修复示例

**示例 1：缺少 Frontmatter**
```bash
# 自动生成 frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py generate docs/api/new-endpoint.md

# 输出会显示生成的 frontmatter，复制到文件顶部
```

**示例 2：引用文件不存在**
```bash
# 检查 related_documents 中的路径是否真的存在
ls -la docs/architecture/system-design.md

# 如果文件不存在，要么：
# a) 更新引用为正确路径
# b) 或从 related_documents 中移除该引用
```

**示例 3：日期不一致**
```bash
# 使用 /wf_11_commit 在提交时自动更新 last_updated
/wf_11_commit "fix: 更新文档"

# 脚本会自动更新所有修改过的文档的 last_updated
```

### 后续处理

1. **修复所有错误** - 按上表的解决方案处理每个错误
2. **重新验证** - 修复后再次运行验证命令确认通过
3. **更新 KNOWLEDGE.md** - 如果发现新的文档，添加到索引
4. **生成文档关系图** - 查看整个文档网络是否合理

```bash
# 生成文档关系图
python ~/.claude/commands/scripts/frontmatter_utils.py graph docs/ --format mermaid > docs/graph.mmd

# 或分析文档关系指标
python ~/.claude/commands/scripts/doc_graph_builder.py docs/ --analyze
```

**详细规范参考**: [Frontmatter规范参考](../reference/FRONTMATTER.md)
- § 标准模板 - 完整字段说明
- § 枚举值定义 - 所有有效值清单
- § 验证逻辑 - 验证规则实现
- § 工具和脚本 - 命令行使用方法

---

## 4. Optimization Suggestions (优化建议)

Provide actionable recommendations:

### Management Layer Optimization
```
If management docs > 100KB:
  → Extract technical details to docs/
  → Suggest content to move to KNOWLEDGE.md
  → Identify verbose sections for condensing
```

### Technical Layer Organization
```
If docs/ has >50 files in single directory:
  → Suggest subdirectory structure
  → Group related documents
  → Create category README.md files
```

### Working Layer Cleanup
```
Research docs older than 3 months:
  → Mark for review: convert to formal doc or archive
  → Suggest which spikes resulted in implemented features
  → Identify abandoned prototypes
```

**Output**:
- Prioritized optimization suggestions
- Estimated impact (context cost reduction, maintainability improvement)
- Implementation steps

---

## 5. Archive Execution (归档执行)

Move documents to archive layer (Requires Confirmation):

```
Archive Candidates:
1. Outdated content (>6 months, no references)
2. Deprecated features (code removed)
3. Completed research (working layer cleanup)
4. Superseded documents (newer version exists)
```

**Process**:
1. Present archive candidates with reasons
2. Ask user for confirmation: `Archive these N documents? [y/N]`
3. If confirmed:
   - Create archive directory (docs/archive/YYYY-QX/)
   - Move files with metadata:
     ```markdown
     ---
     archived: 2024-10-31
     reason: "Superseded by docs/api/rest-api-v2.md"
     original_path: "docs/api/rest-api-v1.md"
     ---
     ```
   - Update KNOWLEDGE.md index (remove archived entries)
   - Add archive summary to KNOWLEDGE.md
4. If `--dry-run`: Only show what would be archived

**Output**:
- Archive manifest (what was moved)
- Updated KNOWLEDGE.md
- Archive layer structure

---

## 6. Generate Maintenance Report (生成维护报告)

Create comprehensive documentation health report:

```markdown
# Documentation Maintenance Report

**Generated**: 2024-10-31
**Execution Mode**: [auto / manual / dry-run]

## Executive Summary
- Total documents: 45
- Management layer size: 87KB ✓
- Structure compliance: 92% ✓
- Outdated documents: 3 ⚠️
- Orphaned documents: 2 ⚠️
- Duplicates found: 1 pair ⚠️

## Structure Audit
### 🚨 CRITICAL Issues
✓ KNOWLEDGE.md location: 根目录 ✓ (正确位置)
  - If found in docs/management/, this would be CRITICAL ERROR

### 管理层 - 全局索引文件 (根目录, 4 docs, 45KB)
✓ KNOWLEDGE.md: 根目录 ✓
✓ CLAUDE.md: 根目录 ✓
✓ PHILOSOPHY.md: 根目录 ✓
✓ README.md: 根目录 ✓
✓ Size within limits

### 项目管理文档 (docs/management/, 4 docs, 42KB)
✓ PRD.md, PLANNING.md, TASK.md, CONTEXT.md present
✓ Size within limits

### Technical Layer (32 docs)
⚠️ 2 files misplaced:
  - docs/old-design.md → should be docs/archive/
  - docs/spike-auth.md → should be docs/research/spikes/

### Working Layer (5 docs)
⚠️ 3 files >3 months old - review needed

### Archive Layer (3 docs)
✓ Properly organized by quarter

## Content Analysis
### Outdated Documents (3)
1. docs/api/auth-v1.md (8 months old, superseded by v2)
   → Action: Archive
2. docs/deployment/old-pipeline.md (6 months old, CI/CD changed)
   → Action: Archive
3. docs/database/deprecated-schema.md (marked deprecated)
   → Action: Move to archive/deprecated/

### Duplicate Content (1 pair)
- docs/api/authentication.md ↔ docs/api/auth-flow.md (85% similar)
  → Suggestion: Merge into single comprehensive doc

### Orphaned Documents (2)
- docs/architecture/caching-strategy.md
  → Action: Add to KNOWLEDGE.md index, link from system-design.md
- docs/database/backup-procedure.md
  → Action: Add to KNOWLEDGE.md index (priority: 中)

## Index Verification
### KNOWLEDGE.md Status
✓ 28/32 technical docs indexed (87.5%)
⚠️ 4 missing index entries
✓ All indexed paths valid
⚠️ 2 outdated "last_updated" dates

### Recommended Index Updates
Add entries:
  - docs/architecture/caching-strategy.md
  - docs/database/backup-procedure.md
  - docs/api/webhooks.md
  - docs/deployment/monitoring.md

Update dates:
  - docs/api/authentication.md: 2024-08-15 → 2024-10-28
  - docs/database/schema.md: 2024-09-01 → 2024-10-15

## Optimization Suggestions
1. **High Priority**
   - Archive 3 outdated documents (reduce clutter)
   - Add 4 missing index entries (improve discoverability)

2. **Medium Priority**
   - Merge duplicate auth docs (reduce redundancy)
   - Link orphaned docs (improve connectivity)

3. **Low Priority**
   - Review working layer docs >3 months
   - Add category README.md to api/ directory

## Proposed Actions
If executed with --auto:
  - Archive 3 outdated documents to docs/archive/2024-Q4/
  - Update KNOWLEDGE.md with 4 new entries
  - Update 2 timestamp entries

Estimated context cost reduction: ~15KB
Estimated maintainability improvement: +12%

## Next Steps
1. Review this report
2. Run with `--auto` to apply safe changes, or
3. Manually handle edge cases
4. Re-run `/wf_03_prime` to reload updated context
```

---

**See Also**:
- [Frontmatter规范参考](../reference/FRONTMATTER.md) - 元数据标准
- [wf_13_doc_maintain.md](../../wf_13_doc_maintain.md) - 命令主文档
- [KNOWLEDGE.md](../../KNOWLEDGE.md) - 文档索引中心
