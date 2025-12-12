---
title: "wf_11_commit 工作流指南"
description: "Git提交管理的详细执行指南、4阶段流程和标准输出模板"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-12"
last_updated: "2025-12-12"
related_documents:
  - "../../wf_11_commit.md"
  - "../command_consistency_strategy.md"
  - "wf_05_code_workflows.md"
  - "wf_08_review_workflows.md"
related_code: []
---

# wf_11_commit 工作流指南

本文档提供 `/wf_11_commit` 命令的详细执行流程和标准化输出模板，确保AI提交过程的一致性和质量。

---

## 🤖 AI执行协议（强制）

**本节为AI执行的强制规范，必须严格遵循，不得跳过或自行解释**

### 核心原则

1. **强制读取**: AI必须首先读取本文档的关键章节
2. **严格遵循**: 所有步骤按顺序执行，不得合并或跳过
3. **标准输出**: 必须使用本文档提供的输出模板
4. **检查验证**: 完成前必须通过所有检查清单项
5. **质量优先**: 提交前必须通过所有质量门控

### 执行流程概览

```
Step 0: 读取执行指南（强制）
  ↓
Step 1: 4阶段提交流程选择
  ├─ Stage 1: Preparation (修复和校验) → 预处理和质量检查
  ├─ Stage 2: Analysis (分析和更新) → 变更分析和文档生成
  ├─ Stage 3: Commit (提交和验证) → Git提交和验证
  └─ Stage 4: Finalization (完成和报告) → CONTEXT.md更新和报告
  ↓
Final: 输出提交报告（使用标准模板）
```

---

## 🎯 4阶段提交流程（强制执行）

**AI必须按照以下4个阶段顺序执行，不得跳过或合并**：

### Stage 1: Preparation (修复和校验)
**目标**: 清理代码、修复常见问题、校验质量

**核心决策**: 检测并选择质量门控策略

```
检查项目是否配置了 .pre-commit-config.yaml？
│
├─ YES (项目有 pre-commit 配置)
│  ├─ pre-commit 工具已安装?
│  │  ├─ YES → 使用 Path A: Pre-commit Framework
│  │  └─ NO → 使用 Path B: Self-managed Fixes + 提示安装
│  └─
│
└─ NO (项目无 pre-commit 配置)
   └─ 使用 Path B: Self-managed Fixes
```

**Path A: Pre-commit Framework (推荐)**
- 执行 `pre-commit run` (仅对staged文件)
- 由框架处理：trailing whitespace, line endings, formatting
- 验证所有hooks通过

**Path B: Self-managed Fixes (备选)**
- 手动修复 trailing whitespace (`sed -i 's/[[:space:]]*$//'`)
- 修复 line endings (`dos2unix` 或 `sed -i 's/\r$//'`)
- 基础 Markdown 格式化
- 自定义质量检查

**通用处理**:
- 自动更新维护日期: `$(date +%Y-%m-%d)`
- 更新 Frontmatter `last_updated` 字段
- 验证 Frontmatter 格式完整性

### Stage 2: Analysis & Generation (分析和更新)
**目标**: 理解变更内容、生成文档、评估README更新需求

**变更分析**:
```
1. 分析变更范围
   - 代码文件 vs 文档文件
   - 新功能 vs 修复 vs 重构
   - 影响的模块和依赖关系

2. 确定文档需求
   - 是否需要更新 README.md?
   - 是否需要添加 KNOWLEDGE.md 条目?
   - 是否有新的设计模式或解决方案?

3. MCP Serena 增强（如可用）
   - 符号级变更检测
   - 引用完整性验证
   - 跨文件依赖分析
```

**文档生成决策**:
- **重大功能** → 更新 README.md
- **新模式/解决方案** → 添加到 KNOWLEDGE.md
- **架构变更** → 考虑更新 PLANNING.md
- **小修复/调整** → 仅提交消息记录

### Stage 3: Commit (提交和验证)
**目标**: 执行Git提交并验证结果

**提交流程**:
```bash
# 1. 暂存所有相关文件
git add [修改的文件]

# 2. 生成语义化提交消息
格式: [type] subject

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>

# 3. 执行提交
git commit -m "$(cat <<'EOF'
[生成的提交消息]
EOF
)"

# 4. 验证提交成功
git log -1 --oneline
```

**提交消息格式**:
- **type**: feat, fix, docs, refactor, test, style, chore
- **subject**: 简明描述变更内容
- **body**: 详细说明（如需要）
- **标准签名**: Co-Authored-By: Claude Sonnet 4

