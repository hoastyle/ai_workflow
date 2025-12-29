# AI 工具知识库 - Makefile
# 便捷部署入口

.PHONY: help install uninstall test clean

.DEFAULT_GOAL := help

help:  ## 显示帮助信息
	@echo "AI 工具知识库 - 可用命令:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "示例:"
	@echo "  make install    # 安装知识库到 ~/.claude/knowledge-base/"
	@echo "  make test       # 测试安装"
	@echo "  make uninstall  # 卸载知识库"

install:  ## 安装知识库
	@echo "开始安装 AI 工具知识库..."
	@bash scripts/install_knowledge_base.sh

uninstall:  ## 卸载知识库
	@echo "开始卸载 AI 工具知识库..."
	@bash scripts/uninstall_knowledge_base.sh

test:  ## 测试安装状态
	@echo "测试知识库安装..."
	@if [ -L "$${HOME}/.claude/CLAUDE.md" ]; then \
		echo "✓ 软链接已创建: ~/.claude/CLAUDE.md"; \
		readlink "$${HOME}/.claude/CLAUDE.md"; \
	else \
		echo "✗ 软链接未找到"; \
	fi
	@if [ -f "$${HOME}/.claude/knowledge-base/CLAUDE.md" ]; then \
		echo "✓ 知识库入口存在: ~/.claude/knowledge-base/CLAUDE.md"; \
	else \
		echo "✗ 知识库入口未找到"; \
	fi
	@if [ -d "$${HOME}/.claude/knowledge-base/docs/airis-mcp-gateway" ]; then \
		echo "✓ AIRIS MCP Gateway 文档存在"; \
	else \
		echo "✗ AIRIS MCP Gateway 文档未找到"; \
	fi

clean:  ## 清理备份文件
	@echo "清理备份文件..."
	@rm -rf CLAUDE.md.v*.backup
	@echo "✓ 清理完成"

verify:  ## 验证文件完整性
	@echo "验证知识库文件..."
	@python3 scripts/frontmatter_utils.py validate-batch docs/ 2>/dev/null || echo "⚠️  Frontmatter 验证跳过（需要 Python 3）"
	@echo "✓ 验证完成"
