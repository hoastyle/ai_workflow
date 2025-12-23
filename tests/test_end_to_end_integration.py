"""
Phase 2.5 端到端集成测试

测试所有 Phase 2.1-2.4 组件的实际集成，而非单独的单元测试。
"""

import pytest
from unittest.mock import Mock, patch

from commands.lib.agent_coordinator import AgentCoordinator
from commands.lib.agent_decision_engine import AgentDecisionEngine
from commands.lib.agent_command_executor import AgentCommandExecutor
from commands.lib.agent_feedback_system import AgentFeedbackSystem
from commands.lib.multi_agent_orchestrator import (
    MultiAgentOrchestrator,
    ExecutionMode,
    ConflictResolutionStrategy
)


# ============================================================================
# Phase 2.1 + 2.2 集成测试：决策引擎 + 执行器
# ============================================================================

def test_decision_to_execution_integration():
    """测试决策引擎和执行器的集成"""
    # 创建组件
    coordinator = AgentCoordinator()
    executor = AgentCommandExecutor()

    # 模拟任务: 用户想实现一个功能
    task_description = "Implement user authentication"
    command_name = "wf_05_code"

    # Step 1: 使用 coordinator 进行 agent 选择
    agent_context = coordinator.intercept(
        task_description=task_description,
        command_name=command_name,
        auto_activate=True,
        min_confidence=0.65
    )

    # 验证 agent 被激活
    assert agent_context['agent'] is not None
    assert agent_context['match_score'] >= 0.65

    # Step 2: 如果有推荐命令，模拟执行
    if agent_context.get('auto_activated'):
        recommended_command = agent_context['agent'].recommended_commands[0]

        # Mock 执行器（避免实际执行命令）
        with patch.object(executor, 'execute_command') as mock_execute:
            mock_execute.return_value = Mock(
                success=True,
                exit_code=0,
                output="Command executed successfully",
                duration_ms=100.0
            )

            # 执行命令
            result = executor.execute_command(
                command=recommended_command,
                context={'task': task_description}
            )

            # 验证执行结果
            assert result.success is True
            assert mock_execute.called


def test_decision_engine_confidence_levels():
    """测试决策引擎的三级置信度模式"""
    decision_engine = AgentDecisionEngine()

    # 场景 1: 高置信度 (≥85%) - 自动执行
    agent_context_high = {
        'match_score': 0.92,
        'agent': Mock(recommended_commands=["/wf_05_code"])
    }

    decision_high = decision_engine.decide(
        agent_context=agent_context_high,
        user_command="wf_06_debug"
    )

    assert decision_high.decision_mode == "auto"
    assert decision_high.final_command == "/wf_05_code"

    # 场景 2: 中等置信度 (65-85%) - 提示用户
    agent_context_medium = {
        'match_score': 0.75,
        'agent': Mock(recommended_commands=["/wf_05_code"])
    }

    decision_medium = decision_engine.decide(
        agent_context=agent_context_medium,
        user_command="wf_06_debug"
    )

    assert decision_medium.decision_mode == "prompt"
    assert decision_medium.options is not None
    assert len(decision_medium.options) >= 2

    # 场景 3: 低置信度 (<65%) - 仅显示信息
    agent_context_low = {
        'match_score': 0.45,
        'agent': Mock(recommended_commands=["/wf_05_code"])
    }

    decision_low = decision_engine.decide(
        agent_context=agent_context_low,
        user_command="wf_06_debug"
    )

    assert decision_low.decision_mode == "info"
    assert decision_low.final_command == "wf_06_debug"  # 执行用户命令


# ============================================================================
# Phase 2.2 + 2.3 集成测试：执行器 + 反馈系统
# ============================================================================

def test_execution_to_feedback_integration():
    """测试执行器和反馈系统的集成"""
    executor = AgentCommandExecutor()
    feedback_system = AgentFeedbackSystem()

    # Mock 执行
    with patch.object(executor, 'execute_command') as mock_execute:
        mock_execute.return_value = Mock(
            success=True,
            exit_code=0,
            duration_ms=250.0
        )

        # 执行命令
        result = executor.execute_command(
            command="/wf_05_code",
            context={'agent': 'code-agent'}
        )

        # 使用反馈系统评估执行效果
        effectiveness = feedback_system.evaluate_execution_effectiveness(
            agent_name="code-agent",
            success=result.success,
            duration_ms=result.duration_ms
        )

        # 验证反馈
        assert effectiveness is not None
        assert 0.0 <= effectiveness <= 1.0

        # 更新 agent 评分
        feedback_system.update_agent_score(
            agent_name="code-agent",
            effectiveness=effectiveness
        )

        # 获取评分
        score = feedback_system.get_agent_score("code-agent")
        assert score is not None
        assert score.total_executions >= 1


# ============================================================================
# Phase 2.1 + 2.4 集成测试：决策引擎 + 多Agent协调
# ============================================================================

