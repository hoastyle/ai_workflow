# /wf_14_doc 完整示例库

本文档包含 `/wf_14_doc` 命令的完整执行示例和输出格式参考。

## 快速导航

- [核心命令示例](#核心命令示例)
- [1. 代码库分析输出示例](#1-代码库分析输出示例)
- [2. 文档缺口分析示例](#2-文档缺口分析示例)
- [3. 交互式文档向导示例](#3-交互式文档向导示例)
- [4. 信息提取示例](#4-信息提取示例)
- [5. 完整执行示例](#5-完整执行示例)

---

## 核心命令示例

### Frontmatter 工具使用

```bash
# 生成单个文档的 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py generate docs/api/auth.md

# 批量生成
python ~/.claude/commands/scripts/frontmatter_utils.py generate-batch docs/api/

# 验证 Frontmatter
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/api/auth.md

# 批量验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 更新 KNOWLEDGE.md 索引
python ~/.claude/commands/scripts/frontmatter_utils.py update-index KNOWLEDGE.md
```

---

## 1. 代码库分析输出示例

**待补充**：详细的代码库分析报告示例

---

## 2. 文档缺口分析示例

**待补充**：文档缺口检测报告示例

---

## 3. 交互式文档向导示例

**待补充**：交互式用户确认界面示例

---

## 4. 信息提取示例

**待补充**：
- API 文档提取示例
- 环境变量提取示例
- 依赖和技术栈提取示例
- 从测试代码提取使用示例

---

## 5. 完整执行示例

本节包含3个完整的执行场景：

### 场景 1: 新项目首次生成文档

**待补充**

### 场景 2: 代码更新后更新 API 文档

**待补充**

### 场景 3: CI/CD 检查模式

**待补充**

---

**See Also**:
- [/wf_14_doc](../../wf_14_doc.md) - 命令主文档
- [文档模板库](doc_templates/) - 标准文档模板
- [文档生成工作流](doc_generation_workflow.md) - 约束驱动工作流
- [文档生成输出格式](doc_generation_outputs.md) - 输出格式参考
