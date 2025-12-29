# ADR: CLAUDE.md 分离和角色明确化

**日期**: 2025-12-29
**状态**: 已接受
**决策者**: 架构团队

---

## 背景

在之前的设计中，`CLAUDE.md` 承担了双重角色：
1. 作为知识库的主入口（提供场景导航、快速参考）
2. 部署到 `~/.claude/CLAUDE.md` 作为用户配置

但源码仓库缺少"如何开发维护这个仓库"的指南，导致贡献者不清楚：
- 如何添加新文档
- 如何修改安装脚本
- 如何创建 ADR
- 如何发布新版本

同时，`CLAUDE_DEPLOY.md`（全局 Workflow 配置）的作用和使用场景也不够清晰。

---

## 决策

采用 **文件重命名 + 职责分离** 的方案：

### 文件架构

```
源码仓库 (ai_workflow/)
├── CLAUDE.md                    # 🔵 仓库开发指南（新编写）
│   └─ 职责：指导如何开发维护这个仓库
│   └─ 受众：贡献者、维护者
│
├── CLAUDE_KBASE.md             # 🟢 知识库入口（重命名当前 CLAUDE.md）
│   └─ 职责：用户使用知识库的导航
│   └─ 受众：使用知识库的项目开发者
│   └─ 安装时重命名为 CLAUDE.md
│
└── CLAUDE_DEPLOY.md            # 🟡 全局 Workflow 配置（保持不变）
    └─ 职责：全局 workflow 配置基线
    └─ 受众：所有项目通用配置

安装后 (~/.claude/)
├── CLAUDE.md                    # 软链接 → knowledge-base/CLAUDE.md
├── knowledge-base/
│   └── CLAUDE.md               # 来自 CLAUDE_KBASE.md
└── CLAUDE_DEPLOY.md (可选)     # 全局配置
```

### 关键设计点

1. **CLAUDE_KBASE.md 在安装时重命名为 CLAUDE.md**
   - 源码中：`CLAUDE_KBASE.md`（知识库入口源文件）
   - 安装后：`~/.claude/knowledge-base/CLAUDE.md`（用户看到的入口）

2. **源码中的 CLAUDE.md = 仓库开发指南**
   - 仅在源码仓库中被 Claude Code 读取
   - 指导贡献者如何开发维护这个仓库

3. **Makefile 作为便捷入口**
   - `make install` 调用 Bash 脚本
   - 保留脚本的交互性和灵活性

---

## 候选方案

### 方案 A：创建 CLAUDE_USER.md（被拒绝）

```
源码：CLAUDE.md, CLAUDE_USER.md, CLAUDE_DEPLOY.md
安装：CLAUDE_USER.md → ~/.claude/knowledge-base/CLAUDE.md
```

**劣势**：
- 引入新文件名，增加认知负担
- `CLAUDE_USER.md` 名字不够直观
- 需要解释为什么有三个相似名字的文件

### 方案 B：不分离（被拒绝）

保持当前状态，`CLAUDE.md` 继续承担双重角色。

**劣势**：
- 贡献者没有开发指南
- 角色混淆持续存在
- 不利于长期维护

### 方案 C：文件重命名（最终选择） ✅

```
源码：CLAUDE.md（开发指南）, CLAUDE_KBASE.md（入口源文件）
安装：CLAUDE_KBASE.md → CLAUDE.md
```

**优势**：
- 角色清晰：位置决定职责
- 命名直观：KBASE = Knowledge Base
- 向后兼容：软链接机制不变

---

## 权衡

| 维度 | 优势 | 劣势 | 缓解措施 |
|------|------|------|---------|
| **角色清晰** | ✅ 开发者和用户各得其所 | 源码有两个文件名不同 | 在文件第一句话明确说明 |
| **命名直观** | ✅ KBASE 安装后变为 CLAUDE.md | KBASE 名字可能不够直观 | README 详细说明 |
| **向后兼容** | ✅ 软链接机制不变 | - | - |
| **维护成本** | ✅ 职责单一，易于修改 | 需要维护两个文件 | 内容模块化避免重复 |

---

## 实施

### Phase 1: 文件准备

```bash
# 1. 备份
cp CLAUDE.md CLAUDE.md.v2.1.backup

# 2. 重命名
mv CLAUDE.md CLAUDE_KBASE.md

# 3. 创建新 CLAUDE.md（仓库开发指南，~200 行）
```

### Phase 2: 修改安装脚本

```bash
# scripts/install_knowledge_base.sh 关键修改

# 修改检查逻辑
if [ ! -f "$SOURCE_DIR/CLAUDE_KBASE.md" ]; then
    echo "错误: 未找到 CLAUDE_KBASE.md"
    exit 1
fi

# 修改复制逻辑（重命名）
cp "$SOURCE_DIR/CLAUDE_KBASE.md" "$INSTALL_DIR/CLAUDE.md"
```

### Phase 3: 创建 Makefile

```makefile
install:  ## 安装知识库
    @bash scripts/install_knowledge_base.sh

test:  ## 测试安装状态
    # 验证软链接和文件存在
```

### Phase 4: 更新文档

1. 更新 `README.md` 添加文件说明表格
2. 更新 `KNOWLEDGE.md` 索引
3. 创建本 ADR

### Phase 5: 测试验证

```bash
# 测试全新安装
rm -rf ~/.claude/knowledge-base
bash scripts/install_knowledge_base.sh

# 验证
readlink ~/.claude/CLAUDE.md
cat ~/.claude/knowledge-base/CLAUDE.md | head -5
cat CLAUDE.md | head -5  # 应显示开发指南
```

---

## 成功标准

**验证点**:
```bash
# 源码仓库
cat ai_workflow/CLAUDE.md | grep "仓库开发指南"
# ✓ 应该匹配

# 安装后
cat ~/.claude/knowledge-base/CLAUDE.md | grep "使用指南"
# ✓ 应该匹配

# 软链接
readlink ~/.claude/CLAUDE.md
# ✓ 应该指向 knowledge-base/CLAUDE.md
```

---

## 后续影响

### 对贡献者的影响

- ✅ 有明确的仓库开发指南
- ✅ 清晰的文档添加流程
- ✅ 安装脚本维护说明
- ✅ PR 和发布流程

### 对用户的影响

- ✅ 安装后看到的是知识库入口（无变化）
- ✅ 场景导航和快速参考（无变化）
- ⚠️ 需要理解三个文件的区别（通过 README 说明）

### 对 Claude Code 的影响

- ✅ 在源码仓库工作时，读取仓库开发指南
- ✅ 在用户项目中，读取知识库入口
- ✅ 优先级机制保持不变

---

## 参考资料

- [当前 CLAUDE.md (v2.1)](../CLAUDE.md.v2.1.backup)
- [新 CLAUDE.md (仓库开发指南)](../CLAUDE.md)
- [CLAUDE_KBASE.md (知识库入口)](../CLAUDE_KBASE.md)
- [CLAUDE_DEPLOY.md (全局配置)](../CLAUDE_DEPLOY.md)
- [安装脚本](../scripts/install_knowledge_base.sh)
- [Makefile](../Makefile)

---

**决策日期**: 2025-12-29
**实施日期**: 2025-12-29
**审核人**: 架构团队
**状态**: ✅ 已实施
