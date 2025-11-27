---
command: /wf_05_code
index: 05
phase: "开发实现"
description: "功能实现协调器，遵循架构标准编写代码，集成 Ultrathink 优雅实现 | MCP: --ui / --serena"
reads: [PLANNING.md(开发标准), TASK.md(当前任务), KNOWLEDGE.md(代码模式), PHILOSOPHY.md(可选)]
writes: [代码文件, TASK.md(状态更新)]
prev_commands: [/wf_03_prime, /wf_04_ask]
next_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
ultrathink_lens: "craft_elegance"
model: sonnet
mcp_support:
  - name: "Magic"
    flag: "--ui"
    detail: "UI组件生成和设计系统集成"
  - name: "Serena"
    flag: "--serena"
    detail: "深度代码理解、精确定位、智能代码插入点"
context_rules:
  - "遵循PLANNING.md的代码标准"
  - "满足PRD需求"
  - "更新TASK.md进度"
  - "Ultrathink 优雅实现（Craft, Don't Code）：函数名清晰、抽象自然、错误处理优雅"
  - "✅ 支持 --serena 标志用于复杂修改，精确定位代码位置"
---

## 执行上下文
**输入**: PLANNING.md标准 + TASK.md任务 + KNOWLEDGE.md模式
**输出**: 代码实现 + TASK.md更新
**依赖链**: /wf_04_ask (可选) → **当前（代码实现）** → /wf_07_test → /wf_08_review

## Usage
`/wf_05_code <FEATURE_DESCRIPTION> [--serena] [--ui]`

**标志说明**:
- `--serena` - 启用 Serena MCP，用于复杂代码修改的精确定位和代码插入
  - 场景：大型类中添加新方法、在特定位置插入代码、理解复杂代码结构
  - 时间节省：50-70% (理解结构 5-15 分钟 → 快速定位 1-3 分钟)
  - 准确性提升：代码插入点准确率 70% → 95%
- `--ui` - 启用 Magic MCP，生成交互式 UI 组件和设计系统集成

## Context
- Feature/functionality to implement: $ARGUMENTS
- PLANNING.md defines architecture and standards
- TASK.md tracks implementation progress
- Existing codebase patterns will be followed
- **Serena MCP Integration** (optional via --serena):
  - Precise code location identification
  - Intelligent insertion point detection
  - Symbol-level understanding of code structure

## Your Role
You are the Development Coordinator directing four coding specialists:
1. **Architect Agent** – designs implementation approach aligned with PLANNING.md
2. **Implementation Engineer** – writes code following project standards
3. **Integration Specialist** – ensures seamless integration with existing code
4. **Code Reviewer** – validates quality and updates TASK.md progress

## Process

### Phase 1: 基础代码开发 (Step 1-7)

**核心步骤快速参考**:

| 步骤 | 职责 | Serena MCP 增强（可选） |
|------|------|----------------------|
| **1-2** | 上下文加载和架构设计 | `get_symbols_overview()` 快速理解文件结构 |
| **3-4** | 增量开发和质量验证 | `insert_after_symbol()` 精确插入代码 |
| **5-7** | 集成验证和准备提交 | `find_referencing_symbols()` 验证集成正确性 |

**详细说明**:

1. **Context Loading** (with optional Serena support):
   - Read relevant sections from PLANNING.md
   - Check TASK.md for related tasks and dependencies
   - Identify existing patterns to follow
   - **[Optional --serena]**: 使用 `get_symbols_overview()` 快速理解目标文件结构

2. **Implementation Strategy**:
   - Architect: Design components per architecture guidelines
   - Engineer: Implement with project's coding standards
   - **[Optional --serena]**: 使用 `find_symbol()` 精确定位插入点
   - Integration: Ensure compatibility with existing systems
   - Reviewer: Validate against quality criteria

3. **Progressive Development**:
   - Build incrementally with validation
   - **[Optional --serena]**: 使用 `insert_after_symbol()` 精确插入新代码
   - Update TASK.md after each milestone

4. **Quality Validation**:
   - Ensure code meets PLANNING.md standards
   - **[Optional --serena]**: 使用 `find_referencing_symbols()` 验证集成正确性
   - Run tests as specified in workflow

**Serena MCP 详细使用指南**: [§ wf_05_code Serena MCP 使用指南](docs/guides/wf_05_code_serena_guide.md)

---

### Phase 2: 文档同步决策树 (Step 8 - 约束驱动) ⭐

**强制执行**: 代码完成后**必须**执行此步，文档是代码的一等公民

#### 快速参考 - 6 个强制步骤

| 步骤 | 职责 | 输出 | 工具 |
|------|------|------|------|
| **8.1** | 文档变更范围确定 | Q1-Q5 检查清单结果 | 人工判断 |
| **8.2** | 按层级路由文档决策 | 确定类型 (A/B/C/D/E) | 决策树 |
| **8.3** | 自动更新文档索引 | Frontmatter 验证 + 索引同步 | Python 脚本 |
| **8.4** | 成本检查门控 | 所有约束检查状态 | 自动检查 |
| **8.5** | 决策记录和承诺 | commit message 文档部分 | Git commit |
| **8.6** | 准备进入下一步 | 工作流路径选择 | 决策矩阵 |

#### 文档类型快速查找表

