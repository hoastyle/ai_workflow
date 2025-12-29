---
title: "Workflow Optimization Guide"
description: "Complete guide for using PM Agent patterns in ai_workflow framework"
type: "教程"
status: "完成"
priority: "高"
created_date: "2025-12-03"
last_updated: "2025-12-03"
related_documents:
  - "docs/templates/PROJECT_INDEX_TEMPLATE.md"
  - "docs/management/PLANNING.md"
  - "wf_03_prime.md"
  - "wf_04_ask.md"
  - "wf_05_code.md"
  - "wf_06_debug.md"
tags: ["optimization", "pm-agent", "token-efficiency", "workflow"]
---

# Workflow Optimization Guide

**目标**: 通过 PM Agent 模式优化 ai_workflow 框架，实现 **80% token 节省**和更高的工作流效率。

**适用对象**: 使用 ai_workflow 命令系统的所有项目

---

## 📊 优化成果总结

实施本指南的优化后，预期获得：

| 优化项 | 节省效果 | 实施难度 | ROI |
|--------|---------|---------|-----|
| **PROJECT_INDEX.md** | 80% (~8,000 tokens/session) | 简单 | 立即见效 |
| **Confidence Check** | 25-750x (阻止失败实现) | 中等 | 高回报 |
| **Token Budget** | 30-50% (高效agent协调) | 简单 | 持续优化 |
| **Smart Context Loading** | 50-80% (按需加载) | 中等 | 渐进式 |

**总体效果**: 从 ~10,000 tokens/session → ~2,000 tokens/session (80% reduction)

---

## 🎯 核心优化策略

### Strategy 1: PROJECT_INDEX.md - 轻量级项目入口

**问题**: 传统 /wf_03_prime 加载 5 个完整管理文档 (~10,000 tokens)

**解决方案**: 创建 PROJECT_INDEX.md 作为项目概览 (~2,000 tokens)

#### 实施步骤

**Step 1: 创建 PROJECT_INDEX.md**

使用模板创建项目索引：
```bash
# 方法 1: 使用模板手动创建
cp docs/templates/PROJECT_INDEX_TEMPLATE.md PROJECT_INDEX.md
# 编辑 PROJECT_INDEX.md，替换所有 [placeholder] 内容

# 方法 2: 使用 wf_14_doc 自动生成（推荐）
/wf_14_doc --generate-index
```

**Step 2: 验证token节省**

```bash
# 测试传统完整加载
/wf_03_prime --full
# 观察输出: "Loaded 5 management documents (~10,000 tokens)"

# 测试新的轻量级加载
/wf_03_prime
# 观察输出: "Loaded PROJECT_INDEX.md (~2,000 tokens)"
```

**Step 3: 渐进式深化**

只在需要详细信息时才加载完整文档：
```bash
# 快速启动 (默认)
/wf_03_prime                   # ~2,000 tokens

# 任务聚焦模式
/wf_03_prime --task            # ~3,000 tokens (INDEX + active task details)

# 完整上下文
/wf_03_prime --full            # ~10,000 tokens (所有5个文档)
```

#### 内容指南

**PROJECT_INDEX.md 应该包含** (✅):
- 项目结构树状图 (~50 行)
- 核心模块简要说明 (~30 行/模块)
- 入口点和关键文件位置 (~20 行)
- 快速开始命令 (~10 行)
- 文档索引 (指针而非内容)

**不应包含** (❌):
- 完整的API文档细节
- 代码示例全文
- 详细的架构设计文档
- 历史决策记录全文
- 任务列表详情

#### 维护策略

**何时更新 PROJECT_INDEX.md**:
- ✅ 新增核心模块或重要文件
- ✅ 项目结构发生重大变化
- ✅ 关键依赖版本更新
- ❌ 不需要在每次 commit 后更新

**自动化维护**:
```bash
# 定期重新生成索引 (建议每月或重大变更后)
/wf_14_doc --generate-index --update

# 验证索引完整性
/wf_14_doc --validate-index
```

---

### Strategy 2: Confidence Check - 预执行评估门控