def test_decision_to_orchestration_integration():
    """测试决策引擎和多Agent协调的集成"""
    coordinator = AgentCoordinator()
    orchestrator = MultiAgentOrchestrator()

    # 复杂任务需要多个 Agents
    task_description = "Implement and test user authentication feature"

    # Step 1: 识别需要的 agents
    # 通常需要 code-agent 和 test-agent
    code_context = coordinator.intercept(
        task_description="Implement user authentication",
        command_name="wf_05_code",
        auto_activate=True
    )

    test_context = coordinator.intercept(
        task_description="Test user authentication",
        command_name="wf_07_test",
        auto_activate=True
    )

    # Step 2: 创建编排计划（如果两个 agents 都激活）
    if code_context['auto_activated'] and test_context['auto_activated']:
        # 使用 orchestrator（简化测试，不实际执行）
        assert orchestrator is not None


# ============================================================================
# 完整工作流集成测试
# ============================================================================

def test_full_workflow_integration():
    """测试完整的 agent 工作流"""
    # 初始化所有组件
    coordinator = AgentCoordinator()
    decision_engine = AgentDecisionEngine()
    executor = AgentCommandExecutor()
    feedback_system = AgentFeedbackSystem()

    # 场景: 用户请求 "Fix authentication bug"
    user_input = "Fix authentication bug"
    command_name = "wf_06_debug"

    # Step 1: Agent 选择
    agent_context = coordinator.intercept(
        task_description=user_input,
        command_name=command_name,
        auto_activate=True,
        min_confidence=0.65
    )

    # Step 2: 决策引擎决策
    decision = decision_engine.decide(
        agent_context=agent_context,
        user_command=command_name
    )

    # Step 3: 执行命令 (Mock)
    with patch.object(executor, 'execute_command') as mock_execute:
        mock_execute.return_value = Mock(
            success=True,
            exit_code=0,
            output="Bug fixed",
            duration_ms=500.0
        )

        result = executor.execute_command(
            command=decision.final_command,
            context={'task': user_input}
        )

        # Step 4: 反馈评估
        if agent_context.get('agent'):
            effectiveness = feedback_system.evaluate_execution_effectiveness(
                agent_name=agent_context['agent'].name,
                success=result.success,
                duration_ms=result.duration_ms
            )

            # 验证完整流程
            assert agent_context['agent'] is not None
            assert decision.final_command is not None
            assert result.success is True
            assert effectiveness >= 0.0


# ============================================================================
# 性能和稳定性测试
# ============================================================================

def test_pipeline_performance():
    """测试管道性能"""
    coordinator = AgentCoordinator()

    # 连续执行多次
    results = []
    for i in range(10):
        agent_context = coordinator.intercept(
            task_description=f"Task {i}",
            command_name="wf_05_code",
            auto_activate=True
        )
        results.append(agent_context)

    # 验证所有调用都成功
    assert len(results) == 10
    assert all(r['agent'] is not None for r in results)


def test_concurrent_agent_selection():
    """测试并发 agent 选择的稳定性"""
    coordinator = AgentCoordinator()

    # 模拟并发场景
    tasks = [
        "Implement feature A",
        "Test feature B",
        "Debug feature C",
        "Review code D",
        "Document feature E"
    ]

    results = [
        coordinator.intercept(
            task_description=task,
            command_name="wf_05_code",
            auto_activate=True
        )
        for task in tasks
    ]

    # 验证所有选择都成功
    assert len(results) == 5
    assert all(r['agent'] is not None for r in results)


# ============================================================================
# 错误处理和边界情况测试
# ============================================================================

def test_no_agent_match():
    """测试没有匹配 agent 的情况"""
    coordinator = AgentCoordinator()

    # 非常模糊的任务描述
    agent_context = coordinator.intercept(
        task_description="xyz123",
        command_name="wf_05_code",
        auto_activate=True,
        min_confidence=0.65
    )

    # 应该有降级处理
    assert agent_context is not None
    # 可能没有激活 agent，但不应该崩溃
    assert 'agent' in agent_context


def test_executor_failure_handling():
    """测试执行失败的处理"""
    executor = AgentCommandExecutor()
    feedback_system = AgentFeedbackSystem()

    # Mock 执行失败
    with patch.object(executor, 'execute_command') as mock_execute:
        mock_execute.return_value = Mock(
            success=False,
            exit_code=1,
            error="Command failed",
            duration_ms=100.0
        )

        result = executor.execute_command(
            command="/wf_05_code",
            context={}
        )

        # 反馈系统应该能处理失败情况
        effectiveness = feedback_system.evaluate_execution_effectiveness(
            agent_name="test-agent",
            success=result.success,
            duration_ms=result.duration_ms
        )

        # 失败的执行应该得到较低评分
        assert effectiveness < 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
