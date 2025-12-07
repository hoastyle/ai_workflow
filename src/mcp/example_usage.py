#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Gateway Usage Examples

Demonstrates how to use MCP Gateway in workflow commands.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.mcp.gateway import get_mcp_gateway


def example_1_basic_usage():
    """Example 1: Basic Gateway Usage"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Gateway Usage")
    print("=" * 60 + "\n")

    # Get global gateway instance
    gateway = get_mcp_gateway()

    # List all registered servers
    servers = gateway.list_servers()
    print(f"✅ Found {len(servers)} registered MCP servers:")
    for server in servers:
        print(f"   • {server}")

    print()


def example_2_check_availability():
    """Example 2: Check Server Availability (Auto-Degradation)"""
    print("\n" + "=" * 60)
    print("Example 2: Check Server Availability")
    print("=" * 60 + "\n")

    gateway = get_mcp_gateway()

    # Check if Serena is available
    if gateway.is_available("serena"):
        print("✅ Serena MCP is available")
        info = gateway.get_server_info("serena")
        print(f"   Command: {info['command']}")
        print(f"   Args: {' '.join(info['args'][:3])}...")
    else:
        print("❌ Serena MCP unavailable - falling back to standard mode")

    # Check Sequential-thinking
    if gateway.is_available("sequential-thinking"):
        print("✅ Sequential-thinking MCP is available")
    else:
        print("❌ Sequential-thinking unavailable")

    print()


def example_3_get_tool():
    """Example 3: Get Tool (Lazy Loading)"""
    print("\n" + "=" * 60)
    print("Example 3: Get Tool (Lazy Loading)")
    print("=" * 60 + "\n")

    gateway = get_mcp_gateway()

    # Get Serena read_memory tool (lazy loading)
    try:
        print("📦 Requesting tool: serena/read_memory")
        memory_tool = gateway.get_tool("serena", "read_memory")

        print(f"✅ Tool loaded: {memory_tool.name}")
        print(f"   Server: {memory_tool.server}")
        print(f"   Description: {memory_tool.description}")

        # Note: Actual tool call requires real MCP server connection
        # result = memory_tool.call(memory_name="project_overview")

    except ValueError as e:
        print(f"❌ Error: {e}")

    print()


def example_4_integration_pattern():
    """Example 4: Integration Pattern for wf_*.md Commands"""
    print("\n" + "=" * 60)
    print("Example 4: Integration Pattern for Workflow Commands")
    print("=" * 60 + "\n")

    gateway = get_mcp_gateway()

    # Simulated user args
    user_args = ["--think", "--c7"]

    print(f"User flags: {' '.join(user_args)}\n")

    # Pattern 1: Flag-based activation
    if "--think" in user_args:
        if gateway.is_available("sequential-thinking"):
            print("✅ Activating Sequential-thinking MCP")
            # think_tool = gateway.get_tool("sequential-thinking", "analyze")
            # result = think_tool.call(problem=user_question)
        else:
            print("⚠️  Sequential-thinking unavailable, using standard analysis")

    if "--c7" in user_args:
        if gateway.is_available("context7"):
            print("✅ Activating Context7 MCP for official docs")
            # docs_tool = gateway.get_tool("context7", "get_library_docs")
            # result = docs_tool.call(library_name=lib_name)
        else:
            print("⚠️  Context7 unavailable, using standard docs")

    print()


def example_5_shutdown():
    """Example 5: Proper Shutdown"""
    print("\n" + "=" * 60)
    print("Example 5: Gateway Shutdown")
    print("=" * 60 + "\n")

    gateway = get_mcp_gateway()

    # Shutdown gateway (close all connections)
    gateway.shutdown()
    print("✅ Gateway shutdown complete")

    print()


if __name__ == "__main__":
    print("\n" + "🚀 MCP Gateway Usage Examples")
    print("=" * 60)

    # Run examples
    example_1_basic_usage()
    example_2_check_availability()
    example_3_get_tool()
    example_4_integration_pattern()
    example_5_shutdown()

    print("✅ All examples completed\n")
