# 代码风格和约定

## 语言规范

### 交互沟通
- **语言**: 中文（默认）
- **例外**: 如果项目设置为英文，优先使用英文

### 代码
- **变量、函数、类名**: 全部英文（国际惯例）
- **注释**: 英文
- **文档字符串**: 英文

### 提交信息
- **格式**: `[type] subject`
- **类型**: feat, fix, docs, refactor, test
- **示例**: `[feat] Add user authentication system`

### 文档
- **默认语言**: 中文（除非项目另有规定）
- **代码注释**: 英文
- **变量名**: 英文

## 代码风格

### 格式化

**自动应用（通过 `/wf_11_commit`）**：

- **Python**: Black
- **JavaScript/TypeScript**: Prettier
- **C++**: clang-format
- **Go**: gofmt

### 行尾规范

- **标准**: Unix LF（`\n`）
- **禁止**: Windows CRLF（`\r\n`）
- **验证**: pre-commit hooks 自动检查

### 尾部空格

- **规则**: 零容忍，绝不允许
- **验证**: pre-commit hooks 自动拒绝
- **修复**: 使用 `pre-commit run --all-files` 自动清理

### 文件格式

- **Markdown**: UTF-8 编码
- **JSON**: 标准格式，不允许注释
- **YAML**: 2 空格缩进

## 提交规范

### 提交信息格式

```
[type] subject

body (可选，但重要改动应包含)
```

### 类型标签

| 类型 | 说明 | 示例 |
|------|------|------|
| `[feat]` | 新功能 | `[feat] Add user login endpoint` |
| `[fix]` | Bug修复 | `[fix] Resolve authentication timeout` |
| `[docs]` | 文档更新 | `[docs] Update API documentation` |
| `[refactor]` | 代码重构 | `[refactor] Improve error handling` |
| `[test]` | 测试添加 | `[test] Add unit tests for validator` |

### 提交最佳实践

1. **原子性**: 一个提交应该是一个逻辑完整的变更
2. **清晰性**: 提交信息要清楚表达意图
3. **追踪性**: 在 body 中关联任务或问题
4. **质量**: 提交前运行 `/wf_08_review`

## 文档标准

### Markdown 格式规范

- **标题**: 使用 `#` `##` `###` 等级制
- **列表**: 使用 `-` 或 `1.`
- **代码块**: 使用 ` ```language ``` `
- **链接**: 使用 `[text](url)` 格式
- **不允许**: emoji 编号（如 `1️⃣:` ）会导致字符重叠

### 推荐的替代方式

```markdown
❌ 错误的做法
1️⃣: 第一步
2️⃣: 第二步

✅ 正确的做法
Step 1: 第一步
Step 2: 第二步

或

1. 第一步
2. 第二步

或

### 步骤 1: 第一步
### 步骤 2: 第二步
```

### Frontmatter 元数据规范

**所有新文档必须包含完整的 Frontmatter**（7个必需字段）：

```yaml
---
title: "文档标题"
description: "一句话描述"
type: "技术设计 | 系统集成 | API参考 | 教程 | 故障排查 | 架构决策"
status: "草稿 | 完成 | 待审查"
priority: "高 | 中 | 低"
created_date: "2025-11-24"
last_updated: "2025-11-24"
---
```

### 文档层级

| 层级 | 位置 | 约束 | 示例 |
|------|------|------|------|
| 管理层 | docs/management/ | 5个文件 | PRD.md, PLANNING.md, TASK.md |
| 技术层 | docs/ | < 500 行/文件 | API 文档、架构设计 |
| 工作层 | docs/research/ | 临时 | Spike、原型验证 |
| 归档层 | docs/archive/ | 历史 | 废弃文档 |

## 约束规范（v3.4）

### 文档约束

| 约束 | 限制 | 目的 | 检查点 |
|------|------|------|--------|
| KNOWLEDGE.md | < 200 行 | 纯索引 | /wf_11_commit |
| 单文件大小 | < 500 行 | 易维护 | /wf_08_review Dimension 6 |
| 单次增长 | < 30% | 避免爆炸 | /wf_14_doc Phase 2 |
| Frontmatter | 必需 | 自动化 | /wf_11_commit |

### 文档类型和位置

| 类型 | 位置 | 约束 | 示例 |
|------|------|------|------|
| Type A（架构） | PLANNING.md | < 50 行 | 为什么和架构影响 |
| Type B（ADR） | docs/adr/ | < 200 行 | 按 ADR 模板 |
| Type C（功能） | docs/ | < 500 行 | API、部署文档 |
| Type D（问题） | KNOWLEDGE.md | < 50 行 | FAQ、最佳实践 |
| Type E（无文档） | - | - | 代码优化 |

## 质量检查

### Pre-commit Hooks

自动执行的检查：

- 尾部空格检测
- 文件格式验证
- 行尾统一（LF）
- Markdown 链接验证
- 命令参考一致性

### 手动检查

**提交前必须**：

```bash
# 运行 code review
/wf_08_review

# 验证测试
/wf_07_test --coverage

# 检查格式
pre-commit run --all-files
```

## 日期管理

### 核心原则

**绝不手动输入日期，总是使用命令动态获取**

```bash
TODAY=$(date +%Y-%m-%d)              # 今天
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S) # 完整时间戳
```

### 日期类型

1. **历史日期**（创建时间） - 创建时固定，永不修改
2. **维护日期**（最后更新） - 每次编辑自动更新为当前日期
3. **ADR 决策日期** - 决策当天的日期

## 工具命令

### Git 操作

```bash
# 查看状态
git status

# 查看日志
git log --oneline -10

# 查看差异
git diff

# 提交代码
/wf_11_commit "提交信息"
```

### 代码质量

```bash
# 运行 code review
/wf_08_review

# 运行测试
/wf_07_test "组件"

# 覆盖率分析
/wf_07_test --coverage

# 自动格式化
/wf_11_commit "提交"  # 自动应用
```

### 文档管理

```bash
# 生成文档
/wf_14_doc

# 维护文档
/wf_13_doc_maintain

# 验证格式
pre-commit run --all-files
```

## 常见问题修复

| 问题 | 修复方案 |
|------|---------|
| 尾部空格 | `pre-commit run --all-files` |
| 行尾混乱 | `pre-commit run --all-files` |
| 格式不统一 | `/wf_11_commit` 自动处理 |
| Markdown 格式错误 | 查看 [docs/reference/MARKDOWN_STYLE.md](docs/reference/MARKDOWN_STYLE.md) |

## 设计原则（Ultrathink）

详见 PHILOSOPHY.md：

1. **简化复杂性** - 复杂问题分解为简单部分
2. **标准优先** - 选择业界标准而非创新
3. **约束驱动** - 在约束下设计，而非无限扩展
4. **可验证性** - 所有设计都能被验证
5. **可维护性** - 考虑 5 年后的维护成本
6. **人类友好** - 优先考虑人的认知负荷
