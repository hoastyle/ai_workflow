---
title: "AIRIS MCP Gateway 文档缺失分析报告"
description: "分析文档完整性和优化建议"
type: "架构决策"
status: "完成"
priority: "中"
created_date: "2025-12-30"
last_updated: "2025-12-31"
related_documents:
  - path: "PARAMETER_TRAPS.md"
    type: "补充"
    description: "基于本分析创建的参数陷阱文档"
  - path: "TROUBLESHOOTING.md"
    type: "补充"
    description: "基于本分析创建的故障排查文档"
  - path: "README.md"
    type: "参考"
    description: "主要使用指南"
related_code: []
tags: ["documentation", "gap-analysis", "quality-assurance"]
---

# 文档缺失分析报告

**日期**: 2025-12-30
**问题来源**: 使用 airis-mcp-gateway 调用 Serena 时多次失败
**分析范围**: ai_workflow 和 howie_skills 两个仓库

---

## 🔍 问题概述

在本次会话中，使用 AIRIS MCP Gateway 调用 Serena 时遇到以下困难：

1. **airis-find 查询失败**:
   - 使用 `airis-find({ query: "serena" })` 返回 "Found 0 tools"
   - 空查询 `airis-find({ query: "" })` 反而成功
   - 需要多次重试才能成功

2. **缺少故障排查指导**:
   - 不知道问题原因
   - 不知道如何调试
   - 不知道如何避免

---

## 📋 文档缺失清单

### ai_workflow 仓库

#### 缺失的核心文档

| 文档名称 | 优先级 | 状态 | 说明 |
|---------|--------|------|------|
| **TROUBLESHOOTING.md** | 🔴 严重 | ✅ 已创建并更新 | AIRIS MCP Gateway 故障排查完整指南（含参数陷阱章节） |
| **PARAMETER_TRAPS.md** | 🔴 严重 | ✅ 已创建 | 常见参数命名错误和正确用法快速参考 |
| **KNOWN_ISSUES.md** | 🟡 高 | ⚠️ 部分完成 | 已在 TROUBLESHOOTING.md 中记录核心问题 |
| **MIGRATION_FROM_DIRECT_MCP.md** | 🟡 高 | ⚠️ 部分 | 从直接 MCP 迁移到 Gateway 的指南 |
| **PERFORMANCE_TUNING.md** | 🟢 中 | ❌ 缺失 | HOT/COLD 模式性能优化 |

#### 现有文档的改进需求

| 文档 | 问题 | 改进建议 |
|------|------|----------|
| **README.md** | 提到"常见问题速查"但未实现 | 补充 FAQ 章节或链接到 TROUBLESHOOTING.md |
| **QUICK_REFERENCE.md** | 缺少错误处理示例 | 添加"常见错误和快速修复"章节 |
| **servers/SERENA.md** | 未说明 HOT 模式特性 | 添加"HOT 模式注意事项"章节 |

### howie_skills 仓库

#### 严重缺失的文档

| 文档名称 | 优先级 | 状态 | 说明 |
|---------|--------|------|------|
| **docs/TROUBLESHOOTING.md** | 🔴 严重 | ❌ 缺失 | Skills 使用故障排查指南 |
| **docs/GATEWAY_INTEGRATION.md** | 🔴 严重 | ❌ 缺失 | 如何通过 Gateway 使用 skills |
| **docs/ERROR_HANDLING.md** | 🟡 高 | ❌ 缺失 | 统一错误处理最佳实践 |
| **docs/TESTING_GUIDE.md** | 🟡 高 | ❌ 缺失 | 如何测试 skills 可用性 |
| **README.md** | 🔴 严重 | ❌ 缺失 | 仓库主文档（目前没有） |

#### 现有文档问题