### Stage 4: Finalization (完成和报告)
**目标**: 更新CONTEXT.md、生成报告、提供后续建议

**自动更新 CONTEXT.md**:
```markdown
# CONTEXT.md 更新模板

**最后会话**: $(date +%Y-%m-%d %H:%M)
**Git 基准**: commit $(git rev-parse --short HEAD)

## 📍 上下文指针 (Context Pointers)

### 当前工作焦点
- 活跃任务: TASK.md § [任务描述] (Line X)
- 相关架构: PLANNING.md § [章节] (如适用)
- 相关 ADR: KNOWLEDGE.md § [ADR日期] (如适用)

### 会话状态
- Git commits (本次会话): X commits ([哈希列表])
- 修改文件数: X files
- 主要变更领域: [领域描述]

### 下次启动时
- 推荐命令: /wf_03_prime
- 推荐下一步: [基于TASK.md的建议]
```

---

## 📋 质量门控决策树（自适应）

**AI必须根据项目配置选择合适的质量检查策略**：

### 检测逻辑
```bash
# Step 1: 检测项目配置
HAS_PRECOMMIT=$([ -f .pre-commit-config.yaml ] && echo "true" || echo "false")
HAS_PRECOMMIT_TOOL=$(command -v pre-commit >/dev/null 2>&1 && echo "true" || echo "false")

# Step 2: 选择策略
if [ "$HAS_PRECOMMIT" = "true" ] && [ "$HAS_PRECOMMIT_TOOL" = "true" ]; then
    STRATEGY="precommit_framework"
elif [ "$HAS_PRECOMMIT" = "true" ] && [ "$HAS_PRECOMMIT_TOOL" = "false" ]; then
    STRATEGY="selfmanaged_with_warning"
else
    STRATEGY="selfmanaged_basic"
fi
```

### 策略对比

| 策略 | 适用场景 | 质量检查 | 性能 | 可靠性 |
|------|---------|---------|------|--------|
| **precommit_framework** | 项目配置了.pre-commit-config.yaml + 工具已安装 | 高（项目定制） | 快（增量） | 高（框架管理） |
| **selfmanaged_with_warning** | 项目有配置但工具未安装 | 中（基础检查） | 中 | 中（提示安装） |
| **selfmanaged_basic** | 项目无pre-commit配置 | 低（基础检查） | 快 | 中（手动实现） |

---

## 📊 变更影响分析模式

**AI必须分析变更的影响范围和文档需求**：

### 影响分析维度

```
1. 文件类型分析
   ├─ 代码文件 (.py, .ts, .js, .go, etc.)
   │  ├─ 新增功能? → 考虑 README.md 更新
   │  ├─ 修复BUG? → 记录解决方案到 KNOWLEDGE.md
   │  └─ 重构? → 检查架构影响
   │
   ├─ 文档文件 (.md)
   │  ├─ PLANNING.md → 架构决策变更
   │  ├─ README.md → 项目描述更新
   │  └─ docs/* → 技术文档修订
   │
   └─ 配置文件 (.yaml, .json, .toml)
      ├─ 构建配置 → 可能影响部署
      ├─ 依赖管理 → 记录依赖变更理由
      └─ 工作流配置 → 过程改进

2. 功能影响分析
   ├─ 用户可见功能? → 更新 README.md § 功能列表
   ├─ 开发工作流程? → 更新 README.md § 开发指南
   ├─ 新设计模式? → 添加到 KNOWLEDGE.md
   └─ 架构变更? → 考虑更新 PLANNING.md

3. 集成影响分析
   ├─ API 变更? → 检查向后兼容性
   ├─ 数据库变更? → 记录迁移策略
   ├─ 第三方依赖? → 记录选择理由
   └─ 配置变更? → 文档化配置要求
```

### 文档更新决策矩阵

| 变更类型 | README.md | KNOWLEDGE.md | PLANNING.md | 提交消息 |
|---------|-----------|--------------|-------------|----------|
| **新用户功能** | ✅ 功能列表 | 可选 | 可选 | 详细描述 |
| **BUG修复** | 如果重大 | ✅ 解决方案 | 如果架构相关 | 问题和解决方案 |
| **重构** | 如果影响使用 | ✅ 新模式 | ✅ 设计变更 | 重构理由 |
| **工具改进** | ✅ 开发指南 | ✅ 最佳实践 | 可选 | 工具配置 |
| **文档更新** | 如果结构变更 | 如果新知识 | 如果架构相关 | 文档改进 |

