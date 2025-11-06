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
| 99 | `/wf_99_help` | 帮助系统 | [wf_99_help.md](wf_99_help.md) |

---

## 基础设施阶段

### /wf_01_planning - 项目规划

**用途**: 创建或更新PLANNING.md，建立项目架构和开发标准

**使用**:
```bash
/wf_01_planning "项目名称"
```

**读取**: PRD.md, 现有PLANNING.md, 项目代码结构
**写入**: PLANNING.md
**后续**: /wf_02_task

**关键功能**:
- 从PRD.md提取需求
- 定义系统架构
- 确立技术栈
- 制定开发标准
- 创建测试策略

---

### /wf_02_task - 任务管理

**用途**: 管理TASK.md任务追踪，维护项目进度

**使用**:
```bash
/wf_02_task create   # 创建任务列表
/wf_02_task update   # 更新任务状态
/wf_02_task review   # 审查进度
```

**读取**: PLANNING.md (create), TASK.md (update/review)
**写入**: TASK.md
**后续**: /wf_03_prime, /wf_05_code

**关键功能**:
- 从PLANNING.md生成任务
- 追踪任务状态
- 识别阻塞问题
- 计算完成度

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

**用途**: 获取技术架构建议和代码审查

**使用**:
```bash
/wf_04_ask "如何实现XX功能？"
/wf_04_ask "性能优化建议" --review-codebase  # 包含代码库审查
```

**读取**: PLANNING.md, TASK.md, KNOWLEDGE.md, 代码库(--review-codebase)
**写入**: PLANNING.md(可能), KNOWLEDGE.md(可能), TASK.md(可能)
**后续**: /wf_05_code, /wf_01_planning

**关键功能**:
- 提供架构指导
- 评估技术选型
- 识别风险
- 代码库深度分析 (--review-codebase)

---

### /wf_05_code - 代码实现

**用途**: 多智能体协调开发，自动格式化

**使用**:
```bash
/wf_05_code "实现用户认证功能"
```

**读取**: PLANNING.md(开发标准), TASK.md(当前任务), KNOWLEDGE.md(代码模式)
**写入**: 代码文件, TASK.md(状态更新)
**后续**: /wf_07_test, /wf_08_review, /wf_11_commit

**关键功能**:
- 遵循PLANNING.md标准
- 满足PRD需求
- 自动代码格式化
- 更新任务进度

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
**后续**: /wf_07_test, /wf_09_refactor, /wf_11_commit

**关键功能**:
- 根本原因分析
- 利用KNOWLEDGE.md已知解决方案
- 系统化调试流程
- 记录新问题模式

---

## 质量保证阶段

### /wf_07_test - 测试开发

**用途**: 创建和执行测试，集成覆盖率分析

**使用**:
```bash
/wf_07_test "认证模块"
/wf_07_test "API endpoints" --coverage  # 覆盖率分析
```

**读取**: PLANNING.md(测试策略), TASK.md(测试任务), 代码文件
**写入**: 测试文件, TASK.md(测试状态), 覆盖率报告
**后续**: /wf_08_review, /wf_09_refactor, /wf_11_commit

**关键功能**:
- 单元测试和集成测试
- 覆盖率分析 (--coverage)
- PRD标准验证
- 测试报告生成

---

### /wf_08_review - 代码审查

**用途**: 代码质量审查，PRD合规性检查

**使用**:
```bash
/wf_08_review
/wf_08_review "src/auth"  # 指定范围
```

**读取**: PLANNING.md(质量标准), KNOWLEDGE.md(代码模式), 代码文件
**写入**: TASK.md(改进任务), KNOWLEDGE.md(新模式)
**后续**: /wf_09_refactor, /wf_11_commit

**关键功能**:
- 质量标准验证
- PRD合规性检查
- 识别可重用模式
- 生成改进任务

---

### /wf_09_refactor - 代码重构

**用途**: 代码结构改进，保持PRD合规

**使用**:
```bash
/wf_09_refactor "用户服务"
```

**读取**: PLANNING.md(架构设计), TASK.md(技术债), KNOWLEDGE.md(代码模式)
**写入**: 代码文件, TASK.md(重构完成), PLANNING.md(可能)
**后续**: /wf_07_test, /wf_08_review, /wf_11_commit

**关键功能**:
- 对齐PLANNING.md架构
- 应用KNOWLEDGE.md最佳实践
- 保持功能不变
- 清理技术债

---

### /wf_10_optimize - 性能优化

**用途**: 性能调优，满足PRD性能要求

**使用**:
```bash
/wf_10_optimize "API响应时间"
```

**读取**: PLANNING.md(性能目标), TASK.md(优化任务), 代码文件
**写入**: 代码文件, TASK.md(优化完成), 性能报告
**后续**: /wf_09_refactor, /wf_07_test, /wf_11_commit

**关键功能**:
- 性能分析
- 瓶颈识别
- 优化实施
- 性能报告

---

## 文档维护阶段 (NEW)

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

## 运维部署阶段

### /wf_11_commit - 代码提交

**用途**: Git提交，自动格式化，更新CONTEXT.md

**使用**:
```bash
/wf_11_commit
/wf_11_commit "feat: 添加用户认证"
```

**读取**: PLANNING.md(标准), TASK.md(任务), 代码更改
**写入**: CONTEXT.md, TASK.md, KNOWLEDGE.md(可能), README.md(可能), Git提交
**后续**: /wf_02_task, /clear, /wf_03_prime

**关键功能**:
- 自动代码格式化
- Pre-commit质量门控
- 自动更新CONTEXT.md
- README.md智能更新
- KNOWLEDGE.md提取

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
/wf_03_prime → /wf_04_ask → /wf_05_code → /wf_07_test → /wf_08_review → /wf_11_commit

Bug修复:
/wf_06_debug → /wf_07_test → /wf_11_commit

代码改进:
/wf_08_review → /wf_09_refactor → /wf_07_test → /wf_11_commit
```

---

**最后更新**: 2025-11-06
**版本**: v3.2 (整合 Ultrathink 设计哲学)
