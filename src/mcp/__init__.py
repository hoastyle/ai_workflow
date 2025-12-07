"""
MCP (Model Context Protocol) Integration Module

Provides:
  - MCPGateway: Unified MCP server interface
  - MCPConfigManager: Configuration management
  - MCPToolRegistry: Tool lazy loading and compression
  - get_mcp_gateway(): Global gateway singleton
"""

from .gateway import (
    MCPGateway,
    MCPConfigManager,
    MCPToolRegistry,
    MCPTool,
    get_mcp_gateway,
)

__all__ = [
    "MCPGateway",
    "MCPConfigManager",
    "MCPToolRegistry",
    "MCPTool",
    "get_mcp_gateway",
]
