---
command: /wf_13_doc_maintain
index: 13
phase: "文档维护"
description: "文档架构维护，索引更新和归档管理"
model: haiku
reads: [PLANNING.md, KNOWLEDGE.md, docs/, TASK.md]
writes: [KNOWLEDGE.md, docs/archive/, 维护报告]
prev_commands: [/wf_11_commit, /wf_03_prime]
next_commands: [/wf_03_prime]
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

### 1. **Structure Audit**
Verify four-layer architecture compliance:

```
✓ Management Layer (Root):
  - PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md
  - Check file sizes (warn if >20KB for single file)
  - Total size should be <100KB for AI context efficiency

✓ Technical Layer (docs/):
  - docs/architecture/
  - docs/api/
  - docs/database/
  - docs/deployment/
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
```

**Output**:
- List of misplaced documents with suggested locations
- Management layer size report
- Structure compliance score (0-100%)

---

### 2. **Content Analysis**

#### A. Outdated Content Detection
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

#### B. Duplicate Content Detection
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

#### C. Orphaned Documents
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

### 3. **Index Verification**

Ensure KNOWLEDGE.md documentation index is accurate:

```
Checks:
✓ All technical documents listed in index
✓ Index paths are valid (files exist)
✓ Priorities are assigned (高/中/低)
✓ Last updated dates are accurate
✓ Task-document mappings are current
✓ No broken links in documentation map
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

### 4. **Optimization Suggestions**

Provide actionable recommendations:

#### Management Layer Optimization
```
If management docs > 100KB:
  → Extract technical details to docs/
  → Suggest content to move to KNOWLEDGE.md
  → Identify verbose sections for condensing
```

#### Technical Layer Organization
```
If docs/ has >50 files in single directory:
  → Suggest subdirectory structure
  → Group related documents
  → Create category README.md files
```

#### Working Layer Cleanup
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

### 5. **Archive Execution** (Requires Confirmation)

Move documents to archive layer:

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

### 6. **Generate Maintenance Report**

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
### Management Layer (5 docs, 87KB)
✓ All required files present
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

## Output Format

1. **Console Summary** - High-level statistics and warnings
2. **Detailed Report** - Markdown file with all findings (saved to docs/maintenance-report-YYYY-MM-DD.md)
3. **Action Plan** - Prioritized list of recommended actions
4. **Updated Files** - KNOWLEDGE.md with corrected index (if --auto)
5. **Archive Manifest** - List of archived files (if archiving occurred)

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

---

## Example Scenarios

### Scenario 1: Quarterly Maintenance
```bash
# End of Q4 2024
/wf_13_doc_maintain

# Output:
# 📊 Documentation Health: 88% (Good)
# ⚠️ Found 3 outdated docs, 2 orphans
# 💡 Suggest archiving to docs/archive/2024-Q4/
#
# Proceed with auto-fixes? [y/N]
```

### Scenario 2: Pre-Release Cleanup
```bash
# Before v2.0 release
/wf_13_doc_maintain --dry-run

# Review report, then:
/wf_13_doc_maintain --auto

# Confirm archiving outdated v1 docs
```

### Scenario 3: Daily Check (No Issues)
```bash
# After 10 commits
/wf_13_doc_maintain

# Output:
# ✅ Documentation Health: 95% (Excellent)
# ✅ All checks passed
# ℹ️ No maintenance needed
```

---

## Best Practices

1. **Run Regularly**: Don't let documentation debt accumulate
2. **Review Before Auto-Fix**: Always check report before --auto
3. **Preserve History**: Archive, don't delete (unless truly useless)
4. **Update Index**: Keep KNOWLEDGE.md in sync after manual doc changes
5. **Communicate**: If archiving shared docs, notify team

---

**See Also**:
- [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md) - Documentation structure reference
- [/wf_01_planning](wf_01_planning.md) - Initialize documentation
- [/wf_03_prime](wf_03_prime.md) - Context loading with smart doc selection
- [/wf_11_commit](wf_11_commit.md) - Updates CONTEXT.md and KNOWLEDGE.md
