## Usage
`@wf_help.md [command|workflow|quick]`

## Purpose
提供工作流命令的快速使用指导和交互式帮助

## Process
根据参数提供不同级别的帮助：

### 无参数 - 显示快速入门指南
```
🚀 Claude Code 工作流快速入门

1️⃣ 首次使用:
   @wf_planning.md 项目名称  # 创建项目规划
   @wf_task.md create       # 生成任务列表

2️⃣ 日常工作:
   @wf_prime.md            # 加载项目上下文
   @wf_code.md 功能描述     # 开发功能
   @wf_test.md            # 创建测试
   @wf_commit.md          # 提交代码

3️⃣ 上下文管理:
   /clear                 # 清理上下文
   @wf_prime.md          # 重新加载继续

输入 @wf_help.md quick 查看常用命令
输入 @wf_help.md workflow 查看完整流程
输入 @wf_help.md <命令名> 查看具体命令
```

### quick - 显示常用命令速查
```
📋 常用命令速查

基础流程:
• @wf_prime.md         - 加载项目上下文
• @wf_code.md <功能>   - 实现功能
• @wf_test.md <模块>   - 创建测试
• @wf_commit.md        - 提交代码

问题解决:
• @wf_debug.md <错误>  - 调试问题
• @wf_fix.md <错误>    - 修复错误
• @wf_ask.md <问题>    - 架构咨询

代码质量:
• @wf_review.md        - 代码审查
• @wf_refactor.md      - 代码重构
• @wf_optimize.md      - 性能优化

任务管理:
• @wf_task.md review   - 查看任务
• @wf_task.md update   - 更新进度
```

### workflow - 显示完整工作流
```
🔄 完整工作流程

【新功能开发】
1. @wf_ask.md 架构设计问题
2. @wf_code.md 实现功能
3. @wf_test.md 添加测试
4. @wf_review.md 代码审查
5. @wf_format.md 格式化
6. @wf_commit.md 提交
7. @wf_task.md update 更新任务

【Bug修复】
1. @wf_debug.md 分析错误
2. @wf_fix.md 实施修复
3. @wf_test.md 验证修复
4. @wf_commit.md 提交修复

【代码优化】
1. @wf_review.md 识别问题
2. @wf_refactor.md 重构代码
3. @wf_optimize.md 性能优化
4. @wf_test.md 回归测试
5. @wf_commit.md 提交改进

【部署准备】
1. @wf_coverage.md 检查覆盖率
2. @wf_review.md 最终审查
3. @wf_deploy_check.md 部署检查
```

### 具体命令 - 显示命令详情
对于 `@wf_help.md wf_code` 这样的查询：
```
📖 wf_code.md - 功能实现命令

用途: 实现新功能，遵循项目架构和标准

用法: @wf_code.md <功能描述>

示例:
• @wf_code.md 实现用户登录功能
• @wf_code.md 添加邮件发送服务
• @wf_code.md 修复购物车计算逻辑

集成:
• 读取: PLANNING.md (架构标准)
• 更新: TASK.md (任务进度)
• 触发: @wf_test.md (测试验证)
• 后续: @wf_commit.md (代码提交)

提示:
✓ 实现前先用 @wf_ask.md 咨询架构
✓ 完成后运行 @wf_test.md 验证
✓ 提交前执行 @wf_format.md 格式化
```

## Output Format
根据参数返回相应的帮助信息，使用清晰的格式和表情符号增强可读性

## Integration
- 可在任何时候调用获取帮助
- 不需要项目上下文
- 提供交互式学习路径