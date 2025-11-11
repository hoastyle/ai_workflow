# Scripts 目录

自动化工具脚本集合，用于处理项目文档元数据和关系图。

## 📦 脚本清单

| 脚本 | 功能 | 主要用途 |
|------|------|---------|
| **frontmatter_utils.py** | Frontmatter 处理核心工具 | 验证、生成、关系图构建 |
| **doc_graph_builder.py** | 文档关系图生成器 | 可视化文档关系网络 |

## 🚀 快速开始

### 安装依赖

```bash
pip install pyyaml
```

### 常用命令

```bash
# 验证文档 frontmatter
python scripts/frontmatter_utils.py validate docs/api/auth.md

# 批量验证
python scripts/frontmatter_utils.py validate-batch docs/

# 生成模板
python scripts/frontmatter_utils.py generate docs/api/new-doc.md

# 生成关系图
python scripts/doc_graph_builder.py docs/ --format mermaid > docs/graph.mmd
```

## 📚 详细文档

完整的使用指南请参考：
- [Frontmatter 元数据规范](../docs/reference/FRONTMATTER.md)
- [工作流命令文档](../COMMANDS.md)

## 🔧 维护说明

这些脚本由 Claude Code 自动生成和维护：
- **生成源**: docs/reference/FRONTMATTER.md
- **更新方式**: 通过 /wf_14_doc 和 /wf_13_doc_maintain 命令
- **版本控制**: 随项目一起进行 Git 版本控制

⚠️ **注意**: 不建议手动修改这些脚本。如需更新，请修改源文档并重新生成。

## 💡 Token 效率

使用这些脚本相比动态执行代码可节省 **97.5% 的 Token 消耗**：

- 单次验证：8000 → 200 tokens
- 批量验证：50000 → 500 tokens
- 关系图生成：12000 → 300 tokens

---

**版本**: 1.0
**最后更新**: 2025-11-11
**维护者**: Claude Code