| 文档 | 问题 | 影响 |
|------|------|------|
| **docs/** 目录 | 只有一个 SKILL_TEMPLATE.md | 用户无法找到使用指南 |
| **各 Skill SKILL.md** | 虽然已标准化，但缺少故障排查章节 | 遇到问题不知道怎么办 |

---

## 🎯 核心问题分析

### 问题概要（详细解决方案见 TROUBLESHOOTING.md）

**已发现的两大核心问题**:

1. **airis-find 查询不稳定** (已在 TROUBLESHOOTING.md 问题 1 记录)
   - 现象：带参数查询返回空结果，空查询反而成功
   - 解决方案：使用空查询 + 手动过滤
   - 文档覆盖：✅ TROUBLESHOOTING.md

2. **参数命名不统一导致 validation error** (已在 TROUBLESHOOTING.md 问题 5 + PARAMETER_TRAPS.md 记录)
   - 现象：直觉性参数名（如 `path`）导致验证错误
   - 根本原因：MCP 服务器间参数命名不统一
   - 解决方案：使用 airis-schema 验证 + 查阅 PARAMETER_TRAPS.md
   - 文档覆盖：✅ TROUBLESHOOTING.md + PARAMETER_TRAPS.md

**文档完成状态**:
- ✅ 问题已记录在 TROUBLESHOOTING.md
- ✅ 参数陷阱已文档化在 PARAMETER_TRAPS.md
- ✅ 用户有清晰的排查路径

---

## 📝 建议的后续工作

### 立即执行（高优先级）

1. **✅ 已完成**: 创建 `docs/airis-mcp-gateway/TROUBLESHOOTING.md`

2. **howie_skills 紧急补充**:
   ```
   howie_skills/
   ├── README.md （新建）
   │   - 仓库介绍
   │   - 7 个 skills 快速索引
   │   - 安装和使用快速开始
   │
   ├── docs/
   │   ├── TROUBLESHOOTING.md （新建）
   │   │   - 常见问题
   │   │   - Gateway 连接失败
   │   │   - 工具调用失败
   │   │
   │   ├── GATEWAY_INTEGRATION.md （新建）
   │   │   - 如何通过 AIRIS MCP Gateway 使用 skills
   │   │   - airis-find/schema/exec 三步工作流
   │   │   - HOT/COLD 模式说明
   │   │
   │   └── QUICK_START.md （新建）
   │       - 5 分钟上手指南
   │       - 第一个 skill 调用示例
   ```

3. **ai_workflow 补充**:
   ```
   docs/airis-mcp-gateway/
   ├── KNOWN_ISSUES.md （新建）
   │   - airis-find 查询不稳定
   │   - HOT 模式启动延迟
   │   - 其他已知限制
   │
   └── FAQ.md （新建）
       - 为什么 airis-find 返回 0 结果？
       - 如何知道服务器是否就绪？
       - 什么时候用 HOT，什么时候用 COLD？
   ```

### 短期执行（中优先级）

4. **更新现有文档**:
   - [ ] README.md: 补充 FAQ 章节或链接到 TROUBLESHOOTING.md
   - [ ] QUICK_REFERENCE.md: 添加"常见错误和快速修复"
   - [ ] servers/SERENA.md: 添加 HOT 模式特性说明

5. **在各 skill 中添加故障排查章节**:
   ```markdown
   ## 🔧 故障排查

   ### 问题 1: 工具调用失败
   - 检查 Gateway 是否运行
   - 查看完整排查指南: [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md)

   ### 问题 2: 参数错误
   - 使用 airis-schema 验证参数
   - 查看参数陷阱: [本文档的"常见陷阱"章节](#常见陷阱)
   ```

6. **创建测试工具**:
   ```bash
   # scripts/test_gateway.sh
   # 用于测试 Gateway 连接和服务器状态
   ```

### 长期执行（低优先级）

7. **性能调优文档**: PERFORMANCE_TUNING.md
8. **迁移指南**: MIGRATION_FROM_DIRECT_MCP.md（完善）
9. **视频教程**: 制作 3-5 分钟的快速开始视频

---

## 💡 关键经验教训

1. **文档必须覆盖故障情况**:
   - ✅ 不仅要有"如何使用"
   - ✅ 更要有"出问题怎么办"

2. **已知问题必须明确记录**:
   - ✅ airis-find 查询不稳定应该在文档中明确标注
   - ✅ 提供临时解决方案（空查询 + 过滤）

3. **示例代码要包含错误处理**:
   - ✅ 不能只展示"Happy Path"
   - ✅ 要展示完整的防御性编程

4. **HOT/COLD 模式需要特别说明**:
   - ✅ 不仅是性能差异
   - ✅ 更是使用模式的差异（预热、重试等）

---

## 📊 文档完整性评分

| 仓库 | 现状评分 | 补充后评分 | 改进幅度 |
|------|---------|-----------|---------|
| **ai_workflow** | 6/10 | 9/10 | +50% |
| **howie_skills** | 3/10 | 8/10 | +167% |

**评分标准**:
- 基础文档 (2分): README, 使用指南
- 参考文档 (2分): API 参考, 工具索引
- 故障排查 (3分): Troubleshooting, 已知问题, FAQ
- 最佳实践 (2分): 性能优化, 错误处理模式
- 示例代码 (1分): 完整的可运行示例

---

## 🚀 行动计划

### 第一阶段: 紧急补充 (1-2小时)
- [x] 创建 ai_workflow/docs/airis-mcp-gateway/TROUBLESHOOTING.md
- [x] 创建 ai_workflow/docs/airis-mcp-gateway/PARAMETER_TRAPS.md
- [x] 更新 TROUBLESHOOTING.md 添加参数陷阱章节
- [ ] 创建 howie_skills/README.md
- [ ] 创建 howie_skills/docs/TROUBLESHOOTING.md

### 第二阶段: 核心文档 (2-3小时)
- [ ] 创建 howie_skills/docs/GATEWAY_INTEGRATION.md
- [ ] 创建 ai_workflow/docs/airis-mcp-gateway/KNOWN_ISSUES.md
- [ ] 创建 ai_workflow/docs/airis-mcp-gateway/FAQ.md

### 第三阶段: 完善和优化 (1-2小时)
- [ ] 更新所有 SKILL.md 添加故障排查章节
- [ ] 更新现有文档链接到新创建的文档
- [ ] 创建测试脚本

---

**报告生成时间**: 2025-12-30
**分析人员**: Claude (基于实际使用经验)
**后续跟踪**: 定期review文档完整性，根据新问题持续更新
