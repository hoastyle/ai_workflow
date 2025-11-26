# /wf_14_doc 文档生成最佳实践

本文档提供使用 `/wf_14_doc` 命令的最佳实践指南，包括使用时机、审查流程、更新策略和工作流集成。

---

## 1. 何时运行 /wf_14_doc

### ✅ 推荐时机

- **完成新功能实现后** - 为新功能生成 API 文档和使用指南
- **添加新 API 端点后** - 更新 API 参考文档
- **修改配置或环境变量后** - 更新部署和配置文档
- **重构架构后** - 更新架构设计文档
- **项目初始化时** - 生成完整的项目文档集

### ❌ 不推荐时机

- **代码频繁变动中** - 等代码稳定后再生成，避免文档过时
- **正在调试 bug 时** - 专注修复问题，不要分心生成文档
- **未经测试的代码** - 先确保代码质量，再生成文档

---

## 2. 文档审查和完善流程

### 核心原则

**AI 生成的文档是基础，需要人工审查和完善**

### 审查检查清单

#### 技术准确性检查
- [ ] 验证所有代码示例可运行
- [ ] 检查 API 端点 URL 和参数正确性
- [ ] 确认配置选项和环境变量名称准确
- [ ] 验证技术栈版本信息最新

#### 内容完整性检查
- [ ] 添加业务背景和使用场景说明
- [ ] 补充最佳实践和注意事项
- [ ] 添加常见错误和解决方案
- [ ] 提供完整的示例代码（不仅是代码片段）

#### 可读性检查
- [ ] 确保结构清晰，章节层次合理
- [ ] 添加必要的图表和流程图
- [ ] 使用一致的术语和命名
- [ ] 提供目录和交叉引用链接

#### Frontmatter 验证
```bash
# 验证单个文档
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/api/new-endpoint.md

# 批量验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/
```

---

## 3. 增量更新策略

### 核心原则

**不要全量重新生成，使用增量更新**

### 推荐做法

```bash
# ✅ 只更新 API 文档
/wf_14_doc --update api

# ✅ 只更新部署文档
/wf_14_doc --update deployment

# ✅ 只更新开发指南
/wf_14_doc --update dev
```

### 避免做法

```bash
# ❌ 重新生成所有文档（除非重大重构）
/wf_14_doc --auto
```

### 何时使用全量生成

- 项目初始化，首次生成文档
- 重大架构重构，需要更新所有文档
- 技术栈升级，影响多个文档类型
- 季度文档审查和更新

---

## 4. 工作流集成

### 标准开发流程

```bash
# 完整的功能开发流程
/wf_05_code "实现新功能"        # 实现功能
/wf_07_test "测试新功能"        # 编写测试
/wf_08_review                   # 代码审查
/wf_14_doc --update api         # 生成/更新文档
/wf_13_doc_maintain             # 维护文档结构
/wf_11_commit "完成新功能"      # 提交代码和文档
```

### 文档优先流程（推荐）

```bash
# 先设计文档，后实现代码
/wf_14_doc --template api       # 基于模板创建 API 文档草稿
# 手动完善 API 设计文档
/wf_05_code "实现已设计的 API" # 按照文档实现代码
/wf_07_test                     # 测试
/wf_14_doc --update api         # 更新文档（补充实现细节）
/wf_11_commit                   # 提交
```

### CI/CD 集成

```bash
# 在 CI 流程中检查文档同步
/wf_14_doc --check

# 返回状态码：
# 0 = 文档与代码同步
# 1 = 存在文档缺口
```

---

## 5. 文档质量保证

### 自动验证

```bash
# 1. Frontmatter 完整性
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/

# 2. Markdown 链接有效性
pre-commit run --all-files markdown-link-check

# 3. 代码示例语法检查
pre-commit run --all-files check-code-blocks
```

### 人工审查要点

