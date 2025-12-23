"""
AgentFeedbackSystem 和 AgentExecutionHistory 单元测试

测试覆盖:
- 执行历史记录 (3 个测试)
- 有效性评估 (3 个测试)
- Agent 评分更新 (2 个测试)
- 反馈报告 (2 个测试)

总计: 10 个单元测试
"""

import pytest
from datetime import datetime
from unittest.mock import Mock

from commands.lib.agent_feedback_system import (
    AgentFeedbackSystem,
    AgentScore,
)
from commands.lib.agent_execution_history import (
    AgentExecutionHistory,
    ExecutionRecord,
)


class TestAgentExecutionHistory:
    """AgentExecutionHistory 测试类"""

    @pytest.fixture
    def history(self):
        """创建执行历史实例"""
        return AgentExecutionHistory()

    def test_add_and_retrieve_records(self, history):
        """测试添加和检索记录"""
        record = ExecutionRecord(
            timestamp=datetime.now().isoformat(),
            agent_id="test-agent",
            agent_name="Test Agent",
            user_command="/wf_05_code",
            agent_recommendation="/wf_05_code 实现功能",
            executed_command="/wf_05_code 实现功能",
            execution_status="success",
            exit_code=0,
            match_score=0.9,
            was_adopted=True,
        )

        history.add_record(record)
        records = history.get_records_by_agent("test-agent")

        assert len(records) == 1
        assert records[0].agent_id == "test-agent"
        assert records[0].execution_status == "success"

    def test_get_agent_statistics(self, history):
        """测试获取 Agent 统计信息"""
        # 添加多条记录
        for i, status in enumerate(["success", "success", "failure"]):
            record = ExecutionRecord(
                timestamp=datetime.now().isoformat(),
                agent_id="test-agent",
                agent_name="Test Agent",
                user_command=f"/wf_{i}",
                agent_recommendation=f"/wf_{i} test",
                executed_command=f"/wf_{i} test",
                execution_status=status,
                was_adopted=i < 2,  # 前两个被采纳
                effectiveness=1.0 if status == "success" else 0.3,
            )
            history.add_record(record)

        stats = history.get_agent_statistics("test-agent")

        assert stats["total_executions"] == 3
        assert stats["success_count"] == 2
        assert stats["failure_count"] == 1
        assert stats["adoption_rate"] == 2 / 3
        assert stats["success_rate"] == 2 / 3

    def test_get_recent_records(self, history):
        """测试获取最近的记录"""
        for i in range(5):
            record = ExecutionRecord(
                timestamp=datetime.now().isoformat(),
                agent_id="test-agent",
                agent_name="Test Agent",
                user_command=f"/wf_{i}",
                agent_recommendation=f"/wf_{i}",
                executed_command=f"/wf_{i}",
                execution_status="success",
            )
            history.add_record(record)

        recent = history.get_recent_records("test-agent", limit=3)
        assert len(recent) == 3