**问题**: AI 在信心不足时仍然执行任务，导致失败实现浪费大量 token

**解决方案**: 在 3 个关键命令中添加 Confidence Check 机制

#### 已集成的命令

1. **wf_04_ask.md** - 架构咨询
2. **wf_05_code.md** - 代码实现
3. **wf_06_debug.md** - 调试修复

#### 工作原理

**5 维度评估** (命令特定):

每个命令根据其职责定义 5 个评估维度，例如：

**wf_05_code.md** (代码实现):
1. **需求清晰度** - 功能描述是否明确？
2. **技术可行性** - 有成熟方案支持吗？
3. **架构对齐** - 符合 PLANNING.md 吗？
4. **代码理解** - 理解现有代码库吗？
5. **测试可验证性** - 可以编写测试验证吗？

**决策树**:
```
Base confidence: 50%

评估 5 个维度 → 调整信心值
├─ ≥90% → 直接执行 (高信心)
├─ 70-89% → 提供替代方案，询问用户确认
└─ <70% → 暂停执行，请求更多信息或明确指示
```

#### 使用示例

**场景 1: 高信心 (≥90%)** - 直接执行
```
用户: "使用React实现一个登录表单，包含用户名和密码输入框"

AI评估:
✅ 需求清晰度: +30% (明确的UI需求)
✅ 技术可行性: +25% (React是现有技术栈)
✅ 架构对齐: +20% (PLANNING.md 有前端标准)
✅ 代码理解: +15% (理解现有组件结构)
✅ 测试可验证性: +10% (可以编写单元测试)

总信心: 50% + 100% = 100% (实际上限95%)
→ 直接执行实现
```

**场景 2: 中等信心 (70-89%)** - 提供选项
```
用户: "优化数据库查询性能"

AI评估:
✅ 需求清晰度: +20% (目标明确但缺少具体场景)
⚠️ 技术可行性: +5% (需要先profile找瓶颈)
✅ 架构对齐: +20% (符合性能目标)
⚠️ 代码理解: +10% (需要详细分析查询模式)
✅ 测试可验证性: +15% (可以benchmark验证)

总信心: 50% + 70% = 70%
→ 提供选项: "我可以通过以下方式优化：
  A. 先运行性能分析，识别慢查询
  B. 基于你的经验，直接优化已知的慢查询
  C. 使用 /wf_04_ask 先咨询最佳优化策略

  你希望选择哪种方式？"
```

**场景 3: 低信心 (<70%)** - 暂停并请求信息
```
用户: "修复那个bug"

AI评估:
❌ 需求清晰度: -30% (哪个bug？)
❌ 技术可行性: -30% (没有错误信息)
⚠️ 架构对齐: 0% (无法判断)
❌ 代码理解: -20% (不知道涉及哪些代码)
❌ 测试可验证性: -10% (无法确定验证方法)

总信心: 50% - 90% = -40% (实际下限10%)
→ 暂停: "我需要更多信息才能修复bug：
  1. 请提供完整的错误信息或堆栈跟踪
  2. 这个bug出现在什么场景下？
  3. 预期行为是什么？
  4. 可以提供复现步骤吗？

  或者使用 /wf_06_debug '详细错误描述' 进行系统化调试"
```

#### ROI 分析

**成本**: 100-200 tokens (5维度评估 + 决策树判断)

**收益**: 阻止一次失败实现
- 低复杂度任务: ~5,000 tokens
- 中等复杂度: ~15,000 tokens
- 高复杂度: ~50,000 tokens

**ROI**: 25x - 250x token savings

**Break-even**: 阻止 1 次失败实现即可回本

---

### Strategy 3: Token Budget - 分级资源管理

**问题**: 所有命令使用相同的 token 分配，导致简单任务过度消耗，复杂任务资源不足

**解决方案**: 为每个命令配置 3 级 token budget

#### Token Budget 级别

| 级别 | Token 限制 | 适用场景 | 推荐模型 |
|------|----------|---------|---------|
| **simple** | 200 | CRUD操作、自动化更新、快速查询 | haiku |
| **medium** | 1,000 | 标准工作流、单一专家分析 | sonnet |
| **complex** | 2,500 | 多agent协调、深度研究 | sonnet |

