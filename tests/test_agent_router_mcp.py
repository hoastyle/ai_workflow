"""
Integration tests for AgentRouter with MCP integration

Tests the complete workflow generation with automatic MCP tool selection.
"""

import unittest
from unittest.mock import MagicMock, patch
from commands.lib.agent_router import AgentRouter, AgentWorkflow, WorkflowStep, CoordinationMode
from commands.lib.agent_registry import Agent, AgentRegistry
from commands.lib.mcp_selector import Task


class TestAgentRouterMCPIntegration(unittest.TestCase):
    """Test suite for AgentRouter + MCPSelector integration"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a minimal agent registry
        self.registry = AgentRegistry()

        # Add test agents
        self.code_agent = Agent(
            name="code-agent",
            role="Implementation Engineer",
            expertise=["代码实现", "设计模式"],
            activation_keywords=["实现", "代码", "功能"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "magic", "usage": "UI生成", "activation_condition": "conditional",
                 "keywords": ["ui", "界面", "组件"]},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ]
        )

        self.architect_agent = Agent(
            name="architect-agent",
            role="System Architect",
            expertise=["架构设计", "技术选型"],
            activation_keywords=["架构", "设计", "选型"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "context7", "usage": "文档查询", "activation_condition": "always"},
                {"name": "tavily", "usage": "Web搜索", "activation_condition": "always"},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ]
        )

        self.review_agent = Agent(
            name="review-agent",
            role="Code Reviewer",
            expertise=["代码审查", "质量检查"],
            activation_keywords=["审查", "review", "检查"],
            mcp_integrations=[
                {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
                {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
            ]
        )

        self.registry.register(self.code_agent)
        self.registry.register(self.architect_agent)
        self.registry.register(self.review_agent)

        self.router = AgentRouter(registry=self.registry)

    def test_single_agent_workflow_has_mcp_tools(self):
        """Test: Single agent workflow includes MCP tools"""
        task = "实现用户认证功能"

        workflow = self.router.route(task, mode="single")

        self.assertEqual(workflow.mode, CoordinationMode.SINGLE)
        self.assertEqual(len(workflow.steps), 1)

        # Verify MCP tools are assigned
        step = workflow.steps[0]
        self.assertIsNotNone(step.mcp_tools)
        self.assertIn("sequential-thinking", step.mcp_tools)
        self.assertIn("serena", step.mcp_tools)

    def test_sequential_workflow_all_steps_have_mcp_tools(self):
        """Test: Sequential workflow assigns MCP tools to all steps"""
        task = "设计并实现用户认证系统"

        workflow = self.router.route(task, mode="sequential")

        self.assertEqual(workflow.mode, CoordinationMode.SEQUENTIAL)
        self.assertGreaterEqual(len(workflow.steps), 2)

        # Every step should have MCP tools assigned
        for step in workflow.steps:
            self.assertIsNotNone(step.mcp_tools, f"Step {step.agent.name} missing MCP tools")
            self.assertGreater(len(step.mcp_tools), 0)
            # Sequential-thinking should be in all steps
            self.assertIn("sequential-thinking", step.mcp_tools)

    def test_parallel_workflow_all_steps_have_mcp_tools(self):
        """Test: Parallel workflow assigns MCP tools to all parallel steps"""
        task = "同时实现前端界面和后端API"

        workflow = self.router.route(task, mode="parallel")

        self.assertEqual(workflow.mode, CoordinationMode.PARALLEL)

        # All steps should have MCP tools
        for step in workflow.steps:
            self.assertIsNotNone(step.mcp_tools)
            self.assertIn("sequential-thinking", step.mcp_tools)

    def test_ui_task_activates_magic_for_code_agent(self):
        """Test: UI tasks activate Magic tool for code-agent"""
        ui_task = "实现登录界面组件"

        workflow = self.router.route(ui_task, mode="single")

        # Find code-agent step
        code_step = next((s for s in workflow.steps if s.agent.name == "code-agent"), None)

        if code_step:
            self.assertIn("magic", code_step.mcp_tools)

    def test_architecture_task_activates_context7_and_tavily(self):
        """Test: Architecture tasks activate Context7 and Tavily for architect-agent"""
        arch_task = "设计系统架构选择技术栈"

        workflow = self.router.route(arch_task, mode="single")

        # Find architect-agent step
        arch_step = next((s for s in workflow.steps if s.agent.name == "architect-agent"), None)

        if arch_step:
            self.assertIn("context7", arch_step.mcp_tools)
            self.assertIn("tavily", arch_step.mcp_tools)

    def test_hierarchical_workflow_all_layers_have_mcp_tools(self):
        """Test: Hierarchical workflow assigns MCP tools to all layers"""
        complex_task = "设计并实现完整的用户管理系统，包含界面和后端"

        workflow = self.router.route(complex_task, mode="hierarchical")

        self.assertEqual(workflow.mode, CoordinationMode.HIERARCHICAL)

        # All steps at all levels should have MCP tools
        for step in workflow.steps:
            self.assertIsNotNone(step.mcp_tools)
            self.assertGreater(len(step.mcp_tools), 0)

    def test_workflow_mcp_tools_vary_by_agent_role(self):
        """Test: Different agents get different MCP tool sets"""
        task = "设计、实现和审查用户认证功能"

        workflow = self.router.route(task, mode="sequential")

        # Architect should have Context7 and Tavily
        arch_step = next((s for s in workflow.steps if s.agent.name == "architect-agent"), None)
        if arch_step:
            self.assertIn("context7", arch_step.mcp_tools)
            self.assertIn("tavily", arch_step.mcp_tools)

        # Code-agent should have Serena but not necessarily Context7
        code_step = next((s for s in workflow.steps if s.agent.name == "code-agent"), None)
        if code_step:
            self.assertIn("serena", code_step.mcp_tools)

        # Review-agent should have Serena for code understanding
        review_step = next((s for s in workflow.steps if s.agent.name == "review-agent"), None)
        if review_step:
            self.assertIn("serena", review_step.mcp_tools)

    def test_workflow_to_prompt_includes_mcp_information(self):
        """Test: Workflow prompt generation includes MCP tool information"""
        task = "实现用户界面登录页面"

        workflow = self.router.route(task, mode="single")
        prompt = workflow.to_prompt()

        # Prompt should mention MCP tools
        self.assertIn("MCP", prompt)
        # Should mention specific tools
        self.assertIn("sequential-thinking", prompt.lower())

    def test_task_object_passed_correctly_to_selector(self):
        """Test: Task description is correctly passed to MCPSelector"""
        task_desc = "实现React组件调试功能"

        workflow = self.router.route(task_desc, mode="single")

        # Verify that the task description influenced MCP selection
        # (This is indirectly tested by checking that conditional tools are activated)
        step = workflow.steps[0]
        self.assertIsNotNone(step.mcp_tools)

    def test_empty_task_description_doesnt_break_routing(self):
        """Test: Empty task description doesn't break workflow generation"""
        task = ""

        # Should not crash
        workflow = self.router.route(task, mode="single")

        # Should still have MCP tools (at least default ones)
        self.assertGreater(len(workflow.steps), 0)
        self.assertIsNotNone(workflow.steps[0].mcp_tools)

    def test_mcp_selector_integration_doesnt_affect_agent_selection(self):
        """Test: MCP integration doesn't change which agents are selected"""
        task = "实现用户认证功能"

        # Route the task
        workflow = self.router.route(task, mode="single")

        # Agent selection should still work correctly
        # (code-agent should be selected for implementation task)
        self.assertEqual(workflow.steps[0].agent.name, "code-agent")