| 改动类型 | 文档类型 | 位置 | 约束 | 例子 |
|---------|---------|------|------|------|
| 系统核心架构改动 | 类型A | PLANNING.md | < 50 行 | 重构认证层 Session → JWT |
| 技术决策和权衡 | 类型B | docs/adr/ | < 200 行 | 为什么选择异步队列 |
| 新 API/功能 | 类型C | docs/ | < 500 行 | API 端点使用说明 |
| 常见问题/最佳实践 | 类型D | KNOWLEDGE.md § FAQ | < 50 行/Q | 处理并发竞态条件 |
| 内部重构/优化 | 类型E | 无文档 | - | 变量名改进、内部函数重构 |

**完整文档同步指南**: [§ wf_05_code 文档同步决策树指南](docs/guides/wf_05_code_doc_sync_guide.md)

---

## Output Format

### 基础输出（Step 1-7）
1. **Implementation Plan** – approach aligned with project architecture
2. **Code Implementation** – working code following standards
3. **Task Updates** – TASK.md updates for completed work
4. **Integration Notes** – how code fits into system
5. **Next Actions** – remaining tasks and dependencies

### 文档决策输出（Step 8 - 约束驱动）⭐ NEW
6. **📋 文档决策总结** – 完成 Step 8.1-8.5 的结果：
   - ✅ 执行文档范围检查 (8.1) - 5 项检查清单结果
   - ✅ 文档分层决策 (8.2) - 确定文档类型 (A/B/C/D/E)
   - ✅ 索引更新执行 (8.3) - Frontmatter 验证 + 索引同步结果
   - ✅ 成本检查通过 (8.4) - 所有约束检查的状态
   - ✅ 决策记录 (8.5) - 将记录在 git commit message 中的文档部分

   **输出示例**：
   ```
   📄 文档决策总结
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   范围检查 (8.1):
   - Q1: 添加公开 API？ YES → 需要文档
   - Q2-Q5: NO

   分层决策 (8.2):
   - 类型C: 新增 docs/api/auth-endpoints.md (155 行)

   索引更新 (8.3):
   - ✅ Frontmatter 验证通过
   - ✅ KNOWLEDGE.md 索引已更新 (+1 条目)

   成本检查 (8.4):
   - KNOWLEDGE.md: 150 → 151 行 (+0.7%, ✅)
   - docs/: 2400 → 2555 行 (+6.5%, ✅)
   - 所有约束通过

   决策记录 (8.5):
   - 将在 commit message 中包含文档部分说明
   ```

7. **📚 文档完整性检查** – 如果创建了技术文档：
   - ✅ 所有新 docs/ 文件都有完整的 Frontmatter 元数据
   - ✅ 必需字段 (7个) 都已填写：title, description, type, status, priority, created_date, last_updated
   - ✅ 推荐字段已填写：related_documents, related_code, tags
   - ⚠️ 如果缺失：回到 Step 8.3，使用脚本修复或参考 CLAUDE.md FRONTMATTER 规范

8. **🎨 Ultrathink 设计检查** (可选提醒) – 代码优雅度自检（参见 PHILOSOPHY.md）
   - ✅ 函数/变量名字是否自然而清晰？(Obsess Over Details)
   - ✅ 代码结构是否流畅易懂？(Craft, Don't Code)
   - ✅ 错误处理是否优雅而有用？(Craft, Don't Code)
   - ✅ 有没有不必要的复杂性能移除？(Simplify Ruthlessly)

## Workflow Integration
- Reads context from PLANNING.md
- Updates progress in TASK.md
- Triggers `/wf_07_test` for validation
- Prepares for `/wf_08_review` cycle
- Leads to `/wf_11_commit` when complete

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[任务确认] → [架构咨询] → [代码实现 ← 当前] → [测试验证] → [代码审查] → [提交保存]
   STEP 1      STEP 2 (可选)   STEP 3        STEP 4      STEP 5     STEP 6
```

### 建议下一步（3 个选项）

| 选项 | 适用场景 | 命令序列 | 优势 |
|------|---------|---------|------|
| **A** | 功能复杂且新增 | `/wf_07_test` → `/wf_08_review` → `/wf_11_commit` | 测试先行，确保质量 |
| **B** | 功能修改已有代码 | `/wf_08_review` → `/wf_07_test` → `/wf_11_commit` | 快速发现设计问题 |
| **C** | 简单功能/文档修改 | `/wf_08_review` → `/wf_11_commit` | 减少开销 |

### 💡 决策指南

**我应该执行哪个选项？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 功能复杂且新增 | 选项 A | /wf_07_test → /wf_08_review → /wf_11_commit |
| 功能修改已有代码 | 选项 B | /wf_08_review → /wf_07_test → /wf_11_commit |
| 简单功能/文档修改 | 选项 C | /wf_08_review → /wf_11_commit |
| 不确定 | 咨询 | /wf_04_ask "我应该先测试还是先审查？" |

### 🔄 回到上一步

如果需要修改设计或架构：
```bash
/wf_04_ask "需要重新讨论的架构问题..."
# 修改代码后继续当前步骤
```

**完整工作流导航指南**: [§ wf_05_code 工作流和决策路径指南](docs/guides/wf_05_code_workflows.md)

---

## 相关文档

- **主命令系统**: WORKFLOWS.md - 完整工作流说明
- **代码标准**: PLANNING.md (Development Standards)
- **任务追踪**: TASK.md
- **设计原则**: PHILOSOPHY.md (Ultrathink)
- **文档同步指南**: [docs/guides/wf_05_code_doc_sync_guide.md](docs/guides/wf_05_code_doc_sync_guide.md)
- **Serena MCP 指南**: [docs/guides/wf_05_code_serena_guide.md](docs/guides/wf_05_code_serena_guide.md)
- **工作流导航指南**: [docs/guides/wf_05_code_workflows.md](docs/guides/wf_05_code_workflows.md)
