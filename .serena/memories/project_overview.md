# AI 工具知识库 (ai_workflow) - 项目概览

**版本**: v2.2 (Claude Code 优先 + CLAUDE.md 分离)
**项目类型**: AI 工具知识库和最佳实践集合
**主要定位**: 为 Claude Code 提供设计哲学、最佳实践、MCP 集成指南和工具库
**最后更新**: 2025-12-30

## 项目定位

### 历史演变
- v1.0-v3.4: Workflow 命令系统（14 个 wf_* 命令）
- v4.0+ (2025-12): 转型为 AI 工具知识库

### 当前角色
为 Claude Code 和 AI 辅助开发提供：
1. **设计哲学和原则** - Ultrathink 设计思维框架（6 个核心原则）
2. **开发最佳实践** - 文档架构、AI 协作模式、代码质量规范
3. **MCP 集成经验** - Model Context Protocol 的使用指南和故障排查
4. **AIRIS MCP Gateway** - 统一访问 13 个 MCP 服务器的 112 个工具
5. **架构决策记录** - 17 个技术决策的"为什么"和权衡
6. **工具和脚本** - DocLoader、AgentCoordinator 等可复用工具

## 核心内容区域

| 区域 | 路径 | 说明 |
|------|------|------|
| **最佳实践** | best-practices/ | 设计哲学、文档架构、AI 协作模式 |
| **MCP 集成** | mcp-integration/ | MCP 服务器使用指南和故障排查 |
| **架构决策** | docs/adr/ | 17 个架构决策记录 (ADR) |
| **AIRIS Gateway文档** | docs/airis-mcp-gateway/ | 完整的 Gateway 使用指南 |
| **参考文档** | docs/reference/ | Frontmatter、Markdown 格式等规范 |
| **工具库** | commands/lib/ | DocLoader、AgentCoordinator 等工具 |
| **实用脚本** | scripts/ | 安装、验证、文档保护工具 |
| **归档内容** | archive/ | 历史 workflow 命令和文档 |

## 知识库统计

| 类型 | 数量 |
|------|------|
| 最佳实践文档 | 4 |
| MCP 集成文档 | 15+ |
| AIRIS MCP Gateway 文档 | 13 (NEW: +2) |
| 架构决策记录 | 17 |
| 参考文档 | 3 |
| 工具库 | 5+ |
| 归档文档 | 30+ |

## 最新更新 (2025-12-30)

### 新增文档
1. **PARAMETER_TRAPS.md** (3,300+ 行)
   - MCP 工具参数陷阱速查
   - 覆盖 9 个 MCP 服务器的常见参数错误
   - 包含错误示例、正确用法、验证方法

2. **TROUBLESHOOTING.md 更新**
   - 新增"问题 5: 参数验证错误"章节
   - 高频参数陷阱速查表
   - 链接到 PARAMETER_TRAPS.md

### 文档整合
- 更新 DOCUMENTATION_GAP_ANALYSIS.md
- 更新 KNOWLEDGE.md 索引
- 消除重复内容，职责分离

## 项目价值

- **设计思维**: Ultrathink 六大原则指导架构决策
- **约束驱动**: 文档生成三阶段门控防止内容爆炸
- **MCP 集成**: 统一访问 112 个 MCP 工具的完整指南
- **参数陷阱文档**: 避免 90% 的常见参数命名错误
- **实践导向**: 所有内容来自真实项目经验，而非理论

**主要用户**: Claude Code、AI 开发者、架构师