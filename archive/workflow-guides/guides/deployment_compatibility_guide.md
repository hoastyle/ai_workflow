# 老版本部署兼容性指南

---
title: "老版本部署兼容性指南"
description: "AI Workflow 命令系统在老版本环境中的兼容性、降级策略和迁移指南"
type: "故障排查"
status: "完成"
priority: "高"
created_date: "2025-12-08"
last_updated: "2025-12-08"
related_documents:
  - "KNOWLEDGE.md"
  - "scripts/validate_command_compatibility.py"
  - "docs/integration/MCP_INTEGRATION_STRATEGY.md"
tags: ["兼容性", "部署", "MCP", "降级", "迁移"]
authors: ["Claude"]
version: "1.0"
---

## 老版本定义

**老版本部署** 包括：
1. **版本范围**: v1.0-v1.6 (相对于当前 v1.7)
2. **功能定义**: 任何不支持 MCP (Model Context Protocol) 的环境

**常见场景**: 渐进式升级、企业IT限制、离线部署、CI/CD受限环境

---

## 版本对比矩阵

| 版本 | MCP 支持 | 命令可用性 | 关键特性 |
|------|---------|-----------|---------|
| v1.0-v1.2 | ❌ 无 | 3个完全 + 9个基础 + 2个不可用 | 基础工作流 |
| v1.3-v1.5 | 🟡 部分 (Context7, Tavily) | 3个完全 + 9个部分 + 2个不可用 | 智能加载、Token预算 |
| v1.6 | 🟠 3个 (+ Serena) | 3个完全 + 11个增强 + 2个受限 | Serena 集成 |
| v1.7 | ✅ 全部6个 | 全部14个完整 | Agent系统 + 100% MCP |

**MCP 引入时间线**: Sequential-thinking (v1.5), Context7 (v1.4), Tavily (v1.4), Serena (v1.6), Magic (v1.7), Playwright (v1.7)

---

## 环境检测方法

### 自动检测（推荐）

```bash
# 运行兼容性脚本
python scripts/validate_command_compatibility.py

# 输出示例
# ✅ 环境版本: v1.7 (完全兼容)
# ✅ MCP 可用: 6/6
# ✅ 命令兼容: 14/14 (FULL: 14, LIMITED: 0, UNAVAILABLE: 0)
```

**检测逻辑**:
```python
import importlib.util
import sys
from pathlib import Path

def detect_environment_version():
    """检测环境版本"""
    if Path("commands/lib/agent_registry.py").exists() and \
       Path("src/mcp/gateway.py").exists() and \
       Path("COMMAND_INDEX.md").exists():
        return "v1.7", "完全兼容"
    elif Path("src/mcp/gateway.py").exists():
        return "v1.6", "大部分兼容"
    elif Path("docs_index.json").exists():
        return "v1.3-v1.5", "基础兼容"
    else:
        return "v1.0-v1.2", "受限兼容"

def detect_mcp_servers():
    """检测 MCP 可用性"""
    mcps = ["mcp_sequential_thinking", "mcp_context7", "mcp_serena",
            "mcp_tavily", "mcp_magic", "mcp_playwright"]
    return {mcp: importlib.util.find_spec(mcp) is not None for mcp in mcps}
```

### 手动检测（5步）

```bash
# Step 1: 检查标识文件
ls COMMAND_INDEX.md src/mcp/gateway.py docs_index.json commands/lib/agent_registry.py

# Step 2: Python 版本
python --version  # 要求 3.9+，推荐 3.10+

# Step 3: 测试 MCP 导入
python -c "import importlib.util; print('\n'.join(f'{m}: {"✅" if importlib.util.find_spec(m) else "❌"}' for m in ['mcp_sequential_thinking', 'mcp_context7', 'mcp_serena', 'mcp_tavily', 'mcp_magic', 'mcp_playwright']))"

# Step 4: 运行兼容性测试
/wf_03_prime --quick

# Step 5: 查看版本标识
grep "版本" KNOWLEDGE.md | head -3
```

**判断规则**: 全通过→v1.7, Step1-3通过→v1.6, Step1-2通过→v1.3-v1.5, 否则→v1.0-v1.2

---

## 命令兼容性说明

### Tier 1: 完全兼容（3个）

无 MCP 依赖，所有版本 100% 功能：

| 命令 | 功能 |
|------|------|
| /wf_01_planning | 项目规划 |
| /wf_02_task | 任务追踪 |
| /wf_11_commit | Git提交 |

---

### Tier 2: 功能降级（9个）

可选 MCP，老版本降级 50-80%：

