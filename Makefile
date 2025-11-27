.PHONY: install install-link verify verify-manifest uninstall clean lint help mcp-install mcp-list mcp-check

# Default target
.DEFAULT_GOAL := help

###############################################################################
# Installation Targets
###############################################################################

install: ## Install commands to ~/.claude/ (copy mode, default)
	@echo "🔧 Installing AI Workflow Commands..."
	@[ -f ./install.sh ] || (echo "❌ install.sh not found in project root"; exit 1)
	@./install.sh --copy
	@echo ""
	@echo "✅ Installation complete!"
	@echo "   Next: Run 'make verify' to verify installation"

install-link: ## Install commands using symbolic links (development mode)
	@echo "🔧 Installing AI Workflow Commands (symlink mode)..."
	@[ -f ./install.sh ] || (echo "❌ install.sh not found in project root"; exit 1)
	@./install.sh --link
	@echo ""
	@echo "✅ Installation complete (symlink mode)!"
	@echo "   Files in project are directly used from ~/.claude/"

install-no-backup: ## Install without creating backup
	@echo "🔧 Installing without backup..."
	@./install.sh --copy --no-backup
	@echo "✅ Installation complete (no backup)"

verify: ## Verify installation is working correctly
	@echo "🔍 Verifying AI Workflow Installation"
	@echo "======================================"
	@echo ""
	@[ -d ~/.claude/commands ] || (echo "❌ Installation directory not found: ~/.claude/commands"; exit 1)
	@echo "✅ Installation directory exists: ~/.claude/commands"
	@echo ""
	@echo "📋 Installed commands:"
	@ls -1 ~/.claude/commands 2>/dev/null | grep "^wf_" | wc -l | xargs -I {} echo "   {} wf_* commands found"
	@ls -1 ~/.claude/commands 2>/dev/null | grep "^wf_" | sed 's/^/   - /' | head -5
	@echo "   ..."
	@echo ""
	@echo "📚 Installed guide documents:"
	@if [ -d ~/.claude/commands/docs/guides ]; then \
		find ~/.claude/commands/docs/guides -name "*.md" 2>/dev/null | wc -l | xargs -I {} echo "   {} guide documents found"; \
		find ~/.claude/commands/docs/guides -name "*.md" 2>/dev/null | sed 's|.*/||' | sed 's/^/   - /' | head -5; \
		echo "   ..."; \
	else \
		echo "   ⚠️  Guide documents directory not found"; \
	fi
	@echo ""
	@echo "✅ Configuration file:"
	@[ -f ~/.claude/CLAUDE.md ] && echo "   ✅ ~/.claude/CLAUDE.md exists" || echo "   ❌ ~/.claude/CLAUDE.md not found"
	@echo ""
	@echo "======================================"
	@echo "✅ Verification complete"

uninstall: ## Uninstall commands from ~/.claude/
	@echo "🧹 Uninstalling AI Workflow Commands..."
	@[ -f ./uninstall.sh ] || (echo "❌ uninstall.sh not found in project root"; exit 1)
	@./uninstall.sh
	@echo "✅ Uninstall complete"

###############################################################################
# Manifest and Configuration Verification
###############################################################################

verify-manifest: ## Verify install and uninstall manifests are consistent
	@echo "🔍 Verifying manifest consistency..."
	@[ -f ./scripts/verify_manifest.sh ] || (echo "❌ verify_manifest.sh not found"; exit 1)
	@bash ./scripts/verify_manifest.sh

###############################################################################
# Documentation Management
###############################################################################

docs-validate: ## Validate Frontmatter metadata for all documents
	@echo "📄 Validating document Frontmatter..."
	@[ -f ./scripts/frontmatter_utils.py ] || (echo "❌ frontmatter_utils.py not found"; exit 1)
	@python3 ./scripts/frontmatter_utils.py validate-batch docs/
	@echo "✅ Frontmatter validation complete"

docs-index: ## Update KNOWLEDGE.md documentation index
	@echo "📚 Updating documentation index..."
	@[ -f ./scripts/frontmatter_utils.py ] || (echo "❌ frontmatter_utils.py not found"; exit 1)
	@python3 ./scripts/frontmatter_utils.py validate-batch docs/ > /tmp/doc_index.json
	@echo "✅ Documentation index updated (results in /tmp/doc_index.json)"

docs-graph: ## Generate documentation relationship graph
	@echo "🔗 Generating documentation relationship graph..."
	@[ -f ./scripts/doc_graph_builder.py ] || (echo "❌ doc_graph_builder.py not found"; exit 1)
	@python3 ./scripts/doc_graph_builder.py docs/ --format mermaid > /tmp/doc_graph.mmd
	@echo "✅ Documentation graph generated (results in /tmp/doc_graph.mmd)"

docs-check: docs-validate docs-index ## Validate and update all documentation

###############################################################################
# Code Quality and Linting
###############################################################################

lint: ## Run linting checks (validate shell scripts and manifests)
	@echo "🔍 Running linting checks..."
	@echo ""
	@echo "1. Checking shell script syntax..."
	@(bash -n install.sh && echo "   ✅ install.sh" || echo "   ❌ install.sh has syntax errors")
	@(bash -n uninstall.sh && echo "   ✅ uninstall.sh" || echo "   ❌ uninstall.sh has syntax errors")
	@(bash -n scripts/install_utils.sh && echo "   ✅ install_utils.sh" || echo "   ❌ install_utils.sh has syntax errors")
	@(bash -n scripts/verify_manifest.sh && echo "   ✅ verify_manifest.sh" || echo "   ❌ verify_manifest.sh has syntax errors")
	@echo ""
	@echo "2. Checking manifest consistency..."
	@($(MAKE) verify-manifest > /dev/null 2>&1 && echo "   ✅ Manifests are consistent" || echo "   ⚠️  Manifest inconsistency detected")
	@echo ""
	@echo "✅ Linting complete"

