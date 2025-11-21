# MCP 集成实现指南

**版本**: v1.0
**日期**: 2025-11-21
**目的**: 逐步实现 MCP 与 AI Workflow 的集成

---

## 🚀 快速开始

### 前置条件

1. **安装 SuperClaude Framework**
   ```bash
   # 安装 SuperClaude
   pip install SuperClaude

   # 验证安装
   python3 -m SuperClaude --version
   ```

2. **安装 MCP 服务器** (自动或手动)
   ```bash
   # 自动安装所有 MCP
   SuperClaude install --mcp-all

   # 或手动安装特定 MCP
   npm install -g @anthropic-mcp/sequential-thinking
   npm install -g @anthropic-mcp/context7
   npm install -g @anthropic-mcp/serena
   # 等等...
   ```

3. **验证 MCP 安装**
   ```bash
   # 检查已安装的 MCP
   SuperClaude install --list-components | grep mcp
   ```

---

## 📍 阶段 1: 框架建立 (2-3 小时)

### 任务 1.1: 更新 CLAUDE.md

**位置**: `/home/hao/Workspace/MM/utility/ai_workflow/CLAUDE.md`

**添加内容** (在 "命令调用规则" 之后):

```markdown
## 🔌 MCP 集成和增强功能 (NEW - 2025-11-21)

### 什么是 MCP？

MCP (Model Context Protocol) 是 SuperClaude Framework 提供的模型扩展协议。它允许通过外部服务器（Node.js 进程）向 Claude 提供额外的上下文和能力。

**当前支持的 MCP 服务器**:
- **Sequential-thinking**: 结构化多步推理
- **Context7**: 官方库文档查询
- **Serena**: 语义代码理解和项目内存
- **Tavily**: Web 搜索和实时信息
- **Magic**: UI 组件生成

### MCP 激活机制

#### 显式激活 (用户标志)

某些 wf 命令支持通过标志显式启用特定 MCP：

```bash
# 启用结构化思考
/wf_04_ask "技术决策" --think

# 启用官方文档
/wf_04_ask "..." --c7

# 启用 Web 搜索
/wf_04_research "..." --research

# 启用深度代码分析
/wf_06_debug "..." --deep

# 启用 UI 生成
/wf_14_doc "..." --ui

# 组合激活
/wf_04_ask "..." --think --c7 --research
```

#### 自动激活

某些 MCP 在特定条件下自动激活：
- **Sequential-thinking**: 检测复杂决策关键词时
- **Context7**: 检测框架/库名时
- **Serena**: 在 /wf_03_prime 中加载项目上下文时

#### 禁用 MCP

用户可以通过 --no-mcp 标志禁用所有 MCP 增强（性能考虑）：

```bash
/wf_04_ask "..." --no-mcp
# 使用纯文本分析，跳过所有 MCP 调用
```

### MCP 可用性和降级

- ✅ MCP 完全可选，不启用时工作流保持原样
- ✅ 如果 MCP 未安装或不可用，自动降级到标准功能
- ✅ 用户可以选择启用或禁用 MCP 增强
- 📝 建议: 首次使用时运行 `SuperClaude install --mcp-all` 获得最佳体验

### 支持 MCP 的 wf 命令

| 命令 | 支持的 MCP | 标志 |
|------|-----------|------|
| wf_03_prime | Serena (自动) | 无 |
| wf_04_ask | Sequential-thinking, Context7, Tavily | --think, --c7, --research |
| wf_04_research | Context7, Tavily | --c7, --research |
| wf_05_code | Magic | --ui |
| wf_06_debug | Sequential-thinking, Serena | --think, --deep |
| wf_14_doc | Magic | --ui |

### 更多信息

详见:
- [MCP 集成策略报告](docs/integration/MCP_INTEGRATION_STRATEGY.md)
- [MCP 架构设计](docs/integration/MCP_ARCHITECTURE.md)
- [SuperClaude 官方文档](https://superclaudeframework.ai/)
```

