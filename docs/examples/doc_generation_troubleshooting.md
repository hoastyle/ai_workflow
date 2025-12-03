# /wf_14_doc 故障排查和限制说明

本文档说明 `/wf_14_doc` 命令的当前限制和常见问题解决方案。

---

## 当前限制

### 1. 语言支持

**主要支持** (完整特性):
- Python (FastAPI, Flask, Django)
- JavaScript/TypeScript (Express, Next.js)
- Rust (Actix, Rocket)
- Go (Gin, Echo)

**部分支持** (基础特性):
- Java (Spring)
- C# (.NET Core)
- Ruby (Rails)

**不支持**:
- 冷门语言和框架
- 自定义 DSL
- 非标准项目结构

---

### 2. 框架支持

#### Web 框架
- ✅ FastAPI, Express, Flask, Django, Spring
- ⚠️ 自定义框架需要手动配置提取规则

#### CLI 框架
- ✅ Click, Clap, Commander
- ⚠️ 自定义 CLI 需要补充文档

#### 其他框架
- 需要手动完善或提供配置文件
- 支持通过插件扩展

---

### 3. 提取准确性

**依赖因素**:
- 代码注释和类型注解的质量
- 路由定义的标准性
- 配置文件的规范性

**已知限制**:
- ❌ 动态生成的端点可能遗漏
- ❌ 运行时配置难以提取
- ❌ 复杂的配置可能需要人工补充

---

## 常见问题解决方案

### Q1: 为什么某些端点没有被提取到？

**可能原因**:
- 端点是动态生成的
- 路由定义在非标准位置
- 使用了自定义装饰器

**解决方法**:
1. 手动补充到文档中
2. 在代码中添加更多注释：
   ```python
   @app.post("/api/users")  # 创建用户 API
   async def create_user(user: UserCreate):
       """
       创建新用户

       Args:
           user: 用户创建请求
       Returns:
           User: 创建的用户对象
       """
       pass
   ```
3. 使用标准的路由定义模式

---

### Q2: 生成的文档风格不一致怎么办？

**原因分析**:
- 现有文档示例不足（少于 3 个参考文档）
- 项目中使用了多种文档风格
- 没有明确的文档风格指南

**解决方法**:

**方法 1 - 提供参考文档**:
确保项目中有至少 3-5 个风格一致的参考文档，AI 会学习这些文档的风格。

**方法 2 - 首次生成后手动调整**:
```bash
# 1. 生成初始文档
/wf_14_doc --update api

# 2. 手动调整第一个文档的风格
# 编辑 docs/api/first-endpoint.md

# 3. 后续生成会学习已有文档风格
/wf_14_doc --update api
```

**方法 3 - 使用统一模板**:
```bash
/wf_14_doc --template docs/examples/doc_templates/API_template.md
```

---

### Q3: 如何自定义文档模板？

**使用现有模板**:
```bash
# 使用标准 API 模板
/wf_14_doc --template api

# 使用部署文档模板
/wf_14_doc --template deployment
```

**创建自定义模板**:

**步骤 1**: 复制标准模板
```bash
cp docs/examples/doc_templates/API_template.md docs/custom/my_template.md
```

**步骤 2**: 修改模板内容
```markdown
---
# Frontmatter 部分
title: "{{ project_name }} API 参考"
type: "API参考"
---

# {{ project_name }} API 文档

## 概览
{{ api_overview }}

## 端点列表
{% for endpoint in api_endpoints %}
### {{ endpoint.method }} {{ endpoint.path }}
{{ endpoint.description }}
{% endfor %}
```

**步骤 3**: 使用自定义模板
```bash
/wf_14_doc --template docs/custom/my_template.md
```

**模板语法**:
- 变量：`{{ variable_name }}`
- 循环：`{% for item in items %} ... {% endfor %}`
- 条件：`{% if condition %} ... {% endif %}`
- 完整语法参考：Jinja2 模板引擎

---

### Q4: 文档生成时间太长怎么办？

**问题原因**:
- 代码库过大（数千个文件）
- 全量分析所有文件
- 生成所有类型的文档

**解决方法**:

**方法 1 - 只更新特定类型**:
```bash
# 只更新 API 文档（最快）
/wf_14_doc --update api

# 只更新部署文档
/wf_14_doc --update deployment
```

**方法 2 - 限制扫描范围**:
```bash
# 只扫描 src/api/ 目录
/wf_14_doc --scope src/api/

# 排除测试和示例目录
/wf_14_doc --exclude tests/,examples/,node_modules/
```

**方法 3 - 使用缓存**:
```bash
# 启用缓存（第二次运行更快）
/wf_14_doc --cache

# 强制刷新缓存
/wf_14_doc --cache-refresh
```

