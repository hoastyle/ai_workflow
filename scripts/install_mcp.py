#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server Installation Tool for AI Workflow Command System

Installs and manages MCP (Model Context Protocol) servers using the Claude CLI.
Based on SuperClaude Framework implementation patterns.

Version: 1.0
Date: 2025-11-22
"""

import json
import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# MCP Server Registry - Real public MCP servers
MCP_SERVERS = {
    # Anthropic Official Servers
    "sequential-thinking": {
        "name": "sequential-thinking",
        "description": "Multi-step problem solving and systematic analysis",
        "transport": "stdio",
        "command": "npx -y @modelcontextprotocol/server-sequential-thinking",
        "required": False,
        "source": "Anthropic Official",
        "docs": "https://github.com/modelcontextprotocol/servers"
    },
    "github": {
        "name": "github",
        "description": "GitHub repository and issue management",
        "transport": "stdio",
        "command": "npx -y @modelcontextprotocol/server-github",
        "required": False,
        "api_key_env": "GITHUB_TOKEN",
        "api_key_description": "GitHub Personal Access Token",
        "source": "Anthropic Official",
        "docs": "https://github.com/modelcontextprotocol/servers"
    },
    "postgres": {
        "name": "postgres",
        "description": "PostgreSQL database query and management",
        "transport": "stdio",
        "command": "npx -y @modelcontextprotocol/server-postgres",
        "required": False,
        "api_key_env": "DATABASE_URL",
        "api_key_description": "PostgreSQL connection string (postgresql://user:pass@host/db)",
        "source": "Anthropic Official",
        "docs": "https://github.com/modelcontextprotocol/servers"
    },
    "puppeteer": {
        "name": "puppeteer",
        "description": "Browser automation and web scraping",
        "transport": "stdio",
        "command": "npx -y @modelcontextprotocol/server-puppeteer",
        "required": False,
        "source": "Anthropic Official",
        "docs": "https://github.com/modelcontextprotocol/servers"
    },
    "google-drive": {
        "name": "google-drive",
        "description": "Google Drive file access and management",
        "transport": "stdio",
        "command": "npx -y @modelcontextprotocol/server-google-drive",
        "required": False,
        "api_key_env": "GOOGLE_API_KEY",
        "api_key_description": "Google API credentials (requires OAuth2 setup)",
        "source": "Anthropic Official",
        "docs": "https://github.com/modelcontextprotocol/servers"
    },
    "slack": {
        "name": "slack",
        "description": "Slack workspace and message management",
        "transport": "stdio",
        "command": "npx -y @modelcontextprotocol/server-slack",
        "required": False,
        "api_key_env": "SLACK_BOT_TOKEN",
        "api_key_description": "Slack Bot API Token (xoxb-...)",
        "source": "Anthropic Official",
        "docs": "https://github.com/modelcontextprotocol/servers"
    },

    # Community and Enterprise Servers
    "tavily": {
        "name": "tavily",
        "description": "Web search and real-time information retrieval",
        "transport": "stdio",
        "command": "npx -y tavily-mcp@0.1.2",
        "required": False,
        "api_key_env": "TAVILY_API_KEY",
        "api_key_description": "Tavily API key from https://app.tavily.com",
        "source": "Community (Tavily)",
        "docs": "https://github.com/tavily-ai/tavily-python"
    },
    "context7": {
        "name": "context7",
        "description": "Official library documentation and code examples",
        "transport": "stdio",
        "command": "npx -y @upstash/context7-mcp@latest",
        "required": False,
        "source": "Community (Upstash)",
        "docs": "https://github.com/upstash/context7-mcp"
    },
    "playwright": {
        "name": "playwright",
        "description": "Cross-browser E2E testing and automation",
        "transport": "stdio",
        "command": "npx -y @playwright/mcp@latest",
        "required": False,
        "source": "Community (Playwright)",
        "docs": "https://github.com/microsoft/playwright"
    },
    "magic": {
        "name": "magic",
        "description": "Modern UI component generation and design systems",
        "transport": "stdio",
        "command": "npx -y @21st-dev/magic",
        "required": False,
        "api_key_env": "TWENTYFIRST_API_KEY",
        "api_key_description": "21st.dev API key for UI component generation",
        "source": "Community (21st.dev)",
        "docs": "https://21st.dev"
    },
    "serena": {
        "name": "serena",
        "description": "Semantic code analysis and intelligent editing",
        "transport": "stdio",
        "command": "uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false",
        "required": False,
        "source": "Community (Serena)",
        "docs": "https://github.com/oraios/serena"
    },
    "morphllm-fast-apply": {
        "name": "morphllm-fast-apply",
        "description": "Fast Apply capability for context-aware code modifications",
        "transport": "stdio",
        "command": "npx -y @morph-llm/morph-fast-apply",
        "required": False,
        "api_key_env": "MORPH_API_KEY",
        "api_key_description": "Morph API key for Fast Apply",
        "source": "Community (Morph LLM)",
        "docs": "https://github.com/morph-llm"
    },
    "chrome-devtools": {
        "name": "chrome-devtools",
        "description": "Chrome DevTools debugging and performance analysis",
        "transport": "stdio",
        "command": "npx -y chrome-devtools-mcp@latest",
        "required": False,
        "source": "Community",
        "docs": "https://github.com/browsertools/chrome-devtools-mcp"
    },
}

# Color output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


def echo(message: str, color: str = Colors.NC) -> None:
    """Print colored message."""
    print(f"{color}{message}{Colors.NC}")


def run_command(cmd: List[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run a command with proper cross-platform shell handling.

    Args:
        cmd: Command as list of strings
        **kwargs: Additional subprocess.run arguments

    Returns:
        CompletedProcess result
    """
    if platform.system() == "Windows":
        cmd = ["cmd", "/c"] + cmd
        return subprocess.run(cmd, **kwargs)
    else:
        cmd_str = " ".join(shlex.quote(str(arg)) for arg in cmd)
        user_shell = os.environ.get("SHELL", "/bin/bash")
        return subprocess.run(
            cmd_str, shell=True, env=os.environ, executable=user_shell, **kwargs
        )


