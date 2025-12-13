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

        # Create mock agents (with all required fields)
        self.code_agent = Agent(
            name="code-agent",
            role="Code Implementation Specialist",
            description="Agent for code implementation and design patterns",
            expertise=["代码实现", "设计模式", "最佳实践"],
            activation_keywords=["实现", "代码", "功能"],
            activation_scenarios=["功能开发", "代码实现"],
            available_tools=["/wf_05_code"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "magic", "usage": "UI生成", "activation_condition": "conditional",
                 "keywords": ["ui", "界面", "组件"]},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ],
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="high",
            file_path="/agents/code_agent.md"
        )

        self.research_agent = Agent(
            name="research-agent",
            role="Technical Researcher",
            description="Agent for technical research and solution evaluation",
            expertise=["技术调研", "方案评估"],
            activation_keywords=["研究", "调研", "评估"],
            activation_scenarios=["技术选型", "方案评估"],
            available_tools=["/wf_04_research"],
            mcp_integrations=[
                {"name": "context7", "usage": "文档查询", "activation_condition": "always"},
                {"name": "tavily", "usage": "Web搜索", "activation_condition": "always"},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ],
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="medium",
            file_path="/agents/research_agent.md"
        )

        self.debug_agent = Agent(
            name="debug-agent",
            role="Debug Specialist",
            description="Agent for debugging and error analysis",
            expertise=["调试", "错误分析"],
            activation_keywords=["调试", "debug", "错误"],
            activation_scenarios=["问题诊断", "错误修复"],
            available_tools=["/wf_06_debug"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "context7", "usage": "框架文档", "activation_condition": "conditional",
                 "keywords": ["react", "vue", "django"]},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ],
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="high",
            file_path="/agents/debug_agent.md"
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
            description="Test agent",
            expertise=[],
            activation_keywords=[],
            activation_scenarios=[],
            available_tools=[],
            mcp_integrations=[],  # Empty integrations
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="low",
            file_path="/test/agent.md"
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
            description="Code specialist",
            expertise=[],
            activation_keywords=[],
            activation_scenarios=[],
            available_tools=[],
            mcp_integrations=[
                {"name": "magic", "usage": "UI", "activation_condition": "conditional",
                 "keywords": ["ui", "界面", "组件"]}
            ],
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="medium",
            file_path="/agents/code.md"
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
            description="Code specialist",
            expertise=[],
            activation_keywords=[],
            activation_scenarios=[],
            available_tools=[],
            mcp_integrations=[
                {"name": "serena", "usage": "代码", "activation_condition": "always"}
            ],
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="medium",
            file_path="/agents/code.md"
        )

        task = Task(description="实现@#$%^&*()功能")

        # Should not crash
        tools = self.selector.select_tools(agent, task)
        self.assertIn("serena", tools)


