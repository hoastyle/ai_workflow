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

# 5. 提交代码（自动格式化+上下文更新）
/wf_11_commit "feat: add JWT authentication"

# 6. 更新任务进度
/wf_02_task update
```

**预计时间**: 中等功能 30-60分钟
**关键检查点**:
- [ ] PLANNING.md标准遵守
- [ ] PRD需求满足
- [ ] 测试覆盖率达标
- [ ] 代码审查通过

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

---

## 最佳实践

### 会话管理

✅ **永远先 `/wf_03_prime`**
- 每个新会话的第一个动作
- `/clear` 后立即运行
- 确保AI理解项目上下文

✅ **经常 `/wf_11_commit`**
- 完成一个逻辑功能就提交
- 自动更新CONTEXT.md
- 支持跨会话连续性

✅ **及时 `/wf_02_task update`**
- 完成任务后立即更新
- 保持进度可见
- 便于团队协作

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

✅ **文档维护**
- PLANNING.md：重大决策更新
- KNOWLEDGE.md：新模式记录
- TASK.md：实时进度追踪

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

**最后更新**: 2025-10-31
**版本**: v3.0

**相关文档**:
- [命令完整参考](COMMANDS.md)
- [故障排查指南](TROUBLESHOOTING.md)
- [AI执行规则](CLAUDE.md)