format: ## Format shell scripts (with shfmt if available)
	@echo "📝 Formatting shell scripts..."
	@if command -v shfmt > /dev/null 2>&1; then echo "Using shfmt for formatting..."; shfmt -i 4 -w install.sh uninstall.sh scripts/*.sh; echo "✅ Formatting complete"; else echo "⚠️  shfmt not found. Install with: sudo apt-get install shfmt"; fi

###############################################################################
# MCP (Model Context Protocol) Integration
###############################################################################

mcp-install: ## Install MCP servers (interactive)
	@echo "📦 Installing MCP Servers..."
	@[ -f ./scripts/install_mcp.py ] || (echo "❌ install_mcp.py not found in scripts/"; exit 1)
	-@python3 ./scripts/install_mcp.py

mcp-install-all: ## Install all available MCP servers
	@echo "📦 Installing all MCP servers..."
	@[ -f ./scripts/install_mcp.py ] || (echo "❌ install_mcp.py not found in scripts/"; exit 1)
	-@python3 ./scripts/install_mcp.py --all

mcp-list: ## List all available MCP servers
	@echo "📋 Available MCP Servers:"
	@[ -f ./scripts/install_mcp.py ] || (echo "❌ install_mcp.py not found in scripts/"; exit 1)
	-@python3 ./scripts/install_mcp.py --list

mcp-check: ## Check MCP prerequisites (Claude CLI and Node.js)
	@echo "🔍 Checking MCP prerequisites..."
	@which claude > /dev/null && echo "   ✅ Claude CLI found: $$(claude --version)" || echo "   ❌ Claude CLI not found"
	@which node > /dev/null && echo "   ✅ Node.js found: $$(node --version)" || echo "   ❌ Node.js not found"
	@which npm > /dev/null && echo "   ✅ npm found: $$(npm --version)" || echo "   ❌ npm not found"

###############################################################################
# Maintenance and Cleanup
###############################################################################

clean: ## Clean up temporary files and caches
	@echo "🧹 Cleaning up..."
	@rm -rf .pytest_cache .mypy_cache __pycache__ .ruff_cache
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

status: ## Show installation and project status
	@echo "📊 Project Status"
	@echo "=================================================="
	@echo ""
	@echo "📁 Project Location:"
	@pwd
	@echo ""
	@echo "📦 Installation Status:"
	@if [ -d ~/.claude/commands ]; then echo "   ✅ Commands installed: ~/.claude/commands"; echo "   📋 $$(ls -1 ~/.claude/commands 2>/dev/null | grep '^wf_' | wc -l) wf_* commands"; echo "   ✅ Configuration: ~/.claude/CLAUDE.md"; else echo "   ❌ Not installed yet"; echo "   💡 Run 'make install' to install"; fi
	@echo ""
	@echo "📚 Project Files:"
	@echo "   📄 Command definitions: $$(ls -1 wf_*.md 2>/dev/null | wc -l) files"
	@echo "   📚 Documentation: $$(ls -1 docs/ 2>/dev/null | wc -l) directories"
	@echo "   🔧 Scripts: $$(ls -1 scripts/*.sh 2>/dev/null | wc -l) shell scripts, $$(ls -1 scripts/*.py 2>/dev/null | wc -l) python scripts"
	@echo ""
	@echo "=================================================="

###############################################################################
# Help and Information
###############################################################################

help: ## Show this help message
	@echo "Claude Code Workflow Commands - Makefile"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make install         - Install commands (recommended)"
	@echo "  make verify          - Verify installation is working"
	@echo "  make uninstall       - Remove installed commands"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make install-link    - Install with symlinks (development mode)"
	@echo "  make lint            - Check code quality and manifests"
	@echo "  make format          - Format shell scripts (requires shfmt)"
	@echo "  make clean           - Clean temporary files"
	@echo ""
	@echo "🔌 MCP Integration:"
	@echo "  make mcp-check       - Check MCP prerequisites (Claude CLI, Node.js)"
	@echo "  make mcp-list        - List all available MCP servers"
	@echo "  make mcp-install     - Install MCP servers (interactive)"
	@echo "  make mcp-install-all - Install all available MCP servers"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  make docs-validate   - Validate document Frontmatter"
	@echo "  make docs-index      - Update documentation index"
	@echo "  make docs-graph      - Generate documentation graph"
	@echo "  make docs-check      - Validate and update all documentation"
	@echo ""
	@echo "📊 Information:"
	@echo "  make verify-manifest - Verify install/uninstall consistency"
	@echo "  make status          - Show project status"
	@echo "  make help            - Show this help message"
	@echo ""
	@echo "📖 Project Documentation:"
	@echo "  INSTALL.md           - Detailed installation guide"
	@echo "  README.md            - Project overview"
	@echo "  COMMANDS.md          - Complete command reference"
	@echo "  docs/integration/MCP_INTEGRATION_GUIDE.md - MCP setup and usage"
	@echo ""