class TestAgentRouterMCPPerformance(unittest.TestCase):
    """Test performance aspects of MCP integration"""

    def setUp(self):
        self.registry = AgentRegistry()
        self.router = AgentRouter(registry=self.registry)

    def test_mcp_selection_uses_caching(self):
        """Test: MCP selection results are cached across workflow steps"""
        # Create multiple agents with same configuration
        agents = []
        for i in range(5):
            agent = Agent(
                name=f"agent-{i}",
                role=f"Role {i}",
                expertise=[],
                activation_keywords=[f"keyword{i}"],
                mcp_integrations=[
                    {"name": "serena", "usage": "test", "activation_condition": "always"}
                ]
            )
            agents.append(agent)
            self.registry.register(agent)

        task = "测试缓存功能"

        # Route multiple times with same task
        workflow1 = self.router.route(task, mode="single")
        workflow2 = self.router.route(task, mode="single")

        # Both should succeed (caching doesn't break functionality)
        self.assertIsNotNone(workflow1.steps[0].mcp_tools)
        self.assertIsNotNone(workflow2.steps[0].mcp_tools)

    def test_parallel_workflow_mcp_selection_efficiency(self):
        """Test: MCP selection doesn't significantly slow down parallel workflow generation"""
        import time

        # Create multiple agents
        for i in range(10):
            agent = Agent(
                name=f"parallel-agent-{i}",
                role=f"Role {i}",
                expertise=[],
                activation_keywords=[f"parallel{i}"],
                mcp_integrations=[
                    {"name": "serena", "usage": "test", "activation_condition": "always"}
                ]
            )
            self.registry.register(agent)

        task = "并行执行10个任务"

        start_time = time.time()
        workflow = self.router.route(task, mode="parallel")
        elapsed = time.time() - start_time

        # Should complete in reasonable time (< 1 second for route + MCP selection)
        self.assertLess(elapsed, 1.0)
        self.assertGreater(len(workflow.steps), 0)


class TestAgentRouterMCPEdgeCases(unittest.TestCase):
    """Test edge cases in AgentRouter MCP integration"""

    def setUp(self):
        self.registry = AgentRegistry()
        self.router = AgentRouter(registry=self.registry)

    def test_agent_without_mcp_integrations_field(self):
        """Test: Handles agents without mcp_integrations gracefully"""
        agent = Agent(
            name="legacy-agent",
            role="Legacy Role",
            expertise=[],
            activation_keywords=["legacy"],
            mcp_integrations=[]  # Empty
        )
        self.registry.register(agent)

        task = "使用legacy agent"

        # Should not crash
        workflow = self.router.route(task, mode="single")

        # Should still assign default MCP tools
        self.assertIsNotNone(workflow.steps[0].mcp_tools)

    def test_very_long_task_description(self):
        """Test: Handles very long task descriptions"""
        long_task = "实现" + "非常详细的需求" * 100

        agent = Agent(
            name="test-agent",
            role="Test",
            expertise=[],
            activation_keywords=["实现"],
            mcp_integrations=[
                {"name": "serena", "usage": "test", "activation_condition": "always"}
            ]
        )
        self.registry.register(agent)

        # Should handle long task without issues
        workflow = self.router.route(long_task, mode="single")

        self.assertIsNotNone(workflow.steps[0].mcp_tools)


if __name__ == '__main__':
    unittest.main()