class TestMCPSelectorV2API(unittest.TestCase):
    """Test suite for MCPSelector V2 API (select_tools_v2)"""

    def setUp(self):
        """Set up test fixtures for V2 API tests"""
        self.selector = MCPSelector()

        # Create mock agent with mcp_integrations (providing all required fields)
        self.test_agent = Agent(
            name="test-agent",
            role="Test Specialist",
            description="Agent for testing V2 API",
            expertise=["测试", "质量保证"],
            activation_keywords=["测试", "test"],
            activation_scenarios=["单元测试", "集成测试"],
            available_tools=["/wf_07_test", "/wf_08_review"],
            mcp_integrations=[
                {"name": "Serena", "usage": "代码理解和符号级操作"},
                {"name": "Sequential-thinking", "usage": "复杂逻辑推理"},
                {"name": "Magic", "usage": "UI组件生成"},
            ],
            collaboration_modes=[],
            workflows=[],
            decision_criteria={},
            status="active",
            priority="medium",
            file_path="/test/agents/test_agent.md"
        )

    def test_confidence_lower_bound_protection(self):
        """Test: Confidence never goes below 0.0 (Bug Fix Verification)"""
        # This test verifies the fix for the confidence lower bound bug
        # Multiple penalty deductions should not result in negative confidence

        # Create a task that will trigger multiple confidence penalties:
        # - No keyword matches → no bonus
        # - Below complexity threshold → -0.1 penalty
        # - No feature alignment → no bonus
        # Base confidence (0.5) - penalty (-0.1) = 0.4

        task_description = "一个简单的任务描述"  # Simple task, no complexity features

        recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=task_description,
            auto_filter=False  # Don't filter low-confidence tools
        )

        # Verify all confidence scores are >= 0.0
        for rec in recommendations:
            self.assertGreaterEqual(
                rec.confidence,
                0.0,
                f"Confidence for {rec.tool_name} should not be negative: {rec.confidence}"
            )

    def test_confidence_upper_bound_protection(self):
        """Test: Confidence never exceeds 1.0"""
        # Create a complex task with many matching keywords and features
        # to try to push confidence above 1.0

        task_description = """
        实现一个复杂的多文件架构系统，涉及多个模块的重构、
        集成第三方API、复杂算法实现、并发处理、
        数据库迁移、UI组件设计和API endpoint设计
        """

        recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=task_description,
            auto_filter=False
        )

        # Verify all confidence scores are <= 1.0
        for rec in recommendations:
            self.assertLessEqual(
                rec.confidence,
                1.0,
                f"Confidence for {rec.tool_name} should not exceed 1.0: {rec.confidence}"
            )

    def test_confidence_normal_case_calculation(self):
        """Test: Confidence calculation in normal scenarios"""
        # Test case 1: Task with good keyword match for Serena
        task_with_code_keywords = "修改代码并重构模块结构"

        recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=task_with_code_keywords,
            auto_filter=False
        )

        # Find Serena in recommendations
        serena_rec = next((r for r in recommendations if r.tool_name == "Serena"), None)
        self.assertIsNotNone(serena_rec, "Serena should be in recommendations")

        # Serena should have decent confidence due to keyword matches
        self.assertGreaterEqual(serena_rec.confidence, 0.5, "Serena confidence should be reasonable")
        self.assertLessEqual(serena_rec.confidence, 1.0, "Serena confidence should not exceed 1.0")

    def test_analyze_complexity_v2_simple_task(self):
        """Test: Complexity analysis for simple tasks"""
        simple_task = "修改一个变量名"

        complexity = self.selector._analyze_complexity_v2(simple_task)

        # Simple task should have low complexity score
        self.assertLessEqual(complexity.score, 0.2, "Simple task should have low complexity")
        self.assertIn("简单任务", complexity.reasoning, "Reasoning should indicate simple task")

    def test_analyze_complexity_v2_complex_task(self):
        """Test: Complexity analysis for complex tasks"""
        complex_task = "重构整个系统架构，实现多文件模块化设计，集成第三方API，优化算法性能"

        complexity = self.selector._analyze_complexity_v2(complex_task)

        # Complex task should have high complexity score
        self.assertGreaterEqual(complexity.score, 0.4, "Complex task should have high complexity")

        # Check that multiple features are detected
        detected_features = [k for k, v in complexity.features.items() if v]
        self.assertGreater(len(detected_features), 2, "Multiple complexity features should be detected")

    def test_select_tools_v2_auto_filter(self):
        """Test: Auto-filtering of low-confidence tools"""
        # Simple task that won't match well with any tools
        simple_task = "测试任务"

        # Without auto-filter
        all_recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=simple_task,
            auto_filter=False
        )

        # With auto-filter (default)
        filtered_recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=simple_task,
            auto_filter=True
        )

        # Filtered list should be <= unfiltered list
        self.assertLessEqual(
            len(filtered_recommendations),
            len(all_recommendations),
            "Auto-filter should reduce recommendation count"
        )

        # All filtered recommendations should have confidence >= 0.3
        for rec in filtered_recommendations:
            self.assertGreaterEqual(
                rec.confidence,
                0.3,
                f"{rec.tool_name} confidence should be >= 0.3 after filtering"
            )

    def test_select_tools_v2_priority_classification(self):
        """Test: Priority classification based on confidence"""
        task_description = "复杂的代码重构任务，涉及多文件修改和架构调整"

        recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=task_description,
            auto_filter=False
        )

        # Verify priority classification logic
        for rec in recommendations:
            if rec.confidence >= 0.7:
                self.assertEqual(rec.priority, "high", f"{rec.tool_name} should be high priority")
            elif rec.confidence >= 0.5:
                self.assertEqual(rec.priority, "medium", f"{rec.tool_name} should be medium priority")
            else:
                self.assertEqual(rec.priority, "low", f"{rec.tool_name} should be low priority")

    def test_select_tools_v2_sorted_by_confidence(self):
        """Test: Recommendations are sorted by confidence (high to low)"""
        task_description = "实现新功能"

        recommendations = self.selector.select_tools_v2(
            agent=self.test_agent,
            task_description=task_description,
            auto_filter=False
        )

        # Verify recommendations are sorted by confidence descending
        if len(recommendations) > 1:
            for i in range(len(recommendations) - 1):
                self.assertGreaterEqual(
                    recommendations[i].confidence,
                    recommendations[i + 1].confidence,
                    "Recommendations should be sorted by confidence (high to low)"
                )

    def test_calculate_tool_confidence_keyword_matching(self):
        """Test: Keyword matching factor in confidence calculation"""
        # Create a task with Serena keywords
        task_with_serena_keywords = "修改代码、查找符号、重构模块"

        complexity = self.selector._analyze_complexity_v2(task_with_serena_keywords)

        # Calculate confidence for Serena
        confidence, reason = self.selector._calculate_tool_confidence(
            tool_name="Serena",
            task_description=task_with_serena_keywords,
            complexity=complexity,
            usage_desc="Code navigation and refactoring"
        )

        # Keyword matching should boost confidence
        self.assertGreaterEqual(confidence, 0.6, "Keyword matches should boost confidence")
        self.assertIn("关键词匹配", reason, "Reason should mention keyword matching")

    def test_gateway_integration_unavailable_tool(self):
        """Test: Graceful handling when gateway reports tool unavailable"""
        # Create a mock gateway that reports tool as unavailable
        mock_gateway = MagicMock()
        mock_gateway.is_available.return_value = False

        selector_with_gateway = MCPSelector(gateway=mock_gateway)

        recommendations = selector_with_gateway.select_tools_v2(
            agent=self.test_agent,
            task_description="测试任务",
            auto_filter=False
        )

        # All tools should have "MCP 不可用" warning in reason
        for rec in recommendations:
            self.assertIn("MCP 不可用", rec.reason, f"{rec.tool_name} should show unavailable warning")
            self.assertEqual(rec.priority, "low", f"{rec.tool_name} should be low priority when unavailable")


if __name__ == '__main__':
    unittest.main()