#### 命令分级（15个命令）

**Simple Budget** (5个命令):
- wf_02_task - 任务CRUD操作
- wf_11_commit - 自动化提交更新
- wf_12_deploy_check - 部署检查清单
- wf_13_doc_maintain - 定期文档维护
- wf_99_help - 帮助查询

**Medium Budget** (8个命令):
- wf_03_prime - 智能上下文加载
- wf_04_ask - 架构咨询
- wf_06_debug - 系统化调试
- wf_07_test - 测试开发
- wf_08_review - 代码审查
- wf_09_refactor - 代码重构
- wf_10_optimize - 性能优化
- wf_14_doc - 文档生成

**Complex Budget** (2个命令):
- wf_01_planning - 综合架构规划
- wf_04_research - 深度方案研究
- wf_05_code - 多agent实现协调

#### 实施效果

**Before**: 所有命令统一使用 ~2,000 tokens
**After**: 根据需求分级使用 200/1,000/2,500 tokens

**效果计算**:
```
假设一个开发会话中:
- 5次 simple 操作 (wf_02_task, wf_11_commit, etc.)
- 8次 medium 操作 (wf_07_test, wf_08_review, etc.)
- 2次 complex 操作 (wf_05_code, wf_04_research)

Before:
  15 * 2,000 = 30,000 tokens

After:
  (5 * 200) + (8 * 1,000) + (2 * 2,500)
  = 1,000 + 8,000 + 5,000
  = 14,000 tokens

Savings: 53% (16,000 tokens)
```

---

### Strategy 4: Smart Context Loading - 按需加载

**问题**: wf_03_prime 总是加载所有 5 个管理文档，即使用户只需要快速查看当前任务

**解决方案**: 3 种智能加载模式

#### 3 种加载模式

**Mode 1: Quick Start** (~2,000 tokens)
```bash
/wf_03_prime            # 默认模式
```
- 加载: PROJECT_INDEX.md + CONTEXT.md
- 适用: 快速启动、查看项目概况、确定下一步行动
- Token: ~2,000

**Mode 2: Task Focused** (~3,000 tokens)
```bash
/wf_03_prime --task     # 或检测到 TASK.md 有 in_progress 任务
```
- 加载: PROJECT_INDEX.md + CONTEXT.md + Active Task Details
- 适用: 继续当前任务、需要任务上下文的操作
- Token: ~3,000

**Mode 3: Full Context** (~10,000 tokens)
```bash
/wf_03_prime --full     # 显式请求完整上下文
```
- 加载: All 5 documents (PRD, PLANNING, TASK, CONTEXT, KNOWLEDGE)
- 适用: 重大架构决策、深度代码审查、完整项目理解
- Token: ~10,000

#### 自动检测逻辑

wf_03_prime 会自动检测最佳模式：

```bash
# 检测 1: PROJECT_INDEX.md 存在吗？
if [ -f PROJECT_INDEX.md ]; then
  default_mode="quick_start"  # 使用轻量级模式
else
  default_mode="full_context"  # 传统完整模式
fi

# 检测 2: 有活跃任务吗？
if grep -q "status: in_progress" TASK.md; then
  suggest_mode="task_focused"  # 建议任务聚焦模式
fi

# 检测 3: 用户标志覆盖
if [ "$1" = "--full" ]; then
  mode="full_context"
elif [ "$1" = "--task" ]; then
  mode="task_focused"
fi
```

#### 渐进式深化策略

**会话初期** (信息收集):
```
/wf_03_prime                # Quick Start (~2,000 tokens)
→ 了解项目结构和当前状态
→ 确定需要的详细信息

如果需要任务细节:
/wf_03_prime --task         # Task Focused (~3,000 tokens)

如果需要完整架构:
/wf_03_prime --full         # Full Context (~10,000 tokens)
```

