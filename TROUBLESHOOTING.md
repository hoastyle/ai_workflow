# 故障排查指南

> 🔧 常见问题和解决方案

---

## 📑 目录

- [上下文和会话问题](#上下文和会话问题)
- [命令执行问题](#命令执行问题)
- [文件和权限问题](#文件和权限问题)
- [Git和提交问题](#git和提交问题)
- [Pre-commit问题](#pre-commit问题)
- [其他常见问题](#其他常见问题)

---

## 上下文和会话问题

### 问题：丢失项目上下文

**症状**:
- AI不知道项目架构
- AI不记得之前的工作
- AI询问已经提供过的信息

**解决方案**:
```bash
# 1. 重新加载项目上下文
/wf_03_prime

# 2. 检查CONTEXT.md查看最新会话状态
# (在项目根目录)

# 3. 如果CONTEXT.md不存在或过旧
/wf_11_commit "save current progress"  # 先保存
/wf_03_prime                           # 再加载
```

**预防措施**:
- ✅ 每次会话开始运行 `/wf_03_prime`
- ✅ 完成工作后运行 `/wf_11_commit` 保存
- ✅ `/clear` 后立即运行 `/wf_03_prime`

---

### 问题：Token上下文过大

**症状**:
- Claude提示上下文接近限制
- 响应变慢
- 部分历史消息被截断

**解决方案**:
```bash
# 1. 清理上下文
/clear

# 2. 立即重新加载项目上下文
/wf_03_prime

# 3. 继续工作（CONTEXT.md保证连续性）
```

**原理**:
- `/wf_11_commit` 自动将工作进度保存到 CONTEXT.md
- `/wf_03_prime` 从 CONTEXT.md 恢复会话状态
- 实现跨 `/clear` 边界的工作连续性

---

### 问题：不清楚当前应该做什么

**症状**:
- 忘记当前任务
- 不知道下一步
- 工作流程混乱

**解决方案**:
```bash
# 1. 加载项目上下文
/wf_03_prime

# 2. 查看任务状态
/wf_02_task review

# 3. 查看CONTEXT.md了解最新进度
# (AI会在prime时自动读取)

# 4. 如果仍不清楚
/wf_99_help guide  # 查看工作流指导
```

---

## 命令执行问题

### 问题：不知道用哪个命令

**症状**:
- 面对多个命令不知如何选择
- 不确定命令的功能
- 工作流程不清晰

**解决方案**:
```bash
# 1. 查看命令速查表
/wf_99_help quick

# 2. 查看场景工作流指导
/wf_99_help guide

# 3. 查看工作流决策树
# 阅读 WORKFLOWS.md

# 4. 查询具体命令帮助
/wf_99_help wf_05_code  # 示例
```

**常见场景映射**:
- 新项目 → `/wf_01_planning`
- 会话开始 → `/wf_03_prime`
- 写代码 → `/wf_05_code`
- 修Bug → `/wf_06_debug`
- 提交 → `/wf_11_commit`

---

### 问题：命令执行失败

**症状**:
- 命令报错
- 输出不符合预期
- 无法完成操作

**通用解决步骤**:
```bash
# 1. 检查命令格式是否正确
/wf_XX_name "参数"  # 正确格式

# 2. 检查依赖文件是否存在
# 例如 /wf_05_code 需要 PLANNING.md

# 3. 查看命令的详细说明
/wf_99_help wf_XX_name

# 4. 如果是文件缺失问题，先初始化
/wf_01_planning "项目名"  # 创建PLANNING.md
/wf_02_task create       # 创建TASK.md
```

---

## 文件和权限问题

### 问题：PRD.md相关错误

**症状**:
- AI尝试修改PRD.md
- PRD.md冲突警告
- PRD需求不一致

**解决方案**:

**情况1：AI误修改PRD.md**
```
这是违反规则的！PRD.md是只读文档。

正确做法：
1. 在PLANNING.md中记录技术决策
2. 与团队讨论PRD修改需求
3. 由授权人员更新PRD.md
```

**情况2：PRD.md不存在**
```bash
# 如果是新项目
1. 创建PRD.md（手动或由产品经理提供）
2. 然后运行 /wf_01_planning
```

**情况3：需求冲突**
```
AI会提示冲突并询问确认。
选择：
- 修改实现以符合PRD
- 或明确确认要覆盖PRD（记录原因）
```

---

### 问题：PLANNING.md不存在

**症状**:
- `/wf_05_code` 提示缺少PLANNING.md
- `/wf_02_task create` 失败
- 没有开发标准参考

**解决方案**:
```bash
# 创建PLANNING.md
/wf_01_planning "你的项目名称"

# 然后继续其他操作
/wf_02_task create
/wf_03_prime
```

---

### 问题：TASK.md不存在或过旧

**症状**:
- AI不知道当前任务
- 进度追踪缺失
- `/wf_02_task update` 失败

**解决方案**:
```bash
# 情况1：TASK.md不存在
/wf_02_task create

# 情况2：TASK.md过旧
/wf_02_task update  # 更新现有任务

# 情况3：需要重新生成
# 手动删除或重命名旧的TASK.md
/wf_02_task create  # 从PLANNING.md重新生成
```

---

### 问题：CONTEXT.md混乱或过时

**症状**:
- `/wf_03_prime` 加载的上下文不准确
- 会话恢复不正确
- 工作进度丢失

**解决方案**:
```bash
# CONTEXT.md由/wf_11_commit自动管理，不要手动编辑

# 如果确实有问题：
# 1. 手动删除CONTEXT.md
rm CONTEXT.md

# 2. 完成当前工作并提交（会重新生成）
/wf_11_commit "current work"

# 3. 重新加载
/wf_03_prime
```

---

## Git和提交问题

### 问题：提交被pre-commit拒绝

**症状**:
- `git commit` 失败
- Pre-commit hooks报错
- 文件格式问题

**解决方案**:
```bash
# 1. 查看具体错误
pre-commit run

# 2. 常见问题自动修复
pre-commit run --all-files

# 3. 如果是尾部空格问题（会自动修复）
# 重新尝试提交即可

# 4. 如果是行结尾问题（会自动转换为Unix LF）
# 重新尝试提交即可

# 5. 如果是Markdown链接问题
# 手动检查并修复broken links
```

**最佳实践**:
- 使用 `/wf_11_commit` 而不是手动 `git commit`
- `/wf_11_commit` 自动处理格式化和质量检查

---

### 问题：Pre-commit未安装

**症状**:
- `pre-commit: command not found`
- Hooks未运行
- 无自动格式检查

**解决方案**:
```bash
# 1. 安装pre-commit框架
pip install pre-commit

# 2. 安装hooks到仓库
pre-commit install

# 3. 验证安装
pre-commit run --all-files

# 4. 继续正常提交
/wf_11_commit
```

---

### 问题：尾部空格检测

**症状**:
- Pre-commit报错：trailing whitespace
- 文件有多余空格

**解决方案**:
```bash
# 自动修复（100%安全）
pre-commit run trailing-whitespace --all-files

# 或者运行所有auto-fix hooks
pre-commit run --all-files

# 然后重新提交
git add .
git commit -m "your message"
```

**预防**:
- 使用 `/wf_11_commit`（自动处理）
- 配置编辑器自动删除尾部空格

---

### 问题：行结尾混乱（CRLF vs LF）

**症状**:
- Pre-commit报错：mixed line endings
- Windows/Unix换行符冲突

**解决方案**:
```bash
# 自动转换为Unix LF
pre-commit run mixed-line-ending --all-files

# 或运行所有修复
pre-commit run --all-files

# 配置Git自动处理（推荐）
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows
```

---

### 问题：Git提交信息格式错误

**症状**:
- 不知道用什么commit message格式
- 提交信息不一致

**解决方案**:

使用标准格式：
```
[type] subject

body (optional)
```

类型标签：
- `[feat]` - 新功能
- `[fix]` - Bug修复
- `[docs]` - 文档更新
- `[refactor]` - 代码重构
- `[test]` - 测试添加
- `[chore]` - 维护任务

**最佳实践**:
- 使用 `/wf_11_commit`，AI会自动生成规范的提交信息

---

## Pre-commit问题

### 问题：Pre-commit hooks运行太慢

**症状**:
- 提交等待时间长
- Hooks处理大量文件

**解决方案**:
```bash
# 只检查staged文件（默认行为）
pre-commit run

# 跳过特定hook（谨慎使用）
SKIP=hook-id git commit -m "message"

# 更新hook缓存
pre-commit clean
pre-commit install
```

---

### 问题：Auto-repair hooks失败

**症状**:
- 自动修复未生效
- 文件仍有格式问题

**解决方案**:
```bash
# 1. 手动运行auto-repair hooks
pre-commit run trailing-whitespace --all-files
pre-commit run mixed-line-ending --all-files
pre-commit run auto-fix-markdown --all-files

# 2. 检查文件权限
chmod +x .git/hooks/pre-commit

# 3. 重新安装hooks
pre-commit uninstall
pre-commit install
pre-commit run --all-files
```

---

### 问题：Markdown链接验证失败

**症状**:
- Pre-commit报错：broken markdown links
- 链接指向不存在的文件

**解决方案**:
```bash
# 1. 检查报错的具体链接
pre-commit run markdown-link-check

# 2. 手动修复broken links
# - 检查文件路径是否正确
# - 检查锚点是否存在
# - 修复或删除无效链接

# 3. 对于外部链接
# - 确认URL可访问
# - 或添加到忽略列表
```

---

## 其他常见问题

### 问题：AI给出的代码不符合项目标准

**症状**:
- 代码风格不一致
- 不遵循PLANNING.md规范
- 违反PRD要求

**解决方案**:
```bash
# 1. 明确提醒AI查看标准
/wf_03_prime  # 重新加载PLANNING.md

# 2. 使用代码审查
/wf_08_review

# 3. 如果需要，更新PLANNING.md标准
# 然后重新生成代码
/wf_05_code "same feature with updated standards"
```

---

### 问题：不知道某个决策是否符合PRD

**症状**:
- 技术选型不确定
- 实现方案有疑问
- 需求理解不清

**解决方案**:
```bash
# 1. 架构咨询
/wf_04_ask "这个方案是否符合PRD要求？"

# 2. AI会：
# - 检查PRD.md需求
# - 分析技术方案
# - 提供对齐建议
# - 标记潜在冲突

# 3. 记录决策
# AI会自动更新PLANNING.md（如果是重大决策）
```

---

### 问题：测试覆盖率不足

**症状**:
- `/wf_07_test --coverage` 显示覆盖率低
- 关键代码路径未测试

**解决方案**:
```bash
# 1. 分析覆盖率报告
/wf_07_test --coverage

# 2. AI会识别未覆盖的代码
# 并生成改进任务到TASK.md

# 3. 逐个添加测试
/wf_07_test "uncovered module"

# 4. 再次验证
/wf_07_test --coverage
```

---

### 问题：KNOWLEDGE.md内容混乱

**症状**:
- 难以找到过去的决策
- ADR条目重复
- 解决方案过时

**解决方案**:

定期整理KNOWLEDGE.md：
```markdown
# 建议结构
## 架构决策记录 (ADR)
- ADR-001: 选择技术栈
- ADR-002: 数据库设计

## 问题-解决方案
- [2025-01-01] 登录超时 → 增加token过期时间

## 代码模式
- 错误处理统一模式
- API接口命名规范

## 最佳实践
- 测试策略
- 部署流程
```

**维护规则**:
- 新问题解决后立即记录
- 定期review并归档过时条目
- 保持结构清晰

---

## 🎯 快速诊断流程

遇到问题时，按此顺序排查：

1. **上下文问题？** → `/wf_03_prime`
2. **不知道用什么命令？** → `/wf_99_help`
3. **文件缺失？** → `/wf_01_planning` / `/wf_02_task create`
4. **Git提交失败？** → `pre-commit run --all-files`
5. **代码质量问题？** → `/wf_08_review`
6. **仍然无法解决？** → 查阅本文档或询问团队

---

## 📞 获取更多帮助

- **命令参考**: [COMMANDS.md](COMMANDS.md)
- **工作流指导**: [WORKFLOWS.md](WORKFLOWS.md)
- **AI执行规则**: [CLAUDE.md](CLAUDE.md)
- **项目README**: [README.md](README.md)

---

**最后更新**: 2025-10-31
**版本**: v3.1
