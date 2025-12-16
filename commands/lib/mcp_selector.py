#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Selector - Intelligent MCP Tool Selection for Agents

This module provides dynamic MCP tool selection based on agent responsibilities
and task complexity. It serves as a bridge between Agent Coordinator and MCP Gateway.

Design Principles:
- Agent-driven MCP selection (agents define their preferred MCP tools via mcp_integrations)
- Task complexity scoring (automatic detection of complexity features)
- Dynamic tool filtering (only recommend relevant tools for current task)
- Performance optimization (caching, batch queries, parallel calls)
- Gateway integration (checks MCP availability before recommendation)

Integration:
    from commands.lib.mcp_selector import MCPSelector, get_mcp_selector
    from commands.lib.agent_coordinator import get_agent_coordinator
    from src.mcp.gateway import get_mcp_gateway

    coordinator = get_agent_coordinator()
    selector = get_mcp_selector()  # Auto-creates with gateway

    agent_context = coordinator.intercept(task_description, "wf_05_code")
    if agent_context['auto_activated']:
        recommendations = selector.select_tools(
            agent=agent_context['agent'],
            task_description=task_description
        )
        print(selector.format_recommendations(recommendations))

Version: 2.0 (Phase 5 Task 5.2 Enhanced)
Date: 2025-12-13
Part of: Phase 5 Task 5.2 - Agent-MCP 协同模式实现
"""

import re
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass


@dataclass
class MCPToolRecommendation:
    """MCP tool recommendation with confidence score"""
    tool_name: str
    usage_description: str
    confidence: float  # 0.0-1.0
    reason: str
    priority: str  # "high", "medium", "low"

    def __str__(self) -> str:
        return f"{self.tool_name} ({self.confidence:.0%}) - {self.reason}"


@dataclass
class TaskComplexity:
    """Task complexity scoring result"""
    score: float  # 0.0-1.0
    features: Dict[str, bool]
    reasoning: str

    def __str__(self) -> str:
        return f"Complexity: {self.score:.0%} - {self.reasoning}"


# Legacy Task class for backward compatibility
@dataclass
class Task:
    """Task description for MCP tool selection (legacy)"""
    description: str
    complexity: Optional[str] = None  # "simple", "moderate", "complex"
    technical_stack: Optional[List[str]] = None  # ["React", "Django", etc.]


class MCPSelector:
    """
    Intelligent MCP Tool Selector

    Responsibilities:
    - Analyze task complexity and characteristics
    - Filter agent's MCP tools based on task relevance
    - Provide tool recommendations with confidence scores
    - Support batch and parallel MCP operations

    Architecture:
    - Layer 1: Task Analysis (complexity scoring, feature detection)
    - Layer 2: Tool Filtering (agent preferences + task requirements)
    - Layer 3: Recommendation (confidence scoring, priority ranking)

    Version 2.0 Changes (Phase 5 Task 5.2):
    - Agent-driven selection (reads from agent.mcp_integrations)
    - Confidence scoring system (0.0-1.0)
    - Gateway availability checking
    - Enhanced complexity analysis
    """

    # Complexity scoring weights
    COMPLEXITY_WEIGHTS = {
        "multifile": 0.15,        # Multiple files involved
        "architecture": 0.20,      # Architecture/design changes
        "integration": 0.15,       # Third-party integrations
        "algorithm": 0.15,         # Complex algorithms/logic
        "concurrent": 0.10,        # Concurrency/async handling
        "data_migration": 0.10,    # Database migrations
        "ui_component": 0.10,      # UI/frontend work
        "api_design": 0.05,        # API design/changes
    }

    # MCP tool capability matrix
    MCP_CAPABILITIES = {
        "Serena": {
            "capabilities": ["code_navigation", "symbol_search", "refactoring", "dependency_analysis"],
            "complexity_threshold": 0.3,
            "keywords": ["修改", "重构", "查找", "定位", "符号", "引用"],
        },
        "Sequential-thinking": {
            "capabilities": ["complex_logic", "decision_making", "planning", "decomposition"],
            "complexity_threshold": 0.5,
            "keywords": ["复杂", "决策", "规划", "分解", "算法", "逻辑"],
        },
        "Magic": {
            "capabilities": ["ui_generation", "component_design", "frontend"],
            "complexity_threshold": 0.0,
            "keywords": ["UI", "组件", "前端", "界面", "设计", "样式"],
        },
        "Context7": {
            "capabilities": ["documentation", "api_reference", "library_lookup"],
            "complexity_threshold": 0.0,
            "keywords": ["文档", "API", "库", "框架", "官方", "参考"],
        },
        "Tavily": {
            "capabilities": ["web_search", "research", "latest_info"],
            "complexity_threshold": 0.2,
            "keywords": ["搜索", "研究", "最新", "方案", "对比", "开源"],
        },
    }

    # Keyword constants (extracted from __init__ for performance)
    UI_KEYWORDS = [
        "ui", "界面", "组件", "按钮", "表单", "页面",
        "component", "button", "form", "page", "layout"
    ]

    FRAMEWORK_KEYWORDS = [
        "react", "vue", "django", "express", "flask", "fastapi",
        "spring", "angular", "next.js", "nuxt", "rails"
    ]

    RESEARCH_KEYWORDS = [
        "最新", "最佳实践", "对比", "趋势", "调研",
        "latest", "best practice", "compare", "trend", "research"
    ]

    AGENT_SPECIFIC_TOOLS = {
        "architect-agent": ["context7", "tavily"],
        "research-agent": ["context7", "tavily"],
    }

    # Pre-compiled regex patterns for task complexity analysis
    FEATURE_PATTERNS = {
        "multifile": re.compile(r"(多个文件|多文件|跨文件|多模块|几个文件)", re.IGNORECASE),
        "architecture": re.compile(r"(架构|设计|重构|模式|系统)", re.IGNORECASE),
        "integration": re.compile(r"(集成|API|第三方|外部|接口)", re.IGNORECASE),
        "algorithm": re.compile(r"(算法|逻辑|计算|复杂|性能)", re.IGNORECASE),
        "concurrent": re.compile(r"(并发|异步|多线程|并行|concurrent|async)", re.IGNORECASE),
        "data_migration": re.compile(r"(迁移|数据库|schema|migration)", re.IGNORECASE),
        "ui_component": re.compile(r"(UI|组件|前端|界面|页面|component)", re.IGNORECASE),
        "api_design": re.compile(r"(API|endpoint|路由|接口设计)", re.IGNORECASE),
    }

    def __init__(self, gateway=None):
        """
        Initialize MCP selector with gateway

        Args:
            gateway: Optional MCP Gateway instance (for availability checking)

        Note:
            All keyword lists and regex patterns are now class-level constants
            for better performance (no repeated allocation/compilation).
        """
        self.gateway = gateway

        # Cache for selected tools (performance optimization)
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
        if agent.name in self.AGENT_SPECIFIC_TOOLS:
            tools.update(self.AGENT_SPECIFIC_TOOLS[agent.name])

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
        return any(kw in task_description for kw in self.UI_KEYWORDS)

    def _has_framework_reference(self, task_description: str) -> bool:
        """
        Detect if task references specific frameworks/libraries

        Args:
            task_description: Lowercase task description

        Returns:
            bool: True if framework keywords found
        """
        return any(fw in task_description for fw in self.FRAMEWORK_KEYWORDS)

    def _needs_web_search(self, task_description: str) -> bool:
        """
        Detect if task requires web search or research

        Args:
            task_description: Lowercase task description

        Returns:
            bool: True if research keywords found
        """
        return any(kw in task_description for kw in self.RESEARCH_KEYWORDS)

    # =========================================================================
    # V2 API - Enhanced MCP Selection with Confidence Scoring
    # =========================================================================

    def select_tools_v2(
        self,
        agent,
        task_description: str,
        auto_filter: bool = True
    ) -> List[MCPToolRecommendation]:
        """
        Select MCP tools for an agent based on task requirements (V2 API)

        Args:
            agent: Agent object with mcp_integrations list
            task_description: User's task description
            auto_filter: Automatically filter irrelevant tools (default: True)

        Returns:
            List of MCPToolRecommendation objects, sorted by confidence (high to low)
        """
        # Step 1: Analyze task complexity
        complexity = self._analyze_complexity_v2(task_description)

        # Step 2: Get agent's preferred MCP tools
        agent_tools = self._extract_agent_mcp_tools(agent)

        # Step 3: Filter tools based on task requirements
        recommendations = []
        for tool_name, usage_desc in agent_tools.items():
            confidence, reason = self._calculate_tool_confidence(
                tool_name=tool_name,
                task_description=task_description,
                complexity=complexity,
                usage_desc=usage_desc
            )

            # Apply auto-filtering (skip low-confidence tools)
            if auto_filter and confidence < 0.3:
                continue

            # Determine priority based on confidence
            if confidence >= 0.7:
                priority = "high"
            elif confidence >= 0.5:
                priority = "medium"
            else:
                priority = "low"

            # Check if tool is available in gateway
            if self.gateway and hasattr(self.gateway, 'is_available'):
                if not self.gateway.is_available(tool_name.lower()):
                    reason += " (⚠️ MCP 不可用)"
                    priority = "low"

            recommendations.append(MCPToolRecommendation(
                tool_name=tool_name,
                usage_description=usage_desc,
                confidence=confidence,
                reason=reason,
                priority=priority
            ))

        # Sort by confidence (high to low)
        recommendations.sort(key=lambda r: r.confidence, reverse=True)

        return recommendations

    def _analyze_complexity_v2(self, task_description: str) -> TaskComplexity:
        """
        Analyze task complexity based on description (V2 Enhanced)

        Args:
            task_description: User's task description

        Returns:
            TaskComplexity object with score and feature breakdown
        """
        features = {}
        score = 0.0

        # Feature detection using pre-compiled regex patterns (performance optimized)
        for feature, compiled_pattern in self.FEATURE_PATTERNS.items():
            if compiled_pattern.search(task_description):
                features[feature] = True
                score += self.COMPLEXITY_WEIGHTS.get(feature, 0.0)
            else:
                features[feature] = False

        # Cap score at 1.0
        score = min(score, 1.0)

        # Generate reasoning
        detected_features = [k for k, v in features.items() if v]
        if detected_features:
            reasoning = f"检测到特征: {', '.join(detected_features)}"
        else:
            reasoning = "简单任务，无复杂特征"

        return TaskComplexity(
            score=score,
            features=features,
            reasoning=reasoning
        )

    def _extract_agent_mcp_tools(self, agent) -> Dict[str, str]:
        """
        Extract MCP tools from agent's mcp_integrations

        Args:
            agent: Agent object

        Returns:
            Dict mapping tool_name -> usage_description
        """
        tools = {}
        if hasattr(agent, 'mcp_integrations'):
            for integration in agent.mcp_integrations:
                tool_name = integration.get("name", "")
                usage = integration.get("usage", "")
                if tool_name:
                    tools[tool_name] = usage

        return tools

    def _calculate_tool_confidence(
        self,
        tool_name: str,
        task_description: str,
        complexity: TaskComplexity,
        usage_desc: str
    ) -> Tuple[float, str]:
        """
        Calculate confidence score for a specific MCP tool

        Args:
            tool_name: MCP tool name (e.g., "Serena", "Sequential-thinking")
            task_description: User's task description
            complexity: TaskComplexity object
            usage_desc: Agent's usage description for this tool

        Returns:
            Tuple of (confidence_score, reasoning)
        """
        confidence = 0.5  # Base confidence
        reasons = []

        # Check if tool exists in capability matrix
        if tool_name not in self.MCP_CAPABILITIES:
            return (0.3, f"工具未在能力矩阵中定义")

        tool_info = self.MCP_CAPABILITIES[tool_name]

        # Factor 1: Keyword matching (30% weight)
        keywords = tool_info.get("keywords", [])
        keyword_matches = sum(
            1 for keyword in keywords
            if keyword.lower() in task_description.lower()
        )
        if keyword_matches > 0:
            keyword_confidence = min(keyword_matches * 0.15, 0.3)
            confidence += keyword_confidence
            reasons.append(f"关键词匹配 ({keyword_matches} 个)")

        # Factor 2: Complexity threshold (30% weight)
        complexity_threshold = tool_info.get("complexity_threshold", 0.0)
        if complexity.score >= complexity_threshold:
            complexity_boost = min((complexity.score - complexity_threshold) * 0.5, 0.3)
            confidence += complexity_boost
            if complexity_boost > 0:
                reasons.append(f"复杂度匹配 ({complexity.score:.0%})")
        else:
            # Penalize if below threshold
            confidence -= 0.1
            reasons.append(f"复杂度低于阈值")

        # Factor 3: Feature alignment (40% weight)
        capabilities = tool_info.get("capabilities", [])
        feature_alignment = self._calculate_feature_alignment(
            capabilities=capabilities,
            complexity_features=complexity.features
        )
        confidence += feature_alignment * 0.4
        if feature_alignment > 0.3:
            reasons.append(f"特征对齐 ({feature_alignment:.0%})")

        # Cap confidence at [0.0, 1.0]
        confidence = max(0.0, min(confidence, 1.0))

        # Generate final reasoning
        if reasons:
            reason = f"{tool_name}: " + ", ".join(reasons)
        else:
            reason = f"{tool_name}: 基础匹配"

        return (confidence, reason)

    def _calculate_feature_alignment(
        self,
        capabilities: List[str],
        complexity_features: Dict[str, bool]
    ) -> float:
        """
        Calculate alignment between tool capabilities and task features

        Args:
            capabilities: List of tool capabilities
            complexity_features: Dict of detected task features

        Returns:
            Alignment score (0.0-1.0)
        """
        # Capability-to-feature mapping
        capability_mapping = {
            "code_navigation": ["multifile", "architecture"],
            "symbol_search": ["multifile", "integration"],
            "refactoring": ["architecture", "multifile"],
            "dependency_analysis": ["integration", "multifile"],
            "complex_logic": ["algorithm", "concurrent"],
            "decision_making": ["architecture", "algorithm"],
            "planning": ["architecture", "multifile"],
            "decomposition": ["algorithm", "multifile"],
            "ui_generation": ["ui_component"],
            "component_design": ["ui_component", "architecture"],
            "frontend": ["ui_component"],
            "documentation": ["api_design", "architecture"],
            "api_reference": ["integration", "api_design"],
            "library_lookup": ["integration"],
            "web_search": ["integration", "architecture"],
            "research": ["architecture", "integration"],
            "latest_info": ["integration"],
        }

        total_alignment = 0.0
        for capability in capabilities:
            related_features = capability_mapping.get(capability, [])
            for feature in related_features:
                if complexity_features.get(feature, False):
                    total_alignment += 1.0

        # Normalize by number of capabilities
        if len(capabilities) > 0:
            return min(total_alignment / len(capabilities), 1.0)
        else:
            return 0.0

    # =========================================================================
    # End of V2 API
    # =========================================================================

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
                if agent.name in self.AGENT_SPECIFIC_TOOLS:
                    justifications[tool] = f"Agent-specific tool for {agent.name}"
                else:
                    justifications[tool] = "Framework/library reference detected"
            elif tool == "tavily":
                if agent.name in self.AGENT_SPECIFIC_TOOLS:
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


    def format_recommendations(
        self,
        recommendations: List[MCPToolRecommendation],
        verbose: bool = False
    ) -> str:
        """
        Format tool recommendations for display

        Args:
            recommendations: List of MCPToolRecommendation
            verbose: Include detailed reasoning (default: False)

        Returns:
            Formatted string for display
        """
        if not recommendations:
            return "ℹ️ 无可用的 MCP 工具推荐"

        lines = ["## 🛠️ MCP 工具推荐\n"]

        for idx, rec in enumerate(recommendations, 1):
            # Priority emoji
            priority_emoji = {
                "high": "🔴",
                "medium": "🟠",
                "low": "🟡"
            }.get(rec.priority, "⚪")

            # Confidence indicator
            conf_pct = f"{rec.confidence:.0%}"

            lines.append(f"{idx}. {priority_emoji} **{rec.tool_name}** ({conf_pct})")
            lines.append(f"   - 用途: {rec.usage_description}")

            if verbose:
                lines.append(f"   - 推荐原因: {rec.reason}")

            lines.append("")

        return "\n".join(lines)


# Convenience functions
def get_mcp_selector(gateway=None):
    """
    Get MCPSelector instance (creates with gateway if needed)

    Args:
        gateway: Optional MCP Gateway instance

    Returns:
        MCPSelector instance
    """
    if gateway is None:
        try:
            from src.mcp.gateway import get_mcp_gateway
            gateway = get_mcp_gateway()
        except ImportError:
            # Gateway not available, create selector without it
            pass

    return MCPSelector(gateway=gateway)


def main():
    """CLI interface for testing MCPSelector (V2 Enhanced)"""
    import sys

    # Mock Agent class for testing
    @dataclass
    class MockAgent:
        name: str
        role: str
        mcp_integrations: List[Dict] = None

        def __post_init__(self):
            if self.mcp_integrations is None:
                # Default MCP integrations for testing
                self.mcp_integrations = [
                    {"name": "Serena", "usage": "Code navigation and refactoring"},
                    {"name": "Sequential-thinking", "usage": "Complex logic decomposition"},
                    {"name": "Magic", "usage": "UI component generation"},
                ]

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

    # Create mock agent
    agent = MockAgent(name=agent_name, role="Test Role")

    # V2: Enhanced selection with recommendations
    print("\n=== MCPSelector V2 (Phase 5) ===")
    print(f"🤖 Agent: {agent_name}")
    print(f"📋 Task: {task_desc}\n")

    try:
        # New API: select_tools_v2 with recommendations
        recommendations = selector.select_tools_v2(agent, task_desc)

        if recommendations:
            print(selector.format_recommendations(recommendations, verbose=True))
        else:
            print("ℹ️ No MCP tools recommended for this task")

    except AttributeError:
        # Fallback to legacy API
        print("⚠️ Using legacy API (V1)")
        task = Task(description=task_desc)
        tools = selector.select_tools(agent, task)
        justifications = selector.get_tool_justification(agent, task)

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
