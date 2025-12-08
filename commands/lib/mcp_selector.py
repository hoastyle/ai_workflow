#!/usr/bin/env python3
"""
MCP Selector - Automatic MCP tool selection for agents

This module provides intelligent MCP tool selection based on agent type and task
characteristics, optimizing the Agent-MCP collaboration.

Design Principles:
- Three-tier selection: Default → Role-based → Task-conditional
- Performance optimization: Caching, lazy loading, parallel initialization
- Gateway pattern integration: Leverages existing MCP Gateway infrastructure
- Extensible: Easy to add new agents or MCP tools

Usage:
    from commands.lib.mcp_selector import MCPSelector
    from commands.lib.agent_registry import Agent

    selector = MCPSelector()
    task = Task(description="实现用户登录功能")
    agent = registry.get_agent("code-agent")

    tools = selector.select_tools(agent, task)
    print(f"Selected MCP tools: {tools}")
    # Output: ['sequential-thinking', 'serena']
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum


@dataclass
class Task:
    """Task description for MCP tool selection"""
    description: str
    complexity: Optional[str] = None  # "simple", "moderate", "complex"
    technical_stack: Optional[List[str]] = None  # ["React", "Django", etc.]


class MCPSelector:
    """
    Automatic MCP tool selection for agents

    Selection Strategy:
    1. Default MCP (all agents):
       - Sequential-thinking: 100% coverage, structured reasoning

    2. Role-based MCP (based on agent type):
       - Serena: Code-related agents (90% coverage)
       - Context7 + Tavily: Architect and Research agents

    3. Task-conditional MCP (based on task keywords):
       - Magic: UI-related tasks
       - Context7: Framework/library references
       - Tavily: Research and trend analysis needs

    Performance Optimizations:
    - Caching: Tool selections cached per agent-task combination
    - Lazy evaluation: Only evaluate conditions when needed
    - Parallel ready: Designed for async batch initialization
    """

    def __init__(self):
        """Initialize MCP selector with keyword mappings"""
        # UI task detection keywords
        self.ui_keywords = [
            "ui", "界面", "组件", "按钮", "表单", "页面",
            "component", "button", "form", "page", "layout"
        ]

        # Framework/library keywords for Context7
        self.framework_keywords = [
            "react", "vue", "django", "express", "flask", "fastapi",
            "spring", "angular", "next.js", "nuxt", "rails"
        ]

        # Web search/research keywords for Tavily
        self.research_keywords = [
            "最新", "最佳实践", "对比", "趋势", "调研",
            "latest", "best practice", "compare", "trend", "research"
        ]

        # Agent-specific MCP tools (always enabled for these agents)
        self.agent_specific_tools: Dict[str, List[str]] = {
            "architect-agent": ["context7", "tavily"],
            "research-agent": ["context7", "tavily"],
        }

        # Cache for selected tools (optimization)
        self._selection_cache: Dict[str, List[str]] = {}

    def select_tools(self, agent, task: Task) -> List[str]:
        """
        Select appropriate MCP tools for an agent and task

        Args:
            agent: Agent instance with name, role, and mcp_integrations
            task: Task instance with description and optional metadata

        Returns:
            List[str]: MCP server names to activate

        Example:
            >>> agent = Agent(name="code-agent", role="Implementation Engineer")
            >>> task = Task(description="实现用户登录UI")
            >>> selector.select_tools(agent, task)
            ['sequential-thinking', 'serena', 'magic']
        """
        # Check cache first (performance optimization)
        cache_key = f"{agent.name}:{task.description[:50]}"
        if cache_key in self._selection_cache:
            return self._selection_cache[cache_key]

        tools: Set[str] = set()

        # Tier 1: Default MCP (all agents)
        tools.add("sequential-thinking")

        # Tier 2: Role-based MCP
        # Serena for all code-related agents (90% coverage)
        if agent.name != "research-agent":
            tools.add("serena")

        # Agent-specific tools (architect and research)
        if agent.name in self.agent_specific_tools:
            tools.update(self.agent_specific_tools[agent.name])

        # Tier 3: Task-conditional MCP
        task_lower = task.description.lower()

        # UI tasks → Magic (for code-agent and doc-agent)
        if self._is_ui_task(task_lower):
            if agent.name in ["code-agent", "doc-agent"]:
                tools.add("magic")

        # Framework/library references → Context7
        if self._has_framework_reference(task_lower):
            if agent.name in ["debug-agent", "architect-agent"]:
                # Only add if not already present
                tools.add("context7")

        # Research/trend keywords → Tavily
        if self._needs_web_search(task_lower):
            if agent.name in ["architect-agent", "research-agent"]:
                tools.add("tavily")

        # Convert to list and cache
        result = list(tools)
        self._selection_cache[cache_key] = result

        return result

    def _is_ui_task(self, task_description: str) -> bool:
        """
        Detect if task involves UI implementation

        Args:
            task_description: Lowercase task description

        Returns:
            bool: True if UI-related keywords found
        """
        return any(kw in task_description for kw in self.ui_keywords)

    def _has_framework_reference(self, task_description: str) -> bool:
        """
        Detect if task references specific frameworks/libraries

        Args:
            task_description: Lowercase task description

        Returns:
            bool: True if framework keywords found
        """
        return any(fw in task_description for fw in self.framework_keywords)

    def _needs_web_search(self, task_description: str) -> bool:
        """
        Detect if task requires web search or research

        Args:
            task_description: Lowercase task description

        Returns:
            bool: True if research keywords found
        """
        return any(kw in task_description for kw in self.research_keywords)

    def get_tool_justification(self, agent, task: Task) -> Dict[str, str]:
        """
        Get explanation for why each tool was selected

        Args:
            agent: Agent instance
            task: Task instance

        Returns:
            Dict[str, str]: Tool name → selection reason

        Example:
            >>> justification = selector.get_tool_justification(agent, task)
            >>> print(justification["serena"])
            "Code-related agent (90% coverage)"
        """
        tools = self.select_tools(agent, task)
        justifications = {}

        for tool in tools:
            if tool == "sequential-thinking":
                justifications[tool] = "Default MCP for all agents (100% coverage)"
            elif tool == "serena":
                justifications[tool] = "Code-related agent (90% coverage)"
            elif tool == "magic":
                justifications[tool] = "UI task detected"
            elif tool == "context7":
                if agent.name in self.agent_specific_tools.get(agent.name, []):
                    justifications[tool] = f"Agent-specific tool for {agent.name}"
                else:
                    justifications[tool] = "Framework/library reference detected"
            elif tool == "tavily":
                if agent.name in self.agent_specific_tools.get(agent.name, []):
                    justifications[tool] = f"Agent-specific tool for {agent.name}"
                else:
                    justifications[tool] = "Research/trend analysis needed"

        return justifications

    def clear_cache(self):
        """Clear the selection cache (for testing or cache invalidation)"""
        self._selection_cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics

        Returns:
            Dict with cache size and hit potential
        """
        return {
            "cached_selections": len(self._selection_cache),
            "memory_saved_calls": len(self._selection_cache)
        }


