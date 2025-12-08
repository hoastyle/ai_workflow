"""
Integration tests for MCPSelector

Tests the automatic MCP tool selection logic based on agent and task context.
"""

import unittest
from unittest.mock import MagicMock, patch
from commands.lib.mcp_selector import MCPSelector, Task
from commands.lib.agent_registry import Agent


class TestMCPSelector(unittest.TestCase):
    """Test suite for MCPSelector functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.selector = MCPSelector()

        # Create mock agents
        self.code_agent = Agent(
            name="code-agent",
            role="Code Implementation Specialist",
            expertise=["代码实现", "设计模式", "最佳实践"],
            activation_keywords=["实现", "代码", "功能"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "magic", "usage": "UI生成", "activation_condition": "conditional",
                 "keywords": ["ui", "界面", "组件"]},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ]
        )

        self.research_agent = Agent(
            name="research-agent",
            role="Technical Researcher",
            expertise=["技术调研", "方案评估"],
            activation_keywords=["研究", "调研", "评估"],
            mcp_integrations=[
                {"name": "context7", "usage": "文档查询", "activation_condition": "always"},
                {"name": "tavily", "usage": "Web搜索", "activation_condition": "always"},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ]
        )

        self.debug_agent = Agent(
            name="debug-agent",
            role="Debug Specialist",
            expertise=["调试", "错误分析"],
            activation_keywords=["调试", "debug", "错误"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "context7", "usage": "框架文档", "activation_condition": "conditional",
                 "keywords": ["react", "vue", "django"]},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ]
        )

    def test_tier1_default_mcp_always_included(self):
        """Test: Sequential-thinking is always included (Tier 1)"""
        task = Task(description="任意任务描述")

        # Test with code-agent
        tools = self.selector.select_tools(self.code_agent, task)
        self.assertIn("sequential-thinking", tools)

        # Test with research-agent
        tools = self.selector.select_tools(self.research_agent, task)
        self.assertIn("sequential-thinking", tools)

    def test_tier2_role_based_serena_included(self):
        """Test: Serena is included for all agents except research-agent (Tier 2)"""
        task = Task(description="代码实现任务")

        # Code-agent should have Serena
        tools = self.selector.select_tools(self.code_agent, task)
        self.assertIn("serena", tools)

        # Research-agent should NOT have Serena
        tools = self.selector.select_tools(self.research_agent, task)
        self.assertNotIn("serena", tools)

    def test_tier3_ui_task_magic_activation(self):
        """Test: Magic is activated for UI-related tasks (Tier 3)"""
        ui_task = Task(description="实现用户界面登录页面组件")
        non_ui_task = Task(description="实现数据库查询逻辑")

        # UI task should activate Magic for code-agent
        tools = self.selector.select_tools(self.code_agent, ui_task)
        self.assertIn("magic", tools)

        # Non-UI task should NOT activate Magic
        tools = self.selector.select_tools(self.code_agent, non_ui_task)
        self.assertNotIn("magic", tools)

    def test_tier3_framework_task_context7_activation(self):
        """Test: Context7 is conditionally activated for framework references"""
        framework_task = Task(description="调试React组件渲染问题")
        generic_task = Task(description="调试逻辑错误")

        # Framework task should activate Context7 for debug-agent
        tools = self.selector.select_tools(self.debug_agent, framework_task)
        self.assertIn("context7", tools)

        # Generic task should NOT activate conditional Context7
        tools = self.selector.select_tools(self.debug_agent, generic_task)
        self.assertNotIn("context7", tools)

    def test_research_agent_always_has_tavily_and_context7(self):
        """Test: Research-agent always has Tavily and Context7"""
        task = Task(description="调研缓存技术方案")

        tools = self.selector.select_tools(self.research_agent, task)
        self.assertIn("tavily", tools)
        self.assertIn("context7", tools)
        self.assertNotIn("serena", tools)  # Research-agent doesn't use Serena

    def test_ui_keywords_detection(self):
        """Test: UI keyword detection works for various UI terms"""
        ui_keywords = ["界面", "组件", "按钮", "表单", "页面", "component", "button", "form", "layout"]

        for keyword in ui_keywords:
            task = Task(description=f"实现{keyword}功能")
            tools = self.selector.select_tools(self.code_agent, task)
            self.assertIn("magic", tools, f"Magic should be activated for keyword: {keyword}")

    def test_framework_keywords_detection(self):
        """Test: Framework keyword detection for Context7"""
        frameworks = ["react", "vue", "django", "express", "fastapi", "spring", "next.js"]

        for framework in frameworks:
            task = Task(description=f"调试{framework}应用问题")
            tools = self.selector.select_tools(self.debug_agent, task)
            self.assertIn("context7", tools, f"Context7 should be activated for: {framework}")

    def test_caching_functionality(self):
        """Test: Selection results are cached correctly"""
        task = Task(description="实现用户认证功能")

        # First call
        tools1 = self.selector.select_tools(self.code_agent, task)

        # Second call (should use cache)
        tools2 = self.selector.select_tools(self.code_agent, task)

        self.assertEqual(tools1, tools2)
        # Cache should have an entry
        self.assertGreater(len(self.selector._selection_cache), 0)

    def test_cache_invalidation_after_ttl(self):
        """Test: Cache entries expire after TTL"""
        import time

        # Use a very short TTL for testing
        self.selector._cache_ttl = 0.1  # 100ms

        task = Task(description="测试任务")

        # First call
        tools1 = self.selector.select_tools(self.code_agent, task)

        # Wait for TTL to expire
        time.sleep(0.2)

        # Cache should be cleared by TTL
        # Second call should recalculate
        tools2 = self.selector.select_tools(self.code_agent, task)

        self.assertEqual(tools1, tools2)  # Results should still be same

    def test_empty_task_description_handling(self):
        """Test: Handles empty task descriptions gracefully"""
        empty_task = Task(description="")

        # Should still return default tools (sequential-thinking, serena)
        tools = self.selector.select_tools(self.code_agent, empty_task)
        self.assertIn("sequential-thinking", tools)
        self.assertIn("serena", tools)

    def test_case_insensitive_keyword_matching(self):
        """Test: Keyword matching is case-insensitive"""
        uppercase_task = Task(description="实现UI界面")
        lowercase_task = Task(description="实现ui界面")

        tools_upper = self.selector.select_tools(self.code_agent, uppercase_task)
        tools_lower = self.selector.select_tools(self.code_agent, lowercase_task)

        self.assertEqual(tools_upper, tools_lower)
        self.assertIn("magic", tools_upper)


class TestMCPSelectorEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def setUp(self):
        self.selector = MCPSelector()

    def test_agent_without_mcp_integrations(self):
        """Test: Handles agents without mcp_integrations field"""
        agent = Agent(
            name="test-agent",
            role="Test Role",
            expertise=[],
            activation_keywords=[],
            mcp_integrations=[]  # Empty integrations
        )

        task = Task(description="测试任务")

        # Should still return default tools
        tools = self.selector.select_tools(agent, task)
        self.assertIn("sequential-thinking", tools)

    def test_multiple_ui_keywords_in_task(self):
        """Test: Multiple UI keywords don't cause duplicate tool selection"""
        agent = Agent(
            name="code-agent",
            role="Code Specialist",
            expertise=[],
            activation_keywords=[],
            mcp_integrations=[
                {"name": "magic", "usage": "UI", "activation_condition": "conditional",
                 "keywords": ["ui", "界面", "组件"]}
            ]
        )

        task = Task(description="实现UI界面组件按钮表单")

        tools = self.selector.select_tools(agent, task)
        # Magic should appear only once
        self.assertEqual(tools.count("magic"), 1)

    def test_special_characters_in_task_description(self):
        """Test: Handles special characters in task descriptions"""
        agent = Agent(
            name="code-agent",
            role="Code Specialist",
            expertise=[],
            activation_keywords=[],
            mcp_integrations=[
                {"name": "serena", "usage": "代码", "activation_condition": "always"}
            ]
        )

        task = Task(description="实现@#$%^&*()功能")

        # Should not crash
        tools = self.selector.select_tools(agent, task)
        self.assertIn("serena", tools)


if __name__ == '__main__':
    unittest.main()
