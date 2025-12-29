---
title: "文档维护工作流指南"
description: "wf_13_doc_maintain.md 的工作流路径、示例场景和最佳实践"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-11-27"
last_updated: "2025-11-27"
related_documents:
  - "../../wf_13_doc_maintain.md"
  - "doc_maintenance_process.md"
  - "../../KNOWLEDGE.md"
related_code: []
---

# 文档维护工作流指南

本文档说明 `/wf_13_doc_maintain` 命令的工作流路径选择、示例场景和最佳实践。

---

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程中的**定期维护阶段**：

```
[项目启动] → [任务规划] → [加载上下文] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [提交保存] → [文档维护 ← 当前] → [重新加载]
  STEP 0       STEP 0.5        STEP 1         STEP 2       STEP 3       STEP 4       STEP 5            STEP 6            STEP 8          STEP 1
```

### ✅ 已完成的步骤

执行 `/wf_13_doc_maintain` 前，通常已经完成：

- ✅ **多次提交或定期维护触发** (STEP 6) - 已进行 10+ 次 `/wf_11_commit`
  - 或者：季度末进行定期维护
  - 或者：大版本发布前进行清理

### 📝 当前步骤

**正在执行**: `/wf_13_doc_maintain [--auto] [--dry-run]` (文档架构维护)

**这个命令的职责**：
- 审计四层文档架构的合规性
- 检测过期、重复、孤立的文档
- 验证 KNOWLEDGE.md 索引的准确性
- 检查所有文档的 Frontmatter 完整性
- 提供文档优化建议
- 执行文档归档（需确认）

### ⏭️ 建议下一步

**文档维护完成后**，根据执行模式和发现选择下一步：

#### 路径 1：一切正常，重新加载上下文 ✅
```bash
# 当前: 文档检查完成，无需修改或修改已完成
# 下一步: 重新加载项目上下文

/wf_03_prime

# 后续: 继续开发工作
/wf_05_code "继续实现功能"
```
**适用场景**: 运行 `--dry-run` 确认无问题，或执行 `--auto` 自动修复已完成

#### 路径 2：发现问题需要手动处理 🔧
```bash
# 当前: 识别了需要手动处理的问题（可能 dry-run 输出）
# 下一步: 按照报告建议手动处理

# 按优先级处理建议:
# - 高优先级: 归档过期文档、更新 KNOWLEDGE.md 索引
# - 中优先级: 合并重复内容、修复 Frontmatter 问题
# - 低优先级: 链接孤立文档、组织工作层文档

# 手动处理后运行自动验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 处理完成后重新加载上下文
/wf_03_prime
```
**适用场景**: 需要人工审核和决定的问题，或涉及团队沟通的归档操作

#### 路径 3：季度末全面维护 📅
```bash
# 当前: 季度末进行全面文档维护
# 下一步: 使用 --auto 执行所有安全的自动修复

# Step 1: 先运行 --dry-run 预览
/wf_13_doc_maintain --dry-run

# Step 2: 审查报告，确认无问题
# Step 3: 执行自动修复
/wf_13_doc_maintain --auto

# Step 4: 如果有交互式提示（如：是否归档），确认选择
# (系统会询问是否接受 archive 操作)

# Step 5: 重新加载上下文
/wf_03_prime

# Step 6: 提交维护记录
/wf_11_commit "docs: 季度末文档维护 (Q4 2025)"
```
**适用场景**: 定期季度末维护，进行全面的文档清理和优化

#### 路径 4：发布前清理 🚀
```bash
# 当前: 大版本发布前进行文档清理
# 下一步: 执行发布前的文档检查

# Step 1: 预览将要改动的内容
/wf_13_doc_maintain --dry-run

# Step 2: 审查报告，确保不删除重要文档
# Step 3: 执行自动修复（这会清理过期 v1 文档等）
/wf_13_doc_maintain --auto

# Step 4: 提交清理结果
/wf_11_commit "docs: 发布前文档清理 (v2.0 发布準備)"

# Step 5: 重新加载上下文供发布测试
/wf_03_prime
```
**适用场景**: 即将发布新版本，需要清理旧版本文档和过期内容

### 📊 工作流进度提示

当你完成文档维护时，确保输出中包含：

✅ 已完成:
- 文档结构合规性评分
- 过期、重复、孤立文档的清单
- KNOWLEDGE.md 索引准确性报告
- Frontmatter 验证结果
- 优化建议的优先级列表
- 处理的文件清单（如果执行了 --auto）

