"""
Tests for Agent Execution Pipeline - Phase 2.5

端到端集成测试，验证所有 Phase 2.1-2.4 组件的集成。
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from commands.lib.agent_execution_pipeline import (
    AgentExecutionPipeline,
    PipelineConfig,
    PipelineResult
)
from commands.lib.agent_decision_engine import DecisionResult
from commands.lib.agent_command_executor import ExecutionResult
from commands.lib.agent_registry import Agent
from commands.lib.multi_agent_orchestrator import (
    AgentTask,
    ExecutionMode,
    ConflictResolutionStrategy,
    OrchestrationResult
)


# ============================================================================
# 基础测试
# ============================================================================

def test_pipeline_initialization():
    """测试管道初始化"""
    pipeline = AgentExecutionPipeline()

    assert pipeline.decision_engine is not None
    assert pipeline.executor is not None
    assert pipeline.feedback_system is not None
    assert pipeline.orchestrator is not None
    assert pipeline.history is not None
    assert pipeline._pipeline_counter == 0


def test_pipeline_initialization_with_custom_config():
    """测试使用自定义配置初始化管道"""
    config = PipelineConfig(
        decision_confidence_threshold=0.90,
        execution_timeout=60,
        enable_feedback=False,
        enable_history=False
    )

    pipeline = AgentExecutionPipeline(config)

    assert pipeline.config.decision_confidence_threshold == 0.90
    assert pipeline.config.execution_timeout == 60
    assert pipeline.config.enable_feedback is False
    assert pipeline.history is None  # 因为 enable_history=False


# ============================================================================
# 单 Agent 执行测试
# ============================================================================

def test_execute_single_agent_success():
    """测试单 Agent 成功执行流程"""
    pipeline = AgentExecutionPipeline()

    # Mock 决策引擎
    mock_agent = Agent(
        name="test-agent",
        description="Test agent",
        keywords=["test"],
        expertise=["testing"],
        available_tools=[],
        role="Testing",
        recommended_commands=["/wf_05_code"]
    )

    mock_decision = DecisionResult(
        matched_agent=mock_agent,
        confidence=0.95,
        recommended_command="/wf_05_code",
        reasoning="High confidence match",
        context_hints={}
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)

    # Mock 执行器
    mock_execution = ExecutionResult(
        success=True,
        command="/wf_05_code",
        exit_code=0,
        output="Success",
        duration_ms=100.0
    )

    pipeline.executor.execute_command = Mock(return_value=mock_execution)

    # 执行
    result = pipeline.execute_single_agent(
        user_input="Implement feature X",
        command_name="wf_05_code"
    )

    # 验证
    assert result.success is True
    assert result.decision_result == mock_decision
    assert result.execution_result == mock_execution
    assert result.decision_duration_ms > 0
    assert result.execution_duration_ms > 0
    assert result.total_duration_ms > 0


def test_execute_single_agent_low_confidence():
    """测试低置信度决策被跳过"""
    config = PipelineConfig(decision_confidence_threshold=0.85)
    pipeline = AgentExecutionPipeline(config)

    # Mock 低置信度决策
    mock_decision = DecisionResult(
        matched_agent=None,
        confidence=0.50,  # 低于阈值
        recommended_command="",
        reasoning="Low confidence",
        context_hints={}
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)

    # 执行
    result = pipeline.execute_single_agent(
        user_input="Unclear task",
        command_name="wf_05_code"
    )

    # 验证 - 应该成功但跳过执行
    assert result.success is True
    assert result.metadata.get('skipped') is True
    assert result.metadata.get('reason') == 'Low confidence decision'
    assert result.execution_result is None


def test_execute_single_agent_execution_failure():
    """测试执行失败的情况"""
    pipeline = AgentExecutionPipeline()

    # Mock 成功决策
    mock_agent = Agent(
        name="test-agent",
        description="Test agent",
        keywords=["test"],
        expertise=["testing"],
        available_tools=[],
        role="Testing",
        recommended_commands=["/wf_05_code"]
    )

    mock_decision = DecisionResult(
        matched_agent=mock_agent,
        confidence=0.95,
        recommended_command="/wf_05_code",
        reasoning="High confidence",
        context_hints={}
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)

    # Mock 执行失败
    mock_execution = ExecutionResult(
        success=False,
        command="/wf_05_code",
        exit_code=1,
        error="Execution failed",
        duration_ms=50.0
    )

    pipeline.executor.execute_command = Mock(return_value=mock_execution)

    # 执行
    result = pipeline.execute_single_agent(
        user_input="Implement feature X",
        command_name="wf_05_code"
    )

    # 验证
    assert result.success is False
    assert result.execution_result.success is False
    assert result.execution_result.error == "Execution failed"


def test_execute_single_agent_with_feedback():
    """测试带反馈的单 Agent 执行"""
    config = PipelineConfig(enable_feedback=True, enable_history=True)
    pipeline = AgentExecutionPipeline(config)

    # Mock 决策和执行
    mock_agent = Agent(
        name="test-agent",
        description="Test agent",
        keywords=["test"],
        expertise=["testing"],
        available_tools=[],
        role="Testing",
        recommended_commands=["/wf_05_code"]
    )

    mock_decision = DecisionResult(
        matched_agent=mock_agent,
        confidence=0.95,
        recommended_command="/wf_05_code",
        reasoning="High confidence",
        context_hints={}
    )

    mock_execution = ExecutionResult(
        success=True,
        command="/wf_05_code",
        exit_code=0,
        output="Success",
        duration_ms=100.0
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)
    pipeline.executor.execute_command = Mock(return_value=mock_execution)

    # 执行
    result = pipeline.execute_single_agent(
        user_input="Implement feature X",
        command_name="wf_05_code"
    )

    # 验证反馈
    assert result.success is True
    assert result.feedback_score is not None
    assert result.feedback_score >= 0.0 and result.feedback_score <= 1.0


def test_execute_single_agent_exception_handling():
    """测试异常处理"""
    pipeline = AgentExecutionPipeline()

    # Mock 决策引擎抛出异常
    pipeline.decision_engine.analyze_and_recommend = Mock(
        side_effect=Exception("Decision engine error")
    )

    # 执行
    result = pipeline.execute_single_agent(
        user_input="Test input",
        command_name="wf_05_code"
    )

    # 验证
    assert result.success is False
    assert result.error == "Decision engine error"
    assert result.error_stage == "decision"


# ============================================================================
# 多 Agent 协调测试
# ============================================================================

def test_execute_multi_agent_success():
    """测试多 Agent 协调成功执行"""
    pipeline = AgentExecutionPipeline()

    # 创建测试任务
    tasks = [
        AgentTask(
            agent_name="agent1",
            command="/wf_05_code",
            priority=1,
            dependencies=[]
        ),
        AgentTask(
            agent_name="agent2",
            command="/wf_07_test",
            priority=2,
            dependencies=["agent1"]
        )
    ]

    # Mock 协调器
    mock_orchestration = OrchestrationResult(
        success=True,
        mode=ExecutionMode.SEQUENTIAL,
        task_results={
            "agent1": {"success": True, "duration_ms": 100.0},
            "agent2": {"success": True, "duration_ms": 150.0}
        },
        execution_order=["agent1", "agent2"],
        total_duration_ms=250.0
    )

    pipeline.orchestrator.execute_plan = Mock(return_value=mock_orchestration)

    # 执行
    result = pipeline.execute_multi_agent(
        tasks=tasks,
        execution_mode=ExecutionMode.SEQUENTIAL
    )

    # 验证
    assert result.success is True
    assert result.orchestration_result == mock_orchestration
    assert len(result.agent_scores) > 0


def test_execute_multi_agent_parallel_mode():
    """测试并行执行模式"""
    pipeline = AgentExecutionPipeline()

    tasks = [
        AgentTask(
            agent_name="agent1",
            command="/wf_05_code",
            priority=1,
            dependencies=[]
        ),
        AgentTask(
            agent_name="agent2",
            command="/wf_05_code",
            priority=1,
            dependencies=[]
        )
    ]

    # Mock 并行执行结果
    mock_orchestration = OrchestrationResult(
        success=True,
        mode=ExecutionMode.PARALLEL,
        task_results={
            "agent1": {"success": True, "duration_ms": 100.0},
            "agent2": {"success": True, "duration_ms": 120.0}
        },
        execution_order=["agent1", "agent2"],
        total_duration_ms=120.0  # 并行所以取最大值
    )

    pipeline.orchestrator.execute_plan = Mock(return_value=mock_orchestration)

    # 执行
    result = pipeline.execute_multi_agent(
        tasks=tasks,
        execution_mode=ExecutionMode.PARALLEL
    )

    # 验证
    assert result.success is True
    assert result.orchestration_result.mode == ExecutionMode.PARALLEL


def test_execute_multi_agent_with_conflict_resolution():
    """测试冲突解决策略"""
    pipeline = AgentExecutionPipeline()

    tasks = [
        AgentTask(
            agent_name="agent1",
            command="/wf_05_code",
            priority=1,
            dependencies=[]
        ),
        AgentTask(
            agent_name="agent2",
            command="/wf_05_code",
            priority=2,
            dependencies=[]
        )
    ]

    mock_orchestration = OrchestrationResult(
        success=True,
        mode=ExecutionMode.SEQUENTIAL,
        task_results={
            "agent1": {"success": True, "duration_ms": 100.0},
            "agent2": {"success": True, "duration_ms": 150.0}
        },
        execution_order=["agent2", "agent1"],  # 按优先级排序
        total_duration_ms=250.0
    )

    pipeline.orchestrator.execute_plan = Mock(return_value=mock_orchestration)

    # 执行
    result = pipeline.execute_multi_agent(
        tasks=tasks,
        conflict_strategy=ConflictResolutionStrategy.PRIORITY_BASED
    )

    # 验证
    assert result.success is True
    assert result.orchestration_result.execution_order == ["agent2", "agent1"]


def test_execute_multi_agent_failure():
    """测试多 Agent 执行失败"""
    pipeline = AgentExecutionPipeline()

    tasks = [
        AgentTask(
            agent_name="agent1",
            command="/wf_05_code",
            priority=1,
            dependencies=[]
        )
    ]

    # Mock 失败结果
    mock_orchestration = OrchestrationResult(
        success=False,
        mode=ExecutionMode.SEQUENTIAL,
        task_results={
            "agent1": {"success": False, "error": "Task failed", "duration_ms": 50.0}
        },
        execution_order=["agent1"],
        total_duration_ms=50.0
    )

    pipeline.orchestrator.execute_plan = Mock(return_value=mock_orchestration)

    # 执行
    result = pipeline.execute_multi_agent(tasks=tasks)

    # 验证
    assert result.success is False


def test_execute_multi_agent_exception_handling():
    """测试多 Agent 异常处理"""
    pipeline = AgentExecutionPipeline()

    tasks = [
        AgentTask(
            agent_name="agent1",
            command="/wf_05_code",
            priority=1,
            dependencies=[]
        )
    ]

    # Mock 协调器抛出异常
    pipeline.orchestrator.execute_plan = Mock(
        side_effect=Exception("Orchestration error")
    )

    # 执行
    result = pipeline.execute_multi_agent(tasks=tasks)

    # 验证
    assert result.success is False
    assert result.error == "Orchestration error"
    assert result.error_stage == "orchestration"


# ============================================================================
# 统计和监控测试
# ============================================================================

def test_get_pipeline_statistics():
    """测试获取管道统计信息"""
    pipeline = AgentExecutionPipeline()

    # 执行一些操作以生成统计
    mock_decision = DecisionResult(
        matched_agent=Agent(
            name="test-agent",
            description="Test",
            keywords=["test"],
            expertise=["testing"],
            available_tools=[],
            role="Testing",
            recommended_commands=["/wf_05_code"]
        ),
        confidence=0.95,
        recommended_command="/wf_05_code",
        reasoning="Test",
        context_hints={}
    )

    mock_execution = ExecutionResult(
        success=True,
        command="/wf_05_code",
        exit_code=0,
        output="Success",
        duration_ms=100.0
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)
    pipeline.executor.execute_command = Mock(return_value=mock_execution)

    # 执行几次
    for _ in range(3):
        pipeline.execute_single_agent(
            user_input="Test",
            command_name="wf_05_code"
        )

    # 获取统计
    stats = pipeline.get_pipeline_statistics()

    # 验证
    assert stats['total_pipelines_executed'] == 3
    assert 'config' in stats
    assert stats['config']['decision_threshold'] == 0.85
    assert 'execution_history' in stats
    assert 'feedback_summary' in stats


def test_reset_statistics():
    """测试重置统计信息"""
    pipeline = AgentExecutionPipeline()

    # 执行一些操作
    pipeline._pipeline_counter = 10

    # 重置
    pipeline.reset_statistics()

    # 验证
    assert pipeline._pipeline_counter == 0


# ============================================================================
# 性能测试
# ============================================================================

def test_pipeline_performance_single_agent():
    """测试单 Agent 执行性能"""
    pipeline = AgentExecutionPipeline()

    # Mock 快速响应
    mock_decision = DecisionResult(
        matched_agent=Agent(
            name="test-agent",
            description="Test",
            keywords=["test"],
            expertise=["testing"],
            available_tools=[],
            role="Testing",
            recommended_commands=["/wf_05_code"]
        ),
        confidence=0.95,
        recommended_command="/wf_05_code",
        reasoning="Test",
        context_hints={}
    )

    mock_execution = ExecutionResult(
        success=True,
        command="/wf_05_code",
        exit_code=0,
        output="Success",
        duration_ms=50.0
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)
    pipeline.executor.execute_command = Mock(return_value=mock_execution)

    # 执行并测量时间
    result = pipeline.execute_single_agent(
        user_input="Test",
        command_name="wf_05_code"
    )

    # 验证性能指标
    assert result.total_duration_ms > 0
    assert result.decision_duration_ms >= 0
    assert result.execution_duration_ms >= 0
    assert result.total_duration_ms >= (result.decision_duration_ms + result.execution_duration_ms)


def test_pipeline_performance_multi_agent():
    """测试多 Agent 执行性能"""
    pipeline = AgentExecutionPipeline()

    tasks = [
        AgentTask(
            agent_name=f"agent{i}",
            command="/wf_05_code",
            priority=i,
            dependencies=[]
        )
        for i in range(5)
    ]

    # Mock 快速并行执行
    mock_orchestration = OrchestrationResult(
        success=True,
        mode=ExecutionMode.PARALLEL,
        task_results={
            f"agent{i}": {"success": True, "duration_ms": 100.0}
            for i in range(5)
        },
        execution_order=[f"agent{i}" for i in range(5)],
        total_duration_ms=100.0  # 并行执行
    )

    pipeline.orchestrator.execute_plan = Mock(return_value=mock_orchestration)

    # 执行
    result = pipeline.execute_multi_agent(
        tasks=tasks,
        execution_mode=ExecutionMode.PARALLEL
    )

    # 验证 - 并行执行应该比顺序快
    assert result.success is True
    assert result.total_duration_ms > 0


# ============================================================================
# 集成场景测试
# ============================================================================

def test_end_to_end_workflow():
    """测试完整的端到端工作流"""
    pipeline = AgentExecutionPipeline()

    # 场景: 用户请求实现功能
    user_input = "Implement user authentication feature"
    command_name = "wf_05_code"

    # Mock 所有组件
    mock_agent = Agent(
        name="code-agent",
        description="Implementation Engineer",
        keywords=["implement", "code", "feature"],
        expertise=["coding", "development"],
        available_tools=[],
        role="Developer",
        recommended_commands=["/wf_05_code"]
    )

    mock_decision = DecisionResult(
        matched_agent=mock_agent,
        confidence=0.92,
        recommended_command="/wf_05_code",
        reasoning="High confidence for code implementation",
        context_hints={"complexity": "medium"}
    )

    mock_execution = ExecutionResult(
        success=True,
        command="/wf_05_code",
        exit_code=0,
        output="Feature implemented successfully",
        duration_ms=2500.0
    )

    pipeline.decision_engine.analyze_and_recommend = Mock(return_value=mock_decision)
    pipeline.executor.execute_command = Mock(return_value=mock_execution)

    # 执行完整流程
    result = pipeline.execute_single_agent(
        user_input=user_input,
        command_name=command_name,
        context={"project": "auth-system"}
    )

    # 验证完整流程
    assert result.success is True
    assert result.decision_result.confidence == 0.92
    assert result.execution_result.success is True
    assert result.feedback_score is not None
    assert "code-agent" in result.agent_scores
    assert result.total_duration_ms > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
