#!/bin/bash
# MCP 诊断脚本 - 检查 Serena MCP 服务器状态

echo "🔍 MCP 诊断工具"
echo "=================="

# 1. 检查 uvx 是否可用
echo ""
echo "1️⃣ 检查 uvx 命令..."
if command -v uvx &> /dev/null; then
    echo "✅ uvx 已安装: $(uvx --version 2>&1 | head -1)"
else
    echo "❌ uvx 未安装或不在 PATH 中"
fi

# 2. 检查 Serena 是否可安装
echo ""
echo "2️⃣ 测试 Serena 安装..."
timeout 10 uvx --from git+https://github.com/oraios/serena serena --version &> /tmp/serena_test.log
if [ $? -eq 0 ]; then
    echo "✅ Serena 可以正常安装"
    cat /tmp/serena_test.log
else
    echo "❌ Serena 安装超时或失败"
    echo "错误日志："
    cat /tmp/serena_test.log
fi

# 3. 检查项目大小
echo ""
echo "3️⃣ 检查项目大小..."
PROJECT_DIR="${PROJECT_DIR:-.}"
FILE_COUNT=$(find "$PROJECT_DIR" -type f -not -path "*/\.*" 2>/dev/null | wc -l)
CODE_FILE_COUNT=$(find "$PROJECT_DIR" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" \) -not -path "*/\.*" 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1)

echo "📊 项目统计 (目录: $PROJECT_DIR)："
echo "   总文件数: $FILE_COUNT"
echo "   代码文件数: $CODE_FILE_COUNT"
echo "   总大小: $TOTAL_SIZE"

if [ "$CODE_FILE_COUNT" -gt 1000 ]; then
    echo "⚠️  代码文件较多，LSP 初始化可能需要较长时间"
fi

# 4. 检查 Claude Code 日志
echo ""
echo "4️⃣ 检查最近的错误日志..."
if [ -d "$HOME/.claude/logs" ]; then
    echo "📋 最近的错误（最多 5 条）："
    find "$HOME/.claude/logs" -name "*.log" -type f -mtime -1 -exec grep -i "serena\|mcp\|timeout\|error" {} \; 2>/dev/null | tail -5
else
    echo "ℹ️  未找到日志目录"
fi

# 5. 测试 MCP 连接
echo ""
echo "5️⃣ 测试 Serena MCP 启动..."
echo "⏱️  启动 Serena MCP 服务器（30秒超时）..."
timeout 30 uvx --from git+https://github.com/oraios/serena serena start-mcp-server \
    --context ide-assistant \
    --enable-web-dashboard false \
    --enable-gui-log-window false &> /tmp/serena_mcp.log &
MCP_PID=$!

sleep 5
if ps -p $MCP_PID > /dev/null; then
    echo "✅ Serena MCP 服务器已启动（PID: $MCP_PID）"
    kill $MCP_PID 2>/dev/null
else
    echo "❌ Serena MCP 服务器启动失败"
    echo "错误日志："
    cat /tmp/serena_mcp.log
fi

echo ""
echo "=================="
echo "🎯 诊断完成"
echo ""
echo "💡 建议："
echo "   - 如果 Serena 安装失败：检查网络连接和 GitHub 访问"
echo "   - 如果项目太大：优化 .gitignore，排除大文件夹"
echo "   - 如果 MCP 启动慢：临时禁用 Serena（编辑 ~/.claude/mcp.json）"
echo "   - 查看完整日志：cat /tmp/serena_mcp.log"
