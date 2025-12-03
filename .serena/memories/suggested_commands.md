# 项目主要命令

## 核心工作流命令（14个）

所有命令都是 Slash Commands，格式为 `/wf_XX_name`

### 1. 项目初始化和管理

```bash
# 创建项目规划文档
/wf_01_planning "项目描述"

# 管理任务追踪
/wf_02_task create          # 初始化任务
/wf_02_task update "任务"   # 更新任务状态
/wf_02_task list            # 列出所有任务

# 加载项目上下文（每次会话必须）
/wf_03_prime
```

### 2. 开发实现

```bash
# 架构咨询
/wf_04_ask "技术问题"
/wf_04_ask "问题" --review-codebase  # 深度代码库分析
/wf_04_ask "问题" --think             # 启用结构化思考
/wf_04_ask "问题" --c7                # 查询官方库文档

# 功能实现
/wf_05_code "功能描述"

# 调试修复
/wf_06_debug "错误描述"
/wf_06_debug "错误" --quick   # 快速修复模式
/wf_06_debug "错误" --deep    # 深度分析
```

### 3. 质量保证

```bash
# 测试开发
/wf_07_test "组件名"
/wf_07_test "组件" --coverage  # 覆盖率分析

# 代码审查
/wf_08_review

# 代码重构
/wf_09_refactor "组件名"

# 性能优化
/wf_10_optimize "目标"
```

### 4. 提交和部署

```bash
# 提交代码（自动更新CONTEXT.md）
/wf_11_commit "提交信息"

# 部署检查
/wf_12_deploy_check
```

### 5. 文档管理（NEW v3.4）

```bash
# 智能文档生成（约束驱动）
/wf_14_doc
/wf_14_doc --ui  # UI 增强

# 文档维护和清理
/wf_13_doc_maintain
```

### 6. 帮助

```bash
# 获取帮助
/wf_99_help
```

## 常用命令组合

### 新功能开发流程

```bash
/wf_03_prime                    # 加载上下文
/wf_04_ask "架构设计"            # 获取指导（可选）
/wf_05_code "实现功能"           # 编写代码
/wf_07_test "组件名"             # 添加测试
/wf_08_review                   # 代码审查
/wf_11_commit "feat: 新功能"     # 提交
```

### Bug 修复流程

```bash
/wf_06_debug "错误描述"           # 调试
/wf_07_test "相关组件"            # 验证修复
/wf_11_commit "fix: Bug描述"      # 提交
```

### 代码质量改进

```bash
/wf_08_review                   # 分析质量
/wf_09_refactor "组件"           # 重构
/wf_10_optimize "目标"           # 优化
/wf_07_test --coverage          # 验证覆盖率
/wf_11_commit "refactor: 改进"  # 提交
```

### 文档生成流程

```bash
/wf_03_prime                     # 加载上下文
/wf_05_code "实现功能"           # 完成代码
                                # Step 8: 自动文档决策树
/wf_08_review                   # 代码审查
                                # Dimension 6: 文档约束检查
/wf_14_doc                      # 生成文档（三阶段门控）
/wf_13_doc_maintain             # 验证索引
/wf_11_commit "docs: 新文档"    # 提交
```

## 命令参数和标志

### 常用标志

| 标志 | 命令 | 说明 |
|------|------|------|
| `--coverage` | `/wf_07_test` | 显示测试覆盖率分析 |
| `--quick` | `/wf_06_debug` | 快速修复模式 |
| `--deep` | `/wf_06_debug` | 深度分析模式 |
| `--think` | `/wf_04_ask` | 启用结构化思考 |
| `--c7` | `/wf_04_ask` | 查询官方库文档 |
| `--research` | `/wf_04_ask` | Web 搜索模式 |
| `--review-codebase` | `/wf_04_ask` | 深度代码库分析 |
| `--ui` | `/wf_14_doc` | UI 增强模式 |

## 快速参考

### 我应该用哪个命令？

- **需要设计建议** → `/wf_04_ask`
- **要实现功能** → `/wf_05_code`
- **遇到 Bug** → `/wf_06_debug`
- **要添加测试** → `/wf_07_test`
- **要审查代码** → `/wf_08_review`
- **要改进结构** → `/wf_09_refactor`
- **要优化性能** → `/wf_10_optimize`
- **要生成文档** → `/wf_14_doc`
- **要提交代码** → `/wf_11_commit`
- **丢失上下文** → `/wf_03_prime`

### 完整命令参考

详见项目中的 COMMANDS.md 文件。
