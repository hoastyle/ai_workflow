---
title: "DocLoader 集成示例"
description: "如何在 workflow 命令中集成 DocLoader"
type: "教程"
status: "完成"
priority: "高"
created_date: "2025-12-09"
last_updated: "2025-12-09"
related_documents:
  - "docs/examples/doc_loader_usage.md"
  - "commands/lib/doc_loader.py"
related_code:
  - "commands/wf_03_prime.md"
  - "commands/wf_08_review.md"
tags: ["integration", "doc-loader", "workflow"]
authors: ["Claude"]
version: "1.0"
---

# DocLoader Workflow 集成示例

## 集成方案概览

本文档展示如何在三个高频命令中集成 DocLoader，实现渐进式优化：

| 命令 | 当前行数 | 优化目标 | Token节省 | 优先级 |
|------|---------|---------|----------|--------|
| **wf_03_prime** | 1092 | ~500 | 2k-3k | 🔴 最高 |
| **wf_08_review** | 1764 | ~800 | 3k-5k | 🔴 最高 |
| **wf_05_code** | 1158 | ~600 | 2k-4k | 🟡 高 |

**总优化潜力**: 7k-12k tokens 节省

---

## 示例 1: wf_03_prime.md 集成

### 当前问题

wf_03_prime.md (1092 行) 需要加载多个技术文档：
- docs/guides/wf_03_prime_smart_loading.md
- docs/guides/wf_03_prime_workflows.md
- docs/guides/wf_03_prime_mcp_serena.md

**问题**: 全文加载导致 ~3k tokens 消耗

### 优化方案

使用 DocLoader 按需加载相关章节：

```markdown
## Step 1.2: 智能文档加载

根据用户的工作模式，只加载相关指导：

\`\`\`python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 检测用户工作模式
if mode == "Quick Start":
    # 快速启动模式：只加载摘要
    content = loader.load_summary("docs/guides/wf_03_prime_smart_loading.md")

elif mode == "Full Context":
    # 完整上下文模式：加载关键章节
    sections = loader.load_sections(
        "docs/guides/wf_03_prime_smart_loading.md",
        sections=["Step 2: 文档分层加载", "Step 3: Token预算管理"]
    )

elif mode == "Task Focused":
    # 任务聚焦模式：根据当前任务选择章节
    if current_task == "实现功能":
        sections = ["开发实现相关文档"]
    elif current_task == "调试问题":
        sections = ["调试和故障排查"]

    content = loader.load_sections(
        "docs/guides/wf_03_prime_workflows.md",
        sections=sections
    )

# Token 估算和预算控制
estimated = loader.estimate_tokens(str(content))
print(f"📊 将加载 ~{estimated} tokens 的文档")

if estimated > 2000:
    print("⚠️ 文档较大，考虑使用摘要模式")
\`\`\`

**优化效果**:
- Quick Start: 3000 → 300 tokens (90% 节省)
- Full Context: 3000 → 800 tokens (73% 节省)
- Task Focused: 3000 → 500 tokens (83% 节省)
```

---

## 示例 2: wf_08_review.md 集成

### 当前问题

wf_08_review.md (1764 行) 包含大量嵌入式文档：
- MCP 使用指南
- 代码审查规范
- 设计模式参考

**问题**: 内容全部嵌入命令文件，导致文件过大

### 优化方案

将文档外移，使用 DocLoader 按需加载：

```markdown
## Dimension 3: 设计优雅度评审

使用 DocLoader 加载设计模式参考：

\`\`\`python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 只在需要时加载设计模式参考
if review_needs_design_patterns:
    patterns = loader.load_sections(
        "docs/reference/DESIGN_PATTERNS.md",
        sections=[
            "SOLID 原则",
            "依赖注入",
            "策略模式"
        ]
    )

    # 显示相关模式
    for pattern_name, content in patterns.items():
        print(f"### 参考: {pattern_name}")
        print(content[:500] + "...")  # 显示前500字符

# MCP 使用指南也按需加载
if code_uses_mcp:
    mcp_guide = loader.load_sections(
        "docs/integration/MCP_USAGE_GUIDE.md",
        sections=["Serena 最佳实践", "Context7 集成"]
    )
\`\`\`

**优化效果**:
- 命令文件: 1764 → ~800 行 (55% 减少)
- Token 消耗: ~5k → ~1.5k (70% 节省)
- 文档分离: 将嵌入内容移到独立文档
```

