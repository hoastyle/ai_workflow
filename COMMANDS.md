# 命令完整参考

> 📖 13个工作流命令的详细参考手册

---

## 📑 目录

- [命令索引](#命令索引)
- [基础设施阶段 (1-3)](#基础设施阶段)
- [开发实现阶段 (4-6)](#开发实现阶段)
- [质量保证阶段 (7-10)](#质量保证阶段)
- [运维部署阶段 (11-12)](#运维部署阶段)
- [支持命令 (99)](#支持命令)

---

## 命令索引

| 索引 | 命令 | 说明 | 文档 |
|:----:|------|------|------|
| 01 | `/wf_01_planning` | 创建/更新项目规划 | [wf_01_planning.md](wf_01_planning.md) |
| 02 | `/wf_02_task` | 管理任务追踪 | [wf_02_task.md](wf_02_task.md) |
| 03 | `/wf_03_prime` | 加载项目上下文 | [wf_03_prime.md](wf_03_prime.md) |
| 04 | `/wf_04_ask` | 架构咨询 | [wf_04_ask.md](wf_04_ask.md) |
| 05 | `/wf_05_code` | 功能实现 | [wf_05_code.md](wf_05_code.md) |
| 06 | `/wf_06_debug` | 调试修复 | [wf_06_debug.md](wf_06_debug.md) |
| 07 | `/wf_07_test` | 测试开发 | [wf_07_test.md](wf_07_test.md) |
| 08 | `/wf_08_review` | 代码审查 | [wf_08_review.md](wf_08_review.md) |
| 09 | `/wf_09_refactor` | 代码重构 | [wf_09_refactor.md](wf_09_refactor.md) |
| 10 | `/wf_10_optimize` | 性能优化 | [wf_10_optimize.md](wf_10_optimize.md) |
| 11 | `/wf_11_commit` | 提交代码 | [wf_11_commit.md](wf_11_commit.md) |
| 12 | `/wf_12_deploy_check` | 部署检查 | [wf_12_deploy_check.md](wf_12_deploy_check.md) |
| 13 | `/wf_13_doc_maintain` | 文档维护 | [wf_13_doc_maintain.md](wf_13_doc_maintain.md) |
| 14 | `/wf_14_doc` | 智能文档生成 | [wf_14_doc.md](wf_14_doc.md) |
| 99 | `/wf_99_help` | 帮助系统 | [wf_99_help.md](wf_99_help.md) |

---

## 基础设施阶段

### /wf_01_planning - 项目规划

**用途**: 创建或更新PLANNING.md，建立项目架构和开发标准（仅处理项目级设计）

**使用**:
```bash
/wf_01_planning "项目名称"
```

**读取**: PRD.md, 现有PLANNING.md, 项目代码结构
**写入**: PLANNING.md
**后续**: /wf_02_task create (创建初始任务列表) 或 /wf_03_prime (如已有任务)

**使用场景** ✅:
- 全新项目启动时 (必须先执行)
- 架构重大调整时 (如技术栈变更)
- 开发标准更新时 (新的编码规范)

**不适用场景** ❌:
- 日常任务管理 → 用 `/wf_02_task`
- 功能完成后状态更新 → 用 `/wf_02_task update`
- 简单任务追踪 → 用 `/wf_02_task quick` 或 `/wf_02_task update`

**关键功能**:
- 从PRD.md提取需求
- 定义系统架构
- 确立技术栈
- 制定开发标准
- 创建测试策略
- 初始化KNOWLEDGE.md文档索引

**完成后提示**:
```
✅ PLANNING.md 已创建/更新

📋 下一步操作:
  1️⃣ 新项目？→ /wf_02_task create     (从PLANNING.md生成初始任务列表)
  2️⃣ 已有任务？→ /wf_03_prime         (加载项目上下文，开始工作)

💡 提示:
  - PLANNING.md 是项目架构的权威文档，仅在重大决策时更新
  - TASK.md 由 /wf_02_task 管理，负责日常任务追踪
  - 关于文档索引，见 KNOWLEDGE.md
```

---

### /wf_02_task - 任务管理

**用途**: 管理TASK.md任务追踪，维护项目进度（支持创建、更新、快速操作三种模式）

**使用**:
```bash
/wf_02_task create              # 从PLANNING.md生成初始任务列表 (需PLANNING.md)
/wf_02_task update              # 更新现有任务状态、添加新任务 (独立运行)
/wf_02_task quick "描述"         # 快速创建临时任务 (无依赖)
/wf_02_task review              # 审查进度和识别阻塞 (独立运行)
```

**读取**: PLANNING.md (create模式) 或 TASK.md (update/review/quick模式)
**写入**: TASK.md
**后续**: /wf_03_prime (开始工作) 或 /wf_05_code (实现任务)

**三种模式详解**:

1️⃣ **create** - 初始化任务 (仅在项目启动时使用)
   - 前置: `/wf_01_planning` 已完成
   - 作用: 从PLANNING.md分解出具体任务
   - 后续: `/wf_03_prime` (加载上下文)

2️⃣ **update** - 日常任务管理 (最常用，可独立运行)
   - 前置: 无 (可随时运行)
   - 作用: 更新任务状态、添加新发现的任务、调整优先级
   - 后续: `/wf_05_code` 或 `/wf_06_debug` (执行任务)

3️⃣ **quick** - 快速创建临时任务 (简单一次性工作)
   - 前置: 无
   - 作用: 快速记录临时任务（如：合并commit、更新配置、小修复）
   - 后续: 直接执行操作，执行后自动标记完成

4️⃣ **review** - 进度审查 (定期运行，如周末或冲刺结束)
   - 前置: 无
   - 作用: 分析进度、识别风险、生成报告
   - 后续: `/wf_01_planning` 更新 (如需调整策略)

**使用场景** ✅:
- 任何时候都可以用 `/wf_02_task update` (不需要PLANNING.md)
- 快速任务 → `/wf_02_task quick` (无任何依赖)
- 初始化任务 → `/wf_02_task create` (仅在项目启动后)

**关键功能**:
- 从PLANNING.md生成初始任务列表 (create)
- 实时更新任务状态 (update)
- 快速创建临时任务 (quick)
- 追踪任务依赖和阻塞
- 计算完成度和进度指标
- 识别关键路径

**完成后提示**:
```
✅ TASK.md 已更新

📋 下一步操作:
  1️⃣ 开始开发？→ /wf_03_prime          (加载项目上下文)
  2️⃣ 实现具体任务？→ /wf_05_code "任务描述"
  3️⃣ 修复问题？→ /wf_06_debug "问题描述"

💡 提示:
  - 任务完成后，用 /wf_02_task update 更新状态
  - 临时任务用 /wf_02_task quick "描述" (自动记录)
  - 定期用 /wf_02_task review 审查进度
```

---

### /wf_03_prime - 上下文加载 ⭐

**用途**: 加载项目完整上下文到AI工作记忆（智能按需加载）

**使用**:
```bash
/wf_03_prime
```

**读取**: PRD.md, PLANNING.md, TASK.md, CONTEXT.md, KNOWLEDGE.md + 智能加载技术文档
**写入**: 无（仅加载到内存）
**后续**: /wf_05_code, /wf_04_ask, /wf_02_task

**关键功能**:
- 自动加载5个管理层文档
- 从KNOWLEDGE.md解析文档索引（NEW）
- 根据任务相关性智能加载技术文档（NEW）
- 恢复会话上下文
- 准备工作环境

**智能加载策略**（NEW）:
- 优先级=高 且 任务相关 → 立即加载
- 优先级=中 且 任务相关 → 按需加载
- 其他文档 → 仅记录可用性

**💡 最佳实践**: 每次会话开始必须运行，通过文档索引优化上下文成本

---

## 开发实现阶段

### /wf_04_ask - 架构咨询

**用途**: 获取技术架构建议和代码库深度分析

**使用**:
```bash
/wf_04_ask "如何实现XX功能？"
/wf_04_ask "性能优化建议" --review-codebase  # 包含代码库深度分析
```

**读取**: PLANNING.md, TASK.md, KNOWLEDGE.md, 代码库(--review-codebase)
**写入**: PLANNING.md(可能), KNOWLEDGE.md(可能), TASK.md(可能)
**后续**: 根据咨询结果，可能是 /wf_05_code, /wf_09_refactor, /wf_01_planning, 或 /wf_02_task

**关键功能**:
- 提供架构指导和技术方案
- 评估技术选型的权衡
- 识别系统风险和瓶颈
- 代码库深度分析 (--review-codebase)
- 自动记录重要决策到PLANNING.md
- 生成可执行的改进任务到TASK.md

**咨询类型和后续操作**:

1️⃣ **功能实现咨询** (如："如何实现XX功能？")
   - 输出: 实现方案、技术选择、代码示例
   - 后续: `/wf_05_code "实现方案描述"` (开始编码)

2️⃣ **架构决策咨询** (如："应该用A还是B技术栈？")
   - 输出: 对比分析、权衡说明、推荐选择
   - 记录: 自动更新PLANNING.md的架构决策
   - 后续: `/wf_01_planning` 更新规划 (如涉及全局影响)

3️⃣ **性能/优化咨询** (如："如何优化数据库查询？")
   - 输出: 性能分析、优化方案、预期收益
   - 后续: `/wf_10_optimize "优化目标描述"` (执行优化)
          或 `/wf_02_task quick "性能优化任务"` (记录任务)

4️⃣ **代码库深度分析** (使用 --review-codebase)
   - 输出: 代码质量报告、改进建议、风险识别、任务列表
   - 记录: 自动生成改进任务到TASK.md
   - 后续: 逐个处理生成的任务
            - 简单修复 → `/wf_06_debug`
            - 重构优化 → `/wf_09_refactor`
            - 功能完善 → `/wf_05_code`

**完成后提示** (示例):
```
✅ 架构咨询完成

📊 咨询结果已生成:
  - 📋 方案分析: [方案对比]
  - 📝 推荐: [选择理由]
  - ⚠️  风险: [需要注意的问题]

📋 下一步操作:

  如果是功能实现:
    → /wf_05_code "按照上述方案实现XX功能"

  如果是架构决策:
    → /wf_01_planning "更新项目规划以反映新决策"

  如果涉及代码审查 (--review-codebase):
    → /wf_02_task update "添加生成的改进任务"
    → 逐个执行: /wf_09_refactor, /wf_06_debug, /wf_05_code

  如果是性能优化:
    → /wf_10_optimize "按照方案执行优化"

💡 提示:
  - 重要的架构决策已记录到PLANNING.md
  - 可执行的任务已添加到TASK.md
  - 新的模式和解决方案已添加到KNOWLEDGE.md
```

---

### /wf_05_code - 代码实现

**用途**: 多智能体协调开发，自动格式化，遵循架构标准

**使用**:
```bash
/wf_05_code "实现用户认证功能"
/wf_05_code "按照方案修复性能问题"  # 基于 /wf_04_ask 的建议
```

**读取**: PLANNING.md(开发标准), TASK.md(当前任务), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(设计参考)
**写入**: 代码文件, TASK.md(状态更新)
**后续**: /wf_07_test (编写测试) → /wf_08_review (代码审查) → /wf_11_commit (提交)

**关键功能**:
- 遵循PLANNING.md开发标准
- 满足PRD需求
- 自动代码格式化和优化
- 更新TASK.md任务进度
- Ultrathink优雅实现（函数名清晰、抽象自然、错误处理优雅）

**完成后提示**:
```
✅ 代码实现完成

📊 实现成果:
  - ✅ 代码已编写并格式化
  - ✅ TASK.md 已更新进度
  - 📝 实现细节: [主要改动说明]

📋 下一步操作:

  推荐流程 (标准工作流):
    1️⃣ /wf_07_test "编写测试"           (编写单元测试，验证功能)
    2️⃣ /wf_08_review                   (代码审查，检查质量)
    3️⃣ [可选] /wf_09_refactor "重构"    (如审查发现需要改进)
    4️⃣ /wf_11_commit "提交消息"         (提交代码)

  快速路径 (简单改动):
    → /wf_11_commit "完成XX功能"        (代码测试后直接提交)

💡 提示:
  - 建议按标准流程执行，确保代码质量
  - 完整的测试覆盖可避免后期问题
  - 代码审查可发现潜在的改进空间
```

---

### /wf_06_debug - 调试修复

**用途**: 系统化调试和根本原因修复

**使用**:
```bash
/wf_06_debug "用户登录500错误"
/wf_06_debug "性能慢" --quick  # 快速修复模式
```

**读取**: PLANNING.md(系统设计), TASK.md(相关任务), KNOWLEDGE.md(已知问题)
**写入**: 代码文件, TASK.md(修复记录), KNOWLEDGE.md(新解决方案)
**后续**: /wf_07_test (验证修复) → /wf_11_commit (提交)

**关键功能**:
- 根本原因分析
- 利用KNOWLEDGE.md已知解决方案
- 系统化调试流程
- 记录新问题模式和解决方案

**完成后提示**:
```
✅ 调试完成

📊 修复成果:
  - 🎯 问题根本原因: [原因分析]
  - ✅ 修复方案已实施
  - 📝 修复代码: [主要改动]

📋 下一步操作:

  推荐流程 (确保修复有效):
    1️⃣ /wf_07_test "验证修复"        (编写或运行测试确认bug已修复)
    2️⃣ /wf_08_review                 (代码审查修复方案)
    3️⃣ /wf_11_commit "bug修复完成"   (提交修复)

  快速路径 (简单bug):
    → /wf_11_commit "fix: 修复XX问题"  (代码已验证，直接提交)

💡 提示:
  - 新发现的问题模式已记录到KNOWLEDGE.md
  - 相似问题的解决方案已保存，便于后续参考
  - 修复记录已添加到TASK.md
  - 建议通过测试验证修复有效性
```

---

## 质量保证阶段

### /wf_07_test - 测试开发

**用途**: 创建和执行测试，集成覆盖率分析，验证PRD需求

**使用**:
```bash
/wf_07_test "认证模块"
/wf_07_test "API endpoints" --coverage  # 覆盖率分析
/wf_07_test --coverage                  # 全项目覆盖率检查
```

**读取**: PLANNING.md(测试策略), TASK.md(测试任务), KNOWLEDGE.md(测试模式), 代码文件
**写入**: 测试文件, TASK.md(测试状态), 覆盖率报告
**后续**: /wf_08_review (代码审查) 或 /wf_11_commit (如无审查需要)

**关键功能**:
- 单元测试和集成测试
- 覆盖率分析和报告 (--coverage)
- PRD需求验证
- 测试报告生成
- 识别可复用的测试模式

**完成后提示**:
```
✅ 测试完成

📊 测试成果:
  - ✅ 测试已编写并执行
  - 📊 覆盖率: X% (目标: >90%)
  - ✅ 所有测试通过

📋 下一步操作:

  如果测试覆盖率达标:
    1️⃣ /wf_08_review            (代码审查)
    2️⃣ /wf_11_commit "测试完成"  (提交)

  如果需要改进测试:
    → /wf_07_test "补充测试"     (增加测试覆盖)

  如果发现代码问题:
    → /wf_09_refactor "改进设计"  (重构改进)

💡 提示:
  - 覆盖率应该 > 90%
  - 关键路径的测试最重要
  - 边界条件的测试容易遗漏
```

---

### /wf_08_review - 代码审查

**用途**: 代码质量审查，PRD合规性检查，Ultrathink设计优雅度评审

**使用**:
```bash
/wf_08_review                    # 审查全部代码
/wf_08_review "src/auth"        # 审查特定模块
/wf_08_review --quick           # 快速审查模式
```

**读取**: PLANNING.md(质量标准), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(设计参考), 代码文件
**写入**: TASK.md(改进任务), KNOWLEDGE.md(新模式)
**后续**: /wf_09_refactor (需要改进) 或 /wf_11_commit (质量合格)

**关键功能**:
- 质量标准验证
- PRD合规性检查
- Ultrathink设计优雅度评审（代码结构、命名质量、必然性、权衡认知）
- 识别可重用模式和最佳实践
- 生成改进任务
- 识别架构决策

**审查维度**:
- 📐 **代码质量**: 风格、命名、结构
- ✨ **设计优雅度**: 函数职责、抽象清晰度、错误处理
- 🎯 **必然性**: 有无不必要的复杂性
- ⚖️ **权衡**: 性能/可读性权衡是否合理
- 🛡️ **安全性**: 安全漏洞、校验完整性
- ⚡ **性能**: 效率目标达成情况

**完成后提示** (示例):
```
✅ 代码审查完成

📊 审查结果:
  - 📈 质量评分: X/5
  - ✅ PRD合规: 是
  - ⚠️  发现问题: Y 个

📋 审查发现:

  🔴 必须修复 (阻塞提交):
    1. [问题描述]
    2. [问题描述]

  🟡 建议改进 (可选):
    1. [改进建议]
    2. [改进建议]

  ✨ 发现的优雅模式 (添加到KNOWLEDGE.md):
    - [可复用模式]

📋 下一步操作:

  如果有必须修复的问题:
    1️⃣ /wf_09_refactor "修复审查发现的问题"
    2️⃣ /wf_07_test --coverage              (回归测试)
    3️⃣ /wf_08_review                       (二次审查)
    4️⃣ /wf_11_commit "代码审查完成"

  如果没有问题，质量达标:
    → /wf_11_commit "代码已审查，质量合格"

  如果只有建议，可继续:
    → /wf_11_commit "功能完成，待优化"     (优化可留待后续)

💡 提示:
  - 必须修复的问题会阻止提交
  - 建议改进可以先记录到TASK.md，后续优化
  - 新发现的模式已记录到KNOWLEDGE.md供后续参考
```

---

### /wf_09_refactor - 代码重构

**用途**: 代码结构改进，保持功能不变，提升设计优雅度

**使用**:
```bash
/wf_09_refactor "用户服务模块"
/wf_09_refactor "简化业务逻辑"    # 基于 /wf_08_review 建议
```

**读取**: PLANNING.md(架构设计), TASK.md(技术债), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(设计参考)
**写入**: 代码文件, TASK.md(重构完成)
**后续**: /wf_07_test (回归测试) → /wf_08_review (二次审查) → /wf_11_commit (提交)

**关键功能**:
- 对齐PLANNING.md架构
- 应用KNOWLEDGE.md最佳实践
- 保持功能不变（100%回归测试）
- 清理技术债和代码坏味道
- 提升设计优雅度（Craft, Don't Code）

**完成后提示**:
```
✅ 代码重构完成

📊 重构成果:
  - ✅ 代码结构改进
  - ✅ 功能保持不变（需验证）
  - ✅ 可读性提升

📋 下一步操作:

  重要: 必须进行回归测试，确保功能未破坏
    1️⃣ /wf_07_test --coverage            (运行完整测试)
    2️⃣ /wf_08_review                     (二次代码审查)
    3️⃣ /wf_11_commit "重构完成"           (提交)

💡 提示:
  - 重构后必须通过所有测试
  - 测试覆盖率应保持 > 90%
  - 发现的改进建议已记录到TASK.md
```

---

### /wf_10_optimize - 性能优化

**用途**: 性能分析和调优，满足PRD性能目标

**使用**:
```bash
/wf_10_optimize "API响应时间"
/wf_10_optimize "数据库查询性能"   # 基于 /wf_04_ask 建议
```

**读取**: PLANNING.md(性能目标), TASK.md(优化任务), KNOWLEDGE.md(优化模式), 代码文件
**写入**: 代码文件, TASK.md(优化完成), 性能报告
**后续**: /wf_07_test (性能测试) → /wf_08_review (代码审查) → /wf_11_commit (提交)

**关键功能**:
- 性能分析和瓶颈识别
- 优化方案设计和实施
- 性能基准对比
- 性能报告生成
- 记录性能优化决策

**完成后提示**:
```
✅ 性能优化完成

📊 优化成果:
  - 📈 性能提升: X%
  - ✅ 目标达成: [是/否]
  - 📝 优化详情: [主要优化项]

📋 下一步操作:

  1️⃣ /wf_07_test --coverage            (性能测试和回归)
  2️⃣ /wf_08_review                     (代码审查)
  3️⃣ /wf_11_commit "性能优化完成"      (提交)

💡 提示:
  - 关键性能指标已达成目标
  - 优化决策已记录到PLANNING.md
  - 可复用的优化模式已添加到KNOWLEDGE.md
```

---

## 文档管理阶段

### /wf_13_doc_maintain - 文档维护

**用途**: 维护项目文档结构，确保文档层次清晰、上下文成本可控

**使用**:
```bash
/wf_13_doc_maintain           # 交互模式（生成报告+确认）
/wf_13_doc_maintain --auto    # 自动执行安全修复
/wf_13_doc_maintain --dry-run # 预览模式（不做修改）
```

**读取**: PLANNING.md, KNOWLEDGE.md, docs/, TASK.md
**写入**: KNOWLEDGE.md(索引更新), docs/archive/, 维护报告
**后续**: /wf_03_prime (重新加载优化后的上下文)

**关键功能**:
- 结构审查（四层架构合规性）
- 内容分析（过期、重复、孤立文档）
- 索引验证（KNOWLEDGE.md准确性）
- 优化建议（上下文成本减少）
- 归档执行（移动过期文档）

**执行时机**:
- 每10次提交后
- 季度末（Q1/Q2/Q3/Q4）
- 文档混乱时

**💡 最佳实践**: 定期运行确保管理层 < 100KB

---

### /wf_14_doc - 智能文档生成 ⭐ NEW

**用途**: 从代码库提取信息生成和更新项目文档（提取而非编造）

**使用**:
```bash
/wf_14_doc                  # 交互式（分析+选择+生成）
/wf_14_doc --update api     # 增量更新API文档
/wf_14_doc --check          # 只检查不生成（CI/CD）
/wf_14_doc --auto           # 自动生成所有缺失文档
```

**读取**: 项目代码, PLANNING.md, KNOWLEDGE.md, 现有文档
**写入**: docs/, README.md, KNOWLEDGE.md(索引更新)
**后续**: /wf_13_doc_maintain, /wf_11_commit

**关键功能**:
- 代码库分析（技术栈、架构、API自动识别）
- 文档缺口检测（对比代码 vs 现有文档）
- 智能信息提取（从代码、配置、注释提取）
- 交互式文档生成（用户选择需要的类型）
- 增量更新支持（不是全量重写）
- 自动索引管理（更新KNOWLEDGE.md）

**支持的文档类型** (5个核心):
- 📚 项目概览 (README.md)
- 🔌 API 文档 (docs/api/)
- ⚙️ 开发指南 (docs/development/)
- 🚀 部署文档 (docs/deployment/)
- 🏗️ 架构设计 (docs/architecture/)

**执行时机**:
- 项目初始化时
- 完成新功能后
- 添加新API端点后
- 修改配置或环境变量后
- 重构架构后

**💡 核心理念**: "提取而非编造" - 文档从代码中提取真实信息，不是基于通用模板

---

## 运维部署阶段

### /wf_11_commit - 代码提交

**用途**: Git提交，自动格式化，更新CONTEXT.md和项目文档

**使用**:
```bash
/wf_11_commit                       # 交互式提交
/wf_11_commit "feat: 添加用户认证"  # 指定提交消息
/wf_11_commit --squash 3 "合并消息"  # 合并最后3个commit (NEW)
```

**读取**: PLANNING.md(标准), TASK.md(任务), KNOWLEDGE.md(决策), 代码更改
**写入**: CONTEXT.md(自动更新), TASK.md(更新任务完成), KNOWLEDGE.md(新决策), README.md(可能), Git提交
**后续**: /wf_02_task update (可选) 或 /clear + /wf_03_prime (开始新工作)

**关键功能**:
- 自动代码格式化（black, prettier, clang-format等）
- Pre-commit质量门控和自动修复
- 自动更新CONTEXT.md会话状态
- README.md智能更新（重要功能完成时）
- KNOWLEDGE.md决策和模式提取
- 合并commit功能 (--squash)
- 完整的Frontmatter元数据更新
- Git提交历史维护

**完成后提示**:
```
✅ 代码已提交

📊 提交成果:
  - ✅ 格式化完成 (black/prettier等)
  - ✅ 质量检查通过 (pre-commit)
  - ✅ CONTEXT.md 已更新
  - ✅ TASK.md 已更新任务状态
  - ✅ Git提交成功

📝 提交信息:
  [feat] 功能描述

  主要改动说明

📋 下一步操作:

  如果需要继续工作:
    1️⃣ /wf_02_task update "更新新任务"      (添加新发现的任务)
    2️⃣ /wf_04_ask "下一步架构问题"          (或咨询)
    3️⃣ /wf_05_code "下一个功能"             (继续开发)

  如果上下文过大，需要清理:
    1️⃣ /clear                              (清理上下文)
    2️⃣ /wf_03_prime                        (重新加载，无缝继续)

  如果完成工作，准备部署:
    → /wf_12_deploy_check "production"     (部署就绪检查)

  如果需要定期文档维护:
    → /wf_13_doc_maintain                  (每10次提交后运行一次)

💡 提示:
  - CONTEXT.md 已自动更新，会话状态已保存
  - 下次执行 /clear 后，用 /wf_03_prime 恢复工作状态
  - 完成一个逻辑功能就提交，保持提交粒度适当
  - 定期运行 /wf_13_doc_maintain 整理文档

📚 相关文档:
  - 会话状态: docs/management/CONTEXT.md
  - 任务追踪: docs/management/TASK.md
  - 架构规划: PLANNING.md
  - 知识库: KNOWLEDGE.md
```

**合并commit示例** (NEW):
```bash
# 合并最后3个commit为一个
/wf_11_commit --squash 3 "feat: 完整的功能实现"

# 结果:
#   - 最后3个commit合并为1个
#   - 新commit包含所有改动
#   - 提交消息为指定的内容
#   - CONTEXT.md自动更新
```

---

### /wf_12_deploy_check - 部署检查

**用途**: 部署就绪性验证，PRD标准验证

**使用**:
```bash
/wf_12_deploy_check "production"
/wf_12_deploy_check "staging"
```

**读取**: PLANNING.md(部署要求), TASK.md(任务完成度), 测试报告
**写入**: 部署报告, TASK.md(部署任务)
**后续**: 实际部署操作

**关键功能**:
- PRD需求验证
- 测试通过确认
- 安全检查
- Go/No-Go决策

---

## 支持命令

### /wf_99_help - 帮助系统

**用途**: 完整帮助系统，中文友好界面

**使用**:
```bash
/wf_99_help              # 主菜单
/wf_99_help quick        # 命令速查表
/wf_99_help guide        # 场景工作流指导
/wf_99_help wf_05_code   # 具体命令帮助
```

**读取**: 所有wf_*.md命令文件
**写入**: 无
**后续**: 用户选择的命令

**关键功能**:
- 快速参考
- 场景指导
- 命令详情
- 中文界面

---

## 📌 快速参考

### 记住这5件事

1. 🔄 会话开始时运行 `/wf_03_prime`
2. 💻 使用 `/wf_05_code` 实现功能
3. ✅ 提交前使用 `/wf_08_review`
4. 💾 完成后用 `/wf_11_commit` 保存
5. ❓ 不确定时运行 `/wf_99_help`

### 命令依赖关系图

```
项目启动:
/wf_01_planning → /wf_02_task → /wf_03_prime

功能开发:
/wf_03_prime → /wf_04_ask → /wf_05_code → /wf_07_test → /wf_08_review → /wf_14_doc → /wf_11_commit

Bug修复:
/wf_06_debug → /wf_07_test → /wf_11_commit

代码改进:
/wf_08_review → /wf_09_refactor → /wf_07_test → /wf_11_commit

文档生成:
/wf_05_code → /wf_08_review → /wf_14_doc → /wf_13_doc_maintain → /wf_11_commit
```

---

**最后更新**: 2025-11-07
**版本**: v3.3 (增加智能文档生成)
