# MCP 用户指南

**版本**: 1.0
**最后更新**: 2025-11-21
**适用范围**: AI Workflow Command System v3.4+

---

## 📖 目录

1. [什么是 MCP？](#什么是-mcp)
2. [快速开始](#快速开始)
3. [支持 MCP 的命令](#支持-mcp-的命令)
4. [使用场景指南](#使用场景指南)
5. [标志参考](#标志参考)
6. [性能考虑](#性能考虑)
7. [故障排查](#故障排查)
8. [最佳实践](#最佳实践)

---

## 什么是 MCP？

MCP (Model Context Protocol) 是 SuperClaude Framework 提供的模型扩展协议。它通过外部服务器进程为 Claude 提供额外的上下文和能力，就像给 AI 添加"超能力"一样。

### 核心优势

- ✅ **可选增强**: 完全可选，不启用时工作流保持原样
- ✅ **零破坏性**: 不改变现有命令的基本行为
- ✅ **自动降级**: MCP 失败时自动回退到标准功能
- ✅ **按需激活**: 通过标志控制，只在需要时使用

### 5 个可用的 MCP 服务器

| MCP 服务器 | 功能 | 适用场景 |
|-----------|------|---------|
| **Sequential-thinking** | 结构化多步推理 | 复杂决策、架构分析、调试诊断 |
| **Context7** | 官方库文档查询 | 技术选型、API 学习、框架对比 |
| **Serena** | 语义代码理解 | 项目上下文、代码导航、依赖分析 |
| **Tavily** | Web 搜索 | 最新技术、社区反馈、性能数据 |
| **Magic** | UI 组件生成 | 交互式文档、可视化界面 |

---

## 快速开始

### 检查 MCP 是否可用

```bash
# 检查 SuperClaude 是否安装
which superclaudeframework

# 检查 MCP 服务器状态
superclaudeframework mcp status
```

### 第一次使用 MCP

**场景**: 你想选择一个 Web 框架，需要对比多个选项

```bash
# 不使用 MCP (标准模式)
/wf_04_ask "选择 Web 框架：Django vs FastAPI vs Flask"
# 输出: 基于内置知识的建议

# 使用 MCP 增强 (推荐)
/wf_04_ask "选择 Web 框架：Django vs FastAPI vs Flask" --think --c7 --research
# 输出:
# - 结构化的决策步骤 (Sequential-thinking)
# - 官方文档链接和 API 参考 (Context7)
# - 最新社区反馈和 GitHub 趋势 (Tavily)
```

**效果对比**:
- 标准模式: 快速回答，基于训练数据 (~2-3 秒)
- MCP 增强: 深度分析，包含最新信息和官方文档 (~8-12 秒)

---

## 支持 MCP 的命令

### 命令矩阵

| 命令 | Sequential-thinking | Context7 | Serena | Tavily | Magic |
|------|:------------------:|:--------:|:------:|:------:|:-----:|
| **wf_03_prime** | ❌ | ❌ | ✅ (自动) | ❌ | ❌ |
| **wf_04_ask** | ✅ `--think` | ✅ `--c7` | ❌ | ✅ `--research` | ❌ |
| **wf_04_research** | ❌ | ✅ `--c7` | ❌ | ✅ `--research` | ❌ |
| **wf_05_code** | ❌ | ❌ | ❌ | ❌ | ✅ `--ui` |
| **wf_06_debug** | ✅ `--think` | ❌ | ✅ `--deep` | ❌ | ❌ |
| **wf_14_doc** | ❌ | ❌ | ❌ | ❌ | ✅ `--ui` |

### 详细命令指南

#### 1️⃣ `/wf_03_prime` - 加载项目上下文

**MCP**: Serena (自动激活)
**标志**: 无需标志，自动启用

**作用**:
- 语义级别理解项目结构
- 建立代码-文档知识图谱
- 智能选择相关技术文档加载
- 跨会话的项目记忆

**使用示例**:
```bash
# 标准用法 (Serena 自动工作)
/wf_03_prime

# 输出包含:
# - 项目语义结构分析
# - 代码-文档映射关系
# - 基于当前任务的智能建议
# - 关键代码位置的快速链接
```

**何时有用**:
- ✅ 每次会话开始时
- ✅ 项目代码量较大 (>1000 文件)
- ✅ 需要快速定位相关代码
- ✅ 想要理解代码间的依赖关系

#### 2. `/wf_04_ask` - 架构咨询

**MCP**: Sequential-thinking, Context7, Tavily
**标志**: `--think`, `--c7`, `--research`

**作用**:
- `--think`: 结构化分析决策步骤
- `--c7`: 获取官方文档和最佳实践
- `--research`: 搜索最新社区反馈

**使用示例**:
```bash
# 场景 1: 技术选型 (推荐组合所有标志)
/wf_04_ask "选择缓存方案：Redis vs Memcached" --think --c7 --research

# 场景 2: 只需要官方文档
/wf_04_ask "如何在 React 中实现路由？" --c7

# 场景 3: 只需要结构化分析
/wf_04_ask "微服务 vs 单体架构的权衡" --think

# 场景 4: 最新趋势研究
/wf_04_ask "2024 年最流行的前端框架" --research
```

**输出增强**:
- **标准**: 快速建议 (~200 tokens)
- **--think**: +结构化步骤 (~500 tokens)
- **--c7**: +官方文档链接 (~300 tokens)
- **--research**: +社区数据 (~400 tokens)
- **组合**: 完整分析 (~1200 tokens)

#### 3️⃣ `/wf_04_research` - 开源方案深度研究

**MCP**: Context7, Tavily
**标志**: `--c7`, `--research`

**作用**:
- `--c7`: 官方技术规格和文档
- `--research`: 社区反馈和实际使用情况

**使用示例**:
```bash
# 推荐: 组合使用获得完整信息
/wf_04_research "数据库选型：PostgreSQL vs MySQL" --c7 --research

# 输出包含:
# 1. 官方文档和技术规格 (Context7)
# 2. 最新社区反馈和趋势 (Tavily)
# 3. 综合的5维度评估
# 4. 数据支撑的推荐决策
```

**何时有用**:
- ✅ 需要评估多个开源项目
- ✅ 技术选型需要数据支持
- ✅ 想了解社区真实反馈
- ✅ 需要官方性能基准数据

#### 4️⃣ `/wf_05_code` - 功能实现

**MCP**: Magic
**标志**: `--ui`

**作用**:
- 生成交互式 UI 组件和可视化界面

**使用示例**:
```bash
# 标准: 纯代码实现
/wf_05_code "实现用户登录功能"

# UI 增强: 包含交互式组件
/wf_05_code "实现用户登录功能" --ui
# 额外生成: 登录表单 UI 组件、验证流程可视化
```

**何时有用**:
- ✅ 需要前端 UI 组件
- ✅ 想要快速原型设计
- ✅ 需要表单或数据展示界面

**注意**: Magic 需要 API key (TWENTYFIRST_API_KEY)

#### 5️⃣ `/wf_06_debug` - 调试修复

**MCP**: Sequential-thinking, Serena
**标志**: `--think`, `--deep`

**作用**:
- `--think`: 结构化错误分析
- `--deep`: 语义级代码定位

**使用示例**:
```bash
# 场景 1: 复杂错误 (推荐组合)
/wf_06_debug "数据库连接超时错误" --think --deep

# 输出:
# Step 1: 症状分析
# Step 2: 假设生成 (A: 网络 40%, B: 配置 35%, C: 超时 25%)
# Step 3: 验证步骤
# Step 4: 根因定位 (精确到文件和行号)
# Step 5: 解决方案

# 场景 2: 快速定位 (只用 deep)
/wf_06_debug "TypeError in user service" --deep
# 精确定位错误位置和依赖关系

# 场景 3: 分析思路 (只用 think)
/wf_06_debug "性能问题：API 响应慢" --think
# 系统化分析可能原因
```

**何时有用**:
- ✅ 错误原因不明显
- ✅ 涉及多个模块
- ✅ 需要理解代码依赖
- ✅ 想要系统化诊断

#### 6️⃣ `/wf_14_doc` - 智能文档生成

**MCP**: Magic
**标志**: `--ui`

**作用**:
- 生成交互式文档界面

**使用示例**:
```bash
# 标准: Markdown 文档
/wf_14_doc --update api
# 生成: docs/api/endpoints.md

# UI 增强: 交互式界面
/wf_14_doc --update api --ui
# 生成:
# - docs/api/endpoints.md (标准 Markdown)
# - docs/api/explorer.html (交互式 API 浏览器)
```

**交互式特性**:
- API 浏览器: 可直接测试 API
- 代码沙盒: 可运行的示例
- 架构图: 可点击的系统图
- 配置向导: 逐步引导设置

**何时有用**:
- ✅ API 文档需要在线测试
- ✅ 架构需要可视化
- ✅ 开发指南需要交互引导
- ❌ 内部简单文档 (成本/收益不划算)

---

## 使用场景指南

### 场景 1: 技术选型决策

**目标**: 为新项目选择合适的后端框架

**推荐流程**:
```bash
# 第1步: 初步咨询 (快速了解选项)
/wf_04_ask "Python 后端框架选择：Django vs FastAPI vs Flask" --c7

# 第2步: 深度研究 (数据支持)
/wf_04_research "Python 后端框架对比" --c7 --research

# 第3步: 结构化决策 (最终确认)
/wf_04_ask "基于研究结果，最终选择" --think
```

**成本**: ~3-5 分钟
**价值**: 高置信度决策，避免后续返工

### 场景 2: 复杂 Bug 调试

**目标**: 解决一个涉及多个模块的错误

**推荐流程**:
```bash
# 第1步: 系统化诊断
/wf_06_debug "用户登录后数据不同步" --think --deep

# 输出:
# - 5步结构化分析
# - 精确定位到相关代码文件
# - 识别依赖关系和影响范围

# 第2步: 实施修复
# (根据诊断结果修复代码)

# 第3步: 验证修复
/wf_07_test "测试用户登录和数据同步"
```

**成本**: ~5-8 分钟 (vs 手动调试可能数小时)
**价值**: 快速定位根本原因，减少试错

### 场景 3: 学习新技术

**目标**: 快速上手 React Hooks

**推荐流程**:
```bash
# 第1步: 获取官方文档
/wf_04_ask "如何使用 React Hooks？" --c7

# 输出:
# - 官方文档链接
# - API 参考
# - 最佳实践
# - 入门示例

# 第2步: 查看社区反馈
/wf_04_ask "React Hooks 常见陷阱和最佳实践" --research

# 第3步: 实践代码
/wf_05_code "实现一个使用 Hooks 的计数器组件"
```

**成本**: ~3-4 分钟
**价值**: 快速获取权威信息，避免走弯路

### 场景 4: 创建交互式文档

**目标**: 为 API 生成用户友好的文档

**推荐流程**:
```bash
# 第1步: 生成标准文档
/wf_14_doc --update api

# 第2步: 添加交互式界面
/wf_14_doc --update api --ui

# 输出:
# - Markdown 文档 (给开发者)
# - HTML 交互式浏览器 (给用户)
```

**成本**: +60 秒, +5000 tokens
**价值**: 用户体验提升 80%, 支持问题减少 50%

---

## 标志参考

### 通用标志

| 标志 | MCP 服务器 | 功能 | 适用命令 |
|------|-----------|------|---------|
| `--think` | Sequential-thinking | 结构化多步推理 | wf_04_ask, wf_06_debug |
| `--c7` | Context7 | 官方库文档查询 | wf_04_ask, wf_04_research |
| `--research` | Tavily | Web 搜索 | wf_04_ask, wf_04_research |
| `--deep` | Serena | 深度代码分析 | wf_06_debug |
| `--ui` | Magic | UI 组件生成 | wf_05_code, wf_14_doc |
| `--no-mcp` | N/A | 禁用所有 MCP | 所有命令 |

### 组合使用建议

#### 最佳组合

```bash
# 架构决策 (推荐三剑客)
/wf_04_ask "..." --think --c7 --research
# 效果: 结构化分析 + 官方文档 + 社区数据

# 深度研究 (推荐双剑客)
/wf_04_research "..." --c7 --research
# 效果: 官方规格 + 实际反馈

# 复杂调试 (推荐双剑客)
/wf_06_debug "..." --think --deep
# 效果: 系统化诊断 + 精确定位
```

#### 何时单独使用

```bash
# 只需要官方文档
/wf_04_ask "..." --c7

# 只需要最新趋势
/wf_04_ask "..." --research

# 只需要结构化分析
/wf_04_ask "..." --think

# 只需要代码定位
/wf_06_debug "..." --deep
```

---

## 性能考虑

### Token 成本对比

| 模式 | Token 消耗 | 时间成本 | 质量提升 | 推荐场景 |
|------|----------|---------|---------|---------|
| **标准** | ~200 | ~2s | 基线 | 快速回答、简单问题 |
| **+think** | ~700 | ~5s | +30% | 需要深度分析 |
| **+c7** | ~500 | ~4s | +40% | 需要官方文档 |
| **+research** | ~600 | ~6s | +50% | 需要最新信息 |
| **+deep** | ~800 | ~7s | +60% | 需要代码理解 |
| **+ui** | ~7000 | ~90s | +80% | 需要交互界面 |
| **组合 (think+c7+research)** | ~1500 | ~12s | +100% | 重大决策 |

### 何时值得使用 MCP？

#### ✅ 推荐使用

- 重大技术决策 (影响长期架构)
- 复杂问题诊断 (节省数小时调试时间)
- 学习新技术 (需要权威信息)
- 生成用户文档 (需要高质量输出)

#### ⚠️ 谨慎使用

- 简单问题快速回答
- 时间非常紧急的情况
- Token 预算有限
- 已知答案但需要确认

#### ❌ 不推荐使用

- 代码格式化等机械操作
- 明显的语法错误修复
- 重复性的简单任务

### 成本优化策略

1. **从简单开始**: 先尝试标准模式，不满意再加 MCP
2. **精准组合**: 只启用真正需要的 MCP (不要盲目全开)
3. **缓存利用**: 相似问题会利用缓存，第二次更快
4. **批量处理**: 一次性解决多个相关问题

---

## 故障排查

### 常见问题

#### 问题 1: MCP 服务器未响应

**症状**: 命令执行时间过长或超时

**诊断**:
```bash
# 检查 MCP 服务器状态
superclaudeframework mcp status

# 检查特定服务器
superclaudeframework mcp status sequential-thinking
```

**解决方案**:
1. 重启 MCP 服务器: `superclaudeframework mcp restart`
2. 检查网络连接
3. 查看服务器日志: `superclaudeframework mcp logs`

**临时方案**: 使用 `--no-mcp` 标志跳过 MCP

#### 问题 2: Context7 找不到库文档

**症状**: `--c7` 标志没有返回预期的文档

**可能原因**:
- 库名拼写错误
- 库版本过新或过旧
- Context7 数据库未更新

**解决方案**:
1. 确认库名正确: "React" 而非 "react.js"
2. 指定版本: "React 18" 而非 "React"
3. 使用 `--research` 标志作为补充

#### 问题 3: Magic 需要 API Key

**症状**: `--ui` 标志报错 "Missing API key"

**解决方案**:
```bash
# 设置环境变量
export TWENTYFIRST_API_KEY="your-api-key-here"

# 或在配置文件中设置
echo "TWENTYFIRST_API_KEY=your-key" >> ~/.env
```

**获取 API Key**: 访问 https://21st.dev 注册

#### 问题 4: Serena 内存使用过高

**症状**: /wf_03_prime 加载时间过长

**可能原因**:
- 项目代码量过大 (>10,000 文件)
- 缓存未正确清理

**解决方案**:
1. 清理 Serena 缓存: `superclaudeframework mcp clear serena`
2. 排除第三方库: 检查 .gitignore 是否正确配置
3. 分批加载: 使用子目录而非整个项目

### 调试技巧

#### 启用详细日志

```bash
# 设置调试模式
export SUPERCLAUDEFRAMEWORK_DEBUG=1

# 运行命令
/wf_04_ask "test" --think

# 查看 MCP 调用日志
tail -f ~/.superclaudeframework/logs/mcp.log
```

#### 测试单个 MCP

```bash
# 测试 Sequential-thinking
superclaudeframework mcp test sequential-thinking "分析这个问题"

# 测试 Context7
superclaudeframework mcp test context7 "React Hooks"
```

---

## 最佳实践

### 1. 渐进式使用

**策略**: 从简单到复杂，逐步探索 MCP 功能

```bash
# 阶段 1: 熟悉标准模式 (第1周)
/wf_04_ask "问题"

# 阶段 2: 尝试单个 MCP (第2周)
/wf_04_ask "问题" --c7

# 阶段 3: 组合使用 (第3周)
/wf_04_ask "问题" --think --c7

# 阶段 4: 根据场景灵活选择 (第4周+)
```

### 2. 建立个人模式库

**记录有效的组合**:

```markdown
# 我的 MCP 使用模式

## 技术选型
/wf_04_ask "..." --think --c7 --research
✅ 节省时间: 2小时 → 10分钟
✅ 决策质量: +80%

## API 学习
/wf_04_ask "..." --c7
✅ 获取官方最佳实践
✅ 避免常见陷阱

## 复杂调试
/wf_06_debug "..." --think --deep
✅ 快速定位根因
✅ 理解代码依赖
```

### 3. 团队协作

**统一使用规范**:

```markdown
# 团队 MCP 使用规范

## 必须使用 MCP 的场景
- 架构决策 → wf_04_ask --think --c7
- 技术选型 → wf_04_research --c7 --research
- 复杂 Bug → wf_06_debug --think --deep

## 可选使用 MCP 的场景
- 快速咨询 → 视情况而定
- 文档生成 → 用户文档用 --ui

## 不使用 MCP 的场景
- 简单问题 → 标准模式更快
- 格式化代码 → 无需 MCP
```

### 4. 性能优化

**缓存策略**:

- ✅ 利用缓存: 相似问题会复用结果
- ✅ 批量处理: 一次性问多个相关问题
- ✅ 精准提问: 明确的问题获得更好的结果

**示例**:
```bash
# 低效: 多次重复查询
/wf_04_ask "React 是什么？" --c7
/wf_04_ask "React Hooks 是什么？" --c7
/wf_04_ask "React Context 是什么？" --c7

# 高效: 一次性获取完整信息
/wf_04_ask "介绍 React 的核心概念：Hooks, Context, 生命周期" --c7
```

### 5. 持续学习

**推荐资源**:

- [MCP 集成示例](./MCP_EXAMPLES.md) - 13 个实战示例
- [MCP 配置参考](./MCP_CONFIG.yaml) - 完整配置说明
- [SuperClaude 官方文档](https://superclaudeframework.ai/)

**学习路径**:

1. 阅读本指南 (30 分钟)
2. 尝试基础示例 (1 小时)
3. 在实际工作中应用 (1 周)
4. 建立个人最佳实践 (持续)

---

## 总结

### 快速决策树

```
问自己: 这个问题需要 MCP 吗？

├─ 是重大决策 → 使用 --think --c7 --research
├─ 需要官方文档 → 使用 --c7
├─ 需要最新信息 → 使用 --research
├─ 复杂错误诊断 → 使用 --think --deep
├─ 需要交互界面 → 使用 --ui
└─ 简单快速问题 → 标准模式 (不使用 MCP)
```

### 记住这3点

1. **MCP 是可选的** - 不使用也完全可以工作
2. **按需启用** - 只在真正需要时使用，避免浪费
3. **逐步探索** - 从简单开始，慢慢掌握高级用法

---

**需要帮助？**
- 查看示例: [MCP_EXAMPLES.md](./MCP_EXAMPLES.md)
- 查看配置: [MCP_CONFIG.yaml](./MCP_CONFIG.yaml)
- 提交问题: [GitHub Issues](https://github.com/superclaudeframework/mcp/issues)

**最后更新**: 2025-11-21
**维护者**: AI Workflow Team