---

## 示例 3: wf_05_code.md 集成

### 当前问题

wf_05_code.md (1158 行) 包含：
- 开发流程指导
- MCP 集成文档
- 后续工作流导航

**问题**: 用户通常只需要当前步骤的指导

### 优化方案

渐进式加载，只显示当前步骤：

```markdown
## Step 3: 渐进式开发

根据开发模式动态加载文档：

\`\`\`python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 第一次：只加载当前步骤的指导
current_step = get_current_step()  # e.g., "Step 3"

workflow_guide = loader.load_sections(
    "docs/guides/wf_05_code_workflows.md",
    sections=[f"{current_step}: 渐进式开发"]
)

print(f"📖 当前步骤指导:")
print(workflow_guide[f"{current_step}: 渐进式开发"])

# 如果用户需要更多信息，再加载
if user_needs_more_context:
    additional = loader.load_sections(
        "docs/guides/wf_05_code_workflows.md",
        sections=["Step 4: 质量保证", "Step 5: 集成测试"]
    )

# Token 预算管理
cache_stats = loader.get_cache_stats()
print(f"📊 缓存状态: {cache_stats['items']} 项, "
      f"~{cache_stats['estimated_tokens']} tokens")
\`\`\`

**优化效果**:
- 初始加载: 3k → 600 tokens (80% 节省)
- 缓存命中: 0 → 90% (后续加载速度提升)
- 用户体验: 渐进式引导，避免信息过载
```

---

## 实施路线图

### 阶段 1: 基础集成 (1-2 天)

**目标**: 在 wf_03_prime.md 中集成 DocLoader

**步骤**:
1. 识别需要外移的大文档
2. 重构加载逻辑使用 DocLoader
3. 测试 3 种工作模式
4. 收集 token 消耗数据

**预期成果**:
- wf_03_prime.md: 1092 → ~500 行
- Token 节省: 2k-3k per execution

### 阶段 2: 扩展集成 (2-3 天)

**目标**: 集成到 wf_08_review.md 和 wf_05_code.md

**步骤**:
1. 将嵌入文档移到独立文件
2. 更新命令使用 DocLoader
3. 创建文档索引和导航
4. 验证功能完整性

**预期成果**:
- wf_08_review.md: 1764 → ~800 行
- wf_05_code.md: 1158 → ~600 行
- 总 token 节省: 7k-12k

### 阶段 3: 全面优化 (1 周)

**目标**: 优化所有 workflow 命令

**步骤**:
1. 分析其余 13 个命令
2. 识别优化机会
3. 批量集成 DocLoader
4. 建立最佳实践文档

**预期成果**:
- 项目总行数: 10,027 → ~5,000 行 (50% 减少)
- 平均 token 消耗: 减少 60-70%

---

## 集成检查清单

在集成 DocLoader 到每个命令时，确保：

### 功能完整性
- [ ] 所有原有功能正常工作
- [ ] 文档内容完整无遗漏
- [ ] 章节引用正确无误
- [ ] 错误处理健壮

### 性能优化
- [ ] Token 消耗降低 > 50%
- [ ] 加载速度无明显延迟
- [ ] 缓存命中率 > 80%
- [ ] 内存占用合理

### 用户体验
- [ ] 渐进式加载逻辑清晰
- [ ] 文档导航便捷
- [ ] 错误提示友好
- [ ] 调试信息充足

### 文档维护
- [ ] 外移文档有完整 Frontmatter
- [ ] 索引更新在 KNOWLEDGE.md
- [ ] 使用示例清晰
- [ ] 相关性链接正确

---

## 实际集成代码模板

### 模板 1: 基础集成