def check_prerequisites() -> Tuple[bool, List[str]]:
    """Check if required tools are available."""
    errors = []

    # Check Claude CLI
    try:
        result = run_command(
            ["claude", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            errors.append("Claude CLI not found - required for MCP server management")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        errors.append("Claude CLI not found - required for MCP server management")

    # Check Node.js for npm-based servers
    try:
        result = run_command(
            ["node", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            errors.append("Node.js not found - required for npm-based MCP servers")
        else:
            version = result.stdout.strip()
            try:
                version_num = int(version.lstrip("v").split(".")[0])
                if version_num < 18:
                    errors.append(f"Node.js version {version} found, but version 18+ required")
            except (ValueError, IndexError):
                pass
    except (subprocess.TimeoutExpired, FileNotFoundError):
        errors.append("Node.js not found - required for npm-based MCP servers")

    return len(errors) == 0, errors


def check_mcp_server_installed(server_name: str) -> bool:
    """Check if an MCP server is already installed."""
    try:
        result = run_command(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            output = result.stdout.lower()
            return server_name.lower() in output
        return False
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False


def prompt_for_api_key(
    server_name: str, env_var: str, description: str
) -> Optional[str]:
    """Prompt user for API key if needed."""
    echo(f"\n🔑 MCP server '{server_name}' requires an API key", Colors.YELLOW)
    echo(f"   Environment variable: {env_var}")
    echo(f"   Description: {description}")

    # Check if already set in environment
    if os.getenv(env_var):
        echo(f"   ✅ {env_var} already set in environment", Colors.GREEN)
        return os.getenv(env_var)

    # Prompt user
    response = input(f"   Would you like to set {env_var} now? (y/n) [y]: ").strip().lower()
    if response != 'n':
        api_key = input(f"   Enter {env_var}: ").strip()
        if api_key:
            return api_key

    echo(f"   ⚠️  Proceeding without {env_var} - server may not function properly",
         Colors.YELLOW)
    return None


def install_mcp_server(
    server_info: Dict, scope: str = "user", dry_run: bool = False
) -> bool:
    """
    Install a single MCP server using Claude CLI.

    Args:
        server_info: Server configuration dictionary
        scope: Installation scope (user, project, local)
        dry_run: If True, only show what would be done

    Returns:
        True if successful, False otherwise
    """
    server_name = server_info["name"]
    transport = server_info["transport"]
    command = server_info["command"]

    echo(f"📦 Installing MCP server: {server_name}", Colors.BLUE)

    # Check if already installed
    if check_mcp_server_installed(server_name):
        echo(f"   ✅ Already installed: {server_name}", Colors.GREEN)
        return True

    # Handle API key requirements
    env_args = []
    if "api_key_env" in server_info:
        api_key_env = server_info["api_key_env"]
        api_key = prompt_for_api_key(
            server_name,
            api_key_env,
            server_info.get("api_key_description", f"API key for {server_name}"),
        )
        if api_key:
            env_args = ["-e", f"{api_key_env}={api_key}"]

    # Build installation command
    cmd = ["claude", "mcp", "add", "--transport", transport]

    if scope != "local":
        cmd.extend(["--scope", scope])

    if env_args:
        cmd.extend(env_args)

    cmd.append(server_name)
    cmd.append("--")
    cmd.extend(shlex.split(command))

    if dry_run:
        echo(f"   [DRY RUN] Would run: {' '.join(cmd)}", Colors.YELLOW)
        return True

    try:
        echo(f"   Running: claude mcp add --transport {transport} {server_name} -- {command}",
             Colors.CYAN)
        result = run_command(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            echo(f"   ✅ Successfully installed: {server_name}", Colors.GREEN)
            return True
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            echo(f"   ❌ Failed to install {server_name}: {error_msg}", Colors.RED)
            return False

    except subprocess.TimeoutExpired:
        echo(f"   ❌ Timeout installing {server_name}", Colors.RED)
        return False
    except Exception as e:
        echo(f"   ❌ Error installing {server_name}: {e}", Colors.RED)
        return False


def list_available_servers() -> None:
    """List all available MCP servers."""
    echo("\n📋 Available MCP Servers:\n", Colors.CYAN)

    for server_key, server_info in MCP_SERVERS.items():
        name = server_info["name"]
        description = server_info["description"]
        source = server_info.get("source", "Unknown")
        api_key_note = ""

        if "api_key_env" in server_info:
            api_key_note = f" (requires {server_info['api_key_env']})"

        # Check if installed
        is_installed = check_mcp_server_installed(name)
        status = "✅ installed" if is_installed else "⬜ not installed"

        echo(f"   {name:25} {status}", Colors.GREEN if is_installed else Colors.YELLOW)
        echo(f"      {description}{api_key_note}")
        echo(f"      Source: {source}")
        echo(f"      Docs: {server_info.get('docs', 'N/A')}")
        echo("")

    echo(f"Total: {len(MCP_SERVERS)} servers available", Colors.CYAN)


def install_mcp_servers(
    selected_servers: Optional[List[str]] = None,
    scope: str = "user",
    dry_run: bool = False,
    interactive: bool = True,
) -> Tuple[bool, str]:
    """
    Install MCP servers for Claude Code.

    Args:
        selected_servers: List of server names to install, or None for interactive selection
        scope: Installation scope (user, project, local)
        dry_run: If True, only show what would be done
        interactive: If True, prompt for server selection

    Returns:
        Tuple of (success, message)
    """
    # Check prerequisites
    success, errors = check_prerequisites()
    if not success:
        error_msg = "Prerequisites not met:\n" + "\n".join(f"  ❌ {e}" for e in errors)
        return False, error_msg

    # Determine which servers to install
    servers_to_install = []

    if selected_servers:
        # Use explicitly selected servers
        for server_name in selected_servers:
            if server_name in MCP_SERVERS:
                servers_to_install.append(server_name)
            else:
                echo(f"⚠️  Unknown server: {server_name}", Colors.YELLOW)
    elif interactive:
        # Interactive selection
        echo("\n🎯 Select MCP servers to install:\n", Colors.BLUE)
        for i, (key, server_info) in enumerate(MCP_SERVERS.items(), 1):
            echo(f"   {i}. {server_info['name']:25} - {server_info['description']}")

        echo(f"\n   a. Install All")
        echo(f"   n. Install None")
        response = input("\nEnter selection (comma-separated numbers or 'a'/'n') [a]: ").strip().lower()

        if response == 'a' or response == '':
            servers_to_install = list(MCP_SERVERS.keys())
        elif response != 'n':
            try:
                selected_indices = [int(x.strip()) - 1 for x in response.split(',')]
                server_list = list(MCP_SERVERS.keys())
                servers_to_install = [server_list[i] for i in selected_indices if 0 <= i < len(server_list)]
            except (ValueError, IndexError):
                return False, "Invalid selection"

    # Install selected servers
    failed_servers = []
    for server_name in servers_to_install:
        if server_name in MCP_SERVERS:
            if not install_mcp_server(MCP_SERVERS[server_name], scope, dry_run):
                failed_servers.append(server_name)

    if failed_servers:
        msg = f"⚠️  {len(failed_servers)} server(s) failed to install: {', '.join(failed_servers)}"
        return False, msg
    else:
        msg = f"✅ Successfully installed {len(servers_to_install)} MCP server(s)"
        return True, msg


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Install and manage MCP (Model Context Protocol) servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive selection (default)
  %(prog)s

  # Install all servers
  %(prog)s --all

  # Install specific servers
  %(prog)s --servers sequential-thinking,tavily,github

  # List available servers
  %(prog)s --list

  # Dry run
  %(prog)s --all --dry-run
        """
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Install all available MCP servers"
    )
    parser.add_argument(
        "--servers",
        type=str,
        help="Comma-separated list of server names to install"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available MCP servers"
    )
    parser.add_argument(
        "--scope",
        choices=["user", "project", "local"],
        default="user",
        help="Installation scope (default: user)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it"
    )

    args = parser.parse_args()

    # Show header
    echo("\n" + "="*50, Colors.CYAN)
    echo("MCP Server Installation Tool v1.0", Colors.CYAN)
    echo("="*50 + "\n", Colors.CYAN)

    # List servers and exit
    if args.list:
        list_available_servers()
        return 0

    # Determine servers to install
    selected_servers = None
    interactive = True

    if args.all:
        selected_servers = list(MCP_SERVERS.keys())
        interactive = False
    elif args.servers:
        selected_servers = [s.strip() for s in args.servers.split(",")]
        interactive = False

    # Install servers
    success, message = install_mcp_servers(
        selected_servers=selected_servers,
        scope=args.scope,
        dry_run=args.dry_run,
        interactive=interactive
    )

    echo(f"\n{message}\n", Colors.GREEN if success else Colors.RED)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
