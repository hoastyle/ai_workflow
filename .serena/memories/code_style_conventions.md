# 代码风格和约定

## 语言规范速查表
| 场景 | 语言 | 示例 |
|------|------|------|
| 交互沟通 | 中文（默认） | - |
| 代码命名 | 英文 | function_name, ClassName |
| 代码注释 | 英文 | // This function handles... |
| 提交信息 | [type] subject | [feat] Add user auth |
| 项目文档 | 中文（默认） | README.md, PLANNING.md |

## 代码格式规范
| 工具 | 语言 | 执行方式 |
|------|------|---------|
| Black | Python | /wf_11_commit自动 |
| Prettier | JS/TS | /wf_11_commit自动 |
| clang-format | C++ | /wf_11_commit自动 |
| gofmt | Go | /wf_11_commit自动 |

## 严格规范（零容忍）
| 规则 | 标准 | 验证 | 修复 |
|------|------|------|------|
| 行尾 | Unix LF | pre-commit | 自动 |
| 尾部空格 | 禁止 | pre-commit（拒绝提交） | pre-commit run --all-files |
| 文件编码 | UTF-8 | pre-commit | 自动 |

## Git 提交规范
**格式**: `[type] subject`

| 类型 | 用途 | 示例 |
|------|------|------|
| [feat] | 新功能 | [feat] Add login API |
| [fix] | Bug修复 | [fix] Resolve timeout |
| [docs] | 文档更新 | [docs] Update README |
| [refactor] | 代码重构 | [refactor] Improve handler |
| [test] | 测试添加 | [test] Add validator tests |

## Markdown 格式规范
| 元素 | 正确 ✅ | 错误 ❌ |
|------|--------|--------|
| 编号 | `Step 1:`, `1.`, `### 步骤 1` | `1️⃣:` (emoji+冒号重叠) |
| 标题层级 | `#`, `##`, `###` | - |
| 列表 | `-`, `1.` | - |
| 代码块 | ` ```language ``` ` | - |
| 链接 | `[text](url)` | - |

## Frontmatter 必需字段（7个）
```yaml
---
title: "文档标题"
description: "一句话描述"
type: "技术设计|系统集成|API参考|教程|故障排查|架构决策"
status: "草稿|完成|待审查"
priority: "高|中|低"
created_date: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---
```

**检查点**: /wf_11_commit自动验证

## 文档分层和约束
| 层级 | 位置 | 约束 | 用途 |
|------|------|------|------|
| 管理层 | docs/management/ | 5个固定文件 | PRD, PLANNING, TASK, CONTEXT, INDEX |
| 技术层 | docs/ | < 500行/文件 | API文档、架构设计 |
| 工作层 | docs/research/ | 临时 | Spike、原型 |
| 归档层 | docs/archive/ | 历史 | 废弃文档 |

## 约束驱动文档规范 (v3.4)
| 约束类型 | 限制 | 检查命令 |
|---------|------|---------|
| 索引大小 | KNOWLEDGE.md < 200行 | /wf_11_commit |
| 单文件大小 | < 500行 | /wf_08_review Dimension 6 |
| 单次增长率 | < 30% | /wf_14_doc Phase 2 |
| Frontmatter | 必需7个字段 | /wf_11_commit |

### 文档类型分类
| 类型 | 位置 | 约束 | 说明 |
|------|------|------|------|
| Type A（架构） | PLANNING.md | < 50行 | 为什么+架构影响 |
| Type B（ADR） | docs/adr/ | < 200行 | 遵循ADR模板 |
| Type C（功能） | docs/ | < 500行 | API、部署文档 |
| Type D（问题） | KNOWLEDGE.md | < 50行 | FAQ、最佳实践 |
| Type E（无文档） | - | - | 代码优化 |

## Pre-commit Hooks自动检查
- 尾部空格检测（零容忍）
- 文件格式验证
- 行尾统一（LF）
- Markdown链接验证
- 命令参考一致性

## 质量检查流程
```bash
# 代码审查
/wf_08_review

# 测试覆盖率
/wf_07_test --coverage

# 格式检查
pre-commit run --all-files

# 提交（自动格式化）
/wf_11_commit "提交信息"
```

## 日期管理规范
**核心原则**: 绝不手动输入，总是使用命令

```bash
TODAY=$(date +%Y-%m-%d)              # 今天
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S) # 完整时间戳
```

| 日期类型 | 规则 |
|---------|------|
| 创建日期 | 创建时固定，永不修改 |
| 最后更新 | 每次编辑自动更新为当前日期 |
| ADR决策日期 | 决策当天的日期 |

## 常用工具命令
| 操作 | 命令 |
|------|------|
| 状态查询 | git status, git log --oneline -10 |
| 代码审查 | /wf_08_review |
| 运行测试 | /wf_07_test "组件" |
| 覆盖率分析 | /wf_07_test --coverage |
| 文档生成 | /wf_14_doc |
| 文档维护 | /wf_13_doc_maintain |
| 提交代码 | /wf_11_commit "消息" |

## 常见问题修复表
| 问题 | 修复方案 |
|------|---------|
| 尾部空格 | pre-commit run --all-files |
| 行尾混乱 | pre-commit run --all-files |
| 格式不统一 | /wf_11_commit（自动处理） |
| Markdown格式错误 | 查看 docs/reference/MARKDOWN_STYLE.md |
| Frontmatter缺失 | python scripts/frontmatter_utils.py generate |

## 设计原则参考
详见 PHILOSOPHY.md（Ultrathink 6原则）

---
**最后更新**: 2025-12-06
**Token节省**: ~390 tokens（通过表格化和移除冗余示例）