---

## 🔧 MCP Serena 增强协议（可选）

**当 Serena MCP 可用时，AI应该执行额外的代码完整性检查**：

### 符号级完整性验证

```python
# 检测代码符号变更的完整性
def verify_symbol_integrity():
    """
    使用 Serena MCP 验证代码变更的完整性
    确保函数重命名、签名变更等操作的引用都已正确更新
    """

    # Step 1: 获取本次提交的修改文件
    modified_files = get_staged_files()

    # Step 2: 对每个代码文件进行符号分析
    for file_path in modified_files:
        if is_code_file(file_path):
            symbols = serena.get_symbols_overview(file_path)

            for symbol in symbols:
                # Step 3: 检查符号的所有引用
                references = serena.find_referencing_symbols(
                    symbol.name_path,
                    file_path
                )

                # Step 4: 验证引用的一致性
                for ref in references:
                    if not is_reference_consistent(ref, symbol):
                        report_integrity_issue(symbol, ref)

    # Step 5: 如果发现问题，阻止提交
    if integrity_issues:
        print("❌ 代码完整性验证失败")
        print("请修复所有引用不一致问题后重新提交")
        exit(1)
    else:
        print("✅ 代码完整性验证通过")
```

### 典型应用场景

1. **函数重命名验证**
   - 检测 `getUserData()` → `fetchUserData()` 的重命名
   - 确保所有调用点都已更新
   - 防止遗漏的旧名称引用

2. **API 签名变更验证**
   - 检测函数参数变化：`authenticate(user, pass)` → `authenticate(credentials)`
   - 验证所有调用点使用新签名
   - 识别不兼容的调用

3. **模块重构验证**
   - 检测文件移动或重构：`utils/helper.py` → `services/data.py`
   - 验证所有 import 语句已更新
   - 确保依赖关系完整

---

## ✅ 执行检查清单（AI必须验证）

**在输出最终提交报告前，AI必须确认以下所有项目**：

### Stage 1 检查（Preparation）
- [ ] ✅ 已检测项目的质量门控配置（pre-commit vs self-managed）
- [ ] ✅ 已执行相应的质量修复流程
- [ ] ✅ 已更新所有维护日期为当前日期
- [ ] ✅ 已验证 Frontmatter 格式完整性
- [ ] ✅ 所有质量检查通过（无 trailing whitespace, 正确 line endings）

### Stage 2 检查（Analysis）
- [ ] ✅ 已分析变更影响范围（代码/文档/配置）
- [ ] ✅ 已确定文档更新需求（README/KNOWLEDGE/PLANNING）
- [ ] ✅ 如使用 Serena MCP，已执行符号完整性检查
- [ ] ✅ 已识别新的设计模式或解决方案（如适用）

### Stage 3 检查（Commit）
- [ ] ✅ 已生成语义化提交消息（[type] subject 格式）
- [ ] ✅ 提交消息包含 Co-Authored-By 签名
- [ ] ✅ 已成功执行 `git commit`
- [ ] ✅ 已验证提交哈希和内容

### Stage 4 检查（Finalization）
- [ ] ✅ 已按指针文档模式更新 CONTEXT.md（~50行，无冗余）
- [ ] ✅ CONTEXT.md 包含正确的 git 基准和会话状态
- [ ] ✅ 已基于 TASK.md 提供下一步建议
- [ ] ✅ 已更新相关文档（README/KNOWLEDGE，如适用）

### 输出格式检查
- [ ] ✅ 使用了本文档提供的标准输出模板
- [ ] ✅ 提交报告包含完整的4阶段执行总结
- [ ] ✅ 提供了明确的后续工作建议
- [ ] ✅ 错误和警告都有清晰的解决方案

### 质量验证检查
- [ ] ✅ 所有文件无 trailing whitespace
- [ ] ✅ 所有文件使用统一的 line endings (LF)
- [ ] ✅ Markdown 格式符合项目标准
- [ ] ✅ Git 仓库状态clean（无未提交的临时更改）

**如果任何检查项未通过，必须重新执行对应阶段**

---

## 📤 标准输出模板

### 成功提交报告模板