---

### 任务 1.2: 创建 MCP 配置文件

**位置**: `/home/hao/Workspace/MM/utility/ai_workflow/docs/integration/MCP_CONFIG.yaml`

```yaml
# MCP 集成配置文件
# 版本: 1.0
# 日期: 2025-11-21

mcp:
  enabled: true
  auto_install: false  # 用户需要手动安装
  fallback_on_error: true  # MCP 失败时优雅降级

servers:
  sequential_thinking:
    name: "Sequential-thinking"
    purpose: "结构化多步推理和分析"
    enabled: true
    auto_activate: true
    keywords:
      - "为什么"
      - "权衡"
      - "对比"
      - "架构决策"
    manual_flags:
      - "--think"
    port: 3001
    timeout: 30

  context7:
    name: "Context7"
    purpose: "官方库文档查询"
    enabled: true
    auto_activate: true
    keywords:
      - "React"
      - "Django"
      - "Spring"
      - "FastAPI"
      - "Node.js"
      - "Rust"
      - "Go"
    manual_flags:
      - "--c7"
    port: 3002
    timeout: 15

  serena:
    name: "Serena"
    purpose: "语义代码理解和项目内存"
    enabled: true
    auto_activate: true
    activate_in_commands:
      - "wf_03_prime"
      - "wf_06_debug"
    manual_flags:
      - "--deep"
    port: 3003
    timeout: 20

  tavily:
    name: "Tavily"
    purpose: "Web 搜索和实时信息"
    enabled: true
    auto_activate: false
    manual_flags:
      - "--research"
    port: 3004
    timeout: 25
    requires_api_key: false

  magic:
    name: "Magic"
    purpose: "UI 组件生成"
    enabled: true
    auto_activate: false
    manual_flags:
      - "--ui"
    port: 3005
    timeout: 20
    requires_api_key: true
    api_key_env: "TWENTYFIRST_API_KEY"

caching:
  enabled: true
  default_ttl: 3600  # 1 小时

  ttl_by_server:
    sequential_thinking: 3600  # 1 小时
    context7: 86400  # 24 小时
    tavily: 1800  # 30 分钟
    serena: 0  # 会话级 (无缓存)
    magic: -1  # 永久缓存

performance:
  parallel_requests: true
  max_concurrent: 3
  fallback_timeout: 5

logging:
  enabled: true
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_mcp_calls: true
  log_results: true
```

---

### 任务 1.3: 创建使用示例文档

**位置**: `/home/hao/Workspace/MM/utility/ai_workflow/docs/integration/MCP_EXAMPLES.md`

创建文件包含:
```markdown
# MCP 使用示例

## 示例 1: 基础架构决策 (不使用 MCP)

\`\`\`bash
/wf_04_ask "应该使用 MongoDB 还是 PostgreSQL？"
\`\`\`

输出:
- 基于项目经验和 PLANNING.md 的建议
- 权衡分析
- 建议方案

---

## 示例 2: 深度架构决策 (使用 MCP)

\`\`\`bash
/wf_04_ask "应该使用 MongoDB 还是 PostgreSQL？" --think --c7 --research
\`\`\`

输出:
- Sequential-thinking: 多步骤分析框架
- Context7: 官方文档和最佳实践
- Tavily: 最新社区反馈
- 综合建议

---

[更多示例...]
\`\`\`

---

## 📍 阶段 2: 优先命令集成 (3-4 小时)

### 集成顺序 (按优先级)

1. **wf_04_ask** - 最高价值，最常用
2. **wf_06_debug** - 高价值，改善调试
3. **wf_04_research** - 中高价值，增强研究
4. **wf_03_prime** - 高价值，改善上下文
5. **wf_14_doc** - 中价值，改善文档

### 任务 2.1: 集成 wf_04_ask

**修改文件**: `commands/wf_04_ask.md`

**添加内容** (在 frontmatter 之后):

```markdown
## 🔌 MCP 增强能力

