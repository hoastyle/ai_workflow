"""
Tests for Multi-Agent Orchestrator

测试多 Agent 协调器的各项功能
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from commands.lib.multi_agent_orchestrator import (
    MultiAgentOrchestrator,
    ExecutionMode,
    ConflictResolutionStrategy,
    AgentTask,
    OrchestrationPlan,
    OrchestrationResult
)
from commands.lib.agent_registry import Agent, AgentMatch


def create_test_agent(**kwargs):
    """创建测试 Agent 的辅助函数"""
    defaults = {
        'activation_scenarios': [],
        'mcp_integrations': [],
        'workflows': [],
        'decision_criteria': {},
        'status': 'active',
        'file_path': ''
    }
    defaults.update(kwargs)
    return Agent(**defaults)


@pytest.fixture
def mock_registry():
    """创建模拟的 Agent Registry"""
    registry = Mock()

    # 创建测试 Agents
    code_agent = create_test_agent(
        name="code-agent",
        role="Implementation Engineer",
        description="代码实现",
        expertise=["功能实现", "代码编写"],
        activation_keywords=["实现", "代码", "功能"],
        available_tools=["/wf_05_code"],
        collaboration_modes=[
            {"agent": "test-agent", "mode": "parallel", "scenario": "同时编写代码和测试"}
        ],
        priority="high"
    )

    test_agent = create_test_agent(
        name="test-agent",
        role="Test Engineer",
        description="测试开发",
        expertise=["测试编写", "测试覆盖"],
        activation_keywords=["测试", "test"],
        available_tools=["/wf_07_test"],
        collaboration_modes=[
            {"agent": "code-agent", "mode": "parallel", "scenario": "同时编写代码和测试"}
        ],
        priority="high"
    )

    pm_agent = create_test_agent(
        name="pm-agent",
        role="Project Manager",
        description="项目管理",
        expertise=["项目规划", "任务管理"],
        activation_keywords=["规划", "管理"],
        available_tools=["/wf_01_planning"],
        collaboration_modes=[
            {"agent": "code-agent", "mode": "hierarchical", "scenario": "PM 协调开发"}
        ],
        priority="high"
    )

    registry.agents = [code_agent, test_agent, pm_agent]
    return registry


@pytest.fixture
def orchestrator(mock_registry):
    """创建测试用的协调器"""
    return MultiAgentOrchestrator(registry=mock_registry)


class TestComplexityAnalysis:
    """测试任务复杂度分析"""

    def test_simple_task_analysis(self, orchestrator, mock_registry):
        """测试简单任务（单 Agent）"""
        # Mock find_agents 返回单个高分 Agent
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[0],
                score=0.95,
                matched_keywords=["实现", "功能"], matched_scenarios=[], reason="test"
            )
        ]

        result = orchestrator.analyze_task_complexity("实现用户登录功能")

        assert result['needs_multiple_agents'] is False
        assert result['estimated_agents_count'] == 1
        assert result['complexity_score'] < 0.4

    def test_complex_task_analysis(self, orchestrator, mock_registry):
        """测试复杂任务（多 Agent）"""
        # Mock find_agents 返回多个高分 Agents
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[0],
                score=0.90,
                matched_keywords=["实现", "代码"], matched_scenarios=[], reason="test"
            ),
            AgentMatch(
                agent=mock_registry.agents[1],
                score=0.85,
                matched_keywords=["测试"], matched_scenarios=[], reason="test"
            ),
            AgentMatch(
                agent=mock_registry.agents[2],
                score=0.70,
                matched_keywords=["规划"], matched_scenarios=[], reason="test"
            )
        ]

        result = orchestrator.analyze_task_complexity("实现和测试用户认证系统")

        assert result['needs_multiple_agents'] is True
        assert result['estimated_agents_count'] == 3
        assert result['complexity_score'] >= 0.4
        assert len(result['suggested_agents']) == 3


class TestConflictResolution:
    """测试冲突解决"""

    def test_highest_score_strategy(self, orchestrator, mock_registry):
        """测试选择最高分策略"""
        candidates = [
            AgentMatch(agent=mock_registry.agents[0], score=0.95, matched_keywords=[], matched_scenarios=[], reason="test"),
            AgentMatch(agent=mock_registry.agents[1], score=0.80, matched_keywords=[], matched_scenarios=[], reason="test"),
        ]

        result = orchestrator.resolve_conflicts(
            candidates,
            ConflictResolutionStrategy.HIGHEST_SCORE
        )

        assert len(result) == 1
        assert result[0].name == "code-agent"

    def test_priority_based_strategy(self, orchestrator, mock_registry):
        """测试基于优先级策略"""
        # 修改一个 agent 的优先级
        low_priority_agent = create_test_agent(
        name="doc-agent",
            role="Documentation Specialist",
            description="文档生成",
            expertise=["文档编写"],
            activation_keywords=["文档"],
            available_tools=["/wf_14_doc"],
            collaboration_modes=[],
            priority="low"  # 低优先级
        )

        candidates = [
            AgentMatch(agent=mock_registry.agents[0], score=0.85, matched_keywords=[], matched_scenarios=[], reason="test"),  # high
            AgentMatch(agent=low_priority_agent, score=0.90, matched_keywords=[], matched_scenarios=[], reason="test"),  # low
        ]

        result = orchestrator.resolve_conflicts(
            candidates,
            ConflictResolutionStrategy.PRIORITY_BASED
        )

        # 应该选择高优先级的，即使分数稍低
        assert len(result) >= 1
        assert result[0].name == "code-agent"

    def test_merge_all_strategy(self, orchestrator, mock_registry):
        """测试合并所有策略"""
        candidates = [
            AgentMatch(agent=mock_registry.agents[0], score=0.95, matched_keywords=[], matched_scenarios=[], reason="test"),
            AgentMatch(agent=mock_registry.agents[1], score=0.80, matched_keywords=[], matched_scenarios=[], reason="test"),
        ]

        result = orchestrator.resolve_conflicts(
            candidates,
            ConflictResolutionStrategy.MERGE_ALL
        )

        assert len(result) == 2


class TestDependencyAnalysis:
    """测试依赖分析"""

    def test_no_dependencies(self, orchestrator):
        """测试无依赖关系"""
        # 创建两个没有依赖的 agents
        agent1 = create_test_agent(
        name="agent1",
            role="Role 1",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],  # 无协作
            priority="high"
        )
        agent2 = create_test_agent(
        name="agent2",
            role="Role 2",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )

        deps = orchestrator.analyze_dependencies([agent1, agent2])

        assert deps == {'agent1': [], 'agent2': []}

    def test_sequential_dependencies(self, orchestrator):
        """测试顺序依赖"""
        agent1 = create_test_agent(
        name="agent1",
            role="Role 1",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[
                {"agent": "agent2", "mode": "sequential", "scenario": "test"}
            ],
            priority="high"
        )
        agent2 = create_test_agent(
        name="agent2",
            role="Role 2",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )

        deps = orchestrator.analyze_dependencies([agent1, agent2])

        assert 'agent2' in deps['agent1']


class TestExecutionMode:
    """测试执行模式选择"""

    def test_parallel_mode_no_dependencies(self, orchestrator):
        """测试并行模式（无依赖）"""
        agents = [
            create_test_agent(
        name=f"agent{i}",
                role=f"Role {i}",
                description="Test",
                expertise=[],
                activation_keywords=[],
                available_tools=[],
                collaboration_modes=[],
                priority="high"
            )
            for i in range(3)
        ]

        deps = {agent.name: [] for agent in agents}
        mode = orchestrator.determine_execution_mode(agents, deps)

        assert mode == ExecutionMode.PARALLEL

    def test_sequential_mode_with_dependencies(self, orchestrator):
        """测试顺序模式（有依赖）"""
        agent1 = create_test_agent(
        name="agent1",
            role="Role 1",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[
                {"agent": "agent2", "mode": "sequential", "scenario": "test"}
            ],
            priority="high"
        )
        agent2 = create_test_agent(
        name="agent2",
            role="Role 2",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )

        agents = [agent1, agent2]
        deps = orchestrator.analyze_dependencies(agents)
        mode = orchestrator.determine_execution_mode(agents, deps)

        assert mode == ExecutionMode.SEQUENTIAL

    def test_hierarchical_mode_with_coordinator(self, orchestrator, mock_registry):
        """测试层级模式（有协调者）"""
        agents = [
            mock_registry.agents[2],  # PM agent (coordinator)
            mock_registry.agents[0],  # Code agent
        ]

        deps = orchestrator.analyze_dependencies(agents)
        mode = orchestrator.determine_execution_mode(agents, deps)

        assert mode == ExecutionMode.HIERARCHICAL


class TestOrchestrationPlan:
    """测试编排计划"""

    def test_simple_plan_creation(self, orchestrator, mock_registry):
        """测试简单计划创建（单 Agent）"""
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[0],
                score=0.95,
                matched_keywords=["实现"], matched_scenarios=[], reason="test"
            )
        ]

        plan = orchestrator.create_orchestration_plan(
            "实现用户登录",
            "wf_05_code"
        )

        assert len(plan.tasks) == 1
        assert plan.tasks[0].agent.name == "code-agent"
        assert plan.execution_mode == ExecutionMode.SEQUENTIAL

    def test_complex_plan_creation(self, orchestrator, mock_registry):
        """测试复杂计划创建（多 Agent）"""
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[0],
                score=0.90,
                matched_keywords=["实现", "代码"], matched_scenarios=[], reason="test"
            ),
            AgentMatch(
                agent=mock_registry.agents[1],
                score=0.85,
                matched_keywords=["测试"], matched_scenarios=[], reason="test"
            ),
        ]

        plan = orchestrator.create_orchestration_plan(
            "实现和测试用户认证系统",
            "wf_05_code",
            ConflictResolutionStrategy.MERGE_ALL
        )

        assert len(plan.tasks) >= 2
        assert plan.execution_mode in [ExecutionMode.PARALLEL, ExecutionMode.SEQUENTIAL]

    def test_hierarchical_plan(self, orchestrator, mock_registry):
        """测试层级计划"""
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[2],  # PM agent
                score=0.95,
                matched_keywords=["规划"], matched_scenarios=[], reason="test"
            ),
            AgentMatch(
                agent=mock_registry.agents[0],  # Code agent
                score=0.85,
                matched_keywords=["实现"], matched_scenarios=[], reason="test"
            ),
        ]

        plan = orchestrator.create_orchestration_plan(
            "规划和实现新功能",
            "wf_01_planning",
            ConflictResolutionStrategy.MERGE_ALL
        )

        # PM agent 应该在前
        assert plan.tasks[0].agent.name == "pm-agent"
        assert plan.execution_mode == ExecutionMode.HIERARCHICAL


class TestPlanFormatting:
    """测试计划格式化"""

    def test_format_sequential_plan(self, orchestrator):
        """测试顺序计划格式化"""
        agent1 = create_test_agent(
        name="agent1",
            role="Role 1",
            description="Test",
            expertise=["Skill 1"],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )

        plan = OrchestrationPlan(
            tasks=[
                AgentTask(agent=agent1, command="wf_05_code", task_description="test", execution_order=0)
            ],
            execution_mode=ExecutionMode.SEQUENTIAL,
            conflict_resolution=ConflictResolutionStrategy.HIGHEST_SCORE
        )

        formatted = orchestrator.format_plan(plan, verbose=True)

        assert "Multi-Agent Orchestration Plan" in formatted
        assert "sequential" in formatted
        assert "Role 1" in formatted

    def test_format_parallel_plan(self, orchestrator):
        """测试并行计划格式化"""
        agent1 = create_test_agent(
        name="agent1",
            role="Role 1",
            description="Test",
            expertise=["Skill 1"],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )
        agent2 = create_test_agent(
        name="agent2",
            role="Role 2",
            description="Test",
            expertise=["Skill 2"],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )

        plan = OrchestrationPlan(
            tasks=[
                AgentTask(agent=agent1, command="wf_05_code", task_description="test", execution_order=0),
                AgentTask(agent=agent2, command="wf_07_test", task_description="test", execution_order=0)
            ],
            execution_mode=ExecutionMode.PARALLEL,
            conflict_resolution=ConflictResolutionStrategy.MERGE_ALL
        )

        formatted = orchestrator.format_plan(plan)

        assert "parallel" in formatted
        assert "Role 1" in formatted
        assert "Role 2" in formatted


class TestTopologicalSort:
    """测试拓扑排序"""

    def test_simple_ordering(self, orchestrator):
        """测试简单排序（A -> B）"""
        agent_a = create_test_agent(
        name="agent-a",
            role="Role A",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )
        agent_b = create_test_agent(
        name="agent-b",
            role="Role B",
            description="Test",
            expertise=[],
            activation_keywords=[],
            available_tools=[],
            collaboration_modes=[],
            priority="high"
        )

        agents = [agent_b, agent_a]  # 故意倒序
        deps = {
            'agent-a': [],
            'agent-b': ['agent-a']  # B 依赖 A
        }

        sorted_agents = orchestrator._topological_sort(agents, deps)

        # A 应该在 B 前面
        assert sorted_agents[0].name == "agent-a"
        assert sorted_agents[1].name == "agent-b"

    def test_complex_ordering(self, orchestrator):
        """测试复杂排序（A -> B -> C）"""
        agent_a = create_test_agent(
        name="agent-a", role="A", description="", expertise=[], activation_keywords=[], available_tools=[], collaboration_modes=[], priority="high")
        agent_b = create_test_agent(
        name="agent-b", role="B", description="", expertise=[], activation_keywords=[], available_tools=[], collaboration_modes=[], priority="high")
        agent_c = create_test_agent(
        name="agent-c", role="C", description="", expertise=[], activation_keywords=[], available_tools=[], collaboration_modes=[], priority="high")

        agents = [agent_c, agent_a, agent_b]  # 故意打乱
        deps = {
            'agent-a': [],
            'agent-b': ['agent-a'],
            'agent-c': ['agent-b']
        }

        sorted_agents = orchestrator._topological_sort(agents, deps)

        # 应该是 A, B, C 的顺序
        assert sorted_agents[0].name == "agent-a"
        assert sorted_agents[1].name == "agent-b"
        assert sorted_agents[2].name == "agent-c"

    def test_circular_dependency_handling(self, orchestrator):
        """测试环形依赖处理"""
        agent_a = create_test_agent(
        name="agent-a", role="A", description="", expertise=[], activation_keywords=[], available_tools=[], collaboration_modes=[], priority="high")
        agent_b = create_test_agent(
        name="agent-b", role="B", description="", expertise=[], activation_keywords=[], available_tools=[], collaboration_modes=[], priority="high")

        agents = [agent_a, agent_b]
        deps = {
            'agent-a': ['agent-b'],  # A 依赖 B
            'agent-b': ['agent-a']   # B 依赖 A (环)
        }

        # 应该返回原始顺序，不崩溃
        sorted_agents = orchestrator._topological_sort(agents, deps)
        assert len(sorted_agents) == 2


# 集成测试
class TestIntegration:
    """端到端集成测试"""

    def test_end_to_end_simple_task(self, orchestrator, mock_registry):
        """端到端测试：简单任务"""
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[0],
                score=0.95,
                matched_keywords=["实现"], matched_scenarios=[], reason="test"
            )
        ]

        # 创建计划
        plan = orchestrator.create_orchestration_plan(
            "实现用户登录",
            "wf_05_code"
        )

        # 验证计划
        assert len(plan.tasks) == 1

        # 格式化输出
        formatted = orchestrator.format_plan(plan, verbose=True)
        assert "Implementation Engineer" in formatted

    def test_end_to_end_complex_task(self, orchestrator, mock_registry):
        """端到端测试：复杂任务（多 Agent 协作）"""
        mock_registry.find_agents.return_value = [
            AgentMatch(
                agent=mock_registry.agents[0],
                score=0.90,
                matched_keywords=["实现", "代码"], matched_scenarios=[], reason="test"
            ),
            AgentMatch(
                agent=mock_registry.agents[1],
                score=0.85,
                matched_keywords=["测试"], matched_scenarios=[], reason="test"
            ),
        ]

        # 创建计划
        plan = orchestrator.create_orchestration_plan(
            "实现和测试用户认证系统",
            "wf_05_code",
            ConflictResolutionStrategy.MERGE_ALL
        )

        # 验证计划
        assert len(plan.tasks) >= 2

        # 格式化输出
        formatted = orchestrator.format_plan(plan, verbose=True)
        assert "Implementation Engineer" in formatted or "Test Engineer" in formatted