```markdown
## 🎯 提交完成报告

**提交哈希**: [git_hash]
**提交消息**: [commit_message]
**提交时间**: [timestamp]

### Stage 1: Preparation 结果
**质量门控**: [precommit_framework|selfmanaged_basic|selfmanaged_with_warning]
**修复项目**:
- ✅ Trailing whitespace: [数量] 处已修复
- ✅ Line endings: [数量] 个文件已修复
- ✅ 维护日期: [数量] 个文件已更新
- ✅ Frontmatter: [数量] 个文档已验证

### Stage 2: Analysis 结果
**变更范围**: [影响的文件类型和模块]
**文档更新**:
- README.md: [已更新|无需更新] - [更新内容概述]
- KNOWLEDGE.md: [已添加|无需更新] - [新增模式或解决方案]
- PLANNING.md: [已更新|无需更新] - [架构变更]

**MCP 增强**:
- Serena 完整性检查: [✅ 通过|⚠️ 不可用|❌ 发现问题]

### Stage 3: Commit 结果
**提交统计**:
```
[git diff --stat 输出]
```

**提交验证**: ✅ 提交成功，哈希为 [短哈希]

### Stage 4: Finalization 结果
**CONTEXT.md**: ✅ 已更新会话状态和git基准
**会话状态**:
- 本次修改: [X] 个文件
- 累计提交: [X] 个
- 主要变更: [变更领域描述]

### 下一步建议

**立即可执行**:
- ✅ 代码已提交，工作进度已保存
- ✅ 可以安全执行 `/clear` 清理上下文

**后续工作**:
- 📋 继续相关任务: [基于 TASK.md 的建议]
- 🔄 恢复工作: 使用 `/wf_03_prime` 重新加载上下文
- 🚀 部署准备: [如果相关] 考虑运行 `/wf_12_deploy_check`

**工作流连续性**: ✅ 确保下次会话可通过 `/wf_03_prime` 无缝继续
```

### 错误处理报告模板

```markdown
## ❌ 提交失败报告

**失败阶段**: Stage [X] - [阶段名称]
**错误类型**: [质量检查失败|Git错误|MCP错误|其他]

### 问题详情
**错误描述**: [具体错误信息]
**影响文件**: [相关文件列表]
**错误位置**: [文件:行号，如适用]

### 解决方案
**自动修复**: [可自动修复的问题]
**手动处理**: [需要人工干预的问题]
**建议操作**:
1. [具体修复步骤1]
2. [具体修复步骤2]
3. 重新运行 `/wf_11_commit "[消息]"`

### 预防措施
**工具建议**: [如安装 pre-commit 等]
**流程改进**: [如提前运行检查]
**配置优化**: [项目配置建议]
```

---

## 🔧 常见问题和最佳实践

### Q1: 何时更新 README.md？

**答案**:
- ✅ **新用户可见功能**: 添加到功能列表
- ✅ **开发流程改变**: 更新开发指南部分
- ✅ **依赖或安装要求变更**: 更新安装说明
- ❌ **内部重构**: 如果不影响用户使用，无需更新
- ❌ **小BUG修复**: 除非是关键功能的修复

### Q2: KNOWLEDGE.md 应该记录什么？

**答案**:
- ✅ **新的设计模式**: 可复用的代码模式
- ✅ **解决方案**: 特定问题的解决方法
- ✅ **最佳实践**: 开发中的经验总结
- ✅ **工具配置**: 有效的工具设置
- ❌ **临时解决方案**: 不应作为长期模式
- ❌ **项目特定细节**: 应该记录在 PLANNING.md

### Q3: 提交消息应该多详细？

**答案**:
- **Subject行**: 简明扼要（50字符以内）
- **Body**: 解释"为什么"而不是"是什么"
- **包含影响**: 如果影响API或用户体验
- **参考问题**: 如果修复特定BUG或实现特定需求

### Q4: 质量检查失败怎么办？

**答案**:
1. **分析失败原因**: 查看具体错误消息
2. **确定修复策略**: 自动修复 vs 手动修复
3. **执行修复**: 优先使用自动化工具
4. **重新验证**: 确保修复完整
5. **重新提交**: 使用相同或更新的提交消息

### Q5: 如何处理 Serena MCP 完整性错误？

**答案**:
1. **理解错误**: 查看具体的符号引用问题
2. **修复引用**: 更新所有不一致的引用
3. **验证修复**: 重新运行完整性检查
4. **如果复杂**: 考虑分步骤重构和提交
5. **无法修复**: 暂时跳过 MCP 检查（添加 --no-verify 等）

---

## 📚 相关文档

- **命令定义**: wf_11_commit.md
- **一致性策略**: command_consistency_strategy.md
- **代码实现指南**: wf_05_code_workflows.md
- **代码审查指南**: wf_08_review_workflows.md
- **项目管理**: CONTEXT.md, TASK.md, PLANNING.md