class TestAgentFeedbackSystem:
    """AgentFeedbackSystem 测试类"""

    @pytest.fixture
    def feedback_system(self):
        """创建反馈系统实例"""
        return AgentFeedbackSystem()

    def test_record_execution(self, feedback_system):
        """测试记录执行"""
        record = feedback_system.record_execution(
            agent_id="code-agent",
            agent_name="Code Agent",
            user_command="/wf_05_code",
            agent_recommendation="/wf_05_code 实现功能",
            executed_command="/wf_05_code 实现功能",
            execution_status="success",
            match_score=0.9,
            was_adopted=True,
        )

        assert record.agent_id == "code-agent"
        assert record.execution_status == "success"
        assert record.was_adopted is True

    def test_evaluate_effectiveness_success(self, feedback_system):
        """测试成功执行的有效性评估"""
        effectiveness = feedback_system.evaluate_effectiveness(
            execution_status="success",
            was_adopted=True,
            match_score=0.9,
        )

        # 成功 (1.0) + 采纳奖励 (0.2) + 匹配奖励 (0.18) = 1.0 (capped)
        assert effectiveness > 0.8
        assert effectiveness <= 1.0

    def test_evaluate_effectiveness_failure(self, feedback_system):
        """测试失败执行的有效性评估"""
        effectiveness = feedback_system.evaluate_effectiveness(
            execution_status="failure",
            was_adopted=False,
            match_score=0.5,
        )

        # 失败 (0.3) + 无采纳 (0) + 匹配奖励 (0.1) = 0.4
        assert 0.3 <= effectiveness <= 0.5

    def test_update_and_get_agent_score(self, feedback_system):
        """测试更新和获取 Agent 评分"""
        # 添加一些执行记录
        for _ in range(3):
            feedback_system.record_execution(
                agent_id="test-agent",
                agent_name="Test Agent",
                user_command="/wf_test",
                agent_recommendation="/wf_test 推荐",
                executed_command="/wf_test 推荐",
                execution_status="success",
                was_adopted=True,
            )

        score = feedback_system.update_agent_score("test-agent", "Test Agent")

        assert score.agent_id == "test-agent"
        assert score.composite_score > 0.5
        assert score.adoption_rate > 0.5

    def test_get_top_and_bottom_agents(self, feedback_system):
        """测试获取顶级和低效 Agent"""
        # 创建多个 Agent
        agents_data = [
            ("agent-1", "Agent 1", "success", True, 5),   # 高分
            ("agent-2", "Agent 2", "failure", False, 5),  # 低分
            ("agent-3", "Agent 3", "success", True, 3),   # 中等
        ]

        for agent_id, agent_name, status, adopted, count in agents_data:
            for _ in range(count):
                feedback_system.record_execution(
                    agent_id=agent_id,
                    agent_name=agent_name,
                    user_command="/wf_test",
                    agent_recommendation="/wf_test",
                    executed_command="/wf_test",
                    execution_status=status,
                    was_adopted=adopted,
                )
            feedback_system.update_agent_score(agent_id, agent_name)

        top = feedback_system.get_top_agents(2)
        bottom = feedback_system.get_bottom_agents(2)

        assert len(top) == 2
        assert len(bottom) == 2
        assert top[0].composite_score >= top[1].composite_score
        assert bottom[0].composite_score <= bottom[1].composite_score

    def test_should_recommend_agent(self, feedback_system):
        """测试是否应该推荐 Agent"""
        # 高分 Agent
        for _ in range(10):
            feedback_system.record_execution(
                agent_id="good-agent",
                agent_name="Good Agent",
                user_command="/wf_test",
                agent_recommendation="/wf_test",
                executed_command="/wf_test",
                execution_status="success",
                was_adopted=True,
            )
        feedback_system.update_agent_score("good-agent", "Good Agent")

        # 低分 Agent
        for _ in range(10):
            feedback_system.record_execution(
                agent_id="bad-agent",
                agent_name="Bad Agent",
                user_command="/wf_test",
                agent_recommendation="/wf_test",
                executed_command="/wf_test",
                execution_status="failure",
                was_adopted=False,
            )
        feedback_system.update_agent_score("bad-agent", "Bad Agent")

        # 新 Agent
        assert feedback_system.should_recommend_agent("new-agent") is True
        assert feedback_system.should_recommend_agent("good-agent", min_score=0.7) is True
        assert feedback_system.should_recommend_agent("bad-agent", min_score=0.7) is False

    def test_get_recommendation_impact(self, feedback_system):
        """测试获取推荐影响"""
        # 添加一些执行记录
        for i in range(5):
            feedback_system.record_execution(
                agent_id="agent-1",
                agent_name="Agent 1",
                user_command=f"/wf_{i}",
                agent_recommendation=f"/wf_{i}",
                executed_command=f"/wf_{i}",
                execution_status="success" if i < 4 else "failure",
                was_adopted=i < 3,
            )

        impact = feedback_system.get_recommendation_impact()

        assert impact["total_recommendations"] == 5
        assert impact["adoption_rate"] == 3 / 5
        assert impact["success_rate"] == 4 / 5
        assert impact["total_agents"] == 1

    def test_generate_feedback_report(self, feedback_system):
        """测试生成反馈报告"""
        # 添加一些执行记录
        for _ in range(3):
            feedback_system.record_execution(
                agent_id="test-agent",
                agent_name="Test Agent",
                user_command="/wf_test",
                agent_recommendation="/wf_test",
                executed_command="/wf_test",
                execution_status="success",
                was_adopted=True,
            )
        feedback_system.update_agent_score("test-agent", "Test Agent")

        report = feedback_system.generate_feedback_report()

        assert "Agent Feedback System Report" in report
        assert "Global Statistics" in report
        assert "Top 5 Agents" in report
        assert "Test Agent" in report
