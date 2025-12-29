#!/bin/bash

# AI 工具知识库卸载脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

INSTALL_DIR="$HOME/.claude/knowledge-base"
BACKUP_DIR="$HOME/.claude/backup/uninstall_$(date +%Y%m%d_%H%M%S)"

echo -e "${YELLOW}=== AI 工具知识库卸载脚本 ===${NC}"
echo ""

# 检查是否已安装
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}错误: 未找到安装目录 $INSTALL_DIR${NC}"
    exit 1
fi

# 确认卸载
echo "即将卸载知识库:"
echo "  安装目录: $INSTALL_DIR"
echo "  软链接: ~/.claude/CLAUDE.md"
echo ""
read -p "确认卸载? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消卸载"
    exit 0
fi

# 备份
echo ""
echo "创建备份..."
mkdir -p "$BACKUP_DIR"
if [ -d "$INSTALL_DIR" ]; then
    cp -r "$INSTALL_DIR" "$BACKUP_DIR/"
    echo -e "${GREEN}✓ 备份完成: $BACKUP_DIR${NC}"
fi

# 删除软链接
echo ""
echo "删除软链接..."
if [ -L "$HOME/.claude/CLAUDE.md" ]; then
    rm "$HOME/.claude/CLAUDE.md"
    echo -e "${GREEN}✓ 软链接已删除${NC}"
fi

# 删除安装目录
echo ""
echo "删除安装目录..."
rm -rf "$INSTALL_DIR"
echo -e "${GREEN}✓ 安装目录已删除${NC}"

# 完成
echo ""
echo -e "${GREEN}=== 卸载完成 ===${NC}"
echo ""
echo "备份位置: $BACKUP_DIR"
echo ""
echo "如需重新安装，请运行:"
echo "  bash scripts/install_knowledge_base.sh"
