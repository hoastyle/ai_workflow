---
title: "Frontmatter 快速参考"
description: "Frontmatter 字段定义和常用示例，快速查询和复制"
type: "API参考"
status: "完成"
priority: "中"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/reference/FRONTMATTER.md"
  - "docs/examples/doc_generation_quick_guide.md"
related_code:
  - "scripts/frontmatter_utils.py"
tags: ["Frontmatter", "元数据", "模板"]
---

# Frontmatter 快速参考

## 必需字段（7个）

```yaml
---
title: "文档标题"
description: "一句话描述"
type: "类型"
status: "状态"
priority: "优先级"
created_date: "2025-11-24"
last_updated: "2025-11-24"
---
```

## 字段详解

### title
- **说明**: 文档标题
- **格式**: 字符串，不超过 80 字
- **示例**: `"用户管理 API 端点"`

### description
- **说明**: 一句话描述核心内容
- **格式**: 字符串，不超过 150 字
- **示例**: `"用户 CRUD 操作的 REST API 完整参考"`

### type
- **说明**: 文档类型（枚举）
- **有效值**:
  - `技术设计` - 系统或功能设计
  - `系统集成` - 第三方或模块集成
  - `API参考` - API 或配置参考
  - `教程` - 使用指南或最佳实践
  - `故障排查` - 问题诊断或错误处理
  - `架构决策` - 重大技术选择（ADR）
- **示例**: `type: "API参考"`

### status
- **说明**: 文档状态（枚举）
- **有效值**:
  - `草稿` - 初稿，内容可能变化
  - `完成` - 完成并验证
  - `待审查` - 等待审查意见
- **示例**: `status: "完成"`

### priority
- **说明**: 文档优先级（枚举）
- **有效值**:
  - `高` - 多人依赖，更新频繁
  - `中` - 部分人依赖，定期更新
  - `低` - 个人参考，不常更新
- **示例**: `priority: "高"`

### created_date
- **说明**: 文档创建日期
- **格式**: ISO 日期（YYYY-MM-DD）
- **注意**: 创建后永不修改
- **示例**: `created_date: "2025-11-24"`

### last_updated
- **说明**: 文档最后更新日期
- **格式**: ISO 日期（YYYY-MM-DD）
- **注意**: 每次编辑自动更新
- **示例**: `last_updated: "2025-11-24"`

## 推荐字段（2个）

### related_documents
- **说明**: 相关文档路径列表
- **格式**: 数组，使用相对路径
- **最多**: 3-5 个（过多表示设计有问题）
- **示例**:
```yaml
related_documents:
  - "docs/api/authentication.md"
  - "docs/adr/2025-11-24-api-design.md"
  - "KNOWLEDGE.md"
```

### related_code
- **说明**: 实现代码路径列表
- **格式**: 数组，指向代码目录或文件
- **示例**:
```yaml
related_code:
  - "src/api/users/"
  - "tests/api/test_users.py"
```

## 可选字段

### tags
- **说明**: 文档标签（用于分类和搜索）
- **格式**: 字符串数组
- **示例**: `tags: ["API", "认证", "安全"]`

### authors
- **说明**: 文档作者或贡献者
- **格式**: 字符串数组
- **示例**: `authors: ["Claude", "张三"]`

### version
- **说明**: 文档版本号
- **格式**: 版本号（如 1.0、1.1、2.0）
- **示例**: `version: "2.1"`

## 常用模板

### API 文档模板
```yaml
---
title: "XXX API 端点"
description: "XXX 的 REST API 完整参考，包含端点、参数和错误处理"
type: "API参考"
status: "完成"
priority: "高"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/api/authentication.md"
  - "docs/api/errors.md"
related_code:
  - "src/api/xxx/"
  - "tests/api/test_xxx.py"
tags: ["API", "XXX"]
version: "1.0"
---
```

### 架构决策（ADR）模板
```yaml
---
title: "选择 XXX 而非 YYY"
description: "权衡分析 XXX 和 YYY，最终选择 XXX"
type: "架构决策"
status: "完成"
priority: "高"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/technical/xxx-implementation.md"
related_code:
  - "config/xxx-config.yaml"
tags: ["架构", "技术选型"]
---
```

### 教程模板
```yaml
---
title: "XXX 快速开始"
description: "5 分钟内学会如何使用 XXX，包含完整代码示例"
type: "教程"
status: "完成"
priority: "中"
created_date: "2025-11-24"
last_updated: "2025-11-24"
related_documents:
  - "docs/api/xxx.md"
related_code:
  - "examples/xxx_quickstart.py"
  - "tests/xxx/test_quickstart.py"
tags: ["教程", "快速开始"]
---
```

## 常见错误

### ❌ 错误：错误的路径格式
```yaml
# 错误
related_documents:
  - "/home/user/project/docs/api.md"

# 正确
related_documents:
  - "docs/api/auth.md"
```

### ❌ 错误：枚举值不标准
```yaml
# 错误
type: "API 文档"
status: "进行中"
priority: "很高"

# 正确
type: "API参考"
status: "草稿"
priority: "高"
```

### ❌ 错误：日期格式不一致
```yaml
# 错误
created_date: "2025/11/24"
last_updated: "24-11-2025"

# 正确
created_date: "2025-11-24"
last_updated: "2025-11-24"
```

### ❌ 错误：过多关联
```yaml
# 错误：10+ 个关联（太复杂）
related_documents:
  - "docs/a.md"
  - "docs/b.md"
  - ... (7 个更多)

# 正确：只列出最相关的
related_documents:
  - "docs/main.md"
  - "docs/related.md"
  - "KNOWLEDGE.md"
```

## 快速生成工具

### 自动生成 Frontmatter
```bash
# 单个文档
python ~/.claude/commands/scripts/frontmatter_utils.py generate docs/new.md

# 批量生成
python ~/.claude/commands/scripts/frontmatter_utils.py generate-batch docs/
```

### 验证 Frontmatter
```bash
# 单个验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate docs/file.md

# 批量验证
python ~/.claude/commands/scripts/frontmatter_utils.py validate-batch docs/
```

### 更新索引
```bash
# 更新 KNOWLEDGE.md
python ~/.claude/commands/scripts/frontmatter_utils.py update-index KNOWLEDGE.md
```

## 验证清单

生成文档后检查：

- [ ] title：不超过 80 字，清晰准确
- [ ] description：一句话，不超过 150 字
- [ ] type：选择正确的枚举值
- [ ] status：通常为"完成"或"草稿"
- [ ] priority：根据影响范围判定
- [ ] created_date：使用创建当天的日期
- [ ] last_updated：使用修改当天的日期
- [ ] related_documents：最多 3-5 个，路径正确
- [ ] related_code：指向实现代码

---

**相关文档**：
- 完整规范 → [docs/reference/FRONTMATTER.md](../../reference/FRONTMATTER.md)
- 详细示例 → [docs/examples/](.)
- 快速指南 → [doc_generation_quick_guide.md](doc_generation_quick_guide.md)

**版本**: v1.0 | **更新**: 2025-11-24
