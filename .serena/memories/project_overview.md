# AI Workflow 项目概览

## 核心定位
为 Claude Code 提供项目规划、任务管理和开发最佳实践的完整集成工作流系统

## 关键特性
- **会话连续性**: CONTEXT.md跨/clear边界保持工作状态
- **自动化追踪**: 开发周期全程自动更新TASK.md
- **质量保证**: 内置格式化、测试、代码审查
- **文档驱动**: PRD → PLANNING → TASK 完整追溯链
- **四层架构**: 管理/技术/工作/归档 + 按需加载
- **约束驱动文档** (v3.4): 从代码提取，非凭空编造

## 技术栈
| 类别 | 技术 |
|------|------|
| 核心系统 | Markdown闭环工作流 |
| 集成框架 | Claude Code Slash Commands |
| MCP服务器 | Serena, Context7, Sequential-thinking, Tavily, Magic |
| 验证系统 | pre-commit hooks，自动格式化 |
| 配置存储 | JSON (src/mcp/configs/) |

## 项目结构
```
ai_workflow/
├── wf_*.md (14个)        # 工作流命令
├── KNOWLEDGE.md          # 知识库+文档索引
├── CLAUDE.md             # AI执行规则
├── *.md (7个)            # 核心文档
├── docs/
│   ├── management/       # 管理层（5个）
│   ├── adr/              # 架构决策记录
│   ├── guides/           # 工作流指导
│   ├── examples/         # 使用示例
│   ├── reference/        # 参考文档
│   └── integration/      # MCP集成
├── scripts/              # 自动化脚本
└── src/mcp/configs/      # MCP配置
```

## 工作流命令（14个）
| 分组 | 命令 | 功能 | 关键特性 |
|------|------|------|---------|
| **基础设施** | /wf_01_planning | 项目规划 | 创建/更新PLANNING.md |
|  | /wf_02_task | 任务管理 | create/update/list |
|  | /wf_03_prime | 上下文加载 | 智能按需加载 ⭐ |
| **开发实现** | /wf_04_ask | 架构咨询 | --review-codebase, --think, --c7 |
|  | /wf_05_code | 功能实现 | Step 8文档决策树 |
|  | /wf_06_debug | 调试修复 | --quick, --deep |
| **质量保证** | /wf_07_test | 测试开发 | --coverage |
|  | /wf_08_review | 代码审查 | Dimension 6文档约束 |
|  | /wf_09_refactor | 代码重构 | - |
|  | /wf_10_optimize | 性能优化 | - |
| **运维部署** | /wf_11_commit | 提交代码 | 自动更新CONTEXT.md + Frontmatter验证 |
|  | /wf_12_deploy_check | 部署检查 | - |
| **文档管理** | /wf_13_doc_maintain | 文档维护 | 清理+链接检查 |
|  | /wf_14_doc | 智能文档生成 | 约束驱动三阶段门控 ⭐ |
| **支持** | /wf_99_help | 帮助系统 | - |

## 管理文档体系
| 文件 | 职责 | 权限 | 特性 |
|------|------|------|------|
| PRD.md | 项目需求 | 只读 | 权威数据源 |
| PLANNING.md | 技术架构 | 读写 | 技术栈决策+开发标准 |
| TASK.md | 任务追踪 | 读写 | 进度管理+状态追踪 |
| CONTEXT.md | 会话指针 | 只读 | /wf_11_commit自动管理 |

## 知识库系统
- **KNOWLEDGE.md** - ADR索引、问题方案、设计模式、**文档索引中心**
- **docs/adr/** - 架构决策详情
- **docs/knowledge/** - 知识内容

## 约束驱动文档生成 (v3.4)
| 约束类型 | 规则 |
|---------|------|
| 文档大小 | < 500行/文件 |
| 索引大小 | KNOWLEDGE.md < 200行 |
| 增长率 | 单次 < 30% |
| 元数据 | 必需7个Frontmatter字段 |
| 分层 | 管理/技术/工作/归档 |

**三阶段门控**:
1. Phase 1: `/wf_05_code` Step 8 - 文档决策树
2. Phase 2: `/wf_14_doc` - 成本估计+约束检查
3. Phase 3: `/wf_08_review` Dimension 6 - 验证

## 开发规范
| 类别 | 规则 |
|------|------|
| 语言 | 中文交互、英文代码 |
| 格式化 | 自动（Black/Prettier） |
| 行尾 | Unix LF |
| 尾部空格 | 零容忍（pre-commit） |
| 提交格式 | [type] subject |
| 提交类型 | [feat]/[fix]/[docs]/[refactor]/[test] |

## 标准工作流
**功能开发**: `/wf_03_prime` → `/wf_05_code` → `/wf_07_test` → `/wf_08_review` → `/wf_11_commit`
**Bug修复**: `/wf_06_debug` → `/wf_07_test` → `/wf_11_commit`
**文档生成**: `/wf_05_code` → `/wf_08_review` → `/wf_14_doc` → `/wf_13_doc_maintain` → `/wf_11_commit`

## MCP 配置
| MCP | 配置文件 | 功能 |
|-----|---------|------|
| Serena | src/mcp/configs/serena.json | 语义代码理解 |
| Context7 | src/mcp/configs/context7.json | 官方库文档 |
| Sequential-thinking | src/mcp/configs/sequential-thinking.json | 结构化推理 |
| Tavily | src/mcp/configs/tavily.json | Web搜索 |
| Magic | src/mcp/configs/magic.json | UI组件生成 |

## 核心文档快速参考
| 文件 | 用途 | 权限 |
|------|------|------|
| COMMANDS.md | 14个命令完整参考 | 读取 |
| WORKFLOWS.md | 场景化工作流 | 读取 |
| TROUBLESHOOTING.md | 故障排查 | 读取 |
| CLAUDE.md | AI执行规则 | 读取 |
| README.md | 项目介绍 | 读取 |
| KNOWLEDGE.md | 知识库+索引 | 读写 |

## 版本历史
- **v3.4** (2025-11-24): 约束驱动文档生成完善版、三阶段门控、100% Frontmatter检查
- **v3.3** (2025-11-21): 智能文档生成、MCP集成
- **v3.2** (2025-11-06): Ultrathink设计哲学
- **v3.1**: 四层文档架构、智能按需加载

## 核心最佳实践
1. **会话开始**: `/wf_03_prime` ⭐
2. **提交前**: `/wf_08_review`（含Dimension 6）
3. **让命令处理一切**: `/wf_11_commit`（自动格式化+CONTEXT.md更新）
4. **PRD只读**: 需求修改需授权
5. **文档约束**: 遵守大小和增长率规范
6. **测试覆盖率**: `/wf_07_test --coverage`

---
**最后更新**: 2025-12-06
**Token节省**: ~456 tokens（通过表格化和紧凑布局）