**性能优化建议**:
- 首次生成：分批生成不同类型的文档
- 增量更新：只更新变更的文件
- 使用 `--update-changed` 选项

---

### Q5: 如何处理多语言项目？

**问题**:
项目包含多种编程语言，如何生成统一的文档？

**解决方法**:

**方法 1 - 分别生成**:
```bash
# 为 Python 部分生成文档
/wf_14_doc --scope backend/ --language python

# 为 JavaScript 部分生成文档
/wf_14_doc --scope frontend/ --language javascript
```

**方法 2 - 统一配置**:
创建 `.wf_14_doc_config.yaml`:
```yaml
languages:
  - python:
      scope: backend/
      frameworks: [fastapi, flask]
  - javascript:
      scope: frontend/
      frameworks: [react, next.js]
  - rust:
      scope: services/
      frameworks: [actix]

output:
  structure: unified  # 或 separated
  naming: by_service  # 或 by_language
```

**方法 3 - 使用通用模板**:
```bash
/wf_14_doc --template docs/templates/multilang_api.md
```

---

### Q6: 文档与代码不同步怎么办？

**问题**:
代码已更新，但文档没有自动更新

**预防措施**:

**1. 集成到 CI/CD**:
```yaml
# .github/workflows/docs-check.yml
name: Docs Sync Check
on: [pull_request]
jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check docs sync
        run: /wf_14_doc --check
```

**2. Pre-commit Hook**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: docs-sync-check
        name: Check docs sync
        entry: /wf_14_doc --check
        language: system
        pass_filenames: false
```

**3. 定期审查**:
```bash
# 每周运行
/wf_14_doc --check --report

# 查看报告
cat docs/sync-report.md
```

**修复方法**:
```bash
# 1. 识别过时的文档
/wf_14_doc --check --verbose

# 2. 更新特定文档
/wf_14_doc --update api

# 3. 验证同步
/wf_14_doc --check
```

---

### Q7: 如何处理敏感信息？

**问题**:
文档中不应包含密钥、密码等敏感信息

**预防措施**:

**1. 配置过滤规则**:
```yaml
# .wf_14_doc_config.yaml
filters:
  exclude_patterns:
    - ".*_KEY"
    - ".*_SECRET"
    - ".*_PASSWORD"
    - ".*_TOKEN"
  exclude_values:
    - "sk-.*"  # OpenAI keys
    - "[0-9a-f]{32}"  # MD5 hashes
```

**2. 使用占位符**:
```python
# 代码中使用占位符
API_KEY = os.getenv("API_KEY", "your-api-key-here")

# 文档会显示
API_KEY = "your-api-key-here"  # 占位符，请替换为实际值
```

**3. Post-process 检查**:
```bash
# 生成后检查敏感信息
/wf_14_doc --update api --post-check-secrets

# 手动检查
grep -r "sk-" docs/ || echo "No secrets found"
```

---

### Q8: 大型项目如何优化？

**问题**:
项目有上千个文件，文档生成很慢

**优化策略**:

**1. 分模块生成**:
```bash
# 按模块分别生成
/wf_14_doc --scope src/auth/ --output docs/auth/
/wf_14_doc --scope src/api/ --output docs/api/
/wf_14_doc --scope src/db/ --output docs/database/
```

**2. 增量生成**:
```bash
# 只生成变更的部分
/wf_14_doc --update-changed --since HEAD~10
```

**3. 并行处理**:
```bash
# 使用多个进程
/wf_14_doc --parallel --jobs 4
```

**4. 使用配置文件**:
```yaml
# .wf_14_doc_config.yaml
performance:
  cache: true
  parallel: true
  max_workers: 4
  incremental: true

scope:
  include:
    - src/
  exclude:
    - tests/
    - examples/
    - node_modules/
    - vendor/
```

---

## 未来改进方向

正在规划中的功能：

- [ ] 支持更多编程语言和框架
- [ ] 集成 OpenAPI/Swagger 自动同步
- [ ] 支持生成架构图（基于模块依赖）
- [ ] AI 驱动的文档质量评分
- [ ] 文档变更自动检测和提醒
- [ ] 实时文档预览服务器
- [ ] 多版本文档管理
- [ ] 文档国际化支持

---

**See Also**:
- [/wf_14_doc](../../wf_14_doc.md) - 命令主文档
- [文档生成最佳实践](doc_generation_best_practices.md) - 使用指南
- [文档生成工作流](doc_generation_workflow.md) - 6步流程
- [KNOWLEDGE.md](../../KNOWLEDGE.md) - 已知问题和解决方案