| 命令 | v1.7 增强 | 老版本降级 | 功能损失 |
|------|----------|-----------|---------|
| /wf_03_prime | Serena 自动加载 | 标准文件读取 | -39% token |
| /wf_04_ask | Sequential-thinking + Context7 + Tavily | 纯文本分析 | 无结构推理/文档/搜索 |
| /wf_04_research | Context7 + Tavily | 手动查询 | 无自动化 |
| /wf_05_code | Serena + Magic | 标准编辑 | 无语义/UI生成 |
| /wf_06_debug | Sequential-thinking + Serena | 标准分析 | 无结构化/符号定位 |
| /wf_07_test | Serena + Sequential-thinking | 标准执行 | 无符号覆盖/推理 |
| /wf_08_review | Serena + Sequential-thinking | 文本审查 | 无语义/结构分析 |
| /wf_09_refactor | Serena 符号重构 | 文本替换 | 无依赖分析 |
| /wf_10_optimize | Serena 性能分析 | 手动分析 | 无符号瓶颈定位 |

**降级示例**:
```bash
# v1.7 (完整)
/wf_04_ask "技术决策" --think --c7 --research
# → 12步推理 + 官方文档 + Web搜索

# v1.0-v1.6 (降级)
/wf_04_ask "技术决策"
# → 文本分析 + 建议手动查询
```

---

### Tier 3: 受限/不可用（2个）

强依赖 MCP，老版本不可用：

| 命令 | 依赖 | 老版本 | 替代 |
|------|------|--------|------|
| /wf_12_deploy_check | Playwright | ❌ 不可用 | 手动 E2E: `pytest tests/e2e/` |
| /wf_14_doc | Magic | ⚠️ 严重受限 | 手动文档: `cp docs/examples/doc_templates/README_template.md docs/` |

---

### 兼容性总结

| 等级 | 命令数 | 可用性 |
|------|--------|--------|
| ✅ Tier 1 | 3 | 100% |
| 🟡 Tier 2 | 9 | 50-80% |
| 🔴 Tier 3 | 2 | 0-30% |
| **总计** | **14** | **~70%** |

---

## 完整迁移指南

### Step 1: 评估（15-30分钟）

```bash
# 运行检测
python scripts/validate_command_compatibility.py

# 决策矩阵
# v1.0-v1.2 → v1.7: 优先级🔴高, 工作量 8-16h
# v1.3-v1.5 → v1.7: 优先级🟠中, 工作量 4-8h
# v1.6 → v1.7:      优先级🟡低, 工作量 2-4h
```

---

### Step 2: 备份（10-20分钟）

```bash
# 创建备份
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/
tar -czf backups/ai_workflow_${BACKUP_DATE}.tar.gz \
    docs/management/ KNOWLEDGE.md COMMAND_INDEX.md src/ commands/

# 记录状态
git rev-parse HEAD > backups/git_commit_${BACKUP_DATE}.txt
python --version > backups/env_${BACKUP_DATE}.txt
pip list >> backups/env_${BACKUP_DATE}.txt
```

---

### Step 3: 升级（30-120分钟）

**v1.0-v1.2 → v1.7**:
```bash
git checkout tags/v1.5 && pip install -r requirements.txt && /wf_03_prime --quick
git checkout tags/v1.6 && pip install mcp-serena && /wf_03_prime
git checkout tags/v1.7 && pip install mcp-magic mcp-playwright
python scripts/validate_command_compatibility.py
```

**v1.3-v1.5 → v1.7**:
```bash
git checkout tags/v1.7
pip install -r requirements.txt
pip install mcp-serena mcp-magic mcp-playwright
python scripts/validate_command_compatibility.py
```

**v1.6 → v1.7**:
```bash
git pull origin master
pip install --upgrade mcp-magic mcp-playwright
/wf_03_prime
```

---

### Step 4: 验证（20-40分钟）

```bash
# 兼容性验证
python scripts/validate_command_compatibility.py
# 预期: 14/14 命令完全兼容

# 测试核心工作流
/wf_03_prime
/wf_04_ask "测试MCP" --think --c7
/wf_05_code "测试" --ui
/wf_08_review

# 验证 MCP
python -c "import importlib.util; print('\n'.join(f'{"✅" if importlib.util.find_spec(f"mcp_{m}") else "❌"} {m}' for m in ['sequential_thinking', 'context7', 'serena', 'tavily', 'magic', 'playwright']))"

# 集成测试
pytest tests/integration/ -v
```

**验收清单**:
- [ ] 14/14 命令兼容
- [ ] 6/6 MCP 可用
- [ ] 核心工作流正常
- [ ] 集成测试通过
- [ ] KNOWLEDGE.md 版本更新

---

## 降级与回滚场景

### 场景1: MCP 服务器不可用

**症状**: `错误: MCP 'serena' connection failed / Fallback: 使用标准功能`

