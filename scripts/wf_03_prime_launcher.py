#!/usr/bin/env python3
"""
wf_03_prime 启动器 - 带有 Serena MCP 连接检查和自动降级

功能：
1. 检查 Serena MCP 连接状态
2. 自动选择合适的加载模式
3. 在 Serena 不可用时自动降级
4. 提供诊断信息和日志
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.mcp.serena_manager import get_wf03_adapter, should_use_serena


def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )


def print_header():
    """打印启动头"""
    print("\n" + "=" * 70)
    print("🚀 wf_03_prime 启动器 v2.0 (带 Serena MCP 连接检查)")
    print("=" * 70 + "\n")


def print_mode_info(mode: str, strategy: dict):
    """打印模式信息"""
    mode_names = {
        "serena": "Serena 智能加载模式",
        "traditional": "传统文件读取模式"
    }

    print(f"📍 执行模式: {mode_names.get(mode, '未知模式')}")
    print(f"   - MCP 增强: {'启用' if strategy.get('use_mcp') else '禁用'}")
    print(f"   - LSP 索引: {'启用' if strategy.get('enable_lsp') else '禁用'}")
    print(f"   - 超时时间: {strategy.get('timeout', '?')}s")

    if strategy.get('features'):
        print(f"   - 可用功能: {', '.join(strategy['features'])}")

    print()


def print_recommendations(adapter):
    """打印建议"""
    if not adapter.serena.is_available():
        print("⚠️  Serena MCP 连接失败")
        print("   可能的原因：")
        print("   1. Serena 服务器未启动或崩溃")
        print("   2. 网络连接问题")
        print("   3. 项目代码库过大，LSP 初始化超时")
        print()
        print("💡 建议解决方案：")
        print("   • 方案 1: 重启 Claude Code 以重新启动 Serena")
        print("   • 方案 2: 优化 .gitignore，排除大文件夹")
        print("   • 方案 3: 运行 scripts/diagnose_mcp.sh 进行诊断")
        print("   • 方案 4: 在 ~/.claude/mcp.json 中禁用 Serena（临时方案）")
        print()


def main():
    """主函数"""
    setup_logging()
    print_header()

    # 获取适配器
    adapter = get_wf03_adapter()

    # 检测模式
    mode = adapter.detect_mode()
    strategy = adapter.get_load_strategy()

    # 显示模式信息
    print_mode_info(mode, strategy)

    # 如果不是 Serena 模式，显示建议
    if mode != "serena":
        print_recommendations(adapter)

    # 输出诊断信息（可选）
    if os.environ.get("WF03_VERBOSE"):
        print("\n📊 详细诊断信息：")
        adapter.log_diagnostics()

    print("=" * 70)
    print("✅ 启动器准备完成\n")

    # 返回模式给调用者
    return 0 if mode else 1


if __name__ == "__main__":
    sys.exit(main())
