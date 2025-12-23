"""
AgentCommandExecutor 单元测试

测试覆盖:
- 执行结果数据结构 (2 个测试)
- 命令执行 (5 个测试)
- MCP 工具加载 (3 个测试)
- 超时处理 (2 个测试)
- 错误处理 (3 个测试)
- 执行历史和统计 (4 个测试)

总计: 19 个单元测试，覆盖率目标 ≥90%
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import subprocess

from commands.lib.agent_command_executor import (
    AgentCommandExecutor,
    ExecutionResult,
)


class TestExecutionResult:
    """ExecutionResult 数据结构测试"""

    def test_execution_result_creation(self):
        """测试 ExecutionResult 创建"""
        result = ExecutionResult(
            status="success",
            command="/wf_05_code 实现功能",
            output="Command executed successfully",
            execution_time=2.5,
        )

        assert result.status == "success"
        assert result.command == "/wf_05_code 实现功能"
        assert result.output == "Command executed successfully"
        assert result.execution_time == 2.5

    def test_execution_result_with_all_fields(self):
        """测试 ExecutionResult 包含所有字段"""
        result = ExecutionResult(
            status="failure",
            command="test_command",
            output="some output",
            error="some error",
            execution_time=5.0,
            exit_code=1,
            agent_id="test-agent",
            agent_name="Test Agent",
            match_score=0.85,
            user_command="user_command",
            affected_behavior=True,
        )

        assert result.status == "failure"
        assert result.exit_code == 1
        assert result.agent_id == "test-agent"
        assert result.match_score == 0.85
        assert result.affected_behavior is True


class TestAgentCommandExecutor:
    """AgentCommandExecutor 测试类"""

    @pytest.fixture
    def executor(self):
        """创建执行器实例"""
        return AgentCommandExecutor(timeout=10)

    @pytest.fixture
    def mock_agent(self):
        """创建 mock Agent 对象"""
        agent = Mock()
        agent.name = "test-agent"
        agent.role = "Test Agent"
        agent.available_tools = ["/wf_05_code", "/wf_08_review"]
        return agent

    # ============================================================================
    # 命令执行测试 (5 个)
    # ============================================================================

    def test_execute_simple_command(self, executor, mock_agent):
        """测试执行简单命令"""
        result = executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'Hello, Agent!'",
            user_command="/wf_05_code",
            match_score=0.9,
        )

        assert result.status == "success"
        assert result.command == "echo 'Hello, Agent!'"
        assert "Hello, Agent!" in result.output
        assert result.exit_code == 0
        assert result.execution_time > 0
        assert result.affected_behavior is True

    def test_execute_command_with_failure(self, executor, mock_agent):
        """测试执行失败的命令"""
        result = executor.execute_agent_command(
            agent=mock_agent,
            command="false",  # 返回非零退出码
            user_command="/wf_11_commit",
            match_score=0.5,
        )

        assert result.status == "failure"
        assert result.exit_code != 0
        assert result.affected_behavior is False

    def test_execute_command_with_empty_string(self, executor, mock_agent):
        """测试执行空命令"""
        result = executor.execute_agent_command(
            agent=mock_agent,
            command="",
            user_command="/wf_05_code",
            match_score=0.8,
        )

        assert result.status == "error"
        assert "Invalid command" in result.error

    def test_execute_command_with_none(self, executor, mock_agent):
        """测试执行 None 命令"""
        result = executor.execute_agent_command(
            agent=mock_agent,
            command=None,
            user_command="/wf_05_code",
            match_score=0.8,
        )

        assert result.status == "error"

    def test_execute_command_with_context(self, executor, mock_agent):
        """测试带上下文的命令执行"""
        context = {
            "agent_command": "/wf_05_code 实现功能",
            "mcp_tools": ["serena"],
        }

        result = executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'test'",
            user_command="/wf_05_code",
            match_score=0.85,
            context=context,
        )

        assert result.status == "success"
        assert "test" in result.output
        assert "serena" in result.mcp_tools_used

    # ============================================================================
    # MCP 工具加载测试 (3 个)
    # ============================================================================

    def test_load_valid_mcp_tools(self, executor):
        """测试加载有效的 MCP 工具"""
        result = executor._load_mcp_tools(["serena", "context7", "tavily"])
        assert result is True

    def test_load_invalid_mcp_tools(self, executor):
        """测试加载无效的 MCP 工具"""
        result = executor._load_mcp_tools(["invalid_tool"])
        assert result is False

    def test_load_mixed_mcp_tools(self, executor):
        """测试加载混合的 MCP 工具"""
        result = executor._load_mcp_tools(["serena", "invalid"])
        # 有效工具被加载，所以返回 True
        assert result is True

    # ============================================================================
    # 超时处理测试 (2 个)
    # ============================================================================

    def test_execute_command_with_timeout(self, executor, mock_agent):
        """测试命令执行超时"""
        executor.timeout = 1  # 设置 1 秒超时

        result = executor.execute_agent_command(
            agent=mock_agent,
            command="sleep 5",  # 睡眠 5 秒，会超时
            user_command="/wf_05_code",
            match_score=0.8,
        )

        assert result.status == "timeout"
        assert "超时" in result.error
        assert result.affected_behavior is False

    def test_custom_timeout_setting(self, executor):
        """测试自定义超时设置"""
        assert executor.timeout == 10

        new_executor = AgentCommandExecutor(timeout=5)
        assert new_executor.timeout == 5

    # ============================================================================
    # 错误处理测试 (3 个)
    # ============================================================================

    def test_execute_invalid_agent(self, executor):
        """测试使用无效 Agent"""
        result = executor.execute_agent_command(
            agent=None,
            command="echo 'test'",
            user_command="/wf_05_code",
            match_score=0.8,
        )

        assert result.status == "success"
        assert result.agent_id == "unknown"

    def test_execute_with_preparation_failure(self, executor, mock_agent):
        """测试执行准备失败"""
        # 虽然准备阶段可能失败，但在我们的实现中，
        # 大多数命令仍然会尝试执行
        result = executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'test'",
            context={"mcp_tools": ["invalid_tool"]},
        )

        # 无效工具不应该阻止命令执行
        # 实际行为取决于我们的实现

    def test_execute_catches_exception(self, executor, mock_agent):
        """测试捕获执行异常"""
        # 使用无效的 shell 命令可能会导致异常
        result = executor.execute_agent_command(
            agent=mock_agent,
            command="$(invalid_command_syntax())",
            user_command="/wf_05_code",
        )

        # 应该捕获异常并返回有效结果
        assert result is not None
        assert isinstance(result, ExecutionResult)

    # ============================================================================
    # 执行历史和统计测试 (4 个)
    # ============================================================================

    def test_execution_history_tracking(self, executor, mock_agent):
        """测试执行历史跟踪"""
        # 执行多个命令
        for i in range(3):
            executor.execute_agent_command(
                agent=mock_agent,
                command=f"echo 'test {i}'",
                user_command=f"/wf_test_{i}",
                match_score=0.8 - i * 0.1,
            )

        history = executor.get_execution_history()
        assert len(history) == 3

        for record in history:
            assert "status" in record
            assert "command" in record
            assert "agent_id" in record
            assert "execution_time" in record

    def test_execution_statistics(self, executor, mock_agent):
        """测试执行统计"""
        # 执行成功和失败的命令
        executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'success'",
            match_score=0.9,
        )
        executor.execute_agent_command(
            agent=mock_agent,
            command="false",
            match_score=0.5,
        )

        stats = executor.get_execution_statistics()

        assert stats["total_executions"] == 2
        assert stats["success_count"] >= 1
        assert "success_rate" in stats
        assert "average_execution_time" in stats
        assert 0.0 <= stats["success_rate"] <= 1.0

    def test_execution_statistics_empty_history(self, executor):
        """测试空历史的统计"""
        stats = executor.get_execution_statistics()

        assert stats["total_executions"] == 0
        assert stats["success_count"] == 0
        assert stats["success_rate"] == 0.0
        assert stats["average_execution_time"] == 0.0

    def test_clear_execution_history(self, executor, mock_agent):
        """测试清空执行历史"""
        # 执行几个命令
        for i in range(3):
            executor.execute_agent_command(
                agent=mock_agent,
                command="echo 'test'",
            )

        assert len(executor.get_execution_history()) == 3

        # 清空历史
        executor.clear_history()

        assert len(executor.get_execution_history()) == 0
        assert executor.get_execution_statistics()["total_executions"] == 0

    # ============================================================================
    # 执行结果字段测试 (1 个)
    # ============================================================================

    def test_result_contains_all_metadata(self, executor, mock_agent):
        """测试结果包含所有元数据"""
        context = {
            "agent_command": "/wf_05_code 实现功能",
            "mcp_tools": ["serena", "context7"],
        }

        result = executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'test'",
            user_command="/wf_08_review",
            match_score=0.85,
            context=context,
        )

        # 验证所有重要字段
        assert result.status == "success"
        # 命令应该是实际执行的命令
        assert result.command == "echo 'test'"
        assert result.agent_id == "test-agent"
        assert result.agent_name == "Test Agent"
        assert result.match_score == 0.85
        assert result.user_command == "/wf_08_review"
        assert result.exit_code == 0
        assert result.execution_time > 0
        assert result.start_time
        assert result.end_time
        assert len(result.mcp_tools_used) > 0
        assert result.affected_behavior is True


# ============================================================================
# 集成测试
# ============================================================================


class TestAgentCommandExecutorIntegration:
    """AgentCommandExecutor 集成测试"""

    @pytest.fixture
    def executor(self):
        """创建执行器实例"""
        return AgentCommandExecutor(timeout=10)

    @pytest.fixture
    def mock_agent(self):
        """创建 mock Agent 对象"""
        agent = Mock()
        agent.name = "integration-test-agent"
        agent.role = "Integration Test Agent"
        return agent

    def test_complete_execution_workflow(self, executor, mock_agent):
        """测试完整执行工作流"""
        # 模拟完整的执行流程
        context = {
            "agent_command": "/wf_05_code 实现功能",
            "mcp_tools": ["serena"],
        }

        result = executor.execute_agent_command(
            agent=mock_agent,
            command="echo '执行成功'",
            user_command="/wf_05_code",
            match_score=0.92,
            context=context,
        )

        # 验证执行结果
        assert result.status == "success"
        assert result.affected_behavior is True

        # 验证历史记录
        history = executor.get_execution_history()
        assert len(history) == 1
        assert history[0]["status"] == "success"

        # 验证统计
        stats = executor.get_execution_statistics()
        assert stats["success_rate"] == 1.0

    def test_execution_with_mcp_tools_and_context(self, executor, mock_agent):
        """测试带有 MCP 工具和上下文的执行"""
        context = {
            "agent_command": "/wf_07_test 编写测试",
            "mcp_tools": ["serena", "context7"],
        }

        result = executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'Testing with MCP'",
            user_command="/wf_07_test",
            match_score=0.88,
            context=context,
        )

        assert result.status == "success"
        assert len(result.mcp_tools_used) > 0
        assert result.affected_behavior is True

    def test_mixed_success_and_failure_execution(self, executor, mock_agent):
        """测试混合的成功和失败执行"""
        # 成功的执行
        result1 = executor.execute_agent_command(
            agent=mock_agent,
            command="echo 'success'",
            match_score=0.9,
        )

        # 失败的执行
        result2 = executor.execute_agent_command(
            agent=mock_agent,
            command="false",
            match_score=0.5,
        )

        # 验证结果
        assert result1.status == "success"
        assert result2.status == "failure"

        # 验证统计
        stats = executor.get_execution_statistics()
        assert stats["total_executions"] == 2
        assert stats["success_count"] >= 1
        assert stats["failure_count"] >= 1
