# Serena MCP 连接故障排查指南

## 问题描述

使用 `/wf_03_prime` 命令时，有时会出现以下错误：

```
● Agent Output wf_03_prime
  ⎿ Error retrieving agent output
```

或者在日志中看到：

```
❌ Serena MCP 连接失败
⚠️ 无法连接到 Serena 服务器
```

## 根本原因分析

| 原因 | 概率 | 症状 | 解决难度 |
|------|------|------|---------|
| **Serena 服务器未启动/崩溃** | 40% | 无法连接，错误立即出现 | 容易 ✅ |
| **LSP 初始化超时** | 35% | 30-60秒后超时，出现 "Error retrieving" | 中等 ⚠️ |
| **项目代码库过大** | 15% | LSP 扫描时间过长 | 中等 ⚠️ |
| **网络/系统问题** | 10% | 间歇性连接失败 | 困难 ❌ |

## 诊断步骤

### Step 1: 运行诊断脚本

首先运行项目中的诊断脚本，它会检查所有关键组件：

```bash
cd /home/hao/Workspace/MM/utility/ai_workflow
bash scripts/diagnose_mcp.sh
```

**诊断脚本检查的内容**：
- ✅ `uvx` 命令是否可用
- ✅ Serena 是否可以正常安装
- ✅ 项目大小和代码文件数量
- ✅ 最近的错误日志
- ✅ Serena MCP 服务器是否能启动

### Step 2: 根据诊断结果采取行动

#### 情况 A：`uvx` 命令不可用

**症状**：诊断脚本第一步失败

**解决方案**：
```bash
# 安装 uv（Python 包管理器）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
uvx --version
```

#### 情况 B：Serena 无法安装

**症状**：诊断脚本第二步失败，显示网络或 Git 错误

**可能原因**：
- GitHub 访问问题
- 网络连接不稳定

**解决方案**：
```bash
# 检查网络连接
ping github.com

# 尝试直接克隆 Serena 仓库
git clone https://github.com/oraios/serena.git /tmp/serena-test

# 如果都失败，临时禁用 Serena（见下文）
```

#### 情况 C：项目太大，LSP 初始化超时

**症状**：诊断脚本显示代码文件数 > 1000 或总大小 > 100MB

**解决方案**：

1. **优化 `.gitignore`，减少扫描范围**：

```bash
# 添加到 .gitignore
echo "
# Large directories that slow down LSP
node_modules/
.git/
build/
dist/
venv/
.venv/
__pycache__/
*.min.js
*.bundle.js
.cache/
" >> .gitignore
```

2. **或者在 MCP 配置中添加项目排除列表**：

编辑 `~/.claude/mcp.json`，在 Serena 配置中添加：

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--context",
        "ide-assistant",
        "--enable-web-dashboard",
        "false",
        "--enable-gui-log-window",
        "false"
      ],
      "env": {
        "SERENA_EXCLUDE_PATTERNS": "node_modules,venv,__pycache__,.git,build,dist"
      }
    }
  }
}
```

#### 情况 D：Serena MCP 启动失败

**症状**：诊断脚本第五步失败，显示 "Serena MCP 服务器启动失败"

**可能原因**：
- Serena 进程崩溃
- 资源不足（内存）
- Python 依赖缺失

**解决方案**：

```bash
# 1. 查看详细错误日志
cat /tmp/serena_mcp.log

# 2. 检查系统资源
free -h  # 检查内存
df -h    # 检查磁盘

# 3. 重新安装 Serena（清除缓存）
rm -rf ~/.cache/uv/archive-v0/
uvx --from git+https://github.com/oraios/serena serena --version

# 4. 重启 Claude Code
# 通过 GUI 或重启终端
```

## 快速解决方案

### 方案 1：重启 Claude Code（最简单）

经常 Serena 连接失败只是因为进程状态不一致，重启通常能解决：

```bash
# 方法 1：关闭所有 Claude Code 进程
pkill -f "claude"

# 方法 2：重启终端/IDE
# 重新启动使用 Claude Code 的终端或 IDE