```python
#!/usr/bin/env python3
"""
Workflow command with DocLoader integration
"""

from commands.lib.doc_loader import DocLoader

def load_documentation(mode: str, task_type: str = None):
    """
    智能加载文档

    Args:
        mode: 工作模式 (quick/full/task)
        task_type: 任务类型（可选）

    Returns:
        加载的文档内容
    """
    loader = DocLoader()

    if mode == "quick":
        # 快速模式：只加载摘要
        return loader.load_summary("docs/guides/workflow_guide.md")

    elif mode == "full":
        # 完整模式：加载所有章节
        return loader.load_sections(
            "docs/guides/workflow_guide.md",
            sections=["Step 1", "Step 2", "Step 3", "Step 4"]
        )

    elif mode == "task":
        # 任务模式：根据任务类型加载
        task_sections = {
            "implementation": ["Step 3: 开发", "Step 4: 测试"],
            "debugging": ["Step 5: 调试", "Step 6: 修复"],
            "review": ["Step 7: 审查", "Step 8: 优化"]
        }

        sections = task_sections.get(task_type, ["Step 1"])
        return loader.load_sections(
            "docs/guides/workflow_guide.md",
            sections=sections
        )

    # 默认：摘要
    return loader.load_summary("docs/guides/workflow_guide.md")

# 使用示例
if __name__ == "__main__":
    docs = load_documentation(mode="task", task_type="implementation")
    print(f"Loaded {len(docs)} sections")
```

### 模板 2: 带 Token 预算控制

```python
from commands.lib.doc_loader import DocLoader

def load_with_budget(doc_path: str, sections: list, max_tokens: int = 2000):
    """
    带 token 预算控制的文档加载

    Args:
        doc_path: 文档路径
        sections: 需要的章节列表
        max_tokens: 最大 token 限制

    Returns:
        加载的内容（可能被截断）
    """
    loader = DocLoader()

    # 先尝试加载所有章节
    content = loader.load_sections(doc_path, sections)

    # 估算 token
    full_content = "\n\n".join(content.values())
    estimated = loader.estimate_tokens(full_content)

    if estimated > max_tokens:
        print(f"⚠️ 内容过大 ({estimated} tokens)，使用摘要模式")
        return loader.load_summary(doc_path)
    else:
        print(f"✅ 内容适中 ({estimated} tokens)，加载完成")
        return content

# 使用示例
content = load_with_budget(
    "docs/guides/workflow_guide.md",
    sections=["Step 1", "Step 2", "Step 3"],
    max_tokens=2000
)
```

---

## 性能监控

### Token 消耗对比

集成前后的实际数据收集：

```python
from commands.lib.doc_loader import DocLoader

def measure_optimization():
    """测量优化效果"""

    # Before: 全文加载
    with open("docs/guides/workflow_guide.md", 'r') as f:
        full_content = f.read()

    before_tokens = len(full_content) // 4

    # After: 章节加载
    loader = DocLoader()
    sections = loader.load_sections(
        "docs/guides/workflow_guide.md",
        sections=["Step 3", "Step 5"]
    )

    after_content = "\n".join(sections.values())
    after_tokens = loader.estimate_tokens(after_content)

    # 计算优化
    reduction = (before_tokens - after_tokens) / before_tokens * 100

    print(f"📊 优化效果:")
    print(f"   Before: {before_tokens} tokens")
    print(f"   After:  {after_tokens} tokens")
    print(f"   Reduction: {reduction:.1f}%")

    return {
        "before": before_tokens,
        "after": after_tokens,
        "reduction_pct": reduction
    }
```

---

## 故障排查

### 常见问题

1. **章节未找到**
   - 检查章节标题是否完全匹配
   - 使用 Grep 工具查找实际标题
   - 验证文档结构

2. **Token 估算不准**
   - 当前公式: `len(content) // 4`
   - 适用于中英混合文档
   - 纯代码文档可能偏低 10-20%

3. **缓存未命中**
   - 检查路径是否一致
   - 验证 use_cache 参数
   - 考虑清理过期缓存

---

## 相关文档

- [DocLoader 使用指南](doc_loader_usage.md)
- [DocLoader 源代码](../../commands/lib/doc_loader.py)
- [ADR: 三层架构迁移](../adr/2025-12-09-workflow-three-tier-architecture.md)

---

**创建日期**: 2025-12-09
**最后更新**: 2025-12-09
**维护者**: AI Workflow Team