**方案A - 临时降级**:
```bash
export DISABLE_MCP_SERENA=true
# 或
/wf_04_ask "问题" --no-mcp
```

**方案B - Circuit Breaker 自动**:
```python
# v1.7+ 内置 (src/mcp/gateway.py)
# 失败5次 → OPEN状态 → 自动降级 → 60秒后尝试恢复
```

**方案C - 完全回滚**:
```bash
git checkout tags/v1.6
pip uninstall mcp-magic mcp-playwright
# 12/14 命令可用
```

---

### 场景2: Python 版本不兼容

**症状**: `错误: Python 3.10+ required / 当前: 3.8.x`

**方案A - 升级 Python**:
```bash
sudo apt install python3.10 python3.10-venv  # Ubuntu
brew install python@3.10                      # macOS
python3.10 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**方案B - 降级项目**:
```bash
git checkout tags/v1.2  # 支持 Python 3.7+
```

---

### 场景3: 网络环境受限

**症状**: `错误: Cannot connect to MCP server / Timeout: 网络不可达`

**离线模式**:
```bash
# 配置
export MCP_OFFLINE_MODE=true
export MCP_CACHE_DIR=/path/to/cache

# 预下载缓存（在联网环境）
python scripts/download_mcp_cache.py

# 验证
/wf_04_ask "测试" --c7  # 使用缓存
```

**降级方案** - 使用 Tier 1-2 命令（离线可用）:
```bash
/wf_01_planning   # ✅ 完全
/wf_02_task       # ✅ 完全
/wf_03_prime      # 🟡 降级
/wf_05_code       # 🟡 降级
/wf_11_commit     # ✅ 完全
```

---

## 常见问题 FAQ

### Q1: 如何判断需要升级？

**A**: 运行 `python scripts/validate_command_compatibility.py`

| 结果 | 业务影响 | 优先级 |
|------|---------|--------|
| 14/14 | 无 | 低 |
| 10-13 | 效率降低 30-50% | 中 |
| <10 | 效率降低 >50% | 高 |

---

### Q2: 升级后可以回滚吗？

**A**: 可以。按 Step 2 备份后：
```bash
ls backups/
tar -xzf backups/ai_workflow_YYYYMMDD_HHMMSS.tar.gz
git checkout $(cat backups/git_commit_YYYYMMDD_HHMMSS.txt)
/wf_03_prime --quick
```
回滚时间: 5-10分钟

---

### Q3: MCP 连接失败怎么办？

**A**: 3层降级：
1. **自动重试** (3次, 5秒间隔)
2. **Circuit Breaker** (5次失败后降级)
3. **功能降级** (标准功能继续)

手动: `/wf_04_ask "问题" --no-mcp` 或 `export DISABLE_ALL_MCP=true`

---

### Q4: 老版本能用哪些核心功能？

**A**: 3个工作流：

```bash
# 工作流1: 项目启动
/wf_01_planning → /wf_02_task → /wf_03_prime
# ✅ 完全可用

# 工作流2: 功能开发
/wf_03_prime → /wf_05_code → /wf_11_commit
# 🟡 降级 30-50% (prime, code), ✅ commit 正常

# 工作流3: 质量保证
/wf_08_review → /wf_11_commit
# 🟡 review 降级, ✅ commit 正常
```

总体: ~70% 功能可用

---

### Q5: CI/CD 中如何处理兼容性？

**A**: Tox 矩阵 + 条件测试：

```ini
# tox.ini
[tox]
envlist = py{39,310,311}-{with_mcp,no_mcp}

[testenv]
deps = pytest; with_mcp: mcp-sequential-thinking mcp-context7 mcp-serena
commands = pytest tests/ --cov=src
```

```python
# 条件跳过
import pytest, importlib.util

@pytest.mark.skipif(
    importlib.util.find_spec("mcp_serena") is None,
    reason="Serena MCP not available"
)
def test_serena(): pass
```

---

### Q6: 升级时间和成本？

**A**:

| 起始 | 目标 | 时间 | 复杂度 |
|------|------|------|--------|
| v1.0-v1.2 | v1.7 | 4-8h | 高 |
| v1.3-v1.5 | v1.7 | 2-4h | 中 |
| v1.6 | v1.7 | 1-2h | 低 |

**ROI**: 效率提升 30-50%, Token 节省 31k+, 投资回收 1-2周

---

## 相关资源

- **自动化**: `scripts/validate_command_compatibility.py`
- **MCP 策略**: `docs/integration/MCP_INTEGRATION_STRATEGY.md`
- **技术模式**: `KNOWLEDGE.md § 技术模式参考`

---

**最后更新**: 2025-12-08 | **维护者**: AI Workflow Team | **版本**: 1.0