**Token 节省示例**:
```
场景: 用户想查看项目概况并决定下一步

传统方式:
  /wf_03_prime (总是加载全部)
  Token: 10,000

优化方式:
  /wf_03_prime (Quick Start)
  Token: 2,000

  [用户决定继续当前任务]
  → 不需要额外加载 (CONTEXT.md已包含指针)
  或
  /wf_03_prime --task (如果需要任务详情)
  Token: +1,000 (累计 3,000)

最终节省: 70-80% tokens
```

---

## 🛠️ 实施路线图

### Phase 1: 基础优化 (1-2小时)

**Step 1: 创建 PROJECT_INDEX.md**
```bash
# 使用模板
cp docs/templates/PROJECT_INDEX_TEMPLATE.md PROJECT_INDEX.md

# 编辑并填写项目信息
# 目标: ~2,000 tokens, ~300 行
```

**Step 2: 验证 Token Budget 配置**
```bash
# 检查所有命令都有 token_budget 字段
grep -r "token_budget:" wf_*.md

# 应该看到 15 个结果
```

**Step 3: 测试 Smart Loading**
```bash
# 测试 3 种模式
/wf_03_prime              # Quick Start
/wf_03_prime --task       # Task Focused
/wf_03_prime --full       # Full Context

# 观察 token 消耗差异
```

**预期效果**: 立即获得 80% token 节省

---

### Phase 2: 工作流集成 (1-2周)

**Week 1: 适应新流程**
- 使用 Quick Start 模式作为默认
- 只在必要时使用 --full
- 记录哪些场景需要完整上下文

**Week 2: 优化迭代**
- 根据使用模式调整 PROJECT_INDEX.md
- 识别经常需要的详细信息，考虑加入索引
- 移除不常用的索引内容

**预期效果**: 建立高效的工作流习惯

---

### Phase 3: 高级优化 (持续)

**定期维护** (每月):
```bash
# 更新 PROJECT_INDEX.md
/wf_14_doc --generate-index --update

# 检查文档架构健康度
/wf_13_doc_maintain
```

**性能监控**:
- 追踪平均每次会话的 token 消耗
- 识别 token 消耗异常的命令
- 调整 token budget 分配

**预期效果**: 持续优化，保持高效状态

---

## 📈 效果测量

### 关键指标

**KPI 1: Token 消耗**
```
Baseline (无优化):
  平均每会话: ~10,000 tokens (prime) + ~30,000 tokens (工作流)
  = 40,000 tokens/session

Target (完全优化):
  平均每会话: ~2,000 tokens (prime) + ~14,000 tokens (工作流)
  = 16,000 tokens/session

Reduction: 60% (24,000 tokens saved)
```

**KPI 2: 失败实现率**
```
Baseline (无 Confidence Check):
  失败率: ~20% (需要重做)
  浪费 token: 20% * 30,000 = 6,000 tokens/session

Target (有 Confidence Check):
  失败率: <5%
  浪费 token: 5% * 14,000 = 700 tokens/session

Reduction: 88% (5,300 tokens saved from failures)
```

**KPI 3: 会话启动效率**
```
Baseline:
  /wf_03_prime: ~10,000 tokens
  启动时间: ~30秒

Target:
  /wf_03_prime (Quick Start): ~2,000 tokens
  启动时间: ~6秒

Improvement: 5x faster, 80% fewer tokens
```

### 测量方法

**方法 1: 手动追踪**
```bash
# 在每次会话后记录
echo "Session $(date +%Y-%m-%d): prime_mode=quick, tokens_saved=8000" >> optimization_log.txt
```

**方法 2: 自动统计**
```bash
# 使用 wf_99_help 的统计功能 (如果有)
/wf_99_help --stats
```

---

## 🎓 最佳实践

### DO ✅

1. **总是从 Quick Start 开始**
   - 使用 `/wf_03_prime` (无参数) 作为默认
   - 80% 的场景下足够使用

2. **让 Confidence Check 工作**
   - 不要在低信心 (<70%) 时强制执行
   - 提供更多信息或使用建议的替代方案

3. **按需深化**
   - 只在需要时使用 `--task` 或 `--full`
   - 记录哪些操作真正需要完整上下文