⏭️ 下一步提示:
- 建议执行的路径（1/2/3/4）
- 是否需要手动处理某些问题
- 执行的修改摘要（文件移动、索引更新等）
- 预计的上下文成本减少量

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 日常维护，检查无问题 | 路径 1 | /wf_03_prime → /wf_05_code |
| 发现需要手动处理的问题 | 路径 2 | 手动处理 → /wf_03_prime |
| 季度末定期全面维护 | 路径 3 | --dry-run → --auto → /wf_03_prime |
| 大版本发布前清理 | 路径 4 | --dry-run → --auto → /wf_11_commit |

**何时使用 --dry-run？**
- 不确定会发生什么改动时
- 归档敏感的文档前
- 第一次运行 --auto 时
- 需要向团队展示改动时

**何时使用 --auto？**
- 已审查 --dry-run 的报告
- 修改都是安全的（如索引更新）
- 时间紧张的定期维护
- 团队同意了 archiving 决策

---

## Example Scenarios (示例场景)

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

### Scenario 4: CRITICAL - KNOWLEDGE.md Misplaced
```bash
# Detecting critical structure error
/wf_13_doc_maintain

# Output:
# 🚨 CRITICAL ERROR: KNOWLEDGE.md found in docs/management/
# 📍 Expected location: 项目根目录
# 📍 Current location: docs/management/KNOWLEDGE.md
#
# ⚠️ This breaks the documentation architecture!
#
# 🔧 Recommended fix:
#   git mv docs/management/KNOWLEDGE.md ./KNOWLEDGE.md
#   /wf_11_commit "fix: 恢复 KNOWLEDGE.md 到根目录（修正误操作）"
#
# Would you like to fix this automatically? [Y/n]
```

---

## Best Practices (最佳实践)

1. **🚨 Verify KNOWLEDGE.md Location First**: Always check KNOWLEDGE.md is in root directory
   - KNOWLEDGE.md 必须在项目根目录
   - 如果在 docs/management/，立即修复
   - 这是结构审计的第一优先级检查项

2. **Run Regularly**: Don't let documentation debt accumulate
   - 每 10 次提交后运行
   - 季度末进行全面维护
   - 大版本发布前清理

3. **Review Before Auto-Fix**: Always check report before --auto
   - 先运行 --dry-run 预览改动
   - 审查将要归档的文档
   - 确认索引更新的准确性

4. **Preserve History**: Archive, don't delete (unless truly useless)
   - 归档而非删除过期文档
   - 保留归档元数据（原因、替代文档）
   - 按季度组织归档目录

5. **Update Index**: Keep KNOWLEDGE.md in sync after manual doc changes
   - 手动修改文档后更新索引
   - 定期验证索引准确性
   - 移除已归档文档的索引条目

6. **Communicate**: If archiving shared docs, notify team
   - 归档团队共享文档前通知
   - 说明归档原因和替代方案
   - 提供旧文档的访问路径

7. **Understand Layer Separation**:
   - 根目录 = 全局索引文件（KNOWLEDGE.md, CLAUDE.md, PHILOSOPHY.md）
   - docs/management/ = 项目管理文档（PRD, PLANNING, TASK, CONTEXT）
   - 两者职责不同，不可混淆

---

## Integration Notes (集成说明)

### When to Run (何时运行)
- **Automatic Trigger**: After every 10 commits (tracked in CONTEXT.md)
- **Scheduled**: End of each quarter (Q1/Q2/Q3/Q4)
- **Manual**: When documentation feels cluttered or disorganized
- **Before Major Release**: Ensure documentation is clean

### Integration with Other Commands (与其他命令的集成)
- **After `/wf_11_commit`**: Count commits, suggest maintenance if threshold reached
- **Before `/wf_03_prime`**: Clean docs ensure optimal context loading
- **Updates `/wf_01_planning`**: May suggest updates to Documentation Architecture section
- **Complements `/wf_08_review`**: Code review + doc review = complete quality check

### Success Metrics (成功指标)
- Management layer size < 100KB ✓
- All technical docs indexed in KNOWLEDGE.md ✓
- <5% duplicate content ✓
- <10% orphaned documents ✓
- Structure compliance >90% ✓
- **All technical docs have valid Frontmatter ✓ (NEW)**
- **Frontmatter reference accuracy >95% ✓ (NEW)**
- **反向引用一致性 >90% ✓ (NEW)**

---

**See Also**:
- [doc_maintenance_process.md](doc_maintenance_process.md) - 六步维护流程详细说明
- [wf_13_doc_maintain.md](../../wf_13_doc_maintain.md) - 命令主文档
- [DOC_ARCHITECTURE.md](../../DOC_ARCHITECTURE.md) - 文档结构参考
- [/wf_03_prime](../../wf_03_prime.md) - 上下文加载
- [/wf_11_commit](../../wf_11_commit.md) - 提交更改
