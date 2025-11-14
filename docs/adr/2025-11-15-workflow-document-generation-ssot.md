---
title: "Workflow 文档生成 SSOT 架构：消除系统性冗余"
date: 2025-11-15
status: "Accepted"
philosophy: ["Simplify Ruthlessly", "Think Different", "Obsess Over Details"]
impact: "high"
---

## 背景

### 问题陈述

Workflow 命令系统在设计时存在 **3 个系统性设计缺陷**，导致所有使用该系统的项目都会产生 management 文档冗余：

1. **缺陷 1 - /wf_02_task 任务格式要求记录"实现细节"**
   - 任务格式模板包含 `Notes: Implementation details or blockers`
   - 导致 TASK.md 记录大量已完成任务的实现细节（"实现 XX 类"、"创建 XX 文件"）
   - 这些细节已经在 **Git commit messages** 中记录，形成 100% 冗余
   - 影响：TASK.md 冗余率 **31%** (~150 行实现细节冗余)

2. **缺陷 2 - /wf_11_commit 未明确 TASK.md 更新边界**
   - Stage 3 的 "Update TASK.md with completions" 没有明确说明"什么算 completions"
   - 没有禁止记录实现细节
   - 没有指示使用 Git commits 作为 SSOT
   - 导致 AI 自由发挥，记录风格不一致，产生冗余