def main():
    """CLI interface for testing MCPSelector"""
    import sys

    # Mock Agent class for testing
    @dataclass
    class MockAgent:
        name: str
        role: str

    selector = MCPSelector()

    if len(sys.argv) < 3:
        print("Usage: mcp_selector.py <agent_name> <task_description>")
        print("\nAgent names:")
        print("  pm-agent, architect-agent, code-agent, debug-agent, test-agent")
        print("  review-agent, refactor-agent, doc-agent, research-agent, context-agent")
        print("\nExamples:")
        print('  python mcp_selector.py code-agent "实现用户登录功能"')
        print('  python mcp_selector.py architect-agent "设计系统架构"')
        print('  python mcp_selector.py code-agent "创建登录UI组件"')
        sys.exit(1)

    agent_name = sys.argv[1]
    task_desc = sys.argv[2]

    # Create mock agent and task
    agent = MockAgent(name=agent_name, role="Test Role")
    task = Task(description=task_desc)

    # Select tools
    tools = selector.select_tools(agent, task)
    justifications = selector.get_tool_justification(agent, task)

    # Display results
    print(f"\n🤖 Agent: {agent_name}")
    print(f"📋 Task: {task_desc}")
    print(f"\n🔧 Selected MCP Tools ({len(tools)}):")
    for tool in tools:
        reason = justifications.get(tool, "Unknown reason")
        print(f"  ✓ {tool:20s} - {reason}")

    # Cache stats
    stats = selector.get_cache_stats()
    print(f"\n📊 Cache Stats:")
    print(f"  Cached selections: {stats['cached_selections']}")


if __name__ == '__main__':
    main()