本命令支持以下 MCP 服务器的可选增强：

### Sequential-thinking (结构化思考)

**启用**: `--think` 标志
**用途**: 复杂架构决策时使用结构化多步推理
**自动激活**: 检测到复杂决策关键词

**示例**:
\`\`\`bash
# 启用深度思考
/wf_04_ask "选择 Web 框架" --think

# 组合启用
/wf_04_ask "..." --think --c7 --research
\`\`\`

**改进点**:
- 问题分解为清晰的步骤
- 逐步分析每个选项
- 权衡明确和可追踪
- 建议基于结构化分析

---

### Context7 (官方文档)

**启用**: `--c7` 标志或自动检测
**用途**: 获取官方框架和库的文档、API 参考、最佳实践
**自动激活**: 检测到框架/库名

**示例**:
\`\`\`bash
# 明确启用
/wf_04_ask "如何在 React 中实现路由？" --c7

# 自动启用 (检测到 React)
/wf_04_ask "React vs Vue，哪个更好？"
\`\`\`

**改进点**:
- 官方文档链接
- 官方推荐的最佳实践
- API 参考
- 版本兼容性信息

---

### Tavily (Web 搜索)

**启用**: `--research` 标志
**用途**: 搜索最新的技术发展、社区讨论、性能对比
**自动激活**: 否 (用户明确启用)

**示例**:
\`\`\`bash
/wf_04_ask "Rust vs Go for 2024" --research
\`\`\`

**改进点**:
- 最新的社区讨论
- GitHub 趋势数据
- 性能对比报告
- 新版本发布信息

---

### 组合使用

\`\`\`bash
# 全面的架构决策分析
/wf_04_ask "选择微服务框架" --think --c7 --research

# 输出包含:
# 1. 多步骤结构化分析 (Sequential-thinking)
# 2. 官方文档和最佳实践 (Context7)
# 3. 最新社区反馈 (Tavily)
# 4. 综合建议
\`\`\`

---

### 禁用 MCP

\`\`\`bash
# 使用纯文本分析，不启用任何 MCP
/wf_04_ask "..." --no-mcp
\`\`\`
```

**在命令输出部分添加**:

```markdown
## Output Format (Enhanced with MCP)

### Without MCP (default)
- **Recommendation**: Direct suggestion
- **Rationale**: Why this choice
- **Considerations**: What to keep in mind
- **Next Steps**: How to proceed

### With --think (Sequential-thinking)
- **Problem Decomposition**: Break down the decision
- **Option Analysis**: Systematic evaluation of each option
- **Trade-off Analysis**: Explicit pros/cons comparison
- **Recommendation**: Based on structured analysis

### With --c7 (Context7)
- **Official Documentation**: Links and references
- **Best Practices**: From official sources
- **API Reference**: Key details
- **Version Info**: Compatibility notes

### With --research (Tavily)
- **Community Feedback**: What developers are saying
- **Performance Data**: Latest benchmarks
- **Adoption Trends**: GitHub stars, usage stats
- **Recent Updates**: New versions, breaking changes
```

---

### 任务 2.2: 集成 wf_06_debug

**修改文件**: `commands/wf_06_debug.md`

**添加内容** (类似 wf_04_ask，但针对调试):

```markdown
## 🔌 MCP 增强能力

### Sequential-thinking (结构化诊断)

**启用**: `--think` 标志
**用途**: 系统化的问题诊断和根因分析

### Serena (深度代码分析)

**启用**: `--deep` 标志
**用途**: 语义级别的代码分析，识别性能模式和问题

**示例**:
\`\`\`bash
# 结构化诊断
/wf_06_debug "API 响应慢" --think

# 代码级分析
/wf_06_debug "内存泄漏" --deep

# 组合分析
/wf_06_debug "性能问题" --think --deep
\`\`\`
```