3. **缺陷 3 - /wf_01_planning 架构决策位置不明确**
   - Architecture 部分包含 "Technology decisions rationale"
   - 没有明确说明详细决策理由应该在 **docs/adr/**
   - 潜在风险：PLANNING.md 与 ADR 重复记录架构决策

### 约束条件

- 必须保持 workflow 系统的功能完整性
- 必须向后兼容现有项目（现有项目需要手动清理一次）
- 修复后的设计必须符合 SSOT (Single Source of Truth) 原则
- 修复方案必须清晰、易于 AI 理解和执行

### SSOT 违反分析

| 信息类型 | 当前设计要求放在 | SSOT 应该在 | 冲突 |
|---------|----------------|-----------|------|
| 实现细节 | TASK.md (Notes) | Git commit messages | ❌ 违反 |
| 任务完成状态 | TASK.md ✅ | TASK.md | ✅ 正确 |
| 架构决策理由 | PLANNING.md (Technology decisions rationale) | docs/adr/ | ❌ 违反 |
| 技术栈列表 | PLANNING.md ✅ | PLANNING.md | ✅ 正确 |
| 代码变更详情 | （未明确禁止记录） | Git commit messages | ⚠️ 模糊 |

---

## 选项分析

### 选项 A: 修复 3 个命令文件的设计缺陷（推荐）

**描述**: 直接修改 3 个核心命令文件，明确 SSOT 边界和禁止事项。

**修复内容**:

1. **wf_02_task.md** (Lines 48-57):
   - 删除 `Notes: Implementation details or blockers`
   - 替换为 `Git commits: [hash]`, `Related ADR: [link]`, `Blockers: [reason]`
   - 添加 "SSOT Principles" 说明

2. **wf_11_commit.md** (Lines 137-142):
   - 明确 TASK.md 更新边界（✅ DO / ❌ DON'T）
   - 添加 TASK.md 更新格式模板
   - 禁止记录实现细节

3. **wf_01_planning.md** (Lines 48-60):
   - 修改 "Technology decisions rationale" → "Technology decisions (What, not Why)"
   - 添加 ADR 引用示例
   - 明确 PLANNING.md 只记录 "是什么"，不记录 "为什么"

**优势**:
- ✅ 直接解决问题根源
- ✅ 所有新项目自动零冗余
- ✅ 修改最小，影响最小
- ✅ 符合 SSOT 原则

**劣势**:
- 现有项目需要手动清理一次（参考 CONTEXT.md/TASK.md 的清理方案）
- 需要更新相关文档（CLAUDE.md, KNOWLEDGE.md）

**成本估计**: 1 小时（修改 3 个文件）

---

### 选项 B: 创建新的文档生成规范文档

**描述**: 创建一个新的 `docs/reference/DOCUMENT_GENERATION.md` 文档，详细说明各类文档的生成规范，但不修改命令文件。

**优势**:
- ✅ 集中管理所有文档生成规范
- ✅ 不修改命令文件，风险更小

**劣势**:
- ❌ AI 不会主动读取该文档，依赖 AI 自觉性
- ❌ 不解决命令文件的设计缺陷
- ❌ 仍会产生冗余（除非 AI 每次都记得查文档）
- ❌ 无法保证一致性

**成本估计**: 2 小时（创建文档 + 测试验证）

---

### 选项 C: 组合方案（修复命令 + 创建规范文档）

**描述**: 既修改命令文件（选项 A），又创建规范文档（选项 B）。

**优势**:
- ✅ 双重保障：命令文件 + 规范文档
- ✅ 便于用户查询和理解

**劣势**:
- ❌ 工作量翻倍
- ❌ 可能产生新的冗余（命令文件 vs 规范文档）
- ❌ 维护成本高（需要同步更新两处）

**成本估计**: 3 小时

---

## 决策

**我们选择了: 选项 A - 修复 3 个命令文件的设计缺陷**

### 理由

1. **直接解决根源**: 修改命令文件是最直接的解决方案，AI 执行命令时会自动遵守新规范
2. **最小化成本**: 只需修改 3 个文件，工作量最小
3. **长期收益最大**: 所有未来项目都自动零冗余，不需要依赖 AI 自觉性
4. **SSOT 原则**: 命令文件是唯一的权威来源，不需要额外文档
5. **向后兼容**: 现有项目只需手动清理一次（已有成功案例：CONTEXT.md）
6. **Ultrathink 对齐**:
   - **Simplify Ruthlessly**: 直接修复设计缺陷，不引入额外复杂性
   - **Think Different**: 从"事后清理"转变为"事前预防"
   - **Obsess Over Details**: 精确定义每个文档的职责边界

### 关键考量

1. **影响范围**: 所有使用 workflow 的项目（当前项目 + 未来项目）
2. **修复成本**: 低（~1 小时）
3. **收益**:
   - 消除 TASK.md 31% 冗余
   - 消除 PLANNING.md 潜在冗余
   - 统一所有项目的文档格式
4. **风险**: 低（向后兼容，现有项目手动清理一次即可）

---

## 影响分析

### 正面影响

1. **系统性解决冗余**: 所有使用 workflow 的项目都不会再产生这些冗余
2. **统一文档格式**: 所有项目的 TASK.md、PLANNING.md 格式一致
3. **降低维护成本**: SSOT 清晰，修改只需一处
4. **提升可读性**: 文档更简洁，查询实现细节统一使用 `git log`
5. **长期收益**: 新项目从一开始就是零冗余

### 变更范围

**需要修改的文件** (3个):
1. `wf_02_task.md` - 任务格式模板（Lines 48-67）
2. `wf_11_commit.md` - TASK.md 更新规范（Lines 137-174）
3. `wf_01_planning.md` - Architecture 部分说明（Lines 48-79）

**需要更新的文档** (2个):
1. `KNOWLEDGE.md` - 添加 ADR 索引
2. `docs/adr/2025-11-15-workflow-document-generation-ssot.md` - 本 ADR

**破坏性变更**: 无
- 现有项目继续使用旧格式不会报错
- 建议现有项目手动清理一次 TASK.md（参考 `/tmp/task_md_redundancy_analysis.md`）

### 迁移计划

1. **Phase 1** (完成): 修改 3 个命令文件
2. **Phase 2** (完成): 创建本 ADR
3. **Phase 3** (下一步): 更新 KNOWLEDGE.md
4. **Phase 4** (可选): 手动清理当前项目的 TASK.md

---

## 权衡

### 收益

| 指标 | 修复前 | 修复后 | 改进 |
|------|--------|--------|------|
| TASK.md 冗余率 | 31% | <5% | **-84%** |
| PLANNING.md 冗余风险 | 潜在高 | 零 | **完全消除** |
| SSOT 违反次数 | 3 处 | 0 处 | **完全消除** |
| 文档格式一致性 | 不一致 | 统一 | **100%** |
| 影响范围 | **所有项目** | **所有项目** | **系统性修复** |

### 成本

- **实现时间**: 1 小时（修改 3 个文件）
- **文档更新**: 2 个文件（ADR + KNOWLEDGE.md）
- **现有项目清理**: 可选，手动清理一次 TASK.md（~1 小时）

### 风险

- **低风险**: 向后兼容，现有项目可选择性清理
- **测试成本**: 需要验证 /wf_02_task 和 /wf_11_commit 的集成

---

## 成功指标

**量化指标**:
- [x] wf_02_task.md 添加 SSOT Principles 说明
- [x] wf_11_commit.md 添加 TASK.md 更新格式模板
- [x] wf_01_planning.md 添加 ADR 引用示例
- [ ] 新项目的 TASK.md 冗余率 < 5%（待验证）
- [ ] PLANNING.md 不包含架构决策详细理由（待验证）

**质量指标**:
- [x] 符合 SSOT 原则（所有信息只有一个真实来源）
- [x] Ultrathink 对齐度 ⭐⭐⭐⭐⭐ (5/5)
- [ ] 现有项目手动清理后冗余率 < 5%（待验证）
- [ ] 所有项目文档格式一致（待验证）

---

## 后续行动

1. **立即执行**:
   - [x] 修改 wf_02_task.md (完成)
   - [x] 修改 wf_11_commit.md (完成)
   - [x] 修改 wf_01_planning.md (完成)
   - [x] 创建本 ADR (当前)
   - [ ] 更新 KNOWLEDGE.md 添加 ADR 索引

2. **可选执行**（当前项目）:
   - [ ] 手动清理 TASK.md 的已完成任务部分（参考 `/tmp/task_md_redundancy_analysis.md`）
   - [ ] 删除 TASK.md 的"📝 笔记和决策"部分（已有 ADR 记录）

3. **测试验证**:
   - [ ] 运行 /wf_02_task 验证新格式
   - [ ] 运行 /wf_11_commit 验证 TASK.md 更新逻辑
   - [ ] 在新项目中测试整个工作流

4. **3个月后重新评估** (2025-02-15):
   - 评估新项目的冗余率
   - 收集用户反馈
   - 评估是否需要进一步优化

---

## 修复后的 SSOT 架构

### 文档职责清晰化

| 文档 | 职责 | 记录内容 | 不记录内容 |
|------|------|---------|-----------|
| **TASK.md** | 任务追踪 | 任务名、状态、优先级、Git commits | ❌ 实现细节、代码变更 |
| **Git commits** | 代码变更 | 实现细节、代码行数、技术细节 | ❌ 任务状态、架构决策 |
| **PLANNING.md** | 架构描述 | 技术栈列表（What） | ❌ 决策理由（Why） |
| **docs/adr/** | 架构决策 | 决策背景、选项、权衡、理由（Why） | ❌ 实现细节、代码 |
| **KNOWLEDGE.md** | 索引中心 | ADR 索引、文档索引 | ❌ 详细内容（仅指针） |
| **CONTEXT.md** | 会话指针 | 指针+元数据 | ❌ 任何重复内容 |

### 信息流转图

```
/wf_05_code 完成功能
  ↓
/wf_11_commit 提交代码
  ↓
├─ Git commit message: 实现细节（SSOT）
│  - "实现 FrontmatterValidator 类"
│  - "添加类型注解"
│  - "修复错误处理"
│
├─ TASK.md: 任务状态 + 指针
│  - [x] 完善脚本类型注解
│  - Completed: 2025-11-15
│  - Git commits: abc1234
│  - Details: git log abc1234
│
└─ ADR (如有架构决策): 决策理由（SSOT）
   - docs/adr/2025-11-15-decision.md
   - 背景、选项、权衡、理由
```

---

## 相关决策

- **ADR 2025-11-15**: [CONTEXT.md 指针文档模式](./2025-11-15-context-md-pointer-document.md) - 同样强调 SSOT 原则，消除 85% 冗余
- **ADR 2025-11-13**: [优先考虑开源方案](./2025-11-13-prioritize-opensource-in-architecture.md) - 体现了 "Think Different" 哲学
- **ADR 2025-11-11**: [使用项目工具而非重新实现](./2025-11-11-use-existing-tools-over-reimplementation.md) - 强调重用优于重写

---

## 参考资料

- **SSOT 原则**: [Single Source of Truth (Wikipedia)](https://en.wikipedia.org/wiki/Single_source_of_truth)
- **Ultrathink 设计哲学**: [PHILOSOPHY.md](../../PHILOSOPHY.md)
- **文档架构**: [CLAUDE.md § 文档管理规则](../../CLAUDE.md)
- **冗余分析报告**: `/tmp/workflow_document_generation_analysis.md`