# 然后重新运行
/wf_03_prime
```

### 方案 2：临时禁用 Serena（快速规避）

如果需要立即继续工作，可以临时禁用 Serena MCP：

**步骤 1**：备份 MCP 配置
```bash
cp ~/.claude/mcp.json ~/.claude/mcp.json.backup
```

**步骤 2**：编辑 `~/.claude/mcp.json`，注释掉 Serena 部分

```json
{
  "mcpServers": {
    // ... 其他 MCP 服务器 ...

    // 临时注释掉 Serena（使用传统模式）
    /*
    "serena": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--context",
        "ide-assistant",
        "--enable-web-dashboard",
        "false",
        "--enable-gui-log-window",
        "false"
      ]
    }
    */
  }
}
```

**步骤 3**：重启 Claude Code

使用 `/wf_03_prime` 时，系统会自动降级到传统模式。

### 方案 3：使用项目中的 MCP 管理器

项目中已包含 Serena MCP 连接管理器，提供自动重试和降级：

```bash
# 测试连接管理器
python src/mcp/serena_manager.py

# 运行启动器（自动检测模式）
python scripts/wf_03_prime_launcher.py
```

这将显示：
- ✅ 当前 Serena 连接状态
- 📍 选择的执行模式（Serena 智能 vs 传统）
- 💡 如果连接失败的建议

## 预防措施

### 1. 定期健康检查

将诊断加入定期计划：

```bash
# 每周运行诊断
# 添加到 crontab（可选）
0 9 * * 1 cd ~/Workspace/MM/utility/ai_workflow && bash scripts/diagnose_mcp.sh >> /tmp/mcp_health.log
```

### 2. 监控日志

保存 Serena MCP 的执行日志：

```bash
# 启用详细日志
WF03_VERBOSE=1 /wf_03_prime
```

### 3. 优化项目配置

确保 `.gitignore` 排除不必要的大文件夹：

```bash
# 检查哪些文件夹最大
du -sh * | sort -h | tail -10
```

## 高级诊断

### 查看详细的 Serena 日志

```bash
# Serena 将日志写到标准错误和 stdout
# 直接启动 Serena（不通过 MCP）可以看到详细日志
uvx --from git+https://github.com/oraios/serena serena start-mcp-server \
    --context ide-assistant \
    --enable-web-dashboard false \
    --enable-gui-log-window false \
    2>&1 | tee /tmp/serena_debug.log
```

### 检查 Claude Code 配置

```bash
# 查看 MCP 配置
cat ~/.claude/mcp.json | jq '.mcpServers.serena'

# 查看 Claude Code 日志（如果有）
find ~/.claude -name "*.log" -type f -mtime -1 2>/dev/null
```

## 何时联系支持

如果尝试上述所有方案都无法解决，请收集以下信息后联系支持：

1. 诊断脚本的完整输出：
   ```bash
   bash scripts/diagnose_mcp.sh 2>&1 | tee /tmp/mcp_diagnosis.txt
   ```

2. Serena 启动日志：
   ```bash
   cat /tmp/serena_debug.log
   ```

3. 系统信息：
   ```bash
   uname -a
   python3 --version
   uvx --version
   ```

4. Claude Code 版本和配置：
   ```bash
   cat ~/.claude/mcp.json
   ```

## 总结决策树

```
遇到 /wf_03_prime 连接错误
│
├─ Step 1: 运行 bash scripts/diagnose_mcp.sh
│
├─ uvx 不可用？
│  └─ 安装 uv：curl -LsSf https://astral.sh/uv/install.sh | sh
│
├─ Serena 无法安装？
│  └─ 检查网络，尝试 git clone https://github.com/oraios/serena.git
│
├─ 项目太大（>1000 代码文件）？
│  └─ 优化 .gitignore，排除 node_modules, venv 等大目录
│
├─ Serena MCP 启动失败？
│  ├─ 查看 /tmp/serena_mcp.log
│  └─ 重启 Claude Code
│
├─ 问题仍未解决？
│  └─ 临时禁用 Serena（编辑 ~/.claude/mcp.json，注释 serena 部分）
│
└─ 继续使用传统模式开发
   （性能略有下降，但功能完整）
```

## 相关资源

- Serena GitHub: https://github.com/oraios/serena
- Claude Code 文档: https://claude.com/claude-code
- MCP 配置: `~/.claude/mcp.json`
- 项目 MCP 管理器: `src/mcp/serena_manager.py`
- 诊断脚本: `scripts/diagnose_mcp.sh`

---

**最后更新**: 2025-12-10
**版本**: 1.0
