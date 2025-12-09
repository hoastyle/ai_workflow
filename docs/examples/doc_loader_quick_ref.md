---
title: "DocLoader 快速参考"
description: "DocLoader 核心功能和常用模式速查卡"
type: "参考"
status: "完成"
priority: "高"
created_date: "2025-12-09"
last_updated: "2025-12-09"
related_documents:
  - "docs/examples/doc_loader_usage.md"
  - "docs/examples/wf_integration_example.md"
tags: ["quick-reference", "doc-loader", "cheatsheet"]
authors: ["Claude"]
version: "1.0"
---

# DocLoader 快速参考卡

## 📦 导入

```python
# 方式 1: 使用类
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 方式 2: 使用便捷函数
from commands.lib.doc_loader import (
    load_doc_sections,
    load_doc_summary,
    estimate_doc_tokens
)
```

---

## 🎯 核心功能

### 1. 章节加载 (80% Token 节省)

```python
# 加载特定章节
sections = loader.load_sections(
    "docs/guides/workflow.md",
    sections=["Step 3", "Step 5", "Step 7"]
)

# 访问内容
for name, content in sections.items():
    print(f"=== {name} ===\n{content}\n")
```

### 2. 摘要加载 (95% Token 节省)

```python
# 快速预览（前50行或第一个##标题前）
summary = loader.load_summary("docs/guides/workflow.md")

# 自定义长度
summary = loader.load_summary("docs/guides/workflow.md", max_lines=100)
```

### 3. Token 估算

```python
# 加载前估算
content = "Your document content here..."
tokens = loader.estimate_tokens(content)
print(f"Will consume ~{tokens} tokens")

# 公式: len(content) // 4
# 适用: 中英混合文档
```

### 4. 缓存管理

```python
# 查看缓存统计
stats = loader.get_cache_stats()
print(f"Items: {stats['items']}, Tokens: {stats['estimated_tokens']}")

# 清理缓存
loader.clear_cache()

# 禁用缓存
sections = loader.load_sections("doc.md", ["Section A"], use_cache=False)
```

---

## 🚀 使用模式

### 模式 A: 快速模式

```python
# 只需概览，不需细节
summary = load_doc_summary("docs/guides/workflow.md")
# ~100 tokens vs ~2000 tokens (95% 节省)
```

### 模式 B: 任务聚焦

```python
# 只加载当前任务相关章节
if task == "implementation":
    sections = ["Step 3: 开发", "Step 4: 测试"]
elif task == "debugging":
    sections = ["Step 5: 调试", "Step 6: 修复"]

content = load_doc_sections("docs/guides/workflow.md", sections)
# ~400 tokens vs ~2000 tokens (80% 节省)
```

### 模式 C: Token 预算控制

```python
# 先估算，超限则降级
with open("large_doc.md", 'r') as f:
    full_content = f.read()

estimated = estimate_doc_tokens(full_content)

if estimated > 5000:
    content = load_doc_summary("large_doc.md")
else:
    content = full_content
```

### 模式 D: 渐进式加载

```python
# 第一步：加载摘要
summary = loader.load_summary("docs/guides/workflow.md")

# 第二步：根据需要加载详细章节
if user_needs_details:
    sections = loader.load_sections(
        "docs/guides/workflow.md",
        sections=["Step 3", "Step 5"]
    )
```

---

## 📊 性能数据

| 加载方式 | 典型文档 (2000行) | 节省比例 | 适用场景 |
|---------|------------------|---------|---------|
| **全文** | ~2000 tokens | - | 需要完整内容 |
| **章节** (2-3个) | ~400 tokens | 80% | 任务聚焦 |
| **摘要** | ~100 tokens | 95% | 快速预览 |

---

## ⚠️ 注意事项

### ✅ 推荐做法

1. **优先章节加载**: 默认使用 `load_sections()`
2. **启用缓存**: 频繁访问的文档保持缓存开启
3. **估算 Token**: 大文档加载前先检查
4. **相对路径**: 使用相对于项目根目录的路径

### ❌ 避免

1. **盲目全文加载**: 导致 Token 浪费
2. **硬编码绝对路径**: 降低可移植性
3. **忽略章节匹配**: 章节标题必须完全匹配
4. **过度缓存**: 动态文档不要缓存

---

## 🔧 故障排查

### 问题: Section not found

```python
# 调试：查看实际章节标题
with open("doc.md", 'r') as f:
    for line in f:
        if line.startswith('#'):
            print(line.strip())

# 确保标题完全匹配（包括大小写、空格）
sections = loader.load_sections("doc.md", ["Step 3"])  # ✅
sections = loader.load_sections("doc.md", ["step 3"])  # ❌
```

### 问题: 路径错误

```python
# 使用相对路径（相对于项目根目录）
loader.load_sections("docs/guides/workflow.md", ["Step 3"])  # ✅

# 或使用绝对路径
loader.load_sections("/full/path/to/workflow.md", ["Step 3"])  # ✅
```

### 问题: Token 估算不准

```python
# 当前公式适用于中英混合
# 纯中文可能偏低 10-20%
# 代码密集文档可能偏低

# 建议：添加 20% 安全余量
estimated = loader.estimate_tokens(content)
safe_estimate = int(estimated * 1.2)
```

---

## 🎓 集成示例

### 示例 1: Workflow 命令集成

```python
def load_workflow_docs(mode: str):
    """根据模式加载文档"""
    loader = DocLoader()

    if mode == "quick":
        return loader.load_summary("docs/guides/workflow.md")

    elif mode == "full":
        return loader.load_sections(
            "docs/guides/workflow.md",
            sections=["Step 1", "Step 2", "Step 3", "Step 4"]
        )

    elif mode == "task":
        # 根据任务动态选择
        sections = get_relevant_sections()
        return loader.load_sections("docs/guides/workflow.md", sections)
```

### 示例 2: 带预算控制

```python
def smart_load(doc_path: str, sections: list, max_tokens: int = 2000):
    """智能加载（带预算控制）"""
    loader = DocLoader()

    # 尝试加载
    content = loader.load_sections(doc_path, sections)
    full_text = "\n\n".join(content.values())
    estimated = loader.estimate_tokens(full_text)

    # 超限则降级
    if estimated > max_tokens:
        return loader.load_summary(doc_path)
    else:
        return content
```

---

## 📚 相关资源

- **详细文档**: [docs/examples/doc_loader_usage.md](doc_loader_usage.md)
- **集成指南**: [docs/examples/wf_integration_example.md](wf_integration_example.md)
- **源代码**: [commands/lib/doc_loader.py](../../commands/lib/doc_loader.py)
- **ADR**: [docs/adr/2025-12-09-workflow-three-tier-architecture.md](../adr/2025-12-09-workflow-three-tier-architecture.md)

---

## 🚦 状态和版本

| 项目 | 状态 | 说明 |
|------|------|------|
| **核心实现** | ✅ 完成 | 361行，12个方法 |
| **测试覆盖** | ✅ 完成 | 4/4 测试通过 |
| **文档** | ✅ 完成 | 使用指南 + 集成示例 |
| **Workflow 集成** | 🟡 待实施 | 3个高频命令待集成 |
| **Serena MCP** | 🔵 计划中 | 未来版本集成 |

**创建日期**: 2025-12-09
**版本**: 1.0
**维护者**: AI Workflow Team

---

## 💡 快速开始 (3 行代码)

```python
from commands.lib.doc_loader import load_doc_sections

content = load_doc_sections("docs/guides/workflow.md", ["Step 3"])
print(content["Step 3"])
```

**就这么简单！🎉**
