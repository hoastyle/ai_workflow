# 贡献指南

> 📖 为Claude Code Workflow Commands项目贡献的标准和流程

---

## 📑 目录

- [项目概览](#项目概览)
- [开发环境设置](#开发环境设置)
- [命令开发规范](#命令开发规范)
- [文档维护规范](#文档维护规范)
- [提交流程](#提交流程)
- [质量标准](#质量标准)

---

## 项目概览

### 目的
本项目为Claude Code提供一套完整的工作流命令系统，支持从项目规划到部署的完整开发生命周期。

### 核心组件

| 组件 | 文件 | 用途 |
|------|------|------|
| **命令定义** | `wf_*.md` (13个) | 工作流命令实现 |
| **用户文档** | `README.md` | 项目入口和快速开始 |
| **命令参考** | `COMMANDS.md` | 13个命令的完整参考 |
| **工作流指导** | `WORKFLOWS.md` | 场景化工作流和决策树 |
| **故障排查** | `TROUBLESHOOTING.md` | 常见问题解决方案 |
| **AI规则** | `CLAUDE.md` | AI执行规范和权限 |
| **历史记录** | `CHANGELOG.md` | 版本更新历史 |

---

## 开发环境设置

### 环境要求
- Git 2.0+
- Python 3.7+ (用于pre-commit)
- Pre-commit框架

### 初始化步骤

```bash
# 1. 克隆仓库
git clone <repository-url>
cd commands

# 2. 安装pre-commit框架
pip install pre-commit

# 3. 安装git hooks
pre-commit install

# 4. 验证安装（可选）
pre-commit run --all-files
```

### 开发工具
- **编辑器**: VSCode, Vim, 等任意Markdown编辑器
- **Markdown预览**: VSCode Markdown Preview 或在线工具
- **Mermaid图表**: 使用GitHub Markdown或Mermaid Live Editor预览
- **Git工具**: Git CLI 或 GitHub Desktop

---

## 命令开发规范

### 命令文件结构

每个命令文件(`wf_XX_name.md`)必须遵循以下结构：

```markdown
---
command: /wf_XX_name
index: XX
phase: "阶段名称"
reads: [文件列表]
writes: [文件列表]
prev_commands: [命令列表]
next_commands: [命令列表]
context_rules:
  - "规则1"
  - "规则2"
---

## 执行上下文
**输入**: 具体输入说明
**输出**: 具体输出说明
**依赖链**: 命令依赖关系

## Usage
`/wf_XX_name <ARGUMENTS>`

## Context
- 项目上下文和需求说明

## Your Role
- AI角色说明和职责

## Process
1. **步骤1**: 说明
2. **步骤2**: 说明
3. ...

## Output Format
1. **产出1** - 说明
2. **产出2** - 说明
3. ...

## Workflow Integration
- 与其他命令的集成说明
```

### YAML元数据规范

#### command
- **格式**: `/wf_XX_name`
- **要求**: 必须与文件名对应
- **例子**: `/wf_05_code`

#### index
- **格式**: 两位数字
- **范围**: 01-12, 99
- **规则**: 按开发生命周期顺序

#### phase
- **可选值**:
  - "基础设施" (1-3)
  - "开发实现" (4-6)
  - "质量保证" (7-10)
  - "运维部署" (11-12)
  - "支持" (99)

#### reads/writes
- **格式**: 列表 `[文件1, 文件2, ...]`
- **值**: 具体文件名或说明
- **例子**: `[PLANNING.md(开发标准), TASK.md(当前任务)]`

#### prev_commands/next_commands
- **格式**: 列表 `[/wf_XX, /wf_YY, ...]`
- **说明**: 前置命令和后续命令
- **可选**: 不是所有命令都有

#### context_rules
- **格式**: 列表 `["规则1", "规则2"]`
- **用途**: AI执行规则和约束
- **例子**: `"PRD.md是只读的，绝不修改"`

### 最佳实践

1. **清晰的命令Usage**
   ```markdown
   ✅ 好: `/wf_05_code "实现用户认证"`
   ❌ 差: `/wf_05_code`
   ```

2. **完整的执行上下文**
   ```markdown
   **输入**: PLANNING.md标准 + TASK.md任务
   **输出**: 代码实现 + TASK.md更新
   **依赖链**: /wf_04_ask (可选) → 当前 → /wf_07_test
   ```

3. **详细的Process步骤**
   - 每个步骤应该清晰且可执行
   - 包含检查点和验证方法
   - 提供具体的示例

4. **Output Format清晰**
   - 列出所有可能的输出
   - 说明输出的用途和格式

---

## 文档维护规范

### 文档结构规范

所有主要文档(`COMMANDS.md`, `WORKFLOWS.md`, `TROUBLESHOOTING.md`, `README.md`)应遵循：

```markdown
# 标题

> 简要说明

---

## 📑 目录

- [节点1](#节点1)
- [节点2](#节点2)
- ...

---

## 节点1

### 小节1.1

内容...

---

**最后更新**: YYYY-MM-DD
**版本**: vX.X
```

### 版本号规范

- **格式**: `vX.Y.Z` (语义化版本)
  - X: 主版本 (大功能变更)
  - Y: 次版本 (新功能)
  - Z: 补丁版本 (bug修复)

- **当前版本**: v3.0
  - 同步所有文档的版本号
  - 每次重大发布更新版本号

### 日期格式规范

- **格式**: `YYYY-MM-DD` (ISO 8601)
- **标签**: `**最后更新**: YYYY-MM-DD`
- **自动更新**: 使用`$(date +%Y-%m-%d)`在脚本中
- **手动更新**: 提交时更新为当前日期

### 文档交叉引用

- **链接格式**: `[描述](文件.md)` 或 `[描述](文件.md#锚点)`
- **锚点**: 使用小写英文加连字符
- **验证**: 提交前运行`pre-commit run`验证链接

---

## 提交流程

### 前置检查

```bash
# 1. 确保本地分支最新
git pull origin master

# 2. 创建特性分支（如需）
git checkout -b feature/your-feature-name

# 3. 进行修改
# 编辑文件...

# 4. 运行pre-commit检查
pre-commit run --files <修改的文件>

# 修复任何问题后重新检查
pre-commit run --files <修改的文件>
```

### 提交信息格式

```
[type][scope] subject

body

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 提交类型 (type)

| 类型 | 说明 | 例子 |
|------|------|------|
| `[feat]` | 新功能 | `[feat] Add new command wf_13` |
| `[fix]` | Bug修复 | `[fix] 统一命令Usage格式` |
| `[docs]` | 文档更新 | `[docs] 更新CHANGELOG` |
| `[refactor]` | 代码重构 | `[refactor] 重组文档结构` |
| `[test]` | 测试相关 | `[test] 添加链接验证` |
| `[chore]` | 杂务 | `[chore] 清理临时文件` |

### 提交作用域 (scope)

指定修改的主要部分：
- `commands` - 命令文件修改
- `docs` - 文档修改
- `workflow` - 工作流修改
- `ci` - CI/CD修改
- `config` - 配置文件修改

### 完整提交示例

```bash
git commit -m "$(cat <<'EOF'
[docs] 更新CHANGELOG和版本号

统一所有文档的版本号为v3.0，添加v3.0的完整变更记录。

- COMMANDS.md: v2.5 → v3.0
- WORKFLOWS.md: v2.5 → v3.0
- TROUBLESHOOTING.md: v2.5 → v3.0
- CHANGELOG.md: 添加v3.0历史记录

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## 质量标准

### Pre-commit钩子

项目配置了自动质量检查，提交前会自动运行：

```yaml
- 尾部空格检测 (zero tolerance)
- 行结尾验证 (Unix LF)
- 文件格式验证
- Markdown链接验证
- 命令引用一致性检查
```

### 代码审查清单

提交前检查：

- [ ] **命令一致性**
  - [ ] Usage格式: `/wf_XX_name`
  - [ ] YAML元数据完整
  - [ ] reads/writes列表准确

- [ ] **文档质量**
  - [ ] 中文或英文一致
  - [ ] Markdown格式正确
  - [ ] 链接有效（通过pre-commit验证）
  - [ ] 无拼写错误

- [ ] **版本号和日期**
  - [ ] 版本号与CHANGELOG一致
  - [ ] 日期格式为YYYY-MM-DD
  - [ ] 日期为当前日期或提交日期

- [ ] **依赖关系**
  - [ ] prev_commands正确
  - [ ] next_commands正确
  - [ ] 与其他命令的集成清晰

- [ ] **流程指导**
  - [ ] Process步骤清晰可执行
  - [ ] Output Format完整
  - [ ] 包含具体示例

### 常见问题修复

| 问题 | 解决方案 |
|------|---------|
| 尾部空格 | `pre-commit run --all-files` (自动修复) |
| 行结尾混乱 | `pre-commit run --all-files` (自动修复) |
| 链接错误 | 检查文件是否存在和锚点拼写 |
| 命令引用不一致 | 统一使用 `/wf_XX_name` 格式 |

---

## 维护规范

### 版本发布流程

1. **特性完成**
   - 所有代码审查完成
   - 所有测试通过
   - 文档已更新

2. **版本号更新**
   - 更新CHANGELOG.md添加新版本
   - 更新所有文档的版本号
   - 更新所有文档的日期

3. **提交发布**
   ```bash
   git tag vX.X.X
   git push origin master --tags
   ```

### 常见维护任务

#### 添加新命令

1. 创建`wf_XX_name.md`文件
2. 填写YAML frontmatter元数据
3. 编写完整的Process和Output
4. 更新COMMANDS.md添加引用
5. 更新WORKFLOWS.md的命令表和决策树
6. 运行pre-commit验证
7. 提交："[feat] Add new command /wf_XX_name"

#### 更新命令

1. 修改对应的`wf_XX_name.md`
2. 更新CHANGELOG.md说明变更
3. 如有interface变更，更新COMMANDS.md
4. 运行pre-commit验证
5. 提交："[docs] Update /wf_XX_name documentation"

#### 删除命令

1. 确认没有其他命令依赖此命令
2. 从git中删除文件：`git rm wf_XX_name.md`
3. 从COMMANDS.md删除引用
4. 从WORKFLOWS.md删除引用
5. 更新CHANGELOG.md说明弃用
6. 提交："[refactor] Remove deprecated command /wf_XX_name"

---

## 常见问题

### Q: 如何测试文档链接有效性？
A: 运行 `pre-commit run`，它会自动验证所有Markdown链接。

### Q: 如何添加mermaid图表？
A: 在Markdown中使用：
```markdown
\`\`\`mermaid
graph TD
    A --> B
\`\`\`
```
GitHub会自动渲染。

### Q: 如何更新版本号？
A: 同步更新以下文件中的版本号：
- CHANGELOG.md (新增v版本条目)
- COMMANDS.md (**版本**: vX.X)
- WORKFLOWS.md (**版本**: vX.X)
- TROUBLESHOOTING.md (**版本**: vX.X)
- README.md (**版本**: vX.X)

### Q: 如何处理breaking changes？
A:
1. 在CHANGELOG.md中清楚标记breaking changes
2. 更新所有受影响的文档
3. 提升主版本号 (v3.0 → v4.0)
4. 在提交信息中说明impact

---

## 相关资源

- **项目README**: [README.md](README.md)
- **命令参考**: [COMMANDS.md](COMMANDS.md)
- **工作流指导**: [WORKFLOWS.md](WORKFLOWS.md)
- **故障排查**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **AI规则**: [CLAUDE.md](CLAUDE.md)
- **更新历史**: [CHANGELOG.md](CHANGELOG.md)

---

**最后更新**: 2025-10-31
**版本**: v3.0

本贡献指南遵循项目的高质量标准，确保所有贡献保持一致性和可维护性。
