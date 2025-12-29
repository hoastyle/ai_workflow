# AI 协作最佳实践

**版本**: v1.0
**日期**: 2025-12-29

---

## 🎯 核心原则

### 1. 明确的上下文管理

**每次会话开始**:
- 运行上下文加载命令（原 `/wf_03_prime`）
- 使用 CONTEXT.md 跨 `/clear` 边界保持状态
- 确认当前任务和焦点

**上下文内容**:
- 当前活跃任务
- 相关架构文档
- 相关 ADR 决策
- 会话状态（Git commits, 修改文件）

### 2. 约束驱动交互

**在 CLAUDE.md 中明确规则**:
```markdown
## 文件操作权限矩阵

| 文件 | 读取 | 创建 | 修改 | 删除 |
|------|:----:|:----:|:----:|:----:|
| PRD.md | ✅ | ❌ | ❌ | ❌ | 只读 |
| PLANNING.md | ✅ | ✅ | ✅ | ❌ | 重大决策更新 |
| TASK.md | ✅ | ✅ | ✅ | ❌ | 实时更新 |
```

**使用 Frontmatter 定义约束**:
```yaml
---
context_rules:
  - "强制语言规则: 中文"
  - "遵循项目 CLAUDE.md 的语言规范"
  - "代码注释使用中文"
---
```

### 3. 渐进式自动化

**从简单任务开始**:
1. Level 1: 代码生成和格式化
2. Level 2: 测试生成和覆盖
3. Level 3: 文档生成和维护
4. Level 4: 架构分析和重构建议

**使用 MCP 扩展能力**:
- **Serena**: 语义代码理解和项目内存
- **Context7**: 官方库文档查询
- **Sequential-thinking**: 结构化多步推理
- **Tavily**: Web 搜索和实时信息

### 4. 质量门控

**自动化检查**:
- Pre-commit hooks（尾部空格、行尾格式）
- 代码格式化（Black, Prettier）
- 链接验证（Markdown 链接）
- Frontmatter 验证（完整性检查）

**人工审查**:
- 关键决策需要确认
- 架构变更需要 ADR
- 大型重构需要讨论

---

## 📝 文档协作规范

### 文档读取保护

**防止上下文爆炸**:
```bash
# 必须先检查文档大小
lines=$(wc -l < "document.md")

# 根据大小选择策略
if [ $lines -lt 100 ]; then
    # 直接读取
elif [ $lines -lt 300 ]; then
    # 摘要模式
elif [ $lines -lt 800 ]; then
    # 章节模式（必须使用 DocLoader）
else
    # 禁止完整读取
fi
```

**加载策略**:
| 文档大小 | 策略 | Token 消耗 |
|---------|------|-----------|
| < 100 行 | 直接读取 | ~300 tokens ✅ |
| 100-300 行 | 摘要模式 | ~100 tokens ✅ |
| 300-800 行 | 章节模式 | ~400 tokens ⚠️ |
| \> 800 行 | 禁止 | ❌ |

### 文档生成约束

**三阶段门控**:
1. **Phase 1**: 代码完成后的文档决策树
2. **Phase 2**: 文档生成时的成本估计和门控
3. **Phase 3**: 审查时的架构合规性检查

**成本约束**:
- 类型 A (架构): < 50 行
- 类型 B (决策): < 200 行
- 类型 C (功能): < 500 行
- 增长率: 单次 < 30%

---

## 🔄 会话生命周期

### 会话开始时

**检查清单**:
- [ ] 是否运行了上下文加载
- [ ] 是否是新会话且未加载
- [ ] 是否是全新项目

**启动命令**:
```bash
# 标准启动
/prime-context  # 原 /wf_03_prime

# 新项目
/planning "项目描述"  # 原 /wf_01_planning
```

### 会话进行中

**决策前检查**:
- 确认是否符合需求
- 遇到模糊需求，使用架构咨询
- 不确定时主动询问

**进度追踪**:
- 完成任务后，主动更新任务文档
- 做重大技术决策后，更新技术规划

### 会话结束前

**保存进度**:
- 提醒运行提交命令
- 这会自动更新上下文文档
- 确保下次会话能恢复工作状态

---

## 🛠️ 工具和命令

### MCP 工具集成

**可用 MCP 服务器**:
- **Serena**: 语义代码理解、符号操作、项目内存
- **Context7**: 官方库文档查询
- **Sequential-thinking**: 结构化多步推理
- **Tavily**: Web 搜索和实时信息
- **Magic**: UI 组件生成

**使用示例**:
```python
# 通过 Gateway 使用 MCP
from src.mcp.gateway import get_mcp_gateway

gateway = get_mcp_gateway()
if gateway.is_available("serena"):
    tool = gateway.get_tool("serena", "find_symbol")
    result = tool.call(name="MyClass")
```

### 文档加载工具

**DocLoader 工具**:
```python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 摘要模式（100-300行）
summary = loader.load_summary(doc_path, max_lines=50)

# 章节模式（300-800行）
content = loader.load_sections(
    doc_path,
    sections=["Step 3", "MCP Integration"]
)
```

---

## 🎯 应用场景

### 场景 1: 技术选型

**流程**:
1. 明确需求和约束
2. 使用 MCP 查询官方文档
3. 列举 3 个以上开源方案
4. 分析优缺点和权衡
5. 记录决策到 ADR
6. 通过 PoC 验证

### 场景 2: 代码实现

**流程**:
1. 加载项目上下文
2. 确认需求和设计
3. 使用 AI 生成代码
4. 编写测试
5. 代码审查
6. 提交代码

### 场景 3: 文档生成

**流程**:
1. 使用文档决策树确定类型
2. 估计成本和检查约束
3. 生成文档和 Frontmatter
4. 更新索引
5. 验证一致性

---

## 📊 质量指标

**上下文效率**:
- 会话开始加载时间: < 1 秒
- 上下文文档总大小: < 100KB
- 80% 任务只需 0-2 个技术文档

**协作效率**:
- AI 响应准确率: > 90%
- 代码自动生成率: > 60%
- 文档自动生成率: > 50%

**质量保证**:
- Pre-commit 检查通过率: 100%
- Frontmatter 完整性: 100%
- 文档索引准确率: > 90%

---

**最后更新**: 2025-12-29
**相关文档**: [document-architecture.md](document-architecture.md) | [philosophy.md](philosophy.md)
