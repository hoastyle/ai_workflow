## Usage
`@wf_help.md [command|guide|quick]`

## Purpose
提供工作流命令的完整帮助系统，整合快速参考、场景指导和命令详情

## Process
根据参数提供不同级别的帮助：

### 无参数 - 显示主菜单和快速入门
```
🚀 Claude Code 工作流帮助系统

═══════════════════════════════════════

🏁 快速入门 (3步开始)
1️⃣ @wf_planning.md 项目名称    # 创建项目规划
2️⃣ @wf_task.md create         # 生成任务列表  
3️⃣ @wf_prime.md               # 开始工作！

📋 常用命令
• @wf_code.md <功能>           # 实现功能
• @wf_debug.md <错误> [--quick] # 调试修复  
• @wf_test.md <模块>           # 创建测试
• @wf_commit.md                # 提交代码

🔄 会话管理
• /clear → @wf_prime.md        # 清理并重新加载

═══════════════════════════════════════

📖 获取更多帮助:
@wf_help.md quick      # 命令速查表
@wf_help.md guide      # 场景流程指导
@wf_help.md <命令名>    # 具体命令帮助
```

### quick - 显示命令速查表
```
📋 WF_ 命令速查表 (13个核心命令)

══════════════════════════════════════════════════

🔄 核心流程
@wf_prime.md                  # 加载项目上下文
@wf_planning.md <项目名>      # 创建/更新项目规划
@wf_task.md <action>          # 任务管理(create/review/update)

💻 开发命令  
@wf_code.md <功能描述>        # 实现功能(含格式化)
@wf_ask.md <架构问题>         # 架构咨询
@wf_debug.md <错误> [--quick] # 调试修复(合并fix功能)
@wf_refactor.md <目标>        # 代码重构

✅ 质量保证
@wf_test.md <模块>            # 测试开发(含覆盖率)
@wf_review.md <范围>          # 代码审查(含格式验证)
@wf_optimize.md <目标>        # 性能优化

🔧 操作命令
@wf_commit.md [消息]          # 提交(含格式化+上下文更新)
@wf_deploy_check.md <环境>    # 部署检查

📚 帮助
@wf_help.md [选项]            # 帮助系统(整合版)

══════════════════════════════════════════════════

💡 黄金法则:
1. 永远先 @wf_prime.md
2. 经常 @wf_task.md update  
3. 遇事不决 @wf_ask.md
```

### guide - 显示场景工作流指导
```
🔄 工作流场景指导

══════════════════════════════════════════════════

🆕 【新项目开始】
1. @wf_planning.md <项目名>     # 创建项目架构
2. @wf_task.md create           # 生成初始任务
3. @wf_prime.md                 # 准备开发环境

🏗️ 【功能开发】(标准流程)
1. @wf_ask.md 如何实现XX功能？   # 架构咨询
2. @wf_code.md 实现XX功能        # 开发实现  
3. @wf_test.md XX模块            # 创建测试
4. @wf_review.md XX模块          # 代码审查
5. @wf_commit.md                 # 提交(自动格式化)
6. @wf_task.md update            # 更新进度

🐛 【问题修复】
• 复杂问题: @wf_debug.md <详细错误描述>
• 简单问题: @wf_debug.md <错误> --quick  
• 验证修复: @wf_test.md <相关模块>
• 提交修复: @wf_commit.md

🔧 【代码改进】
1. @wf_review.md                # 识别改进点
2. @wf_refactor.md <目标代码>    # 重构改进
3. @wf_optimize.md <性能目标>    # 性能优化
4. @wf_test.md                   # 回归测试
5. @wf_commit.md                 # 提交改进

📦 【部署准备】
1. @wf_test.md --coverage        # 检查测试覆盖率
2. @wf_review.md --final         # 最终代码审查
3. @wf_deploy_check.md <环境>    # 部署就绪检查

💼 【会话管理】
启动: @wf_prime.md              # 每个会话开始
工作: 各种开发命令...            # 正常开发流程
保存: @wf_commit.md + @wf_task.md update
清理: /clear                    # 上下文过大时
恢复: @wf_prime.md              # 重新加载继续

══════════════════════════════════════════════════

📊 闭环追踪:
PRD.md → PLANNING.md → TASK.md → CONTEXT.md → Git提交
```

### 具体命令 - 显示命令详情
对于 `@wf_help.md wf_xxx` 形式的查询，显示该命令的详细信息：

```
📖 {COMMAND_NAME} - {命令用途}

═══════════════════════════════════════════════

📋 基本信息
用法: @{COMMAND_NAME} <参数说明>
功能: {详细功能描述}

🎯 使用示例  
• @{COMMAND_NAME} {示例1}
• @{COMMAND_NAME} {示例2} 
• @{COMMAND_NAME} {示例3}

🔗 集成关系
读取文件: {相关输入文件}
更新文件: {相关输出文件}  
前置命令: {建议的前置命令}
后续命令: {建议的后续命令}

💡 最佳实践
✓ {实践建议1}
✓ {实践建议2}
✓ {实践建议3}

⚠️ 注意事项
• {注意事项1}
• {注意事项2}

═══════════════════════════════════════════════

💬 需要更多帮助？
@wf_help.md guide    # 查看工作流指导
@wf_ask.md <问题>    # 针对具体问题咨询
```

## Command Map
当请求具体命令帮助时，提供以下标准化信息：

### 核心命令信息模板
- **wf_prime.md**: 会话初始化，加载项目上下文
- **wf_planning.md**: 项目规划管理，创建架构文档  
- **wf_task.md**: 任务跟踪，管理开发进度
- **wf_code.md**: 功能实现，集成自动格式化
- **wf_ask.md**: 架构咨询，设计决策支持
- **wf_debug.md**: 调试修复，支持快速和深度模式
- **wf_refactor.md**: 代码重构，结构改进
- **wf_test.md**: 测试开发，集成覆盖率分析
- **wf_review.md**: 代码审查，质量验证
- **wf_optimize.md**: 性能优化，效率提升
- **wf_deploy_check.md**: 部署检查，上线准备
- **wf_commit.md**: 代码提交，集成格式化和上下文更新
- **wf_help.md**: 帮助系统，整合所有指导功能

## Output Format
根据参数返回相应的帮助信息：
- 使用清晰的ASCII分隔线和表情符号
- 提供结构化的信息布局
- 包含实用的示例和最佳实践
- 支持中文界面的友好交互

## Integration
- 不需要项目上下文，可随时调用
- 整合原有guide和quick功能
- 提供完整的命令学习路径
- 支持交互式帮助导航