# 工作流场景指导

> 🔄 常见开发场景的命令组合和最佳实践

---

## 📑 目录

- [核心工作流](#核心工作流)
- [完整开发流程](#完整开发流程)
- [常见场景](#常见场景)
- [工作流决策树](#工作流决策树)
- [最佳实践](#最佳实践)

---

## 核心工作流

### 🆕 全新项目开始

```bash
# 1. 创建项目规划
/wf_01_planning "项目名称"

# 2. 生成任务列表
/wf_02_task create

# 3. 加载项目上下文
/wf_03_prime
```

**预计时间**: 15-30分钟
**输出**: PLANNING.md + TASK.md
**下一步**: 开始功能开发

---

### 📱 会话管理生命周期

```bash
# 会话开始
/wf_03_prime              # 加载所有项目上下文

# 进行工作
/wf_05_code "功能"        # 开发
/wf_07_test "模块"        # 测试
/wf_11_commit            # 提交

# 上下文过大时
/clear                   # 清理上下文
/wf_03_prime             # 重新加载，无缝继续
```

**关键点**:
- 始终以 `/wf_03_prime` 开始会话
- 定期用 `/wf_11_commit` 保存进度（自动更新CONTEXT.md）
- `/clear` 后必须运行 `/wf_03_prime` 恢复上下文

---

## 完整开发流程

### ✨ 功能开发（标准流程）

```bash
# 1. 架构咨询（可选）
/wf_04_ask "如何实现用户认证功能？"

# 2. 代码实现
/wf_05_code "实现JWT用户认证"

# 3. 编写测试
/wf_07_test "authentication module"

# 4. 代码审查
/wf_08_review

# 5. 生成/更新文档（NEW）
/wf_14_doc  # 交互式选择要生成的文档

# 6. 提交代码（自动格式化+上下文更新）
/wf_11_commit "feat: add JWT authentication"

# 7. 更新任务进度
/wf_02_task update
```

**预计时间**: 中等功能 30-60分钟
**关键检查点**:
- [ ] PLANNING.md标准遵守
- [ ] PRD需求满足
- [ ] 测试覆盖率达标
- [ ] 代码审查通过
- [ ] 文档已更新（NEW）

---

### 🐛 Bug修复（快速路径）

```bash
# 1. 系统化调试（标准）
/wf_06_debug "用户登录返回500错误"

# 或：快速修复（简单问题）
/wf_06_debug "按钮文字错误" --quick

# 2. 验证修复
/wf_07_test "login functionality"

# 3. 提交修复
/wf_11_commit "fix: resolve login 500 error"
```

**预计时间**:
- 简单Bug: 5-15分钟
- 复杂Bug: 30-90分钟

**调试技巧**:
- 使用 `/wf_06_debug` 的系统化分析
- 查阅 KNOWLEDGE.md 已知问题
- 记录新解决方案到 KNOWLEDGE.md

---

### 📊 代码质量改进

```bash
# 1. 质量分析
/wf_08_review

# 2. 代码重构
/wf_09_refactor "user service"

# 3. 性能优化
/wf_10_optimize "API response time"

# 4. 回归测试（确保无破坏）
/wf_07_test --coverage

# 5. 提交改进
/wf_11_commit "refactor: improve code quality"
```

**预计时间**: 45-120分钟
**关键原则**:
- 保持功能不变
- 测试先行
- 对齐PLANNING.md架构

---

### 📦 部署准备

```bash
# 1. 测试覆盖率检查
/wf_07_test --coverage

# 2. 最终代码审查
/wf_08_review

# 3. 部署就绪检查
/wf_12_deploy_check "production"

# 4. 实际部署（根据项目配置）
# 例如: npm run deploy, docker push, etc.
```

**部署清单**:
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] PRD需求验证
- [ ] 安全检查通过
- [ ] 性能指标达标

---

### 📚 文档维护流程 (NEW)

```bash
# 1. 定期执行（每10次提交或季度末）
/wf_13_doc_maintain

# 2. 查看维护报告
# - 结构合规性
# - 过期/重复/孤立文档
# - 索引准确性

# 3. 自动修复（可选）
/wf_13_doc_maintain --auto

# 4. 预览模式（不做修改）
/wf_13_doc_maintain --dry-run

# 5. 重新加载优化后的上下文
/wf_03_prime
```

**维护时机**:
- 每10次提交后
- 季度末（Q1/Q2/Q3/Q4）
- 发现文档混乱时
- 管理层文档 > 100KB时

**预计时间**: 5-15分钟

---

## 常见场景

### 场景1：添加新功能

**步骤**:
```
/wf_04_ask "技术方案咨询"
  ↓
/wf_05_code "功能实现"
  ↓
/wf_07_test "测试覆盖"
  ↓
/wf_08_review "质量检查"
  ↓
/wf_11_commit "提交保存"
```

### 场景2：修复紧急Bug

**快速路径**:
```
/wf_06_debug "错误描述" --quick
  ↓
/wf_07_test "验证修复"
  ↓
/wf_11_commit "紧急修复"
```

### 场景3：代码重构

**谨慎路径**:
```
/wf_08_review "识别问题"
  ↓
/wf_09_refactor "重构实施"
  ↓
/wf_07_test --coverage "回归测试"
  ↓
/wf_08_review "二次验证"
  ↓
/wf_11_commit "重构完成"
```

### 场景4：架构咨询后的深度代码审查

**深度分析路径**:
```
/wf_04_ask "架构问题" --review-codebase
  ↓
查看生成的TASK.md改进任务
  ↓
逐个处理高优先级任务:
  /wf_05_code / /wf_09_refactor
  ↓
/wf_07_test --coverage
  ↓
/wf_11_commit
```

### 场景5：智能文档生成 ⭐ NEW

**文档生成路径** (功能完成后):
```bash
# 完成功能开发
/wf_05_code "实现用户认证"
  ↓
/wf_08_review "代码审查"
  ↓
# 生成/更新文档
/wf_14_doc
  ↓
AI分析代码库并展示:
  - 📊 项目技术栈分析
  - 📋 文档缺口报告（3个新API端点缺文档）
  - 💡 建议生成的文档列表
  ↓
选择要生成的文档:
  [1] API 文档更新
  [2] 环境变量文档
  [3] README 更新
  ↓
AI从代码提取信息并生成文档
  ↓
审查生成的文档，完善细节
  ↓
/wf_13_doc_maintain  # 检查文档结构
  ↓
/wf_11_commit "docs: update API documentation"
```

**快速更新特定文档**:
```bash
# 只更新API文档
/wf_14_doc --update api

# 只检查不生成（CI/CD）
/wf_14_doc --check
```

**核心理念**: "提取而非编造" - 文档从代码中自动提取真实信息

---

### 场景6：文档维护和优化

**定期维护路径**:
```bash
/wf_13_doc_maintain
  ↓
审查维护报告:
  - 文档结构合规性
  - 过期文档识别
  - 重复内容检测
  - 索引准确性
  ↓
确认自动修复或手动处理
  ↓
/wf_03_prime  # 重新加载优化后的上下文
```
**详细流程**: 查看 [DOC_ARCHITECTURE.md](DOC_ARCHITECTURE.md#文档维护流程)

---

## 工作流决策树

### 我应该用哪个命令？

```
📍 当前状态？
│
├─ 🆕 全新开始
│  ├─ 新项目启动 → /wf_01_planning
│  └─ 新会话开始 → /wf_03_prime
│
├─ 💻 开发阶段
│  ├─ 不确定如何实现 → /wf_04_ask
│  ├─ 开始写代码 → /wf_05_code
│  ├─ 遇到Bug → /wf_06_debug
│  └─ 添加测试 → /wf_07_test
│
├─ 🔍 质量改进
│  ├─ 检查代码质量 → /wf_08_review
│  ├─ 需要重构 → /wf_09_refactor
│  └─ 性能问题 → /wf_10_optimize
│
├─ 💾 完成工作
│  ├─ 更新任务状态 → /wf_02_task update
│  ├─ 提交代码 → /wf_11_commit
│  └─ 准备部署 → /wf_12_deploy_check
│
└─ ❓ 需要帮助 → /wf_99_help
```

### 命令依赖关系

```
典型依赖链：

必须顺序：
/wf_01_planning → /wf_02_task → /wf_03_prime

推荐顺序：
/wf_05_code → /wf_07_test → /wf_08_review → /wf_11_commit

可选分支：
/wf_08_review → /wf_09_refactor → /wf_07_test (回归)
/wf_08_review → /wf_10_optimize → /wf_07_test (验证)
```

### 完整Workflow流程图

```mermaid
graph TD
    A["🆕 新项目<br/>/wf_01_planning"] --> B["📋 任务初始化<br/>/wf_02_task"]
    B --> C["📱 会话开始<br/>/wf_03_prime"]

    C --> D{开发任务?}
    D -->|不清楚架构| E["❓ 架构咨询<br/>/wf_04_ask"]
    E --> F["💻 实现功能<br/>/wf_05_code"]
    D -->|直接开发| F
    D -->|遇到Bug| G["🐛 调试修复<br/>/wf_06_debug"]

    F --> H["✅ 添加测试<br/>/wf_07_test"]
    G --> H
    H --> I["👀 代码审查<br/>/wf_08_review"]

    I --> J{需要改进?}
    J -->|代码重构| K["🔧 代码重构<br/>/wf_09_refactor"]
    J -->|性能问题| L["⚡ 性能优化<br/>/wf_10_optimize"]
    J -->|直接提交| M["💾 提交保存<br/>/wf_11_commit"]

    K --> H
    L --> H

    M --> N["🚀 准备部署<br/>/wf_12_deploy_check"]
    N --> O["📦 实际部署<br/>(外部操作)"]

    M --> P["🔄 清理上下文<br/>/clear"]
    P --> C

    style A fill:#e1f5ff
    style C fill:#fff3e0
    style F fill:#f3e5f5
    style H fill:#e8f5e9
    style I fill:#fce4ec
    style M fill:#fff9c4
    style N fill:#f1f8e9
```

### 常见场景的快速决策流

```mermaid
graph LR
    Start{我要做什么?}

    Start -->|新项目| P1["/wf_01_planning"]
    Start -->|启动会话| P2["/wf_03_prime"]
    Start -->|实现功能| P3["/wf_05_code → /wf_07_test<br/> → /wf_08_review → /wf_11_commit"]
    Start -->|修复Bug| P4["/wf_06_debug → /wf_07_test<br/> → /wf_11_commit"]
    Start -->|代码改进| P5["/wf_08_review → /wf_09_refactor<br/> → /wf_07_test"]
    Start -->|部署检查| P6["/wf_12_deploy_check"]
    Start -->|需要帮助| P7["/wf_99_help"]

    P1 --> End["✅ 开始工作"]
    P2 --> End
    P3 --> End
    P4 --> End
    P5 --> End
    P6 --> End
    P7 --> End

    style Start fill:#fff9c4
    style End fill:#c8e6c9
```

---

## 最佳实践

### 会话管理

✅ **永远先 `/wf_03_prime`**
- 每个新会话的第一个动作
- `/clear` 后立即运行
- 确保AI理解项目上下文
- 智能加载技术文档（NEW）

✅ **经常 `/wf_11_commit`**
- 完成一个逻辑功能就提交
- 自动更新CONTEXT.md
- 支持跨会话连续性

✅ **及时 `/wf_02_task update`**
- 完成任务后立即更新
- 保持进度可见
- 便于团队协作

✅ **定期 `/wf_13_doc_maintain`** (NEW)
- 每10次提交后运行
- 季度末执行维护
- 保持管理层 < 100KB
- 确保文档索引准确

---

### 开发质量

✅ **测试先行**
- 实现功能后立即 `/wf_07_test`
- 使用 `--coverage` 检查覆盖率
- 回归测试防止破坏

✅ **审查驱动**
- 提交前必须 `/wf_08_review`
- 识别问题早期修复
- 维护代码质量

✅ **架构咨询**
- 复杂功能先 `/wf_04_ask`
- 使用 `--review-codebase` 深度分析
- 记录决策到PLANNING.md

---

### 上下文优化

✅ **按需清理**
- Token接近上限时 `/clear`
- 清理后立即 `/wf_03_prime`
- CONTEXT.md保证连续性

✅ **文档维护** (ENHANCED)
- PLANNING.md：重大决策更新，核心概念保持简洁
- KNOWLEDGE.md：新模式记录 + 📚维护文档索引（NEW）
- TASK.md：实时进度追踪
- **技术细节外放到 docs/**（NEW）: 保持管理层轻量
- **定期运行 /wf_13_doc_maintain**（NEW）: 清理过期文档

✅ **智能文档管理** (NEW)
- 创建技术文档必须在KNOWLEDGE.md中建立索引
- 标记文档优先级（高/中/低）
- 建立任务-文档关联关系
- 工作层文档（docs/research/）添加日期前缀
- 过期文档及时归档到docs/archive/

---

### PRD对齐

✅ **需求追溯**
- 每个任务关联PRD需求
- 决策验证PRD约束
- 提交时检查PRD合规

✅ **质量门控**
- PRD.md永远只读
- PLANNING.md对齐PRD
- 代码满足PRD标准

---

## 🎯 快速参考

### 记住这5个流程

1. **项目启动**: `/wf_01_planning` → `/wf_02_task` → `/wf_03_prime`
2. **功能开发**: `/wf_05_code` → `/wf_07_test` → `/wf_08_review` → `/wf_11_commit`
3. **Bug修复**: `/wf_06_debug` → `/wf_07_test` → `/wf_11_commit`
4. **质量改进**: `/wf_08_review` → `/wf_09_refactor` → `/wf_07_test`
5. **会话管理**: `/wf_03_prime` (开始) → 工作 → `/wf_11_commit` (保存)

### 关键原则

- 🔄 **上下文连续性**: prime → work → commit → clear → prime
- ✅ **质量第一**: code → test → review → commit
- 📋 **进度可见**: 及时更新TASK.md
- 🎯 **PRD对齐**: 所有决策验证PRD需求

---

**最后更新**: 2025-11-07
**版本**: v3.3 (新增智能文档生成)

**相关文档**:
- [命令完整参考](COMMANDS.md)
- [故障排查指南](TROUBLESHOOTING.md)
- [AI执行规则](CLAUDE.md)
- [文档架构最佳实践](DOC_ARCHITECTURE.md) (NEW)