1. **准确性** - 技术细节正确，代码示例可运行
2. **完整性** - 覆盖所有使用场景，提供足够的上下文
3. **可维护性** - 结构清晰，易于后续更新
4. **一致性** - 术语、格式、风格统一

---

## 6. 常见问题和解决方案

### Q: 为什么某些端点没有被提取到？

**原因**：
- 端点是动态生成的
- 路由定义在非标准位置
- 使用了自定义装饰器

**解决方法**：
- 手动补充到文档中
- 在代码中添加更多注释和类型注解
- 使用标准的路由定义模式

---

### Q: 生成的文档风格不一致怎么办？

**原因**：
- 现有文档示例不足
- 项目中使用了多种文档风格

**解决方法**：
- 确保项目中有至少 3-5 个参考文档
- 第一次生成后手动调整风格
- 后续生成会学习已有文档的风格
- 使用 `--template` 参数指定统一模板

---

### Q: 如何自定义文档模板？

**方法 1 - 使用现有模板**：
```bash
/wf_14_doc --template api
/wf_14_doc --template deployment
```

**方法 2 - 创建自定义模板**：
1. 复制 `docs/examples/doc_templates/` 中的模板
2. 修改为项目特定的结构
3. 使用 `--template /path/to/custom_template.md`

**模板语法**：
- 使用 Jinja2 语法
- 变量：`{{ project_name }}`, `{{ tech_stack }}`, `{{ api_endpoints }}`
- 控制流：`{% if %}`, `{% for %}`

---

### Q: 文档生成时间太长怎么办？

**原因**：
- 代码库过大
- 分析所有文件耗时
- 生成所有类型的文档

**解决方法**：
```bash
# 只更新特定类型
/wf_14_doc --update api

# 限制扫描范围
/wf_14_doc --scope src/api/

# 跳过某些目录
/wf_14_doc --exclude tests/,examples/
```

---

## 7. 性能优化建议

### 首次生成优化

```bash
# 1. 分批生成（按优先级）
/wf_14_doc --update overview    # 先生成项目概览
/wf_14_doc --update api          # 再生成 API 文档
/wf_14_doc --update deployment   # 最后生成部署文档

# 2. 使用缓存（第二次运行会更快）
/wf_14_doc --cache

# 3. 并行处理（如果支持）
/wf_14_doc --parallel --jobs 4
```

### 增量更新优化

```bash
# 只更新变更的文件
/wf_14_doc --update-changed

# 基于 Git diff 生成
/wf_14_doc --since HEAD~5
```

---

## 8. 文档维护最佳实践

### 定期审查

- **每月审查** - 检查文档是否与代码同步
- **每季度更新** - 重新生成过时的文档
- **版本发布前** - 确保文档完整准确

### 使用文档维护命令

```bash
# 每 10 次提交后运行
/wf_13_doc_maintain --auto

# 季度末执行
/wf_13_doc_maintain --archive-old

# 清理孤立文档
/wf_13_doc_maintain --clean-orphans
```

---

## 9. 团队协作建议

### 文档所有权

- 为每个文档指定维护者（使用 Frontmatter `authors` 字段）
- 定期轮换文档维护责任
- 使用 Code Owners 文件管理文档审查

### 文档审查流程

```bash
# 1. 生成文档
/wf_14_doc --update api

# 2. 自检
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/api/

# 3. 提交 PR
git add docs/
git commit -m "docs: update API documentation"
git push origin feature/update-docs

# 4. 团队审查
# 等待团队成员审查和批准

# 5. 合并后维护
/wf_13_doc_maintain --auto
```

---

**See Also**:
- [/wf_14_doc](../../wf_14_doc.md) - 命令主文档
- [文档生成工作流](doc_generation_workflow.md) - 6步流程
- [文档生成后续步骤](doc_generation_next_steps.md) - 完成后的路径选择
- [Frontmatter 规范](../reference/FRONTMATTER.md) - 元数据标准