---

### 任务 2.3: 集成 wf_04_research 和其他命令

**类似修改**:
- `wf_04_research.md` - 添加 Context7 和 Tavily
- `wf_03_prime.md` - 自动激活 Serena
- `wf_14_doc.md` - 添加 Magic UI 生成选项

---

## 📍 阶段 3: 文档和测试 (1-2 小时)

### 任务 3.1: 创建用户指南

**位置**: `/home/hao/Workspace/MM/utility/ai_workflow/docs/integration/MCP_USER_GUIDE.md`

内容包括:
```markdown
# MCP 使用指南

## 快速开始
1. 安装 SuperClaude
2. 安装 MCP 服务器
3. 使用标志启用 MCP

## 常见问题
- MCP 没有安装怎么办？
- 如何知道 MCP 是否在工作？
- 为什么某些命令比较慢？
- 如何禁用 MCP？

## 性能优化
- 缓存策略
- 何时使用 MCP
- 何时禁用 MCP

## 故障排查
- MCP 进程不启动
- MCP 超时错误
- 网络错误
```

---

### 任务 3.2: 创建 ADR 记录

**位置**: `docs/adr/2025-11-21-mcp-integration-strategy.md`

包含:
```markdown
# ADR 2025-11-21: 集成 SuperClaude MCP 到 AI Workflow

## 背景
当前的 AI Workflow 系统是独立的，缺乏某些高级能力...

## 决策
采用"选择性增强"模式集成 5 个关键 MCP 服务器...

## 选择
- 不替代现有系统，而是增强
- 用户可选启用
- 优雅降级

## 权衡
- 优点: 大幅增强功能
- 缺点: 额外的依赖和复杂性
```

---

### 任务 3.3: 集成验证

**检查清单**:
```markdown
## 集成验证清单

### 框架验证
- [ ] CLAUDE.md 已更新
- [ ] MCP 配置文件已创建
- [ ] 示例文档已创建

### 命令验证
- [ ] wf_04_ask 支持 --think, --c7, --research
- [ ] wf_06_debug 支持 --think, --deep
- [ ] wf_04_research 支持 --research
- [ ] wf_03_prime 自动激活 Serena
- [ ] wf_14_doc 支持 --ui

### 功能验证
- [ ] 标志正确传递
- [ ] MCP 正确激活
- [ ] 结果正确集成
- [ ] 错误正确处理
- [ ] 优雅降级正常工作

### 文档验证
- [ ] 用户指南完整
- [ ] ADR 记录清晰
- [ ] 示例准确可用
- [ ] 常见问题涵盖全面
```

---

## 🎯 后续步骤

### 立即行动 (本周)

1. **审核本文档**
   - 获取团队反馈
   - 确认方案可行性

2. **准备 Phase 1**
   - 分配任务
   - 准备开发环境

3. **开始 Phase 1 实施**
   - 更新 CLAUDE.md
   - 创建配置文件
   - 创建示例

### 短期行动 (1-2 周)

1. **完成 Phase 2**
   - 集成优先命令
   - 创建使用指南
   - 进行基础测试

2. **社区反馈**
   - 让核心用户测试
   - 收集反馈意见

### 中期行动 (3-4 周)

1. **完成 Phase 3**
   - 创建全面文档
   - 创建 ADR 记录
   - 性能优化

2. **发布**
   - 更新项目 README
   - 通知用户
   - 提供迁移指南

---

## 📚 相关资源

- [MCP 集成策略报告](MCP_INTEGRATION_STRATEGY.md)
- [MCP 架构设计](MCP_ARCHITECTURE.md)
- [SuperClaude 官方文档](https://superclaudeframework.ai/)
- [当前项目 CLAUDE.md](../../CLAUDE.md)

---

**版本**: v1.0
**日期**: 2025-11-21
**作者**: Claude Code
**状态**: 就绪审核和实施