4. **定期维护 PROJECT_INDEX**
   - 每月或重大变更后更新
   - 保持索引简洁和相关

5. **监控 token 消耗**
   - 追踪优化效果
   - 识别改进机会

### DON'T ❌

1. **不要盲目使用 --full**
   - 完整上下文只在必要时使用
   - 大多数操作不需要所有文档

2. **不要忽略 Confidence Check 警告**
   - 低信心继续执行 = 浪费 token
   - 先解决信心问题再执行

3. **不要让 PROJECT_INDEX 膨胀**
   - 目标: ~2,000 tokens
   - 超过 3,000 tokens 考虑精简

4. **不要跳过定期维护**
   - 过时的索引会误导 AI
   - 定期更新保持准确性

5. **不要为了省 token 牺牲质量**
   - 在需要时使用完整上下文
   - 优化是为了效率，不是极端节约

---

## 🔧 故障排查

### 问题 1: Confidence Check 总是低信心

**症状**: AI 频繁报告信心不足 (<70%)

**原因**:
- 项目文档不完整 (PLANNING.md, KNOWLEDGE.md 缺失)
- 需求描述过于模糊
- 缺少官方文档参考

**解决方案**:
```bash
# Step 1: 完善项目文档
/wf_01_planning              # 确保 PLANNING.md 完整
/wf_14_doc                   # 补充缺失的技术文档

# Step 2: 提供更详细的需求
不要: "修复bug"
改为: "修复登录表单验证失败的bug，错误信息: 'Invalid credentials'，
      复现步骤: 1) 打开登录页 2) 输入test@example.com 3) 点击登录"

# Step 3: 添加官方文档引用
/wf_04_research "React form validation" --c7
```

---

### 问题 2: PROJECT_INDEX 过大

**症状**: PROJECT_INDEX.md > 3,000 tokens

**原因**:
- 包含了太多实现细节
- 代码示例过多
- 历史信息未清理

**解决方案**:
```bash
# 使用精简原则
✅ 保留: 项目结构、模块概述、入口点、文档索引
❌ 删除: 完整代码示例、详细API文档、历史决策全文

# 重新生成精简版本
/wf_14_doc --generate-index --compact
```

---

### 问题 3: Smart Loading 不工作

**症状**: 总是加载完整上下文，即使使用 Quick Start

**原因**:
- PROJECT_INDEX.md 不存在
- wf_03_prime.md 未更新到最新版本

**解决方案**:
```bash
# 检查 PROJECT_INDEX.md
ls -lh PROJECT_INDEX.md

# 如果不存在，创建它
cp docs/templates/PROJECT_INDEX_TEMPLATE.md PROJECT_INDEX.md

# 验证 wf_03_prime.md 有 smart loading 逻辑
grep "context_loading: smart" wf_03_prime.md

# 如果没有，更新到最新版本
git pull origin master   # 或从 ai_workflow 框架更新
```

---

## 📚 参考资源

### 核心文档
- **PROJECT_INDEX_TEMPLATE.md** - 项目索引模板
- **wf_03_prime.md** - Smart Context Loading 实现
- **wf_04_ask.md** - Confidence Check 实现 (架构)
- **wf_05_code.md** - Confidence Check 实现 (代码)
- **wf_06_debug.md** - Confidence Check 实现 (调试)

### 外部参考
- **SuperClaude Framework**: PM Agent 模式原始实现
- **Context7**: 官方文档查询 MCP
- **Tavily**: Web 搜索和研究 MCP

---

## 🎯 下一步行动

完成本指南后，建议按以下顺序行动：

1. ✅ **立即**: 创建 PROJECT_INDEX.md (1小时)
2. ✅ **本周**: 适应 Smart Loading 模式 (1周)
3. ✅ **本月**: 监控并优化 token 消耗 (持续)
4. ✅ **季度**: 定期维护和更新文档架构 (每3个月)

**目标**: 在 1 个月内实现 60-80% token 节省，提升开发效率 2-3x

---

**版本**: 1.0
**最后更新**: 2025-12-03
**维护者**: ai_workflow 框架团队
