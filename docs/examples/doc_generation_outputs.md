# 文档生成输出格式示例

本文档包含 `/wf_14_doc` 命令的各种输出格式示例。

## 1. 成本估计和分层建议报告（约束驱动）

此报告在生成前展示成本估计，确保符合约束：

```markdown
# 📊 文档生成成本估计

## 现有文档规模
- KNOWLEDGE.md: {current_lines} 行
- docs/ 总计: {current_docs_lines} 行
- 总规模: {total_lines} 行

## 预算约束
- KNOWLEDGE.md 上限: < 200 行 (当前 {pct}% 使用)
- KNOWLEDGE.md 增长限制: < 20% per commit
- docs/ 增长限制: < 30% per commit
- 单个文档限制: < 500 行

## 检测到的文档需求

| # | 类型 | 建议位置 | 预估大小 | 约束 | 状态 |
|---|------|--------|---------|-----|------|
| 1 | Type A | PLANNING.md | ~30行 | <50 | ✅ |
| 2 | Type B | docs/adr/ | ~150行 | <200 | ✅ |
| 3 | Type C | docs/api/ | ~400行 | <500 | ✅ |
| 4 | Type D | KNOWLEDGE.md FAQ | ~25行 | <50 | ✅ |

## 成本影响预测

```
KNOWLEDGE.md:
  当前: 155 行
  增加: +25 行 (Type D)
  预计: 180 行
  增长率: +16.1% (符合 <20% 约束) ✅

docs/:
  当前: 2450 行
  增加: +580 行 (Types A,B,C)
  预计: 3030 行
  增长率: +23.7% (符合 <30% 约束) ✅

总体: 所有约束符合 ✅
```

## 后续步骤

这个估计将在用户确认后执行实际生成。
如果有文档被取消或修改，成本估计会重新计算。
```

## 2. 分析和选择报告

```markdown
# 📋 文档生成选择

## 代码库概览
- 项目: {project_name}
- 规模: {loc} LOC
- 技术栈: {tech_stack}

## 检测到的文档缺口

### ⚠️ 严重缺口 ({count})
- API 文档过时 (3 个新端点未记录)
- 环境变量文档缺失

### 📝 中等缺口 ({count})
- 开发指南需要更新
- 部署文档部分缺失

### ✅ 完整文档 ({count})
- 项目 README
- 架构决策已记录

## 建议生成的文档

```
[1] API 文档更新 (Type C)
    位置: docs/api/endpoints.md
    大小估计: ~400 行
    原因: 检测到 3 个新的 REST 端点

[2] 架构决策 (Type B)
    位置: docs/adr/2025-11-18-xxx.md
    大小估计: ~150 行
    原因: 最近的技术选型决策

[3] FAQ 更新 (Type D)
    位置: KNOWLEDGE.md § 常见问题
    大小估计: ~25 行
    原因: 3 个常见开发问题

成本影响: KNOWLEDGE.md +8%, docs/ +15% (均符合约束)
```

## 确认选择

请从下列选项中选择:

```
[ ] (1) 生成全部建议的文档
[ ] (2) 自定义选择 (输入编号, 如: 1,3)
[ ] (3) 取消 (返回不生成)
```
```

## 3. 生成和验证报告（约束驱动）

```markdown
# ✅ 文档生成完成（约束已验证）

## 生成的文档 ({count})
1. ✅ docs/api/endpoints.md (400 行) - Type C
2. ✅ docs/adr/2025-11-18-xxx.md (145 行) - Type B
3. ✅ KNOWLEDGE.md FAQ 补充 (24 行) - Type D

## Frontmatter 验证
- ✅ 所有文档都有完整的 Frontmatter
- ✅ 7 个必需字段完整
- ✅ 枚举值有效，日期格式正确
- ✅ related_documents 和 related_code 已填写

## 成本验证（约束检查）
```
约束检查结果:
  ✅ KNOWLEDGE.md 行数: 155 → 179 (< 200)
  ✅ KNOWLEDGE.md 增长: +15.5% (< 20%)
  ✅ docs/ 增长: +18.7% (< 30%)
  ✅ 单个文档: 400 < 500, 145 < 200, 24 < 50

所有约束符合 ✅
```

## 索引更新
- KNOWLEDGE.md 索引: 添加 3 个条目（API, FAQ, ADR）
- 文档关系图: 已更新

## 下一步（强制工作流）

```
✅ 文档已生成且通过约束检查！

推荐工作流:
1. /wf_08_review          ← 执行 Dimension 6 文档架构合规性检查
2. [审查通过]
3. /wf_11_commit          ← 提交文档和记录决策

命令序列:
  /wf_08_review
  /wf_11_commit "docs: 生成 API 和 FAQ 文档"
```
```
```
