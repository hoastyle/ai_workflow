#!/bin/bash

# AI 工具知识库安装脚本
# 将知识库安装到 ~/.claude/knowledge-base/

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
INSTALL_DIR="$HOME/.claude/knowledge-base"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$HOME/.claude/backup/$(date +%Y%m%d_%H%M%S)"

echo -e "${GREEN}=== AI 工具知识库安装脚本 ===${NC}"
echo ""
echo "源目录: $SOURCE_DIR"
echo "安装目录: $INSTALL_DIR"
echo ""

# 检查源目录
if [ ! -f "$SOURCE_DIR/CLAUDE_KBASE.md" ]; then
    echo -e "${RED}错误: 未找到 CLAUDE_KBASE.md，请确保在正确的目录运行脚本${NC}"
    exit 1
fi

# 备份现有安装
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}检测到现有安装，正在备份...${NC}"
    mkdir -p "$BACKUP_DIR"
    cp -r "$INSTALL_DIR" "$BACKUP_DIR/"
    echo -e "${GREEN}✓ 备份完成: $BACKUP_DIR${NC}"
fi

# 创建安装目录
echo ""
echo "创建安装目录..."
mkdir -p "$INSTALL_DIR"

# 复制核心文件
echo "复制核心文件..."
cp "$SOURCE_DIR/CLAUDE_KBASE.md" "$INSTALL_DIR/CLAUDE.md"  # 重命名：知识库入口
cp "$SOURCE_DIR/KNOWLEDGE.md" "$INSTALL_DIR/"
cp "$SOURCE_DIR/PHILOSOPHY.md" "$INSTALL_DIR/"
cp "$SOURCE_DIR/README.md" "$INSTALL_DIR/"

# 复制文档目录
echo "复制文档目录..."
cp -r "$SOURCE_DIR/docs" "$INSTALL_DIR/"
cp -r "$SOURCE_DIR/best-practices" "$INSTALL_DIR/"
cp -r "$SOURCE_DIR/mcp-integration" "$INSTALL_DIR/"

# 复制脚本和工具
echo "复制脚本和工具..."
mkdir -p "$INSTALL_DIR/scripts"
mkdir -p "$INSTALL_DIR/commands/lib"
cp -r "$SOURCE_DIR/scripts/"*.py "$INSTALL_DIR/scripts/" 2>/dev/null || true
cp -r "$SOURCE_DIR/commands/lib/"*.py "$INSTALL_DIR/commands/lib/" 2>/dev/null || true

# 创建软链接到 ~/.claude/CLAUDE.md
echo ""
echo "创建软链接..."
if [ -L "$HOME/.claude/CLAUDE.md" ] || [ -f "$HOME/.claude/CLAUDE.md" ]; then
    echo -e "${YELLOW}警告: ~/.claude/CLAUDE.md 已存在，正在备份...${NC}"
    mv "$HOME/.claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)"
fi

ln -s "$INSTALL_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
echo -e "${GREEN}✓ 软链接已创建: ~/.claude/CLAUDE.md -> $INSTALL_DIR/CLAUDE.md${NC}"

# 设置权限
echo ""
echo "设置文件权限..."
chmod -R u+rw "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/scripts/"*.sh 2>/dev/null || true

# 生成安装信息文件
cat > "$INSTALL_DIR/.install_info" <<EOF
# AI 工具知识库安装信息

安装时间: $(date)
源目录: $SOURCE_DIR
安装目录: $INSTALL_DIR
备份目录: $BACKUP_DIR

版本: v2.1 (Claude Code 优先)
最后更新: $(date +%Y-%m-%d)
EOF

# 验证安装
echo ""
echo "验证安装..."
ERRORS=0

if [ ! -f "$INSTALL_DIR/CLAUDE.md" ]; then
    echo -e "${RED}✗ CLAUDE.md 未找到${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ CLAUDE.md${NC}"
fi

if [ ! -d "$INSTALL_DIR/docs/airis-mcp-gateway" ]; then
    echo -e "${RED}✗ AIRIS MCP Gateway 文档未找到${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ AIRIS MCP Gateway 文档${NC}"
fi

if [ ! -L "$HOME/.claude/CLAUDE.md" ]; then
    echo -e "${RED}✗ 软链接未创建${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ 软链接已创建${NC}"
fi

# 统计信息
echo ""
echo "=== 安装统计 ==="
echo "文件总数: $(find "$INSTALL_DIR" -type f | wc -l)"
echo "目录总数: $(find "$INSTALL_DIR" -type d | wc -l)"
echo "总大小: $(du -sh "$INSTALL_DIR" | cut -f1)"

# 完成
echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}=== 安装成功！===${NC}"
    echo ""
    echo "知识库已安装到: $INSTALL_DIR"
    echo "CLAUDE.md 软链接: ~/.claude/CLAUDE.md"
    echo ""
    echo "快速开始:"
    echo "  1. 在 Claude Code 中查看: ~/.claude/CLAUDE.md"
    echo "  2. 快速参考: $INSTALL_DIR/docs/airis-mcp-gateway/QUICK_REFERENCE.md"
    echo "  3. 工具索引: $INSTALL_DIR/docs/airis-mcp-gateway/TOOL_INDEX.md"
    echo ""
    echo -e "${YELLOW}提示: 如需更新知识库，重新运行此脚本即可${NC}"
else
    echo -e "${RED}=== 安装完成，但有 $ERRORS 个错误 ===${NC}"
    echo "请检查上述错误信息"
    exit 1
fi
