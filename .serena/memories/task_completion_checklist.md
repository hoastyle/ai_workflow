# 任务完成清单 (Task Completion Checklist)

## 代码修改后

- [ ] Python 代码遵循 PEP 8
- [ ] 所有公共函数有 docstrings 和 type hints
- [ ] 错误处理完善
- [ ] 测试通过
- [ ] Git 提交: `git add <files> && git commit -m "[type] 描述"`

## 文档更新后

- [ ] Frontmatter 验证: `python scripts/frontmatter_utils.py validate <file>`
- [ ] 必需字段: title, description, type, status, priority, created_date, last_updated
- [ ] 文档大小: 管理层<200行, 技术层<500行
- [ ] 在 KNOWLEDGE.md 中添加条目
- [ ] 链接检查和交叉引用更新

## 创建 ADR 时

- [ ] 使用模板: `cp docs/adr/TEMPLATE.md docs/adr/$(date +%Y-%m-%d)-topic.md`
- [ ] 必须包含: 背景、决策、候选方案、权衡、实施
- [ ] 更新 docs/adr/README.md 和 KNOWLEDGE.md

## 发布版本时

- [ ] 更新版本号：CLAUDE_KBASE.md, KNOWLEDGE.md, install_knowledge_base.sh
- [ ] 测试安装: `bash scripts/install_knowledge_base.sh`
- [ ] Git 标签: `git tag -a vX.Y.Z -m "Version X.Y.Z"` && `git push origin vX.Y.Z`